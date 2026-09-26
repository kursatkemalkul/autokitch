# -*- coding: utf-8 -*-
"""AKTARMA İTİCİSİ v2 · itici_cad_v2 · 26 Eyl 2026 gece (v1 + montaj v49 bulguları: makara/kaldırma pimi −w tarafına, link 26 geniş simetrik)
v1 (Kemal: "itici tasarımını yap")
Görev: TOPPING tablası aktarma konumundayken (disk merkezi x 2337, z −170) pideyi (Ø280–300, 28 mm) diskten fırının ön odasındaki
giriş bandına, fırın bandının eksenine (z −249) iter: tek ÇAPRAZ hareket (+170 x, −79 z = 187,5 mm, 24,9°). Pide diskte kaydırılmaz;
diyagonal itmede arkada kalan kısmı DESTEK PLAKASI (y 1167, diskin arka kenarının gerisi) taşır.
Neden çapraz: fırın tüneli ön duvara 20 mm boşluk ister (ürün −249), tabla ekseni −170 (TOPPING nozülleri). Kaydırma disk üstünde olamaz
(Ø340 disk, Ø300 pide → 20 mm pay), fırın öne alınamaz (ön yüz), TOPPING arkaya alınamaz. Tek eksen + çapraz = en az parça.
Neden kaldırma: iticinin ev konumu pidenin geliş koridorunun (z −320…−20) içinde; tabla gelirken çubuk yukarıda olmalı → çubuk
pivotlu; dönüşün son 17,5 mm'sinde link'teki makara SABİT KALDIRMA PİMİNE dayanır, çubuk 90° kalkar (ek eyleyici yok, hortum yok);
ileri giderken yerçekimiyle iner, dayama pimi dik tutar. (Kalem silindirli sürüm koridora iniyordu → kaldırıldı.)
KATALOG: SMC MY1B16-250 kolsuz silindir (ölçüler föy 8-11-22: NW 37 · NE 27,8 · H 37 · L 80 · LW 30 · Z 160 + strok) · pimler ISO 8734
(4 m6 × 30 pivot · 3 m6 × 26 dayama · 3 m6 × 14 makara · 8 m6 × 70 kaldırma) · igus GFM-0405-20 burç · D-M9BL anahtar ×2 · AS1201F-M5-06 ×2 · KQ2H06-M5 ×2.
KOORDİNAT: dünya (x hat, y zemin, z ön 0 / arka −). Yerel (s, y, w): s itme yönü u, w ona dik (sağ-ön) v; başlangıç Pc = pide
kenarına temas noktası. Parçalar yerelde kurulur, Y ekseninde +THETA döndürülüp Pc'ye taşınır.
GRUPLAR: SABIT · ARABA (kızak tablası + pivot braketi + pimler) · KOL (ARABA'nın çocuğu: link + çubuk + makara, pivot etrafında döner)."""
import math, os, sys, time
import cadquery as cq

V = cq.Vector
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "otonom", "hat3d")

# ================================================================ ÖLÇÜLER (dünya)
C0 = (2337.0, -170.0)                         # pide merkezi: tabla aktarma konumu (x, z)
C1 = (2507.0, -249.0)                         # pide merkezi: itme sonu = disk kenarı; pidenin ön 89 mm'si fırın bandında (2568+), ortası giriş bandında (2505–2569), eksen −249
R_PIDE = 150.0                                # Ø300 (en büyük)
DISK_UST, PIDE_UST, TOP_UST = 1168.0, 1196.0, 1201.0      # disk üstü · pide üstü · topping üstü (kaşar katmanı)
TAVAN = 1277.0                                # soğuk oda yalıtımının alt yüzü (montaj düzlemi)
KORIDOR_Z = (-320.0, -20.0)                   # pidenin x boyunca geliş koridoru (z) — bu koridorda 1210'un altında sabit parça olamaz
Y_SERBEST = 1210.0                            # gelen pidenin (topping 1201) üstünde bırakılan boşluk çizgisi
dx, dz = C1[0] - C0[0], C1[1] - C0[1]
L_ITME = math.hypot(dx, dz)                   # 217,8
U = (dx / L_ITME, dz / L_ITME)                # (0,932, −0,363)
W = (-U[1], U[0])                             # (0,363, 0,932) — sağa-öne
THETA = math.degrees(math.atan2(-U[1], U[0])) # 21,27° (Y ekseninde döndürme açısı)
PC = (C0[0] - R_PIDE * U[0], C0[1] - R_PIDE * U[1])       # (2197,2 · −115,6) çubuk yüzünün pideye değdiği nokta (s = 0)
S_TEMAS = -20.0                               # makaranın kaldırma pimine değdiği çubuk-yüzü konumu (pideye 20 kala çubuk iner)
S_HOME, S_END = S_TEMAS - 17.5, L_ITME + 15.0 # çubuk yüzü: ev (−37,5: kalkık) · son (pide 15 mm daha ileri: bantlar tuttu)
W_AXIS = -42.0                                # kolsuz silindir ekseni, çubuk yüzü çizgisinin 42 mm gerisi (kaşar/sucuk iniş boruları arasından ≥ 4 mm payla geçer)
STROK = 250.0                                 # MY1B16-250
S_STROK0 = S_HOME - 5.0                       # tabla strok aralığı [−42,5, 207,5] ⊇ [S_HOME, S_END] (240 gerekli, 10 pay)
# SMC MY1B16 (föy 8-11-22)
MY = dict(NW=37.0, NE=27.8, H=37.0, L=80.0, LW=30.0, Z=160.0, PA=40.0, PB=20.0)
# çubuk (bar) · link · pivot
BAR_W0, BAR_W1 = -90.0, 80.0                  # çubuk w aralığı (170 boy) — link w −40'ta (eksen), çubuk asimetrik; ön ucu ön yüze 18 mm kala biter
BAR_Y0, BAR_Y1 = 1170.0, 1200.0               # çubuk yüzü kotları (diskin 2 mm üstünden pide üstüne)
LINK_W = 20.0                                 # link genişliği (w)
Y_TABLA_YUZ = TAVAN - 6.0 - MY["H"]           # 1234 · kızak tablası alt yüzü (kiriş 6 + H 37)
PIVOT_Y = 1224.0                              # pivot ekseni (w yönünde), taban plakasının 7 altı; çatal kulakları 1219'a iner
MAKARA = dict(s=-7.5, y=1214.0, r=4.0, w=-37.0)  # v2: POM makara Ø8 × 8: link'in −s yüzünde, −w'de (w = wa−37 = −79: gövdenin/tablanın dışında, sucuk borusunun gerisinde); altı 1210
PIM_KALDIRMA_S = S_TEMAS - 7.5 - 4.0 - 4.0    # sabit kaldırma pimi (Ø8) ekseni: makaraya temas S_TEMAS'ta · w = wa + MAKARA['w']
STOP_S = -4.55                                # dayama pimi Ø3: link dik dururken arkasına (−s) dayanır (0,05 boşluk)

PARCALAR = []
BIRIMLER = [("C_ITICI", "Aktarma iticisi (bizim) · SMC MY1B16-250 kolsuz silindir çapraz (24,9°) · pivotlu çubuk 170 × 30, dönüşte sabit pime rolan makarayla 90° kalkar · pideyi diskten giriş bandına iter (187,5 mm: +170 x, −79 z)"),
            ("C_DESTEK", "Aktarma destek plakası (bizim) · 2 mm 304 · y 1167 · diskin arka kenarının gerisinde (z −345…−420): çapraz itmede pidenin arkada kalan kısmını taşır")]
MALZEME = {"paslanmaz": dict(renk=(0.80, 0.82, 0.84, 1.0), met=0.9, ruf=0.30), "pom": dict(renk=(0.93, 0.93, 0.90, 1.0), met=0.0, ruf=0.50),
           "alu": dict(renk=(0.78, 0.80, 0.82, 1.0), met=0.8, ruf=0.35), "siyah": dict(renk=(0.12, 0.12, 0.13, 1.0), met=0.2, ruf=0.60),
           "hortum_mavi": dict(renk=(0.20, 0.45, 0.90, 1.0), met=0.0, ruf=0.50), "celik": dict(renk=(0.60, 0.62, 0.66, 1.0), met=1.0, ruf=0.35)}


def kut(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), centered=False).translate((min(x0, x1), min(y0, y1), min(z0, z1)))
def silx(y, z, r, x0, x1): return cq.Workplane("YZ").center(y, z).circle(r).extrude(x1 - x0).translate((x0, 0, 0))
def sily(x, z, r, y0, y1): return cq.Workplane("XZ").center(x, z).circle(r).extrude(-(y1 - y0)).translate((0, y0, 0))
def silz(x, y, r, z0, z1): return cq.Workplane("XY").center(x, y).circle(r).extrude(z1 - z0).translate((0, 0, z0))


def yerel(wp):
    """yerel (s, y, w) → dünya: Y ekseninde +THETA, sonra Pc'ye taşı"""
    return wp.rotate((0, 0, 0), (0, 1, 0), THETA).translate((PC[0], 0.0, PC[1]))


def dunya_nokta(s, y, w):
    return (PC[0] + s * U[0] + w * W[0], y, PC[1] + s * U[1] + w * W[1])


def ekle(ad, wp, mal, birim, grup="SABIT", kaynak="BİZİM", bom=None):
    PARCALAR.append(dict(ad=ad, wp=wp, mal=mal, birim=birim, grup=grup, kaynak=kaynak, bom=bom))


def dunya(p):
    sh = p["wp"].val() if isinstance(p["wp"], cq.Workplane) and len(p["wp"].vals()) == 1 else cq.Compound.makeCompound([o for o in p["wp"].vals() if isinstance(o, cq.Shape)])
    return sh


# ================================================================ KURULUM
def kur(s_araba=S_HOME, kalkik=True):
    """s_araba: çubuk yüzünün s konumu · kalkik: çubuk 90° kalkık (ev) / dik (itme). ARABA ve KOL parçaları bu konumda kurulur;
    montaj animasyonu için ARABA yerel ağı s=0'da, KOL yerel ağı pivotta üretilir (montaj kendi öteler)."""
    PARCALAR[:] = []
    S0, S1 = S_STROK0 - MY["Z"] / 2.0, S_STROK0 + STROK + MY["Z"] / 2.0      # gövde: strok aralığının iki ucunda 80'er uç kutusu (Z 160)
    wa = W_AXIS
    # ---- 1 SABİT: montaj kirişi + kolsuz silindir gövdesi + anahtarlar + hız ayarları + KALDIRMA PİMİ ----
    ekle("montaj_kirisi", yerel(kut(S0 - 20.0, S1 + 20.0, TAVAN - 6.0, TAVAN, wa - MY["NW"] / 2.0, wa + MY["NW"] / 2.0)), "paslanmaz", "C_ITICI",
         bom=("Montaj kirişi lama 37 × 6", 1, "304 · %.0f mm" % (S1 - S0 + 40.0), "soğuk oda tabanının çerçevesine (raf ön bükümü + sağ duvar alt profili) 4 × M6 · silindir alt deliklerinden 4 × M4 · gövde genişliğinde (iniş boruları arasından geçer)"))
    ekle("pim_braketi", yerel(kut(PIM_KALDIRMA_S - 12.0, PIM_KALDIRMA_S + 12.0, TAVAN - 6.0, TAVAN, wa + MAKARA["w"] - 10.0, wa - MY["NW"] / 2.0)), "paslanmaz", "C_ITICI",
         bom=("Kaldırma pimi braketi 6 mm", 1, "304 · 24 × %.0f" % (-MAKARA["w"] + 10.0 - MY["NW"] / 2.0), "kirişin −w kenarına kaynak · pim M8 dişle · ev ucunda (borulardan ve fitilden uzak)"))
    ekle("my1b16_govde", yerel(kut(S0, S1, TAVAN - 6.0 - MY["NE"], TAVAN - 6.0, wa - MY["NW"] / 2.0, wa + MY["NW"] / 2.0)), "alu", "C_ITICI", kaynak="K",
         bom=("SMC MY1B16-250 kolsuz silindir (mekanik bağlantılı, temel tip)", 1, "SMC · katalog ölçüleriyle kutu model (STEP indirilmedi)",
              "Ø16 · strok 250 · gövde %.0f × 37 × 27,8 · 0,5 MPa'da 100 N · ters (tabla aşağı) asılı · portlar M5 uçlarda" % (S1 - S0)))
    for i, s_ in enumerate((S0 + 8.0, S1 - 8.0)):
        ekle("hiz_ayar_%d" % i, yerel(silz(s_, TAVAN - 6.0 - MY["NE"] - 8.0, 4.0, wa + MY["NW"] / 2.0, wa + MY["NW"] / 2.0 + 14.0)), "siyah", "C_ITICI", kaynak="K",
             bom=("SMC AS1201F-M5-06 hız ayar valfi (M5, Ø6 hortum)", 2, "SMC", "her uçta çıkış kısma") if i == 0 else None)
        ekle("anahtar_%d" % i, yerel(kut(s_ - 12.0, s_ + 12.0, TAVAN - 6.0 - MY["NE"] - 2.0, TAVAN - 6.0 - MY["NE"] + 4.0, wa - MY["NW"] / 2.0 - 5.0, wa - MY["NW"] / 2.0)), "siyah", "C_ITICI", kaynak="K",
             bom=("SMC D-M9BL manyetik anahtar", 2, "SMC", "ev / son konum") if i == 0 else None)
    ekle("kaldirma_pimi", yerel(sily(PIM_KALDIRMA_S, wa + MAKARA["w"], 4.0, Y_SERBEST, TAVAN - 6.0).union(sily(PIM_KALDIRMA_S, wa + MAKARA["w"], 9.0, TAVAN - 12.0, TAVAN - 6.0))), "celik", "C_ITICI", kaynak="K",
         bom=("Pim ISO 8734 8 m6 × 70 + Ø18 × 6 boyun", 1, "paslanmaz · pim braketine M8 diş", "sabit KALDIRMA PİMİ: araba eve dönerken makara buna dayanır, link 90° kalkar · altı 1210 (pide üstü 1201)"))
    # ---- 2 ARABA (hareketli, s = s_araba): kızak tablası + pivot braketi (U) + pivot/dayama pimleri ----
    sa = s_araba
    ekle("kizak_tablasi", yerel(kut(sa - MY["L"] / 2.0, sa + MY["L"] / 2.0, Y_TABLA_YUZ, Y_TABLA_YUZ + (MY["H"] - MY["NE"]), wa - MY["LW"] / 2.0, wa + MY["LW"] / 2.0)), "alu", "C_ITICI", "ARABA", kaynak="K",
         bom=("MY1B16 kızak tablası (silindirin parçası)", 1, "SMC", "80 × 30 · 4 × M4 (40 × 20)"))
    ekle("pivot_braketi", yerel(kut(sa - 30.0, sa + 30.0, Y_TABLA_YUZ - 3.0, Y_TABLA_YUZ, wa - 19.0, wa + 15.0)
                                .union(kut(sa - 12.0, sa + 6.0, PIVOT_Y - 5.0, Y_TABLA_YUZ, wa - 19.0, wa - 16.0))
                                .union(kut(sa - 12.0, sa + 6.0, PIVOT_Y - 5.0, Y_TABLA_YUZ, wa + 10.0, wa + 13.0))
                                .cut(silz(sa, PIVOT_Y, 2.05, wa - 20.0, wa + 30.0)).cut(silz(sa + STOP_S, PIVOT_Y - 4.0, 1.55, wa - 20.0, wa + 30.0))), "paslanmaz", "C_ITICI", "ARABA",
         bom=("Pivot braketi 3 mm (U)", 1, "304 lazer + büküm · 60 × 34 taban, iki kulak 18 × 15 (asimetrik: −12…+6, kalkık link kulağı geçer)", "tablaya 4 × M4 · pivot deliği Ø4,1 · dayama pimi deliği Ø3,1"))
    ekle("pivot_pimi", yerel(silz(sa, PIVOT_Y, 2.0, wa - 20.0, wa + 15.0)), "celik", "C_ITICI", "ARABA", kaynak="K",
         bom=("Pim ISO 8734 4 m6 × 35 A1", 1, "sertleştirilmiş paslanmaz", "kulaklara sıkı, link POM burçta döner"))
    ekle("dayama_pimi", yerel(silz(sa + STOP_S, PIVOT_Y - 4.0, 1.5, wa - 19.0, wa + 13.0)), "celik", "C_ITICI", "ARABA", kaynak="K",
         bom=("Pim ISO 8734 3 m6 × 32", 1, "paslanmaz", "link dikken arkasına dayanır: itme momentini taşır (pivotun 4 altında)"))
    # ---- 3 KOL (ARABA'nın çocuğu, pivot etrafında döner): link + çubuk + POM burç + makara ----
    mw = wa + MAKARA["w"]                                                                                  # makara merkezi w (−5)
    link = kut(sa - 3.0, sa, BAR_Y1, PIVOT_Y + 4.0, wa - 16.0, wa + 10.0)                                    # ana plaka 26 geniş (kulakların arasında)
    link = link.union(kut(sa - 3.0, sa, BAR_Y1, PIVOT_Y - 7.0, mw + 4.0, wa - 16.0))                         # v2: alt uzantı −w'ye, −w kulağının ALTINDAN makara kulağına (1217'ye kadar)
    link = link.union(silz(sa - 1.5, PIVOT_Y, 5.0, wa - 16.0, wa + 10.0)).cut(silz(sa - 1.5, PIVOT_Y, 2.75, wa - 18.0, wa + 12.0))   # burç borusu Ø10 × 26, delik Ø5,5
    bar = kut(sa - 3.0, sa, BAR_Y0, BAR_Y1, BAR_W0, BAR_W1).union(kut(sa - 12.0, sa - 3.0, BAR_Y0, BAR_Y0 + 2.0, BAR_W0, BAR_W1))   # çubuk 3 mm + arka taban 9 (rijitlik; kalkınca en alt 1212)
    mak_kulak = kut(sa - 12.0, sa - 3.0, MAKARA["y"] - 6.0, MAKARA["y"] + 4.0, mw + 4.0, mw + 7.0)         # v2: makara kulağı 3 mm (−s yüzünden çıkar, makaranın +w yanında)
    kol = link.union(bar).union(mak_kulak)
    burc = silz(sa - 1.5, PIVOT_Y, 2.75, wa - 16.0, wa + 10.0).cut(silz(sa - 1.5, PIVOT_Y, 2.05, wa - 17.0, wa + 11.0))
    mak = silz(sa + MAKARA["s"], MAKARA["y"], MAKARA["r"], mw - 4.0, mw + 4.0)
    mak_pim = silz(sa + MAKARA["s"], MAKARA["y"], 1.5, mw - 4.0, mw + 8.0)
    if kalkik:   # +90°: pivot ekseni (w) etrafında, alt uç +s'ye ve yukarı
        kol = kol.rotate((sa, PIVOT_Y, 0), (sa, PIVOT_Y, 1), 90.0); burc = burc.rotate((sa, PIVOT_Y, 0), (sa, PIVOT_Y, 1), 90.0)
        mak = mak.rotate((sa, PIVOT_Y, 0), (sa, PIVOT_Y, 1), 90.0); mak_pim = mak_pim.rotate((sa, PIVOT_Y, 0), (sa, PIVOT_Y, 1), 90.0)
    ekle("kol_link_cubuk", yerel(kol), "paslanmaz", "C_ITICI", "KOL",
         bom=("Link + itici çubuk (tek parça kaynak)", 1, "304 · 3 mm · çubuk 170 × 30 + 9 mm taban · link 26 × 28 + alt uzantı + burç borusu Ø10 × 26 + makara kulağı", "pide kenarını 30 mm boyunca iter · POM burçla pivot pimine · kalkınca 1222–1226'da yatar"))
    ekle("kol_burcu", yerel(burc), "pom", "C_ITICI", "KOL", kaynak="K", bom=("Burç igus iglidur G GSM-0405-25 (Ø4 × 5,5 × 25, flanşsız; boru 26)", 1, "igus", "yağsız pivot yatağı, burç borusuna sıkı"))
    ekle("kol_makarasi", yerel(mak), "pom", "C_ITICI", "KOL", bom=("Makara POM Ø8 × 8", 1, "POM torna", "kaldırma pimine rolan"))
    ekle("kol_makara_pimi", yerel(mak_pim), "celik", "C_ITICI", "KOL", kaynak="K", bom=("Pim ISO 8734 3 m6 × 12", 1, "paslanmaz", "makara aksı, kulağa sıkı (konsol)"))
    # ---- 4 DESTEK PLAKASI (sabit): y 1167, z −345…−420, x 2200…2500 + arka flanş + sağ saca braket + sol ayak ----
    ekle("destek_plakasi", kut(2200.0, 2490.0, 1165.0, 1167.0, -420.0, -345.0).union(kut(2200.0, 2490.0, 1147.0, 1165.0, -422.0, -420.0)), "paslanmaz", "C_DESTEK",
         bom=("Destek plakası 2 mm", 1, "304 · 300 × 75 + 20 arka flanş", "üstü 1167 = disk üstünün 1 mm altı · diskin arka kenarına (−340) 5 mm · pidenin arkada kalan 60 mm'sini taşır · bant yan sacına (2502) 2 mm"))
    ekle("destek_sag_braketi", kut(2460.0, 2489.0, 1162.0, 1165.0, -420.0, -345.0).union(kut(2489.0, 2492.0, 1130.0, 1165.0, -420.0, -345.0)), "paslanmaz", "C_DESTEK",
         bom=("Destek braketi 3 mm (L)", 1, "304", "TOPPING sağ dış sacının iç yüzüne 2 × M5"))
    ekle("destek_sol_ayagi", kut(2205.0, 2220.0, 1124.0, 1165.0, -440.0, -425.0), "paslanmaz", "C_DESTEK",
         bom=("Destek ayağı 15 × 15", 1, "304 · 41 mm", "enerji zinciri kanalının üstüne (1124) 1 × M5"))
    return PARCALAR


def _boru(pts, r):
    """kırık çizgi boyunca boru (yerel koordinatta silindir parçaları)"""
    shp = None
    for (a, b) in zip(pts[:-1], pts[1:]):
        L = math.dist(a, b)
        if L < 1e-6: continue
        seg = cq.Solid.makeCylinder(r, L, V(*a), V(b[0] - a[0], b[1] - a[1], b[2] - a[2]))
        shp = seg if shp is None else shp.fuse(seg)
    return shp


# ================================================================ DENETİM
def kontrol_hepsi():
    """kendi arasında kesişim (ev + son konum), koridor kuralı, boruları/sensör boşlukları, zarf"""
    sonuc = []
    BORU_KASAR = ("sil", 2061.0, -150.0, 25.0, 1216.0, 1305.0)                # kaşar iniş borusu Ø50 (TU6 ölçüldü)
    BORU_SUCUK = ("sil", 2310.0, -150.0, 24.0, 1216.0, 1305.0)                # sucuk iniş borusu Ø48
    SENSOR = ("kut", 2341.0, 2359.0, 1210.0, 1250.0, -179.0, -161.0)          # tabla boş sensörü (TC24)
    def bb(sh): return sh.BoundingBox()
    KUTU = {}
    def bos(sh, kutu):
        if kutu not in KUTU:
            KUTU[kutu] = sily(kutu[1], kutu[2], kutu[3], kutu[4], kutu[5]).val() if kutu[0] == "sil" else kut(kutu[1], kutu[2], kutu[3], kutu[4], kutu[5], kutu[6]).val()
        try: return sh.distance(KUTU[kutu])
        except Exception: return -1.0
    for s_, kal, ad in ((S_HOME, True, "EV (kalkık)"), (S_HOME, False, "EV (çubuk inik)"), (S_END, False, "SON (itme bitti)"), ((S_HOME + S_END) / 2.0, False, "ORTA"),
                        (100.0, False, "s 100 (sucuk borusu altı)"), (120.0, False, "s 120"), (140.0, False, "s 140"), (160.0, False, "s 160 (sensör)")):
        P = kur(s_, kal)
        shs = [(p["ad"], dunya(p)) for p in P]
        kes = []
        for i in range(len(shs)):
            for j in range(i + 1, len(shs)):
                a, b = shs[i], shs[j]
                if a[0].startswith("kol_") and b[0].startswith("kol_"): continue                      # tek parça sayılır
                if {a[0], b[0]} & {"pivot_pimi", "kol_burcu", "dayama_pimi", "kol_makara_pimi", "kol_makarasi"}: continue   # deliklerde / temas
                ba, bb_ = bb(a[1]), bb(b[1])
                if not (ba.xmin < bb_.xmax and bb_.xmin < ba.xmax and ba.ymin < bb_.ymax and bb_.ymin < ba.ymax and ba.zmin < bb_.zmax and bb_.zmin < ba.zmax): continue
                try: v_ = a[1].intersect(b[1]).Volume()
                except Exception: v_ = -1.0
                if v_ > 1.0 or v_ < 0: kes.append((a[0], b[0], round(v_, 1)))
        sonuc.append(("%s · kendi arasında kesişim yok" % ad, not kes, str(kes[:5])))
        # boruları / sensör boşluğu (hareketli + sabit hepsi)
        en = 1e9; kim = ""
        for nm, sh in shs:
            if nm.startswith("destek"): continue
            for kad, kutu in (("kaşar iniş borusu", BORU_KASAR), ("sucuk iniş borusu", BORU_SUCUK), ("tabla boş sensörü", SENSOR)):
                d_ = bos(sh, kutu)
                if d_ < en: en, kim = d_, "%s ↔ %s" % (nm, kad)
        sonuc.append(("%s · iniş boruları ve sensöre en az 3 mm (%.1f: %s)" % (ad, en, kim), en >= 3.0, ""))
        # koridor kuralı: ev konumunda 1210'un altında hiçbir itici parçası pide koridorunda olamaz
        if s_ == S_HOME and kal:
            ihlal = []
            for nm, sh in shs:
                if nm.startswith("destek"): continue
                b_ = bb(sh)
                if b_.ymin < Y_SERBEST and b_.zmax > KORIDOR_Z[0] and b_.zmin < KORIDOR_Z[1]: ihlal.append((nm, round(b_.ymin, 1)))
            sonuc.append(("EV (kalkık) · pide koridorunda (z −320…−20) 1210'un altında parça yok", not ihlal, str(ihlal)))
        # zarf: modül içinde (x ≤ 2492 sağ dış sac, z ≤ −5, y ≤ 1277)
        b_all = [bb(sh) for nm, sh in shs if not nm.startswith("destek")]
        sonuc.append(("%s · zarf: x ≤ 2492 (%.0f) · z ≤ −5 (%.0f) · y ≤ 1277 (%.0f)" % (ad, max(b.xmax for b in b_all), max(b.zmax for b in b_all), max(b.ymax for b in b_all)),
                      max(b.xmax for b in b_all) <= 2492.0 and max(b.zmax for b in b_all) <= -5.0 and max(b.ymax for b in b_all) <= TAVAN + 0.01, ""))
        if not kal:
            kol = [sh for nm, sh in shs if nm == "kol_link_cubuk"][0]; b_ = bb(kol)
            sonuc.append(("%s · çubuk altı diskin 2 mm üstünde (%.1f)" % (ad, b_.ymin), abs(b_.ymin - (DISK_UST + 2.0)) < 0.01, ""))
    # itme geometrisi
    pc_end = (C0[0] + (S_END - 15.0) * U[0], C0[1] + (S_END - 15.0) * U[1])
    sonuc.append(("itme sonu pide merkezi (%.0f, %.0f) = hedef (2540, −249)" % pc_end, abs(pc_end[0] - C1[0]) < 0.1 and abs(pc_end[1] - C1[1]) < 0.1, ""))
    sonuc.append(("son konumda pidenin ön kenarı z %.0f ≥ tünel ön duvarı −79 + 20" % (C1[1] + R_PIDE), C1[1] + R_PIDE <= -99.0 + 0.01, ""))
    sonuc.append(("pide sonda bantlarda: ön kenar %.0f ≥ fırın bandı başı 2568 + 80 · merkez %.0f ≥ giriş bandı burnu 2505 · arka kenar %.0f ≥ destek başı 2200" % (C1[0] + R_PIDE, C1[0], C1[0] - R_PIDE), C1[0] + R_PIDE >= 2648.0 and C1[0] >= 2505.0 and C1[0] - R_PIDE >= 2200.0, ""))
    mk = (MAKARA["s"], MAKARA["y"] - PIVOT_Y); mk90 = (-mk[1], mk[0])       # −90° (alt uç +s'ye): (s, y) → (−y, s)
    sonuc.append(("kaldırma: makara 0°→90° s %.1f→%.1f (+%.1f = pimle ev arası %.1f)" % (mk[0], mk90[0], mk90[0] - mk[0], S_TEMAS - S_HOME), abs((mk90[0] - mk[0]) - (S_TEMAS - S_HOME)) < 0.01, ""))
    return sonuc


if __name__ == "__main__":
    t0 = time.time()
    DEN = kontrol_hepsi()
    for ad, ok, ek in DEN: print("  %-95s %s %s" % (ad, "GEÇTİ" if ok else "** KALDI **", ek))
    kal = [d for d in DEN if not d[1]]
    kur(S_HOME, True)
    print("İTİCİ v1 · %d parça · u = (%.3f, %.3f) · θ = %.2f° · Pc = (%.1f, %.1f) · strok %d (tabla %.0f…%.0f) · %.0f sn" % (len(PARCALAR), U[0], U[1], THETA, PC[0], PC[1], STROK, S_STROK0, S_STROK0 + STROK, time.time() - t0))
    assert not kal, kal
