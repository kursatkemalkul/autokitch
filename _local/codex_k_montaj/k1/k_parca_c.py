# -*- coding: utf-8 -*-
"""K parça çıkarımı (Claude, 6 Eki 2026) — zincir 86 sonrası model → k_parca_c.pkl
1 · modelden K bölgesi + K/* bileşenleri (k_cikar_c: e_cikar ile aynı yöntem)
2 · ad aktarımı: Codex devrindeki 1.037 parçanın üçgenleri (plan_k_clip_full.pkl · P) anahtar olarak; yeni bileşenin her üçgeni eski parçaya
    oy verir (koordinat 0,01 mm). Delik açılan parçada değişmeyen üçgenler çoğunlukta → aynı ad. Taşınan parça (zincir 86 'tasi') eski üçgenleri
    taşıma vektörüyle kaydırılarak eşlenir. Eşleşmeyen yeni bileşenler 86'nın _ent.json kutularıyla (kb_* adları).
Kullanım: python k_parca_c.py <model.glb> <86_ent.json>"""
import sys, os, json, pickle, collections, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'claude_son_yerel', 'gece2', 'cekmece'))
from glb import G, bilesen
t0 = time.time()
GLB, ENTJ = sys.argv[1], sys.argv[2]
D = pickle.load(open('plan_k_clip_full.pkl', 'rb')); P0 = D['P']
ENT = json.load(open(ENTJ, encoding='utf-8'))
TASI = {a: np.array(v['v'], float) for a, v in ENT.get('ek', {}).get('tasi', {}).items()} if 'ek' in ENT else {}
if not TASI:
    TASI = {a: np.array(v['v'], float) for a, v in json.load(open(os.path.join(HERE, '..', '..', '..', 'arastirma', '_uretec', 'h3', 'yama_v9', 'veri', '86_k_baglanti.json'), encoding='utf-8'))['tasi'].items()}
SIL = set(json.load(open(os.path.join(HERE, '..', '..', '..', 'arastirma', '_uretec', 'h3', 'yama_v9', 'veri', '86_k_baglanti.json'), encoding='utf-8'))['sil'])
def key(T):
    return [tuple(sorted(map(tuple, np.round(t, 2)))) for t in T]
KEY = {}
for a, v in P0.items():
    if a in SIL: continue
    T = v['V'][v['F']]
    if a in TASI: T = T + TASI[a]
    for k in key(T): KEY[k] = a
print('anahtar', len(KEY), round(time.time() - t0, 1), 's', flush=True)
# ---- 1 · çıkarım
g = G(GLB); MEK = g.MEK
KK = set(i for i, m in enumerate(MEK) if m['kod'].startswith('K/'))
lo0 = np.array([3700, 0, -900.]); hi0 = np.array([4470, 2250, 160.])
L = []
for ni, nd in enumerate(g.J['nodes']):
    if 'mesh' not in nd or ni not in g.W: continue
    M = g.W[ni]
    if abs(np.linalg.det(M[:3, :3])) ** (1 / 3) < 0.01: continue
    for pi, (X, T, mek, mat, ex) in enumerate(g.tris(ni)):
        Pt = X[T]
        m = (np.all(Pt.max(1) >= lo0, 1) & np.all(Pt.min(1) <= hi0, 1)) | np.isin(mek, list(KK))
        if not m.any(): continue
        ar = np.linalg.norm(np.cross(Pt[:, 1] - Pt[:, 0], Pt[:, 2] - Pt[:, 0]), axis=1); m &= ar > 1e-9
        idx = np.where(m)[0]; Tm = T[idx]; mk = mek[idx]
        if not len(Tm): continue
        cl = bilesen(X, Tm)
        for k in np.unique(cl):
            sel = cl == k; Tc = Tm[sel]; u, inv = np.unique(Tc.reshape(-1), return_inverse=True); V = X[u]
            L.append(dict(dug=nd['name'], mek=int(np.bincount(mk[sel] + 1).argmax() - 1), V=V, F=inv.reshape(-1, 3), lo=V.min(0), hi=V.max(0)))
print('bileşen', len(L), round(time.time() - t0, 1), 's', flush=True)
# ---- 2 · ad aktarımı
PARCA = collections.defaultdict(list); YENI = []
for o in L:
    ks = key(o['V'][o['F']]); ad = [KEY.get(k) for k in ks]
    c = collections.Counter(x for x in ad if x)
    if not c: YENI.append(o); continue
    if len(c) == 1:
        PARCA[c.most_common(1)[0][0]].append((o, np.arange(len(o['F']))))
        continue
    # birden çok eski parça: üçgen üçgen; eşleşmeyen üçgen (delik duvarı) bileşenin çoğunluğuna
    cog = c.most_common(1)[0][0]
    ad = np.array([x or cog for x in ad], dtype=object)
    for a in set(ad): PARCA[a].append((o, np.where(ad == a)[0]))
# yeni bileşenler: 86 ent kutusu
EP = ENT['parca']
def ic(o, k, tol=0.6): return np.all(o['lo'] >= np.array([k[0], k[2], k[4]]) - tol) and np.all(o['hi'] <= np.array([k[1], k[3], k[5]]) + tol)
ESLESMEYEN = []
for o in YENI:
    en, hc = None, None
    for a, v in EP.items():
        k = v['kutu']
        if v['dugum'] != o['dug'] or not ic(o, k): continue
        h = np.prod(np.subtract([k[1], k[3], k[5]], [k[0], k[2], k[4]]) + 1e-3)
        if hc is None or h < hc: en, hc = a, h
    if en: PARCA[en].append((o, np.arange(len(o['F']))))
    else: ESLESMEYEN.append(o)
P = {}
for a, LL in PARCA.items():
    VV, FF, n = [], [], 0
    for o, tri in LL:
        Tc = o['F'][tri]; u, inv = np.unique(Tc.reshape(-1), return_inverse=True)
        VV.append(o['V'][u]); FF.append(inv.reshape(-1, 3) + n); n += len(u)
    V = np.vstack(VV); F = np.vstack(FF)
    if a in P0:
        P[a] = dict(P0[a], V=V, F=F)
    else:
        v = EP[a]; b = ' '.join(str(x) for x in (v.get('bom') or []))
        tur = 'kaynak' if 'kaynak' in a else 'baglanti'
        m = 'kaynak' if tur == 'kaynak' else 'baglanti'
        P[a] = dict(V=V, F=F, m=m, tur=tur, ac=b or a, dugum=v['dugum'], kpk=False)
kayip = sorted(set(P0) - set(P) - SIL)
print('parça', len(P), '· eski parçadan eşleşmeyen', len(kayip), kayip[:10], '· adsız yeni bileşen', len(ESLESMEYEN),
      [(o['dug'], np.round(o['lo']).tolist()) for o in ESLESMEYEN[:5]], round(time.time() - t0, 1), 's')
pickle.dump(dict(P=P, ENT=EP, MEK=MEK), open('k_parca_c.pkl', 'wb'))
