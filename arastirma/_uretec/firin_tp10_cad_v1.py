# -*- coding: utf-8 -*-
"""AUTOKITCH · F FIRIN DENEMESİ (AYRI SÜRÜM) · Sveba Dahlen TP Infinity TP10 · 3B MODEL + HATTA UYARLAMA v1 (26 Eyl 2026)
Kemal: "ayrı versiyon olarak modelle, tüm detaylarıyla, adapte et bizim 3D'ye ama istemezsem geri alınacak şekilde".
Ana makine (hat_montaj_v47) DEĞİŞMEZ; bu model yalnız hat_montaj_tp10_v1 (ayrı GLB) ve firin_tp10.html içindir.

KAYNAK (föy): Sveba Dahlen broşür 990004-002 (Oca 2024) s.6 ölçü çizimi + ürün sayfası + opsiyon föyü 990004-002-2 (Ara 2025)
  https://sveba.com/sites/default/files/2024-02/TP%20Pizza-Series_990004-002_EN.pdf
  https://sveba.com/en/products/ovens/tunnel-pizza-oven-tp-infinity
  Föyde YAZILI: toplam 1550 · derinlik 730 · yükseklik 599–637 (ayak 82–120) · bant 381 × 1450 · iç yükseklik 85 · 0,34 m² ·
  9,5 kW · 25 A · 160 kg · 400 °C · plaka max 390 · kızılötesi, üst/alt ayrı, fansız.
  "≈" = föyün ölçü çiziminden ölçekle (uzun görünüş 1,856 mm/px · uç görünüş 1,14 / 1,152 mm/px) — ÜRETİCİDEN TEYİT GEREKİR.
  VARSAYIM = föyde ve çizimde yok (iç yerleşim, rulo çapı, ray) — gösterim içindir, üretici CAD'i istenmeli.
DÜZELTME (pafta v1'e göre): uç kutuları bandın iki yanını SARMAZ; ekran tarafında YAN KUTU (uç görünüşünde 0–237 mm, 110–277 mm
  kotlarında çizgiler + üstünde gergi düğmeleri). Bandın uçları açık. → pafta v2.

KOORDİNAT (fırın yereli): x bant yönü (0 = gövde ortası) · y yukarı (0 = gövde altı) · z: 0 = ekransız uzun yüz (hatta ÖN YÜZ),
  −730 = ekranlı yüz (hatta ARKA, servis tarafı).  Hat yerleşimi: YER = (XC_TP, YG0, 0) ötelemesi.
"""
import math, os, sys
import cadquery as cq

U = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, U)
KOK = os.path.dirname(os.path.dirname(U))
from kaset_3d_v3 import Mesh, MM, MALZEME

# ================================================================ ÖLÇÜLER ================================================================
# ---- föy ----
L_TOP, D_TP = 1550.0, 730.0                      # toplam boy (uç kutusu dış yüzleri) · derinlik
H_AYAKLI, AYAK = (599.0, 637.0), (82.0, 120.0)   # ayaklı yükseklik · ayak (ayarlı)
BANT_W, BANT_L, IC_H, ALAN = 381.0, 1450.0, 85.0, 0.34
GUC, SIGORTA, KUTLE, T_MAX, PLAKA_MAX = 9.5, 25, 160, 400, 390.0
# ---- ≈ föy çiziminden ----
H_GOV = H_AYAKLI[0] - AYAK[0]                    # 517 gövde (599 − 82 = 637 − 120)
L_GOV = 960.0                                    # gövde boyu (çizim 952–964 · TP10/20 sehpası 960 × 730)
ODA = ALAN / (BANT_W / 1000.0) * 1000.0          # 892,4 ısıtılan boy (0,34 m² ÷ 0,381 m)
UC = (L_TOP - L_GOV) / 2.0                       # 295 uç kutusu (gövde dışı)
UC_Z = (-D_TP + 237.0, -D_TP)                    # uç kutusu ekran tarafında 237 genişlik: z −493 … −730
UC_Y = (110.0, 277.0)                            # uç kutusu alt/üst (uzun görünüş 107–277 · uç görünüşü 112–278)
BANT_Y = 210.0                                   # bant üstü gövde altından (uç görünüşü 208–223 · plaka bağlantısı 200–220) ±15
TUNEL_Z = (-485.0, -79.0)                        # tünel (ağız) genişliği 406 · ön duvar 79 (uç görünüşü 245–651 mm ekran yüzünden)
BANT_Z = (-473.5, -92.5)                         # bant 381, eksen −283 (çizimde 263–631 mm ekran yüzünden)
TUNEL_Y = (33.0, 307.0)                          # uç yüzü açıklığı: alt bölme 33–208 + ağız 208–307
EKRAN = (189.0, 151.0, 240.0)                    # dokunmatik ekran genişlik · yükseklik · alt kotu
TEPE_BANDI = 59.0                                # üst etiket bandı (SVEBA DAHLEN)
FAN = (133.0, 148.0, 194.0)                      # uç kutusu fanı Ø · dış uçtan x · kot
DUGME_X = (78.0, 84.0)                           # gergi düğmesi dış uçtan (sol · sağ)
AYAK_X, AYAK_Z = 353.0, (-131.0, -527.0)
# ---- VARSAYIM (föyde yok) ----
RULO_R, BANT_K = 20.0, 6.0                       # bant ucu rulosu Ø40 · paslanmaz tel örgü bant 6 mm
RULO_X = BANT_L / 2.0 - RULO_R - BANT_K          # 699 rulo ekseni
RULO_Y = BANT_Y - BANT_K - RULO_R                # 184
RAY_X = RULO_X + 6.0                             # 705 konveyör yan rayı ucu
RAY_Y = (150.0, BANT_Y - 8.0)                    # ray üstü bandın 8 mm altında (taşan ürün kenarı üstünden geçer)
ADIM = 310.0                                     # ürün adımı (Ø300 + 10) [hat kuralı]

# ================================================================ HATTA YERLEŞİM ================================================================
# Kısıtlar (ölçüldü, 26 Eyl): TOPPING X tahriki F'ye taşıyor (x motoru ≤ 2563, kaidesi ≤ 2580, y ≤ 1135) · K'nin bant yan levhaları 4010,
# itici eksen uç bloğu 4016'dan başlıyor · TOPPING sağ yan sacı 2500 · K sol sacı 4000. TP10 bandı 1450 → bu aralık 1430.
# SEÇİM: bant başı x 2564 (x motoruna 1 mm, kaide köşesi pahlanır) → bant ucu 4014 (K yan levhaları 18'den başlar).
BANT_UST_HAT = 1166.0                            # kot zinciri: disk 1168 → fırın bandı 1166 → K 1164
X0 = 2514.0                                      # uç kutusu sol dış yüzü
XC_TP = X0 + L_TOP / 2.0                         # 3289 gövde ortası
YG0 = BANT_UST_HAT - BANT_Y                      # 956 gövde altı (ayaksız, F taban dolabı üstüne oturur)
YG1 = YG0 + H_GOV                                # 1473 gövde üstü
YER = (XC_TP, YG0, 0.0)
def hx(x): return XC_TP + x
BANT_X = (hx(-BANT_L / 2.0), hx(BANT_L / 2.0))   # 2564 … 4014
GOV_X = (hx(-L_GOV / 2.0), hx(L_GOV / 2.0))      # 2809 … 3769
ODA_X = (hx(-ODA / 2.0), hx(ODA / 2.0))          # 2843 … 3735
ZT = -170.0                                      # hat ürün ekseni (tabla · K)
Z_URUN_FIRIN = -249.0                            # fırında ürün merkezi (Ø300 ön kenarı −99: tünel ön duvarına 20 mm)
PZ_R = 150.0                                     # çit hesabında ürün zarfı Ø300 (K'nin çitiyle aynı kural)

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
    """(x, z) çokgeni y0 … y1 arasında dik prizma"""
    return cq.Workplane("XZ", origin=(0.0, y1, 0.0)).polyline(pts).close().extrude(y1 - y0)


def ekle(ad, wp, mal, birim, grup="SABIT", kaynak="VARSAYIM", bom=None, yerel=True):
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


# ================================================================ 1 · TP10 (katalog ünitesi) ================================================================
def firin(ayak=False, plaka=False):
    """TP10 dış görünüşü föy + çizimden, iç yerleşimi VARSAYIM (şematik). Parçalar fırın yerelinde."""
    G, K = "F_TP10_GOVDE", "F_TP10_KONVEYOR"
    ox, oy0, oy1 = L_GOV / 2.0, 0.0, H_GOV
    # --- gövde: dış kabuk 1,5 · tünel kaplaması 1 · taşyünü · teknik bölme duvarı ---
    kab = kut(-ox, ox, oy0, oy1, -D_TP, 0.0).cut(kut(-ox + 1.5, ox - 1.5, 1.5, oy1 - 1.5, -D_TP + 1.5, -1.5)) \
        .cut(kut(-ox - 10, ox + 10, TUNEL_Y[0], TUNEL_Y[1], TUNEL_Z[0], TUNEL_Z[1]))
    ekle("govde_kabugu", kab, "paslanmaz", G, kaynak="föy 1550/730 · ≈ gövde 960 × 517",
         bom=("TP10 gövde kabuğu · paslanmaz", 1, "Sveba Dahlen (katalog ünitesi)", "960 × 517 × 730 ≈"))
    ekle("tunel_kaplamasi", kut(-ox + 1.5, ox - 1.5, TUNEL_Y[0] - 1.0, TUNEL_Y[1] + 1.0, TUNEL_Z[0] - 1.0, TUNEL_Z[1] + 1.0)
         .cut(kut(-ox - 10, ox + 10, TUNEL_Y[0], TUNEL_Y[1], TUNEL_Z[0], TUNEL_Z[1])), "paslanmaz", G, kaynak="VARSAYIM (iç)")
    ekle("yalitim_tasyunu", kut(-ox + 1.5, ox - 1.5, 1.5, oy1 - 1.5, TUNEL_Z[0] - 4.0, -1.5)
         .cut(kut(-ox - 10, ox + 10, TUNEL_Y[0] - 1.0, TUNEL_Y[1] + 1.0, TUNEL_Z[0] - 1.0, TUNEL_Z[1] + 1.0)), "yalitim", G, kaynak="VARSAYIM (iç)")
    ekle("teknik_bolme_duvari", kut(-ox + 1.5, ox - 1.5, 1.5, oy1 - 1.5, TUNEL_Z[0] - 5.5, TUNEL_Z[0] - 4.0), "paslanmaz", G, kaynak="≈ uç görünüşü 237 mm",
         bom=("Teknik bölme (sürücü · kontaktör · SSR — iç yerleşim üreticide)", 1, "katalog", "≈ 239 derinlik, ekran tarafı"))
    # --- ısıtıcılar: üstte + altta 2'şer bölge (şematik) ---
    for i, (a, b) in enumerate(((-ODA / 2.0 + 5.0, -5.0), (5.0, ODA / 2.0 - 5.0))):
        ekle("ust_isitici_%d" % (i + 1), kut(a, b, TUNEL_Y[1] - 10.0, TUNEL_Y[1] - 1.0, BANT_Z[0], BANT_Z[1]), "ir", G, kaynak="föy: IR üst/alt ayrı · yerleşim VARSAYIM",
             bom=("Kızılötesi ısıtıcı · üst · bölge %d" % (i + 1), 1, "katalog", "400 °C · 9,5 kW toplam") if i == 0 else None)
        ekle("alt_isitici_%d" % (i + 1), kut(a, b, RULO_Y - 12.0, RULO_Y - 4.0, BANT_Z[0], BANT_Z[1]), "ir", G, kaynak="föy: IR üst/alt ayrı · yerleşim VARSAYIM",
             bom=("Kızılötesi ısıtıcı · alt · bölge %d" % (i + 1), 1, "katalog", "bandın üst ve alt kolu arasında") if i == 0 else None)
    ekle("kirinti_tepsisi", kut(-ox + 12.0, ox - 12.0, TUNEL_Y[0], TUNEL_Y[0] + 5.0, TUNEL_Z[0] + 2.0, TUNEL_Z[1] - 2.0), "paslanmaz", G, kaynak="VARSAYIM")
    # --- ekran tarafı (hatta ARKA): etiket bandı · ekran · şalter · servis plakası · vidalar · mandallar ---
    ekle("ust_etiket_bandi", kut(-ox, ox, oy1 - TEPE_BANDI, oy1, -D_TP - 1.0, -D_TP), "grafit", G, kaynak="≈ uzun görünüş (SVEBA DAHLEN)")
    ew, eh, ey = EKRAN
    ekle("ekran_cercevesi", kut(-ew / 2 - 10, ew / 2 + 10, ey - 10, ey + eh + 10, -D_TP - 8.0, -D_TP), "koyu", G, kaynak="≈ uzun görünüş",
         bom=("Dokunmatik ekran (TP Infinity kumanda)", 1, "katalog", "≈ 189 × 151 · arka yüzde (servis tarafı)"))
    ekle("ekran_cami", kut(-ew / 2, ew / 2, ey, ey + eh, -D_TP - 9.0, -D_TP - 8.0), "ekran", G, kaynak="≈ uzun görünüş")
    ekle("ana_salter", silz(0.0, 200.0, 18.0, -D_TP - 20.0, -D_TP), "koyu", G, kaynak="≈ uzun görünüş (ekranın altı)")
    ekle("servis_plakasi", kut(352.0, 437.0, 138.0, 199.0, -D_TP - 2.0, -D_TP), "koyu", G, kaynak="≈ uzun görünüş")
    for i, (x, y) in enumerate(((-462.0, 171.0), (462.0, 171.0), (-462.0, 431.0), (462.0, 431.0))):
        ekle("panel_vidasi_%d" % i, silz(x, y, 4.0, -D_TP - 2.0, -D_TP), "celik", G, kaynak="≈ uzun görünüş")
    for i, s in enumerate((-1.0, 1.0)):
        ekle("kapak_mandali_%d" % i, kut(s * ox, s * (ox + 69.0), 290.0, 300.0, -D_TP + 8.0, -D_TP + 18.0), "celik", G, kaynak="≈ uzun görünüş (gövde uçlarında)")
    # --- uç kutuları (ekran tarafında yan kutu) + fan + gergi düğmesi ---
    for i, s in enumerate((-1.0, 1.0)):
        a, b = sorted((s * ox, s * (ox + UC)))
        uk = kut(a, b, UC_Y[0], UC_Y[1], UC_Z[1], UC_Z[0]).cut(kut(a + 1.5, b - 1.5, UC_Y[0] + 1.5, UC_Y[1] - 1.5, UC_Z[1] + 1.5, UC_Z[0] - 1.5))
        ekle("uc_kutusu_%s" % ("giris" if s < 0 else "cikis"), uk, "paslanmaz", G, kaynak="föy 1550 · ≈ 295 × 237 × 167",
             bom=("Uç kutusu (bant tahriki / gergisi · fan)", 2, "katalog", "≈ 295 × 237 × 167 · ekran tarafında") if i == 0 else None)
        fx_ = s * (ox + UC - FAN[1])
        ekle("fan_%d" % i, silz(fx_, FAN[2], FAN[0] / 2.0, -D_TP - 2.0, -D_TP), "koyu", G, kaynak="≈ uzun görünüş Ø133")
        ekle("fan_halkasi_%d" % i, silz(fx_, FAN[2], FAN[0] / 2.0, -D_TP - 3.0, -D_TP - 2.0).cut(silz(fx_, FAN[2], FAN[0] / 2.0 - 5.0, -D_TP - 4.0, -D_TP)), "celik", G, kaynak="≈")
        dx_ = s * (ox + UC - DUGME_X[i])
        ekle("gergi_dugmesi_%d" % i, sily(dx_, sum(UC_Z) / 2.0, 15.0, UC_Y[1], UC_Y[1] + 38.0).union(sily(dx_, sum(UC_Z) / 2.0, 11.0, UC_Y[1] + 38.0, UC_Y[1] + 46.0)),
             "koyu", G, kaynak="≈ uzun görünüş (uç kutusu üstünde)")
        for j, (dx2, dy2) in enumerate(((-110.0, -60.0), (110.0, -60.0), (-110.0, 60.0), (110.0, 60.0))):
            ekle("uc_vidasi_%d_%d" % (i, j), silz(s * (ox + UC / 2.0) + dx2 * 0.9, (UC_Y[0] + UC_Y[1]) / 2.0 + dy2, 3.0, -D_TP - 1.5, -D_TP), "celik", G, kaynak="≈")
    # --- uç yüzü (giriş): elektrik girişi + sinyal kutusu (uç görünüşü) ---
    ekle("cee_priz", silx(74.0, -647.0, 28.0, -ox - 30.0, -ox), "koyu", G, kaynak="≈ uç görünüşü (Ø57)")
    ekle("sinyal_kutusu", kut(-ox - 5.0, -ox, 54.0, 108.0, -607.0, -499.0), "koyu", G, kaynak="≈ uç görünüşü 108 × 54")
    # --- KONVEYÖR: tel örgü bant (üst kol şerit şerit) · alt kol · sarımlar · rulolar · raylar · yataklar ---
    z0, z1 = BANT_Z
    n = int((2 * RULO_X) // 25.0)
    for j in range(n):
        xa = -RULO_X + j * 25.0; xb = min(RULO_X, xa + 20.0)
        ekle("bant_ust_%02d" % j, kut(xa, xb, BANT_Y - BANT_K, BANT_Y, z0, z1), "tel_bant", K, kaynak="föy 381 × 1450 · örgü VARSAYIM",
             bom=("Konveyör bandı · paslanmaz tel örgü", 1, "katalog", "381 × 1450 (föy)") if j == 0 else None)
    ekle("bant_alt_kol", kut(-RULO_X, RULO_X, RULO_Y - RULO_R - BANT_K, RULO_Y - RULO_R, z0, z1), "tel_bant", K, kaynak="VARSAYIM")
    for s, ad in ((-1.0, "giris"), (1.0, "cikis")):
        x = s * RULO_X
        sar = silz(x, RULO_Y, RULO_R + BANT_K, z0, z1).cut(silz(x, RULO_Y, RULO_R, z0 - 1, z1 + 1))
        sar = sar.cut(kut(x, x - s * 100.0, RULO_Y - 40, RULO_Y + 40, z0 - 1, z1 + 1))
        g = "RULO_TP_%s" % ad.upper()
        ekle("bant_sarimi_%s" % ad, sar, "tel_bant", K, grup=g, kaynak="VARSAYIM Ø40 rulo")
        ekle("rulo_%s" % ad, silz(x, RULO_Y, RULO_R, z0 + 1.5, z1 - 1.5).cut(silz(x, RULO_Y, 10.0, z0, z1)), "celik", K, grup=g, kaynak="VARSAYIM Ø40",
             bom=("Bant ucu rulosu Ø40 (VARSAYIM)", 2, "katalog", "giriş: gergi · çıkış: tahrik (uç kutusunda)") if s < 0 else None)
        ekle("rulo_mili_%s" % ad, silz(x, RULO_Y, 10.0, UC_Z[0], -80.0), "celik", K, grup=g, kaynak="VARSAYIM")
        ekle("on_yatak_%s" % ad, kut(x - 18.0, x + 18.0, RULO_Y - 16.0, RULO_Y + 16.0, -80.0, -62.0).cut(silz(x, RULO_Y, 10.2, -81.0, -61.0)), "koyu", K, kaynak="VARSAYIM")
    _del = lambda w: w.cut(silz(-RULO_X, RULO_Y, 10.2, -500.0, -60.0)).cut(silz(RULO_X, RULO_Y, 10.2, -500.0, -60.0))
    ekle("on_ray", _del(kut(-RAY_X, RAY_X, RAY_Y[0], RAY_Y[1], -84.0, -81.0)), "paslanmaz", K, kaynak="VARSAYIM")
    ekle("arka_ray", _del(kut(-RAY_X, RAY_X, RAY_Y[0], RAY_Y[1], -484.0, -481.0)), "paslanmaz", K, kaynak="VARSAYIM")
    if ayak:
        for i, (x, z) in enumerate(((-AYAK_X, AYAK_Z[0]), (AYAK_X, AYAK_Z[0]), (-AYAK_X, AYAK_Z[1]), (AYAK_X, AYAK_Z[1]))):
            ekle("ayak_%d" % i, sily(x, z, 22.0, -AYAK[0], -8.0).union(sily(x, z, 30.0, -8.0, 0.0)), "koyu", "F_TP10_AYAK", kaynak="föy 82–120 · ≈ Ø")
    if plaka:
        c, s_ = math.cos(math.radians(25.0)), math.sin(math.radians(25.0))
        xa = BANT_L / 2.0 + 2.0
        pts = [(xa, BANT_Y), (xa + PLAKA_MAX * c, BANT_Y - PLAKA_MAX * s_), (xa + PLAKA_MAX * c, BANT_Y - PLAKA_MAX * s_ - 3.0), (xa, BANT_Y - 3.0)]
        ekle("cikis_plakasi", cq.Workplane("XY", origin=(0, 0, z0)).polyline(pts).close().extrude(z1 - z0), "paslanmaz", "F_TP10_PLAKA", kaynak="föy max 390 · ≈ 25°")


# ================================================================ 2 · ÇİT GEOMETRİSİ + ÜRÜN YOLU ================================================================
TAN20 = math.tan(math.radians(20.0))
# giriş çiti: ÜRÜNÜN ÖNÜNDE, ürünü −170'ten −249'a iter · temas çizgisi (x, z) · gövdeye 2 mm kala biter
# NOT: ürün çitin UCUNU geçerken uç köşe ürünü kendi z'sine kadar iter → son konum = köşe z ∓ R (teğet noktası değil)
GC_B = (GOV_X[0] - 2.0, Z_URUN_FIRIN + PZ_R)                                                # (2807, −99)  ön kenar −99
GC_A = (GC_B[0] - (GC_B[1] - (-15.0)) / (-TAN20), -15.0)                                     # (2576, −15)
# çıkış çiti: ÜRÜNÜN ARKASINDA, ürünü −249'dan −170'e geri iter · gövdeden 2 mm sonra başlar
CC_A = (GOV_X[1] + 2.0, Z_URUN_FIRIN - PZ_R - 5.0)                                            # (3771, −404)
CC_B = (CC_A[0] + (ZT - PZ_R - CC_A[1]) / TAN20, ZT - PZ_R)                                  # (4002, −320)  arka kenar −320


def _cit_noktalari(A, B, n=400):
    return [(A[0] + (B[0] - A[0]) * i / n, A[1] + (B[1] - A[1]) * i / n) for i in range(n + 1)]


_GC = _cit_noktalari(GC_A, GC_B); _CC = _cit_noktalari(CC_A, CC_B)


def urun_z(xc):
    """ürün merkezinin z'si (xc'de) — çitler Ø300 zarfı iter (K'nin 20° çitiyle aynı kural)."""
    z = ZT
    # giriş çiti (önde): merkez her çit noktasından R uzakta ve ARKASINDA kalır
    for px, pz in _GC:
        d = xc - px
        if abs(d) < PZ_R:
            z = min(z, pz - math.sqrt(PZ_R * PZ_R - d * d))
    if xc > GC_B[0]:
        z = min(z, Z_URUN_FIRIN)                    # çit bitti: ürün −249'da kalır (kimse geri itmez)
    zc = z
    for px, pz in _CC:                              # çıkış çiti (arkada): merkez çitin ÖNÜNDE kalır
        d = xc - px
        if abs(d) < PZ_R:
            zc = max(zc, pz + math.sqrt(PZ_R * PZ_R - d * d))
    if xc > CC_B[0]:
        zc = max(zc, ZT)
    return min(ZT, zc)


# ================================================================ 3 · HATTA UYARLAMA (bizim parçalar, DÜNYA koordinatı) ================================================================
X_DISK_KENAR = 2507.0                            # TOPPING tabla aktarma konumunda disk kenarı (700 + 1637 + 170)
GB_RY = BANT_UST_HAT - 1.5 - 10.0                # 1154,5 giriş bandı rulo ekseni
GB_XB = X_DISK_KENAR + 2.0 + 1.5 + 10.0          # 2520,5 burun (disk kenarına 2 mm)
GB_XT = BANT_X[0] - 2.5 - 1.5 - 10.0             # 2550 tahrik (TP10 bandına 2,5 mm)


def adaptor(nema23=None):
    """TP10'u hatta bağlayan parçalar (bizim üretim). nema23: topping_cad'in gerçek motor katısı (STP-MTR-23079)."""
    GB, GD, GCT, CCT, CD, AS = "F_GIRIS_BANDI", "F_GIRIS_DESTEK", "F_GIRIS_CITI", "F_CIKIS_CITI", "F_CIKIS_DESTEK", "F_ARKA_SAC"
    # ---- 3.1 GİRİŞ BANDI: TOPPING'in 420 mm'lik aktarma bandının yerine 70 mm (disk kenarı 2507 → TP10 bandı 2564) ----
    Y = BANT_UST_HAT; BR, BK = 10.0, 1.5
    RY, XB, XT = GB_RY, GB_XB, GB_XT                     # rulo ekseni 1154,5 · burun 2520,5 · tahrik 2550
    ZA, ZB_ = -345.0, -25.0                              # bant 320 geniş (ürün kayarken arka kenarı −342'ye iner)
    ekle("giris_burun_rulosu", silz(XB, RY, BR, ZA + 3, ZB_ - 3).union(silz(XB, RY, 4.0, -355.0, -15.0)), "celik", GB, grup="RULO_GB_BURUN", yerel=False,
         bom=("Giriş bandı burun rulosu Ø20 × 314 + Ø8 mil", 1, "304 · iki ucta rulman", "disk kenarına 2 mm · eski aktarma bandının burnuyla aynı çap"))
    ekle("giris_tahrik_rulosu", silz(XT, RY, BR, ZA + 3, ZB_ - 3).union(silz(XT, RY, 4.0, -372.0, -15.0)), "celik", GB, grup="RULO_GB_TAHRIK", yerel=False,
         bom=("Giriş bandı tahrik rulosu Ø20 × 314 (kauçuk kaplı)", 1, "304", "arkada GT2 kasnağıyla motora bağlı"))
    ust = kut(XB, XT, Y - BK, Y, ZA, ZB_)
    alt = kut(XB, XT, RY - BR - BK, RY - BR, ZA, ZB_)
    s1 = silz(XB, RY, BR + BK, ZA, ZB_).cut(silz(XB, RY, BR, ZA - 1, ZB_ + 1)).cut(kut(XB, XB + 40, RY - 20, RY + 20, ZA - 1, ZB_ + 1))
    s2 = silz(XT, RY, BR + BK, ZA, ZB_).cut(silz(XT, RY, BR, ZA - 1, ZB_ + 1)).cut(kut(XT - 40, XT, RY - 20, RY + 20, ZA - 1, ZB_ + 1))
    ekle("giris_bandi", ust.union(alt).union(s1).union(s2), "ptfe_bant", GB, yerel=False,
         bom=("Giriş bandı · PTFE kaplı cam elyaf 1,5 mm · sonsuz", 1, "320 × ≈ 130", "üst yüz 1166 = TP10 bandı (kot aynı)"))
    ekle("giris_tasiyici_sac", kut(XB + 12.0, XT - 12.0, Y - BK - 4.0, Y - BK - 1.0, ZA + 5, ZB_ - 5), "sac", GB, yerel=False)
    for i, (a, b) in enumerate(((-355.0, -350.0), (-20.0, -15.0))):
        ekle("giris_yan_saci_%d" % i, kut(X_DISK_KENAR + 2.0, BANT_X[0] - 2.0, RY - 18.0, RY + 5.5, a, b)
             .cut(silz(XB, RY, 4.2, a - 1, b + 1)).cut(silz(XT, RY, 4.2, a - 1, b + 1)), "sac", GB, yerel=False,
             bom=("Giriş bandı yan sacı 5 mm (rulman yuvalı)", 2, "304 lazer", "") if i == 0 else None)
    # motor: STP-MTR-23079 (gerçek STEP) tahrik rulosunun ÜSTÜNDE, arkada · GT2 1:1 kasnak (Ø15)
    MX, MY, MZF = XT, 1206.0, -368.0
    if nema23 is not None:
        ekle("giris_bandi_motoru", cq.Workplane(obj=nema23.translate(cq.Vector(MX, MY, MZF))), "motor", GB, yerel=False, kaynak="STP-MTR-23079 GERÇEK CAD",
             bom=("Giriş bandı motoru · NEMA23 STP-MTR-23079", 1, "1,95 N·m kapalı çevrim", "GERÇEK CAD · GT2 1:1 → 115 dev/dk = 0,12 m/s"))
    # L plaka: bandın üstünde (y > 1170) geniş, altında TP10 rulo sarımından (x ≥ 2564) uzak
    ekle("motor_plakasi", kut(MX - 30.0, MX + 30.0, 1170.0, MY + 30.0, MZF, MZF + 3.0).union(kut(MX - 30.0, BANT_X[0] - 3.0, RY - 18.0, 1170.0, MZF, MZF + 3.0))
         .cut(silz(MX, MY, 20.0, MZF - 1, MZF + 4)).cut(silz(XT, RY, 4.5, MZF - 1, MZF + 4)),
         "sac", GB, yerel=False, bom=("Motor plakası 3 mm", 1, "304 lazer", "yan saca iki takozla"))
    ekle("motor_takozu", kut(XB + 1.0, XT - 10.0, RY - 17.0, RY - 7.0, -365.0, -355.0), "sac", GB, yerel=False)
    ekle("kasnak_rulo", silz(XT, RY, 7.5, -364.0, -356.0).cut(silz(XT, RY, 4.1, -365.0, -355.0)), "aluminyum", GB, grup="RULO_GB_TAHRIK", yerel=False)
    ekle("kasnak_motor", silz(MX, MY, 7.5, -364.0, -356.0), "aluminyum", GB, yerel=False)
    kay = cq.Workplane("XY", origin=((XT + MX) / 2.0, (RY + MY) / 2.0, -364.0)).slot2D(math.hypot(MX - XT, MY - RY) + 17.0, 17.0, math.degrees(math.atan2(MY - RY, MX - XT))).extrude(8.0)
    kay = kay.cut(cq.Workplane("XY", origin=((XT + MX) / 2.0, (RY + MY) / 2.0, -365.0)).slot2D(math.hypot(MX - XT, MY - RY) + 15.0, 15.0, math.degrees(math.atan2(MY - RY, MX - XT))).extrude(10.0))
    ekle("gt2_kayis", kay, "koyu", GB, yerel=False, bom=("GT2 kayış 6 mm", 1, "kauçuk", "1:1"))
    # bağlantı: iki L konsolla TOPPING'in çıkış çerçevesine (x 2492–2498,5 · y 1152–1210 · z −325…−15) — eski aktarma bandı gibi
    # TOPPING tarafında taşınır; disk aktarma konumunda (kenar 2507, z −223…−117 kirişi) konsollara değmez.
    ekle("konsol_on", kut(2498.5, X_DISK_KENAR + 2.0, 1152.0, 1160.0, -20.0, -15.0), "sac", GB, yerel=False,
         bom=("Giriş bandı konsolu 5 mm (L)", 2, "304", "TOPPING çıkış çerçevesinin dış yüzüne cıvatalı"))
    ekle("konsol_arka", kut(2498.5, X_DISK_KENAR + 2.0, 1152.0, 1160.0, -355.0, -320.0), "sac", GB, yerel=False)
    # ---- 3.2 GİRİŞ DESTEK SACI: ürünün TP10 bandından önde taşan kenarını taşır (bant başı → gövde) ----
    ekle("giris_destek_saci", kut(BANT_X[0] + 2.0, GOV_X[0] - 2.0, Y - 2.0, Y, -80.0, -12.0), "sac", GD, yerel=False,
         bom=("Giriş destek sacı 2 mm PTFE kaplı", 1, "304", "üstü 1166 = bant · ürün çitle geri itilirken ön kenarı burada kayar"))
    for i, x in enumerate((2640.0, 2730.0)):
        ekle("giris_destek_takozu_%d" % i, kut(x - 10.0, x + 10.0, YG0 + RAY_Y[1], Y - 2.0, -84.0, -79.0), "sac", GD, yerel=False)
    # ---- 3.3 GİRİŞ ÇİTİ (POM, 20°): ürünü −170'ten −249'a iter · 1 mm bant üstü, 25 yüksek ----
    nx_, nz_ = math.sin(math.radians(20.0)), math.cos(math.radians(20.0))
    pts = [GC_A, GC_B, (GC_B[0] + 10 * nx_, GC_B[1] + 10 * nz_), (GC_A[0] + 10 * nx_, GC_A[1] + 10 * nz_)]
    ekle("giris_citi", prizma_xz(pts, Y + 1.0, Y + 26.0), "pom", GCT, yerel=False,
         bom=("Giriş çiti 20° · UHMW-PE / POM 10 × 25", 1, "gıda", "ürünü 79 mm arkaya iter: fırında ön kenar −99, tünel ön duvarına 20 mm"))
    for i, x in enumerate((2650.0, 2740.0)):
        zl = GC_A[1] - (x - 8.0 - GC_A[0]) * TAN20 + 10.0 / nz_           # çitin ön yüzü konsolun SOL kenarında (en önde)
        ekle("giris_citi_konsolu_%d" % i, kut(x - 8.0, x + 8.0, Y, Y + 26.0, zl, min(-12.5, zl + 12.0)), "sac", GCT, yerel=False)
    # ---- 3.4 ÇIKIŞ ÇİTİ (POM, 20°): ürünü −249'dan −170'e geri iter (K bandı + bıçak ekseni) ----
    pts = [CC_A, CC_B, (CC_B[0] + 10 * nx_, CC_B[1] - 10 * nz_), (CC_A[0] + 10 * nx_, CC_A[1] - 10 * nz_)]
    ekle("cikis_citi", prizma_xz(pts, Y + 1.0, Y + 26.0), "pom", CCT, yerel=False,
         bom=("Çıkış çiti 20° · UHMW-PE / POM 10 × 25", 1, "gıda", "ürünü 79 mm öne alır: K'ye hat ekseninde (−170) girer"))
    for i, x in enumerate((3810.0, 3890.0, 3965.0)):
        zl = CC_A[1] + (x - 8.0 - CC_A[0]) * TAN20 - 10.0 / nz_           # çitin arka yüzü kolun SOL kenarında (en geride)
        ekle("cikis_citi_dikmesi_%d" % i, kut(x - 8.0, x + 8.0, YG0 + RAY_Y[1], Y + 26.0, -484.0, -476.0), "sac", CCT, yerel=False)
        ekle("cikis_citi_kolu_%d" % i, kut(x - 8.0, x + 8.0, Y + 16.0, Y + 26.0, -476.0, zl), "sac", CCT, yerel=False)
    # ---- 3.5 ÇIKIŞ DESTEK SACI: ürün öne alınırken bandın önünden taşan kenarı taşır (gövde → K) ----
    ekle("cikis_destek_saci", kut(GOV_X[1] + 2.0, BANT_X[1] - 2.0, Y - 2.0, Y, -80.0, -12.0), "sac", CD, yerel=False,
         bom=("Çıkış destek sacı 2 mm PTFE kaplı", 1, "304", "üstü 1166 · K bandına (1164) 2 mm iner"))
    for i, x in enumerate((3830.0, 3930.0)):
        ekle("cikis_destek_takozu_%d" % i, kut(x - 10.0, x + 10.0, YG0 + RAY_Y[1], Y - 2.0, -84.0, -79.0), "sac", CD, yerel=False)
    # ---- 3.6 F ARKA SACI (istasyon = kapalı ürün): fırının arkası, hava hattının arkasında ----
    ekle("f_arka_saci", kut(2500.0, 4000.0, YG0, YG1 + 10.0, -830.0, -828.5), "sac", AS, yerel=False,
         bom=("F arka sacı 1,5 mm", 1, "304", "956–1483 · hava ana hattı önünde kalır"))


BIRIMLER = [
    ("F_TP10_GOVDE", "Sveba Dahlen TP10 gövdesi · kızılötesi üst + alt (2 bölge) · ısıtılan ≈892 · ağız 85 · ekran + uç kutuları arkada · 9,5 kW · 160 kg (katalog)"),
    ("F_TP10_KONVEYOR", "TP10 konveyörü · paslanmaz tel örgü bant 381 × 1450 · bant üstü 1166 · uç ruloları + raylar (VARSAYIM)"),
    ("F_GIRIS_BANDI", "Giriş bandı (bizim) · TOPPING'in 420'lik aktarma bandının yerine 70 mm · Ø20 burun + tahrik · NEMA23 + GT2 · PTFE bant 320"),
    ("F_GIRIS_DESTEK", "Giriş destek sacı (bizim) · ürünün bantten taşan ön kenarını taşır · 1166"),
    ("F_GIRIS_CITI", "Giriş çiti (bizim) · 20° POM · ürünü −170 → −249 (TP10 bant ekseni −283)"),
    ("F_CIKIS_CITI", "Çıkış çiti (bizim) · 20° POM · ürünü −249 → −170 (K bıçak ekseni)"),
    ("F_CIKIS_DESTEK", "Çıkış destek sacı (bizim) · öne alınan ürünün ön kenarını taşır · 1166"),
    ("F_ARKA_SAC", "F arka sacı (bizim) · 1,5 mm · 956–1483"),
]


def dunya(p):
    """parçanın DÜNYA (hat) katısı"""
    sh = p["wp"].val() if isinstance(p["wp"], cq.Workplane) and len(p["wp"].vals()) == 1 else cq.Compound.makeCompound([o for o in p["wp"].vals() if isinstance(o, cq.Shape)])
    return sh.translate(cq.Vector(*YER)) if p["yerel"] else sh


def kur(ayak=False, plaka=False, uyarla=True):
    PARCALAR[:] = []
    firin(ayak=ayak, plaka=plaka)
    if uyarla:
        import topping_cad_v23 as _TC
        adaptor(_TC.nema23()["govde"])
    return PARCALAR


# ================================================================ 4 · TEK BAŞINA TP10 (katalog hali: ayaklı + çıkış plakalı) ================================================================
def ag(wp, tol=0.5, aci=0.6):
    import kiyma_cad_v6 as _K
    return _K.ag(wp, tol, aci)


def glb_yaz(yol, parcalar):
    """yalnız kullanılan malzemeleri yazan sade GLB (dokusuz)"""
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
    g = {"asset": {"version": "2.0", "generator": "AUTOKITCH firin_tp10_cad_v1"}, "scene": 0, "scenes": [{"nodes": list(range(len(nodes)))}], "nodes": nodes,
         "meshes": meshes, "materials": mats, "accessors": accs, "bufferViews": views, "buffers": [{"byteLength": len(bb)}]}
    js = json.dumps(g, separators=(",", ":")).encode("utf-8")
    while len(js) % 4: js += b" "
    with open(yol, "wb") as f:
        f.write(struct.pack("<4sII", b"glTF", 2, 12 + 8 + len(js) + 8 + len(bb))); f.write(struct.pack("<I4s", len(js), b"JSON")); f.write(js)
        f.write(struct.pack("<I4s", len(bb), b"BIN\x00")); f.write(bb)
    return len(bb) + len(js)


if __name__ == "__main__":
    import time, json
    import kaset_3d_v3 as K3
    t0 = time.time()
    ps = kur(ayak=True, plaka=True, uyarla=False)
    gecersiz = [p["ad"] for p in ps if not p["wp"].val().isValid()]
    print("TP10 · %d parça · katı denetimi: %s" % (len(ps), "hepsi geçerli" if not gecersiz else "GEÇERSİZ %s" % gecersiz)); assert not gecersiz
    bb = cq.Compound.makeCompound([p["wp"].val() for p in ps]).BoundingBox()
    print("ZARF (katalog hali): x %.0f…%.0f (%.0f) · y %.0f…%.0f · z %.0f…%.0f" % (bb.xmin, bb.xmax, bb.xlen, bb.ymin, bb.ymax, bb.zmin, bb.zmax))
    ton = {}
    for p in ps:
        ton.setdefault((p["mal"], p["birim"]), Mesh()).ekle(ag(p["wp"]))
    parca = [("TP10__%s__%s" % (b, m), msh, m) for (m, b), msh in sorted(ton.items())]
    # model-viewer görünümü: ekranlı yüz izleyiciye dönük olsun (Y ekseninde 180°)
    for _a, msh, _m in parca:
        msh.P = [(-q[0], q[1], -q[2] - D_TP * MM) for q in msh.P]; msh.N = [(-n[0], n[1], -n[2]) for n in msh.N]
    yol = os.path.join(KOK, "otonom", "hat3d", "firin_tp10_v1.glb")
    b1 = glb_yaz(yol, parca)
    _dk = {"ad": K3.doku_ad("SVEBA DAHLEN TP10", "katalog fırını · AUTOKITCH denemesi"), "montaj": K3.doku_ad("TP10", "ayrı sürüm", ok_sol=False)}   # USD tüm malzemeleri yazıyor: etiket dokuları bulunmalı
    b2, prim, sorun, _u = K3.usdz_yaz([yol.replace(".glb", ".usdz")], "firin_tp10_v1", parca, _dk)
    print("firin_tp10_v1.glb %.0f KB · usdz %.0f KB · %d prim · USD: %s · %.0f sn" % (b1 / 1024.0, b2 / 1024.0, prim, "GEÇTİ" if not sorun else sorun, time.time() - t0))
    print("ÇİTLER: giriş %s → %s · çıkış %s → %s" % (tuple(round(v, 1) for v in GC_A), tuple(round(v, 1) for v in GC_B), tuple(round(v, 1) for v in CC_A), tuple(round(v, 1) for v in CC_B)))
    for x in (2400, 2520, 2560, 2650, 2757, 2800, 3300, 3760, 3850, 3940, 3975, 4000):
        print("   ürün merkezi x %4d → z %.1f" % (x, urun_z(x)))
    sys.stdout.flush(); os._exit(0)
