# -*- coding: utf-8 -*-
"""h3_u_sac_v1 — ÜST DOLAPLAR (U_F · U_KE) + FIRIN ÜSTÜ KABİN (F_UST_KABIN) GÖVDESİ · ÜRETİM SACI v1 (4 Eki 2026 · Claude · GECE 2 ADIM 5b · YEREL ·
montaja bağlı DEĞİL)

Kemal: "üretim sacını yap ama tam yap, üretime yönelik" — sac atölyesi doğrudan 3B'den üretir (açınım JSON + parça listesi CSV · pafta yok).
STANDART: h3_k_sac_v1 (K pilotu) · h3_sac_v1 (gerçek abkant bükümü: R 1,5t · K 0,45 · büküm payı · köşe/uç rahatlatma) · h3_govde_ortak_v1 ·
          sac_kararlar_v1.json · h3_e_sac_v1 (ProfilD · kulak · bağlantı yardımcıları).
REFERANS (bugünkü gövde, şekil/ölçü AYNI): hat3_v8zq.glb U_F_GOVDE__* · U_KE_GOVDE__* · F_UST_KABIN__* · F_DAVLUMBAZ__sac (bölme duvarı) ·
          kuruluş betikleri u_govde_yeni.py (v8u) + f_kabin_yeni.py (v8v) · elektrik: elk3/tasarim.py (J1 / J2 birleşim paneli, U_F gömme giriş cebi).
KOORDİNAT: DÜNYA (U ve F üst kabin modülleri dünyada kurulu, öteleme yok) · x hat boyunca · y yukarı · z ön +59 / arka −830.

U_F + U_KE (her kutu x0–x1 · y 1862–2200 · z −830…+59; içerik / komşular değişmez)
  ALT GÖVDE KAYNAKLI: TABAN 1,5 (düz = raf · koli / kutu doğrudan üstünde) + SOL / SAĞ YAN 1,5 (ön + arka 16,5 iç dönüş) → iç köşe aralıklı TIG
     (40 / 200, görünmez) · tavan + arka SÖKÜLEBİLİR (FHP gömme saplama, somun içeriden; dış yüzde iz yok).
  TAVAN 430 1,5: dört kenar aşağı dönüş (yan / arka 21,5 · ön 31,5 = eski ön kayıt yerine) · köşeler açık + kare rahatlatma · yan saclar arasına oturur.
  TAVAN OMEGASI 304 1,2 (iki büküm + iki kanat) tavanın altına punta · U_F x 3325 (pano toplama kanalı askıları) · U_KE x 4615.
  ARKA 1,5: alt iç dönüş (tabana FHP) · yan dönüşlere + tavan arka dönüşüne FHP · U_F: 4 fan ızgarası (9 × 100 × 6 yarık) + GÖMME GİRİŞ CEBİ
     (1,5 tava: taban + 4 duvar + 3 kenar flanşı, arka sacın iç yüzüne FHP · tabanda 4 rakor deliği) — cep sol duvarı 11,5 sola alındı (bina
     rakoru Ø22 duvara 1 mm'deydi → DFM 5,25).
  U ↔ istasyon tavanı: tabanda Ø9 + ISO 7380 M8 (içeriden) → istasyon tavanında PEM SP-M8 (F üst kabin: bu üreteç · E: h3_e_sac_v1 · K: ARAYÜZ).
  U_F ↔ U_KE: komşu yan saclar arasında ISO 4762 M8 + pul + fiberli somun.
F_UST_KABIN (fırın üstü kabin x 2500–4000 · y 788–1862)
  KAYNAKLI ÇERÇEVE (tek parça gelir): SOL + SAĞ YAN 1,5 (alt bölümde fırın gövdesi için z −651'e kadar, üstte tam derinlik · arka / ön dönüş) +
     304 kare boru 30 × 30 × 2: 3 alt profil (ön / orta / arka, y 1316,5–1346,5) · ön üst kayıt (y 1830,5–1860,5) · ön orta dikme + tavan kirişi
     (dikmeye kaynaklı) — profil uçları yan saclara köşe dikişi · KESİM LİSTESİ CSV'de.
  DÜZ TABAN 1,5 (y 1346,5–1348) profillere delik kaynağı (25 × 8 yarık, yüz taşlanır) · ALTINDA 20 mm TAŞ YÜNÜ (A1, ≥ 100 kg/m³) iki gözde ·
     0,5 mm 304 KILIF TAVASI (dört kenar 20 yukarı dönüş, profillere / yan saclara kör perçin Ø3,2) → taş yünü görünmez · rakor kovanı Ø25,4.
  ORTA BÖLME 1,5 (davlumbaz ön duvarı, z −441,5…−440): yan dönüşler yan saclara FHP · 9 emiş yarığı · hava borusu Ø12 · kiriş çentiği.
  TAVAN 1,5: yan dönüşler · atış kanalı ağzı 297 × 197 (davlumbaz → U_F bacası, kanal içeriden geçer) · V1 iniş çentiği · U_F için 4 × PEM SP-M8.
  ARKA 1,5: üst iç dönüş (tavana FHP) · 2 panjur grubu (8 yarık 170 × 12 + iç lamel 12 × 1,5, dikiş kaynak) · 4 rakor deliği.
  J1 / J2 birleşim panelleri: yan saclarda ağız 67 × 57 + 4 burç saplaması (FHP-M5, arayüz) · K ↔ F M8 Ø9 (sağ yan).
DUVARA DEĞEN HER MEKANİZMA / ELEKTRİK PARÇASINA FHP saplama deliği (ARAYÜZ: karşı parçada Ø5,5) — h3_e_sac_v1.mekanizma_saplamalari ile aynı kural.
ÇIKTI (yalnız <scratchpad>/gece2/adim5): U_sac_v1.glb · U_parca.csv · acinim_U/*.json · U_denetim.json. Ana GLB'ye / sayfaya YAZMAZ."""
import math, os, sys, json, time, re, collections, pickle
H3 = os.path.dirname(os.path.abspath(__file__)); _U = os.path.dirname(H3)
for _p in (_U, H3):
    if _p not in sys.path: sys.path.insert(0, _p)
import numpy as np
import cadquery as cq
import h3_sac_v1 as S
import h3_govde_ortak_v1 as GO
import h3_e_sac_v1 as E

SURUM = "h3_u_sac_v1"
assert S.STD.dosyalar, ("sac standardı okunamadı: AUTOKITCH_SAC_STANDART → <scratchpad>/sac_standart", S._STD_KLASOR)
V = cq.Vector
T = 1.5
Y0, YT = 1862.0, 2200.0
ZA, ZAI, ZO = -830.0, -828.5, 59.0
FL = 16.5                                                     # yan dönüş dış ölçüsü (x0 → x0 + 16,5)
U_KUTU = {"F": dict(x0=2500.0, x1=4000.0, omega=3325.0, gecis_sol=(2104.0, 2169.0, -820.0, -689.0), gecis_sag=(2142.0, 2166.0, -820.0, -765.0), basac=(2510.0, 3990.0),
                    baca=(2950.0, 3250.0, -720.0, -520.0), tavan_baca=(2951.5, 3248.5, -718.5, -521.5), v1=(3930.0, 3996.0, -826.0, -786.0),
                    fan=((3660.0, 1930.0), (3860.0, 1930.0), (2640.0, 2075.0), (2820.0, 2075.0)), cep=(3915.0, 3983.0, 2081.5, 2166.5, -790.0)),
          "KE": dict(x0=4000.0, x1=5230.0, omega=4615.0, gecis_sol=(2142.0, 2166.0, -820.0, -765.0), gecis_sag=None, basac=None, baca=None, tavan_baca=None, v1=None,
                     fan=(), cep=None, harting=((4267.0, 4333.0, -778.0, -742.0), (5067.0, 5133.0, -778.0, -742.0)))}
CEP_DELIK = dict(bina=(3940.0, 2146.0, 22.0), bina_v=(3967.0, 2146.0, 10.7), zemin=(3942.0, 2118.0, 17.0), zemin_v=(3966.0, 2118.0, 10.7))   # elk3 GECIS (r + 1)
UF_F_M8 = ((2580.0, -790.0), (2580.0, 0.0), (3250.0, 0.0), (3900.0, 0.0))        # U_F ↔ F üst kabin
UKE_E_M8 = ((4500.0, -700.0), (4815.0, -700.0), (5130.0, -700.0))                 # U_KE ↔ E (h3_e_sac_v1.U_M8 dünya)
UKE_K_M8 = ((4100.0, -700.0), (4300.0, -700.0))                                   # U_KE ↔ K (K tavanında SP-M8 gerekir · ARAYÜZ)
UF_UKE_M8 = ((1950.0, 40.0), (2110.0, 40.0), (2030.0, -560.0))                   # U_F sağ ↔ U_KE sol (y, z)
# F üst kabin
FX0, FX1 = 2500.0, 4000.0
FY0, FYT, FYTV = 788.0, 1862.0, 1860.5
F_ON_Y = 1305.0                                               # yan sacın tam derinlik başladığı kot (altında fırın gövdesi önde)
PRF = 30.0
YP0, YP1 = 1316.5, 1346.5                                     # alt profiller
YT0, YT1 = 1346.5, 1348.0                                     # taban levhası
PRO_Z = {"on": (27.0, 57.0), "orta": (-455.75, -425.75), "arka": (-826.5, -796.5)}   # arka: v8zq −828,5 → −826,5 (yan arka dönüşünün önünde, 0,5 hava)
YAL = 20.0
RAKOR = (3460.0, -780.15)
V2 = (2890.0, 2930.0, -796.0, -756.0)                         # F V2 kablo kanalı (elk3 F_V2: x 2890–2930 · z −796…−756) taban levhasından geçer                                     # davlumbaz fanı kablo rakoru (taban Ø16,5 · kovan Ø25,4)
BOLME_Z = (-441.5, -440.0)
EMIS = [(xa, yr) for yr in (1520.0, 1620.0, 1720.0) for xa in (3390.0, 3590.0, 3790.0)]   # 160 × 10
KIRIS_X = (3326.0, 3356.0)
F_RAKOR = ((2560.3, 860.0, 32.4), (2630.2, 830.0, 20.1), (3689.2, 1825.0, 20.1), (2600.2, 1825.0, 20.1))
PANJUR = dict(x=((2555.0, 2725.0), (3775.0, 3945.0)), y0=894.0, adim=22.0, n=8, h=12.0)
J1 = dict(c=-715.0, x=FX0); J2 = dict(c=-615.0, x=FX1)
K_F_M8 = ((1000.0, -800.0), (1825.0, -800.0), (1700.0, 42.0), (877.0, -720.0))   # h3_k_sac_v1.M8_F → F sağ yanında Ø9
ESKI = dict(U_F_GOVDE=("ust_f_taban_sac", "ust_f_yan_sol", "ust_f_yan_sag", "ust_f_arka_sac", "ust_f_tavan_sac", "ust_f_tavan_omegasi_0"),
            U_KE_GOVDE=("ust_ke_taban_sac", "ust_ke_yan_sol", "ust_ke_yan_sag", "ust_ke_arka_sac", "ust_ke_tavan_sac", "ust_ke_tavan_omegasi_0"),
            F_UST_KABIN=("f_ust_yan_sol", "f_ust_yan_sag", "f_ust_tavan_sac", "f_ust_arka_sac", "f_ust_panjur_lamelleri_0", "f_ust_panjur_lamelleri_1",
                         "f_ust_alt_profil_on", "f_ust_alt_profil_orta", "f_ust_alt_profil_arka", "f_ust_taban_levhasi", "f_ust_taban_yalitimi_on",
                         "f_ust_taban_yalitimi_arka", "f_ust_taban_yalitim_kilifi_on", "f_ust_taban_yalitim_kilifi_arka", "f_ust_taban_rakor_kovani",
                         "onyuz_f_ust_ust_kayit", "onyuz_f_ust_dikme_0", "f_davlumbaz_bolme_duvari"))
MEK_HARIC = re.compile(r"^(U_F_GOVDE__(sac|paslanmaz)|U_KE_GOVDE|F_UST_KABIN__(sac|yalitim|paslanmaz)|F_DAVLUMBAZ__sac|E_GOVDE|K_GOVDE|TOPPING_MODUL|F_TP10|ZEMIN|U_F_BACA|U_F_HAVALANDIRMA__paslanmaz)"
                       r"|karton|__hava|kablo|conta|yigin")
# ADIM 8 (4 Eki 2026) · entegrasyonda (zincir 36, sac_ent saplama boyu denetimi) engel yüzünden çıkarılan FHP saplamalar: kur() SONUNDA
# E.saplama_duzelt() ile kaldırılır (saplama + sacdaki PEM deliği) · diğer saplamaların yeri ve adları birebir aynı kalır.
SAPLAMA_CIKAR = {
    "arayuz_mek_ust_f_taban_sac_0": "ana pano ayak lamasının (4 mm) tamamı pano kutusunun altında (pano 4,5 mm'de)",
    "arayuz_mek_ust_f_taban_sac_1": "ana pano ayak lamasının (4 mm) tamamı pano kutusunun altında (pano 4,5 mm'de)",
    "arayuz_mek_ust_f_taban_sac_2": "ana pano ayak lamasının (4 mm) tamamı pano kutusunun altında (pano 4,5 mm'de)",
    "arayuz_mek_ust_f_taban_sac_3": "ana pano ayak lamasının (4 mm) tamamı pano kutusunun altında (pano 4,5 mm'de)",
    "arayuz_baca_flansi_2935_620": "eski v8zq baca flanşı (yalıtım 4,5 mm'de) · zincir 38'de F üreteci bacayı yeniler, flanşı U_F tavanına 8 × M6 ile kendisi bağlar",
    "arayuz_baca_flansi_3265_620": "eski v8zq baca flanşı · F üreteci 8 × M6 ile bağlar",
    "arayuz_baca_flansi_3100_505": "eski v8zq baca flanşı · F üreteci 8 × M6 ile bağlar",
    "arayuz_baca_flansi_3100_735": "eski v8zq baca flanşı · F üreteci 8 × M6 ile bağlar",
    "arayuz_j1_burc_1476_769": "J1 üst burç · 23,5 mm'de ELK_ZINCIR etiketi (burç yeri elektrik modelinde sabit; panel alt 2 burçla tutulur)",
    "arayuz_j1_burc_1594_769": "J1 üst burç · 23,5 mm'de Harting (panel alt 2 burçla tutulur)",
    "arayuz_j2_burc_1476_669": "J2 üst burç · 23,5 mm'de ELK_ZINCIR etiketi (panel alt 2 burçla tutulur)",
    "arayuz_j2_burc_1594_669": "J2 üst burç · 23,5 mm'de Harting (panel alt 2 burçla tutulur)",
    "arayuz_mek_f_ust_tavan_sac_8": "hava hortumu askısı tepe tablası 14 × 14 · ortasından askı laması iniyor (3,5 mm'de), taşınacak serbest yer yok",
    "arayuz_mek_f_ust_tavan_sac_9": "hava hortumu askısı tepe tablası 14 × 14 · ortasından askı laması iniyor (3,5 mm'de), taşınacak serbest yer yok",
    "arayuz_mek_f_ust_taban_levhasi_18": "davlumbaz taşıyıcı lamasının tamamı davlumbaz gövdesinin altında (6 mm'de)",
    "arayuz_mek_f_ust_taban_levhasi_19": "davlumbaz taşıyıcı lamasının tamamı davlumbaz gövdesinin altında (6 mm'de)",
    "arayuz_mek_f_ust_taban_levhasi_22": "davlumbaz taşıyıcı lamasının tamamı davlumbaz gövdesinin altında (6 mm'de)",
    "arayuz_mek_f_ust_taban_levhasi_23": "davlumbaz taşıyıcı lamasının tamamı davlumbaz gövdesinin altında (6 mm'de)",
}
# taşınan: fan braketi (U_F_HAVALANDIRMA__celik 70 × 34) ortasında plastik gövde (x 3343–3376) → iki uçtaki serbest banda ikiye bölünür
# (braket başka saplamayla tutulmuyordu) · (dünya ekseni, yeni değer) · aynı duvar düzlemi
SAPLAMA_TASI = {"arayuz_mek_ust_f_arka_sac_6": ((0, 3334.0), (0, 3386.0))}


def kutu(*a): return GO.kutu(*a)


def donus_centigi(P, kenar, w0, w1, derin=40.0, tip="donus_centigi", parca=""):
    """P panelinin 'kenar'ındaki büküm + flanşı w0–w1 aralığında keser (açınımda kenardan dışarı 'derin' kadar) · kenara açık çentik (dfm dışı)"""
    kn = P.kenar(kenar); q = lambda w, s_: tuple(kn["p0"] + kn["e2"] * w + kn["out2"] * s_)
    return P.kesik([q(w0, -0.5), q(w1, -0.5), q(w1, derin), q(w0, derin)], tip=tip, dfm=False, parca=parca)


def ozel_kati(g, ad, sh, tanim, olcu, malzeme, tur="sac", mal="sac", meta=None):
    p = g.ozel(ad, sh, "özel", tanim, olcu, malzeme=malzeme, mal=mal, uretim=True, tur=tur, meta=meta)
    g.eleman(p, mal=mal)
    return p


# =====================================================================================================================================
# 1 · U KUTUSU (U_F · U_KE)
# =====================================================================================================================================
def u_kutu(g, kod):
    k = U_KUTU[kod]; c = kod.lower(); x0, x1 = k["x0"], k["x1"]
    P = {}
    # --- taban (raf) · x0+1,5 … x1−1,5 · arka kenarı arka sacın dış yüzüyle aynı (z −830)
    tb = g.sac("ust_%s_taban_sac" % c, "dis")
    Tb = tb.taban([(x0 + T, -ZO), (x1 - T, -ZO), (x1 - T, -ZA), (x0 + T, -ZA)], O=(0, Y0, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="taban")   # n = +y
    if k["baca"]:
        a0, a1, b0, b1 = k["baca"]; Tb.dikdortgen((a0 + a1) / 2.0, -(b0 + b1) / 2.0, a1 - a0 + 1.0, b1 - b0 + 1.0, r=0.5, tip="baca_acikligi", parca="baca kanalı geçişi 301 × 201 (kanal 300 × 200)")
    if k["v1"]:
        a0, a1, b0, b1 = k["v1"]; Tb.dikdortgen((a0 + a1) / 2.0, -(ZA + b1 + 0.5) / 2.0, a1 - a0 + 1.0, b1 + 0.5 - ZA + 0.2, tip="v1_centigi", dfm=False,
                                                   parca="pano V1 kablo kanalı iniş çentiği (arka kenara açık)")
    for h in k.get("harting", ()):
        a0, a1, b0, b1 = h; Tb.dikdortgen((a0 + a1) / 2.0, -(b0 + b1) / 2.0, a1 - a0, b1 - b0, r=2.0, tip="harting_kesigi", parca="Harting Han 10B soket ağzı 66 × 36")
    P["taban"] = Tb
    # --- yan saclar (y 1862–2200 · tabanın kenarını örter · ön + arka iç dönüş)
    for tr, xs in (("sol", x0), ("sag", x1)):
        s = g.sac("ust_%s_yan_%s" % (c, tr), "dis", kabuk=True); gg = s.R + s.t
        if tr == "sol":
            Y = s.taban([(Y0, ZAI + gg), (YT, ZAI + gg), (YT, ZO - gg), (Y0, ZO - gg)], O=(xs, 0, 0), ex=(0, 1, 0), ey=(0, 0, 1), ad="yan"); zv = lambda z: z
            ka, ko = 0, 2
            arka = Y.flans(ka, FL, yon=+1, bas=T, son=YT - 2175.0, ad="arka_donus")
            on = Y.flans(ko, FL, yon=+1, bas=YT - (2128.0 if k["basac"] else 2165.0), son=T, ad="on_donus")
        else:
            Y = s.taban([(Y0, -ZO + gg), (YT, -ZO + gg), (YT, -ZAI - gg), (Y0, -ZAI - gg)], O=(xs, 0, 0), ex=(0, 1, 0), ey=(0, 0, -1), ad="yan"); zv = lambda z: -z
            ka, ko = 2, 0
            arka = Y.flans(ka, FL, yon=+1, bas=YT - 2175.0, son=T, ad="arka_donus")
            on = Y.flans(ko, FL, yon=+1, bas=T, son=YT - (2128.0 if k["basac"] else 2165.0), ad="on_donus")
        gc = k["gecis_sol"] if tr == "sol" else k["gecis_sag"]
        if gc:
            a0, a1, b0, b1 = gc
            Y.dikdortgen((a0 + a1) / 2.0, zv((b0 + b1) / 2.0), a1 - a0, b1 - b0, r=2.0, tip="hat_gecisi", parca="ana hat kanal geçişi (v8zq · arka kenarı dönüşten 7 mm'ye çekildi)")
        if k["basac"]:
            g.not_("ust_%s_yan_%s: ön dönüş y 2128'de biter — F kapağı bas-aç gövdesi (y 2130–2150) dönüşün üstünden geçer" % (c, tr))
        P[tr] = dict(yan=Y, arka=arka, on=on, s=s)
    # --- alt gövde kaynakları (taban ↔ yan, iç köşe, aralıklı 40 / 200)
    for tr, xs, nx in (("sol", x0 + T, 1.0), ("sag", x1 - T, -1.0)):
        for z in (-780.0, -580.0, -380.0, -180.0, -40.0):
            g.kaynak(S.kaynak_dikisi((xs, Y0 + T, z), (xs, Y0 + T, z + 40.0), (nx, 0, 0), (0, 1.0, 0), 1.5, ad="ust_%s_taban_yan_kaynagi_%s_%d" % (c, tr, int(-z)),
                                     birim=g.birim, taraf="iç (aralıklı 40 / 200)", not_="taban ↔ yan sac"))
    # --- tavan (430) · yanlar arasında · dört kenar aşağı
    s = g.sac("ust_%s_tavan_sac" % c, "dis", malzeme="AISI 430 (1.4016) 2B"); gg = s.R + s.t
    Tv = s.taban([(x0 + T + gg, -ZO + gg), (x1 - T - gg, -ZO + gg), (x1 - T - gg, -ZAI - gg), (x0 + T + gg, -ZAI - gg)], O=(0, YT - T, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="tavan")
    fo = Tv.flans(0, 31.5, yon=-1, ad="on_donus"); fs = Tv.flans(1, 21.5, yon=-1, ad="sag_donus")
    fa = Tv.flans(2, 21.5, yon=-1, ad="arka_donus"); fl = Tv.flans(3, 21.5, yon=-1, ad="sol_donus")
    for f1, f2 in ((fo, fs), (fs, fa), (fa, fl), (fl, fo)): s.kose(f1, f2, "acik", rahat="kare")
    if k["tavan_baca"]:
        a0, a1, b0, b1 = k["tavan_baca"]; Tv.dikdortgen((a0 + a1) / 2.0, -(b0 + b1) / 2.0, a1 - a0, b1 - b0, r=2.0, tip="baca_acikligi", parca="baca kanalı ağzı 297 × 197 (flanş altta)")
    P["tavan"] = dict(tavan=Tv, on=fo, sag=fs, arka=fa, sol=fl, s=s)
    # --- omega (1,2) tavanın altına punta
    # omega: 30 taç × 20 yükseklik dar şapka düz bıçakla bükülemiyor (abkant denetimi: hiçbir sırada temiz değil) → HADDELENMİŞ HAZIR OMEGA PROFİL
    # (304 · 1,2 · 60 × 20 · taç 30) boyuna kesilir; geometri aynı (açınım hesabı yalnız kesim boyu için)
    om = S.Sac("ust_%s_tavan_omegasi_0" % c, rol="ic", birim=g.birim, kaynak=SURUM); go = om.R + om.t; xc = k["omega"]
    Om = om.taban([(xc - 15.0 + go, -54.5), (xc + 15.0 - go, -54.5), (xc + 15.0 - go, 824.0), (xc - 15.0 + go, 824.0)], O=(0, 2178.0, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="tac")
    w1 = Om.flans(1, 20.0, yon=+1, ad="sag_ag"); w3 = Om.flans(3, 20.0, yon=+1, ad="sol_ag")
    w1.flans(1, 15.0, yon=-1, ad="sag_kanat"); w3.flans(1, 15.0, yon=-1, ad="sol_kanat")
    osh = om.kati(); ob = osh.BoundingBox()
    osh = osh.translate(cq.Vector(0, (YT - T - 0.02) - ob.ymax, 0))                # kanat üstü tavana değer (0,02 · punta)
    ozel_kati(g, "ust_%s_tavan_omegasi_0" % c, osh, "Omega profil AISI 304 haddelenmiş 1,2 · taç 30 · yükseklik 20 · kanat 15 (hazır profil, boy kesim) · tavana punta ≈150",
              "L %.0f" % (ob.zmax - ob.zmin), "AISI 304", tur="profil", mal="sac")
    s.punta(s, [(xc + sg * 22.5, YT - T, z) for sg in (-1, 1) for z in np.arange(-780.0, 40.0, 150.0)], not_="omega kanatları → tavan alt yüzü (≈150 aralık)")
    # --- arka sac (alt iç dönüş tabana)
    s = g.sac("ust_%s_arka_sac" % c, "dis"); gg = s.R + s.t
    A = s.taban([(x0, Y0 + T + gg), (x1, Y0 + T + gg), (x1, YT), (x0, YT)], O=(0, 0, ZA), ex=(1, 0, 0), ey=(0, 1, 0), ad="arka")    # n = +z
    alt = A.flans(0, 24.0, yon=+1, bas=18.5, son=(x1 - k["v1"][0] + 6.0) if k["v1"] else 18.5, ad="alt_donus")
    for (xf, yf) in k["fan"]:
        for j in range(9):
            A.dikdortgen(xf, yf - 48.0 + 12.0 * j, 100.0, 6.0, r=2.5, tip="fan_izgarasi", parca="fan ızgarası yarığı 100 × 6 (9 sıra)")
    if k["cep"]:
        a0, a1, b0, b1, _z = k["cep"]
        A.dikdortgen((a0 + a1) / 2.0, (b0 + b1) / 2.0, a1 - a0, b1 - b0, r=1.0, tip="giris_cebi_agzi", parca="gömme giriş cebi ağzı (cep tavası içeriden)")
    P["arka"] = dict(arka=A, alt=alt, s=s)
    g.PANEL[kod] = P
    # --- bağlantılar
    for tr, xx in (("sol", x0 + 10.5), ("sag", x1 - 10.5)):
        for y in ((2060.0, 2165.0) if (tr == "sag" and k["v1"]) else (1890.0, 2030.0, 2150.0)):
            E.bag(g, A, P[tr]["arka"], (xx, y, ZA), "govde_%s_bag_arka_%s_%d" % (c, tr, int(y)), boy=10)
    xs_ = [x for x in E.dizi(x0 + 40.0, x1 - 40.0, maks=200.0, uc=10.0) if abs(x - k["omega"]) > 40]
    for x in xs_:
        E.bag(g, A, P["tavan"]["arka"], (x, 2186.0, ZA), "govde_%s_bag_tavan_arka_%d" % (c, int(x)), boy=10)
    fanx = [(xf - 65.0, xf + 65.0) for xf, yf in k["fan"]]
    for x in E.dizi(x0 + 60.0, x1 - 60.0, maks=200.0, uc=10.0):
        if any(a <= x <= b for a, b in fanx) or (k["v1"] and k["v1"][0] - 10 <= x <= k["v1"][1] + 10): continue
        E.bag(g, Tb, alt, (x, Y0, -815.0), "govde_%s_bag_taban_arka_%d" % (c, int(x)))
    for tr, xs in (("sol", x0), ("sag", x1)):
        for z in E.dizi(-800.0, 40.0, maks=200.0, uc=10.0):
            E.bag(g, P[tr]["yan"], P["tavan"][tr], (xs, 2189.0, z), "govde_%s_bag_tavan_%s_%d" % (c, tr, int(-z)))
    return P


def giris_cebi(g):
    """U_F arka sacında GÖMME GİRİŞ CEBİ: 1,5 tava (taban z −791,5…−790 · 4 duvar · sol / üst / alt flanş arka sacın iç yüzünde) · 4 rakor deliği"""
    a0, a1, b0, b1, zt = U_KUTU["F"]["cep"]
    s = g.sac("ust_f_giris_cebi", "dis"); gg = s.R + s.t
    C = s.taban([(a0 + gg, -b1 + gg), (a1 - gg, -b1 + gg), (a1 - gg, -b0 - gg), (a0 + gg, -b0 - gg)], O=(0, 0, zt), ex=(1, 0, 0), ey=(0, -1, 0), ad="taban")   # n = −z
    w = [C.flans(i, zt - ZAI, yon=+1, ad=a) for i, a in enumerate(("ust_duvar", "sag_duvar", "alt_duvar", "sol_duvar"))]
    for i in range(4): s.kose(w[i], w[(i + 1) % 4], "acik", rahat="kare")
    rim = {}
    for i, a in ((2, "alt_flans"), (3, "sol_flans")):
        rim[a] = w[i].flans(1, 20.0, yon=-1, ad=a)
    for nm, (x, y, d) in CEP_DELIK.items():
        C.delik(x, -y, d, tip="rakor_deligi", parca="%s rakoru Ø%g" % (nm, d))
    A = g.PANEL["F"]["arka"]["arka"]
    for a, pts in (("sol_flans", ((a0 - 12.0, 2095.0), (a0 - 12.0, 2124.0), (a0 - 12.0, 2153.0))),
                   ("alt_flans", ((3935.0, b0 - 12.0), (3965.0, b0 - 12.0)))):
        for (x, y) in pts:
            E.bag(g, A, rim[a], (x, y, ZA), "govde_f_bag_cep_%s_%d_%d" % (a, int(x), int(y)), boy=10)
    g.not_("giriş cebi: köşeler açık + TIG (su sızdırmaz, dışta taşlanır) · sağ duvarda flanş yok (yan sacın arka dönüşü 0,5 yanında) · üst duvarda "
           "flanş yok (tavanın arka dönüşü) · "
           "ELK_ZINCIR cep + cep_taban parçalarının yerine geçer · rakorlar (ELK_ZINCIR__rakor) aynı")
    return s


def u_baglantilari(gF, gK, gFU):
    """U_F ↔ F üst kabin (F tavanında SP-M8) · U_KE ↔ E (E üst sacında SP-M8 — h3_e_sac_v1) · U_KE ↔ K (ARAYÜZ) · U_F ↔ U_KE (yan saclar arası)"""
    TbF = gF.PANEL["F"]["taban"]; TbK = gK.PANEL["KE"]["taban"]; TvF = gFU.PANEL["tavan"]["tavan"]
    for x, z in UF_F_M8:
        TbF.delik(x, -z, 9.0, tip="vida_deligi", parca="U_F ↔ F üst kabin M8 (ISO 273 orta)")
        gF.eleman(S.vida("ISO7380", "M8", 16, (x, Y0 + T, z), (0, -1.0, 0), ad="govde_f_m8_firin_%d_%d" % (int(x), int(-z)), birim=gF.birim))
        ps, c, ms = S.pem_somun("SP", "M8", (x, FYTV, z), (0, -1.0, 0), TvF.sac.t, ad="govde_fu_pem_m8_%d_%d" % (int(x), int(-z)), birim=gFU.birim)
        uv = TvF.yerel((x, FYT, z)); TvF.delik(uv[0], uv[1], c["delik"], tip="pem_somun", parca=ps["meta"]["parca"], pem_tip="SP", kenar_min=c["kenar"], min_sac=ms)
        gFU.eleman(ps)
    for x, z in UKE_E_M8:
        TbK.delik(x, -z, 9.0, tip="vida_deligi", parca="U_KE ↔ E M8 (E üst sacında PEM SP-M8 · h3_e_sac_v1)")
        gK.eleman(S.vida("ISO7380", "M8", 16, (x, Y0 + T, z), (0, -1.0, 0), ad="govde_ke_m8_e_%d" % int(x), birim=gK.birim))
    for x, z in UKE_K_M8:
        TbK.delik(x, -z, 9.0, tip="vida_deligi", parca="U_KE ↔ K M8 (K üst sacında PEM SP-M8 GEREKİR · arayüz)")
        gK.arayuz(S.vida("ISO7380", "M8", 16, (x, Y0 + T, z), (0, -1.0, 0), ad="arayuz_ke_m8_k_%d" % int(x), birim=gK.birim), "K_GOVDE ust_sac",
                  "K üst sacında PEM SP-M8-1 (dünya x %.0f z %.0f) · ISO 7380 M8 × 16 U_KE içinden" % (x, z), "K sahibi")
        gK.KARSI_DELIK.append(dict(etiket="UKE_K_%d" % int(x), karsi="K_GOVDE ust_sac", cap="PEM SP-M8 (Ø10,5)", merkez_dunya=[x, Y0, z]))
    A = gF.PANEL["F"]["sag"]["yan"]; B = gK.PANEL["KE"]["sol"]["yan"]
    for y, z in UF_UKE_M8:
        b = S.vidali_birlesim(A, B, (4000.0, y, z), "somun", dis="M8", vida_std="ISO4762", ad="govde_f_ke_m8_%d_%d" % (int(y), int(-z)), birim=gF.birim)
        for q in b["parcalar"]: gF.eleman(q)
        gF.BIRLESIM.append(b)


# =====================================================================================================================================
# 2 · F ÜST KABİN
# =====================================================================================================================================
def f_yan(g, tr):
    s = g.sac("f_ust_yan_%s" % tr, "dis"); gg = s.R + s.t
    r = ZAI + gg; f = ZO - gg
    pts = [(FY0, r), (FYT, r), (FYT, f), (F_ON_Y, f), (F_ON_Y, -652.0), (1246.0, -652.0), (1246.0, -651.0), (FY0, -651.0)]
    if tr == "sol":
        Y = s.taban(pts, O=(FX0, 0, 0), ex=(0, 1, 0), ey=(0, 0, 1), ad="yan"); zv = lambda z: z
        arka = Y.flans(0, FL, yon=+1, bas=0.0, son=FYT - 1610.0, ad="arka_donus")         # üstü: J1 PD kanalı (y 1618–1648, z −826) → köşebent
        on = Y.flans(2, FL, yon=+1, bas=FYT - 1858.0, son=1625.0 - F_ON_Y, ad="on_donus")      # gazlı yay (y 1337–1612) önde serbest
    else:
        pts = [(p[0], -p[1]) for p in pts][::-1]
        Y = s.taban(pts, O=(FX1, 0, 0), ex=(0, 1, 0), ey=(0, 0, -1), ad="yan"); zv = lambda z: -z
        # ters sırada kenarlar: arka kenar = (FYT, −r) → (FY0, −r) · ön kenar = (F_ON_Y, −f) → (FYT, −f)
        n = len(pts)
        ka = [i for i in range(n) if abs(pts[i][1] + r) < 1e-9 and abs(pts[(i + 1) % n][1] + r) < 1e-9][0]
        ko = [i for i in range(n) if abs(pts[i][1] + f) < 1e-9 and abs(pts[(i + 1) % n][1] + f) < 1e-9][0]
        arka = Y.flans(ka, FL, yon=+1, bas=FYT - 1610.0, son=0.0, ad="arka_donus")         # üstü: J2 PD + V1 kanalı
        on = Y.flans(ko, FL, yon=+1, bas=1625.0 - F_ON_Y, son=FYT - 1858.0, ad="on_donus")
    J = J1 if tr == "sol" else J2
    u0, u1, v0, v1 = E.J3["agiz"]
    Y.dikdortgen(E.J3["Y0"] + (v0 + v1) / 2.0, zv(J["c"] + (u0 + u1) / 2.0), v1 - v0 + 1.0, u1 - u0 + 1.0, r=1.0, tip="j_gecis_agzi",
                 parca="%s birleşim paneli contalı geçiş ağzı 57 × 67" % ("J1" if tr == "sol" else "J2"))
    for (u, v) in E.J3["burc"]:
        y, z = E.J3["Y0"] + v, J["c"] + u
        sx = 1.0 if tr == "sol" else -1.0
        E.fhp_arayuz(g, Y, (J["x"], y, z), (sx, 0, 0), "ELK_ZINCIR %s F paneli burcu" % ("J1" if tr == "sol" else "J2"),
                     "burç Ø10 × 20 + panel plakası Ø5,5 · FHP-M5 × 25 · önde pul + fiberli somun", boy=25, ad="arayuz_%s_burc_%d_%d" % ("j1" if tr == "sol" else "j2", int(y), int(-z)))
    if tr == "sag":
        for nm, y, z, d in (("K tartı kablosu rakoru (G4)", 1387.0, -296.0, 16.5), ("K yağ emiş hortumu contası", 1828.0, -249.85, 20.2),
                            ("K yağ dönüş hortumu contası", 1828.0, -179.85, 18.3)):
            Y.delik(y, zv(z), d, tip="gecis", parca=nm + " Ø%g (K sol sacındaki delikle eş eksen)" % d)
        for y, z in K_F_M8:
            Y.delik(y, zv(z), 9.0, tip="vida_deligi", parca="K ↔ F M8 (K dikmesindeki perçin somun · cıvata F içinden · h3_k_sac_v1.M8_F)")
    g.PANEL[tr] = dict(yan=Y, arka=arka, on=on, s=s)
    return Y


def f_cerceve(g):
    """kaynaklı çerçeve: yan saclar + 3 alt profil + ön üst kayıt + ön orta dikme + tavan kirişi"""
    PR = {}
    for ad, (z0, z1) in PRO_Z.items():
        PR[ad] = g.profil("f_ust_alt_profil_%s" % ad, "x", FX0 + T, FX1 - T, ((YP0 + YP1) / 2.0, (z0 + z1) / 2.0), b=PRF, t=2.0, not_="alt profil (taban taşıyıcı)")
    PR["ust_kayit"] = g.profil("onyuz_f_ust_ust_kayit", "x", FX0 + T, FX1 - T, (FYTV - PRF / 2.0, 42.0), b=PRF, t=2.0, not_="ön üst kayıt")
    xd = (KIRIS_X[0] + KIRIS_X[1]) / 2.0
    PR["dikme"] = g.profil("onyuz_f_ust_dikme_0", "y", YT1, FYTV - PRF, (xd, 42.0), b=PRF, t=2.0, not_="ön orta dikme (kapak ortası)")
    PR["kiris"] = g.profil("f_ust_tavan_kirisi", "z", -804.0, 27.0, (xd, FYTV - PRF / 2.0), b=PRF, t=2.0, not_="tavan kirişi (ön ucu kayda kaynaklı · arka ucu 3 mm tapa)")
    GO.dikme_tapasi(g, PR["kiris"], uc="alt", t=2.0, pah=2.5, ad="f_ust_tavan_kirisi_tapa")
    # profil uçları ↔ yan saclar: köşe dikişi yalnız serbest yüzlerde (üst yüz: taban levhası / tavan · ön: yan sacın ön bükümü · arka: arka bükümü)
    YUZ = {"on": [(0, -1.0, 0)], "orta": [(0, -1.0, 0)], "arka": [(0, -1.0, 0)], "ust_kayit": [(0, -1.0, 0)]}   # diğer yüzler alın (taşlanır)
    PAH = {"on": (53.0, 57.0), "ust_kayit": (53.0, 57.0), "arka": (-826.5, -822.5)}       # yan sac bükümü (iç R 2,25) profil köşesine girer → uç köşesi 4 × 3 pah
    g.PROFIL_PAH = {}
    for ad, p in PR.items():
        if p.eksen != "x": continue
        for x, e in ((FX0 + T, (1.0, 0, 0)), (FX1 - T, (-1.0, 0, 0))):
            c = p.merkez(x)
            g.kaynak(GO.uc_kaynaklari("%s_yan_kaynagi_%d" % (p.ad, int(x)), tuple(c), e, YUZ[ad], b=PRF, a=2.0, flat=PRF - 8.0, Ro=4.0, birim=g.birim))
        if ad in PAH:
            z0, z1 = PAH[ad]; y0_, y1_ = p.c[0] - PRF / 2.0 - 1, p.c[0] + PRF / 2.0 + 1
            g.PROFIL_PAH[p.ad] = (p, [kutu(xa, xb, y0_, y1_, z0, z1) for xa, xb in ((FX0 + T - 1, FX0 + T + 3.0), (FX1 - T - 3.0, FX1 - T + 1))])
            g.not_("%s: iki ucunda yan sac bükümü için köşe pahı 3 × 4 (taşlama) — kesim listesine işlenir" % p.ad)
    # dikme ↔ ön alt profil (üstü) · dikme ↔ kayıt (altı) · kiriş ↔ kayıt (arka yüzü)
    g.kaynak(GO.uc_kaynaklari("onyuz_f_ust_dikme_0_alt_kaynagi", (xd, YT1, 42.0), (0, 1.0, 0), [(1.0, 0, 0), (-1.0, 0, 0)], b=PRF, a=2.0, flat=PRF - 8.0, birim=g.birim))
    g.kaynak(GO.uc_kaynaklari("onyuz_f_ust_dikme_0_ust_kaynagi", (xd, FYTV - PRF, 42.0), (0, -1.0, 0), [(1.0, 0, 0), (-1.0, 0, 0)], b=PRF, a=2.0, flat=PRF - 8.0, birim=g.birim))
    g.kaynak(GO.uc_kaynaklari("f_ust_tavan_kirisi_kaynagi", (xd, FYTV - PRF / 2.0, 27.0), (0, 0, -1.0), [(1.0, 0, 0), (-1.0, 0, 0)], b=PRF, a=2.0, flat=PRF - 8.0, birim=g.birim))
    g.PROF_F = PR
    return PR


def f_taban(g):
    """düz taban levhası + delik kaynakları · taş yünü (2 göz) + 0,5 kılıf tavası + kör perçinler + rakor kovanı"""
    s = g.sac("f_ust_taban_levhasi", "dis")
    L = s.taban([(FX0 + T, -57.0), (FX1 - T, -57.0), (FX1 - T, 828.5), (FX0 + T, 828.5)], O=(0, YT0, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="taban")   # n = +y
    for xa, xb in ((FX0 + T, FX0 + FL), (FX1 - FL, FX1 - T)):
        L.kesik([(xa - 0.5, 824.0), (xb, 824.0), (xb, 829.0), (xa - 0.5, 829.0)], tip="donus_centigi", dfm=False, parca="yan sac arka dönüşü + bükümü çentiği")
    for xa, xb in ((FX0 + T - 0.5, FX0 + T + 4.0), (FX1 - T - 4.0, FX1 - T + 0.5)):
        L.kesik([(xa, -57.5), (xb, -57.5), (xb, -53.0), (xa, -53.0)], tip="bukum_centigi", dfm=False, parca="yan sac ön bükümü köşe çentiği 4 × 4")
    L.delik(RAKOR[0], -RAKOR[1], 16.5, tip="rakor_deligi", parca="davlumbaz fanı kablo rakoru Ø16,5")
    L.dikdortgen((V2[0] + V2[1]) / 2.0, -(V2[2] + V2[3]) / 2.0 + 0.0, V2[1] - V2[0] + 1.0, V2[3] - V2[2] + 1.0, r=0.5, tip="v2_gecisi", parca="V2 kablo kanalı geçişi 41 × 41")
    yr = []
    for ad, (z0, z1) in PRO_Z.items():
        zc = (z0 + z1) / 2.0
        for x in np.arange(FX0 + 150.0, FX1 - 100.0, 300.0):
            if abs(x - (KIRIS_X[0] + KIRIS_X[1]) / 2.0) < 30 and ad == "on": continue
            L.oblong(x, -zc, 25.0, 8.0, 0.0, tip="kaynak_yarigi", parca="delik kaynağı 25 × 8 (profile) · yüz taşlanır"); yr.append((x, zc))
    for i, (x, zc) in enumerate(yr):
        f = S.yuz_oblong(x, -zc, 25.0, 8.0, 0.0)
        sh = S._tasi(S._prizma(f, T), S._M(np.column_stack([[1, 0, 0], [0, 0, -1.0], [0, 1.0, 0]]), (0, YT0, 0)))
        g.kaynak(dict(ad="f_ust_taban_levhasi_delik_kaynagi_%d" % i, wp=cq.Workplane("XY").add(sh), sh=sh, mal="sac", birim=g.birim, grup="SABIT", kaynak=SURUM, tur="kaynak",
                      bom=("Delik (yarık) kaynağı · TIG 141 · ER308LSi · yüz taşlanır", 1, "25 × 8 × 1,5", "taban levhası ↔ alt profil", "ÜRETİM"),
                      meta=dict(tur="kaynak", tip="delik", yontem="TIG 141")))
    g.PANEL["taban"] = L
    # yalıtım gözleri: ön (orta profil ön yüzü → ön profil arka yüzü) · arka (arka profil ön yüzü → orta profil arka yüzü) · x yan saclar arası
    gozler = (("on", PRO_Z["orta"][1], PRO_Z["on"][0]), ("arka", PRO_Z["arka"][1], PRO_Z["orta"][0]))
    for ad, za, zb in gozler:
        k = g.sac("f_ust_taban_yalitim_kilifi_%s" % ad, "ic", t=0.5); gk = k.R + k.t
        K = k.taban([(FX0 + T + gk, -zb + gk), (FX1 - T - gk, -zb + gk), (FX1 - T - gk, -za - gk), (FX0 + T + gk, -za - gk)], O=(0, YP1 - YAL - 0.5, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="taban")
        v2 = za < V2[2] < zb
        fl = []
        for i, a in enumerate(("on_donus", "sag_donus", "arka_donus", "sol_donus")):
            if i == 2 and v2: fl.append(K.flans(i, YAL, yon=+1, bas=0.0, son=V2[1] + 2.0 - (FX0 + T + gk), ad=a))   # arka dönüş V2'nin sağında
            else: fl.append(K.flans(i, YAL, yon=+1, ad=a))
        for i in range(4):
            if v2 and i == 2: continue                                    # sol-arka köşede arka dönüş yok (arka profil yüzü kapatır)
            k.kose(fl[i], fl[(i + 1) % 4], "acik", rahat="kare")
        if v2:
            K.kesik([(V2[0] - 1.5, -V2[3] - 1.5), (V2[1] + 1.5, -V2[3] - 1.5), (V2[1] + 1.5, -za + 1.0), (V2[0] - 1.5, -za + 1.0)], tip="v2_centigi", dfm=False,
                    parca="V2 kablo kanalı kenar çentiği 43 × 41,5 (arka kenara açık)")
        icx0, icx1, icz0, icz1 = FX0 + T + 1.25, FX1 - T - 1.25, za + 1.25, zb - 1.25
        y = kutu(icx0, icx1, YP1 - YAL, YP1, icz0, icz1)
        if v2:                                                        # F V2 kablo kanalı (x 2890–2930 · z −796…−756) taban + yalıtım + kılıftan geçer
            y = y.cut(kutu(V2[0] - 2.5, V2[1] + 2.5, YP1 - YAL - 1, YP1 + 1, za - 1.0, V2[3] + 2.5))
            kv = kutu(V2[0] - 2.5, V2[1] + 2.5, YP1 - YAL, YP1, za + 0.5, V2[3] + 2.5).cut(kutu(V2[0] - 1.5, V2[1] + 1.5, YP1 - YAL - 1, YP1 + 1, za, V2[3] + 1.5))
            ozel_kati(g, "f_ust_taban_v2_kovani", kv, "V2 kanal kovanı AISI 304 1,0 · U büküm (2 büküm) · arka açık (arka profil yüzü kapatır) · kılıfa 2 kör perçin",
                      "45 × 42 × 20", "AISI 304")
        if za < RAKOR[1] < zb:
            K.delik(RAKOR[0], -RAKOR[1], 25.6, tip="rakor_kovani_deligi", parca="rakor kovanı Ø25,4")
            y = y.cut(GO.silindir((RAKOR[0], YP1 - YAL - 1, RAKOR[1]), (0, 1.0, 0), 12.7, YAL + 2))
            kv = GO.silindir((RAKOR[0], YP1 - YAL - 0.5, RAKOR[1]), (0, 1.0, 0), 12.7, YAL + 0.5).cut(GO.silindir((RAKOR[0], YP1 - YAL - 1.0, RAKOR[1]), (0, 1.0, 0), 11.7, YAL + 2))
            ozel_kati(g, "f_ust_taban_rakor_kovani", kv, "Rakor kovanı AISI 304 Ø25,4 × 1 (kılıf → taban levhası · yalıtım rakora açılmaz)", "Ø25,4 × 1 × 20,5", "AISI 304")
        g.YAL_BEKLEYEN = getattr(g, "YAL_BEKLEYEN", []) + [(ad, y, icx0, icx1, icz0, icz1)]
        g.eleman(dict(ad="f_ust_taban_yalitimi_%s" % ad, wp=cq.Workplane("XY").add(y), sh=y, mal="conta", birim=g.birim, grup="SABIT", kaynak=SURUM, tur="yalitim",
                      bom=("Taş yünü levha A1 (EN 13501-1) ≥ 100 kg/m³ · 20 mm · kesilerek yerleştirilir (kılıf tavası içinde, görünmez)", 1,
                           "%.0f × %.0f × 20" % (icx1 - icx0, icz1 - icz0), "satın alma levha → kesim", "SATIN ALMA"),
                      meta=dict(tur="yalitim", malzeme="taş yünü", gorunmez=True)), mal="conta")
        # kör perçinler: tava ön / arka dönüşü → profil yan duvarı (her biri 4) · sol / sağ dönüş → yan sac (her biri 2)
        PR = g.PROF_F; cep_ = []
        for zz, pr_ad, n_ in ((zb, "on" if ad == "on" else "orta", -1.0), (za, "orta" if ad == "on" else "arka", 1.0)):
            pr = PR[pr_ad]
            for x in np.linspace(FX0 + 150.0, FX1 - 150.0, 4):
                yy = YP1 - 10.0
                pr.duvar_delik("-z" if n_ < 0 else "+z", x, yy - (YP0 + YP1) / 2.0, 3.3, tip="kor_percin", not_="kılıf tavası perçini Ø3,2")
                fz = [f for f in fl if abs(np.dot(f.normal(), (0, 0, 1.0))) > 0.9 and abs(f.yerel((x, yy, zz))[2]) < 2.0]
                if fz:
                    uv = fz[0].yerel((x, yy, zz)); fz[0].delik(uv[0], uv[1], 3.3, tip="kor_percin", parca="kör perçin Ø3,2 (ISO 15983)")
                g.eleman(S.kor_percin(3.2, 6.0, (x, yy, zz + n_ * 0.5), (0, 0, -n_), ad="f_ust_kilif_percin_%s_%s_%d" % (ad, pr_ad, int(x)), birim=g.birim, kavrama=2.5))
                cep_.append(GO.silindir((x, yy, zz + n_ * 0.5), (0, 0, n_), 6.0, 3.0))
        yp = [q for q in g.ELEMAN if q["ad"] == "f_ust_taban_yalitimi_%s" % ad][0]           # taş yünü: perçin başı yerinde Ø12 × 3 kesilir
        sh_ = yp["sh"]
        for c_ in cep_: sh_ = sh_.cut(c_)
        yp["sh"] = sh_; yp["wp"] = cq.Workplane("XY").add(sh_)


def f_bolme(g):
    """orta bölme (davlumbaz ön duvarı) · yan dönüşler (+z) yan saclara FHP"""
    s = g.sac("f_davlumbaz_bolme_duvari", "dis"); gg = s.R + s.t
    y0, y1 = YT1, FYTV
    B = s.taban([(FX0 + T + gg, y0), (FX1 - T - gg, y0), (FX1 - T - gg, y1), (FX0 + T + gg, y1)], O=(0, 0, BOLME_Z[0]), ex=(1, 0, 0), ey=(0, 1, 0), ad="bolme")   # n = +z
    fs = B.flans(1, 20.0, yon=+1, bas=4.0, son=y1 - 1836.0, ad="sag_donus"); fl = B.flans(3, 20.0, yon=+1, bas=y1 - 1836.0, son=4.0, ad="sol_donus")
    for xa, yr in EMIS:
        B.dikdortgen(xa + 80.0, yr + 5.0, 160.0, 10.0, r=2.0, tip="emis_yarigi", parca="davlumbaz emiş yarığı 160 × 10")
    B.delik(3548.9, 1809.0, 12.0, tip="gecis", parca="hava borusu Ø12 (boru Ø9,8)")
    B.dikdortgen((KIRIS_X[0] + KIRIS_X[1]) / 2.0, (FYTV - PRF + y1) / 2.0 + 1.0, KIRIS_X[1] - KIRIS_X[0] + 1.0, PRF + 2.0, tip="kiris_centigi", dfm=False,
                 parca="tavan kirişi çentiği 31 × 31 (üst kenara açık)")
    for tr, xs, F_ in (("sol", FX0, fl), ("sag", FX1, fs)):
        for y in (1420.0, 1600.0, 1790.0):
            E.bag(g, g.PANEL[tr]["yan"], F_, (xs, y, BOLME_Z[0] + 12.0), "govde_fu_bag_bolme_%s_%d" % (tr, int(y)))
    g.PANEL["bolme"] = B


def f_tavan_arka(g):
    s = g.sac("f_ust_tavan_sac", "dis"); gg = s.R + s.t
    Tv = s.taban([(FX0 + T + gg, -ZO), (FX1 - T - gg, -ZO), (FX1 - T - gg, -ZA), (FX0 + T + gg, -ZA)], O=(0, FYTV, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="tavan")
    sag = Tv.flans(1, 21.5, yon=-1, bas=ZO - 26.0, son=8.0, ad="sag_donus"); sol = Tv.flans(3, 21.5, yon=-1, bas=8.0, son=ZO - 26.0, ad="sol_donus")
    a0, a1, b0, b1 = U_KUTU["F"]["tavan_baca"]
    Tv.dikdortgen((a0 + a1) / 2.0, -(b0 + b1) / 2.0, a1 - a0, b1 - b0, r=0.5, tip="atis_agzi", parca="davlumbaz atış kanalı ağzı 297 × 197 (kanal 296 × 196 içinden geçer)")
    a0, a1, b0, b1 = U_KUTU["F"]["v1"]
    Tv.dikdortgen((a0 + a1) / 2.0, -(ZA + b1 + 0.5) / 2.0, a1 - a0 + 1.0, b1 + 0.5 - ZA + 0.2, tip="v1_centigi", dfm=False, parca="pano V1 kanal çentiği (arka kenara açık)")
    g.PANEL["tavan"] = dict(tavan=Tv, sol=sol, sag=sag, s=s)
    s = g.sac("f_ust_arka_sac", "dis"); gg = s.R + s.t
    A = s.taban([(FX0, FY0), (FX1, FY0), (FX1, FYTV - gg - 0.5), (FX0, FYTV - gg - 0.5)], O=(0, 0, ZA), ex=(1, 0, 0), ey=(0, 1, 0), ad="arka")
    ust = A.flans(2, 24.0, yon=+1, bas=FX1 - 3925.0, son=4.0, ad="ust_donus")
    for xa, xb in PANJUR["x"]:
        for j in range(PANJUR["n"]):
            y0 = PANJUR["y0"] + PANJUR["adim"] * j
            A.dikdortgen((xa + xb) / 2.0, y0 + PANJUR["h"] / 2.0, xb - xa, PANJUR["h"], r=2.0, tip="panjur_yarigi", parca="panjur yarığı 170 × 12")
    for i, (xa, xb) in enumerate(PANJUR["x"]):
        for j in range(PANJUR["n"]):
            y = PANJUR["y0"] + PANJUR["h"] + PANJUR["adim"] * j
            l = kutu(xa, xb, y, y + T, ZAI, ZAI + 12.0)
            ozel_kati(g, "f_ust_panjur_lameli_%d_%d" % (i, j), l, "Panjur lameli AISI 304 170 × 12 × 1,5 (lazer · arka sacın iç yüzüne iki uçtan dikiş kaynak)", "170 × 12 × 1,5", "AISI 304")
            for xx in (xa + 2.0, xb - 12.0):
                g.kaynak(S.kaynak_dikisi((xx, y + T, ZAI), (xx + 10.0, y + T, ZAI), (0, 1.0, 0), (0, 0, 1.0), 1.0, ad="f_ust_panjur_lameli_%d_%d_kaynak_%d" % (i, j, int(xx)),
                                         birim=g.birim, taraf="iç", not_="lamel ↔ arka sac (2 × 10)"))
    for x, y, d in F_RAKOR:
        A.delik(x, y, d, tip="rakor_deligi", parca="kablo rakoru Ø%g" % d)
    g.PANEL["arka"] = dict(arka=A, ust=ust, s=s)
    # bağlantılar: yan ↔ arka (arka sactan FHP) · yan ↔ tavan (yandan FHP) · tavan ↔ arka üst dönüşü (tavandan FHP)
    for tr, xx in (("sol", FX0 + 10.5), ("sag", FX1 - 10.5)):
        for y in (850.0, 1050.0, 1250.0, 1450.0, 1575.0):
            if 1300 < y < 1360 or 1600 < y < 1665 or (tr == "sag" and y > 1640): continue
            E.bag(g, A, g.PANEL[tr]["arka"], (xx, y, ZA), "govde_fu_bag_arka_%s_%d" % (tr, int(y)), boy=10)
    for tr, xs in (("sol", FX0), ("sag", FX1)):
        for z in E.dizi(-760.0 if tr == "sag" else -800.0, 0.0, maks=200.0, uc=10.0):
            E.bag(g, g.PANEL[tr]["yan"], g.PANEL["tavan"][tr], (xs, 1849.0, z), "govde_fu_bag_tavan_%s_%d" % (tr, int(-z)))
    for x in E.dizi(FX0 + 40.0, 3900.0, maks=200.0, uc=10.0):
        E.bag(g, Tv, ust, (x, FYT, -815.0), "govde_fu_bag_tavan_arka_%d" % int(x))
    s = g.sac("govde_fu_kosebent_sol_arka_ust", "braket"); tt, R = s.t, s.R
    Pk = s.taban([(FX0 + T + tt + R, 1700.0), (FX0 + T + 32.0, 1700.0), (FX0 + T + 32.0, 1780.0), (FX0 + T + tt + R, 1780.0)], O=(0, 0, ZAI), ex=(1, 0, 0), ey=(0, 1, 0), ad="arka_ayak")
    Fk = Pk.flans(3, 32.0, yon=+1, ad="yan_ayak")
    E.bag(g, A, Pk, (FX0 + T + 20.5, 1740.0, ZA), "govde_fu_bag_kosebent_arka")
    E.bag(g, g.PANEL["sol"]["yan"], Fk, (FX0, 1740.0, ZAI + 22.0), "govde_fu_bag_kosebent_yan")


# =====================================================================================================================================
# 3 · MEKANİZMA TEMAS SAPLAMALARI (h3_e_sac_v1 ile aynı kural, dünya koordinatı)
# =====================================================================================================================================
def mek_saplama(g, duvarlar, bolge, log=print):
    L = E._bilesen_listesi(); out, atla = [], []
    for P, ax, d, sg, dis in duvarlar:
        for ad, lo, hi, n in L:
            if MEK_HARIC.search(ad): continue
            lo = np.array(lo, float); hi = np.array(hi, float)
            yuz = lo[ax] if sg > 0 else hi[ax]
            if abs(yuz - d) > 0.06: continue
            if (lo < np.array(bolge[0]) - 1).any() or (hi > np.array(bolge[1]) + 1).any(): continue
            o = [i for i in range(3) if i != ax]
            a0, a1 = lo[o[0]], hi[o[0]]; b0, b1 = lo[o[1]], hi[o[1]]
            if min(a1 - a0, b1 - b0) < 9.0: atla.append((P.sac.ad, ad, "yama dar")); continue
            if (a1 - a0) >= (b1 - b0): nok = [((a0 + a1) / 2.0 + s * (a1 - a0) / 4.0, (b0 + b1) / 2.0) for s in ((-1, 1) if (a1 - a0) > 70 else (0,))]
            else: nok = [((a0 + a1) / 2.0, (b0 + b1) / 2.0 + s * (b1 - b0) / 4.0) for s in ((-1, 1) if (b1 - b0) > 70 else (0,))]
            for (a, b) in nok:
                p = np.zeros(3); p[ax] = d; p[o[0]] = a; p[o[1]] = b
                ya = P.yerel(p)
                if not E.guvenli(P, ya[0], ya[1], kenar=12.0, delik=9.0): atla.append((P.sac.ad, ad, "yer güvenli değil %s" % np.round(p, 1).tolist())); continue
                yon = np.zeros(3); yon[ax] = sg
                E.fhp_arayuz(g, P, p, yon, ad + " bbox %s" % [round(float(v), 1) for v in (lo[0], hi[0], lo[1], hi[1], lo[2], hi[2])],
                             "mekanizma tarafında Ø5,5 delik (FHP-M5 saplama · pul + fiberli somun)", dis=dis, boy=12, ad="arayuz_mek_%s_%d" % (P.sac.ad, len(g.ARAYUZ)))
                out.append((P.sac.ad, ad, np.round(p, 1).tolist()))
    log("%s mekanizma temas saplaması: %d · atlanan %d" % (g.birim, len(out), len(atla)))
    g.MEK_SAPLAMA, g.MEK_ATLA = out, atla
    return out


# =====================================================================================================================================
# 4 · KUR · MONTAJ SÖZLEŞMESİ
# =====================================================================================================================================
def kur(log=print):
    t0 = time.time()
    gF = GO.Govde("U_F_GOVDE", SURUM, istasyon="U_F"); gK = GO.Govde("U_KE_GOVDE", SURUM, istasyon="U_KE"); gFU = GO.Govde("F_UST_KABIN", SURUM, istasyon="F_UST")
    u_kutu(gF, "F"); giris_cebi(gF); u_kutu(gK, "KE")
    f_yan(gFU, "sol"); f_yan(gFU, "sag"); f_cerceve(gFU); f_taban(gFU); f_bolme(gFU); f_tavan_arka(gFU)
    u_baglantilari(gF, gK, gFU)
    for g, kod, x0, x1 in ((gF, "F", 2500.0, 4000.0), (gK, "KE", 4000.0, 5230.0)):
        P = g.PANEL[kod]
        mek_saplama(g, [(P["taban"], 1, Y0 + T, +1, "M5"), (P["arka"]["arka"], 2, ZAI, +1, "M5"), (P["tavan"]["tavan"], 1, YT - T, -1, "M5"),
                        (P["sol"]["yan"], 0, x0 + T, +1, "M5"), (P["sag"]["yan"], 0, x1 - T, -1, "M5")], ((x0, Y0, ZA), (x1, YT, ZO + 20)), log)
    P = gFU.PANEL
    mek_saplama(gFU, [(P["tavan"]["tavan"], 1, FYTV, -1, "M5"), (P["arka"]["arka"], 2, ZAI, +1, "M5"), (P["sol"]["yan"], 0, FX0 + T, +1, "M5"),
                      (P["sag"]["yan"], 0, FX1 - T, -1, "M5"), (P["taban"], 1, YT1, +1, "M5"), (P["bolme"], 2, BOLME_Z[1], +1, "M5"),
                      (P["bolme"], 2, BOLME_Z[0], -1, "M5")], ((FX0, FY0, ZA), (FX1, FYT, ZO + 20)), log)
    # fan çerçeveleri (4 köşe) ve baca flanşı (4 nokta): ızgara / ağız kenarına yakın → elle (otomatik kural yarıklara 9 mm koruma ister)
    A = gF.PANEL["F"]["arka"]["arka"]; Tv = gF.PANEL["F"]["tavan"]["tavan"]
    for xf, yf in U_KUTU["F"]["fan"]:
        for dx in (-58.0, 58.0):
            for dy in (-40.0, 40.0):
                E.fhp_arayuz(gF, A, (xf + dx, yf + dy, ZA), (0, 0, 1.0), "U_F_HAVALANDIRMA fan çerçevesi %g/%g" % (xf, yf),
                             "fan çerçevesi köşesinde Ø5,5 (FHP-M5 · pul + fiberli somun)", ad="arayuz_fan_%d_%d_%d_%d" % (xf, yf, dx > 0, dy > 0))
    for x, z in ((2935.0, -620.0), (3265.0, -620.0), (3100.0, -505.0), (3100.0, -735.0)):
        E.fhp_arayuz(gF, Tv, (x, YT, z), (0, -1.0, 0), "U_F_BACA baca flanşı (360 × 260)", "flanşta Ø5,5 (FHP-M5 tavandan · altta pul + fiberli somun)",
                     ad="arayuz_baca_flansi_%d_%d" % (x, -z))
    for ad_, (pr_, kes_) in gFU.PROFIL_PAH.items():               # profil uç pahları EN SONDA (duvar delikleri katıyı yeniden kurar)
        sh_ = pr_.kati()
        for k_ in kes_: sh_ = sh_.cut(k_)
        pr_._sh = sh_.clean()
    for g in (gF, gK, gFU): E.saplama_duzelt(g, SAPLAMA_CIKAR, SAPLAMA_TASI, log=log)      # ADIM 8 (adlar birim içinde tekil)
    for g in (gF, gK, gFU): g.doner_guncelle()
    log("%s · kuruldu: U_F %d sac · U_KE %d sac · F_UST %d sac + %d profil · eleman %d · kaynak %d · arayüz %d · %.1f sn" % (
        SURUM, len(gF.SAC), len(gK.SAC), len(gFU.SAC), len(gFU.PROF), len(gF.ELEMAN) + len(gK.ELEMAN) + len(gFU.ELEMAN),
        len(gF.KAYNAK) + len(gK.KAYNAK) + len(gFU.KAYNAK), len(gF.ARAYUZ) + len(gK.ARAYUZ) + len(gFU.ARAYUZ), time.time() - t0))
    return dict(U_F=gF, U_KE=gK, F_UST=gFU)


def govde_parcalari(g):
    return GO.govde_parcalari(g)


ONEK = dict(U_F_GOVDE=("ust_f_", "govde_f_", "onyuz_ust_f_"), U_KE_GOVDE=("ust_ke_", "govde_ke_"), F_UST_KABIN=("f_ust_", "f_davlumbaz_bolme", "onyuz_f_ust_", "govde_fu_"))


def uygula(MOD_PARCALAR, birim, g, rapor=None):
    """montaj (SONRA, ayrı adım) · birim: U_F_GOVDE / U_KE_GOVDE / F_UST_KABIN"""
    isaret = {"U_F_GOVDE": "ust_f_giris_cebi", "U_KE_GOVDE": "ust_ke_tavan_omegasi_0", "F_UST_KABIN": "f_ust_taban_yalitim_kilifi_on"}[birim]
    return GO.uygula(MOD_PARCALAR, govde_parcalari(g), ESKI[birim], isaret, onekler=ONEK[birim], rapor=rapor, etiket=birim)


if __name__ == "__main__":
    sys.path.insert(0, E._cikti())
    import sac_denetim_5b as DEN
    DEN.calistir_U(sys.modules[__name__], hizli="--hizli" in sys.argv)
    sys.stdout.flush(); os._exit(0)
