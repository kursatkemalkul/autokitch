# -*- coding: utf-8 -*-
"""hat_montaj_v34 -> v35 : HAT ATOSA TABLALI v7 YERLESIMI + TABAN HIZASI + SUREC KOTU 1168

Kemal (24 Eyl 2026): "su an teknik resmimizdeki gibi yapacagiz. Firin, topping, hamur acma,
kesme-sprey ve kutu — hepsinin alt tabanlari ayni hizada olacak; tabla, bant, kesme, sprey ve
kutu da ayni hizada. Kesme plakasi-sprey istasyonunun tabani da ayni yerden kesilsin, ayri
istasyon olsun. Karton kutu katlama tek uzun olacak, onu kesme." · "kutulari kaldir ordan
yedek kutulari" · kot secimi: "B'yi yap" (TOPPING'e dokunma, digerleri tablanin kotuna insin).

DEGISEN
  · Yerlesim HAT 2 KOL v19 yerine ATOSA TABLALI v7'den okunur: A 700 · C 1800 · F 1500 · K 600 · E 700 = 5300.
    (v34 hala v19'un 700'luk KATLI FIRIN kolonunu ve iki robotunu ciziyordu.)
  · TABAN HIZASI: A, C, F, K istasyonlari H_B = 1060'ta baslar; altlari taban dolabi (B cekmeceleri,
    F tabani: pano/UPS/bulasik makinesi, K tabani: yag + kart). E kesilmez: 0-2030 tek parca.
  · SUREC KOTU TOPPING'den OLCULUR: calisma diski ustu 1168, firin bandi 1166 (TOPPING'deki aktarma
    bandinin devami, ayni 290 genislik ve eksen z -170), kesme plakasi 1164, kutu tepsisi 1104.
    Urun hep 2 mm ASAGI iner — yukari basamak olursa pide plakanin kenarina carpar.
  · K'deki 4 gunluk YEDEK KUTU kaldirildi.
  · Tek robot (FR5) yer rayinda + QR dolabi, paftadaki yerlerinde.
  · Harf esleme: sitede firin sayfasi modul_D'yi yukluyor -> firin (paftada F) D harfinde kaldi;
    K yeni modul (modul_K.glb).
DENETIM: surec kotu CAD'den olculur ve assert edilir; taban hizasi assert edilir; TOPPING CAD
  parcalari ile yeni F/K/E birimleri arasindaki kesisimler RAPOR edilir (durdurmaz).
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v34.py"), encoding="utf-8").read()

# ------------------------------------------------------------------ 0) basliga v35 notu
s = s.replace('"""v7 (22 Eyl 2026): GLB yazicisi', '''"""v35 (24 Eyl 2026): YERLESIM = HAT ATOSA TABLALI v7 (A 700 · C 1800 · F 1500 · K 600 · E 700 = 5300).
TABAN HIZASI: A, C, F, K istasyonlari 1060'ta baslar, altlari taban dolabi; E (kutu katlama) 0-2030 TEK PARCA.
SUREC KOTU TOPPING'den olculur (Kemal "B"): disk 1168 · firin bandi 1166 · kesme plakasi 1164 · kutu tepsisi 1104.
K'deki yedek kutular kaldirildi. Tek FR5 yer rayinda + QR dolabi. Onceki: hat_montaj_v34.py
v7 (22 Eyl 2026): GLB yazicisi''', 1)

# ------------------------------------------------------------------ 1) yerlesim blogu
a = s.index("# ---------------------------------------------------------------- PAFTA v19'DAN OKUNAN")
b = s.index("\n", s.index("MODUL_Y = {")) + 1
YENI_YER = r'''# ---------------------------------------------------------------- v35 · PAFTA: HAT ATOSA TABLALI v7 ----------------------------------------------------------------
# Yerlesim (modul genislikleri, firin/kesme/kutu ic duzeni, robot, QR) ATOSA TABLALI v7'den OKUNUR.
# Cekmece modulu B'nin ic verisi (kolonlar, kotlar) v19 ile BIREBIR ayni ("ORTAK VERI") -> v19'dan okunmaya devam eder.
_p = open(os.path.join(U, "teknik_hat_2kol_v19.py"), encoding="utf-8").read()
_g = {"__name__": "_pafta", "os": os, "math": math}
exec(_p[_p.index("# ======================= VERI ======================="):_p.index("# ======================= YERLESIM =======================")], _g)
_p7 = open(os.path.join(U, "teknik_hat_atosa_tablali_v7.py"), encoding="utf-8").read()
_g7 = {"__name__": "_pafta7", "os": os, "math": math}
exec(_p7[_p7.index("# ======================= ORTAK VERI (HAT 2 KOL v19) ======================="):_p7.index("\nOX, FY_TOP")], _g7)
DZ, H_MAK, H_B = _g7["DZ"], _g7["H_MAK"], _g7["H_B"]                                    # 830 · 2030 · 1060 (TABAN HIZASI)
X_A, W_A, X_BC, W_BC, W_B = _g7["X_A"], _g7["W_A"], _g7["X_C"], _g7["W_C"], _g7["W_B"]   # A 0-700 · C 700-2500 · B 0-2500
X_D, W_D = _g7["X_F"], _g7["W_F"]                # FIRIN: paftada F, sitede oven.html modul_D'yi yukluyor -> harf D
X_K, W_K, X_E, W_E = _g7["X_K"], _g7["W_K"], _g7["X_E"], _g7["W_E"]
HAT_W = _g7["HAT"]                                                                       # 5300
HAZNE = _g7["HAZNE"]                                                                     # firin pisirme haznesi 1400
RZ, OMUZ, ERISIM, RX = _g7["RZ"], _g7["OMUZ"], _g7["ERISIM"], _g7["RX"]
QRX, QRZ = _g7["QRX"], _g7["QRZ"]
KOLON, KOL_Y0, K1_TABAN = _g["KOLON"], _g["KOL_Y0"], _g["K1_TABAN"]
import topping_hesap_v6 as TH, topping_cad_v22 as TC                                      # TOPPING modülü: derinlik dizilimi ve yuva konumları ORADAN okunur
KASET_Z = (TH.Z_KASET[1], TH.Z_KASET[0])
T_KAS = (H_B + TC.KAS[0], H_B + TC.KAS[1])        # v35: kaset kotu CAD'den (paftadaki 1627 VARSAYIMDI)

# ---- v35 · SUREC KOTU (Kemal 24 Eyl "B": TOPPING'e dokunma, digerleri tablanin kotuna insin) ----
# Sayilar topping_cad_v22'den; yazildiktan sonra ASAGIDA parcalarin gercek kutusundan OLCULUP assert edilir.
DISK_UST_Y = 108.0                                # calisma_diski ust yuzu (yerel y)
P = H_B + DISK_UST_Y                              # 1168
BANT_UST = H_B + 106.0                            # 1166 · firin bandi ust kosu (CAD AKT_Y: diskin 2 mm alti)
ZT = TH.Z_KASET[0] + 30.0                         # -170 · tabla ekseni (topping_cad_v22 ile ayni formul)
BANT_Z = (ZT - 145.0, ZT + 145.0)                 # 290 genis · TOPPING'deki aktarma bandiyla ayni
BANT_X0 = X_BC + 2195.0                           # CAD'deki aktarma bandinin tahrik silindiri (hat x 2895) -> devam buradan
PLAKA = BANT_UST - 2.0                            # 1164 · kesme plakasi bandin 2 mm ALTINDA: urun hep asagi iner
TEPSI_Y = PLAKA - 60.0                            # 1104 · kutu tepsisi yuzu (pafta kurali: surec - 60) -> kutu agzi ~1149
E_A0, E_A1 = PLAKA - 90.0, PLAKA + 160.0          # kutulama agzi (pafta: P-90 ... P+160)
F_G1 = BANT_UST + 320.0                           # 1486 · firin govdesi ustu (pafta: bant + 320)
KAIDE = OMUZ - 152.0                              # FR5 taban -> omuz 152 [katalog Fairino FR5 d1]

MODUL = [("A", "MODÜL A · KONİLİ AÇICI (B üstünde)", X_A, W_A), ("B", "MODÜL B · ÇEKMECELER (taban)", X_A, W_B),
         ("C", "MODÜL C · TOPPING (B üstünde)", X_BC, W_BC), ("D", "MODÜL F · KONVEYÖR FIRIN (+ taban)", X_D, W_D),
         ("K", "MODÜL K · KESME + SPREY (+ taban)", X_K, W_K), ("E", "MODÜL E · KUTU KATLAMA (tek parça)", X_E, W_E)]
MODUL_Y = {"A": (H_B, H_MAK), "B": (0.0, H_B), "C": (H_B, H_MAK), "D": (0.0, H_MAK), "K": (0.0, H_MAK), "E": (0.0, H_MAK)}
'''
s = s[:a] + YENI_YER + s[b:]

# ------------------------------------------------------------------ 2) eski D / E / 2 robot -> yeni A, F(D), K, E, robot, QR
a = s.index('birim("D_KABIN"')
b = s.index("DURUM_RENK = ")
YENI_BIRIM = r'''birim("A_KABIN", "AÇICI modülü kabini (B üstünde · açıcının kendisi TOPPING CAD'inde)", "A", "KUTU", (X_A, X_A + W_A), (H_B, H_MAK), (-DZ, 0.0), "kabin", "pafta ATOSA TABLALI v7")

# ============================ v35 · TABAN HIZASI ============================
# Kemal 24 Eyl: A, C, F(D), K istasyonlarinin ALT TABANI AYNI HIZADA (H_B = 1060); altlari taban dolabi.
# E (kutu katlama) KESILMEZ: yerden 2030'a tek parca (sarjor altta, katlama ustte).
# SUREC: disk 1168 > firin bandi 1166 > kesme plakasi 1164 > kutu agzi ~1149 — urun hep asagi iner.

# --- D · (paftada F) KONVEYOR FIRIN ---
birim("D_TABAN_KABIN", "F taban dolabı 0–1060 (pano · UPS · bulaşık makinesi)", "D", "KUTU", (X_D, X_D + W_D), (0.0, H_B), (-DZ, 0.0), "kabin", "v35 taban hizası")
for kod_, ad_, (a_, b_), (y0_, y1_), dz_, kat_, kay_ in (
        ("D_ROBOT_KONTROL", "Robot kontrol kutusu (FR5) · ray yanında", (60.0, 700.0), (135.0, 270.0), 180.0, True, "pafta v7 · 245 × 180 × 45"),
        ("D_ANA_PANO", "Ana pano · PLC · ana şalter · ekran yok (tablet)", (60.0, 460.0), (320.0, 670.0), 250.0, False, "pafta v7 · 400 × 350 × 250"),
        ("D_UPS", "UPS 500 VA", (480.0, 730.0), (320.0, 670.0), 350.0, True, "pafta v7 · derinlik VARSAYIM"),
        ("D_BULASIK", "Bulaşık makinesi · tezgâh altı · MEIKO M-iClean UM sınıfı · sepet 500 × 500", (760.0, 1220.0), (135.0, 865.0), 600.0, True, "MEIKO UM 460 × 600 × 730"),
        ("D_DETERJAN", "Makine deterjanı + parlatıcı 2 × 5 L bidon", (1250.0, 1440.0), (135.0, 500.0), 300.0, False, "pafta v7 · derinlik VARSAYIM")):
    birim(kod_, ad_, "D", "KATALOG" if kat_ else "KUTU", (X_D + a_, X_D + b_), (y0_, y1_), (-20.0 - dz_, -20.0), "katalog" if kat_ else "kutu", kay_)
birim("D_FIRIN_GOVDE", "Konveyör fırın gövdesi · özel · elektrikli · taban 1060 · bant altı pay 106 (alt ısıtma: ince rezistans / taş — VARSAYIM)", "D", "KUTU",
      (X_D, X_D + W_D), (H_B, F_G1), (-DZ, 0.0), "sicak", "pafta v7 · gövde tabanı 1040 -> 1060 (taban hizası), bant 1340 -> 1166 (Kemal B)")
birim("D_HAZNE", "Pişirme haznesi 1400 · aynı anda 4 ürün (adım 350) · üst + alt ısıtma", "D", "KUTU",
      (X_D + 50.0, X_D + 50.0 + HAZNE), (H_B + 20.0, BANT_UST + 270.0), (-500.0, -10.0), "sicak", "pafta v7 · ön duvar 10 (bant z -25'e kadar geliyor)")
birim("D_BANT", "Fırın bandı (devamı) · 290 · üst yüz 1166 · TOPPING'deki bıçak burunlu aktarma bandının devamı", "D", "KUTU",
      (BANT_X0, X_K + 15.0), (BANT_UST - 61.5, BANT_UST), BANT_Z, "koyu", "PTFE kaplı cam elyaf örgü · genişlik ve eksen topping_cad_v22'den")
birim("D_DAVLUMBAZ", "Egzoz davlumbazı · fan · yağ + karbon filtre · fırın kartı + SSR + kontaktör", "D", "KUTU", (X_D, X_D + W_D), (F_G1 + 10.0, H_MAK), (-DZ, 0.0), "kutu", "pafta v7")

# --- K · KESME + SPREY (ayri istasyon) ---
birim("K_TABAN_KABIN", "K taban dolabı 0–1060 · yedek kutu KALDIRILDI (Kemal 24 Eyl)", "K", "KUTU", (X_K, X_K + W_K), (0.0, H_B), (-DZ, 0.0), "kabin", "v35 taban hizası")
birim("K_YAG", "Yağ kartuşu 4 L × 2 · ısıtmalı", "K", "KUTU", (X_K + 60.0, X_K + 300.0), (140.0, 330.0), (-420.0, -20.0), "kutu", "pafta v7")
birim("K_KART", "K kontrol kartı · tahrik", "K", "KUTU", (X_K + 320.0, X_K + 540.0), (140.0, 330.0), (-220.0, -20.0), "kutu", "pafta v7")
birim("K_KABIN", "KESME + SPREY istasyonu kabini 1060–2030", "K", "KUTU", (X_K, X_K + W_K), (H_B, H_MAK), (-DZ, 0.0), "kabin", "v35 taban hizası")
birim("K_PLAKA", "Kesme plakası 560 × 450 · üstü 1164 (fırın bandının 2 mm altı)", "K", "KUTU", (X_K + 20.0, X_K + 580.0), (PLAKA - 14.0, PLAKA), (-470.0, -20.0), "sac", "pafta v7 · kot v35")
birim("K_ITICI", "İtici · kutuya süren", "K", "KUTU", (X_K + 24.0, X_K + 64.0), (PLAKA + 2.0, PLAKA + 50.0), (-470.0, -20.0), "kutu", "pafta v7")
birim("K_BICAK", "Yıldız bıçak Ø300 · 6 dilim · piston 100 strok", "K", "KUTU", (X_K + 110.0, X_K + 490.0), (PLAKA + 90.0, PLAKA + 340.0), (ZT - 150.0, ZT + 150.0), "kutu", "pafta v7")
birim("K_SPREY", "Tereyağı spreyi", "K", "KUTU", (X_K + 505.0, X_K + 535.0), (PLAKA + 105.0, PLAKA + 135.0), (ZT - 15.0, ZT + 15.0), "kutu", "pafta v7")
birim("K_ICECEK_YEDEK", "İçecek + tatlı yedeği · 4 gün (97 kutu 330 ml + 8 tatlı)", "K", "KUTU", (X_K + 33.0, X_K + W_K - 33.0), (PLAKA + 355.0, H_MAK - 2.0), (-800.0, -30.0), "kutu", "pafta v7")

# --- E · KUTU KATLAMA (TEK PARCA, kesilmez) ---
birim("E_KABIN", "KUTU katlama kabini · TEK PARÇA 0–2030 (kesilmez)", "E", "KUTU", (X_E, X_E + W_E), (0.0, H_MAK), (-DZ, 0.0), "kabin", "pafta v7")
birim("E_SARJOR", "Kutu şarjörü · alttan kaldırmalı · blank 400 × 760 yatay yığın", "E", "KUTU", (X_E + 150.0, X_E + 550.0), (123.0, E_A0 - 10.0), (-786.0, -25.0), "kutu", "pafta v7")
birim("E_AGZ", "Kutulama ağzı · kutu 320 × 320 × 45", "E", "KUTU", (X_E + 30.0, X_E + W_E - 30.0), (E_A0, E_A1), (-500.0, 0.0), "kutu", "pafta v7 · kot v35")
birim("E_TEPSI", "Kutu tepsisi Ø340 · yüzü 1104 (kutu ağzı plakanın ~15 mm altı)", "E", "KUTU", (X_E + W_E / 2.0 - 170.0, X_E + W_E / 2.0 + 170.0), (TEPSI_Y - 12.0, TEPSI_Y), (ZT - 170.0, ZT + 170.0), "sac", "pafta v7 · kot v35")
birim("E_KALIP", "Kalıp + plunger · vantuz · strok 250", "E", "KUTU", (X_E + 60.0, X_E + 400.0), (E_A1 + 30.0, E_A1 + 330.0), (-760.0, -20.0), "kutu", "pafta v7")
birim("E_VAKUM", "Vakum pompası", "E", "KUTU", (X_E + 420.0, X_E + 640.0), (E_A1 + 30.0, E_A1 + 170.0), (-400.0, -20.0), "kutu", "pafta v7")
birim("E_KART", "E kontrol kartı · tahrik", "E", "KUTU", (X_E + 420.0, X_E + 640.0), (E_A1 + 185.0, E_A1 + 330.0), (-200.0, -20.0), "kutu", "pafta v7")

# --- ROBOT (tek FR5, yer rayinda) + QR DOLABI (hattin onunde, z > 0) ---
birim("ROBOT_RAY", "Yer rayı · tek araba · x 200–5100", "-", "KATALOG", (200.0, 5100.0), (0.0, 60.0), (RZ - 120.0, RZ + 120.0), "katalog", "pafta v7")
birim("ROBOT_1", "Fairino FR5 · tek robot (pafta konumu x %.0f)" % RX, "-", "KATALOG", (RX - 90.0, RX + 90.0), (60.0, KAIDE), (RZ - 90.0, RZ + 90.0), "robot", "katalog · kaide + araba")
birim("ROBOT_1_KOL", "FR5 omuz + kol zarfı (erişim %.0f)" % ERISIM, "-", "KATALOG", (RX - 120.0, RX + 120.0), (KAIDE, OMUZ + 180.0), (RZ - 120.0, RZ + 120.0), "robot", "yalnız ZARF · gerçek kol modeli yok")
birim("QR_DOLABI", "QR teslim dolabı · 2 × 6 göz · koridorun karşısında", "-", "KUTU", QRX, (0.0, 2000.0), QRZ, "kutu", "pafta v7 · ayrıntı SERVİS_TESLİM")

'''
s = s[:a] + YENI_BIRIM + s[b:]

# ------------------------------------------------------------------ 3) denetimler (ciktilardan once)
imza = "    # ---- çıktılar ----"
DENETIM = r'''    # ---- v35 · SUREC KOTU + TABAN HIZASI + CAKISMA ----
    _pp = {p["ad"]: p for p in TC.PARCALAR}
    _cd = _pp["calisma_diski"]["wp"].val().BoundingBox(); _bt = _pp["bant"]["wp"].val().BoundingBox()
    print("SUREC KOTU (CAD'den olculdu): disk ustu %.1f · firin bandi %.1f · kesme plakasi %.1f · kutu tepsisi %.1f · tabla ekseni z %.0f"
          % (H_B + _cd.ymax, H_B + _bt.ymax, PLAKA, TEPSI_Y, ZT))
    assert abs(H_B + _cd.ymax - P) < 0.05, "disk ustu %.2f, beklenen %.2f" % (H_B + _cd.ymax, P)
    assert abs(H_B + _bt.ymax - BANT_UST) < 0.05, "bant ustu %.2f, beklenen %.2f" % (H_B + _bt.ymax, BANT_UST)
    assert P > BANT_UST > PLAKA > TEPSI_Y, "urun yukari basamaga carpar"
    _bk = {b["kod"]: b for b in B}
    for k_ in ("A_KABIN", "TOPPING_MODUL", "D_FIRIN_GOVDE", "K_KABIN"):
        assert abs(_bk[k_]["y"][0] - H_B) < 0.01, "%s tabani %.1f" % (k_, _bk[k_]["y"][0])
    for k_ in ("B_KABIN", "D_TABAN_KABIN", "K_TABAN_KABIN"):
        assert abs(_bk[k_]["y"][1] - H_B) < 0.01, "%s ustu %.1f" % (k_, _bk[k_]["y"][1])
    assert tuple(_bk["E_KABIN"]["y"]) == (0.0, H_MAK), "E kesilmemeli"
    assert not [b for b in B if "KUTU YEDE" in b["ad"].upper() or "KUTU_YEDEK" in b["kod"]], "yedek karton kutu hala var"
    print("TABAN HIZASI: A · C · F · K istasyon tabani %.0f · taban dolaplari 0-%.0f · E tek parca 0-%.0f -> GECTI" % (H_B, H_B, H_MAK))
    _ZON = ("D_FIRIN_GOVDE", "E_AGZ")                      # zarf/bolge birimleri: icindekilerle kesismesi dogal
    def _kes(a_, b_):
        return all(a_[i][0] < b_[i][1] - 0.5 and b_[i][0] < a_[i][1] - 0.5 for i in range(3))
    _yeni = [b for b in B if b["modul"] in ("D", "K", "E") and not b["kod"].endswith("_KABIN")]
    _cak = []
    for p in TC.PARCALAR:
        if p["ad"].startswith("_bom") or p["ad"] in KAPAK:
            continue
        bb = p["wp"].val().BoundingBox()
        z_ = ((bb.xmin + X_BC, bb.xmax + X_BC), (bb.ymin + H_B, bb.ymax + H_B), (bb.zmin, bb.zmax))
        if z_[0][1] <= X_D:
            continue
        for b in _yeni:
            if _kes(z_, (b["x"], b["y"], b["z"])):
                _cak.append(("TOPPING:" + p["ad"], b["kod"]))
    for i, a_ in enumerate(_yeni):
        for c in _yeni[i + 1:]:
            if a_["kod"] in _ZON or c["kod"] in _ZON:
                continue
            if _kes((a_["x"], a_["y"], a_["z"]), (c["x"], c["y"], c["z"])):
                _cak.append((a_["kod"], c["kod"]))
    print("CAKISMA RAPORU (TOPPING <-> F/K/E ve F/K/E kendi arasinda): %s" % ("YOK" if not _cak else "%d cift" % len(_cak)))
    for a_, c in _cak[:60]:
        print("    %s  <->  %s" % (a_, c))

'''
assert s.count(imza) == 1
s = s.replace(imza, DENETIM + imza, 1)

# ------------------------------------------------------------------ 4) modul dosyalari: K eklendi
e = 'for mk in ("A", "B", "C", "D", "E", "-"):'
assert s.count(e) == 1
s = s.replace(e, 'for mk in ("A", "B", "C", "D", "K", "E", "-"):', 1)

# ------------------------------------------------------------------ 5) durum.json pafta adi
e = 'pafta="HAT_2KOL_v19"'
assert s.count(e) == 1
s = s.replace(e, 'pafta="HAT_ATOSA_TABLALI_v7 · v35 taban hizasi · surec 1168"', 1)

# ------------------------------------------------------------------ 6) cikti adlari
s = s.replace("hat_v34", "hat_v35").replace("HAT_v34", "HAT_v35")

# ------------------------------------------------------------------ 7) artik tanimsiz v19 adlari kalmasin (AST: yalniz gercek ad kullanimi)
import ast
_agac = ast.parse(s)
_tanimli = {t.id for n in ast.walk(_agac) if isinstance(n, (ast.Assign, ast.For)) for t in ast.walk(n.targets[0] if isinstance(n, ast.Assign) else n.target) if isinstance(t, ast.Name)}
_eski = {"YUVA", "PZP", "FIR", "TEK", "YAG", "KES", "E_MEK", "E_AGZ", "E_SAR", "R1X", "R2X", "T_AGZ", "T_BAS", "T_SOG"}
kalan = sorted({n.id for n in ast.walk(_agac) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load) and n.id in _eski and n.id not in _tanimli})
assert not kalan, "tanimsiz eski v19 adi kullaniliyor: %s" % kalan

io.open(os.path.join(U, "hat_montaj_v35.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v35.py yazildi")
