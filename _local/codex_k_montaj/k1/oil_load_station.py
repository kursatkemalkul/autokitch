"""Adapt the established K/v6 plan to real oil wall/shelf/plate fastenings."""
from pathlib import Path
import json,hashlib,pickle
H=Path(__file__).resolve().parent;variant=H/'mount_station_candidate.py'
ns=dict(__file__=str(variant),__name__='variant_definition')
prefix=variant.read_text(encoding='utf-8').rsplit("exec(compile(code,str(source),'exec')",1)[0]
exec(compile(prefix,str(variant),'exec'),ns)
code=ns['code'];source=ns['source']
scope=json.loads((H.parent/'oil_load_mount_candidate/source_scope_audit.json').read_text(encoding='utf-8'))
path=H/'k_parca_oil_load_verified.pkl'
assert scope['full_triangle_rebind_passed'] and hashlib.sha256(path.read_bytes()).hexdigest()==scope['verified_parts_sha256']
P=pickle.loads(path.read_bytes())['P']
old_order=json.loads((H/'mount_order_probe.json').read_text(encoding='utf-8'))
assert all(a in P and b in P for a,b in old_order['requested_edges'])
new_order=dict(old_order,source_parts_sha256=scope['verified_parts_sha256'],
               inherited_edge_report_sha256=hashlib.sha256((H/'mount_order_probe.json').read_bytes()).hexdigest())
(H/'oil_load_mount_order_probe.json').write_text(json.dumps(new_order,indent=2),encoding='utf-8')
for old,new in [('k_parca_bottom_verified.pkl','k_parca_oil_load_verified.pkl'),
                ('current_sheet_bending_bottom.json','current_sheet_bending_oil_load.json'),
                ('native_sheet_mapping_audit_bottom.json','native_sheet_mapping_audit_oil_load.json'),
                ('site_weld_contacts.json','oil_load_weld_contacts.json'),
                ('mount_order_probe.json','oil_load_mount_order_probe.json')]:code=code.replace(old,new)
anchor='# Mount the long left wireway'
assert anchor in code
code=code.replace(anchor,"""# Fabricate two real corner brackets and the front retaining strip on a
# bench; they remain independent station attachments with explicit bolts.
for side in ('sol','sag'):
 head='yag_pompa_rafi_kosebendi_'+side
 GROUPS[head]=[head,'k79_yag_raf_yatay_kosebent_'+side]
 WELDS[head]=['k79_yag_raf_kose_kaynagi_'+side]
 done.update(GROUPS[head][1:]);done.update(WELDS[head])
GROUPS['yag_pompa_rafi']=['yag_pompa_rafi','k79_yag_raf_on_dayama']
WELDS['yag_pompa_rafi']=['k79_yag_raf_on_dayama_kaynagi']
done.add('k79_yag_raf_on_dayama');done.add('k79_yag_raf_on_dayama_kaynagi')

"""+anchor)
anchor='# Base first; finished welded supports next, shelf later; enclosing panels last.'
code=code.replace(anchor,"""_oil_load=json.loads((HERE.parent/'oil_load_mount_candidate/audit.json').read_text(encoding='utf-8'))
for j in _oil_load['joins']:
 a=j['stud'];receiver=j['wall'];e=np.array(j['axis'],float)
 P[a].update(yan=e,pem_ad='PEM FHP M5x12',sac=receiver)
 PRESS_BY_SHEET.setdefault(receiver,[]).append(a);done.add(a)
 haric(a,receiver,'FHP M5x12 presses into the measured native Ø5 wall bore; own flush press-head material only, not an obstruction exemption')
 THREAD_AXES[j['washer']]=(e*100.).tolist();THREAD_AXES[j['nut']]=(e*100.).tolist()
 haric(a,j['nut'],'Measured M5 stud/nut thread pair:5mm engagement and1.5mm protrusion, common X-axis insertion only')
for j in _oil_load['load_joins']:
 THREAD_AXES[j['screw']]=[0,100.,0]
 for a in (j['shim'],j['washer'],j['nut']):THREAD_AXES[a]=[0,-100.,0]
 haric(j['screw'],j['nut'],'Measured catalog DIN7991 M5x16 / ISO10511 M5 pair:5mm engagement,2mm protrusion; common Y-axis only')
"""+anchor)
anchor='ordered=[];cycle_breaks=[]'
code=code.replace(anchor,"""# Fix both brackets to the walls before loading the shelf.
for j in _oil_load['joins']:
 before(j['wall'],j['bracket']);before(j['bracket'],j['washer'])
 before(j['washer'],j['nut']);before(j['nut'],'yag_pompa_rafi')
for j in _oil_load['load_joins']:
 before(j['host'],j['carrier']);before(j['carrier'],j['screw'])
 before(j['screw'],j['shim']);before(j['shim'],j['washer']);before(j['washer'],j['nut'])
 targets=['yag_pompa_plakasi'] if j['carrier']=='yag_pompa_rafi' else [a for a in P if a.startswith(('yag_pompasi_','yag_emis_filtresi','yag_T_parcasi','yag_geri_basinc_','yag_basinc_sensoru_','yag_boru_'))]
 for a in targets:before(j['nut'],a)
"""+anchor)
anchor="  elif a=='DGRF-C-63-125_govde':"
assert anchor in code
code=code.replace(anchor,"""  elif a.startswith('yag_pompa_rafi_kosebendi_'):
   side=a.rsplit('_',1)[-1];sgn=1. if side=='sol' else -1.
   alternatives=[YOL((sgn*d,0,0)) for d in (100,150,250,400)]
"""+anchor)
for old,new in [('mount_order_constraints.json','oil_load_order_constraints.json'),
                ('mount_plan_progress.json','oil_load_plan_progress.json'),
                ('plan_k_mount_candidate.pkl','plan_k_oil_load_candidate.pkl'),
                ('mount_plan_audit.json','oil_load_plan_audit.json'),
                ('mount_weld_schedule_audit.json','oil_load_weld_schedule_audit.json')]:code=code.replace(old,new)
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
