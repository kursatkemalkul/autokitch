# ön görünüş derinlik haritası (bbox ile): her (x,y) hücresinde en öndeki parçanın zmax'ı
import json, io, sys
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
L = json.load(io.open(sys.argv[1], encoding="utf-8"))
X0, X1, Y0, Y1, R = 700, 5300, 0, 2220, 2.0
nx, ny = int((X1 - X0) / R), int((Y1 - Y0) / R)
Z = np.full((ny, nx), -900.0)
HAR = tuple(sys.argv[3].split(",")) if len(sys.argv) > 3 and sys.argv[3] else ()
for b, a, m, g, bb in L:
    if b.startswith(("QR_", "TEZGAH", "ROBOT", "ELK_QR", "ELK_ANA_PANO", "ELK_ZEMIN", "DUZ_TEZGAH", "INSAN")) or b.startswith(HAR): continue
    if m == "on_seffaf": pass
    x0, x1, y0, y1, z0, z1 = bb
    if z1 > 200: continue
    i0, i1 = int((x0 - X0) / R), int(np.ceil((x1 - X0) / R)); j0, j1 = int((y0 - Y0) / R), int(np.ceil((y1 - Y0) / R))
    i0, j0 = max(i0, 0), max(j0, 0)
    sl = Z[j0:j1, i0:i1]
    np.maximum(sl, z1, out=sl)
np.save(sys.argv[2] + ".npy", Z)
fig, ax = plt.subplots(figsize=(28, 14))
im = ax.imshow(Z, origin="lower", extent=(X0, X1, Y0, Y1), cmap="nipy_spectral", vmin=-100, vmax=80, aspect="equal")
plt.colorbar(im, ax=ax, fraction=0.02)
ax.set_xticks(range(700, 5301, 100)); ax.set_yticks(range(0, 2201, 100)); ax.grid(True, lw=0.3, color="w")
plt.xticks(rotation=90, fontsize=6); plt.yticks(fontsize=6)
plt.savefig(sys.argv[2] + ".png", dpi=110, bbox_inches="tight")
print("ok")
