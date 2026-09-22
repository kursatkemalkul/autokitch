# -*- coding: utf-8 -*-
"""kasar_cad_v12 -> harc_cad_v1   ·   HARÇ / SOS KASETI
Kemal (22 Eyl): "su harc kasetleri ile sos ayni sey aslinda, bu ikisinin nasil olacagini TAM MODELLE,
NOZZLE falan da yap. Full detayli uretilebilir — ben bunu disardan satin alicam ama en azindan gosterip
'bunu istiyorum' derim."

URUN: lahmacun harci ve pizza sosu — ikisi de MACUN/SIVI sinifi, ayni kaset.
  · yogunluk 1,05 g/mL [V: salca/harc 1,0-1,1]
  · parcacik <= 3 mm (soganin/biberin cekilmis hali) -> kopruleme yok, capi DEBI belirler
  · doz: lahmacun harci 110 g · pizza sosu 80 g [V: paftada yalniz kg var, porsiyon verilmedi]

GOVDE: 280'lik ORTAK GOVDE (kasar kalibi) — W 280 x D 325 x H 360, ic hacim 20,6 L.
  Paftadaki 21,6 kg @ 1,05 = 20,6 L, yani kabin AGZINA kadar dolu demek. %85 dolulukla 18,4 kg aliyorum;
  eksik kalan 3,2 kg UYARI olarak duruyor (ya doz dusecek ya gun icinde bir kez doldurulacak).

SIVIDA IKI YENI SORUN, IKI STANDART COZUM:
  1 DAMLAMA — vida durunca macun akmaya devam eder. Cozum: borunun ucunda SILIKON DUCKBILL (ordek gagasi)
    VALF. Basinc gelince acilir, kesilince kendi elastikligiyle kapanir; hareketli parcasi, yayi, contasi yok.
    Gida dolum makinelerinin standart parcasi, 1" olcusu raftan alinir.
  2 COKME/AYRISMA — sos beklerken su ustte, kati altta toplanir. Cozum: kasetteki KARISTIRICI ROTOR zaten
    var (kasar kalibindan gelir); dozdan once birkac tur cevrilir.

BORU CAPI: doz 110 g / 10 s = 11 g/s -> 10,5 mL/s. Ic O25 (1" duckbill'in standart olcusu) -> 491 mm2
-> 21 mm/s. Tupun ic O44'unden 22 mm'lik konik gecisle O25'e iner, dis O31 (tup disi O50'nin icinde).

ACIK KALAN: harc pideye IP gibi iner, kendiliginden YAYILMAZ. Yayma (spiral yol + yayici) ayri bir is;
bu model dozu verir, yaymayi vermez. Kemal'in karari bekleniyor.
"""
import io, os, re

U = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\_uretec".replace("WEBSITE", "WEBS\u0130TE")
s = io.open(os.path.join(U, "kasar_cad_v12.py"), encoding="utf-8").read()
n = [0]


def yama(a, b):
    global s
    assert a in s, "BULUNAMADI: " + a[:110]
    n[0] += 1
    s = s.replace(a, b, 1)


# ---- adlar ----
s = s.replace("kasar_cad_v12", "harc_cad_v1").replace("kasar_kabi_v12", "harc_kaseti_v1")
s = s.replace("kasar_v12", "harc_v1").replace("kasar_dolgu", "harc_dolgu").replace("kasar_pide_ustu", "harc_pide_ustu")
s = s.replace("kasar_dusen", "harc_dusen")
s = re.sub(r'MALZEME\.setdefault\(.kasar.', "MALZEME.setdefault('harc'", s)
s = s.replace('"kasar"', '"harc"').replace("'kasar'", "'harc'")
i = s.index('"""')
j = s.index('"""', i + 3)
s = s[:i] + ('"""AUTOKITCH · HARÇ / SOS KASETİ v1 (22 Eyl 2026) — kaşar kabı v12 gövdesinden türetildi.\n'
             'ÜRÜN: lahmacun harcı + pizza sosu (aynı sınıf: macun/sıvı, ρ 1,05, parçacık ≤ 3 mm).\n'
             'FARKI: çıkış borusu iç Ø25 ve ucunda SİLİKON DUCKBILL VALF — vida durunca damlamayı o kesiyor.\n'
             'Karıştırıcı rotor gövdeden geliyor: sos beklerken ayrışır, dozdan önce birkaç tur çevrilir.\n'
             'Hesap ve gerekçeler: yap_harc_v1.py\n"""\n') + s[j + 4:]

# ---- urun ozellikleri ----
yama("from kasar_akis_model_v2 import RHO, YASA, T_DOK, r_t",
     "from kasar_akis_model_v2 import RHO as RHO_KASAR, YASA, T_DOK, r_t     # akis yasasi ayni govdeden; YOGUNLUK urunun kendisi" + chr(10) +
     "RHO = 1.05                                                           # harc / sos g/mL [V: salca-harc 1,0-1,1; tartilacak]" + chr(10) +
     "KG2 = 18.4                                                           # 2 gunluk - 280lik kap 85% dolu" + chr(10) +
     "#   UYARI: pafta HAT v19da kaset basina 21,6 kg yaziyor; 21,6 / 1,05 = 20,6 L = kabin AGZINA kadar dolu." + chr(10) +
     "#   Gercekte 85% doluluk siniri -> 18,4 kg. Eksik 3,2 kg ya dozdan ya gun ici bir ek doldurmadan cikacak.")
s = s.replace("v4.dolum_kotu(8.8 / RHO)", "v4.dolum_kotu(KG2 / RHO)")
s = s.replace("100 * 8.8 / RHO / V", "100 * KG2 / RHO / V")
s = s.replace("(ic boy %.0f) - 8,8 kg", "(ic boy %.0f) - KG kg")
s = s.replace(chr(34) + "HACIM %.1f L (ic boy %.0f) · 8,8 kg @ %.2f", chr(34) + "HACIM %.1f L (ic boy %.0f) · %.1f kg @ %.2f")
s = s.replace("% (V, D - 2 * TP, RHO, yd,", "% (V, D - 2 * TP, KG2, RHO, yd,")
yama("BORU_D, BORU_ET, BORU_ALT, BORU_GECIS = 44.0", "BORU_D, BORU_ET, BORU_ALT, BORU_GECIS = 25.0")

# ---- DUCKBILL VALF ----
yama('    ekle("tasima_tapasi",',
     '''    # ---- DUCKBILL (ÖRDEK GAGASI) VALF — damlamayı kesen tek parça ----
    # Boruya geçen bilezik + basınçla açılan yassı gaga. Hareketli parçası, yayı, contası yok;
    # gıda dolum makinelerinin standart parçası, 1" ölçüsü raftan alınır.
    RB_V = BORU_D / 2 + BORU_ET
    vy0, vy1 = BORU_ALT - 26.0, BORU_ALT + 14.0                                                          # gaga ucu … bileziğin üst kotu
    vlf = sily(0, BZ, RB_V + 1.6, BORU_ALT - 1.0, vy1)                                                   # boruya geçen bilezik
    vlf = vlf.union(koni_y(BZ, 5.0, RB_V + 1.6, vy0 + 6.0, BORU_ALT - 1.0))                              # konik gövde
    vlf = vlf.union(kut(-11.0, 11.0, vy0, vy0 + 7.0, BZ - 5.0, BZ + 5.0))                                # yassı gaga ağzı
    vlf = vlf.cut(sily(0, BZ, RB_V + 0.2, BORU_ALT - 2.0, vy1 + 1.0))                                    # boru oturma yuvası
    vlf = vlf.cut(koni_y(BZ, 1.2, BORU_D / 2, vy0 + 5.0, BORU_ALT - 1.5))                                # iç kanal
    vlf = vlf.cut(kut(-9.0, 9.0, vy0 - 1.0, vy0 + 5.5, BZ - 0.9, BZ + 0.9))                              # gaganın kapalı dudağı (yarık)
    ekle("duckbill_valf", vlf, "silikon",
         bom=("Duckbill valf 1\\"", 1, "platin silikon, gıda onaylı · KATALOG PARÇASI", "borunun ucuna geçer; basınçla açılır, doz bitince kendi elastikliğiyle kapanır → damlama yok"))

    ekle("tasima_tapasi",''')

# ---- etiket / bom metinleri ----
s = s.replace("KAŞAR KABI", "HARÇ / SOS KASETİ").replace("Kaşar kabı", "Harç / sos kaseti").replace("kaşar", "harç")

s = s.replace("KG2 = 18.4", "MALZEME.setdefault('harc', dict(renk=(0.72, 0.20, 0.12, 1.0), met=0.0, ruf=0.85))" + chr(10) +
              "MALZEME.setdefault('harc_dolgu', dict(renk=(0.72, 0.20, 0.12, 1.0), met=0.0, ruf=0.85))" + chr(10) + "KG2 = 18.4", 1)
s = s.replace("v4.harc_dolgu", "v4.kasar_dolgu")   # dolgu fonksiyonu ORTAK modulde, adi degismez
s = s.replace("BORU_D / 2 + BORU_ET + 2.0, BORU_ALT - 8.0, BORU_ALT + 14.0", "BORU_D / 2 + BORU_ET + 4.0, BORU_ALT - 38.0, BORU_ALT - 18.0")
s = s.replace("BORU_D / 2 + BORU_ET + 0.2, BORU_ALT - 6.0, BORU_ALT + 16.0", "BORU_D / 2 + BORU_ET + 2.2, BORU_ALT - 36.0, BORU_ALT - 16.0")
s = s.replace("kap makine dışındayken çıkış borusunun ucuna geçer", "kap makine dışındayken DUCKBILL VALFIN ucuna geçer (valf zaten kapatır; tapa taşımada korur)")
io.open(os.path.join(U, "harc_cad_v1.py"), "w", encoding="utf-8").write(s)
print("harc_cad_v1.py yazildi ·", n[0], "yama")
