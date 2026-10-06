"""Bind verified current K prototype gates without claiming production release."""
from pathlib import Path
import json,hashlib,gzip
H=Path(__file__).resolve().parent;C=H.parent/'oil_pump_clamp_candidate'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
scope=read(C/'source_scope_audit.json');bind=read(H/'pump_plan_source_binding_audit.json')
plan=read(H/'pump_plan_audit.json');bench=read(H/'pump_bench_prototype_audit.json')
integration=read(H/'pump_bench_integration_audit.json');ccd=read(H/'full_ccd_plan_k_pump_full.json')
dense=read(H/'pump_dense_bend_morph_audit.json');closure=read(H/'physical_sheet_closure_audit_pump.json')
assert scope['full_triangle_rebind_passed'] and scope['a_b_byte_identical'] and not scope['changed_nodes_outside_scope']
assert scope['expected_product_parts']==plan['parts']==integration['parts']==ccd['parts']==975
assert bind['source_model_sha256']==integration['source_model_sha256']==ccd['source_model_sha256']==scope['output_sha256']
assert bind['source_parts_sha256']==scope['verified_parts_sha256']==sha(H/'k_parca_pump_verified.pkl')
assert not plan['plan_problems'] and not plan['unplanned']
assert len(bench['groups'])==22 and all(not r['plan_problems'] for r in bench['groups'])
assert bind['source_plan_sha256']==integration['source_plan_sha256']==sha(H/'plan_k_pump_candidate.pkl')
assert integration['combined_plan_sha256']==ccd['source_plan_sha256']==dense['source_plan_sha256']==sha(H/'plan_k_pump_full.pkl')
assert ccd['rigid_path_passed'] and not ccd['path_issues'] and ccd['step_mm']==2
assert dense['bend_morph_sampling_passed'] and dense['dense_plan_sha256']==sha(H/'plan_k_pump_dense.pkl')
assert closure['passed_closure_only'] and closure['physical_sheet_count']==105 and not closure['open_sheets']
assert closure['source_encoding_sha256']==sha(H/'current_sheet_bending_pump.json')
files=['pump_body_connection_measured_audit.json','pump_lower_connection_measured_audit.json','pump_mount_connection_measured_audit.json','pump_panel_join_audit.json']
counts={}
for name in files:
 a=read(H/name);assert a['source_parts_sha256']==scope['verified_parts_sha256'] and a['passed'];counts[name]=len(a['checks'])
for name,key in [('pump_actual_contacts.json','passed_selected_geometry_contacts'),('pump_din_contacts.json','passed_selected_geometry_contacts'),('pump_load_order_audit.json','passed'),('pump_tool_axial_access.json','passed_axial_envelopes_only')]:
 a=read(H/name);assert a[key];assert a.get('source_parts_sha256',scope['verified_parts_sha256'])==scope['verified_parts_sha256'];files.append(name)
work=read(H/'pump_din_evidence.json');assert work['source_parts_sha256']==scope['verified_parts_sha256'] and work['source_plan_sha256']==sha(H/'plan_k_pump_full.pkl')
files+=['full_ccd_plan_k_pump_full.json','pump_dense_bend_morph_audit.json','pump_din_evidence.json','pump_bench_integration_audit.json','pump_plan_source_binding_audit.json','physical_sheet_closure_audit_pump.json']
r={'source_model_sha256':scope['output_sha256'],'parts':975,'triangles':scope['matched_triangles'],'closed_sheets':105,'bench_groups':22,'rigid_paths_passed':True,'tested_pairs':ccd['tested_pairs'],'measured_joint_counts':counts,'new_pump_contacts':46,'oil_and_pump_load_order_checks':18,'selected_tool_axial_envelopes':8,'bend_sampling_passed':True,'remaining_connection_records':work['remaining_count'],'artifacts_sha256':{name:sha(H/name) for name in files},'canonical_source_changed':False,'whole_station_connections_verified':False,'manufacturing_release':False,'production_release':False,'k_completed':False,'u_started':False}
(H/'pump_motion_audit.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
print('PUMP_MOTION_BOUND',r['parts'],r['tested_pairs'],'release',False)
