import sys, numpy as np, trimesh
sys.path.insert(0,'.')
from glbkit import Glb
G=Glb(sys.argv[1])
for a in sys.argv[2:]:
    nm,ci=a.rsplit(':',1); ci=int(ci)
    p=G.bul(nm); tl,kut=G.komp(p); m=(tl==ci)&G.gorunur(p)
    tm=trimesh.Trimesh(p['X'],p['T'][m],process=True); tm.merge_vertices(digits_vertex=2)
    print(nm,ci,'tris',m.sum(),'watertight',tm.is_watertight,'winding',tm.is_winding_consistent,'vol',round(tm.volume/1e6,3) if tm.is_watertight else '-', 'bodies',len(tm.split(only_watertight=False)))
