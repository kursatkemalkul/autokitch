"""Compose explicit native cap fabrication into existing common-player plan data."""
from pathlib import Path
import pickle,json,hashlib
H=Path(__file__).resolve().parent;source=H/'k_bench_birlestir.py'
code=source.read_text(encoding='utf-8')
for old,new in [('plan_k.pkl','plan_k_cap_candidate.pkl'),('bench_plans.pkl','cap_bench_plans.pkl'),('k_parca.pkl','k_parca_catalog_verified.pkl'),('plan_k_full.pkl','plan_k_cap_full.pkl'),('bench_integration_audit.json','cap_bench_integration_audit.json')]:code=code.replace(old,new)
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
p=H/'plan_k_cap_full.pkl';D=pickle.loads(p.read_bytes());B=pickle.loads((H/'cap_bench_plans.pkl').read_bytes());audit=json.loads((H/'cap_bench_integration_audit.json').read_text())
root=json.loads((H/'catalog_flush_cap_welds.json').read_text());joins=[]
for g in audit['groups']:
 w=B['groups'][g['head']].get('native_flush_cap_weld')
 if not w:continue
 r=next(x for x in root['checks'] if x['profile']==w['profile'])
 t0=g['base_seconds']+w['t0'];t1=g['base_seconds']+w['t1']
 assert t1<g['departure_seconds']
 joins.append(dict(w,t0=t0,t1=t1,root_segments_mm=r['closed_root_segments'],bench_offset_m=g['bench_offset_m'],post_and_cap_fixed_before_group_delivery=True,visual_highlight_integrated=False))
assert len(joins)==4
D['FABRICATION_JOINS']=joins;pickle.dump(D,p.open('wb'))
audit['combined_plan_sha256']=hashlib.sha256(p.read_bytes()).hexdigest();audit['native_flush_cap_welds']=joins
(H/'cap_bench_integration_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
print('CAP_FABRICATION_JOINS',len(joins),'PARTS',len(D['P']),flush=True)
