# -*- coding: utf-8 -*-
"""topping_cad_v29 → v30 (29 Eyl 2026 gece · YEREL).
Kemal: "soğutma grubunu alta (arka köşe), sağ köşedekileri kaldır, o bölüm temiz boş · basamaklı yalıtımı kaldır, dikdörtgen · eşitlik isterim · temiz modelle".
  · TEKNİK CEP KALKTI: Secop + pano + UPS + güç kaynağı + DIN + pedler + T kapağı + T çerçevesi + T köşebentleri
  · SOĞUTMA GRUBU KAİDEDE: Secop CU KLF6.6CND (dikdörtgen kutu → 43 °C'ye yakın pay) yan çevrili, arka-alt köşede C kaidesinin 3. gözüne ~78 mm gömülü
    (kaide_cad_v4 cebi) · tepsi + 4 askı TC tabanına · Ø40 pedler
  · HAVA sanayi dolabı gibi ÖNDEN: sol mekanizma kanadının alt bandı EMİŞ (70 yarık 60 × 6 + yıkanabilir filtre) → kaide 1.–2. göz → taban açıklıkları →
    teknik bölme → ayırma perdesi → ünite → 3.–4. göz → sağ kanadın alt bandı ATIŞ · teknik bölme gıda tarafına kapalı (ön perde z −475, enerji zinciri kanalı 25 öne) · kuru bölme tabanı
  · pano + UPS + güç kaynağı KURU BÖLMENİN ÜSTÜNE (arka saca) · üstte ayrı servis kapağı · ana hava rakoru kuru bölmeye (z −740)
Yalnız okur: topping_cad_v29.py · yazar: topping_cad_v30.py"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_cad_v29.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:100], s.count(a), n)
    s = s.replace(a, b)


def blok(bas, son, yeni):
    global s
    assert s.count(bas) == 1, ("bas", bas[:100], s.count(bas))
    i = s.index(bas)
    assert s.count(son, i) >= 1, ("son", son[:100])
    j = s.index(son, i)
    s = s[:i] + yeni + s[j:]


# ---------------------------------------------------------------- 0 · başlık + sabitler
degis('"""topping_cad_v29 (29 Eyl 2026 · YEREL · yap_topping_cad_v29.py): TEKNİK CEP KUTUNUN ÜSTÜNDE',
      '"""topping_cad_v30 (29 Eyl 2026 gece · YEREL · yap_topping_cad_v30.py): SOĞUTMA GRUBU KAİDEDE (arka-alt) · TEKNİK CEP KALKTI · HAVA ÖNDEN KANATLARIN ALT BANDINDAN\n'
      'v30: Kemal "soğutma grubunu alta, sağ köşedekileri kaldır, o bölüm temiz boş · dikdörtgen · eşitlik isterim": Secop CU KLF6.6CND yan çevrili, C kaidesinin 3. gözünde\n'
      '     (kaide_cad_v4 cebi) · sol kanat alt bandı EMİŞ + filtre / sağ kanat ATIŞ · teknik bölme (ön perde −475 · enerji zinciri kanalı 25 öne · ayırma perdesi · kuru bölme tabanı) · pano + UPS kuru bölmenin\n'
      '     üstünde (üstten servis kapağı) · ana hava rakoru kuru bölmeye (z −740) · soğuk kutu dikdörtgen + eşit kapaklar topping_uno_cad_v18\n'
      'v29: topping_cad_v29 (29 Eyl 2026 · YEREL · yap_topping_cad_v29.py): TEKNİK CEP KUTUNUN ÜSTÜNDE')
degis('TU_DOSYA = os.environ.get("TOPPING_TU", "topping_uno_cad_v16.py")', 'TU_DOSYA = os.environ.get("TOPPING_TU", "topping_uno_cad_v18.py")   # v30: dikdörtgen soğuk kutu + eşit kapaklar')
degis("RAKOR_ANA = (1809.0 - 892.0, -432.0)", "RAKOR_ANA = (1809.0 - 892.0, -740.0)   # v30: KURU BÖLMEYE (teknik cep yok · v25–v29 z −432)")
degis('(1600.75, 2497.0, MEK_PAN_Y0, 1107.5),\n               "onyuz_T_kapagi": (1521.5, 2497.0, 1578.0, 1859.0)}',
      '(1600.75, 2497.0, MEK_PAN_Y0, 1107.5)}   # v30: T kapağı KALKTI (teknik cep yok · K2 tavana kadar, topping_uno_cad_v18)')
degis(', "onyuz_T_kapagi": (2497.0, "sag")}', '}')
degis("TEK_TABAN_D, TEK_PED = 1578.0, 6.0",
      '''# v30 · SOĞUTMA GRUBU KAİDEDE (Kemal 29 Eyl gece): Secop CU KLF6.6CND 307 × 272 × 380 YAN ÇEVRİLİ (380 x boyunca · kondenser + fan SOL uçta → hava soldan girer,
#       sağdan çıkar — ünite yönü soğutmacı firmayla doğrulanacak) · C kaidesinin 3. arka gözünde (kaide_cad_v4 cebi) · tepsi + askılar TC tabanına · DÜNYA ölçüleri
CU_X, CU_Y, CU_Z = (1633.0, 2013.0), (815.0, 1087.0), (-785.0, -478.0)            # 380 × 272 × 307 · taban sacının (893,5) 78,5 altına gömülü · üstü soğuk kutuya 22
CU_PED, CU_TEPSI_Y = 6.0, (806.0, 809.0)                                           # Ø40 × 6 titreşim pedi · tepsi 3 mm (B tavanına 806 − 788 = 18 mm hava)
CU_CEP = (1628.0, 2095.0, -790.0, -477.0)                                          # taban + kaide plakası kesiği: ünite + 5 (1628–2018) · sağında ATIŞ boşluğu (2018–2095) · önü perdenin arkasında
AYIRMA_X = 1631.5                                                                  # hava ayırma perdesi (ünitenin sol yüzü) · solu EMİŞ, sağı ATIŞ
TB_PERDE_Z, TB_X1 = -475.0, 2420.0                                                 # teknik bölme ön perdesi = enerji zinciri kanalının arka yüzü (kanal 25 öne: −475…−415) · sağ perde (sabit tahrik x ≥ 2434 dışarıda)
EZK_Z = (-475.0, -415.0)                                                           # v30 · enerji zinciri kanalı (v25–v29 −500…−440 → ünitenin önüne 22 mm giriyordu) · mekanizma teknesinin arka kenarına dayalı
TABAN_EMIS = ((745.0, 1129.0), (1179.0, 1575.0)); TABAN_ATIS = ((2145.0, 2415.0),); TABAN_Z = (-785.0, -480.0)   # taban hava açıklıkları (kaide 1., 2. / 4. arka göz · ön perdenin arkasında)
KAIDE_PENCERE_X = {"emis": ((750.0, 1124.0), (1184.0, 1570.0)), "atis": ((1630.0, 2090.0), (2150.0, 2450.0))}   # = kaide_cad_v4.C_PENCERE_X (dünya denetiminde karşılaştırılır)
KAIDE_PENCERE_Y = (800.0, 866.0)                                                   # = kaide_cad_v4.C_PENCERE_Y
IZGARA_Y = [826.0 + 9.0 * i_ for i_ in range(7)]                                   # mekanizma kanatlarının alt bandı: 7 sıra × 6 (dünya y 826–886 · alt kaydın 821 üstü, kaide 888 altı)
IZGARA_X = {"sol": [750.0 + 70.0 * i_ for i_ in range(10)], "sag": [1758.5 + 70.0 * i_ for i_ in range(10)]}   # 10 × 60 · derze simetrik (sol 750–1440 · sağ 1758,5–2448,5)
KLF66 = {32: 499.0, 35: 480.0, 38: 460.0, 40: 446.0}                               # W @ −10 °C · Secop föy (sogutma_topping_v1 SECOP_LISTE 314H6003, 35 / 40 doğrusal)
GEREKEN_DIK = {32: 340.0, 35: 368.0, 38: 393.0, 40: 410.0}                         # W · dikdörtgen kutu, dolum + ılık gün (dikdortgen_sogutma_v1 = sogutma_topping_v1 yöntemi, TU v16/v18 geometrisi)
# v29 (tarihçe): TEK_TABAN_D, TEK_PED = 1578.0, 6.0''')
degis("CU_KLF = (860.0, 1167.0, 272.0, -40.0, -420.0)", "# v29 (tarihçe): CU_KLF = (860.0, 1167.0, 272.0, -40.0, -420.0)")

# ---------------------------------------------------------------- 1 · dış kabuk: taban açıklıkları + ünite cebi · tavan + kuru bölme servis kapağı · rakor
degis('    ekle("dis_taban", kut(0, W, 0, SAC, Z_KABUK, -D), "sac", bom=("Dış taban sacı", 1, "304 1,5 mm · lazer + abkant", "modülün tabanı, alttaki B modülüne oturur"))',
      '''    _dt = kut(0, W, 0, SAC, Z_KABUK, -D)
    for _a, _b in TABAN_EMIS + TABAN_ATIS:                                       # v30 · kaide gözlerine hava açıklıkları (teknik bölmenin altında, gıda bölgesinin DIŞINDA)
        _dt = _dt.cut(kut(_a - DX_D, _b - DX_D, -1.0, SAC + 1.0, TABAN_Z[1], TABAN_Z[0]))
    _dt = _dt.cut(kut(CU_CEP[0] - DX_D, CU_CEP[1] - DX_D, -1.0, SAC + 1.0, CU_CEP[3], CU_CEP[2]))   # v30 · soğutma grubu cebi + sağında atış
    ekle("dis_taban", _dt, "sac", bom=("Dış taban sacı", 1, "304 1,5 mm · lazer + abkant · v30: arka bantta 3 hava açıklığı + soğutma grubu cebi", "modülün tabanı, alttaki B modülüne oturur"))''')
degis('    ekle("dis_tavan", kut(0, W, Y - SAC, Y, Z_KABUK, -D), "sac", bom=("Dış tavan sacı", 1, "304 1,5 mm · lazer + abkant", "üst kapak; soğutma grubu buraya oturur"))',
      '''    ekle("dis_tavan", kut(0, W, Y - SAC, Y, Z_KABUK, -630.0), "sac", bom=("Dış tavan sacı", 1, "304 1,5 mm · lazer + abkant", "v30: soğuk kutunun üstü (TU v18 tavanı, düz) · üstünde cihaz YOK"))
    ekle("kuru_bolme_servis_kapagi", kut(0, W, Y - SAC, Y, -630.0, -D), "sac",
         bom=("Kuru bölme servis kapağı", 1, "304 1,5 mm · 1800 × 200 · kenarları bükülü · 8 × M5 perçin somun", "v30 · pano + UPS + güç kaynağı + sürücüler + valf adası ÜSTTEN buradan · yan saclara, arka saca ve soğuk kutunun arka dış sacına oturur"))''')
degis('"ana hat fırın üstünden TOPPING teknik cebine (montaj ANA_V44)"', '"v30: ana hat fırın üstünden TOPPING KURU BÖLMESİNE (z −740 · montaj ANA_V44)"')
degis('    ekle("enerji_zinciri_kanali", kut(-520.0, 1790.0, SAC, SAC + 60.0, -500.0, -440.0).cut(kut(-517.0, 1787.0, SAC + 2.0, SAC + 61.0, -497.0, -443.0)), "sac",   # v25: tabana oturur (v24: 3 mm havada)',
      '    ekle("enerji_zinciri_kanali", kut(-520.0, 1790.0, SAC, SAC + 60.0, EZK_Z[0], EZK_Z[1]).cut(kut(-517.0, 1787.0, SAC + 2.0, SAC + 61.0, EZK_Z[0] + 3.0, EZK_Z[1] - 3.0)), "sac",   # v30: 25 öne (arka duvarı = teknik bölme ön perdesinin altı) · v25: tabana oturur')

# ---------------------------------------------------------------- 2 · teknik cep → SOĞUTMA GRUBU KAİDEDE + TEKNİK BÖLME + KURU BÖLME ELEKTRİĞİ
blok('    # v29 · TEKNİK CEP (Kemal: "havada mı, tek sağ duvardan mı destekleniyor',
     "    # v25 · KURU BÖLME SÜRÜCÜLERİ",
     '''    # v30 · SOĞUTMA GRUBU KAİDEDE + TEKNİK BÖLME (Kemal 29 Eyl gece: "soğutma grubunu alta, sağ köşedekileri kaldır, o bölüm temiz boş · eşitlik isterim"):
    #       v29'un teknik cebi (ünite + pano + UPS + güç kaynağı + DIN + pedler) KALKTI → soğuk kutu dikdörtgen (topping_uno_cad_v18). Ünite arka-alt köşede,
    #       C kaidesinin 3. arka gözüne gömülü (kaide_cad_v4 cebi) · tepsi + 4 askı TC tabanına · hava sanayi dolabı gibi ÖNDEN: sol mekanizma kanadının alt
    #       bandından girer (kaide 1.–2. gözler) → taban açıklıkları → teknik bölme → ayırma perdesi → ünite → sağ taraf → 3.–4. gözler → sağ kanadın alt bandı ·
    #       teknik bölme GIDA tarafına kapalı (ön perde z −475 = enerji zinciri kanalının arkası; kanal 25 öne alındı) · kuru bölme tabanı ünite havasını kuru bölmeden ayırır
    _xl = lambda x_: x_ - DX_D
    _yl = lambda y_: y_ - DY_D
    ekle("sogutma_grubu_KLF66", kut(_xl(CU_X[0]), _xl(CU_X[1]), _yl(CU_Y[0]), _yl(CU_Y[1]), CU_Z[0], CU_Z[1]), "motor",
         bom=("Yoğuşma ünitesi Secop CU KLF6.6CND (R290) · 314H6003", 1, "307 × 272 × 380 · 14,5 kg · 499 W @ −10/32 °C · 460 @ 38 · 426 @ 43 (föy)",
              "v30 · KAİDEDE arka-alt (yan çevrili: 380 x boyunca · kondenser + fan SOL uçta → hava soldan girer, sağdan çıkar · yön soğutmacı firmayla doğrulanacak) · "
              "gereken (dikdörtgen kutu, dolum + ılık) 340 / 368 / 393 / 410 W @ 32 / 35 / 38 / 40 °C · hatlar üst yüzüne dikine (TU v18) · montaj / gaz dolumu soğutmacı firma"))
    for _i, (_px, _pz) in enumerate(((CU_X[0] + 25.0, CU_Z[0] + 25.0), (CU_X[1] - 25.0, CU_Z[0] + 25.0), (CU_X[0] + 25.0, CU_Z[1] - 25.0), (CU_X[1] - 25.0, CU_Z[1] - 25.0))):
        ekle("sogutma_grubu_pedi_%d" % _i, sily(_xl(_px), _pz, 20.0, _yl(CU_TEPSI_Y[1]), _yl(CU_TEPSI_Y[1] + CU_PED)), "silikon",
             bom=("Titreşim pedi Ø40 × 6 · neopren 60 Shore A (tepsiye yapıştırma + ünite tabanına M6)", 4, "parça no VARSAYIM", "v30 · soğutma grubu tepsisinde") if _i == 0 else None)
    ekle("sogutma_grubu_tepsisi", kut(_xl(CU_X[0]), _xl(CU_X[1]), _yl(CU_TEPSI_Y[0]), _yl(CU_TEPSI_Y[1]), CU_CEP[2] + 1.0, -438.0), "sac",
         bom=("Soğutma grubu tepsisi AISI 304 3 mm", 1, "380 × 351 · arka kenarı 2 askıya kaynak · ön kenarı kaidenin tepsi köşebendine oturur (kaide_cad_v4, 2 × M5)",
              "v30 · kaide cebinde · B dolabının tavanına 18 mm hava (ısı köprüsü yok)"))
    for _i, (_ax, _ar) in enumerate(((CU_X[0] + 5.0, "arka"), (CU_X[1] - 35.0, "arka"))):                    # önde askı yok: enerji zinciri kanalı taban sacında (−475…−415)
        _z0, _z1 = (CU_CEP[2] + 1.0, CU_CEP[2] + 4.0) if _ar == "arka" else (CU_CEP[3] - 4.0, CU_CEP[3] - 1.0)
        _zu = (CU_CEP[2] - 29.0, CU_CEP[2] + 4.0) if _ar == "arka" else (CU_CEP[3] - 4.0, CU_CEP[3] + 29.0)
        _as = kut(_xl(_ax), _xl(_ax + 30.0), _yl(CU_TEPSI_Y[1]), SAC, _z0, _z1).union(kut(_xl(_ax), _xl(_ax + 30.0), SAC, SAC + 3.0, _zu[0], _zu[1]))
        ekle("sogutma_grubu_askisi_%d" % _i, _as, "sac",
             bom=("Soğutma grubu askısı L 30 × 3 AISI 304", 2, "dik kol tepsinin arka kenarına kaynak · yatay kol TC tabanına 2 × M6 (altında kaide arka profili)", "v30 · ünite + tepsi ≈ 18 kg: yarısı 2 askıda (≈ 45 N), yarısı kaidenin ön köşebendinde") if _i == 0 else None)
    _cp = kut(_xl(CU_CEP[0] + 1.0), _xl(CU_CEP[0] + 2.5), _yl(CU_TEPSI_Y[1]), SAC, CU_CEP[2] + 1.0, CU_CEP[3] - 1.0).union(
        kut(_xl(CU_CEP[0] - 14.0), _xl(CU_CEP[0] + 2.5), SAC, SAC + 1.5, CU_CEP[2] + 1.0, CU_CEP[3] - 1.0))
    ekle("sogutma_grubu_cep_perdesi", _cp, "sac",
         bom=("Soğutma grubu cebi sol perdesi AISI 304 1,5 · L", 1, "üst kolu TC tabanına 2 × M5", "v30 · cebin emiş tarafını kapatır (atış havası ünitenin altından emişe dönmez)"))
    _ayir = lambda x0_, x1_: kut(x0_, x1_, SAC, _yl(1107.5), -D + SAC, -630.0).union(kut(x0_, x1_, SAC, _yl(1109.0), -630.0, TB_PERDE_Z - 1.5))   # kuru bölme tabanının altında / soğuk kutunun altında
    ekle("teknik_bolme_ayirma_perdesi", _ayir(_xl(AYIRMA_X), _xl(AYIRMA_X + 1.5)).cut(kut(_xl(AYIRMA_X) - 1.0, _xl(AYIRMA_X + 1.5) + 1.0, SAC - 1.0, _yl(CU_Y[1]), CU_Z[0], CU_Z[1])), "sac",
         bom=("Teknik bölme hava ayırma perdesi AISI 304 1,5", 1, "ünite kesiti kadar pencereli · kenarları köpük bantlı", "v30 · solu EMİŞ (kaide 1.–2. göz), sağı ATIŞ (3.–4. göz) · hava yalnız ünitenin içinden geçer"))
    ekle("teknik_bolme_on_perdesi", kut(SAC, _xl(TB_X1), SAC + 60.0, _yl(1109.0), TB_PERDE_Z - 1.5, TB_PERDE_Z), "sac",
         bom=("Teknik bölme ön perdesi AISI 304 1,5 (sökülebilir)", 1, "%.0f × %.1f · alt kenarı enerji zinciri kanalının arka kenarına oturur (kanalın arka duvarı perdenin altı) · kenarları köpük bantlı · 8 × M5 perçin somun" % (TB_X1 - DX_D - SAC, 1109.0 - DY_D - SAC - 60.0),
              "v30 · teknik bölmeyi GIDA bölgesine (mekanizma) kapatır · servis: mekanizma kanatları açılıp tabla kenara alınınca sökülür (ünite önü ön düzlemden ≈ 560 mm)"))
    ekle("teknik_bolme_sag_perdesi", _ayir(_xl(TB_X1 - 1.5), _xl(TB_X1)), "sac",
         bom=("Teknik bölme sağ perdesi AISI 304 1,5", 1, "arka sac + ön perde + kuru bölme tabanı arasında", "v30 · sabit tahrik (x ≥ 2434) bölmenin DIŞINDA kalır"))
    _kt = kut(SAC, _xl(TB_X1), _yl(1107.5), _yl(1109.0), -D + SAC, -630.0)
    _kt = _kt.cut(kut(_xl(2349.0), _xl(2401.0), _yl(1106.0), _yl(1110.0), -781.0, -689.0))                 # şartlandırıcı gövdesi geçer (TU FRL x 2350–2400)
    for _hx, _hr in ((1990.0, 15.5), (1950.0, 3.2)):                                                       # soğutma hatları (TU v18 HAT_X_INIS · z −660)
        _kt = _kt.cut(sily(_xl(_hx), -660.0, _hr + 1.0, _yl(1106.0), _yl(1110.0)))
    ekle("kuru_bolme_tabani", _kt, "sac",
         bom=("Kuru bölme tabanı AISI 304 1,5", 1, "hat + şartlandırıcı delikleri (lastik rakor)", "v30 · kuru bölmeyi teknik bölmeden (ünite havası 40–50 °C) ayırır · pano / sürücüler sıcak havada kalmaz"))
    # v30 · KURU BÖLMENİN ÜSTÜ: pano + UPS + güç kaynağı arka saca (üstten servis kapağıyla) · R290 sızarsa aşağı çöker → röleler ünitenin 500 mm üstünde
    ekle("kuru_pano_kutusu", kut(_xl(900.0), _xl(1450.0), _yl(1585.0), _yl(1845.0), -D + SAC, -D + SAC + 120.0).cut(
        kut(_xl(901.5), _xl(1448.5), _yl(1586.5), _yl(1843.5), -D + SAC + 1.5, -D + SAC + 118.5)), "sac",
         bom=("TOPPING panosu", 1, "304 · 550 × 260 × 120 · önü (kuru bölmeye) kapaklı, IP54", "PLC giriş/çıkış + röleler + sürücü beslemesi · v30: kuru bölmenin ÜSTÜNDE arka saca 4 × M6 (üstten servis kapağıyla ulaşılır)"))
    ekle("kuru_din_plakasi", kut(_xl(2020.0), _xl(2230.0), _yl(1600.0), _yl(1760.0), -D + SAC, -D + SAC + 2.0), "sac",
         bom=("DIN montaj plakası 304 2 mm", 1, "210 × 160 · arka saca 4 × M6 (perçin somun)", "v30 · UPS + güç kaynağı raylarını taşır (kuru bölmenin üstü, soğutma hatlarının sağı)"))
    ekle("kuru_din_rayi_ups", kut(_xl(2030.0), _xl(2130.0), _yl(1612.0), _yl(1647.0), -D + SAC + 2.0, -D + SAC + 9.5), "sac",
         bom=("DIN ray TS35 × 7,5 · UPS", 1, "EN 60715 · 100 mm", "v30 · DIN plakasında"))
    ekle("kuru_din_rayi_guc", kut(_xl(2135.0), _xl(2215.0), _yl(1622.0), _yl(1657.0), -D + SAC + 2.0, -D + SAC + 9.5), "sac",
         bom=("DIN ray TS35 × 7,5 · güç kaynağı", 1, "EN 60715 · 80 mm", "v30 · DIN plakasında · güç kaynağının ray tırnağı gövde altının 10 mm üstünde (v29 ile aynı)"))
    ekle("kuru_ups", din_parca(UPS_STEP, _xl(2040.0), _yl(1612.0), -D + SAC + 9.5 + 130.5), "koyu",
         bom=("UPS PULS UB10.242 · DIN ray 24 V", 1, "121,7 × 49,0 × 130,5 mm (GERÇEK CAD) · ayrıca akü modülü ister",
              "elektrik kesintisinde kaset konumları ve saat korunur · v30: kuru bölmenin üstünde DIN plakasında"))
    ekle("kuru_guc_kaynagi", din_parca(GUC_STEP, _xl(2140.0), _yl(1612.0), -D + SAC + 9.5 + 122.8), "sac",
         bom=("Güç kaynağı MEAN WELL NDR-240-24 · 24 V 240 W", 1, "DIN ray · 125,2 × 63,0 × 122,8 mm (GERÇEK CAD)",
              "aynı anda en çok 2 mil döner; motor 2,8 A → gerek %d W, bir üst standart boy 240 W · v30: kuru bölmenin üstünde" % H.S["elektrik"]["guc_kaynagi_W"]))
''')

# ---------------------------------------------------------------- 3 · ön yüz: T çerçevesi + T kapağı + köşebentler KALKTI · kanatların alt bandı ızgara + filtre
degis("    MEK_Y = (yl(791.0), yl(1107.5)); T_Y = (yl(TEK_TABAN_D), yl(1859.0))          # v29: T teknik tabandan (TU v16 · 1578)",
      "    MEK_Y = (yl(791.0), yl(1107.5))                                                   # v30: T (teknik cep) kalktı")
blok('           ("onyuz_cerceve_T_sol_dikme", boru_y(xl(1521.5)',
     "    for _i, (_a, _w) in enumerate(CER):",
     "           ]                                                                            # v30: T çerçevesi (4 parça) KALKTI\n")
degis('"mekanizma bandı (5 parça) + teknik cep (4 parça) · z +39…+59 (panel arkası) · yan sacların ön dönüşüne M6"',
      '"mekanizma bandı (6 parça) · z +39…+59 (panel arkası) · yan sacların ön dönüşüne M6 · v30: teknik cep çerçevesi (4 parça) kalktı"')
blok("    for _i, _yk in enumerate((yl(1600.0), yl(1790.0))):",
     "    # tava paneller · derz 3 · dünya:",
     "    # v30: T sol dikme köşebentleri KALKTI (T çerçevesi yok)\n")
blok("    _yar = []",
     "    for _a, (_x0, _x1, _y0, _y1), _yr, _mt, _yc in PAN:",
     '''    # v30 · MEKANİZMA KANATLARININ ALT BANDI = SOĞUTMA GRUBU IZGARASI (sanayi dolabı gibi): kaide hizası (dünya 826–886), alt kaydın (791–821) üstü ·
    #       10 kolon × 7 sıra lazer yarık 60 × 6 · derze simetrik (sol 750–1440 EMİŞ · sağ 1758,5–2448,5 ATIŞ · arası 318,5 → kısa devre yok)
    _yar = {"sol": [], "sag": []}
    for _kn, _xs in IZGARA_X.items():
        for _xg in _xs:
            for _yg in IZGARA_Y:
                _yar[_kn].append((xl(_xg), xl(_xg + 60.0), yl(_yg), yl(_yg + 6.0)))
    PAN = [("onyuz_mekanizma_kanadi_sol", (xl(701.5), xl(1597.75), MEK_PY[0], MEK_PY[1]), tuple(_yar["sol"]), "sol", 57.0),
           ("onyuz_mekanizma_kanadi_sag", (xl(1600.75), xl(2497.0), MEK_PY[0], MEK_PY[1]), tuple(_yar["sag"]), "sag", 57.0)]   # v30: T kapağı yok
''')
degis('" · 64 lazer yarık 60 × 4 (giriş sol-alt / çıkış sağ-üst, soğutma grubu havası)" if _yr else ""',
      '(" · %d lazer yarık 60 × 6 alt bantta (kaide hizası · %s · soğutma grubu havası)" % (len(_yr), "EMİŞ" if _mt == "sol" else "ATIŞ")) if _yr else ""')
degis("    # v25b · denetim_C bulgu 12: montajın düşürdüğü v1 soğuk hücresi",
      '''    ekle("onyuz_mekanizma_kanadi_sol_filtre", kut(xl(745.0), xl(1445.0), yl(823.0), yl(886.0), Z_PAN_C[0] + 3.0, Z_ON - 1.5), "pom",
         bom=("Kondenser emiş filtresi · yıkanabilir paslanmaz tel örgü + çerçeve", 1, "700 × 63 × 15,5 · sol kanadın alt bandının içinde 2 klipsle",
              "v30 · sol kanat açılınca çıkar, suyla yıkanır (ayda 1 · VARSAYIM) · kondenseri yağ / undan korur"))
    # v25b · denetim_C bulgu 12: montajın düşürdüğü v1 soğuk hücresi''')

# ---------------------------------------------------------------- 4 · dünya denetimi
degis("ANA_V44_DUNYA = [(3790.0, 1809.0, -380.0), (3790.0, 1809.0, -432.0), (2340.0, 1809.0, -432.0), (2340.0, 1809.0, -740.0)]",
      "ANA_V44_DUNYA = [(3790.0, 1809.0, -380.0), (3790.0, 1809.0, -740.0), (2340.0, 1809.0, -740.0), (2340.0, 1167.0, -740.0)]   # v30: fırın üstünde arkaya (z −740), TOPPING'e kuru bölmeden (hat_montaj_v86 ANA_V44)")
degis('             "TC:onyuz_T_kapagi": (1521.5, 2497.0, TEK_TABAN_D, 1859.0), "TU:onyuz_K1_dis_sac": (701.5, 1518.5, 1110.5, 1859.0), "TU:onyuz_K2_dis_sac": (1521.5, 2497.0, 1110.5, TEK_TABAN_D - 3.0)}',
      '             "TU:onyuz_K1_dis_sac": (701.5, 1597.75, 1110.5, 1859.0), "TU:onyuz_K2_dis_sac": (1600.75, 2497.0, 1110.5, 1859.0)}   # v30: T kapağı yok · K1 = K2 (TU v18)')
degis("    derz = 1795.5 * 3.0 + 3.0 * (1107.5 - MEK_PAN_Y0) + 3.0 * 748.5 + 975.5 * 3.0",
      "    derz = 1795.5 * 3.0 + 3.0 * (1859.0 - MEK_PAN_Y0) - 9.0                          # v30: yatay 1107,5/1110,5 + dikey 1597,75/1600,75 (kanatlar + K1|K2 aynı derz) − kesişim")
degis('k("ön yüz kapsama: 5 panel %.0f mm²', 'k("ön yüz kapsama: 4 panel (v30 · 2 kanat + K1 + K2, EŞİT) %.0f mm²')
degis('k("montaj ana hattı (ANA_V44 · y 1809 · z −432) sağ yan sacın rakorundan geçer:', 'k("v30 · montaj ana hattı (ANA_V44 · y 1809 · z −740, KURU BÖLMEYE) sağ yan sacın rakorundan geçer:')
blok("    # 8 · teknik cep tabanı + DIN ray sınırı",
     "    # 8b · v25b · SOĞUK ODA TABANI + ÇERÇEVE BANDI",
     '''    # 8 · v30 · SAĞ ÜST BOŞ · SOĞUTMA GRUBU KAİDEDE · TEKNİK BÖLME + HAVA YOLU · KURU BÖLME ELEKTRİĞİ
    _S = dict(W_)
    _mt = lambda a_, c_: (lambda d_: d_.Value() if d_.IsDone() else 99.0)(DSS(_S[a_].wrapped, _S[c_].wrapped))
    _eski_tek = [a for a in B_ if a.startswith(("TC:teknik_sogutma", "TC:teknik_pano", "TC:teknik_ups", "TC:teknik_guc", "TC:teknik_din", "TC:teknik_takoz",
                                               "TC:onyuz_T_", "TC:onyuz_cerceve_T_", "TU:teknik_ayirma", "TU:teknik_bant", "TU:kabin_sag_teknik"))]
    _cu = B_["TC:sogutma_grubu_KLF66"]; _ts = B_["TC:sogutma_grubu_tepsisi"]; _ua = B_["TU:alt_yalitim_saci"]
    _ust = [(a, B_[a].ymin) for a in B_ if B_[a].xmin < 2497.0 and B_[a].xmax > 1550.0 and B_[a].ymin > 1805.0 and B_[a].zmin > -628.0 and not a.startswith(("TC:dis_", "TC:kuru_bolme_servis", "TU:yalitim_blogu", "TU:soguk_", "TU:onyuz_", "TC:onyuz_", "TU:kabin_", "TU:evaporator", "TU:sogutma_"))]
    k("v30 · SAĞ ÜST BOŞ: teknik cep parçası %d (Secop, pano, UPS, güç kaynağı, DIN, pedler, T kapağı + çerçevesi, ayırma sacları) · soğuk kutunun üstünde cihaz %d · soğutma grubu (Secop CU KLF6.6CND yan çevrili) KAİDEDE x %.0f–%.0f · y %.0f–%.0f (taban sacının %.1f altına gömülü) · z %.0f…%.0f · üstü soğuk kutunun altına %.1f (≥ 15) · tepsi B tavanına %.1f (≥ 15, ısı köprüsü yok)"
      % (len(_eski_tek), len(_ust), _cu.xmin, _cu.xmax, _cu.ymin, _cu.ymax, DY_D + SAC - _cu.ymin, _cu.zmin, _cu.zmax, _ua.ymin - _cu.ymax, _ts.ymin - 788.0),
      not _eski_tek and not _ust and _ua.ymin - _cu.ymax >= 15.0 and _ts.ymin - 788.0 >= 15.0, str((_eski_tek + [a for a, y_ in _ust])[:6]))
    _Q = (KLF66[32] + 279.0 * 1.1) / (1.2 * 1006.0 * 10.0)                     # m³/s · KLF6.6CND 32 °C'de atılan ısı (kapasite + güç × 1,1 · güç 279 W @ −10/25 föy) · hava 10 K ısınır
    _etkin = lambda xs, pen: sum(max(0.0, min(x_ + 60.0, b_) - max(x_, a_)) for x_ in xs for a_, b_ in pen) * 6.0 * len(IZGARA_Y) * 1e-6
    _es, _ea = _etkin(IZGARA_X["sol"], KAIDE_PENCERE_X["emis"]), _etkin(IZGARA_X["sag"], KAIDE_PENCERE_X["atis"])
    _pw = lambda pen: sum(b_ - a_ for a_, b_ in pen) * (KAIDE_PENCERE_Y[1] - KAIDE_PENCERE_Y[0]) * 1e-6
    _fe = sum((b_ - a_) * (TABAN_Z[1] - TABAN_Z[0]) for a_, b_ in TABAN_EMIS) * 1e-6
    _fa = sum((b_ - a_) * (TABAN_Z[1] - TABAN_Z[0]) for a_, b_ in TABAN_ATIS) * 1e-6 + (CU_CEP[1] - (CU_X[1] + 5.0)) * (CU_CEP[3] - CU_CEP[2]) * 1e-6
    _ara = IZGARA_X["sag"][0] - (IZGARA_X["sol"][-1] + 60.0)
    k("v30 · HAVA YOLU (sanayi dolabı gibi önden): %.0f m³/h (KLF6.6CND 32 °C'de atılan %.0f W, hava 10 K ısınır) · EMİŞ sol kanat %d yarık → pencere önünde etkin %.4f m² (%.1f m/s ≤ 3,5) · kaide penceresi %.4f · taban açıklığı %.4f · "
      "ATIŞ sağ kanat %d yarık → etkin %.4f m² (%.1f m/s ≤ 3,5) · pencere %.4f · taban + cep yanı %.4f · emiş / atış yarıkları arası %.0f mm (≥ 250, kısa devre yok) · orta dikme (1584–1614) iki yanı ayırır"
      % (_Q * 3600.0, KLF66[32] + 279.0 * 1.1, len(IZGARA_X["sol"]) * len(IZGARA_Y), _es, _Q / _es, _pw(KAIDE_PENCERE_X["emis"]), _fe,
         len(IZGARA_X["sag"]) * len(IZGARA_Y), _ea, _Q / _ea, _pw(KAIDE_PENCERE_X["atis"]), _fa, _ara),
      _Q / _es <= 3.5 and _Q / _ea <= 3.5 and _ara >= 250.0 and min(_pw(KAIDE_PENCERE_X["emis"]), _pw(KAIDE_PENCERE_X["atis"]), _fe, _fa) >= max(_es, _ea))
    _pay = {t_: KLF66[t_] / GEREKEN_DIK[t_] - 1.0 for t_ in KLF66}
    _yuz = (CU_Y[1] - (DY_D + SAC)) / (CU_Y[1] - CU_Y[0])                          # kondenser yüzünün taban üstünde kalan (açık) oranı
    k("v30 · KLF6.6CND (dikdörtgen kutu, dolum + ılık gün) pay: %s · kondenser yüzünün %%%.0f'i taban üstünde açık (alt %.0f mm cepte) → %%5 kayıp sayılsa 40 °C'de %+.0f%% (≥ 0)"
      % (" · ".join("%d °C %+.0f%%" % (t_, 100.0 * p_) for t_, p_ in sorted(_pay.items())), 100.0 * _yuz, DY_D + SAC - CU_Y[0], 100.0 * (0.95 * KLF66[40] / GEREKEN_DIK[40] - 1.0)),
      min(_pay.values()) >= 0.05 and 0.95 * KLF66[40] >= GEREKEN_DIK[40] and _yuz >= 0.65)
    _pn = B_["TC:kuru_pano_kutusu"]; _kz = B_["TC:kuru_bolme_tabani"]
    k("v30 · KURU BÖLMENİN ÜSTÜ: pano (x %.0f–%.0f · y %.0f–%.0f) + UPS + güç kaynağı arka sacta · kuru bölme tabanı y %.1f (ünite havası altta) · pano altı ünite üstünün %.0f mm yukarısında (R290 aşağı çöker) · üstleri servis kapağının %.1f mm altında"
      % (_pn.xmin, _pn.xmax, _pn.ymin, _pn.ymax, _kz.ymax, _pn.ymin - _cu.ymax, B_["TC:kuru_bolme_servis_kapagi"].ymin - max(B_[a].ymax for a in ("TC:kuru_pano_kutusu", "TC:kuru_ups", "TC:kuru_guc_kaynagi"))),
      _pn.ymin - _cu.ymax >= 400.0 and _kz.ymax <= _ua.ymin + 0.01 and B_["TC:kuru_bolme_servis_kapagi"].ymin - max(B_[a].ymax for a in ("TC:kuru_pano_kutusu", "TC:kuru_ups", "TC:kuru_guc_kaynagi")) >= 5.0)
''')
degis('        hn = ("TC:" + ad, "TC:" + ad + "_omega", "TC:" + ad + "_mentese_0", "TC:" + ad + "_mentese_1")',
      '        hn = ("TC:" + ad, "TC:" + ad + "_omega", "TC:" + ad + "_mentese_0", "TC:" + ad + "_mentese_1", "TC:" + ad + "_filtre")   # v30: filtre kanatla döner')
blok('    _bg = [("TU:onyuz_mentese_tabani_K1_mentese_0", "TC:dis_yan_sol")',
     "    _bd = [(a.split(\":\")[1]",
     '''    _bg = [("TU:onyuz_mentese_tabani_K1_mentese_0", "TC:dis_yan_sol"), ("TU:onyuz_mentese_tabani_K1_mentese_1", "TC:dis_yan_sol"),
           ("TU:onyuz_mentese_tabani_K2_mentese_0", "TC:dis_yan_sag"), ("TU:onyuz_mentese_tabani_K2_mentese_1", "TC:dis_yan_sag"),
           ("TU:raf_askisi_burclari_sol", "TC:dis_yan_sol"), ("TU:raf_askisi_burclari_sag", "TC:dis_yan_sag"), ("TU:kabin_sol_duvar_PU", "TC:dis_yan_sol"), ("TU:kabin_sag_duvar_PU", "TC:dis_yan_sag"),
           ("TU:yalitim_blogu", "TC:dis_tavan"), ("TU:yalitim_blogu", "TC:dis_yan_sag"), ("TU:soguk_arka_dis_sac", "TC:dis_yan_sol"), ("TU:soguk_arka_dis_sac", "TC:dis_yan_sag"),
           ("TU:alt_yalitim_saci", "TC:dis_yan_sol"), ("TU:alt_yalitim_saci", "TC:sensor_braketi_tabla_bos"), ("TU:alt_yalitim_saci", "TC:fire_silecegi_silindiri"),
           ("TC:st_yatak_flansi", "TC:st_tahrik_kutusu"), ("TC:st_yatak_flansi", "TC:st_tahrik_yatak_burcu"), ("TC:st_motor_adaptor_flansi", "TC:st_motor_kutusu"),
           ("TC:st_motor_adaptor_flansi", "TC:st_tahrik_motoru"), ("TC:st_motor_adaptor_flansi", "TC:st_tahrik_kutusu"), ("TC:st_tahrik_braketi", "TC:kayis_kirisi"),
           ("TU:onyuz_kilavuz_flipper", "TU:tasiyici_raf_3mm"),
           ("TC:sogutma_grubu_pedi_0", "TC:sogutma_grubu_tepsisi"), ("TC:sogutma_grubu_pedi_3", "TC:sogutma_grubu_tepsisi"), ("TC:sogutma_grubu_pedi_0", "TC:sogutma_grubu_KLF66"),
           ("TC:sogutma_grubu_pedi_3", "TC:sogutma_grubu_KLF66"), ("TC:sogutma_grubu_askisi_0", "TC:sogutma_grubu_tepsisi"), ("TC:sogutma_grubu_askisi_1", "TC:sogutma_grubu_tepsisi"),
           ("TC:sogutma_grubu_askisi_0", "TC:dis_taban"), ("TC:sogutma_grubu_askisi_1", "TC:dis_taban"), ("TC:sogutma_grubu_cep_perdesi", "TC:dis_taban"),
           ("TC:enerji_zinciri_kanali", "TC:dis_taban"), ("TC:enerji_zinciri_kanali", "TC:mekanizma_teknesi"),
           ("TU:sogutma_emis_hatti", "TC:sogutma_grubu_KLF66"), ("TU:sogutma_sivi_hatti", "TC:sogutma_grubu_KLF66"),
           ("TC:teknik_bolme_ayirma_perdesi", "TC:sogutma_grubu_KLF66"), ("TC:teknik_bolme_ayirma_perdesi", "TC:dis_taban"), ("TC:teknik_bolme_ayirma_perdesi", "TU:alt_yalitim_saci"),
           ("TC:teknik_bolme_on_perdesi", "TC:enerji_zinciri_kanali"), ("TC:teknik_bolme_on_perdesi", "TU:alt_yalitim_saci"), ("TC:teknik_bolme_on_perdesi", "TC:dis_yan_sol"),
           ("TC:teknik_bolme_sag_perdesi", "TC:dis_taban"), ("TC:teknik_bolme_sag_perdesi", "TC:kuru_bolme_tabani"), ("TC:teknik_bolme_sag_perdesi", "TC:dis_arka"),
           ("TC:kuru_bolme_tabani", "TC:dis_arka"), ("TC:kuru_bolme_tabani", "TU:soguk_arka_dis_sac"), ("TC:kuru_bolme_tabani", "TC:dis_yan_sol"),
           ("TC:kuru_pano_kutusu", "TC:dis_arka"), ("TC:kuru_din_plakasi", "TC:dis_arka"), ("TC:kuru_din_rayi_ups", "TC:kuru_din_plakasi"), ("TC:kuru_din_rayi_guc", "TC:kuru_din_plakasi"),
           ("TC:kuru_ups", "TC:kuru_din_rayi_ups"), ("TC:kuru_guc_kaynagi", "TC:kuru_din_rayi_guc"), ("TC:kuru_bolme_servis_kapagi", "TC:dis_yan_sag"), ("TC:kuru_bolme_servis_kapagi", "TC:dis_arka"),
           ("TC:onyuz_mekanizma_kanadi_sol_filtre", "TC:onyuz_mekanizma_kanadi_sol"),
           ("TC:onyuz_mekanizma_kanadi_sol_mentese_0", "TC:onyuz_mekanizma_kanadi_sol_mentese_0_taban"), ("TC:onyuz_mekanizma_kanadi_sol_mentese_0_taban", "TC:onyuz_cerceve_mek_sol_dikme"),
           ("TC:onyuz_mekanizma_kanadi_sol_basac", "TC:onyuz_cerceve_mek_ust_kayit"), ("TC:onyuz_mekanizma_kanadi_sag_basac", "TC:onyuz_cerceve_mek_ust_kayit"),
           ("TU:kasar_cad_v14_yarik_dili", "TU:kasar_cad_v14__cikis_tupu"), ("TU:motor_kablosu_kasar_cad_v14_helezon", "TU:motor_kasar_cad_v14_helezon")]
''')
degis('    k("v29 · bağlantılar (%d çift: K1/K2 menteşe tabanı ↔ TC yan sacı · T köşebendi ↔ L dış sacı + dikme · SOĞUK KUTU ↔ TC yan / tavan sacları (yapışık, boşluk yok) · raf burçları ↔ TC yan sacları · alt sac ↔ sensör / silecek askısı · kılavuz ↔ raf · ped ↔ teknik taban · DIN plakası · panel menteşesi · mandallar · yarık dili · kablo rakoru): hepsi ≤ 0,05 mm"',
      '    k("v30 · bağlantılar (%d çift: K1/K2 menteşe tabanı ↔ TC yan sacı · SOĞUK KUTU ↔ TC yan / tavan sacları · raf burçları · alt sac ↔ sensör / silecek askısı · kılavuz ↔ raf · SOĞUTMA GRUBU ped ↔ tepsi ↔ askı ↔ taban · hatlar ↔ ünite · teknik bölme perdeleri · kuru bölme tabanı · pano / DIN / UPS ↔ arka sac · servis kapağı · filtre ↔ kanat · panel menteşesi · mandallar · yarık dili · kablo rakoru): hepsi ≤ 0,05 mm"')
degis('        V24 = importlib.import_module("topping_cad_v28"); V24.PARCALAR[:] = []; V24.modul()',
      '        V24 = importlib.import_module("topping_cad_v29"); V24.PARCALAR[:] = []; V24.modul()      # v30: referans v29')
degis('        k("v29 · kinematik v28 ile aynı (koniler', '        k("v30 · kinematik v29 ile aynı (koniler')
blok("    # 10 · bilgi: A kabini + kaide v2 ile",
     '    print("DUNYA DENETIMI SURESI',
     '''    # 10 · v30 · KAİDE v4 (soğutma grubu cebi + hava pencereleri) ↔ C istasyonu: GERÇEK DENETİM · A kabini BİLGİ
    try:
        import kaide_cad_v4 as KD4
        KD4.kur()
        K_ = [("KAIDE:" + p["ad"], KD4.dunya(p)) for p in KD4.PARCALAR]
        cK = []
        for a, sa in K_:
            ba = sa.BoundingBox()
            for c, sc in W_:
                if _bbk(ba, B_[c]):
                    v = _hacim(sa, sc)
                    if v > 1.0 or v < 0: cK.append((round(v, 1), a, c))
        _es4 = abs(KD4.C_PENCERE_Y[0] - KAIDE_PENCERE_Y[0]) < 0.01 and abs(KD4.C_PENCERE_Y[1] - KAIDE_PENCERE_Y[1]) < 0.01 and KD4.C_PENCERE_X == KAIDE_PENCERE_X
        _es4 = _es4 and any(abs(k_[0] - CU_CEP[0]) < 0.01 and abs(k_[1] - CU_CEP[1]) < 0.01 and abs(k_[2] - CU_CEP[2]) < 0.01 and abs(k_[3] - CU_CEP[3]) < 0.01 for k_ in KD4.C_PLAKA_KESIK)
        k("v30 · kaide_cad_v4 (%d parça · 3. göz 1620–2100 ünite cebi · 4 gözde hava penceresi) ↔ C istasyonu (TC + TU) çakışma %d · pencere / cep ölçüleri TC ile aynı: %s"
          % (len(KD4.PARCALAR), len(cK), "evet" if _es4 else "HAYIR"), not cK and _es4, str(cK[:6]))
    except Exception as e_:
        k("v30 · kaide_cad_v4 denetimi yapılamadı: %s" % str(e_)[:160], False)
    try:
        import acici_kabin_cad_v1 as AK
        AK.kur()
        A_ = [("A:" + p["ad"], AK.dunya(p)) for p in AK.PARCALAR]
        cA = []
        for a, sa in A_:
            ba = sa.BoundingBox()
            for c, sc in W_:
                if _bbk(ba, B_[c]):
                    v = _hacim(sa, sc)
                    if v > 1.0 or v < 0: cA.append((round(v, 1), a, c))
        print("  BİLGİ · A kabini (acici_kabin_cad_v1) ↔ C istasyonu (%d parça) çakışma: %s" % (len(AK.PARCALAR), "TEMİZ" if not cA else "%d BULGU %s" % (len(cA), cA[:6])))
        R.append(("BİLGİ · A kabini ↔ C çakışma %d" % len(cA), True, str(cA[:6])))
    except Exception as e_:
        print("  BİLGİ · A kabini yüklenemedi (%s)" % str(e_)[:100])
''')

# ---------------------------------------------------------------- 5 · __main__
degis('    print("TOPPING MODULU v29 · %d parca', '    print("TOPPING MODULU v30 · %d parca')
degis('b.ymin < ((MEK_PAN_Y0 - DY_D) if a.startswith("onyuz_") else 0.0) - 0.01', 'b.ymin < ((MEK_PAN_Y0 - DY_D) if a.startswith(("onyuz_", "sogutma_grubu")) else 0.0) - 0.01')
degis('_pn = {a: (round(b.zmin, 2), round(b.zmax, 2)) for a, b in bb if a in ("onyuz_mekanizma_kanadi_sol", "onyuz_mekanizma_kanadi_sag", "onyuz_T_kapagi")}',
      '_pn = {a: (round(b.zmin, 2), round(b.zmax, 2)) for a, b in bb if a in ("onyuz_mekanizma_kanadi_sol", "onyuz_mekanizma_kanadi_sag")}   # v30: T kapağı yok')
degis("    assert len(_pn) == 3 and all(", "    assert len(_pn) == 2 and all(")

for _yasak in ("TEK_TABAN_D", "TEK_PED", "CU_KLF", "T_Y[", "onyuz_T_kapagi\"", "teknik_ayirma_saci"):
    _kal = [l_ for l_ in s.splitlines() if _yasak in l_ and not l_.lstrip().startswith("#")]
    _kal = [l_ for l_ in _kal if "_eski_tek" not in l_ and "TU:teknik_ayirma" not in l_]
    assert not _kal, (_yasak, [l_[:120] for l_ in _kal[:4]])
compile(s, "topping_cad_v30.py", "exec")
io.open(os.path.join(U, "topping_cad_v30.py"), "w", encoding="utf-8").write(s)
print("topping_cad_v30.py yazıldı · %d satır" % s.count("\n"))
