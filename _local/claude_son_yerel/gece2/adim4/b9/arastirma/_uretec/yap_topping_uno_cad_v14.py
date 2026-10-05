# -*- coding: utf-8 -*-
"""topping_uno_cad_v13.py -> topping_uno_cad_v14.py (27/28 Eyl 2026 gece) · ÖN DÜZLEM +79 · SOĞUK ODA KAPAKLI TEMİZ KUTU (SPEC_on_duzlem_v63.md §1 + §2.3)
Kemal: "fırının ön yüzü sınır yüzey, her şeyi o yüzeye getireceğiz … içeride havada kalan parça olmasın … her istasyon kendi başına temiz bir kutu".
Yapılanlar (TU = soğuk paket + UNO'lar + kasetler + hava tesisatı; dünya: x + 700 · y − 168):
  · soğuk zarf öne uzar: yalıtım bloğu / yan duvarlar / raf + bükümler / alt yalıtım / teknik ayırma sacları ön yüzü −104 → +23 (Z_KAPAK[1] = Z_ZARF)
  · yan duvarlar SANDVİÇ: 304 1,5 dış + PU 57,5 + 304 1,0 iç = 60 · duvar ↔ TC yan sacı 2 × Z profil (28,5 boşluk) · raf uçları L 40 × 40 × 3 köşebentlere oturur
  · 430 ön çerçeve sacı +23…+24 · soğuk kapaklar K1 (sol menteşe) / K2 (sağ menteşe) 40 sandviç +39…+79 · manyetik fitil +24…+39 (store_cad_v7 profili)
    · K1 kenarında katlanır orta dikme (flipper, ısıtıcılı) · kaset tüpü çentikleri fitilin İÇİNDE (conta sürekli)
  · eski fitil (−104) silindi · havada kalanlar bağlandı (kaset tahrik grubu, iniş boruları, TC kelepçeler, D70 silindirler, UNO çıkış ferrulü, mandal pimi)
  · hortumlar yeniden yollandı (üst üste binmiyor) + geçiş bloğunda hortum delikleri · açıcı hattı 2 × Ø6 → Z silindirine (TC v25) · kompresör vanası motorda
  · kaset çekme testi 0–630 (kapak açık) · DEN montajda assert edilebilir: den_assert()
Önceki: topping_uno_cad_v13.py. Çalıştır: python yap_topping_uno_cad_v14.py [çıkış_adı.py]
"""
import io, os, sys

U = os.path.dirname(os.path.abspath(__file__))
CIKIS = sys.argv[1] if len(sys.argv) > 1 else "topping_uno_cad_v14.py"
s = io.open(os.path.join(U, "topping_uno_cad_v13.py"), encoding="utf-8").read()
NL = "\n"


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:140])
    s = s.replace(a, b)


def bolum(bas, son, yeni):
    """bas … son (son dahil) arasını değiştir — ikisi de tek olmalı"""
    global s
    assert s.count(bas) == 1, ("bas", s.count(bas), bas[:100])
    i = s.index(bas); j = s.index(son, i)
    assert s.count(son) >= 1
    s = s[:i] + yeni + s[j + len(son):]


# ---------------------------------------------------------------- 0 · başlık
degis('"""TOPPING v2 (UNO\'lu) · 3B MODEL · topping_uno_cad_v13 · 27 Eyl 2026 gece (v12 + YAN YALITIM = ÜST YALITIM — Kemal: "ön yüzeyleri aynı planda, kalınlıkları üstle aynı")',
      '"""TOPPING v2 (UNO\'lu) · 3B MODEL · topping_uno_cad_v14 · 28 Eyl 2026 gece (v13 + ÖN DÜZLEM +79 · SOĞUK ODA KAPAKLI TEMİZ KUTU — SPEC_on_duzlem_v63 §2.3)' + NL +
      'v14: soğuk zarf ön yüzü −104 → +23 · yan duvar sandviç 1,5 + 57,5 + 1,0 (Z profille TC yan sacına) · raf L 40×40×3 köşebentte · 430 çerçeve +23…+24 ·' + NL +
      '    K1 / K2 soğuk kapak 40 sandviç +39…+79 + manyetik fitil +24…+39 + flipper · eski fitil silindi · havada parça bağlandı · hortumlar ayrıldı ·' + NL +
      '    açıcı hattı 2 × Ø6 · kaset çekme 0–630 · den_assert(). Önceki: topping_uno_cad_v13.py (yap_topping_uno_cad_v14.py)' + NL +
      'v13 (27 Eyl gece): (v12 + YAN YALITIM = ÜST YALITIM — Kemal: "ön yüzeyleri aynı planda, kalınlıkları üstle aynı")')

# ---------------------------------------------------------------- 1 · malzemeler (SPEC: sac / conta / plastik)
degis('    "hamur": ((0.93, 0.78, 0.52, 1.0), 0.0, 0.85, False),\n}',
      '    "hamur": ((0.93, 0.78, 0.52, 1.0), 0.0, 0.85, False),\n'
      '    "sac": ((0.74, 0.77, 0.80, 1.0), 0.85, 0.32, False), "conta": ((0.12, 0.12, 0.13, 1.0), 0.0, 0.7, False),   # v14 · SPEC ön yüz malzemeleri\n'
      '    "plastik": ((0.12, 0.12, 0.13, 1.0), 0.0, 0.6, False),\n}')

# ---------------------------------------------------------------- 2 · ön düzlem sabitleri
degis('Z_KAPAK = (-84.0, -104.0); Z_SOGUK = (-104.0, -565.0); Z_BOLME = (-565.0, -630.0); Z_KURU = (-630.0, -830.0)',
      'Z_ON = 79.0                                                                        # v14 · ÖN DÜZLEM (fırın ön yüzü) · montaj sözleşmesi Z_ON = FT.ZS = 79\n'
      'Z_ZARF = 23.0                                                                      # v14 · soğuk zarfın ön yüzü (v13 −104): önünde 430 çerçeve +23…+24 · fitil +24…+39 · kapak +39…+79\n'
      'Z_CER = (Z_ZARF, Z_ZARF + 1.0); Z_SKAPAK = (Z_ON - 40.0, Z_ON)                  # v14 · 430 ferritik çerçeve sacı 1,0 · soğuk kapak 40 = dış 1,5 + PU 37,5 + iç 1,0\n'
      'Z_KAPAK = (-84.0, Z_ZARF); Z_SOGUK = (Z_ZARF, -565.0); Z_BOLME = (-565.0, -630.0); Z_KURU = (-630.0, -830.0)   # v14: Z_KAPAK[1] = soğuk zarf ön yüzü (v13 −104)\n'
      'DX_DUNYA, DY_DUNYA = 700.0, -168.0                                                 # v14 · montaj: dünya x = x + 700 · dünya y = y − 168 (TU bir kez kaydırılır)\n'
      'def xu(x_dunya): return x_dunya - DX_DUNYA\n'
      'def yu(y_dunya): return y_dunya - DY_DUNYA')

# ---------------------------------------------------------------- 3 · yan duvarlar: sandviç 1,5 + 57,5 + 1,0 (SPEC soğuk gövde duvarı)
degis('ekle("kabin_sol_duvar_PU", kut(BAY_A[0] - 60.0, BAY_A[0], 1277.0, YUST - 1.5, Z_KAPAK[1], Z_BOLME[1]), "pu", "V", not_="v13: PU 60 · ön yüz −104 / arka −630 = üst yalıtımla aynı düzlem · v7: 1277\'den başlar (altı mekanizma bölgesi: tabla park/aktarmada duvar hizasını geçer; alt yanlar topping_cad\'in sacı)")\n'
      'ekle("kabin_sag_duvar_PU", kut(BAY_B[1], BAY_B[1] + 60.0, 1277.0, Y_TEK, Z_KAPAK[1], Z_BOLME[1]), "pu", "V", not_="v13: PU 60 · ön yüz −104 / arka −630 = üst yalıtımla aynı · v11: yalnız soğuk hacim yüksekliği 1277–1720 (üstü teknik cep, yalıtımsız)")',
      'DUVAR = (1.0, 57.5, 1.5)                                                                  # v14 · SPEC soğuk gövde duvarı: iç 304 1,0 + PU 57,5 (40 kg/m³) + dış 304 1,5 = 60\n'
      'for _yn, _xi0, _sg, _y1 in (("sol", BAY_A[0], -1.0, YUST - 1.5), ("sag", BAY_B[1], 1.0, Y_TEK)):\n'
      '    _a = _xi0; _b = _a + _sg * DUVAR[0]; _c = _b + _sg * DUVAR[1]; _d = _c + _sg * DUVAR[2]\n'
      '    ekle("soguk_duvar_%s_ic_sac" % _yn, kut(min(_a, _b), max(_a, _b), 1277.0, _y1, Z_KAPAK[1], Z_BOLME[1]), "paslanmaz", "V",\n'
      '         not_="v14 · AISI 304 1,0 · sandviç iç kabuğu (soğuk yüz) · raf köşebendi (L 40×40×3) buna M6 perçin somunla")\n'
      '    ekle("kabin_%s_duvar_PU" % _yn, kut(min(_b, _c), max(_b, _c), 1277.0, _y1, Z_KAPAK[1], Z_BOLME[1]), "pu", "V",\n'
      '         not_="v14 · PU 57,5 (sandviç çekirdeği) · ön yüz +23 / arka −630 = üst yalıtımla aynı düzlem · v7: 1277\'den başlar")\n'
      '    ekle("soguk_duvar_%s_dis_sac" % _yn, kut(min(_c, _d), max(_c, _d), 1277.0, _y1, Z_KAPAK[1], Z_BOLME[1]), "paslanmaz", "V",\n'
      '         not_="v14 · AISI 304 1,5 · sandviç dış kabuğu · 2 × Z profille TC yan sacına (28,5 boşluk) — soğuk paketin yük yolu")')
degis('YAN_T = YUST - 1.5 - TAVAN_A                                                              # v13: üst yalıtımın kalınlığı (60,5 ≈ 60) → yanlar da bu\n',
      'YAN_T = YUST - 1.5 - TAVAN_A                                                              # v13: üst yalıtımın kalınlığı (60,5 ≈ 60) → yanlar da bu (v14: sandviç 60)\n')

# ---------------------------------------------------------------- 4 · yalıtım: UNO kovanı + geçiş bloğu yuvası TAM ölçü (kovan / blok deliğe değer) + evaporatör hava ağızları
degis('_yal = _yal.cut(kut(89, 1201, 1439, 1471, Z_BOLME[1] - 1, Z_BOLME[0] + 1))                              # geçiş bloğu yuvası',
      '_yal = _yal.cut(kut(89, 1200, 1440, 1470, Z_BOLME[1] - 1, Z_BOLME[0] + 1))                              # geçiş bloğu yuvası (v14: blok ölçüsünde → blok yuvaya değer)')
degis('    _yal = _yal.cut(silz(_cx, V_EKSEN, 15.5, Z_BOLME[1] - 1, Z_BOLME[0] + 1))                         # UNO mil geçiş kovanı',
      '    _yal = _yal.cut(silz(_cx, V_EKSEN, 15.0, Z_BOLME[1] - 1, Z_BOLME[0] + 1))                         # UNO mil geçiş kovanı (v14: Ø30 = kovan → sıkı geçme)\n'
      'EVAP_AGIZ = ((720.0, 1080.0, 1570.0, 1610.0), (720.0, 1080.0, 1640.0, 1685.0))                   # v14 · dönüş (alt) + üfleme (üst): TC evaporatörü (dünya x 1400–1800 · y 1392–1572) arka bölmenin hemen arkasında\n'
      'for _x0, _x1, _y0, _y1 in EVAP_AGIZ:\n'
      '    _yal = _yal.cut(kut(_x0, _x1, _y0, _y1, Z_BOLME[1] - 1, Z_BOLME[0] + 1))')

# ---------------------------------------------------------------- 5 · UNO: hazne TC kelepçesi · D70 silindir uç bilezikleri · uzatma · spreader braketi · çıkış ferrulü (valf tarafı)
degis('    ekle("%s_tc_kelepce_hazne" % k, sily(cx, VZ, 45.5, 1410, 1428).cut(sily(cx, VZ, 32.5, 1409, 1429)), "paslanmaz", "Ö")',
      '    ekle("%s_tc_kelepce_hazne" % k, sily(cx, VZ, 45.5, 1410, 1428).cut(sily(cx, VZ, 31.75, 1409, 1429)), "paslanmaz", "Ö",\n'
      '         not_="v14 · 2,5\\" TC kelepçe · iç Ø63,5 = boyun (sıkınca temas; v13 0,75 mm boşlukla havadaydı)")')
degis('        ekle("%s__urun_silindiri_D70" % k, silz(cx, V_EKSEN, 38, VZ - 165, VZ - 49).cut(silz(cx, V_EKSEN, 35, VZ - 166, VZ - 48)), "saydam_celik", "B",\n'
      '             not_="Beldos Ø70 silindir seçeneği (100–275 ml) · doz %.0f ml > Ø52\'nin 151 ml\'si" % doz)',
      '        ekle("%s__urun_silindiri_D70" % k, silz(cx, V_EKSEN, 38, VZ - 172, VZ - 41).cut(silz(cx, V_EKSEN, 33, VZ - 173, VZ - 40)).cut(silz(cx, V_EKSEN, 35, VZ - 165, VZ - 49)), "saydam_celik", "B",\n'
      '             not_="Beldos Ø70 silindir seçeneği (100–275 ml) · doz %.0f ml > Ø52\'nin 151 ml\'si · v14: iki ucunda Ø66 iç omuz (7 + 8) → UNO kapağına ve bileziğine oturur" % doz)')
degis('        ekle("%s_agiz_uzatmasi" % k, sily(cx, ZT, 18, 1216.0, 1264.0).cut(sily(cx, ZT, 16.5, 1180, 1265)), "paslanmaz", "H",',
      '        ekle("%s_agiz_uzatmasi" % k, sily(cx, ZT, 18, 1216.0, 1263.5).cut(sily(cx, ZT, 16.5, 1180, 1265)), "paslanmaz", "H",')
degis('        ekle("%s_spreader_valf_braketi" % k, kut(vx, cx - 16.0, v0 + 20.0, v0 + 44.0, ZT - 2.0, ZT + 2.0), "paslanmaz", "F")',
      '        ekle("%s_spreader_valf_braketi" % k, kut(vx, cx - 18.5, v0 + 20.0, v0 + 44.0, ZT - 2.0, ZT + 2.0), "paslanmaz", "F")   # v14: UNO ağzına girmez (v13 cx − 16)')
degis('    ekle("%s_hazne_boynu" % k, sily(cx, VZ, 31.75, V_UST, 1452).cut(sily(cx, VZ, 30.25, V_UST - 1, 1453)), "paslanmaz", "Ö")',
      '    # v14 · UNO çıkış TC bağlantısının VALF TARAFI ferrulü + contası (beldos_cad_v1 modelinde boru ucu ile ağız ferrulü arasında 9,9 mm boşluk vardı → ağız havada)\n'
      '    _cb = [p["sh"] for p in P if p["ad"] == "%s__cikis_borusu" % k][0].BoundingBox(); _cf = [p["sh"] for p in P if p["ad"] == "%s__cikis_tc_ferrule" % k][0].BoundingBox()\n'
      '    ekle("%s__cikis_tc_ferrule_valf" % k, silz(cx, V_EKSEN, _cf.xlen / 2.0 + 0.35, _cb.zmax, _cf.zmin).cut(silz(cx, V_EKSEN, 16.5, _cb.zmax - 1.0, _cf.zmin + 1.0)), "paslanmaz", "B",\n'
      '         not_="v14 · 1,5\\" TC ferrule (valf tarafı, boruya kaynaklı) + EPDM conta · kelepçe bunu ve ağız ferrulünü sıkar (dış Ø = kelepçe iç Ø)")\n'
      '    ekle("%s_hazne_boynu" % k, sily(cx, VZ, 31.75, V_UST, 1452).cut(sily(cx, VZ, 30.25, V_UST - 1, 1453)), "paslanmaz", "Ö")')

degis('        ekle("%s_spreader_giris_kelepcesi" % k, sily(cx, ZT, 25.0, BICAK_UST, BICAK_UST + 12.0).cut(sily(cx, ZT, 18.2, BICAK_UST - 1, BICAK_UST + 13.0)), "paslanmaz", "F",',
      '        ekle("%s_spreader_giris_kelepcesi" % k, sily(cx, ZT, 25.0, BICAK_UST, BICAK_UST + 12.0).cut(sily(cx, ZT, 18.0, BICAK_UST - 1, BICAK_UST + 13.0)), "paslanmaz", "F",   # v14: kelepçe boruları sıkar (iç = dış Ø36)')
degis('        ekle("%s_spreader_dik_boru" % k, sily(cx, ZT, 18.0, yb + 40.0, BICAK_UST).cut(sily(cx, ZT, 16.5, yb + 39.0, BICAK_UST + 1)), "paslanmaz", "F")',
      '        ekle("%s_spreader_dik_boru" % k, sily(cx, ZT, 18.0, yb + 40.0, BICAK_UST + 1.5).cut(sily(cx, ZT, 16.5, yb + 39.0, BICAK_UST + 2.5)), "paslanmaz", "F")   # v14: ucu UNO ağzının ucuna (1263,5) oturur (v13: 1,5 boşluk, spreader havadaydı)')

# ---------------------------------------------------------------- 6 · kaset tahriki: yalıtım deliği = kovan · motor redüktöre oturur · redüktör ↔ kovan flanş burcu
degis('        YAL_BLOK[0] = YAL_BLOK[0].cut(silz(xc, yy, 30.5, Z_BOLME[1] - 1, Z_BOLME[0] + 1))            # v6: yalıtım bloğunda kovan deliği',
      '        YAL_BLOK[0] = YAL_BLOK[0].cut(silz(xc, yy, 30.0, Z_BOLME[1] - 1, Z_BOLME[0] + 1))            # v6: yalıtım bloğunda kovan deliği (v14: Ø60 = kovan, sıkı)')
degis('        g, kb = TC.nema23_koy(xc, yy, -670.0 - 79.0 - 2.0)',
      '        ekle("reduktor_flans_burcu_" + tag, silz(xc, yy, 28.0, -670.0, -648.0).cut(silz(xc, yy, 15.0, -671.0, -647.0)), "paslanmaz", "V",\n'
      '             not_="v14 · redüktör flanşı ↔ kovan ara burcu 304 Ø56/Ø30 × 22 · 4 × M5 · redüktör + motor kovana (kovan yalıtıma sıkı) asılır — v13\'te havadaydı")\n'
      '        g, kb = TC.nema23_koy(xc, yy, -670.0 - 79.0)                                               # v14: motor redüktörün giriş yüzüne oturur (v13: 2 mm boşluk)')

# ---------------------------------------------------------------- 7 · kaset yuvası mandal pimi sıkı geçme
degis('    ekle("yuva_%s_mandal_pimi" % k, silx(ST + 18.0, mz + 4.0, 1.5, px0 - 23.5, px0 - 5.5), "celik", "K", not_="Pim ISO 8734 3 m6 × 18 A1: iki yan duvara sıkı geçme, dil üstünde kayar (0,5 içeride)")',
      '    ekle("yuva_%s_mandal_pimi" % k, silx(ST + 18.0, mz + 4.0, 1.6, px0 - 23.5, px0 - 5.5), "celik", "K", not_="Pim ISO 8734 3 m6 × 18 A1: iki yan duvara sıkı geçme, dil üstünde kayar (0,5 içeride) · v14: modelde delik çapında (sıkı geçme = temas)")')

# ---------------------------------------------------------------- 8 · iniş boruları rafa kulakla
degis('ekle("raf_arka_bukumu", kut(90, W - 90, SOGUK_TABAN - RAF_T - RAF_BUKUM, SOGUK_TABAN - RAF_T, Z_BOLME[0], Z_BOLME[0] + RAF_T), "paslanmaz", "H")',
      'ekle("raf_arka_bukumu", kut(90, W - 90, SOGUK_TABAN - RAF_T - RAF_BUKUM, SOGUK_TABAN - RAF_T, Z_BOLME[0], Z_BOLME[0] + RAF_T), "paslanmaz", "H")\n'
      '# v14 · İNİŞ BORULARI RAFA ASILI: borunun iki yanında 3 mm kulak (boruya kaynak) + dik lama rafın altına M5 · kulaklar tüpün kayma izinin (±30) dışında (±35…38)\n'
      'for _ad, _mod, _x0, _x1 in KASET:\n'
      '    _x = (_x0 + _x1) / 2.0; _, ro, ri = KAS_R[_mod]\n'
      '    for _sg, _yn in ((-1.0, "sol"), (1.0, "sag")):\n'
      '        _k = kut(_x + _sg * ro, _x + _sg * 38.0, 1250.0, 1256.0, KAS_Z - 10.0, KAS_Z + 10.0).union(kut(_x + _sg * 35.0, _x + _sg * 38.0, 1256.0, SOGUK_TABAN - RAF_T, KAS_Z - 10.0, KAS_Z + 10.0))\n'
      '        ekle("%s_boru_kulagi_%s" % (_mod.split("_")[0], _yn), _k, "paslanmaz", "H",\n'
      '             not_="v14 · 304 lama 3 × 20 · boruya kaynak (yatay kol) + rafın altına 2 × M5 (dik kol 35–38) · iniş borusu + huni v13\'te havadaydı")')

# ---------------------------------------------------------------- 9 · eski fitil (−104) kalkar
bolum('# ön fitil: soğuk odanın L ağzının çevresi', 'çekmece fitiliyle aynı profil")',
      '# v14 · ESKİ ÖN FİTİL (z −104) KALKTI — fitil artık soğuk kapakların (K1 / K2) arkasında (+24…+39), bkz. bölüm 5b (ÖN YÜZ)\n'
      'FITIL_BOSLUK = (1325.0, 1455.0)                                                       # (tarihçe) v8: itici geçişi — v9 kesiksiz · v14: fitil kapakta')

# ---------------------------------------------------------------- 10 · hava tesisatı: ayrık hortum yolları · geçiş bloğu delikleri · açıcı hattı · kompresör vanası
degis('ana = [(3600, 1030, -380), (3600, 1040, -790), (1830, 1040, -790), (1830, 1100, -790), (1675, 1100, -790), (1675, 1250, -740)]',
      'ana = [(3600, 1001, -380), (3600, 1040, -790), (1830, 1040, -790), (1830, 1100, -790), (1675, 1100, -790), (1675, 1250, -740)]   # v14: başı motorun arkasındaki vanada (y 1001)')
bolum('ekle("hava_hatti_acici_D6", boru(', '(ex, 1455, -420), (ex, V_EKSEN + 22, -420)], 3.0), renk, "V")',
      '# v14 · AÇICI HATTI 2 × Ø6 (iki yönlü silindir): valf adasından sola → TC sol yan sacındaki 2 rakordan (dünya y 1472 / 1460, z −700 / −712) A\'ya → Z silindirinin\n'
      '#       (TC v25 acici_pnomatigi, Festo DSBC-32-100, dünya x 327,5–372,5 · y 1280–1474 · z −562,5…−517,5) +x yüzündeki portlara (arka port dünya y 1460, ön port 1292)\n'
      'for _j, (_yA, _zA, _xd, _yP, _renk) in enumerate(((1640.0, -700.0, 420.0, 1460.0, "hortum_mavi"), (1628.0, -712.0, 428.0, 1292.0, "hortum_siyah"))):\n'
      '    ekle("hava_hatti_acici_D6_%d" % (_j + 1), boru([(ADA[0], _yA, _zA), (xu(_xd), _yA, _zA), (xu(_xd), yu(_yP), _zA), (xu(_xd), yu(_yP), -540.0), (xu(372.5), yu(_yP), -540.0)], 3.0), _renk, "V",\n'
      '         not_="v14 · Ø6 PU · valf adası → TC sol yan sacı rakoru → açıcı Z silindiri (%s port) · v13\'te tek hat, A\'da boşta bitiyordu" % ("arka" if _j == 0 else "ön"))\n'
      '# v14 · UNO HORTUMLARI AYRIK YOLLARDA (v13\'te 4 UNO\'nun hortumları aynı çizgide üst üste biniyordu): piston hortumları y 1386 + 8·(2i + j), z −672 ·\n'
      '#       döner valf hortumları z −690 − 16·i − 8·j, y 1452 / 1460 (geçiş bloğunun içinden, ağ 8)\n'
      'HORTUM_GECIS = []\n'
      'for i, (ad, cx, *_r) in enumerate(UNO):\n'
      '    k = ad.lower(); tx = ADA[0] + 20 + i * 48.0\n'
      '    for j, (zp, renk) in enumerate(((-680.0, "hortum_mavi"), (-800.0, "hortum_siyah"))):\n'
      '        dx = j * 8.0; yh = 1386.0 + 8.0 * (2 * i + j)\n'
      '        ekle("%s_hortum_silindir_%d" % (k, j + 1), boru([(tx + dx, ADA[2], -672.0), (tx + dx, yh, -672.0), (cx + dx, yh, -672.0),\n'
      '                                                       (cx + dx, yh, zp), (cx + dx, V_EKSEN + 19, zp)], 3.0), renk, "V")\n'
      '    for j, renk in enumerate(("hortum_mavi", "hortum_siyah")):\n'
      '        dx = j * 8.0; ex = cx - 72 + dx; zi = -690.0 - 16.0 * i - 8.0 * j; yj = 1452.0 + 8.0 * j\n'
      '        ekle("%s_hortum_doner_valf_%d" % (k, j + 1), boru([(tx + 24 + dx, ADA[2], zi), (tx + 24 + dx, yj, zi), (ex, yj, zi),\n'
      '                                                          (ex, yj, -420), (ex, V_EKSEN + 22, -420)], 3.0), renk, "V")\n'
      '        HORTUM_GECIS.append("%s_hortum_doner_valf_%d" % (k, j + 1))\n'
      'HORTUM_GECIS += ["%s_spreader_hava_hortumu" % a_.lower() for a_ in ("SOS", "HARC")]\n'
      'for q in P:                                                                          # v14: geçiş bloğunda hortum delikleri (hortum çapında, keçeli)\n'
      '    if q["ad"] == "gecis_blogu_yalitim":\n'
      '        for p in P:\n'
      '            if p["ad"] in HORTUM_GECIS:\n'
      '                q["sh"] = q["sh"].cut(p["sh"])')
degis('ekle("kompresor_cikis_vanasi", sily(3600, -380, 8, KOMP[3], 1036), "siyah", "V")',
      'ekle("kompresor_cikis_vanasi", silz(3600, 1001.0, 8, -380.0, KOMP[5] + 60.0), "siyah", "V",\n'
      '     not_="v14 · motorun arka yüzüne bağlı çıkış vanası (z −380…−360) · ucu = montaj ana hattının başı (dünya 3790, 1809, −380) · v13\'te motorun 20 mm arkasında havadaydı")')

# ---------------------------------------------------------------- 11 · v14 ÖN YÜZ + YÜK YOLU (alt yalıtımdan sonra; denetimden önce)
ONYUZ = r'''
# ================================================================ 5b · v14 · YÜK YOLU + ÖN YÜZ (SPEC_on_duzlem_v63 §1 + §2.3)
# (a) RAF KÖŞEBENTLERİ L 40 × 40 × 3 (304): rafın iki ucu bunlara oturur; köşebent duvarın iç sacına M6, bükümlerin arasında (z −562…+20)
RAF_L = {}
for _yn, _x0, _sg in (("sol", BAY_A[0], 1.0), ("sag", BAY_B[1], -1.0)):
    _L = kut(_x0, _x0 + _sg * 40.0, SOGUK_TABAN - RAF_T - 3.0, SOGUK_TABAN - RAF_T, Z_BOLME[0] + RAF_T, Z_KAPAK[1] - RAF_T)
    _L = _L.union(kut(_x0, _x0 + _sg * 3.0, YAL_Y0, SOGUK_TABAN - RAF_T, Z_BOLME[0] + RAF_T, Z_KAPAK[1] - RAF_T))
    if _yn == "sol":                                                                    # sos spreader hava hortumu raftaki Ø10 delikten geçer → köşebentte de aynı delik
        _L = _L.cut(sily(UNO[0][1] - 100.0, ZT + 34.0, 5.0, SOGUK_TABAN - RAF_T - 4.0, SOGUK_TABAN - RAF_T + 1.0))
    RAF_L[_yn] = _L
    ekle("raf_kosebendi_%s" % _yn, _L, "paslanmaz", "H",
         not_="v14 · L 40 × 40 × 3 AISI 304 · rafın ucu yatay koluna oturur (M5 havşa) · dik kol duvarın iç sacına 4 × M6 · raf 154 kg → uç başına 0,76 kN")
for q in P:                                                                            # alt yalıtım köşebendi sarar (tam ölçü kesik)
    if q["ad"] in ("alt_yalitim_PU", "alt_yalitim_saci"):
        for _L in RAF_L.values():
            q["sh"] = q["sh"].cut(_L.val())
# (b) Z PROFİLLER 2 mm: duvarın dış sacı (x 30 / 1770) ↔ TC yan sacının iç yüzü (dünya 701,5 / 2498,5 = x 1,5 / 1798,5) · 28,5 boşluk · 2 kat
ZPROF = []
for _yn, _xa, _xb, _ys in (("sol", 1.5, BAY_A[0] - 60.0, (1290.0, 1900.0)), ("sag", W - 1.5, BAY_B[1] + 60.0, (1290.0, 1640.0))):
    _sg = 1.0 if _xb > _xa else -1.0
    for _i, _y0 in enumerate(_ys):
        _z = kut(_xa, _xa + _sg * 2.0, _y0, _y0 + 30.0, -600.0, -20.0)
        _z = _z.union(kut(_xa, _xb, _y0 + 28.0, _y0 + 30.0, -600.0, -20.0)).union(kut(_xb - _sg * 2.0, _xb, _y0 + 28.0, _y0 + 58.0, -600.0, -20.0))
        ekle("soguk_duvar_%s_z_profili_%d" % (_yn, _i), _z, "paslanmaz", "H",
             not_="v14 · Z profil 30 × 28,5 × 30 × 2 AISI 304 · boy 580 · TC yan sacına 4 × M6 (dıştan kör perçin somun) + duvarın dış sacına 4 × M6 · ısı köprüsü: PU arkasında, dış sacta")
        ZPROF.append("soguk_duvar_%s_z_profili_%d" % (_yn, _i))

# (c) ÖN YÜZ · 430 ÇERÇEVE SACI (+23…+24): soğuk zarfın bütün ön yüzünü örter, L ağız açık; kaset tüpü çentikleri (fitilin İÇİNDE → conta sürekli)
CER_DIS = [(1.5, YAL_Y0), (W - 1.5, YAL_Y0), (W - 1.5, Y_TEK), (X_TEK, Y_TEK), (X_TEK, YUST - 1.5), (1.5, YUST - 1.5)]
AGIZ_L = [(BAY_A[0], SOGUK_TABAN), (BAY_B[1], SOGUK_TABAN), (BAY_B[1], TAVAN_B), (BAY_A[1], TAVAN_B), (BAY_A[1], TAVAN_A), (BAY_A[0], TAVAN_A)]
CENTIK_Y0 = 1311.0                                                                     # kaset tüpünün altı 1312 (dünya 1144) − 1
_cer = cq.Workplane("XY", origin=(0, 0, Z_CER[0])).polyline(CER_DIS).close().extrude(1.0)
_cer = _cer.cut(cq.Workplane("XY", origin=(0, 0, Z_CER[0] - 1.0)).polyline(AGIZ_L).close().extrude(3.0))
CENTIK = []
for _ad, _mod, _x0, _x1 in KASET:
    _xc = (_x0 + _x1) / 2.0; _r = KAS_R[_mod][0] + 1.0
    CENTIK.append((_xc - _r, _xc + _r))
    _cer = _cer.cut(kut(_xc - _r, _xc + _r, CENTIK_Y0, SOGUK_TABAN + 1.0, Z_CER[0] - 1.0, Z_CER[1] + 1.0))
ekle("onyuz_soguk_cerceve_saci", _cer, "sac", "Ö",
     not_="v14 · 430 ferritik 1,0 (manyetik fitil tutar; 304 tutmaz) · BOM notu 430 · soğuk zarfın ön yüzüne yapıştırma + kenarda TC yan saclarına · kaset tüpü çentikleri 62 × 9 (fitilin içinde) · terleme: çevresinde ısıtıcı kablo (VARSAYIM 10 W/m)")

# (d) SOĞUK KAPAKLAR K1 (sol menteşe) + K2 (sağ menteşe) · 40 sandviç (dış 304 fırçalı 1,5 dört kenardan bükülü + PU 37,5 + iç 304 1,0) · fitil kanalı iç sacda
FITIL_G = 4.0
FITIL_PROF = [(-2.0, -31.7), (2.0, -31.7), (2.0, -33.0), (3.15, -34.0), (2.0, -35.2), (2.0, -40.0), (6.0, -40.0), (6.0, -42.0), (8.0, -42.0), (8.0, -50.0),
              (10.5, -50.0), (10.5, -55.0), (-10.5, -55.0), (-10.5, -50.0), (-8.0, -50.0), (-8.0, -42.0), (-6.0, -42.0), (-6.0, -40.0), (-2.0, -40.0),
              (-2.0, -35.2), (-3.15, -34.0), (-2.0, -33.0)]              # store_cad_v7 FITIL (z: kapak ön yüzü 0) → burada + Z_ON
KANAL_PROF = [(-3.2, -31.6), (3.2, -31.6), (3.2, -40.05), (-3.2, -40.05)]


def cevre_supur(ax0, ax1, ay0, ay1, prof):
    """store_cad_v7.cevre_supur · açıklık (ax0..ax1 × ay0..ay1) çevresinde FITIL_G dışarıdaki yol · z + Z_ON"""
    g = FITIL_G
    Pp = [((ax0 + ax1) / 2.0, ay0 - g), (ax1 + g, ay0 - g), (ax1 + g, ay1 + g), (ax0 - g, ay1 + g), (ax0 - g, ay0 - g)]
    yol = cq.Workplane("XY", origin=(0, 0, Z_ON - 40.0)).polyline(Pp).close()
    pts = [(ay0 - g - u, zz + Z_ON) for u, zz in prof]
    return cq.Workplane("YZ", origin=((ax0 + ax1) / 2.0, 0, 0)).polyline(pts).close().sweep(yol, transition="right")


# dünya ölçüleri (SPEC §2.3) → TU: x − 700 · y + 168
SKAPAK = {"K1": dict(x=(xu(701.5), xu(1518.5)), y=(yu(1110.5), yu(1859.0)), fitil=(BAY_A[0], xu(1500.0), yu(1136.0), TAVAN_A), mentese="sol"),
          "K2": dict(x=(xu(1521.5), xu(2497.0)), y=(yu(1110.5), yu(1550.5)), fitil=(xu(1537.5), BAY_B[1], yu(1136.0), TAVAN_B), mentese="sag")}
for _kn, _k in SKAPAK.items():
    (x0, x1), (y0, y1) = _k["x"], _k["y"]; z0, z1 = Z_SKAPAK; ac = _k["fitil"]
    _ds = kut(x0, x1, y0, y1, z0, z1).cut(kut(x0 + 1.5, x1 - 1.5, y0 + 1.5, y1 - 1.5, z0 - 1.0, z1 - 1.5))
    _pu = kut(x0 + 1.5, x1 - 1.5, y0 + 1.5, y1 - 1.5, z0 + 1.0, z1 - 1.5)
    _ic = kut(x0 + 1.5, x1 - 1.5, y0 + 1.5, y1 - 1.5, z0, z0 + 1.0)
    _kn_ = cevre_supur(*ac, KANAL_PROF)
    _pu, _ic = _pu.cut(_kn_), _ic.cut(_kn_)
    _kg = ((x1 - x0) * (y1 - y0) * 1.5 + 2 * (x1 - x0 + y1 - y0) * 38.5 * 1.5 + (x1 - x0 - 3) * (y1 - y0 - 3) * 1.0) * 7.93e-6 + (x1 - x0 - 3) * (y1 - y0 - 3) * 37.5 * 40e-9
    ekle("onyuz_%s_dis_sac" % _kn, _ds, "sac", "Ö",
         not_="v14 · soğuk kapak %s %.1f × %.1f × 40 · AISI 304 fırçalı 1,5 dört kenardan 40 bükülü (kulpsuz, bas-aç) · ≈%.1f kg · gizli menteşe %s" % (_kn, x1 - x0, y1 - y0, _kg, _k["mentese"]))
    ekle("onyuz_%s_pu" % _kn, _pu, "pu", "Ö", not_="v14 · PU 37,5 (40 kg/m³) · fitil kanalı")
    ekle("onyuz_%s_ic_sac" % _kn, _ic, "paslanmaz", "Ö", not_="v14 · AISI 304 1,0 · fitil geçme kanalı 6,4 × 8,4")
    ekle("onyuz_%s_fitil" % _kn, cevre_supur(*ac, FITIL_PROF), "conta", "K",
         not_="v14 · geçmeli manyetik fitil 21 × 18,5 (sıkışınca 15) · store_cad_v7 ile aynı profil · 430 çerçeveye / flipper'a basar · çevre %.0f mm" % (2 * (ac[1] - ac[0] + ac[3] - ac[2] + 4 * FITIL_G)))
# gizli menteşe (kapak arkası ↔ TC yan sacının ön dönüşü) + bas-aç mandal — ölçüler VARSAYIM (katalog föyü doğrulanacak)
for _ad, _x0, _x1, _y0 in (("K1_mentese_0", 31.5, 55.0, 1330.0), ("K1_mentese_1", 31.5, 55.0, 1900.0), ("K2_mentese_0", xu(2443.0), xu(2466.5), 1330.0), ("K2_mentese_1", xu(2443.0), xu(2466.5), 1620.0)):
    ekle("onyuz_" + _ad, kut(_x0, _x1, _y0, _y0 + 70.0, Z_CER[1], Z_SKAPAK[0]), "paslanmaz", "K",
         not_="v14 · gizli menteşe 3B ayarlı (Sugatsune HES3D sınıfı — parça no + ölçü VARSAYIM) · kapak ≈13 / 9 kg · ön dönüşe 2 × M5, kapağın iç sacına perçin somun")
for _ad, _x0, _x1, _y0, _y1 in (("K1_basac", 780.0, 810.0, 1990.0, 2020.0), ("K2_basac", 830.0, 870.0, 1705.5, 1717.5)):
    ekle("onyuz_" + _ad, kut(_x0, _x1, _y0, _y1, Z_CER[1], Z_SKAPAK[0]), "plastik", "K",
         not_="v14 · bas-aç mandal (push-to-open, gizli) · Southco E4 sınıfı — parça no + ölçü VARSAYIM · kapak kulpsuz")
# (e) FLIPPER (katlanır orta dikme, ısıtıcılı): K1'in serbest kenarına menteşeli; kapalıyken ön yüzü çerçeveyle aynı düzlemde (+24), K1 ve K2 fitilleri buna basar
FLIP = (xu(1493.0), xu(1547.0), SOGUK_TABAN + 0.5, TAVAN_B - 0.5)
ekle("onyuz_flipper_govde", kut(FLIP[0], FLIP[1], FLIP[2], FLIP[3], -16.0, Z_CER[1] - 1.5), "plastik", "V",
     not_="v14 · katlanır orta dikme (flipper) 54 × 369 × 38,5 · ABS gövde + PU + ısıtıcı kablo (ter önleme, VARSAYIM 10 W/m) · K1 ile birlikte açılır (kıyma haznesinin çekme yolu açık kalır)")
ekle("onyuz_flipper_on_sac", kut(FLIP[0], FLIP[1], FLIP[2], FLIP[3], Z_CER[1] - 1.5, Z_CER[1]), "sac", "V", not_="v14 · 430 ferritik 1,5 · manyetik fitil tutar · ön yüzü +24 (çerçeveyle aynı)")
for _i, _y0 in enumerate((1330.0, 1660.0)):
    ekle("onyuz_flipper_mentese_%d" % _i, kut(xu(1515.5), xu(1518.5), _y0, _y0 + 20.0, Z_CER[1], Z_SKAPAK[0]), "paslanmaz", "K",
         not_="v14 · flipper menteşesi (yay yüklü, 90°) · K1 iç sacına · parça no VARSAYIM")
'''
degis('# ================================================================ 5 · DENETİM', ONYUZ + '\n# ================================================================ 5 · DENETİM')

# ---------------------------------------------------------------- 12 · denetim güncellemeleri
degis('_ftb = bb("on_fitil"); _ftk = [p for p in P if p["ad"] == "on_fitil"][0]["sh"].intersect(kut(FITIL_BOSLUK[0] + 1.0, FITIL_BOSLUK[1] - 1.0, YAL_Y0 - FITIL_W, YAL_Y0, Z_KAPAK[1], Z_KAPAK[1] + FITIL_T).val()).Volume()\n'
      'kontrol("ön fitil alt şeridi %.0f–%.0f arasında KESİKSİZ (v9: itici düz) · hacim %.0f > 0" % (FITIL_BOSLUK[0], FITIL_BOSLUK[1], _ftk), _ftk > 1.0)\n',
      'kontrol("v14 · eski ön fitil (z −104) kalktı", not [p for p in P if p["ad"] == "on_fitil"])\n')
degis('''    kontrol("v13 · %s: kalınlık %.0f (üst %.1f) · ön yüz z %.0f = üst ön yüz %.0f · arka z %.0f = üst arka %.0f · iç yüz soğuk oda sınırında"
            % (p["ad"], b_.xlen, YAN_T, b_.zmax, _ust.zmax, b_.zmin, _ust.zmin),
            abs(b_.xlen - 60.0) < 0.01 and abs(b_.zmax - _ust.zmax) < 0.01 and abs(b_.zmin - _ust.zmin) < 0.01 and (abs(b_.xmax - BAY_A[0]) < 0.01 or abs(b_.xmin - BAY_B[1]) < 0.01))''',
      '''    _yn = "sol" if "sol" in p["ad"] else "sag"
    _bs = cq.Compound.makeCompound([q["sh"] for q in P if q["ad"] in ("soguk_duvar_%s_ic_sac" % _yn, p["ad"], "soguk_duvar_%s_dis_sac" % _yn)]).BoundingBox()
    kontrol("v14 · %s duvarı sandviç 1,0 + %.1f + 1,5 = %.1f (üst %.1f) · ön yüz z %.0f = üst ön yüz %.0f · arka z %.0f = üst arka %.0f · iç yüz soğuk oda sınırında"
            % (_yn, b_.xlen, _bs.xlen, YAN_T, _bs.zmax, _ust.zmax, _bs.zmin, _ust.zmin),
            abs(_bs.xlen - 60.0) < 0.01 and abs(b_.xlen - 57.5) < 0.01 and abs(_bs.zmax - _ust.zmax) < 0.01 and abs(_bs.zmin - _ust.zmin) < 0.01 and (abs(_bs.xmax - BAY_A[0]) < 0.01 or abs(_bs.xmin - BAY_B[1]) < 0.01))''')

DEN_EK = r'''
# ---------------------------------------------------------------- v14 · ön düzlem + yük yolu + havada kalanlar (TU tek başına ölçülebilenler; dünya denetimi topping_cad_v25'te)
from OCP.BRepExtrema import BRepExtrema_DistShapeShape as _DSS
def _mes(a, b):
    sa = [p for p in P if p["ad"] == a][0]["sh"]; sb = [p for p in P if p["ad"] == b][0]["sh"]
    d_ = _DSS(sa.wrapped, sb.wrapped); return d_.Value() if d_.IsDone() else 99.0
kontrol("v14 · soğuk zarf ön yüzü +%.0f: yalıtım bloğu %.1f · raf %.1f · teknik ayırma sacları %.1f / %.1f · yan duvarlar %.1f / %.1f"
        % (Z_ZARF, bb("yalitim_blogu").zmax, bb("tasiyici_raf_3mm").zmax, bb("teknik_ayirma_saci_yatay").zmax, bb("teknik_ayirma_saci_dikey").zmax, bb("soguk_duvar_sol_dis_sac").zmax, bb("soguk_duvar_sag_dis_sac").zmax),
        all(abs(bb(a_).zmax - Z_ZARF) < 0.01 for a_ in ("yalitim_blogu", "tasiyici_raf_3mm", "raf_on_bukumu", "teknik_ayirma_saci_yatay", "teknik_ayirma_saci_dikey", "kabin_sol_duvar_PU", "kabin_sag_duvar_PU", "soguk_duvar_sol_dis_sac", "soguk_duvar_sag_dis_sac", "soguk_duvar_sol_ic_sac", "soguk_duvar_sag_ic_sac")))
_cb_ = bb("onyuz_soguk_cerceve_saci")
kontrol("v14 · 430 çerçeve sacı z %.1f…%.1f (+23…+24) · dünya x %.1f–%.1f · y %.1f–%.1f" % (_cb_.zmin, _cb_.zmax, _cb_.xmin + DX_DUNYA, _cb_.xmax + DX_DUNYA, _cb_.ymin + DY_DUNYA, _cb_.ymax + DY_DUNYA),
        abs(_cb_.zmin - Z_CER[0]) < 0.01 and abs(_cb_.zmax - Z_CER[1]) < 0.01 and abs(_cb_.xmin + DX_DUNYA - 701.5) < 0.01 and abs(_cb_.xmax + DX_DUNYA - 2498.5) < 0.01)
for _kn, _k in SKAPAK.items():
    _b = bb("onyuz_%s_dis_sac" % _kn)
    kontrol("v14 · %s dünya x %.1f–%.1f · y %.1f–%.1f · z %.1f…%.1f (ön yüz +79, 40 sandviç)" % (_kn, _b.xmin + DX_DUNYA, _b.xmax + DX_DUNYA, _b.ymin + DY_DUNYA, _b.ymax + DY_DUNYA, _b.zmin, _b.zmax),
            abs(_b.zmax - Z_ON) < 0.01 and abs(_b.zmin - Z_SKAPAK[0]) < 0.01 and abs(_b.xmin - _k["x"][0]) < 0.01 and abs(_b.xmax - _k["x"][1]) < 0.01 and abs(_b.ymin - _k["y"][0]) < 0.01 and abs(_b.ymax - _k["y"][1]) < 0.01)
    _f = bb("onyuz_%s_fitil" % _kn)
    kontrol("v14 · %s fitili z %.1f…%.1f (bası yüzü +24 = çerçeve ön yüzü) · kapağın içinde (x %.1f–%.1f ⊂ %.1f–%.1f)" % (_kn, _f.zmin, _f.zmax, _f.xmin, _f.xmax, _k["x"][0], _k["x"][1]),
            abs(_f.zmin - Z_CER[1]) < 0.01 and _f.xmin >= _k["x"][0] + 1.0 and _f.xmax <= _k["x"][1] - 1.0 and _f.ymin >= _k["y"][0] + 1.0 and _f.ymax <= _k["y"][1] - 1.0)
    _fs = [p for p in P if p["ad"] == "onyuz_%s_fitil" % _kn][0]["sh"]
    _vc = sum(_fs.intersect(kut(c0, c1, CENTIK_Y0, SOGUK_TABAN, Z_CER[1], Z_SKAPAK[0]).val()).Volume() for c0, c1 in CENTIK)
    kontrol("v14 · %s fitili kaset çentiklerinin ALTINDA (çentik bölgesinde fitil hacmi %.1f = 0 → conta sürekli)" % (_kn, _vc), _vc < 0.01)
kontrol("v14 · derz K1 | K2 = %.1f (3)" % (SKAPAK["K2"]["x"][0] - SKAPAK["K1"]["x"][1]), abs(SKAPAK["K2"]["x"][0] - SKAPAK["K1"]["x"][1] - 3.0) < 0.01)
_fb = bb("onyuz_flipper_on_sac")
kontrol("v14 · flipper ön yüzü +%.1f = çerçeve ön yüzü · açıklıkta (y %.1f–%.1f ⊂ %.0f–%.0f) · K1 | K2 derzinin arkasında (dünya x %.0f–%.0f)" % (_fb.zmax, _fb.ymin, _fb.ymax, SOGUK_TABAN, TAVAN_B, _fb.xmin + DX_DUNYA, _fb.xmax + DX_DUNYA),
        abs(_fb.zmax - Z_CER[1]) < 0.01 and _fb.ymin > SOGUK_TABAN and _fb.ymax < TAVAN_B and _fb.xmin + DX_DUNYA < 1518.5 and _fb.xmax + DX_DUNYA > 1521.5)
for _a, _b_ in (("onyuz_K1_fitil", "onyuz_flipper_on_sac"), ("onyuz_K2_fitil", "onyuz_flipper_on_sac"), ("onyuz_K1_fitil", "onyuz_soguk_cerceve_saci"), ("onyuz_K2_fitil", "onyuz_soguk_cerceve_saci"),
                ("onyuz_K1_fitil", "onyuz_K1_ic_sac"), ("onyuz_K2_fitil", "onyuz_K2_ic_sac"), ("onyuz_flipper_mentese_0", "onyuz_K1_ic_sac"), ("onyuz_flipper_mentese_0", "onyuz_flipper_on_sac"),
                ("raf_kosebendi_sol", "tasiyici_raf_3mm"), ("raf_kosebendi_sag", "tasiyici_raf_3mm"), ("raf_kosebendi_sol", "soguk_duvar_sol_ic_sac"), ("raf_kosebendi_sag", "soguk_duvar_sag_ic_sac"),
                ("soguk_duvar_sol_z_profili_0", "soguk_duvar_sol_dis_sac"), ("soguk_duvar_sag_z_profili_0", "soguk_duvar_sag_dis_sac"),
                ("kasar_boru_kulagi_sag", "kasar_inis_borusu"), ("kasar_boru_kulagi_sag", "tasiyici_raf_3mm"), ("sucuk_boru_kulagi_sol", "sucuk_inis_borusu"), ("sucuk_boru_kulagi_sol", "tasiyici_raf_3mm"),
                ("reduktor_flans_burcu_kasar_cad_v14_helezon", "reduktor_kasar_cad_v14_helezon"), ("reduktor_flans_burcu_kasar_cad_v14_helezon", "kovan_kasar_cad_v14_helezon"),
                ("motor_kasar_cad_v14_helezon", "reduktor_kasar_cad_v14_helezon"), ("kovan_kasar_cad_v14_helezon", "yalitim_blogu"), ("kiyma_mil_gecis_kovani", "yalitim_blogu"),
                ("kiyma_tc_kelepce_hazne", "kiyma_hazne_boynu"), ("kiyma__urun_silindiri_D70", "kiyma__urun_silindiri_kapagi"), ("kiyma__cikis_tc_ferrule_valf", "kiyma__cikis_tc_kelepcesi"),
                ("kiyma__cikis_tc_ferrule_valf", "kiyma__cikis_borusu"), ("kiyma__cikis_tc_ferrule_valf", "kiyma__cikis_tc_ferrule"), ("kiyma_agiz_uzatmasi", "kiyma__agiz_90_derece"),
                ("yuva_kasar_mandal_pimi", "yuva_kasar_mandal_govdesi"), ("gecis_blogu_yalitim", "yalitim_blogu"), ("kompresor_cikis_vanasi", "kompresor_JUNAIR_OF302_15B_motor")):
    _d = _mes(_a, _b_)
    kontrol("v14 · temas %s ↔ %s: %.3f mm (≤ 0,05)" % (_a, _b_, _d), _d <= 0.05)
_hv = [p for p in P if "hortum" in p["ad"] and p["mal"].startswith("hortum")]
_hk = []
for _i, _p in enumerate(_hv):
    for _q in _hv[_i + 1:]:
        _A, _B = _p["sh"].BoundingBox(), _q["sh"].BoundingBox()
        if _A.xmax < _B.xmin or _B.xmax < _A.xmin or _A.ymax < _B.ymin or _B.ymax < _A.ymin or _A.zmax < _B.zmin or _B.zmax < _A.zmin: continue
        try: _v = _p["sh"].intersect(_q["sh"]).Volume()
        except Exception: _v = -1.0
        if _v > 1.0 or _v < 0: _hk.append((_p["ad"], _q["ad"], round(_v, 1)))
kontrol("v14 · hortumlar birbirine girmiyor (%d hortum · v13'te 60+ üst üste binme)" % len(_hv), not _hk, str(_hk[:4]))
_gb = [p for p in P if p["ad"] == "gecis_blogu_yalitim"][0]["sh"]
_gk_ = [p["ad"] for p in P if p["ad"] in HORTUM_GECIS and _gb.intersect(p["sh"]).Volume() > 1.0]
kontrol("v14 · geçiş bloğunda hortum delikleri (%d hortum geçer, iç içe 0)" % len(HORTUM_GECIS), not _gk_, str(_gk_))
_ac = [bb("hava_hatti_acici_D6_%d" % j_) for j_ in (1, 2)]
kontrol("v14 · açıcı hattı 2 × Ø6: uçları dünya x %.1f / %.1f = Z silindiri yüzü 372,5 (TC v25) · A tarafında" % (_ac[0].xmin + DX_DUNYA, _ac[1].xmin + DX_DUNYA),
        all(abs(b_.xmin + DX_DUNYA - 372.5) < 0.01 for b_ in _ac))
_vn = bb("kompresor_cikis_vanasi")
kontrol("v14 · kompresör vanası motorun arka yüzünde (z %.0f…%.0f) · montajdaki ucu dünya (%.0f, %.0f, %.0f) = ana hat başı (3790, 1809, −380)"
        % (_vn.zmin, _vn.zmax, 3600 + DX_DUNYA - 510.0, (_vn.ymin + _vn.ymax) / 2.0 + DY_DUNYA + 976.0, _vn.zmin),
        abs(_vn.zmax - (KOMP[5] + 60.0)) < 0.01 and abs((_vn.ymin + _vn.ymax) / 2.0 + DY_DUNYA + 976.0 - 1809.0) < 0.01 and abs(_vn.zmin + 380.0) < 0.01)


def den_assert():
    """v14 · montaj TU'yu yükleyince çağırır: modül seviyesindeki bütün denetimler geçmeli"""
    kal = [d for d in DEN if not d[1]]
    assert not kal, "topping_uno_cad_v14 denetimi KALDI: %s" % kal
    return len(DEN)
'''
degis('abs(_ay.ymax - (SOGUK_TABAN - RAF_T)) < 0.01 and abs(_as.ymin - YAL_Y0) < 0.01 and _ay.xmin == BAY_A[0] and _ay.xmax == BAY_B[1])',
      'abs(_ay.ymax - (SOGUK_TABAN - RAF_T)) < 0.01 and abs(_as.ymin - YAL_Y0) < 0.01 and abs(_ay.xmin - BAY_A[0] - 3.0) < 0.01 and abs(_ay.xmax - BAY_B[1] + 3.0) < 0.01)   # v14: iki uçta raf köşebendinin dik kolu (3)')
degis('\n# ================================================================ 6 · ANİMASYON + GLB', DEN_EK + '\n# ================================================================ 6 · ANİMASYON + GLB')

# ---------------------------------------------------------------- 13 · __main__: kaset çekme 0–630 (kapak açık) · çıktılar on_duzlem_v63/ (siteye yazılmaz)
degis('    # v6 · KASET ÇIKIŞ YOLU: kaset (mandal kalkık) 10 mm adımlarla öne çekilir; hiçbir sabit parçaya değmemeli',
      '    # v6 · KASET ÇIKIŞ YOLU: kaset (mandal kalkık) 10 mm adımlarla öne çekilir; hiçbir sabit parçaya değmemeli · v14: 0–630 (ön düzlem +79 geçilir), soğuk kapaklar + flipper AÇIK')
degis('        sabit = [p for p in P if not p["ad"].startswith((mod, "yuva_%s_mandal_dili" % k, "baglam", "kompresor", "hava_ana", "pide", "tabla_diski"))]',
      '        sabit = [p for p in P if not p["ad"].startswith((mod, "yuva_%s_mandal_dili" % k, "baglam", "kompresor", "hava_ana", "pide", "tabla_diski", "onyuz_K1_", "onyuz_K2_", "onyuz_flipper"))]')
degis('        for dz in range(10, 431, 10):', '        for dz in range(10, 631, 10):')
degis('        kontrol("%s kaseti öne çekilirken (0–430 mm) hiçbir parçaya değmiyor" % KOD, not bul, "%d bulgu %s" % (len(bul), bul[:6]))',
      '        kontrol("v14 · %s kaseti öne çekilirken (0–630 mm, kapak açık) hiçbir sabit parçaya değmiyor (430 çerçeve çentikli)" % KOD, not bul, "%d bulgu %s" % (len(bul), bul[:6]))')
degis('    glb_yaz(os.path.join(OUT, "topping_uno_v13.glb"))\n    with open(os.path.join(OUT, "topping_uno_v13.json"), "w", encoding="utf-8") as f:\n        json.dump(dict(surum="topping_uno_cad_v13 · %s"',
      '    _od = OUT if "--site" in sys.argv else os.path.join(U, "on_duzlem_v63")                  # v14: siteye yazılmaz (montaj ajanı yayınlar)\n'
      '    glb_yaz(os.path.join(_od, "topping_uno_v14.glb"))\n    with open(os.path.join(_od, "topping_uno_v14.json"), "w", encoding="utf-8") as f:\n        json.dump(dict(surum="topping_uno_cad_v14 · %s"')
degis('"generator": "AUTOKITCH topping_uno_cad_v11"', '"generator": "AUTOKITCH topping_uno_cad_v14"')
degis('    print("JSON yazıldı · %d denetim hepsi GEÇTİ" % len(DEN))',
      '    print("JSON yazıldı · %d denetim hepsi GEÇTİ" % len(DEN))\n    sys.stdout.flush(); os._exit(0)')

# ================================================================ 14 · v14 DÜZELTME TURU (28 Eyl 2026 sabah · on_duzlem_v63/denetim_C.md)
#   bulgu 1 KRİTİK (soğuk taban açıklığı) · 2 ORTA (kapak açılışı / flipper) · 3 ORTA (menteşe taşıyıcısı) · KÜÇÜK 4 (motor kablosu) · 11 (itici kirişi profili) · 13 (bkz. TC)
degis('    açıcı hattı 2 × Ø6 · kaset çekme 0–630 · den_assert(). Önceki: topping_uno_cad_v13.py (yap_topping_uno_cad_v14.py)\n',
      '    açıcı hattı 2 × Ø6 · kaset çekme 0–630 · den_assert(). Önceki: topping_uno_cad_v13.py (yap_topping_uno_cad_v14.py)\n'
      'v14 DÜZELTME (28 Eyl sabah · on_duzlem_v63/denetim_C.md): SOĞUK TABAN SIZDIRMAZ — kasetle çıkan YARIK DİLİ + arka yaka contası + UNO / hortum geçiş\n'
      '    contaları; alt PU yalnız üst 6 mm yarık (iniş borusu + huni altı dolu) · FLIPPER KATLANIR (eksen x 1493 · z +20, burulma yayı, raf üstünde kam oluklu\n'
      '    kılavuz; K2 kapalıyken K1 açılır) · K1 / K2 çok kollu gizli menteşe, sanal pivot ön dış köşe, TABAN TC yan sacına · motor kablo rakoru ·\n'
      '    itici kirişi için sağ duvar alt profili · kapak açılma taramaları + soğuk taban kaçak denetimi (den_assert)\n')
# 14.1 · kaset yalnız üst 6 mm'den öne çekilir
degis('KAS_Z = -150.0                                   # kaset çıkış borusu ekseni (tabla ekseninin 20 mm önü, v1 ile aynı)\n',
      'KAS_Z = -150.0                                   # kaset çıkış borusu ekseni (tabla ekseninin 20 mm önü, v1 ile aynı)\n'
      'KAS_YARIK_Y0 = 1311.0                            # v14b · kaset tüpünün altı 1312 − 1: kaset yalnız bu kotun ÜSTÜNDEN öne çekilir (ön büküm + alt PU yarığı yalnız 1311–1317)\n')
degis('    _rob = _rob.cut(kut(_xc - _r, _xc + _r, SOGUK_TABAN - RAF_T - RAF_BUKUM - 1, SOGUK_TABAN - RAF_T + 1, Z_KAPAK[1] - RAF_T - 1, Z_KAPAK[1] + 1))',
      '    _rob = _rob.cut(kut(_xc - _r, _xc + _r, KAS_YARIK_Y0, SOGUK_TABAN - RAF_T + 1, Z_KAPAK[1] - RAF_T - 1, Z_KAPAK[1] + 1))   # v14b: çentik yalnız üst 6 mm, altındaki 34 mm kiriş sürekli')
degis('"40 mm aşağı büküm (rafın kirişi) · v6: kaset yarıklarında 60 çentik")',
      '"40 mm aşağı büküm (rafın kirişi) · v6: kaset yarıklarında 60 çentik · v14b: çentik yalnız 1311–1317 (tüp + yarık dili geçer), altındaki 34 mm kiriş sürekli")')
# 14.2 · motor kablosu: dış rakor motor yüzüne oturur (STEP'te kablo gövdeden 0,707 mm açıktı → havada)
degis('        ekle("motor_kablosu_" + tag, kb, "koyu", "B")',
      '        _kbs, _gms = kb.val(), g.val(); _kbb, _gbb = _kbs.BoundingBox(), _gms.BoundingBox()                  # v14b · kablo rakoru (denetim_C bulgu 4)\n'
      '        _rak = sily((_kbb.xmin + _kbb.xmax) / 2.0, (_kbb.zmin + _kbb.zmax) / 2.0, 5.0, _gbb.ymin - 12.0, _gbb.ymin).val()\n'
      '        ekle("motor_kablosu_" + tag, _kbs.fuse(_rak), "koyu", "B",\n'
      '             not_="motor kablosu (katalog STEP ucu) · v14b: kablo rakoru Ø10 × 12 (PG7 sınıfı, VARSAYIM) motor gövdesinin yüzüne oturur — STEP\'te kablo gövdeden 0,707 mm açıktı")')
# 14.3 · SOĞUK TABAN SIZDIRMAZLIĞI + itici için sağ duvar alt profili (alt yalıtımdan ÖNCE: delik mantığı yarık dilini görür)
BLOK_E = r'''
# ================================================================ v14b · SOĞUK ODA TABANI SIZDIRMAZ (denetim_C bulgu 1 · KRİTİK)
# Raf dilimi (y 1317–1320) ürün kanalları dışında TAM kapalı olmalı. v14'te kaset U-yarıkları raf + ön büküm + alt PU + alt sac boyunca öne açıktı
# (2 × ≈9 800 mm² doğrudan hava yolu) + UNO ağız halkaları (4 × 360) + hortum delikleri (2 × 50) → soğuk hava mekanizma bandına (ürün yoluna) iniyordu.
#   · KASET YARIK DİLİ (POM-C, kasetin tüpüne yarıklı yaka ile sıkılı → KASETLE BİRLİKTE çıkar, unutulamaz): raf U-yarığını tüpün önünde doldurur,
#     alt PU'nun üst yarığında (1311–1317) tüpü sarar, 430 çerçeve çentiğini ön flanşıyla kapatır (fitil zaten çentiğin altından geçer)
#   · RAF KASET CONTASI (silikon dudak, SABİT): raf deliğinin arka yarısında tüp ↔ delik halkası
#   · RAF GEÇİŞ CONTALARI (silikon grommet): UNO ağızları Ø36 ↔ raf deliği Ø42 · spreader hortumları Ø6 ↔ Ø10
#   · alt PU: kaset yalnız ÜST 6 mm yarıktan öne çekilir; iniş borusu + huni SABİT → altları ve önleri dolu PU (delikleri öne açık DEĞİL)
def _kesit(sh, y=1318.5):
    """y düzlemindeki boru kesiti → (merkez x, merkez z, dış r, iç r) · iç r alandan"""
    k = sh.intersect(kut(-1.0e4, 1.0e4, y - 0.05, y + 0.05, -2000.0, 500.0).val()); b = k.BoundingBox(); a = k.Volume() / 0.1
    ro = (b.xlen + b.zlen) / 4.0
    return ((b.xmin + b.xmax) / 2.0, (b.zmin + b.zmax) / 2.0, ro, math.sqrt(max(0.0, ro * ro - a / math.pi)))
KANAL = []                                                                            # ürün kanalları (x, z, iç r, ad) — soğuk taban kaçak denetiminde muaf
for _ad, _mod, _x0, _x1 in KASET:
    _xc = (_x0 + _x1) / 2.0; _r = KAS_R[_mod][0]; _k = _mod.split("_")[0]
    _tup = [p["sh"] for p in P if p["ad"] == "%s__cikis_tupu" % _mod][0]
    _tx, _tz, _to, _ti = _kesit(_tup); KANAL.append((_tx, _tz, (_to + _ti) / 2.0, "%s tüpü" % _k))           # kanal = boru etinin ortasına kadar (et zaten dolu)
    _dolu = sily(_tx, _tz, (_to + _ti) / 2.0, KAS_YARIK_Y0 - 1.0, SOGUK_TABAN + 1.0)                          # tüp + içi (et ortası) → dil / conta tüpün DIŞ yüzünden başlar
    _dil = kut(_xc - _r, _xc + _r, KAS_YARIK_Y0 + 1.0, SOGUK_TABAN, KAS_Z, Z_ZARF)                              # raf U-yarığı + ön büküm çentiği + alt PU üst yarığı (tüpün önü)
    _dil = _dil.union(sily(_xc, KAS_Z, _r, KAS_YARIK_Y0 + 1.0, SOGUK_TABAN - RAF_T))                            # alt PU üst yarığında tüpü saran yaka (Ø60)
    _dil = _dil.union(kut(_xc - _r - 1.0, _xc + _r + 1.0, KAS_YARIK_Y0, SOGUK_TABAN, Z_CER[0], Z_CER[1]))      # ön flanş: 430 çerçeve çentiği (62 × 9) kapanır
    _dil = _dil.cut(_dolu).cut(_tup)
    ekle("%s_yarik_dili" % _mod, _dil, "pom", "V",
         not_="v14b · KASET YARIK DİLİ POM-C (gıda) · %.0f × %.0f × 8 + Ø60 yaka + 62 × 9 ön flanş · kasetin tüpüne yarıklı yaka ile 2 × M4 A2 (kelebek) → kasetle BİRLİKTE çıkar · "
              "raf U-yarığını + ön büküm / alt PU üst yarığını + 430 çerçeve çentiğini kapatır (denetim_C bulgu 1: v14'te ≈9 800 mm² doğrudan hava yolu)" % (2 * _r, Z_ZARF - KAS_Z))
    _yk = sily(_xc, KAS_Z, _r, SOGUK_TABAN - RAF_T, SOGUK_TABAN).intersect(kut(_xc - _r - 1.0, _xc + _r + 1.0, SOGUK_TABAN - RAF_T - 1.0, SOGUK_TABAN + 1.0, KAS_Z - _r - 1.0, KAS_Z))
    ekle("raf_kaset_contasi_%s" % _k, _yk.cut(_dolu).cut(_tup), "conta", "K",
         not_="v14b · gıda tipi silikon dudak conta (yarım halka: raf deliğinin arka yarısı Ø60 ↔ tüp Ø%.0f) · raf deliğine yapışık, SABİT · kaset çekilince tüp öne kayar, conta yerinde kalır" % (2 * _to))
for _ad, _cx, *_r in UNO:
    _k = _ad.lower(); _ag = [p["sh"] for p in P if p["ad"] == "%s__agiz_90_derece" % _k][0]
    _ax, _az, _ao, _ai = _kesit(_ag); KANAL.append((_ax, _az, (_ao + _ai) / 2.0, "%s ağzı" % _k))
    ekle("raf_gecis_contasi_%s" % _k, sily(_cx, ZT, 21.0, SOGUK_TABAN - RAF_T, SOGUK_TABAN).cut(sily(_ax, _az, (_ao + _ai) / 2.0, SOGUK_TABAN - RAF_T - 1.0, SOGUK_TABAN + 1.0)).cut(_ag), "conta", "K",
         not_="v14b · gıda tipi silikon geçiş contası (grommet) · raf deliği Ø42 ↔ UNO ağzı Ø%.0f · 3 mm halka kapanır (v14: açık, 360 mm²)" % (2 * _ao))
    if _ad in ("SOS", "HARC"):
        _h = [p["sh"] for p in P if p["ad"] == "%s_spreader_hava_hortumu" % _k][0]
        ekle("raf_gecis_contasi_%s_hortum" % _k, sily(_cx - 100.0, ZT + 34.0, 5.0, SOGUK_TABAN - RAF_T, SOGUK_TABAN).cut(_h), "conta", "K",
             not_="v14b · hortum geçiş lastiği Ø10 → Ø6 hortum (v14: 50 mm² açık)")
# v14b · SAĞ DUVAR ALT PROFİLİ (denetim_C bulgu 11): aktarma iticisinin montaj kirişi (itici_cad_v5, dünya y 1103–1109) sağ ucuyla buna bağlanır — v14'te kiriş yalnız 1 mm alt sac + PU'ya değiyordu
ekle("soguk_duvar_sag_alt_profili", kut(BAY_B[1] + 60.0, W - 1.5, YAL_Y0, 1290.0, -245.0, -180.0), "paslanmaz", "H",
     not_="v14b · lama 28,5 × 13 × 65 AISI 304 · soğuk duvarın dış sacı ↔ TC sağ yan sacı arası (Z profilin altına kaynak + TC yan sacına 2 × M6) · itici montaj kirişi (dünya x 2044,5–2489,5) sağ ucu buna 2 × M6 · yük: kiriş → profil → TC yan sacı")


def soguk_taban_kacagi(parcalar, dx=0.0, dy=0.0):
    """v14b · soğuk oda tabanı (raf dilimi y 1317,5–1319,5 TU; dünyada + dy) ürün kanalları DIŞINDA açık alan (mm²) · parcalar: [(ad, şekil)] · (alan, [(alan, kutu)])"""
    R = kut(BAY_A[0] + dx, BAY_B[1] + dx, SOGUK_TABAN - RAF_T + 0.5 + dy, SOGUK_TABAN - 0.5 + dy, Z_BOLME[0], Z_ZARF).val(); rb = R.BoundingBox()
    for _a, sh in parcalar:
        b = sh.BoundingBox()
        if b.xmax < rb.xmin or b.xmin > rb.xmax or b.ymax < rb.ymin or b.ymin > rb.ymax or b.zmax < rb.zmin or b.zmin > rb.zmax: continue
        try: R = R.cut(sh)
        except ValueError: return 0.0, []                                          # kesim sonucu BOŞ (OCC boş şekil) → açık alan 0
    for x_, z_, r_, _n in KANAL:
        try: R = R.cut(sily(x_ + dx, z_, r_, rb.ymin - 1.0, rb.ymax + 1.0).val())
        except ValueError: return 0.0, []
    kal = [(s.Volume() / (rb.ymax - rb.ymin), s.BoundingBox()) for s in R.Solids() if s.Volume() > 1e-6]
    return sum(a for a, _b in kal), kal


def cerceve_bandi_acik(parcalar, dx=0.0, dy=0.0):
    """v14b · 430 çerçeve düzlemi (z 23,25–23,75) soğuk oda ALTINDAKİ bantta (y 1277–1320 TU) açık alan (mm²) — kaset çentikleri yarık dili flanşıyla kapalı olmalı"""
    R = kut(1.5 + dx, W - 1.5 + dx, YAL_Y0 + dy, SOGUK_TABAN + dy, Z_CER[0] + 0.25, Z_CER[1] - 0.25).val(); rb = R.BoundingBox()
    for _a, sh in parcalar:
        b = sh.BoundingBox()
        if b.xmax < rb.xmin or b.xmin > rb.xmax or b.ymax < rb.ymin or b.ymin > rb.ymax or b.zmax < rb.zmin or b.zmin > rb.zmax: continue
        try: R = R.cut(sh)
        except ValueError: return 0.0, []
    kal = [(s.Volume() / 0.5, s.BoundingBox()) for s in R.Solids() if s.Volume() > 1e-6]
    return sum(a for a, _b in kal), kal
'''
degis('# ================================================================ v12 · SOĞUK ODANIN ALTI: sac kaplı PU (Kemal: "altına da az da olsa yalıtım yap")',
      BLOK_E + '\n# ================================================================ v12 · SOĞUK ODANIN ALTI: sac kaplı PU (Kemal: "altına da az da olsa yalıtım yap")')
# 14.4 · alt yalıtım delikleri: kaset parçaları (tüp + dil) yalnız ÜST YARIK (öne açık), iniş borusu / huni / diğerleri kapalı delik · hortum deliği gerçek kesişimden
bolum('_ab = _alt.val().BoundingBox()\n', '    _alt = _alt.cut(kut(x0_, x1_, ALT_YAL[2] - 1.0, ALT_YAL[3] + 1.0, z0_, z1_))',
      r'''_ab = _alt.val().BoundingBox()
ALT_YARIK = []                                                                                # v14b · kaset ÜST yarıkları (y 1311–1317, öne açık)
for p in P:
    if p["ad"].startswith(("tasiyici_raf", "raf_", "yalitim_blogu", "kabin_", "baglam", "kompresor", "hava_ana", "teknik_bant", "pide", "tabla_diski")):
        continue
    if any(p["ad"].startswith(m_) for _a, m_, _x0, _x1 in KASET):
        continue                                                                              # v14b: öne çekilen kaset parçaları (tüp + yarık dili) → yalnız üst yarık (aşağıda)
    b_ = p["sh"].BoundingBox()
    if not (b_.xmin < _ab.xmax and _ab.xmin < b_.xmax and b_.ymin < _ab.ymax and _ab.ymin < b_.ymax and b_.zmin < _ab.zmax and _ab.zmin < b_.zmax):
        continue
    try:
        _k = _alt.val().intersect(p["sh"]); v_ = abs(_k.Volume()); lb = _k.BoundingBox() if v_ > 0.5 else None
    except Exception:
        v_, lb = 1.0, None
    if v_ <= 0.5 and not p["ad"].endswith("hava_hortumu"):
        continue
    x0_, x1_, z0_, z1_ = b_.xmin, b_.xmax, b_.zmin, b_.zmax
    if lb is not None and lb.xlen > 0.1:
        x0_, x1_, z0_, z1_ = lb.xmin, lb.xmax, lb.zmin, lb.zmax                                # delik yalnız yalıtımın İÇİNDEKİ kısım kadar
    else:                                                                                     # v14b: boru bileşiği (hortum) → katı katı kesişim (v14: tüm hortum kutusu, 72 × 473 delik)
        try:
            _lk = [q_.BoundingBox() for q_ in (s_.intersect(_alt.val()) for s_ in p["sh"].Solids()) if q_.Volume() > 0.01]
            if _lk:
                x0_, x1_, z0_, z1_ = min(q.xmin for q in _lk), max(q.xmax for q in _lk), min(q.zmin for q in _lk), max(q.zmax for q in _lk)
        except Exception:
            pass
    ALT_DELIK.append((p["ad"], x0_ - ALT_PAY, x1_ + ALT_PAY, z0_ - ALT_PAY, z1_ + ALT_PAY))   # v14b: iniş borusu / huni dahil HİÇBİRİ öne açık değil
for _ad, _mod, _x0, _x1 in KASET:
    _xc = (_x0 + _x1) / 2.0; _r = KAS_R[_mod][0]
    ALT_YARIK.append((_mod, _xc - _r, _xc + _r, KAS_Z - _r - ALT_PAY, ALT_YAL[5] + 1.0))
for _ad, x0_, x1_, z0_, z1_ in ALT_DELIK:
    _alt = _alt.cut(kut(x0_, x1_, ALT_YAL[2] - 1.0, ALT_YAL[3] + 1.0, z0_, z1_))
for _ad, x0_, x1_, z0_, z1_ in ALT_YARIK:
    _alt = _alt.cut(kut(x0_, x1_, KAS_YARIK_Y0, ALT_YAL[3] + 1.0, z0_, z1_))''')
degis('"v12 · PU 39 (40 kg/m³) · rafın altı, bükümlerin arası · kaset / UNO / hava geçişlerinde 3 mm boşluklu delik (kaset yarıkları öne açık)")',
      '"v12 · PU 39 (40 kg/m³) · rafın altı, bükümlerin arası · kaset / UNO / hava geçişlerinde 3 mm boşluklu delik · v14b: kaset yalnız ÜST 6 mm yarık (öne açık, yarık diliyle dolu), iniş borusu + huni altı / önü dolu")')
degis('_ya = sum((x1_ - x0_) * (z1_ - z0_) for _a, x0_, x1_, z0_, z1_ in ALT_DELIK) / ((BAY_B[1] - BAY_A[0]) * (ALT_YAL[5] - ALT_YAL[4]))',
      'for _ad, x0_, x1_, z0_, z1_ in ALT_YARIK:\n'
      '    print("     alt yalıtım ÜST YARIĞI (v14b, y %.0f–%.0f, öne açık, yarık diliyle dolu): %-16s x %.0f–%.0f · z %.0f…%.0f" % (KAS_YARIK_Y0, ALT_YAL[3], _ad, x0_, x1_, z0_, z1_))\n'
      '_ya = (sum((x1_ - x0_) * (z1_ - z0_) for _a, x0_, x1_, z0_, z1_ in ALT_DELIK) + sum((x1_ - x0_) * (z1_ - z0_) * (ALT_YAL[3] - KAS_YARIK_Y0) / (ALT_YAL[3] - ALT_YAL[2])\n'
      '       for _a, x0_, x1_, z0_, z1_ in ALT_YARIK)) / ((BAY_B[1] - BAY_A[0]) * (ALT_YAL[5] - ALT_YAL[4]))')
# 14.5 · K1 / K2 menteşeleri (taban + kol, sanal pivot ön dış köşe) · bas-aç gövde tarafı · FLIPPER katlanır (eksen + kılavuz oluğu + yay)
bolum('# gizli menteşe (kapak arkası ↔ TC yan sacının ön dönüşü) + bas-aç mandal — ölçüler VARSAYIM (katalog föyü doğrulanacak)\n',
      '         not_="v14 · flipper menteşesi (yay yüklü, 90°) · K1 iç sacına · parça no VARSAYIM")',
      r'''# v14b · SOĞUK KAPAK MENTEŞELERİ (denetim_C bulgu 2 + 3): ÇOK KOLLU gizli menteşe, SANAL dönme merkezi kapağın ÖN DIŞ KÖŞESİ (K1 x 701,5 · K2 x 2497, z +79) —
#       kapak dönerken kendi dış kenarının ötesine (A / F derzine) geçmez · KOL (kapak tarafı) kapağın iç sacına, TABAN (gövde tarafı) TC yan sacının iç yüzüne
#       + ön dönüşünün arkasına (v14: menteşe yalnız 1 mm 430 çerçeveye yapışıktı, yan saca bağlanamıyordu)
K1_PIVOT = (xu(701.5), Z_ON); K2_PIVOT = (xu(2497.0), Z_ON)
for _ad, _x0, _x1, _y0, _tx in (("K1_mentese_0", 31.5, 55.0, 1330.0, (1.5, 31.5)), ("K1_mentese_1", 31.5, 55.0, 1900.0, (1.5, 31.5)),
                               ("K2_mentese_0", xu(2443.0), xu(2468.5), 1330.0, (xu(2468.5), xu(2498.5))), ("K2_mentese_1", xu(2443.0), xu(2468.5), 1620.0, (xu(2468.5), xu(2498.5)))):
    ekle("onyuz_" + _ad, kut(_x0, _x1, _y0, _y0 + 70.0, Z_CER[1], Z_SKAPAK[0]), "paslanmaz", "K",
         not_="v14b · çok kollu gizli menteşe KOLU (kapak tarafı · 3B ayarlı, Sugatsune HES3D sınıfı — parça no + ölçü + sanal pivot VARSAYIM, föy doğrulanacak) · kapağın iç sacına perçin somun · kapak %s"
              % ("≈14,4 kg" if _ad.startswith("K1") else "≈10,4 kg"))
    ekle("onyuz_mentese_tabani_" + _ad, kut(_tx[0], _tx[1], _y0, _y0 + 70.0, Z_CER[1], Z_SKAPAK[0] - 1.5), "paslanmaz", "K",
         not_="v14b · menteşe TABANI AISI 304 blok 30 × 13,5 × 70 · TC yan sacının iç yüzüne 2 × M6 + ön dönüşün (+37,5…+39) arkasına dayalı · kol buna 2 × M5 (denetim_C bulgu 3)")
for _ad, _x0, _x1, _y0, _y1 in (("basac_K1", 780.0, 810.0, 1990.0, 2020.0), ("basac_K2", 830.0, 870.0, 1705.5, 1717.5)):
    ekle("onyuz_" + _ad, kut(_x0, _x1, _y0, _y1, Z_CER[1], Z_SKAPAK[0]), "plastik", "K",
         not_="v14 · bas-aç mandal (push-to-open, gizli) · Southco E4 sınıfı — parça no + ölçü VARSAYIM · kapak kulpsuz · v14b: gövde tarafı (çerçevede), ad onyuz_basac_K*")
# (e) FLIPPER v14b (denetim_C bulgu 2) — katlanır orta dikme, ısıtıcılı, K1'in iç yüzünde MENTEŞELİ:
#     katlanma ekseni FLIP_EKSEN (dünya x 1493 · z +20, dikey; menteşe braketi K1 fitilinin solunda) · BURULMA YAYI flipper'ı KATLAR (sağ ucu geriye, −90°) ·
#     raf üstündeki KILAVUZ BLOĞUNUN kam oluğu flipper'ın altındaki pimi yönlendirir: katlanma = min(90°, FLIP_K · α) (α = K1 açısı) → sağ ucu K2'nin
#     arkasından K1 dönmeden çekilir (K2 KAPALIYKEN K1 açılır) · K1 kapanırken pim oluğa ön yüzden −90°'de girer, oluk flipper'ı DÜZLER · K2 tek başına
#     açılırken pim oluğun kapalı ucunda tutulur (flipper düz kalır)
FLIP_EKSEN = (xu(1493.0), 20.0); FLIP_K = 30.0
KILAVUZ = (xu(1440.0), xu(1547.0), SOGUK_TABAN, SOGUK_TABAN + 15.0, -40.0, Z_CER[1])
FLIP = (xu(1493.0), xu(1547.0), KILAVUZ[3] + 0.5, TAVAN_B - 0.5)
FLIP_PIM = (xu(1541.0), -10.0, 4.0, KILAVUZ[3] - 9.5)                                  # pim merkezi x, z · r · alt ucu y (oluk 10 derin)


def kapak_don(sh, kn, aci, dx=0.0):
    """v14b · soğuk kapak (K1 sol / K2 sağ menteşe) açık konumu: sanal dönme merkezi ön dış köşe, dikey eksen · aci derece (0 = kapalı)"""
    px, pz = K1_PIVOT if kn == "K1" else K2_PIVOT
    return sh.rotate(V(px + dx, 0.0, pz), V(px + dx, 1.0, pz), -aci if kn == "K1" else aci)


def flipper_aci(aci):
    return min(90.0, FLIP_K * aci)


def flipper_don(sh, aci, dx=0.0):
    """v14b · flipper: önce katlanır (FLIP_EKSEN etrafında flipper_aci(α)°, sağ ucu geriye) sonra K1 ile döner"""
    fx, fz = FLIP_EKSEN
    return kapak_don(sh.rotate(V(fx + dx, 0.0, fz), V(fx + dx, 1.0, fz), flipper_aci(aci)), "K1", aci, dx)


def _pim_yolu(adim=0.6):
    """pim merkezinin (x, z, α) yolu: α 0 → pim kılavuzun ön yüzünden tamamen çıkana dek · noktalar arası ≤ adim mm"""
    pim = cq.Vertex.makeVertex(FLIP_PIM[0], 0.0, FLIP_PIM[1]); yol = []; a = 0.0; son = None
    while a <= 12.0:
        v = flipper_don(pim, a).toTuple()
        if son is None or math.hypot(v[0] - son[0], v[2] - son[2]) >= adim:
            yol.append((v[0], v[2], a)); son = v
        if v[2] - FLIP_PIM[2] > KILAVUZ[5] + 0.5:
            yol.append((v[0], v[2], a)); break
        a += 0.005
    return yol


PIM_YOLU = _pim_yolu()
_ol = [sily(x_, z_, FLIP_PIM[2], FLIP_PIM[3] - 0.5, KILAVUZ[3] + 1.0).val() for x_, z_, _a in PIM_YOLU]
while len(_ol) > 1:
    _ol = [_ol[i].fuse(_ol[i + 1]) if i + 1 < len(_ol) else _ol[i] for i in range(0, len(_ol), 2)]
ekle("onyuz_kilavuz_flipper", kut(*KILAVUZ).cut(_ol[0]), "pom", "V",
     not_="v14b · flipper KILAVUZ BLOĞU POM-C 107 × 15 × 64 · rafa 2 × M5 havşa · üstünde kam OLUĞU (pim Ø8 yolu, 10 derin, %d nokta, α 0–%.2f°) · ön yüzü +24 → K1 / K2 fitilleri 1152–1167 bandında buna basar · "
          "oluk ön yüzden K1 fitil halkasının İÇİNDE (dünya x ≈ %.0f) çıkar" % (len(PIM_YOLU), PIM_YOLU[-1][2], PIM_YOLU[-1][0] + DX_DUNYA))
_fp = sily(FLIP_EKSEN[0], FLIP_EKSEN[1], 3.0, FLIP[2] - 1.0, FLIP[3] + 1.0)                   # menteşe pimi deliği (katlanma ekseni)
ekle("onyuz_flipper_govde", kut(FLIP[0], FLIP[1], FLIP[2], FLIP[3], -16.0, Z_CER[1] - 1.5).cut(_fp), "plastik", "V",
     not_="v14b · katlanır orta dikme (flipper) 54 × %.0f × 38,5 · ABS gövde + PU + ısıtıcı kablo (ter önleme, VARSAYIM 10 W/m) · katlanma ekseni dünya x 1493 · z +20 · K1 %.0f° açılınca tam katlanır (−90°) · kıyma haznesinin çekme yolu açık kalır"
          % (FLIP[3] - FLIP[2], 90.0 / FLIP_K))
ekle("onyuz_flipper_on_sac", kut(FLIP[0], FLIP[1], FLIP[2], FLIP[3], Z_CER[1] - 1.5, Z_CER[1]).cut(_fp), "sac", "V", not_="v14 · 430 ferritik 1,5 · manyetik fitil tutar · ön yüzü +24 (çerçeveyle aynı)")
ekle("onyuz_flipper_pimi", sily(FLIP_PIM[0], FLIP_PIM[1], FLIP_PIM[2], FLIP_PIM[3], FLIP[2]), "celik", "K",
     not_="v14b · kam pimi Ø8 × 10 AISI 316 (flipper altına vidalı) · kılavuz oluğunda kayar")
for _i, _y0 in enumerate((1360.0, 1640.0)):
    ekle("onyuz_K1_flipper_mentese_%d" % _i, kut(xu(1481.0), FLIP_EKSEN[0], _y0, _y0 + 20.0, FLIP_EKSEN[1] + 1.0, Z_SKAPAK[0]).union(sily(FLIP_EKSEN[0], FLIP_EKSEN[1], 3.0, _y0 - 5.0, _y0 + 25.0)), "paslanmaz", "K",
         not_="v14b · flipper menteşesi (K1 ile döner): K1 iç sacına braket 12 × 20 × 18 + pim Ø6 (katlanma ekseni) + BURULMA YAYI (katlar, −90° dayamalı — parça no VARSAYIM) · braket K1 fitilinin solunda (dünya x ≤ 1493)")''')
# 14.6 · denetim: temaslar + yeni denetimler
degis('("onyuz_flipper_mentese_0", "onyuz_K1_ic_sac"), ("onyuz_flipper_mentese_0", "onyuz_flipper_on_sac"),',
      '("onyuz_K1_flipper_mentese_0", "onyuz_K1_ic_sac"), ("onyuz_K1_flipper_mentese_0", "onyuz_flipper_govde"), ("onyuz_flipper_pimi", "onyuz_flipper_govde"), ("onyuz_flipper_pimi", "onyuz_kilavuz_flipper"),\n'
      '                ("onyuz_kilavuz_flipper", "tasiyici_raf_3mm"), ("onyuz_K1_mentese_0", "onyuz_K1_ic_sac"), ("onyuz_K1_mentese_0", "onyuz_mentese_tabani_K1_mentese_0"),\n'
      '                ("onyuz_K2_mentese_1", "onyuz_K2_ic_sac"), ("onyuz_K2_mentese_1", "onyuz_mentese_tabani_K2_mentese_1"), ("kasar_cad_v14_yarik_dili", "kasar_cad_v14__cikis_tupu"),\n'
      '                ("sucuk_cad_v7_yarik_dili", "sucuk_cad_v7__cikis_tupu"), ("raf_kaset_contasi_kasar", "tasiyici_raf_3mm"), ("raf_kaset_contasi_sucuk", "sucuk_cad_v7__cikis_tupu"),\n'
      '                ("raf_gecis_contasi_kiyma", "kiyma__agiz_90_derece"), ("raf_gecis_contasi_sos", "tasiyici_raf_3mm"), ("raf_gecis_contasi_harc_hortum", "harc_spreader_hava_hortumu"),\n'
      '                ("motor_kablosu_sucuk_cad_v7_rotor", "motor_sucuk_cad_v7_rotor"), ("soguk_duvar_sag_alt_profili", "soguk_duvar_sag_dis_sac"), ("soguk_duvar_sag_alt_profili", "soguk_duvar_sag_z_profili_0"),')
DEN_B = r'''
# ---------------------------------------------------------------- v14b · denetim_C düzeltmeleri (TU tek başına; dünya karşılıkları topping_cad_v25.dunya_denetimi)
_TUP = [(p["ad"], p["sh"]) for p in P]
_ak, _akl = soguk_taban_kacagi(_TUP)
kontrol("v14b · SOĞUK ODA TABANI (raf dilimi y 1317,5–1319,5): %d ürün kanalı dışında AÇIK alan %.2f mm² ≤ 1 (v14: ≈ 21 350 — kaset U-yarıkları 2 × ≈9 900 + UNO ağız halkaları 4 × 360 + hortum delikleri 2 × 50)"
        % (len(KANAL), _ak), _ak <= 1.0, str([(round(a_, 2), round(b_.xmin), round(b_.zmin)) for a_, b_ in _akl if a_ > 0.01][:6]))
_ab2, _abl = cerceve_bandi_acik(_TUP)
kontrol("v14b · 430 çerçeve düzlemi soğuk oda altı bandında (y 1277–1320) kesintisiz: kaset çentikleri yarık dili flanşıyla kapalı · açık alan %.2f mm² ≤ 1" % _ab2, _ab2 <= 1.0,
        str([(round(a_, 2), round(b_.xmin), round(b_.ymin)) for a_, b_ in _abl if a_ > 0.01][:6]))
for _ad, _mod, _x0, _x1 in KASET:
    _db = bb("%s_yarik_dili" % _mod); _k = _mod.split("_")[0]
    kontrol("v14b · %s yarık dili: x %.0f–%.0f · y %.0f–%.0f (raf üstü = raf üstü %.0f) · z %.0f…%.0f (ön flanş çerçeve düzleminde)" % (_k, _db.xmin, _db.xmax, _db.ymin, _db.ymax, SOGUK_TABAN, _db.zmin, _db.zmax),
            abs(_db.ymax - SOGUK_TABAN) < 0.01 and abs(_db.zmax - Z_CER[1]) < 0.01 and abs(_db.ymin - KAS_YARIK_Y0) < 0.01)
ACI_TARAMA = (0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 7.5, 10.0, 20.0, 45.0, 90.0, 110.0)


def kapak_tarama(parcalar, kn, dx=0.0, acilar=ACI_TARAMA):
    """v14b · soğuk kapak (K1: flipper katlanarak) açılırken hareketsiz parçalara + (K1) flipper ↔ K1 parçalarına çakışma (> 1 mm³) ·
    parcalar [(ad, şekil)] (dünya adlarında 'TU:' öneki olabilir) · [(açı, hareketli, diğer, hacim)]"""
    yal = lambda a: a.split(":")[-1]
    g_ = ("onyuz_%s_" % kn,) + (("onyuz_flipper",) if kn == "K1" else ())
    har = [(a, s) for a, s in parcalar if yal(a).startswith(g_)]
    sab = [(a, s, s.BoundingBox()) for a, s in parcalar if not yal(a).startswith(g_)]
    bul = []
    for aci in acilar:
        mv = [(a, flipper_don(s, aci, dx) if yal(a).startswith("onyuz_flipper") else kapak_don(s, kn, aci, dx)) for a, s in har]
        for a, m in mv:
            mb = m.BoundingBox()
            for c, sc, bc in sab + ([(c_, m_, m_.BoundingBox()) for c_, m_ in mv if not yal(c_).startswith("onyuz_flipper")] if yal(a).startswith("onyuz_flipper") else []):
                if mb.xmax < bc.xmin or bc.xmax < mb.xmin or mb.ymax < bc.ymin or bc.ymax < mb.ymin or mb.zmax < bc.zmin or bc.zmax < mb.zmin: continue
                try: v = m.intersect(sc).Volume()
                except Exception: v = -1.0
                if v > 1.0 or v < 0: bul.append((aci, a, c, round(v, 1)))
    return bul


for _kn in ("K1", "K2"):
    _kt = kapak_tarama(_TUP, _kn)
    kontrol("v14b · %s AÇILMA TARAMASI (TU parçaları · 0–110°, %d açı · sanal pivot ön dış köşe%s): çakışma %d"
            % (_kn, len(ACI_TARAMA), " · flipper katlanır min(90, %.0f·α), K2 KAPALI" % FLIP_K if _kn == "K1" else " · K1 + flipper KAPALI", len(_kt)), not _kt, str(_kt[:6]))
kontrol("v14b · flipper kam oluğu: pim yolu %d nokta · α 0–%.2f° · tam katlanma (α %.1f°) oluğun İÇİNDE → kapanırken pim oluğa −90°'de aynı yerden girer · çıkış dünya x %.1f + r 4 < 1493 (K1 fitil halkasının içi)"
        % (len(PIM_YOLU), PIM_YOLU[-1][2], 90.0 / FLIP_K, PIM_YOLU[-1][0] + DX_DUNYA), PIM_YOLU[-1][2] >= 90.0 / FLIP_K and PIM_YOLU[-1][0] + DX_DUNYA + FLIP_PIM[2] < 1493.0)
'''
degis('\n\ndef den_assert():', DEN_B + '\n\ndef den_assert():')

io.open(os.path.join(U, CIKIS), "w", encoding="utf-8").write(s)
compile(s, CIKIS, "exec")
print("%s yazildi (%d satir)" % (CIKIS, s.count(NL) + 1))
