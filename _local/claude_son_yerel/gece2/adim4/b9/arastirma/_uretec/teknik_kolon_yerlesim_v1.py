# -*- coding: utf-8 -*-
"""TOPPING · TEKNİK KOLON v1 (öneri) — ÖN GÖRÜNÜŞ (kolon + A + C) · KOLON YAN KESİT · 25 Eyl 2026
Kemal: "hamur açmanın üstü boş değil, orası hamur açma şeyinin motoru falan var" → TEKNIK_DOLAP_v1 (A'nın üstü) geçersiz.
Modelde (topping_cad_v22 · montaj v43) açıcının en üstü kolon 1440, motorları 1235–1308 ve öndeki motor gövdeden 167 mm
dışarıda; Kemal açıcı tahrikini yukarıda istiyor → A'nın üstü açıcıya bırakıldı.
Öneri: hattın sol ucuna TOPPING'e ait tam boy TEKNİK KOLON 400 × 830 × 2030 (hat 5430 → 5830).
Ağır parçalar altta: JUN-AIR OF302-15B 380 × 380 × 510 · 25 kg (topping_uno_cad_v4, broşür) + üstünde Secop CU KLF4.0CND
350 × 272 × 450 · 15,2 kg (store_cad_v4, secop.com; B'deki ile aynı). Göz hizasında önden kapaklı pano.
Kolon ↔ C bağlantısı açıcı kolonunun ARKASINDAN (A'da z −660…−830 boş: topping_cad_v22 ölçümü).
3B modele dokunulmadı.
"""
import math, os
from PIL import Image, ImageDraw, ImageFont
U = os.path.dirname(os.path.abspath(__file__)); KOK = os.path.dirname(os.path.dirname(U))
CIKTI = os.path.join(KOK, "arastirma", "FULL_MAKINE", "TEKNIK_KOLON_v1_teknik.png")

INK, GRI, ACIK = (25, 25, 28), (120, 124, 130), (205, 208, 212)
PU, PUC = (246, 232, 180), (214, 188, 118)
PAS, BEL, SOG = (206, 211, 218), (228, 231, 236), (240, 247, 253)
KIR, MAVI, BAKIR = (200, 30, 30), (30, 90, 170), (190, 110, 50)
TEK_Z, TEK_P, TEK_C = (255, 244, 230), (250, 216, 172), (196, 110, 30)
KOYU = (92, 96, 104)
W, H = 3000, 1860
im = Image.new("RGB", (W, H), (255, 255, 255)); d = ImageDraw.Draw(im)
fn = lambda n, b=False: ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf" if b else "C:/Windows/Fonts/arial.ttf", n)
fB, fG, fE, fO, fK, fS = fn(40, True), fn(27, True), fn(20), fn(19), fn(21, True), fn(16)

# ---------------------------------------------------------------- ölçüler (mm, hat koordinatı; kolon x −400…0)
KL0, KL1 = -400.0, 0.0
H_B, H_MAK, Y_ALT = 1060.0, 2030.0, 123.0
KI0, KI1 = KL0 + 3.0, KL1 - 3.0                       # iç 394
KOMP = dict(x=(KI0 + 4.0, KI0 + 384.0), y=(Y_ALT + 7.0, Y_ALT + 517.0), z=(-820.0, -440.0))      # 380 × 510 × 380
RAF1 = (KOMP["y"][1] + 10.0, KOMP["y"][1] + 20.0)     # Secop rafı
SEC = dict(x=(KI0 + 22.0, KI0 + 372.0), y=(RAF1[1], RAF1[1] + 272.0), z=(-820.0, -370.0))         # 350 × 272 × 450
PANO = dict(y=(1150.0, 1950.0), z=-250.0)
KX0, KX1, KB_ALT, KB_UST, KD_UST, KK_UST, ACIK_UST = 728.0, 2472.0, 1276.0, 1320.0, 1852.0, 1914.0, 2499.0
KAPAK_BOL = [(728.0, 1490.0), (1490.0, 1910.0), (1910.0, 2472.0)]


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


d.text((60, 28), "TOPPING · TEKNİK KOLON v1 (öneri) — ağır parçalar altta, pano göz hizasında, hattın sol ucunda", font=fB, fill=INK)
d.text((60, 82), "ölçüler mm · kotlar yerden · turuncu = TOPPING teknik kolonu · mavi = soğuk kutu · A'nın üstü açıcının tahrikine bırakıldı · "
       "hat 5430 → 5830 (+400)", font=fE, fill=GRI)

# ================================================================ ÖN GÖRÜNÜŞ · KOLON + A + C
S = 0.45; OY = 1745
X = lambda x: 300 + S * x
Y = lambda y: OY - S * y
d.text((60, 150), "ÖN GÖRÜNÜŞ · hattın sol ucu (kolon kapağı kaldırılmış)", font=fG, fill=INK)
d.line([(X(-470), Y(0)), (X(2560), Y(0))], fill=INK, width=3)
# B, A, C
kutu(X(0), Y(Y_ALT), X(2500), Y(H_B), renk=GRI, w=1); kutu(X(30), Y(0), X(2470), Y(Y_ALT), renk=GRI, w=1)
ortala("B · ÇEKMECELER (değişmiyor)", X(1250), Y(600), fO, GRI)
kutu(X(0), Y(H_B), X(700), Y(H_MAK), renk=INK, w=2)
kutu(X(290), Y(H_B), X(410), Y(1440), fill=BEL, renk=INK, w=1)
kutu(X(270), Y(1310), X(430), Y(1322), fill=PAS, renk=INK, w=1)
kutu(X(305), Y(1176), X(395), Y(1264), fill=BEL, renk=INK, w=1)
kutu(X(180), Y(1154), X(520), Y(1176), fill=(250, 226, 196), renk=INK, w=1)
kesik_kutu(X(40), Y(2000), X(660), Y(1460), GRI, 2)
ortala("AÇICI TAHRİKİ", X(350), Y(1790), fK, GRI); ortala("(motor vb. · Kemal)", X(350), Y(1790) + 26, fS, GRI)
ortala("AÇICI", X(350), Y(1440) - 22, fS)
kutu(X(700), Y(H_B), X(2500), Y(H_MAK), renk=INK, w=2)
tara(X(KX0), Y(KK_UST), X(KX1), Y(KB_ALT))
d.rectangle([X(KX0 + 62), Y(KD_UST), X(KX1 - 62), Y(KB_UST)], fill=SOG)
for (a, b) in KAPAK_BOL: kutu(X(a + 2), Y(KK_UST), X(b - 2), Y(KD_UST), renk=INK, w=1)
kutu(X(KX0), Y(KK_UST), X(KX1), Y(KB_ALT), renk=MAVI, w=3)
ortala("SOĞUK KUTU (düz kutu)", X(1600), Y(1640), fK, MAVI)
kesik_kutu(X(KX0), Y(ACIK_UST), X(KX1), Y(KK_UST), GRI, 1)
ortala("kapak açılma alanı · boş", X(1600), Y(2230), fO, GRI)
# teknik kolon (kapak kaldırılmış)
d.rectangle([X(KI0), Y(H_MAK - 3), X(KI1), Y(Y_ALT + 3)], fill=TEK_Z)
kutu(X(KL0), Y(Y_ALT), X(KL1), Y(H_MAK), renk=TEK_C, w=3)
kutu(X(KL0 + 30), Y(0), X(KL1 - 30), Y(Y_ALT), renk=GRI, w=1)
kutu(X(KOMP["x"][0]), Y(KOMP["y"][1]), X(KOMP["x"][1]), Y(KOMP["y"][0]), fill=KOYU, renk=INK, w=2)
d.ellipse([X(-330), Y(520), X(-170), Y(360)], outline=(210, 210, 215), width=2)
ortala("kompresör", X(-200), Y(250), fS, (255, 255, 255))
kutu(X(KI0), Y(RAF1[1]), X(KI1), Y(RAF1[0]), fill=PAS, renk=INK, w=1)
kutu(X(SEC["x"][0]), Y(SEC["y"][1]), X(SEC["x"][1]), Y(SEC["y"][0]), fill=KOYU, renk=INK, w=2)
ortala("Secop", X(-200), Y(760), fS, (255, 255, 255))
kutu(X(KI0 + 8), Y(PANO["y"][1]), X(KI1 - 8), Y(PANO["y"][0]), fill=(250, 250, 250), renk=TEK_C, w=2)
SIRA = [("PLC + G/Ç", 1860.0), ("UPS + akü · 24 V", 1710.0), ("sürücüler (9)", 1560.0), ("yedek ray", 1410.0), ("klemens + röle", 1260.0)]
for t, yr in SIRA:
    kutu(X(KI0 + 20), Y(yr + 60), X(KI1 - 20), Y(yr - 50), fill=(TEK_P if t != "yedek ray" else (255, 255, 255)), renk=TEK_C, w=1)
    ortala(t, X(-200), Y(yr + 5) - 10, fS)
# boru + kablo: kolondan A'nın arkasından C'ye
kesik((X(KL1), Y(1150)), (X(KX0 + 20), Y(1150)), BAKIR, 3, 10, 6); ok(X(KX0 + 20), Y(1150), 1, 0, BAKIR)
kesik((X(KL1), Y(1110)), (X(KX0 + 20), Y(1110)), INK, 2, 10, 6); ok(X(KX0 + 20), Y(1110), 1, 0, INK)
# ölçüler + kotlar
yo = Y(0) + 34
for x_ in (KL0, 0.0, 700.0, 2500.0): uzat(X(x_), Y(0) + 6, X(x_), yo + 8)
olcu_x(yo, X(KL0), X(0), "400", KIR, alt=True); olcu_x(yo, X(0), X(700), "A 700", alt=True); olcu_x(yo, X(700), X(2500), "C 1800", alt=True)
for y_ in (0.0, Y_ALT, H_B, 1440.0, KB_ALT, KK_UST, H_MAK, ACIK_UST):
    d.line([(X(KL0) - 34, Y(y_)), (X(KL0) - 20, Y(y_))], fill=GRI, width=1)
    t = "%.0f" % y_; d.text((X(KL0) - 38 - d.textlength(t, font=fS), Y(y_) - 9), t, font=fS, fill=INK)
yb = Y(2620)
d.line([(X(KL0), yb + 14), (X(KL0), yb), (X(2500), yb), (X(2500), yb + 14)], fill=TEK_C, width=3)
ortala("TOPPING İSTASYONU = teknik kolon + açıcı + topping (hepsi kendi gövdesinde)", X(1050), yb - 28, fK, TEK_C)

# ================================================================ KOLON · YAN KESİT (arka solda · ön sağda)
S2 = 0.6; OY2 = 1745
Zs = lambda z: 1700 + (z + 830.0) * S2
Y2 = lambda y: OY2 - S2 * y
d.text((1640, 150), "TEKNİK KOLON · YAN KESİT (arka solda · ön sağda)", font=fG, fill=INK)
d.line([(Zs(-900), Y2(0)), (Zs(90), Y2(0))], fill=INK, width=3)
d.rectangle([Zs(-827), Y2(H_MAK - 3), Zs(-3), Y2(Y_ALT + 3)], fill=TEK_Z)
kutu(Zs(-830), Y2(Y_ALT), Zs(0), Y2(H_MAK), renk=TEK_C, w=3)
kutu(Zs(-800), Y2(0), Zs(-60), Y2(Y_ALT), renk=GRI, w=1)
kutu(Zs(KOMP["z"][0]), Y2(KOMP["y"][1]), Zs(KOMP["z"][1]), Y2(KOMP["y"][0]), fill=KOYU, renk=INK, w=2)
d.ellipse([Zs(-720), Y2(560), Zs(-540), Y2(380)], outline=(210, 210, 215), width=2)
kutu(Zs(-827), Y2(RAF1[1]), Zs(-3), Y2(RAF1[0]), fill=PAS, renk=INK, w=1)
kutu(Zs(SEC["z"][0]), Y2(SEC["y"][1]), Zs(SEC["z"][1]), Y2(SEC["y"][0]), fill=KOYU, renk=INK, w=2)
kutu(Zs(-420), Y2(760), Zs(-372), Y2(700), fill=(60, 60, 64), renk=INK, w=1)
kutu(Zs(PANO["z"] - 3), Y2(PANO["y"][1]), Zs(PANO["z"]), Y2(PANO["y"][0]), fill=PAS, renk=INK, w=1)
for t, yr in SIRA:
    kutu(Zs(PANO["z"]), Y2(yr + 60), Zs(-120), Y2(yr - 50), fill=(TEK_P if t != "yedek ray" else (255, 255, 255)), renk=TEK_C, w=1)
kutu(Zs(-20), Y2(1990), Zs(0), Y2(Y_ALT + 20), fill=(236, 236, 240), renk=INK, w=2)
panjur(Zs(-12), Y2(SEC["y"][1]), Zs(0), Y2(SEC["y"][0]))
panjur(Zs(-12), Y2(KOMP["y"][1] - 40), Zs(0), Y2(KOMP["y"][0] + 40))
kutu(Zs(-360), Y2(460), Zs(-120), Y2(200), fill=BEL, renk=INK, w=1)
ortala("şartlandırıcı", Zs(-240), Y2(330) - 10, fS)
panjur(Zs(-820), Y2(H_MAK) - 8, Zs(-300), Y2(H_MAK) + 4, dikey=False)
d.line([(Zs(-285), Y2(RAF1[1] + 290)), (Zs(-285), Y2(H_MAK - 3))], fill=INK, width=3)
for zz in (-760, -560, -380):
    d.line([(Zs(zz), Y2(RAF1[1] + 300)), (Zs(zz), Y2(2130))], fill=KIR, width=2); ok(Zs(zz), Y2(2130), 0, -1, KIR)
for yy in (800.0, 350.0):
    d.line([(Zs(60), Y2(yy)), (Zs(-10), Y2(yy))], fill=MAVI, width=2); ok(Zs(-10), Y2(yy), -1, 0, MAVI)
# ölçüler
xr = Zs(0) + 60
olcu_y(xr, Y2(Y_ALT), Y2(RAF1[0]), "527"); olcu_y(xr, Y2(RAF1[1]), Y2(SEC["y"][1]), "272"); olcu_y(xr, Y2(PANO["y"][0]), Y2(PANO["y"][1]), "800")
yz = Y2(H_MAK) - 70
for z_ in (-830.0, -440.0, -370.0, 0.0): uzat(Zs(z_), Y2(H_MAK), Zs(z_), yz - 8)
olcu_x(yz, Zs(-830), Zs(-440), "kompresör 380"); olcu_x(yz - 40, Zs(-830), Zs(-370), "Secop 450"); olcu_x(yz, Zs(-370), Zs(0), "370")
EX = Zs(0) + 130
et(Zs(-630), Y2(250), EX, Y2(220), "kompresör JUN-AIR OF302-15B · 380 × 380 × 510 · 25 kg (hava kalırsa)")
et(Zs(-600), Y2(700), EX, Y2(720), "soğutma grubu Secop CU KLF4.0CND · 15,2 kg (B'dekiyle aynı)")
et(Zs(-240), Y2(420), EX, Y2(420), "şartlandırıcı + ana hat çıkışı (hava kalırsa)")
et(Zs(-10), Y2(800), EX, Y2(880), "ön ızgara · hava girişi", MAVI)
et(Zs(-185), Y2(1560), EX, Y2(1560), "pano · göz hizasında · önden kapak")
et(Zs(-285), Y2(1300), EX, Y2(1300), "ısı perdesi (sıcak hava arkadan yukarı)")
et(Zs(-560), Y2(H_MAK), EX, Y2(2100), "üst panjur · sıcak hava çıkışı", KIR)
et(Zs(-400), Y2(RAF1[1] - 5), EX, Y2(1000), "ağır parçalar altta: 25 + 15,2 kg")

os.makedirs(os.path.dirname(CIKTI), exist_ok=True)
im.save(CIKTI, optimize=True)
ic = KI1 - KI0
print("PNG", CIKTI, im.size, "· kolon iç %.0f · kompresör 380 %s · Secop 350 %s · yükseklik %.0f ≤ 1060 %s" % (
    ic, "SIĞAR" if ic >= 380 + 8 else "SIĞMAZ", "SIĞAR" if ic >= 350 + 8 else "SIĞMAZ", SEC["y"][1], "✓" if SEC["y"][1] <= 1060 else "✗"))
