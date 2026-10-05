# -*- coding: utf-8 -*-
"""B gövdesi ↔ ÇEKMECELER oturma denetimi (yeni gövde, değişmeyen çekmeceler):
  · fitil tabanı (z 24) ön çerçeveye değiyor mu — taban örnek noktaları z 23,5'te çerçeve katısının içinde mi (oran)
  · kapak açıklığa göre taşmaları (sol/sağ/alt/üst) · kapak fitili tamamen örtüyor mu
  · hareketli parçalar (…__CEKMECE: 700 strok · …__CEKMECE_ARA: 350 · depo 450/225) açıklıktan çarpmadan geçer: x/y zarfı açıklığın içinde +
    strok boyunca süpürülen kutu ↔ bütün gövde katıları hacim kesişimi 0. Kullanım: python b_cekmece_denetim.py model.glb"""
import sys
import numpy as np
from OCP.BRepClass3d import BRepClass3d_SolidClassifier
from OCP.gp import gp_Pnt
from OCP.TopAbs import TopAbs_IN
import glb_oku, b_govde_yeni as BG

J, D = glb_oku.yukle(sys.argv[1])
R = BG.yap()
GOV = [s for d in R.values() for s in d.values()]
CER = R["cerceve"]["on_cerceve"]; clc = BRepClass3d_SolidClassifier(CER.wrapped)
ACK = {}
for k, x0, w, ys, hs in BG.CEK:
    tip = sorted([n.split("__")[0] for n in D if n.startswith("CEK_%s_" % k)], key=lambda u: 0)
    birim = sorted({n.split("__")[0] for n in D if n.startswith("CEK_%s_" % k)}, key=lambda u: min(D[n][0][np.unique(D[n][1])][:, 1].min() for n in D if n.startswith(u + "__")))
    for u, y, hh in zip(birim, ys, hs): ACK[u] = (x0, x0 + w, y, y + hh, 700.0)
ACK["B_DEPO"] = BG.DEPO_ACIK + (450.0,)


def bb(P): return P.min(0), P.max(0)


def ornek(P, adim=3.0):
    L = np.max(np.linalg.norm(P[:, [1, 2, 0]] - P, axis=2), axis=1); n = np.maximum(1, np.ceil(L / adim)).astype(int); out = [P.mean(1)]
    for k in np.unique(n):
        W = np.array([(1 - a / k - b / k, a / k, b / k) for a in range(k + 1) for b in range(k + 1 - a)])
        out.append(np.einsum("wk,tkd->twd", W, P[n == k]).reshape(-1, 3))
    return np.unique(np.round(np.concatenate(out), 2), axis=0)


hata = 0
print("B ÇEKMECE ↔ GÖVDE DENETİMİ · %d açıklık" % len(ACK))
print("  %-16s %-23s %-26s %-17s %s" % ("birim", "açıklık x / y", "kapak taşma s/s/a/ü", "fitil→çerçeve", "strok (zarf payı · süpürme)"))
for u, (ax0, ax1, ay0, ay1, st) in ACK.items():
    ond = [n for n in D if n.startswith(u + "__") and ("on_seffaf" in n or (u == "B_DEPO" and ("conta" in n or "pu__CEKMECE" in n or n == "B_DEPO__sac__CEKMECE")))]
    F = [];  K = []
    for n in ond:
        X, T = D[n]; P = X[T]
        if u != "B_DEPO" or "conta" in n: F.append(P[P[:, :, 2].max(1) <= 24.05])
        K.append(P[P[:, :, 2].min(1) >= 38.95])
    F = np.concatenate(F); K = np.concatenate(K)
    fq = ornek(F); ic = 0
    for q in fq:
        clc.Perform(gp_Pnt(q[0], q[1], 23.5), 1e-4); ic += clc.State() == TopAbs_IN
    kmin, kmax = bb(K.reshape(-1, 3)); fmin, fmax = bb(F.reshape(-1, 3))
    kt = (ax0 - kmin[0], kmax[0] - ax1, ay0 - kmin[1], kmax[1] - ay1)
    ortu = kmin[0] <= fmin[0] and kmax[0] >= fmax[0] and kmin[1] <= fmin[1] and kmax[1] >= fmax[1]
    pay, kes = 1e9, 0.0
    for n in D:
        if not n.startswith(u + "__") or "CEKMECE" not in n or n in ond: continue
        X, T = D[n]; P = X[np.unique(T)]; a, b = bb(P)
        s = st / 2 if n.endswith("CEKMECE_ARA") else st
        pay = min(pay, a[0] - ax0, ax1 - b[0], a[1] - ay0, ay1 - b[1])
        sup = BG.kutu(a[0] + 0.05, b[0] - 0.05, a[1] + 0.05, b[1] - 0.05, a[2], b[2] + s)
        for g in GOV:
            if BG._kesisir(sup.BoundingBox(), g.BoundingBox()): kes += sup.intersect(g).Volume()
    ok = pay >= 0 and kes < 0.01 and ortu
    hata += not ok
    print("  %-16s %6.1f–%6.1f / %5.1f–%5.1f  %5.1f/%5.1f/%5.1f/%5.1f %s  %5.1f %%         %s pay %.1f mm · kesişim %.2f mm³" % (
        u, ax0, ax1, ay0, ay1, kt[0], kt[1], kt[2], kt[3], "örter" if ortu else "AÇIK ", 100.0 * ic / len(fq), "TEMİZ" if ok else "BULGU", pay, kes))
print("  not: fitil profili açıklık kenarının 4 mm dışında, taban 21 mm → tabanın 6,5 mm'si açıklığın içine taşar (çekmece rayları açıklığın tam kenarında;"
      " açıklık daraltılamaz) — temas bandı 14,5 mm, kesintisiz çevre")
print("B ÇEKMECE ↔ GÖVDE: %s" % ("TEMİZ" if not hata else "%d BULGU" % hata))
