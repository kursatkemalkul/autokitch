# -*- coding: utf-8 -*-
"""TOPPING · TEKNİK DOLAP YERLEŞİMİ v1 (öneri) — ÖN GÖRÜNÜŞ A + C · A YAN KESİT · A ÜST GÖRÜNÜŞ · 25 Eyl 2026
Kemal: "soğuk hazne düz kutu (yanlar, arka, alt dolap gibi yalıtımlı, sac tam kapatsın) — o zaman sağ üstteki UPS vb. ne olacak;
kompresörün başka istasyonda (K) olması hoşuma gitmedi; ağır parçaları üste koysak çok mu ağır, sığmaz da. Karar veremedim."

Öneri: teknik parçalar AÇICI modülünün (A) boş üst yarısında (1450–2030). Açıcı zaten TOPPING'in tablasıyla çalışıyor
(topping_cad_v22'de, tabla altında parkta) → A + C tek istasyon sayılırsa kural (feedback_istasyon_kapali_urun) bozulmaz.
Ölçü kaynakları: pafta HAT_ATOSA_TABLALI v8 (A 0–700, C 700–2500, B 0–2500, açıcı kolonu x 290–410 · 1060–1440, kafa 1310,
hamur ağzı 1168–1388) · topping_cad_v22 (açıcı z: kolon −610…−660, kafa −500…+180) · store_cad_v4 (Secop CU KLF4.0CND
350 × 272 × 450, 15,2 kg, secop.com) · topping_uno_cad_v4 (JUN-AIR OF302-15B 380 × 380 × 510, 25 kg).
Kompresör A'da Secop'la birlikte SIĞMIYOR (plan: 694 − 10 − 450 − 10 = 224 < 380) — paftada kırmızı kesik.
3B modele dokunulmadı (Kemal onayı bekleniyor).
"""
import math, os
from PIL import Image, ImageDraw, ImageFont
U = os.path.dirname(os.path.abspath(__file__)); KOK = os.path.dirname(os.path.dirname(U))
CIKTI = os.path.join(KOK, "arastirma", "FULL_MAKINE", "TEKNIK_DOLAP_v1_teknik.png")

INK, GRI, ACIK = (25, 25, 28), (120, 124, 130), (205, 208, 212)
PU, PUC = (246, 232, 180), (214, 188, 118)
PAS, BEL, BIZ, SOG = (206, 211, 218), (228, 231, 236), (214, 230, 250), (240, 247, 253)
KIR, MAVI, YES, BAKIR = (200, 30, 30), (30, 90, 170), (30, 130, 70), (190, 110, 50)
TEK_Z, TEK_P, TEK_C = (255, 244, 230), (250, 216, 172), (196, 110, 30)
W, H = 3000, 1840
im = Image.new("RGB", (W, H), (255, 255, 255)); d = ImageDraw.Draw(im)
fn = lambda n, b=False: ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf" if b else "C:/Windows/Fonts/arial.ttf", n)
fB, fG, fE, fO, fK, fS = fn(40, True), fn(27, True), fn(20), fn(19), fn(21, True), fn(16)

# ---------------------------------------------------------------- ölçüler (mm, hat koordinatı)
X_A0, X_A1, X_C0, X_C1 = 0.0, 700.0, 700.0, 2500.0
H_B, H_MAK, Y_ALT = 1060.0, 2030.0, 123.0
DOLAP_TABAN = 1450.0                                  # açıcı kolonu 1440'ta biter
DI0, DI1 = 3.0, 697.0                                 # A iç genişliği (1,5 sac + pay) → 694
SEC = dict(x=(13.0, 463.0), z=(-820.0, -470.0), y=(1470.0, 1742.0))     # Secop 350 × 272 × 450, fanı sola bakacak şekilde 90° çevrik
PANO_Z = -250.0                                       # DIN montaj plakası
ARA_Z = -460.0                                        # ısı perdesi
KOMP = 380.0                                          # JUN-AIR OF302-15B taban 380 × 380
# soğuk kutu (C yerel + 700)
KX0, KX1, KB_ALT, KB_UST, KD_UST, KK_UST = 728.0, 2472.0, 1276.0, 1320.0, 1852.0, 1914.0
KAPAK_BOL = [(728.0, 1490.0), (1490.0, 1910.0), (1910.0, 2472.0)]
ACIK_UST = 2499.0
UNO = [("SOS", 910, 220, 1737), ("HARÇ", 1260, 440, 1832), ("KIYMA", 1595, 190, 1667), ("KUŞBAŞI", 1805, 190, 1667)]
KAS = [("KAŞAR", 1920, 2202, 1680), ("SUCUK", 2222, 2364, 1680)]


def tara(x0, y0, x1, y1, adim=9, renk=PUC, dolgu=PU):
    x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1))
    d.rectangle([x0, y0, x1, y1], fill=dolgu); h = y1 - y0; k = x0 - h
    while k < x1:
        a = max(k, x0); b = min(k + h, x1)
        if b > a: d.line([(a, y1 - (a - k)), (b, y1 - (b - k))], fill=renk, width=1)
        k += adim
    d.rectangle([x0, y0, x1, y1], outline=renk, width=1)


def kutu(x0, y0, x1, y1, fill=None, renk=INK, w=2):
    x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1))
    d.rectangle([x0, y0, x1, y1], fill=fill, outline=renk, width=w)


def kesik(p0, p1, renk=INK, w=2, a=12, b=7):
    (x0, y0), (x1, y1) = p0, p1; L = math.hypot(x1 - x0, y1 - y0)
    if L < 1: return
    ux, uy = (x1 - x0) / L, (y1 - y0) / L; t = 0.0
    while t < L:
        t1 = min(L, t + a); d.line([(x0 + ux * t, y0 + uy * t), (x0 + ux * t1, y0 + uy * t1)], fill=renk, width=w); t = t1 + b


def kesik_kutu(x0, y0, x1, y1, renk=INK, w=2):
    x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1))
    for p, q in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))): kesik(p, q, renk, w)


def ok(x, y, dx, dy, renk=INK, n=12):
    L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
    d.polygon([(x, y), (x - ux * n - uy * n * 0.42, y - uy * n + ux * n * 0.42), (x - ux * n + uy * n * 0.42, y - uy * n - ux * n * 0.42)], fill=renk)


def olcu_x(y, x0, x1, t, renk=INK, alt=False):
    d.line([(x0, y), (x1, y)], fill=renk, width=2); ok(x0, y, -1, 0, renk); ok(x1, y, 1, 0, renk)
    tw = d.textlength(t, font=fO); ty = y + 4 if alt else y - 24
    d.rectangle([(x0 + x1) / 2 - tw / 2 - 3, ty, (x0 + x1) / 2 + tw / 2 + 3, ty + 21], fill=(255, 255, 255))
    d.text(((x0 + x1) / 2 - tw / 2, ty), t, font=fO, fill=renk)


def olcu_y(x, y0, y1, t, renk=INK, sol=False):
    d.line([(x, y0), (x, y1)], fill=renk, width=2); ok(x, min(y0, y1), 0, -1, renk); ok(x, max(y0, y1), 0, 1, renk)
    tw = d.textlength(t, font=fO); tx = x - tw - 8 if sol else x + 8
    d.rectangle([tx - 2, (y0 + y1) / 2 - 12, tx + tw + 2, (y0 + y1) / 2 + 11], fill=(255, 255, 255))
    d.text((tx, (y0 + y1) / 2 - 11), t, font=fO, fill=renk)


def uzat(x0, y0, x1, y1):
    d.line([(x0, y0), (x1, y1)], fill=ACIK, width=1)


def et(px, py, hx, hy, t, renk=INK, f=None):
    f = f or fE
    d.line([(px, py), (hx, hy)], fill=GRI, width=1); d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=GRI)
    tw = d.textlength(t, font=f); x = hx + 6
    d.rectangle([x - 3, hy - 13, x + tw + 3, hy + 13], fill=(255, 255, 255)); d.text((x, hy - 12), t, font=f, fill=renk)


def ortala(t, x, y, f=fO, renk=INK):
    d.text((x - d.textlength(t, font=f) / 2, y), t, font=f, fill=renk)


def panjur(x0, y0, x1, y1, dikey=True):
    kutu(x0, y0, x1, y1, fill=(255, 255, 255), renk=TEK_C, w=1)
    if dikey:
        yy = y0 + 5
        while yy < y1 - 3: d.line([(x0 + 1, yy), (x1 - 1, yy + 3)], fill=TEK_C, width=2); yy += 9
    else:
        xx = x0 + 5
        while xx < x1 - 3: d.line([(xx, y0 + 1), (xx + 3, y1 - 1)], fill=TEK_C, width=2); xx += 9


d.text((60, 28), "TOPPING · TEKNİK DOLAP YERLEŞİMİ v1 (öneri) — soğutma + pano AÇICI modülünün boş üst yarısında", font=fB, fill=INK)
d.text((60, 82), "ölçüler mm · kotlar yerden · turuncu = teknik dolap · mavi = soğuk kutu · kırmızı = sığmayan · "
       "A ile C tek istasyon (AÇICI + TOPPING) sayılarak · hava yerine elektrikli UNO varsayımıyla", font=fE, fill=GRI)

# ================================================================ ÖN GÖRÜNÜŞ · A + C
S = 0.52; OY = 1735
X = lambda x: 190 + S * x
Y = lambda y: OY - S * y
d.text((60, 150), "ÖN GÖRÜNÜŞ · A + C (dolap kapağı kaldırılmış)", font=fG, fill=INK)
d.line([(X(-80), Y(0)), (X(2580), Y(0))], fill=INK, width=3)
# B
kutu(X(0), Y(Y_ALT), X(2500), Y(H_B), renk=GRI, w=1); kutu(X(30), Y(0), X(2470), Y(Y_ALT), renk=GRI, w=1)
ortala("B · ÇEKMECELER (kendi soğutması + panosu var · dokunulmuyor)", X(1250), Y(620), fO, GRI)
# A kabini + açıcı
kutu(X(X_A0), Y(H_B), X(X_A1), Y(H_MAK), renk=INK, w=2)
kesik_kutu(X(53), Y(1168), X(647), Y(1388), GRI, 1); ortala("hamur ağzı", X(170), Y(1388) + 4, fS, GRI)
kutu(X(290), Y(H_B), X(410), Y(1440), fill=BEL, renk=INK, w=1)
kutu(X(270), Y(1310), X(430), Y(1322), fill=PAS, renk=INK, w=1)
kutu(X(305), Y(1176), X(395), Y(1264), fill=BEL, renk=INK, w=1)
kutu(X(180), Y(1154), X(520), Y(1176), fill=(250, 226, 196), renk=INK, w=1)
ortala("AÇICI", X(350), Y(1440) - 24, fK)
# teknik dolap (kapak kaldırılmış)
d.rectangle([X(DI0), Y(H_MAK - 3), X(DI1), Y(DOLAP_TABAN + 10)], fill=TEK_Z)
kutu(X(DI0), Y(DOLAP_TABAN + 10), X(DI1), Y(DOLAP_TABAN), fill=PAS, renk=INK, w=1)
kesik_kutu(X(33), Y(2010), X(667), Y(1470), TEK_C, 2)
kesik_kutu(X(SEC["x"][0]), Y(SEC["y"][1]), X(SEC["x"][1]), Y(SEC["y"][0]), INK, 2)       # Secop plakanın arkasında
d.rectangle([X(SEC["x"][0]) + 2, Y(1640) + 1, X(SEC["x"][1]) - 2, Y(SEC["y"][0]) - 2], fill=(92, 96, 104))
ortala("soğutma grubu (arkada)", X(238), Y(1560) - 2, fS, (255, 255, 255))
kutu(X(13), Y(2018), X(687), Y(1650), fill=(250, 250, 250), renk=TEK_C, w=2)                  # DIN montaj plakası
for yr in (1965.0, 1845.0, 1725.0): d.line([(X(20), Y(yr)), (X(680), Y(yr))], fill=GRI, width=2)
for (a, b, t) in ((25, 300, "PLC + G/Ç"), (315, 505, "UPS + akü"), (520, 680, "güç 24 V")):
    kutu(X(a), Y(2005), X(b), Y(1925), fill=TEK_P, renk=TEK_C, w=1); ortala(t, X((a + b) / 2), Y(1965) - 10, fS)
for i in range(18):
    a = 40 + i * 33.0; kutu(X(a), Y(1885), X(a + 28), Y(1805), fill=(40, 90, 60), renk=INK, w=1)
ortala("sürücüler × 18", X(350), Y(1805) + 2, fS)
for i in range(40):
    a = 30 + i * 16.0; kutu(X(a), Y(1760), X(a + 12), Y(1690), fill=(235, 235, 235), renk=GRI, w=1)
ortala("klemens + röle", X(350), Y(1690) + 2, fS)
panjur(X(0) - 12, Y(1740), X(0), Y(1475))
# C · soğuk kutu (düz kutu) + tabla yolu + açılma alanı
kutu(X(X_C0), Y(H_B), X(X_C1), Y(H_MAK), renk=INK, w=2)
tara(X(KX0), Y(KK_UST), X(KX1), Y(KB_ALT))
d.rectangle([X(KX0 + 62), Y(KD_UST), X(KX1 - 62), Y(KB_UST)], fill=SOG)
for (a, b) in KAPAK_BOL: kutu(X(a + 2), Y(KK_UST), X(b - 2), Y(KD_UST), renk=INK, w=1)
kutu(X(KX0), Y(KK_UST), X(KX1), Y(KB_ALT), renk=MAVI, w=3)
for n, cx, w, ust in UNO:
    p = [(X(cx - 32), Y(1452)), (X(cx + 32), Y(1452)), (X(cx + w / 2), Y(1632)), (X(cx + w / 2), Y(ust)), (X(cx - w / 2), Y(ust)), (X(cx - w / 2), Y(1632))]
    for i_ in range(len(p)): kesik(p[i_], p[(i_ + 1) % len(p)], MAVI, 1, 7, 5)
    ortala(n, X(cx), Y(ust) + 4, fS, MAVI)
for n, x0, x1, ust in KAS:
    kesik_kutu(X(x0), Y(ust), X(x1), Y(1328), MAVI, 1); ortala(n, X((x0 + x1) / 2), Y(ust) + 4, fS, MAVI)
ortala("SOĞUK KUTU +3 °C · düz kutu", X(1600), Y(1440), fK, MAVI)
ortala("4 yan + alt 60 PU · dışı tam sac · üstte 3 contalı kapak", X(1600), Y(1440) + 28, fS, MAVI)
for cx in (910, 1260, 1595, 1805, 2061, 2293):
    kutu(X(cx - 14), Y(KB_ALT), X(cx + 14), Y(1200), fill=BEL, renk=INK, w=1)
kesik((X(X_C0), Y(1165)), (X(X_C1), Y(1165)), GRI, 2)
ortala("tabla yolu", X(2380), Y(1165) + 4, fS, GRI)
kesik_kutu(X(KX0), Y(ACIK_UST), X(KX1), Y(KK_UST), GRI, 1)
ortala("kapak açılma alanı · BOŞ KALIR (üste bir şey konmaz)", X(1600), Y(2230), fK, GRI)
# boru + kablo A → C
kesik((X(470), Y(1600)), (X(KX0 + 30), Y(1600)), BAKIR, 3, 10, 6); ok(X(KX0 + 30), Y(1600), 1, 0, BAKIR)
kesik((X(690), Y(1950)), (X(800), Y(1950)), INK, 3, 10, 6); ok(X(800), Y(1950), 1, 0, INK)
# ölçüler + kotlar
yo = Y(0) + 34
for x_ in (0.0, 700.0, 2500.0): uzat(X(x_), Y(0) + 6, X(x_), yo + 8)
olcu_x(yo, X(0), X(700), "A 700", alt=True); olcu_x(yo, X(700), X(2500), "C 1800", alt=True)
olcu_y(X(0) - 60, Y(DOLAP_TABAN), Y(H_MAK), "580", sol=True)
for y_ in (0.0, Y_ALT, H_B, DOLAP_TABAN, KB_ALT, KK_UST, H_MAK, ACIK_UST):
    d.line([(X(-20), Y(y_)), (X(-6), Y(y_))], fill=GRI, width=1)
    t = "%.0f" % y_; d.text((X(-24) - d.textlength(t, font=fS), Y(y_) - 9), t, font=fS, fill=(KIR if y_ == ACIK_UST else INK))
# istasyon parantezi
yb = Y(2600)
d.line([(X(0), yb + 14), (X(0), yb), (X(2500), yb), (X(2500), yb + 14)], fill=TEK_C, width=3)
ortala("A + C = TEK İSTASYON (AÇICI + TOPPING) · açıcı TOPPING'in tablası üstünde çalışıyor", X(1250), yb - 28, fK, TEK_C)

# ================================================================ A · YAN KESİT (x 240, Secop'tan geçer)
S2 = 0.72
Zs = lambda z: 1600 + (z + 830.0) * S2
Y2 = lambda y: 1010 - (y - 1040.0) * S2
d.text((1600, 150), "A · YAN KESİT (arka solda · ön sağda)", font=fG, fill=INK)
kutu(Zs(-830), Y2(H_B), Zs(0), Y2(H_MAK), renk=INK, w=2)
# açıcı
kutu(Zs(-660), Y2(H_B), Zs(-610), Y2(1440), fill=BEL, renk=INK, w=1)
kutu(Zs(-660), Y2(1410), Zs(-490), Y2(1440), fill=BEL, renk=INK, w=1)
kutu(Zs(-500), Y2(1310), Zs(180), Y2(1322), fill=PAS, renk=INK, w=1)
d.polygon([(Zs(-170), Y2(1176)), (Zs(-30), Y2(1221)), (Zs(-30), Y2(1176))], fill=BEL, outline=INK)
d.polygon([(Zs(-170), Y2(1176)), (Zs(-310), Y2(1221)), (Zs(-310), Y2(1176))], fill=BEL, outline=INK)
kutu(Zs(-340), Y2(1154), Zs(0), Y2(1176), fill=(250, 226, 196), renk=INK, w=1)
d.rectangle([Zs(0) - 2, Y2(1388), Zs(0) + 2, Y2(1168)], fill=(255, 255, 255))
ortala("açıcı", Zs(-560), Y2(1300), fS)
# dolap
d.rectangle([Zs(-827), Y2(H_MAK - 3), Zs(-3), Y2(DOLAP_TABAN + 10)], fill=TEK_Z)
kutu(Zs(-827), Y2(DOLAP_TABAN + 10), Zs(-3), Y2(DOLAP_TABAN), fill=PAS, renk=INK, w=1)
kutu(Zs(SEC["z"][0]), Y2(SEC["y"][1]), Zs(SEC["z"][1]), Y2(SEC["y"][0]), fill=(92, 96, 104), renk=INK, w=2)
d.ellipse([Zs(-700), Y2(1640), Zs(-580), Y2(1520)], outline=(200, 200, 205), width=2)
ortala("Secop", (Zs(-820) + Zs(-470)) / 2, Y2(1742) + 6, fS, (255, 255, 255))
d.line([(Zs(ARA_Z), Y2(DOLAP_TABAN + 10)), (Zs(ARA_Z), Y2(H_MAK - 3))], fill=INK, width=3)
kutu(Zs(PANO_Z - 3), Y2(2018), Zs(PANO_Z), Y2(1650), fill=PAS, renk=INK, w=1)
for (y0_, y1_) in ((1925.0, 2005.0), (1805.0, 1885.0), (1690.0, 1760.0)):
    kutu(Zs(PANO_Z), Y2(y1_), Zs(-120), Y2(y0_), fill=TEK_P, renk=TEK_C, w=1)
kutu(Zs(-20), Y2(2010), Zs(0), Y2(1470), fill=(236, 236, 240), renk=INK, w=2)
d.ellipse([Zs(-10) - 5, Y2(1480) - 5, Zs(-10) + 5, Y2(1480) + 5], fill=INK)
panjur(Zs(SEC["z"][0]), Y2(H_MAK) - 8, Zs(SEC["z"][1]), Y2(H_MAK) + 4, dikey=False)
for zz in (-760, -645, -530):
    d.line([(Zs(zz), Y2(1760)), (Zs(zz), Y2(2080))], fill=KIR, width=2); ok(Zs(zz), Y2(2080), 0, -1, KIR)
# ölçüler
yz = Y2(H_MAK) - 40
for z_ in (-830.0, ARA_Z, PANO_Z, 0.0): uzat(Zs(z_), Y2(H_MAK), Zs(z_), yz - 8)
olcu_x(yz, Zs(-830), Zs(ARA_Z), "370"); olcu_x(yz, Zs(ARA_Z), Zs(PANO_Z), "210"); olcu_x(yz, Zs(PANO_Z), Zs(0), "250")
olcu_y(Zs(0) + 150, Y2(DOLAP_TABAN), Y2(H_MAK), "580")
et(Zs(-645), Y2(1470), Zs(0) + 205, Y2(1530), "Secop CU KLF4.0CND · 350 × 272 × 450 · 15,2 kg")
et(Zs(ARA_Z), Y2(1900), Zs(0) + 205, Y2(1965), "ısı perdesi (sac)")
et(Zs(-190), Y2(1845), Zs(0) + 205, Y2(1880), "DIN montaj plakası (pano)")
et(Zs(-10), Y2(1700), Zs(0) + 205, Y2(1790), "önden kapak · menteşe")
et(Zs(-600), Y2(H_MAK), Zs(0) + 205, Y2(2110), "üst panjur · sıcak hava", KIR)
et(Zs(-400), Y2(DOLAP_TABAN + 5), Zs(0) + 205, Y2(1420), "dolap tabanı 1450 (açıcı 1440'ta biter)")

# ================================================================ A · ÜST GÖRÜNÜŞ (1600 kotunda kesit)
S3 = 0.62
Px = lambda x: 1600 + x * S3
Pz = lambda z: 1745 + z * S3
d.text((1600, 1100), "A · ÜST GÖRÜNÜŞ (1600 kotunda · ön altta)", font=fG, fill=INK)
d.rectangle([Px(DI0), Pz(-827), Px(DI1), Pz(-3)], fill=TEK_Z)
kutu(Px(0), Pz(-830), Px(700), Pz(0), renk=INK, w=2)
kutu(Px(SEC["x"][0]), Pz(SEC["z"][0]), Px(SEC["x"][1]), Pz(SEC["z"][1]), fill=(92, 96, 104), renk=INK, w=2)
d.ellipse([Px(20), Pz(-700), Px(60), Pz(-590)], outline=(220, 220, 225), width=2)
ortala("Secop", Px(238), Pz(-660), fS, (255, 255, 255))
d.line([(Px(DI0), Pz(ARA_Z)), (Px(DI1), Pz(ARA_Z))], fill=INK, width=3)
kutu(Px(13), Pz(PANO_Z - 3), Px(687), Pz(PANO_Z), fill=PAS, renk=INK, w=1)
for (a, b) in ((25, 300), (315, 505), (520, 680)):
    kutu(Px(a), Pz(PANO_Z), Px(b), Pz(-120), fill=TEK_P, renk=TEK_C, w=1)
d.line([(Px(33), Pz(0)), (Px(667), Pz(0))], fill=INK, width=4)
d.ellipse([Px(33) - 5, Pz(0) - 5, Px(33) + 5, Pz(0) + 5], fill=INK)
panjur(Px(0) - 12, Pz(SEC["z"][0]), Px(0), Pz(SEC["z"][1]))
for zz in (-760, -645, -530):
    d.line([(Px(SEC["x"][0]), Pz(zz)), (Px(-70), Pz(zz))], fill=KIR, width=2); ok(Px(-70), Pz(zz), -1, 0, KIR)
kesik_kutu(Px(SEC["x"][1] + 10), Pz(-820), Px(SEC["x"][1] + 10 + KOMP), Pz(-820 + KOMP), KIR, 3)
ortala("kompresör 380 × 380", Px(SEC["x"][1] + 10 + KOMP / 2), Pz(-640) - 22, fK, KIR)
ortala("SIĞMIYOR", Px(SEC["x"][1] + 10 + KOMP / 2), Pz(-640) + 6, fK, KIR)
kesik((Px(DI1), Pz(-480)), (Px(DI1) + 70, Pz(-480)), BAKIR, 3, 10, 6); ok(Px(DI1) + 70, Pz(-480), 1, 0, BAKIR)
kesik((Px(400), Pz(-200)), (Px(400), Pz(-735)), INK, 3, 10, 6); kesik((Px(400), Pz(-735)), (Px(DI1) + 70, Pz(-735)), INK, 3, 10, 6)
ok(Px(DI1) + 70, Pz(-735), 1, 0, INK)
# ölçüler
yp = Pz(-830) - 30
for x_ in (SEC["x"][0], SEC["x"][1], DI1): uzat(Px(x_), Pz(-830), Px(x_), yp - 8)
olcu_x(yp, Px(SEC["x"][0]), Px(SEC["x"][1]), "450 Secop"); olcu_x(yp, Px(SEC["x"][1]), Px(DI1), "234 boş")
olcu_x(Pz(0) + 30, Px(DI0), Px(DI1), "iç 694", alt=True)
et(Px(DI1) + 70, Pz(-480), Px(DI1) + 250, Pz(-560), "soğutucu borusu → soğuk kutu (evaporatör)", BAKIR)
et(Px(DI1) + 70, Pz(-735), Px(DI1) + 250, Pz(-680), "kablo kanalı (Secop üstünden, 1950) → C arka şeridi")
d.text((Px(-75) - 20, Pz(-470) + 8), "sol yan", font=fS, fill=KIR); d.text((Px(-75) - 20, Pz(-470) + 28), "panjur", font=fS, fill=KIR)
et(Px(350), Pz(-190), Px(DI1) + 250, Pz(-160), "pano: PLC · UPS · güç · sürücüler")
et(Px(500), Pz(-30), Px(DI1) + 250, Pz(-50), "önden kapak 634")

os.makedirs(os.path.dirname(CIKTI), exist_ok=True)
im.save(CIKTI, optimize=True)
bos = DI1 - SEC["x"][1]
print("PNG", CIKTI, im.size, "· Secop yanında boş %.0f mm (kompresör %0.f) → %s" % (bos, KOMP, "SIĞAR" if bos >= KOMP else "SIĞMAZ"))
