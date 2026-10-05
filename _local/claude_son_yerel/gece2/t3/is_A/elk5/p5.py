# -*- coding: utf-8 -*-
"""Ana pano arka çıkışı: arka rakorlardan hemen arkadaki dik kapaklı kanal (güç | bilgi ayrı bölme), üstte bina/zemin girişi yatay kanalı,
altta U tabanı üstünde F arka iç kanalına (V1) yatay kanal. Yağ tenekesinin hacmine / üstüne (F içinde) girilmez — hepsi U içinde."""
import numpy as np
IST = "U"
def K(ad, e, lo, hi, **kw): return dict(ad=ad, e=e, lo=lo, hi=hi, ist=IST, **kw)
KAN = [K("PG", 1, (3926, 1863.5, -400), (3960, 2100, -350)), K("PV", 1, (3960, 1863.5, -400), (3994, 2100, -350)),
       K("PTG", 2, (3926, 2100, -776), (3960, 2172, -350)), K("PTV", 2, (3960, 2100, -776), (3994, 2172, -350)),
       K("PFG", 2, (3926, 1863.5, -786), (3960, 1898.5, -400)), K("PFV", 2, (3960, 1863.5, -786), (3994, 1898.5, -400))]
# yeni kablo yolları (pano arka rakoru -> V1 içi); A,B güç r7.5, C,D bilgi r4.3
PYOL = {"A": ([(3942, 2070, -344), (3942, 2070, -390), (3936, 2070, -390), (3936, 1889, -390), (3945, 1889, -390), (3945, 1889, -808)], 7.5, "guc", 2070),
        "B": ([(3942, 2046, -344), (3942, 2046, -370), (3951, 2046, -370), (3951, 1873, -370), (3945, 1873, -370), (3945, 1873, -808)], 7.5, "guc", 2046),
        "C": ([(3966, 2070, -344), (3966, 2070, -390), (3968, 2070, -390), (3968, 1880, -390), (3968, 1880, -808)], 4.3, "veri", 2070),
        "D": ([(3966, 2046, -344), (3966, 2046, -370), (3984, 2046, -370), (3984, 1880, -370), (3984, 1880, -808)], 4.3, "veri", 2046)}
def _s(a, b, r): return (np.asarray(a, float), np.asarray(b, float), r)
EK_SEG = []
for Q, r, t, y in PYOL.values(): EK_SEG += [_s(a, b, r) for a, b in zip(Q[:-1], Q[1:])]
# üst yatay: bina 5G6 (y 2146) + zemin güç (2118) + bilgi (2118 / 2146) — mevcut düz yollar
for x, y, r in ((3940, 2146, 10), (3942, 2118, 7.5), (3966, 2118, 4.3), (3967, 2146, 4.3)): EK_SEG.append(_s((x, y, -850), (x, y, -344), r))
YOL = {}
DELIK = [("ELK_ZINCIR__kanal", 2, (3929, 1860, -788), (3997, 1900, -785), [(3936.5, 3953.5, 1864.5, 1897.5), (3963, 3989, 1875, 1885)])]
