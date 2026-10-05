import json, sys
P = json.load(open(r"b3/otonom/hat3d/v3/parca_kutulari.json", encoding="utf-8"))["parca"]
X0,X1,Y0,Y1,Z0,Z1 = map(float, sys.argv[1:7]); pre = sys.argv[7] if len(sys.argv) > 7 else ""
for b, l in P.items():
    if pre and not b.startswith(pre): continue
    for p in l:
        n, _, x0, x1, y0, y1, z0, z1 = p[:8]
        if x1 > X0 and x0 < X1 and y0 < Y1 and y1 > Y0 and z0 < Z1 and z1 > Z0:
            print(b[:16].ljust(16), n[:40].ljust(40), round(x0), round(x1), "y", round(y0), round(y1), "z", round(z0), round(z1))
