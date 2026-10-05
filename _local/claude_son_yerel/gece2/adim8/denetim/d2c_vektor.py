# -*- coding: utf-8 -*-
"""havada gruplarının en yakın komşuya taşıma vektörü (adım 9): python d2c_vektor.py → ../../adim9/havada_vektor.json"""
import os, sys, json, numpy as np, trimesh
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "cak"))
import c8a_ortak as M
J, B, _ = M.tum_bilesenler(False)
idx = {"%s[%d]" % (b.dugum, b.no): i for i, b in enumerate(B)}
LO = np.array([b.lo for b in B]); HI = np.array([b.hi for b in B])
H = json.load(open("havada.json", encoding="utf-8"))
out = []
for g in H:
    ii = [idx[p.split(" ")[0]] for p in g["parca"] if p.split(" ")[0] in idx]
    k = np.array(g["kutu"]); lo, hi = k[:3] - 30, k[3:] + 30
    m = ((LO <= hi) & (HI >= lo)).all(1); m[ii] = False
    V = np.concatenate([B[i].P.reshape(-1, 3) for i in ii])
    best = (1e9, None, None)
    for j in np.where(m)[0]:
        P = B[j].P; tm = trimesh.Trimesh(P.reshape(-1, 3), np.arange(len(P) * 3).reshape(-1, 3), process=False)
        cp, d, _ = trimesh.proximity.closest_point(tm, V)
        a = int(np.argmin(d))
        if d[a] < best[0]: best = (float(d[a]), j, (cp[a] - V[a]).tolist())
    d, j, v = best
    r = dict(adet=g["adet"], ilk=g["parca"][0], bilesen=[(B[i].dugum, int(B[i].no), B[i].lo.tolist(), B[i].hi.tolist()) for i in ii],
             bosluk=d, komsu="%s[%d]" % (B[j].dugum, B[j].no), vektor=v)
    out.append(r); print("%3d %s · %.2f → %s · v %s · tam %s" % (g["adet"], g["parca"][0], d, r["komsu"], np.round(v, 2), len(ii) == g["adet"]), flush=True)
json.dump(out, open("../../adim9/havada_vektor.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
sys.stdout.flush(); os._exit(0)
