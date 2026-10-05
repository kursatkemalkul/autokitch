import json, sys
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
B = json.load(open(S + r"\gece2\menu7\m\bil_v9t.json", encoding="utf-8"))
x0,x1,y0,y1,z0,z1 = map(float, sys.argv[1:7])
for o in B:
    lo, hi = o["lo"], o["hi"]
    if hi[0] <= x0 or lo[0] >= x1 or hi[1] <= y0 or lo[1] >= y1 or hi[2] <= z0 or lo[2] >= z1: continue
    print("%-40s %4d %-18s k%s %s x %7.1f %7.1f  y %7.1f %7.1f  z %7.1f %7.1f  n%d" % (o["d"], o["no"], o["mek"], o["kat"], "K" if o["kapali"] else "a", lo[0], hi[0], lo[1], hi[1], lo[2], hi[2], o["n"]))
