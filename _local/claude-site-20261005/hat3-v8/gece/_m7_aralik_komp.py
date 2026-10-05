import sys, numpy as np
sys.path.insert(0,'.')
from glbkit import Glb
G=Glb(sys.argv[1]); p=G.bul(sys.argv[2]); a=int(sys.argv[3]); n=int(sys.argv[4])
tl,kut=G.komp(p); vis=G.gorunur(p)
m=np.zeros(len(p['T']),bool); m[a:a+n]=True; m&=vis
for c in np.unique(tl[m]):
    mm=m&(tl==c); outside=((tl==c)&vis&~m).sum()
    Q=p['X'][p['T'][mm]].reshape(-1,3); lo=Q.min(0); hi=Q.max(0)
    print('#%-5d tris %5d (disarida %d)  x %7.1f %7.1f y %7.1f %7.1f z %7.1f %7.1f'%(c,mm.sum(),outside,lo[0],hi[0],lo[1],hi[1],lo[2],hi[2]))
