# -*- coding: utf-8 -*-
"""ALTERNATİF A1 · ROBOTSUZ — TEKNİK RESİM v1 (26 Eyl 2026) · ön görünüş + üst görünüş (mevcut v45 ile alan karşılaştırması) + 2 yan kesit.
Sade pafta: görünüş + ölçü + parça adı. Ölçüler alt_robotsuz_cad_v1'den okunur."""
import math, os, sys
from PIL import Image, ImageDraw, ImageFont
U = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, U)
import alt_robotsuz_cad_v1 as A

K = 2.0
W_PX, H_PX = 5200, 3000
im = Image.new("RGB", (int(W_PX * K), int(H_PX * K)), (255, 255, 255)); dr = ImageDraw.Draw(im)
INK, GRAY, LINE, ACC, RED, BLUE, SOFT, FILL = (25, 28, 33), (120, 126, 134), (70, 76, 84), (36, 86, 200), (200, 50, 40), (28, 86, 166), (232, 234, 238), (246, 247, 249)
YENI, YENI_D = (255, 238, 214), (196, 124, 24)
FONT = r"C:\Windows\Fonts\arial.ttf"; FONTB = r"C:\Windows\Fonts\arialbd.ttf"
def F(s, b=False): return ImageFont.truetype(FONTB if b else FONT, int(s * K))
f7, f8, f9, f11, f13, f16, f24 = F(15), F(17), F(19), F(22), F(26), F(32, True), F(44, True)
S = 0.34
def P(x, y): return (x * K, y * K)
def rect(x0, y0, x1, y1, fill=None, out=LINE, w=2): dr.rectangle([P(min(x0, x1), min(y0, y1)), P(max(x0, x1), max(y0, y1))], fill=fill, outline=out, width=int(w * K))
def line(pts, c=INK, w=2): dr.line([P(*p) for p in pts], fill=c, width=int(w * K))
def txt(x, y, s, f=f8, c=INK, a="mm"): dr.text(P(x, y), s, font=f, fill=c, anchor=a)
def dash(x0, y0, x1, y1, c=GRAY, w=1):
    for (a, b) in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
        L = math.hypot(b[0] - a[0], b[1] - a[1]); n = max(1, int(L / 9))
        for i in range(0, n, 2):
            u0, u1 = i / n, min(1, (i + 1) / n)
            line([(a[0] + (b[0] - a[0]) * u0, a[1] + (b[1] - a[1]) * u0), (a[0] + (b[0] - a[0]) * u1, a[1] + (b[1] - a[1]) * u1)], c, w)
def olcu_h(x0, x1, y, s, c=INK):
    line([(x0, y), (x1, y)], c, 1.5); line([(x0, y - 7), (x0, y + 7)], c, 1.5); line([(x1, y - 7), (x1, y + 7)], c, 1.5); txt((x0 + x1) / 2, y - 12, s, f8, c)
def olcu_v(x, y0, y1, s, c=INK):
    line([(x, y0), (x, y1)], c, 1.5); line([(x - 7, y0), (x + 7, y0)], c, 1.5); line([(x - 7, y1), (x + 7, y1)], c, 1.5); txt(x + 10, (y0 + y1) / 2, s, f8, c, "lm")

txt(80, 60, "AUTOKITCH  ·  ALTERNATİF A1  ·  ROBOTSUZ MAKİNE  ·  TEKNİK RESİM v1  ·  KAVRAM (öneri, onay bekliyor)", f24, INK, "lm")
txt(80, 110, "robot + yer rayı + koridor + karşıdaki QR dolabı YOK  ·  çekmeceler yerine TOP OTOMATI (30 bantlı şerit + asansör + itici)  ·  kutu modülünün önünde ÇIKIŞ ÇATALI + DÖNER TESLİM DOLABI (paternoster 8 raf + içecek otomatı)  ·  A · C · F · K · E aynen (montaj v45)  ·  ölçüler mm  ·  26 Eylül 2026", f9, GRAY, "lm")
line([(80, 140), (W_PX - 80, 140)], LINE, 2)

# ---------------- ÖN GÖRÜNÜŞ ----------------
S = 0.6
OX, FY = 200.0, 1500.0
fx = lambda x: OX + x * S; fy = lambda y: FY - y * S
txt(OX, 190, "ÖN GÖRÜNÜŞ", f16, ACC, "lm")
MOD = [("A · AÇICI", 0, 700, 1060, 2030), ("C · TOPPING", 700, 2500, 1060, 2030), ("F · FIRIN", 2500, 4000, 123, 2030), ("K · KESME", 4000, 4600, 123, 2030), ("E · KUTU", 4600, 5430, 123, 2030)]
for ad, x0, x1, y0, y1 in MOD:
    rect(fx(x0), fy(y1), fx(x1), fy(y0), FILL, LINE, 2.5); txt(fx((x0 + x1) / 2), fy(y1) - 16, ad, f9, INK)
rect(fx(0), fy(1060), fx(2500), fy(123), YENI, YENI_D, 3)
txt(fx(1250), fy(1060) - 16 + 1060 * S * 0 - 0, "", f9)
for k, (tip, y, _p) in enumerate(A.KATLAR):
    line([(fx(A.X_SERIT[0]), fy(y)), (fx(A.X_SERIT[1]), fy(y))], YENI_D, 2)
    d, adim = A.TOP[tip]
    for m in range(0, int((A.X_SERIT[1] - A.X_SERIT[0] - 30) // adim), 3):
        cx = fx(A.X_SERIT[0] + 20 + adim / 2 + m * adim); dr.ellipse([P(cx - d * S / 2, fy(y) - d * S), P(cx + d * S / 2, fy(y))], outline=YENI_D, width=int(1 * K))
    txt(fx(A.X_SERIT[1]) + 12, fy(y) - 10, "%s · %d top/şerit × 5" % ("pide" if tip == "pide" else "lahmacun", int((A.X_SERIT[1] - A.X_SERIT[0] - 30) // adim)), f7, YENI_D, "lm")
rect(fx(62), fy(1300), fx(190), fy(190), None, RED, 2)
txt(fx(126), fy(1330), "ASANSÖR", f8, RED); txt(fx(126), fy(1300) - 34 + 60, "", f7)
txt(fx(1100), fy(80) + 10, "TOP OTOMATI (B yerine) · 2500 × 830 × 1060 · 6 kat × 5 şerit = 30 bant · 160 pide + 440 lahmacun = 2 gün · soğuk", f8, YENI_D)
rect(fx(4600), fy(2030), fx(5430), fy(123), None, YENI_D, 1.5)
txt(fx(5015), fy(2030) - 42, "DÖNER TESLİM DOLABI (E'nin önünde, z 0…+820)", f8, YENI_D)
olcu_h(fx(0), fx(5430), fy(2030) - 80, "5430 (aynı)")
olcu_v(fx(-60), fy(1060), fy(123), "1060")

# ---------------- ÜST GÖRÜNÜŞ: mevcut v45 · A1 ----------------
def plan(OXp, PY, baslik, a1):
    px = lambda x: OXp + x * 0.3; pz = lambda z: PY + (z + 830) * 0.3
    txt(OXp, PY - 70, baslik, f16, ACC, "lm")
    for ad, x0, x1, *_ in MOD:
        rect(px(x0), pz(-830), px(x1), pz(0), FILL, LINE, 2); txt(px((x0 + x1) / 2), pz(-415), ad.split(" · ")[0], f9, INK)
    if a1:
        rect(px(0), pz(-830), px(2500), pz(0), YENI, YENI_D, 2); txt(px(1250), pz(-415), "A · C (B yerine TOP OTOMATI altta)", f8, YENI_D)
        rect(px(4600), pz(0), px(5430), pz(820), YENI, YENI_D, 2); txt(px(5015), pz(410), "DÖNER DOLAP", f8, YENI_D)
        txt(px(5015), pz(820) + 20, "müşteri kapağı ↓", f8, RED)
        txt(px(2300), pz(420), "robot koridoru YOK · makine önü servis alanı (dükkânın ortak alanı)", f9, GRAY)
        alan = (5430 * 830 + 830 * 820) / 1e6
        txt(px(0), pz(1340) + 60, "makinenin kapladığı alan: 5430 × 830 + 830 × 820 = %.2f m²" % alan, f11, YENI_D, "lm")
    else:
        rect(px(200), pz(360 - 120), px(5100), pz(360 + 120), SOFT, LINE, 1.5); txt(px(2650), pz(360), "ROBOT RAYI 4900 · FR5", f8, ACC)
        rect(px(4425), pz(900), px(5430), pz(1340), SOFT, LINE, 2); txt(px(4928), pz(1120), "QR DOLABI", f8, INK)
        alan = 5430 * (830 + 1340) / 1e6
        txt(px(0), pz(1340) + 60, "robot + koridor + QR ile kapladığı alan: 5430 × 2170 = %.2f m²" % alan, f11, INK, "lm")
    olcu_h(px(0), px(5430), pz(-830) - 16, "5430")
plan(200.0, 1720.0, "ÜST GÖRÜNÜŞ · BUGÜN (montaj v45)", False)
plan(2150.0, 1720.0, "ÜST GÖRÜNÜŞ · A1 ROBOTSUZ", True)

# ---------------- YAN KESİT 1: TOP OTOMATI (x 125 · asansör) ----------------
def kesit(OXk, PY, baslik):
    zx = lambda z: OXk + (z + 830) * 0.42; yy = lambda y: PY - y * 0.42
    txt(OXk, PY - 2030 * 0.42 - 50, baslik, f13, ACC, "lm")
    return zx, yy
zx, yy = kesit(3700.0, 1500.0, "KESİT 1 · TOP OTOMATI + AÇICI")
rect(zx(-830), yy(1060), zx(0), yy(123), YENI, YENI_D, 2.5)
rect(zx(-830), yy(2030), zx(0), yy(1060), FILL, LINE, 2)
for k, (tip, y, _p) in enumerate(A.KATLAR):
    d = A.TOP[tip][0]
    for z in A.Z_SERIT:
        line([(zx(z - 58), yy(y)), (zx(z + 58), yy(y))], YENI_D, 2)
        dr.ellipse([P(zx(z) - d * 0.21, yy(y) - d * 0.42), P(zx(z) + d * 0.21, yy(y))], outline=YENI_D, width=int(K))
line([(zx(-770), yy(190)), (zx(-770), yy(1300))], RED, 3); txt(zx(-770), yy(1330), "dikey eksen", f7, RED)
line([(zx(-752), yy(700)), (zx(-90), yy(700))], RED, 2); txt(zx(-420), yy(700) + 16, "z ekseni + kap", f7, RED)
rect(zx(-230), yy(1060), zx(-110), yy(1000), (255, 255, 255), RED, 2); txt(zx(-170), yy(1000) + 18, "tavan kapağı", f7, RED)
dr.ellipse([P(zx(-170) - 49 * 0.42, yy(1172) - 98 * 0.42), P(zx(-170) + 49 * 0.42, yy(1172))], outline=RED, width=int(2 * K))
line([(zx(-340), yy(1168)), (zx(0), yy(1168))], INK, 3); txt(zx(-170), yy(1168) + 16, "tabla 1168 (açıcının altı)", f7, INK)
txt(zx(-415), yy(1650), "A · AÇICI (aynen)", f8, INK); txt(zx(-415), yy(1650) + 24, "kafa park 90 (60 yetmez)", f7, RED)
olcu_v(zx(0) + 30, yy(1060), yy(123), "1060")

# ---------------- YAN KESİT 2: E + DÖNER DOLAP ----------------
zx2, yy2 = kesit(4200.0, 1500.0, "KESİT 2 · E + ÇATAL + DÖNER DOLAP")
rect(zx2(-830), yy2(2030), zx2(0), yy2(123), FILL, LINE, 2); txt(zx2(-415), yy2(1700), "E · KUTU (aynen)", f9, INK)
rect(zx2(0), yy2(2030), zx2(820), yy2(123), YENI, YENI_D, 2.5)
y0, y1 = A.PAT_Y; za, zo = A.PAT_Z; r = (zo - za) / 2
line([(zx2(za), yy2(y0)), (zx2(za), yy2(y1))], YENI_D, 2); line([(zx2(zo), yy2(y0)), (zx2(zo), yy2(y1))], YENI_D, 2)
for yc in (y0, y1):
    dr.ellipse([P(zx2(za), yy2(yc + r)), P(zx2(zo), yy2(yc - r))], outline=YENI_D, width=int(2 * K))
L = A.pat_boy()
for k in range(A.N_RAF):
    yk, zk = A.pat_yol(k * L / A.N_RAF)
    line([(zx2(zk - 175), yy2(yk)), (zx2(zk + 175), yy2(yk))], YENI_D, 4)
txt(zx2(820) + 12, yy2(800), "PATERNOSTER", f8, YENI_D, "lm"); txt(zx2(820) + 12, yy2(800) + 22, "8 raf · zincir %.0f" % L, f7, YENI_D, "lm")
rect(zx2(30), yy2(2010), zx2(640), yy2(1680), None, BLUE, 2); txt(zx2(335), yy2(1845) - 10, "İÇECEK OTOMATI", f7, BLUE); txt(zx2(335), yy2(1845) + 12, "3 × 6 spiral · 180", f7, BLUE)
line([(zx2(-366), yy2(1098)), (zx2(A.ZC_DISARI), yy2(1098))], RED, 4); txt(zx2(-250), yy2(1098) + 18, "ÇIKIŞ ÇATALI · z %d · +55" % (A.ZC_DISARI - A.ZC_ICERI), f7, RED)
rect(zx2(800), yy2(1380), zx2(820), yy2(980), (255, 255, 255), RED, 2); txt(zx2(820) + 12, yy2(1180), "müşteri kapağı · QR", f7, RED, "lm")
olcu_h(zx2(0), zx2(820), yy2(123) + 30, "820")

# ---------------- PARÇA LİSTESİ ----------------
PX, PYL = 200.0, 2560.0
txt(PX, PYL - 40, "YENİ PARÇALAR (A1)", f16, ACC, "lm")
satir = [("TOP OTOMATI", "30 bantlı şerit (6 kat × 5) · şerit redüktörlü motoru 24 V × 30 [V] · sağ uçta tahrik · cleat'li PU bant", "B gövdesinde · soğuk"),
         ("ASANSÖR", "igus ZLW-1040 dikey (strok 1000) + ZLW-0630 z (strok 560) + POM kap · tavanda yaylı klape", "sol uç 62–190"),
         ("TABLA İTİCİSİ", "mini lineer eksen strok 230 · POM kol · topu kaptan tablaya sürer", "A'nın sol boşluğu"),
         ("ÇIKIŞ ÇATALI", "3 dişli çatal (robot çatalının aynısı) · igus ZLW-1040 z strok 456 · SMC MGPM16-60 kaldırma · NEMA 23", "E'nin önü"),
         ("DÖNER DOLAP", "paternoster 8 raf · 2 zincir + 4 dişli · redüktörlü motor + fren · müşteri kapağı + QR okuyucu", "830 × 820 × 2030"),
         ("İÇECEK OTOMATI", "soğuk · 3 tepsi × 6 spiral × 10 = 180 kutu · oluk rafın bardaklığına", "dolabın üstü"),
         ("KALKAN", "Fairino FR5 · yer rayı 4900 · QR dolabı (koridorun karşısı) · 25 motorlu çekmece", "—")]
for i, (a, b, c) in enumerate(satir):
    y = PYL + i * 50
    txt(PX, y, a, f8, INK if i < 6 else RED, "lm"); txt(PX + 300, y, b, f8, GRAY, "lm"); txt(PX + 2100, y, c, f8, INK, "lm")
yol = os.path.join(os.path.dirname(U), "FULL_MAKINE", "ALT_A1_ROBOTSUZ_v1_teknik.png")
im.save(yol, dpi=(300, 300)); print("yazildi", yol, im.size)
