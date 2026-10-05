import sys,numpy as np
sys.path.insert(0,'.'); from elib import *
import glbkit
G=glbkit.Glb(sys.argv[1]); ad=sys.argv[2]; lo=np.array(eval(sys.argv[3])); hi=np.array(eval(sys.argv[4]))
for p in G.prims:
    if p['name']!=ad: continue
    P=p['X'][p['T']]; vis=G.gorunur(p)
    m=vis&np.all(P.max(1)>=lo,1)&np.all(P.min(1)<=hi,1)
    nn=np.cross(P[:,1]-P[:,0],P[:,2]-P[:,0]); nn/=np.maximum(np.linalg.norm(nn,axis=1,keepdims=True),1e-12)
    for i in np.where(m)[0][:80]: print(np.round(P[i].min(0),1),np.round(P[i].max(0),1),np.round(nn[i],2))
