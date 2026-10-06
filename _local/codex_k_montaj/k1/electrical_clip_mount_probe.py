"""Recover native electrical clip roles and measure mounting-face carriers.
Metadata bbox matches are candidates, never renamed geometry or mount proof.
"""
from pathlib import Path
import pickle,json,hashlib,numpy as np,trimesh
H=Path(__file__).resolve().parent;root=H.parents[2]
cache=H/'k_parca_head_verified.pkl';P=pickle.loads(cache.read_bytes())['P']
native=root/'arastirma/_uretec/h3/yama_v9/kaynak/_v7/parca_kutulari.json'
inventory=json.loads(native.read_text(encoding='utf-8'))['parca']
rows=[]
for unit,items in inventory.items():
 for r in items:
  if len(r)>=8 and 'kelepce' in r[0] and unit.startswith(('ELK_K','ELK_K_TARTI')):
   rows.append((unit,r[0],np.array(r[2:8],float).reshape(3,2).T))
mesh={}
def tm(a):
 if a not in mesh:mesh[a]=trimesh.Trimesh(P[a]['V'],P[a]['F'],process=False)
 return mesh[a]
out=[]
for a in sorted(P):
 if not a.startswith(('elk_k_celik_','elk_k_tarti_celik_')):continue
 v=np.asarray(P[a]['V']);lo=v.min(0);hi=v.max(0);bb=np.array([lo,hi])
 matches=[(float(abs(bb-b).max()),u,n) for u,n,b in rows if abs(bb-b).max()<.3]
 if not matches:continue
 candidates=[]
 for host in P:
  if host==a or P[host]['tur'] not in ('sac','profil','kapak','mek'):continue
  w=np.asarray(P[host]['V']);wl=w.min(0);wh=w.max(0)
  if np.any(lo>wh+.15) or np.any(hi<wl-.15):continue
  faces=[]
  for axis in range(3):
   for side,value in [('lo',lo[axis]),('hi',hi[axis])]:
    q=v[abs(v[:,axis]-value)<.001]
    if len(q)<3:continue
    _,d,_=trimesh.proximity.closest_point(tm(host),q)
    if d.max()<.15:
     faces.append(dict(axis='xyz'[axis],side=side,plane_mm=float(value),vertex_count=len(q),max_distance_mm=float(d.max())))
  if faces:candidates.append(dict(part=host,faces=faces,stock_bbox_mm=[wl.tolist(),wh.tolist()]))
 out.append(dict(part=a,native_bbox_candidates=[dict(unit=u,name=n,max_bbox_difference_mm=d) for d,u,n in sorted(matches)],
  mounting_face_candidates=candidates,lo_mm=lo.tolist(),hi_mm=hi.tolist(),mount_verified=False))
r=dict(source_parts_sha256=hashlib.sha256(cache.read_bytes()).hexdigest(),native_inventory_sha256=hashlib.sha256(native.read_bytes()).hexdigest(),
 clips=out,native_helper='h3_elk_ortak.kelepce: fused ring/tongue/tab, no mounting hole or screw',
 production_release=False)
(H/'electrical_clip_mount_probe.json').write_text(json.dumps(r,indent=2,ensure_ascii=False),encoding='utf-8')
for r in out:print(r['part'],r['native_bbox_candidates'],r['mounting_face_candidates'],flush=True)
