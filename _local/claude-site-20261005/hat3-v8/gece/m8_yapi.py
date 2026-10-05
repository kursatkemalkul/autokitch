import json,struct,sys
raw=open(sys.argv[1],'rb').read(); jl=struct.unpack('<I',raw[12:16])[0]; J=json.loads(raw[20:20+jl])
print(len(J['nodes']),'nodes',len(J['meshes']),'meshes', len(J.get('animations',[])),'anims')
sc=J['scenes'][0].get('extras',{}); print('scene extras keys',list(sc.keys()))
for k,v in sc.items(): print(k, json.dumps(v,ensure_ascii=False)[:1500])
nm=[n.get('name') for n in J['nodes']]
import collections
print(collections.Counter(n.split('__')[0] for n in nm if n).most_common(400))
ex=0
for n in J['nodes']:
  if 'mesh' in n:
    for pr in J['meshes'][n['mesh']]['primitives']:
      e=pr.get('extras',{})
      if ex<5 and e: print(n['name'], {k:v[:12] for k,v in e.items()}); ex+=1
