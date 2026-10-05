# -*- coding: utf-8 -*-
"""AUTOKITCH · açıklama çizimi v1 (27 Eyl 2026 gece) — Kemal: "enerji zincirini anlamadım, QR'ı da anlamadım".
Yalnız kesitler + ölçü + ad; açıklama mesajda. Değerler: ray_ek_cad_v1 (zincir U döngüsü 340, üst kol y 302–342, z 498–562, oluk z 485–575 y 0–60),
store_cad_v6 (K1 lahmacun çekmeceleri adım 93, ilk ön 167,5, açık strok 628), qr_cad_v1 (göz 380 × 190, taban 3 mm düz), kutu_cad_v5 (çatal dişi 26 × 8 × 430, 3 diş).
"""
import os
from PIL import Image, ImageDraw, ImageFont

KL = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\FULL_MAKINE"
W, H = 4200, 1500
BG, INK, GRAY, LINE, RED, ACC, ORN, GRN = (255, 255, 255), (26, 26, 28), (130, 130, 138), (70, 70, 76), (198, 42, 32), (0, 86, 184), (225, 110, 0), (14, 120, 90)


def F(sz, b=False):
    try:
        return ImageFont.truetype("arialbd.ttf" if b else "arial.ttf", sz)
    except Exception:
        return ImageFont.load_default()


f13, f16, f20, f24, f30 = F(17), F(20), F(24), F(28, True), F(34, True)
im = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(im)


def T(x, y, s, f=f16, c=INK, a="mm"):
    d.text((x, y), s, font=f, fill=c, anchor=a)


def kesit(ox, oy, s, baslik, durum):
    """Yan kesit (z yatay, y dikey) — K1 önü, koridor. durum: 'dik' | 'yatik' | 'araba'."""
    X = lambda z: ox + (z + 300) * s
    Y = lambda y: oy - y * s
    T(ox, Y(1000), baslik, f24, INK, "la")
    d.line([(X(-300), Y(0)), (X(900), Y(0))], fill=INK, width=3)
    # dolap kesiti (z −300…0 gösterilir)
    d.rectangle([X(-300), Y(788), X(0), Y(123)], outline=LINE, width=3)
    for i in range(6):
        y0 = 167.5 + i * 93
        d.rectangle([X(-280), Y(y0 + 87), X(0), Y(y0)], outline=GRN, width=2)
    # açık 2. çekmece
    y2 = 167.5 + 93
    d.rectangle([X(0), Y(y2 + 87), X(628), Y(y2)], outline=GRN, width=4, fill=(225, 243, 236))
    T((X(0) + X(628)) / 2, (Y(y2 + 87) + Y(y2)) / 2, "açık 2. çekmece (628 dışarı)", f13, GRN)
    # ray + araba + robot kaidesi
    d.rectangle([X(240), Y(60), X(480), Y(0)], fill=(250, 226, 200), outline=ORN, width=2)
    T((X(240) + X(480)) / 2, (Y(60) + Y(0)) / 2, "ray", f13, ORN)
    T((X(240) + X(480)) / 2, Y(90), "robot yanda", f13, GRAY)
    if durum == "dik":
        d.rectangle([X(485), Y(60), X(575), Y(0)], outline=ORN, width=2)
        d.rectangle([X(498), Y(342), X(562), Y(302)], fill=(255, 200, 160), outline=RED, width=4)
        d.rectangle([X(498), Y(42), X(562), Y(2)], fill=(255, 220, 190), outline=ORN, width=2)
        d.arc([X(498) - 40, Y(342), X(562) + 40, Y(2)], 0, 360, fill=ORN, width=1)
        T(X(620), Y(322), "zincirin üst kolu 302–342", f13, RED, "lm")
        T(X(620), Y(22), "alt kol (olukta)", f13, ORN, "lm")
        d.line([(X(530), Y(342)), (X(530), Y(2))], fill=RED, width=2)
        T(X(505), Y(172), "340", f16, RED, "rm")
        T(X(300), Y(-60), "ÇARPIŞIR: çekmece 260–348 ↔ zincir 302–342", f16, RED, "mm")
    elif durum == "yatik":
        d.rectangle([X(485), Y(60), X(839), Y(0)], outline=ORN, width=3, fill=(255, 236, 214))
        T((X(485) + X(839)) / 2, Y(30), "zincir yan yatık · 60", f13, ORN)
        T(X(300), Y(-60), "SERBEST: zincir 0–60 · en alt çekmece 167,5'ten başlar", f16, GRN, "mm")
        T((X(485) + X(839)) / 2, Y(150), "oluk z 485–839 (354 geniş)", f13, ORN)
    else:
        d.rectangle([X(485), Y(140), X(575), Y(0)], outline=ORN, width=3, fill=(255, 236, 214))
        T((X(485) + X(575)) / 2, Y(70), "ince", f13, ORN)
        T(X(600), Y(120), "yalnız 230 V + ağ + acil stop", f13, ORN, "lm")
        T(X(600), Y(90), "döngü ~140 (VARSAYIM R 50)", f13, ORN, "lm")
        T(X(600), Y(200), "robot kutusu robot arabasında, robotla gider", f13, ORN, "lm")
        T(X(300), Y(-60), "SERBEST: ince zincir < 167,5", f16, GRN, "mm")
    T(X(-150), Y(830), "çekmeceli dolap (K1)", f13, GRAY)
    T(X(700), Y(830), "koridor", f13, GRAY)


S = 0.62
kesit(80, 1180, S, "1 · ŞİMDİ: dik U zincir", "dik")
kesit(820, 1180, S, "2 · SEÇENEK: zincir yere yan yatık", "yatik")
kesit(1560, 1180, S, "3 · SEÇENEK: robot kutusu robot arabasında", "araba")


def goz(ox, oy, s, baslik, yuva):
    X = lambda x: ox + x * s
    Y = lambda y: oy - y * s
    T(ox, oy - 260 * s - 40, baslik, f24, INK, "la")
    d.rectangle([X(0), Y(190), X(380), Y(0)], outline=LINE, width=3)
    T(X(190), Y(205), "göz 380 × 190 (önden kesit)", f13, GRAY)
    dis = [110, 190, 270]
    if not yuva:
        d.rectangle([X(0), Y(0), X(380), Y(-3)], fill=INK)
        ky = 8.0
        for x in dis:
            d.rectangle([X(x - 13), Y(ky), X(x + 13), Y(0)], fill=ORN)
        T(X(380) + 20, Y(4), "çatal dişleri (3 × 26 × 8)", f13, ORN, "lm")
        d.rectangle([X(30), Y(ky + 44), X(350), Y(ky)], outline=ACC, width=3, fill=(220, 235, 255))
        T(X(190), Y(ky + 22), "kutu 320 × 44", f13, ACC)
        T(X(190), Y(-30), "düz taban: kutu dişlerin üstünde kalır → çatal çekilince kutuyu da sürükler", f13, RED)
    else:
        d.rectangle([X(0), Y(0), X(380), Y(-3)], fill=INK)
        for x in dis:
            d.rectangle([X(x - 20), Y(0), X(x + 20), Y(-16)], fill=BG, outline=INK, width=2)
            d.rectangle([X(x - 13), Y(-4), X(x + 13), Y(-12)], fill=ORN)
        T(X(380) + 20, Y(-8), "dişler yuvada", f13, ORN, "lm")
        d.rectangle([X(30), Y(44), X(350), Y(0)], outline=ACC, width=3, fill=(220, 235, 255))
        T(X(190), Y(22), "kutu 320 × 44", f13, ACC)
        T(X(190), Y(-40), "tabanda 3 yuva (40 × 16): dişler yuvaya iner, kutu tabana oturur, çatal boş çekilir", f13, GRN)
    T(X(dis[0]), Y(-70) if yuva else Y(-60), "", f13)


goz(2800, 700, 1.6, "4 · QR GÖZÜ ŞİMDİ: taban düz", False)
goz(2800, 1320, 1.6, "5 · ÖNERİ: tabanda çatal yuvası", True)
T(80, 60, "AUTOKITCH  ·  AÇIKLAMA  ·  enerji zinciri (K1 önünden yan kesit)  ·  QR gözü (önden kesit)  ·  mm  ·  27 Eylül 2026", f30, INK, "la")
d.line([(80, 110), (W - 80, 110)], fill=LINE, width=3)
ad = "ACIKLAMA_zincir_goz_v1"
im.save(os.path.join(KL, ad + ".png"), optimize=True)
print("yazildi", ad)
