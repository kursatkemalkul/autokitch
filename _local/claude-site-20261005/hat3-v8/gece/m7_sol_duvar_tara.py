# -*- coding: utf-8 -*-
"""sol duvar bolgesindeki (x 1430-1500, y>=1105, z -632..40) koseleri olan bilesenler + koselerin x seviyeleri"""
import sys, numpy as np
sys.path.insert(0,'.')
from glbkit import Glb
G=Glb(sys.argv[1])
for p in G.prims:
    X=p['X']
    if X.size==0: continue
    if not p['name'].startswith(('TOPPING','ELK_TOPPING','A_','U_','ELK_ANA')): continue
    a=X.min(0);b=X.max(0)
    if b[0]<1425 or a[0]>1505 or b[1]<1100: continue
    tl,kut=G.komp(p)
    for i,(lo,hi,n) in kut.items():
        if hi[0]<1425 or lo[0]>1505 or hi[1]<1100 or lo[2]>45 or hi[2]<-635: continue
        m=(tl==i)&G.gorunur(p); vs=np.unique(p['T'][m].reshape(-1)); V=X[vs]
        k=(V[:,0]>1425)&(V[:,0]<1500)&(V[:,1]>=1105)&(V[:,2]>=-632)&(V[:,2]<=40)
        if not k.any(): continue
        xs=np.unique(np.round(V[k,0],1)); 
        print("%-30s #%-5d %5d x %7.1f %7.1f y %7.1f %7.1f z %7.1f %7.1f | x-lev %s | ylo<1105:%d"%(p['name'],i,n,lo[0],hi[0],lo[1],hi[1],lo[2],hi[2],xs[:8],(V[:,1]<1105).sum()))
