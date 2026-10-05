# -*- coding: utf-8 -*-
"""topping_uno_cad_v15 → topping_uno_cad_v16 (29 Eyl 2026 · YEREL) — Kemal: "yap herşeyi düzgün yap temiz olsun"
(TOPPING soruları: "yalıtımda kalınlıklar neden hep farklı ve düzgün değil · sağ sol duvardaki yalıtımla sac duvar arasında boşluk var ·
teknik raf havada mı, structure lazım değil mi · soğutma motoru yeterli mi, düzgün mü").
SOĞUK KUTU = KÖPÜK DOLGULU SANDVİÇ, HER YÜZ 60 (iç 304 1,0 + PU 57,5 + dış 304 1,5):
  · yan duvarların dış kabuğu = TC yan sacı (28,5 Z profil boşluğu + ayrı dış sac + Z profiller KALKTI) → soğuk oda 60 genişledi (x 60–1740)
  · A tavanı 60 (dış = TC tavan sacı) · L dikey 30 → 60 · B tavanı 30 → 60 (dış sacı = TEKNİK CEP TABANI) · arka 65 sacsız → 60 (iç + dış sac)
  · İÇ KAPLAMA tek parça 304 1,0 (v15'te yalnız yan duvarlarda vardı) · ALT DIŞ SAC tek parça (yan + arka duvarların altını da kapatır)
  · taban 43 kalır (raf 3 + PU 38,5 + sac 1,5): UNO ağzı + yayıcı giriş kelepçesi 1274'te bitiyor; daha kalın taban kelepçeyi yalıtıma gömer
  · sos / harç yayıcısının kesme valfi 20 aşağı (v15'te tabana 17 mm gömülüydü, alt PU'da cep vardı) → tabanın altında hiçbir parça gömülü değil
  · B tavanı 1690 → 1686 (kaset üstü 1672 + 14; hazne dolumda 15 kalkar), teknik cep tabanı 1746 (dünya 1578): Secop CU KLF4.8CND (272 yüksek) sığar
  · raf köşebentleri 4 × GFRP ısı köprüsü burcu + M8 ile TC yan saclarına · sağ duvar alt profili (itici kirişi, v70'ten beri itici yok) KALKTI
  · EVAPORATÖR KUTUNUN İÇİNDE: A bölmesinin tavanında, SOS haznesinin üstünde (v15'te TC kuru bölmesinde çıplaktı: +134 W, yoğuşma) · hatlar L duvarındaki
    POM bloktan teknik cepteki yoğuşma ünitesine · yoğuşma suyu arka duvardan kuru bölmedeki elektrikli buharlaştırma kabına · arka duvardaki evaporatör ağızları KALKTI
  · K1 / K2 menteşe kolları fitile yer açmak için 12,5 (TC yan sacının ön dönüşünün yanında) · K2 kapağı teknik tabana kadar (dünya 1110,5–1575)
Önceki: topping_uno_cad_v15.py"""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_uno_cad_v15.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


def blok(bas, son, yeni):
    """bas'ın başından son'un sonuna kadar olan metni yeni ile değiştirir (ikisi de tek)"""
    global s
    assert s.count(bas) == 1, ("bas", s.count(bas), bas[:90])
    i = s.index(bas)
    assert s.count(son, i) >= 1, ("son", son[:90])
    j = s.index(son, i) + len(son)
    s = s[:i] + yeni + s[j:]


# ---------------------------------------------------------------- 0 · başlık
degis('"""TOPPING v2 (UNO\'lu) · 3B MODEL · topping_uno_cad_v15 · 28 Eyl 2026 akşam (v14 + KAPAK İÇ SACI TEK PARÇA · sucuk_cad_v8 · Codex STEP kırıntıları atılır · yap_topping_uno_cad_v15.py)',
      '"""TOPPING v2 (UNO\'lu) · 3B MODEL · topping_uno_cad_v16 · 29 Eyl 2026 · YEREL (v15 + SOĞUK KUTU KÖPÜK DOLGULU SANDVİÇ, HER YÜZ 60 · EVAPORATÖR İÇERİDE · yap_topping_uno_cad_v16.py)' + NL +
      'v16: yan dış kabuk = TC yan sacı (boşluk / Z profil yok) · iç kaplama tek parça · L + B tavanı + arka 60 · taban 43 (UNO ağzı sınırı) · yayıcı kesme valfi tabanın altında ·' + NL +
      '    B tavanı 1686 · teknik taban 1746 · raf askısı GFRP burç · evaporatör A tavanında (SOS üstü) + hat bloğu + yoğuşma kabı · menteşe kolları 12,5' + NL +
      'v15: topping_uno_cad_v15 · 28 Eyl 2026 akşam (v14 + KAPAK İÇ SACI TEK PARÇA · sucuk_cad_v8 · Codex STEP kırıntıları atılır · yap_topping_uno_cad_v15.py)')

# ---------------------------------------------------------------- 1 · ölçüler
blok('BAY_A = (90.0, 790.0); TAVAN_A = 1968.0;', 'TEK_Y0 = Y_TEK + SAC_T + 10.0                                                      # v11: teknik bant zarflarının altı 1731,5',
     '# v16 · SOĞUK KUTU = KÖPÜK DOLGULU SANDVİÇ (Kemal 29 Eyl: "yap herşeyi düzgün yap temiz olsun"): her yüz 60 = iç 304 1,0 + PU 57,5 + dış 304 1,5 · yan / üst dış kabuk = TC\'nin kendi sacı' + NL +
     'T_IC, T_PU, T_DIS = 1.0, 57.5, 1.5; T_DUV = T_IC + T_PU + T_DIS                        # 60' + NL +
     'X_SAC = (1.5, W - 1.5)                                                                  # TC yan saclarının iç yüzü (dünya 701,5 / 2498,5)' + NL +
     'Y_UST_SAC = YUST - 1.5                                                                  # TC tavan sacının alt yüzü 2028,5' + NL +
     'BAY_A = (X_SAC[0] + T_PU + T_IC, 790.0); BAY_B = (790.0, X_SAC[1] - T_PU - T_IC)       # v16: 60 / 1740 (v15 90 / 1710: 28,5 Z profil boşluğu + ayrı dış sac kalktı → soğuk oda 60 geniş)' + NL +
     'TAVAN_A = Y_UST_SAC - T_PU - T_IC                                                       # v16: 1970 (v15 1968: A tavanı 60,5)' + NL +
     'TAVAN_B = 1686.0                                                                        # v16: kaset üstü 1672 + 14 · kıyma / kuşbaşı haznesi (1667) dolumda 15 kalkar → 1682 (v15 1690)' + NL +
     'SAC_T = T_DIS; PU_L = T_DUV                                                             # v16: L (soğuk ↔ teknik) 30 → 60' + NL +
     'Y_TEK = TAVAN_B + T_DUV; X_TEK = BAY_A[1] + T_DUV                                      # v16: teknik cep tabanı 1746 (dünya 1578) · sol duvarı 850 (dünya 1550)' + NL +
     'TEK_Y0 = Y_TEK + 6.0                                                                    # v16: teknik cihazlar 6 mm titreşim pedinde (topping_cad_v29)')
degis('Z_KAPAK = (-84.0, Z_ZARF); Z_SOGUK = (Z_ZARF, -565.0); Z_BOLME = (-565.0, -630.0); Z_KURU = (-630.0, -830.0)',
      'Z_KAPAK = (-84.0, Z_ZARF); Z_SOGUK = (Z_ZARF, -570.0); Z_BOLME = (-570.0, -630.0); Z_KURU = (-630.0, -830.0)   # v16: arka duvar 60 (iç sac −570…−571 · PU · dış sac −628,5…−630; v15 −565…−630 sacsız 65)')

# ---------------------------------------------------------------- 2 · kabin: v15 yan duvarları (iç sac + PU + ayrı dış sac + Z profil boşluğu) kalkar
blok('YAN_T = YUST - 1.5 - TAVAN_A', '"v14 · AISI 304 1,5 · sandviç dış kabuğu · 2 × Z profille TC yan sacına (28,5 boşluk) — soğuk paketin yük yolu")',
     'YAN_T = T_DUV                                                                           # v16: bütün yüzler 60 (v13–v15: A tavanı 60,5 · yan 60 · L 30 · arka 65 · taban 40)' + NL +
     'DUVAR = (T_IC, T_PU, T_DIS)                                                             # v16: iç 304 1,0 + PU 57,5 (40 kg/m³) + dış 304 1,5 · yan / üst dış kabuğu = TC sacı' + NL +
     '# v16: yan duvar sandviçi bölüm 1b\'de (SOĞUK KUTU) — v15\'teki ayrı dış sac + 28,5 Z profil boşluğu + Z profiller KALKTI')

# ---------------------------------------------------------------- 3 · raf: soğuk oda 60 → 1740 · bükümler alt sacın üstünde
degis('RAF_T, RAF_BUKUM = 3.0, 40.0', 'RAF_T, RAF_BUKUM = 3.0, 38.5                                                            # v16: bükümler alt dış sacın (1277–1278,5) üstünde biter')
degis('_raf = kut(90, W - 90, SOGUK_TABAN - RAF_T, SOGUK_TABAN, Z_KAPAK[1], Z_BOLME[0])', '_raf = kut(BAY_A[0], BAY_B[1], SOGUK_TABAN - RAF_T, SOGUK_TABAN, Z_KAPAK[1], Z_BOLME[0])   # v16: 60–1740')
degis('_rob = kut(90, W - 90, SOGUK_TABAN - RAF_T - RAF_BUKUM,', '_rob = kut(BAY_A[0], BAY_B[1], SOGUK_TABAN - RAF_T - RAF_BUKUM,')
degis('not_="AISI 304 · 3 mm · yük 154 kg · sehim 3,4 mm · emniyet 2,3 · ağız delikleri',
      'not_="AISI 304 · 3 mm + 2 × 38,5 büküm · v16: açıklık 1680 (v15 1620) · yük 154 kg → sehim 4,1 mm (L/410) · 101 MPa · emniyet 2,1 (bükümler + alt sandviç hesaba katılmadan) · ağız delikleri')
degis('not_="40 mm aşağı büküm (rafın kirişi)', 'not_="38,5 mm aşağı büküm (rafın kirişi · v16: alt dış sacın üstünde biter)')
degis('ekle("raf_arka_bukumu", kut(90, W - 90, SOGUK_TABAN - RAF_T - RAF_BUKUM,', 'ekle("raf_arka_bukumu", kut(BAY_A[0], BAY_B[1], SOGUK_TABAN - RAF_T - RAF_BUKUM,')

# ---------------------------------------------------------------- 4 · SOĞUK KUTU (kaplama · PU · dış saclar) + teknik zarflar
blok('# v6 · YALITIM TEK BLOK ("tam kare")', '     not_="v11: 1,5 mm AISI 304 · teknik cebin sol duvarı, PU 30\'un sağında")',
     '''YAL_Y0 = SOGUK_TABAN - 43                                                             # 1277 · soğuk oda tabanının altı (v16: alt sac 1,5 + PU 38,5 + raf 3 = 43)
Y_ALT1 = YAL_Y0 + T_DIS                                                               # v16: 1278,5 · alt dış sacın üstü (yan / arka duvarlar, raf bükümleri, köşebentler buradan)
CEP_TEKNIK = (X_TEK, W, Y_TEK, YUST, Z_KAPAK[1], -D)                                # v16: 850–1800 × 1746–2030 · yalıtımın dışında · arkası açık
# ================================================================ 1b · v16 · SOĞUK KUTU (köpük dolgulu sandviç · Kemal 29 Eyl: "yap herşeyi düzgün yap temiz olsun")
#   iç kaplama 304 1,0 TEK PARÇA (yanlar + arka + A tavanı + L + B tavanı; köşeler kaynaklı-taşlanmış) · PU 57,5 yerinde köpük · dış kabuk 1,5:
#   yanlar = TC yan sacları · A tavanı = TC tavan sacı · arka + taban + teknik taban + L dış yüzü = kutunun kendi sacları
#   (v15: yanlarda ayrı dış sac + 28,5 Z profil boşluğu · L 30 · arka 65 sacsız · tavan / arka / L'de iç kaplama yoktu)
def _kutu2(a, b, z0, z1):
    """iki kutunun birleşimi: a, b = (x0, x1, y0, y1) · z0…z1"""
    return kut(a[0], a[1], a[2], a[3], z0, z1).union(kut(b[0], b[1], b[2], b[3], z0, z1))


ODA = ((BAY_A[0], BAY_A[1], Y_ALT1 - 1.0, TAVAN_A), (BAY_A[0], BAY_B[1], Y_ALT1 - 1.0, TAVAN_B))                        # soğuk oda (kaplama tabana kadar iner)
ODA_K = ((BAY_A[0] - T_IC, BAY_A[1] + T_IC, Y_ALT1, TAVAN_A + T_IC), (BAY_A[0] - T_IC, BAY_B[1] + T_IC, Y_ALT1, TAVAN_B + T_IC))   # kaplamanın dış yüzü
ZARF_K = ((X_SAC[0], X_SAC[1], Y_ALT1, Y_TEK - T_DIS), (X_SAC[0], X_TEK - T_DIS, Y_TEK - T_DIS, Y_UST_SAC))                   # dış kabukların iç yüzü
_odak = _kutu2(*ODA_K, Z_SOGUK[1] - T_IC, Z_ZARF)
KUTU = {"soguk_ic_kaplama": _odak.cut(_kutu2(*ODA, Z_SOGUK[1], Z_ZARF + 1.0))}
_pu = _kutu2(*ZARF_K, Z_BOLME[1] + T_DIS, Z_ZARF).cut(_odak)
_psol = _pu.intersect(kut(X_SAC[0], BAY_A[0] - T_IC, Y_ALT1, TAVAN_A + T_IC, Z_SOGUK[1] - T_IC, Z_ZARF))
_psag = _pu.intersect(kut(BAY_B[1] + T_IC, X_SAC[1], Y_ALT1, Y_TEK - T_DIS, Z_SOGUK[1] - T_IC, Z_ZARF))
KUTU["kabin_sol_duvar_PU"] = _psol
KUTU["kabin_sag_duvar_PU"] = _psag
KUTU["yalitim_blogu"] = _pu.cut(_psol).cut(_psag)                                     # arka + A tavanı + L dikey + B tavanı (tek köpük)
KUTU["soguk_arka_dis_sac"] = cq.Workplane("XY", origin=(0, 0, Z_BOLME[1])).polyline([(X_SAC[0], YAL_Y0), (X_SAC[1], YAL_Y0), (X_SAC[1], Y_TEK), (X_TEK, Y_TEK),
                                                                                    (X_TEK, Y_UST_SAC), (X_SAC[0], Y_UST_SAC)]).close().extrude(T_DIS)
KUTU["teknik_ayirma_saci_yatay"] = kut(X_TEK - T_DIS, X_SAC[1], Y_TEK - T_DIS, Y_TEK, Z_BOLME[1] + T_DIS, Z_ZARF)      # B tavanının dış sacı = teknik cep tabanı
KUTU["teknik_ayirma_saci_dikey"] = kut(X_TEK - T_DIS, X_TEK, Y_TEK, Y_UST_SAC, Z_BOLME[1] + T_DIS, Z_ZARF)            # L dikeyin dış sacı = teknik cebin sol yüzü
KUTU["alt_yalitim_saci"] = kut(X_SAC[0], X_SAC[1], YAL_Y0, Y_ALT1, Z_BOLME[1] + T_DIS, Z_ZARF)                         # geçiş delikleri bölüm v12'de (ALT_DELIK)
ARKA3 = ("soguk_ic_kaplama", "yalitim_blogu", "soguk_arka_dis_sac")                   # arka duvarın katmanları


def kutu_delik(sh, adlar):
    """v16 · soğuk kutu parçalarından bir geçiş deliği çıkarır"""
    for k_ in adlar:
        KUTU[k_] = KUTU[k_].cut(sh)


kutu_delik(kut(90, 1200, 1440, 1470, Z_BOLME[1] - 1, Z_BOLME[0] + 1), ARKA3)          # geçiş bloğu yuvası (blok ölçüsünde → blok yuvaya değer)
for _u in UNO:
    kutu_delik(silz(_u[1], V_EKSEN, 15.0, Z_BOLME[1] - 1, Z_BOLME[0] + 1), ARKA3)       # UNO mil geçiş kovanı Ø30 (sıkı geçme)
RAF_BURC_Y = (Y_ALT1 + SOGUK_TABAN - RAF_T - 3.0) / 2.0                              # v16 · raf köşebendi dik kolunun ortası (1296,25)
RAF_BURC_Z = (-520.0, -360.0, -200.0, -40.0)
for _yn, _bx in (("sol", (X_SAC[0], BAY_A[0] - T_IC)), ("sag", (BAY_B[1] + T_IC, X_SAC[1]))):
    for _bz in RAF_BURC_Z:
        kutu_delik(silx(RAF_BURC_Y, _bz, 8.0, _bx[0] - 1.0, _bx[1] + 1.0), ("kabin_%s_duvar_PU" % _yn,))   # GFRP burç yuvası Ø16
YAL_BLOK = [None]                                                                     # (v15 adı · v16'da KUTU sözlüğü)
for ad, x0, x1, h_, z1_ in (("sogutma_grubu", 860, 1167, 272.0, -420.0), ("pano_PLC", 1180, 1580, 240.0, -290.0), ("guc_kaynagi", 1592, 1655, 126.0, -163.0), ("UPS", 1660, 1709, 122.0, -171.0)):
    ekle("teknik_bant_" + ad, kut(x0, x1, TEK_Y0, TEK_Y0 + h_, -40, z1_), "zarf", "Ö", not_="v16 teknik cep (yalıtımın dışında, soğuk kutunun üstünde) · ZARF · gerçek parçalar topping_cad_v29'da")''')

# ---------------------------------------------------------------- 5 · yayıcı kesme valfi tabanın altına (v15'te tabana 17 mm gömülüydü)
degis('        vx = cx - 40.0; v0, v1 = yb + 40.0, yb + 86.0',
      '        vx = cx - 40.0; v0, v1 = yb + 20.0, yb + 66.0                                      # v16: kesme valfi 20 aşağı (v15 yb + 40) → kapağı 1274, soğuk oda tabanının (1277) altında · v15\'te tabana 17 mm gömülüydü' + NL +
      '        vk = (yb + 42.5, BICAK_UST - 0.5)                                                  # v16: braket + kelepçe dik borunun üçgen gövde (1242) ile giriş kelepçesi (1262) arası')
degis('ekle("%s_spreader_valf_braketi" % k, kut(vx, cx - 18.5, v0 + 20.0, v0 + 44.0, ZT - 2.0, ZT + 2.0)',
      'ekle("%s_spreader_valf_braketi" % k, kut(vx, cx - 18.5, vk[0], vk[1], ZT - 2.0, ZT + 2.0)')
degis('ekle("%s_spreader_valf_kelepcesi" % k, sily(cx, ZT, 21.0, v0 + 20.0, v0 + 44.0).cut(sily(cx, ZT, 18.1, v0 + 19.0, v0 + 45.0))',
      'ekle("%s_spreader_valf_kelepcesi" % k, sily(cx, ZT, 21.0, vk[0], vk[1]).cut(sily(cx, ZT, 18.1, vk[0] - 1.0, vk[1] + 1.0))')
degis('ekle("%s_spreader_valf_mili" % k, silx(v0 + 32.0, ZT, 3.0, vx + 14.0, cx - 18.0)',
      'ekle("%s_spreader_valf_mili" % k, silx((vk[0] + vk[1]) / 2.0, ZT, 3.0, vx + 14.0, cx - 18.0)')

# ---------------------------------------------------------------- 6 · kaset kovanı delikleri → bütün arka duvar katmanları
degis('        YAL_BLOK[0] = YAL_BLOK[0].cut(silz(xc, yy, 30.0, Z_BOLME[1] - 1, Z_BOLME[0] + 1))',
      '        kutu_delik(silz(xc, yy, 30.0, Z_BOLME[1] - 1, Z_BOLME[0] + 1), ARKA3)                            # v16: kaplama + PU + arka dış sac')

# ---------------------------------------------------------------- 7 · SOĞUTMA (evaporatör içeride) + kutu parçaları eklenir
blok('ekle("yalitim_blogu", YAL_BLOK[0], "pu", "Ö",', 'teknik cep yalıtımın dışında · 4 kaset kovanı + 4 UNO kovanı + geçiş bloğu delikleri")',
     '''# ================================================================ 3c · v16 · SOĞUTMA: EVAPORATÖR KUTUNUN İÇİNDE (v15: TC kuru bölmesinde çıplaktı → +134 W, kuru bölmede yoğuşma · sogutma_topping_v1)
#   standart üstten üniteli dolap düzeni: fanlı ince evaporatör A bölmesinin tavanında, SOS haznesinin üstünde (dolumda hazne 15 kalkar → 1752 < 1762) ·
#   yoğuşma ünitesi (Secop CU KLF4.8CND, topping_cad_v29) teknik cepte · hatlar L duvarındaki POM bloktan · yoğuşma suyu arka duvardan kuru bölmedeki
#   elektrikli buharlaştırma kabına. EVAPORATÖR YAPTIRILACAK (soğutmacı firma): model YER ZARFI 260 × 208 × 500
EVAP = (BAY_A[0] + 6.0, BAY_A[0] + 266.0, 1762.0, TAVAN_A, -560.0, -60.0)           # x 66–326 · y 1762–1970 · z −560…−60
_ex0, _ex1, _ey0, _ey1, _ez0, _ez1 = EVAP
_g = kut(_ex0, _ex1, _ey1 - 1.0, _ey1, _ez0, _ez1)                                    # üst sac (tavan kaplamasına)
_g = _g.union(kut(_ex0, _ex0 + 1.0, _ey0, _ey1, _ez0, _ez1)).union(kut(_ex1 - 1.0, _ex1, _ey0, _ey1, _ez0, _ez1))   # yan saclar
_g = _g.union(kut(_ex0, _ex1, _ey0, _ey1, _ez0, _ez0 + 1.0))                          # arka sac
_g = _g.union(kut(_ex0, _ex1, _ey0, _ey0 + 1.0, -322.0, _ez1))                        # ön-alt sac (fan + üfleme kanalının altı)
ekle("evaporator_govdesi", _g, "paslanmaz", "V",
     not_="v16 · evaporatör gövdesi AISI 304 1,0 · 260 × 208 × 500 · A tavan kaplamasına 4 × M6 perçin somun (köpük içi takviye lama) · emiş arka-alt açıklıktan (z −559…−478) · üfleme ön yüzden tavan boyunca kapıya · YER ZARFI (soğutmacı firma)")
ekle("evaporator_lamel_paketi", kut(_ex0 + 1.0, _ex1 - 1.0, 1790.0, 1965.0, -470.0, -330.0), "aluminyum", "V",
     not_="v16 · lamel paketi (Al kanat / Cu boru) 258 × 175 × 140 · hava z yönünde · 300–380 W @ −10 °C (gereken 231–326 W @ 32 °C · sogutma_topping_v1) · uç plakaları gövde yan saclarına · YER ZARFI")
ekle("evaporator_fani", kut(_ex0 + 55.0, _ex0 + 205.0, 1802.0, 1952.0, -330.0, -280.0), "motor", "V",
     not_="v16 · eksenel fan 150 × 150 × 50 (EC 24 V) · lamel paketinin ön çerçevesine 4 × M4 · paketten çekip tavan boyunca kapıya üfler · model / debi soğutmacı firma")
ekle("evaporator_damlama_tavasi", kut(_ex0 + 1.0, _ex1 - 1.0, 1766.0, 1790.0, -478.0, -322.0).cut(kut(_ex0 + 2.0, _ex1 - 2.0, 1767.0, 1791.0, -477.0, -323.0)), "paslanmaz", "V",
     not_="v16 · damlama tavası 304 1,0 · lamel paketinin altında · %1 eğimle sol-arka köşedeki Ø8 çıkışa")
TAHLIYE = [(90.0, 1766.0, -470.0), (90.0, 1754.0, -470.0), (90.0, 1754.0, -660.0), (90.0, 1745.0, -660.0)]
ekle("evaporator_tahliye_hortumu", boru(TAHLIYE, 4.0), "silikon", "V",
     not_="v16 · yoğuşma tahliyesi Ø8 silikon · tavadan SOS haznesinin solundan (x 86–94 < 100) arka duvara, duvar deliği hortum çapında (silikonla) · kuru bölmedeki buharlaştırma kabına düşer · sifonlu")
kutu_delik(silz(90.0, 1754.0, 4.0, Z_BOLME[1] - 1.0, Z_BOLME[0] + 1.0), ARKA3)
ekle("yogusma_buharlastirma_kabi", kut(60.0, 160.0, 1700.0, 1745.0, -790.0, Z_BOLME[1]).cut(kut(62.0, 158.0, 1702.0, 1746.0, -788.0, Z_BOLME[1] - 2.0)), "paslanmaz", "V",
     not_="v16 · elektrikli yoğuşma buharlaştırma kabı 100 × 45 × 160 (0,6 L · 30 W rezistans + şamandıra, VARSAYIM) · arka duvarın dış sacına 2 × M5 · altında elektrik yok (valf adası x ≥ 150, bobinler y ≤ 1690)")
HAT_GECIS = (BAY_A[1], X_TEK, 1885.0, 1955.0, -425.0, -375.0)                       # L duvarı hat geçişi (kaplama + PU + dış sac)
_hg = kut(*HAT_GECIS)
for _hy, _hr in ((1935.0, 15.5), (1905.0, 3.2)):
    _hg = _hg.cut(silx(_hy, -400.0, _hr, BAY_A[1] - 1.0, X_TEK + 1.0))
kutu_delik(kut(*HAT_GECIS), ("soguk_ic_kaplama", "yalitim_blogu", "teknik_ayirma_saci_dikey"))
ekle("sogutma_hat_gecis_blogu", _hg, "pom", "V", not_="v16 · POM-C hat geçiş bloğu 60 × 70 × 50 · L duvarını boydan geçer · iki hat deliği hat çapında (silikonla sızdırmaz)")
ekle("sogutma_emis_hatti", silx(1935.0, -400.0, 15.5, _ex1, 860.0), "koyu", "V",
     not_="v16 · emiş hattı Cu Ø12,7 + Armaflex 9 mm (dış Ø31) · evaporatörün sağ yüzünden L duvarından teknik cepteki yoğuşma ünitesine (topping_cad_v29, x 860) · HARÇ haznesinin üstünden (1832; dolumda 1847)")
ekle("sogutma_sivi_hatti", silx(1905.0, -400.0, 3.2, _ex1, 860.0), "celik", "V",
     not_="v16 · sıvı hattı Cu Ø6,35 · genleşme valfi / kılcal evaporatör girişinde (soğutmacı firma)")
for _k, _mal, _not in (
        ("soguk_ic_kaplama", "paslanmaz", "v16 · İÇ KAPLAMA AISI 304 1,0 TEK PARÇA: yanlar + arka + A tavanı + L + B tavanı (köşeler kaynaklı-taşlanmış, iç köşe R ≥ 6) · önü açık (430 çerçeve + kapaklar) · tabanı raf · kovan / blok / tahliye delikleri"),
        ("kabin_sol_duvar_PU", "pu", "v16 · sol duvar PU 57,5 (40 kg/m³, yerinde köpük) · dış kabuğu TC sol yan sacı (x 0–1,5) · iç kaplamaya ve sacın iç yüzüne yapışık · v15'teki ayrı dış sac + 28,5 Z profil boşluğu KALKTI · 4 GFRP raf burcu"),
        ("kabin_sag_duvar_PU", "pu", "v16 · sağ duvar PU 57,5 · dış kabuğu TC sağ yan sacı (x 1798,5–1800) · teknik tabana kadar · 4 GFRP raf burcu"),
        ("yalitim_blogu", "pu", "v16 · PU 57,5 TEK KÖPÜK: arka duvar + A tavanı + L dikey + B tavanı (hepsi 60 sandviç; v15: A tavanı 60,5 · L 30 · arka 65 sacsız) · 4 kaset + 4 UNO kovanı + geçiş bloğu + hat bloğu + tahliye delikleri"),
        ("soguk_arka_dis_sac", "paslanmaz", "v16 · arka duvarın dış kabuğu AISI 304 1,5 (kuru bölmeye bakar) · x 1,5–1798,5 · A tarafında TC tavanına, teknik cep tarafında teknik tabana kadar · kovan / blok / tahliye delikleri"),
        ("teknik_ayirma_saci_yatay", "paslanmaz", "v16 · B tavanının dış kabuğu = TEKNİK CEP TABANI AISI 304 1,5 (dünya 1576,5–1578) · cihazlar bunun üstüne titreşim pedleriyle (topping_cad_v29) · B tavanı iki ucundan (L duvarı + sağ duvar) taşınır, konsol yok"),
        ("teknik_ayirma_saci_dikey", "paslanmaz", "v16 · L dikey duvarın dış kabuğu AISI 304 1,5 (teknik cebin sol yüzü, dünya x 1548,5–1550) · T sol dikme köşebentleri buna (topping_cad_v29) · hat bloğu deliği")):
    ekle(_k, KUTU[_k], _mal, "Ö", not_=_not)''')

# ---------------------------------------------------------------- 8 · sağ duvar alt profili (itici kirişi) kalkar
blok('# v14b · SAĞ DUVAR ALT PROFİLİ (denetim_C bulgu 11)', 'yük: kiriş → profil → TC yan sacı")',
     '# v16 · SAĞ DUVAR ALT PROFİLİ KALKTI (aktarma iticisi v70\'ten beri yok — bantlı tabla; profil v15\'te Z profil boşluğundaydı)')

# ---------------------------------------------------------------- 9 · taban: tek parça alt dış sac + PU 38,5
degis('    if p["ad"].startswith(("tasiyici_raf", "raf_", "yalitim_blogu", "kabin_", "baglam", "kompresor", "hava_ana", "teknik_bant", "pide", "tabla_diski")):',
      '    if p["ad"].startswith(("tasiyici_raf", "raf_", "yalitim_blogu", "kabin_", "baglam", "kompresor", "hava_ana", "teknik_bant", "pide", "tabla_diski", "soguk_", "teknik_ayirma", "evaporator", "sogutma_", "yogusma_")):')
blok('ekle("alt_yalitim_saci", _alt.intersect(', 'iniş borusu + huni altı / önü dolu")',
     '''_asc = KUTU["alt_yalitim_saci"]
for _ad, x0_, x1_, z0_, z1_ in ALT_DELIK:
    _asc = _asc.cut(kut(x0_, x1_, YAL_Y0 - 1.0, Y_ALT1 + 1.0, z0_, z1_))
ekle("alt_yalitim_saci", _asc.val(), "paslanmaz", "V",
     not_="v16 · soğuk kutunun ALT DIŞ KABUĞU AISI 304 1,5 TEK PARÇA · x 1,5–1798,5 (yan ve arka duvarların altını da kapatır, v15 1,0 ve yalnız raf altı) · aşağı bakar (pişirme bölgesinin üstü) · geçişlerde 3 mm boşluklu delik")
ekle("alt_yalitim_PU", _alt.intersect(kut(ALT_YAL[0], ALT_YAL[1], Y_ALT1, ALT_YAL[3], ALT_YAL[4], ALT_YAL[5])).val(), "pu", "V",
     not_="v16 · taban PU 38,5 (40 kg/m³) · rafın altı, bükümlerin ve köşebentlerin arası · kaset / UNO / hava geçişlerinde 3 mm boşluklu delik · kaset yalnız ÜST 6 mm yarık (öne açık, yarık diliyle dolu) · TABAN 43: UNO ağzı + yayıcı kelepçesi 1274'te — daha kalını kelepçeyi yalıtıma gömer")''')

# ---------------------------------------------------------------- 10 · raf köşebentleri: alt sacın üstünden · GFRP burçla TC yan sacına
degis('    _L = _L.union(kut(_x0, _x0 + _sg * 3.0, YAL_Y0, SOGUK_TABAN - RAF_T, Z_BOLME[0] + RAF_T, Z_KAPAK[1] - RAF_T))',
      '    _L = _L.union(kut(_x0, _x0 + _sg * 3.0, Y_ALT1, SOGUK_TABAN - RAF_T, Z_BOLME[0] + RAF_T, Z_KAPAK[1] - RAF_T))   # v16: alt dış sacın üstünden')
degis('not_="v14 · L 40 × 40 × 3 AISI 304 · rafın ucu yatay koluna oturur (M5 havşa) · dik kol duvarın iç sacına 4 × M6 · raf 154 kg → uç başına 0,76 kN")',
      '''not_="v16 · L 40 × 40 × 3 AISI 304 · rafın ucu yatay koluna oturur (M5 havşa) · dik kol iç kaplamaya dayalı, 4 × M8 GFRP burçtan TC yan sacına · raf 154 kg → uç başına 0,76 kN")
    _bx = (X_SAC[0], BAY_A[0] - T_IC) if _yn == "sol" else (BAY_B[1] + T_IC, X_SAC[1])
    _bc = None
    for _bz in RAF_BURC_Z:
        _b = silx(RAF_BURC_Y, _bz, 8.0, _bx[0], _bx[1]).cut(silx(RAF_BURC_Y, _bz, 4.5, _bx[0] - 1.0, _bx[1] + 1.0))
        _bc = _b if _bc is None else _bc.union(_b)
    ekle("raf_askisi_burclari_%s" % _yn, _bc, "pom", "H",
         not_="v16 · 4 × ısı köprüsü kesici burç GFRP Ø16/Ø9 × 57,5 (PU'nun içinden) · raf köşebendini TC yan sacına bağlayan M8 A2 cıvata içinden geçer, sacda kör perçin somun · 0,76 kN → cıvata başına 190 N")''')

# ---------------------------------------------------------------- 11 · Z profiller kalkar
blok('# (b) Z PROFİLLER 2 mm', '        ZPROF.append("soguk_duvar_%s_z_profili_%d" % (_yn, _i))',
     '# (b) v16: Z PROFİLLER KALKTI — yan duvarın dış kabuğu TC yan sacının kendisi (boşluk yok)' + NL + 'ZPROF = []')

# ---------------------------------------------------------------- 12 · ön yüz: K2 teknik tabana kadar · menteşe kolları fitile yer açar · K2 bas-aç
degis('"K2": dict(x=(xu(1521.5), xu(2497.0)), y=(yu(1110.5), yu(1550.5)),', '"K2": dict(x=(xu(1521.5), xu(2497.0)), y=(yu(1110.5), yu(1575.0)),')
degis('''for _ad, _x0, _x1, _y0, _tx in (("K1_mentese_0", 31.5, 55.0, 1330.0, (1.5, 31.5)), ("K1_mentese_1", 31.5, 55.0, 1900.0, (1.5, 31.5)),
                               ("K2_mentese_0", xu(2443.0), xu(2468.5), 1330.0, (xu(2468.5), xu(2498.5))), ("K2_mentese_1", xu(2443.0), xu(2468.5), 1620.0, (xu(2468.5), xu(2498.5)))):''',
      '''for _ad, _x0, _x1, _y0, _tx in (("K1_mentese_0", 31.5, 44.0, 1330.0, (1.5, 31.5)), ("K1_mentese_1", 31.5, 44.0, 1900.0, (1.5, 31.5)),        # v16: fitil 60'a geldi (x 45,5–66,5) → kol 31,5–44 (TC yan sacının ön dönüşü 1,5–31,5'in yanında) · taban aynı
                               ("K2_mentese_0", xu(2456.0), xu(2468.5), 1330.0, (xu(2468.5), xu(2498.5))), ("K2_mentese_1", xu(2456.0), xu(2468.5), 1620.0, (xu(2468.5), xu(2498.5)))):''')
degis('not_="v14b · çok kollu gizli menteşe KOLU (kapak tarafı', 'not_="v16 · kol 12,5 geniş (fitil 30 dışa geldi, x 45,5 / 1754,5) · v14b · çok kollu gizli menteşe KOLU (kapak tarafı')
degis('("basac_K2", 830.0, 870.0, 1705.5, 1717.5)', '("basac_K2", 830.0, 870.0, 1730.0, 1742.0)')

# ---------------------------------------------------------------- 13 · denetim
degis('kontrol("sos valf eyleyicisi sol duvara değmiyor (%.0f > 90)" % bb("sos__valf_dondurme_aktuatoru").xmin, bb("sos__valf_dondurme_aktuatoru").xmin > 90)',
      'kontrol("sos valf eyleyicisi sol duvara değmiyor (%.0f > %.0f)" % (bb("sos__valf_dondurme_aktuatoru").xmin, BAY_A[0]), bb("sos__valf_dondurme_aktuatoru").xmin > BAY_A[0])')
blok('_sd = [p for p in P if p["ad"] in ("kabin_sol_duvar_PU", "kabin_sag_duvar_PU")]', 'abs(_bs.xmin - BAY_B[1]) < 0.01))',
     '''# v16 · SOĞUK KUTU: her yüz 60 · yan dış kabuk = TC yan sacı · boşluk yok
_sd = [p for p in P if p["ad"] in ("kabin_sol_duvar_PU", "kabin_sag_duvar_PU")]
kontrol("v16 · yan PU duvarları alt dış sacın üstünden (%.1f) başlıyor · TC yan saclarının iç yüzüne YAPIŞIK (x %.1f / %.1f · boşluk 0, v15 28,5)" % (Y_ALT1, bb("kabin_sol_duvar_PU").xmin, bb("kabin_sag_duvar_PU").xmax),
        all(abs(p["sh"].BoundingBox().ymin - Y_ALT1) < 0.01 for p in _sd) and abs(bb("kabin_sol_duvar_PU").xmin - X_SAC[0]) < 0.01 and abs(bb("kabin_sag_duvar_PU").xmax - X_SAC[1]) < 0.01)
_k60 = {"sol duvar": BAY_A[0], "sağ duvar": W - BAY_B[1], "arka": Z_BOLME[0] - Z_BOLME[1], "A tavanı": YUST - TAVAN_A, "L dikey": X_TEK - BAY_A[1], "B tavanı": Y_TEK - TAVAN_B}
kontrol("v16 · BÜTÜN YÜZLER 60 (kaplama 1,0 + PU 57,5 + dış 1,5): %s · PU yan %.1f / %.1f · taban %.0f (UNO ağzı + yayıcı kelepçesi 1274'te) · kapaklar 40"
        % (" · ".join("%s %.1f" % (a_, v_) for a_, v_ in _k60.items()), bb("kabin_sol_duvar_PU").xlen, bb("kabin_sag_duvar_PU").xlen, SOGUK_TABAN - YAL_Y0),
        all(abs(v_ - T_DUV) < 0.01 for v_ in _k60.values()) and abs(bb("kabin_sol_duvar_PU").xlen - T_PU) < 0.01 and abs(bb("kabin_sag_duvar_PU").xlen - T_PU) < 0.01)''')
degis('_yb = bb("yalitim_blogu"); kontrol("yalıtım tek blok, dışı düz (x %.0f…%.0f · y %.0f…%.0f · z %.0f…%.0f)" % (_yb.xmin, _yb.xmax, _yb.ymin, _yb.ymax, _yb.zmin, _yb.zmax), _yb.xmin == BAY_A[0] and _yb.xmax == BAY_B[1] and _yb.zmax == Z_KAPAK[1] and _yb.zmin == Z_BOLME[1])',
      '''_yb = bb("yalitim_blogu"); _ik = bb("soguk_ic_kaplama")
kontrol("v16 · PU tek köpük (arka + A tavanı + L + B tavanı: x %.1f…%.1f · y %.1f…%.1f · z %.1f…%.1f) · iç kaplama TEK PARÇA (x %.0f…%.0f · y %.1f…%.0f · z %.0f…%.0f)"
        % (_yb.xmin, _yb.xmax, _yb.ymin, _yb.ymax, _yb.zmin, _yb.zmax, _ik.xmin, _ik.xmax, _ik.ymin, _ik.ymax, _ik.zmin, _ik.zmax),
        len([p for p in P if p["ad"] == "yalitim_blogu"][0]["sh"].Solids()) == 1 and len([p for p in P if p["ad"] == "soguk_ic_kaplama"][0]["sh"].Solids()) == 1
        and abs(_yb.xmin - X_SAC[0]) < 0.01 and abs(_yb.xmax - X_SAC[1]) < 0.01 and abs(_yb.zmax - Z_ZARF) < 0.01 and abs(_yb.zmin - Z_BOLME[1] - T_DIS) < 0.01 and abs(_yb.ymax - Y_UST_SAC) < 0.01
        and abs(_ik.xmin - BAY_A[0] + T_IC) < 0.01 and abs(_ik.xmax - BAY_B[1] - T_IC) < 0.01 and abs(_ik.ymax - TAVAN_A - T_IC) < 0.01 and abs(_ik.zmin - Z_SOGUK[1] + T_IC) < 0.01)''')
blok('_kb = 0; _ybs = [q for q in P if q["ad"] == "yalitim_blogu"][0]["sh"]', 'kontrol("yalıtım bloğuna hiçbir parça girmiyor (kovanlar deliklerinde)", _kb == 0, "%d" % _kb)',
     '''KUTU_AD = tuple(KUTU) + ("alt_yalitim_PU",)
_BAGLAM = ("kabin_taban_saci", "kabin_arka_saci", "kabin_ust_saci", "kabin_sag_teknik_sac", "teknik_bant", "baglam", "kompresor", "hava_ana", "pide", "tabla_diski")
_kb = []
_ks = [(q["ad"], q["sh"], q["sh"].BoundingBox()) for q in P if q["ad"] in KUTU_AD]
for p in P:
    if p["ad"].startswith(_BAGLAM): continue
    b_ = p["sh"].BoundingBox()
    for a_, s_, bk_ in _ks:
        if a_ == p["ad"]: continue
        if b_.xmax < bk_.xmin or bk_.xmax < b_.xmin or b_.ymax < bk_.ymin or bk_.ymax < b_.ymin or b_.zmax < bk_.zmin or bk_.zmax < b_.zmin: continue
        try: v_ = p["sh"].intersect(s_).Volume()
        except Exception: v_ = -1.0
        if v_ > 1.0 or v_ < 0: _kb.append((p["ad"], a_, round(v_, 1)))
kontrol("v16 · soğuk kutuya (kaplama · 3 PU · dış saclar · taban) hiçbir parça girmiyor · kutu parçaları birbirine girmiyor (kovan / blok / hortum / burç deliklerinde): %d" % len(_kb), not _kb, str(_kb[:6]))''')
blok('_ay = bb("alt_yalitim_PU"); _as = bb("alt_yalitim_saci")', 'abs(_ay.xmax - BAY_B[1] + 3.0) < 0.01)   # v14: iki uçta raf köşebendinin dik kolu (3)',
     '''_ay = bb("alt_yalitim_PU"); _as = bb("alt_yalitim_saci")
kontrol("v16 · soğuk oda TABANI 43: alt dış sac 1,5 y %.1f–%.1f (x %.1f–%.1f TEK PARÇA, yan + arka duvarların altı dahil) + PU 38,5 y %.1f–%.1f · x %.0f–%.0f · z %.0f…%.0f + raf 3 · %d geçiş deliği"
        % (_as.ymin, _as.ymax, _as.xmin, _as.xmax, _ay.ymin, _ay.ymax, _ay.xmin, _ay.xmax, _ay.zmin, _ay.zmax, len(ALT_DELIK)),
        abs(_ay.ymax - (SOGUK_TABAN - RAF_T)) < 0.01 and abs(_ay.ymin - Y_ALT1) < 0.01 and abs(_as.ymin - YAL_Y0) < 0.01 and abs(_as.ymax - Y_ALT1) < 0.01
        and abs(_as.xmin - X_SAC[0]) < 0.01 and abs(_as.xmax - X_SAC[1]) < 0.01 and abs(_ay.xmin - BAY_A[0] - 3.0) < 0.01 and abs(_ay.xmax - BAY_B[1] + 3.0) < 0.01)''')
blok('kontrol("v14 · soğuk zarf ön yüzü +%.0f: yalıtım bloğu', '"soguk_duvar_sol_ic_sac", "soguk_duvar_sag_ic_sac")))',
     '''_ZA = ("yalitim_blogu", "tasiyici_raf_3mm", "raf_on_bukumu", "teknik_ayirma_saci_yatay", "teknik_ayirma_saci_dikey", "kabin_sol_duvar_PU", "kabin_sag_duvar_PU", "soguk_ic_kaplama", "alt_yalitim_saci")
kontrol("v16 · soğuk kutunun ön yüzü TEK DÜZLEM +%.0f (%d parça: kaplama, 3 PU, teknik saclar, alt sac, raf) · alt PU %.1f (raf ön bükümünün arkası)" % (Z_ZARF, len(_ZA), bb("alt_yalitim_PU").zmax),
        all(abs(bb(a_).zmax - Z_ZARF) < 0.01 for a_ in _ZA) and abs(bb("alt_yalitim_PU").zmax - (Z_ZARF - RAF_T)) < 0.01)''')
degis('("motor_kablosu_sucuk_cad_v8_rotor", "motor_sucuk_cad_v8_rotor"), ("soguk_duvar_sag_alt_profili", "soguk_duvar_sag_dis_sac"), ("soguk_duvar_sag_alt_profili", "soguk_duvar_sag_z_profili_0"),',
      '("motor_kablosu_sucuk_cad_v8_rotor", "motor_sucuk_cad_v8_rotor"),')
degis('("raf_kosebendi_sol", "soguk_duvar_sol_ic_sac"), ("raf_kosebendi_sag", "soguk_duvar_sag_ic_sac"),',
      '("raf_kosebendi_sol", "soguk_ic_kaplama"), ("raf_kosebendi_sag", "soguk_ic_kaplama"),')
degis('("soguk_duvar_sol_z_profili_0", "soguk_duvar_sol_dis_sac"), ("soguk_duvar_sag_z_profili_0", "soguk_duvar_sag_dis_sac"),',
      '''("raf_askisi_burclari_sol", "soguk_ic_kaplama"), ("raf_askisi_burclari_sag", "soguk_ic_kaplama"), ("kabin_sol_duvar_PU", "soguk_ic_kaplama"), ("kabin_sag_duvar_PU", "soguk_ic_kaplama"),
                ("yalitim_blogu", "soguk_ic_kaplama"), ("yalitim_blogu", "soguk_arka_dis_sac"), ("yalitim_blogu", "teknik_ayirma_saci_yatay"), ("yalitim_blogu", "teknik_ayirma_saci_dikey"),
                ("alt_yalitim_saci", "soguk_arka_dis_sac"), ("alt_yalitim_saci", "kabin_sol_duvar_PU"), ("alt_yalitim_PU", "alt_yalitim_saci"), ("raf_on_bukumu", "alt_yalitim_saci"), ("raf_arka_bukumu", "soguk_ic_kaplama"),
                ("evaporator_govdesi", "soguk_ic_kaplama"), ("evaporator_lamel_paketi", "evaporator_govdesi"), ("evaporator_fani", "evaporator_lamel_paketi"), ("evaporator_damlama_tavasi", "evaporator_govdesi"),
                ("evaporator_tahliye_hortumu", "evaporator_damlama_tavasi"), ("yogusma_buharlastirma_kabi", "soguk_arka_dis_sac"), ("sogutma_emis_hatti", "evaporator_govdesi"), ("sogutma_sivi_hatti", "evaporator_govdesi"),
                ("sogutma_hat_gecis_blogu", "soguk_ic_kaplama"), ("sogutma_emis_hatti", "sogutma_hat_gecis_blogu"), ("sogutma_sivi_hatti", "sogutma_hat_gecis_blogu"),''')
degis('# ---------------------------------------------------------------- v14b · denetim_C düzeltmeleri (TU tek başına; dünya karşılıkları topping_cad_v25.dunya_denetimi)',
      '''# ---------------------------------------------------------------- v16 · SOĞUK KUTU + SOĞUTMA
_ev = bb("evaporator_govdesi"); _sh_ = bb("sos_hazne_bizim"); _hh = bb("harc_hazne_bizim"); _eh = bb("sogutma_emis_hatti"); _sv = bb("sogutma_sivi_hatti")
kontrol("v16 · evaporatör soğuk odanın İÇİNDE (x %.0f–%.0f ⊂ %.0f–%.0f · y %.0f–%.0f ≤ tavan %.0f · z %.0f…%.0f) · SOS haznesi dolumda 15 kalkınca %.0f < evaporatör altı %.0f"
        % (_ev.xmin, _ev.xmax, BAY_A[0], BAY_A[1], _ev.ymin, _ev.ymax, TAVAN_A, _ev.zmin, _ev.zmax, _sh_.ymax + 15.0, _ev.ymin),
        _ev.xmin >= BAY_A[0] and _ev.xmax <= BAY_A[1] and _ev.ymax <= TAVAN_A + 0.01 and _ev.zmin >= Z_SOGUK[1] and _ev.zmax <= Z_ZARF and _sh_.ymax + 15.0 < _ev.ymin)
kontrol("v16 · soğutma hatları (emiş Ø31 yalıtımlı + sıvı Ø6,35) L duvarındaki POM bloktan teknik cebe (x %.0f → %.0f) · HARÇ haznesinin üstünden: hat altı %.1f > hazne dolumda %.0f · tavan altı %.1f < %.0f"
        % (_eh.xmin, _eh.xmax, min(_eh.ymin, _sv.ymin), _hh.ymax + 15.0, max(_eh.ymax, _sv.ymax), TAVAN_A),
        _eh.xmax >= X_TEK and min(_eh.ymin, _sv.ymin) > _hh.ymax + 15.0 and max(_eh.ymax, _sv.ymax) < TAVAN_A)
_th = bb("evaporator_tahliye_hortumu"); _yk = bb("yogusma_buharlastirma_kabi")
kontrol("v16 · yoğuşma suyu: tava → Ø8 hortum arka duvardan (y %.0f) → kuru bölmedeki elektrikli buharlaştırma kabı (üstü %.0f · x %.0f–%.0f) · altında elektrik yok (valf adası x ≥ %.0f · bobin üstü %.0f)"
        % (TAHLIYE[1][1], _yk.ymax, _yk.xmin, _yk.xmax, ADA[0], ADA[3] + 30.0), TAHLIYE[1][1] > _yk.ymax and _yk.zmax <= Z_BOLME[1] + 0.01 and _yk.ymin > ADA[3] + 30.0)
for _u in ("sos", "harc"):
    _vk = bb("%s_spreader_kesme_valfi_kapak" % _u); _gk_ = bb("%s_spreader_giris_kelepcesi" % _u)
    kontrol("v16 · %s yayıcısı tabanın ALTINDA: kesme valfi kapağı %.0f · giriş kelepçesi %.0f < taban altı %.0f (v15'te valf tabana 17 mm gömülüydü)" % (_u, _vk.ymax, _gk_.ymax, YAL_Y0),
            _vk.ymax < YAL_Y0 and _gk_.ymax < YAL_Y0)
# v16 · BOŞLUK YOK (Kemal: "sağ sol duvardaki yalıtımla sac duvar arasında boşluk var"): taban üstünde (y ≥ 1320) dış kabukların içi = oda + kutu parçaları + geçişler
_ZT_ = _kutu2((X_SAC[0], X_SAC[1], SOGUK_TABAN, Y_TEK), (X_SAC[0], X_TEK, Y_TEK, Y_UST_SAC), Z_BOLME[1], Z_ZARF).val()
_ODT = _kutu2((BAY_A[0], BAY_A[1], SOGUK_TABAN, TAVAN_A), (BAY_A[0], BAY_B[1], SOGUK_TABAN, TAVAN_B), Z_SOGUK[1], Z_ZARF + 1.0).val()
_kal = _ZT_.cut(_ODT)
for _p in P:
    if _p["ad"] in KUTU or _p["ad"].startswith(("kovan_", "gecis_blogu_yalitim", "sogutma_hat_gecis_blogu", "raf_askisi_burclari", "evaporator_tahliye_hortumu", "sogutma_emis_hatti", "sogutma_sivi_hatti")) \\
            or _p["ad"].endswith("_mil_gecis_kovani") or _p["ad"] in HORTUM_GECIS:
        _kal = _kal.cut(_p["sh"])
for _p in [p for p in P if p["ad"].startswith("kovan_") or p["ad"].endswith("_mil_gecis_kovani")]:          # kovan içi = mil (keçeli geçiş, ölçüm dışı)
    _b = _p["sh"].BoundingBox(); _kal = _kal.cut(silz((_b.xmin + _b.xmax) / 2.0, (_b.ymin + _b.ymax) / 2.0, 11.5, _b.zmin - 1.0, _b.zmax + 1.0).val())
_kv = [(s_.Volume(), s_.BoundingBox()) for s_ in _kal.Solids() if s_.Volume() > 1e-3]
kontrol("v16 · soğuk kutu duvar + tavanlarında BOŞLUK YOK (y ≥ %.0f · dış kabukların içi = oda + kaplama + PU + saclar + kovan / blok / hortum geçişleri): kalan %.2f mm³ ≤ 5"
        % (SOGUK_TABAN, sum(v_ for v_, b_ in _kv)), sum(v_ for v_, b_ in _kv) <= 5.0, str([(round(v_, 1), round(b_.xmin), round(b_.ymin), round(b_.zmin)) for v_, b_ in sorted(_kv, key=lambda t: -t[0])[:6]]))

# ---------------------------------------------------------------- v14b · denetim_C düzeltmeleri (TU tek başına; dünya karşılıkları topping_cad_v25.dunya_denetimi)''')
degis('assert not kal, "topping_uno_cad_v14 denetimi KALDI: %s" % kal', 'assert not kal, "topping_uno_cad_v16 denetimi KALDI: %s" % kal')
degis('"generator": "AUTOKITCH topping_uno_cad_v14"', '"generator": "AUTOKITCH topping_uno_cad_v16"')
degis('glb_yaz(os.path.join(_od, "topping_uno_v15.glb"))', 'glb_yaz(os.path.join(_od, "topping_uno_v16.glb"))')
degis('with open(os.path.join(_od, "topping_uno_v15.json"), "w", encoding="utf-8") as f:', 'with open(os.path.join(_od, "topping_uno_v16.json"), "w", encoding="utf-8") as f:')
degis('json.dump(dict(surum="topping_uno_cad_v15 · %s"', 'json.dump(dict(surum="topping_uno_cad_v16 · %s"')
assert "soguk_duvar_sol_dis_sac" not in s and "soguk_duvar_sag_alt_profili\"," not in s, "eski duvar adı kaldı"
compile(s, "topping_uno_cad_v16.py", "exec")
io.open(os.path.join(U, "topping_uno_cad_v16.py"), "w", encoding="utf-8").write(s)
print("topping_uno_cad_v16.py yazildi")
