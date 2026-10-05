# -*- coding: utf-8 -*-
"""TOPPING v5 yol sorunu analizi (5 Eki): carp(a, b, yol) → a, son konumdan 'yol' kadar uzaktan gelirken b'ye ilk temas (λ, nokta, derinlik).
Kullanım: python -i analiz.py  ya da import analiz as A; A.carp('teknik_on_perde', 'arayuz_kaide_M6_0', (0, 600, 0))"""
import sys, os, pickle
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'cekmece')); sys.path.insert(0, HERE)
import yol_denetim_v2 as Y
import sac_morf_t5 as SM
P = pickle.load(open('t5_parca.pkl', 'rb'))['P']
for f in sorted(os.listdir(SM.ACN_DIR)):
    ad = f[:-5]; s = SM.Sac(ad)
    pass   # 5 Eki: yol denetimi MODEL ağıyla (açınım ağı yalnız gösterim)
VEK = {}
def tri(a):
    if a not in VEK: VEK[a] = Y._vekil(P[a]['V'] / 1000.0, np.asarray(P[a]['F']))
    return VEK[a]
def kutu(a): return P[a]['V'].min(0), P[a]['V'].max(0)
def carp(a, b, yol, ofs2=(0, 0, 0)):
    """a: başlangıç ofseti yol (mm) → ofs2'ye doğru hareket; b sabit. Döner: temas listesi (λ, a-üçgen merkezi mm, derinlik mm)"""
    ofs = np.asarray(yol, float); ofs2 = np.asarray(ofs2, float); v = (ofs2 - ofs) / 1000.0
    A0 = tri(a) + ofs / 1000.0; B = tri(b)
    lam = Y.ccd(np.ascontiguousarray(A0), np.ascontiguousarray(B), v.astype(np.float64), Y.SINIR)
    m = lam < 1.5
    if not m.any(): return []
    pts = lam[m][:, None] * v[None, :]
    der = np.minimum(np.linalg.norm(pts - v[None, :], axis=1), np.linalg.norm(pts, axis=1)) * 1000
    c = A0[m].mean(1) * 1000 + pts * 1000
    o = np.argsort(-der)
    return [(round(float(lam[m][i]), 4), np.round(c[i], 1).tolist(), round(float(der[i]), 2)) for i in o[:6]]
def ozet(a):
    l, h = kutu(a); print(a, P[a].get('ac', ''), np.round(l, 1).tolist(), np.round(h, 1).tolist(), len(P[a]['F']))
print('SINIR', Y.SINIR, 'OTURMA', Y.OTURMA)
