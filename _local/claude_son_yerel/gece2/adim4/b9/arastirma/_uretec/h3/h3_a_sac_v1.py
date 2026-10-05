# -*- coding: utf-8 -*-
"""h3_a_sac_v1 — A (AÇICI KABİNİ) + KAİDELER (KAIDE_A · KAIDE_C) · ÜRETİM SACI GÖVDESİ v1 (2 Eki 2026 · Claude · YEREL · montaja bağlı DEĞİL)

Kemal: "gövdede tam çalışma; büküm gerçek; sanayi mutfaklarında nasıl kuruluyorsa öyle; nereden bükülür, vida nereye atılır, boşluk nerede açılır;
vidasına kadar ama mantıklı; sanayi tipi mutfakçı 3B'den direkt üretsin" · Pafta YOK, önce 3B (açınım JSON'ları ayrıca).
KAYNAKLAR: h3_sac_v1 (S) · h3_govde_ortak_v1 (GO, İSTASYON GÖVDE REÇETESİ) · sac_kararlar_v1.json > sac_standart_v1.json · K pilotu (h3_k_sac_v1) ·
           A'nın mevcut gövdesi (h3_acici_v1 → acici_kabin_cad_v1 + h3_moduler_v1._A sağ duvar/çerçeve) · kaideler (h3_kaide_v1 → kaide_cad_v4) ·
           v3.7 tek kapak h3_kapak_v1.A_X × (788, 2197) + robot ağzı penceresi A_PEN · elektrik h3/_elk (KD kaide_C_ust_plaka_4 · TC dis_yan_sol G9/G10).
KOORDİNAT: A modülü DÜNYADA (h3_acici_v1 / h3_kaide_v1 ile aynı · Cerceve('A') ötelemesiz): x hat boyunca · y yerden · z ön +79 / arka −830.

KURGU (atölye mantığı)
  1 · A BİRİMİ = TEK KAYNAKLI ALT MONTAJ: KAIDE_A çerçevesi (304 dikdörtgen boru 100 × 40 × 2, dik) + 4 mm üst plaka (delik kaynağı) + 1,5 taban sacı
      (delik kaynağı) + A iskeleti (304 kare boru 30 × 30 × 2 · ön alt bant 30 × 20 × 2) — dikmeler taban sacına çevre kaynağıyla oturur.
      İskelet 30 × 30 (kararlarda 40 × 40) = SAPMA: emniyet sensörü (sağ ön dikme iç yüzü x 1404), ışık perdesi tutucuları ve cihaz yerleri DEĞİŞMEZ.
      Ön çerçeve +9…+59 → +27…+57 (2 mm geri): kapak çift cidarlı (iç tava arkası +59) ve gizli menteşe plakası (1,5) dikme önüne sığsın (K pilotu gibi).
      Arka dikmeler z −815…−785 (13,5 mm içeri, K gibi): yan sac arka dönüşü + kulak + arka sac bağlantısı arkada yer bulur · KAIDE_A arka profili 1,5 içeri.
      A sağ duvarı ve boğaz çerçevesi (lento + boğaz dikmesi + alt kayıt) h3_moduler_v1._A'dan BU DOSYAYA alındı (montajda _A kapatılır).
  2 · SÖKÜLEBİLİR PANELLER (1,5 · R 2,25 · K 0,45): sol yan (ön 12 + arka 22 iç dönüş, 788'den — kaide bandını örter) · sağ duvar (ray/tabla boğazı
      çentikli, ön 12 + arka 22) · arka sac (düz, 788–1862 · arka z −830'da BAŞ YOK: PEM FHP-M5 gömme saplama → yan / sağ / üst dönüşler + taban sacına
      kaynaklı 4 L kulak · somunlar içeriden · kaide bandı 788–893,5 serbest etek) · üst şerit (v3.4 632 × 803 açıklıklı çerçeve, ön + arka aşağı dönüş, A ↔ U_A M8 sandviçi) · yan ve arka sacta 1,0 omega.
      Panel → iskelet: 3 mm L kulak (iskelete kaynaklı) + PEM FHP-M5 gömme saplama + DIN 9021 + DIN 1587 KÖR somun içeriden (dışta iz yok · kabin içi un/hamur sıçrama bölgesi → açık diş yok).
  3 · TEK ÖN KAPAK (v3.7 · 736–1434,5 × 788–2197): çift cidar (dış tava 1,5 köşeler bindirme + TIG · iç tava 1,0 punta) · robot ağzı PENCERESİ
      986–1186 × 960–1160 (iki cidarda hizalı kesik + 4 L kasa çıtası) · 3 gizli 180° kaldır-çıkar menteşe (sol ön dikme içinde · sanal pivot x 736 · z 79) ·
      3 bas-aç (sağ ön dikme içinde) · emniyet hedefi (RST 36-1) iç tavanın arkasından sökülür tutucuyla · KULP YOK.
  4 · KAİDELER: KAIDE_A (yukarıda) · KAIDE_C (TOPPING altı) yeniden kuruldu: 6 mm'lik dilim artığı enine profil KALKTI (üretilemez), göz 1 + 3 birleşti,
      boyuna profil tek parça · hava pencereleri (ön / boyuna / arka) ve plaka açıklıkları AYNI · ana besleme geçişi (elk) plakada hazır (atış açıklığıyla birleşik).
  5 · BAĞLANTI NOKTALARI (A tarafı hazır, karşı taraf ARAYÜZ + karşı delik listesi): A ↔ U_A 6 × M8 (yan üst kuşaklardan, kovanlı) · A ↔ TOPPING 2 × M8
      (sağ arka dikmede gömme perçin somun + 0,5 ara pul) · KAIDE_A → B 4 × M8 · KAIDE_C → B 2 × M8 (kovanlı, servis deliği + silikon tapa · B_AC arka hattı z −706 · KAIDE_C sağ ucu ELK ana besleme
      kanalının üstünde → cıvatasız) ·
      KAIDE_C ↔ TOPPING dis_taban 7 × M6 (plaka + profil üst duvarı birlikte kılavuz) · açıcı kolonu ankrajı 4 × M8 kaynak somunu (plaka altı).
ARAYÜZLER DEĞİŞMEZ: A x 736–1436 · y 788 / 892 / 893,5 / 1862 · kapak 788–2197 (+59…+79) · arka −830 · robot ağzı · ray/tabla boğazı (y 892,5–1042,5 ·
  z −510,5…+9) · v3.4 üst açıklık (770–1402 × −796…+7) · kaide pencereleri/açıklıkları · cihaz ve mekanizma yerleri (açıcı satın alınır, DOKUNULMAZ).
Çalıştır (öz denetim + çıktılar <scratchpad>/sac_a): python -u h3_a_sac_v1.py"""
import math, os, sys, json, time, re, collections
H3 = os.path.dirname(os.path.abspath(__file__)); _U = os.path.dirname(H3)
for _p in (_U, H3):
    if _p not in sys.path: sys.path.insert(0, _p)
import numpy as np
import cadquery as cq
import h3_sac_v1 as S
import h3_govde_ortak_v1 as GO

SURUM = "h3_a_sac_v1"
V = cq.Vector
CER = GO.Cerceve("A")                                                    # A modülü DÜNYADA (h3_acici_v1 / h3_kaide_v1) → öteleme yok
EKSEN = GO.EKSEN
# ---------------------------------------------------------------- ARAYÜZ (DÜNYA · değişmez) ----------------------------------------------------------------
X_A0, X_A1 = 736.0, 1436.0                                               # A modülü (h3_hesap_v1.A_X)
X_SOL_IC, X_SAG_IC, X_SAG_DIS = 737.5, 1434.0, 1435.5                    # sol yan sac iç yüzü · sağ duvar iç / dış yüzü (TOPPING dis_yan_sol 1436 → 0,5 derz)
Y_DUZ, Y_PL, Y_MEK, Y_TABAN, Y_UST_ALT, Y_UST = 788.0, 888.0, 892.0, 893.5, 1860.5, 1862.0
Z_ARKA, Z_ARKA_IC, Z_ON, Z_KAPAK = -830.0, -828.5, 59.0, 79.0            # arka dış · arka sac iç yüzü · gövde ön düzlemi (kapak iç tavası arkası) · kapak dış yüzü
KAPAK_X, KAPAK_Y = (736.0, 1434.5), (788.0, 2197.0)                      # v3.7 h3_kapak_v1.A_X × (Y_DUZ, Y_TAVAN_KAPAK)
PENCERE = (986.0, 1186.0, 960.0, 1160.0)                                 # v3.7 h3_kapak_v1.A_PEN (robot ağzı · acici_kabin_cad_v1 AGIZ + 736)
BOGAZ = dict(y=(892.5, 1042.5), z=(-510.5, 9.0))                         # ray / tabla geçiş ağzı (h3_moduler_v1 BOGAZ) · sağ duvarda çentik
UST_ACIKLIK = (770.0, 1402.0, -796.0, 7.0)                               # v3.4 A + U_A tek hacim (montaj _v34_ac) — üst şeritte hazır
RAKOR_G = [("G10_A_TOPPING_sensor_0", 1612.0, -720.0), ("G9_A_TOPPING_motor", 1640.0, -720.0)]   # h3_elk_ist_v1 gecis() · TC dis_yan_sol Ø16,5 ile hizalı
RAKOR_CAP = 16.5
# cihazlar (yerleri DEĞİŞMEZ · acici_kabin_cad_v1 + 736) — gövde bunlara göre
SENSOR = (1369.0, 1404.0, 1540.0, 1648.2, 28.5, 55.5)                   # RSS 36 (sağ ön dikmenin iç yüzü x 1404)
HEDEF = (1376.0, 1401.0, 1548.6, 1639.6, 55.5, 77.5)                    # RST 36-1 (kapakla döner)
PERDE_TUTUCU = [(986.0, 1016.0), (1156.0, 1186.0)]                        # ışık perdesi tutucuları x (alt 821–834 · üst 1187–1200)
# ---------------------------------------------------------------- A İSKELETİ (30 × 30 × 2 · R 4) ----------------------------------------------------------------
PB, PT, PRO = 30.0, 2.0, 4.0
X_SOL, X_SAG = 752.5, 1419.0                                             # dikme eksenleri x (737,5–767,5 · 1404–1434)
Z_ON_D, Z_ARKA_D = 42.0, -800.0                                          # ön dikme z 27–57 · arka dikme z −815…−785
Y_DIKME = (Y_TABAN, 1856.5)                                              # + 2 mm tapa → 1858,5 (üst şerit kuşaklara oturur)
Y_KUSAK = (1830.5, 1860.5)
Y_PERDE_KAYIT = (1200.0, 1230.0)
Y_LENTO = (1042.5, 1072.5)                                               # boğaz lentosu (h3_moduler_v1)
Z_BOGAZ_D = (-540.5, -510.5)                                             # boğaz dikmesi
Y_ALT_KAYIT_SAG = (Y_TABAN, 923.5)
# ön alt bant (kaide önü, 30 × 20 × 2, z 37–57) + 2 mm ara lama (kaide ön profili +35)
Z_ALT_BANT = (37.0, 57.0)
Y_ALT_DIKME = (791.0, Y_TABAN)
Y_ALT_KAYIT = (791.0, 821.0)
ARA_LAMA = [("sol", (746.0, 766.0), (800.0, 880.0)), ("sag", (1406.0, 1424.0), (800.0, 880.0)), ("orta", (1071.0, 1101.0), (793.0, 819.0))]
# kapak donanımı
MENTESE_Y = (950.0, 1370.0, 1790.0)
BASAC_Y = (1000.0, 1430.0, 1800.0)
BASAC_A = 20.0                                                           # kapağın sağ kenarından 20 (x 1414,5): baş Ø14 sağ duvarın ön dönüşüne (x ≥ 1423,5) değmez ·
                                                                         #   Ø12,2 delik dikme ön yüzünün düz bölgesinde (kayma 4,5 + 6,1 ≤ 11) · karşılık iç tava büküm bölgesinden uzak
PIVOT = (KAPAK_X[0], 0.0, Z_KAPAK)                                       # sanal pivot (sol dış köşe) · eksen +y · dışa açılış −açı
# kulaklar (y konumları) — omega (1325–1365) · ELK kelepçe 3/4 (1097–1110 · 1455–1467, sağ arka) · lento kaynağı (sağ ön, 1042,5–1072,5) dışında
KUL_SOL_ON = (915.0, 1105.0, 1295.0, 1405.0, 1595.0, 1785.0)
KUL_SOL_ARKA = (915.0, 1105.0, 1295.0, 1405.0, 1595.0, 1785.0)
KUL_SAG_ON = (1100.0, 1290.0, 1405.0, 1595.0, 1785.0)
KUL_SAG_ARKA = (960.0, 1140.0, 1295.0, 1405.0, 1520.0, 1710.0, 1800.0)
KUL_BOGAZ_Y = (985.0, 1045.0)                                            # boğaz dikmesi arka yüzü
KUL_LENTO_Z = (-420.0, -250.0, -80.0)                                    # lento üst yüzü
KUL_ALT_KAYIT_Z = (-650.0, -580.0)                                       # sağ alt kayıt üst yüzü (KAIDE → B M8 lokma geçişi z −706 ± 8 dışında)
OMEGA_Y = 1350.0                                                         # yan omegalar (tepe 40 → 1310–1390: kulaklar 1295 / 1405 arası)
OMEGA_TEPE = 40.0                                                        # 1,0 omega tepe genişliği (20'de düz bıçak abkantta çarpar · 40'ta [3, 1, 4, 2] sırasıyla temiz)
# arka sac bağlantıları
ARKA_SOL_Y = (925.0, 1110.0, 1295.0, 1480.0, 1665.0, 1840.0)            # kaide bandının (788–893,5) üstünde: bantta dönüşün arkası kaide profili (somun yeri yok)
ARKA_SAG_Y = (935.0, 1115.0, 1300.0, 1485.0, 1670.0, 1840.0)
ARKA_UST_X = (790.0, 980.0, 1170.0, 1360.0)
ARKA_KAIDE_X = (790.0, 980.0, 1170.0, 1360.0)                            # arka sacın alt bağlantısı: taban sacına kaynaklı 3 mm L kulak (FHP saplama, somun içeriden)
# bağlantı noktaları
M8_U = [(X_SOL, -40.0), (X_SOL, -400.0), (X_SOL, -760.0), (X_SAG, -40.0), (X_SAG, -400.0), (X_SAG, -760.0)]   # A ↔ U_A (yan üst kuşaklar)
M8_T_Y = (1270.0, 1660.0)                                                # A ↔ TOPPING (sağ arka dikme +x duvarı)
# ---------------------------------------------------------------- KAİDELER (100 × 40 × 2 dik · R 4) ----------------------------------------------------------------
KB, KH, KT = 40.0, 100.0, 2.0
YK = (Y_DUZ + Y_PL) / 2.0                                                # 838 · kaide profil ekseni y
KA_X = (737.5, 1436.0)
KA_X_ARKA0 = 740.5                                                       # arka profilin sol ucu: sol yan sacın arka büküm bölgesi (737,5–739,75 · z −827…−824,75) dışında
KA_KOSE_PAH = 3.0                                                        # plaka + taban sacının arka-sol köşesi 3 × 3 pah (aynı büküm bölgesi)
KA_Z = (-827.0, 35.0)                                                    # arka 1,5 içeri (yan sac arka dönüşü kaide bandında da sürer)
KA_ENINE_X = 1086.0                                                      # açıcı kolonu altında
KA_BOYUNA_Z = -635.0                                                     # kolon dikmesi altında (−655…−615)
KOLON_DELIK = (1025.0, 1147.0, -661.0, -609.0)                           # taban sacında kolon dikmesi deliği (kaide_cad_v4 · 122 × 52)
KOLON_ANKRAJ = [(1016.0, -670.0), (1156.0, -670.0), (1016.0, -600.0), (1156.0, -600.0)]
KC_X = (1436.0, 2500.0)
KC_Z = (-830.0, 35.0)
KC_ENINE_X = 2120.0                                                      # tek enine (göz 3 | göz 4) · 6 mm dilim artığı (1614–1620) KALKTI
KC_BOYUNA_Z = -415.0                                                     # −435…−395
KC_PENCERE_Y = (800.0, 866.0)
KC_PENCERE_ON = [(1486.0, 1614.0), (1630.0, 2090.0), (2150.0, 2450.0)]   # ön profil + boyuna (göz başına) — h3_kaide_v1 C_PENCERE_X
KC_PENCERE_ARKA = [(1486.0, 1614.0)]                                     # arka emiş (h3_kaide_v1 C_ARKA_PENCERE_X)
KC_PLAKA_KESIK = [(1481.0, 1614.0, -785.0, -480.0), (1628.0, 2095.0, -790.0, -477.0)]
KC_ATIS_ELK = ((2145.0, 2415.0, -785.0, -480.0), (2419.5, 2454.0, -699.5, -558.5))   # elk delik kutusu 2419,5–2451 ama kanal dışı 2452,5'e kadar → +3   # atış açıklığı + ana besleme geçişi (elk KD) → TEK kesik
KC_TEPSI = (1640.0, 2006.0)                                              # soğutma grubu tepsisi ön köşebendi
B_AC_Z = (-110.0, -706.0)                                                # B_AC üst kirişleri: ön −110 · arka −747 → −706 (h3_moduler_v1 gider ana hattı kılıfı yüzünden 41 öne,
                                                                         #   montaj v7 log 2 Eki: "B/AC hattı z -747 → -706" · B_AC_Z_UYGULANAN) — kiriş z ±15
M8_B_A = [(757.5, B_AC_Z[0]), (757.5, B_AC_Z[1]), (KA_ENINE_X, B_AC_Z[1]), (1416.0, B_AC_Z[1])]   # KAIDE_A → B_AC kirişleri
M8_B_C = [(1456.0, B_AC_Z[1]), (KC_ENINE_X, B_AC_Z[1])]                  # KAIDE_C → B · ön hat TOPPING teknesinin altında (lokma erişimi yok) · sağ uç (x 2480)
                                                                         #   YOK: ELK ana besleme kanalı dolap tavanında x 2421–2750 · z −761,5…−558,5 (cıvata kanala girer)
M6_TC = [(1500.0, 15.0), (1800.0, 15.0), (2180.0, 15.0), (2440.0, 15.0), (1500.0, -810.0), (2250.0, -810.0), (2440.0, -810.0)]   # TOPPING dis_taban → KAIDE_C
KOVAN_UST = 878.0                                                        # kaide → B kovanı üst ucu (cıvata başı profil içinde, Ø16 servis deliğinden lokma)
BIRIM = "A_GOVDE"
MALZEME = {"kabuk": dict(renk=(0.74, 0.77, 0.80, 1.0), met=0.85, ruf=0.32, saydam=False), "celik": dict(renk=(0.78, 0.80, 0.83, 1.0), met=0.95, ruf=0.28, saydam=False),
           "siyah": dict(renk=(0.12, 0.12, 0.13, 1.0), met=0.2, ruf=0.6, saydam=False), "conta": dict(renk=(0.10, 0.10, 0.11, 1.0), met=0.0, ruf=0.8, saydam=False)}
S._RENK.update({"profil": ((0.70, 0.73, 0.77, 1.0), 0.85, 0.30), "mekanizma": ((0.42, 0.46, 0.52, 1.0), 0.4, 0.5), "arayuz": ((0.90, 0.22, 0.15, 1.0), 0.3, 0.5),
                "kapak": ((0.70, 0.82, 0.95, 1.0), 0.2, 0.25), "cihaz": ((0.15, 0.15, 0.17, 1.0), 0.2, 0.6)})
# ---------------------------------------------------------------- ESKİ GÖVDE (montajdaki adlar) ----------------------------------------------------------------
ESKI_A = ("a_govde_sol_yan", "a_govde_sol_yan_omega", "a_govde_ust", "a_govde_arka", "a_govde_arka_omega", "a_kose_dikmesi_arka_sol", "a_kose_dikmesi_arka_sag",
          "onyuz_cerceve_sol_dikme", "onyuz_cerceve_sag_dikme", "onyuz_cerceve_ust_kayit", "a_ust_kusak_arka", "a_ust_kusak_sol", "a_ust_kusak_sag",
          "onyuz_cerceve_sol_alt_dikme", "onyuz_cerceve_sag_alt_dikme", "onyuz_cerceve_alt_kayit", "onyuz_cerceve_orta_kayit_sol", "onyuz_cerceve_orta_kayit_sag",
          "onyuz_cerceve_perde_kayit", "onyuz_cerceve_ara_lama_sol", "onyuz_cerceve_ara_lama_sag", "onyuz_cerceve_ara_lama_orta",
          "onyuz_alt_panel", "onyuz_alt_panel_omega", "onyuz_alt_panel_tutucu_0", "onyuz_alt_panel_tutucu_1", "onyuz_alt_panel_tutucu_2", "onyuz_alt_panel_tutucu_3",
          "onyuz_servis_kapagi", "onyuz_servis_kapagi_omega_0", "onyuz_servis_kapagi_omega_1",
          "onyuz_servis_kapagi_mentese_0_sabit", "onyuz_servis_kapagi_mentese_0_kanat", "onyuz_servis_kapagi_mentese_0_pim",
          "onyuz_servis_kapagi_mentese_1_sabit", "onyuz_servis_kapagi_mentese_1_kanat", "onyuz_servis_kapagi_mentese_1_pim",
          "onyuz_servis_kapagi_basac_mandal", "onyuz_emniyet_hedefi", "onyuz_emniyet_hedefi_alt", "onyuz_emniyet_sensoru_alt")
#   a_govde_ust_omega montajda (v3.4) zaten düşer · KALAN cihazlar: onyuz_emniyet_sensoru · onyuz_isik_perdesi_alt/ust · onyuz_isik_perdesi_tutucu_{alt,ust}_{0,1}
ESKI_KD = ("kaide_A_on_profil", "kaide_A_arka_profil", "kaide_A_yan_profil_sol", "kaide_A_yan_profil_sag", "kaide_A_enine_profil_0", "kaide_A_boyuna_profil_0",
           "kaide_A_boyuna_profil_1", "kaide_A_ust_plaka_4", "kaide_A_mekanizma_taban_saci",
           "kaide_C_on_profil", "kaide_C_arka_profil", "kaide_C_yan_profil_sol", "kaide_C_yan_profil_sag", "kaide_C_enine_profil_1", "kaide_C_enine_profil_2",
           "kaide_C_boyuna_profil_0", "kaide_C_boyuna_profil_2", "kaide_C_boyuna_profil_3", "kaide_C_ust_plaka_4", "kaide_C_tepsi_kosebendi")
#   KALAN: kaide_C_arka_emis_filtresi (satın alma filtre, yeri aynı)
ESLEME = {
    "onyuz_alt_panel": "onyuz_kapak_A (v3.7 tek kapak · alt panel + servis kapağı + U_A kapağı)", "onyuz_servis_kapagi": "onyuz_kapak_A",
    "onyuz_alt_panel_omega": "onyuz_kapak_A_ic_tava (çift cidar omeganın yerini aldı)", "onyuz_servis_kapagi_omega_0": "onyuz_kapak_A_ic_tava",
    "onyuz_servis_kapagi_omega_1": "onyuz_kapak_A_ic_tava",
    "onyuz_alt_panel_tutucu_0": "onyuz_kapak_A_basac_0 (tek kapak: yaylı tutucu yok · sol 3 gizli menteşe + sağ 3 bas-aç)", "onyuz_alt_panel_tutucu_1": "onyuz_kapak_A_basac_0",
    "onyuz_alt_panel_tutucu_2": "onyuz_kapak_A_basac_0", "onyuz_alt_panel_tutucu_3": "onyuz_kapak_A_basac_0",
    "onyuz_servis_kapagi_mentese_0_sabit": "onyuz_kapak_A_mentese_0_sabit", "onyuz_servis_kapagi_mentese_0_kanat": "onyuz_kapak_A_mentese_0_kanat",
    "onyuz_servis_kapagi_mentese_0_pim": "onyuz_kapak_A_mentese_0_kanat (gizli 180° kaldır-çıkar: ayrı pim yok)",
    "onyuz_servis_kapagi_mentese_1_sabit": "onyuz_kapak_A_mentese_1_sabit", "onyuz_servis_kapagi_mentese_1_kanat": "onyuz_kapak_A_mentese_1_kanat",
    "onyuz_servis_kapagi_mentese_1_pim": "onyuz_kapak_A_mentese_1_kanat",
    "onyuz_servis_kapagi_basac_mandal": "onyuz_kapak_A_basac_1 (+ _basac_0 · _basac_2 · _karsilik_*)",
    "onyuz_emniyet_hedefi": "onyuz_emniyet_hedefi (aynı cihaz · aynı yer · + onyuz_kapak_A_hedef_tutucu)",
    "onyuz_emniyet_hedefi_alt": "kalktı (v3.7: tek kapak → tek kilit sensörü)", "onyuz_emniyet_sensoru_alt": "kalktı (v3.7 h3_kapak_v1.bolge_A ile aynı)",
    "onyuz_cerceve_orta_kayit_sol": "kalktı (v3.7: 1107,5/1110,5 derzi yok)", "onyuz_cerceve_orta_kayit_sag": "kalktı (v3.7)",
    "a_govde_ust_omega": "kalktı (v3.4 montaj: üst açıklık) — bu dosyada da yok",
    "A_bagimsiz_sag_duvar_1p5": "a_govde_sag_yan (h3_moduler_v1._A kapatılır)", "A_sag_bogaz_lentosu": "a_sag_bogaz_lentosu",
    "A_sag_bogaz_dikmesi": "a_sag_bogaz_dikmesi", "A_sag_alt_kayit": "a_sag_alt_kayit",
    "kaide_C_enine_profil_1": "kalktı (6 mm dilim artığı · üretilemez · göz 1 + göz 3 birleşti)",
    "kaide_C_boyuna_profil_2": "kaide_C_boyuna_profil_0 (1476–2100 tek parça)",
    "onyuz_kapak_A": "onyuz_kapak_A (v3.7 h3_kapak_v1.bolge_A tek kat tavası → çift cidar)",
    "onyuz_kapak_A_omega_0": "onyuz_kapak_A_ic_tava", "onyuz_kapak_A_omega_1": "onyuz_kapak_A_ic_tava", "onyuz_kapak_A_omega_2": "onyuz_kapak_A_ic_tava",
    "onyuz_kapak_A_omega_3": "onyuz_kapak_A_ic_tava",
    "onyuz_servis_kapagi_mentese_2_sabit": "onyuz_kapak_A_mentese_2_sabit", "onyuz_servis_kapagi_mentese_2_kanat": "onyuz_kapak_A_mentese_2_kanat",
    "onyuz_servis_kapagi_mentese_2_pim": "onyuz_kapak_A_mentese_2_kanat",
    "onyuz_servis_kapagi_basac_mandal_alt": "onyuz_kapak_A_basac_0", "onyuz_servis_kapagi_basac_mandal_ust": "onyuz_kapak_A_basac_2",
}


# =====================================================================================================================================
# 0 · DİKDÖRTGEN PROFİL (GO.Profil'in bu × bv genellemesi · dış R = 2t)
# =====================================================================================================================================
class ProfilD(GO.Profil):
    """304 dikdörtgen boru bu × bv × t · bu: profil eksenine dik İLK eksen boyunca (y profil → x · x profil → y · z profil → x), bv: ikinci"""
    def __init__(self, ad, eksen, a0, a1, c, bu, bv, t=2.0, Ro=None, birim=BIRIM, kaynak=SURUM, not_=""):
        GO.Profil.__init__(self, ad, eksen, a0, a1, c, b=max(bu, bv), t=t, Ro=Ro, birim=birim, kaynak=kaynak, not_=not_)
        self.bu, self.bv = float(bu), float(bv)
        self.dik = [k for k in "xyz" if k != eksen]

    def yarim(self, eks):
        return (self.bu if eks == self.dik[0] else self.bv) / 2.0

    def _govde(self):
        dis = S.yuz_dikd_r(0.0, 0.0, self.bu, self.bv, 0.0, self.Ro)
        ic = S.yuz_dikd_r(0.0, 0.0, self.bu - 2 * self.t, self.bv - 2 * self.t, 0.0, self.Ro - self.t)
        sh = S._prizma(dis.cut(ic), self.a1 - self.a0)
        ex, ey, ez = EKSEN[self.dik[0]], EKSEN[self.dik[1]], EKSEN[self.eksen]
        if np.linalg.det(np.column_stack([ex, ey, ez])) < 0: ey = -ey
        return S._tasi(sh, S._M(np.column_stack([ex, ey, ez]), self.merkez(self.a0)))

    def duvar_delik(self, yuz, a, kayma, cap, tip="delik", not_=""):
        n = GO._yuz_vektor(yuz)
        dk = [k for k in "xyz" if k not in (self.eksen, yuz[1])][0]
        p = self.merkez(a) + n * (self.yarim(yuz[1]) + 1.0) + EKSEN[dk] * kayma
        cut = GO.silindir(p, -n, cap / 2.0, self.t + 1.6)
        self.kesikler.append(dict(sh=cut, tip=tip, yuz=yuz, a=round(a - self.a0, 2), kayma=kayma, cap=cap, not_=not_)); self._sh = None
        return cut

    def duvar_pencere(self, yuz, a, kayma, la, lk, r=1.0, tip="pencere", not_=""):
        sg = 1.0 if yuz[0] == "+" else -1.0
        dk = [k for k in "xyz" if k not in (self.eksen, yuz[1])][0]
        c = self.merkez(a); h = self.yarim(yuz[1])
        lo, hi = np.zeros(3), np.zeros(3)
        for i, k in enumerate("xyz"):
            if k == self.eksen: lo[i], hi[i] = a - la / 2.0, a + la / 2.0
            elif k == dk: lo[i], hi[i] = c[i] + kayma - lk / 2.0, c[i] + kayma + lk / 2.0
            else:
                d0, d1 = c[i] + sg * (h - self.t - 0.6), c[i] + sg * (h + 1.0)
                lo[i], hi[i] = min(d0, d1), max(d0, d1)
        cut = GO.kutu(lo[0], hi[0], lo[1], hi[1], lo[2], hi[2])
        self.kesikler.append(dict(sh=cut, tip=tip, yuz=yuz, a=round(a - self.a0, 2), kayma=kayma, olcu=[la, lk], not_=not_)); self._sh = None
        return cut

    def dfm(self):
        out = []; L = self.a1 - self.a0
        for k in self.kesikler:
            dk = [q for q in "xyz" if q not in (self.eksen, k["yuz"][1])][0]
            duz = self.yarim(dk) - self.Ro
            yar = (k.get("cap") or k["olcu"][1]) / 2.0
            ok = abs(k["kayma"]) + yar <= duz + 1e-6
            out.append(dict(kural="profil_duz_yuz", durum="GEÇTİ" if ok else "HATA", detay="%s %s %s Ø/en %.1f kayma %.1f · düz yüz ±%.1f" % (self.ad, k["tip"], k["yuz"], 2 * yar, k["kayma"], duz)))
            la = (k.get("cap") or k["olcu"][0]) / 2.0
            uc = min(k["a"] - la, L - k["a"] - la)
            out.append(dict(kural="profil_uc", durum="GEÇTİ" if uc >= 3.0 else "HATA", detay="%s %s → boru ucu %.1f (≥ 3)" % (self.ad, k["tip"], uc)))
            for (yz, b0, b1) in self.uc_kaynak:
                if yz == k["yuz"] and b0 - la - 3.0 < k["a"] < b1 + la + 3.0:
                    out.append(dict(kural="profil_kaynak_bolgesi", durum="HATA", detay="%s %s kaynaklı birleşim bölgesinde (%s %.0f–%.0f)" % (self.ad, k["tip"], yz, b0, b1)))
        out.append(dict(kural="profil_boy", durum="GEÇTİ" if L <= 6000 else "HATA", detay="%s L %.1f ≤ 6000 (boy stoğu)" % (self.ad, L)))
        return out

    def parca(self):
        p = GO.Profil.parca(self)
        L = self.a1 - self.a0; kg = p["meta"]["kg"]
        p["bom"] = ("%s boru AISI 304 %g × %g × %g (EN 10217-7 / ASTM A554 · dış R %g) · %s" % ("Kare" if self.bu == self.bv else "Dikdörtgen", self.bu, self.bv, self.t, self.Ro, self.not_),
                    1, "L %.1f" % L, "boru lazer / şerit testere 90° · %d kesik · %.2f kg" % (len(self.kesikler), kg), "ÜRETİM")
        p["meta"]["kesit"] = [self.bu, self.bv, self.t, self.Ro]
        return p


# =====================================================================================================================================
# 1 · KAYIT DEFTERİ + yardımcılar
# =====================================================================================================================================
G = None                                                                 # kur() sonrası GO.Govde


def _pd(ad, eksen, a0, a1, c, bu, bv, t=PT, not_=""):
    if ad in G.PROF: raise ValueError("profil adı çift: %s" % ad)
    p = ProfilD(ad, eksen, a0, a1, c, bu, bv, t=t, birim=G.birim, not_=not_)
    G.PROF[ad] = p
    return p


def _ps(ad, eksen, a0, a1, c, not_=""):
    return _pd(ad, eksen, a0, a1, c, PB, PB, not_=not_)


def _kaynak(p0, p1, u1, u2, a, ad, not_=""):
    G.kaynak(S.kaynak_dikisi(p0, p1, u1, u2, a, ad=ad, birim=G.birim, taraf="dis (köşe)", not_=not_))


def _uc(ad, pr, uc, yuzler, flat=None, a=2.0):
    """kuşak / kayıt ucunun karşı yüze köşe kaynağı · uc 'a0' | 'a1' · yuzler: içbükey köşe yapan yüz normalleri (kuşağın)"""
    e = EKSEN[pr.eksen] * (1.0 if uc == "a0" else -1.0)
    nok = pr.merkez(pr.a0 if uc == "a0" else pr.a1)
    for i, nf in enumerate(yuzler):
        nf = np.asarray(nf, float); ax = "xyz"[int(np.argmax(np.abs(nf)))]
        h = pr.yarim(ax) if isinstance(pr, ProfilD) else pr.b / 2.0
        w = np.cross(e, nf); dg = [k for k in "xyz" if k not in (pr.eksen, ax)][0]
        L = (flat if flat is not None else 2 * (pr.yarim(dg) if isinstance(pr, ProfilD) else pr.b / 2.0) - 2 * pr.Ro)
        p = nok + nf * h
        _kaynak(p - w * L / 2.0, p + w * L / 2.0, e, nf, a, "%s_%d" % (ad, i), not_="TIG 141 · ER308LSi · uç ↔ karşı profil")


def _tapa(pr, uc="ust", t=2.0, pah=2.5, ad=None):
    """dikdörtgen / kare profil ucuna tapa (köşeler pah · çevresi TIG alın, taşlanır)"""
    ex, ey = {"y": ((1.0, 0, 0), (0, 0, -1.0)), "x": ((0, 1.0, 0), (0, 0, 1.0)), "z": ((1.0, 0, 0), (0, 1.0, 0))}[pr.eksen]
    ex, ey = np.array(ex), np.array(ey)
    if uc == "alt": ey = -ey
    a = pr.a1 if uc == "ust" else pr.a0
    O = EKSEN[pr.eksen] * a; C = pr.merkez(a)
    hu = (pr.yarim("xyz"[int(np.argmax(np.abs(ex)))]) if isinstance(pr, ProfilD) else pr.b / 2.0)
    hv = (pr.yarim("xyz"[int(np.argmax(np.abs(ey)))]) if isinstance(pr, ProfilD) else pr.b / 2.0)
    cu, cv = float(np.dot(C, ex)), float(np.dot(C, ey)); c = pah
    u0, u1, v0, v1 = cu - hu, cu + hu, cv - hv, cv + hv
    s = G.sac(ad or pr.ad + "_tapa", "braket", t=t)
    s.taban([(u0 + c, v0), (u1 - c, v0), (u1, v0 + c), (u1, v1 - c), (u1 - c, v1), (u0 + c, v1), (u0, v1 - c), (u0, v0 + c)], O=tuple(O), ex=tuple(ex), ey=tuple(ey), ad="tapa")
    return s


def _ozel(ad, sh, std, tanim, olcu, malzeme="AISI 304", mal="celik", uretim=False, tur="baglanti", meta=None):
    return G.ozel(ad, sh, std, tanim, olcu, malzeme=malzeme, mal=mal, uretim=uretim, tur=tur, meta=meta)


def _delik_kaynagi(ad, P, u, v, plaka_t, M_dunya, boy=25.0, en=8.0, aci=0.0, not_=""):
    """delik (yarık) kaynağı: P paneline 25 × 8 yarık + yarığı dolduran TIG dolgu katısı (yüzle aynı, taşlanır)"""
    P.oblong(u, v, boy, en, aci, tip="kaynak_yarigi", parca="delik kaynağı %g × %g · yüz taşlanır" % (boy, en))
    sh = P.dunya(u, v, 0.0)
    f = S.yuz_oblong(u, v, boy, en, aci)
    kat = S._tasi(S._prizma(f, plaka_t), P.M)
    G.kaynak(dict(ad=ad, wp=cq.Workplane("XY").add(kat), sh=kat, mal="sac", birim=G.birim, grup="SABIT", kaynak=SURUM, tur="kaynak",
                  bom=("Delik (yarık) kaynağı · TIG 141 · ER308LSi · yüz taşlanır", 1, "%g × %g × %g" % (boy, en, plaka_t), not_, "ÜRETİM"),
                  meta=dict(tur="kaynak", tip="delik", yontem="TIG 141", boy=boy)))


def _yer_tapa(ad, x, y, z, cap=16.0, yukari=(0, 1.0, 0), t_sac=1.5):
    """Ø16 servis deliği kapama tapası (gıda sınıfı silikon) · (x, y, z) sacın üst yüzü"""
    e = np.asarray(yukari, float)
    sh = GO.silindir(np.array([x, y, z]) - e * t_sac, e, cap / 2.0, t_sac).fuse(GO.silindir((x, y, z), e, cap / 2.0 + 2.0, 1.0))
    G.eleman(_ozel(ad, sh, "gıda sınıfı silikon (FDA 21 CFR 177.2600)", "Kapama tapası Ø%g delik · Ø%g × 1 baş · silikon" % (cap, cap + 4), "Ø%g × %g + Ø%g × 1" % (cap, t_sac, cap + 4),
                   malzeme="VMQ silikon", mal="conta"))


def _kalinlik_ek(s, n=41):
    """h3_sac_v1.kalinlik_denetle SINIRI (raporlandı, kütüphaneye yazılmadı): yüz başına 9 SABİT (u, v) oranında örnek alır (0,13–0,87) → dar çerçeve
    yüzlerinde (üst şerit: 632 × 803 açıklığın çevresi 30–50 mm) hepsi açıklığa düşer, ışın yok → 'HATA isin []'. Burada YALNIZ örneği hiç
    alınamayan yüzler n × n ızgarayla yeniden örneklenir; ≥ 3 noktada karşı yüz t ise yüz 'ana' sayılır (ölçümler rapora 'ek_ornekleme')."""
    r = s.dogrula(); k = r["kalinlik"]
    if k["gecti"]: return k
    A = s.kati_temel(); fs = A.Faces(); t = s.t; tol = max(0.01, 0.01 * t)
    it = S.IntCurvesFace_ShapeIntersector(); it.Load(A.wrapped, 1e-7)
    kalan, ek = [], []
    for h in k["hata"]:
        f = fs[h["yuz"]]
        if h["isin"] or S._yuz_ornekleri(f): kalan.append(h); continue
        Sf = S.BRepAdaptor_Surface(f.wrapped, True)
        u0, u1, v0, v1 = Sf.FirstUParameter(), Sf.LastUParameter(), Sf.FirstVParameter(), Sf.LastVParameter()
        ds = []
        for i in range(n):
            for j in range(n):
                u, v = u0 + (u1 - u0) * (i + 0.5) / n, v0 + (v1 - v0) * (j + 0.5) / n
                if S.BRepClass_FaceClassifier(f.wrapped, S.gp_Pnt2d(u, v), 1e-9).State() != S.TopAbs_IN: continue
                pr = S.BRepLProp_SLProps(Sf, u, v, 1, 1e-9)
                if not pr.IsNormalDefined(): continue
                nn = pr.Normal(); nv = np.array([nn.X(), nn.Y(), nn.Z()])
                if f.wrapped.Orientation() == S.TopAbs_REVERSED: nv = -nv
                pp = Sf.Value(u, v); q = np.array([pp.X(), pp.Y(), pp.Z()]) - nv * 1e-5
                it.Perform(S.gp_Lin(S.gp_Pnt(*q), S.gp_Dir(*(-nv))), 1e-7, 1e5)
                ws = sorted(it.WParameter(m) for m in range(1, it.NbPnt() + 1) if it.WParameter(m) > 1e-7)
                ds.append(ws[0] + 1e-5 if ws else float("inf"))
        if len(ds) >= 3 and all(abs(d - t) < tol for d in ds):
            k["ana"] += 1; ek.append(dict(yuz=h["yuz"], alan=h["alan"], ornek=len(ds), olcum=[round(min(ds), 5), round(max(ds), 5)]))
        else:
            kalan.append(dict(h, ek_ornek=len(ds), ek_olcum=[round(min(ds), 4), round(max(ds), 4)] if ds else []))
    k["hata"] = kalan; k["gecti"] = not kalan; k["ek_ornekleme"] = ek
    k["ek_not"] = "h3_sac_v1.kalinlik_denetle 9 sabit örnek noktası dar çerçeve yüzüne düşmüyor → h3_a_sac_v1._kalinlik_ek %d × %d ızgara" % (n, n)
    return k


SOMUN_IC = "DIN1587"                                                     # kabin içi somunlar: KÖR (kapalı) somun · açıcı hamuru açarken un / hamur sıçrar (reçete 4: sıçrama bölgesinde açık diş yok)


def _kor_boy(paket, dis="M5", pul="DIN9021", seri=None):
    """saplama / cıvata boyu: kör somunda diş kavraması ≥ 1d ve saplama ucu somun dibine (0,75 m − 0,5) değmez · paket = sac paketi kalınlığı"""
    h = (S.DIN9021 if pul == "DIN9021" else S.DIN125)[dis][2]; m = S.DIN1587[dis][1]
    lo, hi = paket + h + S.D_NOM[dis], paket + h + 0.75 * m - 0.5
    L = [x for x in (seri or S.SAPLAMA_BOY) if lo - 1e-9 <= x <= hi + 1e-9]
    if not L: raise ValueError("kör somun için uygun boy yok: paket %.2f · %s · aralık %.1f–%.1f" % (paket, dis, lo, hi))
    return float(L[0])


def _kulak(g, ad, A, stud, u, v, v_cerceve, L_kaynak=25.0, gen=25.0, uc=9.75, dis="M5", rol="braket"):
    """GO.kulak ile birebir aynı geometri (3 mm L kulak · FHP-M5 · DIN 9021) — tek fark: somun KÖR (DIN 1587) + saplama boyu kör somuna göre
    (GO.kulak somun standardını parametre almıyor; ortak modüle yazılmadı → raporda öneri)"""
    s = g.sac(ad, rol)
    stud = np.asarray(stud, float); u, v = np.asarray(u, float), np.asarray(v, float)
    t, R = s.t, s.R
    vb = v_cerceve - (R + t)
    va = -uc
    if vb < S.DIN9021[dis][1] / 2.0 + 1.0 - 1e-9: raise ValueError("%s: pul büküme taşar (saplama → büküm %.1f · v_cerceve %.1f)" % (ad, vb, v_cerceve))
    if uc < S.PEM_SAPLAMA[dis]["kenar"] - 1e-9: raise ValueError("%s: saplama kenar mesafesi %.2f < %.2f" % (ad, uc, S.PEM_SAPLAMA[dis]["kenar"]))
    n = np.cross(u, v)
    zA = A.yerel(stud + n * 1.0)[2]
    if -1e-6 < zA < A.sac.t + 1e-6: raise ValueError("%s: u × v A panelinin içine bakıyor (kulak sacın içinde kalır)" % ad)
    P = s.taban([(-gen / 2, va), (gen / 2, va), (gen / 2, vb), (-gen / 2, vb)], O=tuple(stud), ex=tuple(u), ey=tuple(v), ad="saplama_ayagi")
    P.flans(2, L_kaynak, yon=+1, ad="kaynak_ayagi")
    for sg in (+1, -1):
        p0 = stud + u * sg * gen / 2.0 + v * v_cerceve + n * (R + t)
        p1 = stud + u * sg * gen / 2.0 + v * v_cerceve + n * L_kaynak
        g.kaynak(S.kaynak_dikisi(p0, p1, u * sg, -v, min(t, 3.0), ad=ad + "_kaynak_%s" % ("a" if sg > 0 else "b"), birim=g.birim, taraf="dis (köşe)",
                                 not_="kulak ↔ iskelet"))
    b = S.vidali_birlesim(A, P, tuple(stud), "pem_saplama", dis=dis, somun_std=SOMUN_IC, boy=_kor_boy(A.sac.t + t, dis), ad=ad + "_bag", birim=g.birim)
    for q in b["parcalar"]: g.eleman(q)
    g.BIRLESIM.append(b); g.KULAK.append(s)
    return s, P, b


def _cd_saplama(ad, P, n, boy=8.0, dis="M5"):
    """CD saplama kaynağı (ISO 13918 PT · A2): taban flanşı panelin iç yüzünde (dış yüzde iz yok, sac_standart §5.2) · n: panelden içeri"""
    d = S.D_NOM[dis]; P = np.asarray(P, float); n = np.asarray(n, float)
    sh = GO.silindir(P, n, 6.7 / 2.0, 1.0).fuse(GO.silindir(P, n, d / 2.0 - 0.03, boy))
    return G.eleman(_ozel(ad, sh, "ISO 13918 PT", "CD kaynak saplaması %s×%g (kondansatör deşarjlı, panel arkasına · dışta iz yok)" % (dis, boy), "%s×%g · flanş Ø6,7" % (dis, boy),
                          malzeme="A2 (1.4301)", mal="celik"))


def _omega(ad, L0, L1, eksen, merkez_w, panel_noktasi, n_panel, w_ekseni, panel, h=15.0, ayak=20.0, aralik=200.0):
    """1,0 omega (şapka) takviye 20 + 15 + 40 + 15 + 20: tepe panelden h · uzunluk 'eksen' boyunca L0 → L1 · ayaklar panelin iç yüzünde.
    Bağlantı: panelin arkasına CD saplama M5 × 8 (dışta iz yok) + ayakta Ø7,5 (saplama flanşı içeride) + DIN 125 + DIN 1587 kör somun · punta YOK (görünür panel)."""
    s = G.sac(ad, "kapak_ic")                                            # 1,0 (kararlar · takviye sacı)
    t, R = s.t, s.R; g_ = R + t
    e = EKSEN[eksen]; n = np.asarray(n_panel, float); w = np.asarray(w_ekseni, float)
    P0 = np.asarray(panel_noktasi, float)
    tepe = P0 + n * h                                                   # tepenin DIŞ yüzü (panelden en uzak)
    ex, ey = e, w
    if np.dot(np.cross(ex, ey), -n) < 0: ey = -w
    O = tepe - e * float(np.dot(tepe, e)) - w * float(np.dot(tepe, w))
    cw = float(merkez_w) * float(np.dot(w, ey))
    tw = OMEGA_TEPE / 2.0
    P = s.taban([(L0, cw - tw + g_), (L1, cw - tw + g_), (L1, cw + tw - g_), (L0, cw + tw - g_)], O=tuple(O), ex=tuple(ex), ey=tuple(ey), ad="tepe")
    d1 = P.flans(0, h, yon=+1, ad="duvar_a"); d2 = P.flans(2, h, yon=+1, ad="duvar_b")
    ayaklar = []
    for d_, nm in ((d1, "ayak_a"), (d2, "ayak_b")):
        f = d_.flans(1, ayak, yon=-1, ad=nm)
        ayaklar.append(f)
    # ayak yönü denetimi (ayaklar dışa, panel üzerinde)
    for f in ayaklar:
        q = np.asarray(f.dunya(ayak / 2.0, (L1 - L0) / 2.0, 0.0), float)
        if abs(float(np.dot(q - P0, n))) > t + 1e-3: raise ValueError("%s: omega ayağı panelde değil (%.2f)" % (ad, float(np.dot(q - P0, n))))
    say = 0
    for f in ayaklar:
        for a in GO.vida_konumlari(L0, L1, maks=aralik, uc=40.0):
            q = np.asarray(f.dunya(ayak / 2.0 - g_ / 2.0, 0.0, 0.0), float); q["xyz".index(eksen)] = a
            uv = f.yerel(q)
            f.delik(uv[0], uv[1], 7.5, tip="vida_deligi", parca="CD saplama M5 geçişi (flanş Ø6,7 içeride)")
            Pp = q - n * float(np.dot(q - P0, n))                           # panel iç yüzü
            _cd_saplama("%s_saplama_%d" % (ad, say), Pp, n)
            G.eleman(S.pul("DIN125", "M5", tuple(Pp + n * t), tuple(n), ad="%s_pul_%d" % (ad, say), birim=G.birim))
            G.eleman(S.somun(SOMUN_IC, "M5", tuple(Pp + n * (t + S.DIN125["M5"][2])), tuple(n), ad="%s_somun_%d" % (ad, say), birim=G.birim))
            say += 1
    G.not_("%s: omega panele %d × CD saplama M5 × 8 (ISO 13918) + DIN 125 + DIN 1587 kör somun · punta yok (görünür panel)" % (ad, say))
    return s, P, ayaklar


# =====================================================================================================================================
# 2 · A İSKELETİ (kaynaklı alt montaj · KAIDE_A ile tek parça) — 30 × 30 × 2 · ön alt bant 30 × 20 × 2
# =====================================================================================================================================
def iskelet():
    P = G.PROF
    for ad, x, z, nt in (("onyuz_cerceve_sol_dikme", X_SOL, Z_ON_D, "sol ön dikme · gizli menteşe gövdeleri içinde"),
                         ("onyuz_cerceve_sag_dikme", X_SAG, Z_ON_D, "sağ ön dikme · bas-aç gövdeleri içinde · emniyet sensörü iç yüzde"),
                         ("a_kose_dikmesi_arka_sol", X_SOL, Z_ARKA_D, "sol arka köşe dikmesi"),
                         ("a_kose_dikmesi_arka_sag", X_SAG, Z_ARKA_D, "sağ arka köşe dikmesi · A ↔ TOPPING M8")):
        _ps(ad, "y", Y_DIKME[0], Y_DIKME[1], (x, z), not_=nt)
    yk = sum(Y_KUSAK) / 2.0
    _ps("onyuz_cerceve_ust_kayit", "x", X_SOL + PB / 2, X_SAG - PB / 2, (yk, Z_ON_D), not_="ön üst kayıt")
    _ps("a_ust_kusak_arka", "x", X_SOL + PB / 2, X_SAG - PB / 2, (yk, Z_ARKA_D), not_="arka üst kuşak")
    _ps("a_ust_kusak_sol", "z", Z_ARKA_D + PB / 2, Z_ON_D - PB / 2, (X_SOL, yk), not_="sol üst kuşak · A ↔ U_A 3 × M8 kovanlı")
    _ps("a_ust_kusak_sag", "z", Z_ARKA_D + PB / 2, Z_ON_D - PB / 2, (X_SAG, yk), not_="sağ üst kuşak · A ↔ U_A 3 × M8 kovanlı")
    _ps("onyuz_cerceve_perde_kayit", "x", X_SOL + PB / 2, X_SAG - PB / 2, (sum(Y_PERDE_KAYIT) / 2.0, Z_ON_D), not_="ışık perdesi üst kaydı")
    _ps("a_sag_bogaz_lentosu", "z", Z_BOGAZ_D[1], Z_ON_D - PB / 2, (X_SAG, sum(Y_LENTO) / 2.0), not_="ray/tabla boğazının üstü (h3_moduler_v1'den)")
    _ps("a_sag_bogaz_dikmesi", "y", Y_TABAN, Y_LENTO[1], (X_SAG, sum(Z_BOGAZ_D) / 2.0), not_="boğazın arka kenarı")
    _ps("a_sag_alt_kayit", "z", Z_ARKA_D + PB / 2, Z_BOGAZ_D[0], (X_SAG, sum(Y_ALT_KAYIT_SAG) / 2.0), not_="sağ alt kayıt (taban sacında)")
    zb = sum(Z_ALT_BANT) / 2.0
    _pd("onyuz_cerceve_sol_alt_dikme", "y", Y_ALT_DIKME[0], Y_ALT_DIKME[1], (X_SOL, zb), PB, 20.0, not_="ön alt bant · kaide önünde")
    _pd("onyuz_cerceve_sag_alt_dikme", "y", Y_ALT_DIKME[0], Y_ALT_DIKME[1], (X_SAG, zb), PB, 20.0, not_="ön alt bant · kaide önünde")
    _pd("onyuz_cerceve_alt_kayit", "x", X_SOL + PB / 2, X_SAG - PB / 2, (sum(Y_ALT_KAYIT) / 2.0, zb), PB, 20.0, not_="ön alt kayıt · ışık perdesi alt tutucuları üstünde")
    # ---- kaynak bölgeleri (profil DFM: delik / pencere bu bölgelerde YOK)
    def kb(ad, yuz, a0, a1): P[ad].kaynak_bolgesi(yuz, a0, a1)
    for y0, y1 in ((Y_KUSAK[0], Y_DIKME[1]), Y_PERDE_KAYIT):
        kb("onyuz_cerceve_sol_dikme", "+x", y0, y1); kb("onyuz_cerceve_sag_dikme", "-x", y0, y1)
    kb("a_kose_dikmesi_arka_sol", "+x", Y_KUSAK[0], Y_DIKME[1]); kb("a_kose_dikmesi_arka_sag", "-x", Y_KUSAK[0], Y_DIKME[1])
    kb("onyuz_cerceve_sol_dikme", "-z", Y_KUSAK[0], Y_DIKME[1]); kb("onyuz_cerceve_sag_dikme", "-z", Y_KUSAK[0], Y_DIKME[1])
    kb("a_kose_dikmesi_arka_sol", "+z", Y_KUSAK[0], Y_DIKME[1]); kb("a_kose_dikmesi_arka_sag", "+z", Y_KUSAK[0], Y_DIKME[1])
    kb("onyuz_cerceve_sag_dikme", "-z", Y_LENTO[0], Y_LENTO[1]); kb("a_sag_bogaz_dikmesi", "+z", Y_LENTO[0], Y_LENTO[1])
    kb("a_kose_dikmesi_arka_sag", "+z", Y_ALT_KAYIT_SAG[0], Y_ALT_KAYIT_SAG[1]); kb("a_sag_bogaz_dikmesi", "-z", Y_ALT_KAYIT_SAG[0], Y_ALT_KAYIT_SAG[1])
    kb("onyuz_cerceve_sol_alt_dikme", "+x", Y_ALT_KAYIT[0], Y_ALT_KAYIT[1]); kb("onyuz_cerceve_sag_alt_dikme", "-x", Y_ALT_KAYIT[0], Y_ALT_KAYIT[1])
    # ---- uç kaynakları (kuşak ucu ↔ dikme yüzü · dikmeyle aynı düzlemdeki yüzler alın dikişi, taşlanır → katı yok)
    alt = [(0, -1.0, 0)]; iki = [(0, 1.0, 0), (0, -1.0, 0)]
    _uc("onyuz_cerceve_ust_kayit_kaynak_sol", P["onyuz_cerceve_ust_kayit"], "a0", alt); _uc("onyuz_cerceve_ust_kayit_kaynak_sag", P["onyuz_cerceve_ust_kayit"], "a1", alt)
    _uc("a_ust_kusak_arka_kaynak_sol", P["a_ust_kusak_arka"], "a0", alt); _uc("a_ust_kusak_arka_kaynak_sag", P["a_ust_kusak_arka"], "a1", alt)
    _uc("a_ust_kusak_sol_kaynak_arka", P["a_ust_kusak_sol"], "a0", alt); _uc("a_ust_kusak_sol_kaynak_on", P["a_ust_kusak_sol"], "a1", alt)
    _uc("a_ust_kusak_sag_kaynak_arka", P["a_ust_kusak_sag"], "a0", alt); _uc("a_ust_kusak_sag_kaynak_on", P["a_ust_kusak_sag"], "a1", alt)
    _uc("onyuz_cerceve_perde_kayit_kaynak_sol", P["onyuz_cerceve_perde_kayit"], "a0", iki); _uc("onyuz_cerceve_perde_kayit_kaynak_sag", P["onyuz_cerceve_perde_kayit"], "a1", iki)
    _uc("a_sag_bogaz_lentosu_kaynak_arka", P["a_sag_bogaz_lentosu"], "a0", iki); _uc("a_sag_bogaz_lentosu_kaynak_on", P["a_sag_bogaz_lentosu"], "a1", iki)
    _uc("a_sag_alt_kayit_kaynak_arka", P["a_sag_alt_kayit"], "a0", [(0, 1.0, 0)]); _uc("a_sag_alt_kayit_kaynak_on", P["a_sag_alt_kayit"], "a1", [(0, 1.0, 0)])
    _uc("onyuz_cerceve_alt_kayit_kaynak_sol", P["onyuz_cerceve_alt_kayit"], "a0", iki); _uc("onyuz_cerceve_alt_kayit_kaynak_sag", P["onyuz_cerceve_alt_kayit"], "a1", iki)
    # ---- dikme ↔ taban sacı çevre kaynakları (iç yüzler katı; panel tarafı alın, taşlanır)
    for ad in ("onyuz_cerceve_sol_dikme", "onyuz_cerceve_sag_dikme", "a_kose_dikmesi_arka_sol", "a_kose_dikmesi_arka_sag", "a_sag_bogaz_dikmesi"):
        pr = P[ad]; x, z = pr.c; sx = 1.0 if x < 1000 else -1.0
        px = x + sx * PB / 2
        if ad.startswith("onyuz"):                                       # ön dikme: taban sacı z 27–37 (37–57 alt dikmenin üst ucu)
            _kaynak((x - 11, Y_TABAN, z - PB / 2), (x + 11, Y_TABAN, z - PB / 2), (0, 0, -1.0), (0, 1.0, 0), 2.0, ad + "_taban_kaynagi_z")
        else:
            sz = 1.0
            _kaynak((px, Y_TABAN, z - 11), (px, Y_TABAN, z + 11), (sx, 0, 0), (0, 1.0, 0), 2.0, ad + "_taban_kaynagi_x")
            if ad != "a_kose_dikmesi_arka_sag":                              # sağ arka dikmenin +z yüzüne sağ alt kayıt oturuyor (kayıt ucu kaynaklı)
                _kaynak((x - 11, Y_TABAN, z + sz * PB / 2), (x + 11, Y_TABAN, z + sz * PB / 2), (0, 0, sz), (0, 1.0, 0), 2.0, ad + "_taban_kaynagi_z")
    # ---- tapalar
    for ad in ("onyuz_cerceve_sol_dikme", "onyuz_cerceve_sag_dikme", "a_kose_dikmesi_arka_sol", "a_kose_dikmesi_arka_sag", "a_sag_bogaz_dikmesi"):
        _tapa(P[ad], "ust")
    for ad in ("onyuz_cerceve_sol_alt_dikme", "onyuz_cerceve_sag_alt_dikme"):
        _tapa(P[ad], "alt")
    # ---- ara lamalar 2 mm (ön alt bant ↔ kaide ön profili · kaynaklı)
    for nm, (x0, x1), (y0, y1) in ARA_LAMA:
        s = G.sac("onyuz_cerceve_ara_lama_" + nm, "braket", t=2.0)
        s.taban([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], O=(0, 0, KA_Z[1]), ex=(1, 0, 0), ey=(0, 1, 0), ad="lama")
        _kaynak((x0, y1, KA_Z[1]), (x1, y1, KA_Z[1]), (0, 1.0, 0), (0, 0, 1.0), 2.0, "onyuz_cerceve_ara_lama_%s_kaynak_ust" % nm,
                not_="2 mm boşlukta: lama üst kenarı + kaide ön yüzü + alt bant arka yüzü birlikte (TIG, taşlanmaz · görünmez)")
        _kaynak((x0, y0, KA_Z[1]), (x1, y0, KA_Z[1]), (0, -1.0, 0), (0, 0, 1.0), 2.0, "onyuz_cerceve_ara_lama_%s_kaynak_alt" % nm,
                not_="2 mm boşlukta: lama alt kenarı + kaide ön yüzü + alt bant arka yüzü birlikte")
    G.not_("ön dikme alt ucu: taban sacına (z 27–37) + ön alt bant dikmesinin üst ucuna (z 37–57) çevre TIG (taşlanır) · alt dikme ↔ lama ↔ kaide ön profili kaynaklı")


# =====================================================================================================================================
# 3 · KAİDELER (100 × 40 × 2 dik · 4 mm plaka · delik kaynağı) — KAIDE_A + KAIDE_C
# =====================================================================================================================================
def _plaka(ad, x0, x1, z0, z1, t=4.0, pah=0.0):
    """kaide üst plakası (y 888–892) · pah: arka-sol köşe (x0, z0) pahı (sol yan sacın arka büküm bölgesi)"""
    s = G.sac(ad, "braket", t=t)
    poly = [(x0, -z1), (x1, -z1), (x1, -z0), (x0 + pah, -z0), (x0, -z0 - pah)] if pah else [(x0, -z1), (x1, -z1), (x1, -z0), (x0, -z0)]
    P = s.taban(poly, O=(0, Y_PL, 0), ex=(1, 0, 0), ey=(0, 0, -1.0), ad="plaka")
    return s, P


def _plaka_kaynaklari(onek, P, t, hatlar, kacin, aralik=230.0):
    """plaka → profil delik kaynakları · hatlar: [(eksen, a0, a1, sabit)] ('x': x a0–a1, z sabit · 'z': z a0–a1, x sabit) · kacin: [(x, z, r)]"""
    i = 0
    for eks, a0, a1, c in hatlar:
        for a in GO.vida_konumlari(a0 + 20.0, a1 - 20.0, maks=aralik, uc=20.0):
            x, z = (a, c) if eks == "x" else (c, a)
            if any(math.hypot(x - kx, z - kz) < kr + 22.0 for kx, kz, kr in kacin): continue
            if not P.icerir(x, -z): continue
            _delik_kaynagi("%s_delik_kaynagi_%d" % (onek, i), P, x, -z, t, None, aci=0.0 if eks == "x" else 90.0, not_="plaka ↔ profil üst duvarı · yüz taşlanır")
            i += 1
    return i


def kaide_A():
    zf, zb = KA_Z[1] - KB / 2, KA_Z[0] + KB / 2
    zi0, zi1 = KA_Z[0] + KB, KA_Z[1] - KB
    on = _pd("kaide_A_on_profil", "x", KA_X[0], KA_X[1], (YK, zf), KH, KB, t=KT, not_="KAIDE_A ön")
    ar = _pd("kaide_A_arka_profil", "x", KA_X_ARKA0, KA_X[1], (YK, zb), KH, KB, t=KT, not_="KAIDE_A arka (1,5 içeri: yan sac dönüşü · sol ucu 740,5: dönüşün büküm bölgesi)")
    ys = _pd("kaide_A_yan_profil_sol", "z", zi0, zi1, (KA_X[0] + KB / 2, YK), KB, KH, t=KT, not_="KAIDE_A sol · → B M8")
    yg = _pd("kaide_A_yan_profil_sag", "z", zi0, zi1, (KA_X[1] - KB / 2, YK), KB, KH, t=KT, not_="KAIDE_A sağ")
    en = _pd("kaide_A_enine_profil_0", "z", zi0, zi1, (KA_ENINE_X, YK), KB, KH, t=KT, not_="açıcı kolonu altı enine")
    b0 = _pd("kaide_A_boyuna_profil_0", "x", KA_X[0] + KB, KA_ENINE_X - KB / 2, (YK, KA_BOYUNA_Z), KH, KB, t=KT, not_="kolon dikmesi altı boyuna")
    b1 = _pd("kaide_A_boyuna_profil_1", "x", KA_ENINE_X + KB / 2, KA_X[1] - KB, (YK, KA_BOYUNA_Z), KH, KB, t=KT, not_="kolon dikmesi altı boyuna")
    for xc in (KA_X[0] + KB / 2, KA_ENINE_X, KA_X[1] - KB / 2):
        on.kaynak_bolgesi("-z", xc - KB / 2, xc + KB / 2); ar.kaynak_bolgesi("+z", xc - KB / 2, xc + KB / 2)
    ys.kaynak_bolgesi("+x", KA_BOYUNA_Z - KB / 2, KA_BOYUNA_Z + KB / 2); yg.kaynak_bolgesi("-x", KA_BOYUNA_Z - KB / 2, KA_BOYUNA_Z + KB / 2)
    en.kaynak_bolgesi("-x", KA_BOYUNA_Z - KB / 2, KA_BOYUNA_Z + KB / 2); en.kaynak_bolgesi("+x", KA_BOYUNA_Z - KB / 2, KA_BOYUNA_Z + KB / 2)
    yx = [(1.0, 0, 0), (-1.0, 0, 0)]; yz = [(0, 0, 1.0), (0, 0, -1.0)]
    for pr, nm, yy in ((ys, "yan_sol", [(1.0, 0, 0)]), (yg, "yan_sag", [(-1.0, 0, 0)]), (en, "enine_0", yx)):   # yan profillerin dış yüzü ön/arka profilin ucuyla aynı düzlem → alın dikişi (taşlanır)
        _uc("kaide_A_%s_kaynak_arka" % nm, pr, "a0", yy); _uc("kaide_A_%s_kaynak_on" % nm, pr, "a1", yy)
    _uc("kaide_A_boyuna_0_kaynak_sol", b0, "a0", yz); _uc("kaide_A_boyuna_0_kaynak_sag", b0, "a1", yz)
    _uc("kaide_A_boyuna_1_kaynak_sol", b1, "a0", yz); _uc("kaide_A_boyuna_1_kaynak_sag", b1, "a1", yz)
    # üst plaka 4 (888–892)
    s, PL = _plaka("kaide_A_ust_plaka_4", KA_X[0], KA_X[1], KA_Z[0], KA_Z[1], pah=KA_KOSE_PAH)
    G.PANEL["kaide_A_plaka"] = PL
    kacin = [(x, z, 8.0) for x, z in M8_B_A] + [(x, z, 4.5) for x, z in KOLON_ANKRAJ]
    _plaka_kaynaklari("kaide_A_ust_plaka_4", PL, 4.0, [("x", KA_X[0], KA_X[1], zf), ("x", KA_X[0], KA_X[1], zb), ("z", zi0, zi1, KA_X[0] + KB / 2),
                                                      ("z", zi0, zi1, KA_X[1] - KB / 2), ("z", zi0, zi1, KA_ENINE_X),
                                                      ("x", KA_X[0] + KB, KA_ENINE_X - KB / 2, KA_BOYUNA_Z), ("x", KA_ENINE_X + KB / 2, KA_X[1] - KB, KA_BOYUNA_Z)], kacin)
    # taban sacı 1,5 (892–893,5) · plakaya delik kaynağı · kolon dikmesi deliği (kaide_cad_v4)
    tb = G.sac("kaide_A_mekanizma_taban_saci", "yuk")
    TB = tb.taban([(KA_X[0], -Z_ALT_BANT[0]), (KA_X[1], -Z_ALT_BANT[0]), (KA_X[1], -KA_Z[0]), (KA_X[0] + KA_KOSE_PAH, -KA_Z[0]), (KA_X[0], -KA_Z[0] - KA_KOSE_PAH)],
                  O=(0, Y_MEK, 0), ex=(1, 0, 0), ey=(0, 0, -1.0), ad="taban")
    x0, x1, z0, z1 = KOLON_DELIK
    TB.dikdortgen((x0 + x1) / 2.0, -(z0 + z1) / 2.0, x1 - x0, z1 - z0, tip="kolon_deligi", parca="açıcı kolonu dikmesi 122 × 52 (kolon plakaya oturur)")
    G.PANEL["kaide_A_taban"] = TB
    i = 0
    for x in (800.0, 960.0, 1240.0, 1380.0):
        for z in (-560.0, -330.0, -60.0):
            _delik_kaynagi("kaide_A_mekanizma_taban_saci_delik_kaynagi_%d" % i, TB, x, -z, 1.5, None, boy=20.0, en=6.0, not_="taban sacı ↔ plaka · yüz taşlanır"); i += 1
    # açıcı kolonu ankrajı: 4 × M8 kaynak somunu plakanın altında (plaka çerçeveye kaynaklanmadan ÖNCE)
    for x, z in KOLON_ANKRAJ:
        PL.delik(x, -z, 9.0, tip="vida_deligi", parca="açıcı kolonu ankrajı M8 (ISO 273 orta)")
        TB.delik(x, -z, 9.0, tip="vida_deligi", parca="açıcı kolonu ankrajı M8")
        G.eleman(S.kaynak_somunu("M8", (x, Y_PL, z), (0, -1.0, 0), ad="kaide_A_kolon_ankraj_somunu_%d_%d" % (int(x), int(-z)), birim=G.birim))
        G.arayuz(S.vida("ISO4762", "M8", 20, (x, Y_TABAN + 6.0, z), (0, -1.0, 0), ad="arayuz_kolon_ankraj_%d_%d" % (int(x), int(-z)), birim=G.birim),
                 "TOPPING acici_kolonu (açıcı · satın alma)", "kolon taban flanşında Ø9 (VARSAYIM 6 mm flanş · satıcı föyünden teyit) · ISO 4762 M8 × 20 + DIN 125", "açıcı tedarikçisi")
    return dict(on=on, ar=ar, ys=ys, yg=yg, en=en, plaka=PL, taban=TB)


def kaide_C():
    zf, zb = KC_Z[1] - KB / 2, KC_Z[0] + KB / 2
    zi0, zi1 = KC_Z[0] + KB, KC_Z[1] - KB
    on = _pd("kaide_C_on_profil", "x", KC_X[0], KC_X[1], (YK, zf), KH, KB, t=KT, not_="KAIDE_C ön · 3 hava penceresi")
    ar = _pd("kaide_C_arka_profil", "x", KC_X[0], KC_X[1], (YK, zb), KH, KB, t=KT, not_="KAIDE_C arka · arka emiş penceresi")
    ys = _pd("kaide_C_yan_profil_sol", "z", zi0, zi1, (KC_X[0] + KB / 2, YK), KB, KH, t=KT, not_="KAIDE_C sol")
    yg = _pd("kaide_C_yan_profil_sag", "z", zi0, zi1, (KC_X[1] - KB / 2, YK), KB, KH, t=KT, not_="KAIDE_C sağ")
    en = _pd("kaide_C_enine_profil_2", "z", zi0, zi1, (KC_ENINE_X, YK), KB, KH, t=KT, not_="göz 3 | göz 4")
    b0 = _pd("kaide_C_boyuna_profil_0", "x", KC_X[0] + KB, KC_ENINE_X - KB / 2, (YK, KC_BOYUNA_Z), KH, KB, t=KT, not_="göz 1+3 boyuna (tek parça)")
    b3 = _pd("kaide_C_boyuna_profil_3", "x", KC_ENINE_X + KB / 2, KC_X[1] - KB, (YK, KC_BOYUNA_Z), KH, KB, t=KT, not_="göz 4 boyuna")
    yk_ = sum(KC_PENCERE_Y) / 2.0 - YK; lk = KC_PENCERE_Y[1] - KC_PENCERE_Y[0]
    for a, b in KC_PENCERE_ON:                                          # iki et birden (ön + arka duvar)
        for yz_ in ("+z", "-z"): on.duvar_pencere(yz_, (a + b) / 2.0, yk_, b - a, lk, tip="hava_penceresi", not_="soğutma grubu %s" % ("emiş" if a < 1620 else "atış"))
    for a, b in KC_PENCERE_ARKA:
        for yz_ in ("+z", "-z"): ar.duvar_pencere(yz_, (a + b) / 2.0, yk_, b - a, lk, tip="hava_penceresi", not_="arka emiş (filtre içte)")
    for pr, x0, x1 in ((b0, KC_X[0] + KB, KC_ENINE_X - KB / 2), (b3, KC_ENINE_X + KB / 2, KC_X[1] - KB)):
        for a, b in KC_PENCERE_ON:
            if a >= x0 - 1e-6 and b <= x1 + 1e-6:
                for yz_ in ("+z", "-z"): pr.duvar_pencere(yz_, (a + b) / 2.0, yk_, b - a, lk, tip="hava_penceresi", not_="göz içi hava geçişi")
    for xc in (KC_X[0] + KB / 2, KC_ENINE_X, KC_X[1] - KB / 2):
        on.kaynak_bolgesi("-z", xc - KB / 2, xc + KB / 2); ar.kaynak_bolgesi("+z", xc - KB / 2, xc + KB / 2)
    ys.kaynak_bolgesi("+x", KC_BOYUNA_Z - KB / 2, KC_BOYUNA_Z + KB / 2); yg.kaynak_bolgesi("-x", KC_BOYUNA_Z - KB / 2, KC_BOYUNA_Z + KB / 2)
    en.kaynak_bolgesi("-x", KC_BOYUNA_Z - KB / 2, KC_BOYUNA_Z + KB / 2); en.kaynak_bolgesi("+x", KC_BOYUNA_Z - KB / 2, KC_BOYUNA_Z + KB / 2)
    yx = [(1.0, 0, 0), (-1.0, 0, 0)]; yz = [(0, 0, 1.0), (0, 0, -1.0)]
    for pr, nm, yy in ((ys, "yan_sol", [(1.0, 0, 0)]), (yg, "yan_sag", [(-1.0, 0, 0)]), (en, "enine_2", yx)):
        _uc("kaide_C_%s_kaynak_arka" % nm, pr, "a0", yy); _uc("kaide_C_%s_kaynak_on" % nm, pr, "a1", yy)
    _uc("kaide_C_boyuna_0_kaynak_sol", b0, "a0", yz); _uc("kaide_C_boyuna_0_kaynak_sag", b0, "a1", yz)
    _uc("kaide_C_boyuna_3_kaynak_sol", b3, "a0", yz); _uc("kaide_C_boyuna_3_kaynak_sag", b3, "a1", yz)
    # üst plaka 4 · emiş / ünite cebi açıklıkları + (atış açıklığı ∪ ana besleme geçişi) tek kesik
    s, PL = _plaka("kaide_C_ust_plaka_4", KC_X[0], KC_X[1], KC_Z[0], KC_Z[1])
    G.PANEL["kaide_C_plaka"] = PL
    for x0, x1, z0, z1 in KC_PLAKA_KESIK:
        PL.dikdortgen((x0 + x1) / 2.0, -(z0 + z1) / 2.0, x1 - x0, z1 - z0, tip="hava_acikligi", parca="soğutma grubu emiş / ünite cebi (kaide_cad_v4)")
    (a0, a1, c0, c1), (e0, e1, f0, f1) = KC_ATIS_ELK
    PL.kesik([(a0, -c1), (a1, -c1), (a1, -f1), (e1, -f1), (e1, -f0), (a1, -f0), (a1, -c0), (a0, -c0)], tip="hava_acikligi",
             parca="atış açıklığı + ana besleme kanalı geçişi (h3/_elk KD kaide_C_ust_plaka_4 · tek kesik, ince köprü yok)")
    kacin = [(x, z, 8.0) for x, z in M8_B_C] + [(x, z, 3.0) for x, z in M6_TC]
    hat = [("x", KC_X[0], KC_X[1], zf), ("x", KC_X[0], KC_X[1], zb), ("z", zi0, zi1, KC_X[0] + KB / 2), ("z", zi0, zi1, KC_ENINE_X),
           ("z", zi0, zi1, KC_X[1] - KB / 2), ("x", KC_X[0] + KB, KC_ENINE_X - KB / 2, KC_BOYUNA_Z), ("x", KC_ENINE_X + KB / 2, KC_X[1] - KB, KC_BOYUNA_Z)]
    _plaka_kaynaklari("kaide_C_ust_plaka_4", PL, 4.0, hat, kacin)
    # soğutma grubu tepsisi ön köşebendi L 3 mm (boyuna profilin arka yüzüne · pencerenin altından kaynak)
    kt = G.sac("kaide_C_tepsi_kosebendi", "braket")
    gk = kt.R + kt.t
    zk = KC_BOYUNA_Z - KB / 2                                            # boyuna arka yüzü −435
    KTP = kt.taban([(KC_TEPSI[0], Y_DUZ + 2.0), (KC_TEPSI[1], Y_DUZ + 2.0), (KC_TEPSI[1], 806.0 - gk), (KC_TEPSI[0], 806.0 - gk)],
                   O=(0, 0, zk - kt.t), ex=(1, 0, 0), ey=(0, 1, 0), ad="dik_ayak")
    YT = KTP.flans(2, 33.0, yon=-1, ad="tepsi_ayagi")
    G.PANEL["kaide_C_kosebent"] = YT
    for x in (1700.0, 1946.0):
        P0 = np.array([x, 806.0, zk - 33.0 / 2.0 - 2.0])
        q = YT.yerel(P0)
        alt = np.asarray(YT.dunya(q[0], q[1], 0.0), float); ust = np.asarray(YT.dunya(q[0], q[1], kt.t), float)
        if ust[1] < alt[1]: alt, ust = ust, alt
        ps, c, ms = S.pem_somun("SP", "M5", tuple(alt), (0, -1.0, 0), kt.t, ad="kaide_C_tepsi_kosebendi_pem_%d" % int(x), birim=G.birim)
        YT.delik(q[0], q[1], c["delik"], tip="pem_somun", parca=ps["meta"]["parca"], pem_tip="SP", kenar_min=c["kenar"], min_sac=ms)
        G.eleman(ps)
        G.arayuz(S.vida("ISO7380", "M5", 10, (x, ust[1] + 3.0, alt[2]), (0, -1.0, 0), ad="arayuz_tepsi_%d" % int(x), birim=G.birim),
                 "TOPPING sogutma_grubu_tepsisi", "tepsinin ön kenarında Ø5,5 · ISO 7380 M5 × 10 → köşebentteki PEM SP-M5", "TOPPING sahibi")
    _kaynak((KC_TEPSI[0], Y_DUZ + 2.0, zk), (KC_TEPSI[1], Y_DUZ + 2.0, zk), (0, -1.0, 0), (0, 0, -1.0), 2.0,
            "kaide_C_tepsi_kosebendi_kaynak", not_="köşebent alt kenarı ↔ boyuna profil arka yüzü (pencerenin altında)")
    G.not_("KAIDE_C: 6 mm dilim artığı enine profil KALKTI · göz 1 + göz 3 tek göz (plaka sehimi ≈ 1,2 mm @ 400 kg VARSAYIM, açık: üretimde ölçülecek)")
    return dict(on=on, ar=ar, ys=ys, yg=yg, en=en, plaka=PL)


# =====================================================================================================================================
# 4 · SÖKÜLEBİLİR PANELLER (dış 1,5 · R 2,25 · K 0,45) + omega takviyeler
# =====================================================================================================================================
def paneller():
    # ---- sol yan sac (x 736–737,5 · y 788–1860,5 · ön 12 + arka 22 iç dönüş)
    s = G.sac("a_govde_sol_yan", "dis", kabuk=True); g_ = s.R + s.t
    P = s.taban([(Y_DUZ, Z_ARKA_IC + g_), (Y_UST_ALT, Z_ARKA_IC + g_), (Y_UST_ALT, Z_ON - g_), (Y_DUZ, Z_ON - g_)], O=(X_A0, 0, 0), ex=(0, 1, 0), ey=(0, 0, 1), ad="yan")
    arka = P.flans(0, 22.0, yon=+1, ad="arka_donus"); on = P.flans(2, 12.0, yon=+1, ad="on_donus")
    G.PANEL["sol"] = dict(yan=P, arka=arka, on=on, s=s)
    # ---- sağ duvar (x 1434–1435,5 · y 893,5–1860,5 · ray/tabla boğazı alttan çentik · ön 12 + arka 22) · h3_moduler_v1 A_bagimsiz_sag_duvar_1p5'in yerine
    s = G.sac("a_govde_sag_yan", "dis", kabuk=True); g_ = s.R + s.t
    za, zo = Z_ARKA_IC + g_, Z_ON - g_
    bz0, bz1 = BOGAZ["z"]; by1 = BOGAZ["y"][1]
    poly = [(za, Y_TABAN), (bz0, Y_TABAN), (bz0, by1), (bz1, by1), (bz1, Y_TABAN), (zo, Y_TABAN), (zo, Y_UST_ALT), (za, Y_UST_ALT)]
    R_ = s.taban(poly, O=(X_SAG_DIS, 0, 0), ex=(0, 0, 1), ey=(0, 1, 0), ad="yan")
    on_r = R_.flans(5, 12.0, yon=+1, ad="on_donus"); arka_r = R_.flans(7, 22.0, yon=+1, ad="arka_donus")
    for nm, y, z in RAKOR_G:
        R_.delik(z, y, RAKOR_CAP, tip="gecis", parca="%s rakoru (TC dis_yan_sol ile hizalı Ø%g)" % (nm, RAKOR_CAP))
    G.PANEL["sag"] = dict(yan=R_, arka=arka_r, on=on_r, s=s)
    # ---- arka sac (z −830…−828,5 · x 736–1435,5 · y 788–1862 · düz, sökülür, arka = servis yüzü → ISO 7380 serbest)
    s = G.sac("a_govde_arka", "dis", kabuk=True)
    A = s.taban([(X_A0, Y_DUZ), (X_SAG_DIS, Y_DUZ), (X_SAG_DIS, Y_UST), (X_A0, Y_UST)], O=(0, 0, Z_ARKA), ex=(1, 0, 0), ey=(0, 1, 0), ad="arka")
    G.PANEL["arka"] = dict(arka=A, s=s)
    # ---- üst şerit (y 1860,5–1862 · 632 × 803 açıklıklı çerçeve · ön + arka aşağı dönüş) — U_A tabanı bunun üstüne oturur
    s = G.sac("a_govde_ust", "dis", kabuk=True); g_ = s.R + s.t
    U = s.taban([(X_A0, -Z_ON + g_), (X_SAG_DIS, -Z_ON + g_), (X_SAG_DIS, -Z_ARKA_IC - g_), (X_A0, -Z_ARKA_IC - g_)], O=(0, Y_UST_ALT, 0), ex=(1, 0, 0), ey=(0, 0, -1.0), ad="ust")
    on_u = U.flans(0, Y_UST - 1840.5, yon=-1, bas=14.5, son=16.0, ad="on_donus")
    arka_u = U.flans(2, Y_UST - 1840.5, yon=-1, bas=25.0, son=25.0, ad="arka_donus")
    x0, x1, z0, z1 = UST_ACIKLIK
    U.dikdortgen((x0 + x1) / 2.0, -(z0 + z1) / 2.0, x1 - x0, z1 - z0, tip="ust_aciklik", parca="v3.4 A + U_A tek hacim açıklığı 632 × 803 (montaj _v34_ac ile aynı)")
    G.PANEL["ust"] = dict(ust=U, on=on_u, arka=arka_u, s=s)
    # ---- omega takviyeler (1,0 · CD saplama + somun · punta YOK)
    _omega("a_govde_sol_yan_omega", Z_ARKA_D + PB / 2 + 5.0, Z_ON_D - PB / 2 - 5.0, "z", OMEGA_Y, (X_SOL_IC, OMEGA_Y, 0.0), (1.0, 0, 0), (0, 1.0, 0), P)
    _omega("a_govde_sag_yan_omega", Z_ARKA_D + PB / 2 + 5.0, Z_ON_D - PB / 2 - 5.0, "z", OMEGA_Y, (X_SAG_IC, OMEGA_Y, 0.0), (-1.0, 0, 0), (0, 1.0, 0), R_)
    _omega("a_govde_arka_omega", X_SOL + PB / 2 + 5.0, X_SAG - PB / 2 - 5.0, "x", 1300.0, (0.0, 1300.0, Z_ARKA_IC), (0, 0, 1.0), (0, 1.0, 0), A)


# =====================================================================================================================================
# 5 · PANEL KULAKLARI (3 mm L · FHP-M5) + arka sac bağlantıları (ISO 7380 + PEM SP-M5 / M5 perçin somun)
# =====================================================================================================================================
def kulaklar():
    L, R_ = G.PANEL["sol"]["yan"], G.PANEL["sag"]["yan"]
    zo_k, za_k = Z_ON_D - PB / 2 - 19.0, Z_ARKA_D + PB / 2 + 19.0        # 8 · −766
    for y in KUL_SOL_ON: _kulak(G, "govde_kulak_sol_on_%d" % int(y), L, (X_SOL_IC, y, zo_k), (0, 1.0, 0), (0, 0, 1.0), 19.0)
    for y in KUL_SOL_ARKA: _kulak(G, "govde_kulak_sol_arka_%d" % int(y), L, (X_SOL_IC, y, za_k), (0, -1.0, 0), (0, 0, -1.0), 19.0)
    for y in KUL_SAG_ON: _kulak(G, "govde_kulak_sag_on_%d" % int(y), R_, (X_SAG_IC, y, zo_k), (0, -1.0, 0), (0, 0, 1.0), 19.0)
    for y in KUL_SAG_ARKA: _kulak(G, "govde_kulak_sag_arka_%d" % int(y), R_, (X_SAG_IC, y, za_k), (0, 1.0, 0), (0, 0, -1.0), 19.0)
    for y in KUL_BOGAZ_Y: _kulak(G, "govde_kulak_sag_bogaz_%d" % int(y), R_, (X_SAG_IC, y, Z_BOGAZ_D[0] - 19.0), (0, -1.0, 0), (0, 0, 1.0), 19.0)
    for z in KUL_LENTO_Z: _kulak(G, "govde_kulak_sag_lento_%d" % int(-z), R_, (X_SAG_IC, Y_LENTO[1] + 19.0, z), (0, 0, -1.0), (0, -1.0, 0), 19.0)
    for z in KUL_ALT_KAYIT_Z: _kulak(G, "govde_kulak_sag_alt_kayit_%d" % int(-z), R_, (X_SAG_IC, Y_ALT_KAYIT_SAG[1] + 19.0, z), (0, 0, -1.0), (0, -1.0, 0), 19.0)
    P = G.PROF
    for ys_, ad in ((KUL_SOL_ON, "onyuz_cerceve_sol_dikme"), (KUL_SOL_ARKA, "a_kose_dikmesi_arka_sol"), (KUL_SAG_ON, "onyuz_cerceve_sag_dikme"), (KUL_SAG_ARKA, "a_kose_dikmesi_arka_sag")):
        yuz = "-z" if ad.startswith("onyuz") else "+z"
        for y in ys_: P[ad].kaynak_bolgesi(yuz, y - 12.5, y + 12.5)
    for y in KUL_BOGAZ_Y: P["a_sag_bogaz_dikmesi"].kaynak_bolgesi("-z", y - 12.5, y + 12.5)
    for z in KUL_LENTO_Z: P["a_sag_bogaz_lentosu"].kaynak_bolgesi("+y", z - 12.5, z + 12.5)
    for z in KUL_ALT_KAYIT_Z: P["a_sag_alt_kayit"].kaynak_bolgesi("+y", z - 12.5, z + 12.5)


def arka_baglantilari():
    """arka sac (z −830 KEMAL KURALI · dışa taşan baş YOK · K pilotu v1.1 gibi): arka saca preslenmiş PEM FHP-M5 gömme saplama (baş dış yüzle aynı) →
    sol yan / sağ duvar / üst şerit arka dönüşlerinde Ø5,5 · DIN 9021 + DIN 1587 kör somun İÇERİDEN (dikme ↔ dönüş arası 12 mm yarıktan SW8 açık ağız) ·
    alt kenar: taban sacına kaynaklı 3 mm L kulaklar (x 790 / 980 / 1170 / 1360) aynı FHP + somun · kaide bandı (788–893,5) serbest etek, kaide arka
    profiline 1,5 boşluk (bantta dönüşün arkası kaide profili → somun yeri yok)"""
    A = G.PANEL["arka"]["arka"]
    for tr, xx, ys in (("sol", X_A0 + 12.5, ARKA_SOL_Y), ("sag", X_SAG_DIS - 12.5, ARKA_SAG_Y)):
        for y in ys:
            b = S.vidali_birlesim(A, G.PANEL[tr]["arka"], (xx, y, Z_ARKA), "pem_saplama", somun_std=SOMUN_IC, boy=_kor_boy(3.0), ad="govde_bag_arka_%s_%d" % (tr, int(y)), birim=G.birim)
            for q in b["parcalar"]: G.eleman(q)
            G.BIRLESIM.append(b)
    for x in ARKA_UST_X:
        b = S.vidali_birlesim(A, G.PANEL["ust"]["arka"], (x, 1849.5, Z_ARKA), "pem_saplama", somun_std=SOMUN_IC, boy=_kor_boy(3.0), ad="govde_bag_arka_ust_%d" % int(x), birim=G.birim)
        for q in b["parcalar"]: G.eleman(q)
        G.BIRLESIM.append(b)
    for x in ARKA_KAIDE_X:                                               # alt kenar → taban sacına kaynaklı L kulak (kaide + iskelet tek kaynaklı alt montaj)
        _kulak(G, "govde_kulak_arka_taban_%d" % int(x), A, (x, Y_TABAN + 19.0, Z_ARKA_IC), (-1.0, 0, 0), (0, -1.0, 0), 19.0)
    G.not_("arka sac: 0 dış baş (FHP-M5 gömme saplama) · alt kenar 4 L kulak taban sacında · kaide bandı serbest etek (1,5 boşluk, kaide arka profili arkasında)")


# =====================================================================================================================================
# 6 · İSTASYON ↔ İSTASYON BAĞLANTI NOKTALARI (A tarafı hazır · cıvata/pul ARAYÜZ · karşı delik KARSI_DELIK)
# =====================================================================================================================================
def _karsi(et, karsi, kod, cap, sac_t, eksen, P, yer, not_=""):
    kd = dict(etiket=et, karsi=karsi, karsi_kod=kod, cap=cap, sac_t=sac_t, eksen=[float(c) for c in eksen], merkez_dunya=[round(float(c), 2) for c in CER.nokta(P)],
              merkez_yerel=[round(float(c), 2) for c in P], not_=not_)
    G.KARSI_DELIK.append(kd)
    G.M8.append(dict(etiket=et, taraf=kod, yer=yer, dunya=[round(float(c), 1) for c in CER.nokta(P)], karsi_delik=kd))
    return kd


def m8_u():
    """A ↔ U_A: yan üst kuşaklardan geçen M8 (kovanlı) · A üst şeridi + U_A taban sacı aynı cıvatayla sandviç · cıvata U_A içinden, somun A içinde"""
    U = G.PANEL["ust"]["ust"]; hp = S.DIN125["M8"][2]
    for x, z in M8_U:
        pr = G.PROF["a_ust_kusak_sol" if x < 1000 else "a_ust_kusak_sag"]
        et = "U_%d_%d" % (int(x), int(-z))
        pr.duvar_delik("-y", z, 0.0, 9.0, tip="m8_civata", not_="A ↔ U_A M8 (alt duvar)")
        pr.duvar_delik("+y", z, 0.0, 12.2, tip="m8_kovan", not_="kovan Ø12 (üst duvar · kovan üst yüzle aynı, çevre kaynağı taşlanır)")
        y0 = Y_KUSAK[0] + PT
        kv = GO.halka((x, y0, z), (0, 1.0, 0), 6.0, 4.5, Y_KUSAK[1] - y0)
        G.eleman(_ozel("govde_m8_%s_kovan" % et, kv, "özel (304 boru Ø12 × 1,5)", "Kovan AISI 304 Ø12 × 1,5 · L %.0f (kuşak ezilmesin · üst yüzle aynı, kaynak taşlanır)" % (Y_KUSAK[1] - y0),
                       "Ø12/Ø9 × %.0f" % (Y_KUSAK[1] - y0), uretim=True, mal="sac"))
        U.delik(x, -z, 9.0, tip="vida_deligi", parca="A ↔ U_A M8 (ISO 273 orta)")
        G.eleman(S.pul("DIN125", "M8", (x, Y_KUSAK[0], z), (0, -1.0, 0), ad="govde_m8_%s_pul" % et, birim=G.birim))
        G.eleman(S.somun(SOMUN_IC, "M8", (x, Y_KUSAK[0] - hp, z), (0, -1.0, 0), ad="govde_m8_%s_somun" % et, birim=G.birim))
        yu = Y_UST + 1.5                                                  # U_A taban sacının üst yüzü
        G.arayuz(S.pul("DIN125", "M8", (x, yu, z), (0, 1.0, 0), ad="arayuz_m8_%s_pul" % et, birim=G.birim), "U_A_GOVDE ust_a_taban_sac", "U_A taban sacında Ø9 (aynı eksen)", "")
        G.arayuz(S.vida("ISO4762", "M8", 45, (x, yu + hp, z), (0, -1.0, 0), ad="arayuz_m8_%s" % et, birim=G.birim), "U_A_GOVDE ust_a_taban_sac",
                 "ISO 4762 M8 × 45 A2-70 + DIN 125 · U_A içinden takılır · altta A'nın DIN 125 + DIN 1587 kör somunu (uç 8,8 mm kavrar, somun dibine 2,4 kalır)", "")
        _karsi(et, "U_A_GOVDE ust_a_taban_sac", "U", 9.0, 1.5, (0, -1.0, 0), np.array([x, Y_UST, z]), pr.ad, "U_A tabanı A üst şeridinin üstünde (sandviç)")


def m8_t():
    """A ↔ TOPPING: sağ arka dikmenin +x duvarında M8 perçin somun (başı sağ duvarın Ø16,5 deliğinde gömülü) + 0,5 ara pul (derz) · cıvata TOPPING içinden"""
    R_ = G.PANEL["sag"]["yan"]; pr = G.PROF["a_kose_dikmesi_arka_sag"]; hp = S.DIN125["M8"][2]
    xk = X_SAG_DIS + 0.5 + 1.5                                           # TOPPING dis_yan_sol iç yüzü (1436 + 1,5)
    for y in M8_T_Y:
        et = "T_%d" % int(y)
        ps, c = S.percin_somun("M8", PT, (X_SAG_IC, y, Z_ARKA_D), (-1.0, 0, 0), ad="govde_m8_" + et, birim=G.birim)
        pr.duvar_delik("+x", y, 0.0, c["delik"], tip="m8_percin_somun", not_="A ↔ TOPPING M8 (gömme baş)")
        G.eleman(ps)
        R_.delik(Z_ARKA_D, y, 16.5, tip="percin_basi_yuvasi", parca="M8 perçin somun başı Ø15 × 1,5 (duvar kalınlığında gömülü)")
        ap = GO.halka((X_SAG_DIS, y, Z_ARKA_D), (1.0, 0, 0), 8.0, 4.6, 0.5)
        G.eleman(_ozel("govde_m8_ara_pul_" + et, ap, "özel (304 · lazer)", "Ara pul AISI 304 Ø16 / Ø9,2 × 0,5 (A ↔ TOPPING 0,5 derzi)", "Ø16 × 0,5", uretim=True, mal="sac"))
        G.arayuz(S.pul("DIN125", "M8", (xk, y, Z_ARKA_D), (1.0, 0, 0), ad="arayuz_m8_%s_pul" % et, birim=G.birim), "TOPPING_MODUL dis_yan_sol", "TOPPING sol yan sacında Ø9 (aynı eksen)", "")
        G.arayuz(S.vida("ISO4762", "M8", 20, (xk + hp, y, Z_ARKA_D), (-1.0, 0, 0), ad="arayuz_m8_" + et, birim=G.birim), "TOPPING_MODUL dis_yan_sol",
                 "ISO 4762 M8 × 20 A2-70 + DIN 125 · TOPPING kuru bölmesinden takılır", "")
        _karsi(et, "TOPPING_MODUL dis_yan_sol", "T", 9.0, 1.5, (-1.0, 0, 0), np.array([X_SAG_DIS + 0.5, y, Z_ARKA_D]), pr.ad, "TOPPING kuru bölmesi tarafından erişim")


def m8_b():
    """KAIDE → B: kaide profilinin içinden düşey M8 (kovan alt yüzle aynı, kaynak taşlanır) · baş kovanın üstünde, Ø16 servis deliğinden lokma · silikon tapa"""
    hp = S.DIN125["M8"][2]
    prof = {(757.5, "A"): "kaide_A_yan_profil_sol", (KA_ENINE_X, "A"): "kaide_A_enine_profil_0", (1416.0, "A"): "kaide_A_yan_profil_sag",
            (1456.0, "C"): "kaide_C_yan_profil_sol", (KC_ENINE_X, "C"): "kaide_C_enine_profil_2", (2480.0, "C"): "kaide_C_yan_profil_sag"}
    for k, liste in (("A", M8_B_A), ("C", M8_B_C)):
        for x, z in liste:
            on = "kaide_" + k; et = "B_%d_%d" % (int(x), int(-z))
            pr = G.PROF[prof[(x, k)]]
            pr.duvar_delik("+y", z, 0.0, 16.0, tip="lokma_gecisi", not_="kaide → B M8 · baş + lokma (üst duvar)")
            pr.duvar_delik("-y", z, 0.0, 12.2, tip="m8_kovan", not_="kovan (alt duvar · alt yüzle aynı, kaynak taşlanır)")
            kv = GO.halka((x, Y_DUZ, z), (0, 1.0, 0), 6.0, 4.5, KOVAN_UST - Y_DUZ)
            G.eleman(_ozel("%s_m8_%s_kovan" % (on, et), kv, "özel (304 boru Ø12 × 1,5)", "Kovan AISI 304 Ø12 × 1,5 · L %.0f (100'lük profil ezilmesin · alt yüzle aynı, kaynak taşlanır)"
                           % (KOVAN_UST - Y_DUZ), "Ø12/Ø9 × %.0f" % (KOVAN_UST - Y_DUZ), uretim=True, mal="sac"))
            G.PANEL[on + "_plaka"].delik(x, -z, 16.0, tip="servis_deligi", parca="kaide → B M8 lokma geçişi")
            if k == "A":
                G.PANEL["kaide_A_taban"].delik(x, -z, 16.0, tip="servis_deligi", parca="kaide → B M8 lokma geçişi · gıda sınıfı silikon tapa")
                if x > 1400.0:                                           # sağ alt kayıt bu noktanın üstünde → kayıttan da lokma geçişi
                    ak = G.PROF["a_sag_alt_kayit"]
                    ak.duvar_delik("-y", z, x - X_SAG, 16.0, tip="lokma_gecisi", not_="kaide → B M8 lokma geçişi"); ak.duvar_delik("+y", z, x - X_SAG, 16.0, tip="lokma_gecisi", not_="kaide → B M8 lokma geçişi")
                    _yer_tapa("kaide_A_m8_%s_tapa" % et, x, Y_ALT_KAYIT_SAG[1], z, t_sac=PT)
                else:
                    _yer_tapa("kaide_A_m8_%s_tapa" % et, x, Y_TABAN, z, t_sac=1.5)
            else:
                _karsi(et + "_servis", "TOPPING_MODUL dis_taban", "T", 16.0, 1.5, (0, -1.0, 0), np.array([x, Y_MEK, z]), pr.ad,
                       "kaide C → B cıvatasının lokma geçişi + gıda sınıfı silikon tapa (TOPPING tabanında)")
            G.arayuz(S.pul("DIN125", "M8", (x, KOVAN_UST, z), (0, 1.0, 0), ad="arayuz_m8_%s_%s_pul" % (k, et), birim=G.birim), "B_KASA tavan_dis_sac + B_AC_ust_kiris (h3_moduler_v1)", "", "")
            G.arayuz(S.vida("ISO4762", "M8", 110, (x, KOVAN_UST + hp, z), (0, -1.0, 0), ad="arayuz_m8_%s_%s" % (k, et), birim=G.birim), "B_KASA tavan_dis_sac + B_AC_ust_kiris (h3_moduler_v1)",
                     "B: tavan dış sacında Ø9 · B_AC üst kirişinin üst duvarında M8 perçin somun (PU köpüklemeden ÖNCE) · 3 mm PU boşluğuna Ø16 × 3 ara burç · ISO 4762 M8 × 110 + DIN 125",
                     "kaide servis deliğinden uzatmalı lokma")
            _karsi(et, "B_KASA tavan_dis_sac + B_AC_ust_kiris (perçin somun M8)", "B", 9.0, 1.5, (0, -1.0, 0), np.array([x, Y_DUZ, z]), pr.ad,
                   "B_AC kiriş hattı z %.0f (h3_moduler_v1.B_AC_Z_UYGULANAN · montaj v7: arka hat −747 → −706; hat yine kayarsa bu delik de kayar)" % z)


def m6_tc():
    """KAIDE_C ↔ TOPPING dis_taban: plaka (4) + profil üst duvarı (2) birlikte delinip M6 kılavuz · ISO 7380 M6 × 12 TOPPING içinden"""
    PL = G.PANEL["kaide_C_plaka"]
    for x, z in M6_TC:
        pr = G.PROF["kaide_C_on_profil" if z > -400.0 else "kaide_C_arka_profil"]
        et = "%d_%d" % (int(x), int(-z))
        PL.delik(x, -z, 5.0, tip="dis_M6", parca="M6 kılavuz (plaka 4 + profil üst duvarı 2 birlikte · 6 mm diş) · TOPPING dis_taban")
        pr.duvar_delik("+y", x, z - pr.c[1], 5.0, tip="dis_M6", not_="M6 kılavuz (plakayla birlikte)")
        G.arayuz(S.vida("ISO7380", "M6", 12, (x, Y_TABAN, z), (0, -1.0, 0), ad="arayuz_tc_m6_%s" % et, birim=G.birim), "TOPPING_MODUL dis_taban",
                 "dis_taban'da Ø6,6 (ISO 273 orta) · ISO 7380 M6 × 12 → kaide C plakası + profil üst duvarı M6 diş (6 mm, yalnız konum/devrilme · ağırlık plakaya oturur)", "TOPPING sahibi")
        _karsi("TC_M6_" + et, "TOPPING_MODUL dis_taban", "T", 6.6, 1.5, (0, -1.0, 0), np.array([x, Y_MEK, z]), pr.ad, "TOPPING tabanı → KAIDE_C (M6)")


# =====================================================================================================================================
# 7 · TEK ÖN KAPAK (v3.7 · çift cidar · robot ağzı penceresi · 3 gizli menteşe · 3 bas-aç · emniyet hedefi tutucusu)
# =====================================================================================================================================
def hedef(K):
    """emniyet hedefi (RST 36-1 · yeri DEĞİŞMEZ): iç tavadaki pencereden geçer · 1,5 L tutucuya 2 × M4 (gövdeden, x yönünde) · tutucu iç tavanın ARKASINA
    2 × ISO 7380 M4 + iç tavada PEM SP-M4 → kapak açıkken arkadan sökülür (dış yüzde iz yok)"""
    I = K.I
    x0, x1, y0, y1, z0, z1 = HEDEF
    I.dikdortgen((1371.0 + 1402.0) / 2.0, (1540.0 + 1648.0) / 2.0, 31.0, (1648.0 - 1540.0) + 4.0, tip="hedef_penceresi", parca="emniyet hedefi + tutucu ayağı geçişi (ayak boyu 108 + 2 × 2)")
    s = G.sac("onyuz_kapak_A_hedef_tutucu", "dis", doner=K); g_ = s.R + s.t
    ue = x0 - g_
    F = s.taban([(1350.0, 1540.0), (ue, 1540.0), (ue, 1648.0), (1350.0, 1648.0)], O=(0, 0, Z_ON - s.t), ex=(1, 0, 0), ey=(0, 1, 0), ad="flans")
    AY = F.flans(1, 19.5, yon=+1, ad="ayak")
    for y in (1560.0, 1628.0):
        b = S.vidali_birlesim(F, I, (1361.0, y, Z_ON - s.t), "pem_somun", dis="M4", ad="onyuz_kapak_A_hedef_tutucu_bag_%d" % int(y), birim=G.birim)
        for q in b["parcalar"]: G.eleman(q, doner=K)
        G.BIRLESIM.append(b)
    for y in (1560.0, 1628.0):
        q = AY.yerel((x0, y, 69.0))
        ps, c, ms = S.pem_somun("SP", "M4", (x0 - s.t, y, 69.0), (-1.0, 0, 0), s.t, ad="onyuz_kapak_A_hedef_pem_%d" % int(y), birim=G.birim)
        AY.delik(q[0], q[1], c["delik"], tip="pem_somun", parca=ps["meta"]["parca"], pem_tip="SP", kenar_min=c["kenar"], min_sac=ms)
        G.eleman(ps, doner=K)
        G.eleman(S.vida("ISO7380", "M4", 30, (x1, y, 69.0), (-1.0, 0, 0), ad="onyuz_kapak_A_hedef_vida_%d" % int(y), birim=G.birim), doner=K)
    sh = GO.kutu(x0, x1, y0, y1, z0, z1)
    for y in (1560.0, 1628.0): sh = sh.cut(GO.silindir((x0 - 1.0, y, 69.0), (1.0, 0, 0), 2.25, (x1 - x0) + 2.0))
    p = _ozel("onyuz_emniyet_hedefi", sh, "Schmersal RST 36-1", "Emniyet sensörü hedefi (kodlu RFID) · kapakla döner · 2 × M4 tutucuya (delik konumu VARSAYIM, föyden teyit)",
              "91 × 22 × 25 · yeri v3.6 ile aynı", malzeme="katalog", mal="siyah", tur="cihaz")
    G.eleman(p, doner=K)
    G.not_("emniyet hedefi: v3.6 konumu aynı (sensör Sao 10 · 0 mm) · iç tava penceresi 31 × %.1f · tutucu arkadan 2 × M4 → kapak sökülmeden değiştirilir" % ((y1 - y0) + 2.0))


def kapak():
    pu, pv = (PENCERE[0] + PENCERE[1]) / 2.0, (PENCERE[2] + PENCERE[3]) / 2.0
    K = GO.kapak(G, "onyuz_kapak_A", KAPAK_X[0], KAPAK_X[1], KAPAK_Y[0], KAPAK_Y[1], Z_KAPAK, Z_ON,
                 acikliklar=[dict(ad="pencere", u=pu, v=pv, boy=PENCERE[1] - PENCERE[0], en=PENCERE[3] - PENCERE[2], tip="pencere")])
    GO.gizli_mentese(G, K, G.PROF["onyuz_cerceve_sol_dikme"], "sol", MENTESE_Y)
    GO.bas_ac(G, K, G.PROF["onyuz_cerceve_sag_dikme"], "sag", BASAC_Y, a=BASAC_A)
    hedef(K)
    G.doner_guncelle()
    G.KAPAK_A = K
    return K


# =====================================================================================================================================
# 8 · KUR
# =====================================================================================================================================
def kur(log=print):
    global G
    if G is not None and getattr(G, "kuruldu", False): return G
    t0 = time.time()
    try:                                                                 # v3.7 kapak düzeni (h3_kapak_v1 · başka ajan koordinat düzeltiyor) ile eşitlik — yalnız OKUNUR
        import h3_kapak_v1 as KP
        assert (tuple(KP.A_X), tuple(KP.A_PEN), KP.Y_DUZ, KP.Y_TAVAN_KAPAK, KP.Z_ON) == (KAPAK_X, PENCERE, KAPAK_Y[0], KAPAK_Y[1], Z_KAPAK),             ("h3_kapak_v1 A ölçüleri değişmiş — KAPAK_X / PENCERE / KAPAK_Y güncellenmeli", KP.A_X, KP.A_PEN, KP.Y_DUZ, KP.Y_TAVAN_KAPAK, KP.Z_ON)
    except ImportError:
        log("UYARI: h3_kapak_v1 yok — v3.7 A ölçüleri sabitlerden (KAPAK_X %s · PENCERE %s)" % (KAPAK_X, PENCERE))
    G = GO.Govde(BIRIM, SURUM, istasyon="A", cerceve=CER)
    iskelet(); kaide_A(); kaide_C(); paneller(); kulaklar(); arka_baglantilari()
    m8_u(); m8_t(); m8_b(); m6_tc(); kapak()
    for s_ in G.SAC:
        if s_.ad == "a_govde_ust": _kalinlik_ek(s_)                    # dar çerçeve yüzü (kütüphane örnekleme sınırı · raporlandı)
    G.kuruldu = True
    log("%s · kuruldu: %d sac · %d profil · %d eleman · %d kaynak · %d birleşim · %d arayüz · %d M8/M6 noktası · %.1f sn"
        % (SURUM, len(G.SAC), len(G.PROF), len(G.ELEMAN), len(G.KAYNAK), len(G.BIRLESIM), len(G.ARAYUZ), len(G.M8), time.time() - t0))
    return G


# =====================================================================================================================================
# 9 · MONTAJ SÖZLEŞMESİ (AK.PARCALAR + KD.PARCALAR · DÜNYA · wp)
# =====================================================================================================================================
ISARET_A = "onyuz_kapak_A_ic_tava"
ISARET_KD = "kaide_A_m8_B_757_110_kovan"
BIRIMLER_A = [
    ("A_GOVDE", "A AÇICI kabini gövdesi · ÜRETİM SACI (h3_a_sac_v1): KAIDE_A ile tek kaynaklı alt montaj · 304 kare boru 30 × 30 × 2 iskelet (ön +27…+57, arka −815…−785) + "
                "ön alt bant 30 × 20 × 2 · sökülür paneller 1,5 (R 2,25 · K 0,45: sol yan ön 12 / arka 22, sağ duvar ray/tabla boğazlı, arka sac düz · FHP saplama (arkada baş yok), üst şerit 632 × 803 açıklıklı) + "
                "1,0 omega (CD saplama) · 3 mm kulak + PEM FHP-M5 · A ↔ U_A 6 × M8 · A ↔ TOPPING 2 × M8 · ışık perdesi + emniyet sensörü yerinde · x 736–1436 · y 788–1862"),
    ("A_ONYUZ", "A ön kapağı (v3.7 · 736–1434,5 × 788–2197): çift cidar 1,5 + 1,0 (dönüş 20 · köşeler bindirme + TIG) · robot ağzı penceresi 986–1186 × 960–1160 (kasa çıtalı) · "
                "3 gizli 180° kaldır-çıkar menteşe (sol ön dikme içinde · sanal pivot x 736 · z 79) · 3 bas-aç (sağ ön dikme) · emniyet hedefi arkadan sökülür · KULP YOK"),
]
BIRIMLER_KD = [
    ("KAIDE_A", "A mekanizma kaidesi 104 · ÜRETİM SACI (h3_a_sac_v1): 304 dikdörtgen boru 100 × 40 × 2 (dik) kaynaklı çerçeve + 4 mm plaka (delik kaynağı) + 1,5 taban sacı · "
                "x 737,5–1436 · y 788–893,5 · z −827…+37 · açıcı kolonu ankrajı 4 × M8 kaynak somunu · → B 4 × M8 (B_AC z −110 / −706 · kovanlı, servis deliği + tapa)"),
    ("KAIDE_C", "C (TOPPING) mekanizma kaidesi 104 · ÜRETİM SACI (h3_a_sac_v1): 100 × 40 × 2 çerçeve (6 mm dilim artığı enine KALKTI, göz 1 + 3 birleşik) + 4 mm plaka · "
                "x 1436–2500 · z −830…+35 · hava pencereleri (ön / boyuna / arka) + soğutma grubu cebi + atış ∪ ana besleme açıklığı · → B 2 × M8 (z −706) · TOPPING dis_taban 7 × M6"),
]


def _birim(ad):
    if ad.startswith("kaide_A"): return "KAIDE_A"
    if ad.startswith("kaide_C"): return "KAIDE_C"
    if ad.startswith("onyuz_kapak_A") or ad == "onyuz_emniyet_hedefi": return "A_ONYUZ"
    return "A_GOVDE"


def kapakla_doner(ad):
    kur()
    return G.kapakla_doner(ad)


def govde_parcalari():
    """montaja girecek parçalar (arayüz elemanları HARİÇ) · DÜNYA · birim A_GOVDE / A_ONYUZ / KAIDE_A / KAIDE_C · kapakla dönenler grup SERVIS_KAPAGI"""
    kur()
    L = GO.govde_parcalari(G)
    for q in L:
        q["birim"] = _birim(q["ad"])
        if G.kapakla_doner(q["ad"]): q["grup"] = "SERVIS_KAPAGI"
    return L


def uygula_ak(AK, rapor=None):
    """montaj (h3_acici_v1 = AK): eski A gövdesi + ön yüz (ESKI_A) çıkar, üretim sacı A gövdesi + tek kapak girer · idempotent · birim metinleri güncellenir"""
    L = AK.PARCALAR
    if any(p["ad"] == ISARET_A for p in L): return L
    L[:] = [p for p in L if p["ad"] != "a_govde_ust_omega"]                 # montaj v3.4 adımı (yoksa burada) · yeni üst şeritte omega yok
    yeni = [q for q in govde_parcalari() if q["birim"] in ("A_GOVDE", "A_ONYUZ")]
    GO.uygula(L, yeni, ESKI_A, ISARET_A, rapor=rapor, etiket="A")
    AK.BIRIMLER[:] = list(BIRIMLER_A)
    # gizli 180° menteşe → SANAL PIVOT (kapağın sol dış köşesi x 736 · z 79) · montajın v3.7 açılma taraması AK.MENTESE['pivot']'u okur
    AK.MENTESE = dict(AK.MENTESE, pivot=(PIVOT[0], PIVOT[2]))
    if hasattr(AK, "KAPAK_EKSEN"): AK.KAPAK_EKSEN = dict(AK.KAPAK_EKSEN, pivot=AK.MENTESE["pivot"], not_="h3_a_sac_v1: gizli 180° kaldır-çıkar menteşe · sanal pivot x 736 · z 79 (kapağın sol dış köşesi)")
    return L


def uygula_kd(KD, rapor=None):
    """montaj (h3_kaide_v1 = KD): eski kaide parçaları (ESKI_KD) çıkar, üretim sacı KAIDE_A + KAIDE_C girer (kaide_C_arka_emis_filtresi yerinde) · idempotent"""
    L = KD.PARCALAR
    if any(p["ad"] == ISARET_KD for p in L): return L
    yeni = [q for q in govde_parcalari() if q["birim"] in ("KAIDE_A", "KAIDE_C")]
    GO.uygula(L, yeni, ESKI_KD, ISARET_KD, rapor=rapor, etiket="KAIDE")
    KD.BIRIMLER[:] = list(BIRIMLER_KD)
    return L


def kapak_dunya(L=None):
    """A kapağıyla dönen bütün parçaların DÜNYA bileşiği (dış + iç tava, kasa çıtaları, kanat yarıları, karşılıklar, hedef + tutucu, kapaktaki PEM/vida, köşe kaynakları)"""
    L = L if L is not None else govde_parcalari()
    return GO.kapak_dunya(L, CER, kapakla_doner)


# =====================================================================================================================================
# 10 · ÖZ DENETİM + ÇIKTILAR (yalnız <scratchpad>/sac_a'ya yazar)
# =====================================================================================================================================
def _cikti_klasoru():
    S_ = os.environ.get("A_SAC_CIKTI") or os.path.abspath(os.path.join(H3, "..", "..", "..", "..", "sac_a"))
    os.makedirs(os.path.join(S_, "acinim"), exist_ok=True)
    return S_


if __name__ == "__main__":
    sys.path.insert(0, _cikti_klasoru())
    import a_sac_denetim_v1 as DEN                                            # <scratchpad>/sac_a/a_sac_denetim_v1.py (denetim + çıktı)
    DEN.calistir()
    sys.stdout.flush(); os._exit(0)
