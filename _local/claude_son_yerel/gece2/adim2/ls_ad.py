import json,numpy as np,collections,sys,re
PJ=json.load(open("m8_parca.json",encoding="utf-8"))
MEK=[m["kod"] for m in PJ["MEK"]]
pat=re.compile(sys.argv[1])
d=collections.OrderedDict()
for p in PJ["parca"]:
    k=MEK[p["mek"]] if p["mek"]>=0 else "-"
    if not (pat.search(k) or pat.search(p["ad"])): continue
    lo=np.array(p["lo"]);hi=np.array(p["hi"])
    kk=(p["ad"],k)
    a=d.setdefault(kk,[0,lo,hi,0]); a[0]+=1;a[1]=np.minimum(a[1],lo);a[2]=np.maximum(a[2],hi);a[3]+=p["n"]
for (ad,k),(n,lo,hi,t) in d.items(): print("%-50s %-24s %4d %7d %s %s"%(ad,k,n,t,np.round(lo).astype(int).tolist(),np.round(hi).astype(int).tolist()))
