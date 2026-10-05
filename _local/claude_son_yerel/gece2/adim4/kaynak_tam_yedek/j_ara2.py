import json,struct,sys,re
raw=open(sys.argv[1],'rb').read(); jl=struct.unpack('<I',raw[12:16])[0]; J=json.loads(raw[20:20+jl])
for i,n in enumerate(J['nodes']):
    if 'ANA_PANO' in n.get('name','') : print(i,n['name'],n.get('mesh'),n.get('translation'),n.get('rotation'),n.get('scale'),n.get('children'))
ex=J['scenes'][0]['extras']; print(ex.keys())
s=json.dumps(ex,ensure_ascii=False)
for m in re.finditer(r'iSW|ana_salter',s): print(s[max(0,m.start()-300):m.end()+300]); print("==")
for i,m in enumerate(J['meshes']):
  for p in m['primitives']:
    s=json.dumps(p.get('extras',{}),ensure_ascii=False)
    if 'iSW' in s or 'salter' in s.lower(): print('mesh',i,m['name'],s[:300])
