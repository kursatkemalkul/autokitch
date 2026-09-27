# -*- coding: utf-8 -*-
"""AUTOKITCH · S · PERSONEL TEZGÂHI + DUVAR ASKISI · CAD v1 (27 Eyl 2026) — ALÇAK HAT v57 (SPEC_alcak_hat_v57.md · QR_TEZGAH_v4 resmi)
TEZGÂH 600 × 450 × 900 · dünya x 3950–4550 · z 1429–1879 (ön duvara yaslı, arka yüz z 1879) · y 0–900
  plint 0–100 (4 ayar ayağı + 50 geride süpürgelik) · gövde 100–870 (AISI 304 1,2 mm) · tabla 870–900 (her yandan 15 taşar, resimdeki gibi)
  içi (resim birebir): altta TEMİZLİK 2 × 5 L bidon 105–405 (damla tepsisinde) + sağ yarı boş · raf 412 (taşıyıcı 412–416,5, raf yüzü 418) ·
  rafta BEZ / ELDİVEN / POŞET kutusu 418–568 (önde solda) + ÇÖP 10 L kapaklı, poşetli 418–668 (arkada sağda) · en üstte KİLİTLİ KİŞİSEL
  ÇEKMECE 700–855 (bilyalı teleskopik ray) · tek ön kapak.
DUVAR ASKISI 1650'de, tezgâhın üstünde, basit: ray x 4000–4500 + 3 kanca (x 4070 · 4250 · 4430), duvardan 70 çıkar.
KOORDİNAT: parçalar YEREL kurulur (x 0…600 tezgâhın solundan, y yerden, z 0 = tezgâh ön yüzü … 450 = duvar) ve ekle()'de
  (X0, Y0, Z0) = (3950, 0, 1429) ile dünyaya taşınır. Ön yüz −z yönüne (hatta / ince duvara) bakar.
VARSAYIM: bidon 125 × 285 × 190 (+ kapak 15) · kutu/çöp ölçüleri resimden · ray 12,7 × 45 × 300 tam açılım · kam kilit Ø19 · ayak 100 ayarlı.
DENETÇİ DÜZELTMESİ (27 Eyl): çekmece stroku 350 → 300. 350'de açık çekmecenin kulpu (ön yüzden 23 çıkar) ince duvara 17 mm kalıyordu
  (denetim kulpu saymıyor, "pay 40" yazıyordu) · parmak sıkışma boşluğu ≥ 25 (ISO 13854, eski EN 349) → strok ≤ 342 → 50'lik ray adımında 300.
"""
import math, os, sys, time
import cadquery as cq

U = os.path.dirname(os.path.abspath(__file__)); KOK = os.path.dirname(os.path.dirname(U)); sys.path.insert(0, U)
import qr_cad_v1 as QR                    # ortak denetim + BOM yardımcıları (QR burada kurulmaz)

X0, Y0, Z0 = 3950.0, 0.0, 1429.0          # SPEC: x 3950–4550 · z 1429–1879
W, D, H = 600.0, 450.0, 900.0
T = 1.2                                   # gövde sacı AISI 304 1,2 mm
PLINT, GOVDE_UST, TABLA = 100.0, 870.0, 30.0
TASMA = 15.0                              # tabla taşması (resim: TX0 − 15 … TX0 + TW + 15)
RAF_Y = (412.0, 416.5, 418.0)             # taşıyıcı altı · raf altı · raf üstü
BIDON = dict(w=125.0, h=285.0, d=190.0, kapak=15.0, y0=105.0)   # VARSAYIM (SPEC: 190 × 125 × 285)
CEKMECE = dict(y=(700.0, 855.0), strok=300.0)                     # resim: 700–855 · strok ince duvara göre (kulp dahil, ISO 13854 parmak 25) · denetçi: 350 → 300
KULP_CIKINTI = 23.0                       # kulp() ön yüzden 23 çıkar
PARMAK_BOSLUK = 25.0                      # ISO 13854 (eski EN 349): parmak sıkışmasına karşı en az boşluk 25 mm
ASKI_Y = 1650.0
INCE_DUVAR_Z = (979.0, 1039.0)            # dükkân v13 / QR_TEZGAH v4 planı: ince duvar z 979–1039 (x 0–4570)

PARCALAR = []
MODUL = "S"
BIRIMLER = [
    ("TEZGAH_GOVDE", "Personel tezgâhı 600 × 450 × 900 · AISI 304 · x 3950–4550 · z 1429–1879 (ön duvara yaslı) · plint 100 · tabla 870–900 · raf 412 · tek kapak"),
    ("TEZGAH_CEKMECE", "Kilitli kişisel çekmece 700–855 · bilyalı teleskopik ray 300 (tam açılım) · kam kilit"),
    ("TEZGAH_TEMIZLIK", "Temizlik · 2 × 5 L bidon 105–405 · damla tepsisi"),
    ("TEZGAH_SARF", "Bez / eldiven / poşet kutusu 418–568 (3 bölmeli)"),
    ("TEZGAH_COP", "Çöp kovası 10 L · kapaklı · poşetli · 418–668"),
    ("TEZGAH_ASKI", "Duvar askısı · y 1650 · ray 500 + 3 kanca · duvardan 70"),
]
BIRIM_MODUL = {k: MODUL for k, _a in BIRIMLER}
ON_BIRIMLER = tuple(k for k, _a in BIRIMLER)     # hepsi hattın önünde (z > 0) · montajın ÖN YÜZ istisnasına "TEZGAH" öneki EKLENMELİ
MALZEME = {"paslanmaz": dict(renk=(0.80, 0.82, 0.84, 1.0), met=0.9, ruf=0.30), "celik": dict(renk=(0.60, 0.62, 0.66, 1.0), met=1.0, ruf=0.35),
           "plastik": dict(renk=(0.12, 0.12, 0.13, 1.0), met=0.0, ruf=0.6), "bidon": dict(renk=(0.20, 0.45, 0.80, 1.0), met=0.0, ruf=0.5),
           "bidon_kapak": dict(renk=(0.95, 0.80, 0.15, 1.0), met=0.0, ruf=0.5), "pp_gri": dict(renk=(0.55, 0.57, 0.60, 1.0), met=0.0, ruf=0.6),
           "cop_kova": dict(renk=(0.25, 0.27, 0.29, 1.0), met=0.0, ruf=0.55), "poset": dict(renk=(0.10, 0.10, 0.10, 1.0), met=0.0, ruf=0.4),
           "bez": dict(renk=(0.30, 0.55, 0.85, 1.0), met=0.0, ruf=0.9), "eldiven": dict(renk=(0.35, 0.35, 0.85, 1.0), met=0.0, ruf=0.7),
           "aluminyum": dict(renk=(0.86, 0.87, 0.89, 1.0), met=0.8, ruf=0.35)}
kut, sily, silz, silx = QR.kut, QR.sily, QR.silz, QR.silx


def ekle(ad, wp, mal, birim, bom=None, grup="SABIT", kaynak=""):
    """bom = (kalem, adet, tanım, kaynak/not, tür)"""
    assert all(p["ad"] != ad for p in PARCALAR), ad
    PARCALAR.append(dict(ad=ad, wp=wp.translate((X0, Y0, Z0)), mal=mal, birim=birim, grup=grup, kaynak=kaynak, bom=bom))


dunya = QR.dunya


def kulp(x0, x1, y0, y1):
    """çubuk kulp (ön yüzden 23 çıkar): çubuk + iki ayak tek katı"""
    return kut(x0, x1, y0, y1, -23.0, -15.0).union(kut(x0, x0 + 10.0, y0, y1, -15.0, 0.0)).union(kut(x1 - 10.0, x1, y0, y1, -15.0, 0.0))


# ---------------------------------------------------------------- GÖVDE ----------------------------------------------------------------
def govde():
    b = "TEZGAH_GOVDE"
    for i, (x, z) in enumerate(((40.0, 91.0), (560.0, 91.0), (40.0, 411.0), (560.0, 411.0))):
        ekle("ayar_ayagi_%d" % i, sily(x, z, 20.0, 0.0, 8.0).union(sily(x, z, 14.0, 8.0, PLINT)), "plastik", b,
             bom=("Mutfak dolabı ayar ayağı 100 mm (±15)", 4, "Ø40 taban", "VARSAYIM · katalog", "SATIN ALMA") if i == 0 else None)
    ekle("supurgelik", kut(2.0, W - 2.0, 3.0, PLINT - 3.0, 50.0, 62.0), "paslanmaz", b,
         bom=("Süpürgelik 12 mm (klipsli, 50 geride)", 1, "596 × 94", "üretim", "ÜRETİM"))
    ekle("yan_sol", kut(0.0, T, PLINT, GOVDE_UST, 0.0, D), "paslanmaz", b, bom=("Yan panel AISI 304 1,2 mm", 2, "450 × 770", "üretim (abkant)", "ÜRETİM"))
    ekle("yan_sag", kut(W - T, W, PLINT, GOVDE_UST, 0.0, D), "paslanmaz", b)
    ekle("taban", kut(T, W - T, PLINT, PLINT + T, 0.0, D - T), "paslanmaz", b, bom=("Taban AISI 304 1,2 mm", 1, "597,6 × 448,8", "üretim", "ÜRETİM"))
    ekle("arka_panel", kut(T, W - T, PLINT + T, GOVDE_UST, D - T, D), "paslanmaz", b, bom=("Arka panel AISI 304 1,2 mm (duvara)", 1, "597,6 × 768,8", "üretim", "ÜRETİM"))
    ekle("ust_on_kusak", kut(T, W - T, 857.0, GOVDE_UST, 0.0, 20.0), "paslanmaz", b)
    ekle("tabla_30", kut(-TASMA, W + TASMA, GOVDE_UST, GOVDE_UST + TABLA, -TASMA, D), "paslanmaz", b,
         bom=("Tezgâh tablası AISI 304 1,2 mm kaplı · 30 mm · ön + yan 15 taşar", 1, "630 × 465", "üretim · resim birebir", "ÜRETİM"))
    ekle("raf_tasiyici_sol", kut(T, T + 15.0, RAF_Y[0], RAF_Y[1], 20.0, 431.0), "paslanmaz", b, bom=("Raf taşıyıcı köşebent", 2, "411", "üretim", "ÜRETİM"))
    ekle("raf_tasiyici_sag", kut(W - T - 15.0, W - T, RAF_Y[0], RAF_Y[1], 20.0, 431.0), "paslanmaz", b)
    ekle("raf", kut(2.0, W - 2.0, RAF_Y[1], RAF_Y[2], 22.0, 441.0), "paslanmaz", b, bom=("Raf AISI 304 1,5 mm (bükümlü)", 1, "596 × 419", "üretim", "ÜRETİM"))
    ekle("on_kapak", kut(1.7, W - 1.7, 104.0, 694.0, 0.0, 18.0), "paslanmaz", b,
         bom=("Ön kapak 18 mm çift cidar AISI 304 (tek kanat, menteşe solda)", 1, "596,6 × 590", "üretim · SPEC 'tek kapak'", "ÜRETİM"))
    for i, y in enumerate((150.0, 600.0)):
        ekle("kapak_mentesesi_%d" % i, kut(T, T + 15.0, y, y + 40.0, 18.0, 38.0), "celik", b,
             bom=("Gizli menteşe 110° (kapak)", 2, "", "VARSAYIM · katalog", "SATIN ALMA") if i == 0 else None)
    ekle("kapak_kulpu", kulp(430.0, 570.0, 655.0, 670.0), "celik", b, bom=("Çubuk kulp 140 mm paslanmaz", 2, "kapak + çekmece", "katalog", "SATIN ALMA"))


def cekmece():
    b = "TEZGAH_CEKMECE"
    y0, y1 = CEKMECE["y"]; s = CEKMECE["strok"]
    ekle("cekmece_onu", kut(1.7, W - 1.7, y0, y1, 0.0, 18.0).cut(silz(300.0, 830.0, 9.75, -1.0, 19.0)), "paslanmaz", b,
         bom=("Çekmece önü 18 mm çift cidar AISI 304", 1, "596,6 × 155", "üretim", "ÜRETİM"))
    ekle("cekmece_kulpu", kulp(230.0, 370.0, 745.0, 760.0), "celik", b)
    ekle("kam_kilit_silindiri", silz(300.0, 830.0, 9.5, -2.0, 21.0), "celik", b, bom=("Kam kilit Ø19 (anahtarlı, 2 anahtar)", 1, "kam ön kuşağın arkasına kilitler", "VARSAYIM · katalog", "SATIN ALMA"))
    ekle("kam_kilit_dili", kut(292.0, 308.0, 830.0, 866.0, 21.0, 24.0), "celik", b)
    for ad_, (xa, xb) in (("sol", (T, T + 12.7)), ("sag", (W - T - 12.7, W - T))):
        ekle("teleskopik_ray_%s" % ad_, kut(xa, xb, 740.0, 785.0, 20.0, 20.0 + s), "celik", b,
             bom=("Bilyalı teleskopik ray 12,7 × 45 · %.0f tam açılım (çift)" % s, 1, "yan montaj", "Accuride DZ3832 sınıfı · boy VARSAYIM", "SATIN ALMA") if ad_ == "sol" else None)
    xa, xb = T + 12.7 + 1.0, W - T - 12.7 - 1.0
    ekle("cekmece_kutu_tabani", kut(xa, xb, 712.0, 712.0 + T, 18.0, 18.0 + s), "paslanmaz", b,
         bom=("Çekmece kutusu AISI 304 1,2 mm (taban + yanlar + arka)", 1, "%.0f × %.0f × 128" % (xb - xa, s), "üretim", "ÜRETİM"))
    ekle("cekmece_kutu_yan_sol", kut(xa, xa + T, 712.0 + T, 840.0, 18.0, 18.0 + s), "paslanmaz", b)
    ekle("cekmece_kutu_yan_sag", kut(xb - T, xb, 712.0 + T, 840.0, 18.0, 18.0 + s), "paslanmaz", b)
    ekle("cekmece_kutu_arka", kut(xa + T, xb - T, 712.0 + T, 840.0, 18.0 + s - T, 18.0 + s), "paslanmaz", b)


def icerik():
    ekle("damla_tepsisi", kut(22.0, 312.0, PLINT + T, BIDON["y0"], 25.0, 225.0), "pp_gri", "TEZGAH_TEMIZLIK",
         bom=("Damla tepsisi PP (kimyasal sızıntısı)", 1, "290 × 200 × 3,8", "VARSAYIM", "SATIN ALMA"))
    for i, x in enumerate((29.0, 167.0)):
        yb = BIDON["y0"] + BIDON["h"]
        ekle("temizlik_bidonu_%d" % i, kut(x, x + BIDON["w"], BIDON["y0"], yb, 30.0, 30.0 + BIDON["d"]), "bidon", "TEZGAH_TEMIZLIK",
             bom=("Temizlik kimyasalı 5 L bidon (yüzey temizleyici + dezenfektan)", 2, "125 × 285 × 190 + kapak", "tedarikçi bidonu · ölçü VARSAYIM", "SATIN ALMA") if i == 0 else None)
        ekle("temizlik_bidonu_kapagi_%d" % i, sily(x + BIDON["w"] / 2.0, 60.0, 19.0, yb, yb + BIDON["kapak"]), "bidon_kapak", "TEZGAH_TEMIZLIK")
    b = "TEZGAH_SARF"
    ekle("sarf_kutusu", kut(25.0, 283.0, RAF_Y[2], 568.0, 30.0, 230.0).cut(kut(27.0, 281.0, RAF_Y[2] + 2.0, 569.0, 32.0, 228.0)), "pp_gri", b,
         bom=("Saklama kutusu 3 bölmeli (bez · eldiven · poşet)", 1, "258 × 150 × 200", "VARSAYIM · resim ölçüsü", "SATIN ALMA"))
    for i, x in enumerate((111.0, 197.0)):
        ekle("sarf_kutusu_bolme_%d" % i, kut(x, x + 2.0, RAF_Y[2] + 2.0, 568.0, 32.0, 228.0), "pp_gri", b)
    ekle("bez_yigini", kut(30.0, 108.0, RAF_Y[2] + 2.0, RAF_Y[2] + 72.0, 36.0, 224.0), "bez", b)
    ekle("eldiven_kutusu", kut(116.0, 194.0, RAF_Y[2] + 2.0, RAF_Y[2] + 92.0, 36.0, 224.0), "eldiven", b,
         bom=("Tek kullanımlık eldiven kutusu", 1, "sarf", "—", "SATIN ALMA"))
    ekle("poset_rulosu", silz(240.0, RAF_Y[2] + 2.0 + 35.0, 35.0, 40.0, 220.0), "poset", b)
    b = "TEZGAH_COP"
    ekle("cop_kovasi_10L", kut(300.0, 520.0, RAF_Y[2], 653.0, 240.0, 440.0).cut(kut(302.0, 518.0, RAF_Y[2] + 2.0, 654.0, 242.0, 438.0)), "cop_kova", b,
         bom=("Çöp kovası 10 L kapaklı (çekip açılır)", 1, "220 × 250 × 200", "VARSAYIM · resim ölçüsü", "SATIN ALMA"))
    ekle("cop_kovasi_kapagi", kut(300.0, 520.0, 653.0, 668.0, 240.0, 440.0), "cop_kova", b)       # resim: TX0 + 300 … 520
    ekle("cop_poseti", kut(303.0, 517.0, RAF_Y[2] + 3.0, 653.0, 243.0, 437.0).cut(kut(303.4, 516.6, RAF_Y[2] + 3.4, 654.0, 243.4, 436.6)), "poset", b,
         bom=("Çöp poşeti 10 L", 1, "sarf", "—", "SATIN ALMA"))


def aski():
    b = "TEZGAH_ASKI"
    ekle("aski_rayi", kut(50.0, 550.0, ASKI_Y - 10.0, ASKI_Y + 10.0, D - 10.0, D), "aluminyum", b,
         bom=("Duvar askısı rayı alüminyum 20 × 10 (2 dübel)", 1, "500", "üretim · resim birebir", "ÜRETİM"))
    for i, x in enumerate((120.0, 300.0, 480.0)):
        k = kut(x - 6.0, x + 6.0, ASKI_Y - 50.0, ASKI_Y - 10.0, D - 7.0, D)
        k = k.union(silz(x, ASKI_Y - 44.0, 5.0, D - 63.0, D - 7.0)).union(sily(x, D - 63.0, 5.0, ASKI_Y - 44.0, ASKI_Y - 20.0))
        k = k.union(cq.Workplane(obj=cq.Solid.makeSphere(7.0, cq.Vector(x, ASKI_Y - 20.0, D - 63.0), angleDegrees1=-90, angleDegrees2=90)))   # uç topuzu duvardan 70
        ekle("aski_kancasi_%d" % i, k, "paslanmaz", b, bom=("Askı kancası Ø10 paslanmaz (J)", 3, "duvardan 70", "üretim", "ÜRETİM") if i == 0 else None)


def kur():
    PARCALAR[:] = []
    govde(); cekmece(); icerik(); aski()
    return PARCALAR


BOM_KLASOR = os.path.join(KOK, "arastirma", "7_TEZGAH_v1")
DEN = []


def kontrol(ad, sart, deger=""):
    DEN.append((ad, bool(sart), deger)); print("  %-100s %s %s" % (ad, "GEÇTİ" if sart else "** KALDI **", deger))


if __name__ == "__main__":
    t0 = time.time(); arg = sys.argv[1:]
    ps = kur()
    gec = [p["ad"] for p in ps if not dunya(p).isValid()]
    print("TEZGÂH v1 · %d parça · katı denetimi: %s · %.0f sn" % (len(ps), "hepsi geçerli" if not gec else gec, time.time() - t0))
    for kod, _a in BIRIMLER:
        q = [dunya(p).BoundingBox() for p in ps if p["birim"] == kod]
        print("   %-16s %2d parça · x %.1f–%.1f · y %.1f–%.1f · z %.1f–%.1f" % (kod, len(q), min(v.xmin for v in q), max(v.xmax for v in q), min(v.ymin for v in q), max(v.ymax for v in q), min(v.zmin for v in q), max(v.zmax for v in q)))
    print("DENETİM (tezgah_cad_v1)")
    kontrol("katılar geçerli", not gec, ", ".join(gec))
    g = [dunya(p).BoundingBox() for p in ps if p["birim"] in ("TEZGAH_GOVDE", "TEZGAH_CEKMECE") and not p["ad"].startswith(("tabla", "kapak_kulpu", "cekmece_kulpu", "kam_kilit_sil"))]
    kontrol("gövde zarfı x %.0f–%.0f · y %.0f–%.0f · z %.0f–%.0f (SPEC 3950–4550 · 0–900 · 1429–1879; tabla taşması + kulplar hariç)"
            % (min(v.xmin for v in g), max(v.xmax for v in g), min(v.ymin for v in g), max(v.ymax for v in g), min(v.zmin for v in g), max(v.zmax for v in g)),
            abs(min(v.xmin for v in g) - 3950) < 0.01 and abs(max(v.xmax for v in g) - 4550) < 0.01 and abs(min(v.zmin for v in g) - 1429) < 0.01 and abs(max(v.zmax for v in g) - 1879) < 0.01)
    tb = [dunya(p).BoundingBox() for p in ps if p["ad"] == "tabla_30"][0]
    kontrol("tabla 870–900 · x %.0f–%.0f · z %.0f–%.0f" % (tb.xmin, tb.xmax, tb.zmin, tb.zmax), abs(tb.ymin - 870) < 0.01 and abs(tb.ymax - 900) < 0.01)
    by = lambda ad: [dunya(p).BoundingBox() for p in ps if p["ad"] == ad][0]
    kontrol("kotlar: bidon %.0f–%.0f · raf %.0f (yüz %.0f) · sarf %.0f–%.0f · çöp %.0f–%.0f · çekmece %.0f–%.0f (resim 105–405 · 412 · 418–568 · 418–668 · 700–855)"
            % (by("temizlik_bidonu_0").ymin, by("temizlik_bidonu_kapagi_0").ymax, by("raf_tasiyici_sol").ymin, by("raf").ymax, by("sarf_kutusu").ymin, by("sarf_kutusu").ymax,
               by("cop_kovasi_10L").ymin, by("cop_kovasi_kapagi").ymax, by("cekmece_onu").ymin, by("cekmece_onu").ymax),
            abs(by("temizlik_bidonu_0").ymin - 105) < 0.01 and abs(by("temizlik_bidonu_kapagi_0").ymax - 405) < 0.01 and abs(by("raf_tasiyici_sol").ymin - 412) < 0.01
            and abs(by("sarf_kutusu").ymax - 568) < 0.01 and abs(by("cop_kovasi_kapagi").ymax - 668) < 0.01 and abs(by("cekmece_onu").ymin - 700) < 0.01 and abs(by("cekmece_onu").ymax - 855) < 0.01)
    v_cop = 216.0 * (653.0 - RAF_Y[2] - 2.0) * 196.0 / 1e6
    kontrol("çöp kovası iç hacmi %.1f L ≥ 9,5 (10 L)" % v_cop, v_cop >= 9.5)
    v_b = BIDON["w"] * BIDON["h"] * BIDON["d"] / 1e6
    kontrol("bidon zarfı %.1f L ≥ 5 L (VARSAYIM ölçü)" % v_b, v_b >= 5.0)
    print("  UYARI: çöp kapağı ile çekmece kutusu altı arası %.0f mm → kapak yerinde açılmaz, kova öne çekilip açılır (VARSAYIM kullanım)" % (712.0 - 668.0))
    koridor = Z0 - INCE_DUVAR_Z[1]
    ck = [dunya(p).BoundingBox() for p in ps if p["birim"] == "TEZGAH_CEKMECE"]
    acik = min(v.zmin for v in ck) - CEKMECE["strok"]          # ölçülen: kulp dahil en ön nokta, strok kadar açık
    kontrol("çekmece tam açık (strok %.0f) kulp dahil en önü z %.0f − ince duvar %.0f = %.0f ≥ parmak boşluğu %.0f (ISO 13854)"
            % (CEKMECE["strok"], acik, INCE_DUVAR_Z[1], acik - INCE_DUVAR_Z[1], PARMAK_BOSLUK), acik - INCE_DUVAR_Z[1] >= PARMAK_BOSLUK)
    kontrol("çekmece kulp çıkıntısı ölçüsü %.0f = KULP_CIKINTI %.0f" % (Z0 - min(v.zmin for v in ck), KULP_CIKINTI), abs(Z0 - min(v.zmin for v in ck) - KULP_CIKINTI) < 0.01)
    kg = W - 2 * 1.7
    print("  UYARI: tezgâh önü ile ince duvar (z %.0f) arası %.0f mm → kapak (%.0f) en çok %.0f° açılır (tam açılım için ≥ %.0f; iki kanat 2 × %.0f tam açılır) · çalışma aralığı dar (≥ 900 önerilir) — Kemal'e sor"
          % (INCE_DUVAR_Z[1], koridor, kg, math.degrees(math.asin(min(1.0, koridor / kg))), kg, kg / 2.0))
    ay = [dunya(p).BoundingBox() for p in ps if p["birim"] == "TEZGAH_ASKI"]
    kontrol("duvar askısı ray ekseni y %.0f · kancalar duvardan %.0f çıkar · x %.0f–%.0f (resim 1650 · 70)" % ((min(v.ymin for v in ay[:1]) + max(v.ymax for v in ay[:1])) / 2.0, Z0 + D - min(v.zmin for v in ay), min(v.xmin for v in ay), max(v.xmax for v in ay)),
            abs((ay[0].ymin + ay[0].ymax) / 2.0 - ASKI_Y) < 0.01 and abs(Z0 + D - min(v.zmin for v in ay) - 70.0) < 0.5)
    kontrol("QR dolabıyla arası: tabla x %.0f < QR x %.0f · z aralıkları ayrı (tezgâh ≥ %.0f · QR ≤ %.0f)" % (tb.xmax, QR.X0, Z0 - 23.0, QR.Z0 + QR.D), tb.xmax < QR.X0 and Z0 - 23.0 > QR.Z0 + QR.D)
    cak = QR.kendi_arasinda(ps, istisna=lambda a, c: False)
    print("KENDİ ARASINDA (> 1 mm³): %s" % ("TEMİZ" if not cak else cak[:20]))
    kontrol("kendi arasında çakışma = 0 (%d parça)" % len(ps), not cak, str(len(cak)))
    if "bom" in arg:
        QR.bom_yaz(BOM_KLASOR, ps)
    kal = [d_ for d_ in DEN if not d_[1]]
    print("DENETIM: %d madde · %d KALDI · toplam %.0f sn" % (len(DEN), len(kal), time.time() - t0))
    assert not kal
    sys.stdout.flush(); os._exit(0)
