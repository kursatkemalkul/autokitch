"""Measured TIG tip envelope around four native flush-cap welds, free-post bench only.
This verifies an explicit limiting envelope, not an unspecified purchased torch.
Fixtures, full scene clearance and the chosen torch catalogue remain separate gates.
"""
from pathlib import Path
import json,pickle,hashlib
import numpy as np
import trimesh
H=Path(__file__).resolve().parent;path=H/'k_parca_catalog_verified.pkl'
P=pickle.loads(path.read_bytes())['P'];roots=json.loads((H/'catalog_flush_cap_welds.json').read_text())
assert hashlib.sha256(path.read_bytes()).hexdigest()==roots['source_parts_sha256']
checks=[]
for record in roots['checks']:
 targets={name:trimesh.Trimesh(P[name]['V'],P[name]['F'],process=False) for name in (record['profile'],record['cap'])}
 nodes=[];radii=[];frames=[]
 for segment in record['closed_root_segments']:
  a=np.array(segment['start_mm']);b=np.array(segment['end_mm']);edge=b-a
  # ConvexHull in XZ is CCW: outward is (dz,0,-dx).
  out=np.array([edge[2],0.,-edge[0]]);out/=np.linalg.norm(out)
  direction=(out+np.array([0.,1.,0.]))/np.sqrt(2.)
  for q in np.linspace(a,b,int(np.ceil(segment['length_mm']))+1):
   frames.append({'tip_mm':q.tolist(),'torch_axis':direction.tolist()})
   for s in np.arange(1.,51.,1.):
    nodes.append(q+direction*s);radii.append(min(6.,.15+.11*s))
 centers=np.asarray(nodes);rad=np.asarray(radii);row=[]
 for name,mesh in targets.items():
  _,dist,_=trimesh.proximity.closest_point(mesh,centers)
  margin=dist-rad-.002
  row.append({'part':name,'minimum_surface_clearance_minus_envelope_radius_mm':float(margin.min()),'sample_count':len(centers),'passed_local_clearance':bool(margin.min()>0)})
 checks.append({'profile':record['profile'],'cap':record['cap'],'root_sample_step_mm':1.,'tool_axis_sample_step_mm':1.,'limiting_tip_envelope':{'length_mm':50.,'maximum_radius_mm':6.,'start_distance_from_weld_mm':1.,'first_mm':'intentional electrode/process zone at weld root'},'tool_frames':frames,'checks':row,'passed_free_post_cap_envelope':all(x['passed_local_clearance'] for x in row)})
r={'source_parts_sha256':roots['source_parts_sha256'],'source_model_sha256':roots['source_model_sha256'],'checks':checks,'passed_all_free_post_cap_envelopes':all(x['passed_free_post_cap_envelope'] for x in checks),'chosen_torch_catalogue_verified':False,'fixture_verified':False,'full_scene_torch_paths_verified':False,'production_release':False}
(H/'cap_torch_access.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
print('CAP_TORCH_ENVELOPE',r['passed_all_free_post_cap_envelopes'],[min(c['minimum_surface_clearance_minus_envelope_radius_mm'] for c in q['checks']) for q in checks],flush=True)
assert r['passed_all_free_post_cap_envelopes']
