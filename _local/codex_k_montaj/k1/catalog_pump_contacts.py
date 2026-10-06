"""Measure selected native-source oil mounting contacts; not production approval."""
from pathlib import Path
import pickle,json,hashlib
import numpy as np
import trimesh
H=Path(__file__).resolve().parent
path=H/'k_parca_catalog_verified.pkl'
P=pickle.loads(path.read_bytes())['P']
folder=H.parent/'oil_fluid_clamp_candidate'
scope=json.loads((H.parent/'actuator_catalog_fastener_candidate/source_scope_audit.json').read_text(encoding='utf-8'))
assert scope['full_triangle_rebind_passed']
assert scope['verified_parts_sha256']==hashlib.sha256(path.read_bytes()).hexdigest()
definition=json.loads((H.parent/'oil_pump_clamp_candidate/audit.json').read_text(encoding='utf-8'))
cache={}
def contact(a,b):
    distances=[]
    for p,q in ((a,b),(b,a)):
        v=np.asarray(P[p]['V']);w=np.asarray(P[q]['V'])
        mask=np.all(v>=w.min(0)-.6,axis=1)&np.all(v<=w.max(0)+.6,axis=1)
        if not mask.any():continue
        if q not in cache:cache[q]=trimesh.Trimesh(w,P[q]['F'],process=False)
        _,d,_=trimesh.proximity.closest_point(cache[q],v[mask])
        distances.append(float(d.min()))
    distance=min(distances) if distances else None
    return {'a':a,'b':b,'minimum_sampled_surface_distance_mm':distance,
            'contact_within_0_6_mm':distance is not None and distance<=.6}
rows=[]
for j in definition['joins']:
 for a,b in ((j['screw'],j['foot']),(j['foot'],'yag_pompa_plakasi'),(j['shim'],'yag_pompa_rafi'),(j['washer'],j['shim']),(j['nut'],j['washer']),(j['screw'],j['nut'])):
  r=contact(a,b);r['joint']=j['id'];rows.append(r)
 for seam in j['seams']:
  for a in (j['portal'],j['foot']):rows.append(contact(seam,a))
for i in (0,1):
 for a,b in ((f'k79_pompa_ust_pad_{i}','yag_pompasi_GJ-N21_EagleDrive'),(f'k79_pompa_ust_pad_{i}',f'k79_pompa_pad_yapistirici_{i}'),(f'k79_pompa_pad_yapistirici_{i}',f'k79_pompa_portal_{i}')):rows.append(contact(a,b))
rows.append(contact('yag_pompasi_GJ-N21_EagleDrive','yag_pompa_plakasi'))
r={'source_model_sha256':scope['output_sha256'],'source_parts_sha256':scope['verified_parts_sha256'],'checks':rows,'passed_selected_geometry_contacts':all(x['contact_within_0_6_mm'] for x in rows),'tool_access_checked':False,'load_capacity_checked':False,'production_release':False}
(H/'catalog_pump_contacts.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
print('PUMP_CONTACTS',r['passed_selected_geometry_contacts'],len(rows),flush=True)
for row in rows:
 if not row['contact_within_0_6_mm']:print('OPEN',row,flush=True)
assert r['passed_selected_geometry_contacts']
