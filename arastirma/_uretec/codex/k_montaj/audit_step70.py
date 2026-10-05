import sys
sys.dont_write_bytecode=True
from pathlib import Path
import sys,json,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[4];Y=ROOT/'arastirma/_uretec/h3/yama_v9'
for p in (Y/'kaynak',Y/'kaynak/gece'):sys.path.insert(0,str(p))
from m8kit import Glb
from fastener_audit import audit
OUT=ROOT/'_local/codex_k_montaj';a=Glb(str(OUT/'hat3_v10c.glb'));b=Glb(str(OUT/'k70a.glb'))
def signature(g):
 excluded={}; records=[]; components={}
 for name in sorted({p['name'] for p in g.prims if p['name'].startswith('K_GOVDE') and not p.get('gizli')}):
  try:g.bilesen(name,no=0)
  except (ValueError,IndexError):continue
  for q in g._bc[name]:
   ident=name+'['+str(q['no'])+']';components[ident]=q;records.append({'id':ident,'node':name,'lo':q['lo'].tolist(),'hi':q['hi'].tolist()})
 for item in audit(records)['results']:
  for prim,tri in components[item['stud']]['parca']:excluded.setdefault(id(prim),set()).update(tri.tolist())
 out={}
 for p in g.prims:
  if p.get('gizli'):continue
  name=p['name']
  tri=np.array([i for i in range(len(p['T'])) if i not in excluded.get(id(p),set())]);P=p['X'][p['T'][tri]];P=P[np.linalg.norm(np.cross(P[:,1]-P[:,0],P[:,2]-P[:,0]),axis=1)>1e-6]
  Q=np.round(P,2);Q=Q[np.linalg.norm(np.cross(Q[:,1]-Q[:,0],Q[:,2]-Q[:,0]),axis=1)>1e-6]
  rows=np.sort(Q.view([('x','<f8'),('y','<f8'),('z','<f8')]).reshape(-1,3),axis=1).view('<f8').reshape(-1,9)
  keys=sorted(set(row.tobytes() for row in rows));out.setdefault(name,[]).extend(keys)
 return {name:hashlib.sha256(b''.join(sorted(keys))).hexdigest() for name,keys in out.items()}
s1,s2=signature(a),signature(b);changed=[name for name in set(s1)|set(s2) if s1.get(name)!=s2.get(name)]
records=[]
for name in sorted({p['name'] for p in b.prims if p['name'].startswith('K_GOVDE') and not p.get('gizli')}):
 try:b.bilesen(name,no=0)
 except (ValueError,IndexError):continue
 for q in b._bc[name]:records.append({'id':name+'['+str(q['no'])+']','node':name,'lo':q['lo'].tolist(),'hi':q['hi'].tolist()})
f=audit(records); same=hashlib.sha256((OUT/'k70a.glb').read_bytes()).hexdigest()==hashlib.sha256((OUT/'k70b.glb').read_bytes()).hexdigest()
r={'step':70,'two_runs_byte_identical':same,'untouched_station_surface_check_tolerance_mm':.01,'changed_nodes_outside_32_target_studs':changed,'fastener_audit':f,'passed':same and not changed and f['passed'],'assembly_publication_allowed':False}
(OUT/'step70_audit.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({'passed':r['passed'],'changed_nodes_outside_32_target_studs':changed,'fasteners_passed':f['passed'],'two_runs_byte_identical':same}),flush=True)
