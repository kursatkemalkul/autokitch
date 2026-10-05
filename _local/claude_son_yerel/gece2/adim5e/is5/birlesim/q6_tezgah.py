# -*- coding: utf-8 -*-
"""q6 · TEZGÂH (iş 2). Tarama (kapaklar gizli, havada parça): yalnız 1 bulgu — çekmece kilidinin dili (3×26×16 çelik, x 3878–3881)
yalnız kilit gövdesine (kpk) bağlı, kendisi kpk'sız → çekmece önü gizlenince havada kalıyordu. Kilit dili çekmeceye aittir → kpk.
Bulaşık + evye yerleri / ölçüleri, gövde sacı DEĞİŞMEDİ (gövde tek kabuk: açık PU yok, havada parça yok; batarya + poşet rulosu
m8_fix_5'te oturtulmuştu, tarama temiz).
python q6_tezgah.py giris.glb cikis.glb"""
import sys
from qlib import *
gi, go = sys.argv[1:3]
G = m8kit.Glb(gi)
p, m, et = bilesen(G, "TEZGAH_CEKMECE__celik", (3878.0, 840.0, 1272.0), (3881.0, 866.0, 1288.0), tol=0.3)
tri = np.where(m)[0]
G.kpk_yaz(dict(parca=[(p, tri)]), True)
print("  kilit dili kpk:", len(tri)); G.kaydet(go); print("yazildi", go)
