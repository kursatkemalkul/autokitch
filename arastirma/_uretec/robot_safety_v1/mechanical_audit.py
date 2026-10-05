"""Exact solid intersection of all new CAD parts. No collision exemption by name."""
from pathlib import Path
import json
import build
build.qr();build.gate()
parts=build.P;bounds=[p['sh'].BoundingBox() for p in parts];hits=[];contacts=[]
for i,a in enumerate(parts):
    A=bounds[i]
    for j in range(i+1,len(parts)):
        b=parts[j];B=bounds[j]
        if min(A.xmax,B.xmax)<max(A.xmin,B.xmin)-.01 or min(A.ymax,B.ymax)<max(A.ymin,B.ymin)-.01 or min(A.zmax,B.zmax)<max(A.zmin,B.zmin)-.01:continue
        volume=a['sh'].intersect(b['sh']).Volume()
        if volume>.05:hits.append({'a':a['ad'],'b':b['ad'],'volume_mm3':round(volume,3)})
        elif a['sh'].distance(b['sh'])<.02:contacts.append([i,j])
    if i%100==0:print('Checked',i,'/',len(parts),'hits',len(hits),flush=True)
adj=[set() for p in parts]
for a,b in contacts:adj[a].add(b);adj[b].add(a)
seen={i for i,b in enumerate(bounds) if abs(b.ymin)<.02};queue=list(seen)
while queue:
    a=queue.pop()
    for b in adj[a]-seen:seen.add(b);queue.append(b)
disconnected=[parts[i]['ad'] for i in range(len(parts)) if i not in seen]
result={'parts':len(parts),'unintended_solid_overlaps':hits,'contacts':contacts,'disconnected_contact_components':disconnected,'passed':not hits and not disconnected,'manufacturing_release':False,'scope':'new CAD solids and ground contact graph only; touching does not prove fastening strength; migrated/device mounting separately audited'}
Path(__file__).with_name('mechanical_audit.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k!='contacts'},indent=2),flush=True)
import os,sys
sys.stdout.flush();os._exit(0 if result['passed'] else 1)
