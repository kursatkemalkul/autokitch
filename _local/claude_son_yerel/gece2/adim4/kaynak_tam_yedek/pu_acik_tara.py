# -*- coding: utf-8 -*-
"""Açıkta kalan YALITIM (PU) taraması: verilen düğümdeki PU yüzleri, bakış yönünde ilk görülen yüz mü? (ışın atma, trimesh yoksa raster)
Yöntem: önden (+z → −z) ortografik raster · her hücrede en öndeki yüzün malzemesi · PU öndeyse 'açık'.
Kullanım: python pu_acik_tara.py model.glb x0 x1 y0 y1 [adim]"""
import sys
import numpy as np
import glb_oku

gi = sys.argv[1]; X0, X1, Y0, Y1 = map(float, sys.argv[2:6]); h = float(sys.argv[6]) if len(sys.argv) > 6 else 1.0
J, D = glb_oku.yukle(gi)
xs = np.arange(X0 + h / 2, X1, h); ys = np.arange(Y0 + h / 2, Y1, h)
zbuf = np.full((len(ys), len(xs)), -1e9); kim = np.full((len(ys), len(xs)), -1, int)
adlar = []
GIZLI = ("on_seffaf",)                                       # kapaklar kapalıyken önde olurlar; boğaz (kapak açık) durumu için kapaklar hariç
for ad, (X, T) in D.items():
    if any(g in ad for g in GIZLI): continue
    if ad.startswith(("INSAN", "ZEMIN", "ROBOT", "ELK_ZEMIN", "ELK_ANA_HAT")): continue
    P = X[T]
    m = (P[:, :, 0].max(1) > X0) & (P[:, :, 0].min(1) < X1) & (P[:, :, 1].max(1) > Y0) & (P[:, :, 1].min(1) < Y1) & (P[:, :, 2].max(1) > -900)
    if not m.any(): continue
    k = len(adlar); adlar.append(ad)
    for tri in P[m]:
        (x0, y0, z0), (x1, y1, z1), (x2, y2, z2) = tri
        d = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
        if abs(d) < 1e-9: continue
        ix = np.where((xs >= min(x0, x1, x2)) & (xs <= max(x0, x1, x2)))[0]; iy = np.where((ys >= min(y0, y1, y2)) & (ys <= max(y0, y1, y2)))[0]
        if not len(ix) or not len(iy): continue
        XX, YY = np.meshgrid(xs[ix], ys[iy])
        a = ((y1 - y2) * (XX - x2) + (x2 - x1) * (YY - y2)) / d; b = ((y2 - y0) * (XX - x2) + (x0 - x2) * (YY - y2)) / d; c = 1 - a - b
        ins = (a >= -1e-6) & (b >= -1e-6) & (c >= -1e-6)
        Z = a * z0 + b * z1 + c * z2
        sub = zbuf[np.ix_(iy, ix)]; ks = kim[np.ix_(iy, ix)]
        yeni = ins & (Z > sub + 1e-4)
        sub[yeni] = Z[yeni]; ks[yeni] = k
        zbuf[np.ix_(iy, ix)] = sub; kim[np.ix_(iy, ix)] = ks
pu = np.array([("__pu" in a) or ("yalitim" in a) for a in adlar] + [False])
acik = pu[kim]
from scipy import ndimage
lab, n = ndimage.label(acik)
print("önden açık PU hücresi: %d (%.0f mm²) · %d bölge" % (acik.sum(), acik.sum() * h * h, n))
R = []
for i, sl in enumerate(ndimage.find_objects(lab)):
    c = (lab[sl] == i + 1).sum()
    if c * h * h < 4: continue
    x0, x1 = xs[sl[1].start] - h / 2, xs[sl[1].stop - 1] + h / 2; y0, y1 = ys[sl[0].start] - h / 2, ys[sl[0].stop - 1] + h / 2
    zz = zbuf[sl][lab[sl] == i + 1]
    dug = adlar[np.bincount(kim[sl][lab[sl] == i + 1]).argmax()]
    R.append((round(x0, 1), round(x1, 1), round(y0, 1), round(y1, 1), round(zz.min(), 1), round(zz.max(), 1), round(c * h * h), dug))
for r in sorted(R): print("  x %7.1f–%7.1f  y %6.1f–%6.1f  z %6.1f…%6.1f  %6d mm²  %s" % r)
import json; json.dump(R, open("pu_acik.json", "w"))
