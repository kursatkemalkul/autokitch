import sys, numpy as np, time
S=r"@@KOK_W@@"
sys.path.insert(0,S+r"\gece"); sys.path.insert(0,S)
import m8kit
t=time.time(); G=m8kit.Glb(S+r"\hat3_v8zk.glb"); print("yuk",time.time()-t)
import re, collections
d=collections.OrderedDict()
for p in G.prims:
    if p.get("gizli"): continue
    nm=p["name"]
    if not re.search(r"kablo|hortum|kanal|kelepce|sinyal|rakor|hava",nm,re.I): continue
    vis=G.gorunur(p); P=p["X"][p["T"][vis]]
    if not len(P): continue
    lo=P.reshape(-1,3).min(0); hi=P.reshape(-1,3).max(0)
    print("%-45s %7d  lo %s hi %s"%(nm,len(P),np.round(lo).astype(int).tolist(),np.round(hi).astype(int).tolist()))
