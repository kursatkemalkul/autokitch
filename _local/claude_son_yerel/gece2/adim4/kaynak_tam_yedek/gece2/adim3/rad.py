import os, sys, numpy as np
S = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, S)
import govde_denetim_dogru as G
D = G.glb_oku(sys.argv[1]); ad = sys.argv[2]; cx, cy = float(sys.argv[3]), float(sys.argv[4])
nd, no = ad[:-1].split("["); b = [b for b in G.bilesenler(nd, D[nd]) if b.no == int(no)][0]
V = b.V - np.array([cx, 1152 + cy, -362.5]); r = np.hypot(V[:, 0], V[:, 1])
for z in sorted(set(np.round(V[:, 2], 2))):
    m = np.abs(V[:, 2] - z) < 0.01
    rr = np.unique(np.round(r[m], 2))
    print("z %.2f n %d r: %s" % (z, m.sum(), rr[:12].tolist() if len(rr) < 30 else (rr.min(), rr.max(), len(rr))))
