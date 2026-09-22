# -*- coding: utf-8 -*-
"""AUTOKITCH - HAT v9 (ilk cizime sadik: cekmeceler istasyon altlarinda, onde YER RAYI + TEK ROBOT) (16 Eyl 2026): iki robot, bant yok, 3 gozlu kaviteli firin (2 lahmacun alt alta + 1 pide).
2 gunluk ritim: 20 hamur cekmecesi (560 top), 6 standart kaset + kasar kabi + sucuk cubuk dilimleyici,
3 icecek + 1 tatli cekmecesi, 12 gozlu QR dolabi (2 sutun x 6 sira).
Robotlar FR5 WML (1.900 mm), govdeye 1.400 kotunda bagli, ray yok.
Kural: paftada yalniz gorunus + olcu + parca adi; aciklama mesajda. Olculer mm.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE\HAT_ROBOT_v9_teknik.png".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX = 5200, 2960
BG, INK, GRAY, LINE = (255, 255, 255), (26, 26, 28), (132, 132, 140), (72, 72, 78)
FILL, ACC, RED, SOFT = (246, 246, 248), (0, 86, 184), (198, 42, 32), (228, 228, 234)
DOLAP, SOGUK, HAVA, ERIS = (14, 120, 90), (226, 238, 252), (255, 225, 200), (205, 218, 236)
QRC, ICE, KASET = (240, 214, 170), (214, 226, 244), (250, 236, 210)


def F(sz, b=False):
    for n in (("arialbd.ttf", "segoeuib.ttf") if b else ("arial.ttf", "segoeui.ttf")):
        try:
            return ImageFont.truetype(n, sz)
        except Exception:
            pass
    return ImageFont.load_default()


f7, f8, f9, f11, f13, f16, f20, f34 = F(15), F(17), F(19), F(22), F(25), F(29, True), F(34, True), F(50, True)
im = Image.new("RGB", (W_PX, H_PX), BG)
d = ImageDraw.Draw(im)


def txt(x, y, s, f=f11, c=INK, a="la"):
    d.text((x, y), s, font=f, fill=c, anchor=a)


def sayi(v):
    return ("%g" % v).replace(".", ",")


def dline(p0, p1, c, w=1, dash=9, gap=6):
    (ax, ay), (bx, by) = p0, p1
    L = math.hypot(bx - ax, by - ay)
    if L < 1:
        return
    for i in range(int(L // (dash + gap)) + 1):
        t0, t1 = min(1.0, i * (dash + gap) / L), min(1.0, (i * (dash + gap) + dash) / L)
        d.line([(ax + (bx - ax) * t0, ay + (by - ay) * t0), (ax + (bx - ax) * t1, ay + (by - ay) * t1)], fill=c, width=w)


def dcircle(cx, cy, r, c, w=2, step=5):
    p = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in range(0, 361, step)]
    for i in range(0, len(p) - 1, 2):
        d.line([p[i], p[i + 1]], fill=c, width=w)


def ok(x0, y0, x1, y1, c, w=3):
    d.line([(x0, y0), (x1, y1)], fill=c, width=w)
    a = math.atan2(y1 - y0, x1 - x0)
    for s_ in (-0.5, 0.5):
        d.line([(x1, y1), (x1 - 16 * math.cos(a + s_), y1 - 16 * math.sin(a + s_))], fill=c, width=w)


def olcu_h(x0, x1, y, s, f=f9, c=INK):
    d.line([(x0, y), (x1, y)], fill=c, width=2)
    for xx in (x0, x1):
        d.line([(xx, y - 8), (xx, y + 8)], fill=c, width=2)
    tw = d.textlength(s, font=f)
    d.rectangle([(x0 + x1) / 2 - tw / 2 - 6, y - 13, (x0 + x1) / 2 + tw / 2 + 6, y + 13], fill=BG)
    txt((x0 + x1) / 2, y, s, f, c, "mm")


def olcu_v(x, y0, y1, s, f=f9, c=INK, yon="r"):
    d.line([(x, y0), (x, y1)], fill=c, width=2)
    for yy in (y0, y1):
        d.line([(x - 8, yy), (x + 8, yy)], fill=c, width=2)
    txt(x + (12 if yon == "r" else -12), (y0 + y1) / 2, s, f, c, "lm" if yon == "r" else "rm")


# ======================= VERI (mm) =======================
H_MAK, DER, HB = 1915.0, 830.0, 1245.0
BANT0, BANT1 = 600.0, 1700.0
MOD = [("STORE", 655.0), ("PRESS", 670.0), ("TOPPING", 900.0), ("FIRIN", 1200.0),
       ("KESME", 500.0), ("PACK", 700.0), ("QR DOLABI", 860.0)]
X0, _x = {}, 0.0
for ad, w in MOD:
    X0[ad] = _x
    _x += w
HAT = _x                                   # 6070
W = dict(MOD)
RAY0, RAY1 = 250.0, 5235.0                 # ray strok araligi
R1X, R2X = 1600.0, 4200.0                  # arabanin gosterildigi yer / 2. robot yeri
OMUZ = 1400.0
ERISIM = 1900.0

SA = 0.60   # on gorunus olcegi
SU = 0.45   # ust gorunus olcegi


def on_gorunus(OX, ZY, S):
    def px(x):
        return OX + x * S

    def pz(z):
        return ZY - z * S

    d.rectangle([px(0), pz(H_MAK), px(HAT), pz(0)], fill=FILL, outline=LINE, width=2)
    for ad, w in MOD:
        x0 = X0[ad]
        d.line([(px(x0 + w), pz(H_MAK)), (px(x0 + w), pz(0))], fill=LINE, width=2)
        txt(px(x0 + w / 2), pz(250.0), ad, f11, INK, "mm")
        olcu_h(px(x0), px(x0 + w), pz(0) + 44, sayi(w))
    d.line([(px(0) - 70, pz(0)), (px(HAT) + 70, pz(0))], fill=INK, width=3)
    txt(px(0) - 70, pz(0) + 16, "zemin", f8, GRAY, "la")

    # --- STORE: 2 kolon hamur
    kol = [(20.0, 635.0, [(8, 108.0, "PİDE ×8"), (8, 93.0, "LAHMACUN ×8")]),
           (X0["PRESS"] + 40, X0["PRESS"] + W["PRESS"] - 40, [(4, 93.0, "LAHMACUN ×4")])]
    for x0, x1, gruplar in kol:
        z = 120.0 if x0 > 700 else BANT0
        for n, h, ad in gruplar:
            z_bas = z
            for k in range(n):
                d.rectangle([px(x0), pz(z + h), px(x1), pz(z)], fill=SOGUK, outline=DOLAP, width=1)
                z += h
            txt(px((x0 + x1) / 2), (pz(z_bas) + pz(z)) / 2, ad, f8, DOLAP, "mm")

    # --- PRESS
    p0 = X0["PRESS"]
    d.rectangle([px(p0 + 40), pz(1560.0), px(p0 + W["PRESS"] - 40), pz(620.0)], fill=SOFT, outline=GRAY, width=1)
    d.line([(px(p0 + 40), pz(HB)), (px(p0 + W["PRESS"] - 40), pz(HB))], fill=RED, width=3)
    txt(px(p0 + W["PRESS"] / 2), pz(HB) + 26, "PRES TABLASI 1245", f8, RED, "mm")

    # --- TOPPING: on sira 4 harc + kiyma · arka sira (kesik) kusbasi + kasar + sucuk
    t0 = X0["TOPPING"]
    z0, zh = 1150.0, 360.0
    x = t0 + 40
    for ad, w in (("HARÇ", 140.0), ("HARÇ", 140.0), ("HARÇ", 140.0), ("HARÇ", 140.0), ("KIYMA", 140.0)):
        d.rectangle([px(x), pz(z0 + zh), px(x + w - 8), pz(z0)], fill=KASET, outline=GRAY, width=1)
        txt(px(x + w / 2), pz(z0 + zh / 2), ad, f7, INK, "mm")
        x += w
    dline((px(t0 + 40), pz(z0 - 40)), (px(t0 + W["TOPPING"] - 40), pz(z0 - 40)), GRAY, 1)
    txt(px(t0 + W["TOPPING"] / 2), pz(z0 - 90), "arkada: KUŞBAŞI · KAŞAR KABI · SUCUK DİLİMLEYİCİ", f7, GRAY, "mm")
    olcu_v(px(t0 + 20), pz(z0 + zh), pz(z0), "360", yon="l")

    # --- FIRIN: lahmacun 2 goz alt alta + pide 1 goz
    f0 = X0["FIRIN"]
    d.rectangle([px(f0 + 30), pz(1560.0), px(f0 + 570), pz(500.0)], fill=HAVA, outline=LINE, width=2)
    for z in (850.0, 1200.0):
        d.rectangle([px(f0 + 70), pz(z + 150.0), px(f0 + 530), pz(z)], fill=BG, outline=RED, width=2)
        txt(px(f0 + 300), pz(z + 75.0), "LAHMACUN GÖZÜ", f8, RED, "mm")
    txt(px(f0 + 300), pz(1610.0), "2 GÖZ ALT ALTA", f8, INK, "mm")
    d.rectangle([px(f0 + 630), pz(1560.0), px(f0 + 1170), pz(500.0)], fill=HAVA, outline=LINE, width=2)
    d.rectangle([px(f0 + 670), pz(1180.0), px(f0 + 1130), pz(1030.0)], fill=BG, outline=RED, width=2)
    txt(px(f0 + 900), pz(1105.0), "PİDE GÖZÜ", f8, RED, "mm")
    txt(px(f0 + 900), pz(1610.0), "1 GÖZ", f8, INK, "mm")
    olcu_v(px(f0 + 1190), pz(1350.0), pz(1200.0), "150", yon="r")

    # --- KESME
    k0 = X0["KESME"]
    d.line([(px(k0 + 60), pz(HB)), (px(k0 + W["KESME"] - 60), pz(HB))], fill=RED, width=3)
    txt(px(k0 + W["KESME"] / 2), pz(HB) + 26, "KESME + SPREY", f8, RED, "mm")

    # --- PACK + icecek/tatli cekmeceleri
    pk = X0["PACK"]
    d.rectangle([px(pk + 60), pz(1600.0), px(pk + W["PACK"] - 60), pz(1300.0)], fill=SOFT, outline=GRAY, width=1)
    txt(px(pk + W["PACK"] / 2), pz(1450.0), "KUTU ŞARJÖRÜ", f8, GRAY, "mm")
    z = BANT0
    for n, h, ad in ((3, 165.0, "İÇECEK ×3"), (1, 120.0, "TATLI ×1")):
        z_bas = z
        for k in range(n):
            d.rectangle([px(pk + 40), pz(z + h), px(pk + W["PACK"] - 40), pz(z)], fill=ICE, outline=DOLAP, width=1)
            z += h
        txt(px(pk + W["PACK"] / 2), (pz(z_bas) + pz(z)) / 2, ad, f8, DOLAP, "mm")

    # --- QR dolabi 2 sutun x 6 sira
    q0 = X0["QR DOLABI"]
    gx, gz = q0 + 50, 600.0
    for r in range(6):
        for c in range(2):
            d.rectangle([px(gx + c * 380.0), pz(gz + (r + 1) * 200.0), px(gx + (c + 1) * 380.0 - 10), pz(gz + r * 200.0)],
                        fill=QRC, outline=LINE, width=1)
    txt(px(q0 + W["QR DOLABI"] / 2), pz(gz + 1250.0), "12 GÖZ · 380 × 200", f8, INK, "mm")
    olcu_v(px(q0 + W["QR DOLABI"]) + 40, pz(gz + 1200.0), pz(gz), "1200")

    # --- robotlar
    # --- YER RAYI (hattin onunde, koridorda)
    d.rectangle([px(RAY0), pz(220.0), px(RAY1), pz(120.0)], fill=ACC, outline=INK, width=2)
    txt(px((RAY0 + RAY1) / 2), pz(70.0), "YER RAYI · STROK 4985", f11, ACC, "mm")
    ok(px(R1X + 420), pz(300.0), px(RAY1 - 60), pz(300.0), INK, 3)
    ok(px(R1X - 420), pz(300.0), px(RAY0 + 60), pz(300.0), INK, 3)
    # araba + kaide + robot
    cx = R1X
    d.rectangle([px(cx - 220), pz(360.0), px(cx + 220), pz(220.0)], fill=SOFT, outline=INK, width=2)
    txt(px(cx), pz(290.0), "ARABA", f8, GRAY, "mm")
    d.rectangle([px(cx - 90), pz(OMUZ - 60), px(cx + 90), pz(360.0)], fill=SOFT, outline=INK, width=2)
    txt(px(cx) + 104, pz(800.0), "KAİDE 1040", f8, GRAY, "lm")
    d.ellipse([px(cx) - 22, pz(OMUZ) - 22, px(cx) + 22, pz(OMUZ) + 22], fill=ACC, outline=INK, width=2)
    hedef = (t0 + 250, 1400.0)
    mx = (cx + hedef[0]) / 2
    d.line([(px(cx), pz(OMUZ)), (px(mx), pz(OMUZ + 400))], fill=ACC, width=10)
    d.line([(px(mx), pz(OMUZ + 400)), (px(hedef[0]), pz(hedef[1] + 110))], fill=ACC, width=10)
    d.line([(px(hedef[0]), pz(hedef[1] + 110)), (px(hedef[0]), pz(hedef[1] + 30))], fill=ACC, width=7)
    txt(px(cx), pz(1980.0), "ROBOT · FR5 (922)", f11, ACC, "mm")
    dcircle(px(cx), pz(OMUZ), 922 * S, ERIS, 2)
    # 2. robot yeri (sonradan)
    d.rectangle([px(R2X - 220), pz(360.0), px(R2X + 220), pz(220.0)], fill=BG, outline=GRAY, width=1)
    dline((px(R2X - 90), pz(OMUZ)), (px(R2X + 90), pz(OMUZ)), GRAY, 1)
    dline((px(R2X - 90), pz(OMUZ)), (px(R2X - 90), pz(360.0)), GRAY, 1)
    dline((px(R2X + 90), pz(OMUZ)), (px(R2X + 90), pz(360.0)), GRAY, 1)
    txt(px(R2X), pz(1980.0), "2. ROBOT YERİ (sonradan)", f9, GRAY, "mm")

    dline((px(-120), pz(OMUZ)), (px(HAT + 120), pz(OMUZ)), GRAY, 1)
    olcu_v(px(0) - 90, pz(OMUZ), pz(0), "OMUZ 1400", yon="l")
    olcu_v(px(0) - 210, pz(BANT1), pz(BANT0), "ERİŞİM BANDI 1100", yon="l")
    olcu_v(px(0) - 330, pz(BANT0), pz(0), "600", yon="l")
    olcu_v(px(HAT) + 170, pz(H_MAK), pz(0), "1915")
    olcu_h(px(0), px(HAT), pz(0) + 120, "HAT %s" % sayi(HAT), f13)


def ust_gorunus(OX, OY, S):
    def px(x):
        return OX + x * S

    def py(y):
        return OY - y * S

    d.rectangle([px(0), py(DER), px(HAT), py(0)], fill=FILL, outline=LINE, width=2)
    for ad, w in MOD:
        x0 = X0[ad]
        d.line([(px(x0 + w), py(DER)), (px(x0 + w), py(0))], fill=LINE, width=1)
        txt(px(x0 + w / 2), (py(DER) + py(0)) / 2, ad, f9, INK, "mm")
    olcu_v(px(HAT) + 44, py(DER), py(0), "830")
    dline((px(0), py(-800.0)), (px(HAT), py(-800.0)), GRAY, 1)
    olcu_v(px(0) - 60, py(0), py(-800.0), "800", yon="l")
    txt(px(HAT / 2), py(-400.0), "ROBOT KORİDORU", f9, GRAY, "mm")
    d.rectangle([px(RAY0), py(-260.0), px(RAY1), py(-360.0)], fill=ACC, outline=INK, width=1)
    txt(px((RAY0 + RAY1) / 2), py(-500.0), "YER RAYI (koridorda)", f9, ACC, "mm")
    d.ellipse([px(R1X) - 18, py(-310.0) - 18, px(R1X) + 18, py(-310.0) + 18], fill=ACC, outline=INK, width=2)
    txt(px(R1X), py(-620.0), "ROBOT", f9, ACC, "mm")
    d.ellipse([px(R2X) - 16, py(-310.0) - 16, px(R2X) + 16, py(-310.0) + 16], fill=BG, outline=GRAY, width=2)
    txt(px(R2X), py(-620.0), "2. ROBOT YERİ", f9, GRAY, "mm")
    q0 = X0["QR DOLABI"]
    ok(px(q0 + W["QR DOLABI"] / 2), py(DER + 420.0), px(q0 + W["QR DOLABI"] / 2), py(DER + 80.0), INK, 3)
    txt(px(q0 + W["QR DOLABI"] / 2), py(DER + 500.0), "MÜŞTERİ", f9, INK, "mm")
    ok(px(X0["STORE"] + 500), py(-1080.0), px(X0["STORE"] + 500), py(-840.0), GRAY, 2)
    txt(px(X0["STORE"] + 500), py(-1160.0), "ELEMAN — koridordan dolum", f9, GRAY, "mm")


# ======================= SAYFA =======================
txt(210, 92, "AUTOKITCH · HAT v9 · YER RAYI + TEK ROBOT · 3 GÖZLÜ FIRIN", f34, INK)
txt(210, 152, "ön görünüş + üst görünüş  ·  bant yok  ·  2 günlük stok  ·  2. robot için yer ayrıldı  ·  ölçüler mm  ·  16 Eylül 2026", f13, GRAY)

on_gorunus(560, 1560, SA)
ust_gorunus(560, 2380, SU)

# ======================= LEJANT =======================
LX, LY = 210, 2860
for i, (fl, oc, ad) in enumerate(((SOGUK, DOLAP, "hamur çekmecesi"), (ICE, DOLAP, "içecek / tatlı çekmecesi"),
                                  (KASET, GRAY, "kaset 140 × 400 × 360"), (HAVA, LINE, "fırın gövdesi"),
                                  (QRC, LINE, "QR teslim gözü"), (SOFT, GRAY, "pres / şarjör / kaide"))):
    xx = LX + i * 620
    d.rectangle([xx, LY, xx + 42, LY + 30], fill=fl, outline=oc, width=2)
    txt(xx + 56, LY + 15, ad, f9, INK, "lm")
d.ellipse([LX + 3720, LY + 2, LX + 3752, LY + 32], fill=ACC, outline=INK, width=2)
txt(LX + 3768, LY + 16, "robot omuz noktası (FR5 · erişim 922, ray üstünde)", f9, INK, "lm")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.save(OUT)
print("OK ->", OUT, im.size, "· hat", HAT)
