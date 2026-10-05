# -*- coding: utf-8 -*-
"""TOPPING v5 · denetimin bulduğu öteleme çakışmalarını ayırır (5 Eki): hareket penceresi boyunca 0,5 mm adımla parça konumları örneklenir,
model ağlarında 0,3 mm toleranslı gerçek kesişim (poz_kesisim) aranır. Hiç kesişim yoksa çift 'sıfır boşluklu yüzey teması (kayma)' sayılır.
Kullanım: python temas_dogrula.py  → temas.json {"a ↔ b": {"gercek": bool, "en_cok": n, "t": ...}}"""
import os, sys, json, pickle
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'cekmece'))
import yol_denetim_v2 as Y
D = pickle.load(open('plan_t5.pkl', 'rb')); P, HAR = D['P'], D['HAR']
S = json.load(open('sonuc_t5.json', encoding='utf-8'))
def tri(a): return np.asarray(P[a].get('Vm', P[a]['V']))[np.asarray(P[a].get('Fm', P[a]['F']))] / 1000.0
def ofs(a, tt):
    o = np.zeros(3)
    for h in HAR[a]:
        u = 1.0 if tt >= h[1] else (0.0 if tt <= h[0] else (tt - h[0]) / (h[1] - h[0]))
        o += np.array(h[2:5]) * (1 - u * u * (3 - 2 * u))
    return o
out = {}
for c in S['cakismalar']:
    if c.get('yon') != 'oteleme': continue
    a, b = c['a'], c['b']; A0, B0 = tri(a), tri(b)
    t0, t1 = c['w']; n = max(8, int((t1 - t0) / 0.02))
    en, tt_ = 0, None
    for tt in np.linspace(t0, t1, n):
        A = A0 + ofs(a, tt); B = B0 + ofs(b, tt)
        lo = np.maximum(A.reshape(-1, 3).min(0), B.reshape(-1, 3).min(0)) - 1e-3; hi = np.minimum(A.reshape(-1, 3).max(0), B.reshape(-1, 3).max(0)) + 1e-3
        if np.any(lo > hi): continue
        sa = np.all(A.max(1) >= lo, 1) & np.all(A.min(1) <= hi, 1); sb = np.all(B.max(1) >= lo, 1) & np.all(B.min(1) <= hi, 1)
        if not sa.any() or not sb.any(): continue
        k = int(Y.poz_kesisim(np.ascontiguousarray(A[sa]), np.ascontiguousarray(B[sb]), 3e-4).sum())
        if k > en: en, tt_ = k, round(float(tt), 3)
    out['%s ↔ %s' % (a, b)] = dict(gercek=en > 0, en_cok=en, t=tt_, derin=c['derin'], hareket=c.get('hareket'))
    print('%-55s %s  kesişen üçgen (en çok) %d  t %s' % ('%s ↔ %s' % (a, b), 'GERÇEK' if en else 'yüzey teması', en, tt_), flush=True)
json.dump(out, open('temas.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
