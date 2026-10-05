# python kv.py glb ad comp y0 y1  -> bilesenin o y bandindaki kose kumeleri (kablo ucu bulmak)
from _env import *
import m8kit
G=m8kit.Glb(sys.argv[1]); p=[q for q in G.prims if q["name"]==sys.argv[2] and not q.get("gizli")][0]
tl,kut=G.komp(p); c=int(sys.argv[3]); ax=int(sys.argv[6]) if len(sys.argv)>6 else 1
m=(tl==c)&G.gorunur(p); V=p["X"][np.unique(p["T"][m])]
s=V[(V[:,ax]>=float(sys.argv[4]))&(V[:,ax]<=float(sys.argv[5]))]
# kumele 30 mm
from scipy.cluster.hierarchy import fcluster, linkage
if len(s)>1:
    L=fcluster(linkage(s,'single'),8,'distance')
    for k in np.unique(L):
        q=s[L==k]; print(len(q), q.min(0).round(1), q.max(0).round(1))
