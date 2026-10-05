# -*- coding: utf-8 -*-
import json, struct, sys, collections
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
raw = open(S + r"\gece2\b4\52a\hat3_v9t.glb", "rb").read(); jl = struct.unpack("<I", raw[12:16])[0]
J = json.loads(raw[20:20 + jl])
EX = J["scenes"][0]["extras"]
print("extras keys", list(EX.keys()))
for i, m in enumerate(EX["mekanizmalar"]):
    print(i, json.dumps(m, ensure_ascii=False)[:300])
for k in EX:
    if k != "mekanizmalar": print(k, json.dumps(EX[k], ensure_ascii=False)[:600])
P = json.load(open(S + r"\gece2\menu7\parca.json", encoding="utf-8"))
c = collections.Counter(p["ad"] for p in P)
for k, v in sorted(c.items()): print(v, k)
