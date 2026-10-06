"""Recover existing hollow-post end triangles by native box-tube boundary.

Source kesme_cad_v8 defines 20x20x2 rectangular hollow stock. Current mesh
provides authoritative length/end planes; no obsolete903mm endpoint used.
"""
from pathlib import Path
import json,pickle,hashlib
import numpy as np,manifold3d as M
H=Path(__file__).resolve().parent;src=H/'k_parca.pkl';P=pickle.load(src.open('rb'))['P'];changes=[];after={a:list(p['V'][p['F']]) for a,p in P.items()}
source=H.parents[2]/'arastirma/_uretec/kesme_cad_v8.py';code=source.read_text(encoding='utf-8-sig')
assert 'kut(x - 8, x + 8, 902.0, 959.0, z - 8, z + 8)' in code
for name in ('k_itici_sac_0','k_itici_sac_1','k_itici_sac_2','k_itici_sac_3'):
 v=P[name]['V'];lo=v.min(0);hi=v.max(0);assert np.max(abs((hi-lo)[[0,2]]-20))<.001
 assert abs(lo[1]-900)<.001 and abs(hi[1]-958)<.001
 for owner,p in P.items():
  if owner==name:continue
  q=p['V'][p['F']];mask=np.all(q.min(1)>=lo-.001,1)&np.all(q.max(1)<=hi+.001,1)
  for i in np.flatnonzero(mask):
   t=q[i];normal=np.cross(t[1]-t[0],t[2]-t[0]);normal/=max(np.linalg.norm(normal),1e-20)
   level=hi[1] if normal[1]>0 else lo[1]
   if abs(normal[1])<.999999 or np.max(abs(t[:,1]-level))>.001:continue
   # Every triangle point belongs to the rectangular annulus, not the void.
   center=(lo+hi)/2;points=np.vstack([t,t.mean(0)]);d=abs(points[:,[0,2]]-center[[0,2]])
   assert np.all(np.max(d,axis=1)>=8-.001) and np.all(d<=10+.001)
   changes.append({'from':owner,'current_triangle':int(i),'to':name,'triangle_sha256':hashlib.sha256(np.asarray(t,dtype='<f8').tobytes()).hexdigest(),'current_post_bounds_mm':[lo.tolist(),hi.tolist()],'source_stock':'20x20x2 hollow rectangular tube','outward_y_normal':float(normal[1])})
moves={(r['from'],r['current_triangle']):r['to'] for r in changes};out={a:[] for a in P};affected=set()
for a,p in P.items():
 for i,t in enumerate(p['V'][p['F']]):
  b=moves.get((a,i),a);out[b].append(t)
  if b!=a:affected.update((a,b))
def close(q):
 v,f=np.unique(np.asarray(q).reshape(-1,3),axis=0,return_inverse=True);mesh=M.Mesh64(np.ascontiguousarray(v),np.ascontiguousarray(f.reshape(-1,3),dtype=np.uint32),tolerance=.001);mesh.merge();s=M.Manifold(mesh)
 return {'status':str(s.status()),'volume_mm3':s.volume() if str(s.status())=='Error.NoError' else None}
checks=[{'part':a,'before':close(P[a]['V'][P[a]['F']]),'after':close(out[a])} for a in sorted(affected)]
for r in checks:
 if r['part'].startswith('k_itici_sac_'):assert r['after']['status']=='Error.NoError' and abs(r['after']['volume_mm3']-8352)<1
# The four upper plates are named in two fragments each. Their physical stock
# must be checked as one, not require each arbitrary fragment to be manifold.
physical=[]
for x in (40,360):
 for z in (-755,-645):
  a=f'itici_taban_{x}_{z}';b=f'k72_itici_ust_plaka_{4000.+x}_{float(z)}';result=close(out[a]+out[b]);physical.append({'physical_sheet':b,'fragments':[a,b],'after':result});assert result['status']=='Error.NoError'
report={'source_parts_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'source_stock_generator_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'proposed_changes':changes,'checks':checks,'physical_sheet_checks':physical,'geometry_changed':False,'ownership_applied':False,'production_release':False}
(H/'post_end_face_proposals.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('POST_END_FACES',len(changes),'FOUR_POSTS_AND_UPPER_SHEETS_CLOSED',flush=True)
