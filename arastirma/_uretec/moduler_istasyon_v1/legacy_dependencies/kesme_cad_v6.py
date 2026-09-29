# -*- coding: utf-8 -*-
"""AUTOKITCH · K · KESME + TEREYAĞI SPREYİ İSTASYONU — ÜRETİM MODELİ v6 (28 Eyl 2026 gece): ÖN DÜZLEM +79 · TEMİZ KUTU (SPEC_on_duzlem_v63 §2.5 · Kemal:
"fırının ön yüzü sınır yüzey … her şeyi extend edip kapak takacaksın … bulaşık makinesi önüne kapak, alt ayaklarını kaldır … içeride havada kalan parça olmasın").
Kabuk ön kenarı +59 · ön çerçeve (2 kesintisiz dikme + 4 kayıt) · 3 tava kapak (304 fırçalı 1,5 · 20 büküm · z +59…+79 · SOL gizli menteşe, bas-aç,
ORTA + ÜST AZM40 kilitli; önden YALNIZ düz yüzey + derz — lazer yarık yalnız SEÇENEK: YARIK_ACIK) ayrı hareketli gruplar · plint y 0–123 · x 0–600 · +17,5…+19 ·
köprü kirişleri uç plakalarıyla yan saclara + ön dikmeye · bulaşık bulasik_cad_v2 (ayaksız) 40×20×2 kirişli 3 mm tablaya oturur (+13), bağlantıları taban
sacındaki rakorlu geçişlerden çıkar · havada kalan 17 bileşen bağlandı (0) · hava_besleme_K silindi · TAM İSTİSNASIZ çakışma taraması 0 (ISTISNA listesi boş).
Ürün yolu, kotlar, kinematik, E arayüzü v5 ile AYNI (ölçülür; E v7 ileri uyum da). Üretici: yap_kesme_v6.py (2. tur: denetçi düzeltmeleri). Önceki: kesme_cad_v5.py
v5 (27 Eyl 2026 gece): DETERJAN + PARLATICI KALKTI (Kemal: "deterjanları makinenin
arkasına koyma, tabii şimdilik sil") — bulaşığın arkasındaki kanister rafı (y 325–330) + 2 konsol + deterjan / parlatıcı bidonları + kapakları + 2 dozaj
emiş hortumu (9 parça, hepsi "deterjan_") ve YALNIZ onlar için eklenen sabitler, malzemeler, BOM anahtarı ve denetimler silindi. Bulaşık makinesinin yeri
AYNI (BULASIK_YER); arkası + MEIKO arka payı artık BOŞ (ölçülür). v4 ↔ v5 parça parça karşılaştırılır (yalnız deterjan_ çıktı). E arayüzü kutu_cad_v6
(E'nin ön alt sacı kalktı; kotlar / pencere / kinematik aynı). Deterjanın yeri AÇIK (karar Kemal'de). Üretici: yap_kesme_v5.py. Önceki: kesme_cad_v4.py
v4 (27 Eyl 2026): ALÇAK HAT (SPEC_alcak_hat_v57) — y 700–868 dilimi çıkarıldı,
her şey 168 aşağı (üst 1862 · taban 892 · bant 996); altında bulaşık makinesinin yeri + arkasında deterjan / parlatıcı rafı. Üretici: yap_kesme_v4.py. Önceki: kesme_cad_v3.py
v3 (27 Eyl 2026): yağ tankı + pano YUKARIDA (köprünün arkası), taban dolabı BOŞ (içecek kolileri fırın üstüne) — Kemal. Önceki: kesme_cad_v2.py
v2 (27 Eyl 2026): ÖN KAPAKLAR YOK (Kemal) — taban kapısı, PC pencereli
üst kapı, kulplar, AZM kilidi ve ön acil stop kaldırıldı; ön yüz açık (TOPPING gibi: "kapaklar en son"). Önceki: kesme_cad_v1.py
v1 (25 Eyl 2026):

Kemal: "her şeyi araştır, full detaylı yap, modelle. Kesme ve spreyi aynı yerde çalışır şekilde, üretilir şekilde araştır ve
modelle, animasyonuyla tüm detaylarıyla yap."

ÇALIŞMA (20 sn çevrim, kutu modülünün saati ile AYNI — E pizzayı 8,5 sn'de bekliyor):
  0,3–2,3  ürün fırın bandından K BANDINA geçer, bant onu kesme merkezine (x 300) getirir, fotosel durdurur.
           NEDEN BANT: fırın bandı PTFE (kayganlık ~0,15), düz sac plaka ~0,35 → ürün, ağırlığının ~%70'i hâlâ fırın
           bandındayken durur, arka kenarı fırının içinde kalır. İki bant arası aktarma (ikisi de tahrikli) güvenilir.
           Aynı ilke: Q-T-S PC5000 otomatik pizza kesici (poliüretan bantlı konveyör, 40 pizza/dk).
  2,6–3,8  SPREY (yalnız pide): tereyağı, bıçak yıldızının GÖBEĞİNDEKİ nozülden, kafa yukarıdayken. Bıçaklar göbekten çıkan
           ışınlara paralel olduğu için gölge yapmaz (1,5 mm × 6 → alanın %1–3'ü).
  4,0–6,5  KESME: kafa hızlı iner (95 mm), yavaş keser (30 mm), bıçak bandın 0,5 mm üstünde mekanik dayamada durur
           ("bıçak izi yeter"), kalkar. 6 dilim.
  6,8–7,8  bant ürünü 300 → 500 taşır; ön ÇİT (20°) ürünü 36 mm içeri kaydırır (E'nin kutu ekseni z −206). Aynı anda itici
           (yukarıda) ürünün üstünden geri gelir, 7,95–8,3 arkasına iner.
  8,5–10,1 İTİCİ ürünü E'ye sürer (merkez 500 → 860, kutu modülünün beklediği zaman ve yol); 10,3–10,9 geri, 11,0 kalkar.

KOORDİNAT (modül yereli): x 0..600 (hatta 4000 + x) · y yerden (v4: 0..1862) · z 0 ön yüz, −830 arka. E modülü x 600'den başlar.
STANDART ÜRÜNLER (kaynaklar arastirma/4_KESME_v1 BOM'da): Festo DGRF-C-63-125 temiz tasarım kılavuzlu silindir (6 bar 1870 N) ·
Spraying Systems PulsaJet AA10000AUH-104210 (gıda) + UniJet TG tam koni uç · Interroll RollerDrive EC5000 24 V Ø50 ·
igus drylin ZLW-1040 dişli kayışlı eksen + AutomationDirect STP-MTR-23079 · SMC MGPM20-60 kılavuzlu silindir ·
Siemens S7-1200 · Mean Well NDR-240 · Omron E3Z / E2E · Elesa LV.A ayak. Ölçüsü teyit edilmeyenler [V].
"""
import csv, io, json, math, os, struct, sys, time
import cadquery as cq

U = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.dirname(os.path.dirname(U))
sys.path.insert(0, U)
import kutu_cad_v6 as KC                                   # v5: kutu_cad_v6 (E'nin ön alt sacı kalktı · kotlar / pencere / kinematik v5 ile aynı) · v4: ALÇAK HAT E'si (v3 yanlışlıkla kutu_cad_v3'ü alıyordu) · ortak geometri yardımcıları + E'nin kendisi (arayüz ve tarama)
import bulasik_cad_v2 as BM                                # v6: ayaksız (tablaya oturur, +13) · sepet rayları + kol göbek boruları · v4: K altındaki bulaşık makinesi (ayrı modül; burada yalnız REF + yer denetimi)
import topping_cad_v22 as TC
from kaset_3d_v3 import Mesh, MM, MALZEME

for _k, _v in {"pu_bant": ((0.95, 0.95, 0.93, 1.0), 0.0, 0.55), "pc": ((0.80, 0.88, 0.95, 0.18), 0.0, 0.05),
               "tereyag": ((0.98, 0.86, 0.42, 1.0), 0.0, 0.5), "hortum_isi": ((0.85, 0.20, 0.15, 1.0), 0.0, 0.6),
               "hava": ((0.15, 0.40, 0.85, 1.0), 0.0, 0.5), "kasar_ust": ((0.96, 0.85, 0.50, 1.0), 0.0, 0.8),
               "kesik": ((0.35, 0.22, 0.12, 1.0), 0.0, 0.9), "kirmizi": ((0.80, 0.12, 0.10, 1.0), 0.1, 0.5), "siyah": ((0.07, 0.07, 0.08, 1.0), 0.1, 0.6)}.items():
    MALZEME.setdefault(_k, dict(renk=_v[0], met=_v[1], ruf=_v[2], saydam=_v[0][3] < 1.0))
MALZEME.setdefault("sprey", dict(renk=(0.98, 0.88, 0.45, 0.30), met=0.0, ruf=0.6, saydam=True))
MALZEME.setdefault("pom", dict(renk=(0.95, 0.95, 0.93, 1.0), met=0.0, ruf=0.42))
MALZEME.setdefault("conta", dict(renk=(0.90, 0.90, 0.88, 1.0), met=0.0, ruf=0.8))     # v6 2. tur: EPDM dayama lastiği / geçiş lastikleri (store / kutu ile aynı anahtar)
# v5: v4'ün kanister / mavi_kapak / dozaj malzemeleri kalktı (deterjan + parlatıcı bidonları ve dozaj hortumları yok)

kut, silx, sily, silz = KC.kut, KC.silx, KC.sily, KC.silz
boru_y = KC.boru_y

# ---------------------------------------------------------------- ÖLÇÜLER ----------------------------------------------------------------
W, H, D = 600.0, 1862.0, 830.0     # v4 ALÇAK HAT: 2030 − 168
DILIM_Y0, DILIM_DY = 700.0, 168.0  # v4: v3'ten çıkarılan yatay dilim y 700–868 (bandı yalnız 3 sac + 4 dikme geçer; hava besleme ucu 1040 > 868)
SAC = 1.5
Y_PLINT = 123.0                   # alt taban çizgisi (bütün istasyonlar) [K: kural kitabı 4]
H_B = 892.0                       # istasyon tabanı (sacın altı; sac 892–895) [K] · v4: 1060 − 168 = 788 düz çizgi + 104 kaide
BANT = 996.0                      # K bandı üstü = kesme yüzeyi (fırın bandı 998'in 2 mm altı) [K: kot zinciri] · v4: 1164 − 168
FIRIN_BANDI = 998.0               # v4: firin_tp10_cad_v7 BANT_UST_HAT (1166 − 168)
XC, ZC = 300.0, -170.0            # kesme merkezi (E'nin beklediği pizza yeri: hat 4300, z −170) [K: kutu_cad_v3]
X_TASI = 500.0                    # kesimden sonra bandın taşıdığı yer (itici buradan iter)
X_SON = 860.0                     # E'nin kutu merkezi (E yereli 260) [K: kutu_cad_v3 pizza_trs]
X_OLU = 597.0                     # ölü plakanın ucu (ürün bu kenarı geçince köprüye iner)
ZB = KC.ZB                        # −206 · kutu ekseni
PZ_R, PZ_H = 150.0, 15.0          # ürün zarfı Ø300 × 15 (E'nin pizza modeliyle aynı) [K]
E_PENCERE = (BANT - 18.0, BANT + 66.0, -372.0, -24.0)   # E sol duvarındaki pizza penceresi y0 y1 z0 z1 = 978–1062 [K: kutu_cad_v6.PENCERE, v5 ile aynı] · v3'te 1146–1230 sabitti
URUN_GIRISI = (BANT - 64.0, BANT + 76.0, -420.0, -8.0)  # v4: sol duvardaki fırın bandı / ürün girişi y0 y1 z0 z1 = 932–1072 (v3 1100–1240 sabitti) — montajdaki _ka

# ---------------------------------------------------------------- v6 · ÖN DÜZLEM +79 (SPEC_on_duzlem_v63 §1 + §2.5) ----------------------------------------------------------------
Z_ON = 79.0                       # ön düzlem = fırın gövdesinin ön yüzü (montaj sözleşmesi: KS.Z_ON = FT.ZS = 79) — bütün kapakların DIŞ yüzü
Z_ARKA = -D                       # −830 SABİT (arka dış sac yerinde) → gövde derinliği 909
TAVA_T, TAVA_D = 1.5, 20.0        # tava panel: 304 fırçalı 1,5 · kenarlar 20 arkaya bükülü (kuru istasyon kapağı, SPEC §1)
Z_TAVA = (Z_ON - TAVA_D, Z_ON)    # (+59 · +79)
Z_KABUK_ON = Z_TAVA[0]            # kabuk (sol, sağ, üst, taban sacı, istasyon tabanı) ön kenarı +59 = kapak arkası
DERZ = 3.0                        # panel ↔ panel, kapak ↔ kapak, istasyon ↔ istasyon
CER = 30.0                        # ön çerçeve profili 30 × 30 × 2
Z_CER = (Z_TAVA[0] - 2.0 - CER, Z_TAVA[0] - 2.0)   # (+27 · +57): kapak arkasıyla 2 mm = bas-aç mandal stroku
CER_X_SOL = (SAC, SAC + CER)      # 1,5–31,5
CER_X_SAG = (570.0, W - SAC)      # 570–598,5 (SPEC): 28,5 geniş → bükme kutu; bulaşık kapak zarfına (568,5) 1,5 pay
Y_CER = (Y_PLINT + 3.0, H - SAC)  # 126–1860,5 kesintisiz (taban sacı üstü → üst sac altı)
KAYITLAR = (("alt", Y_CER[0], Y_CER[0] + CER), ("883", 862.0, 892.0), ("1306", 1291.5, 1321.5), ("ust", Y_CER[1] - CER, Y_CER[1]))   # derz çizgilerinin arkasında
KAPAK_X = (DERZ, W - DERZ / 2.0)  # 3,0–598,5 (dünya 4003–4598,5): fırın / dolap yüzü 4000 → derz 3 · E kapakları 4601,5 → derz 3
X_E_KAPAK0 = 4601.5               # E kapaklarının sol kenarı (SPEC §1 dikey derzler: E 4601,5–5430)
KAPAKLAR = (("KAPAK_ALT", "alt", Y_PLINT + DERZ, 883.0), ("KAPAK_ORTA", "orta", 886.0, 1305.0), ("KAPAK_UST", "ust", 1308.0, H - DERZ))   # yatay derzler 883/886 · 1305/1308 · üst 1859
KAPAK_GRUP = tuple(k_[0] for k_ in KAPAKLAR)
SABIT_GRUP = ("SABIT",) + KAPAK_GRUP  # makine çalışırken kapaklar KAPALI → çakışma taramasında sabit gibi
MENTESE_EKSEN = (KAPAK_X[0], Z_ON)    # SOL gizli menteşe, sanal pivot = kapağın ön-sol köşesi (x 3, z 79) · dikey eksen
KAPAK_MAX = 90.0                  # EMKA 1046-U5 en çok 90° (emka.com)
MENTESE = dict(x=(8.0, 24.0), boy=79.0)          # EMKA 1046-U5 zarfı: boy ≈ 79 · pim Ø16 (GlobalSpec föyü) · genişlik 16 · kanat derinliği VARSAYIM
MENTESE_Y = {"alt": (226.0, 783.0), "orta": (986.0, 1205.0), "ust": (1408.0, 1759.0)}   # kapak kenarından 100
MANDAL = dict(x=(578.0, 592.0), boy=44.0, derin=14.0)   # Southco E4 dokun-aç mandal zarfı 14 × 44 × 14 VARSAYIM (sağ dikmenin ön yüzünde)
AZM = dict(boy=119.5, en=40.0, kal=20.0)          # Schmersal AZM40 119,5 × 40 × 20 (schmersal.com)
AZM_KAPAK = ("orta", "ust")                       # ORTA: bıçak + itici · ÜST: kılavuz mili uçları, tank (45 °C), pano
AZM_AGIZ = 8.0                    # 2. tur: kilit dili AZM40 giriş ağzına 8 mm girer (v6-1: dil z 59,5'te bitiyordu, kilide 2,5 mm — ulaşmıyordu) · ağız yeri/derinliği VARSAYIM (Schmersal çizimiyle teyit)
YARIK_ACIK = False                # 2. tur (denetçi ORTA-2): SPEC §1 "önden yalnız düz yüzey + derz" → VARSAYILAN YARIKSIZ · True = SEÇENEK (ısı kararıyla birlikte Kemal'e soruldu)
YARIK = dict(en=3.0, boy=40.0, adim=10.0, n=52,   # SEÇENEK: lazer yarık 3 × 40 (ISO 13857: e ≤ 4 → parmak geçmez), adım 10, sırada 52 · desen kapakta ORTALI (x0 44,25; v6-1 40 → 4,25 sola kaymıştı)
             bant={"alt": ((197.0, 237.0), (247.0, 287.0), (722.0, 762.0), (772.0, 812.0)),        # ALT: alt emiş · üst atış · paylar 71 / 71 (üst bant dayama lastiğinin 814–844 altında biter)
                   "ust": ((1330.0, 1370.0), (1380.0, 1420.0), (1747.0, 1787.0), (1797.0, 1837.0))})  # ÜST: paylar 22 / 22
DAYAMA = dict(x=(108.5, 568.5), y=(814.0, 844.0), t=3.0)   # 2. tur (denetçi K-11): ALT kapağın iç yüzünde EPDM dayama lastiği — bulaşık kapağının üst kenarı (x 110,5–566,5) buna dayanır, 1,5 sac değil
U_KAPALI = 5.0                    # W/m²K VARSAYIM (iyimser): kapalı bölmenin ön kapaktan ısı geçişi (doğal taşınım ~4 + ışınım, iç direnç yok sayıldı)
PLINT_FLANS = 15.0                # 2. tur (denetçi K-4): plint üst flanşı 15 (taban sacına M5 perçin somunu)
Z_PLINT = (Z_ON - 60.0 - TAVA_T, Z_ON - 60.0)    # (+17,5 · +19) — ön düzlemin 60 gerisi, bütün hat boyunca tek çizgi
RHO_304 = 7.93e-6                 # kg/mm³
E_304 = 193000.0                  # N/mm²
Q_BULASIK_W = 300.0               # VARSAYIM: MEIKO tezgâh altı makinenin duyulur ısı yayımı (föyde yok) — ısı tahmini için
Q_UST_W = 100.0                   # VARSAYIM: pano (~40) + tank ısıtıcısı ortalaması (~30) + ısıtmalı hortum / nozül (~30) · fırın ağzı sızıntısı BİLİNMİYOR
BULASIK_KG = 90.0                 # VARSAYIM: 70 kg (föy) + su + sepet + yük
V6_DEGISEN = ("taban_sac_3", "istasyon_tabani_3", "ust_sac", "sol_sac_urun_girisi", "sag_sac_E_penceresi", "kopru_kirisi_0", "kopru_kirisi_1", "olu_plaka",
              "yag_tanki_rafi", "yag_tanki_rafi_koseben", "yag_tanki_isitici_ceketi", "PulsaJet_isitici_ceket", "kesici_reed_0", "kesici_reed_1",
              "hava_hortumu_kaldirma", "hava_hortumu_tank",
              # 2. tur (denetçi ORTA-1 + K-9): kanal dikmenin önüne · eski gömülü örtüşmeler delik / yuva ile giderildi (işlev ve zarf aynı)
              "kablo_kanali_dikey", "yag_tanki_kelepcesi", "eksen_ayagi_1", "tahrik_rulosu_RollerDrive_EC5000", "kuyruk_rulosu", "bant_yan_levhasi_0",
              "bant_yan_levhasi_1", "bicak_gobek_halkasi", "sprey_dirsegi", "surucu_STP-DRV-4830") + tuple("koruma_braketi_%d" % _i for _i in range(6))   # + bütün REF_bulasik_ parçaları (+13 y)
              # (bant_PU_2mm de kesildi — 9,3 mm³, dilim_v1'in hacim eşiğinin altında "birebir" sayılır; V6_DELIK denetiminde ölçülür)
V6_DELIK = ("tahrik_rulosu_RollerDrive_EC5000", "kuyruk_rulosu", "bant_yan_levhasi_0", "bant_yan_levhasi_1", "bant_PU_2mm", "bicak_gobek_halkasi", "surucu_STP-DRV-4830",
            "yag_tanki_kelepcesi", "eksen_ayagi_1")    # 2. tur: yalnız delik / yuva / kesim — sınır kutusu v5 ile AYNI, hacim yalnız azalır (denetimde ölçülür)
V6_CIKAN = ("plint_on", "hava_besleme_K", "kose_dikmesi_0", "kose_dikmesi_1") + tuple("REF_bulasik_ayar_ayagi_%d" % _i for _i in range(4))
YENI_V6 = ("onyuz_", "kopru_kirisi_uc_plakasi_", "bulasik_tabla_kirisi_", "bulasik_tavasi", "sensor_braketi_", "PulsaJet_semeri", "DGRF_burcu_", "itici_home_braketi",
           "pano_ara_burcu_", "sartlandirici_montaj_saci", "REF_bulasik_sepet_rayi_", "REF_bulasik_yikama_kolu_gobek_borusu_", "bulasik_gecis_")


def _kati_kes(wp, arac):
    """2. tur: çok katılı (üretici STEP) bileşiği KATI KATI keser — bileşiği tek hamlede kesmek geçersiz katı üretir (OCP; din_parca notu)"""
    a = arac.val() if hasattr(arac, "val") else arac
    A = a.BoundingBox(); ss = []
    for q in wp.val().Solids():
        B_ = q.BoundingBox()
        kes_ = A.xmin < B_.xmax and B_.xmin < A.xmax and A.ymin < B_.ymax and B_.ymin < A.ymax and A.zmin < B_.zmax and B_.zmin < A.zmax
        ss.append(q.cut(a) if kes_ and q.intersect(a).Volume() > 1e-6 else q)
    return cq.Workplane(obj=cq.Compound.makeCompound(ss))

# bant
BANT_Z = (-412.0, -12.0)          # bant genişliği 400
BANT_K = 2.0                      # PU bant kalınlığı [V]
X_KUYRUK, R_KUYRUK = 37.0, 15.0   # kuyruk (gergi) rulosu Ø30 [V]
X_TAHRIK, R_TAHRIK = 560.0, 25.0  # RollerDrive EC5000 Ø50 [K: interroll.com EC5000]
Y_KUYRUK = BANT - BANT_K - R_KUYRUK
Y_TAHRIK = BANT - BANT_K - R_TAHRIK

# kesici (Festo DGRF-C-63-125 · 6 bar: 1870 N) [K: festo DGRF-C clean design veri sayfası]
STROK = 125.0
BICAK_R0, BICAK_R1, BICAK_H, BICAK_T = 15.0, 148.0, 45.0, 1.5    # yıldız bıçak Ø296 × 6 [V: Ø300 sınıfı]
KESIM_ALT = BANT + 0.5            # bıçak ağzı alt dayamada bandın 0,5 mm üstünde ("bıçak izi yeter")
Y_AGIZ_UST = KESIM_ALT + STROK    # 1121,5 (v4; v3 1289,5) · kafa yukarıda bıçak ağzı
Y_GOBEK = Y_AGIZ_UST + BICAK_H    # 1166,5 (v4; v3 1334,5) · bıçak üstü = kafa plakası altı
Y_KAFA = (Y_GOBEK, Y_GOBEK + 8.0)
Y_BOY = (Y_KAFA[1], Y_KAFA[1] + 50.0)          # ara dikmeler
Y_ON_PL = (Y_BOY[1], Y_BOY[1] + 15.0)          # silindirin ön (boyunduruk) plakası
Y_GOVDE = (Y_ON_PL[1] + 20.0, Y_ON_PL[1] + 170.0)   # DGRF-C gövdesi 150 [V: Ø63 gövde boyu]
Y_KIRIS = (Y_GOVDE[1] + 10.0, Y_GOVDE[1] + 50.0)
KORUMA_R = (156.5, 158.0)         # bıçak koruma halkası
KORUMA_ALT = Y_AGIZ_UST + 8.0
UC_T = 8.0                        # v6: köprü uç plakası 8 mm (kirişler yan saclara + ön çerçeve dikmesine bu plakayla bağlanır)
UC_Y = (Y_KIRIS[0] - 20.0, Y_KIRIS[1] + 20.0)
UC_Z = (-290.0, Z_CER[0])         # arka ucu arka kirişin 20 gerisi · ön ucu ön çerçeve dikmesinin arka yüzü (+27)

# çit (ürünü 36 mm içeri kaydırır)
CIT_ACI = 20.0
CIT_R = 160.0                     # çit, bekleyen ürünün merkezinden 160 mm (ürün 150, koruma halkası 158)
_ca = math.radians(CIT_ACI)
CIT_P0 = (XC + CIT_R * math.sin(_ca), ZC + CIT_R * math.cos(_ca))    # teğet noktası
CIT_Z_DUZ = ZB + PZ_R             # −56 · düz kısım (kaydırma bitti)
CIT_X_DONUS = CIT_P0[0] + (CIT_P0[1] - CIT_Z_DUZ) / math.tan(_ca)
CIT_Y = (BANT + 1.0, BANT + 21.0)

# itici
ITICI_KALK = 60.0                 # kaldırma stroku (SMC MGPM20-60) [V]
Y_ITICI = (BANT + 3.0, BANT + 48.0)      # itici plaka (aşağıda)
ITICI_Z = (-320.0, -60.0)
ITICI_ONU = 224.0                 # itici yüzü = araba merkezi + 224
YUZ_BEKLE, YUZ_BAS, YUZ_SON = 596.0, 345.0, 710.0
EKSEN_X = (16.0, 591.0)           # igus ZLW-1040 profil boyu 575 (strok 365 + araba 100 + uçlar 110) [V: ölçü teyidi]
Y_EKSEN = (BANT - 64.0, BANT - 16.0)   # v4: 932–980 (v3 1100–1148 sabitti)
Z_EKSEN = (-485.0, -445.0)

# sprey
SPREY_G = 8.0                     # g tereyağı / pide [V: araştırma tahmini 5–15 g]
SPREY_DEBI = 7.0                  # g/s [V: TPU8002 su 0,76 L/dk ≈ 11 g/s · tereyağı daha koyu]
TANK_L = 3.0                      # ısıtmalı basınçlı tank [H: 2 gün = 80 × 8 × 2 / 0,91 = 1,41 L + ölü hacim]
Y_UC = Y_GOBEK - 6.5              # nozül gövdesinin altı; uç 6 mm daha aşağıda = göbek halkasının altıyla aynı (kafa yukarıda)

PARCALAR = []


def ekle(ad, wp, mal, grup="SABIT", bom=None):
    assert all(p["ad"] != ad for p in PARCALAR), ad
    PARCALAR.append(dict(ad=ad, wp=wp, mal=mal, grup=grup, bom=bom))


def kc(fn, *a, **k):
    """kutu_cad_v3'ün standart parça fonksiyonu (gerçek STEP'ler) → bu modülün listesine"""
    n = len(KC.PARCALAR); fn(*a, **k)
    for p in KC.PARCALAR[n:]:
        ekle(p["ad"], p["wp"], p["mal"], p["grup"], p["bom"])
    del KC.PARCALAR[n:]


def boru(pts, r):
    ss = []
    for a, b in zip(pts[:-1], pts[1:]):
        v = cq.Vector(*b) - cq.Vector(*a)
        if v.Length > 1e-6: ss.append(cq.Solid.makeCylinder(r, v.Length, cq.Vector(*a), v.normalized()))
    for p in pts[1:-1]: ss.append(cq.Solid.makeSphere(r, cq.Vector(*p), angleDegrees1=-90, angleDegrees2=90))
    return cq.Workplane(obj=cq.Compound.makeCompound(ss))


def radyal(r0, r1, t, y0, y1, phi):
    """XC,ZC merkezli, φ açısında (x ekseninden, xz düzleminde) radyal levha"""
    b = kut(r0, r1, y0, y1, -t / 2.0, t / 2.0)
    return b.rotate((0, 0, 0), (0, 1, 0), -phi).translate((XC, 0, ZC))


def polar(r, phi):
    return XC + r * math.cos(math.radians(phi)), ZC + r * math.sin(math.radians(phi))


# ---------------------------------------------------------------- 1 · GÖVDE ----------------------------------------------------------------
def govde():
    for i, (ax, az) in enumerate(((50.0, -110.0), (550.0, -110.0), (50.0, -770.0), (550.0, -770.0))):
        ekle("ayak_%d" % i, sily(ax, az, 20.0, 0.0, 8.0).union(sily(ax, az, 6.0, 8.0, Y_PLINT)), "celik",
             bom=("Ayarlı ayak Elesa+Ganter LV.A-SST · M12", 4, "paslanmaz · taban Ø40", "elesa-ganter.com LV.A-SST") if i == 0 else None)
    zk = Z_KABUK_ON                                                                    # v6: kabuğun ön kenarı +59 (kapak arkası) · v5: 0 / −1,5
    tsc = kut(SAC, W - SAC, Y_PLINT, Y_PLINT + 3.0, -D + SAC, zk)
    for _k, (gx, gz, gr, _ri, _ro, _h) in GECIS.items():                              # 2. tur (denetçi K-8): bulaşık bağlantılarının rakorlu geçiş delikleri (makinenin arkasında)
        tsc = tsc.cut(sily(gx, gz, gr, Y_PLINT - 1.0, Y_PLINT + 4.0))
    ekle("taban_sac_3", tsc, "sac")
    # v6: plint_on (z −61,5…−60) KALKTI → onyuz_plint (z +17,5…+19) on_cerceve()'de
    ist = kut(SAC, W - SAC, H_B, H_B + 3.0, -D + SAC, zk)
    for x0, x1 in (CER_X_SOL, CER_X_SAG):                                              # ön çerçeve dikmeleri kesintisiz geçer: önden açık çentik (kaynakla birleşir)
        ist = ist.cut(kut(x0, x1, H_B - 1.0, H_B + 4.0, Z_CER[0], zk + 1.0))
    for x0 in (SAC, W - SAC - 30.0):                                                   # v6: arka köşe dikmeleri de çentikten geçer (v5: sac dikmenin içinden geçiyordu, 2 × 672 mm³)
        ist = ist.cut(kut(x0, x0 + 30.0, H_B - 1.0, H_B + 4.0, -D + SAC - 1.0, -D + SAC + 30.0))
    ekle("istasyon_tabani_3", ist, "sac")                                              # v6: hava_besleme_K deliği (x 200–260 · z −800…−760) KALKTI (hortum silindi)
    ekle("arka_sac", kut(0, W, Y_PLINT, H, -D, -D + SAC), "kabuk")
    ekle("ust_sac", kut(0, W, H - SAC, H, -D + SAC, zk), "kabuk")
    # sol yan: fırın bandı + ürün girişi (fırın bandı K'ya 15 mm girer) · v6: ön kenar +59, açıklık AYNI
    ekle("sol_sac_urun_girisi", kut(0, SAC, Y_PLINT, H - SAC, -D + SAC, zk).cut(kut(-1, SAC + 1, URUN_GIRISI[0], URUN_GIRISI[1], URUN_GIRISI[2], URUN_GIRISI[3])), "kabuk")
    ekle("sag_sac_E_penceresi", kut(W - SAC, W, Y_PLINT, H - SAC, -D + SAC, zk).cut(kut(W - SAC - 1, W + 1, E_PENCERE[0], E_PENCERE[1], E_PENCERE[2], E_PENCERE[3])), "kabuk")
    # köşe dikmeleri 30 × 30 × 2: v6 yalnız ARKA iki dikme (2, 3) — öndeki kesik dikmeler (0, 1) KALKTI, yerine kesintisiz ön çerçeve dikmeleri (on_cerceve)
    for i, (x0, z0) in ((2, (SAC, -D + SAC)), (3, (W - SAC - 30.0, -D + SAC))):
        dik = kut(x0, x0 + 30.0, Y_PLINT + 3.0, H - SAC, z0, z0 + 30.0).cut(kut(x0 + 2, x0 + 28, Y_PLINT + 2, H, z0 + 2, z0 + 28))
        ekle("kose_dikmesi_%d" % i, dik, "sac", bom=("Kare profil 30 × 30 × 2 AISI 304 (arka köşe dikmesi)", 2, "boy %.1f" % (H - SAC - Y_PLINT - 3.0), "lazer + kaynak") if i == 2 else None)
    on_cerceve()


def _profil(x0, x1, y0, y1, z0, z1, eksen, t=2.0):
    """kutu profil (et t) · eksen 'y' dikey, 'x' yatay · uçları açık (kaynakla kapanır)"""
    if eksen == "y":
        return kut(x0, x1, y0, y1, z0, z1).cut(kut(x0 + t, x1 - t, y0 - 1.0, y1 + 1.0, z0 + t, z1 - t))
    return kut(x0, x1, y0, y1, z0, z1).cut(kut(x0 - 1.0, x1 + 1.0, y0 + t, y1 - t, z0 + t, z1 - t))


def on_cerceve():
    """v6 · ön çerçeve (SPEC §2.5): 2 kesintisiz dikme (y 126–1860,5 · z +27…+57) + 4 kayıt (yatay derzlerin arkasında) · plint +17,5…+19"""
    ekle("onyuz_cerceve_dikme_sol", _profil(CER_X_SOL[0], CER_X_SOL[1], Y_CER[0], Y_CER[1], Z_CER[0], Z_CER[1], "y"), "sac",
         bom=("Ön çerçeve dikmesi · kare profil 30 × 30 × 2 AISI 304", 1, "boy %.1f · kesintisiz · sol gizli menteşeler + köprü uç plakası buna" % (Y_CER[1] - Y_CER[0]),
              "üretim · taban sacı + üst sac + yan saca kaynak"))
    ekle("onyuz_cerceve_dikme_sag", _profil(CER_X_SAG[0], CER_X_SAG[1], Y_CER[0], Y_CER[1], Z_CER[0], Z_CER[1], "y"), "sac",
         bom=("Ön çerçeve dikmesi · bükme kutu 28,5 × 30 × 2 AISI 304", 1, "boy %.1f · kesintisiz · bas-aç mandallar + AZM40 + köprü uç plakası buna" % (Y_CER[1] - Y_CER[0]),
              "KARAR (varsayım): SPEC x 570–598,5 → standart 30 × 30 sığmaz; 2 mm sac bükülüp dikiş kaynaklı (bulaşık kapak zarfına 1,5 pay)"))
    for ad_, y0, y1 in KAYITLAR:
        ekle("onyuz_cerceve_kayit_%s" % ad_, _profil(CER_X_SOL[1], CER_X_SAG[0], y0, y1, Z_CER[0], Z_CER[1], "x"), "sac",
             bom=("Ön çerçeve kaydı · kare profil 30 × 30 × 2 AISI 304", len(KAYITLAR), "boy %.1f · derz çizgilerinin arkasında (126 · 883/886 · 1305/1308 · 1860)" % (CER_X_SAG[0] - CER_X_SOL[1]),
                  "üretim · dikmelere kaynak") if ad_ == "alt" else None)
    zp0, zp1 = Z_PLINT
    # 2. tur (denetçi K-4): SPEC §1 y 0–123 (v6-1 10–123) · x 0–600 (v6-1 30–570; E v7 plinti x 0'dan başlar "K ile birleşir" → K + E tek çizgi) ·
    # yan dönüşler TAM DERİNLİK (store_cad_v8 gibi −828,5; v6-1 58 idi — K'nin altı yandan açıktı) · yan sacların altında, ayaklara değmez (ayak tabanı x 30–70 / 530–570)
    pl = kut(0.0, W, 0.0, Y_PLINT, zp0, zp1)
    for xd in (0.0, W - TAVA_T):
        pl = pl.union(kut(xd, xd + TAVA_T, 0.0, Y_PLINT, -D + SAC, zp0))
    pl = pl.union(kut(TAVA_T, W - TAVA_T, Y_PLINT - TAVA_T, Y_PLINT, zp0 - PLINT_FLANS, zp0))       # üst flanş 15: taban sacının altına M5 perçin somunla
    ekle("onyuz_plint", pl, "sac", bom=("Plint 304 fırçalı 1,5 · tam derinlik yan dönüşlü + üst flanşlı", 1,
                                        "600 × 123 · ön yüz z +19 (ön düzlemin 60 gerisi) · yan dönüşler x 0 / 598,5 → z −828,5 · üst flanş %.0f" % PLINT_FLANS,
                                        "v6 · flanş taban sacına M5 perçin somunla (sökülebilir) · E v7 plintiyle x 600'de birleşir"))


def _yarik_x():
    """SEÇENEK yarık deseninin sol kenarları · desen kapak üzerinde ORTALI (2. tur: v6-1 x0 40 → sol pay 37 / sağ 45,5)"""
    n, a, e = YARIK["n"], YARIK["adim"], YARIK["en"]
    x0 = (KAPAK_X[0] + KAPAK_X[1]) / 2.0 - ((n - 1) * a + e) / 2.0
    return [x0 + i * a for i in range(n)]


def _yarik(ad_):
    """SEÇENEK · lazer yarık bandı (havalandırma): dikey yarıklar 3 × 40, adım 10 · yalnız ön sacı keser → (bileşik katı, yarık sayısı)"""
    ss = [cq.Solid.makeBox(YARIK["en"], yb - ya, TAVA_T + 2.0, cq.Vector(x, ya, Z_ON - TAVA_T - 1.0)) for ya, yb in YARIK["bant"][ad_] for x in _yarik_x()]
    return cq.Compound.makeCompound(ss), len(ss)


def _tava(y0, y1):
    x0, x1 = KAPAK_X; z0, z1 = Z_TAVA; t = TAVA_T
    return kut(x0, x1, y0, y1, z0, z1).cut(kut(x0 + t, x1 - t, y0 + t, y1 - t, z0 - 1.0, z1 - t))


def kapaklar():
    """v6 · ÖN KAPAKLAR (SPEC §2.5) — tava panel 304 fırçalı 1,5, kenarlar 20 arkaya bükülü (z +59…+79), x 3–598,5 (dünya 4003–4598,5):
    ALT (bulaşık) y 126–883 · ORTA y 886–1305 · ÜST y 1308–1859 · SOL gizli menteşe (EMKA 1046-U5, sanal pivot x 3 z 79, en çok 90°) ·
    bas-aç mandal (Southco E4, sağ dikmede; strok = kapak arkası 59 ↔ çerçeve 57) · ORTA + ÜST: Schmersal AZM40 emniyet kilidi (gizli, dil ağıza 8 mm girer) ·
    ALT: iç yüzde EPDM dayama lastiği (bulaşık kapağı kilitte buna dayanır) · önden YALNIZ düz yüzey + derz (SPEC §1) — lazer yarık yalnız SEÇENEK (YARIK_ACIK) ·
    panel < 600 geniş → omega takviye YOK (SPEC kuralı)"""
    x0, x1 = KAPAK_X; z0, z1 = Z_TAVA; t = TAVA_T
    mx0, mx1 = MENTESE["x"]; ml = MENTESE["boy"]
    for g, ad_, y0, y1 in KAPAKLAR:
        w = _tava(y0, y1)
        ny = 0
        if YARIK_ACIK and ad_ in YARIK["bant"]:                                         # 2. tur: varsayılan KAPALI (SPEC) — seçenek
            yk, ny = _yarik(ad_)
            w = w.cut(yk)
        kg = w.val().Volume() * RHO_304
        ekle("onyuz_kapak_%s" % ad_, w, "sac", g,
             bom=("Ön kapak %s · tava panel 304 fırçalı 1,5 · kenarlar 20 büküm" % ad_.upper(), 1,
                  "%.1f × %.1f · %.1f kg · 2 gizli menteşe + bas-aç%s%s" % (x1 - x0, y1 - y0, kg, " + AZM40 kilit" if ad_ in AZM_KAPAK else "",
                                                                             " · %d lazer yarık 3 × 40 (havalandırma)" % ny if ny else ""),
                  "lazer + abkant · köşeler kaynaklı taşlanmış · derz 3 · önden yalnız düz yüzey"))
        for j, ym in enumerate(MENTESE_Y[ad_]):
            ekle("onyuz_mentese_govde_%s_%d" % (ad_, j), kut(mx0, mx1, ym - ml / 2.0, ym + ml / 2.0, Z_CER[1], z0), "celik",
                 bom=("Gizli menteşe EMKA 1046-U5 (AISI 304 · 90° · kaynaklı · katalog 4B-130)", 6,
                      "boy ≈ 79 · pim Ø16 (GlobalSpec) · çerçeve kanadı sol dikmeye, kapak kanadı kapak içine kaynak",
                      "emka.com/products/1046-u5 · sanal pivot (kapak ön-sol köşesi) + kanat ölçüleri VARSAYIM — üreticiden teyit") if (ad_, j) == ("alt", 0) else None)
            ekle("onyuz_mentese_kanat_%s_%d" % (ad_, j), kut(mx0, mx1, ym - ml / 2.0, ym + ml / 2.0, z0, z1 - t), "celik", g)
        ym = (y0 + y1) / 2.0
        ekle("onyuz_basac_mandal_%s" % ad_, kut(MANDAL["x"][0], MANDAL["x"][1], ym - MANDAL["boy"] / 2.0, ym + MANDAL["boy"] / 2.0, Z_CER[1], Z_CER[1] + MANDAL["derin"]), "plastik",
             bom=("Dokun-aç mandal Southco E4 (touch latch, gizli)", 3, "sağ çerçeve dikmesinin ön yüzüne · strok 2 (kapak arkası 59 ↔ çerçeve 57)",
                  "southco.com E4 touch latches (ör. E4-10-201-10) · gövde ölçüsü VARSAYIM 14 × 44 × 14") if ad_ == "alt" else None)
        ekle("onyuz_basac_karsilik_%s" % ad_, kut(MANDAL["x"][0], MANDAL["x"][1], ym - MANDAL["boy"] / 2.0, ym + MANDAL["boy"] / 2.0, Z_CER[1] + MANDAL["derin"], z1 - t), "celik", g)
        if ad_ in AZM_KAPAK:
            xa = CER_X_SAG[0]
            azm = kut(xa - AZM["kal"], xa, ym - AZM["boy"] / 2.0, ym + AZM["boy"] / 2.0, Z_CER[1] - AZM["en"], Z_CER[1]).cut(
                kut(xa - AZM["kal"] + 1.0, xa - 1.0, ym - 16.0, ym + 16.0, Z_CER[1] - AZM_AGIZ, Z_CER[1] + 1.0))              # 2. tur: dil giriş ağzı 18 × 32 × 8 (VARSAYIM)
            ekle("onyuz_kilit_AZM40_%s" % ad_, azm, "sari",
                 bom=("Emniyet kilidi Schmersal AZM40 (solenoid, RFID kodlu, IP69) — SPEC'te YOK, Kemal onayı gerekir", 2,
                      "119,5 × 40 × 20 · 2000 N kilitleme · PLe · sağ dikmenin iç yüzüne · dil ağıza 8 mm girer",
                      "schmersal.com/en/azm40 · ORTA (bıçak + itici) + ÜST (kılavuz mili uçları, tank, pano) · PNOZ s3'e · ağız yeri Schmersal çizimiyle teyit") if ad_ == "orta" else None)
            ekle("onyuz_kilit_dili_%s" % ad_, kut(xa - AZM["kal"] + 2.0, xa - 2.0, ym - 15.0, ym + 15.0, Z_CER[1] - AZM_AGIZ, z1 - t), "celik", g)   # 2. tur: z 49 (ağız dibi) … 77,5 (v6-1: 59,5'te bitiyordu)
        if ad_ == "alt":                                                                # 2. tur (denetçi K-11): bulaşık kapağının kilitte dayandığı yer — 1,5 sac yerine EPDM
            ekle("onyuz_dayama_lastigi_alt", kut(DAYAMA["x"][0], DAYAMA["x"][1], DAYAMA["y"][0], DAYAMA["y"][1], z1 - t - DAYAMA["t"], z1 - t), "conta", g,
                 bom=("Dayama lastiği EPDM 3 × 30 (yapışkanlı şerit)", 1, "460 × 30 × 3 · ALT kapağın iç yüzüne · bulaşık kapağının üst kenarı kilitte buna dayanır",
                      "VARSAYIM ölçü · genel katalog EPDM şerit (parça no yok)"))


# ---------------------------------------------------------------- 2 · K BANDI ----------------------------------------------------------------
def bant():
    z0, z1 = BANT_Z
    for i, (a, b) in enumerate(((z0 - 5.0, z0 - 2.0), (z1 + 2.0, z1 + 5.0))):
        ekle("bant_yan_levhasi_%d" % i, kut(10.0, 590.0, BANT - 64.0, BANT - BANT_K - 0.5, a, b).cut(silz(X_TAHRIK, Y_TAHRIK, 6.0, a - 1.0, b + 1.0)).cut(   # 2. tur: mil yatak delikleri + gergi yarığı
             silz(X_KUYRUK, Y_KUYRUK, 4.0, a - 1.0, b + 1.0)).cut(silx(Y_KUYRUK - 10.0, (a + b) / 2.0, 3.0, X_KUYRUK, X_KUYRUK + 40.0)), "sac",
             bom=("Bant yan levhası 3 mm AISI 304 (lazer + büküm)", 2, "580 × 62", "üretim") if i == 0 else None)
    ekle("kayma_tablasi_6", kut(52.0, 535.0, BANT - BANT_K - 6.0, BANT - BANT_K, z0 + 2.0, z1 - 2.0), "sac",
         bom=("Kayma tablası 6 mm AISI 304 (kesim yükünü taşır)", 1, "483 × 396", "üretim"))
    for i, x in enumerate((150.0, 450.0)):
        ekle("tabla_kirisi_%d" % i, kut(x - 20.0, x + 20.0, BANT - BANT_K - 26.0, BANT - BANT_K - 6.0, z0 - 2.0, z1 + 2.0), "sac",
             bom=("Kutu profil 40 × 20 × 2 AISI 304", 2, "boy 404", "üretim") if i == 0 else None)
    for i, (x, za, zb) in enumerate(((60.0, z0 - 5.0, z0 + 19.0), (540.0, z0 - 5.0, z0 + 19.0), (60.0, z1 - 19.0, z1 + 5.0), (540.0, z1 - 19.0, z1 + 5.0))):
        ekle("bant_ayagi_%d" % i, kut(x - 15.0, x + 15.0, H_B + 3.0, BANT - 64.0, za, zb), "sac",
             bom=("Bant ayağı 30 × 24 lama", 4, "", "üretim") if i == 0 else None)
    # rulolar: tahrik = RollerDrive (motor içinde), kuyruk = gergili avara
    ekle("tahrik_rulosu_RollerDrive_EC5000", silz(X_TAHRIK, Y_TAHRIK, R_TAHRIK, z0 - 2.0, z1 + 2.0).cut(silz(X_TAHRIK, Y_TAHRIK, 6.0, z0 - 3.0, z1 + 3.0)), "aluminyum", "SABIT",   # 2. tur: mil yuvası (içi dolu modeldi)
         ("Interroll RollerDrive EC5000 AI 24 V Ø50 (motor rulonun içinde, IP66)", 1, "boy 404 · kaplamalı", "interroll.com EC5000 [V: kaplama + IP teyidi]"))
    ekle("tahrik_rulosu_mili", silz(X_TAHRIK, Y_TAHRIK, 6.0, z0 - 5.0, z1 + 5.0), "celik")
    ekle("kuyruk_rulosu", silz(X_KUYRUK, Y_KUYRUK, R_KUYRUK, z0 + 2.0, z1 - 2.0).cut(silz(X_KUYRUK, Y_KUYRUK, 4.0, z0 + 1.0, z1 - 1.0)), "aluminyum",   # 2. tur: mil yuvası
         bom=("Avara rulo Ø30 paslanmaz (gergi cıvatalı)", 1, "boy 404", "[V] katalog"))
    ekle("kuyruk_rulosu_mili", silz(X_KUYRUK, Y_KUYRUK, 4.0, z0 - 5.0, z1 + 5.0), "celik")
    for i, zz in enumerate((z0 - 3.5, z1 + 3.5)):
        ekle("bant_gergi_civatasi_%d" % i, silx(Y_KUYRUK - 10.0, zz, 3.0, X_KUYRUK, X_KUYRUK + 40.0), "celik")
    # bant (PU 2 mm): üst kol + alt kol + iki sarım
    ust = kut(X_KUYRUK, X_TAHRIK, BANT - BANT_K, BANT, z0, z1)
    a0, a1 = Y_KUYRUK - R_KUYRUK, Y_TAHRIK - R_TAHRIK
    alt = cq.Workplane("XY", origin=(0, 0, z0)).polyline([(X_KUYRUK, a0 - BANT_K), (X_TAHRIK, a1 - BANT_K), (X_TAHRIK, a1), (X_KUYRUK, a0)]).close().extrude(z1 - z0)
    sarim_t = silz(X_TAHRIK, Y_TAHRIK, R_TAHRIK + BANT_K, z0, z1).cut(silz(X_TAHRIK, Y_TAHRIK, R_TAHRIK, z0 - 1, z1 + 1)).cut(kut(X_TAHRIK - 40, X_TAHRIK, BANT - 164.0, BANT + 36.0, z0 - 1, z1 + 1))
    sarim_k = silz(X_KUYRUK, Y_KUYRUK, R_KUYRUK + BANT_K, z0, z1).cut(silz(X_KUYRUK, Y_KUYRUK, R_KUYRUK, z0 - 1, z1 + 1)).cut(kut(X_KUYRUK, X_KUYRUK + 40, BANT - 164.0, BANT + 36.0, z0 - 1, z1 + 1))
    ekle("bant_PU_2mm", ust.union(alt).union(sarim_t).union(sarim_k).cut(silz(X_TAHRIK, Y_TAHRIK, R_TAHRIK, z0 - 1.0, z1 + 1.0)).cut(silz(X_KUYRUK, Y_KUYRUK, R_KUYRUK, z0 - 1.0, z1 + 1.0)),   # 2. tur: alt kolun rulo içine giren şeridi (9,3 mm³)
         "pu_bant",
         bom=("Gıda PU bant 2 mm homojen, beyaz (FDA / EU 10-2011), sonsuz birleştirilmiş", 1, "400 × ≈1150", "[V] Ammeraal / Habasit sınıfı · kesim yüzeyi"))
    # bant sonu ölü plakası + çit
    ekle("olu_plaka", kut(587.0, 597.0, BANT - 6.0, BANT, z0 - 2.0, z1 + 2.0), "sac",                          # v6: iki bant yan levhasına kadar (v5 −380…−30 havada)
         bom=("Ölü plaka 10 mm AISI 304 (bant sonu → E köprüsü)", 1, "10 × 6 × 404", "v6: iki yan levhaya M5 × 2"))
    tz = math.tan(_ca)
    zc = lambda x: CIT_P0[1] - tz * (x - CIT_P0[0])
    xa = 330.0
    pts = [(xa, zc(xa)), (CIT_X_DONUS, CIT_Z_DUZ), (597.0, CIT_Z_DUZ), (597.0, CIT_Z_DUZ + 3.0), (CIT_X_DONUS + 3.0 * math.tan(_ca / 2.0), CIT_Z_DUZ + 3.0), (xa, zc(xa) + 3.0)]
    cit = cq.Workplane("XZ", origin=(0, CIT_Y[0], 0)).polyline(pts).close().extrude(-(CIT_Y[1] - CIT_Y[0]))
    ekle("cit_20_derece", cit, "uhmw", bom=("Kılavuz çit: 304 lama 3 mm + UHMW yüz (gıda)", 1, "20° + düz · 20 yüksek", "üretim"))
    for i, x in enumerate((420.0, 560.0)):
        zf = zc(x) if x < CIT_X_DONUS else CIT_Z_DUZ
        ekle("cit_braketi_%d" % i, kut(x - 8.0, x + 8.0, CIT_Y[1], CIT_Y[1] + 4.0, zf, z1 + 5.0).union(kut(x - 8.0, x + 8.0, BANT - BANT_K - 0.5, CIT_Y[1] + 4.0, z1 + 2.0, z1 + 5.0)), "sac")


# ---------------------------------------------------------------- 3 · KESİCİ + SPREY KAFASI (aynı yer) ----------------------------------------------------------------
def kesici():
    # köprü: iki kiriş x boyunca + silindir plakası
    for i, (za, zb) in enumerate(((-110.0, -70.0), (-270.0, -230.0))):
        ekle("kopru_kirisi_%d" % i, kut(SAC + UC_T, W - SAC - UC_T, Y_KIRIS[0], Y_KIRIS[1], za, zb).cut(kut(SAC, W - SAC, Y_KIRIS[0] + 2, Y_KIRIS[1] - 2, za + 2, zb - 2)), "sac",
             bom=("Kare profil 40 × 40 × 2 AISI 304 (köprü)", 2, "boy %.0f · v6: uçları 8 mm uç plakalarına kaynaklı" % (W - 2 * SAC - 2 * UC_T), "üretim") if i == 0 else None)
    for i, (x0, x1) in enumerate(((SAC, SAC + UC_T), (W - SAC - UC_T, W - SAC))):            # v6: köprü yan saclara + ön çerçeve dikmesine bağlanır (v5: 1 mm HAVADA — KRİTİK)
        ekle("kopru_kirisi_uc_plakasi_%d" % i, kut(x0, x1, UC_Y[0], UC_Y[1], UC_Z[0], UC_Z[1]), "sac",
             bom=("Köprü uç plakası 8 mm AISI 304", 2, "%.0f × %.0f · yan saca 6 × M6 perçin somun + ön çerçeve dikmesine kaynak" % (UC_Y[1] - UC_Y[0], UC_Z[1] - UC_Z[0]),
                  "v6 · 1870 N kesme tepkisi → yan sac + ön dikme") if i == 0 else None)
    pl = kut(215.0, 385.0, Y_GOVDE[1], Y_KIRIS[0], -275.0, -65.0)
    for x in (245.0, 300.0, 355.0):
        pl = pl.cut(sily(x, ZC, 12.0, Y_GOVDE[1] - 1, Y_KIRIS[0] + 1))
    ekle("silindir_baglanti_plakasi", pl, "sac")
    # DGRF-C gövdesi (sabit) + milleri (hareketli)
    ekle("DGRF-C-63-125_govde", kut(225.0, 375.0, Y_GOVDE[0], Y_GOVDE[1], ZC - 45.0, ZC + 45.0).cut(sily(245, ZC, 11, Y_GOVDE[0] - 1, Y_GOVDE[1] + 1)).cut(sily(355, ZC, 11, Y_GOVDE[0] - 1, Y_GOVDE[1] + 1)).cut(sily(300, ZC, 11, Y_GOVDE[0] - 1, Y_GOVDE[1] + 1)),
         "aluminyum", bom=("Kılavuzlu silindir Festo DGRF-C-63-125 (Clean Design, paslanmaz kılavuz milleri)", 1, "Ø63 · strok 125 · 6 bar'da 1870 N itme",
                           "festo DGRF-C veri sayfası (almotion.nl) · gövde ölçüsü [V]"))
    for i, yy in enumerate((Y_GOVDE[0] + 30.0, Y_GOVDE[0] + 120.0)):
        ekle("DGRF_hava_rakoru_%d" % i, silx(yy, ZC + 20.0, 5.0, 213.0, 225.0), "siyah")
    ekle("DGRF_piston_mili", sily(300.0, ZC, 10.0, Y_ON_PL[1], Y_GOVDE[1] - 10.0), "celik", "KESICI")
    for i, x in enumerate((245.0, 355.0)):
        ekle("DGRF_kilavuz_mili_%d" % i, sily(x, ZC, 10.0, Y_ON_PL[1], Y_GOVDE[1] + STROK), "celik", "KESICI")
    ekle("DGRF_on_plaka", kut(215.0, 385.0, Y_ON_PL[0], Y_ON_PL[1], ZC - 60.0, ZC + 60.0), "aluminyum", "KESICI")
    # ara dikmeler (3) + kafa plakası
    for i, phi in enumerate((30.0, 150.0, 270.0)):
        x, z = polar(70.0, phi)
        ekle("ara_dikme_%d" % i, sily(x, z, 8.0, Y_BOY[0], Y_BOY[1]), "celik", "KESICI",
             bom=("Ara dikme Ø16 × 50 paslanmaz (M8)", 3, "", "üretim") if i == 0 else None)
    ekle("kafa_plakasi_8", sily(XC, ZC, 115.0, Y_KAFA[0], Y_KAFA[1]).cut(sily(XC, ZC, 11.0, Y_KAFA[0] - 1, Y_KAFA[1] + 1)), "sac", "KESICI",
         bom=("Kafa plakası Ø230 × 8 AISI 304", 1, "", "lazer + CNC"))
    # bıçak yıldızı: göbek halkası + 6 bıçak + koruma halkası + kelebek somunlar
    gob = sily(XC, ZC, 20.0, Y_GOBEK - 12.0, Y_GOBEK).cut(sily(XC, ZC, 13.0, Y_GOBEK - 13.0, Y_GOBEK + 1.0))
    for i in range(6):                                                                     # 2. tur: bıçak kökleri göbekteki yuvalara oturur (v6-1: 6 × 90 mm³ gömülü)
        gob = gob.cut(radyal(BICAK_R0, BICAK_R1, BICAK_T, Y_AGIZ_UST, Y_GOBEK, 60.0 * i))
    ekle("bicak_gobek_halkasi", gob, "celik", "KESICI")
    for i in range(6):
        phi = 60.0 * i
        ekle("bicak_%d" % i, radyal(BICAK_R0, BICAK_R1, BICAK_T, Y_AGIZ_UST, Y_GOBEK, phi), "celik", "KESICI",
             bom=("Yıldız bıçak seti 6 dilim Ø296 (sertleştirilmiş paslanmaz, bulaşık makinesinde yıkanır)", 1, "6 × 133 × 45 × 1,5 · göbek Ø40",
                  "Q-T-S PC1018 / PC5000 bıçak seti sınıfı (q-t-s.com) [V: ölçü bize göre]") if i == 0 else None)
    for i in range(6):
        phi = 30.0 + 60.0 * i
        ekle("koruma_braketi_%d" % i, radyal(110.0, KORUMA_R[1], 12.0, Y_KAFA[0], Y_KAFA[1], phi).cut(sily(XC, ZC, 115.0, Y_KAFA[0] - 1.0, Y_KAFA[1] + 1.0)), "sac", "KESICI")   # 2. tur: kafa plakası kenarına alın kaynak (v6-1: 5 mm gömülü)
    ekle("bicak_koruma_halkasi", sily(XC, ZC, KORUMA_R[1], KORUMA_ALT, Y_KAFA[0]).cut(sily(XC, ZC, KORUMA_R[0], KORUMA_ALT - 1, Y_KAFA[0] + 1)), "sac", "KESICI",
         bom=("Bıçak koruma + sprey perdesi halkası Ø316 × 37 (1,5 mm 304)", 1, "", "üretim"))
    for i, phi in enumerate((90.0, 210.0, 330.0)):
        x, z = polar(85.0, phi)
        ekle("kelebek_somun_%d" % i, sily(x, z, 9.0, Y_KAFA[1], Y_KAFA[1] + 14.0), "celik", "KESICI",
             bom=("Kelebek somun M8 paslanmaz (bıçak seti aletsiz sökülür)", 3, "DIN 315", "katalog") if i == 0 else None)
    # SPREY: PulsaJet (yatay, kafa plakası ile boyunduruk arasında) → dirsek → göbekteki nozül
    yp = (Y_BOY[0] + Y_BOY[1]) / 2.0
    ekle("PulsaJet_AA10000AUH_104210", silx(yp, ZC, 19.0, 305.0, 405.0), "celik", "KESICI",
         ("Elektrikli sprey nozülü Spraying Systems PulsaJet AA10000AUH-104210 (gıda: FDA + EC 1935/2004)", 1,
          "24 VDC 0,36 A · PWM · sıvı ≤ 93 °C · 7 bar", "spray.com katalog 76A · vaka E4058 (tereyağı) · gövde ölçüsü [V]"))
    ekle("PulsaJet_isitici_ceket", silx(yp, ZC, 22.0, 330.0, 395.0).cut(silx(yp, ZC, 19.0, 329.0, 396.0)), "hortum_isi", "KESICI",
         bom=("Silikon ısıtıcı ceket 24 V 20 W + termostat (nozülde tereyağı donmasın)", 1, "45 °C", "[V]"))
    ekle("sprey_dirsegi", kut(292.0, 306.0, Y_KAFA[1], yp + 8.0, ZC - 7.0, ZC + 7.0).cut(silx(yp, ZC, 19.0, 305.0, 405.0)), "celik", "KESICI")   # 2. tur: PulsaJet ucuna oturur (v6-1: 1 mm içindeydi, 372 mm³)
    ekle("UniJet_nozul_govdesi_TG", sily(XC, ZC, 10.0, Y_UC, Y_KAFA[1]), "celik", "KESICI",
         ("Nozül gövdesi UniJet + TG tam koni uç 90° (çek valfli: damlatmaz)", 1, "yıldızın göbeğinde, pideden 150 mm",
          "portal.spray.com TG · uç uyumu Spraying Systems'e teyit [V]"))
    ekle("sprey_ucu_TG", sily(XC, ZC, 7.0, Y_UC - 6.0, Y_UC), "pom", "KESICI")
    ekle("isitmali_hortum_kafa", boru([(405.0, yp, ZC), (440.0, yp, ZC), (440.0, Y_ON_PL[1] + 35.0, ZC)], 5.0), "hortum_isi", "KESICI")
    # v6 · havada kalmasın: PulsaJet kafa plakasına semerle · DGRF-C milleri gövdeye burçla (DGRF-C'nin iç kılavuz burçları — kayar geçme, idealleştirilmiş temas)
    ekle("PulsaJet_semeri", kut(309.0, 327.0, Y_KAFA[1], yp, ZC - 14.0, ZC + 14.0).cut(silx(yp, ZC, 19.0, 308.0, 328.0)), "sac", "KESICI",
         bom=("Sprey nozülü semeri 304 (kafa plakasına 2 × M5)", 1, "18 × 25 × 28 · R19 oturma", "v6: PulsaJet + nozül grubu havada kalmasın"))
    for i, x in enumerate((245.0, 300.0, 355.0)):
        ekle("DGRF_burcu_%d" % i, sily(x, ZC, 11.0, Y_GOVDE[0], Y_GOVDE[1]).cut(sily(x, ZC, 10.0, Y_GOVDE[0] - 1, Y_GOVDE[1] + 1)), "celik")
    # sprey konisi (görsel: yalnız sprey anında)
    ekle("sprey_konisi", cq.Workplane(obj=cq.Solid.makeCone(145.0, 3.0, Y_UC - 6.0 - (BANT + PZ_H), cq.Vector(XC, BANT + PZ_H, ZC), cq.Vector(0, 1, 0))), "sprey", "SPREY")


# ---------------------------------------------------------------- 4 · TEREYAĞI SİSTEMİ (taban dolabı arkası) ----------------------------------------------------------------
TANK = dict(x=140.0, z=-540.0, r=80.0, y0=Y_KIRIS[1] + 12.5, y1=Y_KIRIS[1] + 292.5)   # v3: köprü kirişinin arkası · v4: Y_KIRIS'e bağlandı → 1472–1752


def sprey_sistemi():
    x, z, r, y0, y1 = TANK["x"], TANK["z"], TANK["r"], TANK["y0"], TANK["y1"]
    ekle("yag_tanki_3L", sily(x, z, r, y0, y1).cut(sily(x, z, r - 1.5, y0 + 2, y1 - 2)), "sac",
         bom=("Isıtmalı basınçlı tereyağı tankı 3 L AISI 316 (ceketli, kapaklı, seviye sensörlü)", 1, "Ø160 × 280 · 1,5 bar hava · 45 °C",
              "[V] Spraying Systems basınçlı tank sınıfı · 2 gün = 1,41 L (hesap)"))
    ekle("yag_tanki_isitici_ceketi", sily(x, z, r + 6.0, y0 + 30.0, y1 - 30.0).cut(sily(x, z, r, y0, y1)), "hortum_isi",
         bom=("Tank ısıtıcı ceketi 100 W + PT100", 1, "45 °C (32–35 °C'de tamamen sıvı; aşırı ısıda yağ ayrışır)", "[V] · vaka E4058 uyarısı"))
    ekle("yag_tanki_kapagi", sily(x, z, r + 8.0, y1, y1 + 14.0), "sac")
    ekle("yag_tanki_kelepcesi", sily(x, z, r + 10.0, y1 - 6.0, y1 + 4.0).cut(sily(x, z, r, y1 - 7.0, y1 + 5.0)).cut(sily(x, z, r + 8.0, y1, y1 + 5.0)), "celik")   # 2. tur: basamaklı iç yüz — tanka r 80, kapağa r 88 değer (v6-1: kapağın içinden, 14 866 mm³)
    ekle("yag_regulatoru_manometre", sily(x + 45.0, z, 14.0, y1 + 14.0, y1 + 60.0), "aluminyum",
         bom=("Hava regülatörü + manometre 0–4 bar (tank basıncı)", 1, "", "[V] Festo MS2-LR sınıfı"))
    ekle("yag_seviye_sensoru", sily(x - 45.0, z, 8.0, y1 + 14.0, y1 + 44.0), "sensor",
         bom=("Seviye sensörü (kapasitif, gıda)", 1, "2 gün kala uyarır", "[V]"))
    ekle("yag_tanki_rafi", kut(SAC + 3.0, 290.0, y0 - 5.0, y0, -760.0, -380.0), "sac", bom=("Tank rafı 304 · 5 mm", 1, "285,5 × 380", "v6: köşebendin üst kanadına oturur (v5: 34'ten başlıyordu)"))
    ekle("yag_tanki_rafi_koseben", kut(SAC, 34.0, y0 - 35.0, y0 - 5.0, -760.0, -380.0).cut(kut(SAC + 3.0, 35.0, y0 - 36.0, y0 - 8.0, -761.0, -379.0)), "sac",
         bom=("Köşebent 30 × 30 × 3 AISI 304 (tank rafı)", 1, "boy 380", "sol duvara M6 × 3 · v6: duvara değer (v5: 0,5 boşluk)"))
    # ısıtmalı hortum: tank → istasyon tabanı → arka duvar → köprü üstü → kafa (hareketli kısım kafada)
    ekle("isitmali_hortum_Ø6", boru([(x, y1 + 14.0, z), (x, 1792.0, z), (x, 1792.0, -500.0), (440.0, 1792.0, -500.0),
                                      (440.0, Y_KIRIS[1] + 20.0, -500.0), (440.0, Y_KIRIS[1] + 20.0, ZC), (440.0, Y_ON_PL[1] + 35.0 + STROK * 0.0 + 1.0, ZC)], 5.0), "hortum_isi",
         bom=("Isıtmalı gıda hortumu Ø6 iç · 24 V · 45 °C", 1, "≈ 2,6 m · kafaya yaylı sarımla", "[V]"))
    ekle("hava_hortumu_tank", boru([(x + 45.0, y1 + 60.0, z), (x + 45.0, 1827.0, z), (x + 45.0, 1827.0, -775.0), (x + 45.0, 1612.0, -775.0)], 3.0), "hava")   # v6: valf adasının üstüne biter (v5: 8,6 boşluk)


# ---------------------------------------------------------------- 5 · İTİCİ (ürünü E'ye sürer) ----------------------------------------------------------------
def itici():
    xa, xb = EKSEN_X
    ekle("ZLW-1040_eksen_profili", kut(xa + 55.0, xb - 55.0, Y_EKSEN[0], Y_EKSEN[1], Z_EKSEN[0], Z_EKSEN[1]), "aluminyum",
         bom=("Dişli kayışlı lineer eksen igus drylin ZLW-1040 (yağsız, gıdaya yakın)", 1, "strok 365 · profil 575",
              "igus.com ZLW-1040 [V: ölçüler katalogdan teyit]"))
    for i, (a, b) in enumerate(((xa, xa + 55.0), (xb - 55.0, xb))):
        ekle("ZLW_uc_blogu_%d" % i, kut(a, b, Y_EKSEN[0] - 5.0, Y_EKSEN[1] + 5.0, Z_EKSEN[0] - 5.0, Z_EKSEN[1] + 5.0), "aluminyum")
    kc(KC.nema23, "itici_motoru", (xa + 27.5, (Y_EKSEN[0] + Y_EKSEN[1]) / 2.0, Z_EKSEN[0] - 5.0), (0, 0, 1), (0, 1, 0))
    for i, x in enumerate((xa + 80.0, xb - 60.0)):
        ekle("eksen_ayagi_%d" % i, kut(x - 15.0, x + 15.0, H_B + 3.0, Y_EKSEN[0], Z_EKSEN[0] + 5.0, Z_EKSEN[1] - 5.0).cut(                    # 2. tur: uç bloğunun ALTINDA basamaklı (v6-1: bloğa 5 mm giriyordu, 1 500 mm³)
             kut(xa, xa + 55.0, Y_EKSEN[0] - 5.0, Y_EKSEN[1] + 5.0, Z_EKSEN[0] - 5.0, Z_EKSEN[1] + 5.0)).cut(kut(xb - 55.0, xb, Y_EKSEN[0] - 5.0, Y_EKSEN[1] + 5.0, Z_EKSEN[0] - 5.0, Z_EKSEN[1] + 5.0)), "sac")
    kc(KC.e2e, "itici_home_sensoru", xa + 60.0, Y_EKSEN[1] + 10.0, Z_EKSEN[0] - 20.0, "x")
    ekle("itici_home_braketi", kut(78.0, 104.0, 960.0, 1000.0, -513.0, -509.0).union(kut(78.0, 104.0, 960.0, 964.0, -509.0, Z_EKSEN[0])), "sac",   # v6: sensör havada kalmasın
         bom=("Sensör L braketi 304 · 4 mm (home sensörü eksen profiline)", 1, "26 × 40 × 28", "v6"))
    # hareketli: araba + kaldırma silindiri gövdesi (x) · kaldırma kızağı + kol + itici (x + y)
    c = YUZ_BEKLE - ITICI_ONU
    ekle("ZLW_araba", kut(c - 50.0, c + 50.0, Y_EKSEN[1], Y_EKSEN[1] + 27.0, Z_EKSEN[0] - 7.0, Z_EKSEN[1] + 7.0), "aluminyum", "ITICI_ARABA")
    ekle("kaldirma_braketi", kut(c - 30.0, c + 30.0, Y_EKSEN[1] + 27.0, 1132.0, Z_EKSEN[0] - 7.0, Z_EKSEN[0] + 5.0), "sac", "ITICI_ARABA")
    ekle("MGPM20-60_govde", kut(c - 22.0, c + 22.0, 1057.0, 1132.0, Z_EKSEN[0] + 5.0, -446.0), "aluminyum", "ITICI_ARABA",
         ("Kılavuzlu kompakt silindir SMC MGPM20-60Z", 1, "Ø20 · strok 60 · itici kaldırma", "smcworld MGP [V: gövde ölçüsü]"))
    ekle("kaldirma_kizagi", kut(c - 30.0, c + 30.0, 1012.0, 1057.0, -446.0, -434.0), "aluminyum", "ITICI_KOL")
    ekle("itici_kolu_x", kut(c + 30.0, c + 100.0, 1017.0, 1032.0, -446.0, -434.0), "sac", "ITICI_KOL")
    ekle("itici_kolu_z", kut(c + 90.0, c + 100.0, 1017.0, 1032.0, -434.0, -205.0), "sac", "ITICI_KOL")
    ekle("itme_cubugu", kut(c + 90.0, c + 208.0, 1017.0, 1037.0, -205.0, -175.0), "sac", "ITICI_KOL")
    ekle("itici_celik_plaka", kut(c + 208.0, c + 214.0, Y_ITICI[0], Y_ITICI[1], ITICI_Z[0], ITICI_Z[1]), "sac", "ITICI_KOL")
    ekle("itici_POM_yuz", kut(c + 214.0, c + ITICI_ONU, Y_ITICI[0], Y_ITICI[1], ITICI_Z[0], ITICI_Z[1]), "pom", "ITICI_KOL",
         bom=("İtici yüzü POM-C 10 mm (gıda, ≤ 90 °C sürekli)", 1, "260 × 45", "Ensinger TECAFORM AH veri sayfası"))


# ---------------------------------------------------------------- 6 · ELEKTRİK + HAVA ----------------------------------------------------------------
def elektrik():
    zd = -815.0
    ekle("pano_plakasi", kut(300.0, 565.0, 1472.0, 1857.0, -826.0, -822.0), "sac")
    for i, (bx, by) in enumerate(((315.0, 1487.0), (550.0, 1487.0), (315.0, 1842.0), (550.0, 1842.0))):   # v6: pano plakası arka saca 4 ara burçla (v5: 2,5 mm havada)
        ekle("pano_ara_burcu_%d" % i, silz(bx, by, 5.0, -D + SAC, -826.0), "celik", bom=("Ara burç M5 × 2,5 paslanmaz (pano plakası)", 4, "", "katalog") if i == 0 else None)
    for i, y in enumerate((1512.0, 1692.0)):                                           # v3: pano yukarıda (+980) · v4: − 168
        ekle("din_rayi_%d" % i, kut(305.0, 560.0, y, y + 35.0, -822.0, -815.0), "celik", bom=("DIN ray 35 × 7,5", 2, "boy 255", "EN 60715") if i == 0 else None)
    ekle("plc_S7-1200_1214C", kut(315.0, 425.0, 1479.5, 1579.5, zd, zd + 75.0), "siemens",
         bom=("PLC Siemens S7-1200 CPU 1214C DC/DC/DC", 1, "6ES7214-1AG40-0XB0 · bant, kesici, itici, sprey", "110 × 100 × 75"))
    ekle("plc_SM1222_DQ16", kut(429.0, 474.0, 1479.5, 1579.5, zd, zd + 75.0), "siemens", bom=("Siemens SM1222 DQ16", 1, "6ES7222-1BH32-0XB0", "45 × 100 × 75"))
    ekle("emniyet_rolesi_PNOZ", kut(478.0, 500.0, 1479.5, 1579.5, zd, zd + 90.0), "sari", bom=("Emniyet rölesi Pilz PNOZ s3", 1, "v6: 2 × AZM40 kapak kilidi (ORTA + ÜST) + hat acil stop zinciri [AÇIK: acil stop yeri]", "[V] pilz.com"))
    ekle("PWMD_sprey_suruculu", kut(504.0, 530.0, 1479.5, 1579.5, zd, zd + 60.0), "siyah",
         bom=("PulsaJet PWM sürücüsü (tek nozül)", 1, "PLC'den tetik · doz = süre × debi", "[V] Spraying Systems PWMD"))
    ekle("sicaklik_kontrol_2", kut(533.0, 560.0, 1479.5, 1579.5, zd, zd + 70.0), "siyah", bom=("Sıcaklık kontrolcüsü DIN (tank + hortum + nozül)", 2, "PT100 · 45 °C", "[V]"))
    ekle("guc_24V_NDR-240-24", TC.din_parca(TC.GUC_STEP, 315.0, 1662.0, zd + 122.8), "aluminyum",
         bom=("Güç kaynağı Mean Well NDR-240-24", 1, "24 V 10 A · PLC, RollerDrive, sensör, ısıtıcılar", "TraceParts STEP"))
    ekle("surucu_STP-DRV-4830", _kati_kes(TC.din_parca(TC.SURUCU_STEP, 450.0, 1692.0, zd + 28.0), kut(305.0, 560.0, 1692.0, 1727.0, -822.0, -815.0)), "kart",   # 2. tur: DIN klipsinin raya giren kısmı (11,6 mm³) — klips rayın flanşına değer
         bom=("Step sürücü AutomationDirect SureStep STP-DRV-4830", 1, "itici ekseni", "automationdirect.com · TraceParts STEP"))
    ekle("guc_48V_NDR-240-48", TC.din_parca(TC.GUC_STEP, 382.0, 1662.0, zd + 122.8), "aluminyum", bom=("Güç kaynağı Mean Well NDR-240-48", 1, "48 V · step sürücü", "NDR-240 gövdesi"))
    ekle("klemens_sirasi", kut(508.0, 560.0, 1692.0, 1737.0, zd, zd + 45.0), "plastik", bom=("Klemens sırası Phoenix UT 2,5", 24, "", "phoenixcontact.com"))
    ekle("kablo_kanali_0", kut(305.0, 560.0, 1812.0, 1852.0, -822.0, -797.0), "plastik", bom=("Kablo kanalı 40 × 25", 3, "", "katalog"))
    ekle("kablo_kanali_dikey", kut(566.0, 591.0, H_B + 3.0, 1827.0, -D + SAC + 30.0, -D + SAC + 55.0), "plastik")   # 2. tur: arka köşe dikmesinin ÖNÜNE (z −798,5…−773,5) — v5/v6-1 dikmenin içinden geçiyordu (82 016 mm³, ISTISNA gizliyordu)
    # üst bölme: hava şartlandırıcı + valf adası (arka duvar)
    ekle("sartlandirici_MS4", kut(60.0, 110.0, 1532.0, 1692.0, -826.0, -780.0), "aluminyum",
         bom=("Şartlandırıcı Festo MS4-LFR (filtre + regülatör + manometre)", 1, "6 bar", "[V] festo.com MS4"))
    ekle("valf_adasi_VUVG_4", kut(130.0, 250.0, 1552.0, 1612.0, -826.0, -770.0), "aluminyum",
         bom=("Valf adası Festo VUVG-L10 · 4 × 5/2 (kesici · itici kaldırma · tank basıncı · yedek)", 1, "24 V", "[V] festo.com VUVG"))
    ekle("sartlandirici_montaj_saci", kut(55.0, 255.0, 1527.0, 1697.0, -D + SAC, -826.0), "sac",                      # v6: MS4 + valf adası arka saca (v5: 2,5 mm havada)
         bom=("Montaj sacı 2,5 · 304 (MS4 + valf adası)", 1, "200 × 170", "v6: arka saca 4 × M5 · MS4 ve VUVG buna vidalı"))
    # v6: hava_besleme_K SİLİNDİ (SPEC §2.5: MS4 zaten üstten ANA_K48 ile besleniyor — çift besleme) + istasyon tabanındaki deliği
    ekle("hava_hortumu_kesici", boru([(190.0, 1612.0, -790.0), (190.0, 1832.0, -790.0), (205.0, 1832.0, -790.0), (205.0, 1832.0, ZC + 20.0), (205.0, Y_GOVDE[0] + 30.0, ZC + 20.0), (213.0, Y_GOVDE[0] + 30.0, ZC + 20.0)], 3.0), "hava")
    ekle("hava_hortumu_kaldirma", boru([(160.0, 1582.0, -770.0), (160.0, 1582.0, -765.0), (160.0, 1152.0, -765.0), (160.0, 1152.0, -470.0)], 3.0), "hava")   # v6: valfin ön yüzünden çıkar · MGPM'e spiral hortum AÇIK
    # sensörler
    for ad_, x_ in (("sensor_urun_merkezde", 445.0), ("sensor_bant_sonu", 520.0)):   # yatık: 31 × 10,8 × 20 · üstü 1009 < itici kolu 1017 (v4)
        ekle(ad_, kut(x_ - 15.5, x_ + 15.5, BANT + 2.0, BANT + 12.8, BANT_Z[0] - 20.0, BANT_Z[0] - 2.0), "sensor",
             bom=("Fotosel Omron E3Z-D62 (dağınık yansımalı)", 2, "ürün merkezde · bant sonu", "omron.com E3Z") if x_ < 500 else None)
        ekle("sensor_braketi_" + ad_[7:], kut(x_ - 10.0, x_ + 10.0, BANT - BANT_K - 0.5, BANT + 2.0, BANT_Z[0] - 18.0, BANT_Z[0] - 2.0), "sac",   # v6: bant yan levhasına (v5: 4,5 havada)
             bom=("Sensör braketi 304 (bant yan levhasına)", 2, "20 × 4,5 × 16", "v6") if x_ < 500 else None)
    for i, y in enumerate((Y_GOVDE[0] + 10.0, Y_GOVDE[1] - 20.0)):
        ekle("kesici_reed_%d" % i, kut(375.0, 383.0, y, y + 20.0, ZC - 10.0, ZC + 10.0), "sensor",                # v6: gövdeye değer (v5: 1 mm)
             bom=("Silindir sensörü Festo SMT-8M (üst / alt)", 2, "", "[V] festo.com") if i == 0 else None)


# ---------------------------------------------------------------- 7 · TABAN ALTI (v4 · ALÇAK HAT): bulaşık yeri · v5: deterjan / parlatıcı YOK ----------------------------------------------------------------
# SPEC_alcak_hat_v57 + QR_TEZGAH_v4 (Kemal onaylı): K altı 126–892 · MEIKO M-iClean US sağ ön köşe dikmesine yaslı (kapağı dikmeye çarpmaz) ·
# solunda önde 77, dikmenin arkasında 107 BOŞ · makinenin bağlantıları (y ≤ 310) altta kalır.
# v6 (SPEC_on_duzlem_v63 · Kemal: "bulaşık makinesi önüne kapak, alt ayaklarını kaldır"): bulasik_cad_v2 AYAKSIZ → 2 × 40×20×2 tabla kirişi (yan saclara
#    kaynaklı, K taban sacına oturur) + 3 mm tava · makine +13 (gövde altı 149) · önünde ALT kapak (y 126–883, SOL menteşe) · bulaşık kapağı ancak ALT kapak açıkken açılır.
# v5 (Kemal 27 Eyl gece: "deterjanları makinenin arkasına koyma, tabii şimdilik sil"): arkadaki kanister rafı (325–330) + deterjan / parlatıcı bidonları +
#    dozaj emiş hortumları SİLİNDİ → bulaşığın arkası (MEIKO arka payı 25 dahil) BOŞ (denetimde ölçülür). Deterjanın yeri AÇIK — karar Kemal'de.
X_K_HAT = 4000.0                                   # K modülünün hattaki x'i (yerel x = dünya − 4000)
TABLA_KIRIS = (40.0, 20.0, 2.0)                    # v6: bulaşık tabla kirişi 40 × 20 × 2 (z × y × et) · yan saclara kaynaklı, K taban sacının üstünde
TAVA_BM = 3.0                                      # v6: tabla tavası 3 mm (makine buna oturur)
Y_TABLA = Y_PLINT + 3.0 + TABLA_KIRIS[1] + TAVA_BM  # 149 = makinenin gövde altı (v5: ayaklar 126'da, gövde 136'da → makine +13)
BULASIK_YER = (4108.5, Y_TABLA - BM.TABAN, -20.0)  # (4108,5 · 139 · −20) bulasik_cad_v2 (X0, Y0, Z0) dünya kökü = kapak ön yüzü — montaj AYNISINI kullanmalı · v6: gövde altı Y0 + 10 = 149 = tava üstü
# denetçi düzeltmesi: kök z −12 değil −20 → makinenin TAMAMI (ışıklı kulp 8 + gövde 600 + arka bağlantılar 25 = 633) SPEC / Resim 1 v4 B–B'deki z −12…−645'e oturur
BULASIK_ZARF = dict(x=(BULASIK_YER[0] - X_K_HAT, BULASIK_YER[0] - X_K_HAT + BM.W), y=(Y_TABLA, BULASIK_YER[1] + BM.H),
                    z=(BULASIK_YER[2] - BM.D - 25.0, BULASIK_YER[2] + 8.0))    # K yereli 108,5–568,5 × 149–839 × −645…−12 (v6: tava üstünden · SPEC: 633 derin = kulp 8 + gövde 600 + arka bağlantılar 25)
BULASIK_ARKA_PAY = (-670.0, -645.0)                # MEIKO föyü: arkada duvar payı 25 — BOŞ (yalnız makinenin arka bağlantı hortumları geçer)
BULASIK_BAGLANTI_UST = 323.0                       # v6: makinenin arka bağlantıları yerden: tahliye 165 + Y0 139 + yarıçap 15 = 319 ≤ 323 (v5 310 + 13, makine +13)
# 2. tur (denetçi K-8): bulaşık bağlantılarının K'den ÇIKIŞI — taban sacında (makinenin arkasındaki 158,5 mm'lik boşlukta, z −750) rakorlu geçiş:
# hortum / kablo bağlantı ucundan (z −645) aşağı iner → taban sacı → plint boşluğu (arkası açık) → duvar / yer gideri. Arka sac TAM kalır (duvara dayalı, rakor çıkıntısı z −830'u aşardı).
# (x K yereli, z, delik r, rakor iç r, flanş dış r, üst yükseklik) — x = bağlantının x'i (föy: soldan 40 / 186 / 313)
GECIS_Z = -750.0
GECIS = {"elektrik": (BULASIK_YER[0] - X_K_HAT + BM.BAG["elektrik"][0], GECIS_Z, 10.25, 4.5, 12.0, 18.0),     # Lapp SKINTOP MS-M 20×1,5 (sıkma 7–13) · delik Ø20,5
         "tahliye": (BULASIK_YER[0] - X_K_HAT + BM.BAG["tahliye"][0], GECIS_Z, 25.0, 20.0, 30.0, 3.0),        # EPDM geçiş lastiği, Ø40 tahliye hortumu · delik Ø50 (VARSAYIM)
         "su": (BULASIK_YER[0] - X_K_HAT + BM.BAG["su"][0], GECIS_Z, 17.5, 13.0, 22.5, 3.0)}                  # EPDM geçiş lastiği, ¾" su hortumu (dış Ø26) · delik Ø35 (VARSAYIM)


def bulasik_parcalari():
    """bulasik_cad_v2'nin (v6; v5: v1) katıları montajdaki yerinde (BULASIK_YER), K yerelinde · + kapak açık zarfı (K yereli).
    BM modülünün durumu (X0, Y0, Z0, PARCALAR) korunur: montaj kendi BM.kur()'unu çağırır."""
    eski = (BM.X0, BM.Y0, BM.Z0, list(BM.PARCALAR))
    try:
        BM.X0, BM.Y0, BM.Z0 = BULASIK_YER
        out = [(p["ad"], BM.dunya(p).translate(cq.Vector(-X_K_HAT, 0.0, 0.0))) for p in BM.kur()]
        kx, ky, kz = BM.kapi_acik_zarf()
    finally:
        BM.X0, BM.Y0, BM.Z0 = eski[:3]
        BM.PARCALAR[:] = eski[3]
    return out, ((kx[0] - X_K_HAT, kx[1] - X_K_HAT), ky, kz)


def taban():
    """v4 · ALÇAK HAT: K tabanının altı — bulaşık makinesi REF (ayrı modül) · v5: kanister rafı + deterjan / parlatıcı + dozaj hortumları KALKTI (Kemal) ·
    v6: bulaşık TABLASI (Kemal: "alt ayaklarını kaldır") — 2 × 40×20×2 kiriş (yan saclara kaynaklı, K taban sacına oturur) + 3 mm tava (makine buna oturur)"""
    for ad_, sh in bulasik_parcalari()[0]:
        ekle("REF_bulasik_" + ad_, cq.Workplane(obj=sh), "referans", "REF")
    yk0 = Y_PLINT + 3.0; kz, ky, kt = TABLA_KIRIS
    for i, zc in enumerate((BULASIK_YER[2] - 30.0, BULASIK_YER[2] - BM.D + 30.0)):          # makinenin eski ayak hatları (z −50 / −590): gövde köşeleri kirişin üstünde
        ekle("bulasik_tabla_kirisi_%d" % i, kut(SAC, W - SAC, yk0, yk0 + ky, zc - kz / 2.0, zc + kz / 2.0).cut(
             kut(SAC - 1.0, W - SAC + 1.0, yk0 + kt, yk0 + ky - kt, zc - kz / 2.0 + kt, zc + kz / 2.0 - kt)), "sac",
             bom=("Tabla kirişi · kutu profil 40 × 20 × 2 AISI 304", 2, "boy %.0f · yan saclara kaynaklı · K taban sacına oturur" % (W - 2 * SAC),
                  "v6 · makine köşeleri (eski ayak hattı z −50 / −590) kirişin üstünde") if i == 0 else None)
    xa, xb = BULASIK_YER[0] - X_K_HAT - 4.0, BULASIK_YER[0] - X_K_HAT + BM.W + 4.0
    za, zb = BULASIK_YER[2] - BM.D - 4.0, BULASIK_YER[2] + 4.0
    tv = kut(xa, xb, Y_TABLA - TAVA_BM, Y_TABLA, za, zb)
    for z0_, z1_ in ((zb - TAVA_BM, zb), (za, za + TAVA_BM)):                                  # ön + arka kenar 15 AŞAĞI bükülü (kirişlerin arasında kalır)
        tv = tv.union(kut(xa, xb, Y_TABLA - TAVA_BM - 15.0, Y_TABLA - TAVA_BM, z0_, z1_))
    ekle("bulasik_tavasi", tv, "sac", bom=("Bulaşık tabla tavası 3 mm AISI 304", 1, "%.0f × %.0f · ön + arka kenar 15 aşağı bükülü" % (xb - xa, zb - za),
                                          "v6 · MEIKO ayaksız buna oturur (+13) · kirişlere kaynak"))
    # 2. tur (denetçi K-8): bağlantı geçişleri — gövde delikte (y 123–126, delik duvarına değer) + üst başlık / flanş taban sacının üstünde
    # (alt dudak / kilit somunu plint boşluğunda ~2 mm — modelde yok: taban çizgisi 123'ün altında yalnız ayak + plint)
    for k_, (gx, gz, gr, ri, ro, hh) in GECIS.items():
        ad_ = ("bulasik_gecis_rakoru_" if k_ == "elektrik" else "bulasik_gecis_lastigi_") + k_
        sh = sily(gx, gz, gr, Y_PLINT, Y_PLINT + 3.0).union(sily(gx, gz, ro, Y_PLINT + 3.0, Y_PLINT + 3.0 + hh)).cut(sily(gx, gz, ri, Y_PLINT - 1.0, Y_PLINT + 4.0 + hh))
        ekle(ad_, sh, "siyah" if k_ == "elektrik" else "conta",
             bom=(("Kablo rakoru Lapp SKINTOP MS-M 20×1,5 (paslanmaz / pirinç, IP68)", 1, "bulaşık besleme kablosu (sıkma 7–13) · taban sacı delik Ø20,5 · kilit somunu altta",
                   "lappgroup.com SKINTOP MS-M · parça no teyit (ör. 53112020) · ölçü VARSAYIM") if k_ == "elektrik" else
                  ("Geçiş lastiği EPDM (grommet) · %s hortumu" % k_, 1, "delik Ø%.0f · iç Ø%.0f · flanş Ø%.0f" % (2 * gr, 2 * ri, 2 * ro),
                   "VARSAYIM ölçü · genel katalog (parça no yok)")))


# ---------------------------------------------------------------- 8 · ÜRÜN + REFERANSLAR ----------------------------------------------------------------
def urun_ref():
    ekle("urun_hamur", sily(XC, ZC, PZ_R, BANT, BANT + 10.0), "hamur", "URUN")
    ekle("urun_ustu", sily(XC, ZC, 142.0, BANT + 10.0, BANT + PZ_H), "kasar_ust", "URUN")
    for i in range(6):
        ekle("urun_kesik_%d" % i, radyal(0.0, 146.0, 2.0, BANT + PZ_H, BANT + PZ_H + 0.6, 60.0 * i), "kesik", "URUN_IZ")
    ekle("REF_firin_bandi_ucu", kut(-120.0, 15.0, 936.5, FIRIN_BANDI, -315.0, -25.0), "referans", "REF")
    ekle("REF_E_sol_duvar", kut(W, W + SAC, 832.0, 1232.0, -420.0, 0.0).cut(kut(W - 1, W + SAC + 1, E_PENCERE[0], E_PENCERE[1], E_PENCERE[2], E_PENCERE[3])), "referans", "REF")
    ekle("REF_E_koprusu", kut(W + 2.0, W + 92.0, KC.KALIP - 6.0, KC.KALIP, -372.0, -40.0), "referans", "REF")
    # v4: REF_kompresor_JUNAIR kalktı (kompresör v48'den beri fırın üstünde; yeri artık bulaşık makinesi)


# ---------------------------------------------------------------- KİNEMATİK (GLB + tarama + ana montaj aynı fonksiyonları çağırır) ----------------------------------------------------------------
DONGU = 20.0
Z_GELIS = (0.3, 2.3)
Z_SPREY = (2.6, 3.8)
Z_INIS, Z_KES, Z_BEKLE, Z_KALK = (4.0, 4.6), (4.6, 5.4), (5.4, 5.7), (5.7, 6.5)
Z_TASI = (6.8, 7.8)
Z_GERI = (6.9, 7.9)
Z_IN = (7.95, 8.3)
Z_YAKLAS = (8.3, 8.5)
Z_ITME = KC.Z_PIZZA[:2]           # (8,5 · 10,1) — kutu modülüyle aynı
Z_DON = (10.3, 10.9)
Z_KALDIR = (11.0, 11.3)
HIZLI = 95.0                      # hızlı iniş yolu (kalan 30 mm yavaş kesim)
ss, lin = KC.ss, KC.lin


def kesici_dy(t):
    if t < Z_INIS[0]: return 0.0
    if t < Z_INIS[1]: return -HIZLI * ss(Z_INIS[0], Z_INIS[1], t)
    if t < Z_KES[1]: return -HIZLI - (STROK - HIZLI) * lin(Z_KES[0], Z_KES[1], t)
    if t < Z_BEKLE[1]: return -STROK
    return -STROK * (1.0 - ss(Z_KALK[0], Z_KALK[1], t))


def cit_z(xc):
    """çit ürünün merkezini ne kadar içeri iter (xc'de)"""
    z = CIT_P0[1] - (PZ_R + (xc - CIT_P0[0]) * math.sin(_ca)) / math.cos(_ca)
    return min(ZC, max(ZB, z))


def yuz(t):
    """itici yüzünün x'i"""
    if t < Z_GERI[0]: return YUZ_BEKLE
    if t < Z_GERI[1]: return YUZ_BEKLE + (YUZ_BAS - YUZ_BEKLE) * ss(Z_GERI[0], Z_GERI[1], t)
    if t < Z_YAKLAS[0]: return YUZ_BAS
    if t < Z_YAKLAS[1]: return YUZ_BAS + 5.0 * ss(Z_YAKLAS[0], Z_YAKLAS[1], t)
    if t < Z_ITME[1]: return YUZ_BAS + 5.0 + (YUZ_SON - YUZ_BAS - 5.0) * ss(Z_ITME[0], Z_ITME[1], t)
    if t < Z_DON[0]: return YUZ_SON
    return YUZ_SON + (YUZ_BEKLE - YUZ_SON) * ss(Z_DON[0], Z_DON[1], t)


def itici_dy(t):
    """0 = aşağıda (itme), +60 = yukarıda"""
    if t < Z_IN[0]: return ITICI_KALK
    if t < Z_IN[1]: return ITICI_KALK * (1.0 - ss(Z_IN[0], Z_IN[1], t))
    if t < Z_KALDIR[0]: return 0.0
    return ITICI_KALK * ss(Z_KALDIR[0], Z_KALDIR[1], t)


def urun_merkez(t):
    """ürün merkezi (x, alt yüz y, z) — 10,1 sn'ye kadar; sonrası kutu modülünün pizza_trs'i"""
    if t < Z_GELIS[1]:
        x = -60.0 + (XC + 60.0) * ss(Z_GELIS[0], Z_GELIS[1], t)
    elif t < Z_TASI[0]:
        x = XC
    elif t < Z_ITME[0]:
        x = XC + (X_TASI - XC) * ss(Z_TASI[0], Z_TASI[1], t)
    else:
        x = X_TASI + (X_SON - X_TASI) * ss(Z_ITME[0], Z_ITME[1], t)
    z = cit_z(x)
    # ürün RİJİT disk: arka kenarı ölü plakayı (x 597) geçmeden inmez — yoksa bant rulosuna gömülür (tarama buldu).
    # Kutu modülünün 10,1 sn'deki yeri (merkez 860, kalıp kotu) aynen korunur.
    if x - PZ_R <= X_OLU: y = BANT
    elif x <= X_OLU + PZ_R + 53.0: y = BANT + (KC.KALIP - BANT) * (x - X_OLU - PZ_R) / 53.0
    else: y = KC.KALIP
    if x < 15.0: y = FIRIN_BANDI                                   # fırın bandının üstünde
    y += (KC.TEPSI + KC.T - KC.KALIP) * ss(KC.Z_PIZZA[1], KC.Z_PIZZA[2], t)
    return (x, y, z)


def urun_trs(t):
    x, y, z = urun_merkez(t)
    return (x - XC, y - BANT, z - ZC)


def urun_gorunur(t):
    return 1.0 if t < KC.Z_PIZZA[2] else 0.0


def sprey_gorunur(t, pide=True):
    return 1.0 if pide and Z_SPREY[0] <= t < Z_SPREY[1] else 0.0


def kesik_olcek(t):
    return 1.0 if Z_KES[0] + 0.3 <= t < KC.Z_PIZZA[2] else 0.0


def grup_trs(g, t):
    if g == "KESICI": return (0.0, kesici_dy(t), 0.0)
    if g == "ITICI_ARABA": return (yuz(t) - YUZ_BEKLE, 0.0, 0.0)
    if g == "ITICI_KOL": return (yuz(t) - YUZ_BEKLE, itici_dy(t) - ITICI_KALK, 0.0)
    if g in ("URUN", "URUN_IZ"): return urun_trs(t)
    return (0.0, 0.0, 0.0)


def kapak_ac(sh, aci):
    """v6 · kapak grubu katısı (Shape) → SOL gizli menteşenin sanal pivotu (x 3, z 79, dikey eksen) etrafında 'aci' derece AÇIK (öne-sola döner).
    Kapaklar yalnız servis içindir: çevrimde (grup_trs) KAPALI kalır."""
    x, z = MENTESE_EKSEN
    return sh.rotate(cq.Vector(x, 0.0, z), cq.Vector(x, 1.0, z), -aci)


# ---------------------------------------------------------------- MODÜL ----------------------------------------------------------------
def modul():
    PARCALAR[:] = []
    govde(); kapaklar(); bant(); kesici(); sprey_sistemi(); itici(); elektrik(); taban(); urun_ref()      # v6: kapaklar()
    # itici modelde YUKARIDA (t = 0 duruşu) çizilir: kol parçalarını +60 kaldır
    for p in PARCALAR:
        if p["grup"] == "ITICI_KOL":
            p["wp"] = p["wp"].translate((0, ITICI_KALK, 0))
    return PARCALAR


# ---------------------------------------------------------------- HESAP + DENETİM ----------------------------------------------------------------
DEN = []


def kontrol(ad, sart, deger=""):
    DEN.append((ad, bool(sart), deger)); print("  %-78s %s %s" % (ad, "GEÇTİ" if sart else "** KALDI **", deger))


def bbx(ad):
    return [p for p in PARCALAR if p["ad"] == ad][0]["wp"].val().BoundingBox()


def tasi(sh, v):
    return sh.translate(cq.Vector(*v))


def hesap():
    H_ = {}
    kenar = 6 * (BICAK_R1 - BICAK_R0)
    H_["bicak_kenar_mm"] = kenar
    H_["kuvvet_kN"] = (kenar * 1.0 / 1000.0, kenar * 3.0 / 1000.0)
    F63 = 0.6 * math.pi / 4 * 63 ** 2
    H_["silindir_N"] = F63
    V = (math.pi / 4 * 63 ** 2 * STROK + math.pi / 4 * (63 ** 2 - 20 ** 2) * STROK) / 1e6
    H_["hava_NL_kesim"] = V * (6.0 + 1.013) / 1.013
    H_["hava_NL_dk_60h"] = H_["hava_NL_kesim"] * 60 / 60.0
    H_["yag_g_gun"] = 80 * SPREY_G
    H_["yag_L_2gun"] = 2 * 80 * SPREY_G / 0.91 / 1000.0
    H_["sprey_sn"] = SPREY_G / SPREY_DEBI
    H_["koni_r_mm"] = (Y_UC - 6.0 - (BANT + PZ_H)) * math.tan(math.radians(45.0))
    H_["kesim_hiz"] = (STROK - HIZLI) / (Z_KES[1] - Z_KES[0])
    H_["itme_vmax"] = 1.5 * (X_SON - X_TASI) / (Z_ITME[1] - Z_ITME[0])
    return H_


def denetim():
    print("DENETİM (kesme_cad_v6)")
    H_ = hesap()
    # zarf
    tasan = []
    for p in PARCALAR:
        if p["grup"] in ("URUN", "URUN_IZ", "REF", "SPREY") or p["ad"].endswith("_kulp") or p["ad"] == "acil_stop":
            continue
        b = p["wp"].val().BoundingBox()
        if b.xmin < -0.5 or b.xmax > W + 0.5 or b.ymin < -0.5 or b.ymax > H + 0.5 or b.zmin < -D - 0.5 or b.zmax > Z_ON + 0.5:
            tasan.append(p["ad"])
    kontrol("zarf %.0f × %.0f × (%.0f + %.0f) içinde: z −830…+79,5 (v6: ön düzlem +79 · kapaklar kapalı)" % (W, H, D, Z_ON), not tasan, ", ".join(tasan))
    alta = [p["ad"] for p in PARCALAR if p["grup"] == "SABIT" and p["wp"].val().BoundingBox().ymin < Y_PLINT - 0.5 and not p["ad"].startswith(("ayak_", "onyuz_plint"))]
    kontrol("alt taban çizgisi %.0f: altında yalnız ayak + süpürgelik" % Y_PLINT, not alta, ", ".join(alta))
    kontrol("istasyon tabanı %.0f" % H_B, abs(bbx("istasyon_tabani_3").ymin - H_B) < 0.01)
    kontrol("K bandı üstü %.1f = fırın bandı %.0f − 2 (ürün hep aşağı iner)" % (bbx("bant_PU_2mm").ymax, FIRIN_BANDI), abs(bbx("bant_PU_2mm").ymax - BANT) < 0.01 and BANT < FIRIN_BANDI)
    ag = min(bbx("bicak_%d" % i).ymin for i in range(6)) + kesici_dy(5.5)
    kontrol("bıçak ağzı alt dayamada bandın %.1f mm üstünde (bandı kesmez)" % (ag - BANT), 0.3 <= ag - BANT <= 1.0)
    kontrol("kafa yukarıda: bıçak ağzı ürünün %.0f mm üstünde (ürün ≤ 50)" % (Y_AGIZ_UST - BANT - 50.0), Y_AGIZ_UST - BANT - 50.0 >= 40.0)
    iy = bbx("itici_POM_yuz").ymin                      # t = 0: yukarıda
    kontrol("itici yukarıda: altı ürünün (15) %.0f mm üstünde" % (iy - BANT - PZ_H), iy - BANT - PZ_H >= 30.0)
    kontrol("itici yukarıda: üstü (%.0f) kafa yukarıdayken bıçak ağzının (%.1f) altında" % (bbx("itici_POM_yuz").ymax, Y_AGIZ_UST), bbx("itici_POM_yuz").ymax < Y_AGIZ_UST - 10.0)
    kontrol("itici aşağıda banttan %.0f mm yukarıda" % (Y_ITICI[0] - BANT), 2.0 <= Y_ITICI[0] - BANT <= 5.0)
    kontrol("çit koruma halkasından %.1f mm uzakta" % (CIT_R - KORUMA_R[1]), CIT_R - KORUMA_R[1] >= 1.5)
    kontrol("çit kaydırması x %.0f'de biter (E'nin varsayımı 440 · E penceresine giriş 450)" % min(x for x in range(300, 600) if cit_z(x) <= ZB + 0.01), min(x for x in range(300, 600) if cit_z(x) <= ZB + 0.01) <= 450)
    y0, y1, z0, z1 = E_PENCERE
    iz = bbx("itici_POM_yuz")
    kontrol("itici E penceresinden geçer (y %.0f–%.0f, z %.0f…%.0f)" % (Y_ITICI[0], Y_ITICI[1], ITICI_Z[0], ITICI_Z[1]), y0 < Y_ITICI[0] and Y_ITICI[1] < y1 and z0 < ITICI_Z[0] and ITICI_Z[1] < z1)
    kontrol("itici E'ye %.0f mm girer (E'nin varsayımı 110)" % (YUZ_SON - W), abs(YUZ_SON - W - 110.0) < 0.5)
    kontrol("itici kolu E'ye girmez (kol x ≤ %.0f < %.0f)" % (YUZ_SON - ITICI_ONU + 100.0, W - SAC), YUZ_SON - ITICI_ONU + 100.0 < W - SAC)
    ex = bbx("ZLW-1040_eksen_profili"); ec = [bbx("ZLW_uc_blogu_0"), bbx("ZLW_uc_blogu_1")]
    ca = YUZ_BAS - ITICI_ONU; cb = YUZ_SON - ITICI_ONU
    kontrol("araba stroku %.0f (araba merkezi %.0f → %.0f) eksen profilinde (%.0f…%.0f)" % (cb - ca, ca, cb, ex.xmin, ex.xmax), ca - 50 >= ex.xmin - 0.5 and cb + 50 <= ex.xmax + 0.5)
    kontrol("ürün E'ye girerken (merkez 450) z %.1f = kutu ekseni %.0f" % (urun_merkez(9.0)[2] if False else cit_z(450.0), ZB), abs(cit_z(450.0) - ZB) < 0.5)
    kontrol("itme zamanı kutu modülüyle aynı (%.1f–%.1f sn) · son merkez %.0f (E yereli %.0f)" % (Z_ITME[0], Z_ITME[1], X_SON, X_SON - W), abs(urun_merkez(Z_ITME[1])[0] - X_SON) < 0.5)
    kontrol("kesim itmeden önce biter (kafa %.1f sn'de yukarıda)" % Z_KALK[1], Z_KALK[1] < Z_TASI[0] and Z_KALK[1] < Z_GERI[0])
    kontrol("kesme kuvveti %.1f–%.1f kN [V: 1–3 N/mm × %.0f mm] · DGRF-C-63 %.0f N → %s" % (H_["kuvvet_kN"][0], H_["kuvvet_kN"][1], H_["bicak_kenar_mm"], H_["silindir_N"],
            "yeter (≤ 2,3 N/mm)" if H_["silindir_N"] / H_["bicak_kenar_mm"] >= 2.0 else "PİLOTTA ÖLÇ"), H_["silindir_N"] / H_["bicak_kenar_mm"] >= 2.0)
    kontrol("hava: kesim başına %.1f NL · saatte 60 ürünle %.1f NL/dk (kompresör 43 L/dk; TOPPING ~1,7)" % (H_["hava_NL_kesim"], H_["hava_NL_dk_60h"]), H_["hava_NL_dk_60h"] + 1.7 < 43.0 * 0.5)
    kontrol("tereyağı: pide başına %.0f g · günde %.0f g · 2 gün %.2f L < tank %.0f L" % (SPREY_G, H_["yag_g_gun"], H_["yag_L_2gun"], TANK_L), H_["yag_L_2gun"] < TANK_L * 0.7)
    kontrol("sprey %.2f sn (pencere %.1f sn) · koni yarıçapı ürün üstünde %.0f mm (ürün 140–150)" % (H_["sprey_sn"], Z_SPREY[1] - Z_SPREY[0], H_["koni_r_mm"]), H_["sprey_sn"] <= Z_SPREY[1] - Z_SPREY[0] and 140 <= H_["koni_r_mm"] <= 160)
    denetim_v6(H_)
    return H_


UYARI = []


def _sek(ad):
    L = [p for p in PARCALAR if p["ad"] == ad]
    assert len(L) == 1, ad
    return L[0]["wp"].val()


def _mesafe(a, b):
    """gerçek katı aralığı (mm) · OCC BRepExtrema"""
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape
    sa = _sek(a) if isinstance(a, str) else a; sb = _sek(b) if isinstance(b, str) else b
    x = BRepExtrema_DistShapeShape(sa.wrapped, sb.wrapped)
    return x.Value() if x.IsDone() else 1e9


def isi_dT(Q, A, h, Cd=0.6, T=298.0):
    """doğal çekiş (baca etkisi) · alt + üst eşit açıklık seri (A_eff = A/√2) · Q = ρ·cp·ΔT·Cd·A_eff·√(2·g·h·ΔT/T) → ΔT [K]"""
    k = 1.2 * 1005.0 * Cd * (A / math.sqrt(2.0)) * math.sqrt(2.0 * 9.81 * h / T)
    return (Q / k) ** (2.0 / 3.0)


def denetim_v6(H_):
    """v6 · ÖN DÜZLEM +79 (SPEC_on_duzlem_v63 §2.5) — hepsi katılardan ölçülür:
    1 kotlar + E arayüzü · 2 v5 ↔ v6 parça parça (değişen / yeni / çıkan listeleri beklenenle birebir) · 3 kinematik v5 ile aynı ·
    4 ön düzlem +79 / kabuk +59 / plint / derz / tava · 5 yük yolu temasları · 6 kapaklar (kinematik + 0–90° tarama) ·
    7 bulaşık v2 (tabla, zarf, kapak açık zarfı ALT kapak AÇIKKEN) · 8 havada parça = 0 · 9 hesaplar (köprü, tabla, kapak, ısı VARSAYIM) · 10 açıklıklar"""
    import dilim_v1 as DL
    import kesme_cad_v5 as V5
    import denetim_temas_v1 as DT
    import firin_tp10_cad_v8 as FT8                                                    # 2. tur (denetçi K-13): güncel fırın sürümü (ZS 79 aynı)
    def kutu_(x, y, z):
        return cq.Solid.makeBox(x[1] - x[0], y[1] - y[0], z[1] - z[0], cq.Vector(x[0], y[0], z[0]))
    def giren(bolge, liste):
        L = []; B_ = bolge.BoundingBox()
        for p, sh in liste:
            if not KC._bb_kesisir(sh.BoundingBox(), B_): continue
            v = sh.intersect(bolge).Volume()
            if v > 0.01: L.append((p["ad"], round(v, 1)))
        return L
    # ---- 1 · kotlar + E arayüzü (v5 ile aynı) ----
    ts = bbx("istasyon_tabani_3"); ust = max(p["wp"].val().BoundingBox().ymax for p in PARCALAR if p["grup"] == "SABIT")
    H_["taban_ust"] = ts.ymax; H_["bant"] = bbx("bant_PU_2mm").ymax; H_["ust"] = ust
    kontrol("ALÇAK HAT kotları (v5 ile aynı): üst %.1f · istasyon tabanı sacı %.0f–%.0f · K bandı %.1f · fırın bandı %.0f · ürün girişi %.0f–%.0f"
            % (ust, ts.ymin, ts.ymax, H_["bant"], FIRIN_BANDI, URUN_GIRISI[0], URUN_GIRISI[1]),
            abs(ust - 1862.0) < 0.01 and abs(ts.ymin - 892.0) < 0.01 and abs(H_["bant"] - 996.0) < 0.01 and abs(FIRIN_BANDI - 998.0) < 0.01)
    kontrol("E arayüzü kutu_cad_v6: E plakası %.1f = K bandı %.1f · E penceresi %.0f–%.0f = K'deki · E kalıbı %.1f · tepsi %.0f" % (KC.PLAKA_K, BANT, KC.PENCERE[0], KC.PENCERE[1], KC.KALIP, KC.TEPSI),
            KC.__name__ == "kutu_cad_v6" and abs(KC.PLAKA_K - BANT) < 0.01 and all(abs(a - b) < 0.01 for a, b in zip(KC.PENCERE, E_PENCERE)))
    kontrol("ön düzlem sözleşmesi: Z_ON %.1f = firin_tp10_cad_v8.ZS %.1f (fırın gövdesinin ön yüzü, değişmez referans) · arka %.0f → derinlik %.0f" % (Z_ON, FT8.ZS, Z_ARKA, Z_ON - Z_ARKA),
            abs(Z_ON - FT8.ZS) < 1e-9 and abs(Z_ARKA + 830.0) < 1e-9)
    # 2. tur (denetçi K-13): E'nin montaj v63 sürümü kutu_cad_v7 — K'nin kullandığı arayüz sabitleri v6 ile AYNI mı (ürün × E v7 / itici × E v7 taraması __main__'de, e7_ileri)
    try:
        import kutu_cad_v7 as KC7
    except Exception as e_:
        KC7 = None; UYARI.append("E v7 (kutu_cad_v7) yüklenemedi: %s — ileri uyum denetlenemedi" % e_)
    if KC7 is not None:
        ARA_ = ("PLAKA_K", "PENCERE", "KALIP", "TEPSI", "T", "ZB", "Z_PIZZA")
        fk_ = [a_ for a_ in ARA_ if getattr(KC, a_) != getattr(KC7, a_)]
        H_["E_v7_arayuz"] = {a_: [getattr(KC, a_), getattr(KC7, a_)] for a_ in ARA_}
        kontrol("E ileri uyum (kutu_cad_v7 = montaj v63'ün E'si): %s kutu_cad_v6 ile AYNI → K'nin ürün yolu / itici arayüzü değişmez (ürün × E v7 + itici × E v7 taraması: __main__ e7_ileri)"
                % " · ".join(ARA_), not fk_, str(fk_))
    # ---- 2 · v5 ↔ v6 parça parça ----
    V5.modul()
    k = DL.karsilastir(PARCALAR, V5.PARCALAR)
    fark_ad = sorted(set(f.split(":")[0] for f in k["fark"]))
    yeni = sorted(k["yeni_ek"]); cikan = sorted(k["ref_eksik"])
    fark_k = [a for a in fark_ad if not a.startswith("REF_bulasik_")]
    fark_bm = [a for a in fark_ad if a.startswith("REF_bulasik_")]
    bm_ortak = sorted(p["ad"] for p in V5.PARCALAR if p["ad"].startswith("REF_bulasik_") and p["ad"] not in cikan)
    V5P = {p["ad"]: p["wp"].val() for p in V5.PARCALAR}
    dy = BULASIK_YER[1] - V5.BULASIK_YER[1]
    bm_kay = []
    for a in bm_ortak:                                                                 # bulaşık v1 → v2: ortak parçalar tam +13 y (filtre: + göbek deliği)
        b6, b5 = bbx(a), V5P[a].BoundingBox()
        ot = max(abs(b6.xmin - b5.xmin), abs(b6.xmax - b5.xmax), abs(b6.ymin - b5.ymin - dy), abs(b6.ymax - b5.ymax - dy), abs(b6.zmin - b5.zmin), abs(b6.zmax - b5.zmax))
        dv = _sek(a).Volume() - V5P[a].Volume()
        if ot > 0.01 or (abs(dv) > 0.5 and a != "REF_bulasik_miclean_filtre"): bm_kay.append((a, round(ot, 3), round(dv, 1)))
    yeni_x = [a for a in yeni if not a.startswith(YENI_V6)]
    H_["v5_v6"] = dict(v5=len(V5.PARCALAR), v6=len(PARCALAR), ayni=len(k["ayni"]), degisen=fark_ad, yeni=yeni, cikan=cikan, bulasik_dy=dy)
    kontrol("v5 ↔ v6 (dilim_v1.karsilastir: sınır kutusu ±0,01 + hacim): v5 %d → v6 %d parça · birebir %d · değişen %d (K %d + bulaşık REF %d, hepsi +%.0f y) · yeni %d · çıkan %d — listeler beklenenle birebir"
            % (len(V5.PARCALAR), len(PARCALAR), len(k["ayni"]), len(fark_ad), len(fark_k), len(fark_bm), dy, len(yeni), len(cikan)),
            fark_k == sorted(V6_DEGISEN) and cikan == sorted(V6_CIKAN) and not yeni_x and fark_bm == bm_ortak and not bm_kay and abs(dy - 13.0) < 0.01
            and len(k["ayni"]) == len(V5.PARCALAR) - len(cikan) - len(fark_ad),
            "değişen fazla %s eksik %s · çıkan %s · yeni tanımsız %s · bulaşık kayma %s" % (sorted(set(fark_k) - set(V6_DEGISEN)), sorted(set(V6_DEGISEN) - set(fark_k)), cikan, yeni_x, bm_kay))
    print("     v5 → v6 DEĞİŞEN (K, %d): %s" % (len(fark_k), ", ".join(fark_k)))
    print("     v5 → v6 DEĞİŞEN (bulaşık REF +13, %d): %s" % (len(fark_bm), ", ".join(fark_bm)))
    print("     v5 → v6 ÇIKAN (%d): %s" % (len(cikan), ", ".join(cikan)))
    print("     v6 YENİ (%d): %s" % (len(yeni), ", ".join(yeni)))
    dk_, dsum = [], 0.0
    for a in V6_DELIK:
        b6, b5 = bbx(a), V5P[a].BoundingBox()
        ot = max(abs(b6.xmin - b5.xmin), abs(b6.xmax - b5.xmax), abs(b6.ymin - b5.ymin), abs(b6.ymax - b5.ymax), abs(b6.zmin - b5.zmin), abs(b6.zmax - b5.zmax))
        dv = _sek(a).Volume() - V5P[a].Volume(); dsum += dv
        if ot > 0.05 or dv > -0.01: dk_.append((a, round(ot, 3), round(dv, 1)))
    H_["v6_delik"] = {a: round(_sek(a).Volume() - V5P[a].Volume(), 1) for a in V6_DELIK}
    kontrol("2. tur · yalnız DELİK / YUVA / KESİM açılan %d parça (rulo mil yuvaları, yan levha delikleri + gergi yarığı, bant şeridi, göbek yuvaları, DIN klipsi, kelepçe, eksen ayağı): "
            "sınır kutusu v5 ile AYNI (±0,05; göbek yuva ağzı 0,014) · hacim yalnız AZALDI (Σ %.0f mm³) → zarf ve işlev değişmedi" % (len(V6_DELIK), dsum), not dk_, str(dk_ or H_["v6_delik"]))
    kk_ = bbx("kablo_kanali_dikey"); dir_ = bbx("sprey_dirsegi")
    kontrol("2. tur · taşınan / kısalan: kablo_kanali_dikey z %.1f…%.1f (arka köşe dikmesinin önü −798,5; v5 −822…−797 dikmenin içindeydi) · sprey_dirsegi x ≤ %.1f (PulsaJet ucu 305) · koruma braketleri r ≥ 115 (kafa plakası kenarı)"
            % (kk_.zmin, kk_.zmax, dir_.xmax), abs(kk_.zmin - (-D + SAC + 30.0)) < 0.01 and dir_.xmax <= 306.0 + 0.01)
    # ---- 3 · kinematik v5 ile AYNI ----
    fu = max(max(abs(a - b) for a, b in zip(urun_merkez(t), V5.urun_merkez(t))) for t in [i * 0.05 for i in range(401)])
    fg = max(max(abs(a - b) for a, b in zip(grup_trs(g, t), V5.grup_trs(g, t))) for g in ("KESICI", "ITICI_ARABA", "ITICI_KOL", "URUN", "URUN_IZ") for t in [i * 0.1 for i in range(201)])
    kontrol("kinematik v5 ile AYNI: urun_merkez(t) 401 an · en büyük fark %.4f mm · grup_trs(t) 201 an × 5 grup %.4f (kapaklar yalnız servis — çevrimde KAPALI)" % (fu, fg), fu < 1e-9 and fg < 1e-9)
    # ---- 4 · ön düzlem · kabuk · plint · derz · tava ----
    ONG = [p for p in PARCALAR if p["grup"] not in ("REF", "URUN", "URUN_IZ", "SPREY")]
    zmx = max(p["wp"].val().BoundingBox().zmax for p in ONG)
    kap = [bbx("onyuz_kapak_%s" % a) for _g, a, _y0, _y1 in KAPAKLAR]
    kontrol("ÖN DÜZLEM: 3 kapağın dış yüzü z %s = Z_ON %.1f · tava 20 → arka kenar z %s · K'nin en ön noktası %.2f ≤ %.1f"
            % ("/".join("%.2f" % b.zmax for b in kap), Z_ON, "/".join("%.2f" % b.zmin for b in kap), zmx, Z_ON + 0.5),
            len(kap) == 3 and all(abs(b.zmax - Z_ON) < 0.01 and abs(b.zmin - Z_TAVA[0]) < 0.01 for b in kap) and zmx <= Z_ON + 0.01)
    on59 = [p for p in ONG if p["wp"].val().BoundingBox().zmax > Z_KABUK_ON + 0.01]
    yab = [p["ad"] for p in on59 if p["grup"] not in KAPAK_GRUP and not p["ad"].startswith("onyuz_basac_mandal_")]
    H_["on59"] = sorted(p["ad"] for p in on59)
    kontrol("+59'un önünde YALNIZ kapak grupları (tava + menteşe kanadı + mandal karşılığı + kilit dili) + kapak boşluğuna giren 3 bas-aç mandalı (z ≤ %.0f): %d parça"
            % (Z_CER[1] + MANDAL["derin"], len(on59)), not yab, str(yab))
    kab = [(a, bbx(a)) for a in ("ust_sac", "sol_sac_urun_girisi", "sag_sac_E_penceresi", "taban_sac_3", "istasyon_tabani_3")]
    kontrol("kabuk ön kenarı +%.0f (kapak arkası): %s · arka sac z %.1f (SABİT) → gövde derinliği %.0f"
            % (Z_KABUK_ON, " · ".join("%s %.2f" % (a, b.zmax) for a, b in kab), bbx("arka_sac").zmin, Z_ON - bbx("arka_sac").zmin),
            all(abs(b.zmax - Z_KABUK_ON) < 0.01 for _a, b in kab) and abs(bbx("arka_sac").zmin + 830.0) < 0.01 and abs(Z_ON - bbx("arka_sac").zmin - 909.0) < 0.01)
    pb = bbx("onyuz_plint"); pv = _sek("onyuz_plint").Volume()
    pv_b = W * Y_PLINT * TAVA_T + 2 * TAVA_T * Y_PLINT * (Z_PLINT[0] + D - SAC) + (W - 2 * TAVA_T) * TAVA_T * PLINT_FLANS
    kontrol("plint onyuz_plint (2. tur): ön yüz z %.1f…%.1f (ön düzlemin %.0f gerisi) · y %.0f–%.0f (SPEC 0–123) · x %.0f–%.0f (E v7 plinti x 600'den devam: tek çizgi) · "
            "yan dönüşler TAM DERİNLİK → z %.1f · üst flanş %.0f · hacim %.0f = beklenen %.0f · eski plint_on YOK"
            % (Z_PLINT[0], pb.zmax, Z_ON - pb.zmax, pb.ymin, pb.ymax, pb.xmin, pb.xmax, pb.zmin, PLINT_FLANS, pv, pv_b),
            abs(pb.zmax - Z_PLINT[1]) < 0.01 and abs(Z_ON - pb.zmax - 60.0) < 0.01 and abs(pb.ymin) < 0.01 and abs(pb.ymax - Y_PLINT) < 0.01 and abs(pb.xmin) < 0.01
            and abs(pb.xmax - W) < 0.01 and abs(pb.zmin + D - SAC) < 0.01 and abs(pv - pv_b) < 1.0 and not [p for p in PARCALAR if p["ad"] == "plint_on"])
    # K'nin altı kapalı mı: önden (z +79 → arka) ve yandan (x −10 → 610) ışın — plint ön yüzüne / yan dönüşüne çarpmalı (v6-1: yan cepler + alttaki 10 mm açıktı)
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape as _DSS
    ps_ = _sek("onyuz_plint"); isin = []
    for ad_, a_, b_ in (("ön x 15", (15.0, 60.0, Z_ON), (15.0, 60.0, -D)), ("ön x 585", (585.0, 60.0, Z_ON), (585.0, 60.0, -D)), ("ön y 5", (300.0, 5.0, Z_ON), (300.0, 5.0, -D)),
                        ("yan sol z −400", (-10.0, 60.0, -400.0), (300.0, 60.0, -400.0)), ("yan sağ z −400", (W + 10.0, 60.0, -400.0), (300.0, 60.0, -400.0))):
        e_ = cq.Edge.makeLine(cq.Vector(*a_), cq.Vector(*b_)); x_ = _DSS(ps_.wrapped, e_.wrapped)
        isin.append((ad_, round(x_.Value(), 3)))
    H_["plint_isin"] = isin
    kontrol("K'nin altı KAPALI (ışın testi, 5 ışın): önden x 15 / 585 / y 5 ve yandan x 0 / 600 → hepsi plinte çarpar (aralık 0) · %s" % " · ".join("%s %.2f" % v for v in isin),
            all(v < 1e-6 for _a, v in isin), str(isin))
    ky_ = [(b.ymin, b.ymax) for b in kap]; kx_ = [(b.xmin, b.xmax) for b in kap]
    dz_ = [ky_[i + 1][0] - ky_[i][1] for i in range(len(ky_) - 1)]
    d_f = kx_[0][0]; d_e = X_E_KAPAK0 - (X_K_HAT + kx_[0][1])
    H_["derz"] = dict(yatay=dz_, firin=d_f, E=d_e, kapak_y=ky_, kapak_x_dunya=(X_K_HAT + kx_[0][0], X_K_HAT + kx_[0][1]))
    kontrol("derzler %.0f mm: yatay %s (883/886 · 1305/1308) · alt kenar %.0f · üst kenar %.0f (1862 − 3) · fırın/dolap ↔ K %.1f (x 4000 → %.0f) · K ↔ E %.1f (%.1f → %.1f)"
            % (DERZ, "/".join("%.1f" % v for v in dz_), ky_[0][0], ky_[-1][1], d_f, X_K_HAT + kx_[0][0], d_e, X_K_HAT + kx_[0][1], X_E_KAPAK0),
            all(abs(v - DERZ) < 0.01 for v in dz_) and abs(ky_[0][0] - 126.0) < 0.01 and abs(ky_[-1][1] - (H - DERZ)) < 0.01 and abs(d_f - DERZ) < 0.01 and abs(d_e - DERZ) < 0.01
            and all(abs(a - kx_[0][0]) < 0.01 and abs(b - kx_[0][1]) < 0.01 for a, b in kx_) and abs(ky_[0][1] - 883.0) < 0.01 and abs(ky_[1][1] - 1305.0) < 0.01)
    tv_ = []
    for _g, a, y0, y1 in KAPAKLAR:
        w_, h_ = KAPAK_X[1] - KAPAK_X[0], y1 - y0
        n_ = len(YARIK["bant"].get(a, ())) * len(_yarik_x()) if YARIK_ACIK else 0          # 2. tur: varsayılan YARIKSIZ
        ve = w_ * h_ * TAVA_D - (w_ - 2 * TAVA_T) * (h_ - 2 * TAVA_T) * (TAVA_D - TAVA_T) - n_ * YARIK["en"] * YARIK["boy"] * TAVA_T
        vg = _sek("onyuz_kapak_%s" % a).Volume()
        tv_.append((a, n_, vg, ve, vg * RHO_304))
    H_["kapak"] = {a: dict(yarik=n_, kg=round(kg_, 2)) for a, n_, _vg, _ve, kg_ in tv_}
    kontrol("tava panel katıdan: sac %.1f + büküm %.0f (hacim = dış kutu − iç boşluk − yarıklar) · %s"
            % (TAVA_T, TAVA_D, " · ".join("%s %.2f kg %d yarık" % (a, kg_, n_) for a, n_, _vg, _ve, kg_ in tv_)), all(abs(vg - ve) < 1.0 for _a, _n, vg, ve, _k in tv_),
            str([(a, round(vg - ve, 2)) for a, _n, vg, ve, _k in tv_]))
    # 2. tur (denetçi ORTA-2 + K-10): lazer yarık yalnız SEÇENEK — varsayılan modelde ön sacda kesik YOK; seçenek katıdan ölçülür (ortalı, paylar eşit, dayama lastiğine denk gelmez)
    yok_ = [a for _g, a, _y0, _y1 in KAPAKLAR if H_["kapak"][a]["yarik"]]
    kontrol("ÖNDEN YALNIZ DÜZ YÜZEY + DERZ (SPEC §1): YARIK_ACIK = %s → 3 kapağın ön sacında kesik %s (v6-1: ALT + ÜST'te 416 yarık varsayılandı)" % (YARIK_ACIK, "YOK" if not yok_ else yok_),
            not YARIK_ACIK and not yok_)
    xs_ = _yarik_x(); sol_ = xs_[0] - KAPAK_X[0]; sag_ = KAPAK_X[1] - (xs_[-1] + YARIK["en"])
    pay_ = {a: (YARIK["bant"][a][0][0] - y0, y1 - YARIK["bant"][a][-1][1]) for _g, a, y0, y1 in KAPAKLAR if a in YARIK["bant"]}
    vs_ = {}
    for _g, a, y0, y1 in KAPAKLAR:
        if a in YARIK["bant"]:
            yk_, ns_ = _yarik(a); t_ = _tava(y0, y1).val(); w_ = t_.cut(yk_)
            vs_[a] = (ns_, t_.Volume() - w_.Volume(), ns_ * YARIK["en"] * YARIK["boy"] * TAVA_T, w_.isValid())
    H_["yarik_secenek"] = dict(acik=YARIK_ACIK, sira=len(xs_), sol_pay=sol_, sag_pay=sag_, dikey_pay=pay_, yarik={a: v[0] for a, v in vs_.items()})
    kontrol("SEÇENEK yarık deseni (katıdan, modele girmez): %d yarık/sıra · ORTALI sol pay %.2f = sağ pay %.2f (v6-1 37 / 45,5) · dikey paylar %s · %s · ALT üst bandı ≤ dayama lastiği %.0f"
            % (len(xs_), sol_, sag_, " · ".join("%s %.0f/%.0f" % (a, p0, p1) for a, (p0, p1) in pay_.items()), " · ".join("%s %d yarık" % (a, v[0]) for a, v in vs_.items()), DAYAMA["y"][0]),
            abs(sol_ - sag_) < 0.01 and all(abs(p0 - p1) < 0.01 for p0, p1 in pay_.values()) and all(abs(v - vb) < 0.5 and ok for _n, v, vb, ok in vs_.values())
            and YARIK["bant"]["alt"][-1][1] <= DAYAMA["y"][0], str(vs_))
    # ---- 5 · yük yolu temasları (gerçek katı aralığı ≤ 0,05) ----
    TEMAS = [("onyuz_cerceve_dikme_sol", "sol_sac_urun_girisi"), ("onyuz_cerceve_dikme_sol", "taban_sac_3"), ("onyuz_cerceve_dikme_sol", "ust_sac"),
             ("onyuz_cerceve_dikme_sag", "sag_sac_E_penceresi"), ("onyuz_cerceve_dikme_sag", "taban_sac_3"), ("onyuz_cerceve_dikme_sag", "ust_sac"),
             ("onyuz_cerceve_dikme_sol", "istasyon_tabani_3"), ("onyuz_cerceve_dikme_sag", "istasyon_tabani_3")]
    TEMAS += [("onyuz_cerceve_kayit_%s" % a, "onyuz_cerceve_dikme_%s" % s_) for a, _y0, _y1 in KAYITLAR for s_ in ("sol", "sag")]
    TEMAS += [("kopru_kirisi_%d" % i, "kopru_kirisi_uc_plakasi_%d" % j) for i in range(2) for j in range(2)]
    TEMAS += [("kopru_kirisi_uc_plakasi_0", "sol_sac_urun_girisi"), ("kopru_kirisi_uc_plakasi_1", "sag_sac_E_penceresi"),
              ("kopru_kirisi_uc_plakasi_0", "onyuz_cerceve_dikme_sol"), ("kopru_kirisi_uc_plakasi_1", "onyuz_cerceve_dikme_sag"),
              ("silindir_baglanti_plakasi", "kopru_kirisi_0"), ("silindir_baglanti_plakasi", "kopru_kirisi_1"),
              ("bulasik_tabla_kirisi_0", "sol_sac_urun_girisi"), ("bulasik_tabla_kirisi_0", "sag_sac_E_penceresi"), ("bulasik_tabla_kirisi_1", "sol_sac_urun_girisi"),
              ("bulasik_tabla_kirisi_1", "sag_sac_E_penceresi"), ("bulasik_tabla_kirisi_0", "taban_sac_3"), ("bulasik_tabla_kirisi_1", "taban_sac_3"),
              ("bulasik_tavasi", "bulasik_tabla_kirisi_0"), ("bulasik_tavasi", "bulasik_tabla_kirisi_1"), ("REF_bulasik_govde_cift_cidar", "bulasik_tavasi"),
              ("onyuz_plint", "taban_sac_3")]
    TEMAS += [("onyuz_mentese_govde_%s_%d" % (a, j), "onyuz_cerceve_dikme_sol") for _g, a, _y0, _y1 in KAPAKLAR for j in range(2)]
    TEMAS += [("onyuz_mentese_kanat_%s_%d" % (a, j), "onyuz_mentese_govde_%s_%d" % (a, j)) for _g, a, _y0, _y1 in KAPAKLAR for j in range(2)]
    TEMAS += [("onyuz_mentese_kanat_%s_%d" % (a, j), "onyuz_kapak_%s" % a) for _g, a, _y0, _y1 in KAPAKLAR for j in range(2)]
    TEMAS += [("onyuz_basac_mandal_%s" % a, "onyuz_cerceve_dikme_sag") for _g, a, _y0, _y1 in KAPAKLAR]
    TEMAS += [("onyuz_kilit_AZM40_%s" % a, "onyuz_cerceve_dikme_sag") for a in AZM_KAPAK]
    # 2. tur: kilit dili ağızda · dayama lastiği · plint dönüşleri yan saclarda · geçişler taban sacında · taşınan kanal / delik-yuva parçaları eşlerine değer
    TEMAS += [("onyuz_kilit_dili_%s" % a, "onyuz_kilit_AZM40_%s" % a) for a in AZM_KAPAK]
    TEMAS += [("onyuz_dayama_lastigi_alt", "onyuz_kapak_alt"), ("onyuz_plint", "sol_sac_urun_girisi"), ("onyuz_plint", "sag_sac_E_penceresi"),
              ("kablo_kanali_dikey", "kose_dikmesi_3"), ("kablo_kanali_dikey", "istasyon_tabani_3"), ("yag_tanki_kelepcesi", "yag_tanki_3L"), ("yag_tanki_kelepcesi", "yag_tanki_kapagi"),
              ("eksen_ayagi_1", "ZLW_uc_blogu_1"), ("eksen_ayagi_1", "ZLW-1040_eksen_profili"), ("tahrik_rulosu_RollerDrive_EC5000", "tahrik_rulosu_mili"),
              ("kuyruk_rulosu", "kuyruk_rulosu_mili"), ("bant_yan_levhasi_0", "tahrik_rulosu_mili"), ("bant_yan_levhasi_1", "kuyruk_rulosu_mili"),
              ("bant_yan_levhasi_0", "bant_gergi_civatasi_0"), ("bant_yan_levhasi_1", "bant_gergi_civatasi_1"), ("bicak_0", "bicak_gobek_halkasi"),
              ("koruma_braketi_0", "kafa_plakasi_8"), ("sprey_dirsegi", "PulsaJet_AA10000AUH_104210"), ("surucu_STP-DRV-4830", "din_rayi_1")]
    TEMAS += [(("bulasik_gecis_rakoru_" if k_ == "elektrik" else "bulasik_gecis_lastigi_") + k_, "taban_sac_3") for k_ in GECIS]
    tm = [(a, b, _mesafe(a, b)) for a, b in TEMAS]
    kotu = [(a, b, round(v, 3)) for a, b, v in tm if v > 0.05]
    kontrol("yük yolu temasları (%d çift, gerçek katı aralığı ≤ 0,05): ön çerçeve ↔ kabuk · kayıt ↔ dikme · köprü kirişi ↔ uç plakası ↔ yan sac + ön dikme · "
            "tabla kirişi ↔ yan sac + taban · tava ↔ kiriş · makine ↔ tava · plint ↔ taban · menteşe / mandal / AZM ↔ çerçeve · menteşe kanadı ↔ kapak" % len(TEMAS), not kotu, str(kotu))
    # ---- 6 · kapaklar: kinematik + 0–90° tarama ----
    kb = kapak_ac(_sek("onyuz_kapak_orta"), KAPAK_MAX).BoundingBox()
    kontrol("kapak kinematiği: SOL menteşe sanal pivotu (x %.1f, z %.1f) · %.0f°'de ORTA kapak x %.1f–%.1f · z %.1f…%.1f (öne-sola açılır, fırın/dolap önüne yaslanır)"
            % (MENTESE_EKSEN + (KAPAK_MAX, kb.xmin, kb.xmax, kb.zmin, kb.zmax)),
            abs(kb.xmin - KAPAK_X[0]) < 0.05 and abs(kb.xmax - (KAPAK_X[0] + TAVA_D)) < 0.05 and abs(kb.zmin - Z_ON) < 0.05 and abs(kb.zmax - (Z_ON + KAPAK_X[1] - KAPAK_X[0])) < 0.05)
    t0 = time.time()
    SAB = [(p, p["wp"].val()) for p in PARCALAR if p["grup"] == "SABIT" or p["ad"].startswith("REF_bulasik_")]
    SAB = [(p, s_, s_.BoundingBox()) for p, s_ in SAB]
    bul, xb, zb, zd_ = {}, [1e9, -1e9], [1e9, -1e9], [1e9]
    ANG = [float(a) for a in range(0, int(KAPAK_MAX) + 1, 5)]
    for g in KAPAK_GRUP:
        dg = SAB + [(p, p["wp"].val(), p["wp"].val().BoundingBox()) for p in PARCALAR if p["grup"] in KAPAK_GRUP and p["grup"] != g]
        kp = [(p, p["wp"].val()) for p in PARCALAR if p["grup"] == g]
        for aci in ANG:
            for p, s_ in kp:
                r = kapak_ac(s_, aci); A = r.BoundingBox()
                xb[0] = min(xb[0], A.xmin); xb[1] = max(xb[1], A.xmax); zb[1] = max(zb[1], A.zmax)
                if p["ad"].startswith("onyuz_kilit_dili_"): zd_[0] = min(zd_[0], A.zmin)                 # 2. tur: dil AZM ağzına girer (z 49)
                else: zb[0] = min(zb[0], A.zmin)
                for q, b, B_ in dg:
                    if not KC._bb_kesisir(A, B_): continue
                    v = r.intersect(b).Volume()
                    if v > 1.0: bul[(g, p["ad"], q["ad"])] = (round(v, 1), aci)
    H_["kapak_tarama"] = dict(an=len(ANG), bulgu=len(bul), x=xb, z=zb, kilit_dili_zmin=zd_[0])
    kontrol("kapaklar 0–%.0f° (%d açı × 3 kapak, her 5°) ↔ bütün sabit parçalar + bulaşık + öbür kapaklar (kapalı): %d çakışma · süpürülen x %.1f–%.1f · z %.1f…%.1f (K bandında kalır: fırın/dolap ve E yüzlerine girmez, "
            "+59'un arkasına YALNIZ kilit dili geçer: AZM ağzına z %.1f) · %.0f sn"
            % (KAPAK_MAX, len(ANG), len(bul), xb[0], xb[1], zb[0], zb[1], zd_[0], time.time() - t0),
            not bul and xb[0] >= KAPAK_X[0] - 0.05 and xb[1] <= KAPAK_X[1] + 0.05 and zb[0] >= Z_TAVA[0] - 0.05 and abs(zd_[0] - (Z_CER[1] - AZM_AGIZ)) < 0.05, str(sorted(bul.items())[:5]))
    # 6c · TAM TARAMA — İSTİSNA LİSTESİ YOK, BÜTÜN PARÇALAR (2. tur, denetçi ORTA-1: v6-1 istisnasız taramayı yalnız yeni + değişen 69 parçaya yapıyordu;
    #      ISTISNA kablo_kanali_dikey ↔ kose_dikmesi_3 82 016 mm³ GERÇEK çakışmayı + 25 gömülü örtüşmeyi gizliyordu → hepsi düzeltildi, ISTISNA BOŞ)
    #      (i) sabit + kapaklar (kapalı) + bulaşık kendi aralarında · (ii) her hareketli grup kendi içinde · (iii) hareketliler çevrim boyunca (her 0,1 sn) ↔ sabit + öbür gruplar
    t0 = time.time()
    HARG = ("KESICI", "ITICI_ARABA", "ITICI_KOL")
    SK = [(p, s_, s_.BoundingBox()) for p, s_ in ((p, p["wp"].val()) for p in PARCALAR if p["grup"] in SABIT_GRUP or p["ad"].startswith("REF_bulasik_"))]
    tam, ncift = {}, [0]
    def _yaz_(p, q, a, b, an):
        ncift[0] += 1
        v = a.intersect(b).Volume()
        if v > 0.01:
            k_ = tuple(sorted((p["ad"], q["ad"])))
            if v > tam.get(k_, (0.0, ""))[0]: tam[k_] = (round(v, 2), an)
    for i, (p, a, A) in enumerate(SK):
        for q, b, B_ in SK[i + 1:]:
            if KC._bb_kesisir(A, B_): _yaz_(p, q, a, b, "sabit")
    HP = [p for p in PARCALAR if p["grup"] in HARG]
    for g in HARG:
        G_ = [(p, p["wp"].val(), p["wp"].val().BoundingBox()) for p in HP if p["grup"] == g]
        for i, (p, a, A) in enumerate(G_):
            for q, b, B_ in G_[i + 1:]:
                if KC._bb_kesisir(A, B_): _yaz_(p, q, a, b, "grup içi")
    anl = [round(0.1 * k_, 2) for k_ in range(int(DONGU / 0.1) + 1)]
    for t in anl:
        hh = [(p, tasi(p["wp"].val(), grup_trs(p["grup"], t))) for p in HP]
        hh = [(p, a, a.BoundingBox()) for p, a in hh]
        for i, (p, a, A) in enumerate(hh):
            for q, b, B_ in [x for x in hh[i + 1:] if x[0]["grup"] != p["grup"]] + SK:
                if KC._bb_kesisir(A, B_): _yaz_(p, q, a, b, "t=%.1f" % t)
    tl_ = sorted(tam.items(), key=lambda kv: -kv[1][0])
    H_["tam_tarama"] = dict(parca=len(SK) + len(HP), an=len(anl), aday_cift=ncift[0], cakisma=len(tam), bulgu=[[a, b, v, an] for (a, b), (v, an) in tl_[:30]], istisna=len(ISTISNA))
    kontrol("TAM TARAMA İSTİSNASIZ (2. tur): %d parça (sabit + 3 kapak kapalı + bulaşık + %d hareketli) · hareketliler %d an (her 0,1 sn) · %d aday çift · eşik 0,01 mm³ → %d çakışma · ISTISNA listesi %d kalem · %.0f sn"
            % (len(SK) + len(HP), len(HP), len(anl), ncift[0], len(tam), len(ISTISNA), time.time() - t0), not tam and not ISTISNA, str(tl_[:8]))
    # ---- 7 · BULAŞIK v2 (ayrı modül, montajdaki yerinde) ----
    bm, (kx, ky, kz) = bulasik_parcalari()
    ONDE = ("isikli_kulp", "dokunmatik_ekran")
    bmb = cq.Compound.makeCompound([sh for a_, sh in bm if a_ not in ONDE]).BoundingBox()
    bon = max(sh.BoundingBox().zmax for a_, sh in bm if a_ in ONDE)
    bta = cq.Compound.makeCompound([sh for a_, sh in bm]).BoundingBox()
    Z = BULASIK_ZARF; tv = bbx("bulasik_tavasi")
    H_["bulasik"] = dict(x=(bmb.xmin, bmb.xmax), y=(bmb.ymin, bmb.ymax), z=(bmb.zmin, bmb.zmax), dunya_x=(bmb.xmin + X_K_HAT, bmb.xmax + X_K_HAT), kulp_onu_z=bon, tam_z=(bta.zmin, bta.zmax),
                         yer=BULASIK_YER, tava_ustu=tv.ymax)
    kontrol("bulaşık (bulasik_cad_v2, kök %s · AYAKSIZ): dünya x %.1f–%.1f · gövde altı y %.1f = tava üstü %.1f (v5: gövde 136 → +%.0f) · üst %.0f · TAMAMI z %.0f…%.0f = zarf · kulp + ekran önü z %.1f (kapak arkasına %.1f)"
            % (BULASIK_YER, bmb.xmin + X_K_HAT, bmb.xmax + X_K_HAT, bmb.ymin, tv.ymax, bmb.ymin - 136.0, bmb.ymax, bta.zmin, bta.zmax, bon, Z_TAVA[0] - bon),
            not [a_ for a_, _s in bm if a_.startswith("ayar_ayagi")] and abs(bmb.ymin - tv.ymax) < 0.01 and abs(bmb.ymin - Y_TABLA) < 0.01 and abs(bmb.ymin - 149.0) < 0.01
            and abs(bta.zmin - Z["z"][0]) < 0.01 and abs(bta.zmax - Z["z"][1]) < 0.01 and bmb.xmin >= Z["x"][0] - 0.01 and bmb.xmax <= Z["x"][1] + 0.01
            and bmb.ymin >= Z["y"][0] - 0.01 and bmb.ymax <= Z["y"][1] + 0.01 and bon < Z_CER[0])
    bag = max(sh.BoundingBox().ymax for a_, sh in bm if a_.startswith("baglanti_"))
    kontrol("bulaşık arka bağlantıları üstü y %.1f ≤ %.0f (v6: +13 · föy tahliye 165 + Y0 %.0f + r 15)" % (bag, BULASIK_BAGLANTI_UST, BULASIK_YER[1]), bag <= BULASIK_BAGLANTI_UST + 0.01)
    K_ = [(p, p["wp"].val()) for p in PARCALAR if p["grup"] not in ("REF", "URUN", "URUN_IZ", "SPREY")]
    g1 = giren(kutu_(Z["x"], Z["y"], Z["z"]), K_)
    kontrol("bulaşık zarfına (%.1f–%.1f × %.0f–%.0f × %.0f…%.0f) hiçbir K parçası girmez (kapaklar kapalı · tava üstü = zarf altı)" % (Z["x"] + Z["y"] + Z["z"]), not g1, str(g1[:5]))
    g2 = []
    for p, sh in K_:
        A = sh.BoundingBox()
        for a_, b_ in bm:
            if KC._bb_kesisir(A, b_.BoundingBox()):
                v = sh.intersect(b_).Volume()
                if v > 0.01: g2.append((p["ad"], a_, round(v, 1)))
    kontrol("bulaşık gerçek katıları (%d parça) ↔ K parçaları (kapaklar kapalı) çakışma %d" % (len(bm), len(g2)), not g2, str(g2[:5]))
    ZK = kutu_(kx, ky, kz)
    alt = [(p, p["wp"].val()) for p in PARCALAR if p["grup"] == "KAPAK_ALT"]
    def alt_hacim(aci):
        v = 0.0
        for _p, s_ in alt:
            r = kapak_ac(s_, aci)
            if KC._bb_kesisir(r.BoundingBox(), ZK.BoundingBox()): v += r.intersect(ZK).Volume()
        return v
    v_kapali = alt_hacim(0.0)
    v60 = alt_hacim(60.0)
    amin = next((a for a in range(60, int(KAPAK_MAX) + 1) if alt_hacim(float(a)) <= 0.01), None)
    SABK = [(p, s_) for p, s_ in K_ if p["grup"] != "KAPAK_ALT"] + [(p, kapak_ac(s_, KAPAK_MAX)) for p, s_ in alt]
    g3 = giren(ZK, SABK)
    ka_ = cq.Compound.makeCompound([kapak_ac(s_, KAPAK_MAX) for _p, s_ in alt]).BoundingBox()
    L_bm = BM.KAPI["y1"] - BM.KAPI["y0"]
    z_day = Z_ON - TAVA_T - DAYAMA["t"]                                                 # 2. tur: EPDM dayama lastiğinin yüzü (74,5) — bulaşık kapağının üst ön kenarı buna değer
    bm_aci = math.degrees(math.asin(min(1.0, (z_day - BULASIK_YER[2]) / L_bm)))
    y_day = BULASIK_YER[1] + BM.KAPI["y0"] + L_bm * math.cos(math.radians(bm_aci))   # temas çizgisinin y'si (menteşe y 384 + 455·cos)
    bmk_ = [sh for a_, sh in bm if a_ == "kapak"][0].BoundingBox()
    H_["bulasik_kapak_zarfi"] = dict(x=kx, y=ky, z=kz, alt_kapak_min_aci=amin, alt_kapali_hacim=round(v_kapali, 0), pay_90=round(kx[0] - ka_.xmax, 1), bulasik_kapak_kilitte_aci=round(bm_aci, 1),
                                     dayama_temas_y=round(y_day, 1), dayama=DAYAMA)
    kontrol("bulaşık kapak açık zarfı (x %.1f–%.1f · y %.0f–%.0f · z %.0f…%.0f) ↔ K sabitleri + ORTA/ÜST (kapalı) + ALT kapak %.0f° AÇIK: %d parça · ALT kapakla pay %.1f mm"
            % (kx + ky + kz + (KAPAK_MAX, len(g3), kx[0] - ka_.xmax)), not g3, str(g3[:5]))
    kontrol("KİLİT (mekanik): ALT kapak kapalıyken zarfta (%.0f mm³) → bulaşık kapağı ≈ %.1f° açılıp ALT kapağın EPDM dayama lastiğine (x %.1f–%.1f · y %.0f–%.0f) y %.1f'de dayanır — 1,5 sac yüklenmez "
            "(kapak x %.1f–%.1f lastiğin içinde) · ALT kapak ≥ %s° açıkken bulaşık kapağı serbest (menteşe en çok %.0f°)"
            % (v_kapali, bm_aci, DAYAMA["x"][0], DAYAMA["x"][1], DAYAMA["y"][0], DAYAMA["y"][1], y_day, bmk_.xmin, bmk_.xmax, amin, KAPAK_MAX),
            v_kapali > 0 and v60 > 0 and amin is not None and amin <= KAPAK_MAX - 5.0 and DAYAMA["y"][0] + 5.0 <= y_day <= DAYAMA["y"][1] - 5.0
            and DAYAMA["x"][0] <= bmk_.xmin and bmk_.xmax <= DAYAMA["x"][1])
    g4 = giren(kutu_(Z["x"], Z["y"], BULASIK_ARKA_PAY), K_)
    kontrol("MEIKO arka payı z %.0f…%.0f BOŞ: hiçbir K parçası girmez (makinenin kendi bağlantıları y ≤ %.0f)" % (BULASIK_ARKA_PAY + (BULASIK_BAGLANTI_UST,)), not g4, str(g4))
    ab = (Z["x"], Z["y"], (bbx("arka_sac").zmax, BULASIK_ARKA_PAY[0]))
    g5 = giren(kutu_(*ab), K_)
    H_["bulasik_arka_bos"] = dict(x=ab[0], y=ab[1], z=ab[2], derinlik=ab[2][1] - ab[2][0])
    kontrol("bulaşığın arkası BOŞ: x %.1f–%.1f · y %.0f–%.0f · z %.1f…%.0f (%.1f mm derin) → K parçası yok" % (ab[0] + ab[1] + ab[2] + (ab[2][1] - ab[2][0],)), not g5, str(g5[:5]))
    ustu = [(p["wp"].val().BoundingBox().ymin, p["ad"]) for p in PARCALAR if p["grup"] not in ("REF", "URUN", "URUN_IZ", "SPREY")
            and KC._bb_kesisir(p["wp"].val().BoundingBox(), kutu_(Z["x"], (Z["y"][1], H), Z["z"]).BoundingBox())]
    H_["bulasik_ust_bosluk"] = min(ustu)[0] - bmb.ymax
    kontrol("bulaşığın üstü %.0f → ilk K parçası %s %.0f: boşluk %.0f mm (v5: 66 → makine +13)" % (bmb.ymax, min(ustu)[1], min(ustu)[0], H_["bulasik_ust_bosluk"]), H_["bulasik_ust_bosluk"] > 0.0)
    sol = bmb.xmin - bbx("onyuz_cerceve_dikme_sol").xmax; sol_ark = bmb.xmin - bbx("sol_sac_urun_girisi").xmax
    H_["bulasik_sol"] = dict(on=sol, arka=sol_ark)
    print("     bulaşığın solu: sol ön çerçeve dikmesinden %.1f · sol sacdan %.1f → BOŞ (v6: öndeki kesik köşe dikmesi yok)" % (sol, sol_ark))
    # ---- 8 · HAVADA PARÇA (denetim_temas_v1 · hareketliler t = 0 · kapaklar kapalı · bulaşık dahil) ----
    HV = [(p["ad"], p["wp"]) for p in PARCALAR if p["grup"] not in ("URUN", "URUN_IZ", "SPREY") and (p["grup"] != "REF" or p["ad"].startswith("REF_bulasik_"))]
    hv = DT.havada(HV)
    nh = DT.yaz(hv, baslik="HAVADA PARCA (K v6 + bulasik v2 · hareketliler t=0 · kapaklar kapali)")
    BEYAZ = ()                                                                          # beyaz liste: BOŞ (DGRF-C burçları kayar geçme — idealleştirilmiş temas, modelde gerçek parça)
    H_["havada"] = dict(once=dict(bilesen=17, parca=74, not_="kesme v5 + bulaşık v1 (K'deki yerinde, ayaklı) · aynı denetim"), sonra=dict(parca=hv["parca"], bagli=hv["bagli"],
                        bilesen=nh, uye=[d_["uye"] for d_ in hv["bilesen"]]), beyaz_liste=list(BEYAZ))
    kontrol("HAVADA PARÇA (denetim_temas_v1, tol 0,05): %d parça · kök (ayak) %d · zemine bağlı %d · HAVADA %d bileşen · v5: 17 bileşen / 74 parça · beyaz liste BOŞ"
            % (hv["parca"], hv["kok"], hv["bagli"], nh), nh == 0 and hv["bagli"] == hv["parca"])
    HVa = [(p["ad"], (kapak_ac(p["wp"].val(), KAPAK_MAX) if p["grup"] in KAPAK_GRUP else p["wp"])) for p in PARCALAR
           if p["grup"] not in ("URUN", "URUN_IZ", "SPREY") and (p["grup"] != "REF" or p["ad"].startswith("REF_bulasik_"))]
    hva = DT.havada(HVa)
    uy_ = set(u for d_ in hva["bilesen"] for u in d_["uye"]); kap_ = set(p["ad"] for p in PARCALAR if p["grup"] in KAPAK_GRUP)
    H_["havada_kapak_acik"] = dict(bilesen=len(hva["bilesen"]), parca=len(uy_), uye=[d_["uye"] for d_ in hva["bilesen"]])
    kontrol("2. tur · kapaklar %.0f° AÇIK: havada kalan YALNIZ %d kapak grubu (%d parça: tava + menteşe kanadı + karşılık + dil + dayama) — menteşe mekanizması sanal pivot, modelde YOK "
            "(EMKA pivot yeri üreticiden teyit) · kapağa dayanan başka parça YOK" % (KAPAK_MAX, len(hva["bilesen"]), len(uy_)), uy_ <= kap_ and len(hva["bilesen"]) == len(KAPAK_GRUP), str(sorted(uy_ - kap_)))
    UYARI.append("kapaklar AÇIK konumda bağlılık: menteşe kanadı ↔ gövde arası sanal pivot (EMKA 1046-U5 iç mekanizması modelde yok) → açıkken %d kapak grubu havada görünür; kapalı konumda bağlı (havada 0)" % len(hva["bilesen"]))
    # ---- 9 · hesaplar ----
    L_k = (W - SAC - UC_T) - (SAC + UC_T)
    I_k = (40.0 ** 4 - 36.0 ** 4) / 12.0
    P_k = H_["silindir_N"] / 2.0
    d_k = P_k * L_k ** 3 / (48.0 * E_304 * I_k)
    s_k = P_k * L_k / 4.0 / (I_k / 20.0)
    yb_k = 2.0 * P_k / 2.0 / (6 * 6.0 * SAC)
    H_["kopru"] = dict(aciklik=L_k, P_kiris=P_k, sehim=d_k, gerilme=s_k, uc_plaka_yatak=yb_k)
    kontrol("köprü (v6): 2 × 40×40×2 · açıklık %.0f · tepki %.0f N (DGRF-C-63, 6 bar) → kiriş başına %.0f N: sehim %.2f mm (basit mesnet, en kötü; uçlar kaynaklı) · gerilme %.0f MPa (304 akma 205, emniyet %.1f) · uç plakası → yan sac 6 × M6 yatak basıncı %.1f MPa"
            % (L_k, H_["silindir_N"], P_k, d_k, s_k, 205.0 / s_k, yb_k), d_k < 0.5 and s_k < 205.0 / 3.0 and yb_k < 100.0)
    kz, ky, kt = TABLA_KIRIS
    I_t = (kz * ky ** 3 - (kz - 2 * kt) * (ky - 2 * kt) ** 3) / 12.0
    L_t = W - 2 * SAC
    P_t = BULASIK_KG * 9.81 / 4.0
    yuk = [(BULASIK_YER[0] - X_K_HAT + 30.0 - SAC, P_t), (BULASIK_YER[0] - X_K_HAT + BM.W - 30.0 - SAC, P_t)]
    def sehim_t(x):
        s_ = 0.0
        for a_, P_ in yuk:
            b_ = L_t - a_
            s_ += P_ * b_ * x * (L_t ** 2 - b_ ** 2 - x ** 2) / (6 * L_t * E_304 * I_t) if x <= a_ else P_ * a_ * (L_t - x) * (L_t ** 2 - a_ ** 2 - (L_t - x) ** 2) / (6 * L_t * E_304 * I_t)
        return s_
    d_t = max(sehim_t(L_t * i / 200.0) for i in range(201))
    H_["tabla"] = dict(kiris=TABLA_KIRIS, I=I_t, P_kose=P_t, sehim=d_t, kg=BULASIK_KG)
    kontrol("bulaşık tablası: 2 × 40×20×2 kiriş (I %.0f mm⁴, açıklık %.0f, yan saclara kaynaklı) · makine %.0f kg [VARSAYIM] köşe başına %.0f N (köşeler kirişin üstünde) → sehim %.2f mm (basit mesnet, taban sacı desteği yok sayıldı)"
            % (I_t, L_t, BULASIK_KG, P_t, d_t), d_t < 1.0)
    mg = {a: H_["kapak"][a]["kg"] * 9.81 for _g, a, _y0, _y1 in KAPAKLAR}
    mom = {a: mg[a] * (KAPAK_X[1] - KAPAK_X[0]) / 2.0 / (MENTESE_Y[a][1] - MENTESE_Y[a][0]) for a in mg}
    H_["mentese"] = dict(dikey_N=dict((a, round(mg[a] / 2.0, 1)) for a in mg), yatay_N=dict((a, round(mom[a], 1)) for a in mom))
    UYARI.append("menteşe yükü: kapak başına 2 × EMKA 1046-U5 · dikey %s N/menteşe · 90° açıkken yatay kuvvet çifti %s N (kapak ağırlık merkezi 298 mm dışarıda) — EMKA yük değeri föyde yok, üreticiden teyit"
                 % ("/".join("%.0f" % (mg[a] / 2.0) for a in mg), "/".join("%.0f" % mom[a] for a in mom)))
    A_b = 2 * len(_yarik_x()) * YARIK["en"] * YARIK["boy"] / 1e6
    hA = (sum(YARIK["bant"]["alt"][2]) + sum(YARIK["bant"]["alt"][3]) - sum(YARIK["bant"]["alt"][0]) - sum(YARIK["bant"]["alt"][1])) / 4000.0
    hU = (sum(YARIK["bant"]["ust"][2]) + sum(YARIK["bant"]["ust"][3]) - sum(YARIK["bant"]["ust"][0]) - sum(YARIK["bant"]["ust"][1])) / 4000.0
    dTA, dTU = isi_dT(Q_BULASIK_W, A_b, hA), isi_dT(Q_UST_W, A_b, hU)
    A_alt = (KAPAK_X[1] - KAPAK_X[0]) * (KAPAKLAR[0][3] - KAPAKLAR[0][2]) / 1e6; A_ust = (KAPAK_X[1] - KAPAK_X[0]) * (KAPAKLAR[2][3] - KAPAKLAR[2][2]) / 1e6
    dTA0, dTU0 = Q_BULASIK_W / (U_KAPALI * A_alt), Q_UST_W / (U_KAPALI * A_ust)
    H_["isi"] = dict(varsayilan="YARIKSIZ (SPEC §1)", yarik_acik=YARIK_ACIK, kapali=dict(U=U_KAPALI, A_alt=A_alt, A_ust=A_ust, dT_alt=dTA0, dT_ust=dTU0),
                     secenek_yarik=dict(yarik_alan_bant_cm2=A_b * 1e4, alt=dict(Q=Q_BULASIK_W, h=hA, dT=dTA), ust=dict(Q=Q_UST_W, h=hU, dT=dTU), alt_15K_cm2=A_b * 1e4 * (dTA / 15.0) ** 1.5))
    UYARI.append("ISI — KARAR GEREKLİ, montaja almadan önce (VARSAYIM, ölç): varsayılan model SPEC'e uygun YARIKSIZ → kapalı bölme ısıyı yalnız ön kapaktan atar: ALT (bulaşık Q %.0f W) ΔT ≈ %.0f K · "
                 "ÜST (Q %.0f W) ΔT ≈ %.0f K (U %.0f W/m²K iyimser, A %.2f / %.2f m²) → KABUL EDİLEMEZ. Seçenekler: (a) YARIK_ACIK = True: bant başına %.0f cm² → ALT ΔT ≈ %.0f K (baca %.2f m) · "
                 "ÜST ≈ %.0f K; (b) ALT için bant başına ≈ %.0f cm² (ΔT ≤ 15 K); (c) 24 V fan (B dolabındaki ebm-papst 4414 FL) + gizli emiş/atış; (d) MEIKO'ya kapalı niş havalandırma şartı sorulmalı · "
                 "fırın ağzından K'ye sızan sıcak hava BİLİNMİYOR" % (Q_BULASIK_W, dTA0, Q_UST_W, dTU0, U_KAPALI, A_alt, A_ust, A_b * 1e4, dTA, hA, dTU, A_b * 1e4 * (dTA / 15.0) ** 1.5))
    # 2. tur (denetçi K-7 + K-12): ölçülen açık konular
    hk_ = _sek("hava_hortumu_kaldirma"); mg_ = _sek("MGPM20-60_govde")
    hm_ = [(t, _mesafe(hk_, tasi(mg_, grup_trs("ITICI_ARABA", t)))) for t in [k_ * 0.1 for k_ in range(int(DONGU / 0.1) + 1)]]
    H_["kaldirma_hortumu_MGPM"] = dict(t0=hm_[0][1], min=min(v for _t, v in hm_), max=max(v for _t, v in hm_))
    UYARI.append("kaldırma hortumu (AÇIK): valf ucu bağlı, MGPM ucu BOŞTA — t = 0'da %.0f mm, çevrim boyunca %.0f–%.0f mm (itici arabası 365 strok) → spiral hortum (ör. SMC TCU0425 sarmal PU) "
                 "ya da mini enerji zinciri (igus E2 micro) modellenmeli; 'havada 0' yalnız valf ucunun bağlı olmasından" % (H_["kaldirma_hortumu_MGPM"]["t0"], H_["kaldirma_hortumu_MGPM"]["min"], H_["kaldirma_hortumu_MGPM"]["max"]))
    pp_ = bbx("pano_plakasi")
    H_["pano_erisim"] = dict(derinlik=Z_ON - pp_.zmax, y=(pp_.ymin, pp_.ymax), v5_derinlik=0.0 - pp_.zmax)
    UYARI.append("pano erişimi (AÇIK): pano plakasının ön yüzü ön düzlemden %.0f mm derinde (v5: %.0f; +79 ile uzadı), y %.0f–%.0f (1,47–1,86 m) → önden kablolama / servis zor: "
                 "menteşeli / öne çekilir pano plakası ya da servisin arkadan yapılması karar ister (tank dolumu 619 mm derinde, aynı konu)" % (Z_ON - pp_.zmax, -pp_.zmax, pp_.ymin, pp_.ymax))
    # ---- 10 · açıklıklar + temizlik ----
    ac = []
    for a, (y0, y1, z0, z1), x0 in (("sol_sac_urun_girisi", URUN_GIRISI, 0.0), ("sag_sac_E_penceresi", E_PENCERE, W - SAC)):
        ac.append(_sek(a).intersect(kutu_((x0 - 0.1, x0 + SAC + 0.1), (y0 + 0.01, y1 - 0.01), (z0 + 0.01, z1 - 0.01))).Volume())
    kontrol("ürün açıklıkları yan saclarda AYNI ve BOŞ: fırın → K girişi y %.0f–%.0f z %.0f…%.0f · K → E penceresi y %.0f–%.0f z %.0f…%.0f · K ön yüzünde açıklık YOK (ürün ön yüzden geçmez, K'de robot noktası yok)"
            % (URUN_GIRISI + E_PENCERE), all(v < 0.01 for v in ac), str(ac))
    hb = [p["ad"] for p in PARCALAR if p["ad"].startswith("hava_besleme")]
    it = _sek("istasyon_tabani_3").Volume()
    it_b = (W - 2 * SAC) * 3.0 * (D - SAC + Z_KABUK_ON) - sum((x1 - x0) * 3.0 * (Z_KABUK_ON - Z_CER[0]) for x0, x1 in (CER_X_SOL, CER_X_SAG)) - 2 * 30.0 * 3.0 * 30.0
    kontrol("hava_besleme_K YOK (MS4 zaten üstten ANA_K48 ile beslenir) · istasyon tabanında delik YOK (hacim %.0f = düz sac − 2 ön + 2 arka dikme çentiği %.0f mm³)" % (it, it_b), not hb and abs(it - it_b) < 1.0)
    UYARI.append("montaj (hat_montaj_v62 → yeni sürüm): K_BIRIM'e 'onyuz_' + 'bulasik_tabla' + 'bulasik_tavasi' + 'bulasik_gecis' öneki · ÖN YÜZ denetimi z ≤ 79,5 · SOZLESME bulaşık y 126 → %.0f + KS.Z_ON = FT.ZS · "
                 "_IZIN K girdileri sil · _KIC y alt sınırı 1 mm pay gereksiz (ayak yok) · bulaşık kapak zarfı ↔ K yazdırması ALT kapak AÇIK (KS.kapak_ac) ile" % BULASIK_YER[1])
    for u in UYARI:
        print("  UYARI: " + u)
    H_["uyari"] = list(UYARI)


# ---------------------------------------------------------------- ÇAKIŞMA TARAMASI ----------------------------------------------------------------
ISTISNA = []      # v6 2. tur: BOŞ — bütün yüz temasları 0 hacim; gömülü geçmeler delik / yuva olarak modellendi (denetim_v6 · TAM TARAMA İSTİSNASIZ 0).
                  # v5 / v6-1'deki alt-dizgi listesi kablo_kanali_dikey ↔ kose_dikmesi_3 (82 016 mm³) gerçek çakışmasını gizliyordu (denetçi ORTA-1).


def _ist(a, b):
    for p, q in ISTISNA:
        if (p in a and q in b) or (p in b and q in a):
            return True
    return False


def cakisma(esik=1.0, adim=0.1):
    t0 = time.time()
    sab = [(p, p["wp"].val()) for p in PARCALAR if p["grup"] in SABIT_GRUP]              # v6: kapaklar KAPALI (sabit gibi)
    sab = [(p, v, v.BoundingBox()) for p, v in sab]
    bul = {}
    for i, (p, a, A) in enumerate(sab):
        for q, b, B_ in sab[i + 1:]:
            if not KC._bb_kesisir(A, B_) or _ist(p["ad"], q["ad"]):
                continue
            v = a.intersect(b).Volume()
            if v > esik: bul[(p["ad"], q["ad"])] = (v, "sabit")
    HAR = ("KESICI", "ITICI_ARABA", "ITICI_KOL")
    anlar = [round(adim * i, 2) for i in range(int(DONGU / adim) + 1)]
    for t in anlar:
        hh = []
        for p in PARCALAR:
            if p["grup"] in HAR:
                sh = tasi(p["wp"].val(), grup_trs(p["grup"], t)); hh.append((p, sh, sh.BoundingBox()))
        for i, (p, a, A) in enumerate(hh):
            for q, b, B_ in hh[i + 1:] + sab:
                if q["grup"] == p["grup"] or not KC._bb_kesisir(A, B_) or _ist(p["ad"], q["ad"]):
                    continue
                v = a.intersect(b).Volume()
                if v > esik and (p["ad"], q["ad"]) not in bul: bul[(p["ad"], q["ad"])] = (v, "t=%.1f" % t)
    print("CAKISMA (K makine): %d parca · %d an · %d cakisma · %.0f sn" % (len(PARCALAR), len(anlar), len(bul), time.time() - t0))
    for (a, b), (v, an) in sorted(bul.items(), key=lambda kv: -kv[1][0])[:60]:
        print("    %10.1f mm3  %-7s %s <-> %s" % (v, an, a, b))
    return bul


URUN_ISTISNA = ("bant_PU", "kayma_tablasi", "olu_plaka")     # ürün bunların üstünde kayar (yüz teması, hacim 0)


def _bbt(bb, M=None, d=(0.0, 0.0, 0.0)):
    """sınır kutusunu 4×4 dönüşümle (köşeleri taşıyarak) + ötelemeyle taşır → (x0,x1,y0,y1,z0,z1)"""
    P = [(x, y, z) for x in (bb.xmin, bb.xmax) for y in (bb.ymin, bb.ymax) for z in (bb.zmin, bb.zmax)]
    if M is not None:
        P = [tuple(M[i][0] * p[0] + M[i][1] * p[1] + M[i][2] * p[2] + M[i][3] for i in range(3)) for p in P]
    return (min(p[0] for p in P) + d[0], max(p[0] for p in P) + d[0], min(p[1] for p in P) + d[1], max(p[1] for p in P) + d[1],
            min(p[2] for p in P) + d[2], max(p[2] for p in P) + d[2])


def _kes(A, B, pay=0.05):
    return A[0] < B[1] - pay and B[0] < A[1] - pay and A[2] < B[3] - pay and B[2] < A[3] - pay and A[4] < B[5] - pay and B[4] < A[5] - pay


_E_ON = []


def _e_parcalari():
    """kutu modülünün parçaları (K yerelinde +600) · sabitler bir kez taşınır"""
    if not _E_ON:
        KC.modul()
        for p in KC.PARCALAR:
            if p["grup"] in ("PIZZA", "K_ITICI", "SABIT_REF", "CATAL") or p["ad"].startswith(("robot_", "REF_")):
                continue
            sh = p["wp"].val(); bb = sh.BoundingBox()
            if p["grup"] == "SABIT":
                sh = tasi(sh, (W, 0.0, 0.0)); _E_ON.append((p, sh, _bbt(sh.BoundingBox()), None))
            else:
                _E_ON.append((p, sh, None, bb))
    return _E_ON


def _e_anda(t, bolge):
    """t anında, BÖLGE ile kesişebilecek E parçaları (dünyada) — önce sınır kutusu taşınır, gerekirse katı"""
    L = []; We = None
    for p, sh, bb_s, bb0 in _e_parcalari():
        if bb_s is not None:
            if _kes(bb_s, bolge): L.append((p, sh, bb_s))
            continue
        g = p["grup"]
        if g.startswith("B_"):
            We = We or KC.blank_dunya(t); M = We[g]
        else:
            M = KC.grup_matrisi(g, t)
        if not _kes(_bbt(bb0, M, (W, 0.0, 0.0)), bolge):
            continue
        s2 = tasi(KC.uygula(sh, M), (W, 0.0, 0.0)); L.append((p, s2, _bbt(s2.BoundingBox())))
    return L


def urun_cakisma(esik=1.0, adim=0.05):
    """ürün fırın bandından kutuya kadar: ürün × K (sabit + hareketli) × E (o anki konumunda, katlanan karton dahil)"""
    t0 = time.time(); bul = {}
    anlar = [round(0.35 + adim * i, 2) for i in range(int((KC.Z_PIZZA[1] - 0.35) / adim) + 1)]
    uz = [p for p in PARCALAR if p["grup"] == "URUN"]
    sab = [(p, p["wp"].val()) for p in PARCALAR if p["grup"] in SABIT_GRUP]              # v6: kapaklar KAPALI (sabit gibi)
    sab = [(p, v, _bbt(v.BoundingBox())) for p, v in sab]
    for t in anlar:
        U_ = [(p, tasi(p["wp"].val(), urun_trs(t))) for p in uz]
        bolge = _bbt(U_[0][1].BoundingBox())
        for _p, a in U_[1:]:
            b_ = _bbt(a.BoundingBox()); bolge = (min(bolge[0], b_[0]), max(bolge[1], b_[1]), min(bolge[2], b_[2]), max(bolge[3], b_[3]), min(bolge[4], b_[4]), max(bolge[5], b_[5]))
        diger = [x for x in sab if _kes(x[2], bolge)]
        for p in PARCALAR:
            if p["grup"] in ("KESICI", "ITICI_ARABA", "ITICI_KOL"):
                sh = tasi(p["wp"].val(), grup_trs(p["grup"], t)); bb = _bbt(sh.BoundingBox())
                if _kes(bb, bolge): diger.append((p, sh, bb))
        diger += [(dict(p, ad="E:" + p["ad"]), sh, bb) for p, sh, bb in _e_anda(t, bolge)] if bolge[1] > W - 5.0 else []
        for p, a in U_:
            A = _bbt(a.BoundingBox())
            for q, b, B_ in diger:
                if q["ad"].startswith(URUN_ISTISNA) or (q["ad"].startswith("bicak") and Z_KES[0] <= t <= Z_KALK[0] + 0.3):   # kesim: bıçak üründe (bilerek)
                    continue
                if not _kes(A, B_):
                    continue
                v = a.intersect(b).Volume()
                if v > esik: bul[(p["ad"], q["ad"], t)] = v
    print("CAKISMA (urun yolu firin -> E): %d an · %d cakisma · %.0f sn" % (len(anlar), len(bul), time.time() - t0))
    for (a, b, t), v in sorted(bul.items(), key=lambda kv: -kv[1])[:40]:
        print("    %10.1f mm3  t=%.2f  %s <-> %s" % (v, t, a, b))
    return bul


def e_itici_cakisma(esik=1.0, adim=0.05):
    """itici E'ye girerken: itici × E'nin bütün parçaları (o anki konumlarında) + katlanan kutu kartonu"""
    t0 = time.time(); bul = {}
    anlar = [round(8.3 + adim * i, 2) for i in range(int((11.4 - 8.3) / adim) + 1)]
    it = [p for p in PARCALAR if p["grup"] in ("ITICI_KOL", "ITICI_ARABA")]
    for t in anlar:
        I_ = [(p, tasi(p["wp"].val(), grup_trs(p["grup"], t))) for p in it]
        I_ = [(p, a, _bbt(a.BoundingBox())) for p, a in I_]
        I_ = [x for x in I_ if x[2][1] > W - 5.0]                   # yalnız E'ye uzanan itici parçaları
        if not I_: continue
        bolge = (min(x[2][0] for x in I_), max(x[2][1] for x in I_), min(x[2][2] for x in I_), max(x[2][3] for x in I_), min(x[2][4] for x in I_), max(x[2][5] for x in I_))
        for q, b, B_ in _e_anda(t, bolge):
            for p, a, A in I_:
                if not _kes(A, B_): continue
                v = a.intersect(b).Volume()
                if v > esik: bul[(p["ad"], "E:" + q["ad"], t)] = v
    print("CAKISMA (itici x E): %d an · %d cakisma · %.0f sn" % (len(anlar), len(bul), time.time() - t0))
    for (a, b, t), v in sorted(bul.items(), key=lambda kv: -kv[1])[:40]:
        print("    %10.1f mm3  t=%.2f  %s <-> %s" % (v, t, a, b))
    return bul


# ---------------------------------------------------------------- GLB (gruplar + animasyon) ----------------------------------------------------------------
def _ag(wp, kaba=False):
    return KC._ag(wp, kaba)


def glb_yaz(yol, adim=1.0 / 15.0, pide=True):
    GRUPLAR = ["SABIT", "REF", "KESICI", "ITICI_ARABA", "ITICI_KOL", "URUN", "URUN_IZ", "SPREY"] + list(KAPAK_GRUP)      # v6: 3 kapak düğümü (kapalı; açma KS.kapak_ac)
    assert set(p["grup"] for p in PARCALAR) <= set(GRUPLAR), sorted(set(p["grup"] for p in PARCALAR) - set(GRUPLAR))
    mesh_g = {g: {} for g in GRUPLAR}
    for p in PARCALAR:
        kaba = p["ad"].startswith(("surucu_", "guc_", "itici_motoru"))
        mesh_g[p["grup"]].setdefault(p["mal"], Mesh()).ekle(_ag(p["wp"], kaba))
    blob, views, accs, meshes, mats, mi, nodes = [], [], [], [], [], {}, []
    off = [0]
    def gomu(bt, hedef=None):
        while off[0] % 4: blob.append(b"\x00"); off[0] += 1
        v = {"buffer": 0, "byteOffset": off[0], "byteLength": len(bt)}
        if hedef: v["target"] = hedef
        views.append(v); blob.append(bt); off[0] += len(bt); return len(views) - 1
    def mat(k):
        if k not in mi:
            d = MALZEME[k]; m_ = {"name": k, "pbrMetallicRoughness": {"baseColorFactor": list(d["renk"]), "metallicFactor": d["met"], "roughnessFactor": d["ruf"]}, "doubleSided": True}
            if d.get("saydam") or d["renk"][3] < 1.0: m_["alphaMode"] = "BLEND"
            mi[k] = len(mats); mats.append(m_)
        return mi[k]
    uc = 0
    for g in GRUPLAR:
        prims = []
        for k, m in sorted(mesh_g[g].items()):
            vp = gomu(struct.pack("<%df" % (3 * len(m.P)), *[c for q in m.P for c in q]), 34962)
            vn = gomu(struct.pack("<%df" % (3 * len(m.N)), *[c for q in m.N for c in q]), 34962)
            vi = gomu(struct.pack("<%dI" % len(m.I), *m.I), 34963)
            accs.append({"bufferView": vp, "componentType": 5126, "count": len(m.P), "type": "VEC3", "min": [min(q[i] for q in m.P) for i in range(3)], "max": [max(q[i] for q in m.P) for i in range(3)]})
            accs.append({"bufferView": vn, "componentType": 5126, "count": len(m.N), "type": "VEC3"})
            accs.append({"bufferView": vi, "componentType": 5125, "count": len(m.I), "type": "SCALAR"})
            prims.append({"attributes": {"POSITION": len(accs) - 3, "NORMAL": len(accs) - 2}, "indices": len(accs) - 1, "material": mat(k)}); uc += len(m.I) // 3
        n = {"name": g}
        if prims:
            meshes.append({"name": g, "primitives": prims}); n["mesh"] = len(meshes) - 1
        nodes.append(n)
    ix = {g: i for i, g in enumerate(GRUPLAR)}
    N = int(round(DONGU / adim)) + 1; TT = [min(DONGU, i * adim) for i in range(N)]; sm, ch = [], []
    def kanal(g, yol_, vals):
        ti = gomu(struct.pack("<%df" % len(TT), *TT)); accs.append({"bufferView": ti, "componentType": 5126, "count": len(TT), "type": "SCALAR", "min": [0.0], "max": [DONGU]})
        vo = gomu(struct.pack("<%df" % (3 * len(vals)), *[c for v in vals for c in v])); accs.append({"bufferView": vo, "componentType": 5126, "count": len(vals), "type": "VEC3"})
        sm.append({"input": len(accs) - 2, "output": len(accs) - 1, "interpolation": "LINEAR"}); ch.append({"sampler": len(sm) - 1, "target": {"node": ix[g], "path": yol_}})
    for g in ("KESICI", "ITICI_ARABA", "ITICI_KOL", "URUN", "URUN_IZ"):
        kanal(g, "translation", [tuple(c * MM for c in grup_trs(g, t)) for t in TT])
    kanal("URUN", "scale", [(max(1e-4, urun_gorunur(t)),) * 3 for t in TT])
    kanal("URUN_IZ", "scale", [(max(1e-4, kesik_olcek(t)),) * 3 for t in TT])
    kanal("SPREY", "scale", [(max(1e-4, sprey_gorunur(t, pide)),) * 3 for t in TT])
    while off[0] % 4: blob.append(b"\x00"); off[0] += 1
    bb = b"".join(blob)
    gl = {"asset": {"version": "2.0", "generator": "AUTOKITCH kesme_cad_v6"}, "scene": 0, "scenes": [{"nodes": list(range(len(nodes)))}], "nodes": nodes, "meshes": meshes,
          "materials": mats, "accessors": accs, "bufferViews": views, "buffers": [{"byteLength": len(bb)}],
          "animations": [{"name": "kesme_sprey_dongusu", "samplers": sm, "channels": ch}]}
    js = json.dumps(gl, separators=(",", ":")).encode("utf-8")
    while len(js) % 4: js += b" "
    with open(yol, "wb") as f:
        f.write(struct.pack("<4sII", b"glTF", 2, 12 + 8 + len(js) + 8 + len(bb))); f.write(struct.pack("<I4s", len(js), b"JSON")); f.write(js)
        f.write(struct.pack("<I4s", len(bb), b"BIN\x00")); f.write(bb)
    print("GLB: %s · %d KB · %d üçgen · %d kanal · %d kare" % (os.path.basename(yol), (len(bb) + len(js)) // 1024, uc, len(ch), N))


# ---------------------------------------------------------------- BOM ----------------------------------------------------------------
def bom_yaz(klasor):
    os.makedirs(klasor, exist_ok=True)
    satir = []
    for p in PARCALAR:
        if p["grup"] in ("URUN", "URUN_IZ", "REF", "SPREY"):
            continue
        if p["bom"]:
            ad, adet, tanim, not_ = p["bom"]
            tur = "SATIN ALMA" if any(s in ad for s in ("Festo", "SMC", "igus", "Interroll", "PulsaJet", "UniJet", "Siemens", "Mean Well", "AutomationDirect", "Omron",
                                                         "Elesa", "Pilz", "Schmersal", "Phoenix", "DIN ray", "Kablo kanalı", "Kelebek", "PU bant", "Isıtmalı", "ısıtıcı", "Sıcaklık",
                                                         "Seviye", "regülatör", "Polikarbonat", "PWM", "Acil", "Silindir sensörü", "koli", "kolisi", "hortum", "Avara", "tank", "EMKA", "Southco", "Ara burç", "Lapp", "Geçiş lastiği", "Dayama lastiği")) else "ÜRETİM"
            satir.append((p["ad"], ad, adet, tanim, not_, tur))
        else:
            b = p["wp"].val().BoundingBox()
            satir.append((p["ad"], p["ad"].replace("_", " "), 0, "", "aynı kalemin eşi ya da üretim parçası · zarf %.0f × %.0f × %.0f" % (b.xlen, b.ylen, b.zlen), "ALT"))
    with io.open(os.path.join(klasor, "BOM.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";"); w.writerow(["parça (model adı)", "kalem", "adet", "tanım / ürün", "not / kaynak", "tür"])
        for r in satir: w.writerow(r)
    top, bil = {}, {}
    for _p, ad, adet, tanim, not_, tur in satir:
        if tur == "ALT": continue
        top[ad] = top.get(ad, 0) + int(adet); bil.setdefault(ad, (tanim, not_, tur))
    with io.open(os.path.join(klasor, "BOM_OZET.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";"); w.writerow(["tür", "kalem", "toplam adet", "tanım / ürün", "not / kaynak"])
        for k in sorted(top, key=lambda a: (0 if bil[a][2] == "SATIN ALMA" else 1, a)):
            w.writerow([bil[k][2], k, top[k], bil[k][0], bil[k][1]])
    print("BOM: %d satir · %d kalem (%d satin alma)" % (len(satir), len(top), sum(1 for k in top if bil[k][2] == "SATIN ALMA")))


def e7_ileri():
    """v6 2. tur (denetçi K-13): ürün yolu + itici × E taramalarını E'nin montaj v63 sürümü kutu_cad_v7 ile çalıştırır (K'nin kendi geometrisi kutu_cad_v6'ya bağlı kalır)"""
    global KC
    try:
        import kutu_cad_v7 as K7
    except Exception as e_:
        print("E v7 yuklenemedi: %s" % e_); return None, None
    esk = KC; KC = K7; _E_ON[:] = []
    try:
        print("E v7 ILERI UYUM (kutu_cad_v7):"); a = urun_cakisma(); b = e_itici_cakisma()
    finally:
        KC = esk; _E_ON[:] = []
    return a, b


def json_yaz(yol, H_, cak):
    with io.open(yol, "w", encoding="utf-8") as f:
        json.dump(dict(surum="kesme_cad_v6 · %s" % time.strftime("%d.%m.%Y %H:%M"),
                       parcalar=[dict(ad=p["ad"], grup=p["grup"], mal=p["mal"], bom=list(p["bom"]) if p["bom"] else None) for p in PARCALAR],
                       denetim=[dict(ad=a, sonuc="GEÇTİ" if s else "KALDI", deger=v) for a, s, v in DEN], hesap=H_, cakisma=cak), f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    t0 = time.time(); arg = sys.argv[1:]
    modul()
    print("K KESME + SPREY v6 (on duzlem +79: 3 tava kapak · on cerceve · kopru uc plakalari · bulasik ayaksiz tablada · havada 0): %d parca · %.0f sn" % (len(PARCALAR), time.time() - t0)); sys.stdout.flush()
    H_ = denetim(); sys.stdout.flush()
    cak = {}
    if "hizli" not in arg:
        cak["makine"] = len(cakisma()); sys.stdout.flush()
        cak["urun"] = len(urun_cakisma()); sys.stdout.flush()
        cak["itici_E"] = len(e_itici_cakisma()); sys.stdout.flush()
        a7_, b7_ = e7_ileri(); sys.stdout.flush()                                             # v6 2. tur: E v7 ileri uyum
        if a7_ is not None: cak["urun_E7"] = len(a7_); cak["itici_E7"] = len(b7_)
    if "glb" in arg or "hepsi" in arg:
        glb_yaz(os.path.join(KOK, "otonom", "hat3d", "kesme_v6.glb"))
    if "bom" in arg or "hepsi" in arg:
        bom_yaz(os.path.join(KOK, "arastirma", "4_KESME_v6"))
    json_yaz(os.path.join(KOK, "otonom", "hat3d", "kesme_v6.json"), H_, cak)
    kal = [d for d in DEN if not d[1]]
    print("DENETIM: %d madde · %d KALDI · cakisma %s · toplam %.0f sn" % (len(DEN), len(kal), cak, time.time() - t0))
    sys.stdout.flush(); os._exit(0)
