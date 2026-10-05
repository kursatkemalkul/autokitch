"""Refine native bend morphs in a separate prototype using the existing player.
No timeline, rigid trajectory, base geometry, shared player or release changes.
"""
from pathlib import Path
import pickle,json,hashlib
import numpy as np
from k_sac_kaynak import load
from k_bukum_ornekle import Decoder
H=Path(__file__).resolve().parent;source=H/'plan_k_full.pkl'
D=pickle.load(source.open('rb'));samples=json.loads((H/'current_bend_samples.json').read_text(encoding='utf-8'))
assert samples['source_encoding_sha256']==hashlib.sha256((H/'current_sheet_bending.json').read_bytes()).hexdigest()
assert samples['passed_sampling_only']
SAC,mapping=load(D['P']);assert all(r['passed'] for r in mapping)
by={r['sheet']:r for r in samples['checks']};rows=[];source_har=pickle.dumps(D['HAR']);source_rot=pickle.dumps(D['ROT'])
for a,m in D['MF'].items():
 if 'seg' not in m or a not in SAC:continue
 s=SAC[a];record=s.record;n=len(record['order']);assert len(m['seg'])==n
 decoder=Decoder(record);phases=by[record['name']]['phase_samples'];frames=[];segments=[];maximum=0.;endpoint=0.
 root=np.array(record['root']);offset=np.array(record['source_offset'])
 def frame(phase):
  local=decoder.at(phase);return (local@root[:3,:3].T+root[:3,3]+offset)[s.indices]-s.current
 for i,old in enumerate(m['seg']):
  inside=[p for p in phases if i/n-1e-12<=p<=(i+1)/n+1e-12]
  minimum=min(np.diff(inside));count=int(round(1/(minimum*n)))
  assert count>=1
  begin=len(frames)-1 if frames else 0
  for j in range(count+1):
   f=frame((i+j/count)/n)
   if frames and j==0:assert np.max(abs(f-frames[-1]))<1e-8;continue
   if frames:maximum=max(maximum,float(np.linalg.norm(f-frames[-1],axis=1).max()))
   frames.append(f)
  segments.append(old[:2]+[begin,len(frames)-1])
 endpoint=float(np.linalg.norm(frames[-1],axis=1).max())
 assert maximum<=2.000001 and endpoint<=.01,(a,maximum,endpoint)
 D['FRAMES'][a]=frames;m['seg']=segments
 rows.append({'part':a,'physical_sheet':record['name'],'morph_frames':len(frames),'maximum_vertex_step_mm':maximum,'endpoint_error_mm':endpoint,'native_bend_count':n})
 print('DENSE_BEND',a,len(frames),round(maximum,5),flush=True)
assert pickle.dumps(D['HAR'])==source_har and pickle.dumps(D['ROT'])==source_rot
D['prototype_dense_native_bends']=True;D['production_release']=False
out=H/'plan_k_dense.pkl';pickle.dump(D,out.open('wb'))
report={'source_plan_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'dense_plan_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'checks':rows,'rigid_paths_unchanged':True,'timeline_unchanged':True,'base_geometry_unchanged':True,'shared_player_changed':False,'bend_morph_sampling_passed':True,'self_collision_checked':False,'fixture_checked':False,'connection_checked':False,'production_release':False}
(H/'dense_bend_morph_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('DENSE_MORPH_COMPLETE',len(rows),'parts',out.stat().st_size,'bytes',flush=True)
