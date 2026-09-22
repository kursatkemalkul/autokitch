# -*- coding: utf-8 -*-
"""AUTOKITCH - TOPPING DOZAJ KATI · USTTEN GORUNUS · TEPSI HAREKETI v2 (13 Eyl 2026). Olculer mm.
v2: ustten gorunusler v1 ile ayni + ONDEN GORUNUS (kat 3 kesiti) eklendi (Kemal: 'onde de ciz').

Soru (Kemal): kabin 700'de kaliyor; iki kaset yan yana; robot pideyi kasetlerin altinda gezdirip dondurerek
her yerine malzeme koyacak. Tepsinin uc konumlari kesik cizgiyle.

VERI (kaynak):
  kabin 700 x 830 · yan duvar sac 1,5 + PU 40 + sac 1 = 42,5 -> ic genislik 42,5..657,5 = 615   (sw_topping4.py PU=40)
  kaset 140 x 680, merkez x 270 / 430, 830'da z -695,5..-15,5                                   (teknik_store_topping_v4.py)
  kaset agzi 45 x 50 (x +-22,5, z -80..-30 -> 830'da +4,5 kayma: -75,5..-25,5, merkez z -50,5)   (sw_topping4.py kap_detay)
  on yuz z +40 · robot agzi tam genislik x 30..670                                              (sw_topping4.py ROBOT_AGZI)
  pide O300 · tepsi O320                                                                        (DUZEN.md / TEPSI_D320)
GEOMETRI: agzin altina pidenin p noktasini getirmek icin tepsi merkezi c = agiz - p.
  1) YALNIZ KAYDIRMA: p pide icinde her yon -> c agizin cevresinde R150 daire -> tepsi zarfi R310.
  2) DONDUR + ONE CEK: tepsi doner, merkez yalniz one kayar (r = 0..150) -> x sabit, duvara pay 67,5.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont, ImageChops

OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\3_TOPPING_v4\TOPPING_dozaj_hareketi_v2.png".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX = 2200, 2440
BG, INK, GRAY, LINE = (255, 255, 255), (26, 26, 28), (132, 132, 140), (72, 72, 78)
SOFT, ACC, RED, PUC = (228, 228, 234), (0, 86, 184), (198, 42, 32), (255, 240, 200)
KAS, TEPSI, PIDE, ZARF = (214, 218, 226), (0, 86, 184), (196, 140, 60), (14, 120, 90)


def F(sz, b=False):
    for n in (("arialbd.ttf", "segoeuib.ttf") if b else ("arial.ttf", "segoeui.ttf")):
        try:
            return ImageFont.truetype(n, sz)
        except Exception:
            pass
    return ImageFont.load_default()


f7, f8, f9, f11, f13, f16, f38 = F(15), F(17), F(19), F(22), F(25), F(30, True), F(52, True)
im = Image.new("RGBA", (W_PX, H_PX), BG + (255,))
d = ImageDraw.Draw(im)

# ---------------- veri ----------------
XI0, XI1 = 42.5, 657.5
KASET = {"A": 270.0, "B": 430.0}
KW, KZ0, KZ1 = 140.0, -695.5, -15.5
AG_W, AG_Z0, AG_Z1 = 45.0, -75.5, -25.5
AGZ = (AG_Z0 + AG_Z1) / 2.0            # -50,5
ZF1 = 40.0
R_T, R_P = 160.0, 150.0
OY = 430.0                              # ekranda z = -790


def txt(x, y, s, f=f11, c=INK, a="la"):
    d.text((x, y), s, font=f, fill=c, anchor=a)


class Pano:
    def __init__(self, ox):
        self.ox = ox

    def X(self, x):
        return self.ox + x

    def Y(self, z):
        return OY + (z + 790.0)


def kesik_daire(cx, cy, r, c, w=3, dash=16, gap=10):
    L = 2 * math.pi * r
    n = max(8, int(L // (dash + gap)))
    for i in range(n):
        a0 = 2 * math.pi * i / n
        a1 = a0 + 2 * math.pi * dash / (dash + gap) / n
        pts = [(cx + r * math.cos(a0 + (a1 - a0) * k / 6), cy + r * math.sin(a0 + (a1 - a0) * k / 6)) for k in range(7)]
        d.line(pts, fill=c, width=w)


def noktali(pts, c, w=3, adim=12):
    for i in range(len(pts) - 1):
        (ax, ay), (bx, by) = pts[i], pts[i + 1]
        L = math.hypot(bx - ax, by - ay)
        n = max(1, int(L // adim))
        for k in range(n):
            t = k / n
            x, y = ax + (bx - ax) * t, ay + (by - ay) * t
            d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=c)


def olcu_h(x0, x1, y, s, f=f9, c=INK):
    d.line([(x0, y), (x1, y)], fill=c, width=2)
    for xx in (x0, x1):
        d.line([(xx, y - 9), (xx, y + 9)], fill=c, width=2)
    tw = d.textlength(s, font=f)
    d.rectangle([(x0 + x1) / 2 - tw / 2 - 6, y - 14, (x0 + x1) / 2 + tw / 2 + 6, y + 14], fill=BG)
    txt((x0 + x1) / 2, y, s, f, c, "mm")


def olcu_v(x, y0, y1, s, f=f9, c=INK, yon="r"):
    d.line([(x, y0), (x, y1)], fill=c, width=2)
    for yy in (y0, y1):
        d.line([(x - 9, yy), (x + 9, yy)], fill=c, width=2)
    txt(x + (14 if yon == "r" else -14), (y0 + y1) / 2, s, f, c, "lm" if yon == "r" else "rm")


def ok(x0, y0, x1, y1, c, w=3):
    d.line([(x0, y0), (x1, y1)], fill=c, width=w)
    a = math.atan2(y1 - y0, x1 - x0)
    for s in (+1, -1):
        d.line([(x1, y1), (x1 - 16 * math.cos(a + s * 0.45), y1 - 16 * math.sin(a + s * 0.45))], fill=c, width=w)


def kabin(p):
    X, Y = p.X, p.Y
    d.rectangle([X(0), Y(-790), X(700), Y(ZF1)], fill=(250, 250, 251), outline=LINE, width=3)
    for (a, b) in ((0, XI0), (XI1, 700)):
        d.rectangle([X(a), Y(-790), X(b), Y(ZF1)], fill=PUC, outline=GRAY, width=1)
    d.rectangle([X(XI0), Y(-790), X(XI1), Y(-767.5)], fill=PUC, outline=GRAY, width=1)
    d.line([(X(0), Y(ZF1)), (X(700), Y(ZF1))], fill=INK, width=5)
    txt(X(350), Y(ZF1) + 20, "ÖN YÜZ · robot ağzı", f8, INK, "ma")
    txt(X(350), Y(-790) - 16, "ARKA", f8, GRAY, "md")


def kasetler(p, katman):
    X, Y = p.X, p.Y
    kd = ImageDraw.Draw(katman)
    for ad, xc in KASET.items():
        kd.rectangle([X(xc - KW / 2), Y(KZ0), X(xc + KW / 2), Y(KZ1)], fill=KAS + (150,), outline=LINE + (255,), width=2)
    for ad, xc in KASET.items():
        txt(X(xc), Y(-380), "KASET " + ad, f9, INK, "mm")
        txt(X(xc), Y(-350), "140 × 680", f7, GRAY, "mm")
        txt(X(xc), Y(-320), "üstte", f7, GRAY, "mm")


def agizlar(p):
    X, Y = p.X, p.Y
    for ad, xc in KASET.items():
        d.rectangle([X(xc - AG_W / 2), Y(AG_Z0), X(xc + AG_W / 2), Y(AG_Z1)], fill=RED, outline=RED)
    d.line([(X(KASET["A"]), Y(-262)), (X(KASET["A"]), Y(AG_Z0) - 3)], fill=RED, width=2)
    txt(X(KASET["A"]), Y(-278), "AĞIZ 45 × 50", f7, RED, "mm")


def carpisma(p, cx, cz):
    """tepsi dairesinin yan duvarlarin icindeki kismi (kabin icinde, z < on yuz) kirmizi"""
    X, Y = p.X, p.Y
    m1 = Image.new("L", (W_PX, H_PX), 0)
    ImageDraw.Draw(m1).ellipse([X(cx - R_T), Y(cz - R_T), X(cx + R_T), Y(cz + R_T)], fill=255)
    m2 = Image.new("L", (W_PX, H_PX), 0)
    md = ImageDraw.Draw(m2)
    md.rectangle([X(-400), Y(-790), X(XI0), Y(ZF1)], fill=255)
    md.rectangle([X(XI1), Y(-790), X(1100), Y(ZF1)], fill=255)
    m = ImageChops.multiply(m1, m2)
    kirmizi = Image.new("RGBA", (W_PX, H_PX), RED + (150,))
    im.alpha_composite(Image.composite(kirmizi, Image.new("RGBA", (W_PX, H_PX), (0, 0, 0, 0)), m))


def tepsi(p, cx, cz, renk=TEPSI, w=3, pide=True):
    X, Y = p.X, p.Y
    kesik_daire(X(cx), Y(cz), R_T, renk, w)
    if pide:
        d.ellipse([X(cx - R_P), Y(cz - R_P), X(cx + R_P), Y(cz + R_P)], outline=PIDE, width=1)
    d.ellipse([X(cx) - 5, Y(cz) - 5, X(cx) + 5, Y(cz) + 5], fill=renk)


# ======================= BASLIK =======================
txt(100, 50, "AUTOKITCH  ·  TOPPING DOZAJ KATI  ·  TEPSİ HAREKETİ  v2", f38, INK)
txt(100, 120, "üstten ve önden  ·  700 mm kabin  ·  2 kaset yan yana  ·  tepsi Ø320  ·  pide Ø300  ·  ölçüler mm  ·  13 Eylül 2026", f13, GRAY)
d.line([(100, 165), (W_PX - 100, 165)], fill=LINE, width=3)

# ======================= 1 · YALNIZ KAYDIRMA =======================
P1 = Pano(230.0)
txt(P1.X(0), 205, "1 · YALNIZ KAYDIRMA", f16, RED)
txt(P1.X(0), 248, "tepsi dönmez · pidenin her kenarı ağzın altına gelmeli", f8, GRAY)
kabin(P1)
kat = Image.new("RGBA", (W_PX, H_PX), (0, 0, 0, 0))
kasetler(P1, kat)
im.alpha_composite(kat)
d = ImageDraw.Draw(im)
xa = KASET["A"]
UC_A = [(xa + R_P, AGZ), (xa - R_P, AGZ), (xa, AGZ - R_P), (xa, AGZ + R_P)]        # c = agiz - p (4 uc)
for cx, cz in UC_A:
    carpisma(P1, cx, cz)
d = ImageDraw.Draw(im)
carpisma(P1, KASET["B"] + R_P, AGZ)
d = ImageDraw.Draw(im)
for cx, cz in UC_A:
    tepsi(P1, cx, cz)
tepsi(P1, KASET["B"] + R_P, AGZ, renk=GRAY, w=2, pide=False)
# zarf: agiz cevresinde R150 + R160 = R310
for xc, renk in ((xa, ZARF),):
    pts = [(P1.X(xc + 310 * math.cos(t)), P1.Y(AGZ + 310 * math.sin(t))) for t in [2 * math.pi * k / 180 for k in range(181)]]
    noktali(pts, renk, 3, 14)
agizlar(P1)
X, Y = P1.X, P1.Y
olcu_h(X(xa - R_P - R_T), X(XI0), Y(AGZ) - 200, "82,5 çarpar", f9, RED)
d.line([(X(XI0), Y(-790)), (X(XI0), Y(ZF1))], fill=RED, width=2)
txt(X(xa - R_P), Y(AGZ) + 172, "duvara çarpan uç", f8, RED, "ma")
olcu_h(X(XI1), X(KASET["B"] + R_P + R_T), Y(AGZ) - 200, "82,5 çarpar", f9, RED)
txt(X(350), Y(AGZ + 310) + 40, "zarf R310 · ağız çevresinde", f8, ZARF, "ma")

# ======================= 2 · DONDUR + ONE CEK =======================
P2 = Pano(1270.0)
txt(P2.X(0), 205, "2 · DÖNDÜR + ÖNE ÇEK", f16, ZARF)
txt(P2.X(0), 248, "tepsi kendi merkezinde döner · merkez yalnız öne-arkaya kayar", f8, GRAY)
kabin(P2)
kat = Image.new("RGBA", (W_PX, H_PX), (0, 0, 0, 0))
kasetler(P2, kat)
im.alpha_composite(kat)
d = ImageDraw.Draw(im)
X, Y = P2.X, P2.Y
for ad, xc in KASET.items():
    renk = TEPSI if ad == "A" else GRAY
    # zarf: kapsul (merkez z AGZ .. AGZ+150, yaricap 160)
    z0, z1 = AGZ, AGZ + R_P
    pts = [(X(xc - R_T), Y(z0))] + [(X(xc + R_T * math.cos(t)), Y(z0 - R_T * math.sin(t))) for t in [math.pi - math.pi * k / 60 for k in range(61)]]
    pts += [(X(xc + R_T), Y(z1))] + [(X(xc + R_T * math.cos(t)), Y(z1 + R_T * math.sin(t))) for t in [math.pi * k / 60 for k in range(61)]]
    pts += [(X(xc - R_T), Y(z0))]
    noktali(pts, ZARF if ad == "A" else (150, 190, 170), 3, 14)
    tepsi(P2, xc, z0, renk, 3 if ad == "A" else 2, pide=(ad == "A"))
    if ad == "A":
        tepsi(P2, xc, z1, renk, 3)
# spiral: agzin pide uzerindeki izi (A, r=0 konumunda pideye cizilir)
xs, zs = KASET["A"], AGZ
sp = []
for k in range(0, 4 * 360 + 1, 6):
    t = math.radians(k); r = 130.0 * k / (4 * 360)
    sp.append((X(xs + r * math.cos(t)), Y(zs + r * math.sin(t))))
noktali(sp, PIDE, 2, 7)
# donus oku
cxp, cyp = X(xs), Y(zs)
arc = [(cxp + 190 * math.cos(math.radians(a)), cyp + 190 * math.sin(math.radians(a))) for a in range(200, 321, 5)]
d.line(arc, fill=TEPSI, width=4)
ok(arc[-2][0], arc[-2][1], arc[-1][0], arc[-1][1], TEPSI, 4)
txt(cxp - 205, cyp - 130, "döner", f8, TEPSI, "rm")
# one cekme oku ve olcusu
ok(X(xs) + 10, Y(z0) + 10, X(xs) + 10, Y(z1) - 10, TEPSI, 3)
olcu_v(X(xs - R_T) - 40, Y(z0), Y(z1), "150", f9, INK, "l")
agizlar(P2)
olcu_h(X(XI0), X(KASET["A"] - R_T), Y(AGZ) - 200, "67,5", f9, ZARF)
olcu_h(X(KASET["B"] + R_T), X(XI1), Y(AGZ) - 200, "67,5", f9, ZARF)
txt(X(xs), Y(z1 + R_T) + 18, "ön uç", f8, TEPSI, "ma")
txt(X(560), Y(AGZ + 310) + 40, "zarf · merkez 150 öne", f8, ZARF, "ma")

# ======================= ORTAK OLCULER =======================
for p in (P1, P2):
    X, Y = p.X, p.Y
    olcu_h(X(0), X(700), Y(-790) - 60, "700", f11, INK)
    olcu_h(X(XI0), X(XI1), Y(-790) - 110, "iç 615", f9, GRAY)
    olcu_h(X(KASET["A"] - KW / 2), X(KASET["A"] + KW / 2), Y(-720), "140", f7, GRAY)
    olcu_h(X(KASET["A"] + KW / 2), X(KASET["B"] - KW / 2), Y(-650), "20", f7, GRAY)
    olcu_h(X(KASET["A"]), X(KASET["B"]), Y(-590), "ağız arası 160", f8, RED)
olcu_v(P1.X(-40) - 70, P1.Y(-790), P1.Y(ZF1), "830", f11, INK, "l")


# ======================= ONDEN GORUNUS (kat 3 kesiti) =======================
Y_AG0, Y_AG1 = 774.0, 891.0            # kat 3 robot agzi · sw_topping4 ROBOT_AGZI
Y_BANT1 = 1170.0                        # kat 3 kaset bandi ustu · sw_topping4 KLAPE
Y_RAF = 885.0                           # kat 3 raf kotu · sw_topping4 LAYOUT
Y_K0, Y_K1 = Y_RAF + 24.0, Y_RAF + 264.0   # kaset govdesi 909..1149 · KAP_DETAY y 24..264
Y_TP = 809.0                            # tepsi duzlemi · sw_topping4 TEPSI_Y kat 3
T_KAL, P_KAL = 20.0, 15.0               # tepsi ve pide kalinligi · SEMATIK (olcu verilmez)
AGZ_BANT = (253, 244, 243)
CARP = (230, 150, 145)
FOY = 1700.0                            # ekranda y = 1200


def FY(y):
    return FOY + (1200.0 - y)


def kirik(x0, x1, y):
    n = max(2, int((x1 - x0) // 24))
    d.line([(x0 + i * (x1 - x0) / n, y + (6 if i % 2 else -6)) for i in range(n + 1)], fill=GRAY, width=2)


def kesik_dikdortgen(x0, y0, x1, y1, renk, w=3, adim=22):
    for (a, b) in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
        L = math.hypot(b[0] - a[0], b[1] - a[1]); n = max(1, int(L // adim))
        for k in range(n):
            t0, t1 = k / n, min(1.0, (k + 0.6) / n)
            d.line([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0), (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)], fill=renk, width=w)


def on_kabin(p, baslik, renk):
    X = p.X
    txt(X(0), FY(1200) - 78, baslik, f16, renk)
    txt(X(0), FY(1200) - 40, "kat 3 kesiti · kaset kapağı çizilmedi", f8, GRAY)
    d.rectangle([X(0), FY(1200), X(XI0), FY(740)], fill=PUC, outline=GRAY, width=1)
    d.rectangle([X(XI1), FY(1200), X(700), FY(740)], fill=PUC, outline=GRAY, width=1)
    kirik(X(0), X(700), FY(1200)); kirik(X(0), X(700), FY(740))
    d.rectangle([X(XI0), FY(Y_AG1), X(XI1), FY(Y_AG0)], fill=AGZ_BANT, outline=RED, width=2)
    txt(X(XI0) + 10, FY(Y_AG1) + 8, "ROBOT AĞZI", f7, RED, "la")
    for yy in (Y_AG1, Y_BANT1):
        d.line([(X(XI0), FY(yy)), (X(XI1), FY(yy))], fill=LINE, width=3)
    for ad, xc in KASET.items():
        d.rectangle([X(xc - KW / 2), FY(Y_K1), X(xc + KW / 2), FY(Y_K0)], fill=KAS, outline=LINE, width=2)
        txt(X(xc), FY((Y_K0 + Y_K1) / 2) - 12, "KASET " + ad, f8, INK, "mm")
        txt(X(xc), FY((Y_K0 + Y_K1) / 2) + 14, "140 × 240", f7, GRAY, "mm")
        d.rectangle([X(xc - AG_W / 2), FY(Y_K0), X(xc + AG_W / 2), FY(Y_AG1)], fill=RED)
    olcu_h(X(XI0), X(XI1), FY(740) + 44, "iç 615", f9, GRAY)
    olcu_v(X(700) + 40, FY(Y_AG1), FY(Y_AG0), "117", f8, INK, "r")
    olcu_v(X(700) + 130, FY(Y_K0), FY(Y_TP), "100", f8, INK, "r")
    txt(X(700) + 130, FY(Y_TP) + 14, "kaset altı · tepsi", f7, GRAY, "ma")


def on_tepsi(p, xc, renk, kesik):
    X = p.X
    x0, x1, y0, y1 = X(xc - R_T), X(xc + R_T), FY(Y_TP + T_KAL), FY(Y_TP)
    if kesik:
        kesik_dikdortgen(x0, y0, x1, y1, renk)
    else:
        d.rectangle([x0, y0, x1, y1], fill=(220, 232, 250), outline=renk, width=3)
        d.rectangle([X(xc - R_P), FY(Y_TP + T_KAL + P_KAL), X(xc + R_P), FY(Y_TP + T_KAL)], fill=(240, 214, 170), outline=PIDE, width=2)
        noktali([(X(xc), FY(Y_AG1)), (X(xc), FY(Y_TP + T_KAL + P_KAL))], PIDE, 3, 8)


def on_carpisma(p, xc):
    X = p.X
    y0, y1 = FY(Y_TP + T_KAL), FY(Y_TP)
    if xc - R_T < XI0:
        d.rectangle([X(xc - R_T), y0, X(XI0), y1], fill=CARP)
    if xc + R_T > XI1:
        d.rectangle([X(XI1), y0, X(xc + R_T), y1], fill=CARP)


# ---- 1 · onden yalniz kaydirma
on_kabin(P1, "ÖNDEN · YALNIZ KAYDIRMA", RED)
X = P1.X
for xc in (xa - R_P, xa + R_P, KASET["B"] + R_P):
    on_carpisma(P1, xc)
on_tepsi(P1, xa - R_P, TEPSI, True)
on_tepsi(P1, xa + R_P, TEPSI, True)
on_tepsi(P1, KASET["B"] + R_P, GRAY, True)
on_tepsi(P1, xa, TEPSI, False)
olcu_h(X(xa - R_P - R_T), X(XI0), FY(Y_TP) + 48, "82,5 çarpar", f9, RED)
olcu_h(X(XI1), X(KASET["B"] + R_P + R_T), FY(Y_TP) + 48, "82,5 çarpar", f9, RED)
txt(X(xa - R_P), FY(Y_TP + T_KAL) - 16, "sol uç", f7, TEPSI, "md")
txt(X(xa + R_P), FY(Y_TP + T_KAL) - 16, "sağ uç", f7, TEPSI, "md")

# ---- 2 · onden dondur + one cek
on_kabin(P2, "ÖNDEN · DÖNDÜR + ÖNE ÇEK", ZARF)
X = P2.X
on_tepsi(P2, KASET["B"], GRAY, True)
on_tepsi(P2, xa, TEPSI, False)
cx0, cy0 = X(xa), FY(Y_TP) + 16
arc = [(cx0 + 130 * math.cos(math.radians(a)), cy0 + 9 * math.sin(math.radians(a))) for a in range(20, 161, 5)]
d.line(arc, fill=TEPSI, width=4)
ok(arc[-2][0], arc[-2][1], arc[-1][0], arc[-1][1], TEPSI, 4)
txt(X(560), FY(868), "döner · öne-arkaya 150", f7, TEPSI, "mm")
olcu_h(X(XI0), X(xa - R_T), FY(Y_TP) + 14, "67,5", f8, ZARF)
olcu_h(X(KASET["B"] + R_T), X(XI1), FY(Y_TP) + 14, "67,5", f8, ZARF)

# ======================= LEJANT =======================
ly = H_PX - 80
d.line([(100, ly - 50), (W_PX - 100, ly - 50)], fill=LINE, width=2)
xx = 100
LEJ = [("kaset · üstte", "kaset"), ("kaset ağzı", "agiz"), ("tepsi uç konumu Ø320", "tepsi"), ("pide Ø300", "pide"),
       ("hareket zarfı", "zarf"), ("malzeme izi · spiral", "spiral"), ("duvara çarpan kısım", "carp")]
for ad, tip in LEJ:
    if tip == "kaset":
        d.rectangle([xx, ly - 12, xx + 36, ly + 12], fill=KAS, outline=LINE, width=2)
    elif tip == "agiz":
        d.rectangle([xx, ly - 12, xx + 36, ly + 12], fill=RED)
    elif tip == "tepsi":
        kesik_daire(xx + 18, ly, 13, TEPSI, 3, 7, 5)
    elif tip == "pide":
        d.ellipse([xx + 4, ly - 13, xx + 30, ly + 13], outline=PIDE, width=2)
    elif tip == "zarf":
        noktali([(xx, ly), (xx + 36, ly)], ZARF, 3, 9)
    elif tip == "spiral":
        noktali([(xx, ly), (xx + 36, ly)], PIDE, 2, 6)
    elif tip == "carp":
        d.rectangle([xx, ly - 12, xx + 36, ly + 12], fill=(230, 150, 145))
    txt(xx + 48, ly, ad, f9, INK, "lm")
    xx += 48 + d.textlength(ad, font=f9) + 60

assert not os.path.exists(OUT), "v2 zaten var — yeni numara ver"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.convert("RGB").save(OUT)
print("yazildi:", OUT)
