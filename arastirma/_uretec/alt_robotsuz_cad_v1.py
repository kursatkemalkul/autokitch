# -*- coding: utf-8 -*-
"""AUTOKITCH · ALTERNATİF A1 · ROBOTSUZ MAKİNE — KAVRAM MODELİ v1 (26 Eyl 2026)

Kemal: "her şey bitince bambaşka bir alternatif oluştur — sen olsan ne yapardın, nasıl tasarlardın; yeni bir 3B model yap."

TEZ: ROBOTU KALDIR. Bugünkü hatta tek Fairino FR5 + 4,9 m yer rayı üç iş yapıyor: (1) çekmeceden hamur topunu açıcıya taşır,
(2) kutuyu kutu modülünden QR dolabına taşır, (3) içecek/tatlıyı dolaba koyar. Sim ölçümü: hattın darboğazı robot (41–55 ürün/saat).
Robot + ray + koridor + karşıdaki QR dolabı yerine bu üç işi, her biri 1–3 eksenli, standart parçalı ÜÇ BASİT MAKİNE yapar:
  1 · TOP OTOMATI (B'nin yerine, aynı gövde 2500 × 830 × 1060): çekmece yok. 6 kat × 5 şerit = 30 bantlı top şeridi
      (vending makinelerindeki bantlı şerit gibi), sol uçta 2 eksenli ASANSÖR topu şeritten alır, B'nin tavanındaki kapaktan
      açıcının sol boşluğuna çıkarır, İTİCİ topu tablaya sürer. Soğuk bölmede; operatör kapağı açıp şeritleri önden doldurur.
  2 · ÇIKIŞ ÇATALI (kutu modülünün önünde): robotun çatalının aynı hareketi, sabit 2 eksen (igus eksen z + SMC kaldırma).
  3 · DÖNER TESLİM DOLABI (kutu modülünün önünde, 830 × 820 × 2030): 8 raflı dikey döner raf (paternoster). Kutu arka kolda
      yüklenir, raf yukarı çıkarken üstteki soğuk İÇECEK OTOMATI (spiral) kutuyu rafın bardaklığına bırakır; raf ön kolda
      müşteri kapağının önüne iner (QR ile açılır).
Açıcı (A), TOPPING (C), fırın (F), kesme (K) ve kutu (E) AYNEN kalır — bu dosya yalnız yeni parçaları çizer.

KOORDİNAT: HAT (hat_montaj ile aynı) — x 0 hattın sol ucu, y yerden, z 0 makinenin ön yüzü (+z koridor/dükkân tarafı).
Bu bir KAVRAM modelidir: ölçüler hesaplı, parça tipleri standart sınıfı; ayrıntılı üretim modeli onaydan sonra.
"""
import math, os, sys
import cadquery as cq

U = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, U)
import kutu_cad_v3 as KC
kut, silx, sily, silz = KC.kut, KC.silx, KC.sily, KC.silz

# ---------------------------------------------------------------- ÖLÇÜLER ----------------------------------------------------------------
H_B, Y_ALT, DZ = 1060.0, 123.0, 830.0
X_A_TABLA, Z_T, Y_DISK = 350.0, -170.0, 1168.0      # açıcının altındaki tabla merkezi, ekseni, çalışma diski üstü [K: montaj v45]
PU = 60.0
# top otomatı
X_SERIT = (205.0, 1985.0)                          # şerit boyu 1780
Z_SERIT = [-120.0 - 62.0 - 124.0 * i for i in range(5)]   # 5 şerit ekseni (z −182 … −678)
KATLAR = [("pide", 205.0, 130.0), ("pide", 335.0, 130.0), ("lahm", 465.0, 110.0), ("lahm", 575.0, 110.0), ("lahm", 685.0, 110.0), ("lahm", 795.0, 110.0)]
TOP = {"pide": (98.0, 105.0), "lahm": (71.0, 78.0)}  # top çapı · şeritteki adım [H: pide Ø280×8 → 493 ml → Ø98 · lahmacun Ø280×3 → 185 ml → Ø71]
X_ASANSOR = 125.0                                  # asansör kabının x ekseni (sol uç boşluğu 62–190)
Y_ASANSOR = (190.0, 1172.0)                        # kap: en alt şerit → tabla kotu
Z_KAPAK = Z_T                                      # B tavanındaki top kapağı tabla ekseninde
# çıkış çatalı + döner dolap
X_E = 4600.0
X_CATAL = ((157.0, 183.0), (247.0, 273.0), (337.0, 363.0))   # kutu modülündeki tepsi aralıkları (E yereli) [K: kutu_cad_v3]
Y_CATAL = (1094.0, 1102.0)
ZC_ICERI, ZC_DISARI = 64.0, 520.0                  # çatal arabasının z'si: dişler kutunun altında · kutu dolabın arka rafında
DOLAP_Z = (0.0, 820.0)
PAT_Z = (250.0, 620.0)                             # paternoster arka kol (yükleme) · ön kol (müşteri)
PAT_Y = (330.0, 1450.0)                            # alt ve üst dişli ekseni
N_RAF = 8

PARCALAR = []


def ekle(ad, wp, mal, grup="SABIT", not_=""):
    assert all(p["ad"] != ad for p in PARCALAR), ad
    PARCALAR.append(dict(ad=ad, wp=wp, mal=mal, grup=grup, not_=not_))


def kure(x, y, z, r):
    return cq.Workplane(obj=cq.Solid.makeSphere(r, cq.Vector(x, y, z), angleDegrees1=-90, angleDegrees2=90))


# ---------------------------------------------------------------- 1 · TOP OTOMATI ----------------------------------------------------------------
def top_otomati():
    # gövde: sandviç kabuk (PU 60) — çekmece kolonları yok, şeritler 1780 boyunca açık
    ekle("B1_taban", kut(0, 2500, Y_ALT, Y_ALT + PU, -DZ, -40.0), "pu", not_="alt PU 60")
    ekle("B1_tavan", kut(0, 2500, H_B - PU, H_B, -DZ, -40.0).cut(kut(X_ASANSOR - 60, X_ASANSOR + 60, H_B - PU - 1, H_B + 1, Z_KAPAK - 60, Z_KAPAK + 60)), "pu",
         not_="üst PU 60 · asansör kapağı 120 × 120 (yaylı klape)")
    ekle("B1_arka", kut(0, 2500, Y_ALT + PU, H_B - PU, -DZ, -DZ + PU), "pu")
    ekle("B1_sol", kut(0, PU, Y_ALT + PU, H_B - PU, -DZ + PU, -40.0), "pu")
    ekle("B1_sag", kut(2500 - PU, 2500, Y_ALT + PU, H_B - PU, -DZ + PU, -40.0), "pu")
    ekle("B1_teknik_bolme", kut(1995.0, 2011.0, Y_ALT + PU, H_B - PU, -DZ + PU, -40.0), "sac", not_="K4 teknik kolonu (Secop + pano + kaşar/sucuk deposu) aynen")
    for i, (x0, x1) in enumerate(((0.0, 698.5), (701.5, 1353.5), (1356.5, 2008.5), (2011.5, 2500.0))):
        ekle("B1_kapak_%d" % i, kut(x0, x1, 126.0, 1057.0, -40.0, 0.0), "kapak", not_="tam kaplayan kapak (menteşeli) · şeritleri önden doldurmak için")
    for i, x in enumerate((60.0, 1250.0, 2440.0)):
        for z in (-110.0, -770.0):
            ekle("B1_ayak_%d_%d" % (i, int(-z)), sily(x, z, 20.0, 0.0, Y_ALT), "celik")
    # 30 şerit: tepsi + bant + tahrik (sağ uçta)
    for k, (tip, y, _p) in enumerate(KATLAR):
        d, adim = TOP[tip]
        for j, z in enumerate(Z_SERIT):
            ekle("serit_%d_%d_tepsi" % (k, j), kut(X_SERIT[0], X_SERIT[1], y - 26.0, y - 3.0, z - 58.0, z + 58.0).cut(kut(X_SERIT[0] - 1, X_SERIT[1] + 1, y - 23.0, y, z - 56.0, z + 56.0)), "sac")
            ekle("serit_%d_%d_bant" % (k, j), kut(X_SERIT[0] + 5.0, X_SERIT[1] - 5.0, y - 3.0, y, z - 52.0, z + 52.0), "pu_bant")
            ekle("serit_%d_%d_motor" % (k, j), kut(X_SERIT[1] - 40.0, X_SERIT[1], y - 70.0, y - 26.0, z - 20.0, z + 20.0), "motor",
                 not_="şerit redüktörlü motoru 24 V (vending sınıfı) [V]")
            n = int((X_SERIT[1] - X_SERIT[0] - 30.0) // adim)
            for m in range(n):
                ekle("top_%d_%d_%d" % (k, j, m), kure(X_SERIT[0] + 20.0 + adim / 2.0 + m * adim, y + d * 0.41, z, d / 2.0), "hamur", "TOPLAR")
    # asansör: dikey igus ekseni (arkada) + yatay z ekseni + kap
    ekle("asansor_dikey_eksen", kut(X_ASANSOR - 55.0, X_ASANSOR - 15.0, Y_ALT + PU, 1300.0, -792.0, -752.0), "aluminyum",
         not_="igus drylin ZLW-1040 dikey · strok 1000 [V]")
    ekle("asansor_z_ekseni", kut(X_ASANSOR - 15.0, X_ASANSOR + 15.0, -40.0, -20.0, -752.0, -90.0), "aluminyum", "ASANSOR", "igus ZLW-0630 yatay · strok 560 [V]")
    ekle("asansor_arabasi", kut(X_ASANSOR - 55.0, X_ASANSOR + 15.0, -60.0, 0.0, -792.0, -740.0), "aluminyum", "ASANSOR")
    ekle("asansor_kabi", sily(X_ASANSOR, 0.0, 55.0, -6.0, 0.0).union(sily(X_ASANSOR, 0.0, 55.0, 0.0, 14.0).cut(sily(X_ASANSOR, 0.0, 52.0, -1.0, 15.0)).cut(kut(X_ASANSOR, X_ASANSOR + 60.0, -1.0, 15.0, -60.0, 60.0))),
         "pom", "KAP", "kap: ön yarısı açık (itici topu tablaya sürer)")
    # tablaya itici (A'nın sol boşluğunda, açıcı kafa plakasının altında)
    ekle("itici_eksen", kut(20.0, 305.0, 1275.0, 1300.0, Z_T - 20.0, Z_T + 20.0), "aluminyum", not_="mini lineer eksen strok 230 [V]")
    ekle("itici_kolu", kut(0.0, 12.0, 1180.0, 1275.0, Z_T - 45.0, Z_T + 45.0), "pom", "ITICI")
    ekle("B1_secop_teknik_REF", kut(2011.5, 2440.0, Y_ALT + PU, 460.0, -770.0, -60.0), "referans", not_="K4: Secop CU KLF4.0CND + pano (store_cad_v5 ile aynı)")


# ---------------------------------------------------------------- 2 · ÇIKIŞ ÇATALI ----------------------------------------------------------------
def cikis_catali():
    for i, (a, b) in enumerate(X_CATAL):
        ekle("catal_disi_%d" % i, kut(X_E + a, X_E + b, Y_CATAL[0], Y_CATAL[1], ZC_ICERI - 430.0, ZC_ICERI), "celik", "CATAL")
    ekle("catal_govdesi", kut(X_E + 140.0, X_E + 380.0, 1080.0, 1112.0, ZC_ICERI, ZC_ICERI + 16.0), "celik", "CATAL")
    ekle("catal_kaldirma_MGPM", kut(X_E + 230.0, X_E + 290.0, 1040.0, 1080.0, ZC_ICERI + 16.0, ZC_ICERI + 70.0), "aluminyum", "CATAL", "SMC MGPM16-60 · 55 mm kaldırma [V]")
    ekle("catal_z_ekseni", kut(X_E + 240.0, X_E + 280.0, 1000.0, 1040.0, 20.0, 800.0), "aluminyum", not_="igus ZLW-1040 · strok 456 [V]")
    ekle("catal_motoru", kut(X_E + 238.0, X_E + 282.0, 978.0, 1034.0, 800.0, 876.0), "motor", not_="NEMA 23 (kutu modülüyle aynı)")


# ---------------------------------------------------------------- 3 · DÖNER TESLİM DOLABI + İÇECEK OTOMATI ----------------------------------------------------------------
def pat_yol(s):
    """paternoster zinciri üstünde yay uzunluğu s → (y, z) · arka kol yukarı, üstten öne, ön kol aşağı, alttan arkaya"""
    y0, y1 = PAT_Y; za, zo = PAT_Z; r = (zo - za) / 2.0; zc = (za + zo) / 2.0
    L_d = y1 - y0; L_y = math.pi * r; L = 2 * L_d + 2 * L_y
    s = s % L
    if s < L_d: return (y0 + s, za)
    s -= L_d
    if s < L_y: a = s / r; return (y1 + r * math.sin(a), zc - r * math.cos(a))
    s -= L_y
    if s < L_d: return (y1 - s, zo)
    s -= L_d
    a = s / r; return (y0 - r * math.sin(a), zc + r * math.cos(a))


def pat_boy():
    return 2 * (PAT_Y[1] - PAT_Y[0]) + math.pi * (PAT_Z[1] - PAT_Z[0])


def teslim_dolabi():
    x0, x1 = X_E, X_E + 830.0
    ekle("dolap_sol", kut(x0, x0 + 20.0, Y_ALT, 2030.0, DOLAP_Z[0] + 20.0, DOLAP_Z[1]), "kapak")
    ekle("dolap_sag", kut(x1 - 20.0, x1, Y_ALT, 2030.0, DOLAP_Z[0] + 20.0, DOLAP_Z[1]), "kapak")
    ekle("dolap_ust", kut(x0, x1, 2010.0, 2030.0, DOLAP_Z[0] + 20.0, DOLAP_Z[1]), "kapak")
    on = kut(x0, x1, Y_ALT, 2030.0, DOLAP_Z[1] - 20.0, DOLAP_Z[1]).cut(kut(x0 + 180.0, x1 - 180.0, 980.0, 1380.0, DOLAP_Z[1] - 21.0, DOLAP_Z[1] + 1.0))
    ekle("dolap_on_yuz", on, "kapak", not_="müşteri yüzü · kapak 470 × 400 · QR okuyucu")
    ekle("dolap_musteri_kapagi", kut(x0 + 180.0, x1 - 180.0, 980.0, 1380.0, DOLAP_Z[1] - 20.0, DOLAP_Z[1] - 4.0), "pc", not_="QR ile açılan kapak (kilitli)")
    ekle("dolap_QR_okuyucu", kut(x1 - 150.0, x1 - 60.0, 1180.0, 1280.0, DOLAP_Z[1], DOLAP_Z[1] + 25.0), "siyah")
    ekle("dolap_arka_yukleme_acikligi_REF", kut(x0 + 100.0, x1 - 100.0, 1080.0, 1320.0, DOLAP_Z[0], DOLAP_Z[0] + 20.0), "referans", not_="kutu modülünün ağzına bakan açıklık")
    for i, x in enumerate((x0 + 60.0, x1 - 60.0)):
        for j, y in enumerate(PAT_Y):
            ekle("pat_disli_%d_%d" % (i, j), silx(y, (PAT_Z[0] + PAT_Z[1]) / 2.0, 190.0, x - 8.0, x + 8.0).cut(silx(y, (PAT_Z[0] + PAT_Z[1]) / 2.0, 175.0, x - 9.0, x + 9.0)), "celik")
        ekle("pat_mili_%d" % i, silx(PAT_Y[1], (PAT_Z[0] + PAT_Z[1]) / 2.0, 12.0, x0 + 20.0, x1 - 20.0), "celik") if i == 0 else None
    ekle("pat_motoru", kut(x1 - 20.0, x1 + 0.0, PAT_Y[1] - 40.0, PAT_Y[1] + 40.0, 400.0, 480.0), "motor", not_="redüktörlü motor + fren · raf adımı 1 hamle [V]")
    L = pat_boy()
    for k in range(N_RAF):
        yy, zz = pat_yol(k * L / N_RAF)
        raf = None
        for (a, b) in ((0.0, 155.0), (185.0, 245.0), (275.0, 335.0), (365.0, 420.0)):          # kutu modülünün tepsisi gibi çubuklu (çatal dişleri arada)
            c_ = kut(x0 + 100.0 + a, x0 + 100.0 + b, -12.0, 0.0, -175.0, 175.0)
            raf = c_ if raf is None else raf.union(c_)
        raf = raf.union(kut(x0 + 540.0, x0 + 680.0, -12.0, 0.0, -80.0, 80.0)).union(sily(x0 + 610.0, 0.0, 44.0, 0.0, 40.0).cut(sily(x0 + 610.0, 0.0, 40.0, -1.0, 41.0)))
        raf = raf.union(kut(x0 + 60.0, x0 + 100.0, -12.0, 60.0, -30.0, 30.0)).union(kut(x1 - 100.0, x1 - 60.0, -12.0, 60.0, -30.0, 30.0))
        ekle("raf_%d" % k, raf, "aluminyum", "RAF_%d" % k, "çubuklu raf + içecek bardaklığı · askıda (hep yatay)")
    # içecek otomatı (soğuk, üstte)
    ekle("icecek_otomati_kabuk", kut(x0 + 20.0, x1 - 20.0, 1680.0, 2010.0, 30.0, 640.0), "kabin", not_="soğuk içecek otomatı · 3 spiral tepsi × 6 spiral × 10 kutu = 180 ≥ 2 gün 160 [V] · tatlı 30 ayrı tepside [V]")
    for i, y in enumerate((1710.0, 1810.0, 1910.0)):
        for j in range(6):
            xs = x0 + 100.0 + j * 110.0
            ekle("spiral_%d_%d" % (i, j), silz(xs, y + 45.0, 40.0, 60.0, 600.0).cut(silz(xs, y + 45.0, 36.0, 59.0, 601.0)), "celik")
    ekle("icecek_olugu", kut(x0 + 540.0, x0 + 680.0, 1480.0, 1680.0, 150.0, 350.0).cut(kut(x0 + 550.0, x0 + 670.0, 1479.0, 1681.0, 160.0, 340.0)), "sac", not_="kutu → rafın bardaklığı")
    ekle("sogutma_REF", kut(x0 + 20.0, x1 - 20.0, Y_ALT, 300.0, 30.0, 800.0), "referans", not_="soğutma grubu + pano (dolap tabanı)")


def modul():
    PARCALAR[:] = []
    top_otomati(); cikis_catali(); teslim_dolabi()
    return PARCALAR


# ---------------------------------------------------------------- KİNEMATİK (30 s gösterim döngüsü) ----------------------------------------------------------------
DONGU = 30.0
ss = KC.ss
SEC = (2, 2)                                        # gösterimde topu veren şerit: kat 2 (lahmacun), şerit 2


def kap_konum(t):
    """kap (x sabit): (y, z) — şerit ucunda top alır, arka kolda kalkar, kapaktan tabla kotuna çıkar"""
    k, j = SEC; y_s = KATLAR[k][1] + 2.0; z_s = Z_SERIT[j]
    y_ust, y_bekle = Y_ASANSOR[1] - 8.0, 150.0 + Y_ALT + PU
    if t < 1.0: y = y_bekle + (y_s - 30.0 - y_bekle) * ss(0.0, 1.0, t); z = z_s * ss(0.0, 1.0, t) + (-400.0) * (1 - ss(0.0, 1.0, t))
    elif t < 2.2: y, z = y_s - 30.0, z_s
    elif t < 3.2: y = y_s - 30.0; z = z_s + (Z_KAPAK - z_s) * ss(2.2, 3.2, t)
    elif t < 5.0: y = y_s - 30.0 + (y_ust - (y_s - 30.0)) * ss(3.2, 5.0, t); z = Z_KAPAK
    elif t < 6.2: y, z = y_ust, Z_KAPAK
    elif t < 8.0: y = y_ust + (y_bekle - y_ust) * ss(6.2, 8.0, t); z = Z_KAPAK + (-400.0 - Z_KAPAK) * ss(6.2, 8.0, t)
    else: y, z = y_bekle, -400.0
    return y, z


def top_konum(t):
    """gösterim topu: şeridin ucundan kaba düşer, kapla çıkar, itici tablaya sürer, sonra açıcıda kalır"""
    k, j = SEC; d = TOP[KATLAR[k][0]][0]
    y_s = KATLAR[k][1]; z_s = Z_SERIT[j]
    if t < 1.0: return (X_SERIT[0] + 20.0 + TOP[KATLAR[k][0]][1] / 2.0, y_s + d * 0.41, z_s)
    if t < 2.0:
        u = ss(1.0, 2.0, t); return (X_SERIT[0] + 20.0 + TOP[KATLAR[k][0]][1] / 2.0 - (X_SERIT[0] + 20.0 + 40.0 - X_ASANSOR) * u, y_s + d * 0.41 - 30.0 * u, z_s)
    y, z = kap_konum(t)
    if t < 6.2: return (X_ASANSOR, y + d * 0.41 + 2.0, z)
    if t < 7.2:
        u = ss(6.2, 7.2, t); return (X_ASANSOR + (X_A_TABLA - X_ASANSOR) * u, Y_DISK + d * 0.41 + 2.0, Z_T)
    return (X_A_TABLA, Y_DISK + d * 0.41 + 2.0, Z_T)


def itici_dx(t):
    return (X_A_TABLA - d_top() / 2.0 - 12.0) * (ss(6.2, 7.2, t) - ss(7.4, 8.4, t))


def d_top():
    return TOP[KATLAR[SEC[0]][0]][0]


def catal_trs(t):
    """çıkış çatalı: 12 s'de içeri, kaldırır, dolabın arka rafına taşır, bırakır, döner"""
    dz = (ZC_DISARI - ZC_ICERI)
    z = dz * (1.0 - ss(12.0, 13.5, t)) + dz * ss(14.3, 16.3, t) - dz * ss(17.3, 18.8, t) + dz * ss(17.3, 18.8, t) * 0.0
    if t < 12.0: z = dz
    elif t < 13.5: z = dz * (1.0 - ss(12.0, 13.5, t))
    elif t < 14.3: z = 0.0
    elif t < 16.3: z = dz * ss(14.3, 16.3, t)
    else: z = dz
    y = 55.0 * (ss(13.5, 14.3, t) - ss(16.3, 16.9, t))
    return (0.0, y, z)


def kutu_trs(t):
    """kapalı kutu (kutu modülünün tepsisinde, E yereli z −206) → çatalla dolabın arka rafına → raf döner"""
    if t < 13.5: return (0.0, 0.0, 0.0)
    c = catal_trs(min(t, 16.3))
    if t < 16.9: return (0.0, c[1], c[2])
    y_r, z_r = raf_konum(t, RAF_YUKLE)
    y0, z0 = raf_konum(16.9, RAF_YUKLE)
    return (0.0, c[1] + (y_r - y0), c[2] + (z_r - z0))


RAF_YUKLE = 1                                          # gösterimde yüklenen raf


def raf_s(t):
    """zincir ilerlemesi: 17–27 s arası 4 raf adımı (kutu yükleme kotundan içecek oluğuna, oradan müşteri kapağına)"""
    L = pat_boy(); a = L / N_RAF
    return a * 4.0 * ss(17.0, 27.0, t)


def raf_konum(t, k):
    L = pat_boy()
    return pat_yol(k * L / N_RAF + raf_s(t))


def grup_trs(g, t):
    if g == "KAP" or g == "ASANSOR":                    # kap ve araba y 0 / z 0 etrafında çizildi → mutlak konum
        y, z = kap_konum(t)
        return (0.0, y, z if g == "KAP" else 0.0)
    if g == "ITICI": return (itici_dx(t), 0.0, 0.0)
    if g == "CATAL": return catal_trs(t)
    if g.startswith("RAF_"):
        k = int(g[4:]); y, z = raf_konum(t, k); y0, z0 = raf_konum(0.0, k)
        return (0.0, y - y0, z - z0)
    return (0.0, 0.0, 0.0)


if __name__ == "__main__":
    modul()
    n_top = sum(1 for p in PARCALAR if p["ad"].startswith("top_"))
    kap = {}
    for k, (tip, y, _p) in enumerate(KATLAR):
        kap[tip] = kap.get(tip, 0) + sum(1 for p in PARCALAR if p["ad"].startswith("top_%d_" % k))
    print("A1 ROBOTSUZ: %d parca · top otomati %d top (pide %d · lahmacun %d; 2 gun gerek 160 + 432) · raf %d · zincir %.0f mm"
          % (len(PARCALAR), n_top, kap["pide"], kap["lahm"], N_RAF, pat_boy()))
