# -*- coding: utf-8 -*-
"""occupancy voxel (h mm) of triangle soup from m8 cache, excluding name regex"""
import numpy as np, json, re
S = r"@@KOK_W@@"
def yukle(d=S + r"\elk2\zj"):
    D = np.load(d + r"\m8_onbellek.npz"); PJ = json.load(open(d + r"\m8_parca.json"))["parca"]
    ad = np.array([p["ad"] for p in PJ])
    return D["A"], D["B"], D["C"], D["P"], ad, D["kpk"]
def vox(A, B, C, lo, hi, h=5.0):
    lo = np.asarray(lo, float); hi = np.asarray(hi, float)
    n = np.ceil((hi - lo) / h).astype(int) + 1
    tlo = np.minimum(np.minimum(A, B), C); thi = np.maximum(np.maximum(A, B), C)
    m = np.all(thi >= lo, 1) & np.all(tlo <= hi, 1)
    A, B, C = A[m], B[m], C[m]
    occ = np.zeros(n, bool)
    L = np.maximum(np.maximum(np.linalg.norm(B - A, axis=1), np.linalg.norm(C - A, axis=1)), np.linalg.norm(C - B, axis=1))
    K = np.minimum(np.ceil(L / (h * 0.5)).astype(int), 3000)
    for k in np.unique(K):
        sel = K == k; k = max(int(k), 1)
        u, v = np.meshgrid(np.arange(k + 1), np.arange(k + 1)); s = (u + v) <= k; u = u[s] / k; v = v[s] / k
        a, b, c = A[sel], B[sel], C[sel]
        st = max(1, 3_000_000 // len(u))
        for j in range(0, len(a), st):
            Q = a[j:j+st, None] + (b[j:j+st] - a[j:j+st])[:, None] * u[None, :, None] + (c[j:j+st] - a[j:j+st])[:, None] * v[None, :, None]
            g = np.round((Q.reshape(-1, 3) - lo) / h).astype(int)
            ok = np.all((g >= 0) & (g < n), 1); g = g[ok]
            occ[g[:, 0], g[:, 1], g[:, 2]] = True
    return occ
