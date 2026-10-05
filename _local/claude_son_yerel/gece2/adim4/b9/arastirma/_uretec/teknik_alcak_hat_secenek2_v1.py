# -*- coding: utf-8 -*-
"""AUTOKITCH · ALÇAK HAT ÖNERİSİ v2 (27 Eyl 2026) — ÖN GÖRÜNÜŞ (yalnız teknik resim, model yok).
Kemal: "kırmızı çizdiğim hattan böl, alttaki çekmece kısmını ona göre ayarla, sağa doğru ekle · içecek/lahmacun/pide sola, soğutma + kaşar/sucuk
sağa sığar mı · bulaşığın arkasındakilere nasıl erişeceğiz, sağdaki kutu yerine koy · arkada teknik, önde erişilen · sadece teknik resim".
HESAP (cekmece_ara2.py, tam arama): alt bant üstü L = 824 (kırmızı çizgi ≈ 809; fırın altına 2 soğuk sütunla bütün çekmecelerin sığdığı en düşük L)
→ her şey 236 aşağı → hat 1794. Fırın, bant kotu yüzünden alt bandın hep 104 altında oturur (disk = L + 108, fırın bandı = fırın altı + 210).
Soğutma + kaşar/sucuk (Secop + depo, yığın 540) fırın altına SIĞMAZ (orada 430 yer var; fırın ısısı da yoğuşturucuya kötü) → fırının hemen solunda, en sağdaki tam boy sütunda (K4)."""
import os
from PIL import Image, ImageDraw, ImageFont

KLASOR = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE".replace("WEBSITE", "WEBS\u0130TE")
S = 0.8
OX, OY = 600, 300
W_PX, H_PX = int(OX + 5430 * S + 780), int(OY + 2030 * S + 470)
L = 824.0
DLT = 1060.0 - L                                  # 236
FIRIN_ALT, DISK, BANT_F, K_BANT, TEPSI, TOP = L - 104.0, L + 108.0, L + 106.0, L + 104.0, 1104.0 - DLT, L + 970.0
BG, INK, GRAY, LINE, ACC, RED = (255, 255, 255), (26, 26, 28), (130, 130, 138), (70, 70, 76), (0, 86, 184), (198, 42, 32)
DOLAP, PUC, SICAK, TURUNCU, KARTON, SOFT, EVC, YESIL = (14, 120, 90), (255, 240, 200), (255, 226, 214), (200, 90, 30), (236, 214, 176), (232, 232, 238), (220, 235, 255), (40, 150, 80)


def F(sz, b=False):
    try:
        return ImageFont.truetype("arialbd.ttf" if b else "arial.ttf", sz)
    except Exception:
        return ImageFont.load_default()


f11, f13, f15, f18, f30 = F(15), F(17), F(19), F(22), F(32, True)
im = Image.new("RGB", (W_PX, H_PX), BG)
d = ImageDraw.Draw(im)
fx = lambda x: OX + x * S
fy = lambda y: OY + (2030.0 - y) * S


def box(x0, x1, y0, y1, fill=None, out=LINE, w=2):
    d.rectangle([fx(x0), fy(y1), fx(x1), fy(y0)], fill=fill, outline=out, width=w)


def kesik(x0, x1, y0, y1, c=GRAY, w=2, dash=10, gap=6):
    for (a, b) in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
        X0, Y0, X1, Y1 = fx(a[0]), fy(a[1]), fx(b[0]), fy(b[1])
        Lg = ((X1 - X0) ** 2 + (Y1 - Y0) ** 2) ** 0.5
        i = 0
        while i * (dash + gap) < Lg:
            t0, t1 = i * (dash + gap) / Lg, min(1.0, (i * (dash + gap) + dash) / Lg)
            d.line([(X0 + (X1 - X0) * t0, Y0 + (Y1 - Y0) * t0), (X0 + (X1 - X0) * t1, Y0 + (Y1 - Y0) * t1)], fill=c, width=w)
            i += 1


def cizgi_kesik(x0, x1, y, c, w=2, dash=16, gap=8):
    X0, X1, Y = fx(x0), fx(x1), fy(y)
    x = X0
    while x < X1:
        d.line([(x, Y), (min(x + dash, X1), Y)], fill=c, width=w); x += dash + gap


def txt(x, y, s, f=f13, c=INK, a="mm"):
    d.text((x, y), s, font=f, fill=c, anchor=a)


def lab(x0, x1, y0, y1, s, f=f13, c=INK):
    satir = s.split("|")
    cy = (fy(y0) + fy(y1)) / 2 - (len(satir) - 1) * 10
    for i, t in enumerate(satir):
        txt((fx(x0) + fx(x1)) / 2, cy + i * 20, t, f, c if i == 0 else GRAY)


# ---- bugünkü siluet 2030 · Kemal'in kırmızı çizgisi 809 · yeni alt bant 824
kesik(0, 5430, 0, 2030, RED, 2, 14, 8)
txt(fx(5430) + 12, fy(2030), "bugün 2030", f15, RED, "lm")
for x0, x1 in ((0, 3810), (3810, 4000), (4000, 4600), (4600, 5430)):
    box(x0 + 30, x1 - 30, 0, 123, SOFT, LINE, 1)
# ================= B · çekmece dolabı 0–3810 (tam boy 0–2500 üstü L · fırın altı 2500–3810) =================
box(0, 2500, 123, L, (246, 248, 247), LINE, 3)
box(2500, 3810, 123, FIRIN_ALT, (246, 248, 247), LINE, 3)
PITCH = dict(P=108.0, L=93.0, T=104.0, I=159.0)
AD = dict(P="PİDE", L="LAHMACUN", T="TATLI", I="İÇECEK")
KOL = [("K1", 62.5, 682.5, "PPLLLL"), ("K2", 717.5, 1337.5, "PPLLLL"), ("K3", 1372.5, 1992.5, "PPLLLL"),
       ("K5", 2535.0, 3155.0, "PII"), ("K6", 3190.0, 3810.0 - 35.0, "PII")]
for ad, a, b, seq in KOL:
    y = 167.5
    for k in seq:
        p = PITCH[k]
        box(a, b, y, y + p - 3.0, (255, 250, 236) if k in "TI" else BG, DOLAP, 2)
        txt((fx(a) + fx(b)) / 2, (fy(y) + fy(y + p - 3.0)) / 2, AD[k], f11, DOLAP if k in "PL" else TURUNCU)
        y += p
    txt((fx(a) + fx(b)) / 2, fy(123) + 18, ad, f13, GRAY)
box(2011.5, 2500.0, 128.5, 400.5, None, GRAY, 1); lab(2011.5, 2500.0, 128.5, 400.5, "SOĞUTMA Secop|arkadan servis", f11, INK)
box(2011.5, 2500.0, 423.0, 669.0, None, GRAY, 1); lab(2011.5, 2500.0, 423.0, 669.0, "KAŞAR + SUCUK|DEPO 2 gün", f11, INK)
box(2011.5, 2500.0, 672.5, 773.5, (255, 250, 236), DOLAP, 2); txt((fx(2011.5) + fx(2500)) / 2, (fy(672.5) + fy(773.5)) / 2, "TATLI", f11, TURUNCU)
txt((fx(2011.5) + fx(2500)) / 2, fy(123) + 18, "K4", f13, GRAY)
box(2517.0, 3793.0, FIRIN_ALT - 60.0, FIRIN_ALT, PUC, GRAY, 1)
txt((fx(2517) + fx(3793)) / 2, (fy(FIRIN_ALT - 60) + fy(FIRIN_ALT)) / 2, "PU 60 · fırın altı ısı kalkanı", f11, GRAY)
txt(fx(1250), fy(L) + 22, "B · ÇEKMECE DOLABI 3810 (bugün 2500) · üstü 824 (bugün 1060) · +3 °C", f15, DOLAP)
# fırın altı şerit 3810–4000: 2 içecek kolisi yan yatık (123 × 267 × 400)
box(3810, 4000, 123, FIRIN_ALT, (250, 250, 252), LINE, 3)
for i in range(2):
    box(3843, 3966, 130 + i * 270.0, 397 + i * 270.0, KARTON, LINE, 2)
lab(3810, 4000, 560, 700, "İÇECEK|2 koli|yan", f11)
# ================= A (üstü teknik) + C =================
box(0, 700, L, TOP, (250, 250, 252), LINE, 3); lab(0, 700, L + 60, L + 380, "A · AÇICI|(içi aynı)", f15)
box(40, 660, TOP - 560, TOP - 330, (255, 244, 230), LINE, 2); lab(40, 660, TOP - 560, TOP - 330, "TEMİZLİK · önde|2 × 5 L · bez · eldiven · poşet", f13)
kesik(40, 515, TOP - 320, TOP - 52, GRAY, 2); lab(40, 515, TOP - 320, TOP - 180, "ROBOT KONTROL · arkada|475 × 268 (V)", f11, GRAY)
kesik(90, 490, TOP - 170, TOP - 20, GRAY, 1); lab(90, 490, TOP - 170, TOP - 20, "ANA PANO · arkada (üstte)", f11, GRAY)
kesik(530, 645, TOP - 320, TOP - 107, GRAY, 2); lab(530, 645, TOP - 320, TOP - 107, "UPS", f11, GRAY)
box(700, 2500, L, TOP, (250, 250, 252), LINE, 3)
_pu = [(733, 1277 - DLT), (733, 2028 - DLT), (1520, 2028 - DLT), (1520, 1720 - DLT), (2467, 1720 - DLT), (2467, 1277 - DLT)]
d.polygon([(fx(x_), fy(y_)) for x_, y_ in _pu], outline=(230, 190, 90))
lab(700, 2500, 1150, 1500, "C · TOPPING|içi aynı (uno v11) · 236 aşağı · disk 932", f15)
d.line([(fx(700), fy(DISK)), (fx(2500), fy(DISK))], fill=ACC, width=3)
# ================= F =================
box(2500, 4000, FIRIN_ALT, FIRIN_ALT + 517.0, SICAK, TURUNCU, 3)
lab(2500, 4000, FIRIN_ALT + 100, FIRIN_ALT + 420, "F · TP10 FIRIN 1500 · 79 öne|gövde 720–1237 · bant 930", f15)
d.line([(fx(2560), fy(BANT_F)), (fx(3996), fy(BANT_F))], fill=TURUNCU, width=4)
RAF = FIRIN_ALT + 517.0 + 43.0
box(2510, 3990, RAF - 4.0, RAF, INK, INK, 1)
box(2520, 3324, RAF, RAF + 512.0, KARTON, LINE, 2); lab(2520, 3324, RAF, RAF + 512.0, "PİZZA KUTUSU YEDEĞİ 320|(aynı)", f13)
box(3600, 3980, RAF, RAF + 510.0, EVC, ACC, 2); lab(3600, 3980, RAF, RAF + 510.0, "KOMPRESÖR|(aynı)", f13, ACC)
# ================= K · taban: bulaşık yerden =================
box(4000, 4600, 123, TOP, (250, 250, 252), LINE, 3)
box(4000, 4600, L - 3.0, L, INK, INK, 1)
box(4070, 4530, 10, 710, (245, 247, 250), INK, 3); lab(4070, 4530, 250, 600, "BULAŞIK MAKİNESİ · önde|MEIKO M-iClean US 460 × 600 × 700|yerden (dolap tabanı yok) · ayak 10", f13)
d.line([(fx(4010), fy(K_BANT)), (fx(4597), fy(K_BANT))], fill=ACC, width=4)
box(4185, 4415, 1290 - DLT, 1702 - DLT, None, INK, 2); lab(4185, 4415, 1290 - DLT, 1702 - DLT, "KESİCİ + SPREY|(aynı)", f11)
kesik(4054, 4226, 1635 - DLT, 1980 - DLT, RED, 2); lab(4054, 4226, 1635 - DLT, 1980 - DLT, "YAĞ 3 L", f11, RED)
kesik(4300, 4565, 1640 - DLT, 2025 - DLT, GRAY, 2); lab(4300, 4565, 1640 - DLT, 2025 - DLT, "PANO|arkada", f11, GRAY)
txt(fx(4300), fy(TOP) + 24, "K · KESME + SPREY", f15)
# ================= E =================
box(4600, 5430, 123, TOP, (250, 250, 252), LINE, 3)
kesik(4608, 5412, 240, 1148 - DLT, GRAY, 2); lab(4608, 5412, 600, 1148 - DLT, "KUTU ŞARJÖRÜ (arkada) 240–912|420 kutu (bugün 567)", f11, RED)
box(4602, 5428, 1085 - DLT, 1330 - DLT, (253, 244, 243), RED, 3); lab(4602, 5428, 1085 - DLT, 1330 - DLT, "KUTULAMA AĞZI 849–1094 · tepsi 868", f13, RED)
box(4604, 5400, 790 - DLT - 4.0, 790 - DLT, INK, INK, 1); txt(fx(5000), fy(790 - DLT) - 14, "alt raf 554", f11, INK)
for i in range(3):
    box(4610, 5010, 130 + i * 123, 252 + i * 123, KARTON, LINE, 2)
txt(fx(4810), fy(130 + 3 * 123) - 14, "İÇECEK 3 koli · önde", f11, INK)
for i in range(2):
    box(5030 + i * 132, 5160 + i * 132, 130, 420, (225, 238, 250), ACC, 2)
lab(5030, 5292, 130, 420, "DETERJAN|+ parlatıcı|önde", f11, ACC)
box(4620, 5410, 1300 - DLT + 50, TOP - 10, None, GRAY, 1); lab(4620, 5410, 1300 - DLT + 50, TOP - 10, "BESLEYİCİ · PİSTON · PANO (arkada)|(aynı, 236 aşağı)", f11, GRAY)
txt(fx(5015), fy(TOP) + 24, "E · KUTU KATLAMA", f15)
# ================= tek alt bant çizgisi + Kemal'in çizgisi =================
cizgi_kesik(0, 5430, L, YESIL, 3)
txt(fx(-20), fy(L), "ALT BANT 824", f15, YESIL, "rm")
cizgi_kesik(0, 5430, 809.0, RED, 1, 6, 6)
txt(fx(-20), fy(809.0) + 16, "senin çizgin ≈ 809", f11, RED, "rm")


def olcu_v(x, y0, y1, s, c=INK, sag=True):
    d.line([(x, fy(y0)), (x, fy(y1))], fill=c, width=2)
    for yy in (y0, y1):
        d.line([(x - 8, fy(yy)), (x + 8, fy(yy))], fill=c, width=2)
    txt(x + (14 if sag else -14), (fy(y0) + fy(y1)) / 2, s, f18, c, "lm" if sag else "rm")


olcu_v(fx(0) - 170, 0, TOP, "1794", INK, False)
olcu_v(fx(0) - 290, 0, 2030, "2030 (bugün)", RED, False)
olcu_v(fx(5430) + 70, TOP, 2030, "−236", RED, True)
for yy, s in ((123, "123"), (FIRIN_ALT, "720 fırın altı"), (L, "824 alt bant (B · K tabanı)"), (TEPSI, "868 kutu tepsisi"), (DISK, "928–932 süreç (K bandı · fırın bandı · disk)"), (TOP, "1794")):
    d.line([(fx(5430) + 150, fy(yy)), (fx(5430) + 170, fy(yy))], fill=INK, width=2)
    txt(fx(5430) + 178, fy(yy), s, f13, INK, "lm")
for x0, x1, s in ((0, 700, "700"), (700, 2500, "1800"), (2500, 4000, "1500"), (4000, 4600, "600"), (4600, 5430, "830")):
    d.line([(fx(x0), fy(TOP) - 60), (fx(x1), fy(TOP) - 60)], fill=INK, width=2)
    for xx in (x0, x1):
        d.line([(fx(xx), fy(TOP) - 70), (fx(xx), fy(TOP) - 50)], fill=INK, width=2)
    txt((fx(x0) + fx(x1)) / 2, fy(TOP) - 74, s, f18, INK, "md")
d.line([(fx(0), fy(0) + 60), (fx(3810), fy(0) + 60)], fill=DOLAP, width=2)
txt(fx(1905), fy(0) + 82, "B dolabı 3810 (K1 · K2 · K3 · K4 · K5 · K6)", f15, DOLAP)
d.line([(fx(0), fy(0) + 110), (fx(5430), fy(0) + 110)], fill=INK, width=2)
txt(fx(2715), fy(0) + 134, "HAT 5430 (aynı)", f18, INK)
txt(OX, 60, "AUTOKITCH  ·  ALÇAK HAT  ·  SEÇENEK 2 (kırmızı çizgi)  ·  ÖN GÖRÜNÜŞ  ·  tek alt bant 824  ·  hat 2030 → 1794 (−236)", f30, INK, "la")
txt(OX, 112, "önde erişilenler (çekmece · içecek · bulaşık · deterjan · temizlik) · arkada teknik (Secop · pano · UPS · robot kontrol) arka servis kapağından · düz = önde · kesik = arkada · ölçüler mm · 27 Eylül 2026", f15, GRAY, "la")
d.line([(OX, 150), (W_PX - 80, 150)], fill=LINE, width=3)
im.save(os.path.join(KLASOR, "ALCAK_HAT_SECENEK2_v1.png"), optimize=True)
im.save(os.path.join(KLASOR, "ALCAK_HAT_SECENEK2_v1.pdf"), "PDF", resolution=150.0)
print("yazildi", im.size)
