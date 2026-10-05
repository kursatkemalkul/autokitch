import sys, json, numpy as np
sys.path.insert(0, r"@@KOK_F@@/tg")
from glbx import yukle
J, D = yukle(sys.argv[1])
for n, d in D.items():
    if n.startswith("E_") or n.startswith("ELK_E") or "_E_" in n or n.startswith("KAIDE_E") :
        X=d["X"]; T=d["T"][d["ok"]]
        if len(T)==0: print(n, "BOS"); continue
        Q=X[T].reshape(-1,3); mn=Q.min(0); mx=Q.max(0)
        print("%-34s tri %7d  x %.1f..%.1f y %.1f..%.1f z %.1f..%.1f  ex=%s rot=%s" % (n, len(T), mn[0],mx[0],mn[1],mx[1],mn[2],mx[2], {k:(v[:6] if isinstance(v,list) else v) for k,v in d["ex"].items()}, d["rot"]))
