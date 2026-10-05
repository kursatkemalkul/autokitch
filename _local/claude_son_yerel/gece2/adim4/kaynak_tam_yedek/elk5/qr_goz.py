import json,numpy as np,sys
PJ=json.load(open("c0/m8_parca.json",encoding="utf-8"))
y0,y1=float(sys.argv[1]),float(sys.argv[2])
for p in PJ["parca"]:
    lo=np.array(p["lo"]);hi=np.array(p["hi"])
    if hi[2]<560 or lo[0]<4560 or hi[1]<y0 or lo[1]>y1: continue
    if p["ad"].startswith(("TEZGAH","ELK_ZEMIN")): continue
    print("%-46s %5d %s %s %s"%(p["ad"],p["n"],np.round(lo,1).tolist(),np.round(hi,1).tolist(),"kpk" if p["kpk"] else ""))
