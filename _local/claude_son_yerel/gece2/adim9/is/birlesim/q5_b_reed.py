# -*- coding: utf-8 -*-
"""q5 · B ÇEKMECE REED KABLOLARI KLİPSLİ (iş 3b). 21 reed kablosu (Ø4, kolon x 806/1461/2116/2771/3426) her çekmece sırasında
z −760…−55 açık (705 mm, 0 tutucu) gidiyordu. Her kablonun hemen +x yanında SABİT L lama var (CEK_*__celik, çekmece kızağı DEĞİL;
kablo yüzü → lama 0,25 mm). YENİ: POM U-klips (1 mm, 10 mm boy) lamaya geçmeli, kabloyu üç yandan sarar · z −700/−550/−400/−250/−100
(150 aralık) → 21 × 5 = 105 klips. Kontrol: klipsin x-y izdüşümü, kapalı konumda klipslerin gerisinde/hizasında (z ≤ −95) kalan hiçbir hareketli (…__CEKMECE) parçanın izdüşümüne değmez →
çekmece 700 mm açılırken kızak/çekmece klipse çarpmaz (hareket z boyunca).
python q5_b_reed.py giris.glb cikis.glb"""
import sys
from qlib import *
from kesit import kesit
gi, go = sys.argv[1:3]
G = m8kit.Glb(gi)
L = kesit(G, "ELK_DOLAP__kablo", 2, -400.0, np.array([700, 150, -900.]), np.array([3500, 790, 0.]))
K = [(c, d) for c, d in L if abs(d[0] - 4) < 0.3 and abs(d[1] - 4) < 0.3]
assert len(K) == 21, len(K)
YS = m8kit.Yuzey(G, haric=("INSAN", "ZEMIN"))
ZS = (-700.0, -550.0, -400.0, -250.0, -100.0)
# hareketli parca izdusumleri (x-y)
HP = []
for p in G.prims:
    if "CEKMECE" not in p["name"] or p.get("gizli"): continue
    P = p["X"][p["T"][G.gorunur(p)]]
    HP.append(np.stack([P[:, :, 0].min(1), P[:, :, 0].max(1), P[:, :, 1].min(1), P[:, :, 1].max(1), P[:, :, 2].min(1)], 1))
HP = np.concatenate(HP)
et = G._etiketler(prim(G, "ELK_DOLAP__celik"), 0)
Pw = []; cak = 0
for c, d in K:
    xc, yc = c[0], c[1]; r = 2.0
    t = YS.isin((xc + r + 0.01, yc + 1.0, -400.0), (1, 0, 0), 10, haric_ad=r"kablo")
    assert t is not None and t < 1.0, (xc, yc, t)
    xl = xc + r + 0.01 + t                                   # lama yuzu
    x0 = xc - r - 1.2
    box = (x0, xl, yc - r - 1.2, yc + r + 1.2)
    ov = (HP[:, 1] > box[0] - 0.3) & (HP[:, 0] < box[1] + 0.3) & (HP[:, 3] > box[2] - 0.3) & (HP[:, 2] < box[3] + 0.3) & (HP[:, 4] <= max(ZS) + 5)   # cekmece yalniz +z acilir: kapali konumda klipsin onunde (z > -95) duran parca klipse ulasmaz
    cak += int(ov.sum())
    for z in ZS:
        z0, z1 = z - 5, z + 5
        Pw += [kutu_ucgen((x0, yc - r - 1.2, z0), (xc - r - 0.2, yc + r + 1.2, z1)),             # sirt
               kutu_ucgen((xc - r - 0.2, yc + r + 0.2, z0), (xl, yc + r + 1.2, z1)),             # ust bacak -> lama
               kutu_ucgen((xc - r - 0.2, yc - r - 1.2, z0), (xl, yc - r - 0.2, z1))]             # alt bacak
print("  reed kablo %d · klips %d · hareketli parca izdusum kesisimi %d" % (len(K), len(K) * len(ZS), cak))
assert cak == 0
n = ekle(G, "ELK_DOLAP__celik", np.concatenate(Pw), et); print("  klips ucgen", n)
G.kaydet(go); print("yazildi", go)
