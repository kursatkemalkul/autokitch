import json,struct,sys,re
raw=open(sys.argv[1],"rb").read();jl=struct.unpack("<I",raw[12:16])[0];J=json.loads(raw[20:20+jl])
pat=re.compile(sys.argv[2])
for i,n in enumerate(J["nodes"]):
    nm=n.get("name","")
    if pat.search(nm):
        m=n.get("mesh"); np_=len(J["meshes"][m]["primitives"]) if m is not None else 0
        ex=J["meshes"][m]["primitives"][0].get("extras",{}) if m is not None else {}
        print(i,nm,{k:n[k] for k in ("translation","rotation","scale","matrix") if k in n},"prims",np_,"children",n.get("children",[])[:5], "exkeys",list(ex.keys()), "nodeextras", list(n.get("extras",{}).keys()))
