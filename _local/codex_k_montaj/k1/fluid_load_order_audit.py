"""Check completed wall/shelf/plate fastenings before the next station load."""
from pathlib import Path
import json,pickle,hashlib
H=Path(__file__).resolve().parent;path=H/'plan_k_fluid_full.pkl'
D=pickle.loads(path.read_bytes())
definition=json.loads((H.parent/'oil_load_mount_candidate/audit.json').read_text(encoding='utf-8'))
def seated(a):return max([D['GOR'][a]]+[h[1] for h in D['HAR'][a]])
checks=[]
for j in definition['joins']:
    events=[seated(a) for a in (j['wall'],j['bracket'],j['washer'],j['nut'],'yag_pompa_rafi')]
    checks.append({'joint':j['id'],'parts':[j['wall'],j['bracket'],j['washer'],j['nut'],'yag_pompa_rafi'],
                   'seated_seconds':events,'passed':all(a<=b+.001 for a,b in zip(events,events[1:]))})
for j in definition['load_joins']:
    events=[seated(a) for a in (j['host'],j['carrier'],j['screw'],j['shim'],j['washer'],j['nut'])]
    loads=['yag_pompa_plakasi'] if j['carrier']=='yag_pompa_rafi' else [a for a in D['P'] if a.startswith(('yag_pompasi_','yag_emis_filtresi','yag_T_parcasi','yag_geri_basinc_','yag_basinc_sensoru_','yag_boru_'))]
    times={a:seated(a) for a in loads}
    checks.append({'joint':j['id'],'parts':[j['host'],j['carrier'],j['screw'],j['shim'],j['washer'],j['nut']],
                   'seated_seconds':events,'load_seated_seconds':times,
                   'passed':all(a<=b+.001 for a,b in zip(events,events[1:])) and all(t>=events[-1]-.001 for t in times.values())})
pump=json.loads((H.parent/'oil_pump_clamp_candidate/audit.json').read_text(encoding='utf-8'))
for j in pump['joins']:
 parts=['yag_pompa_plakasi','yag_pompasi_GJ-N21_EagleDrive',j['portal'],j['screw'],j['shim'],j['washer'],j['nut']]
 events=[seated(a) for a in parts]
 checks.append({'joint':j['id'],'parts':parts,'seated_seconds':events,'passed':all(a<=b+.001 for a,b in zip(events,events[1:]))})
fluid=json.loads((H.parent/'oil_fluid_clamp_candidate/audit.json').read_text(encoding='utf-8'))
for j in fluid['joins']:
 parts=['yag_pompa_plakasi',j['supplier_body'],j['portal'],j['screw'],j['shim'],j['washer'],j['nut']]
 events=[seated(a) for a in parts]
 loads=['yag_boru_filtre_pompa','yag_boru_pompa_T','yag_boru_T_regulator','yag_emis_hortumu_TLM1008','yag_donus_hortumu_TLM0806']
 times={a:seated(a) for a in loads}
 checks.append({'joint':j['id'],'parts':parts,'seated_seconds':events,'load_seated_seconds':times,'passed':all(a<=b+.001 for a,b in zip(events,events[1:])) and all(t>=events[-1]-.001 for t in times.values())})
for j in pump['joins']:
 loads=['yag_boru_filtre_pompa','yag_boru_pompa_T','yag_boru_T_regulator']
 checks.append({'joint':j['id']+'_pipes_after_fixed','parts':[j['nut']],'load_seated_seconds':{a:seated(a) for a in loads},'passed':all(seated(a)>=seated(j['nut'])-.001 for a in loads)})
r={'source_model_sha256':D['source_model_sha256'],
   'source_plan_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
   'checks':checks,'passed':len(checks)==26 and all(j['passed'] for j in checks),
   'fixture_and_load_strength_checked':False,'production_release':False}
(H/'fluid_load_order_audit.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
print('OIL_LOAD_ORDER',r['passed'],len(checks),flush=True)
assert r['passed']
