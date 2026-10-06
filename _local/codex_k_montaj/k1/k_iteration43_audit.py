"""Bind this progress checkpoint to current artifacts; never grant a release."""
from pathlib import Path
import json,hashlib
from collections import Counter
H=Path(__file__).resolve().parent
def sha(name):return hashlib.sha256((H/name).read_bytes()).hexdigest()
def read(name):return json.loads((H/name).read_text(encoding='utf-8'))
replay=read('ownership_replay_audit.json');closure=read('physical_sheet_closure_audit.json');plan=read('plan_audit.json');ccd=read('full_ccd_plan_k_full.json');dense=read('dense_bend_morph_audit.json');connections=read('baglanti_denetim.json');body=read('body_connection_measured_audit.json');topology=read('topology_repair_proposal.json')
assert replay['current_parts_sha256']==sha('k_parca.pkl')
assert replay['registry_sha256']==sha('surface_ownership_registry.json')
assert closure['source_encoding_sha256']==sha('current_sheet_bending.json')
assert not plan['plan_problems'] and not plan['unplanned']
assert ccd['source_plan_sha256']==sha('plan_k_full.pkl')
assert dense['source_plan_sha256']==sha('plan_k_full.pkl') and dense['dense_plan_sha256']==sha('plan_k_dense.pkl')
assert topology['source_encoding_sha256']==sha('current_sheet_bending.json')
files=('surface_ownership_registry.json','ownership_replay_audit.json','current_sheet_bending.json','physical_sheet_closure_audit.json','plan_source_binding_audit.json','bench_prototype_audit.json','bench_integration_audit.json','current_bend_samples.json','dense_bend_morph_audit.json','full_ccd_plan_k_full.json','body_connection_measured_audit.json','baglanti_denetim.json','topology_repair_proposal.json')
report={'iteration':43,'source_model_sha256':replay['source_model_sha256'],'source_face_ownership_replay_passed':True,'parts':replay['parts'],'triangles':replay['source_triangles'],'ownership_rows':replay['registry_rows'],'current_closed_sheets':sum(r['closed_nonempty_solid'] for r in closure['checks']),'physical_sheets':closure['physical_sheet_count'],'open_sheets':closure['open_sheets'],'three_topology_repairs_proposed_not_applied':topology['all_proposed_repairs_closed'],'plan_problems':plan['plan_problems'],'combined_rigid_ccd_passed':ccd['rigid_path_passed'],'combined_rigid_path_issues':ccd['path_issues'],'dense_bend_sampling_passed':dense['bend_morph_sampling_passed'],'body_connection_unresolved':body['unresolved'],'connection_classes':dict(Counter(r['sinif'] for r in connections.values())),'artifacts_sha256':{f:sha(f) for f in files},'historical_native4240_note':'The original native-plane proposal was overwritten by a later diagnostic. The current complete canonical registry is independently replay-verified against every raw source triangle; the historical intermediate proposal hash is not claimed present.','production_release':False,'k_completed':False,'u_started':False,'open_work':['Apply deterministic topology source correction, rebuild extraction and names','Resolve whole-station connection worklist and current slot-specific audit','Verify bend self-collision, press tooling, fixtures and weld access','Replay registered chain over latest shared model under coordination lock','Generate audited player output and browser review before final publication']}
(H/'iteration43_audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print('ITERATION43_BOUND',report['current_closed_sheets'],report['physical_sheets'],'rigid_ccd',report['combined_rigid_ccd_passed'],'release',False,flush=True)
