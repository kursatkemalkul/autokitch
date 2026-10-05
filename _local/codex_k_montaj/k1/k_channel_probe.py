from pathlib import Path
import sys,pickle,json,numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'_local/claude_son_yerel/gece2/cekmece'))
import yol_denetim_v2 as Y
P=pickle.load((HERE/'k_parca.pkl').open('rb'))['P'];SAC={};tr=lambda a:a;bk=lambda a:a
exec((HERE/'_altyapi.py').read_text(encoding='utf-8'))
r=[]
for a in ['elk_zincir_kanal_0','elk_zincir_kanal_2']:
 # All final rigid fixtures: no omitted structural obstacle and no exception.
 fixtures=[b for b in P if b!=a and P[b]['tur'] not in ('kaynak','kablo','silikon')]
 for axis in range(3):
  for sign in (-1,1):
   d=np.zeros(3);d[axis]=sign*35
   errors=serbest([a],d,fixtures)
   r.append({'part':a,'offset_mm':d.tolist(),'collisions':errors});print(a,d.tolist(),errors[:12],flush=True)
(HERE/'channel_probe.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
