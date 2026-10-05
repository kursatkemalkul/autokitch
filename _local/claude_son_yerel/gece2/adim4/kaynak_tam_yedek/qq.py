import sys, re, json, io
L = json.load(io.open(sys.argv[1], encoding="utf-8"))
x0, x1, y0, y1, z0, z1 = map(float, sys.argv[2:8]); pat = sys.argv[8] if len(sys.argv) > 8 else "."
def ust(a, b): return a[0] < b[1] and b[0] < a[1] and a[2] < b[3] and b[2] < a[3] and a[4] < b[5] and b[4] < a[5]
for b, a, m, g, bb in L:
    if ust((x0, x1, y0, y1, z0, z1), bb) and re.search(pat, b + "|" + a):
        print("%-60s %-10s x %7.1f %7.1f  y %7.1f %7.1f  z %7.1f %7.1f" % (b + "|" + a, g[:10], *bb))
