import json, io, re, sys
L = json.load(io.open(sys.argv[1], encoding="utf-8"))
U = {}
for b, a, m, g, bb in L:
    u = U.setdefault(b, [1e9, -1e9, 1e9, -1e9, 1e9, -1e9, 0])
    for k in range(3):
        u[2*k] = min(u[2*k], bb[2*k]); u[2*k+1] = max(u[2*k+1], bb[2*k+1])
    u[6] += 1
for b, u in U.items():
    if not b.startswith("CEK_"):
        print("%-22s n%-4d x %7.1f..%7.1f  y %7.1f..%7.1f  z %7.1f..%7.1f" % (b, u[6], *u[:6]))
