# -*- coding: utf-8 -*-
"""kaset bolgesindeki bilesenleri parca_kutulari adlariyla eslestir. python kimlik.py model.glb pk.json [x0 x1]"""
import os, sys, json, numpy as np
S = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, S)
import govde_denetim_dogru as G
glb, pkj = sys.argv[1], sys.argv[2]; x0, x1 = (float(sys.argv[3]), float(sys.argv[4])) if len(sys.argv) > 4 else (1915, 2390)
PK = json.load(open(pkj, encoding="utf-8"))["parca"]["TOPPING_MODUL"]
TUM = G.yukle_bilesen(G.glb_oku(glb), ("TOPPING_MODUL__",))
def ad(b):
    best, bs = None, 1e9
    for e in PK:
        lo = np.array([e[2], e[4], e[6]]); hi = np.array([e[3], e[5], e[7]])
        d = np.abs(lo - b.lo).sum() + np.abs(hi - b.hi).sum()
        if d < bs: best, bs = e[0], d
    return best, bs
for b in TUM:
    if b.lo[0] >= x0 and b.hi[0] <= x1 and b.lo[1] > 1130 and b.hi[2] > -560 and b.lo[2] < -80 and b.hi[1] < 1520:
        n, d = ad(b); print("%-28s %-45s fark %6.1f  lo %s hi %s kapali %s" % (b.ad, n, d, np.round(b.lo, 1).tolist(), np.round(b.hi, 1).tolist(), b.kapali))
