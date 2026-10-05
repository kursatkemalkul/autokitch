# -*- coding: utf-8 -*-
"""m8: m7kit uzantisi — denetim bileseni (govde_denetim_dogru.bilesenler, 'DUGUM[no]') -> ucgen haritasi; bileseni tasi / sil / kopyala.
Donuk (rotation) dugumlerde dunya<->yerel donusum. Tasima = eski ucgenleri sil + yeni konumda ayni etiketle (kat/mek/kpk) yeniden ekle."""
import os, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, S)
from m7kit import Glb as _G7
import govde_denetim_dogru as G


def _R(nd):
    q = nd.get("rotation", [0, 0, 0, 1]); x, y, z, w = q
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


class Glb(_G7):
    def __init__(s, yol):
        _G7.__init__(s, yol)
        s._bc = {}
        # tam dunya donusumu (hiyerarsi + TRS): glbkit X = (yerel + t)*1000 kabul eder; dunya = W * yerel
        J = s.J; W = {}
        def trs(nd):
            M = np.eye(4)
            if "matrix" in nd: return np.array(nd["matrix"], float).reshape(4, 4).T
            M[:3, :3] = _R(nd) * np.array(nd.get("scale", [1, 1, 1]), float)[None, :]; M[:3, 3] = nd.get("translation", [0, 0, 0]); return M
        def gez(i, P):
            W[i] = P @ trs(J["nodes"][i])
            for c in J["nodes"][i].get("children", []): gez(c, W[i])
        for r in J["scenes"][J.get("scene", 0)]["nodes"]: gez(r, np.eye(4))
        idx = {id(nd): i for i, nd in enumerate(J["nodes"])}
        for p in s.prims:
            M = W.get(idx[id(p["nd"])], np.eye(4)); p["W"] = M
            sc = abs(np.linalg.det(M[:3, :3])) ** (1 / 3)
            if sc < 0.01: p["gizli"] = True
            yalin = np.allclose(M[:3, :3], np.eye(3)) and np.allclose(M[:3, 3], p["t"])
            if not yalin:
                loc = p["X"] / 1000.0 - p["t"]
                p["X"] = (loc @ M[:3, :3].T + M[:3, 3]) * 1000.0
                p["donuk"] = True
            p["R"] = M[:3, :3]

    def dprims(s, dugum):
        return [p for p in s.prims if p["name"] == dugum]

    def bilesen(s, dugum, no=None, lo=None, hi=None, tol=0.3):
        """denetimdeki DUGUM[no] bileseni -> [(prim, ucgen idx dizisi)], lo, hi. no yerine lo/hi ile de bulunur."""
        key = dugum
        if key not in s._bc:
            PP, MAP = [], []
            for p in s.dprims(dugum):
                if p.get("gizli"): continue
                if p["pr"].get("mode", 4) != 4: continue
                P = p["X"][p["T"]]
                ar = np.linalg.norm(np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]), axis=1)
                ii = np.where(ar > 1e-9)[0]
                PP.append(P[ii]); MAP += [(id(p), i) for i in ii]
            P = np.concatenate(PP)
            # bilesenler 'iyi' suzgecini tekrar et, sonra P satirlarini MAP'e eslemek icin P baytlari
            bb = G.bilesenler(dugum, P)
            kk = {}
            for i in range(len(P)): kk.setdefault(P[i].tobytes(), []).append(i)
            pid = {id(p): p for p in s.dprims(dugum)}
            out = []
            for b in bb:
                idx = []
                for r in b.P:
                    l = kk.get(r.tobytes())
                    if l: idx.append(l[0])
                tri = [MAP[i] for i in idx]
                d = {}
                for pp, t in tri: d.setdefault(pp, []).append(t)
                out.append(dict(no=b.no, lo=b.lo, hi=b.hi, kapali=b.kapali, parca=[(pid[k], np.array(sorted(set(v)))) for k, v in d.items()]))
            s._bc[key] = out
        L = s._bc[key]
        if no is not None and lo is None: return L[no]
        c = [b for b in L if np.all(np.abs(b["lo"] - lo) < tol) and np.all(np.abs(b["hi"] - hi) < tol)]
        if len(c) != 1: raise KeyError("%s bilesen bulunamadi/coklu (%d) lo %s hi %s" % (dugum, len(c), lo, hi))
        return c[0]

    def _etiketler(s, p, tri):
        ex = p["pr"].get("extras", {})
        kat = s.etiket_of(p, tri, "kat") if ex.get("kat") else None
        mek = s.etiket_of(p, tri, "mek") if ex.get("mek") else None
        kpk = bool(s.kpk_maske(p)[tri]) if ex.get("kpk") else False
        return kat, mek, kpk

    def _ekle_dunya(s, p, Pw, kat, mek, kpk):
        """Pw: (n,3,3) dunya mm -> prim'e ekle (donuk dugumde yerele cevir; m7kit X'i (yerel+t)*1000 sanar)"""
        Q = Pw.reshape(-1, 3)
        if p.get("donuk"):
            M = p["W"]; loc = (Q / 1000.0 - M[:3, 3]) @ np.linalg.inv(M[:3, :3]).T
            Q = (loc + p["t"]) * 1000.0
        T = np.arange(len(Q)).reshape(-1, 3)
        return s.ekle_etiket(p, Q, T, kat=kat, mek=mek, kpk=kpk)

    def donustur(s, b, f):
        """b bileseninin ucgenlerini sil, f(Pw (n,3,3)) -> yeni Pw ile ayni etiketlerle yeniden ekle"""
        n = 0
        for p, tri in b["parca"]:
            # etiket gruplari
            gr = {}
            for t in tri: gr.setdefault(s._etiketler(p, t), []).append(t)
            Pw = p["X"][p["T"]]
            m = np.zeros(len(p["T"]), bool); m[tri] = True
            for (kat, mek, kpk), tt in gr.items():
                Q = f(Pw[np.array(tt)].copy())
                if Q is not None and len(Q): n += s._ekle_dunya(p, Q, kat, mek, kpk)
            s.sil(p, m)
        return n

    def tasi_b(s, b, d):
        d = np.asarray(d, float); return s.donustur(b, lambda P: P + d)

    def sil_b(s, b):
        return s.donustur(b, lambda P: None)

    def kopya_b(s, b, d, kat=None, mek=None):
        d = np.asarray(d, float); n = 0
        for p, tri in b["parca"]:
            gr = {}
            for t in tri: gr.setdefault(s._etiketler(p, t), []).append(t)
            Pw = p["X"][p["T"]]
            for (k0, m0, kp), tt in gr.items():
                n += s._ekle_dunya(p, Pw[np.array(tt)] + d, kat if kat is not None else k0, mek if mek is not None else m0, kp)
        return n

    def ucgen_ekle(s, dugum, Pw, kat=None, mek=None, kpk=False, ornek=None):
        """dugum'un ilk primine yeni ucgenler (dunya mm). etiket verilmezse 'ornek' (lo,hi) bilesenin etiketi"""
        p = [q for q in s.dprims(dugum) if not q.get("gizli")][0]
        return s._ekle_dunya(p, np.asarray(Pw, float), kat, mek, kpk)


def kutu_ucgen(lo, hi):
    """eksen hizali kutu, disa bakan 12 ucgen (n,3,3)"""
    x0, y0, z0 = lo; x1, y1, z1 = hi
    v = np.array([[x0, y0, z0], [x1, y0, z0], [x1, y1, z0], [x0, y1, z0], [x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1]], float)
    f = [(0, 2, 1), (0, 3, 2), (4, 5, 6), (4, 6, 7), (0, 1, 5), (0, 5, 4), (2, 3, 7), (2, 7, 6), (1, 2, 6), (1, 6, 5), (0, 4, 7), (0, 7, 3)]
    return v[np.array(f)]


def silindir_ucgen(p0, p1, r, n=16):
    p0 = np.asarray(p0, float); p1 = np.asarray(p1, float); a = p1 - p0; L = np.linalg.norm(a); a /= L
    u = np.cross(a, [1, 0, 0]) if abs(a[0]) < 0.9 else np.cross(a, [0, 1, 0]); u /= np.linalg.norm(u); w = np.cross(a, u)
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    C = [np.cos(t) * u * r + np.sin(t) * w * r for t in th]
    out = []
    for i in range(n):
        j = (i + 1) % n
        A0, B0, A1, B1 = p0 + C[i], p0 + C[j], p1 + C[i], p1 + C[j]
        out += [(A0, B0, B1), (A0, B1, A1), (p0, B0, A0), (p1, A1, B1)]
    return np.array(out)


def _kaydet(s, yol):
    for p in s.prims:
        if p.get("donuk"):
            M = p["W"]; loc = (p["X"] / 1000.0 - M[:3, 3]) @ np.linalg.inv(M[:3, :3]).T
            p["X"] = (loc + p["t"]) * 1000.0; p["donuk"] = False
    _G7.kaydet(s, yol)


Glb.kaydet = _kaydet
_eski_donustur = Glb.donustur


def _donustur(s, b, f):
    r = _eski_donustur(s, b, f)
    for p, _ in b["parca"]: s._bc.pop(p["name"], None)
    return r


Glb.donustur = _donustur


# ------------------------------------------------------------------ geometri yardimcilari
def _sh(poly, ax, val, keep_less):
    out = []
    n = len(poly)
    for i in range(n):
        A, B = poly[i], poly[(i + 1) % n]
        ia = (A[ax] <= val) if keep_less else (A[ax] >= val)
        ib = (B[ax] <= val) if keep_less else (B[ax] >= val)
        if ia: out.append(A)
        if ia != ib:
            t = (val - A[ax]) / (B[ax] - A[ax]); out.append(A + t * (B - A))
    return out


def _fan(poly):
    return [(poly[0], poly[i], poly[i + 1]) for i in range(1, len(poly) - 1)]


def delik_ucgenler(P, eksen, duzlemler, u0, u1, w0, w1, tol=0.02):
    """P (n,3,3): duzlemlerden birinde yatan ucgenlerden dikdortgen [u0,u1]x[w0,w1] (u,w = diger iki eksen, artan sira) cikarilir.
    Donus: yeni P + delik duvarlari (duzlem cifti arasinda)."""
    a = eksen; u, w = [i for i in range(3) if i != a]
    out = []
    for tri in P:
        on = any(np.all(np.abs(tri[:, a] - v) < tol) for v in duzlemler)
        lo = tri.min(0); hi = tri.max(0)
        if not on or hi[u] <= u0 or lo[u] >= u1 or hi[w] <= w0 or lo[w] >= w1:
            out.append(tri); continue
        poly = [tri[0], tri[1], tri[2]]
        parts = [_sh(poly, u, u0, True), _sh(poly, u, u1, False)]
        mid = _sh(_sh(poly, u, u0, False), u, u1, True)
        if len(mid) >= 3:
            parts += [_sh(mid, w, w0, True), _sh(mid, w, w1, False)]
        for pp in parts:
            if len(pp) >= 3:
                for t in _fan(pp):
                    T = np.array(t)
                    if np.linalg.norm(np.cross(T[1] - T[0], T[2] - T[0])) > 1e-6: out.append(T)
    out = list(out)
    if len(duzlemler) == 2:
        v0, v1 = sorted(duzlemler)
        def pt(uu, ww, vv):
            q = np.zeros(3); q[a] = vv; q[u] = uu; q[w] = ww; return q
        # duvarlar, normal deligin icine
        kos = [(u0, w0), (u1, w0), (u1, w1), (u0, w1)]
        cu, cw = (u0 + u1) / 2, (w0 + w1) / 2
        for i in range(4):
            (ua, wa), (ub, wb) = kos[i], kos[(i + 1) % 4]
            Q = [pt(ua, wa, v0), pt(ub, wb, v0), pt(ub, wb, v1), pt(ua, wa, v1)]
            for t in ((Q[0], Q[1], Q[2]), (Q[0], Q[2], Q[3])):
                T = np.array(t); nrm = np.cross(T[1] - T[0], T[2] - T[0]); c = T.mean(0)
                hedef = pt(cu, cw, c[a]) - c
                if nrm @ hedef < 0: T = T[[0, 2, 1]]
                out.append(T)
    return np.array(out)


def kenetle(P, eksen, mn=None, mx=None):
    P = P.copy()
    if mn is not None: P[..., eksen] = np.maximum(P[..., eksen], mn)
    if mx is not None: P[..., eksen] = np.minimum(P[..., eksen], mx)
    return P


def esle(P, eksen, eski, yeni, tol=0.02, kosul=None):
    P = P.copy(); V = P.reshape(-1, 3)
    m = np.abs(V[:, eksen] - eski) < tol
    if kosul is not None: m &= kosul(V)
    V[m, eksen] = yeni; return V.reshape(P.shape)


def radyal(P, eksen, merkez, d, rmax=None, rmin=None, olcek=None):
    """eksen etrafinda (merkez = diger iki eksendeki nokta) r<=rmax kose noktalarini d kadar disa (ya da olcek ile) it"""
    P = P.copy(); V = P.reshape(-1, 3); u, w = [i for i in range(3) if i != eksen]
    du = V[:, u] - merkez[0]; dw = V[:, w] - merkez[1]; r = np.hypot(du, dw)
    m = np.ones(len(V), bool)
    if rmax is not None: m &= r <= rmax
    if rmin is not None: m &= r >= rmin
    m &= r > 1e-6
    k = np.where(m, (r + d) / np.maximum(r, 1e-9), 1.0) if olcek is None else np.where(m, olcek, 1.0)
    V[:, u] = merkez[0] + du * k; V[:, w] = merkez[1] + dw * k
    return V.reshape(P.shape)



# ------------------------------------------------------------------ kablo / yuzey yardimcilari
def kure_ucgen(c, r, n=8, m=6):
    c = np.asarray(c, float); out = []
    th = np.linspace(0, np.pi, m + 1); ph = np.linspace(0, 2 * np.pi, n + 1)
    def p(i, j): return c + r * np.array([np.sin(th[i]) * np.cos(ph[j]), np.cos(th[i]), np.sin(th[i]) * np.sin(ph[j])])
    for i in range(m):
        for j in range(n):
            a, b, cc, d = p(i, j), p(i + 1, j), p(i + 1, j + 1), p(i, j + 1)
            if i > 0: out.append((a, cc, b) if False else (a, b, cc))
            if i < m - 1: out.append((a, cc, d))
    T = np.array(out)
    # disa bakan yon
    n_ = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0]); k = (T.mean(1) - c)
    ters = (n_ * k).sum(1) < 0; T[ters] = T[ters][:, [0, 2, 1]]
    return T


def tup(noktalar, r, n=12):
    """dik acili kablo/hortum: noktalar arasi silindir + kose kuresi"""
    Q = [np.asarray(q, float) for q in noktalar]; out = []
    for a, b in zip(Q[:-1], Q[1:]):
        if np.linalg.norm(b - a) > 1e-6: out.append(silindir_ucgen(a, b, r, n))
    for q in Q[1:-1]: out.append(kure_ucgen(q, r, n, 6))
    return np.concatenate(out)


def _bul_nokta(s, dugum, q, tol=0.5):
    """noktayi (kutusu) iceren en kucuk bilesen"""
    s.bilesen(dugum, 0); q = np.asarray(q, float); best = None
    for b in s._bc[dugum]:
        if np.all(b["lo"] - tol <= q) and np.all(q <= b["hi"] + tol):
            v = np.prod(b["hi"] - b["lo"] + 0.1)
            if best is None or v < best[0]: best = (v, b)
    if best is None: raise KeyError("%s nokta %s" % (dugum, q))
    return best[1]


Glb.bul_nokta = _bul_nokta


def _etiket_b(s, b):
    p, t = b["parca"][0]; return s._etiketler(p, int(t[0]))


Glb.etiket_b = _etiket_b


def _ekle_dugum(s, dugum, Pw, ornek=None, kat=None, mek=None, kpk=False):
    """dugume (ilk gorunur prim) yeni ucgenler; etiket ornek bilesenden"""
    if ornek is not None: kat, mek, kpk = s.etiket_b(ornek)
    p = [q for q in s.dprims(dugum) if not q.get("gizli")][0]
    return s._ekle_dunya(p, np.asarray(Pw, float), kat, mek, kpk)


Glb.ekle_dugum = _ekle_dugum


class Yuzey:
    """m8_onbellek benzeri tum model ucgenleri (dunya mm) uzerinde isin: en yakin yuzey"""
    def __init__(s, g, haric=()):
        A = []; N = []; s.adlar = []
        for p in g.prims:
            if p.get("gizli") or any(p["name"].startswith(h) for h in haric): continue
            P = p["X"][p["T"]]
            ar = np.linalg.norm(np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]), axis=1)
            A.append(P[ar > 1e-6]); s.adlar.append(p["name"]); N.append(np.full(int((ar > 1e-6).sum()), len(s.adlar) - 1))
        s.P = np.concatenate(A); s.N = np.concatenate(N); s.lo = s.P.min(1); s.hi = s.P.max(1)

    def isin(s, o, d, maxd=150.0, atla=None, haric_ad=None):
        o = np.asarray(o, float); d = np.asarray(d, float); d = d / np.linalg.norm(d)
        e = o + d * maxd; blo = np.minimum(o, e) - 1; bhi = np.maximum(o, e) + 1
        m = np.all(s.hi >= blo, 1) & np.all(s.lo <= bhi, 1)
        if atla is not None: m &= ~atla(s.P)
        if haric_ad is not None:
            import re as _re
            bad = np.array([bool(_re.search(haric_ad, a)) for a in s.adlar]); m &= ~bad[s.N]
        P = s.P[m]
        if not len(P): return None
        v0, v1, v2 = P[:, 0], P[:, 1], P[:, 2]; e1 = v1 - v0; e2 = v2 - v0
        h = np.cross(d, e2); a = (e1 * h).sum(1); ok = np.abs(a) > 1e-12
        f = np.where(ok, 1.0 / np.where(ok, a, 1), 0); sv = o - v0; u = f * (sv * h).sum(1)
        q = np.cross(sv, e1); v = f * (q @ d); t = f * (e2 * q).sum(1)
        hit = ok & (u >= 0) & (v >= 0) & (u + v <= 1) & (t > 1e-6) & (t < maxd)
        return float(t[hit].min()) if hit.any() else None



# ------------------------------------------------------------------ etiket / temas yardimcilari
def _kpk_yaz(s, b, deger=True):
    for p, tri in b["parca"]:
        m = s.kpk_maske(p); m[np.asarray(tri)] = deger
        idx = np.where(m)[0]; runs = []
        if len(idx):
            br = np.where(np.diff(idx) > 1)[0]; st = np.r_[idx[0], idx[br + 1]]; en = np.r_[idx[br], idx[-1]]
            for a, e in zip(st, en): runs += [int(a) * 3, int(e - a + 1) * 3]
        ex = p["pr"].setdefault("extras", {})
        if runs: ex["kpk"] = runs
        elif "kpk" in ex: del ex["kpk"]
    return sum(len(t) for _, t in b["parca"])


Glb.kpk_yaz = _kpk_yaz
YAPI_DISI = r"kablo|__hava|hortum|rakor|__conta|__on_seffaf"


def bosluk(g, YS, lo, hi, dugum, maxd=60.0, n=3, yapi=False, haric_eksen=None):
    """kutunun 6 yuzunden (n x n ornek) disa isin: her yon icin en kucuk carpma -> [(t, ax, sg)] kucukten buyuge"""
    icinde = lambda P: np.all((P.mean(1) >= lo - 0.3) & (P.mean(1) <= hi + 0.3), axis=1)
    R = []
    for ax in range(3):
        if ax == haric_eksen: continue
        u, w = [i for i in range(3) if i != ax]
        for sg in (-1, 1):
            d = np.zeros(3); d[ax] = sg; best = None
            for fu in np.linspace(0.15, 0.85, n):
                for fw in np.linspace(0.15, 0.85, n):
                    o = np.zeros(3); o[ax] = hi[ax] if sg > 0 else lo[ax]
                    o[u] = lo[u] + fu * (hi[u] - lo[u]); o[w] = lo[w] + fw * (hi[w] - lo[w])
                    t = YS.isin(o, d, maxd, atla=icinde, haric_ad=(YAPI_DISI + "|" if yapi else "") + "^" + dugum + "$")
                    if t is not None and (best is None or t < best): best = t
            if best is not None: R.append((best, ax, sg))
    return sorted(R)


def _mek_yaz(s, b, deger):
    """bilesenin ucgenlerine mek etiketi (3'lu [etiket, baslangic, sayi] listesi yeniden kurulur)"""
    for p, tri in b["parca"]:
        ex = p["pr"].setdefault("extras", {}); L = ex.get("mek") or []
        n = len(p["T"]); a = np.full(n, -1, int)
        for k in range(0, len(L) - 2, 3): a[L[k + 1] // 3:(L[k + 1] + L[k + 2]) // 3] = L[k]
        a[np.asarray(tri)] = deger
        out = []; i = 0
        while i < n:
            j = i
            while j + 1 < n and a[j + 1] == a[i]: j += 1
            if a[i] >= 0: out += [int(a[i]), i * 3, (j - i + 1) * 3]
            i = j + 1
        ex["mek"] = out
    return True


Glb.mek_yaz = _mek_yaz
