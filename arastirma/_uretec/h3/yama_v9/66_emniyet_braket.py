# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 66 · TOPPING KAPAK EMNİYET SENSÖRLERİ VİDALI BRAKETE (5 Eki 2026 · Claude · bulut oturumu · TOPPING montaj v6)
python 66_emniyet_braket.py girdi.glb cikti.glb      (zincir: hat3_v10g.glb → hat3_v10h.glb)

Bağlantı denetimi (KURALLAR §2.3 kural 10): adım 59'un TOPPING K1 / K2 sensörleri (Schmersal RSS36, x 1892,5 / 2016,5 · y 894–966 · z 6–24) dış tabanın
üstünde (0,5 mm) duruyordu, vida yok. Arkalarında (z 6) boşluk, X ekseni ray tabanının ön duvarı z −5'te.
Çözüm (her sensör): 2 mm AISI 304 L braket — dik kol sensörün arkasında (z 4–6, y 893,5–962), ayak dış tabanın üstünde arkaya (z −2…4), ayağın arka
kenarı tabana TIG (21 mm). Dik kolda 2 × PEM S-M4-2 preslenmiş somun (arka yüzde). Sensör, kendi gövde deliklerinden önden 2 × ISO 4762 M4 × 20 ile
(baş sensörün gömme yuvasında; RSS36 montajı) → braketin PEM somununa. Sensör hazır ürün: yalnız kendi montaj delikleri (gömme yuva) açılır.
Aktüatör kapakta (z 27–39) sensörün 3 mm önünde → vida başı sensör ön yüzünden taşmaz.
Denetim (bu betikte): braket / kaynak / somun hacmi boş · her vida sensörü deler (yoksa durur)."""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb
import cadquery as cq

gi, go = sys.argv[1:3]
t0 = time.time(); LOG = SE.log
SENSOR = [("K1", 1892.5, 1917.5), ("K2", 2016.5, 2041.5)]                     # x aralığı · y 894–966 · z 6–24
YT, ZS, T = 893.5, 6.0, 2.0                                                     # taban üstü · sensör arka yüzü · sac
YV = (905.0, 955.0)                                                             # vida eksenleri (y)


def kutu(lo, hi):
    lo = np.array(lo, float); hi = np.array(hi, float)
    return cq.Workplane("XY").box(*(hi - lo), centered=False).translate(tuple(lo)).val()


def silz(x, y, z0, z1, r):
    return cq.Solid.makeCylinder(r, abs(z1 - z0), cq.Vector(x, y, min(z0, z1)), cq.Vector(0, 0, 1))


def prizma(pts, v):
    w = cq.Wire.makePolygon([cq.Vector(*p) for p in pts], close=True)
    return cq.Solid.extrudeLinear(cq.Face.makeFromWires(w), cq.Vector(*v))


BRK, KAY, SOM, VIDA = [], [], [], []
for ad, x0, x1 in SENSOR:
    bx0, bx1 = x0 + 2.0, x1 - 2.0; xc = (x0 + x1) / 2
    kol = kutu((bx0, YT, ZS - T), (bx1, 962.0, ZS))
    ayak = kutu((bx0, YT, -2.0), (bx1, YT + T, ZS - T))
    br = cq.Workplane("XY").add(kol).union(cq.Workplane("XY").add(ayak))
    for y in YV: br = br.cut(cq.Workplane("XY").add(silz(xc, y, ZS - T - 0.5, ZS + 0.5, 2.9)))   # PEM S-M4 montaj deliği Ø5,8 (somun gövdesi dolduruyor)
    BRK.append(dict(ad="emniyet_%s_braket" % ad, sh=br.val(), bom=["Emniyet sensörü braketi AISI 304 2 mm L (lazer + 1 büküm, tabana TIG, 2 × PEM S-M4-2)"],
                    kutular=[((bx0, YT, ZS - T), (bx1, 962.0, ZS)), ((bx0, YT, -2.0), (bx1, YT + T, ZS - T))]))
    KAY.append(dict(ad="emniyet_%s_braket_kaynak" % ad, sh=prizma([(bx0, YT, -2.0), (bx0, YT, -4.0), (bx0, YT + 2.0, -2.0)], (bx1 - bx0, 0, 0)),
                    bom=["TIG 141 köşe dikişi a 1,5 · ER308LSi · %.0f mm · emniyet braketi ↔ dış taban" % (bx1 - bx0)],
                    kutular=[((bx0, YT, -4.0), (bx1, YT + 2.0, -2.0))]))
    for i, y in enumerate(YV):
        # PEM somun: gövde braket deliğinde (z 4–6), başı arka yüzde (z 1–4, Ø7,9)
        som = silz(xc, y, 1.0, ZS - T, 3.95).fuse(silz(xc, y, ZS - T, ZS, 2.9))
        som = cq.Workplane("XY").add(som).cut(cq.Workplane("XY").add(silz(xc, y, 0.5, ZS + 0.5, 1.7))).val()
        SOM.append(dict(ad="emniyet_%s_%d_somun" % (ad, i), sh=som, bom=["PEM S-M4-2 preslenmiş somun (braketin dik koluna)"],
                        kutular=[((xc - 3.95, y - 3.95, 1.0), (xc + 3.95, y + 3.95, ZS - T))]))
        # vida: baş sensörün gömme yuvasında (z 20–24, Ø7), gövde z 1,5…20
        VIDA.append(dict(ad="emniyet_%s_%d_vida" % (ad, i), sh=silz(xc, y, 20.0, 24.0, 3.5).fuse(silz(xc, y, 1.5, 20.0, 2.0)),
                         bom=["ISO 4762 cıvata M4 × 20 A2-70 (RSS36 montaj deliğinden, gömme yuvada)"]))

g = Glb(gi)
MN, MX, AD = [], [], []
for p in g.prims:
    if p.get("gizli") or p["pr"].get("mode", 4) != 4: continue
    P = p["X"][p["T"]]; m = np.all(P.max(1) >= [1850, 880, -20], 1) & np.all(P.min(1) <= [2080, 980, 40], 1)
    MN.append(P[m].min(1)); MX.append(P[m].max(1)); AD += [p["name"]] * int(m.sum())
MN = np.concatenate(MN); MX = np.concatenate(MX); AD = np.array(AD)


def bos(lo, hi, pay=0.3):
    lo = np.array(lo) + pay; hi = np.array(hi) - pay
    m = np.all(MX > lo, 1) & np.all(MN < hi, 1)
    return sorted(set(AD[m]))


for L in (BRK, KAY, SOM):
    for p in L:
        for k in p["kutular"]:
            d = bos(*k)
            assert not d, "ADIM 66 DUR: %s hacmi dolu %s %s" % (p["ad"], k, d)
K = SE.Karsi(g, acik_dene=True)
kayit = K.delik_ac(VIDA)
for k in kayit: LOG("  delik: %s · −%s mm³" % (k.get("karsi"), k.get("cikan")))
delinen = set(a for k in kayit for a in k.get("eleman", []))
assert delinen == set(p["ad"] for p in VIDA), "ADIM 66 DUR: sensöre girmeyen vida %s" % sorted(set(p["ad"] for p in VIDA) - delinen)
tmp = go + ".e1.glb"; g.kaydet(tmp); del g, K
H = SE.Ham(tmp)
PAR = [("TOPPING_EMNIYET_BRAKET__paslanmaz", "TOPPING_GOVDE__sac", BRK),
       ("TOPPING_EMNIYET_BRAKET__kaynak", "TOPPING_GOVDE__sac", KAY),
       ("TOPPING_EMNIYET_BRAKET__vida", "U_F_GOVDE__paslanmaz", VIDA + SOM)]
TUM = {}
for d, sb, L in PAR:
    H.koy(d, L, kat=0, mek=7, kpk_fn=lambda a: False, sablon=sb)
    TUM[d] = L
H.yaz(tmp + ".e2.glb")
SE.sikistir(tmp + ".e2.glb", go)
for f in (tmp, tmp + ".e2.glb"): os.remove(f)
for d in TUM: H.aralik[d] = {p["ad"]: (0, 0) for p in TUM[d]}
SE.ent_json(go[:-4] + "_ent.json", "TOPPING_EMNIYET", [(d, TUM[d]) for d in sorted(TUM)], H.aralik, lambda a: False, "TOPPING/Gövde", (), kayit,
            ek=dict(sensor=SENSOR, yv=YV))
LOG("ADIM 66 bitti · %s · %d braket · %d vida · %.0f sn" % (go, len(BRK), len(VIDA), time.time() - t0))
sys.stdout.flush(); os._exit(0)
