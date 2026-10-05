import sys, json, numpy as np
sys.path.insert(0, r"@@KOK_F@@/tg")
from glbx import yukle
J, D = yukle(sys.argv[1])
x0,x1=float(sys.argv[2]),float(sys.argv[3])
for n, d in D.items():
    X=d["X"]; T=d["T"][d["ok"]]
    if len(T)==0: continue
    Q=X[T].reshape(-1,3)
    # fraction of verts in x-range
    m=((Q[:,0]>=x0)&(Q[:,0]<=x1)).mean()
    if m>0.0:
        mn=Q.min(0); mx=Q.max(0)
        print("%-40s tri %7d frac %.2f x %.1f..%.1f y %.1f..%.1f z %.1f..%.1f" % (n, len(T), m, mn[0],mx[0],mn[1],mx[1],mn[2],mx[2]))
