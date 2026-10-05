import sys, numpy as np
sys.path.insert(0,'.')
from glbkit import Glb
G=Glb(sys.argv[1]); p=G.bul(sys.argv[2]); a=int(sys.argv[3]); n=int(sys.argv[4]); ci=int(sys.argv[5]) if len(sys.argv)>5 else None
tl,kut=G.komp(p); vis=G.gorunur(p)
m=np.zeros(len(p['T']),bool); m[a:a+n]=True; m&=vis
if ci is not None: m&=(tl==ci)
C=p['X'][p['T'][m]]; nrm=np.cross(C[:,1]-C[:,0],C[:,2]-C[:,0]); nrm/=np.linalg.norm(nrm,axis=1,keepdims=True)+1e-12
d=np.abs(nrm).argmax(1)
for k in range(3):
    mk=d==k; pc=np.round(C[mk][:,0,k],2)
    for v in np.unique(pc):
        mm=mk.copy(); mm[mk]=(pc==v); Q=C[mm].reshape(-1,3)
        print('n%s=%8.2f tris %4d  x %7.1f %7.1f y %7.1f %7.1f z %7.1f %7.1f'%('xyz'[k],v,mm.sum(),Q[:,0].min(),Q[:,0].max(),Q[:,1].min(),Q[:,1].max(),Q[:,2].min(),Q[:,2].max()))
