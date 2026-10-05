# -*- coding: utf-8 -*-
"""Duzlem gecis cozucu: kablolar dikey (y) inerken her biri kendi y seviyesinde yatay L (x-z) ile p -> q konumuna gecer.
Kesisme kurallari (kapsul, bosluk G):
  - k ve j seviyeleri |yk-yj| < rk+rj+G ise L yollari 2B'de ayrik olmali
  - k'nin L'si yk'da: j daha asagida gececekse (yj<yk) p_j'de dikey, yukarida gectiyse q_j'de dikey -> nokta-yol mesafesi
  - iki dikey: yk>yj araliginda k q_k'da, j p_j'de -> |q_k-p_j| yeterli
Rastgele arama: sira (permutasyon) + yon (x-once / z-once) + seviye (sira boyunca asagi dogru, en az gerekli aralik)."""
import numpy as np, random, itertools
G = 0.4


def seg_pt(a, b, c):
    d = b - a; L2 = d @ d
    t = 0.0 if L2 < 1e-12 else np.clip(((c - a) @ d) / L2, 0, 1)
    return np.linalg.norm(a + t * d - c)


def seg_seg(a, b, c, d):
    # 2B eksen hizali parcalar: ornekleyerek yeterli (kisa)
    best = min(seg_pt(a, b, c), seg_pt(a, b, d), seg_pt(c, d, a), seg_pt(c, d, b))
    # kesisme (dik kesisen iki parca)
    def ccw(p, q, r): return (r[1] - p[1]) * (q[0] - p[0]) - (q[1] - p[1]) * (r[0] - p[0])
    if ccw(a, b, c) * ccw(a, b, d) < 0 and ccw(c, d, a) * ccw(c, d, b) < 0: return 0.0
    return best


def L_yol(p, q, yon):
    """2B (x,z) L yolu: yon 0 = once x, 1 = once z"""
    m = np.array([q[0], p[1]]) if yon == 0 else np.array([p[0], q[1]])
    return [(p, m), (m, q)]


def yol_mesafe(Y1, Y2):
    return min(seg_seg(a, b, c, d) for a, b in Y1 for c, d in Y2)


def nokta_mesafe(Y, c):
    return min(seg_pt(a, b, c) for a, b in Y)


def coz(ad, p, q, r, ylo, yhi, alan=None, deneme=20000, tohum=1, sabit_yon=None):
    """ad: liste; p,q: {ad: (x,z)}; r: {ad}; seviyeler y in [ylo+r, yhi-r]; alan(yol, y, r) -> bool icinde mi.
    Donus: {ad: (y, yon)} ya da None"""
    rnd = random.Random(tohum)
    P = {a: np.array(p[a], float) for a in ad}; Q = {a: np.array(q[a], float) for a in ad}
    n = len(ad)
    # dikey-dikey on kontrol: q_k vs p_j (k once gecerse) -> izinli sira iliskisi
    izin = {}
    for k in ad:
        for j in ad:
            if k == j: continue
            izin[(k, j)] = np.linalg.norm(Q[k] - P[j]) >= r[k] + r[j] + G   # k j'den once (yukarida) gecebilir mi
    en_iyi = None
    for it in range(deneme):
        # rastgele topolojik-ish sira: izin grafiginde gecerli
        kalan = list(ad); sira = []
        ok = True
        while kalan:
            aday = [k for k in kalan if all(izin[(k, j)] for j in kalan if j != k)]
            if not aday: ok = False; break
            k = rnd.choice(aday); sira.append(k); kalan.remove(k)
        if not ok: return None
        yon = {a: (sabit_yon[a] if sabit_yon and a in sabit_yon else rnd.randint(0, 1)) for a in ad}
        Y = {a: L_yol(P[a], Q[a], yon[a]) for a in ad}
        # seviyeleri yukaridan asagi yerlestir: her kablo, oncekilerle (yukaridakiler) cakismayan en yuksek y
        sev = {}
        bad = False
        for i, k in enumerate(sira):
            if alan and not alan(Y[k], r[k]): bad = True; break
            # k'nin L'si yk'da: asagidakiler (sira'da sonra) p'de dikey; yukaridakiler q'da
            for j in sira[i + 1:]:
                if nokta_mesafe(Y[k], P[j]) < r[k] + r[j] + G: bad = True; break
            if bad: break
            for j in sira[:i]:
                if nokta_mesafe(Y[k], Q[j]) < r[k] + r[j] + G: bad = True; break
            if bad: break
            ust = yhi - r[k]
            for j in sira[:i]:
                if yol_mesafe(Y[k], Y[j]) < r[k] + r[j] + G:
                    ust = min(ust, sev[j] - r[k] - r[j] - G)
            if ust < ylo + r[k]: bad = True; break
            sev[k] = ust
        if bad: continue
        alt = min(sev[k] - r[k] for k in ad)
        if en_iyi is None or alt > en_iyi[0]:
            en_iyi = (alt, {k: (sev[k], yon[k]) for k in ad}, list(sira))
    return en_iyi
