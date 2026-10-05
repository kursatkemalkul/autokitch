import sys, json, numpy as np
from _env import *
import m8kit
sys.path.insert(0, S+r"\gece")
from m8t2_yaz import miter_tup
G = m8kit.Glb(S+r"\hat3_v8zh.glb")
Yo = json.load(open(S+r"\gece\m8t2\yollar_z2.json"))
for dug in ("ELK_ANA_HAT__kablo","ELK_ANA_HAT__kablo_veri"):
    ps=[p for p in G.dprims(dug) if not p.get("gizli")]
    print(dug, len(ps), [len(p["T"]) for p in ps])
    X=np.concatenate([p["X"][p["T"][G.gorunur(p)]].reshape(-1,3) for p in ps])
    keys=set(map(bytes,np.round(X,1).astype(np.float32)))
    for a,d in Yo.items():
        if ("veri" in dug)!=(d["mal"]=="kablo_veri"): continue
        T=miter_tup(np.array(d["P"]),d["r"]).reshape(-1,3)
        k=[bytes(v) for v in np.round(T,1).astype(np.float32)]
        print("  %-13s %.2f eslesen"%(a, np.mean([q in keys for q in k])))
