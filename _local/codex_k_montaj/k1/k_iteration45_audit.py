"""Bind stage78 checks to their actual caches. This is not a release gate."""
from pathlib import Path
import hashlib,json
from collections import Counter
H=Path(__file__).resolve().parent
def sha(name):return hashlib.sha256((H/name).read_bytes()).hexdigest()
def read(name):return json.loads((H/name).read_text(encoding='utf-8'))
manifest=read('current_source_manifest.json')
replay=read('ownership_replay_audit.json');closure=read('physical_sheet_closure_audit.json')
binding=read('plan_source_binding_audit.json');plan=read('plan_audit.json')
bench=read('bench_integration_audit.json');ccd=read('full_ccd_plan_k_full.json')
dense=read('dense_bend_morph_audit.json');body=read('body_connection_measured_audit.json')
connections=read('baglanti_denetim.json')
source=manifest['source_model_sha256']
assert replay['source_model_sha256']==binding['source_model_sha256']==bench['source_model_sha256']==ccd['source_model_sha256']==source
assert replay['current_parts_sha256']==binding['source_parts_sha256']==body['source_parts_sha256']==sha('k_parca.pkl')
assert replay['registry_sha256']==sha('surface_ownership_registry.json')
assert closure['source_encoding_sha256']==sha('current_sheet_bending.json')
assert not closure['open_sheets'] and all(r['closed_nonempty_solid'] for r in closure['checks'])
assert not plan['plan_problems'] and not plan['unplanned']
assert binding['source_plan_sha256']==bench['source_plan_sha256']==sha('plan_k.pkl')
assert bench['combined_plan_sha256']==ccd['source_plan_sha256']==dense['source_plan_sha256']==sha('plan_k_full.pkl')
assert dense['dense_plan_sha256']==sha('plan_k_dense.pkl')
assert ccd['rigid_path_passed'] and not ccd['path_issues']
assert dense['bend_morph_sampling_passed'] and not body['unresolved']
files=('current_source_manifest.json','surface_ownership_registry.json','ownership_replay_audit.json','current_sheet_bending.json','physical_sheet_closure_audit.json','plan_source_binding_audit.json','plan_audit.json','bench_prototype_audit.json','bench_integration_audit.json','current_bend_samples.json','dense_bend_morph_audit.json','full_ccd_plan_k_full.json','body_connection_measured_audit.json','baglanti_denetim.json','topology_repair_recipe.json.gz','topology_recipe_serialization_audit.json')
report={'iteration':45,'source_stage':78,'source_model_sha256':source,'parts':replay['parts'],'triangles':replay['source_triangles'],'physical_sheets':closure['physical_sheet_count'],'closed_sheets':len(closure['checks']),'combined_rigid_ccd_pairs':ccd['tested_pairs'],'combined_rigid_ccd_passed':True,'dense_bend_sampling_passed':True,'measured_body_connections_passed':len(body['checks']),'connection_classes':dict(Counter(r['sinif'] for r in connections.values())),'artifacts_sha256':{f:sha(f) for f in files},'production_release':False,'k_completed':False,'u_started':False,'open_work':['Whole-station fasteners, supplier mounts and temporary-load support','Bend self-collision, press tooling, fixtures and weld access','Custom stock thickness and profile radius conformity','Registered deterministic chain replay on latest shared model','Audited player output and browser review before publication']}
(H/'iteration45_audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print('ITERATION45_BOUND',report['closed_sheets'],report['physical_sheets'],'rigid_pairs',report['combined_rigid_ccd_pairs'],'body_joins',report['measured_body_connections_passed'],'release',False,flush=True)
