# -*- coding: utf-8 -*-
"""m8t2: T yeniden diziliş — park yerli sıralı planlayıcı. Her kablo en çok 1 park (ara konum) + son konum; her hamle kendi z diliminde.
python m8t2_t_park.py giris.json cikis.json"""
import sys, os, json, random, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import m8t2_ana as A, m8t2_yol as Y
gir, cik = sys.argv[1], sys.argv[2]
d = json.load(open(gir))
TK = [a for a, k in A.K.items() if k["bacak"][0][0] == "z" and k["gec"][0][0] == "ayni" and k["bas"][-1][1] > 2100 and k["bas"][-1][2] > -300]
BX = (3327.5, 3423.5); BY = (2105.0, 2175.0); GAP = 0.4
S = {a: np.array([A.K[a]["bacak"][0][1]["x"], A.K[a]["bacak"][0][1]["y"]]) for a in TK}
Gt = {a: np.array([A.K[a]["bacak"][1][1]["x"], A.K[a]["bacak"][1][1]["y"]]) for a in TK}
R = {a: A.K[a]["r"] for a in TK}


def seg_ok(a, p, q, sabit):
    r = R[a]
    for P in (p, q):
        if not (BX[0] + r + 0.2 <= P[0] <= BX[1] - r - 0.2 and BY[0] + r + 0.2 <= P[1] <= BY[1] - r - 0.2): return False
    d_ = q - p; L2 = d_ @ d_
    for b, c in sabit.items():
        t = 0.0 if L2 < 1e-12 else np.clip((c - p) @ d_ / L2, 0, 1)
        if np.linalg.norm(p + t * d_ - c) < r + R[b] + GAP: return False
    return True


def yollar(a, s, g, rnd, n3=40):
    out = []
    for u in (0, 1):
        m1 = s.copy(); m1[u] = g[u]; out.append(([s, m1, g], ("2", "xy"[u])))
    for _ in range(n3):
        u = rnd.choice((0, 1)); v = 1 - u
        rng = (BX if u == 0 else BY); m = rng[0] + R[a] + 0.5 + rnd.random() * (rng[1] - rng[0] - 2 * R[a] - 1)
        p1 = s.copy(); p1[u] = m; p2 = p1.copy(); p2[v] = g[v]; out.append(([s, p1, p2, g], ("3", "xy"[u], m)))
    return out


def gecer(a, s, g, sabit, rnd, n3=40):
    if np.linalg.norm(s - g) < 1e-6: return ("0",)
    for pts, tip in yollar(a, s, g, rnd, n3):
        if all(seg_ok(a, p, q, sabit) for p, q in zip(pts[:-1], pts[1:]) if np.linalg.norm(q - p) > 1e-6): return tip
    return None


def planla(seed, maxadim=int(os.environ.get("MA", "40"))):
    rnd = random.Random(seed)
    poz = {a: S[a].copy() for a in TK}; park = {}; bitti = set(); adimlar = []
    for _ in range(maxadim):
        if len(bitti) == len(TK): return adimlar, []
        aday = [a for a in TK if a not in bitti]; rnd.shuffle(aday)
        hamle = None
        if rnd.random() < float(os.environ.get("PP", "0.0")): aday_park = True
        else: aday_park = False
        for a in aday:
            sabit = {b: poz[b] for b in TK if b != a}
            tip = gecer(a, poz[a], Gt[a], sabit, rnd)
            if tip is not None: hamle = (a, poz[a].copy(), Gt[a].copy(), tip, "son"); break
        if hamle is None:                                   # park: (bitmiş olsa da) bir kabloyu boş bir yere
            hepsi = list(TK); rnd.shuffle(hepsi)
            for a in hepsi:
                if park.get(a, 0) >= int(os.environ.get("NP", "2")): continue
                sabit = {b: poz[b] for b in TK if b != a}
                for _ in range(30):
                    q = np.array([BX[0] + R[a] + 1 + rnd.random() * (BX[1] - BX[0] - 2 * R[a] - 2), BY[0] + R[a] + 1 + rnd.random() * (BY[1] - BY[0] - 2 * R[a] - 2)])
                    if any(np.linalg.norm(q - poz[b]) < R[a] + R[b] + GAP + 1 for b in TK if b != a): continue
                    if any(np.linalg.norm(q - Gt[b]) < R[a] + R[b] + GAP for b in TK if b != a and b not in bitti): continue
                    tip = gecer(a, poz[a], q, sabit, rnd, 20)
                    if tip is not None: hamle = (a, poz[a].copy(), q, tip, "park"); break
                if hamle: break
        if hamle is None: return adimlar, [a for a in TK if a not in bitti]
        a, s_, g_, tip, tur = hamle
        adimlar.append(hamle); poz[a] = g_.copy()
        if tur == "park": park[a] = park.get(a, 0) + 1; bitti.discard(a)
        else: bitti.add(a)
    return adimlar, [a for a in TK if a not in bitti]


best = None
S0 = int(os.environ.get("S0", "0"))
for seed in range(S0, S0 + int(os.environ.get("NS", "3000"))):
    ad, kalan = planla(seed)
    if best is None or len(kalan) < len(best[1]): best = (ad, kalan); print("tohum", seed, "kalan", len(kalan), kalan, "adım", len(ad), flush=True)
    if not kalan: break
ad, kalan = best
if kalan: print("çözülemedi", kalan); sys.exit(1)
print("adımlar:", [(a, t) for a, _, _, _, t in ad])
json.dump([(a, s_.tolist(), g_.tolist(), list(tip), t) for a, s_, g_, tip, t in ad], open(cik, "w"))
