# -*- coding: utf-8 -*-
"""python c8a_yuzey.py k N -> yuzey_k.json : seçili çakışmalarda iki ağın YÜZEYLERİ gerçekten kesişiyor mu (kenar-üçgen kesişimi, iki yönlü).
Seçim: OCC derinliği 0 olanlar + en az bir tarafı açık ağ / hacmi hesaplanamayan (manifold yok) çiftler. VTK iç testi kötü ağda yanılabilir."""
import os, sys, json, numpy as np
import c8a_ortak as M
k, N = int(sys.argv[1]), int(sys.argv[2])
J, B, _ = M.tum_bilesenler(False)
C = json.load(open("birlesik.json"))["cak"]
import glob
OCC = {}
for f in glob.glob("occ_*.json"): OCC.update({int(a): v for a, v in json.load(open(f)).items()})


def kenar_ucgen(P, Q, lo, hi, eps=1e-7):
    """P üçgenlerinin kenarları ↔ Q üçgenleri: kesişim noktaları"""
    def kut(X): return ((X.max(1) >= lo) & (X.min(1) <= hi)).all(1)
    P = P[kut(P)]; Q = Q[kut(Q)]
    if not len(P) or not len(Q): return np.zeros((0, 3))
    E0 = np.concatenate([P[:, 0], P[:, 1], P[:, 2]]); E1 = np.concatenate([P[:, 1], P[:, 2], P[:, 0]])
    key = np.round(np.sort(np.stack([E0, E1], 1).reshape(len(E0), -1), 1), 4)
    _, u = np.unique(np.round(np.concatenate([np.minimum(E0, E1), np.maximum(E0, E1)], 1), 4), axis=0, return_index=True)
    E0, E1 = E0[u], E1[u]
    elo = np.minimum(E0, E1); ehi = np.maximum(E0, E1)
    qlo = Q.min(1); qhi = Q.max(1)
    out = []
    v0 = Q[:, 0]; e1 = Q[:, 1] - v0; e2 = Q[:, 2] - v0
    CH = max(1, int(2e7 // max(len(Q), 1)))
    for s in range(0, len(E0), CH):
        a0, a1 = E0[s:s + CH], E1[s:s + CH]
        m = ((elo[s:s + CH, None, :] <= qhi[None]) & (ehi[s:s + CH, None, :] >= qlo[None])).all(2)
        ii, jj = np.nonzero(m)
        if not len(ii): continue
        o = a0[ii]; d = a1[ii] - a0[ii]
        E1_, E2_ = e1[jj], e2[jj]
        h = np.cross(d, E2_); a = (E1_ * h).sum(1)
        ok = np.abs(a) > eps
        f = np.zeros_like(a); f[ok] = 1.0 / a[ok]
        sv = o - v0[jj]; uu = f * (sv * h).sum(1)
        q = np.cross(sv, E1_); vv = f * (d * q).sum(1); t = f * (E2_ * q).sum(1)
        g = ok & (uu > 1e-6) & (vv > 1e-6) & (uu + vv < 1 - 1e-6) & (t > 1e-6) & (t < 1 - 1e-6)
        if g.any(): out.append(o[g] + t[g, None] * d[g])
    return np.concatenate(out) if out else np.zeros((0, 3))


res = {}
for n in range(k, len(C), N):
    r = C[n]; A, Bb = B[r["i"]], B[r["j"]]
    occ = OCC.get(n)
    sec = (isinstance(occ, list) and occ and max(occ) < 0.05) or r["hacim"] is None
    if not sec: continue
    lo = np.maximum(A.lo, Bb.lo) - 0.1; hi = np.minimum(A.hi, Bb.hi) + 0.1
    X = np.concatenate([kenar_ucgen(A.P, Bb.P, lo, hi), kenar_ucgen(Bb.P, A.P, lo, hi)])
    if len(X):
        res[n] = dict(n=int(len(X)), lo=np.round(X.min(0), 1).tolist(), hi=np.round(X.max(0), 1).tolist(), orta=np.round(X.mean(0), 1).tolist())
    else:
        res[n] = dict(n=0)
json.dump(res, open("yuzey_%02d.json" % k, "w"))
sys.stdout.flush(); os._exit(0)
