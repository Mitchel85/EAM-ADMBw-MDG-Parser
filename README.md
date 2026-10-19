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
| `admbw-knowledge-stereotypes.md` | Stereotyp-Katalog: Name, Metatype, Vererbung (`generalizes` + `baseStereotypes`), AppliesTo, Beschreibung | **318 Modell-Stereotype** (davon 293 mit AppliesTo im Modell nutzbar, 25 abstrakte Basis-Stereotype ohne AppliesTo, 5 ohne Metatype) |
| `admbw-knowledge-topology.md` | Beziehungsregeln aus Metaconstraints: Quelle (client), Ziel (supplier), weitere Rollen | **203 Stereotype mit Regeln** (114 vollständig mit Quelle **und** Ziel — nur diese sind maschinell prüfbar) |
| `admbw-knowledge-viewpoints.md` | Die NAFv4-Viewpoints (DiagramProfile, ohne das Diagramm-Artefakt „Business Process“) | **52 Viewpoints** |
| `admbw-knowledge-tagtypes.md` | Tagged-Value-Definitionen mit Typeregeln (`Type=RefGUID; Values=Class; Stereotypes=…`), je `DataRow` einzeln geparst | **27 Property-Typen** |
| `admbw-meta.md` | Quelle, Version, Extraktionszeitpunkt, Statistiken, Zählweise | – |

> **Zählweise:** Die MDG enthält die Stereotype in drei getrennten Bereichen:
> `UMLProfiles` (318 Deklarationen — das Modellprofil, der eigentliche Katalog),
> `UIToolboxes` (271 Elemente / 125 UI-Toolbox-Seiten — reine Bedienoberfläche, keine Modell-Stereotype) und
> `DiagramProfile` (53 Einträge = 52 Viewpoints + 1 Diagramm-Artefakt „Business Process“).
> Der Katalog zählt ausschließlich die `UMLProfiles`-Stereotype; Toolbox-Seiten werden nicht extrahiert.
> Viewpoint-Properties gibt es in dieser MDG nicht — die `Property`-Elemente der XML sind
> Diagramm-Konfiguration (`Apply`) und werden nicht als fachliche Properties ausgegeben.

## Reproduzierbarkeit & Fehlerverhalten

- `--no-timestamp` unterdrückt Zeitstempel in allen fünf Dateien → zwei Läufe sind **byte-identisch**.
- Alternativ `SOURCE_DATE_EPOCH=<unix-zeit>` setzen → deterministischer Zeitstempel.
- Nur Dateien mit Root-Element `<MDG.Technology>` werden akzeptiert. Alle Fehler
  (Datei fehlt, kein/defektes XML, fremdes XML, IO-Fehler) beenden das Programm mit
  **Exit 2**, einer kurzen deutschen Meldung auf stderr und **ohne** Ausgabedateien.

## Online-Version (GitHub Pages)

Dieselbe Extraktion läuft auch **direkt im Browser** — keine Installation, 100 % lokal:

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
- **EAM-AI-Suite** → eingebettete Regelprüfung

**Ablauf bei MDG-Update:** neue XML herunterladen → Parser ausführen → erzeugte Dateien in die Ziel-Repos kopieren → committen. Die Tools arbeiten sofort mit den neuen Regeln.

## Autor & Lizenz

- **Autor:** Michael Estel
- **Lizenz:** MIT License
- Hinweis: Dieses Werkzeug liest ausschließlich die **öffentlich bereitgestellte** MDG-Technologie der Bundeswehr und erzeugt daraus Dokumentation. Es werden keine Bestandteile von Sparx Systems oder der Bundeswehr weiterverteilt.
