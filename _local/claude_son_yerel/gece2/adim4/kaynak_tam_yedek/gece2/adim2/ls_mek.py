import json,numpy as np,collections,sys
PJ=json.load(open("m8_parca.json",encoding="utf-8"))
MEK=[m["kod"] for m in PJ["MEK"]]
d=collections.OrderedDict()
for p in PJ["parca"]:
    k=MEK[p["mek"]] if p["mek"]>=0 else "-"
    lo=np.array(p["lo"]);hi=np.array(p["hi"])
    a=d.setdefault(k,[0,lo,hi,0]); a[0]+=1;a[1]=np.minimum(a[1],lo);a[2]=np.maximum(a[2],hi);a[3]+=p["n"]
for k,(n,lo,hi,t) in d.items(): print("%-28s %5d %7d %s %s"%(k,n,t,np.round(lo).astype(int).tolist(),np.round(hi).astype(int).tolist()))
