#!/usr/bin/env python3
"""Unabhängige Gegenprobe: Parser-Ausgabe gegen die MDG-XML neu berechnen.

Prüft nicht, ob der Parser dasselbe tut wie gestern, sondern ob seine Ausgabe
inhaltlich zur Quelle passt — mit einer zweiten, getrennten Implementierung.

Aufruf:
    python3 tests/verify_against_source.py [mdg.xml] [ausgabeordner]
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
XML = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "tests/fixtures/NAFv4-ADMBw-MDG-2026.05.xml"
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "output"

ok = 0
bad = 0


def check(cond, label, detail=""):
    global ok, bad
    if cond:
        ok += 1
        print(f"PASS  {label}")
    else:
        bad += 1
        print(f"FAIL  {label}")
        if detail:
            print(f"      {detail}")


def tag(e):
    return e.tag.split("}")[-1]


def cells(line):
    body = line.strip().strip("|")
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", body)]


def rows(path):
    lines = [l for l in path.read_text(encoding="utf-8").splitlines() if l.startswith("|")]
    return [cells(l) for l in lines[2:]]


def as_set(value):
    return {v.strip() for v in value.split(",") if v.strip()}


# ---------------------------------------------------------------- XML-Seite

root = ET.parse(XML).getroot()

# Modell-Stereotype: UMLProfiles > UMLProfile > Content > Stereotypes > Stereotype
model = []
for up in [e for e in root.iter() if tag(e) == "UMLProfiles"]:
    for prof in [e for e in up.iter() if tag(e) == "UMLProfile"]:
        for content in [e for e in prof if tag(e) == "Content"]:
            for grp in [e for e in content if tag(e) == "Stereotypes"]:
                model.extend([e for e in grp if tag(e) == "Stereotype"])

by_name = {}
for st in model:
    name = (st.get("name") or "").strip()
    if name and name not in by_name:
        by_name[name] = st

src_roles = {"client", "source", "end[0].role", "informationSource"}
dst_roles = {"supplier", "target", "end[1].role", "informationTarget"}

xml_topo = {}
for name, st in by_name.items():
    src, dst, other = [], [], []
    for block in [c for c in st if tag(c) == "metaconstraints"]:
        for mc in [c for c in block if tag(c) == "metaconstraint"]:
            role = mc.get("umlRole") or ""
            for part in (mc.get("constraint") or "").split(";"):
                short = part.split("::")[-1].strip()
                if not short:
                    continue
                if role in src_roles:
                    src.append(short)
                elif role in dst_roles:
                    dst.append(short)
                else:
                    other.append(f"{role} → {short}")
    if src or dst or other:
        xml_topo[name] = {
            "src": set(src), "dst": set(dst), "other": set(other),
            "complete": bool(src and dst),
        }

xml_viewpoints = set()
for dp in [e for e in root.iter() if tag(e) == "DiagramProfile"]:
    for st in [e for e in dp.iter() if tag(e) == "Stereotype"]:
        n = (st.get("name") or "").strip()
        if n and n != "Business Process":
            xml_viewpoints.add(n)

xml_tagtypes = set()
for block in [e for e in root.iter() if tag(e) == "TaggedValueTypes"]:
    for ds in [e for e in block.iter() if tag(e) == "DataSet"]:
        for row in [e for e in ds if tag(e) == "DataRow"]:
            cols = {c.get("name"): (c.get("value") or "") for c in row if tag(c) == "Column"}
            prop = cols.get("Property", "").strip()
            if prop:
                xml_tagtypes.add(prop)

xml_stags = set()
for name, st in by_name.items():
    for tvs in [c for c in st if tag(c) == "TaggedValues"]:
        for tv in [c for c in tvs if tag(c) == "Tag"]:
            t = (tv.get("name") or "").strip()
            if t:
                xml_stags.add(f"{name}|{t}")

# ---------------------------------------------------------------- MD-Seite

md_st = rows(OUT / "admbw-knowledge-stereotypes.md")
md_topo = rows(OUT / "admbw-knowledge-topology.md")
md_vp = {m.group(1).strip() for m in re.finditer(r"^## (.+)$", (OUT / "admbw-knowledge-viewpoints.md").read_text(encoding="utf-8"), re.M)}
md_vp.discard("Lesart")
md_tt = rows(OUT / "admbw-knowledge-tagtypes.md")
md_stags = {f"{r[0]}|{r[1]}" for r in rows(OUT / "admbw-knowledge-stereotype-tags.md") if len(r) >= 2}

print(f"Quelle: {XML.name}")
print()

# 1 — Katalog
check(len(by_name) == len(md_st),
      f"Stereotyp-Anzahl XML={len(by_name)} / MD={len(md_st)}")
check({r[0] for r in md_st} == set(by_name),
      "Stereotyp-Namen identisch",
      f"nur XML: {sorted(set(by_name) - {r[0] for r in md_st})[:5]} · nur MD: {sorted({r[0] for r in md_st} - set(by_name))[:5]}")

# 2 — Attribute je Stereotyp
mismatch_meta, mismatch_gen, mismatch_applies = [], [], []
for r in md_st:
    name, meta, gen, applies = r[0], r[1], r[2], r[3]
    st = by_name.get(name)
    if st is None:
        continue
    if (st.get("metatype") or "").strip() != meta:
        mismatch_meta.append((name, (st.get("metatype") or "").strip(), meta))
    parents = []
    for p in [(st.get("generalizes") or "").strip()] + (st.get("baseStereotypes") or "").replace(",", " ").split():
        if p and p not in parents:
            parents.append(p)
    if " ".join(parents) != gen:
        mismatch_gen.append((name, " ".join(parents), gen))
    x_applies = sorted({(ap.get("type") or "").strip() for at in [c for c in st if tag(c) == "AppliesTo"]
                        for ap in [c for c in at if tag(c) == "Apply"] if (ap.get("type") or "").strip()})
    if x_applies != sorted(as_set(applies)):
        mismatch_applies.append((name, x_applies, applies))

check(not mismatch_meta, "Metatype je Stereotyp korrekt", str(mismatch_meta[:3]))
check(not mismatch_gen, "Vererbung je Stereotyp korrekt", str(mismatch_gen[:3]))
check(not mismatch_applies, "AppliesTo je Stereotyp korrekt", str(mismatch_applies[:3]))

# 3 — Topologie
md_topo_map = {}
for r in md_topo:
    md_topo_map[r[0]] = {
        "src": as_set(r[1]),
        "dst": as_set(r[2]),
        "other": as_set(r[3]),
        "complete": bool(as_set(r[1]) and as_set(r[2])),
    }
check(len(md_topo) == len(xml_topo), f"Topologie-Anzahl XML={len(xml_topo)} / MD={len(md_topo)}")
check(set(md_topo_map) == set(xml_topo), "Topologie-Stereotype identisch",
      f"{sorted(set(xml_topo) ^ set(md_topo_map))[:5]}")
topo_diff = []
for n, x in xml_topo.items():
    m = md_topo_map.get(n)
    if not m:
        continue
    if (x["src"], x["dst"], x["other"]) != (m["src"], m["dst"], m["other"]):
        topo_diff.append((n, x["src"] ^ m["src"], x["dst"] ^ m["dst"], x["other"] ^ m["other"]))
check(not topo_diff, "Quelle/Ziel/weitere Rollen je Regel korrekt", str(topo_diff[:2]))
n_complete_x = sum(1 for v in xml_topo.values() if v["complete"])
n_complete_m = sum(1 for v in md_topo_map.values() if v["complete"])
check(n_complete_x == n_complete_m == 133, f"vollständige Regeln XML={n_complete_x} / MD={n_complete_m} (erwartet 133)")

# 4 — Viewpoints
check(md_vp == xml_viewpoints, f"Viewpoints XML={len(xml_viewpoints)} / MD={len(md_vp)}",
      f"{sorted(md_vp ^ xml_viewpoints)[:5]}")

# 5 — Property-Typen
check({r[0] for r in md_tt} == xml_tagtypes,
      f"Property-Typen XML={len(xml_tagtypes)} / MD={len(md_tt)}",
      f"{sorted({r[0] for r in md_tt} ^ xml_tagtypes)[:5]}")

# 6 — Stereotyp-Tags
check(md_stags == xml_stags, f"Stereotyp-Tags XML={len(xml_stags)} / MD={len(md_stags)}",
      f"{sorted(md_stags ^ xml_stags)[:5]}")

# 7 — Stichprobe: eine Regel im Roh-XML nachlesen
sample = "AchievedEffect"
x = xml_topo.get(sample, {})
check(x.get("src") == {"Achiever"} and x.get("dst") == {"ActualState"},
      f"Stichprobe {sample}: Quelle={sorted(x.get('src', []))} Ziel={sorted(x.get('dst', []))}")

print()
print(f"{ok} bestanden, {bad} fehlgeschlagen")
sys.exit(1 if bad else 0)
