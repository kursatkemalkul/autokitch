import sys, numpy as np
sys.path.insert(0, r"@@KOK_W@@\gece")
import glbkit
G = glbkit.Glb(sys.argv[1]); nm = sys.argv[2]; xd = float(sys.argv[3]); ref = list(map(float, sys.argv[4:7]))
p = G.bul(nm); tl, kut = G.komp(p)
X = p['X']; T = p['T']; vis = G.gorunur(p)
d = np.linalg.norm(X - ref, axis=1); v0 = np.argmin(d); print('ref dist', d[v0])
ci = tl[np.where((T == v0).any(1))[0][0]]
P = X[T]
m = vis & (tl == ci) & (np.abs(P[:, :, 0] - xd).max(1) < 0.02)
print('yuz ucgen', m.sum(), 'bilesen', kut[ci])
Q = np.round(P[m][:, :, 1:], 2)
from collections import Counter
E = Counter()
for t in Q:
    for k in range(3):
        a = tuple(t[k]); b = tuple(t[(k + 1) % 3]); E[(min(a, b), max(a, b))] += 1
B = [e for e, n in E.items() if n == 1]
print('sinir kenar', len(B))
# halkalar
adj = {}
for a, b in B: adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
seen = set(); loops = []
for s in adj:
    if s in seen: continue
    L = [s]; seen.add(s); cur = s; prev = None
    while True:
        nx = [q for q in adj[cur] if q != prev and q not in seen]
        if not nx: break
        prev, cur = cur, nx[0]; L.append(cur); seen.add(cur)
    loops.append(L)
for L in loops:
    A = np.array(L); ar = 0.5 * abs(np.dot(A[:, 0], np.roll(A[:, 1], 1)) - np.dot(A[:, 1], np.roll(A[:, 0], 1)))
    print('halka', len(L), 'alan', round(ar), 'y', A[:, 0].min(), A[:, 0].max(), 'z', A[:, 1].min(), A[:, 1].max())
