# -*- coding: utf-8 -*-
"""h3_e_sac_v1 — E (KUTU KATLAMA) İSTASYONU GÖVDESİ · ÜRETİM SACI v1 (2 Eki 2026 · Claude · YEREL · TASLAK, montaja bağlı DEĞİL)

Kemal: "gövdede tam çalışma; büküm gerçek; sanayi mutfaklarında nasıl kuruluyorsa öyle; nereden bükülür, vida nereye atılır, boşluk nerede açılır;
vidasına kadar ama mantıklı; sanayi tipi mutfakçı 3B'den direkt üretsin; sonra açınım verilip kesim/büküm yapılacak. Pafta YOK, önce 3B."

KAYNAKLAR: h3_sac_v1 (S) · h3_govde_ortak_v1 (GO, reçete + kılavuz) · sac_kararlar_v1.json > sac_standart_v1.json · E'nin mevcut gövdesi (kutu_cad_v14.govde/onyuz
           → h3_kutu_v1, E_GOVDE 43 parça) · v3.7 ön kapak düzeni h3_kapak_v1 (E_X, KARAR E_DERZ, B_UST, Y_DUZ, Y_TAVAN_KAPAK, E_AGIZ, E_KLAPE — ÇALIŞMA ANINDA okunur) ·
           elektrik deliği h3/_elk (KC 'ust_sac' Harting kesiği) · K pilotunun E'ye açtığı 3 × M8 (h3_k_sac_v1.M8_E).
KOORDİNAT: E YERELİ (kutu_cad_v14 / h3_kutu_v1 ile aynı: x 0…830, dünya = x + 4400 · y yerden · z ön +79 / arka −830). Bütün PARÇALAR KC.PARCALAR sözleşmesinde (wp yerel).

KURGU (kendinden taşıyıcı bükümlü kutu — iskelet YOK; mekanizma duvarlara / tavana / tabana bağlı, mevcut kurgu korunur)
  1 · TABAN 3 mm düz levha (123–126) → moduler alt şasesine (40 × 60 × 3, M12 kaynak somunlu 6 ayak) oturur · kenarlarına 3 mm L KULAK (kaynaklı) ·
      ön dikmelerin (orta + sağ) 3 mm ayak plakaları tabandaki PEM FHP-M6'ya (baş ALTTA flush) üstten pul + fiberli somun · mekanizma ayakları FHP-M5
      (baş altta flush, arayüz) — tabanın altında HİÇBİR çıkıntı yok (montaj denetimi: gövde altı = 123, alt şaseye düz oturur).
  2 · YAN SACLAR 1,5 (sol: pizza penceresi · sağ: şarjör yan kapısı açıklığı) · arka 90° dönüş 25 (arka sacın iç yüzüne · PEM SP-M5 + ISO 7380 arkadan) ·
      üst 90° dönüş 25 (tavan sacının altına · tavandan FHP-M5) · ön 90° dönüş (dikmenin önünde, kapak dayaması · sol 15,5 / sağ 13,5: menteşe plakası payı) ·
      tabana / ön dikmelere / tavan kirişlerine kaynaklı kulaklardan FHP-M5 gömme saplama (dışta iz yok) · sağ sacta şarjör açıklığı arka köşeye kadar
      (bükümden 1,75 mm'de kesik üretilemez → arka dönüş iki parça: açıklığın altı + üstü).
  3 · ARKA SAC 1,5 · üst 90° dönüş 25 (tavan altına) · yan dönüşler + taban kulakları + pano burçları + mekanizma ISO 7380 M5 arkadan (arka yüzde vida serbest).
  4 · TAVAN SACI 1,5 düz (üstünde U_KE oturur → dış yüzde yalnız FHP gömme saplama) · altında 2 × 40 × 40 × 2 KİRİŞ (z −245 / −500: askı sıraları arasında)
      kulaklarla yan saclara · mekanizma askıları (besleyici + piston) FHP-M5 · U_KE'ye 4 × M8 (E içinden, U_KE raf kirişlerine).
  5 · ÖN KASA = KAYNAKLI ALT MONTAJ: sol dikme 30 × 30 × 2 (y 442'den: altında robot çöpü kovası çekme yolu) · orta dikme 40 × 40 × 2 (iki kapağın bas-açları) ·
      sağ dikme 30 × 30 × 2 · 788 kayıtları + üst kayıtlar 30 × 30 × 2 · orta + sağ dikme 3 mm ayak plakalı · dikme başları 2 mm tapa.
  6 · 4 ÇİFT CİDARLI KAPAK (v3.7: 2 × 2 · yatay derz 785/788 · dikey derz E_DERZ): dış tava 1,5 (bindirme + TIG) + iç tava 1,0 (punta) · gizli 180° kaldır-çıkar menteşe
      dış dikmelerin içinde (alt 2 · üst 3) · bas-aç orta dikmenin içinde (her kapağa 2) · robot ağzı = sol üst kapakta pencere + 4 kasa çıtası · robot çöpü
      klapesi = sol alt kapakta 130 × 130 dış açıklık + klapenin içe döndüğü iç cep (kasa çıtalı) · KULP YOK.
  7 · ŞARJÖR YAN KAPISI 1,5 DÜZ levha (v14'ün 12'lik dönüşleri gerçek büküm R'siyle kılavuz taşıyıcısının raylarına binerdi) · sağ kılavuz taşıyıcısı
      (mekanizma, kapıda) rayları kapıya 4 × CD M4 (iç yüzde kaynak, dışta iz yok) — rijitliği taşıyıcı verir · arka kenarda 2 gizli menteşe (sabit yarısı
      arka sacın iç yüzünde, ISO 7380 arkadan) · ön kenarda 1 bas-aç (gövdesi yan sacın iç yüzünde, FHP-M5).
  8 · BAĞLANTI: K ← E 3 × M8 (K'nın perçin somunları, E sol sacında Ø9) · E ← B 2 × M8 (taban sol kulaklarında DIN 929 kaynak somunu, B içinden) ·
      E → U_KE 4 × M8 (E içinden, U_KE raf kirişi alt duvarında perçin somun) · E taban → alt şase 4 × M8 (arayüz).
ARAYÜZLER DEĞİŞMEZ: dış ölçüler 0–830 × 123–1862 × −830…+59 · kapak +59…+79 · kotlar · pizza penceresi · robot ağzı · klape · şarjör açıklığı (arka kenar hariç) ·
  ayak noktaları · mekanizma parçalarına dokunulmaz (bağlantıları ARAYÜZ listesinde, karşı delik mekanizma sahibine).
Çalıştır (öz denetim + çıktılar <scratchpad>/sac_e): python -u <scratchpad>/sac_e/e_sac_denetim_v1.py"""
import math, os, sys, json, time, re, collections
H3 = os.path.dirname(os.path.abspath(__file__)); _U = os.path.dirname(H3)
for _p in (_U, H3):
    if _p not in sys.path: sys.path.insert(0, _p)
import numpy as np
import cadquery as cq
import h3_sac_v1 as S
import h3_govde_ortak_v1 as GO

SURUM = "h3_e_sac_v1"
V = cq.Vector
X_E = 4400.0
BIRIM = "E_GOVDE"
# ---------------------------------------------------------------- ARAYÜZ (E yereli · değişmez) ----------------------------------------------------------------
W = 830.0
Y_ALT, Y_TB, Y_UST, Y_UA = 123.0, 126.0, 1862.0, 1860.5
Z_A, Z_AI, Z_ON, Z_KAP, Z_CER = -830.0, -828.5, 59.0, 79.0, 57.0          # Z_ON: gövde ön düzlemi = kapak iç düzlemi · Z_CER: ön kasa ön yüzü
PENCERE = (978.0, 1062.0, -372.0, -24.0)                                  # sol sac · K→E pizza penceresi (y0, y1, z0, z1) = K E_PENCERE = kutu_cad_v14.PENCERE
SARJOR_AC = (231.0, 989.0, -823.0, -411.0)                               # sağ sac · şarjör yan kapısı açıklığı (mevcut) · arka kenarı köşeye uzar (sapma)
SARJOR_KAPI = (234.0, 986.0, -820.0, -414.0)                             # yan kapı (mevcut)
AYAK_XZ = ((60.0, -110.0), (770.0, -110.0), (60.0, -770.0), (770.0, -770.0), (415.0, -110.0), (415.0, -770.0))   # kutu_cad_v14.AYAK_XZ (moduler alt şase okur)
K_M8 = ((1100.0, -800.0), (1750.0, -800.0), (877.0, -100.0))             # h3_k_sac_v1.M8_E → E sol sacında Ø9 (y, z)
KLAPE_ICE = dict(levha=(58.0, 200.0, 604.0, 753.5), yaprak=(69.0, 189.0, 742.5, 770.0), z=(66.4, 77.6))   # ecop_klape_* (mekanizma, kanatla döner) E yereli
# ---------------------------------------------------------------- ön kasa ----------------------------------------------------------------
PB, PB_O = 30.0, 40.0
X_DSOL, X_DSAG = 16.5, W - 16.5
Z_D, Z_DO = Z_CER - PB / 2.0, Z_CER - PB_O / 2.0                          # 42 · 37
Y_DSOL0 = 442.0                                                          # sol dikme altı (+2 tapa = 440): robot çöpü kovası (y ≤ 428) öne çekilir
Y_D0, Y_D1 = Y_TB + 3.0, Y_UA - 2.0                                      # 129 (3 mm ayak plakası üstü) · 1858,5 (+2 tapa = 1860,5)
Y_K788, Y_KUST = 788.0, Y_UA - PB / 2.0                                  # kayıt eksenleri
# kapak donanımı
MENTESE_ALT, MENTESE_UST = (480.0, 700.0), (900.0, 1360.0, 1750.0)
MENTESE_SOL = dict(govde_a=(12.5, 25.0))                                 # sol kapak kenarı x 2 (sağdakiler x 830 = yan sac dış yüzü) → menteşe penceresi 30'luk dikmenin düz yüzünde kalsın
BASAC_ALT, BASAC_UST, BASAC_A = (300.0, 650.0), (1150.0, 1800.0), 8.0      # orta dikme 40: bas-aç deliği düz yüzde (± 16) · uç iç tavanın düz alanında
# tavan kirişleri (40 × 40 × 2 · askı sıraları arasında) · tavan sacı ↔ kiriş kulakları
KIRIS_Z = (-245.0, -500.0)
KIRIS_X = (28.0, 802.0)                                                  # tapalar 26–28 / 802–804 · yan sacların üst dönüşüne (x ≤ 25) 1 mm
# bağlantı noktaları
B_M8_Z = (-700.0, -590.0)                                                # E ← B · taban sol kulaklarında DIN 929 M8
UKE_M8 = ((417.5, -100.0), (417.5, -600.0), (813.5, -100.0), (813.5, -600.0))   # E → U_KE raf kirişi_2 (dünya 4802,5–4832,5) / _3 (5198,5–5228,5)
SASE_M8 = ((230.0, -110.0), (600.0, -110.0), (230.0, -770.0), (600.0, -770.0))   # taban → moduler alt şase boyuna (arayüz)
# ---- VERİ (sac_e/q_ref_e2 → gen_veri_e · 2 Eki 2026 · elle düzenleme — yeniden üret) ----
HARTING = (667.0, 733.0, -778.0, -742.0)                                       # E Harting Han 10B soket kesiği (h3/_elk delik.brep · KC|ust_sac · E yereli x0, x1, z0, z1)
MEK_TEMAS = [                                                            # mekanizma (SABIT) ↔ duvar temas yamaları (v3.6 döküm, E yereli) — bağlantı noktaları buradan
    dict(ad='kilavuz_arka_tasiyici', duvar='arka', bb=(48.0, 772.0, 244.0, 972.0, -828.5, -828.2), alan=527072.0),
    dict(ad='pano_plakasi_burcu_0', duvar='arka', bb=(74.0, 86.0, 1411.0, 1423.0, -828.5, -828.2), alan=113.1),
    dict(ad='pano_plakasi_burcu_1', duvar='arka', bb=(754.0, 766.0, 1411.0, 1423.0, -828.5, -828.2), alan=113.1),
    dict(ad='pano_plakasi_burcu_2', duvar='arka', bb=(74.0, 86.0, 1831.0, 1843.0, -828.5, -828.2), alan=113.1),
    dict(ad='pano_plakasi_burcu_3', duvar='arka', bb=(754.0, 766.0, 1831.0, 1843.0, -828.5, -828.2), alan=113.1),
    dict(ad='asansor_ray_plakasi_ust_kosebendi_sag', duvar='sag', bb=(828.2, 828.5, 940.0, 972.0, -404.0, -378.0), alan=832.0),
    dict(ad='besleyici_motor_rafi', duvar='sag', bb=(828.2, 828.5, 1321.0, 1327.0, -376.0, -314.0), alan=372.0),
    dict(ad='kablo_kanali_ust_mesafe_0', duvar='sag', bb=(828.2, 828.5, 1240.0, 1260.0, -45.0, -30.0), alan=300.0),
    dict(ad='kablo_kanali_ust_mesafe_1', duvar='sag', bb=(828.2, 828.5, 1490.0, 1510.0, -45.0, -30.0), alan=300.0),
    dict(ad='kablo_kanali_ust_mesafe_2', duvar='sag', bb=(828.2, 828.5, 1750.0, 1770.0, -45.0, -30.0), alan=300.0),
    dict(ad='kalip_alt_rafi_duvar_takozu_sag', duvar='sag', bb=(828.2, 828.5, 588.0, 618.0, -372.0, -55.0), alan=9510.0),
    dict(ad='sarjor_kapi_esigi_kosebendi_sag', duvar='sag', bb=(828.2, 828.5, 880.0, 930.0, -411.5, -380.0), alan=1575.0),
    dict(ad='sensor_blank_var_braketi', duvar='sag', bb=(828.2, 828.5, 1053.0, 1080.0, -216.0, -196.0), alan=540.0),
    dict(ad='sensor_yigin_ustu_braketi', duvar='sag', bb=(828.2, 828.5, 1053.0, 1080.0, -800.0, -780.0), alan=540.0),
    dict(ad='asansor_ray_plakasi_ust_kosebendi_sol', duvar='sol', bb=(1.5, 1.8, 940.0, 972.0, -404.0, -378.0), alan=832.0),
    dict(ad='kalip_alt_rafi_koseben_sol', duvar='sol', bb=(1.5, 1.8, 588.0, 618.0, -372.0, -24.0), alan=10440.0),
    dict(ad='kilavuz_sol_tasiyici', duvar='sol', bb=(1.5, 1.8, 244.0, 984.0, -700.0, -680.0), alan=14800.0),
    dict(ad='kopru_motor_askisi', duvar='sol', bb=(1.5, 1.8, 776.0, 832.0, -236.0, -176.0), alan=3360.0),
    dict(ad='kopru_plaka_tutucu', duvar='sol', bb=(1.5, 1.8, 832.0, 853.0, -346.0, -66.0), alan=5880.0),
    dict(ad='sarjor_kapi_esigi_kosebendi_sol', duvar='sol', bb=(1.5, 1.8, 880.0, 930.0, -411.5, -380.0), alan=1575.0),
    dict(ad='sensor_kutu_dolu_braketi', duvar='sol', bb=(1.5, 1.8, 1099.0, 1130.0, -250.0, -230.0), alan=620.0),
    dict(ad='asansor_kayis_koruyucu', duvar='taban', bb=(380.0, 772.0, 126.0, 126.3, -417.0, -363.0), alan=888.0),
    dict(ad='asansor_motor_plakasi', duvar='taban', bb=(704.0, 766.0, 126.0, 126.3, -410.0, -407.0), alan=186.0),
    dict(ad='asansor_motor_plakasi', duvar='taban', bb=(704.0, 766.0, 126.0, 126.3, -354.0, -351.0), alan=186.0),
    dict(ad='asansor_ray_plakasi', duvar='taban', bb=(200.0, 379.0, 126.0, 126.3, -378.0, -374.0), alan=716.0),
    dict(ad='asansor_ray_plakasi_flansi', duvar='taban', bb=(200.0, 600.0, 126.0, 126.3, -363.0, -354.0), alan=3600.0),
    dict(ad='ecop_cop_kova_kizagi', duvar='taban', bb=(16.0, 198.0, 126.0, 126.3, -396.0, 29.0), alan=77350.0),
    dict(ad='kablo_kanali_dikey', duvar='taban', bb=(806.0, 826.0, 126.0, 126.3, -50.0, -25.0), alan=500.0),
    dict(ad='sarjor_kapi_esigi', duvar='taban', bb=(8.0, 188.0, 126.0, 126.3, -414.5, -399.0), alan=2665.0),
    dict(ad='sarjor_kapi_esigi', duvar='taban', bb=(222.0, 379.0, 126.0, 126.3, -414.5, -399.0), alan=2358.5),
    dict(ad='sarjor_kapi_esigi', duvar='taban', bb=(773.0, 812.0, 126.0, 126.3, -414.5, -399.0), alan=542.0),
    dict(ad='besleyici_plaka_askisi_0', duvar='ust', bb=(140.0, 160.0, 1860.2, 1860.5, -600.0, -580.0), alan=400.0),
    dict(ad='besleyici_plaka_askisi_1', duvar='ust', bb=(640.0, 660.0, 1860.2, 1860.5, -600.0, -580.0), alan=400.0),
    dict(ad='besleyici_plaka_askisi_2', duvar='ust', bb=(140.0, 160.0, 1860.2, 1860.5, -420.0, -400.0), alan=400.0),
    dict(ad='besleyici_plaka_askisi_3', duvar='ust', bb=(640.0, 660.0, 1860.2, 1860.5, -420.0, -400.0), alan=400.0),
    dict(ad='piston_BK_askisi_0', duvar='ust', bb=(240.0, 300.0, 1860.2, 1860.5, -345.0, -339.0), alan=360.0),
    dict(ad='piston_BK_askisi_1', duvar='ust', bb=(240.0, 300.0, 1860.2, 1860.5, -311.0, -305.0), alan=360.0),
    dict(ad='piston_eksen_askisi', duvar='ust', bb=(170.0, 370.0, 1860.2, 1860.5, -394.0, -380.0), alan=2800.0),
    dict(ad='piston_motor_askisi_0', duvar='ust', bb=(308.0, 316.0, 1860.2, 1860.5, -350.0, -336.0), alan=112.0),
    dict(ad='piston_motor_askisi_1', duvar='ust', bb=(364.0, 372.0, 1860.2, 1860.5, -350.0, -336.0), alan=112.0),
]
# ---- VERİ SONU ----
ESKI_GOVDE = tuple(["ayak_%d" % i for i in range(6)] + ["taban_sac_3", "arka_sac", "ust_sac", "sol_sac_pizza_penceresi", "sag_sac", "sarjor_yan_kapisi",
                    "sarjor_yan_kapisi_mentese_0", "sarjor_yan_kapisi_mentese_1", "sarjor_yan_kapisi_basac", "onyuz_dikme_sol", "onyuz_dikme_sag",
                    "onyuz_kayit_orta", "onyuz_kayit_ust", "onyuz_alt_kanat_sol", "onyuz_alt_kanat_sag", "onyuz_orta_sabit_panel", "onyuz_orta_servis_kapagi",
                    "onyuz_ust_kanat_sol", "onyuz_ust_kanat_sag", "onyuz_alt_dayama_dudagi"] +
                   ["onyuz_mentese_%d" % i for i in range(12)] + ["onyuz_basac_%d" % i for i in range(5)])
GOVDE_ONEK = ("ayak_", "taban_sac", "plint_on", "arka_sac", "ust_sac", "sol_sac", "sag_sac", "sarjor_yan_kapisi", "on_ust_kapak", "kose_dikme_", "onyuz_", "govde_")
KAPAKLAR = ("onyuz_kapak_E_alt_sol", "onyuz_kapak_E_alt_sag", "onyuz_kapak_E_ust_sol", "onyuz_kapak_E_ust_sag")
KANAT_AD = ("ecop_klape_levhasi", "ecop_klape_mentesesi", "ecop_klape_mentese_yapragi", "ecop_serit_dusme_olugu")   # sol alt kapakla döner (mekanizma)
S._RENK.update({"profil": ((0.70, 0.73, 0.77, 1.0), 0.85, 0.30), "mekanizma": ((0.42, 0.46, 0.52, 1.0), 0.4, 0.5), "arayuz": ((0.90, 0.22, 0.15, 1.0), 0.3, 0.5),
                "kapak": ((0.70, 0.82, 0.95, 1.0), 0.2, 0.25)})


def kapak_olcu():
    """v3.7 E kapak düzeni (h3_kapak_v1 — ÇALIŞMA ANINDA okunur · başka ajan koordinat düzeltmesi yapabilir) → E yereli"""
    import h3_kapak_v1 as HK
    d0, d1 = HK.KARAR["E_DERZ"]
    y1 = HK.Y_TAVAN_KAPAK if HK.KARAR["KE_1862_KALKAR"] else 1859.0
    a = HK.E_AGIZ; k = HK.E_KLAPE
    return dict(u0=HK.E_X[0] - X_E, u1=HK.E_X[1] - X_E, d0=d0 - X_E, d1=d1 - X_E, alt=(126.0, float(HK.B_UST)), ust=(float(HK.Y_DUZ), float(y1)),
                agiz=(a[0] - X_E, a[1] - X_E, a[2], a[3]), klape=(k[0] - X_E, k[1] - X_E, k[2], k[3]), kaynak="h3_kapak_v1 E_X %s · E_DERZ %s · B_UST %s · Y %s"
                % (HK.E_X, HK.KARAR["E_DERZ"], HK.B_UST, (HK.Y_DUZ, y1)))


# =====================================================================================================================================
# 0 · yardımcılar
# =====================================================================================================================================
G = None                       # kurulan Govde (modül düzeyinde tek örnek)
P = {}                         # paneller / profiller: ad → nesne
ATLANAN = []                   # konumu uymadığı için atlanan mekanizma bağlantıları (rapor)
EK = {}                        # rapor ekleri


def _n(v):
    v = np.asarray(v, float); return v / np.linalg.norm(v)


def kutu(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), V(min(x0, x1), min(y0, y1), min(z0, z1)))


def kulak(g, ad, A, stud, u, v, v_cerceve, L_kaynak=25.0, gen=25.0, uc=9.75, dis="M5", birlesim="pem_saplama", kaynak_bas=None, rol="braket", not_="kulak ↔ çerçeve", t=None):
    """3 mm L KULAK (GO.kulak ile aynı geometri) · birlesim 'pem_saplama' (A'da FHP gömme saplama, dışta iz yok) ya da 'pem_somun' (kulakta PEM SP,
    A dışından ISO 7380 — arka sac) · kaynak_bas: kaynak dikişinin A'dan başladığı mesafe (çerçeve yüzü A'dan uzakta başlıyorsa)"""
    s = g.sac(ad, rol, t=t) if t else g.sac(ad, rol)
    stud = np.asarray(stud, float); u, v = np.asarray(u, float), np.asarray(v, float)
    t, R = s.t, s.R
    vb = v_cerceve - (R + t)
    if vb < S.DIN9021[dis][1] / 2.0 + 1.0 - 1e-9: raise ValueError("%s: pul büküme taşar" % ad)
    n = np.cross(u, v)
    zA = A.yerel(stud + n * 1.0)[2]
    if -1e-6 < zA < A.sac.t + 1e-6: raise ValueError("%s: u × v A panelinin içine bakıyor" % ad)
    Pk = s.taban([(-gen / 2, -uc), (gen / 2, -uc), (gen / 2, vb), (-gen / 2, vb)], O=tuple(stud), ex=tuple(u), ey=tuple(v), ad="saplama_ayagi")
    Pk.flans(2, L_kaynak, yon=+1, ad="kaynak_ayagi")
    k0 = max(R + t, kaynak_bas if kaynak_bas is not None else 0.0)
    for sg in (+1, -1):
        p0 = stud + u * sg * gen / 2.0 + v * v_cerceve + n * k0
        p1 = stud + u * sg * gen / 2.0 + v * v_cerceve + n * L_kaynak
        g.kaynak(S.kaynak_dikisi(p0, p1, u * sg, -v, min(t, 3.0), ad=ad + "_kaynak_%s" % ("a" if sg > 0 else "b"), birim=g.birim, taraf="dis (köşe)", not_=not_))
    b = S.vidali_birlesim(A, Pk, tuple(stud), birlesim, dis=dis, ad=ad + "_bag", birim=g.birim)
    for q in b["parcalar"]: g.eleman(q)
    g.BIRLESIM.append(b); g.KULAK.append(s)
    return s, Pk, b


def bag(g, A, B, nokta, tip, ad, dis="M5"):
    b = S.vidali_birlesim(A, B, tuple(nokta), tip, dis=dis, ad=ad, birim=g.birim)
    for q in b["parcalar"]: g.eleman(q)
    g.BIRLESIM.append(b)
    return b


def serbest(Pn, u, v, r, kenar=8.0, kopru=3.0):
    """panel düz bölgesinde (u, v) çevresinde r yarıçaplı delik / PEM için yer var mı · kenar: kenara (büküm teğeti dahil) eksen mesafesi ·
    kopru: mevcut kesiklere kenar mesafesi"""
    if not Pn.icerir(u, v): return False
    q = np.array([u, v])
    for i in range(len(Pn.poly)):
        k = Pn.kenar(i); d = q - k["p0"]; s_ = np.clip(np.dot(d, k["e2"]), 0.0, k["L"])
        if np.linalg.norm(d - k["e2"] * s_) < kenar - 1e-6: return False
    nok = cq.Vertex.makeVertex(float(u), float(v), 0.0)
    for k in Pn.kesikler:
        if k.tip in ("rahatlatma", "kose_rahatlatma"): continue
        if k.yuz.distance(nok) < r + kopru - 1e-6: return False
    return True


# =====================================================================================================================================
# 1 · SACLAR (taban · yanlar · arka · tavan)
# =====================================================================================================================================
def taban(g):
    s = g.sac("taban_sac_3", "braket", t=3.0)
    # ön köşeler 2,5 × 45° pah: yan sacların ön dönüş büküm yayı (R 2,25, x 1,5–3,75 · z 55,25–59) tabanın köşesine binmesin
    Pn = s.taban([(4.0, -57.5), (W - 4.0, -57.5), (W - 1.5, -55.0), (W - 1.5, -Z_AI), (1.5, -Z_AI), (1.5, -55.0)], O=(0, Y_ALT, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="taban")
    P["taban"] = Pn
    s.notlar.append("3 mm düz levha · moduler alt şasesine oturur (40 × 60 × 3, 6 ayak) · kenarlarında kaynaklı kulaklar")
    return s


def yan_sol(g):
    s = g.sac("sol_sac_pizza_penceresi", "dis", kabuk=True); gg = s.R + s.t
    vb, vf, y1 = Z_AI + gg, Z_ON - gg, Y_UA - gg
    Pn = s.taban([(Y_ALT, vb), (y1, vb), (y1, vf), (Y_ALT, vf)], O=(0, 0, 0), ex=(0, 1, 0), ey=(0, 0, 1), ad="yan")
    arka = Pn.flans(0, 25.0, yon=+1, bas=3.5, ad="arka_donus")                  # arka sacın iç yüzüne · tabanın üstünden başlar
    ust = Pn.flans(1, 25.0, yon=+1, son=vf - 25.0, ad="ust_donus")              # tavan sacının altına · ön kasaya 2 kala biter (z 25)
    s.kose(arka, ust, "acik", rahat="kare")
    on = Pn.flans(2, 15.5, yon=+1, ad="on_donus")                                # dikmenin 0,5 önünde · kapak iç tavasına dayama (z 57,5–59)
    y0, y1_, z0, z1 = PENCERE
    Pn.dikdortgen((y0 + y1_) / 2.0, (z0 + z1) / 2.0, y1_ - y0, z1 - z0, r=6.0, tip="pizza_penceresi", parca="K→E pizza penceresi 84 × 348 (R6 · kenar çapaksız) = K sağ sacı")
    for y, z in K_M8:
        Pn.delik(y, z, 9.0, tip="vida_deligi", parca="K ↔ E M8 (K dikme / kuşak perçin somunu · cıvata E içinden · ISO 273 orta)")
    P["sol"] = dict(yan=Pn, arka=arka, ust=ust, on=on, s=s)
    return s


def yan_sag(g):
    s = g.sac("sag_sac", "dis", kabuk=True); gg = s.R + s.t
    vb, vf, y1 = -Z_AI - gg, -Z_ON + gg, Y_UA - gg                             # v = −z
    ya, yb, za, zb = SARJOR_AC
    poly = [(Y_ALT, vf), (y1, vf), (y1, vb), (yb, vb), (yb, -zb), (ya, -zb), (ya, vb), (Y_ALT, vb)]
    Pn = s.taban(poly, O=(W, 0, 0), ex=(0, 1, 0), ey=(0, 0, -1), ad="yan")
    on = Pn.flans(0, 13.5, yon=+1, ad="on_donus")                                # menteşe plakası x 816'dan başlar → dönüş 13,5
    ust = Pn.flans(1, 25.0, yon=+1, bas=(-25.0) - vf, ad="ust_donus")
    arka_ust = Pn.flans(2, 25.0, yon=+1, ad="arka_donus_ust")
    s.kose(ust, arka_ust, "acik", rahat="kare")
    arka_alt = Pn.flans(6, 25.0, yon=+1, son=3.5, ad="arka_donus_alt")
    P["sag"] = dict(yan=Pn, arka=arka_ust, arka_alt=arka_alt, ust=ust, on=on, s=s)
    return s


def arka(g):
    s = g.sac("arka_sac", "dis", kabuk=True); gg = s.R + s.t
    y1 = Y_UA - gg
    Pn = s.taban([(0.0, Y_ALT), (W, Y_ALT), (W, y1), (0.0, y1)], O=(0, 0, Z_A), ex=(1, 0, 0), ey=(0, 1, 0), ad="arka")
    ust = Pn.flans(2, 25.0, yon=+1, bas=26.0, son=26.0, ad="ust_donus")         # tavan altına · yan sacların üst dönüşleri arasında
    P["arka"] = dict(arka=Pn, ust=ust, s=s)
    return s


def tavan(g):
    s = g.sac("ust_sac", "dis", kabuk=True)
    Pn = s.taban([(0.0, -Z_CER), (W, -Z_CER), (W, -Z_A), (0.0, -Z_A)], O=(0, Y_UA, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="ust")
    if HARTING is not None:
        x0, x1, z0, z1 = HARTING
        Pn.dikdortgen((x0 + x1) / 2.0, -(z0 + z1) / 2.0, x1 - x0, z1 - z0, tip="harting_kesigi", parca="E Harting Han 10B soket kesiği (h3_elk · KC ust_sac)")
    P["ust"] = Pn
    s.notlar.append("üstünde U_KE tabanı oturur → dış yüzde yalnız FHP gömme saplama başı (düz)")
    return s


# =====================================================================================================================================
# 2 · ÖN KASA (kaynaklı alt montaj) · tavan kirişleri
# =====================================================================================================================================
def on_kasa(g, KO):
    xm = (KO["d0"] + KO["d1"]) / 2.0
    ds = g.profil("onyuz_dikme_sol", "y", Y_DSOL0, Y_D1, (X_DSOL, Z_D), b=PB, not_="sol dikme 30 × 30 × 2 (y 440'tan: altında robot çöpü kovasının çekme yolu)")
    do = g.profil("onyuz_dikme_orta", "y", Y_D0, Y_D1, (xm, Z_DO), b=PB_O, not_="orta dikme 40 × 40 × 2 (iki kapağın bas-açları içinde)")
    dg = g.profil("onyuz_dikme_sag", "y", Y_D0, Y_D1, (X_DSAG, Z_D), b=PB, not_="sağ dikme 30 × 30 × 2")
    xo0, xo1 = xm - PB_O / 2.0, xm + PB_O / 2.0
    xs1, xg0 = X_DSOL + PB / 2.0, X_DSAG - PB / 2.0
    kay = {}
    for nm, yc in (("788", Y_K788), ("ust", Y_KUST)):
        kay[nm] = (g.profil("onyuz_kayit_%s_sol" % nm, "x", xs1, xo0, (yc, Z_D), b=PB, not_="%s kayıt sol (dikmelere alın)" % nm),
                   g.profil("onyuz_kayit_%s_sag" % nm, "x", xo1, xg0, (yc, Z_D), b=PB, not_="%s kayıt sağ (dikmelere alın)" % nm))
    P.update(dsol=ds, dorta=do, dsag=dg, kayit=kay, xm=xm)
    # kaynak bölgeleri (profil DFM) + kuşak uç kaynakları (içbükey köşeler)
    for nm, yc in (("788", Y_K788), ("ust", Y_KUST)):
        y0, y1 = yc - PB / 2.0, yc + PB / 2.0
        ds.kaynak_bolgesi("+x", y0, y1); dg.kaynak_bolgesi("-x", y0, y1); do.kaynak_bolgesi("-x", y0, y1); do.kaynak_bolgesi("+x", y0, y1)
        yz = [(0, 1.0, 0), (0, -1.0, 0)] if nm == "788" else [(0, -1.0, 0)]
        ks, kg = kay[nm]
        g.kaynak(GO.uc_kaynaklari("onyuz_kayit_kaynak_%s_sol_0" % nm, (xs1, yc, Z_D), (1, 0, 0), yz, b=PB, birim=g.birim))
        g.kaynak(GO.uc_kaynaklari("onyuz_kayit_kaynak_%s_sol_1" % nm, (xo0, yc, Z_D), (-1, 0, 0), yz + [(0, 0, -1.0)], b=PB, birim=g.birim))
        g.kaynak(GO.uc_kaynaklari("onyuz_kayit_kaynak_%s_sag_0" % nm, (xo1, yc, Z_D), (1, 0, 0), yz + [(0, 0, -1.0)], b=PB, birim=g.birim))
        g.kaynak(GO.uc_kaynaklari("onyuz_kayit_kaynak_%s_sag_1" % nm, (xg0, yc, Z_D), (-1, 0, 0), yz, b=PB, birim=g.birim))
    # tapalar (üst + sol dikme altı)
    for d in (ds, do, dg): GO.dikme_tapasi(g, d, "ust")
    GO.dikme_tapasi(g, ds, "alt", ad=ds.ad + "_tapa_alt")
    g.not_("dikme tapaları 2 mm, köşeler 2,5 pah · çevresi TIG alın kaynağı, taşlanır (kapalı profil · yüzle aynı → katı yok)")
    # orta + sağ dikme ayak plakaları 3 mm (dikmeye 4 kenar köşe kaynağı) → tabanda 2 × PEM FHP-M6 (baş taban ALT yüzünde gömme/flush: gövde altı 123
    # düz kalır, alt şaseye oturur) · plakada Ø6,6 + DIN 9021 + ISO 10511 M6 üstten · pul dikme kaynağına ≥ 1 mm
    for ad, d, (x0, x1), boltlar in (("onyuz_dikme_orta_ayak", do, (xo0 - 24.0, xo1 + 24.0), ((xo0 - 12.0, Z_DO), (xo1 + 12.0, Z_DO))),
                                       ("onyuz_dikme_sag_ayak", dg, (xg0 - 28.0, W - 1.5), ((xg0 - 14.0, Z_DO - 10.0), (xg0 - 14.0, Z_DO + 10.0)))):
        s = g.sac(ad, "braket", t=3.0)
        z0, z1 = Z_CER - PB_O, Z_CER
        if x1 > W - 2.0:                                                  # sağ plaka yan sacın büküm yayına (x 826,25–828,5 · z 55,25–57) binmesin: ön-sağ köşe 2,5 pah
            Pa = s.taban([(x0, -z1), (x1 - 2.5, -z1), (x1, -z1 + 2.5), (x1, -z0), (x0, -z0)], O=(0, Y_TB, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="ayak")
        else:
            Pa = s.taban([(x0, -z1), (x1, -z1), (x1, -z0), (x0, -z0)], O=(0, Y_TB, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="ayak")
        cx, cz = d.c; h = d.b / 2.0; fl = d.b - 2 * d.Ro
        # köşe kaynağı: ön yüz (+z) kapak arkasında / yan sacın ön dönüşünde → YOK · sağ dikmenin +x yüzü yan saca dayalı → YOK (3 / 2 kenar yeter)
        for i, (nx, nz) in enumerate(((1, 0), (-1, 0), (0, 1), (0, -1))):
            if nz == 1 or (nx == 1 and x1 > W - 2.0): continue
            pc = np.array([cx + nx * h, Y_D0, cz + nz * h]); w = np.array([abs(nz), 0, abs(nx)])
            g.kaynak(S.kaynak_dikisi(pc - w * fl / 2, pc + w * fl / 2, (nx, 0, nz), (0, 1, 0), 2.0, ad="%s_kaynak_%d" % (ad, i), birim=g.birim, taraf="dis (köşe)",
                                     not_="dikme ↔ ayak plakası"))
        for j, (bx, bz) in enumerate(boltlar):
            bag(g, P["taban"], Pa, (bx, Y_ALT, bz), "pem_saplama", ad="govde_bag_%s_%d" % (ad.replace("onyuz_", ""), j), dis="M6")
        P[ad] = Pa
    return ds, do, dg


def tavan_kirisleri(g):
    out = []
    for zc in KIRIS_Z:
        k = g.profil("ust_sac_kirisi_%d" % int(-zc), "x", KIRIS_X[0], KIRIS_X[1], (Y_UA - 20.0, zc), b=40.0,
                     not_="tavan kirişi (askı sıraları arasında · uçlar kulakla yan saclara · tavan sacı kulaklarla)")
        GO.dikme_tapasi(g, k, "ust", ad=k.ad + "_tapa_sag"); GO.dikme_tapasi(g, k, "alt", ad=k.ad + "_tapa_sol")
        out.append(k)
    P["kiris"] = out
    return out


# =====================================================================================================================================
# 3 · KULAKLAR + PANEL BAĞLANTILARI
# =====================================================================================================================================
def kulaklar(g):
    A_s, A_g = P["sol"]["yan"], P["sag"]["yan"]
    # ön dikmeler ↔ yan saclar (dikmenin arka yüzüne · saplama z 8)
    for tr, A, d, xs, uy in (("sol", A_s, P["dsol"], 1.5, 1.0), ("sag", A_g, P["dsag"], W - 1.5, -1.0)):
        for y in GO.vida_konumlari(d.a0, d.a1, maks=200.0, uc=30.0 if tr == "sol" else 51.0):          # sağ: ilk kulak y 180 (altında taban kulağı z 0)
            kulak(g, "govde_kulak_%s_dikme_%d" % (tr, int(y)), A, (xs, y, 8.0), (0, uy, 0), (0, 0, 1.0), 19.0)
            d.kaynak_bolgesi("-z", y - 13.0, y + 13.0)
    # tavan kirişleri ↔ yan saclar (kiriş ön / arka yüzüne · kaynak kiriş başladığı yerden)
    for k in P["kiris"]:
        zc = k.c[1]
        for tr, A, xs, sg in (("sol", A_s, 1.5, 1.0), ("sag", A_g, W - 1.5, -1.0)):
            for yz, zs, vz in (("on", zc + 20.0 + 19.0, -1.0), ("arka", zc - 20.0 - 19.0, 1.0)):
                u = (0, sg * vz, 0)                                              # u × v = içe (sol +x · sağ −x)
                assert abs(np.dot(np.cross(u, (0, 0, vz)), (sg, 0, 0)) - 1.0) < 1e-9
                kulak(g, "govde_kulak_%s_kiris_%d_%s" % (tr, int(-zc), yz), A, (xs, Y_UA - 20.0, zs), u, (0, 0, vz), 19.0, L_kaynak=45.0,
                      kaynak_bas=(KIRIS_X[0] - 1.5) + 1.0, not_="kulak ↔ tavan kirişi ucu (kiriş x 26 / 804'te başlar)")
    # taban ↔ yan saclar (saplama y 145 · kulak tabana kaynaklı) · kova kızağı bölgesinde (sol, z > −397) kısa kaynak ayağı
    # sol: robot çöpü kova kızağı bölgesinde (z −397,5 … 29, kızak x ≥ 16) kulak 2 mm, kaynak ayağı 13 (2 mm için en kısa flanş 11) · en önde z 44 (gen 20: kaynak
    # dikişi kızağa / kovaya 2 mm) · B M8 kulakları (z −700 / −590) arasında −645 · sağ: en önde z 0 (dikey kablo kanalı z −50…−25 ile sağ ayak plakası arası)
    for tr, A, xs, zler in (("sol", A_s, 1.5, (-800.0, -645.0, -480.0, -330.0, -180.0, -30.0, 44.0)), ("sag", A_g, W - 1.5, (-800.0, -640.0, -480.0, -330.0, -170.0, 0.0))):
        for z in zler:
            kizak = tr == "sol" and -397.5 <= z <= 29.0 + 12.5
            u = (0, 0, 1.0) if tr == "sol" else (0, 0, -1.0)
            ad_ = "govde_kulak_%s_taban_%s" % (tr, ("on" if z > 0 else str(int(round(-z)))) if z != 0 else "0")
            kulak(g, ad_, A, (xs, Y_TB + 19.0, z), u, (0, -1.0, 0), 19.0, L_kaynak=13.0 if kizak else 25.0, gen=20.0 if z > 0 else 25.0, t=2.0 if kizak else None,
                  not_="kulak ↔ taban sacı" + (" (kova kızağı bölgesi · 2 mm)" if kizak else ""))
    # taban ↔ arka sac (kulakta PEM SP-M5, arkadan ISO 7380)
    A_a = P["arka"]["arka"]
    for x in GO.vida_konumlari(60.0, W - 60.0, maks=200.0, uc=0.0):
        kulak(g, "govde_kulak_arka_taban_%d" % int(x), A_a, (x, Y_TB + 19.0, Z_AI), (-1.0, 0, 0), (0, -1.0, 0), 19.0, birlesim="pem_somun", not_="kulak ↔ taban sacı")
    # tavan ↔ üst kayıtlar (kayıt arka yüzüne · saplama z 8) · tavan ↔ kirişler
    A_u = P["ust"]
    xm = P["xm"]
    for x in (90.0, 300.0, xm + 80.0, W - 90.0):
        kulak(g, "govde_kulak_ust_kayit_%d" % int(x), A_u, (x, Y_UA, 8.0), (1.0, 0, 0), (0, 0, 1.0), 19.0)
    for k in P["kiris"]:
        zc = k.c[1]
        xl = (90.0, 450.0, 740.0) if zc > -300 else (90.0, 400.0, 740.0)
        for x in xl:
            kulak(g, "govde_kulak_ust_kiris_%d_on_%d" % (int(-zc), int(x)), A_u, (x, Y_UA, zc + 20.0 + 19.0), (-1.0, 0, 0), (0, 0, -1.0), 19.0)
        for x in ((90.0, 520.0, 740.0) if zc > -300 else (90.0, 400.0, 740.0)):
            kulak(g, "govde_kulak_ust_kiris_%d_arka_%d" % (int(-zc), int(x)), A_u, (x, Y_UA, zc - 20.0 - 19.0), (1.0, 0, 0), (0, 0, 1.0), 19.0)
        for x in xl + (520.0,):
            k.kaynak_bolgesi("+z", x - 13.0, x + 13.0); k.kaynak_bolgesi("-z", x - 13.0, x + 13.0)


def panel_baglantilari(g):
    A_a, A_u = P["arka"]["arka"], P["ust"]
    # arka sac ↔ yan sacların arka dönüşleri (ISO 7380 M5 arkadan + dönüşte PEM SP-M5)
    for tr, B, x in (("sol", P["sol"]["arka"], 14.0), ("sag", P["sag"]["arka"], W - 14.0), ("sag_alt", P["sag"]["arka_alt"], W - 14.0)):
        if tr == "sag_alt": yl = (150.0, 207.0)
        elif tr == "sag": yl = GO.vida_konumlari(SARJOR_AC[1] + 12.0, Y_UA - 20.0, maks=200.0, uc=0.0)
        else: yl = GO.vida_konumlari(150.0, Y_UA - 20.0, maks=200.0, uc=0.0)
        for y in yl:
            bag(g, A_a, B, (x, y, Z_AI), "pem_somun", ad="govde_bag_arka_%s_%d" % (tr, int(y)))
    # tavan ↔ yan sacların üst dönüşleri (tavanda FHP-M5 · altta pul + fiberli somun)
    for tr, B, x in (("sol", P["sol"]["ust"], 14.0), ("sag", P["sag"]["ust"], W - 14.0)):
        for z in GO.vida_konumlari(Z_AI + 30.0, 15.0, maks=200.0, uc=0.0):
            if any(abs(z - zz) < 20.0 for _x, zz in UKE_M8): z += 25.0
            bag(g, A_u, B, (x, Y_UA, z), "pem_saplama", ad="govde_bag_ust_%s_%d" % (tr, int(-z)))
    # tavan ↔ arka sacın üst dönüşü (FHP-M5)
    for x in (60.0, 250.0, 415.0, 580.0, 770.0):
        bag(g, A_u, P["arka"]["ust"], (x, Y_UA, Z_AI + 13.5), "pem_saplama", ad="govde_bag_ust_arka_%d" % int(x))


# =====================================================================================================================================
# 4 · KAPAKLAR (v3.7 · 2 × 2) · menteşe · bas-aç · robot ağzı · klape cebi
# =====================================================================================================================================
def bas_ac_e(g, K, dikme, kenar, konumlar, a=8.0, plaka=(5.5, 29.5, 20.0)):
    """GO.bas_ac ile aynı (dikme içi bas-aç) · tek fark: karşılık plakası iç tavanın DÜZ alanına kaydırılmış (a = plaka[0] … plaka[1], b ± plaka[2]) —
    E orta dikmesi iki kapağa ortak (her kapak 18,5 biner), bas-aç kapak kenarından 8 içeride → GO'nun ortalı plakası iç tava dönüşüne binerdi"""
    m = dict(GO.BASAC)
    av, bv = K.eksenler(kenar); nv = K.n
    yuz_on = GO._yuz_adi(nv)
    ki = K.ki
    adlar = []; i0 = len(K.basaclar)
    for j, s in enumerate(konumlar):
        i = i0 + j; ad = "%s_basac_%d" % (K.ad, i)
        L = GO._hinge_L(K, kenar, s)
        C, a_c, w_c = GO._dikme_yeri(K, dikme, kenar, L, a)
        h = dikme.b / 2.0; w_on = w_c + h; rg = m["govde_cap"] / 2.0
        if not (a_c - h + dikme.t <= a - rg and a + rg <= a_c + h - dikme.t): raise ValueError("%s: bas-aç gövdesi dikme boşluğuna sığmıyor" % ad)
        uc_len = K.w_ic - w_on - m["bas_h"]
        if uc_len <= 1e-6: raise ValueError("%s: bas-aç ucu yok" % ad)
        dikme.duvar_delik_nokta(yuz_on, L(a, 0.0, w_on), m["delik_cap"], tip="basac_deligi", not_="bas-aç gövdesi (geçme)")
        sh = GO.silindir(L(a, 0.0, w_on - m["govde_boy"]), nv, rg, m["govde_boy"]).fuse(GO.silindir(L(a, 0.0, w_on), nv, m["bas_cap"] / 2.0, m["bas_h"])) \
            .fuse(GO.silindir(L(a, 0.0, w_on + m["bas_h"]), nv, m["uc_cap"] / 2.0, uc_len))
        g.eleman(g.ozel(ad, sh, m["sinif"], "Bas-aç mandalı (push-to-open, geçme gövde Ø%g · O-ring) — orta dikme ön yüzünde Ø%g" % (m["govde_cap"], m["delik_cap"]),
                        "Ø%g × %g · baş Ø%g × %g · strok %g" % (m["govde_cap"], m["govde_boy"], m["bas_cap"], m["bas_h"], m["strok"]), malzeme=m["malzeme"], mal="siyah"), sabit=K)
        dp = g.sac("%s_karsilik_%d" % (K.ad, i), m["karsilik_rol"], mal=K.mal, doner=K)
        pa0, pa1, pb = plaka
        q = [K.uv(kenar, s, aa, bb) for aa, bb in ((pa0, -pb), (pa1, -pb), (pa1, pb), (pa0, pb))]
        us, vs = [x[0] for x in q], [x[1] for x in q]
        u0, u1, v0, v1 = min(us), max(us), min(vs), max(vs)
        dp.taban([(u0, v0), (u1, v0), (u1, v1), (u0, v1)], O=tuple(K.kf(0.0, 0.0, K.w_ic + ki.t)), ex=tuple(K.ex), ey=tuple(K.ey), ad="plaka")
        dp.punta(ki, [tuple(L(aa, bb, K.w_ic + ki.t)) for aa, bb in (((pa0 + pa1) / 2.0 + 6.0, -pb + 7.0), ((pa0 + pa1) / 2.0 + 6.0, pb - 7.0))],
                 not_="karşılık takviyesi → iç tava (kapak kapanmadan önce)")
        K.basaclar.append(dict(ad=ad, kenar=kenar, konum=s, a=a, dikme=dikme.ad))
        adlar.append(ad)
    return adlar


def klape_cebi(g, K, KO, ayak=8.0, bosluk=0.5):
    """sol alt kapak · robot çöpü klapesi: DIŞ tavada 130 × 130 açıklık (klape levhası arkadan 6 bindirir) · İÇ tavada klapenin içe döndüğü cep açıklığı
    (levha + pim kıvrımları + 1 pay) · cep çevresi 4 L kasa çıtası 1,0 (iç tavaya punta, dış tavaya 0,5 + gıda silikonu) · üst çıta yaprağın 0,5 altında biter"""
    x0, x1, y0, y1 = KO["klape"]
    K.D.dikdortgen((x0 + x1) / 2.0, (y0 + y1) / 2.0, x1 - x0, y1 - y0, tip="klape_acikligi", parca="robot çöpü klapesi açıklığı %g × %g (dış tava)" % (x1 - x0, y1 - y0))
    lx0, lx1, ly0, ly1 = KLAPE_ICE["levha"]
    uo0, uo1, vo0, vo1 = lx0 - 1.0, lx1 + 1.0, ly0 - 1.0, 756.0                  # cep: levha + pim kıvrımları (y 753,5) + pay
    K.I.dikdortgen((uo0 + uo1) / 2.0, (vo0 + vo1) / 2.0, uo1 - uo0, vo1 - vo0, tip="klape_cebi", parca="klape cebi (iç tava · klape içe 45° döner)")
    kd, ki = K.kd, K.ki
    ks_t = S.STD.t("kapak_ic"); ks_R = S.STD.R(ks_t); e = ks_R + ks_t
    wk = K.w_ic + ki.t
    hk = (K.w_dis - kd.t - bosluk) - wk
    hk_ust = (KLAPE_ICE["z"][0] + 9.6) - wk                                         # yaprak düz kısmı z 76 → üst çıta 75,5'te biter
    ua, ub = uo0 + ks_t + 0.5, uo1 - ks_t - 0.5
    ui0, ui1, vi0, vi1 = K.ic_kutu; gi = ki.R + ki.t
    assert uo0 - e - ayak >= ui0 + gi + 2.0 and vo1 + e + ayak <= vi1 - gi - 2.0, "klape cebi kasası iç tavaya sığmıyor"
    yanlar = [("sol", [(uo0 - e - ayak, vo0), (uo0 - e, vo0), (uo0 - e, vo1), (uo0 - e - ayak, vo1)], 1, hk),
              ("sag", [(uo1 + e, vo0), (uo1 + e + ayak, vo0), (uo1 + e + ayak, vo1), (uo1 + e, vo1)], 3, hk),
              ("alt", [(ua, vo0 - e - ayak), (ub, vo0 - e - ayak), (ub, vo0 - e), (ua, vo0 - e)], 2, hk),
              ("ust", [(ua, vo1 + e), (ub, vo1 + e), (ub, vo1 + e + ayak), (ua, vo1 + e + ayak)], 0, hk_ust)]
    out = []
    for yan, poly, kenar, h_ in yanlar:
        s = g.sac("%s_klape_cebi_kasa_%s" % (K.ad, yan), "kapak_ic", mal=K.mal, doner=K)
        Pk = s.taban(poly, O=tuple(K.kf(0.0, 0.0, wk)), ex=tuple(K.ex), ey=tuple(K.ey), ad="ayak")
        Pk.flans(kenar, h_, yon=+1, ad="kasa")
        us = [p[0] for p in poly]; vs = [p[1] for p in poly]
        if yan in ("sol", "sag"):
            um = (min(us) + max(us)) / 2.0; nk = [tuple(K.kf(um, y, wk)) for y in GO._dizi(vo0, vo1, 100.0, 20.0)]
        else:
            vm = (min(vs) + max(vs)) / 2.0; nk = [tuple(K.kf(x, vm, wk)) for x in GO._dizi(ua, ub, 100.0, 20.0)]
        s.punta(ki, nk, not_="kasa çıtası ayağı → iç tava (kapak boşluğu tarafı)")
        out.append(s.ad)
    g.not_("%s klape cebi: kasa çıtaları dış tavaya %.1f boşluk (üst çıta yaprağa 0,5) → gıda sınıfı silikon · klape modülü (levha + yaylı menteşe + yaprak) cep içinden "
           "takılır, yaprak dış tavanın arkasına 2 × M4 CD saplama (ISO 13918 · arkadan, dışta iz yok) — ARAYÜZ" % (K.ad, bosluk))
    K.acikliklar.append(dict(ad="klape_cebi", tip="klape", dis=[x0, x1, y0, y1], ic=[uo0, uo1, vo0, vo1], kasa=out))
    # klape yaprağı CD saplamaları (arayüz: yaprakta Ø4,5 delik + M4 somun)
    for xx in (99.0, 159.0):
        p0 = K.kf(xx, 762.5, K.w_dis - kd.t)
        sp = S.pem_saplama("FHP", "M4", 8, tuple(p0), (0, 0, -1.0), ad="arayuz_klape_yapragi_cd_M4_%d" % int(xx), birim=g.birim)[0]
        sp["bom"] = ("CD saplama ISO 13918 PT M4 × 8 A2 (dış tava arka yüzüne kaynak · dışta iz yok)", 1, "M4 × 8", "ISO 13918 · A2", "SATIN ALMA")
        g.arayuz(sp, "E_COP ecop_klape_mentese_yapragi", "yaprakta Ø4,5 delik (y 762,5 · x %g E yereli) + DIN 125 pul + ISO 10511 M4 somun" % xx, "mekanizma (robot çöpü) sahibi")
    return out


def kapaklar(g, KO):
    u0, u1, d0, d1 = KO["u0"], KO["u1"], KO["d0"], KO["d1"]
    ka = dict(w_dis=Z_KAP, w_ic=Z_ON)
    Ks = {}
    for ad, (a0, a1), (v0, v1) in (("onyuz_kapak_E_alt_sol", (u0, d0), KO["alt"]), ("onyuz_kapak_E_alt_sag", (d1, u1), KO["alt"]),
                                     ("onyuz_kapak_E_ust_sol", (u0, d0), KO["ust"]), ("onyuz_kapak_E_ust_sag", (d1, u1), KO["ust"])):
        Ks[ad] = GO.kapak(g, ad, a0, a1, v0, v1, **ka)
    # robot ağzı (sol üst kapakta pencere · sağ kenarı kapak kenarına 20 → kasa ayağı 10)
    ax0, ax1, ay0, ay1 = KO["agiz"]
    GO.aciklik(Ks["onyuz_kapak_E_ust_sol"], "robot_agzi", (ax0 + ax1) / 2.0, (ay0 + ay1) / 2.0, ax1 - ax0, ay1 - ay0, tip="pencere", kasa_ayak=10.0)
    # robot çöpü klapesi (sol alt kapak)
    klape_cebi(g, Ks["onyuz_kapak_E_alt_sol"], KO)
    # menteşeler (dış dikmeler) · bas-açlar (orta dikme)
    for ad, K in Ks.items():
        sol = ad.endswith("_sol")
        kon = MENTESE_ALT if "_alt_" in ad else MENTESE_UST
        GO.gizli_mentese(g, K, P["dsol"] if sol else P["dsag"], "sol" if sol else "sag", kon, olcu=MENTESE_SOL if sol else None)
        bas_ac_e(g, K, P["dorta"], "sag" if sol else "sol", BASAC_ALT if "_alt_" in ad else BASAC_UST, a=BASAC_A)
    g.doner_guncelle()
    P["kapak"] = Ks
    return Ks


# =====================================================================================================================================
# 5 · ŞARJÖR YAN KAPISI (sağ sac açıklığında · 1,5 DÜZ levha) + sağ kılavuz taşıyıcısına CD saplama + gizli menteşe + bas-aç
# =====================================================================================================================================
KAPI_CD = ((240.25, -780.0), (240.25, -455.0), (981.25, -780.0), (981.25, -455.0))   # (y, z) · kılavuz taşıyıcısının üst / alt rayları (mekanizma, kapıyla döner)


def yan_kapi(g):
    """kutu_cad_v14: 'sağ kılavuz (UHMW + taşıyıcı) KAPIDA kalır' — taşıyıcının üst / alt rayları (y 235,5–245 · 978–984,5, x 815,5–828,5) kapı iç yüzüne tam boy
    oturur ve kapının rijitliğini verir. Üst/alt 12'lik dönüş (v14 kurgusu) gerçek büküm R 2,25 ile rayların köşesine biner → kapı DÜZ 1,5 levha; rayına
    4 × ISO 13918 PT M4 × 12 CD saplama (kapı iç yüzüne kaynak, dışta iz yok) + rayda Ø4,5 + DIN 125 + ISO 10511 M4 (ARAYÜZ · mekanizma sahibi)."""
    s = g.sac("sarjor_yan_kapisi", "dis", kabuk=True)
    ya, yb, za, zb = SARJOR_KAPI
    Pn = s.taban([(ya, -zb), (yb, -zb), (yb, -za), (ya, -za)], O=(W, 0, 0), ex=(0, 1, 0), ey=(0, 0, -1), ad="kapi")
    s.notlar.append("düz levha 752 × 406 × 1,5 (büküm yok) · sağ kılavuz taşıyıcısı (mekanizma) rayları rijitlik verir · 4 × CD M4 kapı iç yüzüne")
    P["yan_kapi"] = Pn
    for y, z in KAPI_CD:
        sp = S.pem_saplama("FHP", "M4", 12, (W - 1.5, y, z), (-1.0, 0, 0), ad="arayuz_yan_kapi_cd_M4_%d_%d" % (int(y), int(-z)), birim=g.birim)[0]
        sp["bom"] = ("CD saplama ISO 13918 PT M4 × 12 A2 (kapı iç yüzüne kondansatör deşarjlı kaynak · dışta iz yok)", 1, "M4 × 12", "ISO 13918 · A2", "SATIN ALMA")
        g.arayuz(sp, "E_SARJOR kilavuz_sag_tasiyici", "rayda Ø4,5 delik (y %.2f · z %.0f E yereli) + DIN 125 + ISO 10511 M4 · CD saplama gövde üretiminde kapıya kaynaklanır" % (y, z),
                 "mekanizma (şarjör) sahibi")
    # gizli menteşe (2): sabit gövde arka sacın iç yüzünde (arkadan 2 × ISO 7380 M5 · gövdede M5 diş) · kanat yaprağı kapının iç yüzünde (FHP-M5 ×2) ·
    # kol arka derzden geçer · sanal pivot kapının dış arka köşesi (x 830 · z −820) — ölçüler TEMSİLİ (Sugatsune / EMKA 1036 sınıfı, katalogdan teyit)
    A_a = P["arka"]["arka"]
    for i, yc in enumerate((300.0, 900.0)):
        ad = "sarjor_yan_kapisi_mentese_%d" % i
        gov = kutu(819.0, 828.0, yc - 25.0, yc + 25.0, Z_AI, Z_AI + 7.0)
        for dy in (-15.0, 15.0):
            gov = gov.cut(GO.silindir((823.5, yc + dy, Z_AI - 0.5), (0, 0, 1.0), S.D_NOM["M5"] / 2.0, 6.0))
        g.eleman(g.ozel(ad, gov, "Sugatsune / EMKA 1036 sınıfı (TEMSİLİ)", "Yan kapı gizli menteşesi · SABİT gövde (arka saca) AISI 316", "9 × 50 × 7 · 2 × M5 diş",
                        malzeme="AISI 316", mal="celik", meta=dict(pivot=[W, -820.0], aci=110)))
        for dy, ek in ((-15.0, "a"), (15.0, "b")):
            A_a.delik(823.5, yc + dy, S.STD.delik_iso273("M5"), tip="vida_deligi", parca="yan kapı menteşesi M5 (ISO 273 orta)")
            g.eleman(S.vida("ISO7380", "M5", 6, (823.5, yc + dy, Z_A), (0, 0, 1.0), ad="%s_vida_%s" % (ad, ek), birim=g.birim))
        kan = kutu(826.5, 828.5, yc - 25.0, yc + 25.0, -818.0, -790.0).fuse(kutu(822.0, 826.5, yc - 10.0, yc + 10.0, -821.0, -812.0))
        for dy in (-15.0, 15.0):
            kan = kan.cut(GO.silindir((825.5, yc + dy, -800.0), (1.0, 0, 0), 2.75, 4.0))
        g.eleman(g.ozel(ad + "_kanat", kan, "Sugatsune / EMKA 1036 sınıfı (TEMSİLİ)", "Yan kapı gizli menteşesi · KANAT yaprağı + kol (kapıyla döner)", "2 × 50 × 28 + kol",
                        malzeme="AISI 316", mal="celik", meta=dict(kapakla_doner=True, kapi="sarjor_yan_kapisi")))
        for dy, ek in ((-15.0, "a"), (15.0, "b")):
            bp = S.saplama_baglantisi(Pn, (W, yc + dy, -800.0), (-1.0, 0, 0), 2.0, dis="M5", ad="%s_kanat_bag_%s" % (ad, ek), birim=g.birim)
            for q in bp["parcalar"]: g.eleman(q)
            g.BIRLESIM.append(bp)
    # bas-aç (1 · kapı ortası, ön kenar): ince gövdeli itmeli mandal (Southco 97-10 / EMKA 1084 sınıfı · TEMSİLİ) — gövde yan sacın iç yüzünde (açıklığın 3 önü ↔
    # kapının 6 arkası) · 2 × FHP-M5 (yan sacta, dışta iz yok) gövdedeki Ø5,5 deliklerden · uç kapının iç yüzüne (ön kenarın 4 arkası) basar
    A_g = P["sag"]["yan"]
    ad = "sarjor_yan_kapisi_basac"; yc = (SARJOR_KAPI[0] + SARJOR_KAPI[1]) / 2.0; za = SARJOR_AC[3]
    gov = kutu(819.5, W - 3.0, yc - 20.0, yc + 20.0, za - 9.0, za - 0.5).fuse(kutu(819.5, W - 1.5, yc - 20.0, yc + 20.0, za + 0.5, za + 15.0)) \
        .fuse(kutu(819.5, W - 3.0, yc - 20.0, yc + 20.0, za - 0.5, za + 0.5))
    for dy in (-12.0, 12.0):
        gov = gov.cut(GO.silindir((W - 0.5, yc + dy, za + 8.0), (-1.0, 0, 0), 2.75, 12.0))
    gov = gov.fuse(GO.silindir((W - 3.0, yc, za - 5.0), (1.0, 0, 0), 2.5, 1.5 - 0.02))           # itme ucu (kapı iç yüzüne 0,02)
    g.eleman(g.ozel(ad, gov, "Southco 97-10 / EMKA 1084 sınıfı (TEMSİLİ)", "Yan kapı bas-aç mandalı (push-to-open · uç kapı iç yüzüne) · gövde yan sacın iç yüzünde",
                    "9 × 40 × 24 · strok 6 · 2 × M5", malzeme="AISI 316 / POM", mal="siyah"))
    for dy, ek in ((-12.0, "a"), (12.0, "b")):
        bp = S.saplama_baglantisi(A_g, (W - 1.5, yc + dy, za + 8.0), (-1.0, 0, 0), 9.0, dis="M5", ad="%s_bag_%s" % (ad, ek), birim=g.birim)
        for q in bp["parcalar"]: g.eleman(q)
        g.BIRLESIM.append(bp)
    g.not_("şarjör yan kapısı: açıklığın arka kenarı köşeye uzatıldı (arka dönüş bükümünden 1,75 mm'de kesik üretilemez) · kapı ölçüsü/yeri aynı · arka derz 3 → 8,5 · "
           "kapı düz 1,5 (v14'ün 12'lik dönüşleri kılavuz raylarına binerdi) · 2 gizli menteşe (sabit gövde arka sacta) + 1 bas-aç (yan sacta) · ölçüler TEMSİLİ (katalogdan teyit)")


# =====================================================================================================================================
# 6 · AYAKLAR · BAĞLANTI NOKTALARI (K · B · U_KE · alt şase) · MEKANİZMA BAĞLANTILARI
# =====================================================================================================================================
def ayaklar(g):
    for i, (x, z) in enumerate(AYAK_XZ):
        q = S.ayarli_ayak("M12", (x, 0.0, z), (0, 1.0, 0), 108.0, ise=14.0, D_taban=40.0, ad="ayak_%d" % i, birim=g.birim, kontra=False)
        for p in q: g.eleman(p, mal="celik")
    g.not_("ayaklar: GN 20 sınıfı hijyenik M12 · taban Ø40 (SAPMA: kararlar Ø60 — ön sıra ayakların hemen önünden zemin üstü elektrik kanalı geçiyor, Ø60 kanala "
           "biner; yük ≈ 350 kg / 6 ayak ≈ 60 kg, Ø40 M12 yeterli) · ayak noktaları aynı · moduler alt şasesindeki M12 kaynak somununa (y 108–120) 14 diş · kontra "
           "somun alt şase kapalı profilde takılamaz → kaynak somunu dışa (profil altına) alınmalı (moduler sahibine not)")


def baglanti_noktalari(g):
    A_s, A_u, Tb = P["sol"]["yan"], P["ust"], P["taban"]
    M = []
    # E ← B: taban sol kulağı (3 mm) + DIN 929 M8 kaynak somunu · B içinden ISO 4762 M8 × 20 + DIN 125 (B'nin sağ sacında Ø9)
    ym = Y_TB + 42.0                                                             # 168 · saplamanın 18 üstü
    for z in B_M8_Z:
        ad = "govde_m8_B_%d" % int(-z)
        s, Pk, _b = kulak(g, ad + "_kulagi", A_s, (1.5, Y_TB + 24.0, z), (0, 0, 1.0), (0, -1.0, 0), 24.0, L_kaynak=25.0, gen=40.0, uc=33.75, not_="M8 kulağı ↔ taban")
        Pk.delik(*Pk.yerel((1.5, ym, z))[:2], 9.0, tip="vida_deligi", parca="B ↔ E M8 (DIN 929 kaynak somunu arkada)")
        A_s.delik(ym, z, 9.0, tip="vida_deligi", parca="B ↔ E M8 (ISO 273 orta)")
        g.eleman(S.kaynak_somunu("M8", (4.5, ym, z), (1.0, 0, 0), ad=ad + "_kaynak_somunu", birim=g.birim))
        hp = S.DIN125["M8"][2]
        pu = S.pul("DIN125", "M8", (-1.5 - hp, ym, z), (1.0, 0, 0), ad="arayuz_m8_B_%d_pul" % int(-z), birim=g.birim)
        vd = S.vida("ISO4762", "M8", 16, (-1.5 - hp, ym, z), (1.0, 0, 0), ad="arayuz_m8_B_%d" % int(-z), birim=g.birim)
        g.arayuz(pu, "B_KASA kasa_yan_dis_sac_sag", "B sağ sacında Ø9 (aynı eksen)", "B sahibi")
        g.arayuz(vd, "B_KASA kasa_yan_dis_sac_sag", "ISO 4762 M8 × 16 A2-70 + DIN 125 · B'nin teknik sütunu içinden (soğutma bölmesi servis panelinden)", "B sahibi")
        kd = dict(etiket="B_%d" % int(-z), karsi="B_KASA kasa_yan_dis_sac_sag", karsi_kod="B", cap=9.0, sac_t=1.5, eksen=[1.0, 0, 0],
                  merkez_dunya=[X_E - 1.5, ym, z], merkez_yerel=[-1.5, ym, z], not_="E pasif: DIN 929 M8 kaynak somunu E taban sol kulağında")
        g.KARSI_DELIK.append(kd); M.append(dict(taraf="B", yer="taban sol M8 kulağı (DIN 929)", y=ym, z=z, dunya=[X_E - 1.5, ym, z], karsi_delik=kd))
    # K → E: K'nın perçin somunları · E sol sacında Ø9 (yan_sol'da açıldı) · cıvata E içinden (K'nın arayüz listesinde)
    for y, z in K_M8:
        M.append(dict(taraf="K", yer="E sol sacı Ø9 (K tanımlı)", y=y, z=z, dunya=[X_E + 1.5, y, z], karsi_delik=None))
    # E → U_KE: tavan sacında Ø9 (x 813,5'te yan sacın üst dönüşü de) · ISO 4762 M8 × 25 + DIN 125 E İÇİNDEN · U_KE raf kirişi alt duvarında perçin somun
    for x, z in UKE_M8:
        A_u.delik(x, -z, 9.0, tip="vida_deligi", parca="E → U_KE M8 (ISO 273 orta)")
        y_alt = Y_UA                                                             # tavan sacının alt yüzü
        if x > W - 26.0:                                                         # sağ sacın üst dönüşü de pakette
            Bu = P["sag"]["ust"]; uv = Bu.yerel((x, Y_UA - 0.75, z)); Bu.delik(uv[0], uv[1], 9.0, tip="vida_deligi", parca="E → U_KE M8 (ISO 273 orta)"); y_alt = Y_UA - 1.5
        hp = S.DIN125["M8"][2]
        pu = S.pul("DIN125", "M8", (x, y_alt - hp, z), (0, 1.0, 0), ad="arayuz_m8_UKE_%d_%d_pul" % (int(x), int(-z)), birim=g.birim)
        vd = S.vida("ISO4762", "M8", 25, (x, y_alt - hp, z), (0, 1.0, 0), ad="arayuz_m8_UKE_%d_%d" % (int(x), int(-z)), birim=g.birim)
        kir = "ust_ke_raf_kirisi_2" if x < 600 else "ust_ke_raf_kirisi_3"
        g.arayuz(pu, "U_KE_GOVDE " + kir, "DIN 125 M8 (E içinde, tavan altında)", "")
        g.arayuz(vd, "U_KE_GOVDE " + kir, "U_KE tabanında Ø9 + %s alt duvarında M8 perçin somun (dünya x %.1f z %.0f) · cıvata E içinden" % (kir, x + X_E, z), "U_KE sahibi")
        kd = dict(etiket="UKE_%d_%d" % (int(x), int(-z)), karsi="U_KE_GOVDE ust_ke_taban_sac + " + kir, karsi_kod="U_KE", cap=9.0, sac_t=1.5, eksen=[0, 1.0, 0],
                  merkez_dunya=[x + X_E, Y_UST, z], merkez_yerel=[x, Y_UST, z], not_="U_KE: tabanda Ø9 · raf kirişi alt duvarında M8 perçin somun")
        g.KARSI_DELIK.append(kd); M.append(dict(taraf="U_KE", yer="tavan sacı Ø9 (E aktif)", x=x, z=z, dunya=[x + X_E, Y_UST, z], karsi_delik=kd))
    # taban → moduler alt şase (boyuna 40 × 60 × 3 üst duvarında M8 perçin somun) · ISO 7380 M8 × 16 yukarıdan
    for x, z in SASE_M8:
        Tb.delik(x, -z, 9.0, tip="vida_deligi", parca="taban → alt şase M8 (ISO 273 orta)")
        vd = S.vida("ISO7380", "M8", 16, (x, Y_TB, z), (0, -1.0, 0), ad="arayuz_m8_sase_%d_%d" % (int(x), int(-z)), birim=g.birim)
        g.arayuz(vd, "E_MODULER E_alt_sasi_boyuna", "alt şase boyuna profilinin üst duvarında M8 perçin somun (dünya x %.0f z %.0f) — moduler sahibi" % (x + X_E, z), "moduler")
        M.append(dict(taraf="ALT_SASE", yer="taban Ø9", x=x, z=z, dunya=[x + X_E, Y_ALT, z]))
    g.M8 = M


def mekanizma_baglantilari(g):
    """MEK_TEMAS (q_ref_e: mekanizma parçası ↔ duvar temas yaması, E yereli) → duvarda delik / PEM + ARAYÜZ bağlantı elemanı (karşı delik mekanizma sahibine)
      yan sac / yan kapı / tavan: FHP-M5 gömme saplama (dışta iz yok) → parçada Ø5,5 + DIN 9021 + ISO 10511
      arka sac: ISO 7380 M5 × 6 arkadan → parçada M5 diş (≥ 4 mm et) ya da PEM / perçin somun
      taban (3 mm): PEM SP-M5 (gövde altta, üst yüz düz) → parçada Ø5,5 + ISO 7380 M5 yukarıdan"""
    PANEL = {"sol": P["sol"]["yan"], "sag": P["sag"]["yan"], "kapi": P["yan_kapi"], "ust": P["ust"], "arka": P["arka"]["arka"], "taban": P["taban"]}
    for ti, t in enumerate(MEK_TEMAS):
        duvar, ad, bb = t["duvar"], t["ad"], t["bb"]
        Pn = PANEL[duvar]
        x0, x1, y0, y1, z0, z1 = bb
        if duvar in ("sol", "sag", "kapi"): a0, a1, b0, b1 = y0, y1, z0, z1
        elif duvar in ("ust", "taban"): a0, a1, b0, b1 = x0, x1, z0, z1
        else: a0, a1, b0, b1 = x0, x1, y0, y1
        La, Lb = a1 - a0, b1 - b0
        uzun_a = La >= Lb
        L, Ls = (La, Lb) if uzun_a else (Lb, La)
        if Ls < 11.0:
            ATLANAN.append(dict(ad=ad, duvar=duvar, neden="temas yaması dar (%.1f mm) — parçada flanş / tırnak yok · mekanizma sahibi bağlantı kulağı eklemeli" % Ls, bb=bb)); continue
        n = 1 if L < 60.0 else (2 if L < 260.0 else (3 if L < 500.0 else 4))
        if t.get("n"): n = t["n"]
        uc = max(10.0, min(30.0, L / (2.0 * n)))
        konum = [0.5] if n == 1 else [(uc + (L - 2 * uc) * i / (n - 1)) / L for i in range(n)]
        ok = 0
        for j, f in enumerate(konum):
            am = a0 + f * La if uzun_a else (a0 + a1) / 2.0
            bm = (b0 + b1) / 2.0 if uzun_a else b0 + f * Lb
            if duvar in ("sol", "sag", "kapi"): pw = (1.5 if duvar == "sol" else W - 1.5, am, bm)
            elif duvar == "ust": pw = (am, Y_UA, bm)
            elif duvar == "taban": pw = (am, Y_TB, bm)
            else: pw = (am, bm, Z_AI)
            uv = Pn.yerel(pw)
            et = "%s_%s_%d_%d" % (re.sub(r"[^a-z0-9_]", "", ad.lower())[:40], duvar, ti, j)
            if duvar in ("sol", "sag", "kapi", "ust"):
                if not serbest(Pn, uv[0], uv[1], 2.5, kenar=10.0): ATLANAN.append(dict(ad=ad, duvar=duvar, neden="konum dolu / kenara yakın", nokta=list(pw))); continue
                ic = {"sol": (1.0, 0, 0), "sag": (-1.0, 0, 0), "kapi": (-1.0, 0, 0), "ust": (0, -1.0, 0)}[duvar]
                dis_ = np.asarray(pw, float) - np.asarray(ic) * Pn.sac.t
                sp, c = S.pem_saplama("FHP", "M5", 12, tuple(dis_), ic, ad="arayuz_mek_" + et, birim=g.birim, sac_ad=Pn.sac.ad)
                Pn.delik(uv[0], uv[1], c["delik"], tip="pem_saplama", parca=sp["meta"]["parca"] + " (mekanizma: %s)" % ad, pem_tip="FHP", kenar_min=c["kenar"], min_sac=c["min_sac"])
                g.arayuz(sp, "MEK " + ad, "parçada Ø5,5 delik + DIN 9021 pul + ISO 10511 M5 somun (FHP-M5 × 12 gövde sacında)", "mekanizma sahibi")
            elif duvar == "arka":
                if not serbest(Pn, uv[0], uv[1], 2.75, kenar=8.0): ATLANAN.append(dict(ad=ad, duvar=duvar, neden="konum dolu / kenara yakın", nokta=list(pw))); continue
                Pn.delik(uv[0], uv[1], S.STD.delik_iso273("M5"), tip="vida_deligi", parca="mekanizma %s · ISO 7380 M5 arkadan" % ad)
                vd = S.vida("ISO7380", "M5", 6, (pw[0], pw[1], Z_A), (0, 0, 1.0), ad="arayuz_mek_" + et, birim=g.birim)
                g.arayuz(vd, "MEK " + ad, "parçada M5 dişli delik (≥ 4 mm et) ya da PEM SP-M5 / perçin somun · ISO 7380 M5 × 6 arka sacın dışından", "mekanizma sahibi")
            else:
                # taban 3 mm: PEM FHP gömme saplama, baş taban ALT yüzünde flush (gövde altı 123 düz · montajın 'gövde altı = 123' denetimi) · saplama yukarı
                # mekanizma ayağının deliğinden geçer, üstten DIN 9021 + ISO 10511 (içeriden sökülür)
                dis_m = t.get("dis", "M5")
                if not serbest(Pn, uv[0], uv[1], 3.0 if dis_m == "M6" else 2.5, kenar=10.0): ATLANAN.append(dict(ad=ad, duvar=duvar, neden="konum dolu / kenara yakın", nokta=list(pw))); continue
                sp, c = S.pem_saplama("FHP", dis_m, 15, (pw[0], Y_ALT, pw[2]), (0, 1.0, 0), ad="arayuz_mek_" + et, birim=g.birim, sac_ad=Pn.sac.ad)
                Pn.delik(uv[0], uv[1], c["delik"], tip="pem_saplama", parca=sp["meta"]["parca"] + " (mekanizma: %s · baş altta flush)" % ad, pem_tip="FHP",
                         kenar_min=c["kenar"], min_sac=c["min_sac"])
                g.arayuz(sp, "MEK " + ad, "parçada Ø%.1f delik + DIN 9021 + ISO 10511 %s üstten (FHP-%s × 15 taban sacında, baş altta flush)" % (S.STD.delik_iso273(dis_m), dis_m, dis_m),
                         "mekanizma sahibi")
            ok += 1
        EK.setdefault("mek_baglanti", []).append(dict(ad=ad, duvar=duvar, adet=ok, istenen=n))


def _sase_izi():
    """moduler alt şasesinin (E) üst yüz izleri (x, z) — taban PEM gövdesi bunların üstüne gelmesin · kaba ızgara noktaları"""
    pts = []
    for zc in (-110.0, -770.0):
        for x in np.arange(40.0, 791.0, 10.0): pts.append((float(x), zc))
    for xc in (60.0, 415.0, 770.0):
        for z in np.arange(-770.0, -109.0, 10.0): pts.append((xc, float(z)))
    return pts


# =====================================================================================================================================
# 7 · KUR · MONTAJ SÖZLEŞMESİ
# =====================================================================================================================================
def kur(log=print):
    global G
    if G is not None: return G
    t0 = time.time()
    P.clear(); ATLANAN[:] = []; EK.clear()
    KO = kapak_olcu(); EK["kapak_olcu"] = KO
    g = GO.Govde(BIRIM, SURUM, istasyon="E", cerceve=GO.Cerceve("E", X_E))
    taban(g); yan_sol(g); yan_sag(g); arka(g); tavan(g)
    on_kasa(g, KO); tavan_kirisleri(g)
    kulaklar(g); panel_baglantilari(g)
    kapaklar(g, KO)
    yan_kapi(g)
    ayaklar(g)
    baglanti_noktalari(g)
    mekanizma_baglantilari(g)
    g.doner_guncelle()
    G = g
    log("%s · kuruldu: %d sac · %d profil · %d eleman · %d kaynak · %d birleşim · %d arayüz · %d kapak · atlanan mekanizma bağlantısı %d · %.1f sn"
        % (SURUM, len(g.SAC), len(g.PROF), len(g.ELEMAN), len(g.KAYNAK), len(g.BIRLESIM), len(g.ARAYUZ), len(g.KAPAK), len(ATLANAN), time.time() - t0))
    return g


def govde_parcalari():
    return GO.govde_parcalari(kur())


def kapakla_doner(ad, kapak=None):
    g = kur()
    k = g.DONER.get(ad)
    return k is not None and (kapak is None or k == kapak)


ESLEME = {"onyuz_alt_kanat_sol": "onyuz_kapak_E_alt_sol (+ _ic_tava, _klape_cebi_kasa_*, _mentese_*, _basac_*, _karsilik_*) · v3.7",
          "onyuz_alt_kanat_sag": "onyuz_kapak_E_alt_sag · v3.7", "onyuz_ust_kanat_sol": "onyuz_kapak_E_ust_sol (+ _robot_agzi_kasa_*) · v3.7",
          "onyuz_ust_kanat_sag": "onyuz_kapak_E_ust_sag · v3.7", "onyuz_orta_sabit_panel": "onyuz_kapak_E_ust_sol (robot ağzı penceresi) · v3.7",
          "onyuz_orta_servis_kapagi": "onyuz_kapak_E_ust_sag · v3.7", "onyuz_kayit_orta": ["onyuz_kayit_788_sol", "onyuz_kayit_788_sag"],
          "onyuz_kayit_ust": ["onyuz_kayit_ust_sol", "onyuz_kayit_ust_sag"], "onyuz_alt_dayama_dudagi": "kalktı → yan sacların ön dönüşleri + bas-açlar kapak dayaması",
          **{"onyuz_mentese_%d" % i: "onyuz_kapak_E_*_mentese_* (dikme içi gizli 180°)" for i in range(12)},
          **{"onyuz_basac_%d" % i: "onyuz_kapak_E_*_basac_* (orta dikme içi)" for i in range(5)}}


def vida_araligi_raporu():
    """reçete 3 · panel kenarı boyunca bağlantı aralığı (≤ 200 · köşeden ≤ 80 · kenar başına ≥ 2) — UYARI'lar rapora"""
    g = kur(); out = []
    gr = collections.defaultdict(list)
    for b in g.BIRLESIM:
        m = re.match(r"(govde_bag_(arka_sag_alt|arka_sol|arka_sag|ust_sol|ust_sag|ust_arka))_-?\d+$", b["ad"])
        if m: gr[m.group(1)].append(b["nokta"])
    eks = {"govde_bag_arka_sol": (1, 123.0, Y_UA), "govde_bag_arka_sag": (1, SARJOR_AC[1], Y_UA), "govde_bag_arka_sag_alt": (1, 123.0, SARJOR_AC[0]),
           "govde_bag_ust_sol": (2, Z_A, Z_ON), "govde_bag_ust_sag": (2, Z_A, Z_ON), "govde_bag_ust_arka": (0, 0.0, W)}
    for k, L in sorted(gr.items()):
        i, a0, a1 = eks[k]
        out += GO.vida_araligi_denetle([p[i] for p in L], a0, a1, ad=k)
    for k, (i, a0, a1) in (("govde_kulak_sol_dikme", (1, Y_DSOL0, Y_D1)), ("govde_kulak_sag_dikme", (1, Y_D0, Y_D1)), ("govde_kulak_arka_taban", (0, 0.0, W)),
                           ("govde_kulak_sol_taban", (2, Z_A, Z_ON)), ("govde_kulak_sag_taban", (2, Z_A, Z_ON))):
        L = [b["nokta"][i] for b in g.BIRLESIM if re.match(re.escape(k) + r"_(on|-?\d+)_bag$", b["ad"])]
        if L: out += GO.vida_araligi_denetle(L, a0, a1, ad=k)
    return [m for m in out if m["durum"] != "GEÇTİ"] or "hepsi GEÇTİ"


MONTAJ_SIRASI = [
    "1 · LAZER (N₂, folyo yukarı): acinim/*.json — 1,5 kabuk (sol / sağ yan, arka, tavan, yan kapı) · 3 mm taban + kulaklar + ayak plakaları · 1,0 / 1,5 kapak "
    "tavaları, kasa çıtaları, karşılıklar · 2 mm tapalar · boru lazer: acinim/profil_kesim_listesi.json (30 × 30 × 2 · 40 × 40 × 2) · çapak alma",
    "2 · PEM / SAPLAMA (düz sacta, bükümden ÖNCE): yan saclara FHP-M5 (kulak, mekanizma askıları) · tavana FHP-M5 (kulak, yan / arka üst dönüş, mekanizma) · "
    "tabana FHP-M6 (ayak plakaları, baş ALTTA flush) + FHP-M5 (mekanizma ayakları) · yan saclarin arka dönüşlerine SP-M5 · arka kulaklara SP-M5 · kapak iç "
    "tavalarına SP-M5 (menteşe kanatları) · yan kapıya FHP-M5 (menteşe kanadı) + CD M4 (kılavuz rayı) · sol alt kapak dış tavasına CD M4 (klape yaprağı)",
    "3 · ABKANT (folyolu, rapor 'abkant_sira'): yan saclar (ön → arka → üst dönüş · sağ sacta arka dönüş iki parça) · arka sac üst dönüşü · kapak dış tava 4 "
    "(bindirme köşe) · iç tava 4 · kasa çıtaları · kulaklar 1'er büküm",
    "4 · KAYNAKLI ALT MONTAJLAR (fikstür · kısa atlamalı TIG 141 · ER308LSi): (a) ÖN KASA: sol 30 × 30 / orta 40 × 40 / sağ 30 × 30 dikme + 788 ve üst "
    "kayıtlar (alın + içbükey köşe dikişi) + tapalar + orta / sağ ayak plakaları · (b) tavan kirişleri 40 × 40 × 2 (tapalı) · (c) kulakların kaynak ayakları "
    "(dikme arka yüzü, kiriş yan yüzleri, taban üst yüzü, kayıt arka yüzü) — kulak saplama ayağı panelin iç yüzüne oturacak şekilde fikstürde · (d) taban sol "
    "kenarı: 2 × M8 kulağı + DIN 929 kaynak somunu (B bağlantısı)",
    "5 · TAŞLAMA + SATİNE (dış yüzler: yanlar, kapaklar, yan kapı · hat boyunca 240 kum) → dekapaj + pasivasyon (ASTM A380 / A967)",
    "6 · KAPAKLAR: iç tava + karşılık plakaları + kasa çıtaları (punta) + menteşe kanat yarıları (SP-M5 + ISO 7380) → dış tavaya oturt, dönüşlerden punta "
    "(≈ 150) · robot ağzı penceresi ve klape açıklığı kasa ayağı ↔ dış tava 0,5: gıda sınıfı silikon",
    "7 · GÖVDE YERİNDE: alt şase (moduler, 6 ayak M12) teraziye → taban sacı (alt şaseye 4 × M8 arayüz) → mekanizma taban ayakları (FHP saplamalar) → "
    "ön kasa (ayak plakaları FHP-M6) → yan saclar (kulak saplamaları: pul + fiberli somun içeriden) → tavan kirişleri yan kulaklara → tavan (kulak saplamaları + "
    "yan üst dönüşler) → mekanizma askıları tavana / yanlara → arka sac EN SON (ISO 7380 dışarıdan; pano + mekanizma arka bağlantıları) → yan kapı (menteşe "
    "kanatları kaldır-tak) → ön kapaklar (gizli menteşe kaldır-tak · bas-aç ayarı · derz 3 kontrolü)",
    "8 · SAHA: K ↔ E 3 × M8 (E içinden, K perçin somunlarına) · B ↔ E 2 × M8 (B teknik sütunundan, E DIN 929'una) · E → U_KE 4 × M8 (E içinden, U_KE raf "
    "kirişi perçin somunlarına) · Harting soketi tavan kesiğine · folyo sökümü"]



def uygula_kc(KC, rapor=None):
    """montaj: KC.modul() + v3.6 plint düşürme SONRASI (h3_kapak_v1.bolge_E YERİNE) · eski 42 gövde parçası çıkar, üretim sacı gövdesi girer (E yereli) · idempotent"""
    return GO.uygula(KC.PARCALAR, govde_parcalari(), [a for a in ESKI_GOVDE if a != "onyuz_plint"], "onyuz_kapak_E_alt_sol_ic_tava", onekler=GOVDE_ONEK,
                     rapor=rapor, etiket="E")


def dunya_listesi(L):
    return GO.dunya_listesi(L, GO.Cerceve("E", X_E))


def kapak_dunya(L, kapak):
    """montaj v3.7 süpürmesi için: 'kapak' ile dönen bütün E parçalarının DÜNYA bileşiği (dış + iç tava, kasa çıtaları, karşılıklar, menteşe kanatları, PEM, kaynak)"""
    g = kur()
    return GO.kapak_dunya(L, GO.Cerceve("E", X_E), lambda a: g.DONER.get(a) == kapak)


if __name__ == "__main__":
    sys.path.insert(0, os.environ.get("E_SAC_CIKTI") or os.path.abspath(os.path.join(H3, "..", "..", "..", "..", "sac_e")))
    import e_sac_denetim_v1 as DEN
    DEN.calistir()
    sys.stdout.flush(); os._exit(0)
