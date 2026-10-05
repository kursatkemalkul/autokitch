import sys, numpy as np
sys.path.insert(0,"."); import govde_denetim_dogru as GD
D=GD.glb_oku("hat3_v8r.glb")
for (y,z) in ((877,-100),(1100,-800),(1750,-800)):
    lo=np.array([4401.5,y-9,z-9]); hi=np.array([4416,y+9,z+9])
    out=[]
    for nd,P in D.items():
        if nd.startswith("E_GOVDE") or not len(P): continue
        Q=P.reshape(-1,3)
        if (Q.min(0)>hi).any() or (Q.max(0)<lo).any(): continue
        for b in GD.bilesenler(nd,P):
            if (b.lo>hi).any() or (b.hi<lo).any(): continue
            out.append((nd,b.no,b.lo.round(1).tolist(),b.hi.round(1).tolist()))
    print((y,z),out, flush=True)
import os; os._exit(0)
