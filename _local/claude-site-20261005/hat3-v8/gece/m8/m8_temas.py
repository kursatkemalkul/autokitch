# -*- coding: utf-8 -*-
"""m8: parca-parca temas (<=0,5 mm) grafi. Noktalar: her parcanin kose noktalari (+ istege bagli kenar ornekleri).
Ucgen kutulari (0,5 mm sisirilmis) rtree; nokta-ucgen kesin uzaklik (Ericson)."""
import json, sys, time, numpy as np
from rtree import index
TOL = 0.5
Z = np.load("m8_onbellek.npz"); A, B, C, TPc = Z["A"], Z["B"], Z["C"], Z["P"]
lo = np.minimum(np.minimum(A, B), C) - TOL; hi = np.maximum(np.maximum(A, B), C) + TOL

def nokta_ucgen(p, a, b, c):
    ab = b - a; ac = c - a; ap = p - a
    d1 = (ab * ap).sum(1); d2 = (ac * ap).sum(1)
    bp = p - b; d3 = (ab * bp).sum(1); d4 = (ac * bp).sum(1)
    cp = p - c; d5 = (ab * cp).sum(1); d6 = (ac * cp).sum(1)
    vc = d1 * d4 - d3 * d2; vb = d5 * d2 - d1 * d6; va = d3 * d6 - d5 * d4
    den = va + vb + vc; den = np.where(np.abs(den) < 1e-18, 1e-18, den)
    v = vb / den; w = vc / den
    q = a + ab * v[:, None] + ac * w[:, None]
    # bolgeler
    m = (d1 <= 0) & (d2 <= 0); q[m] = a[m]
    m2 = (d3 >= 0) & (d4 <= d3); q[m2] = b[m2]
    m3 = (d6 >= 0) & (d5 <= d6); q[m3] = c[m3]
    t = d1 / np.where(np.abs(d1 - d3) < 1e-18, 1e-18, d1 - d3)
    m4 = (vc <= 0) & (d1 >= 0) & (d3 <= 0) & ~m & ~m2 & ~m3; q[m4] = (a + ab * t[:, None])[m4]
    t = d2 / np.where(np.abs(d2 - d6) < 1e-18, 1e-18, d2 - d6)
    m5 = (vb <= 0) & (d2 >= 0) & (d6 <= 0) & ~m & ~m2 & ~m3 & ~m4; q[m5] = (a + ac * t[:, None])[m5]
    t = (d4 - d3) / np.where(np.abs((d4 - d3) + (d5 - d6)) < 1e-18, 1e-18, (d4 - d3) + (d5 - d6))
    m6 = (va <= 0) & ((d4 - d3) >= 0) & ((d5 - d6) >= 0) & ~m & ~m2 & ~m3 & ~m4 & ~m5; q[m6] = (b + (c - b) * t[:, None])[m6]
    return np.linalg.norm(p - q, axis=1)

_IDX = None
def agac():
    global _IDX
    if _IDX is None:
        t = time.time(); p = index.Property(); p.dimension = 3
        _IDX = index.Index((np.arange(len(lo), dtype=np.int64), lo, hi), properties=p, interleaved=True)
        print("rtree %.1f s" % (time.time() - t), flush=True)
    return _IDX

def temas(pts, pid, tol=TOL, parca_haric=True, ucgen_maske=None):
    """pts Nx3, pid N (noktanin parcasi). Donus: (nokta indisi, ucgen indisi, uzaklik) <= tol (farkli parca)"""
    I = agac(); R = []
    for s in range(0, len(pts), 200000):
        p = pts[s:s + 200000]
        ids, cnt = I.intersection_v(p, p); ids = ids.astype(np.int64); cnt = cnt.astype(np.int64)
        qi = np.repeat(np.arange(len(p)), cnt) + s
        ok = TPc[ids] != pid[qi]
        if ucgen_maske is not None: ok &= ucgen_maske[ids]
        qi = qi[ok]; ids = ids[ok]
        for s2 in range(0, len(qi), 3000000):
            a = qi[s2:s2 + 3000000]; b = ids[s2:s2 + 3000000]
            d = nokta_ucgen(pts[a], A[b], B[b], C[b])
            k = d <= tol
            R.append(np.stack([a[k], b[k]], 1)); 
    return np.vstack(R) if R else np.zeros((0, 2), int)

def koseler():
    """parca basina tekil kose noktalari"""
    V = np.concatenate([A, B, C]); P = np.concatenate([TPc, TPc, TPc])
    K = np.concatenate([np.round(V, 2), P[:, None]], 1)
    u = np.unique(K, axis=0)
    return u[:, :3], u[:, 3].astype(np.int64)

def kenar_ornek(parcalar, adim=0.7, azami=400000):
    """verilen parcalarin ucgen kenarlarindan ornek noktalar"""
    m = np.isin(TPc, list(parcalar)); ti = np.where(m)[0]
    E = []
    for a_, b_ in ((A, B), (B, C), (C, A)):
        E.append(np.stack([a_[ti], b_[ti]], 1))
    E = np.concatenate(E); pid = np.concatenate([TPc[ti]] * 3)
    L = np.linalg.norm(E[:, 1] - E[:, 0], axis=1); n = np.clip(np.ceil(L / adim).astype(int), 1, 4000)
    rep = np.repeat(np.arange(len(E)), n); off = np.arange(n.sum()) - np.repeat(np.cumsum(n) - n, n)
    t = (off + 0.5) / n[rep]
    pts = E[rep, 0] + (E[rep, 1] - E[rep, 0]) * t[:, None]
    return pts, pid[rep]

if __name__ == "__main__":
    t0 = time.time()
    pts, pid = koseler(); print(len(pts), "kose", flush=True)
    R = temas(pts, pid); print(len(R), "temas cifti (nokta-ucgen) %.0f s" % (time.time() - t0), flush=True)
    pa = pid[R[:, 0]]; pb = TPc[R[:, 1]]
    E = np.unique(np.stack([np.minimum(pa, pb), np.maximum(pa, pb)], 1), axis=0)
    np.save("m8_kenar_kose.npy", E); print(len(E), "parca cifti", flush=True)
    # kose testinde temassiz gorunen parcalar: kenar ornekleriyle yeniden
    J = json.load(open("m8_parca.json")); n = len(J["parca"])
    der = np.bincount(E.reshape(-1), minlength=n)
    yalniz = set(np.where(der == 0)[0].tolist()); print(len(yalniz), "kose-temassiz parca", flush=True)
    if yalniz:
        pts2, pid2 = kenar_ornek(yalniz); print(len(pts2), "kenar ornegi", flush=True)
        R2 = temas(pts2, pid2)
        pa = pid2[R2[:, 0]]; pb = TPc[R2[:, 1]]
        E2 = np.unique(np.stack([np.minimum(pa, pb), np.maximum(pa, pb)], 1), axis=0) if len(R2) else np.zeros((0, 2), int)
        E = np.unique(np.vstack([E, E2]), axis=0)
    np.save("m8_kenar.npy", E); print(len(E), "parca cifti (son) %.0f s" % (time.time() - t0))
