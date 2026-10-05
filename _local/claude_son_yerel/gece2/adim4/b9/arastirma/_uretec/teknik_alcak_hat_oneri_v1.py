# -*- coding: utf-8 -*-
"""AUTOKITCH · ALÇAK HAT ÖNERİSİ v1 (27 Eyl 2026) — ÖN GÖRÜNÜŞ (öneri paftası, 3B'den önce).
Kemal: "boyutu küçültmemiz lazım: bulaşık makinesini sağa, mavi çizdiklerimi kesme yerine ve sağdaki boş yerlere; tatlı-içecek üst çekmecelerini
bulaşık makinesinin yerine → dolap daha geniş ama alçak, her şey aşağı iner; yükseklik olabilecek en az olsun; sarı boşlukları mantıkla doldur".
HESAP (cekmece_ara.py, tam arama): çekmece adımı = yükseklik + 2×15 + 3 (pide 108 · lahmacun 93 · tatlı 104 · içecek 159); K4 tabanı 505 (Secop + depo);
fırın altındaki sütun 164 kısa (fırın gövdesi B üstünden 104 aşağıda + 60 ısı yalıtımı). Fırın altına 1 sütun: yığın 683 → B üstü 913 → her şey 147 AŞAĞI → hat 1883.
(2 sütun: B 839, −221, hat 1809 — ama pano/UPS/robot kontrol + içecek aşağıya sığmıyor; öneri 1 sütun.)"""
import os
from PIL import Image, ImageDraw, ImageFont

KLASOR = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE".replace("WEBSITE", "WEBS\u0130TE")
IMG = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\otonom\hat\img".replace("WEBSITE", "WEBS\u0130TE")
S = 0.8
OX, OY = 420, 300
W_PX, H_PX = int(OX + 5430 * S + 760), int(OY + 2030 * S + 470)
DLT = 147.0
H_B, FIRIN_ALT, BANT_F, DISK, K_BANT, TEPSI, TOP = 913.0, 809.0, 1019.0, 1021.0, 1017.0, 957.0, 1883.0
BG, INK, GRAY, LINE, ACC, RED = (255, 255, 255), (26, 26, 28), (130, 130, 138), (70, 70, 76), (0, 86, 184), (198, 42, 32)
DOLAP, PUC, SICAK, TURUNCU, KARTON, SOFT, EVC = (14, 120, 90), (255, 240, 200), (255, 226, 214), (200, 90, 30), (236, 214, 176), (232, 232, 238), (220, 235, 255)


def F(sz, b=False):
    for n in (("arialbd.ttf",) if b else ("arial.ttf",)):
        try:
            return ImageFont.truetype(n, sz)
        except Exception:
            pass
    return ImageFont.load_default()


f11, f13, f15, f18, f22, f30, f44 = F(15), F(17), F(19), F(22), F(26, True), F(32, True), F(46, True)
im = Image.new("RGB", (W_PX, H_PX), BG)
d = ImageDraw.Draw(im)
fx = lambda x: OX + x * S
fy = lambda y: OY + (2030.0 - y) * S


def box(x0, x1, y0, y1, fill=None, out=LINE, w=2):
    d.rectangle([fx(x0), fy(y1), fx(x1), fy(y0)], fill=fill, outline=out, width=w)


def kesik(x0, x1, y0, y1, c=GRAY, w=2, dash=10, gap=6):
    for (a, b) in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
        X0, Y0, X1, Y1 = fx(a[0]), fy(a[1]), fx(b[0]), fy(b[1])
        L = ((X1 - X0) ** 2 + (Y1 - Y0) ** 2) ** 0.5
        n = int(L // (dash + gap)) + 1
        for i in range(n):
            t0, t1 = i * (dash + gap) / L, min(1.0, (i * (dash + gap) + dash) / L)
            if t0 >= 1: break
            d.line([(X0 + (X1 - X0) * t0, Y0 + (Y1 - Y0) * t0), (X0 + (X1 - X0) * t1, Y0 + (Y1 - Y0) * t1)], fill=c, width=w)


def txt(x, y, s, f=f13, c=INK, a="mm"):
    d.text((x, y), s, font=f, fill=c, anchor=a)


def lab(x0, x1, y0, y1, s, f=f13, c=INK):
    satir = s.split("|")
    cy = (fy(y0) + fy(y1)) / 2 - (len(satir) - 1) * 10
    for i, t in enumerate(satir):
        txt((fx(x0) + fx(x1)) / 2, cy + i * 20, t, f, c if i == 0 else GRAY)


# ---- bugünkü siluet (2030) kesik kırmızı
kesik(0, 5430, 0, 2030, RED, 2, 14, 8)
txt(fx(5430) + 12, fy(2030), "bugün 2030", f15, RED, "lm")
# ---- plint
for x0, x1 in ((0, 3190), (3190, 4000), (4000, 4600), (4600, 5430)):
    box(x0 + 30, x1 - 30, 0, 123, SOFT, LINE, 1)
# ================= B · çekmece dolabı (0–3190, 123–913) =================
box(0, 3190, 123, H_B, (246, 248, 247), LINE, 3)
PITCH = dict(H=108.0, L=93.0, T=104.0, I=159.0)
AD = dict(H="PİDE", L="LAHMACUN", T="TATLI", I="İÇECEK")
KOL = [("K1", 62.5, 682.5, "HHLLLLL"), ("K2", 717.5, 1337.5, "HHLLLLL"), ("K3", 1372.5, 1992.5, "HHHLTI"), ("K5", 2535.0, 3155.0, "HLII")]
for ad, a, b, seq in KOL:
    y = 167.5
    for k in seq:
        p = PITCH[k]
        box(a, b, y, y + p - 3.0, (255, 250, 236) if k in "TI" else BG, DOLAP, 2)
        txt((fx(a) + fx(b)) / 2, (fy(y) + fy(y + p - 3.0)) / 2, AD[k], f11, DOLAP if k in "HL" else TURUNCU)
        y += p
    txt((fx(a) + fx(b)) / 2, fy(123) + 18, ad, f13, GRAY)
# K4
box(2011.5, 2500.0, 128.5, 400.5, None, GRAY, 1); lab(2011.5, 2500.0, 128.5, 400.5, "SOĞUTMA|Secop (B)", f11, INK)
box(2011.5, 2500.0, 423.0, 669.0, None, GRAY, 1); lab(2011.5, 2500.0, 423.0, 669.0, "KAŞAR + SUCUK|DEPO 2 gün", f11, INK)
box(2011.5, 2500.0, 687.5, 843.5, (255, 250, 236), DOLAP, 2); txt((fx(2011.5) + fx(2500)) / 2, (fy(687.5) + fy(843.5)) / 2, "İÇECEK dar", f11, TURUNCU)
txt((fx(2011.5) + fx(2500)) / 2, fy(123) + 18, "K4", f13, GRAY)
# K5 üstü: ısı yalıtımı (fırın altı)
box(2517.0, 3172.0, 749.0, FIRIN_ALT, PUC, GRAY, 1); txt((fx(2517) + fx(3172)) / 2, (fy(749) + fy(FIRIN_ALT)) / 2, "PU 60 · fırın altı ısı kalkanı", f11, GRAY)
txt(fx(1595), fy(H_B) + 22, "B · ÇEKMECE DOLABI 3190 (bugün 2500) · üstü 913 (bugün 1060) · +3 °C", f15, DOLAP)
# ================= A + C (B'nin üstünde, 147 aşağı) =================
box(0, 700, H_B, TOP, (250, 250, 252), LINE, 3); lab(0, 700, H_B + 300, TOP - 200, "A · AÇICI|içi aynı · 147 aşağı", f15)
box(700, 2500, H_B, TOP, (250, 250, 252), LINE, 3)
box(790, 2410, 1277 - DLT, 2028 - DLT, None, PUC, 3)
lab(700, 2500, 1300, 1700, "C · TOPPING|içi aynı (uno v11) · 147 aşağı · disk 1021", f15)
d.line([(fx(700), fy(DISK)), (fx(2500), fy(DISK))], fill=ACC, width=3)
# ================= F · fırın + üstü + dolap artığı =================
box(2500, 4000, FIRIN_ALT, FIRIN_ALT + 517.0, SICAK, TURUNCU, 3)
lab(2500, 4000, FIRIN_ALT + 100, FIRIN_ALT + 420, "F · TP10 FIRIN 1500 · 79 öne|gövde 809–1326 · bant 1019", f15)
d.line([(fx(2560), fy(BANT_F)), (fx(3996), fy(BANT_F))], fill=TURUNCU, width=4)
RAF = FIRIN_ALT + 517.0 + 43.0
box(2510, 3990, RAF - 4.0, RAF, INK, INK, 1)
box(2520, 3324, RAF, RAF + 512.0, KARTON, LINE, 2); lab(2520, 3324, RAF, RAF + 512.0, "PİZZA KUTUSU YEDEĞİ 320|fırın üstü sol (aynı)", f13)
box(3600, 3980, RAF, RAF + 510.0, EVC, ACC, 2); lab(3600, 3980, RAF, RAF + 510.0, "KOMPRESÖR|(aynı)", f13, ACC)
kesik(2500, 4000, FIRIN_ALT + 527.0, TOP, GRAY, 1)
# F dolap artığı (3190–4000, 126–806): önde içecek 3 + 2 · arkada pano / UPS / robot kontrol
box(3190, 4000, 123, FIRIN_ALT, (250, 250, 252), LINE, 3)
for i in range(3):
    box(3195, 3595, 130 + i * 123, 252 + i * 123, KARTON, LINE, 2)
for i in range(2):
    box(3595, 3995, 130 + i * 123, 252 + i * 123, KARTON, LINE, 2)
txt((fx(3195) + fx(3995)) / 2, fy(130 + 3 * 123) - 16, "İÇECEK YEDEĞİ 5 koli (3 + 2) · 120 · önde", f13, INK)
kesik(3200, 3675, 530, 798, GRAY, 2); lab(3200, 3675, 530, 798, "ROBOT KONTROL · arkada|UR sınıfı 475 × 423 × 268 (V)", f11, GRAY)
kesik(3690, 3805, 530, 743, GRAY, 2); lab(3690, 3805, 530, 743, "UPS", f11, GRAY)
kesik(3820, 3990, 440, 790, GRAY, 2); lab(3820, 3990, 440, 790, "ANA|PANO|arkada", f11, GRAY)
# ================= K · kesme + sprey (147 aşağı) · taban: bulaşık =================
box(4000, 4600, 123, TOP, (250, 250, 252), LINE, 3)
box(4000, 4600, H_B - 3.0, H_B, INK, INK, 1)
box(4070, 4530, 126, 826, (245, 247, 250), INK, 3); lab(4070, 4530, 300, 700, "BULAŞIK MAKİNESİ|MEIKO M-iClean US|460 × 600 × 700", f13)
kesik(4020, 4580, 126, 420, GRAY, 1); txt(fx(4300), fy(160), "deterjan + parlatıcı (arkada)", f11, GRAY)
d.line([(fx(4010), fy(K_BANT)), (fx(4597), fy(K_BANT))], fill=ACC, width=4)
box(4185, 4415, 1143, 1555, None, INK, 2); lab(4185, 4415, 1143, 1555, "KESİCİ + SPREY|kafası (aynı)", f11)
kesik(4054, 4226, 1488, 1833, RED, 2); lab(4054, 4226, 1488, 1833, "YAĞ|3 L", f11, RED)
kesik(4300, 4565, 1493, 1878, GRAY, 2); lab(4300, 4565, 1493, 1878, "PANO", f11, GRAY)
txt(fx(4300), fy(TOP) + 24, "K · KESME + SPREY", f15)
# ================= E · kutu katlama (147 aşağı; şarjör kısalır) =================
box(4600, 5430, 123, TOP, (250, 250, 252), LINE, 3)
kesik(4608, 5412, 240, 1001, GRAY, 2); lab(4608, 5412, 800, 1001, "KUTU ŞARJÖRÜ (arkada) 240–1001|475 kutu (bugün 567)", f11, RED)
box(4602, 5428, 938, 1183, (253, 244, 243), RED, 3); lab(4602, 5428, 938, 1183, "KUTULAMA AĞZI 938–1183 · tepsi 957", f13, RED)
box(4604, 5400, 639, 643, INK, INK, 1); txt(fx(5000), fy(643) - 14, "alt raf 643", f11, INK)
box(4610, 4900, 130, 480, (255, 244, 230), LINE, 2); lab(4610, 4900, 130, 480, "TEMİZLİK|2 × 5 L|bez · eldiven", f11)
kesik(4905, 5395, 130, 600, (60, 150, 90), 2); lab(4905, 5395, 130, 600, "BOŞ|≈ 490 × 470 × 348", f13, (60, 150, 90))
box(4620, 5410, 1300, TOP - 10, None, GRAY, 1); lab(4620, 5410, 1300, TOP - 10, "BESLEYİCİ · PİSTON · PANO|(aynı, 147 aşağı)", f11, GRAY)
txt(fx(5015), fy(TOP) + 24, "E · KUTU KATLAMA", f15)
# ================= ölçüler + kotlar =================
def olcu_v(x, y0, y1, s, c=INK, sag=True):
    d.line([(x, fy(y0)), (x, fy(y1))], fill=c, width=2)
    for yy in (y0, y1):
        d.line([(x - 8, fy(yy)), (x + 8, fy(yy))], fill=c, width=2)
    txt(x + (14 if sag else -14), (fy(y0) + fy(y1)) / 2, s, f18, c, "lm" if sag else "rm")


olcu_v(fx(0) - 60, 0, TOP, "1883", INK, False)
olcu_v(fx(0) - 130, 0, 2030, "2030 (bugün)", RED, False)
olcu_v(fx(5430) + 70, TOP, 2030, "−147", RED, True)
for yy, s in ((123, "123"), (FIRIN_ALT, "809 fırın altı"), (H_B, "913 B üstü · K tabanı"), (TEPSI, "957 kutu tepsisi"), (DISK, "1017–1021 süreç (K bandı · fırın bandı · disk)"), (TOP, "1883")):
    d.line([(fx(5430) + 150, fy(yy)), (fx(5430) + 170, fy(yy))], fill=INK, width=2)
    txt(fx(5430) + 178, fy(yy), s, f13, INK, "lm")
for x0, x1, s in ((0, 700, "700"), (700, 2500, "1800"), (2500, 4000, "1500"), (4000, 4600, "600"), (4600, 5430, "830")):
    d.line([(fx(x0), fy(TOP) - 60), (fx(x1), fy(TOP) - 60)], fill=INK, width=2)
    for xx in (x0, x1):
        d.line([(fx(xx), fy(TOP) - 70), (fx(xx), fy(TOP) - 50)], fill=INK, width=2)
    txt((fx(x0) + fx(x1)) / 2, fy(TOP) - 74, s, f18, INK, "md")
d.line([(fx(0), fy(0) + 60), (fx(3190), fy(0) + 60)], fill=DOLAP, width=2)
txt(fx(1595), fy(0) + 82, "B dolabı 3190 (K1 · K2 · K3 · K4 · K5)", f15, DOLAP)
d.line([(fx(0), fy(0) + 110), (fx(5430), fy(0) + 110)], fill=INK, width=2)
txt(fx(2715), fy(0) + 134, "HAT 5430 (aynı)", f18, INK)
# ---- başlık
txt(OX, 60, "AUTOKITCH  ·  ALÇAK HAT ÖNERİSİ v1  ·  ÖN GÖRÜNÜŞ  ·  B çekmeceleri fırın altına (1 sütun)  ·  hat 2030 → 1883 (−147)", f30, INK, "la")
txt(OX, 112, "tatlı + içecek çekmeceleri B'nin sağına (fırın altı K5) · bulaşık K tabanına · pano / UPS / robot kontrol fırın dolabının arkasına · içecek yedeği önde · temizlik E altına · her şey 147 aşağı · ölçüler mm · 27 Eylül 2026", f15, GRAY, "la")
d.line([(OX, 150), (W_PX - 80, 150)], fill=LINE, width=3)
for p, ad in ((KLASOR, "ALCAK_HAT_ONERI_v1.png"), (IMG, "ALCAK_HAT_ONERI_v1.png")):
    im.save(os.path.join(p, ad), optimize=True)
im.save(os.path.join(KLASOR, "ALCAK_HAT_ONERI_v1.pdf"), "PDF", resolution=150.0)
print("yazildi", im.size)
