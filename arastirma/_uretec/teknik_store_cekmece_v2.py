# -*- coding: utf-8 -*-
"""AUTOKITCH - STORE CEKMECE SISTEMI v2 (14 Eyl 2026): ON GORUNUS (hat alti 6 kolon) + YAN KESIT (acik cekmece, robot ustten) + UST GORUNUS (tepsiler).
Kemal: "cekmece sistemini gelistir, ayni alanda daha cok urun; kurallari bozma: robot hamuru USTTEN alir, hamurun etrafinda robot eli icin alan".
KORUNAN KURALLAR (proje kayitlari):
  - her cekmece ayri, motorlu teleskopik ray, 700 acilir; robot cekmeceyi cekmez, ustten alir; ustteki cekmeceler kapali kalir
  - conta icin acikliklar arasi ALIN 33 zorunlu (STORE v2, M15-M16); tek buyuk kapi / gruplu kapak reddedilmisti
  - topun ETRAFINDA parmak hendegi: pide O95 top, top-top arasi 35 (her yanda 17,5) · lahmacun O75 top, O98 cukur, adim 105 (arasi 30)
  - icecek dik kutu O66x115, kanal 82, on sirada 40 arka parmak payi; 830 hatta 56 kutu/cekmece (STORE v4)
  - tam 3 gun: pide 240 · lahmacun 600 · icecek 210 · 2 gunluk dolu yedek hazne seti (3 raf)
YENI (ayni alan, daha cok urun):
  1) cekmece ic yuksekligi urune gore: tepsi 30 (cukur 18) yerine 12 mm tepsi (1,5 sac + 10,5 silikon, cukur 8)
     pide: 4 + 59,5 top + 10 pay = ic 75 -> adim 108 (eski 88 + 33 = 121)
     lahmacun: 4 + 45 top + 10 pay = ic 60 -> adim 93 (eski 121)   [VARSAYIM: lahmacun topu yuksekligi 45, olculecek]
  2) lahmacun tepsisi kaydirmali (petek) dizilim, 590 x 655: 7 sira x 5 = 35 (eski GN 2/1 5 x 6 = 30); halka O105 her yonde ayni -> el payi degismedi
  3) pide dizilimi ayni (4 x 5 = 20): O130 halka ile petek 590 x 655'e ek sira sigmiyor
HESAP (kullanilir yukseklik 120..1005 = 885): pide 12 x 108 + lahmacun 18 x 93 + icecek 4 x 165 + raf 3 x 418 = 4884 -> 6 kolon.
  eski adimlarla 32 x 121 + 4 x 165 + 3 x 418 = 5786 -> 7 kolon (optimum v3'te adim 111 cizilmisti, alin kurali bozuluyordu).
Kural: paftada yalniz gorunus + olcu + parca adi; aciklama mesajda.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE\STORE_CEKMECE_v2_teknik.png".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX = 3800, 2600
BG, INK, GRAY, LINE = (255, 255, 255), (26, 26, 28), (132, 132, 140), (72, 72, 78)
FILL, ACC, RED, SOFT = (244, 244, 246), (0, 86, 184), (198, 42, 32), (228, 228, 234)
DOLAP, BOSL, PUC, TOPC, TOPK = (14, 120, 90), (190, 190, 196), (255, 240, 200), (238, 214, 168), (190, 150, 80)
SIL, KUTU = (214, 226, 236), (205, 60, 50)


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


def dline(p0, p1, c, w=1, dash=6, gap=4):
    (ax, ay), (bx, by) = p0, p1
    L = math.hypot(bx - ax, by - ay)
    if L < 1:
        return
    for i in range(int(L // (dash + gap)) + 1):
        t0, t1 = min(1.0, i * (dash + gap) / L), min(1.0, (i * (dash + gap) + dash) / L)
        d.line([(ax + (bx - ax) * t0, ay + (by - ay) * t0), (ax + (bx - ax) * t1, ay + (by - ay) * t1)], fill=c, width=w)


def dcirc(cx, cy, r, c, w=1, n=28):
    p = [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n + 1)]
    for i in range(0, n, 2):
        d.line([p[i], p[i + 1]], fill=c, width=w)


# ======================= VERI =======================
ALIN = 33.0
IC = {"pide": 75.0, "lahm": 60.0, "icecek": 132.0, "raf": 385.0}
ESKI_IC = {"pide": 88.0, "lahm": 88.0, "icecek": 132.0}
ADIM = {k: v + ALIN for k, v in IC.items()}                     # pide 108 · lahm 93 · icecek 165 · raf 418
ADET = {"pide": 20, "lahm": 35, "icecek": 56}
AD = {"pide": "TAZE PİDE", "lahm": "LAHMACUN", "icecek": "İÇECEK"}
BR = {"pide": "top", "lahm": "top", "icecek": "kutu"}
Y0, TOP, WO, BOL, XI = 120.0, 1005.0, 620.0, 35.0, 35.0
KOLON = [[("raf", "raf 1 · HARÇ ×4"), ("raf", "raf 2 · KIYMA ×2 + KAŞAR")],
         [("raf", "raf 3 · KAŞAR + KUŞ. ×4 + SUC. ×2"), (5, "lahm")],
         [(8, "pide")],
         [(4, "pide"), (4, "lahm")],
         [(9, "lahm")],
         [(4, "icecek")]]
say = {"pide": 0, "lahm": 0, "icecek": 0}
for kol in KOLON:
    yy = Y0
    for it in kol:
        yy += ADIM["raf"] if it[0] == "raf" else it[0] * ADIM[it[1]]
        if it[0] != "raf":
            say[it[1]] += it[0]
    assert yy <= TOP + 0.5, ("kolon tasiyor", yy)
assert say["pide"] * 20 >= 240 and say["lahm"] * 35 >= 600 and say["icecek"] * 56 >= 210, say
ihtiyac = say["pide"] * ADIM["pide"] + say["lahm"] * ADIM["lahm"] + say["icecek"] * ADIM["icecek"] + 3 * ADIM["raf"]
eski = (say["pide"] + 20) * 121.0 + say["icecek"] * 165.0 + 3 * 418.0
print("yeni yigin %.0f (%.2f kolon) · eski %.0f (%.2f kolon)" % (ihtiyac, ihtiyac / 885, eski, eski / 885), say)

# ======================= BASLIK =======================
txt(170, 60, "AUTOKITCH  ·  STORE  ·  ÇEKMECE SİSTEMİ  v2", f38, INK)
txt(170, 128, "ön görünüş (hat altı 6 kolon) + yan kesit (açık çekmece, robot üstten alır) + üst görünüş (tepsiler)  ·  çekmece alın 33 (conta)  ·  ölçüler mm  ·  14 Eylül 2026", f13, GRAY)
d.line([(170, 170), (W_PX - 120, 170)], fill=LINE, width=3)

# ======================= 1) ON GORUNUS =======================
S1, OX1, FY1 = 0.60, 250.0, 1040.0
fx1 = lambda x: OX1 + x * S1
fy1 = lambda y: FY1 - y * S1
L1 = XI + len(KOLON) * WO + (len(KOLON) - 1) * BOL
txt(OX1, fy1(1105) - 60, "ÖN GÖRÜNÜŞ  ·  hat altı STORE", f16, ACC)
d.rectangle([fx1(0), fy1(1105), fx1(L1 + 35), fy1(1065)], fill=SOFT, outline=LINE, width=1)
txt(fx1((L1 + 35) / 2), fy1(1085), "hat üstü istasyonların alt yüzü 1065–1105", f7, GRAY, "mm")
d.rectangle([fx1(0), fy1(80), fx1(L1 + 35), fy1(0)], fill=SOFT, outline=LINE, width=2)
cx = XI
for ki, kol in enumerate(KOLON):
    if ki:
        d.rectangle([fx1(cx - BOL), fy1(TOP), fx1(cx), fy1(Y0)], fill=SOFT, outline=LINE, width=1)
    d.rectangle([fx1(cx), fy1(TOP + 60), fx1(cx + WO), fy1(TOP)], fill=PUC, outline=GRAY, width=1)
    y = Y0
    for it in kol:
        if it[0] == "raf":
            h = ADIM["raf"]
            d.rectangle([fx1(cx + 6), fy1(y + h - 3), fx1(cx + WO - 6), fy1(y)], fill=BG, outline=INK, width=2)
            txt(fx1(cx + WO / 2), fy1(y + h / 2) - 13, "YEDEK HAZNE RAFI · kızaklı", f8, INK, "mm")
            txt(fx1(cx + WO / 2), fy1(y + h / 2) + 13, it[1], f7, GRAY, "mm")
            y += h
            continue
        n, tip = it
        h = ADIM[tip]
        ybas = y
        for _ in range(n):
            d.rectangle([fx1(cx + 6), fy1(y + h - 3), fx1(cx + WO - 6), fy1(y)], fill=BG, outline=DOLAP, width=1)
            y += h
        ym = (fy1(ybas) + fy1(y)) / 2
        for k_, (ss, ff, cc) in enumerate((("%s × %d" % (AD[tip], n), f8, INK), ("%d %s/çekmece · adım %s" % (ADET[tip], BR[tip], sayi(h)), f7, DOLAP))):
            tw = d.textlength(ss, font=ff)
            ty = ym + (-12 if k_ == 0 else 12)
            d.rectangle([fx1(cx + WO / 2) - tw / 2 - 5, ty - 11, fx1(cx + WO / 2) + tw / 2 + 5, ty + 11], fill=BG, outline=DOLAP, width=1)
            txt(fx1(cx + WO / 2), ty, ss, ff, cc, "mm")
    if TOP - y > 20:
        d.rectangle([fx1(cx + 6), fy1(TOP), fx1(cx + WO - 6), fy1(y)], fill=(250, 250, 251), outline=BOSL, width=1)
        tarali(fx1(cx + 6) + 1, fy1(TOP) + 1, fx1(cx + WO - 6) - 1, fy1(y) - 1)
        txt(fx1(cx + WO / 2), (fy1(TOP) + fy1(y)) / 2, "boş %s" % sayi(TOP - y), f7, GRAY, "mm")
    txt(fx1(cx + WO / 2), fy1(Y0) + 12, "K%d · üst %s" % (ki + 1, sayi(y)), f7, GRAY, "mm")
    cx += WO + BOL
olcu_h(fx1(XI), fx1(XI + WO), fy1(0) + 34, "620", f8, GRAY)
olcu_h(fx1(0), fx1(L1), fy1(0) + 70, "STORE  %s  ·  6 kolon  ·  kullanılır yükseklik 120–1005 = 885" % sayi(L1), f11, INK)
olcu_v(fx1(0) - 30, fy1(TOP), fy1(Y0), "885", f9, INK, "l")
for yy_, s_ in ((0, "0"), (80, "80"), (Y0, "120"), (TOP, "1005"), (TOP + 60, "1065")):
    d.line([(fx1(L1 + 35) + 6, fy1(yy_)), (fx1(L1 + 35) + 22, fy1(yy_))], fill=INK, width=2)
    txt(fx1(L1 + 35) + 28, fy1(yy_), s_, f7, INK, "lm")

# ======================= 2) YAN KESIT =======================
S2, OX2, BY2 = 1.0, 170.0, 2130.0
fz = lambda z: OX2 + (z + 830.0) * S2
fy2 = lambda y: BY2 - (y - Y0) * S2
P = ADIM["pide"]
txt(OX2, fy2(Y0 + 3 * P + 470) - 10, "YAN KESİT  ·  pide çekmecesi açık, üstteki kapalı  ·  robot üstten alır", f16, ACC)
# kasa: arka PU, plenum, on yuz cizgisi
d.rectangle([fz(-830), fy2(Y0 + 3 * P), fz(-770), fy2(Y0 - 40)], fill=PUC, outline=GRAY, width=1)
tarali(fz(-830) + 1, fy2(Y0 + 3 * P) + 1, fz(-770) - 1, fy2(Y0 - 40) - 1, (225, 205, 160), 9)
txt(fz(-800), fy2(Y0 - 40) + 18, "PU 60", f7, GRAY, "mm")
d.rectangle([fz(-770), fy2(Y0 + 3 * P), fz(-722), fy2(Y0 - 40)], fill=(250, 250, 251), outline=BOSL, width=1)
txt(fz(-746), fy2(Y0 - 40) + 42, "plenum 48", f7, GRAY, "mm")
d.line([(fz(0), fy2(Y0 + 3 * P + 20)), (fz(0), fy2(Y0 - 40))], fill=LINE, width=3)
txt(fz(0), fy2(Y0 + 3 * P + 20) - 14, "kasa ön yüzü", f7, GRAY, "mm")


def cekmece(k, acik):
    yb = Y0 + k * P
    dz = 700.0 if acik else 0.0
    kb0, kb1 = yb + 16.5, yb + 16.5 + IC["pide"]               # kutu ici
    d.rectangle([fz(-680 + dz), fy2(kb1), fz(0 + dz), fy2(kb0 - 1.5)], fill=BG, outline=DOLAP, width=2)
    d.rectangle([fz(0 + dz), fy2(yb + P - 1.5), fz(40 + dz), fy2(yb + 1.5)], fill=SOFT, outline=DOLAP, width=2)
    if not acik:
        d.rectangle([fz(-770), fy2(kb0 + 45), fz(-713), fy2(kb0 + 5)], fill=(235, 235, 240), outline=GRAY, width=1)
    # tepsi 12 + toplar
    d.rectangle([fz(-665 + dz), fy2(kb0 + 12), fz(-15 + dz), fy2(kb0)], fill=SIL, outline=ACC, width=1)
    for j in range(5):
        zc = -665 + dz + 65 + 130 * j
        d.chord([fz(zc - 47.5), fy2(kb0 + 4 + 59.5), fz(zc + 47.5), fy2(kb0 + 4 - 59.5)], 180, 360, fill=TOPC, outline=TOPK, width=2)
    return yb, kb0, kb1


for k in (2, 1):
    cekmece(k, False)
yb, kb0, kb1 = cekmece(0, True)
# alin bandi
for k in range(1, 3):
    yk = Y0 + k * P
    d.rectangle([fz(-2), fy2(yk + 16.5), fz(0), fy2(yk - 16.5)], fill=INK)
# robot eli: on siradaki top (zc = 35 + 65 + 520 = 620)
ZC = -665 + 700 + 65 + 130 * 4
ytop = kb0 + 4 + 59.5
d.rectangle([fz(ZC - 90), fy2(ytop + 330), fz(ZC + 90), fy2(ytop + 190)], fill=(236, 240, 246), outline=INK, width=2)
txt(fz(ZC), fy2(ytop + 260), "ROBOT ELİ", f8, INK, "mm")
d.rectangle([fz(ZC - 30), fy2(ytop + 470), fz(ZC + 30), fy2(ytop + 330)], fill=(210, 214, 222), outline=INK, width=1)
for sg in (-1, 1):
    zf = ZC + sg * (47.5 + 8.75)
    d.rectangle([fz(zf - 6), fy2(ytop + 190), fz(zf + 6), fy2(kb0 + 16)], fill=(150, 150, 158), outline=INK, width=1)
ok_y = fy2(ytop + 400)
d.line([(fz(ZC + 140), ok_y), (fz(ZC + 140), fy2(ytop + 210))], fill=RED, width=3)
d.polygon([(fz(ZC + 140), fy2(ytop + 200)), (fz(ZC + 132), fy2(ytop + 218)), (fz(ZC + 148), fy2(ytop + 218))], fill=RED)
txt(fz(ZC + 155), ok_y + 10, "üstten iner", f7, RED, "lm")
# olculer
olcu_h(fz(0), fz(700), fy2(Y0 - 40) + 50, "700 açılır (motorlu ray)", f8, INK)
olcu_h(fz(ZC - 130), fz(ZC), fy2(kb0) + 26, "130", f7, GRAY)
olcu_h(fz(ZC - 47.5 - 17.5), fz(ZC - 47.5), fy2(ytop + 150), "17,5", f7, RED)
txt(fz(ZC - 65), fy2(ytop + 175), "el payı", f7, RED, "mm")
xv = fz(-722) + 40
olcu_v(fz(-880), fy2(Y0 + 2 * P), fy2(Y0 + P), "adım %s" % sayi(P), f8, INK, "l")
olcu_v(fz(8), fy2(Y0 + 16.5 + IC["pide"]), fy2(Y0 + 16.5), "iç %s" % sayi(IC["pide"]), f7, INK, "l")
olcu_v(fz(60), fy2(Y0 + 2 * P + 16.5), fy2(Y0 + 2 * P - 16.5), "alın 33", f7, INK, "r")
olcu_v(fz(760), fy2(ytop), fy2(kb0 + 4), "top 59,5", f7, INK, "r")
olcu_v(fz(850), fy2(kb0 + 12), fy2(kb0), "tepsi 12", f7, ACC, "r")
txt(fz(-360), fy2(kb1) - 16, "çekmece kutusu 680 · tepsi 650 · 5 sıra × 130", f7, DOLAP, "mm")
txt(fz(-350), fy2(Y0 + 3 * P) - 14, "kapalı çekmeceler · motorlar arkada (plenum)", f7, GRAY, "mm")

# ======================= 3) UST GORUNUS: TEPSILER =======================
S3, TY3 = 0.55, 1420.0
TEPSI = [("PİDE · YENİ = ESKİ", 590.0, 655.0, "pide"), ("LAHMACUN · ESKİ", 530.0, 650.0, "lahm_eski"),
         ("LAHMACUN · YENİ", 590.0, 655.0, "lahm_yeni"), ("İÇECEK", 590.0, 655.0, "icecek")]
txt(1950, TY3 - 150, "ÜST GÖRÜNÜŞ  ·  çekmece tepsileri (açık)  ·  kesik halka = robot eli payı", f16, ACC)
tx = 1950.0
for ad_, tw_, td_, tip in TEPSI:
    px = lambda x: tx + x * S3
    pz = lambda z: TY3 + z * S3
    d.rectangle([px(0), pz(0), px(tw_), pz(td_)], fill=SIL if tip != "icecek" else BG, outline=ACC if tip != "icecek" else DOLAP, width=2)
    n = 0
    if tip == "pide":
        for j in range(4):
            for k in range(5):
                x_, z_ = 100 + 130 * j, 65 + 130 * k
                dcirc(px(x_), pz(z_), 65 * S3, RED, 1)
                d.ellipse([px(x_ - 47.5), pz(z_ - 47.5), px(x_ + 47.5), pz(z_ + 47.5)], fill=TOPC, outline=TOPK, width=1)
                n += 1
        not_ = "4 × 5 · Ø95 top · halka Ø130 (arası 35)"
    elif tip == "lahm_eski":
        for j in range(5):
            for k in range(6):
                x_, z_ = 52.5 + 105 * j, 52.5 + 105 * k
                dcirc(px(x_), pz(z_), 52.5 * S3, RED, 1)
                d.ellipse([px(x_ - 37.5), pz(z_ - 37.5), px(x_ + 37.5), pz(z_ + 37.5)], fill=TOPC, outline=TOPK, width=1)
                n += 1
        not_ = "GN 2/1 · 5 × 6 · Ø75 top · halka Ø105"
    elif tip == "lahm_yeni":
        for k in range(7):
            for j in range(5):
                x_ = (52.5 if k % 2 == 0 else 105.0) + 105 * j
                z_ = 52.5 + 90.93 * k
                dcirc(px(x_), pz(z_), 52.5 * S3, RED, 1)
                d.ellipse([px(x_ - 37.5), pz(z_ - 37.5), px(x_ + 37.5), pz(z_ + 37.5)], fill=TOPC, outline=TOPK, width=1)
                n += 1
        not_ = "petek 7 sıra × 5 · halka Ø105 aynı"
    else:
        for c in range(7):
            x0_ = 8 + 82 * c
            if c:
                d.line([(px(x0_), pz(10)), (px(x0_), pz(td_ - 10))], fill=DOLAP, width=1)
            for k in range(8):
                z_ = td_ - 40 - 33 - 67 * k
                d.ellipse([px(x0_ + 41 - 33), pz(z_ - 33), px(x0_ + 41 + 33), pz(z_ + 33)], fill=(250, 226, 222), outline=KUTU, width=1)
                n += 1
        d.rectangle([px(8), pz(td_ - 40), px(8 + 574), pz(td_ - 8)], outline=RED, width=1)
        txt(px(tw_ / 2), pz(td_ - 24), "ön 40 · arka parmak payı", f7, RED, "mm")
        not_ = "7 kanal × 8 · dik kutu Ø66 · kanal 82"
    txt(px(tw_ / 2), pz(0) - 58, ad_, f9, INK, "mm")
    txt(px(tw_ / 2), pz(0) - 32, "%d %s / çekmece" % (n, "kutu" if tip == "icecek" else "top"), f11, RED if tip in ("lahm_yeni",) else INK, "mm")
    olcu_h(px(0), px(tw_), pz(td_) + 26, sayi(tw_), f7, GRAY)
    olcu_v(px(tw_) + 16, pz(0), pz(td_), sayi(td_), f7, GRAY, "r")
    txt(px(tw_ / 2), pz(td_) + 62, not_, f7, GRAY, "mm")
    tx += tw_ * S3 + 110
txt(1950, TY3 + 655 * S3 + 110, "ÖN (robot tarafı) altta", f7, GRAY, "la")

# ======================= LEJANT =======================
ly = H_PX - 70
d.line([(170, ly - 45), (W_PX - 120, ly - 45)], fill=LINE, width=2)
xx = 170
for kind, a_ in (("top", "hamur topu"), ("halka", "robot eli payı (kesik halka)"), ("tepsi", "silikon tepsi 12"), ("cek", "çekmece ön yüzü · alın 33"),
                 ("raf", "yedek hazne rafı (eleman çeker)"), ("bos", "boş"), ("pu", "PU yalıtım")):
    if kind == "top":
        d.ellipse([xx, ly - 12, xx + 24, ly + 12], fill=TOPC, outline=TOPK, width=2)
    elif kind == "halka":
        dcirc(xx + 12, ly, 13, RED, 2)
    elif kind == "tepsi":
        d.rectangle([xx, ly - 10, xx + 30, ly + 10], fill=SIL, outline=ACC, width=2)
    elif kind == "cek":
        d.rectangle([xx, ly - 10, xx + 30, ly + 10], fill=BG, outline=DOLAP, width=2)
    elif kind == "raf":
        d.rectangle([xx, ly - 10, xx + 30, ly + 10], fill=BG, outline=INK, width=2)
    elif kind == "bos":
        d.rectangle([xx, ly - 10, xx + 30, ly + 10], fill=(250, 250, 251), outline=BOSL, width=2)
    else:
        d.rectangle([xx, ly - 10, xx + 30, ly + 10], fill=PUC, outline=GRAY, width=2)
    txt(xx + 42, ly, a_, f9, INK, "lm")
    xx += 42 + d.textlength(a_, font=f9) + 60
txt(W_PX - 120, ly + 36, "STORE 6 kolon · pide %d çekmece (240) · lahmacun %d (600) · içecek %d (210) · yedek hazne rafı 3 · adım: pide 108 · lahmacun 93 · içecek 165 · raf 418" % (say["pide"], say["lahm"], say["icecek"]), f9, GRAY, "rm")

assert not os.path.exists(OUT), "cekmece v2 zaten var — yeni numara ver"
im.save(OUT)
print("yazildi:", OUT)
