import sys,os,numpy as np
sys.path.insert(0,'../cekmece'); sys.stdout.reconfigure(encoding='utf-8')
from glb import G
g=G('../../hat3_v9k.glb')
ck=sorted(set(n.get('name','').split('__')[0] for n in g.J['nodes'] if n.get('name','').startswith('CEK_')))
print(len(ck),ck)
print([n.get('name') for n in g.J['nodes'] if n.get('name','').startswith('CEK_K2_lahm_3')])
print(len(g.J['nodes']), len(g.J['meshes']))
