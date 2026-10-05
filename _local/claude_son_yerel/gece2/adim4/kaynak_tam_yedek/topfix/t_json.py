# -*- coding: utf-8 -*-
"""mekanizma_v3_8.json: 'kutu' (unite sinir kutusu, m) yeni modelden yeniden · glb surum etiketi. python t_json.py npz_dizini json_yolu etiket"""
import sys, json, numpy as np
d, js, et = sys.argv[1:4]
J = json.load(open(js, encoding="utf-8"))
D = np.load(d + "/m8_onbellek.npz"); M = [m["kod"] for m in json.load(open(d + "/m8_parca.json", encoding="utf-8"))["MEK"]]
T = np.stack([D["A"], D["B"], D["C"]], 1); mek = D["mek"]
deg = []
for k, v in J["kutu"].items():
    m = mek == M.index(k)
    lo = T[m].reshape(-1, 3).min(0) / 1000; hi = T[m].reshape(-1, 3).max(0) / 1000
    w = [round(float(x), 4) for x in (lo[0], hi[0], lo[1], hi[1], lo[2], hi[2])]
    if max(abs(a - b) for a, b in zip(w, v)) > 0.0006:
        deg.append(k); J["kutu"][k] = w
J["glb"] = "hat3_v8.glb (%s)" % et
json.dump(J, open(js, "w", encoding="utf-8"), ensure_ascii=False)
print("degisen kutu:", deg)
