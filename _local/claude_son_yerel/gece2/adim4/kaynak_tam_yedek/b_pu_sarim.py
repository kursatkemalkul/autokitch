# -*- coding: utf-8 -*-
"""B gövdesi PU SARIM DENETİMİ (kesit): her PU katısının BÜTÜN yüzleri ≤ 6 mm aralıkla örneklenir, nokta yüz normali boyunca 0,4 mm DIŞARI
kaydırılır; o nokta bir sacın / başka PU'nun / gömülü elemanın (modüler, taşıyıcı, kanal, gider kılıfı, elektrik kanalı, depo + ara saclar) İÇİNDE
olmalı. Değilse PU yüzü havaya bakıyor (açık / sac ile PU arası boşluk) → bulgu. Kullanım: python b_pu_sarim.py"""
import numpy as np
import cadquery as cq
from OCP.BRepClass3d import BRepClass3d_SolidClassifier
from OCP.gp import gp_Pnt
from OCP.TopAbs import TopAbs_IN, TopAbs_ON
import b_govde_yeni as BG

ADIM, OFS = 6.0, 0.4
R = BG.yap()
ORTU = {}
for g, d in R.items():
    for k, s in d.items():
        if g == "moduler" and not k.startswith("sase"):
            b = s.BoundingBox(); s = BG.kutu(b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)   # boru dış zarfı (PU zarfa döker)
        ORTU["%s/%s" % (g, k)] = s
for k, s in BG.yabanci().items(): ORTU["glb/" + k] = s
BB = {k: s.BoundingBox() for k, s in ORTU.items()}
CL = {k: BRepClass3d_SolidClassifier(s.wrapped) for k, s in ORTU.items()}


def ornek(f):
    v, t = f.tessellate(0.05, 0.2)
    V = np.array([[q.x, q.y, q.z] for q in v]); T = np.array(t)
    if not len(T): return np.zeros((0, 3)), np.zeros((0, 3))
    P = V[T]; L = np.max(np.linalg.norm(P[:, [1, 2, 0]] - P, axis=2), axis=1); n = np.maximum(1, np.ceil(L / ADIM)).astype(int)
    out = []
    for k in np.unique(n):
        W = np.array([(1 - a / k - b / k, a / k, b / k) for a in range(k + 1) for b in range(k + 1 - a)])
        out.append(np.einsum("wk,tkd->twd", W, P[n == k]).reshape(-1, 3))
    Q = np.unique(np.round(np.concatenate(out), 3), axis=0)
    N = np.array([f.normalAt(cq.Vector(*q)).toTuple() for q in Q]) if f.geomType() != "PLANE" else np.tile(f.normalAt().toTuple(), (len(Q), 1))
    return Q, N


top_n, top_a = 0, 0
for ad, s in R["pu"].items():
    acik = []; n_ = 0
    for f in s.Faces():
        Q, N = ornek(f)
        if not len(Q): continue
        Q = Q + OFS * N; n_ += len(Q)
        kalan = np.ones(len(Q), bool)
        for k, bb in BB.items():
            if k == "pu/" + ad or not kalan.any(): continue
            m = kalan & (Q[:, 0] > bb.xmin - 1e-6) & (Q[:, 0] < bb.xmax + 1e-6) & (Q[:, 1] > bb.ymin - 1e-6) & (Q[:, 1] < bb.ymax + 1e-6) & (Q[:, 2] > bb.zmin - 1e-6) & (Q[:, 2] < bb.zmax + 1e-6)
            for i in np.where(m)[0]:
                CL[k].Perform(gp_Pnt(*Q[i]), 1e-4)
                if CL[k].State() in (TopAbs_IN, TopAbs_ON): kalan[i] = False      # ON: iki örtücünün birleşim düzlemi (köşe/kenar)
        if kalan.any(): acik.append(Q[kalan])
    top_n += n_
    if acik:
        A = np.concatenate(acik); top_a += len(A)
        print("  AÇIK  %-22s %5d / %6d nokta" % (ad, len(A), n_))
        from scipy.cluster.hierarchy import fcluster, linkage
        Z = fcluster(linkage(A[:4000], "single"), 8.0, "distance") if len(A) > 1 else np.array([1])
        for c in np.unique(Z)[:12]:
            B_ = A[:4000][Z == c]; print("        %4d nokta  %s … %s" % (len(B_), B_.min(0).round(1).tolist(), B_.max(0).round(1).tolist()))
    else:
        print("  tam   %-22s %6d nokta · bütün yüzler sac / PU / gömülü elemana değiyor" % (ad, n_))
print("B PU SARIM DENETİMİ: %d PU · %d yüzey noktası · açık %d → %s" % (len(R["pu"]), top_n, top_a, "TEMİZ" if not top_a else "BULGU"))
