# -*- coding: utf-8 -*-
"""kutu_cad_v4 → kutu_cad_v5 (27 Eyl 2026): ALÇAK HAT (SPEC_alcak_hat_v57.md · Kemal: "bu teknik resme göre 3D modelle").
E modülünden y 400–568 arasındaki YATAY DİLİM çıkarıldı (her şey 168 aşağı, makine üstü 2030 → 1862):
  · bant seçimi: asansör arabası üstü 300 < 400 ve şarjör kapısı kulpu altı 640 > 568 → bandın içinde biten parça YOK;
    bandı boydan boya geçen 20 parça (kabuk sacları, ön dikmeler, şarjör kılavuzları, kapı eşiği, karton yığını, asansör ray plakası,
    2 HGR15, Tr16×4 vida, alt dikey kablo kanalı) 168 kısalır, üstündeki her şey 168 iner, altı (ayak, taban, asansör + tahriki) yerinde.
  · parçalar YENİ KOTLARDA doğrudan kurulur (sabitler + fonksiyonlardaki mutlak y değerleri yeniden bağlandı); dilim_v1 v4'ü dilimleyip
    v5 ile parça parça karşılaştırır (olcum_v5: sınır kutusu ±0,01 · hacim) → hiçbir kot kaçmadı. HGR15 asansör rayları katalog delik
    deseniyle (P60, uçtan 20) 822 boyda yeniden açılır → yalnız sınır kutusu karşılaştırılır.
  · kotlar: TEPSİ 1104 → 936 · KALIP 981,5 · YB 981,6 · PLAKA_K 996 · ALT RAF 618–622 · şarjör yığını 240–980 = 462 kutu (@1,6)
    · H_UST 1310 · KOL_P (560, 912) · PARMAK_P (88, 1092) · Y_BES_PL 1332 · H_BEKLE 1299 · kafa() 2. vuruş TEPSI + 4 (= 940; v4'te
    1108,0 sabit yazılıydı) · blank_acilar() ön ray KALIP − 20 (= 961,5; v4 1129,5) · DUGUM menteşeleri YB'den kendiliğinden.
  · YENİ: İÇECEK YEDEĞİ 6 koli (400 × 267 × 123, 24 kutu) 2 sütun × 3 kat: x 3–403 / 405–805 · y 130–499 · z −350…−83 + PE altlık 126–130.
  · BOM metinleri: yığın 740 mm = 462 kutu · asansör rayı boy 822 · Tr16×4 boy 807 · alt raf notu. Çıktılar: kutu_modulu_v5.glb · 5_PACK_kutu_v5.
Önceki: kutu_cad_v4.py"""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "kutu_cad_v4.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:130])
    s = s.replace(a, b)


NL = chr(10)
i = s.index('"""') + 3
s = s[:i] + ("AUTOKITCH · E · KUTU KATLAMA · kutu_cad_v5 (27 Eyl 2026) — ALÇAK HAT (SPEC_alcak_hat_v57): y 400–568 dilimi çıkarıldı, her şey 168 aşağı" + NL +
             "  (üst 1862 · tepsi 936 · alt raf 618–622 · şarjör 240–980 = 462 kutu) + önde İÇECEK YEDEĞİ 6 koli. Üretici: yap_kutu_v5.py. Önceki: kutu_cad_v4.py" + NL) + s[i:]
d("ÇEVRİM: şarjör (asansör yığını 1149,6'da tutar)", "ÇEVRİM: şarjör (asansör yığını YB'de tutar: v5 981,6)")
d("KOORDİNAT (modül yereli): x 0..830 soldan sağa (K tarafı 0) · y 0..2030 zeminden", "KOORDİNAT (modül yereli): x 0..830 soldan sağa (K tarafı 0) · y 0..1862 zeminden (v5 alçak hat)")

# ---------------------------------------------------------------- ÖLÇÜLER ----------------------------------------------------------------
d("W, H, D = 830.0, 2030.0, 830.0", "W, H, D = 830.0, 1862.0, 830.0                 # v5 ALÇAK HAT: 2030 − 168" + NL +
  "DILIM_Y0, DILIM_DY = 400.0, 168.0          # v5: v4'ten çıkarılan yatay dilim y 400–568 (asansör arabası üstü 300 < 400 · şarjör kapısı kulpu altı 640 > 568)")
d("TEPSI = 1104.0                  # kutu tabanının oturduğu yüz (hat süreç zinciri: kesme plakası 1164 − 60)",
  "TEPSI = 936.0                   # kutu tabanının oturduğu yüz (hat süreç zinciri: kesme plakası 996 − 60) · v5: 1104 − 168")
d("KALIP = 1149.5                  # kalıp ray üstleri", "KALIP = 981.5                   # v5 (1149,5 − 168) · kalıp ray üstleri")
d("YB = 1149.6                     # düz blankın alt yüzü", "YB = 981.6                      # v5 (1149,6 − 168) · düz blankın alt yüzü")
d("PLAKA_K = 1164.0                # K kesme plakası üstü (arayüz)",
  "PLAKA_K = 996.0                 # K kesme plakası üstü (arayüz) · v5: kesme_cad_v4.BANT 996" + NL +
  "PENCERE = (PLAKA_K - 18.0, PLAKA_K + 66.0, -372.0, -24.0)   # v5: sol duvardaki pizza penceresi y0 y1 z0 z1 = 978–1062 (v4 1146–1230) · K'nin E_PENCERE'si ile aynı")
d("ALT_RAF_Y = (786.0, 790.0)            # v4: alt raf — mekanizmanın en alt parçası flap katlayıcı motoru 797,5 altında",
  "ALT_RAF_Y = (618.0, 622.0)            # v4: alt raf — mekanizmanın en alt parçası flap katlayıcı motoru 629,5 altında (v5: 786–790 − 168)")
d("Y_YIGIN_UST = YB - T            # 1148,0 · 2. blankın üstü",
  "Y_YIGIN_UST = YB - T            # v5 980,0 · 2. blankın üstü" + NL +
  "SARJOR_ADET = int((Y_YIGIN_UST - Y_PLAT) / T)   # v5: yığın 240–980 = 740 mm → 462 kutu @1,6 (v4 567)")
d("H_UST = 1478.0                  # piston kafası altı (yukarıda bekler; dik kapağın tepesi 1461,4)",
  "H_UST = 1310.0                  # piston kafası altı (yukarıda bekler; dik kapağın tepesi 1293,4) · v5: 1478 − 168")
d("KOL_P = (560.0, 1080.0)         # kapak kolu mili", "KOL_P = (560.0, 912.0)          # kapak kolu mili · v5: 1080 − 168")
d("KMER = (BX1, TEPSI + T / 2.0 + H_ARKA)            # kapak menteşesi (420, 1148,8)", "KMER = (BX1, TEPSI + T / 2.0 + H_ARKA)            # kapak menteşesi (420, 980,8)")
# denetçi: v4'ten kalan eski kot yorumları (değerler türetilmiş, yalnız yorum)
d("Y_KAPI_UST = Y_YIGIN_UST + 0.8                      # 1148,8 · 2. blankı tutar", "Y_KAPI_UST = Y_YIGIN_UST + 0.8                      # 980,8 (v5; v4 1148,8) · 2. blankı tutar")
d("KM_UST = TEPSI + T / 2.0 + H_ARKA - T / 2.0          # 1148,0 · kapak masası üstü", "KM_UST = TEPSI + T / 2.0 + H_ARKA - T / 2.0          # 980,0 (v5; v4 1148,0) · kapak masası üstü")

# ---------------------------------------------------------------- GÖVDE ----------------------------------------------------------------
d("sol = kut(0, SAC, Y_PLINT, H - SAC, -D + SAC, 0).cut(kut(-1, SAC + 1, 1146.0, 1230.0, -372.0, -24.0))             # pizza penceresi",
  "sol = kut(0, SAC, Y_PLINT, H - SAC, -D + SAC, 0).cut(kut(-1, SAC + 1, PENCERE[0], PENCERE[1], PENCERE[2], PENCERE[3]))   # pizza penceresi (v5 978–1062)")
d(".cut(kut(W - SAC - 1, W + 1, 232.0, 1156.0, -822.0, -412.0))  # şarjör yan kapısı", ".cut(kut(W - SAC - 1, W + 1, 232.0, 988.0, -822.0, -412.0))  # şarjör yan kapısı (v5 üstü 1156 − 168)")
d('ekle("sarjor_yan_kapisi", kut(W - SAC, W, 234.0, 1154.0, -820.0, -414.0), "kabuk")', 'ekle("sarjor_yan_kapisi", kut(W - SAC, W, 234.0, 986.0, -820.0, -414.0), "kabuk")')
d('ekle("sarjor_yan_kapisi_kulp", kut(W, W + 22.0, 640.0, 760.0, -440.0, -425.0), "celik")', 'ekle("sarjor_yan_kapisi_kulp", kut(W, W + 22.0, 472.0, 592.0, -440.0, -425.0), "celik")')
d('ekle("on_alt_sac", kut(SAC, W - SAC, Y_PLINT + 3.0, 1085.0, -SAC, 0), "kabuk")', 'ekle("on_alt_sac", kut(SAC, W - SAC, Y_PLINT + 3.0, 917.0, -SAC, 0), "kabuk")')
d('ekle("on_ust_kapak", kut(SAC, W - SAC, 1345.0, H - SAC, -SAC, 0), "kabuk")', 'ekle("on_ust_kapak", kut(SAC, W - SAC, 1177.0, H - SAC, -SAC, 0), "kabuk")')
d('ekle("on_ust_kapak_kulp", kut(380.0, 450.0, 1360.0, 1378.0, 0.0, 18.0), "celik")', 'ekle("on_ust_kapak_kulp", kut(380.0, 450.0, 1192.0, 1210.0, 0.0, 18.0), "celik")')
d('ekle("agiz_ust_kirisi", kut(SAC, W - SAC, 1330.0, 1345.0, -40.0, -20.0), "celik")', 'ekle("agiz_ust_kirisi", kut(SAC, W - SAC, 1162.0, 1177.0, -40.0, -20.0), "celik")')
d("kut(x0, x0 + 20.0, Y_PLINT + 3.0, 1085.0, z0, z0 + 20.0).cut(kut(x0 + (2 if i == 0 else 0), x0 + (20 if i == 0 else 18), Y_PLINT + 2, 1086, z0 - 1, z0 + 18))",
  "kut(x0, x0 + 20.0, Y_PLINT + 3.0, 917.0, z0, z0 + 20.0).cut(kut(x0 + (2 if i == 0 else 0), x0 + (20 if i == 0 else 18), Y_PLINT + 2, 918, z0 - 1, z0 + 18))")

# ---------------------------------------------------------------- ŞARJÖR + ASANSÖR ----------------------------------------------------------------
d('ekle("kilavuz_sol_uhmw", kut(X_BL0 - 3.5, X_BL0 - 0.5, 244.0, 1152.0, ZS0, ZS1), "uhmw",', 'ekle("kilavuz_sol_uhmw", kut(X_BL0 - 3.5, X_BL0 - 0.5, 244.0, 984.0, ZS0, ZS1), "uhmw",')
d('ekle("kilavuz_sag_uhmw", kut(X_BL1 + 0.5, X_BL1 + 3.5, 244.0, 1152.0, ZS0, ZS1), "uhmw", bom=None)', 'ekle("kilavuz_sag_uhmw", kut(X_BL1 + 0.5, X_BL1 + 3.5, 244.0, 984.0, ZS0, ZS1), "uhmw", bom=None)')
d('ekle("kilavuz_sol_tasiyici", kut(SAC, X_BL0 - 3.5, 244.0, 1152.0, -700.0, -680.0), "sac")', 'ekle("kilavuz_sol_tasiyici", kut(SAC, X_BL0 - 3.5, 244.0, 984.0, -700.0, -680.0), "sac")')
d('ekle("kilavuz_sag_tasiyici", kut(X_BL1 + 3.5, W - SAC, 244.0, 1152.0, -700.0, -680.0), "sac")', 'ekle("kilavuz_sag_tasiyici", kut(X_BL1 + 3.5, W - SAC, 244.0, 984.0, -700.0, -680.0), "sac")')
d('ekle("kilavuz_arka_uhmw", kut(X_BL0, X_BL1, 244.0, 1140.0, ZS0 - 3.5, ZS0 - 0.5), "uhmw")', 'ekle("kilavuz_arka_uhmw", kut(X_BL0, X_BL1, 244.0, 972.0, ZS0 - 3.5, ZS0 - 0.5), "uhmw")')
d('ekle("kilavuz_arka_tasiyici", kut(X_BL0 + 40.0, X_BL1 - 40.0, 244.0, 1140.0, -D + SAC, ZS0 - 3.5), "sac")', 'ekle("kilavuz_arka_tasiyici", kut(X_BL0 + 40.0, X_BL1 - 40.0, 244.0, 972.0, -D + SAC, ZS0 - 3.5), "sac")')
d("kapi = kapi.cut(kut(x0 - 2.0, x1 + 2.0, 243.0, 1112.0, Z_KAPI0 - 1, Z_KAPI1 + 1))", "kapi = kapi.cut(kut(x0 - 2.0, x1 + 2.0, 243.0, 944.0, Z_KAPI0 - 1, Z_KAPI1 + 1))")
d('''bom=("Pizza kutusu 32 × 32 × 4,2 E-dalga (düz açılım 804 × 404)", 567, "yığın 908 mm = 567 adet @1,6 · 504 @1,8", "AmbalajPazarı · 100'lü paket (sarf)"))''',
  '''bom=("Pizza kutusu 32 × 32 × 4,2 E-dalga (düz açılım 804 × 404)", SARJOR_ADET, "yığın %.0f mm = %d adet @1,6 · %d @1,8 (v5 alçak hat; + fırın üstü yedek 320)"
              % (Y_YIGIN_UST - Y_PLAT, SARJOR_ADET, int((Y_YIGIN_UST - Y_PLAT) / 1.8)), "AmbalajPazarı · 100'lü paket (sarf)"))''')
d('ekle("asansor_ray_plakasi", kut(200.0, 600.0, 150.0, 1140.0, -378.0, -374.0), "sac")', 'ekle("asansor_ray_plakasi", kut(200.0, 600.0, 150.0, 972.0, -378.0, -374.0), "sac")')
d('hgr15("asansor_rayi_%d" % i, 990.0, (xr, 150.0, -378.0), (0, 1, 0), (0, 0, -1),', 'hgr15("asansor_rayi_%d" % i, 822.0, (xr, 150.0, -378.0), (0, 1, 0), (0, 0, -1),')
d('bom=("Lineer ray HIWIN HGR15R", 2, "asansör · boy 990", "hiwin.com")', 'bom=("Lineer ray HIWIN HGR15R", 2, "asansör · boy 822 (v5)", "hiwin.com")')
d('ekle("asansor_vidasi_Tr16x4", sily(405.0, -392.0, 8.0, 150.0, 1125.0), "celik",', 'ekle("asansor_vidasi_Tr16x4", sily(405.0, -392.0, 8.0, 150.0, 957.0), "celik",')
d('"boy 975 + Ø12 alt uç 42', '"boy 807 (v5) + Ø12 alt uç 42')
d('for ad_, y0 in (("asansor_alt_yatak", 150.0), ("asansor_ust_yatak", 1125.0)):', 'for ad_, y0 in (("asansor_alt_yatak", 150.0), ("asansor_ust_yatak", 957.0)):')

# ---------------------------------------------------------------- BESLEYİCİ ----------------------------------------------------------------
d("Y_BES_PL = 1500.0                # besleyici üst plakası altı — dik kapağın (flapıyla 1466) ÜSTÜNDE",
  "Y_BES_PL = 1332.0                # v5 (1500 − 168) · besleyici üst plakası altı — dik kapağın (flapıyla 1298) ÜSTÜNDE")
d('ekle("itici_asma_plakasi_%d" % i, kut(xr - 20.0, xr + 20.0, 1176.2, Y_BES_PL - 34.0, -826.0, -818.0), "aluminyum", "ITICI")',
  'ekle("itici_asma_plakasi_%d" % i, kut(xr - 20.0, xr + 20.0, 1008.2, Y_BES_PL - 34.0, -826.0, -818.0), "aluminyum", "ITICI")')
d('ekle("itici_kirisi_40x20", kut(10.0, 810.0, 1156.2, 1176.2, -826.0, -819.5), "aluminyum", "ITICI")', 'ekle("itici_kirisi_40x20", kut(10.0, 810.0, 988.2, 1008.2, -826.0, -819.5), "aluminyum", "ITICI")')
d('ekle("itici_cubugu", kut(10.0, 810.0, YB + 0.6, 1156.2, -826.0, -819.5), "celik", "ITICI",', 'ekle("itici_cubugu", kut(10.0, 810.0, YB + 0.6, 988.2, -826.0, -819.5), "celik", "ITICI",')
d('"alt kenarı 1150,2: yalnız EN ÜSTTEKİ blankı yakalar (1149,6–1151,2)"', '"alt kenarı 982,2: yalnız EN ÜSTTEKİ blankı yakalar (981,6–983,2)"')

# ---------------------------------------------------------------- KALIP + TEPSİ ----------------------------------------------------------------
d('ekle("kalip_tablasi_6", kut(90.0, 430.0, 1080.0, 1086.0, -372.5, -32.0), "sac")', 'ekle("kalip_tablasi_6", kut(90.0, 430.0, 912.0, 918.0, -372.5, -32.0), "sac")')
d("kut(xp - 20.0, xp + 20.0, ALT_RAF_Y[1], 1080.0, zp - 20.0, zp + 20.0).cut(kut(xp - 17.8, xp + 17.8, ALT_RAF_Y[1] - 1, 1081, zp - 17.8, zp + 17.8))",
  "kut(xp - 20.0, xp + 20.0, ALT_RAF_Y[1], 912.0, zp - 20.0, zp + 20.0).cut(kut(xp - 17.8, xp + 17.8, ALT_RAF_Y[1] - 1, 913, zp - 17.8, zp + 17.8))")
d('"boy %.0f (v4: alt rafta biter)" % (1080.0 - ALT_RAF_Y[1])', '"boy %.0f (v4: alt rafta biter)" % (912.0 - ALT_RAF_Y[1])')
d('"v4: kalıp + kapak plakası ayakları üstünde · altı boş (≈ 796 × 630 × 348)"',
  '"v4: kalıp + kapak plakası ayakları üstünde · v5: altı 126–588, önde içecek yedeği 6 koli (x 3–805 · y 130–499 · z −350…−83)"')
d("b = kut(x0, x1, 1096.0, TEPSI, BZ0, BZ1)", "b = kut(x0, x1, 928.0, TEPSI, BZ0, BZ1)")
d("b = b.cut(kut(x0 - 1, x0 + 32.0, 1094.0, TEPSI + 1, z0 - 2.0, z1 + 2.0))", "b = b.cut(kut(x0 - 1, x0 + 32.0, 926.0, TEPSI + 1, z0 - 2.0, z1 + 2.0))")
d('ekle("tepsi_ayagi_%d" % i, kut((x0 + x1) / 2.0 - 8.0, (x0 + x1) / 2.0 + 8.0, 1086.0, 1096.0, ZB - 8.0, ZB + 8.0), "sac")',
  'ekle("tepsi_ayagi_%d" % i, kut((x0 + x1) / 2.0 - 8.0, (x0 + x1) / 2.0 + 8.0, 918.0, 928.0, ZB - 8.0, ZB + 8.0), "sac")')
d('ekle("kalip_rayi_arka_z", kut(BX0, 405.0, 1086.0, KALIP, BZ0 - T - 6.0, BZ0 - T - 0.5), "sac",', 'ekle("kalip_rayi_arka_z", kut(BX0, 405.0, 918.0, KALIP, BZ0 - T - 6.0, BZ0 - T - 0.5), "sac",')
d('ekle("kalip_taragi_on_z_%d" % i, kut(max(x0, BX0), min(x1, 405.0), 1086.0, KALIP, BZ1 + T + 0.5, BZ1 + T + 6.5), "sac",',
  'ekle("kalip_taragi_on_z_%d" % i, kut(max(x0, BX0), min(x1, 405.0), 918.0, KALIP, BZ1 + T + 0.5, BZ1 + T + 6.5), "sac",')
d('ekle("kalip_on_x_rayi", kut(93.4, 97.9, 1086.0, 1129.5, BZ0, BZ1), "sac",', 'ekle("kalip_on_x_rayi", kut(93.4, 97.9, 918.0, KALIP - 20.0, BZ0, BZ1), "sac",')
d('ekle("kalip_arka_x_dayagi", kut(BX1 + T + 0.5, BX1 + T + 6.5, 1086.0, TEPSI + 8.0, BZ0, BZ1), "sac")', 'ekle("kalip_arka_x_dayagi", kut(BX1 + T + 0.5, BX1 + T + 6.5, 918.0, TEPSI + 8.0, BZ0, BZ1), "sac")')

# ---------------------------------------------------------------- KÖPRÜ ----------------------------------------------------------------
d('ekle("kopru_tasiyici", kut(30.0, 64.0, 1080.0, KALIP - 3.0 - KOPRU_ALT, ZB - 40.0, ZB + 40.0).cut(sily(47.0, ZB, 9.0, 1079, 1120)), "aluminyum", "KOPRU")',
  'ekle("kopru_tasiyici", kut(30.0, 64.0, 912.0, KALIP - 3.0 - KOPRU_ALT, ZB - 40.0, ZB + 40.0).cut(sily(47.0, ZB, 9.0, 911, 952)), "aluminyum", "KOPRU")')
d('ekle("kopru_kilavuz_mili_%d" % i, sily(47.0, zc, 6.0, 950.0, KALIP - 3.0 - KOPRU_ALT), "celik", "KOPRU",', 'ekle("kopru_kilavuz_mili_%d" % i, sily(47.0, zc, 6.0, 782.0, KALIP - 3.0 - KOPRU_ALT), "celik", "KOPRU",')
d('ekle("kopru_burcu_%d" % i, boru_y(47.0, zc, 10.5, 6.1, 985.0, 1015.0), "celik")', 'ekle("kopru_burcu_%d" % i, boru_y(47.0, zc, 10.5, 6.1, 817.0, 847.0), "celik")')
d("bp = kut(20.0, 74.0, 1015.0, 1021.0, BZ0 + 20.0, BZ1 - 20.0)", "bp = kut(20.0, 74.0, 847.0, 853.0, BZ0 + 20.0, BZ1 - 20.0)")
d("bp = bp.cut(sily(47.0, zc, 6.3, 1014, 1022))", "bp = bp.cut(sily(47.0, zc, 6.3, 846, 854))")
d('ekle("kopru_burc_plakasi", bp.cut(sily(47.0, ZB, 9.0, 1014, 1022)), "aluminyum")', 'ekle("kopru_burc_plakasi", bp.cut(sily(47.0, ZB, 9.0, 846, 854)), "aluminyum")')
d('ekle("kopru_plaka_tutucu", kut(SAC, 16.0, 1000.0, 1021.0, BZ0 + 20.0, BZ1 - 20.0), "aluminyum")', 'ekle("kopru_plaka_tutucu", kut(SAC, 16.0, 832.0, 853.0, BZ0 + 20.0, BZ1 - 20.0), "aluminyum")')
d('sfu16("kopru_vidasi", 47.0, ZB, 1000.0, 1112.0, 5, "KOPRU", 1023.0)', 'sfu16("kopru_vidasi", 47.0, ZB, 832.0, 944.0, 5, "KOPRU", 855.0)')
d('bk12("kopru_BK12", 47.0, ZB, 982.5, 1)', 'bk12("kopru_BK12", 47.0, ZB, 814.5, 1)')
d('kaplin("kopru_kaplini", 47.0, 952.5, ZB)', 'kaplin("kopru_kaplini", 47.0, 784.5, ZB)')
d('nema23("kopru_motoru", (47.0, 952.5, ZB), (0, 1, 0), (0, 0, 1))', 'nema23("kopru_motoru", (47.0, 784.5, ZB), (0, 1, 0), (0, 0, 1))')
d('ekle("kopru_motor_braketi", kut(17.0, 77.0, 952.5, 958.5, ZB - 30.0, ZB + 30.0).cut(sily(47.0, ZB, 20.0, 951, 960)), "aluminyum")',
  'ekle("kopru_motor_braketi", kut(17.0, 77.0, 784.5, 790.5, ZB - 30.0, ZB + 30.0).cut(sily(47.0, ZB, 20.0, 783, 792)), "aluminyum")')
d('ekle("kopru_motor_askisi", kut(SAC, 16.0, 952.5, 1000.0, ZB - 30.0, ZB + 30.0), "aluminyum")', 'ekle("kopru_motor_askisi", kut(SAC, 16.0, 784.5, 832.0, ZB - 30.0, ZB + 30.0), "aluminyum")')
d('e2e("kopru_alt_sensor", 72.0, 1030.0, ZB + 34.0, "y")', 'e2e("kopru_alt_sensor", 72.0, 862.0, ZB + 34.0, "y")')

# ---------------------------------------------------------------- PİSTON ----------------------------------------------------------------
d('ekle("piston_eksen_plakasi", kut(170.0, 370.0, 1500.0, 2015.0, -394.0, -389.0), "aluminyum")', 'ekle("piston_eksen_plakasi", kut(170.0, 370.0, 1332.0, 1847.0, -394.0, -389.0), "aluminyum")')
d('ekle("piston_eksen_askisi", kut(170.0, 370.0, 2015.0, H - SAC, -394.0, -380.0), "aluminyum")', 'ekle("piston_eksen_askisi", kut(170.0, 370.0, 1847.0, H - SAC, -394.0, -380.0), "aluminyum")')
d('hgr15("piston_rayi_%d" % i, 515.0, (xr, 1500.0, -389.0), (0, 1, 0), (0, 0, 1),', 'hgr15("piston_rayi_%d" % i, 515.0, (xr, 1332.0, -389.0), (0, 1, 0), (0, 0, 1),')
d('sfu16("piston_vidasi", 270.0, -325.0, 1515.0, 2008.0, 10, "PISTON", h + 417.0)', 'sfu16("piston_vidasi", 270.0, -325.0, 1347.0, 1840.0, 10, "PISTON", h + 417.0)')
d('bk12("piston_BK12", 270.0, -325.0, 1958.0, 1)', 'bk12("piston_BK12", 270.0, -325.0, 1790.0, 1)')
d('ekle("piston_BK_askisi_%d" % i, kut(240.0, 300.0, 1990.5, H - SAC, z0, z1), "aluminyum")', 'ekle("piston_BK_askisi_%d" % i, kut(240.0, 300.0, 1822.5, H - SAC, z0, z1), "aluminyum")')
d('pd1 = kasnak("piston_kasnak_vida", 270.0, 1995.5, -325.0, 20)', 'pd1 = kasnak("piston_kasnak_vida", 270.0, 1827.5, -325.0, 20)')
d('pd2 = kasnak("piston_kasnak_motor", 340.0, 1995.5, -318.0, 20)', 'pd2 = kasnak("piston_kasnak_motor", 340.0, 1827.5, -318.0, 20)')
d('kayis_y("piston_kayisi", 270.0, -325.0, 340.0, -318.0, 1996.5, pd1, pd2)', 'kayis_y("piston_kayisi", 270.0, -325.0, 340.0, -318.0, 1828.5, pd1, pd2)')
d('nema23("piston_motoru", (340.0, 1990.0, -318.0), (0, 1, 0), (0, 0, 1))', 'nema23("piston_motoru", (340.0, 1822.0, -318.0), (0, 1, 0), (0, 0, 1))')
d('ekle("piston_motor_braketi", kut(308.0, 372.0, 1990.0, 1994.0, -350.0, -286.0).cut(sily(340.0, -318.0, 20.0, 1989, 1995)), "aluminyum")',
  'ekle("piston_motor_braketi", kut(308.0, 372.0, 1822.0, 1826.0, -350.0, -286.0).cut(sily(340.0, -318.0, 20.0, 1821, 1827)), "aluminyum")')
d('ekle("piston_motor_askisi_%d" % i, kut(x0, x1, 1994.0, H - SAC, -350.0, -336.0), "aluminyum")', 'ekle("piston_motor_askisi_%d" % i, kut(x0, x1, 1826.0, H - SAC, -350.0, -336.0), "aluminyum")')
d('e2e("piston_ust_sensor", 385.0, 1950.0, -389.0 + 2.0, "z")', 'e2e("piston_ust_sensor", 385.0, 1782.0, -389.0 + 2.0, "z")')

# ---------------------------------------------------------------- PARMAK ----------------------------------------------------------------
d("PARMAK_P = (88.0, 1260.0)", "PARMAK_P = (88.0, 1092.0)       # v5: 1260 − 168")

# ---------------------------------------------------------------- KAPAK MEKANİZMASI ----------------------------------------------------------------
d('ekle("kapak_masasi_diregi_%d" % i, sily(600.0, zc, 8.0, 1000.0, KM_UST - 3.0), "celik")', 'ekle("kapak_masasi_diregi_%d" % i, sily(600.0, zc, 8.0, 832.0, KM_UST - 3.0), "celik")')
d('ekle("kapak_alt_plakasi", kut(440.0, 800.0, 994.0, 1000.0, -368.0, BZ1 + 20.0).cut(sily(750.0, -300.0, 15.0, 993, 1001)), "aluminyum")',
  'ekle("kapak_alt_plakasi", kut(440.0, 800.0, 826.0, 832.0, -368.0, BZ1 + 20.0).cut(sily(750.0, -300.0, 15.0, 825, 833)), "aluminyum")')
d('ekle("kapak_alt_plaka_ayagi_0", kut(780.0, 800.0, ALT_RAF_Y[1], 994.0, -368.0, -348.0), "aluminyum")', 'ekle("kapak_alt_plaka_ayagi_0", kut(780.0, 800.0, ALT_RAF_Y[1], 826.0, -368.0, -348.0), "aluminyum")')
d('ekle("kapak_alt_plaka_ayagi_1", kut(780.0, 800.0, ALT_RAF_Y[1], 994.0, BZ1, BZ1 + 20.0), "aluminyum")', 'ekle("kapak_alt_plaka_ayagi_1", kut(780.0, 800.0, ALT_RAF_Y[1], 826.0, BZ1, BZ1 + 20.0), "aluminyum")')
d("uc = kut(466.0, xa + 3.0, 1112.0, KM_UST, ZL0 - 3.0 - T, ZL0 - T)", "uc = kut(466.0, xa + 3.0, 944.0, KM_UST, ZL0 - 3.0 - T, ZL0 - T)")
d("uc = uc.union(kut(466.0, xa + 3.0, 1112.0, KM_UST, ZL1 + T, ZL1 + 3.0 + T))", "uc = uc.union(kut(466.0, xa + 3.0, 944.0, KM_UST, ZL1 + T, ZL1 + 3.0 + T))")
d("uc = uc.union(kut(xa, xa + 3.0, 1112.0, KM_UST, ZL0 - 3.0 - T, ZL1 + 3.0 + T))", "uc = uc.union(kut(xa, xa + 3.0, 944.0, KM_UST, ZL0 - 3.0 - T, ZL1 + 3.0 + T))")
d('ekle("flap_katlayici_alt_bagi", kut(xa + 3.0, xa + 18.0, 1058.0, 1112.0, ZL0 - 3.0 - T, ZL1 + 3.0 + T).cut(sily(750.0, -300.0, 10.0, 1050, 1120)), "aluminyum", "KATLAYICI")',
  'ekle("flap_katlayici_alt_bagi", kut(xa + 3.0, xa + 18.0, 890.0, 944.0, ZL0 - 3.0 - T, ZL1 + 3.0 + T).cut(sily(750.0, -300.0, 10.0, 882, 952)), "aluminyum", "KATLAYICI")')
d('ekle("flap_katlayici_somun_kolu", kut(xa + 3.0, 770.0, 1058.0, 1068.0, -330.0, -270.0).cut(sily(750.0, -300.0, 8.2, 1050, 1070)), "aluminyum", "KATLAYICI")',
  'ekle("flap_katlayici_somun_kolu", kut(xa + 3.0, 770.0, 890.0, 900.0, -330.0, -270.0).cut(sily(750.0, -300.0, 8.2, 882, 902)), "aluminyum", "KATLAYICI")')
d('sfu16("flap_katlayici_vidasi", 750.0, -300.0, 900.0, 1100.0, 5, "KATLAYICI", 1001.0)', 'sfu16("flap_katlayici_vidasi", 750.0, -300.0, 732.0, 932.0, 5, "KATLAYICI", 833.0)')
d('nema23("flap_katlayici_motoru", (750.0, 862.0, -300.0), (0, 1, 0), (0, 0, 1))', 'nema23("flap_katlayici_motoru", (750.0, 694.0, -300.0), (0, 1, 0), (0, 0, 1))')
d('kaplin("flap_katlayici_kaplini", 750.0, 862.0, -300.0)', 'kaplin("flap_katlayici_kaplini", 750.0, 694.0, -300.0)')
d('ekle("flap_katlayici_motor_braketi", kut(720.0, 780.0, 862.0, 868.0, -330.0, -270.0).cut(sily(750.0, -300.0, 20.0, 861, 869)), "aluminyum")',
  'ekle("flap_katlayici_motor_braketi", kut(720.0, 780.0, 694.0, 700.0, -330.0, -270.0).cut(sily(750.0, -300.0, 20.0, 693, 701)), "aluminyum")')
d('ekle("flap_katlayici_yatak_braketi", kut(720.0, 780.0, 892.0, 900.0, -330.0, -270.0).cut(sily(750.0, -300.0, 6.0, 891, 901)), "aluminyum")',
  'ekle("flap_katlayici_yatak_braketi", kut(720.0, 780.0, 724.0, 732.0, -330.0, -270.0).cut(sily(750.0, -300.0, 6.0, 723, 733)), "aluminyum")')
d('ekle("flap_katlayici_braket_ayagi", kut(780.0, 790.0, 862.0, 994.0, -330.0, -270.0), "aluminyum")', 'ekle("flap_katlayici_braket_ayagi", kut(780.0, 790.0, 694.0, 826.0, -330.0, -270.0), "aluminyum")')
d('e2e("flap_katlayici_sensor", 700.0, 1030.0, -300.0, "y")', 'e2e("flap_katlayici_sensor", 700.0, 862.0, -300.0, "y")')
d('ekle("kol_yatak_ayagi_%d" % i, kut(px - 18.0, px + 18.0, 1000.0, py - 18.0, z0, z1), "aluminyum")', 'ekle("kol_yatak_ayagi_%d" % i, kut(px - 18.0, px + 18.0, 832.0, py - 18.0, z0, z1), "aluminyum")')
d('ekle("kol_reduktor_braketi", kut(px - 30.0, px + 30.0, 1000.0, py - 29.0, -150.0, -140.0), "aluminyum")', 'ekle("kol_reduktor_braketi", kut(px - 30.0, px + 30.0, 832.0, py - 29.0, -150.0, -140.0), "aluminyum")')

# ---------------------------------------------------------------- ELEKTRİK ----------------------------------------------------------------
d('ekle("pano_plakasi", kut(60.0, 780.0, 1565.0, 2025.0, -826.0, -822.0), "sac")', 'ekle("pano_plakasi", kut(60.0, 780.0, 1397.0, 1857.0, -826.0, -822.0), "sac")')
d("for i, y in enumerate((1645.0, 1865.0)):", "for i, y in enumerate((1477.0, 1697.0)):                      # v5: − 168")
d("kut(80.0, 190.0, 1612.5, 1712.5, zd, zd + 75.0)", "kut(80.0, 190.0, 1444.5, 1544.5, zd, zd + 75.0)")
d("kut(194.0, 239.0, 1612.5, 1712.5, zd, zd + 75.0)", "kut(194.0, 239.0, 1444.5, 1544.5, zd, zd + 75.0)")
d("kut(243.0, 288.0, 1612.5, 1712.5, zd, zd + 75.0)", "kut(243.0, 288.0, 1444.5, 1544.5, zd, zd + 75.0)")
d("TC.din_parca(TC.GUC_STEP, x, 1600.0, zd + 122.8 + 0.0)", "TC.din_parca(TC.GUC_STEP, x, 1432.0, zd + 122.8 + 0.0)")
d("TC.din_parca(TC.SURUCU_STEP, x, 1855.0, zd + 28.0)", "TC.din_parca(TC.SURUCU_STEP, x, 1687.0, zd + 28.0)")
d('ekle("klemens_sirasi", kut(450.0, 760.0, 1867.0, 1913.0, zd, zd + 45.0), "plastik",', 'ekle("klemens_sirasi", kut(450.0, 760.0, 1699.0, 1745.0, zd, zd + 45.0), "plastik",')
d("enumerate(((70.0, 770.0, 1745.0, 1785.0), (70.0, 770.0, 1965.0, 2005.0))):", "enumerate(((70.0, 770.0, 1577.0, 1617.0), (70.0, 770.0, 1797.0, 1837.0))):")
d('ekle("kablo_kanali_dikey_alt", kut(801.0, 826.0, Y_PLINT + 3.0, 1325.0, -50.0, -25.0), "plastik")', 'ekle("kablo_kanali_dikey_alt", kut(801.0, 826.0, Y_PLINT + 3.0, 1157.0, -50.0, -25.0), "plastik")')
d('ekle("kablo_kanali_dikey_ust", kut(801.0, 826.0, 1345.0, 1995.0, -50.0, -25.0), "plastik")', 'ekle("kablo_kanali_dikey_ust", kut(801.0, 826.0, 1177.0, 1827.0, -50.0, -25.0), "plastik")')
d('e3z("sensor_yigin_ustu", 770.0, 1190.0, -800.0)', 'e3z("sensor_yigin_ustu", 770.0, 1022.0, -800.0)')
d('e3z("sensor_blank_var", 790.0, 1190.0, -216.0)', 'e3z("sensor_blank_var", 790.0, 1022.0, -216.0)')
d('e3z("sensor_kutu_dolu", SAC + 1.0, 1236.0, -250.0)', 'e3z("sensor_kutu_dolu", SAC + 1.0, 1068.0, -250.0)')

# ---------------------------------------------------------------- ROBOT ÇATALI (referans) ----------------------------------------------------------------
d('ekle("robot_catal_disi_%d" % i, kut(x0, x1, 1094.0, 1102.0, BZ0 + 2.0 + CATAL_DIS, 60.0 + CATAL_DIS), "robot", "CATAL")',
  'ekle("robot_catal_disi_%d" % i, kut(x0, x1, 926.0, 934.0, BZ0 + 2.0 + CATAL_DIS, 60.0 + CATAL_DIS), "robot", "CATAL")')
d('ekle("robot_catal_govdesi", kut(140.0, 380.0, 1080.0, 1112.0, 60.0 + CATAL_DIS, 76.0 + CATAL_DIS), "robot", "CATAL",',
  'ekle("robot_catal_govdesi", kut(140.0, 380.0, 912.0, 944.0, 60.0 + CATAL_DIS, 76.0 + CATAL_DIS), "robot", "CATAL",')
d('ekle("robot_flansi", silz(260.0, 1096.0, 31.5, 76.0 + CATAL_DIS, 96.0 + CATAL_DIS), "robot", "CATAL")', 'ekle("robot_flansi", silz(260.0, 928.0, 31.5, 76.0 + CATAL_DIS, 96.0 + CATAL_DIS), "robot", "CATAL")')

# ---------------------------------------------------------------- KİNEMATİK (mutlak kotlar göreli) ----------------------------------------------------------------
d("Z_KAFA_HAZIR = (10.6, 10.9)       # kafa dik kapağın üstüne (1462)", "Z_KAFA_HAZIR = (10.6, 10.9)       # kafa dik kapağın üstüne (H_BEKLE)")
d("H_BEKLE = 1467.0                 # dik kapak 85°'de: ön flap ucu 1464,3",
  "H_BEKLE = 1299.0                 # dik kapak 85°'de: ön flap ucu 1296,3 · v5: 1467 − 168" + NL +
  "Y_VURUS2 = TEPSI + 4.0           # v5: 2. vuruşta kafa alt yüzü = 940 (v4'te kafa() içinde sabit 1108,0 = TEPSI 1104 + 4 yazılıydı)")
d("    if t < Z_VURUS2[1]: return H_UST + (1108.0 - H_UST) * ss(Z_VURUS2[0], Z_VURUS2[1], t)", "    if t < Z_VURUS2[1]: return H_UST + (Y_VURUS2 - H_UST) * ss(Z_VURUS2[0], Z_VURUS2[1], t)")
d("    if t < Z_VURUS2[2]: return 1108.0", "    if t < Z_VURUS2[2]: return Y_VURUS2")
d("    if t < Z_VURUS2[3]: return 1108.0 + (H_UST - 1108.0) * ss(Z_VURUS2[2], Z_VURUS2[3], t)", "    if t < Z_VURUS2[3]: return Y_VURUS2 + (H_UST - Y_VURUS2) * ss(Z_VURUS2[2], Z_VURUS2[3], t)")
d("    # yan duvarlar: arka ray / ön tarak iç üst köşesi (1149,5; kıvrımdan 2,1 mm dışarıda)", "    # yan duvarlar: arka ray / ön tarak iç üst köşesi (KALIP; kıvrımdan 2,1 mm dışarıda)")
d("    # ön dış duvar: ön ray 20 mm alçak (1129,5) → tırnaklardan SONRA kalkar; kilitlenince 90°" + NL + "    th_f = _ray_uzeri(u, 1129.5, 2.1)",
  "    # ön dış duvar: ön ray 20 mm alçak (KALIP − 20; v4 1129,5 sabitti) → tırnaklardan SONRA kalkar; kilitlenince 90°" + NL + "    th_f = _ray_uzeri(u, KALIP - 20.0, 2.1)")

# ---------------------------------------------------------------- İÇECEK YEDEĞİ (yeni) ----------------------------------------------------------------
ICECEK = '''

# ---------------------------------------------------------------- İÇECEK YEDEĞİ (v5 · ALÇAK HAT) ----------------------------------------------------------------
# SPEC_alcak_hat_v57 · Resim 1 v4: E altı önde 6 koli (24 kutu) 2 sütun × 3 kat → dolaptaki 144 + 144 = 288 (4 gün 277).
# Ön köşe dikmeleri (z −21,5…−1,5) ve kablo_kanali_dikey_alt (x 801–826 · z −50…−25) önde olduğu için koliler geride: z −350…−83.
# Arkada ilk engel asansör ray plakası (z −374); üstte alt raf köşebentleri (alt yüz 588); 4. kat sığmaz (130 + 4 × 123 = 622 > 588).
KOLI = dict(x=400.0, y=123.0, z=267.0, kutu=24)          # koli 400 × 267 × 123 · 24 kutu [VARSAYIM: ölçü resimden, üretici kolisi teyit edilmedi]
ICECEK_X = ((3.0, 403.0), (405.0, 805.0))               # 2 sütun (aralarında 2 mm)
ICECEK_Y0, ICECEK_KAT = 130.0, 3                         # koli tabanı 130 (altlık 126–130) · 3 kat → üst 499
ICECEK_Z = (-350.0, -83.0)
ICECEK_ALTLIK_Y = (Y_PLINT + 3.0, ICECEK_Y0)             # PE-HD altlık 4 mm (taban sacı üstü 126 → koli 130) [VARSAYIM]
ICECEK_YEDEK = dict(x=(ICECEK_X[0][0], ICECEK_X[-1][1]), y=(ICECEK_Y0, ICECEK_Y0 + ICECEK_KAT * KOLI["y"]), z=ICECEK_Z,
                    koli=len(ICECEK_X) * ICECEK_KAT, kutu=len(ICECEK_X) * ICECEK_KAT * KOLI["kutu"])   # montaj için özet (E yereli)


def icecek_yedegi():
    """v5: içecek yedeği — soğutmasız, önde (ön alt sac arkasında) · E_SARJOR'un önü, alt rafın altı"""
    ekle("icecek_yedek_altligi", kut(ICECEK_X[0][0], ICECEK_X[-1][1], ICECEK_ALTLIK_Y[0], ICECEK_ALTLIK_Y[1], ICECEK_Z[0], ICECEK_Z[1]), "plastik",
         bom=("Koli altlığı PE-HD 4 mm (içecek yedeği)", 1, "%.0f × %.0f" % (ICECEK_X[-1][1] - ICECEK_X[0][0], ICECEK_Z[1] - ICECEK_Z[0]), "VARSAYIM · levha kesim"))
    for s_, (x0, x1) in enumerate(ICECEK_X):
        for k_ in range(ICECEK_KAT):
            y0 = ICECEK_Y0 + k_ * KOLI["y"]
            ekle("icecek_yedek_koli_%d%d" % (s_, k_), kut(x0, x1, y0, y0 + KOLI["y"], ICECEK_Z[0], ICECEK_Z[1]), "karton",
                 bom=("İçecek kolisi 24 kutu (yedek, soğutmasız)", ICECEK_YEDEK["koli"], "400 × 267 × 123 · %d kutu" % ICECEK_YEDEK["kutu"],
                      "sarf · koli ölçüsü VARSAYIM (resim)") if s_ == 0 and k_ == 0 else None)
'''
d("\n\n# ---------------------------------------------------------------- BLANK (hareketli kutu ağacı)", ICECEK + "\n\n# ---------------------------------------------------------------- BLANK (hareketli kutu ağacı)")
d("    govde(); sarjor(); besleyici(); kalip(); kopru(); piston(); parmak(); kapak_mekanizmasi(); elektrik(); blank(); catal_pizza()",
  "    govde(); sarjor(); besleyici(); kalip(); kopru(); piston(); parmak(); kapak_mekanizmasi(); elektrik(); icecek_yedegi(); blank(); catal_pizza()")
d('"Destek B", "KFL", "LM12", "Alüminyum profil", "DIN ray", "Klemens", "Kablo kanalı", "UHMW", "Pizza kutusu", "FR5")',
  '"Destek B", "KFL", "LM12", "Alüminyum profil", "DIN ray", "Klemens", "Kablo kanalı", "UHMW", "Pizza kutusu", "FR5", "İçecek kolisi")')
d('r"^guc_48V_NDR-240-48_b$", r"^surucu_STP-DRV-4830_[1-6]$", r"^din_rayi_1$", r"^kablo_kanali_(1|dikey_alt|dikey_ust)$"]',
  'r"^guc_48V_NDR-240-48_b$", r"^surucu_STP-DRV-4830_[1-6]$", r"^din_rayi_1$", r"^kablo_kanali_(1|dikey_alt|dikey_ust)$",' + NL +
  '             r"^icecek_yedek_koli_(0[12]|1[012])$"]')

# ---------------------------------------------------------------- v5 ÖLÇÜM (dilim eşdeğerliği + yeni kotlar + içecek yedeği) ----------------------------------------------------------------
OLCUM = '''

def olcum_v5():
    """v5 · ALÇAK HAT: iddiaları ÖLÇER, bozulursa durur (assert). Dönüş: ölçülen değerler sözlüğü."""
    import dilim_v1 as DL
    import kutu_cad_v4 as ESKI
    O = {}
    def bb(ad):
        return [p for p in PARCALAR if p["ad"] == ad][0]["wp"].val().BoundingBox()
    def yaz(ad, sart, deger):
        print("  %-92s %s %s" % (ad, "GEÇTİ" if sart else "** KALDI **", deger)); assert sart, ad
    print("OLCUM v5 (alcak hat)")
    # 1 · DİLİM EŞDEĞERLİĞİ: v4'ün y %.0f–%.0f dilimi çıkarılmış hali ↔ v5 (doğrudan yeni kotlarda kurulan)
    ESKI.modul()
    ref, rap = DL.dilimle(ESKI.PARCALAR, DILIM_Y0, DILIM_DY, prizma_haric=("asansor_rayi_",))
    k = DL.karsilastir(PARCALAR, ref, yalniz_zarf=("asansor_rayi_",))
    yeni = {"icecek_yedek_altligi"} | {"icecek_yedek_koli_%d%d" % (a, b) for a in range(len(ICECEK_X)) for b in range(ICECEK_KAT)}
    O["dilim"] = dict(alt=len(rap["ALT"]), ust=len(rap["UST"]), gecen=len(rap["GECEN"]), ayni=len(k["ayni"]), fark=k["fark"])
    yaz("dilim y %.0f–%.0f: v4 %d parça (altta %d · üstte %d · boydan geçen %d, bantta biten 0) ↔ v5 birebir %d · fark %d"
        % (DILIM_Y0, DILIM_Y0 + DILIM_DY, len(ESKI.PARCALAR), len(rap["ALT"]), len(rap["UST"]), len(rap["GECEN"]), len(k["ayni"]), len(k["fark"])),
        not k["fark"] and not k["ref_eksik"] and set(k["yeni_ek"]) == yeni, "; ".join(k["fark"][:6]) + (" eksik %s" % k["ref_eksik"] if k["ref_eksik"] else "") +
        (" beklenmeyen yeni %s" % sorted(set(k["yeni_ek"]) - yeni) if set(k["yeni_ek"]) != yeni else ""))
    print("     boydan geçen (168 kısaldı): %s" % ", ".join(rap["GECEN"]))
    # 2 · KOTLAR
    O["ust"] = max(p["wp"].val().BoundingBox().ymax for p in PARCALAR if p["grup"] == "SABIT" and "_kulp" not in p["ad"])
    yaz("makine üstü %.1f = H %.0f (2030 − 168)" % (O["ust"], H), abs(O["ust"] - H) < 0.01 and abs(H - 1862.0) < 0.01, "")
    O["tepsi"] = max(bb("tepsi_cubugu_%d" % i).ymax for i in range(4))
    yaz("kutu tepsisi üstü %.1f = TEPSI (1104 − 168 = 936)" % O["tepsi"], abs(O["tepsi"] - TEPSI) < 0.01 and abs(TEPSI - 936.0) < 0.01, "")
    b_ = bb("kalip_alt_rafi"); O["alt_raf"] = (b_.ymin, b_.ymax)
    yaz("alt raf %.1f–%.1f (786–790 − 168)" % (b_.ymin, b_.ymax), abs(b_.ymin - 618.0) < 0.01 and abs(b_.ymax - 622.0) < 0.01, "")
    b_ = bb("karton_yigini"); O["sarjor"] = (b_.ymin, b_.ymax, SARJOR_ADET)
    yaz("şarjör yığını %.1f–%.1f = %.0f mm → %d kutu @1,6 · %d @1,8 (v4 567) · + fırın üstü 320 = %d" % (b_.ymin, b_.ymax, b_.ylen, int(b_.ylen / 1.6 + 1e-6),
        int(b_.ylen / 1.8), int(b_.ylen / 1.6 + 1e-6) + 320), SARJOR_ADET == 462 and abs(b_.ymax - 980.0) < 0.01 and abs(b_.ymin - Y_PLAT) < 0.01, "")
    b_ = bb("sol_sac_pizza_penceresi")
    yaz("pizza penceresi y %.0f–%.0f = K plakası %.0f − 18 / + 66" % (PENCERE[0], PENCERE[1], PLAKA_K), abs(PENCERE[0] - 978.0) < 0.01 and abs(PENCERE[1] - 1062.0) < 0.01, "")
    yaz("kinematik kotlar: YB %.1f · KALIP %.1f · H_UST %.0f · 2. vuruş %.0f · H_BEKLE %.0f · kapak baskısı %.1f · KOL_P y %.0f · PARMAK_P y %.0f"
        % (YB, KALIP, H_UST, Y_VURUS2, H_BEKLE, KAPAK_BASKI, KOL_P[1], PARMAK_P[1]),
        all(abs(a - b) < 0.01 for a, b in ((YB, 1149.6 - 168), (KALIP, 1149.5 - 168), (H_UST, 1478 - 168), (Y_VURUS2, 1108 - 168), (H_BEKLE, 1467 - 168),
                                            (KOL_P[1], 1080 - 168), (PARMAK_P[1], 1260 - 168), (KAPAK_BASKI, ESKI.KAPAK_BASKI - 168))), "")
    fk = [abs(kafa(t) - (ESKI.kafa(t) - 168.0)) for t in [i * 0.05 for i in range(401)]]
    fb = []
    for t in [i * 0.25 for i in range(81)]:
        a0, A0 = blank_acilar(t); a1, A1 = ESKI.blank_acilar(t)
        fb.append(max([abs(a0[j] - a1[j]) for j in range(3)] + [abs(A0[g] - A1[g]) for g in A0]))
    yaz("kafa(t) = v4 − 168 (401 an, en büyük fark %.4f mm) · blank_acilar(t) = v4 (81 an, en büyük fark %.4f)" % (max(fk), max(fb)), max(fk) < 1e-6 and max(fb) < 1e-6, "")
    # menteşeler 168 aşağıda: M5(x) = M4(x − s) + s → R aynı, t5 = t4 + s − R·s (s = (0, −168, 0))
    s_ = (0.0, -DILIM_DY, 0.0); fd, ft = 0.0, 0.0
    for t in KUTU_ANLARI + GECIS_ANLARI:
        W5, W4 = blank_dunya(t), ESKI.blank_dunya(t)
        for g in W5:
            fd = max(fd, max(abs(W5[g][i][j] - W4[g][i][j]) for i in range(3) for j in range(3)))
            ft = max(ft, max(abs(W5[g][i][3] - (W4[g][i][3] + s_[i] - sum(W4[g][i][j] * s_[j] for j in range(3)))) for i in range(3)))
    yaz("blank_dunya: %d an × %d düğüm · dönme v4 ile aynı (%.1e) · öteleme = v4 + s − R·s (%.1e)" % (len(KUTU_ANLARI + GECIS_ANLARI), len(DUGUM), fd, ft), fd < 1e-9 and ft < 1e-6, "")
    # 3 · İÇECEK YEDEĞİ
    kol = [p for p in PARCALAR if p["ad"].startswith("icecek_yedek_koli_")]
    kb = [p["wp"].val().BoundingBox() for p in kol]
    O["icecek"] = dict(koli=len(kol), kutu=len(kol) * KOLI["kutu"], x=(min(b.xmin for b in kb), max(b.xmax for b in kb)), y=(min(b.ymin for b in kb), max(b.ymax for b in kb)),
                       z=(min(b.zmin for b in kb), max(b.zmax for b in kb)))
    yaz("içecek yedeği %d koli × %d = %d kutu (+ dolap 144 = %d · 4 gün 277) · x %.0f–%.0f · y %.0f–%.0f · z %.0f…%.0f"
        % (len(kol), KOLI["kutu"], O["icecek"]["kutu"], O["icecek"]["kutu"] + 144, O["icecek"]["x"][0], O["icecek"]["x"][1], O["icecek"]["y"][0], O["icecek"]["y"][1],
           O["icecek"]["z"][0], O["icecek"]["z"][1]), len(kol) == 6 and O["icecek"]["kutu"] + 144 >= 277, "")
    ark = {a: bb(a) for a in ("kose_dikme_on_0", "kose_dikme_on_1", "kablo_kanali_dikey_alt", "asansor_ray_plakasi", "kalip_alt_rafi_koseben_on", "sol_sac_pizza_penceresi", "sag_sac", "on_alt_sac")}
    bosluk = dict(on_dikme=ark["kose_dikme_on_0"].zmin - O["icecek"]["z"][1], kablo_kanali=ark["kablo_kanali_dikey_alt"].zmin - O["icecek"]["z"][1],
                  ray_plakasi=O["icecek"]["z"][0] - ark["asansor_ray_plakasi"].zmax, raf_kosebent=ark["kalip_alt_rafi_koseben_on"].ymin - O["icecek"]["y"][1],
                  sol_sac=O["icecek"]["x"][0] - ark["sol_sac_pizza_penceresi"].xmax, sag_sac=ark["sag_sac"].xmin - O["icecek"]["x"][1],
                  on_sac=ark["on_alt_sac"].zmin - O["icecek"]["z"][1])
    O["icecek_bosluk"] = bosluk
    yaz("içecek yedeği boşlukları: ön dikme %.1f · dikey kablo kanalı %.1f · ön alt sac %.1f · asansör ray plakası %.1f · alt raf köşebendi %.1f · sol sac %.1f · sağ sac %.1f"
        % (bosluk["on_dikme"], bosluk["kablo_kanali"], bosluk["on_sac"], bosluk["ray_plakasi"], bosluk["raf_kosebent"], bosluk["sol_sac"], bosluk["sag_sac"]),
        all(v > 0.0 for v in bosluk.values()), "")
    ic = [p for p in PARCALAR if p["ad"].startswith("icecek_")]
    diger = [p for p in PARCALAR if not p["ad"].startswith("icecek_") and p["grup"] in ("SABIT", "ASANSOR")]
    cak = []
    for p in ic:
        a = p["wp"].val(); A = a.BoundingBox()
        for q in diger:
            b2 = q["wp"].val()
            if _bb_kesisir(A, b2.BoundingBox()):
                v = a.intersect(b2).Volume()
                if v > 0.5: cak.append((p["ad"], q["ad"], round(v, 1)))
    yaz("içecek yedeği ↔ E gövde + şarjör + asansör (gerçek katı) çakışma %d" % len(cak), not cak, str(cak[:4]))
    kat4 = ICECEK_Y0 + 4 * KOLI["y"]
    yaz("4. kat sığmaz (üst %.0f > köşebent altı %.0f) → 3 kat doğru" % (kat4, ark["kalip_alt_rafi_koseben_on"].ymin), kat4 > ark["kalip_alt_rafi_koseben_on"].ymin, "")
    # 4 · BOŞ BÖLGE (alt rafın altı, içecek yedeğinin üstü)
    X_, Y_, Z_ = O["icecek"]["x"], O["icecek"]["y"], O["icecek"]["z"]
    ust = []
    for p in PARCALAR:
        if p["ad"].startswith("icecek_") or p["grup"] in ("PIZZA", "CATAL", "K_ITICI", "SABIT_REF") or p["grup"].startswith("B_"):
            continue
        b2 = p["wp"].val().BoundingBox()
        if b2.xmax > X_[0] and b2.xmin < X_[1] and b2.zmax > Z_[0] and b2.zmin < Z_[1] and b2.ymax > Y_[1]:
            assert b2.ymin >= Y_[1] - 0.01, p["ad"]
            ust.append((b2.ymin, p["ad"]))
    alt_en, alt_ad = min(ust)
    O["bos_bolge"] = dict(x=X_, y=(Y_[1], alt_en), z=Z_)
    print("     BOŞ: içecek yedeğinin üstü y %.0f–%.0f (%.0f mm) · x %.0f–%.0f · z %.0f…%.0f (ilk engel %s)" % (Y_[1], alt_en, alt_en - Y_[1], X_[0], X_[1], Z_[0], Z_[1], alt_ad))
    # 5 · ASANSÖR STROKU (v4'ten aynen gelen sınır — bilgi): son kutuyu kaldırmak için platform YB'ye çıkmalı
    som, uy = bb("asansor_somunu"), bb("asansor_ust_yatak")
    p_som = Y_PLAT + (uy.ymin - som.ymax)
    ray, ar = bb("asansor_rayi_0"), bb("asansor_arabasi_01")
    p_ray = Y_PLAT + (ray.ymax - ar.ymax)
    O["asansor"] = dict(platform_somun_siniri=p_som, platform_ray_siniri=p_ray, besleyemez_somun=int((YB - p_som) / T + 0.999), besleyemez_ray=int((YB - p_ray) / T + 0.999))
    print("     UYARI (v4'ten aynen): platform en çok %.1f'e çıkar (somun üst yatağa değer) → son %d kutu beslenemez · üst HGH15 araba ray ucundan çıkmasın dersek %.1f → son %d kutu"
          % (p_som, O["asansor"]["besleyemez_somun"], p_ray, O["asansor"]["besleyemez_ray"]))
    return O
'''
d("\n\n# ---------------------------------------------------------------- GLB (hiyerarşik düğüm + animasyon)", OLCUM + "\n\n# ---------------------------------------------------------------- GLB (hiyerarşik düğüm + animasyon)")

# ---------------------------------------------------------------- ÇIKTILAR ----------------------------------------------------------------
d('"generator": "AUTOKITCH kutu_cad_v4"', '"generator": "AUTOKITCH kutu_cad_v5"')
d('print("E KUTU MODULU v4 (alt raf): %d parca · %.0f sn" % (len(PARCALAR), time.time() - t0)); sys.stdout.flush()',
  'print("E KUTU MODULU v5 (alcak hat · ust 1862 · tepsi 936 · sarjor 462 · icecek yedegi 6 koli): %d parca · %.0f sn" % (len(PARCALAR), time.time() - t0)); sys.stdout.flush()')
d("    olcum(); sys.stdout.flush()", "    olcum(); sys.stdout.flush()" + NL + "    olcum_v5(); sys.stdout.flush()")
d('"otonom", "hat3d", "kutu_modulu_v4.glb")', '"otonom", "hat3d", "kutu_modulu_v5.glb")')
d('bom_yaz(os.path.join(KOK, "arastirma", "5_PACK_kutu_v4"))', 'bom_yaz(os.path.join(KOK, "arastirma", "5_PACK_kutu_v5"))')
hedef = os.path.join(U, "kutu_cad_v5.py")
assert not os.path.exists(hedef), "kutu_cad_v5.py zaten var — üstüne yazılmaz"
io.open(hedef, "w", encoding="utf-8").write(s)
print("kutu_cad_v5.py yazildi")
