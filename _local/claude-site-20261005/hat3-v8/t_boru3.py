import sys, os, math, random, time
sys.path.insert(0, "h3"); sys.path.insert(0, ".")
import cadquery as cq
V = cq.Vector


def silx(a, b, r):
    d = V(*b) - V(*a); return cq.Solid.makeCylinder(r, d.Length, V(*a), d.normalized())


def boru2(pts, r):
    q = [pts[0]]
    for p in pts[1:]:
        if math.dist(p, q[-1]) > 1e-6: q.append(p)
    ss = []
    n = len(q)
    for i, (a, b) in enumerate(zip(q[:-1], q[1:])):
        L = math.dist(a, b); d = [(b[k] - a[k]) / L for k in range(3)]
        a2 = tuple(a[k] - d[k] * r for k in range(3)) if i > 0 else a
        b2 = tuple(b[k] + d[k] * r for k in range(3)) if i < n - 2 else b
        ss.append(silx(a2, b2, r))
    if len(ss) == 1: return ss[0]
    s = ss[0]
    for x in ss[1:]: s = s.fuse(x)
    return s.clean()


random.seed(3)
bad = 0; t0 = time.time()
for it in range(40):
    p = [0.0, 0.0, 0.0]; pts = [tuple(p)]
    for k in range(random.randint(5, 40)):
        ax = random.randint(0, 2); p[ax] += random.choice([-1, 1]) * random.choice([0.3, 4, 8, 12, 40, 120]); pts.append(tuple(p))
    r = random.choice([2.0, 2.5, 3.0, 4.5])
    s = boru2(pts, r)
    nso = len(s.Solids()); v = s.Volume()
    alt = sum(math.pi * r * r * math.dist(a, b) for a, b in zip(pts[:-1], pts[1:]))
    if nso != 1 or v < 0.7 * alt: bad += 1; print("KÖTÜ", it, nso, round(v), round(alt))
print("kötü", bad, "/ 40", round(time.time() - t0), "sn")
sys.stdout.flush(); os._exit(0)
