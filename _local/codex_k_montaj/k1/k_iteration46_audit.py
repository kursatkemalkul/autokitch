"""Bind stage79 progress plus measured mounting joins, without release."""
from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent;source=H/'k_iteration45_audit.py'
code=source.read_text(encoding='utf-8').replace("'iteration':45","'iteration':46").replace("'source_stage':78","'source_stage':79").replace('iteration45_audit.json','iteration46_audit.json').replace('ITERATION45_BOUND','ITERATION46_BOUND')
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
def sha(name):return hashlib.sha256((H/name).read_bytes()).hexdigest()
def read(name):return json.loads((H/name).read_text(encoding='utf-8'))
report=read('iteration46_audit.json');source_audit=read('step79_source_audit.json')
assert source_audit['source_model_sha256']==report['source_model_sha256']
assert source_audit['rebound_parts_sha256']==sha('k_parca.pkl')
counts={}
for name in ('mount_connection_measured_audit.json','lower_connection_measured_audit.json'):
 data=read(name)
 assert data['source_parts_sha256']==sha('k_parca.pkl') and data['source_plan_sha256']==sha('plan_k_full.pkl')
 assert data['passed'] and not data['unresolved']
 counts[name]=len(data['checks'])
 report['artifacts_sha256'][name]=sha(name)
for name in ('step79_source_audit.json','stage79_geometry_audit.json','stage79_post_geometry_audit.json','rounded_post_recipe.json.gz','step79_ownership_rebind_audit.json'):
 report['artifacts_sha256'][name]=sha(name)
report['measured_mounting_connection_counts']=counts
report['four_pusher_profiles_and16_weld_landings_corrected_and_measured']=True
report['connection_release']=False
state=read('current_source_manifest.json')
assert state['stage']==79 and state['source_model_sha256']==report['source_model_sha256']
state['full_montage_checks_need_refresh']=False
state['rigid_montage_plan_sha256']=sha('plan_k_full.pkl')
state['rigid_montage_checks_current']=True
state['whole_station_connection_release']=False
state['manufacturing_release']=False
(H/'current_source_manifest.json').write_text(json.dumps(state,indent=2),encoding='utf-8')
report['artifacts_sha256']['current_source_manifest.json']=sha('current_source_manifest.json')
(H/'iteration46_audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print('ITERATION46_MOUNTS_BOUND',counts,'whole_station_release',False,flush=True)
