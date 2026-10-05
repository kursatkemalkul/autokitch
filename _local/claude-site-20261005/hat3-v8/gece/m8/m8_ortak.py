# -*- coding: utf-8 -*-
import json, numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
J = json.load(open("m8_parca.json", encoding="utf-8")); PC = J["parca"]; MEK = J["MEK"]; KAT = J["KAT"]
N = len(PC); E = np.load("m8_kenar.npy")
LO = np.array([p["lo"] for p in PC]); HI = np.array([p["hi"] for p in PC])
pmek = np.array([p["mek"] for p in PC]); pkpk = np.array([p["kpk"] for p in PC]); pkat = np.array([p["kat"] for p in PC])
def ist(m): return MEK[m]["istasyon"] if m >= 0 else "?"
def mekad(m): return MEK[m]["kod"] if m >= 0 else "(etiketsiz)"
pist = np.array([ist(m) for m in pmek])
HARIC_ON = ("ROBOT", "INSAN", "URUN", "E_KUTU", "E_PIZZA", "D_PIZZA", "ZEMIN", "E_KOSE", "E_PARMAK")
def haric(i):
    a = PC[i]["ad"]
    return a.startswith(HARIC_ON) or (pkat[i] >= 0 and KAT[pkat[i]] in ("ROBOT", "URUN"))
def grafik(gor):
    """gor: bool N. Donus: derece, kume etiketi, kume topraklimi"""
    m = gor[E[:, 0]] & gor[E[:, 1]]; e = E[m]
    der = np.bincount(e.reshape(-1), minlength=N) * gor
    k, lab = connected_components(coo_matrix((np.ones(len(e)), (e[:, 0], e[:, 1])), shape=(N, N)), directed=False)
    zem = gor & (LO[:, 1] <= 1.0)
    topr = np.zeros(k, bool); topr[np.unique(lab[zem])] = True
    return der, lab, topr
def tanim(i):
    p = PC[i]; d = HI[i] - LO[i]
    return dict(parca=i, dugum=p["ad"], istasyon=pist[i], mek=mekad(pmek[i]), kat=KAT[pkat[i]] if pkat[i] >= 0 else "?", kpk=bool(pkpk[i]),
                ucgen=p["n"], x=[round(LO[i, 0], 1), round(HI[i, 0], 1)], y=[round(LO[i, 1], 1), round(HI[i, 1], 1)], z=[round(LO[i, 2], 1), round(HI[i, 2], 1)],
                boyut=[round(v, 1) for v in d.tolist()])

_T = None
def en_yakin(parcalar, gor=None, R=30.0):
    """kume ornek noktalarindan kume DISI (gor icindeki) en yakin ucgene uzaklik (<=R). Donus (uzaklik, parca)"""
    import m8_temas as T
    S = np.zeros(N, bool); S[list(map(int, parcalar))] = True
    if sum(PC[i]["n"] for i in np.where(S)[0]) > 40000: return (None, -1)
    pts, pid = T.kenar_ornek(set(np.where(S)[0].tolist()), adim=3.0)
    if len(pts) > 20000: pts = pts[np.random.default_rng(0).choice(len(pts), 20000, replace=False)]
    I = T.agac(); best = (1e9, -1)
    izin = ~S if gor is None else (~S & gor)
    for s in range(0, len(pts), 1000):
        p = pts[s:s + 1000]
        ids, cnt = I.intersection_v(p - R, p + R); ids = ids.astype(np.int64); cnt = cnt.astype(np.int64)
        qi = np.repeat(np.arange(len(p)), cnt)
        ok = izin[T.TPc[ids]]; qi = qi[ok]; ids = ids[ok]
        for s2 in range(0, len(qi), 2000000):
            a = qi[s2:s2 + 2000000]; b = ids[s2:s2 + 2000000]
            d = T.nokta_ucgen(p[a], T.A[b], T.B[b], T.C[b]); j = d.argmin()
            if d[j] < best[0]: best = (float(d[j]), int(T.TPc[b[j]]))
    return best if best[1] >= 0 else (None, -1)
