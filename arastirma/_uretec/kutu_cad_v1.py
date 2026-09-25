# -*- coding: utf-8 -*-
"""AUTOKITCH · E · KUTU KATLAMA MODÜLÜ — ÜRETİM MODELİ v1 (25 Eyl 2026)
Kemal (24 Eyl): "standart pizza kutusunu bul, nasıl katlanacağını öğren, katlanması için bizim sistemde mühendislik
çalışmasını yap ve modelle, sonra animasyonu hazırla; tüm parçalar standart, motorlar standart; her şeyi tam göster,
sorunlara çözüm üret. Banttan kutuya düşecek, sonra kapak kapanacak: önce düz, sonra katlanıyor, sonra pizza
içine giriyor, sonra kapanıyor. Robot alırken bir yere çarpıp kapanabilir, bu da bir opsiyon. Bizim ölçülere
uydurmaya çalış, olmazsa ikinci bir model yap, daha geniş."

KUTU (standart): pizza kutusu 32 × 32 × 4,2 cm, E-dalga (AmbalajPazarı · 100'lü paket; Bekar Ambalaj 32×32×4: 100 adet 16 kg)
  Dizilim "Amerikan kapama" = US 4441626 A: taban + 2 yan duvar (uçlarında köşe tırnakları) + ÇİFT ön duvar (dış + iç panel,
  iç panelin 2 kilit dili tabandaki yarıklara girer, köşe tırnakları iki ön panelin ARASINDA kalır) + arka duvar (menteşe)
  + kapak (2 yan flap + ön flap; kapanınca flaplar duvarların İÇİNE girer). Wikipedia: "yan duvarlara bağlı flapların ön
  duvarın içine katlandığı tip standart olmuştur".
  AÇILIM (hesap — üreticinin bıçak çizimi alınınca güncellenecek): 804 × 404 mm.

NEDEN 700 DEĞİL 830: açılım 804 uzun. 700'lük modülün içi ~697 → açılım boyuna sığmaz; derinliğe (830) yatırınca şarjör
  ile katlama yeri aynı izdüşümde kalıyor ve blank şarjörden katlama yerine ÇIKAMIYOR (kalıp ve tepsi yolun üstünde).
  Şarjörü üste almak (kapak dönüşünün üstü, 1560 sonrası) ≈ 250–280 kutu = 1,5 gün → 2 gün kuralı tutmuyor.
  → Modül 830 × 830 (hat +130 mm). Açılım x boyunca yatar; şarjör ARKADA, katlama ÖNDE, blank ÜSTTEN İTİLEREK gelir.

ÇEVRİM: şarjör (asansör yığını 1149,6'da tutar) → itici blankı 411 mm öne iter (kalıbın üstüne) → piston iner: taban 45,6 mm
  kalıba girer, yan duvarlar kalkar, köşe tırnakları sabit plow'larla içeri döner, ön dış duvar kalkar (köprü aşağıda:
  ön paneller serbest) → pistonun ön dudağı iç ön paneli içeri devirir, 2. vuruş kilit dillerini yarıklara basar →
  köprü kalkar (pizza yolu) → U çerçeve kapak flaplarını 90° kaldırır → kol kapağı dik tutar → [pizza K plakasından
  köprüden kayıp kutuya düşer] → kol kapağı 10° öne yatırır → piston kapağı kapatıp bastırır (flaplar içeri) → robot
  çatalı tepsinin aralıklarından girer, 55 mm kaldırır, dışarı çeker.

KOORDİNAT (modül yereli): x 0..830 soldan sağa (K tarafı 0) · y 0..2030 zeminden · z 0 ön yüz, −830 arka.
  Hatta: x_hat = 4600 + x (E modülü K'nın sağında).
"""
import csv, io, json, math, os, struct, sys, time
import cadquery as cq

U = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.dirname(os.path.dirname(U))
sys.path.insert(0, U)
from kaset_3d_v3 import Mesh, MM, MALZEME
import topping_cad_v22 as TC

for _k, _v in {"sac": ((0.74, 0.77, 0.80, 1.0), 0.85, 0.32), "aluminyum": ((0.80, 0.82, 0.85, 1.0), 0.9, 0.3),
               "celik": ((0.55, 0.57, 0.60, 1.0), 0.9, 0.35), "motor": ((0.18, 0.19, 0.22, 1.0), 0.5, 0.45),
               "kart": ((0.10, 0.35, 0.22, 1.0), 0.1, 0.6), "siemens": ((0.23, 0.36, 0.40, 1.0), 0.2, 0.5),
               "plastik": ((0.55, 0.57, 0.60, 1.0), 0.0, 0.6), "uhmw": ((0.93, 0.93, 0.90, 1.0), 0.0, 0.7),
               "karton": ((0.74, 0.57, 0.38, 1.0), 0.0, 0.9), "karton_yigin": ((0.66, 0.50, 0.33, 1.0), 0.0, 0.95),
               "hamur": ((0.93, 0.78, 0.52, 1.0), 0.0, 0.85), "sos": ((0.80, 0.30, 0.16, 1.0), 0.0, 0.7),
               "robot": ((0.96, 0.62, 0.10, 1.0), 0.2, 0.45), "kayis": ((0.12, 0.12, 0.13, 1.0), 0.0, 0.8),
               "sensor": ((0.15, 0.30, 0.55, 1.0), 0.2, 0.5), "sari": ((0.93, 0.75, 0.10, 1.0), 0.2, 0.5)}.items():
    MALZEME.setdefault(_k, dict(renk=_v[0], met=_v[1], ruf=_v[2]))
MALZEME.setdefault("referans", dict(renk=(0.62, 0.66, 0.72, 0.28), met=0.0, ruf=0.6, saydam=True))
MALZEME.setdefault("kabuk", dict(renk=(0.78, 0.81, 0.85, 0.14), met=0.3, ruf=0.4, saydam=True))     # dış sac: GLB'de saydam (mekanizma görünsün)

# ---------------------------------------------------------------- ÖLÇÜLER ----------------------------------------------------------------
W, H, D = 830.0, 2030.0, 830.0
SAC = 1.5
Y_PLINT = 80.0
TEPSI = 1104.0                  # kutu tabanının oturduğu yüz (hat süreç zinciri: kesme plakası 1164 − 60)
KALIP = 1149.5                  # kalıp ray üstleri (blank bunun 0,1 üstünde kayar)
YB = 1149.6                     # düz blankın alt yüzü (şarjör üstü = kalıp üstü: blank aynı kotta kayar)
T = 1.6                         # E-dalga kalınlığı (Wikipedia: E dalga adımı 1,0–1,8)
PLAKA_K = 1164.0                # K kesme plakası üstü (arayüz)
# KUTU — dış ölçü 320 × 320; ön duvar −x'te (K tarafı, pizza buradan girer), menteşe +x'te
BX0, BX1 = 100.0, 420.0
ZB = -206.0                     # kutu ekseni z. Düz blank ön yüze taşmasın diye (yan duvar 42) hattın ürün ekseni −170'ten 36 mm içeride
BZ0, BZ1 = ZB - 160.0, ZB + 160.0     # −366 … −46
H_YAN, H_ON, H_IC, H_DIL, H_ARKA = 42.0, 42.0, 40.0, 10.0, 44.0
L_KAP, W_KAP, H_KF = 312.0, 315.0, 36.0
KT_L, KT_H = 38.0, 40.0         # köşe tırnağı (yan duvarın ucunda): boy × yükseklik
X_BL0 = BX0 - H_ON - H_IC - H_DIL                 # 8
X_BL1 = BX1 + H_ARKA + L_KAP + H_KF               # 812
Z_BL0, Z_BL1 = BZ0 - H_YAN, BZ1 + H_YAN            # −408 … −4
ZL0, ZL1 = ZB - W_KAP / 2.0, ZB + W_KAP / 2.0      # kapak −363,5 … −48,5
DIL_Z = ((-300.0, -240.0), (-172.0, -112.0))       # kilit dilleri / tabandaki yarıklar
U_MAX = YB - TEPSI                                  # 45,6 · piston tabanı bu kadar indirir
# ŞARJÖR — açılım z'de 404, x'te 804; yığın ARKADA
BESLE = 411.0                   # itici blankı bu kadar öne iter
ZS0, ZS1 = Z_BL0 - BESLE, Z_BL1 - BESLE            # yığın −819 … −415
Y_PLAT = 240.0                  # tam yığında asansör platformu üstü
Y_YIGIN_UST = YB - T            # 1148,0 · 2. blankın üstü
# ÜST GÖVDELER
H_UST = 1478.0                  # piston kafası altı (yukarıda bekler; dik kapağın tepesi 1461,4)
KOL_P = (560.0, 1080.0)         # kapak kolu mili
KOL_R = 166.0
KMER = (BX1, TEPSI + T / 2.0 + H_ARKA)            # kapak menteşesi (420, 1148,8)

PARCALAR = []


def ekle(ad, wp, mal, grup="SABIT", bom=None):
    PARCALAR.append(dict(ad=ad, wp=wp, mal=mal, grup=grup, bom=bom))


kut = lambda x0, x1, y0, y1, z0, z1: cq.Workplane("XY").box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), centered=False).translate((min(x0, x1), min(y0, y1), min(z0, z1)))
def silx(y, z, r, x0, x1): return cq.Workplane("YZ").center(y, z).circle(r).extrude(x1 - x0).translate((x0, 0, 0))
def sily(x, z, r, y0, y1): return cq.Workplane("XZ").center(x, z).circle(r).extrude(-(y1 - y0)).translate((0, y0, 0))
def silz(x, y, r, z0, z1): return cq.Workplane("XY").center(x, y).circle(r).extrude(z1 - z0).translate((0, 0, z0))
def boru_y(x, z, r, ri, y0, y1): return sily(x, z, r, y0, y1).cut(sily(x, z, ri, y0 - 1, y1 + 1))


def _trsf(M):
    """3x4 satır matrisi -> gp_Trsf (cq.Matrix listeden kurulunca 'non-orthogonal' hatası veriyor)"""
    from OCP.gp import gp_Trsf
    t = gp_Trsf()
    t.SetValues(M[0][0], M[0][1], M[0][2], M[0][3], M[1][0], M[1][1], M[1][2], M[1][3], M[2][0], M[2][1], M[2][2], M[2][3])
    return t


def tasi(sh, M):
    return sh.moved(cq.Location(_trsf(M)))


def eksen_matrisi(ex, ey, ez, P):
    return [[ex[0], ey[0], ez[0], P[0]], [ex[1], ey[1], ez[1], P[1]], [ex[2], ey[2], ez[2], P[2]]]


def capraz(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def yerles(sh, boy, normal, P):
    """kanonik katıyı (boy = x, normal = y, enine = z; kök noktası 0) hedef eksenlere oturtur"""
    return tasi(sh, eksen_matrisi(boy, normal, capraz(boy, normal), P))


# ---------------------------------------------------------------- STANDART PARÇALAR ----------------------------------------------------------------
_RAY = {}


def hgr15(ad, L, P, boy, normal, grup="SABIT", bom=None):
    """HIWIN HGR15 ray — TraceParts STEP'inin kesiti (TC.hiwin_ray) · kök = ray tabanı ortası, boy yönünde L"""
    if L not in _RAY:
        w, _n = TC.hiwin_ray(0.0, L, 0.0)
        _RAY[L] = w.val().translate(cq.Vector(0.0, -20.5, 0.0))
    ekle(ad, cq.Workplane(obj=yerles(_RAY[L], boy, normal, P)), "celik", grup,
         bom or ("Lineer ray HIWIN HGR15R", 1, "15 × 15 · boy %.0f" % L, "hiwin.com · Linear_Guideway-E s.41"))


def hgh15(ad, P, boy, normal, grup="SABIT"):
    """HIWIN HGH15CA araba — gerçek STEP · P = ray tabanında arabanın ortası"""
    sh = TC.hiwin()["araba"].translate(cq.Vector(0.0, -20.5, 0.0))
    ekle(ad, cq.Workplane(obj=yerles(sh, boy, normal, P)), "celik", grup,
         ("Lineer araba HIWIN HGH15CA", 1, "flanşsız · 34 × 61,4 · H 28", "TraceParts 90-03042020-037166"))


def nema23(ad, P, eksen, yukari, grup="SABIT"):
    """AutomationDirect SureStep STP-MTR-23079 · gerçek STEP · P = mil yüzü (flanş), gövde −eksen yönünde"""
    m = TC.nema23()
    # kanonik: mil +z, gövde −z
    ex = capraz(yukari, eksen)
    ekle(ad, cq.Workplane(obj=tasi(m["govde"], eksen_matrisi(ex, yukari, eksen, P))), "motor", grup,
         ("Step motor AutomationDirect SureStep STP-MTR-23079", 1, "NEMA 23 · 1,95 N·m (276 oz-in) · 2,8 A", "automationdirect.com STP-MTR-23079 · TraceParts STEP"))


def pgcn23(ad, P, eksen, yukari, grup="SABIT"):
    """SureGear PGCN23-1025 planet redüktör 10:1 · gerçek STEP · P = çıkış yüzü, gövde −eksen yönünde (79)"""
    r = TC.suregear()
    ex = capraz(yukari, eksen)
    ekle(ad, cq.Workplane(obj=tasi(r["tum"], eksen_matrisi(ex, yukari, eksen, P))), "motor", grup,
         ("Planet redüktör SureGear PGCN23-1025", 1, "10:1 · 5 N·m · NEMA 23", "adcpn.com/pn/PGCN23-1025 · TraceParts STEP"))


def sfu16(ad, x, z, y0, y1, hatve, grup_somun, y_somun, grup="SABIT", somun_yon=1):
    """bilyalı vida SFU16xx: mil Ø16 + flanşlı somun (flanş Ø48 × 10, gövde Ø28, boy 57) · dikey"""
    ekle(ad + "_mil", sily(x, z, 8.0, y0, y1), "celik", grup,
         ("Bilyalı vida TBI/HIWIN SFU16%02d" % hatve, 1, "Ø16 · hatve %d · boy %.0f · uçları BK12/BF12 işli" % (hatve, y1 - y0), "SFU16%02d katalog (fluxelectronix / TBI)" % hatve))
    s = sily(x, z, 14.0, y_somun, y_somun + 47.0).union(sily(x, z, 24.0, y_somun + 47.0, y_somun + 57.0)).cut(sily(x, z, 8.2, y_somun - 1, y_somun + 58))
    ekle(ad + "_somun", s, "celik", grup_somun, ("Bilyalı somun SFU16%02d-4" % hatve, 1, "flanş Ø48 · gövde Ø28 · boy 57", "katalog ölçüsü"))


def bk12(ad, x, z, y0, taban_yon, grup="SABIT", bf=False):
    """BK12 / BF12 rulman yuvası: 60 × 43 × (32,5 | 20), mil merkezi tabandan 25 · y0 = alt yüz, dikey vida için yatay oturur"""
    h = 20.0 if bf else 32.5
    # yatay (dikey mil): gövde x'te 60, z'de 43, y'de h
    b = kut(x - 30.0, x + 30.0, y0, y0 + h, z - 18.0, z + 25.0).cut(sily(x, z, 8.0 if not bf else 6.0, y0 - 1, y0 + h + 1))
    ekle(ad, b, "celik", grup, (("Destek BF12 (serbest)" if bf else "Destek BK12 (sabit)"), 1, "60 × 43 × %.1f · merkez yüksekliği 25" % h, "MISUMI BK/BF · fonlinearguide.com"))


def kasnak(ad, x, y, z, dis, eksen="y", genis=11.0, grup="SABIT"):
    """GT3 kasnak (flanşlı) · PD = dis × 3 / π"""
    pd = dis * 3.0 / math.pi
    r = pd / 2.0 - 0.38
    if eksen == "y":
        k = sily(x, z, r, y, y + genis).union(sily(x, z, r + 2.5, y - 1.0, y)).union(sily(x, z, r + 2.5, y + genis, y + genis + 1.0))
    elif eksen == "x":
        k = silx(y, z, r, x, x + genis).union(silx(y, z, r + 2.5, x - 1.0, x)).union(silx(y, z, r + 2.5, x + genis, x + genis + 1.0))
    else:
        k = silz(x, y, r, z, z + genis).union(silz(x, y, r + 2.5, z - 1.0, z)).union(silz(x, y, r + 2.5, z + genis, z + genis + 1.0))
    ekle(ad, k, "aluminyum", grup, ("Kasnak GT3 %d diş" % dis, 1, "PD %.1f · 9 mm kayış" % pd, "gates.com GT3 · katalog"))
    return pd


def kayis_y(ad, x1, z1, x2, z2, y, pd1, pd2, genis=9.0, grup="SABIT"):
    """iki dikey eksenli kasnak arasında GT3 kayış (y düzleminde) — sırt 1,2 · şerit gövde"""
    t = 1.2
    dx, dz = x2 - x1, z2 - z1; L = math.hypot(dx, dz); ux, uz = dx / L, dz / L; nx, nz = -uz, ux
    r1, r2 = pd1 / 2.0, pd2 / 2.0
    parca = None
    for s in (1.0, -1.0):
        a = (x1 + s * nx * r1, z1 + s * nz * r1); b = (x2 + s * nx * r2, z2 + s * nz * r2)
        q = [(a[0] + s * nx * 0.0, a[1] + s * nz * 0.0), (b[0], b[1]), (b[0] + s * nx * t, b[1] + s * nz * t), (a[0] + s * nx * t, a[1] + s * nz * t)]
        pl = cq.Workplane("XZ", origin=(0, y, 0)).polyline([(p[0], -p[1]) for p in q]).close().extrude(-genis)
        parca = pl if parca is None else parca.union(pl)
    for (cx, cz, r) in ((x1, z1, r1), (x2, z2, r2)):
        parca = parca.union(sily(cx, cz, r + t, y, y + genis).cut(sily(cx, cz, r, y - 1, y + genis + 1)))
    ekle(ad, parca, "kayis", grup, ("Kayış GT3 9 mm", 1, "kapalı çevrim", "gates.com"))


def kayis_z(ad, y1, z1, y2, z2, x, pd1, pd2, genis=9.0, grup="SABIT", mal="kayis"):
    """x eksenli iki kasnak arasında kayış (x düzleminde, yz'de koşar)"""
    t = 1.2
    parca = None
    dy, dz = y2 - y1, z2 - z1; L = math.hypot(dy, dz); uy, uz = dy / L, dz / L; ny, nz = -uz, uy
    r1, r2 = pd1 / 2.0, pd2 / 2.0
    for s in (1.0, -1.0):
        a = (y1 + s * ny * r1, z1 + s * nz * r1); b = (y2 + s * ny * r2, z2 + s * nz * r2)
        q = [a, b, (b[0] + s * ny * t, b[1] + s * nz * t), (a[0] + s * ny * t, a[1] + s * nz * t)]
        pl = cq.Workplane("YZ", origin=(x, 0, 0)).polyline(q).close().extrude(genis)
        parca = pl if parca is None else parca.union(pl)
    for (cy, cz, r) in ((y1, z1, r1), (y2, z2, r2)):
        parca = parca.union(silx(cy, cz, r + t, x, x + genis).cut(silx(cy, cz, r, x - 1, x + genis + 1)))
    ekle(ad, parca, mal, grup, ("Kayış GT3 9 mm", 1, "kapalı çevrim", "gates.com"))


def kaplin(ad, x, y, z, eksen="y", grup="SABIT"):
    k = sily(x, z, 12.5, y, y + 30.0) if eksen == "y" else (silz(x, y, 12.5, z, z + 30.0) if eksen == "z" else silx(y, z, 12.5, x, x + 30.0))
    ekle(ad, k, "aluminyum", grup, ("Kaplin (kavramalı) Ø25 × 30", 1, "8 × 12 / 8 × 10 delik", "MISUMI MCKL / Ruland · katalog"))


def e3z(ad, x, y, z, grup="SABIT"):
    """Omron E3Z-D62 dağınık yansımalı fotosel · 10,8 × 31 × 20 (x · y · z) · x,y,z = gövdenin alt-sol-arka köşesi"""
    ekle(ad, kut(x, x + 10.8, y, y + 31.0, z, z + 20.0), "sensor", grup,
         ("Fotosel Omron E3Z-D62", 1, "dağınık yansımalı · 1 m · PNP", "omron.com E3Z · katalog ölçüsü"))


def e2e(ad, x, y, z, eksen, grup="SABIT"):
    """Omron E2E-X2D1-N endüktif M8 · Ø8 × 30"""
    s = sily(x, z, 4.0, y, y + 30.0) if eksen == "y" else (silz(x, y, 4.0, z, z + 30.0) if eksen == "z" else silx(y, z, 4.0, x, x + 30.0))
    ekle(ad, s, "sensor", grup, ("Endüktif sensör Omron E2E-X2D1-N", 1, "M8 · 2 mm · DC 2 telli", "omron.com E2E · katalog ölçüsü"))


# ---------------------------------------------------------------- GÖVDE ----------------------------------------------------------------
def govde():
    # ayaklar + taban
    for i, (ax, az) in enumerate(((60.0, -60.0), (770.0, -60.0), (60.0, -770.0), (770.0, -770.0))):
        ekle("ayak_%d" % i, sily(ax, az, 20.0, 0.0, 8.0).union(sily(ax, az, 6.0, 8.0, Y_PLINT)), "celik",
             bom=("Ayarlı ayak Elesa+Ganter LV.A-SST · M12", 4, "paslanmaz · taban Ø40", "elesa-ganter.com LV.A-SST") if i == 0 else None)
    taban = kut(SAC, W - SAC, Y_PLINT, Y_PLINT + 3.0, -D + SAC, -SAC).cut(kut(445.0, 515.0, Y_PLINT - 1, Y_PLINT + 4, -425.0, -359.0))   # asansör motoru deliği
    ekle("taban_sac_3", taban, "sac")
    ekle("plint_on", kut(40.0, W - 40.0, 10.0, Y_PLINT, -41.5, -40.0), "sac")
    # kabuk
    ekle("arka_sac", kut(0, W, Y_PLINT, H, -D, -D + SAC), "kabuk")
    ekle("ust_sac", kut(0, W, H - SAC, H, -D + SAC, 0), "kabuk")
    sol = kut(0, SAC, Y_PLINT, H - SAC, -D + SAC, 0).cut(kut(-1, SAC + 1, 1146.0, 1230.0, -372.0, -24.0))             # pizza penceresi
    ekle("sol_sac_pizza_penceresi", sol, "kabuk")
    sag = kut(W - SAC, W, Y_PLINT, H - SAC, -D + SAC, 0).cut(kut(W - SAC - 1, W + 1, 232.0, 1156.0, -822.0, -412.0))  # şarjör yan kapısı
    ekle("sag_sac", sag, "kabuk")
    ekle("sarjor_yan_kapisi", kut(W - SAC, W, 234.0, 1154.0, -820.0, -414.0), "kabuk")
    ekle("sarjor_yan_kapisi_kulp", kut(W, W + 22.0, 640.0, 760.0, -440.0, -425.0), "celik")
    ekle("on_alt_sac", kut(SAC, W - SAC, Y_PLINT + 3.0, 1085.0, -SAC, 0), "kabuk")
    ekle("on_ust_kapak", kut(SAC, W - SAC, 1345.0, H - SAC, -SAC, 0), "kabuk")
    ekle("on_ust_kapak_kulp", kut(380.0, 450.0, 1360.0, 1378.0, 0.0, 18.0), "celik")
    # ağız üst kirişi (ön kose plow'larını tasir) — kapak dik dururken onun ONUNDE (z > -46,5)
    ekle("agiz_ust_kirisi", kut(SAC, W - SAC, 1330.0, 1345.0, -40.0, -20.0), "celik")
    # köşe dikmeleri (şarjör bölgesi dışında): L 20 × 20
    for i, (x0, z0) in enumerate(((SAC, -20.0 - SAC), (W - SAC - 20.0, -20.0 - SAC))):
        ekle("kose_dikme_on_%d" % i, kut(x0, x0 + 20.0, Y_PLINT + 3.0, 1085.0, z0, z0 + 20.0).cut(kut(x0 + (2 if i == 0 else 0), x0 + (20 if i == 0 else 18), Y_PLINT + 2, 1086, z0 - 1, z0 + 18)), "celik")


# ---------------------------------------------------------------- ŞARJÖR + ASANSÖR ----------------------------------------------------------------
X_TIRNAK = ((190.0, 220.0), (385.0, 415.0), (580.0, 610.0))
Z_KAPI0, Z_KAPI1 = ZS1 + 0.5, ZS1 + 3.5            # kapı plakası (itilen blankın önündeki eşik) −414,5 … −411,5
Y_KAPI_UST = Y_YIGIN_UST + 0.8                      # 1148,8 · 2. blankı tutar, en üsttekini geçirir


def sarjor():
    # kılavuzlar (UHMW-PE 3 mm)
    ekle("kilavuz_sol_uhmw", kut(X_BL0 - 3.5, X_BL0 - 0.5, 244.0, 1152.0, ZS0, ZS1), "uhmw",
         bom=("UHMW-PE şerit 3 mm (şarjör kılavuzu)", 3, "sol + sağ + arka", "levha"))
    ekle("kilavuz_sag_uhmw", kut(X_BL1 + 0.5, X_BL1 + 3.5, 244.0, 1152.0, ZS0, ZS1), "uhmw", bom=None)
    ekle("kilavuz_sol_tasiyici", kut(SAC, X_BL0 - 3.5, 244.0, 1152.0, -700.0, -680.0), "sac")
    ekle("kilavuz_sag_tasiyici", kut(X_BL1 + 3.5, W - SAC, 244.0, 1152.0, -700.0, -680.0), "sac")
    ekle("kilavuz_arka_uhmw", kut(X_BL0, X_BL1, 244.0, 1140.0, ZS0 - 3.5, ZS0 - 0.5), "uhmw")
    ekle("kilavuz_arka_tasiyici", kut(X_BL0 + 40.0, X_BL1 - 40.0, 244.0, 1140.0, -D + SAC, ZS0 - 3.5), "sac")
    kapi = kut(X_BL0, X_BL1, 244.0, Y_KAPI_UST, Z_KAPI0, Z_KAPI1)
    for x0, x1 in X_TIRNAK:
        kapi = kapi.cut(kut(x0 - 2.0, x1 + 2.0, 243.0, 1112.0, Z_KAPI0 - 1, Z_KAPI1 + 1))
    ekle("sarjor_kapi_esigi", kapi, "sac")
    # yığın (2. blanktan aşağısı) — en üstteki blank ayrı ve hareketli
    ekle("karton_yigini", kut(X_BL0, X_BL1, Y_PLAT, Y_YIGIN_UST, ZS0, ZS1), "karton_yigin",
         bom=("Pizza kutusu 32 × 32 × 4,2 E-dalga (düz açılım 804 × 404)", 567, "yığın 908 mm = 567 adet @1,6 · 504 @1,8", "AmbalajPazarı · 100'lü paket (sarf)"))
    # asansör: platform + 3 çatal
    ekle("asansor_platformu", kut(X_BL0, X_BL1, Y_PLAT - 3.0, Y_PLAT, ZS0, ZS1), "aluminyum", "ASANSOR")
    for i, (x0, x1) in enumerate(X_TIRNAK):
        ekle("asansor_catali_%d" % i, kut(x0, x1, Y_PLAT - 11.0, Y_PLAT - 3.0, ZS0, -406.0), "celik", "ASANSOR")
    ekle("asansor_arabasi", kut(150.0, 650.0, 170.0, 300.0, -410.0, -406.0), "celik", "ASANSOR")
    # raylar: arka plaka z −378..−374 (kalıp rayının 1,5 mm arkası), raylar −z'ye bakar
    ekle("asansor_ray_plakasi", kut(200.0, 600.0, 150.0, 1140.0, -378.0, -374.0), "sac")
    for i, xr in enumerate((250.0, 550.0)):
        hgr15("asansor_rayi_%d" % i, 990.0, (xr, 150.0, -378.0), (0, 1, 0), (0, 0, -1),
              bom=("Lineer ray HIWIN HGR15R", 2, "asansör · boy 990", "hiwin.com") if i == 0 else ("Lineer ray HIWIN HGR15R", 0, "", ""))
        for j, yc in enumerate((200.0, 270.0)):
            hgh15("asansor_arabasi_%d%d" % (i, j), (xr, yc, -378.0), (0, 1, 0), (0, 0, -1), "ASANSOR")
    # trapez vida Tr16x4 (kendinden kilitli) + blok somun + yataklar + 2:1 kayış + motor (plint içinde)
    ekle("asansor_vidasi_Tr16x4", sily(405.0, -392.0, 8.0, 150.0, 1125.0), "celik",
         bom=("Trapez vida Tr16×4 (DIN 103) + bronz blok somun", 1, "boy 975 · kendinden kilitli (η≈0,35): güç kesilince yığın düşmez", "katalog"))
    ekle("asansor_somunu", kut(390.0, 420.0, 205.0, 250.0, -406.0, -380.0).cut(sily(405.0, -392.0, 8.2, 200, 260)), "celik", "ASANSOR")
    for ad_, y0 in (("asansor_alt_yatak", 150.0), ("asansor_ust_yatak", 1125.0)):
        ekle(ad_, kut(385.0, 425.0, y0 - 12.0, y0, -410.0, -378.0).cut(sily(405.0, -392.0, 6.0, y0 - 13, y0 + 1)), "celik",
             bom=("Flanşlı yatak KFL001 (Ø12)", 2, "vida uçları", "katalog") if y0 < 500 else None)
    pd1 = kasnak("asansor_kasnak_40", 405.0, 120.0, -392.0, 40)
    pd2 = kasnak("asansor_kasnak_20", 480.0, 120.0, -392.0, 20)
    kayis_y("asansor_kayisi", 405.0, -392.0, 480.0, -392.0, 121.0, pd1, pd2)
    nema23("asansor_motoru", (480.0, 118.0, -392.0), (0, 1, 0), (0, 0, 1))
    e2e("asansor_alt_sensor", 610.0, 150.0, -386.0, "y")


# ---------------------------------------------------------------- BESLEYİCİ (İTİCİ) ----------------------------------------------------------------
Y_BES_PL = 1500.0                # besleyici üst plakası altı — dik kapağın (flapıyla 1466) ÜSTÜNDE: raylar kapağın −z flap düzlemini kesmez
Z_RAY_BES = (-828.0, -355.0)          # raylar plakadan 22 mm taşar (piston bağlantı plakası x 170–370'te, raylar x 150/650'de)
Z_BES_PL1 = -367.0                    # plaka ön kenarı: dik kapağın −z flapı −363,5'e kadar gelir


def besleyici():
    """itici: en üstteki blankı arka kenarından yakalayıp 411 mm öne (kalıbın üstüne) sürer.
    2 HGR15 ray plakanın altında (x 150 / 650), GT3 kayış plakanın üstünde (x 729,5), motor plakanın +x ucunun ötesinde."""
    pl = kut(100.0, 721.0, Y_BES_PL, Y_BES_PL + 5.0, Z_RAY_BES[0], Z_BES_PL1).cut(kut(165.0, 375.0, Y_BES_PL - 1, Y_BES_PL + 6, -400.0, Z_BES_PL1 + 1))   # piston ekseni cebi
    ekle("besleyici_plakasi", pl, "aluminyum", bom=("Besleyici plakası 6082 · 5 mm", 1, "621 × 461", "üretim"))
    for i, xr in enumerate((150.0, 650.0)):
        ekle("besleyici_plaka_askisi_%d" % i, kut(xr - 10.0, xr + 10.0, Y_BES_PL + 5.0, H - SAC, -600.0, -580.0), "aluminyum")
        hgr15("besleyici_rayi_%d" % i, Z_RAY_BES[1] - Z_RAY_BES[0], (xr, Y_BES_PL, Z_RAY_BES[0]), (0, 0, 1), (0, -1, 0),
              bom=("Lineer ray HIWIN HGR15R", 2, "besleyici · boy 473", "hiwin.com") if i == 0 else ("Lineer ray HIWIN HGR15R", 0, "", ""))
        hgh15("besleyici_arabasi_%d" % i, (xr, Y_BES_PL, -797.0), (0, 0, 1), (0, -1, 0), "ITICI")      # 411 strokta araba iki uçta da rayda (0,3 mm)
    # iki araba plakası (arka köşe plow askısı x 450–462 arada kalır) + asma plakalar + kiriş + itici çubuk
    ekle("itici_araba_plakasi_sol", kut(130.0, 168.0, Y_BES_PL - 34.0, Y_BES_PL - 28.0, -826.0, -762.0), "aluminyum", "ITICI")
    ekle("itici_araba_plakasi_sag", kut(630.0, 725.0, Y_BES_PL - 34.0, Y_BES_PL - 28.0, -826.0, -750.0), "aluminyum", "ITICI")
    for i, xr in enumerate((150.0, 650.0)):
        ekle("itici_asma_plakasi_%d" % i, kut(xr - 20.0, xr + 20.0, 1176.2, Y_BES_PL - 34.0, -826.0, -818.0), "aluminyum", "ITICI")
    ekle("itici_kirisi_40x20", kut(10.0, 810.0, 1156.2, 1176.2, -826.0, -819.5), "aluminyum", "ITICI")
    ekle("itici_cubugu", kut(10.0, 810.0, YB + 0.6, 1156.2, -826.0, -819.5), "celik", "ITICI",
         bom=("İtici çubuk 304 · 800 × 6,5 × 6", 1, "alt kenarı 1150,2: yalnız EN ÜSTTEKİ blankı yakalar (1149,6–1151,2)", "üretim"))
    # kayış tahriki (plakanın üstünde): TAHRİK ÖNDE (z −345), AVARA ARKADA (z −815). Kasnak kenarları arası 446,6 mm;
    # çene (20) 411 strok yapar → önde 15 mm pay kalır. (v1 ilk hali: kasnaklar 410 aralıkta, çene strok sonunda avaraya giriyordu.)
    YK = Y_BES_PL + 25.0
    pdm = kasnak("besleyici_kasnak_tahrik", 725.0, YK, -345.0, 20, eksen="x")
    pdi = kasnak("besleyici_kasnak_avara", 725.0, YK, -815.0, 20, eksen="x")
    kayis_z("besleyici_kayisi", YK, -345.0, YK, -815.0, 726.0, pdm, pdi)
    ekle("besleyici_avara_yatagi", kut(700.0, 721.0, Y_BES_PL + 5.0, YK + 16.0, -826.0, -805.0), "aluminyum")

    ekle("besleyici_avara_mili", silx(YK, -815.0, 4.0, 700.0, 740.0), "celik")
    ekle("itici_kayis_kulagi", kut(722.0, 725.0, Y_BES_PL - 28.0, Y_BES_PL + 5.0, -803.0, -783.0), "celik", "ITICI")
    ekle("itici_kayis_cenesi", kut(722.0, 737.0, Y_BES_PL + 5.0, YK - 10.8, -803.0, -783.0), "celik", "ITICI")
    nema23("besleyici_motoru", (742.0, YK, -345.0), (-1, 0, 0), (0, 1, 0))
    ekle("besleyici_motor_braketi", kut(738.0, 742.0, YK - 30.0, YK + 30.0, -376.0, -314.0).cut(silx(YK, -345.0, 20.0, 737, 743)), "aluminyum")
    ekle("besleyici_motor_rafi", kut(738.0, W - SAC, YK - 36.0, YK - 30.0, -376.0, -314.0), "aluminyum")
    e2e("besleyici_arka_sensor", 600.0, Y_BES_PL - 18.0, -828.0 + 7.5, "z")


# ---------------------------------------------------------------- KALIP + TEPSİ ----------------------------------------------------------------
X_CATAL = ((157.0, 183.0), (247.0, 273.0), (337.0, 363.0))     # robot çatal dişleri
X_BAR = ((BX0, 155.0), (185.0, 245.0), (275.0, 335.0), (365.0, BX1))


def kalip():
    ekle("kalip_tablasi_6", kut(90.0, 430.0, 1080.0, 1086.0, -372.5, -32.0), "sac")
    for i, (xp, zp) in enumerate(((110.0, -340.0), (410.0, -340.0), (110.0, -70.0), (410.0, -70.0))):
        ekle("kalip_ayagi_%d" % i, kut(xp - 20.0, xp + 20.0, Y_PLINT + 3.0, 1080.0, zp - 20.0, zp + 20.0).cut(kut(xp - 17.8, xp + 17.8, Y_PLINT + 2, 1081, zp - 17.8, zp + 17.8)), "aluminyum",
             bom=("Alüminyum profil 40 × 40 (kalıp ayağı)", 4, "boy 997", "item / Bosch Rexroth 40×40") if i == 0 else None)
    # tepsi çubukları (robot çatalı aralarından girer); ön çubukta kilit dili cebi
    for i, (x0, x1) in enumerate(X_BAR):
        b = kut(x0, x1, 1096.0, TEPSI, BZ0, BZ1)
        if i == 0:
            for z0, z1 in DIL_Z:
                b = b.cut(kut(x0 - 1, x0 + 32.0, 1094.0, TEPSI + 1, z0 - 2.0, z1 + 2.0))      # kilit dili cebi: dil devrilirken 30 mm ileriden iner
        ekle("tepsi_cubugu_%d" % i, b, "sac")
        ekle("tepsi_ayagi_%d" % i, kut((x0 + x1) / 2.0 - 8.0, (x0 + x1) / 2.0 + 8.0, 1086.0, 1096.0, ZB - 8.0, ZB + 8.0), "sac")
    # arka (−z) kalıp rayı ve ön (+z) tarak — tarağın dişleri arasından çatal geçer
    ekle("kalip_rayi_arka_z", kut(BX0, 405.0, 1086.0, KALIP, BZ0 - T - 6.0, BZ0 - T - 0.5), "sac", bom=("Kalıp rayı 304 · 6 mm", 1, "arka yan duvarı kaldırır", "üretim"))
    for i, (x0, x1) in enumerate(X_BAR):
        ekle("kalip_taragi_on_z_%d" % i, kut(max(x0, BX0), min(x1, 405.0), 1086.0, KALIP, BZ1 + T + 0.5, BZ1 + T + 6.5), "sac",
             bom=("Kalıp tarağı 304 · 6 mm (4 diş)", 1, "ön yan duvarı tutar · dişleri arasından robot çatalı geçer", "üretim") if i == 0 else None)
    ekle("kalip_on_x_rayi", kut(93.4, 97.9, 1086.0, 1129.5, BZ0, BZ1), "sac", bom=("Kalıp ön rayı 304 · 4,5 mm", 1, "ön duvar 20 mm geç kalkar (köşe tırnakları önce döner)", "üretim"))
    ekle("kalip_arka_x_dayagi", kut(BX1 + T + 0.5, BX1 + T + 6.5, 1086.0, TEPSI + 8.0, BZ0, BZ1), "sac")
    # KÖŞE TIRNAĞI KIVIRICISI MODELLENMEDİ (v1): sabit plow + askıları yükselen tırnakların ve kapak flaplarının
    # yolunda kalıyordu (geçiş taraması). Seçenekler sayfada: kalıp köşesinde eğik takoz / 2 küçük döner kıvırıcı.


# ---------------------------------------------------------------- KÖPRÜ (pizza yolu, düşer) ----------------------------------------------------------------
KOPRU_ALT = 30.0


def kopru():
    """pizza köprüsü: katlamada 30 mm AŞAĞIDA (ön paneller serbest kalkar), pizza gelirken kalıp kotuna çıkar"""
    ekle("kopru_plakasi", kut(2.0, 92.0, KALIP - 3.0 - KOPRU_ALT, KALIP - KOPRU_ALT, BZ0, BZ1), "sac", "KOPRU",
         bom=("Köprü sacı 304 · 3 mm", 1, "pizza yolu · katlamada 30 mm aşağıda", "üretim"))
    ekle("kopru_tasiyici", kut(30.0, 64.0, 1080.0, KALIP - 3.0 - KOPRU_ALT, ZB - 40.0, ZB + 40.0).cut(sily(47.0, ZB, 9.0, 1079, 1120)), "aluminyum", "KOPRU")
    for i, zc in enumerate((BZ0 + 40.0, BZ1 - 40.0)):
        ekle("kopru_kilavuz_mili_%d" % i, sily(47.0, zc, 6.0, 950.0, KALIP - 3.0 - KOPRU_ALT), "celik", "KOPRU",
             bom=("Kılavuz mili Ø12 h6 + lineer burç LM12UU", 2, "köprü", "katalog") if i == 0 else None)
        ekle("kopru_burcu_%d" % i, boru_y(47.0, zc, 10.5, 6.1, 985.0, 1015.0), "celik")
    bp = kut(20.0, 74.0, 1015.0, 1021.0, BZ0 + 20.0, BZ1 - 20.0)
    for zc in (BZ0 + 40.0, BZ1 - 40.0):
        bp = bp.cut(sily(47.0, zc, 6.3, 1014, 1022))
    ekle("kopru_burc_plakasi", bp.cut(sily(47.0, ZB, 9.0, 1014, 1022)), "aluminyum")
    ekle("kopru_plaka_tutucu", kut(SAC, 16.0, 1000.0, 1021.0, BZ0 + 20.0, BZ1 - 20.0), "aluminyum")
    sfu16("kopru_vidasi", 47.0, ZB, 1000.0, 1112.0, 5, "KOPRU", 1023.0)
    bk12("kopru_BK12", 47.0, ZB, 982.5, 1)
    kaplin("kopru_kaplini", 47.0, 952.5, ZB)
    nema23("kopru_motoru", (47.0, 952.5, ZB), (0, 1, 0), (0, 0, 1))
    ekle("kopru_motor_braketi", kut(17.0, 77.0, 952.5, 958.5, ZB - 30.0, ZB + 30.0).cut(sily(47.0, ZB, 20.0, 951, 960)), "aluminyum")
    ekle("kopru_motor_askisi", kut(SAC, 16.0, 952.5, 1000.0, ZB - 30.0, ZB + 30.0), "aluminyum")
    e2e("kopru_alt_sensor", 72.0, 1030.0, ZB + 34.0, "y")


# ---------------------------------------------------------------- PİSTON ----------------------------------------------------------------
PK_X = (112.0, 408.0)
PK_Z = (-354.0, -58.0)
Z_PBAG = (-361.0, -351.0)       # kafayı arabaya bağlayan dikey plaka (kapak −z flapının 0,5 mm içinde)


def piston():
    """zımba: tabanı kalıba basar (45,6), 2. vuruşta devrilmiş iç paneli kilitler, 3. vuruşta kapağı kapatıp bastırır.
    Vida SFU1610 üstten BK12 ile tutulur, altı serbest (sabit–serbest): bağlantı plakası vidanın arkasından geçtiği için
    alt yatağın braketi hareket yoluna düşüyordu. Kontrol: 450 mm Ø16 burkulma ~3,5 kN ≫ 170 N; kritik devir ~2760 d/dk > 1800."""
    h = H_UST
    kafa_ = cq.Workplane("XY").polyline([(PK_X[0] + 6.0, h), (PK_X[1], h), (PK_X[1], h + 20.0), (PK_X[0], h + 20.0), (PK_X[0], h + 6.0)]).close() \
        .extrude(PK_Z[1] - PK_Z[0]).translate((0, 0, PK_Z[0]))
    ekle("piston_kafasi", kafa_, "aluminyum", "PISTON",
         bom=("Piston kafası 6082 · 296 × 296 × 20 · ön alt kenar 6 mm pah", 1, "tabana basar, iç paneli kilitler, kapağı bastırır", "üretim"))
    for i, xc in enumerate((200.0, 320.0)):
        ekle("piston_kaburgasi_%d" % i, kut(xc - 4.0, xc + 4.0, h + 20.0, h + 70.0, PK_Z[0] + 5.0, PK_Z[1] - 5.0), "aluminyum", "PISTON")
    ekle("piston_baglanti_plakasi", kut(170.0, 370.0, h + 20.0, h + 535.0, Z_PBAG[0], Z_PBAG[1]), "aluminyum", "PISTON")
    ekle("piston_eksen_plakasi", kut(170.0, 370.0, 1500.0, 2015.0, -394.0, -389.0), "aluminyum")
    ekle("piston_eksen_askisi", kut(170.0, 370.0, 2015.0, H - SAC, -394.0, -380.0), "aluminyum")
    for i, xr in enumerate((200.0, 340.0)):
        hgr15("piston_rayi_%d" % i, 515.0, (xr, 1500.0, -389.0), (0, 1, 0), (0, 0, 1),
              bom=("Lineer ray HIWIN HGR15R", 2, "piston · boy 515", "hiwin.com") if i == 0 else ("Lineer ray HIWIN HGR15R", 0, "", ""))
        for j, yc in enumerate((h + 440.0, h + 500.0)):
            hgh15("piston_arabasi_%d%d" % (i, j), (xr, yc, -389.0), (0, 1, 0), (0, 0, 1), "PISTON")
    sfu16("piston_vidasi", 270.0, -325.0, 1515.0, 2008.0, 10, "PISTON", h + 417.0)
    ekle("piston_somun_braketi", kut(240.0, 300.0, h + 464.0, h + 474.0, -351.0, -299.0).cut(sily(270.0, -325.0, 14.5, h + 463, h + 475)), "aluminyum", "PISTON")
    bk12("piston_BK12", 270.0, -325.0, 1958.0, 1)
    for i, (x0, x1) in enumerate(((240.0, 252.0), (288.0, 300.0))):
        ekle("piston_BK_askisi_%d" % i, kut(x0, x1, 1990.5, H - SAC, -343.0, -307.0), "aluminyum")
    pd1 = kasnak("piston_kasnak_vida", 270.0, 1995.5, -325.0, 20)
    pd2 = kasnak("piston_kasnak_motor", 340.0, 1995.5, -318.0, 20)
    kayis_y("piston_kayisi", 270.0, -325.0, 340.0, -318.0, 1996.5, pd1, pd2)
    nema23("piston_motoru", (340.0, 1990.0, -318.0), (0, 1, 0), (0, 0, 1))
    ekle("piston_motor_braketi", kut(308.0, 372.0, 1990.0, 1994.0, -350.0, -286.0).cut(sily(340.0, -318.0, 20.0, 1989, 1995)), "aluminyum")
    for i, (x0, x1) in enumerate(((308.0, 316.0), (364.0, 372.0))):
        ekle("piston_motor_askisi_%d" % i, kut(x0, x1, 1994.0, H - SAC, -350.0, -336.0), "aluminyum")
    e2e("piston_ust_sensor", 385.0, 1950.0, -389.0 + 2.0, "z")


PARMAK_P = (88.0, 1260.0)
PARMAK_R = 72.0
PARMAK_Z = (-350.0, -62.0)


def parmak():
    """iç ön paneli devirir: üstten iner, dik duran panelin tepesini kutunun içine iter (sonra yerçekimi + 2. vuruş)"""
    px, py = PARMAK_P
    p = kut(px - 4.0, px + 4.0, py, py + PARMAK_R, PARMAK_Z[0], PARMAK_Z[1]).union(silz(px, py, 12.0, PARMAK_Z[0], PARMAK_Z[1]))
    ekle("devirme_parmagi", p, "celik", "PARMAK", bom=("Devirme parmağı 304 · 8 mm", 1, "R 72 · 140° döner", "üretim"))
    ekle("parmak_mili", silz(px, py, 6.0, -425.0, PARMAK_Z[0]), "celik")
    for i, (z0, z1) in enumerate(((-364.0, -354.0), (-420.0, -410.0))):
        ekle("parmak_yatagi_%d" % i, kut(px - 16.0, px + 16.0, py - 16.0, py + 16.0, z0, z1).cut(silz(px, py, 6.1, z0 - 1, z1 + 1)), "celik",
             bom=("Flanşlı yatak KFL001 (Ø12)", 2, "parmak mili", "katalog") if i == 0 else None)
    ekle("parmak_yatak_askisi", kut(px - 16.0, px + 16.0, py + 16.0, Y_BES_PL, -420.0, -370.0), "aluminyum")
    ekle("parmak_yatak_kolu_on", kut(px - 16.0, px + 16.0, py + 16.0, py + 26.0, -370.0, -354.0), "aluminyum")
    pgcn23("parmak_reduktoru", (px, py, -425.0), (0, 0, 1), (0, 1, 0))
    nema23("parmak_motoru", (px, py, -504.0), (0, 0, 1), (0, 1, 0))
    ekle("parmak_red_braketi", kut(px - 29.0, px + 29.0, py + 29.0, Y_BES_PL, -432.0, -425.0), "aluminyum")
    e2e("parmak_sensor", px + 22.0, py + 20.0, -400.0, "z")


# ---------------------------------------------------------------- KAPAK MASASI · U ÇERÇEVE · KOL ----------------------------------------------------------------
KM_X = (466.0, 730.0)
KOL_Z = (ZB - 10.0, ZB + 10.0)
UC_KALK = 37.6
KM_UST = TEPSI + T / 2.0 + H_ARKA - T / 2.0          # 1148,0 · kapak masası üstü = kapaklı kutuda kapağın alt yüzü


def kapak_mekanizmasi():
    m = kut(KM_X[0], KM_X[1], KM_UST - 3.0, KM_UST, ZL0 + 1.5, ZL1 - 1.5).cut(kut(KM_X[0] - 1.0, 745.0, KM_UST - 4, KM_UST + 1, KOL_Z[0] - 3.0, KOL_Z[1] + 3.0))
    ekle("kapak_masasi", m, "sac", bom=("Kapak masası 304 · 3 mm", 1, "264 × 312 · kol yarığı", "üretim"))
    for i, zc in enumerate((ZB - 110.0, ZB + 110.0)):
        ekle("kapak_masasi_diregi_%d" % i, sily(600.0, zc, 8.0, 1000.0, KM_UST - 3.0), "celik")
    ekle("kapak_alt_plakasi", kut(440.0, 800.0, 994.0, 1000.0, -368.0, BZ1 + 20.0).cut(sily(750.0, -300.0, 15.0, 993, 1001)), "aluminyum")
    ekle("kapak_alt_plaka_ayagi_0", kut(780.0, 800.0, Y_PLINT + 3.0, 994.0, -368.0, -348.0), "aluminyum")
    ekle("kapak_alt_plaka_ayagi_1", kut(780.0, 800.0, Y_PLINT + 3.0, 994.0, BZ1, BZ1 + 20.0), "aluminyum")
    # U çerçeve: 3 ince plaka (−z, +z, +x) + +x kolunun dışında bağ; masa direkleri kılavuz
    xa = X_BL1 - H_KF - H_ARKA + T                      # kapak ucu kırımı (733,6) — kayma sonrası
    uc = kut(466.0, xa + 3.0, 1112.0, KM_UST, ZL0 - 3.0 - T, ZL0 - T)
    uc = uc.union(kut(466.0, xa + 3.0, 1112.0, KM_UST, ZL1 + T, ZL1 + 3.0 + T))
    uc = uc.union(kut(xa, xa + 3.0, 1112.0, KM_UST, ZL0 - 3.0 - T, ZL1 + 3.0 + T))
    ekle("flap_katlayici_U", uc, "sac", "KATLAYICI", bom=("Flap katlayıcı U çerçeve 304 · 3 mm", 1, "37,6 mm kalkar: kapağın 3 flapını 90° kaldırır", "üretim"))
    ekle("flap_katlayici_alt_bagi", kut(xa + 3.0, xa + 18.0, 1058.0, 1112.0, ZL0 - 3.0 - T, ZL1 + 3.0 + T).cut(sily(750.0, -300.0, 10.0, 1050, 1120)), "aluminyum", "KATLAYICI")
    ekle("flap_katlayici_somun_kolu", kut(xa + 3.0, 770.0, 1058.0, 1068.0, -330.0, -270.0).cut(sily(750.0, -300.0, 8.2, 1050, 1070)), "aluminyum", "KATLAYICI")
    sfu16("flap_katlayici_vidasi", 750.0, -300.0, 900.0, 1100.0, 5, "KATLAYICI", 1001.0)
    nema23("flap_katlayici_motoru", (750.0, 862.0, -300.0), (0, 1, 0), (0, 0, 1))
    kaplin("flap_katlayici_kaplini", 750.0, 862.0, -300.0)
    ekle("flap_katlayici_motor_braketi", kut(720.0, 780.0, 862.0, 868.0, -330.0, -270.0).cut(sily(750.0, -300.0, 20.0, 861, 869)), "aluminyum")
    ekle("flap_katlayici_yatak_braketi", kut(720.0, 780.0, 892.0, 900.0, -330.0, -270.0).cut(sily(750.0, -300.0, 6.0, 891, 901)), "aluminyum")
    ekle("flap_katlayici_braket_ayagi", kut(780.0, 790.0, 862.0, 994.0, -330.0, -270.0), "aluminyum")
    e2e("flap_katlayici_sensor", 700.0, 1030.0, -300.0, "y")
    # KOL (kapağı kaldırır, yatırır): mil z boyunca KOL_P'de, redüktör + motor önde
    px, py = KOL_P
    kol = kut(px, px + KOL_R, py - 6.0, py + 6.0, KOL_Z[0], KOL_Z[1]).union(silz(px, py, 14.0, KOL_Z[0], KOL_Z[1]))
    kol = kol.union(silz(px + KOL_R, py, 10.0, KOL_Z[0] - 2.0, KOL_Z[1] + 2.0))
    ekle("kapak_kolu", kol, "celik", "KOL", bom=("Kapak kolu 304 + makara Ø20 (POM)", 1, "R 166 · kapağı 85° dik tutar, 100° yatırır", "üretim"))
    ekle("kapak_kolu_mili", silz(px, py, 6.0, ZB - 26.0, -150.0), "celik")
    for i, (z0, z1) in enumerate(((ZB - 30.0, ZB - 20.0), (-170.0, -160.0))):
        ekle("kol_yatagi_%d" % i, kut(px - 18.0, px + 18.0, py - 18.0, py + 18.0, z0, z1).cut(silz(px, py, 6.1, z0 - 1, z1 + 1)), "celik",
             bom=("Flanşlı yatak KFL001 (Ø12)", 2, "kol mili", "katalog") if i == 0 else None)
        ekle("kol_yatak_ayagi_%d" % i, kut(px - 18.0, px + 18.0, 1000.0, py - 18.0, z0, z1), "aluminyum")
    pgcn23("kol_reduktoru", (px, py, -150.0), (0, 0, -1), (0, 1, 0))
    nema23("kol_motoru", (px, py, -71.0), (0, 0, -1), (0, 1, 0))
    ekle("kol_reduktor_braketi", kut(px - 30.0, px + 30.0, 1000.0, py - 29.0, -150.0, -140.0), "aluminyum")
    e2e("kol_sensor", px + 30.0, py - 40.0, ZB + 12.0, "z")


# ---------------------------------------------------------------- ELEKTRİK ----------------------------------------------------------------
def elektrik():
    ekle("pano_plakasi", kut(60.0, 780.0, 1565.0, 2025.0, -826.0, -822.0), "sac")
    for i, y in enumerate((1645.0, 1865.0)):
        ekle("din_rayi_%d" % i, kut(70.0, 770.0, y, y + 35.0, -822.0, -815.0), "celik", bom=("DIN ray 35 × 7,5", 2, "boy 700", "EN 60715") if i == 0 else None)
    zd = -815.0
    ekle("plc_S7-1200_1214C", kut(80.0, 190.0, 1612.5, 1712.5, zd, zd + 75.0), "siemens",
         bom=("PLC Siemens S7-1200 CPU 1214C DC/DC/DC", 1, "6ES7214-1AG40-0XB0 · 4 PTO ekseni (7 sürücü enable ile paylaşır; aynı anda en çok 3 eksen döner)", "110 × 100 × 75"))
    ekle("plc_SM1221_DI16", kut(194.0, 239.0, 1612.5, 1712.5, zd, zd + 75.0), "siemens", bom=("Siemens SM1221 DI16", 1, "6ES7221-1BH32-0XB0", "45 × 100 × 75"))
    ekle("plc_SM1222_DQ16", kut(243.0, 288.0, 1612.5, 1712.5, zd, zd + 75.0), "siemens", bom=("Siemens SM1222 DQ16", 1, "6ES7222-1BH32-0XB0 · yön + enable", "45 × 100 × 75"))
    x = 300.0
    for i, (ad_, bom) in enumerate((("guc_24V_NDR-240-24", ("Güç kaynağı Mean Well NDR-240-24", 1, "24 V 10 A · PLC + sensör", "TraceParts STEP")),
                                    ("guc_48V_NDR-240-48_a", ("Güç kaynağı Mean Well NDR-240-48", 2, "48 V 5 A · step sürücüler", "NDR-240 gövdesi (STEP 24 V ile aynı)")),
                                    ("guc_48V_NDR-240-48_b", None))):
        ekle(ad_, TC.din_parca(TC.GUC_STEP, x, 1600.0, zd + 122.8 + 0.0).translate((0, 0, -0.0)), "aluminyum", bom=bom)
        x += 67.0
    x = 90.0
    for i in range(7):                                  # 7 eksen: asansör · itici · köprü · piston · parmak · flap · kol
        ekle("surucu_STP-DRV-4830_%d" % i, TC.din_parca(TC.SURUCU_STEP, x, 1855.0, zd + 28.0), "kart",
             bom=("Step sürücü AutomationDirect SureStep STP-DRV-4830", 7, "3 A/faz · 12–48 VDC · adım/yön", "automationdirect.com · TraceParts STEP") if i == 0 else None)
        x += 50.0
    ekle("klemens_sirasi", kut(450.0, 760.0, 1867.0, 1913.0, zd, zd + 45.0), "plastik", bom=("Klemens sırası Phoenix UT 2,5", 40, "", "phoenixcontact.com"))
    for i, (x0, x1, y0, y1) in enumerate(((70.0, 770.0, 1745.0, 1785.0), (70.0, 770.0, 1965.0, 2005.0))):
        ekle("kablo_kanali_%d" % i, kut(x0, x1, y0, y1, -822.0, -797.0), "plastik", bom=("Kablo kanalı 40 × 25", 4, "pano 2 + dikey 2", "katalog") if i == 0 else None)
    ekle("kablo_kanali_dikey_alt", kut(801.0, 826.0, 100.0, 1325.0, -50.0, -25.0), "plastik")
    ekle("kablo_kanali_dikey_ust", kut(801.0, 826.0, 1345.0, 1995.0, -50.0, -25.0), "plastik")
    e3z("sensor_yigin_ustu", 770.0, 1190.0, -800.0)
    e3z("sensor_blank_var", 790.0, 1190.0, -216.0)
    e3z("sensor_kutu_dolu", SAC + 1.0, 1236.0, -250.0)


# ---------------------------------------------------------------- BLANK (hareketli kutu ağacı) ----------------------------------------------------------------
def panel(x0, x1, z0, z1, kes=None):
    p = kut(x0, x1, YB, YB + T, z0, z1)
    for c in (kes or []):
        p = p.cut(c)
    return p


def blank():
    """kutuyu KATLAMA YERİNDE, düz halde kurar; her panel kendi menteşe düğümüne bağlı (DUGUM)"""
    yarik = [kut(BX0 + T - 0.1, BX0 + 2 * T + 0.3, YB - 1, YB + T + 1, z0 - 1.0, z1 + 1.0) for z0, z1 in DIL_Z]
    ekle("B_TABAN", panel(BX0, BX1, BZ0, BZ1, yarik), "karton", "B_ROOT")
    ekle("B_YAN_ARKA", panel(BX0 + T, BX1 - T, Z_BL0, BZ0), "karton", "B_SWM")
    ekle("B_YAN_ON", panel(BX0 + T, BX1 - T, BZ1, Z_BL1), "karton", "B_SWP")
    ekle("B_TIRNAK_ARKA_ON", panel(BX0 + T - KT_L, BX0 + T - 0.3, BZ0 - KT_H - 1.0, BZ0 - 1.0), "karton", "B_CTMF")
    ekle("B_TIRNAK_ARKA_MENTESE", panel(BX1 - T + 0.3, BX1 - T + KT_L, BZ0 - KT_H - 1.0, BZ0 - 1.0), "karton", "B_CTMB")
    ekle("B_TIRNAK_ON_ON", panel(BX0 + T - KT_L, BX0 + T - 0.3, BZ1 + 1.0, BZ1 + KT_H + 1.0), "karton", "B_CTPF")
    ekle("B_TIRNAK_ON_MENTESE", panel(BX1 - T + 0.3, BX1 - T + KT_L, BZ1 + 1.0, BZ1 + KT_H + 1.0), "karton", "B_CTPB")
    ekle("B_ON_DIS", panel(BX0 - H_ON, BX0, BZ0, BZ1), "karton", "B_FO")
    ic = panel(BX0 - H_ON - H_IC, BX0 - H_ON - 0.2, BZ0 + 2.0, BZ1 - 2.0)
    for z0, z1 in DIL_Z:
        ic = ic.union(panel(X_BL0, BX0 - H_ON - H_IC + 0.1, z0, z1))
    ekle("B_ON_IC_KILITLI", ic, "karton", "B_FI")
    ekle("B_ARKA_MENTESE", panel(BX1, BX1 + H_ARKA, BZ0, BZ1), "karton", "B_BW")
    xk0 = BX1 + H_ARKA
    ekle("B_KAPAK", panel(xk0 + 0.2, xk0 + L_KAP, ZL0, ZL1), "karton", "B_LID")
    ekle("B_KAPAK_ON_FLAP", panel(xk0 + L_KAP + 0.2, X_BL1, ZL0 + 3.0, ZL1 - 3.0), "karton", "B_LF")
    ekle("B_KAPAK_YAN_ARKA", panel(xk0 + 40.0, xk0 + L_KAP - 4.0, ZL0 - H_KF, ZL0 - 0.2), "karton", "B_LSM")
    ekle("B_KAPAK_YAN_ON", panel(xk0 + 40.0, xk0 + L_KAP - 4.0, ZL1 + 0.2, ZL1 + H_KF), "karton", "B_LSP")


# DÜĞÜMLER: ad -> (ebeveyn, menteşe noktası (dünya, düz blank), eksen)
DUGUM = {
    "B_ROOT": (None, (0.0, 0.0, 0.0), None),
    "B_SWM": ("B_ROOT", (0.0, YB + T, BZ0), "x"),
    "B_SWP": ("B_ROOT", (0.0, YB + T, BZ1), "x"),
    "B_CTMF": ("B_SWM", (BX0 + T, YB + T, 0.0), "z"),
    "B_CTMB": ("B_SWM", (BX1 - T, YB + T, 0.0), "z"),
    "B_CTPF": ("B_SWP", (BX0 + T, YB + T, 0.0), "z"),
    "B_CTPB": ("B_SWP", (BX1 - T, YB + T, 0.0), "z"),
    "B_FO": ("B_ROOT", (BX0, YB + T, 0.0), "z"),
    "B_FI": ("B_FO", (BX0 - H_ON, YB + 1.5 * T, 0.0), "z"),
    "B_BW": ("B_ROOT", (BX1, YB + T / 2.0, 0.0), "z"),
    "B_LID": ("B_BW", (BX1 + H_ARKA, YB + T / 2.0, 0.0), "z"),
    "B_LF": ("B_LID", (BX1 + H_ARKA + L_KAP, YB + T, 0.0), "z"),
    "B_LSM": ("B_LID", (0.0, YB + T, ZL0), "x"),
    "B_LSP": ("B_LID", (0.0, YB + T, ZL1), "x"),
}


# ---------------------------------------------------------------- ROBOT ÇATALI · PİZZA · K REFERANSI ----------------------------------------------------------------
CATAL_DIS = 700.0


def catal_pizza():
    for i, (x0, x1) in enumerate(X_CATAL):
        ekle("robot_catal_disi_%d" % i, kut(x0, x1, 1094.0, 1102.0, BZ0 + 2.0 + CATAL_DIS, 60.0 + CATAL_DIS), "robot", "CATAL")
    ekle("robot_catal_govdesi", kut(140.0, 380.0, 1080.0, 1112.0, 60.0 + CATAL_DIS, 76.0 + CATAL_DIS), "robot", "CATAL",
         bom=("[R modülü] FR5 kutu çatalı — robot aletidir, E'ye dahil değil", 0, "3 diş 26 × 8 × 430", "robot"))
    ekle("robot_flansi", silz(260.0, 1096.0, 31.5, 76.0 + CATAL_DIS, 96.0 + CATAL_DIS), "robot", "CATAL")
    # pizza (K plakasının üstünde bekler): Ø300 hamur + Ø284 sos/peynir
    ekle("pizza_hamur", sily(-300.0, -170.0, 150.0, PLAKA_K, PLAKA_K + 10.0), "hamur", "PIZZA")
    ekle("pizza_ustu", sily(-300.0, -170.0, 142.0, PLAKA_K + 10.0, PLAKA_K + 15.0), "sos", "PIZZA")
    # K modülü referansı (saydam): plakanın ucu + itici
    ekle("REF_K_kesme_plakasi_ucu", kut(-320.0, -20.0, PLAKA_K - 14.0, PLAKA_K, -470.0, -20.0), "referans", "SABIT_REF")
    ekle("REF_K_itici", kut(-490.0, -450.0, PLAKA_K + 2.0, PLAKA_K + 50.0, -320.0, -20.0), "referans", "K_ITICI")


# ---------------------------------------------------------------- KİNEMATİK (tek kaynak: GLB animasyonu + çakışma taraması) ----------------------------------------------------------------
DONGU = 20.0
# ZAMAN ÇİZELGESİ (sn) — her satır bir hareket; GLB ve çakışma taraması AYNI fonksiyonları çağırır
Z_BESLE = (0.5, 1.7)          # itici blankı şarjörden kalıba sürer
Z_ITICI_DON = (1.8, 2.8)
Z_INIS = (1.9, 2.7)           # kafa blankın üstüne iner
Z_ZIMBA = (2.7, 3.3)          # taban 45,6 mm kalıba girer, duvarlar kalkar
Z_KALK1 = (3.3, 4.0)          # kafa yukarı (parmağa yer)
Z_PARMAK = (4.0, 4.5, 5.0)    # parmak iner / döner
Z_VURUS2 = (5.0, 5.6, 5.7, 6.4)   # 2. vuruş: in, bekle, çık
Z_KOPRU = (5.8, 6.2, 18.3, 18.7)
Z_FLAP = (6.4, 6.8, 7.4, 7.8)     # U çerçeve kalkar / iner
Z_KOL = (6.8, 7.15, 8.1)          # kol temas, kapak 85°
Z_PIZZA = (8.5, 10.1, 10.35)      # K itici sürer, pizza düşer
Z_KITICI_DON = (10.3, 11.3)
Z_KAFA_HAZIR = (10.6, 10.9)       # kafa dik kapağın üstüne (1462)
Z_YATIR = (10.9, 11.2)            # kol kapağı 100°'ye yatırır
Z_KAPAT = (11.2, 12.6, 12.9, 13.7)    # kafa kapağı kapatır, bastırır, çıkar
Z_KOL_DON = (11.25, 12.2)
Z_CATAL = (13.9, 15.1, 15.6, 17.3)    # robot çatalı gelir, kaldırır, çeker
Z_GIZLE = (19.6, 19.98)
KAPAK_BASKI = KMER[1] + T / 2.0 + 0.2          # kapak kapalıyken üst yüzü
H_BEKLE = 1467.0                 # dik kapak 85°'de: ön flap ucu 1464,3


def ss(a, b, t):
    if t <= a: return 0.0
    if t >= b: return 1.0
    x = (t - a) / (b - a); return x * x * (3.0 - 2.0 * x)


def lin(a, b, t):
    if t <= a: return 0.0
    if t >= b: return 1.0
    return (t - a) / (b - a)


def kafa(t):
    """piston kafası alt yüzü (y)"""
    if t < Z_INIS[0]: return H_UST
    if t < Z_INIS[1]: return H_UST + (YB + T - H_UST) * ss(Z_INIS[0], Z_INIS[1], t)
    if t < Z_ZIMBA[1]: return (YB + T) + (TEPSI + T - (YB + T)) * lin(Z_ZIMBA[0], Z_ZIMBA[1], t)
    if t < Z_KALK1[1]: return (TEPSI + T) + (H_UST - (TEPSI + T)) * ss(Z_KALK1[0], Z_KALK1[1], t)
    if t < Z_VURUS2[0]: return H_UST
    if t < Z_VURUS2[1]: return H_UST + (1108.0 - H_UST) * ss(Z_VURUS2[0], Z_VURUS2[1], t)
    if t < Z_VURUS2[2]: return 1108.0
    if t < Z_VURUS2[3]: return 1108.0 + (H_UST - 1108.0) * ss(Z_VURUS2[2], Z_VURUS2[3], t)
    if t < Z_KAFA_HAZIR[0]: return H_UST
    if t < Z_KAFA_HAZIR[1]: return H_UST + (H_BEKLE - H_UST) * ss(Z_KAFA_HAZIR[0], Z_KAFA_HAZIR[1], t)
    if t < Z_KAPAT[0]: return H_BEKLE
    if t < Z_KAPAT[1]: return H_BEKLE + (KAPAK_BASKI - H_BEKLE) * ss(Z_KAPAT[0], Z_KAPAT[1], t)
    if t < Z_KAPAT[2]: return KAPAK_BASKI
    if t < Z_KAPAT[3]: return KAPAK_BASKI + (H_UST - KAPAK_BASKI) * ss(Z_KAPAT[2], Z_KAPAT[3], t)
    return H_UST


def u_zimba(t):
    """tabanın kalıba giriş derinliği (kafa kalksa da kutu aşağıda kalır)"""
    if t < Z_ZIMBA[0]: return 0.0
    if t < Z_ZIMBA[1]: return U_MAX * lin(Z_ZIMBA[0], Z_ZIMBA[1], t)
    return U_MAX


def parmak_psi(t):
    """parmak açısı (+z etrafında, derece): 0 = dik yukarı, −140 = kutunun içine eğik"""
    return -140.0 * (ss(Z_PARMAK[0], Z_PARMAK[1], t) - ss(Z_PARMAK[1], Z_PARMAK[2], t))


def kapak_acisi_kafa(h):
    s = (h - (KMER[1] + T / 2.0 + 1.5)) / L_KAP             # 1,5: kapak ucu + flap kökü kafanın altında kalsın
    s = max(-1.0, min(1.0, s))
    return 180.0 - math.degrees(math.asin(s))


def kol_icin_beta(alfa):
    """kapak açısı alfa (derece, düz +x = 0) için kol açısı: makara kapağın dış yüzüne değer"""
    a = math.radians(alfa); hx, hy = KMER
    def f(b):
        cx = KOL_P[0] + KOL_R * math.cos(b); cy = KOL_P[1] + KOL_R * math.sin(b)
        return math.sin(a) * (cx - hx) - math.cos(a) * (cy - hy) - (10.0 + T / 2.0)
    lo, hi = 0.0, math.radians(175.0)
    flo = f(lo)
    for _ in range(80):
        mid = (lo + hi) / 2.0; fm = f(mid)
        if (fm > 0) == (flo > 0): lo, flo = mid, fm
        else: hi = mid
    return math.degrees((lo + hi) / 2.0)


BETA_TEMAS = kol_icin_beta(0.0)
BETA_100 = kol_icin_beta(100.0)


def kapak_alfa(t):
    """kapağın dünya açısı: 0 = masada düz (+x), 90 = dik, 180 = kapalı"""
    if t < Z_KOL[1]: return 0.0
    if t < Z_KOL[2]: return 85.0 * ss(Z_KOL[1], Z_KOL[2], t)
    if t < Z_YATIR[0]: return 85.0
    if t < Z_YATIR[1]: return 85.0 + 15.0 * ss(Z_YATIR[0], Z_YATIR[1], t)
    if t < Z_KAPAT[1] + 0.05: return min(180.0, max(100.0, kapak_acisi_kafa(kafa(t))))
    return 180.0


def kol_beta(t):
    if t < Z_KOL[0]: return 0.0
    if t < Z_KOL[1]: return BETA_TEMAS * ss(Z_KOL[0], Z_KOL[1], t)
    if t < Z_YATIR[1]: return kol_icin_beta(kapak_alfa(t))
    return BETA_100 * (1.0 - ss(Z_KOL_DON[0], Z_KOL_DON[1], t))


def katlayici_dy(t):
    return UC_KALK * (ss(Z_FLAP[0], Z_FLAP[1], t) - ss(Z_FLAP[2], Z_FLAP[3], t))


def kopru_dy(t):
    return KOPRU_ALT * (ss(Z_KOPRU[0], Z_KOPRU[1], t) - ss(Z_KOPRU[2], Z_KOPRU[3], t))


def itici_dz(t):
    return BESLE * (ss(Z_BESLE[0], Z_BESLE[1], t) - ss(Z_ITICI_DON[0], Z_ITICI_DON[1], t))


def catal_trs(t):
    """çatal dinlenmede ağzın 700 mm önünde (koridorda)"""
    dz = -CATAL_DIS * ss(Z_CATAL[0], Z_CATAL[1], t) + 900.0 * ss(Z_CATAL[2], Z_CATAL[3], t)
    dy = 55.0 * ss(Z_CATAL[1], Z_CATAL[2], t)
    return (0.0, dy, dz)


def catal_kutu(t):
    """kutunun çatalla birlikte ötelenmesi (kaldırma anından itibaren)"""
    if t < Z_CATAL[1]: return (0.0, 0.0)
    c = catal_trs(t)
    return (c[1], c[2] + CATAL_DIS)


PIZZA_X0, PIZZA_Z0 = -300.0, -170.0


def pizza_trs(t):
    """K itici (2 eksen) pizzayı K plakasının üstünde 36 mm içeri kaydırır (z −170 → −206), sonra düz iter.
    Kayma pizzanın ön kenarı E'ye girmeden BİTER (x −300 → −160): köşe plow'ları ve pencere kenarı pizzanın yolunda kalmaz
    (düz 3,1° çapraz itişte pizza +z plow'una 2,6 mm, pencereye 2 mm değiyordu — pizza taraması)."""
    k = ss(Z_PIZZA[0], Z_PIZZA[1], t)
    x = PIZZA_X0 + (260.0 - PIZZA_X0) * k
    z = PIZZA_Z0 + (ZB - PIZZA_Z0) * ss(0.0, 0.25, k)
    if x <= -20.0: y = PLAKA_K
    elif x <= 40.0: y = PLAKA_K + (KALIP - PLAKA_K) * (x + 20.0) / 60.0
    else: y = KALIP
    y = y + (TEPSI + T - KALIP) * ss(Z_PIZZA[1], Z_PIZZA[2], t)
    dy_c, dz_c = catal_kutu(t)
    return (x - PIZZA_X0, y - PLAKA_K + dy_c, z - PIZZA_Z0 + dz_c)


def k_itici_trs(t):
    """K iticisinin referans hareketi: pizzayı arkasından iter (x) ve onunla birlikte 36 mm içeri kayar (z)"""
    k = ss(Z_PIZZA[0], Z_PIZZA[1], t)
    x_arka = (PIZZA_X0 + (260.0 - PIZZA_X0) * k) - 150.0          # pizzanın arka kenarı
    dz = (ZB - PIZZA_Z0) * ss(0.0, 0.25, k)
    if t <= Z_PIZZA[1]: return (max(0.0, x_arka - (-450.0)), 0.0, dz)
    geri = 1.0 - ss(Z_KITICI_DON[0], Z_KITICI_DON[1], t)
    return ((260.0 - 150.0 + 450.0) * geri, 0.0, (ZB - PIZZA_Z0) * geri)


def _kose_ustu(dy, d):
    """panel, kıvrımının (menteşe = panelin ÜST yüz kenarı) d mm dışındaki ve dy mm yukarısındaki bir köşenin
    ÜSTÜNDEN dönerek kalkar. Panelin ALT yüzü köşeye değer (kalınlık T): köşe, üst yüz çizgisinin T altında kalmalı →
    d·sinθ − dy·cosθ ≥ T  →  θ = φ + asin(T/r),  φ = atan2(dy, d), r = √(dy² + d²)"""
    r = math.hypot(dy, d)
    if r <= T:
        return 0.0
    th = math.degrees(math.atan2(dy, d) + math.asin(T / r))
    return max(0.0, min(90.0, th))


def _ray_uzeri(u, y_kose, d):
    """kalıp rayının iç üst köşesi (y_kose, kıvrımdan d mm dışarıda); kıvrım y = YB + T − u"""
    return _kose_ustu(y_kose - (YB + T - u), d)


def blank_acilar(t):
    """(kök öteleme, {düğüm: açı derece}) — açılar kalıp geometrisinden (el ile yazılmış eğri değil)"""
    u = u_zimba(t)
    dz = -BESLE * (1.0 - ss(Z_BESLE[0], Z_BESLE[1], t))
    dy = -u
    dy_c, dz_c = catal_kutu(t)
    dy += dy_c; dz += dz_c
    # yan duvarlar: arka ray / ön tarak iç üst köşesi (1149,5; kıvrımdan 2,1 mm dışarıda); sonda duvar raya yaslanır (90°)
    th_s = max(_ray_uzeri(u, KALIP, 2.1), 90.0 * ss(U_MAX - 4.0, U_MAX, u))
    # köşe tırnakları: yan duvar 30°'yi geçince içe döner (kalıp köşesi), yan duvar 80°'de bitmiş olur
    th_t = 90.0 * ss(30.0, 80.0, th_s)
    # ön dış duvar: ön ray 20 mm alçak (1129,5) → tırnaklardan SONRA kalkar; kilitlenince 90°
    th_f = _ray_uzeri(u, 1129.5, 2.1)
    if t >= Z_VURUS2[0]:
        th_f = th_f + (90.0 - th_f) * ss(Z_VURUS2[0], Z_VURUS2[1], t)
    th_bw = math.degrees(math.asin(min(u, H_ARKA - 0.001) / H_ARKA)) if u < H_ARKA else 90.0
    # iç ön panel: parmak iter (0 → −70), yerçekimiyle içeri düşer ve kilit dilleri TABANA dayanır (−145),
    # 2. vuruşta kafa paneli dikleştirir, diller yarıklardan tepsinin cebine iner (−180)
    if t < Z_PARMAK[0] + 0.12: fi = 0.0
    elif t < Z_PARMAK[1]: fi = -70.0 * ss(Z_PARMAK[0] + 0.12, Z_PARMAK[1], t)
    elif t < Z_PARMAK[1] + 0.35: fi = -70.0 - 75.0 * ss(Z_PARMAK[1], Z_PARMAK[1] + 0.35, t)
    elif t < Z_VURUS2[0] + 0.3: fi = -145.0
    else: fi = -145.0 - 35.0 * ss(Z_VURUS2[0] + 0.3, Z_VURUS2[1], t)
    alfa = kapak_alfa(t)
    gam = alfa - th_bw
    # kapak flapları: U çerçevenin kolu kırımın 1,6 mm dışında kalkar → flap kolun iç üst köşesinden döner
    if t < Z_FLAP[1]:
        th_fl = _kose_ustu(KM_UST + katlayici_dy(t) - (KM_UST + T), T)      # kolun iç üst köşesi kırımdan 1,6 dışarıda
    else:
        th_fl = 90.0
    A = {"B_SWM": th_s, "B_SWP": -th_s, "B_CTMF": -th_t, "B_CTMB": th_t, "B_CTPF": -th_t, "B_CTPB": th_t,
         "B_FO": -th_f, "B_FI": fi, "B_BW": th_bw, "B_LID": gam, "B_LF": th_fl, "B_LSM": th_fl, "B_LSP": -th_fl}
    return (0.0, dy, dz), A


def gorunur(t):
    """kutu + pizza robotla çıktıktan sonra döngü başına dönerken gizlenir"""
    return 0.0 if Z_GIZLE[0] <= t < Z_GIZLE[1] else 1.0


# ---------------------------------------------------------------- 4x4 MATRİS ----------------------------------------------------------------
def mm4(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def tr4(v):
    return [[1, 0, 0, v[0]], [0, 1, 0, v[1]], [0, 0, 1, v[2]], [0, 0, 0, 1]]


def rot4(eksen, derece):
    a = math.radians(derece); c, s = math.cos(a), math.sin(a)
    if eksen == "x": return [[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]]
    if eksen == "y": return [[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]]
    return [[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]


def quat(eksen, derece):
    a = math.radians(derece) / 2.0; s = math.sin(a)
    v = {"x": (s, 0.0, 0.0), "y": (0.0, s, 0.0), "z": (0.0, 0.0, s)}[eksen]
    return (v[0], v[1], v[2], math.cos(a))


def grup_matrisi(grup, t):
    """makine grubunun dünya dönüşümü (dinlenme konumundaki katıya uygulanır)"""
    if grup == "ITICI": return tr4((0.0, 0.0, itici_dz(t)))
    if grup == "PISTON": return tr4((0.0, kafa(t) - H_UST, 0.0))
    if grup == "KOPRU": return tr4((0.0, kopru_dy(t), 0.0))
    if grup == "KATLAYICI": return tr4((0.0, katlayici_dy(t), 0.0))
    if grup == "KOL": return mm4(mm4(tr4((KOL_P[0], KOL_P[1], 0.0)), rot4("z", kol_beta(t))), tr4((-KOL_P[0], -KOL_P[1], 0.0)))
    if grup == "PARMAK": return mm4(mm4(tr4((PARMAK_P[0], PARMAK_P[1], 0.0)), rot4("z", parmak_psi(t))), tr4((-PARMAK_P[0], -PARMAK_P[1], 0.0)))
    if grup == "CATAL": return tr4(catal_trs(t))
    if grup == "PIZZA": return tr4(pizza_trs(t))
    if grup == "K_ITICI": return tr4(k_itici_trs(t))
    return tr4((0.0, 0.0, 0.0))


def blank_dunya(t):
    """her blank düğümünün dünya matrisi × T(−menteşe): dinlenme katısına uygulanacak dönüşüm"""
    kok, A = blank_acilar(t)
    W = {}
    sira = ["B_ROOT", "B_SWM", "B_SWP", "B_FO", "B_BW", "B_CTMF", "B_CTMB", "B_CTPF", "B_CTPB", "B_FI", "B_LID", "B_LF", "B_LSM", "B_LSP"]
    for d in sira:
        par, P, eks = DUGUM[d]
        if par is None:
            W[d] = tr4(kok)
            continue
        Pp = DUGUM[par][1] if DUGUM[par][0] is not None else (0.0, 0.0, 0.0)
        lok = mm4(tr4((P[0] - Pp[0], P[1] - Pp[1], P[2] - Pp[2])), rot4(eks, A[d]))
        W[d] = mm4(W[par], lok)
    return {d: mm4(W[d], tr4((-DUGUM[d][1][0], -DUGUM[d][1][1], -DUGUM[d][1][2]))) for d in W}


def uygula(sh, M):
    return tasi(sh, M)


# ---------------------------------------------------------------- DENETİM ----------------------------------------------------------------
HAREKETLI = ("ITICI", "PISTON", "KOPRU", "KATLAYICI", "KOL", "PARMAK", "ASANSOR")
KONTROL_ANLARI = tuple(round(0.1 * i, 2) for i in range(201))          # her 0,1 sn
GECIS_ANLARI = (0.6, 0.9, 1.2, 1.5, 2.75, 2.8, 2.9, 3.0, 3.1, 3.2, 4.2, 4.35, 4.5, 4.65, 4.8, 5.3, 5.5, 6.5, 6.6, 6.7,
                7.3, 7.5, 7.7, 7.9, 10.95, 11.05, 11.15, 11.3, 11.5, 11.7, 11.9, 12.1, 12.3, 12.5, 15.2, 15.4, 15.8, 16.2, 16.6, 17.0)
PIZZA_ANLARI = tuple(round(8.5 + 0.1 * i, 2) for i in range(20)) + (12.8, 15.4, 15.8, 16.4, 17.0)
KUTU_ANLARI = (1.7, 4.0, 7.0, 8.1, 12.6, 15.6)          # kutunun durağan anları: düz · katlı · flaplar · dik kapak · kapalı · çatalda


def _bb_kesisir(A, B, pay=0.05):
    return not (A.xmin >= B.xmax - pay or B.xmin >= A.xmax - pay or A.ymin >= B.ymax - pay or B.ymin >= A.ymax - pay or A.zmin >= B.zmax - pay or B.zmin >= A.zmax - pay)


# tasarım gereği değen/kesişen çiftler (sebebiyle): bunlar sayılmaz
ISTISNA = [
    ("_rayi_", "_arabasi_"),                   # HIWIN araba ray üstünde (STEP'te boşluklu; güvenlik için)
    ("_vidasi_mil", "_vidasi_somun"),
    ("_vidasi_mil", "_BK12"), ("_vidasi_mil", "_BF12"),
    ("asansor_vidasi", "asansor_somunu"), ("asansor_vidasi", "asansor_alt_yatak"), ("asansor_vidasi", "asansor_ust_yatak"), ("asansor_vidasi", "asansor_kasnak"),
    ("_kasnak_", "_kayisi"), ("_kasnak_", "_motoru"), ("_kasnak_", "_vidasi_mil"),
    ("_kaplini", "_motoru"), ("_kaplini", "_vidasi_mil"), ("_kaplini", "_BK12"),
    ("kapak_kolu_mili", "kapak_kolu"), ("kapak_kolu_mili", "kol_yatagi"), ("kapak_kolu_mili", "kol_reduktoru"),
    ("parmak_mili", "devirme_parmagi"), ("parmak_mili", "parmak_yatagi"), ("parmak_mili", "parmak_reduktoru"),
    ("_reduktoru", "_motoru"),
    ("kopru_kilavuz_mili", "kopru_burcu"), ("kopru_kilavuz_mili", "kopru_burc_plakasi"),
    ("kapak_masasi_diregi", "kapak_masasi"), ("kapak_masasi_diregi", "kapak_alt_plakasi"),
    ("ayak_", "taban_sac"),
    ("avara_yatagi", "avara_mili"), ("_kasnak_", "avara_mili"),
]


def _istisna(a, b):
    for p, q in ISTISNA:
        if (p in a and q in b) or (p in b and q in a):
            return True
    return False


_SABIT_ONBELLEK = []


def _katilar(t, gruplar=None):
    """t anında makine parçaları (blank ve pizza hariç) dünya konumunda · sabitler bir kez hesaplanır"""
    if not _SABIT_ONBELLEK:
        for p in PARCALAR:
            if p["grup"] == "SABIT":
                sh = p["wp"].val(); _SABIT_ONBELLEK.append((p, sh, sh.BoundingBox()))
    L = list(_SABIT_ONBELLEK)
    for p in PARCALAR:
        g = p["grup"]
        if g.startswith("B_") or g in ("PIZZA", "CATAL", "K_ITICI", "SABIT_REF", "SABIT"):
            continue
        if gruplar and g not in gruplar:
            continue
        sh = uygula(p["wp"].val(), grup_matrisi(g, t))
        L.append((p, sh, sh.BoundingBox()))
    return L


def cakisma(esik=1.0):
    t0 = time.time()
    sabit = [(p, p["wp"].val()) for p in PARCALAR if p["grup"] == "SABIT"]
    sabit = [(p, v, v.BoundingBox()) for p, v in sabit]
    bul = {}
    # 1) sabit parçalar kendi aralarında
    for i, (p, a, A) in enumerate(sabit):
        for q, b, Bb in sabit[i + 1:]:
            if not _bb_kesisir(A, Bb) or _istisna(p["ad"], q["ad"]):
                continue
            v = a.intersect(b).Volume()
            if v > esik:
                bul[(p["ad"], q["ad"])] = (v, "sabit")
    # 2) her kontrol anında hareketliler × (sabit + hareketli)
    for t in KONTROL_ANLARI:
        H_ = []
        for p in PARCALAR:
            g = p["grup"]
            if g in HAREKETLI or g == "CATAL":
                sh = uygula(p["wp"].val(), grup_matrisi(g, t))
                H_.append((p, sh, sh.BoundingBox()))
        hepsi = H_ + sabit
        for i, (p, a, A) in enumerate(H_):
            for q, b, Bb in hepsi[i + 1:]:
                if q is p or (q["grup"] == p["grup"]) or not _bb_kesisir(A, Bb) or _istisna(p["ad"], q["ad"]):
                    continue
                v = a.intersect(b).Volume()
                if v > esik and (p["ad"], q["ad"]) not in bul:
                    bul[(p["ad"], q["ad"])] = (v, "t=%.2f" % t)
    print("CAKISMA TARAMASI (makine): %d parca · %d an · %d cakisma (> %.0f mm3) · %.0f sn" % (len(PARCALAR), len(KONTROL_ANLARI), len(bul), esik, time.time() - t0))
    for (a, b), (v, an) in sorted(bul.items(), key=lambda kv: -kv[1][0])[:200]:
        print("    %10.1f mm3  %-8s %s <-> %s" % (v, an, a, b))
    return bul


def kutu_cakisma(esik=1.0, anlar=None, etiket="duragan"):
    """kutunun durağan anlarında karton × makine (+ pizza)"""
    t0 = time.time()
    bul = {}
    anlar = anlar or KUTU_ANLARI
    for t in anlar:
        W_ = blank_dunya(t)
        kart = [(p, uygula(p["wp"].val(), W_[p["grup"]])) for p in PARCALAR if p["grup"].startswith("B_")]
        kart = [(p, v, v.BoundingBox()) for p, v in kart]
        mak = _katilar(t)
        for p in PARCALAR:
            if p["grup"] in ("PIZZA", "CATAL"):
                sh = uygula(p["wp"].val(), grup_matrisi(p["grup"], t)); mak.append((p, sh, sh.BoundingBox()))
        for p, a, A in kart:
            for q, b, Bb in mak:
                if not _bb_kesisir(A, Bb):
                    continue
                v = a.intersect(b).Volume()
                if v > esik:
                    bul[(p["ad"], q["ad"], t)] = v
    print("CAKISMA TARAMASI (kutu x makine, %s): %d an · %d cakisma · %.0f sn" % (etiket, len(anlar), len(bul), time.time() - t0))
    for (a, b, t), v in sorted(bul.items(), key=lambda kv: -kv[1])[:40]:
        print("    %10.1f mm3  t=%.2f  %s <-> %s" % (v, t, a, b))
    return bul


def pizza_cakisma(esik=1.0):
    """pizza K plakasından kutuya kayarken ve robotla çıkarken: pizza × makine ve pizza × karton"""
    t0 = time.time(); bul = {}
    pz = [p for p in PARCALAR if p["grup"] == "PIZZA"]
    for t in PIZZA_ANLARI:
        Pz = [(p, uygula(p["wp"].val(), grup_matrisi("PIZZA", t))) for p in pz]
        W_ = blank_dunya(t)
        diger = _katilar(t) + [(q, uygula(q["wp"].val(), W_[q["grup"]]), None) for q in PARCALAR if q["grup"].startswith("B_")]
        diger = [(q, b_, bb_ or b_.BoundingBox()) for q, b_, bb_ in diger]
        for q in PARCALAR:
            if q["grup"] in ("CATAL", "K_ITICI"):
                sh = uygula(q["wp"].val(), grup_matrisi(q["grup"], t)); diger.append((q, sh, None))
        for p, a in Pz:
            A = a.BoundingBox()
            for q, b, Bb in diger:
                if q["ad"] == "REF_K_itici" or (q["grup"] == "SABIT_REF"):
                    continue
                if not _bb_kesisir(A, Bb or b.BoundingBox()):
                    continue
                v = a.intersect(b).Volume()
                if v > esik:
                    bul[(p["ad"], q["ad"], t)] = v
    print("CAKISMA TARAMASI (pizza): %d an · %d cakisma · %.0f sn" % (len(PIZZA_ANLARI), len(bul), time.time() - t0))
    for (a, b, t), v in sorted(bul.items(), key=lambda kv: -kv[1])[:40]:
        print("    %10.1f mm3  t=%.2f  %s <-> %s" % (v, t, a, b))
    return bul


def olcum():
    """tasarım iddialarını ölçerek yazdır (varsayım değil)"""
    W_ = blank_dunya(12.9)
    kutu = None
    for p in PARCALAR:
        if p["grup"].startswith("B_"):
            sh = uygula(p["wp"].val(), W_[p["grup"]])
            kutu = sh if kutu is None else kutu.fuse(sh)
    b = kutu.BoundingBox()
    print("KAPALI KUTU (olculdu): x %.1f..%.1f (%.1f) · y %.1f..%.1f (%.1f) · z %.1f..%.1f (%.1f)" % (b.xmin, b.xmax, b.xlen, b.ymin, b.ymax, b.ylen, b.zmin, b.zmax, b.zlen))
    W0 = blank_dunya(1.7)
    duz = None
    for p in PARCALAR:
        if p["grup"].startswith("B_"):
            sh = uygula(p["wp"].val(), W0[p["grup"]])
            duz = sh if duz is None else duz.fuse(sh)
    d = duz.BoundingBox()
    print("DUZ ACILIM (kalipta): %.0f x %.0f mm · x %.1f..%.1f · z %.1f..%.1f (on yuz 0: %.1f mm iceride)" % (d.xlen, d.zlen, d.xmin, d.xmax, d.zmin, d.zmax, -d.zmax))
    assert d.zmax <= -2.0 and d.xmin >= SAC + 2.0 and d.xmax <= W - SAC - 2.0, "duz blank modul disina tasiyor"
    yig = Y_YIGIN_UST - Y_PLAT
    print("SARJOR: yigin %.0f mm = %d kutu @1,6 mm · %d @1,8 mm  (gunde 80 pide + 200 lahmacun = 280 urun; 3 lahmacun/kutu ile ~170 kutu/gun)" % (yig, yig / 1.6, yig / 1.8))
    print("DONGU: blank -> katli kutu %.1f sn · kapak kapatma %.1f sn · tam dongu %.0f sn (sim varsayimi: katlama 15 sn, kapak 3 sn)" %
          (Z_KOL[2] - Z_BESLE[0], Z_KAPAT[2] - Z_YATIR[0], DONGU))
    print("KAPAK KOLU: temas %.1f der · kapak 85 der icin %.1f der · 100 der icin %.1f der" % (BETA_TEMAS, kol_icin_beta(85.0), BETA_100))
    # asansör torku (Tr16x4, eta 0,35, 2:1 kayış)
    m = (yig / 1.6) * 0.160 + 10.0
    Tm = m * 9.81 * 0.004 / (2 * math.pi * 0.35) / 2.0
    print("ASANSOR: yuk %.0f kg -> motor torku %.2f N.m (STP-MTR-23079 tutma 1,95) · Tr16x4 kendinden kilitli" % (m, Tm))
    assert Tm < 1.95 * 0.6
    # piston kuvveti (SFU1610, eta 0,9, 1:1) — 1800 d/dk'da motor ~0,3 N.m
    F = 2 * math.pi * 0.9 * 0.3 / 0.010
    print("PISTON: 1800 d/dk'da ~%.0f N itme (katlama kuvveti tahmini 50-100 N) · hiz %.0f mm/s" % (F, 1800 / 60.0 * 10.0))


# ---------------------------------------------------------------- GLB (hiyerarşik düğüm + animasyon) ----------------------------------------------------------------
def _ag(wp, kaba=False):
    import kiyma_cad_v6 as _K
    if kaba:
        from OCP.BRepTools import BRepTools
        sh = wp.val().copy()
        BRepTools.Clean_s(sh.wrapped)
        return _K.ag(cq.Workplane(obj=sh), 0.6, 0.8)
    return _K.ag(wp, 0.3, 0.5)


def glb_yaz(yol, adim=1.0 / 15.0):
    """düğüm başına (grup) malzeme-mesh; blank düğümleri menteşe ağacı; animasyon aynı kinematikten örneklenir"""
    GRUPLAR = ["SABIT", "SABIT_REF", "ASANSOR", "ITICI", "PISTON", "KOPRU", "KATLAYICI", "KOL", "PARMAK", "CATAL", "PIZZA", "K_ITICI"] + list(DUGUM.keys())
    mesh_g = {g: {} for g in GRUPLAR}
    for p in PARCALAR:
        g = p["grup"]
        kaba = p["ad"].startswith(("surucu_", "guc_", "asansor_motoru", "besleyici_motoru", "piston_motoru", "kopru_motoru", "flap_katlayici_motoru", "kol_motoru", "kol_reduktoru", "parmak_motoru", "parmak_reduktoru"))
        m = _ag(p["wp"], kaba)
        mesh_g[g].setdefault(p["mal"], Mesh()).ekle(m)
    # düğüm ağacı
    nodes, idx = [], {}
    def pivot(g):
        if g == "KOL": return (KOL_P[0], KOL_P[1], 0.0)
        if g == "PARMAK": return (PARMAK_P[0], PARMAK_P[1], 0.0)
        if g in DUGUM: return DUGUM[g][1]
        return (0.0, 0.0, 0.0)
    for g in GRUPLAR:
        P = pivot(g)
        par = DUGUM[g][0] if g in DUGUM else None
        Pp = pivot(par) if par else (0.0, 0.0, 0.0)
        n = {"name": g, "translation": [(P[0] - Pp[0]) * MM, (P[1] - Pp[1]) * MM, (P[2] - Pp[2]) * MM]}
        idx[g] = len(nodes); nodes.append(n)
    for g in GRUPLAR:
        if g in DUGUM and DUGUM[g][0]:
            nodes[idx[DUGUM[g][0]]].setdefault("children", []).append(idx[g])
    kok = [idx[g] for g in GRUPLAR if not (g in DUGUM and DUGUM[g][0])]
    # mesh: köşeler düğümün menteşesine göre
    blob, views, accs, meshes, mats, mat_idx = [], [], [], [], [], {}
    off = [0]
    def gomu(bt, hedef=None):
        while off[0] % 4: blob.append(b"\x00"); off[0] += 1
        v = {"buffer": 0, "byteOffset": off[0], "byteLength": len(bt)}
        if hedef: v["target"] = hedef
        views.append(v); blob.append(bt); off[0] += len(bt); return len(views) - 1
    def mat(k):
        if k not in mat_idx:
            d = MALZEME[k]; pbr = {"baseColorFactor": list(d["renk"]), "metallicFactor": d["met"], "roughnessFactor": d["ruf"]}
            mm_ = {"name": k, "pbrMetallicRoughness": pbr, "doubleSided": True}
            if d.get("saydam"): mm_["alphaMode"] = "BLEND"
            mat_idx[k] = len(mats); mats.append(mm_)
        return mat_idx[k]
    ucgen = 0
    for g in GRUPLAR:
        if not mesh_g[g]:
            continue
        P = pivot(g)
        prims = []
        for k, m in sorted(mesh_g[g].items()):
            pts = [(q[0] - P[0] * MM, q[1] - P[1] * MM, q[2] - P[2] * MM) for q in m.P]
            vp = gomu(struct.pack("<%df" % (3 * len(pts)), *[c for q in pts for c in q]), 34962)
            vn = gomu(struct.pack("<%df" % (3 * len(m.N)), *[c for q in m.N for c in q]), 34962)
            vi = gomu(struct.pack("<%dI" % len(m.I), *m.I), 34963)
            mn = [min(q[i] for q in pts) for i in range(3)]; mx = [max(q[i] for q in pts) for i in range(3)]
            accs.append({"bufferView": vp, "componentType": 5126, "count": len(pts), "type": "VEC3", "min": mn, "max": mx})
            accs.append({"bufferView": vn, "componentType": 5126, "count": len(m.N), "type": "VEC3"})
            accs.append({"bufferView": vi, "componentType": 5125, "count": len(m.I), "type": "SCALAR"})
            prims.append({"attributes": {"POSITION": len(accs) - 3, "NORMAL": len(accs) - 2}, "indices": len(accs) - 1, "material": mat(k)})
            ucgen += len(m.I) // 3
        meshes.append({"name": g, "primitives": prims})
        nodes[idx[g]]["mesh"] = len(meshes) - 1
    # animasyon örnekleri
    N = int(round(DONGU / adim)) + 1
    TT = [min(DONGU, i * adim) for i in range(N)]
    sm, ch = [], []
    def kanal(dugum, yol_, degerler, tip):
        ti = gomu(struct.pack("<%df" % len(TT), *TT))
        accs.append({"bufferView": ti, "componentType": 5126, "count": len(TT), "type": "SCALAR", "min": [0.0], "max": [DONGU]})
        n = 4 if tip == "VEC4" else 3
        vo = gomu(struct.pack("<%df" % (n * len(degerler)), *[c for v in degerler for c in v]))
        accs.append({"bufferView": vo, "componentType": 5126, "count": len(degerler), "type": tip})
        sm.append({"input": len(accs) - 2, "output": len(accs) - 1, "interpolation": "LINEAR"})
        ch.append({"sampler": len(sm) - 1, "target": {"node": idx[dugum], "path": yol_}})
    def trs_kanal(g, f):
        P = nodes[idx[g]]["translation"]
        kanal(g, "translation", [(P[0] + f(t)[0] * MM, P[1] + f(t)[1] * MM, P[2] + f(t)[2] * MM) for t in TT], "VEC3")
    trs_kanal("ITICI", lambda t: (0.0, 0.0, itici_dz(t)))
    trs_kanal("PISTON", lambda t: (0.0, kafa(t) - H_UST, 0.0))
    trs_kanal("KOPRU", lambda t: (0.0, kopru_dy(t), 0.0))
    trs_kanal("KATLAYICI", lambda t: (0.0, katlayici_dy(t), 0.0))
    trs_kanal("CATAL", catal_trs)
    trs_kanal("PIZZA", pizza_trs)
    trs_kanal("K_ITICI", k_itici_trs)
    kanal("KOL", "rotation", [quat("z", kol_beta(t)) for t in TT], "VEC4")
    kanal("PARMAK", "rotation", [quat("z", parmak_psi(t)) for t in TT], "VEC4")
    trs_kanal("B_ROOT", lambda t: blank_acilar(t)[0])
    for d in DUGUM:
        if DUGUM[d][0]:
            kanal(d, "rotation", [quat(DUGUM[d][2], blank_acilar(t)[1][d]) for t in TT], "VEC4")
    for g in ("B_ROOT", "PIZZA"):
        kanal(g, "scale", [(max(1e-4, gorunur(t)),) * 3 for t in TT], "VEC3")
    while off[0] % 4: blob.append(b"\x00"); off[0] += 1
    bb = b"".join(blob)
    gl = {"asset": {"version": "2.0", "generator": "AUTOKITCH kutu_cad_v1"}, "scene": 0, "scenes": [{"nodes": kok}], "nodes": nodes, "meshes": meshes,
          "materials": mats, "accessors": accs, "bufferViews": views, "buffers": [{"byteLength": len(bb)}],
          "animations": [{"name": "kutu_katlama_dongusu", "samplers": sm, "channels": ch}]}
    js = json.dumps(gl, separators=(",", ":")).encode("utf-8")
    while len(js) % 4: js += b" "
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, "wb") as f:
        f.write(struct.pack("<4sII", b"glTF", 2, 12 + 8 + len(js) + 8 + len(bb))); f.write(struct.pack("<I4s", len(js), b"JSON")); f.write(js)
        f.write(struct.pack("<I4s", len(bb), b"BIN\x00")); f.write(bb)
    print("GLB: %s · %d KB · %d dugum · %d ucgen · %d anim kanali · %d kare" % (os.path.basename(yol), (len(bb) + len(js)) // 1024, len(nodes), ucgen, len(ch), N))


# ---------------------------------------------------------------- BOM ----------------------------------------------------------------
def _tur(ad):
    return "SATIN ALMA" if any(s in ad for s in ("HIWIN", "AutomationDirect", "SureGear", "Siemens", "Mean Well", "Omron", "Elesa", "TBI", "Bilyalı", "Trapez", "GT3", "Kaplin",
                                                  "Destek B", "KFL", "LM12", "Alüminyum profil", "DIN ray", "Klemens", "Kablo kanalı", "UHMW", "Pizza kutusu", "FR5")) else "ÜRETİM"


def bom_yaz(klasor):
    os.makedirs(klasor, exist_ok=True)
    satir = []
    for p in PARCALAR:
        if p["grup"] in ("PIZZA", "K_ITICI", "SABIT_REF") or p["grup"].startswith("B_"):
            continue
        if p["bom"]:
            ad, adet, tanim, not_ = p["bom"]
            if adet == 0 and not tanim:
                satir.append((p["ad"], ad, 0, "", "aynı kalemin eşi (adet ana satırda)", "ALT")); continue
            satir.append((p["ad"], ad, adet, tanim, not_, _tur(ad)))
        else:
            bb = p["wp"].val().BoundingBox()
            tanim = {"sac": "304 sac · lazer + büküm", "kabuk": "304 sac 1,5 · lazer + büküm (dış kabuk)", "aluminyum": "alüminyum 6082 · CNC", "celik": "304 / S235 · lazer / torna", "uhmw": "UHMW-PE", "plastik": "",
                     "motor": "", "kart": "", "karton_yigin": ""}.get(p["mal"], p["mal"])
            satir.append((p["ad"], p["ad"].replace("_", " "), 1, tanim, "zarf %.1f × %.1f × %.1f" % (bb.xlen, bb.ylen, bb.zlen), "ÜRETİM"))
    with io.open(os.path.join(klasor, "BOM.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["parça (model adı)", "kalem", "adet", "tanım / ürün", "not / ölçü", "tür"])
        for r in satir:
            w.writerow(r)
    top, bil = {}, {}
    for pad, ad, adet, tanim, not_, tur in satir:
        if tur == "ALT":
            continue
        key = ad if tur == "SATIN ALMA" else ad
        if tur == "SATIN ALMA":
            top[key] = max(top.get(key, 0), int(adet)) if isinstance(adet, int) else 1
        else:
            top[key] = top.get(key, 0) + (int(adet) if isinstance(adet, int) else 1)
        bil.setdefault(key, (tanim, not_, tur))
    with io.open(os.path.join(klasor, "BOM_OZET.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["tür", "kalem", "toplam adet", "tanım / ürün", "not / kaynak"])
        for k in sorted(top, key=lambda a: (0 if bil[a][2] == "SATIN ALMA" else 1, a)):
            w.writerow([bil[k][2], k, top[k], bil[k][0], bil[k][1]])
    sa = sum(1 for k in top if bil[k][2] == "SATIN ALMA")
    print("BOM: %d parca satiri · %d kalem (%d satin alma · %d uretim)" % (len(satir), len(top), sa, len(top) - sa))


# ---------------------------------------------------------------- MODÜL ----------------------------------------------------------------
def modul():
    PARCALAR[:] = []
    govde(); sarjor(); besleyici(); kalip(); kopru(); piston(); parmak(); kapak_mekanizmasi(); elektrik(); blank(); catal_pizza()
    return PARCALAR


if __name__ == "__main__":
    t0 = time.time()
    arg = sys.argv[1:]
    modul()
    print("E KUTU MODULU v1: %d parca · %.0f sn" % (len(PARCALAR), time.time() - t0)); sys.stdout.flush()
    olcum(); sys.stdout.flush()
    if "hizli" not in arg:
        b1 = cakisma(); sys.stdout.flush()
        b2 = kutu_cakisma(); sys.stdout.flush()
        b4 = pizza_cakisma(); sys.stdout.flush()
        if "gecis" in arg:
            b3 = kutu_cakisma(anlar=GECIS_ANLARI, etiket="gecis"); sys.stdout.flush()
    if "glb" in arg or "hepsi" in arg:
        glb_yaz(os.path.join(KOK, "otonom", "hat3d", "kutu_modulu_v1.glb")); sys.stdout.flush()
    if "bom" in arg or "hepsi" in arg:
        bom_yaz(os.path.join(KOK, "arastirma", "5_PACK_v1"))
    print("toplam %.0f sn" % (time.time() - t0))
    sys.stdout.flush()
    os._exit(0)
