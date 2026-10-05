"""Validate step72 legacy GLB fragments on the native physical plate boundary."""
from pathlib import Path
import sys,pickle,json,numpy as np,os
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'arastirma/_uretec/codex/k_montaj'))
from mechanism_mounts import build_mounts
import cadquery as cq
p=pickle.load(open(HERE/'k_parca.pkl','rb'))['P'];native={q['ad']:q['sh'] for q in build_mounts()[0]};rows=[]
for x in (40,360):
 for z in (-755,-645):
  a=f'itici_taban_{x}_{z}';b=f'k72_itici_ust_plaka_{4000.+x}_{float(z)}'
  boundary=cq.Compound.makeCompound(native[b].Faces());q=p[a]['V'][p[a]['F']]
  err=max(boundary.distance(cq.Vertex.makeVertex(*v)) for v in np.vstack([q.reshape(-1,3),q.mean(1)]))
  rows.append({'fragment':a,'physical_stock':b,'max_boundary_distance_mm':float(err),'triangles':len(q)})
report={'checks':rows,'passed':all(r['max_boundary_distance_mm']<=.015 for r in rows),'geometry_modified':False,'production_release':False}
(HERE/'pusher_plate_fragment_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('PUSHER_FRAGMENTS',report['passed'],flush=True);os._exit(0 if report['passed'] else 2)
