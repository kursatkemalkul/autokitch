import json,struct,collections
raw=open('hat3_v8x.glb','rb').read()
jl=struct.unpack('<I',raw[12:16])[0];J=json.loads(raw[20:20+jl])
print(len(J['nodes']),len(J['meshes']))
ad=[n.get('name','') for n in J['nodes']]
c=collections.Counter(a.split('__')[0].split('_')[0] for a in ad)
print(c.most_common(60))
import re
k=[a for a in ad if re.search(r'ELK|KABLO|kablo|HORTUM|hortum|BORU|boru|kanal|KANAL|kelepce|KELEPCE|rakor|RAKOR',a)]
print(len(k))
open('_m8_adlar.txt','w',encoding='utf8').write('\n'.join(k))
n0=J['nodes'][[i for i,a in enumerate(ad) if a.startswith('ELK')][0]]
print(n0)
print(J['meshes'][n0['mesh']]['primitives'][0].keys(), J['meshes'][n0['mesh']].get('extras'))
