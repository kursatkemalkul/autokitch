# -*- coding: utf-8 -*-
"""teknik_firin_tp10_v3 → teknik_firin_tp10_v4 (27 Eyl 2026): FIRIN 79 mm ÖNE (firin_tp10_cad_v5): gövde ön yüzün önünde çıkıntı 0…+79,
ürün fırında −170 (düz), K giriş çiti yok, TOPPING cebi yok (v24 teknesi 2500'de biter). Üst görünüş + yan kesit kayar; ön görünüş aynı."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "teknik_firin_tp10_v3.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


def sil_satir(onek):
    """onek ile başlayan (tek) satırı sil"""
    global s
    i = s.index(onek); assert s.count(onek) == 1, onek
    j = s.index("\n", i) + 1
    s = s[:i] + s[j:]


d('"""AUTOKITCH · F FIRIN (AYRI SÜRÜM) · TP10 KESİTİ, GÖVDESİ 1500\'E UZATILMIŞ · TEKNİK RESİM v3 (26 Eyl 2026)',
  '"""AUTOKITCH · F FIRIN · TP10 KESİTİ · 1500 · TEKNİK RESİM v4 (27 Eyl 2026): FIRIN 79 mm ÖNE (firin_tp10_cad_v5) — çıkıntı 0…+79, ürün −170 düz, K giriş çiti yok.\nv3 (26 Eyl 2026)')
d("import firin_tp10_cad_v2 as FT", "import firin_tp10_cad_v5 as FT")
d("TUN_Y, TUN_Z, BZ = FT.TUN_Y, FT.TUNEL_Z, FT.BANT_Z", "TUN_Y, TUN_Z, BZ = FT.TUN_Y, FT.TUNEL_Z_D, FT.BANT_Z_D                              # v4: DÜNYA (79 öne kaymış)")
d("ADIM, ZUF = FT.ADIM, FT.Z_URUN_FIRIN", "ADIM, ZUF = FT.ADIM, FT.Z_URUN_FIRIN_D")
d("CEP = FT.CEP_AGIZ", "ZS = FT.ZS; DTP0, DTP1 = ZS, -FT.D_TP + ZS                                            # v4: gövde ön yüzü +79 · arka yüzü −651\nGBZ = (FT.GB_Z[0] + ZS, FT.GB_Z[1] + ZS); GBMZ = FT.GB_MOTOR[2] + ZS")
# ---- ön görünüş ----
sil_satir("    drect(fx(CEP[0]), fy(CEP[2]), fx(2586), fy(CEP[1]), RED, 1, 5, 3)")
sil_satir("    isaret(fx(2586) + 40, fy(1075), 1)")
d('''    drect(fx(2490), fy(1135), fx(2580), fy(1064.5), KOMSU, 1, 5, 3)
    drect(fx(2400), fy(1091.5), fx(2585), fy(1061.5), KOMSU, 1, 5, 3)
    txt(fx(X_F0) - 16, fy(1010), "TOPPING X tahriki + mekanizma teknesi", f7, KOMSU, "rm")
    txt(fx(X_F0) - 16, fy(1010) + 20, "F'ye 80–85 mm taşıyor (v47'de de)", f7, RED, "rm")''',
  '''    drect(fx(2400), fy(1091.5), fx(2500), fy(1061.5), KOMSU, 1, 5, 3)
    txt(fx(X_F0) - 16, fy(1010), "TOPPING mekanizma teknesi (v24)", f7, KOMSU, "rm")
    txt(fx(X_F0) - 16, fy(1010) + 20, "2500'de biter · cep yok", f7, KOMSU, "rm")''')
sil_satir("    d.rectangle([fx(FT.CC_A[0]), fy(FT.CIT_Y[1]), fx(FT.CC_B[0]), fy(FT.CIT_Y[0])], fill=(245, 245, 240), outline=ACC, width=2)")
sil_satir("    balon(fx((FT.CC_A[0] + FT.CC_B[0]) / 2), fy(FT.CIT_Y[1]), fx((FT.CC_A[0] + FT.CC_B[0]) / 2), fy(1380), 9)")
d('''    olcu_h(fx(X_F0), fx(X_F1), fy(0) + 44, "F modülü %s" % sayi(X_F1 - X_F0), f9, ACC)''',
  '''    olcu_h(fx(X_F0), fx(X_F1), fy(0) + 44, "F modülü %s · derinlik 830 + çıkıntı %s = %s" % (sayi(X_F1 - X_F0), sayi(ZS), sayi(DZ + ZS)), f9, ACC)
    txt(fx(XC), fy(YG1) - 62, "gövde ön yüzün %s mm ÖNÜNDE (çıkıntı, y %s–%s) → üst görünüş / yan kesit" % (sayi(ZS), sayi(YG0), sayi(YG1)), f8, RED, "mm")''')
# ---- üst görünüş ----
d('txt(FX0, PY0 - 60, "ÜST GÖRÜNÜŞ (ürün yolu: merkez çizgisi · diskte kayma · K bandında çit)", f16, ACC)',
  'txt(FX0, PY0 - 60, "ÜST GÖRÜNÜŞ (ürün yolu DÜZ z −170 · fırın 79 öne · çıkıntı ön yüzün önünde)", f16, ACC)')
d('    d.rectangle([fx(OLU[0]), pz(FT.GB_Z[0]), fx(OLU[1]), pz(FT.GB_Z[1])], fill=(230, 238, 250), outline=ACC, width=1)',
  '    d.rectangle([fx(OLU[0]), pz(GBZ[0]), fx(OLU[1]), pz(GBZ[1])], fill=(230, 238, 250), outline=ACC, width=1)')
i0 = s.index("    nx_, nz_ = math.sin(math.radians(20.0)), math.cos(math.radians(20.0))\n    pts = [FT.CC_A, FT.CC_B")
i1 = s.index("    balon(fx(4150), pz(-380), fx(4150), pz(-DZ) - 40, 9)\n")
i1 = s.index("\n", i1) + 1
s = s[:i0] + "    # v4: K giriş çiti YOK (ürün −170'te düz gelir)\n" + s[i1:]
d('''    d.rectangle([fx(X_F0), pz(-FT.D_TP), fx(X_F1), pz(0)], fill=PASL, outline=INK, width=3)
    d.rectangle([fx(D0), pz(-FT.D_TP), fx(X_F1), pz(TUN_Z[0] - 5.5)], fill=(222, 226, 232), outline=INK, width=1)
    d.rectangle([fx(X_F0) + 2, pz(-FT.D_TP) + 2, fx(D0), pz(0) - 2], fill=(240, 242, 245))''',
  '''    d.rectangle([fx(X_F0), pz(DTP1), fx(X_F1), pz(DTP0)], fill=PASL, outline=INK, width=3)
    d.rectangle([fx(D0), pz(DTP1), fx(X_F1), pz(TUN_Z[0] - 5.5)], fill=(222, 226, 232), outline=INK, width=1)
    d.rectangle([fx(X_F0) + 2, pz(DTP1) + 2, fx(D0), pz(DTP0) - 2], fill=(240, 242, 245))
    d.rectangle([fx(X_F0), pz(0), fx(X_F1), pz(DTP0)], outline=RED, width=3)                                   # v4: ÇIKINTI
    txt(fx(XC), pz(DTP0 / 2.0), "ÇIKINTI %s · gövde ön yüzün önünde · y %s–%s" % (sayi(ZS), sayi(YG0), sayi(YG1)), f8, RED, "mm")''')
d('''    d.rectangle([fx(XC - FT.EKRAN[0] / 2), pz(-FT.D_TP) - 2, fx(XC + FT.EKRAN[0] / 2), pz(-FT.D_TP) + 7], fill=INK)
    balon(fx(XC + 60), pz(-FT.D_TP) + 4, fx(XC + 200), pz(-FT.D_TP) + 60, 12)
    for fx_ in (D0 + 76.0, X_F1 - 140.0):
        d.ellipse([fx(fx_ - FT.FAN_R), pz(-FT.D_TP) - 2, fx(fx_ + FT.FAN_R), pz(-FT.D_TP) + 2], outline=INK, width=1)''',
  '''    d.rectangle([fx(XC - FT.EKRAN[0] / 2), pz(DTP1) - 2, fx(XC + FT.EKRAN[0] / 2), pz(DTP1) + 7], fill=INK)
    balon(fx(XC + 60), pz(DTP1) + 4, fx(XC + 200), pz(DTP1) + 60, 12)
    for fx_ in (D0 + 76.0, X_F1 - 140.0):
        d.ellipse([fx(fx_ - FT.FAN_R), pz(DTP1) - 2, fx(fx_ + FT.FAN_R), pz(DTP1) + 2], outline=INK, width=1)''')
d('''    drect(fx(RX1 - 32), pz(-586), fx(RX1 + 26), pz(-521), INK, 1, 4, 3)
    drect(fx(RX1 - 170), pz(-583), fx(RX1 - 32), pz(-523), INK, 1, 4, 3)
    balon(fx(RX1 - 100), pz(-553), fx(RX1 - 140), pz(-660), 10)
    drect(fx(2556), pz(-520), fx(RX0 - 18), pz(-500), INK, 1, 4, 3)
    balon(fx(2575), pz(-510), fx(2650), pz(-660), 11)''',
  '''    drect(fx(RX1 - 32), pz(-586 + ZS), fx(RX1 + 26), pz(-521 + ZS), INK, 1, 4, 3)
    drect(fx(RX1 - 170), pz(-583 + ZS), fx(RX1 - 32), pz(-523 + ZS), INK, 1, 4, 3)
    balon(fx(RX1 - 100), pz(-553 + ZS), fx(RX1 - 140), pz(-660 + ZS), 10)
    drect(fx(2556), pz(-520 + ZS), fx(RX0 - 18), pz(-500 + ZS), INK, 1, 4, 3)
    balon(fx(2575), pz(-510 + ZS), fx(2650), pz(-660 + ZS), 11)''')
d('''    d.rectangle([fx(GBX0), pz(FT.GB_Z[0]), fx(GBX1), pz(FT.GB_Z[1])], fill=(214, 196, 170), outline=INK, width=1)
    drect(fx(FT.GB_MOTOR[0] - 28.5), pz(FT.GB_MOTOR[2] - 76), fx(FT.GB_MOTOR[0] + 28.5), pz(FT.GB_MOTOR[2]), INK, 1, 5, 3)
    drect(fx(CEP[0]), pz(CEP[3]), fx(2586), pz(CEP[4]), RED, 1, 5, 3)
    isaret(fx(2586) + 22, pz(-30), 1)''',
  '''    d.rectangle([fx(GBX0), pz(GBZ[0]), fx(GBX1), pz(GBZ[1])], fill=(214, 196, 170), outline=INK, width=1)
    drect(fx(FT.GB_MOTOR[0] - 28.5), pz(GBMZ - 76), fx(FT.GB_MOTOR[0] + 28.5), pz(GBMZ), INK, 1, 5, 3)''')
d('''    drect(fx(2490), pz(-397.5), fx(2580), pz(-389.5), KOMSU, 1, 4, 3)
    drect(fx(2507), pz(-462), fx(2563), pz(-397.5), KOMSU, 1, 4, 3)
    drect(fx(2400), pz(-415), fx(2585), pz(-5), KOMSU, 1, 4, 3)''',
  '''    drect(fx(2400), pz(-415), fx(2500), pz(-5), KOMSU, 1, 4, 3)                                              # v4: tekne 2500'de biter''')
d('''    d.line([(fx(TAB_XC), pz(ZT)), (fx(TAB_XC), pz(ZUF))], fill=(200, 120, 40), width=3)
    pts = [(fx(x), pz(FT.urun_z(float(x)))) for x in range(int(TAB_XC), 4301, 8)]''',
  '''    pts = [(fx(x), pz(FT.urun_z(float(x)))) for x in range(int(TAB_XC), 4301, 8)]                          # v4: düz −170''')
d('''    txt(fx(TAB_XC) - 60, pz(ZT - TAB_R - 36), "diskte 79 mm arkaya (itici · AÇIK)", f7, (200, 120, 40), "mm")
    isaret(fx(TAB_XC) - 60 + d.textlength("diskte 79 mm arkaya (itici · AÇIK)", font=f7) / 2 + 24, pz(ZT - TAB_R - 36), 4)''',
  '''    txt(fx(TAB_XC) - 60, pz(ZT - TAB_R - 36), "aktarma iticisi DÜZ 170 (itici_cad_v3) · kayma yok", f7, (200, 120, 40), "mm")''')
d('''    txt(fx(T0) + 8, pz(-FT.D_TP + 40), "fırında ürün merkezi z %s (ön kenar %s · tünel duvarına 20)" % (sayi(ZUF), sayi(ZUF + 150)), f7, (200, 120, 40), "lm")
    xr = fx(4400) + 30
    olcu_v(xr, pz(-FT.D_TP), pz(0), "%s (föy)" % sayi(FT.D_TP), f8, INK, "r")
    olcu_v(xr, pz(-DZ), pz(-FT.D_TP), sayi(DZ - FT.D_TP), f7, INK, "r")
    olcu_v(fx(T1) - 40, pz(TUN_Z[0]), pz(0), "%s + %s" % (sayi(-TUN_Z[1]), sayi(TUN_Z[1] - TUN_Z[0])), f7, INK, "l")''',
  '''    txt(fx(T0) + 8, pz(DTP1 + 40), "fırında ürün merkezi z %s (ön kenar %s · tünel iç yüzü 0 → 20 pay) = tabla ekseni" % (sayi(ZUF), sayi(ZUF + 150)), f7, (200, 120, 40), "lm")
    xr = fx(4400) + 30
    olcu_v(xr, pz(DTP1), pz(DTP0), "%s (föy)" % sayi(FT.D_TP), f8, INK, "r")
    olcu_v(xr, pz(-DZ), pz(DTP1), sayi(DZ + DTP1), f7, INK, "r")
    olcu_v(xr, pz(0), pz(DTP0), "çıkıntı %s" % sayi(ZS), f8, RED, "r")
    olcu_v(fx(T1) - 40, pz(TUN_Z[0]), pz(DTP0), "%s + %s" % (sayi(DTP0 - TUN_Z[1]), sayi(TUN_Z[1] - TUN_Z[0])), f7, INK, "l")''')
sil_satir('    olcu_h(fx(FT.CC_A[0]), fx(FT.CC_B[0]), pz(-DZ) - 80, "K giriş çiti %s (20°) · %s → %s"')
d('    d.rectangle([fx(2492), pz(-417), fx(2498.5), pz(-13)], fill=BG, outline=KOMSU, width=1)\n    txt(fx(2492) - 6, pz(-430), "TOPPING çıkış yarığı çerçevesi v2 · −417…−13", f7, KOMSU, "rm")',
  '    d.rectangle([fx(2492), pz(-417), fx(2498.5), pz(-5)], fill=BG, outline=KOMSU, width=1)\n    txt(fx(2492) - 6, pz(-430), "TOPPING çıkış yarığı çerçevesi · −417…−5 (v5: ön çıta −13…−5)", f7, KOMSU, "rm")')
# ---- yan kesit ----
d('''    d.rectangle([sx(-FT.D_TP), fy(YG1), sx(0), fy(YG0)], fill=PASL, outline=INK, width=3)
    tarali(sx(TUN_Z[1]), fy(YG1) + 2, sx(0) - 2, fy(YG0) - 2, (214, 216, 222), 9)''',
  '''    d.rectangle([sx(DTP1), fy(YG1), sx(DTP0), fy(YG0)], fill=PASL, outline=INK, width=3)
    tarali(sx(TUN_Z[1]), fy(YG1) + 2, sx(DTP0) - 2, fy(YG0) - 2, (214, 216, 222), 9)''')
d('''    d.rectangle([sx(-FT.D_TP), fy(YG1), sx(TUN_Z[0] - 5.5), fy(YG0)], fill=(222, 226, 232), outline=INK, width=1)
    balon(sx((-FT.D_TP + TUN_Z[0]) / 2), fy((YG0 + YG1) / 2), sx((-FT.D_TP + TUN_Z[0]) / 2) - 40, fy(YG1) - 40, 12)
    d.rectangle([sx(-FT.D_TP) - 9, fy(YG0 + FT.EKRAN[2] + FT.EKRAN[1]), sx(-FT.D_TP), fy(YG0 + FT.EKRAN[2])], fill=INK)''',
  '''    d.rectangle([sx(DTP1), fy(YG1), sx(TUN_Z[0] - 5.5), fy(YG0)], fill=(222, 226, 232), outline=INK, width=1)
    balon(sx((DTP1 + TUN_Z[0]) / 2), fy((YG0 + YG1) / 2), sx((DTP1 + TUN_Z[0]) / 2) - 40, fy(YG1) - 40, 12)
    d.rectangle([sx(DTP1) - 9, fy(YG0 + FT.EKRAN[2] + FT.EKRAN[1]), sx(DTP1), fy(YG0 + FT.EKRAN[2])], fill=INK)
    d.rectangle([sx(0), fy(YG1), sx(DTP0), fy(YG0)], outline=RED, width=3)                                      # v4: çıkıntı
    txt(sx(DTP0) + 8, fy(YG1) - 24, "çıkıntı %s" % sayi(ZS), f8, RED, "lm")''')
d('''    olcu_h(sx(-FT.D_TP), sx(0), fy(H_MAK) - 30, "%s (föy)" % sayi(FT.D_TP), f8, INK)
    olcu_h(sx(-DZ), sx(-FT.D_TP), fy(H_MAK) - 30, sayi(DZ - FT.D_TP), f7, INK)
    olcu_h(sx(-DZ), sx(0), fy(H_MAK) - 70, "F %s" % sayi(DZ), f8, ACC)
    olcu_h(sx(-FT.D_TP), sx(TUN_Z[0] - 5.5), fy(YG0) + 90, "≈ 239", f7, INK)
    olcu_h(sx(TUN_Z[0]), sx(TUN_Z[1]), fy(YG0) + 90, "≈ %s" % sayi(TUN_Z[1] - TUN_Z[0]), f7, INK)
    olcu_h(sx(TUN_Z[1]), sx(0), fy(YG0) + 90, "≈ %s" % sayi(-TUN_Z[1]), f7, INK)''',
  '''    olcu_h(sx(DTP1), sx(DTP0), fy(H_MAK) - 30, "%s (föy)" % sayi(FT.D_TP), f8, INK)
    olcu_h(sx(-DZ), sx(DTP1), fy(H_MAK) - 30, sayi(DZ + DTP1), f7, INK)
    olcu_h(sx(-DZ), sx(DTP0), fy(H_MAK) - 70, "F %s + çıkıntı %s = %s" % (sayi(DZ), sayi(ZS), sayi(DZ + ZS)), f8, ACC)
    olcu_h(sx(DTP1), sx(TUN_Z[0] - 5.5), fy(YG0) + 90, "≈ 239", f7, INK)
    olcu_h(sx(TUN_Z[0]), sx(TUN_Z[1]), fy(YG0) + 90, "≈ %s" % sayi(TUN_Z[1] - TUN_Z[0]), f7, INK)
    olcu_h(sx(TUN_Z[1]), sx(DTP0), fy(YG0) + 90, "≈ %s" % sayi(DTP0 - TUN_Z[1]), f7, INK)''')
d('''    xd = sx(0) + 110''', '''    xd = sx(DTP0) + 110''')
d('''        d.line([(sx(0) + 6, fy(yy)), (sx(0) + 22, fy(yy))], fill=c, width=2)
        txt(sx(0) + 28, fy(yy), sayi(yy), f7, c, "lm")
    isaret(sx(0) + 330, fy((H_B + YG0) / 2), 2)''',
  '''        d.line([(sx(DTP0) + 6, fy(yy)), (sx(DTP0) + 22, fy(yy))], fill=c, width=2)
        txt(sx(DTP0) + 28, fy(yy), sayi(yy), f7, c, "lm")
    isaret(sx(DTP0) + 330, fy((H_B + YG0) / 2), 2)''')
d('''    txt(sx(0), fy(0) + 26, "ön (z 0)", f7, GRAY, "rm")''', '''    txt(sx(0), fy(0) + 26, "ön (z 0) · gövde +%s" % sayi(ZS), f7, GRAY, "rm")''')
# ---- liste ----
d('("1", "Fırın gövdesi · TP10 kesiti · paslanmaz · yalıtımlı · boy ÖZEL", "1500 × 730 × 517", "föy kesiti + özel"),',
  '("1", "Fırın gövdesi · TP10 kesiti · paslanmaz · yalıtımlı · boy ÖZEL · 79 mm ÖNE", "1500 × 730 × 517 · z +79…−651", "föy kesiti + özel · Kemal 27 Eyl"),')
d('("5", "Giriş ön odası · ısıtılmaz · TOPPING cebi", "64", "hesap"),', '("5", "Giriş ön odası · ısıtılmaz", "64", "hesap"),')
d('("9", "K giriş çiti 20° (bizim · K bandında) + 2 braket", "−249 → −170 · 231", "hesap"),',
  '("9", "Çıkıntı: gövde ön yüzün önünde (x 2500–4000 · y 956–1473)", "79", "Kemal 27 Eyl"),')
d('''    for s_ in ("C · aktarma bandı (420) çıkar → giriş bandı F'nin ön odasında",
               "C · X motoru kaidesi sağ üst köşe pahlanır (1112)",
               "C · çıkış yarığı çerçevesi −417…−13 · alt çıta 1145–1155",
               "C · ürün diskte 79 mm arkaya kaydırılır (itici · AÇIK)",
               "K · parça değişmez · K bandında giriş çiti + ölü plaka",
               "F · taban dolabı 1060 → 956 · davlumbaz 1483"):''',
  '''    for s_ in ("C · giriş bandı F'nin ön odasında (bizim) · ekseni −170",
               "C · çıkış yarığı çerçevesi −417…−13 · alt çıta 1145–1155",
               "C · aktarma iticisi DÜZ 170 (itici_cad_v3) · destek plakası yok",
               "C · TOPPING v9: ön fitil tam (boşluk kalktı)",
               "K · parça değişmez (kesme_cad_v2) · giriş çiti YOK · ölü plaka",
               "F · 79 öne: çıkıntı 1500 × 517 × 79 · modül 909 derin · dolap 956"):''')
d('''    for i, s_ in enumerate(("TOPPING teknesi + X tahriki F'ye 85 mm taşıyor → cep (ya da TOPPING kısaltılır)",
                            "istasyon tabanı 1060 kuralı F'de 956",
                            "pizza kutusu 4 gün → 3,8 gün (48 kutu)",
                            "tabladan itme + 79 mm arkaya kayma (itici tasarımı)",
                            "boy uzatma özel sipariş (Sveba / yerli IR) · güç ≈14 kW VARSAYIM"), 1):''',
  '''    for i, s_ in enumerate(("çıkıntı 79: üretici ince duvar (60) + pay 10 verirse 50'ye iner [V]",
                            "istasyon tabanı 1060 kuralı F'de 956 · 830 derinlik kuralı F'de 909",
                            "pizza kutusu 4 gün: dolap 505 + raf 55 + şarjör 567",
                            "robot kol zarfı kutu (gerçek kol modeli yok) · çıkıntıya pay 181",
                            "boy uzatma özel sipariş (Sveba / yerli IR) · güç ≈14 kW VARSAYIM"), 1):''')
d('    txt(x0, y, "kesit ölçüleri föy + çizimden (≈) · boy, oda, ön oda, duvarlar hesap · tam yükte 51,7 ürün/sa = bugünkü model (sim, 2. saat)", f7, GRAY, "lm")',
  '    txt(x0, y, "kesit ölçüleri föy + çizimden (≈) · boy, oda, ön oda, duvarlar hesap · z kotları DÜNYA (gövde +79 kaymış) · tam yükte 51,7 ürün/sa (sim, 2. saat)", f7, GRAY, "lm")')
# ---- başlık + çıktı ----
d('txt(FX0, 40, "AUTOKITCH  ·  F FIRIN (AYRI SÜRÜM)  ·  TP10 KESİTİ · GÖVDE 1500\'E UZATILMIŞ  ·  TEKNİK RESİM v3", f30, INK)',
  'txt(FX0, 40, "AUTOKITCH  ·  F FIRIN  ·  TP10 KESİTİ · GÖVDE 1500  ·  79 mm ÖNE (ÇIKINTI)  ·  TEKNİK RESİM v4", f30, INK)')
d('''    txt(FX0, 98, "3B model firin_tp10_cad_v2 (tek kaynak) · gövde %s–%s · bant gövde dışına çıkmaz · ısıtılan %s · aynı anda %d ürün · ana makine v47 değişmez · ölçüler mm · 26 Eylül 2026"
        % (sayi(X_F0), sayi(X_F1), sayi(FT.ODA), N_ICERIDE), f11, GRAY)''',
  '''    txt(FX0, 98, "3B model firin_tp10_cad_v5 (tek kaynak) · gövde %s–%s · gövde + konveyör + giriş bandı 79 öne (Kemal 27 Eyl: hizalanma) · ürün −170 düz · ısıtılan %s · aynı anda %d ürün · ana makine v51 · ölçüler mm · 27 Eylül 2026"
        % (sayi(X_F0), sayi(X_F1), sayi(FT.ODA), N_ICERIDE), f11, GRAY)''')
d('    yol = os.path.join(KLASOR, "FIRIN_TP10_v3_teknik.png")', '    yol = os.path.join(KLASOR, "FIRIN_TP10_v4_teknik.png")')
d('''    im.save(yol.replace(".png", ".pdf"), "PDF", resolution=150.0 * K_HD)
    print("yazildi:", yol, im.size)''',
  '''    im.save(yol.replace(".png", ".pdf"), "PDF", resolution=150.0 * K_HD)
    im.resize((int(W_PX * 0.6), int(H_PX * 0.6)), Image.LANCZOS).save(os.path.join(KLASOR, "..", "..", "otonom", "hat", "img", "FIRIN_TP10_v4_teknik.png"), optimize=True)
    print("yazildi:", yol, im.size)''')
io.open(os.path.join(U, "teknik_firin_tp10_v4.py"), "w", encoding="utf-8").write(s)
print("teknik_firin_tp10_v4.py yazildi")
