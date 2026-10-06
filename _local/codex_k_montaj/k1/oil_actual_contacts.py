"""Measure selected native-source oil mounting contacts; not production approval."""
from pathlib import Path
import pickle,json,hashlib
import numpy as np
import trimesh
H=Path(__file__).resolve().parent
path=H/'k_parca_oil_verified.pkl'
P=pickle.loads(path.read_bytes())['P']
folder=H.parent/'oil_shelf_mount_candidate'
scope=json.loads((folder/'source_scope_audit.json').read_text(encoding='utf-8'))
assert scope['full_triangle_rebind_passed']
assert scope['verified_parts_sha256']==hashlib.sha256(path.read_bytes()).hexdigest()
definition=json.loads((folder/'audit.json').read_text(encoding='utf-8'))
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
    for a,b in ((j['washer'],j['bracket']),(j['washer'],j['nut']),
                (j['nut'],j['stud']),(j['stud'],j['wall'])):
        r=contact(a,b);r['joint']=j['id'];rows.append(r)
for side in ('sol','sag'):
    for a in ('yag_pompa_rafi_kosebendi_'+side,'k79_yag_raf_yatay_kosebent_'+side):
        rows.append(contact('k79_yag_raf_kose_kaynagi_'+side,a))
r={'source_model_sha256':scope['output_sha256'],
   'source_parts_sha256':scope['verified_parts_sha256'],
   'checks':rows,'passed_selected_geometry_contacts':all(x['contact_within_0_6_mm'] for x in rows),
   'method':'bidirectional vertices against actual source triangle surfaces; 0.6mm contact classification only',
   'tool_access_checked':False,'load_capacity_checked':False,'production_release':False,
   'remaining':'Shelf-to-brackets and pump plate-to-shelf fastening, assembly paths and manufacturing processes.'}
(H/'oil_actual_contacts.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
print('OIL_ACTUAL_CONTACTS',r['passed_selected_geometry_contacts'],len(rows),flush=True)
for row in rows:
    if not row['contact_within_0_6_mm']:print('OPEN',row,flush=True)
assert r['passed_selected_geometry_contacts']
