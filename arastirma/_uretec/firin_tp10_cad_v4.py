# -*- coding: utf-8 -*-
"""AUTOKITCH · F FIRIN · Sveba Dahlen TP10 KESİTİ, GÖVDESİ F MODÜLÜNE (1500) UZATILMIŞ · 3B MODEL + HATTA UYARLAMA v3 (26 Eyl 2026 gece)
v3 (ANA MAKİNE v48, Kemal "v2 kabul"): TOPPING v24 teknesi 2500'de bittiği için giriş ön odasındaki TOPPING CEBİ KALKTI (kabuk ve
  giriş duvarı düz). Fırın üstüne HAVALANDIRMALI RAF (3 mm, 40 mm takozlu + 0,8 mm ışınım kalkanı — v4): üstünde pizza kutusu yedeği (55 kutu) + TOPPING kompresörü
  (davlumbaz bölmesinin ön yarısı; egzoz fanı + filtreler arka yarıda). v2 (ayrı sürüm) aynen duruyor.
v2:
Kemal (26 Eyl, akşam): "bizim yaptığımızda ölçüler kafadan atmaydı. şimdi gerçek: sadece önünü arkasını istediğimiz ölçüye uzat,
bant boş olmasın önünde arkada, ona göre yeniden düzenle, son bir kontrol yap".
v1 → v2 (ne değişti):
  · Gövde 960 → 1500 (x 2500–4000 = F modülü). Uç kutuları YOK; bant tahriki + gergi arkadaki teknik bölmede.
  · Bant hiçbir yerde gövde dışına çıkmaz: uç ruloları uç duvarlarının (60) İÇİNDE, bant uçtan uca 2568–3996.
  · Isıtılan oda 2624–3940 = 1316 (TP10'da 892): aynı anda 4 ürün (adım 310 → 4 × 310 = 1240, pay 76).
  · Giriş ön odası (2500–2564, ısıtılmaz): giriş bandı burada + TOPPING X tahrikinin cebi (X tahriki F'ye 80 mm taşıyor —
    v47'de de öyleydi, D_FIRIN_GOVDE "zon" muafiyeti gizliyordu). Giriş bandı TOPPING'e değil F'ye bağlı (köprü braketleri).
  · Ürün TP10 kesitinde −249'da gitmek ZORUNDA (bant ön yüzden 92,5 içeride; −170'te ön kenar tünel duvarına girer).
    v1'de bu kaymayı boş bant üstündeki 2 çit yapıyordu. v2'de boş bant yok → kayma fırının DIŞINDA:
      girişte TOPPING'de, diskte 79 mm arkaya (tabladan itme zaten AÇIK konu — itici bunu da yapar) ·
      çıkışta K bandının üstünde 20° giriş çiti (K'nin kendi çitiyle aynı yapı) → K kesme merkezine −170'te gelir.
  · TOPPING çıkış yarığı çerçevesi genişler (−417…−13) ve alt çıtası diskin altına iner (v47'deki tabla ↔ çerçeve çakışması da kalkar).
  · Çıkış: ölü plaka 3997–4018 (fırın bandı 3996 → K bandı 4020). K'nin parçaları DEĞİŞMEZ (v1'deki 3 K uyarlaması kalktı).
KAYNAK (kesit, föy): Sveba Dahlen 990004-002 (Oca 2024) — derinlik 730 · gövde yüksekliği 517 · bant 381 · ağız 85 · IR üst/alt ayrı · 400 °C.
  Boy uzatma ÖZEL SİPARİŞ (Sveba ya da yerli IR konveyör üreticisi): güç ve ağırlık föyden ölçekli VARSAYIM (14 kW · ≈200 kg).
KOORDİNAT: DÜNYA (hat). x hat boyu · y yerden · z 0 = ön yüz, −830 = arka. Fırın gövdesi z 0…−730, arkasında F arka sacı −830.
"""
import math, os, sys
import cadquery as cq

U = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, U)
KOK = os.path.dirname(os.path.dirname(U))
from kaset_3d_v3 import Mesh, MM, MALZEME

# ================================================================ ÖLÇÜLER ================================================================
# ---- föy (TP10 kesiti, DEĞİŞMEZ) ----
D_TP, H_GOV = 730.0, 517.0                       # derinlik · gövde yüksekliği (599 − 82 ayak)
BANT_W, IC_H = 381.0, 85.0                       # bant genişliği · ağız yüksekliği
ODA_TP10 = 0.34 / (BANT_W / 1000.0) * 1000.0     # 892,4 · TP10'un ısıtılan boyu (karşılaştırma için)
GUC_TP10, T_MAX = 9.5, 400
BANT_Y = 210.0                                   # bant üstü gövde altından (≈ föy çizimi)
TUNEL_Z = (-485.0, -79.0)                        # tünel genişliği 406 · ön duvar 79 · arka teknik bölme 245
BANT_Z = (-473.5, -92.5)                         # bant 381, eksen −283
EKRAN = (189.0, 151.0, 240.0)                    # dokunmatik ekran genişlik · yükseklik · alt kotu (gövde altından)
TEPE_BANDI, FAN_R = 59.0, 66.5
# ---- hat yerleşimi (DÜNYA) ----
X_F0, X_F1 = 2500.0, 4000.0                      # F modülü = gövde (uç kutusu yok)
L_GOV = X_F1 - X_F0                              # 1500
XC_TP = (X_F0 + X_F1) / 2.0                      # 3250
BANT_UST_HAT = 1166.0                            # kot zinciri: disk 1168 → fırın bandı 1166 → K 1164
YG0 = BANT_UST_HAT - BANT_Y                      # 956 gövde altı (F taban dolabının üstü)
YG1 = YG0 + H_GOV                                # 1473 gövde üstü
ON_ODA, DUVAR = 64.0, 60.0                       # giriş ön odası (ısıtılmaz) · uç duvarı (yalıtım + rulo içinde)
X_DUV0 = X_F0 + ON_ODA                           # 2564 giriş duvarı dış yüzü
X_TUN0, X_TUN1 = X_DUV0 + DUVAR, X_F1 - DUVAR    # 2624 · 3940 ısıtılan oda
ODA = X_TUN1 - X_TUN0                            # 1316
ODA_X = (X_TUN0, X_TUN1)
TUN_Y = (YG0 + 33.0, YG0 + 307.0)                # 989 · 1263 tünel boşluğu (alt bölme + ağız + üst ısıtıcı yuvası)
AGIZ_Y = (BANT_UST_HAT, BANT_UST_HAT + IC_H)     # 1166 · 1251 ağız
# ---- konveyör (VARSAYIM: rulo çapı, ray) ----
RULO_R, BANT_K = 20.0, 6.0                       # Ø40 rulo · tel örgü 6
SARIM_R = RULO_R + BANT_K                        # 26
RULO_Y = BANT_UST_HAT - BANT_K - RULO_R          # 1140
RULO_X = (X_DUV0 + DUVAR / 2.0, X_F1 - DUVAR / 2.0)   # 2594 · 3970 (uç duvarlarının ortasında)
BANT_X = (RULO_X[0] - SARIM_R, RULO_X[1] + SARIM_R)   # 2568 · 3996 uçtan uca 1428
ALT_KOL_Y = (RULO_Y - RULO_R - BANT_K, RULO_Y - RULO_R)   # 1114 · 1120
GECIT_Y = (ALT_KOL_Y[0] - 6.0, AGIZ_Y[1])        # 1108 · 1251 uç duvarı geçidi (alt kol + rulo + ağız)
RAY_Y = (GECIT_Y[0] + 2.0, BANT_UST_HAT - 8.0)   # 1110 · 1158
RAY_X = (RULO_X[0] - 6.0, RULO_X[1] + 6.0)
ADIM = 310.0                                     # ürün adımı (Ø300 + 10) [hat kuralı]
N_URUN = int(ODA // ADIM)                        # 4
GUC = GUC_TP10 * ODA / ODA_TP10                  # 14,0 kW VARSAYIM (ısıtıcı yoğunluğu TP10 ile aynı)
# ---- ürün ----
ZT = -170.0                                      # hat ürün ekseni (tabla · K)
Z_URUN_FIRIN = -249.0                            # fırında ürün merkezi (Ø300 ön kenarı −99: tünel ön duvarına 20)
PZ_R = 150.0
# ---- giriş ön odası: giriş bandı + TOPPING X tahriki cebi ----
X_DISK_KENAR = 2507.0                            # TOPPING tabla aktarma konumunda disk kenarı (700 + 1637 + 170)
GB_RY = BANT_UST_HAT - 1.5 - 10.0                # 1154,5 giriş bandı rulo ekseni
GB_XB = X_DISK_KENAR + 2.0 + 1.5 + 10.0          # 2520,5 burun (disk kenarına 2)
GB_XT = BANT_X[0] - 2.5 - 1.5 - 10.0             # 2554 tahrik (fırın bandı ucuna 2,5)
GB_Z = (Z_URUN_FIRIN - 160.0, Z_URUN_FIRIN + 160.0)   # −409 … −89 · bant 320, ekseni ürün ekseninde
GB_MOTOR = (2530.0, 1290.0, -431.0)              # NEMA23 (mil yüzü z) · ağzın üstünde, ön odanın içinde
# TOPPING'in F'ye taşan parçaları (ölçüldü 26 Eyl, dünya): mekanizma teknesi x ≤ 2585 · y 1061,5–1091,5 · z −415…−5 · ray/kayış kirişleri
# x ≤ 2585 · y ≤ 1080,5 · X motoru x ≤ 2563 · y ≤ 1121 · z −462…−397,5 · kaidesi x ≤ 2580 · y ≤ 1135 (pahlı köşe 1112, x > 2560) ·
# z −397,5…−389,5 · uç tamponu x ≤ 2570 · y 1103,5–1123,5 · z −80…−65. (v47'de de taşıyordu; D_FIRIN_GOVDE "zon" muafiyeti gizliyordu.)
# v3: CEP YOK — TOPPING v24 teknesi 2500'de bitiyor (motor sol uca, avara sağa, kelepçeler solda).
UST_RAF_Y = (YG1 + 40.0, YG1 + 43.0)                            # 1513–1516 · fırın üstünde HAVALANDIRMALI raf (40 mm takoz + 3 mm plaka) · v4
ISI_KALKANI_Y = (YG1 + 10.0, YG1 + 10.8)                        # 1483–1483,8 · 0,8 mm 304 ışınım kalkanı (fırın üstünden 10 mm)
# TOPPING çıkış yarığı çerçevesi v2 (dünya): dış · açıklık — tabla 1157–1160 + disk 1160–1168 aktarmada x 2507'ye kadar geldiği için alt çıta 1155'in altında
YARIK_V2 = ((2492.0, 2498.5, 1145.0, 1210.0, -417.0, -13.0), (2491.0, 2499.5, 1155.0, 1206.0, -409.0, -21.0))
# ---- çıkış: ölü plaka + K giriş çiti ----
K_BANT_BAS = 4020.0                              # K kuyruk rulosu sarımının sol ucu (X_KUYRUK 37 − 17)
OLU_X = (BANT_X[1] + 1.0, K_BANT_BAS - 2.0)      # 3997 · 4018
TAN20 = math.tan(math.radians(20.0))
CC_A = (K_BANT_BAS + 6.0, Z_URUN_FIRIN - PZ_R - 5.0)                       # (4026, −404) çit K bandında başlar
CC_B = (CC_A[0] + (ZT - PZ_R - CC_A[1]) / TAN20, ZT - PZ_R)                # (4256,8, −320) → ürün −170'te
K_BANT, K_BANT_Z = 1164.0, (-412.0, -12.0)       # kesme_cad_v1: K bandı üstü · genişlik 400
CIT_Y = (K_BANT + 1.0, K_BANT + 26.0)

# ================================================================ YARDIMCILAR ================================================================
PARCALAR = []


def kut(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), centered=False).translate((min(x0, x1), min(y0, y1), min(z0, z1)))


def silz(x, y, r, z0, z1):
    return cq.Workplane("XY", origin=(x, y, min(z0, z1))).circle(r).extrude(abs(z1 - z0))


def silx(y, z, r, x0, x1):
    return cq.Workplane("YZ", origin=(min(x0, x1), y, z)).circle(r).extrude(abs(x1 - x0))


def sily(x, z, r, y0, y1):
    return cq.Workplane("XZ", origin=(x, max(y0, y1), z)).circle(r).extrude(abs(y1 - y0))


def prizma_xz(pts, y0, y1):
    return cq.Workplane("XZ", origin=(0.0, y1, 0.0)).polyline(pts).close().extrude(y1 - y0)


def ekle(ad, wp, mal, birim, grup="SABIT", kaynak="VARSAYIM", bom=None, yerel=False):
    PARCALAR.append(dict(ad=ad, wp=wp, mal=mal, birim=birim, grup=grup, kaynak=kaynak, bom=bom, yerel=yerel))


for _k, _v in (("paslanmaz", dict(renk=(0.80, 0.82, 0.84, 1.0), met=0.9, ruf=0.30)),
               ("yalitim", dict(renk=(0.86, 0.80, 0.58, 1.0), met=0.0, ruf=0.95)),
               ("ir", dict(renk=(0.95, 0.32, 0.10, 1.0), met=0.1, ruf=0.40)),
               ("ekran", dict(renk=(0.03, 0.05, 0.08, 1.0), met=0.2, ruf=0.08)),
               ("tel_bant", dict(renk=(0.50, 0.52, 0.55, 1.0), met=0.9, ruf=0.45)),
               ("grafit", dict(renk=(0.20, 0.21, 0.23, 1.0), met=0.3, ruf=0.5)),
               ("ptfe_bant", dict(renk=(0.45, 0.35, 0.22, 1.0), met=0.0, ruf=0.6)),
               ("aluminyum", dict(renk=(0.75, 0.77, 0.80, 1.0), met=0.8, ruf=0.35)),
               ("motor", dict(renk=(0.18, 0.19, 0.22, 1.0), met=0.5, ruf=0.45)),
               ("sac", dict(renk=(0.74, 0.77, 0.80, 1.0), met=0.85, ruf=0.32))):
    MALZEME.setdefault(_k, _v)


# ================================================================ 1 · FIRIN (TP10 kesiti · 1500 gövde) ================================================================
def firin(ayak=False, plaka=False):
    """Gövde + konveyör, DÜNYA koordinatında. ayak/plaka: v1 uyumluluğu için (uzatılmış gövdede ikisi de yok)."""
    G, K = "F_TP10_GOVDE", "F_TP10_KONVEYOR"
    x0, x1, y0, y1 = X_F0, X_F1, YG0, YG1
    # --- dış kabuk 1,5: uç yüzlerinde yalnız ürün ağızları + X tahriki cebi ---
    kab = kut(x0, x1, y0, y1, -D_TP, 0.0).cut(kut(x0 + 1.5, x1 - 1.5, y0 + 1.5, y1 - 1.5, -D_TP + 1.5, -1.5))
    kab = kab.cut(kut(x0 - 1.0, x0 + 2.0, 1152.0, 1210.0, -420.0, -10.0))                    # giriş ağzı (TOPPING çıkış yarığına bakar; tabla + disk 2507'ye kadar girer)
    kab = kab.cut(kut(x1 - 2.0, x1 + 1.0, GECIT_Y[0] + 4.0, GECIT_Y[1] + 2.0, TUNEL_Z[0] - 2.0, TUNEL_Z[1] + 2.0))   # çıkış ağzı (K'ye)
    ekle("govde_kabugu", kab, "paslanmaz", G, kaynak="föy kesiti 730 × 517 · boy 1500 ÖZEL",
         bom=("Fırın gövde kabuğu · paslanmaz 1,5", 1, "TP10 kesiti · boy 1500 (özel sipariş)", "uç kutusu yok · giriş ön odası + 2 uç duvarı"))
    # --- ısıtılan oda kaplaması 1 mm (uçları geçit boyunca açık) ---
    kap = kut(X_TUN0 - 1.0, X_TUN1 + 1.0, TUN_Y[0] - 1.0, TUN_Y[1] + 1.0, TUNEL_Z[0] - 1.0, TUNEL_Z[1] + 1.0) \
        .cut(kut(X_TUN0, X_TUN1, TUN_Y[0], TUN_Y[1], TUNEL_Z[0], TUNEL_Z[1])) \
        .cut(kut(X_TUN0 - 4.0, X_TUN1 + 4.0, GECIT_Y[0], GECIT_Y[1], TUNEL_Z[0], TUNEL_Z[1]))
    ekle("tunel_kaplamasi", kap, "paslanmaz", G, kaynak="VARSAYIM (iç)")
    # --- yalıtım (taşyünü): ön odadan sonra, oda + iki uç duvarı; geçitler, rulo milleri, ön yataklar, X tahriki cebi ---
    yal = kut(X_DUV0, x1 - 1.5, y0 + 1.5, y1 - 1.5, TUNEL_Z[0] - 3.5, -1.5) \
        .cut(kut(X_TUN0 - 1.0, X_TUN1 + 1.0, TUN_Y[0] - 1.0, TUN_Y[1] + 1.0, TUNEL_Z[0] - 1.0, TUNEL_Z[1] + 1.0)) \
        .cut(kut(X_DUV0 - 1.0, X_TUN0 + 1.0, GECIT_Y[0], GECIT_Y[1], TUNEL_Z[0], TUNEL_Z[1])) \
        .cut(kut(X_TUN1 - 1.0, x1 + 1.0, GECIT_Y[0], GECIT_Y[1], TUNEL_Z[0], TUNEL_Z[1]))
    for rx in RULO_X:
        yal = yal.cut(silz(rx, RULO_Y, 10.5, -600.0, -40.0)).cut(kut(rx - 20.0, rx + 20.0, RULO_Y - 18.0, RULO_Y + 18.0, TUNEL_Z[1], -45.0))
    ekle("yalitim_tasyunu", yal, "yalitim", G, kaynak="VARSAYIM (iç)",
         bom=("Yalıtım (taşyünü) · uç duvarları 60", 1, "üretici", "geçitler: bant üst kolu + alt kolu + rulo · ön yatak cepleri"))
    duv = kut(X_F0 + 1.5, x1 - 1.5, y0 + 1.5, y1 - 1.5, TUNEL_Z[0] - 5.5, TUNEL_Z[0] - 4.0) \
        .cut(kut(GB_MOTOR[0] - 33.0, GB_MOTOR[0] + 33.0, GB_MOTOR[1] - 33.0, GB_MOTOR[1] + 33.0, TUNEL_Z[0] - 7.0, TUNEL_Z[0] - 2.0))   # giriş bandı motoru penceresi
    for rx in RULO_X:
        duv = duv.cut(silz(rx, RULO_Y, 10.5, -600.0, -40.0))
    ekle("teknik_bolme_duvari", duv, "paslanmaz", G, kaynak="≈ uç görünüşü 237 mm",
         bom=("Teknik bölme (sürücü · kontaktör · SSR · bant motoru · gergi)", 1, "katalog kesiti", "≈ 239 derinlik, ekran tarafı"))
    # --- ısıtıcılar: üstte + altta 2'şer bölge (şematik) ---
    xm = (X_TUN0 + X_TUN1) / 2.0
    for i, (a, b) in enumerate(((X_TUN0 + 5.0, xm - 5.0), (xm + 5.0, X_TUN1 - 5.0))):
        ekle("ust_isitici_%d" % (i + 1), kut(a, b, TUN_Y[1] - 10.0, TUN_Y[1] - 1.0, BANT_Z[0], BANT_Z[1]), "ir", G, kaynak="föy: IR üst/alt ayrı · yerleşim VARSAYIM",
             bom=("Kızılötesi ısıtıcı · üst · bölge %d" % (i + 1), 1, "katalog kesiti", "400 °C · toplam ≈%.0f kW (VARSAYIM: TP10'un 9,5 kW'ı boyla ölçekli)" % GUC) if i == 0 else None)
        ekle("alt_isitici_%d" % (i + 1), kut(a, b, RULO_Y - 12.0, RULO_Y - 4.0, BANT_Z[0], BANT_Z[1]), "ir", G, kaynak="föy: IR üst/alt ayrı · yerleşim VARSAYIM",
             bom=("Kızılötesi ısıtıcı · alt · bölge %d" % (i + 1), 1, "katalog kesiti", "bandın üst ve alt kolu arasında") if i == 0 else None)
    ekle("kirinti_tepsisi", kut(X_TUN0 + 12.0, X_TUN1 - 12.0, TUN_Y[0], TUN_Y[0] + 5.0, TUNEL_Z[0] + 2.0, TUNEL_Z[1] - 2.0), "paslanmaz", G, kaynak="VARSAYIM")
    # --- arka yüz (servis tarafı): etiket bandı · ekran · şalter · servis plakası · vidalar · 2 fan · CEE priz · sinyal kutusu ---
    ekle("ust_etiket_bandi", kut(x0, x1, y1 - TEPE_BANDI, y1, -D_TP - 1.0, -D_TP), "grafit", G, kaynak="≈ uzun görünüş (SVEBA DAHLEN)")
    ew, eh, ey = EKRAN
    ekle("ekran_cercevesi", kut(XC_TP - ew / 2 - 10, XC_TP + ew / 2 + 10, YG0 + ey - 10, YG0 + ey + eh + 10, -D_TP - 8.0, -D_TP), "koyu", G, kaynak="≈ uzun görünüş",
         bom=("Dokunmatik ekran (TP Infinity kumanda)", 1, "katalog", "≈ 189 × 151 · arka yüzde (servis tarafı)"))
    ekle("ekran_cami", kut(XC_TP - ew / 2, XC_TP + ew / 2, YG0 + ey, YG0 + ey + eh, -D_TP - 9.0, -D_TP - 8.0), "ekran", G, kaynak="≈ uzun görünüş")
    ekle("ana_salter", silz(XC_TP, YG0 + 200.0, 18.0, -D_TP - 20.0, -D_TP), "koyu", G, kaynak="≈ uzun görünüş (ekranın altı)")
    ekle("servis_plakasi", kut(XC_TP + 352.0, XC_TP + 437.0, YG0 + 138.0, YG0 + 199.0, -D_TP - 2.0, -D_TP), "koyu", G, kaynak="≈ uzun görünüş")
    for i, (dx, dy) in enumerate(((-462.0, 171.0), (462.0, 171.0), (-462.0, 431.0), (462.0, 431.0))):
        ekle("panel_vidasi_%d" % i, silz(XC_TP + dx, YG0 + dy, 4.0, -D_TP - 2.0, -D_TP), "celik", G, kaynak="≈ uzun görünüş")
    for i, fx_ in enumerate((X_DUV0 + 76.0, X_F1 - 140.0)):
        ekle("fan_%d" % i, silz(fx_, YG0 + 194.0, FAN_R, -D_TP - 2.0, -D_TP), "koyu", G, kaynak="≈ uzun görünüş Ø133 (uç kutularındaki fanlar teknik bölmeye)",
             bom=("Teknik bölme fanı Ø133", 2, "katalog", "giriş: elektronik · çıkış: bant motoru") if i == 0 else None)
        ekle("fan_halkasi_%d" % i, silz(fx_, YG0 + 194.0, FAN_R, -D_TP - 3.0, -D_TP - 2.0).cut(silz(fx_, YG0 + 194.0, FAN_R - 5.0, -D_TP - 4.0, -D_TP)), "celik", G, kaynak="≈")
    ekle("cee_priz", silz(2530.0, YG0 + 200.0, 28.0, -D_TP - 30.0, -D_TP), "koyu", G, kaynak="≈ Ø57 (uç yüzü TOPPING'e dayandığı için ARKA yüze)")
    ekle("sinyal_kutusu", kut(2505.0, 2613.0, YG0 + 54.0, YG0 + 108.0, -D_TP - 5.0, -D_TP), "koyu", G, kaynak="≈ 108 × 54 (arka yüze)")
    # --- KONVEYÖR: tel örgü bant (üst kol şerit şerit) · alt kol · sarımlar · rulolar (uç duvarlarının içinde) · raylar · yataklar ---
    z0, z1 = BANT_Z
    n = int((RULO_X[1] - RULO_X[0]) // 25.0)
    for j in range(n):
        xa = RULO_X[0] + j * 25.0; xb = min(RULO_X[1], xa + 20.0)
        ekle("bant_ust_%02d" % j, kut(xa, xb, BANT_UST_HAT - BANT_K, BANT_UST_HAT, z0, z1), "tel_bant", K, kaynak="föy 381 · örgü VARSAYIM",
             bom=("Konveyör bandı · paslanmaz tel örgü", 1, "381 × 1428 uçtan uca (özel boy)", "üstü 1166 · uçları gövde içinde") if j == 0 else None)
    ekle("bant_alt_kol", kut(RULO_X[0], RULO_X[1], ALT_KOL_Y[0], ALT_KOL_Y[1], z0, z1), "tel_bant", K, kaynak="VARSAYIM")
    for s, ad, x in ((-1.0, "giris", RULO_X[0]), (1.0, "cikis", RULO_X[1])):
        sar = silz(x, RULO_Y, SARIM_R, z0, z1).cut(silz(x, RULO_Y, RULO_R, z0 - 1, z1 + 1)).cut(kut(x, x - s * 100.0, RULO_Y - 40, RULO_Y + 40, z0 - 1, z1 + 1))
        g = "RULO_TP_%s" % ad.upper()
        ekle("bant_sarimi_%s" % ad, sar, "tel_bant", K, grup=g, kaynak="VARSAYIM Ø40 rulo")
        ekle("rulo_%s" % ad, silz(x, RULO_Y, RULO_R, z0 + 1.5, z1 - 1.5).cut(silz(x, RULO_Y, 10.0, z0, z1)), "celik", K, grup=g, kaynak="VARSAYIM Ø40",
             bom=("Bant ucu rulosu Ø40 (VARSAYIM)", 2, "üretici", "giriş: gergili · çıkış: tahrikli · uç duvarının içinde") if s < 0 else None)
        zb = -520.0 if s < 0 else -586.0
        ekle("rulo_mili_%s" % ad, silz(x, RULO_Y, 10.0, zb, -47.0), "celik", K, grup=g, kaynak="VARSAYIM Ø20 · ön duvara gömülü yataktan arka teknik bölmeye")
        ekle("on_yatak_%s" % ad, kut(x - 18.0, x + 18.0, RULO_Y - 16.0, RULO_Y + 16.0, -77.0, -47.0).cut(silz(x, RULO_Y, 10.2, -78.0, -46.0)), "koyu", K,
             kaynak="VARSAYIM · ön duvar yalıtımında cep")
        ekle("arka_yatak_%s" % ad, kut(x - 18.0, x + 18.0, RULO_Y - 16.0, RULO_Y + 16.0, -520.0, -500.0).cut(silz(x, RULO_Y, 10.2, -521.0, -499.0)), "koyu", K,
             kaynak="VARSAYIM · teknik bölmede")
    _del = lambda w: w.cut(silz(RULO_X[0], RULO_Y, 10.2, -500.0, -40.0)).cut(silz(RULO_X[1], RULO_Y, 10.2, -500.0, -40.0))
    ekle("on_ray", _del(kut(RAY_X[0], RAY_X[1], RAY_Y[0], RAY_Y[1], -84.0, -81.0)), "paslanmaz", K, kaynak="VARSAYIM")
    ekle("arka_ray", _del(kut(RAY_X[0], RAY_X[1], RAY_Y[0], RAY_Y[1], -484.0, -481.0)), "paslanmaz", K, kaynak="VARSAYIM")
    # gergi (giriş rulosu, teknik bölmede): arka yatak kızakta, M8 itme vidası + konsol
    ekle("gergi_konsolu", kut(2556.0, 2560.0, RULO_Y - 20.0, RULO_Y + 20.0, -520.0, TUNEL_Z[0] - 5.5), "celik", K, kaynak="VARSAYIM",
         bom=("Bant gergisi · M8 itme vidası + kontra (arka) · ön yatak yuvası uzun delikli", 1, "üretici", "teknik bölmeden ayarlanır"))
    ekle("gergi_vidasi", silx(RULO_Y, -510.0, 4.0, 2560.0, RULO_X[0] - 18.0), "celik", K, kaynak="VARSAYIM M8")
    # tahrik (çıkış rulosu, teknik bölmede): sonsuz vidalı redüktör mil üstünde + motor x boyunca
    ekle("tahrik_reduktoru", kut(RULO_X[1] - 32.0, RULO_X[1] + 26.0, RULO_Y - 35.0, RULO_Y + 35.0, -586.0, -521.0).cut(silz(RULO_X[1], RULO_Y, 10.2, -587.0, -520.0)), "koyu", K,
         kaynak="VARSAYIM", bom=("Bant tahriki · sonsuz vidalı redüktör (arka yatağın arkasında, delik milli) + motor", 1, "üretici (TP10'da uç kutusunda)", "bant hızı 1316 mm / pişme süresi = 6 mm/s (3,5 dk) · ≈2,6 dev/dk"))
    ekle("tahrik_motoru", silx(RULO_Y, -553.0, 30.0, RULO_X[1] - 170.0, RULO_X[1] - 32.0), "motor", K, kaynak="VARSAYIM Ø60 × 138")


# ================================================================ 2 · ÜRÜN YOLU ================================================================
# Ürün fırına −249'da gelir (kayma TOPPING'de, diskte). K bandı üstündeki 20° çit (ürünün ARKASINDA) −249 → −170'e geri iter.
def _cit_noktalari(A, B, n=400):
    return [(A[0] + (B[0] - A[0]) * i / n, A[1] + (B[1] - A[1]) * i / n) for i in range(n + 1)]


_CC = _cit_noktalari(CC_A, CC_B)


def urun_z(xc):
    """ürün merkezinin z'si (xc'de, fırın bandı → K): çit Ø300 zarfı iter (K'nin 20° çitiyle aynı kural, köşe kuralı dahil)."""
    z = Z_URUN_FIRIN
    for px, pz in _CC:
        d = xc - px
        if abs(d) < PZ_R:
            z = max(z, pz + math.sqrt(PZ_R * PZ_R - d * d))
    if xc > CC_B[0]:
        z = max(z, ZT)
    return min(ZT, z)


# ================================================================ 3 · HATTA UYARLAMA (bizim parçalar) ================================================================
def adaptor(nema23=None):
    GB, CP, KC_, AS = "F_GIRIS_BANDI", "F_CIKIS_PLAKA", "F_K_GIRIS_CITI", "F_ARKA_SAC"
    Y = BANT_UST_HAT; BR, BK = 10.0, 1.5
    RY, XB, XT = GB_RY, GB_XB, GB_XT
    ZA, ZB_ = GB_Z
    # ---- 3.1 GİRİŞ BANDI (ön odada): disk kenarı 2507 → fırın bandı 2568 · PTFE 320 · eksen −249 ----
    ekle("giris_burun_rulosu", silz(XB, RY, BR, ZA + 3, ZB_ - 3).union(silz(XB, RY, 4.0, -426.0, -69.0)), "celik", GB, grup="RULO_GB_BURUN",
         bom=("Giriş bandı burun rulosu Ø20 × 314 + Ø8 mil", 1, "304 · iki uçta rulman", "disk kenarına 2 mm"))
    ekle("giris_tahrik_rulosu", silz(XT, RY, BR, ZA + 3, ZB_ - 3).union(silz(XT, RY, 4.0, -436.0, -69.0)), "celik", GB, grup="RULO_GB_TAHRIK",
         bom=("Giriş bandı tahrik rulosu Ø20 × 314 (kauçuk kaplı)", 1, "304", "arkada GT2 kasnağıyla motora bağlı"))
    ust = kut(XB, XT, Y - BK, Y, ZA, ZB_)
    alt = kut(XB, XT, RY - BR - BK, RY - BR, ZA, ZB_)
    s1 = silz(XB, RY, BR + BK, ZA, ZB_).cut(silz(XB, RY, BR, ZA - 1, ZB_ + 1)).cut(kut(XB, XB + 40, RY - 20, RY + 20, ZA - 1, ZB_ + 1))
    s2 = silz(XT, RY, BR + BK, ZA, ZB_).cut(silz(XT, RY, BR, ZA - 1, ZB_ + 1)).cut(kut(XT - 40, XT, RY - 20, RY + 20, ZA - 1, ZB_ + 1))
    ekle("giris_bandi", ust.union(alt).union(s1).union(s2), "ptfe_bant", GB,
         bom=("Giriş bandı · PTFE kaplı cam elyaf 1,5 mm · sonsuz", 1, "320 × ≈ 140", "üst yüz 1166 = fırın bandı · ekseni −249 (fırındaki ürün ekseni)"))
    ekle("giris_tasiyici_sac", kut(XB + 12.0, XT - 12.0, Y - BK - 4.0, Y - BK - 1.0, ZA + 5, ZB_ - 5), "sac", GB)
    for i, (a, b) in enumerate(((ZA - 10.0, ZA - 5.0), (ZB_ + 5.0, ZB_ + 10.0))):
        ekle("giris_yan_saci_%d" % i, kut(X_DISK_KENAR + 2.0, X_DUV0 - 2.0, RY - 18.0, RY + 5.5, a, b)
             .cut(silz(XB, RY, 4.2, a - 1, b + 1)).cut(silz(XT, RY, 4.2, a - 1, b + 1)), "sac", GB,
             bom=("Giriş bandı yan sacı 5 mm (rulman yuvalı)", 2, "304 lazer", "ön odanın ön sacına ve teknik bölme duvarına köprü braketleriyle") if i == 0 else None)
    # köprü braketleri: ön yan sac ↔ kabuğun ön sacı (z −1,5) · arka yan sac ↔ teknik bölme duvarı (z −489)
    for i, x in enumerate((2508.0, 2530.0)):
        ekle("giris_koprusu_on_%d" % i, kut(x, x + 8.0, RY - 18.0, RY + 5.5, ZB_ + 10.0, -1.5), "sac", GB,
             bom=("Giriş bandı köprü braketi 8 mm", 3, "304", "bant F'nin ön odasına bağlı (TOPPING'e değil)") if i == 0 else None)
    ekle("giris_koprusu_arka", kut(2508.0, 2516.0, RY - 18.0, RY + 5.5, TUNEL_Z[0] - 4.0, ZA - 10.0), "sac", GB)
    # motor: STP-MTR-23079 (gerçek STEP) ağzın üstünde, arka yan sacın arkasında · GT2 1:1 kasnak (Ø15)
    MX, MY, MZF = GB_MOTOR
    if nema23 is not None:
        ekle("giris_bandi_motoru", cq.Workplane(obj=nema23.translate(cq.Vector(MX, MY, MZF))), "motor", GB, kaynak="STP-MTR-23079 GERÇEK CAD",
             bom=("Giriş bandı motoru · NEMA23 STP-MTR-23079", 1, "1,95 N·m kapalı çevrim", "GERÇEK CAD · GT2 1:1 → 115 dev/dk = 0,12 m/s"))
    ekle("motor_plakasi", kut(2522.0, 2561.0, RY - 17.5, MY + 32.0, MZF, MZF + 3.0).cut(silz(MX, MY, 20.0, MZF - 1, MZF + 4)).cut(silz(XT, RY, 4.5, MZF - 1, MZF + 4)),
         "sac", GB, bom=("Motor plakası 3 mm", 1, "304 lazer", "arka yan saca takozla · teknik bölme duvarına ayakla"))
    ekle("motor_takozu", kut(2522.0, 2545.0, RY - 17.0, RY - 7.0, MZF + 3.0, ZA - 10.0), "sac", GB)
    ekle("plaka_ayagi", kut(2526.0, 2534.0, 1220.0, 1240.0, TUNEL_Z[0] - 4.0, MZF), "sac", GB)
    ekle("kasnak_rulo", silz(XT, RY, 7.5, MZF + 3.0, MZF + 11.0).cut(silz(XT, RY, 4.1, MZF + 2.0, MZF + 12.0)), "aluminyum", GB, grup="RULO_GB_TAHRIK")
    ekle("kasnak_motor", silz(MX, MY, 7.5, MZF + 3.0, MZF + 11.0), "aluminyum", GB)
    L_ = math.hypot(MX - XT, MY - RY); a_ = math.degrees(math.atan2(MY - RY, MX - XT))
    kay = cq.Workplane("XY", origin=((XT + MX) / 2.0, (RY + MY) / 2.0, MZF + 3.0)).slot2D(L_ + 17.0, 17.0, a_).extrude(8.0)
    kay = kay.cut(cq.Workplane("XY", origin=((XT + MX) / 2.0, (RY + MY) / 2.0, MZF + 2.0)).slot2D(L_ + 15.0, 15.0, a_).extrude(10.0))
    ekle("gt2_kayis", kay, "koyu", GB, bom=("GT2 kayış 6 mm", 1, "kauçuk", "1:1"))
    # ---- 3.2 ÇIKIŞ ÖLÜ PLAKASI: fırın bandı ucu 3996 → K bandı 4020 · L: dikey kanadı kabuğun çıkış sacına kaynaklı ----
    olu = kut(OLU_X[0], OLU_X[1], K_BANT - 1.0, K_BANT + 1.5, ZA, ZB_).union(kut(OLU_X[0], OLU_X[0] + 1.5, GECIT_Y[0] + 4.0, K_BANT - 1.0, ZA, ZB_))
    ekle("cikis_olu_plakasi", olu, "sac", CP, bom=("Çıkış ölü plakası 2,5 mm · L", 1, "304 · üstü parlatılmış", "üstü 1165,5: fırın bandı 1166 → K bandı 1164"))
    # ---- 3.3 K GİRİŞ ÇİTİ (K bandı üstünde, ürünün ARKASINDA): −249 → −170 · K'nin çitiyle aynı yapı (304 lama + UHMW yüz) ----
    nx_, nz_ = math.sin(math.radians(20.0)), math.cos(math.radians(20.0))
    pts = [CC_A, CC_B, (CC_B[0] + 10 * nx_, CC_B[1] - 10 * nz_), (CC_A[0] + 10 * nx_, CC_A[1] - 10 * nz_)]
    ekle("k_giris_citi", prizma_xz(pts, CIT_Y[0], CIT_Y[1]), "pom", KC_,
         bom=("K giriş çiti 20° · 304 lama 3 + UHMW yüz 7 · 25 yüksek", 1, "gıda", "ürünü 79 mm öne alır: K kesme merkezine (4300) hat ekseninde (−170) gelir · K'nin parçaları değişmez"))
    for i, x in enumerate((4090.0, 4200.0)):
        zl = CC_A[1] + (x - 8.0 - CC_A[0]) * TAN20 - 10.0 / nz_           # çitin arka yüzü braketin SOL kenarında (en geride)
        ekle("k_giris_citi_braketi_%d" % i, kut(x - 8.0, x + 8.0, 1130.0, CIT_Y[1] + 2.0, K_BANT_Z[0] - 8.0, K_BANT_Z[0] - 5.0)
             .union(kut(x - 8.0, x + 8.0, CIT_Y[1] - 8.0, CIT_Y[1] + 2.0, zl, K_BANT_Z[0] - 5.0)), "sac", KC_,
             bom=("K giriş çiti braketi 8 mm (L)", 2, "304", "K'nin arka bant yan levhasının dış yüzüne 2 × M5") if i == 0 else None)
    # ---- 3.4 FIRIN ÜSTÜ HAVALI RAF (v3): pizza kutusu yedeği (55) + TOPPING kompresörü bunun üstünde · gövde üstüne 5 mm hava boşluğu ----
    _raf = kut(X_F0 + 10.0, X_F1 - 10.0, UST_RAF_Y[0], UST_RAF_Y[1], -420.0, -15.0)
    for x, z in ((X_F0 + 30.0, -30.0), (XC_TP, -30.0), (X_F1 - 30.0, -30.0), (X_F0 + 30.0, -408.0), (XC_TP, -408.0), (X_F1 - 30.0, -408.0)):
        _raf = _raf.cut(sily(x, z, 3.3, UST_RAF_Y[0] - 1.0, UST_RAF_Y[1] + 1.0))
    ekle("ust_raf", _raf, "sac", "F_UST_RAF",
         bom=("Fırın üstü raf 3 mm", 1, "304 · 1480 × 405", "40 mm takozla gövde üstünde, yanları açık (doğal havalandırma) · altında ışınım kalkanı · kompresör 25 kg + kutular 8 kg · JUN-AIR ortam sınırı 40 °C [föy]"))
    _kal = kut(X_F0 + 10.0, X_F1 - 10.0, ISI_KALKANI_Y[0], ISI_KALKANI_Y[1], -420.0, -15.0)
    for x, z in ((X_F0 + 30.0, -30.0), (XC_TP, -30.0), (X_F1 - 30.0, -30.0), (X_F0 + 30.0, -408.0), (XC_TP, -408.0), (X_F1 - 30.0, -408.0)):
        _kal = _kal.cut(sily(x, z, 3.3, ISI_KALKANI_Y[0] - 1.0, ISI_KALKANI_Y[1] + 1.0))
    ekle("isi_kalkani", _kal, "sac", "F_UST_RAF",
         bom=("Isı kalkanı 0,8 mm", 1, "304 · 1480 × 405 · parlak", "fırın üstünden 10 mm yukarıda, takozlara geçme: fırın üst yüzeyinin ışınımını keser, rafla arasında 29 mm hava"))
    TAKOZ_XZ = ((X_F0 + 30.0, -30.0), (XC_TP, -30.0), (X_F1 - 30.0, -30.0), (X_F0 + 30.0, -408.0), (XC_TP, -408.0), (X_F1 - 30.0, -408.0))
    for i, (x, z) in enumerate(TAKOZ_XZ):                                                       # v4: iki parça boru takoz (alt 10 · üst 29,2), M6 saplama deliği
        ekle("ust_raf_takozu_alt_%d" % i, sily(x, z, 8.0, YG1, ISI_KALKANI_Y[0]).cut(sily(x, z, 3.3, YG1 - 1.0, ISI_KALKANI_Y[0] + 1.0)), "paslanmaz", "F_UST_RAF",
             bom=("Raf takozu alt Ø16 × 10", 6, "304 boru 16 × 1,5 → torna", "fırın üst sacındaki M6 saplamaya geçer · kalkanı taşır") if i == 0 else None)
        ekle("ust_raf_takozu_ust_%d" % i, sily(x, z, 8.0, ISI_KALKANI_Y[1], UST_RAF_Y[0]).cut(sily(x, z, 3.3, ISI_KALKANI_Y[1] - 1.0, UST_RAF_Y[0] + 1.0)), "paslanmaz", "F_UST_RAF",
             bom=("Raf takozu üst Ø16 × 29,2", 6, "304 boru 16 × 1,5 → torna", "kalkan ile raf arasında · rafın üstünden M6 somun") if i == 0 else None)
    # ---- 3.5 F ARKA SACI (istasyon = kapalı ürün) ----
    ekle("f_arka_saci", kut(X_F0, X_F1, YG0, YG1 + 10.0, -830.0, -828.5), "sac", AS,
         bom=("F arka sacı 1,5 mm", 1, "304", "956–1483 · hava ana hattı önünde kalır"))


BIRIMLER = [
    ("F_TP10_GOVDE", "Fırın gövdesi · TP10 kesiti (730 × 517) · boy 1500 ÖZEL SİPARİŞ · giriş ön odası 64 + uç duvarları 60 · ısıtılan 1316 · IR üst + alt 2 bölge · ekran + teknik bölme arkada · ≈14 kW (VARSAYIM)"),
    ("F_TP10_KONVEYOR", "Fırın konveyörü · tel örgü bant 381 × 1428 uçtan uca · üstü 1166 · rulolar uç duvarlarının içinde (boş bant yok) · tahrik + gergi teknik bölmede"),
    ("F_GIRIS_BANDI", "Giriş bandı (bizim) · ön odada · disk kenarı 2507 → fırın bandı 2568 · Ø20 burun + tahrik · NEMA23 + GT2 · PTFE 320 · eksen −249 · F'ye köprü braketleriyle"),
    ("F_CIKIS_PLAKA", "Çıkış ölü plakası (bizim) · 3997–4018 · fırın bandı → K bandı"),
    ("F_K_GIRIS_CITI", "K giriş çiti (bizim · K bandı üstünde) · 20° · ürünü −249'dan −170'e alır · K'nin parçaları değişmez"),
    ("F_UST_RAF", "Fırın üstü HAVALANDIRMALI raf (bizim) · 3 mm raf 40 mm takozlu, altında 0,8 mm ışınım kalkanı (10 mm) · üstünde pizza kutusu yedeği 55 + TOPPING kompresörü (ortam sınırı 40 °C)"),
    ("F_ARKA_SAC", "F arka sacı (bizim) · 1,5 mm · 956–1483"),
]


def dunya(p):
    sh = p["wp"].val() if isinstance(p["wp"], cq.Workplane) and len(p["wp"].vals()) == 1 else cq.Compound.makeCompound([o for o in p["wp"].vals() if isinstance(o, cq.Shape)])
    return sh


def kur(ayak=False, plaka=False, uyarla=True):
    PARCALAR[:] = []
    firin(ayak=ayak, plaka=plaka)
    if uyarla:
        import topping_cad_v23 as _TC
        adaptor(_TC.nema23()["govde"])
    return PARCALAR


# ================================================================ 4 · TEK BAŞINA (uzatılmış fırın, ayaksız) ================================================================
def ag(wp, tol=0.5, aci=0.6):
    import kiyma_cad_v6 as _K
    return _K.ag(wp, tol, aci)


def glb_yaz(yol, parcalar):
    import struct, json
    kul = sorted(set(m for _a, _m, m in parcalar)); blob, views, accs, meshes, nodes = [], [], [], [], []; off = [0]
    def gomu(bt, hedef=None):
        while off[0] % 4: blob.append(b"\x00"); off[0] += 1
        v = {"buffer": 0, "byteOffset": off[0], "byteLength": len(bt)}
        if hedef: v["target"] = hedef
        views.append(v); blob.append(bt); off[0] += len(bt); return len(views) - 1
    for adi, m, mal in parcalar:
        vp = gomu(struct.pack("<%df" % (3 * len(m.P)), *[c for q in m.P for c in q]), 34962)
        vn = gomu(struct.pack("<%df" % (3 * len(m.N)), *[c for q in m.N for c in q]), 34962)
        vi = gomu(struct.pack("<%dI" % len(m.I), *m.I), 34963)
        accs.append({"bufferView": vp, "componentType": 5126, "count": len(m.P), "type": "VEC3", "min": [min(q[k] for q in m.P) for k in range(3)], "max": [max(q[k] for q in m.P) for k in range(3)]})
        accs.append({"bufferView": vn, "componentType": 5126, "count": len(m.N), "type": "VEC3"})
        accs.append({"bufferView": vi, "componentType": 5125, "count": len(m.I), "type": "SCALAR"})
        meshes.append({"name": adi, "primitives": [{"attributes": {"POSITION": len(accs) - 3, "NORMAL": len(accs) - 2}, "indices": len(accs) - 1, "material": kul.index(mal)}]})
        nodes.append({"mesh": len(meshes) - 1, "name": adi})
    mats = []
    for k in kul:
        d_ = MALZEME[k]; mm = {"name": k, "pbrMetallicRoughness": {"baseColorFactor": list(d_["renk"]), "metallicFactor": d_["met"], "roughnessFactor": d_["ruf"]}, "doubleSided": True}
        if d_.get("saydam"): mm["alphaMode"] = "BLEND"
        mats.append(mm)
    while off[0] % 4: blob.append(b"\x00"); off[0] += 1
    bb = b"".join(blob)
    g = {"asset": {"version": "2.0", "generator": "AUTOKITCH firin_tp10_cad_v4"}, "scene": 0, "scenes": [{"nodes": list(range(len(nodes)))}], "nodes": nodes,
         "meshes": meshes, "materials": mats, "accessors": accs, "bufferViews": views, "buffers": [{"byteLength": len(bb)}]}
    js = json.dumps(g, separators=(",", ":")).encode("utf-8")
    while len(js) % 4: js += b" "
    with open(yol, "wb") as f:
        f.write(struct.pack("<4sII", b"glTF", 2, 12 + 8 + len(js) + 8 + len(bb))); f.write(struct.pack("<I4s", len(js), b"JSON")); f.write(js)
        f.write(struct.pack("<I4s", len(bb), b"BIN\x00")); f.write(bb)
    return len(bb) + len(js)


def kendi_arasinda(ps):
    """gerçek katı kesişimi (mm³) — kendi parçaları arasında (yalnız kutuları çakışanlar)"""
    S = [(p["birim"] + ":" + p["ad"], dunya(p)) for p in ps]
    out = []
    for i, (a, sa) in enumerate(S):
        A = sa.BoundingBox()
        for c, sc in S[i + 1:]:
            B = sc.BoundingBox()
            if A.xmin < B.xmax and B.xmin < A.xmax and A.ymin < B.ymax and B.ymin < A.ymax and A.zmin < B.zmax and B.zmin < A.zmax:
                try: v = sa.intersect(sc).Volume()
                except Exception: v = -1.0
                if v > 1.0 or v < 0: out.append((round(v, 1), a, c))
    return sorted(out, reverse=True)


if __name__ == "__main__":
    import time, json
    import kaset_3d_v3 as K3
    t0 = time.time()
    ps = kur(uyarla=True)
    gecersiz = [p["ad"] for p in ps if not dunya(p).isValid()]
    print("TP10-UZUN v2 · %d parça (fırın %d + uyarlama %d) · katı denetimi: %s" % (len(ps), len([p for p in ps if p["birim"].startswith("F_TP10")]),
          len([p for p in ps if not p["birim"].startswith("F_TP10")]), "hepsi geçerli" if not gecersiz else "GEÇERSİZ %s" % gecersiz)); assert not gecersiz
    cak = kendi_arasinda(ps)
    print("KENDİ ARASINDA (gerçek katı kesişimi > 1 mm³): %s" % ("TEMİZ" if not cak else "%d BULGU" % len(cak)))
    for x_ in cak[:30]: print("   %10.1f mm3  %s  <->  %s" % x_)
    bb = cq.Compound.makeCompound([dunya(p) for p in ps if p["birim"].startswith("F_TP10")]).BoundingBox()
    print("ZARF (fırın): x %.0f…%.0f (%.0f) · y %.0f…%.0f · z %.0f…%.0f" % (bb.xmin, bb.xmax, bb.xlen, bb.ymin, bb.ymax, bb.zmin, bb.zmax))
    print("YERLEŞİM: gövde %.0f–%.0f · ön oda %.0f–%.0f · giriş duvarı %.0f–%.0f · ISITILAN %.0f–%.0f = %.0f · çıkış duvarı %.0f–%.0f · bant uçtan uca %.0f–%.0f · rulolar %.0f / %.0f · aynı anda %d ürün (adım %.0f) · güç ≈%.1f kW (VARSAYIM)"
          % (X_F0, X_F1, X_F0, X_DUV0, X_DUV0, X_TUN0, X_TUN0, X_TUN1, ODA, X_TUN1, X_F1, BANT_X[0], BANT_X[1], RULO_X[0], RULO_X[1], N_URUN, ADIM, GUC))
    print("ÇİT (K bandında): %s → %s" % (tuple(round(v, 1) for v in CC_A), tuple(round(v, 1) for v in CC_B)))
    for x in (2400, 2600, 3300, 3990, 4030, 4100, 4200, 4257, 4300):
        print("   ürün merkezi x %4d → z %.1f" % (x, urun_z(x)))
    # tek başına GLB: yalnız fırın (uyarlama parçaları hariç), yerel koordinat, ekranlı yüz izleyiciye dönük
    ton = {}
    for p in ps:
        if not p["birim"].startswith("F_TP10"): continue
        ton.setdefault((p["mal"], p["birim"]), Mesh()).ekle(ag(cq.Workplane(obj=dunya(p).translate(cq.Vector(-XC_TP, -YG0, 0.0)))))
    parca = [("TP10U__%s__%s" % (b, m), msh, m) for (m, b), msh in sorted(ton.items())]
    for _a, msh, _m in parca:
        msh.P = [(-q[0], q[1], -q[2] - D_TP * MM) for q in msh.P]; msh.N = [(-n[0], n[1], -n[2]) for n in msh.N]
    yol = os.path.join(KOK, "otonom", "hat3d", "firin_tp10_v4.glb")
    b1 = glb_yaz(yol, parca)
    _dk = {"ad": K3.doku_ad("TP10 KESİTİ · 1500", "uzatılmış fırın · AUTOKITCH v3"), "montaj": K3.doku_ad("TP10-UZUN", "ana makine v48", ok_sol=False)}
    b2, prim, sorun, _u = K3.usdz_yaz([yol.replace(".glb", ".usdz")], "firin_tp10_v4", parca, _dk)
    print("firin_tp10_v4.glb %.0f KB · usdz %.0f KB · %d prim · USD: %s · %.0f sn" % (b1 / 1024.0, b2 / 1024.0, prim, "GEÇTİ" if not sorun else sorun, time.time() - t0))
    assert not cak, "kendi arasinda cakisma var"
    sys.stdout.flush(); os._exit(0)
