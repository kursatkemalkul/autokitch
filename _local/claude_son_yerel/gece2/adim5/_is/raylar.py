import os, pickle, numpy as np, json
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
B = pickle.load(open(os.path.join(S, "gece2/adim5/_is/bil_hepsi.pkl"), "rb"))
DUV = [798.5, 1418.5, 1453.5, 2073.5, 2108.5, 2728.5, 2763.5, 3383.5, 3418.5, 3993.5, 4028.5]
out = []
for b in B:
    if not (b["ad"].startswith("CEK_") and b["ad"].endswith("__celik")): continue
    d = b["hi"] - b["lo"]
    if 7.5 < d[0] < 9.5 and d[2] > 500:
        w = [x for x in DUV if abs(b["lo"][0] - x) < 0.2 or abs(b["hi"][0] - x) < 0.2]
        out.append(dict(ad=b["ad"], duvar=w[0] if w else None, ylo=round(float(b["lo"][1]), 2), yhi=round(float(b["hi"][1]), 2), zlo=round(float(b["lo"][2]), 2), zhi=round(float(b["hi"][2]), 2),
                        xlo=round(float(b["lo"][0]), 2), xhi=round(float(b["hi"][0]), 2)))
out.sort(key=lambda r: (r["duvar"] or 0, r["ylo"]))
for r in out: print(r)
print(len(out))
json.dump(out, open(os.path.join(S, "gece2/adim5/_is/raylar.json"), "w"))
