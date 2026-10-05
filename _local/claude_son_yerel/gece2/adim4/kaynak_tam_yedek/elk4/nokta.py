import sys,numpy as np
sys.path.insert(0,r"@@KOK_W@@\elk4")
from ortam4 import Ortam
O=Ortam()
for a in sys.argv[1:]:
    p=np.array([float(v) for v in a.split(",")])
    print("NOKTA",p)
    for d in np.vstack([np.eye(3),-np.eye(3)]):
        t,i=O.isin(p,d,300,O.yapi)
        print("  ",d.astype(int).tolist(),"%.1f"%t,O.nm[i] if i>=0 else "-")
