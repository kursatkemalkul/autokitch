import sys, numpy as np
sys.path.insert(0, r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\gece")
import glbkit
for f in sys.argv[1:]:
    G = glbkit.Glb(f); p = G.bul("TOPPING_MODUL__sac"); X = p['X']; T = p['T'][G.gorunur(p)]
    P = X[T]; m = (np.abs(P[:, :, 0] - 2500).max(1) < 0.02) & (P[:, :, 1].min(1) >= 891) & (P[:, :, 2].max(1) <= 40) & (P[:, :, 2].min(1) >= -831)
    Q = P[m][:, :, 1:]
    a = 0.5 * np.abs((Q[:, 1, 0] - Q[:, 0, 0]) * (Q[:, 2, 1] - Q[:, 0, 1]) - (Q[:, 2, 0] - Q[:, 0, 0]) * (Q[:, 1, 1] - Q[:, 0, 1]))
    print(f, 'yuz alan', round(a.sum()))
