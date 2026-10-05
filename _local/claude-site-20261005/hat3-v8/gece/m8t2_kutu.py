# -*- coding: utf-8 -*-
"""m8t2: verilen kutuya giren parcalar (onbellek). python m8t2_kutu.py x0 x1 y0 y1 z0 z1 [filtre]"""
import sys, json, numpy as np, os
HERE = os.path.dirname(os.path.abspath(__file__))
D = np.load(os.path.join(HERE, "m8t2", "m8_onbellek.npz")); J = json.load(open(os.path.join(HERE, "m8t2", "m8_parca.json"), encoding="utf-8"))
x0, x1, y0, y1, z0, z1 = map(float, sys.argv[1:7]); flt = sys.argv[7] if len(sys.argv) > 7 else ""
A, B, C, P = D["A"], D["B"], D["C"], D["P"]
c = (A + B + C) / 3
lo = np.minimum(np.minimum(A, B), C); hi = np.maximum(np.maximum(A, B), C)
m = (hi[:, 0] >= x0) & (lo[:, 0] <= x1) & (hi[:, 1] >= y0) & (lo[:, 1] <= y1) & (hi[:, 2] >= z0) & (lo[:, 2] <= z1)
for pi in np.unique(P[m]):
    q = J["parca"][pi]
    if flt and flt not in q["ad"]: continue
    mm = m & (P == pi)
    L = np.vstack([lo[mm], hi[mm]])
    print("%5d %-40s n%6d  kutu %s .. %s | icerde %s..%s" % (pi, q["ad"][:40], q["n"], np.round(q["lo"], 1), np.round(q["hi"], 1), np.round(L.min(0), 1), np.round(L.max(0), 1)))
