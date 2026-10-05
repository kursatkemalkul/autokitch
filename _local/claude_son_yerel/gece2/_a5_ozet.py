import json,struct,sys,collections
raw=open(sys.argv[1],"rb").read();jl=struct.unpack("<I",raw[12:16])[0];J=json.loads(raw[20:20+jl])
print("nodes",len(J["nodes"]),"meshes",len(J["meshes"]))
sc=J["scenes"][0]; print("scene extras keys",list(sc.get("extras",{}).keys()))
names=[n.get("name","") for n in J["nodes"]]
c=collections.Counter(n.split("__")[0] for n in names)
for k,v in sorted(c.items()): print(k,v)
