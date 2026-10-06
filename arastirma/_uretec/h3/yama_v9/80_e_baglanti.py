# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 80 · E KAPILARI + EMNİYET SENSÖRLERİ BAĞLI (6 Eki 2026 · Claude · bulut oturumu · E montaj v2, KURALLAR §2.3 kural 10 / §5 bağlantı denetimi)
python 80_e_baglanti.py girdi.glb cikti.glb      (zincir: hat3_v10k.glb → hat3_v10l.glb)

E montaj v2 bağlantı denetimi: kapı ve sensör parçaları yerinde duruyor ama hiçbir bağlantı elemanı değmiyordu.
  1 · Üst sol kapı emniyet sensörü + aktüatörü (adım 59) E gövdesinin üstünde, U tabanının önünde (y 1864–1936) duruyordu — U E'den sonra gelir,
      arkasında E'ye ait yüzey yok. Diğer sol sensörlerle aynı düzene taşındı: orta dikmenin solu, x −20 · y −100 (y 1764–1836).
  2 · Sensör braketleri (adım 59, 3 adet) yalnız ara takozdu: sensöre değmiyor (2,8 mm), dikmeye yalnız kenarıyla değiyor, kaynak / vida yok.
      Kaldırıldı. Her sensöre 1,5 mm AISI 304 L braket: yan kol orta dikmenin yan yüzünde (TIG köşe dikişi, kolun ön ucu ↔ dikme), arka kol
      sensörün arkasında (z 24,5–26), arka kolda 2 × PEM S-M4-2 (arka yüz). Sensör önden kendi montaj deliklerinden 2 × ISO 4762 M4 × 20.
  3 · Aktüatörler (4) kapı iç tavasının arka yüzüne oturuyordu, vidasız: iç tavaya 2 × PEM S-M4-1 (gövde iki tava arasında), aktüatör
      arkasından 2 × DIN 7991 M4 × 16 (havşa baş aktüatör gövdesine gömülü — sensörle 3 mm arada baş çıkıntısı yok).
  4 · Kapı menteşe kanatları (12) ve bas-aç karşılık plakaları (6) iç tavanın ön yüzüne düz oturuyordu: her birine 2 punta (iç tavaya).
  5 · Şarjör yan kapısı: dış sac ↔ iç tava kenarı 6 punta.
Denetim (bu betikte): taşınan / silinen bileşenler beklenen kutuda · braket, PEM, kaynak hacmi boş · her vida kendi sensörünü / aktüatörünü deler ·
punta işaretleri iki sacın temas yüzeyinde."""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb
import cadquery as cq

gi, go = sys.argv[1:3]
t0 = time.time(); LOG = SE.log
T = 1.5
SEN = {"ALT_SOL": (4812.5, 164.0, "sol"), "UST_SOL": (4812.5, 1764.0, "sol"), "ALT_SAG": (4883.5, 164.0, "sag"), "UST_SAG": (4883.5, 864.0, "sag")}   # x0, y0 (25 × 72)
DIKME = {"sol": 4841.5, "sag": 4881.5}                                           # orta dikme yan yüzleri (profil 40: x 4841,5–4881,5)
ZS0, ZS1, ZA0, ZA1 = 26.0, 44.0, 47.0, 59.0                                      # sensör z · aktüatör z (iç tava arka yüzü 59)


def kutu(lo, hi):
    lo = np.array(lo, float); hi = np.array(hi, float)
    return cq.Workplane("XY").box(*(hi - lo), centered=False).translate(tuple(lo)).val()


def silz(x, y, z0, z1, r):
    return cq.Solid.makeCylinder(r, abs(z1 - z0), cq.Vector(x, y, min(z0, z1)), cq.Vector(0, 0, 1))


def silx(x0, x1, y, z, r):
    return cq.Solid.makeCylinder(r, abs(x1 - x0), cq.Vector(min(x0, x1), y, z), cq.Vector(1, 0, 0))


def prizma(pts, v):
    w = cq.Wire.makePolygon([cq.Vector(*p) for p in pts], close=True)
    return cq.Solid.extrudeLinear(cq.Face.makeFromWires(w), cq.Vector(*v))


g = Glb(gi)


def bul(dug, lo, hi):
    g.bilesen(dug, no=0)
    return [b for b in g._bc[dug] if np.all(b["lo"] >= np.array(lo) - 0.6) and np.all(b["hi"] <= np.array(hi) + 0.6)]


# ---- 1 · üst sol sensör + aktüatör taşınır
D_ = np.array([-20.0, -100.0, 0.0])
for dug, z0, z1 in (("EMNIYET__sari", ZS0, ZS1), ("EMNIYET__siyah", ZA0, ZA1)):
    L = bul(dug, (4832.5, 1864.0, z0), (4857.5, 1936.0, z1))
    assert len(L) == 1, "ADIM 80 DUR: üst sol %s bileşeni %d" % (dug, len(L))
    g.donustur(L[0], lambda P: P + D_)
    g._bc.pop(dug, None)
    LOG("  üst sol %s → x −20 · y −100" % dug)
# sağdaki iki sensör + aktüatör dikmeye 1,0 mm'ydi → +1 mm sağa (1,5 mm braket kolu + 0,5 boşluk)
for dug, z0, z1 in (("EMNIYET__sari", ZS0, ZS1), ("EMNIYET__siyah", ZA0, ZA1)):
    for y0 in (164.0, 864.0):
        L = bul(dug, (4882.5, y0, z0), (4907.5, y0 + 72.0, z1))
        assert len(L) == 1, "ADIM 80 DUR: sağ %s y %.0f bileşeni %d" % (dug, y0, len(L))
        g.donustur(L[0], lambda P: P + np.array([1.0, 0.0, 0.0]))
        g._bc.pop(dug, None)
    LOG("  sağ %s × 2 → x +1" % dug)
# ---- 2 · eski braket takozları silinir
L = bul("EMNIYET__paslanmaz", (4835.0, 160.0, 25.0), (4884.0, 940.0, 45.0))
assert len(L) == 3, "ADIM 80 DUR: eski E braketi %d (3 bekleniyor)" % len(L)
for b in L: g.sil_b(b)
g._bc.pop("EMNIYET__paslanmaz", None)
LOG("  eski braket takozu silindi × 3")
tmp0 = go + ".e0.glb"; g.kaydet(tmp0); del g                                    # taşınan bileşenler yeniden okunsun (bileşen önbelleği)
g = Glb(tmp0); os.remove(tmp0)
BRK, KAY, PEM, VIDA = [], [], [], []
for ad, (x0, y0, yan) in SEN.items():
    x1, y1 = x0 + 25.0, y0 + 72.0; xc, yc = (x0 + x1) / 2, (y0 + y1) / 2
    xd = DIKME[yan]
    if yan == "sol":
        kol = ((xd - T, y0 + 2, ZS0 - T), (xd, y1 - 2, 42.0)); arka = ((x0 + 2, y0 + 2, ZS0 - T), (xd, y1 - 2, ZS0))
        dik = prizma([(xd, y0 + 2, 42.0), (xd - T, y0 + 2, 42.0), (xd, y0 + 2, 42.0 + T)], (0, 68.0, 0))
        dik_k = ((xd - T, y0 + 2, 42.0), (xd, y1 - 2, 42.0 + T))
    else:
        kol = ((xd, y0 + 2, ZS0 - T), (xd + T, y1 - 2, 42.0)); arka = ((xd, y0 + 2, ZS0 - T), (x1 - 2, y1 - 2, ZS0))
        dik = prizma([(xd, y0 + 2, 42.0), (xd, y0 + 2, 42.0 + T), (xd + T, y0 + 2, 42.0)], (0, 68.0, 0))
        dik_k = ((xd, y0 + 2, 42.0), (xd + T, y1 - 2, 42.0 + T))
    br = cq.Workplane("XY").add(kutu(*kol)).union(cq.Workplane("XY").add(kutu(*arka)))
    YV = (yc - 25.0, yc + 25.0)
    for y in YV: br = br.cut(cq.Workplane("XY").add(silz(xc, y, ZS0 - T - 0.5, ZS0 + 0.5, 2.9)))
    BRK.append(dict(ad="emniyet_E_%s_braket" % ad, sh=br.val(), bom=["Emniyet sensörü braketi AISI 304 1,5 mm L (lazer + 1 büküm, orta dikmeye TIG, 2 × PEM S-M4-2)"],
                    kutular=[kol, arka]))
    KAY.append(dict(ad="emniyet_E_%s_braket_kaynak" % ad, sh=dik, bom=["TIG 141 köşe dikişi a 1,5 · ER308LSi · 68 mm · emniyet braketi ↔ orta dikme"], kutular=[dik_k]))
    for i, y in enumerate(YV):
        som = silz(xc, y, ZS0 - T - 3.0, ZS0 - T, 3.95).fuse(silz(xc, y, ZS0 - T, ZS0, 2.9))
        som = cq.Workplane("XY").add(som).cut(cq.Workplane("XY").add(silz(xc, y, ZS0 - T - 3.5, ZS0 + 0.5, 1.7))).val()
        PEM.append(dict(ad="emniyet_E_%s_%d_somun" % (ad, i), sh=som, bom=["PEM S-M4-2 preslenmiş somun (braketin arka koluna)"],
                        kutular=[((xc - 3.95, y - 3.95, ZS0 - T - 3.0), (xc + 3.95, y + 3.95, ZS0 - T))]))
        VIDA.append(dict(ad="emniyet_E_%s_%d_vida" % (ad, i), sh=silz(xc, y, ZS1 - 4.0, ZS1, 3.5).fuse(silz(xc, y, ZS0 - T - 3.0, ZS1 - 4.0, 2.0)),
                         bom=["ISO 4762 cıvata M4 × 20 A2-70 (RSS36 montaj deliğinden, gömme yuvada)"]))
    # aktüatör: iç tavaya PEM S-M4-1 (gövde tavanın ön yüzünde, iki tava arasında) + arkadan DIN 7991 M4 × 16 (havşa baş aktüatöre gömülü)
    for i, y in enumerate(YV):
        som = silz(xc, y, ZA1 + 1.0, ZA1 + 3.5, 3.95).fuse(silz(xc, y, ZA1, ZA1 + 1.0, 2.9))
        som = cq.Workplane("XY").add(som).cut(cq.Workplane("XY").add(silz(xc, y, ZA1 - 0.5, ZA1 + 4.0, 1.7))).val()
        PEM.append(dict(ad="emniyet_E_%s_aktuator_%d_somun" % (ad, i), sh=som, bom=["PEM S-M4-1 preslenmiş somun (kapı iç tavası)"],
                        kutular=[((xc - 3.95, y - 3.95, ZA1 + 1.0), (xc + 3.95, y + 3.95, ZA1 + 3.5))]))
        bas = cq.Solid.makeCone(4.0, 2.0, 2.0, cq.Vector(xc, y, ZA0), cq.Vector(0, 0, 1))
        VIDA.append(dict(ad="emniyet_E_%s_aktuator_%d_vida" % (ad, i), sh=bas.fuse(silz(xc, y, ZA0, ZA0 + 16.0, 2.0)),
                         bom=["DIN 7991 havşa başlı cıvata M4 × 16 A2-70 (aktüatör arkasından, kapı iç tavasındaki preslenmiş somuna)"]))
# ---- 4 · punta: menteşe kanatları + karşılıklar ↔ iç tava ön yüzü (z 60)
PUN = []
def punta(ad, x, y, z0, z1, eks="z", r=2.5):
    sh = silz(x, y, z0, z1, r) if eks == "z" else silx(z0, z1, x, y, r)
    PUN.append(dict(ad=ad, sh=sh, bom=["Punta kaynağı (direnç) Ø5"]))
for kenar, xs in (("sol", (4410.0, 4441.5)), ("sag", (5188.5, 5220.0))):
    for i, (yl, yh) in enumerate(((295, 365), (525, 595), (675, 745), (895, 965), (1355, 1425), (1745, 1815))):
        k = "%s_%s" % ("alt" if i < 3 else "ust", kenar)
        L = bul("E_GOVDE__on_seffaf", (xs[0], yl, 57.0), (xs[1], yh, 71.0))
        assert L, "ADIM 80 DUR: menteşe kanadı yok %s %d" % (kenar, i)
        for j, f in enumerate((0.3, 0.7)):
            punta("onyuz_kapak_E_%s_punta_mentese_%d_%d" % (k, i, j), xs[0] + (xs[1] - xs[0]) * 0.5, yl + (yh - yl) * f, 59.6, 60.4)
for k, x0, x1, ys in (("alt_sol", 4842.0, 4855.5, (700,)), ("alt_sag", 4867.5, 4881.0, (700,)), ("ust_sol", 4842.0, 4855.5, (1700,)), ("ust_sag", 4867.5, 4881.0, (1000, 1700))):
    for y0 in ys:
        for j, f in enumerate((0.25, 0.75)):
            punta("onyuz_kapak_E_%s_punta_karsilik_%d_%d" % (k, y0, j), (x0 + x1) / 2, y0 + 30 * f, 59.6, 61.0)
# ---- 5 · şarjör yan kapısı: dış sac (x 5228,5) ↔ iç tava kenarı (x ≤ 5228,5) · 6 punta (tava kenar şeridi üstünde)
L = bul("E_GOVDE__sac", (5215.5, 236.0, -812.0), (5228.5, 984.0, -420.0))
assert len(L) >= 1, "ADIM 80 DUR: şarjör kapısı iç tavası yok"
Pt = np.concatenate([np.concatenate([p["X"][p["T"][t]] for p, t in b["parca"]]) for b in L]).reshape(-1, 3)
kenar = Pt[Pt[:, 0] > 5228.3]
assert len(kenar) > 8, "ADIM 80 DUR: iç tava dış sac temas kenarı yok"
for j, (y, z) in enumerate(((236.0, -700.0), (236.0, -520.0), (984.0, -700.0), (984.0, -520.0), (500.0, -812.0), (720.0, -420.0))):
    q = kenar[np.argmin(np.hypot(kenar[:, 1] - y, kenar[:, 2] - z))]                    # hedefe en yakın kenar noktası (temas şeridi)
    punta("sarjor_yan_kapisi_punta_%d" % j, q[1], q[2], 5228.1, 5228.9, eks="x")
# ---- hacim denetimi (braket / PEM / kaynak boş)
MN, MX, AD = [], [], []
for p in g.prims:
    if p.get("gizli") or p["pr"].get("mode", 4) != 4: continue
    P = p["X"][p["T"]]; ar = np.linalg.norm(np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]), axis=1)
    m = (ar > 1e-9) & np.all(P.max(1) >= [4800, 150, 15], 1) & np.all(P.min(1) <= [4920, 1850, 70], 1)
    MN.append(P[m].min(1)); MX.append(P[m].max(1)); AD += [p["name"]] * int(m.sum())
MN = np.concatenate(MN); MX = np.concatenate(MX); AD = np.array(AD)


def bos(lo, hi, pay=0.3):
    lo = np.array(lo) + pay; hi = np.array(hi) - pay
    return sorted(set(AD[np.all(MX > lo, 1) & np.all(MN < hi, 1)]))


for L_ in (BRK, KAY, PEM):
    for p in L_:
        for k in p.get("kutular", []):
            d = bos(*k)
            assert not d, "ADIM 80 DUR: %s hacmi dolu %s %s" % (p["ad"], k, d)
for lo_, hi_ in (((4812.5, 1764.0, ZS0), (4837.5, 1836.0, ZS1)), ((4812.5, 1764.0, ZA0), (4837.5, 1836.0, ZA1)),
                 ((4883.5, 164.0, ZS0), (4908.5, 236.0, ZA1)), ((4883.5, 864.0, ZS0), (4908.5, 936.0, ZA1))):
    d = [x for x in bos(lo_, hi_) if not x.startswith("EMNIYET__")]
    assert not d, "ADIM 80 DUR: taşınan üst sol sensör / aktüatör hacmi dolu %s" % d
K = SE.Karsi(g, acik_dene=True)
kayit = K.delik_ac(VIDA)
delinen = set(a for k in kayit for a in k.get("eleman", []))
assert delinen == set(p["ad"] for p in VIDA), "ADIM 80 DUR: karşı parçaya girmeyen vida %s" % sorted(set(p["ad"] for p in VIDA) - delinen)
tmp = go + ".e1.glb"; g.kaydet(tmp); del g, K
H = SE.Ham(tmp)
PAR = [("EMNIYET_E_BRAKET__paslanmaz", "E_GOVDE__sac", BRK), ("EMNIYET_E_BRAKET__kaynak", "E_GOVDE__sac", KAY),
       ("EMNIYET_E_BRAKET__vida", "E_GOVDE__celik", VIDA + PEM), ("E_GOVDE_PUNTA__kaynak", "E_GOVDE__sac", PUN)]
TUM = {}
for d, sb, L_ in PAR:
    H.koy(d, L_, kat=0, mek=38 if d.startswith("EMNIYET") else 32, kpk_fn=lambda a: False, sablon=sb)
    TUM[d] = L_
H.yaz(tmp + ".e2.glb")
SE.sikistir(tmp + ".e2.glb", go)
for f in (tmp, tmp + ".e2.glb"): os.remove(f)
for d in TUM: H.aralik[d] = {p["ad"]: (0, 0) for p in TUM[d]}
SE.ent_json(go[:-4] + "_ent.json", "E_BAGLANTI", [(d, TUM[d]) for d in sorted(TUM)], H.aralik, lambda a: False, "E/Gövde", (), kayit, ek=dict(sensor=SEN))
LOG("ADIM 80 bitti · %s · %d braket · %d vida · %d PEM · %d punta · %.0f sn" % (go, len(BRK), len(VIDA), len(PEM), len(PUN), time.time() - t0))
sys.stdout.flush(); os._exit(0)
