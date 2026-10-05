import sys; sys.path.insert(0,'.')
from glbkit import Glb
from m7_etiket import etiketle
G=Glb('../hat3_v8w.glb'); R=etiketle(G)
for i,(tl,kut,ad) in R.items():
    p=G.prims[i]
    for c,(lo,hi,n) in sorted(kut.items(), key=lambda q:q[1][0][0]):
        if hi[0]<1400 or lo[1]<1030 and hi[1]<1030: continue
        print("%-28s #%-5d %-45s %5d x %7.1f %7.1f y %7.1f %7.1f z %7.1f %7.1f"%(p['name'][15:] if p['name'].startswith('TOPPING_MODUL') else p['name'],c,ad[c],n,lo[0],hi[0],lo[1],hi[1],lo[2],hi[2]))
