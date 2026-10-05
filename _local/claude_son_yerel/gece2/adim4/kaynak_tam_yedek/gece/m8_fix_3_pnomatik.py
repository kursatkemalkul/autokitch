# -*- coding: utf-8 -*-
"""MADDE 8 · adim 3 · TOPPING valf adasi -> 4 UNO pnomatik silindiri hortumlari (O6 PU, her silindire A/B). python m8_fix_3_pnomatik.py giris.glb cikis.glb
Ada (x 1690-1998, y 1250-1310, z -760...-660): kiyma/kusbasi alt yuzden, harc sol yuzden, sos sag yuzden cikar. Silindir portlari ust yuzde:
on port z -688, arka port z -795. Spreader hava baglantisi YOK (spreader valfi soguk odada, aktuatoru modelde yok -> acik)."""
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m8kit import Glb, tup, kutu_ucgen
g = Glb(sys.argv[1]); LOG = []
def log(*a): LOG.append(" ".join(str(x) for x in a)); print(*a)
ORN = g.bul_nokta("TOPPING_MODUL__hava_ana", (2200, 1125, -740))
R = 3.0
H = {
    "kusbasi_on": [(1814, 1250, -688), (1814, 1208.9, -688)],
    "kusbasi_arka": [(1824, 1250, -750), (1824, 1225, -750), (1824, 1225, -795), (1824, 1208.5, -795)],
    "kiyma_on": [(1700, 1250, -688), (1700, 1225, -688), (1620, 1225, -688), (1620, 1209.0, -688)],
    "kiyma_arka": [(1710, 1250, -750), (1710, 1225, -750), (1710, 1225, -795), (1630, 1225, -795), (1630, 1208.5, -795)],
    "harc_on": [(1690, 1275, -670), (1530, 1275, -670), (1530, 1648, -670), (1494, 1648, -670), (1494, 1648, -688), (1494, 1632.5, -688)],
    "harc_arka": [(1690, 1290, -682), (1540, 1290, -682), (1540, 1655, -682), (1500, 1655, -682), (1500, 1655, -795), (1500, 1632.4, -795)],
    "sos_on": [(1998, 1265, -670), (2290, 1265, -670), (2290, 1648, -670), (2253, 1648, -670), (2253, 1648, -688), (2253, 1632.5, -688)],
    "sos_arka": [(1998, 1302, -676), (2280, 1302, -676), (2280, 1655, -676), (2247, 1655, -676), (2247, 1655, -795), (2247, 1632.4, -795)],
}
for k, pts in H.items():
    # silindir portunda itme-tak rakor (M5 / O6)
    x, y, z = pts[-1]
    ust = 1209.5 if y < 1400 else 1632.5          # silindir ust yuzu + 0,1
    pts = pts[:-1] + [(x, ust + 5.0, z)]
    g.ekle_dugum("TOPPING_MODUL__hava_ana", kutu_ucgen([x - 4, ust, z - 4], [x + 4, ust + 5.0, z + 4]), ornek=ORN)
    g.ekle_dugum("TOPPING_MODUL__hava_ana", tup(pts, R, 10), ornek=ORN)
    log("hortum", k, len(pts))
g.kaydet(sys.argv[2]); log("kaydedildi", sys.argv[2])
open(os.path.splitext(sys.argv[2])[0] + "_log.txt", "w", encoding="utf-8").write("\n".join(LOG))
