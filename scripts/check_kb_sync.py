#!/usr/bin/env python3
"""Prüft, ob die aus dem MDG erzeugte Wissensbasis in den Downstream-Repos
vollständig und zahlenkonsistent angekommen ist.

Aufruf:
    python3 scripts/check_kb_sync.py output downstream/extractor downstream/batch downstream/script-maker
"""
import re
import sys
from pathlib import Path


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


def parses(text, pattern):
    return len(re.findall(pattern, text, flags=re.MULTILINE))


def check(cond, msg):
    print(("PASS  " if cond else "FAIL  ") + msg)
    if not cond:
        raise SystemExit(1)


def read_set(path, min_cols):
    rows = table_rows(path)
    return {r[0] for r in rows if len(r) >= min_cols and r[0]}


def resolve(root, name):
    candidates = [root / name, root / "references" / name.lower()]
    for p in candidates:
        if p.is_file():
            return p
    return candidates[0]


def main():
    if len(sys.argv) < 5:
        raise SystemExit(__doc__)
    parser = Path(sys.argv[1])
    downstream = [Path(p) for p in sys.argv[2:]]

    st = table_rows(parser / "admbw-knowledge-stereotypes.md")
    tp = table_rows(parser / "admbw-knowledge-topology.md")
    tp_complete = [r for r in tp if len(r) >= 4 and r[1] and r[2]]
    vp = parses((parser / "admbw-knowledge-viewpoints.md").read_text(encoding="utf-8"), r"^## ")
    tag = table_rows(parser / "admbw-knowledge-tagtypes.md")
    stag = table_rows(parser / "admbw-knowledge-stereotype-tags.md")

    check(len(st) == 318, f"Parser-Stereotype: {len(st)}/318")
    check(len(tp) == 203, f"Parser-Topologie: {len(tp)}/203")
    check(len(tp_complete) == 133, f"Parser vollständige Regeln: {len(tp_complete)}/133")
    check(vp == 52, f"Parser-Viewpoints: {vp}/52")
    check(len(tag) == 27, f"Parser-Property-Typen: {len(tag)}/27")
    check(len(stag) == 225, f"Parser-Stereotyp-Tags: {len(stag)}/225")

    st_names = {r[0] for r in st}
    tp_names = {r[0] for r in tp}
    down_st, down_tp = [], []
    for root in downstream:
        st_file = resolve(root, "ADMBw-Knowledge-Stereotypes.md")
        tp_file = resolve(root, "ADMBw-Knowledge-Topology.md")
        vp_file = resolve(root, "ADMBw-Knowledge-Viewpoints.md")
        tt_file = resolve(root, "ADMBw-Knowledge-TagTypes.md")
        check(st_file.is_file(), f"{root}: Stereotype-KB vorhanden")
        check(tp_file.is_file(), f"{root}: Topologie-KB vorhanden")
        check(vp_file.is_file(), f"{root}: Viewpoints-KB vorhanden")
        check(tt_file.is_file(), f"{root}: Tag-Typen-KB vorhanden")
        dst = table_rows(st_file)
        dtp = table_rows(tp_file)
        dvp = parses(vp_file.read_text(encoding="utf-8"), r"^## ")
        dtt = table_rows(tt_file)
        dtp_complete = [r for r in dtp if len(r) >= 4 and r[1] and r[2]]
        check(len(dst) == 318, f"{root}: Stereotype {len(dst)}/318")
        check(len(dtp) == 203, f"{root}: Topologie {len(dtp)}/203")
        check(len(dtp_complete) == 133, f"{root}: vollständige Regeln {len(dtp_complete)}/133")
        check(dvp == 52, f"{root}: Viewpoints {dvp}/52")
        check(len(dtt) == 27, f"{root}: Tag-Typen {len(dtt)}/27")
        check({r[0] for r in dst} == st_names, f"{root}: Stereotyp-Namen identisch")
        check({r[0] for r in dtp} == tp_names, f"{root}: Topologie-Namen identisch")
        check({r[0] for r in dtt} == {r[0] for r in tag}, f"{root}: Tag-Typ-Namen identisch")
        if not down_st:
            down_st, down_tp = dst, dtp
        else:
            check({r[0] for r in dst} == {r[0] for r in down_st}, f"{root}: Stereotype == erstes Downstream-Repo")
            check({r[0] for r in dtp} == {r[0] for r in down_tp}, f"{root}: Topologie == erstes Downstream-Repo")

    print("KB-Sync: OK")


if __name__ == "__main__":
    main()
