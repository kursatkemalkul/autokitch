import json,numpy as np,collections,sys
PJ=json.load(open("c0/m8_parca.json",encoding="utf-8"))
MEK=[m["kod"] for m in PJ["MEK"]]
d=collections.OrderedDict()
for p in PJ["parca"]:
    lo=np.array(p["lo"]);hi=np.array(p["hi"])
    if hi[2]<560 or lo[0]<4400: continue
    k=(p["ad"],MEK[p["mek"]] if p["mek"]>=0 else "-")
    a=d.setdefault(k,[0,lo,hi,0]); a[0]+=1;a[1]=np.minimum(a[1],lo);a[2]=np.maximum(a[2],hi);a[3]+=p["n"]
for (ad,m),(n,lo,hi,t) in d.items(): print("%-52s %-22s %4d %6d %s %s"%(ad,m,n,t,np.round(lo).astype(int).tolist(),np.round(hi).astype(int).tolist()))
