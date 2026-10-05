# -*- coding: utf-8 -*-
"""h3_b_sac_v1 — B (ÇEKMECELİ SOĞUK DOLAP) GÖVDESİ · ÜRETİM SACI v1 (4 Eki 2026 · Claude · YEREL · bağımsız üreteç, montaja bağlı DEĞİL)

Kemal: "üretim sacını yap ama tam yap, üretime yönelik" · "altı üstü basit bir çekmece dolabı" · "yalıtım hiçbir yerde görünmesin, sac ile yalıtım
arası boşluk olmasın". STANDART: h3_k_sac_v1 / h3_a_sac_v1 ile aynı · h3_sac_v1 kütüphanesi (gerçek büküm, K 0,45, açınım, DFM, PEM / vida BOM) ·
sac_kararlar_v1 (dış kabuk 304 1,5 · iç kabuk 304 1,2 · ön çerçeve 430 ferritik 1,0 (manyetik fitil) · gıda bölgesi iç köşe R ≥ 3, bindirme yok).
KOORDİNAT: DÜNYA (mm · x hat boyu · y yukarı · z ön +). B zarfı x 736–4400 · y 123–788 · z −830…+39 (kapaklar / fitil CEK_* parçalarında, +39…+79).

KURGU (sandviç soğuk dolap — köpükleme kalıbı mantığı: her PU bloğu sac + sac + ön çerçeve + komşu blok ile KAPALI hacim, köpük yerinde dolar)
  1 · DIŞ KABUK 304 1,5 (gizli birleşim, dışta vida başı yok):
      sol / sağ yan = arka 25 mm İÇE dönüşlü sac (arka saca punta) · tavan / taban ↔ yan: 1,5 L KÖŞEBENT 25 × 25 parçaları (modüler GFRP pedleri,
      Secop rayları ve depo sacı arasında · ikisine de punta) · tavan / taban / arka 3661 mm > 3000 levha → iki parça, ek yeri x 2091 (B2 bölmesi
      ekseni) · 0,5 alın aralığı + iç yüzde 80 mm EK LAMASI (punta; tavanda GFRP pedleri arasında 3 parça) · arka = tava (üst + alt 25 mm öne dönüş,
      uçlarda yan dönüşüne 27 mm pay) · ısı kalkanı arka yarıkları + Secop emiş pencereleri lazerde (zemin elektrik kovanı 1. emiş penceresinden
      çıkar) · tavanda A → B 6 × Ø9, K → B 2 × Ø9 (komşu üreteçlerin ARAYÜZ'ü) · tabanda alt şaseye 10 × M8 (Ø9 · cıvata köpüklemeden önce içeriden).
  2 · ÖN ÇERÇEVE 430 1,0 (manyetik kapı fitili buna yapışır): iki parça (ek x 2091, B2 bölmesinin önündeki 35 mm EK LAMASINA punta) · 21 çekmece +
      depo + Secop servis açıklığı lazerde · çerçeve çevresi dış kabuğa iç köşeden TIG dikiş (20 / 150) + gıda silikonu · iç kabuk / bölme ön kenarları
      çerçevenin arka yüzüne ALIN dayanır (MS polimer + köpük bağı) — ön kenarlarda büküm YOK: büküm dış yayı çerçeve köşesinde boşluk / görünür PU
      bırakırdı (denetimde bulundu).
  3 · İÇ KABUK 304 1,2 (gıda bölgesi): iç taban + arka duvar + sol duvar + iç tavan ayrı DÜZ saclar (B_KABLO dikey kanalları ve ray braketleri
      köşelere dik oturduğu için bükümlü R köşe yapılmadı) · iç köşeler sürekli TIG + taşlama · iç taban / arka / tavan iki parça: x 797,3–2108,5
      (yüksek, 728) ve 2108,5–4027,3 (alçak, 668) · ek yeri K3 sol köşesi (B2 sacı b ile aynı çizgide TIG) · gömülü dikmelerin (modüler + taşıyıcı,
      bölmelerin içinde) geçtiği yerlerde 31 × 31 delik (bölme altında, gıda bölgesi dışında).
  4 · BÖLMELER B1–B5: sac 1,2 + PU 32,6 + sac 1,2 = 35 (düz sac) · ray bağlantısı için her ray başına 3 × PEM SP-M5 (gövde PU tarafında, köpük
      kapağı ile) · hava / kablo kanalı geçişleri 1,2 sac U KOVAN (1 mm boşluklu · bölme saclarına TIG) · kapalı geçiş (B5 depo havası) iki L ·
      gider kılıfı deliği (B5'te alta açık U çentik) · B5'in teknik tarafı tam boy KAPAMA SACI (teknik_sol_duvar) · B2 sacları ve PU önü z 22'de
      (çerçeve ek lamasına yer).
  5 · FIRIN ALTI ISI KALKANI: ayırma sacı + iki yan = TEK U (1,2 · yanlar yukarı) · üstünde 12 PTFE / cam elyaf TAKOZ + 0,8 parlak ışınım sacı ·
      hava boşluğu (729,2–786,5) önü çerçeve, arkası arka sacın 7 yarığı · taşıyıcı kirişler boşlukta (U yanlarında açık çentik).
  6 · TEKNİK SÜTUN (4028,5–4398,5): ara katman arka sacı 1,2 · depo / Secop / ara katman sacları B_DEPO / B_SOGUTMA'da (değişmez, PU onlara oturur).
  7 · PU (yerinde köpük 40 kg/m³): mevcut 21 blok bölgesi − bütün saclar − gömülü elemanlar (modüler iskelet, taşıyıcı, kablo kanalı, gider kılıfı,
      B iç elektrik kanalı, depo sacları) → PU şekli = boşluğun kendisi; hiçbir PU yüzü havaya bakmaz (denetim).
ARAYÜZLER DEĞİŞMEZ: dış zarf · 788 üst düz yüzü · çekmece açıklıkları · fitil arkası z 24 · ray yüzleri (798,5 · 1418,5 · 1453,5 · …) · B_TASIYICI /
  B_MODULER / B_DEPO / B_SOGUTMA / B_ELEKTRIK / B_KABLO / ayaklar (B_KASA__celik) · gider hattı ekseni.
KALDIRILAN: eski elektrik ana hat kovanları (TOPPING altı + B5 üstü) — v8zj'den beri içlerinden kablo geçmiyor (v8zq'da boş).
Çalıştır (denetim + çıktılar): gece2/adim5/b_sac_denetim_v1.py (scratchpad) · bu dosya yalnız KURAR."""
import math, os, sys, re, time
H3 = os.path.dirname(os.path.abspath(__file__)); _U = os.path.dirname(H3)
for _p in (_U, H3):
    if _p not in sys.path: sys.path.insert(0, _p)
import numpy as np
import cadquery as cq
import h3_sac_v1 as S

SURUM = "h3_b_sac_v1"
V = cq.Vector
X_A = 0.0                                                                # dünya koordinatı (öteleme yok)
BIRIM = "B_GOVDE"
# ---------------------------------------------------------------- ARAYÜZ (dünya · değişmez)
T_D, T_I, T_C, T_ISIN = 1.5, 1.2, 1.0, 0.8
X0, X1 = 736.0, 4400.0
YB, YT = 123.0, 788.0
ZA, ZF = -830.0, 39.0
ZC0, ZC1 = 23.0, 24.0                                                    # ön çerçeve (fitil arkası 24)
XDi, XDs = X0 + T_D, X1 - T_D                                            # 737,5 · 4398,5
YDi, YDs = YB + T_D, YT - T_D                                            # 124,5 · 786,5
ZDa = ZA + T_D                                                           # −828,5
XL = 798.5                                                               # sol soğuk yüz
YF, YCH, YCL = 164.5, 728.0, 668.0                                       # iç taban üstü · iç tavan altı (yüksek K1–K2 / alçak K3–K6)
ZB = -790.0                                                              # arka soğuk yüz
X_ALCAK = 2108.5
XFIR = 2500.0
BOLME = [1418.5, 2073.5, 2728.5, 3383.5, 3993.5]
BW = 35.0
T0 = 4028.5
XB5b = T0 - T_I                                                          # 4027,3
X_EK = 2091.0                                                            # dış kabuk + çerçeve ek yeri (B2 bölmesi ekseni)
R_GIDA = 3.0                                                             # gıda bölgesi iç büküm yarıçapı
CEK = [("K1", 798.5, 620.0, [200.5, 308.5, 416.5, 524.5, 632.5], [75.0] * 5),
       ("K2", 1453.5, 620.0, [200.5, 308.5, 416.5, 524.5, 632.5], [75.0] * 5),
       ("K3", 2108.5, 620.0, [200.5, 308.5, 416.5, 524.5], [75.0] * 4),
       ("K5", 2763.5, 620.0, [200.5, 308.5, 416.5, 524.5], [75.0, 75.0, 75.0, 126.0]),
       ("K6", 3418.5, 575.0, [200.5, 308.5, 471.5], [75.0, 130.0, 130.0])]
ACIKLIK = [(k, x, x + w, y, y + h) for k, x, w, ys, hs in CEK for y, h in zip(ys, hs)]
DEPO_ACIK = (4028.5, 4337.5, 463.5, 707.5)
SERVIS_ACIK = (4030.5, 4369.5, YDi - 1.0, 431.0)                         # Secop servis açıklığı · alt kenara açık (eski 1,5 mm şerit kalktı)
DEPO_TAVAN_YUVA = (T0, 4338.5, 728.0, 729.0)                             # B_DEPO depo tavan iç sacı çerçeveden geçer (+37,5'e)
EMIS_T = [(4033.0, 4140.0), (4160.0, 4267.0), (4287.0, 4394.0)]          # taban: Secop emiş pencereleri · z −695…−565
# ELK_ZEMIN kovanı (x 4065–4115 · z −665…−595, contalı) 1. emiş penceresinin içinden çıkar → ayrı ağız gerekmez
ARKA_YARIK = [(2540.0 + 205.0 * i, 2725.0 + 205.0 * i) for i in range(7)]  # arka: ısı kalkanı hava boşluğu · y 748–778
TAKOZ_XZ = [(x, z) for x in (2650.0, 3050.0, 3350.0, 3700.0) for z in (-700.0, -250.0, 10.0)]
KANAL = [(988.5, 1028.5, 164.5, 703.0), (1643.5, 1683.5, 164.5, 703.0), (2298.5, 2338.5, 164.5, 643.0), (2953.5, 2993.5, 164.5, 643.0),
         (3608.5, 3648.5, 164.5, 643.0), (988.5, 2072.5, 703.0, 728.0), (2032.5, 2072.5, 668.0, 703.0), (2072.5, 4032.5, 643.0, 668.0)]
KAN_Z = (-790.0, -765.0)                                                 # B_KABLO kanalı (gömülü değil: arka iç yüze yaslı, bölmelerden kovanla geçer)
GID_A, GID_B, GID_R = (2023.5, 200.5, -738.0), (4073.5, 177.95, -738.0), 12.0
HAVA = {0: [(190.0, 290.0), (560.0, 660.0)], 1: [(190.0, 290.0), (560.0, 660.0)], 3: [(190.0, 290.0), (400.0, 490.0)]}
HAVA_Z = (-790.0, -760.0)
DEPO_HAVA, DEPO_HAVA_Z = [(550.0, 600.0), (610.0, 660.0)], (-430.0, -380.0)
AB_DELIK = [(761.0, -706.0), (761.0, -110.0), (1086.0, -706.0), (1086.0, -110.0), (1411.0, -706.0), (1411.0, -110.0)]   # h3_a_sac_v1.AB_M8 (dünya)
KB_DELIK = [(4016.5, -480.0), (4016.5, -570.0)]                          # h3_k_sac_v1 K → B
SASE_M8 = [(x, z) for x in (1100.0, 1750.0, 2400.0, 3050.0, 3700.0) for z in (-760.0, -110.0)]   # taban ↔ alt şase boyunaları (z −790…−730 · −140…−80)
# gömülü elemanlar (PU bunların etrafına dolar · v8zq'dan ölçü) — (ad, x0, x1, y0, y1, z0, z1)
GOMULU = [("modüler dikme", 737.5, 767.5, 124.5, 753.5, -721.0, -691.0), ("modüler dikme", 1421.0, 1451.0, 124.5, 753.5, -721.0, -691.0),
          ("modüler dikme", 2076.0, 2106.0, 124.5, 753.5, -721.0, -691.0), ("modüler dikme", 737.5, 767.5, 124.5, 753.5, -125.0, -95.0),
          ("modüler dikme", 1421.0, 1451.0, 124.5, 753.5, -125.0, -95.0), ("modüler dikme", 2076.0, 2106.0, 124.5, 753.5, -125.0, -95.0),
          ("modüler üst kiriş", 737.5, 2106.0, 753.5, 786.5, -721.0, -691.0), ("modüler üst kiriş", 737.5, 2731.0, 753.5, 786.5, -125.0, -95.0),
          ("taşıyıcı", 2731.0, 4026.0, 746.5, 786.5, -130.0, -90.0), ("taşıyıcı", 2502.5, 4026.0, 746.5, 786.5, -640.0, -600.0),
          ("taşıyıcı", 2502.5, 2532.5, 746.5, 786.5, -600.0, -125.0), ("taşıyıcı", 2731.0, 2761.0, 746.5, 786.5, -600.0, -130.0),
          ("taşıyıcı", 3386.0, 3416.0, 746.5, 786.5, -600.0, -130.0), ("taşıyıcı", 3996.0, 4026.0, 746.5, 786.5, -600.0, -130.0)] + \
         [("taşıyıcı dikme", x - 15.0, x + 15.0, 124.5, 746.5, z - 15.0, z + 15.0) for x in (2746.0, 3401.0, 4011.0) for z in (-110.0, -620.0)] + \
         [("B iç elektrik kanalı (B2)", 2056.2, 2298.5, 610.0, 630.0, -790.0, -765.0), ("depo tavan iç sacı", 4028.5, 4338.5, 728.0, 729.0, -440.0, 37.5),
          ("depo arka sacı", 4028.5, 4398.5, 463.5, 786.5, -470.0, -469.0)] + \
         [("kablo kanalı", a, b, c, d, KAN_Z[0], KAN_Z[1]) for a, b, c, d in KANAL]
# PU blok bölgeleri (v8zq B_KASA__pu ile aynı 21 bölge; içinden saclar + gömülüler çıkar)
PU_BOLGE = [("pu_sol", XDi, 797.3, YDi, YDs, ZDa, ZC0), ("pu_taban", 797.3, XB5b, YDi, 163.3, -791.2, ZC0),
            ("pu_arka_yuksek", 797.3, XFIR, YDi, YDs, ZDa, -791.2), ("pu_arka_alcak", XFIR, XB5b, YDi, YCH, ZDa, -791.2),
            ("pu_tavan_yuksek", 797.3, X_ALCAK, 729.2, YDs, -791.2, ZC0), ("pu_tavan_topping", X_ALCAK, XFIR, 669.2, YDs, -791.2, ZC0),
            ("pu_tavan_firin", XFIR, XB5b, 669.2, YCH, -791.2, ZC0), ("pu_b5_ust", 3994.7, XB5b, YCH, YDs, ZDa, ZC0),
            ("tk_ara_pu", T0, XDs, 434.5, 462.5, -494.0, ZC0), ("tk_depo_arka_pu", T0, XDs, 463.5, YDs, -469.0, -441.0),
            ("tk_depo_sag_pu", 4338.5, XDs, 463.5, YDs, -441.0, ZC0), ("tk_depo_tavan_pu", T0, 4338.5, 729.0, YDs, -441.0, ZC0)] + \
           [("bolme_%d_pu" % (i + 1), BOLME[i] + T_I, BOLME[i] + BW - T_I, YF, YCH if i <= 1 else YCL, ZB, ZC0) for i in range(5)]
S._RENK.update({"pu": ((0.95, 0.85, 0.30, 1.0), 0.0, 0.9), "kapak": ((0.70, 0.82, 0.95, 1.0), 0.2, 0.25), "arayuz": ((0.90, 0.22, 0.15, 1.0), 0.3, 0.5),
                "cerceve": ((0.70, 0.72, 0.74, 1.0), 0.75, 0.35), "koyu": ((0.25, 0.25, 0.27, 1.0), 0.1, 0.8)})
ESKI_GOVDE = ("B_KASA__sac", "B_KASA__pu", "B_KASA__on_cerceve", "B_KASA__koyu")


def pu_ortu():
    """PU denetiminde örtücü sayılan gömülü eleman zarfları (v8zq'da açık ağ olanlar): gider kılıfı Ø24 (bölme geçiş kovanları açık ağ)"""
    return [gider_silindiri()]


def kutu(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), V(min(x0, x1), min(y0, y1), min(z0, z1)))


def gider_silindiri(r=GID_R, uzat=200.0):
    a, b = np.array(GID_A), np.array(GID_B); d = b - a; L = float(np.linalg.norm(d)); e = d / L
    return cq.Solid.makeCylinder(r, L + 2 * uzat, V(*(a - e * uzat)), V(*e))


def gider_noktasi(x):
    a, b = np.array(GID_A), np.array(GID_B); s = (x - a[0]) / (b[0] - a[0]); return a + (b - a) * s


# =====================================================================================================================================
class G:
    SAC, ELEMAN, KAYNAK, BIRLESIM, ARAYUZ, PU, KAYNAK_ETIKET, NOT, PU_KES, DIS_OLUK, PU_EK, KOSE_CEP = [], [], [], [], [], [], [], [], [], [], [], []
    PANEL = {}
    kuruldu = False


def _sac(ad, rol, **k):
    s = S.Sac(ad, rol=rol, birim=BIRIM, kaynak=SURUM, **k); G.SAC.append(s); return s


def _eleman(p, mal="celik"):
    p["mal"] = p.get("mal") if p.get("mal") not in (None, "katalog", "paslanmaz") else mal
    p["birim"] = BIRIM; G.ELEMAN.append(p); return p


def _arayuz(p, karsi, gerek, not_=""):
    p["tur"] = "arayuz"; p["arayuz"] = dict(karsi=karsi, gerek=gerek, not_=not_); p["birim"] = BIRIM; G.ARAYUZ.append(p); return p


def _etiket(ad, yontem, olcu, not_):
    G.KAYNAK_ETIKET.append(dict(ad=ad, yontem=yontem, olcu=olcu, not_=not_))


def r3_kose(P, zsg):
    """duvar sacının alt-arka köşesi: iç tabanın arka bükümü (iç R 3, merkez y 167,5 · z −787) metaline girmesin → yaya uyan kesik (TIG ile kapanır)"""
    yc, zc, r = YF + R_GIDA, ZB + R_GIDA, R_GIDA
    pts = [(YF - 1.0, zsg * (ZB - 1.0)), (YF - 1.0, zsg * zc), (YF, zsg * zc)]
    for k in range(1, 16):
        a = math.pi + (math.pi / 2.0) * k / 16.0
        pts.append((yc + r * math.cos(a), zsg * (zc + r * math.sin(a))))
    pts += [(yc, zsg * ZB), (yc, zsg * (ZB - 1.0))]
    if zsg < 0: pts = pts[::-1]
    P.kesik(pts, tip="r3_kose_kesigi", dfm=False, parca="iç taban arka bükümü R3 yayına uyum")


def arka_donus_kesigi(P, xd, ust=True, c=0.0):
    """arka sacın üst / alt dönüşünün (t 1,5 · R 2,25 · 25 mm) dik sacdan geçtiği yer: kesik büküm kesitine uyar (0,2 boşluk) → köpük / hava geçmez"""
    t, R = T_D, 2.25; Ro = R + t
    sg = 1.0 if ust else -1.0
    yk = (YDs - Ro) if ust else (YDi + Ro)                                    # arka kökünün dönüşe başladığı y
    zc = ZDa + R                                                              # büküm merkezi z
    yi = (YDs - t - c) if ust else (YDi + t + c)                              # dönüş iç yüzü (+ boşluk)
    pts = [(yk + sg * 4.5, ZDa - 0.1), (yk - sg * c, ZDa - 0.1), (yk - sg * c, zc - (R - c))]
    for k in range(1, 17):
        th = (math.pi / 2.0) * k / 16.0
        pts.append((yk + sg * (R - c) * math.sin(th), zc - (R - c) * math.cos(th)))
    pts += [(yi, ZA + 25.0 + c), (yk + sg * 4.5, ZA + 25.0 + c)]
    loc = [P.yerel((xd, y, z)) for y, z in pts]
    P.kesik([(q[0], q[1]) for q in loc], tip="arka_donus_kesigi", dfm=False, parca="arka sacın %s dönüşü geçişi (büküm kesitine birebir uyan · TIG ile kapatılır)" % ("üst" if ust else "alt"))


def oluk(eksen, a0, a1, c1, c2, s1, s2, Ro):
    """büküm dış yayının dışında kalan köşe oluğu: eksen boyunca a0–a1 · büküm merkezi (c1, c2) (eksene dik iki koordinat, sıra x-y-z) ·
    s1 / s2: köşenin merkezden hangi yönde olduğu (±1) · kare Ro × Ro − daire Ro"""
    i = "xyz".index(eksen); dik = [k for k in range(3) if k != i]
    lo = [0.0] * 3; hi = [0.0] * 3
    lo[i], hi[i] = a0, a1
    for k, c, sg in ((dik[0], c1, s1), (dik[1], c2, s2)):
        lo[k], hi[k] = (c, c + Ro) if sg > 0 else (c - Ro, c)
    kare = kutu(lo[0], hi[0], lo[1], hi[1], lo[2], hi[2])
    m = [0.0] * 3; m[i] = a0 - 1.0; m[dik[0]] = c1; m[dik[1]] = c2
    e = [0.0] * 3; e[i] = 1.0
    return kare.cut(cq.Solid.makeCylinder(Ro, a1 - a0 + 2.0, V(*m), V(*e))).clean()


def dolgu(ad, sh, tanim, tur="kaynak"):
    """köpükleme öncesi kapatılan küçük boşluk: kaynak (TIG) ya da gıda silikonu — katı olarak modellenir (PU'nun görünmediğini denetim doğrular)"""
    if tur == "kaynak":
        p = dict(ad=ad, wp=cq.Workplane("XY").add(sh), sh=sh, mal="paslanmaz", birim=BIRIM, grup="SABIT", kaynak=SURUM, tur="kaynak",
                 bom=("Kaynak dolgusu · TIG 141 · ER308LSi · %s" % tanim, 1, "", "", "ÜRETİM"), meta=dict(tur="kaynak", tip="dolgu", yontem="TIG 141"))
        G.ELEMAN.append(p)
    else:
        p = S._bp(ad, sh, "gıda sınıfı silikon (FDA 21 CFR 177.2600)", tanim, "", "VMQ silikon", birim=BIRIM, mal="conta")
        p["tur"] = "baglanti"; _eleman(p, mal="conta")
    return p


def centik(P, x0, x1, y0, y1, z0, z1, pay=0.5, tip="centik", parca=""):
    """dünya kutusunu panelin düzlemine izdüşürüp dikdörtgen kesik (kenara açık olabilir · dfm dışı) — çakışan komşu eleman için"""
    q = [P.yerel((x, y, z)) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]
    u = [a[0] for a in q]; v = [a[1] for a in q]
    u0, u1, v0, v1 = min(u) - pay, max(u) + pay, min(v) - pay, max(v) + pay
    P.kesik([(u0, v0), (u1, v0), (u1, v1), (u0, v1)], tip=tip, dfm=False, parca=parca)


# =====================================================================================================================================
# 1 · DIŞ KABUK
# =====================================================================================================================================
def _yan(taraf):
    """yan = tava: yalnız ARKA 25 mm iç dönüş (arka saca punta) · üst / alt kenar düz — tavan / taban birleşimi ayrı KÖŞEBENT parçalarıyla
    (modüler iskeletin GFRP pedleri ve dikmeleri yan sacın iç yüzüne dayalı → sürekli dönüş konamaz)"""
    s = _sac("dis_%s_yan" % taraf, "dis"); g = s.R + s.t
    if taraf == "sol":
        P = s.taban([(YDi, ZDa + g), (YDs, ZDa + g), (YDs, ZF), (YDi, ZF)], O=(X0, 0, 0), ex=(0, 1, 0), ey=(0, 0, 1), ad="yan")
        arka = P.flans(0, 25.0, yon=+1, ad="arka_donus")
    else:
        P = s.taban([(YDi, -ZF), (YDs, -ZF), (YDs, -ZDa - g), (YDi, -ZDa - g)], O=(X1, 0, 0), ex=(0, 1, 0), ey=(0, 0, -1), ad="yan")
        arka = P.flans(2, 25.0, yon=+1, ad="arka_donus")
    if taraf == "sag":
        centik(arka, 4370.0, 4392.0, 455.0, 745.0, ZDa, -826.5, pay=0.5, parca="B elektrik kutusu montaj sacı (B_ELEKTRIK, arka iç yüzde)")
    G.PANEL["yan_" + taraf] = dict(yan=P, arka=arka, s=s)
    return s


KOSEBENT = {("sol", "ust"): [(-822.0, -722.5), (-689.5, -126.5), (-93.5, 21.0)], ("sol", "alt"): [(-822.0, -722.5), (-689.5, -126.5), (-93.5, 21.0)],
            ("sag", "ust"): [(-822.0, -471.5), (-467.5, 21.0)], ("sag", "alt"): [(-822.0, -786.0), (-703.5, -563.5), (-520.5, -505.5), (-492.5, -137.5), (-94.5, 21.0)]}   # Secop rayları / conta / kondenser tavası arasında


def kosebentler():
    """1,5 L köşebent 25 × 25 (tek büküm) · yatay kol tavan / taban iç yüzüne, dik kol yan sacın iç yüzüne · ikisine de punta · parçalar GFRP pedleri /
    Secop rayları / depo sacı arasında"""
    for (tr, kn), segs in KOSEBENT.items():
        for k, (z0, z1) in enumerate(segs):
            s = _sac("kosebent_%s_%s_%d" % (tr, kn, k + 1), "dis"); g = s.R + s.t
            y0 = YDs - T_D if kn == "ust" else YDi
            if tr == "sol": u0, u1, ked = XDi + g, XDi + 25.0, 3
            else: u0, u1, ked = XDs - 25.0, XDs - g, 1
            P = s.taban([(u0, -z1), (u1, -z1), (u1, -z0), (u0, -z0)], O=(0, y0, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="yatay")
            D = P.flans(ked, 25.0, yon=-1 if kn == "ust" else +1, ad="dik")
            xs = XDi if tr == "sol" else XDs; xh = (u0 + u1) / 2.0
            yv = YDs - 12.0 if kn == "ust" else YDi + 12.0
            zz = [z for z in np.arange(z0 + 15.0, z1 - 10.0, 90.0)] or [(z0 + z1) / 2.0]
            s.punta(G.PANEL["yan_" + tr]["s"], [(xs, yv, z) for z in zz], not_="köşebent dik kolu ↔ yan sac")
            T = G.PANEL["dis_%s_%d" % ("tavan" if kn == "ust" else "taban", 1 if tr == "sol" else 2)]
            s.punta(T.sac, [(xh, YDs if kn == "ust" else YDi, z) for z in zz], not_="köşebent yatay kolu ↔ %s" % ("tavan" if kn == "ust" else "taban"))


def _duz(ad, rol, O, ex, ey, poly, t=None, mal="paslanmaz"):
    s = _sac(ad, rol, t=t, mal=mal) if t else _sac(ad, rol, mal=mal)
    P = s.taban(poly, O=O, ex=ex, ey=ey, ad="levha")
    return s, P


def dis_kabuk():
    sol = _yan("sol"); sag = _yan("sag")
    # tavan / taban / arka: iki parça (ek x 2091)
    for ad, y0 in (("dis_tavan", YDs), ("dis_taban", YB)):
        for k, (xa, xb) in enumerate(((X0, X_EK - 0.25), (X_EK + 0.25, X1))):
            s, P = _duz("%s_%d" % (ad, k + 1), "dis", (0, y0, 0), (1, 0, 0), (0, 0, -1), [(xa, -ZF), (xb, -ZF), (xb, -ZA), (xa, -ZA)])
            G.PANEL["%s_%d" % (ad, k + 1)] = P
    for k, (xa, xb) in enumerate(((X0, X_EK - 0.25), (X_EK + 0.25, X1))):
        s = _sac("dis_arka_%d" % (k + 1), "dis"); g = s.R + s.t
        P = s.taban([(xa, YDi + g), (xb, YDi + g), (xb, YDs - g), (xa, YDs - g)], O=(0, 0, ZA), ex=(1, 0, 0), ey=(0, 1, 0), ad="arka")
        b, e = (27.0, 0.0) if k == 0 else (0.0, 27.0)
        P.flans(0, 25.0, yon=+1, son=e, bas=b, ad="alt_donus")                 # kenar 0: alt (u artan) · bas = x başı
        P.flans(2, 25.0, yon=+1, bas=e, son=b, ad="ust_donus")                 # kenar 2: üst (u azalan) · bas = x sonu
        G.PANEL["dis_arka_%d" % (k + 1)] = P
        for xa_, xb_ in ARKA_YARIK:
            if xa < xa_ < xb: P.dikdortgen((xa_ + xb_) / 2.0, 763.0, xb_ - xa_, 30.0, r=3.0, tip="havalandirma", parca="ısı kalkanı hava boşluğu yarığı")
    # ek lamaları (80 · iç yüzde · punta)
    L = []
    tav_lama = []
    for k, (za, zb) in enumerate(((-803.0, -727.0), (-685.0, -131.0), (-89.0, 21.0))):     # modüler GFRP pedlerinin (−721…−691 · −125…−95) arasında 3 parça
        s, P = _duz("dis_tavan_ek_lamasi_%d" % (k + 1), "dis", (0, YDs - T_D, 0), (1, 0, 0), (0, 0, -1), [(X_EK - 40, -zb), (X_EK + 40, -zb), (X_EK + 40, -za), (X_EK - 40, -za)])
        L.append((s, G.PANEL["dis_tavan_1"], G.PANEL["dis_tavan_2"], YDs, (za, zb)))
    s, P = _duz("dis_taban_ek_lamasi", "dis", (0, YDi, 0), (1, 0, 0), (0, 0, -1), [(X_EK - 40, -(ZC0 - 2.0)), (X_EK + 40, -(ZC0 - 2.0)), (X_EK + 40, -(ZDa + 25.5)), (X_EK - 40, -(ZDa + 25.5))])
    for z0, z1 in ((-721.0, -691.0), (-125.0, -95.0)): centik(P, 2076.0, 2106.0, 124.5, 127.5, z0, z1, parca="modüler GFRP")
    L.append((s, G.PANEL["dis_taban_1"], G.PANEL["dis_taban_2"], YDi, (ZDa + 25.5, ZC0 - 2.0)))
    s, P = _duz("dis_arka_ek_lamasi", "dis", (0, 0, ZDa), (1, 0, 0), (0, 1, 0), [(X_EK - 40, YDi + 27.0), (X_EK + 40, YDi + 27.0), (X_EK + 40, YDs - 27.0), (X_EK - 40, YDs - 27.0)])
    L.append((s, G.PANEL["dis_arka_1"], G.PANEL["dis_arka_2"], None, None))
    for s, A, B, yy, zz in L:
        nok = []
        for xx in (X_EK - 22.0, X_EK + 22.0):
            if yy is not None: nok += [(xx, yy, z) for z in np.arange(zz[0] + 10.0, zz[1] - 5.0, 75.0) if not (-726 < z < -686 or -130 < z < -90 or (abs(xx - X_EK) < 30 and yy < 200 and False))]
            else: nok += [(xx, y, ZDa) for y in np.arange(170.0, 760.0, 75.0)]
        s.punta(A.sac, nok, not_="ek laması ↔ iki dış sac (alın aralığı 0,5 gıda silikonu ile dolar)")
    # dış köşe olukları (büküm dış yayı ile komşu sac arası, DIŞA açık) — köpük bu oluklara girmez (köpükleme kalıbında bant / kalıp yüzü)
    Ro = 2.25 + T_D
    for xa_, xb_ in ((X0 + 27.0, X_EK - 0.25), (X_EK + 0.25, X1 - 27.0)):
        G.DIS_OLUK.append(oluk("x", xa_, xb_, YDi + Ro, ZDa + 2.25, -1, -1, Ro))       # arka alt dönüşü (taban üstü, arka dış köşe)
        G.DIS_OLUK.append(oluk("x", xa_, xb_, YDs - Ro, ZDa + 2.25, +1, -1, Ro))       # arka üst dönüşü (tavan altı)
    G.DIS_OLUK.append(oluk("y", YDi, YDs, X0 + Ro, ZDa + Ro, -1, -1, Ro))              # sol yan arka dönüşü
    G.DIS_OLUK.append(oluk("y", YDi, YDs, X1 - Ro, ZDa + Ro, +1, -1, Ro))              # sağ yan arka dönüşü
    # arka dönüşlerinin uç payı (27 mm) ile yan arka dönüşü arasındaki köşe cebi (4 köşe) köpüklemeden önce silikonla kapanır
    for k, (xa_, xb_) in enumerate(((X0 + 24.0, X0 + 29.0), (X1 - 29.0, X1 - 24.0))):
        for m, (ya_, yb_) in enumerate(((YDi, YDi + 8.0), (YDs - 8.0, YDs))):
            kb_ = kutu(xa_, xb_, ya_, yb_, ZA, ZDa)
            G.KOSE_CEP.append(("arka_kose_silikonu_%d_%d" % (k, m), kb_))
    # ek yeri alın aralığı (0,5) köpüklemeden önce gıda sınıfı silikonla doldurulur → köpük dışarı çıkmaz, PU görünmez
    for ad, kt in (("tavan", kutu(X_EK - 0.25, X_EK + 0.25, YDs, YT, ZA, ZF)), ("taban", kutu(X_EK - 0.25, X_EK + 0.25, YB, YDi, ZA, ZF)),
                   ("arka", kutu(X_EK - 0.25, X_EK + 0.25, YDi, YDs, ZA, ZDa).fuse(kutu(X_EK - 0.25, X_EK + 0.25, YDi, YDi + T_D, ZDa, ZA + 25.0))
                    .fuse(kutu(X_EK - 0.25, X_EK + 0.25, YDs - T_D, YDs, ZDa, ZA + 25.0)).clean())):
        p_ = S._bp("ek_yeri_silikon_%s" % ad, kt, "gıda sınıfı silikon (FDA 21 CFR 177.2600)", "Ek yeri alın aralığı dolgusu 0,5 · %s" % ad, "0,5 × kalınlık", "VMQ silikon",
                   birim=BIRIM, mal="conta")
        p_["tur"] = "baglanti"; _eleman(p_, mal="conta")
    # punta: arka ↔ yan arka dönüşü (tavan / taban ↔ yan: köşebentler)
    for tr, xx in (("sol", X0 + 13.0), ("sag", X1 - 13.0)):
        Y = G.PANEL["yan_" + tr]
        i = 1 if tr == "sol" else 2
        G.PANEL["dis_arka_%d" % i].sac.punta(Y["s"], [(xx, y, ZDa) for y in np.arange(160.0, 780.0, 80.0)], not_="arka ↔ yan arka dönüşü")
    for i in (1, 2):
        xs = np.arange(800.0, X_EK - 30, 120.0) if i == 1 else np.arange(X_EK + 60, 4380.0, 120.0)
        G.PANEL["dis_arka_%d" % i].sac.punta(G.PANEL["dis_tavan_%d" % i].sac, [(x, YDs, ZDa + 12.0) for x in xs], not_="tavan ↔ arka üst dönüşü")
        G.PANEL["dis_arka_%d" % i].sac.punta(G.PANEL["dis_taban_%d" % i].sac, [(x, YDi, ZDa + 12.0) for x in xs], not_="taban ↔ arka alt dönüşü")
    # tavan / taban delikleri
    T1, T2 = G.PANEL["dis_tavan_1"], G.PANEL["dis_tavan_2"]
    for x, z in AB_DELIK: T1.delik(x, -z, 9.0, tip="vida_deligi", parca="A → B M8 (ISO 273 orta) · h3_a_sac_v1 ARAYÜZ")
    for x, z in KB_DELIK: T2.delik(x, -z, 9.0, tip="vida_deligi", parca="K → B M8 (ISO 273 orta) · h3_k_sac_v1 ARAYÜZ")
    B2 = G.PANEL["dis_taban_2"]
    for a, b in EMIS_T: B2.dikdortgen((a + b) / 2.0, 630.0, b - a, 130.0, r=3.0, tip="emis_penceresi", parca="Secop kondenser emiş penceresi")
    for x, z in SASE_M8:
        P = G.PANEL["dis_taban_1" if x < X_EK else "dis_taban_2"]
        P.delik(x, -z, 9.0, tip="vida_deligi", parca="taban ↔ alt şase M8")
        pu = S.pul("DIN9021", "M8", (x, YDi, z), (0, 1.0, 0), ad="arayuz_sase_%d_%d_pul" % (int(x), int(-z)), birim=BIRIM)
        vd = S.vida("ISO4762", "M8", 20, (x, YDi + 2.0, z), (0, -1.0, 0), ad="arayuz_sase_%d_%d" % (int(x), int(-z)), birim=BIRIM)
        _arayuz(pu, "B_MODULER alt şase boyunası (60 × 60 × 3)", "", "")
        _arayuz(vd, "B_MODULER alt şase boyunası (60 × 60 × 3)",
                "şase üst duvarında M8 perçin somun (dünya x %.0f z %.0f) · cıvata KÖPÜKLEMEDEN ÖNCE B içinden (kasa şaseyle birlikte köpüklenir)" % (x, z), "B_MODULER sahibi")


# =====================================================================================================================================
# 2 · ÖN ÇERÇEVE 430 · 1,0 (iki parça) + ek laması
# =====================================================================================================================================
def cerceve():
    for k, (xa, xb) in enumerate(((XDi, X_EK - 0.25), (X_EK + 0.25, XDs))):
        s = _sac("on_cerceve_%d" % (k + 1), "ic", t=T_C, malzeme="AISI 430 (1.4016) ferritik, 2B · manyetik fitil yüzeyi", mal="cerceve")
        P = s.taban([(xa, YDi), (xb, YDi), (xb, YDs), (xa, YDs)], O=(0, 0, ZC0), ex=(1, 0, 0), ey=(0, 1, 0), ad="cerceve")
        G.PANEL["cerceve_%d" % (k + 1)] = P
        for kk, a, b, c, d in ACIKLIK:
            if xa < a < xb: P.dikdortgen((a + b) / 2.0, (c + d) / 2.0, b - a, d - c, r=2.0, tip="cekmece_acikligi", parca="çekmece %s açıklığı" % kk)
        if k == 1:
            a, b, c, d = DEPO_ACIK; P.dikdortgen((a + b) / 2.0, (c + d) / 2.0, b - a, d - c, r=2.0, tip="depo_acikligi", parca="soğuk depo çekmecesi açıklığı")
            a, b, c, d = SERVIS_ACIK; P.kesik([(a, c), (b, c), (b, d), (a, d)], tip="servis_acikligi", dfm=False, parca="Secop servis açıklığı (alta açık · servis paneli klipsleri)")
            a, b, c, d = DEPO_TAVAN_YUVA; P.dikdortgen((a + b) / 2.0, (c + d) / 2.0, b - a + 1.0, d - c + 0.4, tip="yuva", parca="depo tavan iç sacı geçişi (B_DEPO)")
    # ek laması: B2 bölmesinin önü (2073,5–2108,5 · 164,5–728 · z 22–23)
    s = _sac("on_cerceve_ek_lamasi", "ic", t=T_C, malzeme="AISI 430 (1.4016) ferritik", mal="cerceve")
    s.taban([(BOLME[1], YF), (BOLME[1] + BW, YF), (BOLME[1] + BW, YCH), (BOLME[1], YCH)], O=(0, 0, ZC0 - T_C), ex=(1, 0, 0), ey=(0, 1, 0), ad="lama")
    s.punta(G.PANEL["cerceve_1"].sac, [(X_EK - 9.0, y, ZC0) for y in np.arange(200.0, 720.0, 80.0)] + [(X_EK + 9.0, y, ZC0) for y in np.arange(200.0, 720.0, 80.0)],
            not_="ek laması ↔ iki çerçeve yarısı (alın aralığı 0,5 · fitil yüzü düz kalır, punta izi arkada)")
    _etiket("on_cerceve_cevre_dikisi", "TIG 141 dikiş 20 / 150 + gıda silikonu", "çevre ≈ 8,7 m", "çerçeve kenarı ↔ dış kabuk iç yüzü (etek bölgesinde, kapak arkasında)")


# =====================================================================================================================================
# 3 · İÇ KABUK (gıda) · 4 · BÖLMELER + KOVANLAR · 5 · ISI KALKANI · 6 · TEKNİK
# =====================================================================================================================================
def ic_kabuk():
    for k, (xa, xb, tav) in enumerate(((797.3, X_ALCAK, YCH), (X_ALCAK, XB5b, YCL))):
        s = _sac("ic_taban_%d" % (k + 1), "ic", R=R_GIDA, bolge="gida"); g = s.R + s.t
        u0 = xa
        P = s.taban([(u0, -ZC0), (xb, -ZC0), (xb, -(ZB - T_I)), (u0, -(ZB - T_I))], O=(0, YF - T_I, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="taban")
        on = None                                                          # ön kenar çerçeveye alın (büküm yok: büküm dış yayı çerçeve köşesinde boşluk bırakırdı)
        # arka duvar AYRI düz sac (iç tabanın üstünde): B_KABLO dikey kanalları ve ray arka braketleri köşeye dik oturuyor → bükümlü R3 köşe onlara girerdi
        a_ = _sac("ic_arka_%d" % (k + 1), "ic", R=R_GIDA, bolge="gida")
        arka = a_.taban([(xa, YF), (xb, YF), (xb, tav), (xa, tav)], O=(0, 0, ZB - T_I), ex=(1, 0, 0), ey=(0, 1, 0), ad="arka")
        d = dict(taban=P, on=on, arka=arka, s=s)
        if k == 0:
            w = _sac("ic_sol_duvar", "ic", R=R_GIDA, bolge="gida"); gw = w.R + w.t
            W_ = w.taban([(YF, -ZC0), (YCH, -ZC0), (YCH, -ZB), (YF, -ZB)], O=(XL, 0, 0), ex=(0, 1, 0), ey=(0, 0, -1), ad="duvar")
            d["sol"] = W_
        G.PANEL["ic_taban_%d" % (k + 1)] = d
        t = _sac("ic_tavan_%d" % (k + 1), "ic", R=R_GIDA, bolge="gida"); gt = t.R + t.t
        Q = t.taban([(xa, -ZC0), (xb, -ZC0), (xb, -(ZB - T_I)), (xa, -(ZB - T_I))], O=(0, tav, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="tavan")
        G.PANEL["ic_tavan_%d" % (k + 1)] = dict(tavan=Q, s=t)
        # gömülü dikmeler (modüler / taşıyıcı · bölmelerin PU'sunda) iç taban ve tavandan geçer → 31 × 31 delik (bölmenin altında, gıda bölgesi dışında)
        for g_ in GOMULU:
            if "dikme" not in g_[0]: continue
            x0_, x1_, y0_, y1_, z0_, z1_ = g_[1:]
            if not (xa < x0_ and x1_ < xb): continue
            if y0_ < YF - T_I and y1_ > YF:
                q = P.yerel(((x0_ + x1_) / 2.0, YF - T_I, (z0_ + z1_) / 2.0)); P.dikdortgen(q[0], q[1], x1_ - x0_ + 1.0, z1_ - z0_ + 1.0, tip="dikme_gecisi", dfm=False, parca="%s geçişi" % g_[0])
            if y0_ < tav and y1_ > tav + T_I:
                q = Q.yerel(((x0_ + x1_) / 2.0, tav, (z0_ + z1_) / 2.0)); Q.dikdortgen(q[0], q[1], x1_ - x0_ + 1.0, z1_ - z0_ + 1.0, tip="dikme_gecisi", dfm=False, parca="%s geçişi" % g_[0])
        _etiket("ic_tavan_%d_kose_dikisi" % (k + 1), "TIG 141 sürekli + R3 taşlama (gıda)", "%.0f + %.0f mm" % (xb - xa, 814.2), "iç tavan ↔ arka duvar / sol duvar üst köşesi (iç köşe)")
    _etiket("ic_arka_taban_kose_dikisi", "TIG 141 sürekli + taşlama (gıda, iç köşe)", "3230 mm", "iç arka duvar ↔ iç taban (arka alt köşe)")
    _etiket("ic_taban_ek_dikisi", "TIG 141 sürekli + taşlama (gıda)", "814 mm", "iç taban 1 ↔ 2 alın birleşimi x 2108,5 (K3 sol iç köşesi, B2 sacı b ile aynı dikiş)")
    _etiket("ic_sol_duvar_koseleri", "TIG 141 sürekli + R3 taşlama (gıda)", "814 + 564 + 814 mm", "sol duvar ↔ iç taban / arka duvar / iç tavan iç köşeleri")


def _gecisler(i):
    x = BOLME[i]; tav = YCH if i <= 1 else YCL
    hv = [(y0, y1, HAVA_Z[0], HAVA_Z[1]) for y0, y1 in HAVA.get(i, [])]
    if i == 4: hv += [(y0, y1, DEPO_HAVA_Z[0], DEPO_HAVA_Z[1]) for y0, y1 in DEPO_HAVA]
    kn = [(max(c, YF), min(d, tav), KAN_Z[0], KAN_Z[1]) for a, b, c, d in KANAL if a < x + BW and b > x and c < tav and d > YF]
    gec = [list(g) for g in hv + kn]
    birlesti = True
    while birlesti:
        birlesti = False
        for a_ in range(len(gec)):
            for b_ in range(a_ + 1, len(gec)):
                u, v = gec[a_], gec[b_]
                if u[0] < v[1] + 2 * T_I and v[0] < u[1] + 2 * T_I and u[2] < v[3] + 2 * T_I and v[2] < u[3] + 2 * T_I:
                    gec[a_] = [min(u[0], v[0]), max(u[1], v[1]), min(u[2], v[2]), max(u[3], v[3])]; gec.pop(b_); birlesti = True; break
            if birlesti: break
    out = []
    for y0, y1, z0, z1 in gec:
        y0, y1, z1 = y0 - 1.0, min(y1 + 1.0, tav), z1 + 1.0                      # kanal / hava geçişine 1 mm boşluk (büküm iç R'si kanal köşesine girmesin)
        if z0 > ZB + 1e-6: z0 -= 1.0
        out.append(dict(ic=(y0, y1, z0, z1), dis=(max(y0 - T_I, YF), min(y1 + T_I, tav), max(z0 - T_I, ZB), min(z1 + T_I, ZC0)), arka_acik=z0 <= ZB + 1e-6,
                        ust_tavan=y1 + T_I > tav - 1e-6))
    return out


def kovan(ad, x, gc):
    """U kovan (1,2): ön duvar + alt / üst duvar arkaya (arka iç yüze kadar) · üst duvar tavan iç sacına denk geliyorsa L · arka kapalı geçişte arka kapama"""
    y0d, y1d, z0d, z1d = gc["dis"]; y0, y1, z0, z1 = gc["ic"]
    s = _sac(ad, "ic"); g = s.R + s.t
    if gc["arka_acik"]:                                                    # U (arka iç sac kapatır) ya da L (üstü iç tavan)
        ua = y0d + g; ub = (y1d - g) if not gc["ust_tavan"] else y1d
        P = s.taban([(x, ua), (x + BW, ua), (x + BW, ub), (x, ub)], O=(0, 0, z1), ex=(1, 0, 0), ey=(0, 1, 0), ad="on")
        boy = (z1 + T_I) - ZB
        P.flans(0, boy, yon=-1, ad="alt")
        if not gc["ust_tavan"]: P.flans(2, boy, yon=-1, ad="ust")
    else:                                                                  # kapalı dikdörtgen kovan = iki L (abkant: derin dar U bükülemez) · iki boyuna TIG
        P = s.taban([(x, y0d + g), (x + BW, y0d + g), (x + BW, y1d - T_I), (x, y1d - T_I)], O=(0, 0, z1), ex=(1, 0, 0), ey=(0, 1, 0), ad="on")
        P.flans(0, (z1 + T_I) - z0d, yon=-1, ad="alt")
        k = _sac(ad + "_ust_L", "ic"); gk = k.R + k.t
        Q = k.taban([(x, y0d + T_I), (x + BW, y0d + T_I), (x + BW, y1d - gk), (x, y1d - gk)], O=(0, 0, z0d), ex=(1, 0, 0), ey=(0, 1, 0), ad="arka")
        Q.flans(2, (z1 + T_I) - z0d, yon=+1, ad="ust")
        _etiket(ad + "_boyuna_dikis", "TIG 141", "2 × 35 mm", "iki L kovan yarısı (köpük sızdırmaz)")
    _etiket(ad + "_dikisi", "TIG 141 (köpük sızdırmaz)", "2 × çevre", "kovan ↔ bölme sacları a / b deliği çevresi")
    return s


def bolmeler():
    G.PANEL["bolme"] = {}
    for i in range(5):
        x = BOLME[i]; tav = YCH if i <= 1 else YCL
        zon = ZC0 - (T_C if i == 1 else 0.0)                                   # B2: çerçeve ek laması önde
        gecs = _gecisler(i)
        ps = {}
        for yan in ("a", "b"):
            if i == 4 and yan == "b": continue
            s = _sac("bolme_%d_sac_%s" % (i + 1, yan), "ic", R=R_GIDA, bolge="gida"); g = s.R + s.t
            if yan == "a":
                P = s.taban([(YF, ZB), (tav, ZB), (tav, zon), (YF, zon)], O=(x, 0, 0), ex=(0, 1, 0), ey=(0, 0, 1), ad="sac")
            else:
                P = s.taban([(YF, -zon), (tav, -zon), (tav, -ZB), (YF, -ZB)], O=(x + BW, 0, 0), ex=(0, 1, 0), ey=(0, 0, -1), ad="sac")
            for gc in gecs:
                y0d, y1d, z0d, z1d = gc["dis"]
                centik(P, x - 1, x + BW + 1, y0d, y1d, z0d, z1d, pay=0.0, tip="kovan_deligi", parca="hava / kablo kanalı kovanı")
            if i >= 1:
                c = gider_noktasi(x + (0.6 if yan == "a" else BW - 0.6))
                q = P.yerel(tuple(c)); rr = GID_R + 0.2
                if c[1] - rr - YF < 3.0:                                             # B5: kılıf sacın alt kenarına 2 mm → alta açık U çentik
                    sg = 1.0 if yan == "a" else -1.0
                    pts = [(YF - 1.0, q[1] - rr), (q[0], q[1] - rr)] + [(q[0] + rr * math.sin(math.pi * k / 16.0), q[1] - rr * math.cos(math.pi * k / 16.0)) for k in range(1, 16)] +                           [(q[0], q[1] + rr), (YF - 1.0, q[1] + rr)]
                    P.kesik(pts, tip="gider_centigi", dfm=False, parca="gider kılıfı Ø24 · alta açık U çentik (kılıf sacın alt kenarına 2 mm)")
                else:
                    P.delik(q[0], q[1], 2 * rr, tip="gider_deligi", parca="gider kılıfı Ø24 (B_SOGUTMA)")
            ps[yan] = P
            _etiket("bolme_%d_sac_%s_koseleri" % (i + 1, yan), "TIG 141 sürekli + R3 taşlama (gıda)", "%.0f + %.0f + %.0f mm" % (814.0, tav - YF, 814.0),
                    "bölme sacı ↔ iç taban / iç tavan / arka duvar iç köşeleri")
        G.PANEL["bolme"][i] = ps
        duz = [(x, x + T_I), (x + BW - T_I, x + BW)] if i < 4 else [(x, x + T_I), (XB5b, T0)]       # kovanın geçtiği sac düzlemleri
        for j, gc in enumerate(gecs):
            kovan("bolme_%d_kovan_%d" % (i + 1, j), x, gc)
            y0d, y1d, z0d, z1d = gc["dis"]; z1 = gc["ic"][3]; Ro = 1.8 + T_I
            kos = [(y0d + Ro, z1 - 1.8, -1, +1)]                                          # ön-alt büküm (U / L / kapalı L1)
            if gc["arka_acik"] and not gc["ust_tavan"]: kos.append((y1d - Ro, z1 - 1.8, +1, +1))   # U ön-üst
            if not gc["arka_acik"]: kos.append((y1d - Ro, z0d + Ro, +1, -1))                # kapalı: L2 arka-üst
            for k, (cy, cz, sy, sz) in enumerate(kos):
                for m, (xa_, xb_) in enumerate(duz):
                    dolgu("bolme_%d_kovan_%d_kose_kaynagi_%d_%d" % (i + 1, j, k, m), oluk("x", xa_, xb_, cy, cz, sy, sz, Ro), "kovan büküm köşesi ↔ sac deliği köşesi (çevre dikişinin parçası)")
        if i >= 1:
            for m, (xa_, xb_) in enumerate(duz if i == 4 else duz):
                c = gider_noktasi((xa_ + xb_) / 2.0); e = np.array(GID_B) - np.array(GID_A); e = e / np.linalg.norm(e)
                p0 = c - e * (T_I / 2.0 + 0.05) * (1.0 / e[0]); L = (T_I + 0.1) / e[0]
                halka = cq.Solid.makeCylinder(GID_R + 0.2, L, V(*p0), V(*e)).cut(cq.Solid.makeCylinder(GID_R, L + 2.0, V(*(p0 - e)), V(*e)))
                if c[1] - (GID_R + 0.2) - YF < 3.0 and (xa_, xb_) == (x, x + T_I):                # B5 alta açık çentik: çentik ağzı da silikonla
                    halka = halka.fuse(kutu(xa_, xb_, YF, c[1], c[2] - GID_R - 0.2, c[2] + GID_R + 0.2).cut(cq.Solid.makeCylinder(GID_R, L + 2.0, V(*(p0 - e)), V(*e)))).clean()
                dolgu("bolme_%d_gider_silikonu_%d" % (i + 1, m), halka, "gider kılıfı ↔ sac deliği silikon halkası", tur="silikon")
    # teknik sütun kapama sacı (B5 teknik tarafı)
    s = _sac("teknik_sol_duvar", "ic", R=R_GIDA); g = s.R + s.t
    P = s.taban([(YDi, -ZC0), (YDs, -ZC0), (YDs, -ZDa), (YDi, -ZDa)], O=(T0, 0, 0), ex=(0, 1, 0), ey=(0, 0, -1), ad="duvar")   # düz (ön kenar çerçeveye dayanır · iç taban / tavan ön dönüşleri burada biter)
    for gc in _gecisler(4):
        y0d, y1d, z0d, z1d = gc["dis"]
        centik(P, XB5b - 1, T0 + 1, y0d, y1d, z0d, z1d, pay=0.0, tip="kovan_deligi", parca="B5 geçişi (depo havası / kablo kanalı)")
    c = gider_noktasi(XB5b + 0.6); q = P.yerel(tuple(c)); P.delik(q[0], q[1], 2 * GID_R + 0.4, tip="gider_deligi", parca="gider kılıfı Ø24")
    arka_donus_kesigi(P, XB5b + 0.6, ust=True); arka_donus_kesigi(P, XB5b + 0.6, ust=False)
    G.PANEL["teknik_sol_duvar"] = P
    # B5 kovanları teknik duvarına kadar uzar (arka kapalı depo havası): kovan boyu B5 (35) + teknik duvar 1,2 → kovan() 35 ile kurulur; teknik duvar deliği kovanın ucunu karşılar


def raylar():
    """çekmece rayları: her sabit ray başına 3 × PEM SP-M5 (bölme / sol duvar sacında, gövde PU tarafında) · DIN 7991 M5 havşa vida ray gövdesinden (ARAYÜZ)"""
    RAY = [(798.5, y) for y in (204.5, 312.5, 420.5, 528.5, 636.5)] + [(1418.5, y) for y in (204.5, 312.5, 420.5, 528.5, 636.5)] + \
          [(1453.5, y) for y in (204.5, 312.5, 420.5, 528.5, 636.5)] + [(2073.5, y) for y in (204.5, 312.5, 420.5, 528.5, 636.5)] + \
          [(2108.5, y) for y in (204.5, 312.5, 420.5, 528.5)] + [(2728.5, y) for y in (204.5, 312.5, 420.5, 528.5)] + \
          [(2763.5, y) for y in (204.5, 312.5, 420.5, 528.5)] + [(3383.5, y) for y in (204.5, 312.5, 420.5, 528.5)] + \
          [(3418.5, y) for y in (204.5, 312.5, 475.5)] + [(3993.5, y) for y in (204.5, 312.5, 475.5)]
    n = 0
    for xw, ylo in RAY:
        yc = ylo + 22.85
        if xw == XL: P = G.PANEL["ic_taban_1"]["sol"]; xs, ex = XL - T_I, -1.0
        else:
            i = [k for k in range(5) if abs(BOLME[k] - xw) < 0.1 or abs(BOLME[k] + BW - xw) < 0.1][0]
            yan = "a" if abs(BOLME[i] - xw) < 0.1 else "b"
            P = G.PANEL["bolme"][i][yan]; xs, ex = (xw + T_I, 1.0) if yan == "a" else (xw - T_I, -1.0)
        for z in (-580.0, -330.0, -45.0):                                     # dikmeler (z −635…−605 · −125…−95 · −721…−691) bölme içinde → uzak
            ps, c, ms = S.pem_somun("SP", "M5", (xs, yc, z), (ex, 0, 0), T_I, ad="ray_pem_%d_%d_%d" % (int(xw), int(ylo), int(-z)), birim=BIRIM)
            q = P.yerel((xs, yc, z)); P.delik(q[0], q[1], c["delik"], tip="pem_somun", parca=ps["meta"]["parca"], pem_tip="SP", kenar_min=c["kenar"], min_sac=ms)
            _eleman(ps)
            # köpük kapağı (PE, geçme): PEM gövdesini ve diş deliğini köpükten korur (köpük dişe girerse ray vidası takılamaz)
            e = np.array([ex, 0.0, 0.0]); p0 = np.array([xs, yc, z]); Lb = ps["meta"]["T"] - ps["meta"]["sap"]
            cup = cq.Solid.makeCylinder(c["E"] / 2.0 + 0.8, Lb + 0.8, V(*p0), V(*e)).cut(cq.Solid.makeCylinder(c["E"] / 2.0, Lb, V(*p0), V(*e)))
            kp = S._bp("ray_pem_%d_%d_%d_kopuk_kapagi" % (int(xw), int(ylo), int(-z)), cup, "PE geçme kapak (katalog: PEM / Kalei köpük kapağı)",
                       "Köpük kapağı PEM SP-M5 için · Ø%.1f × %.1f · köpüklemeden önce takılır" % (c["E"] + 1.6, Lb + 0.8), "Ø%.1f × %.1f" % (c["E"] + 1.6, Lb + 0.8), "PE-LD",
                       birim=BIRIM, mal="conta")
            kp["tur"] = "baglanti"; _eleman(kp, mal="conta")
            G.PU_KES.append(cq.Solid.makeCylinder(c["E"] / 2.0 + 0.8, Lb + 0.8, V(*p0), V(*e)))          # kapak içi (diş deliği) köpüksüz
            vd = S.vida("DIN7991", "M5", 10, (xw - ex * 3.0, yc, z), (ex, 0, 0), ad="arayuz_ray_%d_%d_%d" % (int(xw), int(ylo), int(-z)), birim=BIRIM)
            _arayuz(vd, "CEK sabit ray gövdesi (dünya x %.1f · y %.1f–%.1f)" % (xw, ylo, ylo + 45.7), "ray gövdesinde Ø5,5 + 90° havşa (3 adet, z −580 / −330 / −45) · DIN 7991 M5 × 10 A2", "çekmece / ray sahibi")
            n += 1
    G.NOT.append("ray bağlantısı: %d PEM SP-M5 (1,2 sac, kod 1) · PEM gövdesi PU tarafında → köpüklemeden önce PE köpük kapağı (sipariş: PEM SP-M5-1 + köpük kapağı ya da kapalı uçlu muadil)" % n)


def isi_kalkani():
    s = _sac("isi_kalkani_u", "ic"); g = s.R + s.t
    P = s.taban([(XFIR + g, -ZC0), (XB5b - 32.6 - g, -ZC0), (XB5b - 32.6 - g, -ZDa), (XFIR + g, -ZDa)], O=(0, YCH, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="ayirma")
    sol = P.flans(3, YDs - YCH, yon=+1, ad="sol_yan")
    sag = P.flans(1, YDs - YCH, yon=+1, ad="sag_yan")
    for x0, x1, y0, y1, z0, z1 in [(2502.5, 4026.0, 746.5, 786.5, -640.0, -600.0), (2731.0, 4026.0, 746.5, 786.5, -130.0, -90.0)]:
        centik(sag, x0, x1, y0, y1, z0, z1, pay=0.5, parca="taşıyıcı kiriş geçişi (üstten açık çentik)")
    arka_donus_kesigi(sol, XFIR + 0.6, ust=True); arka_donus_kesigi(sag, 3994.1, ust=True)
    centik(sol, 2490.0, 2510.0, 753.5, YDs, -125.0, -95.0, pay=0.5, parca="modüler ön üst kiriş + GFRP pedi geçişi (üstten açık çentik)")
    for x in (2746.0, 3401.0):
        for z in (-110.0, -620.0):
            q = P.yerel((x, YCH, z)); P.dikdortgen(q[0], q[1], 31.0, 31.0, tip="dikme_gecisi", parca="taşıyıcı dikme 30 × 30 geçişi")
    G.PANEL["isi_kalkani"] = P
    Ru = s.R + s.t
    G.PU_EK.append(("pu_isi_kalkani_kose_sol", oluk("z", ZDa, ZC0, XFIR + Ru, YCH + Ru, -1, -1, Ru)))           # U dış köşesi (PU tarafında) köpükle dolar
    G.PU_EK.append(("pu_isi_kalkani_kose_sag", oluk("z", ZDa, ZC0, 3994.7 - Ru, YCH + Ru, +1, -1, Ru)))
    i = _sac("isi_kalkani_isinim_08", "ic", t=T_ISIN, malzeme="AISI 304 BA (parlak tavlı) 0,8 — ışınım yansıtıcı")
    Q = i.taban([(XFIR + 2.2, -(ZC0 - 2.0)), (3992.5, -(ZC0 - 2.0)), (3992.5, -(ZDa + 2.0)), (XFIR + 2.2, -(ZDa + 2.0))], O=(0, 740.0, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="isinim")
    for x in (2746.0, 3401.0):
        for z in (-110.0, -620.0):
            q = Q.yerel((x, 740.0, z)); Q.dikdortgen(q[0], q[1], 31.0, 31.0, tip="dikme_gecisi", parca="taşıyıcı dikme geçişi")
    for k, (x, z) in enumerate(TAKOZ_XZ):
        sh = kutu(x - 10.0, x + 10.0, YCH + T_I, 740.0, z - 10.0, z + 10.0)
        p = S._bp("isi_kalkani_takozu_%d" % k, sh, "PTFE cam elyaf takviyeli (260 °C)", "Isı kalkanı takozu 20 × 20 × 10,8 · yüksek sıcaklık silikonla ayırma sacına", "20 × 20 × 10,8",
                  "PTFE + %25 cam elyaf", birim=BIRIM, mal="koyu")
        p["tur"] = "baglanti"; _eleman(p, mal="koyu")
    i.punta(s, [], not_="(punta yok) ışınım sacı takozlara oturur, 12 × Ø4 kör perçin ile takoza; ayırma sacına temas yok (ışınım boşluğu)")
    _etiket("isi_kalkani_u_cevre", "TIG 141 dikiş 20 / 150", "2 × 58,5 mm × 2", "ısı kalkanı U yanları ↔ dış tavan iç yüzü yok (yalnız dayanır); ön kenar çerçeveye punta")


def teknik():
    _duz("tk_ara_arka_sac", "ic", (0, 0, -494.0 - T_I), (1, 0, 0), (0, 1, 0), [(T0, 433.5), (XDs, 433.5), (XDs, 463.5), (T0, 463.5)])


# =====================================================================================================================================
# 7 · PU
# =====================================================================================================================================
def pu_bloklari():
    saclar = [s.kati() for s in G.SAC]
    sb = [x.BoundingBox() for x in saclar]
    gom = [kutu(*g[1:]) for g in GOMULU]
    gid = gider_silindiri()
    for i in range(5):
        x = BOLME[i]; x1_ = (T0 + 1.0) if i == 4 else (x + BW + 1.0)
        for gc in _gecisler(i):
            y0, y1, z0, z1 = gc["ic"]
            gom.append(kutu(x - 1.0, x1_, y0, y1, z0 if not gc["arka_acik"] else ZB, z1))      # geçişin içi hava / kanal (köpük girmez)
    out = []
    for ad, x0, x1, y0, y1, z0, z1 in PU_BOLGE:
        b = kutu(x0, x1, y0, y1, z0, z1); bb = b.BoundingBox()
        cut = [s for s, q in zip(saclar, sb) if q.xmin < bb.xmax and bb.xmin < q.xmax and q.ymin < bb.ymax and bb.ymin < q.ymax and q.zmin < bb.zmax and bb.zmin < q.zmax]
        cut += [g for g in gom if g.BoundingBox().xmin < bb.xmax and bb.xmin < g.BoundingBox().xmax and g.BoundingBox().ymin < bb.ymax and bb.ymin < g.BoundingBox().ymax
                and g.BoundingBox().zmin < bb.zmax and bb.zmin < g.BoundingBox().zmax]
        cut += [p["sh"] for p in G.ELEMAN + G.ARAYUZ if p.get("sh") is not None and _ic(p["sh"].BoundingBox(), bb)]
        cut += [k for k in G.PU_KES + G.DIS_OLUK if _ic(k.BoundingBox(), bb)]
        cut.append(gid)
        sh = b.cut(*cut).clean() if cut else b
        for k, so in enumerate(sh.Solids() if hasattr(sh, "Solids") else [sh]):
            if so.Volume() < 20.0: continue                                     # < 20 mm³ ara boşluk (pul deliği / cıvata çevresi): köpük girmez
            nm = ad if len(sh.Solids()) == 1 else "%s_%d" % (ad, k)
            out.append(dict(ad=nm, wp=cq.Workplane("XY").add(so), sh=so, mal="pu", birim=BIRIM, grup="SABIT", kaynak=SURUM, tur="pu",
                            bom=("Yerinde köpük PU 40 kg/m³ (λ 0,022) · %s" % ad, 1, "%.1f dm³" % (so.Volume() / 1e6), "kalıp = kasa (enjeksiyon)", "ÜRETİM"),
                            meta=dict(tur="pu", hacim_dm3=round(so.Volume() / 1e6, 3))))
    for ad, sh in G.PU_EK:
        bb = sh.BoundingBox()
        cut = [s for s in saclar if _ic(s.BoundingBox(), bb)]
        so = sh.cut(*cut).clean() if cut else sh
        for k, q in enumerate(so.Solids()):
            if q.Volume() < 0.01: continue
            out.append(dict(ad="%s_%d" % (ad, k), wp=cq.Workplane("XY").add(q), sh=q, mal="pu", birim=BIRIM, grup="SABIT", kaynak=SURUM, tur="pu",
                            bom=("Yerinde köpük PU · %s" % ad, 1, "%.2f cm³" % (q.Volume() / 1e3), "", "ÜRETİM"), meta=dict(tur="pu")))
    G.PU = out
    return out


def _ic(a, b):
    return a.xmin < b.xmax and b.xmin < a.xmax and a.ymin < b.ymax and b.ymin < a.ymax and a.zmin < b.zmax and b.zmin < a.zmax


# =====================================================================================================================================
def kur(log=print):
    if G.kuruldu: return G
    t0 = time.time()
    for a in ("SAC", "ELEMAN", "KAYNAK", "BIRLESIM", "ARAYUZ", "PU", "KAYNAK_ETIKET", "NOT", "PU_KES", "DIS_OLUK", "PU_EK", "KOSE_CEP"): setattr(G, a, [])
    G.PANEL = {}
    dis_kabuk(); kosebentler(); cerceve(); ic_kabuk(); bolmeler(); raylar(); isi_kalkani(); teknik()
    saclar = [x.kati() for x in G.SAC]
    for ad, kb_ in G.KOSE_CEP:
        bb = kb_.BoundingBox(); cut = [x for x in saclar if _ic(x.BoundingBox(), bb)] + [o for o in G.DIS_OLUK if _ic(o.BoundingBox(), bb)]
        q = kb_.cut(*cut).clean() if cut else kb_
        if q.Volume() > 0.01: dolgu(ad, q, "arka dönüş uç payı ↔ yan arka dönüşü köşe cebi", tur="silikon")
    pu_bloklari()
    G.PROFIL = []
    G.kuruldu = True
    log("%s · kuruldu: %d sac · %d PU · %d eleman · %d kaynak etiketi · %d arayüz · %.1f sn" % (SURUM, len(G.SAC), len(G.PU), len(G.ELEMAN), len(G.KAYNAK_ETIKET),
                                                                                         len(G.ARAYUZ), time.time() - t0))
    return G


def _mal(p):
    if p.get("tur") == "pu": return "pu"
    if p.get("tur") == "sac":
        if p["ad"].startswith("on_cerceve"): return "on_cerceve"
        return "kabuk" if p["ad"].startswith("dis_") else "sac"
    if p.get("tur") == "kaynak": return "sac"
    return p.get("mal") if p.get("mal") in ("celik", "conta", "siyah", "sac", "kabuk", "koyu") else "celik"


def govde_parcalari():
    kur()
    L = []
    for s in G.SAC: L += s.parcalar()
    L += G.ELEMAN + G.PU
    out = []
    for p in L:
        sh = p.get("sh") if p.get("sh") is not None else p["wp"].val()
        q = dict(ad=p["ad"], wp=cq.Workplane("XY").add(sh), sh=sh, mal=_mal(p), grup="SABIT", bom=tuple(p["bom"]) if p.get("bom") else None, kaynak=SURUM,
                 birim=BIRIM, tur=p.get("tur", "sac"))
        if p.get("sac"): q["sac"] = p["sac"]
        if p.get("meta"): q["meta"] = p["meta"]
        out.append(q)
    adlar = [q["ad"] for q in out]
    assert len(adlar) == len(set(adlar)), "çift ad: %s" % sorted(a for a in set(adlar) if adlar.count(a) > 1)
    return out


ZARF = (X0, X1, YB, YT, ZA, ZF)


def dunya_listesi(L):
    out = []
    for p in L:
        q = dict(p); s = p.get("sh") if p.get("sh") is not None else p["wp"].val()
        q["sh"] = s; q["wp"] = cq.Workplane("XY").add(s); out.append(q)
    return out


if __name__ == "__main__":
    kur()
    L = govde_parcalari()
    print(len(L), "parça")
    sys.stdout.flush(); os._exit(0)
