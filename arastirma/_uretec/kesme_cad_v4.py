# -*- coding: utf-8 -*-
"""AUTOKITCH · K · KESME + TEREYAĞI SPREYİ İSTASYONU — ÜRETİM MODELİ v4 (27 Eyl 2026): ALÇAK HAT (SPEC_alcak_hat_v57) — y 700–868 dilimi çıkarıldı,
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
import kutu_cad_v5 as KC                                   # v4: ALÇAK HAT E'si (v3 yanlışlıkla kutu_cad_v3'ü alıyordu) · ortak geometri yardımcıları + E'nin kendisi (arayüz ve tarama)
import bulasik_cad_v1 as BM                                # v4: K altındaki bulaşık makinesi (ayrı modül; burada yalnız REF + yer denetimi)
import topping_cad_v22 as TC
from kaset_3d_v3 import Mesh, MM, MALZEME

for _k, _v in {"pu_bant": ((0.95, 0.95, 0.93, 1.0), 0.0, 0.55), "pc": ((0.80, 0.88, 0.95, 0.18), 0.0, 0.05),
               "tereyag": ((0.98, 0.86, 0.42, 1.0), 0.0, 0.5), "hortum_isi": ((0.85, 0.20, 0.15, 1.0), 0.0, 0.6),
               "hava": ((0.15, 0.40, 0.85, 1.0), 0.0, 0.5), "kasar_ust": ((0.96, 0.85, 0.50, 1.0), 0.0, 0.8),
               "kesik": ((0.35, 0.22, 0.12, 1.0), 0.0, 0.9), "kirmizi": ((0.80, 0.12, 0.10, 1.0), 0.1, 0.5), "siyah": ((0.07, 0.07, 0.08, 1.0), 0.1, 0.6)}.items():
    MALZEME.setdefault(_k, dict(renk=_v[0], met=_v[1], ruf=_v[2], saydam=_v[0][3] < 1.0))
MALZEME.setdefault("sprey", dict(renk=(0.98, 0.88, 0.45, 0.30), met=0.0, ruf=0.6, saydam=True))
MALZEME.setdefault("pom", dict(renk=(0.95, 0.95, 0.93, 1.0), met=0.0, ruf=0.42))
for _k, _v in {"kanister": (0.93, 0.94, 0.96, 1.0), "mavi_kapak": (0.15, 0.40, 0.85, 1.0), "dozaj": (0.90, 0.86, 0.62, 1.0)}.items():   # v4: bidon · parlatıcı kapağı · dozaj hortumu
    MALZEME.setdefault(_k, dict(renk=_v, met=0.0, ruf=0.6))

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
E_PENCERE = (BANT - 18.0, BANT + 66.0, -372.0, -24.0)   # E sol duvarındaki pizza penceresi y0 y1 z0 z1 = 978–1062 [K: kutu_cad_v5.PENCERE] · v3'te 1146–1230 sabitti
URUN_GIRISI = (BANT - 64.0, BANT + 76.0, -420.0, -8.0)  # v4: sol duvardaki fırın bandı / ürün girişi y0 y1 z0 z1 = 932–1072 (v3 1100–1240 sabitti) — montajdaki _ka

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
    ekle("taban_sac_3", kut(SAC, W - SAC, Y_PLINT, Y_PLINT + 3.0, -D + SAC, -SAC), "sac")
    ekle("plint_on", kut(30.0, W - 30.0, 10.0, Y_PLINT, -61.5, -60.0), "sac")
    ekle("istasyon_tabani_3", kut(SAC, W - SAC, H_B, H_B + 3.0, -D + SAC, -SAC).cut(kut(200.0, 260.0, H_B - 1, H_B + 4, -800.0, -760.0)), "sac")
    ekle("arka_sac", kut(0, W, Y_PLINT, H, -D, -D + SAC), "kabuk")
    ekle("ust_sac", kut(0, W, H - SAC, H, -D + SAC, 0), "kabuk")
    # sol yan: fırın bandı + ürün girişi (fırın bandı K'ya 15 mm girer)
    ekle("sol_sac_urun_girisi", kut(0, SAC, Y_PLINT, H - SAC, -D + SAC, 0).cut(kut(-1, SAC + 1, URUN_GIRISI[0], URUN_GIRISI[1], URUN_GIRISI[2], URUN_GIRISI[3])), "kabuk")
    ekle("sag_sac_E_penceresi", kut(W - SAC, W, Y_PLINT, H - SAC, -D + SAC, 0).cut(kut(W - SAC - 1, W + 1, E_PENCERE[0], E_PENCERE[1], E_PENCERE[2], E_PENCERE[3])), "kabuk")
    # köşe dikmeleri 30 × 30 × 2 (sol ön dikme ürün girişinde kesik)
    for i, (x0, z0) in enumerate(((SAC, -31.5), (W - SAC - 30.0, -31.5), (SAC, -D + SAC), (W - SAC - 30.0, -D + SAC))):
        dik = kut(x0, x0 + 30.0, Y_PLINT + 3.0, H - SAC, z0, z0 + 30.0).cut(kut(x0 + 2, x0 + 28, Y_PLINT + 2, H, z0 + 2, z0 + 28))
        if i == 0:
            dik = dik.cut(kut(x0 - 1, x0 + 31, BANT - 69.0, BANT + 81.0, z0 - 1, z0 + 31))
        if i == 1:
            dik = dik.cut(kut(x0 - 1, x0 + 31, BANT - 69.0, BANT + 81.0, z0 - 1, z0 + 31))          # bant + E penceresi (sol ön dikme gibi)
        ekle("kose_dikmesi_%d" % i, dik, "sac", bom=("Kare profil 30 × 30 × 2 AISI 304", 4, "boy %.1f (v4)" % (H - SAC - Y_PLINT - 3.0), "lazer + kaynak") if i == 0 else None)
    # v2: ÖN KAPAK YOK (Kemal 27 Eyl) — taban kapısı, PC pencereli üst kapı, kulplar, AZM kilit, acil stop kaldırıldı


# ---------------------------------------------------------------- 2 · K BANDI ----------------------------------------------------------------
def bant():
    z0, z1 = BANT_Z
    for i, (a, b) in enumerate(((z0 - 5.0, z0 - 2.0), (z1 + 2.0, z1 + 5.0))):
        ekle("bant_yan_levhasi_%d" % i, kut(10.0, 590.0, BANT - 64.0, BANT - BANT_K - 0.5, a, b), "sac",
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
    ekle("tahrik_rulosu_RollerDrive_EC5000", silz(X_TAHRIK, Y_TAHRIK, R_TAHRIK, z0 - 2.0, z1 + 2.0), "aluminyum", "SABIT",
         ("Interroll RollerDrive EC5000 AI 24 V Ø50 (motor rulonun içinde, IP66)", 1, "boy 404 · kaplamalı", "interroll.com EC5000 [V: kaplama + IP teyidi]"))
    ekle("tahrik_rulosu_mili", silz(X_TAHRIK, Y_TAHRIK, 6.0, z0 - 5.0, z1 + 5.0), "celik")
    ekle("kuyruk_rulosu", silz(X_KUYRUK, Y_KUYRUK, R_KUYRUK, z0 + 2.0, z1 - 2.0), "aluminyum",
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
    ekle("bant_PU_2mm", ust.union(alt).union(sarim_t).union(sarim_k), "pu_bant",
         bom=("Gıda PU bant 2 mm homojen, beyaz (FDA / EU 10-2011), sonsuz birleştirilmiş", 1, "400 × ≈1150", "[V] Ammeraal / Habasit sınıfı · kesim yüzeyi"))
    # bant sonu ölü plakası + çit
    ekle("olu_plaka", kut(587.0, 597.0, BANT - 6.0, BANT, -380.0, -30.0), "sac")
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
        ekle("kopru_kirisi_%d" % i, kut(SAC + 1.0, W - SAC - 1.0, Y_KIRIS[0], Y_KIRIS[1], za, zb).cut(kut(SAC, W - SAC, Y_KIRIS[0] + 2, Y_KIRIS[1] - 2, za + 2, zb - 2)), "sac",
             bom=("Kare profil 40 × 40 × 2 AISI 304 (köprü)", 2, "boy 595", "üretim") if i == 0 else None)
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
    ekle("bicak_gobek_halkasi", sily(XC, ZC, 20.0, Y_GOBEK - 12.0, Y_GOBEK).cut(sily(XC, ZC, 13.0, Y_GOBEK - 13.0, Y_GOBEK + 1.0)), "celik", "KESICI")
    for i in range(6):
        phi = 60.0 * i
        ekle("bicak_%d" % i, radyal(BICAK_R0, BICAK_R1, BICAK_T, Y_AGIZ_UST, Y_GOBEK, phi), "celik", "KESICI",
             bom=("Yıldız bıçak seti 6 dilim Ø296 (sertleştirilmiş paslanmaz, bulaşık makinesinde yıkanır)", 1, "6 × 133 × 45 × 1,5 · göbek Ø40",
                  "Q-T-S PC1018 / PC5000 bıçak seti sınıfı (q-t-s.com) [V: ölçü bize göre]") if i == 0 else None)
    for i in range(6):
        phi = 30.0 + 60.0 * i
        ekle("koruma_braketi_%d" % i, radyal(110.0, KORUMA_R[1], 12.0, Y_KAFA[0], Y_KAFA[1], phi), "sac", "KESICI")
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
    ekle("PulsaJet_isitici_ceket", silx(yp, ZC, 22.0, 330.0, 395.0).cut(silx(yp, ZC, 19.2, 329.0, 396.0)), "hortum_isi", "KESICI",
         bom=("Silikon ısıtıcı ceket 24 V 20 W + termostat (nozülde tereyağı donmasın)", 1, "45 °C", "[V]"))
    ekle("sprey_dirsegi", kut(292.0, 306.0, Y_KAFA[1], yp + 8.0, ZC - 7.0, ZC + 7.0), "celik", "KESICI")
    ekle("UniJet_nozul_govdesi_TG", sily(XC, ZC, 10.0, Y_UC, Y_KAFA[1]), "celik", "KESICI",
         ("Nozül gövdesi UniJet + TG tam koni uç 90° (çek valfli: damlatmaz)", 1, "yıldızın göbeğinde, pideden 150 mm",
          "portal.spray.com TG · uç uyumu Spraying Systems'e teyit [V]"))
    ekle("sprey_ucu_TG", sily(XC, ZC, 7.0, Y_UC - 6.0, Y_UC), "pom", "KESICI")
    ekle("isitmali_hortum_kafa", boru([(405.0, yp, ZC), (440.0, yp, ZC), (440.0, Y_ON_PL[1] + 35.0, ZC)], 5.0), "hortum_isi", "KESICI")
    # sprey konisi (görsel: yalnız sprey anında)
    ekle("sprey_konisi", cq.Workplane(obj=cq.Solid.makeCone(145.0, 3.0, Y_UC - 6.0 - (BANT + PZ_H), cq.Vector(XC, BANT + PZ_H, ZC), cq.Vector(0, 1, 0))), "sprey", "SPREY")


# ---------------------------------------------------------------- 4 · TEREYAĞI SİSTEMİ (taban dolabı arkası) ----------------------------------------------------------------
TANK = dict(x=140.0, z=-540.0, r=80.0, y0=Y_KIRIS[1] + 12.5, y1=Y_KIRIS[1] + 292.5)   # v3: köprü kirişinin arkası · v4: Y_KIRIS'e bağlandı → 1472–1752


def sprey_sistemi():
    x, z, r, y0, y1 = TANK["x"], TANK["z"], TANK["r"], TANK["y0"], TANK["y1"]
    ekle("yag_tanki_3L", sily(x, z, r, y0, y1).cut(sily(x, z, r - 1.5, y0 + 2, y1 - 2)), "sac",
         bom=("Isıtmalı basınçlı tereyağı tankı 3 L AISI 316 (ceketli, kapaklı, seviye sensörlü)", 1, "Ø160 × 280 · 1,5 bar hava · 45 °C",
              "[V] Spraying Systems basınçlı tank sınıfı · 2 gün = 1,41 L (hesap)"))
    ekle("yag_tanki_isitici_ceketi", sily(x, z, r + 6.0, y0 + 30.0, y1 - 30.0).cut(sily(x, z, r + 0.2, y0, y1)), "hortum_isi",
         bom=("Tank ısıtıcı ceketi 100 W + PT100", 1, "45 °C (32–35 °C'de tamamen sıvı; aşırı ısıda yağ ayrışır)", "[V] · vaka E4058 uyarısı"))
    ekle("yag_tanki_kapagi", sily(x, z, r + 8.0, y1, y1 + 14.0), "sac")
    ekle("yag_tanki_kelepcesi", sily(x, z, r + 10.0, y1 - 6.0, y1 + 4.0).cut(sily(x, z, r + 1.0, y1 - 7.0, y1 + 5.0)), "celik")
    ekle("yag_regulatoru_manometre", sily(x + 45.0, z, 14.0, y1 + 14.0, y1 + 60.0), "aluminyum",
         bom=("Hava regülatörü + manometre 0–4 bar (tank basıncı)", 1, "", "[V] Festo MS2-LR sınıfı"))
    ekle("yag_seviye_sensoru", sily(x - 45.0, z, 8.0, y1 + 14.0, y1 + 44.0), "sensor",
         bom=("Seviye sensörü (kapasitif, gıda)", 1, "2 gün kala uyarır", "[V]"))
    ekle("yag_tanki_rafi", kut(34.0, 290.0, y0 - 5.0, y0, -760.0, -380.0), "sac", bom=("Tank rafı 304 · 5 mm", 1, "256 × 380", "v3: sol duvara köşebentle · hava besleme hortumunun (z −800) önünde biter"))
    ekle("yag_tanki_rafi_koseben", kut(2.0, 34.0, y0 - 35.0, y0 - 5.0, -760.0, -380.0).cut(kut(5.0, 35.0, y0 - 36.0, y0 - 8.0, -761.0, -379.0)), "sac",
         bom=("Köşebent 30 × 30 × 3 AISI 304 (tank rafı)", 1, "boy 380", "sol duvara M6 × 3"))
    # ısıtmalı hortum: tank → istasyon tabanı → arka duvar → köprü üstü → kafa (hareketli kısım kafada)
    ekle("isitmali_hortum_Ø6", boru([(x, y1 + 14.0, z), (x, 1792.0, z), (x, 1792.0, -500.0), (440.0, 1792.0, -500.0),
                                      (440.0, Y_KIRIS[1] + 20.0, -500.0), (440.0, Y_KIRIS[1] + 20.0, ZC), (440.0, Y_ON_PL[1] + 35.0 + STROK * 0.0 + 1.0, ZC)], 5.0), "hortum_isi",
         bom=("Isıtmalı gıda hortumu Ø6 iç · 24 V · 45 °C", 1, "≈ 2,6 m · kafaya yaylı sarımla", "[V]"))
    ekle("hava_hortumu_tank", boru([(x + 45.0, y1 + 60.0, z), (x + 45.0, 1827.0, z), (x + 45.0, 1827.0, -760.0), (x + 45.0, 1617.0, -760.0)], 3.0), "hava")


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
        ekle("eksen_ayagi_%d" % i, kut(x - 15.0, x + 15.0, H_B + 3.0, Y_EKSEN[0], Z_EKSEN[0] + 5.0, Z_EKSEN[1] - 5.0), "sac")
    kc(KC.e2e, "itici_home_sensoru", xa + 60.0, Y_EKSEN[1] + 10.0, Z_EKSEN[0] - 20.0, "x")
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
    for i, y in enumerate((1512.0, 1692.0)):                                           # v3: pano yukarıda (+980) · v4: − 168
        ekle("din_rayi_%d" % i, kut(305.0, 560.0, y, y + 35.0, -822.0, -815.0), "celik", bom=("DIN ray 35 × 7,5", 2, "boy 255", "EN 60715") if i == 0 else None)
    ekle("plc_S7-1200_1214C", kut(315.0, 425.0, 1479.5, 1579.5, zd, zd + 75.0), "siemens",
         bom=("PLC Siemens S7-1200 CPU 1214C DC/DC/DC", 1, "6ES7214-1AG40-0XB0 · bant, kesici, itici, sprey", "110 × 100 × 75"))
    ekle("plc_SM1222_DQ16", kut(429.0, 474.0, 1479.5, 1579.5, zd, zd + 75.0), "siemens", bom=("Siemens SM1222 DQ16", 1, "6ES7222-1BH32-0XB0", "45 × 100 × 75"))
    ekle("emniyet_rolesi_PNOZ", kut(478.0, 500.0, 1479.5, 1579.5, zd, zd + 90.0), "sari", bom=("Emniyet rölesi Pilz PNOZ s3", 1, "kapı kilidi + acil stop", "[V] pilz.com"))
    ekle("PWMD_sprey_suruculu", kut(504.0, 530.0, 1479.5, 1579.5, zd, zd + 60.0), "siyah",
         bom=("PulsaJet PWM sürücüsü (tek nozül)", 1, "PLC'den tetik · doz = süre × debi", "[V] Spraying Systems PWMD"))
    ekle("sicaklik_kontrol_2", kut(533.0, 560.0, 1479.5, 1579.5, zd, zd + 70.0), "siyah", bom=("Sıcaklık kontrolcüsü DIN (tank + hortum + nozül)", 2, "PT100 · 45 °C", "[V]"))
    ekle("guc_24V_NDR-240-24", TC.din_parca(TC.GUC_STEP, 315.0, 1662.0, zd + 122.8), "aluminyum",
         bom=("Güç kaynağı Mean Well NDR-240-24", 1, "24 V 10 A · PLC, RollerDrive, sensör, ısıtıcılar", "TraceParts STEP"))
    ekle("surucu_STP-DRV-4830", TC.din_parca(TC.SURUCU_STEP, 450.0, 1692.0, zd + 28.0), "kart",
         bom=("Step sürücü AutomationDirect SureStep STP-DRV-4830", 1, "itici ekseni", "automationdirect.com · TraceParts STEP"))
    ekle("guc_48V_NDR-240-48", TC.din_parca(TC.GUC_STEP, 382.0, 1662.0, zd + 122.8), "aluminyum", bom=("Güç kaynağı Mean Well NDR-240-48", 1, "48 V · step sürücü", "NDR-240 gövdesi"))
    ekle("klemens_sirasi", kut(508.0, 560.0, 1692.0, 1737.0, zd, zd + 45.0), "plastik", bom=("Klemens sırası Phoenix UT 2,5", 24, "", "phoenixcontact.com"))
    ekle("kablo_kanali_0", kut(305.0, 560.0, 1812.0, 1852.0, -822.0, -797.0), "plastik", bom=("Kablo kanalı 40 × 25", 3, "", "katalog"))
    ekle("kablo_kanali_dikey", kut(566.0, 591.0, H_B + 3.0, 1827.0, -822.0, -797.0), "plastik")
    # üst bölme: hava şartlandırıcı + valf adası (arka duvar)
    ekle("sartlandirici_MS4", kut(60.0, 110.0, 1532.0, 1692.0, -826.0, -780.0), "aluminyum",
         bom=("Şartlandırıcı Festo MS4-LFR (filtre + regülatör + manometre)", 1, "6 bar", "[V] festo.com MS4"))
    ekle("valf_adasi_VUVG_4", kut(130.0, 250.0, 1552.0, 1612.0, -826.0, -770.0), "aluminyum",
         bom=("Valf adası Festo VUVG-L10 · 4 × 5/2 (kesici · itici kaldırma · tank basıncı · yedek)", 1, "24 V", "[V] festo.com VUVG"))
    ekle("hava_besleme_K", boru([(230.0, H_B - 20.0, -790.0), (230.0, H_B + 3.0, -790.0), (230.0, 1332.0, -790.0), (85.0, 1332.0, -800.0), (85.0, 1532.0, -800.0)], 5.0), "hava",
         bom=("PU hava hortumu Ø10 · kompresör hattından T ile", 1, "≈ 1 m", "katalog"))
    ekle("hava_hortumu_kesici", boru([(190.0, 1612.0, -790.0), (190.0, 1832.0, -790.0), (205.0, 1832.0, -790.0), (205.0, 1832.0, ZC + 20.0), (205.0, Y_GOVDE[0] + 30.0, ZC + 20.0), (213.0, Y_GOVDE[0] + 30.0, ZC + 20.0)], 3.0), "hava")
    ekle("hava_hortumu_kaldirma", boru([(160.0, 1552.0, -765.0), (160.0, 1152.0, -765.0), (160.0, 1152.0, -470.0)], 3.0), "hava")
    # sensörler
    for ad_, x_ in (("sensor_urun_merkezde", 445.0), ("sensor_bant_sonu", 520.0)):   # yatık: 31 × 10,8 × 20 · üstü 1009 < itici kolu 1017 (v4)
        ekle(ad_, kut(x_ - 15.5, x_ + 15.5, BANT + 2.0, BANT + 12.8, BANT_Z[0] - 20.0, BANT_Z[0] - 2.0), "sensor",
             bom=("Fotosel Omron E3Z-D62 (dağınık yansımalı)", 2, "ürün merkezde · bant sonu", "omron.com E3Z") if x_ < 500 else None)
    for i, y in enumerate((Y_GOVDE[0] + 10.0, Y_GOVDE[1] - 20.0)):
        ekle("kesici_reed_%d" % i, kut(376.0, 384.0, y, y + 20.0, ZC - 10.0, ZC + 10.0), "sensor",
             bom=("Silindir sensörü Festo SMT-8M (üst / alt)", 2, "", "[V] festo.com") if i == 0 else None)


# ---------------------------------------------------------------- 7 · TABAN ALTI (v4 · ALÇAK HAT): bulaşık yeri + deterjan / parlatıcı ----------------------------------------------------------------
# SPEC_alcak_hat_v57 + QR_TEZGAH_v4 (Kemal onaylı): K altı 126–892 · MEIKO M-iClean US sağ ön köşe dikmesine yaslı (kapağı dikmeye çarpmaz) ·
# solunda önde 77, dikmenin arkasında 107 BOŞ · arkasında tek sıra deterjan + parlatıcı, raf 325–330 · makinenin bağlantıları (y ≤ 310) altta kalır.
X_K_HAT = 4000.0                                   # K modülünün hattaki x'i (yerel x = dünya − 4000)
BULASIK_YER = (4108.5, Y_PLINT + 3.0, -20.0)       # bulasik_cad_v1 (X0, Y0, Z0) dünya kökü = kapak ön yüzü — montaj AYNISINI kullanmalı (ayaklar K'nin alt sacında, 126)
# denetçi düzeltmesi: kök z −12 değil −20 → makinenin TAMAMI (ışıklı kulp 8 + gövde 600 + arka bağlantılar 25 = 633) SPEC / Resim 1 v4 B–B'deki z −12…−645'e oturur
BULASIK_ZARF = dict(x=(BULASIK_YER[0] - X_K_HAT, BULASIK_YER[0] - X_K_HAT + BM.W), y=(BULASIK_YER[1], BULASIK_YER[1] + BM.H),
                    z=(BULASIK_YER[2] - BM.D - 25.0, BULASIK_YER[2] + 8.0))    # K yereli 108,5–568,5 × 126–826 × −645…−12 (SPEC: 633 derin = kulp 8 + gövde 600 + arka bağlantılar 25)
BULASIK_ARKA_PAY = (-670.0, -645.0)                # MEIKO föyü: arkada duvar payı 25 — BOŞ (yalnız makinenin arka bağlantı hortumları geçer, y ≤ 310)
BULASIK_BAGLANTI_UST = 310.0                       # makinenin arka bağlantıları yerden ≤ 165 + 126 + yarıçap 15 → 306 ≤ 310 (föy)
KANISTER = dict(x=190.0, y=285.0, z=125.0, L=5.0, yogunluk=1.3, bos_kg=0.3)   # 5 L bidon 190 × 285 × 125 [VARSAYIM: ölçü; 1,3 kg/L; boş bidon 0,3 kg]
KANISTER_X = (("deterjan", 60.0, 250.0), ("parlatici", 270.0, 460.0))
KANISTER_Y0, KANISTER_Z = 330.0, (-800.0, -675.0)
KANISTER_KAPAK = dict(r=20.0, h=15.0, dx=35.0)     # kapak Ø40 × 15, bidonun hortum tarafındaki kenarından 35 içeride [VARSAYIM]
RAF_Y, RAF_X, RAF_Z = (325.0, 330.0), (40.0, 560.0), (-805.0, -670.0)   # kanister rafı 304 · 5 mm · arka köşe dikmelerinin arası (x 31,5 / 568,5)
KONSOL = dict(yatay=(SAC, 62.0), dikey_h=33.0, t=3.0, z=(-796.0, -672.0))   # raf konsolu L büküm 3 mm: yan saca M6 · arka dikmeden (−798,5) ve arka paydan (−670) 2 mm ayrık
HORTUM = dict(r=3.0, y_ust=640.0, y_giris=280.0, x_inis=(260.0, 480.0), delik_r=7.0)
# dozaj emiş hortumu PVC Ø6/4 [VARSAYIM]: kapaktan yukarı 640 → yana → raftaki Ø14 delikten aşağı 280 → öne, makinenin arka yüzüne.
# MEIKO föyünde dozaj girişinin yeri yok → bağlantı bölgesinde (y ≤ 310), elektrik (x 148,5) / tahliye (294,5) / su (421,5) bağlantılarının arasından [VARSAYIM · MEIKO'ya teyit]


def bulasik_parcalari():
    """bulasik_cad_v1'in katıları montajdaki yerinde (BULASIK_YER), K yerelinde · + kapak açık zarfı (K yereli).
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


def hortum_noktalari(i):
    ad_, xa, xb = KANISTER_X[i]
    zc = (KANISTER_Z[0] + KANISTER_Z[1]) / 2.0
    xk = xb - KANISTER_KAPAK["dx"]; y1 = KANISTER_Y0 + KANISTER["y"]; xi = HORTUM["x_inis"][i]
    return [(xk, y1, zc), (xk, HORTUM["y_ust"], zc), (xi, HORTUM["y_ust"], zc), (xi, HORTUM["y_giris"], zc), (xi, HORTUM["y_giris"], BULASIK_YER[2] - BM.D)]


def taban():
    """v4 · ALÇAK HAT: K tabanının altı — bulaşık makinesi REF (ayrı modül) + kanister rafı + deterjan / parlatıcı + dozaj hortumları"""
    for ad_, sh in bulasik_parcalari()[0]:
        ekle("REF_bulasik_" + ad_, cq.Workplane(obj=sh), "referans", "REF")
    zc = (KANISTER_Z[0] + KANISTER_Z[1]) / 2.0
    raf = kut(RAF_X[0], RAF_X[1], RAF_Y[0], RAF_Y[1], RAF_Z[0], RAF_Z[1])
    for xi in HORTUM["x_inis"]:
        raf = raf.cut(sily(xi, zc, HORTUM["delik_r"], RAF_Y[0] - 1.0, RAF_Y[1] + 1.0))     # hortum geçişi Ø14 (lastik rondela)
    ekle("deterjan_rafi", raf, "sac", bom=("Kanister rafı 304 · 5 mm (bulaşığın arkası)", 1, "%.0f × %.0f · 2 hortum deliği Ø%.0f" % (RAF_X[1] - RAF_X[0], RAF_Z[1] - RAF_Z[0], 2 * HORTUM["delik_r"]),
                                        "v4 · lazer · arka köşe dikmelerinin arasında"))
    t = KONSOL["t"]; z0, z1 = KONSOL["z"]
    for i, (xa, xb, xs0, xs1) in enumerate(((KONSOL["yatay"][0], KONSOL["yatay"][1], SAC, SAC + t), (W - KONSOL["yatay"][1], W - SAC, W - SAC - t, W - SAC))):
        k = kut(xa, xb, RAF_Y[0] - t, RAF_Y[0], z0, z1).union(kut(xs0, xs1, RAF_Y[0] - KONSOL["dikey_h"], RAF_Y[0], z0, z1))
        ekle("deterjan_rafi_konsolu_%d" % i, k, "sac", bom=("Raf konsolu 304 · 3 mm L büküm (yan saca 2 × M6)", 2, "%.1f × %.0f · boy %.0f" % (KONSOL["yatay"][1] - SAC, KONSOL["dikey_h"], z1 - z0),
                                                            "v4 · lazer + büküm") if i == 0 else None)
    for i, (ad_, xa, xb) in enumerate(KANISTER_X):
        yg = KANISTER_Y0 + KANISTER["y"] - KANISTER_KAPAK["h"]
        kg = KANISTER["L"] * KANISTER["yogunluk"] + KANISTER["bos_kg"]
        ekle("deterjan_kanisteri_" + ad_, kut(xa, xb, KANISTER_Y0, yg, KANISTER_Z[0], KANISTER_Z[1]), "kanister",
             bom=(("Bulaşık makinesi deterjanı 5 L bidon" if i == 0 else "Bulaşık makinesi parlatıcısı 5 L bidon"), 1,
                  "190 × 125 × 285 · dolu ≈ %.1f kg" % kg, "sarf · MEIKO uyumlu · ölçü VARSAYIM"))
        ekle("deterjan_kanister_kapagi_" + ad_, sily(xb - KANISTER_KAPAK["dx"], zc, KANISTER_KAPAK["r"], yg, KANISTER_Y0 + KANISTER["y"]), "kirmizi" if i == 0 else "mavi_kapak")
        pts = hortum_noktalari(i)
        L = sum(math.dist(a, b) for a, b in zip(pts[:-1], pts[1:]))
        ekle("deterjan_emis_hortumu_" + ad_, boru(pts, HORTUM["r"]), "dozaj",
             bom=("Dozaj emiş hortumu PVC Ø6/4 + emiş lansı (bidondan MEIKO dozaj pompasına)", 2, "≈ %.2f m / hortum" % (L / 1000.0),
                  "VARSAYIM · MEIKO dozaj girişinin yeri teyit edilecek") if i == 0 else None)


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


# ---------------------------------------------------------------- MODÜL ----------------------------------------------------------------
def modul():
    PARCALAR[:] = []
    govde(); bant(); kesici(); sprey_sistemi(); itici(); elektrik(); taban(); urun_ref()
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
    print("DENETİM (kesme_cad_v4)")
    H_ = hesap()
    # zarf
    tasan = []
    for p in PARCALAR:
        if p["grup"] in ("URUN", "URUN_IZ", "REF", "SPREY") or p["ad"].endswith("_kulp") or p["ad"] == "acil_stop":
            continue
        b = p["wp"].val().BoundingBox()
        if b.xmin < -0.5 or b.xmax > W + 0.5 or b.ymin < -0.5 or b.ymax > H + 0.5 or b.zmin < -D - 0.5 or b.zmax > 0.5:
            tasan.append(p["ad"])
    kontrol("zarf %.0f × %.0f × %.0f içinde (kulp / acil stop hariç)" % (W, H, D), not tasan, ", ".join(tasan))
    alta = [p["ad"] for p in PARCALAR if p["grup"] == "SABIT" and p["wp"].val().BoundingBox().ymin < Y_PLINT - 0.5 and not p["ad"].startswith(("ayak_", "plint_on"))]
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
    denetim_v4(H_)
    return H_


UYARI = []


def denetim_v4(H_):
    """v4 · ALÇAK HAT: dilim eşdeğerliği · yeni kotlar · E arayüzü · bulaşık yeri · kanister rafı (ölçülür)"""
    import dilim_v1 as DL
    import kesme_cad_v3 as ESKI
    # 1 · kotlar + E arayüzü
    ts = bbx("istasyon_tabani_3"); ust = max(p["wp"].val().BoundingBox().ymax for p in PARCALAR if p["grup"] == "SABIT")
    H_["taban_ust"] = ts.ymax; H_["bant"] = bbx("bant_PU_2mm").ymax; H_["ust"] = ust
    kontrol("ALÇAK HAT kotları: üst %.1f (2030 − 168) · istasyon tabanı sacı %.0f–%.0f · K bandı %.1f · fırın bandı %.0f · ürün girişi %.0f–%.0f"
            % (ust, ts.ymin, ts.ymax, H_["bant"], FIRIN_BANDI, URUN_GIRISI[0], URUN_GIRISI[1]),
            abs(ust - 1862.0) < 0.01 and abs(ts.ymin - 892.0) < 0.01 and abs(H_["bant"] - 996.0) < 0.01 and abs(FIRIN_BANDI - 998.0) < 0.01)
    kontrol("E arayüzü kutu_cad_v5: E plakası %.1f = K bandı %.1f · E penceresi %.0f–%.0f = K'deki · E kalıbı %.1f · tepsi %.0f" % (KC.PLAKA_K, BANT, KC.PENCERE[0], KC.PENCERE[1], KC.KALIP, KC.TEPSI),
            KC.__name__ == "kutu_cad_v5" and abs(KC.PLAKA_K - BANT) < 0.01 and all(abs(a - b) < 0.01 for a, b in zip(KC.PENCERE, E_PENCERE)))
    # 2 · DİLİM EŞDEĞERLİĞİ: v3'ün y 700–868 dilimi çıkarılmış hali ↔ v4 (doğrudan yeni kotlarda)
    ESKI.modul()
    ref, rap = DL.dilimle(ESKI.PARCALAR, DILIM_Y0, DILIM_DY, atla=("REF_kompresor_JUNAIR",))
    k = DL.karsilastir(PARCALAR, ref)
    yeni_ok = all(a.startswith(("REF_bulasik_", "deterjan_")) for a in k["yeni_ek"])
    H_["dilim"] = dict(v3=len(ESKI.PARCALAR), alt=len(rap["ALT"]), ust=len(rap["UST"]), gecen=rap["GECEN"], ayni=len(k["ayni"]), yeni=len(k["yeni_ek"]))
    kontrol("dilim y %.0f–%.0f: v3 %d parça (altta %d · üstte %d · boydan geçen %d: 3 sac + 4 dikme · bantta biten 0) ↔ v4 birebir %d · fark %d · yeni %d (bulaşık REF + deterjan)"
            % (DILIM_Y0, DILIM_Y0 + DILIM_DY, len(ESKI.PARCALAR), len(rap["ALT"]), len(rap["UST"]), len(rap["GECEN"]), len(k["ayni"]), len(k["fark"]), len(k["yeni_ek"])),
            not k["fark"] and not k["ref_eksik"] and yeni_ok and len(k["ayni"]) == len(ESKI.PARCALAR) - 1, "; ".join(k["fark"][:5]) + (" eksik %s" % k["ref_eksik"] if k["ref_eksik"] else ""))
    fu = max(max(abs(a - b) for a, b in zip(urun_merkez(t), ESKI.urun_merkez(t)[:1] + (ESKI.urun_merkez(t)[1] - DILIM_DY,) + ESKI.urun_merkez(t)[2:])) for t in [i * 0.05 for i in range(203)])
    fg = max(max(abs(a - b) for a, b in zip(grup_trs(g, t), ESKI.grup_trs(g, t))) for g in ("KESICI", "ITICI_ARABA", "ITICI_KOL", "URUN") for t in [i * 0.1 for i in range(201)])
    kontrol("kinematik: urun_merkez(t) = v3 − 168 (203 an, en büyük fark %.4f mm) · grup_trs(t) = v3 (201 an × 4 grup, %.4f)" % (fu, fg), fu < 1e-6 and fg < 1e-6)
    # 3 · BULAŞIK MAKİNESİ (ayrı modül, montajdaki yerinde)
    bm, (kx, ky, kz) = bulasik_parcalari()
    ONDE = ("isikli_kulp", "dokunmatik_ekran")                              # kapağın önündeki kulp + ekran (föy): kapak yüzü −20'nin önüne taşar
    bmb = cq.Compound.makeCompound([sh for a_, sh in bm if a_ not in ONDE]).BoundingBox()
    bon = max(sh.BoundingBox().zmax for a_, sh in bm if a_ in ONDE)
    bta = cq.Compound.makeCompound([sh for a_, sh in bm]).BoundingBox()     # makinenin TAMAMI (kulp + ekran + arka bağlantılar dahil)
    Z = BULASIK_ZARF
    H_["bulasik"] = dict(x=(bmb.xmin, bmb.xmax), y=(bmb.ymin, bmb.ymax), z=(bmb.zmin, bmb.zmax), dunya_x=(bmb.xmin + X_K_HAT, bmb.xmax + X_K_HAT))
    H_["bulasik"]["kulp_onu_z"] = bon
    H_["bulasik"]["tam_z"] = (bta.zmin, bta.zmax)
    kontrol("bulaşık (bulasik_cad_v1, kök %s): dünya x %.1f–%.1f · y %.0f–%.0f · kapak + gövde z %.0f…%.0f · TAMAMI (kulp + bağlantılar) z %.0f…%.0f = zarf %.0f…%.0f (SPEC 633) · kulp + ekran önü z %.1f ≤ 0 (modül ön yüzü) · ayaklar K alt sacında (%.0f)"
            % (BULASIK_YER, bmb.xmin + X_K_HAT, bmb.xmax + X_K_HAT, bmb.ymin, bmb.ymax, bmb.zmin, bmb.zmax, bta.zmin, bta.zmax, Z["z"][0], Z["z"][1], bon, bbx("taban_sac_3").ymax),
            bon <= 0.0 and abs(bta.zmin - Z["z"][0]) < 0.01 and abs(bta.zmax - Z["z"][1]) < 0.01 and
            bmb.xmin >= Z["x"][0] - 0.01 and bmb.xmax <= Z["x"][1] + 0.01 and bmb.ymin >= Z["y"][0] - 0.01 and bmb.ymax <= Z["y"][1] + 0.01
            and bmb.zmin >= Z["z"][0] - 0.01 and bmb.zmax <= Z["z"][1] + 0.01 and abs(bmb.ymin - bbx("taban_sac_3").ymax) < 0.01)
    K_ = [(p, p["wp"].val()) for p in PARCALAR if p["grup"] not in ("REF", "URUN", "URUN_IZ", "SPREY")]
    def kutu_(x, y, z):
        return cq.Solid.makeBox(x[1] - x[0], y[1] - y[0], z[1] - z[0], cq.Vector(x[0], y[0], z[0]))
    def giren(bolge, haric=()):
        L = []; B_ = bolge.BoundingBox()
        for p, sh in K_:
            if p["ad"].startswith(haric) if haric else False: continue
            if not KC._bb_kesisir(sh.BoundingBox(), B_): continue
            v = sh.intersect(bolge).Volume()
            if v > 0.01: L.append((p["ad"], round(v, 1)))
        return L
    g1 = giren(kutu_(Z["x"], Z["y"], Z["z"]), ("deterjan_emis_hortumu_",))
    kontrol("bulaşık zarfına (%.1f–%.1f × %.0f–%.0f × %.0f…%.0f) hiçbir K parçası girmez (dozaj hortum uçları makinenin arka yüzüne bağlanır)" % (Z["x"] + Z["y"] + Z["z"]), not g1, str(g1[:5]))
    g2 = []
    for p, sh in K_:
        A = sh.BoundingBox()
        for a_, b_ in bm:
            if KC._bb_kesisir(A, b_.BoundingBox()):
                v = sh.intersect(b_).Volume()
                if v > 0.01: g2.append((p["ad"], a_, round(v, 1)))
    kontrol("bulaşık gerçek katıları (%d parça) ↔ K parçaları çakışma %d" % (len(bm), len(g2)), not g2, str(g2[:5]))
    g3 = giren(kutu_(kx, ky, kz))
    H_["bulasik_kapak_zarfi"] = dict(x=kx, y=ky, z=kz)
    kontrol("kapak açık zarfı (alttan menteşeli, önde %.0f): x %.1f–%.1f · y %.0f–%.0f · z %.0f…%.0f → K parçası yok (sağ ön dikme x %.1f'de başlar)"
            % (kz[1] - kz[0], kx[0], kx[1], ky[0], ky[1], kz[0], kz[1], bbx("kose_dikmesi_1").xmin), not g3, str(g3[:5]))
    ap = kutu_(Z["x"], Z["y"], BULASIK_ARKA_PAY)
    g4 = giren(ap)
    hy = max([sh.intersect(ap).BoundingBox().ymax for p, sh in K_ if p["ad"].startswith("deterjan_emis_hortumu_")] + [0.0])
    kontrol("MEIKO arka payı z %.0f…%.0f boş: yalnız 2 dozaj hortumu geçer, o da bağlantı bölgesinde (üstü %.1f ≤ %.0f)" % (BULASIK_ARKA_PAY + (hy, BULASIK_BAGLANTI_UST)),
            all(a.startswith("deterjan_emis_hortumu_") for a, _v in g4) and len(g4) == 2 and hy <= BULASIK_BAGLANTI_UST, str(g4))
    ustu = [(p["wp"].val().BoundingBox().ymin, p["ad"]) for p in PARCALAR if p["grup"] not in ("REF", "URUN", "URUN_IZ", "SPREY")
            and KC._bb_kesisir(p["wp"].val().BoundingBox(), kutu_(Z["x"], (Z["y"][1], H), Z["z"]).BoundingBox())]
    H_["bulasik_ust_bosluk"] = min(ustu)[0] - bmb.ymax
    kontrol("bulaşığın üstü %.0f → ilk K parçası %s %.0f: boşluk %.0f mm" % (bmb.ymax, min(ustu)[1], min(ustu)[0], H_["bulasik_ust_bosluk"]), H_["bulasik_ust_bosluk"] > 0.0)
    sol = bmb.xmin - bbx("kose_dikmesi_0").xmax; sol_ark = bmb.xmin - bbx("sol_sac_urun_girisi").xmax
    H_["bulasik_sol"] = dict(on=sol, arka=sol_ark)
    print("     bulaşığın solu: önde %.1f (köşe dikmesinden) · dikmenin arkasında %.1f (sol sacdan) → BOŞ" % (sol, sol_ark))
    # 4 · KANİSTER RAFI + BİDONLAR
    kg = KANISTER["L"] * KANISTER["yogunluk"] + KANISTER["bos_kg"]
    F = len(KANISTER_X) * kg * 9.81
    Lr = (W - KONSOL["yatay"][1]) - KONSOL["yatay"][1]                    # konsol uçları arası açıklık
    I_ = (RAF_Z[1] - RAF_Z[0]) * (RAF_Y[1] - RAF_Y[0]) ** 3 / 12.0
    w_ = 5.0 * (F / Lr) * Lr ** 4 / (384.0 * 193000.0 * I_)               # basit mesnet, yayılı yük (304: E 193 GPa)
    H_["raf_sehim_mm"] = w_; H_["kanister_kg"] = kg
    kontrol("kanister rafı %.0f × %.0f × %.0f · yük %d × %.1f kg = %.0f N · açıklık %.0f · sehim %.2f mm ≤ L/300 = %.2f [VARSAYIM yoğunluk 1,3]"
            % (RAF_X[1] - RAF_X[0], RAF_Z[1] - RAF_Z[0], RAF_Y[1] - RAF_Y[0], len(KANISTER_X), kg, F, Lr, w_, Lr / 300.0), w_ <= Lr / 300.0)
    kb = [bbx("deterjan_kanisteri_" + a) for a, _x0, _x1 in KANISTER_X]
    kk = [bbx("deterjan_kanister_kapagi_" + a) for a, _x0, _x1 in KANISTER_X]
    kontrol("bidonlar rafın üstünde: x %.0f–%.0f / %.0f–%.0f · y %.0f–%.0f · z %.0f…%.0f · arka paydan %.0f · arka dikmelerden x'te %.1f / %.1f"
            % (kb[0].xmin, kb[0].xmax, kb[1].xmin, kb[1].xmax, kb[0].ymin, max(b.ymax for b in kk), kb[0].zmin, kb[0].zmax,
               BULASIK_ARKA_PAY[0] - kb[0].zmax, kb[0].xmin - bbx("kose_dikmesi_2").xmax, bbx("kose_dikmesi_3").xmin - kb[1].xmax),
            all(abs(b.ymin - RAF_Y[1]) < 0.01 for b in kb) and abs(max(b.ymax for b in kk) - (KANISTER_Y0 + KANISTER["y"])) < 0.01 and kb[0].zmax <= BULASIK_ARKA_PAY[0])
    Lh = [sum(math.dist(a, b) for a, b in zip(hortum_noktalari(i)[:-1], hortum_noktalari(i)[1:])) for i in range(len(KANISTER_X))]
    H_["hortum_m"] = [round(x / 1000.0, 2) for x in Lh]
    print("     dozaj hortumları: %s m · makineye y %.0f'de girer (x %s) · raftan Ø%.0f delikle iner" % (H_["hortum_m"], HORTUM["y_giris"], HORTUM["x_inis"], 2 * HORTUM["delik_r"]))
    # erişim: bidon değişimi için makinenin yanındaki boşluk
    en_dar = min(KANISTER["x"], KANISTER["z"])
    if sol_ark < en_dar:
        UYARI.append("bidon değişimi: bulaşığın solunda dikmenin arkası %.0f mm < bidonun en dar yüzü %.0f → bidon yandan çıkmaz; bulaşık öne çekilmeli (hortum payı) ya da arka sacda servis kapağı gerekir" % (sol_ark, en_dar))
    for u in UYARI:
        print("  UYARI: " + u)
    H_["uyari"] = list(UYARI)


# ---------------------------------------------------------------- ÇAKIŞMA TARAMASI ----------------------------------------------------------------
ISTISNA = [("bant_PU", "rulosu"), ("bant_PU", "kayma_tablasi"), ("rulosu_mili", "rulosu"), ("rulosu_mili", "bant_yan"), ("gergi_civatasi", "bant_yan"),
           ("tabla_kirisi", "bant_yan"), ("tabla_kirisi", "kayma_tablasi"), ("bant_ayagi", "istasyon_tabani"), ("bant_ayagi", "bant_yan"),
           ("ayak_", "taban_sac"), ("kose_dikmesi", "taban_sac"), ("kose_dikmesi", "ust_sac"), ("kose_dikmesi", "istasyon_tabani"),
           ("kose_dikmesi", "_sac"), ("kopru_kirisi", "kose_dikmesi"), ("kopru_kirisi", "_sac_"), ("silindir_baglanti", "kopru_kirisi"), ("silindir_baglanti", "DGRF-C"),
           ("DGRF_", "DGRF-C"), ("DGRF_piston_mili", "DGRF_on_plaka"), ("DGRF_kilavuz", "DGRF_on_plaka"), ("DGRF_kilavuz", "silindir_baglanti"),
           ("ara_dikme", "DGRF_on_plaka"), ("ara_dikme", "kafa_plakasi"), ("bicak_", "kafa_plakasi"), ("bicak_gobek", "bicak_"), ("koruma_braketi", "kafa_plakasi"),
           ("koruma_braketi", "koruma_halkasi"), ("kelebek_somun", "kafa_plakasi"), ("PulsaJet", "sprey_dirsegi"), ("PulsaJet_isitici", "PulsaJet_AA"),
           ("sprey_dirsegi", "kafa_plakasi"), ("UniJet", "kafa_plakasi"), ("UniJet", "bicak_gobek"), ("UniJet", "sprey_dirsegi"), ("UniJet", "bicak_"), ("sprey_ucu", "UniJet"),
           ("isitmali_hortum_kafa", "PulsaJet"), ("yag_tanki", "yag_tanki"), ("yag_regulator", "yag_tanki"), ("yag_seviye", "yag_tanki"), ("yag_tanki_rafi", "yag_tanki"), ("yag_tanki_rafi_koseben", "sol_sac"), ("yag_tanki_rafi_koseben", "yag_tanki_rafi"),
           ("isitmali_hortum_Ø6", "yag_tanki"), ("isitmali_hortum_Ø6", "istasyon_tabani"), ("isitmali_hortum_Ø6", "kopru_kirisi"), ("isitmali_hortum_Ø6", "isitmali_hortum_kafa"),
           ("hava_hortumu_tank", "yag_"), ("hava_hortumu_tank", "istasyon_tabani"), ("hava_besleme", "istasyon_tabani"), ("hava_besleme", "sartlandirici"),
           ("hava_hortumu_kesici", "valf_adasi"), ("hava_hortumu_kesici", "DGRF"), ("hava_hortumu_kesici", "kopru_kirisi"), ("hava_hortumu_kaldirma", "valf_adasi"),
           ("ZLW", "ZLW"), ("itici_motoru", "ZLW_uc"), ("eksen_ayagi", "ZLW"), ("eksen_ayagi", "istasyon_tabani"), ("itici_home", "ZLW"),
           ("ZLW_araba", "kaldirma_braketi"), ("kaldirma_braketi", "MGPM"), ("kaldirma_kizagi", "MGPM"), ("kaldirma_kizagi", "itici_kolu"), ("itici_kolu", "itici_kolu"),
           ("itici_kolu_z", "itme_cubugu"), ("itme_cubugu", "itici_celik"), ("itici_celik", "itici_POM"), ("ZLW_araba", "ZLW-1040"),
           ("pano_plakasi", "din_rayi"), ("din_rayi", "plc_"), ("din_rayi", "guc_"), ("din_rayi", "surucu_"), ("din_rayi", "klemens"), ("din_rayi", "emniyet"), ("din_rayi", "PWMD"),
           ("din_rayi", "sicaklik"), ("pano_plakasi", "kablo_kanali"), ("kablo_kanali_dikey", "istasyon_tabani"), ("kablo_kanali_dikey", "kose_dikmesi"), ("kablo_kanali", "arka_sac"),
           ("sartlandirici", "arka_sac"), ("valf_adasi", "arka_sac"), ("olu_plaka", "bant_yan"), ("cit_braketi", "bant_yan"), ("cit_braketi", "cit_20"),
           ("icecek_kolisi", "icecek_kolisi"), ("icecek_kolisi", "taban_sac"), ("icecek_rafi", "taban_sac"), ("taban_kapisi", "kose_dikmesi"), ("ust_kapi", "kose_dikmesi"),
           ("ust_kapi", "ust_kapi"), ("taban_kapisi", "taban_kapisi"), ("kapi_kilidi", "ust_kapi"), ("kapi_kilidi", "kose_dikmesi"), ("acil_stop", "ust_kapi"),
           ("kesici_reed", "DGRF-C"), ("sensor_", "bant_yan"), ("sensor_", "bant_PU"), ("DGRF_hava", "hava_hortumu_kesici"), ("DGRF_hava", "DGRF-C"), ("sol_sac", "_sac"), ("sag_sac", "_sac"), ("arka_sac", "_sac"), ("ust_sac", "_sac"),
           ("kose_dikmesi", "arka_sac"), ("istasyon_tabani", "_sac"), ("taban_sac", "_sac"), ("plint_on", "taban_sac")]


def _ist(a, b):
    for p, q in ISTISNA:
        if (p in a and q in b) or (p in b and q in a):
            return True
    return False


def cakisma(esik=1.0, adim=0.1):
    t0 = time.time()
    sab = [(p, p["wp"].val()) for p in PARCALAR if p["grup"] == "SABIT"]
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
    sab = [(p, p["wp"].val()) for p in PARCALAR if p["grup"] == "SABIT"]
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
    GRUPLAR = ["SABIT", "REF", "KESICI", "ITICI_ARABA", "ITICI_KOL", "URUN", "URUN_IZ", "SPREY"]
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
    gl = {"asset": {"version": "2.0", "generator": "AUTOKITCH kesme_cad_v4"}, "scene": 0, "scenes": [{"nodes": list(range(len(nodes)))}], "nodes": nodes, "meshes": meshes,
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
                                                         "Seviye", "regülatör", "Polikarbonat", "PWM", "Acil", "Silindir sensörü", "koli", "kolisi", "hortum", "Avara", "tank", "bidon")) else "ÜRETİM"
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


def json_yaz(yol, H_, cak):
    with io.open(yol, "w", encoding="utf-8") as f:
        json.dump(dict(surum="kesme_cad_v4 · %s" % time.strftime("%d.%m.%Y %H:%M"),
                       parcalar=[dict(ad=p["ad"], grup=p["grup"], mal=p["mal"], bom=list(p["bom"]) if p["bom"] else None) for p in PARCALAR],
                       denetim=[dict(ad=a, sonuc="GEÇTİ" if s else "KALDI", deger=v) for a, s, v in DEN], hesap=H_, cakisma=cak), f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    t0 = time.time(); arg = sys.argv[1:]
    modul()
    print("K KESME + SPREY v4 (alcak hat: ust 1862 · taban 892 · bant 996 · altinda bulasik + deterjan): %d parca · %.0f sn" % (len(PARCALAR), time.time() - t0)); sys.stdout.flush()
    H_ = denetim(); sys.stdout.flush()
    cak = {}
    if "hizli" not in arg:
        cak["makine"] = len(cakisma()); sys.stdout.flush()
        cak["urun"] = len(urun_cakisma()); sys.stdout.flush()
        cak["itici_E"] = len(e_itici_cakisma()); sys.stdout.flush()
    if "glb" in arg or "hepsi" in arg:
        glb_yaz(os.path.join(KOK, "otonom", "hat3d", "kesme_v4.glb"))
    if "bom" in arg or "hepsi" in arg:
        bom_yaz(os.path.join(KOK, "arastirma", "4_KESME_v4"))
    json_yaz(os.path.join(KOK, "otonom", "hat3d", "kesme_v4.json"), H_, cak)
    kal = [d for d in DEN if not d[1]]
    print("DENETIM: %d madde · %d KALDI · toplam %.0f sn" % (len(DEN), len(kal), time.time() - t0))
    sys.stdout.flush(); os._exit(0)
