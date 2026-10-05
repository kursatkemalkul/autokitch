# ön yüz: kapak / çekmece ön panelleri (z ≥ 70'e uzanan büyük bileşenler) + istasyon zarfları (GLB)
import sys, os, json, numpy as np, re
Z = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\gece2\menu7\z53A"
sys.path.insert(0, os.path.join(Z, "gece")); sys.path.insert(0, Z)
from m8kit import Glb
g = Glb(sys.argv[1])
KOD = [m["kod"] for m in g.J["scenes"][0]["extras"]["mekanizmalar"]]
out = []
for d in sorted(set(p["name"] for p in g.prims)):
    if re.match(r"^(QR|TEZGAH|ELK|INSAN|ZEMIN|URUN|DUZ_TEZGAH|HAVA|D_PIZZA)", d): continue
    try: g.bilesen(d, no=0)
    except Exception: continue
    for b in g._bc[d]:
        lo, hi = b["lo"], b["hi"]; s = hi - lo
        if hi[2] >= 70.0 and s[0] > 100 and s[1] > 100:
            out.append(dict(d=d, no=b["no"], lo=np.round(lo, 2).tolist(), hi=np.round(hi, 2).tolist()))
out.sort(key=lambda o: (o["lo"][0], o["lo"][1]))
for o in out: print("%-45s %4d  x %8.2f–%8.2f  y %8.2f–%8.2f  z %8.2f–%7.2f" % (o["d"], o["no"], o["lo"][0], o["hi"][0], o["lo"][1], o["hi"][1], o["lo"][2], o["hi"][2]))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "on_yuz.json"), "w"), indent=0)
