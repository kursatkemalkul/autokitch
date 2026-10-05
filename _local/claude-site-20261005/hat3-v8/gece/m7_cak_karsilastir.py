# -*- coding: utf-8 -*-
"""m7 çakışma karşılaştırma: yeni modelin (v8x) çakışmalarını v8w taban çakışmalarıyla PARÇA ADI çiftine göre eşler.
python m7_cak_karsilastir.py yeni.glb yeni_denetim.json taban.glb taban_denetim.json cikti.txt
Ad: çakışma noktasını içeren (en küçük kutulu) bileşenin pk / m7 adı · birim parçaları m7 ötelemesiyle eşlenir."""
import os, sys, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m7kit import Glb
from m7_etiket import etiketle, etiketle_yeni

gy, jy, gt, jt, out = sys.argv[1:6]


def adlar(G, R):
    """dugum -> [(lo, hi, ad)]"""
    D = {}
    for i, p in enumerate(G.prims):
        if len(p["T"]) == 0: continue
        tl, kut = G.komp(p)
        ad = R[i][2] if i in R else {}
        D.setdefault(p["name"], [])
        for c, (lo, hi, n) in kut.items():
            a = ad.get(c, "?")
            if a in ("?", None): a = "%s?%.0f,%.0f,%.0f" % (p["name"].replace("TOPPING_MODUL__", ""), *((lo + hi) / 2 // 5 * 5))
            D[p["name"]].append((lo, hi, a))
    return D


def ad_bul(D, parca, nokta):
    nd = parca.split("[")[0]
    q = np.array(nokta); best, bv = nd, 1e30
    for lo, hi, a in D.get(nd, []):
        if (q >= lo - 0.6).all() and (q <= hi + 0.6).all():
            v = np.prod(np.maximum(hi - lo, 0.01))
            if v < bv: bv, best = v, a
    return best


rap = os.path.join(os.path.dirname(gy), "")
GY = Glb(gy); RY = etiketle_yeni(GY, ("TOPPING_MODUL", "ELK_TOPPING", "A_GOVDE"), [os.path.join(os.path.dirname(gy), f) for f in ("v8x_b_rapor.txt", "v8x_c_rapor.txt")])
GT = Glb(gt); RT = etiketle(GT, ("TOPPING_MODUL", "ELK_TOPPING", "A_GOVDE"))
DY, DT = adlar(GY, RY), adlar(GT, RT)
CY = json.load(open(jy, encoding="utf-8"))["T"]["cakisma"]; CT = json.load(open(jt, encoding="utf-8"))["T"]["cakisma"]


def anahtar(D, r):
    a = ad_bul(D, r["parca"], r["bilgi"]["nokta"]); b = ad_bul(D, r["komsu"], r["bilgi"]["nokta"])
    import re
    norm = lambda s: re.sub(r"_\d+$", "", s)
    return tuple(sorted([norm(a), norm(b)])), a, b


TK = {}
for r in CT:
    k, a, b = anahtar(DT, r); TK.setdefault(k, []).append(r["derinlik"])
L = []; yeni = 0
for r in sorted(CY, key=lambda r: -r["derinlik"]):
    k, a, b = anahtar(DY, r)
    occ = r.get("occ_derinlik")
    sahte = isinstance(occ, list) and occ and max(occ) < 0.05
    if k in TK: tur = "ESKİ (v8w'de de var, en çok %.2f)" % max(TK[k])
    elif sahte: tur = "SAHTE (OCC derinlik 0)"
    else: tur = "YENİ"; yeni += 1
    L.append("%-40s %-46s ↔ %-46s %7.3f mm  %s · nokta %s" % (tur, a[:46], b[:46], r["derinlik"], occ, r["bilgi"]["nokta"]))
bas = "YENİ MODEL ÇAKIŞMA %d · v8w tabanında da olan %d · OCC sahte %d · YENİ %d" % (
    len(CY), sum(1 for x in L if x.startswith("ESKİ")), sum(1 for x in L if x.startswith("SAHTE")), yeni)
open(out, "w", encoding="utf-8").write(bas + "\n" + "\n".join(L))
print(bas); print("\n".join(x for x in L if x.startswith("YENİ")))
sys.stdout.flush(); os._exit(0)
