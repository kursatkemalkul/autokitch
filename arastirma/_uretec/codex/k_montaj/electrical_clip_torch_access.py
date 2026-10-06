"""Limiting TIG envelope over the four bare mounting-foot perimeters.
Check preassembly with all clips on the same own host, before cables.
"""
from lower_support import *
import pickle,hashlib,gzip,trimesh
src=OUT/'k1/k_parca_head_verified.pkl'
P=pickle.loads(src.read_bytes())['P']
folder=OUT/'electrical_clip_weld_candidate'
payload=json.loads(gzip.decompress((folder/'geometry.json.gz').read_bytes()))
assert payload['source_parts_sha256']==hashlib.sha256(src.read_bytes()).hexdigest()
probe=json.loads((OUT/'k1/electrical_clip_mount_probe.json').read_text())
rows={r['part']:r for r in probe['clips']};checks=[];mesh={}
for join in payload['joins']:
 a=join['clip'];host=join['host'];r=rows[a];face=r['mounting_face_candidates'][0]['faces'][0]
 k='xyz'.index(face['axis']);v=np.asarray(P[a]['V']);q=v[abs(v[:,k]-face['plane_mm'])<.001]
 lo=q.min(0);hi=q.max(0);other=[i for i in range(3) if i!=k]
 n=np.zeros(3);n[k]=1 if face['side']=='lo' else -1
 stage=[host]+[j['clip'] for j in payload['joins'] if j['host']==host]
 for edge,(ac,fixed,sign) in enumerate([(other[0],other[1],-1),(other[0],other[1],1),(other[1],other[0],-1),(other[1],other[0],1)]):
  p0=lo.copy();p1=lo.copy();p0[fixed]=p1[fixed]=lo[fixed] if sign<0 else hi[fixed];p1[ac]=hi[ac]
  outward=np.zeros(3);outward[fixed]=sign
  trials=[]
  tangent=np.zeros(3);tangent[ac]=1
  directions=[(angle,skew) for skew in (0,-30,30,-45,45,-60,60) for angle in (45,30,20)]
  for angle,skew in directions:
   axis=np.sin(np.deg2rad(angle))*outward+np.cos(np.deg2rad(angle))*n+np.tan(np.deg2rad(skew))*tangent
   axis=axis/np.linalg.norm(axis)
   cloud=[];radii=[]
   for u in np.linspace(0,1,int(np.ceil(np.linalg.norm(p1-p0)))+1):
    root=p0+u*(p1-p0)
    for s in range(1,51):cloud.append(root+s*axis);radii.append(min(6.,.15+.11*s))
   cloud=np.asarray(cloud);radii=np.asarray(radii);surfaces=[]
   for part in stage:
    if part not in mesh:mesh[part]=trimesh.Trimesh(P[part]['V'],P[part]['F'],process=False)
    _,d,_=trimesh.proximity.closest_point(mesh[part],cloud)
    clearance=float(np.min(d-radii))
    surfaces.append(dict(part=part,minimum_clearance_mm=clearance,passed=clearance>=-.002))
   passed=all(s['passed'] for s in surfaces)
   trials.append(dict(base_angle_deg=angle,tangent_skew_deg=skew,passed=passed))
   if passed:break
  checks.append(dict(seam=join['seams'][edge],stage_parts=stage,axis=axis.tolist(),base_angle_deg=angle,tangent_skew_deg=skew,
   trials=trials,surfaces=surfaces,passed=passed))
r=dict(source_parts_sha256=payload['source_parts_sha256'],candidate_geometry_sha256=hashlib.sha256((folder/'geometry.json.gz').read_bytes()).hexdigest(),
 checks=checks,passed_all_preassembly_envelopes=all(c['passed'] for c in checks),
 tool_envelope=dict(length_mm=50,maximum_radius_mm=6,root_step_mm=1,axis_step_mm=1,root_process_zone_mm=1),
 cables_installed_during_welding=False,particular_purchased_torch_certified=False,fixture_geometry_checked=False,production_release=False)
(folder/'torch_access_audit.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
print('CLIP_TORCH_ACCESS',r['passed_all_preassembly_envelopes'],'FAILED',[c['seam'] for c in checks if not c['passed']],flush=True)
sys.stdout.flush();os._exit(0 if r['passed_all_preassembly_envelopes'] else 2)
