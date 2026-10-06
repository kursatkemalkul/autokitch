"""Schedule actual station welds when their measured carriers are seated.

Preserves source geometry and v6 placement code. Bench seams stay in their
verified bench groups. This does not approve torch access or fixture support.
"""
from pathlib import Path
H=Path(__file__).resolve().parent
variant=H/'bottom_station_candidate.py'
ns=dict(__file__=str(variant),__name__='variant_definition')
prefix=variant.read_text(encoding='utf-8').split("exec(compile(code,str(source),'exec')")[0]
exec(compile(prefix,str(variant),'exec'),ns)
code=ns['code'];source=ns['source']
anchor='ordered=[];cycle_breaks=[]'
assert anchor in code
code=code.replace(anchor,"""_weld_contact_path=HERE/'site_weld_contacts.json'
_weld_contacts=json.loads(_weld_contact_path.read_text(encoding='utf-8'))
import hashlib
assert _weld_contacts['source_parts_sha256']==hashlib.sha256((HERE/'k_parca_bottom_verified.pkl').read_bytes()).hexdigest()
_site_welds={a:r['carriers'] for a,r in _weld_contacts['welds'].items()
             if a not in done and r['carrier_count']>=2}
assert all(P[a]['tur']=='kaynak' for a in _site_welds)
done.update(_site_welds)
_site_pending=set(_site_welds);_site_weld_log=[]
def grow_ready_site_welds(clock,trigger):
 for weld in sorted(_site_pending.copy()):
  hosts=_site_welds[weld]
  if not all(a in YER and a in CUR and np.linalg.norm(CUR[a])<1e-8 for a in hosts):continue
  assert all(YER[a]<=clock+.001 for a in hosts)
  begin=clock
  clock=buyu(weld,clock,.6)
  olay(begin,'Kaynak: '+weld.replace('_',' ')+' — taşıyıcılar oturduktan sonra birleştiriliyor; torç/fikstür denetimi ayrı.')
  _site_weld_log.append(dict(weld=weld,carriers=hosts,carrier_seated_seconds={a:YER[a] for a in hosts},
                             start_seconds=begin,end_seconds=clock,trigger=trigger))
  _site_pending.remove(weld)
 return clock
"""+anchor)
anchor=" (HERE/'bottom_plan_progress.json').write_text"
assert anchor in code
code=code.replace(anchor," t=grow_ready_site_welds(t,a)\n"+anchor)
anchor='for a in CEVRE:'
assert anchor in code
code=code.replace(anchor,"""assert not _site_pending,('Weld carriers never seated',sorted(_site_pending))
(HERE/'site_weld_schedule_audit.json').write_text(json.dumps({
 'source_parts_sha256':_weld_contacts['source_parts_sha256'],
 'source_contacts_sha256':hashlib.sha256(_weld_contact_path.read_bytes()).hexdigest(),
 'checks':_site_weld_log,'scheduled_welds':len(_site_weld_log),
 'all_carriers_seated_before_welding':all(all(t<=r['start_seconds']+.001 for t in r['carrier_seated_seconds'].values()) for r in _site_weld_log),
 'source_geometry_changed':False,'torch_access_checked':False,'fixture_checked':False,
 'production_release':False},indent=2),encoding='utf-8')
"""+anchor)
for old,new in [('bottom_order_constraints.json','site_order_constraints.json'),
                ('bottom_plan_progress.json','site_plan_progress.json'),
                ('plan_k_bottom_candidate.pkl','plan_k_site_candidate.pkl'),
                ('bottom_plan_audit.json','site_plan_audit.json')]:
    code=code.replace(old,new)
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
