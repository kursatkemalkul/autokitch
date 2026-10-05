import sys; sys.path.insert(0,'.')
from glbx import yukle
import numpy as np
J,D=yukle(sys.argv[1]); k=[float(v) for v in sys.argv[2].split(',')]
for ad,d in D.items():
    X,T=d['X'],d['T'][d['ok']]
    P=X[T]; c=P.mean(1)
    m=(c[:,0]>k[0])&(c[:,0]<k[1])&(c[:,1]>k[2])&(c[:,1]<k[3])&(c[:,2]>k[4])&(c[:,2]<k[5])
    if m.sum()==0: continue
    Q=P[m].reshape(-1,3); mn=Q.min(0); mx=Q.max(0)
    print("%-42s %7d/%7d x%7.1f-%7.1f y%7.1f-%7.1f z%7.1f-%7.1f"%(ad,m.sum(),len(T),mn[0],mx[0],mn[1],mx[1],mn[2],mx[2]))
