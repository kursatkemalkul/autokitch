# -*- coding: utf-8 -*-
"""AUTOKITCH - HAT 2 KOL · TEKNIK RESIM v18 (18 Eyl 2026 · v17 + K4 nisinde AKTARMA GOZU: SOL robot toppingli tepsiyi birakir, SAG robot firinlar) · onceki: v17 (19 Eyl 2026) — Kemal: "derinlikleri dusun, her seye erisilsin, kurallari bozma". 3B tarama (omuz x ray derinligi x D kolonu): FR5 omuz 970 · ray ekseni hat yuzunden 360 · D alt kotu 285 -> sprey + kesim + 3 firin gozu + pres + topping + nis + kutu + QR 6 satir + tum cekmeceler erisilir (sim3d v7: aksam 14.076 adim temassiz). Istasyonlar ayri kaldi, 830 derinlik ayni. — v16: Kemal: D komple asagi (bos bolme kullanildi, 200 indi: sprey tepsi kotu 400 = FR5 alt siniri); firin panosu kaldirildi (yoktu); PRES AGZI ASAGI (plaka 1150), motor + govde USTTE. — v15: Kemal: robot kutusu yukarida olmaz (kablo). Robot kontrol kutusu D ALTINA, rayin hemen yanina (kablo ~3 m, zincire yerden girer); ana pano + UPS C ust bandinda kalir. — v14: Kemal: ana pano + robot kontrol kutusu + UPS, topping (C) ust bandinin SAGDAKI bos kismina (x 1100-1765, 700 bos genislik); makinede ekran yok (tablet); D alti bosaldi; D kotlari v12 ile ayni (v13 taslagi iptal: sprey cok alcaga iniyordu). — v12: Kemal: "firin altindaki ana pano/surucu neyin?" -> etiket duzeltmesi: ana panoda SURUCU YOK (eski surumden kalma yazi); cekmece suruculeri B'de, dozaj suruculeri C'de, E karti E'de. Ana pano = hattin beyni (PLC + HMI + ana salter). — v11: Kemal: icecek + tatli cekmecesi SILINMEYECEKTI: K3 ustune geri geldi (v7 yeri, 2 katli); kasar + sucuk deposu topping genisleyince acilan K4 kolonuna (400 x 830 x 300, kapakli); K4: sogutma grubu alt + depo orta + 6 tepsi ust; B karti + suruculer K1 ustundeki 187 bosluga (kuru bolme). — v9: Kemal: depo 4 gunluk (hat 2 gun + depo 4 gun = 6 gunluk ziyaret) — Kemal: 6 gunluk kasar + sucuk icin B'de KAPAKLI soguk bolme (K3 ustu, 620 x 680 x 240, icecek cekmecesi yerine); icecek QR dolabinin altina (ayri pafta SERVIS_TESLIM_v1). — Kemal: cekmeceler contali (vakumlu) ve motorlu lineer 700 strok gosterilsin; cekmece motoru kucuk, topping teknik parcalari buyuk cizilmisti -> gercek olcu; K3 icecek cekmecesi ust PU'ya giriyordu (hata) -> B 1060, hat 2030; her istasyon icin yan kesit. — Kemal: her istasyon kendi urunu (sogutucu, motor, pano kendi icinde). Motor bandi kalkti: B'nin sogutma grubu K1 altindaki tabanda (0-260), C'nin sogutma grubu + pompalar C'nin ust bandinda (1630-1970), icecek B'de K3 (2 katli cekmece 180 kutu), E'de cekmece yok. — Kemal: 'eski yerlesim (v3) iyi, sadece dediklerimi yap': cekmece modulu B (2100 x 830 x 1000, 3 kolon) press + topping altinda; PZP (950) B ustunde 1000-1950; topping ustunde MOTOR BANDI 1000-1300 gercek parcalarla (2 sogutma grubu 400x300x280 + hazne evaporatoru + suruculer), Atosa dozaj 1300-1970; D altinda robot kutusu + ana pano. — v3 Kemal: harc 2 kasete (kasar kalibi 280), motor bandi buyuk -> ic parcalari kesik cizgiyle, PZP zemin makinesi (katalog 640x800x950, 170 kg) -> PRESS tam boy kolon, cekmeceler TOPPING altinda 2 kolon, icecek KUTU altinda, teknik FIRIN altinda; lego moduller. — Kemal eskizi 2: PRESS | ATOSA TOPPING (tabla yok) ustte; altinda DOLAP MOTOR bandi + cekmeceler; sagda FIRIN x3 / KESICI / YAG / ROBOT KUTUSU; en sagda KUTU KATLAYAN. QR dolabi yok.: ON + UST (PLAN KESITI) + 2 YAN KESIT. Olculer mm.
Kemal'in eskizi (17 Eyl): sol secenek = 2 sabit robot kol · Fersah pres · Atosa dozaj TABLASIZ (tabani robot tutar) ·
2 gunluk her sey · firin 1 pide + 2 lahmacun gozu (kapakli, bant yok) · urun pide / pizza / lahmacun.
v14'ten FARKI: ray yok; STORE ayri govde degil — cekmeceler istasyonlarin ALTINDA (M0 12 lahmacun + teknik, M1 8 pide + pres,
M4 3 icecek + kutulama, M5 1 tatli + QR gozleri); TOPPING 2 katli 8 dozaj yuvasi (kaset 140x400x360, kasar kabi 280x400x360, sucuk dilimleyici);
iki robotun erisimi ortada AKTARMA RAFI'nda kesisir (uclar birbirine deger). HAT 5715 -> 4460.
ROBOT: 2 x Fairino FR10 (1.400 mm erisim). FR5 (922) yetmiyor: R1 bolgesi 2.200 mm genis (12+8 cekmece + pres + 8 yuva).
Kural: paftada yalniz gorunus + olcu + parca adi; aciklama mesajda.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE\HAT_2KOL_v18_teknik.png".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX = 6600, 3400
S = 0.62
BG, INK, GRAY, LINE = (255, 255, 255), (26, 26, 28), (132, 132, 140), (72, 72, 78)
FILL, ACC, RED, SOFT = (244, 244, 246), (0, 86, 184), (198, 42, 32), (228, 228, 234)
BUZ, DOLAP, BOSL, PUC, EVC = (28, 86, 166), (14, 120, 90), (190, 190, 196), (255, 240, 200), (220, 235, 255)
AGZ, SICAK = (253, 244, 243), (255, 226, 214)


def F(sz, b=False):
    for n in (("arialbd.ttf", "segoeuib.ttf") if b else ("arial.ttf", "segoeui.ttf")):
        try:
            return ImageFont.truetype(n, sz)
        except Exception:
            pass
    return ImageFont.load_default()


f7, f8, f9, f11, f13, f16, f38 = F(14), F(16), F(18), F(21), F(24), F(28, True), F(54, True)
im = Image.new("RGB", (W_PX, H_PX), BG)
d = ImageDraw.Draw(im)


def txt(x, y, s, f=f11, c=INK, a="la"):
    d.text((x, y), s, font=f, fill=c, anchor=a)


def satirlar(x, y, s, f, c, adim=20):
    ls = s.split("|")
    y0 = y - adim * (len(ls) - 1) / 2.0
    for i, l in enumerate(ls):
        txt(x, y0 + i * adim, l, f if i == 0 else f7, c if i == 0 else GRAY, "mm")


def sayi(v):
    return ("%g" % v).replace(".", ",")


def etiket(x, y, s, f=f8, c=INK, cer=GRAY):
    tw = d.textlength(s, font=f)
    d.rectangle([x - tw / 2 - 6, y - 11, x + tw / 2 + 6, y + 11], fill=BG, outline=cer, width=1)
    txt(x, y, s, f, c, "mm")


def olcu_h(x0, x1, y, s, f=f11, c=INK):
    d.line([(x0, y), (x1, y)], fill=c, width=2)
    for xx in (x0, x1):
        d.line([(xx, y - 8), (xx, y + 8)], fill=c, width=2)
    tw = d.textlength(s, font=f)
    d.rectangle([(x0 + x1) / 2 - tw / 2 - 6, y - 13, (x0 + x1) / 2 + tw / 2 + 6, y + 13], fill=BG)
    txt((x0 + x1) / 2, y, s, f, c, "mm")


def olcu_v(x, y0, y1, s, f=f11, c=INK, yon="r"):
    d.line([(x, y0), (x, y1)], fill=c, width=2)
    for yy in (y0, y1):
        d.line([(x - 8, yy), (x + 8, yy)], fill=c, width=2)
    txt(x + (12 if yon == "r" else -12), (y0 + y1) / 2, s, f, c, "lm" if yon == "r" else "rm")


def tarali(x0, y0, x1, y1, c=(222, 222, 228), adim=12):
    w, h = x1 - x0, y1 - y0
    for k in range(0, int(w + h), adim):
        ax, ay, bx, by = x0 + k, y1, x0 + k - h, y0
        if ax > x1:
            ay, ax = y1 - (ax - x1), x1
        if bx < x0:
            by, bx = y1 - k, x0
        if ay >= y0:
            d.line([(ax, ay), (bx, by)], fill=c, width=1)


def dline(p0, p1, c, w=1, dash=7, gap=4):
    (ax, ay), (bx, by) = p0, p1
    L = math.hypot(bx - ax, by - ay)
    if L < 1:
        return
    for i in range(int(L // (dash + gap)) + 1):
        t0 = min(1.0, i * (dash + gap) / L)
        t1 = min(1.0, (i * (dash + gap) + dash) / L)
        d.line([(ax + (bx - ax) * t0, ay + (by - ay) * t0), (ax + (bx - ax) * t1, ay + (by - ay) * t1)], fill=c, width=w)


def drect(x0, y0, x1, y1, c, w=1):
    dline((x0, y0), (x1, y0), c, w); dline((x1, y0), (x1, y1), c, w)
    dline((x1, y1), (x0, y1), c, w); dline((x0, y1), (x0, y0), c, w)


def darc(cx, cy, r, a0, a1, c, w=2, adim=4.0):
    """kesik yay: a0..a1 derece (PIL: saat yonu, 0 = sag)"""
    a = a0
    while a < a1:
        b = min(a1, a + adim)
        d.arc([cx - r, cy - r, cx + r, cy + r], a, b, fill=c, width=w)
        a = b + adim




# ======================= VERI =======================
DZ = 830.0
WO, BIND, FUGA, BOLME, XI = 620.0, 15.0, 3.0, 35.0, 62.5
CELL0 = 182.5
YUZ0 = CELL0 - BIND
HH = {"hamur": 75.0, "lahm": 60.0, "icecek": 241.0}
AD = {"hamur": "TAZE PİDE", "lahm": "LAHMACUN", "icecek": "İÇECEK + TATLI · 2 katlı çekmece"}
CAP = {"hamur": (20, "top"), "lahm": (35, "top"), "icecek": (0, "180 kutu 330 ml + 14 tatlı · 2,6 gün")}
# MODULLER (lego): A PRESS kolonu · B CEKMECE modulu (TOPPING altinda) · C TOPPING modulu (B ustunde) · D FIRIN kolonu · E KUTU kolonu
W_A, W_BC, W_D, W_E = 700.0, 1800.0, 700.0, 700.0
X_A, X_BC, X_D, X_E = 0.0, 700.0, 2500.0, 3200.0
HAT = W_A + W_BC + W_D + W_E                                # 3500
KOLON = [[(6, "hamur")], [(2, "hamur"), (6, "lahm")], [(6, "lahm"), (1, "icecek")]]   # B: 8 pide + 12 lahm + kasar/sucuk deposu, 3 kolon
K1_TABAN = 120.0                                            # K1 altinda B sogutma grubu tabani (0-240, plint yerine)
KOL_Y0 = (K1_TABAN + 62.5 - BIND, YUZ0, YUZ0)               # kolon baslangic kotlari
KOLON_AD = ("K1", "K2", "K3")
W_B = W_A + W_BC                                            # 2100
H_B = 1060.0                                                # cekmece modulu yuksekligi (ust PU 1000-1060)
H_MAK = 2030.0                                              # hat yuksekligi (B 1060 + PZP 950 + pay 20)
BAND_UST = YUZ0 + 6 * 93.0 + 274.0 - FUGA                   # K3 ustu 996,5
assert BAND_UST <= H_B - 60.0 and KOL_Y0[0] + 6 * 108.0 - FUGA <= H_B - 60.0
assert BAND_UST < H_B - 60.0 + 50.0
# C · TOPPING (Atosa dozaj unitesi, tabla yok): agiz · basliklar · hazne sirasi · sogutma
T_AGZ, T_BAS, T_KAS, T_SOG = (1070.0, 1180.0), (1183.0, 1317.0), (1320.0, 1680.0), (1690.0, 2028.5)
YUVA = [("HARÇ", 280.0, 370.0), ("HARÇ", 280.0, 650.0), ("KIYMA", 140.0, 860.0), ("KUŞBAŞI", 140.0, 1000.0),
        ("KAŞAR KABI", 280.0, 1210.0), ("SUCUK|DİLİMLEYİCİ", 180.0, 1440.0)]
# A · PRESS kolonu (kotlar)
PZP = (1060.0, 2010.0)                                      # Fersah PZP-400 B modulunun ustunde: 640 x 800 x 950 · 170 kg
PLAKA = 1150.0                                              # alt plaka kotu = 1060 + 580 (VARSAYIM - katalogda yok)
# D · FIRIN kolonu
TEK = (123.0, 280.0)
YAG = (285.0, 530.0)
KES = (535.0, 800.0)
FIR = [(805.0, 1120.0, "FIRIN HAZNESİ 1|LAHMACUN · 120 s"), (1125.0, 1440.0, "FIRIN HAZNESİ 2|LAHMACUN · 120 s"),
       (1445.0, 1768.0, "FIRIN HAZNESİ 3|PİDE · PİZZA · 240 s · ayrı sıcaklık")]
# E · KUTU kolonu
E_MEK = (123.0, 420.0)
E_AGZ = (430.0, 680.0)
E_SAR = (690.0, 2028.5)
R1X, R2X, RZ = 1250.0, 3200.0, 380.0
KAIDE, OMUZ = 820.0, 1000.0
ERISIM, ERISIM_P = 1400.0, 1250.0
AKT = (2300.0, 2700.0, 900.0, 1300.0)
KOR = 800.0

# ======================= YERLESIM =======================
OX = 300.0
FY_TOP = 400.0
FY = FY_TOP + H_MAK * S
PY_TOP = FY + 330.0
SX1 = OX + HAT * S + 240.0
SX = SX1 + 700.0
SX2 = SX + (DZ + KOR + 160.0) * S + 180.0
SX4 = SX2 + 700.0


def fx(x):
    return OX + x * S


def fy(y):
    return FY - y * S


def py(z):
    return PY_TOP + (z + 790.0) * S


# ======================= BASLIK =======================
txt(OX, 70, "AUTOKITCH  ·  HAT 2 KOL  ·  TEKNİK RESİM  v18  ·  TEPSİ SOKETLİ (ÇATAL YOK)  ·  TOPPING 1800  ·  İÇECEK + TATLI K3 ÜSTÜNDE  ·  DEPO K4'TE  ·  AKTARMA GÖZÜ K4 NİŞİNDE  ·  HAT 3900 × 2030", f38, INK)
txt(OX, 138, "ön · üst · yan görünüş  ·  günde 80 pide + 200 lahmacun (+ pizza)  ·  2 gün stok  ·  her istasyon kapalı ürün  ·  20 contalı motorlu çekmece + kaşar/sucuk 4 günlük kapaklı bölme tek modülde (haznede 2 gün → 6 günlük ziyaret)  ·  QR dolabı + servis: SERVİS_TESLİM paftası  ·  hat 2030 (B 1060 + pres 950 + pay)  ·  harç 2 kaset (kaşar kalıbı 280)  ·  tek Fairino FR5 yer rayında · omuz 970 · ray ekseni hat yüzünden 360  ·  QR dolabı yok  ·  tüm modüller 830 derin  ·  ölçüler mm  ·  17 Eylül 2026", f13, GRAY)
d.line([(OX, 178), (W_PX - 170, 178)], fill=LINE, width=3)

# ======================= ON GORUNUS =======================
txt(OX, FY_TOP - 190, "ÖN GÖRÜNÜŞ", f16, ACC)
txt(OX, FY_TOP - 152, "kesik çizgi = kapak arkası parça · robotlar koridorda önde, konumları zeminde işaretli", f9, GRAY)


def kabin(x0mm, w, y0, y1, ad=""):
    x0, x1 = fx(x0mm), fx(x0mm + w)
    d.rectangle([x0, fy(y1), x1, fy(y0)], fill=FILL, outline=LINE, width=4)
    if y0 == 0.0:
        d.rectangle([x0, fy(120), x1, fy(0)], fill=SOFT, outline=LINE, width=2)
    if ad:
        txt((x0 + x1) / 2, fy(H_MAK) - 64, ad, f13, INK, "md")


def kapak(x0mm, a, b, y0, y1, et="", yl=None, fill=None):
    d.rectangle([fx(x0mm + a), fy(y1), fx(x0mm + b), fy(y0)], fill=(fill or BG), outline=LINE, width=2)
    if et:
        satirlar(fx(x0mm + (a + b) / 2), fy(yl if yl else (y0 + y1) / 2), et, f8, INK)


def agiz(x0mm, a, b, y0, y1, et):
    d.rectangle([fx(x0mm + a), fy(y1), fx(x0mm + b), fy(y0)], fill=AGZ, outline=RED, width=3)
    cy = (fy(y0) + fy(y1)) / 2
    txt(fx(x0mm + (a + b) / 2), cy - 10, et, f8, RED, "mm")
    txt(fx(x0mm + (a + b) / 2), cy + 12, "y %s – %s" % (sayi(y0), sayi(y1)), f7, RED, "mm")


def kesik(x0mm, a, b, y0, y1, et="", c=INK, alt=""):
    drect(fx(x0mm + a), fy(y1), fx(x0mm + b), fy(y0), c, 1)
    if et:
        txt(fx(x0mm + (a + b) / 2), fy((y0 + y1) / 2) - (8 if alt else 0), et, f7, c, "mm")
    if alt:
        txt(fx(x0mm + (a + b) / 2), fy((y0 + y1) / 2) + 10, alt, f7, GRAY, "mm")


def modul_etiketi(x0mm, w, y0, y1, ad, olcu):
    x0, x1 = fx(x0mm) + 6, fx(x0mm + w) - 6
    d.rectangle([x0, fy(0) + 126, x1, fy(0) + 172], fill=ACC)
    txt((x0 + x1) / 2, fy(0) + 140, ad, f8, BG, "mm")
    txt((x0 + x1) / 2, fy(0) + 160, olcu, f7, BG, "mm")


# --- A · PRESS modulu (B ustunde)
kabin(X_A, W_A, H_B, H_MAK, "A · PRESS")
kapak(X_A, 33.0, 667.0, PZP[0] + 3.0, PZP[1])
kesik(X_A, 40.0, 660.0, PZP[0] + 8.0, PLAKA - 12.0, "alt tabla 90", GRAY)
d.ellipse([fx(X_A + 180), fy(PLAKA) - 4, fx(X_A + 520), fy(PLAKA) + 4], outline=INK, width=2)
txt(fx(X_A + 350), fy(PLAKA) + 16, "alt plaka Ø340 ısıtmalı · kot %s" % sayi(PLAKA), f7, GRAY, "mm")
agiz(X_A, 53.0, 647.0, PLAKA, PLAKA + 220.0, "PRES AĞZI · AŞAĞIDA · robot eli girer")
kesik(X_A, 205.0, 495.0, PLAKA + 225.0, PLAKA + 275.0, "üst plaka Ø290", INK)
kesik(X_A, 40.0, 660.0, PLAKA + 280.0, PZP[1] - 5.0, "PRES GÖVDESİ · MOTOR ÜSTTE", INK, "motor + rezistans + 2 kolon · 3,5 kW · 640 × 800")
txt(fx(X_A + 350), fy(PZP[1]) - 12, "üst pay 20", f7, GRAY, "mm")
modul_etiketi(X_A, W_A, 0.0, H_MAK, "MODÜL A · PRESS", "700 × 830 × 970 · B üstünde")
olcu_h(fx(X_A), fx(X_A + W_A), fy(H_MAK) - 26, sayi(W_A), f11, INK)

# --- B · CEKMECE modulu (press + topping altinda, tek parca)
kabin(X_A, W_B, 0.0, H_B)
d.rectangle([fx(X_A + 30), fy(H_B - 60.0), fx(X_A + W_B - 30), fy(121.5)], fill=BG, outline=LINE, width=2)
d.rectangle([fx(X_A + 30), fy(H_B - 1.5), fx(X_A + W_B - 30), fy(H_B - 60.0)], fill=PUC, outline=GRAY, width=1)
txt(fx(X_A + W_B / 2), fy(H_B - 30.0), "tavan PU 60 · üstünde MODÜL A ve C oturur · 170 kg pres için profil takviye · çekmece önü 40 PU + conta · her çekmecede 24 V lineer motor 700 strok", f7, GRAY, "mm")
cx = X_A + XI
for ki, gruplar in enumerate(KOLON):
    if ki:
        d.rectangle([fx(cx - BOLME), fy(H_B - 60.0), fx(cx), fy(YUZ0)], fill=SOFT, outline=LINE, width=1)
    y = KOL_Y0[ki]
    for adet, tip in gruplar:
        h = HH[tip] + 2 * BIND
        ybas = y
        for _ in range(adet):
            d.rectangle([fx(cx + 8), fy(y + h), fx(cx + WO - 8), fy(y)], fill=BG, outline=DOLAP, width=(2 if tip == "icecek" else 1))
            if tip == "icecek":
                d.line([(fx(cx + 8), fy(y + h / 2)), (fx(cx + WO - 8), fy(y + h / 2))], fill=DOLAP, width=2)
                txt(fx(cx + WO - 70), fy(y + h * 0.75), "üst kat", f7, GRAY, "mm"); txt(fx(cx + WO - 70), fy(y + h * 0.25), "alt kat", f7, GRAY, "mm")
            y += h + FUGA
        cap, br = CAP[tip]
        ym = (fy(ybas) + fy(y - FUGA)) / 2
        etiket(fx(cx + WO / 2), ym - 13, ("%s × %d" % (AD[tip], adet)) if cap else AD[tip], f8, INK, DOLAP)
        etiket(fx(cx + WO / 2), ym + 13, ("%d %s · +3 °C" % (adet * cap, br)) if cap else (br + " · +3 °C"), f7, DOLAP, DOLAP)
    txt(fx(cx + WO / 2), fy(H_B - 60.0) + 14, KOLON_AD[ki], f7, GRAY, "mm")
    olcu_h(fx(cx), fx(cx + WO), fy(0) + 44, "620", f8, GRAY)
    cx += WO + BOLME
# --- K4 · TEKNIK KOLON + TEPSI NISI (B icinde, K3 sagi)
K4X, K4W = cx, 400.0
d.rectangle([fx(K4X - BOLME), fy(H_B - 60.0), fx(K4X), fy(YUZ0)], fill=SOFT, outline=LINE, width=1)
d.rectangle([fx(K4X), fy(H_B - 60.0), fx(K4X + K4W), fy(121.5)], fill=BG, outline=LINE, width=2)
kapak(X_A, K4X - X_A + 8.0, K4X - X_A + K4W - 8.0, 130.0, 368.0)
kesik(X_A, K4X - X_A + 20.0, K4X - X_A + K4W - 20.0, 140.0, 360.0, "SOĞUTMA GRUBU", INK, "400 × 300 × 220 · ⅓ HP · ön ızgara")
d.rectangle([fx(K4X + 8), fy(675.0), fx(K4X + K4W - 8), fy(375.0)], fill=BG, outline=DOLAP, width=3)
for hy in (415.0, 635.0):
    d.rectangle([fx(K4X + 10), fy(hy + 12.0), fx(K4X + 26), fy(hy - 12.0)], fill=DOLAP)
d.rectangle([fx(K4X + K4W - 60), fy(555.0), fx(K4X + K4W - 48), fy(495.0)], fill=INK)
satirlar(fx(K4X + K4W / 2 - 12), fy(525.0), "KAŞAR + SUCUK|DEPOSU · kapaklı · +3 °C|400 × 830 × 300 · iç 61 L|17,6 kg + 28 çubuk · 4 gün", f8, INK, 19)
agiz(X_A, K4X - X_A + 8.0, K4X - X_A + K4W - 8.0, 690.0, 995.0, "")
etiket(fx(K4X + K4W / 2), fy(1030.0), "TEPSİ NİŞİ · 6 boş tepsi · raf 36 · y 690–905", f7, RED, RED)
d.line([(fx(K4X + 30), fy(905.0)), (fx(K4X + K4W - 30), fy(905.0))], fill=RED, width=3)
d.rectangle([fx(K4X + K4W / 2 - 20), fy(927.0), fx(K4X + K4W / 2 + 20), fy(905.0)], fill=BG, outline=RED, width=2)
txt(fx(K4X + K4W / 2), fy(962.0), "AKTARMA GÖZÜ · y 905–995", f7, RED, "mm")
for i in range(6):
    yy = 692.0 + i * 36.0
    d.line([(fx(K4X + 40), fy(yy)), (fx(K4X + K4W - 40), fy(yy))], fill=INK, width=2)
    d.rectangle([fx(K4X + K4W / 2 - 20), fy(yy + 22.0), fx(K4X + K4W / 2 + 20), fy(yy)], fill=BG, outline=ACC, width=2)
# K1 ustu (812,5 – 1000): kuru teknik bolme — B karti + 20 motor surucusu
K1X = X_A + XI
d.rectangle([fx(K1X + 8), fy(995.0), fx(K1X + WO - 8), fy(815.5)], fill=BG, outline=LINE, width=2)
d.rectangle([fx(K1X + 8), fy(855.5), fx(K1X + WO - 8), fy(815.5)], fill=PUC, outline=GRAY, width=1)
txt(fx(K1X + WO / 2), fy(835.5), "PU 40 · üstü kuru teknik bölme", f7, GRAY, "mm")
kesik(X_A, K1X - X_A + 60.0, K1X - X_A + 260.0, 880.0, 965.0, "B KARTI", INK)
kesik(X_A, K1X - X_A + 300.0, K1X - X_A + 560.0, 880.0, 965.0, "20 MOTOR", INK, "SÜRÜCÜSÜ")
olcu_h(fx(K4X), fx(K4X + K4W), fy(0) + 44, "400", f8, GRAY)
d.line([(fx(X_A), fy(H_B)), (fx(X_A + W_B), fy(H_B))], fill=LINE, width=4)

# --- C · TOPPING modulu (B ustunde)
kabin(X_BC, W_BC, H_B, H_MAK, "C · ATOSA (YINDU) DOZAJ ÜNİTESİ · TABLA YOK")
agiz(X_BC, 30.0, 1770.0, T_AGZ[0], T_AGZ[1], "ROBOT AĞZI 1740 × 110 · tepsi nozul altında spiral (r 110) · dış nozullarda tepsi kenarı 40 pay")
kapak(X_BC, 33.0, 1767.0, T_BAS[0], T_BAS[1], "DOZAJ BAŞLIKLARI · harç: piston pompa · kıyma / kuşbaşı: vida · kaşar: karıştırıcı + vida · sucuk: şarjör + bıçak")
kapak(X_BC, 33.0, 1767.0, T_KAS[0], T_KAS[1])
for urun, gw, xc in YUVA:
    kesik(X_BC, xc - gw / 2 + 6, xc + gw / 2 - 6, T_KAS[0] + 8, T_KAS[1] - 8)
    satirlar(fx(X_BC + xc), fy(1510.0) - 4, urun, f7, INK, 16)
    txt(fx(X_BC + xc), fy(1510.0) + 22, ("%s × 400 × 360" % sayi(gw)) if "SUCUK" not in urun else "180 × 400 · 14 çubuk", f7, GRAY, "mm")
txt(fx(X_BC + W_BC / 2), fy(T_KAS[1]) - 14, "HAZNE SIRASI · +3 °C · önden kaset takılır · kaset tabanı kot 1320", f7, INK, "mm")
kapak(X_BC, 33.0, 1767.0, T_SOG[0], T_SOG[1])
kesik(X_BC, 60.0, 360.0, T_SOG[0] + 60.0, T_SOG[0] + 280.0, "SOĞUTMA GRUBU", INK, "300 × 250 × 220 · ⅕ HP · 0,19 m³ kabin")
kesik(X_BC, 380.0, 630.0, T_SOG[0] + 60.0, T_SOG[0] + 210.0, "EVAPORATÖR + FAN", INK, "250 × 150")
kesik(X_BC, 650.0, 900.0, T_SOG[0] + 60.0, T_SOG[0] + 210.0, "DOZAJ SÜRÜCÜLERİ", INK, "6 kart · 250 × 150")
kesik(X_BC, 920.0, 1070.0, T_SOG[0] + 60.0, T_SOG[0] + 210.0, "C KARTI", INK)
d.line([(fx(X_BC + 1085.0), fy(T_SOG[1] - 8)), (fx(X_BC + 1085.0), fy(T_SOG[0] + 8))], fill=LINE, width=2)
kesik(X_BC, 1100.0, 1500.0, T_SOG[0] + 40.0, T_SOG[0] + 290.0, "ANA PANO · PLC · ana şalter", INK, "400 × 350 × 250 · ekran yok → tablet")
kesik(X_BC, 1520.0, 1765.0, T_SOG[0] + 40.0, T_SOG[0] + 290.0, "UPS", GRAY, "500 VA")
txt(fx(X_BC + 1430.0), fy(T_SOG[1] - 18.0), "HAT PANOSU BÖLMESİ · kuru · önden kapak", f7, INK, "mm")
txt(fx(X_BC + W_BC / 2), fy(T_SOG[0]) + 14, "C TEKNİK BANDI · parçalar 220 yüksek, kalan 120 hava kanalı · üst ön ızgara · önden servis", f7, INK, "mm")
modul_etiketi(X_BC, W_BC, H_B, H_MAK, "MODÜL C · TOPPING (kendi soğutucusu üstte)", "1800 × 830 × 970 · B üstünde")
olcu_h(fx(X_BC), fx(X_BC + W_BC), fy(H_MAK) - 26, sayi(W_BC), f11, INK)

# --- D · FIRIN kolonu
kabin(X_D, W_D, 0.0, H_MAK, "D · FIRIN · KESİCİ · YAĞ · ROBOT KUTUSU")
kapak(X_D, 33.0, 667.0, TEK[0], TEK[1])
kesik(X_D, 60.0, 640.0, 135.0, 270.0, "ROBOT KONTROL KUTUSU · ray yanında", INK, "245 × 180 × 45 · kablo → zemin → ray zinciri → robot (~3 m)")
kapak(X_D, 33.0, 667.0, 1773.0, 2028.0, "BOŞ|634 × 770 × 255")
kapak(X_D, 33.0, 667.0, YAG[0], YAG[1])
agiz(X_D, 53.0, 420.0, YAG[0] + 35.0, YAG[1] - 35.0, "SPREY AĞZI · tepsi")
kesik(X_D, 440.0, 640.0, YAG[0] + 20.0, YAG[1] - 20.0, "YAĞ KARTUŞU 4 L × 2", INK, "160 × 160 × 180 · ısıtma")
kapak(X_D, 33.0, 667.0, KES[0], KES[1])
agiz(X_D, 53.0, 647.0, KES[0] + 5.0, KES[0] + 140.0, "KESİM AĞZI · tepsi yuvaya oturur")
kesik(X_D, 160.0, 540.0, KES[0] + 145.0, KES[0] + 245.0, "YILDIZ BIÇAK Ø300 · 6 dilim · piston 100 strok", INK)
for y0f, y1f, et in FIR:
    kapak(X_D, 33.0, 667.0, y0f, y1f, "", None, SICAK)
    kesik(X_D, 60.0, 640.0, y0f + 60.0, y1f - 60.0, "", INK)
    satirlar(fx(X_D + 350), fy((y0f + y1f) / 2), et, f8, INK)
    txt(fx(X_D + 350), fy(y0f + 30.0), "iç 400 × 400 × 100 · taş taban · motorlu kapak", f7, GRAY, "mm")
modul_etiketi(X_D, W_D, 0.0, H_MAK, "MODÜL D · FIRIN KOLONU", "700 × 830 × 2030")
olcu_h(fx(X_D), fx(X_D + W_D), fy(H_MAK) - 26, sayi(W_D), f11, INK)

# --- E · KUTU kolonu
kabin(X_E, W_E, 0.0, H_MAK, "E · KUTU KATLAYAN")
kapak(X_E, 33.0, 667.0, E_MEK[0], E_MEK[1])
kesik(X_E, 60.0, 400.0, E_MEK[0] + 15.0, E_MEK[1] - 15.0, "KALIP + PLUNGER · vantuz", INK, "blankı alttan çeker · strok 250")
kesik(X_E, 420.0, 640.0, E_MEK[0] + 15.0, E_MEK[0] + 150.0, "VAKUM POMPASI", INK)
kesik(X_E, 420.0, 640.0, E_MEK[0] + 160.0, E_MEK[1] - 15.0, "E KONTROL KARTI", INK, "tahrik")
agiz(X_E, 30.0, 670.0, E_AGZ[0], E_AGZ[1], "KUTULAMA AĞZI · kutu 320 × 320 × 45")
kapak(X_E, 33.0, 667.0, E_SAR[0], E_SAR[1])
kesik(X_E, 150.0, 550.0, E_SAR[0] + 20.0, E_SAR[1] - 60.0, "", INK)
for i in range(16):
    yy = E_SAR[0] + 60.0 + i * 80.0
    d.line([(fx(X_E + 160), fy(yy)), (fx(X_E + 540), fy(yy))], fill=BOSL, width=1)
satirlar(fx(X_E + 350), fy(1360.0), "KUTU ŞARJÖRÜ|blank 400 × 760 yatay yığın · 1280 mm|= 710 (1,8 mm) – 850 (1,5 mm) kutu · 2 gün 560 · pay var", f8, INK)
modul_etiketi(X_E, W_E, 0.0, H_MAK, "MODÜL E · KUTU KOLONU", "700 × 830 × 2030")
olcu_h(fx(X_E), fx(X_E + W_E), fy(H_MAK) - 26, sayi(W_E), f11, INK)

olcu_h(fx(0), fx(HAT), fy(0) + 96, "HAT  %s" % sayi(HAT), f13, INK)
txt(fx(0) - 12, fy(0) + 149, "ÜST", f8, ACC, "rm")
txt(fx(0) - 12, fy(0) + 199, "ALT", f8, ACC, "rm")
d.rectangle([fx(X_A) + 6, fy(0) + 176, fx(X_A + W_B) - 6, fy(0) + 222], fill=DOLAP)
txt(fx(X_A + W_B / 2), fy(0) + 190, "MODÜL B · ÇEKMECE MODÜLÜ · 8 pide + 12 lahmacun + içecek/tatlı 2 katlı çekmece (K3 üstü) · K4: soğutma grubu + kaşar/sucuk deposu + 6 tepsi + aktarma gözü · K1 üstü: B kartı + sürücüler · A ve C üstüne oturur", f8, BG, "mm")
txt(fx(X_A + W_B / 2), fy(0) + 210, "2500 × 830 × 1060", f7, BG, "mm")
olcu_v(fx(0) - 44, fy(H_MAK), fy(0), sayi(H_MAK), f11, INK, "l")
for yy in (120.0, K1_TABAN, H_B, T_AGZ[1], T_KAS[0], PLAKA, T_KAS[1], PZP[1], H_MAK):
    d.line([(fx(0) - 24, fy(yy)), (fx(0) - 6, fy(yy))], fill=INK, width=2)
    txt(fx(0) - 52, fy(yy), sayi(yy), f7, INK, "rm")
# birlesim isaretleri
for xj, et, yb in ((X_BC, "A | C", H_B), (X_D, "B·C | D", 0.0), (X_E, "D | E", 0.0)):
    d.rectangle([fx(xj) - 5, fy(H_MAK) - 12, fx(xj) + 5, fy(yb) + 12], fill=BG, outline=None)
    dline((fx(xj), fy(H_MAK) - 12), (fx(xj), fy(yb) + 12), ACC, 3, 10, 6)
    txt(fx(xj), fy(H_MAK) - 120, "BİRLEŞİM", f7, ACC, "mm")
    txt(fx(xj), fy(H_MAK) - 104, et, f7, GRAY, "mm")
for rx, ad in ((R1X, "R1 · FR10"), (R2X, "R2 · FR10")):
    d.polygon([(fx(rx), fy(0) + 4), (fx(rx) - 14, fy(0) + 30), (fx(rx) + 14, fy(0) + 30)], fill=ACC)
    txt(fx(rx), fy(0) + 46, ad + " · koridorda, önde", f8, ACC, "mm")
    txt(fx(rx), fy(0) + 66, "x " + sayi(rx) + " · z +380", f7, GRAY, "mm")

# ======================= UST GORUNUS (PLAN KESITI) =======================
txt(OX, PY_TOP - 100, "ÜST GÖRÜNÜŞ  ·  PLAN KESİTİ  ·  robot erişimi", f16, ACC)
txt(fx(HAT / 2), py(-790) - 34, "ARKA", f9, GRAY, "mm")
zb = 40.0 - DZ
for x0m, w, ad in ((X_A, W_A, "A · PRESS (B üstünde)"), (X_BC, W_BC, "C · TOPPING (B üstünde)"), (X_D, W_D, "D · FIRIN"), (X_E, W_E, "E · KUTU")):
    d.rectangle([fx(x0m), py(zb), fx(x0m + w), py(40.0)], fill=FILL, outline=LINE, width=3)
    txt(fx(x0m + w / 2), py(40.0) + 30, "%s  ·  %s × %s" % (ad, sayi(w), sayi(DZ)), f9, INK, "mm")
# A plan
d.rectangle([fx(X_A + 29), py(-788.0), fx(X_A + 669), py(12.0)], fill=BG, outline=INK, width=2)
d.ellipse([fx(X_A + 180), py(-570.0), fx(X_A + 520), py(-230.0)], outline=GRAY, width=1)
txt(fx(X_A + 350), py(-400.0), "FERSAH PZP-400", f8, INK, "mm")
txt(fx(X_A + 350), py(-370.0), "640 × 800 · alt plaka Ø340", f7, GRAY, "mm")
txt(fx(X_A + 350), py(-660.0), "altta: K1 · TAZE PİDE × 6 + soğutma grubu (B)", f7, DOLAP, "mm")
# B/C plan
d.rectangle([fx(X_A + 1.5), py(zb + 1.5), fx(X_A + W_B - 1.5), py(zb + 61.5)], fill=PUC, outline=GRAY, width=1)
cx = X_A + XI
for ki in range(3):
    drect(fx(cx + 16), py(-680.0), fx(cx + WO - 16), py(0.0), DOLAP, 2)
    d.rectangle([fx(cx + 190), py(-725.0), fx(cx + 450), py(-680.0)], fill=EVC, outline=BUZ, width=1)
    d.rectangle([fx(cx + 18), py(-740.0), fx(cx + 58), py(0.0)], fill=(255, 230, 230), outline=RED, width=1)
    txt(fx(cx + 320), py(-702.5), "EVAPORATÖR", f7, BUZ, "mm")
    txt(fx(cx + WO / 2), py(-640.0), "K%d · 620 × 680 · altta (B)" % (ki + 1), f7, DOLAP, "mm")
    cx += WO + BOLME
for urun, gw, xc in YUVA:
    d.rectangle([fx(X_BC + xc - gw / 2 + 6), py(-470.0), fx(X_BC + xc + gw / 2 - 6), py(-70.0)], fill=BG, outline=INK, width=2)
    satirlar(fx(X_BC + xc), py(-300.0), urun, f7, INK, 16)
    txt(fx(X_BC + xc), py(-250.0), "%s × 400" % sayi(gw), f7, GRAY, "mm")
for xc in (YUVA[0][2], YUVA[-1][2]):
    cxp, cyp = fx(X_BC + xc), py(-310.0)
    darc(cxp, cyp, 280.0 * S, 0.0, 360.0, ACC, 2, 3.0)
    d.ellipse([cxp - 170 * S, cyp - 170 * S, cxp + 170 * S, cyp + 170 * S], outline=ACC, width=1)
txt(fx(X_BC + W_BC / 2), py(-620.0), "TEPSİ SÜPÜRME Ø560 (tepsi Ø340 + spiral r 110) · dış nozullarda yan duvara 40 pay → ağız 1740", f7, ACC, "mm")
d.rectangle([fx(X_BC + 30), py(-780.0), fx(X_BC + W_BC - 30), py(-740.0)], fill=EVC, outline=BUZ, width=1)
txt(fx(X_BC + W_BC / 2), py(-760.0), "EVAPORATÖR · hazne kabini (C) · soğutma grubu C üst bandında", f7, BUZ, "mm")
d.rectangle([fx(X_BC + 30), py(-60.0), fx(X_BC + W_BC - 30), py(0.0)], fill=AGZ, outline=RED, width=1)
txt(fx(X_BC + W_BC / 2), py(-30.0), "ROBOT AĞZI · kapaklı · 1740 × 110", f7, RED, "mm")
txt(fx(X_BC + W_BC / 2), py(-560.0), "C · ATOSA (YINDU) DOZAJ ÜNİTESİ · 6 hazne tek sıra · tabla yok · dozaj pompaları haznelerin arkasında (z −470…−740)", f7, INK, "mm")
# D plan
d.rectangle([fx(X_D + 30), py(-600.0), fx(X_D + 670), py(-20.0)], fill=SICAK, outline=INK, width=2)
drect(fx(X_D + 150), py(-500.0), fx(X_D + 550), py(-100.0), INK, 1)
txt(fx(X_D + 350), py(-325.0), "FIRIN · 3 HAZNE ÜST ÜSTE", f8, INK, "mm")
txt(fx(X_D + 350), py(-295.0), "dış 640 × 600 × 300 · iç 400 × 400 × 100", f7, GRAY, "mm")
d.rectangle([fx(X_D + 30), py(-780.0), fx(X_D + 670), py(-620.0)], fill=BG, outline=GRAY, width=1)
txt(fx(X_D + 350), py(-700.0), "EGZOZ KANALI · fan · karbon filtre · altta robot kontrol kutusu", f7, GRAY, "mm")
# E plan
drect(fx(X_E + 150), py(-785.5), fx(X_E + 550), py(-25.5), GRAY, 1)
txt(fx(X_E + 350), py(-640.0), "BLANK 400 × 760 · üstte", f7, GRAY, "mm")
d.rectangle([fx(X_E + 190), py(-410.0), fx(X_E + 510), py(-90.0)], fill=BG, outline=INK, width=2)
txt(fx(X_E + 350), py(-265.0), "KUTU", f8, INK, "mm")
txt(fx(X_E + 350), py(-235.0), "320 × 320 × 45", f7, GRAY, "mm")
txt(fx(X_E + 350), py(-560.0), "altta: katlama mekanizması + vakum", f7, GRAY, "mm")
olcu_h(fx(0), fx(HAT), py(40.0) + 96, "HAT  %s" % sayi(HAT), f13, INK)
olcu_v(fx(0) - 44, py(-790), py(40.0), sayi(DZ), f11, INK, "l")
d.line([(fx(-60), py(40.0 + KOR)), (fx(HAT + 60), py(40.0 + KOR))], fill=GRAY, width=1)
txt(fx(HAT / 2), py(40.0 + KOR) + 22, "ÖN  ·  robot koridoru %s" % sayi(KOR), f9, GRAY, "mm")
ax0, ax1, ay0, ay1 = AKT
for rx, ad in ((R1X, "R1 · FR10 · erişim 1400"), (R2X, "R2 · FR10 · erişim 1400")):
    cxp, cyp = fx(rx), py(RZ)
    d.rectangle([fx(rx - 200), py(RZ - 200), fx(rx + 200), py(RZ + 200)], fill=SOFT, outline=ACC, width=1)
    d.ellipse([cxp - 100 * S, cyp - 100 * S, cxp + 100 * S, cyp + 100 * S], fill=BG, outline=ACC, width=3)
    darc(cxp, cyp, ERISIM_P * S, 183.0, 357.0, ACC, 2, 3.0)
    darc(cxp, cyp, ERISIM * S, 190.0, 350.0, BOSL, 1, 2.5)
    txt(cxp, py(RZ + 200) + 22, ad, f9, ACC, "mm")
    txt(cxp, py(RZ + 200) + 46, "kaide 400 × 400 · eksen z +380 · pratik erişim 1250", f7, GRAY, "mm")
txt(fx(0) - 50, py(40.0) + 76, "yay: pratik 1250 (mavi) · nominal 1400 (gri)", f7, ACC, "la")
txt(fx(HAT / 2), py(RZ + 200) + 80, "R1: A + B + C (0–2500)  ·  R2: D + E (2500–3900)  ·  SOL → aktarma gözü (K4) → SAĞ fırınlar  ·  boş tepsiler K4 nişinde", f9, INK, "mm")


# ======================= YAN KESITLER · HER ISTASYON =======================
def govde(sx, h0, h1, plint=True, sogukzemin=False):
    def z(v):
        return sx + (v + 790.0) * S
    d.rectangle([z(-790), fy(h1), z(40), fy(h0)], fill=FILL, outline=LINE, width=4)
    if plint:
        d.rectangle([z(-790), fy(120), z(40), fy(0)], fill=SOFT, outline=LINE, width=2)
    d.rectangle([z(-788.5), fy(h1 - 1.5), z(-728.5), fy(h0 + 1.5)], fill=PUC, outline=GRAY, width=1)
    d.rectangle([z(-728.5), fy(h1 - 1.5), z(0.0), fy(h1 - 61.5)], fill=PUC, outline=GRAY, width=1)
    if sogukzemin:
        d.rectangle([z(-728.5), fy(h0 + 61.5), z(0.0), fy(h0 + 1.5)], fill=PUC, outline=GRAY, width=1)
    return z


def cekmeceler(z, gruplar, y0):
    for adet, tip in gruplar:
        h = HH[tip] + 2 * BIND
        for _ in range(adet):
            d.rectangle([z(-680.0), fy(y0 + h), z(0.0), fy(y0)], fill=BG, outline=DOLAP, width=1)
            d.rectangle([z(0.0), fy(y0 + h), z(40.0), fy(y0)], fill=BG, outline=DOLAP, width=1)          # on: 40 PU + conta
            d.line([(z(2.0), fy(y0 + 6.0)), (z(2.0), fy(y0 + h - 6.0))], fill=RED, width=2)                # conta
            d.rectangle([z(-760.0), fy(y0 + h / 2 + 10.0), z(-690.0), fy(y0 + h / 2 - 10.0)], fill=(255, 230, 230), outline=RED, width=1)   # lineer motor kafasi
            y0 += h + FUGA
    return y0


# --- KESIT 1 · A PRESS + B K1 (sogutma tabani)
z1 = govde(SX1, 0.0, H_B, plint=False, sogukzemin=False)
txt(SX1, FY_TOP - 190, "KESİT 1 · A + B", f16, ACC)
txt(SX1, FY_TOP - 152, "pres kolonu: K1 + PZP-400 · pres ağzı alt kenarı plaka kotunda", f9, GRAY)
d.rectangle([z1(-790), fy(K1_TABAN), z1(40), fy(0)], fill=SOFT, outline=LINE, width=2)
txt(z1(-375.0), fy(60.0), "plint 120 · soğutma grubu K4'te", f7, GRAY, "mm")
d.rectangle([z1(-728.5), fy(K1_TABAN + 61.5), z1(0.0), fy(K1_TABAN + 1.5)], fill=PUC, outline=GRAY, width=1)
ytop = cekmeceler(z1, KOLON[0], KOL_Y0[0])
d.rectangle([z1(-728.5), fy(H_B - 60.0), z1(-680.0), fy(K1_TABAN + 61.5)], fill=(250, 250, 251), outline=GRAY, width=1)
txt(z1(-340), fy(600.0) - 10, "K1 · TAZE PİDE × 6 · 680 derin", f8, DOLAP, "mm")
txt(z1(-340), fy(600.0) + 12, "önü 40 PU + conta · lineer motor arkada", f7, GRAY, "mm")
zA = govde(SX1, H_B, H_MAK, plint=False)
drect(z1(-770.0), fy(PZP[1] - 5), z1(30.0), fy(PZP[0] + 8), INK, 1)
drect(z1(-760.0), fy(PLAKA - 12.0), z1(20.0), fy(PZP[0] + 10.0), GRAY, 1)
txt(z1(-370.0), fy(PLAKA + 560.0), "motor + rezistans ÜSTTE · 800 derin", f7, INK, "mm")
d.line([(z1(-570.0), fy(PLAKA)), (z1(-230.0), fy(PLAKA))], fill=INK, width=3)
txt(z1(-400.0), fy(PLAKA) + 14, "alt plaka Ø340 · ~%s" % sayi(PLAKA), f7, GRAY, "mm")
d.rectangle([z1(-545.0), fy(PLAKA + 275.0), z1(-255.0), fy(PLAKA + 225.0)], fill=SOFT, outline=INK, width=1)
txt(z1(-400.0), fy(PLAKA + 250.0), "üst plaka", f7, INK, "mm")
d.rectangle([z1(-10.0), fy(PLAKA + 220.0), z1(40.0), fy(PLAKA)], fill=AGZ, outline=RED, width=2)
txt(z1(-100.0), fy(PLAKA + 115.0), "PRES AĞZI", f7, RED, "rm")
drect(z1(-760.0), fy(PZP[1] - 8), z1(20.0), fy(PLAKA + 280.0), GRAY, 1)
txt(z1(-370.0), fy(PLAKA + 400.0), "pres kafası · kolonlar", f7, GRAY, "mm")
olcu_h(z1(-790), z1(40), fy(0) + 44, "830", f11, INK)
for yy in (K1_TABAN, H_B, PLAKA, PZP[1], H_MAK):
    d.line([(z1(-790) - 24, fy(yy)), (z1(-790) - 6, fy(yy))], fill=INK, width=2)
    txt(z1(-790) - 30, fy(yy), sayi(yy), f7, INK, "rm")
d.line([(z1(40), fy(0)), (z1(140), fy(0))], fill=INK, width=3)


# --- KESIT 2 · C TOPPING + B K2 + robot koridoru
def sz(zv):
    return SX + (zv + 790.0) * S


txt(SX, FY_TOP - 190, "KESİT 2 · C + B", f16, ACC)
txt(SX, FY_TOP - 152, "K2 kolonu + Atosa dozaj (soğutucusu üstte) · robot koridorda", f9, GRAY)
govde(SX, 0.0, H_B, plint=True, sogukzemin=True)
cekmeceler(sz, KOLON[1], KOL_Y0[1])
d.rectangle([sz(-728.5), fy(H_B - 60.0), sz(-680.0), fy(CELL0)], fill=(250, 250, 251), outline=GRAY, width=1)
txt(sz(-340), fy(560.0) - 10, "ÇEKMECE 680 · K2: PİDE × 2 + LAHMACUN × 6", f8, DOLAP, "mm")
txt(sz(-340), fy(560.0) + 12, "önü 40 PU + conta · lineer motor arkada · evaporatör plenumu", f7, GRAY, "mm")
txt(sz(-340), fy(H_B - 30.0), "B | C BİRLEŞİMİ · PU 60", f7, ACC, "mm")
govde(SX, H_B, H_MAK, plint=False)
d.rectangle([sz(-728.5), fy(T_AGZ[1]), sz(-10.0), fy(T_AGZ[0])], fill=AGZ, outline=None)
d.rectangle([sz(-10.0), fy(T_AGZ[1]), sz(40.0), fy(T_AGZ[0])], fill=AGZ, outline=RED, width=2)
txt(sz(-660.0), fy((T_AGZ[0] + T_AGZ[1]) / 2), "AĞIZ", f7, RED, "mm")
d.rectangle([sz(-470.0), fy(T_KAS[1]), sz(-70.0), fy(T_KAS[0])], fill=BG, outline=INK, width=2)
txt(sz(-270.0), fy((T_KAS[0] + T_KAS[1]) / 2) - 10, "KASET 280 × 400 × 360 (harç)", f7, INK, "mm")
txt(sz(-270.0), fy((T_KAS[0] + T_KAS[1]) / 2) + 10, "hazne kabini +3 °C", f7, GRAY, "mm")
d.rectangle([sz(-360.0), fy(T_BAS[1]), sz(-180.0), fy(T_BAS[0])], fill=SOFT, outline=INK, width=1)
txt(sz(-270.0), fy((T_BAS[0] + T_BAS[1]) / 2), "NOZUL", f7, INK, "mm")
drect(sz(-740.0), fy(T_KAS[1]), sz(-480.0), fy(T_BAS[0]), GRAY, 1)
txt(sz(-610.0), fy(1500.0) - 8, "POMPA · MOTOR", f7, GRAY, "mm"); txt(sz(-610.0), fy(1500.0) + 8, "haznenin arkasında", f7, GRAY, "mm")
d.rectangle([sz(-420.0), fy(T_AGZ[0] + 66.0), sz(-120.0), fy(T_AGZ[0] + 54.0)], fill=ACC, outline=ACC)
d.rectangle([sz(-120.0), fy(T_AGZ[0] + 70.0), sz(30.0), fy(T_AGZ[0] + 50.0)], fill=BG, outline=ACC, width=2)
d.rectangle([sz(-10.0), fy(T_AGZ[0] + 66.0), sz(30.0), fy(T_AGZ[0] + 54.0)], fill=ACC, outline=ACC)
txt(sz(-270.0), fy(T_AGZ[0] + 35.0), "TABAN Ø300 · tepside · sap 150 ağızdan dışarı · dişi soket", f7, ACC, "mm")
d.rectangle([sz(-728.5), fy(H_MAK - 61.5), sz(0.0), fy(T_SOG[0])], fill=SOFT, outline=LINE, width=1)
drect(sz(-700.0), fy(T_SOG[0] + 280.0), sz(-450.0), fy(T_SOG[0] + 60.0), INK, 1)
txt(sz(-575.0), fy(T_SOG[0] + 170.0) - 8, "SOĞUTMA GRUBU", f7, INK, "mm"); txt(sz(-575.0), fy(T_SOG[0] + 170.0) + 8, "250 derin · 220", f7, GRAY, "mm")
d.rectangle([sz(-300.0), fy(T_SOG[0] + 210.0), sz(-60.0), fy(T_SOG[0] + 60.0)], fill=EVC, outline=BUZ, width=1)
txt(sz(-180.0), fy(T_SOG[0] + 135.0), "EVAP.", f7, BUZ, "mm")
olcu_h(sz(-790), sz(-728.5), fy(H_MAK) - 26, "62,5", f7, INK)
olcu_h(sz(-470), sz(-70), fy(H_MAK) - 60, "kaset 400", f8, INK)
olcu_h(sz(-790), sz(40), fy(0) + 44, "830", f11, INK)
d.line([(sz(40), fy(0)), (sz(40 + KOR + 160), fy(0))], fill=INK, width=3)
d.rectangle([sz(RZ - 200), fy(15.0), sz(RZ + 200), fy(0)], fill=SOFT, outline=ACC, width=2)
d.rectangle([sz(RZ - 100), fy(KAIDE), sz(RZ + 100), fy(15.0)], fill=BG, outline=ACC, width=3)
txt(sz(RZ), fy(KAIDE / 2), "KAİDE|Ø200 · 820", f7, ACC, "mm")
for w_, c_ in ((16, BG), (9, ACC)):
    d.line([(sz(RZ), fy(OMUZ)), (sz(RZ + 160), fy(1560.0)), (sz(-60.0), fy(T_AGZ[0] + 70.0))], fill=c_, width=w_, joint="curve")
d.ellipse([sz(RZ) - 18, fy(OMUZ) - 18, sz(RZ) + 18, fy(OMUZ) + 18], fill=ACC, outline=BG, width=2)
txt(sz(RZ + 180), fy(OMUZ), "OMUZ 1000", f8, ACC, "lm")
txt(sz(RZ + 180), fy(1640.0), "ROBOT · FR10 · 1400 mm · 10 kg", f8, ACC, "lm")
olcu_h(sz(40), sz(40 + KOR), fy(0) + 46, "KORİDOR 800", f8, INK)
olcu_v(sz(40 + KOR + 100), fy(KAIDE), fy(0), "820", f8, INK, "r")
for yy in (120.0, H_B, T_AGZ[1], T_KAS[0], T_KAS[1], T_SOG[0], H_MAK):
    d.line([(sz(-790) - 24, fy(yy)), (sz(-790) - 6, fy(yy))], fill=INK, width=2)
    txt(sz(-790) - 30, fy(yy), sayi(yy), f7, INK, "rm")


# --- KESIT 3 · D FIRIN
def sz2(zv):
    return SX2 + (zv + 790.0) * S


txt(SX2, FY_TOP - 190, "KESİT 3 · D", f16, ACC)
txt(SX2, FY_TOP - 152, "robot kutusu + pano · yağ · kesici · 3 kapaklı hazne", f9, GRAY)
govde(SX2, 0.0, H_MAK, plint=True)
d.rectangle([sz2(-728.5), fy(TEK[1]), sz2(0.0), fy(TEK[0])], fill=SOFT, outline=LINE, width=1)
drect(sz2(-700.0), fy(270.0), sz2(-450.0), fy(135.0), INK, 1)
txt(sz2(-575.0), fy(205.0), "ROBOT KUTUSU", f7, INK, "mm")
txt(sz2(-364.0), fy(1930.0), "boş", f7, GRAY, "mm")

d.rectangle([sz2(-728.5), fy(YAG[1]), sz2(-400.0), fy(YAG[0])], fill=BG, outline=LINE, width=1)
txt(sz2(-564.0), fy(407.0) - 8, "YAĞ KARTUŞU × 2", f7, INK, "mm"); txt(sz2(-564.0), fy(407.0) + 8, "160 × 160 × 180 · 45 °C", f7, GRAY, "mm")
d.rectangle([sz2(-400.0), fy(YAG[1] - 35), sz2(40.0), fy(YAG[0] + 35)], fill=AGZ, outline=RED, width=2)
txt(sz2(-180.0), fy(407.0), "SPREY AĞZI", f7, RED, "mm")
d.rectangle([sz2(-728.5), fy(KES[1]), sz2(0.0), fy(KES[0])], fill=BG, outline=LINE, width=1)
d.rectangle([sz2(-500.0), fy(KES[0] + 140), sz2(40.0), fy(KES[0] + 5)], fill=AGZ, outline=RED, width=2)
txt(sz2(-230.0), fy(KES[0] + 72), "KESİM AĞZI · yuva", f7, RED, "mm")
drect(sz2(-460.0), fy(KES[1] - 20), sz2(-100.0), fy(KES[0] + 145), INK, 1)
txt(sz2(-280.0), fy(KES[1] - 70), "BIÇAK + PİSTON", f7, INK, "mm")
for y0f, y1f, adf in FIR:
    d.rectangle([sz2(-620.0), fy(y1f), sz2(-20.0), fy(y0f)], fill=SICAK, outline=INK, width=2)
    d.rectangle([sz2(-520.0), fy(y1f - 100), sz2(-120.0), fy(y0f + 100)], fill=BG, outline=INK, width=1)
    d.rectangle([sz2(-20.0), fy(y1f - 40), sz2(40.0), fy(y0f + 40)], fill=AGZ, outline=RED, width=2)
    txt(sz2(-320.0), fy((y0f + y1f) / 2), "iç 400 × 100 · taş", f7, INK, "mm")
    txt(sz2(-320.0), fy(y1f - 45), adf.split("|")[0], f7, GRAY, "mm")
    d.rectangle([sz2(-780.0), fy(y1f - 40), sz2(-630.0), fy(y0f + 40)], fill=BG, outline=GRAY, width=1)
txt(sz2(-705.0), fy(1280.0), "EGZOZ", f7, GRAY, "mm")
txt(sz2(40) + 14, fy(1280.0), "MOTORLU KAPAK", f8, RED, "lm")
olcu_h(sz2(-620), sz2(-20), fy(H_MAK) - 60, "hazne 600", f8, INK)
olcu_h(sz2(-790), sz2(40), fy(0) + 44, "830", f11, INK)
for yy in (120.0, TEK[1], YAG[1], KES[1], FIR[0][1], FIR[1][1], H_MAK):
    d.line([(sz2(40) + 6, fy(yy)), (sz2(40) + 24, fy(yy))], fill=INK, width=2)
    txt(sz2(40) + 30, fy(yy), sayi(yy), f8, INK, "lm")
d.line([(sz2(40), fy(0)), (sz2(40 + 200), fy(0))], fill=INK, width=3)


# --- KESIT 4 · E KUTU
def sz4(zv):
    return SX4 + (zv + 790.0) * S


txt(SX4, FY_TOP - 190, "KESİT 4 · E", f16, ACC)
txt(SX4, FY_TOP - 152, "kutu katlayan: vakum · kalıp · plunger · şarjör", f9, GRAY)
govde(SX4, 0.0, H_MAK, plint=True)
d.rectangle([sz4(-728.5), fy(E_MEK[1]), sz4(0.0), fy(E_MEK[0])], fill=SOFT, outline=LINE, width=1)
drect(sz4(-500.0), fy(E_MEK[1] - 15), sz4(-200.0), fy(E_MEK[0] + 15), INK, 1)
txt(sz4(-350.0), fy(270.0) - 8, "KALIP + PLUNGER", f7, INK, "mm"); txt(sz4(-350.0), fy(270.0) + 8, "strok 250 · vantuz", f7, GRAY, "mm")
drect(sz4(-740.0), fy(300.0), sz4(-540.0), fy(140.0), INK, 1)
txt(sz4(-640.0), fy(220.0) - 8, "VAKUM", f7, INK, "mm"); txt(sz4(-640.0), fy(220.0) + 8, "POMPASI", f7, GRAY, "mm")
d.rectangle([sz4(-10.0), fy(E_AGZ[1]), sz4(40.0), fy(E_AGZ[0])], fill=AGZ, outline=RED, width=2)
d.rectangle([sz4(-728.5), fy(E_AGZ[1]), sz4(-10.0), fy(E_AGZ[0])], fill=AGZ, outline=None)
d.rectangle([sz4(-510.0), fy(E_AGZ[0] + 75.0), sz4(-190.0), fy(E_AGZ[0] + 30.0)], fill=BG, outline=INK, width=2)
txt(sz4(-350.0), fy(E_AGZ[0] + 52.0), "KUTU 320 × 45 plakada", f7, INK, "mm")
txt(sz4(-350.0), fy(E_AGZ[1] - 40.0), "flap parmakları + U kol kapağı kapatır", f7, GRAY, "mm")
txt(sz4(-660.0), fy((E_AGZ[0] + E_AGZ[1]) / 2), "AĞIZ", f7, RED, "mm")
d.rectangle([sz4(-728.5), fy(E_SAR[1]), sz4(0.0), fy(E_SAR[0])], fill=BG, outline=LINE, width=1)
drect(sz4(-765.0), fy(E_SAR[1] - 60), sz4(-5.0), fy(E_SAR[0] + 20), INK, 1)
for i in range(16):
    yy = E_SAR[0] + 60.0 + i * 80.0
    d.line([(sz4(-755.0), fy(yy)), (sz4(-15.0), fy(yy))], fill=BOSL, width=1)
txt(sz4(-385.0), fy(1400.0) - 10, "BLANK YIĞINI 760 derin", f8, INK, "mm")
txt(sz4(-385.0), fy(1400.0) + 12, "alttan çekilir · en alt blank kalıba iner", f7, GRAY, "mm")
olcu_h(sz4(-765), sz4(-5), fy(H_MAK) - 60, "blank 760", f8, INK)
olcu_h(sz4(-790), sz4(40), fy(0) + 44, "830", f11, INK)
for yy in (120.0, E_MEK[1], E_AGZ[1], E_SAR[0], H_MAK):
    d.line([(sz4(40) + 6, fy(yy)), (sz4(40) + 24, fy(yy))], fill=INK, width=2)
    txt(sz4(40) + 30, fy(yy), sayi(yy), f8, INK, "lm")
d.line([(sz4(40), fy(0)), (sz4(40 + 200), fy(0))], fill=INK, width=3)

# ======================= MODUL + PARCA LISTESI =======================
TX, TY = SX1, PY_TOP - 100
txt(TX, TY - 60, "MODÜLLER (lego · cıvatalı flanşla birleşir)  ·  PARÇA LİSTESİ", f16, ACC)
PARCA = [
    ("MODÜL B", "ÇEKMECE modülü · 20 hamur çekmecesi + 2 katlı içecek/tatlı çekmecesi + K4 depo/tepsi kolonu", "1", "2500 × 830 × 1060 · K1 6 pide + kart bölmesi · K2 2 pide + 6 lahm · K3 6 lahm + içecek/tatlı · K4 soğutma + depo + 6 tepsi"),
    ("MODÜL A", "PRESS · Fersah PZP-400 tam makine, B üstünde", "1", "700 × 830 × 970 · 170 kg → B tavanı takviyeli"),
    ("MODÜL C", "TOPPING · Atosa dozaj · tabla yok · ağız 1740 (tepsi süpürme Ø560)", "1", "1800 × 830 × 970 · B üstünde"),
    ("MODÜL D", "FIRIN kolonu · teknik + yağ + kesici + 3 hazne", "1", "700 × 830 × 2030"),
    ("MODÜL E", "KUTU kolonu · katlayıcı + vakum + şarjör", "1", "700 × 830 × 2030"),
    ("ROBOT", "Fairino FR10 · 1400 mm · 10 kg · ±0,05", "2", "kaide Ø200 × 820 · koridorda x 1250 / 3200"),
    ("ROBOT UCU", "erkek pim + kilit · tepsi sapındaki dişi sokete takılır · top için vakum ped", "2", "çatal yok · tepsi = el"),
    ("AKTARMA GÖZÜ", "K4 nişinin en üst gözü · toppingli dolu tepsi · 1 tepsi", "1", "y 905–995 · SOL robot soldan bırakır · SAĞ robot sağdan alır, fırına koyar"),
    ("TEPSİ", "Ø340 · sap 150 · dişi soket · ayaklı", "6", "K4 nişi 690–905 · raf 36 · 6 dolaşımda · yedek 2 adet serviste"),
    ("ÇEKMECE", "contalı çekmece 620 × 680 · önü 40 PU · 24 V lineer motor 700 strok", "20", "8 pide · 12 lahm"),
    ("DEPO", "kapaklı soğuk bölme 400 × 830 × 300 · iç 61 L · elle açılır", "1", "kaşar 17,6 kg + sucuk 5,6 kg · 4 gün · K4 kolonu 375–675"),
    ("İÇECEK", "2 katlı contalı çekmece 620 × 680 · lineer motor · robota açılır", "1", "180 kutu 330 ml + 14 tatlı · 2,6 gün · K3 üstü 725–1000"),
    ("SOĞUTMA", "B: ⅓ HP 400 × 300 × 220 (1,0 m³) · C: ⅕ HP 300 × 250 × 220 (0,19 m³)", "2", "B: K4 kolonu alt · C üst bandı"),
    ("TOPPING", "harç kaseti 280 × 400 × 360 · 28 L (kaşar kalıbı)", "2", "21,6 kg harç + 3,5 kg kap = 25 kg — ağır!"),
    ("TOPPING", "standart kaset 140 × 400 × 360 · 14 L", "2", "kıyma 6,4 kg · kuşbaşı 5,8 kg"),
    ("TOPPING", "kaşar kabı 280 × 400 × 360 · karıştırıcılı", "1", "8,8 kg"),
    ("TOPPING", "sucuk dilimleyici · 14 çubuk Ø38", "1", "180 × 400"),
    ("FIRIN", "kapaklı hazne dış 640 × 600 × 300 · iç 400 × 400 × 100 · taş", "3", "ref. Omake FPZ01 çift katlı 64 × 60 × 56"),
    ("FIRIN", "yıldız kesici Ø300 + piston · yağ kartuşu 4 L × 2 + sprey", "1", "kesim 535–800 · yağ 285–530 · fırın 805–1768"),
    ("KUTU", "katlayıcı (kalıp + plunger + vakum) + şarjör 1280", "1", "blank 400 × 760 · 710–850 kutu"),
    ("KONTROL", "ana pano PLC · robot kontrol kutusu 245 × 180 × 45 · UPS · taşınır tablet (makinede ekran yok)", "1", "ana pano + UPS: C üst bandı sağ boşluk · robot kontrol kutusu: D altı, ray yanında (kablo ~3 m)"),
]
kol = (0, 130, 700, 800)
th = 30
d.rectangle([TX, TY, TX + 1320, TY + th * (len(PARCA) + 1)], fill=BG, outline=LINE, width=2)
d.rectangle([TX, TY, TX + 1320, TY + th], fill=SOFT, outline=LINE, width=1)
for cx_, h_ in zip(kol, ("İSTASYON", "PARÇA", "ADET", "NOT")):
    txt(TX + cx_ + 10, TY + th / 2, h_, f8, INK, "lm")
for i, (a_, b_, c_, e_) in enumerate(PARCA):
    yy = TY + th * (i + 1)
    d.line([(TX, yy), (TX + 1320, yy)], fill=SOFT, width=1)
    for cx_, s_ in zip(kol, (a_, b_, c_, e_)):
        txt(TX + cx_ + 10, yy + th / 2, s_, f8 if cx_ != 800 else f7, INK if cx_ != 800 else GRAY, "lm")

# ======================= LEJANT =======================
d.line([(OX, H_PX - 130), (W_PX - 170, H_PX - 130)], fill=LINE, width=2)
ly = H_PX - 78
LEJ = [(LINE, BG, "kapak / panel", False), (RED, AGZ, "açık ağız · kapak", False), (DOLAP, BG, "çekmece +3 °C", False), (RED, (255, 230, 230), "çekmece lineer motoru 24 V · 700 strok", False),
       (INK, SICAK, "fırın haznesi", False), (GRAY, PUC, "PU yalıtım", False), (INK, BG, "kapak arkası parça", True), (ACC, BG, "modül birleşimi · robot", True)]
xx = OX
for c, fl, a_, kes in LEJ:
    if kes:
        drect(xx, ly - 12, xx + 30, ly + 12, c, 2)
    else:
        d.rectangle([xx, ly - 12, xx + 30, ly + 12], fill=fl, outline=c, width=3)
    txt(xx + 42, ly, a_, f9, INK, "lm")
    xx += 42 + d.textlength(a_, font=f9) + 56
txt(W_PX - 170, ly, "HAT %s × 2030 × 830  ·  5 kapalı istasyon (B altta, A + C üstünde)  ·  2 gün  ·  20 çekmece (8 pide · 12 lahmacun) + kaşar/sucuk 4 gün kapaklı  ·  Atosa dozaj tablasız: 2 harç 280 + kıyma + kuşbaşı + kaşar 280 + sucuk dilimleyici  ·  FIRIN 3 göz  ·  2 × FR10  ·  QR dolabı yok" % sayi(HAT), f9, GRAY, "rm")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.save(OUT)
print("yazildi:", OUT, "· hat %s mm" % sayi(HAT))
