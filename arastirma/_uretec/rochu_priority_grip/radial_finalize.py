from radial_probe import *
model,head=setup();candidate=json.loads((DEST/'radial-search.json').read_text());r=[25.,42.]
products={}
def make_probe(item):
 p=Probe(model,head,item)
 if item=='Dessert':
  p.vertices*=np.array([.065/np.ptp(p.vertices[:,0]),1,.0655/np.ptp(p.vertices[:,2])]);p.eq=np.unique(np.round(ConvexHull(p.vertices).equations,9),axis=0)
 return p
def contacts(p,depth):
 rows=[]
 for name,v,w0 in p.parts:
  w=mount(w0,r);rot=p.R@w[:3,:3];off=p.base+p.R@w[:3,3]+p.R[:,2]*depth*.001
  def measure(sh):
   world=deform(v,sh)@rot.T+off;planes=world@p.eq[:,:3].T+p.eq[:,3];d=-planes.max(1)*1000
   if p.item=='Dough':
    mask=(v[:,2]>.032)&(np.abs(world[:,1]-p.belly)<.003);score=float(d[mask].max()) if mask.any() else -100
   else:score=float(d.max())
   return score,d,planes,world
  low,high=-11.,5.;target=.7 if p.item=='Dough' else 0
  for _ in range(19):
   mid=(low+high)/2
   if measure(mid)[0]>target:high=mid
   else:low=mid
  score,d,planes,world=measure(high);i=d.argmax()
  if p.item=='Dough':
   mask=(v[:,2]>.032)&(np.abs(world[:,1]-p.belly)<.003)
   if mask.any():i=np.where(mask)[0][np.argmax(d[mask])]
  side=np.abs(p.eq[:,:3]@p.R[:,2])<.55;j=planes[i].argmax()
  rows.append({'name':name,'shift_mm':high,'surface_mm':float(d[i]),'tip_contact':bool(v[i,2]>.032),'side_contact':bool(side[j]),'inside_entry_mm':float(-planes[i,~side].max()*1000),'fixed_mm':float(d[v[:,2]<=START].max()),'whole_closed_mm':float(d.max()),'point_world_relative':world[i].tolist(),'inward_axis_dot':float(np.dot(-w[:2,0],-w[:2,3]/np.linalg.norm(w[:2,3])))})
 return rows
for item in ['Box','Cola','Dessert','Dough']:
 p=make_probe(item)
 if item in ['Box','Cola']:depth=candidate['products'][item]['depth_mm']
 elif item=='Dessert':depth=products['Cola']['depth_mm']
 else:
  def loss(x):
   a=p.measure(r,*x);v=a['parts'];return max(abs(t['tip_mm']-.7) for t in v)+4*max(0,max(t['whole_closed_mm'] for t in v)-2)+4*max(0,max(t['fixed_mm'] for t in v)-1)
  sol=differential_evolution(loss,[(-12,12),(-11,5)],seed=31,popsize=6,maxiter=60,tol=.01);depth=float(sol.x[0])
 products[item]={'depth_mm':depth,'opening':-11,'parts':contacts(p,depth)}
 print(item,json.dumps(products[item]),flush=True)
report={'half_spacing_mm':r,'mounting':'All four fixed local -X gripping faces point at tool-axis centre. No per-product mount rotation or spacing change.','dessert_dimensions_mm':[65,65.5,60],'products':products,'status':'Geometric candidate; pressure-force relation and actual soft compliance unvalidated.'}
(DEST/'selected.json').write_text(json.dumps(report,indent=2))
