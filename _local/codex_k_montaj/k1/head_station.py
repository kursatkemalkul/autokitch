"""Existing TOPPINGv6 K planner: source-bound head fabrication and insertions.
Finished rod/adaptor welds are made on the bench. Lower6+upper2 cassette
travels under a declared temporary clamp until its three M8 screws are seated.
All part paths still use the unchanged common placement checker.
"""
from pathlib import Path
import json,hashlib,pickle
H=Path(__file__).resolve().parent;variant=H/'cap_station.py'
ns=dict(__file__=str(variant),__name__='variant_definition')
prefix=variant.read_text(encoding='utf-8').rsplit("exec(compile(code,str(source),'exec')",1)[0]
exec(compile(prefix,str(variant),'exec'),ns)
code=ns['code'];source=ns['source']
scope=json.loads((H.parent/'cut_head_yoke_candidate/source_scope_audit.json').read_text())
path=H/'k_parca_head_verified.pkl'
assert scope['full_triangle_rebind_passed'] and hashlib.sha256(path.read_bytes()).hexdigest()==scope['verified_parts_sha256']
for old,new in [('k_parca_catalog_verified.pkl','k_parca_head_verified.pkl'),('current_sheet_bending_catalog.json','current_sheet_bending_head.json'),('native_sheet_mapping_audit_catalog.json','native_sheet_mapping_audit_head.json'),('cap_order_constraints.json','head_order_constraints.json'),('cap_plan_progress.json','head_plan_progress.json'),('plan_k_cap_candidate.pkl','plan_k_head_candidate.pkl'),('cap_plan_audit.json','head_plan_audit.json'),('cap_weld_schedule_audit.json','head_weld_schedule_audit.json'),('catalog_weld_contacts.json','head_weld_contacts.json'),('catalog_mount_order_probe.json','head_mount_order_probe.json')]:code=code.replace(old,new)
anchor='# Resolve previously observed blocked paths by precedence, without removing any obstacles.'
assert code.count(anchor)==1
code=code.replace(anchor,"""# Actual three continuous rod/adaptor welds. Upper4 is removable stock.
head='kafa_adaptoru'
GROUPS[head]=[head]+['ara_dikme_'+str(i) for i in range(3)]
WELDS[head]=['k79_kafa_dikme_TIG_'+str(i) for i in range(3)]
done.update(GROUPS[head][1:]);done.update(WELDS[head])
# Temporary fixture keeps lower6+upper2 registered while entering below.
# It is released only after the three M8 seats, not a permanent connection.
GROUPS['kafa_plakasi_8']=['kafa_plakasi_8','k79_kafa_ust_plaka_2'];done.add('k79_kafa_ust_plaka_2')
for i in range(3):THREAD_AXES['k79_kafa_alt_M8x20_'+str(i)]=[0,-100.,0]
for i in range(4):THREAD_AXES['k79_kafa_yoke_M8x25_'+str(i)]=[0,-100.,0]
"""+anchor)
anchor='ordered=[];cycle_breaks=[]'
assert code.count(anchor)==1
code=code.replace(anchor,"""for blade in P:
 if blade.startswith('bicak_') and blade!='bicak_koruma_halkasi':
  edges.discard((alias.get(blade,blade),'kopru_kirisi_-286'));before('kopru_kirisi_-286',blade)
before('DGRF-C-63-125_govde','k79_kafa_adaptor_ust_plaka_4')
before('k79_kafa_adaptor_ust_plaka_4','kafa_adaptoru')
for i in range(4):
 screw='k79_kafa_yoke_M8x25_'+str(i)
 before('kafa_adaptoru',screw);before(screw,'kafa_plakasi_8')
for i in range(3):
 screw='k79_kafa_alt_M8x20_'+str(i)
 before('kafa_plakasi_8',screw)
 for a in P:
  if a.startswith(('bicak_','koruma_braketi_','kelebek_somun_')):before(screw,a)
"""+anchor)
anchor="  elif a.startswith('koruma_braketi_'):"
assert code.count(anchor)==1
code=code.replace(anchor,"""  elif a in ('kafa_adaptoru','kafa_plakasi_8','k79_kafa_adaptor_ust_plaka_4'):
   alternatives=[YOL((0,-d,0)) for d in (80,150,300)]+AD
"""+anchor)
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
