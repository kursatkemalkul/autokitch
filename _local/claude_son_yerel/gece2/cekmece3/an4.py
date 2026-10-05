import sys,numpy as np,pickle
sys.path.insert(0,'../cekmece'); sys.stdout.reconfigure(encoding='utf-8')
from glb import G,bilesen
g=G('../../hat3_v9k.glb')
LO=np.array([1440,455,-800.]);HI=np.array([1500,500,10.])
for i,n in enumerate(g.J['nodes']):
    if 'mesh' not in n: continue
    nm=n.get('name','')
    for X,T,mek,mat,ex in g.tris(i):
        P=X[T]; c=P.reshape(-1,3)
        if not (np.any(np.all((c>=LO)&(c<=HI),1))): continue
        cl=bilesen(X,T)
        for k in np.unique(cl):
            Q=P[cl==k].reshape(-1,3); lo,hi=Q.min(0),Q.max(0)
            if np.all(hi>=LO) and np.all(lo<=HI) and (hi-lo).max()<3000 and (hi-lo).max()>1:
                print('%-34s %5d lo %s hi %s'%(nm,(cl==k).sum(),np.round(lo,2),np.round(hi,2)))
