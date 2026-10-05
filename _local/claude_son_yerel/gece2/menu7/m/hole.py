import os, sys, numpy as np
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
K = S + r"\gece2\b4\52a"; sys.path[:0] = [K + r"\gece", K]; os.environ["YAMA_IS_KOK"] = K
from m8kit import Glb
g = Glb(K + r"\hat3_v9t.glb")
for a in sys.argv[1:]:
    d, no, cx, cz, r = a.split(":"); cx, cz, r = float(cx), float(cz), float(r)
    b = g.bilesen(d, int(no)); P = np.concatenate([p["X"][p["T"][t]] for p, t in b["parca"]]).reshape(-1, 3)
    m = (np.abs(P[:, 0] - cx) < r) & (np.abs(P[:, 2] - cz) < r); Q = np.unique(np.round(P[m], 1), axis=0)
    rr = np.hypot(Q[:, 0] - cx, Q[:, 2] - cz)
    print(a, "n", len(Q), "y", np.unique(Q[:, 1])[:20], "r", np.unique(np.round(rr, 1))[:20])
