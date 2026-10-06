"""Two conveyor side weldments using v6 planner and verified actual source.
Diagnostic only: temporary bench support is explicitly warned, not certified.
"""
from pathlib import Path
import os,sys,json,pickle,hashlib,time
import numpy as np
H=Path(__file__).resolve().parent;ROOT=H.parents[2];os.chdir(H)
sys.path.insert(0,str(ROOT/'_local/claude_son_yerel/gece2/cekmece'));sys.path.insert(0,str(H))
import yol_denetim_v2 as Y
import v2geo as G
source=H/'k_sac_kaynak.py';code=source.read_text(encoding='utf-8').replace("'current_sheet_bending.json'","'current_sheet_bending_belt.json'").replace("'native_sheet_mapping_audit.json'","'native_sheet_mapping_audit_belt.json'")
module=dict(__file__=str(source),__name__='belt_sheets');exec(compile(code,str(source),'exec'),module)
P=pickle.load((H/'k_parca_belt_verified.pkl').open('rb'))['P'];SAC,mapping=module['load'](P)
assert all(r['passed'] for r in mapping)
joints=json.loads((H.parent/'belt_support_candidate/audit.json').read_text(encoding='utf-8'))['joints']
rows=[];plans={};started=time.time()
for z in (-421,-3):
 plate='bant_yan_'+str(z);js=[j for j in joints if j['plate']==plate]
 members=[plate];welds=[];operations=[]
 for j in js:
  x=int(j['id'].split('_')[0]);tag=f'{float(x)}_{float(z)}';flange='k72_bant_ayak_flansi_'+tag
  base_seams=sorted(n for n in P if n.startswith('k72_bant_ayak_kaynagi_'+tag+'_'))
  assert len(base_seams)==4
  members += [flange,j['post'],j['cap']]
  welds += base_seams+[j['cap_weld']]+j['plate_welds']
  operations += [([flange],[]),([j['post']],base_seams),([j['cap']],[j['cap_weld']])]
 operations.append(([plate],[w for j in js for w in j['plate_welds']]))
 parts={n:dict(P[n]) for n in members+welds}
 ns=dict(P=parts,SAC={n:SAC[n] for n in members if n in SAC},Y=Y,G=G,np=np,bk=lambda n:n.replace('_',' '),tr=lambda n:parts[n]['ac'])
 exec((H/'_altyapi.py').read_text(encoding='utf-8'),ns)
 from k_yol_hiz import install
 install(ns)
 tt=0.;ns['olay'](tt,'UYARI: Tezgâhta dayalı kaynak alt montajı; geçici destek/fikstür ve kaynak torcu erişimi henüz doğrulanmadı.')
 events=[]
 for names,seams in operations:
  tt=ns['yerlestir'](names,[ns['YOL'](v) for v in ((0,700,0),(0,0,950),(0,0,-950),(650,0,0),(-650,0,0))],tt,parts[names[0]]['ac'],sure_bekle=.02)
  arrival=tt
  for seam in seams:
   tt=ns['buyu'](seam,tt,.6)
  events.append({'parts':names,'arrival_seconds':arrival,'welds_after_arrival':seams,'finished_seconds':tt})
 row={'side_plate':plate,'members':members,'welds':welds,'events':events,'plan_problems':ns['PLAN_SORUN'],
      'supplier_rollers_in_weld_phase':False,'temporary_support_warning_shown':True,'fixtures_verified':False,'torch_access_verified':False,'production_release':False}
 rows.append(row);plans[plate]={k:ns[k] for k in ('HAR','GOR','MF','FRAMES','VU','ISTISNA','ROT','ADIM','OLAY','KAM','ACN','YER','PLAN_SORUN')}
 print('BELT_SIDE',plate,'pieces',len(members),'seams',len(welds),'path_issues',len(ns['PLAN_SORUN']),flush=True)
report={'source_parts_sha256':hashlib.sha256((H/'k_parca_belt_verified.pkl').read_bytes()).hexdigest(),
        'source_sheet_encoding_sha256':hashlib.sha256((H/'current_sheet_bending_belt.json').read_bytes()).hexdigest(),
        'sides':rows,'passed_paths_only':not any(r['plan_problems'] for r in rows),'production_release':False,'elapsed_seconds':time.time()-started}
(H/'belt_side_bench_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
pickle.dump({'source_parts_sha256':report['source_parts_sha256'],'groups':plans},(H/'belt_side_bench_plans.pkl').open('wb'))
sys.stdout.flush();os._exit(0 if report['passed_paths_only'] else 2)
