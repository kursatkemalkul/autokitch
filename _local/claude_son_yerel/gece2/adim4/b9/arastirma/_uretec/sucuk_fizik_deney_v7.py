"""Physical cube dosing experiment on the latest complete twin. ASCII UI.

8 mm, density 1000 kg/m3 and friction 0.25 are design ASSUMPTIONS,
not measured food properties. Rigid cubes cannot validate deformation/adhesion.
No particles are spawned at the outlet or teleported during simulation.
"""
import argparse, json, math, time
from pathlib import Path
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('--gpu', action='store_true')
ap.add_argument('--count', type=int, default=600)
ap.add_argument('--seconds', type=float, default=20)
ap.add_argument('--direction', type=float, default=1)
ap.add_argument('--gui', action='store_true')
ap.add_argument('--tag', default='test')
ap.add_argument('--rpm', type=float, default=8)
ap.add_argument('--tail', type=float, default=3)
ap.add_argument('--feedback', action='store_true', help='Virtual outlet counter, NOT installed hardware')
ap.add_argument('--stop-g', type=float, default=70)
ap.add_argument('--table-rpm', type=float, default=30)
ap.add_argument('--outer-dwell', type=float, default=1.5)
ap.add_argument('--inner-dwell', type=float, default=0.7)
args = ap.parse_args()
from isaacsim import SimulationApp
app = SimulationApp({'headless': not args.gui, 'width':1280, 'height':800})
import omni.usd
from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, PhysxSchema, Gf
from isaacsim.core.api import World
from omni.physx import get_physx_scene_query_interface

ROOT = Path(__file__).resolve().parents[2]
FIZ = ROOT / 'otonom/hat3d/fizik'
OUT = ROOT / 'arastirma/3_TOPPING/sucuk_fizik_deney_v7'
OUT.mkdir(parents=True, exist_ok=True)
cfg = json.loads((ROOT/'otonom/hat3d/sim_makine.json').read_text(encoding='utf-8'))
T = cfg['tabla']; slot = next(y for y in cfg['yuvalar'] if y['cad']=='sucuk_cad_v7')
T=dict(T, rpm=args.table_rpm, t_dis=args.outer_dwell, t_ic=args.inner_dwell)
MY = '/World/MAKINE/TOPPING'
source = FIZ/'TOPPING_IKIZ_v13.usd'
omni.usd.get_context().open_stage(str(source))
app.update(); app.update()
stage = omni.usd.get_context().get_stage()
stage.SetEditTarget(stage.GetSessionLayer())
assert UsdGeom.GetStageUpAxis(stage)=='Z'
dt = 1/(480 if args.gpu else 240)
scene = UsdPhysics.Scene.Get(stage, '/World/MAKINE/physicsScene')
px = PhysxSchema.PhysxSceneAPI.Apply(scene.GetPrim())
px.CreateEnableGPUDynamicsAttr(args.gpu)
px.CreateEnableCCDAttr(True)
px.CreateBroadphaseTypeAttr('GPU' if args.gpu else 'MBP')
px.CreateTimeStepsPerSecondAttr(240)

# Preserve detailed render meshes; skip distant machine contacts in this experiment.
# Retain every mesh of this cassette, the outlet sleeve, carriage, and turntable.
active = []
for p in stage.Traverse():
    s = str(p.GetPath())
    if p.HasAPI(UsdPhysics.CollisionAPI):
        keep = ('KUP_SUCUK' in s or '/ARABA/' in s or '/TABLA/' in s
                or s.startswith('/World/TEPSI/') or s.startswith('/World/PIDE/')
                or s.endswith('/Zemin'))
        if s.startswith(MY+'/SABIT/') and 'dozaj_kovani' in s and 'SUCUK' in s: keep=True
        UsdPhysics.CollisionAPI(p).CreateCollisionEnabledAttr(keep)
        if keep:
            active.append(s)
            pc = PhysxSchema.PhysxCollisionAPI.Apply(p)
            pc.CreateContactOffsetAttr(0.0004)
            pc.CreateRestOffsetAttr(0)

mat = UsdShade.Material.Define(stage, '/World/SucukContact')
pm = UsdPhysics.MaterialAPI.Apply(mat.GetPrim())
pm.CreateStaticFrictionAttr(0.25); pm.CreateDynamicFrictionAttr(0.25)
pm.CreateRestitutionAttr(0.02)
# Material is deliberately applied on both food and food-contact machine surfaces.
# This makes effective friction explicit; real food coefficients still need measurement.
for path in active:
    if 'KUP_SUCUK' in path:
        UsdShade.MaterialBindingAPI.Apply(stage.GetPrimAtPath(path)).Bind(mat,UsdShade.Tokens.strongerThanDescendants,'physics')
cube_m = 0.008; cube_kg = cube_m**3 * 1000
xc = slot['x']/1000
rng = np.random.default_rng(7)
paths=[]
for i in range(args.count):
    # All cubes start inside the open hopper, above the mixer; Z is vertical.
    ix=i%14; iy=(i//14)%31; iz=i//(14*31)
    v=(xc+(ix-6.5)*0.0088, 0.225+iy*0.0088, 0.478+iz*0.0088)
    assert v[2]+cube_m/2 < 0.620, 'Requested stock exceeds collision-free initial hopper fill'
    path=f'/World/SUCUK_CUBES/cube_{i:05d}'
    xf=UsdGeom.Xform.Define(stage,path)
    xf.AddTranslateOp().Set(Gf.Vec3d(*v))
    c=UsdGeom.Cube.Define(stage,path+'/shape'); c.CreateSizeAttr(cube_m)
    c.CreateDisplayColorAttr([Gf.Vec3f(0.48+float(rng.uniform(0,.1)),.12,.07)])
    UsdPhysics.RigidBodyAPI.Apply(xf.GetPrim())
    UsdPhysics.MassAPI.Apply(xf.GetPrim()).CreateMassAttr(cube_kg)
    rb=PhysxSchema.PhysxRigidBodyAPI.Apply(xf.GetPrim())
    rb.CreateEnableCCDAttr(True)
    rb.CreateSolverPositionIterationCountAttr(16); rb.CreateSolverVelocityIterationCountAttr(1)
    UsdPhysics.CollisionAPI.Apply(c.GetPrim())
    pc=PhysxSchema.PhysxCollisionAPI.Apply(c.GetPrim())
    pc.CreateContactOffsetAttr(.0004); pc.CreateRestOffsetAttr(0)
    UsdShade.MaterialBindingAPI.Apply(c.GetPrim()).Bind(mat,UsdShade.Tokens.weakerThanDescendants,'physics')
    paths.append(path)

body_data=None; body_index={}
def pose(path):
    if body_data is None:
        return UsdGeom.Xformable(stage.GetPrimAtPath(path)).ComputeLocalToWorldTransform(Usd.TimeCode.Default())
    v=body_data[body_index[path]]
    m=Gf.Matrix4d(1)
    m.SetRotate(Gf.Quatd(float(v[6]),Gf.Vec3d(*[float(a) for a in v[3:6]])))
    m.SetTranslateOnly(Gf.Vec3d(*[float(a) for a in v[:3]]))
    return m
def position(path): return np.array(pose(path).ExtractTranslation())
def drive(name,kind,value):
    p=stage.GetPrimAtPath(MY+'/EKLEM_'+name)
    assert p.IsValid(), name
    p.GetAttribute(f'drive:{kind}:physics:targetVelocity').Set(float(value))
def xnow(): return T['baslangic_x']/1000+position(MY+'/ARABA')[0]
offset_mm = abs(T['eksen_z'] - slot['agiz_z'])
def target(t):
    u=np.clip((t-T['t_dis'])/(T['doz_sn']-T['t_dis']-T['t_ic']),0,1)
    r2=T['r_dis']**2+(T['r_ic']**2-T['r_dis']**2)*u
    return xc-math.sqrt(max(0,r2-offset_mm**2))/1000

world=World(stage_units_in_meters=1.,physics_dt=dt,rendering_dt=1/60,physics_prim_path='/World/MAKINE/physicsScene',
            backend='warp' if args.gpu else 'numpy', device='cuda:0' if args.gpu else 'cpu')
actual_gpu=px.GetEnableGPUDynamicsAttr().Get()
print('GPU_ACTUAL',actual_gpu,'dt',dt,flush=True)
assert bool(actual_gpu)==args.gpu, 'Physics backend changed unexpectedly'
print('BUILD',args.count,'cubes;',len(active),'machine contact meshes',flush=True)
stage.Flatten().Export(str(OUT/(args.tag+'_initial.usd')))
world.reset()
import carb, omni.physics.tensors
from omni.physx import get_physx_interface
from omni.physx.bindings._physx import SETTING_UPDATE_TO_USD
motion_paths=paths+[MY+'/ARABA',MY+'/TABLA',MY+'/HELEZON_KUP_SUCUK',MY+'/KARISTIRICI_KUP_SUCUK','/World/TEPSI','/World/PIDE']
world.step(render=args.gui)
from pxr import UsdUtils
stage_id=UsdUtils.StageCache.Get().GetId(stage).ToLongInt()
sim_view=omni.physics.tensors.create_simulation_view('warp' if args.gpu else 'numpy', stage_id=stage_id)
body_view=sim_view.create_rigid_body_view(motion_paths)
body_index={p:i for i,p in enumerate(body_view.prim_paths)}
assert set(motion_paths)<=set(body_index)
order=[body_index[p] for p in motion_paths]
def read_bodies():
    data=body_view.get_transforms()
    return data.numpy().copy() if args.gpu else data.copy()
body_data=read_bodies()
if not args.gui: carb.settings.get_settings().set(SETTING_UPDATE_TO_USD,False)
def step():
    global body_data
    world.step(render=False)
    if args.gui: world.render()
    body_data=read_bodies()
for _ in range(480): step()
query=get_physx_scene_query_interface()
rays=[]
for xx in [xc-.024,xc+.024]:
    for yy in [.25,.30,.35,.40,.45,.49]:
        hit=query.raycast_closest([xx,yy,.38],[0,0,-1],.15)
        rays.append({'x':xx,'y':yy,'hit':str(hit)})
print('RAYS',json.dumps(rays),flush=True)
# Bring actual driven table under this nozzle. No product is moved by script.
for _ in range(240*15):
    err=target(0)-xnow()
    drive('X','linear',np.clip(12*err,-.2,.2)); step()
    if abs(err)<.0005: break
drive('X','linear',0)
for _ in range(120):step()
print('READY table',xnow(),'pide',position('/World/PIDE').tolist(),flush=True)
frames=[]; rotations=[]; times=[]; diagnostics=[]; emitted=set(); start=time.time()
motion_paths=paths+[MY+'/ARABA',MY+'/TABLA',MY+'/HELEZON_KUP_SUCUK',MY+'/KARISTIRICI_KUP_SUCUK','/World/TEPSI','/World/PIDE']
def snapshot():
    d=body_data[order]
    return d[:,:3].copy(),d[:,[6,3,4,5]].copy()
xyz0,_=snapshot()
preleak=set(np.flatnonzero(xyz0[:args.count,2]<.160).tolist())
prev=xyz0[:args.count].copy()
stopped_at=None

drive('TABLA','angular',T['rpm']*6)
drive('HELEZON_KUP_SUCUK','angular',args.direction*args.rpm*6)
drive('KARISTIRICI_KUP_SUCUK','angular',args.direction*24)
for n in range(round((args.seconds+args.tail)/dt)):
    t=n*dt
    if stopped_at is not None and t>=stopped_at+args.tail: break
    if stopped_at is None and (t >= args.seconds or (args.feedback and len(emitted)*cube_kg*1000 >= args.stop_g)):
        stopped_at=t
        drive('HELEZON_KUP_SUCUK','angular',0)
        drive('KARISTIRICI_KUP_SUCUK','angular',0)
    # Follow cumulative discharged mass only in explicit virtual-feedback mode.
    phase=min(T['doz_sn'],len(emitted)*cube_kg*1000/slot['doz_g']*T['doz_sn']) if args.feedback else t*T['doz_sn']/args.seconds
    drive('X','linear',np.clip(12*(target(phase)-xnow()),-.05,.05))
    step()
    if n%24==0:
        all_xyz,quat=snapshot()
        xyz=all_xyz[:args.count]
        # Count actual nozzle crossings, not leaked particles reaching the floor elsewhere.
        crossing=(prev[:,2]>=.160)&(xyz[:,2]<.160)&(abs(xyz[:,0]-xc)<.04)&(abs(xyz[:,1]+slot['agiz_z']/1000)<.04)
        emitted.update(np.flatnonzero(crossing).tolist())
        prev=xyz.copy()
        pp=position('/World/PIDE')
        rr=np.linalg.norm(xyz[:,:2]-pp[:2],axis=1)
        on=(rr<.140)&(xyz[:,2]>pp[2])&(xyz[:,2]<pp[2]+.04)
        frames.append(all_xyz);rotations.append(quat);times.append(t)
        diag={'t':round(t,3),'emitted_g':len(emitted)*cube_kg*1000,
              'on_pide_g':int(on.sum())*cube_kg*1000,'cube_z_min':float(xyz[:,2].min()),
              'cube_z_max':float(xyz[:,2].max()),'table_x':xnow(),'pide':pp.tolist(),
              'outside_or_below_g':int(((xyz[:,2]<.160)&~on).sum())*cube_kg*1000,
              'stopped_at':stopped_at,'screw_quat':str(pose(MY+'/HELEZON_KUP_SUCUK').ExtractRotationQuat())}
        diagnostics.append(diag)
        if n%240==0: print('MEASURE',json.dumps(diag),flush=True)
for name,kind in [('X','linear'),('TABLA','angular'),('HELEZON_KUP_SUCUK','angular'),('KARISTIRICI_KUP_SUCUK','angular')]:drive(name,kind,0)
last_xyz=np.array(frames[-1])[:args.count]
pp=position('/World/PIDE')
radius=np.linalg.norm(last_xyz[:,:2]-pp[:2],axis=1)
on=(radius<.140)&(last_xyz[:,2]>pp[2])&(last_xyz[:,2]<pp[2]+.020)
edges=np.sqrt(np.linspace(0,.125**2,6))
rings=np.histogram(radius[on],edges)[0]
report={'initial_stock_g':args.count*cube_kg*1000,'pre_dose_leak_g':len(preleak)*cube_kg*1000,
        'gpu_requested':args.gpu,'gpu_actual':actual_gpu,'dt':dt,'rpm':args.rpm,'table_rpm':T['rpm'],'outer_dwell':T['t_dis'],'inner_dwell':T['t_ic'],'feedback_is_virtual':args.feedback,'stopped_at':stopped_at,
        'nozzle_offset_mm':offset_mm,'equal_area_ring_counts':rings.tolist(),
        'ring_cv_percent':float(np.std(rings)/max(1,np.mean(rings))*100),
        'source':str(source),'assumptions':{'cube_mm':8,'density_kg_m3':1000,'friction':.25,'rigid_food':True,'ccd':bool(px.GetEnableCCDAttr().Get()),'cassette_contact_friction':.25},
        'target_g':slot['doz_g'],'count':args.count,'direction':args.direction,'wall_seconds':time.time()-start,
        'rays':rays,'measurements':diagnostics,'last':diagnostics[-1]}
(OUT/(args.tag+'.json')).write_text(json.dumps(report,indent=2),encoding='utf-8')
np.savez_compressed(OUT/(args.tag+'.npz'),time=times,xyz=frames,quat=rotations,paths=motion_paths)
get_physx_interface().update_transformations(True,True,True,False)
stage.Flatten().Export(str(OUT/(args.tag+'.usd')))
print('FINISHED',json.dumps(report['last']),flush=True)
app.close()










