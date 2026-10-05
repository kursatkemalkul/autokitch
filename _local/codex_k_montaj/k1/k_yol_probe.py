"""Probe candidate K insertion paths against a completed plan; no geometry/model edits.
Omitted predecessors are explicit proposed rescheduling, never collision exceptions.
A selected witness still requires a complete subsequent planner run.
"""
from pathlib import Path
import pickle,json,sys,os,time,hashlib
HERE=Path(__file__).resolve().parent
text=(HERE/'k_montaj.py').read_text(encoding='utf-8').split('ordered=[];cycle_breaks=[]')[0]
ns={'__file__':str(HERE/'k_montaj.py'),'__name__':'path_probe'};exec(compile(text,str(HERE/'k_montaj.py'),'exec'),ns)
D=pickle.load((HERE/'plan_k.pkl').open('rb'));a=sys.argv[1];omitted=[a for a in sys.argv[2:] if not a.startswith('+')];earlier=[a[1:] for a in sys.argv[2:] if a.startswith('+')];members=list(dict.fromkeys(ns['GROUPS'].get(a,[a])+list(ns['PRESS_BY_SHEET'].get(a,()))));start=D['GOR'][a]
ns['YERINDE'][:]=[n for n,t in D['GOR'].items() if t<start-.001 and n not in members and n not in omitted and (n not in D['CEVRE'] or n=='cevre_B')]
ns['YERINDE'][:]=list(dict.fromkeys(ns['YERINDE']+earlier))
ns['HARIC_PLAN']=set(map(tuple,D['HARIC_PLAN']));ns['HARIC_NEDEN']=D['HARIC_NEDEN']
YOL=ns['YOL'];choices=[YOL((-650,0,0)),YOL((0,0,950),(-24,0,0)),YOL((0,0,-950),(-24,0,0))] if a=='sol_sac_urun_girisi' else ([YOL((650,0,0)),YOL((0,0,950),(24,0,0))] if a=='sag_sac_E_penceresi' else [])
if a.startswith('govde_kulak_sag_'):
 choices=[YOL((0,0,z),(0,y,0),(-x,0,0)) for z in (950,-950) for x in (50,75,100) for y in (0,15,30,-15)]
for x in (35,50):
 for y in (50,100,150,200):choices.append(YOL((0,0,950),(0,y,0),(x,0,0)))
for x in (35,50,75,100,-35,-50):
 for y in (50,100,150,-50,-100):
  choices.append(YOL((0,0,950),(x,0,0),(0,y,0)))
for x in (35,50,75,100,-35,-50):
 for z in (50,-50,100,-100):choices.append(YOL((0,700,0),(x,0,0),(0,0,z)))
rows=[];T=time.time();witness=None
for ci,path in enumerate(choices):
 print('CANDIDATE',ci+1,[p.tolist() for p in path],flush=True)
 bad=[]
 for p,q in zip(path[:-1],path[1:]):
  bad+=ns['serbest'](members,p,ns['YERINDE'],ofs2=q)
  if bad:break
 row={'path_mm':[p.tolist() for p in path],'blockers':sorted(set(b for _,b in bad))};rows.append(row)
 if not bad:witness=row;break
result={'part':a,'source_plan_sha256':hashlib.sha256((HERE/'plan_k.pkl').read_bytes()).hexdigest(),'tested_members_including_pressed_hardware':members,'proposed_later_parts':omitted,'proposed_earlier_parts':earlier,'witness':witness,'checked':rows,'elapsed_seconds':time.time()-T,'production_release':False}
(HERE/('probe_'+a+'.json')).write_text(json.dumps(result,indent=2),encoding='utf-8')
print('PROBE',a,'checks',len(rows),'seconds',round(time.time()-T,2),'WITNESS',None if witness is None else witness['path_mm'],flush=True);os._exit(0)
