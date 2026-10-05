import sys, os
H3=sys.argv[1]; sys.path.insert(0,H3); sys.path.insert(0,os.path.dirname(H3))
import h3_k_sac_v1 as K
K.kur(log=lambda *a: None)
L=K.dunya_listesi(K.govde_parcalari())
lim=dict(x=(-1,None),y=(-1,2201),z=(-831,80))
for p in L:
    s=p.get("sh") or p.get("wp"); s=s.val() if hasattr(s,"val") else s; b=s.BoundingBox()
    if b.ymax>2201 or b.zmax>80 or b.zmin<-831 or b.ymin<-1:
        print(p["ad"], p.get("birim"), round(b.xmin),round(b.xmax),round(b.ymin,1),round(b.ymax,1),round(b.zmin,1),round(b.zmax,1))
