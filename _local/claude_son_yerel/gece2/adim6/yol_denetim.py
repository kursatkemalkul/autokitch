# -*- coding: utf-8 -*-
"""MONTAJ YOL ÇAKIŞMA DENETİMİ (4 Eki 2026) — g6_montaj.py hareket modeliyle birebir.
Her parça çifti için (en az biri hareket ederken, ikisi de görünürken) bağıl öteleme yolu ≤ 5 mm adımlarla örneklenir; ardışık örnekler
arası SÜREKLİ çarpışma (CCD) üçgen düzeyinde denetlenir:
  (1) A köşesi → öteleme doğrusu B üçgenini deler mi   (2) B köşesi → ters öteleme A üçgenini deler mi
  (3) A kenarının taradığı paralelkenar B kenarını keser mi
Kenar / sınır temasları (≤ 0,1 mm) ve yüzeye paralel kayma sayılmaz. OTURMA: çarpma noktası o hareketin dinlenme konumuna ≤ 1,0 mm ise
sayılmaz (son konumdaki temas). Kapak dönüşleri (ROT) ≤ 2° adımlarla poz denetimi (üçgen-üçgen, ± 0,3 mm düzlem payı).
Kaynak / silikon / PU (yerinde büyüyen 'k' parçalar) hareketli sayılmaz; büyüme bitince engel olur."""
import numpy as np
import numba as nb

ADIM = 0.005        # m, örnek aralığı
OTURMA = 0.0010     # m, dinlenme konumuna bu kadar yakın çarpma = oturma teması
SINIR = 0.00075     # m, üçgen sınırı / kenar ucu payı (≤ 0,75 mm sıyırma = model toleransı, sayılmaz)


def e(u):
    u = min(max(u, 0.0), 1.0); return u * u * (3 - 2 * u)


def uu(t, h):
    return 1.0 if t >= h[1] else (0.0 if t <= h[0] else (t - h[0]) / (h[1] - h[0]))


def ofs(H, t):
    o = np.zeros(3)
    for h in H:
        k = 1 - e(uu(t, h)); o[0] += h[2] * k; o[1] += h[3] * k; o[2] += h[4] * k
    return o


def aci(Rl, t):
    a = 0.0; px = pz = 0.0
    for r in Rl: a += r[2] * e(uu(t, r)); px = r[3]; pz = r[4]
    return a, px, pz


# ------------------------------------------------------------------ numba çekirdekleri
@nb.njit(cache=True, fastmath=False)
def _seg_tri(p, d, a, b, c, mar):
    """p + λd (λ∈[0,1]) üçgen abc'yi içten (sınır payı mar, metrik) delerse λ, yoksa -1"""
    e1 = b - a; e2 = c - a
    h = np.cross(d, e2); det = np.dot(e1, h)
    n = np.cross(e1, e2); nn = np.sqrt(np.dot(n, n)); dl = np.sqrt(np.dot(d, d))
    if nn < 1e-14 or dl < 1e-12: return -1.0
    if abs(det) < 1e-6 * nn * dl: return -1.0          # paralel (kayma)
    f = 1.0 / det; s = p - a; u = f * np.dot(s, h)
    q = np.cross(s, e1); v = f * np.dot(d, q); w = 1 - u - v
    lam = f * np.dot(e2, q)
    if lam <= 1e-9 or lam >= 1 - 1e-9: return -1.0
    # metrik sınır payı: barisentrik × (karşı kenara yükseklik)
    la = np.sqrt(np.dot(c - b, c - b)); lb = np.sqrt(np.dot(e2, e2)); lc = np.sqrt(np.dot(e1, e1))
    if w * nn / max(la, 1e-12) <= mar: return -1.0
    if u * nn / max(lb, 1e-12) <= mar: return -1.0
    if v * nn / max(lc, 1e-12) <= mar: return -1.0
    return lam


@nb.njit(cache=True)
def _kenar_kenar(e0, e1, v, f0, f1, mar):
    """e0 + u(e1-e0) + λ v = f0 + s(f1-f0) ; u,s,λ ∈ iç → λ"""
    E = e1 - e0; Fv = f1 - f0
    # u E + λ v - s F = f0 - e0
    M = np.empty((3, 3)); M[:, 0] = E; M[:, 1] = v; M[:, 2] = -Fv
    det = np.linalg.det(M)
    le = np.sqrt(np.dot(E, E)); lv = np.sqrt(np.dot(v, v)); lf = np.sqrt(np.dot(Fv, Fv))
    if le < 1e-9 or lv < 1e-12 or lf < 1e-9: return -1.0
    if abs(det) < 1e-6 * le * lv * lf: return -1.0
    x = np.linalg.solve(M, f0 - e0)
    u, lam, s = x[0], x[1], x[2]
    if lam <= 1e-9 or lam >= 1 - 1e-9: return -1.0
    if u * le <= mar or (1 - u) * le <= mar: return -1.0
    if s * lf <= mar or (1 - s) * lf <= mar: return -1.0
    return lam


@nb.njit(cache=True)
def _cift_test(A, B, i, j, v, mar, best):
    a0 = A[i, 0]; a1 = A[i, 1]; a2 = A[i, 2]; b0 = B[j, 0]; b1 = B[j, 1]; b2 = B[j, 2]
    for q in range(3):
        l = _seg_tri(A[i, q], v, b0, b1, b2, mar)
        if l > 0 and l < best: best = l
        l = _seg_tri(B[j, q], -v, a0, a1, a2, mar)
        if l > 0 and l < best: best = l
    for q in range(3):
        ea = A[i, q]; eb = A[i, (q + 1) % 3]
        for r in range(3):
            l = _kenar_kenar(ea, eb, v, B[j, r], B[j, (r + 1) % 3], mar)
            if l > 0 and l < best: best = l
    return best


@nb.njit(cache=True, parallel=True)
def ccd(A, B, v, mar):
    """A (n,3,3) başlangıç pozunda, v kadar ötelenir; B (m,3,3) sabit. dönüş: her A üçgeni için en küçük λ (yoksa 2).
    kaba eleme: B kutuları x-min'e göre sıralı; dar olanlar (x genişliği ≤ W) ikili aramayla, genişler doğrudan."""
    n = A.shape[0]; m = B.shape[0]
    out = np.full(n, 2.0)
    bmin = np.empty((m, 3)); bmax = np.empty((m, 3))
    for j in range(m):
        for k in range(3):
            bmin[j, k] = min(B[j, 0, k], B[j, 1, k], B[j, 2, k]); bmax[j, k] = max(B[j, 0, k], B[j, 1, k], B[j, 2, k])
    W = 0.02
    dar = np.where(bmax[:, 0] - bmin[:, 0] <= W)[0]; gen = np.where(bmax[:, 0] - bmin[:, 0] > W)[0]
    sira = dar[np.argsort(bmin[dar, 0])]; xs = bmin[sira, 0]
    for i in nb.prange(n):
        amin = np.empty(3); amax = np.empty(3)
        for k in range(3):
            lo = min(A[i, 0, k], A[i, 1, k], A[i, 2, k]); hi = max(A[i, 0, k], A[i, 1, k], A[i, 2, k])
            amin[k] = min(lo, lo + v[k]); amax[k] = max(hi, hi + v[k])
        best = 2.0
        s0 = np.searchsorted(xs, amin[0] - W); s1 = np.searchsorted(xs, amax[0], side='right')
        for q in range(s0, s1):
            j = sira[q]
            if bmax[j, 0] < amin[0] or bmin[j, 1] > amax[1] or bmax[j, 1] < amin[1] or bmin[j, 2] > amax[2] or bmax[j, 2] < amin[2]: continue
            best = _cift_test(A, B, i, j, v, mar, best)
        for q in range(gen.shape[0]):
            j = gen[q]
            if bmin[j, 0] > amax[0] or bmax[j, 0] < amin[0] or bmin[j, 1] > amax[1] or bmax[j, 1] < amin[1] or bmin[j, 2] > amax[2] or bmax[j, 2] < amin[2]: continue
            best = _cift_test(A, B, i, j, v, mar, best)
        out[i] = best
    return out


@nb.njit(cache=True)
def _tt(a0, a1, a2, b0, b1, b2, eps):
    """üçgen-üçgen gerçek kesişme (Möller, düzlem payı eps: temas / eş düzlem sayılmaz)"""
    n2 = np.cross(b1 - b0, b2 - b0); l2 = np.sqrt(np.dot(n2, n2))
    if l2 < 1e-14: return False
    n2 /= l2; d0 = np.dot(a0 - b0, n2); d1 = np.dot(a1 - b0, n2); d2 = np.dot(a2 - b0, n2)
    if (d0 > -eps and d1 > -eps and d2 > -eps) or (d0 < eps and d1 < eps and d2 < eps): return False
    n1 = np.cross(a1 - a0, a2 - a0); l1 = np.sqrt(np.dot(n1, n1))
    if l1 < 1e-14: return False
    n1 /= l1; g0 = np.dot(b0 - a0, n1); g1 = np.dot(b1 - a0, n1); g2 = np.dot(b2 - a0, n1)
    if (g0 > -eps and g1 > -eps and g2 > -eps) or (g0 < eps and g1 < eps and g2 < eps): return False
    D = np.cross(n1, n2); ld = np.sqrt(np.dot(D, D))
    if ld < 1e-9: return False
    D /= ld

    def iv(p0, p1, p2, s0, s1, s2):
        P = (np.dot(p0, D), np.dot(p1, D), np.dot(p2, D)); S = (s0, s1, s2)
        lo = 1e30; hi = -1e30
        for i in range(3):
            j = (i + 1) % 3
            if (S[i] > 0) != (S[j] > 0) and S[i] != S[j]:
                x = P[i] + (P[j] - P[i]) * S[i] / (S[i] - S[j])
                lo = min(lo, x); hi = max(hi, x)
        return lo, hi
    l1_, h1_ = iv(a0, a1, a2, d0, d1, d2); l2_, h2_ = iv(b0, b1, b2, g0, g1, g2)
    return min(h1_, h2_) - max(l1_, l2_) > eps


@nb.njit(cache=True, parallel=True)
def poz_kesisim(A, B, eps):
    n = A.shape[0]; m = B.shape[0]; c = np.zeros(n, np.int64)
    for i in nb.prange(n):
        amin = np.empty(3); amax = np.empty(3)
        for k in range(3):
            amin[k] = min(A[i, 0, k], A[i, 1, k], A[i, 2, k]); amax[k] = max(A[i, 0, k], A[i, 1, k], A[i, 2, k])
        for j in range(m):
            ok = True
            for k in range(3):
                if min(B[j, 0, k], B[j, 1, k], B[j, 2, k]) > amax[k] or max(B[j, 0, k], B[j, 1, k], B[j, 2, k]) < amin[k]: ok = False
            if ok and _tt(A[i, 0], A[i, 1], A[i, 2], B[j, 0], B[j, 1], B[j, 2], eps): c[i] += 1
    return c


# ------------------------------------------------------------------ denetim
def ofsv(H, ts):
    """vektörel öteleme: ts (n,) → (n,3)"""
    o = np.zeros((len(ts), 3))
    for h in H:
        if abs(h[2]) + abs(h[3]) + abs(h[4]) < 1e-12: continue
        if h[1] - h[0] < 1e-9: u = (ts >= h[1]).astype(float)
        else: u = np.clip((ts - h[0]) / (h[1] - h[0]), 0, 1)
        k = 1 - u * u * (3 - 2 * u)
        o += k[:, None] * np.array(h[2:5])[None, :]
    return o


_VEKIL = {}


def _vekil(V, F, sinir=8000):
    """denetim vekili: çok üçgenli ağ (delikli / menfezli sac) yalnız denetim için ≤ sinir üçgene sadeleşir (hacim korunur)"""
    if len(F) <= sinir: return V[F]
    k = (len(F), float(V.sum()))
    if k in _VEKIL: return _VEKIL[k]
    import vtk
    from vtk.util.numpy_support import numpy_to_vtk, vtk_to_numpy, numpy_to_vtkIdTypeArray
    n = len(F); pts = vtk.vtkPoints(); pts.SetData(numpy_to_vtk(np.ascontiguousarray(V, np.float64), deep=1))
    cells = np.hstack([np.full((n, 1), 3, np.int64), F.astype(np.int64)]).ravel()
    ca = vtk.vtkCellArray(); ca.SetCells(n, numpy_to_vtkIdTypeArray(cells, deep=1))
    pd = vtk.vtkPolyData(); pd.SetPoints(pts); pd.SetPolys(ca)
    d = vtk.vtkQuadricDecimation(); d.SetInputData(pd); d.SetTargetReduction(1 - sinir / n); d.VolumePreservationOn(); d.Update()
    o = d.GetOutput(); V2 = vtk_to_numpy(o.GetPoints().GetData()).astype(np.float64)
    F2 = vtk_to_numpy(o.GetPolys().GetData()).reshape(-1, 4)[:, 1:]
    _VEKIL[k] = V2[F2]; return _VEKIL[k]


class Denetci:
    """önbellekli denetçi: haric = son konumda zaten geçme olan çiftler (vida → PEM, ürün → mat; oturma/geçme)"""
    def __init__(self, P, HAR, ROT, GOR, KAY, GIZLI, haric=()):
        self.P, self.HAR, self.ROT, self.GOR, self.KAY = P, HAR, ROT, GOR, KAY
        self.ads = [a for a in P if a not in GIZLI and a in GOR]
        self.T = {a: _vekil(P[a]['V'], np.asarray(P[a]['F'])) for a in self.ads}
        self.lo = {a: P[a]['V'].min(0) for a in self.ads}; self.hi = {a: P[a]['V'].max(0) for a in self.ads}
        self.haric = set(haric); self.ciftsay = 0
        self.idx = {a: i for i, a in enumerate(self.ads)}
        self.yenile()

    def gz(self, a):
        return self.HAR[a][0][1] if (a in self.KAY and self.HAR[a]) else self.GOR[a]

    def pw(self, a):
        if a in self.KAY: return []
        return [(h[0], h[1]) for h in self.HAR[a] if abs(h[2]) + abs(h[3]) + abs(h[4]) > 1e-9] + [(r[0], r[1]) for r in self.ROT.get(a, [])]

    def yk(self, a):
        w = self.pw(a); ts = sorted(set([x for x_ in w for x in x_]))
        if not ts: return self.lo[a], self.hi[a]
        O = ofsv(self.HAR[a], np.concatenate([np.linspace(min(ts), max(ts), 60), ts]))
        l, h = self.lo[a] + O.min(0), self.hi[a] + O.max(0)
        if self.ROT.get(a):
            r = float(np.linalg.norm(self.hi[a] - self.lo[a])) + 0.1; c = (self.lo[a] + self.hi[a]) / 2; l = np.minimum(l, c - r); h = np.maximum(h, c + r)
        return l, h

    def yenile(self, adlar=None):
        if adlar is None:
            Y_ = [self.yk(a) for a in self.ads]
            self.L = np.array([y[0] for y in Y_]); self.H = np.array([y[1] for y in Y_])
        else:
            for a in adlar:
                if a in self.idx: l, h = self.yk(a); self.L[self.idx[a]] = l; self.H[self.idx[a]] = h

    def cift(self, a, b, pencere=None):
        """a ↔ b: ilk içinden geçme (dict) ya da None"""
        HAR, ROT, lo, hi, T = self.HAR, self.ROT, self.lo, self.hi, self.T
        t_vis = max(self.gz(a), self.gz(b))
        ws = [(max(w0, t_vis), w1) for w0, w1 in self.pw(a) + self.pw(b) if w1 > t_vis + 1e-9]
        if pencere is not None: ws = [(max(w0, pencere[0]), min(w1, pencere[1])) for w0, w1 in ws if min(w1, pencere[1]) > max(w0, pencere[0]) + 1e-9]
        if not ws: return None
        ws.sort(); birl = []
        for w0, w1 in ws:
            if birl and w0 <= birl[-1][1] + 1e-9: birl[-1][1] = max(birl[-1][1], w1)
            else: birl.append([w0, w1])
        for w0, w1 in birl:
            if any(r[0] < w1 and r[1] > w0 for r in ROT.get(a, []) + ROT.get(b, [])):
                r_ = _rot_denetim(a, b, T, HAR, ROT, w0, w1, lo, hi)
                if r_: return r_
                continue
            grid = np.linspace(w0, w1, 241)
            R = ofsv(HAR[a], grid) - ofsv(HAR[b], grid)
            l2 = lo[a] + R.min(0); h2 = hi[a] + R.max(0)
            if np.any(l2 > hi[b] + 1e-4) or np.any(h2 < lo[b] - 1e-4): continue
            yol = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(R, axis=0), axis=1))])
            if yol[-1] < 1e-6: continue
            ns = max(1, int(np.ceil(yol[-1] / ADIM)))
            hedef = np.linspace(0, yol[-1], ns + 1)
            orn = np.array([np.interp(hedef, yol, R[:, k]) for k in range(3)]).T
            tor = np.interp(hedef, yol, grid)
            kir = [0]
            for k in range(1, ns):
                d1 = orn[k] - orn[kir[-1]]; d2 = orn[k + 1] - orn[k]
                n1, n2 = np.linalg.norm(d1), np.linalg.norm(d2)
                if n1 > 1e-9 and n2 > 1e-9 and np.dot(d1, d2) / (n1 * n2) < 0.99995: kir.append(k)
            kir.append(ns)
            self.ciftsay += 1
            Ab = T[a]; Bb = T[b]
            # dinlenme noktaları: bağıl hareketin durduğu örnekler (pencere sonu + aradaki duruşlar)
            dur = [R[-1]] + [R[k] for k in range(1, len(R) - 1) if np.linalg.norm(R[k + 1] - R[k - 1]) < 1e-7]
            dur = np.array(dur)
            for k0, k1 in zip(kir[:-1], kir[1:]):
                p0 = orn[k0]; v = orn[k1] - orn[k0]
                if np.linalg.norm(v) < 1e-9: continue
                A0 = Ab + p0
                amn = np.minimum(A0.min(1), (A0 + v).min(1)); amx = np.maximum(A0.max(1), (A0 + v).max(1))
                sa = np.all(amn <= hi[b] + 1e-4, 1) & np.all(amx >= lo[b] - 1e-4, 1)
                if not sa.any(): continue
                smn = amn[sa].min(0); smx = amx[sa].max(0)
                sb = np.all(Bb.min(1) <= smx + 1e-4, 1) & np.all(Bb.max(1) >= smn - 1e-4, 1)
                if not sb.any(): continue
                lam = ccd(np.ascontiguousarray(A0[sa]), np.ascontiguousarray(Bb[sb]), v.astype(np.float64), SINIR)
                m = lam < 1.5
                if not m.any(): continue
                pts = p0[None, :] + lam[m][:, None] * v[None, :]
                der = np.min(np.linalg.norm(pts[:, None, :] - dur[None, :, :], axis=2), axis=1)
                if der.max() > OTURMA:
                    kk = int(np.argmax(der)); lm = lam[m][kk]
                    tt = float(tor[k0] + lm * (tor[k1] - tor[k0]))
                    hareket = a if any(w0_ - 1e-9 <= tt <= w1_ + 1e-9 for w0_, w1_ in self.pw(a)) else b
                    return dict(a=a, b=b, t=round(tt, 2), w=[round(w0, 2), round(w1, 2)], derin=round(float(der.max()) * 1000, 1), yon='oteleme', hareket=hareket)
        return None

    def denetle(self, sadece=None, ilerleme=False):
        import time as _t; t0 = _t.time()
        self.ciftsay = 0; sonuc = []; bakildi = set()
        har = [a for a in self.ads if self.pw(a) and (sadece is None or a in sadece)]
        for n_, a in enumerate(har):
            if ilerleme and n_ % 100 == 0: print('  ilerleme %d/%d  %.0f s  çakışma %d' % (n_, len(har), _t.time() - t0, len(sonuc)), flush=True)
            ia = self.idx[a]
            aday = np.where(np.all(self.L <= self.H[ia] + 1e-4, 1) & np.all(self.H >= self.L[ia] - 1e-4, 1))[0]
            for jb in aday:
                b = self.ads[jb]
                if b == a: continue
                key = (a, b) if a < b else (b, a)
                if key in bakildi or key in self.haric: continue
                bakildi.add(key)
                r = self.cift(a, b)
                if r: sonuc.append(r)
        return sonuc


def denetle(P, HAR, ROT, GOR, KAY, GIZLI, sadece=None, haric=()):
    D = Denetci(P, HAR, ROT, GOR, KAY, GIZLI, haric)
    r = D.denetle(sadece, ilerleme=True)
    return r, D.ciftsay


def _rot_denetim(a, b, T, HAR, ROT, w0, w1, lo, hi):
    """kapak dönüşü: ≤ 2° / ≤ 5 mm poz örnekleri, üçgen-üçgen (± 0,3 mm); son pozda zaten kesişen çift sayılmaz"""
    def poz(x, t):
        Tm = T[x].copy(); o = ofs(HAR[x], t); an, px, pz = aci(ROT.get(x, []), t)
        if abs(an) > 1e-9:
            r = np.radians(an); cs, sn = np.cos(r), np.sin(r)
            dx = Tm[..., 0] - px; dz = Tm[..., 2] - pz
            X = px + cs * dx + sn * dz; Z = pz - sn * dx + cs * dz
            Tm[..., 0] = X; Tm[..., 2] = Z
        return Tm + o
    son = poz_kesisim(np.ascontiguousarray(poz(a, w1 + 1e3)), np.ascontiguousarray(poz(b, w1 + 1e3)), 3e-4).sum()
    if son: return None
    n = 120
    for t in np.linspace(w0, w1, n + 1)[1:-1]:
        A = poz(a, t); B = poz(b, t)
        if np.any(A.reshape(-1, 3).min(0) > B.reshape(-1, 3).max(0)) or np.any(A.reshape(-1, 3).max(0) < B.reshape(-1, 3).min(0)): continue
        c = poz_kesisim(np.ascontiguousarray(A), np.ascontiguousarray(B), 3e-4).sum()
        if c: return dict(a=a, b=b, t=round(float(t), 2), w=[round(w0, 2), round(w1, 2)], derin=-1, yon='donme')
    return None


def son_kesisim(P, ads, eps=3e-4):
    """son konumda gerçekten kesişen çiftler (düzlem payı eps; temas / eş düzlem sayılmaz) → {(a,b): kesişen üçgen sayısı}"""
    T = {a: P[a]['V'][np.asarray(P[a]['F'])] for a in ads}
    lo = np.array([P[a]['V'].min(0) for a in ads]); hi = np.array([P[a]['V'].max(0) for a in ads])
    out = {}
    for i, a in enumerate(ads):
        j = np.where(np.all(lo[i + 1:] <= hi[i] - eps, 1) & np.all(hi[i + 1:] >= lo[i] + eps, 1))[0] + i + 1
        for k in j:
            b = ads[k]
            A = T[a]; B = T[b]
            sa = np.all(A.min(1) <= hi[k], 1) & np.all(A.max(1) >= lo[k], 1)
            sb = np.all(B.min(1) <= hi[i], 1) & np.all(B.max(1) >= lo[i], 1)
            if not sa.any() or not sb.any(): continue
            c = int(poz_kesisim(np.ascontiguousarray(A[sa]), np.ascontiguousarray(B[sb]), eps).sum())
            if c: out[(a, b) if a < b else (b, a)] = c
    return out


def temas_denetim(P, HAR, GOR, KAY, GIZLI, tol=6e-4, turler=('sac', 'kapak', 'profil')):
    """her sac / profil yerine oturduğu anda en az bir YERİNDE parçaya (aynı hareket grubu hariç) ≤ tol değiyor mu.
    dönüş: {sac: (t_oturma, [temas edilen parçalar])} — liste boşsa HAVADA"""
    import trimesh, json as _j
    ads = [a for a in P if a not in GIZLI and a in GOR]
    son = {a: max([h[1] for h in HAR[a]] + [GOR[a]]) for a in ads}
    imza = {a: _j.dumps(HAR[a]) for a in ads}
    lo = {a: P[a]['V'].min(0) for a in ads}; hi = {a: P[a]['V'].max(0) for a in ads}
    TM = {}
    out = {}
    for s in ads:
        if P[s]['tur'] not in turler or s in KAY: continue
        tl = son[s]; tem = []
        for b in ads:
            if b == s or son[b] > tl + 1e-6 or imza[b] == imza[s]: continue
            if np.any(lo[b] > hi[s] + tol) or np.any(hi[b] < lo[s] - tol): continue
            if b not in TM: TM[b] = trimesh.Trimesh(P[b]['V'], np.asarray(P[b]['F']), process=False)
            if s not in TM: TM[s] = trimesh.Trimesh(P[s]['V'], np.asarray(P[s]['F']), process=False)
            ok = False
            for x, y in ((s, b), (b, s)):
                V = P[x]['V']; m = np.all(V >= lo[y] - tol, 1) & np.all(V <= hi[y] + tol, 1)
                if m.any():
                    _, d, _ = trimesh.proximity.closest_point(TM[y], V[m][:3000])
                    if d.min() <= tol: ok = True; break
            if ok: tem.append(b)
        out[s] = (tl, tem)
    return out
