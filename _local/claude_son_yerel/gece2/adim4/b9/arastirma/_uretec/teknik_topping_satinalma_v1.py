# -*- coding: utf-8 -*-
"""TOPPING · SATIN ALMA ÜRÜNLERİYLE YERLEŞİM v1 — ÖN + ÜST (öneri pafta) · 25 Eyl 2026

Kemal: "tüm toppingi yap, teknik resim yeni sistemle: rende bizim kaset, sonra ne varsa onlar için kullanacağımız ürünün
yerleşimini yap, bakalım sığıyor mu, ne taşıyor; haznelerini bize göre büyüt ya da küçük seç."
Sıra (soldan, tabla yönünde): SOS (Mini-fill 15 L) · HARÇ (UNO çekirdeği + bizim 45 L) · KIYMA / KUŞBAŞI (Mini-fill 8 L)
· KAŞAR (bizim kaset 280) · KÜP SUCUK (Mini-fill 8 L). Mini-fill'ler 90° çevrik (ön yüzü +x), gövde tabla yolunun
üstünde, hazne soğuk hücrede. Hazne seçimi 2 günlük ihtiyaçtan (stok kuralı): kıyma 6,1 L · kuşbaşı 6,8 L · sucuk 3,7 L
→ 8 L; harç 41,1 L → 45 L bizim. Ölçüler: topping_hesap_v6, pafta v8, beldos_cad_v1, teknik_sos_bolmesi_v1.
"""
import math, os
from PIL import Image, ImageDraw, ImageFont

U = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.dirname(os.path.dirname(U))
CIKTI = os.path.join(KOK, "arastirma", "FULL_MAKINE", "TOPPING_SATINALMA_v1_teknik.png")

Y0, YUST = 1060.0, 2030.0
AGIZ_R = (1070.0, 1180.0); TEKNE = (1061.5, 1091.5); DISK = (1154.0, 1168.0); PIDE = (1168.0, 1176.0)
UC = 1184.0; ZT = -170.0; DUVAR = 90.0; W_BUGUN = 1800.0
SOGUK_TABAN = 1320.0; YAL_TABAN = (1183.0, 1317.0); TAVAN_IC = YUST - 62.0
MF_ALT, MF_UST = 1196.0, 1413.0; HZ0 = MF_ALT + 135.0; MF_YAL = (1424.0, 1484.0)
P15 = [(34, 77), (34, 98.3), (113, 143.7), (121, 152), (126, 163), (128, 177.8), (128, 478), (129.5, 478), (129.5, 488), (45, 488), (30, 494), (0, 495.5)]
P8 = [(34, 77), (34, 89), (36, 89.6), (126.5, 261), (128, 262), (128, 362), (129.5, 362), (129.5, 368), (45, 368), (30, 374), (0, 376)]
GAP = 20.0

# ---- dizilim (x, soldan) ----
DIZI = [("SOS", "mf", P15, "Mini-fill · 15 L"), ("HARÇ", "uno", None, "UNO + bizim 45 L"), ("KIYMA", "mf", P8, "Mini-fill · 8 L"),
        ("KUŞBAŞI", "mf", P8, "Mini-fill · 8 L"), ("KAŞAR", "kaset", None, "bizim rende kaseti"), ("KÜP SUCUK", "mf", P8, "Mini-fill · 8 L")]
YER = []
x = DUVAR + GAP
for ad, tip, prof, alt in DIZI:
    w = {"mf": 296.0 + 72.0, "uno": 460.0, "kaset": 282.0}[tip]
    YER.append(dict(ad=ad, tip=tip, prof=prof, alt=alt, x0=x, x1=x + w))
    x += w + GAP
W_GEREK = x + DUVAR
TASMA = W_GEREK - W_BUGUN

S = 0.95
XA, XB = -40.0, W_GEREK + 40
FA, FB = 1040.0, 2050.0
ML, MR, MT = 290, 330, 210
W = int(ML + (XB - XA) * S + MR); FH = int((FB - FA) * S); TH = int(845 * S)
H = int(MT + FH + 230 + TH + 190)
FX = lambda x: ML + (x - XA) * S
FY = lambda y: MT + (FB - y) * S
PT = MT + FH + 230
TZ = lambda z: PT + (z + 835.0) * S

INK, GRI, ACIK = (25, 25, 28), (120, 124, 130), (205, 208, 212)
F_BEL, F_BIZ, F_SOG, F_YAL, KIR = (228, 231, 236), (214, 230, 250), (236, 245, 252), (238, 238, 238), (200, 30, 30)
MAVI = (30, 90, 170)
im = Image.new("RGB", (W, H), (255, 255, 255)); d = ImageDraw.Draw(im)
fn = lambda n, b=False: ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf" if b else "C:/Windows/Fonts/arial.ttf", n)
f_bas, f_gor, f_et, f_ol, f_ad = fn(38, True), fn(28, True), fn(19), fn(18), fn(22, True)


def kesik(p0, p1, renk=INK, w=2, a=12, b=7):
    (x0, y0), (x1, y1) = p0, p1; L = math.hypot(x1 - x0, y1 - y0)
    if L < 1: return
    ux, uy = (x1 - x0) / L, (y1 - y0) / L; t = 0.0
    while t < L:
        t1 = min(L, t + a); d.line([(x0 + ux * t, y0 + uy * t), (x0 + ux * t1, y0 + uy * t1)], fill=renk, width=w); t = t1 + b


def kutu(x0, x1, y0, y1, fill=None, renk=INK, w=2, gizli=False):
    X0, X1 = sorted((x0, x1)); A, B = sorted((y0, y1))
    if fill: d.rectangle([X0, A, X1, B], fill=fill)
    if gizli:
        for p, q in (((X0, A), (X1, A)), ((X1, A), (X1, B)), ((X1, B), (X0, B)), ((X0, B), (X0, A))): kesik(p, q, renk, w)
    elif renk: d.rectangle([X0, A, X1, B], outline=renk, width=w)


def tarali(x0, x1, y0, y1, adim=11):
    X0, X1 = sorted((x0, x1)); A, B = sorted((y0, y1))
    d.rectangle([X0, A, X1, B], fill=F_YAL); k = X0 - (B - A)
    while k < X1:
        p = max(k, X0); q = min(k + (B - A), X1)
        d.line([(p, B - (p - k)), (q, B - (q - k))], fill=ACIK, width=1); k += adim
    d.rectangle([X0, A, X1, B], outline=GRI, width=1)


def cember(cx, cy, r, renk=INK, w=2, gizli=False, fill=None):
    if fill: d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
    if gizli:
        n = max(24, int(r / 3))
        for i in range(0, n, 2):
            a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
            d.line([(cx + r * math.cos(a0), cy + r * math.sin(a0)), (cx + r * math.cos(a1), cy + r * math.sin(a1))], fill=renk, width=w)
    else: d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=renk, width=w)


def ok(x, y, dx, dy, renk=INK):
    L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
    d.polygon([(x, y), (x - ux * 14 - uy * 5, y - uy * 14 + ux * 5), (x - ux * 14 + uy * 5, y - uy * 14 - ux * 5)], fill=renk)


def olcu_x(y, x0, x1, t, renk=INK):
    d.line([(x0, y), (x1, y)], fill=renk, width=2); ok(x0, y, -1, 0, renk); ok(x1, y, 1, 0, renk)
    tw = d.textlength(t, font=f_ol)
    d.rectangle([(x0 + x1) / 2 - tw / 2 - 4, y - 23, (x0 + x1) / 2 + tw / 2 + 4, y - 3], fill=(255, 255, 255))
    d.text(((x0 + x1) / 2 - tw / 2, y - 23), t, font=f_ol, fill=renk)


def kot(y_mm, t, yt=None):
    y = FY(y_mm); yt = y if yt is None else yt
    d.line([(FX(XA) - 8, y), (FX(XA) + 4, y)], fill=GRI, width=2)
    if yt != y: d.line([(FX(XA) - 12, yt), (FX(XA) - 8, y)], fill=GRI, width=1)
    tw = d.textlength(t, font=f_ol); d.text((FX(XA) - 16 - tw, yt - 10), t, font=f_ol, fill=INK)


def ortala(t, cx, y, font, renk=INK):
    tw = d.textlength(t, font=font); d.text((cx - tw / 2, y), t, font=font, fill=renk)


# ================================================================ başlık
d.text((ML, 40), "TOPPING · SATIN ALMA ÜRÜNLERİYLE YERLEŞİM v1 — ÖN + ÜST GÖRÜNÜŞ (öneri)", font=f_bas, fill=INK)
d.text((ML, 94), "ölçüler mm · kotlar yerden · x: modül C'nin sol ucundan · z: modülün ön yüzünden (arkaya −) · Beldos ölçüleri broşürden · hazneler 2 günlük ihtiyaca göre",
       font=f_et, fill=GRI)

# ================================================================ ÖN GÖRÜNÜŞ
d.text((ML, MT - 44), "ÖN GÖRÜNÜŞ", font=f_gor, fill=INK)
kutu(FX(0), FX(W_GEREK), FY(Y0), FY(YUST), renk=INK, w=3)
tarali(FX(0), FX(DUVAR), FY(Y0), FY(YUST)); tarali(FX(W_GEREK - DUVAR), FX(W_GEREK), FY(Y0), FY(YUST))
tarali(FX(DUVAR), FX(W_GEREK - DUVAR), FY(TAVAN_IC), FY(YUST - 1.5))
kutu(FX(DUVAR), FX(W_GEREK - DUVAR), FY(TEKNE[0]), FY(TEKNE[1]), fill=F_YAL, renk=GRI, w=1)
for y in AGIZ_R: kesik((FX(DUVAR), FY(y)), (FX(W_GEREK - DUVAR), FY(y)), GRI, 1)
# bugünkü modül sonu
kesik((FX(W_BUGUN), FY(Y0) + 40), (FX(W_BUGUN), FY(YUST) - 30), KIR, 3)
ortala("bugünkü modül C sonu (1800)", FX(W_BUGUN), FY(YUST) - 60, f_et, KIR)

for u in YER:
    x0, x1 = u["x0"], u["x1"]; cx = (x0 + x1) / 2
    if u["tip"] == "mf":
        bx0, bx1 = x0, x0 + 296.0; ax = bx1 + 45.0; hx = bx1 - 119.0
        # soğuk taban yalıtımı (hazne boynu geçer) + soğuk hacim
        kutu(FX(x0 - GAP / 2), FX(x1 + GAP / 2), FY(MF_YAL[1]), FY(TAVAN_IC), fill=F_SOG, renk=None)
        tarali(FX(x0 - GAP / 2), FX(hx - 118), FY(MF_YAL[0]), FY(MF_YAL[1])); tarali(FX(hx + 118), FX(x1 + GAP / 2), FY(MF_YAL[0]), FY(MF_YAL[1]))
        kutu(FX(bx0), FX(bx1), FY(MF_ALT + 17), FY(MF_UST), fill=F_BEL, renk=INK, w=2)
        kutu(FX(bx0 + 4), FX(bx1 - 4), FY(MF_ALT + 17), FY(MF_ALT + 45), fill=(60, 60, 64), renk=INK, w=1)
        for xx in (bx0 + 30, bx1 - 30): kutu(FX(xx - 15), FX(xx + 15), FY(MF_ALT), FY(MF_ALT + 17), fill=(60, 60, 64), renk=INK, w=1)
        kutu(FX(bx1 - 157), FX(bx1 - 9), FY(HZ0), FY(HZ0 + 77), fill=(225, 238, 246), renk=MAVI, w=2)
        pts = [(FX(hx + r), FY(HZ0 + z)) for r, z in u["prof"]] + [(FX(hx - r), FY(HZ0 + z)) for r, z in reversed(u["prof"])]
        d.polygon(pts, fill=(247, 247, 247)); d.line(pts + [pts[0]], fill=INK, width=2)
        py = MF_ALT + 197.8
        kutu(FX(bx1 - 9), FX(bx1 + 14), FY(py - 19.5), FY(py + 19.5), fill=(225, 238, 246), renk=MAVI, w=2)
        kutu(FX(bx1 + 14), FX(ax + 10), FY(py - 10), FY(py + 10), fill=F_BEL, renk=INK, w=2)
        kutu(FX(ax - 10), FX(ax + 10), FY(UC + 40), FY(py + 10), fill=F_BEL, renk=INK, w=2)
        d.polygon([(FX(ax - 10), FY(UC + 40)), (FX(ax + 10), FY(UC + 40)), (FX(ax + 25), FY(UC)), (FX(ax - 25), FY(UC))], fill=F_BEL, outline=INK)
        u["ax"] = ax; u["hx"] = hx; u["ust"] = HZ0 + u["prof"][-1][1]
    elif u["tip"] == "uno":
        ux = x0 + 230.0; u["ax"] = ux
        tarali(FX(x0 - GAP / 2), FX(x1 + GAP / 2), FY(YAL_TABAN[0]), FY(YAL_TABAN[1]))
        kutu(FX(x0 - GAP / 2), FX(x1 + GAP / 2), FY(SOGUK_TABAN), FY(TAVAN_IC), fill=F_SOG, renk=None)
        kutu(FX(ux - 41), FX(ux + 41), FY(SOGUK_TABAN), FY(SOGUK_TABAN + 72.6), fill=F_BEL, renk=INK, w=2)
        kutu(FX(ux - 66), FX(ux - 41), FY(1338.5), FY(1378.5), fill=(60, 60, 64), renk=INK, w=1)
        kutu(FX(ux + 41), FX(ux + 91), FY(1336.5), FY(1380.5), fill=F_BIZ, renk=MAVI, w=2)
        cember(FX(ux), FY(1358.5), 29.5 * S, fill=F_BEL)
        kutu(FX(ux - 18), FX(ux + 18), FY(UC + 40), FY(1340), fill=F_BEL, renk=INK, w=2)
        d.polygon([(FX(ux - 18), FY(UC + 40)), (FX(ux + 18), FY(UC + 40)), (FX(ux + 25), FY(UC)), (FX(ux - 25), FY(UC))], fill=F_BEL, outline=INK)
        kutu(FX(ux - 32), FX(ux + 32), FY(1392.6), FY(1452), fill=F_BEL, renk=INK, w=2)
        hp = [(FX(ux - 32), FY(1452)), (FX(ux + 32), FY(1452)), (FX(ux + 220), FY(1632)), (FX(ux + 220), FY(1832)), (FX(ux - 220), FY(1832)), (FX(ux - 220), FY(1632))]
        d.polygon(hp, fill=F_BIZ); d.line(hp + [hp[0]], fill=MAVI, width=3)
        u["ust"] = 1832.0
    else:
        ux = (x0 + x1) / 2; u["ax"] = ux
        tarali(FX(x0 - GAP / 2), FX(x1 + GAP / 2), FY(YAL_TABAN[0]), FY(YAL_TABAN[1]))
        kutu(FX(x0 - GAP / 2), FX(x1 + GAP / 2), FY(SOGUK_TABAN), FY(TAVAN_IC), fill=F_SOG, renk=None)
        kutu(FX(x0 + 1), FX(x1 - 1), FY(SOGUK_TABAN + 10), FY(SOGUK_TABAN + 370), fill=(250, 244, 222), renk=INK, w=2)
        kutu(FX(ux - 22), FX(ux + 22), FY(UC + 32), FY(SOGUK_TABAN + 10), fill=F_BEL, renk=INK, w=2)
        u["ust"] = SOGUK_TABAN + 370
    ortala(u["ad"], FX(u["ax"] if u["tip"] != "mf" else (x0 + x1) / 2), FY(TAVAN_IC) + 14, f_ad)
    ortala(u["alt"], FX(u["ax"] if u["tip"] != "mf" else (x0 + x1) / 2), FY(TAVAN_IC) + 44, f_et, MAVI if u["tip"] != "mf" else GRI)
# tabla (ilk durakta)
t0 = YER[0]["ax"]
kutu(FX(t0 - 170), FX(t0 + 170), FY(DISK[0]), FY(DISK[1]), fill=(250, 226, 196), renk=INK, w=2)
kutu(FX(t0 - 140), FX(t0 + 140), FY(PIDE[0]), FY(PIDE[1]), fill=(240, 200, 150), renk=INK, w=1)
# kotlar
for y, t in [(Y0, "1060"), (SOGUK_TABAN, "1320 soğuk taban"), (MF_UST, "1413 Mini-fill üstü"), (1707.0, "1707 8 L hazne"), (TAVAN_IC, "1968 tavan"), (YUST, "2030")]:
    kot(y, t)
kot(1832.0, "1832 harç haznesi", FY(1832.0) - 12); kot(1826.5, "1826 15 L hazne", FY(1826.5) + 14)
yb = FY(MF_ALT) - 40
for i, (y, t) in enumerate([(MF_ALT, "1196 Mini-fill altı"), (UC, "1184 ağız ucu"), (AGIZ_R[1], "1180 robot ağzı"), (PIDE[1], "1176 pide üstü"), (DISK[1], "1168 süreç")]):
    kot(y, t, yb + i * 26)
# alt ölçüler
yb = FY(FA) + 30
for u in YER:
    olcu_x(yb, FX(u["x0"]), FX(u["x1"]), "%.0f" % (u["x1"] - u["x0"]))
olcu_x(yb + 44, FX(0), FX(W_BUGUN), "bugünkü modül C 1800")
olcu_x(yb + 88, FX(0), FX(W_GEREK), "gereken %.0f" % W_GEREK)
olcu_x(yb + 132, FX(W_BUGUN), FX(W_GEREK), "taşma %.0f" % TASMA, KIR)

# ================================================================ ÜST GÖRÜNÜŞ
d.text((ML, PT - 44), "ÜST GÖRÜNÜŞ", font=f_gor, fill=INK)
kutu(FX(0), FX(W_GEREK), TZ(0), TZ(-830), renk=INK, w=3)
tarali(FX(0), FX(DUVAR), TZ(-830), TZ(0)); tarali(FX(W_GEREK - DUVAR), FX(W_GEREK), TZ(-830), TZ(0))
for z in (-84.0, -104.0, -565.0, -630.0): d.line([(FX(DUVAR), TZ(z)), (FX(W_GEREK - DUVAR), TZ(z))], fill=ACIK, width=1)
kesik((FX(W_BUGUN), TZ(-830) - 10), (FX(W_BUGUN), TZ(0) + 10), KIR, 3)
x = FX(DUVAR)
while x < FX(W_GEREK - DUVAR):
    d.line([(x, TZ(ZT)), (min(x + 22, FX(W_GEREK - DUVAR)), TZ(ZT))], fill=GRI, width=2); x += 32
for u in YER:
    x0, x1 = u["x0"], u["x1"]
    if u["tip"] == "mf":
        bx1 = x0 + 296.0
        kutu(FX(x0), FX(bx1), TZ(-100.0), TZ(-577.0), fill=F_BEL, renk=INK, w=2)
        kutu(FX(bx1 - 157), FX(bx1 - 9), TZ(-162.0), TZ(-311.0), fill=(225, 238, 246), renk=MAVI, w=1)
        kutu(FX(bx1 - 189), FX(bx1 - 55), TZ(-375.0), TZ(-559.0), fill=(200, 200, 204), renk=INK, w=1)
        r = 128.0
        cember(FX(u["hx"]), TZ(-236.5), r * S, gizli=True)
        d.line([(FX(bx1 + 10), TZ(-236.5)), (FX(u["ax"]), TZ(ZT))], fill=INK, width=int(20 * S))
        kutu(FX(u["ax"] - 25), FX(u["ax"] + 25), TZ(ZT + 4), TZ(ZT - 4), fill=INK, renk=INK, w=1)
    elif u["tip"] == "uno":
        ux = u["ax"]
        tarali(FX(x0 - GAP / 2), FX(x1 + GAP / 2), TZ(-565.0), TZ(-630.0))
        kutu(FX(ux - 220), FX(ux + 220), TZ(-120.0), TZ(-560.0), renk=MAVI, w=2, gizli=True)
        kutu(FX(ux - 41), FX(ux + 41), TZ(-346.0), TZ(-428.0), fill=F_BEL, renk=INK, w=2)
        kutu(FX(ux + 41), FX(ux + 91), TZ(-362.0), TZ(-412.0), fill=F_BIZ, renk=MAVI, w=2)
        kutu(FX(ux - 18), FX(ux + 18), TZ(-346.0), TZ(ZT - 18), fill=F_BEL, renk=INK, w=2)
        kutu(FX(ux - 29), FX(ux + 29), TZ(-428.0), TZ(-559.0), fill=(232, 236, 242), renk=INK, w=2)
        kutu(FX(ux - 30), FX(ux + 30), TZ(-640.0), TZ(-820.0), fill=F_BIZ, renk=MAVI, w=2)
        kutu(FX(ux - 25), FX(ux + 25), TZ(ZT + 4), TZ(ZT - 4), fill=INK, renk=INK, w=1)
    else:
        ux = u["ax"]
        tarali(FX(x0 - GAP / 2), FX(x1 + GAP / 2), TZ(-565.0), TZ(-630.0))
        kutu(FX(x0 + 1), FX(x1 - 1), TZ(-200.0), TZ(-525.0), fill=(250, 244, 222), renk=INK, w=2)
        kutu(FX(ux - 22), FX(ux + 22), TZ(-116.0), TZ(-200.0), fill=F_BEL, renk=INK, w=2)
        for dx in (-60.0, 60.0): kutu(FX(ux + dx - 29), FX(ux + dx + 29), TZ(-640.0), TZ(-796.0), fill=F_BIZ, renk=MAVI, w=1)
    ortala(u["ad"], FX((x0 + x1) / 2), TZ(0) + 14, f_ad)
cember(FX(t0), TZ(ZT), 170 * S, renk=(200, 140, 70), w=2)
xr = FX(W_GEREK) + 16
for z, t in [(0, "0 ön yüz"), (ZT, "−170 tabla ekseni"), (-565, "−565"), (-630, "−630"), (-830, "−830")]:
    d.line([(FX(W_GEREK) + 2, TZ(z)), (xr, TZ(z))], fill=GRI, width=1); d.text((xr + 4, TZ(z) - 10), t, font=f_ol, fill=INK)

os.makedirs(os.path.dirname(CIKTI), exist_ok=True)
im.save(CIKTI, optimize=True)
print("PNG", CIKTI, im.size)
for u in YER: print("  %-10s x %.0f–%.0f  ağız x %.0f  üst %.0f" % (u["ad"], u["x0"], u["x1"], u["ax"], u["ust"]))
print("gereken %.0f · bugünkü 1800 · taşma %.0f" % (W_GEREK, TASMA))
