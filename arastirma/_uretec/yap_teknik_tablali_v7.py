# -*- coding: utf-8 -*-
"""teknik_hat_atosa_tablali_v5_hd -> v7 : TOPPING BOLUMU MODELE ESITLENDI

Kemal: "Bu teknik resim son hali degil ki, sen TOPPING'e modele basladin ya sitede,
ordaki son haliydi - hic oyle degil bu. Guncellesene o kisimlarini."

PAFTA v5 topping_cad_v21'i gosteriyordu. Model o gunden beri v22 / hat_montaj_v34 oldu:
X TAHRIK ZINCIRI bastan yazildi (v21'de ray -500'e uzamisti ama kayis x=52'de basliyordu;
PARKTA ARABA KAYISA BAGLI DEGILDI). Paftadaki ray/araba/damlama bandi hala eskiydi.

MODELDEN OKUNAN GERCEK SAYILAR  [topping_hesap_v6 + topping_cad_v22]
  park (acici alti)   C-yerel  -350  ->  hat  350
  aktarma (firin)     C-yerel  1637  ->  hat 2337      strok 1987 mm
  HGR15 ray           C-yerel  -500..1785 -> hat  200..2485   boy 2285
  GT3 kasnak merkezi  C-yerel  -535 / 1835 -> hat 165 / 2535
  kayis GT3-15 kapali cevrim 4800 mm - iki kosu AYNI XY duzleminde
  tekne (ray kirisleri buna kaynakli + damlama) hat 145..2585  boy 2440
  X motoru NEMA23, teknenin ARKASINDA, sag uctaki kasnakta
  22,52 kg x 1,333 m/s2 + 10 N surtunme = 40,0 N -> 0,382 N.m ; motor 1,2 -> 3,14 kat pay

PAFTAYA GIREN UYARI
  Tekne modul C'nin sag kenarini 85 mm, sag kasnak 35 mm asiyor; sol ucu modul A'nin
  icinde (hat 145). "Istasyon = kapali urun" kuralina aykiri. Cozum Kemal'in karari:
  ya C 1900'e uzar, ya kasnak ice alinip strok kisalir. Pafta bunu KIRMIZI yaziyor.

v6 KULLANILMADI: o numara yaziyi buyuten (Kemal'in reddettigi) denemeye verilmis ve
silinmisti; ayni numara ikinci kez kullanilmasin diye v7'ye gecildi.
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "teknik_hat_atosa_tablali_v5_hd.py"), encoding="utf-8").read()
D = []

# ------------------------------------------------------------------ 1) baslik
D.append((
    "ATOSA TABLALI HAT  ·  TEKNİK RESİM  v5 · HD  ·  TOPPING = topping_cad_v21",
    "ATOSA TABLALI HAT  ·  TEKNİK RESİM  v7 · HD  ·  TOPPING = topping_cad_v22 · MONTAJ = hat_montaj_v34 · STROK 1987"))

# ------------------------------------------------------------------ 2) ray bandi: gercek boy, gercek kayis, gercek etiket
D.append((
    '''    d.rectangle([fx(X_A + 33), fy(RAY_T[1]), fx(X_C + W_C - 33), fy(RAY_T[0] + 3.0)], fill=BG, outline=LINE, width=2)
    d.rectangle([fx(X_A + 90), fy(RAY_T[0] + 60.0), fx(X_C + W_C - 40), fy(RAY_T[0] + 25.0)], fill=ACC, outline=ACC)
    txt(fx(X_C + 760), fy(RAY_T[0] + 105.0), "TABLA RAYI + ARABA 150 · x kızak · kaldırma · döndürme · pres altından fırın ağzına (x 90 – 2460)", f7, ACC, "mm")''',
    '''    # v7: ölçüler topping_cad_v22 / topping_hesap_v6'dan okunur. Modül C yereli + 700 = hat.
    RAY_L, RAY_R = 200.0, 2485.0                 # HGR15 gerçek ray boyu 2285
    KAS_L, KAS_R = 165.0, 2535.0                 # GT3 kasnak merkezleri
    TEK_L, TEK_R = 145.0, 2585.0                 # tekne: ray kirişleri buna kaynaklı
    PARK_X, AKT_X = 350.0, 2337.0                # strok 1987
    d.rectangle([fx(TEK_L), fy(RAY_T[1]), fx(TEK_R), fy(RAY_T[0] + 3.0)], fill=BG, outline=LINE, width=2)
    d.rectangle([fx(RAY_L), fy(RAY_T[0] + 78.0), fx(RAY_R), fy(RAY_T[0] + 60.0)], fill=SOFT, outline=INK, width=2)
    d.rectangle([fx(KAS_L), fy(RAY_T[0] + 46.0), fx(KAS_R), fy(RAY_T[0] + 34.0)], fill=ACC, outline=ACC)
    for _kx in (KAS_L, KAS_R):
        d.ellipse([fx(_kx) - 9.55 * S, fy(RAY_T[0] + 40.0) - 9.55 * S,
                   fx(_kx) + 9.55 * S, fy(RAY_T[0] + 40.0) + 9.55 * S], fill=BG, outline=ACC, width=2)
    d.rectangle([fx(KAS_R - 28.5), fy(RAY_T[0] + 96.0), fx(KAS_R + 28.5), fy(RAY_T[0] + 20.0)], fill=BG, outline=INK, width=2)
    txt(fx(KAS_R), fy(RAY_T[0] + 118.0), "X MOTORU", f7, INK, "mm")
    txt(fx(1150.0), fy(RAY_T[0] + 120.0), "TABLA ARABASI · AÇICI ALTINDAN FIRIN AĞZINA · strok 1987 (x 350 → 2337) · kaldırma YOK · ayrıntı aşağıda", f7, ACC, "mm")'''))

# ------------------------------------------------------------------ 3) damlama tavasi -> TEKNE (gercek boy)
D.append((
    '''    d.rectangle([fx(X_C + 33), fy(DAM[1]), fx(X_C + W_C - 33), fy(DAM[0])], fill=SOFT, outline=LINE, width=1)
    txt(fx(X_C + W_C / 2), fy((DAM[0] + DAM[1]) / 2), "DAMLAMA TAVASI 30 · çekmece, günlük yıkanır", f7, GRAY, "mm")''',
    '''    d.rectangle([fx(TEK_L), fy(DAM[1]), fx(TEK_R), fy(DAM[0])], fill=SOFT, outline=LINE, width=1)
    txt(fx(1250.0), fy((DAM[0] + DAM[1]) / 2), "TEKNE + DAMLAMA 30 · boy 2440 (x 145–2585) · iki ray kirişi 60 × 16 buna SÜREKLİ KAYNAK, sonra üç yüzey tek bağlamada frezelenir (0,1 mm/m)", f7, GRAY, "mm")'''))

# ------------------------------------------------------------------ 4) on gorunus: ucuncu tabla konumu = gercek aktarma
D.append((
    "    for xt, kes_ in ((X_A + 350.0, False), (X_C + YUVA[4][2], True), (X_C + W_C - 170.0, True)):",
    "    for xt, kes_ in ((PARK_X, False), (X_C + YUVA[4][2], True), (AKT_X, True)):"))

# ------------------------------------------------------------------ 5) plan: gercek strok
D.append((
    "    dline((fx(X_A + 90), py(-270.0)), (fx(X_C + W_C - 40), py(-270.0)), ACC, 3, 12, 6)",
    '''    dline((fx(350.0), py(-270.0)), (fx(2337.0), py(-270.0)), ACC, 3, 12, 6)'''))
D.append((
    '''    txt(fx(X_C + 760), py(-600.0), "TABLA HATTI z −270 = fırın bandı ekseni · ray tabanın altında (kesik) · hazne ağızları tabla hattının üstünde", f7, ACC, "mm")''',
    '''    txt(fx(1250.0), py(-600.0) + 34, "TABLA HATTI z −270 = fırın bandı ekseni · HGR15 ray x 200–2485 tabanın altında (kesik) · tabla merkezi x 350 (park) → 2337 (fırın ağzı) · hazne ağızları tabla hattının üstünde", f7, ACC, "mm")
    satirlar(fx(1250.0), py(-600.0) - 6,
             "X TAHRİK · HGR15 ray 2285 (x 200–2485, 2 sıra) · GT3-15 KAPALI ÇEVRİM kayış 4800, kasnak merkezleri x 165 / 2535 — iki koşu aynı düzlemde, araba bütün strokta kayışa bağlı|"
             "X motoru NEMA23 kapalı çevrim, TEKNENİN ARKASINDA (ürün düzleminin altında tahrik yok) · 22,52 kg × 1,333 m/s² + 10 N = 40,0 N → 0,382 N·m gerekir; motor 1,2 → 3,14 kat pay · dozajda 8,5 mm/s, geçişte 200 mm/s",
             f7, ACC, 18)
    txt(fx(1250.0), py(-600.0) - 37, "UYARI · tekne modül C'nin sağ kenarını 85 mm, sağ kasnak 35 mm aşıyor; sol ucu modül A'nın içinde (x 145) — İSTASYON = KAPALI ÜRÜN kuralına aykırı, KARAR BEKLİYOR", f7, RED, "mm")'''))
D.append((
    '''    txt(fx(X_A + 350), py(-270.0), "TABLA Ø340 · pres altında · z −270", f7, BUZ, "mm")''',
    '''    txt(fx(X_A + 350), py(-270.0), "TABLA Ø340 · AÇICI altında (park) · z −270", f7, BUZ, "mm")'''))

# ------------------------------------------------------------------ 6) parca listesi
D.append((
    '''        ("MODÜL C", "TOPPING · Atosa (Yindu) dozaj, 6 hazne tek sıra · altında tabla arabası (ray 150 + damlama 30 + bölme 250)", "1", "1800 × 830 × 970 · hazne sırası v19'a göre 290 yukarıda"),''',
    '''        ("MODÜL C", "TOPPING · Atosa (Yindu) dozaj, 6 hazne tek sıra · altında tabla arabası (ray bandı 150 + tekne/damlama 30 + tabla bölmesi 250)", "1", "1800 × 830 × 970 · hazne sırası v19'a göre 290 yukarıda · UYARI: tekne sağa 85, kasnak 35 mm taşıyor"),'''))
D.append((
    '''        ("BANDA AKTARMA",''',
    '''        ("X TAHRİK", "GT3-15 KAPALI ÇEVRİM kayış 4800 mm · 2 × 20 diş kasnak (çevre tam 60,00 mm/tur) x 165 ve 2535 · iki koşu AYNI XY düzleminde, araba bütün strokta kayışa bağlı · gergi sol kasnak plakasından", "1", "strok 1987 (x 350 → 2337) · HGR15 ray 2285 (x 200–2485), 2 sıra · tekne 2440, ray kirişleri kaynaklı + frezeli"),
        ("X MOTORU", "NEMA23 kapalı çevrim step, TEKNENİN ARKASINDA — ürün düzleminin altında tahrik elemanı yok · mili servis cebinden sağ kasnağa girer · 8 mm dik motor plakası, tekneye 4 × M8", "1", "1,2 N·m · gereken 0,382 (22,52 kg × 1,333 m/s² + 10 N sürtünme = 40,0 N) → 3,14 kat pay · 200 mm/s = 200 dev/dk · sürtünme 10 N VARSAYIM, prototipte ölçülecek"),
        ("BANDA AKTARMA",'''))

# ------------------------------------------------------------------ 7) cikti adi
D.append((r"\HAT_ATOSA_TABLALI_v5_HD.png", r"\HAT_ATOSA_TABLALI_v7_HD.png"))

for e, y in D:
    n = s.count(e)
    assert n == 1, "ESSIZ DEGIL (%d bulundu) -> %s" % (n, e[:90])
    s = s.replace(e, y, 1)

io.open(os.path.join(U, "teknik_hat_atosa_tablali_v7.py"), "w", encoding="utf-8").write(s)
print("teknik_hat_atosa_tablali_v7.py yazildi -", len(D), "donusum")
