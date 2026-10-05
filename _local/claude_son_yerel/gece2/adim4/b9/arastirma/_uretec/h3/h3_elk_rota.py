# -*- coding: utf-8 -*-
"""HAT v3.2 · KABLO YOL BULUCU — cihaz ucu S → hedef T: eksenlere paralel (Manhattan) 1–4 köşeli adaylar, makine dökümü + yeni parçalara karşı GERÇEK katı
çakışması (kutu ön elemeli), en kısa temiz yol · uzun parçalara en yakın yüzeye P-kelepçe (≤ 250 mm aralık, yüzey ≤ 90 mm) · bulunamazsa rapor."""
import itertools, math
import cadquery as cq
import h3_elk_ortak as EO
from h3_elk_ortak import boru, kut

V = cq.Vector
_EK = []                                     # yeni parçalar (ad, şekil, kutu) — kablo ↔ kablo / kanal çakışması için


def ekli_ekle(ad, sh):
    b = sh.BoundingBox(); _EK.append((ad, sh, (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)))


def _engeller(bb, haric):
    for ad, s, sb in EO.dokum():
        if EO._ust(bb, sb) and not (haric and ad.startswith(haric)): yield ad, s
    for ad, s, sb in _EK:
        if EO._ust(bb, sb) and not (haric and ad.startswith(haric)): yield "YENI|" + ad, s


def temiz(sh, haric=(), esik=0.3):
    b = sh.BoundingBox(); bb = (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)
    for ad, s in _engeller(bb, haric):
        try: v = sh.intersect(s).Volume()
        except Exception: v = 1.0
        if v > esik: return False, ad
    return True, None


def _manhattan(S, T, ara):
    """S → T eksen sıralarıyla · ara: ek ara noktalar listesi (S'den önce itme)"""
    out = []
    for sira in itertools.permutations((0, 1, 2)):
        p = list(S); pts = [tuple(p)]
        for ax in sira:
            if abs(p[ax] - T[ax]) > 1e-6:
                p[ax] = T[ax]; pts.append(tuple(p))
        out.append(pts)
    return out


def bul(S, T, r, haric=(), itme=None, ek_ara=()):
    """itme: S'den önce cihaz yüzünden dışarı itme [(eksen, mesafe), …] denemeleri · döner (pts, sh) ya da (None, sebep)"""
    adaylar = []
    itmeler = [None] + list(itme or [])
    for it in itmeler:
        S2 = list(S); on = [tuple(S)]
        if it:
            ax, d = it; S2[ax] += d; on.append(tuple(S2))
        for m in _manhattan(tuple(S2), T, ()):
            pts = on + m[1:] if it else m
            adaylar.append(pts)
        for via in ek_ara:
            for m1 in _manhattan(tuple(S2), via, ()):
                for m2 in _manhattan(via, T, ()):
                    adaylar.append((on if it else [tuple(S)]) + m1[1:] + m2[1:])
    # tekrarlı noktaları ayıkla, uzunluğa göre sırala
    temizlenmis = []
    for pts in adaylar:
        q = [pts[0]]
        for p in pts[1:]:
            if math.dist(p, q[-1]) > 1e-6: q.append(p)
        if len(q) >= 2: temizlenmis.append(q)
    temizlenmis.sort(key=lambda q: (EO.uzunluk(q), len(q)))
    son = None
    for q in temizlenmis[:40]:
        ok = True
        for j_, (a_, b_) in enumerate(zip(q[:-1], q[1:])):          # parça parça (ince kutular → az aday) · sonuç önbellekte
            son_ = j_ == len(q) - 2; bas_ = j_ == 0                 # uçlar düz · iç köşelerde parça r kadar uzar (EO.boru ile aynı zarf)
            k_ = (tuple(round(v, 1) for v in a_), tuple(round(v, 1) for v in b_), r, son_, bas_)
            if k_ not in _ONB:
                seg = EO.sil_uzun(a_, b_, r, not bas_, not son_)
                _ONB[k_] = temiz(seg, haric)
            if not _ONB[k_][0]:
                ok = False; son = _ONB[k_][1]; break
        if ok: return q, boru(q, r)
    return None, son


_ONB = {}


def kelepce_yeri(p, eksen, r, maks=200.0, haric=()):
    """p noktasında kabloya dik 4 yönde en yakın engel yüzeyi (kutu yüzü) · döner (yüzey koordinatı, yön) ya da None"""
    ax = "xyz".index(eksen); en = None
    for bx in [i for i in range(3) if i != ax]:
        for sg in (+1, -1):
            # ışın kutusu: p'den ± bx yönünde maks
            lo = [p[i] - r for i in range(3)]; hi = [p[i] + r for i in range(3)]
            if sg > 0: lo[bx], hi[bx] = p[bx] + r, p[bx] + maks
            else: lo[bx], hi[bx] = p[bx] - maks, p[bx] - r
            q = (lo[0], hi[0], lo[1], hi[1], lo[2], hi[2])
            for ad, s in _engeller(q, haric):
                b = s.BoundingBox(); bb = (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)
                yuz = bb[2 * bx] if sg > 0 else bb[2 * bx + 1]
                d = (yuz - p[bx]) * sg
                if d >= r and (en is None or d < en[0]):
                    # gerçekten o noktada malzeme var mı: yüz düzleminde küçük kutu ile kesişim
                    t = [p[i] - 3.0 for i in range(3)]; u = [p[i] + 3.0 for i in range(3)]
                    t[bx], u[bx] = (yuz, yuz + 1.0) if sg > 0 else (yuz - 1.0, yuz)
                    try:
                        if s.intersect(kut(t[0], u[0], t[1], u[1], t[2], u[2])).Volume() > 0.01:
                            en = (d, yuz, ("+" if sg > 0 else "-") + "xyz"[bx])
                    except Exception:
                        pass
    return None if en is None else (en[1], en[2])


def kelepce_yeri_gercek(p, eksen, r, maks=200.0, haric=()):
    """kelepce_yeri kutu yüzüyle bulamazsa (içbükey parça: kablo teknenin İÇİNDE) — p'den her parçaya GERÇEK en yakın nokta ·
    nokta kabloya dik tek eksende (diğer iki eksende ≤ r) ve ≥ r uzaktaysa o yüzey · döner (yüzey koordinatı, yön) ya da None"""
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape
    ax = "xyz".index(eksen); en = None
    q = (p[0] - maks, p[0] + maks, p[1] - maks, p[1] + maks, p[2] - maks, p[2] + maks)
    vx = cq.Vertex.makeVertex(*p).wrapped
    for ad, s in _engeller(q, haric):
        d = BRepExtrema_DistShapeShape(vx, s.wrapped)
        if not d.IsDone() or d.Value() < r or d.Value() > maks: continue
        for k in range(1, d.NbSolution() + 1):
            c = d.PointOnShape2(k); c = (c.X(), c.Y(), c.Z())
            fark = [c[i] - p[i] for i in range(3)]
            bx = max((i for i in range(3) if i != ax), key=lambda i: abs(fark[i]))
            if all(abs(fark[i]) <= r for i in range(3) if i not in (ax, bx)) and abs(fark[bx]) >= r and (en is None or abs(fark[bx]) < en[0]):
                en = (abs(fark[bx]), c[bx], ("+" if fark[bx] > 0 else "-") + "xyz"[bx])
    return None if en is None else (en[1], en[2])


def kelepceler(pts, r, aralik=250.0, haric=()):
    """≥ 200 mm parçalara ~250 mm aralıkla, en yakın yüzeye kelepçe · kelepçe başka parçaya değiyorsa parça boyunca ±20 / ±40 / ±60 mm kaydırılır ·
    döner ([(nokta, şekil)], [askıda kalan parça])"""
    out, aski = [], []
    for a, b in zip(pts[:-1], pts[1:]):
        L = math.dist(a, b)
        if L < 200.0: continue
        eksen = "xyz"[[abs(b[k] - a[k]) > 1e-6 for k in range(3)].index(True)]
        n = max(1, int(L // aralik))
        for j in range(n):
            f0 = (j + 0.5) / n; kon = None; p0 = None
            for dd in (0.0, 20.0, -20.0, 40.0, -40.0, 60.0, -60.0):
                f = f0 + dd / L
                if not (15.0 / L < f < 1.0 - 15.0 / L): continue
                p = tuple(a[k] + f * (b[k] - a[k]) for k in range(3)); p0 = p0 or p
                y = kelepce_yeri(p, eksen, r, haric=haric)
                if y is None: continue
                ks = EO.kelepce(p, eksen, r, y[0], y[1])
                if temiz(ks, haric)[0]: kon = (p, ks); break
            if kon is None:                                                   # içbükey parçada gerçek yüzeyle yeniden dene
                for dd in (0.0, 20.0, -20.0, 40.0, -40.0, 60.0, -60.0):
                    f = f0 + dd / L
                    if not (15.0 / L < f < 1.0 - 15.0 / L): continue
                    p = tuple(a[k] + f * (b[k] - a[k]) for k in range(3))
                    y = kelepce_yeri_gercek(p, eksen, r, haric=haric)
                    if y is None: continue
                    for tb in (8.0, 5.0):
                        ks = EO.kelepce(p, eksen, r, y[0], y[1], tab=tb)
                        if temiz(ks, haric)[0]: kon = (p, ks); break
                    if kon is not None: break
            if kon is None: aski.append((a, b, p0 or a)); continue
            out.append(kon)
    return out, aski
