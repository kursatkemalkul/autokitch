import json,numpy as np,sys,re,collections
PJ=json.load(open("c0/m8_parca.json",encoding="utf-8")); MEK=[m["kod"] for m in PJ["MEK"]]
L=np.array([float(v) for v in sys.argv[1:7]]); pat=sys.argv[7] if len(sys.argv)>7 else "."
d=collections.OrderedDict()
for p in PJ["parca"]:
    lo=np.array(p["lo"]);hi=np.array(p["hi"])
    if np.any(hi<L[0::2]) or np.any(lo>L[1::2]) or not re.search(pat,p["ad"]): continue
    if len(sys.argv)>8:
        print("%-46s %5d %s %s %s"%(p["ad"],p["n"],np.round(lo,1).tolist(),np.round(hi,1).tolist(),"kpk" if p["kpk"] else "")); continue
    k=(p["ad"],MEK[p["mek"]] if p["mek"]>=0 else "-")
    a=d.setdefault(k,[0,lo,hi]); a[0]+=1;a[1]=np.minimum(a[1],lo);a[2]=np.maximum(a[2],hi)
for (ad,m),(n,lo,hi) in d.items(): print("%-50s %-18s %4d %s %s"%(ad,m,n,np.round(lo).astype(int).tolist(),np.round(hi).astype(int).tolist()))
