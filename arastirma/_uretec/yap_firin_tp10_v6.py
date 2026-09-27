# -*- coding: utf-8 -*-
"""firin_tp10_cad_v5 → firin_tp10_cad_v6 (27 Eyl 2026): PİZZA KUTUSU YEDEĞİ TEK YERDE, FIRIN ÜSTÜ SOL (Kemal: "sola koy işte").
Raf 512 mm'lik yığın taşır: 320 kutu (51 kg) + kompresör 25 kg = 76 kg → raf 3 → 4 mm, takoz 6 → 10 (5 sıra × 2, aralık 360). Gerisi v5."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "firin_tp10_cad_v5.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


d('"""AUTOKITCH · F FIRIN · TP10 KESİTİ · 1500 · v5 (27 Eyl 2026): FIRIN 79 mm ÖNE',
  '"""AUTOKITCH · F FIRIN · TP10 KESİTİ · 1500 · v6 (27 Eyl 2026): KUTU YEDEĞİ TEK YERDE fırın üstü sol (320 kutu, raf 4 mm, 10 takoz) · v5: FIRIN 79 mm ÖNE')
d("UST_RAF_Y = (YG1 + 40.0, YG1 + 43.0)                            # 1513–1516 · fırın üstünde HAVALANDIRMALI raf (40 mm takoz + 3 mm plaka) · v4",
  "UST_RAF_Y = (YG1 + 39.0, YG1 + 43.0)                            # 1512–1516 · fırın üstünde HAVALANDIRMALI raf (39 mm takoz + 4 mm plaka) · v6: 320 kutu + kompresör = 76 kg\n"
  "TAKOZ_XZ = tuple((x_, z_) for z_ in (-30.0, -408.0) for x_ in (X_F0 + 30.0, X_F0 + 390.0, XC_TP, X_F0 + 1110.0, X_F1 - 30.0))   # v6: 10 takoz, aralık 360")
d("    for x, z in ((X_F0 + 30.0, -30.0), (XC_TP, -30.0), (X_F1 - 30.0, -30.0), (X_F0 + 30.0, -408.0), (XC_TP, -408.0), (X_F1 - 30.0, -408.0)):",
  "    for x, z in TAKOZ_XZ:", 2)
d("    TAKOZ_XZ = ((X_F0 + 30.0, -30.0), (XC_TP, -30.0), (X_F1 - 30.0, -30.0), (X_F0 + 30.0, -408.0), (XC_TP, -408.0), (X_F1 - 30.0, -408.0))",
  "    # v6: TAKOZ_XZ modül başında (10 takoz)")
d('bom=("Fırın üstü raf 3 mm", 1, "304 · 1480 × 405", "40 mm takozla gövde üstünde, yanları açık (doğal havalandırma) · altında ışınım kalkanı · kompresör 25 kg + kutular 8 kg · JUN-AIR ortam sınırı 40 °C [föy]"))',
  'bom=("Fırın üstü raf 4 mm", 1, "304 · 1480 × 405", "v6: 10 takozla (aralık 360) gövde üstünde, yanları açık (doğal havalandırma) · altında ışınım kalkanı · SOLDA pizza kutusu yedeği 320 kutu 51 kg (0,16 kg/kutu: Bekar Ambalaj 100 adet 16 kg) + SAĞDA kompresör 25 kg = 76 kg · JUN-AIR ortam sınırı 40 °C [föy]"))')
RAF_KOD = '''    # v6 · RAF YÜK HESABI: plak nokta mesnetli iç panel w = 0,00581 q a^4 / D (Timoshenko, kare panel a = büyük açıklık) · kenar panel x3 VARSAYIM
    _E, _nu, _ro, _g = 193e9, 0.29, 7930.0, 9.81
    _qk = 320 * 0.16 * _g / (0.804 * 0.404)
    for _t, _a, _ad in ((0.004, 0.378, "v6 4 mm · 10 takoz (açıklık 360 × 378)"), (0.003, 0.720, "v5 3 mm · 6 takoz (açıklık 720 × 378)")):
        _q = _qk + _ro * _g * _t; _D = _E * _t ** 3 / (12.0 * (1.0 - _nu ** 2)); _w = 0.00581 * _q * _a ** 4 / _D * 1000.0
        print("RAF SEHİM %s: yük %.0f Pa → iç panel %.2f mm · kenar ≈%.1f mm" % (_ad, _q, _w, 3.0 * _w))
    _top = 320 * 0.16 + 25.0 + 1.480 * 0.405 * 0.004 * _ro + 1.480 * 0.405 * 0.0008 * _ro
    print("RAF YÜKÜ: kutu 51,2 + kompresör 25 + raf %.1f + kalkan %.1f = %.0f kg → 10 takoz ort. %.1f kg · Ø16×1,5 boru (68 mm²) 2× yükte %.1f MPa · fırın üst sacına %.0f kg: özel sipariş şartnamesine 10 × M6 kaynak saplama + taşıma yazılacak" % (1.480 * 0.405 * 0.004 * _ro, 1.480 * 0.405 * 0.0008 * _ro, _top, _top / 10.0, 2.0 * _top / 10.0 * _g / 68.3, _top))
'''
d('    for x in (2400, 2600, 3300, 3990, 4030, 4100, 4200, 4257, 4300):',
  RAF_KOD + '    for x in (2400, 2600, 3300, 3990, 4030, 4100, 4200, 4257, 4300):')
d('bom=("Raf takozu alt Ø16 × 10", 6,', 'bom=("Raf takozu alt Ø16 × 10", 10,')
d('bom=("Raf takozu üst Ø16 × 29,2", 6,', 'bom=("Raf takozu üst Ø16 × 28,2", 10,')
for a, b in (("firin_tp10_v5.glb", "firin_tp10_v6.glb"), ('"firin_tp10_v5"', '"firin_tp10_v6"'), ('"generator": "AUTOKITCH firin_tp10_cad_v5"', '"generator": "AUTOKITCH firin_tp10_cad_v6"'),
             ('print("TP10-UZUN v5 ·', 'print("TP10-UZUN v6 ·'), ('"uzatılmış fırın · AUTOKITCH v5 (79 öne)"', '"uzatılmış fırın · AUTOKITCH v6 (79 öne, raf 4 mm)"'), ('"ana makine v51"', '"ana makine v52"')):
    assert s.count(a) >= 1, a
    s = s.replace(a, b)
io.open(os.path.join(U, "firin_tp10_cad_v6.py"), "w", encoding="utf-8").write(s)
print("firin_tp10_cad_v6.py yazildi")
