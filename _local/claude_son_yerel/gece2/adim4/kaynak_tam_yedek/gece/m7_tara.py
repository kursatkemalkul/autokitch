# -*- coding: utf-8 -*-
"""m7 tarama: v8w icinde bolgedeki bilesenler (dugum, bilesen no, kutu, ucgen)"""
import sys, numpy as np
sys.path.insert(0, '.')
from glbkit import Glb
G = Glb(sys.argv[1]); x0,x1,y0,y1,z0,z1 = map(float, sys.argv[2].split(','))
for p in G.prims:
    X=p['X']; 
    if X.size==0: continue
    a=X.min(0); b=X.max(0)
    if b[0]<x0 or a[0]>x1 or b[1]<y0 or a[1]>y1 or b[2]<z0 or a[2]>z1: continue
    if len(p['T'])>400000: print('BUYUK', p['name'], len(p['T'])); continue
    tl,kut=G.komp(p)
    for i,(lo,hi,n) in sorted(kut.items(), key=lambda q:(q[1][0][0])):
        if hi[0]<x0 or lo[0]>x1 or hi[1]<y0 or lo[1]>y1 or hi[2]<z0 or lo[2]>z1: continue
        print("%-36s %d #%-5d %6d x %7.1f %7.1f y %7.1f %7.1f z %7.1f %7.1f"%(p['name'],p['pi'],i,n,lo[0],hi[0],lo[1],hi[1],lo[2],hi[2]))
