"""Kasar V2 / CAD v15: isolated end-flight design, all v14 parts preserved.

Candidate, not manufacturing release. Never writes production or web files.
Run with system Python containing CadQuery.
"""
from pathlib import Path
import csv, hashlib, json, math
import numpy as np
from scipy.spatial import cKDTree
import cadquery as cq
from OCP.BRepMesh import BRepMesh_IncrementalMesh
import kasar_cad_v14 as old

ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'arastirma/3_TOPPING/kasar_kabi_v14/step'
OUT=ROOT/'arastirma/3_TOPPING/kasar_v2/cad'
OUT.mkdir(parents=True,exist_ok=True)
CY=old.CY
OFFSET=np.array([1257.5,260.,-362.5])
report={'revision':'kasar_v2_CAD_v15','source':'kasar_cad_v14','parts':{},'meshes':{}}
arrays={}

def mesh(name,shape,tol=.01,angular=.08):
    assert shape.isValid() and shape.Volume()>0,name
    if len(shape.Solids())>1:
        for i,s in enumerate(shape.Solids()):mesh(name+'_s'+str(i),s,tol,angular)
        return
    copied=shape.copy()
    # CadQuery mesh() uses relative tolerance. Here accuracy is explicitly mm.
    BRepMesh_IncrementalMesh(copied.wrapped,tol,False,angular,True).Perform()
    vv,ff=copied.tessellate(tol+1e-6,angular)
    raw=np.array([v.toTuple() for v in vv]);f=np.array(ff,dtype=np.int32)
    v,inv=np.unique(np.round(raw,7),axis=0,return_inverse=True)
    # CAD face seams can straddle any decimal grid. Weld only coincident
    # vertices within 0.0001 mm; never fill an actual hole in the flight.
    parent=np.arange(len(v))
    def root(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    pairs=cKDTree(v).query_pairs(.0001,output_type='ndarray')
    for a,b in pairs:parent[root(int(b))]=root(int(a))
    mapping=np.array([root(i) for i in range(len(v))])
    f=mapping[inv[f]];f=f[np.array([len(set(t))==3 for t in f])]
    _,unique_faces=np.unique(np.sort(f,axis=1),axis=0,return_index=True)
    f=f[np.sort(unique_faces)]
    edges=np.sort(np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1)
    _,counts=np.unique(edges,axis=0,return_counts=True)
    vol=float(np.einsum('ij,ij->i',v[f[:,0]],np.cross(v[f[:,1]],v[f[:,2]])).sum()/6)
    if vol<0:f=f[:,[0,2,1]];vol=-vol
    # Adaptive integration is essential for BSpline flight faces. Default
    # non-adaptive CAD volume was 1.35% low on the original A STEP.
    true_volume=shape.Volume(tol=1e-7)
    err=abs(vol-true_volume)/true_volume
    assert np.all(counts==2),(name,'open mesh',int(sum(counts!=2)))
    if err>=.001 and tol>.005:
        print('REFINE_MESH',name,err,tol,flush=True)
        return mesh(name,shape,.005,.06)
    assert err<.001,(name,err,vol,shape.Volume())
    p=(v+OFFSET)*.001;p=np.column_stack([p[:,0],-p[:,2],p[:,1]])
    arrays[name+'_V']=p.astype(np.float32);arrays[name+'_F']=f
    report['meshes'][name]=dict(valid=True,closed=True,volume_mm3=true_volume,
        legacy_nonadaptive_volume_mm3=shape.Volume(),mesh_volume_mm3=vol,
        mesh_volume_error=err,triangles=len(f),seam_weld_limit_mm=.0001,seam_pairs=len(pairs),bbox_mm=[v.min(0).tolist(),v.max(0).tolist()])
    print('CLOSED_MESH',name,len(f),err,flush=True)

parts={p.stem:cq.importers.importStep(str(p)).val() for p in sorted(SRC.glob('*.step'))
       if p.stem!='helezon_TEK_PARCA'}
for c in 'ABCD':mesh('baseline_'+c,parts['helezon_'+c])
np.savez_compressed(OUT/'baseline_meshes.npz',**arrays)

# The inherited B/C STEP contains shaft and flight as separate solids.
# Rebuild the same nominal dimensions and require ONE solid after union.
repaired={}
for c,za,zb in [('B',old.bolme_z(19),old.bolme_z(35)),('C',old.bolme_z(35),156.)]:
    s=parts['helezon_'+c]
    core=old.silz(0,CY,8.,za+3,zb-3).union(old.silz(0,CY,7.,za,za+3.5)).union(old.silz(0,CY,7.,zb-3.5,zb))
    flight=old.kanat_surekli(za+.2,zb-.2).val()
    fixed=None
    for angle in [0,37,73,113,151,197,233,271,307]:
        trial=core.val().rotate((0,CY,0),(0,CY,1),angle).fuse(flight)
        print('UNION_TRY',c,angle,len(trial.Solids()),trial.isValid(),flush=True)
        if trial.isValid() and len(trial.Solids())==1:
            trial=trial.cut(old.karez(0,CY,8.3,za-2,zb+2).val())
            if trial.isValid() and len(trial.Solids())==1:fixed=trial;break
    assert fixed is not None,(c,'single solid union failed')
    assert fixed.isValid() and len(fixed.Solids())==1,(c,'shaft/flight union failed',len(fixed.Solids()))
    repaired['helezon_'+c]=fixed
    cq.exporters.export(fixed,str(OUT/f'helezon_{c}_v15.step'))
    mesh('candidate_'+c,fixed)

# D segment: same square drive, neck and front journal. Two starts retained
# for smoother delivery; pitch 36 -> 60, free axial channel 15 -> 27 mm.
# Feed to the outlet centre instead of ending upstream with six pegs.
g=old.silz(0,CY,old.R_MIL,159.,233.)
g=old.kaynat(g,old.silz(0,CY,old.R_MIL-1,156.,159.5),'D neck')
phase=math.degrees(old.teta_z(old.KAN_Z1))%360
for angle in (phase,phase+180):
    g=old.kaynat_kanat(g,old.kanat_sabit(60.,156.,211.,angle),'D open pitch')
g=old.kaynat(g,old.silz(0,CY,6.,233.,253.),'D journal')
g=g.cut(old.karez(0,CY,old.KARE+.3,154.,232.))
assert g.val().isValid() and len(g.val().Solids())==1
new=g.val();mesh('candidate_D',new)
cq.exporters.export(new,str(OUT/'helezon_D_v15.step'))
cq.exporters.export(new,str(OUT/'helezon_D_v15.stl'))
from kasar_v2_tup import build as build_tube
repaired['cikis_tupu']=build_tube()
assert repaired['cikis_tupu'].isValid() and len(repaired['cikis_tupu'].Solids())==1
cq.exporters.export(repaired['cikis_tupu'],str(OUT/'cikis_tupu_v15.step'))
mesh('candidate_tube',repaired['cikis_tupu'])

assembly=cq.Assembly(name='KASAR_V2_CAD_v15_DENEME')
for name,shape in parts.items():
    target=new if name=='helezon_D' else repaired.get(name,shape)
    report['parts'][name]=dict(changed=name in repaired or name=='helezon_D',source_sha256=hashlib.sha256((SRC/(name+'.step')).read_bytes()).hexdigest(),
        old_volume_mm3=shape.Volume(tol=1e-7),new_volume_mm3=target.Volume(tol=1e-7),valid=target.isValid(),
        old_solids=len(shape.Solids()),new_solids=len(target.Solids()))
    # Transport plug is supplied but is not fitted while the machine runs.
    if name!='tasima_tapasi':
        color=(.22,.55,.82) if name=='helezon_D' else ((.72,.87,.9,.2) if name in ('govde','cikis_tupu') else (.83,.83,.79))
        assembly.add(target,name=name,color=cq.Color(*color))
assembly.save(str(OUT/'KASAR_V2_CAD_v15_MONTAJ.step'))

checks=[]
for angle in range(0,360,45):
    r=new.rotate((0,CY,0),(0,CY,1),angle)
    for name in ['cikis_tupu','plaka_on','yatak_kapagi','govde']:
        overlap=r.intersect(repaired.get(name,parts[name])).Volume(tol=1e-7)
        checks.append(dict(angle=angle,part=name,overlap_mm3=overlap,pass_=overlap<.02))
assert all(c['pass_'] for c in checks),checks
report['checks']=checks
report['design']=dict(body_mm=[280,325,360],target_g=55,stock_2day_g=8800,
    screw_od_mm=40,trough_id_mm=44,radial_gap_mm=2,core_diameter_mm=16,
    main_pitch_mm=[old.HATVE0,old.HATVE1],conical_root_diameters_mm=[26,16],
    outlet_pitch_old_mm=36,outlet_pitch_new_mm=60,starts=2,
    axial_channel_old_mm=15,axial_channel_new_mm=27,flight_end_old_mm=194,flight_end_new_mm=211,
    old_pegs=6,new_pegs=0,outlet_id_mm=44,shaft_square_mm=8,journal_mm=12,
    changed_parts=['helezon_B','helezon_C','helezon_D','cikis_tupu'],removed_parts=[],BC_core_diameter_mm=16.,
    vertical_pipe_new_inner_outer_mm=[44.1,50.1],vertical_pipe_old_inner_outer_mm=[44.,50.],
    warning='No crushing, food safety or 48-hour caking validation')
np.savez_compressed(OUT/'closed_meshes.npz',**arrays)
(OUT/'cad_checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
with (OUT/'BOM_diff.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['part','revision','source','material_note'])
    for name in parts:
        changed=name in repaired or name=='helezon_D'
        w.writerow([name,'v15' if changed else 'v14',str(OUT/(name+'_v15.step')) if changed else str(SRC/(name+'.step')),
            'Food-contact declared POM-C candidate; no generic print approval' if changed else 'Unchanged; inherited material qualification not resolved'])
print('CAD_COMPLETE',len(parts),'parts; changed B/C union and D tip',flush=True)
