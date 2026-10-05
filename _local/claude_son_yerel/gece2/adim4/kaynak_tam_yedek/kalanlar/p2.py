import sys, json, numpy as np
from _env import *
import m8kit
sys.path.insert(0, S+r"\gece")
from m8t2_yaz import miter_tup
G = m8kit.Glb(S+r"\hat3_v8zh.glb")
Yo = json.load(open(S+r"\gece\m8t2\yollar_z2.json"))
for dug in ("ELK_ANA_HAT__kablo","ELK_ANA_HAT__kablo_veri"):
    ps=[p for p in G.dprims(dug) if not p.get("gizli")]
    X=np.concatenate([p["X"][p["T"][G.gorunur(p)]].reshape(-1,3) for p in ps])
    keys=set(map(bytes,np.round(X,1).astype(np.float32)))
    for a,d in Yo.items():
        if ("veri" in dug)!=(d["mal"]=="kablo_veri"): continue
        P=np.array(d["P"]); T=miter_tup(P,d["r"])
        # per segment: triangles 32 per segment
        n=16; bad=[]
        for i in range(len(P)-1):
            tri=T[i*2*n:(i+1)*2*n].reshape(-1,3)
            ok=np.mean([bytes(v) in keys for v in np.round(tri,1).astype(np.float32)])
            if ok<0.99: bad.append((i,round(ok,2),P[i].round(1).tolist(),P[i+1].round(1).tolist()))
        if bad: print(a, bad)
