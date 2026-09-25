# -*- coding: utf-8 -*-
"""HAT · ALT KISIM KISALTMA v1 (öneri) — ÖN GÖRÜNÜŞ (0–1250) · F + K TABANI PLAN · B/K4 YAN KESİT · 25 Eyl 2026
Kemal: "alt kısmın boyunu kısalt, boş yer bırakma; PLC soğutma grubunun arkasına; temizlik nişi sağa; taban dolaplarını
(bulaşık, kompresör, UPS, ana pano, robot kontrol) arka arkaya / üst üste temiz yerleştir; sık erişilen önde.
Soğuması gereken çekmeceler (içecek dahil) kendi istasyonunda (B) kalır — her şey kendi istasyonunda."
Hesap (store_cad_v4 / pafta v7 ortak veri): çekmece hatvesi pide 108 · lahmacun 93 · içecek (2 kat) 274; ilk çekmece 167,5.
  Eski: K1 6 pide + pano · K2 2 pide + 6 lah (774) · K3 6 lah + içecek (832 → 999,5) → gövde 1060.
  Yeni: K1 6 pide + 1 lah (741) · K2 2 pide + 6 lah (774) · K3 5 lah + içecek (739) → üst 941,5 → tavan 945 + PU 60 = 1005 (−55).
  K4: Secop 128,5–400,5 · PLC ARKASINDA · ara PU 408,5–438,5 · GN depo 438,5–738,5 · temizlik nişi F'ye → K4 üstü 740.
E şarjörü: platform 240 sabit (asansör arabası 170–300, alt yatak 150 — kutu_cad_v3), yığın üstü 1148 → 1093: 853 mm = 533 kutu (1,6) < 560.
Kompresör K'dan çıkarıldı (TOPPING'e ait, yeri AÇIK). 3B'ye dokunulmadı.
"""
import math, os
from PIL import Image, ImageDraw, ImageFont
U = os.path.dirname(os.path.abspath(__file__)); KOK = os.path.dirname(os.path.dirname(U))
CIKTI = os.path.join(KOK, "arastirma", "FULL_MAKINE", "ALT_KISIM_v1_teknik.png")

INK, GRI, ACIK = (25, 25, 28), (120, 124, 130), (205, 208, 212)
PU, PUC = (246, 232, 180), (214, 188, 118)
SOG, DOL, KIR, MAVI, YES, TUR = (232, 244, 252), (40, 130, 110), (200, 30, 30), (30, 90, 170), (30, 130, 70), (196, 110, 30)
KOYU, PAS = (92, 96, 104), (206, 211, 218)
W, H = 3300, 1880
im = Image.new("RGB", (W, H), (255, 255, 255)); d = ImageDraw.Draw(im)
fn = lambda n, b=False: ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf" if b else "C:/Windows/Fonts/arial.ttf", n)
fB, fG, fE, fO, fK, fS = fn(40, True), fn(27, True), fn(20), fn(18), fn(19, True), fn(15)

H_ESKI, H_YENI, Y_ALT, YUZ0 = 1060.0, 1005.0, 123.0, 167.5
HATVE = {"pide": 108.0, "lah": 93.0, "icecek": 274.0}
ON = {"pide": 105.0, "lah": 90.0, "icecek": 271.0}
KOLON = [("K1", 62.5, [("pide", 6), ("lah", 1)]), ("K2", 717.5, [("pide", 2), ("lah", 6)]), ("K3", 1372.5, [("lah", 5), ("icecek", 1)])]
K4 = (2027.5, 2427.5)
X_F, X_K, X_E, HAT = 2500.0, 4000.0, 4600.0, 5430.0


def kutu(x0, y0, x1, y1, fill=None, renk=INK, w=2):
    x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1)); d.rectangle([x0, y0, x1, y1], fill=fill, outline=renk, width=w)


def kesik(p0, p1, renk=INK, w=2, a=12, b=7):
    (x0, y0), (x1, y1) = p0, p1; L = math.hypot(x1 - x0, y1 - y0)
    if L < 1: return
    ux, uy = (x1 - x0) / L, (y1 - y0) / L; t = 0.0
    while t < L:
        t1 = min(L, t + a); d.line([(x0 + ux * t, y0 + uy * t), (x0 + ux * t1, y0 + uy * t1)], fill=renk, width=w); t = t1 + b


def kk(x0, y0, x1, y1, renk=INK, w=2):
    x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1))
    for p, q in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))): kesik(p, q, renk, w)


def tara(x0, y0, x1, y1, adim=8):
    x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1))
    d.rectangle([x0, y0, x1, y1], fill=PU); h = y1 - y0; k = x0 - h
    while k < x1:
        a = max(k, x0); b = min(k + h, x1)
        if b > a: d.line([(a, y1 - (a - k)), (b, y1 - (b - k))], fill=PUC, width=1)
        k += adim


def ok(x, y, dx, dy, renk=INK, n=11):
    L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
    d.polygon([(x, y), (x - ux * n - uy * n * 0.42, y - uy * n + ux * n * 0.42), (x - ux * n + uy * n * 0.42, y - uy * n - ux * n * 0.42)], fill=renk)


def olcu_x(y, x0, x1, t, renk=INK, alt=False):
    d.line([(x0, y), (x1, y)], fill=renk, width=2); ok(x0, y, -1, 0, renk); ok(x1, y, 1, 0, renk)
    tw = d.textlength(t, font=fO); ty = y + 4 if alt else y - 23
    d.rectangle([(x0 + x1) / 2 - tw / 2 - 3, ty, (x0 + x1) / 2 + tw / 2 + 3, ty + 20], fill=(255, 255, 255)); d.text(((x0 + x1) / 2 - tw / 2, ty), t, font=fO, fill=renk)


def olcu_y(x, y0, y1, t, renk=INK, sol=False):
    d.line([(x, y0), (x, y1)], fill=renk, width=2); ok(x, min(y0, y1), 0, -1, renk); ok(x, max(y0, y1), 0, 1, renk)
    tw = d.textlength(t, font=fO); tx = x - tw - 7 if sol else x + 7
    d.rectangle([tx - 2, (y0 + y1) / 2 - 11, tx + tw + 2, (y0 + y1) / 2 + 10], fill=(255, 255, 255)); d.text((tx, (y0 + y1) / 2 - 10), t, font=fO, fill=renk)


def orta(t, x, y, f=fS, renk=INK):
    for i, s in enumerate(t.split("|")):
        d.text((x - d.textlength(s, font=f) / 2, y + i * (f.size + 3)), s, font=f, fill=renk)


d.text((60, 26), "HAT · ALT KISIM KISALTMA v1 (öneri) — gövde üstü 1060 → 1005 (−55) · her şey kendi istasyonunda", font=fB, fill=INK)
d.text((60, 80), "ölçüler mm · kotlar yerden · yeşil = çekmece (B, soğuk) · turuncu = taşınan parça · kırmızı = eski çizgi / sorun · "
       "üst modüller 55 aşağı iner (süreç 1168 → 1113)", font=fE, fill=GRI)

# ================================================================ ÖN GÖRÜNÜŞ · 0–1250
S = 0.56; OY = 900
X = lambda x: 120 + S * x
Y = lambda y: OY - S * y
d.text((60, 140), "ÖN GÖRÜNÜŞ · ALT KISIM (kapaklar kaldırılmış)", font=fG, fill=INK)
d.line([(X(-80), Y(0)), (X(HAT + 80), Y(0))], fill=INK, width=3)
for x0, x1 in ((0, 2500), (X_F, X_K), (X_K, X_E)):
    kutu(X(x0 + 30), Y(0), X(x1 - 30), Y(Y_ALT), renk=GRI, w=1)
    kutu(X(x0), Y(Y_ALT), X(x1), Y(H_YENI), renk=INK, w=2)
kutu(X(X_E), Y(0), X(HAT), Y(1250), renk=INK, w=2)
kesik((X(-60), Y(H_ESKI)), (X(HAT + 60), Y(H_ESKI)), KIR, 2, 14, 8)
d.text((X(HAT) + 14, Y(H_ESKI) - 12), "1060 eski", font=fO, fill=KIR)
d.text((X(HAT) + 14, Y(H_YENI) - 2), "1005 yeni", font=fK, fill=INK)
# B · tavan PU + çekmeceler
tara(X(30), Y(H_YENI - 1.5), X(2470), Y(H_YENI - 60))
for ad, x0, grup in KOLON:
    y = YUZ0
    for tip, n in grup:
        for _ in range(n):
            kutu(X(x0), Y(y + ON[tip]), X(x0 + 620), Y(y), fill=SOG, renk=DOL, w=2)
            if tip == "icecek": orta("İÇECEK + TATLI · 2 kat · 180 kutu", X(x0 + 310), Y(y + 170), fK, DOL)
            y += HATVE[tip]
    orta("%s · %s · üst %.0f" % (ad, " + ".join("%d %s" % (n, {"pide": "pide", "lah": "lahmacun", "icecek": "içecek"}[t]) for t, n in grup), y), X(x0 + 310), Y(Y_ALT) + 12, fK, DOL)
# K4
kutu(X(K4[0]), Y(400.5), X(K4[1]), Y(128.5), fill=KOYU, renk=INK, w=2); orta("SOĞUTMA GRUBU|Secop CU KLF4.0CND", X(2227.5), Y(330), fS, (255, 255, 255))
kk(X(K4[0] + 30), Y(390), X(K4[1] - 30), Y(140), TUR, 2); d.text((X(K4[0] + 36), Y(212)), "PLC arkada", font=fS, fill=(255, 220, 170))
tara(X(K4[0]), Y(438.5), X(K4[1]), Y(408.5))
kutu(X(K4[0]), Y(738.5), X(K4[1]), Y(438.5), fill=SOG, renk=DOL, w=2); orta("DEPO|2 × GN 1/1-150|kaşar · sucuk +3 °C", X(2227.5), Y(660), fS, DOL)
orta("K4 · üst 740", X(2227.5), Y(Y_ALT) + 12, fK, DOL)
orta("B · ÇEKMECE MODÜLÜ (soğuk) · 2500", X(1250), Y(H_YENI) - 64, fK, INK)
# F tabanı (ön)
kutu(X(X_F + 60), Y(865), X(X_F + 520), Y(135), fill=(245, 245, 247), renk=INK, w=2); orta("BULAŞIK MAKİNESİ|MEIKO M-iClean UM|460 × 600 × 730", X(X_F + 290), Y(560), fS)
kutu(X(X_F + 540), Y(400), X(X_F + 940), Y(135), fill=(255, 244, 230), renk=TUR, w=2); orta("TEMİZLİK NİŞİ|B'den geldi · 2 × 5 L", X(X_F + 740), Y(300), fS, TUR)
kutu(X(X_F + 540), Y(700), X(X_F + 940), Y(420), fill=(255, 244, 230), renk=INK, w=2); orta("MAKİNE DETERJANI|+ PARLATICI · 2 × 5 L", X(X_F + 740), Y(600), fS)
kk(X(X_F + 540), Y(980), X(X_F + 940), Y(720), GRI, 1); orta("arkada: ana pano (alt)|+ UPS (üst)", X(X_F + 740), Y(900), fS, GRI)
kutu(X(X_F + 960), Y(980), X(X_F + 1440), Y(135), fill=(250, 250, 250), renk=GRI, w=1); orta("BOŞ|480 × 830 × 845", X(X_F + 1200), Y(600), fK, GRI)
orta("F · FIRIN TABANI", X(X_F + 750), Y(H_YENI) - 26, fK, INK)
# K tabanı
kutu(X(X_K + 60), Y(330), X(X_K + 300), Y(140), fill=(245, 245, 247), renk=INK, w=2); orta("YAĞ|KARTUŞU", X(X_K + 180), Y(290), fS)
kutu(X(X_K + 320), Y(330), X(X_K + 540), Y(140), fill=(245, 245, 247), renk=INK, w=2); orta("K KARTI", X(X_K + 430), Y(260), fS)
kk(X(X_K + 110), Y(1030), X(X_K + 490), Y(520), KIR, 2); orta("kompresör ÇIKTI|TOPPING'e ait|yeri AÇIK", X(X_K + 300), Y(840), fS, KIR)
orta("K · KESME TABANI", X(X_K + 300), Y(H_YENI) - 26, fK, INK)
# E şarjörü
kutu(X(X_E + 8), Y(1093), X(X_E + 812), Y(240), fill=(250, 246, 236), renk=INK, w=2)
kesik((X(X_E + 8), Y(1148)), (X(X_E + 812), Y(1148)), KIR, 2)
orta("KUTU ŞARJÖRÜ|yığın 240–1093 = 853|533 kutu < 560 (2 gün)", X(X_E + 410), Y(760), fK, KIR)
orta("E · KUTU (tek parça)", X(X_E + 415), Y(1250) - 26, fK, INK)
# ölçüler
yo = Y(0) + 32
for x_ in (0, 2500, 4000, 4600, HAT): d.line([(X(x_), Y(0) + 6), (X(x_), yo + 8)], fill=ACIK, width=1)
olcu_x(yo, X(0), X(2500), "B 2500", alt=True); olcu_x(yo, X(2500), X(4000), "F 1500", alt=True); olcu_x(yo, X(4000), X(4600), "K 600", alt=True); olcu_x(yo, X(4600), X(HAT), "E 830", alt=True)
olcu_y(X(0) - 40, Y(Y_ALT), Y(H_YENI), "882", sol=True)
for y_ in (0.0, Y_ALT, YUZ0, 941.5):
    d.line([(X(-20), Y(y_)), (X(-6), Y(y_))], fill=GRI, width=1)

# ================================================================ PLAN · F + K TABANI (y ≈ 500 kesiti)
S2 = 0.62
PX = lambda x: 120 + (x - X_F) * S2
PZ = lambda z: 1560 + (-z) * S2 * -1 + 0            # ön altta
PZ = lambda z: 1560 - (z + 830.0) * S2 * -1         # z 0 → 1560 + 515 ; basit: ön altta
PZ = lambda z: 1720 + z * S2
d.text((60, 1090), "ÜST GÖRÜNÜŞ · F + K TABANI (önde sık erişilen, arkada az erişilen)", font=fG, fill=INK)
kutu(PX(X_F), PZ(-830), PX(X_K), PZ(0), renk=INK, w=2); kutu(PX(X_K), PZ(-830), PX(X_E), PZ(0), renk=INK, w=2)
d.text((PX(X_F) + 6, PZ(-830) - 26), "ARKA", font=fO, fill=GRI); d.text((PX(X_F) + 6, PZ(0) + 6), "ÖN · robot koridoru", font=fO, fill=GRI)
kutu(PX(X_F + 60), PZ(-600), PX(X_F + 520), PZ(-20), fill=(245, 245, 247), renk=INK, w=2); orta("BULAŞIK|MAKİNESİ", PX(X_F + 290), PZ(-340), fS)
kutu(PX(X_F + 150), PZ(-790), PX(X_F + 395), PZ(-745), fill=(255, 244, 230), renk=TUR, w=2); orta("robot kontrol kutusu (dik)", PX(X_F + 272), PZ(-745) + 4, fS, TUR)
kutu(PX(X_F + 540), PZ(-320), PX(X_F + 940), PZ(-20), fill=(255, 244, 230), renk=TUR, w=2); orta("temizlik (alt)|deterjan (üst)", PX(X_F + 740), PZ(-190), fS, TUR)
kutu(PX(X_F + 540), PZ(-790), PX(X_F + 940), PZ(-540), fill=(255, 244, 230), renk=TUR, w=2); orta("ANA PANO (alt)|UPS (üst)", PX(X_F + 740), PZ(-690), fS, TUR)
kutu(PX(X_F + 960), PZ(-790), PX(X_F + 1440), PZ(-20), fill=(250, 250, 250), renk=GRI, w=1); orta("BOŞ 480 × 770", PX(X_F + 1200), PZ(-420), fK, GRI)
kutu(PX(X_K + 60), PZ(-420), PX(X_K + 300), PZ(-20), fill=(245, 245, 247), renk=INK, w=2); orta("YAĞ", PX(X_K + 180), PZ(-230), fS)
kutu(PX(X_K + 320), PZ(-220), PX(X_K + 540), PZ(-20), fill=(245, 245, 247), renk=INK, w=2); orta("K KARTI", PX(X_K + 430), PZ(-130), fS)
kk(PX(X_K + 110), PZ(-420), PX(X_K + 490), PZ(-40), KIR, 1)
olcu_x(PZ(0) + 30, PX(X_F), PX(X_K), "1500", alt=True); olcu_x(PZ(0) + 30, PX(X_K), PX(X_E), "600", alt=True)

# ================================================================ B · K4 YAN KESİT
S3 = 0.62
ZK = lambda z: 1600 + (z + 830.0) * S3
YK = lambda y: 1765 - y * S3
d.text((1600, 1090), "B · K4 YAN KESİT (arka solda · ön sağda)", font=fG, fill=INK)
kutu(ZK(-830), YK(Y_ALT), ZK(0), YK(H_YENI), renk=INK, w=2)
tara(ZK(-830), YK(H_YENI - 1.5), ZK(0), YK(H_YENI - 60))
kutu(ZK(-516), YK(400.5), ZK(-66), YK(128.5), fill=KOYU, renk=INK, w=2); orta("Secop|350 × 272 × 450", (ZK(-516) + ZK(-66)) / 2, YK(330), fS, (255, 255, 255))
kutu(ZK(-790), YK(390), ZK(-526), YK(140), fill=(255, 244, 230), renk=TUR, w=2); orta("PLC + G/Ç|24 V · sürücü · röle|(K1 üstünden geldi)", (ZK(-790) + ZK(-526)) / 2, YK(330), fS, TUR)
kutu(ZK(-790), YK(130), ZK(-56), YK(125), fill=PAS, renk=INK, w=1)
tara(ZK(-790), YK(438.5), ZK(-56), YK(408.5))
kutu(ZK(-596), YK(738.5), ZK(-66), YK(438.5), fill=SOG, renk=DOL, w=2); orta("DEPO · 2 × GN 1/1-150|+3 °C", (ZK(-596) + ZK(-66)) / 2, YK(620), fS, DOL)
kutu(ZK(-56), YK(400.5), ZK(-40), YK(128.5), fill=(255, 255, 255), renk=INK, w=1)
for yy in range(140, 395, 14): d.line([(ZK(-54), YK(yy)), (ZK(-42), YK(yy + 5))], fill=GRI, width=1)
d.text((ZK(0) + 10, YK(270) - 10), "ızgaralı kapak", font=fS, fill=GRI)
olcu_y(ZK(0) + 130, YK(128.5), YK(400.5), "272"); olcu_y(ZK(0) + 130, YK(438.5), YK(738.5), "300")
olcu_x(YK(Y_ALT) + 30, ZK(-790), ZK(-526), "264", alt=True); olcu_x(YK(Y_ALT) + 30, ZK(-516), ZK(-66), "450", alt=True)
d.text((ZK(-830), YK(900)), "K4 üstü 740 · temizlik nişi F tabanına gitti", font=fO, fill=GRI)

os.makedirs(os.path.dirname(CIKTI), exist_ok=True)
im.save(CIKTI, optimize=True); print("PNG", CIKTI)
