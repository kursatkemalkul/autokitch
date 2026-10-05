import sys, numpy as np, pickle
sys.path.insert(0, r"@@KOK_F@@/tg")
from glbx import yukle
J,D=yukle("hat3_v8p.glb")
X0=4400
walls={"sol":(X0,X0+1.5,123,1860.5,-828.5,59),"sag":(X0+828.5,X0+830,123,1860.5,-828.5,59),"arka":(X0,X0+830,123,1862,-830,-828.5),
 "tavan":(X0,X0+830,1860.5,1862,-828.5,59),"taban":(X0+1.5,X0+828.5,123,126,-828.5,59)}
for bn,b in walls.items():
    lo=np.array(b[0::2]); hi=np.array(b[1::2])
    print("==",bn)
    for nd,d in D.items():
        if nd.startswith("E_GOVDE__"): continue
        P=d["X"][d["T"][d["ok"]]]
        if not len(P): continue
        # triangles with a vertex strictly inside wall slab
        V=P.reshape(-1,3)
        m=((V>lo+0.01)&(V<hi-0.01)).all(1)
        if m.any():
            Q=V[m]; print("   %-34s %5d  %s %s"%(nd,m.sum(),Q.min(0).round(1).tolist(),Q.max(0).round(1).tolist()))
