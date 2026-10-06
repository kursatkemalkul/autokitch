"""Resolve only explicitly measured DIN mounting stacks; no blanket supplier exemption."""
from pathlib import Path
import json,pickle,hashlib
H=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
parts=H/'k_parca_fluid_verified.pkl';plan=H/'plan_k_fluid_full.pkl'
measured=json.loads((H/'fluid_panel_join_audit.json').read_text());contacts=json.loads((H/'fluid_din_contacts.json').read_text())
assert measured['passed'] and contacts['passed_selected_geometry_contacts']
assert measured['source_parts_sha256']==contacts['source_parts_sha256']==sha(parts)
benchpath=H/'fluid_bench_plans.pkl';benches=pickle.loads(benchpath.read_bytes())['groups']
definition=json.loads((H.parent/'din_mount_candidate/audit.json').read_text())
current=json.loads((H/'fluid_connection_worklist.json').read_text())
assert current['source_parts_sha256']==sha(parts) and current['source_plan_sha256']==sha(plan)
rows=[]
for rail,loads in [('din_rayi_0',['guc_24V_NDR-240-24','plc_S7-1200_1214C','plc_tarti_modulu_SIWAREX_WP231']),('din_rayi_1',['sigorta_C10','klemens_sirasi'])]:
 b=next(d for d in benches.values() if rail in d['GOR'])
 seated=lambda a:max([b['GOR'][a]]+[x[1] for x in b['HAR'][a]])
 joints=[j for j in definition['rail_joints'] if rail in j['parts']]
 assert len(joints)==2
 fixes={j['id']:max(seated(a) for a in j['parts']) for j in joints}
 load_times={a:seated(a) for a in loads}
 assert all(t>=max(fixes.values()) for t in load_times.values())
 rows.append({'part':rail,'scope':'Two M5 rail-to-panel mounting stacks only; purchased device clips remain open',
 'fastened_on_bench_seconds':fixes,'supported_devices_seated_on_bench_seconds':load_times,
 'explicit_actual_thread_measurements_and_contacts_passed':True,'fix_before_load_passed':True,
 'binding':{'parts_sha256':sha(parts),'plan_sha256':sha(plan),'bench_sha256':sha(benchpath),'measurements_sha256':sha(H/'fluid_panel_join_audit.json'),'contacts_sha256':sha(H/'fluid_din_contacts.json')},
 'complete_manufacturing_release':False})
resolved={r['part'] for r in rows};assert resolved<=set(x['part'] for x in current['unresolved'])
report={'source_parts_sha256':sha(parts),'source_plan_sha256':sha(plan),
 'original_classifier_open_count':current['count'],'mounting_evidence':rows,
 'remaining_unresolved':[x for x in current['unresolved'] if x['part'] not in resolved],
 'remaining_count':current['count']-len(resolved),'production_release':False,
 'reason':'The original classifier cannot traverse screw-nut-washer stacks because it only links one fastener touching two carrier surfaces. This report accepts only the measured named stacks with verified bench ordering.'}
(H/'fluid_din_evidence.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('DIN_SPECIFIC_EVIDENCE',len(resolved),'REMAINING',report['remaining_count'])
