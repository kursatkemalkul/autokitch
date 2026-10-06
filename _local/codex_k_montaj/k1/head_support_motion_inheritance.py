"""Inherit rigid-path evidence only after exact motion/geometry equality.
Support text does not verify fixture design, manufacturing or connections.
"""
from pathlib import Path
import hashlib,json,pickle,numpy as np
H=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
parent=H/'plan_k_head_full.pkl';child=H/'plan_k_head_supported.pkl'
a=pickle.loads(parent.read_bytes());b=pickle.loads(child.read_bytes())
ccd=json.loads((H/'full_ccd_plan_k_head_full.json').read_text())
assert ccd['source_plan_sha256']==sha(parent)
assert ccd['source_model_sha256']==a['source_model_sha256']==b['source_model_sha256']
assert ccd['rigid_path_passed'] and not ccd['path_issues']
assert b['support_event_parent_plan_sha256']==sha(parent)
def exact(x,y):
 if isinstance(x,np.ndarray):return isinstance(y,np.ndarray) and x.dtype==y.dtype and np.array_equal(x,y)
 if isinstance(x,dict):return isinstance(y,dict) and x.keys()==y.keys() and all(exact(x[k],y[k]) for k in x)
 if isinstance(x,(list,tuple)):return type(x)==type(y) and len(x)==len(y) and all(exact(p,q) for p,q in zip(x,y))
 return type(x)==type(y) and bool(x==y)
fields=['P','HAR','GOR','MF','FRAMES','ROT','ISTISNA','HARIC_PLAN','HARIC_NEDEN','FABRICATION_JOINS']
assert all(exact(a[k],b[k]) for k in fields)
r=dict(parent_plan_sha256=sha(parent),supported_plan_sha256=sha(child),source_model_sha256=a['source_model_sha256'],
 exact_unchanged_fields=fields,tested_pairs=ccd['tested_pairs'],path_issues=[],rigid_path_passed=True,
 evidence_method='Exact geometry, rigid motion, visibility and collision-exception equality with fully tested parent',
 fixture_checked=False,connection_checked=False,bending_self_collision_checked=False,production_release=False)
(H/'head_support_motion_inheritance.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
print('SUPPORTED_HEAD_RIGID_PATH',r['tested_pairs'],'ISSUES',0,flush=True)
