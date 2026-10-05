# -*- coding: utf-8 -*-
"""B çekmece sensör kabloları: arka duvarda kat başına kapaklı kanal + çekmece rayı ile yan duvar arasında yassı kapaklı kanal"""
import numpy as np
from b4lib import KAY
IST = "B"
def K(ad, e, lo, hi, **kw): return dict(ad=ad, e=e, lo=lo, hi=hi, ist=IST, **kw)
KX = {806: 988.5, 1461: 1643.5, 2116: 2298.5, 2771: 2953.5, 3426: 3608.5}
VAR_KANAL = []; KAN = []; YOL = {}
for ci, d in enumerate(KAY):
    if d["ist"] != "B" or not d["S"] or d["prim"] != "ELK_DOLAP__kablo_sinyal": continue
    zs = [q for q in d["S"] if abs(q["b"][2] - q["a"][2]) > 600]
    if not zs: continue
    q = zs[0]; c = round(float(q["a"][0]), 1); yL = float(q["a"][1])
    cx = min(KX, key=lambda k: abs(k - c)); Kx = KX[cx]
    y0 = round(yL - 11.6)
    yb = [s for s in d["S"] if abs(s["b"][0] - s["a"][0]) > 100]
    if yb: y0 = min((float(s_["a"][1]) for s_ in yb), key=lambda v: abs(v - (yL - 11.6)))
    xc = c - 2.6
    YOL[ci] = dict(yol=[[(Kx - 0.2, y0, -777), (xc, y0, -777), (xc, y0, -760), (xc, yL, -760), (xc, yL, -55), (xc, y0, -55), (c - 0.6, y0, -55)]])
    KAN.append(K("Byan%d" % ci, 2, (c - 7.6, yL - 11, -758), (c + 2.1, yL + 11, -62)))
    KAN.append(K("Barka%d" % ci, 0, (c + (64 if y0 > 680 else 10), y0 - 7, -790), (Kx, min(y0 + 19, 702.9), -760)))
for k in KAN:
    if k["ad"] == "Barka130": k["lo"] = (k["lo"][0], k["lo"][1] + 3.5, k["lo"][2])
