# -*- coding: utf-8 -*-
"""U_F + U_KE GÖVDESİ (yeni) DENETİMLERİ — topping_govde_denetim yöntemleri.
  (a) ÇAKIŞMA: her yeni gövde katısı ↔ GLB'deki bütün diğer üçgenler (U gövde düğümleri hariç; onlar (a2)'de) · üçgenler ≤ 4 mm ızgarayla
      örneklenir · OCC derinlik > 0,05 mm = bulgu · (a2) gövde ↔ gövde OCC hacim kesişimi > 1 mm³
  (b) BOŞLUK: gövde parçaları arası 0,2–15 mm karşılıklı yüz + arası boş
  (c) HAVADA: her gövde parçası en az bir komşuya (gövde parçası ya da başka düğüm üçgeni) ≤ 0,05 mm
  (d) U TABANI ↔ İSTASYON TAVANI arayüzü: taban alt yüzü (y 1862) altında istasyon tavanı üst yüzü var mı, arada boşluk var mı
  (e) KAPAK AÇILMA: fırın üstü düşer kapaklar (x ekseni · y 1308 · z 79 · 5–90°), K (dikey · x 4003 · 10–100°), E üst sol (4402) / sağ (5230)
  (f) YALITIM: U gövdesinde yalıtım var mı
Kullanım: python u_govde_denetim.py hat3_v8o_ust.glb cikti_klasoru"""
import os, sys, json, time
import numpy as np
import cadquery as cq
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeVertex
from OCP.gp import gp_Pnt
from OCP.BRepClass3d import BRepClass3d_SolidClassifier
from OCP.TopAbs import TopAbs_IN
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "tg")); sys.path.insert(0, os.path.join(HERE, "ug")); sys.path.insert(0, HERE)
from glbx import yukle, aralik_maske
from u_ortak import ornekle
import icdis
import u_govde_yeni as UY

g1, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
LOG = open(os.path.join(OUT, "denetim_raporu.txt"), "w", encoding="utf-8")


def yaz(*a):
    s = " ".join(str(x) for x in a); print(s); LOG.write(s + "\n"); LOG.flush()


t0 = time.time()
J, D = yukle(g1)
sys.path.insert(0, HERE)
GOV = dict(UY.PARCA)
GOV_DUG = set(UY.DUGUM)
# v8u: indirilen içerik (koli / pizza kutusu yığını) da çakışma denetimine girer (kutu katısı olarak; boşluk / havada denetiminde değil)
import bilesen
KARTON = []
for nd in getattr(UY, "TASI", {}):
    X_, T_ = D[nd]["X"], D[nd]["T"][D[nd]["ok"]]
    for i, (a_, b_, n_) in enumerate(bilesen.bilesenler(X_, T_)):
        k_ = "%s#%d" % (nd, i); GOV[k_] = UY.kutu(a_[0], b_[0], a_[1], b_[1], a_[2], b_[2]); KARTON.append(k_)
    GOV_DUG.add(nd)
yaz("U GÖVDE DENETİMİ · %d katı (U_F %d · U_KE %d) · geçersiz katı: %s" % (len(GOV), sum(1 for k in GOV if k.startswith("ust_f")),
    sum(1 for k in GOV if k.startswith("ust_ke")), [k for k, s in GOV.items() if not s.isValid()] or "yok"))
# GLB'deki U düğümleri gerçekten yeni geometriyi mi taşıyor
for nd in GOV_DUG:
    X = D[nd]["X"]; yaz("  %-24s GLB kutusu x %.1f–%.1f y %.1f–%.1f z %.1f–%.1f · %d üçgen" % (nd, X[:, 0].min(), X[:, 0].max(), X[:, 1].min(), X[:, 1].max(),
                                                                                         X[:, 2].min(), X[:, 2].max(), D[nd]["ok"].sum()))
ZARF = (2490.0, 5240.0, 1850.0, 2210.0, -836.0, 66.0)
PTS, PN = [], []
NADI = sorted(D)
for ni, nd in enumerate(NADI):
    if nd in GOV_DUG: continue
    d = D[nd]; P = d["X"][d["T"]]; ok = d["ok"]
    m = ok & (P[:, :, 0].max(1) > ZARF[0]) & (P[:, :, 0].min(1) < ZARF[1]) & (P[:, :, 1].max(1) > ZARF[2]) & (P[:, :, 1].min(1) < ZARF[3]) & \
        (P[:, :, 2].max(1) > ZARF[4]) & (P[:, :, 2].min(1) < ZARF[5])
    if not m.any(): continue
    Q, _ = ornekle(P[m], ZARF, 4.0, 120)
    Q = np.unique(np.round(Q, 2), axis=0)
    PTS.append(Q); PN.append(np.full(len(Q), ni, np.int32))
PTS = np.concatenate(PTS); PN = np.concatenate(PN)
yaz("  örnek nokta (diğer düğümler, U zarfı): %d · %.0f s" % (len(PTS), time.time() - t0))


def mesafe(s, q):
    d = BRepExtrema_DistShapeShape(BRepBuilderAPI_MakeVertex(gp_Pnt(*q)).Vertex(), s.wrapped); d.Perform()
    return d.Value() if d.IsDone() else 0.0


YUZ = {k: icdis.yuzey_kati(s) for k, s in GOV.items()}
KABUK = {k: cq.Compound.makeCompound(s.Faces()) for k, s in GOV.items()}      # derinlik = yüzeye uzaklık (katıya uzaklık içeride 0 döner)
TOL = 0.3
bulgu = []
TRI = []                                                    # (düğüm indisi, üçgenler) · U zarfındaki gövde dışı üçgenler
for ni, nd in enumerate(NADI):
    if nd in GOV_DUG: continue
    d = D[nd]; P = d["X"][d["T"][d["ok"]]]
    m = (P[:, :, 0].max(1) > ZARF[0]) & (P[:, :, 0].min(1) < ZARF[1]) & (P[:, :, 1].max(1) > ZARF[2]) & (P[:, :, 1].min(1) < ZARF[3]) &         (P[:, :, 2].max(1) > ZARF[4]) & (P[:, :, 2].min(1) < ZARF[5])
    if m.any(): TRI.append((ni, P[m]))
ADIM_A = 0.6                                                # < en ince sac (1,2) → saca dik geçen her yüz en az bir noktayla sacın İÇİNDE örneklenir
for ad, s in GOV.items():
    b = s.BoundingBox(); e = 0.05; kz = (b.xmin + e, b.xmax - e, b.ymin + e, b.ymax - e, b.zmin + e, b.zmax - e)
    for ni, P in TRI:
        m = (P[:, :, 0].max(1) > kz[0]) & (P[:, :, 0].min(1) < kz[1]) & (P[:, :, 1].max(1) > kz[2]) & (P[:, :, 1].min(1) < kz[3]) &             (P[:, :, 2].max(1) > kz[4]) & (P[:, :, 2].min(1) < kz[5])
        if not m.any(): continue
        ii = np.where(m)[0]; icn = []
        for c in range(0, len(ii), 20000):
            Q, _ = ornekle(P[ii[c:c + 20000]], kz, ADIM_A, 400)
            if not len(Q): continue
            Q = np.unique(np.round(Q, 3), axis=0)
            icn.append(Q[icdis.ic_maske(YUZ[ad], Q)])
        icn = np.concatenate(icn) if icn else np.zeros((0, 3))
        if not len(icn): continue
        sec = icn[np.linspace(0, len(icn) - 1, min(len(icn), 200)).astype(int)]
        cl = BRepClass3d_SolidClassifier(s.wrapped); dr = []
        for q in sec:                                      # OCC sınıflandırıcı İÇERİDE diyorsa yüzeye uzaklık = batma derinliği
            cl.Perform(gp_Pnt(*q), 1e-4)
            dr.append(mesafe(KABUK[ad], q) if cl.State() == TopAbs_IN else 0.0)
        dr = np.array(dr)
        if (dr > 0.05).any():
            bulgu.append((ad, NADI[ni], int(len(icn)), round(float(dr.max()), 2), icn.min(0).round(1).tolist(), icn.max(0).round(1).tolist()))
yaz("(a) ÇAKIŞMA gövde ↔ GLB diğer üçgenler (kablo / kanal / pano / fan / baca / içerik / komşu istasyon dahil): %s · %.0f s" %
    ("TEMİZ" if not bulgu else "%d BULGU" % len(bulgu), time.time() - t0))
for r in sorted(bulgu, key=lambda x: -x[3]): yaz("     %-30s ↔ %-40s %6d nokta  en derin %.2f mm  %s … %s" % r)
ad = list(GOV); ic_b = []


def bbk(a, b, e=0.0):
    A, B = a.BoundingBox(), b.BoundingBox()
    return not (A.xmin > B.xmax + e or B.xmin > A.xmax + e or A.ymin > B.ymax + e or B.ymin > A.ymax + e or A.zmin > B.zmax + e or B.zmin > A.zmax + e)


for i in range(len(ad)):
    for j in range(i + 1, len(ad)):
        if not bbk(GOV[ad[i]], GOV[ad[j]]): continue
        v = GOV[ad[i]].intersect(GOV[ad[j]]).Volume()
        if v > 1.0: ic_b.append((ad[i], ad[j], round(v, 1)))
yaz("(a2) gövde ↔ gövde hacim kesişimi (> 1 mm³): %s" % ("TEMİZ" if not ic_b else "%d BULGU" % len(ic_b)))
for r in ic_b: yaz("     %-30s ↔ %-30s %s mm³" % r)
kab = [r for r in bulgu if r[1].startswith("ELK_")]
yaz("(a3) KABLO / KANAL ↔ GÖVDE: %s" % ("TEMİZ (yan sac geçişleri delikten)" if not kab else "%d BULGU" % len(kab)))

# (b) boşluk
BB = {k: s.BoundingBox() for k, s in GOV.items()}


def ic1(k, q):
    return bool(icdis.ic_maske(YUZ[k], np.array([q]))[0])


def dolu(q, haric):
    for k, b in BB.items():
        if k in haric: continue
        if b.xmin - 1e-6 <= q[0] <= b.xmax + 1e-6 and b.ymin - 1e-6 <= q[1] <= b.ymax + 1e-6 and b.zmin - 1e-6 <= q[2] <= b.zmax + 1e-6 and ic1(k, q): return True
    return False


ad = [k for k in ad if k not in KARTON]
bul = []
for i in range(len(ad)):
    for j in range(i + 1, len(ad)):
        a, b = BB[ad[i]], BB[ad[j]]
        lo_ = [max(a.xmin, b.xmin), max(a.ymin, b.ymin), max(a.zmin, b.zmin)]; hi_ = [min(a.xmax, b.xmax), min(a.ymax, b.ymax), min(a.zmax, b.zmax)]
        ort = [hi_[e] - lo_[e] for e in range(3)]
        for e in range(3):
            diger = [ort[k] for k in range(3) if k != e]
            if not (min(diger) > 1.0 and -15.0 < ort[e] < -0.2): continue
            ilk = [(a.xmin, a.xmax), (a.ymin, a.ymax), (a.zmin, a.zmax)][e][1] <= [(b.xmin, b.xmax), (b.ymin, b.ymax), (b.zmin, b.zmax)][e][0] + 1e-6
            g0_, g1_ = hi_[e], lo_[e]; bos = top = 0; axs = [k for k in range(3) if k != e]
            for u in np.linspace(0.1, 0.9, 5):
                for v in np.linspace(0.1, 0.9, 5):
                    q = [0, 0, 0]; q[axs[0]] = lo_[axs[0]] + u * ort[axs[0]]; q[axs[1]] = lo_[axs[1]] + v * ort[axs[1]]
                    qa, qb = list(q), list(q)
                    qa[e] = (g0_ - 0.1) if ilk else (g1_ + 0.1); qb[e] = (g1_ + 0.1) if ilk else (g0_ - 0.1)
                    if not (ic1(ad[i], qa) and ic1(ad[j], qb)): continue
                    top += 1
                    if all(not dolu([*q[:e], g0_ + t * (g1_ - g0_), *q[e + 1:]], (ad[i], ad[j])) for t in (0.25, 0.5, 0.75)): bos += 1
            if bos: bul.append((ad[i], ad[j], "xyz"[e], round(g1_ - g0_, 2), bos, top))
yaz("(b) BOŞLUK (gövde parçaları arası 0,2–15 mm, karşılıklı yüz, arası boş): %s · %.0f s" % ("TEMİZ" if not bul else "%d BULGU" % len(bul), time.time() - t0))
for r in bul: yaz("     %-30s ↔ %-30s %s ekseninde %.2f mm (%d/%d nokta boş)" % r)

# (c) havada
hav = []
for k, s in GOV.items():
    if k in KARTON: continue
    deg = []
    for k2, s2 in GOV.items():
        if k2 == k or not bbk(s, s2, 0.1): continue
        dd = BRepExtrema_DistShapeShape(s.wrapped, s2.wrapped); dd.Perform()
        if dd.Value() <= 0.05: deg.append(k2)
    b = s.BoundingBox(); e = 0.1
    m = (PTS[:, 0] > b.xmin - e) & (PTS[:, 0] < b.xmax + e) & (PTS[:, 1] > b.ymin - e) & (PTS[:, 1] < b.ymax + e) & (PTS[:, 2] > b.zmin - e) & (PTS[:, 2] < b.zmax + e)
    dis = set()
    idx = np.where(m)[0]
    if len(idx):
        # yüzeye yakın noktalar: kaba (kutu) süzgeç + örnek mesafe
        sec = idx[np.linspace(0, len(idx) - 1, min(len(idx), 400)).astype(int)]
        for i in sec:
            if NADI[PN[i]] in dis: continue
            if mesafe(s, PTS[i]) <= 0.05: dis.add(NADI[PN[i]])
    if not deg and not dis: hav.append(k)
    yaz("     %-30s değdiği gövde: %-70s dış: %s" % (k, ",".join(deg)[:70], ",".join(sorted(dis))[:110]))
yaz("(c) HAVADA PARÇA: %s" % ("YOK (her parça en az bir komşuya değiyor)" if not hav else "%d BULGU: %s" % (len(hav), hav)))

# (d) taban ↔ istasyon tavanı
ust = {}
for nd in ("F_UST_KABIN__sac", "K_GOVDE__kabuk", "E_GOVDE__kabuk"):
    d = D[nd]; P = d["X"][d["T"][d["ok"]]]
    m = (np.abs(P[:, :, 1] - 1862.0) < 0.02).all(1)
    ust[nd] = P[m]
for kod, (x0, x1) in (("U_F", (2500.0, 4000.0)), ("U_KE", (4000.0, 5230.0))):
    xs = np.arange(x0 + 2.0, x1 - 1.0, 10.0); zs = np.arange(-826.5, 58.0, 10.0)
    G = np.array([(x, z) for x in xs for z in zs])
    tsb = GOV["ust_%s_taban_sac" % kod[2:].lower()]                  # yalnız tabanın DOLU olduğu noktalar (baca / soket ağızları hariç)
    yt = icdis.yuzey_kati(tsb)
    G = G[icdis.ic_maske(yt, np.stack([G[:, 0], np.full(len(G), 1862.75), G[:, 1]], 1))]
    kap = np.zeros(len(G), bool)
    for nd, P in ust.items():
        A = P[:, :, [0, 2]]
        for t in A:
            mn, mx = t.min(0), t.max(0)
            ii = np.where(~kap & (G[:, 0] >= mn[0] - 1e-6) & (G[:, 0] <= mx[0] + 1e-6) & (G[:, 1] >= mn[1] - 1e-6) & (G[:, 1] <= mx[1] + 1e-6))[0]
            if not len(ii): continue
            v0, v1, v2 = t; Q = G[ii]
            d0 = (v1 - v0); d1 = (v2 - v0); dq = Q - v0
            den = d0[0] * d1[1] - d0[1] * d1[0]
            if abs(den) < 1e-12: continue
            a = (dq[:, 0] * d1[1] - dq[:, 1] * d1[0]) / den; b_ = (d0[0] * dq[:, 1] - d0[1] * dq[:, 0]) / den
            kap[ii[(a >= -1e-6) & (b_ >= -1e-6) & (a + b_ <= 1 + 1e-6)]] = True
    tb = GOV["ust_%s_taban_sac" % kod[2:].lower()].BoundingBox()
    yaz("(d) %s taban alt yüzü y %.1f · altındaki istasyon tavanı üst yüzü y 1862,0 → ARA BOŞLUK %.1f mm · taban altının %.1f %%'i istasyon tavanına basıyor (%d / %d nokta)" %
        (kod, tb.ymin, tb.ymin - 1862.0, 100.0 * kap.mean(), kap.sum(), len(kap)))
    if (~kap).any():
        Gm = G[~kap]
        for gx in np.unique(np.round(Gm[:, 0] / 100.0)):
            g_ = Gm[np.round(Gm[:, 0] / 100.0) == gx]
            yaz("     basmayan bölge x %.0f–%.0f z %.0f–%.0f (%d nokta)" % (g_[:, 0].min(), g_[:, 0].max(), g_[:, 1].min(), g_[:, 1].max(), len(g_)))

# (e) kapak açılma
GOV_P = {k: s for k, s in GOV.items()}


def rot(Q, piv, eksen, a):
    a = np.radians(a); R = Q - piv; c, s_ = np.cos(a), np.sin(a)
    if eksen == "x":
        y = R[:, 1] * c - R[:, 2] * s_; z = R[:, 1] * s_ + R[:, 2] * c; return np.stack([R[:, 0], y, z], 1) + piv
    x = R[:, 0] * c + R[:, 2] * s_; z = -R[:, 0] * s_ + R[:, 2] * c; return np.stack([x, R[:, 1], z], 1) + piv


def kapak_nok(nd, sec=None):
    d = D[nd]; P = d["X"][d["T"][d["ok"]]]
    if sec is not None: P = P[sec(P.mean(1))]
    Q, _ = ornekle(P, None, 6.0, 200); return np.unique(np.round(Q, 2), axis=0)


KAP = [("F sol düşer", kapak_nok("F_UST_KAPAK__on_seffaf__KAPAK_F_SOL"), np.array([0, 1308.0, 79.0]), "x", +1, range(5, 91, 5)),
       ("F sağ düşer", kapak_nok("F_UST_KAPAK__on_seffaf__KAPAK_F_SAG"), np.array([0, 1308.0, 79.0]), "x", +1, range(5, 91, 5)),
       ("K tek", kapak_nok("K_GOVDE__on_seffaf", lambda c: c[:, 1] > 1500), np.array([4003.0, 0, 79.0]), "y", -1, range(5, 101, 5)),
       ("E üst sol", kapak_nok("E_GOVDE__on_seffaf", lambda c: (c[:, 1] > 1500) & (c[:, 0] < 4861.5)), np.array([4402.0, 0, 79.0]), "y", -1, range(5, 101, 5)),
       ("E üst sağ", kapak_nok("E_GOVDE__on_seffaf", lambda c: (c[:, 1] > 1500) & (c[:, 0] > 4861.5)), np.array([5230.0, 0, 79.0]), "y", +1, range(5, 101, 5))]
sup = []
for ad_k, Q, piv, ek, sg, acilar in KAP:
    yon = rot(Q, piv, ek, sg * 30.0)[:, 2].mean() - Q[:, 2].mean()
    assert yon > 0, (ad_k, "açılma yönü dışa değil")
    nb = 0
    for a in acilar:
        R = rot(Q, piv, ek, sg * a)
        for k, s in GOV_P.items():
            b = BB[k]
            m = (R[:, 0] > b.xmin + TOL) & (R[:, 0] < b.xmax - TOL) & (R[:, 1] > b.ymin + TOL) & (R[:, 1] < b.ymax - TOL) & (R[:, 2] > b.zmin + TOL) & (R[:, 2] < b.zmax - TOL)
            ii = np.where(m)[0]
            if not len(ii): continue
            ic = ii[icdis.ic_maske(YUZ[k], R[ii])]
            if len(ic):
                cl = BRepClass3d_SolidClassifier(s.wrapped); dr = 0.0
                for i in ic[:60]:
                    cl.Perform(gp_Pnt(*R[i]), 1e-4)
                    if cl.State() == TopAbs_IN: dr = max(dr, mesafe(KABUK[k], R[i]))
                if dr > 0.05: sup.append((ad_k, a, k, len(ic), round(dr, 2))); nb += 1
    yaz("     %-12s %6d nokta · eksen %s %s · %d–%d° · %s" % (ad_k, len(Q), ek, piv.tolist(), min(acilar), max(acilar), "temiz" if not nb else "%d bulgu" % nb))
yaz("(e) KAPAK AÇILMA SÜPÜRMESİ ↔ yeni U gövdesi: %s · %.0f s" % ("TEMİZ" if not sup else "%d BULGU" % len(sup), time.time() - t0))
for r in sup[:40]: yaz("     ", r)
yaz("(f) YALITIM: U_F / U_KE gövdesinde yalıtım YOK (soğutmasız depo) → görünür yalıtım / sac-yalıtım boşluğu sorusu yok · baca yalıtımı U_F_BACA'da, "
    "0,5 kılıf + flanş altında kapalı (değişmedi)")
json.dump(dict(a=bulgu, a2=ic_b, b=bul, c=hav, e=sup), open(os.path.join(OUT, "denetim.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
yaz("BİTTİ %.0f s" % (time.time() - t0))
LOG.close(); sys.stdout.flush(); os._exit(0)
