import sys, numpy as np
sys.path.insert(0,'.')
from glb import G, bilesen
g=G('../../hat3_v9j.glb')
ni=g.byname['CEK_K2_lahm_3__celik']
X,T,mek,mat,ex=g.tris(ni)[0]
cl=bilesen(X,T)
P=X[T]
for c in np.unique(cl):
    m=cl==c; Q=P[m].reshape(-1,3)
    if abs(Q.min(0)[0]-1454.5)<0.2 and np.ptp(Q,0)[2]>700:
        # sub-cluster triangles by bbox overlap without shared verts: print triangles grouped by z rounded
        cen=P[m].mean(1)
        print(len(cen))
        tri=P[m]
        # group via rounding of tri bbox
        import collections
        grp=collections.defaultdict(list)
        for t in tri:
            lo=t.min(0); hi=t.max(0)
            grp[(round(lo[0],1),round(hi[0],1),round(lo[1],1),round(hi[1],1))].append((round(lo[2],1),round(hi[2],1)))
        for k,v in sorted(grp.items()): print(k, len(v), sorted(set(v))[:12])
