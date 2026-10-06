"""Bind bottom-support results to one source and plan; no production approval."""
from pathlib import Path
import hashlib,json,gzip
H=Path(__file__).resolve().parent
C=H.parent/'belt_bottom_mount_candidate'
def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
g=read(C/'source_geometry_audit.json')
assert g['a_b_byte_identical'] and g['parts']==885 and not g['changed_nodes_outside_scope']
assert sha(C/'A/hat3_v10x.glb')==sha(C/'B/hat3_v10x.glb')==g['output_sha256']
assert sha(H/'k_parca_bottom_verified.pkl')==g['verified_parts_sha256']
bind=read(H/'actuator_plan_source_binding_audit.json')
plan=read(H/'actuator_plan_audit.json')
bench=read(H/'bottom_bench_prototype_audit.json')
integration=read(H/'actuator_bench_integration_audit.json')
ccd=read(H/'full_ccd_plan_k_actuator_full.json')
dense=read(H/'actuator_dense_bend_morph_audit.json')
closure=read(H/'physical_sheet_closure_audit_bottom.json')
assert bind['source_model_sha256']==integration['source_model_sha256']==ccd['source_model_sha256']==g['output_sha256']
assert bind['source_parts_sha256']==g['verified_parts_sha256']
assert not plan['plan_problems'] and not plan['unplanned'] and plan['parts']==885
assert len(bench['groups'])==17 and all(not r['plan_problems'] for r in bench['groups'])
assert bind['source_plan_sha256']==integration['source_plan_sha256']==sha(H/'plan_k_actuator_candidate.pkl')
assert integration['combined_plan_sha256']==ccd['source_plan_sha256']==dense['source_plan_sha256']==sha(H/'plan_k_actuator_full.pkl')
assert ccd['rigid_path_passed'] and not ccd['path_issues'] and ccd['step_mm']==2
assert dense['bend_morph_sampling_passed'] and dense['dense_plan_sha256']==sha(H/'plan_k_actuator_dense.pkl')
assert closure['passed_closure_only'] and closure['physical_sheet_count']==80 and not closure['open_sheets']
assert closure['source_encoding_sha256']==sha(H/'current_sheet_bending_bottom.json')
files=['bottom_body_connection_measured_audit.json','bottom_lower_connection_measured_audit.json',
       'bottom_mount_connection_measured_audit.json','bottom_panel_join_audit.json']
counts={}
for name in files:
    audit=read(H/name)
    assert audit['source_parts_sha256']==g['verified_parts_sha256'] and audit['passed']
    counts[name]=len(audit['checks'])
sequence=read(H/'actuator_mount_sequence_audit.json')
assert sequence['passed'] and sequence['source_plan_sha256']==sha(H/'plan_k_actuator_full.pkl')
assert len(g['measured_joints'])==4 and all(r['passed'] for r in g['measured_joints'])
access=read(C/'access_audit.json')
assert access['passed_access_and_insertion_only']
assert access['candidate_geometry_sha256']==sha(C/'geometry.json.gz')
work=read(H/'actuator_connection_worklist.json')
assert work['source_parts_sha256']==g['verified_parts_sha256'] and work['source_plan_sha256']==sha(H/'plan_k_actuator_full.pkl')
registry=H/'surface_ownership_registry_bottom.json'
packed=H/'surface_ownership_registry_bottom.json.gz'
packed.write_bytes(gzip.compress(registry.read_bytes(),mtime=0))
files += ['actuator_plan_audit.json','actuator_plan_source_binding_audit.json','bottom_bench_prototype_audit.json',
          'actuator_bench_integration_audit.json','full_ccd_plan_k_actuator_full.json',
          'actuator_dense_bend_morph_audit.json','physical_sheet_closure_audit_bottom.json',
          'current_sheet_encoding_audit_bottom.json','actuator_mount_sequence_audit.json',
          'actuator_connection_worklist.json','surface_ownership_registry_bottom.json.gz']
report={'source_model_sha256':g['output_sha256'],'parts':885,'triangles':g['triangles'],
        'closed_source_sheets':80,'bench_groups':17,'rigid_paths_passed':True,
        'tested_pairs':ccd['tested_pairs'],'measured_joint_counts':counts,
        'measured_bottom_clamps':4,'bottom_clamp_access_and_insertion_passed':True,
        'subsequent_load_order_passed':True,'bend_sampling_passed':True,
        'artifacts_sha256':{name:sha(H/name) for name in files},
        'contact_classifier_unresolved':work['count'],'contact_classifier_categories':work['categories'],
        'canonical_source_changed':False,'manufacturing_release':False,
        'whole_station_connections_verified':False,'production_release':False,'k_completed':False,'u_started':False,
        'remaining':['Whole-station connections, supplier clips and mounting',
                     'Actual temporary fixtures, support and weld torch/heat protection',
                     'Actual forming tooling, self-contact and secondary machining',
                     'Custom stock and hinge conformity',
                     'Shared-chain lock, registration and current-source replay',
                     'Final common-player generation, browser review and release']}
(H/'actuator_motion_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('ACTUATOR_MOTION_BOUND',885,80,ccd['tested_pairs'],'production_release',False,flush=True)
