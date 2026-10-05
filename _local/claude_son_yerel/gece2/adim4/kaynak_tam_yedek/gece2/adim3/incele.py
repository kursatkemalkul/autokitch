# -*- coding: utf-8 -*-
import os, sys, numpy as np
S = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, S)
import govde_denetim_dogru as G
glb = sys.argv[1]; a_ad, b_ad = sys.argv[2], sys.argv[3]; cx = float(sys.argv[4])
D = G.glb_oku(glb)
def bil(ad):
    nd, no = ad[:-1].split("["); return [b for b in G.bilesenler(nd, D[nd]) if b.no == int(no)][0]
A, B = bil(a_ad), bil(b_ad)
# A yuzeyini incelt, B icinde olanlar
lo = np.maximum(A.lo, B.lo) - 0.1; hi = np.minimum(A.hi, B.hi) + 0.1
for X, Y, n in ((A, B, "A yuzeyi B icinde"), (B, A, "B yuzeyi A icinde")):
    if not Y.kapali: continue
    Q = G.ornekle(X.P, lo, hi, 0.3)[0]
    if not len(Q): continue
    m = G.icerde(Y.yz(), Q); Q = Q[m]; d0 = G.yuzey_uzaklik(Y.yz(), Q) if len(Q) else None; Q = Q[d0 > 0.05] if len(Q) else Q
    if not len(Q): print(n, 0); continue
    d = G.yuzey_uzaklik(Y.yz(), Q)
    L = Q - np.array([cx, 1152.0, -362.5])
    r = np.hypot(L[:, 0], L[:, 1] - float(sys.argv[5])) if len(sys.argv) > 5 else None
    print(n, len(Q), "derin max %.3f" % d.max())
    print("  yerel x %.1f..%.1f y %.1f..%.1f z %.2f..%.2f" % (L[:, 0].min(), L[:, 0].max(), L[:, 1].min(), L[:, 1].max(), L[:, 2].min(), L[:, 2].max()))
    if r is not None:
        ang = np.degrees(np.arctan2(L[:, 1] - float(sys.argv[5]), L[:, 0]))
        print("  r %.2f..%.2f  aci %.1f..%.1f" % (r.min(), r.max(), ang.min(), ang.max()))
    i = np.argsort(-d)[:8]
    for k in i: print("   ", np.round(L[k], 2).tolist(), round(float(d[k]), 3))
