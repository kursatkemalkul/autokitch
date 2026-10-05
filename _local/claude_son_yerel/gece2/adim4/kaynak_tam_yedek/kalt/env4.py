import sys,numpy as np
S=r"@@KOK_W@@"
sys.path.insert(0,S+r"\gece"); sys.path.insert(0,S)
import glbkit
G=glbkit.Glb(S+r"\hat3_v8zd.glb")
p=G.bul("K_GOVDE__sac"); tl,kut=G.komp(p)
P=p["X"][p["T"]]; m=(tl==20)&G.gorunur(p)
c=P.mean(1)
for y0,y1 in ((788,830),(830,865),(858,900)):
  mm=m&(c[:,1]>y0)&(c[:,1]<y1)
  Q=P[mm]
  # cluster by xz grid
  key=np.round(Q.mean(1)[:,[0,2]]/40).astype(int)
  u,inv=np.unique(key,axis=0,return_inverse=True)
  print("y",y0,y1,mm.sum())
  # sub-components of tris within slab via connectivity
  from scipy.sparse import coo_matrix
  from scipy.sparse.csgraph import connected_components
  V=np.round(Q.reshape(-1,3),2); uu,ii=np.unique(V,axis=0,return_inverse=True); ii=ii.reshape(-1,3)
  r=np.r_[ii[:,0],ii[:,1]]; cc=np.r_[ii[:,1],ii[:,2]]
  k,l=connected_components(coo_matrix((np.ones(len(r)),(r,cc)),shape=(len(uu),)*2))
  tlab=l[ii[:,0]]
  for j in np.unique(tlab):
    q=Q[tlab==j].reshape(-1,3); print("   n%4d lo %s hi %s"%((tlab==j).sum(),q.min(0).round(1),q.max(0).round(1)))
