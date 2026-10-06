"""Fix the actuator bracket before adding the actuator and its accessories."""
from pathlib import Path
H=Path(__file__).resolve().parent
variant=H/'site_station_candidate.py'
ns=dict(__file__=str(variant),__name__='variant_definition')
prefix=variant.read_text(encoding='utf-8').rsplit("exec(compile(code,str(source),'exec')",1)[0]
exec(compile(prefix,str(variant),'exec'),ns)
code=ns['code'];source=ns['source']
anchor='ordered=[];cycle_breaks=[]'
assert anchor in code
code=code.replace(anchor,"""_actuator_order_path=HERE/'actuator_order_probe.json'
_actuator_order=json.loads(_actuator_order_path.read_text(encoding='utf-8'))
assert not _actuator_order['source_precedence_cyclic']
assert _actuator_order['source_parts_sha256']==hashlib.sha256((HERE/'k_parca_bottom_verified.pkl').read_bytes()).hexdigest()
for a,b in _actuator_order['requested_edges']:before(a,b)
"""+anchor)
route_anchor="  else:alternatives=AD"
assert code.count(route_anchor)==1
code=code.replace(route_anchor,"""  elif a=='DGRF-C-63-125_govde':
   # Keep the actuator in front of fixed beam nuts while lowering, then
   # seat back on the actual centring/mounting interface.
   alternatives=[YOL((0,700,0),(0,0,d)) for d in (20,25,30,40,50,60,80,100)]+AD
"""+route_anchor)
for old,new in [('site_order_constraints.json','actuator_order_constraints.json'),
                ('site_plan_progress.json','actuator_plan_progress.json'),
                ('plan_k_site_candidate.pkl','plan_k_actuator_candidate.pkl'),
                ('site_plan_audit.json','actuator_plan_audit.json'),
                ('site_weld_schedule_audit.json','actuator_weld_schedule_audit.json')]:
    code=code.replace(old,new)
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
