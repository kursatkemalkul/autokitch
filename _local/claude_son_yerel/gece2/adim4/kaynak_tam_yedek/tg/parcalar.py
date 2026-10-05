import sys, pickle, numpy as np
sys.path.insert(0,'.')
from glbx import yukle
J,D=yukle(sys.argv[1]); R=pickle.load(open(sys.argv[2],'rb')); sec=sys.argv[3].split(',')
for ad in R:
    if not any(ad==s or (s.endswith('*') and ad.startswith(s[:-1])) for s in sec): continue
    d=D[ad]; X,T,ok=d['X'],d['T'],d['ok']; L=R[ad]
    print('=====',ad)
    for p in sorted(set(L[ok])):
        ti=np.where((L==p)&ok)[0]; Q=X[T[ti]].reshape(-1,3); mn=Q.min(0); mx=Q.max(0)
        print('  %-44s %6d  x%7.1f-%7.1f y%7.1f-%7.1f z%7.1f-%7.1f'%(p,len(ti),mn[0],mx[0],mn[1],mx[1],mn[2],mx[2]))
