"""Restore inner-door hole walls wrongly assigned to PEM component bounds.

Uses the native inner sheet's six hole centers as references and the current
source cylinder vertices, stock z interval and inward chord normal. Records
its 0.01 mm radius difference from the older CAD reference; never substitutes
that reference geometry. Retains existing source triangles exactly.
"""
from pathlib import Path
import sys,pickle,json,hashlib,os
import numpy as np,manifold3d as M
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
sys.path.insert(0,str(ROOT/'arastirma/_uretec/codex/k_montaj'))
from lower_support import K,OUT,cq
from current_cad import factory_from_source
g=factory_from_source(K,OUT)
native=next(s.kati().translate((4000,0,0)) for s in g.SAC if s.ad=='onyuz_kapak_K_ic_tava')
holes=[]
for face in native.Faces():
 if face.geomType()!='CYLINDER':continue
 b=face.BoundingBox()
 if abs(b.zmin-59)>.001 or abs(b.zmax-60)>.001:continue
 if b.xmin<4030 or b.xmax>4055:continue
 holes.append((face,(b.xmin+b.xmax)/2,(b.ymin+b.ymax)/2,(b.xmax-b.xmin)/2))
assert len(holes)==6,len(holes)
print('NATIVE_HOLES',[(x,y,r) for _,x,y,r in holes],flush=True)
path=H/'k_parca.pkl';P=pickle.load(path.open('rb'))['P'];target='k_govde_on_seffaf_1';changes=[]
for owner,p in P.items():
 if not (owner.startswith('onyuz_kapak_K_mentese_') and '_pem_' in owner):continue
 for i,t in enumerate(p['V'][p['F']]):
  if t[:,2].min()<59-.001 or t[:,2].max()>60+.001:continue
  normal=np.cross(t[1]-t[0],t[2]-t[0]);normal/=np.linalg.norm(normal)
  for face,x,y,r in holes:
   radial=np.linalg.norm(t[:,:2]-[x,y],axis=1)
   if max(abs(radial-r))>.012 or np.ptp(radial)>.001:continue
   edge_xy=np.unique(t[:,:2],axis=0);assert len(edge_xy)==2
   midpoint=edge_xy.mean(0);inward=np.array([x-midpoint[0],y-midpoint[1],0]);inward/=np.linalg.norm(inward)
   if np.dot(normal,inward)<.999:continue
   distance=max(face.distance(cq.Vertex.makeVertex(*v)) for v in t)
   assert distance<=.012,distance
   changes.append({'from':owner,'current_triangle':i,'to':target,'triangle_sha256':hashlib.sha256(np.asarray(t,dtype='<f8').tobytes()).hexdigest(),'native_cylinder_center_mm':[x,y],'native_radius_mm':r,'stock_z_mm':[59,60],'current_source_radius_mm':float(np.mean(radial)),'native_radius_difference_mm':float(max(abs(radial-r))),'native_radius_is_reference_not_replacement':True,'maximum_native_vertex_distance_mm':distance,'inward_normal_dot':float(np.dot(normal,inward))})
   break
def closure(q):
 v,f=np.unique(np.asarray(q).reshape(-1,3),axis=0,return_inverse=True)
 mesh=M.Mesh64(np.ascontiguousarray(v),np.ascontiguousarray(f.reshape(-1,3),dtype=np.uint32),tolerance=.001);mesh.merge();solid=M.Manifold(mesh)
 return {'status':str(solid.status()),'volume_mm3':solid.volume() if str(solid.status())=='Error.NoError' else None}
out={a:[] for a in P};moves={(r['from'],r['current_triangle']):r['to'] for r in changes};affected={target}
for a,p in P.items():
 for i,t in enumerate(p['V'][p['F']]):
  b=moves.get((a,i),a);out[b].append(t)
  if b!=a:affected.add(a)
checks=[{'part':a,'before':closure(P[a]['V'][P[a]['F']]),'after':closure(out[a])} for a in sorted(affected)]
report={'source_parts_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'proposed_changes':changes,'checks':checks,'physical_sheet_checks':[r for r in checks if r['part']==target],'geometry_changed':False,'production_release':False}
(H/'door_hole_face_proposals.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('DOOR_NATIVE_HOLE_MOVES',len(changes),flush=True)
for r in checks:print(r['part'],r['before']['status'],'->',r['after']['status'],flush=True)
sys.stdout.flush();os._exit(0)
