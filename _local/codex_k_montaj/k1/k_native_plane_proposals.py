"""Propose source face labels against oriented, bounded native CAD planes.

Only exact native planar boundary matches; curved faces stay untouched.
No generated triangles, no application, no release. Native shapes are metadata
references; obsolete CAD is never substituted for current mesh geometry.
"""
from pathlib import Path
import sys,json,pickle,hashlib,time,os
import numpy as np,manifold3d as M
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
sys.path.insert(0,str(ROOT/'arastirma/_uretec/codex/k_montaj'))
from lower_support import K,S,OUT,build,cq
from current_cad import factory_from_source
from roof_mounts import build_roof
from mechanism_mounts import build_mounts
src=H/'k_parca.pkl';P=pickle.load(src.open('rb'))['P'];native={};T=time.time()
g=factory_from_source(K,OUT)
for s in g.SAC:
 if s.ad in P:native[s.ad]=s.kati().translate((4000,0,0))
 if s.ad=='onyuz_kapak_K_ic_tava':native['k_govde_on_seffaf_1']=s.kati().translate((4000,0,0))
for p in g.PROFIL:
 if p.ad in P:native[p.ad]=p.parca()['sh'].translate((4000,0,0))
lp,_,shelf=build();rp,_,roof=build_roof();mp,_=build_mounts()
for p in lp+rp+mp:
 if p['ad'] in P:native[p['ad']]=p['sh']
native['k71_istasyon_rafi']=shelf.kati();native['ust_sac']=roof.kati().translate((4000,0,0))
native['k_e4_sol_yama_40x40']=K.kutu(4001.5,4003,1789,1829,-790,-750)
planes={};count=0
for a,sh in native.items():
 for face in sh.Faces():
  if face.geomType()!='PLANE':continue
  n=np.array(face.normalAt().toTuple());axis=int(np.argmax(abs(n)))
  if abs(n[axis])<.999999:continue
  point=np.array(face.Center().toTuple());bb=face.BoundingBox();lo=np.array([bb.xmin,bb.ymin,bb.zmin]);hi=np.array([bb.xmax,bb.ymax,bb.zmax]);key=(axis,int(np.sign(n[axis])),int(round(point[axis]*100)))
  planes.setdefault(key,[]).append((a,face,lo,hi,float(point[axis])));count+=1
print('NATIVE_BOUNDARY_PLANES',len(native),count,flush=True)
changes=[];ambiguous=[]
for owner,p in P.items():
 # Context surfaces may coincide with native K faces. They are not K parts.
 if owner.startswith('cevre_'):continue
 Q=p['V'][p['F']];N=np.cross(Q[:,1]-Q[:,0],Q[:,2]-Q[:,0]);length=np.linalg.norm(N,axis=1);N=N/np.maximum(length[:,None],1e-20)
 for i,t in enumerate(Q):
  n=N[i];axis=int(np.argmax(abs(n)))
  if abs(n[axis])<.999999 or np.ptp(t[:,axis])>.001:continue
  level=float(t[0,axis]);sign=int(np.sign(n[axis]));candidates=[]
  for j in (int(round(level*100))-1,int(round(level*100)),int(round(level*100))+1):candidates.extend(planes.get((axis,sign,j),[]))
  if not candidates:continue
  matches=[];distances={}
  for target,face,lo,hi,v in candidates:
   if abs(level-v)>.001 or np.any(t.min(0)<lo-.001) or np.any(t.max(0)>hi+.001):continue
   # Boundary distance, not distance to the containing SOLID (which would
   # misclassify interior faces). Native outward normal must also agree.
   pts=[*t,t.mean(0)];maximum=max(face.distance(cq.Vertex.makeVertex(*x)) for x in pts)
   if maximum<=.001:matches.append(target);distances[target]=maximum
  matches=sorted(set(matches))
  if owner in matches:continue
  if len(matches)==1:
   changes.append({'from':owner,'current_triangle':i,'to':matches[0],'triangle_sha256':hashlib.sha256(np.asarray(t,dtype='<f8').tobytes()).hexdigest(),'maximum_native_face_distance_mm':distances[matches[0]],'plane_axis':'XYZ'[axis],'plane_mm':level,'normal_sign':sign})
  elif len(matches)>1:ambiguous.append({'owner':owner,'triangle':i,'matches':matches})
 print('NATIVE_PLANAR_OWNER',owner,'moves',sum(r['from']==owner for r in changes),'seconds',round(time.time()-T,1),flush=True)
out={a:[] for a in P};moves={(r['from'],r['current_triangle']):r['to'] for r in changes};affected=set()
for a,p in P.items():
 for i,t in enumerate(p['V'][p['F']]):
  b=moves.get((a,i),a);out[b].append(t)
  if b!=a:affected.update((a,b))
checks=[]
def closure(q):
 v,f=np.unique(np.asarray(q).reshape(-1,3),axis=0,return_inverse=True);m=M.Mesh64(np.ascontiguousarray(v),np.ascontiguousarray(f.reshape(-1,3),dtype=np.uint32),tolerance=.001);m.merge();s=M.Manifold(m)
 return {'status':str(s.status()),'volume_mm3':s.volume() if str(s.status())=='Error.NoError' else None}
for a in sorted(affected):checks.append({'part':a,'before':closure(P[a]['V'][P[a]['F']]),'after':closure(out[a])})
report={'source_parts_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'native_parts':len(native),'native_planes':count,'proposed_changes':changes,'ambiguous':ambiguous,'checks':checks,'geometry_changed':False,'ownership_applied':False,'production_release':False,'elapsed_seconds':time.time()-T}
(H/(sys.argv[1] if len(sys.argv)>1 else 'native_plane_face_proposals.json')).write_text(json.dumps(report,indent=2),encoding='utf-8')
print('NATIVE_PLANE_COMPLETE',len(changes),'ambiguous',len(ambiguous),'seconds',round(time.time()-T,1),flush=True)
sys.stdout.flush();os._exit(0)
