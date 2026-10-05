# -*- coding: utf-8 -*-
"""AUTOKITCH · ALÇAK HAT · TEKNİK RESİM 1 v3 (27 Eyl 2026) — yalnız teknik resim, model yok.
v3 (Kemal: "indir; her şey var mı eksiksiz; önce teknik resim, 3D'ye geçme"):
  düz çizgi 788 (tam 2 günle en düşük, cekmece_ara4.py) → hat 1862 (−168) · K1 6L · K2 6L · K3 5P · K4 Secop + B panosu + depo · K5 3P + tatlı · K6 3 içecek
  v56'daki 73 birim tek tek yerleştirildi (scratchpad birimler.txt): teknik (robot kontrol, ana pano, UPS) A'da açıcının ÜSTÜNDE arkada
  (açıcı disk + 214'te biter, hat v56 GLB ölçüsü) · deterjan fırın altı şeridinde önde (bulaşığın yanı) · içecek yedeği 6 koli E altında (2 × 3,
  alt raf 618'in altına 3 kat sığar, 4 kat sığmaz) · davlumbaz fırın üstünün arka yarısı (v2'de ÇİZİLMEMİŞTİ) · v1/v2'de robot kontrol ile ana pano üst üste binmişti, düzeltildi.
v2 (Kemal: "içecekleri sağa, hamurları sola; 2 günlük hamur / içecek / tatlı — ne azı ne fazlası, fazlaysa azalt, boş alanı artır"):
  store_cad_v5 kapasiteleri: pide 20/çekmece → 8 = 160 (2 gün 160) · lahmacun 36 → 12 = 432 (2 gün 400; 11 = 396 yetmez)
  içecek şerit 8 kutu, geniş çekmece 6 şerit = 48 → 3 çekmece 144 (2 gün 139; v1 192 FAZLAYDI) · tatlı şerit 6 → 2 şerit 12 (2 gün 11; v1 30 FAZLAYDI)
  K1 5P · K2 1P+5L · K3 1P+5L · K4 soğutma + kaşar/sucuk · K5 1P+2L+tatlı + BOŞ 121 · K6 3 içecek (en sağ, QR tarafı) — scratchpad cekmece_ara4.py
  dış içecek yedeği 4 güne: 277 − 144 = 133 → 6 koli (şerit 2 + E altı 4). Düz çizgi en az 788 olabilir (hat 1862) — bu resimde 809 kaldı.

RESİM 1 (Kemal: "TOPPING ve hamur açma bölgesinin alt hattı fırının alt hattıyla eşit; çekmeceli dolap tek parça istasyon; sek sek olmasın;
sığmayan çekmeceleri sağa, sağdakileri yeniden düzenle: teknik arkaya, kola öne, kutunun altına bir şeyler, sığmayanı fırının üstüne"):
  A, C ve fırının altı AYNI ÇİZGİ 809 · çekmeceli dolap 0–4000 tek parça, üstü düz 809 · fırın bandı 1019 = disk 1021'in 2 altı kalmalı →
  TOPPING / açıcı mekanizması kendi kabininde 104 yukarıda (kaide) · hat 1883. Çekmece dağılımı cekmece_ara3.py (tam arama): K1–K3 tam boy 579,
  fırın altı K5–K6 519 (PU 60), K4 soğutma + kaşar/sucuk deposu.
RESİM 2 (Kemal: "ikinci resimde soldaki motor / kaşar-sucuk kutularını sağa, fırının altındaki daha alçak yere; sola çekmeceleri sığdır, dene"):
  seçenek 2 (alt bant 824, fırın altı 720, hat 1794) + Secop ve depo fırın altında YAN YANA (üst üste 716'ya çıkar, fırın altında 660 var) ·
  K4 yeri dar çekmeceler · sonuç: SIĞIYOR ama soğuk içecek 144 (160 gerek, −16) → dış yedek 6 koli, toplam 288."""
import os
from PIL import Image, ImageDraw, ImageFont

KLASOR = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE".replace("WEBSITE", "WEBS\u0130TE")
S = 0.8
OX, OY = 600, 300
W_PX, H_PX = int(OX + 5430 * S + 780), int(OY + 2030 * S + 470)
BG, INK, GRAY, LINE, ACC, RED = (255, 255, 255), (26, 26, 28), (130, 130, 138), (70, 70, 76), (0, 86, 184), (198, 42, 32)
DOLAP, PUC, SICAK, TURUNCU, KARTON, SOFT, EVC, YESIL = (14, 120, 90), (255, 240, 200), (255, 226, 214), (200, 90, 30), (236, 214, 176), (232, 232, 238), (220, 235, 255), (40, 150, 80)
PITCH = dict(P=108.0, L=93.0, T=104.0, I=159.0)
AD = dict(P="PİDE 20", L="LAHMACUN 36", T="TATLI 12 · 2 şerit", I="İÇECEK 48")


def F(sz, b=False):
    try:
        return ImageFont.truetype("arialbd.ttf" if b else "arial.ttf", sz)
    except Exception:
        return ImageFont.load_default()


f11, f13, f15, f18, f30 = F(15), F(17), F(19), F(22), F(32, True)


def ciz(no):
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

    def txt(x, y, s, f=f13, c=INK, a="mm"):
        d.text((x, y), s, font=f, fill=c, anchor=a)

    def lab(x0, x1, y0, y1, s, f=f13, c=INK):
        satir = s.split("|")
        cy = (fy(y0) + fy(y1)) / 2 - (len(satir) - 1) * 10
        for i, t in enumerate(satir):
            txt((fx(x0) + fx(x1)) / 2, cy + i * 20, t, f, c if i == 0 else GRAY)

    def kolon(ad, a, b, seq, ust=None):
        y = 167.5
        for k in seq:
            p = PITCH[k]
            box(a, b, y, y + p - 3.0, (255, 250, 236) if k in "TI" else BG, DOLAP, 2)
            txt((fx(a) + fx(b)) / 2, (fy(y) + fy(y + p - 3.0)) / 2, AD[k], f11, DOLAP if k in "PL" else TURUNCU)
            y += p
        if ust is not None and ust - y > 15:
            kesik(a + 6, b - 6, y + 3.0, ust, GRAY, 1, 8, 6)
            lab(a, b, y, ust, "BOŞ %.0f" % (ust - y), f13, GRAY)
        txt((fx(a) + fx(b)) / 2, fy(123) + 18, ad, f13, GRAY)

    def olcu_v(x, y0, y1, s, c=INK, sag=True):
        d.line([(x, fy(y0)), (x, fy(y1))], fill=c, width=2)
        for yy in (y0, y1):
            d.line([(x - 8, fy(yy)), (x + 8, fy(yy))], fill=c, width=2)
        txt(x + (14 if sag else -14), (fy(y0) + fy(y1)) / 2, s, f18, c, "lm" if sag else "rm")

    if no == 1:
        LB, FA, DISK, BANT, KT, KB, TEP, TOP, DLT = 788.0, 788.0, 1000.0, 998.0, 892.0, 996.0, 936.0, 1862.0, 168.0
    else:
        LB, FA, DISK, BANT, KT, KB, TEP, TOP, DLT = 824.0, 720.0, 932.0, 930.0, 824.0, 928.0, 868.0, 1794.0, 236.0
    kesik(0, 5430, 0, 2030, RED, 2, 14, 8)
    txt(fx(5430) + 12, fy(2030), "bugün 2030", f15, RED, "lm")
    for x0, x1 in ((0, 4000), (4000, 4600), (4600, 5430)):
        if no == 2 and x0 == 4000:
            continue
        box(x0 + 30, x1 - 30, 0, 123, SOFT, LINE, 1)
    # ================= çekmeceli dolap =================
    if no == 1:
        box(0, 4000, 123, LB, (246, 248, 247), LINE, 4)
        txt(fx(1250), fy(LB) + 22, "ÇEKMECELİ DOLAP · TEK PARÇA 0–4000 · üstü DÜZ %.0f · +3 °C · 24 çekmece" % LB, f15, DOLAP)
        kolon("K1", 62.5, 682.5, "LLLLLL", LB - 62.5)
        kolon("K2", 717.5, 1337.5, "LLLLLL", LB - 62.5)
        kolon("K3", 1372.5, 1992.5, "PPPPP", LB - 62.5)
        box(2011.5, 2500.0, 128.5, 400.5, None, GRAY, 1); lab(2011.5, 2500.0, 128.5, 400.5, "SOĞUTMA Secop · önde|B PANOSU (PLC) arkasında|arkadan servis", f11, INK)
        box(2011.5, 2500.0, 423.0, 669.0, None, GRAY, 1); lab(2011.5, 2500.0, 423.0, 669.0, "KAŞAR + SUCUK|DEPO 2 gün", f11, INK)
        txt((fx(2011.5) + fx(2500)) / 2, fy(123) + 18, "K4", f13, GRAY)
        kolon("K5", 2535.0, 3155.0, "PPPT", FA - 122.5)
        kolon("K6", 3190.0, 3775.0, "III", FA - 122.5)
        box(2517.0, 3793.0, FA - 60.0, FA, PUC, GRAY, 1)
        txt((fx(2517) + fx(3793)) / 2, (fy(FA - 60) + fy(FA)) / 2, "PU 60 · fırın altı ısı kalkanı (dolabın içinde)", f11, GRAY)
        d.line([(fx(3810), fy(126)), (fx(3810), fy(LB))], fill=LINE, width=3)
        for i in range(2):
            box(3832, 3978, 130 + i * 305.0, 430 + i * 305.0, (225, 238, 250), ACC, 2)
        lab(3810, 4000, 130, 430, "DETERJAN|5 L", f11, ACC)
        lab(3810, 4000, 435, 735, "PARLATICI|5 L", f11, ACC)
        txt(fx(3905), fy(LB - 3) + 14, "şerit · önde", f11, GRAY)
    else:
        box(0, 2500, 123, LB, (246, 248, 247), LINE, 3)
        box(2500, 4000, 123, FA, (246, 248, 247), LINE, 3)
        txt(fx(1250), fy(LB) + 22, "ÇEKMECELİ DOLAP 0–4000 · üstü 824 (fırın altında 720) · +3 °C", f15, DOLAP)
        kolon("K1", 62.5, 682.5, "PPLLLL")
        kolon("K2", 717.5, 1337.5, "PPLLLL")
        kolon("K3", 1372.5, 1992.5, "PPLLLL")
        kolon("K4", 2011.5, 2500.0, "TIII")
        kolon("K5", 2535.0, 3155.0, "PPI")
        box(3190.0, 3610.0, 128.5, 400.5, None, GRAY, 2); lab(3190.0, 3610.0, 128.5, 400.5, "SOĞUTMA Secop|sıcak bölme|arkadan servis", f11, INK)
        box(3620.0, 3985.0, 130.0, 360.0, None, GRAY, 2); lab(3620.0, 3985.0, 130.0, 360.0, "KAŞAR + SUCUK|DEPO|GN yan", f11, INK)
        txt((fx(3190) + fx(3985)) / 2, fy(123) + 18, "K6 · yan yana", f13, GRAY)
        box(2517.0, 3990.0, FA - 60.0, FA, PUC, GRAY, 1)
        txt((fx(2517) + fx(3990)) / 2, (fy(FA - 60) + fy(FA)) / 2, "PU 60 · fırın altı ısı kalkanı", f11, GRAY)
        lab(3190, 3985, 430, 640, "üstü boş (üst üste konsa 716'ya çıkar,|fırın altında 660 var)", f11, GRAY)
    # ================= A + C =================
    box(0, 700, LB, TOP, (250, 250, 252), LINE, 3)
    box(700, 2500, LB, TOP, (250, 250, 252), LINE, 3)
    if no == 1:
        for x0, x1 in ((0, 700), (700, 2500)):
            box(x0 + 8, x1 - 8, LB + 3, LB + 104, (242, 242, 246), GRAY, 1)
        txt(fx(1250), (fy(LB) + fy(LB + 104)) / 2, "mekanizma kaidesi 104 (disk %.0f = fırın bandı %.0f + 2)" % (DISK, BANT), f11, GRAY)
    lab(0, 700, LB + 110, DISK - 30, "A · AÇICI", f15)
    lab(700, 2500, DISK + 250, DISK + 600, "C · TOPPING|içi aynı (uno v11) · disk %.0f" % DISK, f15)
    d.line([(fx(700), fy(DISK)), (fx(2500), fy(DISK))], fill=ACC, width=3)
    _pu = [(733, 1277 - DLT), (733, 2028 - DLT), (1520, 2028 - DLT), (1520, 1720 - DLT), (2467, 1720 - DLT), (2467, 1277 - DLT)]
    d.polygon([(fx(x_), fy(y_)) for x_, y_ in _pu], outline=(230, 190, 90))
    # A üstü: arkada teknik (robot kontrol + ana pano [+ UPS resim 2]) · önde temizlik (resim 2)
    if no == 2:
        box(40, 660, TOP - 560, TOP - 330, (255, 244, 230), LINE, 2); lab(40, 660, TOP - 560, TOP - 330, "TEMİZLİK · önde|2 × 5 L · bez · eldiven · poşet", f13)
        kesik(530, 645, TOP - 320, TOP - 107, GRAY, 2); lab(530, 645, TOP - 320, TOP - 107, "UPS", f11, GRAY)
    if no == 1:
        AC = DISK + 214.0                                   # açıcı sacının üstü (v56 GLB: 1382 = disk 1168 + 214)
        box(160, 540, DISK - 22.0, AC, None, INK, 2); lab(160, 540, DISK, AC, "AÇICI|üstü %.0f" % AC, f11)
        kesik(20, 495, AC + 10, AC + 278, GRAY, 2); lab(20, 495, AC + 10, AC + 278, "ROBOT KONTROL · arkada|475 × 423 × 268", f11, GRAY)
        kesik(20, 420, AC + 288, AC + 638, GRAY, 2); lab(20, 420, AC + 288, AC + 638, "ANA PANO · arkada|400 × 250 × 350", f11, GRAY)
        kesik(440, 555, AC + 288, AC + 501, GRAY, 2); lab(440, 555, AC + 288, AC + 501, "UPS|arkada", f11, GRAY)
        lab(560, 690, AC + 400, AC + 500, "üstte|boşluk %.0f" % (TOP - 1.5 - (AC + 638)), f11, GRAY)
    else:
        kesik(40, 515, TOP - 320, TOP - 52, GRAY, 2); lab(40, 515, TOP - 320, TOP - 180, "ROBOT KONTROL · arkada|475 × 268 (V)", f11, GRAY)
        kesik(90, 490, TOP - 170, TOP - 20, GRAY, 1); lab(90, 490, TOP - 170, TOP - 20, "ANA PANO · arkada", f11, GRAY)
    # ================= F =================
    box(2500, 4000, FA, FA + 517.0, SICAK, TURUNCU, 3)
    lab(2500, 4000, FA + 100, FA + 420, "F · TP10 FIRIN 1500 · 79 öne|gövde %.0f–%.0f · bant %.0f" % (FA, FA + 517, BANT), f15)
    d.line([(fx(2560), fy(BANT)), (fx(3996), fy(BANT))], fill=TURUNCU, width=4)
    RAF = FA + 517.0 + 43.0
    box(2510, 3990, RAF - 4.0, RAF, INK, INK, 1)
    box(2520, 3324, RAF, RAF + 512.0, KARTON, LINE, 2); lab(2520, 3324, RAF, RAF + 512.0, "PİZZA KUTUSU YEDEĞİ 320", f13)
    box(3600, 3980, RAF, RAF + 510.0, EVC, ACC, 2); lab(3600, 3980, RAF, RAF + 510.0, "KOMPRESÖR", f13, ACC)
    if no == 1:
        for i in range(2):
            box(3336 + i * 132, 3466 + i * 132, RAF, RAF + 290.0, (255, 244, 230), LINE, 2)
        lab(3336, 3598, RAF, RAF + 290.0, "TEMİZLİK|2 × 5 L", f11)
        box(3336, 3594, RAF + 300.0, RAF + 450.0, (255, 244, 230), LINE, 2); lab(3336, 3594, RAF + 300, RAF + 450, "bez · eldiven|poşet", f11)
        kesik(2508, 3992, FA + 527.0, TOP - 3.0, GRAY, 2, 16, 10)
        txt(fx(3467), fy(TOP - 3.0) + 14, "DAVLUMBAZ · arkada yarı", f11, GRAY)
    else:
        for i in range(3):
            box(3330, 3597, RAF + i * 123.0, RAF + 122.0 + i * 123.0, KARTON, LINE, 2)
        lab(3330, 3597, RAF + 380, RAF + 480, "İÇECEK 3 koli|sığmayan → fırın üstü", f11, RED)
    # ================= K =================
    box(4000, 4600, 123, TOP, (250, 250, 252), LINE, 3)
    box(4000, 4600, KT - 3.0, KT, INK, INK, 1)
    if no == 1:
        box(4070, 4530, 126, 826, (245, 247, 250), INK, 3); lab(4070, 4530, 300, 700, "BULAŞIK MAKİNESİ · önde|MEIKO M-iClean US|üstü %.0f, K tabanı %.0f" % (826, KT - 3), f13)
    else:
        box(4070, 4530, 0, 700, (245, 247, 250), INK, 3); lab(4070, 4530, 250, 600, "BULAŞIK MAKİNESİ · önde|MEIKO M-iClean US|YERDE (K altında kaide yok:|kaide 123 + 700 = 823 > taban 821)", f13)
    d.line([(fx(4010), fy(KB)), (fx(4597), fy(KB))], fill=ACC, width=4)
    box(4185, 4415, 1290 - DLT, 1702 - DLT, None, INK, 2); lab(4185, 4415, 1290 - DLT, 1702 - DLT, "KESİCİ + SPREY", f11)
    kesik(4054, 4226, 1635 - DLT, 1980 - DLT, RED, 2); lab(4054, 4226, 1635 - DLT, 1980 - DLT, "YAĞ 3 L", f11, RED)
    kesik(4300, 4565, 1640 - DLT, 2025 - DLT, GRAY, 2); lab(4300, 4565, 1640 - DLT, 2025 - DLT, "PANO|arkada", f11, GRAY)
    txt(fx(4300), fy(TOP) + 24, "K · KESME + SPREY", f15)
    # ================= E =================
    box(4600, 5430, 123, TOP, (250, 250, 252), LINE, 3)
    kesik(4608, 5412, 240, 1148 - DLT, GRAY, 2)
    lab(4608, 5412, 790 - DLT + 60, 1148 - DLT, "KUTU ŞARJÖRÜ (arkada) 240–%.0f · %d kutu (bugün 567)" % (1148 - DLT, round((908 - DLT) / 1.6)), f11, RED)
    box(4602, 5428, 1085 - DLT, 1330 - DLT, (253, 244, 243), RED, 3); lab(4602, 5428, 1085 - DLT, 1330 - DLT, "KUTULAMA AĞZI · tepsi %.0f" % TEP, f13, RED)
    box(4604, 5400, 790 - DLT - 4.0, 790 - DLT, INK, INK, 1); txt(fx(5000), fy(790 - DLT) - 14, "alt raf %.0f" % (790 - DLT), f11, INK)
    if no == 1:
        for c_ in range(2):
            for i in range(3):
                box(4612 + c_ * 402, 5012 + c_ * 402, 130 + i * 123, 252 + i * 123, KARTON, LINE, 2)
        txt((fx(4612) + fx(5414)) / 2, fy(520), "İÇECEK YEDEĞİ 6 koli × 24 = 144 · önde (2 × 3)", f11, INK)
    else:
        for i in range(2):
            box(4615 + i * 132, 4745 + i * 132, 130, 420, (225, 238, 250), ACC, 2)
        lab(4615, 4877, 130, 420, "DETERJAN|+ parlatıcı|önde", f11, ACC)
        nk = 3
        for i in range(nk):
            box(4895, 5295, 130 + i * 123, 252 + i * 123, KARTON, LINE, 2)
        lab(4895, 5295, 130 + (nk - 1) * 123, 252 + (nk - 1) * 123, "İÇECEK %d koli · önde" % nk, f11)
    box(4620, 5410, 1300 - DLT + 50, TOP - 10, None, GRAY, 1); lab(4620, 5410, 1300 - DLT + 50, TOP - 10, "BESLEYİCİ · PİSTON · PANO (arkada)", f11, GRAY)
    txt(fx(5015), fy(TOP) + 24, "E · KUTU KATLAMA", f15)
    # ================= düz çizgi + ölçüler =================
    if no == 1:
        X0 = fx(0)
        x = X0
        while x < fx(4000):
            d.line([(x, fy(LB)), (min(x + 18, fx(4000)), fy(LB))], fill=YESIL, width=4); x += 28
        txt(fx(-20), fy(LB), "DÜZ ÇİZGİ %.0f" % LB, f15, YESIL, "rm")
    olcu_v(fx(0) - 170, 0, TOP, "%.0f" % TOP, INK, False)
    olcu_v(fx(0) - 290, 0, 2030, "2030 (bugün)", RED, False)
    olcu_v(fx(5430) + 70, TOP, 2030, "−%.0f" % (2030 - TOP), RED, True)
    kotlar = [(123, "123"), (FA, "%.0f fırın altı" % FA), (TEP, "%.0f kutu tepsisi" % TEP), (DISK, "%.0f–%.0f süreç (K bandı · fırın bandı · disk)" % (KB, DISK)), (TOP, "%.0f" % TOP)]
    kotlar.append((LB, "%.0f dolap üstü = A / C / fırın altı" % LB) if no == 1 else (LB, "%.0f dolap üstü · K tabanı" % LB))
    for yy, s in kotlar:
        if no == 1 and s == "%.0f fırın altı" % FA:
            continue
        d.line([(fx(5430) + 150, fy(yy)), (fx(5430) + 170, fy(yy))], fill=INK, width=2)
        txt(fx(5430) + 178, fy(yy), s, f13, INK, "lm")
    for x0, x1, s in ((0, 700, "700"), (700, 2500, "1800"), (2500, 4000, "1500"), (4000, 4600, "600"), (4600, 5430, "830")):
        d.line([(fx(x0), fy(TOP) - 60), (fx(x1), fy(TOP) - 60)], fill=INK, width=2)
        for xx in (x0, x1):
            d.line([(fx(xx), fy(TOP) - 70), (fx(xx), fy(TOP) - 50)], fill=INK, width=2)
        txt((fx(x0) + fx(x1)) / 2, fy(TOP) - 74, s, f18, INK, "md")
    d.line([(fx(0), fy(0) + 60), (fx(4000), fy(0) + 60)], fill=DOLAP, width=2)
    txt(fx(2000), fy(0) + 82, "çekmeceli dolap 4000 (K1–K6)", f15, DOLAP)
    d.line([(fx(0), fy(0) + 110), (fx(5430), fy(0) + 110)], fill=INK, width=2)
    txt(fx(2715), fy(0) + 134, "HAT 5430 (aynı)", f18, INK)
    if no == 1:
        bas = "AUTOKITCH  ·  ALÇAK HAT  ·  TEKNİK RESİM 1 v3  ·  düz çizgi 788  ·  hamur solda, içecek + tatlı sağda  ·  tam 2 gün  ·  hat 1862 (−168)"
        alt = "soğukta tam 2 gün: pide 8 × 20 = 160 · lahmacun 12 × 36 = 432 (400) · içecek 3 × 48 = 144 (139) · tatlı 12 (11) · dışarıda içecek 6 koli (4 gün 277) · v56'daki 73 birimin hepsi yerinde · düz = önde · kesik = arkada · mm · 27 Eylül 2026"
    else:
        bas = "AUTOKITCH  ·  ALÇAK HAT  ·  TEKNİK RESİM 2  ·  soğutma + kaşar/sucuk SAĞDA fırın altında (yan yana)  ·  çekmeceler solda  ·  hat 1794"
        alt = "SIĞIYOR, TEK AÇIK: soğuk içecek 144 (2 gün için 160 gerek: −16) → dış yedek 6 koli, toplam 288 = 4 gün · 3 koli fırın üstünde (sığmayan) · düz = önde · kesik = arkada · mm · 27 Eylül 2026"
    txt(OX, 60, bas, f30, INK, "la")
    txt(OX, 112, alt, f15, GRAY, "la")
    d.line([(OX, 150), (W_PX - 80, 150)], fill=LINE, width=3)
    ad = "ALCAK_HAT_RESIM%d_v3" % no
    im.save(os.path.join(KLASOR, ad + ".png"), optimize=True)
    im.save(os.path.join(KLASOR, ad + ".pdf"), "PDF", resolution=150.0)
    print("yazildi", ad)


if __name__ == "__main__":
    ciz(1)
