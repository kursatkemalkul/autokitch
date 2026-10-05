import json,struct,sys
raw=open(sys.argv[1],'rb').read(); jl=struct.unpack('<I',raw[12:16])[0]; J=json.loads(raw[20:20+jl])
print(J.keys(), len(J['nodes']), len(J['meshes']))
s=json.dumps(J)
import re
for k in ['kasar_cad_v14','sucuk_cad_v8','yatak_kapagi']:
    print(k, s.count(k))
for i,n in enumerate(J['nodes']):
    if 'kasar' in n.get('name','') or 'sucuk' in n.get('name','') : print(i,n.get('name'), {k:v for k,v in n.items() if k not in('children',)} )
# where does string appear
i=s.find('kasar_cad_v14__cikis'); print(s[i-600:i+200])
