# -*- coding: utf-8 -*-
"""havada.json gruplarının en yakın komşuya boşluğu (grup köşeleri → komşu yüzeyi, trimesh): python d2b_bosluk.py"""
import os, sys, json, re, numpy as np, trimesh
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "cak"))
import c8a_ortak as M
J, B, _ = M.tum_bilesenler(False)
idx = {"%s[%d]" % (b.dugum, b.no): i for i, b in enumerate(B)}
LO = np.array([b.lo for b in B]); HI = np.array([b.hi for b in B])
H = json.load(open("havada.json", encoding="utf-8"))
for g in H:
    ii = [idx[p.split(" ")[0]] for p in g["parca"] if p.split(" ")[0] in idx]
    k = np.array(g["kutu"]); lo, hi = k[:3] - 30, k[3:] + 30
    m = ((LO <= hi) & (HI >= lo)).all(1); m[ii] = False
    # grubun tüm bileşenleri (yalnız ilk 12 adı json'da) → kutu içindeki aynı-düğüm bileşenlerini de grup say
    V = np.concatenate([B[i].P.reshape(-1, 3) for i in ii])
    best = (1e9, None)
    for j in np.where(m)[0]:
        P = B[j].P; tm = trimesh.Trimesh(P.reshape(-1, 3), np.arange(len(P) * 3).reshape(-1, 3), process=False)
        _, d, _ = trimesh.proximity.closest_point(tm, V[:: max(1, len(V) // 3000)])
        if d.min() < best[0]: best = (d.min(), j)
    j = best[1]
    print("%3d bileşen %s · en yakın %.2f mm → %s" % (g["adet"], g["parca"][0], best[0], "%s[%d]" % (B[j].dugum, B[j].no) if j is not None else "-"), flush=True)
sys.stdout.flush(); os._exit(0)
