# -*- coding: utf-8 -*-
"""itici_cad_v1 → itici_cad_v2 (26 Eyl 2026 gece, montaj v49 itici denetimi bulguları):
 1 · MAKARA + KALDIRMA PİMİ −w TARAFINA (w = eksen − 37 = −79): +w'deyken inik link'in alt uzantısı ve makara (y 1217/1218) sucuk iniş
     borusunun altından (1216) geçerken 1–2 mm giriyordu (s 100–140), makara tabla boş sensörüne değiyordu (s 160), pim braketi ön fitili
     kesiyordu. −w tarafı: link uzantısı ve makara sucuk borusunun 35 mm gerisinden geçer; pim braketi fitilin 55 mm gerisinde.
 2 · Link ana plakası wa−16…wa+10, kulaklar wa−19…−16 ve wa+10…+13, taban wa−19…wa+15; pivot pimi 4 × 35, dayama 3 × 32 aynı.
 3 · Denetim: obstacle listesine sucuk borusu için 'alt uzantı geçişi' ORTA yerine s 100/120/140/160 konumları da eklendi (inik).
 Kalan gerçek: silindir gövdesi ve kirişin sol ucu soğuk odanın ön düzlemini (fitil −104…−98) keser → TU v8'de fitil alt şeridine 130 mm boşluk
 (ön kapak yok — Kemal); kapak istenirse itici hattı çözülmeli."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "itici_cad_v1.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


d('"""AKTARMA İTİCİSİ v1 · itici_cad_v1 · 26 Eyl 2026 gece (Kemal: "itici tasarımını yap")',
  '"""AKTARMA İTİCİSİ v2 · itici_cad_v2 · 26 Eyl 2026 gece (v1 + montaj v49 bulguları: makara/kaldırma pimi −w tarafına, link 26 geniş simetrik)\nv1 (Kemal: "itici tasarımını yap")')
d("MAKARA = dict(s=-7.5, y=1214.0, r=4.0, w=37.0)   # POM makara Ø8 × 8: link'in −s yüzünde, +w'de (w = wa+37 = −5: kızak gövdesinin/tablanın dışında); altı 1210",
  "MAKARA = dict(s=-7.5, y=1214.0, r=4.0, w=-37.0)  # v2: POM makara Ø8 × 8: link'in −s yüzünde, −w'de (w = wa−37 = −79: gövdenin/tablanın dışında, sucuk borusunun gerisinde); altı 1210")
# pim braketi −w tarafında (kirişin −w kenarından makara w'sinin 10 ötesine)
d('yerel(kut(PIM_KALDIRMA_S - 12.0, PIM_KALDIRMA_S + 12.0, TAVAN - 6.0, TAVAN, wa + MY["NW"] / 2.0, wa + MAKARA["w"] + 10.0))',
  'yerel(kut(PIM_KALDIRMA_S - 12.0, PIM_KALDIRMA_S + 12.0, TAVAN - 6.0, TAVAN, wa + MAKARA["w"] - 10.0, wa - MY["NW"] / 2.0))')
d('bom=("Kaldırma pimi braketi 6 mm", 1, "304 · 24 × %.0f" % (MAKARA["w"] + 10.0 - MY["NW"] / 2.0 + 0.5), "kirişin +w kenarına kaynak · pim M8 dişle · ev ucunda (her iki borudan uzak)")',
  'bom=("Kaldırma pimi braketi 6 mm", 1, "304 · 24 × %.0f" % (-MAKARA["w"] + 10.0 - MY["NW"] / 2.0), "kirişin −w kenarına kaynak · pim M8 dişle · ev ucunda (borulardan ve fitilden uzak)")')
# pivot braketi: taban wa−19…wa+15, kulaklar wa−19…−16 ve wa+10…+13
d('''    ekle("pivot_braketi", yerel(kut(sa - 30.0, sa + 30.0, Y_TABLA_YUZ - 3.0, Y_TABLA_YUZ, wa - 15.0, wa + 19.0)
                                .union(kut(sa - 12.0, sa + 6.0, PIVOT_Y - 5.0, Y_TABLA_YUZ, wa - 13.0, wa - 10.0))
                                .union(kut(sa - 12.0, sa + 6.0, PIVOT_Y - 5.0, Y_TABLA_YUZ, wa + 16.0, wa + 19.0))''',
  '''    ekle("pivot_braketi", yerel(kut(sa - 30.0, sa + 30.0, Y_TABLA_YUZ - 3.0, Y_TABLA_YUZ, wa - 19.0, wa + 15.0)
                                .union(kut(sa - 12.0, sa + 6.0, PIVOT_Y - 5.0, Y_TABLA_YUZ, wa - 19.0, wa - 16.0))
                                .union(kut(sa - 12.0, sa + 6.0, PIVOT_Y - 5.0, Y_TABLA_YUZ, wa + 10.0, wa + 13.0))''')
d('    ekle("pivot_pimi", yerel(silz(sa, PIVOT_Y, 2.0, wa - 15.0, wa + 20.0)), "celik", "C_ITICI", "ARABA", kaynak="K",',
  '    ekle("pivot_pimi", yerel(silz(sa, PIVOT_Y, 2.0, wa - 20.0, wa + 15.0)), "celik", "C_ITICI", "ARABA", kaynak="K",')
d('    ekle("dayama_pimi", yerel(silz(sa + STOP_S, PIVOT_Y - 4.0, 1.5, wa - 13.0, wa + 19.0)), "celik", "C_ITICI", "ARABA", kaynak="K",',
  '    ekle("dayama_pimi", yerel(silz(sa + STOP_S, PIVOT_Y - 4.0, 1.5, wa - 19.0, wa + 13.0)), "celik", "C_ITICI", "ARABA", kaynak="K",')
# link: ana plaka wa−16…wa+10, alt uzantı −w'ye (wa−16 → mw+4), burç borusu, makara kulağı (mw+4…mw+7), makara aksı mw−4…mw+8
d('''    link = kut(sa - 3.0, sa, BAR_Y1, PIVOT_Y + 4.0, wa - 10.0, wa + 16.0)                                    # ana plaka 26 geniş (kulakların arasında)
    link = link.union(kut(sa - 3.0, sa, BAR_Y1, PIVOT_Y - 7.0, wa + 16.0, mw - 4.0))                         # alt uzantı: +w kulağının ALTINDAN makara kulağına (1217'ye kadar)
    link = link.union(silz(sa - 1.5, PIVOT_Y, 5.0, wa - 10.0, wa + 16.0)).cut(silz(sa - 1.5, PIVOT_Y, 2.75, wa - 12.0, wa + 18.0))   # burç borusu Ø10 × 26, delik Ø5,5''',
  '''    link = kut(sa - 3.0, sa, BAR_Y1, PIVOT_Y + 4.0, wa - 16.0, wa + 10.0)                                    # ana plaka 26 geniş (kulakların arasında)
    link = link.union(kut(sa - 3.0, sa, BAR_Y1, PIVOT_Y - 7.0, mw + 4.0, wa - 16.0))                         # v2: alt uzantı −w'ye, −w kulağının ALTINDAN makara kulağına (1217'ye kadar)
    link = link.union(silz(sa - 1.5, PIVOT_Y, 5.0, wa - 16.0, wa + 10.0)).cut(silz(sa - 1.5, PIVOT_Y, 2.75, wa - 18.0, wa + 12.0))   # burç borusu Ø10 × 26, delik Ø5,5''')
d('''    mak_kulak = kut(sa - 12.0, sa - 3.0, MAKARA["y"] - 6.0, MAKARA["y"] + 4.0, mw - 7.0, mw - 4.0)         # makara kulağı 3 mm (−s yüzünden çıkar)''',
  '''    mak_kulak = kut(sa - 12.0, sa - 3.0, MAKARA["y"] - 6.0, MAKARA["y"] + 4.0, mw + 4.0, mw + 7.0)         # v2: makara kulağı 3 mm (−s yüzünden çıkar, makaranın +w yanında)''')
d('''    burc = silz(sa - 1.5, PIVOT_Y, 2.75, wa - 10.0, wa + 16.0).cut(silz(sa - 1.5, PIVOT_Y, 2.05, wa - 11.0, wa + 17.0))''',
  '''    burc = silz(sa - 1.5, PIVOT_Y, 2.75, wa - 16.0, wa + 10.0).cut(silz(sa - 1.5, PIVOT_Y, 2.05, wa - 17.0, wa + 11.0))''')
d('''    mak_pim = silz(sa + MAKARA["s"], MAKARA["y"], 1.5, mw - 8.0, mw + 4.0)''', '''    mak_pim = silz(sa + MAKARA["s"], MAKARA["y"], 1.5, mw - 4.0, mw + 8.0)''')
# denetim: inik çubukla s 100…160 konumları da boruları/sensör mesafesine girsin
d('''    for s_, kal, ad in ((S_HOME, True, "EV (kalkık)"), (S_HOME, False, "EV (çubuk inik)"), (S_END, False, "SON (itme bitti)"), ((S_HOME + S_END) / 2.0, False, "ORTA")):''',
  '''    for s_, kal, ad in ((S_HOME, True, "EV (kalkık)"), (S_HOME, False, "EV (çubuk inik)"), (S_END, False, "SON (itme bitti)"), ((S_HOME + S_END) / 2.0, False, "ORTA"),
                        (100.0, False, "s 100 (sucuk borusu altı)"), (120.0, False, "s 120"), (140.0, False, "s 140"), (160.0, False, "s 160 (sensör)")):''')
s = s.replace("itici_cad_v1", "itici_cad_v2")
io.open(os.path.join(U, "itici_cad_v2.py"), "w", encoding="utf-8").write(s)
print("itici_cad_v2.py yazildi")
