# -*- coding: utf-8 -*-
"""bir dikey eksen (x,z) etrafında r içinde kutusu olan bileşenler"""
import json, sys
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
B = json.load(open(S + r"\gece2\menu7\m\bil_v9t.json", encoding="utf-8"))
x, z, r, y0, y1 = map(float, sys.argv[1:6])
for o in B:
    lo, hi = o["lo"], o["hi"]
    if hi[0] < x - r or lo[0] > x + r or hi[2] < z - r or lo[2] > z + r or hi[1] < y0 or lo[1] > y1: continue
    if len(sys.argv) > 6 and o["mek"] and not any(o["mek"].find(q) >= 0 for q in sys.argv[6].split(",")): continue
    print("%-44s %4d %-18s k%s %s x %7.1f %7.1f  y %7.1f %7.1f  z %7.1f %7.1f  n%d" % (o["d"], o["no"], o["mek"], o["kat"], "K" if o["kapali"] else "a",
          lo[0], hi[0], lo[1], hi[1], lo[2], hi[2], o["n"]))
