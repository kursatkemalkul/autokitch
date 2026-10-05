# -*- coding: utf-8 -*-
"""elk2 ortak: yeni dugum ekleme (yeni malzeme), plaka/kutu/kanal geometrisi, kablo tupu, carpisma sorgusu + dik acili yol arayici."""
import sys, json, itertools, numpy as np
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\gece2\k3_uyum\z55A"
sys.path.insert(0, S + r"\gece"); sys.path.insert(0, S); sys.path.insert(0, S + r"\birlesim")
from m8kit import kutu_ucgen, silindir_ucgen, kure_ucgen

KAT = dict(GOVDE=0, MEKANIZMA=1, MOTOR=2, SENSOR=3, HAVA=4, SOGUTMA=5, ELEKTRIK=6, KONTROL=7, GIDA=8, ROBOT=9, URUN=10, DUKKAN=11)


def mekno(G, kod):
    L = [m["kod"] for m in G.J["scenes"][0]["extras"]["mekanizmalar"]]
    return L.index(kod)


# ------------------------------------------------------------------ yeni dugum
class Yeni:
    """ad -> (malzeme, [(P (n,3,3) mm dunya, kat, mek)])"""
    def __init__(s):
        s.d = {}

    def ekle(s, ad, mal, P, kat, mek):
        P = np.asarray(P, float).reshape(-1, 3, 3)
        if not len(P): return 0
        s.d.setdefault(ad, [mal, []])[1].append((P, kat, mek)); return len(P)

    def yaz(s, G):
        J = G.J
        for ad, (mal, L) in s.d.items():
            mname, renk, met, ruf = mal
            mi = None
            for i, m in enumerate(J["materials"]):
                if m.get("name") == mname: mi = i
            if mi is None:
                J["materials"].append({"name": mname, "pbrMetallicRoughness": {"baseColorFactor": list(renk), "metallicFactor": met, "roughnessFactor": ruf}, "doubleSided": True})
                mi = len(J["materials"]) - 1
            # mevcut dugum varsa ona yeni primitive
            Xs, Ns, kat, mek = [], [], [], []; base = 0
            for P, k, m in L:
                V = P.reshape(-1, 3) / 1000.0
                n = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]); n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
                Xs.append(V); Ns.append(np.repeat(n, 3, axis=0))
                cnt = len(V)
                if kat and kat[-3] == k and kat[-2] + kat[-1] == base: kat[-1] += cnt
                else: kat += [k, base, cnt]
                if mek and mek[-3] == m and mek[-2] + mek[-1] == base: mek[-1] += cnt
                else: mek += [m, base, cnt]
                base += cnt
            X = np.vstack(Xs).astype(np.float32); N = np.vstack(Ns).astype(np.float32)
            pa = G._ekle_arr(X, "VEC3", 34962); na = G._ekle_arr(N, "VEC3", 34962)
            ia = G._ekle_arr(np.arange(len(X), dtype=np.uint32), "SCALAR", 34963)
            prim = {"attributes": {"POSITION": pa, "NORMAL": na}, "indices": ia, "material": mi, "extras": {"kat": kat, "mek": mek}}
            ni = [i for i, nd in enumerate(J["nodes"]) if nd.get("name") == ad]
            if ni:
                J["meshes"][J["nodes"][ni[0]]["mesh"]]["primitives"].append(prim)
            else:
                J["meshes"].append({"name": ad, "primitives": [prim]})
                J["nodes"].append({"name": ad, "mesh": len(J["meshes"]) - 1})
                J["scenes"][0]["nodes"].append(len(J["nodes"]) - 1)


# ------------------------------------------------------------------ geometri
def kutu(lo, hi):
    return kutu_ucgen(lo, hi)


def plaka(eksen, v0, v1, u0, u1, w0, w1, delikler=()):
    """eksen normalli plaka (kalinlik v0..v1), dikdortgen [u0,u1]x[w0,w1] (u,w artan eksen sirasi), delikler [(u0,u1,w0,w1)] -> kutular (u seritleri)"""
    a = eksen; u, w = [i for i in range(3) if i != a]
    us = sorted(set([u0, u1] + [max(u0, min(u1, d[k])) for d in delikler for k in (0, 1)]))
    out = []
    for ua, ub in zip(us[:-1], us[1:]):
        if ub - ua < 1e-6: continue
        um = (ua + ub) / 2
        ws = [(w0, w1)]
        for d in delikler:
            if d[0] < um < d[1]:
                nw = []
                for wa, wb in ws:
                    if d[3] <= wa or d[2] >= wb: nw.append((wa, wb)); continue
                    if d[2] > wa: nw.append((wa, d[2]))
                    if d[3] < wb: nw.append((d[3], wb))
                ws = nw
        for wa, wb in ws:
            if wb - wa < 1e-6: continue
            lo = np.zeros(3); hi = np.zeros(3)
            lo[a], hi[a] = v0, v1; lo[u], hi[u] = ua, ub; lo[w], hi[w] = wa, wb
            out.append(kutu_ucgen(lo, hi))
    return np.concatenate(out) if out else np.zeros((0, 3, 3))


def kanal(eks, a0, a1, lo2, hi2, t=1.5, acik=(), uc=(True, True), delik=None):
    """eksen eks boyunca dikdortgen kanal: kesit [lo2,hi2] (diger iki eksen, artan sira), 4 cidar t (+ uc kapaklari).
    delik: {'yuz': (eksen, +-1), [(a0,a1,b0,b1)] } -> cidarda ag. acik: atlanan cidarlar [(eksen, +-1)]."""
    u, w = [i for i in range(3) if i != eks]
    out = []
    ea0 = a0 + (t if uc[0] else 0.0); ea1 = a1 - (t if uc[1] else 0.0)
    for ax, sg in ((u, -1), (u, 1), (w, -1), (w, 1)):
        if (ax, sg) in acik: continue
        oth = w if ax == u else u
        oi = 0 if oth == u else 1; ai = 0 if ax == u else 1
        v0 = lo2[ai] if sg < 0 else hi2[ai] - t
        v1 = v0 + t
        # plaka ekseni ax; diger eksenler (eks, oth) artan sira · w-duvarlari u-duvarlarinin arasina (kose bindirmesi yok)
        ql = sorted([eks, oth])
        o0, o1 = lo2[oi], hi2[oi]
        if ax == w:
            if (u, -1) not in acik: o0 += t
            if (u, 1) not in acik: o1 -= t
        rng = {eks: (ea0, ea1), oth: (o0, o1)}
        dl = (delik or {}).get((ax, sg), [])
        # delik: (eks0, eks1, oth0, oth1) -> sira
        dd = []
        for d in dl:
            r = {eks: (d[0], d[1]), oth: (d[2], d[3])}
            dd.append((r[ql[0]][0], r[ql[0]][1], r[ql[1]][0], r[ql[1]][1]))
        out.append(plaka(ax, v0, v1, rng[ql[0]][0], rng[ql[0]][1], rng[ql[1]][0], rng[ql[1]][1], dd))
    for k, a in enumerate((a0, a1)):
        if not uc[k]: continue
        lo = np.zeros(3); hi = np.zeros(3)
        lo[eks], hi[eks] = (a, a + t) if k == 0 else (a - t, a)
        lo[u], hi[u] = lo2[0], hi2[0]; lo[w], hi[w] = lo2[1], hi2[1]
        out.append(kutu_ucgen(lo, hi))
    return np.concatenate(out)


def silindir(p0, p1, r, n=20):
    return silindir_ucgen(p0, p1, r, n)


def tup(Q, r, n=16):
    """dik acili kablo: noktalar arasi silindir + kose kuresi (kapali parcalar)"""
    Q = [np.asarray(q, float) for q in Q]; out = []
    for a, b in zip(Q[:-1], Q[1:]):
        if np.linalg.norm(b - a) > 1e-6: out.append(silindir_ucgen(a, b, r, n))
    for q in Q[1:-1]: out.append(kure_ucgen(q, r, n, 8))
    return np.concatenate(out)


# ------------------------------------------------------------------ carpisma
class Engel:
    def __init__(s, npz, haric_parca=()):
        D = np.load(npz)
        A, B, C = D["A"], D["B"], D["C"]; P = D["P"]
        m = ~np.isin(P, list(haric_parca)) if haric_parca else np.ones(len(A), bool)
        s.A, s.B, s.C, s.P = A[m], B[m], C[m], P[m]
        s.lo = np.minimum(np.minimum(s.A, s.B), s.C); s.hi = np.maximum(np.maximum(s.A, s.B), s.C)
        s.ek = []          # eklenen engeller (n,3,3)

    def ekle(s, T):
        T = np.asarray(T, float).reshape(-1, 3, 3)
        s.A = np.vstack([s.A, T[:, 0]]); s.B = np.vstack([s.B, T[:, 1]]); s.C = np.vstack([s.C, T[:, 2]])
        s.P = np.concatenate([s.P, np.full(len(T), -1)])
        s.lo = np.vstack([s.lo, T.min(1)]); s.hi = np.vstack([s.hi, T.max(1)])

    def aday(s, lo, hi):
        return np.where(np.all(s.hi >= lo, 1) & np.all(s.lo <= hi, 1))[0]

    def seg_mesafe(s, p0, p1, r, adim=2.0, haric=None):
        """segment etrafindaki en kucuk ucgen mesafesi (yaklasik: segment ornekleri). haric(i)->bool maskesi"""
        p0 = np.asarray(p0, float); p1 = np.asarray(p1, float)
        lo = np.minimum(p0, p1) - r - 1; hi = np.maximum(p0, p1) + r + 1
        ii = s.aday(lo, hi)
        if haric is not None and len(ii): ii = ii[~haric(ii)]
        if not len(ii): return 1e9, None
        L = np.linalg.norm(p1 - p0); n = max(2, int(L / adim) + 1)
        Q = p0[None] + (p1 - p0)[None] * np.linspace(0, 1, n)[:, None]
        best = 1e9; bi = None
        for k in range(0, len(ii), 3000):
            jj = ii[k:k + 3000]
            d = _pt_tri(Q, s.A[jj], s.B[jj], s.C[jj])   # (nQ, nT)
            j = np.unravel_index(np.argmin(d), d.shape)
            if d[j] < best: best = float(d[j]); bi = int(jj[j[1]])
        return best, bi

    def yol_bos(s, Q, r, pay=0.5, haric=None, uc_haric=0.0):
        for a, b in zip(Q[:-1], Q[1:]):
            d, i = s.seg_mesafe(a, b, r + pay, haric=haric)
            if d < r + pay: return False, (a, b, d, i)
        return True, None


def _pt_tri(Q, A, B, C):
    """noktalar Q (m,3) ile ucgenler (n) arasi mesafe matrisi (m,n) — Ericson closest point"""
    Q = Q[:, None, :]; A = A[None]; B = B[None]; C = C[None]
    ab = B - A; ac = C - A; ap = Q - A
    d1 = (ab * ap).sum(-1); d2 = (ac * ap).sum(-1)
    bp = Q - B; d3 = (ab * bp).sum(-1); d4 = (ac * bp).sum(-1)
    cp = Q - C; d5 = (ab * cp).sum(-1); d6 = (ac * cp).sum(-1)
    va = d3 * d6 - d5 * d4; vb = d5 * d2 - d1 * d6; vc = d1 * d4 - d3 * d2
    den = va + vb + vc; den = np.where(np.abs(den) < 1e-12, 1e-12, den)
    v = vb / den; w = vc / den
    P = A + ab * v[..., None] + ac * w[..., None]
    # bolgeler
    def sel(m, X):
        nonlocal P
        P = np.where(m[..., None], X, P)
    m = (d1 <= 0) & (d2 <= 0); sel(m, np.broadcast_to(A, P.shape))
    m = (d3 >= 0) & (d4 <= d3); sel(m, np.broadcast_to(B, P.shape))
    m = (d6 >= 0) & (d5 <= d6); sel(m, np.broadcast_to(C, P.shape))
    t = d1 / np.where(np.abs(d1 - d3) < 1e-12, 1e-12, d1 - d3)
    m = (vc <= 0) & (d1 >= 0) & (d3 <= 0); sel(m, A + ab * t[..., None])
    t = d2 / np.where(np.abs(d2 - d6) < 1e-12, 1e-12, d2 - d6)
    m = (vb <= 0) & (d2 >= 0) & (d6 <= 0); sel(m, A + ac * t[..., None])
    t = (d4 - d3) / np.where(np.abs((d4 - d3) + (d5 - d6)) < 1e-12, 1e-12, (d4 - d3) + (d5 - d6))
    m = (va <= 0) & ((d4 - d3) >= 0) & ((d5 - d6) >= 0); sel(m, B + (C - B) * t[..., None])
    return np.linalg.norm(Q - P, axis=-1)


def dik_yollar(S, E, ara=()):
    """S -> E arasi dik acili aday yollar: eksen sirasi permutasyonlari (+ ara noktalar listesi)"""
    S = np.asarray(S, float); E = np.asarray(E, float); out = []
    for perm in itertools.permutations(range(3)):
        Q = [S.copy()]; c = S.copy()
        for ax in perm:
            if abs(E[ax] - c[ax]) > 1e-6: c = c.copy(); c[ax] = E[ax]; Q.append(c)
        out.append(Q)
    return out


def sade(Q):
    Q = [np.asarray(q, float) for q in Q]; R = [Q[0]]
    for q in Q[1:]:
        if np.linalg.norm(q - R[-1]) < 1e-6: continue
        if len(R) >= 2:
            d1 = R[-1] - R[-2]; d2 = q - R[-1]
            if np.linalg.norm(np.cross(d1, d2)) < 1e-6 and d1 @ d2 > 0: R[-1] = q; continue
        R.append(q)
    return R


class Bolge:
    """bölge içindeki yüzeylerden uzaklık alanı (EDT, h mm voksel) — hızlı yol denetimi"""
    def __init__(s, EN, lo, hi, h=2.0):
        from scipy.ndimage import distance_transform_edt
        s.lo = np.asarray(lo, float); s.h = h
        n = np.ceil((np.asarray(hi, float) - s.lo) / h).astype(int) + 1; s.n = n
        occ = np.zeros(n, bool)
        ii = EN.aday(s.lo - 2, np.asarray(hi, float) + 2)
        A, B, C = EN.A[ii], EN.B[ii], EN.C[ii]
        L = np.maximum(np.maximum(np.linalg.norm(B - A, axis=1), np.linalg.norm(C - A, axis=1)), np.linalg.norm(C - B, axis=1))
        for k in np.unique(np.minimum(np.ceil(L / (h * 0.5)).astype(int), 4000)):
            m = np.minimum(np.ceil(L / (h * 0.5)).astype(int), 4000) == k
            k = max(int(k), 1)
            u, v = np.meshgrid(np.arange(k + 1), np.arange(k + 1)); sel = (u + v) <= k
            u = u[sel] / k; v = v[sel] / k
            for j in range(0, m.sum(), max(1, 2_000_000 // len(u))):
                a = A[m][j:j + max(1, 2_000_000 // len(u))]; b = B[m][j:j + max(1, 2_000_000 // len(u))]; c = C[m][j:j + max(1, 2_000_000 // len(u))]
                Q = a[:, None] + (b - a)[:, None] * u[None, :, None] + (c - a)[:, None] * v[None, :, None]
                g = np.round((Q.reshape(-1, 3) - s.lo) / h).astype(int)
                ok = np.all((g >= 0) & (g < n), 1); g = g[ok]
                occ[g[:, 0], g[:, 1], g[:, 2]] = True
        s.D = distance_transform_edt(~occ) * h

    def mesafe(s, Q):
        g = np.round((np.asarray(Q, float) - s.lo) / s.h).astype(int)
        ok = np.all((g >= 0) & (g < s.n), 1)
        d = np.zeros(len(g)); d[ok] = s.D[g[ok, 0], g[ok, 1], g[ok, 2]]; return d

    def seg_ok(s, a, b, r, pay=0.5):
        L = np.linalg.norm(b - a); n = max(2, int(L) + 1)
        Q = a[None] + (b - a)[None] * np.linspace(0, 1, n)[:, None]
        return float(s.mesafe(Q).min()) >= r + pay + s.h * 0.75


def izgara_yol(B, S1, E1, r, adim=3):
    """B (Bolge, ince EDT) üzerinde kaba ızgara (adim voksel) en kısa yol + dik açılı sadeleştirme. S1/E1 serbest olmalı."""
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import dijkstra
    D = B.D[::adim, ::adim, ::adim]; h = B.h * adim
    free = D >= r + 0.5 + B.h * 0.75
    n = D.shape; N = free.size
    idx = np.arange(N).reshape(n)
    rows, cols = [], []
    for ax in range(3):
        a = [slice(None)] * 3; b = [slice(None)] * 3; a[ax] = slice(0, -1); b[ax] = slice(1, None)
        m = free[tuple(a)] & free[tuple(b)]
        rows.append(idx[tuple(a)][m]); cols.append(idx[tuple(b)][m])
    rr = np.concatenate(rows); cc = np.concatenate(cols)
    Gm = coo_matrix((np.ones(len(rr)), (rr, cc)), shape=(N, N)).tocsr()
    def hucre(p):
        g = np.round((np.asarray(p, float) - B.lo) / h).astype(int); g = np.clip(g, 0, np.array(n) - 1)
        if free[tuple(g)]: return g
        # en yakın serbest hücre
        f = np.argwhere(free); return f[np.argmin(np.abs(f - g).sum(1))]
    gs = hucre(S1); ge = hucre(E1)
    dist, pred = dijkstra(Gm, directed=False, indices=idx[tuple(gs)], return_predecessors=True)
    t = idx[tuple(ge)]
    if not np.isfinite(dist[t]): return None
    yolh = [t]
    while yolh[-1] != idx[tuple(gs)]: yolh.append(pred[yolh[-1]])
    yolh = yolh[::-1]
    P = [B.lo + np.array(np.unravel_index(i, n)) * h for i in yolh]
    P = [np.asarray(S1, float)] + P + [np.asarray(E1, float)]
    # dik açılı açgözlü sadeleştirme
    def L_ok(a, b):
        for perm in ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)):
            Q = [a]; c = a.copy()
            for ax in perm:
                if abs(b[ax] - c[ax]) > 1e-6: c = c.copy(); c[ax] = b[ax]; Q.append(c)
            if all(B.seg_ok(q0, q1, r) for q0, q1 in zip(Q[:-1], Q[1:])): return Q
        return None
    out = [P[0]]; i = 0
    while i < len(P) - 1:
        for j in range(len(P) - 1, i, -1):
            Q = L_ok(P[i], P[j])
            if Q is not None or j == i + 1:
                if Q is None: Q = [P[i], P[j]]
                out += Q[1:]; i = j; break
    return sade(out)


def halka(p0, p1, ri, ro, n=24):
    """eksenli halka (rakor / kablo rakoru): iç delikli kapalı ağ"""
    p0 = np.asarray(p0, float); p1 = np.asarray(p1, float); a = p1 - p0; a /= np.linalg.norm(a)
    e = np.cross(a, [1, 0, 0]) if abs(a[0]) < 0.9 else np.cross(a, [0, 1, 0]); e /= np.linalg.norm(e); f = np.cross(a, e)
    th = np.linspace(0, 2 * np.pi, n, endpoint=False); out = []
    C = [np.cos(t) * e + np.sin(t) * f for t in th]
    for i in range(n):
        j = (i + 1) % n
        for r, s in ((ro, 1), (ri, -1)):
            A0, B0, A1, B1 = p0 + C[i] * r, p0 + C[j] * r, p1 + C[i] * r, p1 + C[j] * r
            out += [(A0, B0, B1), (A0, B1, A1)] if s > 0 else [(A0, B1, B0), (A0, A1, B1)]
        for P, s in ((p0, -1), (p1, 1)):
            Ao, Bo, Ai, Bi = P + C[i] * ro, P + C[j] * ro, P + C[i] * ri, P + C[j] * ri
            out += [(Ao, Bi, Bo), (Ao, Ai, Bi)] if s < 0 else [(Ao, Bo, Bi), (Ao, Bi, Ai)]
    return np.array(out)
