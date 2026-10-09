from build import *
import io
source=ROOT.parent/'codex-rochu-v2-belly-v9/otonom/hat3d/rochu-sabit-v2'
head=trimesh.load(io.BytesIO(gzip.decompress((source/'fixed_head.glb.gz').read_bytes())),file_type='glb');d=json.loads((source/'head_definition.json').read_text());roots=[]
for i,old in enumerate(d['finger_roots']):
 w=np.array(old);w[:3,:3]=w[:3,:3]@Rotation.from_euler('z',180,degrees=True).as_matrix();roots.append(w.tolist());head.graph.update(frame_to='Finger_'+str(i),matrix=w)
save_scene(head,'fixed_head')
d.update(finger_roots=roots,root_hash=hashlib.sha256(json.dumps(roots,separators=(',',':')).encode()).hexdigest(),mount_reversed_degrees=0,rotation_from_v9_degrees=180,orientation_note='Returned180degrees relative to V9; mounting radius unchanged50mm',physical_grasp_verified=False,gripping_face='Original orientation restored relative to supplied V9; contact feasibility recorded separately',neutral_diameter_mm=121.,neutral_diameter_note='Distal pad centreline estimate: 2*(50+10.5)mm; not an inner workpiece range',previous_outward_gripping_face_layout_rejected=False)
(OUT/'head_definition.json').write_text(json.dumps(d,indent=2))
