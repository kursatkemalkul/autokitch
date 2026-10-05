"""Read-only CAD/mesh volume diagnosis; no tolerance weakening."""
from pathlib import Path
import cadquery as cq
import numpy as np
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
p=Path(__file__).resolve().parents[2]/'arastirma/3_TOPPING/kasar_kabi_v14/step/helezon_B.step'
s=cq.importers.importStep(str(p)).val()
print('SOLID',s.isValid(),len(s.Solids()),s.Volume(),flush=True)
for eps in [1e-3,1e-5,1e-7]:
    prop=GProp_GProps()
    err=BRepGProp.VolumeProperties_s(s.wrapped,prop,eps,False,False)
    print('ADAPTIVE',eps,prop.Mass(),err,flush=True)
for tol,ang,fix in [(.025,.10,False),(.01,.15,False),(.025,.05,False),(.01,.10,True)]:
    sc=s.copy().fix() if fix else s.copy()
    BRepMesh_IncrementalMesh(sc.wrapped,tol,False,ang,True).Perform()
    vv,ff=sc.tessellate(tol+1e-6,ang)
    v=np.array([p.toTuple() for p in vv]);f=np.array(ff)
    vol=abs(np.einsum('ij,ij->i',v[f[:,0]],np.cross(v[f[:,1]],v[f[:,2]])).sum()/6)
    for decimals in [6,5,4]:
        verts,inv=np.unique(np.round(v,decimals),axis=0,return_inverse=True);fi=inv[f]
        fi=fi[np.array([len(set(x))==3 for x in fi])]
        edges=np.sort(np.vstack([fi[:,[0,1]],fi[:,[1,2]],fi[:,[2,0]]]),axis=1)
        _,cnt=np.unique(edges,axis=0,return_counts=True)
        print('MESH',tol,ang,fix,'volume',vol,'tri',len(f),'decimals',decimals,'badedges',sum(cnt!=2),'counts',np.unique(cnt,return_counts=True),flush=True)
