# -*- coding: utf-8 -*-
"""B dolabı · AÇIKTA KALAN PU (görüş) taraması — pu_acik_tara.py yönteminin genişletilmişi: ortografik z-tampon raster (1 mm), her hücrede ilk
görülen yüzün düğümü; B_KASA__pu öndeyse 'açık'. Bakışlar: tam önden + 4 eğik (sol/sağ/üst/alt 30°). Durumlar:
  1 'kapaklar gizli'   : çekmece / depo önleri + fitiller gizli (boğaz durumu)
  2 'açıklık içi'      : bütün CEK_* düğümleri + depo çekmecesi gizli (kutular, raylar, motorlar yok → açıklıktan içeri bakış)
Örtücü olarak yalnız B_* gövde/teknik düğümleri alınır (elektrik, ürün, kablo örtücü sayılmaz → sonuç güvenli tarafta).
Kullanım: python b_pu_gorunur.py model.glb"""
import sys
import numpy as np
from scipy import ndimage
import glb_oku

J, D = glb_oku.yukle(sys.argv[1])
h = 1.0
GOR = {"on": (0, 0), "sol30": (30, 0), "sag30": (-30, 0), "ust30": (0, 30), "alt30": (0, -30)}


def rot(ay, ax):
    a, b = np.radians(ay), np.radians(ax)
    Ry = np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]])
    Rx = np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]])
    return Rx @ Ry


def tara(durum, ay, ax):
    M = rot(ay, ax)
    sec = []
    for ad, (X, T) in D.items():
        if not ad.startswith("B_") or not len(T): continue
        if durum == 2 and ad.startswith("B_DEPO") and "CEKMECE" in ad: continue
        P = X[T]
        m = (P[:, :, 2].min(1) < 38.9) if durum == 2 else np.ones(len(P), bool)   # 2: servis paneli / ön paneller (z ≥ 39) de gizli
        m &= (P[:, :, 0].max(1) > 730) & (P[:, :, 0].min(1) < 4410) & (P[:, :, 1].min(1) < 795) & (P[:, :, 2].max(1) > -840)
        if m.any(): sec.append((ad, P[m] @ M.T))
    if durum == 1:                                           # kapaklar gizli: depo + servis önleri (z > 39 ön paneller) de gizlenir
        sec = [(a, P) for a, P in sec if not (a.startswith("B_DEPO") and "CEKMECE" in a and ("pu" in a or "conta" in a))]
    allP = np.concatenate([P for _, P in sec]).reshape(-1, 3)
    X0, Y0 = allP[:, 0].min(), allP[:, 1].min(); X1, Y1 = allP[:, 0].max(), allP[:, 1].max()
    xs = np.arange(X0 + h / 2, X1, h); ys = np.arange(Y0 + h / 2, Y1, h)
    zb = np.full((len(ys), len(xs)), -1e9); kim = np.full((len(ys), len(xs)), -1, int)
    adlar = []
    for ad, P in sec:
        k = len(adlar); adlar.append(ad)
        for tri in P:
            (x0, y0, z0), (x1, y1, z1), (x2, y2, z2) = tri
            d = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
            if abs(d) < 1e-9: continue
            i0 = np.searchsorted(xs, min(x0, x1, x2)); i1 = np.searchsorted(xs, max(x0, x1, x2), "right")
            j0 = np.searchsorted(ys, min(y0, y1, y2)); j1 = np.searchsorted(ys, max(y0, y1, y2), "right")
            if i1 <= i0 or j1 <= j0: continue
            XX, YY = np.meshgrid(xs[i0:i1], ys[j0:j1])
            a = ((y1 - y2) * (XX - x2) + (x2 - x1) * (YY - y2)) / d; b = ((y2 - y0) * (XX - x2) + (x0 - x2) * (YY - y2)) / d; c = 1 - a - b
            ins = (a >= -1e-6) & (b >= -1e-6) & (c >= -1e-6); Z = a * z0 + b * z1 + c * z2
            sub = zb[j0:j1, i0:i1]; ks = kim[j0:j1, i0:i1]; y_ = ins & (Z > sub + 1e-4); sub[y_] = Z[y_]; ks[y_] = k
    pu = np.array([a == "B_KASA__pu" for a in adlar] + [False])
    acik = pu[kim]
    lab, n = ndimage.label(acik)
    R = []
    for i, sl in enumerate(ndimage.find_objects(lab)):
        c = int((lab[sl] == i + 1).sum())
        if c < 2: continue
        R.append((round(xs[sl[1].start], 1), round(xs[sl[1].stop - 1], 1), round(ys[sl[0].start], 1), round(ys[sl[0].stop - 1], 1), c))
    return int(acik.sum()), R


toplam = 0
for durum, dad in ((1, "kapaklar gizli"), (2, "açıklık içi (çekmeceler gizli)")):
    for g, (ay, ax) in GOR.items():
        if durum == 1 and g != "on": continue
        n, R = tara(durum, ay, ax); toplam += n
        print("  %-32s %-6s açık PU hücresi %5d (≈ %d mm²)%s" % (dad, g, n, n, "" if not R else "  " + str(R[:6])))
print("B PU GÖRÜNÜRLÜK: %s" % ("TEMİZ" if toplam == 0 else "BULGU %d hücre" % toplam))
