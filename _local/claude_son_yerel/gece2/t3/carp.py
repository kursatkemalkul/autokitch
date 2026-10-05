import sys, os, pickle, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', 'cekmece')); sys.stdout.reconfigure(encoding='utf-8')
import yol_denetim_v2 as Y
D = pickle.load(open('plan_t3.pkl', 'rb')); P = D['P']
def carp(a, b, ofs):
    v = -np.asarray(ofs, float) / 1000.0
    A0 = Y._vekil(P[a]['V'] / 1000.0, np.asarray(P[a]['F'])) + np.asarray(ofs) / 1000.0
    B = Y._vekil(P[b]['V'] / 1000.0, np.asarray(P[b]['F']))
    lam = Y.ccd(np.ascontiguousarray(A0), np.ascontiguousarray(B), v, Y.SINIR)
    m = lam < 1.5
    if not m.any(): print(a, b, 'temiz'); return
    i = np.where(m)[0]; L = lam[i]
    der = (1 - L) * np.linalg.norm(v) * 1000
    k = i[np.argmax(der)]
    print('%s ↔ %s: %d üçgen · en derin kalan yol %.1f mm · üçgen merkezi (son konum) %s' % (a, b, len(i), der.max(), np.round(A0[k].mean(0) * 1000 - np.asarray(ofs), 1).tolist()))
for x in sys.argv[1:]:
    a, b, o = x.split(':'); carp(a, b, [float(t) for t in o.split(',')])
