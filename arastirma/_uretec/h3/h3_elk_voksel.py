# -*- coding: utf-8 -*-
"""HAT v3.2 · KABLO YOL BULUCU 2 (voksel A*) — dar bölmelerde (TOPPING kuru bölme · K · dolap arkası) h3_elk_rota'nın 1–4 köşeli adayları yetmediğinde:
bölgedeki bütün katıların YÜZEYLERİ (üçgenlenmiş) h mm ızgaraya işlenir, kablo yarıçapı + pay kadar şişirilir, S → T arası A* (dönüş cezalı →
az köşeli, eksenlere paralel yol) · sonuç köşe noktalarına indirilir · gerçek katı denetimi h3_elk_rota.temiz ile yapılır (yaklaşık ızgara güvenilmez)."""
import heapq, math
import numpy as np
from scipy import ndimage
import cadquery as cq
import h3_elk_ortak as EO
import h3_elk_rota as ER

_TESS = {}


def _uc(ad, s):
    if ad not in _TESS:
        P, T = None, None
        try:
            v, t = s.tessellate(0.4, 0.3)
            if len(t):
                P = np.array([(p.x, p.y, p.z) for p in v], dtype=float); T = np.array(t, dtype=int).reshape(-1, 3)
        except Exception:
            P = None
        if P is None:                                                         # yüz yüz (bozuk yüz atlanır)
            Ps, Ts, n0 = [], [], 0
            for f in s.Faces():
                try:
                    v, t = f.tessellate(0.4, 0.3)
                except Exception:
                    continue
                if not len(t): continue
                Ps.append(np.array([(p.x, p.y, p.z) for p in v], dtype=float)); Ts.append(np.array(t, dtype=int).reshape(-1, 3) + n0); n0 += len(v)
            P = np.vstack(Ps) if Ps else np.zeros((0, 3)); T = np.vstack(Ts) if Ts else np.zeros((0, 3), int)
        _TESS[ad] = (P, T)
    return _TESS[ad]


def _ornekle(P, T, h):
    """üçgen yüzeyinden ≤ h/2 aralıklı noktalar"""
    out = [P]
    for tri in T:
        a, b, c = P[tri[0]], P[tri[1]], P[tri[2]]
        L = max(np.linalg.norm(b - a), np.linalg.norm(c - a), np.linalg.norm(c - b))
        n = int(math.ceil(L / (h * 0.45)))
        if n <= 1:
            out.append(((a + b + c) / 3.0)[None, :]); continue
        i, j = np.meshgrid(np.arange(n + 1), np.arange(n + 1))
        m = (i + j) <= n
        u, v = i[m] / n, j[m] / n
        out.append(a[None, :] + u[:, None] * (b - a)[None, :] + v[:, None] * (c - a)[None, :])
    return np.vstack(out)


def bul(S, T, r, pay=1.0, h=4.0, marj=160.0, bolge=None, haric=(), ic_bos=(), yakin_w=1.2, w=1.8):
    """S, T dünya noktaları (S cihaz yüzünden itilmiş, T kanal/pano yüzünde) · bolge: (x0,x1,y0,y1,z0,z1) arama sınırı ·
    haric: engel sayılmayacak ad önekleri · ic_bos: tamamen serbest sayılacak kutular (rakor delikleri gibi) · döner (pts, sh) ya da (None, sebep)"""
    lo = np.minimum(S, T) - marj; hi = np.maximum(S, T) + marj
    if bolge is not None:
        lo = np.maximum(lo, [bolge[0], bolge[2], bolge[4]]); hi = np.minimum(hi, [bolge[1], bolge[3], bolge[5]])
    o = np.array(S, float) - h * np.floor((np.array(S, float) - lo) / h)          # S tam bir hücre merkezinde
    N = np.floor((hi - o) / h).astype(int) + 1
    if N.prod() > 9e6: return None, "bölge çok büyük %s" % N
    dolu = np.zeros(N, bool)
    q = (o[0] - h, o[0] + N[0] * h, o[1] - h, o[1] + N[1] * h, o[2] - h, o[2] + N[2] * h)
    kaynak = [(ad, s) for ad, s, sb in EO.dokum() if EO._ust(q, sb, 0.0)] + [("YENI|" + ad, s) for ad, s, sb in ER._EK if EO._ust(q, sb, 0.0)]
    for ad, s in kaynak:
        if haric and ad.startswith(haric): continue
        P, Tr = _uc(ad, s)
        if not len(P): continue
        X = _ornekle(P, Tr, h)
        I = np.floor((X - o) / h + 0.5).astype(int)
        a0 = np.maximum(I.min(axis=0) - 1, 0); a1 = np.minimum(I.max(axis=0) + 2, N)
        if np.any(a1 <= a0): continue
        m = np.all((I >= a0) & (I < a1), axis=1); J = I[m] - a0
        sub = np.zeros(a1 - a0, bool); sub[J[:, 0], J[:, 1], J[:, 2]] = True
        sub = ndimage.binary_fill_holes(sub)                          # katının içi (tek katı içinde kapalı boşluk) dolu
        dolu[a0[0]:a1[0], a0[1]:a1[1], a0[2]:a1[2]] |= sub
    taban = dolu.copy()
    k = int(math.ceil((r + pay) / h - 0.25))
    if k > 0:
        st = ndimage.generate_binary_structure(3, 1)
        dolu = ndimage.binary_dilation(dolu, structure=st, iterations=k)
    for b in ic_bos:
        i0 = np.clip(np.floor((np.array([b[0], b[2], b[4]]) - o) / h).astype(int), 0, N - 1)
        i1 = np.clip(np.ceil((np.array([b[1], b[3], b[5]]) - o) / h).astype(int), 0, N - 1)
        dolu[i0[0]:i1[0] + 1, i0[1]:i1[1] + 1, i0[2]:i1[2] + 1] = False
    for P_ in (S, T):                                                   # uçların çevresinde yalnız şişirmeyi kaldır (yüzey + iç dolu kalır)
        c = np.floor((np.array(P_) - o) / h + 0.5).astype(int); c0 = np.maximum(c - k - 1, 0); c1 = np.minimum(c + k + 2, N)
        dolu[c0[0]:c1[0], c0[1]:c1[1], c0[2]:c1[2]] = taban[c0[0]:c1[0], c0[1]:c1[1], c0[2]:c1[2]]
    s0 = tuple(np.floor((np.array(S) - o) / h + 0.5).astype(int))
    t0 = tuple(np.clip(np.floor((np.array(T) - o) / h + 0.5).astype(int), 0, N - 1))
    for c in (s0, t0): dolu[c] = False
    # yüzeye yakınlık: serbest hücrenin en yakın dolu hücreye uzaklığı (mm) · uzak hücre pahalı → kablo duvara / gövdeye yaslanır (kelepçelenir)
    uz = ndimage.distance_transform_edt(~dolu) * h
    ceza = np.minimum(uz, 60.0) / 60.0 * yakin_w
    # A* · durum (hücre, yön) · adım 1 + dönüş 6 + uzaklık cezası
    D = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    hs = lambda c: abs(c[0] - t0[0]) + abs(c[1] - t0[1]) + abs(c[2] - t0[2])
    acik = [(w * hs(s0), 0, s0, -1)]; best = {(s0, -1): 0}; geri = {}
    son = None; say = 0
    while acik:
        f, g, c, d = heapq.heappop(acik)
        if best.get((c, d), 1e18) < g: continue
        if c == t0: son = (c, d); break
        say += 1
        if say > 12000000: return None, "A* sınırı"
        for di, (dx, dy, dz) in enumerate(D):
            n = (c[0] + dx, c[1] + dy, c[2] + dz)
            if not (0 <= n[0] < N[0] and 0 <= n[1] < N[1] and 0 <= n[2] < N[2]) or dolu[n]: continue
            g2 = g + 1 + ceza[n] + (6 if (d != -1 and di != d) else 0)
            if g2 < best.get((n, di), 1e18):
                best[(n, di)] = g2; geri[(n, di)] = (c, d)
                heapq.heappush(acik, (g2 + w * hs(n), g2, n, di))
    if son is None: return None, "ızgarada yol yok"
    yol = [son[0]]; st_ = son
    while st_ in geri:
        st_ = geri[st_]; yol.append(st_[0])
    yol.reverse()
    W = [tuple(o + h * np.array(c)) for c in yol]
    # köşelere indir
    pts = [W[0]]
    for i in range(1, len(W) - 1):
        a, b, c = np.array(pts[-1]), np.array(W[i]), np.array(W[i + 1])
        if np.linalg.norm(np.cross(b - a, c - b)) > 1e-6: pts.append(W[i])
    pts.append(W[-1])
    pts[0] = tuple(S)
    # T'ye eksen eksen yaklaş (son hücre merkezi ↔ T farkı < h/2) · son parça T'nin yaklaşma yönünde kalsın
    son_p = list(pts[-1])
    for ax in range(3):
        if abs(son_p[ax] - T[ax]) > 1e-6:
            son_p[ax] = T[ax]; pts.append(tuple(son_p))
    q2 = [pts[0]]
    for p in pts[1:]:
        if math.dist(p, q2[-1]) > 0.05: q2.append(p)
    # ardışık aynı doğrultudaki noktaları birleştir
    q3 = [q2[0]]
    for i in range(1, len(q2) - 1):
        a, b, c = np.array(q3[-1]), np.array(q2[i]), np.array(q2[i + 1])
        if np.linalg.norm(np.cross(b - a, c - b)) > 1e-6: q3.append(q2[i])
    q3.append(q2[-1])
    return q3, None
