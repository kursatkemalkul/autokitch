from parallel_probe import *
model,head=setup();out={}
for r in [40,42,44,46]:
 out[str(r)]={}
 for item in ['Box','Cola']:
  p=Probe(model,head,item)
  lo,hi=-35.,5.
  for _ in range(16):
   mid=(lo+hi)/2;a=p.measure(r,mid,-11,True)
   if max(t['open_mm'] for t in a['parts'])>-.2:hi=mid
   else:lo=mid
  depth=lo;parts=[]
  for index,(name,v,w0) in enumerate(p.parts):
   w=w0.copy();w[:2,3]*=r/50;w[:3,:3]=Rotation.from_euler('z',90 if w[1,3]>0 else -90,degrees=True).as_matrix();rot=p.R@w[:3,:3];off=p.base+p.R@w[:3,3]+p.R[:,2]*depth*.001
   def measure(shift):
    vv=deform(v,shift);world=vv@rot.T+off;planes=world@p.eq[:,:3].T+p.eq[:,3];d=-planes.max(1)*1000;i=d.argmax();j=planes[i].argmax()
    return float(d[i]),i,j,world[i],planes[i]
   low,high=-11.,5.
   if measure(high)[0]>=0:
    for _ in range(16):
     mid=(low+high)/2
     if measure(mid)[0]>0:high=mid
     else:low=mid
   val,i,j,pt,planes=measure(high);side=np.abs(p.eq[:,:3]@p.R[:,2])<.55
   depth_inside=float(-planes[~side].max()*1000)
   parts.append({'name':name,'shift_mm':high,'surface_mm':val,'tip_contact':bool(v[i,2]>.032),'side_contact':bool(side[j]),'inside_entry_mm':depth_inside,'local_z_mm':float(v[i,2]*1000),'point_world_relative':pt.tolist()})
  out[str(r)][item]={'radius_mm':r,'depth_mm':depth,'opening':-11,'parts':parts}
  print(r,item,'depth',round(depth,3),[(round(t['shift_mm'],3),round(t['surface_mm'],3),t['tip_contact'],t['side_contact'],round(t['inside_entry_mm'],3)) for t in parts],flush=True)
  (DEST/'parallel-contact.json').write_text(json.dumps(out,indent=2))
