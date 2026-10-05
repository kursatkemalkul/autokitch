# -*- coding: utf-8 -*-
"""teknik_hat_atosa_tablali_v11 → v12: pafta = montaj v45 (K = kesme_cad_v1 gerçek · TOPPING v5 kama yarık)."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "teknik_hat_atosa_tablali_v11.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


degis("import math, sys\n", "import math, sys, os\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nimport kesme_cad_v1 as KS                    # v12: K istasyonu ölçüleri üretim modelinden\n")
_k0 = s.index("def ciz_K():"); _k1 = s.index("def ciz_E():")
s = s[:_k0] + '''def ciz_K():
    """v12 · kesme_cad_v1: K bandı · kesici + sprey aynı kafada · itici · taban: içecek yedeği önde, arkada kompresör + tereyağı + pano"""
    kabin(X_K, W_K, 0.0, H_MAK, "K · KESME + SPREY")
    kapak(X_K, 1.5, W_K - 1.5, Y_ALT + 3.0, H_B - 3.0)
    kapak(X_K, 40.0, 440.0, 130.0, 745.0, "İÇECEK YEDEĞİ|soğutmasız · önde|5 koli × 24 = 120|160 + 120 = 280 = 4 gün", fill=(255, 244, 230))
    kesik(X_K, 40.0, 420.0, 130.0, 640.0, "", GRAY)
    kesik(X_K, 60.0, 220.0, 665.0, 959.0, "TEREYAĞI", RED, "3 L ısıtmalı|basınçlı tank")
    kesik(X_K, 300.0, 565.0, 660.0, 1045.0, "PANO", GRAY, "S7-1200 · STP-DRV|NDR-240 · PNOZ|PWM sprey")
    satirlar(fx(X_K + 510.0), fy(560.0), "ARKADA:|KOMPRESÖR|JUN-AIR|130–640", f7, INK, 17)
    d.line([(fx(X_K), fy(H_B)), (fx(X_K + W_K), fy(H_B))], fill=LINE, width=4)
    # K bandı
    d.rectangle([fx(X_K + KS.X_KUYRUK), fy(KS.BANT), fx(X_K + KS.X_TAHRIK), fy(KS.BANT - 6.0)], fill=EVC, outline=BUZ, width=2)
    for xr, yr, rr in ((KS.X_KUYRUK, KS.Y_KUYRUK, KS.R_KUYRUK), (KS.X_TAHRIK, KS.Y_TAHRIK, KS.R_TAHRIK)):
        d.ellipse([fx(X_K + xr - rr), fy(yr + rr), fx(X_K + xr + rr), fy(yr - rr)], fill=BG, outline=BUZ, width=2)
    txt(fx(X_K + 300.0), fy(KS.BANT + 24.0), "K BANDI 400 · üstü %s" % sayi(KS.BANT), f7, BUZ, "mm")
    # kesici + sprey kafası (yukarıda)
    d.rectangle([fx(X_K + 3), fy(KS.Y_KIRIS[1]), fx(X_K + W_K - 3), fy(KS.Y_KIRIS[0])], fill=SOFT, outline=LINE, width=2)
    d.rectangle([fx(X_K + 225), fy(KS.Y_GOVDE[1]), fx(X_K + 375), fy(KS.Y_GOVDE[0])], fill=BG, outline=INK, width=2)
    txt(fx(X_K + 300), fy((KS.Y_GOVDE[0] + KS.Y_GOVDE[1]) / 2) - 8, "Festo DGRF-C-63-125", f7, INK, "mm")
    txt(fx(X_K + 300), fy((KS.Y_GOVDE[0] + KS.Y_GOVDE[1]) / 2) + 10, "1870 N · strok 125", f7, GRAY, "mm")
    d.rectangle([fx(X_K + 215), fy(KS.Y_ON_PL[1]), fx(X_K + 385), fy(KS.Y_ON_PL[0])], fill=BG, outline=INK, width=2)
    d.rectangle([fx(X_K + 305), fy(1386.0), fx(X_K + 405), fy(1348.0)], fill=(255, 236, 200), outline=RED, width=2)
    txt(fx(X_K + 470), fy(1367.0), "PulsaJet", f7, RED, "lm")
    d.rectangle([fx(X_K + 185), fy(KS.Y_KAFA[1]), fx(X_K + 415), fy(KS.Y_KAFA[0])], fill=BG, outline=INK, width=2)
    drect(fx(X_K + 300 - KS.KORUMA_R[1]), fy(KS.Y_KAFA[0]), fx(X_K + 300 + KS.KORUMA_R[1]), fy(KS.KORUMA_ALT), INK, 1)
    for i in range(7):
        xx = X_K + 300 - KS.BICAK_R1 + i * KS.BICAK_R1 / 3.0
        d.line([(fx(xx), fy(KS.Y_AGIZ_UST)), (fx(xx), fy(KS.Y_GOBEK))], fill=INK, width=1)
    d.line([(fx(X_K + 300 - KS.BICAK_R1), fy(KS.Y_AGIZ_UST)), (fx(X_K + 300 + KS.BICAK_R1), fy(KS.Y_AGIZ_UST))], fill=INK, width=2)
    txt(fx(X_K + 300), fy(KS.Y_AGIZ_UST) + 14, "BIÇAK Ø296 × 6", f7, INK, "mm")
    dline((fx(X_K + 300), fy(KS.Y_UC)), (fx(X_K + 300 - 143), fy(KS.BANT + 15.0)), RED, 1)
    dline((fx(X_K + 300), fy(KS.Y_UC)), (fx(X_K + 300 + 143), fy(KS.BANT + 15.0)), RED, 1)
    olcu_v(fx(X_K + 115), fy(KS.Y_AGIZ_UST), fy(KS.KESIM_ALT), "125", f7, INK, "l")
    # itici (bekleme: yukarıda, sağda) + eksen (arkada)
    iy0 = KS.Y_ITICI[0] + KS.ITICI_KALK; iy1 = KS.Y_ITICI[1] + KS.ITICI_KALK
    d.rectangle([fx(X_K + KS.YUZ_BEKLE - 16), fy(iy1), fx(X_K + KS.YUZ_BEKLE), fy(iy0)], fill=BG, outline=ACC, width=2)
    d.rectangle([fx(X_K + KS.YUZ_BEKLE - 134), fy(iy0 + 38.0), fx(X_K + KS.YUZ_BEKLE - 16), fy(iy0 + 18.0)], fill=BG, outline=ACC, width=1)
    txt(fx(X_K + KS.YUZ_BEKLE - 30), fy(iy1) - 14, "İTİCİ", f7, ACC, "mm")
    drect(fx(X_K + KS.EKSEN_X[0]), fy(KS.Y_EKSEN[1]), fx(X_K + KS.EKSEN_X[1]), fy(KS.Y_EKSEN[0]), ACC, 1)
    txt(fx(X_K + 300), fy(KS.Y_EKSEN[0]) + 14, "igus ZLW-1040 · arkada · strok 365", f7, ACC, "mm")
    kesik(X_K, 60.0, 250.0, 1700.0, 1860.0, "HAVA", GRAY, "MS4 + VUVG 4 × 5/2")
    modul_etiketi(X_K, W_K, "MODÜL K · KESME + SPREY", "600 × 830 × 2030 · bant %s · kesici 125" % sayi(KS.BANT))
    olcu_h(fx(X_K), fx(X_K + W_K), fy(H_MAK) - 26, sayi(W_K), f11, INK)


''' + s[_k1:]
# ---- plan: K ----
_p0 = s.index("    # K (v8 · montaj: plaka z −470…−20, bıçak ve sprey ürün ekseninde z −170)")
_p1 = s.index("    # E (v8 · kutu_cad_v3)")
s = s[:_p0] + '''    # K (v12 · kesme_cad_v1)
    d.rectangle([fx(X_K + KS.X_KUYRUK), py(KS.BANT_Z[0]), fx(X_K + KS.X_TAHRIK), py(KS.BANT_Z[1])], fill=EVC, outline=BUZ, width=2)
    txt(fx(X_K + 300), py(-560.0), "K BANDI 400 · yıldız bıçak Ø296 · koruma Ø316", f7, BUZ, "mm")
    d.ellipse([fx(X_K + 300 - KS.BICAK_R1), py(ZT - KS.BICAK_R1), fx(X_K + 300 + KS.BICAK_R1), py(ZT + KS.BICAK_R1)], outline=INK, width=2)
    for k in range(3):
        a = math.radians(60.0 * k)
        d.line([(fx(X_K + 300) - KS.BICAK_R1 * S * math.cos(a), py(ZT) - KS.BICAK_R1 * S * math.sin(a)), (fx(X_K + 300) + KS.BICAK_R1 * S * math.cos(a), py(ZT) + KS.BICAK_R1 * S * math.sin(a))], fill=INK, width=1)
    _zc = lambda x: KS.CIT_P0[1] - math.tan(math.radians(KS.CIT_ACI)) * (x - KS.CIT_P0[0])
    d.line([(fx(X_K + 330.0), py(_zc(330.0))), (fx(X_K + KS.CIT_X_DONUS), py(KS.CIT_Z_DUZ)), (fx(X_K + 597.0), py(KS.CIT_Z_DUZ))], fill=RED, width=3)
    txt(fx(X_K + 470.0), py(0.0) + 16, "ÇİT 20°", f7, RED, "mm")
    drect(fx(X_K + KS.EKSEN_X[0]), py(KS.Z_EKSEN[0]), fx(X_K + KS.EKSEN_X[1]), py(KS.Z_EKSEN[1]), ACC, 1)
    txt(fx(X_K + 300), py(-505.0), "itici ekseni ZLW-1040", f7, ACC, "mm")
    d.rectangle([fx(X_K + KS.YUZ_BAS - 16), py(KS.ITICI_Z[0]), fx(X_K + KS.YUZ_BAS), py(KS.ITICI_Z[1])], fill=BG, outline=ACC, width=2)
    d.line([(fx(X_K + 300), py(ZT)), (fx(X_K + 500), py(-206.0)), (fx(X_E + 260), py(-206.0))], fill=INK, width=2)
    d.polygon([(fx(X_E + 260), py(-206.0)), (fx(X_E + 240), py(-206.0) - 7), (fx(X_E + 240), py(-206.0) + 7)], fill=INK)
    txt(fx(X_K + 600), py(40.0) + 52, "K: bant ürünü 300 → 500 taşır, çit 36 mm içeri kaydırır · itici 500 → 860 (E'ye 110 mm girer)", f7, RED, "mm")
''' + s[_p1:]
degis('("MODÜL K", "KESME · plaka 560 × 450 (z −470…−20) + yıldız bıçak Ø300 6 dilim + tereyağı spreyi + itici · taban dolabı: önde içecek yedeği · arkada kompresör + yağ + K kartı · üst bölme boş", "1", "600 × 830 × 2030 · plaka üstü 1164 · E için şart: itici 36 mm içeri kaydırır"),',
      '("MODÜL K", "KESME + SPREY (kesme_cad_v1) · K bandı PU 400 + RollerDrive EC5000 · Festo DGRF-C-63-125 + yıldız bıçak Ø296 × 6 + koruma Ø316 · PulsaJet + TG 90° nozül bıçak göbeğinde · 20° çit · itici igus ZLW-1040 + SMC MGPM20-60 · taban: önde içecek yedeği · arkada kompresör + tereyağı tankı 3 L + pano", "1", "600 × 830 × 2030 · bant 1164 · bıçak alt dayama 1164,5 · itici E\'ye 110"),')
degis('("MODÜL C", "TOPPING v2 (topping_uno_cad_v4) ·', '("MODÜL C", "TOPPING v2 (topping_uno_cad_v5 · sos + harç yayıcısında KAMA YARIK: sos 2,0→3,2 · harç 6,0→9,6) ·')
degis('("HAVA", "JUN-AIR OF302-15B yağsız kompresör · 15 L · 43 L/dk @ 7 bar · K tabanı ARKADA (130–640), üstünde yağ + K kartı ·', '("HAVA", "JUN-AIR OF302-15B yağsız kompresör · 15 L · 43 L/dk @ 7 bar · K tabanı ARKADA (130–640), üstünde tereyağı tankı + pano · K kesicisi de bu hattan ·')
degis("TEKNİK RESİM  v11  ·  MONTAJ = hat_montaj_v44  ·  TOPPING = topping_uno_cad_v4 (4 UNO + kaşar/sucuk kaseti · havalı) + topping_cad_v22 tabla",
      "TEKNİK RESİM  v12  ·  MONTAJ = hat_montaj_v45  ·  TOPPING = topping_uno_cad_v5 (4 UNO + kaşar/sucuk kaseti · kama yarık) + topping_cad_v22 tabla · K = kesme_cad_v1")
degis("bıçak burunlu bant fırına çeker → kesme plakası → kutu", "bıçak burunlu bant fırına çeker → K bandı (sprey + kesme aynı kafada) → kutu")
degis("hava: kompresör K tabanında (yeri AÇIK)", "hava: kompresör K tabanında")
degis("ölçüler mm  ·  25 Eylül 2026\")\n    # ---- A · AÇICI", "ölçüler mm  ·  26 Eylül 2026\")\n    # ---- A · AÇICI")
degis('kabin(X_C, W_C, H_B, H_MAK, "C · TOPPING v2 · 4 UNO + 2 kaset · havalı (montaj v43)")', 'kabin(X_C, W_C, H_B, H_MAK, "C · TOPPING v2 · 4 UNO + 2 kaset · havalı · kama yarık (v5)")')
degis('    yol = KLASOR + r"\\HAT_ATOSA_TABLALI_v11_HD.png"', '    yol = KLASOR + r"\\HAT_ATOSA_TABLALI_v12_HD.png"')
degis('k.save(KLASOR + r"\\HAT_ATOSA_TABLALI_v11_EKRAN.png", optimize=True)', 'k.save(KLASOR + r"\\HAT_ATOSA_TABLALI_v12_EKRAN.png", optimize=True)')
io.open(os.path.join(U, "teknik_hat_atosa_tablali_v12.py"), "w", encoding="utf-8").write(s)
print("teknik_hat_atosa_tablali_v12.py yazildi")
