# -*- coding: utf-8 -*-
"""B fitil denetimi · python b_fitil_denetim.py model.glb
 (a) fitil tabanı (z 24) ↔ ön çerçeve (z 23–24) temas oranı · taban halkası 0,25 mm ızgarada, çerçeve = dış çerçeve − bütün açıklıklar (b_govde_yeni)
 (b) fitil + kapak üçgenleri ↔ GLB'deki bütün diğer üçgenler: ayırıcı eksen (SAT) testi, 0,01 mm altı örtüşme = TEMAS (çakışma değil)
 (c) strok süpürmesi: fitil izdüşümü × z 24…47,3+s ve kapak izdüşümü × z 39…79+s kutusu ↔ birimin hareketli parçaları dışındaki bütün üçgenler
 (d) komşu fitiller arası en küçük boşluk"""
import sys
import numpy as np
import glb_oku
import b_govde_yeni as BG

EPS = 0.01
J, D = glb_oku.yukle(sys.argv[1])
UN = [n.split("__")[0] for n in D if n.startswith("CEK_") and n.endswith("__on_seffaf__CEKMECE")] + ["B_DEPO"]


def yeni(u):
    if u == "B_DEPO":
        Xc, Tc = D["B_DEPO__conta__CEKMECE"]; F = Xc[Tc]
        Xs, Ts = D["B_DEPO__sac__CEKMECE"]; Xp, Tp = D["B_DEPO__pu__CEKMECE"]
        K = np.concatenate([Xs[Ts[108:]], Xp[Tp]])
        return F, K, ["B_DEPO__conta__CEKMECE", "B_DEPO__pu__CEKMECE", "B_DEPO__sac__CEKMECE"]
    X, T = D[u + "__on_seffaf__CEKMECE"]; P = X[T]
    f = P[:, :, 2].max(1) <= 39.0 + 1e-6
    f |= (P[:, :, 2].min(1) >= 39.0 - 1e-6) & (P[:, :, 2].max(1) <= 47.31) & ~((np.abs(P[:, :, 2] - 39.0) < 1e-6).all(1))
    # kapak/fitil ayrımı: fitil = bağlı bileşen z 24'e inen → basitçe kapak üçgenleri z ≥ 39 ve kanal içi değil: bileşenle ayır
    from scipy.sparse.csgraph import connected_components
    from scipy.sparse import coo_matrix
    key = np.round(X, 3); uu, inv = np.unique(key, axis=0, return_inverse=True); TT = inv.ravel()[T]; n = len(uu)
    r = np.concatenate([TT[:, 0], TT[:, 1]]); c = np.concatenate([TT[:, 1], TT[:, 2]])
    _, lab = connected_components(coo_matrix((np.ones(len(r)), (r, c)), shape=(n, n)), directed=False)
    tl = lab[TT[:, 0]]; fl = {l for l in np.unique(tl) if P[tl == l][:, :, 2].min() < 30}
    m = np.isin(tl, list(fl))
    return P[m], P[~m], [u + "__on_seffaf__CEKMECE"]


# ---------------------------------------------------------------- SAT
def sat(A, B):
    """A, B (m,3,3) eş üçgen çiftleri → kesişiyor mu (örtüşme > EPS her eksende)"""
    eA = A[:, [1, 2, 0]] - A; eB = B[:, [1, 2, 0]] - B
    ax = [np.cross(eA[:, 0], eA[:, 1]), np.cross(eB[:, 0], eB[:, 1])] + [np.cross(eA[:, i], eB[:, j]) for i in range(3) for j in range(3)]
    kes = np.ones(len(A), bool)
    for a in ax:
        L = np.linalg.norm(a, axis=1); ok = L > 1e-9; a = a / np.maximum(L, 1e-12)[:, None]
        pa = np.einsum("mkd,md->mk", A, a); pb = np.einsum("mkd,md->mk", B, a)
        ayr = (pa.max(1) <= pb.min(1) + EPS) | (pb.max(1) <= pa.min(1) + EPS)
        kes &= ~(ayr & ok)
    return kes


def kutu_tri(B0, B1, P):
    """AABB (B0,B1) ↔ üçgenler P (n,3,3) SAT, EPS içe çekilmiş kutu"""
    c = (B0 + B1) / 2; h = (B1 - B0) / 2 - EPS; Q = P - c
    kes = np.all((Q.min(1) < h) & (Q.max(1) > -h), axis=1)
    e = Q[:, [1, 2, 0]] - Q; nrm = np.cross(e[:, 0], e[:, 1])
    ax = [nrm] + [np.cross(np.eye(3)[i][None, :].repeat(len(Q), 0), e[:, j]) for i in range(3) for j in range(3)]
    for a in ax:
        L = np.linalg.norm(a, axis=1); ok = L > 1e-9
        p = np.einsum("nkd,nd->nk", Q, a); r = np.abs(a) @ h
        kes &= ~(ok & ((p.min(1) >= r) | (p.max(1) <= -r)))
    return kes


def ciftler(A, B):
    """bbox örtüşen üçgen çiftleri (indis)"""
    a0, a1 = A.min(1), A.max(1); b0, b1 = B.min(1), B.max(1)
    I, Jx = [], []
    for s in range(0, len(A), 256):
        o = np.all((a0[s:s + 256, None] < b1[None] - EPS) & (b0[None] < a1[s:s + 256, None] - EPS), axis=2)
        i, j = np.nonzero(o); I.append(i + s); Jx.append(j)
    return np.concatenate(I), np.concatenate(Jx)


# ---------------------------------------------------------------- (a) çerçeve bölgesi (2D)
ACK = [(a, b, c, d) for _k, a, b, c, d in BG.ACIKLIK] + [BG.DEPO_ACIK, BG.SERVIS_ACIK, (BG.T0, 4338.5, 728.0, 729.0)]


def cercevede(x, y):
    ic = (x > BG.XDi) & (x < BG.XDs) & (y > BG.YDi) & (y < BG.YDs)
    for a, b, c, d in ACK: ic &= ~((x > a) & (x < b) & (y > c) & (y < d))
    return ic


hata = 0
print("B FİTİL DENETİMİ · %d birim" % len(UN))
print("  %-16s %-9s %-10s %-22s %s" % ("birim", "temas", "çakışma", "strok (fitil · kapak)", "fitil taban halkası"))
RING = {}
statik_ad = [n for n in D]
for u in UN:
    F, K, kendi = yeni(u)
    # taban halkası (z 24 yüzü)
    tb = F[np.all(np.abs(F[:, :, 2] - 24.0) < 1e-4, axis=1)].reshape(-1, 3)
    x0, x1, y0, y1 = tb[:, 0].min(), tb[:, 0].max(), tb[:, 1].min(), tb[:, 1].max()
    w = float(np.unique(np.round(tb[:, 0], 3))[1] - x0); RING[u] = (x0, x1, y0, y1)
    g = 0.25
    xs = np.arange(x0 + g / 2, x1, g); ys = np.arange(y0 + g / 2, y1, g)
    Xg, Yg = np.meshgrid(xs, ys, indexing="ij")
    hal = ~((Xg > x0 + w) & (Xg < x1 - w) & (Yg > y0 + w) & (Yg < y1 - w))
    oran = cercevede(Xg[hal], Yg[hal]).mean()
    # (b) çakışma
    yeni_tri = np.concatenate([F, K]); nk = 0; bulgu = []
    for n, (X, T) in D.items():
        if n in kendi: continue
        P = X[T]
        if not len(P): continue
        lo, hi = P.reshape(-1, 3).min(0), P.reshape(-1, 3).max(0)
        if np.any(lo > yeni_tri.reshape(-1, 3).max(0)) or np.any(hi < yeni_tri.reshape(-1, 3).min(0)): continue
        i, j = ciftler(yeni_tri, P)
        if len(i):
            k = sat(yeni_tri[i], P[j]).sum()
            if k: nk += k; bulgu.append("%s %d" % (n, k))
    # (c) strok
    st = 450.0 if u == "B_DEPO" else 700.0
    hare = [n for n in D if n.startswith(u + "__") and "CEKMECE" in n]
    kb = []; rob = set()
    for ad, Q, z0, z1 in (("fitil", F, 24.0, 47.3), ("kapak", K, 39.0, 79.0)):
        q = Q.reshape(-1, 3); B0 = np.array([q[:, 0].min(), q[:, 1].min(), z0]); B1 = np.array([q[:, 0].max(), q[:, 1].max(), z1 + st])
        c = 0
        for n, (X, T) in D.items():
            if n in hare: continue
            P = X[T]
            if not len(P): continue
            pl, ph = P.min(1), P.max(1)
            m = np.all((pl < B1) & (ph > B0), axis=1)
            if m.any():
                k = kutu_tri(B0, B1, P[m]).sum()
                if k and n.startswith("ROBOT_"): rob.add(n.split("__")[0])
                elif k: c += k; bulgu.append("strok-%s %s %d" % (ad, n, k))
        kb.append(c)
    ok = oran > 0.9999 and nk == 0 and sum(kb) == 0
    hata += (nk > 0) + (sum(kb) > 0)
    rb = ("  [önde robot hacmi: %s — fitilden bağımsız, kapak izdüşümü aynı]" % ",".join(sorted(rob))) if rob else ""
    print("  %-16s %6.1f %%  %-10s %-22s %.1f–%.1f / %.1f–%.1f (taban %.0f)%s%s" % (u, 100 * oran, "YOK" if nk == 0 else "%d ÜÇGEN" % nk,
          "TEMİZ" if sum(kb) == 0 else "%d / %d" % tuple(kb), x0, x1, y0, y1, w, "" if not bulgu else "  ← " + "; ".join(bulgu[:6]), rb))
# (d) komşu fitil boşlukları
eb = 1e9; ebc = None
ks = list(RING)
for i in range(len(ks)):
    for j in range(i + 1, len(ks)):
        a, b = RING[ks[i]], RING[ks[j]]
        dx = max(b[0] - a[1], a[0] - b[1], 0.0); dy = max(b[2] - a[3], a[2] - b[3], 0.0)
        if dx == 0 and dy == 0: d = -1.0
        else: d = max(dx, dy) if (dx == 0 or dy == 0) else float(np.hypot(dx, dy))
        if d < eb: eb, ebc = d, (ks[i], ks[j])
print("  (d) komşu fitiller arası en küçük boşluk %.1f mm (%s ↔ %s) %s" % (eb, ebc[0], ebc[1], "TEMİZ" if eb >= 1.0 else "BULGU"))
hata += eb < 1.0
print("B FİTİL: %s (çakışma/strok/boşluk) · temas oranları yukarıda" % ("TEMİZ" if not hata else "%d BULGU" % hata))
