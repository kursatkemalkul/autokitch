from radial_probe import *
model,head=setup();report=json.loads((DEST/'selected.json').read_text());r=report['half_spacing_mm'];checks={}
for item,row in report['products'].items():
 p=Probe(model,head,item)
 if item=='Dessert':
  p.vertices*=np.array([.065/np.ptp(p.vertices[:,0]),1,.0655/np.ptp(p.vertices[:,2])]);p.eq=np.unique(np.round(ConvexHull(p.vertices).equations,9),axis=0)
 changes={x['name']:x for x in row['parts']};stats=[];boxes=[]
 for n,v,w0 in p.parts:
  w=mount(w0,r);rot=p.R@w[:3,:3];off=p.base+p.R@w[:3,3]+p.R[:,2]*row['depth_mm']*.001
  sh=changes[n].get('shift_mm',row.get('shift_mm'))
  def values(shift):
   world=deform(v,shift)@rot.T+off;pl=world@p.eq[:,:3].T+p.eq[:,3];d=-pl.max(1)*1000
   return world,pl,d
  if item=='Dough':
   side=np.abs(p.eq[:,:3]@p.R[:,2])<.55
   def belly_pen(shift):
    world,pl,d=values(shift);eligible=(v[:,2]>.032)&(np.abs(world[:,1]-p.belly)<.003)&side[pl.argmax(1)]
    return float(d[eligible].max()) if eligible.any() else -100
   low,high=-11.,5.
   for _ in range(18):
    mid=(low+high)/2
    if belly_pen(mid)>.7:high=mid
    else:low=mid
   sh=high;world,pl,d=values(sh);changes[n].update(shift_mm=sh,tip_mm=belly_pen(sh),whole_closed_mm=float(d.max()),fixed_mm=float(d[v[:,2]<=START].max()))
  closed=values(sh);movement=[]
  for t in np.linspace(0,1,25):movement.append(float(values(-11+(sh+11)*t)[2].max()))
  base_open=deform(v,-11)@rot.T+off
  entry=[]
  for retreat in np.linspace(.060,0,25):
   dd=-((base_open-p.R[:,2]*retreat)@p.eq[:,:3].T+p.eq[:,3]).max(1)*1000;entry.append(float(dd.max()))
  # AABB disjointness is sufficient to exclude finger/finger collision.
  vv=deform(v,sh)@w[:3,:3].T+w[:3,3];boxes.append((n,vv.min(0),vv.max(0)))
  stats.append({'name':n,'shift_mm':sh,'closed_penetration_mm':float(closed[2].max()),'entry_max_penetration_mm':max(entry),'closing_max_penetration_mm':max(movement),'fixed_penetration_mm':float(closed[2][v[:,2]<=START].max())})
 overlap=[]
 for i,(n,a,b) in enumerate(boxes):
  for nn,c,d in boxes[i+1:]:
   if np.all(np.minimum(b,d)-np.maximum(a,c)>0):overlap.append([n,nn])
 checks[item]={'parts':stats,'finger_aabb_overlap_candidates':overlap,'entry_samples':25,'closure_samples':25}
 checks[item]['passed_hard_geometry'] = item!='Dough' and all(x['entry_max_penetration_mm']<=.002 and x['closing_max_penetration_mm']<=.002 for x in stats) and all(x['tip_contact'] and x['side_contact'] and x['inside_entry_mm']>20 and abs(x['surface_mm'])<.01 for x in row['parts']) and not overlap
 assert all(abs(t['inward_axis_dot']-1)<1e-9 for t in row['parts'])
 print(item,'entry',max(x['entry_max_penetration_mm'] for x in stats),'closing',max(x['closing_max_penetration_mm'] for x in stats),'fixed',max(x['fixed_penetration_mm'] for x in stats),flush=True)
 (DEST/'selected.json').write_text(json.dumps(report,indent=2));(DEST/'verification.json').write_text(json.dumps(checks,indent=2))
