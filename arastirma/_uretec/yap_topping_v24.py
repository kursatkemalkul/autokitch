# -*- coding: utf-8 -*-
"""topping_cad_v23 → topping_cad_v24 (26 Eyl 2026 gece) · TOPPING TEKNESİ MODÜLÜN İÇİNDE BİTER (2500'ü geçmez)
Kemal: "kısalırsa kısalt, yoksa bırak". Ölçüldü (v23): mekanizma teknesi + 3 kiriş x ≤ 1885 (dünya 2585), X motoru ≤ 1863, kaidesi ≤ 1880,
sağ uç tamponu 1870, bağlama laması 1850, sağ kasnak 1835 → F fırınına 85 mm giriyordu (v47'de zon muafiyeti gizliyordu).
ÇÖZÜM (v24): X tahriki UÇ DEĞİŞTİRDİ — motor + tahrik kasnağı SOL uca (x −560, park tarafı; sol enerji zinciri kanalının 11 mm solunda),
avara + gergi SAĞ uca (x 1650). Kayış kelepçeleri arabanın SOL yarısına (Xc −130 · Xc −50): aktarmada (Xc 1637) kelepçe 1607'de biter,
avara 1650'de → tekne, kirişler ve kayış kirişi 1795'te biter (duvar 1798,5). Sağ tampon kayış koluna vurur (1617–1629, limit Xc 1650 = aktarma + 13);
limit+ sensörü 1660 → 1647. Bağlama laması 1810 → 1745. Tekne solda −600'e uzadı (motor için). Kayış 4800 → 4480.
Sağ dış saca hava hattı rakor deliği Ø14 (kompresör fırın üstünde, hat y 2000 / z −415'ten girer)."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_cad_v23.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)


d('URETIM = None   # v23: üretim klasörü YOK (kural 6.7)', '''URETIM = None   # v23: üretim klasörü YOK (kural 6.7)
XK_SOL, XK_SAG = -560.0, 1650.0   # v24: X kayışı kasnak merkezleri (motor SOLDA, avara SAĞDA) — H.KAYIS_SOL/SAG yerine


def silx(y, z, r, x0, x1):
    """v24: x boyunca silindir"""
    return cq.Workplane("YZ", origin=(min(x0, x1), y, z)).circle(r).extrude(abs(x1 - x0))''')
# tekne + kirişler: sağda 1795'te biter, solda −600
d('    _TX0, _TX1 = H.KAYIS_SOL - 20.0, H.KAYIS_SAG + 50.0', '    _TX0, _TX1 = XK_SOL - 40.0, 1795.0                                     # v24: tekne modülün içinde biter (duvar 1798,5); solda motor cebi')
d('    tk = tk.cut(kut(H.KAYIS_SAG - 34.0, H.KAYIS_SAG + 34.0, 0.5, 33.0, -416.0, -411.0))', '    tk = tk.cut(kut(XK_SOL - 34.0, XK_SOL + 34.0, 0.5, 33.0, -416.0, -411.0))    # v24: motor servis cebi SOL uçta')
d('    for i_, xb in enumerate((-520.0, -220.0, 80.0, 380.0, 680.0, 980.0, 1280.0, 1580.0, 1810.0)):', '    for i_, xb in enumerate((-520.0, -220.0, 80.0, 380.0, 680.0, 980.0, 1280.0, 1580.0, 1745.0)):   # v24: son lama 1745')
d('''bom=("Kayış kirişi 50 × 16 × 1680", 1, "304 lama", "kayış kasnakları, avara ve gergi bunun üstünde"))''',
  '''bom=("Kayış kirişi 50 × 16 × %.0f" % (_TX1 - _TX0), 1, "304 lama", "kayış kasnakları, avara ve gergi bunun üstünde · v24: modül içinde biter"))''')
# X tahriki: motor sola, avara sağa
d('    _KL, _KR, _KY, _KRAD = H.KAYIS_SOL, H.KAYIS_SAG, 33.0, H.KASNAK_R', '    _KL, _KR, _KY, _KRAD = XK_SOL, XK_SAG, 33.0, H.KASNAK_R                  # v24: −560 / 1650')
d('    ekle("x_tahrik_kasnagi", silz(_KR, _KY, _KRAD, -367.5, -352.5).cut(silz(_KR, _KY, 4.1, -369.0, -351.0)), "celik",',
  '    ekle("x_tahrik_kasnagi", silz(_KL, _KY, _KRAD, -367.5, -352.5).cut(silz(_KL, _KY, 4.1, -369.0, -351.0)), "celik",')
d('    _mg = nema23()["govde"].translate(cq.Vector(_KR, _KY, _mot_yuz))', '    _mg = nema23()["govde"].translate(cq.Vector(_KL, _KY, _mot_yuz))         # v24: motor SOL uçta (park tarafı)')
d('    ekle("x_motor_mili", silz(_KR, _KY, 4.0, _mot_yuz, -352.5), "celik",', '    ekle("x_motor_mili", silz(_KL, _KY, 4.0, _mot_yuz, -352.5), "celik",')
d('    _mk = kut(_KR - 45.0, _KR + 45.0, 4.5, 75.0, _mot_yuz, _mot_yuz + 8.0).cut(silz(_KR, _KY, 20.0, _mot_yuz - 1.0, _mot_yuz + 9.0))',
  '    _mk = kut(_KL - 45.0, _KL + 45.0, 4.5, 75.0, _mot_yuz, _mot_yuz + 8.0).cut(silz(_KL, _KY, 20.0, _mot_yuz - 1.0, _mot_yuz + 9.0))')
d('    ekle("avara_kasnak", silz(_KL, _KY, _KRAD, -367.5, -352.5).cut(silz(_KL, _KY, 4.1, -369.0, -351.0)), "celik",',
  '    ekle("avara_kasnak", silz(_KR, _KY, _KRAD, -367.5, -352.5).cut(silz(_KR, _KY, 4.1, -369.0, -351.0)), "celik",')
d('''         bom=("Avara kasnak GT3 20 dis x 15", 1, "flansli - icinde 2 x 625-2RS paslanmaz rulman", "sol ucta; park arabasinin disinda"))''',
  '''         bom=("Avara kasnak GT3 20 dis x 15", 1, "flansli - icinde 2 x 625-2RS paslanmaz rulman", "v24: SAĞ uçta (1650); aktarmada kelepçe 1607'de biter"))''')
d('    _agb = kut(_KL - 22.0, _KL + 22.0, 20.5, 50.0, -385.0, -377.0).cut(silz(_KL, _KY, 4.2, -386.0, -376.0))',
  '    _agb = kut(_KR - 22.0, _KR + 22.0, 20.5, 50.0, -385.0, -377.0).cut(silz(_KR, _KY, 4.2, -386.0, -376.0))')
d('    ekle("avara_mili", silz(_KL, _KY, 4.0, -385.0, -352.5), "celik",', '    ekle("avara_mili", silz(_KR, _KY, 4.0, -385.0, -352.5), "celik",')
d('''             bom=("X kayisi GT3-15 kapali cevrim %.0f mm" % H.KAYIS_UZUNLUK, 1,''', '''             bom=("X kayisi GT3-15 kapali cevrim %.0f mm" % (2.0 * (XK_SAG - XK_SOL) + H.KASNAK_CEVRE), 1,''')
# kayış kolu + kelepçeler arabanın sol yarısında
d('    kol = kut(Xc - 150.0, Xc + 150.0, _yc + 4.5, _yc + 14.5, -385.0, -315.0).union(kut(Xc - 20.0, Xc + 20.0, _yc + _bt / 2.0 + 0.5, _yc + 4.5, -367.5, -352.5))',
  '    kol = kut(Xc - 150.0, Xc - 30.0, _yc + 4.5, _yc + 14.5, -385.0, -315.0).union(kut(Xc - 110.0, Xc - 70.0, _yc + _bt / 2.0 + 0.5, _yc + 4.5, -367.5, -352.5))   # v24: plakanın SOL yarısı')
d('''    ekle("kayis_kolu", kol, "celik", bom=("Kayis kolu - L", 1, "304 10 mm bukme - plakaya 4 x M8 + O6 pim", "ust kayis kosusunu araba plakasina baglar"))
    for i_, xb in enumerate((Xc - 140.0, Xc + 140.0)):''',
  '''    ekle("kayis_kolu", kol, "celik", bom=("Kayis kolu - L", 1, "304 10 mm bukme - plakaya 4 x M8 + O6 pim", "ust kayis kosusunu araba plakasina baglar · v24: 120 boy, plakanın sol yarısında (sağ uç 2500'ü geçmesin)"))
    for i_, xb in enumerate((Xc - 130.0, Xc - 50.0)):''')
# sensör + tamponlar
d('    for ad_, xb in (("home", H.X_PARK), ("limit_sol", H.X_LIMIT_SOL), ("limit_sag", H.X_LIMIT_SAG)):', '    for ad_, xb in (("home", H.X_PARK), ("limit_sol", H.X_LIMIT_SOL), ("limit_sag", 1647.0)):            # v24: limit+ 1647 (tampon 1650)')
d('''"home %.0f - limit- %.0f - limit+ %.0f" % (H.X_PARK, H.X_LIMIT_SOL, H.X_LIMIT_SAG)) if ad_ == "home" else None)''',
  '''"home %.0f - limit- %.0f - limit+ %.0f" % (H.X_PARK, H.X_LIMIT_SOL, 1647.0)) if ad_ == "home" else None)''')
d('''    for i_, xb in enumerate((H.X_LIMIT_SOL - 200.0, H.X_LIMIT_SAG + 200.0)):
        ekle("uc_tamponu_%d" % i_, silz(xb, 53.5, 10.0, -80.0, -65.0), "silikon",
             bom=("Uç tamponu Ø20 × 15", 2, "poliüretan + 304 braket", "ARABA PLAKASINA çarpar, bloklara değil") if i_ == 0 else None)''',
  '''    ekle("uc_tamponu_0", silz(H.X_LIMIT_SOL - 200.0, 53.5, 10.0, -80.0, -65.0), "silikon",
         bom=("Uç tamponu Ø20 × 15 (sol)", 1, "poliüretan + 304 braket", "ARABA PLAKASINA çarpar, bloklara değil"))
    # v24: SAĞ tampon kayış KOLUNA vurur (kol aktarmada 1607'de biter; tampon 1617–1629 → sert limit Xc 1650 = aktarma + 13)
    ekle("uc_tamponu_1", silx(_yc + 9.5, -372.5, 5.0, 1617.0, 1629.0), "silikon",
         bom=("Uç tamponu Ø10 × 12 (sağ)", 1, "poliüretan", "kayış KOLUNA vurur (kol y 48–58, kayışın üstünde) · gergi braketinin önündeki plakada · tekne 1795'te bittiği için plaka tamponu sığmadı"))
    ekle("uc_tamponu_plakasi", kut(1629.0, 1632.0, 45.0, 62.0, -376.0, -366.0), "celik",
         bom=("Tampon plakası 3 × 17 × 10", 1, "304 · gergi braketinin ön yüzüne kaynak", "kayış düzleminin (y ≤ 44) üstünde"))''')
# dış sağ sac: hava hattı rakor deliği (kompresör fırın üstünde → hat y 2000 / z −415)
d('''        _ys = _ys.cut(kut(x - 1.0, x + SAC + 1.0, 1.0, 66.0, -510.0, -1.0))   # mekanizma gecisi''',
  '''        _ys = _ys.cut(kut(x - 1.0, x + SAC + 1.0, 1.0, 66.0, -510.0, -1.0))   # mekanizma gecisi
        if s == "sag":
            _ys = _ys.cut(silx(940.0, -415.0, 7.0, x - 1.0, x + SAC + 1.0))     # v24: hava ana hattı rakoru Ø14 (kompresör fırın üstünde)''')
# zarf denetimi: sol uçta motor
d('    _zx0, _zx1 = min(H.KAYIS_SOL - 20.0, H.X_LIMIT_SOL - 220.0), 2245.0', '    _zx0, _zx1 = min(XK_SOL - 46.0, H.X_LIMIT_SOL - 220.0), 2245.0                  # v24: motor sol uçta (kaide −605)')
# başlık
d('URETIM = None   # v23', 'URETIM = None   # v24/v23', 1)
s = s.replace('"""', '"""v24 (26 Eyl 2026 gece): TOPPING TEKNESİ MODÜL İÇİNDE BİTER — X motoru + tahrik kasnağı SOL uca (−560), avara + gergi SAĞ uca (1650),\n'
              '  kayış kelepçeleri arabanın sol yarısına (Xc −130 · −50); tekne/kirişler −600…1795 (v23: −555…1885, F fırınına 85 mm giriyordu).\n'
              '  Sağ tampon kayış koluna (1617–1629), limit+ 1647, bağlama laması 1745, kayış 4480. Sağ dış saca hava rakor deliği. Önceki: topping_cad_v23.py\n', 1)
io.open(os.path.join(U, "topping_cad_v24.py"), "w", encoding="utf-8").write(s)
print("topping_cad_v24.py yazildi")
