# -*- coding: utf-8 -*-
"""python m8_incele.py glb DUGUM no [x0 x1 y0 y1 z0 z1] -> bilesenin duzlem gruplari (eksen hizali yuzler: eksen, deger, kapsam)"""
import sys, numpy as np
sys.path.insert(0, __import__("os").path.dirname(__file__))
from m8kit import Glb
g = Glb(sys.argv[1]); b = g.bilesen(sys.argv[2], int(sys.argv[3]))
K = [float(v) for v in sys.argv[4:10]] if len(sys.argv) > 9 else None
P = np.concatenate([p["X"][p["T"][t]] for p, t in b["parca"]])
print("kutu", b["lo"].round(2), b["hi"].round(2), "ucgen", len(P), "kapali", b["kapali"])
n = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
G = {}
for i in range(len(P)):
    Q = P[i]
    if K and not ((Q.max(0) >= [K[0], K[2], K[4]]).all() and (Q.min(0) <= [K[1], K[3], K[5]]).all()): continue
    ax = int(np.argmax(np.abs(n[i])))
    if abs(n[i][ax]) > 0.999:
        k = ("xyz"[ax], "+" if n[i][ax] > 0 else "-", round(Q[0][ax], 2))
    else:
        k = ("egik", tuple(np.round(n[i], 2)), 0)
    G.setdefault(k, []).append(Q)
for k in sorted(G, key=lambda k: (str(k[0]), str(k[2]))):
    Q = np.concatenate(G[k]); print(k, len(G[k]), Q.min(0).round(1), Q.max(0).round(1))
