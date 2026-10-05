"""Track genuinely lost cubes to distinguish edge spill from collider leak."""
from pathlib import Path
import json,sys
import numpy as np
out=Path(__file__).resolve().parents[2]/'arastirma/3_TOPPING/sucuk_v2/runs'
tag=sys.argv[1] if len(sys.argv)>1 else 'mixed_candidate_01'
d=np.load(out/(tag+'.npz'));x=d['xyz'];t=d['time'];n=len(d['mass_kg']);m=d['mass_kg']*1000
p=x[:,d['paths'].tolist().index('/World/PIDE')];rel=x[:,:n]-p[:,None,:]
r=np.linalg.norm(rel[:,:,:2],axis=2)
last=(x[-1,:n,2]<.160)&~((r[-1]<.140)&(rel[-1,:,2]>0)&(rel[-1,:,2]<.040))
for i in np.flatnonzero(last):
    at=np.flatnonzero(x[:,i,2]<.16);j=int(at[0]) if len(at) else 0
    entry=np.flatnonzero((x[:,i,2]<.145)&(x[:,i,2]>.12));k=int(entry[0]) if len(entry) else j
    print(json.dumps({'id':int(i),'g':float(m[i]),'cross_t':float(t[j]),
        'cross_xyz':x[j,i].tolist(),'first_near_dough_t':float(t[k]),'radius_mm':float(r[k,i]*1000),
        'relative_z_mm':float(rel[k,i,2]*1000),'last_xyz':x[-1,i].tolist(),
        'max_radius_before_fall_mm':float(r[j:min(j+20,len(t)),i].max()*1000)}))
