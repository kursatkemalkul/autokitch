import json,struct,sys
def oku(p):
    f=open(p,"rb"); h=f.read(20); jl=struct.unpack("<I",h[12:16])[0]; return json.loads(f.read(jl))
