# -*- coding: utf-8 -*-
"""TOPPING GÖVDESİ (yeni) DENETİMLERİ — b_govde_denetim / b_govde_bosluk / b_pu_sarim yöntemleri + kapak / tabla taramaları.
  (a) ÇAKIŞMA: her yeni / değişen TOPPING gövde katısı ↔ GLB'deki bütün diğer üçgenler (TOPPING içi dahil) · üçgenler ≤ 4 mm barisentrik
      ızgarayla örneklenir · OCC BRepClass3d · yüzeyden > 0,05 mm batan nokta = bulgu · yeni katılar kendi aralarında OCC hacim kesişimi > 1 mm³
  (b) BOŞLUK: gövde parçaları arası 0,2–15 mm karşılıklı yüz + arası boş (kasıtlı derzler ayrı listelenir)
  (c) PU SARIM: her PU katısının bütün yüzleri ≤ 6 mm örneklenir, 0,4 mm dışarı → bir sac / PU / gömülü eleman içinde olmalı
  (d) KABLO / HORTUM ↔ GÖVDE: ELK_* ve hortum / boru düğümlerinin noktaları gövde katılarına girmez (girdiği yer delikten geçer)
  (e) KAPAK AÇILMA 10–100° (sanal pivot ön dış köşe, z 79) + TABLA / X ARABASI x süpürmesi (1041 … 2375,4, park 1086, 5 mm adım)
Kullanım: python topping_govde_denetim.py hat3_v8n.glb hat3_v8o.glb cikti_klasoru"""
import os, sys, json, time
import numpy as np
import cadquery as cq
from OCP.BRepClass3d import BRepClass3d_SolidClassifier
from OCP.gp import gp_Pnt
from OCP.TopAbs import TopAbs_IN, TopAbs_ON
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeVertex
from OCP.TopoDS import TopoDS_Iterator
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "tg")); sys.path.insert(0, HERE)
import tgeo as G
from glbx import yukle, aralik_maske
from dikis import kati
import topping_govde_yeni as TY
import icdis

g0, g1, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(OUT, exist_ok=True)
LOG = open(os.path.join(OUT, "denetim_raporu.txt"), "w", encoding="utf-8")


def yaz(*a):
    s = " ".join(str(x) for x in a); print(s); LOG.write(s + "\n"); LOG.flush()


t0 = time.time()
J0, D0 = yukle(g0); J1, D1 = yukle(g1)
R = TY.segment(J0, D0, ["TOPPING_MODUL", "ELK_TOPPING"])
DZ = json.load(open(os.path.join(HERE, "tg", "cikti", "yeni_dizin.json"), encoding="utf-8"))
sh = cq.Shape.importBrep(os.path.join(HERE, "tg", "cikti", "yeni_katilar.brep"))
it = TopoDS_Iterator(sh.wrapped); KAT = []
while it.More(): KAT.append(cq.Shape.cast(it.Value())); it.Next()
assert len(KAT) == len(DZ["yeni"])
# yeni parçaların v8o'daki üçgen aralıkları
own = {}                                                   # ad → (düğüm, üçgen indisleri)
say = {}
for nd, ad, bb, ntri in DZ["rapor"]["yeni"]:
    b = say.get(nd, len(D0[nd]["T"])); own[ad] = (nd, np.arange(b, b + ntri)); say[nd] = b + ntri
GOV = {ad: s for (ad, nd, ref, kp), s in zip(DZ["yeni"], KAT)}
NODE = {ad: nd for ad, nd, ref, kp in DZ["yeni"]}
YUZ_ESKI = {}
# değişen eski parçalar (uzatılan / ötelenen) → v8o ağından katı
ANALITIK = {("TOPPING_MODUL__paslanmaz", "soguk_ic_kaplama"): [G.kutu(1495.0, 1496.0, 1110.5, 2141.0, 23.0, 38.0), G.kutu(2440.0, 2441.0, 1110.5, 2141.0, 23.0, 38.0),
                                                            G.kutu(1496.0, 2440.0, 2140.0, 2141.0, 23.0, 38.0)],
            ("TOPPING_MODUL__paslanmaz", "?0"): [G.kutu(1437.5, 2498.5, 1109.0, 1110.5, 23.0, 38.0)]}
for nd, lab, *_ in [tuple(u[:2]) for u in DZ["uzat"]] + [tuple(o[:2]) for o in DZ["otele"]]:
    if (nd, lab) in ANALITIK:                                   # uzatılan eski parça: yalnız UZAYAN dilim (z 23 → 38), analitik kutu
        d = D1[nd]; n0 = len(D0[nd]["T"]); m = np.zeros(len(d["T"]), bool); m[:n0] = (R[nd] == lab) & D0[nd]["ok"]
        for i, s in enumerate(ANALITIK[(nd, lab)]):
            k = "ESKI:%s|%s#uzama%d" % (nd.split("__")[-1], lab, i); GOV[k] = s; NODE[k] = nd; own[k] = (nd, np.where(m)[0])
        continue
    d = D1[nd]; n0 = len(D0[nd]["T"]); m = np.zeros(len(d["T"]), bool); m[:n0] = (R[nd] == lab) & D0[nd]["ok"]
    ss = kati(d["X"], d["T"][m])
    for i, s in enumerate(ss):
        k = "ESKI:%s|%s#%d" % (nd.split("__")[-1], lab, i); GOV[k] = s; NODE[k] = nd; own[k] = (nd, np.where(m)[0])
        YUZ_ESKI[k] = icdis.yuzey_ag(d["X"], d["T"][m])
yaz("TOPPING GÖVDE DENETİMİ · yeni %d katı + değişen %d · %.0f s" % (len(DZ["yeni"]), len(GOV) - len(DZ["yeni"]), time.time() - t0))
gecersiz = [k for k, s in GOV.items() if not s.isValid()]
yaz("  geçersiz katı: %s" % (gecersiz or "yok"))

# ---------------------------------------------------------------- nokta bulutu (TOPPING zarfı ± 6)
ZARF = (1430.0, 2506.0, 780.0, 2206.0, -836.0, 85.0)
ADIM = 4.0


def _W(k):
    a, b = np.meshgrid(np.arange(k + 1), np.arange(k + 1), indexing="ij"); m = (a + b) <= k
    a, b = a[m] / k, b[m] / k
    return np.stack([1 - a - b, a, b], axis=1)


def ornekle(P, zarf=None, kmax=None):
    """üçgenler ≤ ADIM barisentrik ızgara · parça parça üretilir, zarf dışı atılır (bellek küçük)"""
    def suz(Q, s):
        if zarf is None: return Q, s
        m = (Q[:, 0] > zarf[0]) & (Q[:, 0] < zarf[1]) & (Q[:, 1] > zarf[2]) & (Q[:, 1] < zarf[3]) & (Q[:, 2] > zarf[4]) & (Q[:, 2] < zarf[5])
        return Q[m], s[m]
    out, src = [], []
    for Q, s in ((P.reshape(-1, 3), np.repeat(np.arange(len(P)), 3)), (P.mean(axis=1), np.arange(len(P)))):
        Q, s = suz(Q, s); out.append(Q); src.append(s)
    L = np.max(np.linalg.norm(P[:, [1, 2, 0]] - P, axis=2), axis=1); n = np.maximum(1, np.ceil(L / ADIM)).astype(int)
    alan = 0.5 * np.linalg.norm(np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]), axis=1); h = 2 * alan / np.maximum(L, 1e-9)
    ince = (h < ADIM) & (n > 1)                     # şerit üçgen: yalnız kenarlar boyunca (iç noktalar kenara ≤ h/2)
    for e0, e1 in ((0, 1), (1, 2), (2, 0)):
        ii = np.where(ince)[0]
        if not len(ii): break
        Le = np.linalg.norm(P[ii, e1] - P[ii, e0], axis=1); ne = np.maximum(1, np.ceil(Le / ADIM)).astype(int)
        for k in np.unique(ne):
            jj = ii[ne == k]; tt = np.linspace(0, 1, k + 1)[:, None, None]
            Q = (P[jj, e0][None] + tt * (P[jj, e1] - P[jj, e0])[None]).reshape(-1, 3); s_ = np.tile(jj, k + 1)
            Q, s_ = suz(Q, s_); out.append(Q); src.append(s_)
    n[ince] = 1
    buyuk = (~ince) & (alan > 5000.0)               # geniş düz yüzler 10 mm ızgara (ince sac girişi uzun kesişim çizgisinde yine yakalanır)
    n[buyuk] = np.maximum(1, np.ceil(L[buyuk] / 10.0)).astype(int)
    if kmax: n = np.minimum(n, kmax)
    for k in np.unique(n):
        if k == 1: continue
        ii = np.where(n == k)[0]
        W = _W(int(k))
        parti = max(1, int(2e6 // len(W)))
        for c in range(0, len(ii), parti):
            jj = ii[c:c + parti]
            Q = np.einsum("wk,tkd->twd", W, P[jj]).reshape(-1, 3); s = np.repeat(jj, len(W))
            Q, s = suz(Q, s); out.append(Q); src.append(s)
    return np.concatenate(out), np.concatenate(src)


PTS, PN, PT = [], [], []
NADI = sorted(D1)
for ni, nd in enumerate(NADI):
    d = D1[nd]; X, T, ok = d["X"], d["T"], d["ok"]
    P = X[T]
    m = ok & (P[:, :, 0].max(1) > ZARF[0]) & (P[:, :, 0].min(1) < ZARF[1]) & (P[:, :, 1].max(1) > ZARF[2]) & (P[:, :, 1].min(1) < ZARF[3]) & \
        (P[:, :, 2].max(1) > ZARF[4]) & (P[:, :, 2].min(1) < ZARF[5])
    if not m.any(): continue
    ii = np.where(m)[0]; Q, s = ornekle(P[ii], ZARF, None if nd.startswith(('TOPPING', 'ELK_TOPPING')) else 80)
    Q = np.round(Q, 2); Q, ui = np.unique(Q, axis=0, return_index=True); s = s[ui]
    PTS.append(Q); PN.append(np.full(len(Q), ni, np.int32)); PT.append(ii[s].astype(np.int64))
PTS = np.concatenate(PTS); PN = np.concatenate(PN); PT = np.concatenate(PT)
yaz("  örnek nokta: %d (%.0f s)" % (len(PTS), time.time() - t0))


def derinlik(s, q):
    d = BRepExtrema_DistShapeShape(BRepBuilderAPI_MakeVertex(gp_Pnt(*q)).Vertex(), s.wrapped); d.Perform()
    return d.Value() if d.IsDone() else 0.0


ELK = ("ELK_", "hortum", "hava_ana", "bakir")
bulgu, kablo_bulgu = [], []
TOL = 0.3
YUZ = {}
for ad, s in GOV.items():
    YUZ[ad] = YUZ_ESKI.get(ad) or icdis.yuzey_kati(s)
for ad, s in GOV.items():
    b = s.BoundingBox(); nd, ti = own[ad]
    m = (PTS[:, 0] > b.xmin + TOL) & (PTS[:, 0] < b.xmax - TOL) & (PTS[:, 1] > b.ymin + TOL) & (PTS[:, 1] < b.ymax - TOL) & (PTS[:, 2] > b.zmin + TOL) & (PTS[:, 2] < b.zmax - TOL)
    m &= ~((PN == NADI.index(nd)) & np.isin(PT, ti))
    if ad.startswith("ESKI:") and any(ad.startswith("ESKI:%s|%s#" % (u[0].split("__")[-1], u[1])) for u in DZ["uzat"]):
        m &= PTS[:, 2] > 22.95                                           # uzatılan eski parça: yalnız yeni uzayan bölge (eskisi zaten denetliydi)
    if ad.startswith("ESKI:") and any(ad.startswith("ESKI:%s|%s#" % (o[0].split("__")[-1], o[1])) for o in DZ["otele"]):
        for o in DZ["otele"]:                                           # birlikte ötelenen parçalar arası göreli konum değişmedi
            m &= ~((PN == NADI.index(o[0])) & np.isin(PT, np.where(R[o[0]] == o[1])[0]))
    idx = np.where(m)[0]
    if not len(idx): continue
    ic = idx[icdis.ic_maske(YUZ[ad], PTS[idx])]
    if not len(ic): continue
    for nn in np.unique(PN[ic]):
        icn = ic[PN[ic] == nn]; secn = icn[np.linspace(0, len(icn) - 1, min(len(icn), 60)).astype(int)]
        cl = BRepClass3d_SolidClassifier(s.wrapped)
        drn = []
        for i in secn:
            cl.Perform(gp_Pnt(*PTS[i]), 1e-4)
            drn.append(derinlik(s, PTS[i]) if (cl.State() == TopAbs_IN or ad.startswith("ESKI")) else 0.0)
        drn = np.array(drn)
        if (drn > 0.05).any():
            rec = (ad, NADI[nn], int(len(icn)), round(float(drn.max()), 2), PTS[icn].min(0).round(1).tolist(), PTS[icn].max(0).round(1).tolist())
            bulgu.append(rec)
            if any(e in NADI[nn] for e in ELK): kablo_bulgu.append(rec)
yaz("(a) ÇAKIŞMA gövde ↔ GLB diğer üçgenler: %s · %.0f s" % ("TEMİZ" if not bulgu else "%d BULGU" % len(bulgu), time.time() - t0))
for r in sorted(bulgu, key=lambda x: -x[3]): yaz("     %-44s ↔ %-36s %6d nokta  en derin %.2f mm  %s … %s" % r)
ad = list(GOV); ic_b = []
for i in range(len(ad)):
    for j in range(i + 1, len(ad)):
        a, b = GOV[ad[i]], GOV[ad[j]]
        if not G._kesisir_bb(G._bb(a), G._bb(b), 0.0): continue
        if ad[i].startswith("ESKI") and ad[j].startswith("ESKI"): continue   # eski parçalar arası (birlikte taşındı / eskiden denetli)
        try: v = a.intersect(b).Volume()
        except Exception: v = -1
        if v > 1.0 or v < 0: ic_b.append((ad[i], ad[j], round(v, 1)))
yaz("    gövde ↔ gövde hacim kesişimi (> 1 mm³): %s" % ("TEMİZ" if not ic_b else "%d BULGU" % len(ic_b)))
for r in ic_b: yaz("     %-44s ↔ %-44s %s mm³" % r)
yaz("(d) KABLO / HORTUM ↔ GÖVDE: %s" % ("TEMİZ (her kablo / hortum gövdeye girmiyor; sac geçişleri delikten)" if not kablo_bulgu else "%d BULGU" % len(kablo_bulgu)))
json.dump(dict(a=bulgu, a_ic=ic_b, d=kablo_bulgu), open(os.path.join(OUT, "denetim_a_d.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------------------------------------------------------------- örtücü katılar (b, c): gövde + gömülü + PU yakınındaki eski TOPPING parçaları
ORTU = dict(GOV)
PU_AD = [k for k in GOV if ("PU" in k or k.endswith("_pu")) and not k.startswith("ESKI")]
pub = [G._bb(GOV[k]) for k in PU_AD]
for nd in [n for n in D0 if n.startswith("TOPPING_MODUL") and n in R]:
    d = D1[nd]; n0 = len(D0[nd]["T"]); L = R[nd]; ok = D0[nd]["ok"] & (D1[nd]["ok"][:n0])
    for lab in set(L[ok]):
        if any(o[0] == nd and o[1] == lab for o in DZ["uzat"]) or any(o[0] == nd and o[1] == lab for o in DZ["otele"]): continue
        tt = np.where(ok & (L == lab))[0]
        Q = d["X"][d["T"][tt]].reshape(-1, 3); bb = (Q[:, 0].min(), Q[:, 0].max(), Q[:, 1].min(), Q[:, 1].max(), Q[:, 2].min(), Q[:, 2].max())
        if not any(G._kesisir_bb(bb, (p[0] - 1, p[1] + 1, p[2] - 1, p[3] + 1, p[4] - 1, p[5] + 1), 0.0) for p in pub): continue
        for i, s in enumerate(kati(d["X"], d["T"][tt])): ORTU["ESKI_ORTU:%s|%s#%d" % (nd.split("__")[-1], lab, i)] = s
for (nd_, lab_) in ANALITIK:                                   # dolgu (yalnız boşluk/sarım denetiminde): eski parçanın v8n ağı (uzama dışı bölge değişmedi)
    d_ = D0[nd_]; T_ = d_["T"][d_["ok"] & (R[nd_] == lab_)]
    k_ = "DOLGU:%s|%s" % (nd_.split("__")[-1], lab_); YUZ[k_] = icdis.yuzey_ag(d_["X"], T_)
    Q_ = d_["X"][T_].reshape(-1, 3); ORTU[k_] = G.kutu(*[v for a_, b_ in zip(Q_.min(0), Q_.max(0)) for v in (a_, b_)])
BB = {k: s.BoundingBox() for k, s in ORTU.items()}
CL = {k: BRepClass3d_SolidClassifier(s.wrapped) for k, s in ORTU.items()}
for k, s in ORTU.items():
    if k not in YUZ: YUZ[k] = icdis.yuzey_kati(s)
CL = {k: v for k, v in CL.items() if not k.startswith("DOLGU:")}
yaz("  örtücü katı: %d · %.0f s" % (len(ORTU), time.time() - t0))


def icinde(k, q, on=True):
    CL[k].Perform(gp_Pnt(*q), 1e-4); st = CL[k].State()
    return st == TopAbs_IN or (on and st == TopAbs_ON)


def dolu(q, haric):
    for k, b in BB.items():
        if k in haric: continue
        if b.xmin - 1e-6 <= q[0] <= b.xmax + 1e-6 and b.ymin - 1e-6 <= q[1] <= b.ymax + 1e-6 and b.zmin - 1e-6 <= q[2] <= b.zmax + 1e-6 and icdis.ic_maske(YUZ[k], np.array([q]))[0]: return True
    return False


def ic1(k, q):
    return bool(icdis.ic_maske(YUZ[k], np.array([q]))[0])


# (b) boşluk
KASITLI = {("onyuz_K1_dis_tava", "onyuz_K2_dis_tava"): "kanatlar arası derz 3 mm", }
ad = [k for k in GOV if not k.startswith(("kablo_", "evap_kaseti_tahliye", "sogutma_grubu_titresim", "kanal_TOPPING"))]
bul, kas = [], []
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
            if bos:
                rec = (ad[i], ad[j], "xyz"[e], round(g1_ - g0_, 2), bos, top)
                kk = [v for (p, q2), v in KASITLI.items() if {p, q2} == {ad[i], ad[j]}]
                kk = kk or (("?13" in ad[i] + ad[j]) and ("kilavuz_flipper" in ad[i] + ad[j] or "uzama2" in ad[i] + ad[j]))
                (kas if kk or ("onyuz_K1" in ad[i] and "onyuz_K2" in ad[j]) or ("onyuz_K2" in ad[i] and "onyuz_K1" in ad[j]) else bul).append(rec)
yaz("(b) BOŞLUK (0,2–15 mm, karşılıklı yüz, arası boş): %s · kasıtlı (kanat derzi) %d · %.0f s" % ("TEMİZ" if not bul else "%d BULGU" % len(bul), len(kas), time.time() - t0))
for r in bul: yaz("     %-40s ↔ %-40s %s ekseninde %.2f mm (%d/%d nokta boş)" % r)
for r in kas: yaz("     kasıtlı: %-32s ↔ %-32s %s %.2f mm" % r[:4])

# (c) PU sarım
OFS = 0.4


def ornek_yuz(f):
    v, t = f.tessellate(0.05, 0.2)
    V = np.array([[q.x, q.y, q.z] for q in v]); T = np.array(t)
    if not len(T): return np.zeros((0, 3)), np.zeros((0, 3))
    P = V[T]; L = np.max(np.linalg.norm(P[:, [1, 2, 0]] - P, axis=2), axis=1); n = np.maximum(1, np.ceil(L / 8.0)).astype(int)
    out = []
    for k in np.unique(n):
        W = np.array([(1 - a / k - b / k, a / k, b / k) for a in range(k + 1) for b in range(k + 1 - a)])
        out.append(np.einsum("wk,tkd->twd", W, P[n == k]).reshape(-1, 3))
    Q = np.unique(np.round(np.concatenate(out), 3), axis=0)
    N = np.array([f.normalAt(cq.Vector(*q)).toTuple() for q in Q]) if f.geomType() != "PLANE" else np.tile(f.normalAt().toTuple(), (len(Q), 1))
    return Q, N


top_n = top_a = 0; acik_kayit = []
import vtk
PADIM = 8.0
TUM_X, TUM_T, TUM_SRC = [], [], []
off = 0
for ni, nd in enumerate(NADI):
    d = D1[nd]; P = d["X"][d["T"]]; ok = d["ok"]
    m = ok & (P[:, :, 0].max(1) > ZARF[0]) & (P[:, :, 0].min(1) < ZARF[1]) & (P[:, :, 1].max(1) > ZARF[2]) & (P[:, :, 1].min(1) < ZARF[3]) &         (P[:, :, 2].max(1) > ZARF[4]) & (P[:, :, 2].min(1) < ZARF[5])
    ii = np.where(m)[0]
    if not len(ii): continue
    TUM_X.append(P[ii].reshape(-1, 3)); TUM_T.append(np.arange(off, off + 3 * len(ii)).reshape(-1, 3)); TUM_SRC.append(np.stack([np.full(len(ii), ni), ii], 1)); off += 3 * len(ii)
TUM_X = np.concatenate(TUM_X); TUM_T = np.concatenate(TUM_T); TUM_SRC = np.concatenate(TUM_SRC)
from vtk.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray
for pk in PU_AD:
    nd, ti = own[pk]
    keep = ~((TUM_SRC[:, 0] == NADI.index(nd)) & np.isin(TUM_SRC[:, 1], ti))
    T_ = TUM_T[keep]
    pts = vtk.vtkPoints(); pts.SetData(numpy_to_vtk(np.ascontiguousarray(TUM_X), deep=1))
    cells = vtk.vtkCellArray(); cells.SetCells(len(T_), numpy_to_vtkIdTypeArray(np.hstack([np.full((len(T_), 1), 3), T_]).astype(np.int64).ravel(), deep=1))
    pd = vtk.vtkPolyData(); pd.SetPoints(pts); pd.SetPolys(cells)
    loc = vtk.vtkStaticCellLocator(); loc.SetDataSet(pd); loc.BuildLocator()
    s_ = GOV[pk]; n_ = 0; acik = []
    cp = [0.0, 0.0, 0.0]; cid = vtk.reference(0); sid = vtk.reference(0); d2 = vtk.reference(0.0)
    for f in s_.Faces():
        Q, N = ornek_yuz(f)
        if not len(Q): continue
        n_ += len(Q)
        for q in Q:
            loc.FindClosestPoint(q, cp, cid, sid, d2)
            if float(d2) > 0.05 ** 2: acik.append(q)
    top_n += n_
    if acik:
        A = np.array(acik); top_a += len(A)
        yaz("     AÇIK %-26s %5d / %6d nokta  %s … %s" % (pk, len(A), n_, A.min(0).round(1).tolist(), A.max(0).round(1).tolist()))
        from scipy.cluster.hierarchy import fcluster, linkage
        Asub = A[np.linspace(0, len(A) - 1, min(len(A), 3000)).astype(int)]
        Z = fcluster(linkage(Asub, "single"), 10.0, "distance") if len(Asub) > 1 else np.array([1])
        for c in np.unique(Z)[:15]:
            B_ = Asub[Z == c]; yaz("          %4d nokta  %s … %s" % (len(B_), B_.min(0).round(1).tolist(), B_.max(0).round(1).tolist()))
        acik_kayit.append((pk, Asub.round(1).tolist()))
    else:
        yaz("     tam  %-26s %6d nokta · bütün yüzler sac / PU / gömülü elemana değiyor" % (pk, n_))
yaz("(c) PU SARIM (kesit): %d PU · %d nokta · açık %d → %s · %.0f s" % (len(PU_AD), top_n, top_a, "TEMİZ" if not top_a else "BULGU", time.time() - t0))
json.dump(dict(b=bul, b_kasitli=kas, c=acik_kayit), open(os.path.join(OUT, "denetim_b_c.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------------------------------------------------------------- (e) kapak açılma + tabla süpürme
KANAT = {"K1": [k for k in GOV if k.startswith("onyuz_K1_") and "mentese_govde" not in k and "basac_govde" not in k],
         "K2": [k for k in GOV if k.startswith("onyuz_K2_") and "mentese_govde" not in k and "basac_govde" not in k]}
KANAT["K1"] = [k for k in KANAT["K1"] if not k.startswith("onyuz_K1_mentese_kanat")]
KANAT["K2"] = [k for k in KANAT["K2"] if not k.startswith("onyuz_K2_mentese_kanat")]
ni_seffaf = NADI.index("TOPPING_MODUL__on_seffaf")
donanim = np.zeros(len(PTS), bool)
for k in GOV:
    if any(w in k for w in ("mentese", "basac")):
        nd, ti = own[k]; donanim |= (PN == NADI.index(nd)) & np.isin(PT, ti)
eng = (PN != ni_seffaf) & ~donanim & (PTS[:, 2] > -200.0)
EP = PTS[eng]; EN = PN[eng]
sup = []
for kn, pivx, isaret in (("K1", 1438.0, -1), ("K2", 2497.0, 1)):
    parca = [GOV[k] for k in KANAT[kn]]
    for a in range(10, 101, 10):
        for s in parca:
            r = s.rotate(cq.Vector(pivx, 0, 79.0), cq.Vector(pivx, 1, 79.0), isaret * a); b = r.BoundingBox()
            m = (EP[:, 0] > b.xmin + TOL) & (EP[:, 0] < b.xmax - TOL) & (EP[:, 1] > b.ymin + TOL) & (EP[:, 1] < b.ymax - TOL) & (EP[:, 2] > b.zmin + TOL) & (EP[:, 2] < b.zmax - TOL)
            if not m.any(): continue
            ii = np.where(m)[0]; ic = list(ii[icdis.ic_maske(icdis.yuzey_kati(r), EP[ii])])
            if ic:
                dr = max(derinlik(r, EP[i]) for i in ic[:50])
                if dr > 0.05: sup.append((kn, a, NADI[EN[ic[0]]], len(ic), round(dr, 2)))
yaz("(e1) KAPAK AÇILMA 10–100° (K1 pivot 1438 · K2 pivot 2497 · z 79): %s · %.0f s" % ("TEMİZ" if not sup else "%d BULGU" % len(sup), time.time() - t0))
for r in sup[:40]: yaz("     ", r)
# tabla / X arabası
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
    if b.ymax < mb[0][1] or b.ymin > mb[1][1] or b.zmax < mb[0][2] or b.zmin > mb[1][2]: continue
    lo = max(XL - PARK, b.xmin - mb[1][0]); hi = min(XR - PARK, b.xmax - mb[0][0])
    if lo > hi: continue
    n = max(2, int((hi - lo) / 5.0) + 1); hit = None
    for dx in np.linspace(lo, hi, n):
        Q = MP + np.array([dx, 0, 0])
        m = (Q[:, 0] > b.xmin + TOL) & (Q[:, 0] < b.xmax - TOL) & (Q[:, 1] > b.ymin + TOL) & (Q[:, 1] < b.ymax - TOL) & (Q[:, 2] > b.zmin + TOL) & (Q[:, 2] < b.zmax - TOL)
        if not m.any(): continue
        Qm = Q[m]; icq = Qm[icdis.ic_maske(YUZ[k], Qm)]
        for q in icq[:20]:
            if derinlik(s, q) > 0.05: hit = (k, round(dx + PARK, 1), q.round(1).tolist()); break
        if hit: break
    tab.append((k, round(lo + PARK, 1), round(hi + PARK, 1), hit))
bt = [t for t in tab if t[3]]
yaz("(e2) TABLA / X ARABASI SÜPÜRMESİ %d nokta · %.1f … %.1f · aday gövde katısı %d: %s · %.0f s" % (len(MP), XL, XR, len(tab), "TEMİZ" if not bt else "%d BULGU" % len(bt), time.time() - t0))
for t in tab: yaz("     %-36s x %.1f … %.1f  %s" % (t[0], t[1], t[2], t[3] or "temiz"))
json.dump(dict(e1=sup, e2=tab), open(os.path.join(OUT, "denetim_e.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
yaz("BİTTİ %.0f s" % (time.time() - t0))
LOG.close(); sys.stdout.flush(); os._exit(0)
