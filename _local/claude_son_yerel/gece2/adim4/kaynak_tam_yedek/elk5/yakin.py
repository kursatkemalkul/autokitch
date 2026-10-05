import json,numpy as np,sys
PJ=json.load(open("c0/m8_parca.json",encoding="utf-8"))
MEK=[m["kod"] for m in PJ["MEK"]]
P=np.array([float(v) for v in sys.argv[1:4]]); r=float(sys.argv[4])
for p in PJ["parca"]:
    lo=np.array(p["lo"]);hi=np.array(p["hi"])
    d=np.linalg.norm(np.maximum(0,np.maximum(lo-P,P-hi)))
    if d<=r: print("%-40s %-20s d%.1f %s %s"%(p["ad"],MEK[p["mek"]] if p["mek"]>=0 else "-",d,np.round(lo,1).tolist(),np.round(hi,1).tolist()))
