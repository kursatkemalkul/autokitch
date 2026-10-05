import sys, pickle, os, time, json, numpy as np
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, '.')
import yol_denetim as Y, yol_duzelt as Z
IST = sys.argv[1]; D = pickle.load(open('durum_%s.pkl' % IST, 'rb'))
H = pickle.load(open('son_%s.pkl' % IST, 'rb'))
De = Y.Denetci(D['P'], D['HAR'], D['ROT'], D['GOR'], D['KAY'], D['GIZLI'], H)
grup = sys.argv[2:]
gi = {a: Z.gel_indeks(D['HAR'], D['GOR'], a) for a in grup}
h0 = D['HAR'][grup[0]][gi[grup[0]]]; print(h0)
yed = {a: [list(h) for h in D['HAR'][a]] for a in grup}
for et, ad in Z.adaylar(D['P'], grup, h0[2:5])[:12]:
    for a in grup: D['HAR'][a] = [list(h) for h in yed[a]]
    Z.uygula_aday(D['HAR'], grup, gi, ad, h0[0], h0[1])
    t0 = time.time(); ok, n = Z.grup_temiz(De, grup); print(et, ok, n, '%.2f s' % (time.time() - t0), flush=True)
