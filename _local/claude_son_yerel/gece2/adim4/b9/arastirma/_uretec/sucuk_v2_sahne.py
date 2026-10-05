"""V2 experiment utilities: closed SDF geometry and variable food sizes.

All food/contact numerical properties below are assumptions, not calibration.
"""
from pathlib import Path
import math, json, re
import numpy as np
from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, PhysxSchema, Gf, Vt, Sdf

ROOT=Path(__file__).resolve().parents[2]
CAD=ROOT/'arastirma/3_TOPPING/sucuk_v2/cad'
MY='/World/MAKINE/TOPPING'

def contact_material(stage,name,mu,k=0.,damping=0.):
    mat=UsdShade.Material.Define(stage,'/World/V2Materials/'+name)
    pm=UsdPhysics.MaterialAPI.Apply(mat.GetPrim())
    pm.CreateStaticFrictionAttr(mu);pm.CreateDynamicFrictionAttr(mu)
    pm.CreateRestitutionAttr(.02)
    px=PhysxSchema.PhysxMaterialAPI.Apply(mat.GetPrim())
    px.CreateFrictionCombineModeAttr('average')
    px.CreateCompliantContactStiffnessAttr(float(k))
    px.CreateCompliantContactDampingAttr(float(damping))
    return mat

def closed_meshes(stage,variant,physics_mat):
    data=np.load(CAD/('relieved_meshes.npz' if variant=='relieved' else 'closed_meshes.npz'))
    screw=MY+'/HELEZON_KUP_SUCUK'
    old=[]
    for p in stage.Traverse():
        path=str(p.GetPath())
        if path.startswith(screw+'/') and re.search(r'helezon_[ABCD]_d\d+',p.GetName()):
            UsdPhysics.CollisionAPI(p).CreateCollisionEnabledAttr(False)
            old.append(path)
            if variant=='relieved' or (variant=='candidate' and re.search('helezon_D_d',p.GetName())):
                UsdGeom.Imageable(p).MakeInvisible()
    assert len(old)>20,'Original flight chunk names not found'
    group=next(p for p in stage.Traverse() if p.IsA(UsdPhysics.CollisionGroup) and p.GetName()=='CarpismaGrubu_MAKINE')
    col=UsdPhysics.CollisionGroup(group).GetCollidersCollectionAPI()
    new=[]
    keys=['baseline_A','baseline_B','baseline_C', 'candidate_D' if variant=='candidate' else 'baseline_D']
    if variant=='candidate':keys.append('candidate_tube')
    if variant=='relieved':keys=['relieved_'+c for c in 'ABCD']+['relieved_tube']
    for key in keys:
        dynamic=not key.endswith('_tube')
        path=(screw if dynamic else MY+'/SABIT')+'/V2_'+key
        m=UsdGeom.Mesh.Define(stage,path)
        m.CreatePointsAttr(Vt.Vec3fArray.FromNumpy(data[key+'_V']))
        f=data[key+'_F'];m.CreateFaceVertexCountsAttr([3]*len(f))
        m.CreateFaceVertexIndicesAttr(Vt.IntArray.FromNumpy(f.ravel()))
        m.CreateSubdivisionSchemeAttr('none')
        UsdPhysics.CollisionAPI.Apply(m.GetPrim())
        mc=UsdPhysics.MeshCollisionAPI.Apply(m.GetPrim())
        mc.CreateApproximationAttr('sdf' if dynamic else 'none')
        if dynamic:
            sdf=PhysxSchema.PhysxSDFMeshCollisionAPI.Apply(m.GetPrim())
            sdf.CreateSdfResolutionAttr(256)
            sdf.CreateSdfSubgridResolutionAttr(6)
        pc=PhysxSchema.PhysxCollisionAPI.Apply(m.GetPrim())
        pc.CreateContactOffsetAttr(.0004);pc.CreateRestOffsetAttr(0.)
        col.CreateIncludesRel().AddTarget(path)
        UsdShade.MaterialBindingAPI.Apply(m.GetPrim()).Bind(physics_mat,UsdShade.Tokens.strongerThanDescendants,'physics')
        if key=='candidate_D' or (variant=='relieved' and dynamic):
            m.CreateDisplayColorAttr([Gf.Vec3f(.16,.45,.75)])
        else:m.CreateVisibilityAttr('invisible')
        new.append(path)
    if variant in ('candidate','relieved'):
        audit=json.loads((CAD/'cad_checks.json').read_text())
        mass=UsdPhysics.MassAPI(stage.GetPrimAtPath(screw))
        old_mass=mass.GetMassAttr().Get()
        delta=(audit['candidate_D']['cad_volume_mm3']-audit['baseline_D']['cad_volume_mm3'])*1.41e-6
        if variant=='relieved':
            ra=json.loads((CAD/'relieved_checks.json').read_text())
            delta=sum(ra['relieved_'+c]['volume_mm3']-audit['baseline_'+c]['cad_volume_mm3'] for c in 'ABCD')*1.41e-6
        mass.CreateMassAttr(float(old_mass+delta))
        found=[]
        for p in stage.Traverse():
            if p.GetName()=='KUP_SUCUK_cikis_tupu':
                UsdPhysics.CollisionAPI(p).CreateCollisionEnabledAttr(False)
                UsdGeom.Imageable(p).MakeInvisible();found.append(str(p.GetPath()))
        assert len(found)==1,found
        # New tube gets original transparent material for inspection.
        m=UsdGeom.Mesh(stage.GetPrimAtPath(MY+'/SABIT/V2_'+('relieved_tube' if variant=='relieved' else 'candidate_tube')))
        m.CreateVisibilityAttr('inherited')
        oldmat=UsdShade.MaterialBindingAPI(stage.GetPrimAtPath(found[0])).ComputeBoundMaterial()[0]
        if oldmat:UsdShade.MaterialBindingAPI.Apply(m.GetPrim()).Bind(oldmat)
    return {'removed_open_chunk_colliders':len(old),'new_closed_colliders':new,'sdf_resolution':256,'variant':variant}

def food_pack(args):
    rng=np.random.default_rng(args.seed)
    sizes=[];masses=[]
    if args.stock_g>0:
        while sum(masses)*1000<args.stock_g:
            s=float(rng.triangular(.006,.008,.010)) if args.mixed else .008
            sizes.append(s);masses.append(s**3*1000.)
    else:
        sizes=(rng.triangular(.006,.008,.010,args.count) if args.mixed else np.full(args.count,.008)).tolist()
        masses=(np.array(sizes)**3*1000.).tolist()
    # Collision-free shelf packing inside upper hopper. No runtime emission/spawn.
    points=[];i=0;z=.474;gap=.00015
    while i<len(sizes):
        y=.212;layer_h=0.
        while i<len(sizes):
            row=[];width=0.;row_h=0.;j=i
            while j<len(sizes) and width+sizes[j]<=.130:
                s=sizes[j];row.append(s);width+=s+gap;row_h=max(row_h,s);j+=1
            if y+row_h>.515:break
            if z+max(layer_h,row_h)>.610:
                raise ValueError('Initial stock will not fit above mixer without overlap; use staged loading')
            x=1.4725-(width-gap)/2
            for s in row:
                points.append([x+s/2,y+s/2,z+s/2]);x+=s+gap
            y+=row_h+gap;layer_h=max(layer_h,row_h);i=j
        assert layer_h>0
        z+=layer_h+gap
    return np.array(sizes),np.array(masses),np.array(points)

def food_geometry(stage,args,mat):
    sizes,masses,points=food_pack(args)
    rng=np.random.default_rng(args.seed+1);paths=[]
    for i,(side,mass,pos) in enumerate(zip(sizes,masses,points)):
        path=f'/World/SUCUK_CUBES/cube_{i:05d}'
        xf=UsdGeom.Xform.Define(stage,path);xf.AddTranslateOp().Set(Gf.Vec3d(*pos))
        c=UsdGeom.Cube.Define(stage,path+'/shape');c.CreateSizeAttr(float(side))
        c.CreateDisplayColorAttr([Gf.Vec3f(.48+float(rng.uniform(0,.1)),.12,.07)])
        UsdPhysics.RigidBodyAPI.Apply(xf.GetPrim())
        UsdPhysics.MassAPI.Apply(xf.GetPrim()).CreateMassAttr(float(mass))
        rb=PhysxSchema.PhysxRigidBodyAPI.Apply(xf.GetPrim())
        rb.CreateEnableCCDAttr(True);rb.CreateSolverPositionIterationCountAttr(24)
        rb.CreateSolverVelocityIterationCountAttr(1)
        UsdPhysics.CollisionAPI.Apply(c.GetPrim())
        pc=PhysxSchema.PhysxCollisionAPI.Apply(c.GetPrim())
        pc.CreateContactOffsetAttr(.00025);pc.CreateRestOffsetAttr(0.)
        UsdShade.MaterialBindingAPI.Apply(c.GetPrim()).Bind(mat,UsdShade.Tokens.weakerThanDescendants,'physics')
        paths.append(path)
    return paths,sizes,masses
