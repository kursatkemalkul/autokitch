# -*- coding: utf-8 -*-
"""AUTOKITCH · İSTASYON + QR DOLABI + TEZGÂH · teknik resim v4 (27 Eyl 2026) — yalnız teknik resim, 3B yok.
v4 (Kemal: "deterjan ve parlatıcı bulaşığın yanında kalsın, arka arkaya bir sıra sığar"): bulaşığın solu önde 77 (köşe dikmesi), dikmenin
  arkasında 107 → standart 5 L bidon (~190 × 125 × 285, VARSAYIM) SIĞMAZ; bulaşığın ARKASINDA 158 derin × 537 geniş boşluk var →
  deterjan + parlatıcı arka arkaya tek sıra, raf 330 üstünde (y 330–615, z −675…−800), bağlantılar (y ≤ 310) altta kalır; hortum kısa.
  Tezgâhta yalnız temizlik 2 × 5 L + bez + çöp 10 L + kişisel çekmece.
v3 (Kemal: "bez, eldiven, temizlik, parlatıcı, deterjanı tezgâha koy; tezgâhtaki çöpü küçült; bulaşığı biraz sağa taşı, duvara yasla,
  robot çöpünü yanına koy, üstünde atılacak boşluğu olsun; robot yalnız 2 günü geçen hamuru atacak, hesapla"):
  · fırın üstündeki temizlik + bez ve şeritteki deterjan + parlatıcı → TEZGÂH (altta 4 bidon, üstte bez kutusu + çöp 10 L, en üstte kişisel çekmece)
  · deterjan + parlatıcı bulaşığa hortumla bağlı → hortum zemin kanalından K'ye (~2,5 m, MEIKO emme hortumu boyu teyit)
  · bulaşık sağ köşe dikmesine yaslandı: x 4108,5–4568,5 → solunda 77 (dikmeden) kalır, robot eli giremez
  · ROBOT ÇÖPÜ hemen yanındaki şeritte (boşaldı): 165 × 400 × 300 ≈ 15 L, 126–426; üstünde 426–785 = 359 atma boşluğu, önde yaylı klape
  · hacim: 2 gün 560 top, fire %5 = 28 top (8 pide × 220 g + 20 lahmacun × 110 g VARSAYIM) ≈ 4 kg ≈ 3,6 L katı → gevşek ≈ 6 L; ×2 pay → 12 L → 15 L kova
  · 2 günlük ritimde süre dolumu tedarik ziyaretine denk gelir: eleman tepsileri değiştirirken satılmayanı atar; robot kovası yalnız
    yırtık/düşen top + tedarik gecikirse 48 saati geçen top içindir (yazılım her topun saatini tutar — 28 Ağu "süre bekçisi")
v2 (Kemal: "biraz daha detaylı çiz, kesik çizgiler farklı renklerle, nerede ne var görelim ki taşı diyebileyim; robot kontrol aşağıda olmalı;
robot kola kutu bir kabloyla mı bağlı, kanal vs nasıl bağlanacak"):
  · makinenin içi de çizildi (Resim 1 v4 kotları, düz çizgi 788) · renk = cins, DÜZ = önde, KESİK = arkada
  · QR: robot kontrol ALTTA (20–443) + kablo kangalı · göz 450–1650 · üstte ana pano + UPS + QR kilit kartı + modem
  · erişim ölçütü düzeltildi: robot kutuyu gözün TABANINA bırakır → bilek ≈ göz tabanı + 100 (çatal + kutu, VARSAYIM);
    v1'deki "göz üst kenarı ≤ bant" fazla sıkıydı. Üst göz tabanı 1460 → bilek 1560 ≤ 1642 · alt göz tabanı 450 → bilek 550 ≥ 298.
  · kablo: Fairino kol ↔ kontrol kutusu TEK kablo (güç + haberleşme), standart 4 m, 11 m uzatma ile 15 m (inluxrobotics.eu FR5 sayfası).
    Yol: QR altı → zemin kanalı (üstü basılır kapak) koridoru geçer → ray boyunca kanal → ENERJİ ZİNCİRİ (sabit ucu ray ortasında x 2650) → robot arabası.
    Gereken ≈ 0,5 + 0,4 + 2,2 + 2,85 + 0,5 ≈ 6,5 m → 4 m YETMEZ → 15 m (artan ≈ 8,5 m QR altında kangal).
  · plan ölçüleri dükkân v13 (hat yüzü 830, fırın çıkıntısı 79, koridor 900, ince duvar 60, ön zon 840; ray ekseni hat yüzünden 330; QR y 1500–2020, x 4570–5430).
SABİT: robot kontrol 475 × 423 × 268 · ana pano 400 × 350 × 250 · UPS 115 × 185 × 213 · göz 380 × 190 × 440 · omuz 970 · pratik erişim 779.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

KLASOR = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\FULL_MAKINE"
W_PX, H_PX = 4900, 3150
BG, INK, GRAY, LINE = (255, 255, 255), (26, 26, 28), (130, 130, 138), (70, 70, 76)
SOFT = (232, 232, 238)
RENK = {
    "elektrik": ((125, 55, 175), "ELEKTRİK · pano, UPS, kilit kartı"),
    "robot": ((225, 110, 0), "ROBOT · kontrol kutusu, kablo, zincir, ray"),
    "sogutma": ((0, 140, 160), "SOĞUTMA / HAVA · Secop, kompresör, davlumbaz"),
    "su": ((0, 86, 184), "SU / TEMİZLİK · bulaşık, deterjan, temizlik"),
    "stok": ((14, 120, 90), "STOK · çekmece, yedek, kutu"),
    "mekanizma": ((90, 90, 96), "MEKANİZMA · açıcı, kesici, yağ, kutulama"),
    "cop": ((140, 85, 40), "ÇÖP"),
    "sicak": ((200, 90, 30), "FIRIN"),
}


def F(sz, b=False):
    try:
        return ImageFont.truetype("arialbd.ttf" if b else "arial.ttf", sz)
    except Exception:
        return ImageFont.load_default()


f10, f11, f13, f15, f18, f22, f30 = F(13), F(15), F(17), F(19), F(22), F(24, True), F(32, True)
im = Image.new("RGB", (W_PX, H_PX), BG)
d = ImageDraw.Draw(im)


def txt(x, y, s, f=f11, c=INK, a="mm"):
    d.text((x, y), s, font=f, fill=c, anchor=a)


def kes(pts, c, w=2, dash=10, gap=6):
    for (a, b) in zip(pts, pts[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1]); i = 0
        while L > 0 and i * (dash + gap) < L:
            t0, t1 = i * (dash + gap) / L, min(1.0, (i * (dash + gap) + dash) / L)
            d.line([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0), (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)], fill=c, width=w); i += 1


def acik(c, k=0.86):
    return tuple(int(v + (255 - v) * k) for v in c)


class Gorunus:
    def __init__(self, ox, oy, s):
        self.ox, self.oy, self.s = ox, oy, s

    def X(self, x):
        return self.ox + x * self.s

    def Y(self, y):
        return self.oy - y * self.s

    def kutu(self, x0, x1, y0, y1, cins=None, arkada=False, ad="", alt="", w=2, dolgu=True, f=f10):
        c = RENK[cins][0] if cins else LINE
        X0, X1, Y0, Y1 = self.X(x0), self.X(x1), self.Y(y1), self.Y(y0)
        if arkada:
            kes([(X0, Y0), (X1, Y0), (X1, Y1), (X0, Y1), (X0, Y0)], c, w + 1)
        else:
            d.rectangle([X0, Y0, X1, Y1], fill=acik(c) if (cins and dolgu) else None, outline=c, width=w)
        if ad:
            sat = [ad] + ([alt] if alt else [])
            cy = (Y0 + Y1) / 2 - (len(sat) - 1) * 8
            for i, t in enumerate(sat):
                txt((X0 + X1) / 2, cy + i * 16, t, f, c if i == 0 else GRAY)

    def cizgi(self, x0, y0, x1, y1, c=INK, w=2):
        d.line([(self.X(x0), self.Y(y0)), (self.X(x1), self.Y(y1))], fill=c, width=w)

    def olcu_v(self, px, y0, y1, s, c=INK, sag=True):
        d.line([(px, self.Y(y0)), (px, self.Y(y1))], fill=c, width=2)
        for yy in (y0, y1):
            d.line([(px - 6, self.Y(yy)), (px + 6, self.Y(yy))], fill=c, width=2)
        txt(px + (9 if sag else -9), (self.Y(y0) + self.Y(y1)) / 2, s, f10, c, "lm" if sag else "rm")

    def olcu_h(self, x0, x1, py, s, c=INK):
        d.line([(self.X(x0), py), (self.X(x1), py)], fill=c, width=2)
        for xx in (x0, x1):
            d.line([(self.X(xx), py - 6), (self.X(xx), py + 6)], fill=c, width=2)
        txt((self.X(x0) + self.X(x1)) / 2, py - 12, s, f10, c)


# ======================================= 1 · ÖN GÖRÜNÜŞ =======================================
g = Gorunus(300, 300 + 2080 * 0.56, 0.56)
txt(300, 240, "1 · ÖN GÖRÜNÜŞ · robot tarafından · DÜZ = önde · KESİK = arkada · renk = cins", f22, (0, 86, 184), "la")
g.cizgi(-150, 0, 7950, 0, INK, 3)
L_, TOP, DISK = 788.0, 1862.0, 1000.0
# gövdeler
for x0, x1 in ((0, 4000), (4000, 4600), (4600, 5430)):
    g.kutu(x0 + 30, x1 - 30, 0, 123, None, w=1)
g.kutu(0, 4000, 123, L_, None, w=3)
for x0, x1, ad in ((0, 700, "A · AÇICI"), (700, 2500, "C · TOPPING"), (4000, 4600, "K · KESME"), (4600, 5430, "E · KUTU")):
    g.kutu(x0, x1, L_ if x1 <= 2500 else 123, TOP, None, w=3)
    txt((g.X(x0) + g.X(x1)) / 2, g.Y(TOP) - 14, ad, f13, INK)
g.kutu(2500, 4000, L_, TOP, None, w=3); txt((g.X(2500) + g.X(4000)) / 2, g.Y(TOP) - 14, "F · FIRIN", f13, INK)
# A + C içi (dolu)
g.kutu(40, 660, L_ + 110, TOP - 30, "mekanizma", ad="açıcı · içi dolu")
g.kutu(730, 2470, L_ + 110, TOP - 30, "mekanizma", ad="TOPPING · kasetler + UNO + soğuk hacim · içi dolu")
g.cizgi(700, DISK, 2500, DISK, RENK["su"][0], 2); txt(g.X(2480), g.Y(DISK) - 10, "disk 1000", f10, GRAY, "rm")
# çekmeceli dolap
def kolon(ad, a, b, seq, ust):
    P = dict(P=108.0, L=93.0, T=104.0, I=159.0)
    AD = dict(P="pide 20", L="lahm 36", T="tatlı 12", I="içecek 48")
    y = 167.5
    for k in seq:
        g.kutu(a, b, y, y + P[k] - 3.0, "stok", ad=AD[k], w=1)
        y += P[k]
    if ust - y > 15:
        g.kutu(a + 6, b - 6, y + 3, ust, "stok", arkada=False, dolgu=False, w=1, ad="boş %.0f" % (ust - y))
    txt((g.X(a) + g.X(b)) / 2, g.Y(123) + 12, ad, f10, GRAY)


kolon("K1", 62.5, 682.5, "LLLLLL", L_ - 62.5)
kolon("K2", 717.5, 1337.5, "LLLLLL", L_ - 62.5)
kolon("K3", 1372.5, 1992.5, "PPPPP", L_ - 62.5)
g.kutu(2011.5, 2500, 128.5, 400.5, "sogutma", ad="SECOP", alt="önde")
g.kutu(2038, 2418, 140, 390, "elektrik", arkada=True)
txt((g.X(2038) + g.X(2418)) / 2, g.Y(140) - 10, "B panosu (PLC) arkada", f10, RENK["elektrik"][0])
g.kutu(2011.5, 2500, 423, 669, "stok", ad="kaşar + sucuk", alt="depo")
txt((g.X(2011.5) + g.X(2500)) / 2, g.Y(123) + 12, "K4", f10, GRAY)
kolon("K5", 2535, 3155, "PPPT", L_ - 122.5)
kolon("K6", 3190, 3775, "III", L_ - 122.5)
g.kutu(2517, 3793, L_ - 60, L_, "sicak", ad="PU 60 ısı kalkanı", w=1)
g.cizgi(3810, 126, 3810, L_, LINE, 2)
g.kutu(3822, 3988, 126, 426, "cop", ad="ROBOT", alt="ÇÖPÜ 15 L")
g.kutu(3822, 3988, 430, 740, "cop", dolgu=False, w=1, ad="atma", alt="boşluğu 359")
g.cizgi(3815, 745, 3995, 745, RENK["cop"][0], 4)
txt((g.X(3810) + g.X(4000)) / 2, g.Y(760) + 2, "klape", f10, RENK["cop"][0])
# fırın
g.kutu(2500, 4000, L_, L_ + 517, "sicak", ad="TP10 FIRIN 1500", alt="gövde 788–1305 · bant 998", f=f11)
RAF = L_ + 517 + 43
g.cizgi(2510, RAF, 3990, RAF, INK, 3)
g.kutu(2508, 3992, 1315, TOP - 3, "sogutma", arkada=True)
txt(g.X(3992), g.Y(TOP) - 34, "DAVLUMBAZ · fırın üstünün arka yarısı (kesik)", f10, RENK["sogutma"][0], "rm")
g.kutu(2520, 3324, RAF, RAF + 512, "stok", ad="PİZZA KUTUSU YEDEĞİ 320")
g.kutu(3336, 3598, RAF, RAF + 450, None, w=1, ad="boş 262", alt="(temizlik tezgâha)")
g.kutu(3600, 3980, RAF, RAF + 510, "sogutma", ad="KOMPRESÖR")
# K
g.cizgi(4000, 889, 4600, 889, INK, 3)
g.kutu(4108.5, 4568.5, 126, 826, "su")
txt((g.X(4108.5) + g.X(4568.5)) / 2, g.Y(230), "BULAŞIK MAKİNESİ", f11, RENK["su"][0]); txt((g.X(4108.5) + g.X(4568.5)) / 2, g.Y(230) + 16, "sağa yaslı", f10, GRAY)
txt((g.X(4108.5) + g.X(4568.5)) / 2, g.Y(720), "raf 330: arkada deterjan + parlatıcı", f10, RENK["su"][0])
g.kutu(4031.5, 4108.5, 126, 826, None, w=1, ad="77", alt="boş")
g.kutu(4060, 4250, 330, 615, "su", arkada=True, ad="deterjan", alt="arkada")
g.kutu(4270, 4460, 330, 615, "su", arkada=True, ad="parlatıcı", alt="arkada")
g.cizgi(4040, 327, 4560, 327, RENK["su"][0], 3)
g.cizgi(4010, 996, 4597, 996, RENK["su"][0], 3)
g.kutu(4185, 4415, 1290 - 168, 1702 - 168, "mekanizma", ad="kesici + sprey")
g.kutu(4054, 4226, 1635 - 168, 1980 - 168, "mekanizma", arkada=True, ad="yağ 3 L")
g.kutu(4300, 4565, 1640 - 168, 2025 - 168, "elektrik", arkada=True, ad="K pano")
# E
g.kutu(4602, 5428, 1085 - 168, 1330 - 168, "mekanizma", ad="kutulama ağzı", alt="tepsi 936")
g.kutu(4608, 5412, 240, 1148 - 168, "stok", arkada=True)
txt((g.X(4608) + g.X(5412)) / 2, g.Y(900) , "kutu şarjörü (arkada) · 462", f10, RENK["stok"][0])
g.cizgi(4604, 622, 5400, 622, INK, 3)
for c_ in range(2):
    for i in range(3):
        g.kutu(4612 + c_ * 402, 5012 + c_ * 402, 130 + i * 123, 252 + i * 123, "stok", w=1)
txt((g.X(4612) + g.X(5414)) / 2, g.Y(540), "içecek yedeği 6 koli · önde", f10, RENK["stok"][0])
g.kutu(4620, 5410, 1182, 1520, "mekanizma", ad="besleyici · piston")
g.kutu(4620, 5410, 1530, 1852, "elektrik", arkada=True, ad="E pano · arkada")
# ray (önde, zeminde)
g.kutu(200, 5100, 0, 60, "robot", ad="robot rayı 200–5100 (hattın önünde, zeminde) · enerji zinciri yanında", w=2)
g.olcu_v(g.X(-60), 0, TOP, "1862", INK, False)
# robot çöp
CX0 = 5580.0
# QR
QX0, QW, QH = 6000.0, 860.0, 2050.0
G0, GH, GN = 450.0, 200.0, 6
g.kutu(QX0, QX0 + QW, 0, QH, None, w=3)
g.kutu(QX0 + 20, QX0 + QW - 20, 0, 20, None, w=1)
for r in range(GN):
    y0 = G0 + r * GH
    for c_ in range(2):
        gx = QX0 + 30 + c_ * 410
        g.kutu(gx, gx + 380, y0, y0 + 190, "stok", ad="göz 380 × 190", w=1)
g.cizgi(QX0 + 20, G0 - 1.5, QX0 + QW - 20, G0 - 1.5, INK, 2)
g.cizgi(QX0 + 20, G0 + GN * GH + 1.5, QX0 + QW - 20, G0 + GN * GH + 1.5, INK, 2)
g.kutu(QX0 + 25, QX0 + 500, 20, 443, "robot", ad="ROBOT KONTROL", alt="475 × 423 × 268", f=f11)
g.kutu(QX0 + 510, QX0 + 835, 20, 300, "robot", arkada=True, ad="kablo kangalı", alt="~8,5 m artan")
UY = G0 + GN * GH + 3
g.kutu(QX0 + 25, QX0 + 425, UY + 5, UY + 355, "elektrik", ad="ANA PANO", alt="400 × 350 × 250", f=f11)
g.kutu(QX0 + 435, QX0 + 550, UY + 5, UY + 190, "elektrik", ad="UPS")
g.kutu(QX0 + 560, QX0 + 835, UY + 5, UY + 205, "elektrik", ad="QR kilit kartı", alt="+ modem")
txt((g.X(QX0) + g.X(QX0 + QW)) / 2, g.Y(QH) - 14, "QR DOLABI 860 × 520 × 2050", f13, INK)
xq = g.X(QX0 + QW) + 14
g.olcu_v(xq, 0, 20, "20")
g.olcu_v(xq, 20, G0, "430 · robot kontrol")
g.olcu_v(xq, G0, G0 + GN * GH, "1200 · 12 göz (6 × 200)")
g.olcu_v(xq, UY, QH, "397 · pano + UPS")
for yy, s_ in ((G0, "450"), (G0 + GN * GH, "1650"), (QH, "2050")):
    txt(g.X(QX0) - 6, g.Y(yy), s_, f10, INK, "rm")
# tezgâh
TX0, TW, TH = 7300.0, 600.0, 900.0
g.kutu(TX0, TX0 + TW, 0, 100, None, w=1)
g.kutu(TX0, TX0 + TW, 100, TH - 30, None, w=2)
g.kutu(TX0 - 15, TX0 + TW + 15, TH - 30, TH, None, w=2)
g.kutu(TX0 + 20, TX0 + TW - 20, TH - 200, TH - 45, "stok", ad="KİŞİSEL ÇEKMECE", alt="kilitli")
for i_, ad_ in enumerate(("temizlik", "temizlik")):
    g.kutu(TX0 + 25 + i_ * 138, TX0 + 158 + i_ * 138, 105, 405, "su", ad=ad_, alt="5 L")
g.kutu(TX0 + 300, TX0 + 575, 105, 405, None, w=1, ad="boş")
g.cizgi(TX0 + 10, 412, TX0 + TW - 10, 412, INK, 3)
g.kutu(TX0 + 25, TX0 + 283, 418, 568, "su", ad="bez · eldiven", alt="poşet")
g.kutu(TX0 + 300, TX0 + 520, 418, 668, "cop", ad="ÇÖP 10 L")
txt((g.X(TX0) + g.X(TX0 + TW)) / 2, g.Y(TH) - 14, "TEZGÂH 600 × 450 × 900", f13, INK)

g.cizgi(TX0 + 50, 1650, TX0 + TW - 50, 1650, INK, 4)
for hx in (TX0 + 120, TX0 + 300, TX0 + 480):
    g.cizgi(hx, 1650, hx, 1600, INK, 3)
txt((g.X(TX0) + g.X(TX0 + TW)) / 2, g.Y(1650) - 14, "DUVAR ASKISI 1650", f10, INK)
g.olcu_h(0, 5430, g.Y(0) + 34, "İSTASYON 5430")
g.olcu_h(QX0, QX0 + QW, g.Y(0) + 34, "860")
g.olcu_h(TX0, TX0 + TW, g.Y(0) + 34, "600")

# ======================================= 2 · YAN KESİT =======================================
s2 = 0.42
k = Gorunus(300 + 380, g.Y(0) + 290 + 2100 * s2, s2)          # x = derinlik: hat arkası −830 → k.X(z + 830)
Z = lambda z: z + 830.0
txt(300, g.Y(0) + 220, "2 · YAN KESİT · QR ortasından · erişim + kablo", f22, (0, 86, 184), "la")
k.cizgi(Z(-900), 0, Z(1600), 0, INK, 3)
k.kutu(Z(-830), Z(0), 123, TOP, None, w=2); txt(k.X(Z(-415)), k.Y(TOP) + 14, "E (yan)", f11, INK)
k.kutu(Z(-828), Z(-354), 240, 980, "stok", arkada=True, ad="şarjör")
k.kutu(Z(-354), Z(-20), 130, 499, "stok", ad="içecek yedeği")
RZ_, OM, ER = 330.0, 970.0, 779.0
k.kutu(Z(RZ_ - 120), Z(RZ_ + 120), 0, 60, "robot", ad="ray")
k.kutu(Z(RZ_ - 70), Z(RZ_ + 70), 60, OM - 152, "robot", ad="kaide", dolgu=True)
d.ellipse([k.X(Z(RZ_)) - 9, k.Y(OM) - 9, k.X(Z(RZ_)) + 9, k.Y(OM) + 9], fill=INK)
txt(k.X(Z(RZ_)) - 14, k.Y(OM), "omuz 970", f10, INK, "rm")
QZ0, QD = 670.0, 520.0
yat = math.hypot(QZ0 - RZ_, 200.0)
dik = math.sqrt(ER ** 2 - yat ** 2)
B0, B1 = OM - dik, OM + dik
R_ = ER * s2
d.arc([k.X(Z(RZ_)) - R_, k.Y(OM) - R_, k.X(Z(RZ_)) + R_, k.Y(OM) + R_], -75, 75, fill=RENK["robot"][0], width=2)
k.kutu(Z(QZ0), Z(QZ0 + QD), 0, QH, None, w=3)
for r in range(GN):
    y0 = G0 + r * GH
    k.kutu(Z(QZ0 + 40), Z(QZ0 + 480), y0, y0 + 190, "stok", w=1)
    # bilek hedefi: göz tabanı + 100
    d.ellipse([k.X(Z(QZ0)) - 5, k.Y(y0 + 100) - 5, k.X(Z(QZ0)) + 5, k.Y(y0 + 100) + 5], outline=RENK["robot"][0], width=2)
k.kutu(Z(QZ0 + 5), Z(QZ0 + 273), 20, 443, "robot", ad="robot kontrol", alt="268 derin")
k.kutu(Z(QZ0 + 5), Z(QZ0 + 255), UY + 5, UY + 355, "elektrik", ad="ana pano", alt="250 derin")
txt(k.X(Z(QZ0 + QD / 2)), k.Y(QH) - 14, "QR 520", f11, INK)
txt(k.X(Z(QZ0)) - 4, k.Y(QH) + 16, "robot tarafı", f10, GRAY, "rm"); txt(k.X(Z(QZ0 + QD)) + 4, k.Y(QH) + 16, "müşteri", f10, GRAY, "lm")
for yy in (B0, B1):
    d.line([(k.X(Z(QZ0)) - 50, k.Y(yy)), (k.X(Z(QZ0)) + 6, k.Y(yy))], fill=(198, 42, 32), width=3)
txt(k.X(Z(QZ0)) - 54, k.Y(B1) + 2, "erişim üst %.0f" % B1, f10, (198, 42, 32), "rm")
txt(k.X(Z(QZ0)) - 54, k.Y(B0) - 2, "erişim alt %.0f" % B0, f10, (198, 42, 32), "rm")
txt(k.X(Z(QZ0 + QD)) + 12, k.Y(1560), "○ bilek hedefi = göz tabanı + 100", f10, RENK["robot"][0], "lm")
txt(k.X(Z(QZ0 + QD)) + 12, k.Y(1500), "üst göz: 1460 + 100 = 1560 ≤ %.0f" % B1, f10, INK, "lm")
txt(k.X(Z(QZ0 + QD)) + 12, k.Y(1440), "alt göz: 450 + 100 = 550 ≥ %.0f" % B0, f10, INK, "lm")
# kablo yolu (yan kesitte): kontrol kutusu → zemin kanalı → ray kanalı
KAN = 60.0
k.kutu(Z(RZ_ + 130), Z(QZ0 + 10), -KAN, 0, "robot", ad="zemin kanalı", w=2)
kes([(k.X(Z(QZ0 + 140)), k.Y(100)), (k.X(Z(QZ0 + 140)), k.Y(-30)), (k.X(Z(RZ_ + 140)), k.Y(-30)), (k.X(Z(RZ_ + 140)), k.Y(30))], RENK["robot"][0], 4, 12, 5)
txt(k.X(Z(500)), k.Y(-KAN) + 16, "kapaklı zemin kanalı · koridoru geçer", f10, RENK["robot"][0])
k.olcu_h(Z(0), Z(RZ_), k.Y(0) + 70, "330")
k.olcu_h(Z(RZ_), Z(QZ0), k.Y(0) + 70, "340")
k.olcu_h(Z(QZ0), Z(QZ0 + QD), k.Y(0) + 70, "520")
txt(k.X(Z(0)), k.Y(0) + 92, "hat yüzü", f10, GRAY)

# ======================================= 3 · PLAN · kablo yolu =======================================
s3 = 0.3
PX0 = 2050
p = Gorunus(PX0, g.Y(0) + 300, s3)                    # p.Y(y) : y aşağı doğru artar → ters çevir
PY = lambda y: g.Y(0) + 300 + y * s3
PXf = lambda x: PX0 + x * s3
txt(PX0, g.Y(0) + 220, "3 · PLAN · üstten · kablo yolu (dükkân v13 ölçüleri)", f22, (0, 86, 184), "la")


def prect(x0, x1, y0, y1, cins=None, arkada=False, ad="", alt="", w=2, f=f10):
    c = RENK[cins][0] if cins else LINE
    X0, X1, Y0, Y1 = PXf(x0), PXf(x1), PY(y0), PY(y1)
    if arkada:
        kes([(X0, Y0), (X1, Y0), (X1, Y1), (X0, Y1), (X0, Y0)], c, w + 1)
    else:
        d.rectangle([X0, Y0, X1, Y1], fill=acik(c) if cins else None, outline=c, width=w)
    if ad:
        txt((X0 + X1) / 2, (Y0 + Y1) / 2 - (8 if alt else 0), ad, f, c)
        if alt:
            txt((X0 + X1) / 2, (Y0 + Y1) / 2 + 9, alt, f, GRAY)


HATD, FCIK, KOR, DUV, ON = 830.0, 79.0, 900.0, 60.0, 840.0
Y_HY = HATD                     # hat yüzü
Y_KOR0 = HATD + FCIK
Y_DUV0 = Y_KOR0 + KOR
Y_ON0 = Y_DUV0 + DUV
Y_SON = Y_ON0 + ON
RAY_Y = Y_KOR0 + 250.0          # dükkân v13: ray ekseni koridor başından 25 cm (hat yüzünden 330)
d.rectangle([PXf(0), PY(0), PXf(5700), PY(Y_SON)], outline=INK, width=4)
for x0, x1, ad in ((0, 700, "A"), (700, 2500, "B + C"), (2500, 4000, "F"), (4000, 4600, "K"), (4600, 5430, "E")):
    prect(x0, x1, 0, HATD, None, ad=ad, w=2, f=f11)
prect(2500, 4000, HATD, HATD + FCIK, "sicak", w=1)
# duvar (ince) ve ön zon
d.rectangle([PXf(0), PY(Y_DUV0), PXf(4570), PY(Y_ON0)], fill=SOFT, outline=LINE, width=1)
txt(PXf(2000), PY(Y_DUV0 + 30), "ince duvar", f10, GRAY)
# ray + enerji zinciri
prect(200, 5100, RAY_Y - 120, RAY_Y + 120, "robot", w=2)
txt(PXf(900), PY(RAY_Y) , "RAY 200–5100", f10, RENK["robot"][0])
ZY = RAY_Y + 170.0
prect(200, 5100, ZY - 45, ZY + 45, "robot", w=1)
txt(PXf(700), PY(ZY), "zincir oluğu (ray boyu)", f10, RENK["robot"][0])
kes([(PXf(4800), PY(ZY + 20)), (PXf(2650), PY(ZY + 20))], RENK["robot"][0], 4, 12, 5)
txt(PXf(3700), PY(ZY + 20) + 16, "sabit kablo oluğun dibinde 4800 → 2650 (2,2 m)", f10, RENK["robot"][0])
d.line([(PXf(2650), PY(ZY - 20)), (PXf(5000), PY(ZY - 20))], fill=RENK["robot"][0], width=6)
d.ellipse([PXf(2650) - 9, PY(ZY) - 9, PXf(2650) + 9, PY(ZY) + 9], fill=RENK["robot"][0])
txt(PXf(2650), PY(ZY) - 30, "zincirin sabit ucu (ray ortası)", f10, RENK["robot"][0])
txt(PXf(3800), PY(ZY - 20) - 14, "ENERJİ ZİNCİRİ (hareketli) → robot arabası", f10, RENK["robot"][0])
# robot (QR önünde)
d.ellipse([PXf(5000) - 90 * s3 * 1.0, PY(RAY_Y) - 90 * s3, PXf(5000) + 90 * s3, PY(RAY_Y) + 90 * s3], outline=RENK["robot"][0], width=3)
txt(PXf(5000), PY(RAY_Y - 200), "robot QR önünde", f10, RENK["robot"][0])
# QR + zemin kanalı
QY0, QY1 = 1500.0, 2020.0
prect(4570, 5430, QY0, QY1, None, ad="QR", w=3, f=f11)
prect(4600, 5075, QY0 + 5, QY0 + 273, "robot", ad="robot kontrol", w=2)
kes([(PXf(4800), PY(QY0 + 140)), (PXf(4800), PY(ZY + 20))], RENK["robot"][0], 4, 12, 5)
txt(PXf(4800) - 8, PY((QY0 + ZY) / 2), "zemin kanalı", f10, RENK["robot"][0], "rm")
# çöp, tezgâh
prect(3822, 3988, 430, 830, "cop", ad="çöp")
prect(4108.5, 4568.5, 185, 818, "su", ad="bulaşık", w=1)
prect(4060, 4460, 30, 155, "su", arkada=True)
txt(PXf(4260), PY(92), "deterjan · parlatıcı", f10, RENK["su"][0])
prect(3950, 4550, Y_SON - 450, Y_SON, None, ad="TEZGÂH", alt="600 × 450", w=2)
prect(3990, 4510, Y_SON - 430, Y_SON - 40, "stok", arkada=True)
txt(PXf(2000), PY(Y_SON - 200), "ön zon (servis)", f10, GRAY)
txt(PXf(5000), PY(Y_SON + 60), "cephe", f10, GRAY)
# kablo boyu tablosu
TBX, TBY = PXf(0), PY(Y_SON) + 60
satir = [("KABLO · Fairino kol ↔ kontrol kutusu (tek kablo: güç + haberleşme)", ""),
         ("QR içinde kutudan zemine", "0,5 m"), ("zemin kanalı (koridoru geçer)", "0,4 m"), ("ray kanalı x 4800 → 2650", "2,2 m"),
         ("enerji zinciri (strok 4,9 m / 2 + dönüş payı)", "2,85 m"), ("araba + robot tabanı", "0,5 m"), ("TOPLAM gereken", "≈ 6,5 m"),
         ("Fairino standart 4 m → YETMEZ · 11 m uzatma ile 15 m (satıcı sayfası) · artan ≈ 8,5 m QR altında kangal", "")]
for i, (a_, b_) in enumerate(satir):
    c_ = RENK["robot"][0] if i in (0, 6, 7) else INK
    txt(TBX, TBY + i * 22, a_, f11 if i else f13, c_, "la")
    if b_:
        txt(TBX + 560, TBY + i * 22, b_, f11, c_, "la")

# ======================================= 4 · TEZGÂH YAN + LEJANT =======================================
T4X = 4300
t = Gorunus(T4X, g.Y(0) + 290 + 2100 * s2, s2)
txt(T4X - 40, g.Y(0) + 220, "4 · TEZGÂH YAN", f22, (0, 86, 184), "la")
t.cizgi(-50, 0, 700, 0, INK, 3)
t.kutu(30, 450, 0, 100, None, w=1)
t.kutu(0, 450, 100, TH - 30, None, w=2)
t.kutu(-15, 460, TH - 30, TH, None, w=2)
t.kutu(20, 430, TH - 200, TH - 45, "stok", ad="çekmece")
t.kutu(30, 220, 105, 405, "su", ad="bidon", alt="190 derin")
t.cizgi(10, 412, 440, 412, INK, 3)
t.kutu(30, 230, 418, 568, "su", ad="bez")
t.kutu(240, 440, 418, 668, "cop", ad="çöp 10 L")
t.cizgi(450, 0, 450, 2000, LINE, 4); txt(t.X(460), t.Y(1950), "duvar", f10, GRAY, "lm")
t.cizgi(450, 1650, 380, 1650, INK, 4); txt(t.X(370), t.Y(1650), "askı", f10, INK, "rm")
LX, LY = T4X - 40, t.Y(0) + 80
txt(LX, LY, "LEJANT", f15, INK, "la")
for i, (kk, (c, ad)) in enumerate(RENK.items()):
    yy = LY + 34 + i * 30
    d.rectangle([LX, yy - 9, LX + 34, yy + 9], fill=acik(c), outline=c, width=2)
    txt(LX + 46, yy, ad, f11, c, "lm")
yy = LY + 34 + len(RENK) * 30 + 10
d.rectangle([LX, yy - 9, LX + 34, yy + 9], outline=INK, width=2); txt(LX + 46, yy, "düz çizgi = önde", f11, INK, "lm")
kes([(LX, yy + 21), (LX + 34, yy + 21), (LX + 34, yy + 39), (LX, yy + 39), (LX, yy + 21)], INK, 2)
txt(LX + 46, yy + 30, "kesik çizgi = arkada", f11, INK, "lm")

# ======================================= başlık =======================================
txt(300, 62, "AUTOKITCH  ·  İSTASYON + QR + TEZGÂH  ·  teknik resim v4  ·  deterjan + parlatıcı bulaşığın arkasında · temizlik tezgâhta · robot çöpü şeritte", f30, INK, "la")
txt(300, 112, "renk = cins · düz = önde · kesik = arkada · sabit: robot kontrol 475 × 423 × 268 · ana pano 400 × 350 × 250 · UPS 115 × 185 × 213 · göz 380 × 190 × 440 · omuz 970 · erişim 779 · mm · 27 Eylül 2026", f15, GRAY, "la")
d.line([(300, 150), (W_PX - 80, 150)], fill=LINE, width=3)
ad = "QR_TEZGAH_v4"
im.save(os.path.join(KLASOR, ad + ".png"), optimize=True)
im.save(os.path.join(KLASOR, ad + ".pdf"), "PDF", resolution=150.0)
print("yazildi", ad, "bant %.0f-%.0f" % (B0, B1))
