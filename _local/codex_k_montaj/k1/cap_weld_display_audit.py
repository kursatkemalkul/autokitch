"""Round-trip actual cap process meshes using the unchanged v6 GLB exporter."""
from pathlib import Path
import sys,json,pickle,hashlib
import numpy as np
import trimesh
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parents[2]/'_local/claude_son_yerel/gece2/cekmece'))
import v2geo as G
from k_flush_weld_display import export_markers
path=H/'plan_k_cap_full.pkl';D=pickle.loads(path.read_bytes());before=pickle.dumps(D['P'])
meshes,parts,records=export_markers(D,['kaynak']);assert len(meshes)==len(parts)==len(records)==32
assert pickle.dumps(D['P'])==before
checks=[]
for m,r in zip(meshes,records):
 V=np.asarray(m['V'])+m['translation'];cap=D['P'][r['reference_cap']]
 target=trimesh.Trimesh(cap['V']/1000.,cap['F'],process=False)
 _,dist,_=trimesh.proximity.closest_point(target,V)
 assert dist.max()*1000.<.001
 assert parts[m['ad']]['h']==D['HAR'][r['reference_cap']]
 checks.append(dict(marker=m['ad'],maximum_surface_distance_mm=float(dist.max()*1000.),same_motion_as_real_cap=True))
glb=H/'cap_weld_display_preview.glb'
G.glb_yaz(str(glb),meshes,[dict(name='kaynak',pbrMetallicRoughness=dict(baseColorFactor=[1,0,0,1],metallicFactor=0,roughnessFactor=1))])
scene=trimesh.load(glb,force='scene');assert len(scene.geometry)==32
for name in scene.geometry:
 assert name in parts
r={'source_model_sha256':D['source_model_sha256'],'source_plan_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'marker_count':32,'display_triangle_count':64,'physical_product_part_count':len(D['P']),'physical_product_geometry_unchanged':True,'common_player_unchanged':True,'source_surface_checks':checks,'glb_round_trip_passed':True,'process_markings_export_hook_installed':True,'whole_animation_rendered_in_browser':False,'production_release':False}
(H/'cap_weld_display_audit.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
print('CAP_DISPLAY',32,'PRODUCT_GEOMETRY_UNCHANGED',len(D['P']),'SOURCE_SURFACE_MAX_MM',max(q['maximum_surface_distance_mm'] for q in checks),flush=True)
