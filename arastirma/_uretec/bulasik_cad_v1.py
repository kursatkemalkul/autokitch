# -*- coding: utf-8 -*-
"""AUTOKITCH · F taban dolabı · BULAŞIK MAKİNESİ · MEIKO M-iClean US · CAD v1 (27 Eyl 2026)
Kemal: "bulaşık makinesi nerede modellediğin · neden detaylı modellemedin · yap".
Kaynak: MEIKO M-iClean US teknik föyü (meiko.us, 8-15-21, sayfa 1-2) + meiko.com M-iClean U teknik veri:
  gövde 460 × 600 (derin) × 700 (AB; ABD föyünde 730 ayaklı) · ayar ayakları ±12 · kapak ağzı 315, yerden 275 ·
  kapak alttan menteşeli, açıkken toplam 1050 (önde 450) · sepet 400 × 400 · arka bağlantılar soldan: elektrik 40,
  tahliye (D) 186, su (W) 313 · yerden: tahliye 165, su 95 · arkada duvar payı 25 · dokunmatik ekran + ışıklı kulp kapağın üstünde ·
  M-iClean filtre ve elle temizlenen parçalar mavi (Blue Touch) · 70 kg.
VARSAYIM (föyde yok): çift cidar kalınlığı, iç hazne sınırları, yıkama kolu boyu/kotu, sepet yüksekliği 100, ekran/kulp boyu.
Koordinat: yerel x 0…460 (soldan sağa), y 0…700 (yerden), z 0 (ön yüz) … −600 (arka) · dünyada (X0, Y0, Z0) = (2540, 130, −20)
(F taban dolabı, önde sol · montaj v52'deki D_BULASIK yeri)."""
import math, os, sys
import cadquery as cq

X0, Y0, Z0 = 2540.0, 130.0, -20.0
W, D, H = 460.0, 600.0, 700.0
AYAK_H = 10.0
KAPI = dict(y0=245.0, y1=700.0, t=22.0)                 # kapak: menteşe y 245, boy 455 → açık 455 ≈ föy 450
AGIZ = dict(y0=275.0, h=315.0)                          # föy: kapak ağzı 315, yerden 275
HAZNE = dict(x0=25.0, x1=435.0, y0=245.0, y1=630.0, z1=-575.0)   # VARSAYIM: çift cidar 25
SEPET = dict(a=400.0, y0=280.0, h=100.0, z0=-98.0)      # föy: 400 × 400 · yükseklik VARSAYIM
BAG = dict(elektrik=(40.0, 60.0, 7.0), tahliye=(186.0, 165.0, 15.0), su=(313.0, 95.0, 10.0))   # (soldan x, yerden y, yarıçap)

PARCALAR = []
BIRIMLER = [("D_BULASIK", "Bulaşık makinesi · MEIKO M-iClean US (GERÇEK MODEL v1, föy ölçüleri) · 460 × 600 × 700 · kapak alttan menteşeli, açık 1050 (önde 450) · ağız 315 (yerden 275) · sepet 400 × 400 · dokunmatik ekran + ışıklı kulp · M-iClean filtre · arka bağlantılar: elektrik 40 · tahliye 186/165 · su 313/95 · 70 kg")]
MALZEME = {"paslanmaz": dict(renk=(0.80, 0.82, 0.84, 1.0), met=0.9, ruf=0.30), "celik": dict(renk=(0.60, 0.62, 0.66, 1.0), met=1.0, ruf=0.35),
           "ekran_cam": dict(renk=(0.06, 0.07, 0.09, 1.0), met=0.3, ruf=0.10), "mavi_touch": dict(renk=(0.15, 0.42, 0.85, 1.0), met=0.0, ruf=0.45),
           "sepet_tel": dict(renk=(0.35, 0.37, 0.40, 1.0), met=0.2, ruf=0.55), "kulp_isik": dict(renk=(0.30, 0.75, 1.00, 1.0), met=0.0, ruf=0.30)}
KAYNAK = "MEIKO M-iClean US föyü (meiko.us 8-15-21)"


def kut(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), centered=False).translate((min(x0, x1), min(y0, y1), min(z0, z1)))
def sily(x, z, r, y0, y1): return cq.Workplane("XZ").center(x, z).circle(r).extrude(-(y1 - y0)).translate((0, y0, 0))
def silz(x, y, r, z0, z1): return cq.Workplane("XY").center(x, y).circle(r).extrude(z1 - z0).translate((0, 0, z0))


def ekle(ad, wp, mal, kaynak=KAYNAK, bom=None, grup="SABIT"):
    PARCALAR.append(dict(ad=ad, wp=wp.translate((X0, Y0, Z0)), mal=mal, birim="D_BULASIK", grup=grup, kaynak=kaynak, bom=bom))


def dunya(p):
    v = p["wp"].vals()
    return v[0] if len(v) == 1 else cq.Compound.makeCompound([o for o in v if isinstance(o, cq.Shape)])


def kur():
    PARCALAR[:] = []
    # ayaklar
    for i, (x, z) in enumerate(((30.0, -30.0), (W - 30.0, -30.0), (30.0, -D + 30.0), (W - 30.0, -D + 30.0))):
        ekle("ayar_ayagi_%d" % i, sily(x, z, 17.5, 0.0, AYAK_H), "celik",
             bom=("Ayar ayağı", 4, "MEIKO", "±12 mm (föy)") if i == 0 else None)
    # gövde (çift cidar) · ön yüzünde hazne ağzı
    g = kut(0.0, W, AYAK_H, H, -D, -KAPI["t"])
    g = g.cut(kut(HAZNE["x0"], HAZNE["x1"], HAZNE["y0"] + 5.0, HAZNE["y1"], HAZNE["z1"], -KAPI["t"] + 1.0))
    ekle("govde_cift_cidar", g, "paslanmaz", bom=("Gövde · çift cidar 304 / 316Ti", 1, "MEIKO M-iClean US", "460 × 600 × 700 · 70 kg (föy)"))
    # kapak altı sabit ön panel
    ekle("alt_on_panel", kut(0.0, W, AYAK_H, KAPI["y0"], -KAPI["t"], 0.0), "paslanmaz", kaynak="VARSAYIM (föy ön görünüşü)")
    # kapak (kapalı) · alttan menteşeli
    k = kut(2.0, W - 2.0, KAPI["y0"] + 1.0, KAPI["y1"], -KAPI["t"], 0.0)
    ekle("kapak", k, "paslanmaz", bom=("Kapak · alttan menteşeli", 1, "MEIKO", "açık toplam 1050, önde 450 (föy)"))
    ekle("dokunmatik_ekran", kut(W / 2 - 60.0, W / 2 + 60.0, 655.0, 685.0, 0.0, 1.5), "ekran_cam",
         kaynak="föy: cam dokunmatik ekran · boy VARSAYIM", bom=("Cam dokunmatik ekran", 1, "MEIKO", "çevrim 95 / 150 / 210 s"))
    ekle("isikli_kulp", silz(W / 2, 612.0, 15.0, 0.0, 8.0).cut(silz(W / 2, 612.0, 10.0, -1.0, 9.0)), "kulp_isik",
         kaynak="föy: ışıklı kapak kulpu · boy VARSAYIM", bom=("Işıklı kapak kulpu", 1, "MEIKO", "renk = makine durumu"))
    # hazne içi: M-iClean filtre (mavi) · alt + üst yıkama kolu · sepet
    zc = (HAZNE["z1"] - KAPI["t"]) / 2.0
    ekle("miclean_filtre", sily(W / 2, zc, 55.0, HAZNE["y0"] + 5.0, HAZNE["y0"] + 11.0), "mavi_touch",
         kaynak="föy: iki kademeli M-iClean filtre · boy VARSAYIM", bom=("M-iClean filtre (Blue Touch)", 1, "MEIKO", "her çevrim sonunda boşaltılır"))
    for ad, yk in (("alt", 262.0), ("ust", 600.0)):
        kol = kut(40.0, W - 40.0, yk, yk + 8.0, zc - 12.0, zc + 12.0).union(sily(W / 2, zc, 16.0, yk - 4.0, yk + 12.0))
        ekle("yikama_kolu_%s" % ad, kol, "paslanmaz", kaynak="föy: paslanmaz birleşik yıkama/durulama kolu · kot VARSAYIM",
             bom=("Yıkama + durulama kolu", 2, "MEIKO", "alt + üst · tıkanmaz") if ad == "alt" else None)
    a, s0, sh = SEPET["a"], SEPET["y0"], SEPET["h"]
    xs0 = (W - a) / 2.0; zs0 = SEPET["z0"]
    sep = kut(xs0, xs0 + a, s0, s0 + sh, zs0 - a, zs0).cut(kut(xs0 + 4.0, xs0 + a - 4.0, s0 + 4.0, s0 + sh + 1.0, zs0 - a + 4.0, zs0 - 4.0))
    for i in range(1, 8):
        xx = xs0 + i * a / 8.0
        sep = sep.union(kut(xx - 1.5, xx + 1.5, s0, s0 + 4.0, zs0 - a + 4.0, zs0 - 4.0))
    ekle("sepet_400", sep, "sepet_tel", kaynak="föy: 400 × 400 sepet · yükseklik VARSAYIM", bom=("Sepet 400 × 400", 2, "MEIKO", "1 bardak + 1 düz (föy)"))
    # arka bağlantılar (föy: soldan 40 / 186 / 313 · yerden 60 / 165 / 95)
    for ad, (x, y, r) in BAG.items():
        ekle("baglanti_%s" % ad, silz(x, y, r, -D - 25.0, -D), "celik" if ad == "elektrik" else "mavi_touch",
             bom=("Bağlantı · %s" % ad, 1, "MEIKO", {"elektrik": "SO kablo 2,2 m", "tahliye": "Ø38 dolaylı tahliye, pompalı · hortum 1,6 m", "su": "¾\" hortum 2 m, Y süzgeçli"}[ad]))
    return PARCALAR


def kapi_acik_zarf():
    """kapağın açılırken taradığı hacim (dünya): menteşe (y 245, z 0) etrafında çeyrek daire, yarıçap 455 → kutu"""
    L = KAPI["y1"] - KAPI["y0"]
    return (X0, X0 + W), (Y0 + KAPI["y0"] - KAPI["t"], Y0 + KAPI["y1"]), (Z0, Z0 + L)


def kendi_arasinda(ps):
    S = [(p["ad"], dunya(p)) for p in ps]
    out = []
    for i, (a, sa) in enumerate(S):
        A = sa.BoundingBox()
        for c, sc in S[i + 1:]:
            B = sc.BoundingBox()
            if A.xmin < B.xmax and B.xmin < A.xmax and A.ymin < B.ymax and B.ymin < A.ymax and A.zmin < B.zmax and B.zmin < A.zmax:
                v = sa.intersect(sc).Volume()
                if v > 1.0: out.append((round(v, 1), a, c))
    return out


if __name__ == "__main__":
    ps = kur()
    gec = [p["ad"] for p in ps if not dunya(p).isValid()]
    print("BULASIK v1 · %d parça · katı denetimi: %s" % (len(ps), "hepsi geçerli" if not gec else gec))
    bb = cq.Compound.makeCompound([dunya(p) for p in ps]).BoundingBox()
    print("ZARF (dünya): x %.0f–%.0f · y %.0f–%.0f · z %.0f–%.0f" % (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax))
    cak = kendi_arasinda(ps)
    print("KENDİ ARASINDA (> 1 mm³): %s" % ("TEMİZ" if not cak else cak))
    kx, ky, kz = kapi_acik_zarf()
    print("KAPAK AÇIK ZARFI: x %.0f–%.0f · y %.0f–%.0f · z %.0f–%.0f (öne %.0f; föy 450)" % (kx + ky + kz + (kz[1] - kz[0],)))
    print("AĞIZ: yerden %.0f–%.0f (makine altı dünyada %.0f) · sepet %s × %s" % (AGIZ["y0"], AGIZ["y0"] + AGIZ["h"], Y0, SEPET["a"], SEPET["a"]))
    assert not gec and not cak
    sys.stdout.flush(); os._exit(0)
