import sys, json, numpy as np
import os
KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))   # depo kökü
sys.path.insert(0, os.path.join(KOK, 'arastirma', '_uretec', 'h3', 'yama_v9'))
import sac_ent  # m8kit yolu (YAMA_IS_KOK/gece)
import e_mek_bag as MB
from m8kit import Glb
g = Glb(sys.argv[1]); M = MB.Mek(g, (4390, 560, -900), (5240, 1900, 100))
def harita(ad, ax, koord, yon, pts):
    P = M.P(ad); e = np.zeros(3); e[ax] = yon
    for u, w in pts:
        p = np.zeros(3); o = [k for k in range(3) if k != ax]; p[o[0]] = u; p[o[1]] = w; p[ax] = koord
        o0 = p - e * 300.0; ts = [(round(t0 - 300, 1), round(t1 - 300, 1)) for t0, t1 in MB.kati_araliklari(P, o0, e, 600.0)]
        print('   %-26s %s=%-7g (%g, %g) → %s' % (ad, 'xyz'[ax], koord, u, w, ts))
exec(open(sys.argv[2], encoding='utf-8').read())
