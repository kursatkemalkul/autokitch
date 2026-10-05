# -*- coding: utf-8 -*-
"""topping_uno_cad_v17 → v18 (29 Eyl 2026 gece · YEREL).
Kemal: "soğutma grubunu alta (arka köşe), sağ köşedekileri kaldır, o bölüm temiz boş · basamaklı yalıtımı kaldır, dikdörtgen temiz dönsün · eşitlik isterim".
  · SOĞUK KUTU DİKDÖRTGEN: B tavanı = A tavanı (1970) · teknik cep, L dikey duvar, teknik ayırma sacları, teknik zarflar KALKTI · dış kabuk / çerçeve dikdörtgen
  · KAPAKLAR EŞİT: K1 701,5–1597,75 · K2 1600,75–2497 (mekanizma kanatlarıyla aynı derz) · ikisi de 1110,5–1859 · flipper + kılavuz + pim +79,25
  · EVAPORATÖR SAĞ ÜSTE ve BÜYÜDÜ (400 geniş): dikdörtgen kutu + KLF6.6CND → gereken 340–410 W (32–40 °C) · kıyma + kuşbaşı haznelerinin üstü
  · SOĞUTMA HATLARI: arka duvar bloğundan kuru bölmeye, DİKİNE aşağı kaidedeki yoğuşma ünitesinin üst yüzüne (topping_cad_v30)
Yalnız okur: topping_uno_cad_v17.py · yazar: topping_uno_cad_v18.py"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_uno_cad_v17.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a), n)
    s = s.replace(a, b)


def blok(bas, son, yeni):
    """bas'tan (dahil) son'a (hariç) kadar olan bölümü yeni ile değiştirir"""
    global s
    assert s.count(bas) == 1, ("bas", bas[:90], s.count(bas))
    i = s.index(bas)
    assert s.count(son, i) >= 1, ("son", son[:90])
    j = s.index(son, i)
    s = s[:i] + yeni + s[j:]


# ---------------------------------------------------------------- 0 · başlık
degis('"""TOPPING v2 (UNO\'lu) · 3B MODEL · topping_uno_cad_v17 · 29 Eyl 2026 · YEREL (',
      '"""TOPPING v2 (UNO\'lu) · 3B MODEL · topping_uno_cad_v18 · 29 Eyl 2026 gece · YEREL (v17 + SOĞUK KUTU DİKDÖRTGEN · EŞİT KAPAKLAR · EVAPORATÖR SAĞ ÜSTTE 400 · HATLAR KAİDEDEKİ ÜNİTEYE · yap_topping_uno_cad_v18.py)\n'
      'v18: Kemal "soğutma grubunu alta, sağ üstü temiz boş · basamaklı yalıtımı kaldır, dikdörtgen · eşitlik isterim": B tavanı = A tavanı (teknik cep yok) · K1 = K2 = 896,25\n'
      '    (mekanizma kanatlarıyla aynı derz 1597,75 / 1600,75) · flipper + kılavuz +79,25 · evaporatör kıyma + kuşbaşı haznelerinin üstünde 400 geniş (gereken 340–410 W) ·\n'
      '    hatlar kuru bölmeden dikine kaidedeki yoğuşma ünitesine (topping_cad_v30: Secop CU KLF6.6CND)\n'
      'v17: topping_uno_cad_v17 · 29 Eyl 2026 · YEREL (')

# ---------------------------------------------------------------- 1 · ölçüler: basamak + teknik cep kalktı
degis("TAVAN_B = 1686.0", "TAVAN_B = TAVAN_A  # v18: DİKDÖRTGEN kutu (Kemal: \"basamaklı yalıtımı kaldır\") · v16/v17: 1686 + teknik cep")
degis("Y_TEK = TAVAN_B + T_DUV; X_TEK = BAY_A[1] + T_DUV", "# v18: Y_TEK / X_TEK (teknik cep tabanı / L dikey) KALKTI")
degis("TEK_Y0 = Y_TEK + 6.0", "# v18: TEK_Y0 kalktı")
degis('ekle("kabin_sag_teknik_sac", kut(W - 1.5, W, Y_TEK, YUST, 0, -D), "kabuk", "V", not_="v11: teknik cebin sağ yan saçı · havalandırma ızgaralı (kondenser havası)")',
      "# v18: kabin_sag_teknik_sac KALKTI (teknik cep yok — sağ yan = TC sacı + soğuk kutunun sağ duvarı)")
degis("CEP_TEKNIK = (X_TEK, W, Y_TEK, YUST, Z_KAPAK[1], -D)", "# v18: CEP_TEKNIK kalktı")

# ---------------------------------------------------------------- 2 · soğuk kutu DİKDÖRTGEN
blok("ODA = ((BAY_A[0], BAY_A[1], Y_ALT1 - 1.0, TAVAN_A), (BAY_A[0], BAY_B[1], Y_ALT1 - 1.0, TAVAN_B))",
     'KUTU["alt_yalitim_saci"] = kut(',
     "# v18 · DİKDÖRTGEN (Kemal 29 Eyl gece: \"üst sağdakiler taşınınca basamaklı yalıtımı kaldır, dikdörtgen temiz dönsün\"): tek kutu, basamak / L dikey / teknik taban yok\n"
     "ODA = (BAY_A[0], BAY_B[1], Y_ALT1 - 1.0, TAVAN_A)                                     # soğuk oda (kaplama tabana kadar iner) · 60–1740 × 1277,5–1970\n"
     "ODA_K = (BAY_A[0] - T_IC, BAY_B[1] + T_IC, Y_ALT1, TAVAN_A + T_IC)                     # kaplamanın dış yüzü\n"
     "ZARF_K = (X_SAC[0], X_SAC[1], Y_ALT1, Y_UST_SAC)                                      # dış kabukların iç yüzü (yan = TC yan sacı · üst = TC tavan sacı)\n"
     "_odak = kut(*ODA_K, Z_SOGUK[1] - T_IC, Z_ZARF)\n"
     "KUTU = {\"soguk_ic_kaplama\": _odak.cut(kut(*ODA, Z_SOGUK[1], Z_ZARF + 1.0))}\n"
     "_pu = kut(*ZARF_K, Z_BOLME[1] + T_DIS, Z_ZARF).cut(_odak)\n"
     "_psol = _pu.intersect(kut(X_SAC[0], BAY_A[0] - T_IC, Y_ALT1, TAVAN_A + T_IC, Z_SOGUK[1] - T_IC, Z_ZARF))\n"
     "_psag = _pu.intersect(kut(BAY_B[1] + T_IC, X_SAC[1], Y_ALT1, TAVAN_A + T_IC, Z_SOGUK[1] - T_IC, Z_ZARF))   # v18: sağ duvar sol duvarla aynı boy (v16/v17 teknik tabana kadar)\n"
     "KUTU[\"kabin_sol_duvar_PU\"] = _psol\n"
     "KUTU[\"kabin_sag_duvar_PU\"] = _psag\n"
     "KUTU[\"yalitim_blogu\"] = _pu.cut(_psol).cut(_psag)                                     # arka + tavan (tek köpük)\n"
     "KUTU[\"soguk_arka_dis_sac\"] = kut(X_SAC[0], X_SAC[1], YAL_Y0, Y_UST_SAC, Z_BOLME[1], Z_BOLME[1] + T_DIS)   # v18: dikdörtgen 1,5 (kuru bölmeye bakar)\n"
     "# v18: teknik_ayirma_saci_yatay / _dikey KALKTI (teknik cep yok)\n")
blok('for ad, x0, x1, h_, z1_ in (("sogutma_grubu", 860, 1167, 272.0, -420.0)',
     "# tabla + pide (ilk durak: sos)",
     "# v18: teknik cep zarfları (teknik_bant_*) KALKTI — yoğuşma ünitesi kaidede (arka-alt), pano + UPS kuru bölmenin üstünde (topping_cad_v30)\n")

# ---------------------------------------------------------------- 3 · evaporatör SAĞ ÜSTE + büyüdü · hatlar kaidedeki üniteye
blok("# ================================================================ 3c · v16 · SOĞUTMA: EVAPORATÖR KUTUNUN İÇİNDE",
     "for _k, _mal, _not in (",
     '''# ================================================================ 3c · v16/v18 · SOĞUTMA: EVAPORATÖR KUTUNUN İÇİNDE
#   v18: dikdörtgen kutunun SAĞ ÜST boşluğuna (kıyma + kuşbaşı haznelerinin üstü: dolumda 15 kalkınca 1682 < 1762) taşındı ve 400 genişliğe büyüdü —
#   dikdörtgen kutu + Secop CU KLF6.6CND (topping_cad_v30, KAİDEDE arka-alt) → gereken 340 / 368 / 393 / 410 W @ 32 / 35 / 38 / 40 °C (dolum + ılık gün ·
#   dikdortgen_sogutma_v1 = sogutma_topping_v1 yöntemi) · v16/v17: A tavanında SOS üstünde 260 geniş (300–380 W) · yoğuşma suyu arka duvardan kuru
#   bölmedeki elektrikli buharlaştırma kabına · EVAPORATÖR YAPTIRILACAK (soğutmacı firma): model YER ZARFI 400 × 208 × 500
EVAP = (830.0, 1230.0, 1762.0, TAVAN_A, -560.0, -60.0)                                # v18 · x 830–1230 (dünya 1530–1930) · y 1762–1970 · z −560…−60
_ex0, _ex1, _ey0, _ey1, _ez0, _ez1 = EVAP
_g = kut(_ex0, _ex1, _ey1 - 1.0, _ey1, _ez0, _ez1)                                    # üst sac (tavan kaplamasına)
_g = _g.union(kut(_ex0, _ex0 + 1.0, _ey0, _ey1, _ez0, _ez1)).union(kut(_ex1 - 1.0, _ex1, _ey0, _ey1, _ez0, _ez1))   # yan saclar
_g = _g.union(kut(_ex0, _ex1, _ey0, _ey1, _ez0, _ez0 + 1.0))                          # arka sac
ekle("evaporator_govdesi", _g, "paslanmaz", "V",
     not_="v18 · evaporatör gövdesi AISI 304 1,0 (üst + yanlar + arka) · 400 × 208 × 500 · tavan kaplamasına 6 × M6 perçin somun (köpük içi takviye lama) · kutunun SAĞ ÜSTÜNDE (kıyma + kuşbaşı haznelerinin üstü) · önü ve altı yarıklı KAPAKLA kapalı · YER ZARFI (soğutmacı firma)")
# v17 · EVAPORATÖR KAPAĞI (Kemal: "teknik kısmı görmeyelim — sanayi dolaplarında önüne delikli sac panel konur, hava oradan gelir"): ön ızgara + alt sac tek parça
#       (L büküm) · lazer yarık 60 × 6, hatve 9 · üfleme öndeki yarıklardan tavan boyunca kapıya, dönüş alt sacın arka yarısındaki yarıklardan · 6 × M4 ile sökülür
EV_Q = 410.0 / (1.2 * 1005.0 * 4.0)                                                   # m³/s · v18: 410 W (dikdörtgen, 40 °C, dolum + ılık), hava ΔT 4 K → ≈0,085
EV_KOL = [(_ex0 + _ex1) / 2.0 + d_ for d_ in (-160.0, -80.0, 0.0, 80.0, 160.0)]       # v18: 5 yarık kolonu (60 genişlik · v17 3)
EV_ON_Y = [1771.0 + 9.0 * i_ for i_ in range(21)]                                     # ön ızgara sıraları (y · 6 yükseklik)
EV_DON_Z = [-553.0 + 9.0 * i_ for i_ in range(15)]                                    # dönüş ızgarası sıraları (z · 6 derinlik) → −553…−421
TAH_X = _ex0 + 24.0                                                                   # v18 · tahliye: tavanın sol-arka köşesi (x 854 · dünya 1554)
_kp = kut(_ex0 + 1.0, _ex1 - 1.0, _ey0 + 1.0, _ey1 - 1.0, _ez1 - 1.0, _ez1).union(kut(_ex0 + 1.0, _ex1 - 1.0, _ey0, _ey0 + 1.0, _ez0 + 1.0, _ez1))
for _xk in EV_KOL:
    for _yr in EV_ON_Y:
        _kp = _kp.cut(kut(_xk - 30.0, _xk + 30.0, _yr, _yr + 6.0, _ez1 - 2.0, _ez1 + 1.0))
    for _zr in EV_DON_Z:
        _kp = _kp.cut(kut(_xk - 30.0, _xk + 30.0, _ey0 - 1.0, _ey0 + 2.0, _zr, _zr + 6.0))
_kp = _kp.cut(sily(TAH_X, -392.0, 4.5, _ey0 - 1.0, _ey0 + 2.0))                      # tahliye hortumu geçişi (hortum Ø8, delik Ø9)
EV_ACIK = (len(EV_KOL) * len(EV_ON_Y) * 360.0, len(EV_KOL) * len(EV_DON_Z) * 360.0)   # mm² · üfleme / dönüş açık alanı
ekle("evaporator_kapagi", _kp, "paslanmaz", "V",
     not_="v17/v18 · EVAPORATÖR KAPAĞI AISI 304 1,0 L büküm (ön + alt) · lazer yarık 60 × 6 hatve 9 · ön ızgara %d yarık = %.0f mm² (üfleme %.1f m/s @ %.3f m³/s) · alt dönüş ızgarası %d yarık = %.0f mm² (%.1f m/s) · "
          "içeriden yalnız düz yarıklı sac görünür (sanayi dolabı düzeni) · 6 × M4 ile sökülür"
          % (len(EV_KOL) * len(EV_ON_Y), EV_ACIK[0], EV_Q / (EV_ACIK[0] * 1e-6), EV_Q, len(EV_KOL) * len(EV_DON_Z), EV_ACIK[1], EV_Q / (EV_ACIK[1] * 1e-6)))
ekle("evaporator_lamel_paketi", kut(_ex0 + 1.0, _ex1 - 1.0, 1790.0, 1965.0, -400.0, -260.0), "aluminyum", "V",
     not_="v18 · lamel paketi (Al kanat / Cu boru) 398 × 175 × 140 · hava arkadan öne (dönüş bölmesi z −559…−400 → paket → fanlar) · 450–580 W @ −10 °C (VARSAYIM: v17 258 genişlikte 300–380 W, yüzey oranıyla) · gereken 340–410 W @ 32–40 °C (dikdörtgen, dolum + ılık) · uç plakaları gövde yan saclarına · YER ZARFI")
ekle("evaporator_fani", kut(_ex0 + 40.0, _ex0 + 190.0, 1802.0, 1952.0, -260.0, -210.0).union(kut(_ex1 - 190.0, _ex1 - 40.0, 1802.0, 1952.0, -260.0, -210.0)), "motor", "V",
     not_="v18 · 2 × eksenel fan 150 × 150 × 50 (EC 24 V) · lamel paketinin ön çerçevesine 4'er × M4 · paketten çekip ön ızgaradan tavan boyunca kapıya üfler · model / debi soğutmacı firma")
ekle("evaporator_damlama_tavasi", kut(_ex0 + 1.0, _ex1 - 1.0, 1766.0, 1790.0, -408.0, -252.0).cut(kut(_ex0 + 2.0, _ex1 - 2.0, 1767.0, 1791.0, -407.0, -253.0)), "paslanmaz", "V",
     not_="v18 · damlama tavası 304 1,0 · lamel paketinin altında · %1 eğimle sol-arka köşedeki Ø8 çıkışa")
TAHLIYE = [(TAH_X, 1766.0, -392.0), (TAH_X, 1754.0, -392.0), (TAH_X, 1754.0, -660.0), (TAH_X, 1745.0, -660.0)]   # v18: x 854 (v17 90)
ekle("evaporator_tahliye_hortumu", boru(TAHLIYE, 4.0), "silikon", "V",
     not_="v18 · yoğuşma tahliyesi Ø8 silikon · tavanın sol-arka köşesinden kapağın deliğinden aşağı, kıyma haznesinin üstünden (1750 > 1682) arka duvara, duvar deliği hortum çapında (silikonla) · kuru bölmedeki buharlaştırma kabına düşer · sifonlu")
kutu_delik(silz(TAH_X, 1754.0, 4.0, Z_BOLME[1] - 1.0, Z_BOLME[0] + 1.0), ARKA3)
ekle("yogusma_buharlastirma_kabi", kut(TAH_X - 54.0, TAH_X + 46.0, 1700.0, 1745.0, -790.0, Z_BOLME[1]).cut(kut(TAH_X - 52.0, TAH_X + 44.0, 1702.0, 1746.0, -788.0, Z_BOLME[1] - 2.0)), "paslanmaz", "V",
     not_="v16/v18 · elektrikli yoğuşma buharlaştırma kabı 100 × 45 × 160 (0,6 L · 30 W rezistans + şamandıra, VARSAYIM) · arka duvarın dış sacına 2 × M5 · v18: tahliyenin altında (dünya x 1500–1600) · altında elektrik yok (valf adası + sürücüler solda, pano solda 1450'ye kadar)")
# v18 · SOĞUTMA HATLARI KAİDEDEKİ ÜNİTEYE (Kemal: "soğutma grubunu alta, sağ üstü temiz boş"): evaporatörün arka yüzünden (z −560) arka duvardaki POM bloktan kuru bölmeye (z −660),
#       kuru bölmenin üstünde sağa (emiş dünya x 1990 · sıvı 1950), oradan DİKİNE aşağı → kuru bölme tabanından (topping_cad_v30) yoğuşma ünitesinin ÜST yüzüne (dünya y 1087)
HAT_X, HAT_Z_KURU = 1205.0, -660.0                                                     # v18 · evaporatörün sağ-arka köşesi (v17: 290)
HAT = {"sogutma_emis_hatti": (1935.0, 15.5), "sogutma_sivi_hatti": (1900.0, 3.2)}
HAT_X_INIS = {"sogutma_emis_hatti": xu(1990.0), "sogutma_sivi_hatti": xu(1950.0)}      # v18 · dikine iniş (kuşbaşı hortumlarının sağı, kaşar motorunun solu)
HAT_Y_UNITE = yu(1087.0)                                                               # v18 · ünite üst yüzü (topping_cad_v30 · dünya y 815–1087)
HAT_GECIS = (HAT_X - 25.0, HAT_X + 25.0, 1885.0, 1955.0, Z_BOLME[1], Z_BOLME[0])      # arka duvar hat geçişi (kaplama + PU + arka dış sac)
_hg = kut(*HAT_GECIS)
for _hy, _hr in HAT.values():
    _hg = _hg.cut(silz(HAT_X, _hy, _hr, Z_BOLME[1] - 1.0, Z_BOLME[0] + 1.0))
kutu_delik(kut(HAT_GECIS[0], HAT_GECIS[1], HAT_GECIS[2], HAT_GECIS[3], Z_BOLME[1] - 1.0, Z_BOLME[0] + 1.0), ARKA3)
ekle("sogutma_hat_gecis_blogu", _hg, "pom", "V", not_="v17/v18 · POM-C hat geçiş bloğu 50 × 70 × 60 · ARKA duvarı boydan geçer (evaporatörün sağ-arka köşesinin arkasında, görünmez) · iki hat deliği hat çapında (silikonla sızdırmaz)")
for _ha, (_hy, _hr) in HAT.items():
    ekle(_ha, boru([(HAT_X, _hy, _ez0), (HAT_X, _hy, HAT_Z_KURU), (HAT_X_INIS[_ha], _hy, HAT_Z_KURU), (HAT_X_INIS[_ha], HAT_Y_UNITE, HAT_Z_KURU)], _hr), "koyu" if "emis" in _ha else "celik", "V",
         not_=("v17 · emiş hattı Cu Ø12,7 + Armaflex 9 mm (dış Ø31)" if "emis" in _ha else "v17 · sıvı hattı Cu Ø6,35 · genleşme valfi / kılcal evaporatör girişinde (soğutmacı firma)") +
              " · v18: evaporatörün arkasından arka duvar bloğundan kuru bölmeye (z −660), sağa, kuru bölmede DİKİNE aşağı → kuru bölme tabanından kaidedeki yoğuşma ünitesinin üst yüzüne (dünya y 1087) · emiş aşağı iner (yağ dönüşü kendiliğinden) · soğuk odada görünmez")
''')
blok("for _k, _mal, _not in (",
     "# v14 · ESKİ ÖN FİTİL (z −104) KALKTI",
     '''for _k, _mal, _not in (
        ("soguk_ic_kaplama", "paslanmaz", "v18 · İÇ KAPLAMA AISI 304 1,0 TEK PARÇA: yanlar + arka + tavan, DİKDÖRTGEN (köşeler kaynaklı-taşlanmış, iç köşe R ≥ 6) · önü açık (430 çerçeve + kapaklar) · tabanı raf · kovan / blok / tahliye delikleri"),
        ("kabin_sol_duvar_PU", "pu", "v16 · sol duvar PU 57,5 (40 kg/m³, yerinde köpük) · dış kabuğu TC sol yan sacı (x 0–1,5) · iç kaplamaya ve sacın iç yüzüne yapışık · 4 GFRP raf burcu"),
        ("kabin_sag_duvar_PU", "pu", "v18 · sağ duvar PU 57,5 · dış kabuğu TC sağ yan sacı (x 1798,5–1800) · sol duvarla aynı boy (tavana kadar) · 4 GFRP raf burcu"),
        ("yalitim_blogu", "pu", "v18 · PU 57,5 TEK KÖPÜK: arka duvar + tavan (DİKDÖRTGEN, hepsi 60 sandviç; v16/v17: + L dikey + B tavanı) · 4 kaset + 4 UNO kovanı + geçiş bloğu + hat bloğu + tahliye delikleri"),
        ("soguk_arka_dis_sac", "paslanmaz", "v18 · arka duvarın dış kabuğu AISI 304 1,5 (kuru bölmeye bakar) · x 1,5–1798,5 · alt sacdan TC tavanına kadar DİKDÖRTGEN · kovan / blok / tahliye delikleri")):
    ekle(_k, KUTU[_k], _mal, "Ö", not_=_not)
''')

# ---------------------------------------------------------------- 4 · ön yüz: çerçeve + kapaklar + flipper
degis("CER_DIS = [(1.5, YAL_Y0), (W - 1.5, YAL_Y0), (W - 1.5, Y_TEK), (X_TEK, Y_TEK), (X_TEK, YUST - 1.5), (1.5, YUST - 1.5)]",
      "CER_DIS = [(1.5, YAL_Y0), (W - 1.5, YAL_Y0), (W - 1.5, YUST - 1.5), (1.5, YUST - 1.5)]          # v18: dikdörtgen")
degis("AGIZ_L = [(BAY_A[0], SOGUK_TABAN), (BAY_B[1], SOGUK_TABAN), (BAY_B[1], TAVAN_B), (BAY_A[1], TAVAN_B), (BAY_A[1], TAVAN_A), (BAY_A[0], TAVAN_A)]",
      "AGIZ_L = [(BAY_A[0], SOGUK_TABAN), (BAY_B[1], SOGUK_TABAN), (BAY_B[1], TAVAN_A), (BAY_A[0], TAVAN_A)]                 # v18: dikdörtgen ağız")
degis('''SKAPAK = {"K1": dict(x=(xu(701.5), xu(1518.5)), y=(yu(1110.5), yu(1859.0)), fitil=(BAY_A[0], xu(1500.0), yu(1136.0), TAVAN_A), mentese="sol"),
          "K2": dict(x=(xu(1521.5), xu(2497.0)), y=(yu(1110.5), yu(1575.0)), fitil=(xu(1537.5), BAY_B[1], yu(1136.0), TAVAN_B), mentese="sag")}''',
      '''SKAPAK = {"K1": dict(x=(xu(701.5), xu(1597.75)), y=(yu(1110.5), yu(1859.0)), fitil=(BAY_A[0], xu(1579.25), yu(1136.0), TAVAN_A), mentese="sol"),     # v18: EŞİT (Kemal "eşitlik isterim")
          "K2": dict(x=(xu(1600.75), xu(2497.0)), y=(yu(1110.5), yu(1859.0)), fitil=(xu(1616.75), BAY_B[1], yu(1136.0), TAVAN_A), mentese="sag")}    # v18: 896,25 × 748,5 · derz = mekanizma kanatlarınınki''')
degis('("K2_mentese_1", xu(2456.0), xu(2468.5), 1620.0, (xu(2468.5), xu(2498.5)))', '("K2_mentese_1", xu(2456.0), xu(2468.5), 1900.0, (xu(2468.5), xu(2498.5)))')
degis('("≈14,4 kg" if _ad.startswith("K1") else "≈10,4 kg")', '"≈15,8 kg (v18: iki kapak eşit 896,25 × 748,5)"')
degis('(("basac_K1", 780.0, 810.0, 1990.0, 2020.0), ("basac_K2", 830.0, 870.0, 1730.0, 1742.0))',
      '(("basac_K1", 859.25, 889.25, 1990.0, 2020.0), ("basac_K2", 909.25, 939.25, 1990.0, 2020.0))')      # v18: derze simetrik
degis("#     katlanma ekseni FLIP_EKSEN (dünya x 1493 · z +20", "#     katlanma ekseni FLIP_EKSEN (v18: dünya x 1572,25 · v17 1493 · z +20")
degis("FLIP_EKSEN = (xu(1493.0), 20.0); FLIP_K = 30.0",
      "FLIP_EKSEN = (xu(1572.25), 20.0); FLIP_K = 33.0                                       # v18: +79,25 (eşit kapaklar) · kam oranı 30 → 33: K1 896 genişlikte ön kenarı daha hızlı öne gelir;\n"
      "#     fitil iç kenarında (eksenden 30) geri çekilme 30·K·α > öne gelme 900·α olmalı (K 30'da 0,1 mm fitile giriyordu · 33'te 89·α pay, v17'deki 78·α kadar)")
degis("KILAVUZ = (xu(1440.0), xu(1547.0), SOGUK_TABAN, SOGUK_TABAN + 15.0, -40.0, Z_CER[1])", "KILAVUZ = (xu(1519.25), xu(1626.25), SOGUK_TABAN, SOGUK_TABAN + 15.0, -40.0, Z_CER[1])")
degis("FLIP = (xu(1493.0), xu(1547.0), KILAVUZ[3] + 0.5, TAVAN_B - 0.5)", "FLIP = (xu(1572.25), xu(1626.25), KILAVUZ[3] + 0.5, TAVAN_A - 0.5)                  # v18: tavana kadar (634)")
degis("FLIP_PIM = (xu(1541.0), -10.0, 4.0, KILAVUZ[3] - 9.5)", "FLIP_PIM = (xu(1620.25), -10.0, 4.0, KILAVUZ[3] - 9.5)")
degis("katlanma ekseni dünya x 1493 · z +20 · K1", "katlanma ekseni dünya x 1572,25 (v18) · z +20 · K1")
degis("for _i, _y0 in enumerate((1360.0, 1640.0)):", "for _i, _y0 in enumerate((1360.0, 1900.0)):                                              # v18: flipper tavana kadar")
degis('kut(xu(1481.0), FLIP_EKSEN[0], _y0, _y0 + 20.0,', 'kut(xu(1560.25), FLIP_EKSEN[0], _y0, _y0 + 20.0,')
degis("braket K1 fitilinin solunda (dünya x ≤ 1493)", "braket K1 fitilinin solunda (dünya x ≤ 1572,25)")

# ---------------------------------------------------------------- 5 · denetimler
degis('_k60 = {"sol duvar": BAY_A[0], "sağ duvar": W - BAY_B[1], "arka": Z_BOLME[0] - Z_BOLME[1], "A tavanı": YUST - TAVAN_A, "L dikey": X_TEK - BAY_A[1], "B tavanı": Y_TEK - TAVAN_B}',
      '_k60 = {"sol duvar": BAY_A[0], "sağ duvar": W - BAY_B[1], "arka": Z_BOLME[0] - Z_BOLME[1], "tavan": YUST - TAVAN_A}   # v18: dikdörtgen (L dikey + B tavanı yok)')
degis('kontrol("v16 · PU tek köpük (arka + A tavanı + L + B tavanı: x', 'kontrol("v18 · PU tek köpük (arka + tavan, DİKDÖRTGEN: x')
degis('_ZA = ("yalitim_blogu", "tasiyici_raf_3mm", "raf_on_bukumu", "teknik_ayirma_saci_yatay", "teknik_ayirma_saci_dikey", "kabin_sol_duvar_PU",',
      '_ZA = ("yalitim_blogu", "tasiyici_raf_3mm", "raf_on_bukumu", "kabin_sol_duvar_PU",')
degis("(%d parça: kaplama, 3 PU, teknik saclar, alt sac, raf)", "(%d parça: kaplama, 3 PU, alt sac, raf · v18 teknik saclar yok)")
degis("SOGUK_TABAN, TAVAN_B, _fb.xmin + DX_DUNYA, _fb.xmax + DX_DUNYA),", "SOGUK_TABAN, TAVAN_A, _fb.xmin + DX_DUNYA, _fb.xmax + DX_DUNYA),")
degis("_fb.ymax < TAVAN_B and _fb.xmin + DX_DUNYA < 1518.5 and _fb.xmax + DX_DUNYA > 1521.5)", "_fb.ymax < TAVAN_A and _fb.xmin + DX_DUNYA < 1597.75 and _fb.xmax + DX_DUNYA > 1600.75)")
degis('("yalitim_blogu", "teknik_ayirma_saci_yatay"), ("yalitim_blogu", "teknik_ayirma_saci_dikey"),\n', "")
blok('_ev = bb("evaporator_govdesi"); _sh_ = bb("sos_hazne_bizim");',
     "_oda_h = sum(",
     '''_ev = bb("evaporator_govdesi"); _eh = bb("sogutma_emis_hatti"); _sv = bb("sogutma_sivi_hatti")
_hz_ev = [(a_.lower(), bb("%s_hazne_bizim" % a_.lower())) for a_, cx_, hw_, *_r in UNO if cx_ + hw_ / 2.0 > _ev.xmin and cx_ - hw_ / 2.0 < _ev.xmax]
_kst = max(p["sh"].BoundingBox().ymax for p in P if p["ad"].startswith(("kasar_cad", "sucuk_cad")))
kontrol("v18 · evaporatör soğuk odanın İÇİNDE, SAĞ ÜSTTE (x %.0f–%.0f ⊂ %.0f–%.0f · y %.0f–%.0f ≤ tavan %.0f · z %.0f…%.0f) · altındaki hazneler (%s) dolumda 15 kalkınca en üst %.0f < evaporatör altı %.0f · kasetlerin üstü %.0f"
        % (_ev.xmin, _ev.xmax, BAY_A[0], BAY_B[1], _ev.ymin, _ev.ymax, TAVAN_A, _ev.zmin, _ev.zmax, ", ".join(a_ for a_, b_ in _hz_ev), max(b_.ymax for a_, b_ in _hz_ev) + 15.0, _ev.ymin, _kst),
        _ev.xmin >= BAY_A[0] and _ev.xmax <= BAY_B[1] and _ev.ymax <= TAVAN_A + 0.01 and _ev.zmin >= Z_SOGUK[1] and _ev.zmax <= Z_ZARF and bool(_hz_ev)
        and max(b_.ymax for a_, b_ in _hz_ev) + 15.0 < _ev.ymin and _kst < _ev.ymin)
''')
degis("_oda_h = sum(p[\"sh\"].intersect(_kutu2(*ODA, Z_SOGUK[1], Z_ZARF).val()).Volume() for p in P if p[\"ad\"] in HAT)          # L biçimli soğuk oda (teknik cep hariç)",
      "_oda_h = sum(p[\"sh\"].intersect(kut(*ODA, Z_SOGUK[1], Z_ZARF).val()).Volume() for p in P if p[\"ad\"] in HAT)          # v18: dikdörtgen soğuk oda")
blok('kontrol("v17 · soğutma hatları ODADA GÖRÜNMEZ:',
     "_kb_ = bb(\"evaporator_kapagi\")",
     '''kontrol("v17/v18 · soğutma hatları ODADA GÖRÜNMEZ: soğuk odadaki hat hacmi %.0f mm³ = evaporatörün arkasındaki 10 mm aralıkta %.0f mm³ (başka yerde 0) · arka duvar bloğundan kuru bölmeye (z %.0f) → DİKİNE aşağı kaidedeki ünitenin üst yüzüne (dünya y %.0f · emiş x %.0f · sıvı x %.0f)"
        % (_oda_h, _oda_g, HAT_Z_KURU, HAT_Y_UNITE + DY_DUNYA, HAT_X_INIS["sogutma_emis_hatti"] + DX_DUNYA, HAT_X_INIS["sogutma_sivi_hatti"] + DX_DUNYA),
        abs(_oda_h - _oda_g) < 1.0 and max(_eh.zmax, _sv.zmax) <= _ez0 + 15.5 + 0.01 and abs(_eh.ymin - HAT_Y_UNITE) < 0.01 and abs(_sv.ymin - HAT_Y_UNITE) < 0.01)
''')
degis('kontrol("v16 · yoğuşma suyu: tava → Ø8 hortum arka duvardan (y %.0f) → kuru bölmedeki elektrikli buharlaştırma kabı (üstü %.0f · x %.0f–%.0f) · altında elektrik yok (valf adası x ≥ %.0f · bobin üstü %.0f)"',
      'kontrol("v16/v18 · yoğuşma suyu: tava → Ø8 hortum arka duvardan (y %.0f) → kuru bölmedeki elektrikli buharlaştırma kabı (üstü %.0f · x %.0f–%.0f) · altında elektrik yok (valf adası x ≥ %.0f · bobin üstü %.0f)"')
degis("_ZT_ = _kutu2((X_SAC[0], X_SAC[1], SOGUK_TABAN, Y_TEK), (X_SAC[0], X_TEK, Y_TEK, Y_UST_SAC), Z_BOLME[1], Z_ZARF).val()",
      "_ZT_ = kut(X_SAC[0], X_SAC[1], SOGUK_TABAN, Y_UST_SAC, Z_BOLME[1], Z_ZARF).val()                                    # v18: dikdörtgen")
degis("_ODT = _kutu2((BAY_A[0], BAY_A[1], SOGUK_TABAN, TAVAN_A), (BAY_A[0], BAY_B[1], SOGUK_TABAN, TAVAN_B), Z_SOGUK[1], Z_ZARF + 1.0).val()",
      "_ODT = kut(BAY_A[0], BAY_B[1], SOGUK_TABAN, TAVAN_A, Z_SOGUK[1], Z_ZARF + 1.0).val()")
degis("çıkış dünya x %.1f + r 4 < 1493 (K1 fitil halkasının içi)", "çıkış dünya x %.1f + r 4 < 1572,25 (K1 fitil halkasının içi · v18)")
degis("PIM_YOLU[-1][0] + DX_DUNYA + FLIP_PIM[2] < 1493.0)", "PIM_YOLU[-1][0] + DX_DUNYA + FLIP_PIM[2] < 1572.25)")

# ---------------------------------------------------------------- 6 · sürüm adları
degis('"topping_uno_cad_v17 denetimi KALDI: %s"', '"topping_uno_cad_v18 denetimi KALDI: %s"')
degis('"generator": "AUTOKITCH topping_uno_cad_v17"', '"generator": "AUTOKITCH topping_uno_cad_v18"')
degis('"topping_uno_v17.glb"', '"topping_uno_v18.glb"')
degis('"topping_uno_v17.json"', '"topping_uno_v18.json"')
degis('surum="topping_uno_cad_v17 · %s"', 'surum="topping_uno_cad_v18 · %s"')

for _yasak in ("Y_TEK", "X_TEK", "TEK_Y0", "CEP_TEKNIK", "teknik_ayirma_saci_yatay\"", "teknik_ayirma_saci_dikey\""):
    _kal = [l_ for l_ in s.splitlines() if _yasak in l_ and not l_.lstrip().startswith("#") and "KALKTI" not in l_ and "kalktı" not in l_]
    assert not _kal or _yasak.startswith("teknik_ayirma"), (_yasak, _kal[:3])
compile(s, "topping_uno_cad_v18.py", "exec")
io.open(os.path.join(U, "topping_uno_cad_v18.py"), "w", encoding="utf-8").write(s)
print("topping_uno_cad_v18.py yazıldı · %d satır" % s.count("\n"))
