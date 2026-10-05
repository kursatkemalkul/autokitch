import pickle, json, numpy as np, trimesh
D = pickle.load(open('plan_b4.pkl', 'rb')); P = D['P']; HAR = D['HAR']; GOR = D['GOR']
H = ['ic_kanal_57', 'tasiyici_dikme_3386_600', 'tasiyici_plaka_-484', 'zemin_conta', 'istasyon_kutusu']
ads = list(P)
son = {a: max([h[1] for h in HAR[a]] + [GOR.get(a, 0)]) if a in HAR else -1 for a in ads}
lo = {a: P[a]['V'].min(0) for a in ads}; hi = {a: P[a]['V'].max(0) for a in ads}
for s in H:
    TS = trimesh.Trimesh(P[s]['V'], np.asarray(P[s]['F']), process=False); best = []
    for b in ads:
        if b == s: continue
        if np.any(lo[b] > hi[s] + 3) or np.any(hi[b] < lo[s] - 3): continue
        V = P[b]['V']; m = np.all(V >= lo[s] - 3, 1) & np.all(V <= hi[s] + 3, 1)
        d = 99
        if m.any(): d = trimesh.proximity.closest_point(TS, V[m][:4000])[1].min()
        best.append((round(float(d), 3), b, son[b]))
    best.sort(); print(s, son[s], lo[s].round(1), hi[s].round(1), best[:6])
