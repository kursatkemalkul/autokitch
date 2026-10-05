import pickle, numpy as np, re, collections, json
P = pickle.load(open('e_parca.pkl', 'rb'))['P']
S = [a for a in P if P[a]['tur'] in ('sac', 'profil')]
OUT = {}
for a in sorted(P):
    if not (a.endswith('saplama') or a.startswith(('arayuz_mek', 'arayuz_j3', 'govde_pem'))): continue
    V = P[a]['V']; lo, hi = V.min(0), V.max(0); e = int(np.argmax(hi - lo)); c = (lo + hi) / 2
    oth = [i for i in range(3) if i != e]
    best = None
    for s in S:
        W = P[s]['V']
        m = np.all(np.abs(W[:, oth] - c[oth]) < 12, 1) & (W[:, e] >= lo[e] - 1) & (W[:, e] <= hi[e] + 1)
        if m.sum() < 3: continue
        smin, smax = W[m, e].min(), W[m, e].max()
        for uc, sgn in ((lo[e], -1), (hi[e], 1)):
            if abs(smin - uc) < 0.3 or abs(smax - uc) < 0.3:
                # baş bu uçta: saplama sacdan diğer uca doğru çıkar → yan = baş tarafı
                y = np.zeros(3); y[e] = sgn
                if best is None or (P[s]['tur'] == 'sac' and P[best[0]]['tur'] != 'sac'): best = (s, y.tolist())
    OUT[a] = best
c = collections.Counter((re.sub(r'_\d+', '#', a), b[0] if b else None, tuple(b[1]) if b else None) for a, b in OUT.items())
for k, n in sorted(c.items(), key=str): print(n, k)
json.dump(OUT, open('host.json', 'w'))
