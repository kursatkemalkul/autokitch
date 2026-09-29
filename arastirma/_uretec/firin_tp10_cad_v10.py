# -*- coding: utf-8 -*-
"""firin_tp10_cad_v10 (29 Eyl 2026): ısıtılan 1316 / 4 ürün korunur · yükleme bandı ısıtılan bölgenin başında (yap_firin_tp10_cad_v10.py).
firin_tp10_cad_v9 (29 Eyl 2026): BANTLI TABLA — yükleme bandı ön odada (352), ısıtılan 1028, ağız alt 965 (yap_firin_tp10_cad_v9.py).
AUTOKITCH · F FIRIN · TP10 KESİTİ · 1500 · v8 (27 Eyl 2026 gece): ÖN DÜZLEM +79 · TEMİZ KUTU (SPEC_on_duzlem_v63 §2.4) — gövde, ön yüz, ürün yolu
v7 ile BİREBİR; Z_ON = ZS (+79) sabiti; f_arka_saci + F_ARKA_SAC KALKTI (yerine firin_ust_kabin_cad_v1 tek parça arka sacı 788–1862); iç havada parçalar
bağlandı (bant kızakları, ray / ısıtıcı braketleri, yatak cepleri ve delikleri yatak ölçüsüne, çıkış tahrik konsolu, giriş bandı yuvaları + taşıyıcı U,
ölü plaka kanadı 940, giriş duvarı 1 mm sac). Önceki: firin_tp10_cad_v7.py (yama: yap_firin_tp10_v8.py)
v7 (27 Eyl 2026): ALÇAK HAT (SPEC_alcak_hat_v57 · resim ALCAK_HAT_RESIM1_v4) — fırının HER ŞEYİ 168 aşağı:
bant 1166 → 998 · gövde 788–1305 · raf üstü 1348 · çıkış plakası K bandı 996'ya. v6'nın mutlak y sabitleri (GB_MOTOR 1290, YARIK_V2, K_BANT 1164,
giriş ağzı kesiği 1152–1210, plaka ayağı 1220–1240) artık BANT_UST_HAT / DISK_UST'e bağlı; x, z, ölçüler, parça adları, birimler, gruplar v6 ile aynı.
Önceki: firin_tp10_cad_v6.py
v6 (27 Eyl 2026): KUTU YEDEĞİ TEK YERDE fırın üstü sol (320 kutu, raf 4 mm, 10 takoz) · v5: FIRIN 79 mm ÖNE — Kemal "fırını taşı, hizalanma olsun". Gövde + konveyör +
giriş bandı + ölü plaka +79 z (ekle() taşır): tünel ön duvarı ön yüzün ÖNÜNDE (0…+79 çıkıntı, y 956–1473), ürün fırında −170 (tabla ekseni),
K giriş çiti KALKTI. Raf/kalkan/takoz/arka sac yerinde. Önceki: firin_tp10_cad_v4.py
v3/v4 (26 Eyl 2026 gece): AUTOKITCH · F FIRIN · Sveba Dahlen TP10 KESİTİ, GÖVDESİ F MODÜLÜNE (1500) UZATILMIŞ · 3B MODEL + HATTA UYARLAMA
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
KOORDİNAT: DÜNYA (hat). x hat boyu · y yerden · v8: ÖN DÜZLEM z = Z_ON = +79 (fırın gövdesinin ön yüzü = bütün istasyon önlerinin dış yüzü) · arka yüz −830.
Gövde parçaları yerel z 0…−730 çizilir; ekle() KAYAN birimlerini +ZS (79) taşır → dünya +79…−651. Arkada üst kabinin tek parça arka sacı −830 (firin_ust_kabin_cad_v1).
"""
import math, os, sys
import cadquery as cq

U = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, U)
KOK = os.path.dirname(os.path.dirname(U))
from kaset_3d_v3 import Mesh, MM, MALZEME
import bantli_tabla_montaj_v1 as BT                                   # v9: yükleme bandı + kaset burnu (tek kaynak bantli_tabla_cad_v1)

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
BANT_UST_HAT = 998.0                             # v7 ALÇAK HAT (v6 1166 − 168) · kot zinciri: disk 1000 → fırın bandı 998 → K 996
DISK_UST = BANT_UST_HAT + 2.0                    # 1000 · v7: TOPPING çalışma diski üstü (mekanizma tabanı 892 + 108) · TOPPING'e bakan kotlar buna bağlı
YG0 = BANT_UST_HAT - BANT_Y                      # 788 gövde altı (v7: çekmeceli dolabın üstü = düz çizgi 788)
YG1 = YG0 + H_GOV                                # 1305 gövde üstü
DUVAR = 60.0                                     # uç duvarı (yalıtım + rulo içinde)
ON_ODA0 = 64.0                                   # v10: v8 ön odası (ısıtılan 1316 korunur · Kemal: kapasite düşmez)
ON_ODA = ON_ODA0                                 # 64 · v10 (v9: 352)
X_DUV0 = X_F0 + ON_ODA                           # 2564 giriş duvarı dış yüzü
X_TUN0, X_TUN1 = X_DUV0 + DUVAR, X_F1 - DUVAR    # 2624 · 3940 ısıtılan oda
ODA = X_TUN1 - X_TUN0                            # 1316
ODA_X = (X_TUN0, X_TUN1)
TUN_Y = (YG0 + 33.0, YG0 + 307.0)                # 821 · 1095 tünel boşluğu (alt bölme + ağız + üst ısıtıcı yuvası)
AGIZ_Y = (BANT_UST_HAT, BANT_UST_HAT + IC_H)     # 998 · 1083 ağız
# ---- konveyör (VARSAYIM: rulo çapı, ray) ----
RULO_R, BANT_K = 20.0, 6.0                       # Ø40 rulo · tel örgü 6
SARIM_R = RULO_R + BANT_K                        # 26
RULO_Y = BANT_UST_HAT - BANT_K - RULO_R          # 972
RULO_X = (round(BT.YB_SON + 10.7 + 26.0), X_F1 - DUVAR / 2.0)   # v10: 2882 (yükleme bandının sonundan 10,7 + sarım 26; ısıtılan bölgenin içinde) · 3970
BANT_X = (RULO_X[0] - SARIM_R, RULO_X[1] + SARIM_R)   # 2568 · 3996 uçtan uca 1428
ALT_KOL_Y = (RULO_Y - RULO_R - BANT_K, RULO_Y - RULO_R)   # 946 · 952
GECIT_Y = (ALT_KOL_Y[0] - 6.0, AGIZ_Y[1])        # 940 · 1083 uç duvarı geçidi (alt kol + rulo + ağız)
RAY_Y = (GECIT_Y[0] + 2.0, BANT_UST_HAT - 8.0)   # 942 · 990
RAY_X = (RULO_X[0] - 6.0, RULO_X[1] + 6.0)
ADIM = 310.0                                     # ürün adımı (Ø300 + 10) [hat kuralı]
N_URUN = int(ODA // ADIM)                        # 4
GUC = GUC_TP10 * ODA / ODA_TP10                  # 14,0 kW VARSAYIM (ısıtıcı yoğunluğu TP10 ile aynı)
# ---- ürün ----
ZT = -170.0                                      # hat ürün ekseni (tabla · K)
Z_URUN_FIRIN = -249.0                            # fırında ürün merkezi (Ø300 ön kenarı −99: tünel ön duvarına 20)
ZS = 79.0                                        # v5: gövde + konveyör + giriş bandı + ölü plaka ÖNE kayma (Kemal 27 Eyl) → tünel ön duvarı ön yüzün önünde (çıkıntı)
Z_ON = ZS                                        # v8 · ÖN DÜZLEM +79 (SPEC_on_duzlem_v63): bütün ön panel / kapak dış yüzleri = fırın gövdesinin ön yüzü
KAYAN = ("F_TP10_GOVDE", "F_TP10_KONVEYOR", "F_GIRIS_BANDI", "F_CIKIS_PLAKA")   # ekle() bu birimleri +ZS z'ye taşır (raf, kalkan, arka sac yerinde)
Z_URUN_FIRIN_D = Z_URUN_FIRIN + ZS               # −170 · DÜNYA: fırında ürün ekseni = tabla ekseni (kayma yok)
TUNEL_Z_D = (TUNEL_Z[0] + ZS, TUNEL_Z[1] + ZS)   # −406 … 0 (dünya)
BANT_Z_D = (BANT_Z[0] + ZS, BANT_Z[1] + ZS)      # −394,5 … −13,5 (dünya)
CIKINTI = ((X_F0, X_F1), (0.0, ZS))              # ön yüzün önündeki gövde bandı (x · z); y = YG0…YG1
PZ_R = 150.0
# ---- giriş ön odası: giriş bandı + TOPPING X tahriki cebi ----
X_DISK_KENAR = BT.AKT + BT.H.X_UC                # 2518,9 · v9: kaset burnu aktarmada (yükleme bandı burnuna 3) · v8: disk kenarı 2507
YB_BURUN, YB_TAHRIK, YB_SON = BT.YB_BURUN, BT.YB_TAHRIK, BT.YB_SON   # v9 yükleme bandı (x, y, r) · sağ ucu 2845,3
GB_RY = YB_BURUN[1]                              # v9 uyumluluk: yükleme bandı burun ekseni
GB_XB = YB_BURUN[0]                              # v9: yükleme bandı burnu
GB_XT = YB_TAHRIK[0]                             # v9: yükleme bandı tahriki
GB_Z = (Z_URUN_FIRIN - 160.0, Z_URUN_FIRIN + 160.0)   # −409 … −89 · bant 320, ekseni ürün ekseninde
GB_MOTOR = (YB_TAHRIK[0] - 50.0, BANT_UST_HAT + 124.0, -431.0)   # v9: yükleme bandı motoru teknik bölmede, tahrik rulosunun sol üstünde (GT2 1:1; fırın bandı gergisi 2844–2864 boş kalır)
# TOPPING'in F'ye taşan parçaları (ölçüldü 26 Eyl, dünya): mekanizma teknesi x ≤ 2585 · y 1061,5–1091,5 · z −415…−5 · ray/kayış kirişleri
# x ≤ 2585 · y ≤ 1080,5 · X motoru x ≤ 2563 · y ≤ 1121 · z −462…−397,5 · kaidesi x ≤ 2580 · y ≤ 1135 (pahlı köşe 1112, x > 2560) ·
# z −397,5…−389,5 · uç tamponu x ≤ 2570 · y 1103,5–1123,5 · z −80…−65. (v47'de de taşıyordu; D_FIRIN_GOVDE "zon" muafiyeti gizliyordu.)
# v7: yukarıdaki ölçüler v6 kotlarıdır (TOPPING tabanı 1060); alçak hatta TOPPING ile fırın birlikte 168 aşağı → bağıl konum aynı.
# v3: CEP YOK — TOPPING v24 teknesi 2500'de bitiyor (motor sol uca, avara sağa, kelepçeler solda).
UST_RAF_Y = (YG1 + 39.0, YG1 + 43.0)                            # 1344–1348 · fırın üstünde HAVALANDIRMALI raf (39 mm takoz + 4 mm plaka) · v6: 320 kutu + kompresör = 76 kg
TAKOZ_XZ = tuple((x_, z_) for z_ in (-30.0, -408.0) for x_ in (X_F0 + 30.0, X_F0 + 390.0, XC_TP, X_F0 + 1110.0, X_F1 - 30.0))   # v6: 10 takoz, aralık 360
KOMP_ACIKLIK = (3595.0, X_F1 - 9.0, -385.0, -75.0)                  # v8 · denetçi #4: raf açıklığı x 3595–3991 · z −385…−75 (kompresör tavası asılır; takozlar dışında)
ISI_KALKANI_Y = (YG1 + 10.0, YG1 + 10.8)                        # 1315–1315,8 · 0,8 mm 304 ışınım kalkanı (fırın üstünden 10 mm)
# TOPPING çıkış yarığı çerçevesi v2 (dünya): dış · açıklık — tabla 989–992 + disk 992–1000 (v6 1157–1168) aktarmada x 2507'ye kadar geldiği için alt çıta 987'nin altında · v7: y'ler DISK_UST'e bağlı (dış −23…+42 · açıklık −13…+38)
YARIK_V2 = ((2492.0, 2498.5, BT.H.AGIZ_YENI_ALT - 10.0, DISK_UST + 42.0, -417.0, 0.0), (2491.0, 2499.5, BT.H.AGIZ_YENI_ALT, DISK_UST + 38.0, -409.0, -8.0))   # v9 = topping_cad_v27 (alt 965 · ön −8)     # v5: ön çıta −13…−5 (ürün −170'te ön kenarı −20: montaj v51 denetimi çıtayı 1 mm kesiyordu)
# ---- çıkış: ölü plaka + K giriş çiti ----
K_BANT_BAS = 4020.0                              # K kuyruk rulosu sarımının sol ucu (X_KUYRUK 37 − 17)
OLU_X = (BANT_X[1] + 1.0, K_BANT_BAS - 2.0)      # 3997 · 4018
TAN20 = math.tan(math.radians(20.0))
CC_A = (K_BANT_BAS + 6.0, Z_URUN_FIRIN - PZ_R - 5.0)                       # (4026, −404) çit K bandında başlar
CC_B = (CC_A[0] + (ZT - PZ_R - CC_A[1]) / TAN20, ZT - PZ_R)                # (4256,8, −320) → ürün −170'te
K_BANT, K_BANT_Z = BANT_UST_HAT - 2.0, (-412.0, -12.0)   # 996 (v6 1164) · K bandı üstü = kesme_cad_v4 BANT (kot zinciri: fırın bandı − 2) · genişlik 400
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
    if birim in KAYAN and ZS:                                                            # v5: fırın + giriş bandı + ölü plaka 79 öne (dünya)
        wp = wp.translate((0.0, 0.0, ZS))
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
    kab = kab.cut(kut(x0 - 1.0, x0 + 2.0, BT.H.AGIZ_YENI_ALT, DISK_UST + 42.0, -341.0 - ZS, -10.0 - ZS))   # v9: alt 984 → 965 (kaset rotor kabı)   # v7: 984–1042 (disk −16…+42; v6 1152–1210)                # v5: dünyada −341…−10 kalır (disk 0…−340); çıkıntıya delik açılmaz                    # giriş ağzı (TOPPING çıkış yarığına bakar; tabla + disk 2507'ye kadar girer)
    kab = kab.cut(kut(x1 - 2.0, x1 + 1.0, GECIT_Y[0] + 4.0, GECIT_Y[1] + 2.0, TUNEL_Z[0] - 2.0, TUNEL_Z[1] + 2.0))   # çıkış ağzı (K'ye)
    ekle("govde_kabugu", kab, "paslanmaz", G, kaynak="föy kesiti 730 × 517 · boy 1500 ÖZEL",
         bom=("Fırın gövde kabuğu · paslanmaz 1,5", 1, "TP10 kesiti · boy 1500 (özel sipariş)", "uç kutusu yok · giriş ön odası + 2 uç duvarı"))
    # --- ısıtılan oda kaplaması 1 mm (uçları geçit boyunca açık) ---
    _ybm = silz(BT.YB_TAHRIK[0], BT.YB_TAHRIK[1], 5.5, -520.0, -80.0)                          # v10: yükleme bandı tahrik mili (yerel z)
    kap = kut(X_TUN0 - 1.0, X_TUN1 + 1.0, TUN_Y[0] - 1.0, TUN_Y[1] + 1.0, TUNEL_Z[0] - 1.0, TUNEL_Z[1] + 1.0).cut(_ybm).cut(silz(RULO_X[0], RULO_Y, 10.2, -600.0, -40.0)) \
        .cut(kut(X_TUN0, X_TUN1, TUN_Y[0], TUN_Y[1], TUNEL_Z[0], TUNEL_Z[1])) \
        .cut(kut(X_TUN0 - 4.0, X_TUN1 + 4.0, GECIT_Y[0], GECIT_Y[1], TUNEL_Z[0], TUNEL_Z[1]))
    ekle("tunel_kaplamasi", kap, "paslanmaz", G, kaynak="VARSAYIM (iç)")
    # --- yalıtım (taşyünü): ön odadan sonra, oda + iki uç duvarı; geçitler, rulo milleri, ön yataklar, X tahriki cebi ---
    yal = kut(X_DUV0, x1 - 1.5, y0 + 1.5, y1 - 1.5, TUNEL_Z[0] - 3.5, -1.5).cut(_ybm) \
        .cut(kut(X_TUN0 - 1.0, X_TUN1 + 1.0, TUN_Y[0] - 1.0, TUN_Y[1] + 1.0, TUNEL_Z[0] - 1.0, TUNEL_Z[1] + 1.0)) \
        .cut(kut(X_DUV0 - 1.0, X_TUN0 + 1.0, GECIT_Y[0], GECIT_Y[1], TUNEL_Z[0], TUNEL_Z[1])) \
        .cut(kut(X_TUN1 - 1.0, x1 + 1.0, GECIT_Y[0], GECIT_Y[1], TUNEL_Z[0], TUNEL_Z[1]))
    for rx in RULO_X:
        yal = yal.cut(silz(rx, RULO_Y, 10.5, -600.0, -40.0)).cut(kut(rx - 18.0, rx + 18.0, RULO_Y - 16.0, RULO_Y + 16.0, -77.0, -1.5))   # v8: ön yatak cebi = yatak (36 × 32) + yatak konsolu, kabuğun ön iç yüzüne kadar (v7 40 × 36 × 34, 2 mm boştu)
    ekle("yalitim_tasyunu", yal, "yalitim", G, kaynak="VARSAYIM (iç)",
         bom=("Yalıtım (taşyünü) · uç duvarları 60", 1, "üretici", "geçitler: bant üst kolu + alt kolu + rulo · ön yatak cepleri"))
    duv = kut(X_F0 + 1.5, x1 - 1.5, y0 + 1.5, y1 - 1.5, TUNEL_Z[0] - 5.5, TUNEL_Z[0] - 4.0) \
        .cut(silz(YB_TAHRIK[0], YB_TAHRIK[1], 5.5, TUNEL_Z[0] - 7.0, TUNEL_Z[0] - 2.0))   # v9: yükleme bandı tahrik mili geçişi (v8: giriş bandı motoru penceresi)
    for rx in RULO_X:
        duv = duv.cut(silz(rx, RULO_Y, 10.5, -600.0, -40.0))
    ekle("teknik_bolme_duvari", duv, "paslanmaz", G, kaynak="≈ uç görünüşü 237 mm",
         bom=("Teknik bölme (sürücü · kontaktör · SSR · bant motoru · gergi)", 1, "katalog kesiti", "≈ 239 derinlik, ekran tarafı"))
    # --- ısıtıcılar: üstte + altta 2'şer bölge (şematik) ---
    xm = (X_TUN0 + X_TUN1) / 2.0
    for i, (a, b) in enumerate(((X_TUN0 + 5.0, xm - 5.0), (xm + 5.0, X_TUN1 - 5.0))):
        ekle("ust_isitici_%d" % (i + 1), kut(a, b, TUN_Y[1] - 10.0, TUN_Y[1] - 1.0, BANT_Z[0], BANT_Z[1]), "ir", G, kaynak="föy: IR üst/alt ayrı · yerleşim VARSAYIM",
             bom=("Kızılötesi ısıtıcı · üst · bölge %d" % (i + 1), 1, "katalog kesiti", "400 °C · toplam ≈%.0f kW (VARSAYIM: TP10'un 9,5 kW'ı boyla ölçekli)" % GUC) if i == 0 else None)
        ekle("alt_isitici_%d" % (i + 1), kut(max(a, RULO_X[0] + SARIM_R + 5.0), b, RULO_Y - 12.0, RULO_Y - 4.0, BANT_Z[0], BANT_Z[1]), "ir", G, kaynak="föy: IR üst/alt ayrı · yerleşim VARSAYIM",
             bom=("Kızılötesi ısıtıcı · alt · bölge %d" % (i + 1), 1, "katalog kesiti", "bandın üst ve alt kolu arasında") if i == 0 else None)
    ekle("kirinti_tepsisi", kut(max(X_TUN0 + 12.0, RULO_X[0] - SARIM_R + 4.0), X_TUN1 - 12.0, TUN_Y[0], TUN_Y[0] + 5.0, TUNEL_Z[0] + 2.0, TUNEL_Z[1] - 2.0), "paslanmaz", G, kaynak="VARSAYIM")
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
             bom=("Konveyör bandı · paslanmaz tel örgü", 1, "381 × 1428 uçtan uca (özel boy)", "üstü %.0f · uçları gövde içinde" % BANT_UST_HAT) if j == 0 else None)
    ekle("bant_alt_kol", kut(RULO_X[0], RULO_X[1], ALT_KOL_Y[0], ALT_KOL_Y[1], z0, z1), "tel_bant", K, kaynak="VARSAYIM")
    for s, ad, x in ((-1.0, "giris", RULO_X[0]), (1.0, "cikis", RULO_X[1])):
        sar = silz(x, RULO_Y, SARIM_R, z0, z1).cut(silz(x, RULO_Y, RULO_R, z0 - 1, z1 + 1)).cut(kut(x, x - s * 100.0, RULO_Y - 40, RULO_Y + 40, z0 - 1, z1 + 1))
        g = "RULO_TP_%s" % ad.upper()
        ekle("bant_sarimi_%s" % ad, sar, "tel_bant", K, grup=g, kaynak="VARSAYIM Ø40 rulo")
        ekle("rulo_%s" % ad, silz(x, RULO_Y, RULO_R, z0 + 1.5, z1 - 1.5).cut(silz(x, RULO_Y, 10.0, z0, z1)), "celik", K, grup=g, kaynak="VARSAYIM Ø40",
             bom=("Bant ucu rulosu Ø40 (VARSAYIM)", 2, "üretici", "giriş: gergili · çıkış: tahrikli · uç duvarının içinde") if s < 0 else None)
        zb = -520.0 if s < 0 else -586.0
        ekle("rulo_mili_%s" % ad, silz(x, RULO_Y, 10.0, zb, -47.0), "celik", K, grup=g, kaynak="VARSAYIM Ø20 · ön duvara gömülü yataktan arka teknik bölmeye")
        ekle("on_yatak_%s" % ad, kut(x - 18.0, x + 18.0, RULO_Y - 16.0, RULO_Y + 16.0, -77.0, -47.0).cut(silz(x, RULO_Y, 10.0, -78.0, -46.0)), "koyu", K,
             kaynak="VARSAYIM · ön duvar yalıtımında cep")
        ekle("arka_yatak_%s" % ad, kut(x - 18.0, x + 18.0, RULO_Y - 16.0, RULO_Y + 16.0, -520.0, -500.0).cut(silz(x, RULO_Y, 10.0, -521.0, -499.0)), "koyu", K,
             kaynak="VARSAYIM · teknik bölmede")
    _del = lambda w: w.cut(silz(RULO_X[0], RULO_Y, 10.2, -500.0, -40.0)).cut(silz(RULO_X[1], RULO_Y, 10.2, -500.0, -40.0))
    ekle("on_ray", _del(kut(RAY_X[0], RAY_X[1], RAY_Y[0], RAY_Y[1], -84.0, -81.0)), "paslanmaz", K, kaynak="VARSAYIM")
    ekle("arka_ray", _del(kut(RAY_X[0], RAY_X[1], RAY_Y[0], RAY_Y[1], -484.0, -481.0)), "paslanmaz", K, kaynak="VARSAYIM")
    # gergi (giriş rulosu, teknik bölmede): arka yatak kızakta, M8 itme vidası + konsol
    ekle("gergi_konsolu", kut(RULO_X[0] - 38.0, RULO_X[0] - 34.0, RULO_Y - 20.0, RULO_Y + 20.0, -520.0, TUNEL_Z[0] - 5.5), "celik", K, kaynak="VARSAYIM",
         bom=("Bant gergisi · M8 itme vidası + kontra (arka) · ön yatak yuvası uzun delikli", 1, "üretici", "teknik bölmeden ayarlanır"))
    ekle("gergi_vidasi", silx(RULO_Y, -510.0, 4.0, RULO_X[0] - 34.0, RULO_X[0] - 18.0), "celik", K, kaynak="VARSAYIM M8")
    # tahrik (çıkış rulosu, teknik bölmede): sonsuz vidalı redüktör mil üstünde + motor x boyunca
    ekle("tahrik_reduktoru", kut(RULO_X[1] - 32.0, RULO_X[1] + 26.0, RULO_Y - 35.0, RULO_Y + 35.0, -586.0, -521.0).cut(silz(RULO_X[1], RULO_Y, 10.0, -587.0, -520.0)), "koyu", K,
         kaynak="VARSAYIM", bom=("Bant tahriki · sonsuz vidalı redüktör (arka yatağın arkasında, delik milli) + motor", 1, "üretici (TP10'da uç kutusunda)", "bant hızı 1316 mm / pişme süresi = 6 mm/s (3,5 dk) · ≈2,6 dev/dk"))
    ekle("tahrik_motoru", silx(RULO_Y, -553.0, 30.0, RULO_X[1] - 170.0, RULO_X[1] - 32.0), "motor", K, kaynak="VARSAYIM Ø60 × 138")
    # ---- v8 · İÇ HAVADA PARÇALAR BAĞLANIR (SPEC_on_duzlem_v63 §2.4 · denetim_temas_v1: v7'de 67 bileşen / 77 parça havadaydı) ----
    # (1) bant kızakları: tel örgü üst kolun iki kenarı 10 mm 304 kızağa oturur (y RAY üstü 990 … şerit altı 992), kızak rayın üstünde (v7: raylar bandın dışında, şeritler 2 mm havada)
    #     x RULO_X ± 20 (denetçi #6: ± 10'da ruloya 0,59 mm; 400 °C'de kızak ≈ 9 mm uzar → uç rulonun dışında, çıkış ucu uzun delikli) · geçit içinden geçer
    KX = (RULO_X[0] + 20.0, RULO_X[1] - 20.0)
    ekle("bant_kizagi_on", kut(KX[0], KX[1], RAY_Y[1], BANT_UST_HAT - BANT_K, BANT_Z[1] - 10.0, -81.0), "paslanmaz", K, kaynak="VARSAYIM",
         bom=("Bant kızağı 304 · 2 mm · L 1336", 2, "lazer + büküm", "v8: üst kol kenarları (10 mm) kızağa, kızak raya oturur · 400 °C (UHMW olmaz) · giriş ucu raya sabit, çıkış ucu uzun delikli (ısıl uzama ≈ 9 mm)"))
    ekle("bant_kizagi_arka", kut(KX[0], KX[1], RAY_Y[1], BANT_UST_HAT - BANT_K, -484.0, BANT_Z[0] + 10.0), "paslanmaz", K, kaynak="VARSAYIM")
    # (2) ray braketleri: ön ray (z −84…−81) → kaplama ön duvarı (−79) 2 mm · arka ray (−484…−481) → kaplama arka duvarı (−485) 1 mm · 5 + 5 adet (aralık 300)
    for i, xb in enumerate((2960.0, 3200.0, 3440.0, 3680.0, 3900.0)):                        # v9: ray 2876–3976 (v8: 2700…3900)
        ekle("tunel_ray_braketi_on_%d" % i, kut(xb - 10.0, xb + 10.0, RAY_Y[0], RAY_Y[0] + 15.0, -81.0, TUNEL_Z[1]), "paslanmaz", K, kaynak="VARSAYIM",
             bom=("Ray braketi 304 · 20 × 15 (ön 2 mm · arka 1 mm ara parça, kaplamaya punta)", 10, "lazer", "v8: raylar kaplamaya bağlı") if i == 0 else None)
        ekle("tunel_ray_braketi_arka_%d" % i, kut(xb - 10.0, xb + 10.0, RAY_Y[0], RAY_Y[0] + 15.0, TUNEL_Z[0], -484.0), "paslanmaz", K, kaynak="VARSAYIM")
    # (3) ısıtıcı braketleri: üstler tavana 1 mm askı lamasıyla (2 şerit / ısıtıcı) · altlar bant kenarından (−92,5 / −473,5) raylara (−84 / −481) 8,5 / 7,5 mm lamayla
    for i, (a, b) in enumerate(((X_TUN0 + 5.0, xm - 5.0), (xm + 5.0, X_TUN1 - 5.0))):
        for j, (za_, zb_) in enumerate(((BANT_Z[0], BANT_Z[0] + 15.0), (BANT_Z[1] - 15.0, BANT_Z[1]))):
            ekle("ust_isitici_askisi_%d_%d" % (i + 1, j), kut(a, b, TUN_Y[1] - 1.0, TUN_Y[1], za_, zb_), "paslanmaz", G, kaynak="VARSAYIM",
                 bom=("Üst ısıtıcı askı laması 304 · 1 mm × 15", 4, "lazer", "v8: ısıtıcı tavan kaplamasına perçinli (1 mm boştu)") if i == 0 and j == 0 else None)
        ekle("alt_isitici_braketi_%d_on" % (i + 1), kut(max(a, RULO_X[0] + SARIM_R + 5.0), b, RULO_Y - 12.0, RULO_Y - 4.0, BANT_Z[1], -84.0), "paslanmaz", G, kaynak="VARSAYIM",
             bom=("Alt ısıtıcı taşıyıcı laması 304 · 8 × 8,5 / 7,5", 4, "lazer", "v8: alt ısıtıcı raylara bağlı (bant kolları arasında dayanaksızdı)") if i == 0 else None)
        ekle("alt_isitici_braketi_%d_arka" % (i + 1), kut(max(a, RULO_X[0] + SARIM_R + 5.0), b, RULO_Y - 12.0, RULO_Y - 4.0, -481.0, BANT_Z[0]), "paslanmaz", G, kaynak="VARSAYIM")
    # (4) çıkış tahrik grubu: redüktör üstünden teknik bölme duvarına L konsol 5 mm (redüktör tork kolu) — v7'de grup duvardan 9,5 mm geride, hiçbir yere bağlı değildi
    ekle("tahrik_konsolu", kut(RULO_X[1] - 30.0, RULO_X[1] + 24.0, RULO_Y + 35.0, RULO_Y + 40.0, -586.0, TUNEL_Z[0] - 5.5)
         .union(kut(RULO_X[1] - 30.0, RULO_X[1] + 24.0, RULO_Y + 35.0, RULO_Y + 88.0, TUNEL_Z[0] - 10.5, TUNEL_Z[0] - 5.5)), "paslanmaz", K, kaynak="VARSAYIM",
         bom=("Tahrik konsolu 304 · L 5 mm · 54 × 95 + 54 × 53", 1, "lazer + büküm", "v8: redüktör → teknik bölme duvarı (M6 × 4) · tork kolu"))
    # (5) giriş duvarının ön odaya bakan x 2564 yüzü: 1 mm 304 sac (v7: taşyünü çıplaktı) · geçit (bant + rulo + ağız) açık
    ekle("giris_duvari_saci", kut(X_DUV0 - 1.0, X_DUV0, y0 + 1.5, y1 - 1.5, TUNEL_Z[0] - 3.5, -1.5)
         .cut(kut(X_DUV0 - 2.0, X_DUV0 + 1.0, GECIT_Y[0], GECIT_Y[1], TUNEL_Z[0], TUNEL_Z[1])), "paslanmaz", G, kaynak="VARSAYIM (özel sipariş şartnamesine)",
         bom=("Giriş duvarı kaplama sacı 304 · 1 mm", 1, "≈ 514 × 408 · geçit kesikli", "v8: ön oda tarafında yalıtımı örter (kabuk iç yüzlerine punta)"))
    # (6) denetçi #5 · ön yataklar yapıya: flanş plakası 3 mm (yatak ön yüzü −47 … −44, Ø22 mil boşluğu) + 2 lama 3 × 32 kabuğun ön iç yüzüne (−44 … −1,5)
    for ad_, x_ in (("giris", RULO_X[0]), ("cikis", RULO_X[1])):
        _k = kut(x_ - 18.0, x_ + 18.0, RULO_Y - 16.0, RULO_Y + 16.0, -47.0, -44.0).cut(silz(x_, RULO_Y, 11.0, -48.0, -43.0))
        for xa_ in (x_ - 18.0, x_ + 15.0):
            _k = _k.union(kut(xa_, xa_ + 3.0, RULO_Y - 16.0, RULO_Y + 16.0, -44.0, -1.5))
        ekle("on_yatak_konsolu_%s" % ad_, _k, "paslanmaz", K, kaynak="VARSAYIM",
             bom=("Ön yatak konsolu 304 · flanş plakası 36 × 32 × 3 + 2 lama 3 × 32 × 42,5", 2, "lazer + kaynak", "denetçi #5: yatak kabuğun ön iç yüzüne (M5 × 2) · giriş konsolu x yönünde uzun delikli (gergi)") if ad_ == "giris" else None)
    # (7) denetçi #5 · arka çıkış yatağı → teknik bölme duvarı: 2 lama 3 × 32 (yatak ön yüzü −500 … duvar arka yüzü −490,5) · redüktör + motor delik mil üstünde, tork kolu tahrik_konsolu
    _k = kut(RULO_X[1] - 18.0, RULO_X[1] - 15.0, RULO_Y - 16.0, RULO_Y + 16.0, -500.0, TUNEL_Z[0] - 5.5).union(
        kut(RULO_X[1] + 15.0, RULO_X[1] + 18.0, RULO_Y - 16.0, RULO_Y + 16.0, -500.0, TUNEL_Z[0] - 5.5))
    ekle("arka_yatak_konsolu_cikis", _k, "paslanmaz", K, kaynak="VARSAYIM",
         bom=("Arka çıkış yatağı konsolu 304 · 2 lama 3 × 32 × 9,5", 1, "lazer", "denetçi #5: yatak teknik bölme duvarına (M5 × 2) · yatak yalnız mile bağlıydı"))


# ================================================================ 2 · ÜRÜN YOLU ================================================================
# v5: ürün baştan sona −170 (fırın 79 öne alındı). CC_A/CC_B yalnız eski montaj arayüzü için duruyor (çit YOK).
def _cit_noktalari(A, B, n=400):
    return [(A[0] + (B[0] - A[0]) * i / n, A[1] + (B[1] - A[1]) * i / n) for i in range(n + 1)]


_CC = _cit_noktalari(CC_A, CC_B)


def urun_z(xc):
    """v5: ürün fırına ve K'ye −170'te (tabla ekseni) DÜZ gider — diskte kayma yok, K giriş çiti yok."""
    return ZT


# ================================================================ 3 · HATTA UYARLAMA (bizim parçalar) ================================================================
def adaptor(nema23=None):
    GB, CP, KC_, AS = "F_GIRIS_BANDI", "F_CIKIS_PLAKA", "F_K_GIRIS_CITI", "F_ARKA_SAC"
    Y = BANT_UST_HAT; BR, BK = 10.0, 1.5
    RY, XB, XT = GB_RY, GB_XB, GB_XT
    ZA, ZB_ = GB_Z
    # ---- 3.1 v9 · YÜKLEME BANDI (bantli_tabla_cad_v1 bölüm 5 · DÜNYA, KAYMAZ): kaset burnu 2518,9 → yükleme bandı 2522 → fırın bandı 2856 · PTFE 296 · eksen −170 ----
    YB_ = "F_YUKLEME_BANDI"
    XT_, YT_, RT_ = YB_TAHRIK
    for p_ in BT.YB:
        sh_ = p_["sh"]
        if p_["ad"] == "yb_tahrik_rulosu":                                                      # v10: mil arkada teknik bölmeye (GT2) · önde çerçevede biter (tünelin ön duvarına girmez)
            _zf = BT.ZE + BT.W_B / 2.0 + 12.0
            sh_ = silz(XT_, YT_, RT_, BT.ZE - BT.W_B / 2.0 - 11.5, _zf - 0.5).union(silz(XT_, YT_, 5.0, -436.0, _zf + 5.0)).val()
        if p_["ad"].startswith("yb_ayak_"):                                                     # v10: ön odada gövde tabanına · tünelde tünel tabanına
            _zf0, _zf1 = BT.ZE - BT.W_B / 2.0 - 12.0, BT.ZE + BT.W_B / 2.0 + 12.0
            _xb, _y0 = ((2540.0, YG0 + 1.5) if p_["ad"].endswith("_0") else (2790.0, TUN_Y[0]))
            sh_ = kut(_xb - 10.0, _xb + 10.0, _y0, 962.0, _zf0 - 5.0, _zf1 + 5.0).cut(kut(_xb - 11.0, _xb + 11.0, _y0 + 5.0, 957.0, _zf0, _zf1)).val()
        g_ = {"yb_burun_rulosu": "RULO_GB_BURUN", "yb_tahrik_rulosu": "RULO_GB_TAHRIK"}.get(p_["ad"], "SABIT")
        ekle(p_["ad"], cq.Workplane(obj=sh_), {"celik": "celik", "ptfe_bant": "ptfe_bant"}.get(p_["mal"], p_["mal"]), YB_, grup=g_,
             kaynak="bantli_tabla_cad_v1 bölüm 5", bom=p_["bom"])
    MX, MY, MZF = GB_MOTOR
    if nema23 is not None:
        ekle("yb_motoru", cq.Workplane(obj=nema23.translate(cq.Vector(MX, MY, MZF))), "motor", YB_, kaynak="STP-MTR-23079 GERÇEK CAD",
             bom=("Yükleme bandı motoru · NEMA23 STP-MTR-23079", 1, "1,95 N·m kapalı çevrim · teknik bölmede", "GT2 1:1 · aktarmada kaset bandıyla eş hız, sonra fırın bandı hızı"))
    ekle("yb_motor_plakasi", kut(MX - 31.0, XT_ + 12.0, YT_ - 17.5, MY + 32.0, MZF, MZF + 3.0).cut(silz(MX, MY, 20.0, MZF - 1, MZF + 4)).cut(silz(XT_, YT_, 5.5, MZF - 1, MZF + 4)),
         "sac", YB_, bom=("Yükleme bandı motor plakası 3 mm", 1, "304 lazer", "teknik bölme duvarına 2 takozla (arka yüz)"))
    for i_, xa_ in enumerate((MX - 31.0, MX + 21.0)):
        ekle("yb_motor_takozu_%d" % i_, kut(xa_, xa_ + 10.0, YT_ - 17.0, YT_ - 7.0, MZF + 3.0, TUNEL_Z_D[0] - 5.5), "sac", YB_,
             bom=("Motor plakası takozu 10 × 10", 2, "304", "plaka → teknik bölme duvarı (M5)") if i_ == 0 else None)
    ekle("yb_kasnak_rulo", silz(XT_, YT_, 7.5, MZF + 3.0, MZF + 11.0).cut(silz(XT_, YT_, 5.0, MZF + 2.0, MZF + 12.0)), "aluminyum", YB_, grup="RULO_GB_TAHRIK",
         bom=("GT2 kasnak 24 diş Ø15", 2, "alüminyum · sıkma bilezikli", "tahrik rulosu mili + motor mili"))
    ekle("yb_kasnak_motor", silz(MX, MY, 7.5, MZF + 3.0, MZF + 11.0), "aluminyum", YB_)
    L_ = math.hypot(MX - XT_, MY - YT_); a_ = math.degrees(math.atan2(MY - YT_, MX - XT_))
    kay = cq.Workplane("XY", origin=((XT_ + MX) / 2.0, (YT_ + MY) / 2.0, MZF + 3.0)).slot2D(L_ + 17.0, 17.0, a_).extrude(8.0)
    kay = kay.cut(cq.Workplane("XY", origin=((XT_ + MX) / 2.0, (YT_ + MY) / 2.0, MZF + 2.0)).slot2D(L_ + 15.0, 15.0, a_).extrude(10.0))
    ekle("yb_gt2_kayis", kay, "koyu", YB_, bom=("GT2 kayış 6 mm kapalı", 1, "kauçuk", "1:1 · teknik bölmede"))
    # ---- 3.2 ÇIKIŞ ÖLÜ PLAKASI: fırın bandı ucu 3996 → K bandı 4020 · L: dikey kanadı kabuğun çıkış sacına kaynaklı (v8: kesiğin altındaki sağlam duvara) ----
    olu = kut(OLU_X[0], OLU_X[1], K_BANT - 1.0, K_BANT + 1.5, ZA, ZB_).union(kut(OLU_X[0], OLU_X[0] + 1.5, GECIT_Y[0], K_BANT - 1.0, ZA, ZB_))   # v8: kanat 944 → 940 (geçit tabanı): kabuğun sağlam çıkış duvarına (x 3998,5, y 940–944) kaynaklı
    ekle("cikis_olu_plakasi", olu, "sac", CP, bom=("Çıkış ölü plakası 2,5 mm · L", 1, "304 · üstü parlatılmış", "üstü %s: fırın bandı %.0f → K bandı %.0f" % (("%.1f" % (K_BANT + 1.5)).replace(".", ","), BANT_UST_HAT, K_BANT)))
    # ---- 3.3 K GİRİŞ ÇİTİ YOK (v5: ürün −170'te düz gelir) ----
    # ---- 3.4 FIRIN ÜSTÜ HAVALI RAF (v3): pizza kutusu yedeği (55) + TOPPING kompresörü bunun üstünde · gövde üstüne 5 mm hava boşluğu ----
    _raf = kut(X_F0 + 10.0, X_F1 - 10.0, UST_RAF_Y[0], UST_RAF_Y[1], -420.0, -15.0)
    for x, z in TAKOZ_XZ:
        _raf = _raf.cut(sily(x, z, 3.3, UST_RAF_Y[0] - 1.0, UST_RAF_Y[1] + 1.0))
    _raf = _raf.cut(kut(KOMP_ACIKLIK[0], KOMP_ACIKLIK[1], UST_RAF_Y[0] - 1.0, UST_RAF_Y[1] + 1.0, KOMP_ACIKLIK[2], KOMP_ACIKLIK[3]))   # v8: kompresör tavası açıklığı
    ekle("ust_raf", _raf, "sac", "F_UST_RAF",
         bom=("Fırın üstü raf 4 mm", 1, "304 · 1480 × 405", "v6: 10 takozla (aralık 360) gövde üstünde, yanları açık (doğal havalandırma) · altında ışınım kalkanı · SOLDA pizza kutusu yedeği 320 kutu 51 kg (0,16 kg/kutu: Bekar Ambalaj 100 adet 16 kg) + SAĞDA kompresör 25 kg = 76 kg · JUN-AIR ortam sınırı 40 °C [föy] · v8: kompresör altında açıklık 395 × 310 (kompresör tavası firin_ust_kabin_cad_v1 alttan flanşla asılır)"))
    _kal = kut(X_F0 + 10.0, X_F1 - 10.0, ISI_KALKANI_Y[0], ISI_KALKANI_Y[1], -420.0, -15.0)
    for x, z in TAKOZ_XZ:
        _kal = _kal.cut(sily(x, z, 3.3, ISI_KALKANI_Y[0] - 1.0, ISI_KALKANI_Y[1] + 1.0))
    ekle("isi_kalkani", _kal, "sac", "F_UST_RAF",
         bom=("Isı kalkanı 0,8 mm", 1, "304 · 1480 × 405 · parlak", "fırın üstünden 10 mm yukarıda, takozlara geçme: fırın üst yüzeyinin ışınımını keser, rafla arasında 29 mm hava"))
    # v6: TAKOZ_XZ modül başında (10 takoz)
    for i, (x, z) in enumerate(TAKOZ_XZ):                                                       # v4: iki parça boru takoz (alt 10 · üst 29,2), M6 saplama deliği
        ekle("ust_raf_takozu_alt_%d" % i, sily(x, z, 8.0, YG1, ISI_KALKANI_Y[0]).cut(sily(x, z, 3.3, YG1 - 1.0, ISI_KALKANI_Y[0] + 1.0)), "paslanmaz", "F_UST_RAF",
             bom=("Raf takozu alt Ø16 × 10", 10, "304 boru 16 × 1,5 → torna", "fırın üst sacındaki M6 saplamaya geçer · kalkanı taşır") if i == 0 else None)
        ekle("ust_raf_takozu_ust_%d" % i, sily(x, z, 8.0, ISI_KALKANI_Y[1], UST_RAF_Y[0]).cut(sily(x, z, 3.3, ISI_KALKANI_Y[1] - 1.0, UST_RAF_Y[0] + 1.0)), "paslanmaz", "F_UST_RAF",
             bom=("Raf takozu üst Ø16 × 28,2", 10, "304 boru 16 × 1,5 → torna", "kalkan ile raf arasında · rafın üstünden M6 somun") if i == 0 else None)
    # ---- 3.5 v8: F ARKA SACI KALKTI → firin_ust_kabin_cad_v1 "f_ust_arka_sac" (tek parça, y 788–1862, rakorlu + panjurlu) ----


BIRIMLER = [
    ("F_TP10_GOVDE", "Fırın gövdesi · TP10 kesiti (730 × 517) · boy 1500 ÖZEL SİPARİŞ · v10: giriş ön odası %.0f + uç duvarları 60 (yükleme bandı geçitten ısıtılan bölgenin başına girer) · ısıtılan %.0f (%d ürün) · IR üst + alt 2 bölge" % (ON_ODA, ODA, N_URUN) + " · ekran + teknik bölme arkada · ≈14 kW (VARSAYIM) · v5: 79 mm ÖNE — ön yüzü = ÖN DÜZLEM +79 (v8: bütün istasyon önleri buraya gelir), F modülü 909 derin · v7 ALÇAK HAT: gövde %.0f–%.0f" % (YG0, YG1)),
    ("F_TP10_KONVEYOR", "Fırın konveyörü · tel örgü bant 381 × 1428 uçtan uca · üstü %.0f · rulolar uç duvarlarının içinde (boş bant yok) · tahrik + gergi teknik bölmede" % BANT_UST_HAT),
    ("F_YUKLEME_BANDI", "Yükleme bandı (bizim · v10) · ön odadan ısıtılan bölgenin başına (2624–2845 ısıda) · kasetten hızlı alır, sonra fırın bandı hızında · paslanmaz ince tel bant (ısıda) · kaset burnu 2518,9 → bant 2522–2845 → fırın bandı 2856 · Ø12 burun + Ø30 tahrik · PTFE 296 · eksen −170 · NEMA23 + GT2 teknik bölmede · ayakları gövde tabanına"),
    ("F_CIKIS_PLAKA", "Çıkış ölü plakası (bizim) · 3997–4018 · fırın bandı → K bandı"),
    ("F_UST_RAF", "Fırın üstü HAVALANDIRMALI raf (bizim) · 4 mm raf %.0f–%.0f, 10 takozlu (Ø16, aralık 360; gövde üstünden 39), altında 0,8 mm ışınım kalkanı (10 mm) · üstünde SOLDA pizza kutusu yedeği 320 + SAĞDA TOPPING kompresörü (ortam sınırı 40 °C)" % UST_RAF_Y),
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
    g = {"asset": {"version": "2.0", "generator": "AUTOKITCH firin_tp10_cad_v8"}, "scene": 0, "scenes": [{"nodes": list(range(len(nodes)))}], "nodes": nodes,
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


def havada_denetimi(ps=None, yaz=True):
    """v8 · denetim_temas_v1 ile havada parça (zemin = gövde altı 788). Beyaz liste YOK."""
    import denetim_temas_v1 as DT
    ps = ps if ps is not None else PARCALAR
    r = DT.havada([(p["ad"], p["wp"]) for p in ps])
    if yaz:
        DT.yaz(r, en_cok=80, baslik="HAVADA PARCA DENETIMI · firin_tp10_cad_v8")
    return r


# v8 · v7 ↔ v8 parça parça karşılaştırma: bilerek değişen / silinen parçalar (başkası değişirse KALDI)
V8_DEGISEN = ("yalitim_tasyunu", "on_yatak_giris", "on_yatak_cikis", "arka_yatak_giris", "arka_yatak_cikis", "tahrik_reduktoru",
              "giris_yan_saci_0", "giris_yan_saci_1", "giris_tasiyici_sac", "cikis_olu_plakasi", "ust_raf")
V8_SILINEN = ("f_arka_saci",)


if __name__ == "__main__":
    import time, json
    import kaset_3d_v3 as K3
    t0 = time.time()
    ARG = sys.argv[1:]
    DEN = []

    def kontrol(ad, sart, deger=""):
        DEN.append((ad, bool(sart), deger)); print("  %-124s %s %s" % (ad, "GEÇTİ" if sart else "** KALDI **", deger))

    ps = kur(uyarla=True)
    gecersiz = [p["ad"] for p in ps if not dunya(p).isValid()]
    print("TP10-UZUN v8 · %d parça (fırın %d + uyarlama %d)" % (len(ps), len([p for p in ps if p["birim"].startswith("F_TP10")]),
          len([p for p in ps if not p["birim"].startswith("F_TP10")])))
    print("DENETİM (firin_tp10_cad_v8)")
    kontrol("katılar geçerli (%d parça)" % len(ps), not gecersiz, ", ".join(gecersiz))
    cak = kendi_arasinda(ps)
    for x_ in cak[:30]: print("   %10.1f mm3  %s  <->  %s" % x_)
    kontrol("FIRIN ÇAKIŞMA: kendi arasında gerçek katı kesişimi > 1 mm³ = 0 (TEMİZ)", not cak, "%d bulgu" % len(cak))
    bb = cq.Compound.makeCompound([dunya(p) for p in ps if p["birim"].startswith("F_TP10")]).BoundingBox()
    print("ZARF (fırın): x %.0f…%.0f (%.0f) · y %.0f…%.0f · z %.0f…%.0f" % (bb.xmin, bb.xmax, bb.xlen, bb.ymin, bb.ymax, bb.zmin, bb.zmax))
    print("YERLEŞİM: gövde %.0f–%.0f · ön oda %.0f–%.0f · giriş duvarı %.0f–%.0f · ISITILAN %.0f–%.0f = %.0f · çıkış duvarı %.0f–%.0f · bant uçtan uca %.0f–%.0f · rulolar %.0f / %.0f · aynı anda %d ürün (adım %.0f) · güç ≈%.1f kW (VARSAYIM)"
          % (X_F0, X_F1, X_F0, X_DUV0, X_DUV0, X_TUN0, X_TUN0, X_TUN1, ODA, X_TUN1, X_F1, BANT_X[0], BANT_X[1], RULO_X[0], RULO_X[1], N_URUN, ADIM, GUC))

    def _bbk(birim=None, ad=None):
        _s = [dunya(p) for p in ps if (birim is None or p["birim"] == birim) and (ad is None or p["ad"] == ad)]
        assert _s, (birim, ad)
        return cq.Compound.makeCompound(_s).BoundingBox()
    # ---- KOT (v7 ile aynı hedefler · f_arka_saci satırı kalktı) ----
    for _a, _v, _h in [("fırın gövdesi altı (F_TP10_GOVDE ymin)", _bbk("F_TP10_GOVDE").ymin, 788.0),
                       ("fırın gövdesi üstü (F_TP10_GOVDE ymax)", _bbk("F_TP10_GOVDE").ymax, 1305.0),
                       ("fırın bandı üstü (bant_ust_00 ymax)", _bbk(ad="bant_ust_00").ymax, 998.0),
                       ("giriş bandı üstü (giris_bandi ymax = fırın bandı)", _bbk(ad="giris_bandi").ymax, 998.0),
                       ("çıkış ölü plakası üstü (K bandı 996 + 1,5)", _bbk(ad="cikis_olu_plakasi").ymax, 997.5),
                       ("ışınım kalkanı altı (gövde üstü + 10)", _bbk(ad="isi_kalkani").ymin, 1315.0),
                       ("raf üstü (ust_raf ymax)", _bbk(ad="ust_raf").ymax, 1348.0),
                       ("F_UST_RAF birimi üstü", _bbk("F_UST_RAF").ymax, 1348.0)]:
        kontrol("KOT %-52s %8.2f · hedef %7.1f" % (_a, _v, _h), abs(_v - _h) < 0.01)
    _tb = (DISK_UST - 11.0, DISK_UST)
    _yk_ok = YARIK_V2[1][2] < _tb[0] and YARIK_V2[1][3] > _tb[1] and DISK_UST - 16.0 < _tb[0] and DISK_UST + 42.0 > _tb[1]
    kontrol("YARIK / AĞIZ: yarık açıklığı %.0f–%.0f · kabuk giriş ağzı %.0f–%.0f · tabla + disk %.0f–%.0f içinden geçer"
            % (YARIK_V2[1][2], YARIK_V2[1][3], DISK_UST - 16.0, DISK_UST + 42.0, _tb[0], _tb[1]), _yk_ok)
    _mb = _bbk(ad="giris_bandi_motoru")
    kontrol("GİRİŞ BANDI MOTORU y %.1f–%.1f · gövde %.0f–%.0f içinde" % (_mb.ymin, _mb.ymax, YG0, YG1), YG0 < _mb.ymin and _mb.ymax < YG1)
    # ---- v8 · ÖN DÜZLEM ----
    _kb = _bbk(ad="govde_kabugu")
    kontrol("ÖN DÜZLEM: Z_ON = ZS = %.1f · gövde kabuğu ön yüzü zmax %.2f = Z_ON · x %.1f–%.1f · y %.1f–%.1f (1500 × 517 düz yüz)" % (Z_ON, _kb.zmax, _kb.xmin, _kb.xmax, _kb.ymin, _kb.ymax),
            abs(Z_ON - 79.0) < 1e-9 and abs(_kb.zmax - Z_ON) < 0.01 and abs(_kb.xmin - X_F0) < 0.01 and abs(_kb.xmax - X_F1) < 0.01)
    _zmax = max(dunya(p).BoundingBox().zmax for p in ps); _zmin = min(dunya(p).BoundingBox().zmin for p in ps)
    kontrol("ÖN DÜZLEM: hiçbir fırın parçası +79'u geçmez (en ön %.2f) · arka ≥ −830 (en arka %.2f)" % (_zmax, _zmin), _zmax <= Z_ON + 0.01 and _zmin >= -830.0 - 0.01)
    kontrol("f_arka_saci / F_ARKA_SAC YOK (yerine firin_ust_kabin_cad_v1 f_ust_arka_sac)", not [p for p in ps if p["ad"] == "f_arka_saci" or p["birim"] == "F_ARKA_SAC"]
            and "F_ARKA_SAC" not in [k for k, _a in BIRIMLER])
    kontrol("BIRIMLER ↔ parçalar: her birimin parçası var, parçasız birim yok", all(any(p["birim"] == k for p in ps) for k, _a in BIRIMLER)
            and all(p["birim"] in [k for k, _a in BIRIMLER] for p in ps))
    # ---- v8 · v7 ↔ v8 PARÇA PARÇA ----
    import firin_tp10_cad_v7 as F7
    F7.kur(uyarla=True)
    A7 = {p["ad"]: F7.dunya(p) for p in F7.PARCALAR}; A8 = {p["ad"]: dunya(p) for p in ps}
    _deg = []
    for ad in sorted(set(A7) & set(A8)):
        b7, b8 = A7[ad].BoundingBox(), A8[ad].BoundingBox()
        fark = max(abs(a_ - b_) for a_, b_ in zip((b7.xmin, b7.xmax, b7.ymin, b7.ymax, b7.zmin, b7.zmax), (b8.xmin, b8.xmax, b8.ymin, b8.ymax, b8.zmin, b8.zmax)))
        if fark > 0.005 or abs(A7[ad].Volume() - A8[ad].Volume()) > 0.05:
            _deg.append(ad)
    _sil = sorted(set(A7) - set(A8)); _yeni = sorted(set(A8) - set(A7))
    print("   v7 → v8: ortak %d · DEĞİŞEN %d %s · SİLİNEN %s · YENİ %d %s" % (len(set(A7) & set(A8)), len(_deg), _deg, _sil, len(_yeni), _yeni))
    kontrol("v7 ↔ v8: değişen parçalar YALNIZ bilerek değişenler (%d) · gövde kabuğu, bant, giriş bandı, rulolar, raf, arka yüz BİREBİR" % len(V8_DEGISEN),
            sorted(_deg) == sorted(V8_DEGISEN), str(sorted(set(_deg) ^ set(V8_DEGISEN))))
    kontrol("v7 ↔ v8: silinen yalnız %s" % (V8_SILINEN,), _sil == sorted(V8_SILINEN), str(_sil))
    _uy = [a_ for a_ in ("govde_kabugu", "tunel_kaplamasi", "teknik_bolme_duvari", "giris_bandi", "bant_alt_kol", "rulo_giris", "rulo_cikis", "rulo_mili_giris",
                         "rulo_mili_cikis", "isi_kalkani", "on_ray", "arka_ray", "giris_bandi_motoru") if a_ in _deg]
    kontrol("FIRIN GÖVDESİ + ÜRÜN YOLU DEĞİŞMEDİ (kabuk, kaplama, bant, rulolar, giriş bandı, kalkan, raylar)", not _uy, str(_uy))
    # ---- denetçi #4 · raf: yalnız kompresör açıklığı ----
    _acik = (min(KOMP_ACIKLIK[1], X_F1 - 10.0) - KOMP_ACIKLIK[0]) * (UST_RAF_Y[1] - UST_RAF_Y[0]) * (KOMP_ACIKLIK[3] - KOMP_ACIKLIK[2])
    _pz = kut(2520.0, 3324.0, UST_RAF_Y[0] - 1.0, UST_RAF_Y[1] + 1.0, -424.0, -20.0).val()
    _p7, _p8 = A7["ust_raf"].intersect(_pz).Volume(), A8["ust_raf"].intersect(_pz).Volume()
    _b8 = A8["ust_raf"].BoundingBox()
    kontrol("RAF (denetçi #4): v7 − v8 hacim %.0f = açıklık %.0f mm³ (x %.0f–%.0f · z %.0f…%.0f) · pizza bölgesi v7 %.0f = v8 %.0f · üst %.2f · takozlar açıklığın dışında"
            % (A7["ust_raf"].Volume() - A8["ust_raf"].Volume(), _acik, KOMP_ACIKLIK[0], KOMP_ACIKLIK[1], KOMP_ACIKLIK[2], KOMP_ACIKLIK[3], _p7, _p8, _b8.ymax),
            abs(A7["ust_raf"].Volume() - A8["ust_raf"].Volume() - _acik) < 1.0 and abs(_p7 - _p8) < 0.5 and abs(_b8.ymax - 1348.0) < 0.01
            and all(not (KOMP_ACIKLIK[0] - 8.0 < x_ < KOMP_ACIKLIK[1] + 8.0 and KOMP_ACIKLIK[2] - 8.0 < z_ < KOMP_ACIKLIK[3] + 8.0) for x_, z_ in TAKOZ_XZ))
    # ---- denetçi #6 · kızak ↔ rulo ----
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape as _DSS
    _kr = min(_DSS(A8[k_].wrapped, A8[r_].wrapped).Value() for k_ in ("bant_kizagi_on", "bant_kizagi_arka") for r_ in ("rulo_giris", "rulo_cikis", "bant_sarimi_giris", "bant_sarimi_cikis"))
    _kb = A8["bant_kizagi_on"].BoundingBox()
    kontrol("KIZAK (denetçi #6): uçlar x %.0f / %.0f = RULO_X ± 20 · kızak ↔ rulo / sarım en yakın %.1f mm ≥ 4 (400 °C uzama payı)" % (_kb.xmin, _kb.xmax, _kr),
            _kr >= 4.0 and abs(_kb.xmin - RULO_X[0] - 20.0) < 0.01 and abs(_kb.xmax - RULO_X[1] + 20.0) < 0.01)
    # ---- v8 · HAVADA PARÇA ----
    hv = havada_denetimi(ps)
    kontrol("HAVADA PARÇA = 0 (v7: 67 bileşen / 77 parça) · beyaz liste YOK", not hv["bilesen"], "%d bileşen" % len(hv["bilesen"]))
    # ---- denetçi #5 · yatak gövdeleri yapıya bağlı mı (miller + taşyünü HARİÇ: zincir mil üzerinden kurulamasın) ----
    import denetim_temas_v1 as DT
    _hv2 = DT.havada([(p["ad"], p["wp"]) for p in ps if p["mal"] != "yalitim" and not p["ad"].startswith("rulo_mili_")])
    _tas = ("on_yatak_giris", "on_yatak_cikis", "arka_yatak_giris", "arka_yatak_cikis", "tahrik_reduktoru", "tahrik_motoru",
            "on_yatak_konsolu_giris", "on_yatak_konsolu_cikis", "arka_yatak_konsolu_cikis", "tahrik_konsolu")
    _yh = sorted(set(a_ for d_ in _hv2["bilesen"] for a_ in d_["uye"] if a_ in _tas))
    kontrol("YATAKLAR YAPIYA BAĞLI (denetçi #5): miller + taşyünü hariç tutulunca yatak / redüktör / motor / konsollar zemine bağlı · havadaki (mile asılı rulo, bant) %d bileşen"
            % len(_hv2["bilesen"]), not _yh, str(_yh))
    # ---- RAF YÜK HESABI (v6, değişmedi) ----
    _E, _nu, _ro, _g = 193e9, 0.29, 7930.0, 9.81
    _qk = 320 * 0.16 * _g / (0.804 * 0.404)
    for _t, _a, _ad in ((0.004, 0.378, "v6 4 mm · 10 takoz (açıklık 360 × 378)"),):
        _q = _qk + _ro * _g * _t; _D = _E * _t ** 3 / (12.0 * (1.0 - _nu ** 2)); _w = 0.00581 * _q * _a ** 4 / _D * 1000.0
        print("RAF SEHİM %s: yük %.0f Pa → iç panel %.2f mm · kenar ≈%.1f mm" % (_ad, _q, _w, 3.0 * _w))
    _top = 320 * 0.16 + 25.0 + 1.480 * 0.405 * 0.004 * _ro + 1.480 * 0.405 * 0.0008 * _ro
    print("RAF YÜKÜ: kutu 51,2 + kompresör 25 + raf %.1f + kalkan %.1f = %.0f kg → 10 takoz ort. %.1f kg" % (1.480 * 0.405 * 0.004 * _ro, 1.480 * 0.405 * 0.0008 * _ro, _top, _top / 10.0))
    for x in (2400, 2600, 3300, 3990, 4030, 4300):
        print("   ürün merkezi x %4d → z %.1f" % (x, urun_z(x)))
    if "glb" in ARG:                                                                 # v8: yalnız istenirse (site klasörüne varsayılan yazım YOK)
        ton = {}
        for p in ps:
            if not p["birim"].startswith("F_TP10"): continue
            ton.setdefault((p["mal"], p["birim"]), Mesh()).ekle(ag(cq.Workplane(obj=dunya(p).translate(cq.Vector(-XC_TP, -YG0, -ZS)))))
        parca = [("TP10U__%s__%s" % (b, m), msh, m) for (m, b), msh in sorted(ton.items())]
        for _a, msh, _m in parca:
            msh.P = [(-q[0], q[1], -q[2] - D_TP * MM) for q in msh.P]; msh.N = [(-n[0], n[1], -n[2]) for n in msh.N]
        yol = os.path.join(KOK, "otonom", "hat3d", "firin_tp10_v8.glb")
        b1 = glb_yaz(yol, parca)
        print("firin_tp10_v8.glb %.0f KB" % (b1 / 1024.0))
    kal = [d_ for d_ in DEN if not d_[1]]
    print("DENETIM (firin_tp10_cad_v8): %d madde · %d KALDI · %.0f sn" % (len(DEN), len(kal), time.time() - t0))
    assert not kal, [d_[0] for d_ in kal]
    sys.stdout.flush(); os._exit(0)
