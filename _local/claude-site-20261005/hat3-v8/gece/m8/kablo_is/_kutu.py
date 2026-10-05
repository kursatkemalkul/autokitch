import sys,numpy as np
sys.path.insert(0,'../..')
import glbkit
G=glbkit.Glb('../../../hat3_v8x.glb')
Q=[(1040,1100,900,935,-40,0,'x sol limit/home sensör'),(4975,4990,620,640,670,690,'goz_00 isitici'),(1440,1600,1440,1560,-820,-650,'surucu bolgesi'),(2400,2470,1270,1320,-830,-780,'KD1 valf adasi ucu')]
for x0,x1,y0,y1,z0,z1,ad in Q:
    print('==',ad)
    for p in G.prims:
        v=G.gorunur(p)
        if not v.any(): continue
        tl,k=G.komp(p)
        for c,(lo,hi,n) in k.items():
            if hi[0]>=x0 and lo[0]<=x1 and hi[1]>=y0 and lo[1]<=y1 and hi[2]>=z0 and lo[2]<=z1 and (hi-lo).max()<400:
                print('  ',p['name'],c,np.round(lo).astype(int),np.round(hi).astype(int))
