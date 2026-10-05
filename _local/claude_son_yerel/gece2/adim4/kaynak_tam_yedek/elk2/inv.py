import json,struct,sys,numpy as np
raw=open(sys.argv[1],'rb').read(); jl=struct.unpack('<I',raw[12:16])[0]; J=json.loads(raw[20:20+jl])
sc=J['scenes'][0]['extras']
M=sc['mekanizmalar']; K=sc['kategoriler']
print(len(J['nodes']),'nodes', len(J['meshes']),'meshes', len(J['materials']),'mats')
for i,m in enumerate(M): print('MEK',i,m['kod'],m.get('ad',''))
for i,k in enumerate(K): print('KAT',i,k)
for i,m in enumerate(J['materials']): print('MAT',i,m.get('name'),m.get('pbrMetallicRoughness',{}).get('baseColorFactor'))
