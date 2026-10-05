import sys, json, io, numpy as np
from scipy import ndimage
D = np.load(sys.argv[1]); key = sys.argv[2]; esik = float(sys.argv[3]) if len(sys.argv) > 3 else -300.0
Z = D[key]; I = D["I" + key[1]]; X0, Y0, R = float(D["X0"]), float(D["Y0"]), float(D["R"])
idx = json.load(io.open(sys.argv[4], encoding="utf-8")) if len(sys.argv) > 4 else None
ny, nx = Z.shape
xc = X0 + (np.arange(nx) + 0.5) * R; yc = Y0 + (np.arange(ny) + 0.5) * R
X, Y = np.meshgrid(xc, yc)
zarf = (X > 736) & (X < 5230) & (Y > 0) & (Y < 2200)
bos = (Z < esik) & zarf
lab, n = ndimage.label(bos)
out = []
for k, sl in enumerate(ndimage.find_objects(lab), 1):
    m = lab[sl] == k
    h, w = m.shape
    if w * R < 10 or h * R < 10: continue
    x0, x1 = X0 + sl[1].start * R, X0 + sl[1].stop * R; y0, y1 = Y0 + sl[0].start * R, Y0 + sl[0].stop * R
    # çevredeki en öndeki parçalar
    js, is_ = sl[0], sl[1]
    J0, J1 = max(js.start - 3, 0), min(js.stop + 3, ny); I0, I1 = max(is_.start - 3, 0), min(is_.stop + 3, nx)
    kom = set(int(v) for v in np.unique(I[J0:J1, I0:I1]) if v >= 0)
    out.append((m.sum() * R * R, x0, x1, y0, y1, [idx[v][0] + "|" + idx[v][1] for v in list(kom)[:8]] if idx else []))
for a, x0, x1, y0, y1, k in sorted(out, reverse=True):
    print("BOSLUK alan %8.0f mm2  x %6.0f-%6.0f  y %6.0f-%6.0f   komsu: %s" % (a, x0, x1, y0, y1, k))
