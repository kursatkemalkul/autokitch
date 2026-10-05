# -*- coding: utf-8 -*-
"""parca_kutulari TOPPING_MODUL kaset bolgesi girdileri: GLB bilesen kutularina 0 / +26,5 / +49,5 x kaydirmayla eslesiyor mu"""
import os, sys, json, numpy as np
S = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, S)
import govde_denetim_dogru as G
D = G.glb_oku(sys.argv[1]); PK = json.load(open(sys.argv[2], encoding="utf-8"))
B = G.yukle_bilesen(D, ("TOPPING_",)); LO = np.array([b.lo for b in B]); HI = np.array([b.hi for b in B])
def es(lo, hi, tol):
    return np.where((np.abs(LO - lo) < tol).all(1) & (np.abs(HI - hi) < tol).all(1))[0]
out = {}
for k, v in PK["parca"].items():
    if not k.startswith("TOPPING"): continue
    for e in v:
        lo = np.array([e[2], e[4], e[6]]); hi = np.array([e[3], e[5], e[7]])
        if not (1900 < e[2] < 2450): continue
        r = {dx: len(es(lo + [dx, 0, 0], hi + [dx, 0, 0], 0.6)) for dx in (0.0, 26.5, 49.5)}
        out[e[0]] = r
        print("%-50s %s" % (e[0], r))
