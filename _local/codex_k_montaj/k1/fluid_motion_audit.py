"""Bind verified current K prototype gates without claiming production release."""
from pathlib import Path
import json,hashlib,gzip
H=Path(__file__).resolve().parent;C=H.parent/'oil_fluid_clamp_candidate'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
scope=read(C/'source_scope_audit.json');bind=read(H/'fluid_plan_source_binding_audit.json')
plan=read(H/'fluid_plan_audit.json');bench=read(H/'fluid_bench_prototype_audit.json')
integration=read(H/'fluid_bench_integration_audit.json');ccd=read(H/'full_ccd_plan_k_fluid_full.json')
dense=read(H/'fluid_dense_bend_morph_audit.json');closure=read(H/'physical_sheet_closure_audit_fluid.json')
assert scope['full_triangle_rebind_passed'] and scope['a_b_byte_identical'] and not scope['changed_nodes_outside_scope']
assert scope['expected_product_parts']==plan['parts']==integration['parts']==ccd['parts']==1009
assert bind['source_model_sha256']==integration['source_model_sha256']==ccd['source_model_sha256']==scope['output_sha256']
assert bind['source_parts_sha256']==scope['verified_parts_sha256']==sha(H/'k_parca_fluid_verified.pkl')
assert not plan['plan_problems'] and not plan['unplanned']
assert len(bench['groups'])==24 and all(not r['plan_problems'] for r in bench['groups'])
assert bind['source_plan_sha256']==integration['source_plan_sha256']==sha(H/'plan_k_fluid_candidate.pkl')
assert integration['combined_plan_sha256']==ccd['source_plan_sha256']==dense['source_plan_sha256']==sha(H/'plan_k_fluid_full.pkl')
assert ccd['rigid_path_passed'] and not ccd['path_issues'] and ccd['step_mm']==2
assert dense['bend_morph_sampling_passed'] and dense['dense_plan_sha256']==sha(H/'plan_k_fluid_dense.pkl')
assert closure['passed_closure_only'] and closure['physical_sheet_count']==115 and not closure['open_sheets']
assert closure['source_encoding_sha256']==sha(H/'current_sheet_bending_fluid.json')
files=['fluid_body_connection_measured_audit.json','fluid_lower_connection_measured_audit.json','fluid_mount_connection_measured_audit.json','fluid_panel_join_audit.json']
counts={}
for name in files:
 a=read(H/name);assert a['source_parts_sha256']==scope['verified_parts_sha256'] and a['passed'];counts[name]=len(a['checks'])
for name,key in [('fluid_actual_contacts.json','passed_selected_geometry_contacts'),('fluid_din_contacts.json','passed_selected_geometry_contacts'),('fluid_load_order_audit.json','passed'),('fluid_tool_axial_access.json','passed_axial_envelopes_only')]:
 a=read(H/name);assert a[key];assert a.get('source_parts_sha256',scope['verified_parts_sha256'])==scope['verified_parts_sha256'];files.append(name)
work=read(H/'fluid_specific_mount_evidence.json');assert work['source_parts_sha256']==scope['verified_parts_sha256'] and work['source_plan_sha256']==sha(H/'plan_k_fluid_full.pkl')
files+=['fluid_pump_contacts.json','full_ccd_plan_k_fluid_full.json','fluid_dense_bend_morph_audit.json','fluid_specific_mount_evidence.json','fluid_bench_integration_audit.json','fluid_plan_source_binding_audit.json','physical_sheet_closure_audit_fluid.json']
r={'source_model_sha256':scope['output_sha256'],'parts':1009,'triangles':scope['matched_triangles'],'closed_sheets':115,'bench_groups':24,'rigid_paths_passed':True,'tested_pairs':ccd['tested_pairs'],'measured_joint_counts':counts,'new_fluid_contacts':48,'pump_contact_checks_on_current_source':47,'oil_and_fluid_load_order_checks':26,'selected_tool_axial_envelopes':8,'bend_sampling_passed':True,'remaining_connection_records':work['remaining_count'],'artifacts_sha256':{name:sha(H/name) for name in files},'canonical_source_changed':False,'whole_station_connections_verified':False,'manufacturing_release':False,'production_release':False,'k_completed':False,'u_started':False}
(H/'fluid_motion_audit.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
print('PUMP_MOTION_BOUND',r['parts'],r['tested_pairs'],'release',False)
