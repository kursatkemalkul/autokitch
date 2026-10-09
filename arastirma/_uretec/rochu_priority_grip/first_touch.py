from inward_probe import *
model,head=setup();data=json.loads((DEST/'strict-search.json').read_text());out={}
for item,rows in data.items():
 p=Probe(model,head,item);out[item]=[]
 for row in rows:
  lo=-11.;hi=row['shift_mm'];r=row['radius_mm'];depth=row['depth_mm']
  for _ in range(15):
   mid=(lo+hi)/2;a=p.measure(r,depth,mid,True)
   if max(t['whole_closed_mm'] for t in a['parts'])>0:hi=mid
   else:lo=mid
  a=p.measure(r,depth,hi,True);a['opening']=-11;out[item].append(a)
  print(item,r,'shift',a['shift_mm'],'entry',max(t['open_mm'] for t in a['parts']),'whole',max(t['whole_closed_mm'] for t in a['parts']),'tips',[t['tip_mm'] for t in a['parts']],flush=True)
  (DEST/'first-touch.json').write_text(json.dumps(out,indent=2))
