# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 69 · E GÖVDESİ: ARKA ↔ YAN SOL (ŞARJÖR ARKASI) SAPLAMA + SOMUN YERİNE PRESLENMİŞ SOMUN + DIŞTAN CIVATA (5 Eki 2026 · Claude · bulut oturumu · E montaj v2)
python 69_e_arka_pem.py girdi.glb cikti.glb      (zincir: hat3_v10j.glb → hat3_v10k.glb)

Montaj sırası denetimi (E v2, yol denetimi): arka sac ↔ yan solun arka iç dönüşü bağlantısı arka sacta FHP saplama + içten pul + fiberli somun.
y 345 / 529 / 714 / 898'deki 4 bağlantıda şarjör + asansör kılavuzu somunun 3,2 mm önünde: arka sac şarjörden sonra gelmek zorunda (şarjör yan
sacların ve tabanın saplamalarına bağlı) → 5 mm'lik somun saplamaya takılamaz.
Çözüm: bu 4 noktada saplama + pul + somun kaldırılır. Yan solun arka dönüşüne iç yüzden PEM S-M5-1 preslenmiş somun (dönüşte Ø7,1 delik,
gövde Ø8,7 × 3 içte: şarjör kılavuzuna 6 mm boşluk). Arka sacın mevcut deliğinden DIŞTAN ISO 7380-1 M5 × 6 bombe başlı cıvata (baş arka dış
yüzde, arkası duvara 20 mm boş — makine servis için duvardan çekilir; F adım 67 ile aynı). Diğer 5 arka sol bağlantı (y 161 / 1082 / 1267 / 1451 /
1820) şarjörün dışında: saplama + somun aynı.
Denetim (bu betikte): 12 bileşen (4 × saplama / pul / somun) beklenen kutuda bulunup silinir · PEM gövdesi ve cıvata başı hacmi boş ·
preslenmiş somun deliği yalnız yan sol sacı keser."""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb
import cadquery as cq

gi, go = sys.argv[1:3]
t0 = time.time(); LOG = SE.log
DUG = "E_GOVDE__celik"
X, YS = 4410.5, (345.33, 529.67, 714.0, 898.33)                                  # saplama ekseni (x) · y (govde_bag_arka_sol_*)
ZD, ZR0, ZR1 = -830.0, -828.5, -827.0                                           # arka dış yüzü · yan sol arka dönüşü (iç yüz −827)
DK, K = 9.5, 2.75                                                               # ISO 7380-1 M5 baş çapı / yüksekliği
PEM_D, PEM_H, PEM_S = 8.7, 3.0, 7.1                                             # PEM S-M5-1 gövde Ø × yükseklik · dönüşteki montaj deliği Ø


def sil(z0, z1, y, r):
    return cq.Solid.makeCylinder(r, z1 - z0, cq.Vector(X, y, z0), cq.Vector(0, 0, 1))


g = Glb(gi)
for y in YS:
    for ne, lo, hi in (("saplama", (X - 3.45, y - 3.45, ZD), (X + 3.45, y + 3.45, -820.0)),
                       ("pul", (X - 5.0, y - 5.0, -827.0), (X + 5.0, y + 5.0, -826.0)),
                       ("somun", (X - 4.0, y - 4.62, -826.0), (X + 4.0, y + 4.62, -821.0))):
        b = g.bilesen(DUG, lo=np.array(lo), hi=np.array(hi), tol=0.6)
        g.sil_b(b)
        LOG("  silindi arka_sol_%d %s" % (round(y), ne))
SOM, VIDA = [], []
for y in YS:
    gov = sil(ZR1, ZR1 + PEM_H, y, PEM_D / 2).fuse(sil(ZR0, ZR1, y, PEM_S / 2))
    gov = cq.Workplane("XY").add(gov).cut(cq.Workplane("XY").add(sil(ZR0 - 0.5, ZR1 + PEM_H + 0.5, y, 2.5))).val()
    SOM.append(dict(ad="e_arka_pem_%d" % round(y), sh=gov, bom=["PEM S-M5-1 preslenmiş somun (yan sol arka dönüşü, iç yüz)"],
                    kutu=((X - PEM_D / 2, y - PEM_D / 2, ZR1), (X + PEM_D / 2, y + PEM_D / 2, ZR1 + PEM_H))))
    bas = cq.Solid.makeSphere(DK / 2, cq.Vector(X, y, ZD), angleDegrees1=-90, angleDegrees2=90)
    bas = cq.Workplane("XY").add(bas).intersect(cq.Workplane("XY").add(sil(ZD - K, ZD, y, DK / 2))).val()
    VIDA.append(dict(ad="e_arka_civata_%d" % round(y), sh=bas.fuse(sil(ZD, ZD + 6.0, y, 2.5)),
                     bom=["ISO 7380-1 bombe başlı cıvata M5 × 6 A2-70 (dıştan, yan sol dönüşündeki preslenmiş somuna)"],
                     kutu=((X - DK / 2, y - DK / 2, ZD - K), (X + DK / 2, y + DK / 2, ZD))))
MN, MX, AD = [], [], []
for p in g.prims:
    if p.get("gizli") or p["pr"].get("mode", 4) != 4: continue
    P = p["X"][p["T"]]; ar = np.linalg.norm(np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]), axis=1)
    m = (ar > 1e-9) & np.all(P.max(1) >= [4395, 330, -840], 1) & np.all(P.min(1) <= [4425, 915, -815], 1)
    MN.append(P[m].min(1)); MX.append(P[m].max(1)); AD += [p["name"]] * int(m.sum())
MN = np.concatenate(MN); MX = np.concatenate(MX); AD = np.array(AD)
for p in SOM + VIDA:
    lo, hi = np.array(p["kutu"][0]) + 0.3, np.array(p["kutu"][1]) - 0.3
    d = sorted(set(AD[np.all(MX > lo, 1) & np.all(MN < hi, 1)]))
    assert not d, "ADIM 69 DUR: %s hacmi dolu %s" % (p["ad"], d)
# preslenmiş somunun montaj deliği (Ø7,1) yalnız yan sol sacın arka dönüşünde
K_ = SE.Karsi(g, haric_onek=(DUG,))
DEL = [dict(ad="e_arka_pem_delik_%d" % round(y), sh=sil(ZR0, ZR1, y, PEM_S / 2)) for y in YS]          # tam dönüş kalınlığı (arka iç yüzü −828,5: temas, hacim 0)
for p in DEL:
    m, P = SE.kesici(p)
    hed = K_.tara(p, m, P)
    assert len(hed) == 1 and hed[0][0] == "E_GOVDE__kabuk" and hed[0][1]["hi"][0] < 4420, "ADIM 69 DUR: %s yalnız yan solu kesmeli: %s" % (p["ad"], [(d, b["lo"], b["hi"]) for d, b, v in hed])
kayit = K_.delik_ac(DEL)
tmp = go + ".e1.glb"; g.kaydet(tmp); del g, K_
H = SE.Ham(tmp)
H.koy("E_GOVDE_BAG__vida", VIDA + SOM, kat=0, mek=32, kpk_fn=lambda a: False, sablon=DUG)
H.yaz(tmp + ".e2.glb")
SE.sikistir(tmp + ".e2.glb", go)
for f in (tmp, tmp + ".e2.glb"): os.remove(f)
H.aralik["E_GOVDE_BAG__vida"] = {p["ad"]: (0, 0) for p in VIDA + SOM}
SE.ent_json(go[:-4] + "_ent.json", "E_ARKA_PEM", [("E_GOVDE_BAG__vida", VIDA + SOM)], H.aralik, lambda a: False, "E/Gövde", (), kayit, ek=dict(y=YS))
LOG("ADIM 69 bitti · %s · %d cıvata + %d preslenmiş somun · %.0f sn" % (go, len(VIDA), len(SOM), time.time() - t0))
sys.stdout.flush(); os._exit(0)
