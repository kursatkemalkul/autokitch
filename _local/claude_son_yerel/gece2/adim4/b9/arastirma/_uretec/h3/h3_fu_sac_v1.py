# -*- coding: utf-8 -*-
"""h3_fu_sac_v1 — FIRIN ÜSTÜ KABİN (F_UST) + DAVLUMBAZ SAC KUTUSU + ÜST DEPOLAR (U_A · U_F · U_KE) · ÜRETİM SACI GÖVDESİ v1
(2 Eki 2026 · Claude · YEREL · istasyon ajanı · TASLAK, montaja bağlı DEĞİL — bağlama: <scratchpad>/sac_fu/yama_fu_sac.py)

Kemal: "gövdede tam çalışma; büküm gerçek; sanayi mutfaklarında nasıl kuruluyorsa öyle; nereden bükülür, vida nereye atılır, boşluk nerede açılır;
vidasına kadar ama mantıklı; sanayi tipi mutfakçı 3B'den direkt üretsin." · pafta YOK, önce 3B (açınım JSON'ları ayrıca).
KAYNAKLAR: h3_sac_v1 (S) · h3_govde_ortak_v1 (GO, reçete) · sac_kararlar_v1 > sac_standart_v1 · mevcut gövde: firin_ust_kabin_cad_v1 (FU0, h3_firin_ust_v1 v3.7) +
           h3_ust_depo_v2 (UD v3.7) · v3.7 kapak düzeni h3_kapak_v1 (KARAR F_KAPAK 'duser', F üstü 2 kanat 1308–2197) · elektrik delik hedefleri h3/_elk.
KOORDİNAT: DÜNYA (FU ve UD montajda dünya koordinatlı: _dis_birim). x hat boyunca · y yukarı · z koridora (ön düzlem +79, gövde ön düzlemi +59, arka −830).

KURGU (atölye mantığı · mevcut kurgu korunur: KENDİNDEN TAŞIYICI SAC KUTU + KAYNAKLI ÖN ÇERÇEVE)
  F_UST (x 2500–4000 · 788/1306–1862): 1 · ÖN ÇERÇEVE = KAYNAKLI ALT MONTAJ 304 kare boru 30 × 30 × 2 (SAPMA: kararlar 40 × 40 — mevcut kayıt kotları / pizza
      yığını / kompresör 2,5 mm payı ve gizli menteşe kol boyu 30'luk profile göre; 40'lık profil kapak iç düzlemine değer): ön alt kayıt (MENTEŞE TAŞIYICI, y 1310–1340)
      + ön üst kayıt (1830,5–1860,5) + orta dikme (x 3326–3356) + tavan kirişi (z boyunca) + 2 boyuna tavan kirişi (pizza yığınının arkasında z −474…−444) ·
      alt kayıt 3 × 5 mm lama takozla fırın üst sacına basar. 2 · SÖKÜLEBİLİR / CIVATALI SAC KUTU: yan saclar L (üst bölüm + fırın arkasında şerit 788'e iner) 1,5 ·
      ön dönüş 16,5 + arka dönüş 22 + şerit ön dönüşü + ayak dönüşü (B tavanına basar) · üst sac 1,5 (ön + arka aşağı dönüş, U_F tabanı + yükü bunun üstünde) ·
      arka sac 1,5 tek parça 1500 × 1074 (ayak dönüşü · iki lazer yarık panjur + iç su kırıcı perde · 4 rakor + elektrik delikleri) · yanlar çerçeveye 3 mm L kulak +
      PEM FHP-M5 (yan yüzler komşu sacına dayanır, dışta iz yok) · arka sac ISO 7380 M5 + PEM SP-M5 (dışarıdan sökülür, servis).
  DAVLUMBAZ SAC KUTUSU (x 2505–3995 · y 1315–1790 · z −827…−440): KAYNAKLI SIZDIRMAZ KUTU (EN 16282 yağ kanalı mantığı) = 2 adet tek bükümlü L (alt + ön · üst + arka) +
      2 tava uç kapağı, iç köşelerden sürekli TIG · 2 askı köşebendi (3 mm L, yan saclara FHP-M6) · atış kanalı 300 × 200 = 2 L + 2 dikiş · üst sacın altında silikon conta.
      İç donanım (dikey kanal · fan · filtreler · konsollar · filtre çerçevesi) v3.7'deki gibi KALIR (cihaz).
  ÖN KAPAK (v3.7 Kemal çizimi · KARAR 'duser'): 2 DÜŞER KANAT 2500–3248,5 / 3251,5–4000 × 1308–2197 (U_F önü dahil) · ÇİFT CİDAR (dış tava 1,5 dönüş 20 bindirme + TIG ·
      iç tava 1,0 dönüş 15, punta) · kanat başına 2 gizli 180° kaldır-çıkar menteşe ön alt kayıt İÇİNDE (sanal pivot alt ön kenar y 1308 · z 79) · 2 bas-aç U_F ön üst kaydı
      İÇİNDE · 1 çekme tipi gazlı yay (dış yanda, bilyalı mafsal) · iki cidarda hizalı lazer yarık havalandırma (kompresör + davlumbaz besleme havası) · KULP YOK.
  U_A / U_F / U_KE (y 1862–2200): KENDİNDEN TAŞIYICI SAC KUTU (3 ayrı ürün): taban TEPSİ 1,5 (yan + arka yukarı dönüş) · yanlar tam boy (taban kenarını örter) ·
      üst sac (arka aşağı dönüş, ön kenar ön üst kayda oturur) · arka sac tek parça · ön alt + ön üst kayıt 30 × 30 × 2 + tavan kirişleri (kaynaklı) ·
      U_F kutu rafı + U_KE içecek rafı: 1,5 tepsi (ön + arka aşağı dönüş) taşıyıcı profillere delik kaynağıyla · U_A tabanı A ile tek hacim (632 × 803 açıklık) ·
      U_A ve U_KE'nin önü A / K / E kapaklarıyla kapanır (v3.7), U_F'nin önü F kanatlarıyla.
  BAĞLANTI: F↔K: K pilotunun 4 M8 perçin somununa sağ yan sacta Ø9 · F↔TOPPING, U_A↔TOPPING, U_F↔TOPPING: bizim taraftan ISO 4762 M8 (F / U içinden, kapak açıkken
      erişilir) → TOPPING tarafında M8 diş (karşı liste) · U_F→F_UST: F_UST içinden yukarı M8 → U_F tabanına kaynaklı DIN 929 somun · U_KE→K / E: K / E içinden yukarı M8 →
      U_KE tabanında DIN 929 kaynak somunu (K / E üst sacında yalnız Ø9) · U_A→A: U_A içinden aşağı M8 → A üst kuşağında perçin somun (karşı liste) · U_F↔U_KE: M8 cıvata + somun ·
      ana pano rayları: U_F tabanında 2 × ISO 13918 M6 kaynak saplaması rayların arkada taşan dilinde (rayın kalanı pano gövdesinin altında; çift sac: alttan somun olmaz).
ARAYÜZLER DEĞİŞMEZ: dış ölçüler · ön düzlem +79 / gövde +59 · arka −830 · 788 / 1305 / 1862 / 2200 · açıklıklar (atış ağzı, baca, U_A 632 × 803, rakorlar, elektrik
  geçişleri) · cihaz / mekanizma yerleri (fırın, raf, kompresör, yağ tenekesi, pizza yığınları, ana pano, fanlar, baca, koliler, davlumbaz içi).
Çalıştır (öz denetim + çıktılar <scratchpad>/sac_fu): python -u h3_fu_sac_v1.py"""
import math, os, sys, json, time, re, collections
H3 = os.path.dirname(os.path.abspath(__file__)); _U = os.path.dirname(H3)
for _p in (_U, H3):
    if _p not in sys.path: sys.path.insert(0, _p)
import numpy as np
import cadquery as cq
import h3_sac_v1 as S
import h3_govde_ortak_v1 as GO

SURUM = "h3_fu_sac_v1"
V = cq.Vector
T = 1.5
# ================================================================ ARAYÜZ (dünya · değişmez) ================================================================
X_F = (2500.0, 4000.0)
X_UA, X_UF, X_UKE = (736.0, 1436.0), (2500.0, 4000.0), (4000.0, 5230.0)
Y_DOLAP, Y_FIRIN, Y_IST, Y_UST = 788.0, 1305.0, 1862.0, 2200.0
Z_ON, Z_KAPAK, Z_ARKA, Z_ARKA_IC = 59.0, 79.0, -830.0, -828.5
Z_FARKA = -651.0                                           # fırın gövdesi arka yüzü
G15 = 2.25 + 1.5                                           # R + t (1,5 sac · R = 1,5t)
# ---- F_UST
F_UST_ALT = 1306.0                                         # yan sac üst bölüm alt kenarı (fırın üstü 1305 + 1)
F_SERIT_ON = -656.0                                        # şerit ön kenarı (büküm teğeti) → ön dönüş dış yüzü −652,25 (fırın arkası −651)
F_TAVAN = (1860.5, 1862.0)
ON_DONUS, ARKA_DONUS, AYAK_DONUS = 16.5, 22.0, 20.0
SERIT_FL_Y0 = 1040.0                                       # şerit ön dönüşü bu kotun üstünde (altında fırın arkasındaki CEE prizi + sinyal kutusu)
AR_PAY = ARKA_DONUS + 1.0 - T - G15                        # taban arka dönüşü yan sacların arka dönüşünden 1 mm uzak (17,75)
PB, PT = 30.0, 2.0                                         # 30 × 30 × 2 (SAPMA · rapor) · dış R 4
KAYIT_Y = (1310.0, 1340.0)                                 # ön alt kayıt (menteşe taşıyıcı) · v3.6'da 1308–1338 → +2 (menteşe penceresi profilin düz yüzüne sığsın)
UST_KAYIT_Y = (1830.5, 1860.5)
KAYIT_Z = (27.0, 57.0)
KIRIS_X = (3326.0, 3356.0)                                 # h3_hesap_v1.KIRIS_X (pizza ≤ 3324 · kompresör ≥ 3359)
BOYUNA_Z = (-474.0, -444.0)                                # boyuna tavan kirişi (pizza z ≥ −424 · atış kanalı z ≤ −520 arası)
TAKOZ_X = (2875.0, 3250.0, 3625.0)
# ---- davlumbaz
DAV = (2525.0, 3975.0, 1315.0, 1790.0, -827.0, -440.0)        # v3.7 2505–3995 → uçlardan 20 kısa: yan sac arka dönüşündeki M5 somun + SW8 lokma payı (iç donanım 2952–3955 değişmez)
ATIS = (2950.0, 3250.0, -720.0, -520.0)
EMIS_X, EMIS_Y = (3390.0, 3590.0, 3790.0), (1520.0, 1620.0, 1720.0)            # 9 emiş yarığı 160 × 10 (sol alt köşeleri, v3.7 ile aynı)
# ---- kapak
KANAT_X = ((2500.0, 3248.5), (3251.5, 4000.0))
KAPAK_Y = (1308.0, 2197.0)
MENTESE_DX = 130.0
BASAC_DX = 95.0
BASAC_A = 17.0                                              # bas-aç ekseni kapak üst kenarından (y 2180 · U_F üst kaydı merkezi 2183,5 → 3,5 aşağı) · karşılık plakası 2168–2192 iç tavanın düz bölgesinde
YARIK_BANT_Y = (1420.0, 1785.0)                             # kanat havalandırma bantları (2 × 3 sıra × 9 · 60 × 5)
YAY = dict(A=(1750.0, -5.0), B=(1458.0, 40.0), x_sol=2529.0)   # çekme gazlı yay: sabit mafsal (y, z) · kapak mafsalı (y, z) kapalı · eksen x (sağ: ayna 3250)
# ---- U
U_TABAN = (1862.0, 1863.5)
U_TAVAN = (2198.5, 2200.0)
U_ALT_KAYIT_Y, U_UST_KAYIT_Y = (1863.5, 1893.5), (2168.5, 2198.5)
RAF_Y = (1893.5, 1895.0)
U_KIRIS = dict(A=(857.5,), F=(2800.0, 3500.0), KE=(4400.0, 4815.0))
UF_RAF = dict(x=(2515.0, 3329.0), z=(-430.0, 25.0), kiris=(2530.0, 2922.0, 3314.0))
UKE_RAF = dict(x=(4002.0, 5228.0), z=(-826.0, 25.0), kiris=(4040.0, 4412.5, 4817.5, 5190.0))     # uç taşıyıcılar 13 içeri (yan kulak saplaması + somun)
UA_ACIKLIK = (770.0, 1402.0, -796.0, 7.0)                  # v3.4 · A + U_A tek hacim
UA_ARKA_X1 = 1225.0                                         # U_A taban arka dönüşü bu x'te biter (ELK A_istasyon_kutusu 1240–1400)
BACA = (2950.0, 3250.0, -720.0, -520.0)
UF_FAN = [("emis_0", 3660.0, 1930.0), ("emis_1", 3860.0, 1930.0), ("atis_0", 2640.0, 2075.0), ("atis_1", 2820.0, 2075.0)]
PANO_RAY = [(3538.0, -332.5), (3958.0, -332.5)]           # ana pano taban rayının pano gövdesinin arkasında taşan 25 mm dili (h3_ana_pano_v1 AYAK z −345…−320)
# ---- komşu bağlantıları (dünya)
K_M8 = [(1000.0, -800.0), (1825.0, -800.0), (1700.0, 42.0), (877.0, -720.0)]          # K pilotu (h3_k_sac_v1 M8_F) · f_ust_yan_sag Ø9
TOP_M8_F = [(1000.0, -740.0), (1825.0, -790.0), (1700.0, 42.0), (1450.0, 0.0)]       # F_UST ↔ TOPPING (sol yan)
TOP_M8_UA = [(1950.0, -150.0), (2100.0, -650.0)]                                     # U_A sağ yan ↔ TOPPING
TOP_M8_UF = [(1950.0, -150.0), (2100.0, -650.0)]                                     # U_F sol yan ↔ TOPPING
UF_UKE_M8 = [(2100.0, -150.0), (2100.0, -650.0)]                                     # U_F sağ ↔ U_KE sol (ikisi de bizim)
UF_F_M8 = [(2670.0, 3.5), (3110.0, 3.5), (3570.0, 3.5), (3790.0, 3.5), (2720.0, -700.0), (3420.0, -700.0), (3800.0, -700.0)]   # U_F → F_UST (DIN 929)
UKE_K_M8 = [(4200.0, 0.0), (4200.0, -400.0)]                                         # U_KE → K
UKE_E_M8 = [(4650.0, 0.0), (5000.0, 0.0), (4650.0, -400.0)]                          # U_KE → E
UA_A_M8 = [(753.0, -320.0), (753.0, -700.0), (1419.0, -320.0), (1419.0, -700.0)]     # U_A → A (A üst kuşağında perçin somun)

ELK_DELIK = os.path.abspath(os.path.join(H3, "..", "..", "..", "..", "sac_fu", "_ref", "elk_delik_fu.json"))
ELK_CAP = {("f_ust_arka_sac", "v3.7b F kutusu bina 230 V girişi"): 20.5}     # M20 rakor gövdesi Ø20 → Ø20,5 (ELK kesicisi Ø18,5)
KALINLIK_IZGARA = ("ust_a_taban_sac",)                     # büyük açıklıklı yüz (h3_sac_v1 örnek noktaları boşluğa düşer)
FU_BIRIMLER = {"F_UST_KABIN": "FU", "F_UST_KAPAK": "FU", "F_DAVLUMBAZ": "FU", "U_A_GOVDE": "UD", "U_F_GOVDE": "UD", "U_KE_GOVDE": "UD"}
S._RENK.update({"profil": ((0.70, 0.73, 0.77, 1.0), 0.85, 0.30), "mekanizma": ((0.42, 0.46, 0.52, 1.0), 0.4, 0.5), "arayuz": ((0.90, 0.22, 0.15, 1.0), 0.3, 0.5),
                "kapak": ((0.70, 0.82, 0.95, 1.0), 0.2, 0.25), "komsu": ((0.55, 0.60, 0.50, 1.0), 0.2, 0.6)})

# ================================================================ ESKİ GÖVDE (montaj listelerinden çıkar) ================================================================
ESKI_FU = (["f_ust_yan_sol", "f_ust_yan_sag", "onyuz_f_ust_gazli_yay_braketi_sol", "onyuz_f_ust_gazli_yay_braketi_sag", "f_ust_tavan_sac", "f_ust_tavan_kirisi",
            "f_ust_arka_sac", "f_ust_panjur_lamelleri_0", "f_ust_panjur_lamelleri_1", "onyuz_f_ust_kayit", "onyuz_f_ust_kayit_takozu_0", "onyuz_f_ust_kayit_takozu_1",
            "onyuz_f_ust_kayit_takozu_2", "onyuz_f_ust_dikme_0", "onyuz_f_ust_bas_ac_sol", "onyuz_f_ust_bas_ac_sag",
            "f_davlumbaz_kutusu", "f_davlumbaz_atis_kanali", "f_davlumbaz_askisi_sol", "f_davlumbaz_askisi_sag"] +
           ["onyuz_f_ust_kapak_%s%s" % (y, e) for y in ("sol", "sag") for e in ("", "_omega_0", "_omega_1", "_burulma_kutusu", "_yay_pimi", "_tipon_plakasi")] +
           ["onyuz_f_ust_mentese_%s_%s_%d" % (t, y, i) for t in ("sabit", "hareketli") for y in ("sol", "sag") for i in (0, 1)] +
           ["onyuz_f_ust_gazli_yay_%s_%s" % (y, e) for y in ("sol", "sag") for e in ("govde", "mil", "goz_a", "goz_b")])
ESKI_UD = []
for _k, _kap in (("a", ("tek",)), ("f", ("sol", "sag")), ("ke", ("sol", "sag"))):
    ESKI_UD += ["ust_%s_taban_sac" % _k, "ust_%s_yan_sol" % _k, "ust_%s_yan_sag" % _k, "ust_%s_arka_sac" % _k, "ust_%s_tavan_sac" % _k,
                "onyuz_ust_%s_alt_kayit" % _k, "onyuz_ust_%s_ust_kayit" % _k]
    ESKI_UD += ["ust_%s_tavan_kirisi_%d" % (_k, i) for i in range(1 if _k == "a" else 2)]
    for _t in _kap:
        ESKI_UD += ["onyuz_ust_%s_kapak_%s" % (_k, _t), "onyuz_ust_%s_kapak_%s_alt_kutusu" % (_k, _t)]
        ESKI_UD += ["onyuz_ust_%s_mentese_%s_%s_%d" % (_k, m, _t, i) for m in ("sabit", "hareketli") for i in (0, 1)]
    if _k == "a":
        ESKI_UD += ["onyuz_ust_a_bas_ac_tek_sol", "onyuz_ust_a_bas_ac_tek_sag", "onyuz_ust_a_kapak_tek_tipon_plakasi_sol", "onyuz_ust_a_kapak_tek_tipon_plakasi_sag"]
    else:
        ESKI_UD += ["onyuz_ust_%s_bas_ac_sol_sol" % _k, "onyuz_ust_%s_bas_ac_sag_sag" % _k, "onyuz_ust_%s_kapak_sol_tipon_plakasi_sol" % _k,
                    "onyuz_ust_%s_kapak_sag_tipon_plakasi_sag" % _k]
ESKI_UD += ["ust_f_raf_kirisi_%d" % i for i in range(3)] + ["ust_f_kutu_rafi"] + ["ust_ke_raf_kirisi_%d" % i for i in range(4)] + ["ust_ke_icecek_rafi"]
ONEK_FU = ("f_ust_", "onyuz_f_ust_", "f_davlumbaz_", "govde_")
ONEK_UD = ("ust_a_", "ust_f_", "ust_ke_", "onyuz_ust_", "govde_")
ISARET_FU, ISARET_UD = "onyuz_f_ust_kapak_sol_ic_tava", "onyuz_ust_f_ust_kayit_tapa_sol"


def kutu(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), V(min(x0, x1), min(y0, y1), min(z0, z1)))


def silindir(p0, eksen, r, L):
    e = np.asarray(eksen, float); e = e / np.linalg.norm(e)
    return cq.Solid.makeCylinder(float(r), float(L), V(*map(float, p0)), V(*map(float, e)))


# =====================================================================================================================================
# 0 · KAYIT DEFTERİ (tek GO.Govde · parça başına birim + modül)
# =====================================================================================================================================
class G:
    g = None
    BIRIM, MODUL = {}, {}
    KAPAK = {}
    P = {}                                                  # paneller / profiller sözlüğü
    M8 = []                                                 # komşu bağlantı kayıtları
    ELK = []                                                # elektrik deliği uygulama kayıtları
    HESAP = {}
    kuruldu = False
    _bolum = None


def _adlar(g):
    s = set()
    for x in g.SAC: s.update(GO._sac_parca_adlari(x))
    s.update(g.PROF.keys()); s.update(p["ad"] for p in g.ELEMAN); s.update(p["ad"] for p in g.KAYNAK)
    return s


class bolum:
    """bu blokta doğan parçalar → birim (+ modül FU / UD)"""
    def __init__(self, birim):
        self.birim = birim

    def __enter__(self):
        self.once = _adlar(G.g); G._bolum = self.birim
        return self

    def __exit__(self, *a):
        for ad in _adlar(G.g) - self.once:
            if ad not in G.BIRIM: G.BIRIM[ad] = self.birim; G.MODUL[ad] = FU_BIRIMLER[self.birim]
        G._bolum = None
        return False


def birim_bul(ad):
    if ad in G.BIRIM: return G.BIRIM[ad]
    for s in G.g.SAC:                                        # köşe kaynakları sonradan doğar (kose() bolum içinde çağrılır)
        if ad in GO._sac_parca_adlari(s): return G.BIRIM.get(s.ad)
    return None


def pan_delik(P, p, cap, tip="delik", **m):
    uv = P.yerel(np.asarray(p, float)); return P.delik(uv[0], uv[1], cap, tip=tip, **m)


def pan_dikd(P, p, boy, en, r=0.0, tip="kesik", aci=0.0, dfm=True, **m):
    uv = P.yerel(np.asarray(p, float)); return P.dikdortgen(uv[0], uv[1], boy, en, aci=aci, r=r, tip=tip, dfm=dfm, **m)


def pan_oblong(P, p, boy, en, aci=0.0, tip="yarik", **m):
    uv = P.yerel(np.asarray(p, float)); return P.oblong(uv[0], uv[1], boy, en, aci, tip=tip, **m)


def bag(A, B, nokta, tip, dis="M5", ad="govde_bag", **k):
    """S.vidali_birlesim + kayıt (elemanlar GO defterine)"""
    g = G.g
    b = S.vidali_birlesim(A, B, tuple(map(float, nokta)), tip, dis=dis, ad=ad, birim=g.birim, **k)
    for q in b["parcalar"]: g.eleman(q)
    g.BIRLESIM.append(b)
    return b


def kulak_arka(ad, A, stud, u, v, v_cerceve, L_kaynak=25.0, gen=25.0, uc=9.75):
    """ARKA sacına L kulak: kulak iskelete kaynaklı · arka sacta PEM FHP-M5 (baş dış yüzle aynı, arkada vida başı yok) · kulakta Ø5,5 · pul + somun içeriden"""
    g = G.g
    s = g.sac(ad, "braket")
    stud = np.asarray(stud, float); u, v = np.asarray(u, float), np.asarray(v, float)
    t, R = s.t, s.R
    vb = v_cerceve - (R + t)
    n = np.cross(u, v)
    P = s.taban([(-gen / 2, -uc), (gen / 2, -uc), (gen / 2, vb), (-gen / 2, vb)], O=tuple(stud), ex=tuple(u), ey=tuple(v), ad="vida_ayagi")
    P.flans(2, L_kaynak, yon=+1, ad="kaynak_ayagi")
    for sg in (+1, -1):
        p0 = stud + u * sg * gen / 2.0 + v * v_cerceve + n * (R + t)
        p1 = stud + u * sg * gen / 2.0 + v * v_cerceve + n * L_kaynak
        g.kaynak(S.kaynak_dikisi(p0, p1, u * sg, -v, min(t, 3.0), ad=ad + "_kaynak_%s" % ("a" if sg > 0 else "b"), birim=g.birim, taraf="dis (köşe)", not_="kulak ↔ iskelet"))
    bag(A, P, stud, "pem_saplama", ad=ad + "_bag")
    g.KULAK.append(s)
    return s, P


def kacir(konum, engel, pay):
    """bağlantı konumlarını engel merkezlerinden (kiriş vb.) en az 'pay' uzağa iter (yakın tarafa)"""
    out = []
    for x in konum:
        for e in engel:
            if abs(x - e) < pay: x = e + (pay if x >= e else -pay)
        out.append(x)
    return out


def kulak(ad, A, stud, u, v, v_cerceve, **k):
    return GO.kulak(G.g, ad, A, stud, u, v, v_cerceve, **k)


def profil(ad, eksen, a0, a1, c, not_=""):
    return G.g.profil(ad, eksen, a0, a1, c, b=PB, t=PT, not_=not_)


def uc_kaynak(ad, nokta, yon, yuzler, b=PB):
    G.g.kaynak(GO.uc_kaynaklari(ad, nokta, yon, yuzler, b=b, a=PT, Ro=2 * PT, birim=G.g.birim))


def tapa(pr, uc):
    return GO.dikme_tapasi(G.g, pr, uc=uc, ad="%s_tapa_%s" % (pr.ad, uc))


def dikis(ad, p0, p1, u1, u2, a=1.5, not_=""):
    G.g.kaynak(S.kaynak_dikisi(p0, p1, u1, u2, a, ad=ad, birim=G.g.birim, taraf="iç (köşe)", not_=not_))


# =====================================================================================================================================
# 1 · F_UST · ÖN ÇERÇEVE (kaynaklı alt montaj)
# =====================================================================================================================================
def f_cerceve():
    P = G.P
    kc, uc_, zc = (KAYIT_Y[0] + KAYIT_Y[1]) / 2.0, (UST_KAYIT_Y[0] + UST_KAYIT_Y[1]) / 2.0, (KAYIT_Z[0] + KAYIT_Z[1]) / 2.0
    xk = (KIRIS_X[0] + KIRIS_X[1]) / 2.0; zb = (BOYUNA_Z[0] + BOYUNA_Z[1]) / 2.0
    xa_, xb_ = X_F[0] + G15 + 0.5 + PT, X_F[1] - G15 - 0.5 - PT                  # uç tapaları (2 mm) yan sacın ön büküm yayından (R + t) 0,5 içeride
    P["kayit"] = profil("onyuz_f_ust_kayit", "x", xa_, xb_, (kc, zc), "ön alt kayıt · düşer kapak menteşe taşıyıcı (gizli menteşe gövdeleri içinde)")
    P["ust_kayit"] = profil("onyuz_f_ust_ust_kayit", "x", xa_, xb_, (uc_, zc), "ön üst kayıt · üst sacın ön kenarı")
    P["dikme"] = profil("onyuz_f_ust_dikme_0", "y", KAYIT_Y[1], UST_KAYIT_Y[0], (xk, zc), "orta dikme (pizza ≤ 3324 · kompresör ≥ 3359)")
    P["kiris"] = profil("f_ust_tavan_kirisi", "z", Z_ARKA_IC + G15 + 0.5 + PT, KAYIT_Z[0], (xk, uc_), "tavan kirişi · U_F yükü → ön üst kayıt + arka sac")
    P["boy_sol"] = profil("f_ust_tavan_boyuna_kirisi_sol", "x", xa_, KIRIS_X[0], (uc_, zb), "boyuna tavan kirişi (pizza yığınının arkası)")
    P["boy_sag"] = profil("f_ust_tavan_boyuna_kirisi_sag", "x", KIRIS_X[1], xb_, (uc_, zb), "boyuna tavan kirişi (kompresörün arkası)")
    # birleşim bölgeleri (profil DFM: kesik bu bölgelerde olmaz)
    P["kayit"].kaynak_bolgesi("+y", KIRIS_X[0], KIRIS_X[1]); P["ust_kayit"].kaynak_bolgesi("-y", KIRIS_X[0], KIRIS_X[1])
    P["ust_kayit"].kaynak_bolgesi("-z", KIRIS_X[0], KIRIS_X[1]); P["kiris"].kaynak_bolgesi("-x", BOYUNA_Z[0], BOYUNA_Z[1]); P["kiris"].kaynak_bolgesi("+x", BOYUNA_Z[0], BOYUNA_Z[1])
    # uç kaynakları: dikme ↔ kayıtlar (alın + yanlarda köşe) · kiriş ↔ üst kayıt arka yüzü · boyuna ↔ kiriş yanları
    uc_kaynak("onyuz_f_ust_dikme_0_kaynak_alt", (xk, KAYIT_Y[1], zc), (0, 1.0, 0), [(1.0, 0, 0), (-1.0, 0, 0)])
    uc_kaynak("onyuz_f_ust_dikme_0_kaynak_ust", (xk, UST_KAYIT_Y[0], zc), (0, -1.0, 0), [(1.0, 0, 0), (-1.0, 0, 0)])
    uc_kaynak("f_ust_tavan_kirisi_kaynak_on", (xk, uc_, KAYIT_Z[0]), (0, 0, -1.0), [(1.0, 0, 0), (-1.0, 0, 0), (0, -1.0, 0)])
    uc_kaynak("f_ust_tavan_boyuna_kirisi_sol_kaynak", (KIRIS_X[0], uc_, zb), (-1.0, 0, 0), [(0, -1.0, 0), (0, 0, 1.0), (0, 0, -1.0)])
    uc_kaynak("f_ust_tavan_boyuna_kirisi_sag_kaynak", (KIRIS_X[1], uc_, zb), (1.0, 0, 0), [(0, -1.0, 0), (0, 0, 1.0), (0, 0, -1.0)])
    for pr in (P["kayit"], P["ust_kayit"], P["boy_sol"], P["boy_sag"]):
        for uc in ("alt", "ust"):
            if pr is P["boy_sol"] and uc == "ust": continue
            if pr is P["boy_sag"] and uc == "alt": continue
            tapa(pr, uc)
    tapa(P["kiris"], "alt")
    G.g.not_("F_UST ön çerçeve: profil uçları 2 mm tapa (kapalı profil, TIG çevre taşlanır) · dikme / kiriş birleşimleri alın + köşe TIG")
    # alt kayıt takozları (5 mm lama · fırın üst sacına basar · kayda kaynaklı)
    for i, x in enumerate(TAKOZ_X):
        s = G.g.sac("onyuz_f_ust_kayit_takozu_%d" % i, "braket", t=KAYIT_Y[0] - Y_FIRIN)
        s.taban([(x - 20.0, -KAYIT_Z[1]), (x + 20.0, -KAYIT_Z[1]), (x + 20.0, -KAYIT_Z[0]), (x - 20.0, -KAYIT_Z[0])], O=(0, Y_FIRIN, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="takoz")
        for sx in (-1.0, 1.0):
            dikis("onyuz_f_ust_kayit_takozu_%d_kaynak_%s" % (i, "a" if sx < 0 else "b"), (x + sx * 20.0, KAYIT_Y[0], KAYIT_Z[0] + 5.0), (x + sx * 20.0, KAYIT_Y[0], KAYIT_Z[1] - 5.0),
                  (sx, 0, 0), (0, -1.0, 0), 2.0, "takoz ↔ kayıt alt yüzü")
    G.g.not_("alt kayıt 3 × 40 × 30 × 5 lama takozla fırın üst sacına basar (açık kapak raf yükü · v3.6'da 3 mm, kayıt 2 mm yükseldi)")


# =====================================================================================================================================
# 2 · F_UST · SAC KUTU (yanlar · üst · arka · panjur perdeleri)
# =====================================================================================================================================
def _f_yan(taraf):
    g = G.g
    s = g.sac("f_ust_yan_%s" % taraf, "dis", kabuk=True)
    zr, zf = Z_ARKA_IC + G15, Z_ON - G15
    ya = Y_DOLAP + G15                                                           # ayak dönüşü dış yüzü 788 (dolap üstü)
    sol = [(ya, zr), (F_TAVAN[0], zr), (F_TAVAN[0], zf), (F_UST_ALT, zf), (F_UST_ALT, F_SERIT_ON), (ya, F_SERIT_ON)]
    if taraf == "sol":
        P = s.taban(sol, O=(X_F[0], 0, 0), ex=(0, 1, 0), ey=(0, 0, 1), ad="yan")
        e_arka, e_on, e_serit, e_ayak = 0, 2, 4, 5
        f_arka = P.flans(e_arka, ARKA_DONUS, yon=+1, ad="arka_donus")
        P.flans(e_on, ON_DONUS, yon=+1, ad="on_donus")
        f_ser = P.flans(e_serit, ON_DONUS, yon=+1, bas=20.0, son=SERIT_FL_Y0 - ya, ad="serit_on_donus")
        f_ayak = P.flans(e_ayak, AYAK_DONUS, yon=+1, ad="ayak_donus")
        s.kose(f_ayak, f_arka, "acik")
    else:
        sag = [(y, -z) for (y, z) in reversed(sol)]
        P = s.taban(sag, O=(X_F[1], 0, 0), ex=(0, 1, 0), ey=(0, 0, -1), ad="yan")
        e_serit, e_on, e_arka, e_ayak = 0, 2, 4, 5
        f_ser = P.flans(e_serit, ON_DONUS, yon=+1, bas=SERIT_FL_Y0 - ya, son=20.0, ad="serit_on_donus")
        P.flans(e_on, ON_DONUS, yon=+1, ad="on_donus")
        f_arka = P.flans(e_arka, ARKA_DONUS, yon=+1, ad="arka_donus")
        f_ayak = P.flans(e_ayak, AYAK_DONUS, yon=+1, ad="ayak_donus")
        s.kose(f_arka, f_ayak, "acik")
    xs = X_F[0] if taraf == "sol" else X_F[1]
    # hava hattı (EPDM geçme bileziği v3.7'deki gibi kalır) · K tarafı: yağ hortumları + K pilotunun M8 perçin somunlarına Ø9
    if taraf == "sol":
        pan_delik(P, (xs, 1809.0, -432.0), 16.0, tip="gecis", parca="hava ana hattı Ø10 · EPDM geçme bileziği (f_ust_hava_gecme_bilezigi_sol)")
    else:
        pan_oblong(P, (xs, 1809.0, -775.0), 26.0, 16.0, aci=90.0, tip="gecis", parca="hava K dalı Ø10 · F bileziği z −780 + K hava giriş rakoru z −770 (10 kaçık · AÇIK: tek eksen) · yuva 26 × 16")
        pan_delik(P, (xs, 1828.0, -250.0), 14.0, tip="gecis", parca="yağ emiş hortumu (K F_DUVAR_DELIKLERI · EPDM bilezik K'de)")
        pan_delik(P, (xs, 1828.0, -180.0), 12.0, tip="gecis", parca="yağ dönüş hortumu (K F_DUVAR_DELIKLERI)")
        for y, z in K_M8:
            pan_delik(P, (xs, y, z), 9.0, tip="vida_deligi", parca="K↔F M8 (K pilotu perçin somunu · cıvata F içinden · ISO 273 orta)")
    G.P["yan_" + taraf] = P; G.P["yan_%s_arka" % taraf] = f_arka; G.P["yan_%s_sac" % taraf] = s
    return s, P


def _f_tavan():
    g = G.g
    s = g.sac("f_ust_tavan_sac", "dis")
    v_on, v_arka = -(Z_ON - G15), -(Z_ARKA_IC + G15)
    P = s.taban([(X_F[0], v_on), (X_F[1], v_on), (X_F[1], v_arka), (X_F[0], v_arka)], O=(0, F_TAVAN[0], 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="ust")
    on = P.flans(0, F_TAVAN[1] - 1840.5, yon=-1, bas=ON_DONUS + 0.5, son=ON_DONUS + 0.5, ad="on_donus")
    arka = P.flans(2, F_TAVAN[1] - 1840.5, yon=-1, bas=ARKA_DONUS + 1.0, son=ARKA_DONUS + 1.0, ad="arka_donus")
    x0, x1, z0, z1 = ATIS
    pan_dikd(P, ((x0 + x1) / 2.0, F_TAVAN[0], (z0 + z1) / 2.0), (x1 - x0) - 2 * T, (z1 - z0) - 2 * T, tip="atis_agzi", parca="davlumbaz atış ağzı 297 × 197 (kanal iç ölçüsü)")
    G.P["tavan"], G.P["tavan_arka"], G.P["tavan_on"] = P, arka, on
    return s, P


def _f_arka():
    g = G.g
    s = g.sac("f_ust_arka_sac", "dis", kabuk=True)
    P = s.taban([(X_F[0], Y_DOLAP + G15), (X_F[1], Y_DOLAP + G15), (X_F[1], Y_IST), (X_F[0], Y_IST)], O=(0, 0, Z_ARKA), ex=(1, 0, 0), ey=(0, 1, 0), ad="arka")
    P.flans(0, 13.5, yon=+1, bas=25.0, son=25.0, ad="ayak_donus")
    # 4 rakor (v3.7 f_ust_rakor_* yerinde kalır) — (ad, x, y, Ø)
    for ad, x, y, cap in (("cee_firin", 2560.0, 860.0, 33.0), ("sinyal_firin", 2630.0, 830.0, 20.5), ("kompresor", 3689.0, 1825.0, 20.5), ("davlumbaz_fani", 2600.0, 1825.0, 20.5)):
        pan_delik(P, (x, y, Z_ARKA), cap, tip="rakor_deligi", parca="kablo rakoru %s (f_ust_rakor_%s)" % (ad, ad))
    # PANJUR = lazer yarık dizisi (fırın teknik bölme fanları, v3.7 panjur yerleri) · iç su kırıcı perde ayrı sac
    for x in (2640.0, 3860.0):
        P.lazer_yarik_dizisi(x, 982.0, 12, 3, kopru=10.0)
    G.P["arka"] = P
    return s, P


def _f_panjur_perdesi(i, x):
    """iç su kırıcı perde (1,2 · ön plaka + üst / yan dönüşler arka saca punta · altı açık) · yarıklardan sıçrayan su içeride aşağı akar, fan havası alttan çıkar"""
    g = G.g
    s = g.sac("f_ust_panjur_perdesi_%d" % i, "ic")
    gi = s.R + s.t
    w, h, d = 230.0, 210.0, 20.0
    y0, y1 = 982.0 - h / 2.0 - 5.0, 982.0 + h / 2.0
    zp = Z_ARKA_IC + d                                                   # ön plaka iç yüzü
    P = s.taban([(x - w / 2 + gi, y0), (x + w / 2 - gi, y0), (x + w / 2 - gi, y1 - gi), (x - w / 2 + gi, y1 - gi)], O=(0, 0, zp), ex=(1, 0, 0), ey=(0, 1, 0), ad="perde")
    # n = +z → dönüşler arka saca doğru (−z) = yon −1 · dönüş dış yüzü arka sacın iç yüzünde
    fs = [P.flans(k, d + s.t, yon=-1, ad=a) for k, a in ((1, "sag_donus"), (2, "ust_donus"), (3, "sol_donus"))]   # uçlar arka sacın iç yüzüne değer
    s.kose(fs[0], fs[1], "acik"); s.kose(fs[1], fs[2], "acik")
    nok = [(x - w / 2 + 2.0, y, Z_ARKA_IC + 0.5) for y in (y0 + 40.0, (y0 + y1) / 2.0, y1 - 40.0)] + [(x + w / 2 - 2.0, y, Z_ARKA_IC + 0.5) for y in (y0 + 40.0, (y0 + y1) / 2.0, y1 - 40.0)]
    s.punta(G.g.SAC[[q.ad for q in G.g.SAC].index("f_ust_arka_sac")], nok, not_="perde dönüşleri → arka sac (iç yüz) · ≤ 100 aralık")
    return s


def f_kutu():
    with bolum("F_UST_KABIN"):
        _f_yan("sol"); _f_yan("sag"); _f_tavan(); _f_arka()
        for i, x in enumerate((2640.0, 3860.0)): _f_panjur_perdesi(i, x)


# =====================================================================================================================================
# 3 · F_UST · KULAKLAR + SAC BAĞLANTILARI
# =====================================================================================================================================
def f_baglantilar():
    P = G.P
    kc, uc_, zb = (KAYIT_Y[0] + KAYIT_Y[1]) / 2.0, (UST_KAYIT_Y[0] + UST_KAYIT_Y[1]) / 2.0, (BOYUNA_Z[0] + BOYUNA_Z[1]) / 2.0
    with bolum("F_UST_KABIN"):
        for tr, xs, sx in (("sol", X_F[0] + T, 1.0), ("sag", X_F[1] - T, -1.0)):
            A = P["yan_" + tr]
            u_y = (0, sx, 0)
            kulak("govde_kulak_f_%s_kayit" % tr, A, (xs, kc, 8.0), u_y, (0, 0, 1.0), KAYIT_Z[0] - 8.0, gen=20.0)
            kulak("govde_kulak_f_%s_ust_kayit" % tr, A, (xs, uc_, 8.0), u_y, (0, 0, 1.0), KAYIT_Z[0] - 8.0, gen=20.0)
            kulak("govde_kulak_f_%s_boyuna" % tr, A, (xs, UST_KAYIT_Y[0] - 19.0, zb), (0, 0, -sx), (0, 1.0, 0), 19.0)
            # arka sac ↔ yan arka dönüşü (arkada vida başı YOK: arka sacta PEM FHP-M5 · dönüşte Ø5,5 · DIN 9021 + ISO 10511 içeriden)
            for y in GO.vida_konumlari(830.0, 1830.0, maks=200.0, uc=0.0):
                bag(P["arka"], P["yan_%s_arka" % tr], (xs - sx * T + sx * 13.0, y, Z_ARKA), "pem_saplama", ad="govde_bag_f_arka_%s_%d" % (tr, int(y)))
        # üst sac kulakları (FHP-M5 · üstte U_F tabanı → görünmez) · ön üst kayıt arka yüzü + tavan kirişi + boyuna kirişler arka yüzü
        U = P["tavan"]
        for x in (2560.0, 2780.0, 3000.0, 3220.0, 3460.0, 3680.0, 3900.0):
            kulak("govde_kulak_f_ust_on_%d" % int(x), U, (x, F_TAVAN[0], 8.0), (1.0, 0, 0), (0, 0, 1.0), KAYIT_Z[0] - 8.0)
        for z in (-560.0, -760.0):                                             # pizza yığını (z ≥ −424) ve kompresör (z ≥ −383) üstü 0,5–2,5 mm → kulak yalnız arkada
            kulak("govde_kulak_f_ust_kiris_%d" % int(-z), U, (KIRIS_X[1] + 19.0, F_TAVAN[0], z), (0, 0, 1.0), (-1.0, 0, 0), 19.0)
        for x in (2650.0, 3100.0, 3560.0, 3800.0):
            kulak("govde_kulak_f_ust_boyuna_%d" % int(x), U, (x, F_TAVAN[0], BOYUNA_Z[0] - 19.0), (1.0, 0, 0), (0, 0, 1.0), 19.0)
        # arka sac ↔ üst sac arka dönüşü
        for x in kacir(GO.vida_konumlari(X_F[0] + 60.0, X_F[1] - 60.0, maks=200.0, uc=0.0), [(KIRIS_X[0] + KIRIS_X[1]) / 2.0], 25.0):
            bag(P["arka"], P["tavan_arka"], (x, 1849.0, Z_ARKA), "pem_saplama", ad="govde_bag_f_arka_ust_%d" % int(x))
        # tavan kirişi arka ucu → arka sac (kulak altta · ISO 7380 dışarıdan)
        kulak_arka("govde_kulak_f_kiris_arka", P["arka"], ((KIRIS_X[0] + KIRIS_X[1]) / 2.0, UST_KAYIT_Y[0] - 19.0, Z_ARKA_IC), (1.0, 0, 0), (0, 1.0, 0), 19.0)


# =====================================================================================================================================
# 4 · DAVLUMBAZ SAC KUTUSU (kaynaklı sızdırmaz) + askılar + atış kanalı
# =====================================================================================================================================
def davlumbaz():
    g = G.g
    x0, x1, y0, y1, z0, z1 = DAV
    with bolum("F_DAVLUMBAZ"):
        # L1 = ön + alt (kutusu · elektrik delik hedefi adı korunur)
        s1 = g.sac("f_davlumbaz_kutusu", "dis", t=T)
        L1 = s1.taban([(x0, -(y1 - T)), (x1, -(y1 - T)), (x1, -(y0 + G15)), (x0, -(y0 + G15))], O=(0, 0, z1), ex=(1, 0, 0), ey=(0, -1, 0), ad="on")
        alt = L1.flans(2, (z1 - z0) - T, yon=+1, ad="alt")
        for xa in EMIS_X:
            for ya in EMIS_Y:
                pan_oblong(L1, (xa + 80.0, ya + 5.0, z1), 160.0, 10.0, tip="emis_yarigi", parca="emiş yarığı 160 × 10 (yağ filtresinin önü)")
        # L2 = üst + arka
        s2 = g.sac("f_davlumbaz_ust_arka_sac", "dis", t=T)
        L2 = s2.taban([(x0, z0 + G15), (x1, z0 + G15), (x1, z1), (x0, z1)], O=(0, y1, 0), ex=(1, 0, 0), ey=(0, 0, 1), ad="ust")
        L2.flans(0, y1 - y0, yon=+1, ad="arka")
        a0, a1, b0, b1 = ATIS
        pan_dikd(L2, ((a0 + a1) / 2.0, y1, (b0 + b1) / 2.0), (a1 - a0) - 2 * T, (b1 - b0) - 2 * T, tip="atis_agzi", parca="atış ağzı 297 × 197")
        # uç kapakları (tava · içe 12 dönüş · uç kenara iç köşe TIG)
        for tr, xo, sx in (("sol", x0, 1.0), ("sag", x1, -1.0)):
            s = g.sac("f_davlumbaz_yan_kapak_%s" % tr, "dis", t=T)
            gg = s.R + s.t; c = 0.2
            if sx > 0:
                Q = s.taban([(y0 + T + c + gg, z0 + T + c + gg), (y1 - T - c - gg, z0 + T + c + gg), (y1 - T - c - gg, z1 - T - c - gg), (y0 + T + c + gg, z1 - T - c - gg)],
                            O=(xo, 0, 0), ex=(0, 1, 0), ey=(0, 0, 1), ad="kapak")
            else:
                Q = s.taban([(y0 + T + c + gg, -(z1 - T - c - gg)), (y1 - T - c - gg, -(z1 - T - c - gg)), (y1 - T - c - gg, -(z0 + T + c + gg)), (y0 + T + c + gg, -(z0 + T + c + gg))],
                            O=(xo, 0, 0), ex=(0, 1, 0), ey=(0, 0, -1), ad="kapak")
            fs = [Q.flans(k, 12.0, yon=+1, ad="d%d" % k) for k in range(4)]
            for k in range(4): s.kose(fs[k], fs[(k + 1) % 4], "acik")
            xt = xo + sx * 12.0                                                 # dönüş uçları (kutu iç yüzünde) → iç köşe dikişi
            for ad_, p0, p1, u2 in (("alt", (xt, y0 + T, z0 + T + 8), (xt, y0 + T, z1 - T - 8), (0, 1.0, 0)), ("ust", (xt, y1 - T, z0 + T + 8), (xt, y1 - T, z1 - T - 8), (0, -1.0, 0)),
                                    ("on", (xt, y0 + T + 8, z1 - T), (xt, y1 - T - 8, z1 - T), (0, 0, -1.0)), ("arka", (xt, y0 + T + 8, z0 + T), (xt, y1 - T - 8, z0 + T), (0, 0, 1.0))):
                dikis("f_davlumbaz_yan_kapak_%s_kaynak_%s" % (tr, ad_), p0, p1, (sx, 0, 0), u2, 1.5, "uç kapağı dönüş ucu ↔ kutu iç yüzü · sürekli TIG (sızdırmaz)")
        # L1 ↔ L2 boyuna iç köşe dikişleri (sürekli · sızdırmaz)
        dikis("f_davlumbaz_kaynak_on_ust", (x0 + T + 1, y1 - T, z1 - T), (x1 - T - 1, y1 - T, z1 - T), (0, -1.0, 0), (0, 0, -1.0), 1.5, "ön ↔ üst iç köşe · sürekli TIG")
        dikis("f_davlumbaz_kaynak_alt_arka", (x0 + T + 1, y0 + T, z0 + T), (x1 - T - 1, y0 + T, z0 + T), (0, 1.0, 0), (0, 0, 1.0), 1.5, "alt ↔ arka iç köşe · sürekli TIG")
        G.P["dav_alt"] = alt; G.P["dav_L1"] = L1; G.P["dav_L2"] = L2
        # askılar (3 mm L 40 × 60 · yan saca 2 × FHP-M6 · kutu tabanına 2 × FHP-M5 · kutu ucu yan sacdan 23,5 içeride)
        for tr, xs, sx in (("sol", X_F[0] + T, 1.0), ("sag", X_F[1] - T, -1.0)):
            s = g.sac("f_davlumbaz_askisi_%s" % tr, "braket")
            gb = s.R + s.t
            if sx > 0:
                Q = s.taban([(1275.0, -826.0), (y0 - gb, -826.0), (y0 - gb, -656.0), (1275.0, -656.0)], O=(xs, 0, 0), ex=(0, 1, 0), ey=(0, 0, 1), ad="dikey")
                F = Q.flans(1, 60.0, yon=+1, ad="yatay")
            else:
                Q = s.taban([(1275.0, 656.0), (y0 - gb, 656.0), (y0 - gb, 826.0), (1275.0, 826.0)], O=(xs, 0, 0), ex=(0, 1, 0), ey=(0, 0, -1), ad="dikey")
                F = Q.flans(1, 60.0, yon=+1, ad="yatay")
            for z in (-800.0, -682.0):
                bag(G.P["yan_" + tr], Q, (xs, 1290.0, z), "pem_saplama", dis="M6", ad="govde_bag_dav_aski_%s_%d" % (tr, int(-z)))
            for z in (-790.0, -692.0):
                bag(alt, F, (xs + sx * 48.0, y0, z), "pem_saplama", dis="M5", ad="govde_bag_dav_kutu_%s_%d" % (tr, int(-z)))
        # atış kanalı 300 × 200 = 2 L (ön + sağ · arka + sol) + 2 iç köşe dikişi · üstte silikon conta (üst saca)
        ya, yb = y1, F_TAVAN[0] - 2.0
        s = g.sac("f_davlumbaz_atis_kanali", "dis", t=T)                     # ön (dış z −520) + sağ (dış x 3250) · sağ duvar arka duvarın iç yüzüne dayanır
        Q = s.taban([(a0, -yb), (a1 - G15, -yb), (a1 - G15, -ya), (a0, -ya)], O=(0, 0, b1), ex=(1, 0, 0), ey=(0, -1, 0), ad="on")
        Q.flans(1, (b1 - b0) - T, yon=+1, ad="sag")
        s = g.sac("f_davlumbaz_atis_kanali_b", "dis", t=T)                   # arka (dış z −720) + sol (dış x 2950) · sol duvar ön duvarın iç yüzüne dayanır
        Q = s.taban([(a0 + G15, ya), (a1, ya), (a1, yb), (a0 + G15, yb)], O=(0, 0, b0), ex=(1, 0, 0), ey=(0, 1, 0), ad="arka")
        Q.flans(3, (b1 - b0) - T, yon=+1, ad="sol")
        dikis("f_davlumbaz_atis_kanali_kaynak_on_sol", (a0 + T, ya + 1.0, b1 - T), (a0 + T, yb - 1.0, b1 - T), (1.0, 0, 0), (0, 0, -1.0), 1.5, "iç köşe · sürekli TIG (sızdırmaz)")
        dikis("f_davlumbaz_atis_kanali_kaynak_arka_sag", (a1 - T, ya + 1.0, b0 + T), (a1 - T, yb - 1.0, b0 + T), (-1.0, 0, 0), (0, 0, 1.0), 1.5, "iç köşe · sürekli TIG (sızdırmaz)")
        for ad_, p0, p1, u1, u2 in (("on", (a0, ya, b1), (a1, ya, b1), (0, 0, 1.0), (0, 1.0, 0)), ("arka", (a0, ya, b0), (a1, ya, b0), (0, 0, -1.0), (0, 1.0, 0)),
                                     ("sol", (a0, ya, b0), (a0, ya, b1), (-1.0, 0, 0), (0, 1.0, 0)), ("sag", (a1, ya, b0), (a1, ya, b1), (1.0, 0, 0), (0, 1.0, 0))):
            dikis("f_davlumbaz_atis_kanali_kaynak_taban_%s" % ad_, p0, p1, u1, u2, 1.5, "kanal ↔ kutu üstü · sürekli TIG (sızdırmaz)")
        cn = kutu(a0, a1, yb, F_TAVAN[0], b0, b1).cut(kutu(a0 + T, a1 - T, yb - 1, F_TAVAN[0] + 1, b0 + T, b1 - T))
        g.eleman(g.ozel("f_davlumbaz_atis_kanali_contasi", cn, "silikon conta (≥ 200 °C)", "Atış kanalı ↔ üst sac contası VMQ 2 mm (300 × 200 çerçeve)", "300 × 200 × 2",
                        malzeme="VMQ silikon", mal="conta"))


# =====================================================================================================================================
# 5 · U KUTULARI (U_A · U_F · U_KE)
# =====================================================================================================================================
def u_kutu(k):
    g = G.g
    x0, x1 = {"a": X_UA, "f": X_UF, "ke": X_UKE}[k]
    B = {"a": "U_A_GOVDE", "f": "U_F_GOVDE", "ke": "U_KE_GOVDE"}[k]
    kz = (KAYIT_Z[0] + KAYIT_Z[1]) / 2.0
    with bolum(B):
        # ---- taban tepsisi
        s = g.sac("ust_%s_taban_sac" % k, "yuk")
        xa, xb = x0 + T + G15, x1 - T - G15
        zon = Z_ON - T - 0.5                                                   # 57 · ön kenar yan sacların ön dönüşünün (z 57,5–59) arkasında
        P = s.taban([(xa, -zon), (xb, -zon), (xb, -(Z_ARKA_IC + G15)), (xa, -(Z_ARKA_IC + G15))], O=(0, U_TABAN[0], 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="taban")
        b_on, b_ar = zon + 30.0, -(Z_ARKA_IC + G15) - 805.0                      # yan dönüşler z −30 … −805
        sag_f = P.flans(1, 20.0, yon=+1, bas=b_on, son=b_ar, ad="sag_donus")
        sol_f = P.flans(3, 20.0, yon=+1, bas=b_ar, son=b_on, ad="sol_donus")
        if k == "f":
            arka_f = P.flans(2, 20.0, yon=+1, bas=(xb - 3590.0), son=AR_PAY, ad="arka_donus")     # emiş fanı filtre kasaları (x ≥ 3597) önünde kesilir
        elif k == "a":
            arka_f = P.flans(2, 20.0, yon=+1, bas=(xb - UA_ARKA_X1), son=AR_PAY, ad="arka_donus")    # A istasyon kutusu (ELK, x 1240–1400) arka sacın iç yüzünde
        else:
            arka_f = P.flans(2, 20.0, yon=+1, bas=AR_PAY, son=AR_PAY, ad="arka_donus")
        if k == "a":
            a0, a1, b0, b1 = UA_ACIKLIK
            pan_dikd(P, ((a0 + a1) / 2.0, U_TABAN[0], (b0 + b1) / 2.0), a1 - a0, b1 - b0, r=6.0, tip="aciklik", parca="A + U_A tek hacim 632 × 803 (v3.4)")
        if k == "f":
            a0, a1, b0, b1 = BACA
            pan_dikd(P, ((a0 + a1) / 2.0, U_TABAN[0], (b0 + b1) / 2.0), (a1 - a0) + 1.0, (b1 - b0) + 1.0, tip="baca_gecisi", parca="baca uzantısı 300 × 200 geçişi")
        G.P["u%s_taban" % k], G.P["u%s_taban_sag" % k], G.P["u%s_taban_sol" % k], G.P["u%s_taban_arka" % k] = P, sag_f, sol_f, arka_f
        # ---- yanlar (tam boy · ön 16,5 + arka 22 iç dönüş)
        for tr in ("sol", "sag"):
            s = g.sac("ust_%s_yan_%s" % (k, tr), "dis", kabuk=True)
            if tr == "sol":
                Q = s.taban([(U_TABAN[0], Z_ARKA_IC + G15), (U_TAVAN[0], Z_ARKA_IC + G15), (U_TAVAN[0], Z_ON - G15), (U_TABAN[0], Z_ON - G15)],
                            O=(x0, 0, 0), ex=(0, 1, 0), ey=(0, 0, 1), ad="yan")
                fa = Q.flans(0, ARKA_DONUS, yon=+1, ad="arka_donus"); Q.flans(2, ON_DONUS, yon=+1, ad="on_donus")
            else:
                Q = s.taban([(U_TABAN[0], -(Z_ON - G15)), (U_TAVAN[0], -(Z_ON - G15)), (U_TAVAN[0], -(Z_ARKA_IC + G15)), (U_TABAN[0], -(Z_ARKA_IC + G15))],
                            O=(x1, 0, 0), ex=(0, 1, 0), ey=(0, 0, -1), ad="yan")
                Q.flans(0, ON_DONUS, yon=+1, ad="on_donus"); fa = Q.flans(2, ARKA_DONUS, yon=+1, ad="arka_donus")
            G.P["u%s_yan_%s" % (k, tr)], G.P["u%s_yan_%s_arka" % (k, tr)] = Q, fa
        # ---- üst sac (ön kenar ön üst kayda oturur · arka aşağı dönüş)
        s = g.sac("ust_%s_tavan_sac" % k, "dis", kabuk=True)
        U = s.taban([(x0, -Z_ON), (x1, -Z_ON), (x1, -(Z_ARKA_IC + G15)), (x0, -(Z_ARKA_IC + G15))], O=(0, U_TAVAN[0], 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="ust")
        ua = U.flans(2, U_TAVAN[1] - 2178.5, yon=-1, bas=ARKA_DONUS + 1.0, son=ARKA_DONUS + 1.0, ad="arka_donus")
        if k == "f":
            a0, a1, b0, b1 = BACA
            pan_dikd(U, ((a0 + a1) / 2.0, U_TAVAN[0], (b0 + b1) / 2.0), (a1 - a0) - 2 * T, (b1 - b0) - 2 * T, tip="baca_agzi", parca="baca ağzı 297 × 197 (kanal iç)")
            for x in (a0 - 15.0, (a0 + a1) / 2.0, a1 + 15.0):
                for z in (b0 - 15.0, b1 + 15.0):
                    pan_delik(U, (x, U_TAVAN[0], z), 6.6, tip="vida_deligi", parca="baca flanşı M6 (bina kanalı üstten · ISO 273 orta)")
            for z in ((b0 + b1) / 2.0,):
                for x in (a0 - 15.0, a1 + 15.0):
                    pan_delik(U, (x, U_TAVAN[0], z), 6.6, tip="vida_deligi", parca="baca flanşı M6")
        G.P["u%s_tavan" % k], G.P["u%s_tavan_arka" % k] = U, ua
        # ---- arka sac (tek parça · düz)
        s = g.sac("ust_%s_arka_sac" % k, "dis", kabuk=True)
        A = s.taban([(x0, U_TABAN[0]), (x1, U_TABAN[0]), (x1, Y_UST), (x0, Y_UST)], O=(0, 0, Z_ARKA), ex=(1, 0, 0), ey=(0, 1, 0), ad="arka")
        if k == "f":
            for ad, xc, yc in UF_FAN:
                for j in range(9):
                    pan_oblong(A, (xc, yc - 48.0 + 12.0 * j, Z_ARKA), 100.0, 6.0, tip="fan_izgarasi", parca="U_F fanı %s ızgarası 9 × 100 × 6" % ad)
        G.P["u%s_arka" % k] = A
        # ---- ön çerçeve (alt + üst kayıt) + tavan kirişleri (kaynaklı)
        al = profil("onyuz_ust_%s_alt_kayit" % k, "x", x0 + G15 + 0.5 + PT, x1 - G15 - 0.5 - PT, ((U_ALT_KAYIT_Y[0] + U_ALT_KAYIT_Y[1]) / 2.0, kz), "U ön alt kayıt")
        ul = profil("onyuz_ust_%s_ust_kayit" % k, "x", x0 + G15 + 0.5 + PT, x1 - G15 - 0.5 - PT, ((U_UST_KAYIT_Y[0] + U_UST_KAYIT_Y[1]) / 2.0, kz), "U ön üst kayıt")
        G.P["u%s_alt_kayit" % k], G.P["u%s_ust_kayit" % k] = al, ul
        for pr in (al, ul):
            for uc in ("alt", "ust"):
                GO.dikme_tapasi(g, pr, uc=uc, ad="%s_tapa_%s" % (pr.ad, "sol" if uc == "alt" else "sag"))
        yk = (U_UST_KAYIT_Y[0] + U_UST_KAYIT_Y[1]) / 2.0
        for i, xc in enumerate(U_KIRIS[{"a": "A", "f": "F", "ke": "KE"}[k]]):
            kr = profil("ust_%s_tavan_kirisi_%d" % (k, i), "z", Z_ARKA_IC + G15 + 0.5 + PT, KAYIT_Z[0], (xc, yk), "U tavan kirişi (üst sacı taşır)")
            ul.kaynak_bolgesi("-z", xc - PB / 2, xc + PB / 2)
            uc_kaynak("ust_%s_tavan_kirisi_%d_kaynak" % (k, i), (xc, yk, KAYIT_Z[0]), (0, 0, -1.0), [(1.0, 0, 0), (-1.0, 0, 0), (0, -1.0, 0)])
            GO.dikme_tapasi(g, kr, uc="alt", ad="%s_tapa" % kr.ad)
            G.P["u%s_kiris_%d" % (k, i)] = kr
        # alt kayıt ↔ taban (3 dikiş / kenar)
        for xc in np.linspace(x0 + 120.0, x1 - 120.0, 3):
            for zz, nz in ((KAYIT_Z[0], -1.0), (KAYIT_Z[1], 1.0)):
                dikis("onyuz_ust_%s_alt_kayit_taban_kaynagi_%d_%s" % (k, int(xc), "a" if nz < 0 else "b"), (xc - 20.0, U_TABAN[1], zz), (xc + 20.0, U_TABAN[1], zz),
                      (0, 0, nz), (0, 1.0, 0), 2.0, "alt kayıt ↔ taban (dikiş 40)")


def u_raf(k):
    """U_F kutu rafı / U_KE içecek rafı: 1,5 tepsi (ön + arka aşağı 15) · z boyunca 30 × 30 × 2 taşıyıcılar tabana kaynaklı · raf taşıyıcılara delik kaynağıyla"""
    g = G.g
    R = UF_RAF if k == "f" else UKE_RAF
    ad_raf = "ust_f_kutu_rafi" if k == "f" else "ust_ke_icecek_rafi"
    B = "U_F_GOVDE" if k == "f" else "U_KE_GOVDE"
    with bolum(B):
        (xa, xb), (za, zb) = R["x"], R["z"]
        s = g.sac(ad_raf, "yuk")
        P = s.taban([(xa, -(zb - G15)), (xb, -(zb - G15)), (xb, -(za + G15)), (xa, -(za + G15))], O=(0, RAF_Y[0], 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="raf")
        P.flans(0, 15.0, yon=-1, bas=27.0, son=27.0, ad="on_donus"); P.flans(2, 15.0, yon=-1, bas=27.0, son=27.0, ad="arka_donus")   # uçlar: alt kayıt kulakları
        G.P["u%s_raf" % k] = P
        ka, kb = za + G15 + 0.5 + PT, zb - G15 - 0.5 - PT                      # tapalar raf dönüşlerinin büküm yayından 0,5 içeride
        for i, xc in enumerate(R["kiris"]):
            pr = profil("ust_%s_raf_kirisi_%d" % (k, i), "z", ka, kb, (xc, (U_TABAN[1] + RAF_Y[0]) / 2.0), "raf taşıyıcı (tabana kaynaklı)")
            GO.dikme_tapasi(g, pr, uc="alt", ad="%s_tapa_arka" % pr.ad); GO.dikme_tapasi(g, pr, uc="ust", ad="%s_tapa_on" % pr.ad)
            for zc in (ka + 60.0, (ka + kb) / 2.0, kb - 60.0):
                for sx in (-1.0, 1.0):
                    dikis("ust_%s_raf_kirisi_%d_taban_kaynagi_%d_%s" % (k, i, int(-zc), "a" if sx < 0 else "b"), (xc + sx * PB / 2, U_TABAN[1], zc - 20.0),
                          (xc + sx * PB / 2, U_TABAN[1], zc + 20.0), (sx, 0, 0), (0, 1.0, 0), 2.0, "taşıyıcı ↔ taban (dikiş 40)")
            for j, zc in enumerate((ka + 80.0, kb - 80.0)):
                P_ = P
                uv = P_.yerel(np.array([xc, RAF_Y[0], zc]))
                P_.oblong(uv[0], uv[1], 25.0, 8.0, 90.0, tip="kaynak_yarigi", parca="delik kaynağı 25 × 8 (taşıyıcıya) · yüz taşlanır")
                f = S.yuz_oblong(uv[0], uv[1], 25.0, 8.0, 90.0)
                sh = S._tasi(S._prizma(f, T), S._M(np.column_stack([[1, 0, 0], [0, 0, -1.0], [0, 1.0, 0]]), (0, RAF_Y[0], 0)))
                g.kaynak(dict(ad="%s_delik_kaynagi_%d_%d" % (ad_raf, i, j), wp=cq.Workplane("XY").add(sh), sh=sh, mal="sac", birim=g.birim, grup="SABIT", kaynak=SURUM,
                              tur="kaynak", bom=("Delik (yarık) kaynağı · TIG 141 · ER308LSi · yüz taşlanır", 1, "25 × 8 × 1,5", "raf ↔ taşıyıcı", "ÜRETİM"),
                              meta=dict(tur="kaynak", tip="delik", yontem="TIG 141")))


def u_baglantilar(k):
    g = G.g
    x0, x1 = {"a": X_UA, "f": X_UF, "ke": X_UKE}[k]
    B = {"a": "U_A_GOVDE", "f": "U_F_GOVDE", "ke": "U_KE_GOVDE"}[k]
    P = G.P
    yka, yku = (U_ALT_KAYIT_Y[0] + U_ALT_KAYIT_Y[1]) / 2.0, (U_UST_KAYIT_Y[0] + U_UST_KAYIT_Y[1]) / 2.0
    with bolum(B):
        for tr, xs, sx in (("sol", x0 + T, 1.0), ("sag", x1 - T, -1.0)):
            A = P["u%s_yan_%s" % (k, tr)]
            kulak("govde_kulak_u%s_%s_alt_kayit" % (k, tr), A, (xs, yka, 8.0), (0, sx, 0), (0, 0, 1.0), KAYIT_Z[0] - 8.0, gen=20.0)
            kulak("govde_kulak_u%s_%s_ust_kayit" % (k, tr), A, (xs, yku, 8.0), (0, sx, 0), (0, 0, 1.0), KAYIT_Z[0] - 8.0, gen=20.0)
            # yan ↔ taban yan dönüşü (FHP-M5 dışarıdan iz yok)
            for z in (-785.0, -600.0, -415.0, -230.0, -50.0):
                bag(A, P["u%s_taban_%s" % (k, tr)], (x0 if sx > 0 else x1, 1873.5, z), "pem_saplama", ad="govde_bag_u%s_taban_%s_%d" % (k, tr, int(-z)))
            # arka sac ↔ yan arka dönüşü (üst hat kablo kanalı y 2143–2167 bölgesi boş)
            for y in (1912.0, 2040.0, 2190.0):
                bag(P["u%s_arka" % k], P["u%s_yan_%s_arka" % (k, tr)], (xs - sx * T + sx * 13.0, y, Z_ARKA), "pem_saplama", ad="govde_bag_u%s_arka_%s_%d" % (k, tr, int(y)))
        # arka sac ↔ taban arka dönüşü / üst sac arka dönüşü
        xa_f = (x0 + 60.0, {"f": 3560.0, "a": UA_ARKA_X1 - 40.0}.get(k, x1 - 60.0))
        for x in GO.vida_konumlari(xa_f[0], xa_f[1], maks=200.0, uc=0.0):
            bag(P["u%s_arka" % k], P["u%s_taban_arka" % k], (x, 1873.5, Z_ARKA), "pem_saplama", ad="govde_bag_u%s_arka_taban_%d" % (k, int(x)))
        for x in kacir(GO.vida_konumlari(x0 + 60.0, x1 - 60.0, maks=200.0, uc=0.0), U_KIRIS[{"a": "A", "f": "F", "ke": "KE"}[k]], 25.0):
            bag(P["u%s_arka" % k], P["u%s_tavan_arka" % k], (x, 2188.5, Z_ARKA), "pem_saplama", ad="govde_bag_u%s_arka_ust_%d" % (k, int(x)))
        # üst sac kulakları: ön üst kayıt arka yüzü + tavan kirişleri yanları
        U = P["u%s_tavan" % k]
        for x in kacir(GO.vida_konumlari(x0 + 80.0, x1 - 80.0, maks=250.0, uc=0.0), U_KIRIS[{"a": "A", "f": "F", "ke": "KE"}[k]], 45.0):
            kulak("govde_kulak_u%s_ust_on_%d" % (k, int(x)), U, (x, U_TAVAN[0], 8.0), (1.0, 0, 0), (0, 0, 1.0), KAYIT_Z[0] - 8.0)
        for i, xc in enumerate(U_KIRIS[{"a": "A", "f": "F", "ke": "KE"}[k]]):
            sk = -1.0 if (k == "f" and i == 1) else 1.0                                # U_F kiriş 1'in sağı ana pano (x ≥ 3518) → kulak solda
            for z in (-280.0, -640.0):
                kulak("govde_kulak_u%s_ust_kiris_%d_%d" % (k, i, int(-z)), U, (xc + sk * (PB / 2 + 19.0), U_TAVAN[0], z), (0, 0, sk), (-sk, 0, 0), 19.0)


# =====================================================================================================================================
# 6 · F ÖN KAPAKLARI (çift cidar · düşer · gizli menteşe kayıt içinde · bas-aç U_F üst kaydında · gazlı yay)
# =====================================================================================================================================
def _yay_parcalar(tr, K):
    """çekme tipi gazlı yay (Bansbach easylift traction sınıfı) · DIN 71805 bilyalı yuvalar · DIN 71803 bilyalı pimler M8 · KAPALI konumda modellenir
    sabit uç: yan sacın iç yüzünde 3 mm lama 70 × 40 (2 × FHP-M6) + DIN 929 M8 kaynak somunu · kapak ucu: iç tavanın arkasına puntalı 3 mm L braket + PEM SP-M8"""
    g = G.g
    sx = 1.0 if tr == "sol" else -1.0
    xs = YAY["x_sol"] if tr == "sol" else 2 * 3250.0 - YAY["x_sol"]
    yA, zA = YAY["A"]; yB, zB = YAY["B"]
    xyan = X_F[0] + T if tr == "sol" else X_F[1] - T
    # ---- sabit braket (lama 70 × 40 × 3 · M6 delikleri kenardan ≥ 2t)
    s = g.sac("govde_gazli_yay_braketi_%s" % tr, "braket")
    if sx > 0:
        Q = s.taban([(yA - 35.0, zA - 20.0), (yA + 35.0, zA - 20.0), (yA + 35.0, zA + 20.0), (yA - 35.0, zA + 20.0)], O=(xyan, 0, 0), ex=(0, 1, 0), ey=(0, 0, 1), ad="lama")
    else:
        Q = s.taban([(yA - 35.0, -zA - 20.0), (yA + 35.0, -zA - 20.0), (yA + 35.0, -zA + 20.0), (yA - 35.0, -zA + 20.0)], O=(xyan, 0, 0), ex=(0, 1, 0), ey=(0, 0, -1), ad="lama")
    for dy in (-21.0, 21.0):
        bag(G.P["yan_" + tr], Q, (xyan, yA + dy, zA), "pem_saplama", dis="M6", ad="govde_gazli_yay_braketi_%s_bag_%s" % (tr, "a" if dy < 0 else "b"))
    xq = xyan + sx * s.t
    pan_delik(Q, (xyan, yA, zA), 9.0, tip="vida_deligi", parca="bilyalı pim M8 geçişi (DIN 929 arkada)")
    ks = S.kaynak_somunu("M8", (xq, yA, zA), (sx, 0, 0), ad="govde_gazli_yay_braketi_%s_kaynak_somunu" % tr, birim=g.birim)
    g.eleman(ks)
    A3 = np.array([xs, yA, zA]); B3 = np.array([xs, yB, zB])

    def pim(ad, taban, uc, doner=None):
        e = np.asarray(uc, float) - np.asarray(taban, float); L = float(np.linalg.norm(e)); e = e / L
        sh = silindir(taban, e, 4.0, max(L - 6.0, 0.5)).fuse(cq.Solid.makeSphere(6.5, V(*map(float, uc)), angleDegrees1=-90, angleDegrees2=90))
        p = g.ozel(ad, sh, "DIN 71803 bilyalı pim M8 · bilya Ø13 · A2", "Bilyalı mafsal pimi M8 / Ø13 (gazlı yay ucu)", "M8 × %.0f" % L, malzeme="A2", mal="celik")
        g.eleman(p, doner=doner)
    pim("onyuz_f_ust_gazli_yay_%s_pim_a" % tr, (xq + sx * S.DIN929["M8"][1], yA, zA), A3)
    # ---- yay (gövde Ø19 · mil Ø8 · bilyalı yuvalar Ø16)
    d = B3 - A3; L = float(np.linalg.norm(d)); e = d / L
    yv, Lg = 16.0, 0.55 * L
    gov = silindir(A3 + e * yv, e, 9.5, Lg)
    mil = silindir(A3 + e * (yv + Lg), e, 4.0, L - 2 * yv - Lg)
    ya_ = silindir(A3 - e * 7.0, e, 8.0, yv + 7.0).cut(cq.Solid.makeSphere(6.6, V(*A3), angleDegrees1=-90, angleDegrees2=90)).cut(silindir(A3, (-sx, 0, 0), 4.6, 20.0))
    yb_ = silindir(B3 - e * yv, e, 8.0, yv + 7.0).cut(cq.Solid.makeSphere(6.6, V(*B3), angleDegrees1=-90, angleDegrees2=90)).cut(silindir(B3, (sx, 0, 0), 4.6, 20.0))
    for ad, sh, tn in (("govde", gov, "Çekme tipi gazlı yay gövdesi Ø19"), ("mil", mil, "gazlı yay mili Ø8"), ("yuva_a", ya_, "bilyalı yuva DIN 71805 Ø13"),
                       ("yuva_b", yb_, "bilyalı yuva DIN 71805 Ø13")):
        g.eleman(g.ozel("onyuz_f_ust_gazli_yay_%s_%s" % (tr, ad), sh, "Bansbach easylift çekme tipi (F ve boy siparişte · hesap: rapor 'yay')", tn,
                        "kapalı göz arası %.0f" % L, malzeme="çelik / paslanmaz", mal="siyah"))
    # ---- kapak braketi (3 mm L · ayak iç tavanın arkasında · kulak arkaya doğru)
    s = g.sac("onyuz_f_ust_kapak_%s_gazli_yay_braketi" % tr, "braket", doner=K)
    gb = s.R + s.t
    xf = xs + sx * 16.0                                                                    # kulak dış yüzü (yaya bakmayan yüz)
    if sx > 0:
        Q = s.taban([(yB - 14.0, xf - 26.0), (yB + 14.0, xf - 26.0), (yB + 14.0, xf - gb), (yB - 14.0, xf - gb)], O=(0, 0, Z_ON), ex=(0, 1, 0), ey=(1, 0, 0), ad="ayak")
    else:
        Q = s.taban([(-(yB + 14.0), -xf - 26.0), (-(yB - 14.0), -xf - 26.0), (-(yB - 14.0), -xf - gb), (-(yB + 14.0), -xf - gb)], O=(0, 0, Z_ON), ex=(0, -1, 0), ey=(-1, 0, 0), ad="ayak")
    F = Q.flans(2, Z_ON - (zB - 14.0), yon=+1, ad="kulak")
    s.punta(K.ki, [(xf - sx * 16.0, yB - 8.0, Z_ON), (xf - sx * 16.0, yB + 8.0, Z_ON)], not_="yay braketi → iç tava (kapak kapanmadan)")
    ps, c, ms = S.pem_somun("SP", "M8", (xf - sx * s.t, yB, zB), (-sx, 0, 0), s.t, ad="onyuz_f_ust_kapak_%s_gazli_yay_pem" % tr, birim=g.birim)
    pan_delik(F, (xf, yB, zB), c["delik"], tip="pem_somun", parca=ps["meta"]["parca"], pem_tip="SP", kenar_min=c["kenar"], min_sac=ms)
    g.eleman(ps, doner=K)
    h_pem = ps["meta"]["T"] - ps["meta"]["sap"]
    pim("onyuz_f_ust_kapak_%s_gazli_yay_pim_b" % tr, (xf - sx * (s.t + h_pem), yB, zB), B3, doner=K)
    G.HESAP["yay_" + tr] = dict(A=[float(c_) for c_ in A3], B=[float(c_) for c_ in B3], L_kapali=round(L, 1))


def f_kapaklar():
    g = G.g
    with bolum("F_UST_KAPAK"):
        for k, (a, b) in enumerate(KANAT_X):
            tr = ("sol", "sag")[k]
            K = GO.kapak(g, "onyuz_f_ust_kapak_%s" % tr, a, b, KAPAK_Y[0], KAPAK_Y[1], Z_KAPAK, Z_ON, ustte="yatay", punta_aralik=150.0)
            G.KAPAK[K.ad] = K
            GO.gizli_mentese(g, K, G.P["kayit"], "alt", (a + MENTESE_DX, b - MENTESE_DX))
            GO.bas_ac(g, K, G.P["uf_ust_kayit"], "ust", (a + BASAC_DX, b - BASAC_DX), a=BASAC_A)
            uc = (a + b) / 2.0
            for vb in YARIK_BANT_Y:
                K.D.lazer_yarik_dizisi(uc, vb, 3, 9, kopru=15.0, sira=10.0)
                K.I.lazer_yarik_dizisi(uc, vb, 3, 9, kopru=15.0, sira=10.0)
            _yay_parcalar(tr, K)
        g.doner_guncelle()


# =====================================================================================================================================
# 7 · KOMŞU / KUTULAR ARASI BAĞLANTILAR (M8)
# =====================================================================================================================================
def _arayuz_civata(etiket, nokta, eksen, karsi, gerek, dis="M8", boy=25, pul="DIN9021", not_=""):
    """bizim taraftan takılan arayüz cıvatası (montaja girmez, BOM'a ARAYÜZ satırı) · nokta: baş oturma yüzü · eksen: uca doğru"""
    g = G.g
    hp = (S.DIN9021 if pul == "DIN9021" else S.DIN125)[dis][2]
    p0 = np.asarray(nokta, float); e = np.asarray(eksen, float)
    pu = S.pul(pul, dis, tuple(p0), tuple(e), ad="arayuz_m8_%s_pul" % etiket, birim=g.birim)
    vd = S.vida("ISO4762", dis, boy, tuple(p0 - e * hp), tuple(e), ad="arayuz_m8_%s" % etiket, birim=g.birim)
    g.arayuz(pu, karsi, gerek, not_); g.arayuz(vd, karsi, gerek, not_)
    return vd


def baglantilar():
    g = G.g; P = G.P
    out = []
    # ---- F_UST ↔ TOPPING (sol yan · cıvata F içinden → TOPPING tarafında M8 diş)
    with bolum("F_UST_KABIN"):
        for y, z in TOP_M8_F:
            pan_delik(P["yan_sol"], (X_F[0], y, z), 9.0, tip="vida_deligi", parca="F↔TOPPING M8 (ISO 273 orta)")
            _arayuz_civata("TOP_F_%d_%d" % (int(y), int(-z)), (X_F[0] + T, y, z), (-1.0, 0, 0), "TOPPING_MODUL dis_yan_sag",
                           "TOPPING sağ yan sacında M8 perçin somun (delik Ø11, kavrama sac + takviye) ya da kaynak somunu · aynı eksen", not_="F içinden takılır (kapak açık)")
            out.append(dict(taraf="TOPPING", ad="TOP_F_%d_%d" % (int(y), int(-z)), dunya=[X_F[0], y, z], bizde="f_ust_yan_sol Ø9 + ISO 4762 M8 × 25 + DIN 9021",
                            karsi="TOPPING_MODUL dis_yan_sag: M8 perçin somun (Ø11) — x %.1f y %.0f z %.0f" % (X_F[0], y, z)))
        for y, z in K_M8:
            out.append(dict(taraf="K", ad="K_F_%d_%d" % (int(y), int(-z)), dunya=[X_F[1], y, z], bizde="f_ust_yan_sag Ø9 (hazır)",
                            karsi="K pilotu: perçin somun + cıvata K tarafında tanımlı (h3_k_sac_v1 M8_F) — ek iş yok"))
    # ---- U_A ↔ TOPPING · U_F ↔ TOPPING (U içinden)
    for k, xs, sx, L, A_ad in (("a", X_UA[1], -1.0, TOP_M8_UA, "ust_a_yan_sag"), ("f", X_UF[0], 1.0, TOP_M8_UF, "ust_f_yan_sol")):
        with bolum("U_A_GOVDE" if k == "a" else "U_F_GOVDE"):
            for y, z in L:
                pan_delik(P["u%s_yan_%s" % (k, "sag" if sx < 0 else "sol")], (xs, y, z), 9.0, tip="vida_deligi", parca="U↔TOPPING M8")
                _arayuz_civata("TOP_U%s_%d_%d" % (k.upper(), int(y), int(-z)), (xs + sx * T, y, z), (-sx, 0, 0), "TOPPING_MODUL dis_yan_%s" % ("sol" if sx < 0 else "sag"),
                               "TOPPING yan sacında M8 perçin somun (Ø11) · aynı eksen", not_="U içinden takılır")
                out.append(dict(taraf="TOPPING", ad="TOP_U%s_%d_%d" % (k.upper(), int(y), int(-z)), dunya=[xs, y, z], bizde="%s Ø9 + ISO 4762 M8 × 25 + DIN 9021" % A_ad,
                                karsi="TOPPING_MODUL dis_yan_%s: M8 perçin somun (Ø11) — x %.1f y %.0f z %.0f" % ("sol" if sx < 0 else "sag", xs, y, z)))
    # ---- U_F ↔ U_KE (ikisi de bizim · M8 cıvata + pul + fiberli somun)
    with bolum("U_F_GOVDE"):
        for y, z in UF_UKE_M8:
            bag(P["uf_yan_sag"], P["uke_yan_sol"], (X_UF[1], y, z), "somun", dis="M8", ad="govde_bag_uf_uke_%d_%d" % (int(y), int(-z)))
    # ---- U_F → F_UST (DIN 929 kaynak somunu U_F tabanında · cıvata F_UST içinden yukarı)
    with bolum("U_F_GOVDE"):
        for x, z in UF_F_M8:
            ks = S.kaynak_somunu("M8", (x, U_TABAN[1], z), (0, 1.0, 0), ad="govde_m8_uf_f_%d_%d_kaynak_somunu" % (int(x), int(-z)), birim=g.birim)
            g.eleman(ks)
            pan_delik(P["uf_taban"], (x, U_TABAN[0], z), 9.0, tip="vida_deligi", parca="U_F→F_UST M8 (DIN 929 üstte)")
            pan_delik(P["tavan"], (x, F_TAVAN[0], z), 9.0, tip="vida_deligi", parca="U_F→F_UST M8")
            pu = S.pul("DIN125", "M8", (x, F_TAVAN[0], z), (0, -1.0, 0), ad="govde_m8_uf_f_%d_%d_pul" % (int(x), int(-z)), birim=g.birim)
            vd = S.vida("ISO4762", "M8", 16, (x, F_TAVAN[0] - 1.6, z), (0, 1.0, 0), ad="govde_m8_uf_f_%d_%d_civata" % (int(x), int(-z)), birim=g.birim)
            g.eleman(pu); g.eleman(vd)
    # ---- U_KE → K / E (DIN 929 U_KE tabanında · cıvata K / E içinden · onlarda yalnız Ø9)
    with bolum("U_KE_GOVDE"):
        for taraf, L, karsi in (("K", UKE_K_M8, "K_GOVDE ust_sac"), ("E", UKE_E_M8, "E_GOVDE üst sac (E sahibi · v3.7 adı)")):
            for x, z in L:
                et = "UKE_%s_%d_%d" % (taraf, int(x), int(-z))
                ks = S.kaynak_somunu("M8", (x, U_TABAN[1], z), (0, 1.0, 0), ad="govde_m8_%s_kaynak_somunu" % et.lower(), birim=g.birim)
                g.eleman(ks)
                pan_delik(P["uke_taban"], (x, U_TABAN[0], z), 9.0, tip="vida_deligi", parca="U_KE→%s M8 (DIN 929 üstte)" % taraf)
                _arayuz_civata(et, (x, U_TABAN[0] - T, z), (0, 1.0, 0), karsi, "%s üst sacında Ø9 (ISO 273 orta) · aynı eksen · cıvata %s içinden" % (taraf, taraf),
                               dis="M8", boy=16, pul="DIN125")
                out.append(dict(taraf=taraf, ad=et, dunya=[x, U_TABAN[0] - T, z], bizde="ust_ke_taban_sac Ø9 + DIN 929 M8 kaynak somunu",
                                karsi="%s: Ø9 (x %.0f z %.0f, sacın üst yüzü 1862) · ISO 4762 M8 × 16 + DIN 125 içeriden" % (karsi, x, z)))
    # ---- U_A → A (U_A içinden aşağı · A üst kuşağında perçin somun)
    with bolum("U_A_GOVDE"):
        for x, z in UA_A_M8:
            et = "UA_A_%d_%d" % (int(x), int(-z))
            pan_delik(P["ua_taban"], (x, U_TABAN[0], z), 9.0, tip="vida_deligi", parca="U_A→A M8")
            _arayuz_civata(et, (x, U_TABAN[1], z), (0, -1.0, 0), "A_GOVDE a_govde_ust + üst kuşak", "A üst sacında Ø9 + altındaki üst kuşağın üst duvarında M8 perçin somun (Ø11)",
                           dis="M8", boy=25, pul="DIN125")
            out.append(dict(taraf="A", ad=et, dunya=[x, U_TABAN[0], z], bizde="ust_a_taban_sac Ø9 + ISO 4762 M8 × 25 + DIN 125 (U_A içinden)",
                            karsi="A_GOVDE: a_govde_ust Ø9 + üst kuşak üst duvarında M8 perçin somun (x %.0f z %.0f)" % (x, z)))
    # ---- ana pano rayları: 2 × ISO 13918 M6 kaynak saplaması (U_F tabanı üstüne, rayların arkada taşan 25 mm dilinde · çift sac: alttan somun olmaz)
    with bolum("U_F_GOVDE"):
        for x, z in PANO_RAY:
            sh = silindir((x, U_TABAN[1], z), (0, 1.0, 0), 2.97, 12.0).fuse(silindir((x, U_TABAN[1], z), (0, 1.0, 0), 4.0, 1.0))
            g.eleman(g.ozel("govde_pano_saplamasi_%d_%d" % (int(x), int(-z)), sh, "ISO 13918 CD (kondansatör deşarjlı) A2", "Kaynak saplaması M6 × 12 (ana pano taban rayı · arka dil)",
                            "M6 × 12", malzeme="A2 (1.4301)", mal="celik"))
            pu = S.pul("DIN125", "M6", (x, U_TABAN[1] + 3.0, z), (0, 1.0, 0), ad="arayuz_pano_ray_%d_%d_pul" % (int(x), int(-z)), birim=g.birim)
            so = S.somun("ISO10511", "M6", (x, U_TABAN[1] + 3.0 + 1.6, z), (0, 1.0, 0), ad="arayuz_pano_ray_%d_%d_somun" % (int(x), int(-z)), birim=g.birim)
            g.arayuz(pu, "ELK_ANA_PANO_UF ana_pano_taban_rayi", "rayda Ø6,6 (saplama geçer) · DIN 125 + ISO 10511 M6 üstten", "pano sahibi: ray delikleri saplama eksenine")
            g.arayuz(so, "ELK_ANA_PANO_UF ana_pano_taban_rayi", "rayda Ø6,6", "")
    G.M8 = out


# =====================================================================================================================================
# 8 · ELEKTRİK DELİKLERİ (h3/_elk DELIKLER — montaj aynı adlara keser · burada açınıma işlenir)
# =====================================================================================================================================
def _elk_delikleri(log=print):
    if not os.path.exists(ELK_DELIK):
        G.g.not_("elektrik delik verisi yok (%s) — delikler yalnız montajın ad-kesiminde" % ELK_DELIK); return
    J = json.load(open(ELK_DELIK, encoding="utf-8"))
    sac = {s.ad: s for s in G.g.SAC}
    for d in J:
        s = sac.get(d["ad"])
        if s is None:
            G.ELK.append(dict(d, durum="SAC YOK")); continue
        bb = d["bb"]; c = np.array([(bb[0] + bb[1]) / 2.0, (bb[2] + bb[3]) / 2.0, (bb[4] + bb[5]) / 2.0])
        en_iyi = None
        for Pn in s.paneller:
            n = Pn.normal(); uvw = Pn.yerel(c)
            ext = np.array([bb[1] - bb[0], bb[3] - bb[2], bb[5] - bb[4]])
            yari_n = float(np.dot(np.abs(n), ext)) / 2.0
            z_ok = -yari_n - 0.01 <= uvw[2] <= s.t + yari_n + 0.01
            if not z_ok or not Pn.icerir(uvw[0], uvw[1]): continue
            if en_iyi is None or abs(uvw[2] - s.t / 2) < abs(en_iyi[1][2] - s.t / 2): en_iyi = (Pn, uvw)
        if en_iyi is None:
            G.ELK.append(dict(d, durum="PANEL BULUNAMADI (montaj ad-kesimi uygular)")); continue
        Pn, uvw = en_iyi
        ex, ey = Pn.M[:3, 0], Pn.M[:3, 1]
        ext = np.array([bb[1] - bb[0], bb[3] - bb[2], bb[5] - bb[4]])
        bu, bv = float(np.dot(np.abs(ex), ext)) - 2.0, float(np.dot(np.abs(ey), ext)) - 2.0
        sil = d.get("silindir")
        if sil and abs(abs(float(np.dot(np.asarray(sil["eksen"]), Pn.normal()))) - 1.0) < 1e-3:
            cap = max(2.0 * sil["r"], ELK_CAP.get((d["ad"], d["not_"]), 0.0))
            Pn.delik(uvw[0], uvw[1], cap, tip="elk_gecis", parca=d["not_"])
            G.ELK.append(dict(modul=d["modul"], ad=d["ad"], not_=d["not_"], panel=Pn.ad, tip="daire", cap=round(cap, 2), kesici_cap=round(2 * sil["r"], 2),
                              uv=[round(uvw[0], 2), round(uvw[1], 2)], durum="AÇINIMDA"))
        else:
            Pn.dikdortgen(uvw[0], uvw[1], bu, bv, tip="elk_gecis", dfm=False, parca=d["not_"])
            G.ELK.append(dict(modul=d["modul"], ad=d["ad"], not_=d["not_"], panel=Pn.ad, tip="dikdortgen", olcu=[round(bu, 1), round(bv, 1)], uv=[round(uvw[0], 2), round(uvw[1], 2)],
                              durum="AÇINIMDA (kesik kenara kadar · dfm dışı)"))


def _kalinlik_izgara(s):
    """GEÇİCİ ÇÖZÜM (h3_sac_v1.kalinlik_denetle sınırı — raporlandı): ölçüm noktaları yüzün UV dikdörtgeninde 9 sabit oranda; büyük açıklıklı
    yüzde (ust_a_taban_sac · 632 × 803 açıklık yüzün %93'ü) 9 nokta da boşluğa düşer → 'ışın yok' HATA. Burada aynı ölçüm (iç normal yönünde ışın,
    karşı yüze uzaklık = t) yalnız ışınsız kalan düz yüzlerde 21 × 21 ızgaradan malzeme üstündeki ilk 9 noktayla tekrarlanır; sonuç dogrula() önbelleğine yazılır."""
    r = s.dogrula(); k = r["kalinlik"]
    if k["gecti"] or not k["hata"] or any(h["isin"] for h in k["hata"]): return None
    A = s.kati_temel(); F = A.Faces(); t = s.t; tol = max(0.01, 0.01 * t)
    it = S.IntCurvesFace_ShapeIntersector(); it.Load(A.wrapped, 1e-7)
    kalan, olc = [], []
    for h in k["hata"]:
        f = F[h["yuz"]]
        if f.geomType() != "PLANE": kalan.append(h); continue
        Sf = S.BRepAdaptor_Surface(f.wrapped, True)
        u0, u1, v0, v1 = Sf.FirstUParameter(), Sf.LastUParameter(), Sf.FirstVParameter(), Sf.LastVParameter()
        ds = []
        for i in range(1, 21):
            for j in range(1, 21):
                u, v = u0 + (u1 - u0) * i / 21.0, v0 + (v1 - v0) * j / 21.0
                if S.BRepClass_FaceClassifier(f.wrapped, S.gp_Pnt2d(u, v), 1e-9).State() != S.TopAbs_IN: continue
                pr = S.BRepLProp_SLProps(Sf, u, v, 1, 1e-9)
                if not pr.IsNormalDefined(): continue
                nn = pr.Normal(); nv = np.array([nn.X(), nn.Y(), nn.Z()])
                if f.wrapped.Orientation() == S.TopAbs_REVERSED: nv = -nv
                p = Sf.Value(u, v); q = np.array([p.X(), p.Y(), p.Z()]) - nv * 1e-5
                it.Perform(S.gp_Lin(S.gp_Pnt(*q), S.gp_Dir(*(-nv))), 1e-7, 1e5)
                ws = sorted(it.WParameter(m) for m in range(1, it.NbPnt() + 1) if it.WParameter(m) > 1e-7)
                ds.append(ws[0] + 1e-5 if ws else float("inf"))
                if len(ds) >= 9: break
            if len(ds) >= 9: break
        if ds and all(abs(d - t) < tol for d in ds): olc += ds
        else: kalan.append(dict(h, izgara=[round(d, 4) for d in ds]))
    k2 = dict(k, hata=kalan, gecti=not kalan, izgara_yuz=len(k["hata"]) - len(kalan),
              not_="h3_sac_v1.kalinlik_denetle: 9 sabit örnek noktası açıklığa düştü → ızgara (21 × 21) örneklemesiyle ölçüldü (h3_fu_sac_v1._kalinlik_izgara)")
    if olc: k2["olcum_min"], k2["olcum_max"] = round(min([k["olcum_min"] or olc[0]] + olc), 5), round(max([k["olcum_max"] or olc[0]] + olc), 5)
    r["kalinlik"] = k2
    return k2


# =====================================================================================================================================
# 9 · KUR
# =====================================================================================================================================
def kur(log=print):
    if G.kuruldu: return G
    t0 = time.time()
    G.g = GO.Govde("F_UST_KABIN", SURUM, istasyon="F", cerceve=GO.Cerceve("FU"))
    G.BIRIM, G.MODUL, G.KAPAK, G.P, G.M8, G.ELK, G.HESAP = {}, {}, {}, {}, [], [], {}
    with bolum("F_UST_KABIN"): f_cerceve()
    f_kutu()
    f_baglantilar()
    davlumbaz()
    for k in ("a", "f", "ke"):
        u_kutu(k)
    u_raf("f"); u_raf("ke")
    for k in ("a", "f", "ke"):
        u_baglantilar(k)
    f_kapaklar()
    baglantilar()
    _elk_delikleri(log)
    G.g.doner_guncelle()
    for s in G.g.SAC:
        if s.ad in KALINLIK_IZGARA:
            k2 = _kalinlik_izgara(s)
            if k2 is not None: G.g.not_("%s kalınlık: %d yüz ızgara örneklemesiyle ölçüldü (%s)" % (s.ad, k2["izgara_yuz"], "GEÇTİ" if k2["gecti"] else "KALDI"))
    G.kuruldu = True
    g = G.g
    log("%s · kuruldu: %d sac · %d profil · %d eleman · %d kaynak · %d birleşim · %d arayüz · %d kapak · %.1f sn"
        % (SURUM, len(g.SAC), len(g.PROF), len(g.ELEMAN), len(g.KAYNAK), len(g.BIRLESIM), len(g.ARAYUZ), len(g.KAPAK), time.time() - t0))
    return G


# =====================================================================================================================================
# 10 · MONTAJ SÖZLEŞMESİ (FU.PARCALAR / UD.PARCALAR · dünya · ad · wp · mal · birim · grup · bom)
# =====================================================================================================================================
def kapakla_doner(ad):
    kur()
    return G.g.kapakla_doner(ad)


def _grup(ad):
    if not G.g.kapakla_doner(ad): return "SABIT"
    k = G.g.DONER.get(ad, "")
    return "KAPAK_F_SOL" if k.endswith("_sol") else "KAPAK_F_SAG"


def govde_parcalari(modul=None):
    """montaja girecek gövde parçaları (arayüz HARİÇ) · dünya koordinatı · modul 'FU' / 'UD' / None (hepsi)"""
    kur()
    out = []
    for q in GO.govde_parcalari(G.g):
        b = birim_bul(q["ad"])
        assert b is not None, ("birimsiz parça", q["ad"])
        m = FU_BIRIMLER[b]
        if modul and m != modul: continue
        q["birim"], q["grup"], q["modul"] = b, _grup(q["ad"]), m
        out.append(q)
    return out


def _uygula(L, yeni, eski, isaret, onek, rapor, etiket):
    if any(p["ad"] == isaret for p in L): return L
    var = set(p["ad"] for p in L)
    eksik = [a for a in eski if a not in var]
    eski = [a for a in eski if a in var]
    GO.uygula(L, yeni, eski, isaret, onekler=onek, rapor=rapor, etiket=etiket)
    if eksik and rapor is not None: rapor.append("%s: listede zaten olmayan eski ad %d (v3.7 öncesi düşmüş) %s" % (etiket, len(eksik), eksik[:6]))
    return L


def uygula_fu(FU, rapor=None):
    """montaj: FU.kur() SONRASI (v3.6 ön üst kayıt bloğundan ÖNCE) · eski F_UST gövdesi / kapak / davlumbaz kutusu → üretim sacı · idempotent"""
    _uygula(FU.PARCALAR, govde_parcalari("FU"), ESKI_FU, ISARET_FU, ONEK_FU, rapor, "F_UST + davlumbaz")
    yeni_bir = {"F_UST_KABIN": "Fırın üstü kabin (bizim) · ÜRETİM SACI (h3_fu_sac_v1): kaynaklı ön çerçeve 30×30×2 (alt kayıt menteşe taşıyıcı · üst kayıt · dikme · tavan + 2 boyuna kiriş) + "
                                 "1,5 bükümlü L yan saclar (fırın arkasında şeritle 788'e · ön 16,5 / arka 22 / ayak dönüşü) + üst sac + tek parça arka sac (lazer yarık panjur + iç perde, "
                                 "4 rakor) · 3 mm L kulak + PEM FHP-M5 · arka ISO 7380 + PEM SP-M5 · K↔F / TOPPING↔F M8",
                "F_UST_KAPAK": "Fırın üstü + U_F ön kapakları · 2 DÜŞER KANAT 1308–2197 ÇİFT CİDAR (dış tava 1,5 bindirme + TIG · iç tava 1,0 punta) · kanat başına 2 gizli 180° "
                                 "kaldır-çıkar menteşe ön alt kayıt içinde (sanal pivot y 1308 · z 79) · 2 bas-aç U_F ön üst kaydında · 1 çekme gazlı yay (bilyalı mafsal) · hizalı lazer "
                                 "yarık havalandırma · kulp yok",
                "F_DAVLUMBAZ": "Davlumbaz sac kutusu (bizim) · KAYNAKLI SIZDIRMAZ: 2 tek bükümlü L (alt+ön / üst+arka) + 2 tava uç kapağı · iç köşeler sürekli TIG · 2 askı L 40 × 40 × 3 "
                                 "(yan saclara FHP-M6) · atış kanalı 2 L + silikon conta · v3.7 iç donanımı (EN 16282-6 yağ filtresi + karbon + Systemair RS 30-15 fan + dikey kanal) KALIR"}
    FU.BIRIMLER[:] = [(k, yeni_bir.get(k, a)) for k, a in FU.BIRIMLER]
    return FU.PARCALAR


def uygula_ud(UD, rapor=None):
    """montaj: UD.kur() SONRASI (KP.bolge_A_ust / bolge_KE_ust ve _v34_ac(ust_a_taban_sac) YERİNE) · U_A / U_F / U_KE gövdeleri + rafları → üretim sacı (kapaksız) · idempotent"""
    _uygula(UD.PARCALAR, govde_parcalari("UD"), ESKI_UD, ISARET_UD, ONEK_UD, rapor, "U_A + U_F + U_KE")
    yeni_bir = {"U_A_GOVDE": "Üst depo A · ÜRETİM SACI: taban tepsisi 1,5 (632 × 803 açıklık · A ile tek hacim) + tam boy yan saclar + üst sac + arka sac + ön alt / üst kayıt + tavan kirişi · "
                               "önü A kapağıyla kapanır (v3.7) · U_A→A M8 (A üst kuşağı) · TOPPING M8",
                "U_F_GOVDE": "Üst depo F · ÜRETİM SACI: taban tepsisi (baca geçişi · DIN 929 → F_UST · ana pano kaynak saplamaları) + yanlar + üst sac (baca ağzı + flanş delikleri) + "
                               "arka sac (4 fan ızgarası) + kayıtlar (üst kayıtta F kanatlarının bas-açları) + 2 tavan kirişi + kutu rafı tepsisi + 3 taşıyıcı · önü F kanatları",
                "U_KE_GOVDE": "Üst depo K + E · ÜRETİM SACI: taban tepsisi (Harting kesikleri · DIN 929 → K / E) + yanlar + üst sac + arka sac + kayıtlar + 2 tavan kirişi + içecek rafı tepsisi + "
                                "4 taşıyıcı · önü K ve E kapaklarıyla kapanır (v3.7)"}
    UD.BIRIMLER[:] = [(k, yeni_bir.get(k, a)) for k, a in UD.BIRIMLER]
    return UD.PARCALAR


def dunya_listesi(L):
    return L                                                                  # FU / UD dünya koordinatlı


def kapak_dunya(L, tr=None):
    """kapakla dönen parçaların bileşiği (tr 'sol' / 'sag' / None)"""
    kur()
    f = lambda a: G.g.kapakla_doner(a) and (tr is None or G.g.DONER.get(a, "").endswith("_" + tr))
    return cq.Compound.makeCompound([GO._sekil(p) for p in L if f(p["ad"])])


ESLEME = {}
for _y in ("sol", "sag"):
    ESLEME.update({"onyuz_f_ust_kapak_%s_omega_0" % _y: "onyuz_f_ust_kapak_%s_ic_tava (çift cidar · omega yok)" % _y,
                   "onyuz_f_ust_kapak_%s_omega_1" % _y: "onyuz_f_ust_kapak_%s_ic_tava" % _y,
                   "onyuz_f_ust_kapak_%s_burulma_kutusu" % _y: "onyuz_f_ust_kapak_%s_ic_tava (çift cidarlı kapak burulmayı taşır)" % _y,
                   "onyuz_f_ust_kapak_%s_yay_pimi" % _y: "onyuz_f_ust_kapak_%s_gazli_yay_pim_b" % _y,
                   "onyuz_f_ust_kapak_%s_tipon_plakasi" % _y: "onyuz_f_ust_kapak_%s_karsilik_0" % _y,
                   "onyuz_f_ust_bas_ac_%s" % _y: "onyuz_f_ust_kapak_%s_basac_0 (+ _1) · U_F ön üst kaydı içinde" % _y,
                   "onyuz_f_ust_gazli_yay_braketi_%s" % _y: "govde_gazli_yay_braketi_%s" % _y,
                   "onyuz_f_ust_gazli_yay_%s_goz_a" % _y: "onyuz_f_ust_gazli_yay_%s_yuva_a" % _y,
                   "onyuz_f_ust_gazli_yay_%s_goz_b" % _y: "onyuz_f_ust_gazli_yay_%s_yuva_b" % _y})
    for _i in (0, 1):
        ESLEME["onyuz_f_ust_mentese_sabit_%s_%d" % (_y, _i)] = "onyuz_f_ust_kapak_%s_mentese_%d_sabit (gizli · kayıt içinde)" % (_y, _i)
        ESLEME["onyuz_f_ust_mentese_hareketli_%s_%d" % (_y, _i)] = "onyuz_f_ust_kapak_%s_mentese_%d_kanat" % (_y, _i)
for _i in (0, 1):
    ESLEME["f_ust_panjur_lamelleri_%d" % _i] = "f_ust_panjur_perdesi_%d (yarıklar f_ust_arka_sac'ta)" % _i
for _a in ESKI_UD:
    if re.match(r"onyuz_ust_a_(kapak|mentese|bas_ac)", _a): ESLEME[_a] = "onyuz_kapak_A (AK · v3.7 A kapağı tavana)"
    elif re.match(r"onyuz_ust_f_(kapak|mentese|bas_ac)", _a): ESLEME[_a] = "onyuz_f_ust_kapak_%s (F kanadı 1308–2197)" % ("sag" if "_sag" in _a else "sol")
    elif re.match(r"onyuz_ust_ke_(kapak|mentese|bas_ac)", _a): ESLEME[_a] = "onyuz_kapak_K / onyuz_kapak_E_ust_* (v3.7 K ve E kapakları tavana)"


if __name__ == "__main__":
    BUR = os.path.abspath(os.path.join(H3, "..", "..", "..", "..", "sac_fu"))
    sys.path.insert(0, BUR)
    import fu_sac_denetim_v1 as DEN                                           # <scratchpad>/sac_fu/fu_sac_denetim_v1.py (denetim + çıktılar)
    DEN.calistir()
    sys.stdout.flush(); os._exit(0)
