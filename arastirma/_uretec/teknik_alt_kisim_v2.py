# -*- coding: utf-8 -*-
"""HAT · ALT KISIM YERLEŞİMİ v2 — ÖN GÖRÜNÜŞ · ÜST GÖRÜNÜŞ · 4 YAN KESİT · STOK TABLOSU · 25 Eyl 2026
Kemal: "eksik hiçbir şey olmasın, her şeyi hesapla; içecek + tatlı yedeğini taşı; 4 günlük pizza kutusunu sığdır; soğuması
gerekenler B'de; her şey kendi istasyonunda; sık erişilen önde, az erişilen arkada; teknik resim yalnız alt kısım."

HESAP (kaynaklar):
  çekmece hatvesi = HH + 2 × 15 (bindirme) + 3 (fuga) · HH pide 75 · lahmacun 60 (store_cad_v4 / pafta ortak veri)
  içecek TEK KAT (robot her kutuya erişsin): HH 126 = kutu 115 + 11 tepsi/itici (VARSAYIM) → hatve 159
     geniş (620): 6 şerit × 8 = 48 kutu · dar (400): 4 şerit × 8 = 32 kutu (store_cad_v4 formülü: ax 82, az 75, kutu Ø66)
     şeritte yaylı market iticisi → robot hep öndeki kutuyu alır (standart ürün, marka seçilmedi)
  günlük ihtiyaç: pide 80 · lahmacun 200 · kutu 280 · içecek 277/4 = 69,25 · tatlı 22/4 = 5,5 (pafta K yedeği: "180 + 97 = 277 = 4 gün")
  E şarjörü: platform 240 → yığın üstü 1148 = 908 mm = 567 kutu (1,6 mm) — gövde 1 mm inerse 0,6 kutu azalır → en çok 11 mm inilebilir
  bulaşık makinesi MEIKO M-iClean US: 460 genişlik · yükseklik 700 · sepet 400 × 400 · giriş 315 (meiko.com) · derinlik 600 VARSAYIM
  UPS APC Back-UPS BX500CI 115 × 213 × 185 (schneider-electric) · robot kontrol kutusu: Fairino kompakt 245 × 180 × 89 (3,6 kg);
     FR5 ile gelen kutu teyit edilene kadar UR sınıfı kutu kadar yer (475 × 423 × 268) ayrıldı — VARSAYIM
  ana pano 400 × 350 × 250 · yağ kartuşu 4 L × 2 (240 × 190 × 400) · K kartı 220 × 190 × 200 (pafta v7, VARSAYIM)
  24'lük içecek kolisi 400 × 267 × 123 · tatlı kabı Ø95 × 60 · 5 L bidon 130 × 190 × 290 (VARSAYIM)
3B'ye dokunulmadı.
"""
import math, os
from PIL import Image, ImageDraw, ImageFont
U = os.path.dirname(os.path.abspath(__file__)); KOK = os.path.dirname(os.path.dirname(U))
CIKTI = os.path.join(KOK, "arastirma", "FULL_MAKINE", "ALT_KISIM_v2_teknik.png")

INK, GRI, ACIK = (25, 25, 28), (120, 124, 130), (205, 208, 212)
PU, PUC = (246, 232, 180), (214, 188, 118)
SOG, DOL, KIR, MAVI, TUR = (232, 244, 252), (40, 130, 110), (200, 30, 30), (30, 90, 170), (196, 110, 30)
KOYU, PAS, BEJ, KUT = (92, 96, 104), (206, 211, 218), (252, 247, 236), (236, 214, 170)
W, H = 3600, 2160
im = Image.new("RGB", (W, H), (255, 255, 255)); d = ImageDraw.Draw(im)
fn = lambda n, b=False: ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf" if b else "C:/Windows/Fonts/arial.ttf", n)
fB, fG, fE, fO, fK, fS, fXS = fn(40, True), fn(26, True), fn(19), fn(17), fn(17, True), fn(14), fn(12)

# ---------------------------------------------------------------- ÖLÇÜLER
H_B, Y_ALT, YUZ0, TAVAN = 1060.0, 123.0, 167.5, 1000.0
HATVE = {"pide": 108.0, "lah": 93.0, "ic": 159.0, "tat": 159.0}
PANEL = {k: v - 3.0 for k, v in HATVE.items()}
AD = {"pide": "pide · 20 top", "lah": "lahmacun · 36", "ic": "içecek · 48 kutu", "tat": "tatlı · 18"}
KOL = [("K1", 62.5, 620.0, YUZ0, [("pide", 6), ("lah", 1)]),
       ("K2", 717.5, 620.0, YUZ0, [("pide", 2), ("lah", 6)]),
       ("K3", 1372.5, 620.0, YUZ0, [("lah", 5), ("ic", 2)]),
       ("K4", 2027.5, 400.0, 441.5, [("ic", 2), ("tat", 1)])]
X_F, X_K, X_E, HAT = 2500.0, 4000.0, 4600.0, 5430.0
DW = dict(x=(2540.0, 3000.0), y=(130.0, 830.0), z=(-20.0, -620.0))           # MEIKO M-iClean US
BID = dict(x=(3010.0, 3156.0))                                               # bidon kolonu 146
PZ = dict(x=(3166.0, 3970.0), y=(130.0, 130.0 + 15.0 + 553 * 1.6), z=(-20.0, -424.0))   # pizza kutusu yedeği (düz)
RBK = dict(x=(3166.0, 3641.0), y=(130.0, 553.0), z=(-434.0, -702.0))          # robot kontrol kutusu yeri
PANO = dict(x=(3166.0, 3566.0), y=(565.0, 915.0), z=(-434.0, -684.0))
UPS = dict(x=(3576.0, 3691.0), y=(565.0, 750.0), z=(-434.0, -647.0))
ICY = dict(x=(4040.0, 4440.0), y=(130.0, 130.0 + 5 * 123.0), z=(-20.0, -287.0))  # 5 koli
TTY = dict(x=(4040.0, 4430.0), y=(ICY["y"][1] + 10.0, ICY["y"][1] + 80.0), z=(-20.0, -280.0))
YAG = dict(x=(4040.0, 4440.0), y=(130.0, 320.0), z=(-420.0, -660.0))
KKART = dict(x=(4040.0, 4260.0), y=(330.0, 520.0), z=(-420.0, -620.0))


def kutu(x0, y0, x1, y1, fill=None, renk=INK, w=2):
    x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1)); d.rectangle([x0, y0, x1, y1], fill=fill, outline=renk, width=w)


def kesik(p0, p1, renk=INK, w=2, a=11, b=6):
    (x0, y0), (x1, y1) = p0, p1; L = math.hypot(x1 - x0, y1 - y0)
    if L < 1: return
    ux, uy = (x1 - x0) / L, (y1 - y0) / L; t = 0.0
    while t < L:
        t1 = min(L, t + a); d.line([(x0 + ux * t, y0 + uy * t), (x0 + ux * t1, y0 + uy * t1)], fill=renk, width=w); t = t1 + b


def kk(x0, y0, x1, y1, renk=INK, w=2):
    x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1))
    for p, q in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))): kesik(p, q, renk, w)


def tara(x0, y0, x1, y1, adim=8, dolgu=PU, renk=PUC):
    x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1))
    d.rectangle([x0, y0, x1, y1], fill=dolgu); h = y1 - y0; k = x0 - h
    while k < x1:
        a = max(k, x0); b = min(k + h, x1)
        if b > a: d.line([(a, y1 - (a - k)), (b, y1 - (b - k))], fill=renk, width=1)
        k += adim


def ok(x, y, dx, dy, renk=INK, n=10):
    L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
    d.polygon([(x, y), (x - ux * n - uy * n * 0.42, y - uy * n + ux * n * 0.42), (x - ux * n + uy * n * 0.42, y - uy * n - ux * n * 0.42)], fill=renk)


def olcu_x(y, x0, x1, t, renk=INK, alt=False, f=None):
    f = f or fO
    d.line([(x0, y), (x1, y)], fill=renk, width=2); ok(x0, y, -1, 0, renk); ok(x1, y, 1, 0, renk)
    tw = d.textlength(t, font=f); ty = y + 3 if alt else y - 21
    d.rectangle([(x0 + x1) / 2 - tw / 2 - 3, ty, (x0 + x1) / 2 + tw / 2 + 3, ty + 18], fill=(255, 255, 255)); d.text(((x0 + x1) / 2 - tw / 2, ty), t, font=f, fill=renk)


def olcu_y(x, y0, y1, t, renk=INK, sol=False, f=None):
    f = f or fO
    d.line([(x, y0), (x, y1)], fill=renk, width=2); ok(x, min(y0, y1), 0, -1, renk); ok(x, max(y0, y1), 0, 1, renk)
    tw = d.textlength(t, font=f); tx = x - tw - 6 if sol else x + 6
    d.rectangle([tx - 2, (y0 + y1) / 2 - 10, tx + tw + 2, (y0 + y1) / 2 + 9], fill=(255, 255, 255)); d.text((tx, (y0 + y1) / 2 - 9), t, font=f, fill=renk)


def orta(t, x, y, f=fS, renk=INK):
    for i, s in enumerate(t.split("|")):
        d.text((x - d.textlength(s, font=f) / 2, y + i * (f.size + 3)), s, font=f, fill=renk)


d.text((60, 24), "HAT · ALT KISIM YERLEŞİMİ v2 — eksiksiz stok · her şey kendi istasyonunda · sık erişilen önde", font=fB, fill=INK)
d.text((60, 76), "ölçüler mm · kotlar yerden · alt kısım 123–1060 (değişmedi: E şarjörü 2 günü yalnız bu kotta tutuyor) · yeşil = soğuk çekmece (B) · "
       "turuncu = taşınan · kesik = arkada · (V) = varsayım ölçü", font=fE, fill=GRI)

# ================================================================ ÖN GÖRÜNÜŞ
S = 0.6; OY = 870
X = lambda x: 150 + S * x
Y = lambda y: OY - S * y
d.text((60, 120), "ÖN GÖRÜNÜŞ · ALT KISIM (kapaklar kaldırılmış)", font=fG, fill=INK)
d.line([(X(-60), Y(0)), (X(HAT + 60), Y(0))], fill=INK, width=3)
for x0, x1, ad in ((0, 2500, "B · ÇEKMECELER (soğuk +3 °C)"), (X_F, X_K, "F · FIRIN TABANI"), (X_K, X_E, "K · KESME TABANI"), (X_E, HAT, "E · KUTU (alt kısmı)")):
    kutu(X(x0 + 30), Y(0), X(x1 - 30), Y(Y_ALT), renk=GRI, w=1)
    kutu(X(x0), Y(Y_ALT), X(x1), Y(H_B), renk=INK, w=2)
    orta(ad, X((x0 + x1) / 2), Y(H_B) - 24, fK)
# B tavan PU + taban PU
tara(X(30), Y(H_B - 1.5), X(2470), Y(TAVAN)); tara(X(30), Y(164.5), X(1992.5), Y(Y_ALT + 1.5))
for ad, x0, w, y0, grup in KOL:
    y = y0
    for tip, n in grup:
        for _ in range(n):
            kutu(X(x0), Y(y + PANEL[tip]), X(x0 + w), Y(y), fill=SOG, renk=DOL, w=2)
            orta(AD[tip].replace(" · 48", " · %d" % (48 if w > 500 else 32)), X(x0 + w / 2), Y(y + PANEL[tip] / 2) - 8, fXS, DOL)
            y += HATVE[tip]
    orta("%s · üst %.0f" % (ad, y), X(x0 + w / 2), Y(Y_ALT) + 8, fK, DOL)
# K4 sıcak bölme
kutu(X(2027.5), Y(408.5), X(2427.5), Y(126.5), fill=KOYU, renk=INK, w=2)
orta("SECOP (önde)|PLC + güç + röle|(arkasında)", X(2227.5), Y(360), fS, (255, 255, 255))
tara(X(2027.5), Y(438.5), X(2427.5), Y(408.5))
kesik((X(-40), Y(TAVAN)), (X(2500), Y(TAVAN)), GRI, 1)
# F
kutu(X(DW["x"][0]), Y(DW["y"][1]), X(DW["x"][1]), Y(DW["y"][0]), fill=(244, 245, 247), renk=INK, w=2)
orta("BULAŞIK MAKİNESİ|MEIKO M-iClean US|460 × 600 (V) × 700|sepet 400 × 400", X(2770), Y(560), fS)
kesik((X(DW["x"][0]), Y(900)), (X(DW["x"][1]), Y(900)), GRI, 1); orta("arkasında: su + gider", X(2770), Y(990), fXS, GRI)
kutu(X(BID["x"][0]), Y(730), X(BID["x"][1]), Y(130), fill=(255, 244, 230), renk=TUR, w=2)
orta("TEMİZLİK|2 × 5 L|bidon||arkada:|makine|deterjanı +|parlatıcı", X(3083), Y(640), fXS, TUR)
kutu(X(BID["x"][0]), Y(1045), X(BID["x"][1]), Y(740), fill=(255, 244, 230), renk=TUR, w=2); orta("bez ·|eldiven ·|poşet", X(3083), Y(960), fXS, TUR)
kutu(X(PZ["x"][0]), Y(PZ["y"][1]), X(PZ["x"][1]), Y(PZ["y"][0]), fill=KUT, renk=INK, w=2)
orta("PİZZA KUTUSU YEDEĞİ (düz, önde)|553 kutu · 804 × 404 × 885|şarjör 567 + 553 = 1120 = 4 gün", X(3568), Y(1015), fK)
for b_, t_ in ((RBK, "ROBOT KONTROL KUTUSU|(arkada) · 475 × 423 × 268 (V)"), (PANO, "ANA PANO (arkada)|400 × 350 × 250 (V)"), (UPS, "UPS|(arkada)")):
    kk(X(b_["x"][0]), Y(b_["y"][1]), X(b_["x"][1]), Y(b_["y"][0]), TUR, 2)
    orta(t_, X((b_["x"][0] + b_["x"][1]) / 2), Y((b_["y"][0] + b_["y"][1]) / 2) - 12, fXS, TUR)
# K
kutu(X(ICY["x"][0]), Y(ICY["y"][1]), X(ICY["x"][1]), Y(ICY["y"][0]), fill=(255, 244, 230), renk=TUR, w=2)
for i in range(1, 5): d.line([(X(ICY["x"][0]), Y(130 + i * 123)), (X(ICY["x"][1]), Y(130 + i * 123))], fill=TUR, width=1)
orta("İÇECEK YEDEĞİ|5 koli × 24 = 120 kutu", X(4240), Y(660), fS, TUR)
kutu(X(TTY["x"][0]), Y(TTY["y"][1]), X(TTY["x"][1]), Y(TTY["y"][0]), fill=(255, 244, 230), renk=TUR, w=2); orta("TATLI YEDEĞİ · 12", X(4235), Y(TTY["y"][1]) + 2, fXS, TUR)
kutu(X(4040), Y(1045), X(4560), Y(TTY["y"][1] + 10), fill=(250, 250, 250), renk=GRI, w=1); orta("boş raf|520 × 390 × 225", X(4300), Y(980), fXS, GRI)
for b_, t_ in ((YAG, "yağ kartuşu (arkada)"), (KKART, "K kartı (arkada)")):
    kk(X(b_["x"][0]), Y(b_["y"][1]), X(b_["x"][1]), Y(b_["y"][0]), INK, 1)
    orta(t_, X((b_["x"][0] + b_["x"][1]) / 2), Y(b_["y"][0]) - 20, fXS, INK)
# E alt kısmı
kutu(X(X_E + 8), Y(H_B + 40), X(X_E + 812), Y(240), fill=BEJ, renk=INK, w=2)
orta("KUTU ŞARJÖRÜ|(arkada)|567 kutu|= 2 gün|yığın|240–1148", X(X_E + 600), Y(760), fK)
for xa in (90, 390): kutu(X(X_E + xa), Y(1060), X(X_E + xa + 40), Y(126), fill=PAS, renk=INK, w=1)
d.text((X(X_E + 440), Y(300)), "önde: zımba kalıbı ayakları", font=fXS, fill=GRI)
# ölçü + kot
yo = Y(0) + 30
for x_ in (0, 2500, 4000, 4600, HAT): d.line([(X(x_), Y(0) + 6), (X(x_), yo + 8)], fill=ACIK, width=1)
olcu_x(yo, X(0), X(2500), "2500", alt=True); olcu_x(yo, X(2500), X(4000), "1500", alt=True); olcu_x(yo, X(4000), X(4600), "600", alt=True); olcu_x(yo, X(4600), X(HAT), "830", alt=True)
for y_, t in ((Y_ALT, "123"), (TAVAN, "1000 B tavanı"), (H_B, "1060")):
    d.line([(X(-40), Y(y_)), (X(-6), Y(y_))], fill=GRI, width=1); d.text((X(-44) - d.textlength(t, font=fXS), Y(y_) - 7), t, font=fXS, fill=INK)

# ================================================================ ÜST GÖRÜNÜŞ (y ≈ 400 kesiti · ön altta)
S2 = 0.6
PX = lambda x: 150 + S2 * x
PZz = lambda z: 1500 + S2 * z                        # z 0 → 1500 (ön), −830 → 1002
d.text((60, 920), "ÜST GÖRÜNÜŞ · ~400 kotunda kesit (ön altta · robot koridoru)", font=fG, fill=INK)
for x0, x1 in ((0, 2500), (X_F, X_K), (X_K, X_E), (X_E, HAT)): kutu(PX(x0), PZz(-830), PX(x1), PZz(0), renk=INK, w=2)
d.text((PX(0), PZz(-830) - 22), "ARKA", font=fS, fill=GRI); d.text((PX(0), PZz(0) + 4), "ÖN", font=fS, fill=GRI)
for ad, x0, w, y0, grup in KOL:
    if ad == "K4": continue
    kutu(PX(x0 + 30), PZz(-736), PX(x0 + w - 30), PZz(-57), fill=SOG, renk=DOL, w=2)
    kutu(PX(x0 + 3), PZz(-787), PX(x0 + 60), PZz(-751), fill=KOYU, renk=INK, w=1)
    orta("%s · kutu 560 × 680|motor + kasnak arkada" % ad, PX(x0 + w / 2), PZz(-420), fS, DOL)
kutu(PX(2077.5), PZz(-516), PX(2427.5), PZz(-66), fill=KOYU, renk=INK, w=2); orta("SECOP|350 × 450", PX(2252), PZz(-300), fS, (255, 255, 255))
kutu(PX(2037.5), PZz(-790), PX(2417.5), PZz(-526), fill=(255, 244, 230), renk=TUR, w=2); orta("B PLC|(K1 üstünden)", PX(2227), PZz(-680), fXS, TUR)
kutu(PX(DW["x"][0]), PZz(DW["z"][1]), PX(DW["x"][1]), PZz(DW["z"][0]), fill=(244, 245, 247), renk=INK, w=2); orta("BULAŞIK|MAKİNESİ", PX(2770), PZz(-330), fS)
kk(PX(DW["x"][0]), PZz(-815), PX(DW["x"][1]), PZz(-630), GRI, 1); orta("su + gider", PX(2770), PZz(-735), fXS, GRI)
kutu(PX(BID["x"][0]), PZz(-210), PX(BID["x"][1]), PZz(-20), fill=(255, 244, 230), renk=TUR, w=2); orta("temizlik", PX(3083), PZz(-125), fXS, TUR)
kutu(PX(BID["x"][0]), PZz(-410), PX(BID["x"][1]), PZz(-220), fill=(250, 250, 250), renk=INK, w=1); orta("makine|deterjanı", PX(3083), PZz(-330), fXS)
kutu(PX(PZ["x"][0]), PZz(PZ["z"][1]), PX(PZ["x"][1]), PZz(PZ["z"][0]), fill=KUT, renk=INK, w=2); orta("PİZZA KUTUSU YEDEĞİ · 804 × 404", PX(3568), PZz(-230), fS)
kutu(PX(RBK["x"][0]), PZz(RBK["z"][1]), PX(RBK["x"][1]), PZz(RBK["z"][0]), fill=(255, 244, 230), renk=TUR, w=2); orta("ROBOT KONTROL|KUTUSU (alt)|ANA PANO (üst)", PX(3403), PZz(-570), fXS, TUR)
kutu(PX(UPS["x"][0]), PZz(UPS["z"][1]), PX(UPS["x"][1]), PZz(UPS["z"][0]), fill=(255, 244, 230), renk=TUR, w=2); orta("UPS", PX(3633), PZz(-545), fXS, TUR)
kutu(PX(ICY["x"][0]), PZz(ICY["z"][1]), PX(ICY["x"][1]), PZz(ICY["z"][0]), fill=(255, 244, 230), renk=TUR, w=2); orta("İÇECEK + TATLI|YEDEĞİ", PX(4240), PZz(-160), fXS, TUR)
kutu(PX(YAG["x"][0]), PZz(YAG["z"][1]), PX(YAG["x"][1]), PZz(YAG["z"][0]), fill=(250, 250, 250), renk=INK, w=1); orta("YAĞ KARTUŞU (alt)|K KARTI (üst)", PX(4240), PZz(-560), fXS)
kutu(PX(X_E + 8), PZz(-819), PX(X_E + 812), PZz(-415), fill=BEJ, renk=INK, w=2); orta("ŞARJÖR 804 × 404", PX(X_E + 410), PZz(-620), fS)
for xa in (90, 390):
    for za in ((-360, -320), (-90, -50)): kutu(PX(X_E + xa), PZz(za[0]), PX(X_E + xa + 40), PZz(za[1]), fill=PAS, renk=INK, w=1)

# ================================================================ YAN KESİTLER (arka solda · ön sağda)
S3 = 0.44
KES = [("KESİT 1 · B / K3 (içecek tek kat)", 60), ("KESİT 2 · B / K4", 700), ("KESİT 3 · F (pizza · robot · pano)", 1340), ("KESİT 4 · K (içecek yedeği · yağ)", 1980)]
OYK = 2060
for ad, x0 in KES: d.text((x0, 1545), ad, font=fK, fill=INK)
YK = lambda y: OYK - S3 * y
def zk(x0): return lambda z: x0 + 20 + (z + 830.0) * S3
# 1 · K3
z = zk(60)
kutu(z(-830), YK(Y_ALT), z(0), YK(H_B), renk=INK, w=2); tara(z(-828), YK(H_B - 1.5), z(-2), YK(TAVAN)); tara(z(-828), YK(164.5), z(-2), YK(Y_ALT + 1.5))
y = YUZ0
for tip, n in [("lah", 5), ("ic", 2)]:
    for _ in range(n):
        kutu(z(-736), YK(y + PANEL[tip] - 12), z(-57), YK(y + 15), fill=SOG, renk=DOL, w=1)
        if tip == "ic":
            for j in range(8):
                zc = -66 - 33 - j * 75
                d.rectangle([z(zc - 33), YK(y + 15 + 115), z(zc + 33), YK(y + 15 + 4)], outline=DOL, width=1)
            d.line([(z(-700), YK(y + 70)), (z(-690), YK(y + 70))], fill=KIR, width=3)
        kutu(z(-40), YK(y + PANEL[tip]), z(0), YK(y), fill=(255, 255, 255), renk=DOL, w=1)
        y += HATVE[tip]
d.text((z(-830), YK(y) - 40), "içecek: şerit başına 8 kutu · yaylı itici (kırmızı)", font=fXS, fill=DOL)
olcu_y(z(0) + 22, YK(YUZ0 + 465), YK(YUZ0 + 465 + 159), "159", f=fXS)
# 2 · K4
z = zk(700)
kutu(z(-830), YK(Y_ALT), z(0), YK(H_B), renk=INK, w=2); tara(z(-828), YK(H_B - 1.5), z(-2), YK(TAVAN))
kutu(z(-516), YK(400.5), z(-66), YK(128.5), fill=KOYU, renk=INK, w=2); orta("Secop", (z(-516) + z(-66)) / 2, YK(290), fS, (255, 255, 255))
d.line([(z(-521), YK(128)), (z(-521), YK(405))], fill=INK, width=3)
kutu(z(-790), YK(390), z(-526), YK(140), fill=(255, 244, 230), renk=TUR, w=2); orta("PLC|güç|röle", (z(-790) + z(-526)) / 2, YK(320), fXS, TUR)
tara(z(-828), YK(438.5), z(-2), YK(408.5))
y = 441.5
for tip in ("ic", "ic", "tat"):
    kutu(z(-736), YK(y + PANEL[tip] - 12), z(-57), YK(y + 15), fill=SOG, renk=DOL, w=1)
    kutu(z(-40), YK(y + PANEL[tip]), z(0), YK(y), fill=(255, 255, 255), renk=DOL, w=1); y += HATVE[tip]
d.text((z(-826), YK(1000) + 4), "üst 918,5 · ara sac Secop ↔ PLC", font=fXS, fill=GRI)
# 3 · F (x 3166–3970 kolonundan)
z = zk(1340)
kutu(z(-830), YK(Y_ALT), z(0), YK(H_B), renk=INK, w=2)
kutu(z(PZ["z"][1]), YK(PZ["y"][1]), z(PZ["z"][0]), YK(PZ["y"][0]), fill=KUT, renk=INK, w=2); orta("PİZZA|KUTUSU|YEDEĞİ|553", (z(-424) + z(-20)) / 2, YK(640), fS)
kutu(z(RBK["z"][1]), YK(RBK["y"][1]), z(RBK["z"][0]), YK(RBK["y"][0]), fill=(255, 244, 230), renk=TUR, w=2); orta("ROBOT|KONTROL|KUTUSU|(V)", (z(-702) + z(-434)) / 2, YK(420), fXS, TUR)
kutu(z(PANO["z"][1]), YK(PANO["y"][1]), z(PANO["z"][0]), YK(PANO["y"][0]), fill=(255, 244, 230), renk=TUR, w=2); orta("ANA|PANO|(V)", (z(-684) + z(-434)) / 2, YK(790), fXS, TUR)
olcu_y(z(0) + 22, YK(PZ["y"][0]), YK(PZ["y"][1]), "900", f=fXS)
olcu_x(YK(Y_ALT) + 26, z(-424), z(-20), "404", alt=True, f=fXS); olcu_x(YK(Y_ALT) + 26, z(-702), z(-434), "268", alt=True, f=fXS)
# 4 · K
z = zk(1980)
kutu(z(-830), YK(Y_ALT), z(0), YK(H_B), renk=INK, w=2)
kutu(z(ICY["z"][1]), YK(ICY["y"][1]), z(ICY["z"][0]), YK(ICY["y"][0]), fill=(255, 244, 230), renk=TUR, w=2)
for i in range(1, 5): d.line([(z(ICY["z"][1]), YK(130 + i * 123)), (z(ICY["z"][0]), YK(130 + i * 123))], fill=TUR, width=1)
orta("5 koli", (z(-287) + z(-20)) / 2, YK(470), fXS, TUR)
kutu(z(TTY["z"][1]), YK(TTY["y"][1]), z(TTY["z"][0]), YK(TTY["y"][0]), fill=(255, 244, 230), renk=TUR, w=1)
kutu(z(YAG["z"][1]), YK(YAG["y"][1]), z(YAG["z"][0]), YK(YAG["y"][0]), fill=(250, 250, 250), renk=INK, w=1); orta("yağ", (z(-660) + z(-420)) / 2, YK(250), fXS)
kutu(z(KKART["z"][1]), YK(KKART["y"][1]), z(KKART["z"][0]), YK(KKART["y"][0]), fill=(250, 250, 250), renk=INK, w=1); orta("K kartı", (z(-620) + z(-420)) / 2, YK(440), fXS)
olcu_y(z(0) + 22, YK(130), YK(745), "615", f=fXS)

# ================================================================ STOK TABLOSU
TX, TY = 2640, 1545
d.text((TX, TY), "STOK · 2 GÜN ROBOTUN ERİŞİMİNDE · 4 GÜN DÜKKÂNDA", font=fK, fill=INK)
SAT = [("ürün", "günlük", "gerekli", "yer · adet", "kapasite"),
       ("pide", "80", "2 gün 160", "B · 8 çekmece × 20", "160 · yeter"),
       ("lahmacun", "200", "2 gün 400", "B · 12 çekmece × 36", "432 · yeter"),
       ("içecek (soğuk)", "69", "2 gün 139", "B · 2 × 48 + 2 × 32 (tek kat)", "160 · yeter"),
       ("tatlı (soğuk)", "5,5", "2 gün 11", "B · K4 · 3 şerit × 6", "18 · yeter"),
       ("içecek yedeği", "", "4 gün 277", "K tabanı önde · 5 koli × 24", "160 + 120 = 280 · yeter"),
       ("tatlı yedeği", "", "4 gün 22", "K tabanı önde · 1 kutu", "18 + 12 = 30 · yeter"),
       ("pizza kutusu", "280", "2 gün 560", "E şarjörü", "567 · yeter"),
       ("pizza kutusu", "", "4 gün 1120", "F tabanı önde · düz yığın", "567 + 553 = 1120 · yeter"),
       ("kaşar / sucuk", "", "2 gün", "TOPPING kasetleri (8,8 / 2,8 kg)", "yeter · B'deki GN depo kalktı")]
CX = [0, 170, 250, 370, 630]
for i, r in enumerate(SAT):
    yy = TY + 36 + i * 30
    if i == 0: d.rectangle([TX - 6, yy - 4, TX + 860, yy + 24], fill=(236, 238, 242))
    for j, c in enumerate(r): d.text((TX + CX[j], yy), c, font=(fK if i == 0 else fO), fill=(DOL if "yeter" in c else INK))
    d.line([(TX - 6, yy + 26), (TX + 860, yy + 26)], fill=ACIK, width=1)
d.text((TX, TY + 36 + len(SAT) * 30 + 8), "kompresör bu paftada yok: TOPPING'e ait, yeri açık · K'nin üst bölmesi boşaldı (içecek yedeği alta indi)", font=fXS, fill=GRI)

os.makedirs(os.path.dirname(CIKTI), exist_ok=True)
im.save(CIKTI, optimize=True)
# ---- denetim
cek = {"pide": 0, "lah": 0, "ic": 0, "tat": 0}; ust = {}
for ad, x0, w, y0, grup in KOL:
    y = y0
    for tip, n in grup: cek[tip] += n; y += n * HATVE[tip]
    ust[ad] = y
ic = 2 * 48 + 2 * 32
print("PNG", CIKTI)
print("çekmece: pide %d (=%d top) · lahmacun %d (=%d) · içecek %d kutu · tatlı 18" % (cek["pide"], cek["pide"] * 20, cek["lah"], cek["lah"] * 36, ic))
print("kolon üstleri:", {k: round(v, 1) for k, v in ust.items()}, "≤ tavan 1000:", all(v <= TAVAN for v in ust.values()))
print("pizza yedeği üstü %.0f ≤ 1057: %s · 553 + 567 = %d" % (PZ["y"][1], PZ["y"][1] <= 1057, 553 + 567))
