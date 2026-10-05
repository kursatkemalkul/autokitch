# -*- coding: utf-8 -*-
"""Kalem 1 karşılaştırma: python d1_karsilastir.py [cak/cakisma.json] [eski_cakisma.json]
yeni taramanın GERÇEK + ŞÜPHELİ bulgularını eski 41'lik 'gerçek' listeyle (gece/m8t3/cak3, v8za; v8zq'ya kadar aynı 41) eşler:
eşleşme = aynı iki düğüm (sırasız) ve konum ≤ 40 mm. Çıktı: d1_karsilastir.txt"""
import sys, json, numpy as np
from collections import Counter
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
Y = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "cak/cakisma.json", encoding="utf-8"))
E = json.load(open(sys.argv[2] if len(sys.argv) > 2 else S + r"\gece\m8t3\cak3\cakisma.json", encoding="utf-8"))
eski = [b for b in E["bulgular"] if b["tur"] == "gerçek"]
out = open("d1_karsilastir.txt", "w", encoding="utf-8")
def yaz(*a):
    s = " ".join(str(x) for x in a); print(s); out.write(s + "\n")
def es(a, b):
    return {a["dugum_a"], a["dugum_b"]} == {b["dugum_a"], b["dugum_b"]} and np.linalg.norm(np.array(a["konum_mm"]) - np.array(b["konum_mm"])) <= 40
yaz("yeni tarama:", dict(Counter(b["tur"] for b in Y["bulgular"])), "· temas", Y["temas"], "· bileşen", Y["bilesen"])
yaz("eski gerçek liste:", len(eski))
kalan = [e for e in eski if any(es(e, y) for y in Y["bulgular"])]
gitti = [e for e in eski if not any(es(e, y) for y in Y["bulgular"])]
yaz("eski 41'den yeni taramada hâlâ çakışan %d · artık çakışmayan %d" % (len(kalan), len(gitti)))
for e in gitti: yaz("   KALKTI  %.2f mm  %s · %s ↔ %s · %s  @ %s" % (e["derinlik_mm"], e["dugum_a"], e["parca_a"], e["dugum_b"], e["parca_b"], [round(v) for v in e["konum_mm"]]))
for tur in ("gerçek", "şüpheli"):
    L = [y for y in Y["bulgular"] if y["tur"] == tur]
    yeni = [y for y in L if not any(es(e, y) for e in eski)]
    yaz("\n== %s %d · eski 41 ile eşleşen %d · YENİ %d" % (tur.upper(), len(L), len(L) - len(yeni), len(yeni)))
    for y in sorted(yeni, key=lambda y: -y["derinlik_mm"]):
        yaz("   YENİ %.2f mm · hacim %s · %s · %s ↔ %s · %s · konum %s · kutu %s · %s" % (y["derinlik_mm"], y["kesisim_hacmi_mm3"], y["dugum_a"], y["parca_a"], y["dugum_b"], y["parca_b"],
            [round(v) for v in y["konum_mm"]], y["kesisim_kutusu"], y["neden"]))
out.close()
