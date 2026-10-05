from _env import *
import m8kit
from scipy.cluster.hierarchy import fcluster, linkage
def kesit(G, ad, ax, v, lo, hi):
    """ad priminin ax=v duzlemiyle kesiti; lo/hi (3) pencere -> [(merkez, boyut)]"""
    out=[]
    for p in [q for q in G.prims if q["name"]==ad and not q.get("gizli")]:
        P=p["X"][p["T"][G.gorunur(p)]]
        for a,b in ((0,1),(1,2),(2,0)):
            A=P[:,a];B=P[:,b]; s=(A[:,ax]-v)*(B[:,ax]-v)<0
            t=(v-A[s,ax])/(B[s,ax]-A[s,ax]); out.append(A[s]+t[:,None]*(B[s]-A[s]))
    Q=np.concatenate(out); Q=Q[np.all(Q>=lo,1)&np.all(Q<=hi,1)]
    if len(Q)<2: return []
    o=[i for i in range(3) if i!=ax]
    L=fcluster(linkage(Q[:,o],'single'),1.5,'distance')
    return [((Q[L==k].min(0)+Q[L==k].max(0))/2,(Q[L==k].max(0)-Q[L==k].min(0))) for k in np.unique(L)]
if __name__=="__main__":
    G=m8kit.Glb(sys.argv[1]); ad=sys.argv[2]; ax=int(sys.argv[3]); v=float(sys.argv[4])
    lo=np.array([float(x) for x in sys.argv[5].split(",")]); hi=np.array([float(x) for x in sys.argv[6].split(",")])
    for c,d in kesit(G,ad,ax,v,lo,hi): print(c.round(2),d.round(2))
