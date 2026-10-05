# -*- coding: utf-8 -*-
"""m8t2: T yeniden dizilişi — ELLE sıra (18 adım, 3 park) + doğrulama -> plan json (m8t2_t_uygula girdisi). python m8t2_t_elle.py cikis_plan.json"""
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import m8t2_ana as A
TK = [a for a, k in A.K.items() if k["bacak"][0][0] == "z" and k["gec"][0][0] == "ayni" and k["bas"][-1][1] > 2100 and k["bas"][-1][2] > -300]
BX = (3327.5, 3423.5); BY = (2105.0, 2175.0); GAP = 0.4
S = {a: np.array([A.K[a]["bacak"][0][1]["x"], A.K[a]["bacak"][0][1]["y"]]) for a in TK}
Gt = {a: np.array([A.K[a]["bacak"][1][1]["x"], A.K[a]["bacak"][1][1]["y"]]) for a in TK}
R = {a: A.K[a]["r"] for a in TK}
# (kablo, hedef ('son' ya da (x,y) park), tip) · tip: ('2','x'|'y') ya da ('3', u, m)
PLAN = [("fan24", "son", ("2", "y")),
        ("K_veri", "son", ("3", "y", 2125.0)),
        ("K_guc", "son", ("3", "y", 2125.0)),
        ("ROBOT_veri", (3368.0, 2144.3), ("2", "x")),
        ("QR_guc", "son", ("3", "y", 2125.0)),
        ("ROBOT_guc", "son", ("2", "y")),
        ("bina", "son", ("2", "x")),
        ("QR_veri", "son", ("2", "x")),
        ("ROBOT_veri", "son", ("2", "x")),
        ("TOPPING_guc", (3361.0, 2146.2), ("2", "x")),
        ("E_guc", "son", ("3", "y", 2128.0)),
        ("TOPPING_veri", (3372.2, 2144.3), ("2", "x")),
        ("E_veri", "son", ("3", "y", 2128.0)),
        ("TOPPING_veri", "son", ("2", "y")),
        ("TOPPING_guc", "son", ("2", "x")),
        ("modem", "son", ("2", "x")),
        ("DOLAP_veri", "son", ("2", "y")),
        ("DOLAP_guc", "son", ("2", "y"))]


def seg_ok(a, p, q, sabit):
    r = R[a]; hata = []
    for P in (p, q):
        if not (BX[0] + r + 0.2 <= P[0] <= BX[1] - r - 0.2 and BY[0] + r + 0.2 <= P[1] <= BY[1] - r - 0.2): hata.append(("kutu", P.round(1).tolist()))
    d_ = q - p; L2 = d_ @ d_
    for b, c in sabit.items():
        t = 0.0 if L2 < 1e-12 else np.clip((c - p) @ d_ / L2, 0, 1)
        dd = np.linalg.norm(p + t * d_ - c)
        if dd < r + R[b] + GAP: hata.append((b, round(dd, 2), round(r + R[b] + GAP, 2)))
    return hata


poz = {a: S[a].copy() for a in TK}; out = []; tamam = set(); ok = True
for a, hedef, tip in PLAN:
    g = Gt[a].copy() if hedef == "son" else np.array(hedef, float)
    s = poz[a].copy()
    if tip[0] == "2":
        u = "xy".index(tip[1]); m1 = s.copy(); m1[u] = g[u]; pts = [s, m1, g]
    else:
        u = "xy".index(tip[1]); v = 1 - u; p1 = s.copy(); p1[u] = tip[2]; p2 = p1.copy(); p2[v] = g[v]; pts = [s, p1, p2, g]
    sabit = {b: poz[b] for b in TK if b != a}
    for p, q in zip(pts[:-1], pts[1:]):
        if np.linalg.norm(q - p) < 1e-6: continue
        h = seg_ok(a, p, q, sabit)
        if h: print("HATA", a, p.round(1), q.round(1), h); ok = False
    poz[a] = g; out.append((a, s.tolist(), g.tolist(), list(tip), "son" if hedef == "son" else "park"))
    if hedef == "son": tamam.add(a)
eksik = [a for a in TK if a not in tamam]
print("eksik:", eksik, "doğru" if ok and not eksik else "SORUNLU")
json.dump(out, open(sys.argv[1], "w"))
