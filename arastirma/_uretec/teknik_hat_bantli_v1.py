# -*- coding: utf-8 -*-
"""AUTOKITCH - BANTLI HAT TEKNIK RESIM v1 (13 Eyl 2026): ON + UST (PLAN KESITI) + YAN (TOPPING KESITI). Olculer mm.

KAVRAM (Kemal'in krokisi, 13 Eyl): Picnic tarzi konveyor bant. Robot STORE'dan hamuru alir, PRESS'e koyar;
pres tabani banda verir (gecis Kemal'de). Bant 6 dozaj kasetinin altindan gecer, dogrudan konveyor firina girer,
cikista kesme plakasi: sprey + 8 bicak kesici, itici pideyi kutuya iter; robot kutuyu QR dolabina tasir.
STORE bant hattinin ALTINDA (2 kat). Hat: PRESS 700 · TOPPING-BANT 1000 · OVEN 1600 · KESME 600 · PACK 700 = 4600.
KAYNAKLAR
  Middleby Marshall PS536 spec (Form 4503E): hazne 36"/914 · bant 20"/508 genis, 60"/1524 uzun · derinlik 39-3/4"/1010 (camsiz)
     · yukseklik 43-1/2"/1105 (17,5" ayakla -> govde 26"/660) · pisme 2:40-29:50 · 16 kW · 299 kg · uc kata kadar istiflenir
     · bosluk: arka 76, kumanda ucu 457, diger uc 76.
  Fersah PZP-400 640 x 950 x 800 (teknik_hat_base_v7). Kaset 140 x 240 x 680 (KAP_DETAY). Cekmece 620 x 680, HH 88 / 132, alin 33.
VARSAYIM (etiketli): bant ust kotu 1300 · firin bandi govde tabanindan 300 yukarida · pres tablasi govde tabanindan 300 yukarida
  · dozaj basligi 300 genis (kaset agzi 45 x 50 banttaki urunu boyayamaz, genis baslik gerekir) · kesme plakasi 560 x 400.
STORE bant altinda: K1 6 · K2 7 · K3 5 · K4 5 · K5 5 = 28 cekmece (43 gerekli: 6 lahmacun + 9 icecek ACIK).
Kural: paftada yalniz gorunus + olcu + parca adi; aciklama mesajda.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE\HAT_BANTLI_v1_teknik.png".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX = 4300, 2860
S = 0.62
BG, INK, GRAY, LINE = (255, 255, 255), (26, 26, 28), (132, 132, 140), (72, 72, 78)
FILL, ACC, RED, SOFT = (244, 244, 246), (0, 86, 184), (198, 42, 32), (228, 228, 234)
DOLAP, BOSL, PUC = (14, 120, 90), (190, 190, 196), (255, 240, 200)
BANT, FIRIN, KAS, HEAD = (0, 120, 160), (200, 90, 30), (236, 240, 246), (222, 228, 240)
AGZ = (253, 244, 243)


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


def ok(x0, y0, x1, y1, c, w=3):
    d.line([(x0, y0), (x1, y1)], fill=c, width=w)
    a = math.atan2(y1 - y0, x1 - x0)
    for s_ in (-0.5, 0.5):
        d.line([(x1, y1), (x1 - 14 * math.cos(a + s_), y1 - 14 * math.sin(a + s_))], fill=c, width=w)


# ======================= VERI =======================
DZ = 830.0
H = 1970.0
ISTASYON = [("PRESS v7", 700.0), ("TOPPING-BANT v1", 1000.0), ("OVEN v6 · konveyör", 1600.0), ("KESME v1", 600.0), ("PACK v5", 700.0)]
X0 = {}
_x = 0.0
def anahtar(ad):
    return ad.split()[0].split("-")[0]


for ad, w in ISTASYON:
    X0[anahtar(ad)] = _x
    _x += w
HAT = _x                                                # 4600
Y_BANT = 1300.0                                         # bant ust kotu (varsayim)
BANT_Z0, BANT_Z1 = -600.0, -200.0                       # topping bandi 400 genis
# firin: PS536
FIRIN_L, FIRIN_H, FIRIN_D, HAZNE, FBANT_W = 1524.0, 660.0, 1010.0, 914.0, 508.0
FX0 = X0["OVEN"] + 38.0
FY0 = Y_BANT - 300.0                                    # govde tabani (bant tabandan 300: varsayim)
FZ0 = 40.0 - FIRIN_D                                    # -970: 180 arkaya tasar
# kasetler (TOPPING): 6 dozaj + 6 depo, bant boyunca 160 adim
KW, KH, KL = 140.0, 240.0, 680.0
KX = [X0["TOPPING"] + 40.0 + i * 160.0 for i in range(6)]
Y_HEAD0, Y_HEAD1 = Y_BANT + 20.0, Y_BANT + 150.0        # dozaj basligi 1320..1450
Y_DOZ0, Y_DOZ1 = Y_HEAD1, Y_HEAD1 + KH                  # dozaj kaseti 1450..1690
Y_DEP0, Y_DEP1 = 1720.0, 1960.0                         # depo kaseti
KZ0, KZ1 = -695.5, -15.5
URUN = ("KAŞAR", "SUCUK", "HARÇ", "HARÇ", "KIYMA", "KUŞBAŞI")
# STORE bant altinda: 5 kolon x 620, bolme 35
XI, WO, BOL = 62.5, 620.0, 35.0
CELL0, BIND, FUGA = 182.5, 15.0, 3.0
HH = {"hamur": 88.0, "lahm": 88.0, "paket": 88.0, "icecek": 132.0}
AD = {"hamur": "TAZE PİDE", "lahm": "LAHMACUN", "paket": "KAŞAR + SUCUK PAKETİ", "icecek": "İÇECEK"}
CAP = {"hamur": (20, "top"), "lahm": (30, "top"), "paket": (None, "vakum"), "icecek": (56, "kutu")}
KOLON = [(940.0, [(6, "hamur")]),                        # K1 PRESS alti
         (1140.0, [(6, "hamur"), (1, "paket")]),          # K2 TOPPING alti
         (900.0, [(1, "paket"), (4, "lahm")]),            # K3 TOPPING/OVEN alti
         (900.0, [(5, "lahm")]),                          # K4 OVEN alti
         (900.0, [(5, "lahm")])]                          # K5 OVEN alti
for top, gruplar in KOLON:
    y = CELL0 - BIND
    for n, tip in gruplar:
        y += n * (HH[tip] + 2 * BIND + FUGA)
    assert y - FUGA <= top, "kolon tasiyor %.1f > %.1f" % (y - FUGA, top)
CEK = sum(n for _, g in KOLON for n, _ in g)
WS = 2 * XI + 5 * WO + 4 * BOL                          # 3365 -> PRESS+TOPPING+OVEN 3300 icine sigmaz: K5 kismen KESME altina
# kesme plakasi
PLK_X0, PLK_X1 = X0["KESME"] + 20.0, X0["KESME"] + 580.0
KUTU = 320.0

# ======================= YERLESIM =======================
OX = 300.0
FY_TOP = 360.0
FY = FY_TOP + H * S
PY_TOP = FY + 300.0
SX = OX + HAT * S + 260.0


def fx(x):
    return OX + x * S


def fy(y):
    return FY - y * S


def py(z):
    return PY_TOP + (z + 970.0) * S


def sz(z):
    return SX + (z + 790.0) * S


# ======================= BASLIK =======================
txt(OX, 70, "AUTOKITCH  ·  BANTLI HAT  ·  TEKNİK RESİM  v1", f38, INK)
txt(OX, 138, "ön · üst · yan görünüş  ·  konveyör bant + konveyör fırın  ·  STORE bant altında  ·  ölçüler mm  ·  13 Eylül 2026", f13, GRAY)
d.line([(OX, 178), (W_PX - 170, 178)], fill=LINE, width=3)

# ======================= ON GORUNUS =======================
txt(OX, FY_TOP - 150, "ÖN GÖRÜNÜŞ", f16, ACC)
for ad, w in ISTASYON:
    x0 = X0[anahtar(ad)]
    d.rectangle([fx(x0), fy(H), fx(x0 + w), fy(0)], fill=FILL, outline=LINE, width=3)
    d.rectangle([fx(x0), fy(120), fx(x0 + w), fy(0)], fill=SOFT, outline=LINE, width=2)
    txt(fx(x0 + w / 2), fy(H) - 64, ad, f13, INK, "md")
    olcu_h(fx(x0), fx(x0 + w), fy(H) - 26, sayi(w), f11, INK)

# --- STORE (alt kat) ---
cx = XI
for ki, (top, gruplar) in enumerate(KOLON):
    if ki:
        d.rectangle([fx(cx - BOL), fy(top), fx(cx), fy(CELL0 - BIND)], fill=SOFT, outline=LINE, width=1)
    d.rectangle([fx(cx), fy(top + 60.0), fx(cx + WO), fy(top)], fill=PUC, outline=GRAY, width=1)   # tavan PU 60
    y = CELL0 - BIND
    for n, tip in gruplar:
        h = HH[tip] + 2 * BIND
        ybas = y
        for _ in range(n):
            d.rectangle([fx(cx + 8), fy(y + h), fx(cx + WO - 8), fy(y)], fill=BG, outline=DOLAP, width=1)
            y += h + FUGA
        cap, br = CAP[tip]
        ikinci = ("%d %s · +3 °C" % (n * cap, br)) if cap else ("%s · +3 °C" % br)
        ym = (fy(ybas) + fy(y - FUGA)) / 2
        etiket(fx(cx + WO / 2), ym - 13, "%s × %d" % (AD[tip], n), f8, INK, DOLAP)
        etiket(fx(cx + WO / 2), ym + 13, ikinci, f7, DOLAP, DOLAP)
    ust = y - FUGA
    if top - ust > 20:
        d.rectangle([fx(cx + 8), fy(top), fx(cx + WO - 8), fy(ust)], fill=(250, 250, 251), outline=BOSL, width=1)
        tarali(fx(cx + 8) + 1, fy(top) + 1, fx(cx + WO - 8) - 1, fy(ust) - 1)
    txt(fx(cx + WO / 2), fy(CELL0 - BIND) + 20, "K%d · %s" % (ki + 1, sayi(top)), f7, GRAY, "mm")
    cx += WO + BOL
# teknik bolme (sogutma gruplari) K5 sagi .. PACK
d.rectangle([fx(cx - BOL), fy(1140.0), fx(X0["PACK"] - 30), fy(120.0)], fill=SOFT, outline=LINE, width=2)
txt(fx((cx - BOL + X0["PACK"] - 30) / 2), fy(630.0) - 12, "TEKNİK", f8, GRAY, "mm")
txt(fx((cx - BOL + X0["PACK"] - 30) / 2), fy(630.0) + 12, "soğutma grupları · pano", f7, GRAY, "mm")
olcu_h(fx(cx - BOL), fx(X0["PACK"] - 30), fy(120.0) + 44, sayi(X0["PACK"] - 30 - (cx - BOL)), f8, GRAY)
olcu_h(fx(XI), fx(XI + WO), fy(0) + 44, "620", f8, GRAY)
olcu_h(fx(0), fx(cx - BOL), fy(0) + 80, "STORE  %s  ·  %d çekmece" % (sayi(cx - BOL), CEK), f11, INK)

# --- ust kat: bant hatti ---
# bant cercevesi (TOPPING -> KESME)
d.rectangle([fx(X0["TOPPING"] + 10), fy(Y_BANT), fx(X0["KESME"] + 590), fy(Y_BANT - 100.0)], fill=BG, outline=BANT, width=2)
d.line([(fx(X0["TOPPING"] + 10), fy(Y_BANT)), (fx(X0["KESME"] + 590), fy(Y_BANT))], fill=BANT, width=5)
txt(fx(X0["TOPPING"] + 750), fy(Y_BANT - 50.0), "TOPPING BANDI 400 · adımlı", f8, BANT, "mm")
txt(fx(X0["KESME"] + 300), fy(Y_BANT - 50.0), "KESME PLAKASI", f8, BANT, "mm")
# PRESS
px0 = X0["PRESS"] + 30.0
d.rectangle([fx(px0), fy(FY0 + 950.0), fx(px0 + 640.0), fy(FY0)], fill=BG, outline=INK, width=2)
txt(fx(px0 + 320), fy(FY0 + 620.0) - 12, "FERSAH PZP-400", f9, INK, "mm")
txt(fx(px0 + 320), fy(FY0 + 620.0) + 12, "640 × 950 × 800", f7, GRAY, "mm")
d.rectangle([fx(px0 + 20), fy(Y_BANT + 260.0), fx(px0 + 620), fy(Y_BANT)], fill=AGZ, outline=RED, width=3)
txt(fx(px0 + 320), fy(Y_BANT + 130.0) - 10, "PRES AĞZI", f8, RED, "mm")
txt(fx(px0 + 320), fy(Y_BANT + 130.0) + 12, "tabla %s · banda geçiş" % sayi(Y_BANT), f7, RED, "mm")
ok(fx(px0 + 620), fy(Y_BANT + 40.0), fx(X0["TOPPING"] + 40), fy(Y_BANT + 40.0), BANT, 3)
# TOPPING: basliklar, dozaj kasetleri, depo kasetleri
for i, kx in enumerate(KX):
    d.rectangle([fx(kx), fy(Y_HEAD1), fx(kx + KW), fy(Y_HEAD0)], fill=HEAD, outline=BANT, width=2)
    d.rectangle([fx(kx), fy(Y_DOZ1), fx(kx + KW), fy(Y_DOZ0)], fill=KAS, outline=INK, width=2)
    txt(fx(kx + KW / 2), fy((Y_DOZ0 + Y_DOZ1) / 2) - 12, URUN[i], f7, INK, "mm")
    txt(fx(kx + KW / 2), fy((Y_DOZ0 + Y_DOZ1) / 2) + 12, "dozaj", f7, GRAY, "mm")
    d.rectangle([fx(kx), fy(Y_DEP1), fx(kx + KW), fy(Y_DEP0)], fill=KAS, outline=INK, width=2)
    txt(fx(kx + KW / 2), fy((Y_DEP0 + Y_DEP1) / 2) - 12, URUN[i], f7, INK, "mm")
    txt(fx(kx + KW / 2), fy((Y_DEP0 + Y_DEP1) / 2) + 12, "depo", f7, GRAY, "mm")
d.line([(fx(X0["TOPPING"] + 20), fy(Y_DEP0 - 10)), (fx(X0["TOPPING"] + 980), fy(Y_DEP0 - 10))], fill=LINE, width=3)   # depo rafi
txt(fx(X0["TOPPING"] + 250), fy(Y_BANT - 50.0), "DOZAJ BAŞLIĞI × 6 · 300 geniş", f8, BANT, "mm")
# OVEN
d.rectangle([fx(FX0), fy(FY0 + FIRIN_H), fx(FX0 + FIRIN_L), fy(FY0)], fill=BG, outline=FIRIN, width=3)
hz0 = FX0 + (FIRIN_L - HAZNE) / 2
drect(fx(hz0), fy(FY0 + FIRIN_H - 40), fx(hz0 + HAZNE), fy(FY0 + 40), FIRIN, 2)
d.line([(fx(FX0 - 30), fy(Y_BANT)), (fx(FX0 + FIRIN_L + 30), fy(Y_BANT))], fill=BANT, width=5)
txt(fx(FX0 + FIRIN_L / 2), fy(FY0 + 520.0) - 12, "MIDDLEBY PS536 · İMPİNGEMENT KONVEYÖR FIRIN", f9, FIRIN, "mm")
txt(fx(FX0 + FIRIN_L / 2), fy(FY0 + 520.0) + 12, "1524 × 660 × 1010  ·  16 kW  ·  299 kg", f7, GRAY, "mm")
txt(fx(FX0 + FIRIN_L / 2), fy(FY0 + 120.0), "PİŞİRME HAZNESİ 914  ·  bant 508 geniş  ·  2:40 – 29:50", f7, FIRIN, "mm")
olcu_h(fx(hz0), fx(hz0 + HAZNE), fy(FY0 + FIRIN_H) - 26, "914", f9, FIRIN)
olcu_h(fx(FX0), fx(FX0 + FIRIN_L), fy(FY0 + FIRIN_H) - 60, "1524", f9, INK)
olcu_v(fx(FX0) + 30, fy(FY0 + FIRIN_H), fy(FY0), "660", f8, INK, "r")
d.rectangle([fx(X0["OVEN"] + 33), fy(1968.0), fx(X0["OVEN"] + 1567), fy(FY0 + FIRIN_H + 20)], fill=BG, outline=LINE, width=2)
txt(fx(X0["OVEN"] + 800), fy((1968.0 + FY0 + FIRIN_H + 20) / 2), "EGZOZ DAVLUMBAZI · fan · karbon filtre", f8, INK, "mm")
# KESME
kx0 = X0["KESME"]
d.rectangle([fx(kx0 + 40), fy(Y_BANT + 400.0), fx(kx0 + 560), fy(Y_BANT + 60.0)], fill=BG, outline=INK, width=2)
txt(fx(kx0 + 300), fy(Y_BANT + 250.0) - 12, "KESİCİ · 8 bıçak", f8, INK, "mm")
txt(fx(kx0 + 300), fy(Y_BANT + 250.0) + 12, "sprey memesi · itici", f7, GRAY, "mm")
d.rectangle([fx(kx0 + 33), fy(1968.0), fx(kx0 + 567), fy(Y_BANT + 430.0)], fill=BG, outline=LINE, width=2)
txt(fx(kx0 + 300), fy((1968.0 + Y_BANT + 430.0) / 2), "TAHRİK · YAĞ KABI", f8, INK, "mm")
# PACK
pk0 = X0["PACK"]
d.rectangle([fx(pk0 + 33), fy(1200.0), fx(pk0 + 667), fy(123.0)], fill=BG, outline=INK, width=2)
txt(fx(pk0 + 350), fy(660.0) - 12, "ŞARJÖR · 506 blank", f8, INK, "mm")
txt(fx(pk0 + 350), fy(660.0) + 12, "alttan kaldırmalı", f7, GRAY, "mm")
d.rectangle([fx(pk0 + 30), fy(Y_BANT + 300.0), fx(pk0 + 670), fy(Y_BANT - 50.0)], fill=AGZ, outline=RED, width=3)
txt(fx(pk0 + 350), fy(Y_BANT + 125.0) - 10, "KUTULAMA AĞZI", f8, RED, "mm")
txt(fx(pk0 + 350), fy(Y_BANT + 125.0) + 12, "y %s – %s" % (sayi(Y_BANT - 50), sayi(Y_BANT + 300)), f7, RED, "mm")
d.rectangle([fx(pk0 + 33), fy(1968.0), fx(pk0 + 667), fy(Y_BANT + 330.0)], fill=BG, outline=LINE, width=2)
txt(fx(pk0 + 350), fy((1968.0 + Y_BANT + 330.0) / 2), "KALIP · TAHRİK · PANO", f8, INK, "mm")
# genel olculer
olcu_h(fx(0), fx(HAT), fy(0) + 116, "HAT  %s" % sayi(HAT), f13, INK)
olcu_v(fx(0) - 44, fy(H), fy(0), "1970", f11, INK, "l")
olcu_v(fx(HAT) + 44, fy(Y_BANT), fy(0), "bant %s" % sayi(Y_BANT), f9, BANT, "r")

# ======================= UST GORUNUS (PLAN KESITI, bant kotu) =======================
txt(OX, PY_TOP - 150, "ÜST GÖRÜNÜŞ  ·  PLAN KESİTİ  ·  bant kotu", f16, ACC)
txt(fx(HAT / 2), py(-970.0) - 40, "ARKA", f9, GRAY, "mm")
for ad, w in ISTASYON:
    x0 = X0[anahtar(ad)]
    d.rectangle([fx(x0), py(-790.0), fx(x0 + w), py(40.0)], fill=FILL, outline=LINE, width=3)
    txt(fx(x0 + w / 2), py(40.0) + 30, "%s  ·  %s" % (ad, sayi(w)), f9, INK, "mm")
# bant
d.rectangle([fx(X0["TOPPING"] + 10), py(BANT_Z0), fx(X0["KESME"] - 20), py(BANT_Z1)], fill=(232, 244, 250), outline=BANT, width=2)
for xx in range(int(X0["TOPPING"] + 40), int(X0["OVEN"]), 60):
    d.line([(fx(xx), py(BANT_Z0)), (fx(xx), py(BANT_Z1))], fill=(200, 225, 240), width=1)
ok(fx(X0["TOPPING"] + 60), py(-400.0), fx(X0["TOPPING"] + 220), py(-400.0), BANT, 3)
txt(fx(X0["TOPPING"] + 500), py(-160.0), "TOPPING BANDI 400 geniş · z −600 … −200", f7, BANT, "mm")
# urun (Ø300) bant uzerinde ornek
# PRESS plan
d.rectangle([fx(X0["PRESS"] + 29), py(-788.0), fx(X0["PRESS"] + 669), py(12.0)], fill=BG, outline=INK, width=2)
txt(fx(X0["PRESS"] + 349), py(-403.0), "FERSAH PZP-400", f8, INK, "mm")
txt(fx(X0["PRESS"] + 349), py(-373.0), "640 × 800", f7, GRAY, "mm")
# TOPPING plan: kasetler bant uzerine dik, basliklar 300 genis
for i, kx in enumerate(KX):
    d.rectangle([fx(kx), py(KZ0), fx(kx + KW), py(KZ1)], outline=INK, width=2)
    d.rectangle([fx(kx - 6), py(-797.5), fx(kx + KW + 6), py(KZ0)], fill=(255, 230, 230), outline=RED, width=1)
    drect(fx(kx - 10), py(-550.0), fx(kx + KW + 10), py(-250.0), BANT, 2)
    txt(fx(kx + KW / 2), py(-700.0) + 10, URUN[i], f7, INK, "mt")
    txt(fx(kx + KW / 2), py(-100.0), "45×50", f7, GRAY, "mm")
txt(fx(X0["TOPPING"] + 500), py(-905.0), "kaset motor paketi 102 · z −797,5 (830'a sığmıyor)", f7, RED, "mm")
olcu_h(fx(KX[0]), fx(KX[1]), py(-838.0), "160", f8, INK)
olcu_h(fx(KX[5]), fx(KX[5] + KW), py(-838.0), "140", f7, GRAY)
olcu_v(fx(X0["TOPPING"]) - 40, py(KZ0), py(KZ1), "680", f8, INK, "l")
# OVEN plan: govde 1010 derin, 180 arkaya tasar
d.rectangle([fx(FX0), py(FZ0), fx(FX0 + FIRIN_L), py(40.0)], fill=BG, outline=FIRIN, width=3)
d.rectangle([fx(FX0), py(-400.0 - FBANT_W / 2), fx(FX0 + FIRIN_L), py(-400.0 + FBANT_W / 2)], fill=(255, 236, 220), outline=FIRIN, width=1)
drect(fx(hz0), py(FZ0 + 40), fx(hz0 + HAZNE), py(0.0), FIRIN, 2)
txt(fx(FX0 + FIRIN_L / 2), py(-560.0), "PS536 · 1524 × 1010", f8, FIRIN, "mm")
txt(fx(FX0 + FIRIN_L / 2), py(-400.0), "FIRIN BANDI 508 · sürekli", f7, FIRIN, "mm")
txt(fx(FX0 + FIRIN_L / 2), py(-880.0), "180 arkaya taşar", f7, RED, "mm")
olcu_v(fx(FX0) + 30, py(FZ0), py(40.0), "1010", f9, FIRIN, "r")
olcu_v(fx(FX0) + 130, py(FZ0), py(-790.0), "180", f7, RED, "r")
olcu_v(fx(X0["OVEN"]) - 40, py(-400.0 - FBANT_W / 2), py(-400.0 + FBANT_W / 2), "508", f8, FIRIN, "l")
# KESME plan
d.rectangle([fx(PLK_X0), py(BANT_Z0), fx(PLK_X1), py(BANT_Z1)], fill=(232, 244, 250), outline=BANT, width=2)
d.ellipse([fx(kx0 + 140), py(-560.0), fx(kx0 + 460), py(-240.0)], outline=INK, width=2)
for k in range(4):
    a = k * math.pi / 4
    d.line([(fx(kx0 + 300) - 160 * S * math.cos(a), py(-400.0) - 160 * S * math.sin(a)),
            (fx(kx0 + 300) + 160 * S * math.cos(a), py(-400.0) + 160 * S * math.sin(a))], fill=INK, width=1)
txt(fx(kx0 + 300), py(-620.0), "KESİCİ Ø320 · 8 bıçak", f7, INK, "mm")
d.rectangle([fx(kx0 + 40), py(-460.0), fx(kx0 + 100), py(-340.0)], fill=BG, outline=INK, width=2)
txt(fx(kx0 + 70), py(-500.0), "İTİCİ", f7, INK, "mm")
d.ellipse([fx(kx0 + 20) - 6, py(-660.0) - 6, fx(kx0 + 20) + 6, py(-660.0) + 6], fill=RED)
txt(fx(kx0 + 20), py(-700.0), "SPREY", f7, RED, "mm")
ok(fx(kx0 + 110), py(-400.0), fx(kx0 + 130), py(-400.0), INK, 2)
# PACK plan
d.rectangle([fx(pk0 + 50), py(-400.0 - KUTU / 2), fx(pk0 + 50 + KUTU), py(-400.0 + KUTU / 2)], fill=BG, outline=INK, width=2)
txt(fx(pk0 + 210), py(-400.0) - 12, "KUTU 320 × 320", f8, INK, "mm")
txt(fx(pk0 + 210), py(-400.0) + 12, "plaka kotunda", f7, GRAY, "mm")
drect(fx(pk0 + 150), py(-785.5), fx(pk0 + 550), py(-25.5), GRAY, 1)
txt(fx(pk0 + 350), py(-700.0), "BLANK 400 × 760 · altta", f7, GRAY, "mm")
ok(fx(PLK_X1 - 40), py(-400.0), fx(pk0 + 50), py(-400.0), INK, 2)
olcu_h(fx(0), fx(HAT), py(40.0) + 96, "HAT  %s" % sayi(HAT), f13, INK)
olcu_v(fx(0) - 44, py(-790.0), py(40.0), "830", f11, INK, "l")
txt(fx(HAT / 2), py(40.0) + 150, "ÖN  ·  robot tarafı  ·  kaset değişimi önden", f9, GRAY, "mm")

# ======================= YAN GORUNUS (TOPPING KESITI) =======================
txt(SX, FY_TOP - 150, "YAN GÖRÜNÜŞ", f16, ACC)
txt(SX, FY_TOP - 112, "TOPPING kesiti · K2 kolonu üstü", f9, GRAY)
d.rectangle([sz(-790), fy(H), sz(40), fy(0)], fill=FILL, outline=LINE, width=3)
d.rectangle([sz(-790), fy(120), sz(40), fy(0)], fill=SOFT, outline=LINE, width=2)
# STORE K2 kesiti
TOP2 = 1140.0
d.rectangle([sz(-788.5), fy(TOP2), sz(-728.5), fy(121.5)], fill=PUC, outline=GRAY, width=1)      # arka PU
d.rectangle([sz(-727.5), fy(181.5), sz(0.0), fy(121.5)], fill=PUC, outline=GRAY, width=1)         # taban PU
d.rectangle([sz(-727.5), fy(TOP2 + 60.0), sz(0.0), fy(TOP2)], fill=PUC, outline=GRAY, width=1)    # tavan PU
d.rectangle([sz(-727.5), fy(TOP2), sz(-680.0), fy(CELL0)], fill=(250, 250, 251), outline=GRAY, width=1)
y0 = CELL0
for i in range(7):
    d.rectangle([sz(-680.0), fy(y0 + 88.0), sz(0.0), fy(y0)], fill=BG, outline=DOLAP, width=1)
    d.rectangle([sz(0.0), fy(y0 + 88.0 + BIND), sz(40.0), fy(y0 - BIND)], fill=BG, outline=DOLAP, width=1)
    y0 += 88.0 + 2 * BIND + FUGA
txt(sz(-340), fy(660.0), "ÇEKMECE 680 × 7", f9, INK, "mm")
txt(sz(-340), fy(660.0) + 26, "TAZE PİDE 6 + PAKET 1 · +3 °C", f7, DOLAP, "mm")
# bant kati
d.rectangle([sz(BANT_Z0), fy(Y_BANT), sz(BANT_Z1), fy(Y_BANT - 100.0)], fill=BG, outline=BANT, width=2)
d.line([(sz(BANT_Z0), fy(Y_BANT)), (sz(BANT_Z1), fy(Y_BANT))], fill=BANT, width=5)
txt(sz(-400), fy(Y_BANT - 50.0), "BANT 400", f7, BANT, "mm")
d.rectangle([sz(-550.0), fy(Y_BANT + 20.0), sz(-250.0), fy(Y_BANT)], fill=(240, 214, 170), outline=(200, 160, 80), width=2)   # urun
d.rectangle([sz(-550.0), fy(Y_HEAD1), sz(-250.0), fy(Y_HEAD0)], fill=HEAD, outline=BANT, width=2)
txt(sz(-400), fy((Y_HEAD0 + Y_HEAD1) / 2), "DOZAJ BAŞLIĞI 300", f7, BANT, "mm")
d.rectangle([sz(KZ0), fy(Y_DOZ1), sz(KZ1), fy(Y_DOZ0)], fill=KAS, outline=INK, width=2)
d.rectangle([sz(-797.5), fy(Y_DOZ1 - 20), sz(KZ0), fy(Y_DOZ0 + 20)], fill=(255, 230, 230), outline=RED, width=1)
txt(sz(-355), fy((Y_DOZ0 + Y_DOZ1) / 2) - 12, "DOZAJ KASETİ 140 × 240 × 680", f8, INK, "mm")
txt(sz(-355), fy((Y_DOZ0 + Y_DOZ1) / 2) + 12, "helezon Ø70 · ağız 45 × 50 önde", f7, GRAY, "mm")
d.rectangle([sz(-80.0), fy(Y_DOZ0), sz(-30.0), fy(Y_DOZ0 - 60.0)], fill=RED)                      # agiz -> oluk
dline((sz(-55.0), fy(Y_DOZ0 - 60.0)), (sz(-250.0), fy(Y_HEAD1)), RED, 2)
d.line([(sz(KZ0 - 10), fy(Y_DEP0 - 10)), (sz(KZ1 + 10), fy(Y_DEP0 - 10))], fill=LINE, width=3)
d.rectangle([sz(KZ0), fy(Y_DEP1), sz(KZ1), fy(Y_DEP0)], fill=KAS, outline=INK, width=2)
txt(sz(-355), fy((Y_DEP0 + Y_DEP1) / 2), "DEPO KASETİ · raf %s" % sayi(Y_DEP0), f8, INK, "mm")
d.rectangle([sz(0.0), fy(1968.0), sz(40.0), fy(Y_BANT - 110.0)], fill=SOFT, outline=LINE, width=1)      # on kapak
txt(sz(20), fy(1600.0), "K", f7, GRAY, "mm")
# olculer
olcu_h(sz(-790), sz(40), fy(0) + 44, "830", f11, INK)
olcu_h(sz(BANT_Z0), sz(BANT_Z1), fy(H) - 26, "bant 400", f8, BANT)
olcu_h(sz(-797.5), sz(KZ0), fy(H) - 60, "102", f7, RED)
for yy in (120.0, CELL0, TOP2, Y_BANT, Y_DOZ0, Y_DOZ1, Y_DEP0, H):
    d.line([(sz(40) + 6, fy(yy)), (sz(40) + 24, fy(yy))], fill=INK, width=2)
    txt(sz(40) + 30, fy(yy), sayi(yy), f8, INK, "lm")

# ======================= LEJANT =======================
d.line([(OX, H_PX - 130), (W_PX - 170, H_PX - 130)], fill=LINE, width=2)
ly = H_PX - 78
LEJ = [(LINE, BG, "kapak / panel", False), (RED, AGZ, "açık ağız", False), (DOLAP, BG, "çekmece +3 °C", False),
       (BANT, (232, 244, 250), "bant / plaka", False), (FIRIN, BG, "konveyör fırın", False), (INK, KAS, "kaset", False),
       (GRAY, PUC, "PU yalıtım", False), (RED, (255, 230, 230), "motor paketi · 830 dışı", False), (BANT, BG, "dozaj başlığı izi", True)]
xx = OX
for c, fl, a_, kes in LEJ:
    if kes:
        drect(xx, ly - 12, xx + 30, ly + 12, c, 2)
    else:
        d.rectangle([xx, ly - 12, xx + 30, ly + 12], fill=fl, outline=c, width=3)
    txt(xx + 42, ly, a_, f9, INK, "lm")
    xx += 42 + d.textlength(a_, font=f9) + 56
txt(W_PX - 170, ly, "HAT %s × 1970 × 830 (OVEN 1010)  ·  STORE %d çekmece (43 gerekli)  ·  6 dozaj + 6 depo kaseti  ·  fırın hazne 914" % (sayi(HAT), CEK), f9, GRAY, "rm")

assert not os.path.exists(OUT), "v1 zaten var — yeni numara ver"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.save(OUT)
print("yazildi:", OUT, "· hat %s · STORE %d cekmece" % (sayi(HAT), CEK))
