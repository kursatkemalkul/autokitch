"""Activate verified DIN geometry locally; invalidate all old motion approvals."""
from pathlib import Path
import json, hashlib, shutil
H=Path(__file__).resolve().parent
C=H.parent/'din_mount_candidate'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
a=read(C/'source_geometry_audit.json')
assert a['a_b_byte_identical'] and a['parts']==873
assert not a['changed_nodes_outside_scope'] and all(r['passed'] for r in a['joints']) and len(a['joints'])==8
assert sha(C/'A/hat3_v10v.glb')==sha(C/'B/hat3_v10v.glb')==a['output_sha256']
assert sha(H/'k_parca_din_verified.pkl')==a['verified_parts_sha256']
r=read(H/'din_ownership_rebind_audit.json');assert r['passed'] and not r['ambiguous'] and not r['unmatched_expected_count']
e=read(H/'current_sheet_encoding_audit_din.json');assert e['passed'] and len(e['checks'])==68
c=read(H/'physical_sheet_closure_audit_din.json');assert c['passed_closure_only'] and c['physical_sheet_count']==68 and not c['open_sheets']
assert c['source_encoding_sha256']==sha(H/'current_sheet_bending_din.json')
previous=read(H/'current_source_manifest.json')
assert previous['source_model_sha256']=='415044b5baa2e454c6976f99a72460a52c6ed8b5c5c42a396a3deb22af856f75'
backup=H/'iteration46_before_panel';assert not backup.exists();backup.mkdir()
names=('k_bil.pkl','k_bil.json','k_parca.pkl','surface_ownership_registry.json','current_sheet_bending.json','current_sheet_encoding_audit.json','physical_sheet_closure_audit.json','custom_flat_stock_audit.json','plan_k.pkl','plan_k_full.pkl','plan_k_dense.pkl','full_ccd_plan_k_full.json','dense_bend_morph_audit.json','current_source_manifest.json','bench_plans.pkl','bench_prototype_audit.json','bench_integration_audit.json','plan_audit.json','plan_source_binding_audit.json')
for n in names:
 if (H/n).exists():shutil.copy2(H/n,backup/n)
pairs={'k_bil_din.pkl':'k_bil.pkl','k_bil_din.json':'k_bil.json','k_parca_din_verified.pkl':'k_parca.pkl','surface_ownership_registry_din.json':'surface_ownership_registry.json','current_sheet_bending_din.json':'current_sheet_bending.json','current_sheet_encoding_audit_din.json':'current_sheet_encoding_audit.json','physical_sheet_closure_audit_din.json':'physical_sheet_closure_audit.json','custom_flat_stock_audit_din.json':'custom_flat_stock_audit.json'}
for s,t in pairs.items():shutil.copy2(H/s,H/t)
state={'stage':79,'local_refinement':'panel_and_DIN_mounts','source_model_sha256':a['output_sha256'],'raw_parts_file':'k_parca_din_raw.pkl','raw_parts_sha256':sha(H/'k_parca_din_raw.pkl'),'previous_verified_parts_file':'iteration46_before_panel/k_parca.pkl','previous_registry_file':'iteration46_before_panel/surface_ownership_registry.json','current_parts_sha256':sha(H/'k_parca.pkl'),'registry_sha256':sha(H/'surface_ownership_registry.json'),'source_sheets':68,'full_montage_checks_need_refresh':True,'rigid_montage_checks_current':False,'whole_station_connection_release':False,'manufacturing_release':False,'production_release':False}
(H/'current_source_manifest.json').write_text(json.dumps(state,indent=2),encoding='utf-8')
print('ACTIVATED_LOCAL_DIN',state['source_model_sha256'],flush=True)
