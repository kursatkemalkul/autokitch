# -*- coding: utf-8 -*-
"""TOPPING · MONTAJ PAFTASI v2 — UNO ÇEKİRDEKLİ İSTASYONLAR + BİZİM KASETLER (öneri) · 25 Eyl 2026

Kemal: "küp sucuk ve kaşar dışındakileri UNO ile kur; hazneleri farklı, çıkışları farklı, birbirine bağlama; bizim
paftaya adapte et. Kaşar ve sucuk bizim. Tüm montajın olduğu pafta."
Sıra (soldan, tabla yönünde): SOS · HARÇ · KIYMA · KUŞBAŞI (her biri ayrı UNO çekirdeği: Beldos valf + ürün silindiri,
bizim soğuk hazne, bizim step tahrik, kendi ağzı) · KAŞAR (bizim rende kaseti 280) · KÜP SUCUK (bizim kaset 140).
Hazneler 2 günlük: harç 43,2 kg → 45 L · kıyma 6,1 L → 8 L · kuşbaşı 6,8 L → 8 L · sos 15 L VARSAYIM (günlük miktar yok).
Ölçü kaynakları: topping_hesap_v6 (zonlar, tabla ekseni z −170), pafta v8 (süreç 1168), beldos_cad_v1 (UNO ölçüleri).
"""
import math, os
from PIL import Image, ImageDraw, ImageFont

U = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.dirname(os.path.dirname(U))
CIKTI = os.path.join(KOK, "arastirma", "FULL_MAKINE", "TOPPING_MONTAJ_v2_teknik.png")

W_MOD, Y0, YUST = 1800.0, 1060.0, 2030.0
AGIZ_R = (1070.0, 1180.0); TEKNE = (1061.5, 1091.5); DISK = (1154.0, 1168.0); PIDE = (1168.0, 1176.0)
ZT = -170.0; DUVAR = 90.0; GAP = 20.0
SOGUK_TABAN = 1320.0; YAL_TABAN = (1183.0, 1317.0); KASET_TAVAN = 1680.0; TEK = (1766.0, 2022.0); TAVAN_YUK = YUST - 62.0
V_EKSEN, V_UST = SOGUK_TABAN + 38.5, SOGUK_TABAN + 72.6
VZ = ZT - 217.0                                   # valf ekseni z (standart 90° ağız erişimi 217)
HUNI = (1452.0, 1632.0); HZ_D = (-120.0, -560.0)
ZON = [(0.0, -84.0), (-84.0, -104.0), (-104.0, -565.0), (-565.0, -630.0), (-630.0, -830.0)]

DIZI = [  # ad, tip, genişlik, hazne L, hazne üstü, ağız tipi, ağız ucu
    ("SOS", "uno", 220.0, "15 L (V)", 1737.0, "yassı 50", 1184.0),
    ("HARÇ", "uno", 440.0, "45 L", 1832.0, "yassı 50", 1184.0),
    ("KIYMA", "uno", 190.0, "8 L", 1667.0, "yuvarlak Ø36", 1216.0),
    ("KUŞBAŞI", "uno", 190.0, "8 L", 1667.0, "yuvarlak Ø36", 1216.0),
    ("KAŞAR", "kaset", 282.0, "8,8 kg", 1690.0, "Ø44 boru", 1216.0),
    ("KÜP SUCUK", "kaset", 142.0, "2,8 kg", 1690.0, "Ø42 boru", 1216.0),
]
YER, x = [], DUVAR + GAP / 2
for ad, tip, w, hz, ust, agiz, uc in DIZI:
    YER.append(dict(ad=ad, tip=tip, w=w, hz=hz, ust=ust, agiz=agiz, uc=uc, x0=x, x1=x + w, cx=x + w / 2)); x += w + GAP
X_SON = x - GAP / 2
W_GEREK = X_SON + DUVAR
YUKSEK_X1 = YER[1]["x1"] + GAP / 2                 # sos + harç üstünde tavan yükselir

S = 1.0
XA, XB = -60.0, W_MOD + 60
ML, MR, MT = 300, 360, 250
FH = int((2050 - 1040) * S); TH = int(845 * S)
YAN_W = int(900 * S)
W = int(ML + (XB - XA) * S + 120 + YAN_W + MR)
H = int(MT + FH + 230 + TH + 200)
FX = lambda x: ML + (x - XA) * S
FY = lambda y: MT + (2050 - y) * S
PT = MT + FH + 230
TZ = lambda z: PT + (z + 835.0) * S
SX0 = ML + (XB - XA) * S + 120                     # yan kesit sol kenarı (z 0 solda, ön)
SZ = lambda z: SX0 + (-z + 20) * S

INK, GRI, ACIK = (25, 25, 28), (120, 124, 130), (205, 208, 212)
F_BEL, F_BIZ, F_SOG, F_YAL, F_KAS = (228, 231, 236), (214, 230, 250), (236, 245, 252), (238, 238, 238), (250, 244, 222)
MAVI, KIR = (30, 90, 170), (200, 30, 30)
im = Image.new("RGB", (W, H), (255, 255, 255)); d = ImageDraw.Draw(im)
fn = lambda n, b=False: ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf" if b else "C:/Windows/Fonts/arial.ttf", n)
f_bas, f_gor, f_et, f_ol, f_ad = fn(40, True), fn(28, True), fn(19), fn(18), fn(21, True)


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


def kot(y_mm, t, yt=None, xk=None):
    xk = FX(XA) if xk is None else xk
    y = FY(y_mm); yt = y if yt is None else yt
    d.line([(xk - 8, y), (xk + 4, y)], fill=GRI, width=2)
    if yt != y: d.line([(xk - 12, yt), (xk - 8, y)], fill=GRI, width=1)
    tw = d.textlength(t, font=f_ol); d.text((xk - 16 - tw, yt - 10), t, font=f_ol, fill=INK)


def ortala(t, cx, y, font, renk=INK):
    tw = d.textlength(t, font=font); d.text((cx - tw / 2, y), t, font=font, fill=renk)


def uc_ciz(cx, uc, tip, yx, ybas):
    """ağız: yassı (trapez, 50) ya da yuvarlak boru"""
    if tip.startswith("yassı"):
        kutu(yx(cx - 18), yx(cx + 18), FY(uc + 40), FY(ybas), fill=F_BEL, renk=INK, w=2)
        d.polygon([(yx(cx - 18), FY(uc + 40)), (yx(cx + 18), FY(uc + 40)), (yx(cx + 25), FY(uc)), (yx(cx - 25), FY(uc))], fill=F_BEL, outline=INK)
    else:
        r = 18.0 if "36" in tip else (22.0 if "44" in tip else 21.0)
        kutu(yx(cx - r), yx(cx + r), FY(uc), FY(ybas), fill=F_BEL, renk=INK, w=2)


# ================================================================ başlık
d.text((ML, 40), "TOPPING · MONTAJ PAFTASI v2 — UNO ÇEKİRDEKLİ İSTASYONLAR + BİZİM KASETLER (öneri)", font=f_bas, fill=INK)
d.text((ML, 96), "ölçüler mm · kotlar yerden · x: modül C'nin sol ucundan · z: ön yüzden (arkaya −) · her UNO istasyonu ayrı: kendi haznesi, kendi valfi, kendi ağzı, kendi tahriki · (V) = varsayım",
       font=f_et, fill=GRI)

# ================================================================ ÖN GÖRÜNÜŞ
d.text((ML, MT - 44), "ÖN GÖRÜNÜŞ", font=f_gor, fill=INK)
kutu(FX(0), FX(W_MOD), FY(Y0), FY(YUST), renk=INK, w=3)
tarali(FX(0), FX(DUVAR), FY(Y0), FY(YUST)); tarali(FX(W_MOD - DUVAR), FX(W_MOD), FY(Y0), FY(YUST))
kutu(FX(DUVAR), FX(W_MOD - DUVAR), FY(TEKNE[0]), FY(TEKNE[1]), fill=F_YAL, renk=GRI, w=1)
for y in AGIZ_R: kesik((FX(DUVAR), FY(y)), (FX(W_MOD - DUVAR), FY(y)), GRI, 1)
tarali(FX(DUVAR), FX(W_MOD - DUVAR), FY(YAL_TABAN[0]), FY(YAL_TABAN[1]))
# soğuk hücre: sos + harç üstünde yüksek, kalanında 1680
kutu(FX(DUVAR), FX(YUKSEK_X1), FY(SOGUK_TABAN), FY(TAVAN_YUK), fill=F_SOG, renk=None)
kutu(FX(YUKSEK_X1), FX(W_MOD - DUVAR), FY(SOGUK_TABAN), FY(KASET_TAVAN), fill=F_SOG, renk=None)
tarali(FX(DUVAR), FX(YUKSEK_X1), FY(TAVAN_YUK), FY(YUST - 1.5))
tarali(FX(YUKSEK_X1), FX(W_MOD - DUVAR), FY(KASET_TAVAN), FY(KASET_TAVAN + 60))
tarali(FX(YUKSEK_X1), FX(YUKSEK_X1 + 60), FY(KASET_TAVAN + 60), FY(TAVAN_YUK))
kutu(FX(YUKSEK_X1 + 60), FX(W_MOD - DUVAR), FY(TEK[0]), FY(TEK[1]), fill=(250, 250, 250), renk=GRI, w=1)
ortala("teknik bant (PLC · UPS · güç)", FX((YUKSEK_X1 + 60 + W_MOD - DUVAR) / 2), FY(TEK[1]) + 40, f_et, GRI)
for u in YER:
    cx = u["cx"]
    if u["tip"] == "uno":
        hw = u["w"] / 2.0
        kutu(FX(cx - 41), FX(cx + 41), FY(SOGUK_TABAN), FY(V_UST), fill=F_BEL, renk=INK, w=2)
        kutu(FX(cx - 66), FX(cx - 41), FY(V_EKSEN - 20), FY(V_EKSEN + 20), fill=(60, 60, 64), renk=INK, w=1)
        kutu(FX(cx + 41), FX(cx + 91), FY(V_EKSEN - 22), FY(V_EKSEN + 22), fill=F_BIZ, renk=MAVI, w=2)
        cember(FX(cx), FY(V_EKSEN), 29.5 * S, fill=F_BEL)
        uc_ciz(cx, u["uc"], u["agiz"], FX, V_EKSEN - 18)
        kutu(FX(cx - 32), FX(cx + 32), FY(V_UST), FY(HUNI[0]), fill=F_BEL, renk=INK, w=2)
        hp = [(FX(cx - 32), FY(HUNI[0])), (FX(cx + 32), FY(HUNI[0])), (FX(cx + hw), FY(HUNI[1])), (FX(cx + hw), FY(u["ust"])),
              (FX(cx - hw), FY(u["ust"])), (FX(cx - hw), FY(HUNI[1]))]
        d.polygon(hp, fill=F_BIZ); d.line(hp + [hp[0]], fill=MAVI, width=3)
        ortala(u["hz"], FX(cx), FY((HUNI[1] + u["ust"]) / 2) - 10, f_et, MAVI)
    else:
        kutu(FX(u["x0"] + 1), FX(u["x1"] - 1), FY(SOGUK_TABAN + 10), FY(SOGUK_TABAN + 370), fill=F_KAS, renk=INK, w=2)
        uc_ciz(cx, u["uc"], u["agiz"], FX, SOGUK_TABAN + 10)
        ortala(u["hz"], FX(cx), FY(1520), f_et, INK)
    ortala(u["ad"], FX(cx), FY(YUST) - 58, f_ad)
    ortala("UNO çekirdeği" if u["tip"] == "uno" else "bizim kaset", FX(cx), FY(YUST) - 32, f_et, MAVI if u["tip"] == "uno" else GRI)
t0 = YER[0]["cx"]
kutu(FX(t0 - 170), FX(t0 + 170), FY(DISK[0]), FY(DISK[1]), fill=(250, 226, 196), renk=INK, w=2)
kutu(FX(t0 - 140), FX(t0 + 140), FY(PIDE[0]), FY(PIDE[1]), fill=(240, 200, 150), renk=INK, w=1)
for y, t in [(Y0, "1060"), (SOGUK_TABAN, "1320 soğuk taban"), (KASET_TAVAN, "1680"), (1737.0, "1737 sos"),
             (TAVAN_YUK, "1968"), (YUST, "2030")]:
    kot(y, t)
kot(1832.0, "1832 harç", FY(1832.0) - 4)
kot(1667.0, "1667 kıyma · kuşbaşı", FY(1667.0) + 14)
yb = FY(1200) - 34
for i, (y, t) in enumerate([(1216.0, "1216 yuvarlak ağız ucu"), (1184.0, "1184 yassı ağız ucu"), (AGIZ_R[1], "1180 robot ağzı"), (PIDE[1], "1176 pide üstü"), (DISK[1], "1168 süreç")]):
    kot(y, t, yb + i * 25)
yb = FY(1040) + 30
for u in YER: olcu_x(yb, FX(u["x0"]), FX(u["x1"]), "%.0f" % u["w"])
for u in YER: ortala("x %.0f" % u["cx"], FX(u["cx"]), yb + 8, f_ol, GRI)
olcu_x(yb + 70, FX(0), FX(W_GEREK), "gereken %.0f (modül 1800 · pay %.0f)" % (W_GEREK, W_MOD - W_GEREK))

# ================================================================ ÜST GÖRÜNÜŞ
d.text((ML, PT - 44), "ÜST GÖRÜNÜŞ", font=f_gor, fill=INK)
kutu(FX(0), FX(W_MOD), TZ(0), TZ(-830), renk=INK, w=3)
tarali(FX(0), FX(DUVAR), TZ(-830), TZ(0)); tarali(FX(W_MOD - DUVAR), FX(W_MOD), TZ(-830), TZ(0))
for z0, z1 in ZON: d.line([(FX(DUVAR), TZ(z1)), (FX(W_MOD - DUVAR), TZ(z1))], fill=ACIK, width=1)
tarali(FX(DUVAR), FX(W_MOD - DUVAR), TZ(-565.0), TZ(-630.0))
xx = FX(DUVAR)
while xx < FX(W_MOD - DUVAR):
    d.line([(xx, TZ(ZT)), (min(xx + 22, FX(W_MOD - DUVAR)), TZ(ZT))], fill=GRI, width=2); xx += 32
for u in YER:
    cx = u["cx"]
    if u["tip"] == "uno":
        hw = u["w"] / 2.0
        kutu(FX(cx - hw), FX(cx + hw), TZ(HZ_D[0]), TZ(HZ_D[1]), renk=MAVI, w=2, gizli=True)
        kutu(FX(cx - 41), FX(cx + 41), TZ(VZ + 41), TZ(VZ - 41), fill=F_BEL, renk=INK, w=2)
        kutu(FX(cx - 66), FX(cx - 41), TZ(VZ + 20), TZ(VZ - 20), fill=(60, 60, 64), renk=INK, w=1)
        kutu(FX(cx + 41), FX(cx + 91), TZ(VZ + 25), TZ(VZ - 25), fill=F_BIZ, renk=MAVI, w=2)
        kutu(FX(cx - 18), FX(cx + 18), TZ(VZ + 41), TZ(ZT - 18), fill=F_BEL, renk=INK, w=2)
        kutu(FX(cx - 29), FX(cx + 29), TZ(VZ - 41), TZ(-559.0), fill=(232, 236, 242), renk=INK, w=2)
        kutu(FX(cx - 6), FX(cx + 6), TZ(-559.0), TZ(-640.0), fill=F_BEL, renk=INK, w=1)
        kutu(FX(cx - 30), FX(cx + 30), TZ(-640.0), TZ(-820.0), fill=F_BIZ, renk=MAVI, w=2)
        if u["agiz"].startswith("yassı"): kutu(FX(cx - 25), FX(cx + 25), TZ(ZT + 4), TZ(ZT - 4), fill=INK, renk=INK, w=1)
        else: cember(FX(cx), TZ(ZT), 18 * S, fill=INK)
    else:
        kutu(FX(u["x0"] + 1), FX(u["x1"] - 1), TZ(-200.0), TZ(-525.0), fill=F_KAS, renk=INK, w=2)
        r = 22.0 if u["ad"] == "KAŞAR" else 21.0
        kutu(FX(cx - r), FX(cx + r), TZ(-116.0), TZ(-200.0), fill=F_BEL, renk=INK, w=2)
        cember(FX(cx), TZ(ZT), r * S, fill=INK)
        for dx in ((-60.0, 60.0) if u["ad"] == "KAŞAR" else (-35.0, 35.0)):
            kutu(FX(cx + dx - 29), FX(cx + dx + 29), TZ(-640.0), TZ(-796.0), fill=F_BIZ, renk=MAVI, w=1)
    ortala(u["ad"], FX(cx), TZ(0) + 14, f_ad)
cember(FX(t0), TZ(ZT), 170 * S, renk=(200, 140, 70), w=2); cember(FX(t0), TZ(ZT), 140 * S, renk=(200, 140, 70), w=1, gizli=True)
xr = FX(W_MOD) + 14
for z, t in [(0, "0 ön yüz"), (-104, "−104"), (ZT, "−170 tabla ekseni"), (VZ, "−387 valf"), (-565, "−565"), (-630, "−630"), (-830, "−830")]:
    d.line([(FX(W_MOD) + 2, TZ(z)), (xr, TZ(z))], fill=GRI, width=1); d.text((xr + 4, TZ(z) - 10), t, font=f_ol, fill=INK)

# ================================================================ YAN KESİT (harç ekseninden, x = HARÇ)
d.text((SX0, MT - 44), "YAN KESİT · HARÇ İSTASYONU", font=f_gor, fill=INK)
kutu(SZ(0), SZ(-830), FY(Y0), FY(YUST), renk=INK, w=3)
tarali(SZ(0), SZ(-830), FY(YAL_TABAN[0]), FY(YAL_TABAN[1]))
kutu(SZ(-104), SZ(-565), FY(SOGUK_TABAN), FY(TAVAN_YUK), fill=F_SOG, renk=None)
tarali(SZ(-565), SZ(-630), FY(SOGUK_TABAN), FY(TAVAN_YUK)); tarali(SZ(0), SZ(-830), FY(TAVAN_YUK), FY(YUST - 1.5))
kutu(SZ(-84), SZ(-104), FY(SOGUK_TABAN), FY(TAVAN_YUK), fill=F_YAL, renk=GRI, w=1)
kutu(SZ(0), SZ(-830), FY(TEKNE[0]), FY(TEKNE[1]), fill=F_YAL, renk=GRI, w=1)
kutu(SZ(ZT + 170), SZ(ZT - 170), FY(DISK[0]), FY(DISK[1]), fill=(250, 226, 196), renk=INK, w=2)
kutu(SZ(ZT + 140), SZ(ZT - 140), FY(PIDE[0]), FY(PIDE[1]), fill=(240, 200, 150), renk=INK, w=1)
# valf, ağız (yandan: valften öne yatay, dirsek, aşağı), silindir, mil, tahrik, hazne
kutu(SZ(VZ + 41), SZ(VZ - 41), FY(SOGUK_TABAN), FY(V_UST), fill=F_BEL, renk=INK, w=2)
kutu(SZ(VZ + 41), SZ(ZT + 18), FY(V_EKSEN - 18), FY(V_EKSEN + 18), fill=F_BEL, renk=INK, w=2)
kutu(SZ(ZT + 18), SZ(ZT - 18), FY(1184 + 40), FY(V_EKSEN + 18), fill=F_BEL, renk=INK, w=2)
d.polygon([(SZ(ZT + 8), FY(1224)), (SZ(ZT - 8), FY(1224)), (SZ(ZT - 4), FY(1184)), (SZ(ZT + 4), FY(1184))], fill=F_BEL, outline=INK)
kutu(SZ(VZ - 41), SZ(-559), FY(V_EKSEN - 29), FY(V_EKSEN + 29), fill=(232, 236, 242), renk=INK, w=2)
kutu(SZ(-559), SZ(-640), FY(V_EKSEN - 6), FY(V_EKSEN + 6), fill=F_BEL, renk=INK, w=1)
kutu(SZ(-640), SZ(-820), FY(V_EKSEN - 30), FY(V_EKSEN + 30), fill=F_BIZ, renk=MAVI, w=2)
kutu(SZ(-650), SZ(-726), FY(V_EKSEN + 34), FY(V_EKSEN + 91), fill=F_BIZ, renk=MAVI, w=2)
kutu(SZ(VZ + 32), SZ(VZ - 32), FY(V_UST), FY(HUNI[0]), fill=F_BEL, renk=INK, w=2)
hp = [(SZ(VZ + 32), FY(HUNI[0])), (SZ(VZ - 32), FY(HUNI[0])), (SZ(HZ_D[1]), FY(HUNI[1])), (SZ(HZ_D[1]), FY(1832)), (SZ(HZ_D[0]), FY(1832)), (SZ(HZ_D[0]), FY(HUNI[1]))]
d.polygon(hp, fill=F_BIZ); d.line(hp + [hp[0]], fill=MAVI, width=3)
for z, t, dy in [(ZT, "tabla ekseni −170", 0), (VZ, "valf −387", 0), (-565, "−565", 0), (-630, "−630", 0)]:
    d.line([(SZ(z), FY(Y0) + 6), (SZ(z), FY(Y0) + 26)], fill=GRI, width=1)
for i, (z, t) in enumerate([(ZT, "−170"), (VZ, "−387"), (-565, "−565"), (-630, "−630"), (-830, "−830")]):
    ortala(t, SZ(z), FY(Y0) + 30, f_ol)
def et(px, py, hx, hy, t, renk=INK):
    d.line([(px, py), (hx, hy)], fill=GRI, width=1); tw = d.textlength(t, font=f_et)
    d.text((hx + 6, hy - 12), t, font=f_et, fill=renk)
EX = SZ(-830) + 20
et(SZ(-340), FY(1750), EX, FY(1900), "bizim hazne 45 L (soğuk)", MAVI)
et(SZ(VZ), FY(1340), EX, FY(1560), "UNO valf bloğu (Beldos)")
et(SZ(-500), FY(V_EKSEN), EX, FY(1470), "ürün silindiri Ø52 (Beldos)")
et(SZ(-600), FY(V_EKSEN), EX, FY(1400), "mil · keçeli geçiş")
et(SZ(-730), FY(V_EKSEN), EX, FY(1330), "step motor + vidalı mil", MAVI)
et(SZ(-250), FY(V_EKSEN), EX, FY(1260), "90° ağız + yassı uç")
et(SZ(-170), FY(1160), EX, FY(1150), "tabla Ø340 · pide Ø280")
et(SZ(-450), FY(1250), EX, FY(1210), "yalıtım tabanı")
for i, (y, t) in enumerate([(1184.0, "1184"), (SOGUK_TABAN, "1320"), (1832.0, "1832"), (TAVAN_YUK, "1968")]):
    kot(y, t, xk=SZ(0) - 6)

os.makedirs(os.path.dirname(CIKTI), exist_ok=True)
im.save(CIKTI, optimize=True)
print("PNG", CIKTI, im.size)
for u in YER: print("  %-10s x %.0f–%.0f · ağız x %.0f · hazne %s · üst %.0f · ağız %s" % (u["ad"], u["x0"], u["x1"], u["cx"], u["hz"], u["ust"], u["agiz"]))
print("gereken %.0f · modül 1800 · pay %.0f" % (W_GEREK, W_MOD - W_GEREK))
