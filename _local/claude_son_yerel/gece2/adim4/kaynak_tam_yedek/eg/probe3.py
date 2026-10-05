import sys, numpy as np
sys.path.insert(0, r"@@KOK_F@@/tg")
from glbx import yukle
J,D=yukle(sys.argv[1] if len(sys.argv)>1 else "hat3_v8p.glb")
X0=4400
walls={"sol":(0,X0+0.75,(123,1860.5),(-828.5,59)),"sag":(0,X0+829.25,(123,1860.5),(-828.5,59)),"arka":(2,-829.25,(X0,X0+830),(123,1862)),
 "tavan":(1,1861.25,(X0,X0+830),(-828.5,59)),"taban":(1,124.5,(X0+1.5,X0+828.5),(-828.5,59))}
for bn,(ax,c,ra,rb) in walls.items():
    o=[a for a in range(3) if a!=ax]
    print("==",bn)
    for nd,d in D.items():
        if nd.startswith("E_GOVDE__"): continue
        P=d["X"][d["T"][d["ok"]]]
        if not len(P): continue
        m=(P[:,:,ax].min(1)<c)&(P[:,:,ax].max(1)>c)
        m&=(P[:,:,o[0]].max(1)>ra[0]+0.5)&(P[:,:,o[0]].min(1)<ra[1]-0.5)&(P[:,:,o[1]].max(1)>rb[0]+0.5)&(P[:,:,o[1]].min(1)<rb[1]-0.5)
        if m.any():
            Q=P[m].reshape(-1,3); print("   %-34s %5d  %s %s"%(nd,m.sum(),Q.min(0).round(1).tolist(),Q.max(0).round(1).tolist()))
