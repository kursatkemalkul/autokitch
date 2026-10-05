import json,struct,sys
raw=open(sys.argv[1],'rb').read();jl=struct.unpack('<I',raw[12:16])[0];J=json.loads(raw[20:20+jl])
print(len(J['nodes']),'nodes',len(J['meshes']),'meshes',len(J['accessors']),'acc', len(J.get('materials',[])),'mat')
ex=J['scenes'][0].get('extras',{})
print(list(ex.keys()))
for k in ex:
  if k not in('mekanizmalar','kategoriler'): print(k, str(ex[k])[:300])
print(json.dumps(ex['kategoriler'],ensure_ascii=False)[:3000])
for i,m in enumerate(ex['mekanizmalar']): print(i,json.dumps(m,ensure_ascii=False))
np_=0
for m in J['meshes']:
  for p in m['primitives']:
    np_+=1
print('prims',np_)
# sample primitive extras
c=0
for ni,nd in enumerate(J['nodes']):
  if 'mesh' in nd:
    for p in J['meshes'][nd['mesh']]['primitives']:
      if c<6: print(nd['name'], {k:(v[:12] if isinstance(v,list) else v) for k,v in p.get('extras',{}).items()}, J['accessors'][p['indices']]['count'], p.get('mode'))
      c+=1
print(J.get('extras'))
