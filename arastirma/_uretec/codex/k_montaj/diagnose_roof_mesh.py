from lower_support import *
Y=H/'yama_v9'
for p in (Y,Y/'kaynak',Y/'kaynak/gece'):sys.path.insert(0,str(p))
from m8kit import Glb
import manifold3d as mf
root=Path('_local/codex_k_montaj/chain73/A')
for name in ('hat3_v10m.glb','hat3_v10q.glb'):
 g=Glb(str(root/name));g.bilesen('K_GOVDE__kabuk',0)
 for b in g._bc['K_GOVDE__kabuk']:
  if abs(b['hi'][1]-1862)<.05 and b['hi'][0]-b['lo'][0]>399 and b['hi'][2]-b['lo'][2]>880:
   P=np.concatenate([p['X'][p['T'][idx]] for p,idx in b['parca']])-np.array([4200.,1853.,-828.5])
   for decimals in (4,3,2):
    V,inv=np.unique(np.round(P.reshape(-1,3),decimals),axis=0,return_inverse=True);F=inv.reshape(-1,3);F=F[(F[:,0]!=F[:,1])&(F[:,1]!=F[:,2])&(F[:,0]!=F[:,2])]
    edges=np.sort(np.concatenate((F[:,[0,1]],F[:,[1,2]],F[:,[2,0]])),axis=1);e,c=np.unique(edges,axis=0,return_counts=True)
    solid=mf.Manifold(mf.Mesh(vert_properties=V.astype(np.float32),tri_verts=F.astype(np.uint32)))
    print(name,decimals,'bbox',b['lo'],b['hi'],'triangles',len(F),'bad_edges',int(np.count_nonzero(c!=2)),'status',solid.status(),flush=True)
 del g
os._exit(0)
