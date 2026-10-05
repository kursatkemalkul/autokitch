# -*- coding: utf-8 -*-
"""m8t2: T (toplama kanalı) yeniden diziliş — SIRALI planlayıcı. Her kablo kendi z dilimini kullanır; dilimde diğerleri sabit
(işlenmemiş = eski yerinde, işlenmiş = yeni yerinde). Kablo yolu kesit içinde 2 ya da 3 eksen hamlesi. Açgözlü + geri izleme.
python m8t2_t_sira.py giris.json cikis.json"""
import sys, os, json, random, itertools, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import m8t2_ana as A, m8t2_yol as Y
gir, cik = sys.argv[1], sys.argv[2]
d = json.load(open(gir))
TK = [a for a, k in A.K.items() if k["bacak"][0][0] == "z" and k["gec"][0][0] == "ayni" and k["bas"][-1][1] > 2100 and k["bas"][-1][2] > -300]
BX = (3327.5, 3423.5); BY = (2105.0, 2175.0); GAP = 0.4
S = {a: np.array([A.K[a]["bacak"][0][1]["x"], A.K[a]["bacak"][0][1]["y"]]) for a in TK}
Gt = {a: np.array([A.K[a]["bacak"][1][1]["x"], A.K[a]["bacak"][1][1]["y"]]) for a in TK}
R = {a: A.K[a]["r"] for a in TK}
print(len(TK), "kablo:", TK)


def seg_ok(a, p, q, sabit):
    r = R[a]
    for P in (p, q):
        if not (BX[0] + r <= P[0] <= BX[1] - r and BY[0] + r <= P[1] <= BY[1] - r): return False
    d_ = q - p; L2 = d_ @ d_
    for b, c in sabit.items():
        if L2 < 1e-12: t = 0.0
        else: t = np.clip((c - p) @ d_ / L2, 0, 1)
        if np.linalg.norm(p + t * d_ - c) < r + R[b] + GAP: return False
    return True


def yol_bul(a, sabit, rnd, deneme=200):
    s, g = S[a], Gt[a]
    secenek = []
    for u in (0, 1):
        m1 = s.copy(); m1[u] = g[u]
        secenek.append(([s, m1, g], ("2", "xy"[u])))
    for _ in range(deneme):
        u = rnd.choice((0, 1)); v = 1 - u
        rng = (BX if u == 0 else BY); m = rng[0] + R[a] + 0.5 + rnd.random() * (rng[1] - rng[0] - 2 * R[a] - 1)
        p1 = s.copy(); p1[u] = m; p2 = p1.copy(); p2[v] = g[v]
        secenek.append(([s, p1, p2, g], ("3", "xy"[u], m)))
    for pts, tip in secenek:
        if all(seg_ok(a, p, q, sabit) for p, q in zip(pts[:-1], pts[1:]) if np.linalg.norm(q - p) > 1e-6):
            return tip
    return None


def planla(seed):
    rnd = random.Random(seed)
    kalan = list(TK); rnd.shuffle(kalan); sira = []
    while kalan:
        ok = False
        for a in list(kalan):
            sabit = {b: (Gt[b] if b in [q for q, _ in sira] else S[b]) for b in TK if b != a}
            tip = yol_bul(a, sabit, rnd, deneme=60 if seed else 200)
            if tip is not None:
                sira.append((a, tip)); kalan.remove(a); ok = True; break
        if not ok: return sira, kalan
    return sira, []


best = None
for seed in range(int(os.environ.get("NS", "400"))):
    sira, kalan = planla(seed)
    if best is None or len(kalan) < len(best[1]): best = (sira, kalan); print("tohum", seed, "kalan", len(kalan), kalan, flush=True)
    if not kalan: break
sira, kalan = best
print("sıra:", [a for a, _ in sira], "çözülemeyen:", kalan)
if kalan: sys.exit(1)
Z0, DZ = -340.0, 20.0
for i, (a, tip) in enumerate(sira):
    z1 = Z0 - DZ * i; z2 = z1 - 6.0; z3 = z1 - 12.0
    j = 0
    if tip[0] == "2": prm = (z1, z2, tip[1])
    else: prm = (z1, z2, z3, tip[1], float(tip[2]))
    d[a]["prm"][0] = list(prm)
for a in A.K: d[a]["P"] = Y.kur(A.K[a], [tuple(p) for p in d[a]["prm"]]).tolist()
json.dump(d, open(cik, "w"))
YL = {a: (A.K[a]["r"], np.array(d[a]["P"])) for a in A.K}
c = Y.carpisma({a: YL[a] for a in TK})
print("T kabloları arası çakışma:", len([q for q in c if q[2][1] > 2090 and q[2][0] > 3320 and q[2][0] < 3430 and q[2][2] > -700]))
