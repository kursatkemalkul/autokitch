# -*- coding: utf-8 -*-
"""ALT BAS-AÇ DENETİMİ (topping_govde_denetim yöntemleri):
  (a) ÇAKIŞMA: her yeni katı ↔ GLB'deki bütün diğer üçgenler (≤ 4 mm barisentrik örnek · VTK içinde + OCC sınıflandırıcı · > 0,05 mm batma = bulgu)
      + yeni katılar kendi aralarında OCC hacim kesişimi > 1 mm³
  (e1) KANAT AÇILMA 10–100° (K1 pivot x 1438 · K2 pivot x 2497 · z 79): kanadın TÜM parçaları (yeni iç tava + alt karşılık dahil) ↔ çevre
      (yeni sabit parçalar dahil; hariç yalnız kanadın kendisi + menteşe gövde yarıları + üst bas-aç gövdeleri, eski denetimdeki gibi)
  (e2) TABLA / X ARABASI x süpürmesi 1041 … 2375,4 (park 1086, 5 mm adım) ↔ yeni katılar
Kullanım: python topping_basac_alt_denetim.py once.glb sonra.glb cikti_klasoru"""
import os, sys, json, time
import numpy as np
import cadquery as cq
from OCP.BRepClass3d import BRepClass3d_SolidClassifier
from OCP.gp import gp_Pnt
from OCP.TopAbs import TopAbs_IN
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeVertex
from OCP.TopoDS import TopoDS_Iterator
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "tg")); sys.path.insert(0, HERE)
import tgeo as G
from glbx import yukle
import icdis

g0, g1, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
CIK = os.path.join(HERE, "ba", "cikti")
os.makedirs(OUT, exist_ok=True)
LOG = open(os.path.join(OUT, "denetim_raporu.txt"), "w", encoding="utf-8")


def yaz(*a):
    s = " ".join(str(x) for x in a); print(s); LOG.write(s + "\n"); LOG.flush()


def brep_oku(p):
    sh = cq.Shape.importBrep(p); it = TopoDS_Iterator(sh.wrapped); out = []
    while it.More(): out.append(cq.Shape.cast(it.Value())); it.Next()
    return out


t0 = time.time()
J0, D0 = yukle(g0); J1, D1 = yukle(g1)
DZ = json.load(open(os.path.join(CIK, "basac_alt_dizin.json"), encoding="utf-8"))
KAT = brep_oku(os.path.join(CIK, "basac_alt_katilar.brep")); assert len(KAT) == len(DZ["yeni"])
GOV = {ad: s for (ad, nd), s in zip(DZ["yeni"], KAT)}
own, say = {}, {}
for nd, ad, bb, ntri in DZ["rapor"]["yeni"]:
    b = say.get(nd, len(D0[nd]["T"])); own[ad] = (nd, np.arange(b, b + ntri)); say[nd] = b + ntri
yaz("ALT BAS-AÇ DENETİMİ · yeni %d katı · geçersiz: %s" % (len(GOV), [k for k, s in GOV.items() if not s.isValid()] or "yok"))

ADIM, TOL = 4.0, 0.3
ZARF = (1430.0, 2506.0, 780.0, 2206.0, -836.0, 85.0)


def _W(k):
    a, b = np.meshgrid(np.arange(k + 1), np.arange(k + 1), indexing="ij"); m = (a + b) <= k
    return np.stack([1 - a[m] / k - b[m] / k, a[m] / k, b[m] / k], axis=1)


def ornekle(P, zarf=None):
    def suz(Q, s):
        if zarf is None: return Q, s
        m = (Q[:, 0] > zarf[0]) & (Q[:, 0] < zarf[1]) & (Q[:, 1] > zarf[2]) & (Q[:, 1] < zarf[3]) & (Q[:, 2] > zarf[4]) & (Q[:, 2] < zarf[5])
        return Q[m], s[m]
    out, src = [], []
    for Q, s in ((P.reshape(-1, 3), np.repeat(np.arange(len(P)), 3)), (P.mean(axis=1), np.arange(len(P)))):
        Q, s = suz(Q, s); out.append(Q); src.append(s)
    L = np.max(np.linalg.norm(P[:, [1, 2, 0]] - P, axis=2), axis=1); n = np.maximum(1, np.ceil(L / ADIM)).astype(int)
    alan = 0.5 * np.linalg.norm(np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]), axis=1); h = 2 * alan / np.maximum(L, 1e-9)
    ince = (h < ADIM) & (n > 1)
    for e0, e1 in ((0, 1), (1, 2), (2, 0)):
        ii = np.where(ince)[0]
        if not len(ii): break
        Le = np.linalg.norm(P[ii, e1] - P[ii, e0], axis=1); ne = np.maximum(1, np.ceil(Le / ADIM)).astype(int)
        for k in np.unique(ne):
            jj = ii[ne == k]; tt = np.linspace(0, 1, k + 1)[:, None, None]
            Q = (P[jj, e0][None] + tt * (P[jj, e1] - P[jj, e0])[None]).reshape(-1, 3); s_ = np.tile(jj, k + 1)
            Q, s_ = suz(Q, s_); out.append(Q); src.append(s_)
    n[ince] = 1
    for k in np.unique(n):
        if k == 1: continue
        ii = np.where(n == k)[0]; W = _W(int(k)); parti = max(1, int(2e6 // len(W)))
        for c in range(0, len(ii), parti):
            jj = ii[c:c + parti]
            Q = np.einsum("wk,tkd->twd", W, P[jj]).reshape(-1, 3); s = np.repeat(jj, len(W))
            Q, s = suz(Q, s); out.append(Q); src.append(s)
    return np.concatenate(out), np.concatenate(src)


PTS, PN, PT = [], [], []
NADI = sorted(D1)
for ni, nd in enumerate(NADI):
    d = D1[nd]; X, T, ok = d["X"], d["T"], d["ok"]; P = X[T]
    m = ok & (P[:, :, 0].max(1) > ZARF[0]) & (P[:, :, 0].min(1) < ZARF[1]) & (P[:, :, 1].max(1) > ZARF[2]) & (P[:, :, 1].min(1) < ZARF[3]) & \
        (P[:, :, 2].max(1) > ZARF[4]) & (P[:, :, 2].min(1) < ZARF[5])
    if not m.any(): continue
    ii = np.where(m)[0]; Q, s = ornekle(P[ii], ZARF)
    Q = np.round(Q, 2); Q, ui = np.unique(Q, axis=0, return_index=True); s = s[ui]
    PTS.append(Q); PN.append(np.full(len(Q), ni, np.int32)); PT.append(ii[s].astype(np.int64))
PTS = np.concatenate(PTS); PN = np.concatenate(PN); PT = np.concatenate(PT)
yaz("  örnek nokta: %d (%.0f s)" % (len(PTS), time.time() - t0))


def derinlik(s, q):
    d = BRepExtrema_DistShapeShape(BRepBuilderAPI_MakeVertex(gp_Pnt(*q)).Vertex(), s.wrapped); d.Perform()
    return d.Value() if d.IsDone() else 0.0


# ---------------------------------------------------------------- (a)
YUZ = {ad: icdis.yuzey_kati(s) for ad, s in GOV.items()}
bulgu, ornek_say = [], 0
for ad, s in GOV.items():
    b = s.BoundingBox(); nd, ti = own[ad]
    m = (PTS[:, 0] > b.xmin + TOL) & (PTS[:, 0] < b.xmax - TOL) & (PTS[:, 1] > b.ymin + TOL) & (PTS[:, 1] < b.ymax - TOL) & (PTS[:, 2] > b.zmin + TOL) & (PTS[:, 2] < b.zmax - TOL)
    m &= ~((PN == NADI.index(nd)) & np.isin(PT, ti))
    idx = np.where(m)[0]; ornek_say += len(idx)
    if not len(idx): continue
    ic = idx[icdis.ic_maske(YUZ[ad], PTS[idx])]
    if not len(ic): continue
    cl = BRepClass3d_SolidClassifier(s.wrapped)
    for nn in np.unique(PN[ic]):
        icn = ic[PN[ic] == nn]; secn = icn[np.linspace(0, len(icn) - 1, min(len(icn), 60)).astype(int)]
        drn = []
        for i in secn:
            cl.Perform(gp_Pnt(*PTS[i]), 1e-4)
            drn.append(derinlik(s, PTS[i]) if cl.State() == TopAbs_IN else 0.0)
        if (np.array(drn) > 0.05).any():
            bulgu.append((ad, NADI[nn], int(len(icn)), round(float(max(drn)), 2), PTS[icn].min(0).round(1).tolist(), PTS[icn].max(0).round(1).tolist()))
yaz("(a) ÇAKIŞMA yeni katı ↔ GLB diğer üçgenler (aday nokta %d): %s · %.0f s" % (ornek_say, "TEMİZ" if not bulgu else "%d BULGU" % len(bulgu), time.time() - t0))
for r in sorted(bulgu, key=lambda x: -x[3]): yaz("     %-36s ↔ %-32s %6d nokta  en derin %.2f mm  %s … %s" % r)
ad = list(GOV); ic_b = []
for i in range(len(ad)):
    for j in range(i + 1, len(ad)):
        a, b = GOV[ad[i]], GOV[ad[j]]
        if not G._kesisir_bb(G._bb(a), G._bb(b), 0.0): continue
        try: v = a.intersect(b).Volume()
        except Exception: v = -1
        if v > 1.0 or v < 0: ic_b.append((ad[i], ad[j], round(v, 1)))
yaz("    yeni ↔ yeni hacim kesişimi (> 1 mm³): %s" % ("TEMİZ" if not ic_b else "%d BULGU" % len(ic_b)))
for r in ic_b: yaz("     %-36s ↔ %-36s %s mm³" % r)

# ---------------------------------------------------------------- (e1) kanat açılma
ESKI = dict(zip([y[0] for y in json.load(open(os.path.join(HERE, "tg", "cikti", "yeni_dizin.json"), encoding="utf-8"))["yeni"]],
                brep_oku(os.path.join(HERE, "tg", "cikti", "yeni_katilar.brep"))))
KANAT = {}
for kn in ("K1", "K2"):
    k_eski = [k for k in ESKI if k.startswith("onyuz_%s_" % kn) and "mentese_govde" not in k and not k.startswith("onyuz_%s_mentese_kanat" % kn)
              and k != "onyuz_%s_ic_tava" % kn]
    k_yeni = [k for k in GOV if k.startswith("onyuz_%s_ic_tava" % kn) or k == "onyuz_basac_alt_karsilik_%s" % kn]
    KANAT[kn] = [ESKI[k] for k in k_eski] + [GOV[k] for k in k_yeni]
    if kn == "K1": KANAT[kn].append(ESKI["onyuz_basac_karsilik_K1"])
    else: KANAT[kn].append(ESKI["onyuz_basac_karsilik_K2"])
    yaz("  %s dönen katı: %d (eski %d + yeni %s)" % (kn, len(KANAT[kn]), len(k_eski) + 1, ", ".join(k_yeni)))
ni_seffaf = NADI.index("TOPPING_MODUL__on_seffaf")
HARIC = [(*G.MENTESE_X[kn], y0, y1, 26.0, G.ZF) for kn in ("K1", "K2") for (y0, y1) in G.MENTESE_Y] + \
        [(x0, x1, G.BASAC_Y[0], G.BASAC_Y[1], 26.0, G.ZF) for (x0, x1) in G.BASAC.values()]
donanim = np.zeros(len(PTS), bool)
for h in HARIC:
    donanim |= (PTS[:, 0] >= h[0] - 1e-3) & (PTS[:, 0] <= h[1] + 1e-3) & (PTS[:, 1] >= h[2] - 1e-3) & (PTS[:, 1] <= h[3] + 1e-3) & \
               (PTS[:, 2] >= h[4] - 1e-3) & (PTS[:, 2] <= h[5] + 1e-3) & (PN == NADI.index("TOPPING_MODUL__paslanmaz"))
eng = (PN != ni_seffaf) & ~donanim & (PTS[:, 2] > -200.0)
EP, EN = PTS[eng], PN[eng]
yeni_sabit = np.zeros(len(PTS), bool)
for k in GOV:
    nd, ti = own[k]
    if nd != "TOPPING_MODUL__on_seffaf": yeni_sabit |= (PN == NADI.index(nd)) & np.isin(PT, ti)
yaz("  çevre noktası %d (yeni sabit parçalardan %d)" % (len(EP), int(yeni_sabit[eng].sum())))
sup = []; en_yakin = {}
for kn, pivx, isaret in (("K1", 1438.0, -1), ("K2", 2497.0, 1)):
    for a in range(10, 101, 10):
        for s in KANAT[kn]:
            r = s.rotate(cq.Vector(pivx, 0, 79.0), cq.Vector(pivx, 1, 79.0), isaret * a); b = r.BoundingBox()
            m = (EP[:, 0] > b.xmin + TOL) & (EP[:, 0] < b.xmax - TOL) & (EP[:, 1] > b.ymin + TOL) & (EP[:, 1] < b.ymax - TOL) & (EP[:, 2] > b.zmin + TOL) & (EP[:, 2] < b.zmax - TOL)
            if not m.any(): continue
            ii = np.where(m)[0]; ic = list(ii[icdis.ic_maske(icdis.yuzey_kati(r), EP[ii])])
            if ic:
                dr = max(derinlik(r, EP[i]) for i in ic[:50])
                if dr > 0.05: sup.append((kn, a, NADI[EN[ic[0]]], len(ic), round(dr, 2)))
# alt karşılık ↔ alt mandal gövdesi açıklığı (10°'de)
for kn, pivx, isaret in (("K1", 1438.0, -1), ("K2", 2497.0, 1)):
    for a in (2, 5, 10):
        r = GOV["onyuz_basac_alt_karsilik_%s" % kn].rotate(cq.Vector(pivx, 0, 79.0), cq.Vector(pivx, 1, 79.0), isaret * a)
        en_yakin[(kn, a)] = round(r.distance(GOV["onyuz_basac_alt_govde_%s" % kn]), 2)
yaz("(e1) KANAT AÇILMA 10–100° (K1 pivot 1438 · K2 pivot 2497 · z 79): %s · %.0f s" % ("TEMİZ" if not sup else "%d BULGU" % len(sup), time.time() - t0))
for r in sup[:40]: yaz("     ", r)
yaz("     alt karşılık ↔ mandal gövdesi açıklığı: %s mm" % ", ".join("%s %d° %.2f" % (k[0], k[1], v) for k, v in en_yakin.items()))

# ---------------------------------------------------------------- (e2) tabla / X arabası
HAR = [n for n in NADI if n.endswith("__ARABA") and n.startswith("TOPPING")] + ["TOPPING_DONER__TABLA"]
MP = []
for nd in HAR:
    d = D1[nd]; P = d["X"][d["T"][d["ok"]]]; Q, _ = ornekle(P); MP.append(Q)
MP = np.unique(np.round(np.concatenate(MP), 2), axis=0)
PARK, XL, XR = 1086.0, 1041.0, 2375.4
mb = MP.min(0), MP.max(0)
tab = []
for k, s in GOV.items():
    b = s.BoundingBox()
    if b.ymax < mb[0][1] or b.ymin > mb[1][1] or b.zmax < mb[0][2] or b.zmin > mb[1][2]:
        tab.append((k, "y/z bandı dışında (hareketli z en çok %.1f, parça z ≥ %.1f)" % (mb[1][2], b.zmin))); continue
    lo = max(XL - PARK, b.xmin - mb[1][0]); hi = min(XR - PARK, b.xmax - mb[0][0]); hit = None
    for dx in np.linspace(lo, hi, max(2, int((hi - lo) / 5.0) + 1)) if lo <= hi else []:
        Q = MP + np.array([dx, 0, 0])
        m = (Q[:, 0] > b.xmin + TOL) & (Q[:, 0] < b.xmax - TOL) & (Q[:, 1] > b.ymin + TOL) & (Q[:, 1] < b.ymax - TOL) & (Q[:, 2] > b.zmin + TOL) & (Q[:, 2] < b.zmax - TOL)
        if not m.any(): continue
        Qm = Q[m]; icq = Qm[icdis.ic_maske(YUZ[k], Qm)]
        for q in icq[:20]:
            if derinlik(s, q) > 0.05: hit = (round(dx + PARK, 1), q.round(1).tolist()); break
        if hit: break
    tab.append((k, hit or "temiz"))
bt = [t for t in tab if isinstance(t[1], tuple)]
yaz("(e2) TABLA / X ARABASI SÜPÜRMESİ %d nokta · x %.1f … %.1f · hareketli zarf y %.1f–%.1f z %.1f–%.1f: %s" %
    (len(MP), XL, XR, mb[0][1], mb[1][1], mb[0][2], mb[1][2], "TEMİZ" if not bt else "%d BULGU" % len(bt)))
for t in tab: yaz("     %-36s %s" % t)
json.dump(dict(a=bulgu, a_ic=ic_b, e1=sup, e2=[[t[0], str(t[1])] for t in tab]), open(os.path.join(OUT, "denetim.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
yaz("BİTTİ %.0f s" % (time.time() - t0))
LOG.close(); sys.stdout.flush(); os._exit(0)
