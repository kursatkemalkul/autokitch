# -*- coding: utf-8 -*-
import json, sys
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
B = json.load(open(S + r"\gece2\menu7\m\bil_v9t.json", encoding="utf-8"))
pat = sys.argv[1]
for o in B:
    if (o["mek"] or "") .find(pat) >= 0 or o["d"].find(pat) >= 0:
        if len(sys.argv) > 2:
            x0, x1, y0, y1 = map(float, sys.argv[2:6])
            if o["hi"][0] < x0 or o["lo"][0] > x1 or o["hi"][1] < y0 or o["lo"][1] > y1: continue
        print("%-44s %4d %-18s k%s %s x %7.1f %7.1f  y %7.1f %7.1f  z %7.1f %7.1f  n%d" % (o["d"], o["no"], o["mek"], o["kat"], "K" if o["kapali"] else "a",
              o["lo"][0], o["hi"][0], o["lo"][1], o["hi"][1], o["lo"][2], o["hi"][2], o["n"]))
