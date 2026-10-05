from pathlib import Path
import sys,pickle,json,numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'_local/claude_son_yerel/gece2/cekmece'))
import yol_denetim_v2 as Y
P=pickle.load((HERE/'k_parca.pkl').open('rb'))['P'];SAC={};tr=lambda a:a;bk=lambda a:a
exec((HERE/'_altyapi.py').read_text(encoding='utf-8'))
r=[]
for a in P:
 if not (a.startswith('onyuz_kapak_K_mentese_') and a.endswith('_sabit') or a.startswith('onyuz_kapak_K_basac_')):continue
 host='kose_dikmesi_20_42' if '_mentese_' in a else 'kose_dikmesi_380_42'
 for ofs in ([0,0,100],[0,0,-100],[50,0,0],[-50,0,0]):
  errors=serbest([a],ofs,[host])
  r.append({'part':a,'host':host,'offset_mm':ofs,'collisions':errors})
  print(a,ofs,errors,flush=True)
(HERE/'pocket_probe.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
