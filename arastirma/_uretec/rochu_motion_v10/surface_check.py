from finger_bend import deform
"""Confirm surface crossings using native triangles, without convex envelopes."""
from audit import *
from rtree import index
def crosses(a,b):
 if np.any(a.min((0,1))>b.max((0,1))) or np.any(b.min((0,1))>a.max((0,1))):return False
 # Exact broad-phase pruning: a triangle outside the other mesh's bounds
 # cannot cross it. Avoid thousands of empty spatial-index queries per pose.
 alo,ahi=a.min((0,1)),a.max((0,1));blo,bhi=b.min((0,1)),b.max((0,1))
 a=a[np.all(a.max(1)>=blo-1e-8,axis=1)&np.all(a.min(1)<=bhi+1e-8,axis=1)]
 b=b[np.all(b.max(1)>=alo-1e-8,axis=1)&np.all(b.min(1)<=ahi+1e-8,axis=1)]
 if not len(a) or not len(b):return False
 prop=index.Property();prop.dimension=3
 mins=b.min(1);maxs=b.max(1);tree=index.Index(((i,tuple(np.r_[x,y]),None)for i,(x,y)in enumerate(zip(mins,maxs))),properties=prop)
 for tri in a:
  ids=list(tree.intersection(tuple(np.r_[tri.min(0),tri.max(0)])))
  if not ids:continue
  bt=b[ids];at=np.broadcast_to(tri,bt.shape);ea=np.roll(at,-1,axis=1)-at;eb=np.roll(bt,-1,axis=1)-bt;na=np.cross(ea[:,0],ea[:,1]);nb=np.cross(eb[:,0],eb[:,1])
  axes=np.concatenate([na[:,None,:],nb[:,None,:],np.cross(ea[:,:,None,:],eb[:,None,:,:]).reshape(-1,9,3),np.cross(na[:,None,:],ea),np.cross(nb[:,None,:],eb)],axis=1)
  mag=np.linalg.norm(axes,axis=2);axes/=np.maximum(mag,1e-24)[:,:,None]
  pa=np.einsum('nvi,nai->nav',at,axes);pb=np.einsum('nvi,nai->nav',bt,axes);sep=(pa.max(2)<pb.min(2)-1e-8)|(pb.max(2)<pa.min(2)-1e-8)
  if np.any(~sep.any(1)):return True
 return False
if __name__=='__main__':
 m=Model();poses=json.loads((OUT/'poses.json').read_text());report=json.loads((OUT/'audit.json').read_text());head=trimesh.load(io.BytesIO(gzip.decompress((OUT/'fixed_head.glb.gz').read_bytes())),file_type='glb');results={}
 for key,p in poses.items():
  ht=[];w=np.array(p['worlds']['UR10E_body_06'])
  for n in head.graph.nodes_geometry:
   local,g=head.graph[n];t=head.geometry[g];v=t.vertices.copy()
   if n.startswith('OEM_DAC_'):
    v=deform(v,p['tip_shift_mm'])
   x=w@local;v=v@x[:3,:3].T+x[:3,3];ht.append((n,v[t.faces]))
  for s in m.shapes:
   if any(s['name'].startswith('UR10E_body_'+str(i).zfill(2)+'_mesh')for i in [4,5,6]):ht.append((s['name'],shape_at(m,s,p)[s['faces']]))
  wanted={x['part']for x in report['poses'][key]['local_environment_hits']}
  if key.startswith('Dough'):
   if p['mode']=='pick':wanted|={s['name']for s in m.shapes if s['name'].startswith('CEK_K1') and '__CEKMECE' in s['name'] and '__CEKMECE_ARA' not in s['name']}
   elif p['valid']:wanted|={s['name']for s in m.shapes if 'DONER__TABLA' in s['name'] or 'ACICI' in s['name']}
  hits=[]
  for s in m.shapes:
   if s['name']not in wanted:continue
   v=s['world'].copy()
   if p['mode']=='pick' and s['name'].startswith('CEK_') and '__CEKMECE' in s['name'] and '__CEKMECE_ARA' not in s['name']:v[:,2]+=p['drawer_open_m']
   bt=v[s['faces']]
   for n,at in ht:
    if crosses(at,bt):hits.append(dict(native_part=s['name'],tool_or_wrist_part=n));break
  results[key]=hits;report['poses'][key]['confirmed_native_surface_hits']=hits;print(key,json.dumps(hits),flush=True)
 report['native_surface_confirmation']='Triangle separating-axis tests including coplanar axes, 0.00001mm tolerance. Confirms crossings; does not prove force, clearance margin or continuous trajectory.'
 (OUT/'audit.json').write_text(json.dumps(report,indent=2));(OUT/'surface_checks.json').write_text(json.dumps(results,indent=2))
