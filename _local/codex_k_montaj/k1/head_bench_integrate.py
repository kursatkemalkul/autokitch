"""Compose explicit native cap fabrication into existing common-player plan data."""
from pathlib import Path
import pickle,json,hashlib
H=Path(__file__).resolve().parent;source=H/'k_bench_birlestir.py'
code=source.read_text(encoding='utf-8')
for old,new in [('plan_k.pkl','plan_k_head_candidate.pkl'),('bench_plans.pkl','head_bench_plans.pkl'),('k_parca.pkl','k_parca_head_verified.pkl'),('plan_k_full.pkl','plan_k_head_full.pkl'),('bench_integration_audit.json','head_bench_integration_audit.json')]:code=code.replace(old,new)
code=code.replace('delivery=[factory,safe,above,offset]',"""delivery=[factory,safe,above,offset]
 if head in ('kafa_adaptoru','kafa_plakasi_8'):
  # Reach the low entry outside the front face before entering below the
  # actuator. A straight descent at final X/Z crosses its fixed housing.
  outside_high=np.array([0.,safe[1],1.5])
  outside_low=np.array([0.,offset[1],1.5])
  delivery=[factory,safe,outside_high,outside_low,offset]
""")
code=code.replace(" for a in s['seams']:\n  tw="," for a in s['seams']:\n  if a in b['GOR']:continue  # Retain explicit earlier measured weld operation.\n  tw=")
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
p=H/'plan_k_head_full.pkl';D=pickle.loads(p.read_bytes());B=pickle.loads((H/'head_bench_plans.pkl').read_bytes());audit=json.loads((H/'head_bench_integration_audit.json').read_text())
root=json.loads((H/'catalog_flush_cap_welds.json').read_text());joins=[]
for g in audit['groups']:
 w=B['groups'][g['head']].get('native_flush_cap_weld')
 if not w:continue
 r=next(x for x in root['checks'] if x['profile']==w['profile'])
 t0=g['base_seconds']+w['t0'];t1=g['base_seconds']+w['t1']
 assert t1<g['departure_seconds']
 joins.append(dict(w,t0=t0,t1=t1,root_segments_mm=r['closed_root_segments'],bench_offset_m=g['bench_offset_m'],post_and_cap_fixed_before_group_delivery=True,visual_highlight_integrated=False))
assert len(joins)==4
for g in audit['groups']:
 if g['head']!='kafa_adaptoru':continue
 bench=B['groups'][g['head']]
 for i in range(3):
  seam='k79_kafa_dikme_TIG_'+str(i);rod='ara_dikme_'+str(i)
  t0=g['base_seconds']+bench['MF'][seam]['buyu'][0]
  t1=g['base_seconds']+bench['MF'][seam]['buyu'][1]
  assert t1<g['departure_seconds']
  assert bench['YER'][rod]<=bench['MF'][seam]['buyu'][0]+.001
  joins.append({'type':'continuous_rod_TIG','part':seam,'carriers':[rod,'kafa_adaptoru'],'t0':t0,'t1':t1,'bench_offset_m':g['bench_offset_m'],'fixed_before_group_delivery':True,'torch_access_report':'cut_head_yoke_candidate/torch_access_audit.json'})
assert len(joins)==7

D['FABRICATION_JOINS']=joins;pickle.dump(D,p.open('wb'))
audit['combined_plan_sha256']=hashlib.sha256(p.read_bytes()).hexdigest();audit['fabrication_joins']=joins
(H/'head_bench_integration_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
print('CAP_FABRICATION_JOINS',len(joins),'PARTS',len(D['P']),flush=True)
