# -*- coding: utf-8 -*-
"""h3/yap_mek_v1.py — MEKANİZMA AĞACI (Kemal 1 Eki 2026: "istasyon → mekanizma → alt kırılım; K → Sprey: spreyin motoru, kablosu,
hava parçaları dahil her şeyi · Bıçak · E → Kutu katlama … hava parçaları ve motorlar da kendi mekanizmasının altında olsun").

Üç iş yapar:
  1) mekanizma_bul(birim, ad, mal) → "ISTASYON/Mekanizma" (ör. "K/Sprey"). Kablo / rakor / ELK_* parçaları beslediği cihazın
     mekanizmasına gider (kablo adı okunur: kablo_K_PulsaJet → K/Sprey). Kural tutmazsa "<istasyon>/Gövde".
     kapak_mi(birim, ad, on) → ön kapak / kanat / servis kapağı / düşer kapak / çekmece önü (+ menteşe, basaç) mı.
  2) uygula(s) → montaj kaynağına (hat3_montaj_vN.py) metin yaması: GLB'ye "kat" ile AYNI yoldan üçgen aralıkları yazılır
       primitive extras  "mek" = [mekanizma indisi, ilk indis, indis sayısı, …]   (kategori "kat" ile aynı biçim)
       primitive extras  "kpk" = [ilk indis, indis sayısı, …]                       (kapak üçgenleri)
       sahne extras      "mekanizmalar" = [{kod, istasyon, ad}, …]                  (indis → ad)
     Kullanım (bir sonraki yap_hat3_montaj_vN.py içinde):
         import yap_mek_v1 as MEK
         s = MEK.uygula(s)            # s = hat3_montaj kaynağı (str) · yamalı kaynak döner · zaten yamalıysa aynen döner
  3) python yap_mek_v1.py <parca_kutulari.json> <hat3_vN.glb> <mekanizma_v3.json>
     GLB henüz etiket taşımıyorsa sayfa (mekanizma-v3.js) bu dosyayı okur: parça → mekanizma tablosu + mevcut GLB'nin
     üçgen aralıkları (parça kutularına göre çıkarılır: her parçanın köşe noktaları ağda ardışık blok — blok sınırı kesin,
     blok → parça eşlemesi sıralı (monoton) en küçük kutu ile).

v3.7 düzeltmeleri (1 Eki 2026 · Claude · YEREL) — montaj bloğu MEK v2:
  · ELK_ANA_PANO_UF (U_F ana panosu, 70 parça) → "Elektrik/Ana pano" (v3.6'da birim adı ELK_ANA_PANO_UF oldu, kural ELK_ANA_PANO'daydı → "Ana hat"a düşüyordu).
  · ELK_ISTASYON (istasyon kutuları + Harting soket / fiş + ana pano tarafı uçlar) ve ELK_QR_KUTU → ait olduğu istasyonun "<istasyon>/Elektrik"
    mekanizması; istasyon kodu parça adının "_" ile ayrılmış parçalarından okunur: A · TOPPING · DOLAP (= B) · B · K · E · F · QR · ROBOT (= Robot).
    Kodsuz ELK_ISTASYON parçası: bina beslemesi / modem ucu → "Elektrik/Ana hat", toplama kanalı vb. → "Elektrik/Ana pano"; ELK_QR_KUTU kodsuzsa QR.
  · ZEMIN_DOSEME → "Çevre/Zemin".
  · Parçasız yer tutucu kutular (BOS_YER_TUTUCU: ROBOT_RAY · ROBOT_1 · ROBOT_1_KOL — durum KUTU / KATALOG, 0 parça) mekanizma listesine girmez
    (düğmesi boş kalıyordu); montaj bloğunda mekanizma yalnız gerçekten üçgen aldığında listeye yazılır (boş düğme yok).
  · uygula(s): v1 bloğu taşıyan metinde (hat3_montaj_v6) bloğu v2 ile değiştirir; yamasız metinde (v5 ve öncesi) tam yamayı uygular.
"""
import io, json, os, re, struct, sys

# ------------------------------------------------------------------ İSTASYONLAR (sıra = sayfadaki sıra)
ISTASYON = [
    ("A", "A · Açıcı", ["A"]),
    ("B", "B · Çekmeceli dolap", ["B"]),
    ("TOPPING", "TOPPING", ["C"]),
    ("F", "F · Fırın", ["D"]),
    ("K", "K · Kesme + sprey", ["K"]),
    ("E", "E · Kutu", ["E"]),
    ("U", "U · Üst depo", ["U"]),
    ("QR", "QR · Teslim dolabı", ["S"]),
    ("Tezgâh", "Tezgâh", ["S"]),
    ("Robot", "Robot", ["-"]),
    ("Elektrik", "Elektrik", ["-", "S"]),
    ("Çevre", "Çevre (ürün · insan)", []),
]
IST_SIRA = {k: i for i, (k, _a, _m) in enumerate(ISTASYON)}

_I = re.I


def _r(p):
    return re.compile(p, _I)


# TOPPING içindeki istasyon-içi mekanizmalar (sıra önemli: ilk tutan kazanır)
_TOP = [
    ("A/Açıcı", _r(r"acici")),
    ("TOPPING/Sucuk", _r(r"^kuru_surucu_[01]$")),                                # sürücü 0 · 1 = sucuk rotor · helezon (kablo adlarından)
    ("TOPPING/Kaşar", _r(r"^kuru_surucu_[23]$")),                                # sürücü 2 · 3 = kaşar rotor · helezon
    ("TOPPING/Soğutma", _r(r"sogutma|evap|yogusma|sicak_gaz|arka_hava_|arka_duvar_kaset_yuzu|teknik_bolme_arka_emis|klf66")),
    ("TOPPING/Kaşar", _r(r"kasar")),
    ("TOPPING/Sucuk", _r(r"sucuk")),
    ("TOPPING/Kıyma", _r(r"kiyma")),
    ("TOPPING/Kuşbaşı", _r(r"kusbasi")),
    ("TOPPING/Sos", _r(r"(^|_)sos(_|$)")),
    ("TOPPING/Harç", _r(r"(^|_)harc(_|$)")),
    ("TOPPING/Hava dağıtımı", _r(r"rakor_hava_ana|sartlandirici|valf_adasi|valf_bobini|hava_hatti")),
    ("TOPPING/Pano", _r(r"^kuru_(pano|din|ups|guc|surucu)")),
    ("TOPPING/Tabla", _r(r"mekanizma_teknesi|ray_kirisi|kayis_kirisi|baglama_lamasi|kizak_blogu|araba_plakasi|doner_yatak|ayar_bilezigi|ayar_konum_pimi|"
                         r"^bk_|^st_|donus_motoru|tahrik_lokmasi|^x_|avara|kayis_kolu|kayis_kelepcesi|siyirici_apron|kirinti_cekmecesi|enerji_zinciri|"
                         r"kilit_burcu|tabla|uc_tamponu|cikis_yarigi_contasi|fire_silecegi|lineer_ray|ray_ortu")),
]
# K pano içindeki havalı / tartılı parçalar
_K_EL = [
    ("K/İtici", _r(r"valf_SY3120_[01]|hava_hortumu_X")),
    ("K/Bıçak", _r(r"valf_SY3120_2|hava_hortumu_DGRF")),
    ("K/Sprey", _r(r"tarti")),
    ("K/Hava dağıtımı", _r(r"valf_adasi|valf_kor|sartlandirici|hava_giris|hava_hortumu_(giris|manifold)")),
]
# ELK_* kabloları: beslediği cihaz adı kablonun adında
_ELK_TOPPING = [
    ("TOPPING/Soğutma", _r(r"sogutma|evap|klf")),
    ("TOPPING/Sucuk", _r(r"sucuk|surucu_[01]_pano")),
    ("TOPPING/Kaşar", _r(r"kasar|surucu_[23]_pano")),
    ("TOPPING/Hava dağıtımı", _r(r"valf_adasi")),
    ("TOPPING/Tabla", _r(r"sabit_tahrik|enerji_zinciri|sensor_x|tabla|x_motoru|rakor_G9")),
    ("F/Yükleme bandı", _r(r"yukleme_bandi|rakor_G6|rakor_G8")),
    ("A/Emniyet", _r(r"kablo_A_|kanal_A_|rakor_G7")),
    ("TOPPING/Pano", _r(r".")),
]
_ELK_K = [
    ("K/Sprey", _r(r"pulsajet|yag|tarti|rakor_G4")),
    ("K/Bant", _r(r"urun_sensoru|EC5000")),
    ("K/Bıçak", _r(r"DGRF")),
    ("K/Pano", _r(r".")),
]
_ELK_DOLAP = [
    ("B/Çekmeceler", _r(r"reed|CEK_")),
    ("B/Soğutma", _r(r"secop|evap|fan")),
    ("B/Pano", _r(r".")),
]
_ELK_QR = [
    ("QR/Gözler", _r(r"^goz_")),
    ("Robot/Kablo + zincir", _r(r"robot")),
    ("QR/Pano", _r(r"qrk_(kart|modem|ups)|qr_kart|ups_|modem")),
    ("Elektrik/Ana hat", _r(r"qrk_(guc|veri)_|^giris_|bina")),
    ("QR/Pano", _r(r".")),
]

# v3.7 · istasyon kutuları + Harting (ELK_ISTASYON, ELK_QR_KUTU): parça adındaki istasyon kodu → "<istasyon>/Elektrik"
ELK_IST_KOD = {"A": "A", "TOPPING": "TOPPING", "DOLAP": "B", "B": "B", "K": "K", "E": "E", "F": "F", "QR": "QR", "ROBOT": "Robot"}
_ELK_IST_KODSUZ = [
    ("Elektrik/Ana hat", _r(r"bina|modem")),                                     # bina beslemesi + modem ucu: dışarıdan ana panoya gelen hat
    ("Elektrik/Ana pano", _r(r".")),                                             # toplama kanalı vb. (ana panonun yanında)
]
# parçasız yer tutucular (durum KUTU / KATALOG, parça 0): mekanizma listesine girmez — düğmesi boş kalıyordu (v3.6: Robot/Ray · Robot/Kol)
BOS_YER_TUTUCU = ("ROBOT_RAY", "ROBOT_1", "ROBOT_1_KOL")


def elk_istasyon_kodu(ad):
    """parça adından istasyon kodu (ilk eşleşen '_' parçası, büyük harf): harting_ANA_PANO_TOPPING_fis → TOPPING · harting_DOLAP_soket → B · yoksa None"""
    for t in (ad or "").split("_"):
        if t in ELK_IST_KOD:
            return ELK_IST_KOD[t]
    return None


def elk_istasyon_mek(birim, ad):
    """ELK_ISTASYON / ELK_QR_KUTU parçası → "<istasyon>/Elektrik" (kodsuzsa: ELK_QR_KUTU → QR · ELK_ISTASYON → Ana hat / Ana pano)"""
    k = elk_istasyon_kodu(ad)
    if k:
        return k + "/Elektrik"
    if birim == "ELK_QR_KUTU":
        return "QR/Elektrik"
    return _ilk(_ELK_IST_KODSUZ, ad or "") or "Elektrik/Ana pano"                # ad yok (düğüm varsayılanı) → ana pano

# birim → (sabit mekanizma) — ada bakılmayan birimler
_BIRIM = {
    "KAIDE_A": "A/Gövde", "A_MODULER": "A/Gövde",
    "B_KASA": "B/Gövde", "B_TASIYICI": "B/Gövde", "B_MODULER": "B/Gövde", "B_SOGUTMA": "B/Soğutma", "DUZ_B_SERPANTIN": "B/Soğutma",
    "B_ELEKTRIK": "B/Pano", "B_KABLO": "B/Pano", "B_DEPO": "B/Soğuk depo",
    "KAIDE_C": "TOPPING/Gövde",
    "F_TP10_GOVDE": "F/Fırın", "F_TP10_KONVEYOR": "F/Fırın", "F_CIKIS_PLAKA": "F/Fırın", "F_DONER": "F/Fırın",
    "F_YUKLEME_BANDI": "F/Yükleme bandı", "F_DAVLUMBAZ": "F/Davlumbaz", "U_F_BACA": "F/Davlumbaz",
    "HAVA_KOMPRESOR": "F/Kompresör", "F_KOMP_AYAK": "F/Kompresör",
    "F_UST_KABIN": "F/Gövde", "F_UST_KAPAK": "F/Gövde", "F_UST_RAF": "F/Gövde", "D_PIZZA_YEDEK_UST": "F/Kutu yedeği",
    "K_BANT": "K/Bant", "K_KESICI": "K/Bıçak", "K_ITICI": "K/İtici", "K_YAG": "K/Sprey", "K_GOVDE": "K/Gövde", "K_ELEKTRIK": "K/Pano",
    "E_BESLEYICI": "E/Besleyici", "E_KOSE": "E/Kutu katlama", "E_KAPAK": "E/Kutu katlama", "E_KOPRU": "E/Kutu katlama",
    "E_PISTON": "E/Kutu katlama", "E_PARMAK": "E/Kutu katlama", "E_KALIP": "E/Kutu katlama", "E_KUTU": "E/Kutu katlama", "E_PIZZA": "E/Kutu katlama",
    "E_GOVDE": "E/Gövde", "E_MODULER": "E/Gövde", "E_ELEKTRIK": "E/Pano", "E_COP": "E/Robot çöpü", "DUZ_E_OLUK": "E/Robot çöpü",
    "U_A_GOVDE": "U/Gövde", "U_F_GOVDE": "U/Gövde", "U_KE_GOVDE": "U/Gövde", "U_ICECEK_YEDEK": "U/Yedek stok", "U_KUTU_YEDEK": "U/Yedek stok",
    "QR_GOVDE": "QR/Gövde", "QR_GOZLER": "QR/Gözler", "QR_DONER": "QR/Gözler", "QR_KILIT_KARTI": "QR/Pano", "QR_UPS": "QR/Pano",
    "QR_HAVALANDIRMA": "QR/Pano", "QR_MUSTERI_PANELI": "QR/Müşteri paneli", "QR_ROBOT_KONTROL": "Robot/Kontrol kutusu",
    "ROBOT_RAY": "Robot/Ray", "ROBOT_1": "Robot/Kol", "ROBOT_1_KOL": "Robot/Kol",
    "ROBOT_ENERJI_ZINCIRI": "Robot/Kablo + zincir", "ROBOT_KABLOSU": "Robot/Kablo + zincir", "ROBOT_ZINCIR_OLUGU": "Robot/Kablo + zincir",
    "ROBOT_KABLO_KOPRUSU": "Robot/Kablo + zincir",
    "ELK_ANA_PANO": "Elektrik/Ana pano", "ELK_ANA_HAT": "Elektrik/Ana hat", "ELK_ZEMIN_KANALI": "Elektrik/Ana hat",
    "ELK_ANA_PANO_UF": "Elektrik/Ana pano", "ANA_PANO": "Elektrik/Ana pano",           # v3.7 · U_F ana panosu (h3_ana_pano_v1 · birimsiz yedek adı ANA_PANO)
    "TEZGAH_BULASIK": "Tezgâh/Bulaşık makinesi", "TEZGAH_EVYE": "Tezgâh/Evye", "TEZGAH_HIJYEN": "Tezgâh/Evye", "DUZ_TEZGAH_DUVAR": "Tezgâh/Gövde",
    "INSAN_180cm": "Çevre/İnsan figürü", "URUN": "Çevre/Ürün", "ZEMIN_DOSEME": "Çevre/Zemin",
}
# özel (menteşeli / dönen) düğüm grupları: ada kaydı olmayan aralıklar için
_GRUP = [
    (_r(r"^ACICI|^KONI"), "A/Açıcı"), (_r(r"^ARABA|^TABLA"), "TOPPING/Tabla"),
    (_r(r"_SOS$"), "TOPPING/Sos"), (_r(r"_HARC$"), "TOPPING/Harç"), (_r(r"_KIYMA$"), "TOPPING/Kıyma"), (_r(r"_KUSBASI$"), "TOPPING/Kuşbaşı"),
    (_r(r"KASAR"), "TOPPING/Kaşar"), (_r(r"SUCUK"), "TOPPING/Sucuk"),
]


def istasyon_of(mek):
    return mek.split("/")[0]


def _ilk(kurallar, ad):
    for mek, r_ in kurallar:
        if r_.search(ad): return mek
    return None


def mekanizma_bul(birim, ad, mal=None, grup=None):
    """birim + parça adı (+ malzeme) → "ISTASYON/Mekanizma". ad None → birimin varsayılanı (grup verilirse önce o)."""
    birim = birim or ""
    a = ad or ""
    if birim == "TOPPING_MODUL" or birim == "TOPPING_DONER":
        if a:
            return _ilk(_TOP, a) or "TOPPING/Gövde"
        g = _grup(grup)
        return g or "TOPPING/Gövde"
    if birim.startswith("CEK_"): return "B/Çekmeceler"
    if birim == "ELK_TOPPING": return _ilk(_ELK_TOPPING, a) if a else "TOPPING/Pano"
    if birim == "ELK_K": return _ilk(_ELK_K, a) if a else "K/Pano"
    if birim == "ELK_DOLAP": return _ilk(_ELK_DOLAP, a) if a else "B/Pano"
    if birim == "ELK_QR_KABLO": return _ilk(_ELK_QR, a) if a else "QR/Pano"
    if birim == "ELK_QR_MONTAJ": return "QR/Gözler" if a.startswith("goz_") else "QR/Gövde"
    if birim in ("ELK_ISTASYON", "ELK_QR_KUTU"): return elk_istasyon_mek(birim, a)   # v3.7 · istasyon kutusu + Harting → kendi istasyonunun Elektrik'i
    if birim in ("A_GOVDE", "A_ONYUZ"):
        return "A/Emniyet" if re.search(r"emniyet|isik_perdesi", a) else "A/Gövde"
    if birim == "K_ELEKTRIK" and a:
        return _ilk(_K_EL, a) or "K/Pano"
    if birim == "KAIDE_C" and "emis_filtresi" in a: return "TOPPING/Soğutma"
    if birim == "E_SARJOR":
        if not a: return "E/Şarjör"
        return "E/Asansör" if a.startswith("asansor") else "E/Şarjör"
    if birim == "E_ELEKTRIK" and a:
        if "yigin_ustu" in a: return "E/Asansör"
        if "blank_var" in a: return "E/Besleyici"
        if "kutu_dolu" in a: return "E/Kutu katlama"
        return "E/Pano"
    if birim == "F_UST_KABIN" and a:
        if "kompresor" in a: return "F/Kompresör"
        if "davlumbaz" in a: return "F/Davlumbaz"
        if "firin" in a: return "F/Fırın"
    if birim in _BIRIM: return _BIRIM[birim]
    if birim.startswith("ROBOT_"): return "Robot/Kol"
    if birim.startswith("TEZGAH_"): return "Tezgâh/Gövde"
    if birim.startswith("URUN"): return "Çevre/Ürün"
    if birim.startswith("ELK_"): return "Elektrik/Ana hat"
    if birim.startswith("U_"): return "U/Gövde"
    if birim.startswith("QR_"): return "QR/Gövde"
    if birim.startswith("E_"): return "E/Gövde"
    if birim.startswith("K_"): return "K/Gövde"
    if birim.startswith(("F_", "D_")): return "F/Gövde"
    if birim.startswith("B_"): return "B/Gövde"
    if birim.startswith("A_"): return "A/Gövde"
    return "Çevre/Diğer"


def _grup(grup):
    if not grup: return None
    for r_, mek in _GRUP:
        if r_.search(grup): return mek
    return None


def mekanizma_dugum(adi, mal=None):
    """GLB düğüm adı ("BIRIM__ton" ya da "BIRIM__ton__GRUP" / "BIRIM__GRUP") → varsayılan mekanizma (ada kaydı olmayan aralıklar)"""
    s_ = adi.split("__")
    birim = s_[0]
    grup = s_[-1] if len(s_) >= 3 else (s_[1] if len(s_) == 2 and s_[1].isupper() else None)
    if birim == "F_DONER" and grup and "_GB_" in grup: return "F/Yükleme bandı"
    return mekanizma_bul(birim, None, mal, grup)                              # grup yalnız TOPPING'te anlamlı (ACICI · ARABA · PISTON_SOS …)


# ------------------------------------------------------------------ KAPAKLAR (ön kapaklar · kanatlar · servis / düşer kapaklar · çekmece önleri)
_KPK_EVET = _r(r"kapak|kapag|kapisi|kapi_|kanat|klape|_on_(dis|ic)_sac|_on_pu$|_on_fitil|onyuz_K[12]_|flipper|alt_panel|musteri_(alt|ust)_panel|"
               r"tipon|bas_ac|basac|gazli_yay|burulma_kutusu|yay_pimi|mentese|servis_kilidi|cekmece_onu|kapak_kulpu")
_KPK_HAYIR = _r(r"kablo_kanal|kanal_kapa|kanali_kapa|kanal.*kapak|oluk_kapag|kopru_kapag|ray_ortu|cop_kovasi|kapak_motoru|kapak_sensoru|kapak_mili|"
                r"mil_yatag|motor_braketi|sensor_braketi|mandal_braketi|kapak_masasi|kapak_kolu|kapak_alt_pla|^B_|flap_|kol_|yatak_kapagi|"
                r"pano_kablo|evap_|depo_kapak_1|enkoder|esigi|tavasi_kapak|pulsajet|bidon|valfi_kapak|isitici|robot_kablo|uc_kapagi|rotor_kapagi|silindiri_kapagi|kasar_cad|sucuk_cad")


def kapak_mi(birim, ad, on=0):
    """parça kapak (ön kapak / kanat / servis kapağı / düşer kapak / çekmece önü + menteşe, basaç, gazlı yay) mı"""
    a = ad or ""
    if birim in ("E_KAPAK", "E_KUTU", "E_KOSE", "E_PIZZA") or birim.startswith(("ELK_ANA_HAT", "ELK_ZEMIN", "ROBOT_")): return False
    if on: return True
    if birim == "F_UST_KAPAK": return True
    if _KPK_HAYIR.search(a): return False
    return bool(_KPK_EVET.search(a))


# ------------------------------------------------------------------ MONTAJ YAMASI
ISARET = "# ---- MEK v2 · MEKANİZMA AĞACI (yap_mek_v1)"
ISARET_V1 = "# ---- MEK v1 · MEKANİZMA AĞACI (yap_mek_v1)"                       # hat3_montaj_v6'daki eski blok (uygula v2 ile değiştirir)
_CAPA_V72 = "# ---- v72 · BAĞIMSIZ İSTASYONLAR"
_YAMA_BLOK = ISARET + r'''
import yap_mek_v1 as _MEK1                                                                            # h3/ sys.path'te
MEK_LISTE, MEK_I, MEK_UCGEN, MEK_BOS = [], {}, {}, set()


def _mek_i(kod):
    if kod not in MEK_I:
        MEK_I[kod] = len(MEK_LISTE); MEK_LISTE.append(dict(kod=kod, istasyon=kod.split("/")[0], ad=kod.split("/", 1)[1]))
    return MEK_I[kod]


def _mek_bos(adi):
    """MEK v2 · parçasız yer tutucu kutu (durum KUTU / KATALOG, 0 parça: ROBOT_RAY · ROBOT_1 · ROBOT_1_KOL) → mekanizma listesine girmez (boş düğme)"""
    if adi not in _MEK1.BOS_YER_TUTUCU: return False
    return any(b_["kod"] == adi and b_["durum"] in ("KUTU", "KATALOG") and not b_.get("parca") for b_ in B)


def _mek_araliklari(m, adi, mal):
    """kategori "kat" ile AYNI aralık biçimi: [mekanizma, ilk, sayı, …] · kaydı olmayan aralık düğümün varsayılanı ·
    MEK v2: mekanizma yalnız üçgen aldığında listeye yazılır (boş düğme yok) · parçasız yer tutucu → aralık yok"""
    if _mek_bos(adi):
        MEK_BOS.add(adi); return []
    n = len(m.I); varsay = _MEK1.mekanizma_dugum(adi, mal); out, pos = [], 0

    def ek(kod, s0, cnt):
        if cnt <= 0: return
        c = _mek_i(kod); MEK_UCGEN[c] = MEK_UCGEN.get(c, 0) + cnt // 3
        if out and out[-3] == c and out[-2] + out[-1] == s0: out[-1] += cnt
        else: out.extend([c, s0, cnt])
    for k_, s0, cnt in sorted(getattr(m, "_katr", []), key=lambda r_: r_[1]):
        if s0 > pos: ek(varsay, pos, s0 - pos)
        if s0 < pos: cnt -= pos - s0; s0 = pos
        if cnt <= 0: continue
        ek(_MEK1.mekanizma_bul(k_[0], k_[1], k_[2]) if k_ else varsay, s0, cnt); pos = s0 + cnt
    if pos < n: ek(varsay, pos, n - pos)
    return out


def _kpk_araliklari(m, adi, mal):
    """kapak üçgenleri: [ilk, sayı, …] · saydam ön kapak malzemesi (on_seffaf) her zaman kapak"""
    if (mal or "").endswith("__on_seffaf"): return [0, len(m.I)] if m.I else []
    out, pos = [], 0
    for k_, s0, cnt in sorted(getattr(m, "_katr", []), key=lambda r_: r_[1]):
        if s0 < pos: cnt -= pos - s0; s0 = pos
        if cnt <= 0: continue
        if k_ and _MEK1.kapak_mi(k_[0], k_[1], 1 if k_[2] == "on_seffaf" else 0):
            if out and out[-2] + out[-1] == s0: out[-1] += cnt
            else: out.extend([s0, cnt])
        pos = s0 + cnt
    return out


'''


_R_EXTRAS = [
    ('"extras": {"kat": _kat_araliklari(m, adi, mal, _ks, _kb)}}',
     '"extras": {"kat": _kat_araliklari(m, adi, mal, _ks, _kb), "mek": _mek_araliklari(m, adi, mal), "kpk": _kpk_araliklari(m, adi, mal)}}'),
    ('"extras": {"kat": _kat_araliklari(m, o["ad"], k_, _ks, _kb)}}',
     '"extras": {"kat": _kat_araliklari(m, o["ad"], k_, _ks, _kb), "mek": _mek_araliklari(m, o["ad"], k_), "kpk": _kpk_araliklari(m, o["ad"], k_)}}'),
    ('"extras": {"kategoriler": [dict(kod=k_["kod"], ad=k_["ad"], icerik=k_["icerik"], kime=k_["kime"]) for k_ in KAT_LISTE]}}',
     '"extras": {"kategoriler": [dict(kod=k_["kod"], ad=k_["ad"], icerik=k_["icerik"], kime=k_["kime"]) for k_ in KAT_LISTE], "mekanizmalar": list(MEK_LISTE)}}'),
]
_KAT_DENETIM = '    assert len(_kd["ucgen"]) >= 9, "v91: kategori eksik %s" % list(_kd["ucgen"])\n'
_YAZ_V1 = ('    print("MEK v1 · MEKANIZMALAR: %d (%s)" % (len(MEK_LISTE), ", ".join(m_["kod"] for m_ in MEK_LISTE)))\n'
           '    assert len(MEK_LISTE) >= 20, "MEK v1: mekanizma eksik"\n')
_YAZ_V2 = ('    print("MEK v2 · MEKANIZMALAR: %d (%s) · listeden cikan parcasiz yer tutucu: %s" % (len(MEK_LISTE), ", ".join(m_["kod"] for m_ in MEK_LISTE), ", ".join(sorted(MEK_BOS)) or "yok"))\n'
           '    assert len(MEK_LISTE) >= 20 and all(MEK_UCGEN.get(i_, 0) > 0 for i_ in range(len(MEK_LISTE))), "MEK v2: mekanizma eksik / bos dugme %s" % [m_["kod"] for j_, m_ in enumerate(MEK_LISTE) if not MEK_UCGEN.get(j_)]\n')


def uygula(s):
    """hat3_montaj kaynağına mekanizma + kapak etiketlerini ekler (GLB primitive extras "mek" / "kpk", sahne extras "mekanizmalar").
    v2 bloğu varsa aynen döner · v1 bloğu varsa (hat3_montaj_v6) blok + özet satırı v2 ile değiştirilir · yamasızsa tam yama."""
    if ISARET in s:
        return s
    if ISARET_V1 in s:                                                            # v6 metni: extras çapaları zaten yamalı → yalnız blok + özet
        assert s.count(ISARET_V1) == 1 and s.count(_CAPA_V72) == 1, "yap_mek_v1: v1 bloğu / v72 çapası tekil değil"
        i0, i1 = s.index(ISARET_V1), s.index(_CAPA_V72)
        assert i0 < i1, "yap_mek_v1: v1 bloğu v72 çapasından sonra"
        s = s[:i0] + _YAMA_BLOK + s[i1:]
        assert s.count(_YAZ_V1) == 1, "yap_mek_v1: v1 özet satırı yok / tekil değil"
        s = s.replace(_YAZ_V1, _YAZ_V2, 1)
        for _a, b in _R_EXTRAS:
            assert s.count(b) == 1, "yap_mek_v1: v1 extras yaması eksik: " + b[:60]
        compile(s, "hat3_montaj_mek", "exec")
        return s
    for a, b in _R_EXTRAS:
        assert s.count(a) == 1, "yap_mek_v1: çapa bulunamadı / tekil değil: " + a[:60]
        s = s.replace(a, b)
    capa = "\n\n" + _CAPA_V72
    assert s.count(capa) == 1, "yap_mek_v1: v72 çapası yok"
    s = s.replace(capa, "\n\n" + _YAMA_BLOK + capa.lstrip("\n"), 1)
    assert s.count(_KAT_DENETIM) == 1, "yap_mek_v1: kategori denetimi çapası yok"
    s = s.replace(_KAT_DENETIM, _KAT_DENETIM + _YAZ_V2, 1)
    compile(s, "hat3_montaj_mek", "exec")
    return s


# ------------------------------------------------------------------ SAYFA TABLOSU (mekanizma_v3.json) — GLB etiketsizken
def _glb_oku(yol):
    b = open(yol, "rb").read()
    L = struct.unpack("<I", b[12:16])[0]
    g = json.loads(b[20:20 + L].decode("utf-8"))
    o = 20 + L
    L2 = struct.unpack("<I", b[o:o + 4])[0]
    return g, b[o + 8:o + 8 + L2]


def _dizi(g, bin_, ai):
    import numpy as np
    a = g["accessors"][ai]; v = g["bufferViews"][a["bufferView"]]
    dt = {5126: np.float32, 5125: np.uint32, 5123: np.uint16}[a["componentType"]]
    n = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}[a["type"]]
    off = v.get("byteOffset", 0) + a.get("byteOffset", 0)
    arr = np.frombuffer(bin_, dt, a["count"] * n, off)
    return arr.reshape(-1, n) if n > 1 else arr


def _quat_mat(q):
    import numpy as np
    x, y, z, w = q
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


def tablo_yaz(parca_yol, glb_yol, cikis, x_e=4400.0):
    import numpy as np
    PK = json.load(io.open(parca_yol, encoding="utf-8"))
    g, bin_ = _glb_oku(glb_yol)
    mats = [m["name"] for m in g["materials"]]
    # parça → mekanizma
    parca, birim_v, kutu, say = {}, {}, {}, dict(toplam=0, ozel=0, govde=0, kapak=0)
    for b_, L_ in PK["parca"].items():
        birim_v[b_] = mekanizma_bul(b_, None)
        for p in L_:
            mk = mekanizma_bul(b_, p[0], None); parca[b_ + "|" + p[0]] = mk
            say["toplam"] += 1
            if mk.endswith("/Gövde"): say["govde"] += 1
            else: say["ozel"] += 1
            if kapak_mi(b_, p[0], p[1]): say["kapak"] += 1
            bx = [v_ / 1000.0 for v_ in p[2:8]]
            k0 = kutu.get(mk)
            kutu[mk] = bx if k0 is None else [min(k0[0], bx[0]), max(k0[1], bx[1]), min(k0[2], bx[2]), max(k0[3], bx[3]), min(k0[4], bx[4]), max(k0[5], bx[5])]
    bos = {b_ for b_ in BOS_YER_TUTUCU if not PK["parca"].get(b_)}               # v3.7 · parçasız yer tutucular listeye girmez
    for b_ in PK.get("birim", {}):
        if b_ in bos: continue
        birim_v.setdefault(b_, mekanizma_bul(b_, None))
    # düğüm dünya dönüşümleri (ilk kare)
    ebeveyn = {}
    for i, n in enumerate(g["nodes"]):
        for c in n.get("children", []): ebeveyn[c] = i

    def dunya(i):
        R = np.eye(3); T = np.zeros(3); j = i
        zincir = []
        while j is not None:
            zincir.append(j); j = ebeveyn.get(j)
        for j in reversed(zincir):
            n = g["nodes"][j]
            r_ = _quat_mat(n["rotation"]) if "rotation" in n else np.eye(3)
            t_ = np.array(n.get("translation", [0, 0, 0]), float)
            T = R @ t_ + T; R = R @ r_
        return R, T
    dugum_mesh = {n["mesh"]: i for i, n in enumerate(g["nodes"]) if "mesh" in n}
    MEK, MI = [], {}

    def mi(k):
        if k not in MI: MI[k] = len(MEK); MEK.append(k)
        return MI[k]
    aralik, kapak, anahtarlar, ist = {}, {}, {}, dict(blok=0, sigan=0, sigmayan=0, dp=0, ucgen=0, ucgen_parca=0)
    ESN = 0.6                                                                     # mm tolerans (kutular 0,1 mm yuvarlak + float32)
    for mi_, mesh in enumerate(g["meshes"]):
        adi = mesh["name"]; birim = adi.split("__")[0]
        R, T = dunya(dugum_mesh[mi_]) if mi_ in dugum_mesh else (np.eye(3), np.zeros(3))
        for pi, prim in enumerate(mesh["primitives"]):
            mal = mats[prim["material"]]
            I = _dizi(g, bin_, prim["indices"]).astype(np.int64)
            P = _dizi(g, bin_, prim["attributes"]["POSITION"]).astype(np.float64)
            key = "%s#%d" % (g["nodes"][dugum_mesh[mi_]]["name"] if mi_ in dugum_mesh else adi, pi)       # düğüm adı # primitive sırası
            anahtarlar[key] = anahtarlar.get(key, 0) + 1
            nt = len(I) // 3; ist["ucgen"] += nt
            if birim in bos:                                                      # v3.7 · parçasız yer tutucu kutu: aralık yok (boş düğme yok)
                aralik[key] = []; ist["bos"] = ist.get("bos", 0) + nt; continue
            varsay = mekanizma_dugum(adi, mal)
            ub = {"TOPPING_DONER": "TOPPING_MODUL", "QR_DONER": "QR_GOZLER", "F_DONER": "F_YUKLEME_BANDI" if "_GB_" in adi else "F_TP10_KONVEYOR"}.get(birim, birim)
            parts = PK["parca"].get(ub, [])
            if not parts or nt == 0:
                aralik[key] = [mi(varsay), 0, len(I)]
                if (mal.endswith("__on_seffaf")) and nt: kapak[key] = [0, len(I)]
                continue
            T3 = I.reshape(-1, 3)
            vmin = T3.min(1); vmax = T3.max(1)
            pm = np.maximum.accumulate(vmax); sm = np.minimum.accumulate(vmin[::-1])[::-1]
            sinir = np.nonzero(pm[:-1] < sm[1:])[0] + 1                       # blok başları (köşe noktası aralığı ayrık)
            bas = np.concatenate([[0], sinir]); son = np.concatenate([sinir, [nt]])
            ist["blok"] += len(bas)
            box = np.array([p[2:8] for p in parts], float)                       # mm
            vol = np.maximum((box[:, 1] - box[:, 0]) * (box[:, 3] - box[:, 2]) * (box[:, 5] - box[:, 4]), 1e-3)
            # dünya koordinatı adayları: düğüm zinciri · + E ofseti · ham
            secenek = [(R, T), (R, T + np.array([x_e / 1000.0, 0, 0])), (np.eye(3), np.zeros(3))]
            en_iyi = None
            for R_, T_ in secenek:
                W = (P @ R_.T + T_) * 1000.0
                tv = W[T3]                                                        # nt × 3 × 3
                tmin = tv.min(1); tmax = tv.max(1)
                bmin = np.minimum.reduceat(tmin, bas, axis=0); bmax = np.maximum.reduceat(tmax, bas, axis=0)
                fit = ((bmin[:, None, 0] >= box[None, :, 0] - ESN) & (bmax[:, None, 0] <= box[None, :, 1] + ESN) &
                       (bmin[:, None, 1] >= box[None, :, 2] - ESN) & (bmax[:, None, 1] <= box[None, :, 3] + ESN) &
                       (bmin[:, None, 2] >= box[None, :, 4] - ESN) & (bmax[:, None, 2] <= box[None, :, 5] + ESN))
                oran = fit.any(1).mean()
                if en_iyi is None or oran > en_iyi[0] + 1e-9: en_iyi = (oran, fit)
                if oran > 0.999: break
            fit = en_iyi[1]
            nb = len(bas)
            # sıralı (monoton) atama: blok j → parça k, k azalmaz · maliyet = log hacim (küçük kutu öncelikli)
            kol = np.nonzero(fit.any(0))[0]
            sec = np.full(nb, -1)
            if len(kol):
                F = fit[:, kol]; C = np.where(F, np.log(vol[kol])[None, :], np.inf)
                dp = np.full(len(kol), 0.0); geri = np.zeros((nb, len(kol)), np.int32); ar = np.arange(len(kol))
                ok = True
                for j in range(nb):
                    pmv = np.minimum.accumulate(dp)                                # önek minimumu (k' <= k)
                    am = np.maximum.accumulate(np.where(dp <= pmv, ar, 0))          # önek argmin
                    if not F[j].any():
                        geri[j] = am; dp = pmv.copy(); continue                   # sığmayan blok: geç (varsayılana gider)
                    dp = pmv + C[j]; geri[j] = am
                if np.isfinite(dp).any():
                    k = int(np.argmin(dp)); ist["dp"] += 1
                    for j in range(nb - 1, -1, -1):
                        if F[j].any(): sec[j] = kol[k]
                        k = int(geri[j][k])
                else:
                    ok = False
                if not ok:
                    for j in range(nb):
                        c = np.nonzero(fit[j])[0]
                        if len(c): sec[j] = c[np.argmin(vol[c])]
            out, kp = [], []
            for j in range(nb):
                s0, cnt = int(bas[j]) * 3, int(son[j] - bas[j]) * 3
                if sec[j] >= 0:
                    p = parts[sec[j]]; mk = mekanizma_bul(ub, p[0], mal); ist["sigan"] += 1; ist["ucgen_parca"] += cnt // 3
                    kk = kapak_mi(ub, p[0], p[1]) or mal.endswith("__on_seffaf")
                else:
                    mk = varsay; ist["sigmayan"] += 1; kk = mal.endswith("__on_seffaf")
                c = mi(mk)
                if out and out[-3] == c and out[-2] + out[-1] == s0: out[-1] += cnt
                else: out.extend([c, s0, cnt])
                if kk:
                    if kp and kp[-2] + kp[-1] == s0: kp[-1] += cnt
                    else: kp.extend([s0, cnt])
            aralik[key] = out
            if kp: kapak[key] = kp
    cak = [k for k, v in anahtarlar.items() if v > 1]
    for k in cak: aralik.pop(k, None); kapak.pop(k, None)                         # çakışan anahtar: sayfa birim varsayılanına düşer
    kullanilan = {MEK[v[i]] for v in aralik.values() for i in range(0, len(v), 3)} | set(parca.values())     # v3.7 · yalnız üçgen / parça alan mekanizma (boş düğme yok)
    birim_v = {b_: v_ for b_, v_ in birim_v.items() if v_ in kullanilan}
    sira = sorted(kullanilan, key=lambda k: (IST_SIRA.get(istasyon_of(k), 99), k.endswith("/Gövde"), k))
    yeni = {k: i for i, k in enumerate(sira)}
    for k, v in aralik.items():
        for i in range(0, len(v), 3): v[i] = yeni[MEK[v[i]]]
    D = dict(surum="mekanizma_v3 · yap_mek_v1", glb=os.path.basename(glb_yol),
             istasyon=[dict(kod=k, ad=a, modul=m) for k, a, m in ISTASYON],
             liste=[dict(kod=k, istasyon=istasyon_of(k), ad=k.split("/", 1)[1]) for k in sira],
             parca=parca, birim=birim_v, aralik=aralik, kapak=kapak,
             kutu={k: [round(v_, 4) for v_ in b] for k, b in kutu.items()},
             kapsam=dict(parca=say["toplam"], mekanizmada=say["ozel"], govde=say["govde"], kapak=say["kapak"],
                         oran=round(100.0 * say["ozel"] / max(1, say["toplam"]), 1),
                         ucgen=ist["ucgen"], ucgen_parcaya_bagli=ist["ucgen_parca"], blok=ist["blok"], blok_sigmayan=ist["sigmayan"], cakisan_anahtar=len(cak),
                         bos_yer_tutucu=sorted(bos), bos_yer_tutucu_ucgen=ist.get("bos", 0)))
    io.open(cikis, "w", encoding="utf-8").write(json.dumps(D, ensure_ascii=False, separators=(",", ":")))
    return D


if __name__ == "__main__":
    if len(sys.argv) >= 4:
        D = tablo_yaz(sys.argv[1], sys.argv[2], sys.argv[3])
        print(json.dumps(D["kapsam"], ensure_ascii=False))
        print("%d mekanizma: %s" % (len(D["liste"]), ", ".join(m["kod"] for m in D["liste"])))
    else:
        print(__doc__)
