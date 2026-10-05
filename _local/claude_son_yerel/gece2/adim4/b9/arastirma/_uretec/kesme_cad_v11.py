# -*- coding: utf-8 -*-
"""AUTOKITCH · K · KESME + SIVI YAĞ SPREYİ · K400 — ÜRETİM MODELİ v11 (30 Eyl 2026 · Claude)
Kemal (30 Eyl, alt dolap ekran görüntüsü): "bunu geriye en gidebileceği kadar it ki ben ön tarafa da bir şeyler koyabileyim"
TEMEL: kesme_cad_v10 AYNEN (kesme · sprey · nozül · pano · teneke / tartı / pompa / hortum parçaları ve katalog değerleri) — yalnız ALT DOLAP YERLEŞİMİ değişir.

v10 → v11 · TENEKE ARKADA · POMPA GRUBU RAFTA · ÖN BOŞ
 · teneke + tartı + damlama tavası 452 mm GERİ: teneke z −769,5…−534,5 · tartı platformu −782…−522 · tava −784…−500
   (arka alt kayıt z −785'te — tava ona 1 mm; daha geri gidemez: kayıt tava ve tartı yüksekliğinde boydan boya)
 · teneke ağzı ÖN-SAĞ köşede (x 285 · z −562): emme borusu + adaptör rafın ÖNÜNDE kalır → teneke öne çekilirken rafa / hortuma değmez
 · pompa grubu (10 µm filtre · GJ-N21 · T · PM1704 · KBP) tenekenin ÜSTÜNE, arkada: 304 1,5 raf y 640 · z −785…−623 · 20 mm kıvrık kenar
   (rafın kendisi pompa grubunun damlama tavası) · 2 × L 30 × 30 × 3 köşebent yan saclara + arka köşe dikmelerine · PM1704 T'nin ÜSTÜNE dik
   (v10'daki gibi öne uzansaydı basınç hattının yolunu kapatırdı) · basınç hattı T'nin önünden taban rakoruna (x 380 · z −600) → nozüle (v10 yolu)
 · ÖN BOŞLUK: z −500 … +27 (ön köşe dikmeleri) ≈ 527 mm derin × x 35…365 × y 156…862 (kapak içi) — eşya konabilir
 · teneke değişimi: kapak açılır, öndeki eşya alınır, teneke emme borusuyla birlikte öne çekilir (emiş / dönüş hortumu CPC çabuk bağlantılı)
KOORDİNAT: v8/v9/v10 ile aynı — x 0…400 (hatta 4000 + x), y yerden, z 0 ön yüz … −830 arka."""
import math
import cadquery as cq
import kesme_cad_v10 as K10
from kesme_cad_v10 import *                     # v10 (ve v9/v8) sabitleri, yardımcıları, PARCALAR, zaman ve denetim işlevleri

# ---------------------------------------------------------------- v11 sabitleri ----------------------------------------------------------------
DZ_T = -452.0                                                                             # teneke + tartı + tava geri kaydırma (v10'a göre)
ARKA_KAYIT_ON = -785.0                                                                    # arka alt kayıt (onyuz_kayit_140_-800) ön yüzü · y 126–156 boydan boya
RAF = dict(x=(4.5, 395.5), y=640.0, t=1.5, z=(-785.0, -623.0), kenar=20.0)               # pompa rafı 304 1,5 (üst yüz 641,5)
KB = dict(y=(610.0, 640.0), z=(-785.0, -620.0), t=3.0)                                    # L 30 × 30 × 3 köşebent (yan sac iç yüzü x 1,5 / 398,5)
DY_P, DZ_P = RAF["y"] + RAF["t"] - 127.0, -225.0                                          # pompa grubu ötelemesi (v10 plakası y 127, z −560…−400)
SENSOR_Y1 = 111.0                                                                          # PM1704 boyu (T üst yüzünden yukarı)


def _t(v, dz):
    return tuple(v[:4]) + (v[4] + dz, v[5] + dz)


TNK = dict(x=(82.5, 317.5), z=(-317.5 + DZ_T, -82.5 + DZ_T), y0=199.0)                   # −769,5 … −534,5
TNK_AGIZ = (285.0, TNK["z"][1] - 27.5)                                                    # ön-sağ köşe (v10: arka-sağ) → z −562
TARTI = dict(taban=_t(K10.TARTI["taban"], DZ_T), hucre=_t(K10.TARTI["hucre"], DZ_T), takoz_h=K10.TARTI["takoz_h"], plat=_t(K10.TARTI["plat"], DZ_T))
TAVA10 = (38.0, 362.0, 126.0, 146.0, ARKA_KAYIT_ON + 1.0, -500.0)                         # tartı + teneke altı (pompa grubu artık rafta)
POMPA_Y, POMPA_Z = K10.POMPA_Y + DY_P, K10.POMPA_Z + DZ_P                                # 688,7 · −705
_pg = K10.PG
PG = dict(plaka=(_pg["plaka"][0], _pg["plaka"][1], _pg["plaka"][2] + DY_P, _pg["plaka"][3] + DY_P, _pg["plaka"][4] + DZ_P, _pg["plaka"][5] + DZ_P),
          filtre=(_pg["filtre"][0], _pg["filtre"][1], _pg["filtre"][2] + DY_P, _pg["filtre"][3] + DY_P),
          pompa=(_pg["pompa"][0], _pg["pompa"][1], _pg["pompa"][2] + DY_P, _pg["pompa"][3] + DY_P, _pg["pompa"][4] + DZ_P, _pg["pompa"][5] + DZ_P),
          t=(_pg["t"][0], _pg["t"][1], _pg["t"][2] + DY_P, _pg["t"][3] + DY_P, _pg["t"][4] + DZ_P, _pg["t"][5] + DZ_P),
          sensor=(_pg["sensor"][0], _pg["sensor"][1], _pg["t"][4] + DZ_P - 1.0, _pg["t"][4] + DZ_P),   # v10 yatay çağrısı için yer tutucu — modul()'de DİK yapılır
          bpr=(_pg["bpr"][0], _pg["bpr"][1], _pg["bpr"][2] + DY_P, _pg["bpr"][3] + DY_P))
_T_ON = PG["t"][5]                                                                         # T'nin ön yüzü (−695) → basınç hattı buradan
Y_UST_HAT = 830.0                                                                          # emiş hattının raf üstü geçişi (arka üst kayıt 862'nin altı)
Y_DONUS = 820.0                                                                            # KBP üstünden ≥ R 50 + boru r 4 + 1 (ilk dirsek küresi KBP'ye girmesin)
H_BASINC = [(225.0, POMPA_Y, _T_ON), (225.0, POMPA_Y, -600.0), (380.0, POMPA_Y, -600.0), (380.0, Y_HORTUM, -600.0), (X_NZ, Y_HORTUM, -600.0), (X_NZ, Y_HORTUM, Z_NZ - 22.0)]
H_EMIS = [(LANS["port"][0][0], None, TNK_AGIZ[1]), (LANS["port"][0][0], Y_UST_HAT, TNK_AGIZ[1]), (PG["filtre"][0], Y_UST_HAT, TNK_AGIZ[1]),
          (PG["filtre"][0], Y_UST_HAT, POMPA_Z), (PG["filtre"][0], PG["filtre"][3], POMPA_Z)]
H_DONUS = [(PG["bpr"][0], PG["bpr"][3], POMPA_Z), (PG["bpr"][0], Y_DONUS, POMPA_Z), (PG["bpr"][0], Y_DONUS, TNK_AGIZ[1]), (LANS["port"][1][0], None, TNK_AGIZ[1])]
_boy = K10._boy
V11_YENI, V11_DEGISEN = [], []

# v10 işlevleri kendi modül değişkenlerini okur → v11 değerleri oraya da yazılır (tek kaynak bu dosya)
for _ad in ("TNK", "TNK_AGIZ", "TARTI", "TAVA10", "POMPA_Y", "POMPA_Z", "PG", "H_BASINC", "H_EMIS", "H_DONUS"):
    setattr(K10, _ad, globals()[_ad])


def ekle11(ad, wp, mal="sac", grup="SABIT", bom=None):
    ekle8(ad, wp, mal, grup, bom)
    V11_YENI.append(ad)


def raf_v11():
    """pompa rafı (kendi damlama tavası) + 2 köşebent"""
    x0, x1 = RAF["x"]; z0, z1 = RAF["z"]; y0 = RAF["y"]; t = RAF["t"]; k = RAF["kenar"]
    raf = kut(x0, x1, y0, y0 + t, z0, z1)
    raf = raf.union(kut(x0, x1, y0 + t, y0 + t + k, z1 - t, z1))                          # ön kıvrım
    raf = raf.union(kut(x0, x0 + t, y0 + t, y0 + t + k, z0, z1 - t)).union(kut(x1 - t, x1, y0 + t, y0 + t + k, z0, z1 - t))   # yan kıvrımlar
    ekle11("yag_pompa_rafi", raf, "sac", "SABIT",
           bom=("Pompa rafı AISI 304 1,5 (3 kenarı 20 kıvrık · köşeler kaynaklı = pompa grubunun damlama tavası)", 1,
                "%.0f × %.0f · üst yüz y %.1f · arka kenarı köşe dikmelerine dayalı · 2 köşebende 4 × M5" % (x1 - x0, z1 - z0, y0 + t), "v11 · üretim", "ÜRETİM"))
    ya, yb = KB["y"]; za, zb = KB["z"]; kt = KB["t"]
    for ad_, xs, xl in (("sol", 1.5, (1.5 + kt, 31.5)), ("sag", 398.5 - kt, (368.5, 398.5 - kt))):
        kb = kut(xs, xs + kt, ya, yb, za, zb).union(kut(xl[0], xl[1], yb - kt, yb, za, zb))
        ekle11("yag_pompa_rafi_kosebendi_" + ad_, kb, "celik", "SABIT",
               bom=("Köşebent L 30 × 30 × 3 AISI 304 (raf taşıyıcı)", 2, "boy %.0f · yan saca 3 × M5 perçin somun + arka köşe dikmesine 1 × M5" % (zb - za), "v11 · üretim", "ÜRETİM")
               if ad_ == "sol" else None)


def sensor_v11():
    """PM1704 T'nin üstüne DİK (v10'da T'den öne 111 mm uzanıyordu → basınç hattının yolu)"""
    p = bul("yag_basinc_sensoru_PM1704")
    sx, sr = PG["sensor"][0], PG["sensor"][1]
    y0 = PG["t"][3]
    p["wp"] = sily(sx, POMPA_Z, sr, y0, y0 + SENSOR_Y1)
    b = list(p["bom"]); b[2] = b[2] + " · v11: T'nin üstünde dik"; p["bom"] = tuple(b)
    V11_DEGISEN.append(p["ad"])


def bom_v11():
    for ad_, eski, yeni in (("yag_damlama_tavasi_10", "teneke + tartı + pompa grubu altı", "teneke + tartı altı · v11: arkada"),
                            ("yag_pompa_plakasi", "tavaya 4 × M5 (lastik)", "rafa 4 × M5 (lastik) · v11")):
        p = bul(ad_); b = list(p["bom"]); b[0] = b[0].replace(eski, yeni); b[2] = b[2].replace(eski, yeni); p["bom"] = tuple(b)
        V11_DEGISEN.append(ad_)
    p = bul("yag_tenekesi_18L"); b = list(p["bom"]); b[2] = b[2] + " · v11: dolabın ARKASINDA, ağız ön-sağda (öne çekilerek değişir)"; p["bom"] = tuple(b)
    V11_DEGISEN.append(p["ad"])


def modul():
    K10.modul()
    raf_v11(); sensor_v11(); bom_v11()
    for ad_ in ("yag_damlama_tavasi_10", "yag_tarti_taban_plakasi", "yag_tarti_alt_takozu", "yag_tarti_yuk_hucresi_PW15AH", "yag_tarti_ust_takozu", "yag_tarti_platformu",
                "yag_tenekesi_18L", "yag_emme_lansi_1038304", "yag_agiz_adaptoru", "yag_pompa_plakasi", "yag_emis_filtresi", "yag_boru_filtre_pompa",
                "yag_pompasi_GJ-N21_EagleDrive", "yag_boru_pompa_T", "yag_T_parcasi", "yag_boru_T_regulator", "yag_geri_basinc_regulatoru_KBP",
                "yag_basinc_hortumu_TLM1008", "yag_emis_hortumu_TLM1008", "yag_donus_hortumu_TLM0806"):
        if ad_ not in V11_DEGISEN:
            V11_DEGISEN.append(ad_)
    return PARCALAR


def on_bosluk():
    """ön boşluk: alt dolaptaki (y 126…862) BÜTÜN parçaların — gövde dikme / kayıt / tabanı hariç — en ön noktası → ön köşe dikmeleri (z 27) ·
    kapak içi x 35…365 · y 156…862 (alt ve üst ön kayıt arası). Parça alt dolap kutusuyla kesilip ölçülür (basınç hattı yukarıda öne gider)."""
    kutu = kut(35.0, 365.0, 156.0, 862.0, -830.0, 27.0).val()
    zmax, en = -830.0, None
    for p in PARCALAR:
        if p["ad"].startswith(("kose_dikmesi", "onyuz_", "taban_sac", "arka_sac", "sol_sac", "sag_sac", "ust_sac", "istasyon_tabani", "plint", "ayak_")): continue
        sh = p["wp"].val()
        b = sh.BoundingBox()
        if b.ymax <= 156.0 or b.ymin >= 862.0 or b.xmax <= 35.0 or b.xmin >= 365.0: continue
        k = sh.intersect(kutu)
        if k.Volume() < 1e-3: continue
        z = k.BoundingBox().zmax
        if z > zmax: zmax, en = z, p["ad"]
    return dict(z_on=round(zmax, 1), en_ondeki=en, derinlik=round(27.0 - zmax, 1), x=(35.0, 365.0), y=(156.0, 862.0))
