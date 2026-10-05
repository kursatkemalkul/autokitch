# -*- coding: utf-8 -*-
"""B gövdesi (yeni) BOŞLUK DENETİMİ — a_govde_bosluk.py kuralı (iki eksende > 1 mm örtüşen, üçüncüde 0,2–15 mm açık parça çifti) + GERÇEKLİK:
aradaki dilim (örtüşme dikdörtgeni × açıklık) 5 × 5 × 3 noktayla örneklenir; nokta (i) iki parçaya da dik yönde bakıyor (dilim kenarından 0,1 mm
içeri kaydırınca A ve B katısının İÇİNDE) ve (ii) başka hiçbir gövde parçası / değişmeyen komşu katı (depo, ara saclar, taşıyıcı, kanal, gider
kılıfı) tarafından doldurulmuyorsa → GERÇEK BOŞLUK. Isı kalkanı hava boşluğunun içindekiler (ışınım sacı, takozlar) kasıtlı listelenir.
Kullanım: python b_govde_bosluk.py"""
import numpy as np
from OCP.BRepClass3d import BRepClass3d_SolidClassifier
from OCP.gp import gp_Pnt
from OCP.TopAbs import TopAbs_IN, TopAbs_ON
import b_govde_yeni as BG

R = BG.yap()
P = {"%s/%s" % (g, k): s for g, d in R.items() for k, s in d.items()}
DOLGU = dict(P); DOLGU.update({"glb/" + k: s for k, s in BG.yabanci().items()})
B = {k: s.BoundingBox() for k, s in DOLGU.items()}
CL = {k: BRepClass3d_SolidClassifier(s.wrapped) for k, s in DOLGU.items()}


def icinde(k, q, on=True):
    CL[k].Perform(gp_Pnt(*q), 1e-4); st = CL[k].State()
    return st == TopAbs_IN or (on and st == TopAbs_ON)


def dolu(q, haric):
    for k, b in B.items():
        if k in haric: continue
        if b.xmin - 1e-6 <= q[0] <= b.xmax + 1e-6 and b.ymin - 1e-6 <= q[1] <= b.ymax + 1e-6 and b.zmin - 1e-6 <= q[2] <= b.zmax + 1e-6 and icinde(k, q): return True
    return False


KASITLI = ("isi_kalkani_isinim", "isi_kalkani_takozu")
ad = list(P); bul, kas = [], []
for i in range(len(ad)):
    for j in range(i + 1, len(ad)):
        a, b = B[ad[i]], B[ad[j]]
        lo_ = [max(a.xmin, b.xmin), max(a.ymin, b.ymin), max(a.zmin, b.zmin)]; hi_ = [min(a.xmax, b.xmax), min(a.ymax, b.ymax), min(a.zmax, b.zmax)]
        ort = [hi_[e] - lo_[e] for e in range(3)]
        for e in range(3):
            diger = [ort[k] for k in range(3) if k != e]
            if not (min(diger) > 1.0 and -15.0 < ort[e] < -0.2): continue
            amin, amax = [(a.xmin, a.xmax), (a.ymin, a.ymax), (a.zmin, a.zmax)][e]
            ilk = amax <= [(b.xmin, b.xmax), (b.ymin, b.ymax), (b.zmin, b.zmax)][e][0] + 1e-6     # A önde mi
            g0, g1 = hi_[e], lo_[e]                                                                # açıklık aralığı (hi < lo)
            bos = 0; top = 0
            ax = [k for k in range(3) if k != e]
            for u in np.linspace(0.1, 0.9, 5):
                for v in np.linspace(0.1, 0.9, 5):
                    q = [0, 0, 0]; q[ax[0]] = lo_[ax[0]] + u * ort[ax[0]]; q[ax[1]] = lo_[ax[1]] + v * ort[ax[1]]
                    qa, qb = list(q), list(q)
                    qa[e] = (g0 - 0.1) if ilk else (g1 + 0.1); qb[e] = (g1 + 0.1) if ilk else (g0 - 0.1)
                    if not (icinde(ad[i], qa, False) and icinde(ad[j], qb, False)): continue     # karşılıklı yüz yok
                    top += 1
                    if all(not dolu([*q[:e], g0 + t * (g1 - g0), *q[e + 1:]], (ad[i], ad[j])) for t in (0.25, 0.5, 0.75)): bos += 1
            if bos:
                rec = (ad[i], ad[j], "xyz"[e], round(g1 - g0, 2), bos, top)
                (kas if any(x in ad[i] + ad[j] for x in KASITLI) else bul).append(rec)
print("B GÖVDESİ BOŞLUK DENETİMİ (0,2–15 mm, karşılıklı yüz, arası boş) · %d parça" % len(ad))
print("  gerçek boşluk: %s" % ("TEMİZ" if not bul else "%d BULGU" % len(bul)))
for b in bul: print("     %-32s ↔ %-32s %s ekseninde %.2f mm  (%d/%d nokta boş)" % b)
print("  kasıtlı — ısı kalkanı hava boşluğu içinde (ışınım sacı takozlarda yüzer, takoz çevresi hava; ısı köprüsü yok): %d" % len(kas))
for b in kas: print("     %-32s ↔ %-32s %s ekseninde %.2f mm  (%d/%d nokta boş)" % b)
