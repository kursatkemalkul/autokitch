# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 39 · SERVİS DÜZELTMELERİ D2–D4 (gece 2 · adım 8 · 4 Eki 2026 · Claude · YEREL)
python 39_servis.py girdi.glb cikti.glb      (zincir: hat3_v9f.glb → hat3_v9g.glb)
Kaynak: gece2/adim7/SERVIS.md bölüm 3.
D1 (A istasyon kutusu öne) UYGULANMADI: v9f'de A istasyon kutusu / A sigortası / A Harting YOK (A elektriksiz — açıcı satın alınır, 1 Eki kararı;
   SERVIS.md eski parca_kutulari kaydından okumuştu). Değişiklik gerekmiyor.
D2 · fırın üstü üst kaydı (F_UST_KABIN__sac, 30×30×2 boru, x 2501,5–3998,5 · y 1830,5–1860,5 · z 27–57) dikmenin sağında bölünür:
     sol parça x 2501,5–3358 kaynaklı kalır · 2 mm aralık (3358–3360) · SAĞ PARÇA x 3360–3996,5 SÖKÜLÜR · sağ uçta 2 mm aralık (3996,5–3998,5).
     Sağ uç kaynak dikişi (x 3996,5–3998,5, kayıt altı) kalkar. İki uçta iç köşebent (5 mm lama L, düşey kanadı aralıkta, sol uçta sol parçanın
     ucuna / sağ uçta yan sacın iç yüzüne kaynaklı; yatay kanadı borunun içinde, M6 dişli) + uç başına 2 × ISO 7380 M6×12 A2 (alttan, boru alt cidarından).
     Dış görünüş aynı (sağ fırın üstü kapağı kaydın önünde). Kompresör (üstü y 1858) kayıt altından (1830,5) artık geçer.
D3 · yağ tenekesi lansı: emiş (PFA 10×8) ve dönüş (8×6) hortumlarına lans ile yan duvar geçişi arasındaki düz parçada kapamalı hızlı kaplin
     (CPC / Colder, polisülfon, gıda uyumlu; emiş Ø20 × 44 · dönüş Ø16 × 21,5 — dönüş hattının düz boyu 23,5 mm, ürün boyu teyit edilecek) ·
     seviye şalteri kablosunda M12 4 kutuplu fiş + dişi (Phoenix Contact SAC-4P-M12 sınıfı, Ø15) lans başlığının yanında.
D4 · kompresör çıkışı: çıkış dirseği ile orta bölme arasında (z −385…−438) 4 turluk PU spiral servis halkası (Ø10, açılmış boy ≈ 380 mm, merkez
     yarıçapı 15; z −391…−432) — düz boru z −437'den geriye kalır · kompresör beslemesi FİŞLİ: motor arkasından kablo (Ø8, H07RN-F 3G1,5) → hat içi
     fiş-priz (Wieland RST20i3 sınıfı, Ø26 × 75, IP68) → orta bölmede rakor (Lapp SKINTOP M16 sınıfı, Ø16 delik) → arka kablo rakoruna
     (f_ust_rakor_kompresor). Kompresör ≈ 300 mm öne çekilince halka uzar, çıkış vanası ve hat içi fiş önden ayrılır.
Etiketler: yeni parçalar eklendikleri düğümün kat / mek değerini alır (kablo: yeni düğüm HAVA_KOMPRESOR__kablo, kat 6 · mek F/Hava)."""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb
import cadquery as cq

gi, go = sys.argv[1:3]
t0 = time.time()
LOG = SE.log


def kutu(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0)).val()


def silindir(p0, p1, r):
    p0 = np.asarray(p0, float); p1 = np.asarray(p1, float); d = p1 - p0; h = float(np.linalg.norm(d))
    return cq.Solid.makeCylinder(r, h, cq.Vector(*p0), cq.Vector(*(d / h)))


def tup(noktalar, r):
    """dik açılı kablo: silindirler + köşe küreleri (tek katı)"""
    Q = [np.asarray(q, float) for q in noktalar]
    sh = None
    for a, b in zip(Q[:-1], Q[1:]):
        c = silindir(a, b, r); sh = c if sh is None else sh.fuse(c)
    for q in Q[1:-1]:
        sh = sh.fuse(cq.Solid.makeSphere(r, cq.Vector(*q), angleDegrees1=-90, angleDegrees2=90))
    return sh.clean()


def tek(sh):
    if sh.ShapeType() != "Solid" and len(sh.Solids()) == 1: return sh.Solids()[0]
    return sh


g = Glb(gi)
# ------------------------------------------------------------------------------------------------------------------------------------
# D2 · kayıt bölünür (m8kit + manifold): boru bileşeni yerinde iki parçaya, sağ uç kaynak dikişi silinir
# ------------------------------------------------------------------------------------------------------------------------------------
import manifold3d as mf
b = g.bilesen("F_UST_KABIN__sac", lo=np.array([2501.5, 1830.5, 27.0]), hi=np.array([3998.5, 1860.5, 57.0]), tol=0.3)
P = np.concatenate([p["X"][p["T"][t]] for p, t in b["parca"]])
m = SE.mf_ucgen(P); assert m is not None, "kayıt kapalı değil"
kes = mf.Manifold.cube([2.0, 40.0, 40.0]).translate([3358.0, 1825.0, 22.0]) + mf.Manifold.cube([2.5, 40.0, 40.0]).translate([3996.5, 1825.0, 22.0])
yeni = m - kes
Pn = SE.mf_P(yeni); v0, v1 = m.volume(), yeni.volume()
ilk = [True]
def _f(_):
    if ilk[0]: ilk[0] = False; return Pn
    return None
g.donustur(b, _f)
LOG("D2 kayıt bölündü: %.0f → %.0f mm³ (2 aralık), parça sayısı %d" % (v0, v1, len(yeni.decompose())))
kd = g.bilesen("F_UST_KABIN__sac", lo=np.array([3996.5, 1828.5, 31.0]), hi=np.array([3998.5, 1830.5, 53.0]), tol=0.3)
g.sil_b(kd); LOG("D2 sağ uç kaynak dikişi silindi")
g._bc.clear()

# ------------------------------------------------------------------------------------------------------------------------------------
# D3 · hortum parçaları kaplin boyunca kesilir (emiş z −250 · x 3948–3992 ; dönüş z −181,5 · x 3974,5–3996)
# ------------------------------------------------------------------------------------------------------------------------------------
KAP = [("emis", 1, (3948.0, 3992.0), (1827.0, -250.0), 10.0, 6.0),     # ad, hortum bileşeni (v9f no), x aralığı, (y, z) eksen, kaplin r, hortum r (kesim payı)
       ("donus", 2, (3974.5, 3996.0), (1826.5, -181.5), 8.0, 6.0)]
g.bilesen("K_YAG__hortum_yag", 0)
for ad, no, (xa, xb), (yc, zc), rk, rh in KAP:
    g._bc.clear(); g.bilesen("K_YAG__hortum_yag", 0)
    c = [q for q in g._bc["K_YAG__hortum_yag"] if q["lo"][0] < xa and q["hi"][0] > xb and q["lo"][1] < yc < q["hi"][1]]
    c = [q for q in c if q["lo"][2] - 1 < zc < q["hi"][2] + 1]
    assert len(c) == 1, (ad, len(c))
    q = c[0]
    P = np.concatenate([p["X"][p["T"][t]] for p, t in q["parca"]])
    m = SE.mf_ucgen(P); assert m is not None, ad
    k = mf.Manifold.cube([xb - xa, 2 * rh + 4, 2 * rh + 4]).translate([xa, yc - rh - 2, zc - rh - 2])
    yeni = m - k; Pn = SE.mf_P(yeni)
    ilk = [True]
    def _f2(_, Pn=Pn, ilk=ilk):
        if ilk[0]: ilk[0] = False; return Pn
        return None
    g.donustur(q, _f2)
    LOG("D3 hortum %s kesildi x %.1f–%.1f: %.0f → %.0f mm³" % (ad, xa, xb, m.volume(), yeni.volume()))
g._bc.clear()

# ------------------------------------------------------------------------------------------------------------------------------------
# D4 · düz çıkış borusu z −438'den başlar (spiral halka yerine) · orta bölmede kablo rakoru deliği (delik_ac)
# ------------------------------------------------------------------------------------------------------------------------------------
g.bilesen("HAVA_KOMPRESOR__hava_ana", 0)
c = [q for q in g._bc["HAVA_KOMPRESOR__hava_ana"] if q["hi"][2] > -381 and q["lo"][2] < -700 and abs(q["lo"][0] - 3544) < 0.6]
assert len(c) == 1, len(c)
def _kis(Pw):
    Q = Pw.copy(); Q[..., 2] = np.minimum(Q[..., 2], -437.0); return Q
g.donustur(c[0], _kis); g._bc.clear()
LOG("D4 düz boru z −437 → arka (spiral halka bölümü boşaldı)")

# ---- yeni parçalar (cadquery) --------------------------------------------------------------------------------------------------
YENI = {}       # düğüm → [parça]
def ekle(dugum, ad, sh, bom, tur=""):
    YENI.setdefault(dugum, []).append(dict(ad=ad, sh=tek(sh), bom=list(bom), tur=tur))

# D2 köşebentler + cıvatalar
for uc, xf0, xf1, xl0, xl1 in (("sol", 3358.0, 3360.0, 3360.0, 3385.0), ("sag", 3996.5, 3998.5, 3971.5, 3996.5)):
    fl = kutu(xf0, xf1, 1832.5, 1856.5, 31.0, 53.0)                       # düşey kanat (aralıkta)
    lg = kutu(min(xl0, xf0), max(xl1, xf1), 1832.5, 1837.5, 31.0, 53.0)    # yatay kanat (boru içinde, 5 mm lama, M6 diş)
    sh = fl.fuse(lg).clean()
    xs = (3366.5, 3378.5) if uc == "sol" else (3977.5, 3989.5)
    for x in xs:
        sh = sh.cut(silindir((x, 1830.0, 42.0), (x, 1840.0, 42.0), 3.1))
    ekle("F_UST_KABIN__sac", "d2_kayit_kosebent_%s" % uc, sh, ["iç köşebent 5 mm lama L (EN 10058) 304, M6 dişli, kaynaklı"], "kosebent")
    for i, x in enumerate(xs):
        bas = silindir((x, 1827.2, 42.0), (x, 1830.5, 42.0), 5.25)
        gov = silindir((x, 1830.5, 42.0), (x, 1842.5, 42.0), 3.0)
        ekle("F_UST_KABIN__paslanmaz", "d2_kayit_civata_%s_%d" % (uc, i), bas.fuse(gov).clean(), ["ISO 7380-1 M6×12 A2 cıvata"], "civata")

# D3 kaplinler + M12 fiş
for ad, no, (xa, xb), (yc, zc), rk, rh in KAP:
    xm = (xa + xb) / 2
    g1 = silindir((xa, yc, zc), (xm + 1.0, yc, zc), rk)                       # dişi (valfli gövde)
    g2 = silindir((xm - 1.0, yc, zc), (xb, yc, zc), rk - 1.5)                 # erkek (valfli uç)
    ekle("K_YAG__kaplin", "d3_kaplin_%s" % ad, g1.fuse(g2).clean(),
         ["CPC (Colder) kapamalı hızlı kaplin, polisülfon, gıda uyumlu — %s hattı (gövde + erkek uç)" % ("emiş PFA 10×8" if ad == "emis" else "dönüş 8×6")], "kaplin")
m12 = silindir((3880.0, 1814.0, -200.0), (3903.0, 1814.0, -200.0), 7.5).fuse(silindir((3902.0, 1814.0, -200.0), (3924.2, 1814.0, -200.0), 7.0)).clean()
ekle("K_YAG__siyah", "d3_seviye_salteri_M12_fis", m12, ["Phoenix Contact SAC-4P-M12 sınıfı 4 kutuplu fiş + dişi (seviye şalteri kablosu)"], "fis")

# D4 spiral halka (4 tur, adım 10,25, merkez yarıçapı 15; ekseni borunun 15 mm üstünde → giriş / çıkış borunun ekseninde)
R, ADIM, TUR = 15.0, 10.25, 4
yol = cq.Wire.makeHelix(ADIM, ADIM * TUR, R, center=cq.Vector(3549.0, 1809.0 + R, -391.0), dir=cq.Vector(0, 0, -1))
p0 = yol.startPoint(); t0v = yol.tangentAt(0)
dairesel = cq.Wire.makeCircle(5.0, p0, t0v)
spiral = cq.Solid.sweep(dairesel, [], yol, isFrenet=True)
spiral = tek(spiral)
yol = yol.rotate(cq.Vector(3549.0, 1809.0 + R, 0), cq.Vector(3549.0, 1809.0 + R, 1), 90)   # başlangıç borunun ekseninde (x 3549 · y 1809)
spiral = spiral.rotate(cq.Vector(3549.0, 1809.0 + R, 0), cq.Vector(3549.0, 1809.0 + R, 1), 90)
p0 = yol.startPoint()
bas_n = np.array([p0.x, p0.y, p0.z]); son = yol.endPoint(); son_n = np.array([son.x, son.y, son.z])
LOG("D4 spiral: başlangıç %s · bitiş %s · hacim %.0f" % (bas_n.round(2), son_n.round(2), spiral.Volume()))
ekle("HAVA_KOMPRESOR__hava_ana", "d4_spiral_servis_halkasi", spiral, ["PU spiral hortum Ø10×6,5, 4 tur, açılmış boy ≈ 380 mm (servis halkası)"], "hortum")
# fişli besleme
ekle("HAVA_KOMPRESOR__kablo", "d4_kompresor_besleme_kablosu_motor", tup([(3690, 1790, -360), (3690, 1790, -410), (3675, 1790, -410)], 4.0),
     ["H07RN-F 3G1,5 kompresör besleme kablosu (motor tarafı)"], "kablo")
fp = silindir((3600, 1790, -410), (3640, 1790, -410), 13.0).fuse(silindir((3638, 1790, -410), (3675, 1790, -410), 12.0)).clean()
ekle("HAVA_KOMPRESOR__siyah", "d4_hat_ici_fis_priz", fp, ["Wieland RST20i3 sınıfı hat içi fiş + priz, 3 kutup 20 A IP68"], "fis")
ekle("HAVA_KOMPRESOR__kablo", "d4_kompresor_besleme_kablosu_arka",
     tup([(3600, 1790, -410), (3588, 1790, -410), (3588, 1790, -795), (3689, 1790, -795), (3689, 1825, -795), (3689, 1825, -809)], 4.0),
     ["H07RN-F 3G1,5 kompresör besleme kablosu (orta bölme → arka kablo rakoru)"], "kablo")
rk_ = (silindir((3588, 1790, -444.5), (3588, 1790, -441.5), 10.0).fuse(silindir((3588, 1790, -441.6), (3588, 1790, -439.9), 8.0))
       .fuse(silindir((3588, 1790, -440.0), (3588, 1790, -437.0), 10.0)).clean().cut(silindir((3588, 1790, -446), (3588, 1790, -436), 4.3)))   # iki flanş + sac kanalı
ekle("F_UST_KABIN__plastik", "d4_orta_bolme_kablo_rakoru", rk_, ["Lapp SKINTOP sınıfı M16 kablo rakoru (orta bölme)"], "rakor")

# karşı taraf: orta bölmede Ø16 delik (rakor gövdesi kadar) — yalnız sac / yalıtım
tmp0 = go + ".e0.glb"; g.kaydet(tmp0); g = Glb(tmp0)                        # m8kit eklenen üçgenleri kayıttan sonra görür → yeniden yükle (sağ kayıt parçası delinecek)
K = SE.Karsi(g, haric_onek=("HAVA_KOMPRESOR__", "K_YAG__"), acik_dene=True)
delik = [dict(ad="d4_orta_bolme_delik_M16", sh=silindir((3588, 1790, -446.0), (3588, 1790, -436.0), 8.0), bom=["Ø16 delik"])]
delik += [p for p in YENI["F_UST_KABIN__paslanmaz"]]                         # D2 cıvataları: kayıt sağ parçasının alt cidarında Ø6,6 geçiş deliği
kayit = K.delik_ac(delik)
tmp = go + ".e1.glb"; g.kaydet(tmp); del g, K

H = SE.Ham(tmp)
ET = {}
for d in YENI:
    ET[d] = H.etiket(d)
ET["HAVA_KOMPRESOR__kablo"] = (6, H.etiket("HAVA_KOMPRESOR__hava_ana")[1])
ET["K_YAG__kaplin"] = H.etiket("K_YAG__pom")
SABLON = {"HAVA_KOMPRESOR__kablo": "ELK_K__kablo", "K_YAG__kaplin": "K_YAG__pom"}
for d in sorted(YENI):
    kat, mek = ET[d]
    H.koy(d, YENI[d], kat=kat, mek=mek, ekle=H.dugum(d) is not None and "mesh" in H.dugum(d), sablon=SABLON.get(d))
H.yaz(tmp + ".e2.glb")
SE.sikistir(tmp + ".e2.glb", go)
for f in (tmp0, tmp, tmp + ".e2.glb"): os.remove(f)
SE.ent_json(go[:-4] + "_ent.json", "SERVIS", [(d, YENI[d]) for d in sorted(YENI)], H.aralik, lambda a: False, "F/Hava", (), kayit,
            ek=dict(d1="uygulanmadı — A istasyon kutusu v9f'de yok (A elektriksiz)"))
LOG("ADIM 39 bitti · %s · %.0f sn" % (go, time.time() - t0))
sys.stdout.flush(); os._exit(0)
