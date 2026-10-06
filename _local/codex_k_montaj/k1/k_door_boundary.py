"""Inspect residual door boundary edges against current source owners only."""
from pathlib import Path
import pickle,json,hashlib
import numpy as np
from scipy.spatial import cKDTree
H=Path(__file__).resolve().parent
P=pickle.load((H/'k_parca.pkl').open('rb'))['P'];a='k_govde_on_seffaf_1';p=P[a]
v=p['V'];f=p['F'];edges=np.sort(f[:,[[0,1],[1,2],[2,0]]].reshape(-1,2),axis=1)
u,c=np.unique(edges,axis=0,return_counts=True);boundary=u[c==1]
print('DOOR_BOUNDARY',len(boundary),flush=True)
rows=[]
for b in range(3):
 y=(950,1360,1750)[b]
 e=boundary[np.all(abs(v[boundary][:,:,1]-y)<100,axis=1)]
 if not len(e):continue
 pts=v[np.unique(e)];print('POCKET',b,len(e),pts.min(0),pts.max(0),flush=True)
 tree=cKDTree(pts);near=[]
 for owner,r in P.items():
  if owner==a:continue
  q=r['V'][r['F']];dist=tree.query(q.reshape(-1,3))[0].reshape(-1,3)
  ids=np.flatnonzero((dist<.001).sum(1)>=2)
  if len(ids):near.append({'owner':owner,'triangles':ids.tolist(),'bounds':[q[ids].min((0,1)).tolist(),q[ids].max((0,1)).tolist()]})
 rows.append({'pocket':b,'edges':v[e].tolist(),'near_faces':near})
 print('NEAR',[(r['owner'],len(r['triangles'])) for r in near],flush=True)
(H/'door_boundary_diagnostic.json').write_text(json.dumps({'parts_sha256':hashlib.sha256((H/'k_parca.pkl').read_bytes()).hexdigest(),'rows':rows},indent=2),encoding='utf-8')
