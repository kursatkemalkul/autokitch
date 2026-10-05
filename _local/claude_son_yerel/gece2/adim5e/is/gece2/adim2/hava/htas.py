# -*- coding: utf-8 -*-
"""HAVA HORTUMU KANALLARI · tasarim (tek kaynak). Her grup = birbirine dayanan eksen hizali kutular -> 304 1,2 mm kapakli kanal.
Kutular dayandigi yuzde ic kesit kadar agizla birlesir (tek surekli kanal), hortum gectigi yerde otomatik delik (r + 1,5)."""
T = 1.2
# (grup, istasyon, [ (ad, lo, hi) ... ])
GRUP = [
    # TOPPING · valf adasi A (x 1684) -> silindirler (x 1719 / 1725): hortum #4 (z -670) + #5 (z -682)
    ("TA", "TOPPING", [("dik", (1676.0, 1312.0, -694.0), (1692.0, 1641.0, -664.0)),
                       ("ust", (1676.0, 1641.0, -694.0), (1731.0, 1666.0, -664.0))]),
    # TOPPING · valf adasi B (x 2008) -> silindirler (x 2256 / 2262): hortum #12 (z -676) + #13 (z -670)
    ("TB", "TOPPING", [("alt", (2014.0, 1259.0, -683.0), (2313.0, 1308.0, -664.0)),
                       ("dik", (2291.0, 1308.0, -683.0), (2313.0, 1641.0, -664.0)),
                       ("ust", (2250.0, 1641.0, -683.0), (2313.0, 1666.0, -664.0))]),
    # TOPPING · ana besleme (regulator x 2420 -> valf adasi B): hortum #14 (r5, z -740)
    ("TC", "TOPPING", [("yatay", (2003.0, 1118.0, -747.0), (2398.0, 1132.0, -733.0)),
                       ("dik", (2003.0, 1132.0, -747.0), (2017.0, 1250.0, -733.0))]),
    # K · valf adasi -> bicak / itici silindirleri (sag duvar): hortum #23 (z -724) + #24 (z -730), r2
    ("KA", "K", [("yatay", (4085.0, 1534.0, -734.5), (4361.0, 1554.0, -718.0)),
                 ("dik", (4349.0, 1393.0, -734.5), (4361.0, 1534.0, -718.0)),
                 ("sag", (4361.0, 1393.0, -734.5), (4397.5, 1411.0, -718.0)),
                 ("alt", (4380.0, 1236.0, -734.5), (4397.5, 1393.0, -718.0))]),
    # K · valf adasi -> kesici (on): hortum #27 (y 1612, z -690) + #28 (y 1600, z -700) -> #32 / #34 z boyunca
    ("KB", "K", [("dik", (4106.0, 1520.0, -706.0), (4118.0, 1594.0, -684.0)),
                 ("yatay", (4106.0, 1594.0, -706.0), (4232.0, 1618.0, -684.0)),
                 ("boy", (4200.0, 1594.0, -684.0), (4232.0, 1618.0, -296.0)),
                 ("on", (4200.0, 1594.0, -256.0), (4232.0, 1618.0, -170.0))]),
    # F · kompresor cikisi -> pano inis kanali V1 (z -603): hortum #17 (r5)
    ("FA", "F", [("boy", (3541.5, 1801.5, -603.0), (3556.5, 1816.5, -520.0))]),
]
# kanal icinde kalan hortum kelepceleri silinir (kucuk bilesen, en buyuk olcu < 60); bu parca kanal gecisi icin centiklenir:
CENTIK = [("ELK_K__celik", (4199.0, 1461.0, -293.0), (4217.0, 1638.0, -259.0))]
# KONSOL (askı): (kutu adı "GRUP.ad", eksen, yön, [kanal boyunca konumlar]) -> kutu yüzünden ışınla en yakın yapıya 14 x 2 mm 304 lama + 14 x 14 x 2 ayak
KONSOL = [("TA.dik", 2, 1, [1400.0, 1560.0]), ("TA.ust", 2, 1, [1712.0]),
          ("TB.alt", 2, 1, [2080.0, 2200.0]), ("TB.dik", 2, 1, [1400.0, 1560.0]), ("TB.ust", 2, 1, [2282.0]),
          ("TC.yatay", 2, -1, [2060.0, 2140.0, 2220.0, 2300.0, 2380.0]), ("TC.yatay", 2, 1, [2060.0, 2140.0, 2220.0, 2300.0, 2380.0]),
          ("TC.yatay", 1, -1, [2060.0, 2140.0, 2220.0, 2300.0, 2380.0]), ("TC.dik", 2, 1, [1150.0, 1200.0, 1240.0]),
          ("FA.boy", 1, 1, [-590.0, -540.0]),
          ("KB.yatay", 2, -1, [4131.0, 4160.0]), ("KB.boy", 1, 1, [-600.0, -490.0, -380.0]), ("KB.on", 1, -1, [-200.0, -179.0])]
