# -*- coding: utf-8 -*-
s = open("teknik_h24.py", encoding="utf-8").read()
BS = "\\"
r = [
 ('X0, XA1, XC1, XF1, XK1, XE1 = 594.0, 1294.0,', 'X0, XA1, XC1, XF1, XK1, XE1 = 736.0, 1436.0,'),
 ('"kalkan' + BS + 'n86,5"', '"kalkan' + BS + 'n228,5"'),
 ('("K1", 656.5, 1276.5, S5, ["lahmacun"] * 5), ("K2", 1311.5, 1931.5, S5, ["lahmacun"] * 5),',
  '("K1", 798.5, 1418.5, S5, ["lahmacun"] * 5), ("K2", 1453.5, 2073.5, S5, ["lahmacun"] * 5),'),
 ('("KD", 1966.5, 2435.0, [126, 342.5, 785], ["kaşar + sucuk' + BS + 'nyedeği 2 gün", "boş"]),', ''),
 ('("K3", 2470.0, 3090.0, S4, ["pide"] * 4), ("K5", 3125.0, 3745.0, S4, ["pide", "pide", "pide", "tatlı"]),',
  '("K3", 2108.5, 2728.5, S4, ["pide"] * 4), ("K5", 2763.5, 3383.5, S4, ["pide", "pide", "pide", "tatlı"]),'),
 ('("K6", 3780.0, 4365.0, S3, ["içecek"] * 3)]',
  '("K6", 3418.5, 4003.5, S3, ["içecek"] * 3), ("KD", 4038.5, 4398.5, [126, 330, 560], ["2 · sucuk' + BS + 'nyedeği 2 gün", "1 · kaşar' + BS + 'nyedeği 2 gün"])]'),
 ('yaz(4200, 830, "teneke YOK", 7.5, R)',
  'kutu(4038.5, 4398.5, 561.5, 785, fc="#ffffff", ec=R, lw=0.9, z=3); yaz(4218, 672, "teneke + tartı' + BS + 'n(arkada)", 7.5, R)'),
 ('"TOPPING 1206"', '"TOPPING 1064"'),
 ('"HAT 4636   (v2.1: 4722,5 → −86,5)"', '"HAT 4494   (v2.1: 4722,5 → −228,5)"'),
 ('yaz(1560, 1850, "üst kat boş"', 'yaz(1630, 1850, "boş"'),
 ('yaz(1440, 1250, "TOPPING · İKİ KAT"', 'yaz(2100, 1110, "TOPPING · İKİ KAT"'),
 ('HAT v2.4 ÖNERİ', 'HAT v2.5 ÖNERİ'),
 ('üst katta yalnız 2 UNO · nozullar yan yana · çöp + teneke yok · çekmeceler sağa',
  'TOPPING sol duvarı kıymanın dibinde · kaşar / sucuk yedeği + teneke K altında · çöp yok'),
]
for a, b in r:
    assert a in s, a[:50]
    s = s.replace(a, b)
open("teknik_h25.py", "w", encoding="utf-8").write(s)
print("ok")
