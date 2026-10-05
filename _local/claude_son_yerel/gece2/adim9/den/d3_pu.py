# -*- coding: utf-8 -*-
"""Kalem 3 açık PU / yalıtım: python d3_pu.py   (DENETIM_GLB ile başka GLB)
numba z-tampon raster (1 mm) 6 eksen yönünden; her hücrede ilk görülen düğüm. Durum A: her şey (kapaklar kapalı) · Durum B: kpk üçgenleri gizli.
Örtücü sayılmayan: ROBOT/INSAN/ZEMIN/TEZGAH/URUN/ELK_ZEMIN (güvenli taraf). PU/yalıtım düğümü = adında __pu / yalitim geçen."""
import os, sys, json, time, numpy as np
from numba import njit
from scipy import ndimage
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "cak"))
import c8a_ortak as M
t0 = time.time()
J, D = M.glb_oku_etiket(M.GLB)
HAR = ("ROBOT", "INSAN", "ZEMIN", "TEZGAH", "DUZ_TEZGAH", "URUN", "ELK_ZEMIN")
AD = []; PP = []; KK = []; ID = []
for nd, (P, L) in D.items():
    if nd.startswith(HAR) or not len(P): continue
    k = len(AD); AD.append(nd); PP.append(P); KK.append(L[:, 2] > 0); ID.append(np.full(len(P), k, np.int32))
P = np.concatenate(PP); KP = np.concatenate(KK); IDS = np.concatenate(ID)
PU = np.array([("__pu" in a or "yalitim" in a) for a in AD])
print(len(P), "üçgen ·", len(AD), "düğüm · PU/yalıtım düğümü", [a for a, p in zip(AD, PU) if p], "%.0f s" % (time.time() - t0), flush=True)


@njit(cache=True)
def ras(T, ids, u0, v0, h, nu, nv):
    zb = np.full((nv, nu), -1e18); kim = np.full((nv, nu), -1, np.int32)
    for t in range(T.shape[0]):
        x0 = T[t, 0, 0]; y0 = T[t, 0, 1]; z0 = T[t, 0, 2]
        x1 = T[t, 1, 0]; y1 = T[t, 1, 1]; z1 = T[t, 1, 2]
        x2 = T[t, 2, 0]; y2 = T[t, 2, 1]; z2 = T[t, 2, 2]
        d = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
        if abs(d) < 1e-12: continue
        i0 = max(0, int(np.ceil((min(x0, x1, x2) - u0) / h - 0.5))); i1 = min(nu - 1, int(np.floor((max(x0, x1, x2) - u0) / h - 0.5)))
        j0 = max(0, int(np.ceil((min(y0, y1, y2) - v0) / h - 0.5))); j1 = min(nv - 1, int(np.floor((max(y0, y1, y2) - v0) / h - 0.5)))
        for j in range(j0, j1 + 1):
            Y = v0 + (j + 0.5) * h
            for i in range(i0, i1 + 1):
                X = u0 + (i + 0.5) * h
                a = ((y1 - y2) * (X - x2) + (x2 - x1) * (Y - y2)) / d
                b = ((y2 - y0) * (X - x2) + (x0 - x2) * (Y - y2)) / d
                c = 1.0 - a - b
                if a < -1e-7 or b < -1e-7 or c < -1e-7: continue
                Z = a * z0 + b * z1 + c * z2
                if Z > zb[j, i] + 1e-4:
                    zb[j, i] = Z; kim[j, i] = ids[t]
    return kim


YON = {"+z (önden)": (0, 1, 2, 1), "-z (arkadan)": (0, 1, 2, -1), "+x (sağdan)": (2, 1, 0, 1), "-x (soldan)": (2, 1, 0, -1), "+y (üstten)": (0, 2, 1, 1), "-y (alttan)": (0, 2, 1, -1)}
h = 1.0; SON = {}
for durum, maske in (("A kapaklar kapalı", np.ones(len(P), bool)), ("B kpk gizli", ~KP)):
    Q = P[maske]; I = IDS[maske]
    for yon, (iu, iv, iw, s) in YON.items():
        T = np.stack([Q[:, :, iu], Q[:, :, iv], s * Q[:, :, iw]], 2)
        u0, v0 = T[:, :, 0].min() - 1, T[:, :, 1].min() - 1
        nu = int((T[:, :, 0].max() - u0) / h) + 2; nv = int((T[:, :, 1].max() - v0) / h) + 2
        kim = ras(T, I, u0, v0, h, nu, nv)
        acik = (kim >= 0) & PU[np.maximum(kim, 0)]
        lab, n = ndimage.label(acik); R = []
        for k_, sl in enumerate(ndimage.find_objects(lab)):
            m = lab[sl] == k_ + 1; c = int(m.sum())
            if c < 4: continue
            dug = AD[np.bincount(kim[sl][m]).argmax()]
            R.append(dict(mm2=c, dugum=dug, u=[round(u0 + sl[1].start * h, 1), round(u0 + sl[1].stop * h, 1)], v=[round(v0 + sl[0].start * h, 1), round(v0 + sl[0].stop * h, 1)]))
        R.sort(key=lambda r: -r["mm2"])
        ax = "xyz"; SON["%s · %s" % (durum, yon)] = dict(eksen="u=%s v=%s" % (ax[iu], ax[iv]), toplam_mm2=int(acik.sum()), bolge=R[:30])
        print("%-20s %-14s açık PU/yalıtım %8d mm² · %d bölge%s  (%.0f s)" % (durum, yon, acik.sum(), len(R), ("  " + "; ".join("%s %d mm² %s %s–%s %s %s–%s" % (r["dugum"], r["mm2"], ax[iu], *r["u"], ax[iv], *r["v"]) for r in R[:4])) if R else "", time.time() - t0), flush=True)
json.dump(SON, open(os.environ.get("PU_CIKTI", "pu.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
sys.stdout.flush(); os._exit(0)
