"""Close four explicit source-defined post/cap weld records on current plan.

This only covers the four named welds, not all station connections. Factory
interface evidence is rebound by actual current-plan group membership.
"""
from pathlib import Path
import hashlib, json, pickle
H=Path(__file__).resolve().parent
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name): return json.loads((H/name).read_text(encoding='utf-8-sig'))
plan=H/'plan_k_cap_full.pkl';D=pickle.loads(plan.read_bytes())
previous=read('catalog_supplier_interfaces.json')
source=H/'k_parca_catalog_verified.pkl'
assert sha(source)==previous['source_parts_sha256']
assert D['source_model_sha256']==previous['source_model_sha256']
display=read('cap_weld_display_audit.json')
assert display['source_plan_sha256']==sha(plan)
root=read('catalog_flush_cap_welds.json')
assert root['source_parts_sha256']==sha(source)
assert root['all_cap_root_geometries_within_0_6_mm']
torch=read('cap_torch_access.json')
assert torch['source_parts_sha256']==sha(source)
for r in previous['explicit_factory_interface_records']:
    child,unit=r['part'],r['supplier_unit']
    assert D['HAR'][child]==D['HAR'][unit] and D['GOR'][child]==D['GOR'][unit]
rows=[]
open_names={r['part'] for r in previous['remaining_unresolved']}
for j in D['FABRICATION_JOINS']:
    cap,post=j['cap'],j['profile']
    assert cap in open_names and j['post_and_cap_fixed_before_group_delivery']
    assert j['t1']>j['t0'] and len(j['root_segments_mm'])==8
    tool=next(r for r in torch['checks'] if r['cap']==cap)
    # A measured limiting tool envelope establishes reachability of the
    # weld. This does not claim a particular purchased torch was certified.
    assert tool['passed_free_post_cap_envelope']
    rows.append({'part':cap,'support':post,'type':'source_defined_continuous_flush_TIG',
        'source_definition':'arastirma/_uretec/h3/h3_k_sac_v1.py:iskelet',
        'operation_seconds':[j['t0'],j['t1']], 'root_segments':8,
        'fixed_before_station_delivery':True,
        'ground_flush_source_geometry_preserved':True,
        'surface_display_report':'cap_weld_display_audit.json',
        'limiting_torch_envelope_report':'cap_torch_access.json',
        'specific_purchased_torch_certification_claimed':False})
assert len(rows)==4
closed={r['part'] for r in rows}
r={'source_model_sha256':previous['source_model_sha256'],'source_parts_sha256':sha(source),
   'source_plan_sha256':sha(plan),'previous_report_sha256':sha(H/'catalog_supplier_interfaces.json'),
   'explicit_factory_groups_rebound':True,'cap_weld_connections':rows,
   'remaining_unresolved':[r for r in previous['remaining_unresolved'] if r['part'] not in closed],
   'remaining_count':previous['remaining_count']-4,
   'whole_station_connections_verified':False,'production_release':False}
(H/'cap_connection_evidence.json').write_text(json.dumps(r,indent=2,ensure_ascii=False),encoding='utf-8')
print('CAP_CONNECTIONS',len(rows),'remaining',r['remaining_count'])
