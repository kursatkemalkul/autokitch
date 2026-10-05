import sys, pickle, os, time, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import yol_denetim as Y
IST = sys.argv[1].upper()
D = pickle.load(open(os.path.join(HERE, 'durum_%s.pkl' % IST), 'rb'))
ads = [a for a in D['P'] if a not in D['GIZLI'] and a in D['GOR']]
t0 = time.time(); S = Y.son_kesisim(D['P'], ads); print(IST, 'son konum kesişen çift', len(S), '%.0f s' % (time.time() - t0))
pickle.dump(S, open(os.path.join(HERE, 'son_%s.pkl' % IST), 'wb'))
def tur(a): return D['P'][a]['tur']
c = collections.Counter(tuple(sorted((tur(a), tur(b)))) for a, b in S); print(c.most_common(30))
for (a, b), n in sorted(S.items(), key=lambda x: -x[1])[:60]: print('%4d %-45s %-45s' % (n, a, b))
