# -*- coding: utf-8 -*-
"""Kalem 1 fark: python d1_fark.py [yeni cak/cakisma.json] [taban cak_v9f/cakisma.json] → d1_fark.txt
eşleşme: aynı iki düğüm (sırasız) + konum ≤ 5 mm (ya da kesişim kutuları üst üste). Yeni modelde olup tabanda olmayan = adım 39/40'ın getirdiği."""
import sys, json, numpy as np
from collections import Counter
Y = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "cak/cakisma.json", encoding="utf-8"))
T = json.load(open(sys.argv[2] if len(sys.argv) > 2 else "cak_v9f/cakisma.json", encoding="utf-8"))
out = open("d1_fark.txt", "w", encoding="utf-8")
def yaz(*a):
    s = " ".join(str(x) for x in a); print(s); out.write(s + "\n")
def kut(b): return np.array(b["kesisim_kutusu"][0]), np.array(b["kesisim_kutusu"][1])
def es(a, b):
    if {a["dugum_a"], a["dugum_b"]} != {b["dugum_a"], b["dugum_b"]}: return False
    if np.linalg.norm(np.array(a["konum_mm"]) - np.array(b["konum_mm"])) <= 5: return True
    al, ah = kut(a); bl, bh = kut(b)
    return bool(((al <= bh + 1) & (ah >= bl - 1)).all())
YB, TB = Y["bulgular"], T["bulgular"]
yaz("YENİ model:", dict(Counter(b["tur"] for b in YB)), "bileşen", Y["bilesen"], "· TABAN:", dict(Counter(b["tur"] for b in TB)), "bileşen", T["bilesen"])
yeni = [b for b in YB if not any(es(b, t) for t in TB)]
giden = [t for t in TB if not any(es(b, t) for b in YB)]
yaz("YENİ modelde olup tabanda olmayan çakışma %d %s · tabanda olup yeni modelde kalkan %d %s" % (len(yeni), dict(Counter(b["tur"] for b in yeni)), len(giden), dict(Counter(b["tur"] for b in giden))))
for nm, L in (("YENİ", yeni), ("KALKAN", giden)):
    for b in sorted(L, key=lambda b: (b["tur"] != "gerçek", -b["derinlik_mm"])):
        yaz("  %-6s %-8s %.2f mm · hacim %s · %s · %s ↔ %s · %s · konum %s · kutu %s · %s" % (nm, b["tur"], b["derinlik_mm"], None if b["kesisim_hacmi_mm3"] is None else round(b["kesisim_hacmi_mm3"], 2),
            b["dugum_a"], b["parca_a"], b["dugum_b"], b["parca_b"], [round(v) for v in b["konum_mm"]], [[round(v) for v in k] for k in b["kesisim_kutusu"]], b["neden"][:70]))
out.close()
