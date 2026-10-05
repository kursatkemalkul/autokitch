"""Closed STEP-based contact meshes. Never edits source or previous exports.

Run with existing system CadQuery Python, not Isaac's Python.
Baseline: A-D exactly from existing STEP. Candidate: extended D flight to 196,
no 6 mm sill. This candidate is NOT released for manufacture.
"""
from pathlib import Path
import json, hashlib, math
import numpy as np
import cadquery as cq

ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'arastirma/3_TOPPING/sucuk_kaseti_v7/step'
OUT=ROOT/'arastirma/3_TOPPING/sucuk_v2/cad'
OUT.mkdir(parents=True,exist_ok=True)
report={}; arrays={}

def save_mesh(name,shape,source=None):
    assert shape.isValid() and shape.Volume()>0, name
    v,f=shape.copy().tessellate(.04,.08)
    raw=np.array([p.toTuple() for p in v]); f=np.array(f,dtype=np.int32)
    # Merge CAD tessellation seam vertices without changing positions measurably.
    vv, inv=np.unique(np.round(raw,6),axis=0,return_inverse=True)
    ff=inv[f]; nondeg=np.array([len(set(t))==3 for t in ff]); ff=ff[nondeg]
    edges=np.sort(np.vstack([ff[:,[0,1]],ff[:,[1,2]],ff[:,[2,0]]]),axis=1)
    _,counts=np.unique(edges,axis=0,return_counts=True)
    bad=int(np.sum(counts!=2))
    vol=float(np.einsum('ij,ij->i',vv[ff[:,0]],np.cross(vv[ff[:,1]],vv[ff[:,2]])).sum()/6)
    if vol<0: ff=ff[:,[0,2,1]];vol=-vol
    err=abs(vol-shape.Volume())/shape.Volume()
    assert bad==0, (name,'non-manifold edges',bad)
    assert err<.01,(name,'mesh volume mismatch',err)
    # Author global positions in meters; CAD Y-up -> USD Z-up.
    gv=(vv+np.array([1472.5,260.,-362.5]))*.001
    gv=np.column_stack([gv[:,0],-gv[:,2],gv[:,1]])
    arrays[name+'_V']=gv.astype(np.float32);arrays[name+'_F']=ff.astype(np.int32)
    report[name]={'valid':True,'closed_mesh':True,'bad_edges':bad,
        'cad_volume_mm3':shape.Volume(),'mesh_volume_mm3':vol,'relative_volume_error':err,
        'vertices':len(vv),'triangles':len(ff),'bbox_local_mm':[vv.min(0).tolist(),vv.max(0).tolist()],
        'source':str(source) if source else 'candidate_CAD',
        'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest() if source else None}
    print(name,report[name],flush=True)

for suffix in ['A','B','C','D']:
    src=SRC/f'helezon_{suffix}.step'
    save_mesh('baseline_'+suffix,cq.importers.importStep(str(src)).val(),src)

# Build only changed D segment; use original flight law, shaft and square bore.
import sucuk_cad_v7 as old
g=old.silz(0,old.CY,old.R_MIL,159.,233.)
g=old.kaynat(g,old.silz(0,old.CY,old.R_MIL-1,156.,159.5),'v2 boyun')
g=old.kaynat_kanat(g,old.kanat_sabit(old.UC_HATVE,156.,196.,math.degrees(old.teta_z(old.KAN_Z1))%360),'v2 extended flight')
g=old.kaynat(g,old.silz(0,old.CY,6.,233.,253.),'v2 muylu')
g=g.cut(old.karez(0,old.CY,old.KARE+.3,154.,232.))
candidate=g.val()
cq.exporters.export(candidate,str(OUT/'helezon_D_v2.step'))
save_mesh('candidate_D',candidate)
base_tube=cq.importers.importStep(str(SRC/'cikis_tupu.step')).val()
tube=base_tube.cut(cq.Solid.makeCylinder(36.,6.4,cq.Vector(0,60,181.8),cq.Vector(0,0,1)))
# A pre-existing 16 mm3 overlap was found at the front journal, also present
# with original D. Clear the actual 12 mm journal by 0.2 mm radial, not by
# disabling machine contact. Bayonet tabs at outer radius remain untouched.
tube=tube.cut(cq.Solid.makeCylinder(6.2,7.,cq.Vector(0,60,247.),cq.Vector(0,0,1)))
assert 0<tube.Volume()<base_tube.Volume()
cq.exporters.export(tube,str(OUT/'cikis_tupu_v2.step'))
save_mesh('candidate_tube',tube)
intersection=candidate.intersect(tube).Volume()
assert intersection<.01,('candidate D / tube interference',intersection)
report['candidate_checks']={'D_tube_interference_mm3':intersection,
    'old_journal_interference_mm3':15.997671186250248,
    'new_journal_clearance_bore_mm':12.4,
    'flight_end_old_mm':170.,'flight_end_new_mm':196.,'sill_old_mm':6.,'sill_new_mm':0.,
    'unchanged':['A','B','C','shaft core','bearings','coupling','140 mm external body','325 mm depth'],
    'warning':'Removing sill can increase idle leakage; must test; NOT production-approved.'}
np.savez_compressed(OUT/'closed_meshes.npz',**arrays)
(OUT/'cad_checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('CAD_EXPORT_COMPLETE',OUT,flush=True)
