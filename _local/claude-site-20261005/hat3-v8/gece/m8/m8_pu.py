# -*- coding: utf-8 -*-
"""m8 madde 4: acikta PU/yalitim — 6 yon ortografik raster (1 mm), kapaklar kapali (on_seffaf opak) / acik (kpk gizli).
Ortuculer: ZEMIN, INSAN, ROBOT, URUN, saydam cam haric. Hat grubu (z ust <= 300) ile karsi grup (QR/tezgah, z alt > 300) ayri taranir."""
import json, sys, numpy as np
from multiprocessing import Pool
from scipy import ndimage
H = float(sys.argv[1]) if len(sys.argv) > 1 and __name__ != "__mp_main__" else 1.0
import os
H = float(os.environ.get("M8_H", H))
def hazirla():
    Z = np.load("m8_onbellek.npz"); J = json.load(open("m8_parca.json", encoding="utf-8")); PC = J["parca"]
    ad = np.array([p["ad"] for p in PC])
    mal = np.array([a.split("__", 1)[1] if "__" in a else "" for a in ad])
    pu = np.array([(m.startswith("pu") and not m.startswith("pu_bant")) or m.startswith("yalitim") for m in mal])
    gor = np.array([m.startswith("yalitim_gorunur") for m in mal])
    haric = np.array([a.startswith(("ZEMIN", "INSAN", "ROBOT", "URUN", "E_PIZZA", "D_PIZZA")) or m.startswith("cam") for a, m in zip(ad, mal)])
    hi = np.array([p["hi"] for p in PC]); lo = np.array([p["lo"] for p in PC])
    karsi = lo[:, 2] > 300
    return Z, PC, pu, gor, haric, karsi
YON = {"on(+z)": (0, 1, 2, +1), "arka(-z)": (0, 1, 2, -1), "sag(+x)": (2, 1, 0, +1), "sol(-x)": (2, 1, 0, -1), "ust(+y)": (0, 2, 1, +1), "alt(-y)": (0, 2, 1, -1)}
def raster(A, B, C, ui, vi, wi, sg, kim):
    U = np.stack([A[:, ui], B[:, ui], C[:, ui]], 1); V = np.stack([A[:, vi], B[:, vi], C[:, vi]], 1); Wd = sg * np.stack([A[:, wi], B[:, wi], C[:, wi]], 1)
    u0 = np.floor(U.min(1).min() / H) * H - H; v0 = np.floor(V.min(1).min() / H) * H - H
    nu = int((U.max() - u0) / H) + 2; nv = int((V.max() - v0) / H) + 2
    zb = np.full(nu * nv, -1e18); ow = np.full(nu * nv, -1, np.int64)
    i0 = np.ceil((U.min(1) - u0) / H - 0.5).astype(np.int64); i1 = np.floor((U.max(1) - u0) / H - 0.5).astype(np.int64)
    j0 = np.ceil((V.min(1) - v0) / H - 0.5).astype(np.int64); j1 = np.floor((V.max(1) - v0) / H - 0.5).astype(np.int64)
    w = np.maximum(i1 - i0 + 1, 0); h = np.maximum(j1 - j0 + 1, 0); n = w * h
    d = (V[:, 1] - V[:, 2]) * (U[:, 0] - U[:, 2]) + (U[:, 2] - U[:, 1]) * (V[:, 0] - V[:, 2])
    ok = np.where((n > 0) & (np.abs(d) > 1e-9))[0]
    cs = np.cumsum(n[ok]); st = 0
    while st < len(ok):
        en = np.searchsorted(cs, (cs[st - 1] if st else 0) + 5e6, side="right"); en = max(en, st + 1)
        t = ok[st:en]; nn = n[t]
        rep = np.repeat(np.arange(len(t)), nn); off = np.arange(nn.sum()) - np.repeat(np.cumsum(nn) - nn, nn)
        tt = t[rep]; ii = i0[tt] + off % w[tt]; jj = j0[tt] + off // w[tt]
        x = u0 + (ii + 0.5) * H; y = v0 + (jj + 0.5) * H
        dd = d[tt]
        a = ((V[tt, 1] - V[tt, 2]) * (x - U[tt, 2]) + (U[tt, 2] - U[tt, 1]) * (y - V[tt, 2])) / dd
        b = ((V[tt, 2] - V[tt, 0]) * (x - U[tt, 2]) + (U[tt, 0] - U[tt, 2]) * (y - V[tt, 2])) / dd
        c = 1 - a - b; m = (a >= -1e-7) & (b >= -1e-7) & (c >= -1e-7)
        z = a * Wd[tt, 0] + b * Wd[tt, 1] + c * Wd[tt, 2]
        f = (jj * nu + ii)[m]; z = z[m]; o = kim[tt[m]]
        srt = np.lexsort((z, f)); f = f[srt]; z = z[srt]; o = o[srt]
        son = np.r_[f[1:] != f[:-1], True]; f = f[son]; z = z[son]; o = o[son]
        y_ = z > zb[f] + 1e-4; zb[f[y_]] = z[y_]; ow[f[y_]] = o[y_]
        st = en
    return zb.reshape(nv, nu), ow.reshape(nv, nu), u0, v0
def is_(arg):
    yon, durum, grup = arg
    Z, PC, pu, gorp, haric, karsi = hazirla()
    P = Z["P"]; kpk = Z["kpk"]
    m = ~haric[P] & (karsi[P] == (grup == "karsi"))
    if durum == "acik": m &= ~kpk
    ti = np.where(m)[0]
    ui, vi, wi, sg = YON[yon]
    zb, ow, u0, v0 = raster(Z["A"][ti], Z["B"][ti], Z["C"][ti], ui, vi, wi, sg, ti)
    tri_pu = pu[P]; ac = (ow >= 0) & tri_pu[np.maximum(ow, 0)]
    lab, n = ndimage.label(ac); R = []
    for i, sl in enumerate(ndimage.find_objects(lab)):
        mm = lab[sl] == i + 1; c = int(mm.sum())
        if c * H * H < 4: continue
        own = ow[sl][mm]; pc = np.bincount(P[own]).argmax(); zz = sg * zb[sl][mm]
        uu = (u0 + (sl[1].start) * H, u0 + sl[1].stop * H); vv = (v0 + sl[0].start * H, v0 + sl[0].stop * H)
        R.append(dict(yon=yon, durum=durum, grup=grup, alan_mm2=round(c * H * H), parca=int(pc), dugum=PC[pc]["ad"], kpk=bool(PC[pc]["kpk"]),
                      gorunur_malzeme=bool(gorp[pc]), eks=["xyz"[ui], "xyz"[vi], "xyz"[wi]], u=[round(uu[0], 1), round(uu[1], 1)], v=[round(vv[0], 1), round(vv[1], 1)],
                      derinlik=[round(float(zz.min()), 1), round(float(zz.max()), 1)], gen=round((sl[1].stop - sl[1].start) * H, 1), yuk=round((sl[0].stop - sl[0].start) * H, 1)))
    print(yon, durum, grup, len(R), int(ac.sum()), flush=True)
    return R
if __name__ == "__main__":
    isler = [(y, d, g) for y in YON for d in ("kapali", "acik") for g in ("hat", "karsi")]
    os.environ["M8_H"] = str(H)
    if H < 1: isler = [i for i in isler if i[2] == "hat"]
    with Pool(6) as p: R = p.map(is_, isler)
    json.dump([r for rr in R for r in rr], open("m8_pu_%s.json" % H, "w", encoding="utf-8"), ensure_ascii=False)
