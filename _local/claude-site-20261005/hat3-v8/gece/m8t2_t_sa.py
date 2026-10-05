# -*- coding: utf-8 -*-
"""m8t2: T (toplama kanalı) geçişi için tavlama (SA) — yalnız T kablolarının ilk 'ayni' geçişi. python m8t2_t_sa.py giris.json cikis.json iter seed"""
import sys, os, json, random, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import m8t2_ana as A, m8t2_yol as Y
gir, cik, N, seed = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
d = json.load(open(gir)); rnd = random.Random(seed)
PP = {a: [tuple(p) for p in d[a]["prm"]] for a in A.K}
TK = [a for a, k in A.K.items() if k["bacak"][0][0] == "z" and abs(k["bas"][-1][2]) < 300 and k["gec"][0][0] == "ayni"]
print("T kabloları", TK)
BB = (np.array([3300.0, 2090.0, -705.0]), np.array([3450.0, 2185.0, -120.0]))


def kes(P):
    """yolun T kutusu içindeki kısmı (z > -705)"""
    return P


def maliyet(YL):
    c = Y.carpisma({a: YL[a] for a in TK})
    s = 0.0; n = 0
    for a, b, m, dd in c:
        if np.all(m >= BB[0]) and np.all(m <= BB[1]): s += dd + 10; n += 1
    dis = 0
    return s + 5 * dis, n


YL = {a: (A.K[a]["r"], Y.kur(A.K[a], PP[a])) for a in TK}
cur, n = maliyet(YL); best = (cur, {a: list(PP[a]) for a in TK}); print("başlangıç", round(cur, 1), n)
T0 = 30.0
for it in range(N):
    temp = T0 * (1 - it / N) + 0.5
    a = rnd.choice(TK); k = A.K[a]; g = k["gec"][0]; lo, hi = g[1], g[2]
    cr = ["x", "y"]
    old = PP[a][0]
    r = rnd.random()
    if r < 0.4 and len(old) == 3:                       # yerel oynatma
        t1 = min(hi, max(lo, old[0] + rnd.gauss(0, 25))); t2 = min(hi, max(lo, old[1] + rnd.gauss(0, 25)))
        ts = sorted([t1, t2], reverse=True); new = (ts[0], ts[1], old[2] if rnd.random() < 0.8 else rnd.choice(cr))
    elif r < 0.7:
        ts = sorted([lo + rnd.random() * (hi - lo) for _ in range(2)], reverse=True); new = (ts[0], ts[1], rnd.choice(cr))
    else:
        ts = sorted([lo + rnd.random() * (hi - lo) for _ in range(3)], reverse=True); u = rnd.choice(cr)
        rg = g[4][u]; m_ = rg[0] + k["r"] + 0.5 + rnd.random() * (rg[1] - rg[0] - 2 * k["r"] - 1)
        new = (ts[0], ts[1], ts[2], u, m_)
    P2 = list(PP[a]); P2[0] = new
    YL2 = dict(YL); YL2[a] = (k["r"], Y.kur(k, P2))
    s2, n2 = maliyet(YL2)
    if s2 <= cur or rnd.random() < math.exp(-(s2 - cur) / temp):
        PP[a] = P2; YL = YL2; cur = s2
        if s2 < best[0]: best = (s2, {a_: list(PP[a_]) for a_ in TK}); print(it, "en iyi", round(s2, 1), n2, flush=True)
    if best[0] <= 0: break
for a in TK: d[a]["prm"] = [list(p) for p in best[1][a]]
for a in A.K: d[a]["P"] = Y.kur(A.K[a], [tuple(p) for p in d[a]["prm"]]).tolist()
json.dump(d, open(cik, "w"))
print("bitti", round(best[0], 1))
