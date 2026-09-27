# -*- coding: utf-8 -*-
"""kesme_cad_v2 → kesme_cad_v3 (27 Eyl 2026): YAĞ TANKI + PANO YUKARIDA, TABAN BOŞ (Kemal: "kesme spreydeki yağ ve panoyu yukarıya taşı, hava
yazan yere, orada yer vardır" + "kesme bölümünün en altında neden kutular var, ... oradan sil").
Tank 3 L: taban dolabı (y 665–945) → köprü kirişinin arkası, sol arka (y 1640–1920, x 60–220, z −620…−460); rafı sol duvara L köşebentle.
Pano (S7-1200 · PNOZ · PWM · NDR-240 × 2 · STP-DRV · klemens): arka duvar y 660–1045 → 1640–2025 (aynı x 300–565).
Isıtmalı hortum ve tank hava hortumu yeni yoldan (tank → üst → kafa / valf adası). Taban dolabı: içecek kolileri + ayırıcı KALKTI (boş)."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "kesme_cad_v2.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


NL = chr(10)
DY = 980.0                                                   # pano kayması 660 → 1640
d('"""AUTOKITCH · K · KESME + TEREYAĞI SPREYİ İSTASYONU — ÜRETİM MODELİ v2 (27 Eyl 2026)',
  '"""AUTOKITCH · K · KESME + TEREYAĞI SPREYİ İSTASYONU — ÜRETİM MODELİ v3 (27 Eyl 2026): yağ tankı + pano YUKARIDA (köprünün arkası), taban dolabı BOŞ (içecek kolileri fırın üstüne) — Kemal. Önceki: kesme_cad_v2.py' + NL + 'v2 (27 Eyl 2026)')
d('TANK = dict(x=140.0, z=-540.0, r=80.0, y0=665.0, y1=945.0)', 'TANK = dict(x=140.0, z=-540.0, r=80.0, y0=1640.0, y1=1920.0)   # v3: köprü kirişinin arkası (Y_KIRIS üstü 1627,5 + 12,5)')
d('    ekle("yag_tanki_rafi", kut(40.0, 290.0, y0 - 5.0, y0, -700.0, -380.0), "sac")',
  '    ekle("yag_tanki_rafi", kut(34.0, 290.0, y0 - 5.0, y0, -760.0, -380.0), "sac", bom=("Tank rafı 304 · 5 mm", 1, "256 × 380", "v3: sol duvara köşebentle · hava besleme hortumunun (z −800) önünde biter"))' + NL +
  '    ekle("yag_tanki_rafi_koseben", kut(2.0, 34.0, y0 - 35.0, y0 - 5.0, -760.0, -380.0).cut(kut(5.0, 35.0, y0 - 36.0, y0 - 8.0, -761.0, -379.0)), "sac",' + NL +
  '         bom=("Köşebent 30 × 30 × 3 AISI 304 (tank rafı)", 1, "boy 380", "sol duvara M6 × 3"))')
d('''    ekle("isitmali_hortum_Ø6", boru([(x, y1 + 14.0, z), (x, 1030.0, z), (230.0, 1030.0, -780.0), (230.0, 1500.0, -780.0), (440.0, 1500.0, -780.0),
                                      (440.0, Y_KIRIS[1] + 20.0, -500.0), (440.0, Y_KIRIS[1] + 20.0, ZC), (440.0, Y_ON_PL[1] + 35.0 + STROK * 0.0 + 1.0, ZC)], 5.0), "hortum_isi",''',
  '''    ekle("isitmali_hortum_Ø6", boru([(x, y1 + 14.0, z), (x, 1960.0, z), (x, 1960.0, -500.0), (440.0, 1960.0, -500.0),
                                      (440.0, Y_KIRIS[1] + 20.0, -500.0), (440.0, Y_KIRIS[1] + 20.0, ZC), (440.0, Y_ON_PL[1] + 35.0 + STROK * 0.0 + 1.0, ZC)], 5.0), "hortum_isi",''')
d('''    ekle("hava_hortumu_tank", boru([(x + 45.0, y1 + 60.0, z), (x + 45.0, 1015.0, z), (x + 45.0, 1015.0, -700.0), (230.0, 1015.0, -700.0), (230.0, 1015.0, -758.0)], 3.0), "hava")''',
  '''    ekle("hava_hortumu_tank", boru([(x + 45.0, y1 + 60.0, z), (x + 45.0, 1995.0, z), (x + 45.0, 1995.0, -760.0), (x + 45.0, 1785.0, -760.0)], 3.0), "hava")''')
# pano: y + 980
for a in ('kut(300.0, 565.0, 660.0, 1045.0, -826.0, -822.0)', 'kut(315.0, 425.0, 667.5, 767.5, zd, zd + 75.0)', 'kut(429.0, 474.0, 667.5, 767.5, zd, zd + 75.0)',
          'kut(478.0, 500.0, 667.5, 767.5, zd, zd + 90.0)', 'kut(504.0, 530.0, 667.5, 767.5, zd, zd + 60.0)', 'kut(533.0, 560.0, 667.5, 767.5, zd, zd + 70.0)',
          'kut(508.0, 560.0, 880.0, 925.0, zd, zd + 45.0)', 'kut(305.0, 560.0, 1000.0, 1040.0, -822.0, -797.0)'):
    import re
    nums = re.findall(r"[-\d.]+", a)
    y0, y1 = float(nums[2]), float(nums[3])
    b = a.replace("%s, %s" % (nums[2], nums[3]), "%.1f, %.1f" % (y0 + DY, y1 + DY), 1)
    d(a, b)
d('    for i, y in enumerate((700.0, 880.0)):', '    for i, y in enumerate((1680.0, 1860.0)):                                           # v3: pano yukarıda (+980)')
d('TC.din_parca(TC.GUC_STEP, 315.0, 850.0, zd + 122.8)', 'TC.din_parca(TC.GUC_STEP, 315.0, 1830.0, zd + 122.8)')
d('TC.din_parca(TC.SURUCU_STEP, 450.0, 880.0, zd + 28.0)', 'TC.din_parca(TC.SURUCU_STEP, 450.0, 1860.0, zd + 28.0)')
d('TC.din_parca(TC.GUC_STEP, 382.0, 850.0, zd + 122.8)', 'TC.din_parca(TC.GUC_STEP, 382.0, 1830.0, zd + 122.8)')
d('ekle("hava_hortumu_kesici", boru([(190.0, 1780.0, -790.0), (190.0, 1800.0, -790.0), (205.0, 1800.0, -790.0), (205.0, 1800.0, ZC + 20.0),',
  'ekle("hava_hortumu_kesici", boru([(190.0, 1780.0, -790.0), (190.0, 2000.0, -790.0), (205.0, 2000.0, -790.0), (205.0, 2000.0, ZC + 20.0),')   # v3: tankın üstünden
# taban boş
i0 = s.index("def taban():"); i1 = s.index("# ---------------------------------------------------------------- 8 · ÜRÜN + REFERANSLAR")
s = s[:i0] + 'def taban():\n    """v3: taban dolabı BOŞ — içecek yedeği fırın üstüne (montaj v54), tank + pano yukarıda (Kemal 27 Eyl)"""\n    return\n\n\n' + s[i1:]
# izinli temaslar
d('("yag_tanki_rafi", "yag_tanki"),', '("yag_tanki_rafi", "yag_tanki"), ("yag_tanki_rafi_koseben", "sol_sac"), ("yag_tanki_rafi_koseben", "yag_tanki_rafi"),')
for a, b in (('print("DENETİM (kesme_cad_v2)")', 'print("DENETİM (kesme_cad_v3)")'), ('print("K KESME + SPREY v2 (on kapak yok): %d parca', 'print("K KESME + SPREY v3 (tank + pano yukarida, taban bos): %d parca'),
             ('"generator": "AUTOKITCH kesme_cad_v2"', '"generator": "AUTOKITCH kesme_cad_v3"'), ('surum="kesme_cad_v2 · %s"', 'surum="kesme_cad_v3 · %s"'),
             ('"otonom", "hat3d", "kesme_v2.glb")', '"otonom", "hat3d", "kesme_v3.glb")'), ('"arastirma", "4_KESME_v2")', '"arastirma", "4_KESME_v3")'),
             ('"otonom", "hat3d", "kesme_v2.json")', '"otonom", "hat3d", "kesme_v3.json")')):
    d(a, b)
io.open(os.path.join(U, "kesme_cad_v3.py"), "w", encoding="utf-8").write(s)
print("kesme_cad_v3.py yazildi")
