# kuşbaşı bölgesindeki bileşenler (v9u)
import sys, os, numpy as np, json
Z = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\gece2\menu7\z53A"
sys.path.insert(0, os.path.join(Z, "gece")); sys.path.insert(0, Z)
from m8kit import Glb
gi = sys.argv[1] if len(sys.argv) > 1 else os.path.join(Z, "hat3_v9u.glb")
g = Glb(gi)
KOD = [m["kod"] for m in g.J["scenes"][0]["extras"]["mekanizmalar"]]
LO = np.array([1700, 950, -620.0]); HI = np.array([1990, 1600, -100.0])
dug = sorted(set(p["name"] for p in g.prims if p["name"].startswith("TOPPING")))
out = []
for d in dug:
    try:
        L = g.bilesen(d, no=0) and g._bc[d]
    except Exception as e:
        continue
    for b in L:
        if np.all(b["hi"] > LO) and np.all(b["lo"] < HI):
            p, t = b["parca"][0]
            kat, mek, kpk = g._etiketler(p, t[0])
            out.append((d, b["no"], np.round(b["lo"], 1).tolist(), np.round(b["hi"], 1).tolist(), KOD[mek] if mek is not None else None, b["kapali"]))
for o in out: print(o)
json.dump(out, open(os.path.join(os.path.dirname(__file__), "kb_bilesen.json"), "w", encoding="utf8"), ensure_ascii=False)
