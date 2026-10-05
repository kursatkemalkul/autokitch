# -*- coding: utf-8 -*-
"""HAT VERSİYON 3 · HESAP v1 (30 Eyl 2026 · Claude · YEREL) — v3 yerleşiminin TEK SAYI KAYNAĞI (bütün h3_* üreteçleri buradan okur).
Kemal (HAT v2.7 önerisi → "bunu da v3 olarak kur · harçla sosun çıkışı sola gitmesin, direkt aşağıya insin, o aralarından en uygun şekilde ·
sorunları çöz ama basit çözümler, kompleksleştirmeden temiz"):
  · TOPPING'in sol duvarı kıyma haznesinin dibinde (1436) · üst katta YALNIZ 2 UNO (sos + harç, 2 günlük hazneler) · kaşar/sucuk yedeği TOPPING'den çıktı
  · sos + harç ÇIKIŞI DİK İNER: yayıcılar alt kat dozajlayıcılarının ARASINDA (sos 1645 · harç 2190 [v3.6, v3.4 2160]: kaşar kulpu ≤ 2168 ile kılavuzu 2202,5 arası · sucuk mandalı 2217'de · hortum DÜMDÜZ iner) · yayıcı ağzı kaset iniş borularıyla aynı kotta (1048)
    → her ürün her ağzın altından geçer (pide koridoru üstü 1033), tabla istasyonları x sırasıyla gezer (pizza: sos → kaşar → sucuk)
  · A açıcı 700 AYNI (Kemal: hamur açma yerine dokunma) — yalnız sağa kayar (sol uç 507,5 → 736)
  · çöp dolaptan çıktı · yağ tenekesi fırın üstünde sağda (kompresör sola) · dolabın soğutma grubu + panosu + kaşar/sucuk deposu DOLABIN KENDİ
    teknik sütununda (K'nin altı, v14'teki K4'ün aynı düzeni: Secop önde altta · pano arkada · ara PU · soğuk depo üstte) · robot çöpü E'nin altında
YÖNTEM: v2 (h2_*) adaptörlerinin kopyası; sol grup v1'e göre DXL = 736 kayar (v2 507,5) · SAĞ TARAF SABİT (F 2500–4000 · K 4000–4400 · E 4400–5230)."""
import math

# ---------------------------------------------------------------- SATIŞ (kural kitabı 2.1 · 2.3)
GUN = dict(pide=80, lahmacun=200, icecek=69.25, tatli=5.5)
KUTU_GUN = 80 + 200 / 2

# ---------------------------------------------------------------- SOĞUK DOLAP (B) · TAM 2 GÜN (5.2)
TEPSI = dict(lahmacun=42, pide=25, icecek=48, tatli=12)                     # store_cad_v14 tepsileri (6×7 · 5×5 · 6×8 · 4×3)
IKI_GUN = dict(lahmacun=400, pide=160, icecek=139, tatli=11)
CEKMECE = {k: math.ceil(IKI_GUN[k] / TEPSI[k]) for k in TEPSI}             # 10 · 7 · 3 · 1 = 21 (en az)
assert CEKMECE == dict(lahmacun=10, pide=7, icecek=3, tatli=1), CEKMECE
STOK = {k: CEKMECE[k] * TEPSI[k] for k in TEPSI}

# ---------------------------------------------------------------- GENİŞLİK ZİNCİRİ (dünya x)
DXL = 736.0                                     # sol grubun v1'e göre kayması (v2 507,5 · v3 +228,5 daha)
X0 = DXL
A_X = (X0, X0 + 700.0)                          # A açıcı 736–1436 (700 AYNI)
C_X = (A_X[1], 2500.0)                          # TOPPING 1436–2500 = 1064 (v2 1292,5 · v1 1800)
F_X = (2500.0, 4000.0)
K_X = (4000.0, 4400.0)
E_X = (4400.0, 5230.0)
HAT_BOY = E_X[1] - X0                           # 4494 (v2 4722,5 · v1 5230)
B_X = (X0, K_X[1])                              # çekmeceli dolap 736–4400 (v3: K'nin altına uzar — teknik sütun)
W_B = B_X[1] - B_X[0]                           # 3664
C_DILIM = (1614.0 - DXL, 1614.0)                # TOPPING + C kaidesinden çıkan dilim (v1 dünya x 878 … 1614)
B_DILIM = (2500.0 - DXL, 2500.0)                # (yalnız h3_moduler'in eski dilim sözleşmesi için · dolap v3'te baştan kurulur)
assert abs((C_DILIM[1] - C_DILIM[0]) - DXL) < 1e-9
ROBOT_RAY_X = (200.0 + DXL, 5100.0)             # 936–5100
X_ROB_AC = 700.0 + DXL                          # 1436 · robot topu açıcıya bırakırken (v1 geometrisiyle aynı bağıl)

# ---------------------------------------------------------------- KOTLAR (dünya y)
Y_PLINT, Y_DUZ, Y_MEK, Y_TABLA = 123.0, 788.0, 892.0, 1000.0
H_IST = 1862.0
H_UST = 2200.0
UST_DEPO_Y = (H_IST, H_UST)

# ---------------------------------------------------------------- TOPPING v3
T_RAF_UST = (1572.0, 1575.0)
T_IC_TAVAN = H_UST - 1.5 - 58.5                 # 2140
# istasyonlar (tabla ekseni x): alt kat v2 ile aynı · yayıcılar alt kat dozajlayıcılarının arasında, UNO'larının tam altında
IST_V3 = {"SOS": 1645.0, "HARC": 2190.0, "KIYMA": 1596.0, "KUSBASI": 1806.0, "KASAR": 2062.0, "SUCUK": 2311.0}
Y_AGIZ = 1048.0                                 # bütün dozaj ağızlarının alt ucu (kaset iniş boruları v2 ile aynı · yayıcılar da buraya çıktı)
Y_KORIDOR = 1000.0 + 28.0 + 5.0                 # pide koridoru üstü (montaj denetimi: Ø300 × 28 + üst malzeme 5)
assert Y_AGIZ - Y_KORIDOR >= 10.0

# ---------------------------------------------------------------- ÇEKMECELİ DOLAP v3 (dünya x) · kolon 620 (K6 585) · bölme 35 · sol duvar 62,5
KOLON_V3 = {"K1": 798.5, "K2": 1453.5, "K3": 2108.5, "K5": 2763.5, "K6": 3418.5}
KOLON_W_V3 = {"K1": 620.0, "K2": 620.0, "K3": 620.0, "K5": 620.0, "K6": 575.0}   # K6 575 (v1/v2 585): tatlı tepsisi 420 + içecek 492 · kutu içi 515 · teknik sütuna 10 mm
BOLME_V3 = [KOLON_V3[k] + KOLON_W_V3[k] for k in ("K1", "K2", "K3", "K5", "K6")]   # 1418,5 · 2073,5 · 2728,5 · 3383,5 · 3993,5 (35'lik bölmelerin sol yüzü)
T_X = (BOLME_V3[-1] + 35.0, B_X[1])             # TEKNİK SÜTUN 4028,5–4400 (K'nin altı): Secop + pano + ara PU + soğuk depo · iç genişlik 370 (Secop 350 + 2 × 10)
assert abs(KOLON_V3["K1"] - (X0 + 62.5)) < 1e-9
for _a, _b in (("K1", "K2"), ("K2", "K3"), ("K3", "K5"), ("K5", "K6")):
    assert abs(KOLON_V3[_b] - (KOLON_V3[_a] + KOLON_W_V3[_a] + 35.0)) < 1e-9, (_a, _b)
# çekmeceler (alttan üste) · S = küçük açıklık (75; tatlı 71 → 75 kolonuna) · L = büyük (130) · fırın altı kolonlarında tavan 668 (ısı kalkanı)
DOLAP_V3 = {"K1": ["lahm"] * 5, "K2": ["lahm"] * 5,
            "K3": ["hamur"] * 4,                                   # yarısı fırın altında → alçak kolon (4 küçük)
            "K5": ["hamur"] * 3 + ["ic1"],                         # 3 pide + 1 içecek (üstte büyük)
            "K6": ["tatli"] + ["ic1"] * 2}                         # 1 tatlı + 2 içecek
_say = {}
for _k, _l in DOLAP_V3.items():
    for _t in _l: _say[_t] = _say.get(_t, 0) + 1
assert _say == {"lahm": 10, "hamur": 7, "ic1": 3, "tatli": 1}, _say
DEPO_L = dict(kasar=22.5, sucuk=6.6)            # 5.4: 2 gün kasette + 2 gün soğuk depoda (teknik sütunun üstü, v14 K4 deposu gibi tek kap bölmeli)

# ---------------------------------------------------------------- KUTU · İÇECEK YEDEĞİ (4 güne kadar dışarıda · v2 ile aynı)
KUTU_4GUN = 4 * KUTU_GUN
KUTU_SARJOR, KUTU_YEDEK = 432, 320
ICECEK_4GUN = math.ceil(4 * GUN["icecek"])
KOLI = dict(adet=24, x=400.0, z=267.0, y=123.0)
ICECEK_YEDEK_KOLI = math.ceil((ICECEK_4GUN - STOK["icecek"]) / KOLI["adet"])
assert ICECEK_YEDEK_KOLI == 6
# v2 sözleşmesi (h3_topping artık kullanmaz — kaşar/sucuk GN yedeği TOPPING'den çıktı)
KASAR_2GUN_L, SUCUK_2GUN_L = DEPO_L["kasar"], DEPO_L["sucuk"]
GN_KASAR = dict(ad="GN 1/1-200", x=530.0, z=325.0, y=200.0, L=28.0)
GN_SUCUK = dict(ad="GN 1/2-150", x=325.0, z=265.0, y=150.0, L=9.5)

# ---------------------------------------------------------------- FIRIN ÜSTÜ (F üst kabini) · kompresör sola, yağ tenekesi sağa
# fırın üstü iç genişlik 1501,5–3998,5: pizza yedeği 2520–3324 (DEĞİŞMEZ) · tavan kirişi + tek ön dikme 3326–3356 · kompresör raf açıklığı 3358–3740 ·
# yağ tavası 3742–3985 · teneke 3746–3981 (sağ gazlı yay 3982–3997 önde: teneke öne çekilir)  → pay 2 + 2 + 2 mm
KIRIS_X = (3326.0, 3356.0)                      # fırın üstü tavan kirişi + ön dikme (v2: kiriş 3336–3366 + 2. dikme 3560–3590 — kompresörün önünde kalırdı)
KOMP_ACIKLIK_X = (3358.0, 3740.0)               # raf açıklığı (v2 3595–3991) · kompresör tavası 3359–3739
KOMP_DX = 3359.0 - 3600.0                       # −241 · JUN-AIR OF302-15B tankı 3600–3980 → 3359–3739
YAG_X = (3742.0, 3985.0)                        # yağ tavası (teneke + 238 tartı) · kompresör açıklığının 2 sağı

if __name__ == "__main__":
    print("A", A_X, "C", C_X, "F", F_X, "K", K_X, "E", E_X, "B", B_X, "· hat", HAT_BOY)
    print("dolap kolonları", KOLON_V3, "bölmeler", BOLME_V3, "teknik sütun", T_X)
    print("çekmece", _say, "stok", STOK)
