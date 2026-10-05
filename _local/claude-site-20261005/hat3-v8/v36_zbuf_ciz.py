import sys, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
D = np.load(sys.argv[1]); key = sys.argv[2]; out = sys.argv[3]
ext = [float(a) for a in sys.argv[4].split(",")] if len(sys.argv) > 4 else None
Z = D[key].copy(); X0, Y0, R = float(D["X0"]), float(D["Y0"]), float(D["R"])
ny, nx = Z.shape
Z[Z < -1500] = np.nan
fig, ax = plt.subplots(figsize=(26, 13))
cm = matplotlib.colormaps["nipy_spectral"].copy(); cm.set_bad("white")
im = ax.imshow(Z, origin="lower", extent=(X0, X0 + nx * R, Y0, Y0 + ny * R), cmap=cm, vmin=-830, vmax=80, aspect="equal", interpolation="nearest")
plt.colorbar(im, ax=ax, fraction=0.02)
if ext: ax.set_xlim(ext[0], ext[1]); ax.set_ylim(ext[2], ext[3])
x0, x1 = ax.get_xlim(); y0, y1 = ax.get_ylim()
st = 100 if (x1 - x0) > 1500 else 20
ax.set_xticks(np.arange(int(x0 / st) * st, x1, st)); ax.set_yticks(np.arange(int(y0 / st) * st, y1, st))
ax.grid(True, lw=0.3, color="k"); plt.xticks(rotation=90, fontsize=6); plt.yticks(fontsize=6)
plt.savefig(out, dpi=100, bbox_inches="tight")
