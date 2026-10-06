"""Whole conveyor subassembly with bottom-access station mounting.
Uses the established v6 planner; separate candidate outputs, no release.
"""
from pathlib import Path
H=Path(__file__).resolve().parent;source=H/'k_montaj.py'
code=source.read_text(encoding='utf-8').replace("'k_parca.pkl'","'k_parca_bottom_verified.pkl'")
code=code.replace('from k_sac_kaynak import load as load_current_sheets','''
_sheet_source=HERE/'k_sac_kaynak.py'
_sheet_code=_sheet_source.read_text(encoding='utf-8').replace("'current_sheet_bending.json'","'current_sheet_bending_bottom.json'").replace("'native_sheet_mapping_audit.json'","'native_sheet_mapping_audit_bottom.json'")
_sheet_ns=dict(__file__=str(_sheet_source),__name__='bottom_sheet_loader');exec(compile(_sheet_code,str(_sheet_source),'exec'),_sheet_ns)
load_current_sheets=_sheet_ns['load']
''')
anchor='GROUPS[head]=members;done.update(members[1:])\n\n# Mount the long left wireway'
replace='''_belt_meta=json.loads((HERE.parent/'belt_support_candidate/audit.json').read_text(encoding='utf-8'))
_bottom_meta=json.loads((HERE.parent/'belt_bottom_mount_candidate/audit.json').read_text(encoding='utf-8'))
seams=[]
for j,k in zip(_belt_meta['joints'],_bottom_meta['joints']):
 assert j['id']==k['id']
 x,z=j['id'].split('_');tag=f'{float(x)}_{float(z)}'
 members += ['k72_bant_ayak_flansi_'+tag,j['post'],j['cap'],k['insert']]
 seams += sorted(a for a in P if a.startswith('k72_bant_ayak_kaynagi_'+tag+'_'))+[j['cap_weld']]+j['plate_welds']+[k['insert_weld']]
assert len(members)==28 and len(seams)==32
GROUPS[head]=members;WELDS[head]=seams;done.update(members[1:]);done.update(seams)

# Mount the long left wireway'''
assert anchor in code;code=code.replace(anchor,replace)
anchor="elif a=='bant_yan_-421':alternatives=[YOL((0,700,0),(0,0,-d)) for d in (50,100,150)]+AD"
assert anchor in code
# The welded foot flanges land flat on the installed shelf. Seat the whole
# frame vertically; the old final lateral segment crossed the landing face.
code=code.replace(anchor,"elif a=='bant_yan_-421':alternatives=[YOL((0,700,0))]")
code=code.replace("members=[a for a in j['parts'] if a in P]\n  if j", "members=[a for a in j['parts'] if a in P]\n  if not members:continue\n  if j")
anchor='# Base first; finished welded supports next, shelf later; enclosing panels last.'
code=code.replace(anchor,"""# Actual bottom-entry offset is negativeY; no old top-entry hardware reused.
for j in _bottom_meta['joints']:
 THREAD_AXES[j['washer']]=[0,-100.,0];THREAD_AXES[j['screw']]=[0,-100.,0]
"""+anchor)
anchor='ordered=[];cycle_breaks=[]'
code=code.replace(anchor,"""# Seat the complete bench-built frame, washer first, then screw from below.
# No subsequent pusher/load-bearing mechanism is placed before tightening.
for j in _bottom_meta['joints']:
 before('bant_yan_-421',j['washer']);before(j['washer'],j['screw'])
 for a in P:
  if a.startswith(('itici_X_','itici_Z_')) or a=='itici_sabit_plaka':before(j['screw'],a)
"""+anchor)
for old,new in [('order_constraints.json','bottom_order_constraints.json'),('plan_progress.json','bottom_plan_progress.json'),('plan_k.pkl','plan_k_bottom_candidate.pkl'),('plan_audit.json','bottom_plan_audit.json')]:code=code.replace(old,new)
code=code.replace('from k_son_kaynak import bind as bind_full_source\nbind_full_source()','')
# Explicit provisional support message; specific fixing step IDs need integration.
code=code.replace("print('INSTALL',a,flush=True)","print('INSTALL',a,flush=True)\n if a=='bant_yan_-421':olay(t,'GEÇİCİ DAYALI: Bant kaynak alt montajı raf üzerinde; sonraki dört alttan M6x16 bağlantısıyla sabitlenecek. Alt montaj fikstürü ve kaynak torcu doğrulaması henüz açık.')\n if a.startswith('k79_bant_M6x16_alttan_'):olay(t,'Önce dayanan bant alt montajı şimdi alttan M6x16 ile sabitleniyor.')")
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
