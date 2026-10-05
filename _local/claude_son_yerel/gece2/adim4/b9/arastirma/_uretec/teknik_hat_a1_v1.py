# -*- coding: utf-8 -*-
"""AUTOKITCH - A1 YERLESIM v1 (16 Eyl 2026): iki sabit Fairino robot. UST GORUNUS x2 + ORTAK ON GORUNUS.
SECENEK 1: hamur FR5 (922) + paket FR5 WML (1900) · QR duvari duz, tek musteri cephesi.
SECENEK 2: hamur FR5 (922) + paket FR5 (922) · QR 6+6 iki yuze bolunmus, kose musteri cephesi.
Kural: paftada yalniz gorunus + olcu + parca adi; aciklama mesajda. Olculer mm.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE\HAT_A1_v1_teknik.png".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX = 5200, 2780
BG, INK, GRAY, LINE = (255, 255, 255), (26, 26, 28), (132, 132, 140), (72, 72, 78)
FILL, ACC, RED, SOFT = (246, 246, 248), (0, 86, 184), (198, 42, 32), (228, 228, 234)
DOLAP, SOGUK, FIRIN, HAVA, YUN = (14, 120, 90), (226, 238, 252), (200, 90, 30), (255, 225, 200), (250, 236, 210)
QRC, ICE = (240, 214, 170), (214, 226, 244)


def F(sz, b=False):
    for n in (("arialbd.ttf", "segoeuib.ttf") if b else ("arial.ttf", "segoeui.ttf")):
        try:
            return ImageFont.truetype(n, sz)
        except Exception:
            pass
    return ImageFont.load_default()


f7, f8, f9, f11, f13, f16, f30 = F(15), F(17), F(19), F(22), F(25), F(29, True), F(46, True)
im = Image.new("RGB", (W_PX, H_PX), BG)
d = ImageDraw.Draw(im)


def txt(x, y, s, f=f11, c=INK, a="la"):
    d.text((x, y), s, font=f, fill=c, anchor=a)


def sayi(v):
    return ("%g" % v).replace(".", ",")


def dline(p0, p1, c, w=1, dash=8, gap=5):
    (ax, ay), (bx, by) = p0, p1
    L = math.hypot(bx - ax, by - ay)
    if L < 1:
        return
    n = int(L // (dash + gap)) + 1
    for i in range(n):
        t0, t1 = min(1.0, i * (dash + gap) / L), min(1.0, (i * (dash + gap) + dash) / L)
        d.line([(ax + (bx - ax) * t0, ay + (by - ay) * t0), (ax + (bx - ax) * t1, ay + (by - ay) * t1)], fill=c, width=w)


def drect(x0, y0, x1, y1, c, w=1):
    dline((x0, y0), (x1, y0), c, w); dline((x1, y0), (x1, y1), c, w)
    dline((x1, y1), (x0, y1), c, w); dline((x0, y1), (x0, y0), c, w)


def dcircle(cx, cy, r, c, w=2, step=6):
    pts = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in range(0, 361, step)]
    for i in range(0, len(pts) - 1, 2):
        d.line([pts[i], pts[i + 1]], fill=c, width=w)


def ok(x0, y0, x1, y1, c, w=3):
    d.line([(x0, y0), (x1, y1)], fill=c, width=w)
    a = math.atan2(y1 - y0, x1 - x0)
    for s_ in (-0.5, 0.5):
        d.line([(x1, y1), (x1 - 15 * math.cos(a + s_), y1 - 15 * math.sin(a + s_))], fill=c, width=w)


def olcu_h(x0, x1, y, s, f=f9, c=INK):
    d.line([(x0, y), (x1, y)], fill=c, width=2)
    for xx in (x0, x1):
        d.line([(xx, y - 7), (xx, y + 7)], fill=c, width=2)
    tw = d.textlength(s, font=f)
    d.rectangle([(x0 + x1) / 2 - tw / 2 - 5, y - 12, (x0 + x1) / 2 + tw / 2 + 5, y + 12], fill=BG)
    txt((x0 + x1) / 2, y, s, f, c, "mm")


def olcu_v(x, y0, y1, s, f=f9, c=INK, yon="r"):
    d.line([(x, y0), (x, y1)], fill=c, width=2)
    for yy in (y0, y1):
        d.line([(x - 7, yy), (x + 7, yy)], fill=c, width=2)
    txt(x + (11 if yon == "r" else -11), (y0 + y1) / 2, s, f, c, "lm" if yon == "r" else "rm")


# ======================= VERI (mm) =======================
MOD = [("PRESS", 0.0, 670.0), ("TOPPING", 670.0, 1555.0), ("OVEN", 1555.0, 2975.0),
       ("KESME", 2975.0, 3475.0), ("PACK", 3475.0, 4175.0)]
DER = 830.0                      # istasyon derinligi
R1 = (335.0, -500.0)             # hamur robotu tabani
CEK = (620.0, 680.0)             # cekmece govdesi: genislik x derinlik
KOL = [("K1 · 6 PİDE + 5 LAHMACUN", -845.0, -810.0, -165.0, -190.0),
       ("K2 · 6 PİDE + 5 LAHMACUN", 835.0, -810.0, 1515.0, -190.0),
       ("K3 · 8 LAHMACUN", 25.0, -1680.0, 645.0, -1000.0)]
PRES_NOK = (335.0, 250.0)        # pres birakma noktasi

S1 = dict(robot=(3825.0, -700.0), r=1900.0, ad="FR5 WML · ERİŞİM 1900",
          qr=[(3255.0, -1750.0, 4395.0, -1300.0, "QR DOLABI · 12 GÖZ", 3)],
          ice=(4325.0, -1010.0, 4945.0, -390.0), kutu=(3825.0, 200.0),
          mus=[(3825.0, -2050.0, 3825.0, -1800.0)])
S2 = dict(robot=(3825.0, -650.0), r=922.0, ad="FR5 · ERİŞİM 922",
          qr=[(2875.0, -1030.0, 3325.0, -270.0, "QR · 6 GÖZ", 2),
              (4325.0, -1030.0, 4775.0, -270.0, "QR · 6 GÖZ", 2)],
          ice=(3515.0, -1830.0, 4135.0, -1150.0), kutu=(3825.0, 50.0),
          mus=[(2500.0, -650.0, 2790.0, -650.0), (5150.0, -650.0, 4860.0, -650.0)])

SC = 0.40                        # plan olcegi px/mm
SF = 0.42                        # on gorunus olcegi


def plan(OX, OY, cfg, baslik):
    def px(x, y):
        return (OX + x * SC, OY - y * SC)

    txt(OX - 845 * SC, OY - 830 * SC - 76, baslik, f16, ACC)

    # --- hat modulleri
    for ad, x0, x1 in MOD:
        a, b = px(x0, DER), px(x1, 0.0)
        c = HAVA if ad == "OVEN" else FILL
        d.rectangle([a[0], a[1], b[0], b[1]], fill=c, outline=LINE, width=2)
        txt((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, ad, f9, INK, "mm")
        olcu_h(a[0], b[0], OY - DER * SC - 34, sayi(x1 - x0))
    olcu_h(px(0, 0)[0], px(4175.0, 0)[0], OY - DER * SC - 78, "HAT 4175")
    olcu_v(px(4175.0, 0)[0] + 30, px(0, DER)[1], px(0, 0.0)[1], "830", yon="r")

    # --- hamur robotu hucresi
    rx, ry = px(*R1)
    dcircle(rx, ry, 922 * SC, (176, 196, 224), 2)
    txt(rx, ry - 922 * SC - 16, "FR5 · ERİŞİM 922", f8, ACC, "mm")
    for ad, x0, y0, x1, y1 in KOL:
        a, b = px(x0, y1), px(x1, y0)
        d.rectangle([a[0], a[1], b[0], b[1]], fill=SOGUK, outline=DOLAP, width=2)
        txt((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, ad, f8, DOLAP, "mm")
    # cekmece olculeri (K1)
    a, b = px(-845.0, -190.0), px(-165.0, -810.0)
    olcu_h(a[0], b[0], b[1] + 34, "680")
    olcu_v(a[0] - 30, a[1], b[1], "620", yon="l")
    # alma mesafesi
    p0, p1 = px(-165.0, -500.0), px(335.0, -500.0)
    d.line([p0, p1], fill=RED, width=2)
    olcu_h(p0[0], p1[0], p0[1] - 30, "500", f9, RED)
    p0, p1 = px(335.0, -1000.0), px(335.0, -500.0)
    olcu_h(0, 0, 0, "")  # no-op guard
    olcu_v(p0[0] + 26, p0[1], p1[1], "500", f9, RED)
    # hucre genisligi
    olcu_h(px(-845.0, 0)[0], px(1515.0, 0)[0], px(0, -1780.0)[1], "HÜCRE 2360")
    # pres birakma
    p = px(*PRES_NOK)
    d.ellipse([p[0] - 9, p[1] - 9, p[0] + 9, p[1] + 9], fill=RED)
    txt(p[0] + 14, p[1], "PRES BIRAKMA", f8, RED, "lm")
    # robot govdesi
    d.ellipse([rx - 74.5 * SC, ry - 74.5 * SC, rx + 74.5 * SC, ry + 74.5 * SC], fill=ACC, outline=INK, width=2)
    txt(rx, ry + 24, "ROBOT 1", f8, ACC, "ma")

    # --- paket robotu
    qx, qy = px(*cfg["robot"])
    dcircle(qx, qy, cfg["r"] * SC, (176, 196, 224), 2)
    txt(qx, qy - cfg["r"] * SC - 16, cfg["ad"], f8, ACC, "mm")
    for (x0, y0, x1, y1, ad, n) in cfg["qr"]:
        a, b = px(x0, y1), px(x1, y0)
        d.rectangle([a[0], a[1], b[0], b[1]], fill=QRC, outline=LINE, width=2)
        for k in range(1, n):
            xx = px(x0 + (x1 - x0) * k / n, 0)[0]
            d.line([(xx, a[1]), (xx, b[1])], fill=LINE, width=1)
        txt((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, ad, f8, INK, "mm")
    x0, y0, x1, y1 = cfg["ice"]
    a, b = px(x0, y1), px(x1, y0)
    d.rectangle([a[0], a[1], b[0], b[1]], fill=ICE, outline=DOLAP, width=2)
    txt((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, "İÇECEK · 4 ÇEKMECE", f8, DOLAP, "mm")
    p = px(*cfg["kutu"])
    d.ellipse([p[0] - 9, p[1] - 9, p[0] + 9, p[1] + 9], fill=RED)
    txt(p[0] + 14, p[1], "KUTU ALMA", f8, RED, "lm")
    d.ellipse([qx - 74.5 * SC, qy - 74.5 * SC, qx + 74.5 * SC, qy + 74.5 * SC], fill=ACC, outline=INK, width=2)
    txt(qx, qy + 24, "ROBOT 2", f8, ACC, "ma")
    for (mx0, my0, mx1, my1) in cfg["mus"]:
        a, b = px(mx0, my0), px(mx1, my1)
        ok(a[0], a[1], b[0], b[1], INK, 3)
        txt(a[0], a[1] + (18 if my0 == my1 else 0), "MÜŞTERİ", f8, INK, "mm" if my0 != my1 else "lm")


# ======================= PLANLAR =======================
txt(210, 96, "AUTOKITCH · A1 YERLEŞİM v1 · İKİ SABİT ROBOT", f30, INK)
txt(210, 158, "üst görünüş ×2  ·  ortak ön görünüş  ·  ölçüler mm  ·  16 Eylül 2026", f13, GRAY)

OY = 430 + 830 * SC
plan(210 + 845 * SC, OY, S1, "SEÇENEK 1  ·  HAMUR FR5 + PAKET FR5 WML")
plan(2760 + 845 * SC, OY, S2, "SEÇENEK 2  ·  HAMUR FR5 + PAKET FR5")

# ======================= ON GORUNUS (ortak, hamur hucresi) =======================
FX, FY = 430.0, 2560.0            # (x=0 mm, zemin) piksel


def fx(x):
    return FX + x * SF


def fy(z):
    return FY - z * SF


txt(FX - 220, fy(1915.0) - 96, "ORTAK ÖN GÖRÜNÜŞ  ·  HAMUR HÜCRESİ (K1 kolonu + robot + pres)", f16, ACC)
d.line([(FX - 260, FY), (fx(3400.0), FY)], fill=INK, width=3)
txt(FX - 260, FY + 16, "zemin", f8, GRAY, "la")

# K1 kolonu (0..620 mm genislik), cekmece bandi 600..1770
d.rectangle([fx(0), fy(1915.0), fx(620.0), FY], fill=FILL, outline=LINE, width=2)
z = 600.0
for i, (n, h, ad) in enumerate(((6, 108.0, "PİDE"), (5, 93.0, "LAHMACUN"))):
    for k in range(n):
        d.rectangle([fx(20.0), fy(z + h), fx(600.0), fy(z)], fill=SOGUK, outline=DOLAP, width=1)
        if k == 0:
            txt(fx(310.0), fy(z + h / 2), "%s ×%d" % (ad, n), f7, DOLAP, "mm")
        z += h
d.rectangle([fx(0), fy(1915.0), fx(620.0), fy(1800.0)], fill=SOFT, outline=LINE, width=1)
txt(fx(310.0), fy(1857.0), "SOĞUTMA", f7, GRAY, "mm")
olcu_v(fx(0) - 34, fy(1770.0), fy(600.0), "1170", yon="l")
olcu_v(fx(0) - 130, FY, fy(600.0), "600", yon="l")
olcu_v(fx(620.0) + 640, FY, fy(1915.0), "1915", yon="r")

# robot kaidesi + kol
KX = 620.0 + 500.0
d.rectangle([fx(KX - 130.0), fy(1215.0), fx(KX + 130.0), FY], fill=SOFT, outline=LINE, width=2)
txt(fx(KX), fy(600.0), "KAİDE", f8, GRAY, "mm")
d.ellipse([fx(KX - 75.0), fy(1290.0), fx(KX + 75.0), fy(1215.0)], fill=ACC, outline=INK, width=2)
d.line([(fx(KX), fy(1366.0)), (fx(KX + 430.0), fy(1720.0))], fill=ACC, width=9)
d.line([(fx(KX + 430.0), fy(1720.0)), (fx(KX + 860.0), fy(1400.0))], fill=ACC, width=9)
d.line([(fx(KX + 860.0), fy(1400.0)), (fx(KX + 860.0), fy(1245.0))], fill=ACC, width=7)
txt(fx(KX + 430.0), fy(1790.0), "FR5", f8, ACC, "mm")
dline((fx(KX - 300.0), fy(1366.0)), (fx(KX + 1000.0), fy(1366.0)), GRAY, 1)
olcu_v(fx(KX - 300.0) - 20, FY, fy(1366.0), "1366 OMUZ", yon="l")

# pres modulu
d.rectangle([fx(KX + 500.0), fy(1915.0), fx(KX + 1170.0), FY], fill=FILL, outline=LINE, width=2)
d.line([(fx(KX + 510.0), fy(1245.0)), (fx(KX + 1160.0), fy(1245.0))], fill=RED, width=3)
txt(fx(KX + 835.0), fy(1245.0) - 20, "PRES TABLASI 1245", f8, RED, "mm")
txt(fx(KX + 835.0), fy(700.0), "PRESS", f9, INK, "mm")
olcu_h(fx(KX - 130.0), fx(KX + 500.0), FY + 52, "500")
olcu_h(fx(0), fx(KX + 1170.0), FY + 108, "HÜCRE KESİTİ 2290")

# ======================= LEJANT =======================
LX, LY = 3400, 2180
kutular = ((SOGUK, DOLAP, "hamur çekmecesi (620 × 680)"), (QRC, LINE, "QR teslim gözü"),
           (ICE, DOLAP, "içecek çekmecesi"), (HAVA, LINE, "fırın"), (FILL, LINE, "istasyon modülü"))
for i, (fl, oc, ad) in enumerate(kutular):
    yy = LY + i * 46
    d.rectangle([LX, yy, LX + 44, yy + 30], fill=fl, outline=oc, width=2)
    txt(LX + 60, yy + 15, ad, f9, INK, "lm")
d.ellipse([LX + 6, LY + 5 * 46 + 4, LX + 38, LY + 5 * 46 + 36], fill=ACC, outline=INK, width=2)
txt(LX + 60, LY + 5 * 46 + 20, "robot (taban Ø149)", f9, INK, "lm")
d.ellipse([LX + 14, LY + 6 * 46 + 12, LX + 30, LY + 6 * 46 + 28], fill=RED)
txt(LX + 60, LY + 6 * 46 + 20, "bırakma / alma noktası", f9, INK, "lm")
dcircle(LX + 22, LY + 7 * 46 + 20, 16, (176, 196, 224), 2, 20)
txt(LX + 60, LY + 7 * 46 + 20, "robot erişim çemberi", f9, INK, "lm")

txt(W_PX - 210, H_PX - 150, "HAMUR: 12 PİDE + 18 LAHMACUN ÇEKMECESİ · 3 KOLON", f11, GRAY, "ra")
txt(W_PX - 210, H_PX - 118, "PAKET: 12 QR GÖZÜ + 4 İÇECEK ÇEKMECESİ", f11, GRAY, "ra")
txt(W_PX - 210, H_PX - 86, "HAT: PRESS · TOPPING · OVEN · KESME · PACK", f11, GRAY, "ra")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.save(OUT)
print("OK ->", OUT, im.size)
