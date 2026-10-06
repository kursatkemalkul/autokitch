from pathlib import Path
import json,hashlib,gzip,numpy as np
import sys
D=Path(__file__).resolve().parent;sys.path.insert(0,str(D))
import panel_mount_candidate as PM
C=PM.OUT/'oil_shelf_mount_candidate'
r=json.loads((C/'audit.json').read_text());recipe=json.loads(gzip.decompress((C/'geometry.json.gz').read_bytes()))
checks=[]
for a,w in recipe['wall_repairs'].items():
 old=np.asarray(w['original_triangles']);v=np.asarray(w['V']);f=np.asarray(w['F'])
 delta=w['added_material_mm3'];closed=PM.solid(v,f,np.array([4200.,1625.,-517.]))
 checks.append({'part':a,'closed_status':str(closed.status()),'added_material_mm3':delta,
 'removed_material_mm3':w['removed_material_mm3'],'before_lo_mm':old.reshape(-1,3).min(0).tolist(),
 'before_hi_mm':old.reshape(-1,3).max(0).tolist(),'after_lo_mm':v.min(0).tolist(),'after_hi_mm':v.max(0).tolist(),
 'native_wall_hole_centers':[j['center_mm'] for j in r['joins'] if j['wall']==a],
 'passed_removal_only_context':delta<1e-6 and np.allclose(old.reshape(-1,3).min(0),v.min(0),atol=.001) and np.allclose(old.reshape(-1,3).max(0),v.max(0),atol=.001)})
a={'source_parts_sha256':r['source_parts_sha256'],'candidate_recipe_sha256':hashlib.sha256((C/'geometry.json.gz').read_bytes()).hexdigest(),
 'checks':checks,'passed_removal_only_context':all(j['passed_removal_only_context'] for j in checks),
 'proof':'Each wall was constructed as original source solid minus the three declared native Ø5 hole cylinders; no wall material added, so unchanged-source intersections cannot increase. Bracket/fastener new solids were audited separately.',
 'precision_mm':.001,'canonical_source_changed':False,'production_release':False}
assert a['passed_removal_only_context']
(C/'wall_context_audit.json').write_text(json.dumps(a,indent=2),encoding='utf-8')
print('OIL_WALL_CONTEXT',a['passed_removal_only_context'],flush=True)

import os
sys.stdout.flush();os._exit(0)
