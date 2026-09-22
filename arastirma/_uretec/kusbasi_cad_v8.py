# -*- coding: utf-8 -*-
"""KAPAK YOK (Kemal, 22 Eyl: "kapak olmasın, TOPPING'de de yok") → gövde ağzında İÇE 8 mm bükme dudak · ROTOR KAYNAKLI (lama-kol kaynak yakaları) · ön kovanda SAVURMA DİSKİ. Üreteç: yap_kapaksiz_v1.py · önceki sürüm: kusbasi_cad_v3.py
BİRLEŞİM DETAYLARI v1 (22 Eyl 2026) uygulandı — bkz. kaset_birlesim_v1.py: dişli saplama + pul + kör somun · kaynaklı kulp (saplama kulpa vidalanır) ·
KLİKLİ bayonet (tırnak + tümsek + cep + O-ring yayı) · gövde contası · muylu O-ringleri · tüp O-ringi + M4 insert. Önceki sürüm: kusbasi_cad_v2.py
AUTOKITCH · KUŞBAŞI KASETİ v2 — ÜRETİM MODELİ (22 Eyl 2026) · ORTAK GÖVDE · kiyma_cad_v3'ten türetildi (yap_kusbasi_v8.py)
v2: gövde + iki uç plakası + kapak + kulp + saplamalar KIYMA v3 ile BİREBİR AYNI (kâse merkezi 177 → 164). Rotor KISA kollu: lama duvara 19, kanada 22 mm — küp hiçbir yerde sıkışmaz.
HESAP: kusbasi_akis_model_v1.py — tasarımı TEK sayı yönetiyor: KÜP KENARI d (VARSAYIM 10 mm; 12'ye kadar çalışır, 15'te çalışmaz).
ÜRÜN: pidelik kuşbaşı, ıslak yumuşak iri tane · 145 g / pide · 20 pide / gün → 2 gün 5,8 kg · dökme 0,80 g/mL (VARSAYIM; 1 cup = 170–198 g)
KURALLAR → ÖLÇÜLER
  · köprü: düşey açıklık ≥ 4 d (BulkInside)        → boğaz = tekne Ø72 (d 10'da 7,2 d) · ağız 48 × 44
  · topak: mil–tekne radyal boşluk ≥ R·d (CEMA)     → 28 mm = 2,8 d (sınıf 2+) · konik kökte 22 = 2,2 d
  · kanatlar arası net boşluk ≥ 3 d                 → hatve 40 → 50,3 (kanat 4 mm) · ÇİFT AĞIZ OLMAZ (boşluk yarıya iner)
  · iki hareketli yüzey arası: ya < d/3 ya > 1,5 d  → lama–duvar 2,4 (küp giremez) · rotor–kanat 18 (küp sıkışmaz)
KIYMA KASETİNDEN FARKLAR: helezon Ø68 / mil Ø16 / kök Ø28 · kanat 4 mm · tüp iç Ø72 · kanat ağızdan 18 mm ÖNCE biter: yatak TIKAÇ olarak
  6 mm'lik EŞİĞİN üstünden itilir → küpler tek tek düşer (tur başına öbek yok) ve eşiğin arkasında ≈ 50 mL et suyu tutulur, ağızdan damlamaz.
  Besleme rotoru, göbekler, kavramalar, kovan, topuz, pimler, miller, saplamalar KIYMA ve KAŞAR ile ORTAK.
UYARI: baskı parça yalnız DENEME içindir; çiğ et teması = 304/316 + POM-C talaşlı.
ÇIKTI: otonom/kaset3d/kusbasi_v8.glb/.usdz + kusbasi_v8_dozaj.glb · arastirma/3_TOPPING/kusbasi_kaseti_v8/
SURUM: kare agiz YUVARLAK BORU oldu (ic D 52, kopruleme kurali D >= 3 x en buyuk parca) ve
kaset tabaninin 100 mm altina uzatildi — urun pidenin 40 mm ustunden dokuluyor, arada baska parca yok.
Kaset artik masaya oturmuyor (boru asagida): yatay konur ya da ayakli sehpaya oturur.
BIRLESIM: boru artik tupun disinda TUP CAPIYLA basliyor, 22 mm konik daralip kendi capina
iniyor (ic D 52) ve duz devam ediyor — basamak yok. Onceki surumde boru tupe basamakla oturuyordu.
BORU BOYU: alt uc artik YALITIMIN UST YUZUNDE bitiyor (kaset yerel y -10; modulde 250).
Onceki surumde 90 mm daha asagi sarkiyordu. Urunu yalitim deligindeki paslanmaz kovan indiriyor.
BORU UCU y 250 DEGIL 252: ic kabuk tabani y 250-251. 250'de kesilince boru saci 1 mm deliyordu ve
ic kabukta YARIK birakmak gerekiyordu; 252'de bitince boru sacin 1 mm USTUNDE kaliyor, hem PU'da hem
ic kabukta YALNIZ YUVARLAK DELIK kaliyor ve kaset one cekilirken hicbir seye degmiyor.
"""
import csv, io, json, math, os, random, struct, sys, time
import cadquery as cq
import kaset_birlesim_v1 as BR                                      # saplama · kulp · bayonet · contalar: dört kasette AYNI kod
from OCP.gp import gp_Pnt
from OCP.TColgp import TColgp_Array1OfPnt
from OCP.TColStd import TColStd_Array1OfReal
from OCP.GeomAPI import GeomAPI_PointsToBSpline
from OCP.GeomAbs import GeomAbs_Shape
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeFace, BRepBuilderAPI_Sewing
from OCP.BRepFill import BRepFill
from OCP.ShapeFix import ShapeFix_Solid
from OCP.TopoDS import TopoDS
from OCP.TopAbs import TopAbs_SHELL
from OCP.TopExp import TopExp_Explorer
import kaset_3d_v4 as v4
from kaset_3d_v3 import Mesh, MM, kutu, doku_ad, doku_montaj, etiket_yuzu, MALZEME, usdz_yaz, OUT
from kasar_akis_model_v2 import YASA, T_DOK, r_t
import kusbasi_akis_model_v2 as AM                                     # ürünün kendi akış modeli: tabla yasası + hesap sayıları buradan
R0 = AM.r_t_k(0.0)                                                   # doz başında ağzın pide merkezine uzaklığı
RHO = 0.80                                                           # kıymalı harç g/mL · VARSAYIM (çiğ kıyma USDA ≈ 0,95; tartılacak)
KG2 = 5.8                                                            # 2 günlük (pafta HAT v19)
MALZEME.setdefault('kusbasi', dict(renk=(0.55, 0.17, 0.16, 1.0), met=0.0, ruf=0.85))
MALZEME.setdefault('kusbasi_dolgu', dict(renk=(0.55, 0.17, 0.16, 1.0), met=0.0, ruf=0.85))

KOK = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
URETIM = os.path.join(KOK, "arastirma", "3_TOPPING", "kusbasi_kaseti_v8")

# ---------------- ANA ÖLÇÜLER (mm) · x: en · y: yukarı · z: helezon ekseni (+z = ÖN) ----------------
W, D, H = 140.0, 325.0, 360.0
TP, ET, OYUK = 8.0, 3.0, 4.0
ZF, ZB = D / 2, -D / 2; ZFI, ZBI = ZF - TP, ZB + TP                 # plaka dış / iç yüzleri
CY, RT, YC, RB, RF, Y_UST, Y_DOLUM = 60.0, 36.0, 164.0, 67.0, 8.0, 352.0, 332.0      # v3 ORTAK GÖVDE (kıyma = kuşbaşı = küp sucuk): tekne Ø72 · kâse merkezi 164
R_MIL, R_KANAT, KARE = 8.0, 34.0, 8.0                                # helezon mili Ø16 · kanat Ø40 · kare çekirdek 8 × 8
KOK_Z0, KOK_Z1, R_KOK = -91.0, -151.0, 14.0                          # v7: ARKADA 60 mm KONİK MİL KÖKÜ Ø16 → Ø26 (v5'te vardı, v6'da düşmüştü)
MUYLU, MUYLU_D = 22.0, 22.4                                          # göbek muylusu / plaka deliği
KAN_Z0, KAN_Z1, HATVE0, TUR = -148.0, 156.0, 40.0, 6.75             # kanat z aralığı · baştaki hatve · toplam tur (ÇEYREK turun katı olmalı:
#   47 çeyrek tur. Böylece hatve sonu ≈30 çıkıyor, yani v7'deki son hatve — dozaj sayıları (7,9 g/tur, 42/35 dev/dk) değişmiyor.)
UC_HATVE, UC_Z0, UC_Z1 = None, 156.0, 170.0      # tüp içi: ana hatvenin sonu sabit sürer, ağzın sonuna kadar                          # tüp içi çift ağızlı bölüm
AG_Z0, AG_Z1, AG_X = 188.0, 232.0, 24.0
ESIK_Y, ESIK_Z0 = 6.0, 182.0                                        # eşik: 6 mm yüksek, ağzın hemen arkasında 6 mm boy
Y_AGIZ = 6.0                                                         # meme dudağı kotu (ayak düzlemi 0 — tapayla birlikte masada durabilsin)                              # alt ağız 36 × 38
TUP_Z1 = 246.5
BORU_D, BORU_ET, BORU_ALT, BORU_GECIS = 52.0, 3.0, -8.0, 22.0      # yuvarlak çıkış borusu: iç çap · et · alt uç · tüpten boruya konik geçiş boyu
R_CUBUK = 124.0                                                      # karıştırıcı dış çubuk yarıçapı
SAPLAMA = [(-52.0, 20.0), (52.0, 20.0), (-48.0, 340.0), (48.0, 340.0)]
for k_, v_ in dict(CY=CY, RT_I=RT, RT_O=RT + ET, YC=YC, D_=D, ZF=ZF, ZB=ZB, HW_I=RB, HW_O=RB + ET, Y_UST=Y_UST, Y_DOLUM=Y_DOLUM, TP=TP).items(): setattr(v4, k_, v_)


# ---------------- YARDIMCILAR ----------------
def kesit(o, y_top):
    """kadeh kesit (kapalı tel) · o = iç yüzeyden dışa ofset"""
    hw, rt, Rb, rf = RB + o, RT + o, RB + o, RF - o
    Fx = RT + RF; Fy = YC - math.sqrt((RB + RF) ** 2 - Fx ** 2)
    aT = math.atan2(YC - Fy, Fx); P = lambda a, s=1: (s * Rb * math.cos(a), YC - Rb * math.sin(a))
    ux, uy = -Fx, YC - Fy; L = math.hypot(ux, uy); ux, uy = ux / L, uy / L
    bx, by = ux - 1.0, uy; Lb = math.hypot(bx, by); bx, by = bx / Lb, by / Lb
    T1, M1, MF, T2 = P(aT), P(aT / 2), (Fx + rf * bx, Fy + rf * by), (rt, Fy)
    return (cq.Workplane("XY").moveTo(hw, y_top).lineTo(hw, YC).threePointArc(M1, T1).threePointArc(MF, T2).lineTo(rt, CY)
            .threePointArc((0, CY - rt), (-rt, CY)).lineTo(-rt, Fy).threePointArc((-MF[0], MF[1]), (-T1[0], T1[1]))
            .threePointArc((-M1[0], M1[1]), (-hw, YC)).lineTo(-hw, y_top).close())


def silz(x, y, r, z0, z1): return cq.Workplane("XY").center(x, y).circle(r).extrude(z1 - z0).translate((0, 0, z0))
def silx(y, z, r, x0, x1): return cq.Workplane("YZ").center(y, z).circle(r).extrude(x1 - x0).translate((x0, 0, 0))
def sily(x, z, r, y0, y1): return cq.Workplane("XZ").center(x, z).circle(r).extrude(-(y1 - y0)).translate((0, y0, 0))
def koni_y(z, r_alt, r_ust, y0, y1):
    """y ekseninde konik: y0 (alt, r_alt) → y1 (üst, r_ust). Tüpten boruya geçişi basamaksız yapar."""
    if abs(r_alt - r_ust) < 0.01: return sily(0, z, r_alt, y0, y1)   # esit yaricap: makeCone hata verir, silindir yeter
    return cq.Workplane(obj=cq.Solid.makeCone(r_alt, r_ust, y1 - y0, cq.Vector(0, y0, z), cq.Vector(0, 1, 0)))


def kut(x0, x1, y0, y1, z0, z1): return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))
def karez(x, y, a, z0, z1): return cq.Workplane("XY").center(x, y).rect(a, a).extrude(z1 - z0).translate((0, 0, z0))
def altigen(x, y, d, z0, z1): return cq.Workplane("XY").center(x, y).polygon(6, d).extrude(z1 - z0).translate((0, 0, z0))


def _hatve_sonu():
    """hatve sonunu öyle seç ki toplam dönüş TAM TUR olsun · θ(z) = 2πL/(p1−p0)·ln(p1/p0)"""
    L, hedef = KAN_Z1 - KAN_Z0, 2 * math.pi * TUR
    f = lambda p1: 2 * math.pi * L / (p1 - HATVE0) * math.log(p1 / HATVE0) - hedef
    a, b = HATVE0 + 0.5, 60.0
    for _ in range(90):
        m = (a + b) / 2
        if f(a) * f(m) <= 0: b = m
        else: a = m
    return (a + b) / 2


HATVE1 = _hatve_sonu(); K_H = (HATVE1 - HATVE0) / (KAN_Z1 - KAN_Z0); UC_HATVE = HATVE1
hatve = lambda z: HATVE0 + K_H * (z - KAN_Z0)                            # DOĞRUSAL artan hatve
teta_z = lambda z: 2 * math.pi / K_H * math.log(hatve(z) / HATVE0)        # analitik integrali
mil_r = lambda z: (R_KOK - (R_KOK - R_MIL) * (z - KOK_Z1) / (KOK_Z0 - KOK_Z1)) if z <= KOK_Z0 else R_MIL
def bolme_z(m):
    """θ = m·90° olan z (kare çubuğa oturması için bölme yerleri burada olmalı)"""
    return KAN_Z0 + (HATVE0 * math.exp(m * K_H / 4.0) - HATVE0) / K_H


def _egri(zs, r_f, dz):
    """noktalardan geçen BSpline kenar · açı ve yarıçap İSTASYON z'sinde, nokta z+dz'ye konur
    (kalınlık EKSENEL ölçülür: üst ve alt yüz aynı helikoit, yalnız z'de 3 mm kaydırılmış.
     dz'yi açıya da katarsan bıçak burulur ve arkada hatve 22'de kendi kendini keser — katı bozuluyordu.)
    parametre = istasyon z · dört eğri AYNI parametrelensin ki ruled yüzey eşleşsin"""
    arr = TColgp_Array1OfPnt(1, len(zs)); par = TColStd_Array1OfReal(1, len(zs))
    for i, z in enumerate(zs):
        t = teta_z(z); r = r_f(z)
        arr.SetValue(i + 1, gp_Pnt(r * math.cos(t), CY + r * math.sin(t), z + dz)); par.SetValue(i + 1, z)
    return BRepBuilderAPI_MakeEdge(GeomAPI_PointsToBSpline(arr, par, 3, 8, GeomAbs_Shape.GeomAbs_C2, 1e-4).Curve()).Edge()


def kaynat_kanat(g, f, ad):
    """TUZAK: mil bir DÖNÜŞ katısı; dikiş çizgisi kanadın yüzeyine/uç kapağına denk gelirse OpenCascade birleşmeyi
    sessizce HACMİ 0 olan 'geçerli' bir katı olarak döndürüyor (fuzzy değer de kurtarmıyor). Mil dönel olduğu için
    onu kendi ekseninde çevirmek geometriyi DEĞİŞTİRMEZ, yalnız dikişi kaydırır. Tutan açıyı arıyoruz; her deneme
    kaynat() ile HACİMLE doğrulanıyor, yani 'tuttu' demek gerçekten birleşti demek."""
    for sap in (0.0, 37.0, 73.0, 113.0, 151.0, 197.0, 233.0, 271.0, 307.0, 17.0, 53.0, 91.0, 127.0, 163.0):
        gg = g if sap == 0.0 else cq.Workplane(obj=g.val().rotate(cq.Vector(0, CY, 0), cq.Vector(0, CY, 1), sap))
        try: return kaynat(gg, f, ad)
        except RuntimeError: continue
    raise RuntimeError("kanat hicbir dikis acisinda kaynamadi: " + ad)


def kanat_surekli(z_bas, z_son, r_dis=R_KANAT, kal=4.0, adim=0.25):
    """SÜREKLİ değişen hatveli kanat · süpürme YOK: 4 kenar eğrisi + aralarında BRepFill ruled yüzeyler → dikiş → katı"""
    k = kal / 2.0; n = max(40, int((z_son - z_bas) / adim))
    zs = [z_bas + (z_son - z_bas) * i / n for i in range(n + 1)]
    ric = lambda z: mil_r(z) - 0.8
    e = {ad: _egri(zs, rf, dz) for ad, rf, dz in
         (("it", ric, k), ("ib", ric, -k), ("ot", lambda z: r_dis, k), ("ob", lambda z: r_dis, -k))}
    dik = BRepBuilderAPI_Sewing(1e-4)
    for a, b in (("it", "ot"), ("ib", "ob"), ("ot", "ob"), ("it", "ib")): dik.Add(BRepFill.Face_s(e[a], e[b]))
    for z in (z_bas, z_son):
        t = teta_z(z); ri = ric(z)
        poly = BRepBuilderAPI_MakePolygon()
        for r, dz in ((ri, -k), (r_dis, -k), (r_dis, k), (ri, k)): poly.Add(gp_Pnt(r * math.cos(t), CY + r * math.sin(t), z + dz))
        poly.Close(); dik.Add(BRepBuilderAPI_MakeFace(poly.Wire()).Face())
    dik.Perform(); ex = TopExp_Explorer(dik.SewedShape(), TopAbs_SHELL); kab = []
    while ex.More(): kab.append(TopoDS.Shell_s(ex.Current())); ex.Next()
    assert len(kab) == 1, "kanat dikisi tek kabuk vermedi: %d" % len(kab)
    w = cq.Workplane(obj=cq.Shape.cast(ShapeFix_Solid().SolidFromShell(kab[0])))
    assert w.val().isValid() and w.val().Volume() > 1000, "kanat katisi bozuk"
    return w


def kanat_sabit(pitch, z_bas, z_son, faz_deg, r_ic=R_MIL - 0.8, r_dis=R_KANAT, kal=4.0):
    """SABİT hatveli kanat (Frenet süpürme — OpenCascade'de güvenilir olan tek yol; değişken hatveli süpürmede kanat yarıçapı 20 → 13 mm çöküyordu)"""
    helix = cq.Wire.makeHelix(pitch, z_son - z_bas, r_ic + 0.01, center=cq.Vector(0, 0, 0), dir=cq.Vector(0, 0, 1))
    prof = cq.Workplane("XZ").polyline([(r_ic, -kal / 2 - 1.0), (r_dis, -kal / 2), (r_dis, kal / 2), (r_ic, kal / 2 + 1.0)]).close()
    sol = prof.sweep(cq.Workplane(obj=helix), isFrenet=True).val()
    return cq.Workplane(obj=sol.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), faz_deg).translate(cq.Vector(0, CY, z_bas)))


def kaynat(g, f, ad=""):
    """birleştir + HACİMLE DOĞRULA: OpenCascade bazen 'geçerli' ama parçası düşmüş katı döndürüyor; hacim artmıyorsa öbür ayarı dene"""
    v0, vf = g.val().Volume(), f.val().Volume()
    # eklenmesi GEREKEN hacim = parçanın gövdenin dışında kalan kısmı (kanat kökü mile/koniye gömülü olduğu için
    # "vf'nin %45'i" gibi sabit eşik yanlış alarm veriyordu — gömülü payı ölçüp çıkarıyoruz)
    try:
        ort = g.intersect(f, clean=False).val().Volume()
        hedef = 0.9 * (vf - ort) if 0.0 <= ort < vf else 0.45 * vf
    except Exception:
        hedef = 0.45 * vf
    for clean in (True, False):
        try: r = g.union(f, clean=clean)
        except Exception: continue
        if r.val().isValid() and r.val().Volume() > v0 + hedef: return r
    raise RuntimeError("kaynak basarisiz: " + ad)


PARCALAR = []            # (ad, workplane, malzeme_glb, grup, bom)
def ekle(ad, wp, mal, grup=None, bom=None): PARCALAR.append(dict(ad=ad, wp=wp, mal=mal, grup=grup, bom=bom))


def kap():
    # ---- 1 GÖVDE ----
    govde = kesit(ET, Y_UST).extrude(D - 2 * TP + 2 * OYUK).translate((0, 0, ZBI - OYUK)).cut(
        kesit(0.0, Y_UST + 1).extrude(D).translate((0, 0, ZB - 1)))
    ekle("govde", govde, "cam", bom=("Gövde · kadeh kesit", 1, "PC 3 mm ısıl form · ya da 304 sac 1 mm (kanal 1,4 olur) · ya da baskı", "iki plakanın 4 mm kanalına oturur"))

    # ---- 2 UÇ PLAKALARI ----
    def plaka(on):
        z0 = ZFI if on else ZB
        p = cq.Workplane("XY").center(0, Y_UST / 2).rect(W, Y_UST).extrude(TP).edges("|Z").edges(">Y").fillet(12.0).translate((0, 0, z0))
        p = p.cut(kut(-36, 36, -1, 6, z0 - 1, z0 + TP + 1))                                         # ayak boşluğu: iki ayak üstünde durur
        kanal = kesit(ET + 0.2, Y_UST + 2).extrude(OYUK).cut(kesit(-0.2, Y_UST + 3).extrude(OYUK))
        p = p.cut(kanal.translate((0, 0, ZFI if on else ZBI - OYUK)))                                  # kanal iç yüzden plakanın içine 4 mm
        for x, y in SAPLAMA: p = p.cut(silz(x, y, 3.25, z0 - 1, z0 + TP + 1))
        p = p.cut(silz(0, YC, MUYLU_D / 2, z0 - 1, z0 + TP + 1))                                       # karıştırıcı yatağı
        if on:
            p = p.cut(silz(0, CY, RT, z0 - 1, z0 + TP + 1)).cut(silz(0, CY, RT + 3.2, ZF - 3.0, ZF + 1))    # tüp geçişi Ø44 + fatura Ø50,4 × 3
            for s in (1, -1): p = p.cut(silz(s * (RT + 11.0), CY, 2.0, ZF - 6.5, ZF + 1))                      # M4 diş (matkap Ø3,3 · kılavuz M4 × 6,5)
        else:
            p = p.cut(silz(0, CY, MUYLU_D / 2, z0 - 1, z0 + TP + 1))                                   # helezon tahrik göbeği yatağı
            for s in (1, -1): p = p.cut(silz(s * 55.0, 70.0, 5.1, z0 - 1, z0 + TP + 1))                # makine konum pimi Ø10
        return p
    ekle("plaka_arka", plaka(False), "cam",
         bom=("Arka uç plakası", 1, "PC / POM / HDPE 8 mm · CNC freze", "kanal 3,4 × 4 · 2 yatak Ø22,4 · 4 saplama Ø6,5 · 2 konum pimi Ø10,2"))
    ekle("plaka_on", plaka(True), "cam",
         bom=("Ön uç plakası", 1, "PC / POM / HDPE 8 mm · CNC freze", "kanal · tüp geçişi Ø72 + fatura Ø78,4 × 3 · yatak Ø22,4 · 2 × M4"))

    # ---- 3 SAPLAMALAR + SOMUNLAR + KULP ----
    for i, (x, y) in enumerate(SAPLAMA):
        ust = y > 300
        ekle("saplama_%d" % i, silz(x, y, 3.0, ZB - 9, ZF + (14 if ust else 9)), "celik",
             bom=(("Saplama M6 × 348 (üst · kulpa girer)", 2) if ust else ("Saplama M6 × 343 (alt)", 2)) + ("A2 paslanmaz · gijon", "plakaları gövdeye sıkar; üsttekiler dolum çizgisinin üstünde") if i in (0, 2) else None)
        ekle("somun_arka_%d" % i, altigen(x, y, 11.5, ZB - 9, ZB - 0.2).cut(silz(x, y, 3.0, ZB - 10, ZB)), "celik",
             bom=("Kör somun M6 + pul", 6, "A2 paslanmaz · DIN 1587", "arka 4 + ön alt 2") if i == 0 else None)
        if not ust: ekle("somun_on_%d" % i, altigen(x, y, 11.5, ZF + 0.2, ZF + 9).cut(silz(x, y, 3.0, ZF, ZF + 10)), "celik")
    kulp = silz(-48, 340, 6.0, ZF + 0.2, ZF + 48).union(silz(48, 340, 6.0, ZF + 0.2, ZF + 48)).union(silx(340, ZF + 42, 5.0, -48, 48))
    kulp = kulp.cut(silz(-48, 340, 3.0, ZF, ZF + 15)).cut(silz(48, 340, 3.0, ZF, ZF + 15))
    ekle("kulp", kulp, "celik", bom=("Boru kulp 96 mm · M6 dişi", 1, "paslanmaz · standart", "üst iki saplamanın ön ucuna vidalanır · kabı yuvadan çekmek için"))

    # ---- 4 HELEZON: kare çekirdek + 4 segment (her segment = TEK sabit hatve) ----
    # Hatvenin değiştiği yerden bölünür → segment içinde kanat birleşimi yok (OpenCascade'in kanat düşürdüğü yer orasıydı).
    # Ek yerinde her iki segmentte 3 mm'lik Ø14 boyun: komşunun kanat kökü (r 7,2–8) mile değmesin. Kanat uçları ek yerinden 0,2 mm geride.
    G = "helezon"; BOYUN, GERI = 3.0, 0.2
    ZC1, ZC2 = bolme_z(9), bolme_z(18)      # bölme yerleri: θ = 19 ve 35 çeyrek tur → parçalar kare çubuğa doğru açıda oturur
    SEG = [("helezon_A", -151.0, ZC1, "hatve %.2f → %.2f · arkada 60 mm KONİK KÖK Ø28 → Ø16" % (hatve(KAN_Z0), hatve(ZC1))),
           ("helezon_B", ZC1, ZC2, "hatve %.2f → %.2f" % (hatve(ZC1), hatve(ZC2))),
           ("helezon_C", ZC2, UC_Z0, "hatve %.2f → %.2f" % (hatve(ZC2), hatve(KAN_Z1))),
           ("helezon_D", UC_Z0, 253.0, "tüp içinde kanat ağızdan 18 mm ÖNCE biter (yatak tıkaç olarak itilir) · ağız üstünde çıplak mil · ön muylu Ø12")]
    for k_, (ad, zA, zB, acik) in enumerate(SEG):
        ilk, son = k_ == 0, k_ == len(SEG) - 1
        zb0, zs0 = zA + (0 if ilk else BOYUN), (233.0 if son else zB - BOYUN)
        if ilk:   # v7: KONİK KÖK — arkadaki kanat boşluğunu daraltır, kapasite öne doğru artar → kaşar yalnız arkadan değil boyunca çekilir.
            prof = cq.Workplane("XZ").polyline([(0.0, zb0), (R_KOK, zb0), (R_MIL, KOK_Z0), (R_MIL, zs0), (0.0, zs0)]).close()   # tek revolve: boolean yok
            g = cq.Workplane(obj=prof.revolve(360, (0, 0, 0), (0, 1, 0)).val().translate(cq.Vector(0, CY, 0)))   # eksen YEREL koordinatta (XZ düzleminde +y = global z)
        else:
            g = silz(0, CY, R_MIL, zb0, zs0)
        if not ilk: g = kaynat(g, silz(0, CY, R_MIL - 1.0, zA, zA + BOYUN + 0.5), ad + " boyun")
        if not son: g = kaynat(g, silz(0, CY, R_MIL - 1.0, zB - BOYUN - 0.5, zB), ad + " boyun")
        if son:
            faz0 = math.degrees(teta_z(KAN_Z1)) % 360.0        # tüp içi çift ağız, ana kanadın bittiği açıdan devam etsin (kare çubukta 270°)
            g = kaynat_kanat(g, kanat_sabit(UC_HATVE, UC_Z0, UC_Z1, faz0), ad + " kanat")            # TEK ağız: yüzey az → daha az yapışma
        else:
            # TUZAK: dönüş yüzeyinin/silindirin DİKİŞ çizgisi kanadın uç kapağıyla aynı açıya gelirse birleşme sessizce
            # HACMİ 0 olan "geçerli" katı veriyor (fuzzy 1e-2 bile geçersiz çıkıyordu). Dikişi 37° kaydırınca düzeliyor.
            zk, zs = max(KAN_Z0, zA) + (0 if ilk else GERI), zB - GERI
            g = kaynat_kanat(g, kanat_surekli(zk, zs), ad + " kanat")
        if son:
            g = kaynat(g, silz(0, CY, 6.0, 233.0, 253.0), "muylu")                                     # ön muylu Ø12
        v0 = g.val().Volume(); delik = karez(0, CY, KARE + 0.3, zA - 2.0, min(zB + 2.0, 232.0)); tamam = None
        for clean in (True, False):
            r = g.cut(delik, clean=clean)
            if r.val().isValid() and 0.5 * v0 < r.val().Volume() < v0 - 1000: tamam = r; break
        assert tamam is not None, "kare delik acilamadi: " + ad
        ekle(ad, tamam, "pom", G, bom=("Helezon segmenti " + ad[-1], 1, "DENEME: PETG / PA12 baskı, kanat 4 mm · ÜRETİM: POM-C talaşlı (çiğ et teması)", acik + " · boy %.0f mm · kare delik 8,3" % (zB - zA)))
    ekle("helezon_cekirdek", karez(0, CY, KARE, -163.0, 231.5), "celik", G,
         bom=("Kare çubuk 8 × 8 × 394", 1, "AISI 304 · yalnız boya kesilir", "torku segmentlere taşır, mili sertleştirir"))

    # ---- 5 TAHRİK GÖBEĞİ + HAÇ KAVRAMA (helezon ve karıştırıcı için AYNI iki parça) ----
    def gobek(y):
        g = silz(0, y, 16.0, ZBI, ZBI + 3.0).union(silz(0, y, MUYLU / 2, ZB, ZBI)).union(karez(0, y, 14.0, ZB - 12.0, ZB))
        return g.cut(karez(0, y, KARE + 0.3, ZB - 1.0, ZBI + 3.1)).cut(silx(y, ZB - 6.0, 2.05, -12, 12))
    def kavrama(y):
        k = silz(0, y, 13.0, ZB - 18.5, ZB - 0.5).union(kut(-18, 18, y - 4, y + 4, ZB - 18.5, ZB - 8.5)).union(kut(-4, 4, y - 18, y + 18, ZB - 18.5, ZB - 8.5))
        return k.cut(karez(0, y, 14.3, ZB - 12.5, ZB)).cut(silx(y, ZB - 6.0, 2.05, -20, 20))
    for ad, y, grup in (("helezon", CY, G), ("karistirici", YC, "karistirici")):
        ekle("gobek_" + ad, gobek(y), "pom", grup, bom=("Tahrik göbeği", 2, "POM torna ya da baskı", "içeriden takılır: flanş Ø32 + muylu Ø22 + kare yuva 8,3 × 12") if ad == "helezon" else None)
        ekle("kavrama_" + ad, kavrama(y), "pom", grup, bom=("Haç kavrama", 2, "POM ya da baskı", "arkadan göbeğin kare başına geçer · makinedeki yaylı yuvaya oturur") if ad == "helezon" else None)
        ekle("yayli_pim_" + ad, silx(y, ZB - 6.0, 2.0, -13, 13), "celik", grup, bom=("Yaylı pim Ø4 × 26", 2, "A2 · ISO 8752", "kavramayı göbeğe kilitler") if ad == "helezon" else None)

    # ---- 6 ÇIKIŞ TÜPÜ + YATAK KAPAĞI ----
    RD = RT + 3.0                                                                                        # tüp dış yarıçapı
    tup = silz(0, CY, RD, ZF - 1.3, TUP_Z1)                # geçme 2,8 → 1,3: faturanın dibinde 1,7 mm O-ring yeri
    flans = silz(0, CY, RD + 6.0, ZF, ZF + 5.0).union(kut(-(RD + 16.0), RD + 16.0, CY - 9, CY + 9, ZF, ZF + 5.0))
    BZ = (AG_Z0 + AG_Z1) / 2.0                                                                            # borunun z ekseni = ağzın ortası
    RB_ = BORU_D / 2 + BORU_ET                                                                            # boru dış yarıçapı
    YG_ = CY - BORU_GECIS                                                                                 # konik geçişin alt kotu
    boru = koni_y(BZ, RB_, RT + 3.0, YG_, CY).union(sily(0, BZ, RB_, BORU_ALT, YG_))                      # tüp çapında başlar, konik daralır, düz iner
    bic_ = koni_y(BZ, BORU_D / 2, RT, YG_, CY + 1.0).union(sily(0, BZ, BORU_D / 2, BORU_ALT - 1.0, YG_))   # iç boşluk da konik
    tup = tup.union(flans).union(boru).cut(silz(0, CY, RT, ZF - 4, TUP_Z1 + 1)).cut(bic_)
    esik = silz(0, CY, RT + 0.5, ESIK_Z0, AG_Z0).intersect(kut(-RT - 1, RT + 1, CY - RT - 1, CY - RT + ESIK_Y, ESIK_Z0 - 1, AG_Z0 + 1))   # EŞİK: tüp tabanında hilal
    tup = tup.union(esik)
    for s in (1, -1): tup = tup.cut(silz(s * (RD + 8.0), CY, 2.25, ZF - 1, ZF + 6))
    tup = BR.tirnak_ekle(tup, RT + 3.0, CY)                                                            # 3 bayonet TIRNAĞI (tüple tek parça)
    ekle("cikis_tupu", tup, "cam", bom=("Çıkış tüpü + eşik", 1, "PC / PETG şeffaf · baskı ya da torna + freze", "iç Ø72 · ön plakaya faturalı + 2 × M4 · kapalı bölümde 6 mm EŞİK (et suyunu tutar, akışı sürekli yapar) · yuvarlak çıkış borusu iç Ø52 (tüpten 22 mm konik geçişle), yalıtımın üst yüzünde biter, ürünü yalıtımdaki kovan indirir · 3 bayonet TIRNAĞI 8 × 4 × 3,2 (tüple tek parça) · plakaya geçme 1,3 + O-ring"))
    for s in (1, -1): ekle("vida_tup_%s" % ("a" if s > 0 else "b"), silz(s * (RD + 8.0), CY, 3.5, ZF + 5.0, ZF + 7.8).union(silz(s * (RD + 8.0), CY, 1.95, ZF - 5.5, ZF + 5.0)), "celik",
                           bom=("Vida M4 × 12 silindir başlı", 2, "A2 · DIN 912", "tüp flanşını ön plakaya bağlar") if s > 0 else None)
    kp = BR.yatak_kapagi(RT, CY, TUP_Z1)                                                               # giriş → halka → tümsek → cep · O-ring kanalı
    ekle("yatak_kapagi", kp, "pom", bom=("Yatak kapağı (bayonet)", 1, "POM / PETG baskı", "İT → 35° ÇEVİR → KLİK (tümsek 0,25 + cep + dayama · içindeki O-ring hem conta hem yay) · ön muyluyu Ø12,4 yatakta taşır · sökünce helezon öne çekilir"))
    ekle("tasima_tapasi", sily(0, BZ, BORU_D / 2 + BORU_ET + 2.0, BORU_ALT - 8.0, BORU_ALT + 14.0)
         .cut(sily(0, BZ, BORU_D / 2 + BORU_ET + 0.2, BORU_ALT - 6.0, BORU_ALT + 16.0)), "silikon",
         bom=("Taşıma tapası", 1, "TPU 95A baskı", "kap makine dışındayken çıkış borusunun ucuna geçer · makineye sürmeden çıkarılır"))

    # ---- 7 BESLEME ROTORU: kıyma kendi akmaz → iki SIYIRICI LAMA duvarı sıyırır, eti helezon boğazına iter ----
    Kg = "karistirici"
    ekle("kar_mil", karez(0, YC, KARE, -163.0, 205.0), "celik", Kg, bom=("Kare çubuk 8 × 8 × 368", 1, "AISI 304", "rotor mili · öne çekilip çıkarılır"))
    R_LAMA, LAMA_G, LAMA_K, LAMA_ACI, R_KOL = 40.0, 15.0, 3.0, 20.0, 43.0          # lama merkezi r · genişlik · kalınlık · eğim · kol ucu
    def lama(g, k, z0, z1):                                                          # yerel: kol +x yönünde, lama kendi ekseninde LAMA_ACI eğik
        b = cq.Workplane("XY").center(R_LAMA, 0).rect(g, k).extrude(z1 - z0).translate((0, 0, z0))
        return cq.Workplane(obj=b.val().rotate(cq.Vector(R_LAMA, 0, 0), cq.Vector(R_LAMA, 0, 1), LAMA_ACI))
    def yerine(wp, a): return cq.Workplane(obj=wp.val().rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), a).translate(cq.Vector(0, YC, 0)))
    def orumcek(z0, z1):
        o = silz(0, YC, 14.0, z0, z1); zo = (z0 + z1) / 2
        for a in (0.0, 180.0):
            kol = kut(6.0, R_KOL, -7.0, 7.0, zo - 7, zo + 7).cut(lama(LAMA_G + 0.3, LAMA_K + 0.3, z0 - 1, z1 + 1))   # lama yuvası: ucu AÇIK çentik, lama koldan 4 mm taşar
            # KAYNAK YAKASI: lama ile kolun birleşimi, kolun iki yanında 3 mm. Lamanın kendi dış yarıçapıyla sınırlı → duvar boşluğu bozulmaz.
            ac_ = math.radians(LAMA_ACI); R_DIS_ = R_LAMA + LAMA_G / 2.0 * math.cos(ac_) + LAMA_K / 2.0 * math.sin(ac_)   # lamanın EN DIŞ köşesi: yaka bundan dışarı çıkmaz
            for za_, zb_ in ((z0 - 3.0, z0), (z1, z1 + 3.0)):
                yaka = lama(LAMA_G + 6.0, LAMA_K + 6.0, za_, zb_).cut(lama(LAMA_G + 0.3, LAMA_K + 0.3, za_ - 1, zb_ + 1)).intersect(
                    cq.Workplane("XY").circle(R_DIS_).extrude(zb_ - za_ + 2).translate((0, 0, za_ - 1)))
                kol = kol.union(yaka)
            o = o.union(yerine(kol, a))
        return o.cut(karez(0, YC, KARE + 0.3, z0 - 1, z1 + 1))
    for ad, z0, z1 in (("arka", -150.5, -133.0), ("orta", -7.0, 7.0), ("on", 133.0, 150.5)):
        ekle("orumcek_" + ad, (orumcek(z0, z1).union(silz(0, YC, 14.0, z1, 153.2).cut(karez(0, YC, KARE + 0.3, z1 - 1, 154.0))) if ad == "on" else orumcek(z0, z1)), "pom", Kg, bom=("Rotor göbeği · 2 kollu", 3, "DENEME: PETG / PA12 baskı (yakalarla tek parça çıkar) · ÜRETİM: 304, lamalarla KAYNAKLI", "2 KISA kol: lamaları r 40'ta 20° eğik tutar · her birleşimde 3 mm KAYNAK YAKASI · kare delik 8,3") if ad == "arka" else None)
    for i, a in enumerate((0.0, 180.0)):
        ekle("cubuk_%d" % i, yerine(lama(LAMA_G, LAMA_K, -146.0, 146.0), a), "celik", Kg, bom=("Sıyırıcı lama 15 × 3 × 292", 2, "AISI 304 lama · kenarları kırık", "kola KAYNAKLI (rotor tek parça: vida/pim yok, aralık yok, bakteri tutmaz) · duvarı sıyırıp eti boğaza iter") if i == 0 else None)
    kovan = silz(0, YC, 16.0, ZFI - 3.0, ZFI).union(silz(0, YC, MUYLU / 2, ZFI, ZF + 14.0)).cut(karez(0, YC, KARE + 0.3, ZFI - 4, ZF + 15)).cut(silx(YC + 7.5, ZF + 7.5, 2.1, -14, 14))
    kovan = kovan.cut(silz(0, YC, 14.2, ZFI - 3.0, ZFI - 1.0))                    # LABİRENT havşası Ø28,4 × 2 (ön örümcek göbeği girer)
    ekle("on_kovan", kovan, "pom", Kg, bom=("Ön kovan", 1, "POM / baskı", "arka yüzünde Ø28,4 × 2 LABİRENT havşası (ön örümcek göbeği girer → ürün mile sürünemez) · içeriden takılır · plakada döner · mil içinden kayar · teğet pim deliği · KAŞAR KABIYLA ORTAK"))
    topuz = silz(0, YC, 18.0, ZF + 1.0, ZF + 56.0).cut(silz(0, YC, MUYLU / 2 + 0.25, ZF, ZF + 14.5)).cut(karez(0, YC, KARE + 0.3, ZF + 14.0, ZF + 43.0)).cut(silx(YC + 7.5, ZF + 7.5, 2.1, -20, 20))
    topuz = topuz.cut(sily(0, ZF + 30.0, 2.0, YC + 3, YC + 20)).edges(">Z").chamfer(3.0)            # M4 diş (matkap Ø3,3)
    ekle("topuz", topuz, "pom", Kg, bom=("Topuz", 1, "POM / baskı", "kare mile M4 setuskurla sabit · eteği kovanın üstüne geçer"))
    ekle("setuskur", sily(0, ZF + 30.0, 1.95, YC + 4.2, YC + 10.2), "celik", Kg, bom=("Setuskur M4 × 6", 1, "A2 · DIN 913", "topuzu mile sabitler"))
    pim = silx(YC + 7.5, ZF + 7.5, 2.0, -24, 20).union(cq.Workplane("XY").circle(9.0).circle(7.2).extrude(1.8).translate((-32.0, YC + 7.5, ZF + 6.6)))
    ekle("kilit_pimi", pim, "celik", Kg, bom=("Halkalı kilit pimi Ø4 × 44", 1, "A2 · standart", "topuz eteği + kovandan TEĞET geçer (mili delmeden) · çekince mil öne çıkar"))

    # ---- 8 AĞIZ DUDAĞI (KAPAK YOK — Kemal, 22 Eyl) ----
    # Gövdenin üst ağzı boyunca İÇE 8 mm bükme dudak (gövdeyle AYNI parça). Dışa bükülemez: kaset dış ölçüsü dolu.
    AD_ = {p["ad"]: p for p in PARCALAR}
    for s_ in (1, -1):
        dudak = kut(min(s_ * (RB - 8.0), s_ * RB), max(s_ * (RB - 8.0), s_ * RB), Y_UST - 1.5, Y_UST, ZBI, ZFI)
        v0_ = AD_["govde"]["wp"].val().Volume(); AD_["govde"]["wp"] = AD_["govde"]["wp"].union(dudak)
        assert AD_["govde"]["wp"].val().isValid() and AD_["govde"]["wp"].val().Volume() > v0_ + 3000.0, "agiz dudagi birlesmedi"
    AD_["govde"]["bom"] = ("Gövde · kadeh kesit + ağız dudağı", 1, AD_["govde"]["bom"][2], "iki plakanın 4 mm kanalına oturur · üst ağız boyunca İÇE 8 mm bükme dudak (KAPAK YOK: kenar keskin kalmaz, ağız esnemez)")
    BR.uygula(globals())                                                                                 # birleşim detayları: dört kasette aynı


def makine():
    """YALNIZ YERLEŞİM. 140'lık kasette redüktörler DİKEY dizilir: NMRV030 90° çevrili (97 × 81 × 63), üstteki motor YUKARI,
    alttaki AŞAĞI bakar — yana bakarsa (kaşar kabındaki gibi) komşu kasetin arkasına taşar."""
    zc = (AG_Z0 + AG_Z1) / 2; y_pide = -40.0; y_tabla = y_pide - 8.0                 # macun ipi kısa düşmeli: meme → pide ≈ 48 mm (tepsiyi robot getirir)
    ekle("M_arka_duvar", kut(-70, 70, -20, 360, ZB - 97, ZB - 95), "cam")
    for ad, y, yon in (("helezon", CY, -1), ("karistirici", YC, 1)):
        z1 = ZB - 32.0; z0 = z1 - 63.0
        motor = kut(-yon * 1.5 - 57 * (yon < 0), -yon * 1.5 + 57 * (yon > 0), min(y + yon * 40.5, y + yon * 130.5), max(y + yon * 40.5, y + yon * 130.5), z0 + 3, z1 - 3)
        ekle("M_red_" + ad, kut(-48.5, 48.5, y - 40.5, y + 40.5, z0, z1).union(motor), "koyu")
        yuva = silz(0, y, 21.0, ZB - 30.0, ZB - 9.5).cut(kut(-18.5, 18.5, y - 4.4, y + 4.4, ZB - 20, ZB - 8)).cut(kut(-4.4, 4.4, y - 18.5, y + 18.5, ZB - 20, ZB - 8)).cut(silz(0, y, 13.4, ZB - 20, ZB - 8))
        ekle("M_yuva_" + ad, yuva, "celik", "helezon" if ad == "helezon" else "karistirici")
    for s in (1, -1):
        ekle("M_konum_pimi_%s" % ("a" if s > 0 else "b"), silz(s * 55.0, 70.0, 5.0, ZB - 95, ZB + 6.0), "celik")
        ekle("M_ray_%s" % ("a" if s > 0 else "b"), kut(min(s * 40, s * 70), max(s * 40, s * 70), -6.0, 0.0, ZB - 40, ZF + 120), "koyu")
    xt = -R0
    ekle("M_tabla", sily(xt, zc, 170.0, y_tabla - 12, y_tabla), "celik", "tabla"); ekle("M_pide", sily(xt, zc, 140.0, y_tabla, y_pide), "hamur", "tabla")
    ekle("M_kolon", sily(xt, zc, 20.0, y_tabla - 70, y_tabla - 12), "koyu", "kolon")
    return zc, y_pide, xt


def ag(wp, tol=0.12, aci=0.35):
    sh = wp.val() if hasattr(wp, "val") else wp
    vs, ts = sh.tessellate(tol, aci); m = Mesh(); P = [(v.x, v.y, v.z) for v in vs]; N = [[0.0, 0.0, 0.0] for _ in P]
    for a, b, c in ts:
        ux, uy, uz = P[b][0] - P[a][0], P[b][1] - P[a][1], P[b][2] - P[a][2]; wx, wy, wz = P[c][0] - P[a][0], P[c][1] - P[a][1], P[c][2] - P[a][2]
        n = (uy * wz - uz * wy, uz * wx - ux * wz, ux * wy - uy * wx)
        for i in (a, b, c): N[i][0] += n[0]; N[i][1] += n[1]; N[i][2] += n[2]
    for p, n in zip(P, N):
        L = math.sqrt(n[0] ** 2 + n[1] ** 2 + n[2] ** 2) or 1.0; m.P.append((p[0] * MM, p[1] * MM, p[2] * MM)); m.N.append((n[0] / L, n[1] / L, n[2] / L))
    for a, b, c in ts: m.I += [a, b, c]
    return m


# ---------------- GLB (gruplar + dönme + kayma) ----------------
DONGU, DT = 12.0, 0.1
_kay = lambda t: ((R0 - AM.r_t_k(t)) * MM if t <= T_DOK else (R0 - AM.r_t_k(T_DOK)) * MM * (DONGU - t) / (DONGU - T_DOK), 0.0, 0.0)
GRUP = {"helezon": dict(pivot=(0, CY * MM, 0), eksen="z", aci=lambda t: -2.1 * min(t, T_DOK) / T_DOK),
        "karistirici": dict(pivot=(0, YC * MM, 0), eksen="z", aci=lambda t: 0.67 * min(t, T_DOK) / T_DOK),
        "tabla": dict(pivot=(-R0 * MM, -0.187, 0.210), eksen="y", aci=lambda t: AM.tabla_tur(t), kay=_kay),
        "kolon": dict(pivot=(0, 0, 0), eksen="y", aci=lambda t: 0.0, kay=_kay)}


def glb_yaz(yol, parcalar, dokular):
    adlar = list(MALZEME.keys()); blob, views, accs, meshes, nodes = [], [], [], [], []; off = [0]
    def gomu(b, hedef=None):
        while off[0] % 4: blob.append(b"\x00"); off[0] += 1
        v = {"buffer": 0, "byteOffset": off[0], "byteLength": len(b)}
        if hedef: v["target"] = hedef
        views.append(v); blob.append(b); off[0] += len(b); return len(views) - 1
    cocuk, kok = {}, []
    for adi, m, mal, grup in parcalar:
        vp = gomu(struct.pack("<%df" % (3 * len(m.P)), *[c for p in m.P for c in p]), 34962); vn = gomu(struct.pack("<%df" % (3 * len(m.N)), *[c for n in m.N for c in n]), 34962)
        vi = gomu(struct.pack("<%dI" % len(m.I), *m.I), 34963)
        mn = [min(p[k] for p in m.P) for k in range(3)]; mx = [max(p[k] for p in m.P) for k in range(3)]
        accs.append({"bufferView": vp, "componentType": 5126, "count": len(m.P), "type": "VEC3", "min": mn, "max": mx})
        accs.append({"bufferView": vn, "componentType": 5126, "count": len(m.N), "type": "VEC3"}); accs.append({"bufferView": vi, "componentType": 5125, "count": len(m.I), "type": "SCALAR"})
        attr = {"POSITION": len(accs) - 3, "NORMAL": len(accs) - 2}; ind = len(accs) - 1
        if m.UV:
            vu = gomu(struct.pack("<%df" % (2 * len(m.UV)), *[c for u in m.UV for c in u]), 34962); accs.append({"bufferView": vu, "componentType": 5126, "count": len(m.UV), "type": "VEC2"}); attr["TEXCOORD_0"] = len(accs) - 1
        meshes.append({"name": adi, "primitives": [{"attributes": attr, "indices": ind, "material": adlar.index(mal)}]}); nd = {"mesh": len(meshes) - 1, "name": adi}
        if grup:
            pv = GRUP[grup]["pivot"]; nd["translation"] = [-pv[0], -pv[1], -pv[2]]; cocuk.setdefault(grup, []).append(len(nodes))
        else: kok.append(len(nodes))
        nodes.append(nd)
    n = int(round(DONGU / DT)); ts = [DONGU * i / n for i in range(n + 1)]
    vt = gomu(struct.pack("<%df" % len(ts), *ts)); accs.append({"bufferView": vt, "componentType": 5126, "count": len(ts), "type": "SCALAR", "min": [0.0], "max": [DONGU]}); a_t = len(accs) - 1
    kanallar, samplerlar = [], []
    for g, c in cocuk.items():
        bil = GRUP[g]; nodes.append({"name": "DON_" + g, "translation": list(bil["pivot"]), "children": c}); gi = len(nodes) - 1; qs = []
        for t in ts:
            a = 2 * math.pi * bil["aci"](t); s, co = math.sin(a / 2), math.cos(a / 2); qs += [0.0, 0.0, s, co] if bil["eksen"] == "z" else [0.0, s, 0.0, co]
        vq = gomu(struct.pack("<%df" % len(qs), *qs)); accs.append({"bufferView": vq, "componentType": 5126, "count": len(ts), "type": "VEC4"})
        samplerlar.append({"input": a_t, "output": len(accs) - 1, "interpolation": "LINEAR"}); kanallar.append({"sampler": len(samplerlar) - 1, "target": {"node": gi, "path": "rotation"}})
        if bil.get("kay"):
            nodes.append({"name": "KAY_" + g, "children": [gi]}); ki = len(nodes) - 1; kok.append(ki); ks = [c_ for t in ts for c_ in bil["kay"](t)]
            vk = gomu(struct.pack("<%df" % len(ks), *ks)); accs.append({"bufferView": vk, "componentType": 5126, "count": len(ts), "type": "VEC3"})
            samplerlar.append({"input": a_t, "output": len(accs) - 1, "interpolation": "LINEAR"}); kanallar.append({"sampler": len(samplerlar) - 1, "target": {"node": ki, "path": "translation"}})
        else: kok.append(gi)
    images, textures, doku_idx = [], [], {}
    for k, veri in dokular.items():
        images.append({"bufferView": gomu(veri), "mimeType": "image/png"}); textures.append({"source": len(images) - 1, "sampler": 0}); doku_idx[k] = len(textures) - 1
    mats = []
    for k in adlar:
        d = MALZEME[k]; pbr = {"baseColorFactor": list(d["renk"]), "metallicFactor": d["met"], "roughnessFactor": d["ruf"]}
        if d.get("doku"): pbr["baseColorTexture"] = {"index": doku_idx[d["doku"]]}
        mm = {"name": k, "pbrMetallicRoughness": pbr, "doubleSided": not d.get("tekyuz", False)}
        if d.get("saydam"): mm["alphaMode"] = "BLEND"
        mats.append(mm)
    while off[0] % 4: blob.append(b"\x00"); off[0] += 1
    bb = b"".join(blob)
    g = {"asset": {"version": "2.0", "generator": "AUTOKITCH kusbasi_cad_v2"}, "scene": 0, "scenes": [{"nodes": kok}], "nodes": nodes, "meshes": meshes, "materials": mats, "accessors": accs,
         "bufferViews": views, "buffers": [{"byteLength": len(bb)}], "images": images, "textures": textures, "samplers": [{"magFilter": 9729, "minFilter": 9987, "wrapS": 33071, "wrapT": 33071}],
         "animations": [{"name": "calis", "channels": kanallar, "samplers": samplerlar}]}
    js = json.dumps(g, separators=(",", ":")).encode("utf-8")
    while len(js) % 4: js += b" "
    with open(yol, "wb") as f:
        f.write(struct.pack("<4sII", b"glTF", 2, 12 + 8 + len(js) + 8 + len(bb))); f.write(struct.pack("<I4s", len(js), b"JSON")); f.write(js); f.write(struct.pack("<I4s", len(bb), b"BIN\x00")); f.write(bb)
    return len(bb) + len(js)


def cakisma_tara(parcalar, esik=1.0):
    """her parça çifti için ortak hacim (mm³) — iç içe geçen var mı?"""
    S = [(p["ad"], p["wp"].val(), p["wp"].val().BoundingBox()) for p in parcalar]; bulgu = []
    for i in range(len(S)):
        for j in range(i + 1, len(S)):
            a, b = S[i][2], S[j][2]
            if a.xmax < b.xmin or b.xmax < a.xmin or a.ymax < b.ymin or b.ymax < a.ymin or a.zmax < b.zmin or b.zmax < a.zmin: continue
            try: v = S[i][1].intersect(S[j][1]).Volume()
            except Exception: v = -1.0
            if v > esik or v < 0: bulgu.append((S[i][0], S[j][0], v))
    return bulgu


def cakisma_cift(A, B, esik=1.0):
    bulgu = []
    for p in A:
        sa = p["wp"].val(); a = sa.BoundingBox()
        for q in B:
            sb = q["wp"].val(); b = sb.BoundingBox()
            if a.xmax < b.xmin or b.xmax < a.xmin or a.ymax < b.ymin or b.ymax < a.ymin or a.zmax < b.zmin or b.zmax < a.zmin: continue
            try: v = sa.intersect(sb).Volume()
            except Exception: v = -1.0
            if v > esik or v < 0: bulgu.append((p["ad"], q["ad"], round(v, 1)))
    return bulgu


if __name__ == "__main__":
    t0 = time.time(); kap(); n_kap = len(PARCALAR)
    print("KAP: %d parca · %.0f sn" % (n_kap, time.time() - t0))
    gecersiz = [p["ad"] for p in PARCALAR if not p["wp"].val().isValid()]
    print("KATI DENETIMI: %s" % ("hepsi gecerli" if not gecersiz else "GECERSIZ: " + ", ".join(gecersiz)))
    assert not gecersiz
    bulgu = cakisma_tara(PARCALAR)
    print("CAKISMA TARAMASI (%d parca, esik 1 mm3): %s" % (n_kap, "TEMIZ — ic ice gecen parca yok" if not bulgu else "%d BULGU" % len(bulgu)))
    for a, b, v in bulgu: print("   %-22s × %-22s ortak hacim %.1f mm3" % (a, b, v))
    # dönen grupları çevirip sabit parçalara karşı tara
    sabit = [p for p in PARCALAR if not p["grup"]]; donen = {}
    for p in PARCALAR:
        if p["grup"]: donen.setdefault(p["grup"], []).append(p)
    for g, eks_y in (("helezon", CY), ("karistirici", YC)):
        for aci in (30.0, 60.0, 90.0, 135.0):
            cev = [dict(ad=p["ad"] + "@%d" % aci, wp=cq.Workplane(obj=p["wp"].val().rotate(cq.Vector(0, eks_y, 0), cq.Vector(0, eks_y, 1), aci)), grup=g) for p in donen[g]]
            diger = [p for gg, L in donen.items() if gg != g for p in L]
            b2 = cakisma_cift(cev, sabit + diger)
            print("   %s %3.0f° donmus: %s" % (g, aci, "temiz" if not b2 else b2))
    # ---- KANAT DENETİMİ: üçgen ağında her 5 mm dilimde kanat ucu r ≈ 20 mi? (boolean ve 'isValid' yanıltıyor; ağ = basılacak şeyin kendisi) ----
    ADK = {p["ad"]: p["wp"].val() for p in PARCALAR}; print("KANAT DENETIMI (ag uzerinde, 5 mm dilimlerde en buyuk yaricap):", end=" "); eksik = []
    ZC1, ZC2 = bolme_z(9), bolme_z(18)
    for ad, zA, zB in (("helezon_A", KAN_Z0, ZC1), ("helezon_B", ZC1, ZC2), ("helezon_C", ZC2, UC_Z0), ("helezon_D", UC_Z0, UC_Z1)):
        vs, _ = ADK[ad].tessellate(0.1, 0.2); mx = {}
        for v in vs: b = int(v.z // 5); mx[b] = max(mx.get(b, 0.0), math.hypot(v.x, v.y - CY))
        dilim = [b for b in range(int((zA + 4) // 5), int((zB - 4) // 5) + 1)]; kotu = [b * 5 for b in dilim if mx.get(b, 0.0) < R_KANAT - 0.1]
        print("%s %d/%d" % (ad[-1], len(dilim) - len(kotu), len(dilim)), end=" · ")
        if kotu: eksik.append((ad, kotu))
    print("→ %s" % ("TAMAM: kanat her yerde Ø68" if not eksik else "EKSIK: %s" % eksik)); assert not eksik
    # ---- çalışma boşlukları (en yakın mesafe, mm) ----
    AD = {p["ad"]: p["wp"].val() for p in PARCALAR}
    CIFT = [("helezon_A", "govde", "kanat ↔ tekne (tasarım 2,0)"), ("helezon_D", "cikis_tupu", "kanat ↔ tüp (2,0)"), ("helezon_C", "plaka_on", "kanat ↔ ön plaka deliği (2,0)"), ("helezon_A", "helezon_B", "segment eki: miller uç uca yaslanır (0)"),
            ("helezon_D", "yatak_kapagi", "ön muylu ↔ yatak (0,2)"), ("helezon_A", "gobek_helezon", "helezon arkası ↔ göbek flanşı (0,5)"), ("gobek_helezon", "plaka_arka", "muylu ↔ plaka deliği (0,2)"),
            ("on_kovan", "plaka_on", "kovan ↔ plaka deliği (0,2)"), ("orumcek_orta", "govde", "rotor kolu ↔ kâse"), ("cubuk_0", "govde", "SIYIRICI LAMA ↔ kâse (hedef 2–3)"),
 ("orumcek_arka", "gobek_karistirici", "örümcek ↔ göbek flanşı (1,0)"), ("orumcek_on", "on_kovan", "örümcek ↔ kovan flanşı (1,0)"),
            ("topuz", "plaka_on", "topuz ↔ plaka (1,0)"), ("topuz", "on_kovan", "topuz eteği ↔ kovan (0,25)"), ("saplama_2", "govde", "üst saplama ↔ gövde"),
            ("tasima_tapasi", "cikis_tupu", "tapa ↔ boru ucu (0,2)"), ("kulp", "topuz", "kulp ↔ topuz")]
    print("CALISMA BOSLUKLARI (olculen en yakin mesafe):"); BOSLUK = []
    asagi = AD["orumcek_orta"].rotate(cq.Vector(0, YC, 0), cq.Vector(0, YC, 1), -90.0)               # rotor kolu AŞAĞI bakarken
    dA = asagi.distance(AD["helezon_B"]); BOSLUK.append(("orumcek_orta (kol aşağı)", "helezon_B", "rotor kolu ↔ helezon kanadı", round(dA, 2)))
    print("   %-16s ↔ %-18s %6.2f mm   %s" % ("orumcek (kol asagi)", "helezon_B", dA, "rotor kolu ↔ helezon kanadı"))
    for a_, b_, acik in CIFT:
        d = AD[a_].distance(AD[b_]); BOSLUK.append((a_, b_, acik, round(d, 2))); print("   %-16s ↔ %-18s %6.2f mm   %s" % (a_, b_, d, acik))
    # ---- üretim dosyaları ----
    os.makedirs(os.path.join(URETIM, "step"), exist_ok=True); os.makedirs(os.path.join(URETIM, "stl"), exist_ok=True)
    asm = cq.Assembly(name="KUSBASI_KASETI_v4"); RENK = dict(cam=(0.75, 0.85, 0.92, 0.45), pom=(0.95, 0.95, 0.92, 1), celik=(0.75, 0.77, 0.8, 1), silikon=(0.16, 0.5, 0.95, 1), koyu=(0.15, 0.15, 0.17, 1))
    bom = []
    for p in PARCALAR:
        sh = p["wp"].val(); bb = sh.BoundingBox()
        cq.exporters.export(p["wp"], os.path.join(URETIM, "step", p["ad"] + ".step"))
        cq.exporters.export(p["wp"], os.path.join(URETIM, "stl", p["ad"] + ".stl"), tolerance=0.05, angularTolerance=0.15)
        asm.add(sh, name=p["ad"], color=cq.Color(*RENK.get(p["mal"], (0.8, 0.8, 0.8, 1))))
        if p["bom"]: bom.append((p["ad"],) + tuple(p["bom"]) + ("%.0f × %.0f × %.0f" % (bb.xlen, bb.ylen, bb.zlen), "%.1f" % (sh.Volume() / 1000.0)))
    asm.save(os.path.join(URETIM, "KUSBASI_KASETI_v4_MONTAJ.step"))

    # ---- TEK PARÇA HELEZON (bölmesiz) · 304 mm'lik yazıcısı/tezgâhı olan için ----
    tek = cq.Workplane(obj=cq.Workplane("XZ").polyline(
        [(0.0, -151.0), (R_KOK, -151.0), (R_MIL, KOK_Z0), (R_MIL, UC_Z0), (0.0, UC_Z0)]).close()
        .revolve(360, (0, 0, 0), (0, 1, 0)).val().translate(cq.Vector(0, CY, 0)))
    tek = kaynat_kanat(tek, kanat_surekli(KAN_Z0, KAN_Z1), "tek parca kanat")
    v0 = tek.val().Volume()
    for clean in (True, False):
        r = tek.cut(karez(0, CY, KARE + 0.3, -153.0, UC_Z0 + 1.0), clean=clean)
        if r.val().isValid() and 0.5 * v0 < r.val().Volume() < v0 - 1000: tek = r; break
    cq.exporters.export(tek, os.path.join(URETIM, "step", "helezon_TEK_PARCA.step"))
    cq.exporters.export(tek, os.path.join(URETIM, "stl", "helezon_TEK_PARCA.stl"))

    # ---- HATVE DENETİMİ: katının KENDİ üstünde ölç (tasarım değeriyle karşılaştır) ----
    vs, _ = tek.val().tessellate(0.03, 0.05)
    ray = sorted(v.z for v in vs if abs(v.y - CY) < 0.6 and v.x > R_KANAT - 0.4)          # θ≈0 ışınında, kanat ucunda
    kume = []
    for z in ray:
        if kume and z - kume[-1][-1] < 2.0: kume[-1].append(z)
        else: kume.append([z])
    orta = [sum(c) / len(c) for c in kume]     # her tur İKİ küme verir: kanadın alt yüzü ve 3 mm üstteki üst yüzü
    print("HATVE DENETIMI (tek parca katisinin uzerinde, θ=0 isininda ardisik turlar):")
    kotu = []
    for i in range(len(orta) - 2):
        zm = (orta[i] + orta[i + 2]) / 2; olc = orta[i + 2] - orta[i]; bek = hatve(zm)   # aynı yüzden aynı yüze = hatve
        if abs(olc - bek) > 0.40: kotu.append((round(zm), round(olc, 2), round(bek, 2)))
        if i % 4 == 0: print("   z %6.0f  olculen %5.2f  tasarim %5.2f mm" % (zm, olc, bek))
    print("   → %s (%d tur olculdu · hatve %.2f → %.2f · toplam %.4f tur)"
          % ("TAMAM" if not kotu else "SAPMA: %s" % kotu, len(orta), hatve(KAN_Z0), hatve(KAN_Z1), teta_z(KAN_Z1) / (2 * math.pi)))
    assert not kotu, kotu
    print("   tek parca: boy %.0f mm · hacim %.0f cm3" % (UC_Z0 + 151.0, tek.val().Volume() / 1000.0))
    with io.open(os.path.join(URETIM, "BOM.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";"); w.writerow(["dosya", "parça", "adet", "malzeme · yöntem", "görevi", "zarf mm", "hacim cm3"]); w.writerows(bom)
    with io.open(os.path.join(URETIM, "bom.json"), "w", encoding="utf-8") as f: json.dump(bom, f, ensure_ascii=False)
    with io.open(os.path.join(URETIM, "denetim.json"), "w", encoding="utf-8") as f:
        json.dump(dict(parca=n_kap, kalem=len(bom), cakisma=len(bulgu), bosluk=BOSLUK), f, ensure_ascii=False)
    print("URETIM: %d STEP + %d STL + MONTAJ.step + BOM.csv (%d kalem) → %s" % (n_kap, n_kap, len(bom), URETIM))
    for b in bom: print("   %-18s %-34s ×%s  %s" % (b[0], b[1], b[2], b[5]))
    # ---- web modeli ----
    V = v4.hacim_L(Y_DOLUM); yd = v4.dolum_kotu(KG2 / RHO)
    print("HACIM %.1f L (ic boy %.0f) · %.1f kg @ %.2f → dolum kotu y %.0f (%%%.0f)" % (V, D - 2 * TP, KG2, RHO, yd, 100 * KG2 / RHO / V))
    import kusbasi_akis_model_v2 as KM                                    # CAD ile HESAP aynı sayıları mı kullanıyor?
    Gm = KM.G; esit = dict(RT=RT, R_MIL=R_MIL, R_KOK=R_KOK, P0=HATVE0, ESIK=ESIK_Y, T=4.0)
    sup = 40.0 + math.hypot(15.0 / 2, 3.0 / 2); olc = dict((x[0] + "|" + x[1], x[3]) for x in BOSLUK)["cubuk_0|govde"]; assert abs(olc - (RB - sup)) < 0.3, "lama-duvar olcumu %.2f, beklenen %.2f" % (olc, RB - sup)
    assert abs(Gm["LAMA_DUVAR"] - (RB - sup)) < 0.2 and abs(Gm["ROTOR_BOSLUK"] - (YC - sup - CY - R_KANAT)) < 0.2, "rotor araliklari model ile ayni degil: duvar %.1f · kanat %.1f" % (RB - sup, YC - sup - CY - R_KANAT)
    for k_, v_ in esit.items(): assert abs(Gm[k_] - v_) < 1e-6, "model ile CAD ayni degil: %s %s != %s" % (k_, Gm[k_], v_)
    assert abs(Gm["P1"] - HATVE1) < 0.05 and abs(Gm["AGIZ"][0] - 2 * AG_X) < 1e-6 and abs(Gm["AGIZ"][1] - (AG_Z1 - AG_Z0)) < 1e-6 and abs(Gm["TIKAC"] + Gm["ESIK"] - (AG_Z0 - UC_Z1)) < 1e-6
    q_on = KM.kapasite(1.0)[4]; g_tur = q_on * 0.60 * RHO
    print("MODEL = CAD · on uc %.1f mL/tur (Roberts) · doluluk 0,60 VARSAYIM → %.0f g/tur · 145 g = %.2f tur · %.0f dev/dk" % (q_on, g_tur, 145.0 / g_tur, 145.0 / g_tur * 6.0))
    dokular = {"ad": doku_ad("KUŞBAŞI KASETİ", "bu yönde tak  ·  140 × 325 × 360 mm  ·  %s L  ·  çıkış ÖNDE alttan" % ("%.1f" % V).replace(".", ","), ok_sol=True),
               "montaj": doku_montaj(["HELEZONU|ÖNDEN SÜR", "YATAK KAPAĞI|İT · 35° ÇEVİR · KLİK", "ROTOR · MİL|TOPUZ · PİM", "TAPAYI ÇIKAR|YUVAYA SÜR"])}
    def etiketler():
        e0, e1 = (Y_UST - 56) * MM, (Y_UST - 8) * MM; ez = (D / 2 - TP - 6) * MM; xo = (RB + ET + 0.4) * MM; L = []
        L.append(("etiket_ad", etiket_yuzu(-xo, e0, e1, -ez, ez, -1), "etiket_ad", None)); L.append(("etiket_montaj", etiket_yuzu(xo, e0, e1, ez, -ez, 1), "etiket_montaj", None))
        for adi, xx, nx in (("etiket_ad_arka", -xo + 0.0002, 1), ("etiket_montaj_arka", xo - 0.0002, -1)):
            ar = Mesh(); ar.quad((xx, e0, -ez), (xx, e0, ez), (xx, e1, ez), (xx, e1, -ez), (nx, 0, 0)); L.append((adi, ar.duzelt(), "sari_arka", None))
        return L
    kap_ag = [(p["ad"], BR.web_ag(ag, p), p["mal"], p["grup"]) for p in PARCALAR if p["ad"] != "tasima_tapasi"] + etiketler()
    b1 = glb_yaz(os.path.join(OUT, "kusbasi_v8.glb"), kap_ag, dokular)
    print("kusbasi_v8.glb · %d parca · %d ucgen · %.0f KB" % (len(kap_ag), sum(len(m.I) // 3 for _, m, _, _ in kap_ag), b1 / 1024.0))
    b2, prim, sorun, uyari = usdz_yaz([os.path.join(OUT, "kusbasi_v8.usdz")], "kusbasi_v8", [(a, m, mal) for a, m, mal, _ in kap_ag], dokular)
    print("   usdz %.0f KB · %d prim · USD denetimi: %s" % (b2 / 1024.0, prim, "GECTI" if not sorun else "KALDI")); [print("   HATA:", x) for x in sorun]
    n0 = len(PARCALAR); zc, y_pide, xt = makine()
    doz = kap_ag + [(p["ad"], BR.web_ag(ag, p), p["mal"], p["grup"]) for p in PARCALAR[n0:]]
    rnd = random.Random(11); ks = Mesh(); d_k = 10.0
    for i in range(137):                                                                       # pide üstünde 137 küp (145 g · d 10)
        rr = 118.0 * math.sqrt(rnd.random()); a = rnd.uniform(0, 2 * math.pi); x, z = xt + rr * math.cos(a), zc + rr * math.sin(a)
        ks.ekle(kutu((x - d_k / 2) * MM, (x + d_k / 2) * MM, (y_pide + 0.3) * MM, (y_pide + 0.3 + d_k * 0.8) * MM, (z - d_k / 2) * MM, (z + d_k / 2) * MM))
    doz.append(("kusbasi_pide_ustu", ks, "kusbasi", "tabla")); dk = Mesh()
    for i in range(9):                                                                         # ağızdan tek tek düşen küpler
        y = rnd.uniform(y_pide + 12, Y_AGIZ - 4); x, z = rnd.uniform(-AG_X + 6, AG_X - 6), rnd.uniform(AG_Z0 + 6, AG_Z1 - 6)
        dk.ekle(kutu((x - d_k / 2) * MM, (x + d_k / 2) * MM, y * MM, (y + d_k) * MM, (z - d_k / 2) * MM, (z + d_k / 2) * MM))
    doz.append(("kusbasi_dusen", dk, "kusbasi", None))
    dolgu = v4.kasar_dolgu(yd); doz.append(("kusbasi_dolgu", dolgu, "kusbasi_dolgu", None))
    b3 = glb_yaz(os.path.join(OUT, "kusbasi_v8_dozaj.glb"), doz, dokular)
    print("kusbasi_v8_dozaj.glb · %d parca · %.0f KB · toplam %.0f sn" % (len(doz), b3 / 1024.0, time.time() - t0))
    sys.stdout.flush(); os._exit(0)                                     # OCC nesneleri kapanışta çöküyordu (exit 139): denetimler bittikten sonra doğrudan çık
