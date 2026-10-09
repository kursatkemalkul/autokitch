from parallel_probe import *
model,head=setup();r=75/2**.5
source=json.loads((DEST/'parallel-wide-contact.json').read_text())['52']
def product_probe(item):
 p=Probe(model,head,item)
 if item=='Dessert':
  p.vertices*=np.array([.065/np.ptp(p.vertices[:,0]),1,.0655/np.ptp(p.vertices[:,2])]);p.eq=np.unique(np.round(ConvexHull(p.vertices).equations,9),axis=0)
 return p
def first_contacts(p,depth):
 rows=[]
 for name,v,w0 in p.parts:
  w=w0.copy();w[:2,3]*=r/50;w[:3,:3]=Rotation.from_euler('z',90 if w[1,3]>0 else -90,degrees=True).as_matrix();rot=p.R@w[:3,:3];off=p.base+p.R@w[:3,3]+p.R[:,2]*depth*.001
  def measure(sh):
   world=deform(v,sh)@rot.T+off;planes=world@p.eq[:,:3].T+p.eq[:,3];d=-planes.max(1)*1000;i=d.argmax();j=planes[i].argmax();return d,i,j,planes[i],world[i]
  low,high=-11.,5.
  for _ in range(18):
   mid=(low+high)/2
   if measure(mid)[0].max()>0:high=mid
   else:low=mid
  d,i,j,planes,pt=measure(high);side=np.abs(p.eq[:,:3]@p.R[:,2])<.55
  rows.append({'name':name,'shift_mm':high,'surface_mm':float(d[i]),'tip_contact':bool(v[i,2]>.032),'side_contact':bool(side[j]),'inside_entry_mm':float(-planes[~side].max()*1000),'fixed_mm':float(d[v[:,2]<=START].max()),'point_world_relative':pt.tolist()})
 return rows
p=product_probe('Dessert');lo,hi=-35.,5.
for _ in range(16):
 mid=(lo+hi)/2;a=p.measure(r,mid,-11,True)
 if max(t['open_mm'] for t in a['parts'])>-.2:hi=mid
 else:lo=mid
source['Dessert']={'radius_mm':r,'depth_mm':lo,'opening':-11,'parts':first_contacts(p,lo)}
for k in ['Cola','Box']:
 source[k]['radius_mm']=r
 p=product_probe(k);source[k]['parts']=first_contacts(p,source[k]['depth_mm'])
p=product_probe('Dough')
def dough_loss(x):
 a=p.measure(r,*x);v=a['parts'];fixed=max(t['fixed_mm'] for t in v)
 return max(abs(t['tip_mm']-.5) for t in v)+.15*max(0,fixed)+2*max(0,fixed-5)
sol=differential_evolution(dough_loss,[(-12,12),(-11,5)],seed=62,popsize=10,maxiter=90,polish=True,tol=.003)
a=p.measure(r,*sol.x,True);a['opening']=-11
source['Dough']=a
report={'radius_mm':r,'mount_axes_mm':2*r,'adjacent_axis_spacing_mm':2*r/2**.5,'mounting':'Four fixed roots on the same star; upper pair localX points +Y, lower pair localX points -Y. Mounted once; no per-product root/angle change.','dessert_dimensions_mm':[65,65.5,60],'products':source,'status':'Hard-product surface contact candidates, not a load-bearing physical certification. Dough intrusion represents required deformation, not simulated material response.','assumptions':'Each soft tip may conform to first contact separately; this is geometric compliance, not independent actuators or a validated common-pressure law.'}
(DEST/'selected.json').write_text(json.dumps(report,indent=2))
for k,v in source.items():print(k,json.dumps(v),flush=True)
