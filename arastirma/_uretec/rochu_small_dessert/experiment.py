from model import *
from finger_bend import deform,START
import trimesh,gzip,io
from scipy.spatial import ConvexHull
from scipy.optimize import differential_evolution
DEST=ROOT/'otonom/hat/denemeler/rochu-small-dessert'
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
 def measure(self,radius,depth,shift,full=False):
  rows=[]
  for n,v,w0 in self.parts:
   if not full:v=v[::max(1,len(v)//1200)]
   w=w0.copy();w[:2,3]*=radius/50
   rot=self.R@w[:3,:3];off=self.base+self.R@w[:3,3]+self.R[:,2]*depth*.001
   def planes(vv):return (vv@rot.T+off)@self.eq[:,:3].T+self.eq[:,3]
   opened=-planes(v).max(1)*1000
   bent=deform(v,shift);d=-planes(bent).max(1)*1000
   tv=bent[v[:,2]>.032];world=tv@rot.T+off;pp=world@self.eq[:,:3].T+self.eq[:,3]
   side=np.abs(self.eq[:,:3]@self.R[:,2])<.55;eligible=side[pp.argmax(1)]
   if (~side).any():eligible &= pp[:,~side].max(1)<-.001
   if self.item=='Dough':eligible &= np.abs(world[:,1]-self.belly)<.003
   td=-pp.max(1)*1000
   rows.append({'name':n,'open_mm':float(opened.max()),'fixed_mm':float(opened[v[:,2]<=START].max()),'tip_mm':float(td[eligible].max()) if eligible.any() else -100.,'whole_closed_mm':float(d.max())})
  return {'radius_mm':float(radius),'depth_mm':float(depth),'shift_mm':float(shift),'parts':rows}
 @staticmethod
 def score(a):
  return max(0,max(x['open_mm'] for x in a['parts'])+.5,max(x['fixed_mm'] for x in a['parts']),max(abs(x['tip_mm']) for x in a['parts'])-.5)
 def solve(self,r):
  f=lambda a:self.score(self.measure(r,*a))
  x=differential_evolution(f,[(-30,20),(-11,0)],seed=19,popsize=6,maxiter=45,polish=False,tol=.01)
  a=self.measure(r,*x.x,full=True);a['residual_mm']=self.score(a);return a

if __name__=='__main__':
 model,head=setup();results={}
 for item,size in [('Cola',None),('Box',None),('Dough',None),('Dessert',80),('Dessert',75),('Dessert',70),('Dessert',65)]:
  key=item+(str(size) if size else '');probe=Probe(model,head,item,size);results[key]=[]
  for radius in np.arange(30,45,2):results[key].append(probe.solve(radius))
  print(key,[(a['radius_mm'],round(a['residual_mm'],2)) for a in results[key]],flush=True)
  (DEST/'search.json').write_text(json.dumps(results,indent=2))
 choices=[]
 for size in [80,75,70,65]:
  for i,r in enumerate(np.arange(30,45,2)):
   rows={k:results[k if k!='Dessert' else 'Dessert'+str(size)][i] for k in ['Dough','Cola','Dessert','Box']}
   choices.append({'size_mm':size,'radius_mm':float(r),'residual_mm':max(v['residual_mm'] for v in rows.values()),'rows':rows})
 best=min(x['residual_mm'] for x in choices)
 # Prefer the largest dessert among candidates within 0.25 mm of the best residual.
 chosen=min((x for x in choices if x['residual_mm']<=best+.25),key=lambda x:(-x['size_mm'],x['residual_mm']))
 chosen.update(status='comparison candidate, not a successful four-product grasp',mount_axes_mm=2*chosen['radius_mm'],constraints='Fixed V10 finger orientations. Same root radius for all four. Only dessert footprint reduced; height60mm, other products unscaled. OEM unchanged.',limits='Sampled convex exterior, illustrative bend, optimization can miss solutions; no load, neighbour, fixture or pressure validation.')
 (DEST/'selected.json').write_text(json.dumps(chosen,indent=2));print('CHOSEN',chosen['size_mm'],chosen['radius_mm'],chosen['residual_mm'],flush=True)
