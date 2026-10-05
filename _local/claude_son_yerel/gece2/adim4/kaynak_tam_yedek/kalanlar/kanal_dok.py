import numpy as np, json, sys
from _env import *
import m8kit
G=m8kit.Glb(S+r"\hat3_v8zh.glb")
lo=np.array(eval(sys.argv[1])); hi=np.array(eval(sys.argv[2]))
for p in G.dprims("ELK_ANA_HAT__paslanmaz"):
    if p.get("gizli"): continue
    tl,kut=G.komp(p); vis=G.gorunur(p)
    P=p["X"][p["T"]]; mn=P.min(1); mx=P.max(1)
    m=vis&np.all(mx>lo,1)&np.all(mn<hi,1)
    for c in np.unique(tl[m]):
        a,b,n=kut[c]
        print("komp",c,"n",n,np.round(a,2).tolist(),np.round(b,2).tolist(), "bolgede",int((m&(tl==c)).sum()), "kpk", bool(G.kpk_maske(p)[np.where(tl==c)[0][0]]) if p["pr"].get("extras",{}).get("kpk") else None)
