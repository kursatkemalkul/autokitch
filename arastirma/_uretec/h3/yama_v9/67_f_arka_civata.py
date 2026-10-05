# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 67 · F ÜST KABİN: ARKA SAC ↔ YANLAR SAPLAMA YERİNE DIŞTAN CIVATA (5 Eki 2026 · Claude · bulut oturumu · F montaj v2)
python 67_f_arka_civata.py girdi.glb cikti.glb      (zincir: hat3_v10h.glb → hat3_v10i.glb)

Montaj sırası denetimi (F v2): adım 36'nın F üst kabin bağlantıları üç sacda üç ayrı eksende preslenmiş saplama —
  yan ↔ tavan: yanda saplama (x) · tavan ↔ arka: tavanda saplama (y) · arka ↔ yan + köşebent: arka sacda saplama (z).
Üç sac çiftler hâlinde birbirine farklı eksende geçtiği için hangi sırayla takılırsa takılsın üçüncü sac bir saplamayı eksenine dik süpürür → kurulamaz.
Çözüm: arka ↔ yan (sol 5 + sağ 5) ve arka ↔ köşebent (1) saplamaları kaldırılır; aynı deliklerden DIŞTAN ISO 7380-1 M5 × 10 bombe başlı cıvata
(baş arka sacın dış yüzünde, arkası boş — makine servis için duvardan çekilir), içteki pul + fiberli somun aynı kalır.
Tavan ↔ arka: tavanın aşağı saplamaları arka sacın üst dönüşündeki deliklerden geçiyordu (y) → delikler öne açık yarık (arka sac arkadan sürülür).
Sıra: yan sol (+x) → tavan / köşebent / bölme duvarı (yan saplamalarına, −x) → davlumbaz (+z) → arka sac (+z, yarıklar tavan saplamalarına) → yan sağ (−x) → cıvatalar.
Denetim (bu betikte): 11 saplama bileşeni beklenen kutuda bulunur ve silinir · cıvata başı hacmi boş."""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb
import cadquery as cq

gi, go = sys.argv[1:3]
t0 = time.time(); LOG = SE.log
DUG = "F_UST_KABIN__paslanmaz"
SAP = [("arka_sol_%d" % y, 2510.5, y + 0.0, -820.0) for y in (850, 1050, 1250, 1450, 1575)] + \
      [("arka_sag_%d" % y, 3989.5, y + 0.0, -820.0) for y in (850, 1050, 1250, 1450, 1575)] + [("kosebent_arka", 2522.0, 1740.0, -818.0)]
Z0, DK, K = -830.0, 9.5, 2.75                                                    # arka sac dış yüzü · ISO 7380-1 M5 baş çapı / yüksekliği


def sil(x0, z0, z1, x, y, r):
    return cq.Solid.makeCylinder(r, z1 - z0, cq.Vector(x, y, z0), cq.Vector(0, 0, 1))


g = Glb(gi)
VIDA = []
for ad, x, y, zu in SAP:
    lo = np.array([x - 3.45, y - 3.45, Z0]); hi = np.array([x + 3.45, y + 3.45, zu])
    b = g.bilesen(DUG, lo=lo, hi=hi, tol=0.3)
    g.sil_b(b)
    bas = cq.Solid.makeSphere(DK / 2, cq.Vector(x, y, Z0), angleDegrees1=-90, angleDegrees2=90)   # bombe baş (yarım küre, sonra kesilir)
    bas = cq.Workplane("XY").add(bas).intersect(cq.Workplane("XY").add(sil(0, Z0 - K, Z0, x, y, DK / 2))).val()
    gov = sil(0, Z0, zu, x, y, 2.5)
    VIDA.append(dict(ad="f_arka_civata_%s" % ad, sh=bas.fuse(gov), bom=["ISO 7380-1 bombe başlı cıvata M5 × 10 A2-70 (dıştan, içte pul + fiberli somun)"],
                     kutu=((x - DK / 2, y - DK / 2, Z0 - K), (x + DK / 2, y + DK / 2, Z0))))
    LOG("  saplama silindi %-14s (%.1f, %.1f) → cıvata" % (ad, x, y))
MN, MX, AD = [], [], []
for p in g.prims:
    if p.get("gizli") or p["pr"].get("mode", 4) != 4: continue
    P = p["X"][p["T"]]; ar = np.linalg.norm(np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]), axis=1)
    m = (ar > 1e-9) & np.all(P.max(1) >= [2490, 830, -845], 1) & np.all(P.min(1) <= [4010, 1760, -810], 1)
    MN.append(P[m].min(1)); MX.append(P[m].max(1)); AD += [p["name"]] * int(m.sum())
MN = np.concatenate(MN); MX = np.concatenate(MX); AD = np.array(AD)
for p in VIDA:
    lo, hi = np.array(p["kutu"][0]) + 0.3, np.array(p["kutu"][1]) - 0.3
    d = sorted(set(AD[np.all(MX > lo, 1) & np.all(MN < hi, 1)]))
    assert not d, "ADIM 67 DUR: %s başı dolu %s" % (p["ad"], d)
# tavan ↔ arka: tavan saplamaları (y, aşağı) arka sacın üst dönüşündeki deliklerden geçer → delikler ÖNE AÇIK YARIK (5,5 genişlik, delikten dönüşün
# ön kenarına): arka sac arkadan sürülürken saplamalar yarığa girer, pul + somun aynı (arka sacın açınımında da yarık: 8 × 5,5 × 9,5)
import manifold3d as mf
ARKA = ("F_UST_KABIN__sac", (2500.0, 788.0, -830.0), (4000.0, 1860.0, -806.0))
YX = [2550.0, 2741.43, 2932.86, 3124.29, 3315.71, 3507.14, 3698.57, 3890.0]
b = g.bilesen(ARKA[0], lo=np.array(ARKA[1]), hi=np.array(ARKA[2]), tol=0.6)
P0 = np.concatenate([p["X"][p["T"][t]] for p, t in b["parca"]])
M = SE.mf_ucgen(P0); assert M is not None, "ADIM 67 DUR: arka sac kapalı katı kurulamadı"
v0 = M.volume()
for x in YX: M = M - mf.Manifold.cube([5.5, 3.0, 10.5]).translate([x - 2.75, 1857.8, -815.0])
v1 = M.volume(); assert 8 * 5.5 * 1.5 * 6.0 < v0 - v1 < 8 * 5.5 * 1.5 * 10.5, "ADIM 67 DUR: yarık hacmi beklenmedik %.0f" % (v0 - v1)
Y_ = SE.mf_P(M); ilk = [True]
def f_(_):
    if ilk[0]: ilk[0] = False; return Y_
    return None
g.donustur(b, f_)
LOG("  arka sac üst dönüşü: 8 öne açık yarık · hacim −%.0f mm³" % (v0 - v1))
tmp = go + ".e1.glb"; g.kaydet(tmp); del g
H = SE.Ham(tmp)
H.koy("F_UST_KABIN_BAG__vida", VIDA, kat=0, mek=19, kpk_fn=lambda a: False, sablon=DUG)
H.yaz(tmp + ".e2.glb")
SE.sikistir(tmp + ".e2.glb", go)
for f in (tmp, tmp + ".e2.glb"): os.remove(f)
H.aralik["F_UST_KABIN_BAG__vida"] = {p["ad"]: (0, 0) for p in VIDA}
SE.ent_json(go[:-4] + "_ent.json", "F_ARKA_CIVATA", [("F_UST_KABIN_BAG__vida", VIDA)], H.aralik, lambda a: False, "F/Gövde", (), [], ek=dict(saplama=SAP))
LOG("ADIM 67 bitti · %s · %d cıvata · %.0f sn" % (go, len(VIDA), time.time() - t0))
sys.stdout.flush(); os._exit(0)
