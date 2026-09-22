# -*- coding: utf-8 -*-
"""PIDE & LAHMACUN MODULE - CONCEPT FRONT VIEW v2 (14 Sep 2026). Olculer mm. Ingilizce (Yindu'ya gidecek).
v1'den FARKI (Kemal): AUTOKITCH adi ve bizim sistemimiz (soguk depo, hamur cekmecesi, robot kol, kesme/kutulama) CIKARILDI;
hazne hedefleri Kemal'in krokisine gore: harc 2 gun (22 kg/gun) · kiymali 3 gun (3,2) · kusbasi 3 gun (2,9) · kasar 7 gun (2,2) · sucuk 7 gun (1,4);
"hazne sayisi artirilabilir" notu; kapsam iki secenek: A = pres + topping + firin (hepsi Yindu) · B = yalniz topping modulu.
KAYNAK: Kemal'in hazne krokisi (13 Eyl), sim_karsi (tepe 42/59 urun/saat), stok kurgusu (80 pide + 200 lahmacun, cumartesi x1,4),
yogunluklar (harc/kiyma 1,0 · kusbasi 0,58 · sucuk 0,59 · kasar 0,40), hat pafta v4 (PRESS 700 · TOPPING 1000 · OVEN 1500 · kot 1300 · firin 1000-1620 · 830 derin).
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE\ATOSA_MODUL_v2_teknik.png".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX, S = 2900, 1720, 0.5
BG, INK, GRAY, LINE = (255, 255, 255), (26, 26, 28), (120, 120, 128), (72, 72, 78)
BLUE, RED, ORG, GRN = (0, 86, 184), (198, 42, 32), (200, 90, 30), (14, 120, 90)
FILL, SOFT, EVC, PROD = (244, 244, 246), (232, 232, 236), (226, 238, 252), (240, 214, 170)


def F(sz, b=False):
    try:
        return ImageFont.truetype("arialbd.ttf" if b else "arial.ttf", sz)
    except Exception:
        return ImageFont.load_default()


f14, f16, f18, f20, f22, f26, f30, f44 = F(14), F(16), F(18), F(20), F(22), F(26, True), F(30, True), F(44, True)
fb16, fb18, fb20, fb22 = F(16, True), F(18, True), F(20, True), F(22, True)
im = Image.new("RGB", (W_PX, H_PX), BG)
d = ImageDraw.Draw(im)
OX, FLOOR = 260.0, 1290.0
fx = lambda x: OX + x * S
fy = lambda y: FLOOR - y * S


def txt(x, y, s, f=f18, c=INK, a="la"):
    d.text((x, y), s, font=f, fill=c, anchor=a)


def dline(p0, p1, c, w=2, dash=10, gap=6):
    (ax, ay), (bx, by) = p0, p1
    L = math.hypot(bx - ax, by - ay)
    for i in range(int(L // (dash + gap)) + 1):
        t0, t1 = min(1, i * (dash + gap) / L), min(1, (i * (dash + gap) + dash) / L)
        d.line([(ax + (bx - ax) * t0, ay + (by - ay) * t0), (ax + (bx - ax) * t1, ay + (by - ay) * t1)], fill=c, width=w)


def drect(x0, y0, x1, y1, c, w=2):
    for a, b in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
        dline(a, b, c, w)


def ok(x0, y0, x1, y1, c, w=4, dashed=False):
    if dashed:
        dline((x0, y0), (x1, y1), c, w)
    else:
        d.line([(x0, y0), (x1, y1)], fill=c, width=w)
    a = math.atan2(y1 - y0, x1 - x0)
    d.polygon([(x1, y1), (x1 - 18 * math.cos(a - 0.4), y1 - 18 * math.sin(a - 0.4)), (x1 - 18 * math.cos(a + 0.4), y1 - 18 * math.sin(a + 0.4))], fill=c)


def adim(x, y, n, c=RED):
    d.ellipse([x - 17, y - 17, x + 17, y + 17], fill=c)
    txt(x, y, str(n), fb20, BG, "mm")


def olcu_h(x0, x1, y, s, f=f18, c=INK):
    d.line([(x0, y), (x1, y)], fill=c, width=2)
    for xx in (x0, x1):
        d.line([(xx, y - 8), (xx, y + 8)], fill=c, width=2)
    tw = d.textlength(s, font=f)
    d.rectangle([(x0 + x1) / 2 - tw / 2 - 6, y - 12, (x0 + x1) / 2 + tw / 2 + 6, y + 12], fill=BG)
    txt((x0 + x1) / 2, y, s, f, c, "mm")


def olcu_v(x, y0, y1, s, f=f18, c=INK):
    d.line([(x, y0), (x, y1)], fill=c, width=2)
    for yy in (y0, y1):
        d.line([(x - 8, yy), (x + 8, yy)], fill=c, width=2)
    txt(x - 12, (y0 + y1) / 2, s, f, c, "rm")


def tarali(x0, y0, x1, y1, c=(215, 215, 222), ad=16):
    w, h = x1 - x0, y1 - y0
    for k in range(0, int(w + h), ad):
        ax, ay, bx, by = x0 + k, y1, x0 + k - h, y0
        if ax > x1:
            ay, ax = y1 - (ax - x1), x1
        if bx < x0:
            by, bx = y1 - k, x0
        if ay >= y0:
            d.line([(ax, ay), (bx, by)], fill=c, width=1)


def urun(xc, yb, c=PROD):
    d.ellipse([fx(xc - 150), fy(yb + 22), fx(xc + 150), fy(yb)], fill=c, outline=(190, 150, 80), width=2)


def tabla(xc, yb, dashed=False):
    if dashed:
        drect(fx(xc - 170), fy(yb + 20), fx(xc + 170), fy(yb), BLUE, 2)
    else:
        d.rectangle([fx(xc - 170), fy(yb + 20), fx(xc + 170), fy(yb)], fill=(214, 226, 244), outline=BLUE, width=3)


# ---------------- HAZNE HEDEFI (normal gun: 80 pide + 200 lahmacun) ----------------
HEDEF = [("Lahmacun paste", "raw minced meat + onion, tomato, pepper, parsley, spices", 22.0, 2, 1.00),
         ("Minced-meat pide filling", "moist minced meat mix", 3.2, 3, 1.00),
         ("Diced meat (kuşbaşı)", "small meat cubes", 2.9, 3, 0.58),
         ("Grated kaşar cheese", "Turkish semi-hard cheese", 2.2, 7, 0.40),
         ("Sucuk (sliced)", "Turkish dry beef sausage", 1.4, 7, 0.59)]
for ad_, _, kg, gun, rho in HEDEF:
    print("%-26s %4.1f kg/day x %d days = %5.1f kg  ~%5.1f L" % (ad_, kg, gun, kg * gun, kg * gun / rho))

# ---------------- BASLIK ----------------
txt(110, 28, "PIDE & LAHMACUN MODULE  ·  CONCEPT FRONT VIEW  v2", f44, INK)
txt(110, 90, "press  →  customized topping module (based on Auto Pizza Artisan)  →  customized conveyor oven  ·  dimensions in mm  ·  14 Sep 2026", f22, GRAY)
d.line([(110, 128), (W_PX - 60, 128)], fill=LINE, width=3)

# ---------------- ALT KISIM (kapsam disi) ----------------
d.rectangle([fx(0), fy(120), fx(3200), fy(0)], fill=SOFT, outline=LINE, width=2)
d.rectangle([fx(0), fy(980), fx(3200), fy(120)], fill=(250, 250, 251), outline=GRAY, width=2)
tarali(fx(0) + 1, fy(980) + 1, fx(3200) - 1, fy(120) - 1)
txt(fx(1600), fy(560), "LOWER PART: FREE SPACE  ·  not in scope", f22, GRAY, "mm")

# ---------------- PRES ----------------
d.rectangle([fx(0), fy(1970), fx(700), fy(980)], fill=FILL, outline=LINE, width=3)
d.rectangle([fx(110), fy(1920), fx(590), fy(1600)], fill=BG, outline=INK, width=2)
txt(fx(350), fy(1800), "PRESS HEAD", fb18, INK, "mm")
txt(fx(350), fy(1745), "option A: by Yindu", f16, BLUE, "mm")
txt(fx(350), fy(1705), "option B: by customer", f16, RED, "mm")
d.rectangle([fx(335), fy(1600), fx(365), fy(1350)], fill=(160, 160, 168))
d.rectangle([fx(160), fy(1350), fx(540), fy(1320)], fill=(120, 120, 128))
txt(fx(150), fy(1335), "platen", f14, GRAY, "rm")
d.rectangle([fx(200), fy(1265), fx(500), fy(1150)], fill=(150, 150, 158), outline=INK, width=2)
txt(fx(350), fy(1207), "FIXED ANVIL", fb18, BG, "mm")
tabla(350, 1265)
urun(350, 1285, (233, 217, 168))

# ---------------- TOPPING MODULU ----------------
d.rectangle([fx(700), fy(1970), fx(1700), fy(980)], fill=FILL, outline=LINE, width=3)
d.rectangle([fx(710), fy(1960), fx(1690), fy(1450)], fill=EVC, outline=BLUE, width=2)
txt(fx(1200), fy(1935), "REFRIGERATED HOPPERS +3 °C · slide in from front", f16, BLUE, "mm")
HOP = [("LAHMACUN", "PASTE", "44 kg", "2 days", 240), ("MINCED", "MEAT", "9.6 kg", "3 days", 175), ("DICED", "MEAT", "8.7 kg", "3 days", 175),
       ("KAŞAR", "CHEESE", "15.4 kg", "7 days", 190), ("SUCUK", "SLICED", "9.8 kg", "7 days", 170)]
x = 710.0
CX = []
for a1, a2, kg, gun, w in HOP:
    d.rectangle([fx(x), fy(1880), fx(x + w), fy(1480)], fill=BG, outline=INK, width=2)
    txt(fx(x + w / 2), fy(1780), a1, fb16, INK, "mm")
    txt(fx(x + w / 2), fy(1735), a2, fb16, INK, "mm")
    txt(fx(x + w / 2), fy(1640), kg, fb18, RED, "mm")
    txt(fx(x + w / 2), fy(1590), gun, f14, GRAY, "mm")
    d.rectangle([fx(x + w / 2 - 25), fy(1480), fx(x + w / 2 + 25), fy(1450)], fill=RED)
    CX.append(x + w / 2)
    x += w + 7.5
txt(fx(1200), fy(1530) , "", f14, GRAY, "mm")
d.rectangle([fx(150), fy(1190), fx(1660), fy(1170)], fill=BLUE)
txt(fx(1180), fy(1150), "tray carriage rail (extends under the press)  ·  drip tray below", f16, BLUE, "mm")
tabla(CX[0], 1390)
urun(CX[0], 1410)
d.rectangle([fx(CX[0] - 12), fy(1390), fx(CX[0] + 12), fy(1190)], fill=(150, 150, 158))
d.arc([fx(CX[0] - 190), fy(1470), fx(CX[0] + 190), fy(1360)], 200, 340, fill=RED, width=4)
ok(fx(CX[0] + 150), fy(1450), fx(CX[0] + 185), fy(1418), RED, 4)
txt(fx(CX[0] - 200), fy(1455), "rotate + slide", f14, RED, "rm")
txt(fx(CX[0] + 22), fy(1268), "lift · load cell", f14, GRAY, "lm")
tabla(1470, 1265, True)
urun(1470, 1285)
d.rectangle([fx(1285), fy(1360), fx(1300), fy(1285)], fill=(255, 190, 0), outline=INK, width=1)
txt(fx(1292), fy(1385), "pusher", f14, INK, "mm")

# ---------------- FIRIN ----------------
d.rectangle([fx(1700), fy(1970), fx(3200), fy(980)], fill=FILL, outline=LINE, width=3)
d.rectangle([fx(1700), fy(1620), fx(3200), fy(1000)], fill=(255, 246, 236), outline=ORG, width=4)
drect(fx(1750), fy(1560), fx(3150), fy(1060), ORG, 2)
d.line([(fx(1640), fy(1285)), (fx(3260), fy(1285))], fill=ORG, width=5)
for xc in (1925, 2275, 2625, 2975):
    urun(xc, 1285, (215, 150, 80))
txt(fx(2450), fy(1520), "CONVEYOR OVEN (customized)  ·  electric  ·  4 products in chamber", fb20, ORG, "mm")
txt(fx(2450), fy(1470), "pide 240 s  ·  lahmacun 180 s  ·  ≥ 60 products / hour", f18, ORG, "mm")
txt(fx(2450), fy(1110), "baking chamber ≈ 1400  ·  belt ≤ 450 wide  ·  depth ≤ 830", f16, ORG, "mm")
d.rectangle([fx(1730), fy(1960), fx(3170), fy(1660)], fill=BG, outline=LINE, width=2)
txt(fx(2450), fy(1810), "EXHAUST HOOD · FAN · GREASE + CARBON FILTER", f18, GRAY, "mm")
ok(fx(3200), fy(1285), fx(3400), fy(1285), INK, 4)
txt(fx(3215), fy(1240), "exit", f16, INK, "la")

# ---------------- AKIS OKLARI ----------------
adim(fx(620), fy(1250), 1, GRN)
adim(fx(620), fy(1790), 2)
ok(fx(530), fy(1300), fx(CX[0] - 180), fy(1395), RED, 4)
adim(fx(CX[0] - 210), fy(1540), 3)
ok(fx(CX[0] + 180), fy(1390), fx(1300), fy(1300), RED, 4)
adim(fx(1370), fy(1420), 4)
ok(fx(1300), fy(1320), fx(1690), fy(1320), ORG, 4)
ok(fx(1300), fy(1212), fx(560), fy(1212), BLUE, 3, True)
adim(fx(1180), fy(1212), 5, BLUE)
adim(fx(1800), fy(1430), 6, ORG)
adim(fx(3300), fy(1340), 7, INK)

# ---------------- KAPSAM (A / B) + OLCULER ----------------
drect(fx(0) - 14, fy(1970) - 14, fx(3200) + 14, fy(980) + 14, BLUE, 4)
d.rectangle([fx(700) - 6, fy(1970) - 6, fx(1700) + 6, fy(980) + 6], outline=RED, width=5)
top = fy(1970)
olcu_h(fx(0), fx(700), top - 104, "700", f18)
olcu_h(fx(700), fx(1700), top - 104, "1000", f18)
olcu_h(fx(1700), fx(3200), top - 104, "1500", f18)
txt(fx(0), top - 66, "OPTION A (preferred): complete module  ·  press + topping + conveyor oven", fb20, BLUE, "lm")
txt(fx(1200), top - 32, "OPTION B: topping module only", fb20, RED, "mm")
olcu_h(fx(0), fx(3200), fy(0) + 40, "3200  ·  depth 830 for all modules", f20)
olcu_v(fx(0) - 190, fy(1970), fy(0), "1970", f18)
for yy, s in ((1450, "outlets 1450"), (1300, "tray / belt 1300"), (1000, "oven 1000")):
    d.line([(fx(0) - 22, fy(yy)), (fx(0) - 4, fy(yy))], fill=INK, width=2)
    txt(fx(0) - 28, fy(yy), s, f16, INK, "rm")

# ---------------- ADIMLAR ----------------
AD = ["A dough ball is placed on the tray under the press.",
      "Press flattens the dough on the tray. The tray sits on a fixed anvil: press force never loads the tray drive.",
      "Tray carriage moves under the hoppers. At each hopper it lifts near the outlet, rotates + slides (spiral) while dosing; load cell checks grams.",
      "At the oven entry a pusher moves the topped product onto the oven belt.",
      "Tray returns empty to the press.",
      "Conveyor oven bakes with 4 products inside the chamber: at least 60 products per hour.",
      "Baked product leaves the oven."]
y0 = 1395
txt(260, y0 - 12, "HOW IT WORKS", f26, INK, "la")
for i, s in enumerate(AD):
    c = GRN if i == 0 else BLUE if i == 4 else ORG if i == 5 else INK if i == 6 else RED
    adim(277, y0 + 48 + i * 40, i + 1, c)
    txt(308, y0 + 48 + i * 40, s, f20, INK, "lm")

# ---------------- IHTIYAC TABLOSU ----------------
TX0, TX1 = 2070, 2840
ty = 150
txt(TX0, ty, "OUR REQUIREMENTS", f30, INK, "la")
ty += 55
for k, v in (("Product", "round base Ø300 mm · lahmacun + pide"), ("Normal day", "80 pide + 200 lahmacun"), ("Busiest day", "×1.4 (Saturday)"),
             ("Peak hour", "42 /h weekday · 59 /h Saturday"), ("Design output", "60 products / hour")):
    txt(TX0, ty, k, fb18, INK, "la")
    txt(TX0 + 230, ty, v, f18, INK, "la")
    d.line([(TX0, ty + 32), (TX1, ty + 32)], fill=(220, 220, 226), width=1)
    ty += 42
ty += 20
txt(TX0, ty, "HOPPER CAPACITY TARGET", fb22, RED, "la")
txt(TX0, ty + 32, "no refilling within these days · normal-day consumption", f16, GRAY, "la")
ty += 72
for hx, h in ((TX0, "ingredient"), (TX0 + 395, "per day"), (TX0 + 505, "lasts"), (TX0 + 590, "capacity"), (TX0 + 700, "≈ L")):
    txt(hx, ty, h, fb18, GRAY, "la")
ty += 34
for ad_, not_, kg, gun, rho in HEDEF:
    txt(TX0, ty, ad_, fb18, INK, "la")
    txt(TX0, ty + 24, not_, f14, GRAY, "la")
    txt(TX0 + 395, ty, "%.1f kg" % kg, f18, INK, "la")
    txt(TX0 + 505, ty, "%d days" % gun, f18, INK, "la")
    txt(TX0 + 590, ty, "%.1f kg" % (kg * gun), fb18, RED, "la")
    txt(TX0 + 700, ty, "%.0f" % (kg * gun / rho), f18, INK, "la")
    d.line([(TX0, ty + 50), (TX1, ty + 50)], fill=(220, 220, 226), width=1)
    ty += 60
ty += 6
d.rectangle([TX0, ty, TX1, ty + 40], fill=(253, 240, 238), outline=RED, width=2)
txt((TX0 + TX1) / 2, ty + 20, "More hoppers per ingredient are fine for us.", fb18, RED, "mm")
ty += 68
txt(TX0, ty, "OVEN · POWER · CONTROL", fb22, ORG, "la")
ty += 42
for k, v in (("Oven", "electric conveyor · 4 in chamber"), ("", "pide 240 s · lahmacun 180 s · ≥60 /h"),
             ("Size", "belt ≤ 450 · depth ≤ 830"), ("Power", "400 V 3-phase 50 Hz per site"),
             ("Control", "PLC / Modbus TCP signals:"), ("", "tray ready · dose done · oven slot free")):
    txt(TX0, ty, k, fb18, INK, "la")
    txt(TX0 + 150, ty, v, f18, INK, "la")
    ty += 34

assert not os.path.exists(OUT), "v2 zaten var — yeni numara ver"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.save(OUT)
print("yazildi:", OUT)
