"""Bench path/manufacture prototype using the unchanged TOPPING v6 planner.
Does not modify the station plan or claim complete connections/tool access.
"""
from pathlib import Path
import sys,pickle,json,time,os
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];os.chdir(HERE)
sys.path.insert(0,str(ROOT/'_local/claude_son_yerel/gece2/cekmece'));sys.path.insert(0,str(HERE))
import yol_denetim_v2 as Y
import v2geo as G
from k_sac_kaynak import load
D=pickle.load((HERE/'k_parca.pkl').open('rb'));P=D['P'];SAC,_=load(P)
# Reuse the declared groups without running the station placement loop.
text=(HERE/'k_montaj.py').read_text(encoding='utf-8');prefix=text.split('ordered=[];cycle_breaks=[]')[0]
initial={'__file__':str(HERE/'k_montaj.py'),'__name__':'bench_initial'};exec(compile(prefix,str(HERE/'k_montaj.py'),'exec'),initial)
report=[];bench_plans={};t0=time.time()
for head,members in initial['GROUPS'].items():
 if not any(a in SAC for a in members):continue
 seams=initial['WELDS'].get(head,[]);presses=list(initial['PRESS_BY_SHEET'].get(head,()));parts={a:dict(initial['P'][a]) for a in list(dict.fromkeys(members+seams+presses))}
 ns=dict(bk=lambda a:a.replace('_',' '),tr=lambda a:parts[a]['ac'],P=parts,SAC={a:SAC[a] for a in members if a in SAC},np=np,Y=Y,G=G)
 exec((HERE/'_altyapi.py').read_text(encoding='utf-8'),ns)
 from k_yol_hiz import install
 install(ns)
 for pair in initial['HARIC_PLAN']:
  if all(a in parts for a in pair):ns['HARIC_PLAN'].add(pair);ns['HARIC_NEDEN'][pair]=initial['HARIC_NEDEN'].get(pair,'declared source interface')
 tt=0.;operations=[([a],presses if a==head else []) for a in members]
 if head.startswith('k71_alt_flans_'):
  profile=next(a for a in members if a.startswith('k71_dik_destek_'));cap=next(a for a in members if a.startswith('k71_disli_ust_kapak_'))
  operations=[([head],presses),([profile],[]),([cap],[])]
 if head.startswith('k72_itici_taban_'):
  upper=next(a for a in members if a.startswith('k72_itici_ust_plaka_'))
  fragment=next(a for a in members if a.startswith('itici_taban_'))
  upright=next(a for a in members if a.startswith('k_itici_sac_'))
  assert upper in SAC and fragment in SAC and SAC[upper].record['name']==SAC[fragment].record['name']
  operations=[([head],presses),([upper,fragment],[]),([upright],[])]
 if head=='sag_sac_E_penceresi':
  ears=[a for a in members if a.startswith('govde_kulak_sag_')]
  ducts=[a for a in members if a.startswith('elk_ic_kanal_')]
  # Press the panel studs before installing ears and their washer/nut.
  operations=[([head],presses)]
  for side in ('on','arka'):
   base=f'govde_kulak_sag_{side}_1150'
   operations += [([base],[]),([base+'_bag_pul'],[]),([base+'_bag_somun'],[])]
  operations += [([a],[]) for a in ducts]
 if head=='k_govde_on_seffaf_0':
  presses=[a for a in members if '_pem_' in a]
  for a in presses:parts[a]['yan']=[0,0,1];parts[a]['pem_ad']='SP-M5-1'
  outer=[a for a in members if a in SAC and SAC[a].record['name']=='onyuz_kapak_K']
  counter=[a for a in members if '_karsilik_' in a]
  other=[a for a in members if a not in outer+counter+presses+['k_govde_on_seffaf_1']]
  other.sort(key=lambda a:('_vida_' in a,a))
  operations=[(['k_govde_on_seffaf_1'],presses)]+[([a],[]) for a in counter]+[(outer,[])]+[([a],[]) for a in other]
 for names,presses in operations:
  a=names[0];directions=[ns['YOL'](q) for q in [(0,0,950),(0,0,-950),(0,700,0),(-650,0,0),(650,0,0),(0,-650,0)]]
  if '_kanat_vida_' in a:directions=[ns['YOL']((0,0,-40))]+directions
  tt=ns['yerlestir'](names,directions,tt,P[a]['ac'],pem=presses,sure_bekle=.02)
  # Separate GLB fragments of one physical source sheet bend together.
  for child in names[1:]:
   assert child in SAC and SAC[child].record['name']==SAC[a].record['name']
   ns['FRAMES'][child]=SAC[child].frames();ns['MF'][child]=dict(seg=[list(x) for x in ns['MF'][a]['seg']])
 # The prototype deliberately leaves welding/connection release open.
 row={'head':head,'members':members,'source_sheet_members':[a for a in members if a in SAC],'laser_timeline_parts':[a['ad'] for a in ns['ACN']],'bend_frame_parts':list(ns['FRAMES']),'plan_problems':ns['PLAN_SORUN'],'welds_to_verify':seams,'connection_release':False,'seconds':tt}
 bench_plans[head]={k:ns[k] for k in ('HAR','GOR','MF','FRAMES','VU','ISTISNA','ROT','ADIM','OLAY','KAM','ACN','YER','PLAN_SORUN')};bench_plans[head]['members']=members;bench_plans[head]['seconds']=tt
 report.append(row);print('BENCH',head,'members',len(members),'laser',len(ns['ACN']),'path_problems',len(ns['PLAN_SORUN']),flush=True)
(HERE/'bench_prototype_audit.json').write_text(json.dumps({'groups':report,'execution_seconds':time.time()-t0,'production_release':False},ensure_ascii=False,indent=2),encoding='utf-8')
import hashlib
pickle.dump({'source_parts_sha256':hashlib.sha256((HERE/'k_parca.pkl').read_bytes()).hexdigest(),'groups':bench_plans},(HERE/'bench_plans.pkl').open('wb'))
sys.stdout.flush();os._exit(0)
