# vida ↔ PEM: yalnız eksenel hareket → kesit (y-z) çokgenlerinin radyal girişimi = gerçek derinlik
import pickle, numpy as np, json
P = pickle.load(open('parca.pkl', 'rb'))
pem = P['cevre_pem']['V'] * 1000
def rfun(pts, c):
    a = np.arctan2(pts[:, 1] - c[1], pts[:, 0] - c[0]); r = np.hypot(pts[:, 0] - c[0], pts[:, 1] - c[1])
    # dış zarf (her açı diliminde en büyük) → çokgen
    o = np.argsort(a); a, r = a[o], r[o]
    P2 = np.stack([r * np.cos(a), r * np.sin(a)], 1)
    def R(th):
        d = np.array([np.cos(th), np.sin(th)]); best = 0
        n = len(P2)
        for i in range(n):
            p, q = P2[i], P2[(i + 1) % n]
            M = np.array([d, p - q]).T
            if abs(np.linalg.det(M)) < 1e-12: continue
            s, u = np.linalg.solve(M, p)
            if s > 0 and -1e-9 <= u <= 1 + 1e-9: best = max(best, s)
        return best
    return R
res = {}
for s, xp in (('sol', 1452.3), ('sag', 2074.7)):
    for k in (1, 2, 3):
        v = P['vida_%s_%d' % (s, k)]['V'] * 1000; c3 = (v.min(0) + v.max(0)) / 2; c = c3[1:]
        rv = np.hypot(v[:, 1] - c[0], v[:, 2] - c[1]); sh = v[rv < 2.6][:, 1:]
        near = pem[(np.abs(pem[:, 2] - c3[2]) < 6) & (np.abs(pem[:, 1] - c3[1]) < 6) & (np.abs(pem[:, 0] - xp) < 1.3)]
        rb = np.hypot(near[:, 1] - c[0], near[:, 2] - c[1]); bore = near[rb < 3.0][:, 1:]
        RS = rfun(sh, c); RB = rfun(bore, c)
        th = np.linspace(-np.pi, np.pi, 1441)
        d = max(RS(t) - RB(t) for t in th)
        res['vida_%s_%d' % (s, k)] = round(float(d), 3)
print(json.dumps(res)); json.dump(res, open('dis_derinlik.json', 'w'))
