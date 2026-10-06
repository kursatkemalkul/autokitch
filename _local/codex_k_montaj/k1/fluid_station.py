"""Existing K/v6 plan with actual filter/regulator mounts before oil tubing."""
from pathlib import Path
import json,hashlib,pickle
H=Path(__file__).resolve().parent;variant=H/'pump_station.py'
ns=dict(__file__=str(variant),__name__='variant_definition')
prefix=variant.read_text(encoding='utf-8').rsplit("exec(compile(code,str(source),'exec')",1)[0]
exec(compile(prefix,str(variant),'exec'),ns)
code=ns['code'];source=ns['source']
scope=json.loads((H.parent/'oil_fluid_clamp_candidate/source_scope_audit.json').read_text(encoding='utf-8'))
path=H/'k_parca_fluid_verified.pkl'
assert scope['full_triangle_rebind_passed'] and hashlib.sha256(path.read_bytes()).hexdigest()==scope['verified_parts_sha256']
old=json.loads((H/'pump_mount_order_probe.json').read_text(encoding='utf-8'))
P=pickle.loads(path.read_bytes())['P'];assert all(a in P and b in P for a,b in old['requested_edges'])
(H/'fluid_mount_order_probe.json').write_text(json.dumps(dict(old,source_parts_sha256=scope['verified_parts_sha256']),indent=2),encoding='utf-8')
for a,b in [('k_parca_pump_verified.pkl','k_parca_fluid_verified.pkl'),('current_sheet_bending_pump.json','current_sheet_bending_fluid.json'),('native_sheet_mapping_audit_pump.json','native_sheet_mapping_audit_fluid.json'),('pump_weld_contacts.json','fluid_weld_contacts.json'),('pump_mount_order_probe.json','fluid_mount_order_probe.json')]:code=code.replace(a,b)
anchor='# Mount the long left wireway'
code=code.replace(anchor,"""# Offset portals leave the inlet and return connections clear.
_flow=json.loads((HERE.parent/'oil_fluid_clamp_candidate/audit.json').read_text(encoding='utf-8'))
for i in (0,1):
 head=f'k79_yag_akis_portal_{i}'
 js=[j for j in _flow['joins'] if j['portal']==head]
 GROUPS[head]=[head]+[j['foot'] for j in js]+[f'k79_yag_akis_ust_pad_{i}',f'k79_yag_akis_pad_yapistirici_{i}']
 WELDS[head]=[a for j in js for a in j['seams']]
 done.update(GROUPS[head][1:]);done.update(WELDS[head])
"""+anchor)
anchor='# Base first; finished welded supports next, shelf later; enclosing panels last.'
code=code.replace(anchor,"""for j in _flow['joins']:
 THREAD_AXES[j['screw']]=[0,100.,0]
 for a in (j['shim'],j['washer'],j['nut']):THREAD_AXES[a]=[0,-100.,0]
 haric(j['screw'],j['nut'],'Measured M5x20 / ISO10511 pair:5mm engagement and2mm protrusion; only the coaxial thread engagement is excluded')
"""+anchor)
anchor='ordered=[];cycle_breaks=[]'
code=code.replace(anchor,"""for j in _flow['joins']:
 before('yag_pompa_plakasi',j['supplier_body']);before(j['supplier_body'],j['portal'])
 before(j['portal'],j['screw']);before(j['screw'],j['shim'])
 before(j['shim'],j['washer']);before(j['washer'],j['nut'])
 for a in ('yag_boru_filtre_pompa','yag_boru_pompa_T','yag_boru_T_regulator','yag_emis_hortumu_TLM1008','yag_donus_hortumu_TLM0806'):
  before(j['nut'],a)
"""+anchor)
anchor="  elif a=='DGRF-C-63-125_govde':"
code=code.replace(anchor,"""  elif a.startswith('k79_yag_akis_portal_'):
   alternatives=[YOL((0,d,0)) for d in (100,150,250,400)]
"""+anchor)
for a,b in [('pump_order_constraints.json','fluid_order_constraints.json'),('pump_plan_progress.json','fluid_plan_progress.json'),('plan_k_pump_candidate.pkl','plan_k_fluid_candidate.pkl'),('pump_plan_audit.json','fluid_plan_audit.json'),('pump_weld_schedule_audit.json','fluid_weld_schedule_audit.json')]:code=code.replace(a,b)
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
