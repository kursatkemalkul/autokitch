# U sac levhalarının (kutu yaklaşımı) içine giren diğer düğüm noktaları
import sys; sys.path.insert(0, '..'); sys.path.insert(0, '../tg')
import numpy as np
from glbx import yukle
from u_ortak import ornekle
J, D = yukle(sys.argv[1])
LEV = {}
for k, (x0, x1) in (("F", (2500., 4000.)), ("KE", (4000., 5230.))):
    LEV[k + "_taban"] = (x0, x1, 1862., 1863.5, -828.5, 59.)
    LEV[k + "_tavan"] = (x0, x1, 2198.5, 2200., -828.5, 59.)
    LEV[k + "_arka"] = (x0, x1, 1862., 2200., -830., -828.5)
    LEV[k + "_yan_sol"] = (x0, x0 + 1.5, 1863.5, 2198.5, -828.5, 59.)
    LEV[k + "_yan_sag"] = (x1 - 1.5, x1, 1863.5, 2198.5, -828.5, 59.)
Z = (2490, 5240, 1855, 2205, -835, 65)
T = 0.05
for nd, d in D.items():
    if nd.startswith(("U_F_GOVDE", "U_KE_GOVDE")): continue
    P = d["X"][d["T"][d["ok"]]]
    m = (P[:, :, 0].max(1) > Z[0]) & (P[:, :, 0].min(1) < Z[1]) & (P[:, :, 1].max(1) > Z[2]) & (P[:, :, 1].min(1) < Z[3]) & (P[:, :, 2].max(1) > Z[4]) & (P[:, :, 2].min(1) < Z[5])
    if not m.any(): continue
    Q, _ = ornekle(P[m], Z, 4.0, 60)
    for ad, b in LEV.items():
        mm = (Q[:, 0] > b[0] + T) & (Q[:, 0] < b[1] - T) & (Q[:, 1] > b[2] + T) & (Q[:, 1] < b[3] - T) & (Q[:, 2] > b[4] + T) & (Q[:, 2] < b[5] - T)
        if mm.any():
            R = Q[mm]; print("%-10s %-44s %6d  %s … %s" % (ad, nd, mm.sum(), R.min(0).round(1).tolist(), R.max(0).round(1).tolist()))
