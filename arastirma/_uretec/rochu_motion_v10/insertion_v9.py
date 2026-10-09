"""Measure deeper entry without scaling CAD or moving the four fixed roots."""
from v2 import *
from finger_bend import deform,START,bend_angle
from scipy.spatial import ConvexHull

class GraspProbe:
 def __init__(self,r,item):
  self.r=r;self.item=item;ps=r.products[item]
  self.eq=np.unique(np.round(ConvexHull(ps['world']-ps['bounds'].mean(0)).equations,10),axis=0)
  self.parts=[]
  for name in r.head.graph.nodes_geometry:
   w,g=r.head.graph[name];m=r.head.geometry[g]
   # Long native planar faces need interior samples as well as vertices.
   v=np.vstack([m.vertices,m.triangles_center])
   self.parts.append((name,v,w))

 def measure(self,R,contact,centre,shift,tip_only=False):
  root=ident(np.array(contact)-np.array(R)@np.array([0,0,TIP]));root[:3,:3]=R
  out=[]
  for name,v,local in self.parts:
   if tip_only:
    if not name.startswith('OEM_DAC_'):continue
    v=v[v[:,2]>.032]
   vv=deform(v,shift) if name.startswith('OEM_DAC_') else v
   w=root@local;world=vv@w[:3,:3].T+w[:3,3]-centre
   d=-(world@self.eq[:,:3].T+self.eq[:,3]).max(1)*1000
   fixed=(v[:,2]<=START) if name.startswith('OEM_DAC_') else np.ones(len(v),bool)
   out.append({'name':name,'penetration_mm':float(d.max()),'fixed_penetration_mm':float(d[fixed].max()) if fixed.any() else None})
  return out

 def evaluate(self,R,contact,centre):
  opened=self.measure(R,contact,centre,-11)
  lo,hi=-11.,5.
  if max(x['penetration_mm'] for x in opened)>.05:
   chosen=-11.
  else:
   for _ in range(25):
    mid=(lo+hi)/2;d=self.measure(R,contact,centre,mid)
    if max(x['penetration_mm'] for x in d)>0:hi=mid
    else:lo=mid
   chosen=hi
  closed=self.measure(R,contact,centre,chosen)
  fingers=[x for x in closed if x['name'].startswith('OEM_DAC_')]
  return {'open_max_penetration_mm':max(x['penetration_mm'] for x in opened),
   'fixed_max_penetration_mm':max(x['fixed_penetration_mm'] for x in closed if x['fixed_penetration_mm'] is not None),
   'contact_shift_mm':chosen,'tip_angle_deg':float(np.rad2deg(bend_angle(chosen))),
   'fingers':fingers,'four_contact_candidates':all(-.20<x['penetration_mm']<.05 for x in fingers),
   'model':'tip-only arc; geometric samples, no pressure/force validation'}

if __name__=='__main__':
 r=Review();rows={}
 for item in ['Box','Cola','Dessert','Dough']:
  seq=json.loads((OUT/(item.lower()+'_v8_candidate.json')).read_text());p=next(f for f in seq['frames'] if f['held'])['pose']
  R=np.array(p['tool_orientation']);c=np.array(p['product']);contact=np.array(p['contact']);probe=GraspProbe(r,item);out=[]
  for depth in [0,2,4,6,8,10,12,14,16,18,20]:
   cp=contact+R[:,2]*depth*.001;result=probe.evaluate(R,cp,c);out.append(dict(extra_depth_mm=depth,contact=cp.tolist(),**result))
   print(item,depth,'open',round(result['open_max_penetration_mm'],2),'fixed',round(result['fixed_max_penetration_mm'],2),'contacts',result['four_contact_candidates'],'shift',round(result['contact_shift_mm'],3),flush=True)
  rows[item]=out
 (OUT/'insertion_v9_scan.json').write_text(json.dumps(rows,indent=2))
