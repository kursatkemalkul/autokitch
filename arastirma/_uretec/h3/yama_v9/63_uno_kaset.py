# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 63 · TOPPING: UNO'LAR RAFA VİDALI · KASETLER KAPAK TAKOZUYLA KİLİTLİ (5 Eki 2026 · Claude · bulut oturumu · TOPPING montaj v6)
python 63_uno_kaset.py girdi.glb cikti.glb      (zincir: hat3_v10d.glb → hat3_v10e.glb)

Kemal (5 Eki): "UNO rafa vida ile oturacak" · "kasetler rafına oturacak, kilit lazım, tam yerine otursun, çok basit — iki günde bir çıkarılıp takılacak;
satın alınan kasetlere bilye vs. yapamam, direkt kullanabileceğim basit çözüm". Hazır ürünlere (UNO, kaset) DOKUNULMAZ; bağlantı bizim parçalarımızla:
  · UNO (5): taban (rafta 82 mm genişlik) üstünde gövde her yana ~50 mm taşar → tabana yukarıdan basılamaz. Her UNO'nun iki yanında RAFA KAYNAKLI
      3 mm L pabuç (taban 25 × 30, dik kol 12): dik kol UNO tabanının yan yüzüne dayanır, 1 × ISO 4762 M5 × 12 + ISO 7089 pul yandan UNO tabanındaki
      dişli deliğe (UNO üreticisinden: taban iki yanında M5 dişli delik — siparişte istenir). Sol pabuç arkada, sağ pabuç önde (çapraz).
      Gıda tarafı: pabuç rafa sürekli TIG (dış kenar boyunca), rafta somun / açık diş yok. Sökme: 2 vida.
  · Kaset (kaşar, sucuk): yan kanal + arka dayama (motor kaplini) kaseti yerine oturtur; kapak K2'nin iç yüzüne her kasetin önüne POM takoz
      (40 × 40, kaset ön yüzüne 1 mm) → kapak kapanınca kaset yerinde kilitli; kaset tam oturmamışsa kapak kapanmaz ve kapak emniyet anahtarı (adım 59)
      makineyi başlatmaz. Kasette değişiklik yok; dil kanalına ya da yuvaya dokunulmaz.
Denetim (bu betikte): her pabuç / vida / takoz hacmi boş (UNO + raf yüzey teması hariç) · 10 vidanın HEPSİ UNO tabanını deler (yoksa durur)."""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb
import cadquery as cq

gi, go = sys.argv[1:3]
t0 = time.time(); LOG = SE.log
# UNO tabanı (model ağından ölçüldü: rafın 2 mm üstünde kesit) · ys = raf üst yüzü · pabuç merkezleri (sol z, sağ z)
# taban = rafa oturan 82 × 82 dozaj gövdesi bloğu (z −428…−346; geri kalanı çıkış boruları — yatay ışınla ölçüldü)
UNO = [("tavuk", 1152.0, (1555.0, 1637.0), (-405.0, -370.0)),
       ("kusbasi", 1152.0, (1807.0, 1889.0), (-405.0, -370.0)),
       ("patates", 1575.4, (2218.5, 2300.5), (-405.0, -370.0)),
       ("harc", 1575.4, (1681.0, 1763.0), (-405.0, -370.0)),
       ("kiyma", 1575.4, (1990.0, 2072.0), (-405.0, -370.0))]
T3, W, AYAK, KOL = 3.0, 30.0, 25.0, 12.0
KASET = [("kasar", (2170.0, 1300.0)), ("sucuk", (2340.0, 1300.0))]           # takoz merkezi (x, y) · kaset ön yüzü z 24, K2 iç yüzü z 39
TAKOZ = (40.0, 40.0, 25.0, 39.0)


def kutu(lo, hi):
    lo = np.array(lo, float); hi = np.array(hi, float)
    return cq.Workplane("XY").box(*(hi - lo), centered=False).translate(tuple(lo)).val()


def silx(x0, x1, y, z, r):
    return cq.Solid.makeCylinder(r, abs(x1 - x0), cq.Vector(min(x0, x1), y, z), cq.Vector(1, 0, 0))


def prizma(pts, v):
    w = cq.Wire.makePolygon([cq.Vector(*p) for p in pts], close=True)
    return cq.Solid.extrudeLinear(cq.Face.makeFromWires(w), cq.Vector(*v))


PAB, VIDA, PUL, KAY, TAK = [], [], [], [], []
for ad, ys, (x0, x1), (zs, zd) in UNO:
    for yan, xw, s, zc in (("sol", x0, -1, zs), ("sag", x1, +1, zd)):
        za, zb = zc - W / 2, zc + W / 2
        xo = xw + s * AYAK                                                     # ayağın dış kenarı
        ayak = kutu((min(xw, xo), ys, za), (max(xw, xo), ys + T3, zb))
        kol = kutu((min(xw, xw + s * T3), ys + T3, za), (max(xw, xw + s * T3), ys + KOL, zb))
        yv = ys + T3 + 4.5                                                     # vida ekseni (kolun ortası)
        pab = cq.Workplane("XY").add(ayak).union(cq.Workplane("XY").add(kol)).cut(
            cq.Workplane("XY").add(silx(xw + s * T3, xw, yv, zc, 2.75)))         # Ø5,5 geçiş deliği
        PAB.append(dict(ad="uno_%s_pabuc_%s" % (ad, yan), sh=pab.val(), bom=["UNO bağlama pabucu AISI 304 3 mm L (lazer + 1 büküm), rafa TIG"],
                        kutu=((min(xo, xw + s * T3), ys, za), (max(xo, xw + s * T3), ys + KOL, zb))))
        # vida: baş kolun dışında (pul 1 + baş 5), gövde UNO tabanına 9 mm
        xk = xw + s * T3
        pul = silx(xk, xk + s * 1.0, yv, zc, 5.0)
        vb = silx(xk + s * 1.0, xk + s * 6.0, yv, zc, 4.25).fuse(silx(xk + s * 1.0, xw - s * 9.0, yv, zc, 2.5))
        PUL.append(dict(ad="uno_%s_pabuc_%s_pul" % (ad, yan), sh=pul, bom=["ISO 7089 pul M5 A2"],
                        kutu=((min(xk, xk + s), yv - 5, zc - 5), (max(xk, xk + s), yv + 5, zc + 5))))
        VIDA.append(dict(ad="uno_%s_pabuc_%s_vida" % (ad, yan), sh=vb, bom=["ISO 4762 cıvata M5 × 12 A2-70 (UNO tabanındaki M5 dişli deliğe)"],
                         kutu=((min(xk + s, xk + s * 6.0), yv - 4.25, zc - 4.25), (max(xk + s, xk + s * 6.0), yv + 4.25, zc + 4.25))))
        # kaynak: ayağın dış kenarı boyunca (raf ↔ ayak köşesi)
        KAY.append(dict(ad="uno_%s_pabuc_%s_kaynak" % (ad, yan),
                        sh=prizma([(xo, ys, za), (xo + s * 3.0, ys, za), (xo, ys + 3.0, za)], (0, 0, W)),
                        bom=["TIG 141 köşe dikişi a 2 · ER308LSi · 30 mm · UNO pabucu ↔ raf"],
                        kutu=((min(xo, xo + s * 3), ys, za), (max(xo, xo + s * 3), ys + 3, zb))))
for ad, (x, y) in KASET:
    lo = (x - TAKOZ[0] / 2, y - TAKOZ[1] / 2, TAKOZ[2]); hi = (x + TAKOZ[0] / 2, y + TAKOZ[1] / 2, TAKOZ[3])
    TAK.append(dict(ad="kaset_%s_kapak_takozu" % ad, sh=kutu(lo, hi), bom=["POM-C takoz 40 × 40 × 14, kapağın iç yüzüne 2 × M4 havşa (kapakla döner)"], kutu=(lo, hi)))

g = Glb(gi)
MN, MX, AD = [], [], []
for p in g.prims:
    if p.get("gizli") or p["pr"].get("mode", 4) != 4: continue
    P = p["X"][p["T"]]; m = np.all(P.max(1) >= [1480, 1100, -600], 1) & np.all(P.min(1) <= [2460, 1700, 60], 1)
    MN.append(P[m].min(1)); MX.append(P[m].max(1)); AD += [p["name"]] * int(m.sum())
MN = np.concatenate(MN); MX = np.concatenate(MX); AD = np.array(AD)


def bos(lo, hi, pay=0.3):
    lo = np.array(lo) + pay; hi = np.array(hi) - pay
    m = np.all(MX > lo, 1) & np.all(MN < hi, 1)
    return sorted(set(AD[m]))


for L in (PAB, PUL, KAY, TAK):
    for p in L:
        d = bos(*p["kutu"])
        assert not d, "ADIM 63 DUR: %s hacmi dolu %s" % (p["ad"], d)
# UNO tabanında vida deliği (vida gövdesi + M5 geçiş): Karsi.delik_ac yalnız UNO bileşenini keser (raf / pabuç değmez)
K = SE.Karsi(g, acik_dene=True)
kayit = K.delik_ac(VIDA)
for k in kayit: LOG("  delik: %s · −%s mm³" % (k.get("karsi"), k.get("cikan")))
delinen = set(a for k in kayit for a in k.get("eleman", []))
assert delinen == set(p["ad"] for p in VIDA), "ADIM 63 DUR: UNO'ya girmeyen vida %s" % sorted(set(p["ad"] for p in VIDA) - delinen)
tmp = go + ".e1.glb"; g.kaydet(tmp); del g, K
H = SE.Ham(tmp)
PAR = [("TOPPING_UNO_PABUC__paslanmaz", "TOPPING_GOVDE__sac", 7, PAB, False),
       ("TOPPING_UNO_PABUC__kaynak", "TOPPING_GOVDE__sac", 7, KAY, False),
       ("TOPPING_UNO_PABUC__vida", "U_F_GOVDE__paslanmaz", 7, VIDA + PUL, False),
       ("TOPPING_KASET_TAKOZ__pom", "K_GOVDE__siyah", 7, TAK, True)]
TUM = {}
for d, sb, mek, L, kp in PAR:
    H.koy(d, L, kat=0, mek=mek, kpk_fn=lambda a, k=kp: k, sablon=sb)
    TUM[d] = L
H.yaz(tmp + ".e2.glb")
SE.sikistir(tmp + ".e2.glb", go)
for f in (tmp, tmp + ".e2.glb"): os.remove(f)
for d in TUM: H.aralik[d] = {p["ad"]: (0, 0) for p in TUM[d]}
SE.ent_json(go[:-4] + "_ent.json", "TOPPING_UNO_KASET", [(d, TUM[d]) for d in sorted(TUM)], H.aralik, lambda a: a.endswith("_takozu"), "TOPPING/Gövde", (), kayit,
            ek=dict(uno=UNO, kaset=KASET))
LOG("ADIM 63 bitti · %s · %d pabuç · %d takoz · %.0f sn" % (go, len(PAB), len(TAK), time.time() - t0))
sys.stdout.flush(); os._exit(0)
