# -*- coding: utf-8 -*-
"""adım 53'te açılan delikleri açınım JSON'larına ekle (üst raf r 19,45 · raf r 18,5 · alt sac r 15,5 · arka iç sac burç r 15,25) → yerel koordinat (donusum_3b tersi)"""
import json, os, numpy as np, pickle, sys
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE); sys.path.insert(0, HERE); sys.stdout.reconfigure(encoding='utf-8')
import sac_morf_t5 as SM, trimesh
DEL = {'ust_raf': ((1911.5, 1575.0, -170.0), 19.45), 'raf': ((1911.5, 1149.0, -169.8), 18.5), 'soguk_alt_sac': ((1911.5, 1110.5, -169.8), 15.5), 'astar_arka': ((2031.25, 1613.5, -570.0), 15.25)}
P = pickle.load(open('t5_parca.pkl', 'rb'))['P']
for ad, (c, r) in DEL.items():
    f = os.path.join(SM.ACN_DIR, ad + '.json'); d = json.load(open(f, encoding='utf-8'))
    if any(k[0].get('t') == 'C' and abs(k[0]['r'] - r) < 1e-6 and k[0].get('adim53') for k in d['ic_konturlar']): print(ad, 'zaten'); continue
    M = np.array(d['donusum_3b']); Mi = np.linalg.inv(M)
    p = Mi @ np.array([c[0], c[1], c[2], 1.0]); print(ad, 'yerel', np.round(p[:3], 3), 't', d['t'])
    d['ic_konturlar'].append([{'t': 'C', 'c': [float(p[0]), float(p[1])], 'r': r, 'adim53': True}])
    d['kesikler'].append(dict(panel=ad, tip='dusme_deligi_adim53', sekil='daire', merkez_duz=[float(p[0]), float(p[1])], parca='adım 53 kıyma düşme hattı deliği', cap=2 * r))
    json.dump(d, open(f, 'w', encoding='utf-8'), ensure_ascii=False)
# doğrulama: her sacın bükülmüş açınımı ↔ model bileşeni (nokta → yüzey uzaklığı, iki yönlü)
kot = []
for f in sorted(os.listdir(SM.ACN_DIR)):
    ad = f[:-5]; s = SM.Sac(ad); X = s.dunya(s.yerel({})); V, F = P[ad]['V'], P[ad]['F']
    tm = trimesh.Trimesh(X, s.F, process=False); tv = trimesh.Trimesh(V, F, process=False)
    d1 = trimesh.proximity.closest_point(tm, V[np.random.RandomState(0).permutation(len(V))[:4000]])[1].max()
    d2 = trimesh.proximity.closest_point(tv, X[np.random.RandomState(0).permutation(len(X))[:4000]])[1].max()
    kb = max(np.abs(X.min(0) - V.min(0)).max(), np.abs(X.max(0) - V.max(0)).max())
    print('%-26s nb %d  kutu %.4f  model→açınım %.3f  açınım→model %.3f' % (ad, len(s.bukum), kb, d1, d2))
    if max(d1, d2) > 0.5: kot.append(ad)
print('KÖTÜ', kot)
