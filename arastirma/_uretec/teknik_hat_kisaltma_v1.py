# -*- coding: utf-8 -*-
"""AUTOKITCH · A SECENEGI HAT KISALTMA ALTERNATIFLERI · TEKNIK RESIM v1 (20 Eyl 2026)
Kemal 20 Eyl: "atosa tabanli konveyor 4 urunlu firin icin boyunu nasil kucultebiliriz birkac alternatif cizim yap,
hatti bozmaman lazim, yuksekligini degisebilirsin cunku cok kullanmadigimiz yer var; birde depo yerlerimiz varya
yedek icecekler kutular ups filan geri kalan hersey onun icine koy baska bir secenekte."

BASLANGIC (A secenegi · olculen 58 urun/saat 2 robot · 42 tek robot):
  A PRESS 0-700 | B CEKMECE 0-2500 (alt) | C TOPPING 700-2500 | F KONVEYOR FIRIN 2500-4000 | K KESME 4000-4600 | E KUTU 4600-5300
  HAT 5300 x 2030 x 830 · surec kotu 1340 · dukkan ici 3900 (1400 fazla)

Bu pafta yalnizca YERLESIM KARSILASTIRMASI gosterir: her alternatifin modul serisi, kazanilan mm, bos hacim kullanimi.
Ayrintili istasyon kesitleri mevcut HAT_ATOSA_TABLALI_v2 paftasindadir.
Kural: paftada yalniz gorunus + olcu + parca adi; aciklama mesajda.
"""
import io, os, sys
from PIL import Image, ImageDraw, ImageFont

KLASOR = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX = 4800, 6200
BG, INK, GRAY, LINE = (255, 255, 255), (26, 26, 28), (132, 132, 140), (72, 72, 78)
FILL, ACC, RED, SOFT = (244, 244, 246), (0, 86, 184), (198, 42, 32), (228, 228, 234)
YESIL, TURUNCU, MOR, SARI = (23, 138, 86), (200, 90, 30), (124, 84, 200), (246, 238, 200)
SICAK, URUN, BUZ, DOLAP = (255, 226, 214), (240, 214, 170), (28, 86, 166), (14, 120, 90)


def F(sz, b=False):
    for n in (("arialbd.ttf", "segoeuib.ttf") if b else ("arial.ttf", "segoeui.ttf")):
        try:
            return ImageFont.truetype(n, sz)
        except Exception:
            pass
    return ImageFont.load_default()


f8, f9, f11, f13, f16, f22, f40 = F(16), F(18), F(21), F(24), F(28, True), F(38, True), F(56, True)
im = Image.new("RGB", (W_PX, H_PX), BG)
d = ImageDraw.Draw(im)


def txt(x, y, s, f=None, c=INK, a="la"):
    d.text((x, y), s, font=f or f11, fill=c, anchor=a)


def sayi(v):
    return ("%d" % round(v)) if abs(v - round(v)) < 0.05 else ("%.1f" % v).replace(".", ",")


def olcu_h(x0, x1, y, s, f=None, c=INK):
    d.line([(x0, y), (x1, y)], fill=c, width=2)
    for x in (x0, x1):
        d.line([(x, y - 9), (x, y + 9)], fill=c, width=2)
    txt((x0 + x1) / 2, y - 13, s, f or f9, c, "md")


def olcu_v(x, y0, y1, s, f=None, c=INK):
    d.line([(x, y0), (x, y1)], fill=c, width=2)
    for y in (y0, y1):
        d.line([(x - 9, y), (x + 9, y)], fill=c, width=2)
    txt(x - 12, (y0 + y1) / 2, s, f or f9, c, "rm")


def tarali(x0, y0, x1, y1, c=(222, 222, 228), adim=13):
    x0, x1 = min(x0, x1), max(x0, x1)
    y0, y1 = min(y0, y1), max(y0, y1)
    v = x0 - (y1 - y0)
    while v < x1:
        d.line([(max(x0, v), y1 - max(0, v - x0)), (min(x1, v + (y1 - y0)), y0 + max(0, (v + (y1 - y0)) - x1))], fill=c, width=1)
        v += adim


# ======================= ALTERNATIFLER =======================
# her modul: (ad, x0, genislik, y0, y1, renk, not)
DERIN, YUK = 830.0, 2030.0

MEVCUT = dict(
    ad="MEVCUT  ·  A SEÇENEĞİ", boy=5300.0, yuk=2030.0, kapasite="58 (2 robot) · 42 (1 robot)",
    kazanc=0.0,
    moduller=[
        ("A · PRES KAFASI", 0, 700, 1060, 2030, FILL),
        ("B · ÇEKMECE (A ve C'nin altı)", 0, 2500, 0, 1060, SOFT),
        ("C · TOPPING · 6 hazne tek sıra", 700, 1800, 1060, 2030, FILL),
        ("F · KONVEYÖR FIRIN · hazne 1400", 2500, 1500, 0, 2030, SICAK),
        ("K · KESME + SPREY", 4000, 600, 0, 2030, FILL),
        ("E · KUTU", 4600, 700, 0, 2030, FILL),
    ],
    notlar=["hat dükkâna 1400 mm sığmıyor", "boş hacim 5476 L · %51", "depo (1311 L) hattın dışında"],
)

ALT1 = dict(
    ad="ALT-1  ·  KESME KUTUNUN İÇİNE", boy=4700.0, yuk=2030.0, kapasite="tahmin 56–58",
    kazanc=600.0,
    moduller=[
        ("A · PRES KAFASI", 0, 700, 1060, 2030, FILL),
        ("B · ÇEKMECE", 0, 2500, 0, 1060, SOFT),
        ("C · TOPPING · 6 hazne tek sıra", 700, 1800, 1060, 2030, FILL),
        ("F · KONVEYÖR FIRIN · hazne 1400", 2500, 1500, 0, 2030, SICAK),
        ("KE · KESME + KUTU tek gövde", 4000, 700, 0, 2030, YESIL),
    ],
    notlar=["kesme plakası kutu ağzının 250 mm üstünde, aynı x'te",
            "bıçak + sprey + itici aynı kolonda üst üste",
            "kutu şarjörü kesme plakasının arkasına (z 60–400) kayar"],
)

ALT2 = dict(
    ad="ALT-2  ·  HAZNE SIRASI İKİ KATA", boy=4770.0, yuk=2030.0, kapasite="tahmin 56–58",
    kazanc=530.0,
    moduller=[
        ("A · PRES KAFASI", 0, 700, 1060, 2030, FILL),
        ("B · ÇEKMECE", 0, 1970, 0, 1060, SOFT),
        ("C · TOPPING · 2 kat × 3 hazne", 700, 1270, 1060, 2030, MOR),
        ("F · KONVEYÖR FIRIN · hazne 1400", 1970, 1500, 0, 2030, SICAK),
        ("K · KESME", 3470, 600, 0, 2030, FILL),
        ("E · KUTU", 4070, 700, 0, 2030, FILL),
    ],
    notlar=["6 hazne tek sırada 1300 mm yer kaplıyordu → 2 kat × 3 hazne = 770 mm",
            "üst kat 1660–2030, alt kat 1270–1640; dozaj başlığı tek nokta, tabla altından geçer",
            "üst kat kaset değişimi 1900 kotunda — eleman erişimi rahat"],
)

ALT3 = dict(
    ad="ALT-3  ·  İKİSİ BİRDEN (kesme+kutu tek gövde · hazne 2 kat)", boy=4170.0, yuk=2030.0, kapasite="tahmin 55–58",
    kazanc=1130.0,
    moduller=[
        ("A · PRES KAFASI", 0, 700, 1060, 2030, FILL),
        ("B · ÇEKMECE", 0, 1970, 0, 1060, SOFT),
        ("C · TOPPING · 2 kat × 3 hazne", 700, 1270, 1060, 2030, MOR),
        ("F · KONVEYÖR FIRIN · hazne 1400", 1970, 1500, 0, 2030, SICAK),
        ("KE · KESME + KUTU tek gövde", 3470, 700, 0, 2030, YESIL),
    ],
    notlar=["ALT-1 + ALT-2 birlikte · hat 5300 → 4170 mm",
            "dükkâna hâlâ 270 mm fazla — ray sol ucu 200'den 0'a çekilirse sığar",
            "akış sırası hiç bozulmadı: pres → dozaj → fırın → kesme → kutu → QR"],
)

ALT4 = dict(
    ad="ALT-4  ·  HER ŞEYİ KAPSAYAN (depo hat içinde)", boy=4170.0, yuk=2030.0, kapasite="tahmin 55–58",
    kazanc=1130.0,
    moduller=[
        ("A · PRES KAFASI", 0, 700, 1060, 2030, FILL),
        ("B · ÇEKMECE + 3 GÜN HAMUR", 0, 1970, 0, 1060, SOFT),
        ("C · TOPPING 2 kat + ÜST DEPO", 700, 1270, 1060, 2030, MOR),
        ("F · KONVEYÖR FIRIN + YAN DEPO", 1970, 1500, 0, 2030, SICAK),
        ("KE · KESME + KUTU + ŞARJÖR DEPO", 3470, 700, 0, 2030, YESIL),
    ],
    notlar=["depo 1311 L tamamen hat içinde: ayrı depo ihtiyacı SIFIR",
            "içecek 7 gün 89 L → K altı · kutu 3 gün 378 L → E arkası + üstü",
            "UPS + pano 268 L → F tabanı · tatlı 71 L · peçete/poşet 89 L · kaset 145 L",
            "hamur 3 gün açığı 271 L → K1 ve K3'e 7. sıra soğuk çekmece"],
)

SIRA = [MEVCUT, ALT1, ALT2, ALT3, ALT4]

# ======================= CIZIM =======================
OX, OY, S = 300.0, 620.0, 0.30
SATIR_H = 1020.0

txt(OX, 120, "AUTOKITCH  ·  A SEÇENEĞİ HAT KISALTMA ALTERNATİFLERİ  ·  TEKNİK RESİM  v1", f40, INK)
txt(OX, 196, "Atosa tablalı + konveyör fırın 4 ürün  ·  ön görünüş şeması, modül serileri  ·  akış sırası hiçbir alternatifte bozulmadı  ·  derinlik 830 mm sabit  ·  ölçüler mm  ·  20 Eylül 2026", f13, GRAY)
txt(OX, 232, "dükkân içi kullanılabilir boy 3900  ·  kapasite tahminleri 3D sim ölçümünden türetildi (ölçülmüş değer yalnız MEVCUT satırındadır)", f13, RED)

for i, A in enumerate(SIRA):
    y0 = OY + i * SATIR_H
    yb = y0 + YUK * S                                       # taban cizgisi
    # satir basligi
    d.rectangle([OX - 30, y0 - 84, OX + 1640, y0 - 30], fill=(ACC if i == 0 else YESIL) if i != 0 else (30, 40, 56))
    txt(OX - 14, y0 - 57, A["ad"], f16, BG, "lm")
    txt(OX + 1680, y0 - 57, "HAT %s × %s × %s" % (sayi(A["boy"]), sayi(A["yuk"]), sayi(DERIN)), f16, INK, "lm")
    if A["kazanc"] > 0:
        txt(OX + 2560, y0 - 57, "−%s mm" % sayi(A["kazanc"]), f22, YESIL, "lm")
    txt(OX + 2860, y0 - 57, "kapasite: %s ürün/saat" % A["kapasite"], f16, TURUNCU, "lm")

    # dukkan siniri
    dx = OX + 3900.0 * S
    d.line([(dx, y0 - 14), (dx, yb + 54)], fill=RED, width=3)
    txt(dx + 8, y0 - 6, "dükkân içi 3900", f8, RED, "la")

    # moduller
    for ad, x0m, w, my0, my1, renk in A["moduller"]:
        x0, x1 = OX + x0m * S, OX + (x0m + w) * S
        ya, yb2 = yb - my1 * S, yb - my0 * S
        d.rectangle([x0, ya, x1, yb2], fill=renk, outline=LINE, width=3)
        if renk is SICAK:
            tarali(x0 + 3, ya + 3, x1 - 3, yb2 - 3, (235, 190, 160), 14)
        kisa = ad.split(" · ")[0]
        txt((x0 + x1) / 2, (ya + yb2) / 2 - 10, kisa, f11, INK, "mm")
        if " · " in ad:
            txt((x0 + x1) / 2, (ya + yb2) / 2 + 12, ad.split(" · ", 1)[1], f8, GRAY, "mm")
        olcu_h(x0, x1, yb + 30, sayi(w), f8, INK)

    # hat toplam olcusu
    olcu_h(OX, OX + A["boy"] * S, yb + 74, "HAT %s" % sayi(A["boy"]), f13, INK)
    olcu_v(OX - 26, yb - YUK * S, yb, sayi(YUK), f8, GRAY)
    # surec kotu
    d.line([(OX - 10, yb - 1340.0 * S), (OX + A["boy"] * S + 30, yb - 1340.0 * S)], fill=BUZ, width=2)
    txt(OX + A["boy"] * S + 38, yb - 1340.0 * S, "süreç kotu 1340", f8, BUZ, "lm")
    # notlar
    txt(OX + 1760, y0 + 8, "NOTLAR", f11, ACC, "la")
    for j, n in enumerate(A["notlar"]):
        txt(OX + 1760, y0 + 40 + j * 40, "· " + n, f11, INK, "la")

# lejant
ly = OY + len(SIRA) * SATIR_H + 40
txt(OX, ly, "OKUMA", f16, ACC)
for j, s_ in enumerate([
    "MEVCUT satırı ölçülmüş değerdir (3D sim, tam yük 2. saat, içecek + tatlı dahil). Alt satırlardaki kapasite TAHMİNDİR: yerleşim değişiyor, akış ve makine süreleri aynı kalıyor.",
    "ALT-1 kesme plakasını kutu ağzının üstüne alır — iki modül tek gövde olur, 600 mm kazanılır. Robotun kutu → QR yolu 600 mm kısalır.",
    "ALT-2 altı hazneyi tek sıradan iki kata çıkarır (3 üst + 3 alt). Tabla yine tek kotta gezer, dozaj başlığı tek noktadır; hazne kasetleri önden takılır.",
    "ALT-3 ikisini birleştirir: 4170 mm. Dükkâna 270 mm fazla — ray sol ucu 200'den 0'a çekilirse tam oturur.",
    "ALT-4 ALT-3'ün üstüne depoyu ekler: yedek içecek, kutu, UPS, pano, tatlı, peçete, poşet, kaset ve 3 günlük hamur açığı hattın kendi boş hacimlerine girer (1311 L / 3972 L).",
]):
    txt(OX, ly + 44 + j * 34, "· " + s_, f11, INK)

yol = os.path.join(KLASOR, "HAT_KISALTMA_v1_teknik.png")
im.save(yol, dpi=(200, 200))
print("yazildi:", yol)
