# -*- coding: utf-8 -*-
"""AUTOKITCH - HAT 2 KOL · TEKNIK RESIM v4 (17 Eyl 2026) — v3 Kemal: harc 2 kasete (kasar kalibi 280), motor bandi buyuk -> ic parcalari kesik cizgiyle, PZP zemin makinesi (katalog 640x800x950, 170 kg) -> PRESS tam boy kolon, cekmeceler TOPPING altinda 2 kolon, icecek KUTU altinda, teknik FIRIN altinda; lego moduller. — Kemal eskizi 2: PRESS | ATOSA TOPPING (tabla yok) ustte; altinda DOLAP MOTOR bandi + cekmeceler; sagda FIRIN x3 / KESICI / YAG / ROBOT KUTUSU; en sagda KUTU KATLAYAN. QR dolabi yok.: ON + UST (PLAN KESITI) + 2 YAN KESIT. Olculer mm.
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

OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE\HAT_2KOL_v4_teknik.png".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX = 5300, 3300
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
DZ = 830.0
WO, BIND, FUGA, BOLME, XI = 620.0, 15.0, 3.0, 35.0, 62.5
CELL0 = 182.5
YUZ0 = CELL0 - BIND
HH = {"hamur": 75.0, "lahm": 60.0, "icecek": 132.0}
AD = {"hamur": "TAZE PİDE", "lahm": "LAHMACUN", "icecek": "İÇECEK 330 ml"}
CAP = {"hamur": (20, "top"), "lahm": (35, "top"), "icecek": (90, "kutu")}
# MODULLER (lego): A PRESS kolonu · B CEKMECE modulu (TOPPING altinda) · C TOPPING modulu (B ustunde) · D FIRIN kolonu · E KUTU kolonu
W_A, W_BC, W_D, W_E = 700.0, 1400.0, 700.0, 700.0
X_A, X_BC, X_D, X_E = 0.0, 700.0, 2100.0, 2800.0
HAT = W_A + W_BC + W_D + W_E                                # 3500
KOLON = [[(8, "hamur"), (1, "lahm")], [(11, "lahm")]]        # B: 20 hamur cekmecesi, 2 kolon
KOLON_AD = ("K1", "K2")
H_B = 1200.0                                                # cekmece modulu yuksekligi (ust PU 1140-1200)
BAND_UST = YUZ0 + 11 * (60.0 + 2 * BIND + FUGA) - FUGA       # K2 ustu 1187,5
assert BAND_UST < H_B - 60.0 + 50.0
# C · TOPPING (Atosa dozaj unitesi, tabla yok): agiz · basliklar · hazne sirasi · sogutma
T_AGZ, T_BAS, T_KAS, T_SOG = (1210.0, 1320.0), (1323.0, 1457.0), (1460.0, 1820.0), (1830.0, 1968.5)
YUVA = [("HARÇ", 280.0, 170.0), ("HARÇ", 280.0, 450.0), ("KIYMA", 140.0, 660.0), ("KUŞBAŞI", 140.0, 800.0),
        ("KAŞAR KABI", 280.0, 1010.0), ("SUCUK|DİLİMLEYİCİ", 180.0, 1240.0)]
# A · PRESS kolonu (kotlar)
PZP = (120.0, 1070.0)                                       # Fersah PZP-400 zeminde (plint ustu): 640 x 800 x 950
PLAKA = 700.0                                               # alt plaka kotu (VARSAYIM - katalogda yok)
UC = (1080.0, 1230.0)
PANO_A = (1240.0, 1968.5)
# D · FIRIN kolonu
TEK = (123.0, 540.0)
YAG = (545.0, 790.0)
KES = (795.0, 1060.0)
FIR = [(1065.0, 1365.0, "FIRIN HAZNESİ 1|LAHMACUN · 120 s"), (1370.0, 1670.0, "FIRIN HAZNESİ 2|LAHMACUN · 120 s"),
       (1675.0, 1968.5, "FIRIN HAZNESİ 3|PİDE · PİZZA · 240 s · ayrı sıcaklık")]
# E · KUTU kolonu
E_CEK = [(2, "icecek")]
E_MEK = (505.0, 675.0)
E_AGZ = (685.0, 935.0)
E_SAR = (945.0, 1968.5)
R1X, R2X, RZ = 1150.0, 2800.0, 380.0
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
txt(OX, 70, "AUTOKITCH  ·  HAT 2 KOL  ·  TEKNİK RESİM  v4  ·  5 LEGO MODÜL  ·  PRESS ZEMİNDE  ·  ÇEKMECELER TOPPING ALTINDA  ·  ATOSA DOZAJ TABLA YOK  ·  FIRIN ×3  ·  KUTU KATLAYAN", f38, INK)
txt(OX, 138, "ön · üst · yan görünüş  ·  günde 80 pide + 200 lahmacun (+ pizza)  ·  2 gün stok  ·  20 hamur + 2 içecek çekmecesi  ·  harç 2 kaset (kaşar kalıbı 280)  ·  2 × Fairino FR10 koridorda  ·  QR dolabı yok  ·  tüm modüller 830 derin  ·  ölçüler mm  ·  17 Eylül 2026", f13, GRAY)
d.line([(OX, 178), (W_PX - 170, 178)], fill=LINE, width=3)

# ======================= ON GORUNUS =======================
txt(OX, FY_TOP - 190, "ÖN GÖRÜNÜŞ", f16, ACC)
txt(OX, FY_TOP - 152, "kesik çizgi = kapak arkası parça · robotlar koridorda önde, konumları zeminde işaretli", f9, GRAY)


def kabin(x0mm, w, y0, y1, ad=""):
    x0, x1 = fx(x0mm), fx(x0mm + w)
    d.rectangle([x0, fy(y1), x1, fy(y0)], fill=FILL, outline=LINE, width=4)
    if y0 == 0.0:
        d.rectangle([x0, fy(120), x1, fy(0)], fill=SOFT, outline=LINE, width=2)
    if ad:
        txt((x0 + x1) / 2, fy(1970) - 64, ad, f13, INK, "md")


def kapak(x0mm, a, b, y0, y1, et="", yl=None, fill=None):
    d.rectangle([fx(x0mm + a), fy(y1), fx(x0mm + b), fy(y0)], fill=(fill or BG), outline=LINE, width=2)
    if et:
        satirlar(fx(x0mm + (a + b) / 2), fy(yl if yl else (y0 + y1) / 2), et, f8, INK)


def agiz(x0mm, a, b, y0, y1, et):
    d.rectangle([fx(x0mm + a), fy(y1), fx(x0mm + b), fy(y0)], fill=AGZ, outline=RED, width=3)
    cy = (fy(y0) + fy(y1)) / 2
    txt(fx(x0mm + (a + b) / 2), cy - 10, et, f8, RED, "mm")
    txt(fx(x0mm + (a + b) / 2), cy + 12, "y %s – %s" % (sayi(y0), sayi(y1)), f7, RED, "mm")


def kesik(x0mm, a, b, y0, y1, et="", c=INK, alt=""):
    drect(fx(x0mm + a), fy(y1), fx(x0mm + b), fy(y0), c, 1)
    if et:
        txt(fx(x0mm + (a + b) / 2), fy((y0 + y1) / 2) - (8 if alt else 0), et, f7, c, "mm")
    if alt:
        txt(fx(x0mm + (a + b) / 2), fy((y0 + y1) / 2) + 10, alt, f7, GRAY, "mm")


def modul_etiketi(x0mm, w, y0, y1, ad, olcu):
    x0, x1 = fx(x0mm) + 6, fx(x0mm + w) - 6
    d.rectangle([x0, fy(0) + 126, x1, fy(0) + 172], fill=ACC)
    txt((x0 + x1) / 2, fy(0) + 140, ad, f8, BG, "mm")
    txt((x0 + x1) / 2, fy(0) + 160, olcu, f7, BG, "mm")


# --- A · PRESS kolonu
kabin(X_A, W_A, 0.0, 1970.0, "A · PRESS")
kapak(X_A, 33.0, 667.0, PZP[0] + 1.5, PZP[1])
kesik(X_A, 40.0, 660.0, 125.0, 600.0, "PZP-400 gövdesi · motor + rezistans · 3,5 kW", INK, "640 × 800 · 170 kg · zeminde")
d.ellipse([fx(X_A + 180), fy(PLAKA) - 4, fx(X_A + 520), fy(PLAKA) + 4], outline=INK, width=2)
txt(fx(X_A + 350), fy(PLAKA) + 16, "alt plaka Ø340 ısıtmalı · kot ~%s (varsayım)" % sayi(PLAKA), f7, GRAY, "mm")
agiz(X_A, 53.0, 647.0, PLAKA + 10.0, PLAKA + 220.0, "PRES AĞZI · tepsi alt plakaya")
kesik(X_A, 205.0, 495.0, PLAKA + 225.0, PLAKA + 275.0, "üst plaka Ø290", INK)
kesik(X_A, 40.0, 660.0, PLAKA + 280.0, PZP[1] - 5.0, "pres kafası · 2 kolon · kumanda", INK)
kapak(X_A, 33.0, 667.0, UC[0], UC[1])
kesik(X_A, 60.0, 250.0, UC[0] + 20.0, UC[1] - 20.0, "PENÇE", INK, "dock 130 × 200")
kesik(X_A, 270.0, 460.0, UC[0] + 20.0, UC[1] - 20.0, "YEDEK PENÇE", INK, "dock 130 × 200")
kesik(X_A, 480.0, 640.0, UC[0] + 20.0, UC[1] - 20.0, "boş", GRAY)
txt(fx(X_A + 350), fy(UC[1]) - 14, "UÇ YUVALARI · takım değiştirici · 150", f7, INK, "mm")
kapak(X_A, 33.0, 667.0, PANO_A[0], PANO_A[1])
kesik(X_A, 60.0, 560.0, 1290.0, 1900.0, "ANA PANO · PLC + HMI · sürücüler", INK, "500 × 610 × 250 · arka duvarda")
kesik(X_A, 575.0, 655.0, 1300.0, 1500.0, "", INK)
txt(fx(X_A + 615), fy(1400.0) - 8, "R1", f7, INK, "mm"); txt(fx(X_A + 615), fy(1400.0) + 8, "R2", f7, INK, "mm")
txt(fx(X_A + 615), fy(1290.0) + 12, "245 × 180 × 45", f7, GRAY, "mm")
txt(fx(X_A + 350), fy(PANO_A[1]) - 14, "PANO BÖLMESİ · 640 × 770 × 730 · önden kapak", f7, INK, "mm")
modul_etiketi(X_A, W_A, 0.0, 1970.0, "MODÜL A · PRESS KOLONU", "700 × 830 × 1970")
olcu_h(fx(X_A), fx(X_A + W_A), fy(1970) - 26, sayi(W_A), f11, INK)

# --- B · CEKMECE modulu (topping altinda)
kabin(X_BC, W_BC, 0.0, H_B)
d.rectangle([fx(X_BC + 30), fy(H_B - 60.0), fx(X_BC + W_BC - 30), fy(121.5)], fill=BG, outline=LINE, width=2)
d.rectangle([fx(X_BC + 30), fy(H_B - 1.5), fx(X_BC + W_BC - 30), fy(H_B - 60.0)], fill=PUC, outline=GRAY, width=1)
txt(fx(X_BC + W_BC / 2), fy(H_B - 30.0), "tavan PU 60 · üstünde MODÜL C oturur", f7, GRAY, "mm")
cx = X_BC + XI
for ki, gruplar in enumerate(KOLON):
    if ki:
        d.rectangle([fx(cx - BOLME), fy(H_B - 60.0), fx(cx), fy(YUZ0)], fill=SOFT, outline=LINE, width=1)
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
    txt(fx(cx + WO / 2), fy(H_B - 60.0) + 14, KOLON_AD[ki], f7, GRAY, "mm")
    olcu_h(fx(cx), fx(cx + WO), fy(0) + 44, "620", f8, GRAY)
    cx += WO + BOLME


# --- C · TOPPING modulu (B ustunde)
kabin(X_BC, W_BC, H_B, 1970.0, "C · ATOSA (YINDU) DOZAJ ÜNİTESİ · TABLA YOK")
agiz(X_BC, 30.0, 1370.0, T_AGZ[0], T_AGZ[1], "ROBOT AĞZI · tabanı robot tutar ve döndürür · tabla yok")
kapak(X_BC, 33.0, 1367.0, T_BAS[0], T_BAS[1], "DOZAJ BAŞLIKLARI · harç: piston pompa · kıyma / kuşbaşı: vida · kaşar: karıştırıcı + vida · sucuk: şarjör + bıçak")
kapak(X_BC, 33.0, 1367.0, T_KAS[0], T_KAS[1])
for urun, gw, xc in YUVA:
    kesik(X_BC, xc - gw / 2 + 6, xc + gw / 2 - 6, T_KAS[0] + 8, T_KAS[1] - 8)
    satirlar(fx(X_BC + xc), fy(1650.0) - 4, urun, f7, INK, 16)
    txt(fx(X_BC + xc), fy(1650.0) + 22, ("%s × 400 × 360" % sayi(gw)) if "SUCUK" not in urun else "180 × 400 · 14 çubuk", f7, GRAY, "mm")
txt(fx(X_BC + W_BC / 2), fy(T_KAS[1]) - 14, "HAZNE SIRASI · +3 °C · önden kaset takılır · kaset tabanı kot 1460", f7, INK, "mm")
kapak(X_BC, 33.0, 1367.0, T_SOG[0], T_SOG[1], "SOĞUTMA · hazne kabini evaporatörü + fan · 140")
d.line([(fx(X_BC), fy(H_B)), (fx(X_BC + W_BC), fy(H_B))], fill=LINE, width=4)
modul_etiketi(X_BC, W_BC, 0.0, 1970.0, "MODÜL B · ÇEKMECE (alt, 20 hamur çekmecesi)  +  MODÜL C · TOPPING (üst)", "B 1400 × 830 × 1200  ·  C 1400 × 830 × 770")
olcu_h(fx(X_BC), fx(X_BC + W_BC), fy(1970) - 26, sayi(W_BC), f11, INK)

# --- D · FIRIN kolonu
kabin(X_D, W_D, 0.0, 1970.0, "D · FIRIN · KESİCİ · YAĞ · TEKNİK")
kapak(X_D, 33.0, 667.0, TEK[0], TEK[1])
kesik(X_D, 50.0, 450.0, 150.0, 430.0, "SOĞUTMA GRUBU 1 (ön)", INK, "400 × 300 × 280 · 1/2 HP · çekmeceler")
kesik(X_D, 70.0, 470.0, 200.0, 480.0, "SOĞUTMA GRUBU 2 (arka)", GRAY, "hazne kabini")
kesik(X_D, 480.0, 650.0, 150.0, 500.0, "hava|filtre", GRAY)
txt(fx(X_D + 350), fy(TEK[1]) - 14, "TEKNİK · hava girişi ön, çıkışı arka · 640 × 770 × 420", f7, INK, "mm")
kapak(X_D, 33.0, 667.0, YAG[0], YAG[1])
agiz(X_D, 53.0, 420.0, YAG[0] + 35.0, YAG[1] - 35.0, "SPREY AĞZI · tepsi")
kesik(X_D, 440.0, 640.0, YAG[0] + 20.0, YAG[1] - 20.0, "YAĞ KARTUŞU|4 L × 2", INK, "160 × 160 × 180 · ısıtma ceketi")
kapak(X_D, 33.0, 667.0, KES[0], KES[1])
agiz(X_D, 53.0, 647.0, KES[0] + 5.0, KES[0] + 140.0, "KESİM AĞZI · tepsi yuvaya oturur")
kesik(X_D, 160.0, 540.0, KES[0] + 145.0, KES[0] + 245.0, "YILDIZ BIÇAK Ø300 · 6 dilim · piston 100 strok", INK)
for y0f, y1f, et in FIR:
    kapak(X_D, 33.0, 667.0, y0f, y1f, "", None, SICAK)
    kesik(X_D, 60.0, 640.0, y0f + 60.0, y1f - 60.0, "", INK)
    satirlar(fx(X_D + 350), fy((y0f + y1f) / 2), et, f8, INK)
    txt(fx(X_D + 350), fy(y0f + 30.0), "iç 400 × 400 × 100 · taş taban · motorlu kapak", f7, GRAY, "mm")
modul_etiketi(X_D, W_D, 0.0, 1970.0, "MODÜL D · FIRIN KOLONU", "700 × 830 × 1970")
olcu_h(fx(X_D), fx(X_D + W_D), fy(1970) - 26, sayi(W_D), f11, INK)

# --- E · KUTU kolonu
kabin(X_E, W_E, 0.0, 1970.0, "E · KUTU KATLAYAN")
d.rectangle([fx(X_E + 30), fy(500.0), fx(X_E + W_E - 30), fy(121.5)], fill=BG, outline=LINE, width=2)
cx = X_E + (W_E - WO) / 2.0
y = YUZ0
for adet, tip in E_CEK:
    h = HH[tip] + 2 * BIND
    ybas = y
    for _ in range(adet):
        d.rectangle([fx(cx + 8), fy(y + h), fx(cx + WO - 8), fy(y)], fill=BG, outline=DOLAP, width=1)
        y += h + FUGA
    ym = (fy(ybas) + fy(y - FUGA)) / 2
    etiket(fx(cx + WO / 2), ym - 13, "İÇECEK 330 ml × 2 (+ tatlı 14)", f8, INK, DOLAP)
    etiket(fx(cx + WO / 2), ym + 13, "180 kutu · +3 °C · 9 × 10 dizi", f7, DOLAP, DOLAP)
kapak(X_E, 33.0, 667.0, E_MEK[0], E_MEK[1])
kesik(X_E, 60.0, 400.0, E_MEK[0] + 15.0, E_MEK[1] - 15.0, "KALIP + PLUNGER · vantuz", INK, "blankı alttan çeker")
kesik(X_E, 420.0, 640.0, E_MEK[0] + 15.0, E_MEK[1] - 15.0, "VAKUM POMPASI", INK, "tahrik")
agiz(X_E, 30.0, 670.0, E_AGZ[0], E_AGZ[1], "KUTULAMA AĞZI · kutu 320 × 320 × 45")
kapak(X_E, 33.0, 667.0, E_SAR[0], E_SAR[1])
kesik(X_E, 150.0, 550.0, E_SAR[0] + 20.0, E_SAR[1] - 60.0, "", INK)
for i in range(12):
    yy = E_SAR[0] + 60.0 + i * 80.0
    d.line([(fx(X_E + 160), fy(yy)), (fx(X_E + 540), fy(yy))], fill=BOSL, width=1)
satirlar(fx(X_E + 350), fy(1450.0), "KUTU ŞARJÖRÜ|blank 400 × 760 yatay yığın · 1020 mm|= 570 (1,8 mm) – 680 (1,5 mm) kutu · 2 gün 560", f8, INK)
modul_etiketi(X_E, W_E, 0.0, 1970.0, "MODÜL E · KUTU KOLONU", "700 × 830 × 1970")
olcu_h(fx(X_E), fx(X_E + W_E), fy(1970) - 26, sayi(W_E), f11, INK)

olcu_h(fx(0), fx(HAT), fy(0) + 96, "HAT  %s" % sayi(HAT), f13, INK)
txt(fx(0) - 12, fy(0) + 149, "MODÜLLER", f8, ACC, "rm")
olcu_v(fx(0) - 44, fy(1970), fy(0), "1970", f11, INK, "l")
for yy in (120.0, PLAKA, PZP[1], H_B, T_AGZ[1], T_KAS[0], T_KAS[1], 1970.0):
    d.line([(fx(0) - 24, fy(yy)), (fx(0) - 6, fy(yy))], fill=INK, width=2)
    txt(fx(0) - 52, fy(yy), sayi(yy), f7, INK, "rm")
# birlesim isaretleri
for xj, et in ((X_BC, "A | B·C"), (X_D, "B·C | D"), (X_E, "D | E")):
    d.rectangle([fx(xj) - 5, fy(1970) - 12, fx(xj) + 5, fy(0) + 12], fill=BG, outline=None)
    dline((fx(xj), fy(1970) - 12), (fx(xj), fy(0) + 12), ACC, 3, 10, 6)
    txt(fx(xj), fy(1970) - 120, "BİRLEŞİM", f7, ACC, "mm")
    txt(fx(xj), fy(1970) - 104, et, f7, GRAY, "mm")
for rx, ad in ((R1X, "R1 · FR10"), (R2X, "R2 · FR10")):
    d.polygon([(fx(rx), fy(0) + 4), (fx(rx) - 14, fy(0) + 30), (fx(rx) + 14, fy(0) + 30)], fill=ACC)
    txt(fx(rx), fy(0) + 46, ad + " · koridorda, önde", f8, ACC, "mm")
    txt(fx(rx), fy(0) + 66, "x " + sayi(rx) + " · z +380", f7, GRAY, "mm")

# ======================= UST GORUNUS (PLAN KESITI) =======================
txt(OX, PY_TOP - 170, "ÜST GÖRÜNÜŞ  ·  PLAN KESİTİ  ·  robot erişimi", f16, ACC)
txt(fx(HAT / 2), py(-790) - 34, "ARKA", f9, GRAY, "mm")
zb = 40.0 - DZ
for x0m, w, ad in ((X_A, W_A, "A · PRESS"), (X_BC, W_BC, "B · ÇEKMECE + C · TOPPING"), (X_D, W_D, "D · FIRIN"), (X_E, W_E, "E · KUTU")):
    d.rectangle([fx(x0m), py(zb), fx(x0m + w), py(40.0)], fill=FILL, outline=LINE, width=3)
    txt(fx(x0m + w / 2), py(40.0) + 30, "%s  ·  %s × %s" % (ad, sayi(w), sayi(DZ)), f9, INK, "mm")
# A plan
d.rectangle([fx(X_A + 29), py(-788.0), fx(X_A + 669), py(12.0)], fill=BG, outline=INK, width=2)
d.ellipse([fx(X_A + 180), py(-570.0), fx(X_A + 520), py(-230.0)], outline=GRAY, width=1)
txt(fx(X_A + 350), py(-400.0), "FERSAH PZP-400", f8, INK, "mm")
txt(fx(X_A + 350), py(-370.0), "640 × 800 · alt plaka Ø340", f7, GRAY, "mm")
txt(fx(X_A + 350), py(-660.0), "üstte: uç yuvaları + ana pano", f7, GRAY, "mm")
# B/C plan
d.rectangle([fx(X_BC + 1.5), py(zb + 1.5), fx(X_BC + W_BC - 1.5), py(zb + 61.5)], fill=PUC, outline=GRAY, width=1)
cx = X_BC + XI
for ki in range(2):
    drect(fx(cx + 16), py(-680.0), fx(cx + WO - 16), py(0.0), DOLAP, 2)
    d.rectangle([fx(cx + 190), py(-725.0), fx(cx + 450), py(-680.0)], fill=EVC, outline=BUZ, width=1)
    d.rectangle([fx(cx + 17), py(-716.0), fx(cx + 67), py(-680.0)], fill=(255, 230, 230), outline=RED, width=1)
    txt(fx(cx + 320), py(-702.5), "EVAPORATÖR", f7, BUZ, "mm")
    txt(fx(cx + 42), py(-698.0), "M", f7, RED, "mm")
    txt(fx(cx + WO / 2), py(-640.0), "K%d · ÇEKMECE 620 × 680 · altta (B)" % (ki + 1), f7, DOLAP, "mm")
    cx += WO + BOLME
for urun, gw, xc in YUVA:
    d.rectangle([fx(X_BC + xc - gw / 2 + 6), py(-470.0), fx(X_BC + xc + gw / 2 - 6), py(-70.0)], fill=BG, outline=INK, width=2)
    satirlar(fx(X_BC + xc), py(-300.0), urun, f7, INK, 16)
    txt(fx(X_BC + xc), py(-250.0), "%s × 400" % sayi(gw), f7, GRAY, "mm")
d.rectangle([fx(X_BC + 30), py(-780.0), fx(X_BC + W_BC - 30), py(-740.0)], fill=EVC, outline=BUZ, width=1)
txt(fx(X_BC + W_BC / 2), py(-760.0), "EVAPORATÖR · hazne kabini (C)", f7, BUZ, "mm")
d.rectangle([fx(X_BC + 30), py(-60.0), fx(X_BC + W_BC - 30), py(0.0)], fill=AGZ, outline=RED, width=1)
txt(fx(X_BC + W_BC / 2), py(-30.0), "ROBOT AĞZI · kapaklı · 1340 × 110", f7, RED, "mm")
txt(fx(X_BC + W_BC / 2), py(-560.0), "C · ATOSA (YINDU) DOZAJ ÜNİTESİ · 6 hazne tek sıra · tabla yok · dozaj pompaları haznelerin arkasında (z −470…−740)", f7, INK, "mm")
# D plan
d.rectangle([fx(X_D + 30), py(-600.0), fx(X_D + 670), py(-20.0)], fill=SICAK, outline=INK, width=2)
drect(fx(X_D + 150), py(-500.0), fx(X_D + 550), py(-100.0), INK, 1)
txt(fx(X_D + 350), py(-325.0), "FIRIN · 3 HAZNE ÜST ÜSTE", f8, INK, "mm")
txt(fx(X_D + 350), py(-295.0), "dış 640 × 600 × 300 · iç 400 × 400 × 100", f7, GRAY, "mm")
d.rectangle([fx(X_D + 30), py(-780.0), fx(X_D + 670), py(-620.0)], fill=BG, outline=GRAY, width=1)
txt(fx(X_D + 350), py(-700.0), "EGZOZ KANALI · fan · karbon filtre · altta teknik", f7, GRAY, "mm")
# E plan
drect(fx(X_E + 150), py(-785.5), fx(X_E + 550), py(-25.5), GRAY, 1)
txt(fx(X_E + 350), py(-640.0), "BLANK 400 × 760 · üstte", f7, GRAY, "mm")
d.rectangle([fx(X_E + 190), py(-410.0), fx(X_E + 510), py(-90.0)], fill=BG, outline=INK, width=2)
txt(fx(X_E + 350), py(-265.0), "KUTU", f8, INK, "mm")
txt(fx(X_E + 350), py(-235.0), "320 × 320 × 45", f7, GRAY, "mm")
drect(fx(X_E + 56), py(-680.0), fx(X_E + 644), py(0.0), DOLAP, 1)
txt(fx(X_E + 350), py(-560.0), "altta: İÇECEK × 2 çekmece", f7, DOLAP, "mm")
olcu_h(fx(0), fx(HAT), py(40.0) + 96, "HAT  %s" % sayi(HAT), f13, INK)
olcu_v(fx(0) - 44, py(-790), py(40.0), sayi(DZ), f11, INK, "l")
d.line([(fx(-60), py(40.0 + KOR)), (fx(HAT + 60), py(40.0 + KOR))], fill=GRAY, width=1)
txt(fx(HAT / 2), py(40.0 + KOR) + 22, "ÖN  ·  robot koridoru %s" % sayi(KOR), f9, GRAY, "mm")
ax0, ax1, ay0, ay1 = AKT
d.rectangle([fx(ax0), py(160.0), fx(ax1), py(560.0)], fill=BG, outline=ACC, width=2)
txt(fx((ax0 + ax1) / 2), py(320.0), "AKTARMA RAFI", f8, ACC, "mm")
txt(fx((ax0 + ax1) / 2), py(365.0), "6 tepsi Ø340 · kot 900–1300", f7, GRAY, "mm")
txt(fx((ax0 + ax1) / 2), py(405.0), "altında çöp 60 L · üstünde tepsi eli yuvası", f7, GRAY, "mm")
for rx, ad in ((R1X, "R1 · FR10 · erişim 1400"), (R2X, "R2 · FR10 · erişim 1400")):
    cxp, cyp = fx(rx), py(RZ)
    d.rectangle([fx(rx - 200), py(RZ - 200), fx(rx + 200), py(RZ + 200)], fill=SOFT, outline=ACC, width=1)
    d.ellipse([cxp - 100 * S, cyp - 100 * S, cxp + 100 * S, cyp + 100 * S], fill=BG, outline=ACC, width=3)
    darc(cxp, cyp, ERISIM_P * S, 183.0, 357.0, ACC, 2, 3.0)
    darc(cxp, cyp, ERISIM * S, 190.0, 350.0, BOSL, 1, 2.5)
    txt(cxp, py(RZ + 200) + 22, ad, f9, ACC, "mm")
    txt(cxp, py(RZ + 200) + 46, "kaide 400 × 400 · eksen z +380 · pratik erişim 1250", f7, GRAY, "mm")
txt(fx(0) - 50, py(40.0) + 76, "yay: pratik 1250 (mavi) · nominal 1400 (gri)", f7, ACC, "la")
txt(fx(HAT / 2), py(RZ + 200) + 80, "R1: A + B + C (0–2100)  ·  R2: D + E (2100–3500)  ·  erişimler AKTARMA RAFI'nda kesişir  ·  FR5 (922) yetmiyor", f9, INK, "mm")


# ======================= YAN KESIT A · K2 / TOPPING =======================
def sz(z):
    return SX + (z + 790.0) * S


txt(SX, FY_TOP - 190, "YAN KESİT A", f16, ACC)
txt(SX, FY_TOP - 152, "K2 kolonundan: MODÜL B çekmeceler + MODÜL C Atosa dozaj · robot koridorda", f9, GRAY)
d.rectangle([sz(-790), fy(H_B), sz(40), fy(0)], fill=FILL, outline=LINE, width=4)
d.rectangle([sz(-790), fy(1970), sz(40), fy(H_B)], fill=FILL, outline=LINE, width=4)
d.rectangle([sz(-790), fy(120), sz(40), fy(0)], fill=SOFT, outline=LINE, width=2)
d.rectangle([sz(-788.5), fy(1968.5), sz(-728.5), fy(121.5)], fill=PUC, outline=GRAY, width=1)
d.rectangle([sz(-728.5), fy(1968.5), sz(0.0), fy(1908.5)], fill=PUC, outline=GRAY, width=1)
d.rectangle([sz(-728.5), fy(181.5), sz(0.0), fy(121.5)], fill=PUC, outline=GRAY, width=1)
d.rectangle([sz(-728.5), fy(H_B - 1.5), sz(0.0), fy(H_B - 60.0)], fill=PUC, outline=GRAY, width=1)
y0 = YUZ0
for adet, tip in KOLON[1]:
    h = HH[tip] + 2 * BIND
    for _ in range(adet):
        d.rectangle([sz(-680.0), fy(y0 + h), sz(0.0), fy(y0)], fill=BG, outline=DOLAP, width=1)
        d.rectangle([sz(0.0), fy(y0 + h), sz(40.0), fy(y0)], fill=BG, outline=DOLAP, width=1)
        y0 += h + FUGA
d.rectangle([sz(-728.5), fy(H_B - 60.0), sz(-680.0), fy(CELL0)], fill=(250, 250, 251), outline=GRAY, width=1)
txt(sz(-340), fy(640.0) - 10, "ÇEKMECE 680 · LAHMACUN × 11", f8, DOLAP, "mm")
txt(sz(-340), fy(640.0) + 12, "motorlu · ön sıra robota sunulur · arkada evaporatör plenumu", f7, GRAY, "mm")
txt(sz(-340), fy(H_B - 30.0), "B | C BİRLEŞİMİ · PU 60", f7, ACC, "mm")
d.rectangle([sz(-728.5), fy(T_AGZ[1]), sz(-10.0), fy(T_AGZ[0])], fill=AGZ, outline=None)
d.rectangle([sz(-10.0), fy(T_AGZ[1]), sz(40.0), fy(T_AGZ[0])], fill=AGZ, outline=RED, width=2)
txt(sz(-660.0), fy(1290.0), "AĞIZ", f7, RED, "mm")
d.rectangle([sz(-470.0), fy(T_KAS[1]), sz(-70.0), fy(T_KAS[0])], fill=BG, outline=INK, width=2)
txt(sz(-270.0), fy(1640.0) - 10, "KASET 280 × 400 × 360 (harç)", f7, INK, "mm")
txt(sz(-270.0), fy(1640.0) + 10, "hazne kabini +3 °C", f7, GRAY, "mm")
d.rectangle([sz(-360.0), fy(T_BAS[1]), sz(-180.0), fy(T_BAS[0])], fill=SOFT, outline=INK, width=1)
txt(sz(-270.0), fy(1390.0), "NOZUL", f7, INK, "mm")
drect(sz(-740.0), fy(T_KAS[1]), sz(-480.0), fy(T_BAS[0]), GRAY, 1)
txt(sz(-610.0), fy(1590.0) - 8, "POMPA · MOTOR", f7, GRAY, "mm")
txt(sz(-610.0), fy(1590.0) + 8, "haznenin arkasında", f7, GRAY, "mm")
d.rectangle([sz(-420.0), fy(1276.0), sz(-120.0), fy(1264.0)], fill=ACC, outline=ACC)
txt(sz(-270.0), fy(1245.0), "TABAN Ø300 · tepside", f7, ACC, "mm")
d.rectangle([sz(-728.5), fy(1908.5), sz(0.0), fy(T_SOG[0])], fill=EVC, outline=BUZ, width=1)
txt(sz(-364), fy(1880.0), "EVAPORATÖR + FAN · 140", f7, BUZ, "mm")
olcu_h(sz(-790), sz(-728.5), fy(1970) - 26, "62,5", f7, INK)
olcu_h(sz(-470), sz(-70), fy(1970) - 60, "kaset 400", f8, INK)
olcu_h(sz(-790), sz(40), fy(0) + 44, "830", f11, INK)
d.line([(sz(40), fy(0)), (sz(40 + KOR + 160), fy(0))], fill=INK, width=3)
d.rectangle([sz(RZ - 200), fy(15.0), sz(RZ + 200), fy(0)], fill=SOFT, outline=ACC, width=2)
d.rectangle([sz(RZ - 100), fy(KAIDE), sz(RZ + 100), fy(15.0)], fill=BG, outline=ACC, width=3)
txt(sz(RZ), fy(KAIDE / 2), "KAİDE|Ø200 · 820", f7, ACC, "mm")
for w_, c_ in ((16, BG), (9, ACC)):
    d.line([(sz(RZ), fy(OMUZ)), (sz(RZ + 120), fy(1560.0)), (sz(-60.0), fy(1280.0))], fill=c_, width=w_, joint="curve")
d.ellipse([sz(RZ) - 18, fy(OMUZ) - 18, sz(RZ) + 18, fy(OMUZ) + 18], fill=ACC, outline=BG, width=2)
txt(sz(RZ + 180), fy(OMUZ), "OMUZ 1000", f8, ACC, "lm")
txt(sz(RZ + 180), fy(1600.0), "ROBOT · FR10 · 1400 mm · 10 kg", f8, ACC, "lm")
olcu_h(sz(40), sz(40 + KOR), fy(0) + 46, "KORİDOR 800", f8, INK)
olcu_v(sz(40 + KOR + 100), fy(KAIDE), fy(0), "820", f8, INK, "r")
for yy in (120.0, H_B, T_AGZ[1], T_KAS[0], T_KAS[1], 1970.0):
    d.line([(sz(-790) - 24, fy(yy)), (sz(-790) - 6, fy(yy))], fill=INK, width=2)
    txt(sz(-790) - 30, fy(yy), sayi(yy), f7, INK, "rm")


# ======================= YAN KESIT B · FIRIN KOLONU =======================
def sz2(z):
    return SX2 + (z + 790.0) * S


txt(SX2, FY_TOP - 190, "YAN KESİT B", f16, ACC)
txt(SX2, FY_TOP - 152, "MODÜL D: teknik · yağ · kesici · 3 kapaklı hazne", f9, GRAY)
d.rectangle([sz2(-790), fy(1970), sz2(40), fy(0)], fill=FILL, outline=LINE, width=4)
d.rectangle([sz2(-790), fy(120), sz2(40), fy(0)], fill=SOFT, outline=LINE, width=2)
d.rectangle([sz2(-728.5), fy(TEK[1]), sz2(0.0), fy(TEK[0])], fill=SOFT, outline=LINE, width=1)
drect(sz2(-330.0), fy(430.0), sz2(-30.0), fy(150.0), INK, 1)
drect(sz2(-700.0), fy(480.0), sz2(-400.0), fy(200.0), INK, 1)
txt(sz2(-180.0), fy(290.0), "GRUP 1", f7, INK, "mm"); txt(sz2(-550.0), fy(340.0), "GRUP 2", f7, INK, "mm")
txt(sz2(-364.0), fy(510.0), "hava: ön giriş → arka çıkış", f7, GRAY, "mm")
d.rectangle([sz2(-728.5), fy(YAG[1]), sz2(-400.0), fy(YAG[0])], fill=BG, outline=LINE, width=1)
txt(sz2(-564.0), fy(667.0) - 8, "YAĞ KARTUŞU × 2", f7, INK, "mm"); txt(sz2(-564.0), fy(667.0) + 8, "160 × 160 × 180 · 45 °C", f7, GRAY, "mm")
d.rectangle([sz2(-400.0), fy(YAG[1] - 35), sz2(40.0), fy(YAG[0] + 35)], fill=AGZ, outline=RED, width=2)
txt(sz2(-180.0), fy(667.0), "SPREY AĞZI", f7, RED, "mm")
d.rectangle([sz2(-728.5), fy(KES[1]), sz2(0.0), fy(KES[0])], fill=BG, outline=LINE, width=1)
d.rectangle([sz2(-500.0), fy(KES[0] + 140), sz2(40.0), fy(KES[0] + 5)], fill=AGZ, outline=RED, width=2)
txt(sz2(-230.0), fy(KES[0] + 72), "KESİM AĞZI · yuva", f7, RED, "mm")
drect(sz2(-460.0), fy(KES[1] - 20), sz2(-100.0), fy(KES[0] + 145), INK, 1)
txt(sz2(-280.0), fy(KES[1] - 70), "BIÇAK + PİSTON", f7, INK, "mm")
for y0f, y1f, adf in FIR:
    d.rectangle([sz2(-620.0), fy(y1f), sz2(-20.0), fy(y0f)], fill=SICAK, outline=INK, width=2)
    d.rectangle([sz2(-520.0), fy(y1f - 100), sz2(-120.0), fy(y0f + 100)], fill=BG, outline=INK, width=1)
    d.rectangle([sz2(-20.0), fy(y1f - 40), sz2(40.0), fy(y0f + 40)], fill=AGZ, outline=RED, width=2)
    txt(sz2(-320.0), fy((y0f + y1f) / 2), "iç 400 × 100 · taş", f7, INK, "mm")
    txt(sz2(-320.0), fy(y1f - 45), adf.split("|")[0], f7, GRAY, "mm")
    d.rectangle([sz2(-780.0), fy(y1f - 40), sz2(-630.0), fy(y0f + 40)], fill=BG, outline=GRAY, width=1)
txt(sz2(-705.0), fy(1520.0), "EGZOZ", f7, GRAY, "mm")
txt(sz2(40) + 14, fy(1520.0), "MOTORLU KAPAK", f8, RED, "lm")
olcu_h(sz2(-620), sz2(-20), fy(1970) - 60, "hazne 600", f8, INK)
olcu_h(sz2(-790), sz2(40), fy(0) + 44, "830", f11, INK)
for yy in (120.0, TEK[1], YAG[1], KES[1], FIR[0][1], FIR[1][1], 1970.0):
    d.line([(sz2(40) + 6, fy(yy)), (sz2(40) + 24, fy(yy))], fill=INK, width=2)
    txt(sz2(40) + 30, fy(yy), sayi(yy), f8, INK, "lm")
d.line([(sz2(40), fy(0)), (sz2(40 + 300), fy(0))], fill=INK, width=3)

# ======================= MODUL + PARCA LISTESI =======================
TX, TY = SX, PY_TOP - 120
txt(TX, TY - 60, "MODÜLLER (lego · cıvatalı flanşla birleşir)  ·  PARÇA LİSTESİ", f16, ACC)
PARCA = [
    ("MODÜL A", "PRESS kolonu · Fersah PZP-400 + uç yuvaları + ana pano", "1", "700 × 830 × 1970 · 170 kg pres zeminde"),
    ("MODÜL B", "ÇEKMECE modülü · 20 hamur çekmecesi · 2 kolon", "1", "1400 × 830 × 1200 · K1 8 pide + 1 lahm · K2 11 lahm"),
    ("MODÜL C", "TOPPING · Atosa (Yindu) dozaj ünitesi · tabla yok", "1", "1400 × 830 × 770 · B'nin üstüne oturur"),
    ("MODÜL D", "FIRIN kolonu · teknik + yağ + kesici + 3 hazne", "1", "700 × 830 × 1970"),
    ("MODÜL E", "KUTU kolonu · 2 içecek çekmecesi + katlayıcı + şarjör", "1", "700 × 830 × 1970"),
    ("ROBOT", "Fairino FR10 · 1400 mm · 10 kg · ±0,05", "2", "kaide Ø200 × 820 · koridorda x 1150 / 2800"),
    ("ROBOT UCU", "pençe ×2 (dock A) · tepsi eli · takım değiştirici", "2 set", "tepsi eli yuvası aktarma rafında"),
    ("AKTARMA", "tepsi rafı · 6 tepsi Ø340 · altında çöp 60 L", "1", "koridor · x 1900–2300"),
    ("ÇEKMECE", "soğutmalı çekmece 620 × 680 · motorlu", "22", "20 hamur (B) + 2 içecek (E, 90 kutu + tatlı)"),
    ("SOĞUTMA", "soğutma grubu 1/2 HP 400 × 300 × 280", "2", "D altı · evaporatörler B arkası + C üstü"),
    ("TOPPING", "harç kaseti 280 × 400 × 360 · 28 L (kaşar kalıbı)", "2", "21,6 kg harç + 3,5 kg kap = 25 kg — ağır!"),
    ("TOPPING", "standart kaset 140 × 400 × 360 · 14 L", "2", "kıyma 6,4 kg · kuşbaşı 5,8 kg"),
    ("TOPPING", "kaşar kabı 280 × 400 × 360 · karıştırıcılı", "1", "8,8 kg"),
    ("TOPPING", "sucuk dilimleyici · 14 çubuk Ø38", "1", "180 × 400"),
    ("FIRIN", "kapaklı hazne dış 640 × 600 × 300 · iç 400 × 400 × 100 · taş", "3", "ref. Omake FPZ01 çift katlı 64 × 60 × 56"),
    ("FIRIN", "yıldız kesici Ø300 + piston · yağ kartuşu 4 L × 2 + sprey", "1", "kesim 795–1060 · yağ 545–790"),
    ("KUTU", "katlayıcı (kalıp + plunger + vakum) + şarjör 1020", "1", "blank 400 × 760 · 570–680 kutu"),
    ("KONTROL", "ana pano PLC + HMI · R1/R2 kontrol kutuları 245 × 180 × 45", "1", "A üst pano bölmesi"),
]
kol = (0, 130, 700, 800)
th = 30
d.rectangle([TX, TY, TX + 1320, TY + th * (len(PARCA) + 1)], fill=BG, outline=LINE, width=2)
d.rectangle([TX, TY, TX + 1320, TY + th], fill=SOFT, outline=LINE, width=1)
for cx_, h_ in zip(kol, ("İSTASYON", "PARÇA", "ADET", "NOT")):
    txt(TX + cx_ + 10, TY + th / 2, h_, f8, INK, "lm")
for i, (a_, b_, c_, e_) in enumerate(PARCA):
    yy = TY + th * (i + 1)
    d.line([(TX, yy), (TX + 1320, yy)], fill=SOFT, width=1)
    for cx_, s_ in zip(kol, (a_, b_, c_, e_)):
        txt(TX + cx_ + 10, yy + th / 2, s_, f8 if cx_ != 800 else f7, INK if cx_ != 800 else GRAY, "lm")

# ======================= LEJANT =======================
d.line([(OX, H_PX - 130), (W_PX - 170, H_PX - 130)], fill=LINE, width=2)
ly = H_PX - 78
LEJ = [(LINE, BG, "kapak / panel", False), (RED, AGZ, "açık ağız · kapak", False), (DOLAP, BG, "çekmece +3 °C", False),
       (INK, SICAK, "fırın haznesi", False), (GRAY, PUC, "PU yalıtım", False), (INK, BG, "kapak arkası parça", True), (ACC, BG, "modül birleşimi · robot", True)]
xx = OX
for c, fl, a_, kes in LEJ:
    if kes:
        drect(xx, ly - 12, xx + 30, ly + 12, c, 2)
    else:
        d.rectangle([xx, ly - 12, xx + 30, ly + 12], fill=fl, outline=c, width=3)
    txt(xx + 42, ly, a_, f9, INK, "lm")
    xx += 42 + d.textlength(a_, font=f9) + 56
txt(W_PX - 170, ly, "HAT %s × 1970 × 830  ·  5 modül  ·  2 gün  ·  22 çekmece (8 pide · 12 lahmacun · 2 içecek + tatlı)  ·  Atosa dozaj tablasız: 2 harç 280 + kıyma + kuşbaşı + kaşar 280 + sucuk dilimleyici  ·  FIRIN 3 göz  ·  2 × FR10  ·  QR dolabı yok" % sayi(HAT), f9, GRAY, "rm")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.save(OUT)
print("yazildi:", OUT, "· hat %s mm" % sayi(HAT))
