# -*- coding: utf-8 -*-
"""AUTOKITCH - TABLALI HAT · MODULER v5 · HER SEY 1 GUN (14 Eyl 2026): ON + UST GORUNUS. Olculer mm.
Kemal (v4 duzeltmesi): cekmeceleri saga dogru ayni yere topla; soldaki TEKNIK modulunu kaldir, sogutma grubu + hat panosunu PRESS ve TOPPING altina koy.
1 GUN: pide 80 = 4 cekmece (20'lik) · lahmacun 200 = 6 cekmece (35'lik) · icecek 70 = KESME altinda 2 dar cekmece (40'lik) · kutu 280 blank.
MODULLER: PRESS 670 (alti SOGUTMA GRUBU) | TOPPING 885 (alti: solda 220 HAT PANOSU + sagda cekmece kolonu) | OVEN 1420 | KESME 500 | PACK 700 = 4175.
TAM ARAMA (pide + lahm 990 mm; kolon tavani TOPPING Hb-421, OVEN Hb-440): TOPPING 4 lahm 372 · OVEN-A 2 pide + 1 lahm 309 · OVEN-B ayni -> tabla 793 -> 795, yukseklik 1465.
  hepsi OVEN altina: 2 pide + 3 lahm x 2 = 495 -> tabla 935, yukseklik 1605 (PRESS/TOPPING alti TEKNIK'e fazla gelir, bos kalir).
TEKNIK: PRESS alti bolme 620 x 395 x 780 -> sogutma grubu (~450 x 330, varsayim) sigar; TOPPING alti sol serit 220 x 374 x 780 -> duz pano (~400 x 600) girmez,
  one kizakli dikey plaka pano (~200 x 350 x 750, varsayim). Sarjor 280 x 2,13 = 596 <= tabla - 140 = 655.
Kural: paftada yalniz gorunus + olcu + parca adi; aciklama mesajda.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE\HAT_MODULER_v5_hersey1gun_teknik.png".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX = 3800, 2460
S = 0.62
BG, INK, GRAY, LINE = (255, 255, 255), (26, 26, 28), (132, 132, 140), (72, 72, 78)
FILL, ACC, RED, SOFT = (246, 246, 248), (0, 86, 184), (198, 42, 32), (228, 228, 234)
DOLAP, BOSL, PUC, SOGUK, YUN = (14, 120, 90), (190, 190, 196), (255, 240, 200), (226, 238, 252), (250, 236, 210)
FIRIN, HAVA, AGZ, TABF, TOPC, TOPK = (200, 90, 30), (255, 225, 200), (253, 244, 243), (214, 226, 244), (240, 214, 170), (200, 160, 80)


def F(sz, b=False):
    for n in (("arialbd.ttf", "segoeuib.ttf") if b else ("arial.ttf", "segoeui.ttf")):
        try:
            return ImageFont.truetype(n, sz)
        except Exception:
            pass
    return ImageFont.load_default()


f7, f8, f9, f11, f13, f16, f38 = F(15), F(17), F(19), F(22), F(25), F(29, True), F(54, True)
im = Image.new("RGB", (W_PX, H_PX), BG)
d = ImageDraw.Draw(im)


def txt(x, y, s, f=f11, c=INK, a="la"):
    d.text((x, y), s, font=f, fill=c, anchor=a)


def sayi(v):
    return ("%g" % v).replace(".", ",")


def olcu_h(x0, x1, y, s, f=f9, c=INK):
    d.line([(x0, y), (x1, y)], fill=c, width=2)
    for xx in (x0, x1):
        d.line([(xx, y - 7), (xx, y + 7)], fill=c, width=2)
    tw = d.textlength(s, font=f)
    d.rectangle([(x0 + x1) / 2 - tw / 2 - 5, y - 12, (x0 + x1) / 2 + tw / 2 + 5, y + 12], fill=BG)
    txt((x0 + x1) / 2, y, s, f, c, "mm")


def olcu_v(x, y0, y1, s, f=f9, c=INK, yon="r"):
    d.line([(x, y0), (x, y1)], fill=c, width=2)
    for yy in (y0, y1):
        d.line([(x - 7, yy), (x + 7, yy)], fill=c, width=2)
    txt(x + (10 if yon == "r" else -10), (y0 + y1) / 2, s, f, c, "lm" if yon == "r" else "rm")


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
        t0, t1 = min(1.0, i * (dash + gap) / L), min(1.0, (i * (dash + gap) + dash) / L)
        d.line([(ax + (bx - ax) * t0, ay + (by - ay) * t0), (ax + (bx - ax) * t1, ay + (by - ay) * t1)], fill=c, width=w)


def drect(x0, y0, x1, y1, c, w=1):
    dline((x0, y0), (x1, y0), c, w); dline((x1, y0), (x1, y1), c, w)
    dline((x1, y1), (x0, y1), c, w); dline((x0, y1), (x0, y0), c, w)


def ok(x0, y0, x1, y1, c, w=3):
    d.line([(x0, y0), (x1, y1)], fill=c, width=w)
    a = math.atan2(y1 - y0, x1 - x0)
    for s_ in (-0.5, 0.5):
        d.line([(x1, y1), (x1 - 14 * math.cos(a + s_), y1 - 14 * math.sin(a + s_))], fill=c, width=w)


def yalitim(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=YUN, outline=GRAY, width=1)
    tarali(x0 + 1, y0 + 1, x1 - 1, y1 - 1, (215, 190, 150), 9)


# ======================= VERI =======================
HB = 795.0                                  # tabla / bant kotu
H = HB + 670.0                               # 1465 · tum moduller ayni
assert 280 * 2.13 <= HB - 140.0, "sarjor 1 gun sigmiyor"
MOD = [("PRESS", "PRESS", 670.0), ("TOPPING", "TOPPING · Atosa uyarlama", 885.0),
       ("OVEN", "OVEN · özel konveyör", 1420.0), ("KESME", "KESME · altı içecek", 500.0), ("PACK", "PACK", 700.0)]
X0, _x = {}, 0.0
for k, _, w in MOD:
    X0[k] = _x
    _x += w
HAT = _x                                     # 4830
W = {k: w for k, _, w in MOD}
ADIM = {"pide": 108.0, "lahm": 93.0, "icecek": 165.0}
RAF = 418.0
ADET = {"pide": 20, "lahm": 35, "icecek": 56}
ADK = {"pide": "TAZE PİDE", "lahm": "LAHMACUN", "icecek": "İÇECEK"}
BRK = {"pide": "top", "lahm": "top", "icecek": "kutu"}
RAFAD = {1: "raf 1 · HARÇ ×4", 2: "raf 2 · KIYMA ×2 + KAŞAR", 3: "raf 3 · KAŞAR + KUŞ. ×4 + SUC. ×2"}
# (modul, kolon sol kenari (modulden), ust sinir, icerik alttan uste)
KOLON = [("TOPPING", 247.5, HB - 381.0, [(4, "lahm")]),
         ("OVEN", 72.5, HB - 400.0, [(2, "pide"), (1, "lahm")]),
         ("OVEN", 727.5, HB - 400.0, [(2, "pide"), (1, "lahm")])]
say = {"pide": 0, "lahm": 0, "icecek": 0}
for m, off, ust, its in KOLON:
    y = 40.0
    for it in its:
        y += RAF if it[0] == "raf" else it[0] * ADIM[it[1]]
        if it[0] != "raf":
            say[it[1]] += it[0]
    assert y <= ust + 0.5, ("kolon tasiyor", m, y, ust)
assert say == {"pide": 4, "lahm": 6, "icecek": 0}, say          # icecek KESME altinda (dar cekmece)
# Atosa (tabla kotuna gore)
AB0, Y_RAY0, Y_RAY1, Y_DAML, Y_AGIZ, Y_HZ0, Y_HZ1, Y_KAPAK = HB - 321, HB - 280, HB - 250, HB - 150, HB + 190, HB + 230, HB + 590, HB + 620
FY0, FY1 = HB - 300.0, HB + 320.0           # firin govdesi 620
GEN = {"sos": 245.0, "peynir": 510.0, "topping": 95.0}
DOLUM = {"HARÇ": "11 kg", "KIYMA": "3,2 kg", "KUŞBAŞI": "1,45 kg", "KAŞAR": "4,4 kg", "SUCUK": "1,4 kg"}
ON_SIRA = [("KAŞAR", "peynir"), ("HARÇ", "sos")]
AR_SIRA = [("HARÇ", "sos"), ("KIYMA", "sos"), ("KUŞBAŞI", "topping"), ("KUŞBAŞI", "topping"), ("SUCUK", "topping")]


def dizi(sira):
    out, k = [], X0["TOPPING"] + 35.0
    for ad_, tip_ in sira:
        out.append((k, GEN[tip_], ad_, tip_))
        k += GEN[tip_] + 10.0
    assert k - 10.0 <= X0["TOPPING"] + W["TOPPING"] - 35.0
    return out


ONX, ARX = dizi(ON_SIRA), dizi(AR_SIRA)
PCX = X0["PRESS"] + 335.0
TX_D = ONX[0][0] + ONX[0][1] / 2
TX_F = X0["TOPPING"] + W["TOPPING"] - 180.0
RAY0, RAY1 = X0["PRESS"] + 120.0, X0["TOPPING"] + W["TOPPING"] - 40.0
OW, HAZNE, PITCH = 1420.0, 1320.0, 330.0

# ======================= YERLESIM =======================
OX = 300.0
FYP = 360.0 + H * S                           # zemin (on gorunus)
PY_TOP = FYP + 300.0
fx = lambda x: OX + x * S
fy = lambda y: FYP - y * S
py = lambda z: PY_TOP + (z + 790.0) * S

txt(OX, 60, "AUTOKITCH  ·  TABLALI HAT  ·  MODÜLER  v5  ·  HER ŞEY 1 GÜN", f38, INK)
txt(OX, 128, "ön görünüş + üst görünüş  ·  her istasyon ayrı dolap, birleşince üst/alt/ön/arka çizgiler hizalı  ·  ayak yok  ·  hat %s × %s × 830  ·  tabla / bant %s  ·  her şey 1 gün  ·  soğutma grubu PRESS altında, hat panosu TOPPING altında  ·  ölçüler mm  ·  14 Eylül 2026" % (sayi(HAT), sayi(H), sayi(HB)), f13, GRAY)
d.line([(OX, 170), (W_PX - 150, 170)], fill=LINE, width=3)

# ======================= ON GORUNUS =======================
txt(OX, fy(H) - 130, "ÖN GÖRÜNÜŞ  ·  robot tarafı", f16, ACC)
for k, ad, w in MOD:
    x0 = X0[k]
    d.rectangle([fx(x0), fy(H), fx(x0 + w), fy(0)], fill=FILL)
    txt(fx(x0 + w / 2), fy(H) - 60, ad, f11, INK, "md")
    olcu_h(fx(x0), fx(x0 + w), fy(H) - 26, sayi(w), f9, INK)


def dolap_zemin(x0, x1, ust):
    d.rectangle([fx(x0), fy(40.0), fx(x1), fy(0)], fill=PUC, outline=GRAY, width=1)
    d.rectangle([fx(x0), fy(ust + 60.0), fx(x1), fy(ust)], fill=PUC, outline=GRAY, width=1)
    d.rectangle([fx(x0), fy(ust), fx(x1), fy(40.0)], fill=(250, 250, 251))


# --- soguk alt bolmeler (modul genisligi icinde)
for m, _, ust, _ in {(k[0], 0, k[2], 0) for k in KOLON}:
    dolap_zemin(X0[m], X0[m] + W[m], ust)
for m, off, ust, its in KOLON:
    cx = X0[m] + off
    y = 40.0
    for it in its:
        if it[0] == "raf":
            d.rectangle([fx(cx + 6), fy(y + RAF - 3), fx(cx + 614), fy(y)], fill=BG, outline=INK, width=2)
            txt(fx(cx + 310), fy(y + RAF / 2) - 12, "YEDEK HAZNE RAFI · kızaklı", f8, INK, "mm")
            txt(fx(cx + 310), fy(y + RAF / 2) + 12, RAFAD[it[1]], f7, GRAY, "mm")
            y += RAF
            continue
        n, tip = it
        h = ADIM[tip]
        ybas = y
        for _ in range(n):
            d.rectangle([fx(cx + 6), fy(y + h - 3), fx(cx + 614), fy(y)], fill=BG, outline=DOLAP, width=1)
            y += h
        ym = (fy(ybas) + fy(y)) / 2
        for k_, (ss, ff, cc) in enumerate(((("%s × %d" % (ADK[tip], n)), f8, INK), ("%d %s/çekmece" % (ADET[tip], BRK[tip]), f7, DOLAP))):
            tw = d.textlength(ss, font=ff)
            yy = ym + (-11 if k_ == 0 else 11) if n > 1 else ym + (-9 if k_ == 0 else 9)
            if n == 1 and k_ == 1:
                continue
            d.rectangle([fx(cx + 310) - tw / 2 - 5, yy - 10, fx(cx + 310) + tw / 2 + 5, yy + 10], fill=BG, outline=DOLAP, width=1)
            txt(fx(cx + 310), yy, ss, ff, cc, "mm")
    if ust - y > 15:
        tarali(fx(cx + 6) + 1, fy(ust) + 1, fx(cx + 614) - 1, fy(y) - 1)
# TOPPING alti sol serit: HAT PANOSU (one kizakli dikey plaka, varsayim)
pn0, pn1 = X0["TOPPING"] + 10.0, X0["TOPPING"] + 230.0
d.rectangle([fx(pn0), fy(HB - 381.0), fx(pn1), fy(40.0)], fill=BG, outline=INK, width=2)
pym = fy((40.0 + HB - 381.0) / 2)
txt(fx((pn0 + pn1) / 2), pym - 22, "HAT PANOSU", f8, INK, "mm")
txt(fx((pn0 + pn1) / 2), pym, "PLC · kontaktör", f7, GRAY, "mm")
txt(fx((pn0 + pn1) / 2), pym + 20, "öne kızaklı", f7, GRAY, "mm")
# PRESS alti: SOGUTMA GRUBU bolmesi
d.rectangle([fx(X0["PRESS"] + 25.0), fy(HB - 360.0), fx(X0["PRESS"] + 645.0), fy(40.0)], fill=BG, outline=INK, width=2)
sym = fy((40.0 + HB - 360.0) / 2)
txt(fx(X0["PRESS"] + 335.0), sym - 11, "SOĞUTMA GRUBU", f8, INK, "mm")
txt(fx(X0["PRESS"] + 335.0), sym + 11, "çekmeceler", f7, GRAY, "mm")
# --- PRESS
px0 = X0["PRESS"] + 15.0
d.rectangle([fx(px0), fy(FY0 + 950.0), fx(px0 + 640.0), fy(FY0)], fill=BG, outline=INK, width=2)
txt(fx(PCX), fy(FY0 + 820.0) - 12, "FERSAH PZP-400", f9, INK, "mm")
txt(fx(PCX), fy(FY0 + 820.0) + 12, "640 × 950 × 800", f7, GRAY, "mm")
d.rectangle([fx(px0 + 20), fy(HB + 260.0), fx(px0 + 620), fy(FY0 + 10)], fill=AGZ, outline=RED, width=3)
txt(fx(PCX), fy(HB + 205.0), "PRES AĞZI + TABLA / RAY GEÇİŞİ", f8, RED, "mm")
d.rectangle([fx(PCX - 150), fy(HB - 20.0), fx(PCX + 150), fy(HB - 120.0)], fill=(150, 150, 158), outline=INK, width=2)
txt(fx(PCX), fy(HB - 70.0), "ÖRS", f8, BG, "mm")
drect(fx(PCX - 170), fy(HB), fx(PCX + 170), fy(HB - 20.0), ACC, 2)
# --- TOPPING (Atosa)
tx0 = X0["TOPPING"]
d.rectangle([fx(tx0), fy(H), fx(tx0 + W["TOPPING"]), fy(AB0)], fill=BG, outline=LINE, width=2)
d.rectangle([fx(tx0), fy(H), fx(tx0 + W["TOPPING"]), fy(Y_KAPAK)], fill=SOFT, outline=LINE, width=1)
txt(fx(tx0 + W["TOPPING"] / 2), fy((H + Y_KAPAK) / 2), "ÜST KAPAK 50 · hazneler üstten takılır", f7, INK, "mm")
d.rectangle([fx(tx0 + 35), fy(Y_KAPAK), fx(tx0 + W["TOPPING"] - 35), fy(Y_AGIZ + 40)], fill=SOGUK, outline=ACC, width=1)
d.rectangle([fx(tx0 + 35), fy(Y_AGIZ + 40), fx(tx0 + W["TOPPING"] - 35), fy(Y_AGIZ)], fill=YUN, outline=GRAY, width=1)
for x_, w_, ad_, tip_ in ONX:
    cx_ = x_ + w_ / 2
    d.rectangle([fx(x_), fy(Y_HZ1), fx(x_ + w_), fy(Y_HZ0)], fill=BG, outline=INK, width=2)
    d.rectangle([fx(cx_ - 15), fy(Y_AGIZ), fx(cx_ + 15), fy(Y_AGIZ - 12)], fill=RED)
    txt(fx(cx_), fy(Y_HZ1 - 90), ad_, f8, INK, "mm")
    txt(fx(cx_), fy(Y_HZ0 + 90), DOLUM[ad_], f7, RED, "mm")
txt(fx(tx0 + W["TOPPING"] / 2), fy(Y_KAPAK - 14), "SOĞUK BÖLME +3 °C · arka sıra: HARÇ · KIYMA · KUŞ. ×2 · SUC.", f7, ACC, "mm")
d.rectangle([fx(tx0 + 35), fy(Y_AGIZ), fx(tx0 + W["TOPPING"] - 35), fy(Y_DAML + 40)], fill=(250, 250, 251), outline=GRAY, width=1)
d.rectangle([fx(tx0 + 35), fy(Y_DAML + 40), fx(tx0 + W["TOPPING"] - 35), fy(Y_DAML)], fill=SOFT, outline=LINE, width=1)
txt(fx(tx0 + 560), fy(Y_DAML + 20), "DAMLAMA TAVASI", f7, INK, "mm")
d.rectangle([fx(tx0), fy(Y_DAML), fx(tx0 + W["TOPPING"]), fy(AB0)], fill=(250, 250, 251), outline=LINE, width=1)
tarali(fx(tx0) + 1, fy(Y_DAML) + 1, fx(tx0 + W["TOPPING"]) - 1, fy(AB0) - 1)
d.rectangle([fx(RAY0), fy(Y_RAY1), fx(RAY1), fy(Y_RAY0)], fill=ACC)
for i_, t_ in enumerate(("RAY + MOTOR PAYI 171", "x kızak · kaldırma · döndürme")):
    tw = d.textlength(t_, font=f8 if i_ == 0 else f7)
    yy = fy(HB - 180.0) + i_ * 20
    d.rectangle([fx(tx0 + 640) - tw / 2 - 5, yy - 10, fx(tx0 + 640) + tw / 2 + 5, yy + 10], fill=BG)
    txt(fx(tx0 + 640), yy, t_, f8 if i_ == 0 else f7, INK, "mm")
d.rectangle([fx(TX_D - 110), fy(Y_RAY1 + 90), fx(TX_D + 110), fy(Y_RAY1)], fill=BG, outline=ACC, width=2)
d.rectangle([fx(TX_D - 12), fy(Y_AGIZ - 60), fx(TX_D + 12), fy(Y_RAY1 + 90)], fill=(150, 150, 158))
d.rectangle([fx(TX_D - 170), fy(Y_AGIZ - 40), fx(TX_D + 170), fy(Y_AGIZ - 60)], fill=TABF, outline=ACC, width=3)
d.ellipse([fx(TX_D - 150), fy(Y_AGIZ - 28), fx(TX_D + 150), fy(Y_AGIZ - 40)], fill=TOPC, outline=TOPK, width=2)
txt(fx(tx0 + 640), fy(HB + 80.0), "TABLA Ø340 · kalkar, döner + kayar", f7, ACC, "mm")
drect(fx(TX_F - 170), fy(HB), fx(TX_F + 170), fy(HB - 20), ACC, 2)
ok(fx(PCX + 190), fy(HB + 30), fx(tx0 + 120), fy(HB + 30), ACC, 3)
ok(fx(TX_F + 120), fy(HB + 30), fx(tx0 + W["TOPPING"] + 60), fy(HB + 30), FIRIN, 3)
# --- OVEN
ox0 = X0["OVEN"]
HZ0, HZ1 = ox0 + 50.0, ox0 + 50.0 + HAZNE
d.rectangle([fx(ox0), fy(FY0), fx(ox0 + OW), fy(FY0 - 40)], fill=BG, outline=GRAY, width=1)
txt(fx(ox0 + OW / 2), fy(FY0 - 20), "havalandırma 40", f7, GRAY, "mm")
yalitim(fx(ox0), fy(FY1), fx(ox0 + OW), fy(FY1 - 50))
yalitim(fx(ox0), fy(FY0 + 50), fx(ox0 + OW), fy(FY0))
yalitim(fx(ox0), fy(FY1), fx(ox0 + 50), fy(FY0))
yalitim(fx(ox0 + OW - 50), fy(FY1), fx(ox0 + OW), fy(FY0))
d.rectangle([fx(HZ0), fy(FY1 - 50), fx(HZ1), fy(FY0 + 50)], fill=BG, outline=FIRIN, width=2)
d.rectangle([fx(HZ0), fy(FY1 - 50), fx(HZ1), fy(HB + 120)], fill=HAVA, outline=FIRIN, width=1)
d.rectangle([fx(HZ0), fy(HB - 70), fx(HZ1), fy(FY0 + 50)], fill=HAVA, outline=FIRIN, width=1)
for k in range(7):
    xa = HZ0 + 60 + k * 185
    d.rectangle([fx(xa), fy(HB + 120), fx(xa + 80), fy(HB + 70)], fill=BG, outline=FIRIN, width=1)
    d.rectangle([fx(xa), fy(HB - 40), fx(xa + 80), fy(HB - 70)], fill=BG, outline=FIRIN, width=1)
d.line([(fx(ox0 - 10), fy(HB)), (fx(ox0 + OW + 10), fy(HB))], fill=FIRIN, width=5)
for k in range(4):
    c_ = HZ0 + PITCH / 2 + k * PITCH
    d.ellipse([fx(c_ - 150), fy(HB + 30), fx(c_ + 150), fy(HB + 2)], fill=TOPC, outline=TOPK, width=2)
txt(fx(HZ0 + 660), fy(HB + 180), "ÜST PLENUM · hava parmakları × 7", f8, FIRIN, "mm")
txt(fx(HZ0 + 660), fy(HB - 140), "ALT PLENUM · hava parmakları × 7", f8, FIRIN, "mm")
txt(fx(HZ0 + 660), fy(FY0 + 75), "PİŞİRME HAZNESİ 1320 · 4 ürün · adım 330 · 60 ürün/saat", f7, FIRIN, "mm")
d.rectangle([fx(ox0 + 33), fy(H - 2), fx(ox0 + OW - 33), fy(FY1 + 40)], fill=BG, outline=LINE, width=2)
txt(fx(ox0 + OW / 2), fy((H + FY1 + 40) / 2), "EGZOZ DAVLUMBAZI · fan · yağ + karbon filtre", f9, INK, "mm")
olcu_h(fx(HZ0), fx(HZ1), fy(FY1) - 22, "HAZNE 1320", f8, FIRIN)
# --- KESME + TEKNIK
kx0 = X0["KESME"]
d.rectangle([fx(kx0 + 10), fy(HB), fx(kx0 + 490), fy(HB - 100)], fill=BG, outline=ACC, width=2)
d.line([(fx(kx0 + 10), fy(HB)), (fx(kx0 + 490), fy(HB))], fill=ACC, width=5)
txt(fx(kx0 + 250), fy(HB - 50), "KESME PLAKASI 460 × 450", f7, ACC, "mm")
d.rectangle([fx(kx0 + 40), fy(HB + 400), fx(kx0 + 460), fy(HB + 60)], fill=BG, outline=INK, width=2)
txt(fx(kx0 + 250), fy(HB + 230) - 11, "KESİCİ · 8 bıçak", f8, INK, "mm")
txt(fx(kx0 + 250), fy(HB + 230) + 11, "sprey · itici", f7, GRAY, "mm")
d.rectangle([fx(kx0 + 33), fy(H - 2), fx(kx0 + 467), fy(HB + 430)], fill=BG, outline=LINE, width=2)
txt(fx(kx0 + 250), fy((H + HB + 430) / 2), "TAHRİK · YAĞ KABI", f8, INK, "mm")
# KESME alti: dar icecek cekmecesi x 2 (5 kanal x 8 = 40 kutu)
KUST = HB - 160.0
dolap_zemin(kx0, kx0 + W["KESME"], KUST)
yk = 40.0
for _ in range(2):
    d.rectangle([fx(kx0 + 26), fy(yk + ADIM["icecek"] - 3), fx(kx0 + 474), fy(yk)], fill=BG, outline=DOLAP, width=1)
    yk += ADIM["icecek"]
assert yk <= KUST
for k_, (ss, ff, cc) in enumerate((("İÇECEK × 2 · dar", f8, INK), ("40 kutu/çekmece", f7, DOLAP))):
    tw = d.textlength(ss, font=ff)
    yy = (fy(40.0) + fy(yk)) / 2 + (-11 if k_ == 0 else 11)
    d.rectangle([fx(kx0 + 250) - tw / 2 - 5, yy - 10, fx(kx0 + 250) + tw / 2 + 5, yy + 10], fill=BG, outline=DOLAP, width=1)
    txt(fx(kx0 + 250), yy, ss, ff, cc, "mm")
tarali(fx(kx0 + 26) + 1, fy(KUST) + 1, fx(kx0 + 474) - 1, fy(yk) - 1)
txt(fx(kx0 + 250), (fy(KUST) + fy(yk)) / 2, "boş %s" % sayi(KUST - yk), f7, GRAY, "mm")
# --- PACK
pk0 = X0["PACK"]
d.rectangle([fx(pk0 + 33), fy(HB - 100), fx(pk0 + 667), fy(40.0)], fill=BG, outline=INK, width=2)
txt(fx(pk0 + 350), fy((HB - 100 + 40) / 2) - 11, "ŞARJÖR · 280 blank", f8, INK, "mm")
txt(fx(pk0 + 350), fy((HB - 100 + 40) / 2) + 11, "alttan kaldırmalı", f7, GRAY, "mm")
d.rectangle([fx(pk0 + 30), fy(HB + 300), fx(pk0 + 670), fy(HB - 50)], fill=AGZ, outline=RED, width=3)
txt(fx(pk0 + 350), fy(HB + 125), "KUTULAMA AĞZI", f8, RED, "mm")
d.rectangle([fx(pk0 + 33), fy(H - 2), fx(pk0 + 667), fy(HB + 330)], fill=BG, outline=LINE, width=2)
txt(fx(pk0 + 350), fy((H + HB + 330) / 2), "KALIP · TAHRİK · PANO", f8, INK, "mm")
# --- modul sinirlari (hizali, en son)
for k, _, w in MOD:
    d.rectangle([fx(X0[k]), fy(H), fx(X0[k] + w), fy(0)], outline=INK, width=4)
d.line([(fx(-150), fy(0)), (fx(HAT + 150), fy(0))], fill=INK, width=2)
txt(fx(-150), fy(0) + 16, "zemin · ayak yok", f7, GRAY, "la")
olcu_h(fx(0), fx(HAT), fy(0) + 60, "HAT  %s" % sayi(HAT), f13, INK)
olcu_v(fx(0) - 40, fy(H), fy(0), sayi(H), f11, INK, "l")
for yy_, s_ in ((0, "0"), (40, "40"), (HB - 400, "%s çekmece üst (fırın altı)" % sayi(HB - 400)), (HB - 100, "%s şarjör üst" % sayi(HB - 100)), (HB, "%s tabla / bant" % sayi(HB)),
                (Y_AGIZ, "%s ağız" % sayi(Y_AGIZ)), (Y_HZ1, "%s hazne üst" % sayi(Y_HZ1)), (H, sayi(H))):
    d.line([(fx(HAT) + 6, fy(yy_)), (fx(HAT) + 22, fy(yy_))], fill=INK, width=2)
    txt(fx(HAT) + 28, fy(yy_), s_, f7, INK, "lm")

# ======================= UST GORUNUS =======================
txt(OX, py(-790) - 70, "ÜST GÖRÜNÜŞ  ·  kapaklar kaldırılmış", f16, ACC)
for k, ad, w in MOD:
    d.rectangle([fx(X0[k]), py(-790), fx(X0[k] + w), py(40)], fill=FILL)
# PRESS
d.rectangle([fx(px0), py(-788), fx(px0 + 640), py(12)], fill=BG, outline=INK, width=2)
txt(fx(PCX), py(-620), "FERSAH PZP-400 · 640 × 800", f7, INK, "mm")
d.ellipse([fx(PCX - 170), py(-490), fx(PCX + 170), py(-150)], outline=ACC, width=3)
txt(fx(PCX), py(-320), "TABLA Ø340 · örs", f7, ACC, "mm")
txt(fx(PCX), py(-70), "altında SOĞUTMA GRUBU", f7, GRAY, "mm")
# TOPPING
d.rectangle([fx(tx0), py(-760), fx(tx0 + W["TOPPING"]), py(40)], fill=BG, outline=LINE, width=2)
for z0, z1, fl_ in ((-50.0, 38.0, SOFT), (-695.0, -595.0, SOFT), (-760.0, -695.0, SOGUK)):
    d.rectangle([fx(tx0 + 35), py(z0), fx(tx0 + W["TOPPING"] - 35), py(z1)], fill=fl_, outline=GRAY, width=1)
txt(fx(tx0 + W["TOPPING"] / 2), py(18), "ÖN PANEL + ÖN SIRA TAHRİKİ", f7, INK, "mm")
txt(fx(tx0 + 300), py(-652), "ARKA SIRA TAHRİKİ", f7, INK, "mm")
txt(fx(tx0 + W["TOPPING"] / 2), py(-728), "EVAPORATÖR + FAN", f7, ACC, "mm")
for sira, z0, z1, agz, zl, pz0 in ((ONX, -305.0, -55.0, -289.0, -110.0, -38.0), (ARX, -585.0, -335.0, -351.0, -530.0, -625.0)):
    for x_, w_, ad_, tip_ in sira:
        cx_ = x_ + w_ / 2
        d.rectangle([fx(x_), py(z0), fx(x_ + w_), py(z1)], fill=BG, outline=INK, width=2)
        d.rectangle([fx(cx_ - 14), py(agz - 14), fx(cx_ + 14), py(agz + 14)], fill=RED)
        d.rectangle([fx(cx_ - 14), py(pz0), fx(cx_ + 14), py(pz0 + 28)], fill=RED)
        txt(fx(cx_), py(zl) - 11, ad_ if w_ > 150 else ad_[:3] + ".", f7, INK, "mm")
        txt(fx(cx_), py(zl) + 11, DOLUM[ad_], f7, GRAY, "mm")
dline((fx(RAY0), py(-320)), (fx(TX_F), py(-320)), ACC, 2)
d.ellipse([fx(TX_F - 170), py(-490), fx(TX_F + 170), py(-150)], outline=ACC, width=3)
# OVEN
yalitim(fx(ox0), py(-790), fx(ox0 + OW), py(-730))
yalitim(fx(ox0), py(-20), fx(ox0 + OW), py(40))
yalitim(fx(ox0), py(-730), fx(ox0 + 50), py(-20))
yalitim(fx(ox0 + OW - 50), py(-730), fx(ox0 + OW), py(-20))
d.rectangle([fx(HZ0), py(-730), fx(HZ1), py(-520)], fill=HAVA, outline=FIRIN, width=2)
for c_ in (HZ0 + 330, HZ0 + 990):
    d.ellipse([fx(c_ - 100), py(-725), fx(c_ + 100), py(-525)], outline=FIRIN, width=3)
    txt(fx(c_), py(-625), "FAN", f8, FIRIN, "mm")
for zz in (-580.0, -625.0, -670.0):
    d.line([(fx(HZ0 + 440), py(zz)), (fx(HZ0 + 880), py(zz))], fill=RED, width=3)
d.rectangle([fx(HZ0), py(-520), fx(HZ1), py(-20)], fill=BG, outline=FIRIN, width=2)
d.rectangle([fx(ox0 + 20), py(-495), fx(ox0 + OW - 20), py(-45)], fill=(255, 236, 220), outline=FIRIN, width=2)
for k in range(4):
    c_ = HZ0 + PITCH / 2 + k * PITCH
    d.ellipse([fx(c_ - 150), py(-420), fx(c_ + 150), py(-120)], fill=TOPC, outline=TOPK, width=2)
txt(fx(HZ0 + 660), py(-70), "PİŞİRME HAZNESİ 1320 × iç 500 · bant 450 · 5,5 mm/s", f7, FIRIN, "mm")
# KESME
d.rectangle([fx(kx0 + 20), py(-495), fx(kx0 + 480), py(-45)], fill=(232, 244, 250), outline=ACC, width=2)
d.ellipse([fx(kx0 + 90), py(-430), fx(kx0 + 410), py(-110)], outline=INK, width=2)
for k in range(4):
    a = k * math.pi / 4
    d.line([(fx(kx0 + 250) - 160 * S * math.cos(a), py(-270) - 160 * S * math.sin(a)), (fx(kx0 + 250) + 160 * S * math.cos(a), py(-270) + 160 * S * math.sin(a))], fill=INK, width=1)
d.rectangle([fx(kx0 + 30), py(-330), fx(kx0 + 80), py(-210)], fill=BG, outline=INK, width=2)
txt(fx(kx0 + 250), py(-600), "KESİCİ Ø320 · itici", f7, INK, "mm")
txt(fx(kx0 + 250), py(-700), "altında 2 dar içecek çekmecesi", f7, GRAY, "mm")
# PACK
d.rectangle([fx(pk0 + 50), py(-430), fx(pk0 + 370), py(-110)], fill=BG, outline=INK, width=2)
txt(fx(pk0 + 210), py(-270), "KUTU 320 × 320", f8, INK, "mm")
drect(fx(pk0 + 150), py(-785), fx(pk0 + 550), py(-25), GRAY, 1)
txt(fx(pk0 + 350), py(-700), "BLANK 400 × 760 · şarjör altta", f7, GRAY, "mm")
ok(fx(kx0 + 460), py(-270), fx(pk0 + 50), py(-270), INK, 2)
for k, ad, w in MOD:
    d.rectangle([fx(X0[k]), py(-790), fx(X0[k] + w), py(40)], outline=INK, width=4)
    olcu_h(fx(X0[k]), fx(X0[k] + w), py(40) + 34, "%s · %s" % (k, sayi(w)), f8, GRAY)
olcu_h(fx(0), fx(HAT), py(40) + 78, "HAT  %s" % sayi(HAT), f13, INK)
olcu_v(fx(0) - 40, py(-790), py(40), "830", f11, INK, "l")
txt(fx(HAT / 2), py(40) + 120, "ÖN · robot tarafı · tüm modüller 830 derin, ön ve arka yüzler aynı çizgide", f9, GRAY, "mm")

# ======================= LEJANT =======================
ly = H_PX - 60
d.line([(OX, ly - 42), (W_PX - 150, ly - 42)], fill=LINE, width=2)
xx = OX
for c, fl, a_ in ((INK, FILL, "modül dolabı (kalın çizgi = birleşim)"), (DOLAP, BG, "çekmece · adım pide 108 / lahmacun 93 / içecek 165"),
                  (GRAY, PUC, "PU yalıtım"), (ACC, SOGUK, "soğuk hazne bölmesi"), (FIRIN, HAVA, "fırın plenum"), (RED, AGZ, "açık ağız")):
    d.rectangle([xx, ly - 11, xx + 30, ly + 11], fill=fl, outline=c, width=3)
    txt(xx + 40, ly, a_, f9, INK, "lm")
    xx += 40 + d.textlength(a_, font=f9) + 50
txt(W_PX - 150, ly + 34, "HAT %s × %s × 830 · 5 modül · pide 4 çekmece (80) · lahmacun 6 (200) · içecek 2 dar çekmece (70) · şarjör 280 blank · soğutma grubu PRESS altında · hat panosu TOPPING altında" % (sayi(HAT), sayi(H)), f9, GRAY, "rm")

assert not os.path.exists(OUT), "moduler v5 zaten var — yeni numara ver"
im.save(OUT)
print("yazildi:", OUT, "· hat", HAT, "· yukseklik", H)
