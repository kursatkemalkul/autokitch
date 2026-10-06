"""Refresh unresolved joins from current geometry; never infer a safe mount."""
from pathlib import Path
from collections import Counter
import json,pickle,hashlib
H=Path(__file__).resolve().parent
def read(name):return json.loads((H/name).read_text(encoding='utf-8'))
def sha(name):return hashlib.sha256((H/name).read_bytes()).hexdigest()
previous=read('connection_worklist.json')
old={r['part']:r for r in previous['unresolved']}
P=pickle.load((H/'k_parca.pkl').open('rb'))['P']
connections=read('baglanti_denetim.json')
rows=[]
for name,c in sorted(connections.items()):
 if c['sinif']!='BAGLANTISIZ':continue
 part=P[name];v=part['V'];prior=old.get(name,{})
 rows.append({'part':name,'role':prior.get('role','connection_requires_source_review'),'native_bom':prior.get('native_bom',[]),'lo_mm':v.min(0).tolist(),'hi_mm':v.max(0).tolist(),'classifier_category':c.get('kategori'),'assembly_step':c.get('adim'),'release_resolved':False,'previously_listed':name in old})
report={'source_parts_sha256':sha('k_parca.pkl'),'source_plan_sha256':sha('plan_k.pkl'),'source_connection_audit_sha256':sha('baglanti_denetim.json'),'production_release':False,'count':len(rows),'categories':dict(Counter(r['classifier_category'] for r in rows)),'new_unresolved_parts':[r['part'] for r in rows if not r['previously_listed']],'not_in_current_unresolved_list':[n for n in sorted(old) if n not in {r['part'] for r in rows}],'note':'A changed classifier result is not proof of a real fastening. Supplier internals and group membership require explicit evidence.','unresolved':rows}
(H/'connection_worklist_current.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print('CURRENT_UNRESOLVED',report['count'],report['categories'],'new',report['new_unresolved_parts'],flush=True)
