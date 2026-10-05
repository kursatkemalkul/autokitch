# -*- coding: utf-8 -*-
"""bir parça grubunun hangi yönden (doğrusal) gelebileceğini dener: grup → final, engeller sabit"""
import sys, os, pickle, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'adim6')); sys.stdout.reconfigure(encoding='utf-8')
import yol_denetim as Y
P = pickle.load(open('parca.pkl', 'rb'))
grup = sys.argv[1].split(','); eng = sys.argv[2].split(',') if sys.argv[2] != 'hepsi' else [a for a in P if a not in grup]
mesafe = float(sys.argv[3]) / 1000 if len(sys.argv) > 3 else 0.06
A = np.concatenate([P[a]['V'][P[a]['F']] for a in grup])
for yon in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
    v = -np.array(yon, float) * mesafe            # başlangıç = final + yon*mesafe, hareket v
    A0 = A - v
    sonuc = []
    for b in eng:
        B = P[b]['V'][P[b]['F']]
        lam = Y.ccd(np.ascontiguousarray(A0), np.ascontiguousarray(B), v, Y.SINIR)
        m = lam < 1.5
        if m.any():
            d = (1 - lam[m].min()) * mesafe * 1000   # finalden uzaklık (mm)
            if d > 1.0: sonuc.append((b, round(d, 1)))
    print(yon, 'TEMIZ' if not sonuc else sonuc)
