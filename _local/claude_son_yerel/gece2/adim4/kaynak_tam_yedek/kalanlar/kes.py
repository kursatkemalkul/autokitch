# coklu kesit: python kes.py glb onek "ax,v,u0,u1,w0,w1" ...
from _env import *
import m8kit, re
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
G=m8kit.Glb(sys.argv[1]); on=sys.argv[2]
for spec in sys.argv[3:]:
    ax,v,u0,u1,w0,w1=[float(x) for x in spec.split(",")]; ax=int(ax)
    u,w=[i for i in range(3) if i!=ax]
    fig,a=plt.subplots(figsize=(15,10)); cols={}
    for p in G.prims:
        if p.get("gizli"): continue
        P=p["X"][p["T"][G.gorunur(p)]]
        if not len(P): continue
        s=(P[:,:,ax].min(1)<v)&(P[:,:,ax].max(1)>v)&(P[:,:,u].max(1)>u0)&(P[:,:,u].min(1)<u1)&(P[:,:,w].max(1)>w0)&(P[:,:,w].min(1)<w1)
        if not s.any(): continue
        Q=P[s]; segs=[]
        for i,j in ((0,1),(1,2),(2,0)):
            A=Q[:,i];B=Q[:,j]; m=(A[:,ax]-v)*(B[:,ax]-v)<0
            t=(v-A[m,ax])/(B[m,ax]-A[m,ax]); segs.append((np.where(m)[0],A[m]+t[:,None]*(B[m]-A[m])))
        idx=np.concatenate([s_[0] for s_ in segs]); pts=np.concatenate([s_[1] for s_ in segs])
        o=np.argsort(idx,kind="stable"); idx=idx[o]; pts=pts[o]
        k=np.where(idx[:-1]==idx[1:])[0]
        if not len(k): continue
        c=cols.setdefault(p["name"],"C%d"%(len(cols)%10))
        ls="-" if len(cols)<=10 else ("--" if len(cols)<=20 else ":")
        for i in k: a.plot([pts[i,u],pts[i+1,u]],[pts[i,w],pts[i+1,w]],color=c,lw=0.9,ls=ls)
        a.plot([],[],color=c,ls=ls,label=p["name"])
    a.set_xlim(u0,u1); a.set_ylim(w0,w1); a.set_aspect("equal"); a.legend(fontsize=7,loc="center left",bbox_to_anchor=(1.01,0.5)); a.grid(alpha=.3)
    a.set_xlabel("xyz"[u]); a.set_ylabel("xyz"[w]); a.set_title("%s=%.1f"%("xyz"[ax],v)); fig.tight_layout(); fig.savefig("%s_%s%d.png"%(on,"xyz"[ax],v),dpi=80); plt.close(fig)
    print("ok",spec)
