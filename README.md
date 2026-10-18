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
| `admbw-knowledge-stereotypes.md` | Stereotyp-Katalog: Name, Metatype, Vererbung, AppliesTo, Beschreibung | **642 Stereotype** |
| `admbw-knowledge-topology.md` | Beziehungsregeln aus Metaconstraints: erlaubte Ziele (client), erlaubte Quellen (supplier), weitere Rollen | **203 Stereotype mit Regeln** |
| `admbw-knowledge-viewpoints.md` | Die NAFv4-Viewpoints mit Properties und Bedeutung | **53 Viewpoints** |
| `admbw-knowledge-tagtypes.md` | Tagged-Value-Definitionen mit Typeregeln (`Type=RefGUID; Values=Class; Stereotypes=…`) | Property-Typen |
| `admbw-meta.md` | Version, Quelle, Extraktionszeitpunkt, Statistiken | – |

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
