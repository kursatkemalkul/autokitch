# -*- coding: utf-8 -*-
"""Kalem 4 kablo↔kablo: python d4_kablo.py [cak/cakisma.json]  → iki tarafı da …kablo… düğümünde olan çakışmalar (sınıf + derinlik)"""
import sys, json
from collections import Counter
Y = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "cak/cakisma.json", encoding="utf-8"))["bulgular"]
K = [y for y in Y if "kablo" in y["dugum_a"].lower() and "kablo" in y["dugum_b"].lower()]
print("kablo↔kablo çakışma", len(K), dict(Counter(y["tur"] for y in K)))
for y in sorted(K, key=lambda y: -y["derinlik_mm"]):
    print("  %-8s %.2f mm · hacim %s · %s · %s ↔ %s · %s · konum %s · %s" % (y["tur"], y["derinlik_mm"], None if y["kesisim_hacmi_mm3"] is None else round(y["kesisim_hacmi_mm3"], 1),
          y["dugum_a"], y["parca_a"], y["dugum_b"], y["parca_b"], [round(v) for v in y["konum_mm"]], y["neden"][:60]))
