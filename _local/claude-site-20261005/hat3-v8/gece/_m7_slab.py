import sys, numpy as np
sys.path.insert(0,'.')
from glbkit import Glb
G=Glb(sys.argv[1]); nm=sys.argv[2]; ci=int(sys.argv[3]); ax=int(sys.argv[4]); a0=float(sys.argv[5]); a1=float(sys.argv[6])
p=G.bul(nm); tl,kut=G.komp(p); X=p['X']
m=(tl==ci)&G.gorunur(p); idx=np.where(m)[0]; C=X[p['T'][idx]]
s=((C[:,:,ax]>=a0)&(C[:,:,ax]<=a1)).all(1)
C=C[s]; n=np.cross(C[:,1]-C[:,0],C[:,2]-C[:,0]); n/=np.linalg.norm(n,axis=1,keepdims=True)+1e-12
print('slab tris',s.sum())
# group by dominant normal axis and plane coord
d=np.abs(n).argmax(1)
for k in range(3):
    mk=d==k
    if not mk.any(): continue
    pc=np.round(C[mk][:,0,k],1)
    for v in np.unique(pc):
        mm=mk.copy(); mm[mk]=(pc==v)
        Q=C[mm].reshape(-1,3); print('n%s=%7.1f  tris %4d  x %7.1f %7.1f y %7.1f %7.1f z %7.1f %7.1f'%('xyz'[k],v,mm.sum(),*np.ravel(list(zip(Q.min(0),Q.max(0))))))
