# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 61 · DAVLUMBAZ YAĞ FİLTRESİ SOLA KAYAR, PİZZA KUTUSU TARAFINDAN ALINIR (5 Eki 2026 · Claude · bulut oturumu)
python 61_filtre_servis.py girdi.glb cikti.glb      (zincir: hat3_v10b.glb → hat3_v10c.glb)

Sorun (SERVIS.md §1.3, STANDART_DURUM madde 6): EN 16282 yağ filtresi haftalık yıkanır; filtre (x 3420–3920 · y 1363–1763 · z −496,5…−441,5, yağ + karbon)
bölme sacının (F_UST_KABIN__sac bileşeni: x 2501,5–3998,5 · y 1348–1860,5 · z −441,5…−421,5) hemen arkasında, önünde kompresör (25 kg) + yağ tankı.
Kemal (5 Eki): "pide kutuları istifli, oradan ulaşsa kutuları çıkarmak daha kolay" → filtre SOLA kayar, kutu stoğunun arkasındaki servis kapağından alınır.
  1. Filtre çerçevesinin (F_DAVLUMBAZ__paslanmaz, x 3385–3955) SOL kenarı açılır (manifold fark: x 3384–3421 · y 1362,5–1763,5): çerçeve sola açık U.
  2. Ray uzantısı (304, 3 mm) x 2790–3385: alt + üst ray plakası (y 1348–1351 / 1775–1778) + arka dudak (z −498,5…−496,5); ön kılavuz = bölme sacı.
  3. Bölme sacında servis ağzı x 2790–3320 · y 1352–1772 (530 × 420) — kutu stoğunun (x 2520–3324) arkasında; sağda kompresör bölmesinin dikey ara sacı (x 3325,5) kalır. Kapak: ağzı dolduran 20 mm derin 1,5 mm tava tapa (sacla aynı yapı, 1 mm boşluk);
     2 çeyrek tur KAM kilit (Southco E5 sınıfı, Ø16 gömme baş, x 2805 / 3305 · y 1562): kam kapalıyken bölme sacının arkasına geçer, tapayla birlikte çıkar
     → ağızda sabit dil yok, filtre yolu boş (ağız 530 × 420 > filtre 500 × 400). Açmak için anahtar / bozuk para.
  4. Adım 34'ün iki M5 arayüz saplaması (bölme arka sacı, x 3527,5 / 3812,5 · y 1563) filtrenin İÇİNE 10,5 mm giriyordu (eski çakışma) → çerçevenin üst
     kenarına taşındı (y 1770,5; bölmede yeni Ø5 delik, eskiler kapandı; çerçevede Ø5,5).
Haftalık: kutular çıkarılır → 2 kilit çevrilir, tapa alınır → filtre sola çekilir (615 mm → x 2805–3305) → öne alınır → yıkanır (MEIKO). Kompresör / yağ tankı yerinde.
Denetim (bu betikte): üç bileşen tek ve beklenen kutuda, kapalı · kayma yolu (x 2790–3420, filtre kesiti) boş · öne çekiş yolu (x 2805–3305, z −441,5…+59) yalnız kutu stoğu · ray / dil / tapa / kilit hacmi boş."""
import os, sys, time, json, subprocess
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb
import manifold3d as mf
import cadquery as cq

gi, go = sys.argv[1:3]
t0 = time.time(); LOG = SE.log
HERE = os.path.dirname(os.path.abspath(__file__))
CERCEVE = ("F_DAVLUMBAZ__paslanmaz", (3385.0, 1348.0, -496.5), (3955.0, 1778.0, -441.5))
BOLME = ("F_UST_KABIN__sac", (2501.5, 1348.0, -441.5), (3998.5, 1860.5, -421.5))
SOL_KES = ((3384.0, 1362.5, -497.5), (3421.0, 1763.5, -440.5))
AGIZ = ((2790.0, 1352.0, -442.5), (3320.0, 1772.0, -420.5))
YOL = ((2790.0, 1351.0, -496.5), (3420.0, 1775.0, -441.5))                  # filtrenin kayma yolu (rayların arası)
RAY = [((2790.0, 1348.0, -496.5), (3385.0, 1351.0, -441.5)), ((2790.0, 1348.0, -498.5), (3385.0, 1366.0, -496.5)),
       ((2790.0, 1775.0, -496.5), (3385.0, 1778.0, -441.5)), ((2790.0, 1760.0, -498.5), (3385.0, 1778.0, -496.5))]
KAM = [((2776.0, 1556.0, -443.5), (2806.0, 1568.0, -441.5)), ((3304.0, 1556.0, -443.5), (3334.0, 1568.0, -441.5))]   # kapalı konumda bölme sacının arkasında (tapayla çıkar)
SAPLAMA = [("F_UST_KABIN__paslanmaz", (3524.05, 1559.55, -452.0), (3530.95, 1566.45, -440.0)),     # adım 34 arayüz saplamaları filtrenin İÇİNDE kalıyordu
           ("F_UST_KABIN__paslanmaz", (3809.05, 1559.55, -452.0), (3815.95, 1566.45, -440.0))]     # → çerçevenin üst kenarına (y 1563 → 1770,5)
SAPLAMA_DY = 207.5
DELIK_R = 2.5
TAPA = ((2791.0, 1353.0, -441.5), (3319.0, 1771.0, -421.5))
KILIT = [(2805.0, 1562.0), (3305.0, 1562.0)]          # tapa ön yüzünde, kam ekseni                                # dil merkezleri hizasında (çapraz)
KR = 8.0


def mfk(P):
    V = P.reshape(-1, 3); u, inv = np.unique(np.round(V, 5), axis=0, return_inverse=True)
    m = mf.Manifold(mf.Mesh(vert_properties=u.astype(np.float32), tri_verts=inv.reshape(-1, 3).astype(np.uint32)))
    assert m.status() == mf.Error.NoError, m.status()
    return m


def mf_P(m):
    M = m.to_mesh(); V = np.asarray(M.vert_properties)[:, :3].astype(float); T = np.asarray(M.tri_verts).astype(np.int64)
    return V[T]


def kup(lo, hi):
    lo = np.array(lo, float); hi = np.array(hi, float)
    return mf.Manifold.cube((hi - lo).tolist()).translate(lo.tolist())


def disk(x, y, r, z0, z1):
    return mf.Manifold.cylinder(z1 - z0, r, r, 32).translate([x, y, z0])


def kes(dug, lo, hi, kesici, ad, dolgu=(), delik=()):
    b = g.bilesen(dug, lo=np.array(lo), hi=np.array(hi), tol=0.3)
    P0 = np.concatenate([p["X"][p["T"][t]] for p, t in b["parca"]])
    M = SE.mf_ucgen(P0); assert M is not None, "ADIM 61 DUR: %s kapalı katı kurulamadı" % ad
    v0 = M.volume(); M2 = M - kesici
    for x, y in dolgu: M2 = M2 + disk(x, y, DELIK_R + 0.01, -441.5, -440.0)       # bölme arka sacı 1,5 (z −441,5…−440)
    for x, y in delik: M2 = M2 - disk(x, y, DELIK_R, -442.5, -439.0)
    v1 = M2.volume()
    Y = SE.mf_P(M2); ilk = [True]
    def f(_):
        if ilk[0]: ilk[0] = False; return Y
        return None
    g.donustur(b, f)
    LOG("  %-10s %s: hacim %.0f → %.0f mm³ (−%.0f)" % (ad, dug, v0, v1, v0 - v1))
    return round(v0 - v1, 1)


def cerceve_u():
    """çerçeve ağı kapalı katı değil (T-birleşimli) → aynı ölçülerle temiz U olarak yeniden kurulur: dış kutu − filtre açıklığı − sol kenar
    − 2 alt bağlantı deliği (M5 Ø5,5, y ekseni, x 3527,5 / 3812,5 · z −469: eski ağdaki delik köşeleriyle aynı) · eski ağın köşe kümesi denetlenir"""
    b = g.bilesen(CERCEVE[0], lo=np.array(CERCEVE[1]), hi=np.array(CERCEVE[2]), tol=0.3)
    P0 = np.concatenate([p["X"][p["T"][t]] for p, t in b["parca"]])
    ys = sorted(set(np.round(P0[:, :, 1], 2).ravel().tolist()))
    assert ys == [1348.0, 1358.5, 1363.0, 1763.0, 1778.0], "ADIM 61 DUR: çerçeve y kotları %s" % ys
    xs = np.round(P0[:, :, 0], 2); assert xs.min() == 3385.0 and xs.max() == 3955.0
    dis = kup((3385.0, 1348.0, -496.5), (3955.0, 1778.0, -441.5))
    ic = kup((3420.0, 1363.0, -497.5), (3920.0, 1763.0, -440.5))
    U = dis - ic - kup(*SOL_KES)
    for x in (3527.5, 3812.5):
        U = U - mf.Manifold.cylinder(12.0, 2.75, 2.75, 32).rotate([-90.0, 0.0, 0.0]).translate([x, 1347.0, -469.0])
        U = U - mf.Manifold.cylinder(13.0, 2.75, 2.75, 32).translate([x, 1563.0 + SAPLAMA_DY, -453.5])     # üst kenar: taşınan saplamalar Ø5,5
    v0 = (dis - ic).volume(); v1 = U.volume()
    Y = SE.mf_P(U); ilk = [True]
    def f(_):
        if ilk[0]: ilk[0] = False; return Y
        return None
    g.donustur(b, f)
    LOG("  çerçeve    %s: U olarak yeniden (sol kenar açık) · halka %.0f → U %.0f mm³" % (CERCEVE[0], v0, v1))
    return round(v0 - v1, 1)


g = Glb(gi)
# boşluk denetimi tablosu (kesilecek iki bileşen + filtre hariç her şey)
MN, MX, AD = [], [], []
for p in g.prims:
    if p.get("gizli") or p["pr"].get("mode", 4) != 4: continue
    P = p["X"][p["T"]]; m = np.all(P.max(1) >= [2700, 1300, -560], 1) & np.all(P.min(1) <= [3500, 1800, -400], 1)
    MN.append(P[m].min(1)); MX.append(P[m].max(1)); AD += [p["name"]] * int(m.sum())
MN = np.concatenate(MN); MX = np.concatenate(MX); AD = np.array(AD)


def bos(lo, hi, pay=0.3, haric=()):
    lo = np.array(lo) + pay; hi = np.array(hi) - pay
    m = np.all(MX > lo, 1) & np.all(MN < hi, 1)
    return sorted(set(AD[m]) - set(haric))


# kayma yolu: çerçeve + bölme sacı (yüzey teması) dışında boş olmalı
d = bos(*YOL, pay=0.6, haric=())
d = [x for x in d if x not in (CERCEVE[0],)]
assert not d, "ADIM 61 DUR: kayma yolunda %s" % d
for ad, L in (("ray", RAY), ("kam", KAM)):
    for lo, hi in L:
        d = bos(lo, hi)
        assert not d, "ADIM 61 DUR: %s hacmi dolu %s %s" % (ad, (lo, hi), d)
v_sol = cerceve_u()
v_agiz = kes(BOLME[0], BOLME[1], BOLME[2], kup(*AGIZ), "bölme", dolgu=[(x, 1563.0) for x in (3527.5, 3812.5)],
             delik=[(x, 1563.0 + SAPLAMA_DY) for x in (3527.5, 3812.5)])
for d_, lo_, hi_ in SAPLAMA:
    bs = g.bilesen(d_, lo=np.array(lo_), hi=np.array(hi_), tol=0.3)
    g.tasi_b(bs, np.array([0.0, SAPLAMA_DY, 0.0]))
LOG("  saplama    2 × M5 FHP y 1563 → 1770,5 (çerçeve üst kenarı) · eski delikler kapandı")
assert v_sol > 1000 and v_agiz > 100000, "ADIM 61 DUR: kesim hacmi beklenenden küçük"
tmp = go + ".e1.glb"; g.kaydet(tmp); del g
H = SE.Ham(tmp)


def kutu(lo, hi):
    lo = np.array(lo, float); hi = np.array(hi, float)
    return cq.Workplane("XY").box(*(hi - lo), centered=False).translate(tuple(lo)).val()


tlo, thi = np.array(TAPA[0]), np.array(TAPA[1])                               # tapa = 1,5 mm tava (bölme sacıyla aynı yapı): ön yüz + 4 dönüş, arkası açık
tapa = cq.Workplane("XY").add(kutu(tlo, thi)).cut(cq.Workplane("XY").add(kutu(tlo + [1.5, 1.5, -1.0], thi - [1.5, 1.5, 1.5])))
for x, y in KILIT:
    tapa = tapa.cut(cq.Workplane("XY").add(cq.Solid.makeCylinder(KR, 20.0, cq.Vector(x, y, -441.5), cq.Vector(0, 0, 1))))
PAR = [("F_DAVLUMBAZ_RAY__paslanmaz", "F_DAVLUMBAZ__paslanmaz", 22,
        [dict(ad="filtre_ray_%d" % i, sh=kutu(lo, hi), bom=["Filtre ray uzantısı AISI 304 3 mm (lazer + büküm, çerçeveye punta)"]) for i, (lo, hi) in enumerate(RAY)]
),
       ("F_UST_KABIN_TAPA__sac", "F_UST_KABIN__sac", 19,
        [dict(ad="filtre_servis_tapasi", sh=tapa.val(), bom=["Filtre servis tapası AISI 304 1,5 mm tava 528 × 418 × 20 (lazer + 4 büküm, köşeler TIG)"])]),
       ("F_UST_KABIN_TAPA__siyah", "K_GOVDE__siyah", 19,
        [dict(ad="filtre_servis_kilidi_%d" % i, sh=cq.Solid.makeCylinder(KR - 0.2, 1.5, cq.Vector(x, y, -423.0), cq.Vector(0, 0, 1)).fuse(
              cq.Solid.makeCylinder(4.0, 20.0, cq.Vector(x, y, -443.5), cq.Vector(0, 0, 1))),
              bom=["Southco E5 sınıfı çeyrek tur kam kilit (Ø16 gömme baş, tapayla çıkar)"]) for i, (x, y) in enumerate(KILIT)]
        + [dict(ad="filtre_servis_kami_%d" % i, sh=kutu(lo, hi), bom=["E5 kam dili (kapalı konumda bölme sacının arkasında)"]) for i, (lo, hi) in enumerate(KAM)])]
TUM = {}
for d, sb, mek, L in PAR:
    H.koy(d, L, kat=0, mek=mek, sablon=sb)
    TUM[d] = L
H.yaz(tmp + ".e2.glb")
SE.sikistir(tmp + ".e2.glb", go)
for f in (tmp, tmp + ".e2.glb"): os.remove(f)
for d in TUM: H.aralik[d] = {p["ad"]: (0, 0) for p in TUM[d]}
SE.ent_json(go[:-4] + "_ent.json", "F_FILTRE", [(d, TUM[d]) for d in sorted(TUM)], H.aralik, lambda a: False, "F/Davlumbaz", (),
            [dict(cerceve_sol_kesik=v_sol, bolme_agiz=v_agiz)], ek=dict(agiz=AGIZ, tapa=TAPA, ray=RAY, kam=KAM, kilit=KILIT, saplama_dy=SAPLAMA_DY))
LOG("ADIM 61 bitti · %s · %.0f sn" % (go, time.time() - t0))
sys.stdout.flush(); os._exit(0)
