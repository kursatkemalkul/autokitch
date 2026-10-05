import sys, numpy as np
sys.path.insert(0,'.')
from glbkit import Glb
G=Glb(sys.argv[1]); nm=sys.argv[2]; ci=int(sys.argv[3]); xmax=float(sys.argv[4])
p=G.bul(nm); tl,kut=G.komp(p)
m=(tl==ci)&G.gorunur(p); T=p['T'][m]; X=p['X']
# triangles with all verts x<xmax
c=X[T]; sel=(c[:,:,0]<xmax).all(1)
print('tri total',m.sum(),'left tris',sel.sum(), 'tris touching left', (c[:,:,0]<xmax).any(1).sum())
V=np.unique(np.round(c[(c[:,:,0]<xmax).any(1)].reshape(-1,3),1),axis=0)
for ax,n in ((0,'x'),(1,'y'),(2,'z')): print(n, np.unique(V[V[:,0]<xmax][:,ax]))
