# ön görünüş z-buffer (gerçek ağ): her (x,y) hücresinde en öndeki yüzeyin z'si + parça indeksi; saydam (on_seffaf) ayrı
import sys, os, io, json, time
import numpy as np
import cadquery as cq
from OCP.TopoDS import TopoDS_Iterator
DD = sys.argv[1]; OUT = sys.argv[2]
R = 4.0; X0, X1, Y0, Y1 = 700.0, 5300.0, 0.0, 2220.0
nx, ny = int((X1 - X0) / R), int((Y1 - Y0) / R)
t0 = time.time()
idx = json.load(io.open(os.path.join(DD, "dunya.json"), encoding="utf-8"))
sh = cq.Shape.importBrep(os.path.join(DD, "dunya.brep"))
it = TopoDS_Iterator(sh.wrapped); ch = []
while it.More(): ch.append(cq.Shape.cast(it.Value())); it.Next()
HAR = ("QR_", "TEZGAH", "ROBOT", "ELK_QR", "ELK_ANA_PANO", "ELK_ZEMIN", "DUZ_TEZGAH", "INSAN", "CEK_")
ZA = np.full((ny, nx), -2000.0); IA = np.full((ny, nx), -1, dtype=np.int32)    # opak
ZS = np.full((ny, nx), -2000.0); IS = np.full((ny, nx), -1, dtype=np.int32)    # saydam dahil
xc = X0 + (np.arange(nx) + 0.5) * R; yc = Y0 + (np.arange(ny) + 0.5) * R
for k, ((b, a, m, g), s) in enumerate(zip(idx, ch)):
    if b.startswith(HAR) and not b.startswith("CEK_"): continue
    bb = s.BoundingBox()
    if bb.zmax < -300 or bb.zmax > 200: continue
    if b.startswith("CEK_") and bb.zmax < 0: continue
    try:
        V, T = s.tessellate(1.0, 0.5)
    except Exception:
        continue
    if not T: continue
    P = np.array([(v.x, v.y, v.z) for v in V]); T = np.array(T)
    seffaf = (m == "on_seffaf")
    for t in T:
        p = P[t]
        xa, xb = p[:, 0].min(), p[:, 0].max(); ya, yb = p[:, 1].min(), p[:, 1].max()
        i0 = max(int(np.ceil((xa - X0) / R - 0.5)), 0); i1 = min(int(np.floor((xb - X0) / R - 0.5)), nx - 1)
        j0 = max(int(np.ceil((ya - Y0) / R - 0.5)), 0); j1 = min(int(np.floor((yb - Y0) / R - 0.5)), ny - 1)
        if i1 < i0 or j1 < j0: continue
        (x1_, y1_, z1_), (x2_, y2_, z2_), (x3_, y3_, z3_) = p
        den = (y2_ - y3_) * (x1_ - x3_) + (x3_ - x2_) * (y1_ - y3_)
        if abs(den) < 1e-9: continue
        X, Y = np.meshgrid(xc[i0:i1 + 1], yc[j0:j1 + 1])
        l1 = ((y2_ - y3_) * (X - x3_) + (x3_ - x2_) * (Y - y3_)) / den
        l2 = ((y3_ - y1_) * (X - x3_) + (x1_ - x3_) * (Y - y3_)) / den
        l3 = 1 - l1 - l2
        ins = (l1 >= -1e-6) & (l2 >= -1e-6) & (l3 >= -1e-6)
        if not ins.any(): continue
        z = l1 * z1_ + l2 * z2_ + l3 * z3_
        for ZZ, II in ((ZS, IS),) + (() if seffaf else ((ZA, IA),)):
            sub = ZZ[j0:j1 + 1, i0:i1 + 1]; si = II[j0:j1 + 1, i0:i1 + 1]
            up = ins & (z > sub)
            sub[up] = z[up]; si[up] = k
print("zbuf %.0f sn" % (time.time() - t0))
np.savez_compressed(OUT, ZA=ZA, IA=IA, ZS=ZS, IS=IS, X0=X0, Y0=Y0, R=R)
sys.stdout.flush(); os._exit(0)
