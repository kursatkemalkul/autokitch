# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 62 · TOPPING: BAĞLANTISIZ SACLARA GERÇEK KAYNAK (5 Eki 2026 · Claude · bulut oturumu · TOPPING montaj v6)
python 62_topping_kaynak.py girdi.glb cikti.glb      (zincir: hat3_v10c.glb → hat3_v10d.glb)

"Bağlı mı" denetimi (gece2/t5/baglanti_denetim.py, KURALLAR §2.3 kural 10): TOPPING'de bizim yaptığımız 9 sac yalnız DAYANIYORDU — hiçbir vida / kaynak
değmiyordu. Hepsi gövdenin fabrikada kaynaklanan parçaları → TIG 141 (ER308LSi) köşe dikişi, a ≈ 2 (3 mm bacaklı üçgen kesit):
  · 4 raf köşebendi (3 mm L) → yan astar sacına (soğuk gıda bölgesi: sürekli dikiş, taşlanır + pasive; raflar köşebentlere OTURUR, yıkamak için kalkar):
      üst köşebentler alt kenar boyunca (z −561…−59) · alt köşebentler ön + arka uçta dikey (y 1110,5–1146; üst kenarı rafın altında, alt kenarı tabanda)
  · 2 kaide cep taşıyıcısı (3 mm L, x 1620–2100) → iki ucunda enine lamaya (x 1620) ve enine boruya (x 2100): dik kolun dış yüzü + yatay kolun altı
  · kaide enine laması (6 mm, z −790…−5) → arka boruya (sağ yüz) ve ön perdeye (iki yüz) dikey dikiş (arka sol yüzde emiş filtresi var → yok)
  · ayırma perdesi (cep sol) + teknik sağ perde (1,5 mm düz) → dış tabana, sol yüzde 3 × 40 mm aralıklı dikiş (perçin yok: tabanın altında kaide plakası,
      perçin kuyruğuna yer yok)
Yeni düğümler TOPPING_GOVDE__kaynak / KAIDE_C__kaynak (kat 0 Gövde · mek 7 TOPPING/Gövde). Her dikiş hacmi boş olmalı (betik içinde denetim)."""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb
import cadquery as cq

gi, go = sys.argv[1:3]
t0 = time.time(); LOG = SE.log
A = 3.0
# dikiş: ad, düğüm, kaynaştırdığı (bilgi), üçgenin 3 köşesi (başlangıç kesiti), uzama vektörü
D = []
def dik(ad, dug, neyi, p1, p2, p3, v):
    D.append((ad, dug, neyi, [tuple(map(float, p)) for p in (p1, p2, p3)], tuple(map(float, v))))

T, K = "TOPPING_GOVDE__kaynak", "KAIDE_C__kaynak"
# --- üst raf köşebentleri: alt kenar (astar yüzü x 1496 / 2440 · kol alt yüzü y 1534) boyunca
dik("ust_raf_kosebendi_sol_kaynak", T, "üst raf köşebendi sol ↔ astar sol", (1496, 1534, -561), (1499, 1534, -561), (1496, 1531, -561), (0, 0, 502))
dik("ust_raf_kosebendi_sag_kaynak", T, "üst raf köşebendi sağ ↔ astar sağ", (2440, 1534, -561), (2437, 1534, -561), (2440, 1531, -561), (0, 0, 502))
# --- alt raf köşebentleri: ön (z 14) + arka (z −561) uçta dikey
for s, xw, xl in (("sol", 1496, 1499), ("sag", 2440, 2437)):
    dik("raf_kosebendi_%s_kaynak_on" % s, T, "raf köşebendi %s ↔ astar (ön uç)" % s, (xw, 1110.5, 14), (xl, 1110.5, 14), (xw, 1110.5, 17), (0, 35.5, 0))
    dik("raf_kosebendi_%s_kaynak_arka" % s, T, "raf köşebendi %s ↔ astar (arka uç)" % s, (xw, 1110.5, -561), (xl, 1110.5, -561), (xw, 1110.5, -564), (0, 35.5, 0))
# --- kaide cep taşıyıcıları: dik kol dış yüzü (y 790–803) + yatay kol altı (y 803) · iki uçta
for i, zd, zn, (zb0, zb1) in ((0, -705, +1, (-730, -713)), (1, -527, +1, (-552, -535))):
    for uc, xw, xs in (("lama", 1620, +1), ("boru", 2100, -1)):
        dik("kaide_cep_tasiyici_%d_kaynak_%s_a" % (i, uc), K, "cep taşıyıcı %d ↔ enine %s (dik kol)" % (i, uc),
            (xw, 790, zd), (xw + xs * A, 790, zd), (xw, 790, zd + zn * A), (0, 13, 0))
        dik("kaide_cep_tasiyici_%d_kaynak_%s_b" % (i, uc), K, "cep taşıyıcı %d ↔ enine %s (yatay kol altı)" % (i, uc),
            (xw, 803, zb0), (xw + xs * A, 803, zb0), (xw, 803 - A, zb0), (0, 0, zb1 - zb0))
# --- kaide enine laması (x 1614–1620): arka boru (z −790, yalnız sağ yüz) + ön perde (z −5, iki yüz)
dik("kaide_enine_lama_6_kaynak_arka_sag", K, "enine lama ↔ arka boru", (1620, 788, -790), (1623, 788, -790), (1620, 788, -787), (0, 99.5, 0))
dik("kaide_enine_lama_6_kaynak_on_sol", K, "enine lama ↔ ön perde", (1614, 788, -5), (1611, 788, -5), (1614, 788, -8), (0, 99.5, 0))
dik("kaide_enine_lama_6_kaynak_on_sag", K, "enine lama ↔ ön perde", (1620, 788, -5), (1623, 788, -5), (1620, 788, -8), (0, 99.5, 0))
# --- perdeler → dış taban (üst yüz y 893,5), sol yüzde 3 × 40 aralıklı
for ad, xw in (("ayirma_perdesi_cep_sol", 1629.5), ("teknik_sag_perde", 2418.5)):
    for j, z0 in enumerate((-800.0, -672.0, -545.0)):
        dik("%s_kaynak_%d" % (ad, j), T, "%s ↔ dış taban" % ad, (xw, 893.5, z0), (xw - A, 893.5, z0), (xw, 893.5 + A, z0), (0, 0, 40))

g = Glb(gi)
MN, MX, AD = [], [], []
for p in g.prims:
    if p.get("gizli") or p["pr"].get("mode", 4) != 4: continue
    P = p["X"][p["T"]]; m = np.all(P.max(1) >= [1400, 780, -840], 1) & np.all(P.min(1) <= [2520, 1600, 40], 1)
    MN.append(P[m].min(1)); MX.append(P[m].max(1)); AD += [p["name"]] * int(m.sum())
MN = np.concatenate(MN); MX = np.concatenate(MX); AD = np.array(AD)
del g


def bos(lo, hi, pay=0.3):
    lo = np.array(lo) + pay; hi = np.array(hi) - pay
    m = np.all(MX > lo, 1) & np.all(MN < hi, 1)
    return sorted(set(AD[m]))


def prizma(pts, v):
    w = cq.Wire.makePolygon([cq.Vector(*p) for p in pts], close=True)
    return cq.Solid.extrudeLinear(cq.Face.makeFromWires(w), cq.Vector(*v))


PAR = {}
for ad, dug, neyi, pts, v in D:
    Q = np.array(pts); lo = np.minimum(Q.min(0), (Q + v).min(0)); hi = np.maximum(Q.max(0), (Q + v).max(0))
    d = bos(lo, hi)
    assert not d, "ADIM 62 DUR: %s dikiş hacmi dolu %s" % (ad, d)
    L = float(np.linalg.norm(v))
    PAR.setdefault(dug, []).append(dict(ad=ad, sh=prizma(pts, v), bom=["TIG 141 köşe dikişi a 2 · ER308LSi · %.0f mm · %s" % (L, neyi)], tur="kaynak"))
    LOG("  %-46s %-16s %5.0f mm · %s" % (ad, dug, L, neyi))
H = SE.Ham(gi)
SAB = {T: "TOPPING_GOVDE__sac", K: "KAIDE_C__paslanmaz"}
for dug in sorted(PAR):
    H.koy(dug, PAR[dug], kat=0, mek=7, sablon=SAB[dug])
tmp = go + ".e2.glb"; H.yaz(tmp)
SE.sikistir(tmp, go); os.remove(tmp)
for d in PAR: H.aralik[d] = {p["ad"]: (0, 0) for p in PAR[d]}
SE.ent_json(go[:-4] + "_ent.json", "TOPPING_KAYNAK", [(d, PAR[d]) for d in sorted(PAR)], H.aralik, lambda a: False, "TOPPING/Gövde", (), [],
            ek=dict(dikis=[[a, d, n, p, v] for a, d, n, p, v in D]))
LOG("ADIM 62 bitti · %s · %d dikiş · %.0f sn" % (go, len(D), time.time() - t0))
sys.stdout.flush(); os._exit(0)
