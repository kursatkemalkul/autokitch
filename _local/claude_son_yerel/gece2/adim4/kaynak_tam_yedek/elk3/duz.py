import numpy as np, json
from vox import *
A,B,C,P,ad,kpk=yukle()
for xf,zc in ((2500,-715),(4000,-615),(4400,-615)):
    lo=np.array([xf-40,1468,zc-62]); hi=np.array([xf+40,1602,zc+62])
    tlo=np.minimum(np.minimum(A,B),C); thi=np.maximum(np.maximum(A,B),C)
    m=np.all(thi>=lo,1)&np.all(tlo<=hi,1)
    n=np.cross(B-A,C-A); n/=np.maximum(np.linalg.norm(n,axis=1,keepdims=True),1e-12)
    print("== face",xf)
    for i in np.where(m)[0]:
        pass
    from collections import defaultdict
    d=defaultdict(int)
    for i in np.where(m)[0]:
        key=(ad[P[i]], round(float(A[i,0]),2) if abs(n[i,0])>0.99 else 'nonx')
        d[key]+=1
    for k,v in sorted(d.items(), key=lambda kv: str(kv[0][1])): print("  ",k,v)
