import sys, numpy as np
sys.path.insert(0,'.')
from glb import G, bilesen
g=G('../../hat3_v9j.glb')
lo=np.array([1400,380,-830.]); hi=np.array([2110,520,100.])
for nm in ['ELK_DOLAP__kablo','ELK_DOLAP__kablo_sinyal','CEK_K2_lahm_3__on_seffaf__CEKMECE','ELK_DOLAP__celik']:
    ni=g.byname[nm]
    for pi,(X,T,mek,mat,ex) in enumerate(g.tris(ni)):
        cl=bilesen(X,T); P=X[T]
        kpk=np.zeros(len(T),bool); L=ex.get('kpk') or []
        for k in range(0,len(L)-1,2): kpk[L[k]//3:(L[k]+L[k+1])//3]=True
        for c in np.unique(cl):
            m=cl==c; Q=P[m].reshape(-1,3); a=Q.min(0); b=Q.max(0)
            if np.all(b>lo) and np.all(a<hi) and np.max(b-a)>5:
                print(nm,pi,'lo',np.round(a,1),'sz',np.round(b-a,1),'n',int(m.sum()),'kpk',int(kpk[m].sum()))
