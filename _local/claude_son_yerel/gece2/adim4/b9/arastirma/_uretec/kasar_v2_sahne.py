"""Closed screw SDFs and short-shred cheese for the isolated Kasar experiment.

No outlet spawning. Shreds are rigid rectangular proxies, not deformable food.
All friction, density, compliance and dimensional distributions are VARSAYIM.
"""
from pathlib import Path
import json, re
import numpy as np
from pxr import UsdGeom, UsdPhysics, UsdShade, PhysxSchema, Gf, Vt
from sucuk_v2_sahne import contact_material
ROOT=Path(__file__).resolve().parents[2]
CAD=ROOT/'arastirma/3_TOPPING/kasar_v2/cad'
MY='/World/MAKINE/TOPPING'

def closed_meshes(stage,variant,physics_mat):
    data=np.load(CAD/('baseline_meshes.npz' if variant=='baseline' else 'closed_meshes.npz'))
    screw=MY+'/HELEZON_KASAR_KABI';old=[]
    assert stage.GetPrimAtPath(screw).IsValid(),screw
    for p in stage.Traverse():
        if str(p.GetPath()).startswith(screw+'/') and re.search(r'helezon_[ABCD]_d\d+',p.GetName()):
            UsdPhysics.CollisionAPI(p).CreateCollisionEnabledAttr(False)
            old.append(str(p.GetPath()))
            if variant=='candidate' and re.search('helezon_[BCD]_d',p.GetName()):UsdGeom.Imageable(p).MakeInvisible()
    assert len(old)>20,old
    group=next(p for p in stage.Traverse() if p.IsA(UsdPhysics.CollisionGroup) and p.GetName()=='CarpismaGrubu_MAKINE')
    col=UsdPhysics.CollisionGroup(group).GetCollidersCollectionAPI()
    prefixes=['baseline_A']+[(('candidate_' if variant=='candidate' else 'baseline_')+c) for c in 'BCD']
    if variant=='candidate':prefixes.append('candidate_tube')
    keys=[k[:-2] for k in data.files if k.endswith('_V') and any(k[:-2]==p or k[:-2].startswith(p+'_s') for p in prefixes)]
    for key in keys:
        dynamic=key!='candidate_tube'
        path=(screw if dynamic else MY+'/SABIT')+'/KASAR_V2_'+key
        m=UsdGeom.Mesh.Define(stage,path)
        m.CreatePointsAttr(Vt.Vec3fArray.FromNumpy(data[key+'_V']))
        f=data[key+'_F'];m.CreateFaceVertexCountsAttr([3]*len(f))
        m.CreateFaceVertexIndicesAttr(Vt.IntArray.FromNumpy(f.ravel()));m.CreateSubdivisionSchemeAttr('none')
        UsdPhysics.CollisionAPI.Apply(m.GetPrim())
        UsdPhysics.MeshCollisionAPI.Apply(m.GetPrim()).CreateApproximationAttr('sdf' if dynamic else 'none')
        if dynamic:
            sdf=PhysxSchema.PhysxSDFMeshCollisionAPI.Apply(m.GetPrim())
            sdf.CreateSdfResolutionAttr(256);sdf.CreateSdfSubgridResolutionAttr(6)
        pc=PhysxSchema.PhysxCollisionAPI.Apply(m.GetPrim())
        pc.CreateContactOffsetAttr(.0002);pc.CreateRestOffsetAttr(0.)
        col.CreateIncludesRel().AddTarget(path)
        UsdShade.MaterialBindingAPI.Apply(m.GetPrim()).Bind(physics_mat,UsdShade.Tokens.strongerThanDescendants,'physics')
        if key.startswith('candidate_'):m.CreateDisplayColorAttr([Gf.Vec3f(.16,.45,.75)])
        else:m.CreateVisibilityAttr('invisible')
    if variant=='candidate':
        oldtube=stage.GetPrimAtPath(MY+'/SABIT/KASAR_KABI_cikis_tupu')
        assert oldtube.IsValid()
        UsdPhysics.CollisionAPI(oldtube).CreateCollisionEnabledAttr(False)
        UsdGeom.Imageable(oldtube).MakeInvisible()
        oldmat=UsdShade.MaterialBindingAPI(oldtube).ComputeBoundMaterial()[0]
        if oldmat:UsdShade.MaterialBindingAPI.Apply(stage.GetPrimAtPath(MY+'/SABIT/KASAR_V2_candidate_tube')).Bind(oldmat)
        audit=json.loads((CAD/'cad_checks.json').read_text())['meshes']
        mass=UsdPhysics.MassAPI(stage.GetPrimAtPath(screw))
        delta=sum((sum(v['volume_mm3'] for k,v in audit.items() if k=='candidate_'+c or k.startswith('candidate_'+c+'_s'))-
                   sum(v['volume_mm3'] for k,v in audit.items() if k=='baseline_'+c or k.startswith('baseline_'+c+'_s')))*1.41e-6 for c in 'BCD')
        mass.CreateMassAttr(float(mass.GetMassAttr().Get()+delta))
    import hashlib
    filepath=CAD/('baseline_meshes.npz' if variant=='baseline' else 'closed_meshes.npz')
    return dict(removed_chunk_colliders=len(old),new_closed_colliders=keys,sdf_resolution=256,variant=variant,
        cad_mesh_sha256=hashlib.sha256(filepath.read_bytes()).hexdigest())

def food_pack(args):
    rng=np.random.default_rng(args.seed);dims=[];masses=[]
    while sum(masses)*1000<args.stock_g:
        d=np.array([rng.triangular(.003,.004,.005),rng.triangular(.006,.010,.014),rng.triangular(.003,.004,.005)])
        dims.append(d);masses.append(float(np.prod(d)*1100.))
    # Shelf packing entirely above the mixer envelope (top ~585 mm).
    # This deliberately limits initial stock rather than overlapping geometry
    # or replacing many real shreds with oversized lumps.
    points=[];i=0;z=.586;gap=.0002
    while i<len(dims):
        y=.212;layer_h=0.
        while i<len(dims):
            row=[];width=0.;depth=0.;height=0.;j=i
            while j<len(dims) and width+dims[j][0]<=.260:
                d=dims[j];row.append(d);width+=d[0]+gap;depth=max(depth,d[1]);height=max(height,d[2]);j+=1
            if y+depth>.514:break
            if z+height>.610:raise ValueError('Stock does not fit initial non-overlapping upper volume; staged loading required')
            x=1.2575-(width-gap)/2
            for d in row:
                points.append([x+d[0]/2,y+d[1]/2,z+d[2]/2]);x+=d[0]+gap
            i=j;y+=depth+gap;layer_h=max(layer_h,height)
        assert layer_h>0
        z+=layer_h+gap
    return np.array(dims),np.array(masses),np.array(points)

def food_geometry(stage,args,mat):
    dims,masses,points=food_pack(args);rng=np.random.default_rng(args.seed+1);paths=[]
    for i,(d,mass,pos) in enumerate(zip(dims,masses,points)):
        path=f'/World/KASAR_SHREDS/shred_{i:05d}'
        xf=UsdGeom.Xform.Define(stage,path);xf.AddTranslateOp().Set(Gf.Vec3d(*pos))
        c=UsdGeom.Cube.Define(stage,path+'/shape');c.CreateSizeAttr(1.)
        c.AddScaleOp().Set(Gf.Vec3f(*d.tolist()))
        c.CreateDisplayColorAttr([Gf.Vec3f(.95,.78+float(rng.uniform(0,.08)),.38)])
        UsdPhysics.RigidBodyAPI.Apply(xf.GetPrim());UsdPhysics.MassAPI.Apply(xf.GetPrim()).CreateMassAttr(float(mass))
        rb=PhysxSchema.PhysxRigidBodyAPI.Apply(xf.GetPrim())
        rb.CreateSolverPositionIterationCountAttr(24);rb.CreateSolverVelocityIterationCountAttr(1)
        UsdPhysics.CollisionAPI.Apply(c.GetPrim())
        pc=PhysxSchema.PhysxCollisionAPI.Apply(c.GetPrim());pc.CreateContactOffsetAttr(.00015);pc.CreateRestOffsetAttr(0.)
        UsdShade.MaterialBindingAPI.Apply(c.GetPrim()).Bind(mat,UsdShade.Tokens.weakerThanDescendants,'physics')
        paths.append(path)
    return paths,dims,masses
