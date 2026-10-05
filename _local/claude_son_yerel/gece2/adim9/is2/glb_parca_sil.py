# -*- coding: utf-8 -*-
"""GLB'den parça silme (hızlı düzeltme, montaj yeniden koşmadan): verilen birim düğümlerinde, parça kutusunun (parca_kutulari.json) içinde kalan üçgenler silinir.
Kullanım: python glb_parca_sil.py giris.glb parca_kutulari.json cikis.glb BIRIM:ad,ad BIRIM:ad ..."""
import json, struct, sys
import numpy as np

gi, pk, go = sys.argv[1:4]
hedef = {}
for a in sys.argv[4:]:
    b, adlar = a.split(":", 1)
    hedef[b] = adlar.split(",")
P = json.load(open(pk, encoding="utf-8"))["parca"]
kutu = {}
for b, adlar in hedef.items():
    m = {p[0]: p[2:8] for p in P[b]}
    kutu[b] = [m[a] for a in adlar]

raw = open(gi, "rb").read()
jl = struct.unpack("<I", raw[12:16])[0]
J = json.loads(raw[20:20 + jl])
bo = 20 + jl
bl = struct.unpack("<I", raw[bo:bo + 4])[0]
BIN = bytearray(raw[bo + 8:bo + 8 + bl])


def acc(i):
    a = J["accessors"][i]; v = J["bufferViews"][a["bufferView"]]
    n = {"SCALAR": 1, "VEC3": 3, "VEC2": 2, "VEC4": 4}[a["type"]]
    dt = {5126: np.float32, 5125: np.uint32, 5123: np.uint16}[a["componentType"]]
    off = v.get("byteOffset", 0) + a.get("byteOffset", 0)
    return np.frombuffer(bytes(BIN[off:off + a["count"] * n * np.dtype(dt).itemsize]), dt).reshape(-1, n) if n > 1 else np.frombuffer(bytes(BIN[off:off + a["count"] * np.dtype(dt).itemsize]), dt), a, v, off, dt


# ölçek: parca_kutulari mm, GLB metre ise 1000
sil_top = 0
for ni, nd in enumerate(J["nodes"]):
    ad = nd.get("name", "")
    b = ad.split("__")[0]
    if b not in kutu or "mesh" not in nd:
        continue
    t = np.array(nd.get("translation", [0, 0, 0]))
    for pr in J["meshes"][nd["mesh"]]["primitives"]:
        X, ax, vx, offx, _ = acc(pr["attributes"]["POSITION"])
        I, ai, vi, offi, dti = acc(pr["indices"])
        Xw = (X + t) * 1000.0
        T = I.reshape(-1, 3)
        tut = np.ones(len(T), bool)
        for (x0, x1, y0, y1, z0, z1) in kutu[b]:
            e = 0.1
            ic = (Xw[:, 0] >= x0 - e) & (Xw[:, 0] <= x1 + e) & (Xw[:, 1] >= y0 - e) & (Xw[:, 1] <= y1 + e) & (Xw[:, 2] >= z0 - e) & (Xw[:, 2] <= z1 + e)
            tut &= ~ic[T].all(axis=1)
        k = int((~tut).sum())
        if k:
            yeni = T.copy()                                          # sıra korunur (kat/mek üçgen aralıkları bozulmasın): silinen üçgen yerinde dejenere olur → görünmez
            yeni[~tut, 1] = yeni[~tut, 0]; yeni[~tut, 2] = yeni[~tut, 0]
            BIN[offi:offi + yeni.size * np.dtype(dti).itemsize] = yeni.astype(dti).tobytes()
            sil_top += k
            print("  %-34s -%d üçgen" % (ad, k))
print("toplam silinen üçgen:", sil_top)
jb = json.dumps(J, separators=(",", ":")).encode()
jb += b" " * ((4 - len(jb) % 4) % 4)
out = struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(jb) + 8 + len(BIN)) + struct.pack("<II", len(jb), 0x4E4F534A) + jb + struct.pack("<II", len(BIN), 0x004E4942) + bytes(BIN)
open(go, "wb").write(out)
print("yazıldı", go)
