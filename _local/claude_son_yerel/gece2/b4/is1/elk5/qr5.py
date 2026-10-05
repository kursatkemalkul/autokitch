# -*- coding: utf-8 -*-
"""QR iç kablolama: göz arkası 3 dik kapaklı kanal (sol: sol sütun kapak kilitleri · orta: sol sensörler + sağ kilitler · sağ: sağ sensörler),
üstte toplayıcı (TL + QZ -> mevcut tavan dağıtım kutusu; QRz -> mevcut sağ kol), KUTU besleme üst kanalı (KT1/KT2), müşteri paneli kanalı (PK + PKz)."""
IST = "QR"
def K(ad, e, lo, hi, **kw): return dict(ad=ad, e=e, lo=lo, hi=hi, ist=IST, **kw)
KAN = [K("QL", 1, (4574, 455, 674), (4599.5, 1650, 699.5)),
       K("QC", 1, (4980.5, 455, 687.5), (5003.5, 1650, 711)),
       K("QRt", 1, (5402.5, 455, 674), (5427, 1650, 699.5)),
       K("TL", 0, (4574, 1653, 674), (4980.5, 1686, 699.5)),
       K("QZ", 2, (4980.5, 1653, 674), (5003, 1688, 760)),
       K("QRz", 2, (5390, 1653, 674), (5427, 1686, 1035)),
       K("KT1", 1, (4947, 1691.5, 770), (4985, 2012, 812)),
       K("KT2", 0, (4862, 2012, 770), (4985, 2042, 812)),
       K("PKz", 2, (4950, 1656, 1080), (4980, 1686, 1108)),
       K("PK", 0, (4845, 1656, 1108), (5245, 1700, 1138))]
YOL = {}
for k, ci in enumerate((135, 136, 137, 138, 139, 140)):            # sol sütun arka kapak kilidi -> QL
    y = 642.5 + 200 * k; YOL[ci] = dict(yol=[[(4618, y, 691), (4586, y, 691)]])
for k, ci in enumerate((153, 154, 155, 156, 157, 158)):            # sol sütun kapak sensörü -> QC
    y = 463 + 200 * k; YOL[ci] = dict(yol=[[(4993.8, y, 681), (4993.8, y, 698)]])
for k, ci in enumerate((159, 160, 161, 162, 163, 164)):            # sağ sütun arka kapak kilidi -> QC
    y = 642.5 + 200 * k; YOL[ci] = dict(yol=[[(5028, y - 3.5, 691), (5028, y, 691), (4997, y, 691)]])
for k, ci in enumerate((167, 170, 173, 176, 179, 182)):            # sağ sütun kapak sensörü -> QRt
    y = 468 + 200 * k; YOL[ci] = dict(yol=[[(5397, y + 0.5, 681), (5397, y + 4, 681), (5414, y + 4, 681)]])
# KUTU besleme (zemin -> orta dik kanal -> tavan kutusu -> KT1 -> KT2 -> KUTU üst rakoru): yollar aynı, kanal içinde
import numpy as np
def _s(a, b, r): return (np.asarray(a, float), np.asarray(b, float), r)
# kanal birleşimleri (yalnız delik/uç açma için sanal parça)
EK_SEG = [_s((4587, 1600, 687), (4587, 1670, 687), 8), _s((4992, 1600, 699), (4992, 1670, 699), 8), _s((5415, 1600, 687), (5415, 1670, 687), 8),
          _s((4950, 1671, 687), (4992, 1671, 687), 8), _s((4992, 1672, 740), (4992, 1672, 780), 8), _s((5380, 1672, 1015), (5400, 1672, 1015), 8),
          _s((4965, 1671, 1070), (4965, 1671, 1120), 8)]
# müşteri paneli kabloları (yeni): (uç noktalar, r, tür)
PANEL = [([(4920, 1680, 1163), (4920, 1680, 1109.2)], 2.5, "veri"), ([(4935, 1680, 1163), (4935, 1680, 1109.2)], 3.0, "guc"),
         ([(5080, 1693, 1143), (5080, 1693, 1109.2)], 2.5, "veri"), ([(5095, 1693, 1143), (5095, 1693, 1109.2)], 3.0, "guc"),
         ([(5193, 1690, 1158.5), (5193, 1690, 1109.2)], 2.5, "veri")]
EK_SEG += [_s((4879, 2000, 783), (4879, 2030, 783), 10), _s((4880, 2000, 797), (4880, 2030, 797), 5.5)]
EK_SEG += [_s(a, b, r) for (a, b), r, _ in [((p[0], p[1]), r, t) for p, r, t in PANEL]]
DELIK = [("ELK_QR_KABLO__kanal", 2, (4980, 1654, 758), (5004, 1693, 763), [(4983, 5000, 1662, 1682)]),
         ("ELK_QR_KABLO__kanal", 0, (5387, 1654, 993), (5391, 1690, 1037), [(1663, 1681, 1003, 1027)]),
         ("ELK_QR_KABLO__kanal", 2, (4948, 1654, 1077), (4982, 1693, 1082), [(4953, 4977, 1660, 1682)])]
PLAKA = [(4576, 4597.5, 676, 697.5), (4982.5, 5001.5, 689.5, 709), (5404.5, 5425, 676, 697.5)]   # göz üst plakası (y 1650–1653) kanal geçişi
for k in KAN:
    if k["ad"] in ("QL", "QC", "QRt"): k["uc1"] = False
