import pickle, json, numpy as np, trimesh
D = pickle.load(open('plan_b4.pkl', 'rb')); P = D['P']; HAR = D['HAR']; GOR = D['GOR']
H = ['g_dis_arka_ek_lamasi', 'g_pu_arka_alcak_arka', 'g_pu_arka_yuksek_arka', 'ic_kanal_57', 'istasyon_kutusu', 'sase_boy_arka', 'sase_boy_on', 'tasiyici_dikme_3386_600', 'tasiyici_plaka_-484', 'tasiyici_plaka_-574', 'zemin_conta']
ads = [a for a in P if a in GOR]
son = {a: max([h[1] for h in HAR[a]] + [GOR[a]]) for a in ads}
imz = {a: json.dumps(HAR[a]) for a in ads}
lo = {a: P[a]['V'].min(0) for a in ads}; hi = {a: P[a]['V'].max(0) for a in ads}
for s in H:
    tl = son[s]; best = []
    TS = trimesh.Trimesh(P[s]['V'], np.asarray(P[s]['F']), process=False)
    for b in ads:
        if b == s or son[b] > tl + 1e-6: continue
        if np.any(lo[b] > hi[s] + 5) or np.any(hi[b] < lo[s] - 5): continue
        V = P[b]['V']; m = np.all(V >= lo[s] - 5, 1) & np.all(V <= hi[s] + 5, 1)
        d = 99
        if m.any(): d = trimesh.proximity.closest_point(TS, V[m][:3000])[1].min()
        best.append((round(float(d), 3), b, 'AYNI' if imz[b] == imz[s] else ''))
    best.sort(); print(s, P[s]['tur'], 't', tl, 'y', round(lo[s][1], 1), best[:4])
