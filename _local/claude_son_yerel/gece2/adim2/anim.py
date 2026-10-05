import sys,struct,json,numpy as np
S=r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
raw=open(sys.argv[1],"rb").read(); jl=struct.unpack("<I",raw[12:16])[0]; J=json.loads(raw[20:20+jl]); bo=20+jl; BIN=raw[bo+8:]
def acc(i):
    a=J["accessors"][i]; v=J["bufferViews"][a["bufferView"]]; n={"SCALAR":1,"VEC3":3,"VEC4":4}[a["type"]]
    off=v.get("byteOffset",0)+a.get("byteOffset",0); r=np.frombuffer(BIN[off:off+a["count"]*n*4],np.float32)
    return r.reshape(-1,n) if n>1 else r
names=sys.argv[2].split(",")
for ai,a in enumerate(J["animations"]):
    for c in a["channels"]:
        n=c["target"]["node"]; nm=J["nodes"][n]["name"]
        if nm not in names: continue
        s=a["samplers"][c["sampler"]]; I=acc(s["input"]); O=acc(s["output"])
        print(a["name"],nm,c["target"]["path"],"in",s["input"],"out",s["output"],len(I))
        for t,o in zip(I,O):
            print("   %.2f"%t, np.round(o,4).tolist())
