"""Diagnose boundary T-junctions in existing sheet surfaces, never apply.

Subdivides triangle edges only at existing near-collinear vertices and records
the deviation. This is a diagnostic topology mesh, not a source/model update.
"""
from pathlib import Path
import json,hashlib
import numpy as np,manifold3d as M
from scipy.spatial import cKDTree
H=Path(__file__).resolve().parent;path=H/'current_sheet_bending.json';D=json.loads(path.read_text(encoding='utf-8'))
closure=json.loads((H/'physical_sheet_closure_audit.json').read_text(encoding='utf-8'));wanted=set(closure['open_sheets']);rows=[]
for r in D['sheets']:
 if r['name'] not in wanted:continue
 v=np.asarray(r['vertices']);f=np.asarray(r['triangles']);edges=np.sort(f[:,[[0,1],[1,2],[2,0]]].reshape(-1,2),axis=1);u,c=np.unique(edges,axis=0,return_counts=True);boundary=u[c==1];tree=cKDTree(v);insert={};worst=0.
 for a,b in boundary:
  p,q=v[a],v[b];d=q-p;L=float(np.linalg.norm(d))
  if L<.002:continue
  candidate=np.asarray(tree.query_ball_point((p+q)/2,L/2+.001),dtype=int);candidate=candidate[(candidate!=a)&(candidate!=b)]
  if not len(candidate):continue
  t=(v[candidate]-p)@d/(L*L);dist=np.linalg.norm(v[candidate]-(p+t[:,None]*d),axis=1);mask=(t>1e-6)&(t<1-1e-6)&(dist<=.001)
  if mask.any():
   insert[(int(a),int(b))]=[int(candidate[j]) for j in np.flatnonzero(mask)[np.argsort(t[mask])]];worst=max(worst,float(dist[mask].max()))
 verts=v.tolist();tri=[];split_count=0
 for face in f:
  poly=[];split=False
  for a,b in zip(face,np.roll(face,-1)):
   poly.append(int(a));key=tuple(sorted((int(a),int(b))));points=insert.get(key,[])
   if points:split=True;poly.extend(points if a<b else list(reversed(points)))
  if not split:tri.append(face.tolist());continue
  center=len(verts);verts.append(v[face].mean(0).tolist());split_count+=1
  for a,b in zip(poly,poly[1:]+poly[:1]):tri.append([center,a,b])
 vv=np.ascontiguousarray(verts);ff=np.ascontiguousarray(tri,dtype=np.uint32);mesh=M.Mesh64(vv,ff,tolerance=.001);mesh.merge();solid=M.Manifold(mesh)
 row={'sheet':r['name'],'original_boundary_edges':len(boundary),'subdivided_source_faces':split_count,'existing_vertex_edge_deviation_mm':worst,'diagnostic_triangles':len(tri),'status_after_t_joint_subdivision':str(solid.status()),'volume_mm3':solid.volume() if str(solid.status())=='Error.NoError' else None,'source_geometry_modified':False,'production_release':False};rows.append(row)
 print('T_JOINT_DIAGNOSTIC',r['name'],split_count,worst,str(solid.status()),flush=True)
(H/'t_joint_diagnostic.json').write_text(json.dumps({'source_encoding_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'checks':rows,'source_updated':False,'production_release':False},indent=2),encoding='utf-8')
