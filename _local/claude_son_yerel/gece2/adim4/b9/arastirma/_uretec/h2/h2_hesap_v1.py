# -*- coding: utf-8 -*-
"""HAT VERSİYON 2 · HESAP v1 (30 Eyl 2026 · Claude · YEREL) — v2 yerleşiminin TEK SAYI KAYNAĞI (bütün h2_* üreteçleri buradan okur).
Kemal 30 Eyl: "bu birinci versiyon olsun … daha az geniş ve biraz daha yüksek … versiyon iki · topping istasyonunu iki raflı yaptık ki azalsın genişlik ·
ne kadar genişliği az o kadar iyi · yukarıda boş alanlar olduğu için içecek yedekleri gibi şeyleri yukarı taşıyabilirsin · çekmeceleri iki günlük hamur
ihtiyacımıza göre, içecek ve tatlıyı da · saçma sapan mantık hataları yapma".
Taslak: Codex "Alt dolap + üç üst yerleşim · Üst kat revize" (hacim taslağı: dolap 3500 · hat 4790 · üst 2240 · K 460).

YÖNTEM: SAĞ TARAF SABİT (fırın F 2500–4000, kesme K 4000–4400, kutu E 4400–5230, QR + tezgâh, robot ev konumu v1 ile AYNI dünya x'inde).
SOL TARAF 507,5 SAĞA: A açıcı, TOPPING'in sol ucu, çekmeceli dolabın K1–K3'ü, kaideler, robot rayının sol ucu.
507,5 = dolaptaki K4 kolonu (Secop + pano + kaşar/sucuk deposu, 1992,5–2500 bölmesiyle) — K4'ün işi başka yere taşındı:
  Secop NLE8.8CN + B panosu → E'nin altı (içecek yedeği yukarı çıkınca boşalan 803,5 × 462 × 379)
  kaşar + sucuk 2 günlük soğuk yedeği → TOPPING üst katı (GN kaplar)
  içecek yedeği 6 koli → makinenin üstündeki yeni üst depo (K + E üstü, 1862–2200)
Kurallar: kural kitabı (25 Eyl) + stok kurgusu (soğukta TAM 2 gün, 4 güne kadar fazlası dışarıda) + store_cad_v14 tepsileri."""
import math

# ---------------------------------------------------------------- SATIŞ (kural kitabı 2.1 · 2.3)
GUN = dict(pide=80, lahmacun=200, icecek=69.25, tatli=5.5)                  # adet / gün (içecek 277/4, tatlı 22/4)
KUTU_GUN = 80 + 200 / 2                                                     # 2.2: pide 1 · lahmacun 2'si 1 kutuda → 180 kutu / gün

# ---------------------------------------------------------------- SOĞUK DOLAP (B) · TAM 2 GÜN, robotun erişiminde (5.2)
TEPSI = dict(lahmacun=42, pide=25, icecek=48, tatli=12)                     # store_cad_v14 silikon tepsiler (6×7 · 5×5 · 6×8 · 4×3)
IKI_GUN = dict(lahmacun=400, pide=160, icecek=139, tatli=11)               # içecek 69,25 × 2 = 138,5 → 139 · tatlı 5,5 × 2 = 11
CEKMECE = {k: math.ceil(IKI_GUN[k] / TEPSI[k]) for k in TEPSI}             # EN AZ sayı: 10 · 7 · 3 · 1 = 21
assert CEKMECE == dict(lahmacun=10, pide=7, icecek=3, tatli=1), CEKMECE
STOK = {k: CEKMECE[k] * TEPSI[k] for k in TEPSI}                           # 420 · 175 · 144 · 12
# v1 dolabı (store_cad_v14) ZATEN bu 21 çekmeceyi taşıyor: K1 lahm ×5 · K2 lahm ×5 · K3 pide ×5 · K5 pide ×2 + tatlı ×1 · K6 içecek ×3.
# v2'de çekmece sayısı DEĞİŞMEZ (kural = 21) — yalnız K4 (Secop + pano + depo) çıkar.

# ---------------------------------------------------------------- GENİŞLİK ZİNCİRİ (dünya x)
DXL = 507.5                                     # sol grubun sağa kayması = K4 kolonu + K3|K4 bölmesi (1992,5 → 2500)
X0 = DXL                                        # makinenin sol ucu (v1: 0)
A_X = (X0, X0 + 700.0)                          # A açıcı 507,5–1207,5 (genişlik 700 aynı)
C_X = (A_X[1], 2500.0)                          # TOPPING 1207,5–2500 = 1292,5 (v1 1800)
F_X = (2500.0, 4000.0)                          # fırın TP10 (v1 ile aynı)
K_X = (4000.0, 4400.0)                          # kesme + sprey (v1 ile aynı)
E_X = (4400.0, 5230.0)                          # kutu katlama (v1 ile aynı)
HAT_BOY = E_X[1] - X0                           # 4722,5 (v1 5230 → −507,5 · Codex taslağı 4790)
B_X = (X0, 4000.0)                              # çekmeceli dolap 507,5–4000 (v1 0–4000)
W_B = B_X[1] - B_X[0]                           # 3492,5
B_DILIM = (1992.5, 2500.0)                      # dolaptan çıkan dilim (v1 dünya x): K3|K4 bölmesi + K4 kolonu · K4|F bölmesi (2500–2535) KALIR
C_DILIM = (1106.5, 1614.0)                      # TOPPING'den ve C kaidesinden çıkan dilim (v1 dünya x) · soğutma grubu cebi (1628…) bölünmez
assert abs((B_DILIM[1] - B_DILIM[0]) - DXL) < 1e-9 and abs((C_DILIM[1] - C_DILIM[0]) - DXL) < 1e-9
ROBOT_RAY_X = (200.0 + DXL, 5100.0)             # yer rayı sol ucu da kayar (707,5–5100)
X_ROB_AC = 700.0 + DXL                          # robot topu açıcıya bırakırken (v1 700: açıcı 350'ye erişim ≤ 915 · aynı geometri)

# ---------------------------------------------------------------- KOTLAR (dünya y)
Y_PLINT, Y_DUZ, Y_MEK, Y_TABLA = 123.0, 788.0, 892.0, 1000.0               # v1 ile aynı (dolap altı · düz çizgi · mekanizma tabanı · tabla / disk)
H_IST = 1862.0                                  # A · F · K · E gövdelerinin üstü (v1 makine üstü)
H_UST = 2200.0                                  # v2 makine üstü = iki katlı TOPPING'in üstü = üst deponun üstü (Codex taslağı 2240)
UST_DEPO_Y = (H_IST, H_UST)                     # üst depo 338 mm (A, F, K, E üstünde; TOPPING bu kotta zaten kendi gövdesi)

# ---------------------------------------------------------------- TOPPING v2 (h2_topping_v1 okur)
T_RAF_UST = (1572.0, 1575.0)                    # üst kat rafı (304 3) · alt kat içi 1152 … 1572 = 420 · üst kat 1575 … 2140
T_IC_TAVAN = H_UST - 1.5 - 58.5                 # 2140 (v1: 1802 = 1860,5 − 58,5)

# ---------------------------------------------------------------- KUTU · İÇECEK · KAŞAR/SUCUK YEDEKLERİ (4 güne kadar dışarıda)
KUTU_4GUN = 4 * KUTU_GUN                        # 720
KUTU_SARJOR, KUTU_YEDEK = 432, 320              # E şarjörü (v66 envanteri) + fırın üstü yığın (v1 ile aynı) → 752 = 4,2 gün
assert KUTU_SARJOR + KUTU_YEDEK >= KUTU_4GUN
ICECEK_4GUN = math.ceil(4 * GUN["icecek"])      # 277
KOLI = dict(adet=24, x=400.0, z=267.0, y=123.0)  # v1 E_ICECEK_YEDEK kolisi (400 × 267 × 123 · 24 kutu)
ICECEK_YEDEK_KOLI = math.ceil((ICECEK_4GUN - STOK["icecek"]) / KOLI["adet"])   # (277 − 144) / 24 = 5,5 → 6 koli = 144
assert ICECEK_YEDEK_KOLI == 6
KASAR_2GUN_L, SUCUK_2GUN_L = 22.5, 6.6          # 5.4: 2 gün kasette + 2 gün soğuk yedek (v1: dolap K4 deposu → v2: TOPPING üst katı, GN kaplar)
GN_KASAR = dict(ad="GN 1/1-200", x=530.0, z=325.0, y=200.0, L=28.0)         # EN 631-1 · brüt ~28 L → 22,5 L sığar
GN_SUCUK = dict(ad="GN 1/2-150", x=325.0, z=265.0, y=150.0, L=9.5)          # EN 631-1 · brüt ~9,5 L → 6,6 L sığar
assert GN_KASAR["L"] >= KASAR_2GUN_L and GN_SUCUK["L"] >= SUCUK_2GUN_L

if __name__ == "__main__":
    print("çekmece", CEKMECE, "stok", STOK)
    print("A", A_X, "C", C_X, "F", F_X, "K", K_X, "E", E_X, "B", B_X, "· hat", HAT_BOY, "· üst", H_UST)
    print("kutu 4 gün", KUTU_4GUN, "=", KUTU_SARJOR, "+", KUTU_YEDEK, "· içecek yedeği", ICECEK_YEDEK_KOLI, "koli")
