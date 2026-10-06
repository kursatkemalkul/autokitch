"""Source-bound axial tool envelopes, not complete torque/process approval."""
import panel_mount_candidate as PM
from lower_support import *
import pickle,hashlib
H=OUT/'k1';folder=OUT/'oil_fluid_clamp_candidate'
P=pickle.loads((H/'k_parca_fluid_verified.pkl').read_bytes())['P']
recipe=json.loads((folder/'audit.json').read_text())
origin=np.array([4150.,1685.,-520.]);cache={}
checks=[]
for j in recipe['joins']:
 x,y,z=j['center_mm']
 for kind,shape in [('hex_key_shaft',cylinder(x,y+.05,z,2.,60.)),
                    ('socket_body',cylinder(x,1629.5-25.,z,7.,25.).cut(cylinder(x,1629.5-25.,z,4.8,25.)))]:
  v,f=PM.mesh(shape);solid=PM.solid(v,f,origin);lo=v.min(0);hi=v.max(0);issues=[]
  for name,r in P.items():
   if name in (j['screw'],j['nut']):continue # Intended drive/socket mating; checked separately by nominal tool fit.
   w=r['V']
   if np.any(np.minimum(hi,w.max(0))-np.maximum(lo,w.min(0))<=.001):continue
   try:
    if name not in cache:cache[name]=PM.solid(w,r['F'],origin)
    vol=float((solid^cache[name]).volume())
    if vol>.02:issues.append({'part':name,'volume_mm3':vol})
   except AssertionError:
    t=w[r['F']];t=t[np.all(t.max(1)>=lo-.01,axis=1)&np.all(t.min(1)<=hi+.01,axis=1)]
    n=int(PM.YD.poz_kesisim(np.asarray(v[f],float),np.asarray(t,float),.002).sum()) if len(t) else 0
    if n:issues.append({'part':name,'surface_crossing_pairs':n})
  checks.append({'joint':j['id'],'tool':kind,'issues':issues,'passed':not issues})
r={'source_parts_sha256':hashlib.sha256((H/'k_parca_fluid_verified.pkl').read_bytes()).hexdigest(),
   'checks':checks,'passed_axial_envelopes_only':all(c['passed'] for c in checks),
   'envelope_assumptions':'4mm shaft envelope for M5 countersunk drive;14mm OD socket with9.6mm hollow clearance;60mm top approach,25mm bottom approach',
   'tool_catalog_and_torque_checked':False,'handle_swing_checked':False,'production_release':False}
(H/'fluid_tool_axial_access.json').write_text(json.dumps(clean(r),indent=2),encoding='utf-8')
print('PUMP_TOOL_ACCESS',r['passed_axial_envelopes_only'],[c for c in checks if not c['passed']],flush=True)
sys.stdout.flush();os._exit(0 if r['passed_axial_envelopes_only'] else 2)
