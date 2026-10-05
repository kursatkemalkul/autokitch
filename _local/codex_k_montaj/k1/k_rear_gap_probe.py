from pathlib import Path
import sys,json,pickle,numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'_local/claude_son_yerel/gece2/cekmece'))
import yol_denetim_v2 as Y
P=pickle.load((HERE/'k_parca.pkl').open('rb'))['P'];SAC={};tr=lambda a:a;bk=lambda a:a
exec((HERE/'_altyapi.py').read_text(encoding='utf-8'))
rows=[]
for a in P:
 if not a.startswith('govde_bag_arka_') or not a.endswith(('_pul','_somun')):continue
 stud=a.rsplit('_',1)[0]+'_saplama';isnut=a.endswith('_somun');dz=6. if isnut else 8.
 if isnut:HARIC_PLAN.add((a,stud))
 paths=[]
 for k in (0,1):
  for sign in (-1,1):
   side=np.zeros(3);side[k]=sign*100;ax=np.array([0,0,dz]);points=YOL(side,ax)
   errors=[]
   for first,last in zip(points[:-1],points[1:]):errors+=serbest([a],first,[q for q in P if q!=a.rsplit('_',1)[0]+'_somun' or isnut],ofs2=last)
   paths.append({'waypoints_mm':[x.tolist() for x in points],'errors':errors})
 clean=next((x for x in paths if not x['errors']),None)
 rows.append({'part':a,'clean_path':clean,'trials':paths});print(a,'PASS' if clean else paths[0]['errors'],flush=True)
(HERE/'rear_gap_probe.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
