"""Run the existing contact classifier on the complete verified new source."""
from pathlib import Path
import hashlib,json
H=Path(__file__).resolve().parent;source=H/'baglanti_denetim.py'
code=source.read_text(encoding='utf-8').split('# taşıyıcı ↔ taşıyıcı temas')[0]
anchor="D = pickle.load(open('plan_k.pkl', 'rb'))"
assert anchor in code
code=code.replace(anchor,"""_input=Path('k_parca_catalog_verified.pkl')
_scope=json.loads((Path(HERE).parent/'actuator_catalog_fastener_candidate/source_scope_audit.json').read_text(encoding='utf-8'))
assert _scope['full_triangle_rebind_passed']
P0=pickle.load(_input.open('rb'))['P']
D=dict(P=P0,HAR={a:[] for a in P0},GOR={a:0. for a in P0},MF={},ADIM=[],
 CEVRE=[a for a in P0 if P0[a]['tur']=='cevre'])
""")
ns=dict(__file__=str(source),__name__='oil_source_contacts',Path=Path)
exec(compile(code,str(source),'exec'),ns)
rows={a:{'carriers':sorted(hosts),'carrier_count':len(hosts)}
      for a,hosts in ns['DEG'].items() if ns['P'][a]['tur']=='kaynak'}
scope=json.loads((H.parent/'actuator_catalog_fastener_candidate/source_scope_audit.json').read_text(encoding='utf-8'))
r={'source_parts_sha256':hashlib.sha256((H/'k_parca_catalog_verified.pkl').read_bytes()).hexdigest(),
   'source_model_sha256':scope['output_sha256'],'distance_tolerance_mm':ns['TOL'],
   'welds':rows,'weld_count':len(rows),'with_at_least_two_carriers':sum(r['carrier_count']>=2 for r in rows.values()),
   'welds_without_two_carriers':[a for a,r in rows.items() if r['carrier_count']<2],
   'production_release':False,'torch_access_checked':False}
(H/'catalog_weld_contacts.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
print('OIL_LOAD_WELD_CONTACTS',r['weld_count'],r['with_at_least_two_carriers'],flush=True)
