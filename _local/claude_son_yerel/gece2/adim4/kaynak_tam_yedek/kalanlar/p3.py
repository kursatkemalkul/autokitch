import sys, json, numpy as np
from scipy.spatial import cKDTree
from _env import *
import m8kit
sys.path.insert(0, S+r"\gece")
from m8t2_yaz import miter_tup
G = m8kit.Glb(S+r"\hat3_v8zh.glb")
Yo = json.load(open(S+r"\gece\m8t2\yollar_z2.json"))
for dug in ("ELK_ANA_HAT__kablo","ELK_ANA_HAT__kablo_veri"):
    p=[p for p in G.dprims(dug) if not p.get("gizli")][0]
    T=p["T"][G.gorunur(p)]; V=p["X"][np.unique(T)]
    names=[a for a,d in Yo.items() if ("veri" in dug)==(d["mal"]=="kablo_veri")]
    Q=[];lab=[]
    for a in names:
        q=miter_tup(np.array(Yo[a]["P"]),Yo[a]["r"]).reshape(-1,3); Q.append(q); lab+= [a]*len(q)
    Q=np.vstack(Q); lab=np.array(lab)
    d,i=cKDTree(Q).query(V)
    print(dug,"GLB vertex",len(V),"eslesmeyen(>0.05)",(d>0.05).sum(), "max",d.max().round(3))
    if (d>0.05).sum(): Vb=V[d>0.05]; print(Vb.min(0).round(1),Vb.max(0).round(1))
    d2,i2=cKDTree(V).query(Q)
    import collections
    print(" z2 tarafinda eksik:",collections.Counter(lab[d2>0.05]))
