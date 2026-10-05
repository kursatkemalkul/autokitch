import sys,numpy as np
sys.stdout.reconfigure(encoding='utf-8')
from glb import G, bilesen
g=G('../../hat3_v9j.glb')
for nm in ['B_KABLO__kanal','ELK_IC__kanal']:
    ni=g.byname[nm]
    for X,T,mek,mat,ex in g.tris(ni):
        P=X[T]; lo=P.min(1); hi=P.max(1)
        m=np.all(hi>=[1600,392,-800],1)&np.all(lo<=[1720,522,-700],1)
        if m.any():
            Q=P[m].reshape(-1,3); print(nm, ex, np.round(Q.min(0),1), np.round(Q.max(0),1))
            cl=bilesen(X,T[m]) if False else None
