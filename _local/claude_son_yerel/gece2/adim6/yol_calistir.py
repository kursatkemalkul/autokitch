# -*- coding: utf-8 -*-
import sys, pickle, os, json, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import yol_denetim as Y
IST = sys.argv[1].upper()
D = pickle.load(open(os.path.join(HERE, 'durum_%s.pkl' % IST), 'rb'))
t0 = time.time()
res, n = Y.denetle(D['P'], D['HAR'], D['ROT'], D['GOR'], D['KAY'], D['GIZLI'])
print(IST, 'çift', n, 'çakışma', len(res), '%.0f s' % (time.time() - t0))
OL = D['OLAY']
def olay_at(t):
    m = ''
    for tt, mm in OL:
        if tt <= t + 1e-6: m = mm
    return m
for r in sorted(res, key=lambda r: r['t']):
    r['olay'] = olay_at(r['w'][0])
for r in sorted(res, key=lambda r: r['t'])[:int(sys.argv[2]) if len(sys.argv) > 2 else 400]:
    print('%6.2f %-45s ← %-45s %6.1f mm  | %s' % (r['t'], r['a'][:45], r['b'][:45], r['derin'], r['olay'][:70]))
json.dump(res, open(os.path.join(HERE, 'yol_%s.json' % IST), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
