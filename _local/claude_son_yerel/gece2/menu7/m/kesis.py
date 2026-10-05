import os, sys, numpy as np, manifold3d as mf
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
K = S + r"\gece2\b4\52a"; sys.path[:0] = [K + r"\gece", K]; os.environ["YAMA_IS_KOK"] = K
from m8kit import Glb
g = Glb(sys.argv[1])
def M(d, no):
    b = g.bilesen(d, int(no)); P = np.concatenate([p["X"][p["T"][t]] for p, t in b["parca"]]).reshape(-1, 3)
    u, inv = np.unique(np.round(P, 4), axis=0, return_inverse=True)
    return mf.Manifold(mf.Mesh(vert_properties=u.astype(np.float32), tri_verts=inv.reshape(-1, 3).astype(np.uint32))), b
for a in sys.argv[2:]:
    x, y = a.split("~"); (d1, n1), (d2, n2) = x.rsplit(":", 1), y.rsplit(":", 1)
    m1, b1 = M(d1, n1); m2, b2 = M(d2, n2)
    print(a, "kutu1", b1["lo"].round(1), b1["hi"].round(1), "kutu2", b2["lo"].round(1), b2["hi"].round(1), "kesişim mm3", round((m1 ^ m2).volume(), 2), "status", m1.status(), m2.status())
