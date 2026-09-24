# -*- coding: utf-8 -*-
"""teknik_hat_atosa_tablali_v3 -> v4 : DUKKANDA HICBIR SEY KALMIYOR

Kemal: "temizlikti, yok yedekti, 4 gunluk kutuyu, 4 gunluk yedek icecegi, ne varsa
buna koy. Mekanda baska birsey istemiyorum, dukkanda sadece lavabo. Hatta bulasik
makinesini de buna koy, bizim kaplarin sigacagi sanayi tipi olanini arastir bul koy.
Bos bir suru yer var."

BULASIK MAKINESI — arastirildi ve secildi
  MEIKO M-iClean UM sinifi TEZGAH ALTI (undercounter)
    dis olcu 460 x 600 x 730 · sepet 500 x 500 · GIRIS YUKSEKLIGI 315 mm
    2,4 L/sepet · cevrim 90/120/180 sn · 40/30/20 sepet/saat · tank 11 L
  NEDEN GIYOTIN DEGIL: giyotin (MEIKO M-iClean HM) 635 x 750 x 1520, kapagi
  kalkinca ~2000 — hatta boyle bir hacim yok. Tezgah alti F modulunun tabanindaki
  680 x 770 x 835'lik BOS hacme oturuyor.
  KISIT: giris 315 mm, kasetimiz 280 x 400 x 360. Kaset AYAKTA girmiyor (360 > 315),
  YATIRILARAK girer (400 x 360 taban, 280 yukseklik) ve 500 x 500 sepete sigar.
  Calisma diski Ø340 duz yatar.

4 GUNLUK STOK — hesap
  KUTU     2 gun 560 -> gunde 280 -> 4 gun 1120. Sarjor 1077 mm yigin = 598 kutu.
           Yedek 522 kutu = 940 mm yatay yigin (blank 400 x 760).
           K modulunun alt bolmesi 330-1280 = 950 mm -> TAM OTURUYOR.
  ICECEK   2,6 gun 180 kutu -> gunde 69 -> 4 gun 277. Cekmece 180 -> yedek 97 kutu.
           K modulunun ust bolmesi 1695-2028 = 333 mm; kutu 115 boy, IKI KAT = 230.
           Taban 534 x 764 -> kat basina ~70 kutu, iki kat 140 > 97. SIGIYOR.
  TATLI    2,6 gun 14 -> gunde 5,4 -> 4 gun 22. Cekmece 14 -> yedek 8, ayni bolmede.
  TEMIZLIK B modulundeki "YEDEK BOLME 385 x 305" bos duruyordu; temizlik malzemesi
           oraya + makine deterjani/parlaticisi bulasik makinesinin yanina.

Not: yedek stok ROBOTUN ERISIMINDE DEGIL — eleman gunluk olarak ana gozlere aktarir.
Robot yalnizca ana cekmeceden ve sarjorden alir; o kisim degismedi.
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "teknik_hat_atosa_tablali_v3.py"), encoding="utf-8").read()
D = []

# ---------------------------------------------------------------- baslik
D.append((
    '''  ·  tabla kotları VARSAYIM (Atosa cevabı yok)  ·  ölçüler mm  ·  24 Eylül 2026")''',
    '''  ·  DÜKKÂNDA YALNIZ LAVABO: bulaşık makinesi, temizlik malzemesi ve 4 günlük kutu + içecek yedeği hattın içinde  ·  tabla kotları VARSAYIM (Atosa cevabı yok)  ·  ölçüler mm  ·  24 Eylül 2026")'''))

# ---------------------------------------------------------------- B: yedek bolme -> temizlik
# DIKKAT: ciz_B iki kez cagriliyor (bantli + tablali). Bizim degistirecegimiz
# TABLALI olan, yani SONUNCUSU.
_e = '''    ciz_B("YEDEK BÖLME|385 × 305 · boş")'''
_y = '''    ciz_B("TEMİZLİK MALZEMESİ|385 × 305 · deterjan · bez · eldiven · poşet")'''
_i = s.rfind(_e)
assert _i > 0, "ciz_B bulunamadi"
s = s[:_i] + _y + s[_i + len(_e):]

# ---------------------------------------------------------------- F tabani: BOS -> bulasik makinesi
D.append((
    '''              (760.0, 1440.0, 135.0, 970.0, "BOŞ", "680 × 770 × 835")])''',
    '''              (760.0, 1230.0, 135.0, 865.0, "BULAŞIK MAKİNESİ · tezgâh altı", "MEIKO M-iClean UM sınıfı · 460 × 600 × 730 · sepet 500 × 500 · giriş 315 · 2,4 L/sepet · 40 sepet/saat"),
              (1250.0, 1440.0, 135.0, 500.0, "MAKİNE DETERJANI + PARLATICI", "2 × 5 L bidon · seviye şamandıralı"),
              (1250.0, 1440.0, 520.0, 865.0, "BOŞ", "190 × 770 × 345")])'''))

# ---------------------------------------------------------------- K alt: kutu yedegi · K ust: icecek yedegi
D.append((
    '''    kesik(X_K, 60.0, 300.0, 140.0, 330.0, "YAĞ KARTUŞU", INK, "4 L × 2 · ısıtma")
    kesik(X_K, 320.0, 540.0, 140.0, 330.0, "K KARTI", INK, "tahrik")''',
    '''    kesik(X_K, 60.0, 300.0, 140.0, 330.0, "YAĞ KARTUŞU", INK, "4 L × 2 · ısıtma")
    kesik(X_K, 320.0, 540.0, 140.0, 330.0, "K KARTI", INK, "tahrik")
    kesik(X_K, 45.0, 555.0, 345.0, 1275.0, "KUTU YEDEĞİ · 4 GÜN", INK,
          "522 kutu = 940 mm yatay yığın (blank 400 × 760)|şarjör 598 + yedek 522 = 1120 = 4 gün|eleman şarjöre aktarır")'''))
D.append((
    '''    kapak(X_K, 33.0, W_K - 33.0, P + 355.0, 2028.0, "BOŞ")''',
    '''    kapak(X_K, 33.0, W_K - 33.0, P + 355.0, 2028.0, "İÇECEK + TATLI YEDEĞİ · 4 GÜN|97 kutu 330 ml (2 kat × 115) + 8 tatlı|çekmece 180 + yedek 97 = 277 = 4 gün")'''))

# ---------------------------------------------------------------- E sarjor yazisi
D.append((
    '''"KUTU ŞARJÖRÜ · alttan kaldırmalı|blank 400 × 760 yatay yığın · %s mm|= %d (1,8 mm) – %d (1,5 mm) kutu · 2 gün 560" % (sayi(yig), int(yig / 1.8), int(yig / 1.5))''',
    '''"KUTU ŞARJÖRÜ · alttan kaldırmalı|blank 400 × 760 yatay yığın · %s mm|= %d (1,8 mm) – %d (1,5 mm) kutu|4 GÜNLÜK YEDEK K MODÜLÜNDE" % (sayi(yig), int(yig / 1.8), int(yig / 1.5))'''))

# ---------------------------------------------------------------- icecek cekmecesi yazisi
D.append((
    '''CAP = {"hamur": (20, "top"), "lahm": (35, "top"), "icecek": (0, "180 kutu 330 ml + 14 tatlı · 2,6 gün")}''',
    '''CAP = {"hamur": (20, "top"), "lahm": (35, "top"), "icecek": (0, "180 kutu 330 ml + 14 tatlı · yedeği K'de → 4 gün")}'''))

# ---------------------------------------------------------------- parca listesi
D.append((
    '''        ("KONTROL", "ana pano PLC + UPS + robot kontrol kutusu: F tabanı, ray yanında (C üst bandı hazne sırasına gitti) · ekran yok (tablet)", "", ""),''',
    '''        ("BULAŞIK MAKİNESİ", "TEZGÂH ALTI · MEIKO M-iClean UM sınıfı · sepet 500 × 500 · giriş yüksekliği 315 · 2,4 L/sepet · çevrim 90/120/180 sn · 40 sepet/saat · tank 11 L", "1", "460 × 600 × 730 · F modülü tabanında · KASET YATIRILARAK yıkanır (280 × 400 × 360 → ayakta 360 > 315) · çalışma diski Ø340 düz yatar"),
        ("YEDEK STOK", "KUTU 522 adet (K alt bölme 950 mm) + İÇECEK 97 kutu ve 8 tatlı (K üst bölme, 2 kat) · şarjör ve çekmeceyle birlikte 4 GÜN", "", "robotun erişiminde DEĞİL — eleman günlük olarak ana gözlere aktarır"),
        ("TEMİZLİK", "deterjan · bez · eldiven · poşet: B modülü 385 × 305 bölmesi · makine deterjanı + parlatıcı 2 × 5 L: bulaşık makinesinin yanında", "", "dükkânda yalnız LAVABO kalır"),
        ("KONTROL", "ana pano PLC + UPS + robot kontrol kutusu: F tabanı, ray yanında (C üst bandı hazne sırasına gitti) · ekran yok (tablet)", "", ""),'''))

for e, y in D:
    assert e in s, "BULUNAMADI -> " + e[:70]
    s = s.replace(e, y, 1)

s = s.replace("TEKNİK RESİM  v3", "TEKNİK RESİM  v4")
s = s.replace(r"\HAT_ATOSA_TABLALI_v3_teknik.png", r"\HAT_ATOSA_TABLALI_v4_teknik.png")
io.open(os.path.join(U, "teknik_hat_atosa_tablali_v4.py"), "w", encoding="utf-8").write(s)
print("teknik_hat_atosa_tablali_v4.py yazildi ·", len(D), "donusum")
