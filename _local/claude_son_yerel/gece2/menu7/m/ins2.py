# -*- coding: utf-8 -*-
"""TOPPING bölgesi bileşen dökümü: düğüm, no, kutu, kapalı, mek, kat -> bil_v9t.json"""
import os, sys, json, time, collections
import numpy as np
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
K = S + r"\gece2\b4\52a"
sys.path[:0] = [K + r"\gece", K]
os.environ["YAMA_IS_KOK"] = K
from m8kit import Glb
t0 = time.time()
g = Glb(sys.argv[1] if len(sys.argv) > 1 else K + r"\hat3_v9t.glb")
print("yuklendi", time.time() - t0)
EX = g.J["scenes"][0]["extras"]; KOD = [m["kod"] for m in EX["mekanizmalar"]]
TOP = {i for i, k in enumerate(KOD) if k.startswith("TOPPING/")}
dug = collections.Counter()
for p in g.prims:
    ex = p["pr"].get("extras", {}); L = ex.get("mek") or []
    for k in range(0, len(L) - 2, 3):
        if L[k] in TOP: dug[p["name"]] += L[k + 2] // 3
print(len(dug), "düğüm TOPPING etiketli")
out = []
for d in sorted(dug):
    try: g.bilesen(d, 0)
    except IndexError: print('bos', d); continue
    for b in g._bc[d]:
        p, t = b["parca"][0]
        kat, mek, kpk = g._etiketler(p, int(t[0]))
        n = sum(len(tt) for _, tt in b["parca"])
        out.append(dict(d=d, no=b["no"], lo=[round(float(v), 1) for v in b["lo"]], hi=[round(float(v), 1) for v in b["hi"]],
                        kapali=bool(b["kapali"]), mek=KOD[mek] if mek is not None else None, kat=kat, kpk=kpk, n=n))
    g._bc.clear()
json.dump(out, open(S + r"\gece2\menu7\m\bil_v9t.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
c = collections.Counter((o["d"], o["mek"]) for o in out)
for k, v in sorted(c.items()): print(v, k)
print("bitti", time.time() - t0)

