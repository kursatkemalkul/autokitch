# -*- coding: utf-8 -*-
"""TOPPING v5 · v9e YERİNE (5 Eki 2026 · bulut oturumu): gövde ent adlarını doğrudan v9w üçgenlerine eşler → merkez_v9w.pkl
(t5_parca.py'nin 'v9e merkez' bloğu bunu okur; hat3_v9e.glb push edilmedi, zinciri OCC ile yeniden koşmak bayt aynılığı garanti etmez).
Kaynak: TOPPING montaj v4 animasyon GLB'si (held-paths/.../topping_montaj.glb) — parça adları = adım-37 ent adları, son konumda.
(1) v9w üçgeni ↔ v4 üçgeni birebir (köşeler 0,02 mm) · (2) v4 parçasının yüzeyinde (≤ 0,02 mm; adım 53'te yeniden ağlanan / delinen saclar)
(3) kalan üçgenler bileşen içinde etiketli komşudan yayılır (çoğunluk) · etiketsiz bileşenler t5_parca'nın YENİ / kısmi mantığına kalır.
Kullanım: python merkez_v9w.py <topping_montaj_v4.glb> (t5_bil.pkl + t3/is_A/hat3_v9e_ent.json okunur)"""
import sys, os, json, pickle, collections
import numpy as np
import trimesh
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'cekmece')); sys.stdout.reconfigure(encoding='utf-8')
from glb import G

ENT = json.load(open(os.path.join(HERE, '..', 't3', 'is_A', 'hat3_v9e_ent.json'), encoding='utf-8'))['parca']
GOVDE_DUG = sorted(set(v['dugum'] for v in ENT.values()))
BIL = pickle.load(open('t5_bil.pkl', 'rb')); L = BIL['L']
GOV = [o for o in L if o['dug'] in GOVDE_DUG]

# v4 parçaları (yalnız ent adları), mm
import glb as _g
_o = _g.G.__init__
class G4(G):
    def __init__(s, p):
        import json as j_, struct
        raw = open(p, 'rb').read(); jl = struct.unpack('<I', raw[12:16])[0]
        s.J = j_.loads(raw[20:20 + jl]); bo = 20 + jl; bl = struct.unpack('<I', raw[bo:bo + 4])[0]; s.BIN = raw[bo + 8:bo + 8 + bl]
        s.W = {}
        for r in s.J['scenes'][0]['nodes']: s._gez(r, np.eye(4))
g4 = G4(sys.argv[1])
eT, eA = [], []
for ni, nd in enumerate(g4.J['nodes']):
    if 'mesh' not in nd or nd['name'] not in ENT: continue
    X, T, *_ = g4.tris(ni)[0]
    eT.append(X[T]); eA += [nd['name']] * len(T)
eT = np.concatenate(eT); eA = np.array(eA, dtype=object)
print('v4 ent parçaları', len(set(eA)), '/', len(ENT), '· üçgen', len(eT))
eC = eT.mean(1); tr = cKDTree(eC)
eS = np.sort(eT.reshape(-1, 9), 1)
# parça başına trimesh (yüzey oyu)
PM = {}
for a in set(eA):
    T = eT[eA == a]; PM[a] = (trimesh.Trimesh(T.reshape(-1, 3), np.arange(len(T) * 3).reshape(-1, 3), process=False), T.reshape(-1, 3).min(0), T.reshape(-1, 3).max(0))

MERKEZ = {}
say = collections.Counter()
for o in GOV:
    V, F = o['V'], np.asarray(o['F'])
    T = V[F]; C = T.mean(1); n = len(F)
    lab = np.full(n, None, dtype=object)
    d, j = tr.query(C)
    ok = (d < 0.02) & (np.abs(eS[j] - np.sort(T.reshape(-1, 9), 1)).max(1) < 0.05)
    ok &= np.array([ENT[a]['dugum'] == o['dug'] for a in eA[j]], bool)
    lab[ok] = eA[j[ok]]; say['birebir'] += int(ok.sum())
    un = np.where(lab == None)[0]
    for a, (m, lo, hi) in PM.items():
        if not len(un): break
        if ENT[a]['dugum'] != o['dug']: continue
        s = un[np.all((C[un] >= lo - 0.1) & (C[un] <= hi + 0.1), 1)]
        if not len(s): continue
        _, dd, _ = trimesh.proximity.closest_point(m, C[s])
        s = s[dd < 0.02]
        if len(s):   # 5 Eki: üç köşe de aynı parçanın yüzeyinde olmalı (eş düzlemli değen saclar: ayak flanşı ↔ taban)
            _, dv, _ = trimesh.proximity.closest_point(m, T[s].reshape(-1, 3))
            s = s[(dv.reshape(-1, 3) < 0.02).all(1)]
        k = s; lab[k] = a; say['yuzey'] += len(k)
        un = np.where(lab == None)[0]
    # yayılım: ortak köşe
    if (lab == None).any() and (lab != None).any():
        TV = coo_matrix((np.ones(3 * n), (np.repeat(np.arange(n), 3), F.ravel())), shape=(n, len(V))).tocsr(); A_ = (TV @ TV.T).tocsr()
        while True:
            un = np.where(lab == None)[0]
            if not len(un): break
            yeni = {}
            for i in un:
                nb = A_.indices[A_.indptr[i]:A_.indptr[i + 1]]
                c = collections.Counter(x for x in lab[nb] if x is not None)
                if c: yeni[i] = c.most_common(1)[0][0]
            if not yeni: break
            for i, a in yeni.items(): lab[i] = a
            say['yayilim'] += len(yeni)
    say['etiketsiz'] += int((lab == None).sum())
    for kk, a in zip([tuple(x) for x in np.round(C, 2)], lab):
        if a is not None: MERKEZ[(o['dug'], kk)] = a
print(dict(say))
bos = [a for a in ENT if a not in set(MERKEZ.values())]
print('v9w gövdesinde karşılığı olmayan ent', len(bos), bos[:40])
pickle.dump(MERKEZ, open('merkez_v9w.pkl', 'wb'))
