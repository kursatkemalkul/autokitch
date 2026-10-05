"""Native source-sheet morph adapter for the existing v6 manufacturing/player pipeline.
Keeps current model vertices/triangles; only maps source encoded bend coordinates.
No new player or geometry simplification. Mapping failures remain release blockers.
"""
from pathlib import Path
import json,numpy as np
from scipy.spatial import cKDTree
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
SRC=ROOT/'arastirma/_uretec/codex/k_montaj/bend_paths.py'
ns={'__file__':str(SRC)};exec(compile(SRC.read_text(encoding='utf-8').split('rows=[]')[0],str(SRC),'exec'),ns)
_decode=ns['decode']

class SourceSac:
 def __init__(self,record,current_vertices,indices,flat):
  self.record=record;self.current=np.asarray(current_vertices);self.indices=indices;self.t=record['t']
  by={b['number']:b for b in record['bends']};self.bukum=[{'no':i+1,'source_no':n,'aci':abs(float(np.degrees(by[n]['angle']))),'ad':'Kaynak büküm '+str(n)} for i,n in enumerate(record['order'])]
  self.levha={'boy':flat['levha']['boy'],'en':flat['levha']['en']} if 'levha' in flat else self._flat_size()
 def _flat_size(self):
  v=_decode(self.record,0.);span=np.ptp(v,axis=0);axes=np.argsort(span)[-2:];return {'boy':float(span[axes[1]]),'en':float(span[axes[0]])}
 def yerel(self,states):
  # Existing v6 calls bends consecutively. The native decoder already uses that same verified order.
  progress=sum(states.get(b['no'],0.) for b in self.bukum)/max(1,len(self.bukum))
  return _decode(self.record,progress)
 def dunya(self,local):
  m=np.asarray(self.record['root']);world=local@m[:3,:3].T+m[:3,3]+np.asarray(self.record['source_offset'])
  return world[self.indices]

 def frames(self):
  result=[];states={b['no']:0. for b in self.bukum};result.append(self.dunya(self.yerel(states))-self.current)
  for b in self.bukum:
   for f in np.linspace(0,1,7)[1:]:
    states[b['no']]=float(f);result.append(self.dunya(self.yerel(states))-self.current)
  return result

def load(P):
 data=json.loads((ROOT/'_local/codex_k_montaj/source_bending_updated.json').read_text(encoding='utf-8'));inventory=json.loads((ROOT/'_local/codex_k_montaj/source_cad_inventory.json').read_text(encoding='utf-8'))
 flats={s['name']:s['flat'] for s in inventory['sheets']};SAC={};audit=[]
 aliases={'onyuz_kapak_K':['k_govde_on_seffaf_0','k_govde_on_seffaf_2','k_govde_on_seffaf_3'],'onyuz_kapak_K_ic_tava':['k_govde_on_seffaf_1']}
 for rec in data['sheets']:
  for a in aliases.get(rec['name'],[rec['name']]):
   if a not in P:continue
   v=np.asarray(P[a]['V']);distance,idx=cKDTree(np.asarray(rec['vertices'])).query(v)
   row={'part':a,'source_sheet':rec['name'],'maximum_mapping_distance_mm':float(distance.max()),'passed':float(distance.max())<=.01}
   if not row['passed']:audit.append(row);continue
   obj=SourceSac(rec,v,idx,flats.get(rec['name'],{}));end=obj.dunya(obj.yerel({b['no']:1. for b in obj.bukum}));row['endpoint_error_mm']=float(np.linalg.norm(end-v,axis=1).max());row['passed'] &= row['endpoint_error_mm']<=.01
   if row['passed']:SAC[a]=obj
   audit.append(row)
 (HERE/'native_sheet_mapping_audit.json').write_text(json.dumps({'checks':audit,'source_mapping_passed':all(r['passed'] for r in audit),'production_release':False,'tool_path_checked':False},ensure_ascii=False,indent=2),encoding='utf-8')
 return SAC,audit
if __name__=='__main__':
 import pickle
 P=pickle.load((HERE/'k_parca.pkl').open('rb'))['P'];SAC,audit=load(P);print('NATIVE_SHEETS',len(SAC),'failed',[r for r in audit if not r['passed']]);print('bends',sum(len(s.bukum) for s in SAC.values()))
