# -*- coding: utf-8 -*-
"""v2 yeni gövde parçaları ↔ modelin geri kalanı (t_bil, v9l_T: TOPPING_GOVDE / KAIDE_C ve v8zq'da yerine geçilen evaporatör sekmeleri hariç) · manifold hacim"""
import pickle, sys, numpy as np, manifold3d as mf, re
sys.stdout.reconfigure(encoding='utf-8')
N = pickle.load(open('v2_parca.pkl', 'rb'))
B = pickle.load(open('t_bil.pkl', 'rb'))['L']
YENI = re.compile(r'^(servis_arka_.*_(burc|vida|punta_\d)|astar_|evaporator_ay|kanal_|derz_|pu_levha|yapistirici|arayuz_kb_.*_pul)')


def man(V, F):
    try:
        m = mf.Manifold(mf.Mesh(vert_properties=np.asarray(V, np.float32), tri_verts=np.asarray(F, np.uint32)))
        return m if m.status() == mf.Error.NoError and m.volume() > 1e-6 else None
    except Exception:
        return None


def kaynak(V, F):
    u, inv = np.unique(np.round(V[F.reshape(-1)], 4), axis=0, return_inverse=True)
    return u, inv.reshape(-1, 3)


eski_sekme = lambda o: o['dug'] == 'TOPPING_MODUL__sac' and abs(o['lo'][2] + 828.5) < 0.1 and abs(o['hi'][2] + 826) < 0.1
DIS = [o for o in B if not o['dug'].startswith(('TOPPING_GOVDE', 'KAIDE_C')) and not eski_sekme(o)]
MD = {}
sonuc = []
for a, (V, F, tur, mal, vol) in N.items():
    if not YENI.match(a): continue
    m = man(*kaynak(V, F))
    if m is None: print('AÇIK AĞ', a); continue
    lo, hi = V.min(0), V.max(0)
    for i, o in enumerate(DIS):
        if np.any(o['lo'] > hi + 0.01) or np.any(o['hi'] < lo - 0.01): continue
        if i not in MD: MD[i] = man(*kaynak(o['V'], o['F']))
        mo = MD[i]
        if mo is None:
            # açık ağ: köşe noktaları parça içinde mi (kaba)
            continue
        v = (m ^ mo).volume()
        if v > 0.05: sonuc.append((round(v, 2), a, o['dug'], np.round(o['lo']).astype(int).tolist(), np.round(o['hi']).astype(int).tolist()))
sonuc.sort(reverse=True)
print('ÇAKIŞMA (>0,05 mm³):', len(sonuc))
for s in sonuc[:60]: print('  ', s)
acik = sum(1 for i, m in MD.items() if m is None)
print('karşı taraf açık ağ (denetlenemedi):', acik, '/', len(MD))
