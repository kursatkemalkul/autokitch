from pathlib import Path
import pickle,sys,numpy as np,json,time
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'_local/claude_son_yerel/gece2/cekmece'))
import yol_denetim_v2 as Y
P=pickle.load((HERE/'k_parca.pkl').open('rb'))['P'];SAC={};tr=lambda a:a;bk=lambda a:a
exec((HERE/'_altyapi.py').read_text(encoding='utf-8'))
CAT={p['name']:p for p in json.loads((ROOT/'_local/codex_k_montaj/legacy_catalog.json').read_text(encoding='utf-8'))}
results=[]
for stud,c in CAT.items():
 meta=c.get('meta') or {}
 if stud not in P or meta.get('pem_tip')!='FHP' or not stud.endswith('_bag_saplama'):continue
 nut=stud[:-len('_saplama')]+'_somun'
 if nut not in P:continue
 HARIC_PLAN.add((stud,nut));pts=P[stud]['V'];extent=HI[stud]-LO[stud];axis=int(np.argmin(np.abs(extent-meta['boy'])));perp=[q for q in range(3) if q!=axis];centre=(LO[stud]+HI[stud])/2
 rd=np.linalg.norm(pts[:,perp]-centre[perp],axis=1);e=np.zeros(3);e[axis]=-1 if rd[pts[:,axis]>=HI[stud][axis]-.02].max()>rd[pts[:,axis]<=LO[stud][axis]+.02].max()+1e-4 else 1
 lo=np.minimum(LO[nut],LO[nut]+e*50);hi=np.maximum(HI[nut],HI[nut]+e*50)
 fixture=[a for a in P if a!=nut and np.all(HI[a]>=lo-.1) and np.all(LO[a]<=hi+.1)]
 conflicts=serbest([nut],e*50,fixture)
 results.append({'nut':nut,'stud':stud,'axis':e.tolist(),'remaining_collisions':conflicts,'thread_mate_exemption':stud+' / '+nut+' FHP + ISO10511 nominal thread'})
 print(nut,'PASS' if not conflicts else conflicts,flush=True)
(HERE/'nut_axes_probe.json').write_text(json.dumps({'results':results,'passed':sum(not r['remaining_collisions'] for r in results),'total':len(results),'whole_sequence_release':False},ensure_ascii=False,indent=2),encoding='utf-8')
