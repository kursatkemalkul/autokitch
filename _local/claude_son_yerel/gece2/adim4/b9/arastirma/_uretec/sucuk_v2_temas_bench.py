"""Small isolated contact test, not a measurement of actual sausage/dough.

Tests configured model for ball-like rebound and excessive interpenetration.
"""
from pathlib import Path
import json,math
import numpy as np
from isaacsim import SimulationApp
app=SimulationApp({'headless':True})
import omni.usd,omni.physics.tensors
from pxr import Usd,UsdGeom,UsdPhysics,PhysxSchema,UsdShade,Gf,UsdUtils
from isaacsim.core.api import World
from sucuk_v2_sahne import contact_material
omni.usd.get_context().new_stage()
s=omni.usd.get_context().get_stage();UsdGeom.SetStageUpAxis(s,'Z');UsdGeom.SetStageMetersPerUnit(s,1.)
sc=UsdPhysics.Scene.Define(s,'/World/physicsScene');sc.CreateGravityDirectionAttr(Gf.Vec3f(0,0,-1));sc.CreateGravityMagnitudeAttr(9.81)
PhysxSchema.PhysxSceneAPI.Apply(sc.GetPrim()).CreateEnableGPUDynamicsAttr(True)
paths=[];cases=[]
for i,k in enumerate([1000.,5000.,20000.]):
    for j,side in enumerate([.006,.008,.010]):
        m=side**3*1000
        floor=UsdGeom.Cube.Define(s,f'/World/floor_{i}_{j}')
        floor.CreateSizeAttr(1.);floor.AddScaleOp().Set(Gf.Vec3f(.04,.04,.008))
        floor.AddTranslateOp().Set(Gf.Vec3d(i*.06/.04,j*.06/.04,.004/.008))
        # Transform order above is scale*translation in USD: explicit matrix avoids ambiguity.
        floor.ClearXformOpOrder()
        fm=Gf.Matrix4d(1);fm.SetScale(Gf.Vec3d(.04,.04,.008));fm.SetTranslateOnly(Gf.Vec3d(i*.06,j*.06,.004))
        floor.AddTransformOp().Set(fm)
        UsdPhysics.CollisionAPI.Apply(floor.GetPrim())
        dm=contact_material(s,f'dough_{i}_{j}',.5,1000.,1.6*math.sqrt(1000*.000512))
        UsdShade.MaterialBindingAPI.Apply(floor.GetPrim()).Bind(dm,UsdShade.Tokens.weakerThanDescendants,'physics')
        path=f'/World/food_{i}_{j}';paths.append(path)
        cube=UsdGeom.Cube.Define(s,path);cube.CreateSizeAttr(side)
        cube.AddTranslateOp().Set(Gf.Vec3d(i*.06,j*.06,.008+.035+side/2))
        UsdPhysics.RigidBodyAPI.Apply(cube.GetPrim());UsdPhysics.MassAPI.Apply(cube.GetPrim()).CreateMassAttr(m)
        rb=PhysxSchema.PhysxRigidBodyAPI.Apply(cube.GetPrim());rb.CreateSolverPositionIterationCountAttr(24)
        rb.CreateSolverVelocityIterationCountAttr(1)
        UsdPhysics.CollisionAPI.Apply(cube.GetPrim())
        for prim in [cube.GetPrim(),floor.GetPrim()]:
            c=PhysxSchema.PhysxCollisionAPI.Apply(prim);c.CreateContactOffsetAttr(.00025);c.CreateRestOffsetAttr(0.)
        mat=contact_material(s,f'food_{i}_{j}',.25,k,1.6*math.sqrt(k*.000512))
        UsdShade.MaterialBindingAPI.Apply(cube.GetPrim()).Bind(mat,UsdShade.Tokens.weakerThanDescendants,'physics')
        cases.append(dict(path=path,side_mm=side*1000,food_k_N_m=k,dough_k_N_m=1000.,initial_drop_mm=35.))
w=World(stage_units_in_meters=1.,physics_dt=1/480,rendering_dt=1/60,physics_prim_path='/World/physicsScene',backend='warp',device='cuda:0')
w.reset();w.step(render=False)
v=omni.physics.tensors.create_simulation_view('warp',stage_id=UsdUtils.StageCache.Get().GetId(s).ToLongInt())
b=v.create_rigid_body_view(paths);order=[b.prim_paths.index(p) for p in paths]
z=[]
for n in range(360):
    w.step(render=False);z.append(b.get_transforms().numpy()[order,2].copy())
z=np.array(z)
for j,c in enumerate(cases):
    clearance=z[:,j]-.008-c['side_mm']/2000
    impact=int(np.flatnonzero(clearance<.001)[0])
    valley=impact+int(np.argmin(clearance[impact:impact+40]))
    c['max_penetration_mm']=float(max(0,-clearance.min())*1000)
    c['max_rebound_after_impact_mm']=float(max(0,clearance[valley:].max())*1000)
    c['settled_clearance_mm']=float(clearance[-1]*1000)
root=Path(__file__).resolve().parents[2]/'arastirma/3_TOPPING/sucuk_v2'
(root/'contact_bench.json').write_text(json.dumps({'status':'MODEL SANITY ONLY - NOT FOOD CALIBRATION','cases':cases},indent=2))
print('CONTACT_BENCH',json.dumps(cases),flush=True)
app.close()
