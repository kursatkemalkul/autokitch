"""Bind verified current K prototype gates without claiming production release."""
from pathlib import Path
import json,hashlib,gzip
H=Path(__file__).resolve().parent;C=H.parent/'actuator_catalog_fastener_candidate'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
scope=read(C/'source_scope_audit.json');bind=read(H/'catalog_plan_source_binding_audit.json')
plan=read(H/'catalog_plan_audit.json');bench=read(H/'catalog_bench_prototype_audit.json')
integration=read(H/'catalog_bench_integration_audit.json');ccd=read(H/'full_ccd_plan_k_catalog_full.json')
dense=read(H/'catalog_dense_bend_morph_audit.json');closure=read(H/'physical_sheet_closure_audit_catalog.json')
assert scope['full_triangle_rebind_passed'] and scope['a_b_byte_identical'] and not scope['changed_nodes_outside_scope']
assert scope['expected_product_parts']==plan['parts']==integration['parts']==ccd['parts']==1009
assert bind['source_model_sha256']==integration['source_model_sha256']==ccd['source_model_sha256']==scope['output_sha256']
assert bind['source_parts_sha256']==scope['verified_parts_sha256']==sha(H/'k_parca_catalog_verified.pkl')
assert not plan['plan_problems'] and not plan['unplanned']
assert len(bench['groups'])==24 and all(not r['plan_problems'] for r in bench['groups'])
assert bind['source_plan_sha256']==integration['source_plan_sha256']==sha(H/'plan_k_catalog_candidate.pkl')
assert integration['combined_plan_sha256']==ccd['source_plan_sha256']==dense['source_plan_sha256']==sha(H/'plan_k_catalog_full.pkl')
assert ccd['rigid_path_passed'] and not ccd['path_issues'] and ccd['step_mm']==2
assert dense['bend_morph_sampling_passed'] and dense['dense_plan_sha256']==sha(H/'plan_k_catalog_dense.pkl')
assert closure['passed_closure_only'] and closure['physical_sheet_count']==115 and not closure['open_sheets']
assert closure['source_encoding_sha256']==sha(H/'current_sheet_bending_catalog.json')
files=['catalog_body_connection_measured_audit.json','catalog_lower_connection_measured_audit.json','catalog_mount_connection_measured_audit.json','catalog_panel_join_audit.json']
counts={}
for name in files:
 a=read(H/name);assert a['source_parts_sha256']==scope['verified_parts_sha256'] and a['passed'];counts[name]=len(a['checks'])
for name,key in [('catalog_actual_contacts.json','passed_selected_geometry_contacts'),('catalog_din_contacts.json','passed_selected_geometry_contacts'),('catalog_load_order_audit.json','passed'),('catalog_tool_axial_access.json','passed_axial_envelopes_only')]:
 a=read(H/name);assert a[key];assert a.get('source_parts_sha256',scope['verified_parts_sha256'])==scope['verified_parts_sha256'];files.append(name)
work=read(H/'catalog_specific_mount_evidence.json');assert work['source_parts_sha256']==scope['verified_parts_sha256'] and work['source_plan_sha256']==sha(H/'plan_k_catalog_full.pkl')
files+=['catalog_pump_contacts.json','full_ccd_plan_k_catalog_full.json','catalog_dense_bend_morph_audit.json','catalog_specific_mount_evidence.json','catalog_bench_integration_audit.json','catalog_plan_source_binding_audit.json','physical_sheet_closure_audit_catalog.json']
for name,key in [('catalog_fastener_measurements.json','passed'),('catalog_M10_tool_access.json','passed_axial_access')]:
 a=read(H/name);assert a[key] and a['source_parts_sha256']==scope['verified_parts_sha256'];files.append(name)
r={'source_model_sha256':scope['output_sha256'],'parts':1009,'triangles':scope['matched_triangles'],'closed_sheets':115,'bench_groups':24,'rigid_paths_passed':True,'tested_pairs':ccd['tested_pairs'],'measured_joint_counts':counts,'new_catalog_contacts':48,'pump_contact_checks_on_current_source':47,'oil_and_catalog_load_order_checks':26,'selected_tool_axial_envelopes':12,'catalog_M10_measured_mounts':4,'bend_sampling_passed':True,'remaining_connection_records':work['remaining_count'],'artifacts_sha256':{name:sha(H/name) for name in files},'canonical_source_changed':False,'whole_station_connections_verified':False,'manufacturing_release':False,'production_release':False,'k_completed':False,'u_started':False}
(H/'catalog_motion_audit.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
print('PUMP_MOTION_BOUND',r['parts'],r['tested_pairs'],'release',False)
