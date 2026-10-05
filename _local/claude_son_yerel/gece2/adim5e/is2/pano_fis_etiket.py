# -*- coding: utf-8 -*-
"""Ana panodaki istasyon fişleri (harting_ANA_PANO_*_fis/_rakoru) istasyonların mekanizmasına etiketliydi → istasyon görünümünde
U_F'teki panonun yanında 'havada kutu' gibi çıkıyordu. Hepsi 'Elektrik/Ana pano' mekanizmasına alınır (fiş panoya takılı, panonun parçası).
Kullanım: python pano_fis_etiket.py giris.glb cikis.glb parca_kutulari.json"""
import json, struct, sys
import numpy as np
gi, go, pk = sys.argv[1:4]
raw = open(gi, "rb").read(); jl = struct.unpack("<I", raw[12:16])[0]; J = json.loads(raw[20:20 + jl]); bo = 20 + jl
bl = struct.unpack("<I", raw[bo:bo + 4])[0]; BIN = raw[bo + 8:bo + 8 + bl]
M = J["scenes"][0]["extras"]["mekanizmalar"]
hedef = next(i for i, m in enumerate(M) if m.get("kod") == "Elektrik/Ana pano")
K = [p[2:8] for p in json.load(open(pk, encoding="utf-8"))["parca"]["ELK_ISTASYON"] if p[0].startswith("harting_ANA_PANO_")]
TD = {5126: np.float32, 5125: np.uint32, 5123: np.uint16}


def acc(i):
    a = J["accessors"][i]; v = J["bufferViews"][a["bufferView"]]; n = {"SCALAR": 1, "VEC3": 3}[a["type"]]; dt = TD[a["componentType"]]
    o = v.get("byteOffset", 0) + a.get("byteOffset", 0); r = np.frombuffer(BIN[o:o + a["count"] * n * np.dtype(dt).itemsize], dt)
    return r.reshape(-1, n) if n > 1 else r


say = 0
for nd in J["nodes"]:
    if not nd.get("name", "").startswith("ELK_ISTASYON") or "mesh" not in nd: continue
    for pr in J["meshes"][nd["mesh"]]["primitives"]:
        ex = pr.get("extras", {}); mk = ex.get("mek")
        if not mk: continue
        X = acc(pr["attributes"]["POSITION"]).astype(float) * 1000.0; I = acc(pr["indices"]).reshape(-1, 3)
        n = len(I); lab = np.zeros(n, np.int64)
        for k in range(0, len(mk), 3): lab[mk[k + 1] // 3:(mk[k + 1] + mk[k + 2]) // 3] = mk[k]
        for (x0, x1, y0, y1, z0, z1) in K:
            e = 0.5
            ic = (X[:, 0] >= x0 - e) & (X[:, 0] <= x1 + e) & (X[:, 1] >= y0 - e) & (X[:, 1] <= y1 + e) & (X[:, 2] >= z0 - e) & (X[:, 2] <= z1 + e)
            m = ic[I].all(axis=1) & (lab != hedef); say += int(m.sum()); lab[m] = hedef
        yeni = []; s = 0
        for t in range(1, n + 1):
            if t == n or lab[t] != lab[s]: yeni += [int(lab[s]), s * 3, (t - s) * 3]; s = t
        ex["mek"] = yeni
print("yeniden etiketlenen üçgen:", say, "→", M[hedef]["kod"])
jb = json.dumps(J, separators=(",", ":")).encode(); jb += b" " * ((4 - len(jb) % 4) % 4)
open(go, "wb").write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(jb) + 8 + len(BIN)) + struct.pack("<II", len(jb), 0x4E4F534A) + jb + struct.pack("<II", len(BIN), 0x004E4942) + BIN)
