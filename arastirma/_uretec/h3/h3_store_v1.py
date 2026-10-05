# -*- coding: utf-8 -*-
"""HAT VERSİYON 3 · B ÇEKMECELİ DOLAP v1 (30 Eyl 2026 · Claude · YEREL) — montajda SC yerine girer.
Kemal (HAT v2.7): "çöpü kaldır · K3'ü boz · yağ tenekesini oradan kaldır · soğutma grubunu dolaba koy · 2 günlükten fazla çekmece yok".
YERLEŞİM (dünya x · h3_hesap_v1): tek parça dolap 736–4400 × 123–788 (K'nin altına uzar) ·
  K1 lahmacun ×5 · K2 lahmacun ×5 (yüksek kolon, tavan 728) · K3 pide ×4 · K5 pide ×3 + içecek · K6 tatlı + içecek ×2 (alçak kolon, tavan 668: yarısı fırın altı)
  · TEKNİK SÜTUN 4028,5–4400 (K'nin altı) = store_cad_v14'teki K4'ün düzeni: altta Secop CU NLE8.8CN (kondenser arkada, arka hava odasından emer, önden
    servis panelinin yarıklarından atar) · hava odasının tabanında buharlaştırma tavası (sıcak gaz serpantinli; iki evaporatörün gideri buraya iner) ·
    arka üstte B panosu (hava odasıyla aynı serin hacim) · önde ara PU katmanı üstünde kaşar + sucuk 2 günlük SOĞUK DEPO çekmecesi (tek kap, bölmeli · 5.4).
Çekmeceler store_cad_v14.cekmece() ile AYNEN üretilir (kutu, tepsi, 3 elemanlı ray, motor + kayış, reed, fitil, 40'lık ön) — yalnız kolon / kot sözlükleri v3.
Gövde (kasa) bu dosyada v3 ölçüsünde yeniden kurulur (v14 kurgusu: sandviç kabuk + PU + 35'lik bölmeler + fırın altı ısı kalkanı + taşıyıcı çerçeve).
SÖZLEŞME (montaj SC olarak kullanır): modul() → özet [(kod, tip, n, ust, acik_ust)] · PARCALAR (dünya) · CEK · STROK · Y_PLINT · RAMPA_SN · KAS_PD · W_B ·
  RAY_ARA_ORAN · KLAPE_AC (robot çöpü E'de: h3_kutu_v1 ile aynı) · H_B · Z_ON · X0 · X1 · KOLON_X · KAPAK_X · BOLME_X · AYAK_XZ · GIDER · BIRIM_AD.
Dünya: x hat boyunca, y yukarı (zemin 0), z derinlik (ön +79 · arka −830). Çalıştır (öz denetim): python -u ob_calistir.py h3/h3_store_v1.py [hizli]"""
import math, os, sys, time

H2 = os.path.dirname(os.path.abspath(__file__)); U = os.path.dirname(H2)
for _p in (U, H2):
    if _p not in sys.path: sys.path.insert(0, _p)
import cadquery as cq
import h3_hesap_v1 as H
import store_cad_v14 as SC0

V = cq.Vector
kut, sily, silx, silz, profil = SC0.kut, SC0.sily, SC0.silx, SC0.silz, SC0.profil

# ---------------------------------------------------------------- v14 ile AYNI sabitler
H_B, Y_PLINT, Y_TABAN, Y_TAVAN, Y_TAVAN_F = SC0.H_B, SC0.Y_PLINT, SC0.Y_TABAN, SC0.Y_TAVAN, SC0.Y_TAVAN_F   # 788 · 123 · 164,5 · 728 · 668
Z_ON, Z_ON0, Z_ON1, Z_CON0, Z_CER0, Z_CER1, ZP1 = SC0.Z_ON, SC0.Z_ON0, SC0.Z_ON1, SC0.Z_CON0, SC0.Z_CER0, SC0.Z_CER1, SC0.ZP1_ON
Z_ARKA, DZ, Z_ARKA_DIS, DERINLIK = SC0.Z_ARKA, SC0.DZ, SC0.Z_ARKA_DIS, SC0.DERINLIK
ZP0 = -DZ + 1.5
BOLME, FUGA, BIND, WO = SC0.BOLME, SC0.FUGA, SC0.BIND, SC0.WO
STROK, KAS_PD, RAMPA_SN, RAY_ARA_ORAN = SC0.STROK, SC0.KAS_PD, SC0.RAMPA_SN, SC0.RAY_ARA_ORAN
ON_ALT, ON_UST = SC0.ON_ALT, SC0.ON_UST
KAN_X, KAN_Z, KAN_UST, KAN_UST_F = SC0.KAN_X, SC0.KAN_Z, SC0.KAN_UST, SC0.KAN_UST_F

# ---------------------------------------------------------------- v3 YERLEŞİM
X0, X1 = H.B_X                                  # 736 · 4400
W_B = X1 - X0                                   # 3664
KOLON_AD = ("K1", "K2", "K3", "K5", "K6")
KOLON_X = dict(H.KOLON_V3)                      # 798,5 · 1453,5 · 2108,5 · 2763,5 · 3418,5
KOLON_W = dict(H.KOLON_W_V3)                    # 620 · K6 575
BOLME_X = tuple(H.BOLME_V3)                     # B1 1418,5 · B2 2073,5 · B3 2728,5 · B4 3383,5 · B5 3993,5 (sol yüzler)
BOLME_AD = ("B1", "B2", "B3", "B4", "B5")
T0 = H.T_X[0]                                   # 4028,5 · teknik sütunun sol iç yüzü (B5'in sağı)
X_IC_SOL = X0 + 61.5                            # 797,5 · sol iç sac (PU 60)
X_SAG_IC = X1 - 1.5                             # 4398,5 · sağ dış sacın iç yüzü
X_DEPO_SAG = X1 - 61.5                          # 4338,5 · depo bölmesinin sağ iç sacı (sağda PU 60)
XF = H.F_X                                      # fırın 2500–4000
YUKSEK = ("K1", "K2")                           # tavan 728
TAVAN_KOL = {k: (Y_TAVAN if k in YUKSEK else Y_TAVAN_F) for k in KOLON_AD}
X_ALCAK = KOLON_X["K3"]                         # 2108,5 · tavan 728 → 668 kademesi (K3'ün sol kenarı = B2'nin sağ yüzü)
HH = {"lahm": 75.0, "hamur": 75.0, "tatli": 75.0, "ic1": 130.0}
HH_UST_K5 = 126.0                               # K5'in üst içecek çekmecesi 126 (kutu 115 + tepsi): 3 küçük + 1 büyük fırın altı tavanına (668) sığsın, fitil ≤ tavan
Y0 = 200.5                                      # bütün kolonlarda ilk çekmece açıklığı (ön çizgileri kolonlar arasında hizalı · v14 K1–K3 ile aynı)


def _kapak_x():
    d = {}
    for k in KOLON_AD:
        a, b = KOLON_X[k] - 16.0, KOLON_X[k] + KOLON_W[k] + 16.0
        d[k] = (X0 if k == "K1" else a, b)
    d["T"] = (d["K6"][1] + FUGA, X1)
    return d


KAPAK_X = _kapak_x()                            # K1 736–1434,5 · K2 1437,5–2089,5 · K3 2092,5–2744,5 · K5 2747,5–3399,5 · K6 3402,5–4009,5 · T 4012,5–4400


def _cek_listesi():
    out, hh = [], {}
    for k in KOLON_AD:
        yo, n = Y0, {}
        tipler = H.DOLAP_V3[k]
        for i, t in enumerate(tipler):
            n[t] = n.get(t, 0) + 1
            kod = "CEK_%s_%s_%d" % (k, t, n[t])
            h = HH_UST_K5 if (k == "K5" and t == "ic1") else HH[t]
            out.append((k, kod, t, KOLON_X[k], yo)); hh[kod] = h
            yo += h + 2 * BIND + FUGA
    return out, hh


CEK, HH_C = _cek_listesi()
ALT_KOD = {min((c for c in CEK if c[0] == k), key=lambda c: c[4])[1] for k in KOLON_AD}
UST_KOD = {max((c for c in CEK if c[0] == k), key=lambda c: c[4])[1] for k in KOLON_AD}

# ---------------------------------------------------------------- TEKNİK SÜTUN (v14 K4 düzeni, K'nin altında)
SECOP_DX = (T0 + X_SAG_IC) / 2.0 - (SC0.SECOP_X[0] + SC0.SECOP_X[1]) / 2.0     # v14 Secop merkezi 2263,75 → 4213,5 (iki yanda 10 mm)
S0 = SC0.S0_K4                                  # 433,5 · ara katman (Secop üstü + 5)
Z_ARA = (-494.0, Z_CER0)                        # ara PU katmanı yalnız ATIŞ tarafının üstünde (kondenser düzleminin önü) · arkası pano bölmesine açık (emiş hacmi)
Z_DEPO_ARKA = (-470.0, -440.0)                  # depo bölmesinin arka PU duvarı (pano bölmesinden ayırır) · sökülür panel (pano servisi)
DEPO_RAY_L = 450.0                              # Accuride DZ3832-0450 (bas-aç) · depo kutusu 455 derin
DEPO_KUTU_D, DEPO_KUTU_UST, DEPO_SUCUK_W = 455.0, 703.0, 65.0
TAVA_T = (T0 + 5.0, X_SAG_IC - 5.0, Y_PLINT + 1.5, Y_PLINT + 34.5, -785.0, -705.0)   # hava odasının tabanında, arkada · 360 × 33 × 80
EMIS_T = [(a_, b_, -695.0, -565.0) for a_, b_ in SC0._pencereler(T0 + 4.5, X_SAG_IC - 4.5, 3, 20.0)]   # taban dış sacında emiş pencereleri (tava ile kondenser arası)
PLINT_IZ = [(4045.0 + 110.0 * c_, 4145.0 + 110.0 * c_, 21.0 + 15.0 * r_, 31.0 + 15.0 * r_) for c_ in range(3) for r_ in range(6)]   # plintte emiş yarıkları 100 × 10
PANEL_YARIK = [(4042.0 + 170.0 * c_, 4187.0 + 170.0 * c_, 165.0 + 13.0 * r_, 173.0 + 13.0 * r_) for c_ in range(2) for r_ in range(20)]   # servis paneli atış yarıkları 145 × 8
SERVIS_PANEL_Y = (ON_ALT, S0 + 12.0)            # 126 … 445,5 (v14 K4 ile aynı)
DEPO_KAPAK_Y = (S0 + 15.0, ON_UST)              # 448,5 … 785
DEPO_ACIK = (T0, X_DEPO_SAG - 1.0, S0 + 30.0, Y_TAVAN - 20.5)                 # depo çekmecesi açıklığı
DEPO_HAVA = ((560.0, 620.0), (640.0, 700.0))    # B5'te K6 ↔ depo hava geçişleri (y) · z −430…−380 (depo rayı 467–513'ün üstü)
DEPO_HAVA_Z = (-430.0, -380.0)

# ---------------------------------------------------------------- TAŞIYICI (fırın 2500–4000 + raf yükü) · dikmeler bölmelerin ortasında
TD_X = (BOLME_X[2] + BOLME / 2.0, BOLME_X[3] + BOLME / 2.0, BOLME_X[4] + BOLME / 2.0)   # B3 2746 · B4 3401 · B5 4011
TD_Z = (-110.0, -620.0)
TK_Y = (H_B - 1.5 - 40.0, H_B - 1.5)            # 746,5–786,5
TK_X_ON = (TD_X[0] - 15.0, TD_X[2] + 15.0)      # ön kiriş 2731–4026 (solu A/C kirişi: h3_moduler alın alına)
TK_X_ARKA = (XF[0] + 2.5, TD_X[2] + 15.0)       # arka kiriş 2502,5–4026 (fırının sol arka köşesi · B3 dikmesinden 228,5 konsol)
TASIYICI = ([("tasiyici_kiris_on", (TK_X_ON[0], TK_X_ON[1], TK_Y[0], TK_Y[1], TD_Z[0] - 20.0, TD_Z[0] + 20.0), "x"),
             ("tasiyici_kiris_arka", (TK_X_ARKA[0], TK_X_ARKA[1], TK_Y[0], TK_Y[1], TD_Z[1] - 20.0, TD_Z[1] + 20.0), "x"),
             ("tasiyici_capraz_uc", (XF[0] + 2.5, XF[0] + 32.5, TK_Y[0], TK_Y[1], TD_Z[1] + 20.0, TD_Z[0] - 15.0), "z")]
            + [("tasiyici_capraz_%d" % i, (x_ - 15.0, x_ + 15.0, TK_Y[0], TK_Y[1], TD_Z[1] + 20.0, TD_Z[0] - 20.0), "z") for i, x_ in enumerate(TD_X)]
            + [("tasiyici_dikme_%d" % (2 * i + j), (x_ - 15.0, x_ + 15.0, Y_PLINT + 1.5, TK_Y[0], z_ - 15.0, z_ + 15.0), "y")
               for i, x_ in enumerate(TD_X) for j, z_ in enumerate(TD_Z)])
M_FIRIN, M_RAF, EMN = SC0.M_FIRIN, SC0.M_RAF + 25.0, SC0.EMN     # v3: fırın üstüne yağ tenekesi (dolu ≈ 17,4 kg) + tartı + pompa ≈ +25 kg
KONSOL = TD_X[0] - 15.0 - TK_X_ARKA[0]          # 228,5 · arka kirişin sol konsolu

# ---------------------------------------------------------------- ISI KALKANI (fırın altı) · arka yarıklar · takozlar
ISINIM_Y = SC0.ISINIM_Y
ARKA_YARIK = [(2540.0 + 205.0 * i_, 2725.0 + 205.0 * i_) for i_ in range(7)]
TAKOZ_XZ = [(x_, z_) for x_ in (2650.0, 3050.0, 3350.0, 3700.0) for z_ in (-700.0, -250.0, 10.0)]

# ---------------------------------------------------------------- AYAKLAR (bölmelerin altında + uçlar) · plint
AYAK_Z = (-110.0, -760.0)
AYAK_X = (X0 + 60.0, BOLME_X[0] + BOLME / 2.0, BOLME_X[1] + BOLME / 2.0, TD_X[0], TD_X[1], TD_X[2], X1 - 60.0)
AYAK_XZ = [(x_, z_) for x_ in AYAK_X for z_ in AYAK_Z]
X_IC0, X_IC1 = X0 + 30.0, X1 - 30.0

# ---------------------------------------------------------------- EVAPORATÖRLER (v14 parçaları kolonla birlikte taşınır) + GİDER
EV_DX = {"sol": KOLON_X["K2"] - SC0.KOLON_X["K2"], "sag": KOLON_X["K5"] - SC0.KOLON_X["K5"]}   # +736 · +228,5
EVAP = {y_: dict(e, gider=(e["gider"][0] + EV_DX[y_], e["gider"][1])) for y_, e in SC0.EVAP.items()}   # gider x: sol 2036 · sağ 3018,5
R_ANA, R_KILIF, R_DAL = 10.0, 12.0, SC0.DR_R
Z_ANA, EGIM = -738.0, 0.011
X_ANA0 = EVAP["sol"]["gider"][0] - 12.5
Y_ANA0 = 200.5
X_ANA1 = T0 + 45.0                              # ana hattın ucu teknik sütunda (hava odası · tavanın üstü)
Y_VALF = TAVA_T[3] + 1.5 + 10.0                 # ördek gagası ağzı tava ağzının 1,5 üstünde


def y_ana(x):
    return Y_ANA0 - EGIM * (x - X_ANA0)


GIDER = dict(ana=[(X_ANA0, Y_ANA0, Z_ANA), (X_ANA1, y_ana(X_ANA1), Z_ANA), (X_ANA1, Y_VALF, Z_ANA)],
             z=Z_ANA, egim=EGIM, cap=2 * R_ANA, kilif_cap=2 * R_KILIF, tava=TAVA_T)


def _dal(yan):
    e = EVAP[yan]; gx = e["gider"][0]; ty = e["y"][0] - 15.0
    y2 = y_ana(gx); y1 = y2 + EGIM * abs(SC0.DR_Z - Z_ANA)
    return [(gx, ty, SC0.DR_Z), (gx, y1, SC0.DR_Z), (gx, y2, Z_ANA)]


GIDER["sol"], GIDER["sag"] = _dal("sol"), _dal("sag")
X_KELEPCE = {"K3": 2400.0, "K5": 3250.0, "K6": 3700.0}

KLAPE_AC = (4464.0, 4594.0, 610.0, 740.0)       # robot çöpü klapesi E'nin altında (h3_kutu_v1 ile aynı sayılar — montaj denetim metni okur)

BIRIM_AD = {
    "B_KASA": "ÇEKMECELİ DOLAP gövdesi (tek parça, +3 °C) · HAT v3 x %.0f–%.0f × 123–788 (K'nin altına uzar) · sandviç kabuk + PU + 5 bölme · fırın altında "
              "hava boşluklu ısı kalkanı · K3 / K5 / K6 alçak kolon (tavan 668)" % (X0, X1),
    "B_KABLO": "Kablo kanalları 40 × 25: her kolonda dikey · üstte yatay (K1–K2 703–728 · K3–K6 643–668, K2'nin arka sağında dikey bağlantı) → B5'ten teknik sütundaki panoya",
    "B_SOGUTMA": "Soğutma (teknik sütun, K'nin altı · v14 K4 düzeni): Secop CU NLE8.8CN R290 (kondenser arkada, hava odasından emer, servis panelinin yarıklarından atar) · "
                 "hava odasının tabanında buharlaştırma tavası + sıcak gaz serpantini · 2 bölge lamelli evaporatör (sol K2 arkası → K1–K3 · sağ K5 arkası → K5–K6 + depo) · "
                 "4 × ebm-papst 4414 FL · gider: Ø12 dallar → Ø20 ana hat (arkada yerde, ≥ %1) → tavaya",
    "B_ELEKTRIK": "B panosu (teknik sütunun arka üstü, emiş hacminde): Siemens S7-1200 1214C + 3 × SM1221 + SM1222 · Mean Well NDR-240-24 · Electromen EM-324C · 21 seçici röle",
    "B_DEPO": "Kaşar + sucuk 2 günlük SOĞUK DEPO (kural 5.4 · teknik sütunun önü, ara PU üstü): tek kap bölmeli · elle çekilen bas-aç çekmece",
    "B_TASIYICI": "Fırın taşıyıcı çerçevesi 304: ön kiriş 2731–4026 + arka kiriş 2502,5–4026 (228,5 konsol) 40 × 40 × 2 · 4 çapraz · 6 dikme (B3 / B4 / B5)",
}

PARCALAR = []
RAPOR = {}


def _ekle_hepsi(L, birim_haritasi=None):
    for p in L:
        PARCALAR.append(dict(p))


def _sh(wp):
    v = wp.vals() if hasattr(wp, "vals") else [wp]
    v = [o for o in v if isinstance(o, cq.Shape)]
    return v[0] if len(v) == 1 else cq.Compound.makeCompound(v)


# ================================================================ ÇEKMECELER (store_cad_v14.cekmece aynen · sözlükler v3)
def _cekmeceler():
    kay = dict(KAPAK_X=SC0.KAPAK_X, HH_C=SC0.HH_C, ALT_KOD=SC0.ALT_KOD, UST_KOD=SC0.UST_KOD, KOLON_W=SC0.KOLON_W, TAVAN_KOL=SC0.TAVAN_KOL,
               K1X=SC0.K1X, K4X=SC0.K4X, KOLON_X=SC0.KOLON_X, PARCALAR=SC0.PARCALAR)
    try:
        SC0.KAPAK_X = dict(KAPAK_X); SC0.HH_C = dict(HH_C); SC0.ALT_KOD = set(ALT_KOD); SC0.UST_KOD = set(UST_KOD)
        SC0.KOLON_W = dict(KOLON_W); SC0.TAVAN_KOL = dict(TAVAN_KOL)
        SC0.K1X = KOLON_X["K1"]; SC0.K4X = X_ALCAK; SC0.KOLON_X = dict(KOLON_X)          # sensör lamı ↔ yatay kablo kanalı sınaması v3 kanallarıyla
        SC0.PARCALAR = []
        ozet = []
        for kol, kod, tip, x0, yo in CEK:
            n, ust, acik_ust = SC0.cekmece(kol, kod, tip, x0, yo)
            ozet.append((kod, tip, n, ust, acik_ust))
        L = SC0.PARCALAR
    finally:
        for k_, v_ in kay.items(): setattr(SC0, k_, v_)
    return L, ozet


# ================================================================ GÖVDE
def _kasa(v1):
    """v1: store_cad_v14.PARCALAR (v1 dünya) — evaporatörler / Secop / pano cihazları buradan taşınır"""
    L = []
    CER = [k for _a, k, _e in TASIYICI]                     # taşıyıcı kutuları: sac ve PU bunlardan kesilir
    GID = _gider_katilari()
    kes_mi = lambda a, b: all(a[2 * i] < b[2 * i + 1] - 0.01 and b[2 * i] < a[2 * i + 1] - 0.01 for i in range(3))
    SACK, PUK = [], []

    def ek(ad, wp, mal, bir, bom=None, grup="SABIT"):
        L.append(dict(ad=ad, wp=wp, mal=mal, birim=bir, bom=bom, grup=grup))

    def sac(ad, k, bir="B_KASA", bom=None, kes=None, mal="sac"):
        w = kut(*k)
        for c in CER:
            if kes_mi(k, c): w = w.cut(kut(*c))
        for d_ in GID["delici"]:
            bb_ = d_.BoundingBox()
            if kes_mi(k, (bb_.xmin, bb_.xmax, bb_.ymin, bb_.ymax, bb_.zmin, bb_.zmax)): w = w.cut(cq.Workplane(obj=d_))
        if kes is not None: w = w.cut(kes)
        SACK.append(k); ek(ad, w, mal, bir, bom)

    def pu(ad, k, bom=None, kes=None):
        w = kut(*k)
        for c in CER + SACK + PUK:
            if kes_mi(k, c): w = w.cut(kut(*c))
        for d_ in GID["delici"]:
            bb_ = d_.BoundingBox()
            if kes_mi(k, (bb_.xmin, bb_.xmax, bb_.ymin, bb_.ymax, bb_.zmin, bb_.zmax)): w = w.cut(cq.Workplane(obj=d_))
        if kes is not None: w = w.cut(kes)
        PUK.append(k); ek(ad, w, "pu", "B_KASA", bom)

    # ---- taşıyıcı çerçeve ----
    for ad_, k_, eks in TASIYICI:
        bom = {"tasiyici_kiris_on": ("Taşıyıcı kiriş 40 × 40 × 2", 2, "AISI 304 kare profil · ısı kalkanının içinde, dış tavan sacının hemen altında",
                                     "ön %.0f–%.0f · arka %.0f–%.0f (arka kiriş B3 dikmesinden %.1f konsol: σ ≈ 68 MPa · sehim ≈ 0,3 mm [H])"
                                     % (TK_X_ON[0], TK_X_ON[1], TK_X_ARKA[0], TK_X_ARKA[1], KONSOL)),
               "tasiyici_capraz_0": ("Taşıyıcı çapraz 30 × 40 × 2", len(TD_X) + 1, "AISI 304 dikdörtgen profil · kirişlere kaynaklı", "B3 / B4 / B5 hizası + fırının sol ucu"),
               "tasiyici_dikme_0": ("Taşıyıcı dikme 30 × 30 × 2", 2 * len(TD_X), "AISI 304 kare profil · bölmenin PU'su içinde · alt ucunda M12 kaynak somunu → ayak",
                                    "B3 · B4 · B5")}.get(ad_)
        ek(ad_, profil(k_, eks), "celik", "B_TASIYICI", bom)
    # ---- plint + ayak ----
    PZ = (Z_ON - 61.5, Z_ON - 60.0)
    pl_ = kut(X_IC0, X_IC1, 0.0, Y_PLINT, PZ[0], PZ[1]).union(kut(X_IC0 + 1.5, X_IC1 - 1.5, Y_PLINT - 1.5, Y_PLINT, PZ[0] - SC0.PLINT_FLANS, PZ[0]))
    for a_, b_, c_, d_ in PLINT_IZ:
        pl_ = pl_.cut(kut(a_, b_, c_, d_, PZ[0] - 1.0, PZ[1] + 1.0))
    ek("onyuz_plint", pl_, "sac", "B_KASA", ("Plint 1,5 (ön)", 1, "304 fırçalı 1,5 · ön düzlemin 60 gerisi · x %.0f–%.0f · teknik sütunun önünde Secop EMİŞ yarıkları %d × 100 × 10"
                                             % (X_IC0, X_IC1, len(PLINT_IZ)), "dolabın altında ayak + plint dışında parça yok"))
    for ad_, x_ in (("sol", X_IC0), ("sag", X_IC1 - 1.5)):
        ek("onyuz_plint_donus_" + ad_, kut(x_, x_ + 1.5, 0.0, Y_PLINT, -DZ + 1.5, PZ[0]).union(
            kut(x_ + 1.5 if ad_ == "sol" else x_ - 20.0, x_ + 21.5 if ad_ == "sol" else x_, Y_PLINT - 1.5, Y_PLINT, -DZ + 1.5, PZ[0] - SC0.PLINT_FLANS)), "sac", "B_KASA")
    for i, (ax, az) in enumerate(AYAK_XZ):
        ek("ayak_%d" % i, sily(ax, az, 20.0, 0.0, 8.0).union(sily(ax, az, 6.0, 8.0, Y_PLINT)), "celik", "B_KASA",
           ("Ayarlı ayak Elesa+Ganter LV.A-SST · M12", len(AYAK_XZ), "paslanmaz · taban Ø40 · yükseklik 123", "bölmelerin + uçların altında") if i == 0 else None)
    # ---- dış kabuk ----
    sac("kasa_yan_dis_sac_sol", (X0, X0 + 1.5, Y_PLINT, H_B, -DZ, Z_ON0), bom=("Yan dış sac 1,5", 2, "304 lazer + büküm · ön kenar +39", ""))
    sac("kasa_yan_dis_sac_sag", (X1 - 1.5, X1, Y_PLINT, H_B, -DZ, Z_ON0))
    sac("tavan_dis_sac", (X0 + 1.5, X1 - 1.5, H_B - 1.5, H_B, -DZ, Z_ON0), bom=("Tavan dış sacı", 1, "304 1,5 · A, TOPPING, fırın ve K bunun üstüne oturur", ""))
    em = None
    for a_, b_, c_, d_ in EMIS_T:
        k_ = kut(a_, b_, Y_PLINT - 1.0, Y_PLINT + 3.0, c_, d_); em = k_ if em is None else em.union(k_)
    sac("taban_dis_sac", (X0 + 1.5, X1 - 1.5, Y_PLINT, Y_PLINT + 1.5, -DZ, Z_ON0), kes=em,
        bom=("Taban dış sacı 1,5", 1, "304 · teknik sütunun altında %d emiş penceresi (hava odasına)" % len(EMIS_T), "plint boşluğundan Secop'a hava"))
    ay = None
    for a_, b_ in ARKA_YARIK:
        k_ = kut(a_, b_, SC0.ARKA_YARIK_Y[0], SC0.ARKA_YARIK_Y[1], -DZ - 1.0, -DZ + 2.5); ay = k_ if ay is None else ay.union(k_)
    sac("arka_dis_sac", (X0 + 1.5, X1 - 1.5, Y_PLINT + 1.5, H_B - 1.5, -DZ, -DZ + 1.5), kes=ay)
    sac("kasa_yan_on_donus_sol", (X0 + 1.5, X0 + 30.0, Y_PLINT + 1.5, H_B - 1.5, ZP1, Z_ON0))
    sac("kasa_yan_on_donus_sag", (X1 - 30.0, X1 - 1.5, S0 + 30.0, H_B - 1.5, ZP1, Z_ON0))          # depo bölmesinin sağ PU'sunun önü (Secop bölmesi önü servis paneli)
    # ---- soğuk iç kabuk (K1 … K6) ----
    sac("yan_ic_sac_sol", (X_IC_SOL, X_IC_SOL + 1.0, Y_TABAN, Y_TAVAN, Z_ARKA, Z_CER0))
    sac("tavan_ic_sac", (X_IC_SOL, X_ALCAK, Y_TAVAN, Y_TAVAN + 1.0, Z_ARKA, ZP1))
    sac("tavan_ic_sac_F", (X_ALCAK, BOLME_X[4], Y_TAVAN_F, Y_TAVAN_F + 1.0, Z_ARKA, ZP1))
    TD_A, TD_F, TD_T = (X_IC0, X_ALCAK, Y_TAVAN, H_B - 1.5, ZP1, Z_ON0), (X_ALCAK, T0 - 18.5, Y_TAVAN_F, H_B - 1.5, ZP1, Z_ON0), (T0, X1 - 30.0, Y_TAVAN, H_B - 1.5, ZP1, Z_ON0)
    ek("tavan_on_donus", kut(*TD_A).union(kut(*TD_F)).union(kut(*TD_T)), "sac", "B_KASA"); SACK.extend([TD_A, TD_F, TD_T])
    sac("taban_ic_sac", (X_IC_SOL, BOLME_X[4], Y_TABAN - 1.0, Y_TABAN, Z_ARKA, ZP1))
    sac("taban_on_donus", (X_IC0, T0, Y_PLINT + 1.5, Y_TABAN, ZP1, Z_ON0))
    sac("arka_ic_sac", (X_IC_SOL, X_ALCAK, Y_TABAN, Y_TAVAN, Z_ARKA - 1.0, Z_ARKA))
    sac("arka_ic_sac_F", (X_ALCAK, BOLME_X[4], Y_TABAN, Y_TAVAN_F, Z_ARKA - 1.0, Z_ARKA))
    CER_A, CER_F = (X_IC0, X_ALCAK, Y_TABAN, Y_TAVAN, Z_CER0, Z_CER1), (X_ALCAK, T0, Y_TABAN, Y_TAVAN_F, Z_CER0, Z_CER1)
    CER_T = (T0, X1 - 30.0, Y_PLINT + 1.5, Y_TAVAN, Z_CER0, Z_CER1)
    SACK.extend([CER_A, CER_F, CER_T])
    # ---- bölmeler 35 (sac 1 + PU 33 + sac 1) · üst arkada kablo geçişi · arka hava geçişleri (sol bölge B1 · B2 / sağ bölge B4) · B3 kapalı ----
    HG = {0: ((190.0, 290.0), (560.0, 660.0)), 1: ((190.0, 290.0), (560.0, 660.0)), 3: ((190.0, 290.0), (400.0, 490.0))}
    for i, x0_ in enumerate(BOLME_X):
        tav = Y_TAVAN if i <= 1 else (Y_TAVAN_F if i <= 3 else H_B - 1.5)
        ku = KAN_UST if i == 0 else KAN_UST_F
        g_ = kut(x0_ - 1.0, x0_ + BOLME + 1.0, ku[0], ku[1] + 1.0, KAN_Z[0] - 1.0, KAN_Z[1])
        if i == 1:
            g_ = g_.union(kut(x0_ - 1.0, x0_ + BOLME + 1.0, KAN_UST_F[0], KAN_UST[1] + 1.0, KAN_Z[0] - 1.0, KAN_Z[1]))
        for y0_, y1_ in HG.get(i, ()):
            g_ = g_.union(kut(x0_ - 1.0, x0_ + BOLME + 1.0, y0_, y1_, SC0.HAVA_Z[0], SC0.HAVA_Z[1]))
        if i == 4:
            for y0_, y1_ in DEPO_HAVA:
                g_ = g_.union(kut(x0_ - 1.0, x0_ + BOLME + 1.0, y0_, y1_, DEPO_HAVA_Z[0], DEPO_HAVA_Z[1]))
            ya = Y_PLINT + 1.5                                                  # B5: soğuk ↔ teknik sütun (Secop bölmesi tabana iner)
            sac("bolme_4_sac_a", (x0_, x0_ + 1.0, Y_TABAN - 1.0, tav, Z_ARKA, Z_CER0), kes=g_)
            sac("bolme_4_sac_b", (x0_ + BOLME - 1.0, x0_ + BOLME, ya, tav, ZP0, Z_CER0), kes=g_,
                bom=("Ara duvar sacı 1,0 (soğuk ↔ teknik sütun)", 1, "304 · taşıyıcı dikme geçişli", "teknik sütun tarafı"))
            pu("bolme_4_pu", (x0_ + 1.0, x0_ + BOLME - 1.0, ya, tav, ZP0, Z_CER0), kes=g_)
            continue
        sac("bolme_%d_sac_a" % i, (x0_, x0_ + 1.0, Y_TABAN, tav, Z_ARKA, Z_CER0), kes=g_)
        sac("bolme_%d_sac_b" % i, (x0_ + BOLME - 1.0, x0_ + BOLME, Y_TABAN, tav, Z_ARKA, Z_CER0), kes=g_)
        pu("bolme_%d_pu" % i, (x0_ + 1.0, x0_ + BOLME - 1.0, Y_TABAN, tav, Z_ARKA, Z_CER0), kes=g_)
    # ---- fırın altı ısı kalkanı (v14 kurgusu) ----
    sac("isi_kalkani_ayirma_saci", (XF[0] + 1.0, BOLME_X[4], Y_TAVAN, Y_TAVAN + 1.0, ZP0, ZP1),
        bom=("Isı kalkanı ayırma sacı 1,0", 1, "304 · alçak kolonların tavan PU'sunun üstü, hava boşluğunun tabanı", "fırın 2500–4000'in altı"))
    sac("isi_kalkani_sol_sac", (XF[0], XF[0] + 1.0, Y_TAVAN_F + 1.0, H_B - 1.5, ZP0, ZP1))
    sac("isi_kalkani_isinim_saci", (XF[0] + 2.0, BOLME_X[4] - 1.0, ISINIM_Y[0], ISINIM_Y[1], ZP0 + 2.0, ZP1 - 2.0),
        bom=("Işınım sacı 0,8 · parlak paslanmaz", 1, "304 BA · takozlar üstünde · dikme geçiş delikli", "fırın tabanının ışınımını geri yansıtır"))
    for i_, (tx_, tz_) in enumerate(TAKOZ_XZ):
        ek("isi_kalkani_takozu_%d" % i_, kut(tx_ - 10.0, tx_ + 10.0, Y_TAVAN + 1.0, ISINIM_Y[0], tz_ - 10.0, tz_ + 10.0), "koyu", "B_KASA",
           ("Isı köprüsü kesici takoz 20 × 20 × 11", len(TAKOZ_XZ), "cam elyaf / PTFE [VARSAYIM]", "ayırma sacı ↔ ışınım sacı") if i_ == 0 else None)
    # ---- PU ----
    pu("yan_pu_sol", (X0 + 1.5, X_IC_SOL, Y_PLINT + 1.5, H_B - 1.5, ZP0, Z_CER0))
    pu("yan_pu_sol_on", (X0 + 1.5, X0 + 29.0, Y_PLINT + 1.5, H_B - 1.5, Z_CER0, ZP1))
    pu("tavan_pu_57.5", (X0 + 29.0, X_ALCAK, Y_TAVAN + 1.0, H_B - 1.5, ZP0, ZP1),
       bom=("PU köpük gövde", 1, "40 kg/m³ enjeksiyon · sac kabuk içine", "yan 60 · tavan 57,5 (alçak kolonlarda 117,5 / fırın altında 59 + hava boşluğu) · arka 37,5 · taban 39 · bölme 33"))
    pu("tavan_pu_T", (X_ALCAK, XF[0], Y_TAVAN_F + 1.0, H_B - 1.5, ZP0, ZP1))              # K3'ün TOPPING altındaki kısmı: fırın yok → tavan PU dolu
    pu("tavan_pu_F", (XF[0], BOLME_X[4] + 1.0, Y_TAVAN_F + 1.0, Y_TAVAN, ZP0, ZP1))
    pu("taban_pu", (X0 + 29.0, BOLME_X[4] + 1.0, Y_PLINT + 1.5, Y_TABAN - 1.0, ZP0, ZP1))
    pu("arka_pu_37.5", (X0 + 29.0, XF[0], Y_PLINT + 1.5, H_B - 1.5, ZP0, Z_ARKA - 1.0))
    pu("arka_pu_F", (XF[0], BOLME_X[4] + 1.0, Y_PLINT + 1.5, Y_TAVAN, ZP0, Z_ARKA - 1.0))            # üstü (728–786,5) ısı kalkanının hava boşluğu: arka yarıklara açık
    # ---- TEKNİK SÜTUN: ara katman (atış tarafının üstü) · depo bölmesi (soğuk) · pano bölmesi ----
    sac("tk_ara_sac_alt", (T0, X_SAG_IC, S0, S0 + 1.0, Z_ARA[0], Z_ARA[1]), bir="B_SOGUTMA")
    pu("tk_ara_pu", (T0, X_SAG_IC, S0 + 1.0, S0 + 29.0, Z_ARA[0], Z_ARA[1]))
    sac("tk_ara_sac_ust", (T0, X_SAG_IC, S0 + 29.0, S0 + 30.0, Z_ARA[0], Z_ARA[1]), bir="B_SOGUTMA")
    sac("tk_depo_arka_sac_on", (T0, X_DEPO_SAG, S0 + 30.0, Y_TAVAN, Z_DEPO_ARKA[1] - 1.0, Z_DEPO_ARKA[1]), bir="B_DEPO")
    sac("tk_depo_arka_sac_arka", (T0, X_SAG_IC, S0 + 30.0, H_B - 1.5, Z_DEPO_ARKA[0], Z_DEPO_ARKA[0] + 1.0), bir="B_DEPO",
        bom=("Depo arka duvarı · sökülür PU panel (sac 1 + PU 28 + sac 1)", 1, "304 · 4 × M5 · depo çekmecesi çıkarılınca sökülür → pano servisi", ""))
    pu("tk_depo_arka_pu", (T0, X_SAG_IC, S0 + 30.0, H_B - 1.5, Z_DEPO_ARKA[0] + 1.0, Z_DEPO_ARKA[1] - 1.0))
    sac("tk_depo_sag_ic_sac", (X_DEPO_SAG - 1.0, X_DEPO_SAG, S0 + 30.0, Y_TAVAN, Z_DEPO_ARKA[1], Z_CER0), bir="B_DEPO")
    pu("tk_depo_sag_pu", (X_DEPO_SAG, X_SAG_IC, S0 + 30.0, H_B - 1.5, Z_DEPO_ARKA[1], Z_CER0))
    sac("tk_depo_tavan_ic_sac", (T0, X_DEPO_SAG, Y_TAVAN, Y_TAVAN + 1.0, Z_DEPO_ARKA[1], ZP1), bir="B_DEPO")
    pu("tk_depo_tavan_pu", (T0, X_SAG_IC, Y_TAVAN + 1.0, H_B - 1.5, Z_DEPO_ARKA[1], ZP1))
    L.extend(_teknik(v1, ek, sac, pu))
    # ---- kablo kanalları ----
    for kol in KOLON_AD:
        cx = KOLON_X[kol]; ku = KAN_UST if kol in YUKSEK else KAN_UST_F
        ek("kablo_kanali_%s" % kol, kut(cx + KAN_X[0], cx + KAN_X[1], Y_TABAN, ku[0], KAN_Z[0], KAN_Z[1]), "kanal", "B_KABLO",
           ("Kablo kanalı 40 × 25", len(KOLON_AD) + 4, "PVC perfore + kapak", "dikey her kolonda + üstte yatay 2 + bağlantı + panoya") if kol == "K1" else None)
    ek("kablo_kanali_ust", kut(KOLON_X["K1"] + KAN_X[0], BOLME_X[1] - 1.0, KAN_UST[0], KAN_UST[1], KAN_Z[0], KAN_Z[1]), "kanal", "B_KABLO")
    ek("kablo_kanali_baglanti_K2", kut(BOLME_X[1] - 41.0, BOLME_X[1] - 1.0, KAN_UST_F[0], KAN_UST[0], KAN_Z[0], KAN_Z[1]), "kanal", "B_KABLO")
    ek("kablo_kanali_ust_F", kut(BOLME_X[1] - 1.0, T0 + 4.0, KAN_UST_F[0], KAN_UST_F[1], KAN_Z[0], KAN_Z[1]), "kanal", "B_KABLO")
    # ---- ön çerçeve sacı 1,0 (430 ferritik) · bütün açıklıklar ----
    cer = kut(*CER_A).union(kut(*CER_F)).union(kut(*CER_T))
    for kol, kod, tip, x0, yo in CEK:
        cer = cer.cut(kut(x0, x0 + KOLON_W[kol], yo, yo + HH_C[kod], Z_CER0 - 1, Z_CER1 + 1))
    cer = cer.cut(kut(T0 + 2.5, X_SAG_IC - 2.5, ON_ALT, S0 - 2.5, Z_CER0 - 1, Z_CER1 + 1))
    cer = cer.cut(kut(DEPO_ACIK[0], DEPO_ACIK[1], DEPO_ACIK[2], DEPO_ACIK[3], Z_CER0 - 1, Z_CER1 + 1))
    ek("onyuz_cerceve_saci_1.0", cer, "sac", "B_KASA", ("Ön çerçeve sacı 1,0", 1, "430 FERRİTİK 1,0 (manyetik fitil) · lazer kesim · %d açıklık" % (len(CEK) + 2), "fitil buna basar"))
    return L, GID


def _gider_katilari():
    A = GIDER["ana"]
    ana = SC0.yol_kati(A, R_ANA).val()
    dis = SC0.yol_kati(A, R_KILIF).val()
    out = dict(ana=ana, dis=dis, dal={}, kilif={}, kelepce={}, delici=[dis])
    for yan in ("sol", "sag"):
        out["dal"][yan] = SC0.yol_kati(GIDER[yan], R_DAL).val().cut(ana)
    for i, x0_ in enumerate(BOLME_X):
        k_ = dis.intersect(SC0.kut(x0_, x0_ + BOLME, 100.0, 300.0, -800.0, -680.0).val())
        if k_.Volume() > 1e-3:
            out["kilif"][BOLME_AD[i]] = k_.cut(ana)
    for k_, xk in X_KELEPCE.items():
        out["kelepce"][k_] = SC0.kut(xk - 5.0, xk + 5.0, Y_TABAN, y_ana(xk), Z_ANA - R_KILIF, Z_ANA + R_KILIF).val().cut(ana)
    return out


def _teknik(v1, ek, sac, pu):
    """teknik sütun: Secop (v14 K4 ünitesi taşınır) + montaj rayları + contalar + tava + serpantin + servis paneli + pano (v14 cihazları yeniden dizilir)"""
    L0 = []
    V1 = {p["ad"]: p for p in v1}
    T = lambda ad, dx, dy=0.0, dz=0.0: V1[ad]["wp"].translate((dx, dy, dz))
    for ad in ("sogutma_grubu_taban", "sogutma_grubu_taban_contasi", "sogutma_grubu_kondenser", "sogutma_grubu_fan", "sogutma_grubu_kompresor") + tuple("sogutma_grubu_takozu_%d" % i for i in range(4)):
        ek(ad, T(ad, SECOP_DX), V1[ad]["mal"], "B_SOGUTMA", V1[ad]["bom"])
    for ad_, (rz0, rz1, dk) in SC0.RAY_SEC.items():
        rd = (rz0, rz0 + SC0.SECOP_RAY_T) if dk < 0 else (rz1 - SC0.SECOP_RAY_T, rz1)
        ray_ = kut(T0, X_SAG_IC, Y_PLINT + 1.5, Y_PLINT + 1.5 + SC0.SECOP_RAY_T, rz0, rz1).union(kut(T0, X_SAG_IC, Y_PLINT + 1.5, Y_PLINT + 41.5, rd[0], rd[1]))
        ek("sogutma_grubu_montaj_rayi_" + ad_, ray_, "celik", "B_SOGUTMA",
           ("Yoğuşturucu montaj rayı L 40×40×3", 2, "AISI 304 köşebent · %.0f boy · uç plakası B5 bölme sacına / sağ dış saca 2 × M6" % (X_SAG_IC - T0), "ön ray SÖKÜLÜR (servis: ünite öne çekilir)") if ad_ == "arka" else None)
    sx0, sx1 = SC0.SECOP_X[0] + SECOP_DX, SC0.SECOP_X[1] + SECOP_DX
    kc = kut(T0, X_SAG_IC, Y_PLINT + 1.5, S0, -504.0, -494.0).cut(kut(sx0, sx1, Y_PLINT + 1.5, SC0.SECOP_Y0 + 297.0, -505.0, -493.0))
    ek("tk_kondenser_contasi", kc, "conta", "B_SOGUTMA",
       ("Kondenser çevre contası EPDM sünger", 1, "ünitenin iki yanı (10) + üstü (5) · kondenser düzleminde: emiş (arka hava odası) ↔ atış (ön) ayrımı", "titreşim geçmez"))
    # tava + sıcak gaz serpantini (hava odasının tabanında, arkada)
    t_ = TAVA_T
    ek("buharlastirma_tavasi", kut(*t_).cut(kut(t_[0] + 1.5, t_[1] - 1.5, t_[2] + 1.5, t_[3] + 1.0, t_[4] + 1.5, t_[5] - 1.5)), "sac", "B_SOGUTMA",
       ("Buharlaştırma tavası 1,5 · sıcak gaz serpantinli", 1, "304 · %.0f × %.0f × %.0f · brüt %.1f L · iki evaporatörün ana gideri ördek gagasıyla üstüne biter" % (
           t_[1] - t_[0], t_[3] - t_[2], t_[5] - t_[4], (t_[1] - t_[0] - 3) * (t_[3] - t_[2] - 1.5) * (t_[5] - t_[4] - 3) / 1e6),
        "hava odası emiş havasında (serin) → buharlaştırmayı basma hattından serpantin yapar (Secop OEM onayı · v2 E tasarımıyla aynı ilke)"))
    yc = t_[2] + 8.0
    pts = [(t_[0] + 15.0, yc, t_[4] + 15.0)]
    zz = [t_[4] + 15.0, t_[5] - 15.0]
    for j_, x_ in enumerate((t_[0] + 15.0, t_[0] + 95.0, t_[0] + 175.0, t_[0] + 255.0, t_[1] - 15.0)):
        pts.append((x_, yc, zz[j_ % 2])); pts.append((x_, yc, zz[(j_ + 1) % 2]))
    pts = [pts[0]] + pts[2:]
    ek("sicak_gaz_serpantini", SC0.yol_kati(pts, 3.175), "bakir", "B_SOGUTMA",
       ("Sıcak gaz serpantini Cu Ø6,35", 1, "Secop basma hattından tava tabanında 5 geçiş · kondensere döner", "hat bağlantıları soğutmacıda (modellenmedi)"))
    # servis paneli (atış yarıklı) + klipsler
    a_, b_ = KAPAK_X["T"]
    ds = kut(a_, b_, SERVIS_PANEL_Y[0], SERVIS_PANEL_Y[1], Z_ON0, Z_ON1).cut(kut(a_ + 1.5, b_ - 1.5, SERVIS_PANEL_Y[0] + 1.5, SERVIS_PANEL_Y[1] - 1.5, Z_ON0 - 1, Z_ON1 - 1.5))
    for xa_, xb_, ya_, yb_ in PANEL_YARIK:
        ds = ds.cut(kut(xa_, xb_, ya_, yb_, Z_ON1 - 2.0, Z_ON1 + 1.0))
    ek("tk_kapak_sogutma_dis_sac", ds, "sac", "B_SOGUTMA",
       ("Teknik sütun servis paneli 1,5 · lazer yarıklı", 1, "304 fırçalı · %d yarık 145 × 8 net %.0f cm² (Secop atışı) · 4 gizli klipsle sökülür" % (
           len(PANEL_YARIK), sum((q - p) * (t - r) for p, q, r, t in PANEL_YARIK) / 100.0), "menteşe YOK"))
    for i_, (xa_, xb_) in enumerate(((a_ + 1.5, T0 + 1.5), (X1 - 28.5, X1 - 1.5))):
        for j_, y_ in enumerate((200.0, 400.0)):
            ek("tk_panel_klipsi_%d" % (2 * i_ + j_), kut(xa_, xb_, y_ - 10.0, y_ + 10.0, Z_CER1, Z_ON0 + 6.0), "celik", "B_SOGUTMA",
               ("Gizli panel klipsi Fastmount", 4, "paslanmaz erkek + dişi", "") if i_ == 0 and j_ == 0 else None)
    # pano (arka üst · emiş hacmi): v14 cihazları yeniden dizilir — üst sıra PLC + 4 modül · alt sıra EM-324C + 21 röle + NDR-240 · klemens
    ZP = -DZ + 1.5; DZ_P = (ZP + 2.0 + 7.5) - (SC0.Z_ARKA + 2.0 + 7.5)             # cihaz arka yüzü −819 (v14 −780,5)
    ek("pano_montaj_plakasi", kut(T0 + 6.5, X_SAG_IC - 6.5, 455.0, 745.0, ZP, ZP + 2.0), "sac", "B_ELEKTRIK", ("Pano montaj plakası 2 mm", 1, "galvaniz · teknik sütunun arka duvarında", "depo arka paneli sökülünce önden erişilir"))
    for i_, yr in enumerate((502.5, 637.5)):
        ek("din_ray_%d" % i_, kut(T0 + 8.5, X_SAG_IC - 8.5, yr, yr + 35.0, ZP + 2.0, ZP + 9.5), "celik", "B_ELEKTRIK", ("DIN ray TS35 × 7,5", 2, "", "") if i_ == 0 else None)
    x_1 = T0 + 11.5 - 2041.5; dy_ = 470.0 - 145.0
    for ad in ("plc_S7-1200_1214C", "plc_SM1221_DI16_a", "plc_SM1221_DI16_b", "plc_SM1221_DI16_c", "plc_SM1222_DQ16", "surucu_EM-324C") + tuple("role_%02d" % (i + 1) for i in range(len(CEK))):
        ek(ad, T(ad, x_1, dy_, DZ_P), V1[ad]["mal"], "B_ELEKTRIK", V1[ad]["bom"])
    xr = 2117.5 + x_1 + len(CEK) * 6.2 + 4.0
    ek("guc_kaynagi_NDR-240-24", T("guc_kaynagi_NDR-240-24", xr - 2335.5, 610.0 - 132.5, DZ_P), V1["guc_kaynagi_NDR-240-24"]["mal"], "B_ELEKTRIK", V1["guc_kaynagi_NDR-240-24"]["bom"])
    zd = ZP + 9.5
    ek("klemens_blogu", kut(xr + 67.0, X_SAG_IC - 12.0, 625.0, 680.0, zd, zd + 45.0), "plastik", "B_ELEKTRIK", V1["klemens_blogu"]["bom"])
    return L0


def _gider_parcalari(GK):
    L = []
    B_ = "B_SOGUTMA"
    L_ = sum(math.dist(u, v) for u, v in zip(GIDER["ana"], GIDER["ana"][1:]))
    L.append(dict(ad="gider_ana_hatti_borusu", wp=cq.Workplane(obj=GK["ana"]), mal="plastik", birim=B_, grup="SABIT",
                  bom=("Gider ana hattı Ø20 × 1,5 PVC", 1, "iki evaporatör gideri (K2 arkası x %.0f · K5 arkası x %.1f, T girişli) · arkada yerde z %.0f, sürekli %%%.1f eğim → teknik sütunun "
                       "hava odasında buharlaştırma tavasına" % (EVAP["sol"]["gider"][0], EVAP["sag"]["gider"][0], Z_ANA, 100 * EGIM), "boy %.0f mm · bölme geçişleri Ø24 kılıfta" % L_)))
    for yan in ("sol", "sag"):
        L.append(dict(ad="gider_borusu_%s" % yan, wp=cq.Workplane(obj=GK["dal"][yan]), mal="plastik", birim=B_, grup="SABIT",
                      bom=("Gider borusu Ø12 × 1 PVC", 2, "damlama teknesinden ana hatta T · ≥ %1", "") if yan == "sol" else None))
    for i_, (ad_, k_) in enumerate(GK["kilif"].items()):
        L.append(dict(ad="gider_ana_hatti_kilifi_" + ad_, wp=cq.Workplane(obj=k_), mal="plastik", birim=B_, grup="SABIT",
                      bom=("Gider ana hattı kılıfı Ø24 × 2 PVC", len(GK["kilif"]), "bölme PU'su içinde · içinden Ø20 boru kayar", ", ".join(GK["kilif"])) if i_ == 0 else None))
    for i_, (ad_, k_) in enumerate(GK["kelepce"].items()):
        L.append(dict(ad="gider_ana_hatti_kelepcesi_" + ad_, wp=cq.Workplane(obj=k_), mal="plastik", birim=B_, grup="SABIT",
                      bom=("Boru eyeri Ø20 · PA", len(GK["kelepce"]), "taban iç sacına 2 × perçin", "K3 · K5 · K6") if i_ == 0 else None))
    x_, y_, z_ = GIDER["ana"][-1]
    L.append(dict(ad="gider_cek_valfi", wp=sily(x_, z_, 11.5, y_ - 11.0, y_ - 1.0), mal="silikon", birim=B_, grup="SABIT",
                  bom=("Ördek gagası çek valf Ø20 (Minivalve DU sınıfı)", 1, "silikon · kuru kapan (tava kurusa da koku / sıcak hava geri gelmez)", "ölçü katalogdan teyit [VARSAYIM]")))
    return L


def _evaporatorler(v1):
    L = []
    for p in v1:
        a = p["ad"]
        for yan in ("sol", "sag"):
            if a.startswith(("evaporator_%s_" % yan, "fan_%s_" % yan, "fan_davlumbazi_%s" % yan, "damlama_teknesi_%s" % yan)):
                L.append(dict(p, wp=p["wp"].translate((EV_DX[yan], 0.0, 0.0))))
    return L


def _depo():
    """v14 k4_depo_cekmecesi() teknik sütunun depo bölmesinde (K4X/K4_SAG · kutu / ray boyu v3) + kapak_on"""
    kay = dict(K4X=SC0.K4X, K4_SAG=SC0.K4_SAG, DEPO_KUTU_D=SC0.DEPO_KUTU_D, DEPO_KUTU_UST=SC0.DEPO_KUTU_UST, DEPO_SUCUK_W=SC0.DEPO_SUCUK_W,
               RAY_L=SC0.RAY_L, PARCALAR=SC0.PARCALAR)
    try:
        SC0.K4X, SC0.K4_SAG = T0, X_DEPO_SAG - 1.0                              # sağ iç sacın iç yüzü (v14'te K4_SAG = B4 sacının yüzü)
        SC0.DEPO_KUTU_D, SC0.DEPO_KUTU_UST, SC0.DEPO_SUCUK_W, SC0.RAY_L = DEPO_KUTU_D, DEPO_KUTU_UST, DEPO_SUCUK_W, DEPO_RAY_L
        SC0.PARCALAR = []
        SC0.k4_depo_cekmecesi(S0 + 30.0)
        a_, b_ = KAPAK_X["T"]
        SC0.kapak_on("k4_kapak_depo", a_, b_, DEPO_KAPAK_Y[0], DEPO_KAPAK_Y[1], "B_DEPO", DEPO_ACIK, grup="CEKMECE",
                     bom=("Depo çekmecesi önü 40 · kulpsuz · bas-aç", 1, "dış 304 1,5 + PU 37,5 + iç 304 1,0 · fitilli", "%.0f × %.0f" % (b_ - a_, DEPO_KAPAK_Y[1] - DEPO_KAPAK_Y[0])))
        L = SC0.PARCALAR
    finally:
        for k_, v_ in kay.items(): setattr(SC0, k_, v_)
    out = []
    for p in L:
        a = p["ad"].replace("k4_", "tk_", 1)
        b = p.get("bom")
        if b and "K4" in b[0]: b = (b[0].replace("K4", "Teknik sütun"),) + tuple(b[1:])
        out.append(dict(p, ad=a, bom=b))
    return out


def modul():
    """v3 dolap (dünya) → PARCALAR · özet [(kod, tip, n, ust, acik_ust)] · İDEMPOTENT"""
    t0 = time.time()
    if not SC0.PARCALAR: SC0.modul()
    v1 = list(SC0.PARCALAR)
    cek, ozet = _cekmeceler()
    kasa, GK = _kasa(v1)
    out = kasa + _gider_parcalari(GK) + _evaporatorler(v1) + _depo() + cek
    PARCALAR[:] = out
    adlar = [p["ad"] for p in out]
    assert len(adlar) == len(set(adlar)), sorted({a for a in adlar if adlar.count(a) > 1})[:10]
    RAPOR.update(sure=time.time() - t0, parca=len(out), cekmece=len(CEK))
    return ozet


def denetim(tarama=True):
    """v3 dolap öz denetimi: sayım (2 gün kuralı) · ön ızgara (126–785, 3 mm aralık) · tavan payları · kapalı + açık konum çakışma (store_cad_v14.cakisma)"""
    say = {}
    for c in CEK:
        say[c[2]] = say.get(c[2], 0) + 1
    stok = dict(lahm=say.get("lahm", 0) * H.TEPSI["lahmacun"], hamur=say.get("hamur", 0) * H.TEPSI["pide"], ic1=say.get("ic1", 0) * H.TEPSI["icecek"], tatli=say.get("tatli", 0) * H.TEPSI["tatli"])
    gun = dict(lahm=H.IKI_GUN["lahmacun"], hamur=H.IKI_GUN["pide"], ic1=H.IKI_GUN["icecek"], tatli=H.IKI_GUN["tatli"])
    print("SAYIM: %s · stok %s · 2 gün %s" % (say, stok, gun))
    assert all(stok[k] >= gun[k] for k in gun) and len(CEK) == 21, "2 gün kuralı tutmuyor"
    BB = {p["ad"]: p["wp"].val().BoundingBox() for p in PARCALAR}
    for kol in KOLON_AD:
        ps = [p for p in PARCALAR if p["birim"].startswith("CEK_%s_" % kol)]
        ust_p = max(BB[p["ad"]].ymax for p in ps if "_on_" not in p["ad"] and p["grup"] != "SABIT")
        ust_s = max(BB[p["ad"]].ymax for p in ps if p["grup"] == "SABIT")
        fit = max(BB[p["ad"]].ymax for p in ps if p["ad"].endswith("_on_fitil"))
        tav = TAVAN_KOL[kol]
        print("   KOLON %s: en üst hareketli %.1f · en üst sabit %.1f · fitil üstü %.1f · iç tavan %.0f" % (kol, ust_p, ust_s, fit, tav))
        assert ust_p <= tav - 2.0 and ust_s <= tav - 0.5 and fit <= tav + 0.01, "%s tavana değiyor" % kol
    on = sorted([b for a, b in BB.items() if a.endswith("_on_dis_sac_1.5") or a in ("tk_kapak_sogutma_dis_sac", "tk_kapak_depo_dis_sac_1.5")], key=lambda b: (b.xmin, b.ymin))
    for kol, (pa, pb) in KAPAK_X.items():
        sut = sorted((b for b in on if abs(b.xmin - pa) < 0.05 and abs(b.xmax - pb) < 0.05), key=lambda b: b.ymin)
        assert sut and abs(sut[0].ymin - ON_ALT) < 0.05 and abs(sut[-1].ymax - ON_UST) < 0.05, "%s: ön yüz 126–785 değil (%s)" % (kol, [(b.ymin, b.ymax) for b in sut])
        for u_, v_ in zip(sut, sut[1:]):
            assert abs(v_.ymin - u_.ymax - FUGA) < 0.05, "%s: önler arası %.1f" % (kol, v_.ymin - u_.ymax)
        print("   ÖN YÜZ %-3s x %7.1f–%7.1f · %d önü · aralar 3" % (kol, pa, pb, len(sut)))
    xs = sorted(KAPAK_X.values())
    assert all(abs(b[0] - a[1] - FUGA) < 0.05 for a, b in zip(xs, xs[1:])) and abs(xs[0][0] - X0) < 0.01 and abs(xs[-1][1] - X1) < 0.01
    zmx = max(b.zmax for b in BB.values()); zmn = min(b.zmin for b in BB.values()); ymx = max(b.ymax for b in BB.values())
    xmn = min(b.xmin for b in BB.values()); xmx = max(b.xmax for b in BB.values())
    print("ZARF: x %.1f–%.1f · y üst %.1f · z %.1f … %.1f" % (xmn, xmx, ymx, zmn, zmx))
    assert abs(zmx - Z_ON1) < 0.01 and abs(zmn - Z_ARKA_DIS) < 0.01 and abs(ymx - H_B) < 0.05 and abs(xmn - X0) < 0.01 and abs(xmx - X1) < 0.01
    depo = [p for p in PARCALAR if p["ad"] == "tk_depo_kutu_U_1.5"][0]["wp"].val().BoundingBox()
    ic_w = depo.xlen - 3.0 - 1.5 - DEPO_SUCUK_W - 1.5; ic_h = depo.ylen - 1.5; ic_d = depo.zlen - 3.0
    kas_L, suc_L = ic_w * ic_h * ic_d / 1e6, DEPO_SUCUK_W * ic_h * ic_d / 1e6
    print("DEPO: kaşar bölmesi %.1f L (2 gün %.1f) · sucuk %.1f L (2 gün %.1f)" % (kas_L, H.DEPO_L["kasar"], suc_L, H.DEPO_L["sucuk"]))
    assert kas_L >= H.DEPO_L["kasar"] and suc_L >= H.DEPO_L["sucuk"], "depo 2 günü almıyor"
    if tarama:
        kay = SC0.PARCALAR
        try:
            SC0.PARCALAR = PARCALAR
            SC0.cakisma(1.0)
        finally:
            SC0.PARCALAR = kay


if __name__ == "__main__":
    t0 = time.time()
    oz = modul()
    print("v3 dolap: %d parça · %d çekmece · %.0f sn" % (len(PARCALAR), len(CEK), time.time() - t0))
    for c in CEK: print("   ", c, HH_C[c[1]])
    denetim(tarama="hizli" not in sys.argv)
    print("DENETIM TAMAM · %.0f sn" % (time.time() - t0))
    sys.stdout.flush(); os._exit(0)
