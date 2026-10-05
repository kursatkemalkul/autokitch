# -*- coding: utf-8 -*-
"""h3_topping_sac_v2 — v1 + KEMAL ONAYLI 4 DÜZELTME (4 Eki 2026 · Claude · YEREL · v1 DEĞİŞMEDİ, zincir adım 37 bu dosyayı çağırır)
  D1 · SERVİS SACI 17 HAVŞA VİDASI: servis sacı + arkadaki dönüş flanşı birlikte ÇÖKERTİLİR (dimple, iç içe 90° koni) · dış yüz düz · dönüşteki PEM SP-M5
       yerine dönüşün iç yüzüne 2 punta TIG ile kaynak burcu M5 (Ø14 × 9, alt yüzü dimple'a havşalı) · vida DIN 7991 M5 × 12 (ucu burç arka yüzünde).
  D2 · SOĞUK ODA İÇ SACI (astar 304 1,0): TIG kaynaklı 4 düz sac YERİNE bükümlü kenarlı 4 sac (R 1 = t) · sol / sağ: arka kenar içe (arka astarın
       ARKASINA), üst kenar içe (tavan astarının ÜSTÜNE), ön kenar dışa (ön çerçevenin ARKASINA) · tavan: arka kenar aşağı (arka astarın arkasına), ön kenar
       yukarı (çerçevenin arkasına) · arka astar düz (en son önden girer) · birleşimler ISO 15983 Ø3,2 kör perçin (içeriden) / ISO 15984 havşa başlı Ø3,2
       (çerçeveden, gömme) · her perçinde POM-C ısı kesici ara pul Ø9 × 1 · gıda tarafı köşeler + ön derz silikon · PU artık YERİNDE KÖPÜK DEĞİL:
       ölçüsünde kesilmiş 4 levha (arka / sol / sağ / tavan) + dış saca 0,5 mm yapıştırıcı (flanş / perçin / pul yuvaları levhada açık).
  D3 · EVAPORATÖR AYAKLARI: servis sacındaki 4 sekme (v8zq TOPPING_MODUL__sac 87 / 88 / 94 / 95) KALKTI → aynı düzlemde 2,5 mm L ayak, kuru bölme
       tabanına 1 × ISO 7380 M5 → tabanda PEM SP-M5 · servis sacı tek başına sökülür · evaporatör konumu aynı.
  D4 · MONTAJ: kuru bölme tabanında kondenser kanalı (dirsekli Ø31 boru) için geçiş deliği 135 × 33 + kanal geçiş kapağı (sağdan açık yarıklı, 2 × M5) ·
       TOPPING → B pulu ISO 7092 Ø15 (Ø16 servis deliğinden geçer; eski zincir_T_tamamla T1).
v1 açıklaması aşağıda (değişmeyen her şey için geçerli):

h3_topping_sac_v1 — TOPPING (C) İSTASYONU GÖVDESİ + KAIDE_C · ÜRETİM SACI v1 (4 Eki 2026 · Claude · GECE 2 ADIM 5c · YEREL · bağımsız üreteç,
montaja bağlı DEĞİL)

Kemal: "üretim sacını yap ama tam yap, üretime yönelik" · "yalıtım hiçbir yerde görünmesin". STANDART: h3_a_sac_v1 / h3_b_sac_v1 ile aynı kurgu ·
h3_sac_v1 (gerçek abkant bükümü R 1,5t · K 0,45 · büküm payı · rahatlatma · açınım · DFM · PEM / vida BOM) · sac_kararlar_v1 (AUTOKITCH_SAC_STANDART).
REFERANS: hat3_v8zq.glb TOPPING_MODUL__sac / __paslanmaz / __pu (gövde bileşenleri) · KAIDE_C__paslanmaz · kuruluş betikleri topping_govde_yeni.py + tg/tgeo.py
(v8o) · topfix t3 (soğuk oda kabuğu) · elk3/tasarim.py (J1 birleşim paneli). Kesik / delik konumları v8zq gövde saclarının orta düzlem kesitinden alındı.
KOORDİNAT: DÜNYA (mm · x hat boyu · y yukarı · z ön +). Zarf x 1436–2500 · y 788–2200 · z −830…+39 (kanatlar z 39–79 bu üreteçte DEĞİL — v8zq kanatları kalır).

KURGU
  1 · DIŞ KABUK 304 1,5 (kaynaklı + PU sandviç gövde):
      SOL / SAĞ YAN (y 892–2200) arka 20 mm iç dönüşlü (servis sacı oturma yüzü, dolu bölgelerde kısaltılmış) · sol yanda TABLA GEÇİŞ AĞZI (alta açık, A'daki
      ağızla eş) + A ↔ TOPPING 4 × PEM SP-M8 (h3_a_sac_v1.M8_T, PU bölgesindekiler köpük kapaklı) · sağ yanda tabla geçişi (F duvarıyla eş) + J1 BİRLEŞİM
      PANELİ AĞZI 57 × 67 (EPDM kovan geçme payı, E/U ile aynı) + 4 burç FHP-M5 + ana hat geçişi (U_F ile eş, arka kenarı −820) + TOPPING ↔ F 4 × PEM SP-M8
      (cıvata F içinden, F sol sacında Ø9 = ARAYÜZ). Eski 40 × 40 yamalı Ø16,4 / Ø13,9 delikler ÜRETİLMEZ.
      TAVAN 1,5 yanların ARASINA oturur: yan + arka 20 mm aşağı dönüş (punta) · kuru bölme üstünde 166 lazer hava yarığı (5 × 70).
      TABAN 1,5: yan + arka yukarı dönüş (yanlara punta · arka dönüş servis sacı oturma yüzü) · menfez yarık alanları · soğutma cebi ağzı · KD1 kanal ağzı ·
      kaideye 2 × M6 (cıvata yukarıdan, kaide plakasında PEM SP-M6) · tabla rayı M6'sı ADIM 8'de kalktı (ray tabanı A'da bağlı).
      ARKA = SÖKÜLÜR SERVİS SACI (Kemal 2 Eki: "kuru bölmeye servis = sökülür arka sac, bombe başlı vida izinli"): düz 1,5 · kondenser emiş penceresi ·
      ISO 7380 M5 (bombe başlı) → yan / tavan / taban dönüşlerinde PEM SP-M5. Pano kutusu, DIN plakası, emiş filtresi, KD3 braketleri bu sacta FHP-M5.
  2 · SOĞUK ODA (sandviç, yerinde köpük PU 40 kg/m³):
      ÖN ÇERÇEVE 430 1,0 (manyetik fitil yüzü, z 38–39) · ALT SAC 1,5 (y 1109) 6 düşme deliği · ARKA DIŞ SAC 1,5 (z −630) POM burç delikleri + 4 evaporatör
      hava kanalı ağzı · ASTAR 304 1,0 gıda (arka + sol + sağ + tavan düz sac, iç köşeler TIG + R3 taşlama) arka duvarda 4 evaporatör lazer yarık alanı ·
      4 EVAPORATÖR HAVA KANALI KOVANI (1,0 · iki L, arka dış sac → astar) · RAF 3,0 (iki büküm + iki köşebent, altı PU) · ÜST RAF 3,0 · EŞİK 1,2 (L) ·
      DİL KANALI U 1,0 (kaşar / sucuk kaset dili, raf + eşik boyunca tek parça) · DÜŞME KOVANLARI: kıyma / kuşbaşı 3,0 iki L (iç 38) · sos / harç
      boru Ø38 × 3,5 (iç 31) · kaşar / sucuk artı kesitli POM-C CNC kovan.
  3 · KURU + TEKNİK BÖLME: kuru bölme tabanı 1,5 (sol + ön dönüş) · teknik bölme ön perdesi 1,5 (22 menfez yarığı · alt + üst dönüş) · sağ perde 1,5 ·
      AYIRMA PERDESİ 1,5 (cep sol duvarı, 24 emiş yarığı) · SOĞUTMA GRUBU CEBİ 1,5 tava (kaide gözüne iner, 4 takoz PEM SP-M8).
  4 · KAIDE_C (kaynaklı, 788–892): 304 dikdörtgen boru 40 × 100 × 2 (arka · iki yan · enine · üç boyuna) + enine lama 6 × 100 (cep yanı) ·
      ÖN PERDE MENFEZLİ = 2,0 C profil (kanat menfezleri hizasında 3 lazer yarık alanı → kondenser / kaide gözü hava girişi) · ÜST PLAKA 4 mm (delik kaynağı,
      4 pencere, PEM SP-M6) · cep taşıyıcı L 3 mm × 2 · KAIDE → B 4 × M8 (boru alt duvarı Ø9, üst duvar + plaka Ø16 servis · B tarafı ARAYÜZ).
  DUVARA DEĞEN HER MEKANİZMA / ELEKTRİK / HAVA PARÇASINA FHP-M5 saplama (ARAYÜZ: karşı parçada Ø5,5) — h3_e_sac_v1 kuralı.
ARAYÜZLER DEĞİŞMEZ: dış zarf · soğuk oda ağzı 1496–2440 × 1152–2140 · raf üstü 1152 · ön düzlem 39 · kaset / UNO / evaporatör / tabla / kablo yerleri.
Çalıştır (denetim + çıktılar): gece2/adim5/topping_sac_denetim_v1.py (scratchpad) · bu dosya yalnız KURAR."""
import math, os, sys, re, time
H3 = os.path.dirname(os.path.abspath(__file__)); _U = os.path.dirname(H3)
for _p in (_U, H3):
    if _p not in sys.path: sys.path.insert(0, _p)
import numpy as np
import cadquery as cq
import h3_sac_v1 as S

SURUM = "h3_topping_sac_v2"
V = cq.Vector
X_A = 0.0
BIRIM = "TOPPING_GOVDE"
T = 1.5
X0, X1 = 1436.0, 2500.0
XI0, XI1 = X0 + T, X1 - T
YB, YBI, YT, YTI = 892.0, 893.5, 2200.0, 2198.5
ZA, ZAI, ZF, ZFC = -830.0, -828.5, 39.0, 38.0
Y_SO, Z_SA = 1109.0, -630.0
AST = dict(x0=1495.0, x1=2441.0, y0=1110.5, y1=2141.0, zb=-571.0, t=1.0)
FL = 20.0
R_GIDA = 3.0
TABLA_SOL = (YB - 1.0, 1042.0, -510.0, 5.0)                       # sol yan: alta açık (y0 y1 z0 z1)
TABLA_SAG = (965.0, 1042.0, -341.0, -10.0)
J1 = dict(Y0=1468.0, c=-715.0, agiz=(1473.5, 1530.5, -723.5, -656.5), burc=[(-54.0, 8.0), (54.0, 75.0), (-54.0, 126.0), (54.0, 98.0)])
HAT_GECIS = (2104.0, 2169.0, -820.0, -689.0)
M8_A = [(1300.0, -300.0), (1300.0, -700.0), (2000.0, -300.0), (2000.0, -700.0)]      # h3_a_sac_v1.M8_T
M8_F = [(1000.0, -760.0), (1250.0, -700.0), (1700.0, -780.0), (1950.0, -780.0)]      # TOPPING ↔ F (kuru / teknik bölgede, köpüksüz)
EMIS_PEN = (1447.0, 1624.5, 905.0, 1099.5)
TAVAN_YARIK = dict(u0=1470.0, u1=2465.0, v0=-815.0, v1=-645.0, gen=5.0, boy=70.0, adim=12.0, ara=24.0)
TABAN_YARIK = [(1481.0, 1614.0), (2145.0, 2415.0)]
CEP = (1629.5, 2093.5, -788.5, -477.5)
Y_CEP = 806.0
KD1_AGIZ = (2419.5, 2451.0, -699.5, -558.5)
TAKOZ = [(1658.0, -760.0), (1988.0, -760.0), (1658.0, -503.0), (1988.0, -503.0)]
GOVDE_M6 = [(1545.0, -458.0), (2300.0, -458.0)]
# ADIM 8 (4 Eki 2026): tabla rayı → kaide M6 (x 1750 / 2250 · z −320 / −20) KALDIRILDI — bu eksenlerde ray tabanı yok (cıvata hiçbir parçaya değmiyordu,
# zincir 37 atlıyordu). Ray tabanı A tarafında h3_a_sac_v1.RAY_M6 (4 × M6) ile bağlı. Kaide plakasında PEM SP-M6 ve gövde tabanında Ø6,6 da açılmaz.
RAY_M6 = []
# ADIM 8 · entegrasyonda (zincir 37, sac_ent saplama boyu denetimi) engel yüzünden çıkarılan FHP saplamalar: kur() SONUNDA saplama_duzelt() ile
# kaldırılır (saplama + sacdaki PEM deliği) · diğer saplamaların yeri ve adları birebir aynı kalır.
SAPLAMA_CIKAR = {
    "arayuz_j1_burc_1476_769": "J1 üst burç · 23,5 mm'de ELK_ZINCIR etiketi (burç yeri elektrik modelinde sabit; panel alt 2 burçla tutulur)",
    "arayuz_j1_burc_1594_769": "J1 üst burç · 23,5 mm'de Harting (panel alt 2 burçla tutulur)",
    "arayuz_mek_yan_sag_0": "ELK_IC kablo kanalı tabanı · kablolar 4 mm'de (kanal boyunca dolu, taşınacak yer yok)",
    "arayuz_mek_yan_sag_1": "ELK_IC kablo kanalı tabanı · kablolar 4 mm'de (kanal boyunca dolu, taşınacak yer yok)",
    "arayuz_mek_arka_19": "evaporatör ayağı 30 × 20 × 2,5 · tamamı evaporatör gövdesinin (PU + sac) altında, 4 mm'de",
    "arayuz_mek_arka_20": "evaporatör ayağı 30 × 20 × 2,5 · tamamı evaporatör gövdesinin altında, 4 mm'de",
    "arayuz_mek_arka_21": "evaporatör ayağı 30 × 20 × 2,5 · tamamı evaporatör gövdesinin altında, 4 mm'de",
    "arayuz_mek_arka_22": "evaporatör ayağı 30 × 20 × 2,5 · tamamı evaporatör gövdesinin altında, 4 mm'de",
}
KUR_TABAN_DELIK = [(1700.0, -804.89, 16.4), (2110.0, -760.0, 14.0), (2236.0, -659.89, 8.39)]      # v2: Ø32,78 kanal deliği → KANAL_DELIK
KANAL_DELIK = (2139.5, 2274.5, -716.5, -683.5)          # v2 D4 · kondenser kanalı dirsekli boru (dikey kol x 2242,6–2273,4 · üst kol x 2140,6'ya dek) dikey iner
KANAL_KAPAK = (2131.0, 2283.0, -731.0, -668.0)          # geçiş kapağı 1,5 (sağdan açık yarık: boru dikey kolu çevresinde sola sürülür)
KANAL_KAPAK_M5 = [(2150.0, -675.0), (2200.0, -675.0)]
EVAP_AYAK = [(1464.0, 1322.0), (1620.0, 1322.0), (1778.0, 1423.0), (2173.0, 1423.0)]   # v2 D3 · (x0 · üst y) 30 geniş · z −828,5…−826 (eski sekme düzlemi)
# soğuk oda kesikleri (v8zq)
DUSME_KARE = [(1596.0, -170.0), (1848.0, -170.0)]                 # kıyma / kuşbaşı (iç 38)
DUSME_YUV = [(1722.0, -169.79), (2259.5, -169.79)]                # sos / harç (iç Ø31)
DUSME_ARTI = [2088.5, 2360.5]                                      # kaşar / sucuk (artı kesit)
ARTI_IC = [(-39.0, -161.0), (-33.0, -161.0), (-33.0, -182.5), (33.0, -182.5), (33.0, -161.0), (39.0, -161.0), (39.0, -139.0), (33.0, -139.0),
           (33.0, -117.0), (-33.0, -117.0), (-33.0, -139.0), (-39.0, -139.0)]             # x kaşar eksenine göre, z
RAF_DELIK = [(1596.0, -169.99, 42.98), (1848.0, -169.99, 42.98), (1722.0, -169.99, 37.18), (2259.5, -169.99, 37.18)]
RAF_MANDAL = [(1963.0, -196.5), (2298.0, -196.5)]
DIL_X = [(2054.0, 2123.0), (2326.0, 2395.0)]                       # dil kanalı dış (duvarlar 1,0)
UST_RAF_DELIK = [(1722.0, -172.44, 40.57), (2259.5, -172.44, 40.57)]
BURC_YUV = [(1596.22, 1190.5), (1722.22, 1613.5), (1848.22, 1190.5), (2259.72, 1613.5)]   # POM burç Ø29,67 (arka dış sac + astar)
BURC_YUV_D = 30.45
BURC_YUV_POLY = [(14.78, 0.0), (13.92, 3.49), (13.06, 6.97), (10.68, 9.66), (8.3, 12.34), (4.94, 13.62), (1.59, 14.89), (-1.98, 14.46), (-5.54, 14.03), (-8.49, 11.99),
                 (-11.45, 9.95), (-13.12, 6.77), (-14.78, 3.59), (-14.78, 0.0), (-14.78, -3.59), (-13.12, -6.77), (-11.45, -9.95), (-8.49, -11.99), (-5.54, -14.03),
                 (-1.98, -14.46), (1.59, -14.89), (4.94, -13.62), (8.3, -12.34), (10.68, -9.66), (13.06, -6.97), (13.92, -3.49)]     # POM burç kesiti (v8zq, x-y)
RAF_BURC_POLY = [(-1.84, 7.435), (0.0, 7.885), (1.88, 7.425), (3.72, 6.965), (5.16, 5.685), (6.58, 4.425), (7.27, 2.625), (7.94, 0.845), (7.71, -1.035), (7.48, -2.955),
                 (6.38, -4.545), (5.3, -6.105), (3.59, -7.005), (1.91, -7.885), (0.02, -7.885), (-1.91, -7.885), (-3.59, -7.005), (-5.3, -6.105), (-6.4, -4.515),
                 (-7.48, -2.955), (-7.71, -1.035), (-7.94, 0.845), (-7.27, 2.625), (-6.58, 4.425), (-5.14, 5.715), (-3.72, 6.965)]   # raf askı burcu kesiti (y-z)
MOTOR_BURC = [(2088.94, 1192.0), (2088.94, 1347.0), (2360.94, 1212.0), (2360.94, 1316.0)]    # POM motor burcu (lob kesit, v8zq)
MOTOR_LOB = [(-11.08, -28.05), (-22.9, -19.89), (-26.23, -13.54), (-29.57, -7.18), (-29.57, 7.18), (-26.23, 13.54), (-22.9, 19.89), (-11.08, 28.05),
             (-3.95, 28.92), (3.18, 29.78), (9.89, 27.24), (16.6, 24.69), (21.36, 19.32), (26.12, 13.94), (29.56, 0.0), (26.12, -13.94), (21.36, -19.32),
             (16.6, -24.69), (9.89, -27.24), (3.18, -29.78), (-3.95, -28.92)]
BURC_YARIK = [(1560.0, 1780.0, 1272.0, 1302.0), (1520.0, 1690.0, 1700.0, 1730.0), (2200.0, 2330.0, 1700.0, 1730.0)]   # POM yarık burçları
EVAP_KAN = [(1503.0, 1623.0, 1338.0, 1497.0), (1503.0, 1623.0, 1582.0, 1637.0), (1807.0, 2121.0, 1434.0, 1530.0), (1807.0, 2174.0, 1582.0, 1786.0)]
# duvara değen kalan parçalar → FHP-M5 saplama (v8zq temas taraması, gece2/adim5c/temas.py)
STUD = [
    ('yan_sol', (1437.5, 928.5, 32.5), 'TOPPING_MODUL__paslanmaz[84] menteşe gövdesi'), ('yan_sol', (1437.5, 1535.0, 32.5), 'TOPPING_MODUL__paslanmaz[85] menteşe gövdesi'),
    ('yan_sol', (1437.5, 2095.0, 32.5), 'TOPPING_MODUL__paslanmaz[86] menteşe gövdesi'),
    ('yan_sag', (2498.5, 1072.0, -608.02), 'ELK_IC__kanal[65]'), ('yan_sag', (2498.5, 1072.0, -186.48), 'ELK_IC__kanal[65]'),
    ('yan_sag', (2498.5, 1029.0, 11.75), 'ELK_IC__kanal[77]'), ('yan_sag', (2498.5, 930.0, 11.75), 'ELK_IC__kanal[90]'),
    ('yan_sag', (2498.5, 1633.0, -788.65), 'ELK_ZINCIR__kanal[2] (J1 PD)'), ('yan_sag', (2498.5, 1633.0, -732.35), 'ELK_ZINCIR__kanal[2] (J1 PD)'),
    ('yan_sag', (2498.5, 928.5, 32.5), 'TOPPING_MODUL__paslanmaz[87] menteşe gövdesi'), ('yan_sag', (2498.5, 1535.0, 32.5), 'TOPPING_MODUL__paslanmaz[88] menteşe gövdesi'),
    ('yan_sag', (2498.5, 2095.0, 32.5), 'TOPPING_MODUL__paslanmaz[89] menteşe gövdesi'),
    ('taban', (1943.0, 893.5, 16.0), 'TOPPING_MODUL__paslanmaz[94]'), ('taban', (1991.0, 893.5, 16.0), 'TOPPING_MODUL__paslanmaz[94]'),
    ('taban', (2120.0, 893.5, -707.5), 'TOPPING_MODUL__sac[7]'), ('taban', (2120.0, 893.5, -562.5), 'TOPPING_MODUL__sac[7]'),
    ('arka', (1500.0, 1255.0, -828.5), 'ELK_TOPPING__celik[1] KD3 braketi'), ('arka', (1950.0, 1255.0, -828.5), 'ELK_TOPPING__celik[2] KD3 braketi'),
    ('arka', (2330.0, 1255.0, -828.5), 'ELK_TOPPING__celik[3] KD3 braketi'), ('arka', (2285.0, 1722.5, -828.5), 'TOPPING_MODUL__celik[0]'),
    ('arka', (2386.0, 1722.5, -828.5), 'TOPPING_MODUL__celik[1]'), ('arka', (1535.72, 951.25, -828.5), 'TOPPING_MODUL__pom[35] emiş filtresi'),
    ('arka', (1535.72, 1053.75, -828.5), 'TOPPING_MODUL__pom[35] emiş filtresi'), ('arka', (1580.5, 2010.0, -828.5), 'TOPPING_MODUL__sac[0] kuru pano kutusu'),
    ('arka', (1855.5, 2010.0, -828.5), 'TOPPING_MODUL__sac[0] kuru pano kutusu'), ('arka', (1495.5, 1760.0, -828.5), 'TOPPING_MODUL__sac[2] DIN plakası'),
    ('arka', (1600.5, 1760.0, -828.5), 'TOPPING_MODUL__sac[2] DIN plakası'), ('arka', (1481.0, 1312.0, -828.5), 'TOPPING_MODUL__sac[87] evaporatör ayağı'),
    ('arka', (1635.0, 1312.0, -828.5), 'TOPPING_MODUL__sac[88] evaporatör ayağı'), ('arka', (1793.0, 1413.0, -828.5), 'TOPPING_MODUL__sac[94] evaporatör ayağı'),
    ('arka', (2188.0, 1413.0, -828.5), 'TOPPING_MODUL__sac[95] evaporatör ayağı'),
    ('soguk_arka', (1684.0, 1400.0, -630.0), 'HAVA_IC__aski[1]'), ('soguk_arka', (1684.0, 1560.0, -630.0), 'HAVA_IC__aski[3]'),
    ('soguk_arka', (1712.0, 1653.5, -630.0), 'HAVA_IC__aski[5]'), ('soguk_arka', (2080.0, 1283.5, -630.0), 'HAVA_IC__aski[7]'),
    ('soguk_arka', (2200.0, 1283.5, -630.0), 'HAVA_IC__aski[9]'), ('soguk_arka', (2302.0, 1400.0, -630.0), 'HAVA_IC__aski[11]'),
    ('soguk_arka', (2302.0, 1560.0, -630.0), 'HAVA_IC__aski[13]'), ('soguk_arka', (2282.0, 1653.5, -630.0), 'HAVA_IC__aski[15]'),
    ('soguk_arka', (2259.5, 1555.4, -630.0), 'TOPPING_MODUL__paslanmaz[80] silindir ayağı'), ('soguk_arka', (1722.0, 1555.4, -630.0), 'TOPPING_MODUL__paslanmaz[81] silindir ayağı'),
    ('soguk_arka', (1596.0, 1132.4, -630.0), 'TOPPING_MODUL__paslanmaz[82] silindir ayağı'), ('soguk_arka', (1848.0, 1132.4, -630.0), 'TOPPING_MODUL__paslanmaz[83] silindir ayağı'),
    ('soguk_arka', (1558.0, 1382.0, -630.0), 'TOPPING_MODUL__pom[36] evaporatör L ısı kesici'), ('soguk_arka', (1558.0, 1582.0, -630.0), 'TOPPING_MODUL__pom[36] evaporatör L ısı kesici'),
    ('soguk_arka', (1874.25, 1609.0, -630.0), 'TOPPING_MODUL__pom[37] evaporatör R ısı kesici'), ('soguk_arka', (2106.75, 1609.0, -630.0), 'TOPPING_MODUL__pom[37] evaporatör R ısı kesici'),
    ('raf', (1958.5, 1152.0, -535.0), 'TOPPING_MODUL__paslanmaz[68] kaset kılavuzu'), ('raf', (2218.5, 1152.0, -535.0), 'TOPPING_MODUL__paslanmaz[70] kaset kılavuzu'),
    ('raf', (2295.0, 1152.0, -535.0), 'TOPPING_MODUL__paslanmaz[72] kaset kılavuzu'), ('raf', (2426.0, 1152.0, -535.0), 'TOPPING_MODUL__paslanmaz[74] kaset kılavuzu'),
    ('raf', (1914.0, 1152.0, 7.0), 'TOPPING_MODUL__pom[29] flipper kılavuzu'), ('raf', (1967.5, 1152.0, 7.0), 'TOPPING_MODUL__pom[29] flipper kılavuzu'),
    ('alt_sac', (2351.0, 1109.0, -215.0), 'TOPPING_MODUL__celik[43]'), ('alt_sac', (1454.11, 1109.0, -170.0), 'TOPPING_MODUL__koyu[25]'),
    ('kuru_taban', (2060.0, 1109.0, -740.0), 'HAVA_IC__aski[17]'), ('kuru_taban', (2140.0, 1109.0, -740.0), 'HAVA_IC__aski[19]'),
    ('kuru_taban', (2220.0, 1109.0, -740.0), 'HAVA_IC__aski[21]'), ('kuru_taban', (2300.0, 1109.0, -740.0), 'HAVA_IC__aski[23]'),
    ('kuru_taban', (2380.0, 1109.0, -740.0), 'HAVA_IC__aski[25]'),
]
# PU'ya gömülü kalan v8zq parçaları (PU bunların etrafına dolar): kutu (ad, x0 x1 y0 y1 z0 z1) · silindir (ad, eksen, merkez, r, a0, a1)
GOMULU_KUTU = [("menteşe gövdesi K1", 1437.5, 1465.0, 1500.0, 1570.0, 26.0, 39.0), ("menteşe gövdesi K1", 1437.5, 1465.0, 2060.0, 2130.0, 26.0, 39.0),
               ("menteşe gövdesi K2", 2471.0, 2498.5, 1500.0, 1570.0, 26.0, 39.0), ("menteşe gövdesi K2", 2471.0, 2498.5, 2060.0, 2130.0, 26.0, 39.0),
               ("bas-aç gövdesi", 1927.0, 1957.0, 2160.0, 2190.0, 26.0, 39.0), ("bas-aç gövdesi", 1977.0, 2007.0, 2160.0, 2190.0, 26.0, 39.0),
               ("POM yarık burcu", 1560.0, 1780.0, 1272.0, 1302.0, -630.0, -570.0), ("POM yarık burcu", 1520.0, 1690.0, 1700.0, 1730.0, -630.0, -570.0),
               ("POM yarık burcu", 2200.0, 2330.0, 1700.0, 1730.0, -630.0, -570.0),
               ("kaset mandalı POM", 1951.0, 1975.0, 1124.0, 1149.0, -214.0, -180.0), ("kaset mandalı POM", 2286.0, 2310.0, 1124.0, 1149.0, -214.0, -180.0),
               ("mandal dili", 1956.0, 1970.0, 1144.0, 1149.0, -201.5, -191.5), ("mandal dili", 1960.0, 1966.0, 1126.0, 1144.0, -199.5, -193.5),
               ("mandal dili", 2291.0, 2305.0, 1144.0, 1149.0, -201.5, -191.5), ("mandal dili", 2295.0, 2301.0, 1126.0, 1144.0, -199.5, -193.5),
               ("kaset dili", 2057.5, 2119.5, 1143.0, 1152.0, -180.0, 24.0), ("kaset dili", 2329.5, 2391.5, 1143.0, 1152.0, -180.0, 24.0)]
GOMULU_SIL = [("raf askı burcu", "x", (1128.25, z), 8.13, 1437.5, 1495.0) for z in (-519.885, -359.885, -199.885, -39.885)] + \
             [("raf askı burcu", "x", (1550.5, z), 8.13, 1437.5, 1495.0) for z in (-519.885, -359.885, -199.885, -89.885)] + \
             [("raf askı burcu", "x", (1128.25, z), 8.13, 2441.0, 2498.5) for z in (-519.885, -359.885, -199.885, -39.885)] + \
             [("raf askı burcu", "x", (1550.5, z), 8.13, 2441.0, 2498.5) for z in (-519.885, -359.885, -199.885, -89.885)] + \
             [("POM burç", "z", c, BURC_YUV_D / 2.0, -630.0, -570.0) for c in BURC_YUV]
S._RENK.update({"pu": ((0.95, 0.85, 0.30, 1.0), 0.0, 0.9), "arayuz": ((0.90, 0.22, 0.15, 1.0), 0.3, 0.5), "cerceve": ((0.70, 0.72, 0.74, 1.0), 0.75, 0.35),
                "profil": ((0.70, 0.73, 0.77, 1.0), 0.85, 0.30), "conta": ((0.15, 0.15, 0.16, 1.0), 0.0, 0.8), "pom": ((0.93, 0.93, 0.90, 1.0), 0.0, 0.6)})
# v8zq'da yerine geçilen bileşenler (düğüm, bileşen no) — denetim + entegrasyon
DEGISEN = {"TOPPING_MODUL__sac": sorted(set([30, 17, 20, 19, 18, 21, 22, 23, 24, 25, 26, 27, 28, 98, 99, 87, 88, 94, 95] + list(range(31, 82)))),   # v2: +evaporatör sekmeleri
           "TOPPING_MODUL__paslanmaz": list(range(105, 156)), "TOPPING_MODUL__pu": [0, 1, 2, 3, 4, 5, 6, 7, 10, 11], "KAIDE_C__paslanmaz": "hepsi"}


def kutu(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), V(min(x0, x1), min(y0, y1), min(z0, z1)))


def silindir(p0, eksen, r, L):
    e = np.asarray(eksen, float); e = e / np.linalg.norm(e)
    return cq.Solid.makeCylinder(float(r), float(L), V(*map(float, p0)), V(*map(float, e)))


def _ic(a, b):
    return a.xmin < b.xmax and b.xmin < a.xmax and a.ymin < b.ymax and b.ymin < a.ymax and a.zmin < b.zmax and b.zmin < a.zmax


def yarik_merkez(u0, u1, v0, v1, gen, boy, adim, ara):
    """tgeo.yarik_alani ile aynı dizilim → [(u, v_alt)] (yarık u'da gen, v'de boy)"""
    n = int((u1 - u0 - gen) // adim) + 1
    bas = u0 + ((u1 - u0) - ((n - 1) * adim + gen)) / 2 + gen / 2
    nsat = max(1, int((v1 - v0 + ara) // (boy + ara)))
    top = nsat * boy + (nsat - 1) * ara; vb = v0 + (v1 - v0 - top) / 2
    return [(bas + i * adim, vb + j * (boy + ara)) for j in range(nsat) for i in range(n)]


# =====================================================================================================================================
class G:
    SAC, PROFIL, ELEMAN, KAYNAK, ARAYUZ, PU, KAYNAK_ETIKET, NOT, PU_KES, PU_EK = [], [], [], [], [], [], [], [], [], []
    PANEL, PROF = {}, {}
    STUD_ATLA = []
    kuruldu = False


def _sac(ad, rol, **k):
    s = S.Sac(ad, rol=rol, birim=BIRIM, kaynak=SURUM, **k); G.SAC.append(s); return s


def _eleman(p, mal="celik"):
    p["mal"] = p.get("mal") if p.get("mal") not in (None, "katalog", "paslanmaz") else mal
    p["birim"] = BIRIM; G.ELEMAN.append(p); return p


def _arayuz(p, karsi, gerek, not_=""):
    p["tur"] = "arayuz"; p["arayuz"] = dict(karsi=karsi, gerek=gerek, not_=not_); p["birim"] = BIRIM; G.ARAYUZ.append(p); return p


def _etiket(ad, yontem, olcu, not_):
    G.KAYNAK_ETIKET.append(dict(ad=ad, yontem=yontem, olcu=olcu, not_=not_))


def _ozel(ad, sh, std, tanim, olcu, malzeme="AISI 304", mal="celik", tur="baglanti", meta=None, uretim=True):
    p = S._bp(ad, sh, std, tanim, olcu, malzeme, birim=BIRIM, meta=meta or {}, uretim=uretim, mal=mal)
    p["tur"] = tur; return _eleman(p, mal=mal)


def wloc(P, pts):
    return [tuple(P.yerel(tuple(p))[:2]) for p in pts]


def wrect(P, x0, x1, y0, y1, z0, z1, r=0.0, tip="kesik", parca="", dfm=True):
    q = [P.yerel((x, y, z)) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]
    u = [a[0] for a in q]; v = [a[1] for a in q]
    if tip == "centik":
        P.kesik([(min(u), min(v)), (max(u), min(v)), (max(u), max(v)), (min(u), max(v))], tip=tip, dfm=False, parca=parca); return
    P.dikdortgen((min(u) + max(u)) / 2.0, (min(v) + max(v)) / 2.0, max(u) - min(u), max(v) - min(v), r=r, tip=tip, dfm=dfm, parca=parca)


def wkesik(P, pts3, tip="kesik", parca="", dfm=False):
    P.kesik(wloc(P, pts3), tip=tip, dfm=dfm, parca=parca)


def wdelik(P, p, cap, tip="delik", parca=""):
    q = P.yerel(tuple(p)); P.delik(q[0], q[1], cap, tip=tip, parca=parca)


def kose_rect(P, ax, d, a0, a1, b0, b1, rr, tip, parca):
    """eksen ax'e dik düzlemde (d) dikdörtgen kesik · rr = (sol-alt, sağ-alt, sağ-üst, sol-üst) köşe yarıçapları (a, b eksenlerinde)"""
    o = [i for i in range(3) if i != ax]
    def P3(a, b):
        p = [0.0, 0.0, 0.0]; p[ax] = d; p[o[0]] = a; p[o[1]] = b; return p
    pts = []
    for (ca, cb, r, a_bas) in ((a0, b0, rr[0], 180.0), (a1, b0, rr[1], 270.0), (a1, b1, rr[2], 0.0), (a0, b1, rr[3], 90.0)):
        if r <= 0: pts.append(P3(ca, cb)); continue
        sa = 1.0 if a_bas in (270.0, 0.0) else -1.0; sb = 1.0 if a_bas in (0.0, 90.0) else -1.0
        cx, cy = ca - sa * r, cb - sb * r
        for k in range(9):
            t = math.radians(a_bas + 90.0 * k / 8.0)
            pts.append(P3(cx + r * math.cos(t), cy + r * math.sin(t)))
    P.kesik(wloc(P, pts), tip=tip, dfm=False, parca=parca)


# ------------------------------------------------------------------------------------------- saplama (FHP) güvenli yer denetimi (h3_e_sac_v1 ile aynı)
def _kenar_uzaklik(P, u, v):
    pts = P.poly; d = 1e9
    for i in range(len(pts)):
        a = np.array(pts[i], float); b = np.array(pts[(i + 1) % len(pts)], float); q = np.array([u, v])
        t_ = np.clip(np.dot(q - a, b - a) / max(np.dot(b - a, b - a), 1e-12), 0, 1); d = min(d, float(np.linalg.norm(q - (a + t_ * (b - a)))))
    return d


def _kesik_uzaklik(P, u, v):
    d = 1e9; vx = cq.Vertex.makeVertex(u, v, 0.0)
    for k in P.kesikler:
        if k.tip in ("rahatlatma", "kose_rahatlatma"): continue
        try: d = min(d, k.yuz.distance(vx))
        except Exception: pass
    return d


def guvenli(P, u, v, kenar=11.0, delik=8.0):
    return P.icerir(u, v) and _kenar_uzaklik(P, u, v) >= kenar and _kesik_uzaklik(P, u, v) >= delik


def fhp(P, nokta, yon, karsi, gerek, dis="M5", boy=12, ad=None):
    ya = P.yerel(tuple(nokta))
    head = P.dunya(ya[0], ya[1], 0.0 if np.dot(np.asarray(yon, float), P.normal()) > 0 else P.sac.t)
    sp, c = S.pem_saplama("FHP", dis, boy, head, yon, ad=ad or "arayuz_fhp_%s_%d" % (P.sac.ad, len(G.ARAYUZ)), birim=BIRIM, sac_ad=P.sac.ad)
    k = P.delik(ya[0], ya[1], c["delik"], tip="pem_saplama", parca=sp["meta"]["parca"], pem_tip="FHP", kenar_min=c["kenar"], min_sac=c["min_sac"])
    _arayuz(sp, karsi, gerek, "mekanizma")
    _FHP[sp["ad"]] = (P, k)
    return sp


_FHP = {}


def saplama_duzelt(log=print):
    """ADIM 8: SAPLAMA_CIKAR → saplama (ARAYÜZ) + sacdaki PEM deliği kaldırılır · kur() SONUNDA (diğer saplamaların yeri / adı değişmez)"""
    cik = []
    for ad in SAPLAMA_CIKAR:
        if ad not in _FHP: continue
        P, k = _FHP.pop(ad)
        P.kesikler.remove(k); P.sac._gecersiz()
        G.ARAYUZ[:] = [e for e in G.ARAYUZ if e["ad"] != ad]
        cik.append(ad)
    G.NOT.append("ADIM 8 · çıkarılan FHP saplama (saplama + PEM deliği): %d → %s" % (len(cik), cik))
    log("TOPPING · ADIM 8 saplama düzeltmesi: çıkarılan %d" % len(cik))
    return cik


def pem(P, nokta, yon, dis, ad, kopuk=False):
    """PEM SP somun: P sacına preslenir, gövde 'yon' tarafında"""
    ps, c, ms = S.pem_somun("SP", dis, tuple(nokta), tuple(yon), P.sac.t, ad=ad, birim=BIRIM)
    q = P.yerel(tuple(nokta)); P.delik(q[0], q[1], c["delik"], tip="pem_somun", parca=ps["meta"]["parca"], pem_tip="SP", kenar_min=c["kenar"], min_sac=ms)
    _eleman(ps)
    if kopuk:
        e = np.asarray(yon, float); p0 = np.asarray(nokta, float); Lb = ps["meta"]["T"] - ps["meta"]["sap"]
        cup = cq.Solid.makeCylinder(c["E"] / 2.0 + 0.8, Lb + 0.8, V(*p0), V(*e)).cut(cq.Solid.makeCylinder(c["E"] / 2.0, Lb, V(*p0), V(*e)))
        kp = S._bp(ad + "_kopuk_kapagi", cup, "PE geçme kapak (PEM / Kalei köpük kapağı)", "Köpük kapağı PEM SP-%s · köpüklemeden önce takılır" % dis,
                   "Ø%.1f × %.1f" % (c["E"] + 1.6, Lb + 0.8), "PE-LD", birim=BIRIM, mal="conta")
        kp["tur"] = "baglanti"; _eleman(kp, mal="conta")
        G.PU_KES.append(cq.Solid.makeCylinder(c["E"] / 2.0 + 0.8, Lb + 0.8, V(*p0), V(*e)))
    return ps, c


# =====================================================================================================================================
# 0 · PROFİL (h3_a_sac_v1.Profil ile aynı)
# =====================================================================================================================================
EKSEN = {"x": np.array([1.0, 0, 0]), "y": np.array([0, 1.0, 0]), "z": np.array([0, 0, 1.0])}


class Profil:
    def __init__(self, ad, eksen, a0, a1, c, b1=40.0, b2=100.0, t=2.0, Ro=4.0, not_="", std="Dikdörtgen boru"):
        self.ad, self.eksen, self.a0, self.a1, self.c = ad, eksen, float(a0), float(a1), tuple(map(float, c))
        self.b1, self.b2, self.t, self.Ro, self.not_, self.std = float(b1), float(b2), t, Ro, not_, std
        self.kesikler, self.uc_kaynak, self._sh = [], [], None

    def merkez(self, a):
        p = np.zeros(3); p["xyz".index(self.eksen)] = a
        dik = [k for k in "xyz" if k != self.eksen]
        p["xyz".index(dik[0])], p["xyz".index(dik[1])] = self.c
        return p

    def yari(self, k):
        dik = [q for q in "xyz" if q != self.eksen]
        return (self.b1 if k == dik[0] else self.b2) / 2.0

    def _govde(self):
        dis = S.yuz_dikd_r(0.0, 0.0, self.b1, self.b2, 0.0, self.Ro)
        ic = S.yuz_dikd_r(0.0, 0.0, self.b1 - 2 * self.t, self.b2 - 2 * self.t, 0.0, self.Ro - self.t)
        sh = S._prizma(dis.cut(ic), self.a1 - self.a0)
        dik = [k for k in "xyz" if k != self.eksen]
        ex, ey, ez = EKSEN[dik[0]], EKSEN[dik[1]], EKSEN[self.eksen]
        if np.linalg.det(np.column_stack([ex, ey, ez])) < 0: ey = -ey
        return S._tasi(sh, S._M(np.column_stack([ex, ey, ez]), self.merkez(self.a0)))

    def duvar_delik(self, yuz, a, kayma, cap, tip="delik", not_=""):
        n = EKSEN[yuz[1]] * (1 if yuz[0] == "+" else -1)
        dik = [k for k in "xyz" if k not in (self.eksen, yuz[1])][0]
        p = self.merkez(a) + n * (self.yari(yuz[1]) + 1.0) + EKSEN[dik] * kayma
        cut = silindir(p, -n, cap / 2.0, self.t + 1.6)
        self.kesikler.append(dict(sh=cut, tip=tip, yuz=yuz, a=round(a - self.a0, 2), kayma=kayma, cap=cap, not_=not_, _dik=dik)); self._sh = None

    def kati(self):
        if self._sh is None:
            sh = self._govde()
            for k in self.kesikler: sh = sh.cut(k["sh"])
            self._sh = sh.clean()
        return self._sh

    def dfm(self):
        out = []; L = self.a1 - self.a0
        for k in self.kesikler:
            duz = self.yari(k["_dik"]) - self.Ro; yar = k["cap"] / 2.0
            ok = abs(k["kayma"]) + yar <= duz + 1e-6
            out.append(dict(kural="profil_duz_yuz", durum="GEÇTİ" if ok else "HATA", detay="%s %s %s Ø %.1f kayma %.1f · düz yüz ±%.1f" % (self.ad, k["tip"], k["yuz"], 2 * yar, k["kayma"], duz)))
            uc = min(k["a"] - yar, L - k["a"] - yar)
            out.append(dict(kural="profil_uc", durum="GEÇTİ" if uc >= 3.0 else "HATA", detay="%s %s → boru ucu %.1f (≥ 3)" % (self.ad, k["tip"], uc)))
        out.append(dict(kural="profil_boy", durum="GEÇTİ" if L <= 6000 else "HATA", detay="%s L %.1f ≤ 6000" % (self.ad, L)))
        return out

    def parca(self):
        sh = self.kati(); L = self.a1 - self.a0; kg = sh.Volume() * S.YOGUNLUK
        kes = [dict({k: v for k, v in x.items() if k not in ("sh", "_dik")}) for x in self.kesikler]
        return dict(ad=self.ad, wp=cq.Workplane("XY").add(sh), sh=sh, mal="sac", birim=BIRIM, grup="SABIT", kaynak=SURUM, tur="profil",
                    bom=("%s AISI 304 %g × %g × %g (EN 10219 · dış R %g) · %s" % (self.std, self.b1, self.b2, self.t, self.Ro, self.not_), 1, "L %.1f" % L,
                         "boru lazer / şerit testere 90° · %d kesik · %.2f kg" % (len(kes), kg), "ÜRETİM"),
                    meta=dict(tur="profil", eksen=self.eksen, L=round(L, 2), kesit=[self.b1, self.b2, self.t, self.Ro], kesikler=kes, kg=round(kg, 3)))


def uc_kaynaklari(ad, nokta, yon_ray, yuzler, b, flat, a=2.0):
    e = np.asarray(yon_ray, float); out = []
    for i, nf in enumerate(yuzler):
        nf = np.asarray(nf, float); w = np.cross(e, nf); p = np.asarray(nokta, float) + nf * (b / 2.0)
        out.append(S.kaynak_dikisi(p - w * flat / 2.0, p + w * flat / 2.0, e, nf, a, ad="%s_%d" % (ad, i), birim=BIRIM, taraf="dis (köşe)", not_="boru ucu ↔ boru · TIG 141"))
    return out


# =====================================================================================================================================
# 1 · DIŞ KABUK
# =====================================================================================================================================
def yanlar():
    for tr in ("sol", "sag"):
        s = _sac("dis_yan_%s" % tr, "dis"); g = s.R + s.t
        if tr == "sol":
            P = s.taban([(YB, ZAI + g), (YT, ZAI + g), (YT, ZF), (YB, ZF)], O=(X0, 0, 0), ex=(0, 1, 0), ey=(0, 0, 1), ad="yan")
            arka = P.flans(0, FL, yon=+1, bas=1110.0 - YB, son=YT - 1675.0, ad="arka_donus")       # emiş filtresi (y ≤ 1105) · DIN plakası / pano (x ≥ 1443) arası
            y0, y1, z0, z1 = TABLA_SOL
            pts = [(X0, y0, z0), (X0, y1 - 6.0, z0)] + [(X0, y1 - 6.0 + 6.0 * math.sin(math.radians(a)), z0 + 6.0 - 6.0 * math.cos(math.radians(a))) for a in range(15, 90, 15)] + \
                  [(X0, y1, z0 + 6.0), (X0, y1, z1 - 6.0)] + [(X0, y1 - 6.0 + 6.0 * math.cos(math.radians(a)), z1 - 6.0 + 6.0 * math.sin(math.radians(a))) for a in range(15, 90, 15)] + \
                  [(X0, y1 - 6.0, z1), (X0, y0, z1)]
            wkesik(P, pts, tip="tabla_gecis_agzi", parca="A → TOPPING tabla geçiş ağzı (alta açık · üst köşeler R6 · A sağ yan ağzıyla eş)")
        else:
            P = s.taban([(YB, -ZF), (YT, -ZF), (YT, -ZAI - g), (YB, -ZAI - g)], O=(X1, 0, 0), ex=(0, 1, 0), ey=(0, 0, -1), ad="yan")
            arka = P.flans(2, FL, yon=+1, bas=YT - 2095.0, son=915.0 - YB, ad="arka_donus")         # ana hat geçişinin altında biter
            y0, y1, z0, z1 = TABLA_SAG
            wrect(P, X1, X1 - T, y0, y1, z0, z1, r=3.0, tip="tabla_gecis_agzi", parca="TOPPING → F tabla geçişi (F duvarındaki ağızla eş · silikon conta)")
            a0, a1, b0, b1 = J1["agiz"]
            wrect(P, X1, X1 - T, a0, a1, b0, b1, r=1.0, tip="j1_agzi", parca="J1 birleşim paneli contalı geçiş ağzı 57 × 67 (EPDM kovan geçme payı 0,5)")
            a0, a1, b0, b1 = HAT_GECIS
            wrect(P, X1, X1 - T, a0, a1, b0, b1, r=2.0, tip="hat_gecisi", parca="ana hat kanal geçişi (U_F sol sacındaki ağızla eş · arka kenarı −820)")
        G.PANEL["yan_" + tr] = dict(yan=P, arka=arka, s=s)
    # A ↔ TOPPING: sol yanda PEM SP-M8 (gövde içeride; PU bölgesindekiler köpük kapaklı)
    P = G.PANEL["yan_sol"]["yan"]
    for y, z in M8_A:
        pem(P, (XI0, y, z), (1.0, 0, 0), "M8", "pem_M8_A_%d_%d" % (int(y), int(-z)), kopuk=(z > Z_SA))
    G.NOT.append("A ↔ TOPPING 4 × M8: cıvata A içinden (h3_a_sac_v1 ARAYÜZ) → TOPPING sol yanında PEM SP-M8 (z −300'dekiler köpük kapaklı)")
    # TOPPING ↔ F: sağ yanda PEM SP-M8 · cıvata F içinden (F sol yan sacında Ø9 = ARAYÜZ, h3_u_sac_v1 sahibi)
    P = G.PANEL["yan_sag"]["yan"]
    for y, z in M8_F:
        pem(P, (XI1, y, z), (-1.0, 0, 0), "M8", "pem_M8_F_%d_%d" % (int(y), int(-z)))
        pu = S.pul("DIN9021", "M8", (X1 + 1.5, y, z), (1.0, 0, 0), ad="arayuz_m8_F_%d_%d_pul" % (int(y), int(-z)), birim=BIRIM)
        vd = S.vida("ISO4762", "M8", 16, (X1 + 1.5 + 2.0, y, z), (-1.0, 0, 0), ad="arayuz_m8_F_%d_%d" % (int(y), int(-z)), birim=BIRIM)
        _arayuz(pu, "F sol yan sacı (h3_u_sac_v1 f_ust_yan_sol) iç yüzü", "DIN 9021 M8 (F içinden)", "")
        _arayuz(vd, "F sol yan sacı → TOPPING sağ yanındaki PEM SP-M8",
                "F sol yan sacında Ø9 delik (dünya x 2500 · y %.0f · z %.0f) · ISO 4762 M8 × 16 A2-70 · F içinden alyan 6" % (y, z), "h3_u_sac_v1 sahibi")
    # J1 birleşim paneli burçları: FHP-M5 × 25 (burç + panel plakasından geçer, önde pul + fiberli somun)
    for (u, v) in J1["burc"]:
        y, z = J1["Y0"] + v, J1["c"] + u
        fhp(P, (X1, y, z), (-1.0, 0, 0), "ELK_ZINCIR J1 TOPPING paneli burcu", "burç Ø10 × 20 + panel plakası Ø5,5 · FHP-M5 × 25 · içte pul + fiberli somun",
            boy=25, ad="arayuz_j1_burc_%d_%d" % (int(y), int(-z)))


def tavan():
    s = _sac("dis_tavan", "dis"); g = s.R + s.t
    vp, vf = 629.0, 636.0                                                     # soğuk oda bölgesi dönüşsüz (tam genişlik) · kuru bölmede yan dönüş · arada rahatlatma
    P = s.taban([(XI0, -ZF), (XI1, -ZF), (XI1, vp), (XI1 - g - 0.5, vp), (XI1 - g - 0.5, vf), (XI1 - g, vf), (XI1 - g, -ZAI - g), (XI0 + g, -ZAI - g),
                 (XI0 + g, vf), (XI0 + g + 0.5, vf), (XI0 + g + 0.5, vp), (XI0, vp)], O=(0, YTI, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="tavan")
    sag = P.flans(5, FL, yon=-1, ad="sag_donus")
    arka = P.flans(6, FL, yon=-1, bas=25.0, son=25.0, ad="arka_donus")
    sol = P.flans(7, FL, yon=-1, ad="sol_donus")
    k = TAVAN_YARIK
    for (u, vb) in yarik_merkez(k["u0"], k["u1"], k["v0"], k["v1"], k["gen"], k["boy"], k["adim"], k["ara"]):
        P.dikdortgen(u, -(vb + k["boy"] / 2.0), k["gen"], k["boy"], r=k["gen"] / 2.0 - 0.01, tip="havalandirma", parca="kuru bölme hava çıkış yarığı 5 × 70")
    G.PANEL["tavan"] = dict(tavan=P, sag=sag, arka=arka, sol=sol, s=s)
    for tr, F_, xx in (("sol", sol, XI0), ("sag", sag, XI1)):
        Y = G.PANEL["yan_" + tr]["s"]
        s.punta(Y, [(xx, YTI - 10.0, z) for z in np.arange(-800.0, -640.0, 50.0)], not_="tavan yan dönüşü ↔ yan sac (dış yüzde iz yok: komşu istasyona bakar)")
    _etiket("tavan_yan_dikisi", "TIG 141 aralıklı 30 / 200 (iç köşe, köpüklemeden önce)", "2 × 667 mm", "soğuk oda bölgesinde tavan ↔ yan iç köşesi (dönüş yok)")


def taban():
    s = _sac("dis_taban", "dis"); g = s.R + s.t
    P = s.taban([(XI0 + g, -ZF), (XI1 - g, -ZF), (XI1 - g, -ZAI - g), (XI0 + g, -ZAI - g)], O=(0, YB, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="taban")
    # kenar 1 (sağ, v −39 → 824,75) · kenar 2 (arka, u azalan) · kenar 3 (sol, v azalan)
    sag = P.flans(1, FL, yon=+1, bas=ZF - 20.0, son=0.0, ad="sag_donus")                       # menteşe gövdesi (z 26–39) önünde biter
    arka = P.flans(2, FL, yon=+1, bas=XI1 - g - 2415.0, son=1632.0 - (XI0 + g), ad="arka_donus")   # emiş filtresi (x ≤ 1629,5) ile KD1 kanalı (x ≥ 2421) arası
    sol = P.flans(3, FL, yon=+1, bas=0.0, son=ZF - (-515.0), ad="sol_donus")                     # tabla geçiş ağzının (z ≥ −510) arkasında biter
    for a, b in TABAN_YARIK:
        for (u, vb) in yarik_merkez(a, b, -785.0, -480.5, 5.0, 60.0, 12.0, 20.0):
            P.dikdortgen(u, -(vb + 30.0), 5.0, 60.0, r=2.49, tip="havalandirma", parca="teknik bölme menfez yarığı 5 × 60")
    x0, x1, z0, z1 = CEP
    wrect(P, x0, x1, YB, YBI, z0, z1, tip="cep_agzi", parca="soğutma grubu cebi ağzı (cep duvarları içinden geçer, çevre TIG)")
    x0, x1, z0, z1 = KD1_AGIZ
    wrect(P, x0, x1, YB, YBI, z0, z1, r=2.0, tip="kanal_agzi", parca="KD1 kablo kanalı geçişi")
    for x, z in GOVDE_M6 + RAY_M6:
        wdelik(P, (x, YB, z), 6.6, tip="vida_deligi", parca="gövde / tabla rayı → kaide plakası M6 (ISO 273 orta)")
    G.PANEL["taban"] = dict(taban=P, sag=sag, arka=arka, sol=sol, s=s)
    for tr, xx in (("sol", XI0), ("sag", XI1)):
        Y = G.PANEL["yan_" + tr]["s"]
        zz = np.arange(-800.0, -530.0, 120.0) if tr == "sol" else np.arange(-800.0, 15.0, 120.0)
        s.punta(Y, [(xx, YB + 12.0, z) for z in zz], not_="taban yan dönüşü ↔ yan sac")


def arka_servis():
    s = _sac("dis_arka_servis", "dis")
    P = s.taban([(XI0, YB), (XI1, YB), (XI1, YT), (XI0, YT)], O=(0, 0, ZA), ex=(1, 0, 0), ey=(0, 1, 0), ad="arka")
    a, b, c, d = EMIS_PEN
    P.dikdortgen((a + b) / 2.0, (c + d) / 2.0, b - a, d - c, r=3.0, tip="emis_penceresi", parca="kondenser emiş penceresi (iç yüzde emiş filtresi)")
    G.PANEL["arka"] = dict(arka=P, s=s)
    gs = 2.25 + T
    xs, xg = X0 + gs + (FL - gs) / 2.0, X1 - gs - (FL - gs) / 2.0
    ys_t, ys_b = YT - gs - (FL - gs) / 2.0, YB + gs + (FL - gs) / 2.0
    nok = [("yan_sol", "arka", (xs, y)) for y in (1150.0, 1255.0)] + [("yan_sag", "arka", (xg, y)) for y in (960.0, 1200.0, 1440.0, 1700.0, 1960.0, 2070.0)] + \
          [("tavan", "arka", (x, ys_t)) for x in (1550.0, 1800.0, 2050.0, 2300.0, 2450.0)] + [("taban", "arka", (x, ys_b)) for x in (1700.0, 1950.0, 2200.0, 2380.0)]
    for pan, fl, (x, y) in nok:
        B = G.PANEL[pan][fl]
        dimple_vida(P, B, x, y, "servis_arka_%s_%d_%d" % (pan, int(x), int(y)))
    G.NOT.append("v2 D1 · arka servis sacı: %d × DIN 7991 M5 × 12 havşa başlı · servis sacı + dönüş flanşı birlikte ÇÖKERTİLİR (dimple, iç içe 90° koni, dış yüz düz) · "
                 "dönüşün iç yüzünde kaynak burcu M5 Ø14 × 9 (2 punta TIG) · sacın üzerindeki pano / DIN / filtre / KD3 braketleri FHP ile sacla birlikte sökülür" % len(nok))


# Kemal 4 Eki: "uzatacaksa olmasın" → iç sac yanlarının ön kenarı ters büküm: KAZ BOYNU BIÇAK KABUL (ayrı profil yok) · DFM'de hata sayılmaz
DFM_KABUL = {"astar_sol": {"abkant": "kabul edildi — kaz boynu bıçak (Kemal 4 Eki)"}, "astar_sag": {"abkant": "kabul edildi — kaz boynu bıçak (Kemal 4 Eki)"}}
DIMPLE = []          # (sac adı, 'kes' | 'ekle', katı) — govde_parcalari() açınımdan SONRA uygular (çökertme = lazer + delik sonrası pres)


def _koni(p0, d, s, r0=5.0, r1=2.45, h=2.8, uzat=0.0):
    """havşa konisi K(s) = DIN 7991 M5 baş konisi (Ø10 → Ø4,9 · k 2,8 · h3_sac_v1.vida ile aynı) eksen boyunca s kaydırılmış · uzat: ters yönde silindir"""
    p0 = np.asarray(p0, float); d = np.asarray(d, float)
    k = cq.Solid.makeCone(r0, r1, h, V(*(p0 + d * s)), V(*d))
    if uzat > 0: k = k.fuse(cq.Solid.makeCylinder(r0, uzat, V(*(p0 + d * s - d * uzat)), V(*d)))
    return k


def dimple_vida(P, B, x, y, ad):
    """D1 · çökertme havşa: servis sacı (A, 1,5) + dönüş (B, 1,5) iç içe 90° dimple · DIN 7991 M5 × 12 · B iç yüzünde kaynak burcu M5"""
    d = np.array([0, 0, 1.0]); p0 = np.array([x, y, ZA]); tA, tB = P.sac.t, B.sac.t
    wdelik(P, (x, y, ZA), 5.5, tip="vida_deligi", parca="ISO 273 orta (dimple öncesi delik)")
    wdelik(B, (x, y, ZA + tA), 5.5, tip="vida_deligi", parca="ISO 273 orta (dimple öncesi delik)")
    del_ = cq.Solid.makeCylinder(2.75, 20.0, V(*(p0 - d * 1.0)), V(*d))
    kat = lambda z0, z1: cq.Solid.makeBox(30.0, 30.0, z1 - z0, V(x - 15.0, y - 15.0, ZA + z0))
    K0, K1, K2 = _koni(p0, d, 0.0, uzat=1.0), _koni(p0, d, tA), _koni(p0, d, tA + tB)
    DIMPLE.append((P.sac.ad, "kes", K0))
    DIMPLE.append((P.sac.ad, "ekle", K1.cut(K0).cut(del_).intersect(kat(tA, tA + 4.0))))
    DIMPLE.append((B.sac.ad, "kes", K1.intersect(kat(tA, tA + tB))))
    DIMPLE.append((B.sac.ad, "ekle", K2.cut(K1).cut(del_).intersect(kat(tA + tB, tA + tB + 4.0))))
    # kaynak burcu M5 Ø14 × 9 · alt yüzü K2 kadar havşalı (dimple çıkıntısı içine oturur)
    z1 = ZA + tA + tB
    bur = cq.Solid.makeCylinder(7.0, 9.0, V(x, y, z1), V(0, 0, 1.0)).cut(K2).cut(cq.Solid.makeCylinder(2.5, 12.0, V(x, y, z1 - 1.0), V(0, 0, 1.0))).clean()
    p = S._bp(ad + "_burc", bur, "özel imalat (torna) · AISI 304", "Kaynak burcu M5 Ø14 × 9 · alt yüzü 90° havşalı (dimple'a oturur) · dönüşe 2 punta TIG",
              "Ø14 × 9 · M5 diş 9", "AISI 304", birim=BIRIM, mal="paslanmaz", uretim=True, meta=dict(dis="M5", tip="kaynak_burcu"))
    _eleman(p)
    for k, a in enumerate((0.5 * math.pi, 1.5 * math.pi) if '_yan_' in ad else (0.0, math.pi)):      # punta flanş boyunca (büküm tarafına değil)
        c = (x + 8.45 * math.cos(a), y + 8.45 * math.sin(a))
        sh = cq.Solid.makeCylinder(1.4, 1.2, V(c[0], c[1], z1), V(0, 0, 1.0))
        _ozel(ad + "_burc_punta_%d" % k, sh, "TIG 141 · ER308LSi", "Kaynak burcu ↔ dönüş punta", "Ø3 × 1,2", mal="sac", tur="kaynak",
              meta=dict(tur="kaynak", tip="punta", yontem="TIG 141"))
    _eleman(S.vida("DIN7991", "M5", 12, tuple(p0), tuple(d), ad=ad + "_vida", birim=BIRIM))


# =====================================================================================================================================
# 2 · SOĞUK ODA
# =====================================================================================================================================
def on_cerceve():
    s = _sac("on_cerceve_430", "ic", t=1.0, malzeme="AISI 430 (1.4016) ferritik, 2B · manyetik fitil yüzeyi", mal="cerceve")
    poly = [(XI0, 963.5), (1467.5, 963.5), (1467.5, Y_SO), (2468.5, Y_SO), (2468.5, 963.5), (XI1, 963.5), (XI1, 1500.0), (2471.0, 1500.0), (2471.0, 1570.0),
            (XI1, 1570.0), (XI1, 2060.0), (2471.0, 2060.0), (2471.0, 2130.0), (XI1, 2130.0), (XI1, YTI), (XI0, YTI), (XI0, 2130.0), (1465.0, 2130.0),
            (1465.0, 2060.0), (XI0, 2060.0), (XI0, 1570.0), (1465.0, 1570.0), (1465.0, 1500.0), (XI0, 1500.0)]
    P = s.taban(poly, O=(0, 0, ZFC), ex=(1, 0, 0), ey=(0, 1, 0), ad="cerceve")
    ag = [(2057.0, 1152.0), (2057.0, 1142.5), (2120.0, 1142.5), (2120.0, 1152.0), (2329.0, 1152.0), (2329.0, 1142.5), (2392.0, 1142.5), (2392.0, 1152.0),
          (2440.0, 1152.0), (2440.0, 2140.0), (1496.0, 2140.0), (1496.0, 1152.0)]
    P.kesik(ag, tip="soguk_oda_agzi", dfm=False, parca="soğuk oda ağzı 944 × 988 + kaset dili kanalları")
    for x in (1942.0, 1992.0):
        P.dikdortgen(x, 2175.0, 30.0, 30.0, tip="basac", parca="kanat bas-aç gövdesi geçişi")
    G.PANEL["cerceve"] = P
    _etiket("on_cerceve_cevre_dikisi", "TIG 141 dikiş 20 / 150 + gıda silikonu", "çevre ≈ 6,7 m", "çerçeve kenarı ↔ yan / tavan / alt sac (kapak arkasında)")


def alt_sac():
    s = _sac("soguk_alt_sac", "dis")
    P = s.taban([(XI0, -ZFC), (XI1, -ZFC), (XI1, -(Z_SA + T)), (XI0, -(Z_SA + T))], O=(0, Y_SO, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="alt")
    for x, z in DUSME_KARE: wrect(P, x - 19.0, x + 19.0, Y_SO, Y_SO + T, z - 19.0, z + 19.0, tip="dusme_deligi", parca="kıyma / kuşbaşı düşme deliği 38 × 38 (kovan içi)")
    for x, z in DUSME_YUV: wdelik(P, (x, Y_SO, z), 31.0, tip="dusme_deligi", parca="sos / harç düşme deliği Ø31 (boru içi)")
    for xc in DUSME_ARTI:
        wkesik(P, [(xc + a, Y_SO, b) for a, b in ARTI_IC], tip="dusme_deligi", parca="kaşar / sucuk düşme deliği (artı kesit, POM kovan içi)")
    G.PANEL["alt_sac"] = P


def soguk_arka():
    s = _sac("soguk_arka_dis_sac", "dis")
    P = s.taban([(XI0, Y_SO), (XI1, Y_SO), (XI1, YTI), (XI0, YTI)], O=(0, 0, Z_SA), ex=(1, 0, 0), ey=(0, 1, 0), ad="arka")
    _gecisler(P, Z_SA, kanal_delik=True)
    G.PANEL["soguk_arka"] = P


def _gecisler(P, z, kanal_delik):
    for x, y in BURC_YUV: wkesik(P, [(x + a, y + b, z) for a, b in BURC_YUV_POLY], tip="burc_deligi", parca="UNO pistonu hortum burcu (POM, v8zq kesiti)")
    for x, y in MOTOR_BURC: wkesik(P, [(x + a, y + b, z) for a, b in MOTOR_LOB], tip="burc_deligi", parca="kaset motor kavrama burcu (POM, v8zq)")
    for a, b, c, d in BURC_YARIK: wrect(P, a, b, c, d, z, z + 1.0, tip="burc_deligi", parca="pnömatik hortum yarık burcu (POM, v8zq)")
    gr = 1.5 + 1.0
    for i, (a, b, c, d) in enumerate(EVAP_KAN):
        if kanal_delik:
            kose_rect(P, 2, z, a, b, c, d, (gr, 0.0, gr, 0.0), tip="evap_kanal_agzi", parca="evaporatör hava kanalı kovanı geçişi (kovan dış ölçüsü)")
        else:
            ia, ib, ic_, id_ = a + 1.0, b - 1.0, c + 1.0, d - 1.0
            for (u, vb) in yarik_merkez(ia + 2.0, ib - 2.0, ic_ + 4.0, id_ - 4.0, 6.0, id_ - ic_ - 8.0, 12.0, 20.0):
                q = P.yerel((u, vb + (id_ - ic_ - 8.0) / 2.0, z))
                P.dikdortgen(q[0], q[1], 6.0, id_ - ic_ - 8.0, r=2.99, tip="havalandirma", parca="evaporatör hava kanalı ağzı lazer yarık (gıda)")


def astar():
    """v2 D2 · bükümlü kenarlı iç sac (304 1,0 · R 1) + kör perçin + POM ısı kesici pul (TIG YOK) — sıra: arka PU → yan PU → tavan PU → sol / sağ
    astar (önden; arka kenar arka levhanın yivine, üst kenar tavan levhasının yivine) → tavan astarı (önden, yanların üst kenarının altına) → arka astar
    (önden, en son) → içeriden perçinler → ön çerçeve (çerçeveden gömme perçin) → derz silikonu"""
    a = AST; t = a["t"]; R = R_GIDA; g = R + t                 # gıda: iç R ≥ 3 (standart) · arka flanşı raf (y < 1155) ve üst raf (1530–1580) hizasında kesik
    ZB, ZON, YUST = -573.0, 37.0, 2143.0                       # yan / tavan arka flanşı dış yüzü · ön flanş dış yüzü · yan üst flanş dış yüzü
    for tr in ("sol", "sag"):
        s = _sac("astar_%s" % tr, "ic", t=t, R=R, bolge="gida")
        if tr == "sol":
            P = s.taban([(a["y0"], ZB + g), (1530.0, ZB + g), (1580.0, ZB + g), (YUST - g, ZB + g), (YUST - g, ZON - g), (a["y0"], ZON - g)], O=(1495.0, 0, 0),
                        ex=(0, 1, 0), ey=(0, 0, 1), ad="sol")
            arka = P.flans(0, 20.0, yon=+1, bas=1155.0 - a["y0"], son=4.0, ad="arka_flans_alt")
            arka2 = P.flans(2, 20.0, yon=+1, bas=4.0, son=YUST - g - 2112.0, ad="arka_flans_ust")
            ust = P.flans(3, 20.0, yon=+1, bas=4.0, son=0.0, ad="ust_flans")
            on = P.flans(4, 20.0, yon=-1, bas=0.0, ad="on_flans")
        else:
            P = s.taban([(a["y0"], -(ZON - g)), (YUST - g, -(ZON - g)), (YUST - g, -(ZB + g)), (1580.0, -(ZB + g)), (1530.0, -(ZB + g)), (a["y0"], -(ZB + g))],
                        O=(2441.0, 0, 0), ex=(0, 1, 0), ey=(0, 0, -1), ad="sag")
            on = P.flans(0, 20.0, yon=-1, son=0.0, ad="on_flans")
            ust = P.flans(1, 20.0, yon=+1, bas=0.0, son=4.0, ad="ust_flans")
            arka2 = P.flans(2, 20.0, yon=+1, bas=YUST - g - 2112.0, son=4.0, ad="arka_flans_ust")
            arka = P.flans(4, 20.0, yon=+1, bas=4.0, son=1155.0 - a["y0"], ad="arka_flans_alt")
        G.PANEL["astar_" + tr] = dict(yan=P, arka=arka, arka2=arka2, ust=ust, on=on, s=s)
    for y0, y1, fl in ((1336.5, 1498.5, "arka"), (1584.0, 1638.5, "arka2")):
        wrect(G.PANEL["astar_sol"][fl], 1501.5, 1516.0, y0, y1, ZB - 0.5, ZB + t + 0.5, tip="centik", parca="evaporatör kanal kovanı çentiği")
    s = _sac("astar_tavan", "ic", t=t, R=R, bolge="gida")
    P = s.taban([(1497.6, ZB + g), (2438.4, ZB + g), (2438.4, ZON - g), (1497.6, ZON - g)], O=(0, a["y1"], 0), ex=(1, 0, 0), ey=(0, 0, 1), ad="tavan")
    arka = P.flans(0, 20.0, yon=+1, bas=22.4, son=22.4, ad="arka_flans")
    on = P.flans(2, 18.0, yon=-1, bas=2.0, son=2.0, ad="on_flans")
    G.PANEL["astar_tavan"] = dict(yan=P, arka=arka, on=on, s=s)
    s = _sac("astar_arka", "ic", t=t, R=R, bolge="gida")
    P = s.taban([(1496.8, a["y0"]), (2439.2, a["y0"]), (2439.2, a["y1"] - 2.0), (1496.8, a["y1"] - 2.0)], O=(0, 0, a["zb"]), ex=(1, 0, 0), ey=(0, 1, 0), ad="arka")
    _gecisler(P, a["zb"], kanal_delik=False)
    G.PANEL["astar_arka"] = dict(yan=P, s=s)
    Ys = [1190.0, 1300.0, 1660.0, 1800.0, 1950.0, 2090.0]
    J = []
    for tr, xr in (("sol", 1507.0), ("sag", 2429.0)):
        for y in Ys: J.append(("arka_%s" % tr, G.PANEL["astar_arka"]["yan"], G.PANEL["astar_" + tr]["arka" if y < 1530 else "arka2"], (xr, y, -570.0), (0, 0, -1.0), "kor"))
        for z in (-520.0, -380.0, -240.0, -100.0, 10.0):
            J.append(("tavan_%s" % tr, G.PANEL["astar_tavan"]["yan"], G.PANEL["astar_" + tr]["ust"], (xr, 2140.0, z), (0, 1.0, 0), "kor"))
    for x in (1560.0, 1720.0, 1880.0, 2050.0, 2220.0, 2380.0):
        J.append(("arka_tavan", G.PANEL["astar_arka"]["yan"], G.PANEL["astar_tavan"]["arka"], (x, 2130.0, -570.0), (0, 0, -1.0), "kor"))
    Yon = [1200.0, 1340.0, 1480.0, 1620.0, 1760.0, 1900.0, 2040.0]
    for tr, xo in (("sol", 1485.0), ("sag", 2451.0)):
        for y in Yon: J.append(("cerceve_%s" % tr, G.PANEL["cerceve"], G.PANEL["astar_" + tr]["on"], (xo, y, ZFC + 1.0), (0, 0, -1.0), "havsa"))
    for x in (1560.0, 1720.0, 1880.0, 2050.0, 2220.0, 2380.0):
        J.append(("cerceve_tavan", G.PANEL["cerceve"], G.PANEL["astar_tavan"]["on"], (x, 2150.0, ZFC + 1.0), (0, 0, -1.0), "havsa"))
    n = 0
    for ad, A, B, p, d, tip in J:
        _percin(A, B, np.asarray(p, float), np.asarray(d, float), tip, "astar_percin_%s_%d" % (ad, n)); n += 1
    G.NOT.append("v2 D2 · iç sac 4 bükümlü sac, %d perçin (ISO 15983 Ø3,2 içeriden · ISO 15984 havşa Ø3,2 çerçeveden) + %d POM-C ısı kesici pul Ø9 × 1 · TIG yok" % (n, n))


def _percin(A, B, p, d, tip, ad):
    """A (baş tarafı) · 1,0 POM pul · B · p: baş tarafı dış yüz noktası · d: içeri"""
    tA, tB = A.sac.t, B.sac.t
    wdelik(A, tuple(p), 3.3, tip="kor_percin", parca="ISO 15983 / 15984 Ø3,2 perçin deliği")
    wdelik(B, tuple(p + d * (tA + 1.0)), 3.3, tip="kor_percin", parca="ISO 15983 / 15984 Ø3,2 perçin deliği")
    kav = tA + 1.0 + tB
    pul = cq.Solid.makeCylinder(4.5, 1.0, V(*(p + d * tA)), V(*d)).cut(cq.Solid.makeCylinder(1.7, 3.0, V(*(p + d * (tA - 1.0))), V(*d)))
    if tip == "havsa":
        bas = cq.Solid.makeCone(3.0, 1.6, 1.4, V(*p), V(*d))
        DIMPLE.append((A.sac.ad, "kes", bas.fuse(cq.Solid.makeCylinder(3.0, 1.0, V(*(p - d * 1.0)), V(*d)))))
        pul = pul.cut(bas)
        sh = bas.fuse(cq.Solid.makeCylinder(1.57, 6.0, V(*p), V(*d))).fuse(cq.Solid.makeCylinder(2.16, 1.2, V(*(p + d * kav)), V(*d))).clean()
        pr = S._bp(ad, sh, "ISO 15984", "Havşa başlı kör perçin Ø3,2 × 6 A2/A2 (çerçeve dış yüzüyle aynı düzlem · kapak fitili oturur)", "delik Ø3,3 · havşa 90°",
                   "A2/A2", birim=BIRIM, meta=dict(cap=3.2, boy=6, delik=3.3, kavrama=kav))
    else:
        pr = S.kor_percin(3.2, 8, tuple(p), tuple(d), ad=ad, birim=BIRIM, kavrama=kav)
        pr["bom"] = ("Kör perçin Ø3,2 × 8 bombe baş A2/A2 · kapalı uçlu (gıda tarafı sızdırmaz)",) + tuple(pr["bom"][1:])
    _eleman(pr)
    pp = S._bp(ad + "_pul", pul.clean(), "POM-C (FDA) · zımba", "Isı kesici ara pul Ø9 × 1 POM-C (iç sac ↔ dış parça arası soğuk köprü kesici)",
               "Ø9 / Ø3,4 × 1", "POM-C", birim=BIRIM, mal="pom")
    pp["tur"] = "baglanti"; _eleman(pp, mal="pom")


def derz_silikonu():
    """gıda tarafı iç köşeler 3 × 3 üçgen fitil + ön derz (iç sacın ön bükümü ↔ ön çerçeve arkası) dolgu · on_cerceve'den sonra çağrılır"""
    def fitil(ad, p0, p1, u, v, a_=1.0):
        p0 = np.asarray(p0, float); p1 = np.asarray(p1, float); u = np.asarray(u, float) * a_; v = np.asarray(v, float) * a_
        w = cq.Wire.makePolygon([V(*p0), V(*(p0 + u)), V(*(p0 + v))], close=True)
        sh = cq.Solid.extrudeLinear(cq.Face.makeFromWires(w), V(*(p1 - p0)))
        p = S._bp(ad, sh, "gıda sınıfı silikon (FDA 21 CFR 177.2600)", "Derz silikonu 3 × 3 (gıda tarafı iç köşe)", "%.0f mm" % np.linalg.norm(p1 - p0),
                  "VMQ silikon", birim=BIRIM, mal="conta")
        p["tur"] = "silikon"; G.ELEMAN.append(p)
    for tr, x, u in (("sol", 1496.0, 1.0), ("sag", 2440.0, -1.0)):
        fitil("derz_arka_%s_alt" % tr, (x + 0.8 * u, 1152.0, -570.0), (x + 0.8 * u, 1533.0, -570.0), (3.0 * u, 0, 0), (-0.8 * u, 0, 3.0))
        fitil("derz_arka_%s_ust" % tr, (x + 0.8 * u, 1576.0, -570.0), (x + 0.8 * u, 2136.0, -570.0), (3.0 * u, 0, 0), (-0.8 * u, 0, 3.0))
        fitil("derz_tavan_%s" % tr, (x + 1.6 * u, 2140.0, -566.0), (x + 1.6 * u, 2140.0, 37.5), (3.0 * u, 0, 0), (-1.6 * u, -3.0, 0))
    fitil("derz_arka_tavan", (1500.0, 2140.0, -569.0), (2436.0, 2140.0, -569.0), (0, 0, 3.0), (0, -3.0, -1.0))
    saclar = [s.kati() for s in G.SAC if s.ad.startswith(("astar", "on_cerceve"))]
    pul = [e["sh"] for e in G.ELEMAN if e["ad"].startswith("astar_percin")]
    for tr, x0, x1 in (("sol", 1494.5, 1497.5), ("sag", 2438.5, 2441.5)):
        for k, (y0, y1) in enumerate(((AST["y0"], 1157.0), (1528.0, 1582.0))):
            sh = kutu(x0, x1, y0, y1, -571.5, -568.5).cut(*[q.kati() for q in G.SAC]).cut(*pul).cut(*[e["sh"] for e in G.ELEMAN if e["ad"].startswith(("derz_", "raf_arka_kose"))]).clean()
            for j, so in enumerate(sh.Solids()):
                if so.Volume() < 1.0: continue
                p = S._bp("derz_kose_%s_%d_%d" % (tr, k, j), so, "gıda sınıfı silikon (FDA 21 CFR 177.2600)", "Köşe dolgu silikonu (yan iç sacın arka kenarı kesik bölgede)",
                          "%.1f cm³" % (so.Volume() / 1e3), "VMQ silikon", birim=BIRIM, mal="conta")
                p["tur"] = "silikon"; G.ELEMAN.append(p)
    for ad, bx in (("derz_on_sol", kutu(1493.5, 1496.0, AST["y0"], 2140.0, 34.0, ZFC)), ("derz_on_sag", kutu(2440.0, 2442.5, AST["y0"], 2140.0, 34.0, ZFC)),
                   ("derz_on_tavan", kutu(1496.0, 2440.0, 2140.0, 2142.5, 34.0, ZFC))):
        sh = bx.cut(*saclar).cut(*pul).clean()
        for k, so in enumerate(sh.Solids()):
            if so.Volume() < 1.0: continue
            p = S._bp("%s_%d" % (ad, k), so, "gıda sınıfı silikon (FDA 21 CFR 177.2600)", "Ön derz silikonu (iç sac ön bükümü ↔ ön çerçeve arkası)",
                      "%.1f cm³" % (so.Volume() / 1e3), "VMQ silikon", birim=BIRIM, mal="conta")
            p["tur"] = "silikon"; G.ELEMAN.append(p)


def kovan_z(ad, x0, x1, y0, y1, z0, z1, t=1.0):
    """z eksenli dikdörtgen kovan = iki L (L1: alt + sol · L2: üst + sağ) · iki boyuna TIG (köşe dolgusu modellendi)"""
    s1 = _sac(ad + "_L1", "ic", t=t); g = s1.R + s1.t
    A = s1.taban([(x0 + g, -z1), (x1 - t, -z1), (x1 - t, -z0), (x0 + g, -z0)], O=(0, y0, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="alt")
    A.flans(3, (y1 - t) - y0, yon=+1, ad="sol")
    s2 = _sac(ad + "_L2", "ic", t=t)
    B = s2.taban([(x0 + t, z0), (x1 - g, z0), (x1 - g, z1), (x0 + t, z1)], O=(0, y1, 0), ex=(1, 0, 0), ey=(0, 0, 1), ad="ust")
    B.flans(1, y1 - (y0 + t), yon=+1, ad="sag")
    for k, (xa, ya) in enumerate(((x1 - t, y0), (x0, y1 - t))):
        sh = kutu(xa, xa + t, ya, ya + t, z0, z1)
        _ozel("%s_boyuna_kaynak_%d" % (ad, k), sh, "TIG 141 · ER308LSi", "Kovan boyuna köşe dikişi (köpük sızdırmaz)", "%.0f mm" % (z1 - z0), mal="sac", tur="kaynak",
              meta=dict(tur="kaynak", tip="kose", boy=z1 - z0, yontem="TIG 141"))


def kovan_y(ad, x0, x1, z0, z1, y0, y1, t):
    """y eksenli kare kovan = iki L (L1: ön + sol · L2: arka + sağ)"""
    s1 = _sac(ad + "_L1", "ic", t=t)
    g = s1.R + s1.t
    A = s1.taban([(x0 + g, -y1), (x1 - t, -y1), (x1 - t, -y0), (x0 + g, -y0)], O=(0, 0, z1), ex=(1, 0, 0), ey=(0, -1, 0), ad="on")
    A.flans(3, z1 - (z0 + t), yon=+1, ad="sol")
    s2 = _sac(ad + "_L2", "ic", t=t)
    B = s2.taban([(x0 + t, y0), (x1 - g, y0), (x1 - g, y1), (x0 + t, y1)], O=(0, 0, z0), ex=(1, 0, 0), ey=(0, 1, 0), ad="arka")
    B.flans(1, (z1 - t) - z0, yon=+1, ad="sag")
    for k, (xa, za) in enumerate(((x1 - t, z1 - t), (x0, z0))):
        sh = kutu(xa, xa + t, y0, y1, za, za + t)
        _ozel("%s_boyuna_kaynak_%d" % (ad, k), sh, "TIG 141 · ER308LSi", "Kovan boyuna köşe dikişi", "%.0f mm" % (y1 - y0), mal="sac", tur="kaynak",
              meta=dict(tur="kaynak", tip="kose", boy=y1 - y0, yontem="TIG 141"))


def evap_kovanlari():
    for i, (a, b, c, d) in enumerate(EVAP_KAN):
        kovan_z("evap_kanal_kovani_%d" % i, a, b, c, d, Z_SA, AST["zb"], t=1.0)


def dusme_kovanlari():
    for k, (x, z) in enumerate(DUSME_KARE):
        kovan_y("dusme_kovani_%s" % ("kiyma", "kusbasi")[k], x - 22.0, x + 22.0, z - 22.0, z + 22.0, Y_SO + T, 1149.0, t=3.0)
    for k, (x, z) in enumerate(DUSME_YUV):
        sh = silindir((x, Y_SO + T, z), (0, 1, 0), 19.0, 1149.0 - Y_SO - T).cut(silindir((x, Y_SO, z), (0, 1, 0), 15.5, 50.0))
        _ozel("dusme_kovani_%s" % ("sos", "harc")[k], sh, "EN 10217-7 / ISO 1127 kalın et boru", "Düşme kovanı boru Ø38 × 3,5 AISI 304 (iç Ø31) · alt sac + raf altına TIG",
              "Ø38 × 3,5 × 37,5", mal="sac", tur="baglanti")
    for k, xc in enumerate(DUSME_ARTI):
        ic = cq.Wire.makePolygon([V(xc + a, Y_SO + T, b) for a, b in ARTI_IC], close=True)
        dis_p = [(-40.0, -162.0), (-34.5, -162.0), (-34.5, -183.5), (34.5, -183.5), (34.5, -162.0), (40.0, -162.0), (40.0, -138.0), (34.5, -138.0),
                 (34.5, -116.0), (-34.5, -116.0), (-34.5, -138.0), (-40.0, -138.0)]
        dw = cq.Wire.makePolygon([V(xc + a, Y_SO + T, b) for a, b in dis_p], close=True)
        govde = cq.Solid.extrudeLinear(cq.Face.makeFromWires(dw, [ic]), V(0, 1143.0 - Y_SO - T, 0))
        dw2 = cq.Wire.makePolygon([V(xc + a, 1143.0, b) for a, b in dis_p], close=True)
        ic2 = cq.Wire.makePolygon([V(xc + a, 1143.0, b) for a, b in ARTI_IC], close=True)
        yaka = cq.Solid.extrudeLinear(cq.Face.makeFromWires(dw2, [ic2]), V(0, 6.0, 0)).cut(kutu(xc - 31.5, xc + 31.5, 1142.0, 1150.0, -180.5, -100.0))
        sh = govde.fuse(yaka).clean()
        _ozel("dusme_kovani_%s" % ("kasar", "sucuk")[k], sh, "POM-C (FDA 21 CFR 177.2470) CNC", "Kaşar / sucuk düşme kovanı · artı kesit, et 1,0 · üst yaka kaset dili yuvalı (1143–1149) · köpüklemeden önce yerleştirilir",
              "80 × 67,5 × 37,5", malzeme="POM-C gıda sınıfı", mal="pom", tur="baglanti")
    _etiket("dusme_kovanlari_dikisi", "TIG 141 (köpük sızdırmaz) / POM: gıda silikonu", "6 kovan × 2 çevre", "kovan ↔ alt sac üstü ve raf altı")


def raf():
    t = 3.0
    s = _sac("raf", "ic", t=t, bolge="gida"); g = s.R + s.t
    vf, vb = -(23.0 - g), 570.0 - g
    n1, n2 = DIL_X
    poly = [(1496.0, vf), (n1[0], vf), (n1[0], 181.0), (n1[1], 181.0), (n1[1], vf), (n2[0], vf), (n2[0], 181.0), (n2[1], 181.0), (n2[1], vf), (2440.0, vf),
            (2440.0, vb), (1496.0, vb)]
    P = s.taban(poly, O=(0, 1149.0, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="raf")
    boy = 1152.0 - (Y_SO + T)
    for k in (0, 4, 8): P.flans(k, boy, yon=-1, ad="on_bukum_%d" % k)
    P.flans(10, boy, yon=-1, ad="arka_bukum")
    for x, z, d in RAF_DELIK: wdelik(P, (x, 1149.0, z), d, tip="dusme_deligi", parca="düşme deliği (raf contası yuvası, v8zq)")
    for x, z in RAF_MANDAL: wrect(P, x - 4.5, x + 4.5, 1149.0, 1152.0, z - 3.5, z + 3.5, tip="mandal_yarigi", parca="kaset kilit mandalı dili yarığı 9 × 7")
    G.PANEL["raf"] = P
    for tr in ("sol", "sag"):
        k = _sac("raf_kosebendi_%s" % tr, "ic", t=t, bolge="gida"); gk = k.R + k.t
        if tr == "sol":
            Q = k.taban([(Y_SO + T, -561.0), (1149.0 - gk, -561.0), (1149.0 - gk, 14.0), (Y_SO + T, 14.0)], O=(1496.0, 0, 0), ex=(0, 1, 0), ey=(0, 0, 1), ad="dik")
        else:
            Q = k.taban([(Y_SO + T, -14.0), (1149.0 - gk, -14.0), (1149.0 - gk, 561.0), (Y_SO + T, 561.0)], O=(2440.0, 0, 0), ex=(0, 1, 0), ey=(0, 0, -1), ad="dik")
        Q.flans(1, 38.0, yon=+1, ad="yatay")
        k.punta(s, [(1516.0 if tr == "sol" else 2420.0, 1149.0, z) for z in (-500.0, -250.0, 0.0)], not_="köşebent yatay kolu ↔ raf altı")
    _etiket("raf_cevre_dikisi", "TIG 141 sürekli + R3 taşlama (gıda)", "2 × 593 mm", "raf yan kenarları ↔ astar sol / sağ (iç köşe)")


def ust_raf():
    t = 3.0
    s = _sac("ust_raf", "ic", t=t, bolge="gida"); g = s.R + s.t
    P = s.taban([(1496.0, -(-50.0 - g)), (2440.0, -(-50.0 - g)), (2440.0, 570.0 - g), (1496.0, 570.0 - g)], O=(0, 1572.0, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="raf")
    boy = 1575.0 - 1534.0
    P.flans(0, boy, yon=-1, ad="on_bukum"); P.flans(2, boy, yon=-1, ad="arka_bukum")
    for x, z, d in UST_RAF_DELIK: wdelik(P, (x, 1572.0, z), d, tip="hortum_deligi", parca="harç / sos hortumu geçişi")
    for tr in ("sol", "sag"):
        k = _sac("ust_raf_kosebendi_%s" % tr, "ic", t=t, bolge="gida"); gk = k.R + k.t
        if tr == "sol":
            Q = k.taban([(1534.0, -561.0), (1572.0 - gk, -561.0), (1572.0 - gk, -59.0), (1534.0, -59.0)], O=(1496.0, 0, 0), ex=(0, 1, 0), ey=(0, 0, 1), ad="dik")
        else:
            Q = k.taban([(1534.0, 59.0), (1572.0 - gk, 59.0), (1572.0 - gk, 561.0), (1534.0, 561.0)], O=(2440.0, 0, 0), ex=(0, 1, 0), ey=(0, 0, -1), ad="dik")
        Q.flans(1, 40.0, yon=+1, ad="yatay")
        k.punta(s, [(1516.0 if tr == "sol" else 2420.0, 1572.0, z) for z in (-450.0, -150.0)], not_="köşebent ↔ üst raf")
    _etiket("ust_raf_kosebent_dikisi", "TIG 141 aralıklı 30 / 100 + taşlama (gıda)", "4 × 514 mm", "üst raf köşebentleri ↔ astar sol / sağ")


def esik_ve_dil():
    t = 1.2
    s = _sac("soguk_esik", "ic", t=t, R=R_GIDA, bolge="gida"); g = s.R + s.t
    yt = 1152.0 - g; yn = 1141.4
    n1, n2 = DIL_X
    poly = [(1496.0, Y_SO + T), (2440.0, Y_SO + T), (2440.0, yt), (n2[1], yt), (n2[1], yn), (n2[0], yn), (n2[0], yt), (n1[1], yt), (n1[1], yn), (n1[0], yn),
            (n1[0], yt), (1496.0, yt)]
    P = s.taban(poly, O=(0, 0, 36.8), ex=(1, 0, 0), ey=(0, 1, 0), ad="on")
    for k in (2, 6, 10): P.flans(k, 38.0 - 23.0, yon=-1, ad="ust_%d" % k)
    G.PANEL["esik"] = P
    _etiket("dil_kanali_dikisi", "TIG 141 + taşlama (gıda)", "2 × 2 × 154 mm", "dil kanalı duvarları ↔ raf / eşik kesik kenarları")


def dil_kanallari():
    for (a, b), nm in zip(DIL_X, ("kasar", "sucuk")):
        d = _sac("dil_kanali_%s" % nm, "ic", t=1.0, R=R_GIDA, bolge="gida"); gd = d.R + d.t
        Q = d.taban([(a + gd, -38.0), (b - gd, -38.0), (b - gd, 116.0), (a + gd, 116.0)], O=(0, 1141.4, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="taban")
        h = 1152.0 - 1141.4
        Q.flans(1, h, yon=+1, ad="sag_duvar"); Q.flans(3, h, yon=+1, ad="sol_duvar")
        G.PANEL["dil_" + nm] = Q


# =====================================================================================================================================
# 3 · KURU + TEKNİK BÖLME + CEP
# =====================================================================================================================================
def kuru_teknik():
    # kuru bölme tabanı
    s = _sac("kuru_bolme_tabani", "dis"); g = s.R + s.t
    P = s.taban([(XI0 + g, -Z_SA + g), (2420.0, -Z_SA + g), (2420.0, -ZAI), (XI0 + g, -ZAI)], O=(0, Y_SO - T, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="taban")
    P.flans(0, 15.0, yon=-1, bas=20.0, ad="on_donus"); P.flans(3, 15.0, yon=-1, ad="sol_donus")
    for x, z, d in KUR_TABAN_DELIK: wdelik(P, (x, Y_SO - T, z), d, tip="rakor_deligi", parca="kablo / tahliye rakoru geçişi (v8zq)")
    G.PANEL["kuru_taban"] = P
    kanal_ve_ayak(P)
    s.punta(G.PANEL["yan_sol"]["s"], [(XI0, Y_SO - 10.0, z) for z in (-800.0, -720.0, -650.0)], not_="kuru bölme tabanı sol dönüşü ↔ sol yan")
    # teknik bölme ön perdesi
    s = _sac("teknik_on_perde", "dis"); g = s.R + s.t
    P = s.taban([(XI0, YBI + g), (2420.0, YBI + g), (2420.0, Y_SO - g), (XI0, Y_SO - g)], O=(0, 0, -476.5), ex=(1, 0, 0), ey=(0, 1, 0), ad="perde")
    P.flans(0, FL, yon=+1, ad="alt_donus"); P.flans(2, FL, yon=+1, ad="ust_donus")
    for i in range(22):
        xc = 1464.0 + 44.0 * i
        P.dikdortgen(xc, 923.5, 36.0, 40.0, r=3.0, tip="menfez", parca="teknik bölme menfez yarığı 36 × 40")
    G.PANEL["on_perde"] = P
    s.punta(G.PANEL["taban"]["s"], [(x, YBI, -466.0) for x in np.arange(1480.0, 2420.0, 150.0)], not_="ön perde alt dönüşü ↔ taban")
    s.punta(G.PANEL["alt_sac"].sac, [(x, Y_SO, -466.0) for x in np.arange(1480.0, 2420.0, 150.0)], not_="ön perde üst dönüşü ↔ soğuk oda alt sacı")
    # sağ perde
    s = _sac("teknik_sag_perde", "dis")
    P = s.taban([(YBI, -824.0), (Y_SO - T, -824.0), (Y_SO - T, -476.5), (YBI, -476.5)], O=(2418.5, 0, 0), ex=(0, 1, 0), ey=(0, 0, 1), ad="perde")
    wrect(P, 2418.0, 2420.5, 1091.5, 1112.0, -634.5, -629.0, tip="centik", dfm=False, parca="kuru bölme tabanı ön dönüşü geçişi (üstten açık çentik)")
    G.PANEL["sag_perde"] = P
    _etiket("teknik_perde_dikisleri", "TIG 141 aralıklı 25 / 150", "≈ 1,6 m", "sağ perde ↔ taban / kuru tabanı / ön perde (sızdırmaz değil, hava ayırma)")
    # ayırma perdesi (cep sol duvarı + teknik bölme ayırma) · 24 emiş yarığı
    s = _sac("ayirma_perdesi_cep_sol", "dis")
    P = s.taban([(807.5, -788.5), (YBI, -788.5), (YBI, -826.9), (Y_SO - T, -826.9), (Y_SO - T, -477.5), (807.5, -477.5)], O=(CEP[0], 0, 0), ex=(0, 1, 0), ey=(0, 0, 1), ad="perde")
    for z in np.arange(-771.0, -494.0, 12.0):
        P.dikdortgen(850.0, z, 62.0, 5.0, r=2.49, tip="havalandirma", parca="kondenser emiş ızgarası yarığı 62 × 5")
    wrect(P, CEP[0] - 0.5, CEP[0] + 2.0, 1091.5, 1112.0, -634.5, -629.0, tip="centik", dfm=False, parca="kuru bölme tabanı ön dönüşü geçişi (üstten açık çentik)")
    G.PANEL["ayirma"] = P
    # soğutma grubu cebi (tava: taban + ön + arka + sağ · sol = ayırma perdesi)
    s = _sac("sogutma_cebi", "dis"); g = s.R + s.t
    x0, x1, z0, z1 = CEP
    C = s.taban([(x0, -z1 + g), (x1 - g, -z1 + g), (x1 - g, -z0 - g), (x0, -z0 - g)], O=(0, Y_CEP, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="taban")
    h = YBI - Y_CEP
    on = C.flans(0, h, yon=+1, bas=T, ad="on"); sag = C.flans(1, h, yon=+1, ad="sag"); ark = C.flans(2, h, yon=+1, son=T, ad="arka")
    s.kose(on, sag, "acik"); s.kose(sag, ark, "acik")
    for i, (x, z) in enumerate(TAKOZ):
        pem(C, (x, Y_CEP, z), (0, -1.0, 0), "M8", "cep_takoz_pem_M8_%d" % i)
    G.PANEL["cep"] = C
    _etiket("cep_cevre_dikisi", "TIG 141 sürekli (su / yoğuşma sızdırmaz)", "≈ 2,7 m", "cep duvarları üst kenarı ↔ taban ağzı · cep ↔ ayırma perdesi · köşeler")


def kanal_ve_ayak(P):
    """v2 D4 · kondenser kanalı geçiş deliği + kapak · v2 D3 · evaporatör ayakları (kuru bölme tabanına PEM SP-M5)"""
    x0, x1, z0, z1 = KANAL_DELIK
    wrect(P, x0, x1, Y_SO - T, Y_SO, z0, z1, r=3.0, tip="kanal_gecisi", parca="kondenser kanalı (dirsekli boru) dikey iniş deliği 135 × 33")
    s = _sac("kanal_gecis_kapagi", "dis")
    a0, a1, b0, b1 = KANAL_KAPAK
    Q = s.taban([(a0, -b1), (a1, -b1), (a1, -(z1 - 0.5)), (2240.5, -(z1 - 0.5)), (2240.5, -(z0 + 0.5)), (a1, -(z0 + 0.5)), (a1, -b0), (a0, -b0)],
                O=(0, Y_SO, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="kapak")          # sağdan açık yarık: kanal borusunun dikey kolu çevresinde sola sürülür
    for x, z in KANAL_KAPAK_M5:
        b_ = S.vidali_birlesim(Q, P, (x, Y_SO + T, z), "pem_somun", dis="M5", vida_std="ISO7380", ad="kanal_kapagi_%d" % int(x), birim=BIRIM)
        for q in b_["parcalar"]: _eleman(q)
    G.PANEL["kanal_kapak"] = Q
    for i, (xa, yt) in enumerate(EVAP_AYAK):
        s = _sac("evaporator_ayagi_%d" % i, "braket", t=2.5)
        g = s.R + s.t
        A = s.taban([(xa, Y_SO + g), (xa + 30.0, Y_SO + g), (xa + 30.0, yt), (xa, yt)], O=(0, 0, ZAI), ex=(1, 0, 0), ey=(0, 1, 0), ad="dik")
        ay = A.flans(0, 30.0, yon=+1, ad="taban_ayak")
        b_ = S.vidali_birlesim(ay, P, (xa + (21.0 if i == 1 else 15.0), Y_SO + 2.5, ZAI + 17.0), "pem_somun", dis="M5", vida_std="ISO7380", ad="evaporator_ayak_%d" % i, birim=BIRIM)
        for q in b_["parcalar"]: _eleman(q)
    G.NOT.append("v2 D3 · evaporatör ayağı 4 × (2,5 mm L, eski sekme düzleminde, kaset gövdesine üreticide kaynaklı) → kuru bölme tabanına ISO 7380 M5 → PEM SP-M5 · "
                 "v2 D4 · kondenser kanalı deliği 135 × 33 + geçiş kapağı (2 × ISO 7380 M5 → tabanda PEM SP-M5)")


# =====================================================================================================================================
# 4 · KAIDE_C
# =====================================================================================================================================
KB, KH = 40.0, 100.0
KY0, KY1, KYP = 788.0, 888.0, 892.0
KB_M8 = [(1456.0, -706.0), (1456.0, -110.0), (2120.0, -110.0), (2480.0, -110.0)]
KAIDE_PEN = [(1481.0, 1614.0, -785.0, -480.0), (1628.0, 2095.0, -790.0, -477.0), (2145.0, 2410.0, -785.0, -480.0), (2419.5, 2451.0, -699.5, -558.5)]


def kaide():
    P = G.PROF; yc = (KY0 + KY1) / 2.0
    P["kaide_arka_boru"] = Profil("kaide_arka_boru", "x", X0, X1, (yc, -810.0), b1=KH, b2=KB, not_="kaide arka (100 × 40)")
    for ad, xm in (("kaide_sol_boru", X0 + 20.0), ("kaide_sag_boru", X1 - 20.0), ("kaide_enine_boru", 2120.0)):
        P[ad] = Profil(ad, "z", -790.0, -5.0, (xm, yc), b1=KB, b2=KH, not_="kaide yan / enine")
    for ad, a0, a1 in (("kaide_boyuna_boru_1", 1476.0, 1614.0), ("kaide_boyuna_boru_2", 1620.0, 2100.0), ("kaide_boyuna_boru_3", 2140.0, 2460.0)):
        P[ad] = Profil(ad, "x", a0, a1, (yc, -415.0), b1=KH, b2=KB, not_="kaide boyuna")
    K = G.KAYNAK
    for ad, yz in (("kaide_sol_boru", [(1.0, 0, 0)]), ("kaide_sag_boru", [(-1.0, 0, 0)]), ("kaide_enine_boru", [(1.0, 0, 0), (-1.0, 0, 0)])):
        xm = P[ad].c[0]
        K += uc_kaynaklari("%s_kaynak_arka" % ad, (xm, yc, -790.0), (0, 0, 1.0), yz, KB, KH - 8.0)
    for ad, xs, e in (("kaide_boyuna_boru_1", 1476.0, (1.0, 0, 0)), ("kaide_boyuna_boru_2", 2100.0, (-1.0, 0, 0)), ("kaide_boyuna_boru_3", 2140.0, (1.0, 0, 0)),
                      ("kaide_boyuna_boru_3", 2460.0, (-1.0, 0, 0))):
        K += uc_kaynaklari("%s_kaynak_%d" % (ad, int(xs)), (xs, yc, -415.0), e, [(0, 0, 1.0), (0, 0, -1.0)], KB, KH - 8.0)
    # enine lama 6 × 100 (cep ile arka emiş filtresi arasında: boru sığmaz)
    s = _sac("kaide_enine_lama_6", "braket", t=6.0)
    s.taban([(KY0, -790.0), (KY1, -790.0), (KY1, -5.0), (KY0, -5.0)], O=(1614.0, 0, 0), ex=(0, 1, 0), ey=(0, 0, 1), ad="lama")
    _etiket("kaide_enine_lama_dikisi", "TIG 141 köşe a3", "2 × 2 × 100 mm", "lama uçları ↔ arka boru / ön perde · yanlar ↔ boyuna borular")
    # ön perde menfezli: 2,0 C (gövde kapanır, kanat menfezleri hizasında lazer yarık)
    s = _sac("kaide_on_perde_menfezli", "dis", t=2.0); g = s.R + s.t
    W_ = s.taban([(X0, -(KY1 - g)), (X1, -(KY1 - g)), (X1, -(KY0 + g)), (X0, -(KY0 + g))], O=(0, 0, 35.0), ex=(1, 0, 0), ey=(0, -1, 0), ad="on")
    W_.flans(0, 40.0, yon=+1, ad="ust_kanat"); W_.flans(2, 40.0, yon=+1, ad="alt_kanat")
    for a, b in ((1490.0, 1610.0), (1634.0, 2086.0), (2154.0, 2446.0)):
        for (u, vb) in yarik_merkez(a, b, 803.0, 863.0, 5.0, 60.0, 12.0, 20.0):
            W_.dikdortgen(u, -(vb + 30.0), 5.0, 60.0, r=2.49, tip="menfez", parca="kaide ön perde menfez yarığı 5 × 60 (kanat yarıkları hizasında)")
    G.PANEL["kaide_on"] = W_
    _etiket("kaide_on_perde_dikisi", "TIG 141 köşe a2", "4 × 100 mm + kanat uçları", "yan / enine boru uçları ↔ ön perde arka kanatları")
    # üst plaka 4 mm
    pl = _sac("kaide_ust_plaka_4", "braket", t=4.0)
    Q = pl.taban([(X0, -35.0), (X1, -35.0), (X1, 830.0), (X0, 830.0)], O=(0, KY1, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="plaka")
    for a, b, c, d in KAIDE_PEN: wrect(Q, a, b, KY1, KYP, c, d, r=3.0, tip="pencere", parca="kaide plakası penceresi (menfez / cep / kanal)")
    yar = [(x, -810.0, 0.0) for x in (1520.0, 1800.0, 2200.0, 2420.0)] + [(1456.0, z, 90.0) for z in (-600.0, -250.0)] + [(2480.0, z, 90.0) for z in (-600.0, -250.0)] + \
          [(2120.0, z, 90.0) for z in (-600.0, -250.0)] + [(x, -415.0, 0.0) for x in (1545.0, 1700.0, 2000.0, 2300.0)] + [(x, 15.0, 0.0) for x in (1600.0, 1968.0, 2340.0)]
    for i, (x, z, a) in enumerate(yar):
        Q.oblong(x, -z, 25.0, 8.0, a, tip="kaynak_yarigi", parca="delik kaynağı 25 × 8 (boruya / ön perdeye) · yüz taşlanır")
        f = S.yuz_oblong(x, -z, 25.0, 8.0, a)
        sh = S._tasi(S._prizma(f, 4.0), S._M(np.column_stack([[1, 0, 0], [0, 0, -1.0], [0, 1.0, 0]]), (0, KY1, 0)))
        G.KAYNAK.append(dict(ad="kaide_ust_plaka_delik_kaynagi_%d" % i, wp=cq.Workplane("XY").add(sh), sh=sh, mal="sac", birim=BIRIM, grup="SABIT", kaynak=SURUM, tur="kaynak",
                             bom=("Delik kaynağı · TIG 141 · yüz taşlanır", 1, "25 × 8 × 4", "kaide plakası ↔ boru", "ÜRETİM"), meta=dict(tur="kaynak", tip="delik", yontem="TIG 141")))
    for i, (x, z) in enumerate(GOVDE_M6 + RAY_M6):
        ps, c, ms = S.pem_somun("SP", "M6", (x, KY1, z), (0, -1.0, 0), pl.t, ad="kaide_plaka_pem_M6_%d" % i, birim=BIRIM)
        Q.delik(x, -z, c["delik"], tip="pem_somun", parca=ps["meta"]["parca"], pem_tip="SP", kenar_min=c["kenar"], min_sac=ms)
        _eleman(ps)
        tanim = "TOPPING tabla rayı taban sacı (TOPPING_MODUL__sac[8]) + gövde tabanı" if (x, z) in RAY_M6 else "TOPPING gövde tabanı (teknik bölme önü)"
        _arayuz(S.vida("ISO4762", "M6", 20 if (x, z) in RAY_M6 else 12, (x, YBI + (31.5 if (x, z) in RAY_M6 else 1.5), z), (0, -1.0, 0),
                       ad="arayuz_kaide_M6_%d" % i, birim=BIRIM), tanim,
                "ray tabanında Ø6,6 delik (dünya x %.0f z %.0f)" % (x, z) if (x, z) in RAY_M6 else "— (gövde tabanında Ø6,6 hazır)", "TOPPING sahibi")
    for x, z in KB_M8:
        Q.delik(x, -z, 16.0, tip="servis_deligi", parca="KAIDE → B M8 lokma geçişi (gövde yerleşmeden önce sıkılır)")
    G.PANEL["kaide_plaka"] = Q
    # kaide → B (borunun alt duvarı Ø9 · üst duvar Ø16)
    for x, z in KB_M8:
        ad = "kaide_sol_boru" if x < 1500 else ("kaide_sag_boru" if x > 2400 else "kaide_enine_boru")
        pr = P[ad]
        pr.duvar_delik("-y", z, x - pr.c[0], 9.0, tip="kb_civata", not_="KAIDE → B M8 (alt duvar)")
        pr.duvar_delik("+y", z, x - pr.c[0], 16.0, tip="kb_servis", not_="KAIDE → B M8 baş geçişi (üst duvar)")
        yk = KY0 + 2.0
        pu = S._bp("arayuz_kb_%d_%d_pul" % (int(x), int(-z)), S._tasi(S._halka(7.5, 4.2, 1.6), S._cerceve((x, yk, z), (0, 1.0, 0))), "ISO 7092",
                   "Küçük seri pul M8 (Ø16 servis deliğinden geçer)", "8,4 / 15 × 1,6", "A2", birim=BIRIM, meta=dict(dis="M8", d1=8.4, d2=15.0, h=1.6))
        vd = S.vida("ISO4762", "M8", 25, (x, yk + 1.6, z), (0, -1.0, 0), ad="arayuz_kb_%d_%d" % (int(x), int(-z)), birim=BIRIM)
        _arayuz(pu, "B dış tavan + B_MODULER üst kiriş", "", "")
        _arayuz(vd, "B dış tavan + B_MODULER üst kiriş",
                "B: dış tavan sacında Ø9 + üst kiriş üst duvarında M8 kapalı uçlu perçin somun (köpüklemeden ÖNCE) dünya x %.0f z %.0f · GFRP pedde Ø9" % (x, z), "h3_b_sac_v1 sahibi")
    # cep taşıyıcı L 3 mm × 2 (lama ↔ enine boru)
    for i, zw in enumerate((-705.0, -527.0)):
        s = _sac("kaide_cep_tasiyici_%d" % i, "braket", t=3.0); gk = s.R + s.t
        L = s.taban([(1620.0, -(Y_CEP - gk)), (2100.0, -(Y_CEP - gk)), (2100.0, -(KY0 + 2.0)), (1620.0, -(KY0 + 2.0))], O=(0, 0, zw), ex=(1, 0, 0), ey=(0, -1, 0), ad="dik")
        L.flans(0, 25.0, yon=+1, ad="yatay")
    _etiket("kaide_cep_tasiyici_dikisi", "TIG 141 köşe a3", "2 × 2 × 40 mm", "taşıyıcı L uçları ↔ enine lama / enine boru · üstte cep tabanı oturur (punta yok)")
    # arka emiş filtresi (v8zq KAIDE_C[11] · paslanmaz çerçeveli filtre kaseti)
    sh = kutu(1486.0, 1614.0, 800.0, 866.0, -790.0, -776.0)
    _ozel("kaide_arka_emis_filtresi", sh, "filtre kaseti (G3, paslanmaz çerçeve)", "Kondenser emiş filtresi 128 × 66 × 14 · kaide gözünde, arka boruya klips", "128 × 66 × 14",
          malzeme="AISI 304 çerçeve + PES keçe", mal="koyu", uretim=False)


# =====================================================================================================================================
# 5 · FHP saplamalar + PU
# =====================================================================================================================================
def saplamalar():
    pan = {"yan_sol": (G.PANEL["yan_sol"]["yan"], (1.0, 0, 0)), "yan_sag": (G.PANEL["yan_sag"]["yan"], (-1.0, 0, 0)), "taban": (G.PANEL["taban"]["taban"], (0, 1.0, 0)),
           "arka": (G.PANEL["arka"]["arka"], (0, 0, 1.0)), "soguk_arka": (G.PANEL["soguk_arka"], (0, 0, -1.0)), "raf": (G.PANEL["raf"], (0, 1.0, 0)),
           "alt_sac": (G.PANEL["alt_sac"], (0, -1.0, 0)), "kuru_taban": (G.PANEL["kuru_taban"], (0, 1.0, 0))}
    n = 0
    for k, p, karsi in STUD:
        P, yon = pan[k]
        ya = P.yerel(tuple(p))
        if not guvenli(P, ya[0], ya[1], kenar=12.0, delik=9.0):
            G.STUD_ATLA.append((k, karsi, list(p))); continue
        fhp(P, p, yon, karsi + " (v8zq)", "karşı parçada Ø5,5 delik (FHP-M5 saplama · pul + fiberli somun)", ad="arayuz_mek_%s_%d" % (k, n)); n += 1
    G.NOT.append("mekanizma temas saplaması FHP-M5: %d · yer güvenli değil (atlanan) %d → %s" % (n, len(G.STUD_ATLA), G.STUD_ATLA))


PU_BOLGE = [("pu_soguk_duvar", (XI0, XI1, AST["y0"], YTI, Z_SA + T, ZFC), (AST["x0"], AST["x1"], AST["y0"] - 1.0, AST["y1"], AST["zb"], ZFC + 1.0)),
            ("pu_raf_esik", (1496.0, 2440.0, Y_SO + T, 1149.0, -570.0, 23.0), (1496.0, 2440.0, Y_SO + T, 1150.8, 20.0, 36.8))]   # raf altı ∪ eşik (tek köpük gözü)


def gomulu_katilar():
    out = [kutu(*g[1:]) for g in GOMULU_KUTU]
    for ad, ex, c, r, a0, a1 in GOMULU_SIL:
        if ex == "x":
            w = cq.Wire.makePolygon([V(a0, c[0] + a, c[1] + b) for a, b in RAF_BURC_POLY], close=True)
            out.append(cq.Solid.extrudeLinear(cq.Face.makeFromWires(w), V(a1 - a0, 0, 0)))
        else:
            w = cq.Wire.makePolygon([V(c[0] + a, c[1] + b, a0) for a, b in BURC_YUV_POLY], close=True)
            out.append(cq.Solid.extrudeLinear(cq.Face.makeFromWires(w), V(0, 0, a1 - a0)))
    for x, y in MOTOR_BURC:
        w = cq.Wire.makePolygon([V(x + a, y + b, Z_SA) for a, b in MOTOR_LOB], close=True)
        out.append(cq.Solid.extrudeLinear(cq.Face.makeFromWires(w), V(0, 0, AST["zb"] + AST["t"] - Z_SA)))
    for k, (a, b) in enumerate(DIL_X):
        out.append(kutu(a + 1.0, b - 1.0, 1142.4, 1153.0, -116.0, ZFC))       # dil kanalı içi (hava + kaset dili) · duvarlar ve büküm yayları PU içinde
    for xc in DUSME_ARTI:
        w = cq.Wire.makePolygon([V(xc + a, Y_SO, b) for a, b in ARTI_IC], close=True)
        out.append(cq.Solid.extrudeLinear(cq.Face.makeFromWires(w), V(0, 1153.0 - Y_SO, 0)))             # artı kesit iç (düşme yolu)
        out.append(kutu(xc - 31.5, xc + 31.5, 1142.0, 1153.0, -180.5, -100.0))                            # yaka kaset dili yuvası
    for a, b in DIL_X: out.append(kutu(a, b, 1143.0, 1153.0, -181.0, -116.0))                              # raf kesiği (kovan üstü)
    for x, z in DUSME_KARE: out.append(kutu(x - 19.0, x + 19.0, Y_SO + T, 1153.0, z - 19.0, z + 19.0))      # kovan içi (kovan sacı ayrıca düşülür → büküm yayları PU içinde)
    for x, z in DUSME_YUV: out.append(silindir((x, Y_SO + T, z), (0, 1, 0), 19.0, 1153.0 - Y_SO - T))
    for x, z, d in RAF_DELIK: out.append(silindir((x, 1148.0, z), (0, 1, 0), d / 2.0, 5.0))
    for x, z in RAF_MANDAL: out.append(kutu(x - 4.5, x + 4.5, 1148.0, 1153.0, z - 3.5, z + 3.5))
    for a, b, c, d in EVAP_KAN: out.append(kutu(a, b, c, d, Z_SA, AST["zb"]))
    return out


def gida_dolgulari():
    """raf ve eşik büküm dış yaylarının bıraktığı yivler (gıda yüzeyi) TIG / gıda silikonu ile doldurulur (taşlanır) — katı olarak modellenir"""
    saclar = [s.kati() for s in G.SAC if s.ad.startswith(("raf", "soguk_esik", "dil_kanali", "astar"))]
    ic = [kutu(a + 1.0, b - 1.0, 1141.0, 1160.0, -200.0, 40.0) for a, b in DIL_X] + [kutu(a, b, 1141.0, 1160.0, -200.0, 40.0) for a, b in DIL_X]
    for k, (a, b) in enumerate(DIL_X):                                         # eşik ön sacı kesiği köşeleri ↔ dil kanalı büküm yayı (çerçeve arkasında)
        for m, xa in enumerate((a, b - 4.0)):
            sh = kutu(xa, xa + 4.0, 1141.4, 1145.6, 36.8, ZFC).cut(*saclar).clean()
            for j, so in enumerate(sh.Solids()):
                if so.Volume() < 0.01: continue
                p = S._bp("dil_kesik_kose_silikonu_%d_%d_%d" % (k, m, j), so, "gıda sınıfı silikon (FDA 21 CFR 177.2600)", "Eşik kesiği köşe cebi dolgusu (köpüklemeden önce)",
                          "≈ 4 × 4 × 1,2", "VMQ silikon", birim=BIRIM, mal="conta")
                p["tur"] = "baglanti"; G.ELEMAN.append(p)
    for ad, bx in (("raf_arka_kose_dolgusu", kutu(1496.0, 2440.0, 1144.0, 1152.0, -570.0, -562.0)), ("raf_esik_yiv_dolgusu", kutu(1496.0, 2440.0, 1144.0, 1152.0, 15.0, 23.0)),
                   ("esik_on_yiv_dolgusu", kutu(1496.0, 2440.0, 1147.0, 1152.0, 33.0, 38.0))):
        sh = bx.cut(*saclar).cut(*ic).clean()
        for k, so in enumerate(sh.Solids()):
            if so.Volume() < 0.5: continue
            bb = so.BoundingBox()
            if bb.ymax < 1149.01 and ad != "esik_on_yiv_dolgusu": continue                 # PU tarafındaki boşluk (köpükle dolar)
            p = S._bp("%s_%d" % (ad, k), so, "TIG 141 dolgu + taşlama / gıda silikonu (FDA 21 CFR 177.2600)", "Büküm yayı yivi dolgusu (gıda yüzeyi düz)", "%.1f cm³" % (so.Volume() / 1e3),
                      "ER308LSi", birim=BIRIM, mal="sac", meta=dict(tur="kaynak", tip="dolgu", yontem="TIG 141"), uretim=True)
            p["tur"] = "kaynak"; G.ELEMAN.append(p)


def pu_bloklari():
    saclar = [s.kati() for s in G.SAC]
    gom = gomulu_katilar()
    out = []
    for ad, (x0, x1, y0, y1, z0, z1), cik in PU_BOLGE:
        b = kutu(x0, x1, y0, y1, z0, z1)
        if cik and ad == "pu_raf_esik": b = b.fuse(kutu(*cik)).clean()
        elif cik: b = b.cut(kutu(*cik))
        bb = b.BoundingBox()
        cut = [s for s in saclar if _ic(s.BoundingBox(), bb)] + [g for g in gom if _ic(g.BoundingBox(), bb)]
        cut += [p["sh"] for p in G.ELEMAN + G.ARAYUZ if p.get("sh") is not None and _ic(p["sh"].BoundingBox(), bb)]
        cut += [k for k in G.PU_KES if _ic(k.BoundingBox(), bb)]
        sh = b.cut(*cut).clean() if cut else b
        sols = sh.Solids() if hasattr(sh, "Solids") else [sh]
        for k, so in enumerate(sols):
            if so.Volume() < 20.0: continue
            nm = ad if len(sols) == 1 else "%s_%d" % (ad, k)
            out.append(dict(ad=nm, wp=cq.Workplane("XY").add(so), sh=so, mal="pu", birim=BIRIM, grup="SABIT", kaynak=SURUM, tur="pu",
                            bom=("Yerinde köpük PU 40 kg/m³ (λ 0,022) · %s" % ad, 1, "%.1f dm³" % (so.Volume() / 1e6), "kalıp = kasa (enjeksiyon)", "ÜRETİM"),
                            meta=dict(tur="pu", hacim_dm3=round(so.Volume() / 1e6, 3))))
    G.PU = levhalar(out)
    return G.PU


PU_KES = [("arka", [((-1e4, -1e4, -1e4), (1e4, 1e4, -571.0))]),
          ("sol", [((-1e4, -1e4, -571.0), (1495.0, 1e4, 1e4)), ((1495.0, -1e4, -571.0), (1968.0, 2140.5, 1e4))]),
          ("sag", [((2441.0, -1e4, -571.0), (1e4, 1e4, 1e4)), ((1968.0, -1e4, -571.0), (2441.0, 2140.5, 1e4))]),
          ("tavan", [((1495.0, 2140.5, -571.0), (2441.0, 1e4, 1e4))])]
YAP = {"sol": (0, XI0, XI0 + 0.5), "sag": (0, XI1 - 0.5, XI1), "tavan": (1, YTI - 0.5, YTI), "arka": (2, Z_SA + T, Z_SA + T + 0.5)}
TRAD = {"arka": "arka", "sol": "sol", "sag": "sağ", "tavan": "tavan"}


def levhalar(out):
    """v2 D2 · yerinde köpük YOK: soğuk oda duvar yalıtımı ölçüsünde kesilmiş 4 PU levha (yüzey yüzey) + dış saca 0,5 mm yapıştırıcı · flanş / perçin / pul
    yuvaları levhada açık (köpük bloğu sacların, perçinlerin ve pulların çıkarılmış hâlidir)"""
    sd = [p for p in out if p["ad"].startswith("pu_soguk_duvar")]
    kalan = [p for p in out if not p["ad"].startswith("pu_soguk_duvar")]
    blok = sd[0]["sh"]
    for p in sd[1:]: blok = blok.fuse(p["sh"])
    yeni = []
    for ad, kutular in PU_KES:
        bx = kutu(*[v for ab in zip(*kutular[0]) for v in ab])
        for lo, hi in kutular[1:]: bx = bx.fuse(kutu(*[v for ab in zip(lo, hi) for v in ab]))
        L = blok.intersect(bx).clean()
        e, a0, a1 = YAP[ad]
        lo = [-1e4] * 3; hi = [1e4] * 3; lo[e] = a0; hi[e] = a1
        sl = kutu(lo[0], hi[0], lo[1], hi[1], lo[2], hi[2])
        Y = L.intersect(sl).clean(); L = L.cut(sl).clean()
        for k, so in enumerate(L.Solids()):
            if so.Volume() < 20.0: continue
            nm = "pu_levha_%s" % ad + ("" if k == 0 else "_%d" % k)
            yeni.append(dict(ad=nm, wp=cq.Workplane("XY").add(so), sh=so, mal="pu", birim=BIRIM, grup="SABIT", kaynak=SURUM, tur="pu",
                             bom=("PU levha %s 40 kg/m³ (λ 0,022) · ölçüsünde kesilmiş, flanş / perçin yuvaları açık" % TRAD[ad], 1, "%.1f dm³" % (so.Volume() / 1e6),
                                  "CNC kesim + yuva frezesi", "ÜRETİM"), meta=dict(tur="pu", hacim_dm3=round(so.Volume() / 1e6, 3))))
        for k, so in enumerate(Y.Solids()):
            if so.Volume() < 1.0: continue
            p = S._bp("yapistirici_%s" % ad + ("" if k == 0 else "_%d" % k), so, "PU levha yapıştırıcısı (tek bileşenli PU, gıda dışı bölge)",
                      "Yapıştırıcı katmanı %s · PU levha → dış sac 0,5 mm" % TRAD[ad], "%.1f cm³" % (so.Volume() / 1e3), "PU yapıştırıcı", birim=BIRIM, mal="conta")
            p["tur"] = "silikon"; G.ELEMAN.append(p)
    return kalan + yeni


def pu_ortu():
    return []


# =====================================================================================================================================
def kur(log=print):
    if G.kuruldu: return G
    t0 = time.time()
    for a in ("SAC", "PROFIL", "ELEMAN", "KAYNAK", "ARAYUZ", "PU", "KAYNAK_ETIKET", "NOT", "PU_KES", "PU_EK", "STUD_ATLA"): setattr(G, a, [])
    G.PANEL, G.PROF = {}, {}
    _FHP.clear(); DIMPLE.clear()
    yanlar(); tavan(); taban(); arka_servis()
    on_cerceve(); alt_sac(); soguk_arka(); astar(); evap_kovanlari(); dusme_kovanlari(); raf(); ust_raf(); esik_ve_dil(); dil_kanallari()
    kuru_teknik(); kaide(); saplamalar()
    saplama_duzelt(log)                                                  # ADIM 8 (PU bloklarından önce: kaldırılan saplamaya PU yuvası açılmaz)
    G.PROFIL = list(G.PROF.values())
    gida_dolgulari()
    derz_silikonu()
    pu_bloklari()
    G.kuruldu = True
    log("%s · kuruldu: %d sac · %d profil · %d PU · %d eleman · %d kaynak · %d arayüz · %.1f sn" % (SURUM, len(G.SAC), len(G.PROFIL), len(G.PU), len(G.ELEMAN), len(G.KAYNAK),
                                                                                                len(G.ARAYUZ), time.time() - t0))
    return G


def _mal(p):
    if p.get("tur") == "pu": return "pu"
    if p.get("tur") == "sac":
        if p["ad"].startswith("on_cerceve"): return "cerceve"
        return "kabuk" if p["ad"].startswith("dis_") else "sac"
    if p.get("tur") in ("profil", "kaynak"): return "sac"
    return p.get("mal") if p.get("mal") in ("celik", "conta", "siyah", "sac", "kabuk", "koyu", "pom") else "celik"


def govde_parcalari():
    kur()
    L = []
    for s in G.SAC: L += s.parcalar()
    L += [p.parca() for p in G.PROFIL] + G.ELEMAN + G.KAYNAK + G.PU
    out = []
    DM = {}
    for sad, isl, k in DIMPLE: DM.setdefault(sad, []).append((isl, k))
    for p in L:
        sh = p.get("sh") if p.get("sh") is not None else p["wp"].val()
        if p.get("tur") == "sac" and p["ad"] in DM:                       # v2: çökertme (dimple) / havşa — lazer + delik + büküm SONRASI pres
            kes = [k for i_, k in DM[p["ad"]] if i_ == "kes"]; ek = [k for i_, k in DM[p["ad"]] if i_ == "ekle"]
            if kes: sh = sh.cut(*kes)
            if ek: sh = sh.fuse(*ek)
            sh = sh.clean()
            if sh.ShapeType() != "Solid" and len(sh.Solids()) == 1: sh = sh.Solids()[0]
        q = dict(ad=p["ad"], wp=cq.Workplane("XY").add(sh), sh=sh, mal=_mal(p), grup="SABIT", bom=tuple(p["bom"]) if p.get("bom") else None, kaynak=SURUM,
                 birim=BIRIM, tur=p.get("tur", "sac"))
        if p.get("sac"): q["sac"] = p["sac"]
        if p.get("meta"): q["meta"] = p["meta"]
        out.append(q)
    adlar = [q["ad"] for q in out]
    assert len(adlar) == len(set(adlar)), "çift ad: %s" % sorted(a for a in set(adlar) if adlar.count(a) > 1)
    return out


ZARF = (X0, X1, 788.0, YT, ZA, ZF)


def dunya_listesi(L):
    out = []
    for p in L:
        q = dict(p); s = p.get("sh") if p.get("sh") is not None else p["wp"].val()
        q["sh"] = s; q["wp"] = cq.Workplane("XY").add(s); out.append(q)
    return out


if __name__ == "__main__":
    kur()
    print(len(govde_parcalari()), "parça")
    sys.stdout.flush(); os._exit(0)
