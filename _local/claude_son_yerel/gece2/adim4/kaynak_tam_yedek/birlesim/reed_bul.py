from _env import *
import m8kit
from kesit import kesit
G=m8kit.Glb(sys.argv[1])
YS=m8kit.Yuzey(G,haric=("INSAN","ZEMIN"))
import re
out=[]
for z in (-400.0,):
    L=kesit(G,"ELK_DOLAP__kablo",2,z,np.array([700,150,-900.]),np.array([4410,790,0.]))
    for c,d in sorted(L,key=lambda t:(t[0][0],t[0][1])):
        r=max(d[0],d[1])/2
        hits=[]
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            o=c+np.array([dx,dy,0])*(r+0.05)
            # en yakin yuzey ve adi
            best=None
            for zz in (z-60,z,z+60):
                oo=o.copy(); oo[2]=zz
                t=YS.isin(oo,(dx,dy,0),40,haric_ad=r"kablo")
                if t is not None and (best is None or t<best): best=t
            hits.append(None if best is None else round(best,2))
        print("c %8.2f %7.2f r %.2f  +x %s -x %s +y %s -y %s"%(c[0],c[1],r,*hits))
