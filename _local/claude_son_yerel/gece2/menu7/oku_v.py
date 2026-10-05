# -*- coding: utf-8 -*-
"""menu7: v9t GLB'den TOPPING dugumlerinin bilesen (bagli parca) kutularini cikarir -> parca.json (salt okuma)"""
import json, struct, sys, numpy as np, re
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
TD = {5126: np.float32, 5125: np.uint32, 5123: np.uint16, 5121: np.uint8}
GLB = sys.argv[1]; OUT = sys.argv[2]
raw = open(GLB, "rb").read(); jl = struct.unpack("<I", raw[12:16])[0]
J = json.loads(raw[20:20 + jl]); bo = 20 + jl; bl = struct.unpack("<I", raw[bo:bo + 4])[0]; BIN = raw[bo + 8:bo + 8 + bl]
def acc(i):
    a = J["accessors"][i]; v = J["bufferViews"][a["bufferView"]]
    n = {"SCALAR": 1, "VEC3": 3, "VEC2": 2, "VEC4": 4}[a["type"]]; dt = TD[a["componentType"]]
    off = v.get("byteOffset", 0) + a.get("byteOffset", 0)
    r = np.frombuffer(BIN[off:off + a["count"] * n * np.dtype(dt).itemsize], dt)
    return r.reshape(-1, n) if n > 1 else r
def trs(nd):
    M = np.eye(4)
    if "matrix" in nd: return np.array(nd["matrix"]).reshape(4, 4).T
    t = nd.get("translation", [0, 0, 0]); q = nd.get("rotation", [0, 0, 0, 1]); s = nd.get("scale", [1, 1, 1])
    x, y, z, w = q
    R = np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                  [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                  [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
    M[:3, :3] = R * np.array(s)[None, :]; M[:3, 3] = t; return M
W = {}
def gez(i, P):
    M = P @ trs(J["nodes"][i]); W[i] = M
    for c in J["nodes"][i].get("children", []): gez(c, M)
for r in J["scenes"][0]["nodes"]: gez(r, np.eye(4))
pat = re.compile(sys.argv[3] if len(sys.argv) > 3 else r"^(TOPPING_MODUL|ELK_TOPPING|URUN__)")
out = []
for ni, nd in enumerate(J["nodes"]):
    if "mesh" not in nd or ni not in W or not pat.search(nd["name"]): continue
    M = W[ni]
    for pi, pr in enumerate(J["meshes"][nd["mesh"]]["primitives"]):
        X = acc(pr["attributes"]["POSITION"]).astype(float)
        X = (X @ M[:3, :3].T + M[:3, 3]) * 1000.0
        T = acc(pr["indices"]).reshape(-1, 3).astype(np.int64)
        u, inv = np.unique(np.round(X, 2), axis=0, return_inverse=True); inv = inv.reshape(-1)
        Tv = inv[T]; n = len(u)
        r = np.concatenate([Tv[:, 0], Tv[:, 1], Tv[:, 2]]); c = np.concatenate([Tv[:, 1], Tv[:, 2], Tv[:, 0]])
        g = coo_matrix((np.ones(len(r)), (r, c)), shape=(n, n))
        k, lab = connected_components(g, directed=False)
        for j in range(k):
            P = u[lab == j]
            if len(P) < 3: continue
            mn = P.min(0); mx = P.max(0)
            out.append(dict(ad=nd["name"], nv=int(len(P)), mn=[round(v, 1) for v in mn], mx=[round(v, 1) for v in mx], P=np.round(P,1).tolist() if len(P)<=70 else None))
json.dump(out, open(OUT, "w"), ensure_ascii=False)
print(len(out))
