#!/usr/bin/env python3
"""
EAM-ADMBw-MDG-Parser — extrahiert aus einer Sparx-MDG-Technologie-Datei
(NAFv4-ADMBw-MDG-*.xml) KI-lesbare Regeldateien (Markdown) für die
ADMBw-Toolfamilie (Script-Maker, Extractor, Batch, KI-Suite).

Offline: reine Python-Stdlib (xml.etree), keine Netzwerkaufrufe zur Laufzeit.

Aufruf:
    python3 mdg_parser.py <pfad-zur-mdg.xml> [-o ausgabeordner]

Erzeugt im Ausgabeordner:
    admbw-knowledge-stereotypes.md   Stereotyp-Katalog (Name, Metatype, Beschreibung, Vererbung, AppliesTo)
    admbw-knowledge-topology.md      Topologie-Regeln (Metaconstraints: client/supplier-Erlaubnisse)
    admbw-knowledge-viewpoints.md    53 Viewpoints mit Properties + View-Definitionen
    admbw-knowledge-enums.md         TaggedValueTypes (Aufzählungen)
    admbw-meta.md                    Version, Quelle, Extraktionszeitpunkt, Statistiken
"""
import argparse
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
    s = " ".join(str(s).split())
    return s


def extract_stereotypes(root):
    """642 Stereotype: Name | Metatype | Beschreibung | Vererbung | AppliesTo."""
    rows = []
    for st in find_all(root, 'Stereotype'):
        name = st.get('name') or '(ohne Name)'
        meta = st.get('metatype') or ''
        notes = clean(st.get('notes'))
        gen = st.get('generalizes') or ''
        base = st.get('baseStereotypes') or ''
        applies = []
        for at in [c for c in st if tag(c) == 'AppliesTo']:
            for ap in [c for c in at if tag(c) == 'Apply']:
                applies.append(ap.get('type') or '')
        # StereoConstraint-Kinder (zusätzliche Regeln)
        extra = [c.get('constraint') for c in st if tag(c) == 'StereoConstraint']
        rows.append({
            'name': name, 'metatype': meta, 'notes': notes,
            'generalizes': gen, 'applies': sorted(set(a for a in applies if a)),
            'extra': sorted(set(e for e in extra if e)),
        })
    return rows


def extract_topology(root):
    """Metaconstraints je Stereotype: client/supplier-Kernregeln + weitere Rollen."""
    rules = []
    for st in find_all(root, 'Stereotype'):
        name = st.get('name') or '(ohne Name)'
        clients, suppliers, others = [], [], []
        for mcb in [c for c in st if tag(c) == 'metaconstraints']:
            for mc in [c for c in mcb if tag(c) == 'metaconstraint']:
                role = mc.get('umlRole')
                target = mc.get('constraint') or ''
                # Pfad kürzen: 'NAFv4-ADMBw::ActualState' -> 'ActualState'
                short = target.split('::')[-1] if '::' in target else target
                if role == 'client':
                    clients.append(short)
                elif role == 'supplier':
                    suppliers.append(short)
                elif short:
                    others.append(f"{role} → {short}")
        if clients or suppliers or others:
            rules.append({
                'name': name,
                'clients': sorted(set(clients)),
                'suppliers': sorted(set(suppliers)),
                'others': sorted(set(others)),
            })
    return rules


def extract_viewpoints(root):
    """Die 53 Stereotype aus der DiagramProfile-Sektion."""
    vps = []
    for dp in find_all(root, 'DiagramProfile'):
        for st in [s for s in dp.iter() if tag(s) == 'Stereotype']:
            vps.append({
                'name': st.get('name') or '(ohne Name)',
                'notes': clean(st.get('notes')),
                'props': [(p.get('name'), p.get('notes') or '') for p in st if tag(p) == 'Property'],
            })
    return vps


def extract_enums(root):
    """Property-Typen aus RefData/DataSet-Struktur (Tagged-Value-Definitionen).

    MDG-Aufbau: TaggedValueTypes > RefData > DataSet > Column-Tripel
    (Property / Description / Notes mit Typ-Regeln wie 'Type=RefGUID; Values=Class; Stereotypes=…').
    """
    enums = []
    for block in find_all(root, 'TaggedValueTypes'):
        for ds in [c for c in block.iter() if tag(c) == 'DataSet']:
            ds_name = ds.get('name') or ''
            cols = [c for c in ds.iter() if tag(c) == 'Column']
            i = 0
            while i < len(cols):
                if cols[i].get('name') == 'Property' and cols[i].get('value'):
                    prop = cols[i].get('value')
                    desc, notes = '', ''
                    if i + 1 < len(cols) and cols[i + 1].get('name') == 'Description':
                        desc = cols[i + 1].get('value') or ''
                    if i + 2 < len(cols) and cols[i + 2].get('name') == 'Notes':
                        notes = cols[i + 2].get('value') or ''
                    enums.append({'name': prop, 'notes': clean(notes), 'dataset': ds_name, 'desc': clean(desc)})
                    i += 3
                else:
                    i += 1
    return enums


def md_escape(s):
    return s.replace('|', '\\|').replace('\n', ' ')


def build_md(st, topo, vps, enums, src, version_hint):
    out = {}

    # 1) Stereotype
    lines = [
        "# ADMBw-Stereotype (MDG-extrahiert)",
        "",
        f"> Quelle: `{src}` — automatisch erzeugt am {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"> {len(st)} Stereotype · Version: {version_hint}",
        "",
        "| Stereotype | Metatype | Vererbung | AppliesTo | Beschreibung |",
        "|---|---|---|---|---|",
    ]
    for s in st:
        lines.append(f"| {md_escape(s['name'])} | {md_escape(s['metatype'])} | {md_escape(s['generalizes'])} | {', '.join(s['applies'])} | {md_escape(s['notes'][:160])} |")
    out['admbw-knowledge-stereotypes.md'] = "\n".join(lines)

    # 2) Topologie
    lines = [
        "# ADMBw-Topologie-Regeln (MDG-Metaconstraints)",
        "",
        f"> Quelle: `{src}` — automatisch erzeugt am {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"> {len(topo)} Stereotype mit Beziehungsregeln (Metaconstraints)",
        "",
        "## Lesart",
        "",
        "- **Erlaubte Ziele (client):** Der Stereotype darf nur als Quelle einer Beziehung zu den gelisteten Ziel-Stereotypen stehen.",
        "- **Erlaubte Quellen (supplier):** Nur die gelisteten Stereotype dürfen als Ziel auf diesen Stereotype zeigen.",
        "- **Weitere Rollen:** zusätzliche Metamodell-Beschränkungen (Rollennamen direkt aus der MDG).",
        "",
        "| Stereotype | Erlaubte Ziele (client) | Erlaubte Quellen (supplier) | Weitere Rollen |",
        "|---|---|---|---|",
    ]
    for t in topo:
        lines.append(f"| {md_escape(t['name'])} | {', '.join(t['clients'])} | {', '.join(t['suppliers'])} | {', '.join(t['others'])} |")
    out['admbw-knowledge-topology.md'] = "\n".join(lines)

    # 3) Viewpoints
    lines = [
        "# ADMBw-Viewpoints (MDG-DiagramProfile)",
        "",
        f"> Quelle: `{src}` — automatisch erzeugt am {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
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
        f"> Quelle: `{src}` — automatisch erzeugt am {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"> {len(enums)} Property-Typen",
        "",
        "| Property | Datensatz | Beschreibung | Einschränkungen (aus MDG) |",
        "|---|---|---|---|",
    ]
    for e in enums:
        lines.append(f"| {md_escape(e['name'])} | {md_escape(e['dataset'])} | {md_escape(e['desc'][:100])} | {md_escape(e['notes'][:160])} |")
    out['admbw-knowledge-tagtypes.md'] = "\n".join(lines)

    # 5) Meta
    lines = [
        "# ADMBw-MDG-Extraktion — Metadaten",
        "",
        f"- **MDG-Datei:** `{src}`",
        f"- **Extrahiert am:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"- **Stereotype:** {len(st)}",
        f"- **Stereotype mit Topologie-Regeln:** {len(topo)}",
        f"- **Viewpoints:** {len(vps)}",
        f"- **TaggedValueTypes:** {len(enums)}",
        "",
        "Diese Dateien wurden automatisch aus der offiziellen ADMBw-MDG-Technologie erzeugt",
        "(https://www.bundeswehr.de/de/organisation/ausruestung-baainbw/vergabe/methode-architektur).",
        "Bei einem MDG-Update einfach den Parser erneut ausführen.",
    ]
    out['admbw-meta.md'] = "\n".join(lines)

    return out


def main():
    ap = argparse.ArgumentParser(description="ADMBw-MDG -> KI-lesbare Regeldateien (offline)")
    ap.add_argument('mdg', help="Pfad zur MDG-XML (z. B. NAFv4-ADMBw-MDG-2026.05.xml)")
    ap.add_argument('-o', '--out', default='./output', help="Ausgabeordner (Default: ./output)")
    args = ap.parse_args()

    if not os.path.isfile(args.mdg):
        print(f"FEHLER: Datei nicht gefunden: {args.mdg}", file=sys.stderr)
        sys.exit(1)

    print(f"Lese {args.mdg} …")
    tree = ET.parse(args.mdg)
    root = tree.getroot()

    st = extract_stereotypes(root)
    topo = extract_topology(root)
    vps = extract_viewpoints(root)
    enums = extract_enums(root)
    version_hint = os.path.basename(args.mdg)

    print(f"  Stereotype: {len(st)}")
    print(f"  Topologie-Regeln (Stereotype mit Metaconstraints): {len(topo)}")
    print(f"  Viewpoints: {len(vps)}")
    print(f"  TaggedValueTypes: {len(enums)}")

    docs = build_md(st, topo, vps, enums, args.mdg, version_hint)
    os.makedirs(args.out, exist_ok=True)
    for fname, content in docs.items():
        path = os.path.join(args.out, fname)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  → {fname} ({len(content)} Zeichen)")

    print(f"\nFertig: {len(docs)} Dateien in {os.path.abspath(args.out)}")


if __name__ == '__main__':
    main()
