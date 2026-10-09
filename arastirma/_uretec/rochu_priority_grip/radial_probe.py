from model import *
from finger_bend import deform,START
import trimesh,gzip,io
from scipy.spatial import ConvexHull
from scipy.optimize import differential_evolution
DEST=ROOT/'otonom/hat/denemeler/rochu-priority-grip'
def setup():
 model=Model();head=trimesh.load(io.BytesIO(gzip.decompress((OUT/'fixed_head.glb.gz').read_bytes())),file_type='glb')
 return model,head
class Probe:
 def __init__(self,model,head,item,size=None):
  self.item=item;self.size=size
  self.s=next(s for s in model.shapes if s['name']==('ROBOT25_PRODUCT_Box' if item=='Box' else 'ROBOT25_'+item+'_stock_shape'))
  self.p=next(f['pose'] for f in json.loads((OUT/(item.lower()+'_v10_candidate.json')).read_text())['frames'] if f['held'])
  self.vertices=self.s['world']-self.s['bounds'].mean(0)
  if size:
   scale=np.array([size/np.ptp(self.vertices[:,0])/1000,1,size/np.ptp(self.vertices[:,2])/1000]);self.vertices=self.vertices*scale
  self.eq=np.unique(np.round(ConvexHull(self.vertices).equations,9),axis=0)
  self.R=np.array(self.p['tool_orientation']);self.base=np.array(self.p['contact'])-self.R[:,2]*.1097-np.array(self.p['product'])
  self.parts=[]
  for n in head.graph.nodes_geometry:
   if not n.startswith('OEM_DAC_'):continue
   w,g=head.graph[n];m=head.geometry[g];v=np.unique(np.round(np.vstack([m.vertices,m.triangles_center]),7),axis=0)
   self.parts.append((n,v,w))
  self.belly=json.loads((OUT/'dough_belly_v9.json').read_text())['relative_height_mm']/1000
 def measure(self,radius,depth,shift,full=False,opening=-11):
  rows=[]
  for n,v,w0 in self.parts:
   if not full:v=v[::max(1,len(v)//4000)]
   w=mount(w0,radius)
   rot=self.R@w[:3,:3];off=self.base+self.R@w[:3,3]+self.R[:,2]*depth*.001
   def planes(vv):return (vv@rot.T+off)@self.eq[:,:3].T+self.eq[:,3]
   opened=-planes(deform(v,opening)).max(1)*1000
   bent=deform(v,shift);d=-planes(bent).max(1)*1000
   tv=bent[v[:,2]>.032];world=tv@rot.T+off;pp=world@self.eq[:,:3].T+self.eq[:,3]
   side=np.abs(self.eq[:,:3]@self.R[:,2])<.55;eligible=side[pp.argmax(1)]
   if (~side).any():eligible &= pp[:,~side].max(1)<-.020
   if self.item=='Dough':eligible &= np.abs(world[:,1]-self.belly)<.003
   td=-pp.max(1)*1000
   rows.append({'name':n,'open_mm':float(opened.max()),'fixed_mm':float(opened[v[:,2]<=START].max()),'tip_mm':float(td[eligible].max()) if eligible.any() else -100.,'whole_closed_mm':float(d.max())})
  return {'half_spacing_mm':list(radius),'depth_mm':float(depth),'shift_mm':float(shift),'parts':rows}
 @staticmethod
 def score(a):
  return max(0,max(x['open_mm'] for x in a['parts'])+.5,max(x['fixed_mm'] for x in a['parts']),max(abs(x['tip_mm']) for x in a['parts'])-.5)
 def solve(self,r):
  f=lambda a:self.score(self.measure(r,*a))
  x=differential_evolution(f,[(-30,20),(-11,0)],seed=19,popsize=6,maxiter=45,polish=False,tol=.01)
  a=self.measure(r,*x.x,full=True);a['residual_mm']=self.score(a);return a


def mount(w0,xy):
 w=w0.copy();w[:2,3]=np.sign(w0[:2,3])*np.array(xy)*.001
 w[:3,:3]=Rotation.from_euler('z',np.arctan2(w[1,3],w[0,3])).as_matrix()
 return w
