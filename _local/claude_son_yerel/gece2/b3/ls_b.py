import sys, json, struct, numpy as np
sys.path.insert(0, r'..\cekmece'); sys.stdout.reconfigure(encoding='utf-8')
from glb import G
g = G(r'..\..\hat3_v9l.glb')
J = g.J
print(J['scenes'][0]['extras'].keys())
# hierarchy names
def walk(i, d, path):
    nd = J['nodes'][i]; nm = nd.get('name','')
    if d <= 2: print('  '*d + nm, ('mesh' if 'mesh' in nd else ''), len(nd.get('children',[])))
    for c in nd.get('children', []): walk(c, d+1, path+[nm])
for r in J['scenes'][0]['nodes']: walk(r, 0, [])
