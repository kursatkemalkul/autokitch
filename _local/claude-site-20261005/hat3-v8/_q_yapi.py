import sys, os, re
sys.path.insert(0,'tg')
from glbx import yukle
import numpy as np
J,D=yukle('hat3_v8p.glb')
print(len(J['nodes']), 'nodes', len(D),'mesh nodes')
mp=[(i,nd.get('name')) for i,nd in enumerate(J['nodes']) if 'mesh' in nd and len(J['meshes'][nd['mesh']]['primitives'])>1]
print('multi prim', len(mp), mp[:5])
rot=[k for k,d in D.items() if d['rot']]; print('rot', len(rot), rot[:20])
ch=[nd.get('name') for nd in J['nodes'] if 'children' in nd]; print('parents', ch[:10])
pref={}
for k,d in D.items():
    p=k.split('__')[0]; pref.setdefault(p,[0,0]); pref[p][0]+=1; pref[p][1]+=int(d['ok'].sum())
for p in sorted(pref): print(p, pref[p])
ex=[(k,list(d['ex'].keys())) for k,d in D.items() if d['ex']]
print(ex[:10])
