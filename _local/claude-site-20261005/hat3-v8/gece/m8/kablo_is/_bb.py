import sys;sys.path.insert(0,'.')
import glbkit,numpy as np,collections
G=glbkit.Glb('../hat3_v8x.glb')
B=collections.defaultdict(lambda:[np.full(3,1e9),np.full(3,-1e9)])
for p in G.prims:
    v=G.gorunur(p)
    if not v.any(): continue
    P=p['X'][np.unique(p['T'][v])]
    b=p['name'].split('__')[0]
    B[b][0]=np.minimum(B[b][0],P.min(0));B[b][1]=np.maximum(B[b][1],P.max(0))
for b,(lo,hi) in sorted(B.items()):
    print("%-28s x %7.0f %7.0f y %7.0f %7.0f z %7.0f %7.0f"%(b,lo[0],hi[0],lo[1],hi[1],lo[2],hi[2]))
