"""Check real mounting precedence before changing any placement trajectory."""
from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent
variant=H/'site_station_candidate.py'
ns=dict(__file__=str(variant),__name__='variant_definition')
text=variant.read_text(encoding='utf-8').rsplit("exec(compile(code,str(source),'exec')",1)[0]
exec(compile(text,str(variant),'exec'),ns)
code=ns['code'].split('ordered=[];cycle_breaks=[]')[0]
initial=dict(__file__=str(ns['source']),__name__='order_probe')
exec(compile(code,str(ns['source']),'exec'),initial)
before=initial['before'];P=initial['P'];alias=initial['alias']
requested=[]
def link(a,b):
    assert a in P and b in P
    before(a,b);requested.append([a,b])
for i in range(2):
    nut=f'k75_kiris_somun_{i}'
    for target in ('DGRF-C-63-125_govde','DGRF_ZBH-12_0','DGRF_ZBH-12_1'):
        link(nut,target)
for i in range(4):
    screw=f'DGRF_M10_civata_{i}'
    for target in ('DGRF_port_on_QSL','DGRF_port_arka_QSL','DGRF_SMT-8M_0','DGRF_SMT-8M_1'):
        link(screw,target)
# Keep the service-side bridge and local electrical bracket open until
# the cylinder is seated and secured by all four real M10 fasteners.
for target in ('kopru_kirisi_-126','elk_k_celik_2'):
    link('DGRF-C-63-125_govde',target)
    for i in range(4):link(f'DGRF_M10_civata_{i}',target)
# Attach the mounting plate before local ancillary brackets add load.
for i in range(2):
    for target in ('elk_k_celik_3','elk_k_celik_4','elk_k_celik_5','elk_k_tarti_celik_0'):
        link(f'k75_kiris_somun_{i}',target)
# Weld receiving ears to seated posts, rather than placing posts onto loose ears.
for ear,post in [('govde_kulak_sol_arka_841','kose_dikmesi_20_-800'),
                 ('govde_kulak_sol_on_841','kose_dikmesi_20_42')]:
    link(post,ear)
remaining=set(initial['items']);edges=initial['edges'];ordered=[]
while remaining:
    ready={a for a in remaining if not any(b==a and x in remaining for x,b in edges)}
    if not ready:break
    a=min(ready,key=initial['seqrank']);ordered.append(a);remaining.remove(a)
blocked={a:[x for x,b in edges if b==a and x in remaining] for a in sorted(remaining)}
report={'source_parts_sha256':hashlib.sha256((H/'k_parca_bottom_verified.pkl').read_bytes()).hexdigest(),
        'requested_edges':requested,'source_precedence_cyclic':bool(remaining),
        'ordered_items':len(ordered),'blocked_items':blocked,
        'geometry_or_paths_changed':False,'production_release':False}
(H/'mount_order_probe.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('ACTUATOR_ORDER_PROBE','cycles',len(remaining),'ordered',len(ordered),flush=True)
