"""Measure actual re-extracted rounded posts and16 weld landings."""
from pathlib import Path
import pickle,json,hashlib
import numpy as np
import manifold3d as m3
import trimesh
H=Path(__file__).resolve().parent
P=pickle.load((H/'k_parca79_verified.pkl').open('rb'))['P'];rows=[]
def mesh(a):return trimesh.Trimesh(P[a]['V'],P[a]['F'],process=False)
def distance(points,names):
 return min(float(trimesh.proximity.closest_point(mesh(a),np.asarray(points))[1].max()) for a in names)
for i,(x,z) in enumerate(((4040.,-755.),(4040.,-645.),(4360.,-755.),(4360.,-645.))):
 a=f'k_itici_sac_{i}';v=P[a]['V'];q=v[:,[0,2]]-[x,z];u=np.abs(q);corner=(u[:,0]>=5.999)&(u[:,1]>=5.999)
 radial=np.linalg.norm(u[corner]-6,axis=1)
 arc_error=np.minimum(abs(radial-4),abs(radial-2));assert len(arc_error)>8
 flat=(np.minimum(abs(u[:,0]-10),abs(u[:,0]-8))<.001)&(u[:,1]<=6.001)
 flat|=(np.minimum(abs(u[:,1]-10),abs(u[:,1]-8))<.001)&(u[:,0]<=6.001)
 classified=corner|flat
 solid=m3.Manifold(m3.Mesh(vert_properties=np.asarray(v-[x,900,z],dtype=np.float32),tri_verts=np.asarray(P[a]['F'],dtype=np.uint32)))
 volume=float(solid.volume());nominal=(144-12*(4-np.pi))*58
 extent_error=float(max(np.max(abs(v.min(0)-[x-10,900,z-10])),np.max(abs(v.max(0)-[x+10,958,z+10]))))
 weldrows=[]
 for e in range(4):
  name=f'k72_itici_ayak_kaynagi_{x}_{z}_{e}';wv=P[name]['V'];taxis=0 if e in (0,2) else 2
  centre=x if taxis==0 else z;span=[float(wv[:,taxis].min()-centre),float(wv[:,taxis].max()-centre)]
  midpoint=[(x,900.5,z-10),(x+10,900.5,z),(x,900.5,z+10),(x-10,900.5,z)][e]
  basepoint=list(midpoint);basepoint[1]=900
  post_contact=distance([midpoint],[a]);plate_contact=distance([basepoint],[f'k72_itici_ust_plaka_{x}_{z}',f'itici_taban_{int(x-4000)}_{int(z)}'])
  weld_contact=distance([midpoint,basepoint],[name])
  weldrows.append({'part':name,'actual_flat_landing_span_mm':span,'post_contact_error_mm':post_contact,'plate_contact_error_mm':plate_contact,'weld_contact_error_mm':weld_contact,'passed':abs(span[0]+6)<.001 and abs(span[1]-6)<.001 and max(post_contact,plate_contact,weld_contact)<.001})
 row={'part':a,'outer_radius_mm':4,'inner_radius_mm':2,'outer_arc_vertices':int((abs(radial-4)<.001).sum()),'inner_arc_vertices':int((abs(radial-2)<.001).sum()),'maximum_arc_radius_error_mm':float(arc_error.max()),'unclassified_cross_section_vertices':int((~classified).sum()),'maximum_envelope_error_mm':extent_error,'manifold_status':str(solid.status()),'actual_volume_mm3':volume,'analytic_rounded_profile_volume_mm3':float(nominal),'relative_volume_error':abs(volume-nominal)/nominal,'welds':weldrows,'passed':bool(arc_error.max()<.001 and classified.all() and extent_error<.001 and str(solid.status())=='Error.NoError' and abs(volume-nominal)/nominal<.005 and all(r['passed'] for r in weldrows))}
 rows.append(row);print('POST79',a,row['passed'],'radius_error',row['maximum_arc_radius_error_mm'],'welds',all(r['passed'] for r in weldrows),flush=True)
report={'source_parts_sha256':hashlib.sha256((H/'k_parca79_verified.pkl').read_bytes()).hexdigest(),'scope':'Four custom pusher posts and their16 bottom welds; no whole-station release','checks':rows,'passed':all(r['passed'] for r in rows),'production_release':False,'weld_strength_and_torch_access_verified':False}
(H/'stage79_post_geometry_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
assert report['passed']
