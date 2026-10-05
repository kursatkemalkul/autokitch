# -*- coding: utf-8 -*-
"""A gövdesi (yeni) ÇAKIŞMA DENETİMİ — yalnız bu gövde: her yeni parçanın katısı ↔ GLB'deki bütün diğer düğümlerin üçgenleri.
Yöntem: komşu üçgenlerin köşeleri + ağırlık merkezleri + kenar orta noktaları gövde parçasının İÇİNDE mi (OCC BRepClass3d, tolerans 0,3 mm).
Ayrıca gövde parçalarının birbiriyle hacim kesişimi (OCC boolean)."""
import sys, importlib.util
import numpy as np
import cadquery as cq
from OCP.BRepClass3d import BRepClass3d_SolidClassifier
from OCP.gp import gp_Pnt
from OCP.TopAbs import TopAbs_IN
import glb_oku

sp = importlib.util.spec_from_file_location("ag", "a_govde_yeni.py")
src = open("a_govde_yeni.py", encoding="utf-8").read().split("gi, go = sys.argv[1:3]")[0]
G = {}; exec(src, G)
PARCA = {**G["SAC"], **G["CERCEVE"], **G["KAIDE_P"], **G["KAIDE_S"]}
J, D = glb_oku.yukle(sys.argv[1])
ATLA = ("A_GOVDE__", "U_A_GOVDE__", "KAIDE_A__")
TOL = 0.3
bulgu = []
for ad, s in PARCA.items():
    bb = s.BoundingBox()
    sc = s.scale(1.0)
    for nd, (X, T) in D.items():
        if nd.startswith(ATLA): continue
        P = X[T]                                                    # (n,3,3)
        nok = np.concatenate([P.reshape(-1, 3), P.mean(axis=1), (P[:, 0] + P[:, 1]) / 2, (P[:, 1] + P[:, 2]) / 2, (P[:, 2] + P[:, 0]) / 2])
        m = (nok[:, 0] > bb.xmin + TOL) & (nok[:, 0] < bb.xmax - TOL) & (nok[:, 1] > bb.ymin + TOL) & (nok[:, 1] < bb.ymax - TOL) & (nok[:, 2] > bb.zmin + TOL) & (nok[:, 2] < bb.zmax - TOL)
        if not m.any(): continue
        ic = 0
        cl = BRepClass3d_SolidClassifier(s.wrapped)
        for p in np.unique(np.round(nok[m], 2), axis=0)[:4000]:
            cl.Perform(gp_Pnt(*p), TOL)
            if cl.State() == TopAbs_IN: ic += 1
        if ic: bulgu.append((ad, nd, ic))
# gövde içi
adlar = list(PARCA)
ic_b = []
for i in range(len(adlar)):
    for j in range(i + 1, len(adlar)):
        a, b = PARCA[adlar[i]], PARCA[adlar[j]]
        ba, bb_ = a.BoundingBox(), b.BoundingBox()
        if ba.xmin > bb_.xmax or bb_.xmin > ba.xmax or ba.ymin > bb_.ymax or bb_.ymin > ba.ymax or ba.zmin > bb_.zmax or bb_.zmin > ba.zmax: continue
        v = a.intersect(b).Volume()
        if v > 1.0: ic_b.append((adlar[i], adlar[j], round(v, 1)))
print("A GÖVDESİ ÇAKIŞMA DENETİMİ · %d parça" % len(PARCA))
print("  gövde ↔ diğer parçalar: %s" % ("TEMİZ" if not bulgu else "%d BULGU" % len(bulgu)))
for b in sorted(bulgu, key=lambda x: -x[2]): print("     %-30s ↔ %-36s %d nokta içeride" % b)
print("  gövde ↔ gövde (hacim > 1 mm³): %s" % ("TEMİZ" if not ic_b else "%d BULGU" % len(ic_b)))
for b in ic_b: print("     %-30s ↔ %-30s %s mm³" % b)
