# -*- coding: utf-8 -*-
"""AUTOKITCH · K altı · BULAŞIK MAKİNESİ · MEIKO M-iClean US · CAD v2 (27 Eyl 2026 gece · SPEC_on_duzlem_v63 §2.5)
v2 — Kemal: "bulaşık makinesi önüne kapak, alt ayaklarını kaldır". v1 ↔ v2:
  · AYAR AYAKLARI KALKTI (4 parça). Makine K'nin içindeki TABLAYA oturur (tabla kesme_cad_v6'da: 3 mm tava + 2 × 40×20×2 kiriş, yan saclara kaynaklı).
    Yerel geometri v1 ile AYNI kalır: gövde altı yerel y = TABAN (10, v1'in ayak boyu) → dünyada Y0 + 10 = tabla üstü (K'de 149: makine v1'e göre +13).
  · Havada kalan iç parçalar bağlandı: sepet 2 rayın üstüne oturur (hazne yan duvarlarına), yıkama kolları göbek borularıyla (alt: hazne tabanı →
    M-iClean filtresinin ortasından; üst: hazne tavanından) — filtreye göbek borusu için Ø20 orta delik açıldı.
  · Diğer bütün parçalar (gövde, alt ön panel, kapak, ekran, kulp, filtre dışı, kollar, sepet, arka bağlantılar) v1 ile birebir (yalnız Y0 kaydı).
Kaynak: MEIKO M-iClean US teknik föyü (meiko.us, 8-15-21, sayfa 1-2) + meiko.com M-iClean U teknik veri:
  gövde 460 × 600 (derin) × 700 (AB; ABD föyünde 730 ayaklı) · ayar ayakları ±12 (v2: SÖKÜLÜR) · kapak ağzı 315, yerden 275 ·
  kapak alttan menteşeli, açıkken toplam 1050 (önde 450) · sepet 400 × 400 · arka bağlantılar soldan: elektrik 40,
  tahliye (D) 186, su (W) 313 · yerden: tahliye 165, su 95 · arkada duvar payı 25 · dokunmatik ekran + ışıklı kulp kapağın üstünde ·
  M-iClean filtre ve elle temizlenen parçalar mavi (Blue Touch) · 70 kg.
VARSAYIM (föyde yok): çift cidar kalınlığı, iç hazne sınırları, yıkama kolu boyu/kotu, sepet yüksekliği 100, ekran/kulp boyu,
  v2: sepet rayı kesiti 9 × 8, göbek borusu Ø20 (gerçek makinede pompa çıkışı / üst besleme borusu; ölçü föyde yok).
Koordinat: yerel x 0…460 (soldan sağa), y 0…700 (v1 ayak tabanından; gövde altı y = TABAN = 10), z 0 (ön yüz) … −600 (arka).
Dünyada (X0, Y0, Z0) = (4108,5 · 139 · −20) — K altında (kesme_cad_v6.BULASIK_YER; montaj AYNISINI atar: BM.X0/Y0/Z0 = KS.BULASIK_YER, kur()'dan ÖNCE).
Sözleşme (v1 ile aynı): kur() · PARCALAR · dunya(p) · BIRIMLER · MALZEME · kapi_acik_zarf() · kendi_arasinda() · W D H. Önceki: bulasik_cad_v1.py"""
import math, os, sys
import cadquery as cq

X0, Y0, Z0 = 4108.5, 139.0, -20.0                        # v2: K altında tabla üstü (gövde altı Y0 + TABAN = 149) · v1 başlığı (2540, 130) eskimişti
W, D, H = 460.0, 600.0, 700.0
TABAN = 10.0                                            # v2: gövde altının yerel y'si (v1'de ayak boyu AYAK_H) — ayak YOK, makine tablaya oturur
AYAK_H = TABAN                                          # v1 adı (geri uyum; v2'de ayak modellenmez)
KAPI = dict(y0=245.0, y1=700.0, t=22.0)                 # kapak: menteşe y 245, boy 455 → açık 455 ≈ föy 450
AGIZ = dict(y0=275.0, h=315.0)                          # föy: kapak ağzı 315, yerden 275
HAZNE = dict(x0=25.0, x1=435.0, y0=245.0, y1=630.0, z1=-575.0)   # VARSAYIM: çift cidar 25
SEPET = dict(a=400.0, y0=280.0, h=100.0, z0=-98.0)      # föy: 400 × 400 · yükseklik VARSAYIM
RAY = dict(h=8.0, z0=-570.0, z1=-40.0)                  # v2: sepet rayı 9 × 8 (hazne duvarından sepet kenarına) · boy 530 VARSAYIM
GOBEK_R = 10.0                                          # v2: yıkama kolu göbek borusu Ø20 VARSAYIM
BAG = dict(elektrik=(40.0, 60.0, 7.0), tahliye=(186.0, 165.0, 15.0), su=(313.0, 95.0, 10.0))   # (soldan x, yerden y, yarıçap) — yerden = v1 ayak tabanından

PARCALAR = []
BIRIMLER = [("D_BULASIK", "Bulaşık makinesi · MEIKO M-iClean US (GERÇEK MODEL v2, föy ölçüleri) · 460 × 600 × 690 gövde · AYAKSIZ, K tablasına oturur (v2) · kapak alttan menteşeli, açık 1050 (önde 450) · ağız 315 · sepet 400 × 400 rayda · yıkama kolları göbek borulu · dokunmatik ekran + ışıklı kulp · M-iClean filtre · arka bağlantılar: elektrik 40 · tahliye 186/165 · su 313/95 · 70 kg")]
BIRIM_MODUL = {"D_BULASIK": "K"}
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
    # v2: AYAR AYAKLARI YOK (Kemal: "alt ayaklarını kaldır") — gövde altı (yerel TABAN) K tablasının üstüne oturur
    # gövde (çift cidar) · ön yüzünde hazne ağzı
    g = kut(0.0, W, TABAN, H, -D, -KAPI["t"])
    g = g.cut(kut(HAZNE["x0"], HAZNE["x1"], HAZNE["y0"] + 5.0, HAZNE["y1"], HAZNE["z1"], -KAPI["t"] + 1.0))
    ekle("govde_cift_cidar", g, "paslanmaz", bom=("Gövde · çift cidar 304 / 316Ti", 1, "MEIKO M-iClean US", "460 × 600 × 690 · 70 kg (föy) · v2: ayaksız, tablaya oturur"))
    # kapak altı sabit ön panel
    ekle("alt_on_panel", kut(0.0, W, TABAN, KAPI["y0"], -KAPI["t"], 0.0), "paslanmaz", kaynak="VARSAYIM (föy ön görünüşü)")
    # kapak (kapalı) · alttan menteşeli
    k = kut(2.0, W - 2.0, KAPI["y0"] + 1.0, KAPI["y1"], -KAPI["t"], 0.0)
    ekle("kapak", k, "paslanmaz", bom=("Kapak · alttan menteşeli", 1, "MEIKO", "açık toplam 1050, önde 450 (föy)"))
    ekle("dokunmatik_ekran", kut(W / 2 - 60.0, W / 2 + 60.0, 655.0, 685.0, 0.0, 1.5), "ekran_cam",
         kaynak="föy: cam dokunmatik ekran · boy VARSAYIM", bom=("Cam dokunmatik ekran", 1, "MEIKO", "çevrim 95 / 150 / 210 s"))
    ekle("isikli_kulp", silz(W / 2, 612.0, 15.0, 0.0, 8.0).cut(silz(W / 2, 612.0, 10.0, -1.0, 9.0)), "kulp_isik",
         kaynak="föy: ışıklı kapak kulpu · boy VARSAYIM", bom=("Işıklı kapak kulpu", 1, "MEIKO", "renk = makine durumu"))
    # hazne içi: M-iClean filtre (mavi) · alt + üst yıkama kolu · sepet
    zc = (HAZNE["z1"] - KAPI["t"]) / 2.0
    fy0, fy1 = HAZNE["y0"] + 5.0, HAZNE["y0"] + 11.0
    ekle("miclean_filtre", sily(W / 2, zc, 55.0, fy0, fy1).cut(sily(W / 2, zc, GOBEK_R, fy0 - 1.0, fy1 + 1.0)), "mavi_touch",
         kaynak="föy: iki kademeli M-iClean filtre · boy VARSAYIM · v2: göbek borusu için Ø20 orta delik", bom=("M-iClean filtre (Blue Touch)", 1, "MEIKO", "her çevrim sonunda boşaltılır"))
    for ad, yk in (("alt", 262.0), ("ust", 600.0)):
        kol = kut(40.0, W - 40.0, yk, yk + 8.0, zc - 12.0, zc + 12.0).union(sily(W / 2, zc, 16.0, yk - 4.0, yk + 12.0))
        ekle("yikama_kolu_%s" % ad, kol, "paslanmaz", kaynak="föy: paslanmaz birleşik yıkama/durulama kolu · kot VARSAYIM",
             bom=("Yıkama + durulama kolu", 2, "MEIKO", "alt + üst · tıkanmaz") if ad == "alt" else None)
    # v2 · göbek boruları: kollar havada kalmasın (alt: hazne tabanı → filtre deliğinden → kol göbeği · üst: kol göbeği → hazne tavanı)
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
    # v2 · sepet rayları: hazne yan duvarından (x 25 / 435) sepet kenarının altına (x 34 / 426) — sepet rayın üstüne oturur
    for ad, (xa, xb) in (("sol", (HAZNE["x0"], xs0 + 4.0)), ("sag", (xs0 + a - 4.0, HAZNE["x1"]))):
        ekle("sepet_rayi_%s" % ad, kut(xa, xb, s0 - RAY["h"], s0, RAY["z0"], RAY["z1"]), "paslanmaz",
             kaynak="VARSAYIM: sepet kızak rayı (föyde ölçü yok)", bom=("Sepet rayı", 2, "MEIKO iç parçası", "9 × 8 × 530 VARSAYIM") if ad == "sol" else None)
    # arka bağlantılar (föy: soldan 40 / 186 / 313 · yerden 60 / 165 / 95)
    for ad, (x, y, r) in BAG.items():
        ekle("baglanti_%s" % ad, silz(x, y, r, -D - 25.0, -D), "celik" if ad == "elektrik" else "mavi_touch",
             bom=("Bağlantı · %s" % ad, 1, "MEIKO", {"elektrik": "SO kablo 2,2 m", "tahliye": "Ø38 dolaylı tahliye, pompalı · hortum 1,6 m", "su": "¾\" hortum 2 m, Y süzgeçli"}[ad]))
    return PARCALAR


def tabla_ustu():
    """makinenin oturduğu yüz (dünya y): gövde altı = Y0 + TABAN"""
    return Y0 + TABAN


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
    print("BULASIK v2 · %d parça · katı denetimi: %s" % (len(ps), "hepsi geçerli" if not gec else gec))
    bb = cq.Compound.makeCompound([dunya(p) for p in ps]).BoundingBox()
    print("ZARF (dünya): x %.1f–%.1f · y %.1f–%.1f · z %.1f–%.1f · gövde altı (tabla üstü) %.1f" % (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax, tabla_ustu()))
    cak = kendi_arasinda(ps)
    print("KENDİ ARASINDA (> 1 mm³): %s" % ("TEMİZ" if not cak else cak))
    kx, ky, kz = kapi_acik_zarf()
    print("KAPAK AÇIK ZARFI: x %.1f–%.1f · y %.1f–%.1f · z %.1f–%.1f (öne %.0f; föy 450)" % (kx + ky + kz + (kz[1] - kz[0],)))
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import denetim_temas_v1 as DT
    hv = DT.havada([(p["ad"], dunya(p)) for p in ps], zemin_y=tabla_ustu())       # kök: tablaya oturan gövde (+ alt ön panel)
    nh = DT.yaz(hv, baslik="HAVADA PARCA (bulasik v2 · kok = tablaya oturan govde)")
    ayak = [p["ad"] for p in ps if p["ad"].startswith("ayar_ayagi")]
    print("AYAK: %s" % ("YOK (v2)" if not ayak else ayak))
    assert not gec and not cak and nh == 0 and not ayak and abs(bb.ymin - tabla_ustu()) < 0.01
    print("BULASIK v2 DENETIM: GECTI")
    sys.stdout.flush(); os._exit(0)
