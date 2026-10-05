# -*- coding: utf-8 -*-
"""FIRIN ÜSTÜ DOLAP (v8v) DENETİMİ — yeni katılar + taşınan / değişen parçalar.
  (a) ÇAKIŞMA: her katı ↔ GLB'deki bütün diğer üçgenler (0,6 mm örnekleme · OCC sınıflandırıcı İÇERİDE + yüzeye uzaklık > 0,05 mm)
  (a2) katı ↔ katı hacim kesişimi > 1 mm³ · (b) yeni gövde parçaları arası 0,2–15 mm boşluk · (c) havada parça
  (e) F düşer kapak açılma 5–90° (x ekseni · y 1308 · z 79) · (f) yalıtım açıkta mı (her yüz noktası ≤ 0,05 mm'de başka parçaya değmeli)
Kullanım: python f_kabin_denetim.py hat3_v8u.glb hat3_v8v.glb cikti"""
import os, sys, json, time
import numpy as np
import cadquery as cq
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeVertex
from OCP.BRepClass3d import BRepClass3d_SolidClassifier
from OCP.gp import gp_Pnt
from OCP.TopAbs import TopAbs_IN
from OCP.TopoDS import TopoDS_Iterator
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "tg")); sys.path.insert(0, os.path.join(HERE, "ug")); sys.path.insert(0, HERE)
from glbx import yukle
from u_ortak import ornekle
from dikis import kati
import icdis

g0, g1, OUT = sys.argv[1:4]
os.makedirs(OUT, exist_ok=True)
LOG = open(os.path.join(OUT, "denetim_raporu.txt"), "w", encoding="utf-8")


def yaz(*a):
    s = " ".join(str(x) for x in a); print(s); LOG.write(s + "\n"); LOG.flush()


t0 = time.time()
J0, D0 = yukle(g0); J1, D = yukle(g1)
NADI = sorted(D)
# ---------------- yeni katılar ----------------
sh = cq.Shape.importBrep(os.path.join(HERE, "ug", "f_yeni_katilar.brep"))
it = TopoDS_Iterator(sh.wrapped); KAT = []
while it.More(): KAT.append(cq.Shape.cast(it.Value())); it.Next()
DZ = json.load(open(os.path.join(HERE, "ug", "f_yeni_dizin.json")))
GOV = {a: s for (a, n), s in zip(DZ, KAT)}
NODE = {a: n for a, n in DZ}
YENI_AD = list(GOV)
# her düğümde eklenen üçgenler (yeni katıların ağı) → nokta bulutundan çıkar
EKLENEN = {}
for nd in set(NODE.values()):
    n0 = len(D0[nd]["T"]) if nd in D0 else 0
    EKLENEN[nd] = np.arange(n0, len(D[nd]["T"]))
# ---------------- taşınan / değişen parçalar (v8v ağından katı) ----------------
import bilesen


def bilesen_sec(nd, kosul):
    d = D[nd]; X, T, ok = d["X"], d["T"], d["ok"]
    n0 = len(D0[nd]["T"]) if nd in D0 else len(T)
    idx = np.where(ok[:n0])[0]
    P = np.round(X, 2); u, inv = np.unique(P, axis=0, return_inverse=True); inv = inv.reshape(-1)
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    Ti = inv[T[idx]]
    g = coo_matrix((np.ones(2 * len(idx)), (np.concatenate([Ti[:, 0], Ti[:, 1]]), np.concatenate([Ti[:, 1], Ti[:, 2]]))), shape=(len(u), len(u)))
    _, lab = connected_components(g, directed=False)
    tl = lab[Ti[:, 0]]; out = []
    for c in np.unique(tl):
        tt = idx[tl == c]; Q = X[T[tt]].reshape(-1, 3)
        if kosul(Q.min(0), Q.max(0)): out.append(tt)
    return out


def ic(mn, mx, k, e=0.6):
    return (mn >= np.array(k[0::2]) - e).all() and (mx <= np.array(k[1::2]) + e).all()


TASINAN = [("fan", "F_DAVLUMBAZ__celik", lambda mn, mx: True),
           ("fan/kanal konsolu", "F_DAVLUMBAZ__paslanmaz", lambda mn, mx: mn[1] >= 1347.0 and mx[1] <= 1362.5),
           ("filtre çerçevesi", "F_DAVLUMBAZ__paslanmaz", lambda mn, mx: ic(mn, mx, (3385, 3955, 1348, 1778, -496.5, -441.5))),
           ("filtre", "F_DAVLUMBAZ__koyu", lambda mn, mx: True),
           ("fan kablo rakoru", "ELK_ISTASYON__rakor", lambda mn, mx: ic(mn, mx, (3448.6, 3471.4, 1334.5, 1356.0, -791.5, -768.8))),
           ("arka kablo kelepçesi", "ELK_ISTASYON__celik", lambda mn, mx: ic(mn, mx, (3452, 3468, 1357, 1369, -828.5, -775))),
           ("F kapak menteşe plakası", "F_UST_KAPAK__celik", lambda mn, mx: True),
           ("yan sac contası", "F_UST_KABIN__conta", lambda mn, mx: True),
           ("ön orta dikme + tavan kirişi", "F_UST_KABIN__paslanmaz", lambda mn, mx: ic(mn, mx, (3326, 3356, 1346.5, 1860.5, -827, 57))),
]
OWN = {}                                                     # ad → (düğüm, üçgen indisleri)
for ad, nd, kos in TASINAN:
    for i, tt in enumerate(bilesen_sec(nd, kos)):
        k = "T:%s#%d" % (ad, i)
        ss = kati(D[nd]["X"], D[nd]["T"][tt])
        if len(ss) != 1 or not ss[0].isValid(): yaz("  UYARI katı kurulamadı:", k, len(ss));
        if not ss: continue
        GOV[k] = ss[0] if len(ss) == 1 else cq.Compound.makeCompound(ss); OWN[k] = (nd, tt); NODE[k] = nd
yaz("F ÜST DOLAP DENETİMİ · yeni %d katı + taşınan / değişen %d · geçersiz: %s · %.0f s" % (len(YENI_AD), len(GOV) - len(YENI_AD),
    [k for k, s in GOV.items() if not s.isValid()] or "yok", time.time() - t0))
ZARF = (2480.0, 4020.0, 1290.0, 1875.0, -836.0, 85.0)
TRI = []
for ni, nd in enumerate(NADI):
    d = D[nd]; P = d["X"][d["T"]]; ok = d["ok"].copy()
    if nd in EKLENEN: ok[EKLENEN[nd]] = False
    if nd == "F_UST_KABIN__yalitim": ok[:] = False
    m = ok & (P[:, :, 0].max(1) > ZARF[0]) & (P[:, :, 0].min(1) < ZARF[1]) & (P[:, :, 1].max(1) > ZARF[2]) & (P[:, :, 1].min(1) < ZARF[3]) & \
        (P[:, :, 2].max(1) > ZARF[4]) & (P[:, :, 2].min(1) < ZARF[5])
    if m.any(): TRI.append((ni, np.where(m)[0], P[m]))
YUZ = {k: icdis.yuzey_kati(s) for k, s in GOV.items()}
KAB = {k: cq.Compound.makeCompound(s.Faces()) for k, s in GOV.items()}


def mesafe(s, q):
    d = BRepExtrema_DistShapeShape(BRepBuilderAPI_MakeVertex(gp_Pnt(*q)).Vertex(), s.wrapped); d.Perform()
    return d.Value() if d.IsDone() else 0.0


bulgu = []
for ad, s in GOV.items():
    b = s.BoundingBox(); e = 0.05; kz = (b.xmin + e, b.xmax - e, b.ymin + e, b.ymax - e, b.zmin + e, b.zmax - e)
    own = OWN.get(ad)
    for ni, ti, P in TRI:
        m = (P[:, :, 0].max(1) > kz[0]) & (P[:, :, 0].min(1) < kz[1]) & (P[:, :, 1].max(1) > kz[2]) & (P[:, :, 1].min(1) < kz[3]) & \
            (P[:, :, 2].max(1) > kz[4]) & (P[:, :, 2].min(1) < kz[5])
        if own and NADI[ni] == own[0]: m &= ~np.isin(ti, own[1])
        if not m.any(): continue
        ii = np.where(m)[0]; icn = []
        for c in range(0, len(ii), 20000):
            Q, _ = ornekle(P[ii[c:c + 20000]], kz, 0.6, 400)
            if not len(Q): continue
            Q = np.unique(np.round(Q, 3), axis=0); icn.append(Q[icdis.ic_maske(YUZ[ad], Q)])
        icn = np.concatenate(icn) if icn else np.zeros((0, 3))
        if not len(icn): continue
        sec = icn[np.linspace(0, len(icn) - 1, min(len(icn), 200)).astype(int)]
        cl = BRepClass3d_SolidClassifier(s.wrapped) if s.ShapeType() == "Solid" else None; dr = []
        for q in sec:
            if cl is None: dr.append(mesafe(KAB[ad], q)); continue
            cl.Perform(gp_Pnt(*q), 1e-4); dr.append(mesafe(KAB[ad], q) if cl.State() == TopAbs_IN else 0.0)
        dr = np.array(dr)
        if (dr > 0.05).any():
            bulgu.append((ad, NADI[ni], int(len(icn)), round(float(dr.max()), 2), icn.min(0).round(1).tolist(), icn.max(0).round(1).tolist()))
yaz("(a) ÇAKIŞMA katı ↔ GLB diğer üçgenler: %s · %.0f s" % ("TEMİZ" if not bulgu else "%d BULGU" % len(bulgu), time.time() - t0))
for r in sorted(bulgu, key=lambda x: -x[3]): yaz("     %-36s ↔ %-36s %6d nokta  en derin %.2f mm  %s … %s" % r)
ad = list(GOV); ic_b = []


def bbk(a, b, e=0.0):
    A, B = a.BoundingBox(), b.BoundingBox()
    return not (A.xmin > B.xmax + e or B.xmin > A.xmax + e or A.ymin > B.ymax + e or B.ymin > A.ymax + e or A.zmin > B.zmax + e or B.zmin > A.zmax + e)


for i in range(len(ad)):
    for j in range(i + 1, len(ad)):
        if ad[i].startswith("T:") and ad[j].startswith("T:") and NODE[ad[i]] == NODE[ad[j]] == "F_UST_KABIN__sac": continue
        if not bbk(GOV[ad[i]], GOV[ad[j]]): continue
        try: v = GOV[ad[i]].intersect(GOV[ad[j]]).Volume()
        except Exception: v = -1
        if v > 1.0 or v < 0: ic_b.append((ad[i], ad[j], round(v, 1)))
yaz("(a2) katı ↔ katı hacim kesişimi (> 1 mm³): %s" % ("TEMİZ" if not ic_b else "%d BULGU" % len(ic_b)))
for r in ic_b: yaz("     %-36s ↔ %-36s %s mm³" % r)
# (b) boşluk (yeni gövde parçaları + kabuk)
BB = {k: s.BoundingBox() for k, s in GOV.items()}
B_AD = YENI_AD + [k for k in GOV if k.startswith("T:ön orta")]


def ic1(k, q): return bool(icdis.ic_maske(YUZ[k], np.array([q]))[0])


def dolu(q, haric):
    for k, b in BB.items():
        if k in haric: continue
        if b.xmin - 1e-6 <= q[0] <= b.xmax + 1e-6 and b.ymin - 1e-6 <= q[1] <= b.ymax + 1e-6 and b.zmin - 1e-6 <= q[2] <= b.zmax + 1e-6 and ic1(k, q): return True
    return False


bul = []
for i in range(len(B_AD)):
    for j in range(i + 1, len(B_AD)):
        a, b = BB[B_AD[i]], BB[B_AD[j]]
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
                    if not (ic1(B_AD[i], qa) and ic1(B_AD[j], qb)): continue
                    top += 1
                    if all(not dolu([*q[:e], g0_ + t * (g1_ - g0_), *q[e + 1:]], (B_AD[i], B_AD[j])) for t in (0.25, 0.5, 0.75)): bos += 1
            if bos: bul.append((B_AD[i], B_AD[j], "xyz"[e], round(g1_ - g0_, 2), bos, top))
yaz("(b) BOŞLUK (yeni gövde parçaları + kabuk arası 0,2–15 mm): %s · %.0f s" % ("TEMİZ" if not bul else "%d BULGU" % len(bul), time.time() - t0))
for r in bul: yaz("     %-34s ↔ %-34s %s ekseninde %.2f mm (%d/%d nokta boş)" % r)
# (c) havada
PTS = []; PN = []
for ni, ti, P in TRI:
    Q, _ = ornekle(P, ZARF, 4.0, 60); Q = np.unique(np.round(Q, 2), axis=0); PTS.append(Q); PN.append(np.full(len(Q), ni))
PTS = np.concatenate(PTS); PN = np.concatenate(PN)
hav = []
for k, s in GOV.items():
    deg = []
    for k2, s2 in GOV.items():
        if k2 == k or not bbk(s, s2, 0.1): continue
        dd = BRepExtrema_DistShapeShape(s.wrapped, s2.wrapped); dd.Perform()
        if dd.Value() <= 0.05: deg.append(k2)
    b = s.BoundingBox(); e = 0.1
    m = (PTS[:, 0] > b.xmin - e) & (PTS[:, 0] < b.xmax + e) & (PTS[:, 1] > b.ymin - e) & (PTS[:, 1] < b.ymax + e) & (PTS[:, 2] > b.zmin - e) & (PTS[:, 2] < b.zmax + e)
    own = OWN.get(k)
    if own: m &= PN != NADI.index(own[0])
    dis = set(); idx = np.where(m)[0]
    if len(idx):
        sec = idx[np.linspace(0, len(idx) - 1, min(len(idx), 600)).astype(int)]
        for i in sec:
            if NADI[PN[i]] in dis: continue
            if mesafe(KAB[k], PTS[i]) <= 0.05: dis.add(NADI[PN[i]])
    if not deg and not dis: hav.append(k)
    yaz("     %-36s değdiği: %-60s dış: %s" % (k, ",".join(deg)[:60], ",".join(sorted(dis))[:120]))
yaz("(c) HAVADA PARÇA: %s" % ("YOK" if not hav else "%d BULGU: %s" % (len(hav), hav)))
# (e) F kapakları
def rot(Q, a):
    a = np.radians(a); R = Q - np.array([0, 1308.0, 79.0]); c, s_ = np.cos(a), np.sin(a)
    return np.stack([R[:, 0], R[:, 1] * c - R[:, 2] * s_, R[:, 1] * s_ + R[:, 2] * c], 1) + np.array([0, 1308.0, 79.0])
sup = []
for nd in ("F_UST_KAPAK__on_seffaf__KAPAK_F_SOL", "F_UST_KAPAK__on_seffaf__KAPAK_F_SAG"):
    d = D[nd]; Q, _ = ornekle(d["X"][d["T"][d["ok"]]], None, 6.0, 200); Q = np.unique(np.round(Q, 2), axis=0)
    for a in range(5, 91, 5):
        Rr = rot(Q, a)
        for k, s in GOV.items():
            if "menteşe" in k: continue
            b = BB[k]
            m = (Rr[:, 0] > b.xmin + 0.3) & (Rr[:, 0] < b.xmax - 0.3) & (Rr[:, 1] > b.ymin + 0.3) & (Rr[:, 1] < b.ymax - 0.3) & (Rr[:, 2] > b.zmin + 0.3) & (Rr[:, 2] < b.zmax - 0.3)
            ii = np.where(m)[0]
            if not len(ii): continue
            icx = ii[icdis.ic_maske(YUZ[k], Rr[ii])]
            dr = max([mesafe(KAB[k], Rr[i]) for i in icx[:40]] or [0])
            if dr > 0.05: sup.append((nd[-11:], a, k, len(icx), round(dr, 2)))
yaz("(e) F DÜŞER KAPAK AÇILMA 5–90° ↔ yeni / taşınan parçalar: %s" % ("TEMİZ" if not sup else "%d BULGU" % len(sup)))
for r in sup[:30]: yaz("     ", r)
# (f) yalıtım açıkta mı: her yüz örnek noktası 0,3 mm dışarı → en yakın (diğer düğüm üçgeni ya da yeni / taşınan katı) ≤ 0,35 mm olmalı
import vtk
from vtk.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray
AX = np.concatenate([P.reshape(-1, 3) for ni, ti, P in TRI]); AT = np.arange(len(AX)).reshape(-1, 3)
pts = vtk.vtkPoints(); pts.SetData(numpy_to_vtk(np.ascontiguousarray(AX), deep=1))
cells = vtk.vtkCellArray(); cells.SetCells(len(AT), numpy_to_vtkIdTypeArray(np.hstack([np.full((len(AT), 1), 3), AT]).astype(np.int64).ravel(), deep=1))
pd = vtk.vtkPolyData(); pd.SetPoints(pts); pd.SetPolys(cells)
loc = vtk.vtkStaticCellLocator(); loc.SetDataSet(pd); loc.BuildLocator()
cp = [0.0, 0.0, 0.0]; cid = vtk.reference(0); sid = vtk.reference(0); d2 = vtk.reference(0.0)
for k in [a for a in YENI_AD if "yalitimi" in a]:
    s = GOV[k]; acik = []; top_ = 0
    for f in s.Faces():
        v, t = f.tessellate(0.05, 0.2); V = np.array([[q.x, q.y, q.z] for q in v]); T = np.array(t)
        Q, _ = ornekle(V[T], None, 10.0, 200); Q = np.unique(np.round(Q, 3), axis=0)
        for q in Q:
            nrm = np.array(f.normalAt(cq.Vector(*q)).toTuple()); p = q + 0.3 * nrm; top_ += 1
            loc.FindClosestPoint(p, cp, cid, sid, d2)
            if float(d2) <= 0.35 ** 2: continue
            if any(BB[k2].xmin - 0.4 <= p[0] <= BB[k2].xmax + 0.4 and BB[k2].ymin - 0.4 <= p[1] <= BB[k2].ymax + 0.4 and BB[k2].zmin - 0.4 <= p[2] <= BB[k2].zmax + 0.4
                   and mesafe(KAB[k2], p) <= 0.35 for k2 in GOV if k2 != k): continue
            acik.append(q)
    A = np.array(acik) if acik else np.zeros((0, 3))
    yaz("(f) %-34s yüz noktası %d · hiçbir parçaya değmeyen %d → %s%s" % (k, top_, len(A), "KAPALI (taban levhası + profiller + yan saclar + alt kılıf)" if not len(A) else "AÇIK",
        "" if not len(A) else "  %s … %s" % (A.min(0).round(1).tolist(), A.max(0).round(1).tolist())))
# (g) hava borusu ↔ yan sac delikleri: boru / geçiş rakoru noktaları yan sac diliminde → delik ekseninden uzaklık < delik yarıçapı mı
d = D["F_UST_KABIN__sac"]; X = d["X"]
gg = []
for xs, zc in (((2500.0, 2501.5), -740.0), ((3998.5, 4000.0), -770.0)):
    m = np.zeros(len(X), bool)
    for xv in xs: m |= np.abs(X[:, 0] - xv) < 0.01
    m &= (X[:, 1] > 1795) & (X[:, 1] < 1823) & (np.abs(X[:, 2] - zc) < 12)
    H = X[m]; cy, cz = (H[:, 1].min() + H[:, 1].max()) / 2.0, (H[:, 2].min() + H[:, 2].max()) / 2.0; r = (H[:, 2].max() - H[:, 2].min()) / 2.0
    for nd in ("HAVA_KOMPRESOR__hava_ana", "K_ELEKTRIK__celik", "TOPPING_MODUL__koyu"):
        dd = D[nd]; P = dd["X"][dd["T"][dd["ok"]]]
        mm = (P[:, :, 0].max(1) > xs[0]) & (P[:, :, 0].min(1) < xs[1]) & (np.abs(P[:, :, 1].mean(1) - cy) < 30) & (np.abs(P[:, :, 2].mean(1) - cz) < 30)
        if not mm.any(): continue
        Q, _ = ornekle(P[mm], (xs[0] + 0.05, xs[1] - 0.05, cy - 30, cy + 30, cz - 30, cz + 30), 0.3, 400)
        if not len(Q): continue
        rr = np.hypot(Q[:, 1] - cy, Q[:, 2] - cz); gg.append((xs[0], round(cy, 1), round(cz, 1), round(r, 2), nd, len(Q), round(float(rr.max()), 2)))
yaz("(g) HAVA BORUSU ↔ F YAN SAC DELİKLERİ:")
for x_, cy, cz, r, nd, n, rm in gg: yaz("     yan sac x %.0f · delik merkezi y %.1f z %.1f r %.2f · %-26s %d nokta sac diliminde · en dış %.2f → %s" % (x_, cy, cz, r, nd, n, rm, "DELİKTEN GEÇİYOR" if rm < r else "SACA GİRİYOR"))
json.dump(dict(a=bulgu, a2=ic_b, b=bul, c=hav, e=sup), open(os.path.join(OUT, "denetim.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
yaz("BİTTİ %.0f s" % (time.time() - t0))
LOG.close(); sys.stdout.flush(); os._exit(0)
