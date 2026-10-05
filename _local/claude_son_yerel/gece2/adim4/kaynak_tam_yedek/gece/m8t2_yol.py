# -*- coding: utf-8 -*-
"""m8t2 · yol kurucu + kademeli geçiş arayıcı (genel).
kablo = dict(r, bas=[noktalar], bacak=[(eksen, {eksen: değer, eksen: değer})], son=[noktalar], gec=[parametre aralıkları])
geçiş türleri (bacak k -> k+1):
  aynı eksen  : ('ayni', lo, hi)  -> param (t1, t2, ilk)  · t1: ilk koordinat düzlemi, t2: ikinci (aynı olabilir)
  köşe a->b   : ('kose', lo, hi)  -> param (mod, t)       · c farklıysa: mod 'once' (a ekseninde t) / 'sonra' (b ekseninde t)
bas -> bacak0 / bacak son -> son[0]: _dik sırası param ('uv' / 'vu')."""
import math, random, numpy as np
EKS = "xyz"; IX = {"x": 0, "y": 1, "z": 2}


def nokta(ax, deger, capraz):
    p = [0.0, 0.0, 0.0]; p[IX[ax]] = deger
    for e, d in capraz.items():
        if e != ax: p[IX[e]] = d
    return p


def dik(a, b, sira):
    out, c = [], list(a)
    for e in sira + "".join(x for x in EKS if x not in sira):
        i = IX[e]
        if abs(c[i] - b[i]) > 1e-6:
            c[i] = b[i]; out.append(list(c))
    return out


def kur(k, P):
    """k: kablo, P: parametre listesi (gec sırasıyla) + P0 (bas sırası) + PL (son sırası)"""
    bas, bac, son = k["bas"], k["bacak"], k["son"]
    pts = [list(map(float, q)) for q in bas]
    k["_i0"] = len(pts) - 1
    a0, p0 = bac[0]
    hedef = nokta(a0, pts[-1][IX[a0]], p0)
    pts += dik(pts[-1], hedef, k.get("bas_sira", ""))
    def sonraki_b(j, eks):
        # bacak j (ekseni eks) boyunca gidilecek son koordinat
        if j + 1 < len(bac):
            e2, p2 = bac[j + 1]
            if e2 != eks: return p2[eks]
            return None
        return son[0][IX[eks]]

    def kenet(t, a_, b_):
        if a_ is None or b_ is None: return t
        lo_, hi_ = min(a_, b_), max(a_, b_)
        if hi_ - lo_ < 2.0: return (lo_ + hi_) / 2.0
        return min(max(t, lo_ + 0.5), hi_ - 0.5)

    for i in range(len(bac) - 1):
        (a, pa), (b, pb) = bac[i], bac[i + 1]
        prm = P[i]
        if a == b:
            cur_a = pts[-1][IX[a]]; son_a = sonraki_b(i + 1, a)
            prm = tuple(kenet(t_, cur_a, son_a) if isinstance(t_, float) and j_ < (2 if len(prm) == 3 else 3) else t_ for j_, t_ in enumerate(prm))
            if len(prm) == 3:
                t1, t2 = sorted([prm[0], prm[1]], key=lambda q: abs(q - cur_a)); prm = (t1, t2, prm[2])
            else:
                ts = sorted(prm[:3], key=lambda q: abs(q - cur_a)); prm = (ts[0], ts[1], ts[2], prm[3], prm[4])
        elif abs(pa[[e for e in EKS if e not in (a, b)][0]] - pb[[e for e in EKS if e not in (a, b)][0]]) > 1e-6:
            mod, t = prm
            if mod == "once": t = kenet(float(t), pts[-1][IX[a]], pb[a])
            else: t = kenet(float(t), pa[b], sonraki_b(i + 1, b))
            prm = (mod, t)
        if a == b:
            cr = [e for e in EKS if e != a]
            cur = dict(pa)
            if len(prm) == 3:
                t1, t2, ilk = prm
                u = ilk; v = [e for e in cr if e != u][0]
                adim = [(t1, u, pb[u]), (t2, v, pb[v])]
            else:                                   # 3 hamle: (t1, t2, t3, u, m): u->m @t1, v @t2, u->son @t3
                t1, t2, t3, u, m_ = prm
                v = [e for e in cr if e != u][0]
                adim = [(t1, u, m_), (t2, v, pb[v]), (t3, u, pb[u])]
            tc = None
            for t_, e_, val in adim:
                if abs(cur[e_] - val) < 1e-6: continue
                if tc is None or abs(t_ - tc) > 1e-6:
                    pts.append(nokta(a, t_, cur)); tc = t_
                cur[e_] = val; pts.append(nokta(a, t_, cur))
            if tc is None: pts.append(nokta(a, prm[0], cur))
        else:
            c = [e for e in EKS if e not in (a, b)][0]
            if abs(pa[c] - pb[c]) < 1e-6:
                pts.append(nokta(b, pa[b], {a: pb[a], c: pa[c]})); continue
            mod, t = prm
            if mod == "once":
                pts.append(nokta(a, t, {b: pa[b], c: pa[c]})); pts.append(nokta(a, t, {b: pa[b], c: pb[c]}))
                pts.append(nokta(b, pa[b], {a: pb[a], c: pb[c]}))
            else:
                pts.append(nokta(b, pa[b], {a: pb[a], c: pa[c]})); pts.append(nokta(b, t, {a: pb[a], c: pa[c]}))
                pts.append(nokta(b, t, {a: pb[a], c: pb[c]}))
    aL, pL = bac[-1]
    E = nokta(aL, son[0][IX[aL]], pL)
    pts.append(E)
    k["_E"] = list(E)
    pts += dik(E, list(son[0]), k.get("son_sira", ""))
    pts += [list(map(float, q)) for q in son[1:]]
    q = [pts[0]]
    for p in pts[1:]:
        if math.dist(p, q[-1]) > 0.05: q.append(p)
    # doğrusal ara noktaları at
    r = [q[0]]
    for i in range(1, len(q) - 1):
        d1 = np.subtract(q[i], r[-1]); d2 = np.subtract(q[i + 1], q[i])
        if np.linalg.norm(np.cross(d1, d2)) < 1e-6 and np.dot(d1, d2) > 0: continue
        r.append(q[i])
    r.append(q[-1])
    return np.array(r)


# ------------------------------------------------------------------ vektörel denetim
def segler(Y):
    """Y: {ad: (r, pts, sinirsiz_idx set)} -> diziler"""
    A, B, R, O, I = [], [], [], [], []
    for j, (ad, (r, p)) in enumerate(Y.items()):
        A.append(p[:-1]); B.append(p[1:]); R.append(np.full(len(p) - 1, r)); O.append(np.full(len(p) - 1, j)); I.append(np.arange(len(p) - 1))
    return np.vstack(A), np.vstack(B), np.concatenate(R), np.concatenate(O), np.concatenate(I)


def segseg_v(P1, Q1, P2, Q2):
    d1 = Q1 - P1; d2 = Q2 - P2; r = P1 - P2
    a = (d1 * d1).sum(1); e = (d2 * d2).sum(1); f = (d2 * r).sum(1); c = (d1 * r).sum(1); b = (d1 * d2).sum(1)
    den = a * e - b * b
    s = np.where(den > 1e-12, np.clip((b * f - c * e) / np.where(den > 1e-12, den, 1), 0, 1), 0.0)
    t = (b * s + f) / np.where(e > 1e-12, e, 1)
    m0 = t < 0; m1 = t > 1
    t = np.clip(t, 0, 1)
    s = np.where(m0, np.clip(-c / np.where(a > 1e-12, a, 1), 0, 1), s)
    s = np.where(m1, np.clip((b - c) / np.where(a > 1e-12, a, 1), 0, 1), s)
    C1 = P1 + d1 * s[:, None]; C2 = P2 + d2 * t[:, None]
    return np.linalg.norm(C1 - C2, axis=1), (C1 + C2) / 2


def carpisma(Y, engel=None, bosluk=0.3, odak=None):
    """Y: {ad: (r, pts)} · engel: [(ad, r, pts)] sabit · odak: yalnız bu ada ait çiftler. -> [(a, b, nokta, derinlik)]"""
    ad = list(Y)
    YY = dict(Y)
    if engel:
        for n, r, p in engel: YY["#" + n] = (r, np.asarray(p, float))
    adl = list(YY)
    A, B, R, O, I = segler(YY)
    lo = np.minimum(A, B) - R[:, None]; hi = np.maximum(A, B) + R[:, None]
    n = len(A)
    out = []
    oi = None if odak is None else set(adl.index(o) for o in odak)
    # x boyunca süpürme ile aday çiftler
    ordr = np.argsort(lo[:, 0]); los = lo[ordr]; his = hi[ordr]
    ii, jj = [], []
    for k in range(n):
        i = ordr[k]
        j = k + 1
        # aday: lo_j <= hi_i
        e = np.searchsorted(los[:, 0], his[k, 0] + bosluk, side="right")
        cand = ordr[k + 1:e]
        if not len(cand): continue
        m = np.all((lo[cand] <= hi[i] + bosluk) & (hi[cand] >= lo[i] - bosluk), axis=1)
        cand = cand[m]
        cand = cand[O[cand] != O[i]]
        if oi is not None:
            cand = cand[np.isin(O[cand], list(oi)) | (O[i] in oi)]
        # iki engel arasını sayma
        if adl[O[i]].startswith("#"):
            cand = cand[[not adl[O[c]].startswith("#") for c in cand]]
        if len(cand):
            ii.append(np.full(len(cand), i)); jj.append(cand)
    if not ii: return []
    ii = np.concatenate(ii); jj = np.concatenate(jj)
    d, M = segseg_v(A[ii], B[ii], A[jj], B[jj])
    lim = R[ii] + R[jj] + bosluk
    h = d < lim - 1e-6
    for i_, j_, d_, m_, l_ in zip(ii[h], jj[h], d[h], M[h], lim[h]):
        out.append((adl[O[i_]], adl[O[j_]], m_, l_ - d_))
    return out


KUTU = [((3327.5, 3423.5), (2105.0, 2175.0), (-692.0, -300.0)), ((3327.5, 3423.5), (2139.5, 2175.0), (-300.0, -125.0)),
        ((3280.0, 3984.0), (2106.5, 2166.5), (-824.5, -691.5)), ((2920.0, 3280.0), (2106.5, 2166.5), (-824.5, -749.5)),
        ((2575.0, 2920.0), (2139.5, 2166.5), (-824.5, -657.5)), ((2575.0, 2920.0), (2106.5, 2166.5), (-786.1, -657.5)),
        ((1993.0, 2575.0), (2106.5, 2166.5), (-824.5, -691.5)), ((1250.0, 1993.0), (2144.5, 2165.0), (-824.5, -767.5)),
        ((3984.0, 4016.0), (2144.5, 2163.5), (-824.5, -767.5)), ((4016.0, 5200.0), (2126.5, 2165.0), (-824.5, -767.5)),
        ((4281.5, 4318.5), (1890.0, 2127.0), (-824.5, -750.0)), ((5081.5, 5118.5), (1890.0, 2127.0), (-824.5, -750.0)),
        ((2452.0, 2478.0), (1255.0, 2106.5), (-826.5, -701.5)), ((2422.5, 2478.0), (1255.0, 1320.0), (-826.5, -632.5)),
        ((2422.5, 2466.5), (1100.0, 1257.0), (-686.0, -632.5)), ((2422.5, 2449.5), (744.0, 1104.0), (-698.0, -560.0)),
        ((2422.5, 4140.0), (744.0, 784.0), (-760.0, -642.0)), ((4100.0, 4140.0), (48.0, 784.0), (-700.0, -642.0)),
        ((4041.5, 4148.5), (1.5, 50.0), (-708.5, -136.5)), ((4041.5, 5407.5), (1.5, 50.0), (-193.5, -136.5)),
        ((5350.5, 5407.5), (1.5, 50.0), (-193.5, 598.5)), ((5350.5, 5518.5), (1.5, 50.0), (541.5, 598.5)),
        ((5461.5, 5518.5), (1.5, 50.0), (541.5, 988.5)), ((5467.5, 5514.5), (1.5, 1120.0), (926.5, 973.5)),
        ((3640.0, 3850.0), (2015.0, 2140.0), (-700.0, -400.0)),
        ((5304.5, 5430.5), (1.5, 84.5), (590.0, 653.5))]
_KL = np.array([[b[0][0], b[1][0], b[2][0]] for b in KUTU]); _KH = np.array([[b[0][1], b[1][1], b[2][1]] for b in KUTU])


def disari(k, P, adim=4.0, tol=0.3):
    """i0..E arasi orneklerden kutularin disinda kalan sayisi"""
    r = k["r"]; E = np.array(k["_E"]); i0 = k["_i0"]
    # E'nin indeksi
    d = np.linalg.norm(P - E, axis=1); iE = int(np.argmin(d))
    Q = []
    for a, b in zip(P[i0:iE], P[i0 + 1:iE + 1]):
        L = np.linalg.norm(b - a); n = max(2, int(L / adim) + 1)
        Q.append(a + np.linspace(0, 1, n)[:, None] * (b - a))
    if not Q: return 0, None
    Q = np.vstack(Q)
    ic = np.zeros(len(Q), bool)
    for lo, hi in zip(_KL, _KH):
        ic |= np.all((Q >= lo + r - tol) & (Q <= hi - r + tol), axis=1)
    return int((~ic).sum()), (Q[~ic][0] if (~ic).any() else None)
