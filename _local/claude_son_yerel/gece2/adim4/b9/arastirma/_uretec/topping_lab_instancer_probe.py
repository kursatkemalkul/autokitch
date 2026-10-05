"""Check native PhysX point-instanced rigid food before scaling up."""
from isaacsim import SimulationApp
app=SimulationApp({'headless':True})
import numpy as np
import omni.usd
from pxr import UsdGeom,UsdPhysics,PhysxSchema,Gf,Vt,UsdUtils
from isaacsim.core.api import World
import omni.physics.tensors
from omni.physx import get_physx_interface
omni.usd.get_context().new_stage()
s=omni.usd.get_context().get_stage()
UsdGeom.SetStageUpAxis(s,UsdGeom.Tokens.z);UsdGeom.SetStageMetersPerUnit(s,1.)
scene=UsdPhysics.Scene.Define(s,'/World/physicsScene')
scene.CreateGravityDirectionAttr(Gf.Vec3f(0,0,-1));scene.CreateGravityMagnitudeAttr(9.81)
px=PhysxSchema.PhysxSceneAPI.Apply(scene.GetPrim());px.CreateEnableGPUDynamicsAttr(True);px.CreateBroadphaseTypeAttr('GPU')
pi=UsdGeom.PointInstancer.Define(s,'/World/Food')
p=UsdGeom.Xform.Define(s,'/World/Food/proto')
UsdPhysics.RigidBodyAPI.Apply(p.GetPrim())
UsdPhysics.MassAPI.Apply(p.GetPrim()).CreateDensityAttr(1100.)
c=UsdGeom.Cube.Define(s,'/World/Food/proto/shape');c.CreateSizeAttr(1.)
UsdPhysics.CollisionAPI.Apply(c.GetPrim())
pc=PhysxSchema.PhysxCollisionAPI.Apply(c.GetPrim());pc.CreateContactOffsetAttr(.0001);pc.CreateRestOffsetAttr(0.)
pi.CreatePrototypesRel().SetTargets([p.GetPath()])
pi.CreateProtoIndicesAttr([0,0,0])
pi.CreatePositionsAttr([Gf.Vec3f(.0,0,.1),Gf.Vec3f(.02,0,.1),Gf.Vec3f(.04,0,.1)])
pi.CreateOrientationsAttr([Gf.Quath(1)]*3)
dims=np.array([[.004,.010,.004],[.005,.012,.003],[.003,.008,.005]],dtype=np.float32)
pi.CreateScalesAttr(Vt.Vec3fArray.FromNumpy(dims))
floor=UsdGeom.Cube.Define(s,'/World/Floor');floor.CreateSizeAttr(1.)
floor.AddTranslateOp().Set(Gf.Vec3d(0,0,-.01));floor.AddScaleOp().Set(Gf.Vec3f(1,1,.02))
UsdPhysics.CollisionAPI.Apply(floor.GetPrim())
w=World(stage_units_in_meters=1.,physics_dt=1/240,rendering_dt=1/60,physics_prim_path='/World/physicsScene',backend='warp',device='cuda:0')
w.reset();w.step(render=False)
import carb
carb.settings.get_settings().set_bool('/physics/updateToUsd',True)
sid=UsdUtils.StageCache.Get().GetId(s).ToLongInt()
sv=omni.physics.tensors.create_simulation_view('warp',stage_id=sid)
for pattern in ['/World/Food','/World/Food/*','/World/Food/proto','/World/*']:
    try:
        view=sv.create_rigid_body_view(pattern)
        print('VIEW',pattern,view.count,view.prim_paths,flush=True)
        if view.count:print('MASSES',view.get_masses().numpy().tolist(),'POSE',view.get_transforms().numpy().tolist(),flush=True)
    except Exception as e:print('PROBE_VIEW_ERROR',pattern,str(e),flush=True)
for i in range(120):w.step(render=False)
get_physx_interface().update_transformations(True,True,True,False)
pos=np.array(pi.GetPositionsAttr().Get());print('POSITIONS',pos.tolist(),flush=True)
from omni.physx import get_physx_scene_query_interface
for x in [0.,.02,.04]:
    print('RAY',x,get_physx_scene_query_interface().raycast_closest([x,0,.12],[0,0,-1],.2),flush=True)
print('POINT_INSTANCER_PHYSICS_VERIFIED',bool(np.all(pos[:,2]<.01) and np.all(pos[:,2]>0)),flush=True)
app.close()
