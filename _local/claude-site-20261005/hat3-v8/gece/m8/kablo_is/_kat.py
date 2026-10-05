import sys;sys.path.insert(0,'.')
import glbkit,numpy as np,collections
G=glbkit.Glb('../hat3_v8x.glb')
MK=G.J['extras']['mekanizmalar'] if 'extras' in G.J else G.J['scenes'][0]['extras']['mekanizmalar']
for p in G.prims:
    ex=p['pr'].get('extras',{});k=ex.get('kat') or [];m=ex.get('mek') or []
    c=collections.Counter()
    for i in range(0,len(k),3):
        if k[i] in (4,5): c['kat%d'%k[i]]+=k[i+2]//3
    for i in range(0,len(m),3):
        if 'Hava' in MK[m[i]]['ad'] or 'Kompres' in MK[m[i]]['ad']: c[MK[m[i]]['kod']]+=m[i+2]//3
    if c: print(p['name'],dict(c))
