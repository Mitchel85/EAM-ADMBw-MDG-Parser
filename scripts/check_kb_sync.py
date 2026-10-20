#!/usr/bin/env python3
"""Prüft, ob die aus dem MDG erzeugte Wissensbasis vollständig und
zahlenkonsistent ist — und ob die Downstream-Repos denselben Stand haben.

Verglichen wird gegen eine **Baseline-Datei** (JSON), nicht gegen im Code
eingebrannte Zahlen. Damit ist eine neue MDG-Version ein meldbarer Zustand
("Drift") und kein Build-Fehler.

Aufruf:
    python3 scripts/check_kb_sync.py output [downstream ...]
    python3 scripts/check_kb_sync.py output --baseline schemas/baseline-mdg-2026.05.json
    python3 scripts/check_kb_sync.py output --label 2027.01 --write-baseline schemas/baseline-mdg-2027.01.json
    python3 scripts/check_kb_sync.py output --json

Exit-Codes:
    0  Alles konsistent, Baseline unverändert
    2  DRIFT: MDG ist neuer als die Baseline (Migration ausstehend, kein Fehler)
    1  REGRESSION: Zähler gesunken, Struktur unerwartet oder Downstream unsynchron
"""
import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

EXIT_OK = 0
EXIT_REGRESSION = 1
EXIT_DRIFT = 2

DEFAULT_BASELINE = Path(__file__).resolve().parent.parent / "schemas" / "baseline-mdg-2026.05.json"

# (Baseline-Schlüssel, Quelldatei, Anzeigename)
KEYS = [
    ("stereotypes", "admbw-knowledge-stereotypes.md", "Stereotype"),
    ("topology", "admbw-knowledge-topology.md", "Topologie"),
    ("rules_complete", "admbw-knowledge-topology.md", "vollständige Regeln"),
    ("viewpoints", "admbw-knowledge-viewpoints.md", "Viewpoints"),
    ("tag_types", "admbw-knowledge-tagtypes.md", "Property-Typen"),
    ("stereotype_tags", "admbw-knowledge-stereotype-tags.md", "Stereotyp-Tags"),
]


# ---------------------------------------------------------------- Tabellen

def cells(line):
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", body)]


def table_rows(path):
    lines = [l for l in path.read_text(encoding="utf-8").splitlines() if l.startswith("|")]
    return [cells(l) for l in lines[2:]]


def viewpoints(path):
    text = path.read_text(encoding="utf-8")
    return set(re.findall(r"^## (.+)$", text, flags=re.MULTILINE)) - {"Lesart"}


def fingerprint(names):
    """Stabiler Fingerprint über eine sortierte Namensliste."""
    joined = "\n".join(sorted(n for n in names if n))
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()


def read_set(path):
    return {r[0] for r in table_rows(path) if r and r[0]}


def resolve(root, name):
    candidates = [root / name, root / "references" / name.lower()]
    for p in candidates:
        if p.is_file():
            return p
    return candidates[0]


# ---------------------------------------------------------------- Messung

def metric_block(root: Path):
    """Liest Zähler, Fingerprints und Namensmengen aus einem Ausgabeverzeichnis."""
    st_rows = table_rows(root / "admbw-knowledge-stereotypes.md")
    tp_rows = table_rows(root / "admbw-knowledge-topology.md")
    tp_complete = [r for r in tp_rows if len(r) >= 4 and r[1] and r[2]]
    vp_names = viewpoints(root / "admbw-knowledge-viewpoints.md")
    tag_rows = table_rows(root / "admbw-knowledge-tagtypes.md")
    stag_rows = table_rows(root / "admbw-knowledge-stereotype-tags.md")

    st_names = {r[0] for r in st_rows if r and r[0]}
    tp_names = {r[0] for r in tp_rows if r and r[0]}
    tag_names = {r[0] for r in tag_rows if r and r[0]}
    stag_pairs = {f"{r[0]}|{r[1]}" for r in stag_rows if len(r) >= 2 and r[0] and r[1]}

    return {
        "counts": {
            "stereotypes": len(st_rows),
            "topology": len(tp_rows),
            "rules_complete": len(tp_complete),
            "viewpoints": len(vp_names),
            "tag_types": len(tag_rows),
            "stereotype_tags": len(stag_rows),
        },
        "fingerprints": {
            "stereotypes": fingerprint(st_names),
            "topology": fingerprint(tp_names),
            "viewpoints": fingerprint(vp_names),
            "tag_types": fingerprint(tag_names),
            "stereotype_tags": fingerprint(stag_pairs),
        },
        "names": {
            "stereotypes": st_names,
            "topology": tp_names,
            "viewpoints": vp_names,
            "tag_types": tag_names,
        },
    }


def mdg_meta(root: Path):
    """Liest MDG-Version und Extraktionszeit aus admbw-meta.md, falls vorhanden."""
    meta_path = root / "admbw-meta.md"
    out: dict[str, str | None] = {"mdg_file": None, "extracted_at": None}
    if not meta_path.is_file():
        return out
    text = meta_path.read_text(encoding="utf-8")
    m = re.search(r"\*\*MDG-Version \(aus Dateiname\):\*\*\s*(\S+)", text)
    if m:
        out["mdg_file"] = m.group(1)
    m = re.search(r"\*\*Extrahiert am:\*\*\s*(.+)$", text, flags=re.MULTILINE)
    if m:
        out["extracted_at"] = m.group(1).strip()
    return out


def build_baseline(root: Path, label: str) -> dict:
    block = metric_block(root)
    return {
        "schema": 1,
        "release": label,
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": mdg_meta(root),
        "counts": block["counts"],
        "fingerprints": block["fingerprints"],
    }


# ---------------------------------------------------------------- Vergleich

def compare(actual: dict, baseline: dict):
    """Liefert (status, meldungen). status ∈ ok|drift|regression."""
    msgs = []
    status = "ok"

    for key, _file, label in KEYS:
        a = actual["counts"][key]
        b = baseline["counts"][key]
        if a < b:
            status = "regression"
            msgs.append(f"REGRESSION  {label}: {a} < Baseline {b} (Zähler gesunken)")
        elif a > b:
            if status == "ok":
                status = "drift"
            msgs.append(f"DRIFT       {label}: {a} > Baseline {b} (MDG neuer als Baseline)")
        else:
            msgs.append(f"OK          {label}: {a} = Baseline {b}")

    for key in baseline.get("fingerprints", {}):
        a = actual["fingerprints"].get(key)
        b = baseline["fingerprints"].get(key)
        if a == b:
            continue
        if actual["counts"][key] == baseline["counts"][key]:
            if status == "ok":
                status = "drift"
            msgs.append(
                f"DRIFT       {key}: gleiche Anzahl, andere Namen "
                f"(Fingerprint {a[:12]}… ≠ {b[:12]}…)"
            )
        else:
            msgs.append(f"INFO        {key}: Fingerprint abweichend (erwartbar bei geänderter Anzahl)")
    return status, msgs


def check_downstream(actual: dict, roots):
    """Downstream muss identisch zum Parser sein — sonst echter Sync-Fehler."""
    msgs = []
    ok = True
    for root in roots:
        files = {
            "stereotypes": resolve(root, "ADMBw-Knowledge-Stereotypes.md"),
            "topology": resolve(root, "ADMBw-Knowledge-Topology.md"),
            "viewpoints": resolve(root, "ADMBw-Knowledge-Viewpoints.md"),
            "tag_types": resolve(root, "ADMBw-Knowledge-TagTypes.md"),
        }
        missing = [f"{k} ({p.name})" for k, p in files.items() if not p.is_file()]
        if missing:
            ok = False
            msgs.append(f"FEHLT       {root}: {', '.join(missing)}")
            continue

        got = {
            "stereotypes": read_set(files["stereotypes"]),
            "topology": read_set(files["topology"]),
            "viewpoints": viewpoints(files["viewpoints"]),
            "tag_types": read_set(files["tag_types"]),
        }
        for key, label in (("stereotypes", "Stereotype"), ("topology", "Topologie"),
                           ("viewpoints", "Viewpoints"), ("tag_types", "Tag-Typen")):
            if got[key] != actual["names"][key]:
                ok = False
                diff = sorted(got[key] ^ actual["names"][key])[:5]
                msgs.append(f"ABWEICHUNG  {root}: {label} ≠ Parser (z.B. {', '.join(diff)})")
            else:
                msgs.append(f"OK          {root}: {label} identisch ({len(got[key])})")
    return ok, msgs


# ---------------------------------------------------------------- Haupt

def main():
    ap = argparse.ArgumentParser(description="MDG-Wissensbasis gegen Baseline prüfen")
    ap.add_argument("parser_out", type=Path)
    ap.add_argument("downstream", nargs="*", type=Path)
    ap.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE)
    ap.add_argument("--write-baseline", type=Path, metavar="PATH")
    ap.add_argument("--label", default=None, help="Release-Label für --write-baseline")
    ap.add_argument("--json", action="store_true", help="Maschinenlesbare Ausgabe")
    args = ap.parse_args()

    actual = metric_block(args.parser_out)

    if args.write_baseline:
        label = args.label or mdg_meta(args.parser_out).get("mdg_file") or "unbenannt"
        data = build_baseline(args.parser_out, label)
        args.write_baseline.parent.mkdir(parents=True, exist_ok=True)
        args.write_baseline.write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(f"Baseline geschrieben: {args.write_baseline} (release={label})")
        for k, v in data["counts"].items():
            print(f"  {k:16} {v}")
        return EXIT_OK

    if not args.baseline.is_file():
        print(f"FEHLER  Baseline nicht gefunden: {args.baseline}", file=sys.stderr)
        return EXIT_REGRESSION

    baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
    status, msgs = compare(actual, baseline)
    ds_ok, ds_msgs = check_downstream(actual, args.downstream) if args.downstream else (True, [])
    if not ds_ok:
        status = "regression"

    if args.json:
        print(json.dumps({
            "status": status,
            "baseline": str(args.baseline),
            "baseline_release": baseline.get("release"),
            "actual": actual["counts"],
            "expected": baseline["counts"],
            "messages": msgs + ds_msgs,
        }, indent=2, ensure_ascii=False))
    else:
        print(f"Baseline: {args.baseline.name} (release {baseline.get('release')})")
        print()
        for m in msgs:
            print(m)
        if ds_msgs:
            print()
            print("Downstream:")
            for m in ds_msgs:
                print("  " + m)
        print()
        if status == "ok":
            print("ERGEBNIS: OK — MDG unverändert, alles synchron.")
        elif status == "drift":
            print("ERGEBNIS: DRIFT — die MDG ist neuer als die Baseline.")
            print("Nächster Schritt: Parser prüfen, dann neue Baseline schreiben:")
            print("  python3 scripts/check_kb_sync.py <out> --label <release> \\")
            print("      --write-baseline schemas/baseline-<release>.json")
            print("Kein Build-Fehler: Exit-Code 2 ist ein Hinweis, keine Regression.")
        else:
            print("ERGEBNIS: REGRESSION — Zähler gesunken oder Downstream unsynchron.")

    return {"ok": EXIT_OK, "drift": EXIT_DRIFT, "regression": EXIT_REGRESSION}[status]


if __name__ == "__main__":
    sys.exit(main())
