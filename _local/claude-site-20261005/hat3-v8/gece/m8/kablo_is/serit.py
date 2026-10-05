# -*- coding: utf-8 -*-
"""Silindir yan şeritlerinden doğru parça çıkarımı (dallı / birleşik kablo bileşenleri için). SALT OKUMA.
segmentler(Tc) -> [dict(a, b, r, d, n)]  (a, b: eksen uçları mm)"""
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components


def _daire(Q):
    x, y = Q[:, 0], Q[:, 1]
    A = np.c_[2 * x, 2 * y, np.ones(len(x))]; b = x * x + y * y
    s, *_ = np.linalg.lstsq(A, b, rcond=None)
    cx, cy = s[0], s[1]; r = np.sqrt(max(s[2] + cx * cx + cy * cy, 0))
    res = np.sqrt(np.mean((np.hypot(x - cx, y - cy) - r) ** 2))
    return np.array([cx, cy]), r, res


def segmentler(Tc):
    """Tc: (n,3,3) üçgen köşeleri mm"""
    if len(Tc) == 0: return []
    E = np.stack([Tc[:, 1] - Tc[:, 0], Tc[:, 2] - Tc[:, 1], Tc[:, 0] - Tc[:, 2]], 1)      # (n,3,3)
    Ln = np.linalg.norm(E, axis=2)
    n = len(Tc); idx = np.arange(n)
    U = E / np.maximum(Ln, 1e-9)[:, :, None]
    al = np.abs(U).max(2); al[Ln < 4.0] = -1
    ai = np.argmax(al, 1); best = al[idx, ai]
    D = U[idx, ai]; LA = Ln[idx, ai]
    ok = best > 0
    sg = np.sign(D[idx, np.argmax(np.abs(D), 1)]); D = D * sg[:, None]
    eks = best > 0.9995
    q = np.where(eks[:, None], np.round(D).astype(int) * 100, np.round(D * 30).astype(int))
    key = q[:, 0] * 1000000 + q[:, 1] * 1000 + q[:, 2]
    # köşe bağlantısı
    P = np.round(Tc.reshape(-1, 3), 2); u, inv = np.unique(P, axis=0, return_inverse=True); inv = inv.reshape(-1, 3)
    out = []
    for kk in np.unique(key[ok]):
        m = ok & (key == kk); ii = np.where(m)[0]
        if len(ii) < 4: continue
        Ti = inv[ii]; nv = len(u)
        r_ = np.r_[Ti[:, 0], Ti[:, 1]]; c_ = np.r_[Ti[:, 1], Ti[:, 2]]
        k, lab = connected_components(coo_matrix((np.ones(len(r_)), (r_, c_)), shape=(nv, nv)), directed=False)
        tl = lab[Ti[:, 0]]
        for g in np.unique(tl):
            jj = ii[tl == g]
            if len(jj) < 4: continue
            d = D[jj].mean(0); d /= np.linalg.norm(d)
            V = u[np.unique(inv[jj])]
            a0 = np.array([1.0, 0, 0]) if abs(d[0]) < 0.9 else np.array([0, 1.0, 0])
            e1 = np.cross(d, a0); e1 /= np.linalg.norm(e1); e2 = np.cross(d, e1)
            Q = np.c_[V @ e1, V @ e2]
            ev = np.linalg.eigvalsh(np.cov(Q.T)) if len(Q) > 2 else np.array([0, 0])
            if ev[0] < 0.05 * ev[1] or len(Q) < 6: continue
            lo2, hi2 = Q.min(0), Q.max(0); cc = (lo2 + hi2) / 2; ext = hi2 - lo2
            if ext.min() < 0.5 * ext.max(): continue
            r = float(ext.max() / 2)
            if r < 0.4 or r > 60: continue
            t = V @ d
            c3 = cc[0] * e1 + cc[1] * e2
            out.append(dict(a=c3 + t.min() * d, b=c3 + t.max() * d, r=float(r), d=d, n=len(jj)))
    # aynı eksende üst üste / bitişik olanları birleştir
    out.sort(key=lambda s: -np.linalg.norm(s['b'] - s['a']))
    bir = []
    for s in out:
        L = np.linalg.norm(s['b'] - s['a'])
        hit = False
        for t_ in bir:
            if abs(abs(np.dot(s['d'], t_['d'])) - 1) > 1e-3 or abs(s['r'] - t_['r']) > 0.3 * t_['r']: continue
            d = t_['d']; w = s['a'] - t_['a']; lat = np.linalg.norm(w - np.dot(w, d) * d)
            if lat > 0.3 * t_['r'] + 0.3: continue
            ta = np.dot(s['a'] - t_['a'], d); tb = np.dot(s['b'] - t_['a'], d); T0 = 0.0; T1 = np.dot(t_['b'] - t_['a'], d)
            lo, hi = min(ta, tb), max(ta, tb)
            if lo > T1 + t_['r'] or hi < T0 - t_['r']: continue
            n0, n1 = min(T0, lo), max(T1, hi); base = t_['a'].copy()
            t_['a'] = base + n0 * d; t_['b'] = base + n1 * d; t_['n'] += s['n']; hit = True; break
        if not hit: bir.append(dict(s))
    return bir


def kapaklar(Tc, rr):
    """uç kapakları: aynı normalli, eş düzlemli, bağlı, ~2r çaplı düz yüz kümeleri -> [(merkez, dışa normal, çap)]"""
    if len(Tc) == 0: return []
    N = np.cross(Tc[:, 1] - Tc[:, 0], Tc[:, 2] - Tc[:, 0]); A = np.linalg.norm(N, axis=1); ok = A > 1e-9
    N[ok] /= A[ok][:, None]
    q = np.round(N * 120).astype(int)
    off = np.round((Tc[:, 0] * N).sum(1) * 5).astype(int)
    key = (q[:, 0] + 200) * 10 ** 9 + (q[:, 1] + 200) * 10 ** 6 + (q[:, 2] + 200) * 10 ** 3
    P = np.round(Tc.reshape(-1, 3), 2); u, inv = np.unique(P, axis=0, return_inverse=True); inv = inv.reshape(-1, 3)
    out = []
    kk = np.stack([key, off], 1)
    _, grp = np.unique(kk[ok], axis=0, return_inverse=True); grp = grp.reshape(-1)
    ii_all = np.where(ok)[0]
    for g in range(grp.max() + 1 if len(grp) else 0):
        ii = ii_all[grp == g]
        if len(ii) < 2: continue
        Ti = inv[ii]; nv = len(u)
        r_ = np.r_[Ti[:, 0], Ti[:, 1]]; c_ = np.r_[Ti[:, 1], Ti[:, 2]]
        k, lab = connected_components(coo_matrix((np.ones(len(r_)), (r_, c_)), shape=(nv, nv)), directed=False)
        tl = lab[Ti[:, 0]]
        for h in np.unique(tl):
            jj = ii[tl == h]
            if len(jj) < 2: continue
            V = u[np.unique(inv[jj])]; n = N[jj].mean(0); n /= np.linalg.norm(n)
            a0 = np.array([1.0, 0, 0]) if abs(n[0]) < 0.9 else np.array([0, 1.0, 0])
            e1 = np.cross(n, a0); e1 /= np.linalg.norm(e1); e2 = np.cross(n, e1)
            Q = np.c_[V @ e1, V @ e2]; ext = Q.max(0) - Q.min(0)
            if ext.max() > 2.9 * rr + 1 or ext.min() < 1.2 * rr: continue
            if abs(ext[0] - ext[1]) > 0.35 * ext.max(): continue
            ar = A[jj].sum() / 2
            if ar < 0.55 * ext[0] * ext[1]: continue
            c = (Q.max(0) + Q.min(0)) / 2
            ctr = c[0] * e1 + c[1] * e2 + n * (V @ n).mean()
            out.append((ctr, n, float(ext.max())))
    return out
