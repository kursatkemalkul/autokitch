# Yeni eklenen katılar ↔ GLB'deki diğer bütün üçgenler (içeride nokta var mı, 0,3 mm) · kullanım: python yeni_parca_denetim.py model.glb modul.py
import sys, importlib.util, numpy as np
from OCP.BRepClass3d import BRepClass3d_SolidClassifier
from OCP.gp import gp_Pnt
from OCP.TopAbs import TopAbs_IN
import glb_oku
sp = importlib.util.spec_from_file_location("m", sys.argv[2]); M = importlib.util.module_from_spec(sp); sp.loader.exec_module(M)
P = {**M.PU, **M.SAC}; J, D = glb_oku.yukle(sys.argv[1]); TOL = 0.3; bul = []
for ad, s in P.items():
    bb = s.BoundingBox(); cl = BRepClass3d_SolidClassifier(s.wrapped)
    for nd, (X, T) in D.items():
        Q = X[T]; nok = np.concatenate([Q.reshape(-1, 3), Q.mean(1), (Q[:, 0] + Q[:, 1]) / 2, (Q[:, 1] + Q[:, 2]) / 2, (Q[:, 2] + Q[:, 0]) / 2])
        m = (nok[:, 0] > bb.xmin + TOL) & (nok[:, 0] < bb.xmax - TOL) & (nok[:, 1] > bb.ymin + TOL) & (nok[:, 1] < bb.ymax - TOL) & (nok[:, 2] > bb.zmin + TOL) & (nok[:, 2] < bb.zmax - TOL)
        if not m.any(): continue
        ic = 0
        for p in np.unique(np.round(nok[m], 2), axis=0)[:4000]:
            cl.Perform(gp_Pnt(*p), TOL); ic += cl.State() == TopAbs_IN
        if ic: bul.append((ad, nd, ic))
print("YENİ PARÇA ÇAKIŞMA: %s" % ("TEMİZ" if not bul else "%d BULGU" % len(bul)))
for b in bul: print("   %-28s ↔ %-32s %d nokta" % b)
