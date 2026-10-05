# -*- coding: utf-8 -*-
"""h3_b_sac_v1 — B (ÇEKMECELİ SOĞUK DOLAP) GÖVDESİ · ÜRETİM SACI v1 (2 Eki 2026 · Claude · YEREL · TASLAK, montaja bağlı DEĞİL)

Kemal: "gövdede tam çalışma; büküm gerçek; sanayi mutfaklarında nasıl kuruluyorsa öyle; nereden bükülür, vida nereye atılır, boşluk nerede
açılır; vidasına kadar ama mantıklı; sanayi tipi mutfakçı 3B'den direkt üretsin." · pafta YOK, önce 3B (açınım JSON'ları ayrıca).

KAYNAKLAR: h3_sac_v1 (S) · h3_govde_ortak_v1 (GO, reçete) · sac_kararlar_v1.json > sac_standart_v1.json · B'nin mevcut gövdesi h3_store_v1 (+ store_cad_v14)
           + h3_moduler_v1'in B parçaları (alt şase, A/C taşıyıcı) · v3.7 ön yüz (h3_kapak_v1.bolge_B_sag: teknik sütun derzi 455) · h3/_elk (SC delikleri)
           · h3_elk_hat_v1 ana besleme kanalı (FA / RL / TS) · komşu M8 istekleri: h3_a_sac_v1 (kaide A/C → B) · h3_k_sac_v1 (K → B) · h3_e_sac_v1 (E ← B).
KOORDİNAT: B DÜNYADA (h3_store_v1.PARCALAR dünya) → Cerceve('B', 0, 0, 0). x hat boyunca 736…4400 · y yerden (alt 123, üst 788) · z ön +79 / arka −830.

KURGU (sanayi soğutmalı tezgâh mantığı · "tek atım köpüklü sandviç gövde + gömülü çelik çerçeve + köpükle yapışan ön çerçeve")
  0 · ALT ŞASE (dolabın kendi ayağı): 304 kare boru 40 × 40 × 2 kaynaklı merdiven (2 boyuna z −110 / −760 + 7 enine) y 83–123 · 14 hijyenik ayar ayağı
      GN 20 sınıfı M12 Ø60 (yerleri AYNI) boyunanın altına kaynaklı kör burca · "ayak_" öneki (montajın alt-taban denetimi ayak_ önekini dışarıda tutar).
  1 · GÖMÜLÜ TAŞIYICI ÇERÇEVE (B_TASIYICI · kaynaklı alt montaj, köpükten ÖNCE): 12 dikme 30 × 30 × 2 bölmelerin / sol duvarın PU'sunda · üst kirişler
      40 × 40 × 2 (ön boydan boya z −110 · A/C arka z −706 [moduler'in uyguladığı hat] x 740–2415 · fırın + teknik arka z −620) + 9 çapraz · kirişlerin
      üstünde 3 mm GFRP ısı kesici şerit · dikme altında 5 mm pabuç + 3 mm GFRP + M8 kaynak saplamaları alt şaseye.
      A/C arka kirişi x 2415'te biter: h3_elk_hat_v1 ana besleme kanalı (RL x 2421–2451 · FA z −761,5…−640,5) 2421'den sağa geçer (v3.6/3.7'de moduler kirişi
      bu kanalla çakışıyordu — montaj denetimi ELK ↔ MODULER bakmıyor).
  2 · DIŞ KABUK 1,5 (sıçrama/dış): sol / sağ yan (ön dönüş + arka iç flanş) · arka 2 parça · üst 2 parça · alt 2 parça (x 1500 ekleri ayakta flanş + kör perçin,
      köpük içinde) · köşe birleşimleri PEM FHP-M5 gömme saplama (dışta iz yok) + DIN 9021 + ISO 10511 içeriden (köpükten önce) · ≤ 150 aralık.
  3 · İÇ KABUK 1,2 (sıçrama): her kolon TEK PARÇA "U" (taban + arka + tavan, R 1,8 · tabanın ön kenarı 35 yukarı = eşik, tavanın ön kenarı köpüğe ya da
      (yer varsa) aşağı) · bölmeler 2 × 1,2 (ön kenar içe 15 dönüş) + PU 32,6 · sol duvar iç sacı · iç köşeler TIG + taşlama (sızdırmaz, köpük kalıbı).
      Raylar / motor braketi / sensör lamı → iç kabukta PEM SP somun (gövdesi köpük tarafında, köpükten önce kör başlıkla kapatılır).
  4 · ÖN ÇERÇEVE 430 1,0 (manyetik fitil yüzü, 2 parça, ek x 2091 B2 derzinin arkasında) · bölme / eşik / tavan / sol / ara kat ön dönüşlerine PEM FHP-M4
      (yüzde iz yok) + fiberli somun içeriden (köpükten ÖNCE) · çekmeceler arası kayıtlar (traversler) 1,2 L + ön bacak + 2 kulak (duvara SP-M4 + ISO 7380) ·
      çerçeve ↔ dış kabuk ön dönüşleri arası PVC ısı kesici çıtalar (köpük sızdırmaz).
  5 · FIRIN ALTI ISI KALKANI (ayırma 1,2 · ışınım 0,8 BA · 12 GFRP takoz + M4) · TEKNİK SÜTUN (ara kat sandviç · depo hücresi · sökülür depo arka paneli ·
      Secop rayları L 3 mm + uç plakaları · yarıklı servis paneli 1,5 tava · 4 gizli klips).
  6 · ÇEKMECELER (21 + depo): ön = dış tava 1,5 (köşe bindirme + TIG, geniş kenarda arka dönüş) + iç ada 1,0 (kanal iç duvarı) + PVC fitil taşıyıcı profil
      (ısı kesici) + PU + manyetik fitil (aynı) · kutu (GIDA) = 1,0 duvar halkası (4 büküm R 3, ek önde alın kaynağı) + 2,0 taban, iç köşeler TIG taşlanmış ·
      ön bağlantı U 2 mm (kutuya dıştan TIG, ön adadaki PEM SP-M5'e ISO 7380 · anahtar deliği) · ray adaptörü U 3 mm (kutuya dıştan TIG, ray iç elemanına M4).
  7 · KOMŞU BAĞLANTILARI M8: kaide A/C → B (kiriş üst duvarında M8 perçin somun · tavanda Ø9) · K → B (çapraz_2) · E ← B (sağ yanda Ø9) · B → E (GO.m8_noktasi).
ARAYÜZLER DEĞİŞMEZ: dış ölçü 736–4400 × 123–788 × −830…+79 · çekmece açıklıkları / önleri / yükseklikleri · ray / motor / kayış / sensör / evaporatör /
  Secop / pano / gider yerleri · 788 / 123 kotları · elektrik delik hedef adları (taban_dis_sac, tavan_dis_sac, bolme_4_*, isi_kalkani_sol_sac, tavan_pu_T).
Çalıştır (öz denetim + çıktılar <scratchpad>/sac_b): python -u <scratchpad>/sac_b/b_sac_denetim_v1.py"""
import math, os, sys, json, time, re, collections
H3 = os.path.dirname(os.path.abspath(__file__)); _U = os.path.dirname(H3)
for _p in (_U, H3):
    if _p not in sys.path: sys.path.insert(0, _p)
import numpy as np
import cadquery as cq
import h3_sac_v1 as S
import h3_govde_ortak_v1 as GO

SURUM = "h3_b_sac_v1"
V = cq.Vector
CER = GO.Cerceve("B", 0.0, 0.0, 0.0)                                   # B parçaları DÜNYADA (h3_store_v1)

# =====================================================================================================================================
# 0 · ARAYÜZ SABİTLERİ (h3_store_v1 / store_cad_v14 / h3_hesap_v1 değerleri · DEĞİŞMEZ)
# =====================================================================================================================================
X0, X1 = 736.0, 4400.0
Y_ALT, Y_UST = 123.0, 788.0
Z_ON0, Z_ON, Z_ARKA_DIS = 39.0, 79.0, -830.0
Y_TABAN, Y_TAVAN, Y_TAVAN_F = 164.5, 728.0, 668.0                       # iç kabuk soğuk yüzleri
Z_ARKA_IC = -790.0                                                     # iç kabuk arka soğuk yüzü
Z_CER0, Z_CER1, Z_CON0 = 23.0, 24.0, 24.0                              # ön çerçeve 430 · fitil teması
KOLON_AD = ("K1", "K2", "K3", "K5", "K6")
KOLON_X = {"K1": 798.5, "K2": 1453.5, "K3": 2108.5, "K5": 2763.5, "K6": 3418.5}
KOLON_W = {"K1": 620.0, "K2": 620.0, "K3": 620.0, "K5": 620.0, "K6": 575.0}
TAVAN_KOL = {"K1": 728.0, "K2": 728.0, "K3": 668.0, "K5": 668.0, "K6": 668.0}
BOLME_X = (1418.5, 2073.5, 2728.5, 3383.5, 3993.5)                     # 35'lik bölmelerin sol yüzleri
BOLME = 35.0
T0 = 4028.5                                                            # teknik sütunun sol yüzü
X_ALCAK = 2108.5
XF = (2500.0, 4000.0)
S0 = 433.5                                                             # teknik sütun ara katı alt
DEPO_ACIK = (4028.5, 4337.5, 463.5, 707.5)
X_DEPO_SAG = 4338.5
Z_ARA = (-494.0, 23.0)
Z_DEPO_ARKA = (-470.0, -440.0)
SERVIS_Y = (126.0, 453.5)                                              # v3.7 · teknik sütun derzi 455 (K6 ile tek çizgi)
DEPO_KAPAK_Y = (456.5, 785.0)
DEPO_FITIL_DY = 8.0                                                    # v3.7 (h3_kapak_v1.bolge_B_sag): depo fitili alt bacağı +8
KAPAK_X = {"K1": (736.0, 1434.5), "K2": (1437.5, 2089.5), "K3": (2092.5, 2744.5), "K5": (2747.5, 3399.5), "K6": (3402.5, 4009.5), "T": (4012.5, 4400.0)}
ON_ALT, ON_UST, BIND, FUGA = 126.0, 785.0, 15.0, 3.0
AYAK_X = (796.0, 1436.0, 2091.0, 2746.0, 3401.0, 4011.0, 4340.0)
AYAK_Z = (-110.0, -760.0)
ISINIM_Y = (740.0, 740.8)
ARKA_YARIK_Y = (748.0, 778.0)
ARKA_YARIK = [(2540.0 + 205.0 * i, 2725.0 + 205.0 * i) for i in range(7)]
TAKOZ_XZ = [(x, z) for x in (2650.0, 3050.0, 3350.0, 3700.0) for z in (-700.0, -250.0, 10.0)]
EMIS_T = [(4033.0, 4140.0, -700.0, -565.0), (4160.0, 4390.0, -695.0, -565.0)]     # Secop emişi (v36: elektrik ana besleme girişi + Harting soketi bu pencerelerden)
PANEL_YARIK = [(4042.0 + 170.0 * c, 4187.0 + 170.0 * c, 165.0 + 13.0 * r, 173.0 + 13.0 * r) for c in range(2) for r in range(20)]
HAVA_GECIS = {0: ((190.0, 290.0), (560.0, 660.0)), 1: ((190.0, 290.0), (560.0, 660.0)), 3: ((190.0, 290.0), (400.0, 490.0))}
HAVA_Z = (-788.0, -760.0)
DEPO_HAVA, DEPO_HAVA_Z = ((560.0, 620.0), (640.0, 700.0)), (-430.0, -380.0)
KAN_X, KAN_Z, KAN_UST, KAN_UST_F = (190.0, 230.0), (-790.0, -765.0), (703.0, 728.0), (643.0, 668.0)
RAY_SEC = {"arka": (-562.0, -522.0, -1), "on": (-136.0, -96.0, 1)}
GIDER_ANA = dict(x0=2023.5, y0=200.5, z=-738.0, egim=0.011, kilif_r=12.0)
ELK_FA = dict(x=(2421.0, 4141.5), y=(742.5, 785.5), z=(-761.5, -640.5))      # h3_elk_hat_v1 ana besleme kanalı (DIŞ) · fırın altı
ELK_RL = dict(x=(2421.0, 2451.0), y=(742.5, 1105.5), z=(-699.5, -558.5))     # C kaidesi yükselişi
ELK_TS = dict(x=(4098.5, 4141.5), y=(125.5, 785.5), z=(-701.5, -640.5))      # teknik sütun yükselişi
# çekmece mekanizması (store_cad_v14 · değişmez)
RAY_T, RAY_H, RAY_Y0, RAY_L, RAY_KISA = 12.7, 45.7, 4.0, 700.0, 2.0
KUTU_KENAR, KC, KUTU_TABAN_T, TUB_D = 30.0, 5.0, 2.0, 619.0
Z_TUB1 = Z_CON0 - 2.0                                                  # 22 · kutu ön dış yüzü
Z_TUB0 = Z_TUB1 - TUB_D                                                # −597
KX, KY, KOL_T, KOL_BOS, KOL_FLANS_Y, KOL_FL = 21.0, 30.0, 2.0, 1.0, 20.0, 12.0
SEN, SEN_X, SEN_Y0, LAM_TIRNAK, LAM_H = (28.57, 19.05, 6.35), (17.0, 23.35), 50.0, 16.0, 6.0
KAS_B, GOBEK_L = 11.0, 2.0
FITIL_G = 4.0
STROK = 700.0
CEK = [("K1", "CEK_K1_lahm_%d" % (i + 1), "lahm", 798.5, 200.5 + 108.0 * i) for i in range(5)] + \
      [("K2", "CEK_K2_lahm_%d" % (i + 1), "lahm", 1453.5, 200.5 + 108.0 * i) for i in range(5)] + \
      [("K3", "CEK_K3_hamur_%d" % (i + 1), "hamur", 2108.5, 200.5 + 108.0 * i) for i in range(4)] + \
      [("K5", "CEK_K5_hamur_%d" % (i + 1), "hamur", 2763.5, 200.5 + 108.0 * i) for i in range(3)] + [("K5", "CEK_K5_ic1_1", "ic1", 2763.5, 524.5)] + \
      [("K6", "CEK_K6_tatli_1", "tatli", 3418.5, 200.5), ("K6", "CEK_K6_ic1_1", "ic1", 3418.5, 308.5), ("K6", "CEK_K6_ic1_2", "ic1", 3418.5, 471.5)]
HH_C = {c[1]: 75.0 for c in CEK}; HH_C.update({"CEK_K5_ic1_1": 126.0, "CEK_K6_ic1_1": 130.0, "CEK_K6_ic1_2": 130.0})
ALT_KOD = {"CEK_K1_lahm_1", "CEK_K2_lahm_1", "CEK_K3_hamur_1", "CEK_K5_hamur_1", "CEK_K6_tatli_1"}
UST_KOD = {"CEK_K1_lahm_5", "CEK_K2_lahm_5", "CEK_K3_hamur_4", "CEK_K5_ic1_1", "CEK_K6_ic1_2"}
# depo çekmecesi (h3_store_v1._depo · store_cad_v14.k4_depo_cekmecesi)
DEPO_KUTU = dict(ka=4041.2, kb=4324.8, kc=466.5, kd=703.0, z0=-433.0, z1=22.0, sucuk_w=65.0)
DEPO_RAY_Z = (-427.0, 23.0)

# ---------------------------------------------------------------- ÜRETİM GEOMETRİSİ (bu dosyanın kararları)
X_EK = 1500.0                                                          # uzun dış sacların eki (üst · alt · arka): ≤ 3000 levha
PB, PB_S = 40.0, 30.0                                                  # 40 × 40 × 2 (şase, kiriş) · 30 × 30 × 2 (dikme · bölmeye sığan)
Y_SASE = (83.0, 123.0)
SASE_X = (740.0, 4396.0)
SASE_ENINE_X = (772.0, 1436.0, 2091.0, 2746.0, 3401.0, 4011.0, 4376.0)
Y_KIRIS = (743.5, 783.5)                                               # üst kirişler · üstünde 3 mm GFRP → 786,5 (üst sac altı)
GFRP_T = 3.0
Z_KIRIS_ON, Z_KIRIS_AC, Z_KIRIS_F = -110.0, -706.0, -620.0
X_KIRIS_ON = (740.0, 4396.0)
X_KIRIS_AC = (740.0, 2415.0)                                           # ana besleme kanalı RL x 2421'de başlar
X_KIRIS_F = (2502.5, 4396.0)
CAPRAZ = [("tasiyici_capraz_ac_772", 772.0, Z_KIRIS_AC + 20.0, Z_KIRIS_ON - 20.0), ("tasiyici_capraz_ac_1436", 1436.0, Z_KIRIS_AC + 20.0, Z_KIRIS_ON - 20.0),
          ("tasiyici_capraz_ac_2091", 2091.0, Z_KIRIS_AC + 20.0, Z_KIRIS_ON - 20.0), ("tasiyici_capraz_ac_uc", 2395.0, Z_KIRIS_AC + 20.0, Z_KIRIS_ON - 20.0),
          ("tasiyici_capraz_uc", 2522.5, Z_KIRIS_F + 20.0, Z_KIRIS_ON - 20.0), ("tasiyici_capraz_0", 2746.0, Z_KIRIS_F + 20.0, Z_KIRIS_ON - 20.0),
          ("tasiyici_capraz_1", 3401.0, Z_KIRIS_F + 20.0, Z_KIRIS_ON - 20.0), ("tasiyici_capraz_2", 4011.0, Z_KIRIS_F + 20.0, Z_KIRIS_ON - 20.0),
          ("tasiyici_capraz_sag", 4376.0, Z_KIRIS_F + 20.0, Z_KIRIS_ON - 20.0)]
DIKME = [("tasiyici_dikme_0", 2746.0, -110.0), ("tasiyici_dikme_1", 2746.0, -620.0), ("tasiyici_dikme_2", 3401.0, -110.0), ("tasiyici_dikme_3", 3401.0, -620.0),
         ("tasiyici_dikme_4", 4011.0, -110.0), ("tasiyici_dikme_5", 4011.0, -620.0),
         ("tasiyici_dikme_ac_772_on", 772.0, -110.0), ("tasiyici_dikme_ac_772_arka", 772.0, -706.0), ("tasiyici_dikme_ac_1436_on", 1436.0, -110.0),
         ("tasiyici_dikme_ac_1436_arka", 1436.0, -706.0), ("tasiyici_dikme_ac_2091_on", 2091.0, -110.0), ("tasiyici_dikme_ac_2091_arka", 2091.0, -706.0)]
Y_GFRP_ALT = (Y_ALT + 1.5, Y_ALT + 1.5 + GFRP_T)                        # 124,5–127,5
Y_PABUC = (Y_GFRP_ALT[1], Y_GFRP_ALT[1] + 5.0)                          # 127,5–132,5
T_IC = 1.2                                                             # iç kabuk (kararlar ic_panel_t)
Z_FL = Z_CER0 - T_IC                                                   # 21,8 · iç kabuk ön dönüşlerinin arka yüzü (ön yüz 23 = çerçeve arkası)
BIRIM = "B_KASA"
GOVDE_ONEK = ("ayak_", "kasa_", "tavan_", "taban_", "arka_", "yan_", "bolme_", "isi_kalkani_", "onyuz_", "tk_", "sogutma_grubu_montaj_rayi_",
              "tasiyici_", "ic_kabuk_", "govde_", "CEK_")
# komşu M8 istekleri (karşı tarafın dosyasından · B tarafı burada karşılanır)
M8_KAIDE = [("A", 757.5, -110.0), ("A", 757.5, -706.0), ("A", 1086.0, -706.0), ("A", 1416.0, -706.0),
            ("C", 1456.0, -706.0), ("C", 2120.0, -706.0)]                # h3_a_sac_v1 M8_B_A / M8_B_C (z −747 → −706: moduler'in UYGULADIĞI hat) · (2480, −747) karşılanamaz (açık)
M8_K = [(4016.5, -480.0), (4016.5, -570.0)]                             # h3_k_sac_v1 K→B (tasiyici_capraz_2 üst duvarı)
E_M8 = [(168.0, -700.0), (168.0, -590.0)]                              # h3_e_sac_v1 B_M8_Z · E tabanındaki DIN 929'a (y, z) · B sağ sacında Ø9
B_E_M8 = [-450.0, -250.0]                                              # B → E (capraz_sag dış duvarı · E sol sacında Ø9 ister)

S._RENK.update({"profil": ((0.70, 0.73, 0.77, 1.0), 0.85, 0.30), "mekanizma": ((0.42, 0.46, 0.52, 1.0), 0.4, 0.5), "arayuz": ((0.90, 0.22, 0.15, 1.0), 0.3, 0.5),
                "kapak": ((0.70, 0.82, 0.95, 1.0), 0.2, 0.25), "pu": ((0.93, 0.88, 0.72, 1.0), 0.0, 0.85), "gfrp": ((0.85, 0.80, 0.55, 1.0), 0.0, 0.6),
                "plastik": ((0.25, 0.27, 0.30, 1.0), 0.0, 0.7)})


def kutu(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), V(min(x0, x1), min(y0, y1), min(z0, z1)))


def silindir(p0, eksen, r, L):
    e = np.asarray(eksen, float); e = e / np.linalg.norm(e)
    return cq.Solid.makeCylinder(float(r), float(L), V(*map(float, p0)), V(*map(float, e)))


def y_ana(x):
    return GIDER_ANA["y0"] - GIDER_ANA["egim"] * (x - GIDER_ANA["x0"])


# =====================================================================================================================================
# 1 · KAYIT (birim / grup / malzeme parça başına) + yardımcılar
# =====================================================================================================================================
g = None                                                               # GO.Govde (kur() doldurur)


class K:
    """parça adı → montaj birimi / grubu / görünüm malzemesi · denetim yardımcı listeleri"""
    BIRIM, GRUP, MAL = {}, {}, {}
    PANEL = {}
    TAKIM = collections.OrderedDict()                                  # alt montaj → [ad]
    PU = collections.OrderedDict()                                     # PU adı → (kutu, birim, grup, bom)
    PU_KES = []                                                        # PU'dan ayrıca kesilecek katılar (gider kılıfı, elektrik delikleri) [(ad_deseni, katı)]
    ELK = {}                                                           # elektrik delik kesicileri (ad → [katı])
    kuruldu = False


def _kaydet(ad, birim, grup="SABIT", mal=None, takim=None):
    if ad in K.BIRIM: raise ValueError("çift ad: %s" % ad)
    K.BIRIM[ad] = birim; K.GRUP[ad] = grup
    if mal: K.MAL[ad] = mal
    if takim: K.TAKIM.setdefault(takim, []).append(ad)


def sac(ad, rol, birim=BIRIM, grup="SABIT", mal=None, kabuk=False, takim=None, **k):
    s = g.sac(ad, rol, kabuk=kabuk, **k)
    _kaydet(ad, birim, grup, mal or ("kabuk" if kabuk else "sac"), takim)
    s._b_birim, s._b_grup, s._b_mal = birim, grup, mal or ("kabuk" if kabuk else "sac")
    return s


def profil(ad, eksen, a0, a1, c, b=PB, t=2.0, birim="B_TASIYICI", takim=None, not_=""):
    p = g.profil(ad, eksen, a0, a1, c, b=b, t=t, not_=not_)
    _kaydet(ad, birim, "SABIT", "sac", takim)
    return p


def eleman(p, birim=BIRIM, grup="SABIT", mal=None, takim=None):
    g.eleman(p, mal=mal or "celik")
    _kaydet(p["ad"], birim, grup, mal or p.get("mal") or "celik", takim)
    return p


def kaynak(p, birim=BIRIM, grup="SABIT", takim=None):
    for q in (p if isinstance(p, (list, tuple)) else [p]):
        g.kaynak(q); _kaydet(q["ad"], birim, grup, "sac", takim)
    return p


def ozel(ad, sh, std, tanim, olcu, malzeme="AISI 304", mal="celik", uretim=False, tur="baglanti", meta=None, birim=BIRIM, grup="SABIT", takim=None):
    p = g.ozel(ad, sh, std, tanim, olcu, malzeme=malzeme, mal=mal, uretim=uretim, tur=tur, meta=meta)
    g.ELEMAN.append(p); p["birim"] = g.birim
    _kaydet(ad, birim, grup, mal, takim)
    return p


def birlesim(b, birim=BIRIM, grup="SABIT", takim=None):
    for q in b["parcalar"]: eleman(q, birim, grup, takim=takim)
    g.BIRLESIM.append(b)
    return b


def arayuz(p, karsi, gerek, not_=""):
    return g.arayuz(p, karsi, gerek, not_)


def kor_percin_birlesim(A, B, nokta, cap=4.8, ad="kor_percin", birim=None):
    """iki paralel sac arası kör perçin (ISO 15983) — h3_sac_v1.vidali_birlesim('kor_percin') dis=float'ta ISO 273 tablosuna bakıp KeyError veriyor
    (kütüphane hatası, raporlandı) → aynı dal burada: iki sacta Ø delik + perçin (baş A dış yüzünde)"""
    d, dis0, tA, b0, b1 = S._yigin(A, B, nokta)
    P = lambda x: dis0 + d * x
    ua = A.yerel(dis0); ub = B.yerel(P(b0 + 1e-9))
    for pan, uu in ((A, ua), (B, ub)):
        if not pan.icerir(uu[0], uu[1]): raise ValueError("birleşim noktası %s düz bölgesinde değil" % pan.ad)
    c = S.KOR_PERCIN[cap]
    A.delik(ua[0], ua[1], c["delik"], tip="kor_percin"); B.delik(ub[0], ub[1], c["delik"], tip="kor_percin")
    L = S._boy_sec(b1 + 1.5 * cap, [6, 8, 10, 12, 14, 16, 18, 20])
    pr = S.kor_percin(cap, L, tuple(P(0.0)), tuple(d), ad=ad + "_percin", birim=birim or g.birim, kavrama=b1)
    return dict(ad=ad, tip="kor_percin", dis=cap, parcalar=[pr], delikler=[], sac=[A.sac.ad, B.sac.ad], paket=round(b1, 4))


# ---------------------------------------------------------------- dünyaya hizalı levha (n: kalınlık yönü, c: dış yüz düzlemi)
_EKS = {"+x": ((0, 1, 0), (0, 0, 1)), "-x": ((0, 0, 1), (0, 1, 0)), "+y": ((0, 0, 1), (1, 0, 0)), "-y": ((1, 0, 0), (0, 0, 1)),
        "+z": ((1, 0, 0), (0, 1, 0)), "-z": ((0, 1, 0), (1, 0, 0))}
_IX = {"x": 0, "y": 1, "z": 2}


def levha(s, n, c, poly, ad="taban"):
    """poly: (u, v) DÜNYA koordinatları — u = ex ekseni, v = ey ekseni (_EKS) · c: levhanın n'e göre 'alt' yüzü (kalınlık c → c ± t, n yönünde)"""
    ex, ey = _EKS[n]
    O = [0.0, 0.0, 0.0]; O[_IX[n[1]]] = float(c)
    return s.taban([(float(a), float(b)) for a, b in poly], O=tuple(O), ex=ex, ey=ey, ad=ad)


def dikd(u0, u1, v0, v1):
    return [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]


def uv(P, p):
    q = P.yerel(np.asarray(p, float)); return float(q[0]), float(q[1])


def delik(P, p, cap, tip="delik", **m):
    u, v = uv(P, p); return P.delik(u, v, cap, tip=tip, **m)


def kesik_kutu(P, k, r=0.0, tip="kesik", dfm=True, **m):
    """dünya kutusunun (x0, x1, y0, y1, z0, z1) panel düzlemindeki izdüşümü → dikdörtgen kesik"""
    pts = [P.yerel(np.array([x, y, z], float)) for x in k[0:2] for y in k[2:4] for z in k[4:6]]
    us, vs = [q[0] for q in pts], [q[1] for q in pts]
    return P.dikdortgen((min(us) + max(us)) / 2.0, (min(vs) + max(vs)) / 2.0, max(us) - min(us), max(vs) - min(vs), r=r, tip=tip, dfm=dfm, **m)


def percin_somun(P, p, eksen, dis, ad, birim=BIRIM, grup="SABIT", kapali=True, takim=None, kavrama=None):
    """P sacının p noktasına (baş tarafı yüzü) perçin somun · eksen: kör tarafa (sacın içine doğru)"""
    t = kavrama if kavrama is not None else P.sac.t
    ps, c = S.percin_somun(dis, t, tuple(p), tuple(eksen), ad=ad, birim=g.birim, kapali=kapali)
    delik(P, p, c["delik"], tip="percin_somun", parca="perçin somun %s %s" % (dis, "kapalı uç" if kapali else ""))
    eleman(ps, birim, grup, takim=takim)
    return ps


def pem_somun(P, p_yuz, eksen, dis, ad, birim=BIRIM, grup="SABIT", takim=None, mal="celik", not_=""):
    """P sacına PEM SP somun: p_yuz = gövdenin oturduğu yüzde nokta (sacın UZAK yüzü) · eksen: gövdenin uzandığı yön (sacdan dışarı)"""
    ps, c, ms = S.pem_somun("SP", dis, tuple(p_yuz), tuple(eksen), P.sac.t, ad=ad, birim=g.birim)
    u, v = uv(P, p_yuz)
    P.delik(u, v, c["delik"], tip="pem_somun", parca=ps["meta"]["parca"] + (" · " + not_ if not_ else ""), pem_tip="SP", kenar_min=c["kenar"], min_sac=ms)
    eleman(ps, birim, grup, mal=mal, takim=takim)
    return ps


def tapa(pr, uc, birim, takim=None, t=2.0, pah=2.5):
    """profil ucuna b × b × t tapa (köşeler pahlı · çevresi TIG alın, taşlanır → kaynak katısı yok) — ucun DIŞINA oturur (boru boyu korunur)"""
    ex, ey = {"y": ((1.0, 0, 0), (0, 0, -1.0)), "x": ((0, 1.0, 0), (0, 0, 1.0)), "z": ((1.0, 0, 0), (0, 1.0, 0))}[pr.eksen]
    ex, ey = np.array(ex), np.array(ey)
    if uc == "alt":
        ey = -ey
        O = GO.EKSEN[pr.eksen] * pr.a0
    else:
        O = GO.EKSEN[pr.eksen] * pr.a1
    C = pr.merkez(pr.a0 if uc == "alt" else pr.a1)
    cu, cv = float(np.dot(C, ex)), float(np.dot(C, ey)); h = pr.b / 2.0; c = pah
    u0, u1, v0, v1 = cu - h, cu + h, cv - h, cv + h
    s = sac(pr.ad + ("_tapa" if uc == "ust" else "_tapa_alt"), "braket", birim=birim, mal="sac", takim=takim, t=t)
    s.taban([(u0 + c, v0), (u1 - c, v0), (u1, v0 + c), (u1, v1 - c), (u1 - c, v1), (u0 + c, v1), (u0, v1 - c), (u0, v0 + c)],
            O=tuple(O), ex=tuple(ex), ey=tuple(ey), ad="tapa")
    return s


def uc_kaynak(ad, nokta, yon, yuzler, b, birim="B_TASIYICI", takim=None, a=2.0):
    return kaynak(GO.uc_kaynaklari(ad, nokta, yon, yuzler, b=b, a=a, Ro=4.0, birim=g.birim), birim=birim, takim=takim)


def pu(ad, k, birim=BIRIM, grup="SABIT", bom=None, kes=None):
    """PU köpük dolgusu: kutu − (o hacmi kesen bütün gövde katıları) · kurulumun sonunda pu_kur() keser"""
    K.PU[ad] = dict(k=tuple(k), birim=birim, grup=grup, bom=bom, kes=kes)
    _kaydet(ad, birim, grup, "pu", "pu")


# =====================================================================================================================================
# 2 · ALT ŞASE + AYAKLAR (B_KASA · "ayak_" öneki) · GÖMÜLÜ TAŞIYICI ÇERÇEVE (B_TASIYICI)
# =====================================================================================================================================
def alt_sase():
    T = "alt_sase"
    yc = (Y_SASE[0] + Y_SASE[1]) / 2.0
    P = {}
    P["on"] = profil("ayak_sase_boyuna_on", "x", SASE_X[0], SASE_X[1], (yc, AYAK_Z[0]), birim=BIRIM, takim=T, not_="alt şase ön boyuna (ayak hattı z −110)")
    P["arka"] = profil("ayak_sase_boyuna_arka", "x", SASE_X[0], SASE_X[1], (yc, AYAK_Z[1]), birim=BIRIM, takim=T, not_="alt şase arka boyuna (ayak hattı z −760)")
    za, zb = AYAK_Z[1] + PB / 2.0, AYAK_Z[0] - PB / 2.0                      # −740 · −130
    for x in SASE_ENINE_X:
        P[x] = profil("ayak_sase_enine_%d" % int(x), "z", za, zb, (x, yc), birim=BIRIM, takim=T, not_="alt şase enine (boyunalara kaynaklı)")
        P["on"].kaynak_bolgesi("-z", x - PB / 2.0, x + PB / 2.0); P["arka"].kaynak_bolgesi("+z", x - PB / 2.0, x + PB / 2.0)
        for yz in ("+x", "-x"):
            P[x].kaynak_bolgesi(yz, za, za + 4.0); P[x].kaynak_bolgesi(yz, zb - 4.0, zb)
        yuz = [(1.0, 0, 0), (-1.0, 0, 0)]
        if x - PB / 2.0 <= SASE_X[0] + 1e-6: yuz = [(1.0, 0, 0)]
        if x + PB / 2.0 >= SASE_X[1] - 1e-6: yuz = [(-1.0, 0, 0)]
        uc_kaynak("ayak_sase_kaynak_%d_on" % int(x), (x, yc, zb), (0, 0, -1.0), yuz, PB, birim=BIRIM, takim=T)
        uc_kaynak("ayak_sase_kaynak_%d_arka" % int(x), (x, yc, za), (0, 0, 1.0), yuz, PB, birim=BIRIM, takim=T)
    for k in ("on", "arka"):
        tapa(P[k], "alt", BIRIM, T); tapa(P[k], "ust", BIRIM, T)
    K.SASE = P
    # ---- ayaklar: kör burç (boyunanın altına çevre kaynaklı, kapalı uç → boru sızdırmaz) + GN 20 sınıfı M12 Ø60 + kontra somun
    i = 0
    for x in AYAK_X:
        for z in AYAK_Z:
            pr = P["on"] if z == AYAK_Z[0] else P["arka"]
            b = S.kor_burc("M12", (x, Y_SASE[0], z), (0, -1.0, 0), D=30.0, H=30.0, ad="ayak_burcu_%d" % i, birim=g.birim)
            eleman(b, BIRIM, mal="celik", takim=T)
            kaynak(S.kaynak_halka((x, Y_SASE[0], z), (0, -1.0, 0), 15.0, 3.0, ad="ayak_burcu_%d_kaynagi" % i, birim=g.birim), BIRIM, takim=T)
            pr.kaynak_bolgesi("-y", x - 18.0, x + 18.0)
            for q in S.ayarli_ayak("M12", (x, 0.0, z), (0, 1.0, 0), Y_SASE[0] - 30.0, ise=20.0, D_taban=60.0, ad="ayak_%d" % i, birim=g.birim):
                eleman(q, BIRIM, mal="celik", takim="ayak")
            i += 1
    g.not_("alt şase 40 × 40 × 2 y 83–123 (gövde altı 83 açık · moduler v1 60 × 80 şase 43 bırakıyordu) · ayaklar GN 20 M12 Ø60 16 kN, yerleri v3.6 ile aynı (14)")
    return P


def _dikme_destek(x, z):
    """dikmenin altındaki şase elemanı + saplama doğrultusu"""
    if abs(z - AYAK_Z[0]) < 1e-6: return K.SASE["on"], (1.0, 0, 0)
    xs = min(SASE_ENINE_X, key=lambda q: abs(q - x))
    assert abs(xs - x) < 1e-6, ("dikme şase enine hattında değil", x, z)
    return K.SASE[xs], (0, 0, 1.0)


def _saplama_yerleri(x, z, sup, yon):
    """dikme saplamaları (şase elemanı boyunca): lokma deliği Ø16 alt duvarda burç kaynağına (± 18) ve boru ucuna değmesin · aralık ≥ 22 · yoksa tek saplama"""
    c0 = x if yon[0] else z
    burc = [ax for ax in AYAK_X] if sup.eksen == "x" else []
    def iyi(s):
        if not (sup.a0 + 8.0 + 3.0 <= s <= sup.a1 - 8.0 - 3.0): return False
        return all(abs(s - b) >= 18.0 + 8.0 + 3.0 + 0.1 for b in burc)
    aday = [c0 + d for d in range(-40, 41)]
    iyi_ = [s for s in aday if iyi(s)]
    cift = [(a, b) for a in iyi_ for b in iyi_ if b - a >= 22.0]
    if cift:
        a, b = min(cift, key=lambda q: (abs((q[0] + q[1]) / 2.0 - c0) + 0.01 * abs(q[1] - q[0] - 24.0)))
        return [a - c0, b - c0]
    assert iyi_, ("dikme saplaması yok", x, z)
    return [min(iyi_, key=lambda s: abs(s - c0)) - c0]


def tasiyici():
    """gömülü taşıyıcı çerçeve: dikmeler + kirişler + çaprazlar + GFRP + pabuç + saplamalar · kaynaklı alt montaj"""
    T = "tasiyici"
    B_ = "B_TASIYICI"
    yk = (Y_KIRIS[0] + Y_KIRIS[1]) / 2.0
    P = {}
    P["tasiyici_kiris_on"] = profil("tasiyici_kiris_on", "x", X_KIRIS_ON[0], X_KIRIS_ON[1], (yk, Z_KIRIS_ON), takim=T, not_="ön üst kiriş (A/C kaidesi + fırın + K yükü)")
    P["tasiyici_kiris_ac_arka"] = profil("tasiyici_kiris_ac_arka", "x", X_KIRIS_AC[0], X_KIRIS_AC[1], (yk, Z_KIRIS_AC), takim=T,
                                         not_="A/C arka üst kiriş (x 2415'te biter: ana besleme kanalı)")
    P["tasiyici_kiris_arka"] = profil("tasiyici_kiris_arka", "x", X_KIRIS_F[0], X_KIRIS_F[1], (yk, Z_KIRIS_F), takim=T, not_="fırın + teknik sütun arka üst kiriş")
    for ad, x, z0, z1 in CAPRAZ:
        P[ad] = profil(ad, "z", z0, z1, (x, yk), takim=T, not_="üst çapraz (kirişler arası)")
    for k in ("tasiyici_kiris_on", "tasiyici_kiris_ac_arka", "tasiyici_kiris_arka"):
        tapa(P[k], "alt", B_, T); tapa(P[k], "ust", B_, T)
    kir = {Z_KIRIS_ON: P["tasiyici_kiris_on"], Z_KIRIS_AC: P["tasiyici_kiris_ac_arka"], Z_KIRIS_F: P["tasiyici_kiris_arka"]}
    for ad, x, z0, z1 in CAPRAZ:
        for zu, yon, zk in ((z0, (0, 0, 1.0), z0 - PB / 2.0), (z1, (0, 0, -1.0), z1 + PB / 2.0)):
            kk = kir[zk]
            yuz = [(1.0, 0, 0), (-1.0, 0, 0)]
            if abs(x - PB / 2.0 - kk.a0) < 1e-6: yuz = [(1.0, 0, 0)]
            if abs(x + PB / 2.0 - kk.a1) < 1e-6: yuz = [(-1.0, 0, 0)]
            uc_kaynak("%s_kaynak_%s" % (ad, "arka" if zu == z0 else "on"), (x, yk, zu), yon, yuz, PB, takim=T)
            kk.kaynak_bolgesi("+z" if zk < zu else "-z", x - PB / 2.0, x + PB / 2.0)
            for yz in ("+x", "-x"):
                P[ad].kaynak_bolgesi(yz, zu, zu + 4.0) if zu == z0 else P[ad].kaynak_bolgesi(yz, zu - 4.0, zu)
    K.SAPLAMA = []; K.PABUC = {}
    for ad, x, z in DIKME:
        d = profil(ad, "y", Y_PABUC[1], Y_KIRIS[0], (x, z), b=PB_S, takim=T, not_="dikme 30 × 30 × 2 (bölme 35'e sığan · 40'lık standart SAPMA)")
        P[ad] = d
        zk = min(kir, key=lambda q: abs(q - z)); kk = kir[zk]
        assert abs(zk - z) <= PB / 2.0 - PB_S / 2.0 + 1e-6, ("dikme kirişin altında değil", ad, z, zk)
        assert kk.a0 + PB_S / 2.0 <= x <= kk.a1 - PB_S / 2.0, ("dikme kiriş boyunda değil", ad, x)
        kk.kaynak_bolgesi("-y", x - PB_S / 2.0 - 3.0, x + PB_S / 2.0 + 3.0)
        uc_kaynak(ad + "_kaynak_ust", (x, Y_KIRIS[0], z), (0, -1.0, 0), [(1.0, 0, 0), (-1.0, 0, 0), (0, 0, 1.0), (0, 0, -1.0)], PB_S, takim=T)
        for yz in ("+x", "-x", "+z", "-z"):
            d.kaynak_bolgesi(yz, Y_PABUC[1], Y_PABUC[1] + 4.0); d.kaynak_bolgesi(yz, Y_KIRIS[0] - 4.0, Y_KIRIS[0])
        sup, yon = _dikme_destek(x, z)
        offs = _saplama_yerleri(x, z, sup, yon)
        spl = [(x + yon[0] * o, z + yon[2] * o) for o in offs]
        xs_ = [p[0] for p in spl] + [x - PB_S / 2.0 - 3.0, x + PB_S / 2.0 + 3.0]; zs_ = [p[1] for p in spl] + [z - PB_S / 2.0 - 3.0, z + PB_S / 2.0 + 3.0]
        px0, px1 = min(min(xs_) - (8.0 if yon[0] else 0.0), x - PB / 2.0), max(max(xs_) + (8.0 if yon[0] else 0.0), x + PB / 2.0)
        pz0, pz1 = min(min(zs_) - (8.0 if yon[2] else 0.0), z - PB / 2.0), max(max(zs_) + (8.0 if yon[2] else 0.0), z + PB / 2.0)
        yuz_alt = [(1.0, 0, 0), (-1.0, 0, 0), (0, 0, 1.0), (0, 0, -1.0)]
        if x > T0 - 30.0:                                                # B5 sağ yüzü teknik sütun duvarına (4027,3) 1,3 mm → pabuç dikme hizasında biter, o yüz kaynaksız
            px1 = x + PB_S / 2.0; yuz_alt = [(-1.0, 0, 0), (0, 0, 1.0), (0, 0, -1.0)]
        if x < X0 + 60.0:                                                # sol duvar dikmesi: pabuç sol dış sacın iç yüzüne (737,5) taşmaz
            px0 = max(px0, X0 + 1.5 + 1.0)
        uc_kaynak(ad + "_kaynak_alt", (x, Y_PABUC[1], z), (0, 1.0, 0), yuz_alt, PB_S, takim=T)
        pb = sac(ad + "_pabuc", "braket", birim=B_, mal="sac", takim=T, t=5.0)
        pb.taban([(px0, -pz1), (px1, -pz1), (px1, -pz0), (px0, -pz0)], O=(0, Y_PABUC[0], 0), ex=(1, 0, 0), ey=(0, 0, -1.0), ad="pabuc")
        gf = kutu(px0, px1, Y_GFRP_ALT[0], Y_GFRP_ALT[1], pz0, pz1)
        for sx, sz in spl:
            gf = gf.cut(silindir((sx, Y_GFRP_ALT[0] - 1.0, sz), (0, 1.0, 0), 4.5, GFRP_T + 2.0))
        ozel(ad + "_gfrp", gf, "GFRP (G10 / FR4)", "Isı kesici plaka GFRP %.0f × %.0f × 3 · %d × Ø9" % (px1 - px0, pz1 - pz0, len(spl)), "%.0f × %.0f × 3" % (px1 - px0, pz1 - pz0),
             malzeme="GFRP", mal="koyu", uretim=True, tur="parca", birim=B_, takim=T)
        K.PABUC[ad] = (px0, px1, pz0, pz1)
        for j, (sx, sz) in enumerate(spl):
            e = "ab"[j]
            sp = silindir((sx, Y_PABUC[0], sz), (0, -1.0, 0), 3.96, 20.0)
            ozel("ayak_saplama_%s_%s" % (ad, e), sp, "ISO 13918 PD M8 × 20 A2", "Kaynak saplaması M8 × 20 (pabuç altına çekme ark kaynağı)", "M8 × 20",
                 malzeme="A2", mal="celik", birim=BIRIM, takim=T)
            y_ust = Y_SASE[1] - 2.0                                       # şase üst duvarının iç yüzü (121)
            eleman(S.pul("DIN125", "M8", (sx, y_ust, sz), (0, -1.0, 0), ad="ayak_saplama_%s_%s_pul" % (ad, e), birim=g.birim), BIRIM, takim=T)
            eleman(S.somun("ISO10511", "M8", (sx, y_ust - S.DIN125["M8"][2], sz), (0, -1.0, 0), ad="ayak_saplama_%s_%s_somun" % (ad, e), birim=g.birim), BIRIM, takim=T)
            sup.duvar_delik_nokta("+y", (sx, Y_SASE[1], sz), 9.0, tip="saplama_gecisi", not_="dikme %s saplaması" % ad)
            sup.duvar_delik_nokta("-y", (sx, Y_SASE[0], sz), 16.0, tip="lokma_deligi", not_="somun lokması (alttan)")
            K.SAPLAMA.append((sx, sz, ad))
    K.GFRP_SERIT = collections.OrderedDict(); K.GFRP_DELIK = collections.defaultdict(list)
    for ad, pr in P.items():
        if pr.eksen == "y": continue
        if pr.eksen == "x":
            k = (pr.a0, pr.a1, Y_KIRIS[1], Y_KIRIS[1] + GFRP_T, pr.c[1] - PB / 2.0, pr.c[1] + PB / 2.0)
        else:
            k = (pr.c[0] - PB / 2.0, pr.c[0] + PB / 2.0, Y_KIRIS[1], Y_KIRIS[1] + GFRP_T, pr.a0, pr.a1)
        K.GFRP_SERIT[ad] = k
    K.TAS = P
    g.not_("gömülü taşıyıcı çerçeve köpükten ÖNCE kaynaklı alt montaj olarak gövdeye girer · dikme 30 × 30 (bölme 35) SAPMA · GFRP üstte şerit, altta plaka · "
           "A/C arka hattı z −706 (h3_moduler_v1'in uyguladığı) · A/C arka kirişi x 2415'te biter (ana besleme kanalı RL/FA)")
    return P


def gfrp_seritleri():
    """üst GFRP şeritleri (perçin somun başı delikleri sonradan) → katı"""
    for ad, k in K.GFRP_SERIT.items():
        sh = kutu(*k)
        for (x, z, cap) in K.GFRP_DELIK.get(ad, []):
            sh = sh.cut(silindir((x, k[2] - 1.0, z), (0, 1.0, 0), cap / 2.0, GFRP_T + 2.0))
        ozel(ad + "_gfrp", sh, "GFRP (G10 / FR4)", "Isı kesici şerit GFRP 40 × 3 (üst sac ↔ çelik kiriş)", "%.0f × 40 × 3" % max(k[1] - k[0], k[5] - k[4]),
             malzeme="GFRP", mal="koyu", uretim=True, tur="parca", birim="B_TASIYICI", takim="tasiyici")


# =====================================================================================================================================
# 3 · DIŞ KABUK 1,5 (B_KASA) · ekler x 1500 · köşeler: üst / alt / arka sacların dönüşleri yan sacların İÇİNE, yan + üst + alt dönüşleri arka sacın İÇİNE
# =====================================================================================================================================
G15 = 2.25 + 1.5                                                       # R + t (1,5)
X_EK_A, X_EK_B = X_EK - 0.25, X_EK + 0.25                               # ek: iki flanşın dış yüzleri (0,5 derz)
Z_DONUS_ARKA = Z_ARKA_DIS + 1.5                                        # −828,5 · arka sacın iç yüzü = diğer sacların arka dönüş dış yüzü
Z_ON_DONUS = Z_ON0                                                     # +39 · ön dönüşlerin dış yüzü
X_YAN_IC = (X0 + 1.5, X1 - 1.5)                                        # 737,5 · 4398,5
Z_KIRIS_BOS = [(Z_KIRIS_AC - PB / 2.0 - 1.0, Z_KIRIS_AC + PB / 2.0 + 1.0), (Z_KIRIS_ON - PB / 2.0 - 1.0, Z_KIRIS_ON + PB / 2.0 + 1.0)]   # üst ek flanşı kirişlerde kesik


def _ek_segmentleri(v0, v1, bosluk):
    """[v0, v1] aralığını boşluklarla böler → [(a, b, flanşlı mı)]"""
    out, a = [], v0
    for b0, b1 in sorted(bosluk):
        if b1 <= v0 or b0 >= v1: continue
        if b0 > a: out.append((a, b0, True))
        out.append((max(a, b0), min(b1, v1), False)); a = min(b1, v1)
    if a < v1: out.append((a, v1, True))
    return out


def dis_kabuk():
    T = "dis_kabuk"
    g_ = G15
    # ---------------- SOL YAN (n +x) · ön dönüş 30 (x 766'ya) + arka iç flanş 21,5
    s = sac("kasa_yan_dis_sac_sol", "dis", kabuk=True, takim=T)
    P = levha(s, "+x", X0, [(Y_ALT, Z_DONUS_ARKA + g_), (Y_UST, Z_DONUS_ARKA + g_), (Y_UST, Z_ON_DONUS - g_), (Y_ALT, Z_ON_DONUS - g_)], ad="yan")
    Pa = P.flans(0, 21.5, yon=+1, bas=1.5, son=1.5, ad="arka_donus")
    Po = P.flans(2, 30.0, yon=+1, bas=1.5, son=1.5, ad="on_donus")
    K.PANEL["yan_sol"] = dict(s=s, yan=P, arka=Pa, on=Po)
    # ---------------- SAĞ YAN (n −x) · ön alt kenar Secop çıkışı için dönüşsüz (y < 463,5), üstte ön dönüş 30 (x 4370'e)
    s = sac("kasa_yan_dis_sac_sag", "dis", kabuk=True, takim=T)
    ya = DEPO_ACIK[2] - 1.5
    P = levha(s, "-x", X1, [(Z_DONUS_ARKA + g_, Y_ALT), (Z_ON_DONUS - g_, Y_ALT), (Z_ON_DONUS - g_, ya), (Z_ON_DONUS - g_, Y_UST), (Z_DONUS_ARKA + g_, Y_UST)], ad="yan")
    Po = P.flans(2, 30.0, yon=+1, bas=1.5, son=1.5, ad="on_donus")
    Pa = P.flans(4, 21.5, yon=+1, bas=1.5, son=1.5, ad="arka_donus")
    K.PANEL["yan_sag"] = dict(s=s, yan=P, arka=Pa, on=Po)
    # ---------------- ARKA (n +z) · 2 parça · ek x 1500 ayakta flanş (köpüğe) · üst/alt sacların arka dönüşleri ile çakışmasın diye ek flanşı y 145–766
    for ad, xa, xb, ek in (("arka_dis_sac_A", X0, X_EK_A - g_, "sag"), ("arka_dis_sac", X_EK_B + g_, X1, "sol")):
        s = sac(ad, "dis", kabuk=True, takim=T)
        P = levha(s, "+z", Z_ARKA_DIS, [(xa, Y_ALT), (xb, Y_ALT), (xb, Y_UST), (xa, Y_UST)], ad="arka")
        F = P.flans(1 if ek == "sag" else 3, 20.0, yon=+1, bas=22.0, son=22.0, ad="ek_flansi")
        if ad == "arka_dis_sac":
            for x0_, x1_ in ARKA_YARIK:
                kesik_kutu(P, (x0_, x1_, ARKA_YARIK_Y[0], ARKA_YARIK_Y[1], Z_ARKA_DIS - 1, Z_ARKA_DIS + 2), r=4.0, tip="havalandirma_yarigi",
                           parca="fırın altı hava boşluğu çıkışı (arkada · iç su kırıcı perde gerekmez: kuru bölge)")
        K.PANEL[ad] = dict(s=s, arka=P, ek=F)
    # ---------------- ÜST (n −y) · 2 parça · ön dönüş (A 60 · F 120 · teknik 60) · sol/sağ/arka iç flanş 20 · ek x 1500 kirişlerde kesik
    for ad, xa, xb, ek in (("tavan_dis_sac_A", X_YAN_IC[0] + g_, X_EK_A - g_, "sag"), ("tavan_dis_sac", X_EK_B + g_, X_YAN_IC[1] - g_, "sol")):
        s = sac(ad, "dis", takim=T)
        z0, z1 = Z_DONUS_ARKA + g_, Z_ON_DONUS - g_
        seg = _ek_segmentleri(z0, z1, Z_KIRIS_BOS)
        if ek == "sag":                                                 # poly (u = x, v = z) CCW · sağ kenar (ek) parçalı
            pts = [(xa, z0), (xb, z0)] + [(xb, b) for a, b, f in seg[:-1]] + [(xb, z1), (xa, z1)]
        else:
            pts = [(xa, z0), (xb, z0), (xb, z1), (xa, z1)] + [(xa, a) for a, b, f in reversed(seg[1:])]
        P = levha(s, "-y", Y_UST, pts, ad="ust")
        if ek == "sag":
            i_arka, i_ek0, i_on, i_uc = 0, 1, 1 + len(seg), 2 + len(seg)
        else:
            i_arka, i_on, i_uc, i_ek0 = 0, 2, 1, 3
        arka_bas = (758.0 - xa) if ek == "sag" else 0.0
        arka_son = 0.0 if ek == "sag" else (xb - 4378.0)
        Fa = P.flans(i_arka, 20.0, yon=+1, bas=arka_bas, son=arka_son, ad="arka_donus")
        Fu = P.flans(i_uc, 20.0, yon=+1, ad="uc_donus")                  # yan sacın içine (sol / sağ)
        if ek == "sag":
            Fo = P.flans(i_on, 60.0, yon=+1, bas=0.0, son=766.5 - xa, ad="on_donus")
        else:
            Fo = P.flans(i_on, 120.0, yon=+1, bas=xb - 4369.5, son=0.0, ad="on_donus")
            for x0_, x1_ in ((X_EK_B - 5.0, X_ALCAK), (T0, 4375.0)):
                kesik_kutu(Fo, (x0_, x1_, Y_TAVAN_F - 5.0, Y_TAVAN, Z_ON0 - 3.0, Z_ON0 + 1.0), r=3.0, tip="on_donus_kademe", dfm=False,
                           parca="ön dönüş derinliği 60 (A / teknik sütun) · 120 (fırın altı)")
        Fe = []
        for j, (a, b, f) in enumerate(seg):
            if not f: continue
            i_e = (i_ek0 + j) if ek == "sag" else (i_ek0 + (len(seg) - 1 - j))
            ra = 0.0 if abs(a - z0) < 1e-6 else 1.6                         # kiriş boşluğuna bakan uçta relief (kenar düz devam ediyor)
            rb = 0.0 if abs(b - z1) < 1e-6 else 1.6
            bas_, son_ = (ra, rb) if ek == "sag" else (rb, ra)
            Fe.append((a, b, P.flans(i_e, 20.0, yon=+1, bas=bas_, son=son_, ad="ek_flansi_%d" % j)))
        e_arka = min(Fe, key=lambda q: q[0])[2]; e_on = max(Fe, key=lambda q: q[1])[2]
        s.kose(Fa, e_arka, "acik"); s.kose(Fo, e_on, "acik")
        K.PANEL[ad] = dict(s=s, ust=P, arka=Fa, on=Fo, uc=Fu, ek=[q[2] for q in Fe])
    # ---------------- ALT (n +y) · 2 parça · ön dönüş 41,5 (x 766,5 … 4012) · sol/sağ/arka iç flanş 20 · ek x 1500 tam boy
    for ad, xa, xb, ek in (("taban_dis_sac_A", X_YAN_IC[0] + g_, X_EK_A - g_, "sag"), ("taban_dis_sac", X_EK_B + g_, X_YAN_IC[1] - g_, "sol")):
        s = sac(ad, "dis", takim=T)
        z0, z1 = Z_DONUS_ARKA + g_, Z_ON_DONUS - g_
        P = levha(s, "+y", Y_ALT, [(z0, xa), (z1, xa), (z1, xb), (z0, xb)], ad="alt")   # (u = z, v = x): 0 sol uç · 1 ön · 2 sağ uç · 3 arka
        Fo = P.flans(1, 41.5, yon=+1, bas=(766.5 - xa) if ek == "sag" else 0.0, son=0.0 if ek == "sag" else (xb - 4012.0), ad="on_donus")
        Fa = P.flans(3, 20.0, yon=+1, bas=0.0 if ek == "sag" else (xb - 4378.0), son=(758.0 - xa) if ek == "sag" else 0.0, ad="arka_donus")
        Fu = P.flans(0 if ek == "sag" else 2, 20.0, yon=+1, ad="uc_donus")
        Fe = P.flans(2 if ek == "sag" else 0, 20.0, yon=+1, ad="ek_flansi")
        s.kose(Fo, Fe, "acik"); s.kose(Fe, Fa, "acik") if ek == "sag" else s.kose(Fa, Fe, "acik")
        if ad == "taban_dis_sac":
            for x0_, x1_, z0_, z1_ in EMIS_T:
                kesik_kutu(P, (x0_, x1_, Y_ALT - 1, Y_ALT + 2, z0_, z1_), r=6.0, tip="emis_penceresi",
                           parca="Secop emiş penceresi (hava odası) · elektrik ana besleme girişi + Harting soketi bu pencerelerden geçer")
        K.PANEL[ad] = dict(s=s, alt=P, on=Fo, arka=Fa, uc=Fu, ek=Fe)


def dis_kabuk_baglanti():
    """yan ↔ üst/alt uç flanşları (yan sacta FHP-M5) · arka ↔ yan/üst/alt arka dönüşleri (arka sacta FHP-M5) · ekler (ayakta flanş, kör perçin Ø4,8)"""
    T = "dis_kabuk"
    zs = GO.vida_konumlari(-805.0, 15.0, maks=150.0, uc=0.0)
    for taraf, xd, ust, alt in (("yan_sol", X0, "tavan_dis_sac_A", "taban_dis_sac_A"), ("yan_sag", X1, "tavan_dis_sac", "taban_dis_sac")):
        A = K.PANEL[taraf]["yan"]
        for k, y in ((ust, 777.0), (alt, 134.0)):
            B = K.PANEL[k]["uc"]
            for z in zs:
                birlesim(S.vidali_birlesim(A, B, (xd, y, z), "pem_saplama", dis="M5", ad="govde_bag_%s_%s_%d" % (taraf, "ust" if k == ust else "alt", int(-z)),
                                           birim=g.birim), takim=T)
    ys = GO.vida_konumlari(150.0, 760.0, maks=150.0, uc=0.0)
    for taraf, xb, arka in (("yan_sol", 749.0, "arka_dis_sac_A"), ("yan_sag", 4387.5, "arka_dis_sac")):
        A = K.PANEL[arka]["arka"]; B = K.PANEL[taraf]["arka"]
        for y in ys:
            birlesim(S.vidali_birlesim(A, B, (xb, y, Z_ARKA_DIS), "pem_saplama", dis="M5", ad="govde_bag_arka_%s_%d" % (taraf, int(y)), birim=g.birim), takim=T)
    for arka, ust, alt, xr in (("arka_dis_sac_A", "tavan_dis_sac_A", "taban_dis_sac_A", (775.0, 1480.0)), ("arka_dis_sac", "tavan_dis_sac", "taban_dis_sac", (1520.0, 4365.0))):
        A = K.PANEL[arka]["arka"]
        for k, y in ((ust, 776.0), (alt, 135.0)):
            B = K.PANEL[k]["arka"]
            for x in GO.vida_konumlari(xr[0], xr[1], maks=150.0, uc=0.0):
                if k == ust and any(a0 - 8.0 < x < a1 + 8.0 for a0, a1 in ARKA_YARIK): continue        # fırın altı arka yarıkları (y 748–778) arasında kalır
                birlesim(S.vidali_birlesim(A, B, (x, y, Z_ARKA_DIS), "pem_saplama", dis="M5", ad="govde_bag_arka_%s_%d" % ("ust" if k == ust else "alt", int(x)),
                                           birim=g.birim), takim=T)
    A, B = K.PANEL["arka_dis_sac_A"]["ek"], K.PANEL["arka_dis_sac"]["ek"]
    for y in GO.vida_konumlari(160.0, 750.0, maks=150.0, uc=0.0):
        birlesim(kor_percin_birlesim(A, B, (X_EK_A, y, -818.0), 4.8, ad="govde_ek_arka_%d" % int(y)), takim=T)
    A, B = K.PANEL["taban_dis_sac_A"]["ek"], K.PANEL["taban_dis_sac"]["ek"]
    for z in GO.vida_konumlari(-800.0, 20.0, maks=150.0, uc=0.0):
        birlesim(kor_percin_birlesim(A, B, (X_EK_A, 135.0, z), 4.8, ad="govde_ek_alt_%d" % int(-z)), takim=T)
    Ua, Ub = K.PANEL["tavan_dis_sac_A"]["ek"], K.PANEL["tavan_dis_sac"]["ek"]
    seg = [(a, b) for a, b, f in _ek_segmentleri(Z_DONUS_ARKA + G15, Z_ON_DONUS - G15, Z_KIRIS_BOS) if f]
    assert len(seg) == len(Ua) == len(Ub), (len(seg), len(Ua), len(Ub))
    def _bul(L, p):
        for q in L:
            u_, v_ = uv(q, p)
            if q.icerir(u_, v_): return q
        raise AssertionError(("üst ek: flanş yok", p))
    for a, b in seg:
        for z in GO.vida_konumlari(a + 8.0, b - 8.0, maks=150.0, uc=0.0, min_adet=2 if b - a > 60 else 1):
            A = _bul(Ua, (X_EK_A - 0.75, 777.0, z)); B = _bul(Ub, (X_EK_B + 0.75, 777.0, z))
            birlesim(kor_percin_birlesim(A, B, (X_EK_A, 777.0, z), 4.8, ad="govde_ek_ust_%d" % int(-z)), takim=T)
    g.not_("dış kabuk köşeleri: dönüşler komşu sacın İÇİNDE · yan yüzlerde ve arkada PEM FHP-M5 gömme saplama (dışta yüzle aynı, iz yok) + DIN 9021 + ISO 10511 · "
           "ekler x 1500 ayakta flanş + kör perçin Ø4,8 (köpük içinde) · dikişler köpükten önce alüminyum bant + mastikle kapatılır (sızdırmaz kalıp)")


# =====================================================================================================================================
# 4 · İÇ KABUK 1,2 (sıçrama) · kolon U'ları · sol duvar iç sacı · bölmeler · fırın altı ısı kalkanı
# =====================================================================================================================================
R12 = 1.8                                                              # 1,2 sac iç R (1,5t)
G12 = R12 + T_IC                                                       # 3,0


def _cek_kolon(k):
    return sorted([c for c in CEK if c[0] == k], key=lambda c: c[4])


def _ust_y1(k):
    c = _cek_kolon(k)[-1]
    return c[4] + HH_C[c[1]]


def _tavan_asagi(k):
    """tavan ön dönüşü kolon içine (aşağı) inebilir mi: en üst çekmece açıklığının üstünde ≥ 35 boşluk (avara kolu ön flanşı y1 + 21'e kadar)"""
    return TAVAN_KOL[k] - _ust_y1(k) >= 35.0


def ic_kabuk():
    T = "ic_kabuk"
    K.DUVAR = {}                                                       # (kolon, 'sol'|'sag') → (Panel, x yüzü, köpük yönü işareti)
    K.CER_DESTEK = []                                                  # ön çerçeve saplamalarının oturacağı dönüşler: (Panel, [(x, y)], somun_std, etiket)
    # ---------------- kolon U'ları (taban + arka + tavan · tabanın önü 35 yukarı eşik · tavanın önü köpüğe ya da aşağı)
    for k in KOLON_AD:
        x0 = KOLON_X[k]; x1 = x0 + KOLON_W[k]; yt = TAVAN_KOL[k]
        yb_d, yt_d = Y_TABAN - T_IC, yt + T_IC                           # taban alt yüzü 163,3 · tavan üst yüzü
        s = sac("ic_kabuk_%s" % k, "ic", takim=T, t=T_IC)
        c = Z_ARKA_IC - T_IC                                           # −791,2 (arka levhanın köpük yüzü)
        P = levha(s, "+z", c, dikd(x0, x1, yb_d + G12, yt_d - G12), ad="arka")
        boy = Z_CER0 - c                                               # 814,2 → ön yüz z 23 (çerçeve arkası)
        Ft = P.flans(0, boy, yon=+1, ad="taban")                        # tanım sırası = abkant sırası (taban · eşik · tavan · tavan önü: DFM'in çarpmasız sırası)
        Fe = Ft.flans(1, 35.0, yon=+1, ad="esik")                       # eşik: 163,3 → 198,3 (en alt çekmece açıklığı 200,5)
        Fc = P.flans(2, boy, yon=+1, ad="tavan")
        if _tavan_asagi(k):
            ya = _ust_y1(k) + 27.5                                     # avara kolu ön flanşının (y1 + 21) 6,5 üstü
            Fo = Fc.flans(1, yt_d - ya, yon=+1, ad="tavan_on")
            K.CER_DESTEK.append((Fo, [(x, (ya + yt) / 2.0) for x in GO.vida_konumlari(x0 + 40.0, x1 - 40.0, maks=200.0, uc=0.0)], "DIN1587", "%s_tavan" % k))
        else:
            Fo = Fc.flans(1, 25.0, yon=-1, ad="tavan_on")              # köpüğe (yukarı)
            K.CER_DESTEK.append((Fo, [(x, yt + 12.0) for x in GO.vida_konumlari(x0 + 40.0, x1 - 40.0, maks=200.0, uc=0.0)], "ISO10511", "%s_tavan" % k))
        K.CER_DESTEK.append((Fe, [(x, 184.0) for x in GO.vida_konumlari(x0 + 40.0, x1 - 40.0, maks=200.0, uc=0.0)], "DIN1587", "%s_esik" % k))
        K.PANEL["ic_kabuk_" + k] = dict(s=s, arka=P, taban=Ft, tavan=Fc, esik=Fe, tavan_on=Fo)
    # ---------------- sol duvar iç sacı (K1 sol duvarı · ön dönüş köpüğe 25)
    s = sac("yan_ic_sac_sol", "ic", takim=T, t=T_IC)
    x0 = KOLON_X["K1"]
    P = levha(s, "+x", x0 - T_IC, [(Y_TABAN, Z_ARKA_IC), (Y_TAVAN, Z_ARKA_IC), (Y_TAVAN, Z_CER0 - G12), (Y_TABAN, Z_CER0 - G12)], ad="yan")
    Fo = P.flans(2, 25.0, yon=-1, ad="on_donus")
    K.PANEL["yan_ic_sac_sol"] = dict(s=s, yan=P, on=Fo)
    K.DUVAR[("K1", "sol")] = (P, x0, -1.0)
    K.CER_DESTEK.append((Fo, [(x0 - 12.5, y) for y in GO.vida_konumlari(185.0, 715.0, maks=200.0, uc=0.0)], "ISO10511", "sol"))
    # ---------------- bölmeler: 2 × 1,2 (ön kenar içe 15) + PU 32,6 · geçişler: kablo kanalı (üst-arka) · hava (arka) · gider kılıfı · elektrik (B5)
    kol_sol = ("K1", "K2", "K3", "K5", "K6"); kol_sag = ("K2", "K3", "K5", "K6", "T")
    for i, b0 in enumerate(BOLME_X):
        b1 = b0 + BOLME
        ust_a = 786.5 if i == 4 else TAVAN_KOL[kol_sol[i]]
        ust_b = 786.5 if i == 4 else TAVAN_KOL[kol_sag[i]]
        alt_b = Y_ALT + 1.5 if i == 4 else Y_TABAN
        arka_b = Z_DONUS_ARKA if i == 4 else Z_ARKA_IC
        sa = sac("bolme_%d_sac_a" % i, "ic", takim="bolme", t=T_IC)
        Pa = levha(sa, "+x", b0, [(Y_TABAN, Z_ARKA_IC), (ust_a, Z_ARKA_IC), (ust_a, Z_CER0 - G12), (Y_TABAN, Z_CER0 - G12)], ad="bolme")
        Fa = Pa.flans(2, 15.0, yon=+1, ad="on_donus")
        sb = sac("bolme_%d_sac_b" % i, "ic", takim="bolme", t=T_IC)
        Pb = levha(sb, "-x", b1, [(arka_b, alt_b), (Z_CER0 - G12, alt_b), (Z_CER0 - G12, ust_b), (arka_b, ust_b)], ad="bolme")
        Fb = Pb.flans(1, 15.0, yon=+1, ad="on_donus")
        K.PANEL["bolme_%d" % i] = dict(a=Pa, b=Pb, a_on=Fa, b_on=Fb, sa=sa, sb=sb)
        K.DUVAR[(kol_sol[i], "sag")] = (Pa, b0, +1.0)
        K.DUVAR[(kol_sag[i], "sol")] = (Pb, b1, -1.0)
        ya_ust = min(ust_a, ust_b) if i < 4 else Y_TAVAN
        K.CER_DESTEK.append((Fa, [(b0 + 8.5, y) for y in GO.vida_konumlari(185.0, min(ya_ust, 700.0) - 15.0, maks=200.0, uc=0.0)], "ISO10511", "b%d_a" % i))
        yb_ust = ust_b if i < 4 else 700.0
        yb_alt = 185.0 if i < 4 else 445.0                              # B5 teknik tarafı: Secop bölmesinin önü açık (servis paneli) · çerçeve 431'den yukarı
        K.CER_DESTEK.append((Fb, [(b1 - 8.5, y) for y in GO.vida_konumlari(yb_alt, min(yb_ust, 700.0) - 15.0, maks=200.0, uc=0.0)], "ISO10511", "b%d_b" % i))
        # geçişler (iki sacta hizalı · PU'da aynı kutu)
        gec = []
        ku = KAN_UST if i == 0 else KAN_UST_F
        gec.append(("kablo_gecisi", (b0 - 1.0, b1 + 1.0, ku[0], (KAN_UST[1] if i == 1 else ku[1]) + 1.0, Z_ARKA_IC - 2.0, KAN_Z[1]), False))
        for y0_, y1_ in HAVA_GECIS.get(i, ()):
            gec.append(("hava_gecisi", (b0 - 1.0, b1 + 1.0, y0_, y1_, Z_ARKA_IC - 2.0, HAVA_Z[1]), False))
        if i == 4:
            for y0_, y1_ in DEPO_HAVA:
                gec.append(("depo_hava_gecisi", (b0 - 1.0, b1 + 1.0, y0_, y1_, DEPO_HAVA_Z[0], DEPO_HAVA_Z[1]), True))
        for ad_, kk, ic in gec:
            for Pq, kenar_alt in ((Pa, True), (Pb, True)):
                yk = kk
                if not ic and Pq is Pb and i == 4: yk = (kk[0], kk[1], kk[2], kk[3], Z_DONUS_ARKA - 1.0, kk[5])     # B5 b sacı arka −828,5'e kadar
                kesik_kutu(Pq, yk, r=0.0 if not ic else 3.0, tip=ad_, dfm=ic, parca="bölme %s (%s)" % (ad_, "iç delik" if ic else "arka kenara açık çentik"))
            K.PU_KES.append(("bolme_%d_pu" % i, kutu(*kk)))
        if i >= 1:                                                      # gider ana hattı Ø24 kılıfı (store: bölme PU'sunda) → iki sacta Ø25
            for Pq, xs, alt_ in ((Pa, b0, Y_TABAN), (Pb, b1, Y_TABAN if i < 4 else Y_ALT + 1.5)):
                yg = y_ana(xs)
                if yg - 12.5 - alt_ < 3.0 + 0.5:                            # B5 a sacı: kılıf iç kabuk tabanının hemen üstünde → alt kenara açık çentik
                    kesik_kutu(Pq, (xs - 1.0, xs + 2.0, alt_ - 1.0, yg + 12.5, GIDER_ANA["z"] - 12.5, GIDER_ANA["z"] + 12.5), r=0.0, tip="gider_gecisi", dfm=False,
                               parca="gider ana hattı kılıfı Ø24 geçişi (alt kenara açık çentik · kılıf çevresine silikon)")
                else:
                    delik(Pq, (xs, yg, GIDER_ANA["z"]), 25.0, tip="gider_gecisi", parca="gider ana hattı kılıfı Ø24 geçişi")
            d = np.array([1.0, -GIDER_ANA["egim"], 0.0])
            K.PU_KES.append(("bolme_%d_pu" % i, silindir((b0 - 1.0, y_ana(b0 - 1.0), GIDER_ANA["z"]), d, 12.5, BOLME + 2.0)))
        if i == 4:                                                      # elektrik ana besleme (h3_elk_hat_v1 FA) B5'ten geçer: y 742,5–785,5 · z −761,5…−640,5
            ek = (b0 - 1.0, b1 + 1.0, ELK_FA["y"][0] - 1.5, 787.5, ELK_FA["z"][0] - 1.5, ELK_FA["z"][1] + 1.5)
            for Pq in (Pa, Pb):
                kesik_kutu(Pq, ek, tip="elektrik_gecisi", dfm=False, parca="ana besleme kanalı geçişi (üst kenara açık) · kanalın çevresine silikon")
            K.PU_KES.append(("bolme_4_pu", kutu(*ek)))
        z_on = Z_FL
        pu("bolme_%d_pu" % i, (b0 + T_IC, b1 - T_IC, Y_TABAN if i < 4 else Y_ALT + 1.5, (max(ust_a, ust_b) if i < 4 else 786.5), (Z_ARKA_IC if i < 4 else Z_DONUS_ARKA), z_on),
           bom=("PU köpük (yerinde enjeksiyon, 40 kg/m³) · bölme %d" % (i + 1), 1, "32,6 kalın", "bölme sacları + gövdeyle tek atım"))
    # ---------------- fırın altı ısı kalkanı: ayırma 1,2 (728 · ön/arka kenar köpüğe 20) · sol sac 1,2 (x 2500) · ışınım sacı 0,8 BA (740) · 12 GFRP takoz + M4
    xa0, xa1 = XF[0] + T_IC, BOLME_X[4]                                # 2501,2 … 3993,5
    s = sac("isi_kalkani_ayirma_saci", "ic", takim="isi_kalkani", t=T_IC)
    P = levha(s, "+y", Y_TAVAN, [(Z_DONUS_ARKA + G12, xa0), (Z_ON0 - 1.5 - G12, xa0), (Z_ON0 - 1.5 - G12, xa1), (Z_DONUS_ARKA + G12, xa1)], ad="ayirma")
    Fon = P.flans(1, 20.0, yon=-1, ad="on_donus"); Far = P.flans(3, 20.0, yon=-1, ad="arka_donus")
    DIK = [(x, z) for _a, x, z in DIKME if xa0 < x < xa1]
    for x, z in DIK:
        kesik_kutu(P, (x - 17.0, x + 17.0, Y_TAVAN - 1, Y_TAVAN + 2, z - 17.0, z + 17.0), r=3.0, tip="dikme_gecisi", parca="taşıyıcı dikme geçişi 34 × 34 · silikon")
    K.PANEL["isi_kalkani_ayirma_saci"] = dict(s=s, P=P)
    s = sac("isi_kalkani_sol_sac", "ic", takim="isi_kalkani", t=T_IC)
    P = levha(s, "+x", XF[0], [(Y_TAVAN_F + T_IC, Z_DONUS_ARKA), (786.5, Z_DONUS_ARKA), (786.5, Z_ON0 - 1.5), (Y_TAVAN_F + T_IC, Z_ON0 - 1.5)], ad="sol")
    for z0_, z1_, ad_ in ((Z_KIRIS_ON - PB / 2.0 - 1.0, Z_KIRIS_ON + PB / 2.0 + 1.0, "kiris_on"), (ELK_FA["z"][0] - 1.5, ELK_FA["z"][1] + 1.5, "elektrik")):
        y0_ = Y_KIRIS[0] - 1.0 if ad_ == "kiris_on" else ELK_FA["y"][0] - 1.5
        kesik_kutu(P, (XF[0] - 1, XF[0] + 2, y0_, 787.5, z0_, z1_), tip="cent_" + ad_, dfm=False,
                   parca="üst kenara açık çentik (%s)" % ("ön kiriş + GFRP" if ad_ == "kiris_on" else "ana besleme kanalı FA"))
    K.PANEL["isi_kalkani_sol_sac"] = dict(s=s, P=P)
    s = sac("isi_kalkani_isinim_saci", "ic", takim="isi_kalkani", t=0.8, malzeme="AISI 304 BA (parlak tavlı)")
    P = levha(s, "+y", ISINIM_Y[0], dikd(-826.5, 35.5, XF[0] + 2.0, BOLME_X[4] - 1.0), ad="isinim")
    for x, z in DIK:
        kesik_kutu(P, (x - 17.0, x + 17.0, ISINIM_Y[0] - 1, ISINIM_Y[1] + 1, z - 17.0, z + 17.0), r=3.0, tip="dikme_gecisi", parca="dikme geçişi")
    K.PANEL["isi_kalkani_isinim_saci"] = dict(s=s, P=P)
    Pa_ = K.PANEL["isi_kalkani_ayirma_saci"]["P"]
    for i, (tx, tz) in enumerate(TAKOZ_XZ):
        tk = kutu(tx - 10.0, tx + 10.0, Y_TAVAN + T_IC, ISINIM_Y[0], tz - 10.0, tz + 10.0).cut(silindir((tx, Y_TAVAN, tz), (0, 1, 0), 2.25, 15.0))
        ozel("isi_kalkani_takozu_%d" % i, tk, "GFRP (G10)", "Isı köprüsü kesici takoz GFRP 20 × 20 × %.1f · Ø4,5" % (ISINIM_Y[0] - Y_TAVAN - T_IC), "20 × 20",
             malzeme="GFRP", mal="koyu", uretim=True, tur="parca", takim="isi_kalkani")
        pem_somun(Pa_, (tx, Y_TAVAN, tz), (0, -1.0, 0), "M4", "isi_kalkani_takozu_%d_pem" % i, takim="isi_kalkani", not_="takoz cıvatası")
        delik(K.PANEL["isi_kalkani_isinim_saci"]["P"], (tx, ISINIM_Y[0], tz), 4.5, tip="vida_deligi", parca="M4 takoz cıvatası")
        eleman(S.vida("ISO7380", "M4", 16, (tx, ISINIM_Y[1], tz), (0, -1.0, 0), ad="isi_kalkani_takozu_%d_vida" % i, birim=g.birim), takim="isi_kalkani")
    g.not_("iç kabuk 1,2 (sıçrama · soğuk dolap içi): her kolon TEK PARÇA U (taban + arka + tavan, R 1,8) · tabanın önü 35 yukarı EŞİK (çerçevenin altını taşır, "
           "su dolaba kalır) · iç kabuk ↔ bölme sacı köşeleri TIG + taşlama (köpük kalıbı sızdırmaz) · dikişler katı olarak çizilmedi (kaynak listesinde boyla)")


# =====================================================================================================================================
# 5 · ÖN ÇERÇEVE 430 1,0 (2 parça) · kayıtlar (traversler) · PVC ısı kesiciler · çerçeve saplamaları
# =====================================================================================================================================
CER_EK = 2091.0                                                        # B2 bölmesinin ortası (K2 | K3 derzinin arkası)
CER_A = [(770.0, 150.0), (CER_EK - 0.25, 150.0), (CER_EK - 0.25, 750.0), (770.0, 750.0)]
CER_F = [(CER_EK + 0.25, 150.0), (4026.0, 150.0), (4026.0, 431.0), (4370.0, 431.0), (4370.0, 750.0), (4012.0, 750.0), (4012.0, 682.0), (2112.0, 682.0), (2112.0, 750.0),
         (CER_EK + 0.25, 750.0)]


def _acikliklar():
    out = [(c[3], c[3] + KOLON_W[c[0]], c[4], c[4] + HH_C[c[1]], c[1]) for c in CEK]
    out.append((DEPO_ACIK[0], DEPO_ACIK[1], DEPO_ACIK[2], DEPO_ACIK[3], "depo"))
    return out


def _icinde_poly(poly, x, y):
    ic = False
    for i in range(len(poly)):
        (x0, y0), (x1, y1) = poly[i], poly[(i + 1) % len(poly)]
        if (y0 > y) != (y1 > y) and x < (x1 - x0) * (y - y0) / (y1 - y0) + x0: ic = not ic
    return ic


def _kenar_mesafe(poly, x, y):
    d = 1e9
    for i in range(len(poly)):
        p0, p1 = np.array(poly[i]), np.array(poly[(i + 1) % len(poly)])
        e = p1 - p0; L = np.linalg.norm(e); t = max(0.0, min(1.0, np.dot(np.array([x, y]) - p0, e) / L / L))
        d = min(d, float(np.linalg.norm(np.array([x, y]) - (p0 + e * t))))
    return d


def on_cerceve():
    T = "on_cerceve"
    K.CER = {}
    for ad, poly in (("onyuz_cerceve_saci_1.0", CER_A), ("onyuz_cerceve_saci_1.0_F", CER_F)):
        s = sac(ad, "kapak_ic", takim=T, t=1.0, malzeme="AISI 430 (1.4016) 2B — manyetik fitil yüzü")
        P = levha(s, "+z", Z_CER0, poly, ad="cerceve")
        for x0, x1, y0, y1, kod in _acikliklar():
            if _icinde_poly(poly, (x0 + x1) / 2.0, (y0 + y1) / 2.0):
                P.dikdortgen((x0 + x1) / 2.0, (y0 + y1) / 2.0, x1 - x0, y1 - y0, r=3.0, tip="cekmece_acikligi", parca="%s açıklığı %.0f × %.0f" % (kod, x1 - x0, y1 - y0))
        K.CER[ad] = (s, P, poly)
    # ---- kayıtlar (traversler): çekmeceler arası 33'lük şeridin arkasında 1,2 L (yatay bacak y1+13 · ön bacak çerçeveye · 2 kulak duvarlara SP-M4 + ISO 7380)
    K.TRAVERS = []
    for k in KOLON_AD:
        x0 = KOLON_X[k]; x1 = x0 + KOLON_W[k]
        cl = _cek_kolon(k)
        for j, (a, b) in enumerate(zip(cl, cl[1:])):
            y1 = a[4] + HH_C[a[1]]; yn = b[4]
            assert abs(yn - y1 - 33.0) < 1e-6, (k, y1, yn)
            yb = y1 + 13.0                                             # yatay bacağın alt yüzü (avara kolu üst flanşı y1 + 12'de biter)
            ad = "onyuz_cerceve_kayit_%s_%d" % (k, j + 1)
            s = sac(ad, "ic", takim=T, t=T_IC)
            zb, zf = -20.0, Z_CER0 - G12
            P = levha(s, "+y", yb, [(zb, x0 + G12), (zf, x0 + G12), (zf, x1 - G12), (zb, x1 - G12)], ad="bacak")
            Fl = P.flans(0, 19.0, yon=+1, ad="kulak_sol"); Fr = P.flans(2, 19.0, yon=+1, ad="kulak_sag")
            Fo = P.flans(1, 19.0, yon=+1, bas=12.0, ad="on_bacak")      # sol uçta avara kolu ön flanşı (x0 + 1 … x0 + 13,7, y1 + 1 … y1 + 21, z 21–23)
            s.kose(Fo, Fr, "acik")
            K.TRAVERS.append(dict(ad=ad, k=k, y1=y1, yb=yb, P=P, on=Fo, sol=Fl, sag=Fr))
            yk = yb + 10.5                                             # kulak / ön bacak bağlantı yüksekliği (yatay bacak + büküm 3 + düz 16)
            for taraf, Fq, xw in (("sol", Fl, x0), ("sag", Fr, x1)):
                # duvar sacında PEM SP-M4: gövde köpük tarafında (duvarın kolondan uzak yüzü)
                ps = _duvar_pem(k, taraf, yk, 0.0, "M4", ad + "_%s_pem" % taraf, not_="kayıt kulağı")
                delik(Fq, (xw, yk, 0.0), 4.5, tip="vida_deligi", parca="kayıt kulağı M4")
                ic = 1.0 if taraf == "sol" else -1.0                    # kolon içi yönü
                eleman(S.vida("ISO7380", "M4", 6, (xw + ic * T_IC, yk, 0.0), (-ic, 0, 0), ad=ad + "_%s_vida" % taraf, birim=g.birim), takim=T)
            K.CER_DESTEK.append((Fo, [(x, yk) for x in GO.vida_konumlari(x0 + 30.0, x1 - 20.0, maks=160.0, uc=0.0)], "DIN1587", ad))
    # ---- PVC ısı kesici çıtalar (çerçeve ↔ dış kabuk ön dönüşleri · köpük sızdırmazlığı)
    for ad, k in (("onyuz_cerceve_isi_kesici_alt", (770.0, 4012.0, 142.0, 158.0)), ("onyuz_cerceve_isi_kesici_sol", (762.0, 778.0, 158.0, 742.0)),
                  ("onyuz_cerceve_isi_kesici_ust_A", (762.0, 2112.0, 742.0, 758.0)), ("onyuz_cerceve_isi_kesici_ust_F", (2112.0, 4012.0, 674.0, 690.0)),
                  ("onyuz_cerceve_isi_kesici_ust_T", (4012.0, 4378.0, 742.0, 758.0)), ("onyuz_cerceve_isi_kesici_sag_T", (4362.0, 4378.0, 431.0, 742.0))):
        ozel(ad, kutu(k[0], k[1], k[2], k[3], Z_CER1, Z_ON0 - 1.5), "PVC sert (ekstrüzyon)", "Isı kesici kapama çıtası PVC %.0f × 13,5 (çerçeve ↔ dış kabuk ön dönüşü)"
             % min(k[1] - k[0], k[3] - k[2]), "L %.0f" % max(k[1] - k[0], k[3] - k[2]), malzeme="PVC", mal="koyu", uretim=False, tur="parca", takim=T)
    # ---- çerçeve saplamaları: PEM FHP (baş çerçeve yüzünde, iz yok) → arkadaki dönüşte delik + DIN 9021 + somun (köpükte ISO 10511 · kolon içinde DIN 1587 kör)
    K.CER_SAPLAMA = []
    for kay in K.CER_DESTEK:
        Fq, pts, sstd, et = kay[0], kay[1], kay[2], kay[3]
        dis = kay[4] if len(kay) > 4 else "M4"
        for (a, b) in pts:
            p = (a, b, Z_CER1)
            par = None
            for ad_, (s_, P_, poly) in K.CER.items():
                if _icinde_poly(poly, a, b) and _kenar_mesafe(poly, a, b) >= 8.0 and \
                        all(not (x0 - 8.0 < a < x1 + 8.0 and y0 - 8.0 < b < y1 + 8.0) for x0, x1, y0, y1, _k in _acikliklar()):
                    par = (ad_, P_)
            if par is None:
                K.CER_SAPLAMA.append(dict(et=et, nokta=[a, b], durum="atlandı (çerçeve kenarına / açıklığa < 8)")); continue
            ad = "onyuz_cerceve_bag_%s_%d_%d" % (et, int(a), int(b))
            bq = S.vidali_birlesim(par[1], Fq, p, "pem_saplama", dis=dis, somun_std=sstd, ad=ad, birim=g.birim)
            birlesim(bq, takim=T)
            K.CER_SAPLAMA.append(dict(et=et, nokta=[a, b], durum="tamam", cerceve=par[0], somun=sstd, dis=dis))
    g.not_("ön çerçeve 430 1,0 (manyetik fitil 304'e tutmaz) · köpükle yapışır + bölme / eşik / tavan / sol / ara kat ön dönüşlerine PEM FHP saplama (yüzde iz yok) · "
           "kolon içinde kalan somunlar DIN 1587 kör somun · çerçeve ↔ dış kabuk arası PVC ısı kesici çıta (metal köprü yok) · çerçeve arkasında ısıtıcı kablo "
           "(24 V silikon, alüminyum bantla — modellenmedi)")


def _duvar_pem(k, taraf, y, z, dis, ad, not_=""):
    """kolon duvar sacında (bölme / sol / depo yan sacı) PEM SP: gövde köpük tarafında · vida kolon içinden"""
    Pw, xs, sg = K.DUVAR[(k, taraf)]
    # sg: köpük tarafı yönü (+1: +x tarafında köpük). Duvarın kolon yüzü xs · köpük yüzü xs + sg·t
    p_uzak = (xs + sg * T_IC, y, z)
    return pem_somun(Pw, p_uzak, (sg, 0, 0), dis, ad, not_=not_)


# =====================================================================================================================================
# 6 · TEKNİK SÜTUN (x 4028,5–4400): ara kat sandviç · depo hücresi · sökülür depo arka paneli · Secop rayları · servis paneli + klipsler
# =====================================================================================================================================
X_SAG_IC = X1 - 1.5                                                    # 4398,5 · sağ dış sacın iç yüzü


def teknik():
    T = "teknik"
    # ---------------- ARA KAT (Secop bölmesi ↔ depo) · alt sac tava (ön + arka dönüş yukarı 30 · sol / sağ dönüş aşağı 20 → B5 + sağ dış saca M5) + üst sac + PU
    s = sac("tk_ara_sac_alt", "ic", birim="B_SOGUTMA", takim=T, t=T_IC)
    xa, xb = T0 + G12, X_SAG_IC - G12
    P = levha(s, "+y", S0, [(Z_ARA[0] + G12, xa), (Z_ON0 - 16.0 - G12, xa), (Z_ON0 - 16.0 - G12, xb), (Z_ARA[0] + G12, xb)], ad="ara_alt")
    # kenarlar: 0 sol (x = xa) · 1 ön · 2 sağ · 3 arka
    Fon = P.flans(1, 30.0 - T_IC, yon=+1, ad="on_donus"); Far = P.flans(3, 30.0 - T_IC, yon=+1, ad="arka_donus")
    Fsl = P.flans(0, 20.0, yon=-1, bas=6.0, son=6.0, ad="sol_donus"); Fsg = P.flans(2, 20.0, yon=-1, bas=6.0, son=6.0, ad="sag_donus")
    K.PANEL["tk_ara_sac_alt"] = dict(s=s, P=P, on=Fon, arka=Far, sol=Fsl, sag=Fsg)
    K.CER_DESTEK.append((Fon, [(x, S0 + 15.0) for x in GO.vida_konumlari(T0 + 40.0, 4340.0, maks=200.0, uc=0.0)], "ISO10511", "ara_kat"))
    for z in (-400.0, -100.0):
        # sol dönüş ↔ B5 b sacı (teknik yüzü): b sacında PEM SP-M5 (gövde B5 köpüğünde) · ISO 7380 Secop bölmesinden
        Pw, xs, sg = K.DUVAR[("T", "sol")]
        pem_somun(Pw, (xs + sg * T_IC, S0 - 10.0, z), (sg, 0, 0), "M5", "tk_ara_sac_alt_sol_pem_%d" % int(-z), birim="B_SOGUTMA", takim=T)
        delik(Fsl, (xs, S0 - 10.0, z), 5.5, tip="vida_deligi", parca="ara kat → B5 M5")
        eleman(S.vida("ISO7380", "M5", 8, (xs + T_IC, S0 - 10.0, z), (-1.0, 0, 0), ad="tk_ara_sac_alt_sol_vida_%d" % int(-z), birim=g.birim), birim="B_SOGUTMA", takim=T)
        # sağ dönüş ↔ sağ dış sac: dış sacta FHP-M5 (dışta iz yok) + DIN 9021 + ISO 10511
        birlesim(S.vidali_birlesim(K.PANEL["yan_sag"]["yan"], Fsg, (X1, S0 - 10.0, z), "pem_saplama", dis="M5", ad="tk_ara_sac_alt_sag_bag_%d" % int(-z), birim=g.birim),
                 birim="B_SOGUTMA", takim=T)
    s = sac("tk_ara_sac_ust", "ic", birim="B_SOGUTMA", takim=T, t=T_IC)
    P = levha(s, "+y", S0 + 30.0 - T_IC, [(Z_ARA[0], T0), (Z_ON0 - 16.0, T0), (Z_ON0 - 16.0, X_SAG_IC), (Z_ARA[0], X_SAG_IC)], ad="ara_ust")
    K.PANEL["tk_ara_sac_ust"] = dict(s=s, P=P)
    pu("tk_ara_pu", (T0, X_SAG_IC, S0 + T_IC, S0 + 30.0 - T_IC, Z_ARA[0] + T_IC, Z_FL), birim=BIRIM)
    # ---------------- DEPO HÜCRESİ: sağ iç sac (4337,5 · ön dönüş köpüğe) · tavan iç sacı (728 · ön dönüş köpüğe) · PU
    s = sac("tk_depo_sag_ic_sac", "ic", birim="B_DEPO", takim=T, t=T_IC)
    P = levha(s, "+x", DEPO_ACIK[1], [(DEPO_ACIK[2], Z_DEPO_ARKA[1]), (Y_TAVAN, Z_DEPO_ARKA[1]), (Y_TAVAN, Z_CER0 - G12), (DEPO_ACIK[2], Z_CER0 - G12)], ad="sag")
    Fo = P.flans(2, 25.0, yon=+1, ad="on_donus")
    K.PANEL["tk_depo_sag_ic_sac"] = dict(s=s, P=P, on=Fo)
    K.DUVAR[("T", "sag")] = (P, DEPO_ACIK[1], +1.0)
    K.CER_DESTEK.append((Fo, [(DEPO_ACIK[1] + 13.0, y) for y in GO.vida_konumlari(480.0, 715.0, maks=200.0, uc=0.0)], "ISO10511", "depo_sag"))
    s = sac("tk_depo_tavan_ic_sac", "ic", birim="B_DEPO", takim=T, t=T_IC)
    P = levha(s, "+y", Y_TAVAN, [(Z_DEPO_ARKA[1], T0), (Z_CER0 - G12, T0), (Z_CER0 - G12, DEPO_ACIK[1]), (Z_DEPO_ARKA[1], DEPO_ACIK[1])], ad="tavan")
    Fo = P.flans(1, 25.0, yon=+1, ad="on_donus")
    K.PANEL["tk_depo_tavan_ic_sac"] = dict(s=s, P=P, on=Fo)
    K.CER_DESTEK.append((Fo, [(x, Y_TAVAN + 12.0) for x in GO.vida_konumlari(T0 + 30.0, DEPO_ACIK[1] - 30.0, maks=200.0, uc=0.0)], "ISO10511", "depo_tavan"))
    pu("tk_depo_sag_pu", (DEPO_ACIK[1] + T_IC, X_SAG_IC, DEPO_ACIK[2], 786.5, Z_DEPO_ARKA[1], Z_ON0 - 1.5), birim=BIRIM)
    pu("tk_depo_tavan_pu", (T0, DEPO_ACIK[1] + T_IC, Y_TAVAN + T_IC, 786.5, Z_DEPO_ARKA[1], Z_ON0 - 1.5), birim=BIRIM)
    # ---------------- DEPO ARKA PANELİ (sökülür sandviç 30 · pano servisi arkadan / Secop bölmesinden) · ön tava + arka sac + PU · 4 kulak
    s = sac("tk_depo_arka_sac_on", "ic", birim="B_DEPO", takim=T, t=T_IC)
    xa, xb, ya, yb = T0 + 1.0, X_SAG_IC - 1.0, DEPO_ACIK[2] + 1.0, 786.5 - 1.0
    P = levha(s, "+z", Z_DEPO_ARKA[1] - T_IC, [(xa + G12, ya + G12), (xb - G12, ya + G12), (xb - G12, yb - G12), (xa + G12, yb - G12)], ad="on")
    fl = [P.flans(i, Z_DEPO_ARKA[1] - Z_DEPO_ARKA[0] - T_IC, yon=-1, ad="donus_%d" % i) for i in range(4)]
    for i in range(4): s.kose(fl[i], fl[(i + 1) % 4], "acik")
    K.PANEL["tk_depo_arka_sac_on"] = dict(s=s, P=P)
    s = sac("tk_depo_arka_sac_arka", "ic", birim="B_DEPO", takim=T, t=T_IC)
    Pr = levha(s, "+z", Z_DEPO_ARKA[0], dikd(xa, xb, ya, yb), ad="arka")
    K.PANEL["tk_depo_arka_sac_arka"] = dict(s=s, P=Pr)
    pu("tk_depo_arka_pu", (xa + T_IC, xb - T_IC, ya + T_IC, yb - T_IC, Z_DEPO_ARKA[0] + T_IC, Z_DEPO_ARKA[1] - T_IC), birim="B_DEPO")
    zk = Z_DEPO_ARKA[0]                                                 # −470 · kulak bacağı arka sacın arkasında (pano tarafı)
    for j, (xk, yk_, taraf) in enumerate(((T0, 500.0, "sol"), (T0, 750.0, "sol"), (X_SAG_IC, 500.0, "sag"), (X_SAG_IC, 750.0, "sag"))):
        ad = "tk_depo_arka_kulak_%d" % j
        ks = sac(ad, "braket", birim="B_DEPO", takim=T)                 # 3 mm L: bir bacak duvarda (x), bir bacak panelin arkasında (z)
        sg = 1.0 if taraf == "sol" else -1.0                            # duvardan içeri
        t3 = ks.t; g3 = ks.R + t3
        if taraf == "sol":
            Pk = levha(ks, "+x", xk, [(yk_ - 15.0, zk - 30.0), (yk_ + 15.0, zk - 30.0), (yk_ + 15.0, zk - g3), (yk_ - 15.0, zk - g3)], ad="duvar_bacagi")
            Fk = Pk.flans(2, 30.0, yon=+1, ad="panel_bacagi")
        else:
            Pk = levha(ks, "-x", xk, [(zk - 30.0, yk_ - 15.0), (zk - g3, yk_ - 15.0), (zk - g3, yk_ + 15.0), (zk - 30.0, yk_ + 15.0)], ad="duvar_bacagi")
            Fk = Pk.flans(1, 30.0, yon=+1, ad="panel_bacagi")
        zm = zk - 20.0
        if taraf == "sol":
            Pw, xs, sgw = K.DUVAR[("T", "sol")]
            pem_somun(Pw, (xs + sgw * T_IC, yk_, zm), (sgw, 0, 0), "M5", ad + "_duvar_pem", birim="B_DEPO", takim=T)
            delik(Pk, (xk, yk_, zm), 5.5, tip="vida_deligi", parca="kulak → B5 M5")
            eleman(S.vida("ISO7380", "M5", 10, (xk + t3, yk_, zm), (-1.0, 0, 0), ad=ad + "_duvar_vida", birim=g.birim), birim="B_DEPO", takim=T)
        else:
            birlesim(S.vidali_birlesim(K.PANEL["yan_sag"]["yan"], Pk, (X1, yk_, zm), "pem_saplama", dis="M5", ad=ad + "_duvar_bag", birim=g.birim), birim="B_DEPO", takim=T)
        xp = xk + sg * 20.0
        birlesim(S.vidali_birlesim(Fk, Pr, (xp, yk_, zk - t3), "pem_somun", dis="M5", ad=ad + "_panel_bag", birim=g.birim), birim="B_DEPO", takim=T)
    # ---------------- SECOP MONTAJ RAYLARI: L 40 × 40 × 3 (abkant) + 2 uç plakası 3 mm (TIG) → B5 b sacına M5 perçin somun · sağ dış saca FHP-M5
    for ad_, (rz0, rz1, dk) in RAY_SEC.items():
        ad = "sogutma_grubu_montaj_rayi_" + ad_
        rs = sac(ad, "braket", birim="B_SOGUTMA", takim=T)
        t3 = rs.t; g3 = rs.R + t3
        xr0, xr1 = T0 + 3.5, X_SAG_IC - 3.5
        if dk < 0:                                                      # dik kol arkada
            P = levha(rs, "+y", Y_ALT + 1.5, [(rz0 + g3, xr0), (rz1, xr0), (rz1, xr1), (rz0 + g3, xr1)], ad="yatay")
            F = P.flans(3, 40.0, yon=+1, ad="dik")
        else:
            P = levha(rs, "+y", Y_ALT + 1.5, [(rz0, xr0), (rz1 - g3, xr0), (rz1 - g3, xr1), (rz0, xr1)], ad="yatay")
            F = P.flans(1, 40.0, yon=+1, ad="dik")
        for uc, xu, sgn in (("sol", T0, 1.0), ("sag", X_SAG_IC, -1.0)):
            up = sac(ad + "_uc_" + uc, "braket", birim="B_SOGUTMA", takim=T)
            xpl = xu if sgn > 0 else xu - 3.0
            Pu = levha(up, "+x", xpl, dikd(Y_ALT + 1.5, Y_ALT + 41.5, rz0, rz1), ad="uc")
            zc = (rz0 + rz1) / 2.0 + (3.0 if dk < 0 else -3.0)
            for j, dz in enumerate((-7.0, 7.0)):
                p = (xu, Y_ALT + 1.5 + 26.0, zc + dz)
                if uc == "sol":
                    Pw, xs, sgw = K.DUVAR[("T", "sol")]
                    pem_somun(Pw, (xs + sgw * T_IC, p[1], p[2]), (sgw, 0, 0), "M5", ad + "_uc_sol_pem_%d" % j, birim="B_SOGUTMA", takim=T)
                    delik(Pu, p, 5.5, tip="vida_deligi", parca="uç plakası → B5 M5")
                    eleman(S.vida("ISO7380", "M5", 10, (xu + 3.0, p[1], p[2]), (-1.0, 0, 0), ad=ad + "_uc_sol_vida_%d" % j, birim=g.birim), birim="B_SOGUTMA", takim=T)
                else:
                    birlesim(S.vidali_birlesim(K.PANEL["yan_sag"]["yan"], Pu, (X1, p[1], p[2]), "pem_saplama", dis="M5", ad=ad + "_uc_sag_bag_%d" % j, birim=g.birim),
                             birim="B_SOGUTMA", takim=T)
            kaynak(S.kaynak_dikisi((xu + sgn * 3.0, Y_ALT + 1.5 + t3, rz0 + 4.0), (xu + sgn * 3.0, Y_ALT + 1.5 + t3, rz1 - 4.0), (sgn, 0, 0), (0, 1, 0), 3.0,
                                   ad=ad + "_uc_%s_kaynak" % uc, birim=g.birim, taraf="iç köşe", not_="uç plakası ↔ L ray"), birim="B_SOGUTMA", takim=T)
    # ---------------- SERVİS PANELİ (Secop bölmesinin önü · v3.7: 126–453,5) · tava 1,5 (dönüş 40, köşe bindirme + TIG) · 40 lazer yarık · 4 gizli klips
    a_, b_ = KAPAK_X["T"]
    s = sac("tk_kapak_sogutma_dis_sac", "kapak_dis", birim="B_SOGUTMA", takim=T, t=1.5)
    gk = s.R + s.t
    D = levha(s, "+z", Z_ON - 1.5, [(a_ + gk, SERVIS_Y[0] + gk), (b_ - gk, SERVIS_Y[0] + gk), (b_ - gk, SERVIS_Y[1] - gk), (a_ + gk, SERVIS_Y[1] - gk)], ad="on_yuz")
    fa = [D.flans(i, Z_ON - Z_ON0, yon=-1, ad=("alt", "sag", "ust", "sol")[i] + "_donus") for i in range(4)]
    s.kose(fa[0], fa[1], "bindirme", ustte=fa[0]); s.kose(fa[1], fa[2], "bindirme", ustte=fa[2])
    s.kose(fa[2], fa[3], "bindirme", ustte=fa[2]); s.kose(fa[3], fa[0], "bindirme", ustte=fa[0])
    for xa_, xb_, ya_, yb_ in PANEL_YARIK:
        D.oblong((xa_ + xb_) / 2.0, (ya_ + yb_) / 2.0, xb_ - xa_, yb_ - ya_, tip="havalandirma_yarigi", parca="Secop atış yarığı 145 × 8")
    K.PANEL["tk_kapak_sogutma_dis_sac"] = dict(s=s, D=D, don=fa)
    for i, (xk0, xk1) in enumerate(((a_ + 1.5, T0 - 0.5), (X1 - 26.0, X1 - 1.5))):
        for j, yk_ in enumerate((200.0, 400.0)):
            kk = kutu(xk0, xk1, yk_ - 10.0, yk_ + 10.0, Z_CER1, Z_ON0 + 6.0)
            ozel("tk_panel_klipsi_%d" % (2 * i + j), kk, "Fastmount (gizli panel klipsi) sınıfı", "Gizli panel klipsi paslanmaz (erkek panelde · dişi %s)" %
                 ("çerçeveye 1 × M4" if i == 0 else "sağ dış saca yapıştırma + 1 × M4"), "20 × %.0f × 21" % (xk1 - xk0), malzeme="AISI 316 / POM", mal="celik",
                 birim="B_SOGUTMA", takim=T)
    g.not_("teknik sütun: ara kat sandviç (alt tava + üst sac + PU 27,6) B5'e PEM SP-M5 + sağ dış saca FHP-M5 · depo hücresi (sağ + tavan iç sacı, ön dönüşler köpüğe) · "
           "depo arka paneli sökülür sandviç: 4 L kulak (B5 + sağ dış sac) · Secop rayları L 3 mm uç plakalı (B5'e perçin somun, sağa FHP) · servis paneli 1,5 tava, "
           "40 lazer yarık, 4 gizli klips (menteşe yok)")


# =====================================================================================================================================
# 7 · ÇEKMECELER (21 + depo) · ön (dış tava 1,5 + iç ada 1,0 + PVC fitil taşıyıcı + PU) · kutu (GIDA: halka 1,0 R3 + taban 2,0) · ön bağlantı U 2 · ray adaptörü L 3
# =====================================================================================================================================
PVC_PROF = [(-5.2, -3.2, 39.0, 49.45), (3.2, 5.2, 39.0, 49.45), (-5.2, 5.2, 47.45, 49.45), (5.2, 9.4, 39.0, 41.0)]   # (u0, u1, z0, z1) · u: yoldan dışarı
PVC_DIS = 9.4                                                          # taşıyıcının dış dudağı (yoldan) · arka dönüşler 0,1 geride biter


def _halka(yol, u0, u1, z0, z1):
    ax0, ax1, ay0, ay1 = yol
    dis = kutu(ax0 - u1, ax1 + u1, ay0 - u1, ay1 + u1, z0, z1)
    ic = kutu(ax0 - u0, ax1 + u0, ay0 - u0, ay1 + u0, z0 - 1.0, z1 + 1.0)
    return dis.cut(ic)


def cekmece_onu(on, birim, pa, pb, pc, pd, yol, baglantilar, grup="CEKMECE", ad_dis=None):
    """sandviç ön 40: dış tava 1,5 (dönüş 40 · köşe bindirme + TIG) + geniş kenarda arka kapama L 1,0 + iç ada 1,0 (kanal iç duvarı, dönüş 10,45) + PVC fitil taşıyıcı
    (ısı kesici · kanal 6,4 × 8,45) + PU · baglantilar: [(x, y)] ön bağlantı U'larının vida noktaları (adada PEM SP-M5)"""
    T = "cekmece_on"
    ax0, ax1, ay0, ay1 = yol
    s = sac(ad_dis or on + "_dis_sac_1.5", "kapak_dis", birim=birim, grup=grup, takim=T, t=1.5)
    gk = s.R + s.t
    D = levha(s, "+z", Z_ON - 1.5, [(pa + gk, pc + gk), (pb - gk, pc + gk), (pb - gk, pd - gk), (pa + gk, pd - gk)], ad="on_yuz")
    fa = [D.flans(i, Z_ON - Z_ON0, yon=-1, ad=("alt", "sag", "ust", "sol")[i] + "_donus") for i in range(4)]
    s.kose(fa[0], fa[1], "bindirme", ustte=fa[0]); s.kose(fa[1], fa[2], "bindirme", ustte=fa[2])
    s.kose(fa[2], fa[3], "bindirme", ustte=fa[2]); s.kose(fa[3], fa[0], "bindirme", ustte=fa[0])
    # geniş kenarlar: ARKA KAPAMA 1,0 (L · flanşı dönüşün iç yüzüne yaslı, kalıpta konumlanır, köpükle yapışır) — dış tavaya ikinci kat büküm abkantta
    # düz bıçakla yapılamıyor (DFM: kaz boynu bıçak gerekir) → ayrı parça · PVC dış dudağına 0,1
    u = dict(alt=ay0 - pc, sag=pb - ax1, ust=pd - ay1, sol=ax0 - pa)
    gen = {k: (v - PVC_DIS - 0.1 - 1.5) for k, v in u.items()}
    arka = {}
    y_a = (ay0 - PVC_DIS - 0.1 + 0.5) if gen["alt"] >= 12.0 else pc + 2.0
    y_b = (ay1 + PVC_DIS + 0.1 - 0.5) if gen["ust"] >= 12.0 else pd - 2.0
    for k in ("alt", "sag", "ust", "sol"):
        if gen[k] < 12.0: continue
        sk = sac(on + "_dis_sac_arka_" + k, "kapak_ic", birim=birim, grup=grup, takim=T, t=1.0)
        gk1 = sk.R + sk.t
        if k == "alt":
            P = levha(sk, "+z", Z_ON0, [(pa + 2.0, pc + 1.5 + gk1), (pb - 2.0, pc + 1.5 + gk1), (pb - 2.0, ay0 - PVC_DIS - 0.1), (pa + 2.0, ay0 - PVC_DIS - 0.1)], ad="kapama")
            F = P.flans(0, 10.0, yon=+1, ad="flans")
        elif k == "ust":
            P = levha(sk, "+z", Z_ON0, [(pa + 2.0, ay1 + PVC_DIS + 0.1), (pb - 2.0, ay1 + PVC_DIS + 0.1), (pb - 2.0, pd - 1.5 - gk1), (pa + 2.0, pd - 1.5 - gk1)], ad="kapama")
            F = P.flans(2, 10.0, yon=+1, ad="flans")
        elif k == "sol":
            P = levha(sk, "+z", Z_ON0, [(pa + 1.5 + gk1, y_a), (ax0 - PVC_DIS - 0.1, y_a), (ax0 - PVC_DIS - 0.1, y_b), (pa + 1.5 + gk1, y_b)], ad="kapama")
            F = P.flans(3, 10.0, yon=+1, ad="flans")
        else:
            P = levha(sk, "+z", Z_ON0, [(ax1 + PVC_DIS + 0.1, y_a), (pb - 1.5 - gk1, y_a), (pb - 1.5 - gk1, y_b), (ax1 + PVC_DIS + 0.1, y_b)], ad="kapama")
            F = P.flans(1, 10.0, yon=+1, ad="flans")
        arka[k] = sk
    K.PU_KES.append((on + "_pu", _halka(yol, -3.2, 3.2, Z_ON0 - 1.0, 47.45)))          # fitil dişinin kanalı boş kalır
    # PVC fitil taşıyıcı (ısı kesici · kanal) — 4 dikdörtgen bileşenden halka (köşeler gönye)
    pv = None
    for u0, u1, z0, z1 in PVC_PROF:
        h = _halka(yol, u0, u1, z0, z1); pv = h if pv is None else pv.fuse(h)
    ozel(on + "_fitil_kanali", pv.clean(), "PVC sert ekstrüzyon (gönye kaynaklı)", "Fitil taşıyıcı / ısı kesici profil PVC · kanal 6,4 × 8,45 (fitil dişi geçer) · dış dudak 4,2",
         "çevre %.0f mm" % (2 * (ax1 - ax0 + ay1 - ay0)), malzeme="PVC", mal="koyu", tur="parca", birim=birim, grup=grup, takim=T)
    # iç ada 1,0 (kanalın iç duvarı: dönüş z 49,45'e)
    si = sac(on + "_ic_sac_1.0", "kapak_ic", birim=birim, grup=grup, takim=T, t=1.0)
    gi = si.R + si.t; e = 5.2 + gi
    I = levha(si, "+z", Z_ON0, [(ax0 + e, ay0 + e), (ax1 - e, ay0 + e), (ax1 - e, ay1 - e), (ax0 + e, ay1 - e)], ad="ada")
    fi = [I.flans(i, 49.45 - Z_ON0, yon=+1, ad="donus_%d" % i) for i in range(4)]
    for i in range(4): si.kose(fi[i], fi[(i + 1) % 4], "acik")
    pu(on + "_pu", (pa + 1.5, pb - 1.5, pc + 1.5, pd - 1.5, Z_ON0, Z_ON - 1.5), birim=birim, grup=grup)
    return dict(dis=s, D=D, don=fa, arka=arka, ic=si, I=I)


def _on_baglanti(kod, birim, taraf, w_dis, y0, y1, I, sg, grup="CEKMECE"):
    """ön bağlantı L 2 mm: gövde (x = w_dis dış yüz, z 22 → 39) ayağı kutunun önüne iki yandan TIG (dıştan · kutunun içinde iz yok) · kanat iç adaya
    (z 39 · 2 × ISO 7380 M5 anahtar deliğinden → adada PEM SP-M5) · U yerine L: 17'lik U ikinci bükümde bıçağa çarpıyor (DFM)"""
    ad = "%s_on_baglanti_%s" % (kod, taraf)
    s = sac(ad, "braket", birim=birim, grup=grup, takim="cekmece_kutu", t=2.0, mal="celik")
    g2 = s.R + s.t
    n = "+x" if sg > 0 else "-x"
    if n == "+x":
        P = levha(s, n, w_dis, [(y0, Z_TUB1), (y1, Z_TUB1), (y1, Z_ON0 - g2), (y0, Z_ON0 - g2)], ad="govde")
        F2 = P.flans(2, 22.0, yon=+1, ad="kanat_on")
    else:
        P = levha(s, n, w_dis, [(Z_TUB1, y0), (Z_ON0 - g2, y0), (Z_ON0 - g2, y1), (Z_TUB1, y1)], ad="govde")
        F2 = P.flans(1, 22.0, yon=+1, ad="kanat_on")
    xh = w_dis + sg * 14.5
    for j, yh in enumerate((y0 + 10.0, y1 - 10.0)):
        b = S.vidali_birlesim(F2, I, (xh, yh, Z_ON0), "pem_somun", dis="M5", ad="%s_bag_%d" % (ad, j), birim=g.birim)
        birlesim(b, birim=birim, grup=grup, takim="cekmece_kutu")
    for j, (xe, u1) in enumerate(((w_dis, (-sg, 0, 0)), (w_dis + sg * 2.0, (sg, 0, 0)))):
        kaynak(S.kaynak_dikisi((xe, y0 + 3.0, Z_TUB1), (xe, y1 - 3.0, Z_TUB1), u1, (0, 0, 1.0), 2.0, ad=ad + "_kaynak_%d" % j, birim=g.birim, taraf="dış",
                               not_="gövde ayağı ↔ kutu önü · TIG dıştan (kutunun içinde iz yok)"), birim=birim, grup=grup, takim="cekmece_kutu")
    return s


def cekmece_kutusu(kod, birim, ka, kb, kc, kd, z0, z1, t_duvar=1.0, t_taban=2.0, grup="CEKMECE", ad_halka=None, ad_taban=None, kaynak_a=2.0, on_ayri=None):
    """GIDA: duvar halkası (arka + 2 yan + 2 ön yarım · 4 büküm R 3 · ek ön ortada alın kaynağı, taşlanır) + taban plakası (içeride, köşeleri 3 pah) · iç köşeler TIG taşlanmış"""
    T = "cekmece_kutu"
    s = sac(ad_halka or "%s_kutu_halka_%.1f" % (kod, t_duvar), "ic", birim=birim, grup=grup, takim=T, t=t_duvar, R=3.0, bolge="gida")
    gk = s.R + s.t
    P = levha(s, "+z", z0, [(ka + gk, kc), (kb - gk, kc), (kb - gk, kd), (ka + gk, kd)], ad="arka")
    Fs = P.flans(1, z1 - z0, yon=+1, ad="sag"); Fl = P.flans(3, z1 - z0, yon=+1, ad="sol")
    if on_ayri is None:
        xm = (ka + kb) / 2.0
        Fs.flans(1, kb - xm - 0.25, yon=+1, ad="on_sag"); Fl.flans(1, xm - ka - 0.25, yon=+1, ad="on_sol")
    else:                                                               # yüksek kap (depo 236,5): halka kapanmıyor (DFM) → U + ayrı ön duvar, iki köşe TIG + taşlama R ≥ 3
        so = sac(on_ayri, "ic", birim=birim, grup=grup, takim=T, t=t_duvar, bolge="gida")
        levha(so, "+z", z1 - t_duvar, dikd(ka + t_duvar, kb - t_duvar, kc, kd), ad="on")
        for ad_, xk, u1 in (("sol", ka + t_duvar, (1.0, 0, 0)), ("sag", kb - t_duvar, (-1.0, 0, 0))):
            kaynak(S.kaynak_dikisi((xk, kc + t_taban + 3.0, z1 - t_duvar), (xk, kd - 3.0, z1 - t_duvar), u1, (0, 0, -1.0), kaynak_a, ad="%s_kaynak_%s" % (on_ayri, ad_),
                                   birim=g.birim, taraf="iç (GIDA)", not_="ön duvar ↔ yan duvar · TIG + taşlama (iç köşe R ≥ 3)"), birim=birim, grup=grup, takim=T)
    st = sac(ad_taban or "%s_kutu_taban_%.1f" % (kod, t_taban), "yuk", birim=birim, grup=grup, takim=T, t=t_taban, bolge="gida")
    c = 3.0; a0, a1, b0, b1 = ka + t_duvar, kb - t_duvar, z0 + t_duvar, z1 - t_duvar
    levha(st, "+y", kc, [(b0 + c, a0), (b1 - c, a0), (b1, a0 + c), (b1, a1 - c), (b1 - c, a1), (b0 + c, a1), (b0, a1 - c), (b0, a0 + c)], ad="taban")
    yt = kc + t_taban
    for ad_, p0, p1, u1, u2 in (("arka", (a0 + 4.0, yt, b0), (a1 - 4.0, yt, b0), (0, 0, 1.0), (0, 1.0, 0)), ("on", (a0 + 4.0, yt, b1), (a1 - 4.0, yt, b1), (0, 0, -1.0), (0, 1.0, 0)),
                                ("sol", (a0, yt, b0 + 4.0), (a0, yt, b1 - 4.0), (1.0, 0, 0), (0, 1.0, 0)), ("sag", (a1, yt, b0 + 4.0), (a1, yt, b1 - 4.0), (-1.0, 0, 0), (0, 1.0, 0))):
        kaynak(S.kaynak_dikisi(p0, p1, u1, u2, kaynak_a, ad="%s_kaynak_%s" % (s.ad, ad_), birim=g.birim, taraf="iç (GIDA)", not_="taban ↔ duvar · TIG + taşlama (iç köşe R ≥ 3)"),
               birim=birim, grup=grup, takim=T)
    return s, P


def _ray_adaptoru(kod, birim, taraf, x0, x1, yo, grup="CEKMECE"):
    """ray adaptörü L 3 mm: dik bacak ray iç elemanına (4 × M4 kılavuz · vidası ray tarafının) · yatay bacak kutu yan duvarına alın (dıştan 3 × TIG)"""
    ad = "%s_ray_adaptor_%s" % (kod, taraf)
    s = sac(ad, "braket", birim=birim, grup=grup, takim="cekmece_kutu", mal="celik")
    g3 = s.R + s.t
    ya = yo + RAY_Y0 + 6.2                                              # ray iç elemanının alt kanadının üstü (yo + 10,2)
    za, zb = Z_TUB0, -30.0                                              # önde avara (z −18…16) + avara kolu (z −9…23) → adaptör −30'da biter
    if taraf == "sol":
        xr, xk = x0 + RAY_T, x0 + KUTU_KENAR
        P = levha(s, "+y", ya, [(za, xr + g3), (zb, xr + g3), (zb, xk), (za, xk)], ad="yatay")
        F = P.flans(0, yo + 38.0 - ya, yon=+1, ad="dik")
        sg = 1.0
    else:
        xr, xk = x1 - RAY_T, x1 - KUTU_KENAR
        P = levha(s, "+y", ya, [(za, xk), (zb, xk), (zb, xr - g3), (za, xr - g3)], ad="yatay")
        F = P.flans(2, yo + 38.0 - ya, yon=+1, ad="dik")
        sg = -1.0
    for z in (-560.0, -400.0, -240.0, -80.0):
        delik(F, (xr, yo + 28.0, z), 3.3, tip="kilavuz_M4", parca="M4 kılavuz (ray iç elemanı DIN 7991 M4 × 8 · ray tarafının)")
        arayuz(S.vida("DIN7991", "M4", 8, (xr - sg * 1.2, yo + 28.0, z), (sg, 0, 0), ad="arayuz_%s_ray_%d" % (ad, int(-z)), birim=g.birim),
               "%s ray iç elemanı (mekanizma)" % kod, "ray iç elemanında havşalı Ø4,5 (Accuride DZ3832 iç eleman delikleri) · adaptörde M4 kılavuz", "mekanizma sahibi")
    for z in (-560.0, -320.0, -80.0):
        kaynak(S.kaynak_dikisi((xk, ya + 3.0, z - 20.0), (xk, ya + 3.0, z + 20.0), (-sg, 0, 0), (0, 1.0, 0), 2.5, ad="%s_kaynak_%d" % (ad, int(-z)), birim=g.birim,
                               taraf="dış", not_="adaptör ↔ kutu yanı · TIG dıştan, aralıklı 3 × 40"), birim=birim, grup=grup, takim="cekmece_kutu")
    return s


def cekmeceler():
    T = "cekmece"
    K.CEK_ON = {}
    for kol, kod, tip, x0, yo in CEK:
        x1 = x0 + KOLON_W[kol]; y1 = yo + HH_C[kod]
        pa, pb = KAPAK_X[kol]
        pc = ON_ALT if kod in ALT_KOD else yo - BIND
        pd = ON_UST if kod in UST_KOD else y1 + BIND
        yol = (x0 - FITIL_G, x1 + FITIL_G, yo - FITIL_G, y1 + FITIL_G)
        ka, kb, kc, kd = x0 + KUTU_KENAR, x1 - KUTU_KENAR, yo + KC, y1 - 10.0
        on = cekmece_onu(kod + "_on", kod, pa, pb, pc, pd, yol, [])
        K.CEK_ON[kod] = on
        cekmece_kutusu(kod, kod, ka, kb, kc, kd, Z_TUB0, Z_TUB1)
        _on_baglanti(kod, kod, "sol", ka, yo + 12.0, kd - 4.0, on["I"], +1.0)
        _on_baglanti(kod, kod, "sag", kb, yo + 12.0, kd - 4.0, on["I"], -1.0)
        _ray_adaptoru(kod, kod, "sol", x0, x1, yo)
        _ray_adaptoru(kod, kod, "sag", x0, x1, yo)
    # ---------------- DEPO çekmecesi (B_DEPO): ön (v3.7 456,5–785 · fitil alt bacağı +8) + kap (GIDA 1,5: halka + taban + ayırıcı) + kapak 1,0 + ön bağlantı U
    B_ = "B_DEPO"
    d = DEPO_KUTU
    a_, b_ = KAPAK_X["T"]
    yol = (DEPO_ACIK[0] - FITIL_G, DEPO_ACIK[1] + FITIL_G, DEPO_ACIK[2] - FITIL_G + DEPO_FITIL_DY, DEPO_ACIK[3] + FITIL_G)
    on = cekmece_onu("tk_kapak_depo", B_, a_, b_, DEPO_KAPAK_Y[0], DEPO_KAPAK_Y[1], yol, [])
    K.CEK_ON["depo"] = on
    s, P = cekmece_kutusu("tk_depo", B_, d["ka"], d["kb"], d["kc"], d["kd"], d["z0"], d["z1"], t_duvar=1.5, t_taban=1.5, ad_halka="tk_depo_kutu_halka_1.5",
                          ad_taban="tk_depo_kutu_taban_1.5", kaynak_a=2.5, on_ayri="tk_depo_kutu_on_1.5")
    xd = d["kb"] - 1.5 - d["sucuk_w"] - 1.5
    sa = sac("tk_depo_ayirici_1.5", "yuk", birim=B_, grup="CEKMECE", takim="depo", t=1.5, bolge="gida")
    levha(sa, "+x", xd, dikd(d["kc"] + 1.5, d["kd"] - 11.0, d["z0"] + 1.5 + 2.0, d["z1"] - 1.5 - 2.0), ad="ayirici")
    for ad_, zz in (("arka", d["z0"] + 1.5), ("on", d["z1"] - 1.5)):
        sg = 1.0 if ad_ == "arka" else -1.0
        kaynak(S.kaynak_dikisi((xd + 1.5, d["kc"] + 1.5 + 4.0, zz), (xd + 1.5, d["kd"] - 15.0, zz), (1.0, 0, 0), (0, 0, sg), 2.0, ad="tk_depo_ayirici_kaynak_%s" % ad_,
                               birim=g.birim, taraf="iç (GIDA)", not_="ayırıcı ↔ kap duvarı · TIG taşlanır"), birim=B_, grup="CEKMECE", takim="depo")
    kaynak(S.kaynak_dikisi((xd + 1.5, d["kc"] + 1.5, d["z0"] + 6.0), (xd + 1.5, d["kc"] + 1.5, d["z1"] - 6.0), (1.0, 0, 0), (0, 1.0, 0), 2.0, ad="tk_depo_ayirici_kaynak_taban",
                           birim=g.birim, taraf="iç (GIDA)", not_="ayırıcı ↔ taban · TIG taşlanır"), birim=B_, grup="CEKMECE", takim="depo")
    # kapak 1,0: yan duvarların üstüne oturur · ön / arka kenarı aşağı 10 (kabın içine, yerinde tutar)
    sk = sac("tk_depo_kapak_1.0", "kapak_ic", birim=B_, grup="CEKMECE", takim="depo", t=1.0, R=3.0, bolge="gida")
    gk = sk.R + sk.t
    zb0, zb1 = d["z0"] + 1.5 + 0.5, d["z1"] - 1.5 - 0.5
    Pk = levha(sk, "+y", d["kd"], [(zb0 + gk, d["ka"]), (zb1 - gk, d["ka"]), (zb1 - gk, d["kb"]), (zb0 + gk, d["kb"])], ad="kapak")
    Pk.flans(1, 10.0, yon=-1, bas=2.5, son=2.5, ad="on_etek"); Pk.flans(3, 10.0, yon=-1, bas=2.5, son=2.5, ad="arka_etek")
    _on_baglanti("tk_depo", B_, "sol", d["ka"] + 2.0, DEPO_ACIK[2] + 12.0, d["kd"] - 4.0, on["I"], +1.0)
    _on_baglanti("tk_depo", B_, "sag", d["kb"] - 2.0, DEPO_ACIK[2] + 12.0, d["kd"] - 4.0, on["I"], -1.0)
    # ray iç elemanları doğrudan kabın yan duvarına: CD kaynak saplaması M4 (dıştan · iç yüz izsiz) · somun ray tarafının (arayüz)
    yr = DEPO_ACIK[2] + RAY_Y0 + RAY_H / 2.0
    for taraf, xw, sg in (("sol", d["ka"], -1.0), ("sag", d["kb"], 1.0)):
        for z in (-400.0, -270.0, -140.0, -10.0):
            sp = silindir((xw, yr, z), (sg, 0, 0), 1.98, 8.0).fuse(silindir((xw, yr, z), (sg, 0, 0), 2.6, 0.8))
            ozel("tk_depo_ray_saplamasi_%s_%d" % (taraf, int(-z)), sp, "ISO 13918 CD M4 × 8 A2", "CD kaynak saplaması M4 × 8 (kap yan duvarına dıştan · gıda yüzü izsiz)",
                 "M4 × 8", malzeme="A2", mal="celik", birim=B_, grup="CEKMECE", takim="depo")
            arayuz(S.somun("ISO10511", "M4", (xw + sg * 1.2, yr, z), (sg, 0, 0), ad="arayuz_tk_depo_ray_%s_%d_somun" % (taraf, int(-z)), birim=g.birim),
                   "tk_depo_ray_ic_%s (mekanizma)" % taraf, "ray iç elemanında Ø4,5 (aynı eksen) · ISO 10511 M4 rayın içinden", "mekanizma sahibi")
    g.not_("çekmece kutusu GIDA: duvar halkası tek parça (4 büküm R 3, ek önde ortada alın kaynağı taşlanır) + taban plakası içeride, taban ↔ duvar TIG iç köşe "
           "taşlanır (R ≥ 3) · kutunun içinde vida / perçin / bindirme YOK · ön bağlantı U ve ray adaptörü kutuya DIŞTAN TIG · ön: PVC fitil taşıyıcı = ısı kesici "
           "(dış tava ↔ iç ada metal teması yok) · v3.7 depo fitili alt bacağı +8 (h3_kapak_v1) → depo önünün kanalı da +8")


# =====================================================================================================================================
# 8 · MEKANİZMA BAĞLANTI NOKTALARI (iç kabukta PEM SP · gövde köpük tarafında, köpükten ÖNCE kör başlıkla kapatılır · vidaları mekanizma tarafının)
# =====================================================================================================================================
RAY_Z_SOMUN = (-590.0, -420.0, -250.0, -60.0)


def mekanizma_somunlari():
    T = "mekanizma_noktasi"
    K.MEK_NOKTA = []
    for kol, kod, tip, x0, yo in CEK:
        x1 = x0 + KOLON_W[kol]
        yr = yo + RAY_Y0 + RAY_H / 2.0
        for taraf in ("sol", "sag"):
            for z in RAY_Z_SOMUN:
                ad = "%s_ray_%s_pem_%d" % (kod, taraf, int(-z))
                _duvar_pem(kol, taraf, yr, z, "M5", ad, not_="ray dış elemanı (Accuride DZ3832 · M5)")
                K.MEK_NOKTA.append(dict(ad=ad, karsi="%s_ray_dis_%s" % (kod, taraf), dis="M5", nokta=[K.DUVAR[(kol, taraf)][1], yr, z]))
        U = K.PANEL["ic_kabuk_" + kol]["arka"]
        cz = Z_ARKA_IC - T_IC
        mx0 = x0 + KX + KAS_B / 2.0 + 2.0 + GOBEK_L; ky = yo + KY
        for j, dy in enumerate((-18.0, 18.0)):
            ad = "%s_motor_braketi_pem_%d" % (kod, j)
            pem_somun(U, (mx0 + 20.0, ky + dy, cz), (0, 0, -1.0), "M5", ad, takim=T, not_="motor braketi ayağı")
            K.MEK_NOKTA.append(dict(ad=ad, karsi="%s_motor_braketi" % kod, dis="M5", nokta=[mx0 + 20.0, ky + dy, Z_ARKA_IC]))
        lx1 = x0 + SEN_X[0] - 0.6
        my0 = yo + SEN_Y0; ly1 = my0 + SEN[1] + 2.0
        kny = None
        for (xa_, xb_), ku in (((KOLON_X["K1"] + KAN_X[1], X_ALCAK + KAN_X[1]), KAN_UST), ((X_ALCAK + KAN_X[1], KOLON_X["K6"] + KAN_X[1]), KAN_UST_F)):
            lx0 = lx1 - SEN[2]
            if xa_ < lx1 and lx0 < xb_ and ku[0] < ly1 + 1.0 and ly1 - 2.0 - 1.0 < ku[1]: kny = ku
        ylo, yhi = ((kny[0] - 4.0 - 22.0, kny[0] - 4.0 + 2.0) if kny else (ly1 - 24.0, ly1))
        for j, yy in enumerate((ylo + 6.0, yhi - 6.0)):
            ad = "%s_sensor_lami_pem_%d" % (kod, j)
            pem_somun(U, (lx1 - 8.0, yy, cz), (0, 0, -1.0), "M4", ad, takim=T, not_="sensör lamı tırnağı")
            K.MEK_NOKTA.append(dict(ad=ad, karsi="%s_sensor_lami" % kod, dis="M4", nokta=[lx1 - 8.0, yy, Z_ARKA_IC]))
    # depo rayları (B5 b sacı + depo sağ iç sacı)
    yr = DEPO_ACIK[2] + RAY_Y0 + RAY_H / 2.0
    for taraf in ("sol", "sag"):
        for z in (-400.0, -270.0, -140.0, -10.0):
            ad = "tk_depo_ray_%s_pem_%d" % (taraf, int(-z))
            _duvar_pem("T", taraf, yr, z, "M5", ad, not_="depo rayı dış elemanı")
            K.MEK_NOKTA.append(dict(ad=ad, karsi="tk_depo_ray_dis_%s" % taraf, dis="M5", nokta=[K.DUVAR[("T", taraf)][1], yr, z]))
    # gider ana hattı boru eyerleri (taban iç sacına 2 × M4) · kablo kanalları (arka iç sacına M4)
    for kol, xk in (("K3", 2400.0), ("K5", 3250.0), ("K6", 3700.0)):
        Ft = K.PANEL["ic_kabuk_" + kol]["taban"]
        for j, z in enumerate((-745.0, -731.0)):
            ad = "ic_kabuk_%s_gider_eyeri_pem_%d" % (kol, j)
            pem_somun(Ft, (xk, Y_TABAN - T_IC, z), (0, -1.0, 0), "M4", ad, takim=T, not_="gider boru eyeri")
            K.MEK_NOKTA.append(dict(ad=ad, karsi="gider_ana_hatti_kelepcesi_%s" % kol, dis="M4", nokta=[xk, Y_TABAN, z]))
    kan = []
    for kol in KOLON_AD:
        x0 = KOLON_X[kol]; ku = KAN_UST if kol in ("K1", "K2") else KAN_UST_F
        kan += [(kol, x0 + 210.0, y) for y in GO.vida_konumlari(Y_TABAN + 40.0, ku[0] - 40.0, maks=220.0, uc=0.0)]
    for kol in ("K1", "K2"):
        x0 = KOLON_X[kol]; x1 = x0 + KOLON_W[kol]
        kan += [(kol, x, (KAN_UST[0] + KAN_UST[1]) / 2.0) for x in GO.vida_konumlari(max(x0, 988.5) + 60.0, min(x1, 2072.5) - 30.0, maks=250.0, uc=0.0)]
    for kol in ("K3", "K5", "K6"):
        x0 = KOLON_X[kol]; x1 = x0 + KOLON_W[kol]
        kan += [(kol, x, (KAN_UST_F[0] + KAN_UST_F[1]) / 2.0) for x in GO.vida_konumlari(x0 + 60.0 if kol != "K3" else x0 + 260.0, x1 - 30.0, maks=250.0, uc=0.0)]
    kan.append(("K2", 2052.5, 673.0))
    for kol, x, y in kan:
        U = K.PANEL["ic_kabuk_" + kol]["arka"]
        ad = "ic_kabuk_%s_kanal_pem_%d_%d" % (kol, int(x), int(y))
        pem_somun(U, (x, y, Z_ARKA_IC - T_IC), (0, 0, -1.0), "M4", ad, takim=T, not_="kablo kanalı")
        K.MEK_NOKTA.append(dict(ad=ad, karsi="kablo_kanali (B_KABLO)", dis="M4", nokta=[x, y, Z_ARKA_IC]))
    g.not_("mekanizma bağlantı noktaları iç kabukta PEM SP (gövde köpük tarafında, köpükten önce kör başlıkla kapatılır): raylar 4 × M5 · motor braketi 2 × M5 · "
           "sensör lamı 2 × M4 · boru eyeri 2 × M4 · kablo kanalı M4 · vidalar mekanizma tarafının (arayüz) · AÇIK: evaporatör askısı / damlama teknesi braketi arka "
           "duvara nasıl bağlanıyor (mekanizma modelinde tırnak yok) → yer verilince PEM SP-M5 eklenir")


# =====================================================================================================================================
# 9 · KOMŞU BAĞLANTILARI (M8) · avara kolu saplamaları (çerçevede FHP-M3)
# =====================================================================================================================================
def _tavan_paneli(x):
    return K.PANEL["tavan_dis_sac_A" if x < X_EK else "tavan_dis_sac"]["ust"]


def komsu_m8():
    T = "komsu"
    K.KOMSU = []
    noktalar = [(k, x, z, "tasiyici_kiris_on" if z == Z_KIRIS_ON else "tasiyici_kiris_ac_arka") for k, x, z in M8_KAIDE] + \
               [("K", x, z, "tasiyici_capraz_2") for x, z in M8_K]
    for k, x, z, prn in noktalar:
        pr = K.TAS[prn]
        et = "%s_%d_%d" % (k, int(x), int(-z))
        pr.duvar_delik_nokta("+y", (x, Y_KIRIS[1], z), 11.0, tip="m8_percin_somun", not_="%s → B M8" % k)
        ps, c = S.percin_somun("M8", 2.0, (x, Y_KIRIS[1], z), (0, -1.0, 0), ad="govde_m8_%s" % et, birim=g.birim, kapali=True)
        eleman(ps, "B_TASIYICI", takim=T)
        K.GFRP_DELIK[prn].append((x, z, 16.5))
        delik(_tavan_paneli(x), (x, Y_UST, z), 9.0, tip="vida_deligi", parca="%s → B M8 (ISO 273 orta)" % k)
        K.KOMSU.append(dict(taraf={"A": "KAIDE_A", "C": "KAIDE_C", "K": "K_GOVDE"}[k], etiket=et, dunya=[x, Y_UST, z], b_tarafi="%s üst duvarında M8 perçin somun (kapalı uç · "
                            "köpükten önce) + GFRP'de Ø16,5 + tavan dış sacında Ø9" % prn, cıvata="karşı tarafın arayüzü (ISO 4762 M8 + DIN 125, üstten)"))
    # E ← B: E tabanındaki DIN 929 M8'e B'nin sağ dış sacından (E dosyası: B_M8_Z) · B tarafı yalnız Ø9
    for y, z in E_M8:
        delik(K.PANEL["yan_sag"]["yan"], (X1, y, z), 9.0, tip="vida_deligi", parca="B → E M8 (E tabanı DIN 929 · cıvata B içinden, Secop bölmesinden)")
        K.KOMSU.append(dict(taraf="E_GOVDE", etiket="E_%d" % int(-z), dunya=[X1, y, z], b_tarafi="sağ dış sacta Ø9", cıvata="E dosyasının arayüzü (ISO 4762 M8 × 16 + DIN 125 B içinden)"))
    # B → E üstte: çapraz_sag dış duvarında M8 perçin somun + ara pul + sağ sacta Ø9 · E sol sacında Ø9 (KARŞI DELİK)
    n0 = len(g.ELEMAN)
    for z in B_E_M8:
        r = GO.m8_noktasi(g, "E_ust_%d" % int(-z), K.TAS["tasiyici_capraz_sag"], z, "+x", K.PANEL["yan_sag"]["yan"], "E_GOVDE sol_sac_pizza_penceresi",
                          karsi_kod="E", karsi_t=1.5, vida_boy=25, kayma=-8.0, yer="tasiyici_capraz_sag")
        K.KOMSU.append(dict(taraf="E_GOVDE", etiket=r["etiket"], dunya=r["dunya"], b_tarafi="çapraz_sag dış duvarında M8 perçin somun + ara pul %.2f + sağ sacta Ø9" % r["ara_pul"],
                            cıvata="B'nin arayüzü: ISO 4762 M8 × 25 + DIN 125 E'nin içinden · E sol sacında Ø9 GEREKİR"))
    for p in g.ELEMAN[n0:]:
        _kaydet(p["ad"], "B_TASIYICI", "SABIT", p.get("mal") or "celik", T)


def avara_saplamalari():
    """avara kolu ön flanşı (mekanizma) çerçeveye 2 × PEM FHP-M3 (store_cad_v14'te FH4-M3 → standartta yasak, FHP) · somun + pul mekanizma tarafının"""
    T = "on_cerceve"
    for kol, kod, tip, x0, yo in CEK:
        y1 = yo + HH_C[kod]
        ust = min(y1 + 1.0 + KOL_FLANS_Y, TAVAN_KOL[kol] - 1.0)
        for j, yy in enumerate((y1 + 6.0, min(y1 + 16.0, ust - 4.0))):
            p = (x0 + 7.35, yy, Z_CER1)
            par = [(a, P_) for a, (s_, P_, poly) in K.CER.items() if _icinde_poly(poly, p[0], p[1])]
            assert par, ("avara saplaması çerçeve dışında", kod)
            P_ = par[0][1]
            sp, c = S.pem_saplama("FHP", "M3", 8, p, (0, 0, -1.0), ad="onyuz_cerceve_avara_%s_%d" % (kod, j), birim=g.birim, sac_ad=par[0][0])
            u_, v_ = uv(P_, p)
            P_.delik(u_, v_, c["delik"], tip="pem_saplama", parca=sp["meta"]["parca"], pem_tip="FHP", kenar_min=c["kenar"], min_sac=c["min_sac"])
            eleman(sp, takim=T)
            arayuz(S.somun("ISO4032", "M3", (p[0], yy, Z_CER0 - 2.0 - 0.5), (0, 0, -1.0), ad="arayuz_%s_avara_%d_somun" % (kod, j), birim=g.birim),
                   "%s_avara_kolu (mekanizma)" % kod, "avara kolu ön flanşında Ø3,4 (aynı eksen) · DIN 125 M3 + ISO 4032 M3 kolun arkasından", "mekanizma sahibi")


# =====================================================================================================================================
# 10 · PU KÖPÜK (yerinde enjeksiyon · bloklar gövde katılarından kesilerek)
# =====================================================================================================================================
ELK_KES = {"tavan_pu_T": [(2419.5, 2503.0, 742.5, 788.5, -761.5, -558.5)], "bolme_4_pu": [(3990.0, 4032.0, 742.5, 785.5, -761.5, -640.5)]}


def pu_bloklari():
    bom = ("PU köpük gövde (yerinde enjeksiyon · siklopentan · 40 kg/m³)", 1, "tek atım (gövde + bölmeler), çekmece önleri ayrı kalıpta", "yan 60 · tavan 57,5 / 117,5 / 59 · taban 38,8 · arka 37,3")
    pu("yan_pu_sol", (X0 + 1.5, KOLON_X["K1"] - T_IC, Y_ALT + 1.5, Y_UST - 1.5, Z_DONUS_ARKA, Z_ON0 - 1.5), bom=bom)
    pu("tavan_pu_57.5", (X0 + 1.5, X_ALCAK, Y_TAVAN + T_IC, Y_UST - 1.5, Z_DONUS_ARKA, Z_ON0 - 1.5))
    pu("tavan_pu_T", (X_ALCAK, XF[0], Y_TAVAN_F + T_IC, Y_UST - 1.5, Z_DONUS_ARKA, Z_ON0 - 1.5))
    pu("tavan_pu_F", (XF[0] + T_IC, BOLME_X[4], Y_TAVAN_F + T_IC, Y_TAVAN, Z_DONUS_ARKA, Z_ON0 - 1.5))
    pu("taban_pu", (X0 + 1.5, T0, Y_ALT + 1.5, Y_TABAN - T_IC, Z_DONUS_ARKA, Z_ON0 - 1.5))
    pu("arka_pu_37.5", (X0 + 1.5, XF[0], Y_TABAN - T_IC, Y_UST - 1.5, Z_DONUS_ARKA, Z_ARKA_IC - T_IC))
    pu("arka_pu_F", (XF[0], BOLME_X[4] + T_IC, Y_TABAN - T_IC, Y_TAVAN + T_IC, Z_DONUS_ARKA, Z_ARKA_IC - T_IC))


def _gov_sekilleri():
    out = []
    for s in g.SAC:
        for p in s.parcalar(): out.append((p["ad"], GO._sekil(p)))
    for p in g.PROF.values(): out.append((p.ad, p.kati()))
    for p in g.ELEMAN + g.KAYNAK: out.append((p["ad"], GO._sekil(p)))
    return out


def pu_kur():
    T0_ = time.time()
    gs = _gov_sekilleri()
    bb = [(a, s, s.BoundingBox()) for a, s in gs]
    K.PU_SH = collections.OrderedDict()
    onceki = []
    for ad, d in K.PU.items():
        k = d["k"]
        sh = kutu(*k)
        kb = sh.BoundingBox()
        tools = [s for a, s, b in bb if GO.bbk(kb, b, -1e-4)]
        tools += [s for a_, s in K.PU_KES if a_ == ad]
        tools += [kutu(*e) for e in ELK_KES.get(ad, [])]
        tools += [s for s in onceki if GO.bbk(kb, s.BoundingBox(), -1e-4)]
        if tools:
            sh = sh.cut(*tools)
        sh = sh.clean()
        K.PU_SH[ad] = sh
        onceki.append(sh)
        v = sh.Volume() / 1e6
        p = g.ozel(ad, sh, "PU (yerinde enjeksiyon)", (d["bom"] or ("PU köpük",))[0], "%.2f L · %.2f kg" % (v, v * 0.040), malzeme="PU 40 kg/m³", mal="pu", uretim=True,
                   tur="pu", meta=dict(hacim_L=round(v, 3), kg=round(v * 0.040, 3)))
        g.ELEMAN.append(p); p["birim"] = g.birim
    g.not_("PU blokları gövde katılarından (sac, profil, bağlantı, kaynak) + geçişlerden + elektrik deliklerinden kesildi (%d blok · %.1f sn)" % (len(K.PU), time.time() - T0_))


# =====================================================================================================================================
# 11 · KURULUM + MONTAJ SÖZLEŞMESİ (SC.PARCALAR: ad · wp · mal · birim · grup · bom) + uygula + ad eşleme
# =====================================================================================================================================
ADIMLAR = ("alt_sase", "tasiyici", "dis_kabuk", "dis_kabuk_baglanti", "ic_kabuk", "teknik", "on_cerceve", "cekmeceler", "mekanizma_somunlari", "komsu_m8",
           "avara_saplamalari", "gfrp_seritleri", "pu_bloklari", "pu_kur")


def kur(adimlar=ADIMLAR, log=print):
    global g
    if K.kuruldu and tuple(adimlar) == ADIMLAR: return g
    t0 = time.time()
    g = GO.Govde("B_KASA", SURUM, istasyon="B", cerceve=CER)
    for a in ("BIRIM", "GRUP", "MAL"): setattr(K, a, {})
    K.PANEL = {}; K.TAKIM = collections.OrderedDict(); K.PU = collections.OrderedDict(); K.PU_KES = []; K.PU_SH = collections.OrderedDict()
    K.CER_DESTEK = []
    for a in adimlar:
        t1 = time.time(); globals()[a](); log("   %-22s %.1f sn" % (a, time.time() - t1))
    K.kuruldu = tuple(adimlar) == ADIMLAR
    log("%s · kuruldu: %d sac · %d profil · %d eleman · %d kaynak · %d birleşim · %d arayüz · %d PU · %.1f sn"
        % (SURUM, len(g.SAC), len(g.PROF), len(g.ELEMAN), len(g.KAYNAK), len(g.BIRLESIM), len(g.ARAYUZ), len(K.PU_SH), time.time() - t0))
    return g


_kur_test = lambda adimlar=ADIMLAR: kur(adimlar)


def _sahip(ad):
    """parça adı → (birim, grup, mal) · sac köşe kaynakları sacın kaydını alır"""
    if ad in K.BIRIM: return K.BIRIM[ad], K.GRUP[ad], K.MAL.get(ad, "sac")
    m = re.match(r"(.+)_kose_kaynagi_\d+$", ad)
    if m and m.group(1) in K.BIRIM: return K.BIRIM[m.group(1)], K.GRUP[m.group(1)], "sac"
    raise KeyError("birimi kayıtsız parça: %s" % ad)


def govde_parcalari_b():
    """montaja girecek gövde parçaları (arayüz elemanları HARİÇ) · DÜNYA (B = dünya) · her parçanın kendi birimi / grubu"""
    kur()
    L = []
    for s in g.SAC: L += s.parcalar()
    L += [p.parca() for p in g.PROF.values()] + g.ELEMAN + g.KAYNAK
    out = []
    for p in L:
        sh = GO._sekil(p)
        b, gr, mal = _sahip(p["ad"])
        q = dict(ad=p["ad"], wp=cq.Workplane("XY").add(sh), mal=mal if mal in ("sac", "kabuk", "celik", "pu", "koyu", "conta") else "celik", grup=gr, birim=b,
                 bom=tuple(p["bom"]) if p.get("bom") else None, kaynak=SURUM, tur=p.get("tur", "sac"))
        if p.get("sac"): q["sac"] = p["sac"]
        if p.get("meta"): q["meta"] = p["meta"]
        out.append(q)
    adlar = [q["ad"] for q in out]
    assert len(adlar) == len(set(adlar)), "çift ad: %s" % sorted(a for a in set(adlar) if adlar.count(a) > 1)
    return out


def _cek_eski(kod):
    return [kod + s for s in ("_on_dis_sac_1.5", "_on_pu", "_on_ic_sac_1.0", "_kutu_2.0_1.0", "_kutu_arka_1.0", "_kutu_on_1.0", "_on_baglanti_sol", "_on_baglanti_sag",
                              "_ray_adaptor_sol", "_ray_adaptor_sag")]


ESKI_B_KASA = (["ayak_%d" % i for i in range(14)] +
               ["kasa_yan_dis_sac_sol", "kasa_yan_dis_sac_sag", "tavan_dis_sac", "taban_dis_sac", "arka_dis_sac", "kasa_yan_on_donus_sol", "kasa_yan_on_donus_sag",
                "yan_ic_sac_sol", "tavan_ic_sac", "tavan_ic_sac_F", "tavan_on_donus", "taban_ic_sac", "taban_on_donus", "arka_ic_sac", "arka_ic_sac_F"] +
               ["bolme_%d_%s" % (i, k) for i in range(5) for k in ("sac_a", "sac_b", "pu")] +
               ["isi_kalkani_ayirma_saci", "isi_kalkani_sol_sac", "isi_kalkani_isinim_saci"] + ["isi_kalkani_takozu_%d" % i for i in range(12)] +
               ["yan_pu_sol", "yan_pu_sol_on", "tavan_pu_57.5", "tavan_pu_T", "tavan_pu_F", "taban_pu", "arka_pu_37.5", "arka_pu_F", "tk_ara_pu", "tk_depo_arka_pu",
                "tk_depo_sag_pu", "tk_depo_tavan_pu", "onyuz_cerceve_saci_1.0"])
ESKI_B_TASIYICI = ["tasiyici_kiris_on", "tasiyici_kiris_arka", "tasiyici_capraz_uc", "tasiyici_capraz_0", "tasiyici_capraz_1", "tasiyici_capraz_2"] + \
                  ["tasiyici_dikme_%d" % i for i in range(6)]
ESKI_B_SOGUTMA = ["tk_ara_sac_alt", "tk_ara_sac_ust", "sogutma_grubu_montaj_rayi_arka", "sogutma_grubu_montaj_rayi_on", "tk_kapak_sogutma_dis_sac"] + \
                 ["tk_panel_klipsi_%d" % i for i in range(4)]
ESKI_B_DEPO = ["tk_depo_arka_sac_on", "tk_depo_arka_sac_arka", "tk_depo_sag_ic_sac", "tk_depo_tavan_ic_sac", "tk_depo_kutu_U_1.5", "tk_depo_kutu_arka_1.5",
               "tk_depo_kutu_on_1.5", "tk_depo_on_baglanti_sol", "tk_depo_on_baglanti_sag", "tk_depo_ayirici_1.5", "tk_depo_kapak_1.0", "tk_kapak_depo_dis_sac_1.5",
               "tk_kapak_depo_pu", "tk_kapak_depo_ic_sac_1.0"]
ESKI_GOVDE = tuple(ESKI_B_KASA + ESKI_B_TASIYICI + ESKI_B_SOGUTMA + ESKI_B_DEPO + [a for c in CEK for a in _cek_eski(c[1])])
ESLEME = {"tavan_ic_sac": "ic_kabuk_K1 + ic_kabuk_K2 (U: taban + arka + tavan tek parça)", "tavan_ic_sac_F": "ic_kabuk_K3 + ic_kabuk_K5 + ic_kabuk_K6",
          "taban_ic_sac": "ic_kabuk_K1 … ic_kabuk_K6 (taban kanadı + eşik)", "arka_ic_sac": "ic_kabuk_K1 + ic_kabuk_K2", "arka_ic_sac_F": "ic_kabuk_K3 + ic_kabuk_K5 + ic_kabuk_K6",
          "tavan_on_donus": "tavan_dis_sac_A + tavan_dis_sac (ön dönüş bükümlü)", "taban_on_donus": "taban_dis_sac_A + taban_dis_sac (ön dönüş bükümlü)",
          "kasa_yan_on_donus_sol": "kasa_yan_dis_sac_sol (ön dönüş bükümlü)", "kasa_yan_on_donus_sag": "kasa_yan_dis_sac_sag (ön dönüş bükümlü)",
          "arka_dis_sac": "arka_dis_sac (x 1500–4400) + arka_dis_sac_A (736–1500)", "tavan_dis_sac": "tavan_dis_sac (x 1500–4400 · elektrik delikleri burada) + tavan_dis_sac_A",
          "taban_dis_sac": "taban_dis_sac (x 1500–4400 · emiş + elektrik girişi burada) + taban_dis_sac_A", "yan_pu_sol_on": "yan_pu_sol",
          "onyuz_cerceve_saci_1.0": "onyuz_cerceve_saci_1.0 (x 770–2090,75) + onyuz_cerceve_saci_1.0_F (2091,25–4370)",
          "tk_depo_kutu_U_1.5": "tk_depo_kutu_halka_1.5 + tk_depo_kutu_taban_1.5", "tk_depo_kutu_arka_1.5": "tk_depo_kutu_halka_1.5 (U: arka + iki yan)"}
for _c in CEK:
    _k = _c[1]
    ESLEME.update({_k + "_kutu_2.0_1.0": "%s_kutu_halka_1.0 + %s_kutu_taban_2.0" % (_k, _k), _k + "_kutu_arka_1.0": _k + "_kutu_halka_1.0",
                   _k + "_kutu_on_1.0": _k + "_kutu_halka_1.0"})
ISARET = "ic_kabuk_K1"


def _fitil_v37(SC_L):
    """h3_kapak_v1.bolge_B_sag'ın depo fitili adımı (alt bacak +8) — o çağrı yama ile kalkıyor, fitil (mekanizma) aynen korunur"""
    fl = [p for p in SC_L if p["ad"] == "tk_kapak_depo_fitil"]
    assert len(fl) == 1, "tk_kapak_depo_fitil yok"
    p = fl[0]; f = GO._sekil(p); bf = f.BoundingBox()
    if bf.ymin > DEPO_ACIK[2] - FITIL_G - 10.5 + DEPO_FITIL_DY - 0.5: return False          # zaten +8
    dy = DEPO_FITIL_DY
    alt = f.intersect(kutu(bf.xmin - 1, bf.xmax + 1, bf.ymin - 1, bf.ymin + 15.0, bf.zmin - 1, bf.zmax + 1)).translate(V(0, dy, 0))
    p["wp"] = cq.Workplane("XY").add(f.intersect(kutu(bf.xmin - 1, bf.xmax + 1, bf.ymin + dy, bf.ymax + 1, bf.zmin - 1, bf.zmax + 1)).fuse(alt).clean())
    return True


def uygula_sc(SC, rapor=None):
    """montaj: SC.modul() + plint silme SONRASI (h3_kapak_v1.bolge_B_sag YERİNE) · eski gövdeyi çıkarır, üretim sacı gövdesini koyar · idempotent"""
    L = SC.PARCALAR
    if any(p["ad"] == ISARET for p in L): return L
    var = set(p["ad"] for p in L)
    eksik = [a for a in ESKI_GOVDE if a not in var]
    assert not eksik, ("h3_b_sac_v1: eski gövde parçası yok", eksik[:10], len(eksik))
    yeni = govde_parcalari_b()
    L[:] = [p for p in L if p["ad"] not in set(ESKI_GOVDE)]
    cak = set(p["ad"] for p in L) & set(q["ad"] for q in yeni)
    assert not cak, ("h3_b_sac_v1: mekanizmayla ad çakışması", sorted(cak)[:10])
    bilinmeyen = [q["ad"] for q in yeni if not q["ad"].startswith(GOVDE_ONEK)]
    assert not bilinmeyen, ("h3_b_sac_v1: B gövde önekine uymayan ad", bilinmeyen[:5])
    f = _fitil_v37(L)
    L.extend(yeni)
    if rapor is not None:
        rapor.append("B üretim sacı gövdesi: −%d eski · +%d yeni (h3_b_sac_v1)%s" % (len(ESKI_GOVDE), len(yeni), " · depo fitili alt bacağı +8 (v3.7)" if f else ""))
    return L


def hareketli(p):
    """çekmeceyle hareket eden gövde parçası mı (grup CEKMECE)"""
    return p.get("grup") == "CEKMECE"


def _cikti_klasoru():
    S_ = os.environ.get("B_SAC_CIKTI") or os.path.abspath(os.path.join(H3, "..", "..", "..", "..", "sac_b"))
    os.makedirs(os.path.join(S_, "acinim"), exist_ok=True)
    return S_


if __name__ == "__main__":
    sys.path.insert(0, _cikti_klasoru())
    import b_sac_denetim_v1 as DEN                                            # <scratchpad>/sac_b/b_sac_denetim_v1.py (yalnız denetim + çıktı)
    DEN.calistir()
    sys.stdout.flush(); os._exit(0)
