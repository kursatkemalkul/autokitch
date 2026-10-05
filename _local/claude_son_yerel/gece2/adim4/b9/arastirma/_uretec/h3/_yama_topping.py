# -*- coding: utf-8 -*-
"""h3_topping_v1 yaması (h2_topping_v1 kopyası → v3) · metin değiştirme, her biri bir kez"""
import io, os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "h3_topping_v1.py")
s = io.open(P, encoding="utf-8").read()
R = []
def r(a, b):
    R.append((a, b))

r('"""HAT VERSİYON 2 · TOPPING v2 — İKİ KATLI (30 Eyl 2026 · Claude · YEREL).',
  '"""HAT VERSİYON 3 · TOPPING v3 (30 Eyl 2026 · Claude · YEREL) — v2 üreteci + Kemal HAT v2.7: sol duvar kıymanın dibinde (1436) · üst katta YALNIZ 2 UNO ·\n'
  'sos + harç ÇIKIŞI DİK İNER (yayıcılar alt kat dozajlayıcılarının arasında, ağız kaset iniş borularıyla aynı kotta) · evaporatör kaseti iki UNO\'nun arasında ·\n'
  'kaşar / sucuk GN yedeği ÇIKTI (dolabın teknik sütununda) · soğutma grubu emişine teknik bölmenin arkasından pencere.\n'
  'AŞAĞISI v2 AÇIKLAMASI (tarihçe):\nHAT VERSİYON 2 · TOPPING v2 — İKİ KATLI (30 Eyl 2026 · Claude · YEREL).')
# ---- istasyonlar / UNO'lar / yayıcılar
r('X_YAYICI = {"sos": 1396.0, "harc": 1466.0}', 'X_YAYICI = {"sos": HS.IST_V3["SOS"], "harc": HS.IST_V3["HARC"]}          # v3: 1645 · 2226 (alt kat dozajlayıcılarının arası)')
r('X_UST = {"sos": 1397.5, "harc": 1747.5}      # üst kattaki UNO eksenleri (v1 aralığı 350 korunur, haznelerin arası 20)',
  'X_UST = {"sos": 1645.0, "harc": 2247.0}      # v3 · üst kattaki UNO eksenleri: sos yayıcısının tam üstü · harç 21 sağda (evaporatör kaseti iki UNO silindirinin arasına sığsın)')
r('ISTASYON = {"SOS": X_YAYICI["sos"], "HARC": X_YAYICI["harc"], "KIYMA": 1595.0 + DX_ALT, "KUSBASI": 1805.0 + DX_ALT,',
  'DY_YAY = {"alt": HS.Y_AGIZ - 1.0 - 1013.0, "ust": 110.0}   # v3 · yayıcı: dağıtıcı + üçgen + tapalar +34 (ağız 1047, pide koridorunun 14 üstü) · valf + dik boru + TC girişi +110 (alt kat tabanının üstünde)\n'
  'YAY_ALT = ("dagitici_boru", "uc_tapasi", "merkez_tapasi", "ucgen_dagitici")\n'
  'YAY_BORU_R = 15.0                             # v3 · üçgen dağıtıcı ↔ valf arası uzatma borusu Ø30 × 1,5 (alt kat tabanını kontayla geçer)\n'
  'ISTASYON = {"SOS": X_YAYICI["sos"], "HARC": X_YAYICI["harc"], "KIYMA": 1595.0 + DX_ALT, "KUSBASI": 1805.0 + DX_ALT,')
r('IZGARA = {"emis": [1257.5 + 65.0 * i_ for i_ in range(5)], "atis": [1869.5 + 65.0 * i_ for i_ in range(9)]}   # 1257,5–1577,5 · 1869,5–2449,5',
  'IZGARA = {"emis": [1470.0, 1535.0], "atis": [1845.0, 1900.0, 1975.0, 2040.0, 2105.0, 2170.0, 2235.0, 2300.0, 2365.0]}   # v3 · emiş sol kanatta (menteşeden sonra) · atış 1845→ (ara 250) · derz 1965,75–1968,75 atlanır\n'
  'ARKA_EMIS = (1447.0, 1625.0, 905.0, 1100.0)    # v3 · TEKNİK BÖLMENİN ARKA EMİŞ PENCERESİ (dış arka sac, ayırma perdesinin solu) · filtreli · C emiş odası v2\'nin yarısı kaldı')
r('EVAP_D = (1778.0 - 1470.0, 1383.0 - 1473.0, 0.0)', 'EVAP_D = (1676.0 - 1470.0, 1383.0 - 1473.0, 0.0)          # v3 · kaset 1676–2216: sos UNO silindir konsolu (≤ 1671) ile harç UNO konsolu (≥ 2221) arası\n_EVAP_D_V2 = (1778.0 - 1470.0, 1383.0 - 1473.0, 0.0)')
r('"kuru_pano_kutusu": (1215.0 - 900.0, 1880.0 - 1585.0, 0.0),', '"kuru_pano_kutusu": (1443.0 - 900.0, 1880.0 - 1585.0, 0.0),')
r('"kuru_din_": (1215.0 - 2020.0, 1680.0 - 1600.0, 0.0),', '"kuru_din_": (1443.0 - 2020.0, 1680.0 - 1600.0, 0.0),')
r('"kuru_ups": (1215.0 - 2020.0, 1680.0 - 1600.0, 0.0), "kuru_guc_kaynagi": (1215.0 - 2020.0, 1680.0 - 1600.0, 0.0),',
  '"kuru_ups": (1443.0 - 2020.0, 1680.0 - 1600.0, 0.0), "kuru_guc_kaynagi": (1443.0 - 2020.0, 1680.0 - 1600.0, 0.0),')
r('"kuru_surucu_": (1575.0 - 1170.0, 0.0, 0.0), "kuru_din_rayi_surucu": (1575.0 - 1170.0, 0.0, 0.0),',
  '"kuru_surucu_": (1458.0 - 1170.0, 0.0, 0.0), "kuru_din_rayi_surucu": (1458.0 - 1170.0, 0.0, 0.0),')
r('"kuru_din_rayi_ayak_": (1575.0 - 1170.0, 0.0, 0.0)}', '"kuru_din_rayi_ayak_": (1458.0 - 1170.0, 0.0, 0.0)}')
r('TU_KURU = {"valf_": (1240.0 - 850.0, 0.0, 0.0),', 'TU_KURU = {"valf_": (1690.0 - 850.0, 1250.0 - 1432.0, 0.0),                    # v3 · valf adası evaporatör kasetinin ALTINDA (1690–1998 × 1250–1340)')
r('ANA_V2 = [(3790.0, 1809.0, -380.0), (3790.0, 1809.0, -740.0),', 'ANA_V2 = [(3520.0, 1809.0, -380.0), (3520.0, 1809.0, -740.0),   # v3 · kompresör fırın üstünde 270 sola (çıkış vanası 3520)\n         ')
r('ADA_V2 = [(2420.0, 1167.0, -740.0), (2390.0, 1167.0, -740.0), (2390.0, 1125.0, -740.0), (1560.0, 1125.0, -740.0), (1560.0, 1462.0, -740.0), (1548.0, 1462.0, -740.0)]',
  'ADA_V2 = [(2420.0, 1167.0, -740.0), (2390.0, 1167.0, -740.0), (2390.0, 1125.0, -740.0), (2010.0, 1125.0, -740.0), (2010.0, 1280.0, -740.0), (1998.0, 1280.0, -740.0)]')
r('SOG_HAT = {"sogutma_emis_hatti": [(2013.0, 1050.0, -700.0), (2258.0, 1050.0, -700.0), (2258.0, 1383.0, -700.0)],\n'
  '           "sogutma_sivi_hatti": [(2013.0, 1070.0, -660.0), (2236.0, 1070.0, -660.0), (2236.0, 1360.0, -660.0), (2236.0, 1360.0, -700.0), (2236.0, 1383.0, -700.0)]}',
  'SOG_HAT = {"sogutma_emis_hatti": [(2013.0, 1050.0, -700.0), (2258.0, 1050.0, -700.0), (2258.0, 1300.0, -700.0), (2156.0, 1300.0, -700.0), (2156.0, 1383.0, -700.0)],\n'
  '           "sogutma_sivi_hatti": [(2013.0, 1070.0, -660.0), (2236.0, 1070.0, -660.0), (2236.0, 1320.0, -660.0), (2134.0, 1320.0, -660.0), (2134.0, 1360.0, -660.0),\n'
  '                                  (2134.0, 1360.0, -700.0), (2134.0, 1383.0, -700.0)]}   # v3 · kaşar | sucuk motorlarının arasından çıkıp kasetin (−102) hat bloğuna döner')
r('TAHLIYE_V2 = [(2203.0, 1425.0, -775.0), (2203.0, 1350.0, -775.0), (2203.0, 1350.0, -805.0), (2203.0, 1372.0, -805.0), (2203.0, 1372.0, -815.0),\n'
  '              (2203.0, 950.0, -815.0), (2120.0, 950.0, -815.0),',
  'TAHLIYE_V2 = [(2108.0, 1425.0, -775.0), (2108.0, 1350.0, -775.0), (2108.0, 1350.0, -805.0), (2108.0, 1372.0, -805.0), (2108.0, 1372.0, -815.0),\n'
  '              (2108.0, 950.0, -815.0), (2120.0, 950.0, -815.0),')
r('HORTUM = {"sos": [(1397.5, 1613.5, -235.0), (1397.5, 1613.5, -170.0), (1397.5, 1520.0, -170.0), (1396.0, 1440.0, -170.0), (1396.0, 1106.0, -170.0)],\n'
  '          "harc": [(1747.5, 1613.5, -235.0), (1747.5, 1613.5, -170.0), (1466.0, 1613.5, -170.0), (1466.0, 1106.0, -170.0)]}',
  '# v3 · UNO çıkışından ÖNE (z −90: alt kat hazneleri −120\'de biter) → DİK iner → kıyma haznesinin altında (1250) yayıcı ekseninin üstüne döner → TC girişine (1216)\n'
  'HORTUM = {"sos": [(1645.0, 1613.5, -235.0), (1645.0, 1613.5, -90.0), (1645.0, 1250.0, -90.0), (1645.0, 1250.0, -170.0), (1645.0, 1216.0, -170.0)],\n'
  '          "harc": [(2247.0, 1613.5, -235.0), (2247.0, 1613.5, -90.0), (2247.0, 1290.0, -90.0), (2226.0, 1290.0, -90.0), (2226.0, 1250.0, -90.0),\n'
  '                   (2226.0, 1250.0, -170.0), (2226.0, 1216.0, -170.0)]}')
# ---- sınıflandırma: yayıcılar (alt grup +34 · üst grup +110)
r('            sh = tasi(_rotY(q["sh"], X_V1[k], TU0.ZT, 90.0), X_YAYICI[k] - X_V1[k])',
  '            dy_ = DY_YAY["alt"] if a.split("_spreader_")[1].startswith(YAY_ALT) else DY_YAY["ust"]\n'
  '            sh = tasi(_rotY(q["sh"], X_V1[k], TU0.ZT, 90.0), X_YAYICI[k] - X_V1[k], dy_)')
# ---- yeni TC: bağlama laması (v3'te dilimde kalan lama yok, boşluk 124) · derz · kuru bölme tabanı delikleri · arka emiş penceresi
r('    ek("baglama_lamasi_3", tasi(kut(xb, xb + 40.0, 4.5, 20.5, -335.0, -305.0), DXW, DYW), "celik")',
  '    # v3: v1 lamaları 0–2 +736 (dünya 916 · 1216 · 1516), 3–4 dilimde, 5 ve sonrası yerinde (1680 …) → en büyük aralık 124 · ek lama GEREKMEZ')
r('    DERZ = (1851.5, 1854.5); XO = (DERZ[0] + DERZ[1]) / 2.0 - 15.0                               # orta dikme 1838–1868',
  '    DERZ = ((XT[0] + SAC + XT[1] - 3.0 - 3.0) / 2.0, (XT[0] + SAC + XT[1] - 3.0 + 3.0) / 2.0); XO = (DERZ[0] + DERZ[1]) / 2.0 - 15.0   # v3 · eşit kanatlar 1965,75 | 1968,75')
r('    IZ_EMIS, IZ_ATIS = IZGARA["emis"], {"sol": [], "sag": IZGARA["atis"]}',
  '    IZ_EMIS = IZGARA["emis"]; IZ_ATIS = {"sol": [x_ for x_ in IZGARA["atis"] if x_ + 60.0 <= DERZ[0] - 5.0], "sag": [x_ for x_ in IZGARA["atis"] if x_ >= DERZ[1] + 5.0]}')
r('    for x_, z_, r_ in ((2258.0, -700.0, 16.5), (2236.0, -660.0, 4.2), (2203.0, -815.0, 5.0)):',
  '    for x_, z_, r_ in ((2258.0, -700.0, 16.5), (2236.0, -660.0, 4.2), (TAHLIYE_V2[0][0], -815.0, 5.0)):')
r('    ek("dis_arka", kut(x0 + SAC, x1 - SAC, 892.0 + SAC, H_UST - SAC, -830.0, -830.0 + SAC), "sac",',
  '    ek("teknik_bolme_arka_emis_filtresi", kut(ARKA_EMIS[0] - 5.0, ARKA_EMIS[1] + 5.0, ARKA_EMIS[2] - 5.0, ARKA_EMIS[3] + 5.0, -828.5, -814.5), "pom",\n'
  '       _bom("Kondenser arka emiş filtresi · yıkanabilir paslanmaz tel örgü + çerçeve", 1, "%.0f × %.0f × 14 · dış arka sacın iç yüzünde 2 klips" % (ARKA_EMIS[1] - ARKA_EMIS[0] + 10, ARKA_EMIS[3] - ARKA_EMIS[2] + 10),\n'
  '            "v3 · teknik bölmenin sol yarısı (ayırma perdesinin solu) = soğutma grubunun EMİŞ odası · makine arkasında ≥ 50 mm boşluk"))\n'
  '    ek("dis_arka", kut(x0 + SAC, x1 - SAC, 892.0 + SAC, H_UST - SAC, -830.0, -830.0 + SAC).cut(kut(ARKA_EMIS[0], ARKA_EMIS[1], ARKA_EMIS[2], ARKA_EMIS[3], -831.0, -828.0)), "sac",')
# ---- yeni TU: geçiş blokları · taban delikleri (uzatma borusu) · kapak derzi · GN yok · konsol · hava hatları · uzatma borusu · harç haznesi
r('    GB = {"alt": (1560.0, 1780.0, 1272.0, 1302.0), "ust": (1290.0, 1790.0, 1700.0, 1730.0)}',
  '    GB = {"alt": (1560.0, 1780.0, 1272.0, 1302.0), "ust_sol": (1520.0, 1690.0, 1700.0, 1730.0), "ust_sag": (2200.0, 2330.0, 1700.0, 1730.0)}   # v3 · üst blok kaset penceresinin iki yanında')
r('        raf = raf.cut(sily(x_, TU0.ZT, HORTUM_R + 3.0, 1148.0, 1153.0))\n'
  '        ek("raf_gecis_contasi_%s" % k_, sily(x_, TU0.ZT, HORTUM_R + 3.0, 1149.0, 1152.0).cut(sily(x_, TU0.ZT, HORTUM_R, 1148.0, 1153.0)), "conta",',
  '        raf = raf.cut(sily(x_, TU0.ZT, YAY_BORU_R + 3.0, 1148.0, 1153.0))\n'
  '        ek("raf_gecis_contasi_%s" % k_, sily(x_, TU0.ZT, YAY_BORU_R + 3.0, 1149.0, 1152.0).cut(sily(x_, TU0.ZT, YAY_BORU_R, 1148.0, 1153.0)), "conta",')
r('        c = sily(x_, TU0.ZT, HORTUM_R + 0.5, KY[0] - 1.0, 1149.5)', '        c = sily(x_, TU0.ZT, YAY_BORU_R + 0.5, KY[0] - 1.0, 1149.5)')
r('    DERZ = (1851.5, 1854.5)\n', '    DERZ = ((XT[0] + SAC + XT[1] - 3.0 - 3.0) / 2.0, (XT[0] + SAC + XT[1] - 3.0 + 3.0) / 2.0)          # v3 · eşit kapaklar (1965,75 | 1968,75)\n')
r('    GX = (1990.0, 2315.0); GZ1 = (-511.0, 19.0)\n    y_ = RAF2[1]\n    gn("gn_kasar_yedek_1_1_200", GX[0], GX[1], y_, 200.0, GZ1[0] + 6.0, GZ1[1] - 6.0, "kasar_urun", HS.KASAR_2GUN_L / HS.GN_KASAR["L"],',
  '    if False:                                                                                    # v3 · kaşar / sucuk GN yedeği TOPPING\'den ÇIKTI (dolabın teknik sütunu)\n      GX = (1990.0, 2315.0); GZ1 = (-511.0, 19.0)\n      y_ = RAF2[1]\n      gn("gn_kasar_yedek_1_1_200", GX[0], GX[1], y_, 200.0, GZ1[0] + 6.0, GZ1[1] - 6.0, "kasar_urun", HS.KASAR_2GUN_L / HS.GN_KASAR["L"],')
r('    gn("gn_sucuk_yedek_1_2_150", GX[0], GX[1], y_ + 200.0 + 1.2, 150.0,', '      gn("gn_sucuk_yedek_1_2_150", GX[0], GX[1], y_ + 200.0 + 1.2, 150.0,')
r('        ek("%s_silindir_konsolu" % u_, kut(b.xmin - 5.0, b.xmax + 5.0, b.ymin - 3.0, b.ymin, -692.0, -630.0).fuse(kut(b.xmin - 5.0, b.xmax + 5.0, b.ymin - 43.0, b.ymin, -633.0, -630.0)),',
  '        ek("%s_silindir_konsolu" % u_, kut(b.xmin - 1.0, b.xmax + 1.0, b.ymin - 3.0, b.ymin, -692.0, -630.0).fuse(kut(b.xmin - 1.0, b.xmax + 1.0, b.ymin - 43.0, b.ymin, -633.0, -630.0)),')
r('    for j_, (yA, zA, xd, yP, renk) in enumerate(((1472.0, -700.0, 420.0 + DXL, 1460.0, "hortum_mavi"), (1460.0, -712.0, 428.0 + DXL, 1292.0, "hortum_siyah"))):\n'
  '        ek("hava_hatti_acici_D6_%d" % (j_ + 1), boru([(1240.0, yA, zA), (xd, yA, zA), (xd, yP, zA), (xd, yP, -540.0), (372.5 + DXL, yP, -540.0)], 3.0), renk,',
  '    for j_, (yA, zA, xd, yP, renk) in enumerate(((1472.0, -700.0, 420.0 + DXL, 1460.0, "hortum_mavi"), (1460.0, -712.0, 428.0 + DXL, 1292.0, "hortum_siyah"))):\n'
  '        yv = yA - 182.0                                                                           # v3 · valf adası 182 aşağıda (kasetin altı) · sürücülerin solundan (x 1447) çıkar\n'
  '        ek("hava_hatti_acici_D6_%d" % (j_ + 1), boru([(1690.0, yv, zA), (1447.0, yv, zA), (1447.0, yA, zA), (xd, yA, zA), (xd, yP, zA), (xd, yP, -540.0), (372.5 + DXL, yP, -540.0)], 3.0), renk,')
r('    # ---- (e) ÜRÜN HORTUMLARI (Ø32 iç · soğuk kutunun içinde) ----',
  '    # ---- (e0) v3 · YAYICI UZATMA BORUSU (üçgen dağıtıcı ↔ valf · alt kat tabanını kontayla geçer) ----\n'
  '    for k, x_ in X_YAYICI.items():\n'
  '        y0_, y1_ = 1074.0 + DY_YAY["alt"], 1072.0 + DY_YAY["ust"]\n'
  '        ek("%s_spreader_uzatma_borusu" % k, sily(x_, TU0.ZT, YAY_BORU_R, y0_, y1_).cut(sily(x_, TU0.ZT, YAY_BORU_R - 1.5, y0_ - 1.0, y1_ + 1.0)), "paslanmaz",\n'
  '           "v3 · Ø30 × 1,5 AISI 316L · üçgen dağıtıcının üstü (%.0f) → kesme valfinin dik borusu (%.0f) · TC ile sökülür · yayıcı ağzı %.0f (pide koridoru %.0f üstü)" % (y0_, y1_, 1013.0 + DY_YAY["alt"], HS.Y_KORIDOR))\n'
  '    # ---- (e) ÜRÜN HORTUMLARI (Ø32 iç · soğuk kutunun içinde) ----')
# ---- hava yolu: teknik bölme arka penceresi
r('    on_e = et(IZGARA["emis"], KD2.C_PENCERE_X["emis"]); arka_e = 0.6 * pw(KD2.C_ARKA_PENCERE_X); at = et(IZGARA["atis"], KD2.C_PENCERE_X["atis"])',
  '    on_e = et(IZGARA["emis"], KD2.C_PENCERE_X["emis"]); arka_e = 0.6 * pw(KD2.C_ARKA_PENCERE_X); at = et(IZGARA["atis"], KD2.C_PENCERE_X["atis"])\n'
  '    arka_e += 0.6 * (ARKA_EMIS[1] - ARKA_EMIS[0]) * (ARKA_EMIS[3] - ARKA_EMIS[2]) * 1e-6                   # v3 · teknik bölmenin arka emiş penceresi (filtreli)')
for a, b in R:
    n = s.count(a)
    assert n == 1, (n, a[:90])
    s = s.replace(a, b)
io.open(P, "w", encoding="utf-8").write(s)
print("yama tamam", len(R))
