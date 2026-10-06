"""Bind panel/DIN motion checks; keep whole-station release explicitly open."""
from pathlib import Path
import json, hashlib
H=Path(__file__).resolve().parent;C=H.parent/'din_mount_candidate'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
m=read(H/'current_source_manifest.json');s=read(C/'source_geometry_audit.json')
b=read(H/'plan_source_binding_audit.json');p=read(H/'plan_audit.json')
bi=read(H/'bench_integration_audit.json');bp=read(H/'bench_prototype_audit.json')
ccd=read(H/'full_ccd_plan_k_full.json');dense=read(H/'dense_bend_morph_audit.json')
closure=read(H/'physical_sheet_closure_audit.json')
assert m['source_model_sha256']==s['output_sha256']==b['source_model_sha256']==bi['source_model_sha256']==ccd['source_model_sha256']
assert m['current_parts_sha256']==s['verified_parts_sha256']==b['source_parts_sha256']==sha(H/'k_parca.pkl')
assert not p['plan_problems'] and not p['unplanned'] and p['parts']==873
assert all(not row['plan_problems'] for row in bp['groups']) and len(bp['groups'])==17
assert bi['combined_plan_sha256']==ccd['source_plan_sha256']==dense['source_plan_sha256']==sha(H/'plan_k_full.pkl')
assert bi['source_plan_sha256']==b['source_plan_sha256']==sha(H/'plan_k.pkl')
assert ccd['rigid_path_passed'] and not ccd['path_issues'] and ccd['step_mm']==2
assert dense['dense_plan_sha256']==sha(H/'plan_k_dense.pkl') and dense['bend_morph_sampling_passed']
assert closure['passed_closure_only'] and closure['physical_sheet_count']==68 and not closure['open_sheets']
assert closure['source_encoding_sha256']==sha(H/'current_sheet_bending.json')
joint_files=['body_connection_measured_audit.json','lower_connection_measured_audit.json','mount_connection_measured_audit.json']
joint_counts={}
for n in joint_files:
 j=read(H/n)
 assert j['source_parts_sha256']==sha(H/'k_parca.pkl') and all(r['passed'] for r in j['checks'])
 joint_counts[n]=len(j['checks'])
m.update(full_montage_checks_need_refresh=False,rigid_montage_checks_current=True,rigid_montage_plan_sha256=sha(H/'plan_k_full.pkl'))
(H/'current_source_manifest.json').write_text(json.dumps(m,indent=2),encoding='utf-8')
files=['current_source_manifest.json','plan_audit.json','bench_prototype_audit.json','bench_integration_audit.json','plan_source_binding_audit.json','full_ccd_plan_k_full.json','dense_bend_morph_audit.json','physical_sheet_closure_audit.json','current_sheet_encoding_audit.json','surface_ownership_registry.json']
files+=joint_files
report={'source_model_sha256':m['source_model_sha256'],'parts':873,'triangles':s['triangles'],'closed_physical_sheets':68,'measured_panel_and_DIN_joints':8,'rigid_paths_passed':True,'tested_pairs':ccd['tested_pairs'],'bend_sampling_passed':True,'artifacts_sha256':{n:sha(H/n) for n in files},'whole_station_connections_verified':False,'manufacturing_release':False,'production_release':False,'k_completed':False,'u_started':False,'remaining':['Actual fixtures and temporary-load support','Whole-station supplier clips, mounting and connections','Sheet forming tooling and self-contact','Countersink secondary machining animation','Custom stock and hinges conformity','Shared-chain registration and whole-source replay','Final player generation and browser review']}
report['previous_structural_joints_rechecked_on_current_source']=joint_counts
(H/'din_motion_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('DIN_MOTION_BOUND',873,68,ccd['tested_pairs'],'release',False,flush=True)
