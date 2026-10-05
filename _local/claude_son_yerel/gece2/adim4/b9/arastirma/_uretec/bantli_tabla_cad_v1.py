# -*- coding: utf-8 -*-
"""
BANTLI TABLA · CAD v1 (28 Eyl 2026 gece) — bantli_tabla_hesap_v1'den OKUR (sayı tek yerde).

ÇIKTILAR
  · otonom/hat/denemeler/bantli-tabla-v2/bantli_tabla_v1.glb  — simülasyon sayfasının modeli (düğüm adı "GRUP__parça")
  · arastirma/_uretec/bantli_tabla_cad_v1.json                  — parça listesi, BOM, kütle, birleşim dökümü, DENETİM sonuçları
  · arastirma/BANTLI_TABLA_v1/BOM_bantli_tabla_v1.csv
  (STEP / STL / montaj STEP ÜRETİLMEZ — kural 6.7 · Kemal 25 Eyl: "SolidWorks için bir şey yapmayacağız")

KOORDİNAT: dünya (mm) x hat boyu (fırına +), y yukarı, z öne (+). Tabla ekseni z = −170.
  KASET / DONER / ROTOR parçaları YEREL çizilir: x_yerel = x − tabla_x, z_yerel = z + 170 (0° = burun fırına bakar).
  ARABA parçaları yerel x (dönmez). ACICI parçaları park eksenine göre yerel (x − 350, z + 170).
  Diğerleri dünyada.

GRUPLAR (GLB düğüm öneki)
  KASET  kaset (elle çıkar) · ROTOR tahrik rotoru (kendi ekseninde döner) · BANT kaset bandı (doku kayar) · GT2 kayış
  DONER  tablayla dönen TOPPING parçaları + yeni pimler · ARABA x arabası (plakası kısaltılmış)
  ACICI  konili açıcı (iner-kalkar, koniler döner) · SABIT değişmeyen bağlam · DEGISIK değişen bağlam (a–f)
  TAHRIK sabit mıknatıslı tahrik (TAHRIK_DISK döner) · YB yükleme bandı (YB_BANT doku kayar) · FIRIN fırın ağzı vekili
"""
import csv, gzip, io, json, math, os, struct, sys, time
import cadquery as cq

U = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, U)
KOK = os.path.dirname(U)
DEPO = os.path.dirname(KOK)
import bantli_tabla_hesap_v1 as H

CIKTI = os.path.join(KOK, "BANTLI_TABLA_v1")
BAGLAM = os.path.join(CIKTI, "baglam")
SAYFA = os.path.join(DEPO, "otonom", "hat", "denemeler", "bantli-tabla-v2")
MOTOR_STEP = os.path.join(KOK, "katalog", "step", "stp-mtr-23079.step")
os.makedirs(SAYFA, exist_ok=True)
T0 = time.time()

# ================================================================ YARDIMCILAR
def kut(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))
def sily(x, z, r, y0, y1):
    return cq.Workplane("XZ").center(x, z).circle(r).extrude(-(y1 - y0)).translate((0, y0, 0))
def silz(x, y, r, z0, z1):
    return cq.Workplane("XY").center(x, y).circle(r).extrude(z1 - z0).translate((0, 0, z0))
def silx(y, z, r, x0, x1):
    return cq.Workplane("YZ").center(y, z).circle(r).extrude(x1 - x0).translate((x0, 0, 0))
def halka_z(x, y, r0, r1, z0, z1):
    return silz(x, y, r1, z0, z1).cut(silz(x, y, r0, z0 - 1, z1 + 1))
def koni_z(x, y, r0, r1, z0, z1):
    """z0'da r0, z1'de r1 (havşa başı)"""
    return cq.Workplane(obj=cq.Solid.makeCone(r0, r1, abs(z1 - z0), cq.Vector(x, y, min(z0, z1)), cq.Vector(0, 0, 1)) if z1 > z0
                        else cq.Solid.makeCone(r1, r0, abs(z1 - z0), cq.Vector(x, y, z1), cq.Vector(0, 0, 1)))

PARCALAR = []
def ekle(ad, grup, wp, mal, bom=None, kaynak=""):
    sh = wp.val() if hasattr(wp, "val") else wp
    assert all(p["ad"] != ad for p in PARCALAR), ad
    PARCALAR.append(dict(ad=ad, grup=grup, sh=sh, mal=mal, bom=bom, kaynak=kaynak))
    return sh

def gt2_kasnak(x, y, z0, z1, dis=20, delik=5.0, flans=0.0):
    """GT2 kasnak: 20 diş, hatve Ø12,73, dış Ø12,22, diş kökü Ø10,70 (2GT profil, sade)."""
    rp = dis * 2.0 / math.pi / 2.0
    r_dis, r_kok = rp - 0.254, rp - 0.254 - 0.76
    pts = []
    for i in range(dis):
        a0 = 2 * math.pi * i / dis
        for k, (da, rr) in enumerate(((0.00, r_dis), (0.30, r_dis), (0.42, r_kok), (0.88, r_kok))):
            a = a0 + da * 2 * math.pi / dis
            pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    w = cq.Workplane("XY").polyline(pts).close().extrude(z1 - z0).translate((0, 0, z0))
    w = w.cut(silz(x, y, delik / 2.0, z0 - 1, z1 + 1))
    if flans > 0:
        w = w.union(halka_z(x, y, delik / 2.0, r_dis + 1.2, z0 - flans, z0)).union(halka_z(x, y, delik / 2.0, r_dis + 1.2, z1, z1 + flans))
    return w

def rulman_z(x, y, d, D, B, z0):
    """bilyalı rulman (iç + dış bilezik + keçe yüzü) — katalog ölçüsü"""
    w = halka_z(x, y, d / 2.0, d / 2.0 + (D - d) * 0.22, z0, z0 + B)
    w = w.union(halka_z(x, y, D / 2.0 - (D - d) * 0.22, D / 2.0, z0, z0 + B))
    w = w.union(halka_z(x, y, d / 2.0 + (D - d) * 0.22, D / 2.0 - (D - d) * 0.22, z0 + 0.3, z0 + B - 0.3))
    return w

def havsa_vida_z(x, y, z_yuz, yon, M=5.0, L=12.0):
    """DIN 7991 havşa başlı vida — baş yüzü z_yuz'da, gövde yon (−1/+1) yönünde L boyunca"""
    dk = {3.0: 6.0, 4.0: 8.0, 5.0: 10.0, 6.0: 12.0}[M]; k = (dk - M) / 2.0 / math.tan(math.radians(45))
    if yon < 0:
        bas = cq.Workplane(obj=cq.Solid.makeCone(M / 2.0, dk / 2.0, k, cq.Vector(x, y, z_yuz - k), cq.Vector(0, 0, 1)))
        gov = silz(x, y, M / 2.0 - 0.45, z_yuz - L, z_yuz - k)
    else:
        bas = cq.Workplane(obj=cq.Solid.makeCone(dk / 2.0, M / 2.0, k, cq.Vector(x, y, z_yuz), cq.Vector(0, 0, 1)))
        gov = silz(x, y, M / 2.0 - 0.45, z_yuz + k, z_yuz + L)
    return bas.union(gov)

def havsa_delik_z(x, y, z_yuz, yon, M=5.0, L=20.0):
    dk = {3.0: 6.4, 4.0: 8.4, 5.0: 10.4, 6.0: 12.4}[M]; k = (dk - M) / 2.0
    if yon < 0:
        return cq.Workplane(obj=cq.Solid.makeCone(M / 2.0 + 0.2, dk / 2.0, k, cq.Vector(x, y, z_yuz - k), cq.Vector(0, 0, 1))).union(silz(x, y, M / 2.0 + 0.2, z_yuz - L, z_yuz))
    return cq.Workplane(obj=cq.Solid.makeCone(dk / 2.0, M / 2.0 + 0.2, k, cq.Vector(x, y, z_yuz), cq.Vector(0, 0, 1))).union(silz(x, y, M / 2.0 + 0.2, z_yuz, z_yuz + L))

# ================================================================ ÖLÇÜLER (hesaptan)
ZE, UST = H.ZE, H.UST
t_b, W_B = H.BANT["t"], H.W_BANT
D_R, Y_R, X_N, X_K, X_UC = H.D_R, H.Y_R, H.X_N, H.X_K, H.X_UC
ZY0, ZY1 = H.Z_YAN                       # 151 / 155
ZG0, ZG1 = H.Z_KILAVUZ                   # 148,5 / 151
YT0, YT1 = H.Y_TABAN                     # 978 / 984
YY0, YY1 = H.Y_YATAK                     # 992,85 / 998,85
XY0, XY1 = H.X_YATAK
TK = H.S["tahrik_kaset"]
X_RO, Y_RO = TK["X_ROTOR"], TK["Y_ROTOR"]
ZK0, ZK1 = TK["Z_KASNAK"]                # −163 / −156
ZRY0, ZRY1 = TK["Z_ROTOR_YATAK"]         # −176 / −164
ZM0, ZM1 = TK["Z_MIKNATIS"]              # −184 / −176,5
D_M = TK["D_MIKNATIS"]
AKT, LB_SOL = H.AKT, H.LB_SOL
X_SUR, Y_SUR = H.X_SUR, H.Y_ROTOR
R_RUL = 5.5                               # SMR115 dış yarıçap (5×11×4)
X_TABAN = (-150.0, 124.0)                 # taban yarık bölgesine (yerel 125,6) girmez
YAN_UST = UST - 0.5                       # yan sac üst kenarı (rulo bosajları hariç)

# ================================================================ 1 · KASET (YEREL)
# --- 1.1 taban sacı (bugünkü göbeğin yerine; ayar bileziğine oturur) ---
tb = kut(X_TABAN[0], X_TABAN[1], YT0, YT1, -ZY0, ZY0)
for sx in (-10.0, 10.0):                                                     # tahrik pimi burçları (lokma pimleri alttan)
    tb = tb.cut(sily(sx, 0.0, 4.05, YT0 - 1, YT1 - 1.0))
PIM_AC = (90.0, 250.0); R_PIM = 75.0
px0, pz0 = R_PIM * math.cos(math.radians(PIM_AC[0])), R_PIM * math.sin(math.radians(PIM_AC[0]))
px1, pz1 = R_PIM * math.cos(math.radians(PIM_AC[1])), R_PIM * math.sin(math.radians(PIM_AC[1]))
tb = tb.cut(sily(px0, pz0, 4.0, YT0 - 1, YT0 + 5.0))                          # yuvarlak konum deliği Ø8 H7
_sl = cq.Workplane("XZ").center(px1, pz1).slot2D(14.0, 8.0, angle=-PIM_AC[1]).extrude(-6.0).translate((0, YT0 - 1, 0))
tb = tb.cut(_sl)                                                              # oval konum deliği (radyal)
for a_ in (40.0, 160.0, 280.0):                                               # açıcı kilit pimi boşluğu (r 92)
    tb = tb.cut(sily(92.0 * math.cos(math.radians(a_)), 92.0 * math.sin(math.radians(a_)), 6.5, YT0 - 1, YT0 + 3.0))
tb = tb.cut(sily(0.0, -128.0, 12.0, YT0 - 1, YT0 + 4.0))                     # tabla home bayrağı cebi (bayrak tepesi 981)
for x0_, x1_ in ((-146.0, -114.0), (112.0, 121.0)):                            # alttan hafifletme cepleri (Ø210 temas dışında)
    tb = tb.cut(kut(x0_, x1_, YT0 - 1, YT0 + 4.0, -ZY0 + 5.0, ZY0 - 5.0))
for zs in (-1.0, 1.0):
    tb = tb.cut(kut(-100.0, 100.0, YT0 - 1, YT0 + 4.0, zs * 112.0 if zs > 0 else -ZY0 + 5.0, ZY0 - 5.0 if zs > 0 else -112.0))
X_VT = (-110.0, 0.0, 90.0)                                                    # yan sac → taban M5 dişleri (kenar) · 90: rotor miline uzak
for xv in X_VT:
    for zs in (-1.0, 1.0):
        tb = tb.cut(silz(xv, (YT0 + YT1) / 2.0, 2.1, zs * ZY0 - (10.0 if zs > 0 else 0.0), zs * ZY0 + (0.0 if zs > 0 else 10.0)))
ekle("taban_saci", "KASET", tb, "celik",
     bom=("Kaset taban sacı 274 × 302 × 6", 1, "AISI 304 · lazer + CNC · alttan 4 mm hafifletme cepleri",
          "bugünkü tabla göbeğinin YERİNE ayar bileziğine (978) oturur · 2 tahrik pimi burcu (r 10) · Ø8 H7 + oval konum deliği (r 75) · açıcı kilit pimi ve home bayrağı cepleri · kenarlarında 6 × M5 diş"),
     kaynak="hesap: Y_TABAN")

# --- 1.2 yatak sacı (açıcı baskısını taşır; bant üstünde kayar) ---
yt = kut(XY0, XY1, YY0, YY1, -ZY0, ZY0)
for xv in (-100.0, 0.0, 90.0):
    for zs in (-1.0, 1.0):
        yt = yt.cut(silz(xv, (YY0 + YY1) / 2.0, 2.1, zs * ZY0 - (10.0 if zs > 0 else 0.0), zs * ZY0 + (0.0 if zs > 0 else 10.0)))
for xv in (-120.0, -40.0, 40.0, 120.0):
    for zs in (-1.0, 1.0):
        yt = yt.cut(sily(xv, zs * (ZG0 + ZG1) / 2.0, 1.25, YY1 - 5.0, YY1 + 1))        # kılavuz M3 dişleri
ekle("yatak_saci", "KASET", yt, "celik",
     bom=("Yatak sacı %.0f × 302 × 6" % (XY1 - XY0), 1, "AISI 316L · iki yüz taşlanmış (Ra ≤ 0,8) · kenar yuvarlatma R1",
          "bandın üst kolu üstünde kayar; açıcının 482 N baskısını iki yan saca taşır · sehim en kötü şerit %.2f mm (hesap)" % H.S["yatak"]["en_kotu_serit_120"]["sehim_mm"]))

# --- 1.3 yan saclar (4 mm, lazer; rulo yatakları, kuyruk kızak penceresi, kaldırma dudağı) ---
def yan_sac(z0, z1, arka):
    w = kut(-150.0, 118.0, YT0, YAN_UST, z0, z1)
    w = w.union(kut(118.0, X_N, 985.9, YAN_UST, z0, z1))                          # burun bölgesi 985,9'un üstünde (fırın ağzı 984, yarık 983)
    w = w.union(silz(X_N, Y_R, 7.0, z0, z1))                                        # burun rulman bosajı R7 (alt 985,85)
    w = w.union(kut(-160.0, -134.0, 983.0, 1002.5, z0, z1))                         # kuyruk kızak çerçevesi
    w = w.cut(kut(X_K - 12.15, X_K + 11.85, Y_R - 8.0, Y_R + 8.0, z0 - 1, z1 + 1))   # kızak penceresi 24 × 16 (kızak ±4 gezer)
    w = w.cut(silz(X_N, Y_R, R_RUL, z0 - 1, z1 + 1))                                # burun rulmanı Ø11 H7
    for xv in X_VT:
        w = w.cut(havsa_delik_z(xv, (YT0 + YT1) / 2.0, z1 if z1 > 0 else z0, 1 if z1 < 0 else -1, 5.0, 4.5))
    for xv in (-100.0, 0.0, 90.0):
        w = w.cut(havsa_delik_z(xv, (YY0 + YY1) / 2.0, z1 if z1 > 0 else z0, 1 if z1 < 0 else -1, 5.0, 4.5))
    if arka:
        w = w.cut(silz(X_RO, Y_RO, 3.0, z0 - 1, z1 + 1))                            # rotor mili deliği (mil kaynaklı)
    # kaldırma dudağı (dışa bükülü tırnak, 10 mm)
    zd = (z1, z1 + 10.0) if z1 > 0 else (z0 - 10.0, z0)
    w = w.union(kut(-45.0, 45.0, YT0, YT0 + 2.0, zd[0], zd[1]))
    return w
ekle("yan_sac_on", "KASET", yan_sac(ZY0, ZY1, False), "celik",
     bom=("Kaset yan sacı ön / arka", 2, "AISI 304 4 mm · lazer + 10 mm kaldırma dudağı abkant",
          "tabana 3 × M5, yatağa 3 × M5 havşa (DIN 7991) · burun rulmanı Ø11 H7 · kuyruk kızak penceresi 30 × 16 · arka sacta rotor mili kulağı"))
ekle("yan_sac_arka", "KASET", yan_sac(-ZY1, -ZY0, True), "celik")

# --- 1.4 kenar kılavuzları (UHMW) ---
for i_, zs in enumerate((-1.0, 1.0)):
    g_ = kut(XY0 + 2.0, XY1 - 2.0, YY1, YY1 + 1.0, zs * ZG0 if zs > 0 else -ZG1, zs * ZG1 if zs > 0 else -ZG0)
    for xv in (-120.0, -40.0, 40.0, 120.0):
        g_ = g_.cut(sily(xv, zs * (ZG0 + ZG1) / 2.0, 1.6, YY1 - 1, YY1 + 2))
    ekle("kenar_kilavuzu_%d" % i_, "KASET", g_, "pom",
         bom=("Bant kenar kılavuzu 2,5 × 1,0 × %.0f" % (XY1 - XY0 - 4), 2, "UHMW-PE gıda (beyaz) · 4 × M3 havşa", "bant kenarına 0,5 mm; yana kaçmayı sınırlar") if i_ == 0 else None)

# --- 1.5 rulolar (burun = tahrikli, kuyruk = gergili; AYNI parça) ---
def rulo(xc, arka_uzun):
    w = silz(xc, Y_R, D_R / 2.0, -ZY0 + 0.5, ZY0 - 0.5)
    w = w.union(silz(xc, Y_R, 2.5, -(ZY1 + (8.0 if arka_uzun else 1.2)), ZY1 + 1.2))
    return w
ekle("burun_rulosu", "KASET", rulo(X_N, True), "celik",
     bom=("Rulo Ø12 × 301 · muylu Ø5", 2, "AISI 316 · taşlanmış · bombe 0,05 · DIN 6799 RS4 segman yuvaları",
          "burun (tahrikli: arka muylusu uzun, GT2 kasnağı) + kuyruk (gergili) AYNI parça (burunda uzun muylu)"))
ekle("kuyruk_rulosu", "KASET", rulo(X_K, False), "celik")
# rulmanlar SMR115-2RS (5 × 11 × 4)
for ad_, xc, zs in (("burun_on", X_N, 1), ("burun_arka", X_N, -1), ("kuyruk_on", X_K, 1), ("kuyruk_arka", X_K, -1)):
    ekle("rulman_" + ad_, "KASET", rulman_z(xc, Y_R, 5.0, 11.0, 4.0, ZY0 if zs > 0 else -ZY1), "celik",
         bom=("Paslanmaz mini rulman SMR115-2RS (5 × 11 × 4)", 4, "AISI 440C · 2 lastik keçe · gıda gresi (NSF H1)", "burunda yan sacta, kuyrukta kızakta") if ad_ == "burun_on" else None)
# segmanlar (DIN 6799 RS4, Ø5 mil)
for ad_, xc, zz in (("burun_on", X_N, ZY1 + 0.3), ("kuyruk_on", X_K, ZY1 + 0.3), ("kuyruk_arka", X_K, -ZY1 - 0.9)):
    ekle("segman_" + ad_, "KASET", halka_z(xc, Y_R, 2.5, 4.6, zz, zz + 0.6), "celik",
         bom=("Segman DIN 6799 RS4 (Ø5 mil)", 4, "paslanmaz 1.4122", "rulonun eksenel tutması (burun arkası kasnak göbeğiyle)") if ad_ == "burun_on" else None)

# --- 1.6 kuyruk gergi kızakları + yaylar (Century Spring 62266SCS, yan sacın DIŞINDA) ---
YAY = H.YAY
L_c = YAY["L0"] - YAY["on_sikma"]
for i_, (z0, z1, zs) in enumerate(((ZY0, ZY1, 1.0), (-ZY1, -ZY0, -1.0))):
    kz = kut(X_K - 8.0, X_K + 8.0, Y_R - 7.95, Y_R + 7.95, z0, z1)                                   # pencerede kayan blok
    zi = (z0 - 1.0, z0) if zs > 0 else (z1, z1 + 1.0)                                                  # iç flanş (1 mm)
    zo = (z1, z1 + 1.0) if zs > 0 else (z0 - 1.0, z0)                                                  # dış flanş
    kz = kz.union(kut(X_K - 11.0, X_K + 11.0, Y_R - 7.5, Y_R + 9.5, zo[0], zo[1]))            # yalnız DIŞ flanş: içe kaçmaz; dışa kaçmayı rulo + karşı kızağın flanşı önler
    zt = (z1 + 1.0, z1 + 9.0) if zs > 0 else (z0 - 9.0, z0 - 1.0)                                      # yay tırnağı (dışta)
    kz = kz.union(kut(X_K + 7.0, X_K + 11.0, Y_R - 3.5, Y_R + 3.5, zt[0], zt[1]))
    kz = kz.cut(silz(X_K, Y_R, R_RUL, min(zi[0], zo[0]) - 1, max(zi[1], zo[1]) + 1))
    ekle("gergi_kizagi_%d" % i_, "KASET", kz, "celik",
         bom=("Kuyruk gergi kızağı (blok 16 × 16 × 4 + dış flanş 22 × 20 × 1 + yay tırnağı)", 2, "AISI 304 · Ø11 H7 rulman yuvası · pencerede ±4 gezer",
              "dış flanşı yan saca dayanır; iki kızak rulo + segmanlarla birbirine bağlı → yanal kaçmaz · tırnağı yay dışa (−x) iter → %.0f N/kol sabit gerginlik" % H.T_KOL) if i_ == 0 else None)
    zc = (zt[0] + zt[1]) / 2.0
    x_a, x_b = X_K + 11.0, X_K + 11.0 + L_c
    r_s, t_s = YAY["D"] / 2.0 - YAY["tel"] / 2.0, YAY["tel"]
    try:
        hel = cq.Wire.makeHelix(pitch=L_c / 5.41, height=L_c, radius=r_s)
        prof = cq.Wire.makeCircle(t_s / 2.0, cq.Vector(r_s, 0, 0), cq.Vector(0, 1, 0))
        yay = cq.Solid.sweep(cq.Face.makeFromWires(prof), [], hel, isFrenet=True)
        assert yay.isValid()
    except Exception:
        yay = cq.Solid.makeCylinder(r_s + t_s / 2.0, L_c).cut(cq.Solid.makeCylinder(r_s - t_s / 2.0, L_c))
    yay = yay.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 1, 0), 90.0).translate(cq.Vector(x_a, Y_R, zc))
    ekle("gergi_yayi_%d" % i_, "KASET", yay, "celik",
         bom=("Basma yayı Century Spring 62266SCS", 2, "316 · Ø9,14 × tel 1,27 × 12,7 · 13,45 N/mm · uçlar kapalı-taşlanmış",
              "çalışma boyu %.1f → %.1f N; kızak tırnağı ile yay kutusunun uç duvarı arasında" % (L_c, H.F_YAY)) if i_ == 0 else None)
    # yay kutusu: dış kapak + üst/alt kenar + uç duvarı (kızak tırnağı içinde ±4 gezer)
    zk0, zk1 = (z1 + 1.2, z1 + 11.2) if zs > 0 else (z0 - 11.2, z0 - 1.2)
    zdis = (zk1 - 1.0, zk1) if zs > 0 else (zk0, zk0 + 1.0)
    kk = kut(X_K - 2.0, x_b + 1.0, Y_R - 6.5, Y_R + 6.5, zdis[0], zdis[1])                               # dış kapak
    kk = kk.union(kut(X_K - 2.0, x_b + 1.0, Y_R + 5.5, Y_R + 6.5, zk0, zk1))                              # üst kenar
    kk = kk.union(kut(X_K - 2.0, x_b + 1.0, Y_R - 6.5, Y_R - 5.5, zk0, zk1))                              # alt kenar
    kk = kk.union(kut(x_b, x_b + 1.0, Y_R - 6.5, Y_R + 6.5, zk0, zk1))                                    # uç duvarı (yay dayanağı)
    ekle("yay_kutusu_%d" % i_, "KASET", kk, "celik",
         bom=("Yay kutusu (U kapak) 1 mm", 2, "AISI 304 · yan saca 2 punta (kenarlarından)", "yayı ve kızak tırnağını örter; uç duvarı yaya dayanak") if i_ == 0 else None)

# --- 1.7 vidalar (DIN 7991 A2) — yan saclar → taban + yatak ---
nv = 0
for zs, zyuz in ((1, ZY1), (-1, -ZY1)):
    for xv in X_VT:
        ekle("vida_taban_%d" % nv, "KASET", havsa_vida_z(xv, (YT0 + YT1) / 2.0, zyuz, -zs, 5.0, 12.0), "koyu"); nv += 1
    for xv in (-100.0, 0.0, 90.0):
        ekle("vida_yatak_%d" % nv, "KASET", havsa_vida_z(xv, (YY0 + YY1) / 2.0, zyuz, -zs, 5.0, 12.0), "koyu"); nv += 1
PARCALAR[[p["ad"] for p in PARCALAR].index("vida_taban_0")]["bom"] = ("Havşa vida DIN 7991 M5 × 12", nv, "A2-70 paslanmaz", "yan sac → taban (6) + yatak (6); kenar dişlerine")

# --- 1.8 tahrik: burun kasnağı + GT2 kayış + rotor (kasnak + yatak + mıknatıs kabı) + sabit mil ---
ekle("burun_kasnagi", "KASET", gt2_kasnak(X_N, Y_R, ZK0, ZK1, delik=5.0), "celik",
     bom=("GT2 kasnak 20 diş, 6 mm, delik 5", 1, "paslanmaz (303) · M3 set vidası muylu düzlüğüne", "burun rulosunun arka muylusunda"))
rot = gt2_kasnak(X_RO, Y_RO, ZK0, ZK1, dis=28, delik=6.5, flans=0.5)                                   # 28 diş (içine 686 sığar)
rot = rot.union(silz(X_RO, Y_RO, 10.0, ZRY0, ZK0 - 0.5))                                                        # ara gövde Ø20
rot = rot.union(silz(X_RO, Y_RO, D_M / 2.0, ZM0 + 0.5, ZRY0))                                                    # mıknatıs kabı Ø36 (kapak ayrı)
rot = rot.cut(silz(X_RO, Y_RO, 3.25, ZM0 - 1, ZK1 + 2))                                                          # mil deliği
rot = rot.cut(silz(X_RO, Y_RO, 6.5, ZK1 - 5.0, ZK1 + 1.0))                                                       # rulman A yuvası (kasnak içinde)
rot = rot.cut(silz(X_RO, Y_RO, 6.5, ZM0 + 2.0, ZM0 + 7.0))                                                       # rulman B yuvası (kap içinde)
rot = rot.cut(silz(X_RO, Y_RO, 7.0, ZM0 - 1, ZM0 + 2.0))                                                         # segman cebi Ø14
MIK = H.MIK
for i in range(MIK["adet"]):
    a = 2 * math.pi * i / MIK["adet"]
    rot = rot.cut(silz(X_RO + MIK["r_hatve"] * math.cos(a), Y_RO + MIK["r_hatve"] * math.sin(a), 5.05, ZM0 - 1, ZM0 + 0.5 + 5.1))
ekle("tahrik_rotoru", "ROTOR", rot, "celik",
     bom=("Tahrik rotoru (GT2 28 diş + ara gövde + mıknatıs kabı) TEK gövde", 1, "AISI 316 · CNC (GT2 dişi azdırma) · 2 rulman yuvası Ø13 H7 · 6 mıknatıs cebi Ø10,1 × 5,1",
          "sabit mil Ø6'da 2 rulmanla (biri kasnakta, biri kapta) döner · dışta 0,5 mm kapak lazer kaynaklı (mıknatıslar gıdaya değmez)"))
for i in range(MIK["adet"]):
    a = 2 * math.pi * i / MIK["adet"]
    ekle("rotor_miknatisi_%d" % i, "ROTOR", silz(X_RO + MIK["r_hatve"] * math.cos(a), Y_RO + MIK["r_hatve"] * math.sin(a), 5.0, ZM0 + 0.55, ZM0 + 0.55 + 5.0), "miknatis",
         bom=("Neodimyum disk mıknatıs supermagnete S-10-05-N", 12, "Ø10 × 5 · N42 · nikel · ~2,6 kg", "6 kasette + 6 sabit tahrikte · kutuplar sırayla N-S") if i == 0 else None)
ekle("rotor_kapagi", "ROTOR", halka_z(X_RO, Y_RO, 7.0, D_M / 2.0, ZM0, ZM0 + 0.5), "celik",
     bom=("Mıknatıs kapağı Ø36 × 0,5", 2, "AISI 316 · lazer kaynak (sızdırmaz)", "kaset rotoru + sabit tahrik diski"))
for j_, zz in enumerate((ZK1 - 5.0, ZM0 + 2.0)):
    ekle("rotor_rulmani_%d" % j_, "ROTOR", rulman_z(X_RO, Y_RO, 6.0, 13.0, 5.0, zz), "celik",
         bom=("Paslanmaz rulman 686-2RS (6 × 13 × 5)", 4, "AISI 440C · 2RS · NSF H1 gres", "kasette rotorda 2, sabit tahrikte 2") if j_ == 0 else None)
ekle("rotor_pulu", "KASET", halka_z(X_RO, Y_RO, 3.0, 4.5, ZK1, -ZY1), "celik",
     bom=("Pul Ø9 × Ø6 × 1", 1, "A2", "rulman A iç bileziği ile yan sac arası"))
ekle("rotor_mili", "KASET", silz(X_RO, Y_RO, 3.0, ZM0 + 1.0, -ZY0), "celik",
     bom=("Rotor mili Ø6 × %.0f" % (-ZY0 - ZM0), 1, "AISI 316 · arka yan saca TIG kaynaklı (içte düz)", "dış ucunda DIN 6799 RS5 segman (kabın ortasındaki Ø14 cepte)"))
ekle("segman_rotor", "KASET", halka_z(X_RO, Y_RO, 3.0, 5.5, ZM0 + 1.2, ZM0 + 1.9), "celik",
     bom=("Segman DIN 6799 RS5 (Ø6 mil)", 1, "paslanmaz 1.4122", "rotoru milde tutar; kabın ortasındaki Ø14 cepte"))
# kilit: ferritik pim (1.4016) — mıknatıslar geçerken tutar (8 konum/tur)
ekle("kilit_pimi", "KASET", silz(X_RO + D_M / 2.0 + 2.5, Y_RO, 2.0, ZM0 + 1.0, ZRY0).union(kut(X_RO + D_M / 2.0 + 0.5, X_RO + D_M / 2.0 + 4.5, Y_RO - 3.0, Y_RO + 3.0, ZRY0, -ZY1)), "koyu",
     bom=("Bant kilidi: ferritik pim Ø4 + ayak", 1, "1.4016 (manyetik paslanmaz) · arka yan saca kaynaklı", "rotorun mıknatısları pime yapışır → bant kendiliğinden dönmez; sabit tahrik gelince yener"))

# ================================================================ 2 · MESH-YALNIZ PARÇALAR (bant, GT2 kayış)
class Ag(object):
    def __init__(self): self.P, self.N, self.I, self.UV = [], [], [], []
    def ekle(self, p, n, uv):
        self.P.append(p); self.N.append(n); self.UV.append(uv); return len(self.P) - 1
def yol_serit(yol, z0, z1, t, u_olcek=80.0, ic=True):
    """yol: [(x, y, nx, ny, s)] kapalı yolun hatve çizgisi · kalınlık t · z0..z1 genişlik → ince katı ağ (UV u=s/ölçek)"""
    m = Ag(); n = len(yol)
    for kat, isaret in ((0, +1.0), (1, -1.0)):
        base = len(m.P)
        for (x, y, nx, ny, s) in yol:
            px, py = x + isaret * nx * t / 2.0, y + isaret * ny * t / 2.0
            m.ekle((px, py, z0), (isaret * nx, isaret * ny, 0.0), (s / u_olcek, 0.0))
            m.ekle((px, py, z1), (isaret * nx, isaret * ny, 0.0), (s / u_olcek, 1.0))
        for i in range(n - 1):
            a, b, c, d = base + 2 * i, base + 2 * i + 1, base + 2 * i + 3, base + 2 * i + 2
            m.I += ([a, d, c, a, c, b] if isaret > 0 else [a, b, c, a, c, d])
    for zz, nz in ((z0, -1.0), (z1, 1.0)):                               # kenarlar
        base = len(m.P)
        for (x, y, nx, ny, s) in yol:
            m.ekle((x + nx * t / 2.0, y + ny * t / 2.0, zz), (0, 0, nz), (s / u_olcek, 0.5))
            m.ekle((x - nx * t / 2.0, y - ny * t / 2.0, zz), (0, 0, nz), (s / u_olcek, 0.5))
        for i in range(n - 1):
            a, b, c, d = base + 2 * i, base + 2 * i + 1, base + 2 * i + 3, base + 2 * i + 2
            m.I += ([a, b, c, a, c, d] if nz > 0 else [a, d, c, a, c, b])
    return m
def iki_daire_yolu(x1, y1, r1, x2, y2, r2, adim=1.0):
    """iki daire (x1<x2) etrafında dış teğet kapalı yol, saat yönünün tersi değil: üst kol x1→x2 (bant yönü +x)"""
    dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
    b = math.asin((r1 - r2) / L)
    # üst teğet normalı
    ang = math.atan2(uy, ux) + math.pi / 2.0 + b
    nx_, ny_ = math.cos(ang), math.sin(ang)
    pts = []
    def seg(ax, ay, bx, by, s0):
        l = math.hypot(bx - ax, by - ay); k = max(2, int(l / adim)); out = []
        for i in range(k):
            f = i / float(k); out.append((ax + (bx - ax) * f, ay + (by - ay) * f, s0 + l * f))
        return out, s0 + l
    def yay(cx, cy, r, a0, a1, s0):
        l = abs(a1 - a0) * r; k = max(4, int(l / adim)); out = []
        for i in range(k):
            a = a0 + (a1 - a0) * i / float(k); out.append((cx + r * math.cos(a), cy + r * math.sin(a), s0 + l * i / float(k), math.cos(a), math.sin(a)))
        return out, s0 + l
    s = 0.0; yol = []
    p1 = (x1 + r1 * nx_, y1 + r1 * ny_); p2 = (x2 + r2 * nx_, y2 + r2 * ny_)
    o, s = seg(p1[0], p1[1], p2[0], p2[1], s); yol += [(x, y, nx_, ny_, ss) for x, y, ss in o]
    a_ust = math.atan2(ny_, nx_)
    ang2 = math.atan2(uy, ux) - math.pi / 2.0 - b; a_alt = ang2
    o, s = yay(x2, y2, r2, a_ust, a_alt, s); yol += [(x, y, nx, ny, ss) for x, y, ss, nx, ny in o]
    q2 = (x2 + r2 * math.cos(a_alt), y2 + r2 * math.sin(a_alt)); q1 = (x1 + r1 * math.cos(a_alt), y1 + r1 * math.sin(a_alt))
    o, s = seg(q2[0], q2[1], q1[0], q1[1], s); yol += [(x, y, math.cos(a_alt), math.sin(a_alt), ss) for x, y, ss in o]
    o, s = yay(x1, y1, r1, a_alt - 2 * math.pi if a_alt > a_ust else a_alt, a_ust - 2 * math.pi if a_alt < a_ust - 2 * math.pi else a_ust - 2 * math.pi, s)
    yol += [(x, y, nx, ny, ss) for x, y, ss, nx, ny in o]
    yol.append((p1[0], p1[1], nx_, ny_, s))
    return yol, s
R_HATVE = D_R / 2.0 + t_b / 2.0
yol_b, L_b = iki_daire_yolu(X_K, Y_R, R_HATVE, X_N, Y_R, R_HATVE)
AGLAR = []   # (ad, grup, Ag, mal)
AGLAR.append(("kaset_bandi", "BANT", yol_serit(yol_b, -W_B / 2.0, W_B / 2.0, t_b), "bant"))
r_gt = H.D_KASNAK / 2.0 + 0.38
yol_g, L_g = iki_daire_yolu(X_RO, Y_RO, r_gt, X_N, Y_R, r_gt)
yol_g, L_g = iki_daire_yolu(X_RO, Y_RO, H.D_KASNAK_R / 2.0 + 0.38, X_N, Y_R, r_gt)
AGLAR.append(("gt2_kayis", "GT2", yol_serit(yol_g, ZK0 + 0.5, ZK1 - 0.5, 1.38, 4.0), "koyu"))
BOM_EK = [("Konveyör bandı Forbo Siegling Transilon E 3/1 U0/U2 MT HACCP white FDA", 1, "1,15 mm · 296 × %.0f sonsuz (sıcak Z-ek)" % L_b, "hesap boyu %.1f · bıçak/rulo r ≥ 3 · FDA + AB" % H.L_BANT),
          ("GT2 kapalı kayış Gates PowerGrip 140-2GT-6", 1, "2 mm hatve · 70 diş · 6 mm", "rotor 28 ↔ burun 20 (1,4) · C %.1f" % TK["C_GT2"])]

# ================================================================ 3 · DONER / ARABA ekleri (TOPPING değişiklikleri e, d)
for i_, a_ in enumerate(PIM_AC):
    ekle("ayar_konum_pimi_%d" % i_, "DONER", sily(R_PIM * math.cos(math.radians(a_)), R_PIM * math.sin(math.radians(a_)), 4.0, 973.0, YT0 + 4.5), "celik",
         bom=("Konum pimi ISO 8734 Ø8 × 10 m6", 2, "1.4305 · ayar bileziğine presli (5 mm dışarıda)", "kaset tabanını yerine oturtur; biri yuvarlak biri oval delikte → kaset tek yönde takılır") if i_ == 0 else None)
for i_, sx in enumerate((-10.0, 10.0)):
    ekle("lokma_pim_uzatmasi_%d" % i_, "DONER", sily(sx, 0.0, 3.95, 966.0, YT1 - 1.5), "celik",
         bom=("Tahrik lokması pimi Ø8 × 36 (eski Ø8 × 8 yerine)", 2, "1.4305 · lokmaya presli", "pim ucu kaset tabanının burçlarına girer (958 → 982,5)") if i_ == 0 else None)
apl = kut(-150.0, 130.0, 940.5, 950.5, -145.0, 145.0).cut(sily(0.0, 0.0, 23.0, 939.0, 952.0))
ekle("araba_plakasi_v27", "ARABA", apl, "celik",
     bom=("Araba plakası 280 × 290 × 10 (sağ kenar −20)", 1, "AISI 304", "aktarma 28 mm ileri gittiğinde fırın kabuğuna değmesin"))

# ================================================================ 4 · SABİT TAHRİK (DÜNYA)
KD, KM = H.KUTU_DAR, H.KUTU_MOTOR
zw = H.Z_SUR_YUZ                          # pencere dış yüzü
kutu = kut(KD["x"][0], KD["x"][1], KD["y"][0], KD["y"][1], KD["z"][0], zw).cut(kut(KD["x"][0] + 1.5, KD["x"][1] - 1.5, KD["y"][0] + 1.5, KD["y"][1] - 1.5, KD["z"][0] - 1, zw - 1.0))
ekle("tahrik_kutusu", "TAHRIK", kutu, "celik",
     bom=("Sabit tahrik kutusu (pencereli)", 1, "AISI 304 1,5 · pencere 316 1,0 mm · TIG kaynak, IP69K sınıfı yıkama",
          "mıknatıs diski pencerenin 0,5 mm arkasında döner; kasetin rotoru önüne gelince 4,5 mm'den kavranır (dokunmadan)"))
kmot = kut(KM["x"][0], KM["x"][1], KM["y"][0], KM["y"][1], KM["z"][0], KM["z"][1]).cut(kut(KM["x"][0] + 1.5, KM["x"][1] - 1.5, KM["y"][0] + 1.5, KM["y"][1] - 1.5, KM["z"][0] + 1.5, KM["z"][1] + 1))
kmot = kmot.cut(silz(X_SUR, Y_SUR, 12.0, KM["z"][1] - 1, KM["z"][1] + 1))
ekle("motor_kutusu", "TAHRIK", kmot, "celik",
     bom=("Motor kutusu 62 × 62 × 88", 1, "AISI 304 1,5 · arka kapak O-ring + 4 × M4 · kablo rakoru M16 IP68 (Lapp SKINTOP INOX)", "tahrik kutusuna TIG kaynaklı"))
zd0 = zw - 1.0 - 0.5
disk = silz(X_SUR, Y_SUR, D_M / 2.0, zd0 - 7.5, zd0)
for i in range(MIK["adet"]):
    a = 2 * math.pi * i / MIK["adet"] + math.pi / MIK["adet"]
    disk = disk.cut(silz(X_SUR + MIK["r_hatve"] * math.cos(a), Y_SUR + MIK["r_hatve"] * math.sin(a), 5.05, zd0 - 5.6, zd0 - 0.5))
ekle("tahrik_diski", "TAHRIK_DISK", disk, "celik",
     bom=("Sabit tahrik mıknatıs diski Ø36", 1, "AISI 316 · 6 mıknatıs (S-10-05-N) · kapak 0,5 lazer kaynak", "motor miline kaplinle"))
for i in range(MIK["adet"]):
    a = 2 * math.pi * i / MIK["adet"] + math.pi / MIK["adet"]
    ekle("tahrik_miknatisi_%d" % i, "TAHRIK_DISK", silz(X_SUR + MIK["r_hatve"] * math.cos(a), Y_SUR + MIK["r_hatve"] * math.sin(a), 5.0, zd0 - 5.55, zd0 - 0.55), "miknatis")
ekle("tahrik_mili", "TAHRIK_DISK", silz(X_SUR, Y_SUR, 3.0, -418.0, zd0 - 7.5), "celik",
     bom=("Tahrik mili Ø6 × %.0f" % (zd0 - 7.5 + 418.0), 1, "AISI 316", "2 × 686-2RS yatak burcunda"))
yb_ = silz(X_SUR, Y_SUR, 11.0, -400.0, zd0 - 9.0).cut(silz(X_SUR, Y_SUR, 6.5, -401.0, zd0 - 8.0))
ekle("tahrik_yatak_burcu", "TAHRIK", yb_, "celik", bom=("Yatak burcu Ø22", 1, "AISI 304 · kutuya kaynaklı · 2 × 686-2RS", ""))
for j_, zz in enumerate((-396.0, zd0 - 14.0)):
    ekle("tahrik_rulmani_%d" % j_, "TAHRIK", rulman_z(X_SUR, Y_SUR, 6.0, 13.0, 5.0, zz), "celik")
ekle("kaplin", "TAHRIK", silz(X_SUR, Y_SUR, 9.5, -419.5, -401.0).cut(silz(X_SUR, Y_SUR, 3.2, -420, -400)), "koyu",
     bom=("Kaplin Ø19 × 18,5 (6,35 ↔ 6) · körüklü/elastomer", 1, "ZARF — katalog kaplin seçilmedi [V]", "motor mili 1/4\" → tahrik mili 6"))
try:
    _m = cq.importers.importStep(MOTOR_STEP).val()
    bb = _m.BoundingBox()
    # STEP: mil +Z yönünde (TOPPING v26 ile aynı kullanım) → mil ucu tahrik miline bakacak şekilde yerleştir
    print("motor STEP bbox", round(bb.xmin, 1), round(bb.xmax, 1), round(bb.ymin, 1), round(bb.ymax, 1), round(bb.zmin, 1), round(bb.zmax, 1))
    _m = cq.Workplane(obj=_m).intersect(kut(-31.0, 31.0, -31.0, 31.0, bb.zmin - 1.0, bb.zmax + 1.0)).val()      # STEP'teki 300 mm kablo atıldı (kablo rakordan çıkar)
    bb = _m.BoundingBox()
    _m = _m.translate(cq.Vector(X_SUR - (bb.xmin + bb.xmax) / 2.0, Y_SUR - (bb.ymin + bb.ymax) / 2.0, (-420.0 + 21.0) - bb.zmax))
    ekle("tahrik_motoru", "TAHRIK", _m, "motor",
         bom=("Step motor NEMA23 AutomationDirect SureStep STP-MTR-23079", 1, "GERÇEK CAD (katalog/step) · 24–48 V · STP-DRV-4830 sürücü (kuru bölmede)",
              "%.0f dev/dk'da aktarma · gereken %.3f N·m" % (H.S["motor"]["n_dev_dk"], H.T_tasarim)), kaynak="katalog/step/stp-mtr-23079.step")
except Exception as e:
    print("MOTOR STEP okunamadı:", e)
brk = kut(X_SUR - 20.0, X_SUR + 20.0, 912.5, KM["y"][0], -400.0, -396.0).union(kut(X_SUR - 20.0, X_SUR + 20.0, 912.5, 916.5, -400.0, -365.0))
brk = brk.union(kut(X_SUR - 20.0, X_SUR + 20.0, KD["y"][0] - 4.0, KD["y"][0], -400.0, -380.0))
ekle("tahrik_braketi", "TAHRIK", brk, "celik",
     bom=("Tahrik braketi L", 1, "AISI 304 4 mm abkant · kayış kirişine 2 × M6 (yeni diş) · kutuya 2 × M5", "kutu 912,5 kotundaki kayış kirişinin üstünden taşınır"))

# ================================================================ 5 · YÜKLEME BANDI (DÜNYA · fırın tarafı, B kavramı)
t_yb = 0.35
Y_YBN = UST - t_yb - 6.0
X_YBN = LB_SOL + t_yb + 6.0
X_YBT, R_YBT = 2830.0, 15.0
Y_YBT = UST - t_yb - R_YBT
ZF = (ZE - W_B / 2.0 - 12.0, ZE + W_B / 2.0 + 12.0)              # çerçeve iç yüzleri
for i_, (z0, z1) in enumerate(((ZF[0] - 5.0, ZF[0]), (ZF[1], ZF[1] + 5.0))):
    fr = kut(X_YBN - 8.0, X_YBT + 20.0, 962.0, UST + 1.0, z0, z1).cut(silz(X_YBN, Y_YBN, 5.5, z0 - 1, z1 + 1)).cut(silz(X_YBT, Y_YBT, 8.0, z0 - 1, z1 + 1))
    ekle("yb_cerceve_%d" % i_, "YB", fr, "celik",
         bom=("Yükleme bandı yan sacı 5 mm", 2, "AISI 304 lazer", "fırının ön odasına köprü braketleriyle (fırın v9'da kesinleşir)") if i_ == 0 else None)
ekle("yb_burun_rulosu", "YB", silz(X_YBN, Y_YBN, 6.0, ZF[0] + 0.5, ZF[1] - 0.5).union(silz(X_YBN, Y_YBN, 2.5, ZF[0] - 5.0, ZF[1] + 5.0)), "celik",
     bom=("YB burun rulosu Ø12 (kasetinkiyle aynı)", 1, "AISI 316 · 2 × SMR115-2RS", "kaset burnuna 3 mm"))
ekle("yb_tahrik_rulosu", "YB", silz(X_YBT, Y_YBT, R_YBT, ZF[0] + 0.5, ZF[1] - 0.5).union(silz(X_YBT, Y_YBT, 5.0, ZF[0] - 5.0, ZF[1] + 20.0)), "celik",
     bom=("YB tahrik rulosu Ø30", 1, "AISI 316 · lastik kaplama · 2 × 6000-2RS", "NEMA23 + GT2 (fırın üst bölmesinden)"))
ekle("yb_yatak_saci", "YB", kut(X_YBN + 7.0, X_YBT - 16.0, UST - t_yb - 3.0, UST - t_yb, ZF[0], ZF[1]), "celik",
     bom=("YB yatak sacı 3 mm", 1, "AISI 304", ""))
for i_, xb in enumerate((X_YBN + 40.0, X_YBT - 40.0)):
    ekle("yb_ayak_%d" % i_, "YB", kut(xb - 10.0, xb + 10.0, 800.0, 962.0, ZF[0] - 5.0, ZF[1] + 5.0).cut(kut(xb - 11.0, xb + 11.0, 805.0, 957.0, ZF[0], ZF[1])), "celik",
         bom=("YB köprü ayağı", 2, "AISI 304 3 mm", "fırın gövdesinin iç tabanına (ön oda)") if i_ == 0 else None)
yol_y, L_y = iki_daire_yolu(X_YBN, Y_YBN, 6.0 + t_yb / 2.0, X_YBT, Y_YBT, R_YBT + t_yb / 2.0)
AGLAR.append(("yukleme_bandi", "YB_BANT", yol_serit(yol_y, ZE - W_B / 2.0, ZE + W_B / 2.0, t_yb, 80.0), "ptfe"))
BOM_EK.append(("Yükleme bandı PTFE-cam kumaş sonsuz bant", 1, "0,35 mm · 296 × %.0f" % L_y, "260 °C'ye kadar · ZARF — üretici seçilmedi [V]"))

# ================================================================ 6 · FIRIN VEKİLİ (DÜNYA · fırın v8 kabuğu + B ısıtma)
AG0 = H.AGIZ_YENI_ALT
for ad_, (y0, y1, z0, z1) in (("alt", (788.0, AG0, -651.0, 79.0)), ("ust", (1042.0, 1305.0, -651.0, 79.0)), ("arka", (AG0, 1042.0, -651.0, -341.0)), ("on", (AG0, 1042.0, -10.0, 79.0))):
    ekle("firin_on_kabuk_" + ad_, "FIRIN", kut(2500.0, 2501.5, y0, y1, z0, z1), "sac")
ISI0 = X_YBT + R_YBT + 67.0
ekle("firin_giris_duvari", "FIRIN", kut(ISI0 - 60.0, ISI0, 1004.0, 1083.0, -406.0, 0.0), "koyu")

# ================================================================ 7 · BAĞLAM (TOPPING v26 + A kabini) + DEĞİŞİKLİKLER
def jyukle(ad):
    yol = os.path.join(BAGLAM, ad)
    if yol.endswith(".gz"):
        with gzip.open(yol, "rb") as f: return json.loads(f.read().decode("utf-8"))
    return json.load(io.open(yol, encoding="utf-8"))
BTC = jyukle("baglam_tc_v26.json.gz")["parcalar"] + jyukle("baglam_ak_v1.json")["parcalar"]
with gzip.open(os.path.join(BAGLAM, "baglam_engel_v1.brep.gz"), "rb") as f: _brep = f.read()
_tmp = os.path.join(CIKTI, "_engel_tmp.brep")
with open(_tmp, "wb") as f: f.write(_brep)
ENGEL_KOK = cq.Shape.importBrep(_tmp); os.remove(_tmp)
ENGEL_AD = json.load(io.open(os.path.join(BAGLAM, "baglam_engel_v1_adlar.json"), encoding="utf-8"))
ENGEL = {ad: (sh, g) for sh, (ad, g) in zip(list(ENGEL_KOK), ENGEL_AD)}
AK_KOK = cq.Shape.importBrep(os.path.join(BAGLAM, "baglam_engel_ak_v1.brep"))
for sh, ad in zip(list(AK_KOK), json.load(io.open(os.path.join(BAGLAM, "baglam_engel_ak_v1_adlar.json"), encoding="utf-8"))):
    ENGEL[ad] = (sh, "SABIT")
# değişiklikler (a, c, d) — yeni katılar DEGISIK grubunda; denetim hem eski hem yeni ile yapılır
DEG = {}
od = ENGEL["onyuz_cerceve_mek_orta_dikme"][0]
DEG["onyuz_cerceve_mek_orta_dikme"] = cq.Workplane(obj=od).cut(kut(1580.0, 1620.0, 965.0, 1012.0, 30.0, 70.0)).val()
YV = H.B["YARIK_V2"]
DEG["cikis_yarigi_contasi"] = kut(YV[0][0], YV[0][1], H.YARIK_YENI_ALT - 10.0, YV[0][3], YV[0][4], 0.0).cut(kut(YV[1][0], YV[1][1], H.YARIK_YENI_ALT, YV[1][3], YV[1][4], -8.0)).val()
dX = AKT - H.AKT_ESKI
for ad_ in ("uc_tamponu_1", "uc_tamponu_plakasi"):
    if ad_ in ENGEL: DEG[ad_] = ENGEL[ad_][0].translate(cq.Vector(dX, 0, 0))
for ad_, sh_ in DEG.items():
    ekle("deg_" + ad_, "DEGISIK", sh_, "degisik")
ekle("deg_ray_uzatmasi_on", "DEGISIK", kut(2485.0, 2498.0, 896.5 + 16.0, 896.5 + 31.0, -65.0 - 7.5, -65.0 + 7.5), "degisik",
     bom=("HGR15 ray uzatması (TOPPING v27)", 2, "ray sağ ucu 2485 → 2498", "aktarma +%.1f" % dX))
ekle("deg_ray_uzatmasi_arka", "DEGISIK", kut(2485.0, 2498.0, 896.5 + 16.0, 896.5 + 31.0, -275.0 - 7.5, -275.0 + 7.5), "degisik")
YER_DEG = set(DEG.keys()) | {"araba_plakasi"}

# ================================================================ 8 · DENETİM
DEN = []
def d_ekle(kod, ad, deger, sart, ok, ayrinti=""):
    DEN.append(dict(kod=kod, ad=ad, deger=deger, sart=sart, gecti=bool(ok), ayrinti=ayrinti)); print("  [%s] %s %s — %s" % ("OK" if ok else "XX", kod, ad, deger))
    if ayrinti: print("        " + ayrinti[:1500])
def vol(a, b):
    try: return a.intersect(b).Volume()
    except Exception: return -1.0
def bb_kes(a, b, pay=0.0):
    A, B = a.BoundingBox(), b.BoundingBox()
    return not (A.xmax + pay < B.xmin or B.xmax + pay < A.xmin or A.ymax + pay < B.ymin or B.ymax + pay < A.ymin or A.zmax + pay < B.zmin or B.zmax + pay < A.zmin)
def uzaklik(a, b):
    try: return a.distance(b)
    except Exception:
        from OCP.BRepExtrema import BRepExtrema_DistShapeShape
        d = BRepExtrema_DistShapeShape(a.wrapped, b.wrapped); d.Perform(); return d.Value()
print("DENETİM")
# D1 katı geçerliliği
gecersiz = [p["ad"] for p in PARCALAR if not p["sh"].isValid()]
d_ekle("D1", "yeni katılar geçerli (%d parça)" % len(PARCALAR), "hepsi" if not gecersiz else ", ".join(gecersiz), "hepsi geçerli", not gecersiz)
# D2 kaset iç çakışma
KASETLER = [p for p in PARCALAR if p["grup"] in ("KASET", "ROTOR")]
cak = []
for i in range(len(KASETLER)):
    for j in range(i + 1, len(KASETLER)):
        a, b = KASETLER[i], KASETLER[j]
        if not bb_kes(a["sh"], b["sh"]): continue
        v = vol(a["sh"], b["sh"])
        if v > 0.5: cak.append("%s ↔ %s %.1f mm³" % (a["ad"], b["ad"], v))
d_ekle("D2", "kaset kendi içinde çakışma (%d parça çifti taranır)" % (len(KASETLER) * (len(KASETLER) - 1) // 2), "%d çakışma" % len(cak), "0", not cak, "; ".join(cak[:12]))

# kaset yerel köşe bulutu → yarıçap profili r(y)
def tum_noktalar():
    N = []
    for p in KASETLER + [p for p in PARCALAR if p["grup"] == "DONER" and p["ad"].startswith("ayar")]:
        for f in p["sh"].Faces():
            vs, _ = f.tessellate(0.3, 0.4); N += [(v.x, v.y, v.z) for v in vs]
    for ad_, g_, m_, _ in AGLAR:
        if g_ in ("BANT", "GT2"): N += m_.P
    return N
NOK = tum_noktalar()
Y_MIN, Y_MAX = min(p[1] for p in NOK), max(p[1] for p in NOK)
DILIM = 2.0
prof = {}
for x, y, z in NOK:
    k = int((y - Y_MIN) // DILIM)
    r = math.hypot(x, z)
    if r > prof.get(k, 0.0): prof[k] = r
R_CAD = max(prof.values())
d_ekle("D3", "dönüş yarıçapı CAD'den (hesap %.1f)" % H.R_SUP, round(R_CAD, 2), "≤ hesap + 0,5", R_CAD <= H.R_SUP + 0.5)
def supurme(x0, x1, pay=0.5):
    kat = None
    for k, r in sorted(prof.items()):
        y0 = Y_MIN + k * DILIM; y1 = y0 + DILIM
        r = r + pay
        if x1 - x0 < 0.01: w = sily(x0, ZE, r, y0, y1)
        else: w = cq.Workplane("XZ").center((x0 + x1) / 2.0, ZE).slot2D(x1 - x0 + 2 * r, 2 * r, 0).extrude(-(y1 - y0)).translate((0, y0, 0))
        kat = w if kat is None else kat.union(w)
    return kat.val()
ISTASYON = [("sos", 910.0, 910.0), ("harc", 1260.0, 1260.0), ("kiyma", 1483.0, 1707.0), ("kusbasi", 1693.0, 1917.0), ("kasar", 1956.0, 2061.0), ("sucuk", 2187.0, 2293.0)]
SUP = {}
def engel_listesi(degisik):
    L = []
    for ad_, (sh_, g_) in ENGEL.items():
        if g_ == "ACICI": continue
        if degisik and ad_ in DEG: L.append((ad_ + " (yeni)", DEG[ad_]))
        else: L.append((ad_, sh_))
    if degisik:
        L += [("sabit_tahrik:" + p["ad"], p["sh"]) for p in PARCALAR if p["grup"] in ("TAHRIK", "TAHRIK_DISK")]
        L += [("yukleme_bandi:" + p["ad"], p["sh"]) for p in PARCALAR if p["grup"] == "YB"]
        L += [("firin:" + p["ad"], p["sh"]) for p in PARCALAR if p["grup"] == "FIRIN"]
    return L
for ad_, x0, x1 in ISTASYON:
    SUP[ad_] = supurme(x0, x1)
for degisik in (False, True):
    sonuc = []
    for ist, x0, x1 in ISTASYON:
        s = SUP[ist]
        for ead, esh in engel_listesi(degisik):
            if not bb_kes(s, esh): continue
            v = vol(s, esh)
            if v > 0.5: sonuc.append("%s: %s %.0f mm³" % (ist, ead, v))
    kod = "D4b" if degisik else "D4a"
    d_ekle(kod, "istasyonlarda dönerken çarpma — %s" % ("AYARLAR (a–f) UYGULANMIŞ" if degisik else "BUGÜNKÜ TOPPING (ayarsız)"),
           "%d çakışma" % len(sonuc), "0" if degisik else "bilgi", (not sonuc) if degisik else True, "; ".join(sonuc[:20]))
# D5 en yakın engel payı (ayarlı) — her istasyon
paylar = {}
for ist, x0, x1 in ISTASYON:
    s = SUP[ist]; en = (1e9, "")
    for ead, esh in engel_listesi(True):
        if not bb_kes(s, esh, 40.0): continue
        d = uzaklik(s, esh)
        if d < en[0]: en = (d, ead)
    paylar[ist] = (round(en[0] + 0.5, 2), en[1])
d_ekle("D5", "dönüşte en yakın engele pay (ayarlı, 0,5 süpürme payı geri eklendi)", {k: v[0] for k, v in paylar.items()}, "≥ 3 mm", all(v[0] >= 3.0 for v in paylar.values()),
       "; ".join("%s → %s %.1f" % (k, v[1], v[0]) for k, v in paylar.items()))
# D6 yolculuk (0°, park → aktarma) — kaset katısı her 5 mm'de
def kaset_poz(x_t, aci=0.0):
    out = []
    for p in KASETLER:
        s = p["sh"].rotate(cq.Vector(0, 0, 0), cq.Vector(0, 1, 0), aci) if aci else p["sh"]
        out.append((p["ad"], s.translate(cq.Vector(x_t, 0, ZE))))
    return out
kaset_kok = cq.Compound.makeCompound([p["sh"] for p in KASETLER])
yol_engel = [(a, s) for a, s in engel_listesi(True) if s.BoundingBox().ymax > 975.0 and s.BoundingBox().ymin < 1010.0 and s.BoundingBox().zmin < -10 + 20 and s.BoundingBox().zmax > -345.0]
yol_cak = []
xs = [H.PARK + i * 5.0 for i in range(int((AKT - H.PARK) / 5.0) + 1)] + [AKT]
for x_t in xs:
    kk = kaset_kok.translate(cq.Vector(x_t, 0, ZE))
    for a, s in yol_engel:
        if not bb_kes(kk, s): continue
        v = vol(kk, s)
        if v > 0.5: yol_cak.append("x %.0f: %s %.0f mm³" % (x_t, a, v))
d_ekle("D6", "0°'de park → aktarma yolculuğu (%d konum × %d engel)" % (len(xs), len(yol_engel)), "%d çakışma" % len(yol_cak), "0", not yol_cak, "; ".join(yol_cak[:12]))
# D7 aktarma konumu payları
akt = kaset_kok.translate(cq.Vector(AKT, 0, ZE))
akt_pay = {}
for a, s in [("yükleme bandı", cq.Compound.makeCompound([p["sh"] for p in PARCALAR if p["grup"] == "YB"])),
             ("yarık contası (yeni)", DEG["cikis_yarigi_contasi"]),
             ("fırın ön kabuğu", cq.Compound.makeCompound([p["sh"] for p in PARCALAR if p["grup"] == "FIRIN" and p["ad"].startswith("firin_on")])),
             ("sabit tahrik kutusu", cq.Compound.makeCompound([p["sh"] for p in PARCALAR if p["grup"] == "TAHRIK"]))]:
    akt_pay[a] = round(uzaklik(akt, s), 2)
rot_akt = cq.Compound.makeCompound([p["sh"] for p in PARCALAR if p["grup"] == "ROTOR"]).translate(cq.Vector(AKT, 0, ZE))
disk_c = cq.Compound.makeCompound([p["sh"] for p in PARCALAR if p["grup"] == "TAHRIK_DISK"])
akt_pay["rotor kapağı ↔ tahrik diski (hava + pencere + hava)"] = round(uzaklik(rot_akt, disk_c), 2)
d_ekle("D7", "aktarma konumunda paylar (x %.1f, 0°)" % AKT, akt_pay, "> 0 · mıknatıs ≈ %.1f" % (H.BOSLUK_KAVRAMA - 1.0),
       all(v > 0.3 for v in akt_pay.values()))
# D8 sabit tahrik + YB bağlama karşı (SABIT)
sb = []
for p in [q for q in PARCALAR if q["grup"] in ("TAHRIK", "TAHRIK_DISK", "YB")]:
    for a, s in engel_listesi(False):
        if not bb_kes(p["sh"], s): continue
        v = vol(p["sh"], s)
        if v > 0.5: sb.append("%s ↔ %s %.0f mm³" % (p["ad"], a, v))
d_ekle("D8", "sabit tahrik + yükleme bandı ↔ TOPPING/A bağlamı", "%d çakışma" % len(sb), "0", not sb, "; ".join(sb[:12]))
# D9 açıcı (basma konumu) ↔ kaset parkta
acici = [(a, s) for a, (s, g) in ENGEL.items() if g == "ACICI" or a == "acici_kolonu"]
ac = []
park = kaset_kok.translate(cq.Vector(H.PARK, 0, ZE))
en_ac = 1e9
for a, s in acici:
    if bb_kes(park, s):
        v = vol(park, s)
        if v > 0.5: ac.append("%s %.0f mm³" % (a, v))
    if bb_kes(park, s, 30.0): en_ac = min(en_ac, uzaklik(park, s))
d_ekle("D9", "açıcı (TOPPING'deki basma konumu) ↔ kaset parkta", "%d çakışma · en yakın %.1f mm" % (len(ac), en_ac if en_ac < 1e8 else -1), "0 çakışma", not ac, "; ".join(ac))
# D10 kütle
YOG = {"celik": 7.95e-6, "koyu": 7.95e-6, "pom": 0.94e-6, "miknatis": 7.5e-6, "motor": 3.0e-6}
m_kaset = sum(p["sh"].Volume() * YOG.get(p["mal"], 7.95e-6) for p in KASETLER) + H.S["tork"]["m_bant"]
d_ekle("D10", "kaset kütlesi (bant dahil)", "%.2f kg" % m_kaset, "≤ 12 kg (elle sökülür)", m_kaset <= 12.0)

# ================================================================ 9 · BİRLEŞİM DÖKÜMÜ
BIRLESIM = [
    ("kaset tabanı ↔ ayar bileziği", "2 × Ø8 konum pimi (ayar bileziğine presli, 5 mm dışarıda) + kasetin ağırlığı (%.1f kg)" % m_kaset,
     "dönme: 2 tahrik pimi (lokma, r 10) taban burçlarına girer · kalkmaz: yük hep aşağı (açıcı 482 N, ağırlık), yatay yükler pimlerde", "ALETSİZ kaldırılır (kaldırma dudakları)", "ıslak · conta yok, kaset komple yıkanır"),
    ("yan saclar ↔ taban / yatak", "12 × DIN 7991 M5×12 A2 havşa, kenar dişlerine", "havşa yüzü yan sacla aynı düzlem", "sökülür (4 mm Allen)", "ıslak · kaynak yok, dişler açık → fırçayla yıkanır"),
    ("burun / kuyruk rulosu ↔ yan saclar", "4 × SMR115-2RS (5×11×4) · burunda yan sac deliğinde H7, kuyrukta gergi kızağında", "eksenel: rulo omzu + DIN 6799 RS4 segman (burun arkası kasnak göbeği)", "segmanlar çıkınca rulo yana çekilir", "keçeli rulman, NSF H1 gres"),
    ("kuyruk kızakları ↔ yan sac", "16×16×4 kızak 30×16 pencerede kayar (±3) + Century Spring 62266SCS dışa iter", "yanal: 1 mm kapak laması (2 × M3)", "lama sökülünce kızak çıkar", "ıslak"),
    ("GT2 kasnak ↔ burun muylusu", "M3 set vidası muylu düzlüğüne", "eksenel: kasnak göbeği rulmana dayanır", "sökülür", "—"),
    ("tahrik rotoru ↔ rotor mili", "2 × 686-2RS rotor gövdesinde · mil arka yan saca TIG kaynaklı (içte düz)", "eksenel: iç rulman mil omzuna, dış uç DIN 6799 RS5 segman (kabın ortasındaki cepte)", "segman çıkınca rotor çekilir", "mıknatıslar 316 kapta lazer kaynaklı kapak altında (sızdırmaz)"),
    ("bant ↔ rulolar", "sonsuz bant 2 rulo üstünde, alt yüz kumaş; yatak sacında kayar", "yanal: 2 UHMW kenar kılavuzu (0,5 mm pay)", "kuyruk kızakları içe itilir → bant gevşer → yana çıkar (yan sac sökülmeden değil: ön yan sac 6 vidayla sökülür)", "ıslak"),
    ("bant kilidi", "rotor mıknatısları 1.4016 ferritik pime yapışır (8 konum/tur)", "tabla dönerken, açıcı bastırırken bant kaymaz", "—", "—"),
    ("kaset ↔ sabit tahrik", "TEMAS YOK · mıknatıs yüzleri %.1f mm (kap 0,5 + hava + pencere 1 + kap 0,5)" % (H.BOSLUK_KAVRAMA), "kaset 0°'de aktarma konumuna gelince diskler karşılıklı hizalanır", "—", "kutu kapalı, pencere 316"),
    ("sabit tahrik ↔ TOPPING", "L braket → kayış kirişine 2 × M6 (yeni diş), kutuya 2 × M5", "—", "sökülür", "motor kutusu O-ring + M16 IP68 rakor"),
    ("yükleme bandı ↔ fırın", "2 köprü ayağı fırın ön odasının tabanına", "—", "—", "fırın v9'da kesinleşir (ÇÖZÜLMEDİ)"),
]

# ================================================================ 10 · GLB
MAL = {
    "celik": ((0.80, 0.82, 0.85, 1.0), 0.85, 0.30), "koyu": ((0.12, 0.12, 0.13, 1.0), 0.3, 0.55), "pom": ((0.95, 0.95, 0.93, 1.0), 0.0, 0.45),
    "miknatis": ((0.55, 0.57, 0.62, 1.0), 0.9, 0.35), "motor": ((0.16, 0.17, 0.19, 1.0), 0.5, 0.45), "sac": ((0.72, 0.75, 0.79, 1.0), 0.8, 0.35),
    "bant": ((0.93, 0.94, 0.92, 1.0), 0.0, 0.8), "ptfe": ((0.55, 0.42, 0.28, 1.0), 0.0, 0.6), "degisik": ((0.96, 0.62, 0.20, 1.0), 0.2, 0.45),
    "silikon": ((0.85, 0.35, 0.25, 1.0), 0.0, 0.6), "kart": ((0.1, 0.35, 0.2, 1.0), 0.0, 0.6), "cam": ((0.8, 0.88, 0.95, 0.35), 0.0, 0.1),
}
def mal_esle(m):
    return m if m in MAL else ("koyu" if m in ("motor", "koyu", "kart") else ("pom" if m in ("pom", "plastik", "uhmw") else "celik"))
def ag_kati(sh, tol=0.12, aci=0.25):
    P, N, I = [], [], []
    for f in sh.Faces():
        try: vs, ts = f.tessellate(tol, aci)
        except Exception: continue
        o = len(P); pp = [(v.x, v.y, v.z) for v in vs]; nn = [[0.0, 0.0, 0.0] for _ in pp]
        for a, b, c in ts:
            ux, uy, uz = pp[b][0] - pp[a][0], pp[b][1] - pp[a][1], pp[b][2] - pp[a][2]
            wx, wy, wz = pp[c][0] - pp[a][0], pp[c][1] - pp[a][1], pp[c][2] - pp[a][2]
            n = (uy * wz - uz * wy, uz * wx - ux * wz, ux * wy - uy * wx)
            for k in (a, b, c): nn[k][0] += n[0]; nn[k][1] += n[1]; nn[k][2] += n[2]
        for n in nn:
            L = math.sqrt(n[0] ** 2 + n[1] ** 2 + n[2] ** 2) or 1.0; N.append((n[0] / L, n[1] / L, n[2] / L))
        P += pp; I += [o + k for t in ts for k in t]
    return P, N, I
def ag_mesh(P, I):
    N = [[0.0, 0.0, 0.0] for _ in P]
    for k in range(0, len(I), 3):
        a, b, c = I[k], I[k + 1], I[k + 2]
        ux, uy, uz = P[b][0] - P[a][0], P[b][1] - P[a][1], P[b][2] - P[a][2]
        wx, wy, wz = P[c][0] - P[a][0], P[c][1] - P[a][1], P[c][2] - P[a][2]
        n = (uy * wz - uz * wy, uz * wx - ux * wz, ux * wy - uy * wx)
        for q in (a, b, c): N[q][0] += n[0]; N[q][1] += n[1]; N[q][2] += n[2]
    out = []
    for n in N:
        L = math.sqrt(n[0] * n[0] + n[1] * n[1] + n[2] * n[2]) or 1.0
        out.append((n[0] / L, n[1] / L, n[2] / L))
    return out
def yerel(P, dx, dz):
    return [(p[0] - dx, p[1], p[2] - dz) for p in P]
GLB = []    # (düğüm adı, P(mm), N, I, UV|None, malzeme)
for p in PARCALAR:
    Pp, Nn, Ii = ag_kati(p["sh"])
    if not Pp: continue
    ad = "%s__%s" % (p["grup"], p["ad"])
    GLB.append((ad, Pp, Nn, Ii, None, mal_esle(p["mal"])))
for ad_, g_, m_, mal_ in AGLAR:
    GLB.append(("%s__%s" % (g_, ad_), m_.P, m_.N, m_.I, m_.UV, mal_))
for b in BTC:
    ad0, g0 = b["ad"], b["grup"]
    if g0 == "KALKAN" or ad0 in YER_DEG: continue
    if ad0.startswith("itici") or ad0.startswith("aktarma"): continue
    P0 = [tuple(p) for p in b["P"]]
    if g0 in ("ARABA", "DONER"): P0 = yerel(P0, H.PARK, ZE)
    elif g0 == "ACICI": P0 = yerel(P0, H.PARK, ZE)
    GLB.append(("%s__%s" % (g0, ad0), P0, ag_mesh(P0, b["I"]), b["I"], None, mal_esle(b["mal"])))
def glb_yaz(yol, dugumler):
    blob, views, accs, meshes, nodes = [], [], [], [], []
    off = [0]
    def gom(b, hedef=None):
        while off[0] % 4: blob.append(b"\x00"); off[0] += 1
        v = {"buffer": 0, "byteOffset": off[0], "byteLength": len(b)}
        if hedef: v["target"] = hedef
        views.append(v); blob.append(b); off[0] += len(b); return len(views) - 1
    madlar = list(MAL.keys())
    for ad, P, N, I, UV, mal in dugumler:
        Pm = [(x * 0.001, y * 0.001, z * 0.001) for x, y, z in P]
        vp = gom(b"".join(struct.pack("<3f", *q) for q in Pm), 34962)
        vn = gom(b"".join(struct.pack("<3f", *n) for n in N), 34962)
        vi = gom(b"".join(struct.pack("<I", i) for i in I), 34963)
        mn = [min(q[k] for q in Pm) for k in range(3)]; mx = [max(q[k] for q in Pm) for k in range(3)]
        accs.append({"bufferView": vp, "componentType": 5126, "count": len(Pm), "type": "VEC3", "min": mn, "max": mx})
        accs.append({"bufferView": vn, "componentType": 5126, "count": len(N), "type": "VEC3"})
        accs.append({"bufferView": vi, "componentType": 5125, "count": len(I), "type": "SCALAR"})
        attr = {"POSITION": len(accs) - 3, "NORMAL": len(accs) - 2}; ind = len(accs) - 1
        if UV:
            vu = gom(b"".join(struct.pack("<2f", *u) for u in UV), 34962)
            accs.append({"bufferView": vu, "componentType": 5126, "count": len(UV), "type": "VEC2"}); attr["TEXCOORD_0"] = len(accs) - 1
        meshes.append({"name": ad, "primitives": [{"attributes": attr, "indices": ind, "material": madlar.index(mal)}]})
        nodes.append({"mesh": len(meshes) - 1, "name": ad})
    mats = []
    for k in madlar:
        c, met, ruf = MAL[k]
        mm = {"name": k, "pbrMetallicRoughness": {"baseColorFactor": list(c), "metallicFactor": met, "roughnessFactor": ruf}, "doubleSided": True}
        if c[3] < 1.0: mm["alphaMode"] = "BLEND"
        mats.append(mm)
    while off[0] % 4: blob.append(b"\x00"); off[0] += 1
    bb = b"".join(blob)
    g = {"asset": {"version": "2.0", "generator": "AUTOKITCH bantli_tabla_cad_v1"}, "scene": 0, "scenes": [{"nodes": list(range(len(nodes)))}],
         "nodes": nodes, "meshes": meshes, "materials": mats, "accessors": accs, "bufferViews": views, "buffers": [{"byteLength": len(bb)}]}
    js = json.dumps(g, separators=(",", ":")).encode("utf-8")
    while len(js) % 4: js += b" "
    with open(yol, "wb") as f:
        f.write(struct.pack("<4sII", b"glTF", 2, 12 + 8 + len(js) + 8 + len(bb)))
        f.write(struct.pack("<I4s", len(js), b"JSON")); f.write(js); f.write(struct.pack("<I4s", len(bb), b"BIN\x00")); f.write(bb)
    return len(bb) + len(js)
boy = glb_yaz(os.path.join(SAYFA, "bantli_tabla_v1.glb"), GLB)
print("GLB %d düğüm · %.1f MB" % (len(GLB), boy / 1e6))

# ================================================================ 11 · BOM + JSON
BOM = []
for p in PARCALAR:
    if p["bom"]: BOM.append(dict(grup=p["grup"], ad=p["bom"][0], adet=p["bom"][1], malzeme=p["bom"][2], not_=p["bom"][3], parca=p["ad"]))
for b in BOM_EK: BOM.append(dict(grup="KASET/YB", ad=b[0], adet=b[1], malzeme=b[2], not_=b[3], parca="-"))
with io.open(os.path.join(CIKTI, "BOM_bantli_tabla_v1.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter=";"); w.writerow(["grup", "kalem", "adet", "malzeme / katalog", "not", "parça"])
    for b in BOM: w.writerow([b["grup"], b["ad"], b["adet"], b["malzeme"], b["not_"], b["parca"]])
OZET = dict(surum="bantli_tabla_cad_v1", tarih=time.strftime("%Y-%m-%d %H:%M"), sure_s=round(time.time() - T0, 1),
            AKT=AKT, LB_SOL=LB_SOL, R_hesap=H.R_SUP, R_cad=R_CAD, kaset_kg=m_kaset, parca_sayisi=len(PARCALAR),
            gruplar={g: sum(1 for p in PARCALAR if p["grup"] == g) for g in sorted(set(p["grup"] for p in PARCALAR))},
            denetim=DEN, birlesim=[dict(zip(("cift", "tutma", "sabitleme", "sokum", "islak"), b)) for b in BIRLESIM], bom=BOM,
            ayarlar=H.S["ayarlar"], hesap_acikliklar=H.S["acikliklar"], paylar_istasyon=paylar, aktarma_paylar=akt_pay,
            pivotlar=dict(tabla_z=ZE, park_x=H.PARK, rotor=(X_RO, Y_RO), tahrik=(X_SUR, Y_SUR), yb_burun=(X_YBN, Y_YBN), yb_tahrik=(X_YBT, Y_YBT, R_YBT),
                          bant_L=L_b, gt2_L=L_g, yb_L=L_y, isi0=ISI0, zaman=H.S["zaman"], acici_strok=90.0))
with io.open(os.path.join(U, "bantli_tabla_cad_v1.json"), "w", encoding="utf-8") as f:
    json.dump(OZET, f, ensure_ascii=False, indent=1)
with io.open(os.path.join(SAYFA, "bantli_tabla_v1.json"), "w", encoding="utf-8") as f:
    json.dump({k: OZET[k] for k in ("surum", "tarih", "AKT", "LB_SOL", "R_hesap", "R_cad", "kaset_kg", "parca_sayisi", "gruplar", "denetim", "birlesim", "bom", "ayarlar", "paylar_istasyon", "aktarma_paylar", "pivotlar")},
              f, ensure_ascii=False, indent=1)
print("BİTTİ %.0f s · %d parça · kaset %.2f kg · R_cad %.1f" % (time.time() - T0, len(PARCALAR), m_kaset, R_CAD))
