import json,sys,numpy as np
d=json.load(open("m8_parca.json"))
lo=np.array(eval(sys.argv[1])); hi=np.array(eval(sys.argv[2]))
MEK=d["MEK"]
for p in d["parca"]:
    a=np.array(p["lo"]);b=np.array(p["hi"])
    if np.all(a<hi)&np.all(b>lo):
        if "kablo" in p["ad"] and "ANA_HAT" in p["ad"] and len(sys.argv)<4: continue
        m=MEK[p["mek"]] if p["mek"]>=0 else "-"
        print("%-34s %-22s n%-5d %s %s"%(p["ad"],(m if isinstance(m,str) else m.get("ad",m))[:22],p["n"],np.round(a,1).tolist(),np.round(b,1).tolist()))
