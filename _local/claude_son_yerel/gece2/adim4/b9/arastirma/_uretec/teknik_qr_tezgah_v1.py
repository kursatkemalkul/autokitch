# -*- coding: utf-8 -*-
"""AUTOKITCH · İSTASYON + QR DOLABI + TEZGÂH · teknik resim v1 (27 Eyl 2026) — yalnız teknik resim, 3B yok.
Kemal: "istasyon yanında QR dolabı, yanına tezgâh çiz; QR dolabı kaçtan başlayıp kaçta bitmeli (robot erişecek), altını mı üstünü mü
kullanırız; QR'ın en altında raf, teknik kısım; tezgâh küçük, altında adamın kendi çekmecesi; çöp lazım (robot çöpünü atsın);
personel WC / soyunma yok, basit duvar askısı; bir göreyim karar vereceğim".
SABİT ÖLÇÜLER (değiştirilmez): robot kontrol kutusu 475 × 423 × 268 (G × Y × D) · ana pano 400 × 350 × 250 · UPS 115 × 185 × 213 (hat v56 durum.json)
QR: 860 × 520 · 12 göz 2 × 6 · göz 380 × 190 × 440 (SERVİS_TESLİM v4 detay paftası). Yükseklik ve göz kotları bu resimde robot erişiminden çıkarılır.
ROBOT: FR5 omuz 970 · pratik bilek erişimi 779 (820 × 0,95) (HAT paftası v16 ortak veri) · ray ekseni hat yüzünden 330, QR robot yüzü 670 (dükkân v13:
  ray y 115,9 · QR arkası y 150 · hat yüzü y 83) → yatay 341 · göz ortası yanda 200 → yatay 395 → dikey ± √(779² − 395²) = ± 671 → 299–1641.
Göz bandı 400–1600 (6 × 200): altta 101, üstte 41 pay. Alt bölme 20–397: ana pano + UPS + QR kilit/kapak kartı + modem. Üst bölme 1603–2048: robot kontrol kutusu
  (alta konsa bant 448'den başlar, üst göz 1648 > 1641 → erişim dışı). Robot çöp kovası 30 L ray sonunda QR'ın yanında (VARSAYIM ölçü 300 × 300 × 450).
Tezgâh 600 × 450 × 900 (öneri): üstte kişisel çekmece (kilitli), altında çöp kovası 30 L; üstünde duvar askısı.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

KLASOR = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\FULL_MAKINE"
S = 0.5
OX, OY = 330, 300
W_PX, H_PX = 4700, 2950
BG, INK, GRAY, LINE, ACC, RED = (255, 255, 255), (26, 26, 28), (130, 130, 138), (70, 70, 76), (0, 86, 184), (198, 42, 32)
DOLAP, PUC, SICAK, TURUNCU, KARTON, SOFT, EVC, YESIL = (14, 120, 90), (255, 240, 200), (255, 226, 214), (200, 90, 30), (236, 214, 176), (232, 232, 238), (220, 235, 255), (40, 150, 80)
TEK = (240, 240, 244)


def F(sz, b=False):
    try:
        return ImageFont.truetype("arialbd.ttf" if b else "arial.ttf", sz)
    except Exception:
        return ImageFont.load_default()


f11, f13, f15, f18, f22, f30 = F(15), F(17), F(19), F(22), F(24, True), F(32, True)
im = Image.new("RGB", (W_PX, H_PX), BG)
d = ImageDraw.Draw(im)


def txt(x, y, s, f=f13, c=INK, a="mm"):
    d.text((x, y), s, font=f, fill=c, anchor=a)


def kesikc(pts, c=GRAY, w=2, dash=10, gap=6):
    for (a, b) in zip(pts, pts[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1]); i = 0
        while L > 0 and i * (dash + gap) < L:
            t0, t1 = i * (dash + gap) / L, min(1.0, (i * (dash + gap) + dash) / L)
            d.line([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0), (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)], fill=c, width=w); i += 1


# ============================ 1 · ÖN GÖRÜNÜŞ (robot tarafından) ============================
Y0 = OY + 2100 * S                         # y = 0 çizgisi (px)
fx = lambda x: OX + x * S
fy = lambda y: Y0 - y * S


def box(x0, x1, y0, y1, fill=None, out=LINE, w=2):
    d.rectangle([fx(x0), fy(y1), fx(x1), fy(y0)], fill=fill, outline=out, width=w)


def kbox(x0, x1, y0, y1, c=GRAY, w=2):
    kesikc([(fx(x0), fy(y0)), (fx(x1), fy(y0)), (fx(x1), fy(y1)), (fx(x0), fy(y1)), (fx(x0), fy(y0))], c, w)


def lab(x0, x1, y0, y1, s, f=f11, c=INK):
    sat = s.split("|"); cy = (fy(y0) + fy(y1)) / 2 - (len(sat) - 1) * 9
    for i, t in enumerate(sat):
        txt((fx(x0) + fx(x1)) / 2, cy + i * 18, t, f, c if i == 0 else GRAY)


def olcu_v(x, y0, y1, s, c=INK, sag=True):
    d.line([(x, fy(y0)), (x, fy(y1))], fill=c, width=2)
    for yy in (y0, y1):
        d.line([(x - 7, fy(yy)), (x + 7, fy(yy))], fill=c, width=2)
    txt(x + (10 if sag else -10), (fy(y0) + fy(y1)) / 2, s, f11, c, "lm" if sag else "rm")


def olcu_h(x0, x1, y, s, c=INK):
    d.line([(fx(x0), y), (fx(x1), y)], fill=c, width=2)
    for xx in (x0, x1):
        d.line([(fx(xx), y - 7), (fx(xx), y + 7)], fill=c, width=2)
    txt((fx(x0) + fx(x1)) / 2, y - 14, s, f11, c)


txt(OX, OY - 120, "1 · ÖN GÖRÜNÜŞ · robot tarafından · yan yana (istasyon · QR dolabı · tezgâh)", f22, ACC, "la")
d.line([(fx(-200), fy(0)), (fx(7900), fy(0))], fill=INK, width=3)
# --- istasyon (alçak hat v4, dış çizgiler)
L_, TOP = 788.0, 1862.0
for x0, x1 in ((0, 4000), (4000, 4600), (4600, 5430)):
    box(x0 + 30, x1 - 30, 0, 123, SOFT, LINE, 1)
box(0, 4000, 123, L_, (246, 248, 247), DOLAP, 3); lab(0, 4000, 123, L_, "ÇEKMECELİ DOLAP 0–4000 · üstü 788", f13, DOLAP)
box(0, 700, L_, TOP, (250, 250, 252)); lab(0, 700, L_, TOP, "A · AÇICI", f13)
box(700, 2500, L_, TOP, (250, 250, 252)); lab(700, 2500, L_, TOP, "C · TOPPING", f13)
box(2500, 4000, L_, L_ + 517, SICAK, TURUNCU, 3); lab(2500, 4000, L_, L_ + 517, "F · FIRIN", f13)
box(2500, 4000, L_ + 517, TOP, (250, 250, 252)); lab(2500, 4000, L_ + 517, TOP, "fırın üstü", f11, GRAY)
box(4000, 4600, 123, TOP, (250, 250, 252)); lab(4000, 4600, 900, TOP, "K", f13)
box(4000, 4600, 123, 889, None, LINE, 1); lab(4000, 4600, 123, 889, "bulaşık", f11, GRAY)
box(4600, 5430, 123, TOP, (250, 250, 252)); lab(4600, 5430, 700, TOP, "E · KUTU", f13)
olcu_v(fx(-60), 0, TOP, "1862", INK, False)
txt((fx(0) + fx(5430)) / 2, fy(TOP) - 26, "İSTASYON · alçak hat (Resim 1 v4) · 5430", f15, INK)
# --- robot çöp kovası (ray sonunda, QR yanında)
KX0 = 5530.0
box(KX0, KX0 + 300, 0, 450, (236, 236, 236), INK, 2); lab(KX0, KX0 + 300, 0, 450, "ROBOT|ÇÖP|30 L", f11)
txt((fx(KX0) + fx(KX0 + 300)) / 2, fy(450) - 14, "ray sonu", f11, GRAY)
# --- QR dolabı
QX0 = 5930.0
QW, QH = 860.0, 2050.0
GOZ0, GOZH, GOZN = 400.0, 200.0, 6
box(QX0, QX0 + QW, 0, QH, (248, 248, 250), INK, 3)
box(QX0 + 20, QX0 + QW - 20, 0, 20, SOFT, LINE, 1)
for r in range(GOZN):
    y0 = GOZ0 + r * GOZH
    for c_ in range(2):
        gx0 = QX0 + 30 + c_ * 410
        box(gx0, gx0 + 380, y0, y0 + 190, EVC, ACC, 2)
        txt((fx(gx0) + fx(gx0 + 380)) / 2, (fy(y0) + fy(y0 + 190)) / 2, "380 × 190", f11, ACC)
box(QX0 + 20, QX0 + QW - 20, GOZ0 - 3, GOZ0, INK, INK, 1)
box(QX0 + 20, QX0 + QW - 20, GOZ0 + GOZN * GOZH, GOZ0 + GOZN * GOZH + 3, INK, INK, 1)
# alt bölme: ana pano + UPS + QR kilit kartı
box(QX0 + 25, QX0 + 425, 20, 370, TEK, INK, 2); lab(QX0 + 25, QX0 + 425, 20, 370, "ANA PANO|400 × 350 × 250", f11)
box(QX0 + 435, QX0 + 550, 20, 205, TEK, INK, 2); lab(QX0 + 435, QX0 + 550, 20, 205, "UPS", f11)
box(QX0 + 560, QX0 + 835, 20, 220, TEK, INK, 2); lab(QX0 + 560, QX0 + 835, 20, 220, "QR KİLİT KARTI|+ modem", f11)
# üst bölme: robot kontrol
UY0 = GOZ0 + GOZN * GOZH + 3.0
box(QX0 + 25, QX0 + 500, UY0, UY0 + 423, TEK, INK, 2); lab(QX0 + 25, QX0 + 500, UY0, UY0 + 423, "ROBOT KONTROL|475 × 423 × 268", f11)
lab(QX0 + 510, QX0 + 835, UY0, UY0 + 423, "boş|325 × 445", f11, GRAY)
txt((fx(QX0) + fx(QX0 + QW)) / 2, fy(QH) - 26, "QR DOLABI 860 × 520 × 2050", f15, INK)
# ölçüler QR
xq = fx(QX0 + QW) + 16
olcu_v(xq, 0, 20, "20 ayak")
olcu_v(xq, 20, GOZ0, "377 alt bölme")
olcu_v(xq, GOZ0, GOZ0 + GOZN * GOZH, "1200 göz (6 × 200)")
olcu_v(xq, UY0, QH, "445 üst bölme")
for yy, s_ in ((GOZ0, "400"), (GOZ0 + GOZN * GOZH, "1600"), (QH, "2050")):
    txt(fx(QX0) - 8, fy(yy), s_, f11, INK, "rm")
# --- tezgâh + askı
TX0 = 7100.0
TW, TH = 600.0, 900.0
box(TX0, TX0 + TW, 0, 100, SOFT, LINE, 1)
box(TX0, TX0 + TW, 100, TH - 30, (250, 246, 238), INK, 2)
box(TX0 - 15, TX0 + TW + 15, TH - 30, TH, (215, 205, 190), INK, 2)
box(TX0 + 20, TX0 + TW - 20, TH - 200, TH - 45, (255, 250, 236), INK, 2); lab(TX0 + 20, TX0 + TW - 20, TH - 200, TH - 45, "KİŞİSEL ÇEKMECE|kilitli", f11)
box(TX0 + 150, TX0 + 450, 110, 560, (236, 236, 236), INK, 2); lab(TX0 + 150, TX0 + 450, 110, 560, "ÇÖP|30 L|poşetli", f11)
txt((fx(TX0) + fx(TX0 + TW)) / 2, fy(TH) - 26, "TEZGÂH 600 × 450 × 900", f15, INK)
d.line([(fx(TX0 + 50), fy(1650)), (fx(TX0 + TW - 50), fy(1650))], fill=INK, width=4)
for hx in (TX0 + 120, TX0 + 300, TX0 + 480):
    d.line([(fx(hx), fy(1650)), (fx(hx), fy(1600))], fill=INK, width=3)
    d.arc([fx(hx) - 10, fy(1600) - 10, fx(hx) + 10, fy(1600) + 10], 0, 180, fill=INK, width=3)
txt((fx(TX0) + fx(TX0 + TW)) / 2, fy(1650) - 18, "DUVAR ASKISI · basit", f11, INK)
olcu_v(fx(TX0 + TW) + 16, 0, TH, "900")
olcu_h(TX0, TX0 + TW, fy(0) + 40, "600")
olcu_h(QX0, QX0 + QW, fy(0) + 40, "860")
olcu_h(KX0, KX0 + 300, fy(0) + 40, "300")
olcu_h(0, 5430, fy(0) + 40, "5430")

# ============================ 2 · YAN KESİT (QR ortasından) · robot erişimi ============================
S2 = 0.5
SX0, SY0 = OX + 200, OY + 2100 * S + 360 + 2100 * S2       # z = hat arkası (−830) solda; y = 0 SY0
gz = lambda z: SX0 + (z + 830.0) * S2                       # z: hat yüzü 0, koridor +
gy = lambda y: SY0 - y * S2
txt(SX0 - 200, gy(2100) - 60, "2 · YAN KESİT · QR ortasından · robot erişimi (dükkân v13 yerleşimi: QR koridorun karşısında)", f22, ACC, "la")
d.line([(gz(-900), gy(0)), (gz(1500), gy(0))], fill=INK, width=3)


def sbox(z0, z1, y0, y1, fill=None, out=LINE, w=2):
    d.rectangle([gz(z0), gy(y1), gz(z1), gy(y0)], fill=fill, outline=out, width=w)


def slab(z0, z1, y0, y1, s, f=f11, c=INK):
    sat = s.split("|"); cy = (gy(y0) + gy(y1)) / 2 - (len(sat) - 1) * 9
    for i, t in enumerate(sat):
        txt((gz(z0) + gz(z1)) / 2, cy + i * 18, t, f, c if i == 0 else GRAY)


# E istasyonu yan
sbox(-830, 0, 123, TOP, (250, 250, 252)); slab(-830, 0, 900, TOP, "E · KUTU (yan)", f13)
sbox(-800, -30, 0, 123, SOFT, LINE, 1)
sbox(-830, 0, 936 - 4, 936, INK, INK, 1); txt(gz(-415), gy(936) + 14, "kutu tepsisi 936", f11, GRAY)
# robot
RZ_, OM, ER = 330.0, 970.0, 779.0
sbox(RZ_ - 120, RZ_ + 120, 0, 60, (200, 200, 205), LINE, 2); txt(gz(RZ_), gy(30), "ray", f11, INK)
sbox(RZ_ - 70, RZ_ + 70, 60, OM - 152, (225, 225, 230), LINE, 2); slab(RZ_ - 70, RZ_ + 70, 60, OM - 152, "kaide", f11, GRAY)
d.ellipse([gz(RZ_) - 10, gy(OM) - 10, gz(RZ_) + 10, gy(OM) + 10], fill=INK)
txt(gz(RZ_) - 16, gy(OM), "omuz 970", f11, INK, "rm")
# erişim yayı (yan düzlemde, göz yanal 200 dahil etkin yarıçap)
QZ0, QD = 670.0, 520.0
yatay = math.hypot(QZ0 - RZ_, 200.0)
dik = math.sqrt(ER ** 2 - yatay ** 2)
BANT = (OM - dik, OM + dik)
R_ = ER * S2
d.arc([gz(RZ_) - R_, gy(OM) - R_, gz(RZ_) + R_, gy(OM) + R_], -75, 75, fill=ACC, width=2)
txt(gz(RZ_) + R_ * 0.26 - 8, gy(OM) - R_ * 0.97, "FR5 pratik erişim 779", f11, ACC, "rm")
# QR yan
sbox(QZ0, QZ0 + QD, 0, QH, (248, 248, 250), INK, 3)
for r in range(GOZN):
    y0 = GOZ0 + r * GOZH
    sbox(QZ0 + 40, QZ0 + 480, y0, y0 + 190, EVC, ACC, 1)
sbox(QZ0 + 5, QZ0 + 255, 20, 370, TEK, INK, 2); slab(QZ0 + 5, QZ0 + 255, 20, 370, "ANA PANO|250 derin", f11)
sbox(QZ0 + 5, QZ0 + 273, UY0, UY0 + 423, TEK, INK, 2); slab(QZ0 + 5, QZ0 + 273, UY0, UY0 + 423, "ROBOT|KONTROL|268 derin", f11)
txt(gz(QZ0 + QD / 2), gy(QH) - 16, "QR 520 derin", f13, INK)
txt(gz(QZ0) - 6, gy(QH) + 20, "robot tarafı", f11, GRAY, "rm"); txt(gz(QZ0 + QD) + 6, gy(QH) + 20, "müşteri tarafı", f11, GRAY, "lm")
# erişim bandı (robot yüzünde)
for yy in BANT:
    d.line([(gz(QZ0) - 60, gy(yy)), (gz(QZ0) + 8, gy(yy))], fill=RED, width=3)
d.line([(gz(QZ0) - 40, gy(BANT[0])), (gz(QZ0) - 40, gy(BANT[1]))], fill=RED, width=2)
txt(gz(QZ0) - 48, gy(1400) - 10, "robotun eriştiği bant", f11, RED, "rm")
txt(gz(QZ0) - 48, gy(1400) + 10, "%.0f – %.0f" % BANT, f13, RED, "rm")
d.line([(gz(QZ0 + QD) + 20, gy(GOZ0)), (gz(QZ0 + QD) + 20, gy(GOZ0 + GOZN * GOZH))], fill=ACC, width=2)
txt(gz(QZ0 + QD) + 30, gy(GOZ0 + 600), "göz 400 – 1600", f13, ACC, "lm")
txt(gz(QZ0 + QD) + 30, gy(GOZ0 + 560), "pay: altta %.0f · üstte %.0f" % (GOZ0 - BANT[0], BANT[1] - (GOZ0 + GOZN * GOZH)), f11, ACC, "lm")
txt(gz(QZ0 + QD) + 30, gy(UY0 + 210), "robot kutusu ALTTA olsaydı: göz 448 – 1648 → üst göz erişim dışı (%.0f)" % BANT[1], f11, RED, "lm")
txt(gz(QZ0 + QD) + 30, gy(200), "altta ana pano + UPS + kilit kartı (robot tarafından servis)", f11, INK, "lm")
# ölçüler yan
d.line([(gz(0), gy(0) + 40), (gz(RZ_), gy(0) + 40)], fill=INK, width=2); txt((gz(0) + gz(RZ_)) / 2, gy(0) + 26, "330 ray", f11, INK)
d.line([(gz(RZ_), gy(0) + 40), (gz(QZ0), gy(0) + 40)], fill=INK, width=2); txt((gz(RZ_) + gz(QZ0)) / 2, gy(0) + 26, "340", f11, INK)
for zz in (0, RZ_, QZ0, QZ0 + QD):
    d.line([(gz(zz), gy(0) + 32), (gz(zz), gy(0) + 48)], fill=INK, width=2)
txt(gz(QZ0 + QD / 2), gy(0) + 26, "520", f11, INK)
txt(gz(0), gy(0) + 66, "hat yüzü", f11, GRAY)

# ============================ 3 · TEZGÂH YAN ============================
TZ0 = 2700.0
txt(gz(TZ0), gy(2100) - 60, "3 · TEZGÂH YAN", f22, ACC, "la")
sbox(TZ0, TZ0 + 450, 100, TH - 30, (250, 246, 238), INK, 2)
sbox(TZ0 - 15, TZ0 + 460, TH - 30, TH, (215, 205, 190), INK, 2)
sbox(TZ0 + 20, TZ0 + 430, TH - 200, TH - 45, (255, 250, 236), INK, 2); slab(TZ0 + 20, TZ0 + 430, TH - 200, TH - 45, "çekmece 410 derin", f11)
sbox(TZ0 + 60, TZ0 + 360, 110, 560, (236, 236, 236), INK, 2); slab(TZ0 + 60, TZ0 + 360, 110, 560, "çöp 30 L", f11)
sbox(TZ0 + 30, TZ0 + 450, 0, 100, SOFT, LINE, 1)
d.line([(gz(TZ0 + 450), gy(0)), (gz(TZ0 + 450), gy(2000))], fill=LINE, width=4); txt(gz(TZ0 + 460), gy(1900), "duvar", f11, GRAY, "lm")
d.line([(gz(TZ0 + 450), gy(1650)), (gz(TZ0 + 380), gy(1650))], fill=INK, width=4); txt(gz(TZ0 + 370), gy(1650), "askı 1650", f11, INK, "rm")
d.line([(gz(TZ0), gy(0) + 40), (gz(TZ0 + 450), gy(0) + 40)], fill=INK, width=2); txt(gz(TZ0 + 225), gy(0) + 26, "450", f11, INK)

# ============================ başlık ============================
txt(OX, 60, "AUTOKITCH  ·  İSTASYON + QR DOLABI + TEZGÂH  ·  teknik resim v1  ·  QR 860 × 520 × 2050, göz 400–1600, teknik altta ve üstte", f30, INK, "la")
txt(OX, 112, "sabit ölçüler: robot kontrol 475 × 423 × 268 · ana pano 400 × 350 × 250 · UPS 115 × 185 × 213 · göz 380 × 190 × 440 · robot omuz 970, pratik erişim 779 · tezgâh, çöp ve askı öneri · mm · 27 Eylül 2026", f15, GRAY, "la")
d.line([(OX, 150), (W_PX - 80, 150)], fill=LINE, width=3)
ad = "QR_TEZGAH_v1"
im.save(os.path.join(KLASOR, ad + ".png"), optimize=True)
im.save(os.path.join(KLASOR, ad + ".pdf"), "PDF", resolution=150.0)
print("yazildi", ad, "bant %.0f-%.0f" % BANT)
