"""Measure carrier contacts of actual source welds for assembly scheduling.

Uses the existing distance classifier; this is geometry/timing evidence,
not weld strength, torch access or fixture approval.
"""
from pathlib import Path
import hashlib,json
H=Path(__file__).resolve().parent
source=H/'baglanti_denetim.py'
code=source.read_text(encoding='utf-8').split('# taşıyıcı ↔ taşıyıcı temas')[0]
code=code.replace('plan_k.pkl','plan_k_bottom_full.pkl')
ns=dict(__file__=str(source),__name__='site_weld_contacts')
exec(compile(code,str(source),'exec'),ns)
P=ns['P'];D=ns['D'];carriers=ns['DEG']
rows={a:{'carriers':sorted(carriers[a]),'carrier_count':len(carriers[a])}
      for a in carriers if P[a]['tur']=='kaynak'}
report={'source_parts_sha256':D['source_parts_sha256'],
        'source_model_sha256':D['source_model_sha256'],
        'source_plan_sha256':hashlib.sha256((H/'plan_k_bottom_full.pkl').read_bytes()).hexdigest(),
        'distance_tolerance_mm':ns['TOL'],'welds':rows,
        'weld_count':len(rows),'with_at_least_two_carriers':sum(r['carrier_count']>=2 for r in rows.values()),
        'welds_without_two_carriers':[a for a,r in rows.items() if r['carrier_count']<2],
        'production_release':False,'torch_access_checked':False}
(H/'site_weld_contacts.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('SITE_WELD_CONTACTS',report['weld_count'],report['with_at_least_two_carriers'],flush=True)
