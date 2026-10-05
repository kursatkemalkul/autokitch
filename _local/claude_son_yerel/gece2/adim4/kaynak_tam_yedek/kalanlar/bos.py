import numpy as np, json, sys
Z=np.load("m8_onbellek.npz"); d=json.load(open("m8_parca.json"))
A,B,C=Z["A"],Z["B"],Z["C"]; P=Z["P"]
lo=np.array(eval(sys.argv[1])); hi=np.array(eval(sys.argv[2]))
mn=np.minimum(np.minimum(A,B),C); mx=np.maximum(np.maximum(A,B),C)
m=np.all(mx>lo,1)&np.all(mn<hi,1)
import collections
c=collections.Counter(P[m])
for k,n in c.most_common(60):
    p=d["parca"][k]; mm=m&(P==k)
    print("%-30s n%-5d parca %s %s | bolgede %s %s"%(p["ad"],n,np.round(p["lo"],1).tolist(),np.round(p["hi"],1).tolist(),np.round(mn[mm].min(0),1).tolist(),np.round(mx[mm].max(0),1).tolist()))
