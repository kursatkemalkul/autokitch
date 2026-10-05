import json, io, re, sys
L = json.load(io.open(sys.argv[1], encoding="utf-8"))
print("--- yere yakin yatay (ymax<=40, alan>20000)")
for b, a, m, g, bb in L:
    x0, x1, y0, y1, z0, z1 = bb
    if y1 <= 40 and (x1 - x0) * (z1 - z0) > 20000:
        print(b, a, m, g, bb)
print("--- ayaklar ornek")
n = 0
for b, a, m, g, bb in L:
    if re.search(r"ayak", a) and bb[2] < 5:
        n += 1
        if n < 400: print(b, a, m, bb)
print("ayak sayisi", n)
xs = [bb for b, a, m, g, bb in L]
print("TUM BBOX", min(v[0] for v in xs), max(v[1] for v in xs), min(v[2] for v in xs), max(v[3] for v in xs), min(v[4] for v in xs), max(v[5] for v in xs))
