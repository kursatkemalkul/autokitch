# -*- coding: utf-8 -*-
"""m8t2 · GLB yazıcı: eski ana hat kablo üçgenlerini sil (eski eksenlere göre sınıflandır) + yeni yollardan gönyeli (miter) tek parça tüp
+ UF3 oluk (fan üstü kanalın ön bölümü tam yükseklik) + kesit geçiş plakaları yeniden.
python m8t2_yaz.py giris.glb yollar.json cikis.glb [--oluk]"""
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import m8kit as MK
import m8t2_rota_eski as RE


def miter_tup(P, r, n=16):
    """dik açılı yol için gönye birleşimli tek kapalı tüp (n,3,3)"""
    P = np.asarray(P, float)
    D = np.diff(P, axis=0); Ls = np.linalg.norm(D, axis=1); D = D / Ls[:, None]
    d0 = D[0]; a = np.array([1.0, 0, 0]) if abs(d0[0]) < 0.9 else np.array([0, 1.0, 0])
    u = np.cross(d0, a); u /= np.linalg.norm(u); v = np.cross(d0, u)
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    rings = []
    C = P[0] + r * (np.cos(th)[:, None] * u + np.sin(th)[:, None] * v); rings.append(C)
    for i in range(1, len(P) - 1):
        din, dout = D[i - 1], D[i]
        m = din + dout; m /= np.linalg.norm(m)
        Cc = P[i] + r * (np.cos(th)[:, None] * u + np.sin(th)[:, None] * v)
        t = -((Cc - P[i]) @ m) / (din @ m)
        rings.append(Cc + t[:, None] * din)
        # çerçeveyi dout'a taşı (Rodrigues)
        k = np.cross(din, dout); s = np.linalg.norm(k); c = din @ dout
        if s > 1e-9:
            k /= s; ang = np.arctan2(s, c)
            def rot(w): return w * np.cos(ang) + np.cross(k, w) * np.sin(ang) + k * (k @ w) * (1 - np.cos(ang))
            u = rot(u); v = rot(v)
    C = P[-1] + r * (np.cos(th)[:, None] * u + np.sin(th)[:, None] * v); rings.append(C)
    out = []
    for A, B in zip(rings[:-1], rings[1:]):
        for j in range(n):
            j2 = (j + 1) % n
            out.append((A[j], A[j2], B[j2])); out.append((A[j], B[j2], B[j]))
    for R_, cen, sg in ((rings[0], P[0], -1), (rings[-1], P[-1], 1)):
        for j in range(n):
            j2 = (j + 1) % n
            out.append((cen, R_[j2], R_[j]) if sg < 0 else (cen, R_[j], R_[j2]))
    T = np.array(out)
    # dışa bakan normal düzelt (yan yüzler: eksenden uzağa)
    nrm = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0])
    cen = T.mean(1)
    # en yakın eksen noktası
    best = np.full(len(T), np.inf); vec = np.zeros_like(cen)
    for a_, b_ in zip(P[:-1], P[1:]):
        d = b_ - a_; L2 = d @ d; t = np.clip(((cen - a_) @ d) / L2, 0, 1); q = a_ + t[:, None] * d
        dist = np.linalg.norm(cen - q, axis=1); m_ = dist < best; best[m_] = dist[m_]; vec[m_] = (cen - q)[m_]
    ters = (nrm * vec).sum(1) < 0
    T[ters] = T[ters][:, [0, 2, 1]]
    return T


def eski_sinifla(G, dugum, eski, tol=0.3):
    """dugum prim'lerindeki üçgenleri eski kablo eksenlerine göre sınıflandır -> {ad: [(prim, idx)]}"""
    out = {}
    for p in G.dprims(dugum):
        if p.get("gizli"): continue
        X = p["X"]; T = p["T"]; vis = G.gorunur(p)
        best = np.full(len(X), np.inf); bad = np.full(len(X), -1)
        D = {}; SD = {}
        for j, (ad, (r, P)) in enumerate(eski.items()):
            P = np.asarray(P, float); dm = np.full(len(X), np.inf)
            for i, (a, b) in enumerate(zip(P[:-1], P[1:])):
                d = b - a; L = np.linalg.norm(d); d /= L
                a2 = a - d * (r if i > 0 else 0.0); b2 = b + d * (r if i < len(P) - 2 else 0.0)
                dd = b2 - a2; L2 = dd @ dd
                lo = np.minimum(a2, b2) - r - 1; hi = np.maximum(a2, b2) + r + 1
                m = np.all((X >= lo) & (X <= hi), axis=1)
                if not m.any(): continue
                t = np.clip(((X[m] - a2) @ dd) / L2, 0, 1); q = a2 + t[:, None] * dd
                dist = np.linalg.norm(X[m] - q, axis=1)
                dm[m] = np.minimum(dm[m], dist)
            D[ad] = np.abs(dm - r); SD[ad] = dm - r
        ads = list(D); M = np.stack([D[a] for a in ads], 1)          # (nv, nk)  |d - r|
        SG = np.stack([SD[a] for a in ads], 1)                          # (nv, nk)  d - r (işaretli)
        tri = M[T]                                                     # (nt, 3, nk)
        med = np.median(tri, axis=1)                                   # (nt, nk)
        k = np.argmin(med, 1); v = med[np.arange(len(T)), k]
        icte = np.max(SG.min(1)[T], axis=1) < tol                      # tüm köşeler bir eski tüpün yüzeyinde / içinde
        ok = vis & ((v < tol) | icte)
        for j, ad in enumerate(ads):
            idx = np.where(ok & (k == j))[0]
            if len(idx): out.setdefault(ad, []).append((p, idx))
    return out


def kutu(lo, hi):
    return MK.kutu_ucgen(lo, hi)


def oluk(G, rapor):
    """UF3 (fan üstü) kanal + iki geçiş plakası: eski üçgenleri sil, yeni kutularla kur"""
    p = [q for q in G.dprims("ELK_ANA_HAT__kanal") if not q.get("gizli")][0]
    P = p["X"][p["T"]]; lo = P.min(1); hi = P.max(1); vis = G.gorunur(p)
    def sec(x0, x1):
        return vis & (lo[:, 0] >= x0 - 0.01) & (hi[:, 0] <= x1 + 0.01) & (lo[:, 1] >= 2104.9) & (hi[:, 1] <= 2166.6)
    m_kanal = sec(2575.85, 2919.25)
    m_p1 = sec(2919.25, 2920.75); m_p2 = sec(2574.25, 2575.75)
    m = m_kanal | m_p1 | m_p2
    # kapak (y >= 2166.5) dahil değil: hi_y <= 2166.6 ve lo_y >= 2104.9 -> kapak (2166.5..2168) hariç
    n_sil = G.sil(p, m)
    ex = p["pr"].get("extras", {}); kat, mek = 6, 26
    B = []
    X0, X1 = 2575.85, 2919.25
    B.append(((X0, 2138.0, -826.0), (X1, 2166.5, -824.5)))           # arka duvar
    B.append(((X0, 2138.0, -824.5), (X1, 2139.5, -787.6)))           # üst taban (fan üstü)
    B.append(((X0, 2105.0, -787.6), (X1, 2139.5, -786.1)))           # oluk arka duvarı
    B.append(((X0, 2105.0, -786.1), (X1, 2106.5, -656.0)))           # oluk tabanı
    B.append(((X0, 2106.5, -657.5), (X1, 2166.5, -656.0)))           # ön duvar
    for xa, xb, zr in ((2919.25, 2920.75, -749.5), (2574.25, 2575.75, -691.5)):
        B.append(((xa, 2105.0, -826.0), (xb, 2106.5, -656.0)))          # alt şerit
        B.append(((xa, 2106.5, -826.0), (xb, 2139.5, -786.1)))          # sol (oluk arkası + fan altı)
        B.append(((xa, 2106.5, zr), (xb, 2166.5, -656.0)))              # sağ
        B.append(((xa, 2139.5, -826.0), (xb, 2166.5, -824.5)))          # arka şerit (üst pencere)
    n = 0
    for a, b in B:
        n += G.ucgen_ekle("ELK_ANA_HAT__kanal", kutu(a, b), kat=kat, mek=mek)
    rapor.append("UF3 oluk: %d eski üçgen silindi, %d kutu (%d üçgen) eklendi" % (n_sil, len(B), n))


if __name__ == "__main__":
    gir, yj, cik = sys.argv[1:4]
    G = MK.Glb(gir)
    Yo = json.load(open(yj))
    O, _ = RE.eski()
    rapor = []
    for dugum, mal in (("ELK_ANA_HAT__kablo", "kablo"), ("ELK_ANA_HAT__kablo_veri", "kablo_veri")):
        eski = {a: (r, p) for a, (r, m, p) in O.items() if m == mal}
        S = eski_sinifla(G, dugum, eski)
        ns = 0
        for ad, lst in S.items():
            for p, idx in lst:
                mm = np.zeros(len(p["T"]), bool); mm[idx] = True; ns += G.sil(p, mm)
        rapor.append("%s: %d eski üçgen silindi (%s)" % (dugum, ns, ", ".join("%s %d" % (a, sum(len(i) for _, i in l)) for a, l in S.items())))
        kat = 6 if mal == "kablo" else 7
        for ad, d in Yo.items():
            if d["mal"] != mal: continue
            Tn = miter_tup(np.array(d["P"]), d["r"], n=16)
            G.ucgen_ekle(dugum, Tn, kat=kat, mek=26)
        rapor.append("%s: %d yeni kablo" % (dugum, sum(1 for d in Yo.values() if d["mal"] == mal)))
    if "--oluk" in sys.argv: oluk(G, rapor)
    # K / E iniş ağzındaki (37 x 57) eski delik artığı taban parçaları (kablonun eski yolu) -> sil
    for p in G.dprims("ELK_ANA_HAT__kanal"):
        if p.get("gizli"): continue
        tl, kut = G.komp(p); n_ = 0
        for ci, (lo, hi, n) in kut.items():
            for xa, xb in ((4281.5, 4318.5), (5081.5, 5118.5)):
                if n <= 40 and lo[0] >= xa - 0.1 and hi[0] <= xb + 0.1 and lo[1] >= 2124.9 and hi[1] <= 2126.6 and lo[2] >= -824.6 and hi[2] <= -767.4:
                    n_ += G.sil(p, tl == ci)
        if n_: rapor.append("K/E iniş ağzı artık taban parçaları silindi: %d üçgen" % n_)
    G.kaydet(cik)
    print("\n".join(rapor))
