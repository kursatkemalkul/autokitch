# -*- coding: utf-8 -*-
"""AUTOKITCH x YINDU/ATOSA - PIDE & LAHMACUN MODULE - CONCEPT FRONT VIEW v1 (14 Sep 2026). Olculer mm. Ingilizce (Yindu'ya gidecek).
Kemal: pres (bizim, Turk firma) + Atosa Auto Pizza Artisan'in bize uyarlanmis hali (tabla presin altina girer, orse oturur) + uyarlanmis konveyor firin;
oklarla nasil calistigi, gunluk/saatlik ihtiyac ve kg tablosu.
KAYNAK: sim_karsi (tabla turu ~40 sn, tepe saat 42/59 urun), stok kurgusu (80 pide + 200 lahmacun, cumartesi x1,4), gramaj arastirmasi
(lahmacun harc 108 g, kasarli 130 g, sucuklu 90+70 g, kiymali 160 g, kusbasi 145 g), yogunluklar (harc/kiyma 1,0 · kusbasi 0,58 · sucuk 0,59 · kasar 0,40),
hat pafta v4 (PRESS 700 · TOPPING 1000 · OVEN 1500 · bant/tabla kotu 1300 · firin govdesi 1000-1620 · 830 derin).
VARSAYIM: pide cesidi 4 cesit esit.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE\ATOSA_MODUL_v1_teknik.png".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX, S = 2900, 1750, 0.5
BG, INK, GRAY, LINE = (255, 255, 255), (26, 26, 28), (120, 120, 128), (72, 72, 78)
BLUE, RED, ORG, GRN = (0, 86, 184), (198, 42, 32), (200, 90, 30), (14, 120, 90)
FILL, SOFT, EVC, HAVA, PROD = (244, 244, 246), (232, 232, 236), (226, 238, 252), (255, 232, 210), (240, 214, 170)


def F(sz, b=False):
    for n in (("arialbd.ttf",) if b else ("arial.ttf",)):
        try:
            return ImageFont.truetype(n, sz)
        except Exception:
            pass
    return ImageFont.load_default()


f14, f16, f18, f20, f22, f26, f30, f44 = F(14), F(16), F(18), F(20), F(22), F(26, True), F(30, True), F(44, True)
fb16 = F(16, True)
fb18, fb20, fb22 = F(18, True), F(20, True), F(22, True)
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
    (dline if dashed else (lambda p, q, cc, ww: d.line([p, q], fill=cc, width=ww)))((x0, y0), (x1, y1), c, w)
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


def tarali(x0, y0, x1, y1, c=(215, 215, 222), adim_=16):
    w, h = x1 - x0, y1 - y0
    for k in range(0, int(w + h), adim_):
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


# ---------------- IHTIYAC HESABI ----------------
NORMAL_PIDE, NORMAL_LAHM, BUSY = 80, 200, 1.4
TUR = 4                                   # pide cesidi esit
pb, lb = NORMAL_PIDE * BUSY, NORMAL_LAHM * BUSY
KG = [("Lahmacun paste", "thick wet minced-meat paste", "108 g", lb * 108 / 1000, 1.00),
      ("Minced-meat pide filling", "moist minced meat mix", "160 g", pb / TUR * 160 / 1000, 1.00),
      ("Diced meat (kuşbaşı)", "small meat cubes", "145 g", pb / TUR * 145 / 1000, 0.58),
      ("Grated kaşar cheese", "Turkish semi-hard cheese", "130 / 90 g", pb / TUR * (130 + 90) / 1000, 0.40),
      ("Sucuk", "sliced, or 38 mm sticks to slice", "70 g", pb / TUR * 70 / 1000, 0.59)]
for ad, _, g, kg, rho in KG:
    print("%-26s %-9s %5.1f kg/busiest day  ~%4.1f L" % (ad, g, kg, kg / rho))

# ---------------- BASLIK ----------------
txt(110, 28, "AUTOKITCH × YINDU / ATOSA  ·  PIDE & LAHMACUN MODULE  ·  CONCEPT FRONT VIEW  v1", f44, INK)
txt(110, 90, "press (AUTOKITCH)  →  customized Auto Pizza Artisan topping module  →  customized conveyor oven  ·  dimensions in mm  ·  14 Sep 2026", f22, GRAY)
d.line([(110, 128), (W_PX - 60, 128)], fill=LINE, width=3)

# ---------------- ALT: SOGUK DEPO (bizim) ----------------
d.rectangle([fx(0), fy(120), fx(3200), fy(0)], fill=SOFT, outline=LINE, width=2)
d.rectangle([fx(0), fy(980), fx(3200), fy(120)], fill=(250, 250, 251), outline=GRAY, width=2)
tarali(fx(0) + 1, fy(980) + 1, fx(3200) - 1, fy(120) - 1)
txt(fx(1600), fy(600), "BELOW THE LINE: AUTOKITCH REFRIGERATED STORE  ·  dough drawers, drinks  ·  not in Yindu scope", f22, GRAY, "mm")
for i in range(5):
    d.rectangle([fx(150 + i * 600), fy(420), fx(620 + i * 600), fy(300)], fill=BG, outline=GRN, width=2)
txt(fx(385), fy(360), "dough drawer", f14, GRN, "mm")

# ---------------- PRES MODULU (bizim) ----------------
d.rectangle([fx(0), fy(1970), fx(700), fy(980)], fill=FILL, outline=LINE, width=3)
d.rectangle([fx(110), fy(1920), fx(590), fy(1600)], fill=BG, outline=INK, width=2)
txt(fx(350), fy(1790), "PRESS HEAD", fb18, INK, "mm")
txt(fx(350), fy(1730), "Turkish press manufacturer", f16, GRAY, "mm")
d.rectangle([fx(335), fy(1600), fx(365), fy(1350)], fill=(160, 160, 168))
d.rectangle([fx(160), fy(1350), fx(540), fy(1320)], fill=(120, 120, 128))
txt(fx(150), fy(1335), "platen", f14, GRAY, "rm")
d.rectangle([fx(200), fy(1265), fx(500), fy(1150)], fill=(150, 150, 158), outline=INK, width=2)
txt(fx(350), fy(1207), "FIXED ANVIL", fb18, BG, "mm")
tabla(350, 1265)
urun(350, 1285, (233, 217, 168))

# ---------------- TOPPING MODULU (Yindu) ----------------
d.rectangle([fx(700), fy(1970), fx(1700), fy(980)], fill=FILL, outline=LINE, width=3)
d.rectangle([fx(710), fy(1960), fx(1690), fy(1450)], fill=EVC, outline=BLUE, width=2)
txt(fx(1200), fy(1935), "REFRIGERATED HOPPERS +3 °C · slide in from front", f16, BLUE, "mm")
HOP = [("LAHMACUN", "PASTE", "30 kg", 240), ("MINCED", "MEAT", "4.5 kg", 175), ("DICED", "MEAT", "4.1 kg", 175), ("KAŞAR", "CHEESE", "6.2 kg", 190), ("SUCUK", "SLICER", "2 kg", 170)]
x = 710.0
CX = []
for a1, a2, kg, w in HOP:
    d.rectangle([fx(x), fy(1880), fx(x + w), fy(1480)], fill=BG, outline=INK, width=2)
    txt(fx(x + w / 2), fy(1760), a1, fb16, INK, "mm")
    txt(fx(x + w / 2), fy(1715), a2, fb16, INK, "mm")
    txt(fx(x + w / 2), fy(1620), kg, f18, RED, "mm")
    txt(fx(x + w / 2), fy(1575), "per day", f14, GRAY, "mm")
    d.rectangle([fx(x + w / 2 - 25), fy(1480), fx(x + w / 2 + 25), fy(1450)], fill=RED)
    CX.append(x + w / 2)
    x += w + 7.5
# kizak + damlama tavasi
d.rectangle([fx(150), fy(1190), fx(1660), fy(1170)], fill=BLUE)
txt(fx(1180), fy(1150), "tray carriage rail (extends under the press)  ·  drip tray below", f16, BLUE, "mm")
# tabla 2: kasetin altinda, kalkmis, donerek
tabla(CX[0], 1390)
urun(CX[0], 1410)
d.rectangle([fx(CX[0] - 12), fy(1390), fx(CX[0] + 12), fy(1190)], fill=(150, 150, 158))
d.arc([fx(CX[0] - 190), fy(1470), fx(CX[0] + 190), fy(1360)], 200, 340, fill=RED, width=4)
ok(fx(CX[0] + 150), fy(1450), fx(CX[0] + 185), fy(1418), RED, 4)
txt(fx(CX[0] - 200), fy(1455), "rotate + slide", f14, RED, "rm")
txt(fx(CX[0] + 22), fy(1268), "lift · load cell", f14, GRAY, "lm")
# tabla 3: firin girisinde, itici
tabla(1470, 1265, True)
urun(1470, 1285)
d.rectangle([fx(1285), fy(1360), fx(1300), fy(1285)], fill=(255, 190, 0), outline=INK, width=1)
txt(fx(1292), fy(1385), "pusher", f14, INK, "mm")

# ---------------- FIRIN (Yindu) ----------------
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
ok(fx(3200), fy(1285), fx(3420), fy(1285), INK, 4)
txt(fx(3215), fy(1245), "to cutting + oil spray", f16, INK, "la")
txt(fx(3215), fy(1210), "+ boxing (AUTOKITCH)", f16, INK, "la")

# ---------------- AKIS OKLARI ----------------
ok(fx(470), fy(380), fx(420), fy(1250), GRN, 4, True)                         # 1 robot: cekmece -> tabla
txt(fx(520), fy(820), "robot arm", f16, GRN, "la")
txt(fx(520), fy(790), "(AUTOKITCH)", f16, GRN, "la")
adim(fx(450), fy(620), 1, GRN)
adim(fx(620), fy(1790), 2)
ok(fx(530), fy(1300), fx(CX[0] - 180), fy(1395), RED, 4)                      # tabla -> kaset
adim(fx(CX[0] - 210), fy(1540), 3)
ok(fx(CX[0] + 180), fy(1390), fx(1300), fy(1300), RED, 4)                     # kaset -> firin agzi
adim(fx(1370), fy(1420), 4)
ok(fx(1300), fy(1320), fx(1690), fy(1320), ORG, 4)                            # itici -> firin bandi
ok(fx(1300), fy(1212), fx(560), fy(1212), BLUE, 3, True)                      # 5 bos donus
adim(fx(1180), fy(1212), 5, BLUE)
adim(fx(1800), fy(1430), 6, ORG)
adim(fx(3330), fy(1340), 7, INK)

# ---------------- KAPSAM + OLCULER ----------------
drect(fx(690) - 8, fy(1990) - 8, fx(3210) + 8, fy(990) + 8, BLUE, 4)
txt(fx(1950), fy(1990) - 22, "REQUEST TO YINDU / ATOSA  ·  customized topping module + conveyor oven", fb20, BLUE, "md")
txt(fx(350), fy(1990) - 22, "AUTOKITCH (Turkey)", fb20, GRAY, "md")
olcu_h(fx(0), fx(700), fy(1970) - 78, "700", f18)
olcu_h(fx(700), fx(1700), fy(1970) - 78, "1000", f18)
olcu_h(fx(1700), fx(3200), fy(1970) - 78, "1500", f18)
olcu_h(fx(0), fx(3200), fy(0) + 40, "3200  ·  depth 830 for all modules", f20)
olcu_v(fx(0) - 190, fy(1970), fy(0), "1970", f18)
for yy, s in ((1450, "outlets 1450"), (1300, "tray / belt 1300"), (1000, "oven 1000")):
    d.line([(fx(0) - 22, fy(yy)), (fx(0) - 4, fy(yy))], fill=INK, width=2)
    txt(fx(0) - 28, fy(yy), s, f16, INK, "rm")

# ---------------- ADIMLAR ----------------
AD = ["Robot arm (AUTOKITCH) takes a dough ball from the refrigerated drawer and places it on the tray under the press.",
      "Press (AUTOKITCH, Turkish partner) flattens the dough on the tray. The tray sits on a fixed anvil: press force never loads the tray drive.",
      "Tray carriage moves under the hoppers. At each hopper it lifts near the outlet, rotates + slides (spiral) while dosing; load cell checks grams.",
      "At the oven entry a pusher moves the topped product onto the oven belt.",
      "Tray returns empty to the press (lahmacun cycle ≈ 40 s in our simulation).",
      "Conveyor oven bakes with 4 products inside the chamber: at least 60 products per hour.",
      "Exit to cutting + oil spray plate and automatic boxing (AUTOKITCH)."]
y0 = 1395
txt(OX, y0 - 12, "HOW IT WORKS", f26, INK, "la")
for i, s in enumerate(AD):
    c = GRN if i == 0 else BLUE if i == 4 else ORG if i == 5 else INK if i == 6 else RED
    adim(OX + 17, y0 + 48 + i * 42, i + 1, c)
    txt(OX + 48, y0 + 48 + i * 42, s, f20, INK, "lm")

# ---------------- IHTIYAC TABLOSU ----------------
TX0, TX1 = 2070, 2840
ty = 150
txt(TX0, ty, "OUR REQUIREMENTS", f30, INK, "la")
ty += 55
ROWS = [("Product", "round base Ø300 mm · lahmacun + pide"),
        ("Normal day", "%d pide + %d lahmacun" % (NORMAL_PIDE, NORMAL_LAHM)),
        ("Busiest day (×1.4)", "%d pide + %d lahmacun" % (round(pb), round(lb))),
        ("Peak hour", "42 /h weekday · 59 /h Saturday"),
        ("Design output", "60 products / hour"),
        ("Refill", "once a day · no touch during the day")]
for k, v in ROWS:
    txt(TX0, ty, k, fb18, INK, "la")
    txt(TX0 + 250, ty, v, f18, INK, "la")
    d.line([(TX0, ty + 32), (TX1, ty + 32)], fill=(220, 220, 226), width=1)
    ty += 42
ty += 20
txt(TX0, ty, "HOPPER CONTENT · BUSIEST DAY", fb22, RED, "la")
ty += 42
for hx, h in ((TX0, "ingredient"), (TX0 + 420, "portion"), (TX0 + 555, "kg/day"), (TX0 + 665, "≈ L")):
    txt(hx, ty, h, fb18, GRAY, "la")
ty += 34
for ad, not_, g, kg, rho in KG:
    txt(TX0, ty, ad, fb18, INK, "la")
    txt(TX0, ty + 24, not_, f14, GRAY, "la")
    txt(TX0 + 420, ty, g, f18, INK, "la")
    txt(TX0 + 555, ty, "%.1f" % kg, fb18, RED, "la")
    txt(TX0 + 665, ty, "%.1f" % (kg / rho), f18, INK, "la")
    d.line([(TX0, ty + 50), (TX1, ty + 50)], fill=(220, 220, 226), width=1)
    ty += 60
ty += 16
txt(TX0, ty, "OVEN · POWER · CONTROL", fb22, ORG, "la")
ty += 42
for k, v in (("Oven", "electric conveyor · 4 in chamber"), ("", "pide 240 s · lahmacun 180 s · ≥60 /h"),
             ("Size", "belt ≤ 450 · depth ≤ 830 · body 1000–1620"),
             ("Power", "400 V 3-phase 50 Hz per site"), ("Control", "PLC / Modbus TCP signals:"),
             ("", "tray ready · dose done · oven slot free")):
    txt(TX0, ty, k, fb18, INK, "la")
    txt(TX0 + 150, ty, v, f18, INK, "la")
    ty += 34
ty += 10
txt(TX0, ty, "pide mix assumed: 4 types equal (kaşar · sucuk+kaşar · minced · diced)", f14, GRAY, "la")

assert not os.path.exists(OUT), "v1 zaten var — yeni numara ver"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.save(OUT)
print("yazildi:", OUT)
