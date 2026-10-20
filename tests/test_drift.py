#!/usr/bin/env python3
"""Beweist, dass der Baseline-Check zwischen Drift und Regression unterscheidet.

Aufruf:
    python3 tests/test_drift.py

Arbeitet auf Kopien von output/ in einem temporären Verzeichnis; das echte
Ausgabeverzeichnis wird nicht angefasst.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = ROOT / "scripts" / "check_kb_sync.py"
BASELINE = ROOT / "schemas" / "baseline-mdg-2026.05.json"
OUTPUT = ROOT / "output"

passed = 0
failed = 0


def run(parser_out, *extra):
    cmd = [sys.executable, str(CHECK), str(parser_out), *extra]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def expect(name, cond, detail=""):
    global passed, failed
    if cond:
        passed += 1
        print(f"PASS  {name}")
    else:
        failed += 1
        print(f"FAIL  {name}")
        if detail:
            print("      " + detail.replace("\n", "\n      ")[:1200])


def copy_output(dst):
    shutil.copytree(OUTPUT, dst)
    return dst


def add_stereotypes(root: Path, count: int):
    path = root / "admbw-knowledge-stereotypes.md"
    lines = path.read_text(encoding="utf-8").splitlines()
    last = max(i for i, l in enumerate(lines) if l.startswith("|"))
    new = [
        f"| TestStereotype{i:03d} | TestStereotype{i:03d} | Element | "
        f"Class | – | Synthetisch für den Drift-Test. |"
        for i in range(count)
    ]
    lines[last + 1:last + 1] = new
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def drop_last_stereotype(root: Path):
    path = root / "admbw-knowledge-stereotypes.md"
    lines = path.read_text(encoding="utf-8").splitlines()
    last = max(i for i, l in enumerate(lines) if l.startswith("|"))
    del lines[last]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def drop_last_table_row(path: Path):
    """Letzte Zeile der ersten Tabelle entfernen (nicht der Folgetabellen)."""
    lines = path.read_text(encoding="utf-8").splitlines()
    start = next(i for i, l in enumerate(lines) if l.startswith("|"))
    end = start
    while end < len(lines) and lines[end].startswith("|"):
        end += 1
    del lines[end - 1]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    tmp = Path(tempfile.mkdtemp(prefix="mdg-drift-"))
    try:
        # 1 — unverändert → OK
        a = copy_output(tmp / "a")
        code, out = run(a)
        expect("unverändert → Exit 0 (OK)", code == 0, out)

        # 2 — neue MDG mit 340 statt 318 Stereotypen → Drift, kein Fehler
        b = copy_output(tmp / "b")
        add_stereotypes(b, 22)
        code, out = run(b)
        expect("+22 Stereotype → Exit 2 (DRIFT)", code == 2, out)
        expect("Drift nennt die neuen Zahlen",
               "340 > Baseline 318" in out, out)
        expect("Drift bricht den Build nicht ab (kein REGRESSION)",
               "REGRESSION" not in out, out)

        # 3 — Zähler gesunken → Regression
        c = copy_output(tmp / "c")
        drop_last_stereotype(c)
        code, out = run(c)
        expect("−1 Stereotyp → Exit 1 (REGRESSION)", code == 1, out)
        expect("Regression nennt den Rückgang", "317 < Baseline 318" in out, out)

        # 4 — gleiche Anzahl, andere Namen → Drift über Fingerprint
        d = copy_output(tmp / "d")
        p = d / "admbw-knowledge-stereotypes.md"
        text = p.read_text(encoding="utf-8")
        text = text.replace("| AchievedEffect |", "| AchievedEffectX |", 1)
        p.write_text(text, encoding="utf-8")
        code, out = run(d)
        expect("gleiche Anzahl, anderer Name → Exit 2 (DRIFT)", code == 2, out)
        expect("Fingerprint-Drift wird benannt",
               "andere Namen" in out, out)

        # 5 — Downstream unsynchron → Regression
        e = copy_output(tmp / "e")
        down = tmp / "downstream"
        down.mkdir()
        # Dateinamen exakt wie im Downstream erwartet
        for old, new in [
            ("admbw-knowledge-stereotypes.md", "ADMBw-Knowledge-Stereotypes.md"),
            ("admbw-knowledge-topology.md", "ADMBw-Knowledge-Topology.md"),
            ("admbw-knowledge-viewpoints.md", "ADMBw-Knowledge-Viewpoints.md"),
            ("admbw-knowledge-tagtypes.md", "ADMBw-Knowledge-TagTypes.md"),
        ]:
            src = ROOT / "output" / old
            shutil.copy(src, down / new)
        # Downstream absichtlich beschneiden
        tp = down / "ADMBw-Knowledge-Topology.md"
        drop_last_table_row(tp)
        code, out = run(e, str(down))
        expect("Downstream unsynchron → Exit 1", code == 1, out)
        expect("Abweichung wird benannt", "ABWEICHUNG" in out, out)

        # 6 — neue Baseline schreiben und damit wieder grün
        new_bl = tmp / "baseline-mdg-2027.01.json"
        code, out = run(b, "--label", "2027.01", "--write-baseline", str(new_bl))
        expect("Baseline schreiben → Exit 0", code == 0, out)
        data = json.loads(new_bl.read_text(encoding="utf-8"))
        expect("neue Baseline hat 340 Stereotype",
               data["counts"]["stereotypes"] == 340, str(data["counts"]))
        code, out = subprocess.run(
            [sys.executable, str(CHECK), str(b), "--baseline", str(new_bl)],
            capture_output=True, text=True
        ).returncode, ""
        expect("gegen neue Baseline → Exit 0", code == 0, out)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print()
    print(f"{passed} bestanden, {failed} fehlgeschlagen")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
