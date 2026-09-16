# -*- coding: utf-8 -*-
"""AUTOKITCH - A1 YERLESIM v4 (16 Eyl 2026): iki sabit Fairino robot. UST GORUNUS x2 (alt alta) + ORTAK ON GORUNUS.
SECENEK 1: hamur FR5 (922) + paket FR5 WML (1900) · QR duvari duz, tek musteri cephesi.
SECENEK 2: hamur FR5 (922) + paket FR5 (922) · QR 6+6 iki yuze bolunmus, kose musteri cephesi.
v3'e gore: lejant asagi alindi, olcu cizgileri ayrildi, omuz olcusu saga tasindi.
Kural: paftada yalniz gorunus + olcu + parca adi; aciklama mesajda. Olculer mm.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE\HAT_A1_v4_teknik.png".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX = 5400, 3720
BG, INK, GRAY, LINE = (255, 255, 255), (26, 26, 28), (132, 132, 140), (72, 72, 78)
FILL, ACC, RED, SOFT = (246, 246, 248), (0, 86, 184), (198, 42, 32), (228, 228, 234)
DOLAP, SOGUK, HAVA, ERIS = (14, 120, 90), (226, 238, 252), (255, 225, 200), (205, 218, 236)
QRC, ICE = (240, 214, 170), (214, 226, 244)


def F(sz, b=False):
    for n in (("arialbd.ttf", "segoeuib.ttf") if b else ("arial.ttf", "segoeui.ttf")):
        try:
            return ImageFont.truetype(n, sz)
        except Exception:
            pass
    return ImageFont.load_default()


f8, f9, f11, f13, f16, f20, f34 = F(17), F(19), F(22), F(25), F(29, True), F(34, True), F(50, True)
im = Image.new("RGB", (W_PX, H_PX), BG)
d = ImageDraw.Draw(im)


def txt(x, y, s, f=f11, c=INK, a="la"):
    d.text((x, y), s, font=f, fill=c, anchor=a)


def sayi(v):
    return ("%g" % v).replace(".", ",")


def dline(p0, p1, c, w=1, dash=9, gap=6):
    (ax, ay), (bx, by) = p0, p1
    L = math.hypot(bx - ax, by - ay)
    if L < 1:
        return
    for i in range(int(L // (dash + gap)) + 1):
        t0, t1 = min(1.0, i * (dash + gap) / L), min(1.0, (i * (dash + gap) + dash) / L)
        d.line([(ax + (bx - ax) * t0, ay + (by - ay) * t0), (ax + (bx - ax) * t1, ay + (by - ay) * t1)], fill=c, width=w)


def dcircle(cx, cy, r, c, w=2, step=5):
    pts = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in range(0, 361, step)]
    for i in range(0, len(pts) - 1, 2):
        d.line([pts[i], pts[i + 1]], fill=c, width=w)


def ok(x0, y0, x1, y1, c, w=3):
    d.line([(x0, y0), (x1, y1)], fill=c, width=w)
    a = math.atan2(y1 - y0, x1 - x0)
    for s_ in (-0.5, 0.5):
        d.line([(x1, y1), (x1 - 16 * math.cos(a + s_), y1 - 16 * math.sin(a + s_))], fill=c, width=w)


def olcu_h(x0, x1, y, s, f=f9, c=INK):
    d.line([(x0, y), (x1, y)], fill=c, width=2)
    for xx in (x0, x1):
        d.line([(xx, y - 8), (xx, y + 8)], fill=c, width=2)
    tw = d.textlength(s, font=f)
    d.rectangle([(x0 + x1) / 2 - tw / 2 - 6, y - 13, (x0 + x1) / 2 + tw / 2 + 6, y + 13], fill=BG)
    txt((x0 + x1) / 2, y, s, f, c, "mm")


def olcu_v(x, y0, y1, s, f=f9, c=INK, yon="r"):
    d.line([(x, y0), (x, y1)], fill=c, width=2)
    for yy in (y0, y1):
        d.line([(x - 8, yy), (x + 8, yy)], fill=c, width=2)
    txt(x + (12 if yon == "r" else -12), (y0 + y1) / 2, s, f, c, "lm" if yon == "r" else "rm")


# ======================= VERI (mm) =======================
MOD = [("PRESS", 0.0, 670.0), ("TOPPING", 670.0, 1555.0), ("OVEN", 1555.0, 2975.0),
       ("KESME", 2975.0, 3475.0), ("PACK", 3475.0, 4175.0)]
DER = 830.0
R1 = (335.0, -500.0)
KOL = [("K1", "6 PİDE + 5 LAHMACUN", -845.0, -810.0, -165.0, -190.0),
       ("K2", "6 PİDE + 5 LAHMACUN", 835.0, -810.0, 1515.0, -190.0),
       ("K3", "8 LAHMACUN", 25.0, -1680.0, 645.0, -1000.0)]
PRES_NOK = (335.0, 250.0)

SEC = [dict(bas="SEÇENEK 1  ·  HAMUR FR5 (922)  +  PAKET FR5 WML (1900)", robot=(3825.0, -700.0), r=1900.0,
            ad="FR5 WML · ERİŞİM 1900",
            qr=[(3255.0, -1750.0, 4395.0, -1300.0, "QR DOLABI · 12 GÖZ (3 × 4)", 3)],
            ice=(4325.0, -1010.0, 4945.0, -390.0), kutu=(3825.0, 200.0),
            mus=[(3825.0, -2150.0, 3825.0, -1830.0, "mm")],
            ayak=(-845.0, -1750.0, 4945.0, 830.0, "TOPLAM AYAK İZİ 5790 × 2580")),
       dict(bas="SEÇENEK 2  ·  HAMUR FR5 (922)  +  PAKET FR5 (922)", robot=(3825.0, -650.0), r=922.0,
            ad="FR5 · ERİŞİM 922",
            qr=[(2875.0, -1030.0, 3325.0, -270.0, "QR · 6 GÖZ", 2),
                (4325.0, -1030.0, 4775.0, -270.0, "QR · 6 GÖZ", 2)],
            ice=(3515.0, -1830.0, 4135.0, -1150.0), kutu=(3825.0, 50.0),
            mus=[(2450.0, -650.0, 2790.0, -650.0, "rm"), (5200.0, -650.0, 4860.0, -650.0, "lm")],
            ayak=(-845.0, -1830.0, 5200.0, 830.0, "TOPLAM AYAK İZİ 6045 × 2660"))]

SC = 0.46
SF = 0.54


def plan(OX, OY, cfg):
    def px(x, y):
        return (OX + x * SC, OY - y * SC)

    txt(OX - 845 * SC, OY - DER * SC - 132, cfg["bas"], f20, ACC)

    # erisim cemberleri (acik ton, en altta)
    rx, ry = px(*R1)
    qx, qy = px(*cfg["robot"])
    dcircle(rx, ry, 922 * SC, ERIS, 2)
    dcircle(qx, qy, cfg["r"] * SC, ERIS, 2)

    # hat modulleri
    for ad, x0, x1 in MOD:
        a, b = px(x0, DER), px(x1, 0.0)
        d.rectangle([a[0], a[1], b[0], b[1]], fill=(HAVA if ad == "OVEN" else FILL), outline=LINE, width=2)
        txt((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, ad, f11, INK, "mm")
        olcu_h(a[0], b[0], OY - DER * SC - 36, sayi(x1 - x0))
    olcu_h(px(0, 0)[0], px(4175.0, 0)[0], OY - DER * SC - 84, "HAT 4175")
    olcu_v(px(4175.0, 0)[0] + 34, px(0, DER)[1], px(0, 0.0)[1], "830")

    # hamur hucresi
    for kod, ad, x0, y0, x1, y1 in KOL:
        a, b = px(x0, y1), px(x1, y0)
        d.rectangle([a[0], a[1], b[0], b[1]], fill=SOGUK, outline=DOLAP, width=2)
        txt((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 13, kod, f13, DOLAP, "mm")
        txt((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 15, ad, f9, DOLAP, "mm")
    a, b = px(-845.0, -190.0), px(-165.0, -810.0)
    olcu_h(a[0], b[0], b[1] + 40, "680")
    olcu_v(a[0] - 36, a[1], b[1], "620", yon="l")
    p0, p1 = px(-165.0, -500.0), px(335.0, -500.0)
    d.line([p0, p1], fill=RED, width=2)
    olcu_h(p0[0], p1[0], p0[1] - 34, "500", f9, RED)
    p0, p1 = px(335.0, -1000.0), px(335.0, -500.0)
    olcu_v(p0[0] + 30, p0[1], p1[1], "500", f9, RED)
    olcu_h(px(-845.0, 0)[0], px(1515.0, 0)[0], px(0, -1880.0)[1], "HAMUR HÜCRESİ 2360")
    p = px(*PRES_NOK)
    d.ellipse([p[0] - 10, p[1] - 10, p[0] + 10, p[1] + 10], fill=RED)
    txt(p[0] + 16, p[1], "PRES BIRAKMA", f9, RED, "lm")
    d.ellipse([rx - 74.5 * SC, ry - 74.5 * SC, rx + 74.5 * SC, ry + 74.5 * SC], fill=ACC, outline=INK, width=2)
    txt(rx, ry - 34, "ROBOT 1", f9, ACC, "mb")
    txt(rx + 16, ry + 20, "FR5 · 922", f8, ACC, "lt")

    # paket hucresi
    for (x0, y0, x1, y1, ad, n) in cfg["qr"]:
        a, b = px(x0, y1), px(x1, y0)
        d.rectangle([a[0], a[1], b[0], b[1]], fill=QRC, outline=LINE, width=2)
        for k in range(1, n):
            xx = px(x0 + (x1 - x0) * k / n, 0)[0]
            d.line([(xx, a[1]), (xx, b[1])], fill=LINE, width=1)
        txt((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, ad, f9, INK, "mm")
    x0, y0, x1, y1 = cfg["ice"]
    a, b = px(x0, y1), px(x1, y0)
    d.rectangle([a[0], a[1], b[0], b[1]], fill=ICE, outline=DOLAP, width=2)
    txt((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, "İÇECEK · 4 ÇEKMECE", f9, DOLAP, "mm")
    p = px(*cfg["kutu"])
    d.ellipse([p[0] - 10, p[1] - 10, p[0] + 10, p[1] + 10], fill=RED)
    txt(p[0] + 16, p[1], "KUTU ALMA", f9, RED, "lm")
    d.ellipse([qx - 74.5 * SC, qy - 74.5 * SC, qx + 74.5 * SC, qy + 74.5 * SC], fill=ACC, outline=INK, width=2)
    txt(qx, qy - 34, "ROBOT 2", f9, ACC, "mb")
    txt(qx, qy + 34, cfg["ad"].split(" · ")[0], f8, ACC, "mt")
    for (mx0, my0, mx1, my1, anc) in cfg["mus"]:
        a, b = px(mx0, my0), px(mx1, my1)
        ok(a[0], a[1], b[0], b[1], INK, 3)
        txt(a[0] + (0 if anc == "mm" else (-14 if anc == "rm" else 14)), a[1] + (16 if anc == "mm" else 0),
            "MÜŞTERİ", f9, INK, anc)
    ax0, ay0, ax1, ay1 = cfg["ayak"][:4]
    a, b = px(ax0, ay1), px(ax1, ay0)
    drect(a[0], a[1], b[0], b[1], (190, 190, 198), 1) if False else None
    olcu_h(a[0], b[0], b[1] + 132, cfg["ayak"][4], f11)


def drect(x0, y0, x1, y1, c, w=1):
    dline((x0, y0), (x1, y0), c, w); dline((x1, y0), (x1, y1), c, w)
    dline((x1, y1), (x0, y1), c, w); dline((x0, y1), (x0, y0), c, w)


# ======================= SAYFA =======================
txt(210, 92, "AUTOKITCH · A1 YERLEŞİM v4 · İKİ SABİT ROBOT", f34, INK)
txt(210, 152, "üst görünüş ×2  ·  ortak ön görünüş  ·  ölçüler mm  ·  16 Eylül 2026", f13, GRAY)

OX0 = 210 + 845 * SC
plan(OX0, 560 + DER * SC, SEC[0])
plan(OX0, 2120 + DER * SC, SEC[1])

# ======================= ON GORUNUS =======================
FX, FY = 3560.0, 2500.0


def fx(x):
    return FX + x * SF


def fy(z):
    return FY - z * SF


txt(FX - 120, fy(1915.0) - 150, "ORTAK ÖN GÖRÜNÜŞ  ·  HAMUR HÜCRESİ", f20, ACC)
txt(FX - 120, fy(1915.0) - 106, "K1 kolonu  ·  robot kaidesi  ·  pres", f11, GRAY)
d.line([(FX - 160, FY), (fx(2400.0), FY)], fill=INK, width=3)
txt(FX - 160, FY + 18, "zemin", f9, GRAY, "la")

d.rectangle([fx(0), fy(1915.0), fx(620.0), FY], fill=FILL, outline=LINE, width=2)
d.rectangle([fx(0), fy(1915.0), fx(620.0), fy(1800.0)], fill=SOFT, outline=LINE, width=1)
txt(fx(310.0), fy(1857.0), "SOĞUTMA", f8, GRAY, "mm")
z = 600.0
for n, h, ad in ((6, 108.0, "PİDE ×6"), (5, 93.0, "LAHMACUN ×5")):
    z0 = z
    for k in range(n):
        d.rectangle([fx(24.0), fy(z + h), fx(596.0), fy(z)], fill=SOGUK, outline=DOLAP, width=1)
        z += h
    txt(fx(310.0), (fy(z0) + fy(z)) / 2, ad, f9, DOLAP, "mm")
olcu_v(fx(0) - 40, fy(1770.0), fy(600.0), "ERİŞİM BANDI 1170", yon="l")
olcu_v(fx(0) - 190, FY, fy(600.0), "600", yon="l")

KX = 1120.0
d.rectangle([fx(KX - 130.0), fy(1215.0), fx(KX + 130.0), FY], fill=SOFT, outline=LINE, width=2)
txt(fx(KX), fy(700.0), "KAİDE", f9, GRAY, "mm")
d.ellipse([fx(KX - 75.0), fy(1300.0), fx(KX + 75.0), fy(1215.0)], fill=ACC, outline=INK, width=2)
d.line([(fx(KX), fy(1366.0)), (fx(KX + 350.0), fy(1780.0))], fill=ACC, width=11)
d.line([(fx(KX + 350.0), fy(1780.0)), (fx(KX + 835.0), fy(1430.0))], fill=ACC, width=11)
d.line([(fx(KX + 835.0), fy(1430.0)), (fx(KX + 835.0), fy(1310.0))], fill=ACC, width=8)
d.rectangle([fx(KX + 790.0), fy(1310.0), fx(KX + 880.0), fy(1265.0)], fill=ACC, outline=INK, width=2)
txt(fx(KX + 350.0), fy(1850.0), "FR5", f11, ACC, "mm")
dline((fx(KX - 260.0), fy(1366.0)), (fx(KX + 980.0), fy(1366.0)), GRAY, 1)
dline((fx(KX + 980.0), fy(1366.0)), (fx(KX + 1330.0), fy(1366.0)), GRAY, 1)
olcu_v(fx(KX + 1290.0), FY, fy(1366.0), "OMUZ 1366", yon="r")

d.rectangle([fx(KX + 500.0), fy(1915.0), fx(KX + 1170.0), FY], fill=FILL, outline=LINE, width=2)
d.line([(fx(KX + 510.0), fy(1245.0)), (fx(KX + 1160.0), fy(1245.0))], fill=RED, width=3)
txt(fx(KX + 835.0), fy(1245.0) + 26, "PRES TABLASI 1245", f9, RED, "mm")
txt(fx(KX + 835.0), fy(700.0), "PRESS", f11, INK, "mm")
olcu_v(fx(KX + 1170.0) + 250, FY, fy(1915.0), "1915")
olcu_h(fx(KX - 130.0), fx(KX + 500.0), FY + 54, "500")
olcu_h(fx(0), fx(KX + 1170.0), FY + 112, "KESİT 2290")

# ======================= LEJANT =======================
LX, LY = 210, 3530
for i, (fl, oc, ad) in enumerate(((SOGUK, DOLAP, "hamur çekmecesi 620 × 680"), (QRC, LINE, "QR teslim gözü"),
                                  (ICE, DOLAP, "içecek çekmecesi"), (HAVA, LINE, "fırın"),
                                  (FILL, LINE, "istasyon modülü"))):
    xx = LX + i * 560
    d.rectangle([xx, LY, xx + 46, LY + 32], fill=fl, outline=oc, width=2)
    txt(xx + 62, LY + 16, ad, f9, INK, "lm")
d.ellipse([LX + 8, LY + 52, LX + 40, LY + 84], fill=ACC, outline=INK, width=2)
txt(LX + 62, LY + 68, "robot · taban Ø149", f9, INK, "lm")
d.ellipse([LX + 576, LY + 60, LX + 596, LY + 80], fill=RED)
txt(LX + 622, LY + 68, "bırakma / alma noktası", f9, INK, "lm")
dcircle(LX + 1140, LY + 68, 17, ERIS, 2, 18)
txt(LX + 1182, LY + 68, "robot erişim çemberi", f9, INK, "lm")
txt(LX + 1680, LY + 68, "HAMUR: 12 PİDE + 18 LAHMACUN ÇEKMECESİ · 3 KOLON · PAKET: 12 QR GÖZÜ + 4 İÇECEK ÇEKMECESİ", f9, GRAY, "lm")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.save(OUT)
print("OK ->", OUT, im.size)
