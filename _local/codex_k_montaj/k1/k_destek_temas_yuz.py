"""Diagnose exact planar contact ownership in native step71 supports.
Normals disambiguate two opposite-oriented solids touching at the same plane.
No generated/duplicated triangles, no geometry edit, no automatic application.
"""
from pathlib import Path
import pickle,json,hashlib
import numpy as np,manifold3d as M
H=Path(__file__).resolve().parent;src=H/'k_parca.pkl';D=pickle.load(src.open('rb'));P=D['P']
def closed(q):
 v,f=np.unique(q.reshape(-1,3),axis=0,return_inverse=True)
 mesh=M.Mesh64(np.ascontiguousarray(v),np.ascontiguousarray(f.reshape(-1,3),dtype=np.uint32),tolerance=.001);mesh.merge();s=M.Manifold(mesh)
 return {'status':str(s.status()),'volume_mm3':s.volume() if str(s.status())=='Error.NoError' else None}
changes=[];rows=[]
for x in (4060,4340):
 for z in (700,379,58):
  tag=f'{x}_{z}';names=[f'k71_alt_flans_{tag}',f'k71_dik_destek_{tag}',f'k71_disli_ust_kapak_{tag}']
  names += [a for a in P if a.startswith(f'k71_alt_pul_{tag}_') or a.startswith(f'k71_alt_somun_{tag}_') or a.startswith(f'k71_ust_havsa_{tag}_')]
  Q={a:P[a]['V'][P[a]['F']] for a in names};out={a:[] for a in names};bb={a:(q.min((0,1)),q.max((0,1))) for a,q in Q.items()}
  # Source K floor ends at Y791. The foot's lower stock face points -Y;
  # co-planar +Y faces are the floor, stolen by the smaller foot bbox.
  floor='taban_sac_3';shelf='k71_istasyon_rafi';out[floor]=[];out[shelf]=[]
  # Only source-defined stock end planes. Hardware's own end planes remain
  # in its label; foot/profile/cap end planes have opposite contact normals.
  stock=names[:3]
  for owner,q in Q.items():
   for i,t in enumerate(q):
    normal=np.cross(t[1]-t[0],t[2]-t[0]);length=np.linalg.norm(normal);normal=normal/max(length,1e-20);targets=[]
    if abs(normal[1])>.999999:
     for a in stock:
      lo,hi=bb[a];level=hi[1] if normal[1]>0 else lo[1]
      if np.max(abs(t[:,1]-level))>.001:continue
      if np.any(t.min(0)[[0,2]]<lo[[0,2]]-.001) or np.any(t.max(0)[[0,2]]>hi[[0,2]]+.001):continue
      targets.append(a)
    target=owner
    if len(targets)==1:target=targets[0]
    if owner==names[0] and normal[1]>.999999 and np.max(abs(t[:,1]-791.))<.001:
     target=floor
    if owner==names[2] and normal[1]<-.999999 and np.max(abs(t[:,1]-889.))<.001:
     target=shelf
    if owner.startswith('k71_alt_pul_') and normal[1]<-.999999 and np.max(abs(t[:,1]-796.))<.001:
     target=owner.replace('k71_alt_pul_','k71_alt_somun_')
    if target!=owner:
     changes.append({'from':owner,'current_triangle':i,'to':target,'triangle_sha256':hashlib.sha256(np.asarray(t,dtype='<f8').tobytes()).hexdigest(),'native_plane_y_mm':float(t[0,1]),'outward_y_normal':float(normal[1])})
    out[target].append(t)
  for a in names:
   rows.append({'part':a,'before':closed(Q[a]),'after':closed(np.asarray(out[a])),'before_triangles':len(Q[a]),'after_triangles':len(out[a])})
report={'source_parts_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'proposed_changes':changes,'checks':rows,'geometry_changed':False,'ownership_applied':False,'production_release':False}
(H/'support_contact_face_proposals.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('SUPPORT_CONTACT_PROPOSALS',len(changes),flush=True)
for r in rows:print(r['part'],r['before']['status'],'->',r['after']['status'],r['before_triangles'],r['after_triangles'],flush=True)
