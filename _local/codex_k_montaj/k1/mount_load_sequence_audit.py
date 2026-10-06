from pathlib import Path
import json,pickle,hashlib
H=Path(__file__).resolve().parent
D=pickle.loads((H/'plan_k_mount_full.pkl').read_bytes())
P=D['P']
def end(a):
 ts=[D['GOR'][a]]+[h[1] for h in D['HAR'][a]]
 if D['MF'].get(a,{}).get('buyu'):ts.append(D['MF'][a]['buyu'][1])
 return max(ts)
def begin(a):
 return min([D['GOR'][a]]+[h[0] for h in D['HAR'][a]])
checks=[]
sets=[('mount_plate_fixed',[f'k75_kiris_somun_{i}' for i in range(2)],
 ['DGRF-C-63-125_govde','elk_k_celik_3','elk_k_celik_4','elk_k_celik_5','elk_k_tarti_celik_0']),
 ('actuator_fixed',[f'DGRF_M10_civata_{i}' for i in range(4)],
 ['DGRF_port_on_QSL','DGRF_port_arka_QSL','DGRF_SMT-8M_0','DGRF_SMT-8M_1','kopru_kirisi_-126','elk_k_celik_2'])]
for label,fixings,loads in sets:
 fixed=max(end(a) for a in fixings)
 for a in loads:
  checks.append({'group':label,'load':a,'fasteners':fixings,'fixed_s':fixed,'load_begins_s':begin(a),
   'load_seated_s':end(a),'passed':begin(a)>=fixed-.001})
# Ear weld carriers are already seated; exact source weld contact evidence checked.
w=json.loads((H/'mount_weld_schedule_audit.json').read_text())
for ear,post in [('govde_kulak_sol_arka_841','kose_dikmesi_20_-800'),('govde_kulak_sol_on_841','kose_dikmesi_20_42')]:
 r=[x for x in w['checks'] if ear in x['carriers'] and post in x['carriers']]
 checks.append({'group':'ear_on_seated_post','ear':ear,'post':post,'source_welds':[x['weld'] for x in r],
  'post_seated_s':end(post),'ear_begins_s':begin(ear),'passed':bool(r) and begin(ear)>=end(post)-.001})
report={'source_model_sha256':D['source_model_sha256'],
 'source_plan_sha256':hashlib.sha256((H/'plan_k_mount_full.pkl').read_bytes()).hexdigest(),
 'checks':checks,'passed':all(r['passed'] for r in checks),'production_release':False,
 'note':'Selected mounting/load sequence proof only; no fixture, strength, torch or whole-station release.'}
(H/'mount_load_sequence_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('SELECTED_MOUNT_LOAD_ORDER',report['passed'],len(checks))
assert report['passed']
