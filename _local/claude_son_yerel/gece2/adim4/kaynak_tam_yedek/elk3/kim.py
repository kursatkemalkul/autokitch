import sys,numpy as np,re
from vox import yukle
import json
A,B,C,P,ad,kpk=yukle()
PJ=json.load(open(S+r"\elk2\zj\m8_parca.json"))["parca"] if False else None
lo=np.array([float(v) for v in sys.argv[1].split(",")]); hi=np.array([float(v) for v in sys.argv[2].split(",")])
tlo=np.minimum(np.minimum(A,B),C); thi=np.maximum(np.maximum(A,B),C)
m=np.all(thi>=lo,1)&np.all(tlo<=hi,1)
from collections import Counter
c=Counter(P[m])
PJ=json.load(open(r"@@KOK_W@@\elk2\zj\m8_parca.json"))["parca"]
for p,n in c.most_common(40):
    q=PJ[p]; print(p,q['ad'],q['mek'],q['kat'],n,np.round(q['lo']).astype(int).tolist(),np.round(q['hi']).astype(int).tolist())
