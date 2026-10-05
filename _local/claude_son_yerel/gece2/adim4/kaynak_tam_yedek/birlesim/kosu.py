# kablo duz kosulari: her eksen icin uzun yan-yuz ucgenlerini eksen-dik kesit merkezine gore grupla
from _env import *
import m8kit, re
G=m8kit.Glb(sys.argv[1]); pat=re.compile(sys.argv[2]); lo=np.array([float(v) for v in sys.argv[3].split(",")]); hi=np.array([float(v) for v in sys.argv[4].split(",")])
for p in [q for q in G.prims if pat.search(q["name"]) and not q.get("gizli")]:
    tl,kut=G.komp(p); vis=G.gorunur(p); P=p["X"][p["T"]]; c=P.mean(1)
    ins=vis&np.all(c>=lo,1)&np.all(c<=hi,1)
    for ax in range(3):
        u,w=[i for i in range(3) if i!=ax]
        d=P[:,:,ax].max(1)-P[:,:,ax].min(1)
        m=ins&(d>60)
        if not m.any(): continue
        for i in np.unique(tl[m]):
            mm=m&(tl==i)
            # kesit merkezleri: komsu ucgenler ayni kablo -> u,w 12 mm grid
            key=np.round(c[mm][:,[u,w]]/12).astype(int)
            for k in np.unique(key,axis=0):
                s=np.where(mm)[0][np.all(key==k,1)]
                R=P[s].reshape(-1,3)
                cu=(R[:,u].max()+R[:,u].min())/2; cw=(R[:,w].max()+R[:,w].min())/2
                print("%-20s c%-3d eksen %s  %s=%.1f %s=%.1f  %.0f..%.0f  cap %.1f"%(p["name"],i,"xyz"[ax],"xyz"[u],cu,"xyz"[w],cw,R[:,ax].min(),R[:,ax].max(),max(R[:,u].max()-R[:,u].min(),R[:,w].max()-R[:,w].min())))
