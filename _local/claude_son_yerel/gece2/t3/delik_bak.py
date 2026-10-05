import sys, pickle, numpy as np
sys.stdout.reconfigure(encoding='utf-8')
D = pickle.load(open('plan_t3.pkl', 'rb')); P = D['P']
def kes(ad, z0, z1):
    V = P[ad]['V']; T = V[P[ad]['F']]; m = (T[:, :, 2].min(1) < z1) & (T[:, :, 2].max(1) > z0); return T[m].reshape(-1, 3)
for mot in sys.argv[1:]:
    Vm = P[mot]['V']
    for wall, z0, z1 in (('soguk_arka_dis_sac', -630, -628), ('pu_levha_arka', -626, -575), ('astar_arka', -571, -570)):
        Q = kes(wall, z0, z1)
        Mm = Vm[(Vm[:, 2] > z0 - 0.5) & (Vm[:, 2] < z1 + 0.5)]
        if not len(Mm): print(mot, wall, 'bu z aralığında ürün yok'); continue
        lo, hi = Mm.min(0), Mm.max(0); c = (lo + hi) / 2
        # duvar köşeleri ürün kesit kutusuna yakın
        near = Q[(np.abs(Q[:, 0] - c[0]) < (hi[0] - lo[0]) / 2 + 15) & (np.abs(Q[:, 1] - c[1]) < (hi[1] - lo[1]) / 2 + 15)]
        r_urun = np.hypot(Mm[:, 0] - c[0], Mm[:, 1] - c[1]).max()
        r_del = np.hypot(near[:, 0] - c[0], near[:, 1] - c[1]).min() if len(near) else None
        print('%-18s %-20s ürün kesit %s merkez %s r_ürün %.2f · duvar en yakın köşe r %s' % (mot, wall, np.round(hi - lo, 1).tolist(), np.round(c[:2], 1).tolist(), r_urun, None if r_del is None else round(r_del, 2)))
