# -*- coding: utf-8 -*-
"""m8t2: park planını (m8t2_t_park çıktısı) T geçiş parametrelerine çevir. python m8t2_t_uygula.py yollar.json plan.json cikis.json"""
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import m8t2_ana as A, m8t2_yol as Y
yj, pj, cj = sys.argv[1:4]
d = json.load(open(yj)); plan = json.load(open(pj))
adim = {}
z1 = -320.0; r_onceki = 10.0
for k, (a, s_, g_, tip, tur) in enumerate(plan):
    r = A.K[a]["r"]; z1 = z1 - (r_onceki + r + 0.6); r_onceki = r
    if tip[0] == "0": prm = None
    elif tip[0] == "2": prm = (z1, z1, tip[1])
    else: prm = (z1, z1, z1, tip[1], float(tip[2]))
    adim.setdefault(a, []).append((tur, g_, prm))
print("son düzlem z", round(z1, 1))
out = dict(d)
for a, lst in adim.items():
    k = A.K[a]
    prm_eski = [tuple(p) for p in d[a]["prm"]]
    bac = list(k["bacak"]); gec = list(k["gec"])
    parklar = [q for q in lst if q[0] == "park"]
    for j, q in enumerate(parklar):
        bac.insert(1 + j, ("z", {"x": q[1][0], "y": q[1][1]})); gec.insert(0, gec[0])
    P = [q[2] for q in lst] + prm_eski[1:]
    P = [p if p is not None else (-640.0, -640.0, "x") for p in P]
    k2 = dict(k); k2["bacak"] = bac; k2["gec"] = gec
    pts = Y.kur(k2, P)
    out[a] = dict(d[a]); out[a]["P"] = pts.tolist(); out[a]["prm"] = [list(p) for p in P]
json.dump(out, open(cj, "w"))
YL = {a: (v["r"], np.array(v["P"])) for a, v in out.items()}
c = Y.carpisma(YL)
T = [q for q in c if q[2][1] > 2090 and 3320 < q[2][0] < 3430 and q[2][2] > -700]
print("toplam", len(c), "T içinde", len(T))
for q in T: print(q[0], q[1], np.round(q[2], 1), round(q[3], 1))
