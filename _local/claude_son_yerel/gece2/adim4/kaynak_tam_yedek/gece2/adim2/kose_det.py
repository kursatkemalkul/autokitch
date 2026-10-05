import json,numpy as np,sys,collections
sys.path.insert(0,r"@@KOK_W@@\elk5")
from ortam_sat import tri_kutu
PJ=json.load(open("c0/m8_parca.json",encoding="utf-8"))
Z=np.load("c0/m8_onbellek.npz"); T=np.stack([Z["A"],Z["B"],Z["C"]],1); Pp=Z["P"]
tlo=T.min(1); thi=T.max(1)
blo=np.array(eval(sys.argv[1]),float); bhi=np.array(eval(sys.argv[2]),float)
m=np.all(thi>blo+0.05,1)&np.all(tlo<bhi-0.05,1); idx=np.where(m)[0]
idx=idx[tri_kutu(T[idx],blo+0.05,bhi-0.05)]
d=collections.defaultdict(list)
for i in idx: d[Pp[i]].append(i)
for pp,ii in d.items():
    p=PJ["parca"][pp]
    if p["ad"].startswith("ELK_DOLAP__kablo"): continue
    Q=T[ii].reshape(-1,3)
    print(p["ad"],len(ii),"parca",np.round(p["lo"],1).tolist(),np.round(p["hi"],1).tolist(),"kesen ucgenler",np.round(Q.min(0),1).tolist(),np.round(Q.max(0),1).tolist())
