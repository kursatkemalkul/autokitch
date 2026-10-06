"""Four native post caps welded before their posts enter K. Source geometry unchanged."""
from pathlib import Path
H=Path(__file__).resolve().parent;variant=H/'catalog_station.py'
ns=dict(__file__=str(variant),__name__='variant_definition')
prefix=variant.read_text(encoding='utf-8').rsplit("exec(compile(code,str(source),'exec')",1)[0]
exec(compile(prefix,str(variant),'exec'),ns)
code=ns['code'];source=ns['source']
anchor='# Resolve previously observed blocked paths by precedence, without removing any obstacles.'
assert code.count(anchor)==1
code=code.replace(anchor,"""# Native flush welded caps are finished on each free post before erection.
for head in ('kose_dikmesi_20_-800','kose_dikmesi_20_42','kose_dikmesi_380_-800','kose_dikmesi_380_42'):
 cap=head+'_tapa'
 assert head in P and cap in P and head not in GROUPS and cap not in done
 GROUPS[head]=[head,cap];done.add(cap)
"""+anchor)
for old,new in [('catalog_order_constraints.json','cap_order_constraints.json'),('catalog_plan_progress.json','cap_plan_progress.json'),('plan_k_catalog_candidate.pkl','plan_k_cap_candidate.pkl'),('catalog_plan_audit.json','cap_plan_audit.json'),('catalog_weld_schedule_audit.json','cap_weld_schedule_audit.json')]:code=code.replace(old,new)
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
