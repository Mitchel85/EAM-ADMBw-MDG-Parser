#!/usr/bin/env python3
"""
EAM-ADMBw-MDG-Parser — extrahiert aus einer Sparx-MDG-Technologie-Datei
(NAFv4-ADMBw-MDG-*.xml) KI-lesbare Regeldateien (Markdown) für die
ADMBw-Toolfamilie (Script-Maker, Extractor, Batch, KI-Suite).

Offline: reine Python-Stdlib (xml.etree), keine Netzwerkaufrufe zur Laufzeit.

Aufruf:
    python3 mdg_parser.py <pfad-zur-mdg.xml> [-o ausgabeordner] [--no-timestamp]

Erzeugt im Ausgabeordner:
    admbw-knowledge-stereotypes.md   Stereotyp-Katalog (nur UMLProfiles; Name, Metatype, Vererbung, AppliesTo)
    admbw-knowledge-topology.md      Topologie-Regeln (Metaconstraints: Quelle / Ziel, inkl. source/target/end-Rollen)
    admbw-knowledge-viewpoints.md    52 Viewpoints (DiagramProfile, ohne Diagramm-Artefakt „Business Process“)
    admbw-knowledge-tagtypes.md      Property-Typen (Tagged-Value-Definitionen mit Typeregeln)
    admbw-knowledge-stereotype-tags.md Konkrete Tags je Stereotyp (Typ, Werte, Default)
    admbw-meta.md                    Quelle, Extraktionszeitpunkt, Statistiken

Reproduzierbarkeit: Mit --no-timestamp (oder gesetzter SOURCE_DATE_EPOCH) sind
zwei Läufe byte-identisch. Nur Dateien mit Root-Element <MDG.Technology> werden
akzeptiert; alle Fehler (Datei fehlt, kein XML, fremdes XML, IO) beenden das
Programm mit Exit 2 und einer kurzen deutschen Meldung — ohne Ausgabedateien.
"""
import argparse
import json
import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone


def tag(e):
    return e.tag.split('}')[-1]


def find_all(root, t):
    return [e for e in root.iter() if tag(e) == t]


def clean(s):
    """Notes für Markdown säubern (Zeilenumbrüche, Länge)."""
    if not s:
        return ""
    return " ".join(str(s).split())


def extract_stereotype_tags(root):
    """Tagged Values je Stereotyp (``TaggedValues/Tag``).

    Die globale ``TaggedValueTypes``-Sektion beschreibt nur die Datentypen;
    die konkreten Tags (z. B. ``ITSD_ServiceTyp`` oder ``ITSD_Group``) hängen
    direkt am jeweiligen Stereotyp. Diese Werte sind für die Modellvalidierung
    und für Tool-Prompts relevant.
    """
    rows = []
    for st in model_stereotypes(root):
        name = (st.get('name') or '').strip()
        if not name:
            continue
        for tv in [c for c in st if tag(c) == 'TaggedValues']:
            for t in [c for c in tv if tag(c) == 'Tag']:
                tag_name = (t.get('name') or '').strip()
                if not tag_name:
                    continue
                rows.append({
                    'stereotype': name,
                    'tag': tag_name,
                    'type': (t.get('type') or '').strip(),
                    'values': (t.get('values') or '').strip(),
                    'default': (t.get('default') or '').strip(),
                    'description': clean(t.get('description') or ''),
                })
    return rows


def md_escape(s):
    return s.replace('|', '\\|').replace('\n', ' ')


def model_stereotypes(root):
    """Stereotype-Elemente aus UMLProfiles (Modell-Katalog).

    UIToolboxes (UI-Toolbox-Seiten) und DiagramProfile (Viewpoints) werden
    nicht berücksichtigt. Fallback für abweichende MDG-Strukturen: alles
    außerhalb von DiagramProfile/UIToolboxes.
    """
    containers = [u for u in root.iter() if tag(u) == 'UMLProfiles']
    stereos = []
    if containers:
        for up in containers:
            for prof in [c for c in up.iter() if tag(c) == 'UMLProfile']:
                for content in [c for c in prof if tag(c) == 'Content']:
                    stereos.extend([c for c in content.iter() if tag(c) == 'Stereotype'])
    else:
        excluded = set()
        for section in ('DiagramProfile', 'UIToolboxes'):
            for sec in [s for s in root.iter() if tag(s) == section]:
                excluded.update(id(c) for c in sec.iter() if tag(c) == 'Stereotype')
        stereos = [c for c in root.iter() if tag(c) == 'Stereotype' and id(c) not in excluded]
    return stereos


def extract_stereotypes(root):
    """Stereotyp-Katalog: nur Modell-Stereotype aus UMLProfiles.

    Die MDG enthält drei getrennte Bereiche:
      * UMLProfiles    — Modell-Stereotype (der eigentliche Katalog)
      * DiagramProfile — 52 Viewpoints + 1 Diagramm-Artefakt (separat)
      * UIToolboxes    — UI-Toolbox-Seiten (keine Modell-Stereotype)
    Namen werden getrimmt; ``baseStereotypes`` (Mehrfach-Eltern) wird
    zusätzlich zu ``generalizes`` ausgewertet.
    """
    rows, seen = [], set()
    for st in model_stereotypes(root):
        name = (st.get('name') or '').strip()
        if not name or name in seen:
            continue  # Mehrfachdeklaration — erste Definition zählt
        seen.add(name)
        meta = (st.get('metatype') or '').strip()
        notes = clean(st.get('notes'))
        gen = (st.get('generalizes') or '').strip()
        base = (st.get('baseStereotypes') or '').strip()
        parents = []
        for p in [gen] + base.replace(',', ' ').split():
            if p and p not in parents:
                parents.append(p)
        applies = []
        for at in [c for c in st if tag(c) == 'AppliesTo']:
            for ap in [c for c in at if tag(c) == 'Apply']:
                applies.append((ap.get('type') or '').strip())
        extra = [c.get('constraint') for c in st if tag(c) == 'StereoConstraint']
        rows.append({
            'name': name, 'metatype': meta, 'notes': notes,
            'generalizes': ' '.join(parents), 'applies': sorted(set(a for a in applies if a)),
            'extra': sorted(set(e for e in extra if e)),
            'abstract': (st.get('isAbstract') or '').lower() == 'true',
        })
    return rows


def extract_topology(root):
    """Metaconstraints je Modell-Stereotype: Quelle/Ziel über alle UML-Endrollen.

    Die MDG verwendet je nach Metaklasse unterschiedliche Endrollen:
      client/supplier, source/target, end[0].role/end[1].role,
      informationSource/informationTarget.
    Diese werden auf Quelle/Ziel normalisiert; nur Regeln mit beiden Enden sind
    für eine automatische Kantenprüfung entscheidbar. ``complete`` kennzeichnet
    genau diese Regeln.
    """
    source_roles = {'client', 'source', 'end[0].role', 'informationSource'}
    target_roles = {'supplier', 'target', 'end[1].role', 'informationTarget'}
    endpoint_roles = source_roles | target_roles
    rules, seen = [], set()
    for st in model_stereotypes(root):
        name = (st.get('name') or '').strip()
        if not name or name in seen:
            continue
        seen.add(name)
        clients, suppliers, others = [], [], []
        for mcb in [c for c in st if tag(c) == 'metaconstraints']:
            for mc in [c for c in mcb if tag(c) == 'metaconstraint']:
                role = mc.get('umlRole') or ''
                raw = mc.get('constraint') or ''
                # Mehrere erlaubte Ziele stehen semikolon-getrennt; Pfad kürzen.
                targets = []
                for part in raw.split(';'):
                    short = part.split('::')[-1].strip()
                    if short:
                        targets.append(short)
                if role in source_roles:
                    clients.extend(targets)
                elif role in target_roles:
                    suppliers.extend(targets)
                elif role not in endpoint_roles:
                    for short in targets:
                        others.append(f"{role} → {short}")
        if clients or suppliers or others:
            rules.append({
                'name': name,
                'clients': sorted(set(clients)),
                'suppliers': sorted(set(suppliers)),
                'others': sorted(set(others)),
                'complete': bool(clients and suppliers),
            })
    return rules


def extract_viewpoints(root):
    """Die 52 Viewpoints aus der DiagramProfile-Sektion.

    Das Diagramm-Artefakt „Business Process“ (Diagramm-Typ-Definition) wird
    gefiltert. Fachliche Properties gibt es in dieser MDG nicht — die
    Property-Elemente der XML gehören zur Diagramm-Konfiguration (Apply) und
    werden hier bewusst nicht als Viewpoint-Properties ausgegeben.
    """
    vps = []
    for dp in find_all(root, 'DiagramProfile'):
        for st in [s for s in dp.iter() if tag(s) == 'Stereotype']:
            name = (st.get('name') or '').strip()
            if not name or name == 'Business Process':
                continue  # Diagramm-Typ-Artefakt, kein Viewpoint
            vps.append({
                'name': name,
                'notes': clean(st.get('notes')),
                'props': [(p.get('name'), p.get('notes') or '') for p in st if tag(p) == 'Property'],
            })
    return vps


def extract_enums(root):
    """Property-Typen aus TaggedValueTypes/DataSet/DataRow-Struktur.

    Jede DataRow wird einzeln geparst (Spalten Property / Description / Notes,
    in beliebiger Reihenfolge und optional) — keine flache i+=3-Indexlogik.
    """
    enums = []
    for block in find_all(root, 'TaggedValueTypes'):
        for ds in [c for c in block.iter() if tag(c) == 'DataSet']:
            ds_name = ds.get('name') or ''
            for row in [c for c in ds if tag(c) == 'DataRow']:
                cols = {c.get('name'): (c.get('value') or '') for c in row if tag(c) == 'Column'}
                prop = cols.get('Property', '').strip()
                if not prop:
                    continue
                enums.append({
                    'name': prop,
                    'notes': clean(cols.get('Notes', '')),
                    'dataset': ds_name,
                    'desc': clean(cols.get('Description', '')),
                })
    return enums


def stereotype_maps(st):
    """Eltern- und Kindbeziehungen aus dem Katalog (Mehrfachvererbung inklusive).

    Die MDG nennt je Stereotyp ``generalizes`` (Hauptelternteil) und
    ``baseStereotypes`` (weitere Rollen). Für die Auflösung abstrakter Typen
    zählt beides — sonst fehlt z. B. ResourceArchitecture der Weg zu
    ResourcePerformer und jede CapabilityConfiguration gälte als Verstoß.
    """
    parents = {}
    for s in st:
        parents[s['name']] = [p for p in s['generalizes'].replace(',', ' ').split() if p]
    children = {}
    for child, ps in parents.items():
        for p in ps:
            children.setdefault(p, []).append(child)

    def all_children(name, seen=None):
        seen = set() if seen is None else seen
        for c in children.get(name, []):
            if c not in seen:
                seen.add(c)
                all_children(c, seen)
        return seen

    return parents, children, all_children


def build_md(st, topo, vps, enums, tags, src, version_hint, ts, ctx):
    out = {}
    parents, children, all_children = stereotype_maps(st)
    by_name = {s['name']: s for s in st}
    abstract_names = sorted(s['name'] for s in st if s['abstract'])

    if ts:
        header = f"> Quelle: `{os.path.basename(src)}` — automatisch erzeugt am {ts}"
    else:
        header = f"> Quelle: `{os.path.basename(src)}` — automatisch erzeugt (ohne Zeitstempel)"

    # 1) Stereotype
    lines = [
        "# ADMBw-Stereotype (MDG-extrahiert)",
        "",
        header,
        f"> {len(st)} Stereotype · {len(abstract_names)} abstrakt (🔒, nicht instanziierbar) · Version: {version_hint}",
        "",
        "| Stereotype | Metatype | Eltern | AppliesTo | Abstrakt | Beschreibung |",
        "|---|---|---|---|---|---|",
    ]
    for s in st:
        lines.append(
            f"| {md_escape(s['name'])} | {md_escape(s['metatype'])} | {md_escape(', '.join(parents.get(s['name'], [])))} | "
            f"{', '.join(s['applies'])} | {'🔒 ja' if s['abstract'] else '–'} | {md_escape(s['notes'][:160])} |"
        )
    out['admbw-knowledge-stereotypes.md'] = "\n".join(lines)

    # 1b) Generische Arbeitsanweisung für KI-Werkzeuge (hartcodiert, nicht aus der MDG)
    lines = [
        "",
        "## Hinweis für KI-Werkzeuge",
        "",
        "- Ein Stereotyp mit **🔒 ja** ist abstrakt. Es darf **nicht** als Element- oder Beziehungstyp verwendet werden.",
        "- Abstrakte Typen sind Platzhalter für ihre konkreten Subtypen. Beispiele: `{REQUIREMENT}` wird als "
        "`FunctionalRequirement` oder `NonfunctionalRequirement` modelliert; `ResourcePerformer` als "
        "`CapabilityConfiguration`, `PhysicalResource`, `OrganizationalResource` oder `Software`.",
        "- Für jede Regel mit abstraktem Endpunkt gilt: erlaubt sind alle konkreten Subtypen "
        "(Feld `concreteDescendants` in `admbw-stereotypes.json`).",
        "- Vor der Ausgabe eines Modells prüfen: kein Element und keine Beziehung trägt ein abstraktes Stereotyp "
        "(`python3 scripts/check_abstract_usage.py modell.qea`).",
    ]
    out['admbw-knowledge-stereotypes.md'] += "\n" + "\n".join(lines)

    # 2) Topologie
    n_complete = sum(1 for t in topo if t['complete'])
    lines = [
        "# ADMBw-Topologie-Regeln (MDG-Metaconstraints)",
        "",
        header,
        f"> {len(topo)} Stereotype mit Beziehungsregeln (Metaconstraints) · {n_complete} vollständig (Quelle und Ziel)",
        "",
        "## Lesart",
        "",
        "- **Quelle:** client, source, end[0].role oder informationSource — je nach UML-Metaklasse.",
        "- **Ziel:** supplier, target, end[1].role oder informationTarget — je nach UML-Metaklasse.",
        "- **Weitere Rollen:** zusätzliche Metamodell-Beschränkungen (Rollennamen direkt aus der MDG).",
        f"- **Vollständigkeit:** Nur Regeln mit Quelle **und** Ziel ({n_complete} von {len(topo)}) sind maschinell prüfbar; Regeln mit ausschließlich „Weiteren Rollen“ dienen als Referenz.",
        "- **Abstrakte Typen:** Endpunkte, die auf abstrakte Stereotype verweisen (🔒), gelten für alle konkreten Subtypen. Die Auflösung steht unten unter „Abstrakte Endpunkte“.",
        "",
        "| Stereotype | Erlaubte Quellen (client/source/end[0]) | Erlaubte Ziele (supplier/target/end[1]) | Weitere Rollen |",
        "|---|---|---|---|",
    ]
    for t in topo:
        lines.append(f"| {md_escape(t['name'])} | {', '.join(t['clients'])} | {', '.join(t['suppliers'])} | {', '.join(t['others'])} |")

    # Abstrakte Endpunkte + konkrete Alternativen (für Prüfprogramme)
    endpoints = {}
    for t in topo:
        for side in ('clients', 'suppliers'):
            for n in t[side]:
                if n in by_name and by_name[n]['abstract']:
                    concrete = sorted(c for c in all_children(n)
                                      if c in by_name and not by_name[c]['abstract'])
                    endpoints[n] = concrete
    lines += [
        "",
        "## Abstrakte Endpunkte",
        "",
        "Diese Typen dürfen **nicht instanziiert** werden. Für die Prüfung eines konkreten Modells "
        "sind sie auf die aufgeführten konkreten Subtypen aufzulösen.",
        "",
        "| Abstrakter Typ | Konkrete Subtypen |",
        "|---|---|",
    ]
    for n, concrete in sorted(endpoints.items()):
        lines.append(f"| 🔒 {n} | {', '.join(concrete) if concrete else '–'} |")
    out['admbw-knowledge-topology.md'] = "\n".join(lines)


    # 3) Viewpoints
    lines = [
        "# ADMBw-Viewpoints (MDG-DiagramProfile)",
        "",
        header,
        f"> {len(vps)} Viewpoints",
        "",
    ]
    for v in vps:
        lines.append(f"## {v['name']}")
        if v['notes']:
            lines.append(f"{v['notes'][:300]}")
        if v['props']:
            lines.append("")
            lines.append("| Property | Bedeutung |")
            lines.append("|---|---|")
            for pn, pn_notes in v['props']:
                lines.append(f"| {md_escape(pn)} | {md_escape((pn_notes or '')[:120])} |")
        lines.append("")
    out['admbw-knowledge-viewpoints.md'] = "\n".join(lines)

    # 4) Property-Typen (Tagged-Value-Definitionen)
    lines = [
        "# ADMBw-Tagged-Value-Definitionen (MDG-Property-Typen)",
        "",
        header,
        f"> {len(enums)} Property-Typen",
        "",
        "| Property | Datensatz | Beschreibung | Einschränkungen (aus MDG) |",
        "|---|---|---|---|",
    ]
    for e in enums:
        lines.append(f"| {md_escape(e['name'])} | {md_escape(e['dataset'])} | {md_escape(e['desc'][:100])} | {md_escape(e['notes'][:160])} |")
    out['admbw-knowledge-tagtypes.md'] = "\n".join(lines)

    # 5) Konkrete Tagged Values je Stereotyp
    lines = [
        "# ADMBw-Stereotyp-Tags (MDG-TaggedValues)",
        "",
        header,
        f"> {len(tags)} Tags an {len(set(t['stereotype'] for t in tags))} Stereotypen",
        "",
        "| Stereotype | Tag | Typ | Erlaubte Werte | Default | Beschreibung |",
        "|---|---|---|---|---|---|",
    ]
    for t in tags:
        lines.append(
            f"| {md_escape(t['stereotype'])} | {md_escape(t['tag'])} | {md_escape(t['type'])} | "
            f"{md_escape(t['values'])} | {md_escape(t['default'])} | {md_escape(t['description'][:120])} |"
        )
    out['admbw-knowledge-stereotype-tags.md'] = "\n".join(lines)

    # 6) Meta
    usable = sum(1 for s in st if s['applies'])
    with_meta = sum(1 for s in st if s['metatype'])
    no_meta = sorted(s['name'] for s in st if not s['metatype'])
    abstract_bases = sum(1 for s in st if s['abstract'] and not s['applies'])
    abstract_usable = sum(1 for s in st if s['abstract'] and s['applies'])
    lines = [
        "# ADMBw-MDG-Extraktion — Metadaten",
        "",
        f"- **MDG-Datei:** `{src}`",
        f"- **MDG-Version (aus Dateiname):** {version_hint}",
        f"- **Extrahiert am:** {ts if ts else '– (ohne Zeitstempel)'}",
        f"- **Stereotype im Katalog:** {len(st)} (nur UMLProfiles)",
        f"- **Davon im Modell nutzbar (mit AppliesTo):** {usable}",
        f"- **Davon mit Metatype:** {with_meta}" + (f" ({len(no_meta)} ohne: {', '.join(no_meta)})" if no_meta else ""),
        f"- **Abstrakte Stereotype (🔒, nicht instanziierbar):** {len(abstract_names)}",
        f"  - davon ohne AppliesTo (reine Platzhalter): {abstract_bases}",
        f"  - davon mit AppliesTo (fachlich zu spezialisieren): {abstract_usable}",
        f"- **Stereotype mit Topologie-Regeln:** {len(topo)} (davon {n_complete} vollständig mit Quelle und Ziel)",
        f"- **Viewpoints:** {len(vps)} (DiagramProfile ohne Diagramm-Artefakt „Business Process“)",
        f"- **Property-Typen:** {len(enums)}",
        f"- **Stereotyp-Tags:** {len(tags)} an {len(set(t['stereotype'] for t in tags))} Stereotypen",
        "",
        "Die Markierung 🔒 steht in der Stereotyp-Tabelle und in `admbw-stereotypes.json` "
        "(`abstract: true`). Ein Modell darf kein Element mit einem abstrakten Stereotyp tragen.",
        "",
        "Zählweise: Die MDG enthält die Stereotype in drei getrennten Bereichen —",
        f"{len(st)} Deklarationen in UMLProfiles (das Modellprofil, der eigentliche Katalog),",
        f"{ctx['toolbox_elems']} Elemente in UIToolboxes ({ctx['toolbox_pages']} UI-Toolbox-Seiten, keine Modell-Stereotype) und",
        f"{ctx['diagram_entries']} Einträge in DiagramProfile ({len(vps)} Viewpoints + 1 Diagramm-Artefakt „Business Process“).",
        "Der Katalog zählt ausschließlich die UMLProfiles-Stereotype; Toolbox-Seiten",
        "und Viewpoints werden nicht (bzw. separat) extrahiert.",
        "",
        "Diese Dateien wurden automatisch aus der offiziellen ADMBw-MDG-Technologie erzeugt",
        "(https://www.bundeswehr.de/de/organisation/ausruestung-baainbw/vergabe/methode-architektur).",
        "Bei einem MDG-Update einfach den Parser erneut ausführen.",
    ]
    out['admbw-meta.md'] = "\n".join(lines)

    # 7) Maschinenlesbarer Katalog (Abstrakt-Flag + Auflösung für Prüfprogramme)
    catalogue = []
    for s in st:
        concrete = sorted(c for c in all_children(s['name'])
                          if c in by_name and not by_name[c]['abstract'])
        catalogue.append({
            'name': s['name'],
            'metatype': s['metatype'],
            'abstract': s['abstract'],
            'parents': parents.get(s['name'], []),
            'appliesTo': s['applies'],
            'concreteDescendants': concrete,
        })
    out['admbw-stereotypes.json'] = json.dumps({
        'release': version_hint,
        'source': os.path.basename(src),
        'counts': {
            'stereotypes': len(st),
            'abstract': len(abstract_names),
            'abstractWithoutAppliesTo': abstract_bases,
            'abstractWithAppliesTo': abstract_usable,
        },
        'stereotypes': catalogue,
    }, ensure_ascii=False, indent=1)

    # 8) Schreibvarianten (britisch/amerikanisch, Alt-MDG) → kanonischer Name
    out['admbw-aliases.json'] = json.dumps({
        'note': 'Alt-Schreibweisen aus Modellen oder älteren MDG-Ständen. '
                'Prüfprogramme sollen vor dem Namensvergleich umschreiben.',
        'aliases': {
            'PropertySetGeneralisation': 'PropertySetGeneralization',
            'ServiceSpecificationGeneralization': 'ServiceGeneralization',
        },
    }, ensure_ascii=False, indent=1)

    return out


def main():
    ap = argparse.ArgumentParser(description="ADMBw-MDG -> KI-lesbare Regeldateien (offline)")
    ap.add_argument('mdg', help="Pfad zur MDG-XML (z. B. NAFv4-ADMBw-MDG-2026.05.xml)")
    ap.add_argument('-o', '--out', default='./output', help="Ausgabeordner (Default: ./output)")
    ap.add_argument('--no-timestamp', action='store_true',
                    help="Keine Zeitstempel in die Ausgabedateien schreiben (reproduzierbare Läufe)")
    args = ap.parse_args()

    if not os.path.isfile(args.mdg):
        print(f"FEHLER: Datei nicht gefunden: {args.mdg}", file=sys.stderr)
        sys.exit(2)

    try:
        tree = ET.parse(args.mdg)
    except ET.ParseError as e:
        print(f"FEHLER: {args.mdg} ist kein gültiges XML ({e}).", file=sys.stderr)
        sys.exit(2)
    except OSError as e:
        print(f"FEHLER: {args.mdg} konnte nicht gelesen werden ({e}).", file=sys.stderr)
        sys.exit(2)
    root = tree.getroot()
    if tag(root) != 'MDG.Technology':
        print(f"FEHLER: Keine MDG-Technologie-Datei — Root-Element ist <{tag(root)}>, "
              f"erwartet <MDG.Technology>.", file=sys.stderr)
        sys.exit(2)

    print(f"Lese {args.mdg} …")
    st = extract_stereotypes(root)
    if not st:
        print("FEHLER: Die Datei enthält keine Modell-Stereotype (UMLProfiles/Content/"
              "Stereotypes). Das ist keine ADMBw-MDG — oder eine unvollständige Datei.",
              file=sys.stderr)
        sys.exit(2)
    topo = extract_topology(root)
    vps = extract_viewpoints(root)
    enums = extract_enums(root)
    tags = extract_stereotype_tags(root)
    version_hint = os.path.basename(args.mdg)
    ctx = {
        'toolbox_elems': sum(1 for sec in find_all(root, 'UIToolboxes') for c in sec.iter() if tag(c) == 'Stereotype'),
        'toolbox_pages': len({(s.get('name') or '').strip() for sec in find_all(root, 'UIToolboxes') for s in sec.iter() if tag(s) == 'Stereotype'}),
        'diagram_entries': sum(1 for sec in find_all(root, 'DiagramProfile') for s in sec.iter() if tag(s) == 'Stereotype'),
    }

    print(f"  Stereotype (UMLProfiles): {len(st)} "
          f"({sum(1 for s in st if s['abstract'])} abstrakt 🔒)")
    print(f"  Topologie-Regeln (Stereotype mit Metaconstraints): {len(topo)} "
          f"(davon {sum(1 for t in topo if t['complete'])} vollständig)")
    print(f"  Viewpoints: {len(vps)}")
    print(f"  Property-Typen (TaggedValueTypes): {len(enums)}")
    print(f"  Stereotyp-Tags (TaggedValues): {len(tags)}")

    # Zeitstempel: --no-timestamp deaktiviert, SOURCE_DATE_EPOCH macht deterministisch
    ts = None
    if not args.no_timestamp:
        epoch = os.environ.get('SOURCE_DATE_EPOCH')
        if epoch:
            try:
                ts = datetime.fromtimestamp(int(epoch), timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
            except (ValueError, OSError, OverflowError):
                pass
        if ts is None:
            ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

    docs = build_md(st, topo, vps, enums, tags, args.mdg, version_hint, ts, ctx)

    try:
        os.makedirs(args.out, exist_ok=True)
    except OSError as e:
        print(f"FEHLER: Ausgabeordner konnte nicht angelegt werden: {args.out} ({e}).", file=sys.stderr)
        sys.exit(2)
    try:
        for fname, content in docs.items():
            path = os.path.join(args.out, fname)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  → {fname} ({len(content)} Zeichen)")
    except OSError as e:
        print(f"FEHLER: Schreiben fehlgeschlagen ({e}).", file=sys.stderr)
        sys.exit(2)

    print(f"\nFertig: {len(docs)} Dateien in {os.path.abspath(args.out)}")


if __name__ == '__main__':
    main()
