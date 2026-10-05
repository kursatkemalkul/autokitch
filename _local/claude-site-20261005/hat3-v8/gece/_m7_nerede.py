import sys, numpy as np
sys.path.insert(0,'.')
from glbkit import Glb
G=Glb(sys.argv[1]); p=G.bul(sys.argv[2]); b=list(map(float,sys.argv[3].split(',')))
C=p['X'][p['T']]; vis=G.gorunur(p)
m=vis&(C[:,:,0]>=b[0]).all(1)&(C[:,:,0]<=b[1]).all(1)&(C[:,:,1]>=b[2]).all(1)&(C[:,:,1]<=b[3]).all(1)&(C[:,:,2]>=b[4]).all(1)&(C[:,:,2]<=b[5]).all(1)
k=p['pr']['extras'].get('kat',[])
idx=np.where(m)[0]
for i in range(0,len(k),3):
    a=k[i+1]//3; n=k[i+2]//3; s=((idx>=a)&(idx<a+n)).sum()
    if s: print('range',a,n,'->',s)
