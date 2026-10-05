# -*- coding: utf-8 -*-
"""zc (@degisen, taban zb) ile zb (@degisen, taban zc) cakismalarini dugum adi cifti + derinlik + hacim ile esle -> YENI / ESKI(tasinan) / KALKAN"""
import json, sys, re
a = json.load(open(sys.argv[1], encoding="utf-8"))["T"]["cakisma"]; b = json.load(open(sys.argv[2], encoding="utf-8"))["T"]["cakisma"]
def ad(s): return re.sub(r"\[\d+\]$", "", s)
def key(c): return tuple(sorted((ad(c["parca"]), ad(c["komsu"]))))
def es(c, d):
    if key(c) != key(d): return False
    if abs(c["derinlik"] - d["derinlik"]) > 0.15: return False
    hc, hd = c.get("hacim"), d.get("hacim")
    if hc is None or hd is None: return True
    return abs(hc - hd) <= max(1.0, 0.03 * max(hc, hd))
kul = set(); yeni = []; eski = []
for c in a:
    if c["tip"] != "CAKISMA": continue
    j = next((j for j, d in enumerate(b) if j not in kul and d["tip"] == "CAKISMA" and es(c, d)), None)
    if j is None: yeni.append(c)
    else: kul.add(j); eski.append(c)
kalkan = [d for j, d in enumerate(b) if d["tip"] == "CAKISMA" and j not in kul]
out = ["zc cakisma %d · eslesen (tasinan birimle ayni, onceden var) %d · YENI %d · zb'de olup kalkan %d" % (len(eski) + len(yeni), len(eski), len(yeni), len(kalkan)), "", "== YENI"]
for c in sorted(yeni, key=lambda c: -c["derinlik"]):
    out.append("  %-40s <-> %-40s derinlik %.3f occ %s hacim %s nokta %s" % (c["parca"], c["komsu"], c["derinlik"], c.get("occ_derinlik"), c.get("hacim"), c["bilgi"]["nokta"]))
out += ["", "== KALKAN (zb'de vardi)"]
for c in sorted(kalkan, key=lambda c: -c["derinlik"]):
    out.append("  %-40s <-> %-40s derinlik %.3f nokta %s" % (c["parca"], c["komsu"], c["derinlik"], c["bilgi"]["nokta"]))
out += ["", "== ESLESEN (onceden var, birimle tasindi)"]
for c in eski: out.append("  %-40s <-> %-40s derinlik %.3f" % (c["parca"], c["komsu"], c["derinlik"]))
open(sys.argv[3], "w", encoding="utf-8").write("\n".join(out)); print("\n".join(out[:60]))
