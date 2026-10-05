import sys, json, numpy as np, collections
from _env import *
sys.path.insert(0, S+r"\gece")
import m8t2_yol as Y
Yo = json.load(open(sys.argv[1] if len(sys.argv)>1 else S+r"\gece\m8t2\yollar_z2.json"))
YL={a:(d["r"],np.array(d["P"])) for a,d in Yo.items() if not a.startswith(("ROBOT","A_"))}
for bos in (0.3,0.0):
    c=Y.carpisma(YL,bosluk=bos)
    print("bosluk",bos,"segment",len(c),"cift",len(set((a,b) for a,b,m,d in c)))
    for (a,b),n in collections.Counter((a,b) for a,b,m,d in c).items():
        ex=[(np.round(m,1).tolist(),round(d,2)) for a2,b2,m,d in c if (a2,b2)==(a,b)]
        print("  ",a,b,n,ex[:4])
