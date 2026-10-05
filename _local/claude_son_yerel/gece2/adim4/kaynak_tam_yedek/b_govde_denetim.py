# -*- coding: utf-8 -*-
"""B gövdesi (yeni) ÇAKIŞMA DENETİMİ — a_govde_denetim.py yöntemi: her yeni gövde katısı ↔ GLB'deki bütün DİĞER düğümlerin üçgenleri
(köşe + ağırlık merkezi + kenar ortaları, OCC BRepClass3d, tolerans 0,3 mm) · gövde parçalarının kendi arasında hacim kesişimi (OCC boolean > 1 mm³).
Kullanım: python b_govde_denetim.py model.glb"""
import sys
import numpy as np
from OCP.BRepClass3d import BRepClass3d_SolidClassifier
from OCP.gp import gp_Pnt
from OCP.TopAbs import TopAbs_IN
import glb_oku, b_govde_yeni as BG

R = BG.yap()
PARCA = {}
for g, d in R.items():
    for k, s in d.items(): PARCA["%s/%s" % (g, k)] = s
J, D = glb_oku.yukle(sys.argv[1])
ATLA = ("B_KASA__sac", "B_KASA__pu", "B_KASA__on_cerceve", "B_KASA__koyu", "B_MODULER__")
TOL = 0.3
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeVertex


def _derinlik(s, q):
    d = BRepExtrema_DistShapeShape(BRepBuilderAPI_MakeVertex(gp_Pnt(*q)).Vertex(), s.wrapped); d.Perform()
    return d.Value() if d.IsDone() else 0.0
bulgu = []
NOK = {}
ADIM = 4.0                                        # büyük üçgenler de yakalansın: her üçgen ≤ 4 mm aralıklı barisentrik ızgarayla örneklenir
ZARF = (730.0, 4410.0, -1.0, 800.0, -840.0, 90.0)


def ornekle(P):
    out = [P.reshape(-1, 3), P.mean(axis=1)]
    L = np.max(np.linalg.norm(P[:, [1, 2, 0]] - P, axis=2), axis=1)
    n = np.maximum(1, np.ceil(L / ADIM)).astype(int)
    for k in np.unique(n):
        Q = P[n == k]
        ab = [(i / k, j / k) for i in range(k + 1) for j in range(k + 1 - i)]
        W = np.array([(1 - a - b, a, b) for a, b in ab])
        out.append(np.einsum("wk,tkd->twd", W, Q).reshape(-1, 3))
    return np.concatenate(out)


for nd, (X, T) in D.items():
    if nd.startswith(ATLA) or not len(T): continue
    P = X[T]
    m = (P[:, :, 0].max(1) > ZARF[0]) & (P[:, :, 0].min(1) < ZARF[1]) & (P[:, :, 1].max(1) > ZARF[2]) & (P[:, :, 1].min(1) < ZARF[3]) & (P[:, :, 2].max(1) > ZARF[4]) & (P[:, :, 2].min(1) < ZARF[5])
    if not m.any(): continue
    NOK[nd] = np.unique(np.round(ornekle(P[m]), 3), axis=0)
for ad, s in PARCA.items():
    bb = s.BoundingBox()
    cl = BRepClass3d_SolidClassifier(s.wrapped)
    for nd, nok in NOK.items():
        m = (nok[:, 0] > bb.xmin + TOL) & (nok[:, 0] < bb.xmax - TOL) & (nok[:, 1] > bb.ymin + TOL) & (nok[:, 1] < bb.ymax - TOL) & (nok[:, 2] > bb.zmin + TOL) & (nok[:, 2] < bb.zmax - TOL)
        if not m.any(): continue
        ic = []
        for p in nok[m]:
            cl.Perform(gp_Pnt(*p), 1e-4)
            if cl.State() == TopAbs_IN: ic.append(p)
        if ic:                                    # yüzeyde duran (temas) noktalar sayılmaz: yüzeye uzaklık > 0,05 mm (gerçek batma) olmalı
            ic = np.array(ic); sec = ic[np.linspace(0, len(ic) - 1, min(len(ic), 300)).astype(int)]
            derin = np.array([_derinlik(s, q) for q in sec])
            if (derin > 0.05).any():
                bulgu.append((ad, nd, int(round(len(ic) * (derin > 0.05).mean())), round(float(derin.max()), 2), ic.min(0).round(1).tolist(), ic.max(0).round(1).tolist()))
adlar = list(PARCA); ic_b = []
for i in range(len(adlar)):
    for j in range(i + 1, len(adlar)):
        a, b = PARCA[adlar[i]], PARCA[adlar[j]]
        if not BG._kesisir(a.BoundingBox(), b.BoundingBox(), 0.0): continue
        v = a.intersect(b).Volume()
        if v > 1.0: ic_b.append((adlar[i], adlar[j], round(v, 1)))
print("B GÖVDESİ ÇAKIŞMA DENETİMİ · %d parça (sac %d · PU %d · çerçeve %d · modüler %d · GFRP %d · takoz %d)" % ((len(PARCA),) + tuple(len(R[k]) for k in ("sac", "pu", "cerceve", "moduler", "gfrp", "koyu"))))
print("  (a) gövde ↔ GLB'deki diğer %d düğüm: %s" % (len(NOK), "TEMİZ" if not bulgu else "%d BULGU" % len(bulgu)))
for b in sorted(bulgu, key=lambda x: -x[2]): print("     %-34s ↔ %-36s %6d nokta  en derin %.2f mm  %s … %s" % b)
print("  (b) gövde ↔ gövde hacim kesişimi (> 1 mm³): %s" % ("TEMİZ" if not ic_b else "%d BULGU" % len(ic_b)))
for b in ic_b: print("     %-34s ↔ %-34s %s mm³" % b)
