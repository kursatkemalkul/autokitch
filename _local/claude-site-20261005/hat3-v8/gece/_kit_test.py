import sys, numpy as np
sys.path.insert(0, r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\gece")
import glbkit
G = glbkit.Glb(sys.argv[1])
print('paylasilan accessor', len(G.paylasim))
print(set(k for p in G.prims for k in p['pr']['attributes']))
print(sum(1 for p in G.prims if 'kpk' in p['pr'].get('extras', {})), 'prim with kpk', len(G.prims), 'prims')
for p in G.prims:
    ex = p['pr'].get('extras', {})
    if 'kpk' in ex and len(ex['kpk']) % 2: print('tek kpk', p['name'])
# kpk olan primler + kapsam
for p in G.prims:
    ex = p['pr'].get('extras', {})
    if 'kpk' in ex:
        m = G.kpk_maske(p); print('%-45s %d/%d' % (p['name'], m.sum(), len(m)))
