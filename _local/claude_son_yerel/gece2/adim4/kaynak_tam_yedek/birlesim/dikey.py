from _env import *
import m8kit
G=m8kit.Glb(sys.argv[1])
for ad in ("ELK_K__kablo","ELK_K__kablo_veri","K_ELEKTRIK__hava"):
  for p in [q for q in G.prims if q["name"]==ad and not q.get("gizli")]:
    tl,kut=G.komp(p); vis=G.gorunur(p)
    P=p["X"][p["T"]]
    e=P[:,1]-P[:,0]; 
    # dikey (y) yan yuz ucgenleri: ucgen y-uzunlugu > 100
    dy=P[:,:,1].max(1)-P[:,:,1].min(1)
    m=vis&(dy>150)
    c=P.mean(1)
    for i in np.unique(tl[m]):
        mm=m&(tl==i); Q=P[mm].reshape(-1,3)
        # x,z merkezleri ayri ayri gruplanir
        xz=np.round(P[mm].mean(1)[:,[0,2]]/6)*6
        u=np.unique(xz,axis=0)
        for xx,zz in u:
            s=mm&(np.abs(c[:,0]-xx)<8)&(np.abs(c[:,2]-zz)<8)
            R=P[s].reshape(-1,3)
            print(ad,"c",i,"x %.0f z %.0f  y %.0f-%.0f  r~%.1f"%(R[:,0].mean(),R[:,2].mean(),R[:,1].min(),R[:,1].max(),(R[:,0].max()-R[:,0].min())/2))
