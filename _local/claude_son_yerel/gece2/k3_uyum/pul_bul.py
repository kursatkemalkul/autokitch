# GLB'deki pul bileşenleri (halka: d2 × d2 × h) — düğüm başına sayım
import sys, os, json, numpy as np, re, collections
Z = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\gece2\menu7\z53A"
sys.path.insert(0, os.path.join(Z, "gece")); sys.path.insert(0, Z)
from m8kit import Glb
g = Glb(sys.argv[1])
PUL = {"DIN125_M5": (10.0, 1.0), "DIN9021_M5": (15.0, 1.2), "DIN125_M8": (16.0, 1.6), "DIN9021_M8": (24.0, 2.0), "ISO7092_M8": (15.0, 1.6),
       "DIN125_M6": (12.0, 1.6), "DIN9021_M6": (18.0, 1.6), "DIN125_M4": (9.0, 0.8), "DIN9021_M4": (12.0, 1.0), "DIN125_M3": (7.0, 0.5)}
say = collections.Counter(); out = []
for d in sorted(set(p["name"] for p in g.prims)):
    if not re.search(r"__(paslanmaz|celik|baglanti)$", d): continue
    try: g.bilesen(d, no=0)
    except Exception: continue
    for b in g._bc[d]:
        s = np.sort(b["hi"] - b["lo"])
        for k, (D, h) in PUL.items():
            if abs(s[0] - h) < 0.06 and abs(s[1] - D) < 0.1 and abs(s[2] - D) < 0.1:
                say[(d, k)] += 1; out.append(dict(d=d, no=b["no"], tip=k, lo=b["lo"].tolist(), hi=b["hi"].tolist()))
for k, v in sorted(say.items()): print(k, v)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pul_%s.json" % os.path.basename(sys.argv[1])[:-4]), "w"), indent=0)
