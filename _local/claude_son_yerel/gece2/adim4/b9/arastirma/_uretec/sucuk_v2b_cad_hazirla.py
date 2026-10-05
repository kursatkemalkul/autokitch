"""V2B high-clearance candidate. Preserve V2A and all original CAD.

50 mm flight OD in 72 mm trough -> 11 mm radial gap. This is a hypothesis,
not proof against crushing: 10 mm cubes have a 17.3 mm body diagonal.
The original 6 mm sill is retained; journal clash correction is retained.
"""
from pathlib import Path
import json
import numpy as np
import cadquery as cq
ROOT=Path(__file__).resolve().parents[2]
OLD=ROOT/'arastirma/3_TOPPING/sucuk_kaseti_v7/step'
OUT=ROOT/'arastirma/3_TOPPING/sucuk_v2/cad'
arrays={};audit={}
def export(name,s):
    assert s.isValid() and s.Volume()>0
    v,f=s.copy().tessellate(.04,.08)
    v=np.array([p.toTuple() for p in v]);f=np.array(f)
    v,ix=np.unique(np.round(v,6),axis=0,return_inverse=True);f=ix[f]
    f=f[np.array([len(set(t))==3 for t in f])]
    edges=np.sort(np.vstack([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),1)
    _,counts=np.unique(edges,axis=0,return_counts=True)
    assert (counts==2).all(),name
    volume=np.einsum('ij,ij->i',v[f[:,0]],np.cross(v[f[:,1]],v[f[:,2]])).sum()/6
    if volume<0:f=f[:,[0,2,1]];volume=-volume
    err=abs(volume/s.Volume()-1);assert err<.001
    gv=(v+[1472.5,260.,-362.5])*.001
    arrays[name+'_V']=np.column_stack([gv[:,0],-gv[:,2],gv[:,1]]).astype(np.float32)
    arrays[name+'_F']=f.astype(np.int32)
    audit[name]={'volume_mm3':s.Volume(),'mesh_volume_error':float(err),'closed_mesh':True,
                 'valid':True,'triangles':len(f)}
    cq.exporters.export(s,str(OUT/(name+'.step')))
    print(name,audit[name],flush=True)
shapes={}
limit=cq.Solid.makeCylinder(25.,510.,cq.Vector(0,60,-200),cq.Vector(0,0,1))
for letter in 'ABCD':
    path=OUT/'helezon_D_v2.step' if letter=='D' else OLD/f'helezon_{letter}.step'
    shape=cq.importers.importStep(str(path)).val().intersect(limit)
    shapes[letter]=shape;export('relieved_'+letter,shape)
tube=cq.importers.importStep(str(OLD/'cikis_tupu.step')).val()
tube=tube.cut(cq.Solid.makeCylinder(6.2,7.,cq.Vector(0,60,247.),cq.Vector(0,0,1)))
export('relieved_tube',tube)
checks=[]
for a in range(0,360,45):
    overlap=shapes['D'].rotate((0,60,0),(0,60,1),a).intersect(tube).Volume()
    checks.append({'angle_deg':a,'overlap_mm3':overlap});assert overlap<.02
audit['checks']={'flight_OD_mm':50,'trough_ID_mm':72,'radial_gap_mm':11,'retained_sill_mm':6,
    'D_flight_end_mm':196,'rotation_checks':checks,
    'warning':'Untested candidate. Bypass, stagnant stock and nipping at sill remain possible.'}
np.savez_compressed(OUT/'relieved_meshes.npz',**arrays)
(OUT/'relieved_checks.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
print('V2B_CAD_COMPLETE',flush=True)
