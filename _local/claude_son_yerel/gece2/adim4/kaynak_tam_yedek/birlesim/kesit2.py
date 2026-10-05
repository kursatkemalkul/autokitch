# duzlem kesiti cizimi (2B, matplotlib): python kesit2.py glb out.png ax v u0 u1 w0 w1 [desen]
from _env import *
import m8kit, re
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
G=m8kit.Glb(sys.argv[1]); out=sys.argv[2]; ax=int(sys.argv[3]); v=float(sys.argv[4]); u0,u1,w0,w1=[float(x) for x in sys.argv[5:9]]
pat=re.compile(sys.argv[9]) if len(sys.argv)>9 else None
u,w=[i for i in range(3) if i!=ax]
fig,a=plt.subplots(figsize=(14,9)); cols={}
for p in G.prims:
    if p.get("gizli") or (pat and not pat.search(p["name"])): continue
    P=p["X"][p["T"][G.gorunur(p)]]
    if not len(P): continue
    s=(P[:,:,ax].min(1)<v)&(P[:,:,ax].max(1)>v)&(P[:,:,u].max(1)>u0)&(P[:,:,u].min(1)<u1)&(P[:,:,w].max(1)>w0)&(P[:,:,w].min(1)<w1)
    if not s.any(): continue
    segs=[]
    for T in P[s]:
        pts=[]
        for i,j in ((0,1),(1,2),(2,0)):
            A,B=T[i],T[j]
            if (A[ax]-v)*(B[ax]-v)<0:
                t=(v-A[ax])/(B[ax]-A[ax]); pts.append(A+t*(B-A))
        if len(pts)==2: segs.append(pts)
    if not segs: continue
    c=cols.setdefault(p["name"],"C%d"%(len(cols)%10))
    for q in segs: a.plot([q[0][u],q[1][u]],[q[0][w],q[1][w]],color=c,lw=0.8)
    a.plot([],[],color=c,label=p["name"])
a.set_xlim(u0,u1); a.set_ylim(w0,w1); a.set_aspect("equal"); a.legend(fontsize=7,loc="center left",bbox_to_anchor=(1.01,0.5)); a.grid(alpha=.3)
a.set_xlabel("xyz"[u]); a.set_ylabel("xyz"[w]); a.set_title("%s=%.1f"%("xyz"[ax],v)); fig.savefig(out,dpi=90)
