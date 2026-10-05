"""Isolated detailed two-cassette assembly; leaves source USD/web untouched."""
import json, math, hashlib
import numpy as np
if __name__=='__main__':
    from isaacsim import SimulationApp
    app=SimulationApp({'headless':True})
from pxr import Usd,UsdGeom,UsdPhysics,UsdShade,PhysxSchema,Gf,Sdf
from topping_lab_config import ROOT,OUT,MY,PRODUCTS
from sucuk_v2_sahne import contact_material,closed_meshes as sucuk_meshes
from kasar_v2_sahne import closed_meshes as kasar_meshes

SOURCE=ROOT/'otonom/hat3d/fizik/TOPPING_IKIZ_v13.usd'

def build(variant='candidate'):
    OUT.mkdir(parents=True,exist_ok=True)
    path=OUT/f'TOPPING_LAB_v1_{variant}.usd'
    source=Usd.Stage.Open(str(SOURCE))
    # A separate layer, never an edit of the original scene.
    stage=Usd.Stage.CreateNew(str(path)) if not path.exists() else Usd.Stage.Open(str(path))
    stage.GetRootLayer().Clear();stage.GetRootLayer().subLayerPaths=[str(SOURCE)]
    UsdGeom.SetStageUpAxis(stage,UsdGeom.Tokens.z)
    UsdGeom.SetStageMetersPerUnit(stage,1.)
    removed=[]
    def remove(p):removed.append(str(p.GetPath()));p.SetActive(False)
    keep={'ARABA','TABLA','SABIT','EKLEM_X','EKLEM_TABLA'}
    for product in PRODUCTS.values():
        for stem in ('HELEZON_','KARISTIRICI_'):
            keep.update([stem+product['slot'],'EKLEM_'+stem+product['slot']])
    for p in list(stage.GetPrimAtPath(MY).GetChildren()):
        if p.GetName() not in keep:remove(p)
    table_prefix=('mekanizma_teknesi','ray_kirisi_','kayis_kirisi','baglama_lamasi_',
        'lineer_ray_','x_tahrik_','x_motor','avara_','x_kayisi_','ray_ortu_',
        'kirinti_','enerji_zinciri_','x_home_','x_limit_','uc_tamponu_')
    for p in list(stage.GetPrimAtPath(MY+'/SABIT').GetChildren()):
        n=p.GetName()
        if not ('KASAR_KABI' in n or 'KUP_SUCUK' in n or n.startswith(table_prefix)):remove(p)
    # Remove distant station/robot geometry, if any source revision adds it.
    for p in list(stage.GetPrimAtPath('/World').GetChildren()):
        if p.GetName() not in ('MAKINE','TEPSI','PIDE','CarpismaGrubu_URUN'):remove(p)
    geometry={}
    for product,p in PRODUCTS.items():
        machine=contact_material(stage,product+'_machine',p['mu'])
        for prim in stage.Traverse():
            if p['slot'] in str(prim.GetPath()) and prim.HasAPI(UsdPhysics.CollisionAPI):
                UsdShade.MaterialBindingAPI.Apply(prim).Bind(machine,UsdShade.Tokens.strongerThanDescendants,'physics')
        geometry[product]=(kasar_meshes if product=='kasar' else sucuk_meshes)(stage,variant,machine)
        for stem in ('HELEZON_','KARISTIRICI_'):
            joint=stage.GetPrimAtPath(MY+'/EKLEM_'+stem+p['slot'])
            joint.GetAttribute('drive:angular:physics:targetVelocity').Set(0.)
            joint.GetAttribute('drive:angular:physics:maxForce').Set(5.)
    # Start on LEFT by changing the initial body configuration only. The rail
    # and joints stay at their original world coordinates and travel limits.
    for name in ('ARABA','TABLA'):
        xf=UsdGeom.Xformable(stage.GetPrimAtPath(MY+'/'+name));xf.ClearXformOpOrder()
        xf.AddTranslateOp().Set(Gf.Vec3d(-.680,0,0))
    for name in ('TEPSI','PIDE'):
        xf=UsdGeom.Xformable(stage.GetPrimAtPath('/World/'+name))
        op=xf.GetOrderedXformOps()[0];v=op.Get();op.Set(Gf.Vec3d(.220,v[1],v[2]))
    dough=contact_material(stage,'dough',.5,1000.,1.6*math.sqrt(1000*.000176))
    for p in stage.Traverse():
        if str(p.GetPath()).startswith('/World/PIDE/') and p.HasAPI(UsdPhysics.CollisionAPI):
            UsdShade.MaterialBindingAPI.Apply(p).Bind(dough,UsdShade.Tokens.strongerThanDescendants,'physics')
        if p.HasAPI(UsdPhysics.CollisionAPI):
            pc=PhysxSchema.PhysxCollisionAPI.Apply(p);pc.CreateRestOffsetAttr(0.);pc.CreateContactOffsetAttr(.0002)
    # Explicit catch floor; lost product remains physical and countable.
    oldfloor=stage.GetPrimAtPath('/World/MAKINE/Zemin')
    if oldfloor:oldfloor.SetActive(False)
    floor=UsdGeom.Cube.Define(stage,'/World/LabFloor');floor.CreateSizeAttr(1.)
    floor.AddTranslateOp().Set(Gf.Vec3d(.9,.3,-.025));floor.AddScaleOp().Set(Gf.Vec3f(3,2,.02))
    floor.CreateDisplayColorAttr([Gf.Vec3f(.16,.18,.21)])
    UsdPhysics.CollisionAPI.Apply(floor.GetPrim())
    scene=PhysxSchema.PhysxSceneAPI.Apply(stage.GetPrimAtPath('/World/MAKINE/physicsScene'))
    scene.CreateEnableGPUDynamicsAttr(True);scene.CreateBroadphaseTypeAttr('GPU')
    scene.CreateTimeStepsPerSecondAttr(480);scene.CreateEnableCCDAttr(False)
    scene.CreateGpuMaxRigidContactCountAttr(4*1024*1024)
    scene.CreateGpuMaxRigidPatchCountAttr(512*1024)
    scene.CreateGpuFoundLostPairsCapacityAttr(4*1024*1024)
    scene.CreateGpuTotalAggregatePairsCapacityAttr(4*1024*1024)
    for name,kind in [('X','linear'),('TABLA','angular')]:
        stage.GetPrimAtPath(MY+'/EKLEM_'+name).GetAttribute(f'drive:{kind}:physics:targetVelocity').Set(0.)
    stage.GetRootLayer().Save()
    audit=dict(source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),variant=variant,removed=removed,
        geometry=geometry,initial_table_x=.220,slot_x={k:p['x'] for k,p in PRODUCTS.items()},
        live_physics=True,limitations=['No cooling cabinet/other cassettes/robot in this test fixture.',
        'Tray seating/contact proxy inherited; not verified fabrication geometry.',
        'Source motor torque limits are catalogue ceilings, not thermal/speed curves.'])
    (OUT/f'assembly_{variant}.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
    print('LAB_SCENE_READY',path,len(removed),'prims excluded',flush=True)
    return path

def _author_food(stage,product,data,progress=None):
    p=PRODUCTS[product];mat=contact_material(stage,product+'_food',p['mu'],p['stiffness'],1.6*math.sqrt(p['stiffness']*p['nominal_particle_kg']))
    paths=[]
    for i,(v,d,mass) in enumerate(zip(data['points'],data['dimensions'],data['mass_kg'])):
        path=f'/World/FOOD_{product}/p_{i:06d}'
        xf=UsdGeom.Xform.Define(stage,path);xf.AddTranslateOp().Set(Gf.Vec3d(*v))
        c=UsdGeom.Cube.Define(stage,path+'/shape');c.CreateSizeAttr(1.)
        c.AddScaleOp().Set(Gf.Vec3f(*d.tolist()))
        c.CreateDisplayColorAttr([Gf.Vec3f(*((.95,.81,.38) if product=='kasar' else (.55,.13,.07)))])
        UsdPhysics.RigidBodyAPI.Apply(xf.GetPrim());UsdPhysics.MassAPI.Apply(xf.GetPrim()).CreateMassAttr(float(mass))
        rb=PhysxSchema.PhysxRigidBodyAPI.Apply(xf.GetPrim());rb.CreateSolverPositionIterationCountAttr(24);rb.CreateSolverVelocityIterationCountAttr(1)
        UsdPhysics.CollisionAPI.Apply(c.GetPrim())
        pc=PhysxSchema.PhysxCollisionAPI.Apply(c.GetPrim());pc.CreateContactOffsetAttr(.00015);pc.CreateRestOffsetAttr(0.)
        UsdShade.MaterialBindingAPI.Apply(c.GetPrim()).Bind(mat,UsdShade.Tokens.weakerThanDescendants,'physics')
        paths.append(path)
        if progress and i%1000==0:progress(product,i,len(data['mass_kg']))
    return paths

def add_food(stage,product,data,progress=None):
    """Batch-copy identical USD schemas, retaining one REAL body per piece.

    Only Sdf APIs run inside ChangeBlock: no stale Usd composition queries.
    Each body's position, dimensions and mass remain individual. This is not
    a merged lump or a particle-instancer approximation.
    """
    count=len(data['mass_kg'])
    if not count:return []
    first={k:data[k][:1] for k in ('points','dimensions','mass_kg')}
    paths=_author_food(stage,product,first)
    layer=stage.GetRootLayer();template=paths[0]
    for start in range(1,count,1000):
        with Sdf.ChangeBlock():
            for i in range(start,min(start+1000,count)):
                path=f'/World/FOOD_{product}/p_{i:06d}'
                Sdf.CopySpec(layer,template,layer,path)
                layer.GetAttributeAtPath(path+'.xformOp:translate').default=Gf.Vec3d(*data['points'][i])
                layer.GetAttributeAtPath(path+'.physics:mass').default=float(data['mass_kg'][i])
                layer.GetAttributeAtPath(path+'/shape.xformOp:scale').default=Gf.Vec3f(*data['dimensions'][i].tolist())
                paths.append(path)
        if progress:progress(product,min(start+1000,count),count)
    assert stage.GetPrimAtPath(paths[-1]).IsValid()
    return paths

if __name__=='__main__':
    build('candidate');build('baseline')
    app.close()
