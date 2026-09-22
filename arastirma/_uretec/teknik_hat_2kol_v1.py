# -*- coding: utf-8 -*-
"""AUTOKITCH - HAT 2 KOL · TEKNIK RESIM v1 (17 Eyl 2026): ON + UST (PLAN KESITI) + 2 YAN KESIT. Olculer mm.
Kemal'in eskizi (17 Eyl): sol secenek = 2 sabit robot kol · Fersah pres · Atosa dozaj TABLASIZ (tabani robot tutar) ·
2 gunluk her sey · firin 1 pide + 2 lahmacun gozu (kapakli, bant yok) · urun pide / pizza / lahmacun.
v14'ten FARKI: ray yok; STORE ayri govde degil — cekmeceler istasyonlarin ALTINDA (M0 12 lahmacun + teknik, M1 8 pide + pres,
M4 3 icecek + kutulama, M5 1 tatli + QR gozleri); TOPPING 2 katli 8 dozaj yuvasi (kaset 140x400x360, kasar kabi 280x400x360, sucuk dilimleyici);
iki robotun erisimi ortada AKTARMA RAFI'nda kesisir (uclar birbirine deger). HAT 5715 -> 4460.
ROBOT: 2 x Fairino FR10 (1.400 mm erisim). FR5 (922) yetmiyor: R1 bolgesi 2.200 mm genis (12+8 cekmece + pres + 8 yuva).
Kural: paftada yalniz gorunus + olcu + parca adi; aciklama mesajda.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE\HAT_2KOL_v1_teknik.png".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX = 5800, 3400
S = 0.62
BG, INK, GRAY, LINE = (255, 255, 255), (26, 26, 28), (132, 132, 140), (72, 72, 78)
FILL, ACC, RED, SOFT = (244, 244, 246), (0, 86, 184), (198, 42, 32), (228, 228, 234)
BUZ, DOLAP, BOSL, PUC, EVC = (28, 86, 166), (14, 120, 90), (190, 190, 196), (255, 240, 200), (220, 235, 255)
AGZ, SICAK = (253, 244, 243), (255, 226, 214)


def F(sz, b=False):
    for n in (("arialbd.ttf", "segoeuib.ttf") if b else ("arial.ttf", "segoeui.ttf")):
        try:
            return ImageFont.truetype(n, sz)
        except Exception:
            pass
    return ImageFont.load_default()


f7, f8, f9, f11, f13, f16, f38 = F(14), F(16), F(18), F(21), F(24), F(28, True), F(54, True)
im = Image.new("RGB", (W_PX, H_PX), BG)
d = ImageDraw.Draw(im)


def txt(x, y, s, f=f11, c=INK, a="la"):
    d.text((x, y), s, font=f, fill=c, anchor=a)


def satirlar(x, y, s, f, c, adim=20):
    ls = s.split("|")
    y0 = y - adim * (len(ls) - 1) / 2.0
    for i, l in enumerate(ls):
        txt(x, y0 + i * adim, l, f if i == 0 else f7, c if i == 0 else GRAY, "mm")


def sayi(v):
    return ("%g" % v).replace(".", ",")


def etiket(x, y, s, f=f8, c=INK, cer=GRAY):
    tw = d.textlength(s, font=f)
    d.rectangle([x - tw / 2 - 6, y - 11, x + tw / 2 + 6, y + 11], fill=BG, outline=cer, width=1)
    txt(x, y, s, f, c, "mm")


def olcu_h(x0, x1, y, s, f=f11, c=INK):
    d.line([(x0, y), (x1, y)], fill=c, width=2)
    for xx in (x0, x1):
        d.line([(xx, y - 8), (xx, y + 8)], fill=c, width=2)
    tw = d.textlength(s, font=f)
    d.rectangle([(x0 + x1) / 2 - tw / 2 - 6, y - 13, (x0 + x1) / 2 + tw / 2 + 6, y + 13], fill=BG)
    txt((x0 + x1) / 2, y, s, f, c, "mm")


def olcu_v(x, y0, y1, s, f=f11, c=INK, yon="r"):
    d.line([(x, y0), (x, y1)], fill=c, width=2)
    for yy in (y0, y1):
        d.line([(x - 8, yy), (x + 8, yy)], fill=c, width=2)
    txt(x + (12 if yon == "r" else -12), (y0 + y1) / 2, s, f, c, "lm" if yon == "r" else "rm")


def tarali(x0, y0, x1, y1, c=(222, 222, 228), adim=12):
    w, h = x1 - x0, y1 - y0
    for k in range(0, int(w + h), adim):
        ax, ay, bx, by = x0 + k, y1, x0 + k - h, y0
        if ax > x1:
            ay, ax = y1 - (ax - x1), x1
        if bx < x0:
            by, bx = y1 - k, x0
        if ay >= y0:
            d.line([(ax, ay), (bx, by)], fill=c, width=1)


def dline(p0, p1, c, w=1, dash=7, gap=4):
    (ax, ay), (bx, by) = p0, p1
    L = math.hypot(bx - ax, by - ay)
    if L < 1:
        return
    for i in range(int(L // (dash + gap)) + 1):
        t0 = min(1.0, i * (dash + gap) / L)
        t1 = min(1.0, (i * (dash + gap) + dash) / L)
        d.line([(ax + (bx - ax) * t0, ay + (by - ay) * t0), (ax + (bx - ax) * t1, ay + (by - ay) * t1)], fill=c, width=w)


def drect(x0, y0, x1, y1, c, w=1):
    dline((x0, y0), (x1, y0), c, w); dline((x1, y0), (x1, y1), c, w)
    dline((x1, y1), (x0, y1), c, w); dline((x0, y1), (x0, y0), c, w)


def darc(cx, cy, r, a0, a1, c, w=2, adim=4.0):
    """kesik yay: a0..a1 derece (PIL: saat yonu, 0 = sag)"""
    a = a0
    while a < a1:
        b = min(a1, a + adim)
        d.arc([cx - r, cy - r, cx + r, cy + r], a, b, fill=c, width=w)
        a = b + adim


# ======================= VERI =======================
DZ = 830.0                                     # tum moduller 830 derin: z -790 .. +40 (on panel)
WO, BIND, FUGA = 620.0, 15.0, 3.0              # cekmece ic genislik · conta alin · fuga
CELL0 = 182.5                                  # cekmece hucre tabani (plint 120 + PU 60 + sac)
YUZ0 = CELL0 - BIND
HH = {"hamur": 75.0, "lahm": 60.0, "icecek": 132.0, "tatli": 132.0}
AD = {"hamur": "TAZE PİDE", "lahm": "LAHMACUN", "icecek": "İÇECEK 330 ml", "tatli": "TATLI"}
CAP = {"hamur": (20, "top"), "lahm": (35, "top"), "icecek": (56, "kutu"), "tatli": (14, "adet")}

# moduller: (ad, genislik, cekmece gruplari, cephe)
# cephe: (tip k=kapak / a=acik agiz / g=QR gozu / y=kaset yuvasi kati, x0, x1, y0, y1, etiket, yuva, etiket kotu)
MOD = [
    ("M0 · STORE + TEKNİK", 700.0, [(12, "lahm")],
     [("k", 33.0, 667.0, 1300.0, 1968.5, "TEKNİK BÖLME|2 soğutma grubu · ana pano · çekmece sürücüleri", None, None)]),
    ("M1 · PRESS", 700.0, [(8, "hamur")],
     [("k", 33.0, 667.0, 1060.0, 1565.0, "FERSAH PZP-400|pres başlığı 640 × 800 · alt kabin yok · platen ~1200", None, 1500.0),
      ("a", 53.0, 647.0, 1120.0, 1400.0, "PRES AĞZI", None, None),
      ("k", 33.0, 667.0, 1580.0, 1968.5, "UÇ İSTASYONU|takım değiştirici · pençe · tepsi eli", None, None)]),
    ("M2 · TOPPING", 800.0, [],
     [("k", 33.0, 767.0, 121.5, 420.0, "PANO|R1 + R2 kontrol kutuları · dozaj sürücüleri", None, None),
      ("a", 30.0, 770.0, 430.0, 550.0, "ROBOT AĞZI · alt kat", None, None),
      ("k", 33.0, 767.0, 553.0, 677.0, "DOZAJ BAŞLIKLARI · nozul · piston pompa", None, None),
      ("y", 33.0, 767.0, 680.0, 1040.0, "", "t1", None),
      ("a", 30.0, 770.0, 1050.0, 1170.0, "ROBOT AĞZI · üst kat", None, None),
      ("k", 33.0, 767.0, 1173.0, 1297.0, "DOZAJ BAŞLIKLARI · nozul · karıştırıcı · dilim bıçağı", None, None),
      ("y", 33.0, 767.0, 1300.0, 1660.0, "", "t2", None),
      ("k", 33.0, 767.0, 1670.0, 1968.5, "SOĞUTMA +3 °C|evaporatör · fan · pano", None, None)]),
    ("M3 · OVEN", 700.0, [],
     [("k", 33.0, 667.0, 123.0, 370.0, "YAĞ KABI · PANO", None, None),
      ("a", 30.0, 670.0, 373.0, 533.0, "İŞLEM AĞZI · sprey", None, None),
      ("k", 33.0, 667.0, 536.0, 816.0, "KESİCİ · yıldız bıçak", None, None),
      ("k", 33.0, 667.0, 822.0, 1097.0, "FIRIN HAZNESİ 1|LAHMACUN · 120 s", None, None),
      ("k", 33.0, 667.0, 1102.0, 1377.0, "FIRIN HAZNESİ 2|LAHMACUN · 120 s", None, None),
      ("k", 33.0, 667.0, 1382.0, 1657.0, "FIRIN HAZNESİ 3|PİDE · PİZZA · 240 s · ayrı sıcaklık", None, None),
      ("k", 33.0, 667.0, 1662.0, 1968.5, "EGZOZ · fan · karbon filtre", None, None)]),
    ("M4 · PACK", 700.0, [(3, "icecek")],
     [("a", 30.0, 670.0, 700.0, 950.0, "KUTULAMA AĞZI", None, None),
      ("k", 33.0, 667.0, 960.0, 1880.0, "KUTU ŞARJÖRÜ|blank 400 × 760 · 920 mm = 510–610 kutu", None, None),
      ("k", 33.0, 667.0, 1883.0, 1968.5, "PANO · vakum · tahrik", None, None)]),
    ("M5 · PICKUP", 860.0, [(1, "tatli")],
     [("k", 33.0, 827.0, 340.0, 590.0, "ISITMA PANOSU · göz kilitleri", None, None)]
     + [("g", 30.0 + c * 410.0, 420.0 + c * 410.0, 600.0 + r * 200.0, 790.0 + r * 200.0,
         "QR GÖZÜ" if r == 5 else "", None, None) for r in range(6) for c in range(2)]
     + [("k", 33.0, 827.0, 1800.0, 1968.5, "PANO", None, None)]),
]
HAT = sum(w for _, w, _, _ in MOD)             # 4460
MX = {}
x = 0.0
for ad, w, _, _ in MOD:
    MX[ad] = x
    x += w
# topping yuvalari: (ad, genislik, merkez x — modul icinde)
YUVA = {"t1": [("HARÇ", 140.0, 190.0), ("HARÇ", 140.0, 330.0), ("HARÇ", 140.0, 470.0), ("HARÇ", 140.0, 610.0)],
        "t2": [("KIYMA", 140.0, 100.0), ("KUŞBAŞI", 140.0, 240.0), ("KAŞAR KABI", 280.0, 450.0), ("SUCUK|DİLİMLEYİCİ", 180.0, 680.0)]}
# robotlar: (ad, x, kaide yuksekligi, omuz)
R1X, R2X, RZ = 1100.0, 3330.0, 300.0           # kaide ekseni koridorda z = +300
KAIDE, OMUZ = 820.0, 1000.0
ERISIM, ERISIM_P = 1400.0, 1250.0              # FR10 nominal / pratik (%90)
AKT = (2000.0, 2400.0, 900.0, 1300.0)          # aktarma rafi: x0, x1, y0, y1 (koridorda z +80..+480)
KOR = 800.0

# ======================= YERLESIM =======================
OX = 300.0
FY_TOP = 400.0
FY = FY_TOP + 1970.0 * S                       # on gorunus zemin
PY_TOP = FY + 330.0                            # plan: z = -790 (arka)
SX = OX + HAT * S + 260.0                      # yan kesit A: z = -790 kenari
SX2 = SX + (DZ + KOR + 120.0) * S + 200.0      # yan kesit B


def fx(x):
    return OX + x * S


def fy(y):
    return FY - y * S


def py(z):
    return PY_TOP + (z + 790.0) * S


# ======================= BASLIK =======================
txt(OX, 70, "AUTOKITCH  ·  HAT 2 KOL  ·  TEKNİK RESİM  v1  ·  İKİ SABİT ROBOT  ·  KAPAKLI FIRIN  ·  BANT YOK  ·  2 GÜNLÜK STOK", f38, INK)
txt(OX, 138, "ön · üst · yan görünüş  ·  günde 80 pide + 200 lahmacun (+ pizza)  ·  çekmeceler istasyonların altında  ·  dozaj tablasız (tabanı robot tutar)  ·  2 × Fairino FR10  ·  tüm modüller 830 derin  ·  ölçüler mm  ·  17 Eylül 2026", f13, GRAY)
d.line([(OX, 178), (W_PX - 170, 178)], fill=LINE, width=3)

# ======================= ON GORUNUS =======================
txt(OX, FY_TOP - 190, "ÖN GÖRÜNÜŞ", f16, ACC)
txt(OX, FY_TOP - 152, "robotlar koridorda, önde — şematik", f9, GRAY)


def cekmece_kolonu(cx, gruplar):
    """cx: kolonun sol ic kenari (mm). donen: son cekmecenin ustu"""
    y = YUZ0
    for adet, tip in gruplar:
        h = HH[tip] + 2 * BIND
        ybas = y
        for _ in range(adet):
            d.rectangle([fx(cx + 8), fy(y + h), fx(cx + WO - 8), fy(y)], fill=BG, outline=DOLAP, width=1)
            y += h + FUGA
        cap, br = CAP[tip]
        ym = (fy(ybas) + fy(y - FUGA)) / 2
        etiket(fx(cx + WO / 2), ym - 13, "%s × %d" % (AD[tip], adet), f8, INK, DOLAP)
        etiket(fx(cx + WO / 2), ym + 13, "%d %s · +3 °C" % (adet * cap, br), f7, DOLAP, DOLAP)
    olcu_h(fx(cx), fx(cx + WO), fy(0) + 44, "620", f8, GRAY)
    return y - FUGA


def modul_on(ad, x0mm, w, gruplar, cephe):
    x0, x1 = fx(x0mm), fx(x0mm + w)
    d.rectangle([x0, fy(1970), x1, fy(0)], fill=FILL, outline=LINE, width=3)
    d.rectangle([x0, fy(120), x1, fy(0)], fill=SOFT, outline=LINE, width=2)
    txt((x0 + x1) / 2, fy(1970) - 64, ad, f13, INK, "md")
    if gruplar:
        cx = x0mm + (w - WO) / 2.0
        d.rectangle([fx(cx - 25), fy(1290.0 if ad.startswith("M0") else (1050.0 if ad.startswith("M1") else (690.0 if ad.startswith("M4") else 336.0))), fx(cx + WO + 25), fy(121.5)], fill=BG, outline=LINE, width=2)
        cekmece_kolonu(cx, gruplar)
    for tip, a, b, y0, y1, et, yv, yl in cephe:
        if tip in ("k", "y", "g"):
            d.rectangle([fx(x0mm + a), fy(y1), fx(x0mm + b), fy(y0)], fill=(SICAK if "FIRIN" in et else BG), outline=LINE, width=2)
        if tip == "y":
            ym = (y0 + y1) / 2.0
            for urun, gw, xc in YUVA[yv]:
                drect(fx(x0mm + xc - gw / 2 + 6), fy(y1 - 8), fx(x0mm + xc + gw / 2 - 6), fy(y0 + 8), INK, 1)
                satirlar(fx(x0mm + xc), fy(ym) - 4, urun, f7, INK, 16)
                txt(fx(x0mm + xc), fy(ym) + 22, ("%s × 400 × 360" % sayi(gw)) if "SUCUK" not in urun else "çubuk şarjörü", f7, GRAY, "mm")
        elif tip == "g":
            if et:
                txt(fx(x0mm + (a + b) / 2), fy((y0 + y1) / 2), et, f7, INK, "mm")
        elif tip == "k" and et:
            satirlar(fx(x0mm + (a + b) / 2), fy(yl if yl else (y0 + y1) / 2), et, f8, INK)
    for tip, a, b, y0, y1, et, yv, yl in cephe:
        if tip != "a":
            continue
        d.rectangle([fx(x0mm + a), fy(y1), fx(x0mm + b), fy(y0)], fill=AGZ, outline=RED, width=3)
        cy = (fy(y0) + fy(y1)) / 2
        txt(fx(x0mm + (a + b) / 2), cy - 10, et, f8, RED, "mm")
        txt(fx(x0mm + (a + b) / 2), cy + 12, "y %s – %s" % (sayi(y0), sayi(y1)), f7, RED, "mm")


for ad, w, gruplar, cephe in MOD:
    modul_on(ad, MX[ad], w, gruplar, cephe)
    olcu_h(fx(MX[ad]), fx(MX[ad] + w), fy(1970) - 26, sayi(w), f11, INK)
olcu_h(fx(0), fx(HAT), fy(0) + 96, "HAT  %s" % sayi(HAT), f13, INK)
olcu_v(fx(0) - 44, fy(1970), fy(0), "1970", f11, INK, "l")
# --- aktarma rafi + cop (koridorda, birlesim onunde)
ax0, ax1, ay0, ay1 = AKT
drect(fx(ax0), fy(ay1), fx(ax1), fy(ay0), ACC, 2)
for i in range(6):
    yy = ay0 + 40 + i * 60
    d.line([(fx(ax0 + 30), fy(yy)), (fx(ax1 - 30), fy(yy))], fill=ACC, width=2)
txt(fx((ax0 + ax1) / 2), fy(ay1) - 16, "AKTARMA RAFI · 6 tepsi Ø340", f8, ACC, "mm")
drect(fx(ax0 + 40), fy(720.0), fx(ax1 - 40), fy(130.0), GRAY, 1)
txt(fx((ax0 + ax1) / 2), fy(425.0), "ÇÖP 60 L", f8, GRAY, "mm")
# --- robotlar (sematik; koridorda onde)
for rx, ad, ex, ey, wx, wy in ((R1X, "R1 · FR10", 1640.0, 1300.0, 2130.0, 1120.0),
                               (R2X, "R2 · FR10", 2800.0, 1310.0, 2280.0, 1130.0)):
    d.rectangle([fx(rx - 200), fy(15.0), fx(rx + 200), fy(0)], fill=SOFT, outline=ACC, width=2)
    d.rectangle([fx(rx - 100), fy(KAIDE), fx(rx + 100), fy(15.0)], fill=BG, outline=ACC, width=3)
    txt(fx(rx), fy(KAIDE / 2), "KAİDE|%s" % sayi(KAIDE), f7, ACC, "mm")
    for w_, c_ in ((16, BG), (9, ACC)):
        d.line([(fx(rx), fy(OMUZ)), (fx(ex), fy(ey)), (fx(wx), fy(wy))], fill=c_, width=w_, joint="curve")
    d.ellipse([fx(rx) - 18, fy(OMUZ) - 18, fx(rx) + 18, fy(OMUZ) + 18], fill=ACC, outline=BG, width=2)
    d.rectangle([fx(rx) - 60, fy(OMUZ) - 60, fx(rx) + 60, fy(OMUZ) - 34], fill=BG)
    txt(fx(rx), fy(OMUZ) - 46, ad, f9, ACC, "mm")

# ======================= UST GORUNUS (PLAN KESITI) =======================
txt(OX, PY_TOP - 170, "ÜST GÖRÜNÜŞ  ·  PLAN KESİTİ  ·  robot erişimi", f16, ACC)
txt(fx(HAT / 2), py(-790) - 34, "ARKA  ·  M5 arkası müşteri cephesi", f9, GRAY, "mm")
for ad, w, gruplar, cephe in MOD:
    x = MX[ad]
    zb = 40.0 - DZ
    d.rectangle([fx(x), py(zb), fx(x + w), py(40.0)], fill=FILL, outline=LINE, width=3)
    cx = x + (w - WO) / 2.0
    if gruplar:
        d.rectangle([fx(x + 1.5), py(zb + 1.5), fx(x + w - 1.5), py(zb + 61.5)], fill=PUC, outline=GRAY, width=1)
        drect(fx(cx + 16), py(-680.0), fx(cx + WO - 16), py(0.0), DOLAP, 2)
        d.rectangle([fx(cx + 190), py(-725.0), fx(cx + 450), py(-680.0)], fill=EVC, outline=BUZ, width=1)
        d.rectangle([fx(cx + 17), py(-716.0), fx(cx + 67), py(-680.0)], fill=(255, 230, 230), outline=RED, width=1)
        txt(fx(cx + 320), py(-702.5), "EVAPORATÖR", f7, BUZ, "mm")
        txt(fx(cx + 42), py(-698.0), "M", f7, RED, "mm")
    if ad.startswith("M0"):
        txt(fx(x + w / 2), py(-420.0), "ÇEKMECE 620 × 680", f8, INK, "mm")
        txt(fx(x + w / 2), py(-390.0), "LAHMACUN × 12 · altta", f7, DOLAP, "mm")
        txt(fx(x + w / 2), py(-250.0), "üstte: 2 soğutma grubu · ana pano", f7, GRAY, "mm")
    elif ad.startswith("M1"):
        d.rectangle([fx(x + 29), py(-788.0), fx(x + 669), py(12.0)], fill=BG, outline=INK, width=2)
        txt(fx(x + 349), py(-430.0), "FERSAH PZP-400", f8, INK, "mm")
        txt(fx(x + 349), py(-400.0), "640 × 800 · platen Ø400", f7, GRAY, "mm")
        d.ellipse([fx(x + 149), py(-500.0), fx(x + 549), py(-100.0)], outline=GRAY, width=1)
        txt(fx(x + 349), py(-250.0), "altta: TAZE PİDE × 8", f7, DOLAP, "mm")
    elif ad.startswith("M2"):
        for urun, gw, xc in YUVA["t2"]:
            d.rectangle([fx(x + xc - gw / 2 + 6), py(-470.0), fx(x + xc + gw / 2 - 6), py(-70.0)], fill=BG, outline=INK, width=2)
            satirlar(fx(x + xc), py(-300.0), urun, f7, INK, 16)
            txt(fx(x + xc), py(-250.0), "%s × 400" % sayi(gw) if "SUCUK" not in urun else "180 × 400", f7, GRAY, "mm")
        for _, gw, xc in YUVA["t1"]:
            drect(fx(x + xc - gw / 2 + 6), py(-470.0), fx(x + xc + gw / 2 - 6), py(-70.0), GRAY, 1)
        txt(fx(x + w / 2), py(-560.0), "alt kat: HARÇ × 4 (kesik çizgi)", f7, GRAY, "mm")
        d.rectangle([fx(x + 30), py(-780.0), fx(x + 770), py(-740.0)], fill=EVC, outline=BUZ, width=1)
        txt(fx(x + w / 2), py(-760.0), "EVAPORATÖR · +3 °C kabin", f7, BUZ, "mm")
        d.rectangle([fx(x + 30), py(-60.0), fx(x + 770), py(0.0)], fill=AGZ, outline=RED, width=1)
        txt(fx(x + w / 2), py(-30.0), "ROBOT AĞZI · kapaklı", f7, RED, "mm")
    elif ad.startswith("M3"):
        d.rectangle([fx(x + 30), py(-600.0), fx(x + 670), py(-20.0)], fill=SICAK, outline=INK, width=2)
        txt(fx(x + 350), py(-325.0), "FIRIN · 3 HAZNE", f8, INK, "mm")
        txt(fx(x + 350), py(-295.0), "640 × 600 × 840 · kapaklı", f7, GRAY, "mm")
        d.rectangle([fx(x + 30), py(-780.0), fx(x + 670), py(-620.0)], fill=BG, outline=GRAY, width=1)
        txt(fx(x + 350), py(-700.0), "EGZOZ KANALI · fan", f7, GRAY, "mm")
    elif ad.startswith("M4"):
        drect(fx(x + 150), py(-785.5), fx(x + 550), py(-25.5), GRAY, 1)
        txt(fx(x + 350), py(-640.0), "BLANK 400 × 760", f7, GRAY, "mm")
        d.rectangle([fx(x + 190), py(-410.0), fx(x + 510), py(-90.0)], fill=BG, outline=INK, width=2)
        txt(fx(x + 350), py(-265.0), "KUTU", f8, INK, "mm")
        txt(fx(x + 350), py(-235.0), "320 × 320 × 45", f7, GRAY, "mm")
        txt(fx(x + 350), py(-540.0), "altta: İÇECEK × 3", f7, DOLAP, "mm")
    elif ad.startswith("M5"):
        for c in range(2):
            d.rectangle([fx(x + 30 + c * 410), py(-760.0), fx(x + 420 + c * 410), py(-10.0)], fill=BG, outline=INK, width=2)
            txt(fx(x + 225 + c * 410), py(-400.0), "QR GÖZÜ × 6", f8, INK, "mm")
            txt(fx(x + 225 + c * 410), py(-370.0), "380 × 190 × 750", f7, GRAY, "mm")
            txt(fx(x + 225 + c * 410), py(-340.0), "çift kapak · ısıtmalı", f7, GRAY, "mm")
        txt(fx(x + w / 2), py(-140.0), "altta: TATLI × 1", f7, DOLAP, "mm")
    txt(fx(x + w / 2), py(40.0) + 30, "%s  ·  %s × %s" % (ad, sayi(w), sayi(DZ)), f9, INK, "mm")
olcu_h(fx(0), fx(HAT), py(40.0) + 96, "HAT  %s" % sayi(HAT), f13, INK)
olcu_v(fx(0) - 44, py(-790), py(40.0), sayi(DZ), f11, INK, "l")
# --- koridor: robot kaideleri, erisim yaylari, aktarma rafi
d.line([(fx(-60), py(40.0 + KOR)), (fx(HAT + 60), py(40.0 + KOR))], fill=GRAY, width=1)
txt(fx(HAT / 2), py(40.0 + KOR) + 22, "ÖN  ·  robot koridoru %s  ·  robot tarafı" % sayi(KOR), f9, GRAY, "mm")
d.rectangle([fx(ax0), py(80.0), fx(ax1), py(480.0)], fill=BG, outline=ACC, width=2)
txt(fx((ax0 + ax1) / 2), py(255.0), "AKTARMA RAFI", f8, ACC, "mm")
txt(fx((ax0 + ax1) / 2), py(300.0), "6 tepsi · altında çöp", f7, GRAY, "mm")
for rx, ad in ((R1X, "R1 · FR10 · erişim 1400"), (R2X, "R2 · FR10 · erişim 1400")):
    cxp, cyp = fx(rx), py(RZ)
    d.rectangle([fx(rx - 200), py(RZ - 200), fx(rx + 200), py(RZ + 200)], fill=SOFT, outline=ACC, width=1)
    d.ellipse([cxp - 100 * S, cyp - 100 * S, cxp + 100 * S, cyp + 100 * S], fill=BG, outline=ACC, width=3)
    darc(cxp, cyp, ERISIM_P * S, 183.0, 357.0, ACC, 2, 3.0)
    darc(cxp, cyp, ERISIM * S, 190.0, 350.0, BOSL, 1, 2.5)
    txt(cxp, py(RZ + 200) + 22, ad, f9, ACC, "mm")
    txt(cxp, py(RZ + 200) + 46, "kaide 400 × 400 · eksen z +300 · pratik erişim 1250", f7, GRAY, "mm")
d.rectangle([fx(0) - 60, py(40.0) + 60, fx(0) + 400, py(40.0) + 130], fill=BG)
txt(fx(0) - 50, py(40.0) + 76, "yay: pratik 1250 (mavi)", f7, ACC, "la")
txt(fx(0) - 50, py(40.0) + 100, "yay: nominal 1400 (gri)", f7, GRAY, "la")
txt(fx(HAT / 2), py(RZ + 200) + 80, "R1 bölgesi M0–M2 (0–2200)  ·  R2 bölgesi M3–M5 (2200–4460)  ·  iki erişim AKTARMA RAFI'nda kesişir", f9, INK, "mm")


# ======================= YAN KESIT A · M2 TOPPING =======================
def sz(z):
    return SX + (z + 790.0) * S


txt(SX, FY_TOP - 190, "YAN KESİT A", f16, ACC)
txt(SX, FY_TOP - 152, "M2 TOPPING · üst kat dozajı · robot koridorda", f9, GRAY)
d.rectangle([sz(-790), fy(1970), sz(40), fy(0)], fill=FILL, outline=LINE, width=3)
d.rectangle([sz(-790), fy(120), sz(40), fy(0)], fill=SOFT, outline=LINE, width=2)                  # plint
d.rectangle([sz(-788.5), fy(1968.5), sz(-728.5), fy(121.5)], fill=PUC, outline=GRAY, width=1)      # arka PU
d.rectangle([sz(-728.5), fy(1968.5), sz(0.0), fy(1908.5)], fill=PUC, outline=GRAY, width=1)        # tavan PU
d.rectangle([sz(-728.5), fy(181.5), sz(0.0), fy(121.5)], fill=PUC, outline=GRAY, width=1)          # taban PU
d.rectangle([sz(-728.5), fy(420.0), sz(0.0), fy(181.5)], fill=SOFT, outline=LINE, width=1)         # pano
txt(sz(-364), fy(300.0), "PANO · kontrol kutuları", f7, GRAY, "mm")
for (m0, m1, h0, h1, k0, k1, urun) in ((430.0, 550.0, 553.0, 677.0, 680.0, 1040.0, "HARÇ (alt kat)"),
                                        (1050.0, 1170.0, 1173.0, 1297.0, 1300.0, 1660.0, "KIYMA · KUŞBAŞI · KAŞAR · SUCUK")):
    d.rectangle([sz(-470.0), fy(k1), sz(-70.0), fy(k0)], fill=BG, outline=INK, width=2)             # kaset 400 derin
    txt(sz(-270.0), fy((k0 + k1) / 2) - 10, "KASET 400 × 360", f7, INK, "mm")
    txt(sz(-270.0), fy((k0 + k1) / 2) + 10, urun, f7, GRAY, "mm")
    d.rectangle([sz(-360.0), fy(h1), sz(-180.0), fy(h0)], fill=SOFT, outline=INK, width=1)          # nozul blogu
    txt(sz(-270.0), fy((h0 + h1) / 2), "NOZUL", f7, INK, "mm")
    d.rectangle([sz(-420.0), fy(m0 + 66.0), sz(-120.0), fy(m0 + 54.0)], fill=ACC, outline=ACC)      # taban o300 tepside
    txt(sz(-560.0), fy(m0 + 60.0), "TABAN Ø300", f7, ACC, "rm")
    d.rectangle([sz(-10.0), fy(m1), sz(40.0), fy(m0)], fill=AGZ, outline=RED, width=2)              # agiz kapagi
    d.rectangle([sz(-728.5), fy(m1), sz(-10.0), fy(m0)], fill=AGZ, outline=None)
    txt(sz(-620.0), fy((m0 + m1) / 2), "AĞIZ", f7, RED, "mm")
    d.rectangle([sz(-780.0), fy(k1 - 20), sz(-735.0), fy(k0 + 20)], fill=EVC, outline=BUZ, width=1)  # evaporator
d.rectangle([sz(-728.5), fy(1908.5), sz(0.0), fy(1670.0)], fill=SOFT, outline=LINE, width=1)
txt(sz(-364), fy(1790.0), "SOĞUTMA · evaporatör · fan", f7, GRAY, "mm")
olcu_h(sz(-790), sz(-728.5), fy(1970) - 26, "62,5", f7, INK)
olcu_h(sz(-470), sz(-70), fy(1970) - 60, "kaset 400", f8, INK)
olcu_h(sz(-790), sz(40), fy(0) + 44, "830", f11, INK)
# koridor + kaide + robot
d.line([(sz(40), fy(0)), (sz(40 + KOR + 120), fy(0))], fill=INK, width=3)
d.rectangle([sz(RZ - 200), fy(15.0), sz(RZ + 200), fy(0)], fill=SOFT, outline=ACC, width=2)
d.rectangle([sz(RZ - 100), fy(KAIDE), sz(RZ + 100), fy(15.0)], fill=BG, outline=ACC, width=3)
txt(sz(RZ), fy(KAIDE / 2), "KAİDE|Ø200 · 820", f7, ACC, "mm")
for w_, c_ in ((16, BG), (9, ACC)):
    d.line([(sz(RZ), fy(OMUZ)), (sz(RZ + 60), fy(1590.0)), (sz(-60.0), fy(1120.0))], fill=c_, width=w_, joint="curve")
d.ellipse([sz(RZ) - 18, fy(OMUZ) - 18, sz(RZ) + 18, fy(OMUZ) + 18], fill=ACC, outline=BG, width=2)
txt(sz(RZ + 180), fy(OMUZ), "OMUZ 1000", f8, ACC, "lm")
txt(sz(RZ + 120), fy(1620.0), "ROBOT · FR10 · 1400 mm · 10 kg", f8, ACC, "lm")
olcu_h(sz(40), sz(40 + KOR), fy(0) + 46, "KORİDOR 800", f8, INK)
olcu_v(sz(40 + KOR + 60), fy(KAIDE), fy(0), "820", f8, INK, "r")
for yy in (120.0, 430.0, 550.0, 680.0, 1040.0, 1050.0, 1170.0, 1300.0, 1660.0, 1970.0):
    d.line([(sz(-790) - 24, fy(yy)), (sz(-790) - 6, fy(yy))], fill=INK, width=2)
    txt(sz(-790) - 30, fy(yy), sayi(yy), f7, INK, "rm")


# ======================= YAN KESIT B · M5 PICKUP =======================
def sz2(z):
    return SX2 + (z + 790.0) * S


txt(SX2, FY_TOP - 190, "YAN KESİT B", f16, ACC)
txt(SX2, FY_TOP - 152, "M5 PICKUP · çift kapaklı QR gözü · arkası müşteri", f9, GRAY)
d.rectangle([sz2(-790), fy(1970), sz2(40), fy(0)], fill=FILL, outline=LINE, width=3)
d.rectangle([sz2(-790), fy(120), sz2(40), fy(0)], fill=SOFT, outline=LINE, width=2)
d.rectangle([sz2(-728.5), fy(1968.5), sz2(0.0), fy(1908.5)], fill=PUC, outline=GRAY, width=1)
d.rectangle([sz2(-728.5), fy(181.5), sz2(0.0), fy(121.5)], fill=PUC, outline=GRAY, width=1)
d.rectangle([sz2(-680.0), fy(332.5), sz2(0.0), fy(167.5)], fill=BG, outline=DOLAP, width=2)        # tatli cekmecesi
txt(sz2(-340.0), fy(250.0), "TATLI ÇEKMECESİ 680", f7, DOLAP, "mm")
d.rectangle([sz2(-728.5), fy(590.0), sz2(0.0), fy(340.0)], fill=SOFT, outline=LINE, width=1)
txt(sz2(-364.0), fy(465.0), "ISITMA PANOSU · kilitler", f7, GRAY, "mm")
for r in range(6):
    y0g = 600.0 + r * 200.0
    d.rectangle([sz2(-750.0), fy(y0g + 190.0), sz2(0.0), fy(y0g)], fill=BG, outline=INK, width=2)
    d.rectangle([sz2(-790.0), fy(y0g + 190.0), sz2(-752.0), fy(y0g)], fill=AGZ, outline=RED, width=1)   # musteri kapagi
    d.rectangle([sz2(0.0), fy(y0g + 190.0), sz2(40.0), fy(y0g)], fill=AGZ, outline=RED, width=1)         # robot kapagi
    d.line([(sz2(-700.0), fy(y0g + 30.0)), (sz2(-50.0), fy(y0g + 30.0))], fill=RED, width=2)              # isitici
txt(sz2(-375.0), fy(1195.0) - 10, "QR GÖZÜ 750 × 190", f8, INK, "mm")
txt(sz2(-375.0), fy(1195.0) + 12, "taban ısıtıcı 60 °C · kutu 320 × 320 × 45", f7, GRAY, "mm")
d.rectangle([sz2(-728.5), fy(1908.5), sz2(0.0), fy(1800.0)], fill=SOFT, outline=LINE, width=1)
txt(sz2(-364.0), fy(1855.0), "PANO", f7, GRAY, "mm")
txt(sz2(-790) - 14, fy(1195.0), "MÜŞTERİ KAPAĞI", f8, RED, "rm")
txt(sz2(40) + 14, fy(1195.0), "ROBOT KAPAĞI", f8, RED, "lm")
txt(sz2(-790) - 14, fy(1195.0) + 24, "cephe · sokak", f7, GRAY, "rm")
olcu_h(sz2(-750), sz2(0), fy(1970) - 60, "göz 750", f8, INK)
olcu_h(sz2(-790), sz2(40), fy(0) + 44, "830", f11, INK)
for yy in (120.0, 600.0, 1790.0, 1970.0):
    d.line([(sz2(40) + 6, fy(yy)), (sz2(40) + 24, fy(yy))], fill=INK, width=2)
    txt(sz2(40) + 30, fy(yy), sayi(yy), f8, INK, "lm")
d.line([(sz2(40), fy(0)), (sz2(40 + 300), fy(0))], fill=INK, width=3)

# ======================= PARCA LISTESI (sag alt) =======================
TX, TY = SX, PY_TOP - 120
txt(TX, TY - 60, "PARÇA LİSTESİ  ·  ana kalemler", f16, ACC)
PARCA = [
    ("ROBOT", "Fairino FR10 · 1.400 mm · 10 kg · ±0,05", "2", "kaide Ø200 × 820 · plaka 400 × 400"),
    ("ROBOT UCU", "takım değiştirici · pençe · tepsi eli", "2 set", "M1 uç istasyonu"),
    ("AKTARMA", "tepsi rafı · 6 tepsi Ø340 · altında çöp 60 L", "1", "koridor · x 2000–2400"),
    ("STORE", "soğutmalı çekmece 620 × 680 · motorlu", "24", "12 lahm · 8 pide · 3 içecek · 1 tatlı"),
    ("STORE", "soğutma grubu 1,5 HP + evaporatörler", "2", "M0 teknik bölme"),
    ("PRESS", "Fersah PZP-400 ısıtmalı pres başlığı", "1", "640 × 800 · platen Ø400 · 3,5 kW"),
    ("TOPPING", "standart kaset 140 × 400 × 360 · 14 L", "6", "harç ×4 · kıyma · kuşbaşı"),
    ("TOPPING", "kaşar kabı 280 × 400 × 360 · karıştırıcılı", "1", "28 L"),
    ("TOPPING", "sucuk dilimleyici · çubuk Ø38 şarjörü", "1", "14 çubuk / 2 gün"),
    ("TOPPING", "dozaj başlığı · piston pompa / vidalı", "8", "±%5"),
    ("OVEN", "kapaklı fırın haznesi 640 × 600 × 275", "3", "2 lahmacun 120 s · 1 pide 240 s"),
    ("OVEN", "yıldız kesici + yağ spreyi", "1", "M3 alt"),
    ("PACK", "kutu şarjörü + kutulama · blank 400 × 760", "1", "510–610 kutu"),
    ("PICKUP", "ısıtmalı QR gözü 380 × 190 × 750 · çift kapak", "12", "2 × 6"),
    ("KONTROL", "PLC + HMI · robot kontrol kutuları · panolar", "1", "M2 alt · M0 üst"),
]
kol = (0, 150, 720, 830)
th = 30
d.rectangle([TX, TY, TX + 1250, TY + th * (len(PARCA) + 1)], fill=BG, outline=LINE, width=2)
d.rectangle([TX, TY, TX + 1250, TY + th], fill=SOFT, outline=LINE, width=1)
for cx_, h_ in zip(kol, ("İSTASYON", "PARÇA", "ADET", "NOT")):
    txt(TX + cx_ + 10, TY + th / 2, h_, f8, INK, "lm")
for i, (a_, b_, c_, e_) in enumerate(PARCA):
    yy = TY + th * (i + 1)
    d.line([(TX, yy), (TX + 1250, yy)], fill=SOFT, width=1)
    for cx_, s_ in zip(kol, (a_, b_, c_, e_)):
        txt(TX + cx_ + 10, yy + th / 2, s_, f8 if cx_ != 830 else f7, INK if cx_ != 830 else GRAY, "lm")

# ======================= LEJANT =======================
d.line([(OX, H_PX - 130), (W_PX - 170, H_PX - 130)], fill=LINE, width=2)
ly = H_PX - 78
LEJ = [(LINE, BG, "kapak / panel", False), (RED, AGZ, "açık ağız · kapak", False), (DOLAP, BG, "çekmece +3 °C", False),
       (INK, SICAK, "fırın haznesi", False), (GRAY, PUC, "PU yalıtım", False), (INK, BG, "kapak arkası", True), (ACC, BG, "robot · aktarma", True)]
xx = OX
for c, fl, a_, kes in LEJ:
    if kes:
        drect(xx, ly - 12, xx + 30, ly + 12, c, 2)
    else:
        d.rectangle([xx, ly - 12, xx + 30, ly + 12], fill=fl, outline=c, width=3)
    txt(xx + 42, ly, a_, f9, INK, "lm")
    xx += 42 + d.textlength(a_, font=f9) + 56
cek = sum(g[0] for _, _, G, _ in MOD for g in G)
txt(W_PX - 170, ly, "HAT %s × 1970 × 830  ·  2 gün  ·  %d çekmece (12 lahmacun · 8 pide · 3 içecek · 1 tatlı)  ·  6 kaset + kaşar kabı + sucuk dilimleyici  ·  FIRIN 3 göz  ·  QR 12 göz  ·  2 × FR10" % (sayi(HAT), cek), f9, GRAY, "rm")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.save(OUT)
print("yazildi:", OUT, "· hat %s mm · %d cekmece" % (sayi(HAT), cek))
