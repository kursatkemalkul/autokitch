from lower_support import *
import hashlib,collections
Y=H/'yama_v9'
for p in (Y,Y/'kaynak',Y/'kaynak/gece'):sys.path.insert(0,str(p))
from m8kit import Glb
root=Path('_local/codex_k_montaj/chain73/A')
def inventory(file):
 g=Glb(str(file));out={}
 for p in g.prims:
  if p['name']=='K_GOVDE__kabuk' or p.get('gizli') or p['pr'].get('mode',4)!=4:continue
  q=p['X'][p['T']];area=np.linalg.norm(np.cross(q[:,1]-q[:,0],q[:,2]-q[:,0]),axis=1);q=q[area>1e-9]
  # Compression may reorder triangles; compare exact positions after 1 micron rounding.
  dst=out.setdefault(p['name'],collections.Counter())
  for t in np.round(q,3):dst[hashlib.sha256(t.tobytes()).hexdigest()]+=1
 return out
before=inventory(root/'hat3_v10r.glb');after=inventory(root/'hat3_v10s.glb')
changed=[n for n in set(before)|set(after) if before.get(n)!=after.get(n)]
r={'source':'hat3_v10r.glb','output':'hat3_v10s.glb','comparison_grid_mm':.001,'compared_nodes':len(before),'changed_nodes_outside_K_body':changed,'passed':not changed,'full_station_release':False}
Path('_local/codex_k_montaj/k78_unrelated_geometry_audit.json').write_text(json.dumps(r,indent=2),encoding='utf-8');print(r,flush=True);os._exit(0)
