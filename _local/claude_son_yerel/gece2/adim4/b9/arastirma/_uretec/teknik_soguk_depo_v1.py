# -*- coding: utf-8 -*-
"""AUTOKITCH - SOGUK DEPO v1 · HAFTALIK TEDARIK (15 Eyl 2026): UST + ON GORUNUS. Olculer mm.
Kemal: "gunluk her sey kasette; tedarikci getirir, kasetlere koyar, buzlukta donar, buzdolabinda cozulur, eleman makineye takar;
 hamurlar da buzdolabinda, 2 gun mayalanip makineye; ust gorunus + buzluk/buzdolabi tam karsidan, icinde kasetler ve hamurlar."
KASET (yeni): dis 50 x 250 x 400, et 2,5 -> ic 45 x 245 x 395 = 4,35 L; agiz/huni kaybi %15 + dolum %90 -> 3,33 L.
  1 gun: HARC 21,6 L -> 7 · KIYMA 3,2 L -> 1 · KUSBASI 2,9 kg / 0,58 = 5,0 L -> 2 · KASAR 4,4 kg / 0,40 = 11 L -> 4 · SUCUK 1,4 / 0,58 = 2,4 L -> 1 = 15.
  45 mm urun kalinligi: buzdolabinda cozulme (Plank, et, +3 C) fanli ~26 sa, durgun hava ~44 sa -> buzluktan 2 gun once alinir.
  (eski 108 mm kaset: 3,5-5 gun)
HAMUR: pide 220 g x 80 + lahmacun 110 g x 200 = 280 top. Buzlukta 1 kasa/gun GN 2/1 650 x 530 x 200 (dip dibe donuk).
  Buzdolabinda 2 gun (cozulme 8-12 sa + yavas mayalanma): 8 kapakli GN 2/1 tepsi x 65 · pide 5 x 6 = 30 (3 tepsi) · lahmacun 6 x 7 = 42 (5 tepsi).
DOLAP: Oztiryakiler GN 1200 LMV dis 1344 x 830 x 2000, 1200 L, GN 2/1 raf; kapi basina ic ~582 x 680 x 1500 (1200 L'den hesap).
  Tek kapi 700 genislik (dogrulanacak). Buzdolabi ayni govde (varsayim).
DURUM: Pazartesi sabahi, teslimat + gunluk tasima sonrasi. Makine: PZT seti. Buzdolabi: SALI (Pazar'dan) + CARSAMBA (bugun). Buzluk: PER..SALI (sonraki) = 6 set.
Kural: paftada yalniz gorunus + olcu + parca adi; aciklama mesajda.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\TEDARIK".replace("WEBSITE", "WEBS\u0130TE")
OUT = os.path.join(OUT_DIR, "SOGUK_DEPO_v1_teknik.png")
W_PX, H_PX = 4700, 1610
S = 0.55
BG, INK, GRAY, LINE = (255, 255, 255), (26, 26, 28), (132, 132, 140), (72, 72, 78)
DON, SOG, GOVDE = (226, 237, 252), (230, 245, 236), (246, 246, 248)
RAFC, BOS = (176, 176, 184), (160, 160, 168)
HAMUR, HAMURK, KASAF = (238, 218, 160), (196, 150, 70), (252, 247, 232)
URUN = [("HARÇ", 7, (176, 60, 44)), ("KIYMA", 1, (112, 38, 32)), ("KUŞBAŞI", 2, (146, 98, 60)),
        ("KAŞAR", 4, (236, 204, 104)), ("SUCUK", 1, (152, 36, 70))]


def F(sz, b=False):
    for n in (("arialbd.ttf", "segoeuib.ttf") if b else ("arial.ttf", "segoeui.ttf")):
        try:
            return ImageFont.truetype(n, sz)
        except Exception:
            pass
    return ImageFont.load_default()


f8, f9, f11, f13, f16, f24 = F(17), F(19), F(22), F(25), F(29, True), F(44, True)
im = Image.new("RGB", (W_PX, H_PX), BG)
d = ImageDraw.Draw(im)


def txt(x, y, s, f=f11, c=INK, a="la"):
    d.text((x, y), s, font=f, fill=c, anchor=a)


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


def darc(cx, cy, r, a0, a1, c, w=1, seg=3.0):
    n = int(abs(a1 - a0) / seg)
    for k in range(0, n, 2):
        p, q = math.radians(a0 + k * seg), math.radians(a0 + (k + 1) * seg)
        d.line([(cx + r * math.cos(p), cy + r * math.sin(p)), (cx + r * math.cos(q), cy + r * math.sin(q))], fill=c, width=w)


def etiket(x, y, s, f=f8, c=INK):
    tw = d.textlength(s, font=f)
    d.rounded_rectangle([x - tw / 2 - 8, y - 13, x + tw / 2 + 8, y + 13], 5, fill=BG, outline=c, width=1)
    txt(x, y, s, f, c, "mm")


# ======================= VERI =======================
KT, KD, KH = 50.0, 250.0, 400.0
KUL = (KT - 5) * (KD - 5) * (KH - 5) / 1e6 * 0.85 * 0.90          # 3,33 L kullanilir
GUNLUK_L = {"HARÇ": 21.6, "KIYMA": 3.2, "KUŞBAŞI": 2.9 / 0.58, "KAŞAR": 4.4 / 0.40, "SUCUK": 1.4 / 0.58}
for _ad, _n, _ in URUN:
    assert math.ceil(GUNLUK_L[_ad] / KUL) == _n, (_ad, GUNLUK_L[_ad] / KUL)
SET = sum(n for _, n, _ in URUN)
assert SET == 15
RENK = [c for _, n, c in URUN for _ in range(n)]      # on sira 10: HARÇ 7 + KIYMA + KUŞBAŞI 2 · arka sira 5: KAŞAR 4 + SUCUK
WALL, BASE, HCAB, DCAB, ICD = 60.0, 150.0, 2000.0, 830.0, 680.0
IN_BOT, IN_H = BASE + WALL, 1500.0
IN_TOP = IN_BOT + IN_H
RAF_W, RAF_D = 530.0, 650.0
ADIM_K, ADIM_KASA, KASA_H, ADIM_T = 480.0, 210.0, 200.0, 65.0
KOMP = 582.0
assert 3 * ADIM_K <= IN_H and 6 * ADIM_KASA <= IN_H and 16 * ADIM_T <= IN_H
assert 10 * KT + 9 * 3.0 <= RAF_W and 2 * KD + 20.0 <= RAF_D
assert abs(3 * WALL + 2 * KOMP - 1344.0) < 1e-9 and abs(2 * WALL + 580.0 - 700.0) < 1e-9
assert 80 <= 3 * 30 and 200 <= 5 * 42                  # tepsi: pide 3 x 30 · lahmacun 5 x 42

DOLAP = [("BUZLUK 1 · −18 °C", 0.0, 1344.0, DON), ("BUZLUK 2 · −18 °C", 1394.0, 700.0, DON),
         ("BUZDOLABI · +2 °C", 2144.0, 1344.0, SOG)]
L_SIRA = DOLAP[-1][1] + DOLAP[-1][2]                    # 3488


def bolme(x0, w):
    if w > 1000:
        return [(x0 + WALL, x0 + WALL + KOMP), (x0 + 2 * WALL + KOMP, x0 + 2 * WALL + 2 * KOMP)]
    return [(x0 + WALL, x0 + w - WALL)]


ICERIK = {(0, 0): ("kaset", ["PERŞEMBE", "CUMA", "CUMARTESİ"]),
          (0, 1): ("kaset", ["PAZAR", "PAZARTESİ (sonraki)", "SALI (sonraki)"]),
          (1, 0): ("kasa", ["PERŞEMBE", "CUMA", "CUMARTESİ", "PAZAR", "PAZARTESİ (sonraki)", "SALI (sonraki)"]),
          (2, 0): ("kaset", ["SALI (yarın)", "ÇARŞAMBA", None]),
          (2, 1): ("tepsi", ["SALI (yarın)", "ÇARŞAMBA"])}
don_set = sum(1 for (i, j), (t, l) in ICERIK.items() if i < 2 and t == "kaset" for g in l if g)
sog_set = sum(1 for g in ICERIK[(2, 0)][1] if g)
assert don_set == 6 and len(ICERIK[(1, 0)][1]) == 6 and sog_set == 2 and len(ICERIK[(2, 1)][1]) == 2

# ======================= BASLIK =======================
OXT, YF = 170.0, 840.0
txt(OXT, 70, "AUTOKITCH · SOĞUK DEPO v1", f24, INK, "lm")
txt(OXT, 125, "haftalık tedarik · Pazartesi sabahı: teslimat ve günlük taşıma sonrası", f11, GRAY, "lm")


# ======================= UST GORUNUS =======================
def tx(x):
    return OXT + x * S


def ty(y):
    return YF - y * S


txt(tx(L_SIRA / 2), ty(DCAB) - 70, "ÜST GÖRÜNÜŞ", f16, INK, "mm")
for i, (ad, x0, w, zem) in enumerate(DOLAP):
    d.rectangle([tx(x0), ty(DCAB), tx(x0 + w), ty(0)], fill=GOVDE, outline=INK, width=4)
    bol = bolme(x0, w)
    for j, (b0, b1) in enumerate(bol):
        d.rectangle([tx(b0), ty(WALL + ICD), tx(b1), ty(WALL)], fill=zem, outline=LINE, width=2)
        cm = (b0 + b1) / 2
        r0x, r0y = cm - RAF_W / 2, WALL + (ICD - RAF_D) / 2
        tur, _g = ICERIK[(i, j)]
        if tur == "kaset":
            drect(tx(r0x), ty(r0y + RAF_D), tx(r0x + RAF_W), ty(r0y), RAFC, 2)
            for r in range(2):
                for k in range(10):
                    xa, ya = r0x + 1.5 + k * 53.0, r0y + 15.0 + r * (KD + 20.0)
                    idx = r * 10 + k
                    if idx < SET:
                        d.rectangle([tx(xa), ty(ya + KD), tx(xa + KT), ty(ya)], fill=RENK[idx], outline=INK, width=1)
                    else:
                        drect(tx(xa), ty(ya + KD), tx(xa + KT), ty(ya), BOS, 1)
        elif tur == "kasa":
            d.rectangle([tx(r0x), ty(r0y + RAF_D), tx(r0x + RAF_W), ty(r0y)], fill=KASAF, outline=HAMURK, width=3)
            rr_, py_ = 37.5, 37.5 * math.sqrt(3)
            row, yy = 0, r0y + 37.5 + 4
            while yy + rr_ <= r0y + RAF_D - 2:
                xx = r0x + rr_ + 4 + (rr_ if row % 2 else 0.0)
                while xx + rr_ <= r0x + RAF_W - 2:
                    d.ellipse([tx(xx - rr_), ty(yy + rr_), tx(xx + rr_), ty(yy - rr_)], fill=HAMUR, outline=HAMURK, width=1)
                    xx += 2 * rr_
                yy += py_
                row += 1
        else:                                            # en ustteki tepsi: lahmacun 6 x 7
            d.rectangle([tx(r0x), ty(r0y + RAF_D), tx(r0x + RAF_W), ty(r0y)], fill=KASAF, outline=HAMURK, width=3)
            for a in range(6):
                for b in range(7):
                    cx, cy = r0x + RAF_W / 2 + (a - 2.5) * 85.0, r0y + RAF_D / 2 + (b - 3) * 85.0
                    d.ellipse([tx(cx - 35), ty(cy + 35), tx(cx + 35), ty(cy - 35)], fill=HAMUR, outline=HAMURK, width=1)
    kapi = [(x0, 0.0, 90.0, bol[0][1] - x0), (x0 + w, 90.0, 180.0, x0 + w - bol[1][0])] if len(bol) == 2 else [(x0, 0.0, 90.0, w)]
    for hx, a0, a1, R in kapi:
        darc(tx(hx), ty(0), R * S, a0, a1, GRAY, 2)
        d.line([(tx(hx), ty(0)), (tx(hx), ty(0) + R * S)], fill=LINE, width=3)
yb = ty(0) + 700 * S + 45
for ad, x0, w, _ in DOLAP:
    olcu_h(tx(x0), tx(x0 + w), yb, "%d" % w)
olcu_h(tx(0), tx(L_SIRA), yb + 58, "%d" % L_SIRA, f11)
olcu_v(tx(0) - 45, ty(DCAB), ty(0), "%d" % DCAB, f9, INK, "l")
olcu_v(tx(L_SIRA) + 45, ty(WALL + (ICD - RAF_D) / 2 + RAF_D), ty(WALL + (ICD - RAF_D) / 2), "raf %d" % RAF_D, f9, INK, "r")

# ======================= ON GORUNUS =======================
OXF, OYF = tx(L_SIRA) + 330, 1390.0


def fx(x):
    return OXF + x * S


def fz(z):
    return OYF - z * S


txt(fx(L_SIRA / 2), fz(HCAB) - 55, "ÖN GÖRÜNÜŞ · kapılar açık", f16, INK, "mm")
d.line([(fx(-80), fz(0)), (fx(L_SIRA + 80), fz(0))], fill=LINE, width=3)
for i, (ad, x0, w, zem) in enumerate(DOLAP):
    d.rectangle([fx(x0), fz(HCAB), fx(x0 + w), fz(BASE)], fill=GOVDE, outline=INK, width=4)
    d.line([(fx(x0), fz(IN_TOP + WALL)), (fx(x0 + w), fz(IN_TOP + WALL))], fill=INK, width=2)
    for ax in (x0 + 50.0, x0 + w - 110.0):
        d.rectangle([fx(ax), fz(BASE), fx(ax + 60), fz(0)], fill=GRAY)
    txt(fx(x0 + w / 2), fz((IN_TOP + WALL + HCAB) / 2), ad, f11 if w > 1000 else f9, INK, "mm")
    for j, (b0, b1) in enumerate(bolme(x0, w)):
        d.rectangle([fx(b0), fz(IN_TOP), fx(b1), fz(IN_BOT)], fill=zem, outline=LINE, width=2)
        cm = (b0 + b1) / 2
        r0x = cm - RAF_W / 2
        tur, gunler = ICERIK[(i, j)]
        if tur == "kaset":
            for k, g in enumerate(gunler):
                z0 = IN_BOT + k * ADIM_K
                d.rectangle([fx(r0x), fz(z0 + 20), fx(r0x + RAF_W), fz(z0)], fill=RAFC)
                for s_ in range(10):
                    xa = r0x + 1.5 + s_ * 53.0
                    if g:
                        d.rectangle([fx(xa), fz(z0 + 20 + KH), fx(xa + KT), fz(z0 + 20)], fill=RENK[s_], outline=INK, width=1)
                    else:
                        drect(fx(xa), fz(z0 + 20 + KH), fx(xa + KT), fz(z0 + 20), BOS, 1)
                etiket(fx(cm), fz(z0 + 20 + KH + 30), ("%s · 15 KASET" % g) if g else "BOŞ RAF", f8, INK if g else GRAY)
        elif tur == "kasa":
            for k, g in enumerate(gunler):
                z0 = IN_BOT + k * ADIM_KASA
                d.rectangle([fx(r0x), fz(z0 + KASA_H), fx(r0x + RAF_W), fz(z0)], fill=KASAF, outline=HAMURK, width=3)
                for b in range(7):
                    cx = r0x + 37.9 + b * 75.7
                    d.ellipse([fx(cx - 36), fz(z0 + 8 + 72), fx(cx + 36), fz(z0 + 8)], fill=HAMUR, outline=HAMURK, width=1)
                for b in range(8):
                    cx = r0x + 33.1 + b * 66.2
                    d.ellipse([fx(cx - 29), fz(z0 + 88 + 58), fx(cx + 29), fz(z0 + 88)], fill=HAMUR, outline=HAMURK, width=1)
                etiket(fx(cm), fz(z0 + KASA_H - 24), "%s · 280 top" % g)
        else:
            for gi, g in enumerate(gunler):
                for t in range(8):
                    z0 = IN_BOT + (gi * 8 + t) * ADIM_T
                    d.rectangle([fx(r0x), fz(z0 + 60), fx(r0x + RAF_W), fz(z0)], fill=KASAF, outline=HAMURK, width=2)
                    nb, cap = (5, 90.0) if t < 3 else (6, 75.0)
                    p_ = RAF_W / nb
                    for b in range(nb):
                        cx = r0x + p_ * (b + 0.5)
                        d.chord([fx(cx - cap / 2), fz(z0 + 49), fx(cx + cap / 2), fz(z0 - 41)], 180, 360, fill=HAMUR, outline=HAMURK, width=1)
                etiket(fx(cm), fz(IN_BOT + (gi * 8 + 4) * ADIM_T), "%s · 8 TEPSİ" % g)
olcu_v(fx(L_SIRA) + 60, fz(HCAB), fz(0), "%d" % HCAB, f11, INK, "r")
olcu_v(fx(0) - 40, fz(IN_BOT + ADIM_K), fz(IN_BOT), "%d" % ADIM_K, f9, INK, "l")
olcu_v(fx(0) - 130, fz(IN_BOT + 20 + KH), fz(IN_BOT + 20), "%d" % KH, f9, INK, "l")
for ad, x0, w, _ in DOLAP:
    olcu_h(fx(x0), fx(x0 + w), fz(0) + 45, "%d" % w)

# ======================= LEJANT =======================
ly = H_PX - 95
d.line([(OXT, ly - 40), (W_PX - 160, ly - 40)], fill=LINE, width=2)
xx = OXT
for ad, n, c in URUN:
    s_ = "%s ×%d" % (ad, n)
    d.rectangle([xx, ly - 11, xx + 30, ly + 11], fill=c, outline=INK, width=1)
    txt(xx + 40, ly, s_, f9, INK, "lm")
    xx += 40 + d.textlength(s_, font=f9) + 40
d.rectangle([xx, ly - 11, xx + 30, ly + 11], fill=HAMUR, outline=HAMURK, width=2)
txt(xx + 40, ly, "HAMUR", f9, INK, "lm")
xx += 40 + d.textlength("HAMUR", font=f9) + 40
drect(xx, ly - 11, xx + 30, ly + 11, BOS, 2)
txt(xx + 40, ly, "boş yer", f9, INK, "lm")
txt(W_PX - 160, ly, "1 GÜN SETİ = 15 KASET · kaset 50 × 250 × 400 (3,3 L) · hamur 1 gün = 280 top (80 pide 220 g + 200 lahmacun 110 g) · kasa 650 × 530 × 200 · tepsi 650 × 530 × 65 (pide 3 × 30, lahmacun 5 × 42)", f9, GRAY, "rm")
txt(W_PX - 160, ly + 40, "dolap: Öztiryakiler GN 1200 LMV 1344 × 830 × 2000 (1200 L, GN 2/1 raf) · buzdolabı aynı gövde · tek kapı ≈ 700 · ölçüler mm", f9, GRAY, "rm")

os.makedirs(OUT_DIR, exist_ok=True)
assert not os.path.exists(OUT), "soguk depo v1 zaten var — yeni numara ver"
im.save(OUT)
print("yazildi:", OUT, "· kaset kullanilir %.2f L" % KUL, "· sira", L_SIRA)
