# -*- coding: utf-8 -*-
"""m7 ölçü kaynağı — TOPPING UNO / kaset yeni yerleşimi (Kemal 2 Eki gece, madde 7). Bütün betikler buradan okur."""
# ---- birim ötelemeleri (x, mm) · eski merkez → yeni merkez
DX = {"kiyma": 28.5,      # hazne 1501–1691 → 1529,5–1719,5  (merkez 1596 → 1624,5) · sol hortuma 11,5
      "kusbasi": 12.5,    # hazne 1711–1901 → 1723,5–1913,5  (merkez 1806 → 1818,5)
      "kasar": 0.0,       # kılavuz 1917,5–2206,5 AYNI (düşme 2062) · motorları evaporatör tahliye hortumuna değmesin diye yerinde
      "sucuk": 44.5,      # kılavuz 2236,5–2385,5 → 2281–2430 (düşme 2311 → 2355,5)
      "harc": -693.0,     # BÜYÜK UNO (380) 2190 → 1497 · solda, sol hortum boşluğunun üstünde (silindiri kuru bölmedeki sürücü kablo kanalına 6,6 mm)
      "sos": 605.0}       # KÜÇÜK UNO (220) 1645 → 2250 · sağda, sağ hortum boşluğunun üstünde
X_L, X_R = 1497.0, 2250.0          # hortum (D32, dış Ø42) eksenleri · z −170 · boşluk 62 (42 + 2×10)
Z_H = -170.0
# ---- soğuk oda sol cebi (A'nın içine; A dış ölçüsü / yeri / açıcı değişmez)
DELTA = 199.0                      # astar sol yüzü 1495 → 1296 (büyük huni 1307–1687, astara 10 mm)
LIN_X0 = 1495.0 - DELTA            # 1296 astar dış · 1297 iç
X_O = LIN_X0 - 57.5 - 1.5          # 1237 cep dış sacı (sol) · PU 1238,5–1296
CEP_Y1 = 2167.5                    # cep üst sac üstü (A çerçeve üst rayı 2168,5)
CEP_ZF = 26.5                      # cep ön sac önü (A çerçeve ön dikmesi 29)
CEP_LIN_ZF = -14.0                 # cep astarı ön yüzü (dış) · ön PU −14…25
# ---- kaset dili kanalları (ön çerçeve / eşik / raf) · eski + öteleme
YARIK_X = [(2030.5 + DX["kasar"], 2093.5 + DX["kasar"]), (2279.5 + DX["sucuk"], 2342.5 + DX["sucuk"])]
