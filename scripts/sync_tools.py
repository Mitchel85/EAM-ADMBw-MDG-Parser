#!/usr/bin/env python3
"""Synchronisiert die Parser-Ausgabe in die EAM-Tools.

Quelle ist immer ``output/`` dieses Repos. Die Tools bekommen dieselben
Regeldateien unter ihren jeweiligen Namen; der Prompt wird dabei auf die
dortigen Dateinamen umgeschrieben.

Aufruf:
    python3 scripts/sync_tools.py            # schreiben
    python3 scripts/sync_tools.py --check    # nur prüfen (Exit 1 bei Abweichung)
    python3 scripts/sync_tools.py --tool EAM-AI-ADMBw-Batch

Nicht angefasst werden tool-eigene Dateien (z. B. ``ADMBw-Knowledge-Connectors.md``
oder ``system_prompt.md``) — sie stammen nicht aus dem Parser.
"""
import argparse
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "output"
WORKSPACE = BASE.parent

# Quellname -> Zielname je Tool. Der Prompt wird zusätzlich im Text umgeschrieben.
TOOLS = {
    "EAM-AI-ADMBw-Extractor": {
        "dir": WORKSPACE / "EAM-AI-ADMBw-Extractor",
        "names": {
            "admbw-knowledge-stereotypes.md": "ADMBw-Knowledge-Stereotypes.md",
            "admbw-knowledge-topology.md": "ADMBw-Knowledge-Topology.md",
            "admbw-knowledge-viewpoints.md": "ADMBw-Knowledge-Viewpoints.md",
            "admbw-knowledge-tagtypes.md": "ADMBw-Knowledge-TagTypes.md",
            "admbw-knowledge-stereotype-tags.md": "ADMBw-Knowledge-Stereotype-Tags.md",
            "admbw-meta.md": "ADMBw-Meta.md",
            "admbw-stereotypes.json": "ADMBw-Stereotypes.json",
            "admbw-aliases.json": "ADMBw-Aliases.json",
            "admbw-prompt.md": "ADMBw-Prompt.md",
        },
    },
    "EAM-AI-ADMBw-Batch": {
        "dir": WORKSPACE / "EAM-AI-ADMBw-Batch",
        "names": {
            "admbw-knowledge-stereotypes.md": "ADMBw-Knowledge-Stereotypes.md",
            "admbw-knowledge-topology.md": "ADMBw-Knowledge-Topology.md",
            "admbw-knowledge-viewpoints.md": "ADMBw-Knowledge-Viewpoints.md",
            "admbw-knowledge-tagtypes.md": "ADMBw-Knowledge-TagTypes.md",
            "admbw-knowledge-stereotype-tags.md": "ADMBw-Knowledge-Stereotype-Tags.md",
            "admbw-meta.md": "ADMBw-Meta.md",
            "admbw-stereotypes.json": "ADMBw-Stereotypes.json",
            "admbw-aliases.json": "ADMBw-Aliases.json",
            "admbw-prompt.md": "ADMBw-Prompt.md",
        },
    },
    "EAM-AI-ADMBw-Script-Maker": {
        "dir": WORKSPACE / "EAM-AI-ADMBw-Script-Maker" / "references",
        "names": {
            "admbw-knowledge-stereotypes.md": "admbw-knowledge-stereotypes.md",
            "admbw-knowledge-topology.md": "admbw-knowledge-topology.md",
            "admbw-knowledge-viewpoints.md": "admbw-knowledge-viewpoints.md",
            "admbw-knowledge-tagtypes.md": "admbw-knowledge-tagtypes.md",
            "admbw-knowledge-stereotype-tags.md": "admbw-knowledge-stereotype-tags.md",
            "admbw-meta.md": "admbw-meta.md",
            "admbw-stereotypes.json": "admbw-stereotypes.json",
            "admbw-aliases.json": "admbw-aliases.json",
            "admbw-prompt.md": "admbw-prompt.md",
        },
    },
}


def rewrite_prompt(text, names):
    """Ersetzt die Parser-Dateinamen im Prompt durch die Zielnamen.

    Längste Namen zuerst, damit ``…-stereotypes.md`` nicht in
    ``…-stereotype-tags.md`` hineinläuft.
    """
    for src in sorted(names, key=len, reverse=True):
        text = text.replace(src, names[src])
    return text


def expected(source_name, content, names):
    if source_name == "admbw-prompt.md":
        return rewrite_prompt(content, names)
    return content


def main():
    ap = argparse.ArgumentParser(description="Parser-Ausgabe in die EAM-Tools spiegeln")
    ap.add_argument("--check", action="store_true",
                    help="Nur prüfen, nichts schreiben (Exit 1 bei Abweichung)")
    ap.add_argument("--tool", choices=sorted(TOOLS), help="Nur ein Tool bearbeiten")
    args = ap.parse_args()

    if not OUT.is_dir():
        print(f"FEHLER: Ausgabeordner fehlt: {OUT}", file=sys.stderr)
        return 2

    missing = [n for n in next(iter(TOOLS.values()))["names"] if not (OUT / n).is_file()]
    if missing:
        print("FEHLER: Parser-Ausgabe unvollständig:", ", ".join(missing), file=sys.stderr)
        return 2

    problems = 0
    for tool, cfg in TOOLS.items():
        if args.tool and tool != args.tool:
            continue
        target_dir = cfg["dir"]
        if not target_dir.is_dir():
            print(f"{tool}: FEHLER — Zielordner fehlt ({target_dir})", file=sys.stderr)
            problems += 1
            continue

        print(tool)
        for src_name, dst_name in cfg["names"].items():
            content = (OUT / src_name).read_text(encoding="utf-8")
            want = expected(src_name, content, cfg["names"])
            dst = target_dir / dst_name
            if dst.is_file():
                have = dst.read_text(encoding="utf-8")
                state = "OK   " if have == want else "DIFF "
            else:
                state = "NEU  "
                have = None

            if state != "OK   ":
                problems += 1
                print(f"  {state} {dst_name}")
                if not args.check:
                    dst.write_text(want, encoding="utf-8")
            else:
                print(f"  {state} {dst_name}")

    if args.check:
        print("\nERGEBNIS:", "OK — alle Tools synchron" if problems == 0
              else f"{problems} Abweichung(en)")
        return 0 if problems == 0 else 1

    print(f"\nFertig: {problems} Datei(en) geschrieben.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
