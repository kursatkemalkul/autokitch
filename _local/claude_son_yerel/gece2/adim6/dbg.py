import sys, pickle, os, numpy as np
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, '.')
import yol_denetim as Y
IST = sys.argv[1]; D = pickle.load(open('durum_%s.pkl' % IST, 'rb'))
P = D['P']; ads = [a for a in P if a not in D['GIZLI'] and a in D['GOR']]
H = pickle.load(open('son_%s.pkl' % IST, 'rb')) if os.path.exists('son_%s.pkl' % IST) else {}
De = Y.Denetci(P, D['HAR'], D['ROT'], D['GOR'], D['KAY'], D['GIZLI'], H)
for a in sys.argv[2:]:
    print(a, 'HAR', D['HAR'][a], 'g', D['GOR'][a])
    ia = De.idx[a]
    aday = np.where(np.all(De.L <= De.H[ia] + 1e-4, 1) & np.all(De.H >= De.L[ia] - 1e-4, 1))[0]
    for jb in aday:
        b = De.ads[jb]
        if b == a: continue
        r = De.cift(a, b)
        if r: print('   ', b, r['t'], r['derin'], 'haric' if (min(a,b),max(a,b)) in H else '')
