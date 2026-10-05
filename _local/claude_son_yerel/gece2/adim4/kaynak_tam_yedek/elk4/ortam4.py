# -*- coding: utf-8 -*-
"""elk4 ortam: m8 önbelleği (tüm üçgenler, parça adı) + ışın / kutu sorguları."""
import json, re, numpy as np
S = r"@@KOK_W@@"
class Ortam:
    def __init__(s, d=S + r"\elk4\c0"):
        D = np.load(d + r"\m8_onbellek.npz"); PJ = json.load(open(d + r"\m8_parca.json", encoding="utf-8"))
        s.ad = np.array([p["ad"] for p in PJ["parca"]])
        s.A, s.B, s.C, s.P = D["A"], D["B"], D["C"], D["P"]
        s.lo = np.minimum(np.minimum(s.A, s.B), s.C); s.hi = np.maximum(np.maximum(s.A, s.B), s.C)
        s.nm = s.ad[s.P]
        # sınıflar
        kab = np.array([bool(re.search(r"__(kablo|kablo_sinyal|kablo_veri|kablo_guc)$", a)) for a in s.ad])
        kel = np.array([bool(re.match(r"ELK_\w+__celik$", a)) for a in s.ad])
        kan = np.array([bool(re.search(r"__kanal$", a)) for a in s.ad])
        s.kablo = kab[s.P]; s.kelepce = kel[s.P]; s.kanal = kan[s.P]
        s.yapi = ~s.kablo & ~s.kelepce & ~np.array([bool(re.match(r"INSAN|URUN|ZEMIN_DOSEME", a)) for a in s.ad])[s.P]
        s.ek = []
    def aday(s, lo, hi, m=None):
        k = np.all(s.hi >= lo, 1) & np.all(s.lo <= hi, 1)
        if m is not None: k &= m
        return np.where(k)[0]
    def isin(s, o, d, maxd, m=None):
        o = np.asarray(o, float); d = np.asarray(d, float); e = o + d * maxd
        c = s.aday(np.minimum(o, e) - 1e-3, np.maximum(o, e) + 1e-3, m)
        if not len(c): return np.inf, -1
        V0, V1, V2 = s.A[c], s.B[c], s.C[c]
        e1 = V1 - V0; e2 = V2 - V0; h = np.cross(d, e2); det = np.einsum('ij,ij->i', e1, h)
        ok = np.abs(det) > 1e-12; f = np.where(ok, 1 / np.where(ok, det, 1), 0)
        sv = o - V0; u = f * np.einsum('ij,ij->i', sv, h); q = np.cross(sv, e1); v = f * (q @ d); t = f * np.einsum('ij,ij->i', e2, q)
        mm = ok & (u >= 0) & (v >= 0) & (u + v <= 1) & (t > 1e-6) & (t <= maxd)
        if not mm.any(): return np.inf, -1
        i = np.argmin(np.where(mm, t, np.inf)); return float(t[i]), int(c[i])
    def kutu_kesis(s, lo, hi, m=None, e=0.05):
        """kutu (iç, e kadar küçültülmüş) ile kesişen üçgenler (SAT)"""
        lo = np.asarray(lo, float) + e; hi = np.asarray(hi, float) - e
        c = s.aday(lo, hi, m)
        if not len(c): return c
        cen = (lo + hi) / 2; h = (hi - lo) / 2
        V = np.stack([s.A[c], s.B[c], s.C[c]], 1) - cen
        ok = np.ones(len(c), bool)
        E = [V[:, 1] - V[:, 0], V[:, 2] - V[:, 1], V[:, 0] - V[:, 2]]
        for i in range(3):
            for ed in E:
                ax = np.zeros((len(c), 3)); a = np.eye(3)[i]; ax = np.cross(a[None], ed)
                p = np.einsum('nkj,nj->nk', V, ax); r = np.abs(ax) @ h
                ok &= ~((p.min(1) > r + 1e-9) | (p.max(1) < -r - 1e-9))
        n = np.cross(E[0], -E[2]); p0 = np.einsum('nj,nj->n', n, V[:, 0]); r = np.abs(n) @ h
        ok &= np.abs(p0) <= r + 1e-9
        return c[ok]


def bolge(O, lo, hi):
    """O'nun kutuya değen üçgenlerinden alt ortam (hızlı sorgu)"""
    import copy
    m = np.all(O.hi >= np.asarray(lo), 1) & np.all(O.lo <= np.asarray(hi), 1)
    o = copy.copy(O)
    for k in ("A", "B", "C", "P", "lo", "hi", "nm", "kablo", "kelepce", "kanal", "yapi"):
        setattr(o, k, getattr(O, k)[m])
    o.idx = np.where(m)[0]
    return o
