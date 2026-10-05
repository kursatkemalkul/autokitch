# -*- coding: utf-8 -*-
s = open("teknik_h25.py", encoding="utf-8").read()
BS = "\\"
r = [
 ('for xc in (1880.0, 2215.0):', 'for xc in (1610.0, 1960.0):'),
 ('hazne(1880.0, 220.0, 1707.0, 285.0, 130.0); hazne(2215.0, 440.0, 1707.0, 380.0, 190.0)',
  'hazne(1610.0, 220.0, 1707.0, 285.0, 130.0); hazne(1960.0, 440.0, 1707.0, 380.0, 190.0)'),
 ('yaz(1880, 1935, "sos', 'yaz(1610, 1935, "sos'),
 ('yaz(2215, 2030, "harç', 'yaz(1960, 2030, "harç'),
 ('yaz(1630, 1850, "boş", 9, G)', 'yaz(2310, 1850, "boş", 9, G)'),
 ('ax.plot([1880, 1880, 1930, 1930], [1612, 1560, 1520, 1050]',
  'ax.plot([1610, 1610, 1520, 1520, 1396, 1396], [1612, 1560, 1520, 1125, 1125, 1050]'),
 ('ax.plot([2215, 2215, 2160, 2160], [1612, 1560, 1520, 1050]',
  'ax.plot([1960, 1960, 1545, 1545, 1466, 1466], [1612, 1560, 1520, 1110, 1110, 1050]'),
 ('(1930, YS, "sos"), (2062, "#8a6a2a", "kaşar"), (2160, YS, "harç")',
  '(1396, YS, "sos"), (1466, YS, "harç"), (2062, "#8a6a2a", "kaşar")'),
 ('HAT v2.5 ÖNERİ · ÖN GÖRÜNÜŞ', 'HAT v2.6 ÖNERİ · ÖN GÖRÜNÜŞ'),
 ('TOPPING sol duvarı kıymanın dibinde', 'sos + harç solda (yayıcılar kıymadan önce) · fırın altı ısı boşluğu 668–788'),
 ('ax.plot([XF1, XF1], [Y_PL, Y_DUZ], color=G, lw=0.7, ls=":")',
  'ax.plot([XF1, XF1], [Y_PL, Y_DUZ], color=G, lw=0.7, ls=":")\n'
  'kutu(XC1, XF1, 668, 788, fc="#ffe9d6", ec=R, lw=0.9, ls="--", z=7, hatch="..")\n'
  'yaz(3250, 728, "fırın altı ısı boşluğu 120 (PU 60 + ışınım sacı + hava) · çekmece tavanı 668", 7.5, R, z=10)'),
]
for a, b in r:
    assert a in s, a[:50]
    s = s.replace(a, b)
open("teknik_h26.py", "w", encoding="utf-8").write(s)
print("ok")
