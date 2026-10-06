"""Prove old CCD applies unchanged; test every pair involving added seams."""
from pathlib import Path
import pickle,json,hashlib,numpy as np,sys,time,os
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H.parents[2]/'_local/claude_son_yerel/gece2/cekmece'))
import yol_denetim_v2 as Y
Y.ADIM=.002
parent=H/'plan_k_head_supported.pkl';child=H/'plan_k_clip_full.pkl'
A=pickle.loads(parent.read_bytes());D=pickle.loads(child.read_bytes())
previous=json.loads((H/'head_support_motion_inheritance.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert previous['supported_plan_sha256']==sha(parent) and previous['rigid_path_passed']
assert D['full_source_triangle_multiset_verified'] and not D['PLAN_SORUN']
def exact(a,b):
 if isinstance(a,np.ndarray):return isinstance(b,np.ndarray) and a.dtype==b.dtype and np.array_equal(a,b)
 if isinstance(a,dict):return isinstance(b,dict) and a.keys()==b.keys() and all(exact(a[k],b[k]) for k in a)
 if isinstance(a,(tuple,list)):return type(a)==type(b) and len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
 return type(a)==type(b) and bool(a==b)
for field in ('P','HAR','GOR','MF','FRAMES','ROT'):
 assert all(exact(v,D[field][a]) for a,v in A[field].items()),field
for field in ('ISTISNA','HARIC_PLAN','HARIC_NEDEN'):assert exact(A[field],D[field]),field
new=sorted(set(D['P'])-set(A['P']));assert len(new)==16
P={a:dict(V=np.asarray(p.get('Vm',p['V']))/1000,F=np.asarray(p.get('Fm',p['F'])),tur=p['tur']) for a,p in D['P'].items()}
inspector=Y.Denetci(P,D['HAR'],D['ROT'],D['GOR'],set(D['ISTISNA']),set(),set(tuple(sorted(p)) for p in D['HARIC_PLAN']))
start=time.time();issues=[];considered=set()
for a in new:
 for b in P:
  if a==b:continue
  pair=tuple(sorted((a,b)))
  if pair in considered:continue
  considered.add(pair)
  x,y=inspector.idx[a],inspector.idx[b]
  if np.any(inspector.L[x]>inspector.H[y]+1e-4) or np.any(inspector.H[x]<inspector.L[y]-1e-4):continue
  issue=inspector.cift(a,b)
  if issue:issues.append(issue);print('CLIP_DELTA_ISSUE',issue,flush=True)
result=dict(source_plan_sha256=sha(child),source_model_sha256=D['source_model_sha256'],parent_plan_sha256=sha(parent),
 parent_unchanged_geometry_and_rigid_paths=True,parent_tested_pairs=previous['tested_pairs'],new_parts=new,
 additional_pairs_considered=len(considered),additional_motion_pairs_tested=inspector.ciftsay,path_issues=issues,
 whole_rigid_path_passed=not issues,step_mm=2,manufacturing_release=False,fixture_checked=False,production_release=False,elapsed_seconds=time.time()-start)
(H/'clip_delta_ccd.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print('CLIP_DELTA_CCD',len(issues),'ISSUES',inspector.ciftsay,'MOTION_PAIRS',len(considered),'PAIRS_CONSIDERED',flush=True)
sys.stdout.flush();os._exit(0 if not issues else 2)
