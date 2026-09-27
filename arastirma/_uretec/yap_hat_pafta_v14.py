# -*- coding: utf-8 -*-
"""teknik_hat_atosa_tablali_v13 → v14 (27 Eyl 2026): pafta = montaj v52 (kural 6.5).
F = firin_tp10_cad_v6 (TP10 kesiti, gövde 1500 ÖZEL SİPARİŞ, 79 mm ÖNE; taban dolabı 123–956; üst raf: SOL kutu yedeği 320, SAĞ kompresör;
davlumbaz arka yarı) · C: aktarma iticisi itici_cad_v3 (bıçak burunlu bant YOK) + F giriş bandı · TOPPING v24 tekne 100–2495, X motoru solda ·
uno v9 · K = kesme_cad_v2 (kapak yok, tabanda kompresör YOK) · hava: kompresör fırın üstünde · derinlik düzeltmesi: modül kutuları
modelle aynı z −830…0 (v13'te −790…+40 çiziliyordu)."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "teknik_hat_atosa_tablali_v13.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)


def blok(bas, son, yeni):
    """bas'tan son'a kadar (son hariç) olan metni yeni ile değiştirir"""
    global s
    i = s.index(bas); j = s.index(son, i)
    s = s[:i] + yeni + s[j:]


NL = chr(10)
degis("import kesme_cad_v1 as KS                    # v12: K istasyonu ölçüleri üretim modelinden",
      "import kesme_cad_v1 as KS                    # v12: K istasyonu ölçüleri üretim modelinden (v2 = v1 eksi ön kapaklar; kesit ölçüleri aynı)" + NL +
      "import firin_tp10_cad_v6 as FT               # v14: F = TP10 kesiti · 1500 · 79 öne (montaj v52)" + NL +
      "import itici_cad_v3 as IT                    # v14: aktarma iticisi (düz 170)")

# ---------------- derinlik: modelle aynı (−830 … 0) ----------------
degis("def py(z):\n    return PY_TOP + (z + 790.0) * S", "def py(z):\n    return PY_TOP + (z + 830.0) * S                                  # v14: arka −830 (model), ön 0")
degis("def sec(sx):\n    return lambda v: sx + (v + 790.0) * S", "def sec(sx):\n    return lambda v: sx + (v + 830.0) * S                           # v14")
degis("    d.rectangle([z(-790), fy(h1), z(40), fy(max(h0, Y_ALT) if plint else h0)], fill=FILL, outline=LINE, width=4)",
      "    d.rectangle([z(-830), fy(h1), z(0), fy(max(h0, Y_ALT) if plint else h0)], fill=FILL, outline=LINE, width=4)")
degis("        d.rectangle([z(-760), fy(Y_ALT), z(-20), fy(0)], fill=SOFT, outline=LINE, width=2)",
      "        d.rectangle([z(-800), fy(Y_ALT), z(-60), fy(0)], fill=SOFT, outline=LINE, width=2)")
degis("    d.line([(z(40), fy(0)), (z(1390), fy(0))], fill=INK, width=3)\n    olcu_h(z(40), z(RZ), fy(0) + 44, sayi(RZ - 40.0) + \" + 40\", f8, ACC)\n    olcu_h(z(-790), z(40), fy(0) + 44, \"830\", f11, INK)",
      "    d.line([(z(0), fy(0)), (z(1390), fy(0))], fill=INK, width=3)\n    olcu_h(z(0), z(RZ), fy(0) + 44, sayi(RZ), f8, ACC)\n    olcu_h(z(-830), z(0), fy(0) + 44, \"830\", f11, INK)")
degis("            d.rectangle([z(-680.0), fy(y0 + h), z(0.0), fy(y0)], fill=BG, outline=DOLAP, width=1)\n            d.rectangle([z(0.0), fy(y0 + h), z(40.0), fy(y0)], fill=BG, outline=DOLAP, width=1)\n            d.line([(z(2.0), fy(y0 + 6.0)), (z(2.0), fy(y0 + h - 6.0))], fill=RED, width=2)\n            d.rectangle([z(-760.0), fy(y0 + h / 2 + 10.0), z(-690.0), fy(y0 + h / 2 - 10.0)], fill=(255, 230, 230), outline=RED, width=1)",
      "            d.rectangle([z(-720.0), fy(y0 + h), z(-40.0), fy(y0)], fill=BG, outline=DOLAP, width=1)\n            d.rectangle([z(-40.0), fy(y0 + h), z(0.0), fy(y0)], fill=BG, outline=DOLAP, width=1)\n            d.line([(z(-38.0), fy(y0 + 6.0)), (z(-38.0), fy(y0 + h - 6.0))], fill=RED, width=2)\n            d.rectangle([z(-800.0), fy(y0 + h / 2 + 10.0), z(-730.0), fy(y0 + h / 2 - 10.0)], fill=(255, 230, 230), outline=RED, width=1)")
degis("    d.rectangle([z(-10.0), fy(a1), z(40.0), fy(a0)], fill=AGZ, outline=RED, width=2)", "    d.rectangle([z(-50.0), fy(a1), z(0.0), fy(a0)], fill=AGZ, outline=RED, width=2)")
degis("    d.rectangle([z(-10.0), fy(P + 220.0), z(40.0), fy(P)], fill=AGZ, outline=RED, width=2)", "    d.rectangle([z(-50.0), fy(P + 220.0), z(0.0), fy(P)], fill=AGZ, outline=RED, width=2)", 2)
degis("    olcu_h(z(40), z(QRZ[0]), fy(0) + 84, \"koridor + pay %s\" % sayi(QRZ[0] - 40.0), f8, GRAY)", "    olcu_h(z(0), z(QRZ[0]), fy(0) + 84, \"koridor + pay %s\" % sayi(QRZ[0]), f8, GRAY)")
s = s.replace("d.line([(z(-790) - 24, fy(yy)), (z(-790) - 6, fy(yy))], fill=INK, width=2)", "d.line([(z(-830) - 24, fy(yy)), (z(-830) - 6, fy(yy))], fill=INK, width=2)")
s = s.replace("txt(z(-790) - 30, fy(yy), sayi(yy), f7, INK, \"rm\")", "txt(z(-830) - 30, fy(yy), sayi(yy), f7, INK, \"rm\")")
degis("    txt(fx(HAT / 2), py(-790) - 30, \"ARKA\", f9, GRAY, \"mm\")\n    zb = 40.0 - DZ", "    txt(fx(HAT / 2), py(-830) - 30, \"ARKA\", f9, GRAY, \"mm\")\n    zb = -DZ")
degis("        d.rectangle([fx(x0m), py(zb), fx(x0m + w), py(40.0)], fill=FILL, outline=LINE, width=3)\n        txt(fx(x0m + w / 2), py(40.0) + 26, \"%s  ·  %s × %s\" % (ad, sayi(w), sayi(DZ)), f8, INK, \"mm\")",
      "        d.rectangle([fx(x0m), py(zb), fx(x0m + w), py(0.0)], fill=FILL, outline=LINE, width=3)\n        txt(fx(x0m + w / 2), py(FT.ZS) + 26, \"%s  ·  %s × %s\" % (ad, sayi(w), sayi(DZ + (FT.ZS if x0m == X_F else 0.0))), f8, INK, \"mm\")")
degis('(X_F, W_F, "F · KONVEYÖR FIRIN")', '(X_F, W_F, "F · TP10 FIRIN · 79 öne")')
degis("    olcu_v(fx(0) - 44, py(-790), py(40.0), sayi(DZ), f11, INK, \"l\")\n    olcu_v(fx(0) - 44, py(40.0), py(40.0 + KOR), \"koridor %s\" % sayi(KOR), f8, GRAY, \"l\")\n    d.line([(fx(-60), py(40.0 + KOR)), (fx(HAT + 60), py(40.0 + KOR))], fill=GRAY, width=1)",
      "    olcu_v(fx(0) - 44, py(-830), py(0.0), sayi(DZ), f11, INK, \"l\")\n    olcu_v(fx(0) - 44, py(0.0), py(KOR), \"koridor %s\" % sayi(KOR), f8, GRAY, \"l\")\n    d.line([(fx(-60), py(KOR)), (fx(HAT + 60), py(KOR))], fill=GRAY, width=1)")
degis("    txt(fx(0) - 50, py(40.0 + KOR) + 24, \"kesik daire", "    txt(fx(0) - 50, py(KOR) + 24, \"kesik daire")
degis("    txt(fx(X_K + 600), py(40.0) + 52, \"K: bant", "    txt(fx(X_K + 600), py(FT.ZS) + 60, \"K: bant")

# ---------------- F · ön görünüş (TP10) ----------------
F_YENI = '''def ciz_F(taban_parcalar=()):
    """v14 · firin_tp10_cad_v6 (montaj v52): TP10 kesiti · gövde 1500 ÖZEL SİPARİŞ · 79 mm öne · taban dolabı 123–956 (kapaksız) ·
    üstte havalandırmalı raf 4 mm (10 takoz): SOL kutu yedeği 320 (tek yer) · SAĞ kompresör · davlumbaz arka yarıda"""
    G0, G1 = FT.YG0, FT.YG1
    kabin(X_F, W_F, 0.0, H_MAK, "F · TP10 KESİTLİ KONVEYÖR FIRIN · 1500 ÖZEL SİPARİŞ · 79 mm ÖNE · 4 ürün")
    for a, b, y0, y1, et, alt in taban_parcalar:
        kesik(X_F, a, b, y0, y1, et, INK, alt)
    # gövde + ön oda + uç duvarları + ısıtılan tünel
    d.rectangle([fx(FT.X_F0), fy(G1), fx(FT.X_F1), fy(G0)], fill=SOFT, outline=INK, width=3)
    tarali(fx(FT.X_DUV0), fy(G1 - 2), fx(FT.X_TUN0), fy(G0 + 2), (226, 214, 190), 11)
    tarali(fx(FT.X_TUN1), fy(G1 - 2), fx(FT.X_F1 - 2), fy(G0 + 2), (226, 214, 190), 11)
    d.rectangle([fx(FT.X_TUN0), fy(FT.TUN_Y[1]), fx(FT.X_TUN1), fy(FT.TUN_Y[0])], fill=SICAK, outline=TURUNCU, width=2)
    txt(fx((FT.X_F0 + FT.X_DUV0) / 2), fy(G1 - 40.0), "ön oda", f7, GRAY, "mm")
    d.line([(fx(FT.BANT_X[0]), fy(BANT_F)), (fx(FT.BANT_X[1]), fy(BANT_F))], fill=TURUNCU, width=4)
    for xr in FT.RULO_X:
        d.ellipse([fx(xr - 20), fy(FT.RULO_Y + 20), fx(xr + 20), fy(FT.RULO_Y - 20)], fill=BG, outline=TURUNCU, width=2)
    xm = (FT.X_TUN0 + FT.X_TUN1) / 2.0
    for i in range(FT.N_URUN):
        xx = xm + (i - (FT.N_URUN - 1) / 2.0) * FT.ADIM
        d.ellipse([fx(xx - 150), fy(BANT_F + 28.0), fx(xx + 150), fy(BANT_F + 2.0)], fill=URUN, outline=(180, 140, 70), width=1)
    txt(fx(xm), fy(FT.TUN_Y[1] - 40.0), "ISITILAN %s · kızılötesi üst + alt · aynı anda %d ürün (adım %s) · bant üstü %s" % (sayi(FT.ODA), FT.N_URUN, sayi(FT.ADIM), sayi(BANT_F)), f7, TURUNCU, "mm")
    olcu_h(fx(FT.X_TUN0), fx(FT.X_TUN1), fy(G1) + 30, "ısıtılan %s" % sayi(FT.ODA), f8, TURUNCU)
    txt(fx(xm), fy(G1 - 30.0), "gövde ön yüzü 79 mm ÖNDE (çıkıntı · y %s–%s) → üst görünüş" % (sayi(G0), sayi(G1)), f7, RED, "mm")
    # giriş bandı (ön odada) + çıkış ölü plakası
    d.rectangle([fx(2509.0), fy(BANT_F), fx(2565.5), fy(BANT_F - 10.0)], fill=EVC, outline=BUZ, width=2)
    d.rectangle([fx(3997.0), fy(BANT_F - 0.5), fx(4018.0), fy(BANT_F - 3.0)], fill=INK)
    # üst: ışınım kalkanı + 10 takoz + 4 mm raf · SOL kutu yedeği 320 · SAĞ kompresör · davlumbaz arka yarı
    d.line([(fx(FT.X_F0 + 10), fy(FT.ISI_KALKANI_Y[0])), (fx(FT.X_F1 - 10), fy(FT.ISI_KALKANI_Y[0]))], fill=GRAY, width=2)
    for xt in sorted(set(x_ for x_, z_ in FT.TAKOZ_XZ)):
        d.rectangle([fx(xt - 8), fy(FT.UST_RAF_Y[0]), fx(xt + 8), fy(G1)], fill=BG, outline=INK, width=1)
    d.rectangle([fx(FT.X_F0 + 10), fy(FT.UST_RAF_Y[1]), fx(FT.X_F1 - 10), fy(FT.UST_RAF_Y[0])], fill=INK)
    drect(fx(FT.X_F0 + 3), fy(2027.0), fx(FT.X_F1 - 3), fy(FT.ISI_KALKANI_Y[1] + 2.0), GRAY, 1)
    d.rectangle([fx(2520.0), fy(2028.0), fx(3324.0), fy(1516.0)], fill=(252, 240, 215), outline=LINE, width=2)
    satirlar(fx(2922.0), fy(1800.0), "PİZZA KUTUSU YEDEĞİ · TEK YER|320 kutu düz · 804 × 404 × 512|şarjör 567 + 320 = 887 = 3,1 gün", f8, INK, 20)
    d.rectangle([fx(3600.0), fy(2026.0), fx(3980.0), fy(1516.0)], fill=BG, outline=ACC, width=2)
    satirlar(fx(3790.0), fy(1800.0), "KOMPRESÖR|JUN-AIR OF302-15B|25 kg · 380 × 380 × 510", f8, ACC, 20)
    satirlar(fx(3462.0), fy(1900.0), "DAVLUMBAZ|arka yarıda|fan + filtre", f7, GRAY, 17)
    txt(fx(3462.0), fy(1540.0), "raf 4 mm · 10 takoz · 99 kg", f7, INK, "mm")
    modul_etiketi(X_F, W_F, "MODÜL F · TP10 FIRIN (firin_tp10_cad_v6) · özel sipariş", "1500 × 909 × 2030 · dolap 123–956 · gövde %s–%s · bant %s · 79 öne" % (sayi(G0), sayi(G1), sayi(BANT_F)))
    olcu_h(fx(X_F), fx(X_F + W_F), fy(H_MAK) - 26, sayi(W_F), f11, INK)


'''
blok("def ciz_F(taban_parcalar):", "def ciz_K():", F_YENI)
# ---------------- K: kapaksız, tabanda kompresör yok ----------------
degis('    """v12 · kesme_cad_v1: K bandı · kesici + sprey aynı kafada · itici · taban: içecek yedeği önde, arkada kompresör + tereyağı + pano"""\n    kabin(X_K, W_K, 0.0, H_MAK, "K · KESME + SPREY")\n    kapak(X_K, 1.5, W_K - 1.5, Y_ALT + 3.0, H_B - 3.0)',
      '    """v14 · kesme_cad_v2: ön kapak YOK · K bandı · kesici + sprey aynı kafada · itici · taban: içecek yedeği önde, arkada tereyağı + pano (kompresör fırın üstünde)"""\n    kabin(X_K, W_K, 0.0, H_MAK, "K · KESME + SPREY · kapaksız")')
degis('    satirlar(fx(X_K + 510.0), fy(560.0), "ARKADA:|KOMPRESÖR|JUN-AIR|130–640", f7, INK, 17)\n', '')
degis('modul_etiketi(X_K, W_K, "MODÜL K · KESME + SPREY",', 'modul_etiketi(X_K, W_K, "MODÜL K · KESME + SPREY (kesme_cad_v2)",')

# ---------------- C: tekne v24 · X motoru solda · aktarma iticisi ----------------
degis("    TEK = (145.0, 2585.0, 1061.5, 1091.5); RAY = (200.0, 2485.0, 1080.5, 1095.5); KAS = (165.0, 2535.0)",
      "    TEK = (100.0, 2495.0, 1061.5, 1091.5); RAY = (200.0, 2485.0, 1080.5, 1095.5); KAS = (140.0, 2350.0)   # v14: topping_cad_v24")
degis('    d.rectangle([fx(2507.0), fy(1121.0), fx(2563.0), fy(1064.0)], fill=BG, outline=INK, width=2)\n    txt(fx(2535.0), fy(1140.0), "X MOTORU", f7, INK, "mm")',
      '    drect(fx(111.5), fy(1121.5), fx(168.5), fy(1064.5), INK, 1)\n    txt(fx(140.0), fy(1040.0), "X MOTORU (arkada)", f7, INK, "mm")')
degis('    d.rectangle([fx(2504.0), fy(BANT_F), fx(2926.0), fy(1103.0)], fill=EVC, outline=BUZ, width=1)\n    txt(fx(2715.0), fy(1088.0), "AKTARMA BANDI · bıçak burunlu", f7, BUZ, "mm")',
      '''    _i0 = IT.PC[0] + IT.S_STROK0 - IT.MY["Z"] / 2.0; _i1 = IT.PC[0] + IT.S_STROK0 + IT.STROK + IT.MY["Z"] / 2.0
    d.rectangle([fx(_i0), fy(IT.Y_TABLA_YUZ + IT.MY["H"]), fx(_i1), fy(IT.Y_TABLA_YUZ)], outline=ACC, width=3)
    _xe = IT.PC[0] + IT.S_END
    d.rectangle([fx(_xe - 10.0), fy(IT.BAR_Y1), fx(_xe), fy(IT.BAR_Y0)], fill=ACC)
    d.line([(fx(_xe - 5.0), fy(IT.BAR_Y1)), (fx(_xe - 5.0), fy(IT.Y_TABLA_YUZ))], fill=ACC, width=2)
    txt(fx(_i1) + 6, fy(1300.0), "AKTARMA İTİCİSİ · SMC MY1B16-250", f7, ACC, "la")
    txt(fx(_i1) + 6, fy(1300.0) + 17, "düz 170 · disk → fırın giriş bandı", f7, ACC, "la")''')
degis('+ topping_cad_v23 tabla ·', '+ topping_cad_v24 tabla ·')

# plan · C/F: itici + giriş bandı · tekne uyarısı · hava hattı
degis('''    dline((fx(2375.0), py(-790.0)), (fx(4230.0), py(-790.0)), (60, 110, 200), 3, 10, 6)
    dline((fx(4230.0), py(-790.0)), (fx(4230.0), py(-765.0)), (60, 110, 200), 3, 10, 6)
    txt(fx(3300.0), py(-790.0) - 14, "HAVA ANA HATTI Ø10 · K tabanı arkasındaki kompresör → F tabanı arkası → TOPPING şartlandırıcısı", f7, (60, 110, 200), "mm")''',
      '''    dline((fx(2375.0), py(-790.0)), (fx(3790.0), py(-790.0)), (60, 110, 200), 3, 10, 6)
    dline((fx(3790.0), py(-790.0)), (fx(3790.0), py(-660.0)), (60, 110, 200), 3, 10, 6)
    txt(fx(3150.0), py(-790.0) - 14, "HAVA ANA HATTI Ø10 · fırın üstü raftaki kompresör (sağ) → davlumbaz bölmesi → TOPPING şartlandırıcısı", f7, (60, 110, 200), "mm")''')
degis('''    drect(fx(2504.0), py(-315.0), fx(2926.0), py(-25.0), BUZ, 2)
    txt(fx(2715.0), py(-5.0) + 14, "aktarma bandı", f7, BUZ, "mm")''',
      '''    d.rectangle([fx(_i0p), py(IT.PC[1] + IT.W_AXIS - IT.MY["NW"] / 2.0), fx(_i1p), py(IT.PC[1] + IT.W_AXIS + IT.MY["NW"] / 2.0)], outline=ACC, width=3)
    d.rectangle([fx(IT.PC[0] + IT.S_END - 10.0), py(IT.PC[1] + IT.BAR_W0), fx(IT.PC[0] + IT.S_END), py(IT.PC[1] + IT.BAR_W1)], fill=ACC)
    txt(fx((_i0p + _i1p) / 2.0), py(IT.PC[1] + IT.W_AXIS - IT.MY["NW"] / 2.0) - 12, "itici MY1B16-250 · ekseni z %s · düz 170 (2337 → 2507)" % sayi(IT.PC[1] + IT.W_AXIS), f7, ACC, "mm")
    d.rectangle([fx(2509.0), py(-341.0), fx(2565.5), py(-10.0)], fill=EVC, outline=BUZ, width=2)''')
degis('''    for xt in (1957.5, 2337.0):''', '''    _i0p = IT.PC[0] + IT.S_STROK0 - IT.MY["Z"] / 2.0; _i1p = IT.PC[0] + IT.S_STROK0 + IT.STROK + IT.MY["Z"] / 2.0
    for xt in (1957.5, 2337.0):''')
degis('''    txt(fx(1350.0), py(-790.0) - 40, "UYARI · tekne modül C'nin sağ kenarını 85 mm, sağ kasnak 35 mm aşıyor; sol ucu modül A'nın içinde (x 145) — İSTASYON = KAPALI ÜRÜN kuralına aykırı, KARAR BEKLİYOR", f7, RED, "mm")''',
      '''    txt(fx(1350.0), py(-790.0) - 40, "v24: tekne x 100–2495 modülün içinde biter · X motoru sol uçta teknenin arkasında · sol ucu A bölgesinde (açıcı altı park) — A ile C arasında iç duvar yok", f7, GRAY, "mm")''')
degis('"TABLA HATTI z −170 = fırın bandı ekseni · park x 350 → fırın ağzı x 2337 · HGR15 ray x 200–2485 (tabanın altında)"',
      '"TABLA HATTI z −170 = fırın ürün ekseni · park x 350 → aktarma x 2337 · itici düz 170 → fırın giriş bandı · HGR15 ray x 200–2485"')

# plan · F (TP10, 79 öne)
blok("    # F\n    x0 = X_F + 50.0", "    # K (v12 · kesme_cad_v1)", '''    # F (v14 · firin_tp10_cad_v6 · 79 öne)
    zb0, zb1 = -FT.D_TP + FT.ZS, FT.ZS
    d.rectangle([fx(FT.X_F0), py(zb0), fx(FT.X_F1), py(zb1)], fill=SOFT, outline=INK, width=2)
    d.rectangle([fx(FT.X_TUN0), py(FT.TUNEL_Z_D[0]), fx(FT.X_TUN1), py(FT.TUNEL_Z_D[1])], fill=SICAK, outline=TURUNCU, width=2)
    tarali(fx(FT.X_DUV0), py(FT.TUNEL_Z_D[0]), fx(FT.X_TUN0), py(zb1 - 2), (226, 214, 190), 11)
    tarali(fx(FT.X_TUN1), py(FT.TUNEL_Z_D[0]), fx(FT.X_F1 - 2), py(zb1 - 2), (226, 214, 190), 11)
    drect(fx(FT.BANT_X[0]), py(FT.BANT_Z_D[0]), fx(FT.BANT_X[1]), py(FT.BANT_Z_D[1]), BUZ, 1)
    xm = (FT.X_TUN0 + FT.X_TUN1) / 2.0
    for i in range(FT.N_URUN):
        xx = xm + (i - (FT.N_URUN - 1) / 2.0) * FT.ADIM
        d.ellipse([fx(xx - 150), py(ZT - 150.0), fx(xx + 150), py(ZT + 150.0)], fill=URUN, outline=(180, 140, 70), width=1)
        txt(fx(xx), py(ZT), "Ø300", f7, (140, 100, 40), "mm")
    txt(fx(xm), py(-540.0), "TEKNİK BÖLME ≈239 (arkada) · sürücü · SSR · bant motoru · gergi · ekran arka yüzde", f7, GRAY, "mm")
    d.rectangle([fx(FT.X_F0), py(0.0), fx(FT.X_F1), py(FT.ZS)], outline=RED, width=3)
    txt(fx(xm), py(FT.ZS / 2.0), "ÇIKINTI 79 · gövde ön yüzün önünde (Kemal) · F 830 + 79 = 909", f7, RED, "mm")
    olcu_h(fx(FT.X_TUN0), fx(FT.X_TUN1), py(-830) - 58, "ısıtılan %s" % sayi(FT.ODA), f8, TURUNCU)
''')
# ---------------- tablalı: F taban dolabı (kapaksız · pizza gözü BOŞ) ----------------
degis('''    kapak(X_F, 666.0, 1470.0, 130.0, 1030.0, "PİZZA KUTUSU YEDEĞİ · 553 · önde|804 × 404 × 885 · şarjör 567 + 553 = 1120 = 4 gün", yl=985.0, fill=(252, 240, 215))''',
      '''    txt(fx(X_F + 1068.0), fy(990.0), "BOŞ (v52: kutu yedeği fırın üstüne alındı) · önde 804 × 823 × 404", f7, GRAY, "mm")''')
degis("    kot_cizgileri((Y_ALT, H_B, TEPSI_E, P, 1320.0, 1486.0, 1680.0, 1772.0, H_MAK))",
      "    kot_cizgileri((Y_ALT, FT.YG0, H_B, TEPSI_E, P, 1320.0, FT.YG1, FT.UST_RAF_Y[1], 1680.0, 1772.0, H_MAK))")

# ---------------- başlık ----------------
degis("TEKNİK RESİM  v13  ·  MONTAJ = hat_montaj_v47  ·  TOPPING = topping_uno_cad_v5 (4 UNO + kaşar/sucuk kaseti · kama yarık) + topping_cad_v24 tabla · K = kesme_cad_v1 · E = kutu_cad_v3",
      "TEKNİK RESİM  v14  ·  MONTAJ = hat_montaj_v52  ·  F = firin_tp10_cad_v6 (TP10 · 1500 · 79 öne)  ·  TOPPING = topping_uno_cad_v9 + topping_cad_v24 · itici_cad_v3 · K = kesme_cad_v2 · E = kutu_cad_v3")
degis("bıçak burunlu bant fırına çeker → K bandı", "aktarma iticisi (SMC MY1B16-250) düz 170 iter → fırın giriş bandı → TP10 fırın (79 mm öne, ürün ekseni −170 düz) → K bandı")
degis("· hava: kompresör K tabanında  ·", "· hava: kompresör fırın üstü rafta (sağ) · pizza kutusu yedeği fırın üstü solda 320 (887 = 3,1 gün)  ·")
degis("ölçüler mm  ·  26 Eylül 2026\")\n    # ---- A · AÇICI", "ölçüler mm  ·  27 Eylül 2026\")\n    # ---- A · AÇICI")
degis('"MODÜL C · TOPPING v2 (topping_uno_cad_v4) · 4 UNO + 2 bizim kaset · havalı"', '"MODÜL C · TOPPING v2 (topping_uno_cad_v9 + topping_cad_v24) · 4 UNO + 2 bizim kaset · havalı · itici"')

# ---------------- parça listesi ----------------
degis('''        ("HAVA", "JUN-AIR OF302-15B yağsız kompresör · 15 L · 43 L/dk @ 7 bar · K tabanı ARKADA (130–640), üstünde tereyağı tankı + pano · K kesicisi de bu hattan · Ø10 ana hat F tabanı arkasından TOPPING'e", "1", "380 × 380 × 510 · 25 kg · arka sacta ızgara"),''',
      '''        ("HAVA", "JUN-AIR OF302-15B yağsız kompresör · 15 L · 43 L/dk @ 7 bar · FIRIN ÜSTÜ RAFTA SAĞDA (x 3600–3980 · 1516–2026) · K kesicisi de bu hattan · Ø10 ana hat davlumbaz bölmesinden TOPPING'e", "1", "380 × 380 × 510 · 25 kg · ortam sınırı 40 °C [föy] · raf üstü sıcaklığı pilotta ölçülecek"),''')
degis('''        ("BANDA AKTARMA", "BIÇAK BURUNLU · bant Ø20 burun silindirine dolanır, üst yüzü diskin 2 mm altı (1166) · pide boşluğu kendi gövdesiyle köprüler", "1", "itici ve köprü YOK · Ø60 kauçuk tahrik silindiri + PTFE kaplı cam elyaf bant · v13: bant motoru ARKADA, tahrik silindiriyle eş eksenli · ön sac + mil uçları ön yüzün içinde · çıkış yarığı 294 × 44"),''',
      '''        ("AKTARMA İTİCİSİ", "itici_cad_v3 · SMC MY1B16-250 kolsuz silindir x boyunca DÜZ · pivotlu çubuk 170 × 30, dönüşte sabit pime rolan makarayla 90° kalkar · pideyi diskten (2337) fırın giriş bandına (2507) iter", "1", "ekseni z −212 · çubuk 1170–1200 · denetim TEMİZ"),
        ("GİRİŞ BANDI", "F ön odasında (bizim) · PTFE 320 · Ø20 burun + tahrik · STP-MTR-23079 + GT2 · disk kenarı 2507 → fırın bandı 2568", "1", "x 2509–2565,5 · üstü 1166"),''')
degis('''        ("MODÜL F", "KONVEYÖR FIRIN · özel · elektrikli · hazne 1400 · aynı anda 4 ürün · taban dolabı: önde bulaşık + temizlik + pizza kutusu yedeği · arkada deterjan + robot kontrol + ana pano + UPS", "1", "1500 × 830 × 2030 · gövde 1060–1486 · bant 1166 · AÇIK: bant altı pay 106 (alt ısıtma)"),''',
      '''        ("MODÜL F", "TP10 KESİTLİ KONVEYÖR FIRIN (firin_tp10_cad_v6) · Sveba Dahlen TP10 kesiti 730 × 517, gövde 1500 ÖZEL SİPARİŞ · kızılötesi üst + alt · ısıtılan 1316 · aynı anda 4 ürün · 79 mm ÖNE · üstte raf 4 mm + 10 takoz: SOL kutu yedeği 320, SAĞ kompresör · davlumbaz arka yarı · taban dolabı (kapaksız): önde bulaşık + temizlik, pizza gözü BOŞ · arkada deterjan + robot kontrol + ana pano + UPS", "1", "1500 × 909 × 2030 · dolap 123–956 · gövde 956–1473 · bant 1166 · raf yükü 99 kg → şartname: 10 × M6 saplama"),''')
degis('"KESME + SPREY (kesme_cad_v1) ·', '"KESME + SPREY (kesme_cad_v2 · ön kapak yok) ·')
degis("taban: önde içecek yedeği · arkada kompresör + tereyağı tankı 3 L + pano", "taban: önde içecek yedeği · arkada tereyağı tankı 3 L + pano (kompresör fırın üstünde)")
degis('"İÇECEK 120 kutu (K tabanı önde, soğutmasız) · PİZZA KUTUSU 553 (F tabanı önde) · kaşar + sucuk 2 gün (B/K4 deposu) → hepsi 4 gün"',
      '"İÇECEK 120 kutu (K tabanı önde, soğutmasız) → 4 gün · PİZZA KUTUSU 320 TEK YERDE fırın üstü sol → şarjörle 887 = 3,1 gün · kaşar + sucuk 2 gün (B/K4 deposu) → 4 gün"')

# ---------------- yerleşim düzeltmeleri (ilk çıktıdan) ----------------
degis('kabin(X_F, W_F, 0.0, H_MAK, "F · TP10 KESİTLİ KONVEYÖR FIRIN · 1500 ÖZEL SİPARİŞ · 79 mm ÖNE · 4 ürün")', 'kabin(X_F, W_F, 0.0, H_MAK, "F · TP10 FIRIN · 1500 özel sipariş · 79 mm öne")')
degis('kabin(X_K, W_K, 0.0, H_MAK, "K · KESME + SPREY · kapaksız")', 'kabin(X_K, W_K, 0.0, H_MAK, "K · KESME + SPREY")')
degis('    olcu_h(fx(FT.X_TUN0), fx(FT.X_TUN1), fy(G1) + 30, "ısıtılan %s" % sayi(FT.ODA), f8, TURUNCU)\n', '')
degis('    txt(fx(3462.0), fy(1540.0), "raf 4 mm · 10 takoz · 99 kg", f7, INK, "mm")', '    satirlar(fx(3462.0), fy(1640.0), "raf 4 mm|10 takoz|99 kg", f7, INK, 17)')
degis('txt(fx(X_F + 1068.0), fy(990.0), "BOŞ (v52:', 'txt(fx(X_F + 1068.0), fy(936.0), "BOŞ (v52:')
degis('''    txt(fx(_i1) + 6, fy(1300.0), "AKTARMA İTİCİSİ · SMC MY1B16-250", f7, ACC, "la")
    txt(fx(_i1) + 6, fy(1300.0) + 17, "düz 170 · disk → fırın giriş bandı", f7, ACC, "la")''',
      '''    pass''')
degis('    txt(X(1150.0), fy(1200.0), "ağızlar tabla ekseninde', '    etiket(fx(2130.0), fy(1252.0), "AKTARMA İTİCİSİ · SMC MY1B16-250 · düz 170", f7, ACC, ACC)' + NL + '    txt(X(1150.0), fy(1200.0), "ağızlar tabla ekseninde')
degis('''    txt(fx((_i0p + _i1p) / 2.0), py(IT.PC[1] + IT.W_AXIS - IT.MY["NW"] / 2.0) - 12, "itici MY1B16-250 · ekseni z %s · düz 170 (2337 → 2507)" % sayi(IT.PC[1] + IT.W_AXIS), f7, ACC, "mm")''',
      '''    txt(fx(2495.0), py(FT.ZS) + 50, "itici MY1B16-250 · ekseni z %s · düz 170 (2337 → 2507) · giriş bandı 2509–2566" % sayi(IT.PC[1] + IT.W_AXIS), f7, ACC, "rm")''')
degis('olcu_h(fx(FT.X_TUN0), fx(FT.X_TUN1), py(-830) - 58, "ısıtılan %s"', 'olcu_h(fx(FT.X_TUN0), fx(FT.X_TUN1), py(-830) - 70, "ısıtılan %s"')
degis('    txt(fx(HAT / 2), py(-830) - 30, "ARKA", f9, GRAY, "mm")', '    txt(fx(1200.0), py(-830) - 30, "ARKA", f9, GRAY, "mm")')
_i = s.index('    baslik("AUTOKITCH  ·  ATOSA TABLALI HAT  ·  TEKNİK RESİM  v14'); _j = s.index("    # ---- A · AÇICI", _i)
s = s[:_i] + '''    baslik("AUTOKITCH  ·  ATOSA TABLALI HAT  ·  TEKNİK RESİM  v14  ·  MONTAJ v52  ·  F TP10 1500 (79 öne)  ·  TOPPING uno v9 + v24  ·  itici v3  ·  K kesme v2  ·  E kutu v3  ·  B store v5  ·  HAT 5430 × 2030 × 830",
           "ön · üst · yan görünüş  ·  günde 80 pide + 200 lahmacun (+ pizza)  ·  gövdeler yerden 123, istasyon tabanları 1060 (F 956)  ·  ürün: disk → konili açıcı → TOPPING → itici → TP10 fırın (79 öne, eksen −170 düz) → K → kutu  ·  kompresör + kutu yedeği (320) fırın üstünde  ·  TEK FR5 yer rayında  ·  ölçüler mm  ·  27 Eylül 2026")
''' + s[_j:]
s = s.replace("HAT_ATOSA_TABLALI_v13_HD.png", "HAT_ATOSA_TABLALI_v14_HD.png").replace("HAT_ATOSA_TABLALI_v13_EKRAN.png", "HAT_ATOSA_TABLALI_v14_EKRAN.png")
io.open(os.path.join(U, "teknik_hat_atosa_tablali_v14.py"), "w", encoding="utf-8").write(s)
print("teknik_hat_atosa_tablali_v14.py yazildi")
