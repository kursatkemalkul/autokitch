"""Export native UR10e body-local visual geometry and exact USD joint frames.
No physics success is implied by this kinematic browser export.
"""
import json, sys, struct
sys.dont_write_bytecode = True
from pathlib import Path
import numpy as np
import trimesh
from pxr import Usd, UsdGeom

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT.parent / 'codex-isaac-pose-editor-v2'
SRC = SOURCE / 'otonom/hat3d/fizik/pose-editor-v2'
sys.path.insert(0, str(SOURCE / 'arastirma/_uretec/isaac_pose_editor_v2'))
from geometry import mesh_of
from rig import numpy_matrix, Rig

OUT = ROOT / 'otonom/hat3d/robot-main-v1'
OUT.mkdir(parents=True, exist_ok=True)
rig_data = json.loads((SRC / 'rig.json').read_text())
poses = json.loads((SRC / 'default_poses.json').read_text())
stage = Usd.Stage.Open(str(SRC / 'POZISYON_DUZENLE.usdc'))
cache = UsdGeom.XformCache(0)
scene = trimesh.Scene()
bodies = sorted(set(rig_data['bodies']))
body_nodes = {b: 'body_%02d' % i for i, b in enumerate(bodies)}
for b, name in body_nodes.items():
    scene.graph.update(frame_to=name, matrix=np.eye(4))
counts = {}
lod=[]
for p in Usd.PrimRange.Stage(stage, Usd.TraverseInstanceProxies()):
    path = str(p.GetPath())
    if not (path.startswith('/World/RailSystem/Arm/') or path.startswith('/World/RailSystem/Gripper/') or path.startswith('/World/RailSystem/Carriage/')):
        continue
    if '/collisions/' in path:
        continue
    if UsdGeom.Imageable(p) and UsdGeom.Imageable(p).ComputeVisibility() == 'invisible':
        continue
    m = mesh_of(p)
    if m is None:
        continue
    body = next((b for b in sorted(bodies, key=len, reverse=True) if path.startswith(b+'/')), None)
    if body is None:
        continue
    relative = np.linalg.inv(numpy_matrix(cache.GetLocalToWorldTransform(stage.GetPrimAtPath(body)))) @ numpy_matrix(cache.GetLocalToWorldTransform(p))
    m.apply_transform(relative)
    # Display only: 1 mm vertex clustering; exact collision meshes below stay intact.
    if '/Arm/' in path and len(m.vertices)>10000:
        old=m.vertices.copy();cells=np.floor(old/.001).astype(np.int64)
        _,ids=np.unique(cells,axis=0,return_inverse=True)
        number=np.bincount(ids);vertices=np.column_stack([np.bincount(ids,weights=old[:,i])/number for i in range(3)])
        faces=ids[m.faces];keep=(faces[:,0]!=faces[:,1])&(faces[:,1]!=faces[:,2])&(faces[:,0]!=faces[:,2])
        error=float(np.linalg.norm(vertices[ids]-old,axis=1).max())
        lod.append(dict(body=body,original_triangles=len(m.faces),render_triangles=int(keep.sum()),max_vertex_displacement_m=error))
        m=trimesh.Trimesh(vertices,faces[keep],process=True)
    color = [.10,.12,.14]
    dc = UsdGeom.Gprim(p).GetDisplayColorAttr().Get()
    if dc: color = list(dc[0])
    elif any(x in path.lower() for x in ('blue','cap')): color = [.45,.72,.77]
    if any(x in path for x in ('Food','SupportLip')): color = [.18,.54,.62]
    m.visual = trimesh.visual.ColorVisuals(m, vertex_colors=np.array(np.array([*color,1.])*255,dtype=np.uint8))
    node = body_nodes[body]+'_mesh_'+str(counts.get(body,0))
    counts[body] = counts.get(body,0)+1
    scene.add_geometry(m, node_name=node, geom_name=node, parent_node_name=body_nodes[body])
scene.export(OUT / 'ur10e_short.glb')
(OUT/'display_lod.json').write_text(json.dumps(dict(display_only=True,collision_geometry_unchanged=True,voxel_m=.001,bodies=lod),indent=2))
collision=[]
for p in Usd.PrimRange.Stage(stage, Usd.TraverseInstanceProxies()):
    path=str(p.GetPath())
    if '/RailSystem/Arm/' in path and '/collisions/' not in path: continue
    if not ('/RailSystem/Arm/' in path or '/RailSystem/Gripper/' in path): continue
    if UsdGeom.Imageable(p) and UsdGeom.Imageable(p).ComputeVisibility() == 'invisible': continue
    body=next((b for b in sorted(bodies,key=len,reverse=True) if path.startswith(b+'/')),None)
    if body is None: continue
    m=mesh_of(p)
    if m is None: continue
    m.apply_transform(np.linalg.inv(numpy_matrix(cache.GetLocalToWorldTransform(stage.GetPrimAtPath(body)))) @ numpy_matrix(cache.GetLocalToWorldTransform(p)))
    if '/Gripper/' in path and not m.is_watertight: m=m.convex_hull
    collision.append(dict(body=body,path=path,vertices=m.vertices.tolist(),faces=m.faces.tolist()))
(OUT/'collision.json').write_text(json.dumps(collision,separators=(',',':')))
rig_data['body_nodes'] = body_nodes
rig_data['arm_joints'] = ['shoulder_pan_joint','shoulder_lift_joint','elbow_joint','wrist_1_joint','wrist_2_joint','wrist_3_joint']
rig_data['machine_base_commit'] = '7866c9213cdcb535d225b1a079194d9938eaab94'
rig_data['physics'] = False
(OUT/'rig.json').write_text(json.dumps(rig_data, indent=2))
(OUT/'poses.json').write_text(json.dumps(poses, indent=2))
# Independently generated reference TCPs for browser FK regression.
rig = Rig(stage, rig_data)
refs=[]
for key,p in poses.items():
    pos,rot=rig.tcp(p['q'],p['rail'],p['jaw'])
    refs.append(dict(key=key,q=p['q'],rail=p['rail'],jaw=p['jaw'],tcp=pos.tolist(),rotation=rot.tolist()))
(OUT/'fk_reference.json').write_text(json.dumps(refs, indent=2))
# Inspect full-machine GLB metadata without loading its meshes.
model=ROOT/'otonom/hat3d/v3/hat3_v7.glb'
with model.open('rb') as f:
    f.read(12);length,kind=struct.unpack('<II',f.read(8));gltf=json.loads(f.read(length))
metadata={ 'node_count':len(gltf.get('nodes',[])), 'nodes':[{ 'index':i, 'name':n.get('name',''), 'mesh':n.get('mesh'), 'translation':n.get('translation'), 'rotation':n.get('rotation'), 'children':n.get('children')} for i,n in enumerate(gltf.get('nodes',[]))], 'animations':[a.get('name') for a in gltf.get('animations',[])] }
(OUT/'machine_nodes.json').write_text(json.dumps(metadata,indent=2))
print(json.dumps(dict(bodies=counts,triangles=sum(len(m.faces) for m in scene.geometry.values()),glb_bytes=(OUT/'ur10e_short.glb').stat().st_size,animations=metadata['animations']),indent=2))
