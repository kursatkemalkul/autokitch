"""Prepare explicit sub-micron topology repairs; do not apply to source/cache.

Side panels: subdivide existing triangle edges at existing collinear vertices.
Roof: weld near-coincident source vertices and remove degenerate triangles.
Every resulting physical sheet must be closed. This is a proposal for a
deterministic source step, not a manufacturing release or changed model.
"""
from pathlib import Path
import json,pickle,hashlib
import numpy as np,manifold3d as M
from scipy.spatial import cKDTree
H=Path(__file__).resolve().parent;path=H/'current_sheet_bending.json';D=json.loads(path.read_text(encoding='utf-8'))
repair={};rows=[]
def closed(v,f):
 mesh=M.Mesh64(np.ascontiguousarray(v),np.ascontiguousarray(f,dtype=np.uint32),tolerance=.001);mesh.merge();s=M.Manifold(mesh)
 return str(s.status()),s.volume() if str(s.status())=='Error.NoError' else None
for r in D['sheets']:
 name=r['name']
 if name not in ('sol_sac_urun_girisi','sag_sac_E_penceresi','ust_sac'):continue
 v=np.asarray(r['vertices']);f=np.asarray(r['triangles']);maximum=0.;split=0;removed=0
 if name=='ust_sac':
  parent=np.arange(len(v));tree=cKDTree(v)
  def root(i):
   while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
   return i
  for a,b in sorted(tree.query_pairs(.001)):parent[root(b)]=root(a)
  roots=np.array([root(i) for i in range(len(v))]);keys,remap=np.unique(roots,return_inverse=True)
  vv=np.array([v[roots==k].mean(0) for k in keys]);maximum=float(np.linalg.norm(v-vv[remap],axis=1).max())
  ff=remap[f];keep=(ff[:,0]!=ff[:,1])&(ff[:,1]!=ff[:,2])&(ff[:,2]!=ff[:,0]);removed=int((~keep).sum());ff=ff[keep]
  assert maximum<=.001
 else:
  edges=np.sort(f[:,[[0,1],[1,2],[2,0]]].reshape(-1,2),axis=1);u,c=np.unique(edges,axis=0,return_counts=True);tree=cKDTree(v);insert={}
  for a,b in u[c==1]:
   p,q=v[a],v[b];d=q-p;L=np.linalg.norm(d)
   if L<.002:continue
   candidates=np.asarray(tree.query_ball_point((p+q)/2,L/2+.001),dtype=int);candidates=candidates[(candidates!=a)&(candidates!=b)]
   if not len(candidates):continue
   t=(v[candidates]-p)@d/(L*L);dist=np.linalg.norm(v[candidates]-(p+t[:,None]*d),axis=1);mask=(t>1e-6)&(t<1-1e-6)&(dist<=.001)
   if mask.any():insert[(int(a),int(b))]=candidates[np.flatnonzero(mask)[np.argsort(t[mask])]].tolist();maximum=max(maximum,float(dist[mask].max()))
  verts=v.tolist();tri=[]
  for face in f:
   poly=[];changed=False
   for a,b in zip(face,np.roll(face,-1)):
    poly.append(int(a));pts=insert.get(tuple(sorted((int(a),int(b)))),[])
    if pts:changed=True;poly.extend(pts if a<b else list(reversed(pts)))
   if not changed:tri.append(face.tolist());continue
   center=len(verts);verts.append(v[face].mean(0).tolist());split+=1
   for a,b in zip(poly,poly[1:]+poly[:1]):tri.append([center,a,b])
  vv=np.asarray(verts);ff=np.asarray(tri,dtype=np.uint32)
 status,volume=closed(vv,ff);assert status=='Error.NoError',(name,status)
 row={'sheet':name,'source_triangles':len(f),'proposed_triangles':len(ff),'subdivided_faces':split,'removed_degenerate_faces':removed,'maximum_declared_precision_adjustment_mm':maximum,'bounding_box_change_mm':float(max(abs(v.min(0)-vv.min(0)).max(),abs(v.max(0)-vv.max(0)).max())),'closed_status':status,'volume_mm3':volume,'source_modified':False}
 rows.append(row);repair[name]={'original_triangles':v[f],'vertices':vv,'triangles':ff,'proof':row};print('TOPOLOGY_PROPOSAL',name,status,maximum,flush=True)
assert len(rows)==3
pickle.dump({'source_encoding_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'repairs':repair},(H/'topology_repair_proposal.pkl').open('wb'))
(H/'topology_repair_proposal.json').write_text(json.dumps({'source_encoding_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'checks':rows,'all_proposed_repairs_closed':True,'source_modified':False,'requires_deterministic_source_step':True,'production_release':False},indent=2),encoding='utf-8')
