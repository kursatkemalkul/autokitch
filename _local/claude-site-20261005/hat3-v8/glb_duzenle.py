# -*- coding: utf-8 -*-
"""GLB hızlı düzenleme (montaj koşmadan): parça sil / parça uzat (bir yüzü taşı) / parça ötele.
Parçalar parca_kutulari.json kutusuyla seçilir (kutu içinde kalan köşeler/üçgenler). Sıra korunur (kat/mek aralıkları bozulmaz).
Kullanım: python glb_duzenle.py giris.glb parca_kutulari.json cikis.glb islemler.json
islemler.json: [{"is":"sil","birim":B,"ad":[..]}, {"is":"uzat","birim":B,"ad":A,"eksen":"y","eski":1860.5,"yeni":2198.5},
                {"is":"otele","birim":B,"ad":A,"d":[0,-45,0]}]"""
import json, struct, sys
import numpy as np

gi, pk, go, ij = sys.argv[1:5]
IS = json.load(open(ij, encoding="utf-8"))
P = json.load(open(pk, encoding="utf-8"))["parca"]
KUT = {b: {p[0]: p[2:8] for p in L} for b, L in P.items()}

raw = open(gi, "rb").read()
jl = struct.unpack("<I", raw[12:16])[0]
J = json.loads(raw[20:20 + jl]); bo = 20 + jl
bl = struct.unpack("<I", raw[bo:bo + 4])[0]
BIN = bytearray(raw[bo + 8:bo + 8 + bl])
TD = {5126: np.float32, 5125: np.uint32, 5123: np.uint16}


def oku(i):
    a = J["accessors"][i]; v = J["bufferViews"][a["bufferView"]]
    n = {"SCALAR": 1, "VEC3": 3}[a["type"]]; dt = TD[a["componentType"]]
    off = v.get("byteOffset", 0) + a.get("byteOffset", 0)
    arr = np.frombuffer(bytes(BIN[off:off + a["count"] * n * np.dtype(dt).itemsize]), dt).copy()
    return (arr.reshape(-1, n) if n > 1 else arr), off, dt, a


def yaz(arr, off, dt):
    BIN[off:off + arr.size * np.dtype(dt).itemsize] = arr.astype(dt).tobytes()


def icinde(Xw, k, e=0.15):
    x0, x1, y0, y1, z0, z1 = k
    return (Xw[:, 0] >= x0 - e) & (Xw[:, 0] <= x1 + e) & (Xw[:, 1] >= y0 - e) & (Xw[:, 1] <= y1 + e) & (Xw[:, 2] >= z0 - e) & (Xw[:, 2] <= z1 + e)


rapor = []
for nd in J["nodes"]:
    if "mesh" not in nd: continue
    b = nd.get("name", "").split("__")[0]
    isler = [w for w in IS if w["birim"] == b]
    if not isler: continue
    t = np.array(nd.get("translation", [0, 0, 0]))
    for pr in J["meshes"][nd["mesh"]]["primitives"]:
        X, offx, dtx, ax = oku(pr["attributes"]["POSITION"])
        I, offi, dti, _ = oku(pr["indices"])
        T = I.reshape(-1, 3)
        Xw = (X + t) * 1000.0
        degX = False; degI = False
        # 1 · sil
        for w in isler:
            if w["is"] != "sil": continue
            for a in w["ad"]:
                ic = icinde(Xw, KUT[b][a]); m = ic[T].all(axis=1) & (T[:, 0] != T[:, 1])
                if m.any():
                    T[m, 1] = T[m, 0]; T[m, 2] = T[m, 0]; degI = True; rapor.append((nd["name"], "sil", a, int(m.sum())))
        # 2 · uzat / ötele (köşe taşıma: yalnız o parçanın üçgenlerinde kullanılan köşeler)
        for w in isler:
            if w["is"] not in ("uzat", "otele"): continue
            k = w.get("kutu") or KUT[b][w["ad"]]; ic = icinde(Xw, k)
            kul = np.zeros(len(Xw), bool); kul[T[T[:, 0] != T[:, 1]].reshape(-1)] = True      # yalnız görünür üçgenlerin köşeleri
            vs = np.where(ic & kul)[0]
            if not len(vs): continue
            if w["is"] == "uzat":
                ex = "xyz".index(w["eksen"])
                sec = vs[np.abs(Xw[vs, ex] - w["eski"]) < 0.2]
                Xw[sec, ex] = w["yeni"]; rapor.append((nd["name"], "uzat", w["ad"], len(sec)))
            else:
                Xw[vs] += np.array(w["d"], float); rapor.append((nd["name"], "otele", w["ad"], len(vs)))
            degX = True
        if degX:
            Xn = (Xw / 1000.0 - t).astype(np.float32); yaz(Xn, offx, dtx)
            ax["min"] = Xn.min(axis=0).tolist(); ax["max"] = Xn.max(axis=0).tolist()
        if degI:
            yaz(T.reshape(-1), offi, dti)
for r in rapor: print("  %-28s %-6s %-36s %d" % r)
jb = json.dumps(J, separators=(",", ":")).encode(); jb += b" " * ((4 - len(jb) % 4) % 4)
open(go, "wb").write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(jb) + 8 + len(BIN)) + struct.pack("<II", len(jb), 0x4E4F534A) + jb + struct.pack("<II", len(BIN), 0x004E4942) + bytes(BIN))
print("yazıldı", go, "·", len(rapor), "işlem")
