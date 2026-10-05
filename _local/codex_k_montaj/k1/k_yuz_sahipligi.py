"""Identify mislabeled surfaces against native CAD without modifying model geometry."""
from pathlib import Path
import sys,pickle,json,os,time
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'arastirma/_uretec/codex/k_montaj'))
from lower_support import *
from current_cad import factory_from_source
factory=factory_from_source(K,OUT)
D=pickle.load((HERE/'k_parca.pkl').open('rb'));P=D['P']
source_names=['arka_sac','ust_sac','sol_sac_urun_girisi','sag_sac_E_penceresi']
source_names += [a for a in P if a.startswith('kose_dikmesi_') and (a.endswith('_tapa') or a.count('_')==3)]
source_names=[a for a in source_names if a in P]
native={s.ad:s.parca()['sh'] for s in factory.SAC if s.ad in source_names}
native.update({p.ad:p.parca()['sh'] for p in factory.PROFIL if p.ad in P})
for p in factory.KAYNAK:
 if p['ad'].startswith('kose_dikmesi'):native[p['ad']]=p['sh']
native={a:sh.translate((4000,0,0)) for a,sh in native.items()}
native['k_e4_sol_yama_40x40']=K.kutu(4001.5,4003,1789,1829,-790,-750)
boxes={a:np.array([[s.BoundingBox().xmin,s.BoundingBox().ymin,s.BoundingBox().zmin],[s.BoundingBox().xmax,s.BoundingBox().ymax,s.BoundingBox().zmax]]) for a,s in native.items()}
changes=[];unknown=[];counts={};t0=time.time()
# Only the seven failing names. Do not disturb correct labels or global geometry.
checks=json.loads((HERE/'current_sheet_encoding_audit.json').read_text(encoding='utf-8'))['checks']
for row in checks:
 a=row['name']
 if row['endpoint_passed'] or a not in P:continue
 v=P[a];tri=v['V'][v['F']];moved=0
 for i,q in enumerate(tri):
  lo=q.min(0);hi=q.max(0);centre=q.mean(0);matches=[]
  for b,sh in native.items():
   box=boxes[b]
   if np.any(lo<box[0]-.015) or np.any(hi>box[1]+.015):continue
   d=sh.distance(cq.Vertex.makeVertex(*centre))
   # GLB bend chords can deviate from the analytic surface between exact vertices; validate all vertices below, retain the centre distance for tie-breaking.
   ds=[0. if sh.isInside(cq.Vector(*x),.001) else sh.distance(cq.Vertex.makeVertex(*x)) for x in q]
   if max(ds)>.015:continue
   matches.append((max(d,max(ds)),b))
  if any(b==a for _,b in matches):continue
  if not matches:
   unknown.append({'part':a,'triangle':i,'centre':centre.tolist()});continue
  _,b=min(matches)
  changes.append({'from':a,'triangle':i,'to':b});moved+=1;counts[a+' -> '+b]=counts.get(a+' -> '+b,0)+1
 print('SURFACE',a,'faces',len(tri),'moved',moved,'unknown',sum(r['part']==a for r in unknown),'s',round(time.time()-t0),flush=True)
(HERE/'surface_ownership_audit.json').write_text(json.dumps({'changes':changes,'unknown':unknown,'counts':counts,'geometry_modified':False,'tolerance_mm':.015},ensure_ascii=False,indent=2),encoding='utf-8')
print('COUNTS',counts,'unknown',len(unknown),flush=True)
os._exit(0)
