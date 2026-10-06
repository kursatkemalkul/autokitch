"""Measure native flush-weld cap roots; no fictitious protruding weld hardware.
Native h3_k_sac_v1 already specifies continuous TIG butt weld, ground flush.
This report does not pass the animation/tool access gate by itself.
"""
from pathlib import Path
import json,pickle,hashlib
import numpy as np
import trimesh
from scipy.spatial import ConvexHull
H=Path(__file__).resolve().parent;parts=H/'k_parca_catalog_verified.pkl'
P=pickle.loads(parts.read_bytes())['P'];rows=[]
for name in ('kose_dikmesi_20_-800','kose_dikmesi_20_42','kose_dikmesi_380_-800','kose_dikmesi_380_42'):
 cap=name+'_tapa';v=P[cap]['V'];y=float(v[:,1].min());points=np.unique(np.round(v[np.abs(v[:,1]-y)<.001][:,[0,2]],4),axis=0)
 outline=points[ConvexHull(points).vertices]
 samples=[];segments=[]
 for a,b in zip(outline,np.roll(outline,-1,axis=0)):
  length=float(np.linalg.norm(b-a));n=max(1,int(np.ceil(length)))
  for q in np.linspace(a,b,n+1):samples.append([q[0],y,q[1]])
  segments.append({'start_mm':[float(a[0]),y,float(a[1])],'end_mm':[float(b[0]),y,float(b[1])],'length_mm':length})
 mesh=trimesh.Trimesh(P[name]['V'],P[name]['F'],process=False)
 _,dist,_=trimesh.proximity.closest_point(mesh,np.asarray(samples))
 assert abs(float(v[:,1].max()-y)-2.)<.001
 # The source chamfered cap and rounded tube have a small corner root gap;
 # record it rather than claiming every point has zero-distance contact.
 rows.append({'cap':cap,'profile':name,'cap_thickness_mm':2.,'closed_root_segments':segments,'perimeter_length_mm':sum(q['length_mm'] for q in segments),'sampling_max_step_mm':1.,'minimum_root_distance_mm':float(dist.min()),'maximum_root_gap_mm':float(dist.max()),'source_declared_process':'Continuous perimeter TIG butt weld, then grind flush; native h3_k_sac_v1.iskelet declaration, not a protruding fillet or extra purchased fastener','source_profile_end_height_mm':float(P[name]['V'][:,1].max()),'cap_bottom_height_mm':y,'root_geometry_within_0_6_mm':bool(dist.max()<=.6),'animation_and_torch_sequence_verified':False})
r={'source_parts_sha256':hashlib.sha256(parts.read_bytes()).hexdigest(),'source_model_sha256':json.loads((H.parent/'actuator_catalog_fastener_candidate/source_scope_audit.json').read_text())['output_sha256'],'source_definition':'arastirma/_uretec/h3/h3_k_sac_v1.py:iskelet, cap declaration','checks':rows,'all_cap_root_geometries_within_0_6_mm':all(q['root_geometry_within_0_6_mm'] for q in rows),'animation_integration_complete':False,'production_release':False,'note':'Four source-declared flush butt welds need an explicit fabrication operation and highlight in the common player; this measured report alone does not resolve whole-station connection gates.'}
(H/'catalog_flush_cap_welds.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
print('FLUSH_CAP_ROOTS',r['all_cap_root_geometries_within_0_6_mm'],[round(q['maximum_root_gap_mm'],4) for q in rows])
