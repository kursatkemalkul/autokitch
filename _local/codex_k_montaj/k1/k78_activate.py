"""Activate audited step78 caches locally, preserving the prior checkpoint.

No chain registration, shared model integration, website or release changes.
"""
from pathlib import Path
import json,hashlib,shutil
H=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
audit=json.loads((H/'step78_source_audit.json').read_text(encoding='utf-8'))
assert audit['two_runs_byte_identical'] and audit['closed_sheets']==67
assert sha(H/'surface_ownership_registry78.json')==audit['registry_sha256']
assert sha(H/'k_parca78_verified.pkl')==audit['rebound_parts_sha256']
assert sha(H/'current_sheet_bending78.json')==audit['encoded_sheets_sha256']
manifest=H/'current_source_manifest.json'
if manifest.exists():
 previous=json.loads(manifest.read_text(encoding='utf-8'))
 if previous['source_model_sha256']==audit['source_model_sha256']:raise SystemExit('Step78 already active; preserve existing checkpoint')
backup=H/'iteration43';backup.mkdir(exist_ok=True)
for name in ('k_bil.pkl','k_bil.json','k_parca.pkl','surface_ownership_registry.json','current_sheet_bending.json','current_sheet_encoding_audit.json','physical_sheet_closure_audit.json','plan_k.pkl','plan_k_full.pkl','plan_k_dense.pkl','full_ccd_plan_k_full.json','dense_bend_morph_audit.json','iteration43_audit.json'):
 source=H/name;target=backup/name
 if source.exists():
  assert not target.exists(),('Checkpoint already exists; do not overwrite',str(target))
  shutil.copy2(source,target)
pairs={'k_bil78.pkl':'k_bil.pkl','k_bil78.json':'k_bil.json','k_parca78_verified.pkl':'k_parca.pkl','surface_ownership_registry78.json':'surface_ownership_registry.json','current_sheet_bending78.json':'current_sheet_bending.json','current_sheet_encoding_audit78.json':'current_sheet_encoding_audit.json','physical_sheet_closure_audit78.json':'physical_sheet_closure_audit.json','custom_flat_stock_audit78.json':'custom_flat_stock_audit.json'}
for source,target in pairs.items():shutil.copy2(H/source,H/target)
state={'stage':78,'source_model_sha256':audit['source_model_sha256'],'raw_parts_file':'k_parca78_raw.pkl','raw_parts_sha256':sha(H/'k_parca78_raw.pkl'),'previous_verified_parts_file':'iteration43/k_parca.pkl','previous_registry_file':'iteration43/surface_ownership_registry.json','current_parts_sha256':sha(H/'k_parca.pkl'),'registry_sha256':sha(H/'surface_ownership_registry.json'),'full_montage_checks_need_refresh':True,'production_release':False}
manifest.write_text(json.dumps(state,indent=2),encoding='utf-8')
print('ACTIVATED_STEP78',state['source_model_sha256'],'preserved_checkpoint',str(backup),flush=True)
