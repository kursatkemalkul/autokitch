import sys, os, pickle, numpy as np
sys.path.insert(0, '../cekmece'); import yol_denetim_v2 as Y
P = pickle.load(open('e_parca.pkl', 'rb'))['P']
Pm = {a: dict(V=P[a]['V'] / 1000.0, F=np.asarray(P[a]['F']), tur=P[a]['tur']) for a in P}
M = [a for a in P if P[a]['tur'] in ('mek', 'profil', 'sac') ]
S = [a for a in P if a.startswith(('arayuz', 'govde_pem')) or a.endswith('saplama')]
for s in sorted(S):
    lo, hi = P[s]['V'].min(0), P[s]['V'].max(0)
    near = [m for m in M if np.all(P[m]['V'].min(0) <= hi + 1) and np.all(P[m]['V'].max(0) >= lo - 1)]
    if not near: continue
    R = Y.son_kesisim({k: Pm[k] for k in [s] + near}, [s] + near, 3e-4)
    hit = {k: v for k, v in R.items() if s in k}
    if hit: print(s, {('↔'.join(k)): int(v) for k, v in hit.items()})
