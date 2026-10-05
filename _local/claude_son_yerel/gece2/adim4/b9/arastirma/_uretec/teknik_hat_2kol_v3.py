# -*- coding: utf-8 -*-
"""AUTOKITCH - HAT 2 KOL · TEKNIK RESIM v3 (17 Eyl 2026) — Kemal eskizi 2: PRESS | ATOSA TOPPING (tabla yok) ustte; altinda DOLAP MOTOR bandi + cekmeceler; sagda FIRIN x3 / KESICI / YAG / ROBOT KUTUSU; en sagda KUTU KATLAYAN. QR dolabi yok.: ON + UST (PLAN KESITI) + 2 YAN KESIT. Olculer mm.
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

OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE\HAT_2KOL_v3_teknik.png".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX = 5200, 3200
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
# Kemal eskizi 2 (17 Eyl): PRESS | ATOSA TOPPING (tabla yok) ustte; altinda DOLAP MOTOR bandi + cekmeceler;
# sagda FIRIN x3 / KESICI / YAG / ROBOT KUTUSU kolonu; en sagda KUTU KATLAYAN. QR dolabi yok.
DZ = 830.0
WO, BIND, FUGA, BOLME, XI = 620.0, 15.0, 3.0, 35.0, 62.5
CELL0 = 182.5
YUZ0 = CELL0 - BIND
HH = {"hamur": 75.0, "lahm": 60.0, "icecek": 132.0, "tatli": 132.0}
AD = {"hamur": "TAZE PİDE", "lahm": "LAHMACUN", "icecek": "İÇECEK 330 ml", "tatli": "TATLI"}
CAP = {"hamur": (20, "top"), "lahm": (35, "top"), "icecek": (56, "kutu"), "tatli": (14, "adet")}
KOLON = [[(8, "hamur")], [(6, "lahm"), (2, "icecek")], [(6, "lahm"), (1, "icecek"), (1, "tatli")]]   # 24 cekmece
KOLON_AD = ("K1", "K2", "K3")
W_PRESS, W_TOP, W_OVEN, W_KUTU = 700.0, 1400.0, 700.0, 700.0
W_SOL = W_PRESS + W_TOP                                    # 2100: cekmece bandi bu genislikte
assert 2 * XI + 3 * WO + 2 * BOLME <= W_SOL
HAT = W_SOL + W_OVEN + W_KUTU                              # 3500
BAND_UST = 1055.5                                          # en yuksek kolonun ustu (K2/K3)
MOTOR = (1060.0, 1360.0)                                   # dolap motor ve diger
UST0 = 1360.0                                              # press / topping tabani
T_AGZ, T_BAS, T_KAS = (1360.0, 1470.0), (1473.0, 1607.0), (1610.0, 1968.5)
YUVA = [("HARÇ", 140.0, 120.0), ("HARÇ", 140.0, 260.0), ("HARÇ", 140.0, 400.0), ("HARÇ", 140.0, 540.0),
        ("KIYMA", 140.0, 680.0), ("KUŞBAŞI", 140.0, 820.0), ("KAŞAR KABI", 280.0, 1030.0), ("SUCUK|DİLİMLEYİCİ", 180.0, 1260.0)]
OVEN_CEPHE = [("k", 33.0, 667.0, 123.0, 590.0, "ROBOT KUTUSU|R1 + R2 kontrol kutuları 245 × 180 × 45 · PLC · HMI", None, None),
              ("k", 33.0, 667.0, 600.0, 860.0, "YAĞ KABI · SPREY", None, 845.0),
              ("a", 53.0, 647.0, 640.0, 820.0, "İŞLEM AĞZI · yağ spreyi", None, None),
              ("k", 33.0, 667.0, 870.0, 1140.0, "KESİCİ · yıldız bıçak · piston", None, None),
              ("k", 33.0, 667.0, 1145.0, 1420.0, "FIRIN HAZNESİ 1|LAHMACUN · 120 s · kapaklı", None, None),
              ("k", 33.0, 667.0, 1425.0, 1700.0, "FIRIN HAZNESİ 2|LAHMACUN · 120 s · kapaklı", None, None),
              ("k", 33.0, 667.0, 1705.0, 1968.5, "FIRIN HAZNESİ 3|PİDE · PİZZA · 240 s · ayrı sıcaklık", None, None)]
KUTU_CEPHE = [("k", 33.0, 667.0, 123.0, 690.0, "PANO|vakum · katlama tahriği · kapak kapatma", None, None),
              ("a", 30.0, 670.0, 700.0, 950.0, "KUTULAMA AĞZI", None, None),
              ("k", 33.0, 667.0, 960.0, 1968.5, "KUTU ŞARJÖRÜ|blank 400 × 760 · 1000 mm = 555–665 kutu (2 gün 560)", None, None)]
R1X, R2X, RZ = 1050.0, 2800.0, 380.0
KAIDE, OMUZ = 820.0, 1000.0
ERISIM, ERISIM_P = 1400.0, 1250.0
AKT = (1900.0, 2300.0, 900.0, 1300.0)
KOR = 800.0

# ======================= YERLESIM =======================
OX = 300.0
FY_TOP = 400.0
FY = FY_TOP + 1970.0 * S
PY_TOP = FY + 330.0
SX = OX + HAT * S + 260.0
SX2 = SX + (DZ + KOR + 160.0) * S + 200.0


def fx(x):
    return OX + x * S


def fy(y):
    return FY - y * S


def py(z):
    return PY_TOP + (z + 790.0) * S


# ======================= BASLIK =======================
txt(OX, 70, "AUTOKITCH  ·  HAT 2 KOL  ·  TEKNİK RESİM  v3  ·  PRESS + ATOSA TOPPING (TABLA YOK) ÜSTTE, ÇEKMECELER ALTTA  ·  FIRIN ×3  ·  KUTU KATLAYAN", f38, INK)
txt(OX, 138, "ön · üst · yan görünüş  ·  günde 80 pide + 200 lahmacun (+ pizza)  ·  2 gün stok  ·  24 çekmece 3 kolon  ·  2 × Fairino FR10 koridorda  ·  QR dolabı yok  ·  tüm modüller 830 derin  ·  ölçüler mm  ·  17 Eylül 2026", f13, GRAY)
d.line([(OX, 178), (W_PX - 170, 178)], fill=LINE, width=3)

# ======================= ON GORUNUS =======================
txt(OX, FY_TOP - 190, "ÖN GÖRÜNÜŞ", f16, ACC)
txt(OX, FY_TOP - 152, "robotlar koridorda önde — konumları zeminde işaretli; kollar plan ve yan kesitte", f9, GRAY)


def kabin(x0mm, w, ad):
    x0, x1 = fx(x0mm), fx(x0mm + w)
    d.rectangle([x0, fy(1970), x1, fy(0)], fill=FILL, outline=LINE, width=3)
    d.rectangle([x0, fy(120), x1, fy(0)], fill=SOFT, outline=LINE, width=2)
    if ad:
        txt((x0 + x1) / 2, fy(1970) - 64, ad, f13, INK, "md")


def cephe(x0mm, liste):
    for tip, a, b, y0, y1, et, yv, yl in liste:
        if tip == "k":
            d.rectangle([fx(x0mm + a), fy(y1), fx(x0mm + b), fy(y0)], fill=(SICAK if "FIRIN" in et else BG), outline=LINE, width=2)
            if et:
                satirlar(fx(x0mm + (a + b) / 2), fy(yl if yl else (y0 + y1) / 2), et, f8, INK)
    for tip, a, b, y0, y1, et, yv, yl in liste:
        if tip == "a":
            d.rectangle([fx(x0mm + a), fy(y1), fx(x0mm + b), fy(y0)], fill=AGZ, outline=RED, width=3)
            cy = (fy(y0) + fy(y1)) / 2
            txt(fx(x0mm + (a + b) / 2), cy - 10, et, f8, RED, "mm")
            txt(fx(x0mm + (a + b) / 2), cy + 12, "y %s – %s" % (sayi(y0), sayi(y1)), f7, RED, "mm")


# --- SOL GOVDE: cekmece bandi + motor bandi + press + topping
kabin(0.0, W_SOL, "")
txt(fx(W_PRESS / 2), fy(1970) - 64, "M1 · PRESS", f13, INK, "md")
txt(fx(W_PRESS + W_TOP / 2), fy(1970) - 64, "M2 · ATOSA (YINDU) DOZAJ ÜNİTESİ · TABLA YOK", f13, INK, "md")
d.rectangle([fx(30), fy(BAND_UST + 3), fx(W_SOL - 30), fy(121.5)], fill=BG, outline=LINE, width=2)
cx = XI
for ki, gruplar in enumerate(KOLON):
    if ki:
        d.rectangle([fx(cx - BOLME), fy(BAND_UST), fx(cx), fy(YUZ0)], fill=SOFT, outline=LINE, width=1)
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
    txt(fx(cx + WO / 2), fy(BAND_UST) + 14, KOLON_AD[ki], f7, GRAY, "mm")
    olcu_h(fx(cx), fx(cx + WO), fy(0) + 44, "620", f8, GRAY)
    cx += WO + BOLME
d.rectangle([fx(33), fy(MOTOR[1]), fx(W_SOL - 33), fy(MOTOR[0])], fill=SOFT, outline=LINE, width=2)
txt(fx(W_SOL / 2), fy((MOTOR[0] + MOTOR[1]) / 2) - 10, "DOLAP MOTOR VE DİĞER  ·  2 soğutma grubu 1,5 HP (yatık) · 3 kolon evaporatörü · çekmece sürücüleri · ana pano", f9, INK, "mm")
txt(fx(W_SOL / 2), fy((MOTOR[0] + MOTOR[1]) / 2) + 14, "300 yüksek · önden servis kapağı · hava girişi ön, çıkışı arka", f7, GRAY, "mm")
# press
d.rectangle([fx(33), fy(1968.5), fx(W_PRESS - 33), fy(UST0)], fill=BG, outline=LINE, width=2)
d.rectangle([fx(33), fy(1860.0), fx(W_PRESS - 33), fy(UST0)], fill=BG, outline=LINE, width=2)
satirlar(fx(W_PRESS / 2), fy(1800.0), "FERSAH PZP-400|pres başlığı 640 × 800 · alt kabin yok", f8, INK)
d.rectangle([fx(53), fy(1720.0), fx(W_PRESS - 53), fy(1420.0)], fill=AGZ, outline=RED, width=3)
txt(fx(W_PRESS / 2), fy(1570.0) - 10, "PRES AĞZI · platen Ø400 kot ~1500", f8, RED, "mm")
txt(fx(W_PRESS / 2), fy(1570.0) + 12, "y 1420 – 1720", f7, RED, "mm")
txt(fx(W_PRESS / 2), fy(1915.0), "kapak üste açılır · 3,5 kW", f7, GRAY, "mm")
d.line([(fx(W_PRESS), fy(1970)), (fx(W_PRESS), fy(UST0))], fill=LINE, width=3)
# topping (atosa)
tx0 = W_PRESS
d.rectangle([fx(tx0 + 30), fy(T_AGZ[1]), fx(tx0 + W_TOP - 30), fy(T_AGZ[0])], fill=AGZ, outline=RED, width=3)
txt(fx(tx0 + W_TOP / 2), fy(1415.0) - 10, "ROBOT AĞZI · tabanı robot tutar ve döndürür · tabla yok", f8, RED, "mm")
txt(fx(tx0 + W_TOP / 2), fy(1415.0) + 12, "y 1360 – 1470 · 1340 geniş", f7, RED, "mm")
d.rectangle([fx(tx0 + 33), fy(T_BAS[1]), fx(tx0 + W_TOP - 33), fy(T_BAS[0])], fill=BG, outline=LINE, width=2)
txt(fx(tx0 + W_TOP / 2), fy(1540.0), "DOZAJ BAŞLIKLARI  ·  harç: piston pompa + nozul  ·  kıyma / kuşbaşı: vidalı dozaj  ·  kaşar: karıştırıcılı hazne + vida  ·  sucuk: çubuk şarjörü + bıçak", f7, INK, "mm")
d.rectangle([fx(tx0 + 33), fy(T_KAS[1]), fx(tx0 + W_TOP - 33), fy(T_KAS[0])], fill=BG, outline=LINE, width=2)
for urun, gw, xc in YUVA:
    drect(fx(tx0 + xc - gw / 2 + 6), fy(T_KAS[1] - 8), fx(tx0 + xc + gw / 2 - 6), fy(T_KAS[0] + 8), INK, 1)
    satirlar(fx(tx0 + xc), fy(1790.0) - 4, urun, f7, INK, 16)
    txt(fx(tx0 + xc), fy(1790.0) + 22, sayi(gw), f7, GRAY, "mm")
txt(fx(tx0 + W_TOP / 2), fy(1950.0), "HAZNE SIRASI · +3 °C · kaset 140 × 400 × 360 · kaşar kabı 280 × 400 × 360 · sucuk şarjörü 180 × 400 · önden takılır (kot 1610)", f7, GRAY, "mm")
olcu_h(fx(0), fx(W_PRESS), fy(1970) - 26, sayi(W_PRESS), f11, INK)
olcu_h(fx(W_PRESS), fx(W_SOL), fy(1970) - 26, sayi(W_TOP), f11, INK)
# --- OVEN kolonu
kabin(W_SOL, W_OVEN, "M3 · FIRIN · KESİCİ · YAĞ")
cephe(W_SOL, OVEN_CEPHE)
olcu_h(fx(W_SOL), fx(W_SOL + W_OVEN), fy(1970) - 26, sayi(W_OVEN), f11, INK)
# --- KUTU kolonu
kabin(W_SOL + W_OVEN, W_KUTU, "M4 · KUTU KATLAYAN")
cephe(W_SOL + W_OVEN, KUTU_CEPHE)
olcu_h(fx(W_SOL + W_OVEN), fx(HAT), fy(1970) - 26, sayi(W_KUTU), f11, INK)
olcu_h(fx(0), fx(HAT), fy(0) + 96, "HAT  %s" % sayi(HAT), f13, INK)
olcu_v(fx(0) - 44, fy(1970), fy(0), "1970", f11, INK, "l")
for yy in (120.0, BAND_UST, MOTOR[1], T_AGZ[1], T_KAS[0], 1970.0):
    d.line([(fx(0) - 24, fy(yy)), (fx(0) - 6, fy(yy))], fill=INK, width=2)
    txt(fx(0) - 52, fy(yy), sayi(yy), f7, INK, "rm")
ax0, ax1, ay0, ay1 = AKT
for rx, ad in ((R1X, "R1 · FR10"), (R2X, "R2 · FR10")):
    d.polygon([(fx(rx), fy(0) + 4), (fx(rx) - 14, fy(0) + 30), (fx(rx) + 14, fy(0) + 30)], fill=ACC)
    txt(fx(rx), fy(0) + 46, ad + " · koridorda, önde", f8, ACC, "mm")
    txt(fx(rx), fy(0) + 66, "x " + sayi(rx) + " · z +380", f7, GRAY, "mm")

# ======================= UST GORUNUS (PLAN KESITI) =======================
txt(OX, PY_TOP - 170, "ÜST GÖRÜNÜŞ  ·  PLAN KESİTİ  ·  robot erişimi", f16, ACC)
txt(fx(HAT / 2), py(-790) - 34, "ARKA", f9, GRAY, "mm")
zb = 40.0 - DZ
for x0m, w, ad in ((0.0, W_PRESS, "M1 · PRESS"), (W_PRESS, W_TOP, "M2 · ATOSA TOPPING"), (W_SOL, W_OVEN, "M3 · FIRIN"), (W_SOL + W_OVEN, W_KUTU, "M4 · KUTU")):
    d.rectangle([fx(x0m), py(zb), fx(x0m + w), py(40.0)], fill=FILL, outline=LINE, width=3)
    txt(fx(x0m + w / 2), py(40.0) + 30, "%s  ·  %s × %s" % (ad, sayi(w), sayi(DZ)), f9, INK, "mm")
d.rectangle([fx(1.5), py(zb + 1.5), fx(W_SOL - 1.5), py(zb + 61.5)], fill=PUC, outline=GRAY, width=1)
cx = XI
for ki in range(3):
    drect(fx(cx + 16), py(-680.0), fx(cx + WO - 16), py(0.0), DOLAP, 2)
    d.rectangle([fx(cx + 190), py(-725.0), fx(cx + 450), py(-680.0)], fill=EVC, outline=BUZ, width=1)
    d.rectangle([fx(cx + 17), py(-716.0), fx(cx + 67), py(-680.0)], fill=(255, 230, 230), outline=RED, width=1)
    txt(fx(cx + 320), py(-702.5), "EVAPORATÖR", f7, BUZ, "mm")
    txt(fx(cx + 42), py(-698.0), "M", f7, RED, "mm")
    txt(fx(cx + WO / 2), py(-640.0), "K%d · ÇEKMECE 620 × 680 · altta" % (ki + 1), f7, DOLAP, "mm")
    cx += WO + BOLME
d.rectangle([fx(29), py(-788.0), fx(669), py(12.0)], fill=BG, outline=INK, width=2)
d.ellipse([fx(149), py(-500.0), fx(549), py(-100.0)], outline=GRAY, width=1)
txt(fx(349), py(-330.0), "FERSAH PZP-400", f8, INK, "mm")
txt(fx(349), py(-300.0), "640 × 800 · platen Ø400", f7, GRAY, "mm")
for urun, gw, xc in YUVA:
    d.rectangle([fx(W_PRESS + xc - gw / 2 + 6), py(-470.0), fx(W_PRESS + xc + gw / 2 - 6), py(-70.0)], fill=BG, outline=INK, width=2)
    satirlar(fx(W_PRESS + xc), py(-300.0), urun, f7, INK, 16)
    txt(fx(W_PRESS + xc), py(-250.0), "%s × 400" % sayi(gw), f7, GRAY, "mm")
d.rectangle([fx(W_PRESS + 30), py(-780.0), fx(W_SOL - 30), py(-740.0)], fill=EVC, outline=BUZ, width=1)
txt(fx(W_PRESS + W_TOP / 2), py(-760.0), "EVAPORATÖR · hazne kabini +3 °C", f7, BUZ, "mm")
d.rectangle([fx(W_PRESS + 30), py(-60.0), fx(W_SOL - 30), py(0.0)], fill=AGZ, outline=RED, width=1)
txt(fx(W_PRESS + W_TOP / 2), py(-30.0), "ROBOT AĞZI · kapaklı · 1340 × 110", f7, RED, "mm")
txt(fx(W_PRESS + W_TOP / 2), py(-560.0), "ATOSA (YINDU) DOZAJ ÜNİTESİ · 8 hazne tek sıra · tabla yok", f8, INK, "mm")
ox = W_SOL
d.rectangle([fx(ox + 30), py(-600.0), fx(ox + 670), py(-20.0)], fill=SICAK, outline=INK, width=2)
txt(fx(ox + 350), py(-325.0), "FIRIN · 3 HAZNE ÜST ÜSTE", f8, INK, "mm")
txt(fx(ox + 350), py(-295.0), "640 × 600 × 275 · kapaklı", f7, GRAY, "mm")
d.rectangle([fx(ox + 30), py(-780.0), fx(ox + 670), py(-620.0)], fill=BG, outline=GRAY, width=1)
txt(fx(ox + 350), py(-700.0), "EGZOZ KANALI · fan · karbon filtre", f7, GRAY, "mm")
kx = W_SOL + W_OVEN
drect(fx(kx + 150), py(-785.5), fx(kx + 550), py(-25.5), GRAY, 1)
txt(fx(kx + 350), py(-640.0), "BLANK 400 × 760", f7, GRAY, "mm")
d.rectangle([fx(kx + 190), py(-410.0), fx(kx + 510), py(-90.0)], fill=BG, outline=INK, width=2)
txt(fx(kx + 350), py(-265.0), "KUTU", f8, INK, "mm")
txt(fx(kx + 350), py(-235.0), "320 × 320 × 45", f7, GRAY, "mm")
olcu_h(fx(0), fx(HAT), py(40.0) + 96, "HAT  %s" % sayi(HAT), f13, INK)
olcu_v(fx(0) - 44, py(-790), py(40.0), sayi(DZ), f11, INK, "l")
d.line([(fx(-60), py(40.0 + KOR)), (fx(HAT + 60), py(40.0 + KOR))], fill=GRAY, width=1)
txt(fx(HAT / 2), py(40.0 + KOR) + 22, "ÖN  ·  robot koridoru %s" % sayi(KOR), f9, GRAY, "mm")
d.rectangle([fx(ax0), py(160.0), fx(ax1), py(560.0)], fill=BG, outline=ACC, width=2)
txt(fx((ax0 + ax1) / 2), py(320.0), "AKTARMA RAFI", f8, ACC, "mm")
txt(fx((ax0 + ax1) / 2), py(365.0), "6 tepsi Ø340 · kot 900–1300", f7, GRAY, "mm")
txt(fx((ax0 + ax1) / 2), py(405.0), "üstünde uç istasyonu · altında çöp 60 L", f7, GRAY, "mm")
for rx, ad in ((R1X, "R1 · FR10 · erişim 1400"), (R2X, "R2 · FR10 · erişim 1400")):
    cxp, cyp = fx(rx), py(RZ)
    d.rectangle([fx(rx - 200), py(RZ - 200), fx(rx + 200), py(RZ + 200)], fill=SOFT, outline=ACC, width=1)
    d.ellipse([cxp - 100 * S, cyp - 100 * S, cxp + 100 * S, cyp + 100 * S], fill=BG, outline=ACC, width=3)
    darc(cxp, cyp, ERISIM_P * S, 183.0, 357.0, ACC, 2, 3.0)
    darc(cxp, cyp, ERISIM * S, 190.0, 350.0, BOSL, 1, 2.5)
    txt(cxp, py(RZ + 200) + 22, ad, f9, ACC, "mm")
    txt(cxp, py(RZ + 200) + 46, "kaide 400 × 400 · eksen z +380 · pratik erişim 1250", f7, GRAY, "mm")
txt(fx(0) - 50, py(40.0) + 76, "yay: pratik 1250 (mavi) · nominal 1400 (gri)", f7, ACC, "la")
txt(fx(HAT / 2), py(RZ + 200) + 80, "R1 bölgesi PRESS + TOPPING + 3 çekmece kolonu (0–2100)  ·  R2 bölgesi FIRIN + KUTU (2100–3500)  ·  erişimler AKTARMA RAFI'nda kesişir", f9, INK, "mm")


# ======================= YAN KESIT A · TOPPING KOLONU =======================
def sz(z):
    return SX + (z + 790.0) * S


txt(SX, FY_TOP - 190, "YAN KESİT A", f16, ACC)
txt(SX, FY_TOP - 152, "M2 · K2 kolonundan kesit: çekmeceler · motor bandı · Atosa dozaj · robot koridorda", f9, GRAY)
d.rectangle([sz(-790), fy(1970), sz(40), fy(0)], fill=FILL, outline=LINE, width=3)
d.rectangle([sz(-790), fy(120), sz(40), fy(0)], fill=SOFT, outline=LINE, width=2)
d.rectangle([sz(-788.5), fy(1968.5), sz(-728.5), fy(121.5)], fill=PUC, outline=GRAY, width=1)
d.rectangle([sz(-728.5), fy(1968.5), sz(0.0), fy(1908.5)], fill=PUC, outline=GRAY, width=1)
d.rectangle([sz(-728.5), fy(181.5), sz(0.0), fy(121.5)], fill=PUC, outline=GRAY, width=1)
d.rectangle([sz(-728.5), fy(MOTOR[0]), sz(0.0), fy(BAND_UST)], fill=PUC, outline=GRAY, width=1)
y0 = YUZ0
for adet, tip in KOLON[1]:
    h = HH[tip] + 2 * BIND
    for _ in range(adet):
        d.rectangle([sz(-680.0), fy(y0 + h), sz(0.0), fy(y0)], fill=BG, outline=DOLAP, width=1)
        d.rectangle([sz(0.0), fy(y0 + h), sz(40.0), fy(y0)], fill=BG, outline=DOLAP, width=1)
        y0 += h + FUGA
txt(sz(-340), fy(450.0) - 10, "ÇEKMECE 680 · LAHMACUN × 6 + İÇECEK × 2", f8, DOLAP, "mm")
txt(sz(-340), fy(450.0) + 12, "motorlu · ön sıra robota sunulur", f7, GRAY, "mm")
d.rectangle([sz(-728.5), fy(MOTOR[1]), sz(0.0), fy(MOTOR[0])], fill=SOFT, outline=LINE, width=1)
txt(sz(-364), fy(1210.0) - 10, "DOLAP MOTOR VE DİĞER · 300", f8, INK, "mm")
txt(sz(-364), fy(1210.0) + 12, "soğutma grubu yatık · sürücüler · pano", f7, GRAY, "mm")
d.rectangle([sz(-728.5), fy(T_AGZ[1]), sz(-10.0), fy(T_AGZ[0])], fill=AGZ, outline=None)
d.rectangle([sz(-10.0), fy(T_AGZ[1]), sz(40.0), fy(T_AGZ[0])], fill=AGZ, outline=RED, width=2)
txt(sz(-660.0), fy(1440.0), "AĞIZ", f7, RED, "mm")
d.rectangle([sz(-470.0), fy(T_KAS[1]), sz(-70.0), fy(T_KAS[0])], fill=BG, outline=INK, width=2)
txt(sz(-270.0), fy(1790.0) - 10, "KASET 140 × 400 × 360", f7, INK, "mm")
txt(sz(-270.0), fy(1790.0) + 10, "hazne kabini +3 °C", f7, GRAY, "mm")
d.rectangle([sz(-360.0), fy(T_BAS[1]), sz(-180.0), fy(T_BAS[0])], fill=SOFT, outline=INK, width=1)
txt(sz(-270.0), fy(1540.0), "NOZUL · POMPA", f7, INK, "mm")
d.rectangle([sz(-420.0), fy(1426.0), sz(-120.0), fy(1414.0)], fill=ACC, outline=ACC)
txt(sz(-270.0), fy(1395.0), "TABAN Ø300 · tepside", f7, ACC, "mm")
d.rectangle([sz(-780.0), fy(T_KAS[1] - 20), sz(-735.0), fy(T_KAS[0] + 20)], fill=EVC, outline=BUZ, width=1)
olcu_h(sz(-790), sz(-728.5), fy(1970) - 26, "62,5", f7, INK)
olcu_h(sz(-470), sz(-70), fy(1970) - 60, "kaset 400", f8, INK)
olcu_h(sz(-790), sz(40), fy(0) + 44, "830", f11, INK)
d.line([(sz(40), fy(0)), (sz(40 + KOR + 160), fy(0))], fill=INK, width=3)
d.rectangle([sz(RZ - 200), fy(15.0), sz(RZ + 200), fy(0)], fill=SOFT, outline=ACC, width=2)
d.rectangle([sz(RZ - 100), fy(KAIDE), sz(RZ + 100), fy(15.0)], fill=BG, outline=ACC, width=3)
txt(sz(RZ), fy(KAIDE / 2), "KAİDE|Ø200 · 820", f7, ACC, "mm")
for w_, c_ in ((16, BG), (9, ACC)):
    d.line([(sz(RZ), fy(OMUZ)), (sz(RZ + 120), fy(1600.0)), (sz(-60.0), fy(1430.0))], fill=c_, width=w_, joint="curve")
d.ellipse([sz(RZ) - 18, fy(OMUZ) - 18, sz(RZ) + 18, fy(OMUZ) + 18], fill=ACC, outline=BG, width=2)
txt(sz(RZ + 180), fy(OMUZ), "OMUZ 1000", f8, ACC, "lm")
txt(sz(RZ + 180), fy(1640.0), "ROBOT · FR10 · 1400 mm · 10 kg", f8, ACC, "lm")
olcu_h(sz(40), sz(40 + KOR), fy(0) + 46, "KORİDOR 800", f8, INK)
olcu_v(sz(40 + KOR + 100), fy(KAIDE), fy(0), "820", f8, INK, "r")
for yy in (120.0, BAND_UST, MOTOR[1], T_AGZ[1], T_KAS[0], 1970.0):
    d.line([(sz(-790) - 24, fy(yy)), (sz(-790) - 6, fy(yy))], fill=INK, width=2)
    txt(sz(-790) - 30, fy(yy), sayi(yy), f7, INK, "rm")


# ======================= YAN KESIT B · FIRIN KOLONU =======================
def sz2(z):
    return SX2 + (z + 790.0) * S


txt(SX2, FY_TOP - 190, "YAN KESİT B", f16, ACC)
txt(SX2, FY_TOP - 152, "M3 · fırın kolonu: 3 kapaklı hazne üst üste · kesici · yağ · robot kutusu", f9, GRAY)
d.rectangle([sz2(-790), fy(1970), sz2(40), fy(0)], fill=FILL, outline=LINE, width=3)
d.rectangle([sz2(-790), fy(120), sz2(40), fy(0)], fill=SOFT, outline=LINE, width=2)
d.rectangle([sz2(-728.5), fy(590.0), sz2(0.0), fy(123.0)], fill=SOFT, outline=LINE, width=1)
txt(sz2(-364.0), fy(356.0), "ROBOT KUTUSU · PLC", f7, GRAY, "mm")
d.rectangle([sz2(-728.5), fy(860.0), sz2(-400.0), fy(600.0)], fill=BG, outline=LINE, width=1)
txt(sz2(-564.0), fy(730.0), "YAĞ KABI", f7, INK, "mm")
d.rectangle([sz2(-400.0), fy(820.0), sz2(40.0), fy(640.0)], fill=AGZ, outline=RED, width=2)
txt(sz2(-180.0), fy(730.0), "SPREY AĞZI", f7, RED, "mm")
d.rectangle([sz2(-728.5), fy(1140.0), sz2(0.0), fy(870.0)], fill=BG, outline=LINE, width=1)
txt(sz2(-364.0), fy(1005.0), "KESİCİ · yıldız bıçak · piston", f7, INK, "mm")
for y0f, y1f, adf in ((1145.0, 1420.0, "HAZNE 1 · lahmacun"), (1425.0, 1700.0, "HAZNE 2 · lahmacun"), (1705.0, 1968.5, "HAZNE 3 · pide · pizza")):
    d.rectangle([sz2(-620.0), fy(y1f), sz2(-20.0), fy(y0f)], fill=SICAK, outline=INK, width=2)
    d.rectangle([sz2(-20.0), fy(y1f - 30), sz2(40.0), fy(y0f + 30)], fill=AGZ, outline=RED, width=2)
    txt(sz2(-320.0), fy((y0f + y1f) / 2) - 10, adf, f7, INK, "mm")
    txt(sz2(-320.0), fy((y0f + y1f) / 2) + 10, "600 derin · taş taban · alt + üst rezistans", f7, GRAY, "mm")
    d.rectangle([sz2(-780.0), fy(y1f - 40), sz2(-630.0), fy(y0f + 40)], fill=BG, outline=GRAY, width=1)
txt(sz2(-705.0), fy(1560.0), "EGZOZ", f7, GRAY, "mm")
txt(sz2(40) + 14, fy(1560.0), "MOTORLU KAPAK", f8, RED, "lm")
olcu_h(sz2(-620), sz2(-20), fy(1970) - 60, "hazne 600", f8, INK)
olcu_h(sz2(-790), sz2(40), fy(0) + 44, "830", f11, INK)
for yy in (120.0, 600.0, 870.0, 1145.0, 1425.0, 1705.0, 1970.0):
    d.line([(sz2(40) + 6, fy(yy)), (sz2(40) + 24, fy(yy))], fill=INK, width=2)
    txt(sz2(40) + 30, fy(yy), sayi(yy), f8, INK, "lm")
d.line([(sz2(40), fy(0)), (sz2(40 + 300), fy(0))], fill=INK, width=3)

# ======================= PARCA LISTESI =======================
TX, TY = SX, PY_TOP - 120
txt(TX, TY - 60, "PARÇA LİSTESİ  ·  ana kalemler", f16, ACC)
PARCA = [
    ("ROBOT", "Fairino FR10 · 1.400 mm · 10 kg · ±0,05", "2", "kaide Ø200 × 820 · plaka 400 × 400 · koridorda"),
    ("ROBOT UCU", "takım değiştirici · pençe · tepsi eli", "2 set", "uç istasyonu aktarma rafında"),
    ("AKTARMA", "tepsi rafı · 6 tepsi Ø340 · altında çöp 60 L", "1", "koridor · x 1900–2300"),
    ("ÇEKMECE", "soğutmalı çekmece 620 × 680 · motorlu", "24", "K1 8 pide · K2 6 lahm + 2 içecek · K3 6 lahm + içecek + tatlı"),
    ("MOTOR BANDI", "soğutma grubu 1,5 HP (yatık) ×2 + 3 evaporatör · sürücüler · pano", "1", "kot 1060–1360 · önden servis"),
    ("PRESS", "Fersah PZP-400 ısıtmalı pres başlığı", "1", "640 × 800 · platen Ø400 · 3,5 kW · kot 1360–1860"),
    ("TOPPING", "Atosa (Yindu) dozaj ünitesi · TABLA YOK · 8 hazne tek sıra", "1", "1400 × 830 · ölçü ve fiyat Yindu'dan bekleniyor"),
    ("TOPPING", "standart kaset 140 × 400 × 360 · 14 L", "6", "harç ×4 · kıyma · kuşbaşı"),
    ("TOPPING", "kaşar kabı 280 × 400 × 360 · karıştırıcılı · 28 L", "1", ""),
    ("TOPPING", "sucuk dilimleyici · çubuk Ø38 şarjörü", "1", "14 çubuk / 2 gün"),
    ("FIRIN", "kapaklı hazne 640 × 600 × 275 · taş taban", "3", "2 lahmacun 120 s · 1 pide / pizza 240 s"),
    ("FIRIN", "yıldız kesici + yağ spreyi", "1", "M3 alt · kot 600–1140"),
    ("KUTU", "kutu katlayan + şarjör · blank 400 × 760", "1", "555–665 kutu · kutu 320 × 320 × 45"),
    ("KONTROL", "R1 + R2 kontrol kutusu 245 × 180 × 45 · PLC + HMI", "1", "M3 robot kutusu 123–590"),
]
kol = (0, 150, 720, 830)
th = 30
d.rectangle([TX, TY, TX + 1300, TY + th * (len(PARCA) + 1)], fill=BG, outline=LINE, width=2)
d.rectangle([TX, TY, TX + 1300, TY + th], fill=SOFT, outline=LINE, width=1)
for cx_, h_ in zip(kol, ("İSTASYON", "PARÇA", "ADET", "NOT")):
    txt(TX + cx_ + 10, TY + th / 2, h_, f8, INK, "lm")
for i, (a_, b_, c_, e_) in enumerate(PARCA):
    yy = TY + th * (i + 1)
    d.line([(TX, yy), (TX + 1300, yy)], fill=SOFT, width=1)
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
cek = sum(g[0] for K in KOLON for g in K)
txt(W_PX - 170, ly, "HAT %s × 1970 × 830  ·  2 gün  ·  %d çekmece altta (8 pide · 12 lahmacun · 3 içecek · 1 tatlı)  ·  Atosa dozaj tablasız: 6 kaset + kaşar kabı + sucuk dilimleyici  ·  FIRIN 3 göz  ·  2 × FR10  ·  QR dolabı yok" % (sayi(HAT), cek), f9, GRAY, "rm")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.save(OUT)
print("yazildi:", OUT, "· hat %s mm · %d cekmece" % (sayi(HAT), cek))
