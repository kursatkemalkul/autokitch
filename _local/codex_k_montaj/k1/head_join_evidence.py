"""Current-plan evidence for seven actual M8 head joints and three rod welds.
Closes only named head connections; never promotes the entire K station.
"""
from pathlib import Path
import pickle,json,hashlib,numpy as np
H=Path(__file__).resolve().parent;folder=H.parent/'cut_head_yoke_candidate'
plan=H/'plan_k_head_full.pkl';D=pickle.loads(plan.read_bytes());P=D['P']
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path):return json.loads(path.read_text(encoding='utf-8'))
source=read(folder/'source_scope_audit.json');geometry=read(folder/'audit.json');access=read(folder/'access_audit.json');torch=read(folder/'torch_access_audit.json')
assert D['source_model_sha256']==source['output_sha256']
assert D['source_parts_sha256']==source['verified_parts_sha256']
assert access['candidate_geometry_sha256']==torch['candidate_geometry_sha256']==sha(folder/'geometry.json.gz')
assert access['passed_bottom_tool_access'] and access['passed_continuous_weld_contacts'] and torch['passed_all_preassembly_envelopes']
def arrival(name):return max([D['GOR'][name]]+[h[1] for h in D['HAR'][name]])
rows=[]
for j in geometry['joins']:
 screw=j['screw'];receiver=j['id'] if j['id'].startswith('ara_dikme_') else 'DGRF_boyunduruk'
 layers=['kafa_plakasi_8','k79_kafa_ust_plaka_2'] if receiver.startswith('ara_dikme_') else ['kafa_adaptoru','k79_kafa_adaptor_ust_plaka_4']
 assert j['engagement_mm']>=8. and j['blind_bottom_clearance_mm']>=j['pitch_mm']
 route=np.array(D['HAR'][screw][-1][2:]);assert np.linalg.norm(route)>0
 axis=-route/np.linalg.norm(route);assert np.linalg.norm(axis-np.array([0,1,0]))<.001
 assert all(arrival(a)<=D['GOR'][screw]+.001 for a in layers+[receiver])
 rows.append({'screw':screw,'receiver':receiver,'clamped_layers':layers,'actual_axial_insertion':[0,1,0],'catalog_length_mm':j['nominal_length_mm'],'engagement_mm':j['engagement_mm'],'blind_clearance_mm':j['blind_bottom_clearance_mm'],'assembly_complete_seconds':arrival(screw),'passed_source_bound_stack_and_order':True})
assert len(rows)==7
welds=[j for j in D['FABRICATION_JOINS'] if j.get('type')=='continuous_rod_TIG'];assert len(welds)==3
lower_release=max(r['assembly_complete_seconds'] for r in rows if r['receiver'].startswith('ara_dikme_'))
upper_release=max(r['assembly_complete_seconds'] for r in rows if r['receiver']=='DGRF_boyunduruk')
blades=[a for a in P if a.startswith(('bicak_','koruma_braketi_'))]
assert all(D['GOR'][a]>=lower_release-.001 for a in blades)
previous=read(H/'cap_connection_evidence.json')
closed={'ara_dikme_0','ara_dikme_1','ara_dikme_2','kafa_adaptoru','kafa_plakasi_8'}
remaining=[r for r in previous['remaining_unresolved'] if r['part'] not in closed]
assert len(remaining)==previous['remaining_count']-len(closed)
result={'source_model_sha256':D['source_model_sha256'],'source_parts_sha256':D['source_parts_sha256'],'source_plan_sha256':sha(plan),'head_threaded_joints':rows,'head_continuous_welds':welds,'closed_previous_head_records':sorted(closed),'remaining_unresolved':remaining,'remaining_count':len(remaining),'temporary_lower_cassette_release_seconds':lower_release,'temporary_upper_spacer_release_seconds':upper_release,'no_blade_load_before_lower_screws':True,'supplier_geometry_correction_disclosed':True,'supplier_cad_axes_visually_confirmed':False,'temporary_fixture_geometry_verified':False,'whole_station_connections_verified':False,'manufacturing_release':False,'production_release':False}
(H/'head_join_evidence.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print('HEAD_JOINTS',len(rows),'HEAD_WELDS',len(welds),'PREVIOUS_HEAD_RECORDS_CLOSED',len(closed),'REMAINING',len(remaining),flush=True)
