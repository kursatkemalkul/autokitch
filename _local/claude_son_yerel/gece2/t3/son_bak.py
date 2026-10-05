import sys, os, pickle, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', 'cekmece')); sys.stdout.reconfigure(encoding='utf-8')
import yol_denetim_v2 as Y
D = pickle.load(open('plan_t3.pkl', 'rb')); P = D['P']
ciftler = set()
for s in D['PLAN_SORUN']:
    for a, b in s['sorun']: ciftler.add((a, b))
ads = sorted(set(sum([[a, b] for a, b in ciftler], [])))
Pm = {a: dict(V=P[a]['V'] / 1000.0, F=np.asarray(P[a]['F']), tur=P[a]['tur']) for a in ads}
SON = Y.son_kesisim(Pm, ads, 3e-4)
for (a, b) in sorted(ciftler):
    n = SON.get((a, b)) or SON.get((b, a))
    if n:
        # derinlik: a'nın köşelerinden b kutusuna giriş
        lo, hi = np.maximum(P[a]['V'].min(0), P[b]['V'].min(0)), np.minimum(P[a]['V'].max(0), P[b]['V'].max(0))
        print('SON KESİŞİM %-32s ↔ %-32s %5d üçgen · ortak kutu %s' % (a, b, n, np.round(hi - lo, 1).tolist()))
    else: print('yol          %-32s ↔ %s' % (a, b))
