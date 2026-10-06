"""Activate audited source79 and preserve stage78 local caches and checks."""
from pathlib import Path
import json,hashlib,shutil
H=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
audit=json.loads((H/'step79_source_audit.json').read_text(encoding='utf-8'))
assert audit['two_runs_byte_identical'] and audit['closed_sheets']==67 and audit['four_rounded_posts_and16_weld_landings_measured_passed']
assert sha(H/'surface_ownership_registry79.json')==audit['registry_sha256']
assert sha(H/'k_parca79_verified.pkl')==audit['rebound_parts_sha256']
assert sha(H/'current_sheet_bending79.json')==audit['encoded_sheets_sha256']
manifest=H/'current_source_manifest.json';previous=json.loads(manifest.read_text(encoding='utf-8'))
assert previous['stage']==78,'Only stage78 may be replaced; preserve newer work'
backup=H/'iteration45';backup.mkdir(exist_ok=True)
for name in ('k_bil.pkl','k_bil.json','k_parca.pkl','surface_ownership_registry.json','current_sheet_bending.json','current_sheet_encoding_audit.json','physical_sheet_closure_audit.json','plan_k.pkl','plan_k_full.pkl','plan_k_dense.pkl','full_ccd_plan_k_full.json','dense_bend_morph_audit.json','iteration45_audit.json','current_source_manifest.json'):
 source=H/name;target=backup/name
 if source.exists():
  assert not target.exists(),('Do not overwrite prior cache',str(target))
  shutil.copy2(source,target)
pairs={'k_bil79.pkl':'k_bil.pkl','k_bil79.json':'k_bil.json','k_parca79_verified.pkl':'k_parca.pkl','surface_ownership_registry79.json':'surface_ownership_registry.json','current_sheet_bending79.json':'current_sheet_bending.json','current_sheet_encoding_audit79.json':'current_sheet_encoding_audit.json','physical_sheet_closure_audit79.json':'physical_sheet_closure_audit.json','custom_flat_stock_audit79.json':'custom_flat_stock_audit.json'}
for source,target in pairs.items():shutil.copy2(H/source,H/target)
state={'stage':79,'source_model_sha256':audit['source_model_sha256'],'raw_parts_file':'k_parca79_raw.pkl','raw_parts_sha256':sha(H/'k_parca79_raw.pkl'),'previous_verified_parts_file':'iteration45/k_parca.pkl','previous_registry_file':'iteration45/surface_ownership_registry.json','current_parts_sha256':sha(H/'k_parca.pkl'),'registry_sha256':sha(H/'surface_ownership_registry.json'),'full_montage_checks_need_refresh':True,'production_release':False}
manifest.write_text(json.dumps(state,indent=2),encoding='utf-8')
print('ACTIVATED_STEP79',state['source_model_sha256'],flush=True)
