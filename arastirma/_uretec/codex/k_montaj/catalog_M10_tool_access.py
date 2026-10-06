"""Actual current-source rear access for four M10 socket heads.
13mm clearance envelope implements8mm key plus5mm surround;80mm approach.
"""
import panel_mount_candidate as PM
from lower_support import *
import pickle,hashlib
H=OUT/'k1';path=H/'k_parca_catalog_verified.pkl';P=pickle.loads(path.read_bytes())['P']
source=json.loads((OUT/'actuator_catalog_fastener_candidate/source_scope_audit.json').read_text())
assert hashlib.sha256(path.read_bytes()).hexdigest()==source['verified_parts_sha256']
recipe=json.loads((OUT/'actuator_catalog_fastener_candidate/audit.json').read_text())
origin=np.array([4200.,1325.,-266.]);cache={};checks=[]
for j in recipe['joins']:
 x,y,z=j['center_mm'];shape=cylinder(x,y,z-10.-80.,6.5,80.-.05,axis=(0,0,1));v,f=PM.mesh(shape)
 solid=PM.solid(v,f,origin);lo=v.min(0);hi=v.max(0);issues=[]
 for name,r in P.items():
  if name==j['id']:continue # Nominal hex-drive mating itself is intentional.
  w=r['V']
  if np.any(np.minimum(hi,w.max(0))-np.maximum(lo,w.min(0))<=.001):continue
  try:
   if name not in cache:cache[name]=PM.solid(w,r['F'],origin)
   volume=float((solid^cache[name]).volume())
   if volume>.02:issues.append({'part':name,'volume_mm3':volume})
  except AssertionError:
   t=w[r['F']];t=t[np.all(t.max(1)>=lo-.01,axis=1)&np.all(t.min(1)<=hi+.01,axis=1)]
   n=int(PM.YD.poz_kesisim(np.asarray(v[f],float),np.asarray(t,float),.002).sum()) if len(t) else 0
   if n:issues.append({'part':name,'surface_crossing_pairs':n})
 checks.append({'part':j['id'],'key_across_flats_mm':8.,'clearance_envelope_diameter_mm':13.,'rear_approach_mm':80.,'issues':issues,'passed':not issues})
r={'source_model_sha256':source['output_sha256'],'source_parts_sha256':source['verified_parts_sha256'],'checks':checks,'passed_axial_access':all(q['passed'] for q in checks),'handle_swing_and_torque_verified':False,'whole_station_tool_access_verified':False,'production_release':False}
(H/'catalog_M10_tool_access.json').write_text(json.dumps(clean(r),indent=2),encoding='utf-8')
print('M10_TOOL_ACCESS',r['passed_axial_access'],len(checks),[q for q in checks if not q['passed']],flush=True)
sys.stdout.flush();os._exit(0 if r['passed_axial_access'] else 2)
