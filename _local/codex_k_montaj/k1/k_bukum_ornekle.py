"""Current 67-sheet adaptive native bend sampling; no collision/release claim.

Vectorized evaluation is checked against the existing decoder. This diagnostic
does not alter the shared player, model, station plan or morph timeline.
"""
from pathlib import Path
import json,hashlib,time
import numpy as np
from k_sac_kaynak import _decode,ns
rotation=ns['rotation'];H=Path(__file__).resolve().parent
path=H/'current_sheet_bending.json';D=json.loads(path.read_text(encoding='utf-8'))
Z=np.array([0.,0.,1.])
class Decoder:
 def __init__(self,s):
  self.s=s;self.panels={};self.curves={};self.by={b['number']:b for b in s['bends']}
  for i,r in enumerate(s['encoded_vertices']):
   container=self.panels if 'panel' in r else self.curves
   key=r.get('panel',r.get('bend'));container.setdefault(key,[]).append((i,r['point']))
  for container in (self.panels,self.curves):
   for key,items in container.items():container[key]=(np.array([i for i,p in items]),np.array([p for i,p in items]))
 def at(self,phase):
  s=self.s;states={n:np.clip(phase*len(s['order'])-i,0,1) for i,n in enumerate(s['order'])};poses={0:np.eye(4)}
  for b in s['bends']:
   f=states[b['number']]
   if f==0:M=np.array(b['flat_child'])
   else:
    theta=b['angle']*f;R=b['BA']/theta-b['K']*s['t'];rot=rotation(b['axis'],theta);c=s['t']+R if b['direction']>0 else -R
    delta=np.cross(b['axis'],Z)*np.sin(theta)-Z*2*np.sin(theta/2)**2
    M=np.eye(4);M[:3,:3]=np.column_stack([rot@b['out'],b['edge'],rot@Z]);M[:3,3]=np.array(b['p0'])-c*delta
   poses[b['child']]=poses[b['parent']]@M
  result=np.empty((len(s['encoded_vertices']),3))
  for panel,(idx,p) in self.panels.items():
   M=poses[panel];result[idx]=p@M[:3,:3].T+M[:3,3]
  for number,(idx,p) in self.curves.items():
   b=self.by[number];f=states[number];v=np.array(b['p0'])+p[:,1,None]*np.array(b['edge'])+p[:,2,None]*Z
   if f==0:v+=p[:,0,None]*np.array(b['out'])
   else:
    theta=b['angle']*f;R=b['BA']/theta-b['K']*s['t'];r=R+s['t']-p[:,2] if b['direction']>0 else R+p[:,2]
    e=Z*(-1 if b['direction']>0 else 1);a=theta*p[:,0]/b['BA']
    v+=r[:,None]*(np.sin(a)[:,None]*np.cross(b['axis'],e)-2*np.sin(a/2)[:,None]**2*e)
   M=poses[b['parent']];result[idx]=v@M[:3,:3].T+M[:3,3]
  return result

def main():
 rows=[];start=time.time()
 for s in D['sheets']:
  decoder=Decoder(s);n=len(s['order']);cache={};times={0.,1.};worst=0.
  for phase in (0.,.137,.5,.823,1.):
   err=float(np.linalg.norm(decoder.at(phase)-_decode(s,phase),axis=1).max());worst=max(worst,err)
  assert worst<1e-8,(s['name'],worst)
  def at(t):
   if t not in cache:cache[t]=decoder.at(t)
   return cache[t]
  def sample(a,b,depth=0):
   mid=(a+b)/2;p,q,r=at(a),at(mid),at(b)
   distance=max(float(np.linalg.norm(q-p,axis=1).max()),float(np.linalg.norm(r-q,axis=1).max()))
   chord=float(np.linalg.norm(q-(p+r)/2,axis=1).max())
   if distance>2 or chord>.01:
    assert depth<20,(s['name'],'nonconvergence');sample(a,mid,depth+1);sample(mid,b,depth+1)
   else:times.update((a,mid,b))
  for i in range(n):sample(i/n,(i+1)/n)
  phases=sorted(times);maximum=max((float(np.linalg.norm(at(b)-at(a),axis=1).max()) for a,b in zip(phases,phases[1:])),default=0.)
  root=np.array(s['root']);world=at(1)@root[:3,:3].T+root[:3,3]+s['source_offset'];endpoint=float(np.linalg.norm(world-s['vertices'],axis=1).max())
  rows.append({'sheet':s['name'],'phase_samples':phases,'sample_count':len(phases),'maximum_vertex_step_mm':maximum,'decoder_reference_error_mm':worst,'endpoint_error_mm':endpoint,'passed_sampling_only':maximum<=2.000001 and endpoint<=.01})
  print('CURRENT_BEND_SAMPLES',s['name'],len(phases),'max_step',round(maximum,5),flush=True)
 report={'source_encoding_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'physical_sheets':len(rows),'checks':rows,'maximum_step_mm':2.,'adaptive_midpoint_chord_tolerance_mm':.01,'passed_sampling_only':all(r['passed_sampling_only'] for r in rows),'morph_timeline_updated':False,'self_collision_checked':False,'tool_access_checked':False,'production_release':False,'elapsed_seconds':time.time()-start}
 (H/'current_bend_samples.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print('CURRENT_BEND_COMPLETE',len(rows),report['passed_sampling_only'],flush=True)
if __name__=='__main__':main()
