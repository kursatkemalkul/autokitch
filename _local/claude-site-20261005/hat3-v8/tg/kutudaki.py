import sys, pickle, numpy as np
sys.path.insert(0,'.')
from glbx import yukle
J,D=yukle(sys.argv[1]); R=pickle.load(open(sys.argv[2],'rb')); k=[float(v) for v in sys.argv[3].split(',')]
tam = len(sys.argv)>4
for ad,d in D.items():
    X,T,ok=d['X'],d['T'],d['ok']; P=X[T]; c=P.mean(1)
    m=ok&(c[:,0]>k[0])&(c[:,0]<k[1])&(c[:,1]>k[2])&(c[:,1]<k[3])&(c[:,2]>k[4])&(c[:,2]<k[5])
    if not m.any(): continue
    L=R.get(ad, np.array(['-']*len(T),dtype=object))
    for p in sorted(set(L[m])):
        ti=np.where(ok&(L==p))[0] if p!='-' else np.where(m)[0]
        Q=X[T[ti]].reshape(-1,3); mn=Q.min(0); mx=Q.max(0)
        print('%-28s %-44s %6d x%7.1f-%7.1f y%7.1f-%7.1f z%7.1f-%7.1f'%(ad[:28],p,len(ti),mn[0],mx[0],mn[1],mx[1],mn[2],mx[2]))
