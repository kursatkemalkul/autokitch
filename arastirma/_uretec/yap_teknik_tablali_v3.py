# -*- coding: utf-8 -*-
"""teknik_hat_bantli_v6_tablali_v2 -> teknik_hat_atosa_tablali_v3

Kemal: "son halinle bir teknik resim yapsana, su anki son halimizle; Atosa tablali
diye yaptigimiz secenegin son hali, bizimki ona adapte et."

TABLALI HAT v2'den v3'e DEGISENLER — hepsi topping_cad_v21'den geliyor:

1) MODUL A: PRES KAFASI -> KONILI DONER ACICI
   v2'de Fersah PZP-400 uyarlamasi vardi ve pres kuvvetini SABIT ORS tasiyordu.
   Duz pres Ø280'i tek seferde ezer: 3-12 kN. Tepsi kalktigi icin bu yuk dogrudan
   tablaya, doner yataga ve raya binerdi. Konili acici hamuru YUVARLAYARAK acar:
   40-160 N — 75 kat az. ORS GEREKMIYOR, kalkti.
   Koninin tepesi tabla ekseninde; koninin yaricapi boyla dogrusal arttigi icin
   donen tablanin her yaricaptaki hiziyla birebir eslesir, hicbir yerde kaymaz.

2) TABLA: uzerine ELLE CIKAN CALISMA DISKI kondu (mat gida UHMW Ø340 x 8->2).
   Tepsi yok; hamur bu diskin ustunde acilir, malzeme buna dokulur, aksam yikanir.
   v2'deki "dozajda +100 kalkar" kalkti: dozaj tabla sabit kotta donerken yapiliyor.

3) FIRIN AGZI: ITICI KALKTI. Yerine BICAK BURUNLU AKTARMA — bant Ø20 burun
   silindirine doluyor, ust yuzu diskin 2 mm alti; diskin kenari burna 8 mm kala
   duruyor, pide o bosluğu kendi govdesiyle kopruluyor. Ek motor yok.

4) Parca listesi ve kesit yazilari buna gore guncellendi.

NOT: icecek/kutu/UPS v2'de zaten vardi ve v3'te aynen duruyor —
   icecek + tatli 2 katli cekmece: 180 x 330 ml + 14 tatli = 2,6 GUN (4 gun degil)
   kutu sarjoru: 2 gun · 560 kutu
   ana pano + PLC + UPS 500 VA + robot kontrol kutusu: MODUL F tabaninda
   temizlik malzemesi HIC KONMAMIS — onun yerinde "YEDEK BOLME 385 x 305 · bos"
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "teknik_hat_bantli_v6_tablali_v2.py"), encoding="utf-8").read()
D = []

# ---------------------------------------------------------------- baslik
D.append((
    '''    baslik("AUTOKITCH  ·  ATOSA TABLALI HAT  ·  TEKNİK RESİM  v2  ·  B = HAT 2 KOL v19  ·  TABLA ARABASI PRES → DOZAJ → FIRIN  ·  HAT 5300 × 2030 × 830",
           "ön · üst · yan görünüş  ·  günde 80 pide + 200 lahmacun (+ pizza)  ·  2 gün stok  ·  her istasyon kapalı ürün  ·  ürün tepsisiz: tabla üstünde basılır, dozajlanır, itici fırın bandına iter → kesme plakası → kutu  ·  robot yalnız hamur + kutu + içecek taşır  ·  TEK Fairino FR5 yer rayında · omuz 970 · ray ekseni hat yüzünden 360  ·  tabla kotları VARSAYIM (Atosa cevabı yok)  ·  ölçüler mm  ·  18 Eylül 2026")''',
    '''    baslik("AUTOKITCH  ·  ATOSA TABLALI HAT  ·  TEKNİK RESİM  v3  ·  TOPPING = topping_cad_v21  ·  TABLA ARABASI AÇICI → DOZAJ → FIRIN  ·  HAT 5300 × 2030 × 830",
           "ön · üst · yan görünüş  ·  günde 80 pide + 200 lahmacun (+ pizza)  ·  2 gün stok  ·  her istasyon kapalı ürün  ·  ürün tepsisiz: hamur topu çalışma diskinde KONİLİ AÇICI ile açılır, dozajlanır, bıçak burunlu bant fırına çeker → kesme plakası → kutu  ·  robot yalnız hamur + kutu + içecek taşır  ·  TEK Fairino FR5 yer rayında · omuz 970 · ray ekseni hat yüzünden 360  ·  tabla kotları VARSAYIM (Atosa cevabı yok)  ·  ölçüler mm  ·  24 Eylül 2026")'''))

# ---------------------------------------------------------------- MODUL A: pres -> acici
D.append((
    '''    kabin(X_A, W_A, H_B, H_MAK, "A · PRES KAFASI · tabla üstüne basar")
    kapak(X_A, 33.0, 667.0, H_B + 3.0, 2010.0)
    kesik(X_A, 180.0, 520.0, RAY_T[1] + 10.0, P - 14.0, "SABİT ÖRS", INK, "pres kuvveti örste")
    agiz(X_A, 53.0, 647.0, P, P + 220.0, "HAMUR AĞZI · robot tablaya bırakır")
    kesik(X_A, 205.0, 495.0, P + 225.0, P + 275.0, "üst plaka Ø290", INK)
    kesik(X_A, 40.0, 660.0, P + 280.0, 2005.0, "PRES KAFASI · MOTOR ÜSTTE", INK, "Fersah PZP-400 uyarlaması · alt tabla yerine örs")
    modul_etiketi(X_A, W_A, "MODÜL A · PRES KAFASI", "700 × 830 × 970 · B üstünde")''',
    '''    kabin(X_A, W_A, H_B, H_MAK, "A · KONİLİ DÖNER AÇICI · tabla altında bekler")
    kapak(X_A, 33.0, 667.0, H_B + 3.0, 2010.0)
    agiz(X_A, 53.0, 647.0, P, P + 220.0, "HAMUR AĞZI · robot TOP halinde bırakır")
    # iki koni: uclari tabla ekseninde bulusur, alt cizgileri yatay (pide ust yuzu)
    _kx = X_A + 350.0
    for _y in (1.0, -1.0):
        d.polygon([(fx(_kx), fy(P + 8.0)), (fx(_kx + _y * 140.0), fy(P + 8.0)),
                   (fx(_kx + _y * 140.0), fy(P + 98.0))], outline=INK)
    txt(fx(_kx), fy(P + 130.0), "2 KONİ · boy 140 = pide yarıçapı · taban Ø90 · yarım açı 17,82°", f7, INK, "mm")
    txt(fx(_kx), fy(P + 152.0), "tepeler TABLA EKSENİNDE → koni kaymadan yuvarlanır · ters yönde dönerler", f7, GRAY, "mm")
    kesik(X_A, 205.0, 495.0, P + 175.0, P + 255.0, "KAFA PLAKASI 160 × 680 × 12", INK)
    kesik(X_A, 40.0, 660.0, P + 260.0, 2005.0, "AÇICI KOLONU · Z KIZAĞI strok 60 · Ø32 PNÖMATİK", INK,
          "2 × NEMA23 + planet redüktör · 40–160 N (düz pres 3–12 kN isterdi, örs gerekmiyor)")
    modul_etiketi(X_A, W_A, "MODÜL A · KONİLİ AÇICI", "700 × 830 × 970 · B üstünde")'''))

# ---------------------------------------------------------------- TABLA yazilari
D.append((
    '''    txt(fx(X_C + YUVA[4][2]), fy(P - 40.0), "TABLA Ø340 · seyir kotu %s · dozajda +100 kalkar, döner + kayar" % sayi(P), f7, BUZ, "mm")
    txt(fx(X_C + W_C - 210.0), fy(P + 40.0), "fırın ağzı · İTİCİ banda iter", f7, BUZ, "mm")''',
    '''    txt(fx(X_C + YUVA[4][2]), fy(P - 40.0), "TABLA Ø340 + ÇALIŞMA DİSKİ Ø340 × 8→2 (mat UHMW, elle çıkar) · seyir kotu %s · dozajda döner + kayar" % sayi(P), f7, BUZ, "mm")
    txt(fx(X_C + W_C - 210.0), fy(P + 40.0), "fırın ağzı · BIÇAK BURUNLU BANT · 8 mm boşluk · itici YOK", f7, BUZ, "mm")'''))

# ---------------------------------------------------------------- kesit yazilari
D.append((
    '''    txt(SX1, FY_TOP - 162, "Robot hamur topunu ağızdan tablanın ortasına bırakır · tabla örse iner, pres basar", f9, GRAY)''',
    '''    txt(SX1, FY_TOP - 162, "Robot hamur TOPUNU ağızdan çalışma diskinin ortasına bırakır · kafa iner, koniler döner, hamur Ø280'e açılır", f9, GRAY)'''))
D.append((
    '''    drect(z(-440.0), fy(P - 14.0), z(-100.0), fy(RAY_T[1] + 10.0), INK, 1)
    txt(z(-270.0), fy(RAY_T[1] + 55.0), "ÖRS", f7, INK, "mm")''',
    '''    txt(z(-270.0), fy(RAY_T[1] + 55.0), "örs YOK — koni yuvarlanıyor, ezmiyor", f7, GRAY, "mm")'''))
D.append((
    '''    txt(z(-270.0), fy(P) + 22, "tabla Ø340 · kot %s · z −270" % sayi(P), f7, BUZ, "mm")''',
    '''    txt(z(-270.0), fy(P) + 22, "tabla Ø340 + çalışma diski · kot %s · z −270" % sayi(P), f7, BUZ, "mm")'''))
D.append((
    '''    txt(z(-375.0), fy(P + 480.0), "pres kafası · motor + rezistans ÜSTTE", f7, INK, "mm")''',
    '''    txt(z(-375.0), fy(P + 480.0), "açıcı kafası · 2 koni + 2 motor ÜSTTE · Z kızağı strok 60", f7, INK, "mm")'''))

# ---------------------------------------------------------------- parca listesi
D.append((
    '''        ("MODÜL A", "PRES KAFASI · Fersah PZP-400 uyarlaması · alt tabla yerine sabit örs · pres tablanın üstüne basar", "1", "700 × 830 × 970 · kafa yüksekliği ≤ 385 (VARSAYIM · Fersah'a sorulacak)"),''',
    '''        ("MODÜL A", "KONİLİ DÖNER AÇICI · 2 koni (boy 140 · taban Ø90 · yarım açı 17,82°) · 2 × NEMA23 + planet · Z kızağı strok 60 · Ø32 pnömatik", "1", "700 × 830 × 970 · 40–160 N · örs YOK (düz pres 3–12 kN isterdi) · kafa ölçüleri VARSAYIM, tedarikçi cevabı bekleniyor"),'''))
D.append((
    '''        ("TABLA ARABASI", "Ø340 tabla · x kızak + kaldırma 100 + döndürme · pres altı → 6 hazne → fırın ağzı · itici ürünü banda iter", "1", "tur ≤ 60 sn (Atosa: bir pizza en fazla 1 dk) · kotlar VARSAYIM"),''',
    '''        ("TABLA ARABASI", "Ø340 tabla (304, göbeğe kaynaklı) + ÇALIŞMA DİSKİ Ø340 × 8→2 mat UHMW elle çıkar · HGR15 x kızağı · pancake dönüş motoru · açıcı altı → 6 hazne → fırın ağzı", "1", "kaldırma YOK · park yeri AÇICININ ALTI · kenar 15 mm'de 2 mm'ye iner (pide soyularak ayrılır)"),
        ("BANDA AKTARMA", "BIÇAK BURUNLU · bant Ø20 burun silindirine dolanır, üst yüzü diskin 2 mm altı · diskin kenarı burna 8 mm kala durur, pide boşluğu kendi gövdesiyle köprüler", "1", "itici ve köprü YOK · ek motor yok · Ø60 kauçuk tahrik silindiri + PTFE kaplı cam elyaf örgü bant 1,5"),'''))


# ---------------------------------------------------------------- plan gorunusu ve A yazilari
D.append((
    """    for x0m, w, ad in ((X_A, W_A, "A · PRESS (B üstünde)"), (X_C, W_C, "C · TOPPING (B üstünde)"), (X_F, W_F, "F · KONVEYÖR FIRIN"), (X_K, W_K, "K · KESME"), (X_E, W_E, "E · KUTU")):""",
    """    for x0m, w, ad in ((X_A, W_A, "A · AÇICI (B üstünde)"), (X_C, W_C, "C · TOPPING (B üstünde)"), (X_F, W_F, "F · KONVEYÖR FIRIN"), (X_K, W_K, "K · KESME"), (X_E, W_E, "E · KUTU")):"""))
D.append((
    """    txt(fx(X_A + 350), py(-745.0), "FERSAH PZP-400 · 640 × 800", f8, INK, "mm")""",
    """    txt(fx(X_A + 350), py(-745.0), "KONİLİ AÇICI KAFASI · 2 koni + 2 motor", f8, INK, "mm")"""))
# A modulunde ust uste binen iki yazi kalksin, bilgi kolonun altyazisina gecsin
D.append((
    """    txt(fx(_kx), fy(P + 130.0), "2 KONİ · boy 140 = pide yarıçapı · taban Ø90 · yarım açı 17,82°", f7, INK, "mm")
    txt(fx(_kx), fy(P + 152.0), "tepeler TABLA EKSENİNDE → koni kaymadan yuvarlanır · ters yönde dönerler", f7, GRAY, "mm")
    kesik(X_A, 205.0, 495.0, P + 175.0, P + 255.0, "KAFA PLAKASI 160 × 680 × 12", INK)
    kesik(X_A, 40.0, 660.0, P + 260.0, 2005.0, "AÇICI KOLONU · Z KIZAĞI strok 60 · Ø32 PNÖMATİK", INK,
          "2 × NEMA23 + planet redüktör · 40–160 N (düz pres 3–12 kN isterdi, örs gerekmiyor)")""",
    """    kesik(X_A, 205.0, 495.0, P + 175.0, P + 255.0, "KAFA PLAKASI 160 × 680 × 12", INK)
    kesik(X_A, 40.0, 660.0, P + 260.0, 2005.0, "AÇICI KOLONU · Z KIZAĞI strok 60 · Ø32 PNÖMATİK", INK,
          "2 KONİ · boy 140 · taban Ø90 · yarım açı 17,82°|tepeler TABLA EKSENİNDE — kaymadan yuvarlanır|"
          "2 × NEMA23 + planet · ters yönde döner|40–160 N · örs YOK")"""))

for e, y in D:
    assert e in s, "BULUNAMADI -> " + e[:70]
    s = s.replace(e, y, 1)

s = s.replace(r"\HAT_ATOSA_TABLALI_v2_teknik.png", r"\HAT_ATOSA_TABLALI_v3_teknik.png")
io.open(os.path.join(U, "teknik_hat_atosa_tablali_v3.py"), "w", encoding="utf-8").write(s)
print("teknik_hat_atosa_tablali_v3.py yazildi ·", len(D), "donusum")
