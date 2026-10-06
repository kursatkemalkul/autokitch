# -*- coding: utf-8 -*-
"""K plan yardımcısı: her bağlantı elemanı / kaynak hangi taşıyıcı parçalara değiyor (≤ 0,6 mm) → k_deg.json
Girdi: k_parca_c.pkl. Montaj planı bir bağlantı elemanını, değdiği taşıyıcıların hepsi yerindeyken takar."""
import json, pickle
import numpy as np
import trimesh
from multiprocessing import Pool
P = pickle.load(open('k_parca_c.pkl', 'rb'))['P']
TOL = 0.6
BAG = [a for a in P if P[a]['tur'] in ('baglanti', 'kaynak', 'silikon')]
TAS = [a for a in P if P[a]['tur'] not in ('baglanti', 'kaynak', 'silikon', 'kablo') and not a.startswith('cevre')]
LO = {a: P[a]['V'].min(0) for a in P}; HI = {a: P[a]['V'].max(0) for a in P}
TM = {}
def tm(a):
    if a not in TM: TM[a] = trimesh.Trimesh(P[a]['V'], P[a]['F'], process=False)
    return TM[a]
def bir(f):
    out = []
    S = np.vstack([P[f]['V'], trimesh.sample.sample_surface_even(tm(f), 400, seed=2)[0] if len(P[f]['F']) else np.zeros((0, 3))])
    for a in TAS:
        if np.any(LO[a] > HI[f] + TOL) or np.any(HI[a] < LO[f] - TOL): continue
        Q = S[np.all(S >= LO[a] - TOL, 1) & np.all(S <= HI[a] + TOL, 1)]
        if not len(Q): continue
        _, d, _ = trimesh.proximity.closest_point(tm(a), Q)
        if d.min() <= TOL: out.append(a)
    return f, out
if __name__ == '__main__':
    with Pool(8) as pool: R = dict(pool.map(bir, BAG, chunksize=4))
    json.dump(R, open('k_deg.json', 'w'), ensure_ascii=False)
    print('bağlantı elemanı', len(R), '· hiçbir taşıyıcıya değmeyen', sum(1 for v in R.values() if not v))
