# EAM-ADMBw-MDG-Parser

**Extrahiert aus der offiziellen ADMBw-MDG-Technologie (Sparx EA / NAFv4) KI-lesbare Regeldateien** — die Wissensbasis für die ADMBw-Toolfamilie (Script-Maker, Extractor, Batch, KI-Suite).

100 % offline: reine Python-Stdlib, keine Netzwerkaufrufe zur Laufzeit.

---

## Warum?

Die ADMBw-Regeln (Stereotype, Topologie, Viewpoints) waren bisher handgepflegt. Bei jedem MDG-Update der Bundeswehr drohten sie still zu veralten. Dieser Parser macht die Pflege zum Einzeiler:

```bash
python3 mdg_parser.py NAFv4-ADMBw-MDG-2026.05.xml -o output
```

## Was er extrahiert

| Ausgabe | Inhalt | Umfang (Stand 2026.05) |
|---|---|---|
| `admbw-knowledge-stereotypes.md` | Stereotyp-Katalog: Name, Metatype, **Eltern** (`generalizes` + `baseStereotypes`), AppliesTo, **Abstrakt (🔒)**, Beschreibung | **318 Modell-Stereotype** (293 mit AppliesTo nutzbar · **44 abstrakt** — davon 25 ohne AppliesTo und 19 mit · 5 ohne Metatype) |
| `admbw-stereotypes.json` | Derselbe Katalog maschinenlesbar: `abstract`, `parents`, `appliesTo`, `concreteDescendants` | 318 Einträge |
| `admbw-aliases.json` | Alt-Schreibweisen (britisch/amerikanisch) → kanonischer Name | `PropertySetGeneralisation` → `PropertySetGeneralization`, `ServiceSpecificationGeneralization` → `ServiceGeneralization` |
| `admbw-knowledge-topology.md` | Beziehungsregeln aus Metaconstraints: Quelle (client/source/end[0]), Ziel (supplier/target/end[1]), weitere Rollen | **203 Stereotype mit Regeln** (133 vollständig mit Quelle **und** Ziel — nur diese sind maschinell prüfbar) |
| `admbw-knowledge-viewpoints.md` | Die NAFv4-Viewpoints (DiagramProfile, ohne das Diagramm-Artefakt „Business Process“) | **52 Viewpoints** |
| `admbw-knowledge-tagtypes.md` | Tagged-Value-Definitionen mit Typeregeln (`Type=RefGUID; Values=Class; Stereotypes=…`), je `DataRow` einzeln geparst | **27 Property-Typen** |
| `admbw-knowledge-stereotype-tags.md` | Konkrete Tagged Values je Stereotyp (Typ, erlaubte Werte, Default, Beschreibung) | **225 Tags an 66 Stereotypen** |
| `admbw-meta.md` | Quelle, Version, Extraktionszeitpunkt, Statistiken, Zählweise | – |

> **Zählweise:** Die MDG enthält die Stereotype in drei getrennten Bereichen:
> `UMLProfiles` (318 Deklarationen — das Modellprofil, der eigentliche Katalog),
> `UIToolboxes` (271 Elemente / 125 UI-Toolbox-Seiten — reine Bedienoberfläche, keine Modell-Stereotype) und
> `DiagramProfile` (53 Einträge = 52 Viewpoints + 1 Diagramm-Artefakt „Business Process“).
> Der Katalog zählt ausschließlich die `UMLProfiles`-Stereotype; Toolbox-Seiten werden nicht extrahiert.
> Viewpoint-Properties gibt es in dieser MDG nicht — die `Property`-Elemente der XML sind
> Diagramm-Konfiguration (`Apply`) und werden nicht als fachliche Properties ausgegeben.

## Prompt-Datei (für Chatbots)

`admbw-prompt.md` ist die **Arbeitsanweisung** — Auftrag, eiserne Regeln, Lesart der
Regeldateien, Ausgabeformat und ein Verzeichnis der acht anderen Dateien. Sie enthält
bewusst **keine Kopie** des Katalogs: Die Regeldateien bleiben die einzige Datenquelle.

```bash
python3 mdg_parser.py NAFv4-ADMBw-MDG-2026.05.xml -o output
# ohne Prompt-Datei:
python3 mdg_parser.py NAFv4-ADMBw-MDG-2026.05.xml -o output --no-prompt
```

| Datei | Rolle | Umfang |
|---|---|---|
| `admbw-knowledge-*.md` | Regeln (Stereotype, Topologie, Viewpoints, Tags) | 6 Dateien, 124 KB |
| `admbw-prompt.md` | Arbeitsanweisung + Dateiverzeichnis | ~4 KB |
| `admbw-*.json` | maschinenlesbar für Prüfprogramme | 86 KB |

Die Auflösung abstrakter Typen steht zusätzlich als Abschnitt in
`admbw-knowledge-stereotypes.md` — der Chatbot braucht dafür keine JSON.

## Abstrakte Stereotype

Die MDG markiert 44 der 318 Stereotype als abstrakt (`isAbstract="true"`). Sie sind
Platzhalter und dürfen nicht instanziiert werden:

- **25 ohne AppliesTo** — reine Metamodell-Knoten (`UAFElement`, `CapableElement`,
  `ExchangeItem`, `ProcessEdge` …). Sie können in EA gar nicht angewendet werden.
- **19 mit AppliesTo** — technisch anwendbar, fachlich aber zu spezialisieren
  (`ResourcePerformer`, `PhysicalResource`, `OrganizationalResource`, `Achiever`,
  `BWRequirement`, `Rule` …).

Die Grundlagen Methode Architektur (BMVg) verlangt genau das: abstrakte Elemente stehen
in geschweiften Klammern, `{REQUIREMENT}` wird als `FunctionalRequirement` oder
`NonfunctionalRequirement` modelliert.

Der Parser kennzeichnet sie in der Tabelle mit **🔒 ja**, im JSON mit `abstract: true`
und liefert in `concreteDescendants` die konkreten Subtypen. Regeln mit abstraktem
Endpunkt gelten für alle diese Subtypen; der Abschnitt „Abstrakte Endpunkte“ in
`admbw-knowledge-topology.md` listet die Auflösung.

Prüfung eines Modells (Exit 1 bei Treffern):

```bash
python3 scripts/check_abstract_usage.py modell.qea
```

## Reproduzierbarkeit & Fehlerverhalten

- `--no-timestamp` unterdrückt Zeitstempel in allen fünf Dateien → zwei Läufe sind **byte-identisch**.
- Alternativ `SOURCE_DATE_EPOCH=<unix-zeit>` setzen → deterministischer Zeitstempel.
- Nur Dateien mit Root-Element `<MDG.Technology>` werden akzeptiert. Alle Fehler
  (Datei fehlt, kein/defektes XML, fremdes XML, IO-Fehler) beenden das Programm mit
  **Exit 2**, einer kurzen deutschen Meldung auf stderr und **ohne** Ausgabedateien.

## Tests & Reproduzierbarkeit

Der offizielle MDG-Stand 2026.05 liegt als Test-Fixture unter
`tests/fixtures/NAFv4-ADMBw-MDG-2026.05.xml` (SHA-256 `c014ceda…701c84`).
Die GitHub Action `MDG Guard` prüft damit:

- Byte-Identität zweier `--no-timestamp`-Läufe
- Übereinstimmung mit der Baseline `schemas/baseline-mdg-2026.05.json`
  (318 Stereotype / 203 Topologie / 133 vollständige Regeln / 52 Viewpoints /
  27 Property-Typen / 225 Stereotyp-Tags) **plus Namens-Fingerprints**
- Namensgleichheit der Wissensbasis in Extractor, Batch und Script-Maker
- den Drift-/Regressions-Selbsttest `tests/test_drift.py`

### Baseline statt eingebrannter Zahlen

Die erwarteten Zahlen stehen **nicht mehr im Code**, sondern in einer
Baseline-Datei. Eine neue MDG-Version ist damit ein meldbarer Zustand und
kein Build-Fehler:

| Ergebnis | Exit | Bedeutung | Reaktion |
|---|---:|---|---|
| OK | 0 | Zähler und Namen identisch | nichts tun |
| DRIFT | 2 | MDG ist neuer als die Baseline | Parser prüfen, neue Baseline schreiben |
| REGRESSION | 1 | Zähler gesunken oder Downstream unsynchron | Fehler untersuchen |

Die CI behandelt Exit 2 als Warnung (`::warning::`), nicht als Abbruch.

Lokal:

```bash
python3 mdg_parser.py tests/fixtures/NAFv4-ADMBw-MDG-2026.05.xml -o /tmp/mdg-a --no-timestamp
python3 scripts/check_kb_sync.py /tmp/mdg-a ../EAM-AI-ADMBw-Extractor ../EAM-AI-ADMBw-Batch
```

### Wenn eine neue MDG erscheint

```bash
# 1. neue XML extrahieren
python3 mdg_parser.py NAFv4-ADMBw-MDG-2027.01.xml -o /tmp/mdg-2027.01 --no-timestamp

# 2. Ist-Stand gegen alte Baseline prüfen (erwartet Exit 2 = DRIFT)
python3 scripts/check_kb_sync.py /tmp/mdg-2027.01

# 3. nach fachlicher Prüfung: neue Baseline schreiben
python3 scripts/check_kb_sync.py /tmp/mdg-2027.01 --label 2027.01 \
    --write-baseline schemas/baseline-mdg-2027.01.json

# 4. Baseline im Workflow umstellen, Wissensbasis in die Downstream-Repos kopieren
```

Der Selbsttest simuliert genau diesen Fall (340 statt 318 Stereotype) und
beweist, dass der Check Drift meldet, ohne rot zu werden:

```bash
python3 tests/test_drift.py
```

## Online-Version (GitHub Pages)

Dieselbe Extraktion läuft auch **direkt im Browser** — keine Installation, 100 % lokal, inklusive Stereotyp-Tags:

**▶️ https://mitchel85.github.io/EAM-ADMBw-MDG-Parser/** (`web/EAM_MDG_Parser.html`)

Die Web-Version liest die Datei als `ArrayBuffer` und bestimmt das Encoding aus der
XML-Deklaration (bzw. BOM; Standard: `windows-1252`), sodass Umlaute und Sonderzeichen
korrekt erhalten bleiben. `docs/EAM_MDG_Parser.html` ist ein identischer Spiegel für
GitHub Pages.

## Quelle

Offizielle MDG-Technologie der Bundeswehr (BAAINBw):

https://www.bundeswehr.de/de/organisation/ausruestung-baainbw/vergabe/methode-architektur

Download dort: **„ADMBw MDG NAFv4"** (ZIP → `NAFv4-ADMBw-MDG-<Version>.xml`).

## Verwendung der Ausgaben

Die erzeugten `.md`-Dateien ersetzen die manuell gepflegten KB-Dateien in den anderen Tools:

- **EAM-AI-ADMBw-Script-Maker** → `references/admbw-knowledge-*.md` (LLM generiert daraus EA-Skripte)
- **EAM-AI-ADMBw-Extractor** → Wissensbasis für Prosa-Extraktion
- **EAM-AI-ADMBw-Batch** → Stereotyp-/Topologie-Prüfung der JSON-Batches
- **EAM-AI-Suite** → `tools/mdg_parser.py` + `tools/admbw_rules.json` (Regelbasis der App)

Die Suite bekommt den Parser als Kopie und erzeugt ihre Regelbasis selbst:

```bash
python3 tools/mdg_parser.py tools/NAFv4-ADMBw-MDG-2026.05.xml --suite-json tools/admbw_rules.json
```

`--suite-json` schreibt ausschließlich `admbw_rules.json` (Element-/Connector-Stereotype,
Metaconstraints, Viewpoints, Toolboxen) und keinen Markdown-Ordner.

**Ablauf bei MDG-Update:** neue XML herunterladen → Parser ausführen → `sync_tools.py` → committen.

```bash
python3 mdg_parser.py NAFv4-ADMBw-MDG-2027.01.xml -o output --no-timestamp
python3 scripts/sync_tools.py --check    # zeigt Abweichungen, Exit 1
python3 scripts/sync_tools.py            # schreibt in alle drei Tools
```

`sync_tools.py` kopiert die sechs Wissens-MDs, beide JSON und die Prompt-Datei in
Extractor, Batch und Script-Maker. Die tool-eigenen Dateien
(`ADMBw-Knowledge-Connectors.md`, `system_prompt.md`, `SKILL.md`) bleiben unangetastet;
im Prompt werden nur die Dateinamen auf das jeweilige Schema umgeschrieben.
`EAM-AI-Suite` hat aktuell kein eigenes Arbeitsverzeichnis im Workspace und wird
deshalb nicht automatisch bespielt.

## Autor & Lizenz

- **Autor:** Michael Estel
- **Lizenz:** MIT License
- Hinweis: Dieses Werkzeug liest ausschließlich die **öffentlich bereitgestellte** MDG-Technologie der Bundeswehr und erzeugt daraus Dokumentation. Es werden keine Bestandteile von Sparx Systems oder der Bundeswehr weiterverteilt.

## Rechtliches

EAM MDG Parser ist ein unabhängiges Drittanbieter-Werkzeug. Es ist nicht mit der Sparx Systems Pty Ltd
verbunden, wird von dieser nicht unterstützt und nicht gesponsert. „Sparx Systems" und
„Enterprise Architect" sind Marken oder eingetragene Marken der Sparx Systems Pty Ltd.
Alle weiteren Marken sind Eigentum ihrer jeweiligen Inhaber.
