# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 64 · TOPPING: HAZIR ÜRÜNLER BİZİM BRAKETLE / VİDAYLA BAĞLI (5 Eki 2026 · Claude · bulut oturumu · TOPPING montaj v6)
python 64_hazir_baglanti.py girdi.glb cikti.glb      (zincir: hat3_v10e.glb → hat3_v10f.glb)

Kemal (5 Eki): hazır ürünlere dokunma, bağlantı BİZİM taraftan basit parçayla; küçük kararları sorma (KURALLAR §3).
  · Kaset motorları (kaşar, sucuk; flanşı gövdeden yalnız 3 mm büyük → flanşa vida yeri yok): gövdenin iki yanında soğuk oda arka dış sacına
      (arka yüz z −630) KAYNAKLI 3 mm L braket + dolgu pulu (flanşın arkasında motor gövdesine dayanır) · 1 × ISO 4762 M5 × 16 + pul yandan motor gövdesine
      (motor siparişinde: gövde iki yanında M5 dişli delik). Braket flanş ve POM burcun dışından dolaşır.
  · Valf adası (havada duruyordu: önü z −660, duvarın arkası z −630, arası BOŞ): iki 3 mm Z braket — ayağı duvara kaynaklı, öbür ayağı valf adasının
      ön yüzüne 1 × M5 × 12 (valf adası siparişinde: ön yüzde 2 × M5 dişli delik). Servis sacı sökülünce valf yerinde kalır.
  · X ekseni (hazır ünite): ray tabanının arka (z −415) ve ön (z −5) duvarına 2 + 2 tabana kaynaklı L pabuç, 1 × M5 × 10 → ray tabanındaki M5 perçin
      somuna (ünite siparişinde) · X motoru ünitenin parçası (üretici bağlantısı).
  · Orta kayıt (kanat dayama dikmesi + alt POM takozu): model verisinde kapakla döner (kpk) → kanadın parçası; gövdeye BAĞLANMAZ.
  · Gizli menteşeler: yan sacta gömme başlı PEM FHS-M4 saplama (2 × menteşe; baş dış yüzeyle aynı), menteşe gövdesinden geçer, iç yüzde pul + fiberli somun.
  · X sensör braketleri: alt saca preslenmiş PEM FHS-M3 saplama, braketin üst ucundaki M3 dişe.
  · Bas-aç mandalları: çerçeve deliğine GEÇME ürün (kendi somunuyla) → değişiklik yok, denetimde "geçme".
  · AÇIK (sonraki iş): kıyma silindirinin duvar flanşı (evaporatör cebinin içinde, halka flanş — üretici çizimi gerek) · iç elektrik kanalları /
      braketleri / 1 rakor 1–10 mm havada → kuyruk 10 (elektrik) ile birlikte.
Denetim (bu betikte): her braket / baş / somun / pul / kaynak hacmi boş · her vida ürünü deler (delik_ac kaydında)."""
import os, sys, time, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb
import cadquery as cq

gi, go = sys.argv[1:3]
t0 = time.time(); LOG = SE.log
HERE = os.path.dirname(os.path.abspath(__file__))
ISO = {"M4": dict(dk=7.0, k=4.0, pul=(9.0, 0.8), somun=(7.0, 3.2)),
       "M5": dict(dk=8.5, k=5.0, pul=(10.0, 1.0), somun=(8.0, 4.7)),
       "M6": dict(dk=10.0, k=6.0, pul=(12.0, 1.6), somun=(10.0, 5.2))}
T3 = 3.0


def kutu(lo, hi):
    lo = np.array(lo, float); hi = np.array(hi, float)
    return cq.Workplane("XY").box(*(hi - lo), centered=False).translate(tuple(lo)).val()


def sil(o, d, t0, t1, r):
    o = np.array(o, float); d = np.array(d, float); a = o + d * min(t0, t1)
    return cq.Solid.makeCylinder(r, abs(t1 - t0), cq.Vector(*a), cq.Vector(*d))


def prizma(pts, v):
    w = cq.Wire.makePolygon([cq.Vector(*p) for p in pts], close=True)
    return cq.Solid.extrudeLinear(cq.Face.makeFromWires(w), cq.Vector(*v))


def kbox(o, d, t0, t1, r):
    o = np.array(o, float); d = np.array(d, float); a = o + d * t0; b = o + d * t1
    ax = int(np.argmax(np.abs(d))); lo = np.minimum(a, b) - r; hi = np.maximum(a, b) + r
    lo[ax] = min(a[ax], b[ax]); hi[ax] = max(a[ax], b[ax])
    return (lo, hi)


BRK, VIDA, PUL, SOM, KAY = [], [], [], [], []


def vida(ad, o, d, M, t_bas, t_uc, bom, somun_t=None):
    """o: baş oturma noktası (pul bu yüzde) · d: vida yönü (baştan uca) · t_bas/t_uc kullanılmaz (uyumluluk) · gövde o → o + d·L"""
    I = ISO[M]; dm = float(M[1:]); L = t_uc
    pul = sil(o, -np.array(d), 0, I['pul'][1], I['pul'][0] / 2)
    bas = sil(o, -np.array(d), I['pul'][1], I['pul'][1] + I['k'], I['dk'] / 2)
    gov = sil(o, d, 0, L, dm / 2)
    VIDA.append(dict(ad=ad, sh=bas.fuse(gov), bom=[bom], kutu=kbox(o, -np.array(d), I['pul'][1] + 0.01, I['pul'][1] + I['k'], I['dk'] / 2)))
    PUL.append(dict(ad=ad + "_pul", sh=pul, bom=["ISO 7089 pul %s A2" % M], kutu=kbox(o, -np.array(d), 0.01, I['pul'][1], I['pul'][0] / 2)))
    if somun_t is not None:                                                   # somun + pul: o + d·somun_t yüzünde
        q = np.array(o) + np.array(d) * somun_t
        pul2 = sil(q, d, 0, I['pul'][1], I['pul'][0] / 2)
        som = sil(q, d, I['pul'][1], I['pul'][1] + I['somun'][1], I['somun'][0] / 2)
        PUL.append(dict(ad=ad + "_somun_pul", sh=pul2, bom=["ISO 7089 pul %s A2" % M], kutu=kbox(q, d, 0.01, I['pul'][1], I['pul'][0] / 2)))
        SOM.append(dict(ad=ad + "_somun", sh=som, bom=["ISO 10511 fiberli somun %s A2" % M], kutu=kbox(q, d, I['pul'][1] + 0.01, I['pul'][1] + I['somun'][1], I['somun'][0] / 2)))


# ---------------------------------------------------------------- kaset motorları
# (ad, motor gövdesi yan yüzü x, yön s (−1 sol / +1 sağ), burç / flanş dış kenarı x, y bandı)
MOTOR = [("kasar_sol", 2063.5, -1, 2059.3, (1180.0, 1210.0)), ("kasar_sag", 2113.5, +1, 2118.6, (1180.0, 1210.0)),
         ("sucuk_sol", 2335.5, -1, 2331.3, (1195.0, 1225.0)), ("sucuk_sag", 2385.5, +1, 2390.6, (1310.0, 1340.0))]
ZD, ZA, ZF = -630.0, -716.0, -672.0                                          # duvar arka yüzü · braket arka ucu · dolgunun önü (flanş arkası −670)
for ad, xm, s, xb, (y0, y1) in MOTOR:
    xl0 = xb; xl1 = xb + s * T3                                              # bacak (burç / flanş dışında)
    ayak = kutu((min(xl1, xl1 + s * 22), y0, ZD - T3), (max(xl1, xl1 + s * 22), y1, ZD))
    bacak = kutu((min(xl0, xl1), y0, ZA), (max(xl0, xl1), y1, ZD))
    dolgu = kutu((min(xm, xb), y0, ZA), (max(xm, xb), y1, ZF))
    yv, zv = (y0 + y1) / 2, -694.0
    br = cq.Workplane("XY").add(ayak).union(cq.Workplane("XY").add(bacak)).union(cq.Workplane("XY").add(dolgu)).cut(
        cq.Workplane("XY").add(sil((xl1, yv, zv), (-s, 0, 0), 0, abs(xl1 - xm), 2.75)))
    BRK.append(dict(ad="motor_%s_braket" % ad, sh=br.val(), bom=["Motor braketi AISI 304 3 mm L + dolgu (lazer + büküm, duvara TIG)"],
                    kutular=[((min(xl1, xl1 + s * 22), y0, ZD - T3), (max(xl1, xl1 + s * 22), y1, ZD)), ((min(xl0, xl1), y0, ZA), (max(xl0, xl1), y1, ZD)),
                             ((min(xm, xb), y0, ZA), (max(xm, xb), y1, ZF))]))
    vida("motor_%s_vida" % ad, (xl1, yv, zv), (-s, 0, 0), "M5", 0, 16.0, "ISO 4762 cıvata M5 × 16 A2-70 (motor gövdesindeki M5 dişli deliğe)")
    xo = xl1 + s * 22
    KAY.append(dict(ad="motor_%s_kaynak" % ad, sh=prizma([(xo, y0, ZD), (xo + s * 3, y0, ZD), (xo, y0, ZD - 3)], (0, y1 - y0, 0)),
                    bom=["TIG 141 köşe dikişi a 2 · ER308LSi · 30 mm · motor braketi ↔ soğuk oda arka dış sacı"],
                    kutu=((min(xo, xo + s * 3), y0, ZD - 3), (max(xo, xo + s * 3), y1, ZD))))

# ---------------------------------------------------------------- valf adası
for ad, x0 in (("sol", 1710.0), ("sag", 1960.0)):
    x1 = x0 + 30.0
    ayak_d = kutu((x0, 1290.0, ZD - T3), (x1, 1310.0, ZD))                    # duvar ayağı
    govde = kutu((x0, 1290.0, -657.0), (x1, 1293.0, ZD - T3))                 # gövde
    ayak_v = kutu((x0, 1260.0, -660.0), (x1, 1293.0, -657.0))                # valf ayağı (ön yüz z −660)
    xc = (x0 + x1) / 2
    br = cq.Workplane("XY").add(ayak_d).union(cq.Workplane("XY").add(govde)).union(cq.Workplane("XY").add(ayak_v)).cut(
        cq.Workplane("XY").add(sil((xc, 1272.0, -657.0), (0, 0, -1), 0, 3.0, 2.75)))
    BRK.append(dict(ad="valf_adasi_braket_%s" % ad, sh=br.val(), bom=["Valf adası Z braketi AISI 304 3 mm (lazer + 2 büküm, duvara TIG)"],
                    kutular=[((x0, 1290.0, ZD - T3), (x1, 1310.0, ZD)), ((x0, 1290.0, -657.0), (x1, 1293.0, ZD - T3)), ((x0, 1260.0, -660.0), (x1, 1293.0, -657.0))]))
    vida("valf_adasi_%s_vida" % ad, (xc, 1272.0, -657.0), (0, 0, -1), "M5", 0, 12.0, "ISO 4762 cıvata M5 × 12 A2-70 (valf adası ön yüzündeki M5 dişli deliğe)")
    KAY.append(dict(ad="valf_adasi_braket_%s_kaynak" % ad, sh=prizma([(x0, 1310.0, ZD), (x0, 1313.0, ZD), (x0, 1310.0, ZD - 3)], (30.0, 0, 0)),
                    bom=["TIG 141 köşe dikişi a 2 · ER308LSi · 30 mm · valf braketi ↔ soğuk oda arka dış sacı"],
                    kutu=((x0, 1310.0, ZD - 3), (x1, 1313.0, ZD))))

# ---------------------------------------------------------------- L pabuç (ürünün yan yüzüne vida) — genel
def pabuc(ad, eks, s, yuz, taban_ax, taban, tsg, merkez, en, boy_ayak, boy_kol, M, L, bom_urun):
    """eks: ürün yüzünün normal ekseni (0/1/2) · s: yüzün dış yönü (+1/−1) · yuz: yüz koordinatı · taban_ax / taban / tsg: pabucun oturduğu yüzey
    (ekseni, koordinatı, dışa yönü: ayak taban + tsg·3 arası) · merkez: diğer eksendeki pabuç merkezi · en: pabuç genişliği"""
    o = [i for i in range(3) if i not in (eks, taban_ax)][0]
    def k(e_lo, e_hi, t_lo, t_hi, o_lo, o_hi):
        lo = [0, 0, 0]; hi = [0, 0, 0]
        lo[eks], hi[eks] = min(e_lo, e_hi), max(e_lo, e_hi); lo[taban_ax], hi[taban_ax] = min(t_lo, t_hi), max(t_lo, t_hi); lo[o], hi[o] = o_lo, o_hi
        return lo, hi
    olo, ohi = merkez - en / 2, merkez + en / 2
    ay = k(yuz, yuz + s * boy_ayak, taban, taban + tsg * T3, olo, ohi)          # ayak tabanda, yüzden dışarı
    ko = k(yuz, yuz + s * T3, taban + tsg * T3, taban + tsg * boy_kol, olo, ohi)  # dik kol yüze dayanır
    vt = taban + tsg * (T3 + (boy_kol - T3) / 2)                              # vida taban ekseni kotu
    c = [0, 0, 0]; c[eks] = yuz + s * T3; c[taban_ax] = vt; c[o] = merkez
    d = [0, 0, 0]; d[eks] = -s
    br = cq.Workplane("XY").add(kutu(*ay)).union(cq.Workplane("XY").add(kutu(*ko))).cut(cq.Workplane("XY").add(sil(c, d, 0, T3, ISO[M]['pul'][0] / 2 * 0 + float(M[1:]) * 0.55)))
    lo = np.minimum(np.array(ay[0]), np.array(ko[0])); hi = np.maximum(np.array(ay[1]), np.array(ko[1]))
    BRK.append(dict(ad=ad, sh=br.val(), bom=["Bağlama pabucu AISI 304 3 mm L (lazer + 1 büküm), tabana TIG"], kutular=[ay, ko]))
    vida(ad + "_vida", c, d, M, 0, L, "ISO 4762 cıvata %s × %d A2-70 (%s)" % (M, L, bom_urun))
    # kaynak: ayağın dış ucunda tabanla köşe
    e = yuz + s * boy_ayak
    p1 = [0, 0, 0]; p2 = [0, 0, 0]; p3 = [0, 0, 0]
    for q in (p1, p2, p3): q[o] = olo
    p1[eks], p1[taban_ax] = e, taban; p2[eks], p2[taban_ax] = e + s * 3, taban; p3[eks], p3[taban_ax] = e, taban + tsg * 3
    v = [0, 0, 0]; v[o] = en
    klo = [0, 0, 0]; khi = [0, 0, 0]
    klo[eks], khi[eks] = min(e, e + s * 3), max(e, e + s * 3); klo[taban_ax], khi[taban_ax] = min(taban, taban + tsg * 3), max(taban, taban + tsg * 3); klo[o], khi[o] = olo, ohi
    KAY.append(dict(ad=ad + "_kaynak", sh=prizma([tuple(p1), tuple(p2), tuple(p3)], tuple(v)), bom=["TIG 141 köşe dikişi a 2 · ER308LSi · %.0f mm · %s ↔ taban" % (en, ad)],
                    kutu=(klo, khi)))


# X ekseni ray tabanı: arka duvar dış yüzü z −415, ön duvar dış yüzü z −5 · taban (dış taban üstü) y 893,5 · ray tabanının bu noktalarında M5 dişli (perçin somun)
for x in (1600.0, 2200.0):
    pabuc("x_ekseni_pabuc_arka_%d" % x, 2, -1, -415.0, 1, 893.5, +1, x, 30.0, 25.0, 14.5, "M5", 10.0, "X ekseni ray tabanı arka duvarındaki M5 perçin somuna")
for x in (1550.0, 2400.0):
    pabuc("x_ekseni_pabuc_on_%d" % x, 2, +1, -5.0, 1, 893.5, +1, x, 30.0, 25.0, 14.5, "M5", 10.0, "X ekseni ray tabanı ön duvarındaki M5 perçin somuna")
# Orta kayıt (dikme + alt POM takozu): model verisinde KAPAKLA DÖNER (kpk) → kanadın parçası, gövdeye bağlanmaz (animasyonda kanatla gelir)

# ---------------------------------------------------------------- menteşeler: yan sacta gömme başlı PEM saplama (dışta yüzeyle aynı), içte pul + somun
ISO["M3"] = dict(dk=5.5, k=3.0, pul=(7.0, 0.5), somun=(5.5, 2.4))
SAPLAMA = []
for ad, xd, xi, s in (("sol", 1436.0, 1465.0, +1), ("sag", 2500.0, 2471.0, -1)):
    for y in (910.0, 947.0):
        o = np.array([xd, y, 32.5]); d = np.array([s, 0.0, 0.0])
        L = abs(xi - xd) + 0.8 + 3.2 + 1.0
        st = sil(o, d, 0, L, 2.0).fuse(sil(o, d, 0, 1.0, 3.5))                 # gövde Ø4 + gömme baş Ø7 × 1
        SAPLAMA.append(dict(ad="mentese_%s_%d_saplama" % (ad, y), sh=st, bom=["PEM FHS-M4 gömme başlı saplama (yan saca preslenir)"], kutu=None))
        q = o + d * abs(xi - xd)
        PUL.append(dict(ad="mentese_%s_%d_pul" % (ad, y), sh=sil(q, d, 0, 0.8, 4.5), bom=["ISO 7089 pul M4 A2"], kutu=kbox(q, d, 0.01, 0.8, 4.5)))
        SOM.append(dict(ad="mentese_%s_%d_somun" % (ad, y), sh=sil(q, d, 0.8, 4.0, 3.5), bom=["ISO 10511 fiberli somun M4 A2"], kutu=kbox(q, d, 0.81, 4.0, 3.5)))
# X sensör braketleri: alt sacın altına asılı (üst ucu y 1109 sacın alt yüzünde) → sacta PEM FHS-M3 saplama aşağı, braketin dişli üst deliğine
for i, (x, z) in enumerate(((1454.05, -330.0), (1454.05, -20.0))):
    o = np.array([x, 1110.5, z]); d = np.array([0.0, -1.0, 0.0])
    st = sil(o, d, 0, 10.0, 1.5).fuse(sil(o, d, 0, 1.0, 2.75))
    SAPLAMA.append(dict(ad="x_sensor_braket_%d_saplama" % i, sh=st, bom=["PEM FHS-M3 gömme başlı saplama (alt saca preslenir) → braketin M3 dişine"], kutu=None))

g = Glb(gi)
MN, MX, AD = [], [], []
for p in g.prims:
    if p.get("gizli") or p["pr"].get("mode", 4) != 4: continue
    P = p["X"][p["T"]]; m = np.all(P.max(1) >= [800, 850, -850], 1) & np.all(P.min(1) <= [2560, 2250, 60], 1)
    MN.append(P[m].min(1)); MX.append(P[m].max(1)); AD += [p["name"]] * int(m.sum())
MN = np.concatenate(MN); MX = np.concatenate(MX); AD = np.array(AD)


def bos(lo, hi, pay=0.3):
    lo = np.array(lo) + pay; hi = np.array(hi) - pay
    m = np.all(MX > lo, 1) & np.all(MN < hi, 1)
    return sorted(set(AD[m]))


for L in (BRK, PUL, SOM, KAY):
    for p in L:
        for kk in (p.get("kutular") or [p["kutu"]]):
            dd = bos(*kk)
            assert not dd, "ADIM 64 DUR: %s hacmi dolu %s %s" % (p["ad"], kk, dd)
for p in VIDA:
    dd = bos(*p["kutu"])
    assert not dd, "ADIM 64 DUR: %s başı dolu %s" % (p["ad"], dd)
K = SE.Karsi(g, acik_dene=True)
kayit = K.delik_ac(VIDA + SAPLAMA)
delinen = set(a for k in kayit for a in k.get("eleman", []))
eks = sorted(set(p["ad"] for p in VIDA + SAPLAMA) - delinen)
assert not eks, "ADIM 64 DUR: hiçbir şeyi delmeyen vida %s" % eks
LOG("  %d vida · %d delik kaydı" % (len(VIDA), len(kayit)))
tmp = go + ".e1.glb"; g.kaydet(tmp); del g, K
H = SE.Ham(tmp)
PAR = [("TOPPING_BRAKET__paslanmaz", "TOPPING_GOVDE__sac", BRK), ("TOPPING_BRAKET__kaynak", "TOPPING_GOVDE__sac", KAY),
       ("TOPPING_BRAKET__vida", "U_F_GOVDE__paslanmaz", VIDA + SAPLAMA + PUL + SOM)]
TUM = {}
for d, sb, L in PAR:
    if not L: continue
    H.koy(d, L, kat=0, mek=7, sablon=sb)
    TUM[d] = L
H.yaz(tmp + ".e2.glb")
SE.sikistir(tmp + ".e2.glb", go)
for f in (tmp, tmp + ".e2.glb"): os.remove(f)
for d in TUM: H.aralik[d] = {p["ad"]: (0, 0) for p in TUM[d]}
SE.ent_json(go[:-4] + "_ent.json", "TOPPING_HAZIR_BAGLANTI", [(d, TUM[d]) for d in sorted(TUM)], H.aralik, lambda a: False, "TOPPING/Gövde", (), kayit,
            ek=dict(motor=MOTOR))
LOG("ADIM 64 bitti · %s · %d braket · %d vida · %d saplama · %.0f sn" % (go, len(BRK), len(VIDA), len(SAPLAMA), time.time() - t0))
sys.stdout.flush(); os._exit(0)
