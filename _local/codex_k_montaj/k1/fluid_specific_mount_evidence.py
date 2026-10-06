from pathlib import Path
import json,pickle,hashlib
H=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
parts=H/'k_parca_fluid_verified.pkl';plan=H/'plan_k_fluid_full.pkl'
D=pickle.loads(plan.read_bytes());scope=read(H.parent/'oil_fluid_clamp_candidate/source_scope_audit.json')
assert scope['verified_parts_sha256']==sha(parts)
current=read(H/'fluid_din_evidence.json')
assert current['source_parts_sha256']==sha(parts) and current['source_plan_sha256']==sha(plan)
contacts=read(H/'fluid_actual_contacts.json');pumpcontacts=read(H/'fluid_pump_contacts.json')
load=read(H/'fluid_load_order_audit.json');tools=read(H/'fluid_tool_axial_access.json')
assert all(x['source_parts_sha256']==sha(parts) and x['passed_selected_geometry_contacts'] for x in (contacts,pumpcontacts))
assert load['passed'] and load['source_plan_sha256']==sha(plan) and tools['passed_axial_envelopes_only'] and tools['source_parts_sha256']==sha(parts)
rows=[]
for folder,body,evidence in [('oil_pump_clamp_candidate','yag_pompasi_GJ-N21_EagleDrive','fluid_pump_contacts.json'),('oil_fluid_clamp_candidate','yag_emis_filtresi','fluid_actual_contacts.json'),('oil_fluid_clamp_candidate','yag_geri_basinc_regulatoru_KBP','fluid_actual_contacts.json')]:
 definition=read(H.parent/folder/'audit.json')
 joints=[j for j in definition['joins'] if j.get('supplier_body',body)==body]
 assert len(joints)==(4 if folder=='oil_pump_clamp_candidate' else 2) and all(j['passed_stack'] for j in joints)
 rows.append({'part':body,'type':'removable_external_hold_down','joints':[j['id'] for j in joints],'contact_report':evidence,'contact_report_sha256':sha(H/evidence),'fix_before_pipe_and_hose_load_report':'fluid_load_order_audit.json','load_capacity_certification_claimed':False})
units=[('DGRF-C-63-125_govde',['DGRF_silindir_borusu','DGRF_uc_kapagi','DGRF_boyunduruk','DGRF_kilavuz_mili_0','DGRF_kilavuz_mili_1','DGRF_piston_mili','DGRF_piston'],'https://media.festo.com/media/202791_documentation.pdf')]
for prefix in ('itici_X_MY1B10G-250','itici_Z_MY1B10G-350'):
 units.append((prefix+'_profil',[prefix+'_uc_kapagi_0',prefix+'_uc_kapagi_1',prefix+'_masa'],'https://www.smcworld.com/catalog/BEST-5-2-en/pdf/2-p1211-1325-my1b_en.pdf'))
open_names={r['part'] for r in current['remaining_unresolved']}
for head,members,doc in units:
 assert all(a in D['P'] and D['HAR'][a]==D['HAR'][head] and D['GOR'][a]==D['GOR'][head] for a in members)
 for a in members:
  if a not in open_names:continue
  rows.append({'part':a,'type':'supplier_internal_delivered_assembly','supplier_unit':head,'supplier_document':doc,'explicit_native_member':True,'same_full_plan_motion_and_visibility_as_unit':True,'external_unit_mount_verified_by_this_record':False,'note':'Only this named factory-internal part is accepted as delivered assembled. Our brackets, sensors, fittings and the unit external mounting are not covered.'})
resolved={r['part'] for r in rows};assert resolved<=open_names
r={'source_parts_sha256':sha(parts),'source_plan_sha256':sha(plan),'source_model_sha256':scope['output_sha256'],'previous_report_sha256':sha(H/'fluid_din_evidence.json'),'specific_evidence':rows,'resolved_named_records':len(rows),'remaining_unresolved':[x for x in current['remaining_unresolved'] if x['part'] not in resolved],'remaining_count':current['remaining_count']-len(rows),'production_release':False,'whole_station_connections_verified':False}
(H/'fluid_specific_mount_evidence.json').write_text(json.dumps(r,indent=2,ensure_ascii=False),encoding='utf-8')
print('SPECIFIC_MOUNT_EVIDENCE',len(rows),'remaining',r['remaining_count'])
