# -*- coding: utf-8 -*-
"""AUTOKITCH · S · BULAŞIK MAKİNESİ · MEIKO M-iClean US · CAD v3 (30 Eyl 2026) — PERSONEL TEZGÂHININ ALTINDA
v3 — Kemal (30 Eyl): "bulaşık makinesini personel tezgâhının altına koy, o tezgâhı ona göre ayarla". v2 ↔ v3:
  · YER: K'nin tablası değil, personel tezgâhının altı (tezgah_cad_v2). Makine ZEMİNE oturur → v1'in 4 AYAR AYAĞI GERİ (Ø35 × 10, föy ±12).
  · YÖN: ön ön yüz dünyada −x'e bakar (YON = −90°: yerel z → dünya −x, yerel x → dünya +z). Kapak, tezgâh cebinin solundaki bekleme alanına
    açılır; ön zon 84 derin olduğu için ince duvara bakan kapak açılamazdı (açık önde 450 > 190).
  · Diğer bütün parçalar (gövde, alt ön panel, kapak, ekran, kulp, filtre, kollar, göbek boruları, sepet + rayları, arka bağlantılar) v2 ile birebir.
Kaynak: MEIKO M-iClean US teknik föyü (meiko.us, 8-15-21, sayfa 1-2) + meiko.com M-iClean U teknik veri:
  gövde 460 × 600 (derin) × 700 (AB, ayaklı; ABD föyünde 730) · ayar ayakları ±12 · kapak ağzı 315, yerden 275 · kapak alttan menteşeli,
  açıkken toplam 1050 (önde 450) · sepet 400 × 400 · arka bağlantılar soldan: elektrik 40, tahliye (D) 186, su (W) 313 · yerden: tahliye 165, su 95 ·
  arkada duvar payı 25 · 2,7 kW 230 V / 6,7 kW 400 V 3N · tank 11 L · 70 kg.
VARSAYIM (föyde yok): çift cidar 25, iç hazne sınırları, yıkama kolu boyu/kotu, sepet yüksekliği 100, ekran/kulp boyu, sepet rayı 9 × 8, göbek borusu Ø20.
Koordinat: YEREL x 0…460 (makineye önden bakınca soldan sağa), y 0…700 (zemin = ayak tabanı), z 0 (ön yüz) … −600 (arka).
Dünyaya: yerel nokta → R_y(YON) → + (X0, Y0, Z0). YON = −90 → ön yüz dünya x = X0, arka x = X0 + 600, sol yan dünya z = Z0, sağ yan z = Z0 + 460.
Sözleşme (v2 ile aynı): kur() · PARCALAR · dunya(p) · BIRIMLER · MALZEME · kapi_acik_zarf() · kendi_arasinda() · tabla_ustu() · W D H.
Önceki: bulasik_cad_v2.py (K altında, ayaksız)."""
import math, os, sys
import cadquery as cq

X0, Y0, Z0 = 3857.0, 0.0, 1050.2                         # v3: ön yüz x 3857 (tezgâh önleriyle aynı düzlem) · zemin · sol yan z 1050,2 (tezgah_cad_v2 atar)
YON = -90.0                                             # v3: derece, düşey (y) eksen etrafında · −90 = ön yüz −x'e bakar
W, D, H = 460.0, 600.0, 700.0
AYAK_H = 10.0                                           # v3: ayak boyu (v1) · föy: ayarlı ±12
TABAN = AYAK_H                                          # gövde altının yerel y'si
AYAR = 12.0                                             # föy: ayak ayarı ±12
KAPI = dict(y0=245.0, y1=700.0, t=22.0)                 # kapak: menteşe y 245, boy 455 → açık 455 ≈ föy 450
AGIZ = dict(y0=275.0, h=315.0)                          # föy: kapak ağzı 315, yerden 275
HAZNE = dict(x0=25.0, x1=435.0, y0=245.0, y1=630.0, z1=-575.0)   # VARSAYIM: çift cidar 25
SEPET = dict(a=400.0, y0=280.0, h=100.0, z0=-98.0)      # föy: 400 × 400 · yükseklik VARSAYIM
RAY = dict(h=8.0, z0=-570.0, z1=-40.0)                  # sepet rayı 9 × 8 · boy 530 VARSAYIM
GOBEK_R = 10.0                                          # yıkama kolu göbek borusu Ø20 VARSAYIM
BAG = dict(elektrik=(40.0, 60.0, 7.0), tahliye=(186.0, 165.0, 15.0), su=(313.0, 95.0, 10.0))   # (soldan x, yerden y, yarıçap) — föy
DUVAR_PAYI = 25.0                                       # föy: arkada bağlantılar için duvar payı

PARCALAR = []
BIRIMLER = [("D_BULASIK", "Bulaşık makinesi · MEIKO M-iClean US (GERÇEK MODEL v3, föy ölçüleri) · 460 × 600 × 700 · PERSONEL TEZGÂHININ ALTINDA (v3), "
                          "zemine 4 ayar ayağıyla (±12) oturur · ön yüz −x'e: kapak alttan menteşeli, bekleme alanına açılır (açık 1050, önde 450) · "
                          "ağız 315 · sepet 400 × 400 · 2,7 kW 230 V / 6,7 kW 400 V 3N · çevrim 90 / 120 / 180 s · 70 kg")]
BIRIM_MODUL = {"D_BULASIK": "S"}
MALZEME = {"paslanmaz": dict(renk=(0.80, 0.82, 0.84, 1.0), met=0.9, ruf=0.30), "celik": dict(renk=(0.60, 0.62, 0.66, 1.0), met=1.0, ruf=0.35),
           "ekran_cam": dict(renk=(0.06, 0.07, 0.09, 1.0), met=0.3, ruf=0.10), "mavi_touch": dict(renk=(0.15, 0.42, 0.85, 1.0), met=0.0, ruf=0.45),
           "sepet_tel": dict(renk=(0.35, 0.37, 0.40, 1.0), met=0.2, ruf=0.55), "kulp_isik": dict(renk=(0.30, 0.75, 1.00, 1.0), met=0.0, ruf=0.30)}
KAYNAK = "MEIKO M-iClean US föyü (meiko.us 8-15-21)"


def kut(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), centered=False).translate((min(x0, x1), min(y0, y1), min(z0, z1)))
def sily(x, z, r, y0, y1): return cq.Workplane("XZ").center(x, z).circle(r).extrude(-(y1 - y0)).translate((0, y0, 0))
def silz(x, y, r, z0, z1): return cq.Workplane("XY").center(x, y).circle(r).extrude(z1 - z0).translate((0, 0, z0))


def yerlestir(wp):
    """yerel → dünya: düşey eksen etrafında YON derece döndür, sonra (X0, Y0, Z0) kadar taşı"""
    return wp.rotate((0, 0, 0), (0, 1, 0), YON).translate((X0, Y0, Z0))


def dunya_nokta(x, y, z):
    """yerel nokta → dünya (yerlestir ile aynı dönüşüm; denetimler için)"""
    a = math.radians(YON)
    return (X0 + x * math.cos(a) + z * math.sin(a), Y0 + y, Z0 - x * math.sin(a) + z * math.cos(a))


def ekle(ad, wp, mal, kaynak=KAYNAK, bom=None, grup="SABIT"):
    PARCALAR.append(dict(ad=ad, wp=yerlestir(wp), mal=mal, birim="D_BULASIK", grup=grup, kaynak=kaynak, bom=bom))


def dunya(p):
    v = p["wp"].vals()
    return v[0] if len(v) == 1 else cq.Compound.makeCompound([o for o in v if isinstance(o, cq.Shape)])


def kur():
    PARCALAR[:] = []
    # v3 · AYAR AYAKLARI (v1 ile aynı): makine zemine oturur, ±12 ayarlı
    for i, (x, z) in enumerate(((30.0, -30.0), (W - 30.0, -30.0), (30.0, -D + 30.0), (W - 30.0, -D + 30.0))):
        ekle("ayar_ayagi_%d" % i, sily(x, z, 17.5, 0.0, AYAK_H), "celik",
             bom=("Ayar ayağı", 4, "MEIKO", "±12 mm (föy)") if i == 0 else None)
    # gövde (çift cidar) · ön yüzünde hazne ağzı
    g = kut(0.0, W, TABAN, H, -D, -KAPI["t"])
    g = g.cut(kut(HAZNE["x0"], HAZNE["x1"], HAZNE["y0"] + 5.0, HAZNE["y1"], HAZNE["z1"], -KAPI["t"] + 1.0))
    ekle("govde_cift_cidar", g, "paslanmaz", bom=("Gövde · çift cidar 304 / 316Ti", 1, "MEIKO M-iClean US", "460 × 600 × 700 · 70 kg (föy)"))
    ekle("alt_on_panel", kut(0.0, W, TABAN, KAPI["y0"], -KAPI["t"], 0.0), "paslanmaz", kaynak="VARSAYIM (föy ön görünüşü)")
    k = kut(2.0, W - 2.0, KAPI["y0"] + 1.0, KAPI["y1"], -KAPI["t"], 0.0)
    ekle("kapak", k, "paslanmaz", bom=("Kapak · alttan menteşeli", 1, "MEIKO", "açık toplam 1050, önde 450 (föy)"))
    ekle("dokunmatik_ekran", kut(W / 2 - 60.0, W / 2 + 60.0, 655.0, 685.0, 0.0, 1.5), "ekran_cam",
         kaynak="föy: cam dokunmatik ekran · boy VARSAYIM", bom=("Cam dokunmatik ekran", 1, "MEIKO", "çevrim 90 / 120 / 180 s"))
    ekle("isikli_kulp", silz(W / 2, 612.0, 15.0, 0.0, 8.0).cut(silz(W / 2, 612.0, 10.0, -1.0, 9.0)), "kulp_isik",
         kaynak="föy: ışıklı kapak kulpu · boy VARSAYIM", bom=("Işıklı kapak kulpu", 1, "MEIKO", "renk = makine durumu"))
    zc = (HAZNE["z1"] - KAPI["t"]) / 2.0
    fy0, fy1 = HAZNE["y0"] + 5.0, HAZNE["y0"] + 11.0
    ekle("miclean_filtre", sily(W / 2, zc, 55.0, fy0, fy1).cut(sily(W / 2, zc, GOBEK_R, fy0 - 1.0, fy1 + 1.0)), "mavi_touch",
         kaynak="föy: iki kademeli M-iClean filtre · boy VARSAYIM · göbek borusu için Ø20 orta delik", bom=("M-iClean filtre (Blue Touch)", 1, "MEIKO", "her çevrim sonunda boşaltılır"))
    for ad, yk in (("alt", 262.0), ("ust", 600.0)):
        kol = kut(40.0, W - 40.0, yk, yk + 8.0, zc - 12.0, zc + 12.0).union(sily(W / 2, zc, 16.0, yk - 4.0, yk + 12.0))
        ekle("yikama_kolu_%s" % ad, kol, "paslanmaz", kaynak="föy: paslanmaz birleşik yıkama/durulama kolu · kot VARSAYIM",
             bom=("Yıkama + durulama kolu", 2, "MEIKO", "alt + üst · tıkanmaz") if ad == "alt" else None)
    ekle("yikama_kolu_gobek_borusu_alt", sily(W / 2, zc, GOBEK_R, fy0, 262.0 - 4.0), "paslanmaz",
         kaynak="VARSAYIM: pompa çıkış borusu (föyde ölçü yok)", bom=("Göbek borusu (yıkama kolu yatağı)", 2, "MEIKO iç parçası", "alt + üst · Ø20 VARSAYIM"))
    ekle("yikama_kolu_gobek_borusu_ust", sily(W / 2, zc, GOBEK_R, 600.0 + 12.0, HAZNE["y1"]), "paslanmaz", kaynak="VARSAYIM: üst besleme borusu (föyde ölçü yok)")
    a, s0, sh = SEPET["a"], SEPET["y0"], SEPET["h"]
    xs0 = (W - a) / 2.0; zs0 = SEPET["z0"]
    sep = kut(xs0, xs0 + a, s0, s0 + sh, zs0 - a, zs0).cut(kut(xs0 + 4.0, xs0 + a - 4.0, s0 + 4.0, s0 + sh + 1.0, zs0 - a + 4.0, zs0 - 4.0))
    for i in range(1, 8):
        xx = xs0 + i * a / 8.0
        sep = sep.union(kut(xx - 1.5, xx + 1.5, s0, s0 + 4.0, zs0 - a + 4.0, zs0 - 4.0))
    ekle("sepet_400", sep, "sepet_tel", kaynak="föy: 400 × 400 sepet · yükseklik VARSAYIM", bom=("Sepet 400 × 400", 2, "MEIKO", "1 bardak + 1 düz (föy)"))
    for ad, (xa, xb) in (("sol", (HAZNE["x0"], xs0 + 4.0)), ("sag", (xs0 + a - 4.0, HAZNE["x1"]))):
        ekle("sepet_rayi_%s" % ad, kut(xa, xb, s0 - RAY["h"], s0, RAY["z0"], RAY["z1"]), "paslanmaz",
             kaynak="VARSAYIM: sepet kızak rayı (föyde ölçü yok)", bom=("Sepet rayı", 2, "MEIKO iç parçası", "9 × 8 × 530 VARSAYIM") if ad == "sol" else None)
    for ad, (x, y, r) in BAG.items():
        ekle("baglanti_%s" % ad, silz(x, y, r, -D - DUVAR_PAYI, -D), "celik" if ad == "elektrik" else "mavi_touch",
             bom=("Bağlantı · %s" % ad, 1, "MEIKO", {"elektrik": "SO kablo 2,2 m", "tahliye": "Ø38 dolaylı tahliye, pompalı · hortum 1,6 m", "su": "¾\" hortum 2 m, Y süzgeçli"}[ad]))
    return PARCALAR


def tabla_ustu():
    """makinenin oturduğu yüz (dünya y): v3'te zemin"""
    return Y0


def govde_zarf():
    """gövde + kapak (bağlantı uçları hariç) dünya sınırları: (x0, x1), (y0, y1), (z0, z1)"""
    p = [dunya_nokta(x, 0.0, z) for x in (0.0, W) for z in (0.0, -D)]
    return (min(q[0] for q in p), max(q[0] for q in p)), (Y0, Y0 + H), (min(q[2] for q in p), max(q[2] for q in p))


def kapi_acik_zarf():
    """kapağın açılırken taradığı hacim (dünya): menteşe (y 245, yerel z 0) etrafında çeyrek daire, yarıçap 455 → kutu (yerel z 0 … +455)"""
    L = KAPI["y1"] - KAPI["y0"]
    p = [dunya_nokta(x, 0.0, z) for x in (0.0, W) for z in (0.0, L)]
    return (min(q[0] for q in p), max(q[0] for q in p)), (Y0 + KAPI["y0"] - KAPI["t"], Y0 + KAPI["y1"]), (min(q[2] for q in p), max(q[2] for q in p))


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
    print("BULASIK v3 · %d parça · katı denetimi: %s" % (len(ps), "hepsi geçerli" if not gec else gec))
    bb = cq.Compound.makeCompound([dunya(p) for p in ps]).BoundingBox()
    print("ZARF (dünya): x %.1f–%.1f · y %.1f–%.1f · z %.1f–%.1f · zemin %.1f" % (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax, tabla_ustu()))
    gx, gy, gz = govde_zarf()
    print("GÖVDE: x %.1f–%.1f · z %.1f–%.1f (ön yüz −x'e bakar · YON %.0f)" % (gx + gz + (YON,)))
    cak = kendi_arasinda(ps)
    print("KENDİ ARASINDA (> 1 mm³): %s" % ("TEMİZ" if not cak else cak))
    kx, ky, kz = kapi_acik_zarf()
    print("KAPAK AÇIK ZARFI: x %.1f–%.1f · y %.1f–%.1f · z %.1f–%.1f (öne %.0f; föy 450)" % (kx + ky + kz + (kx[1] - kx[0],)))
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import denetim_temas_v1 as DT
    hv = DT.havada([(p["ad"], dunya(p)) for p in ps], zemin_y=tabla_ustu())       # kök: zemine oturan ayaklar
    nh = DT.yaz(hv, baslik="HAVADA PARCA (bulasik v3 · kok = zemine oturan ayaklar)")
    ayak = [p["ad"] for p in ps if p["ad"].startswith("ayar_ayagi")]
    assert not gec and not cak and nh == 0 and len(ayak) == 4 and abs(bb.ymin - tabla_ustu()) < 0.01
    assert abs(gx[0] - X0) < 0.01 and abs(gx[1] - (X0 + D)) < 0.01 and abs(gz[0] - Z0) < 0.01 and abs(gz[1] - (Z0 + W)) < 0.01, "v3: yön/yer"
    assert abs(kx[0] - (X0 - (KAPI["y1"] - KAPI["y0"]))) < 0.01, "v3: kapak −x'e açılır"
    print("BULASIK v3 DENETIM: GECTI")
    sys.stdout.flush(); os._exit(0)
