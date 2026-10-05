# -*- coding: utf-8 -*-
import json, struct, numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
TD = {5126: np.float32, 5125: np.uint32, 5123: np.uint16, 5121: np.uint8}
class G:
    def __init__(s, path):
        raw = open(path, "rb").read(); jl = struct.unpack("<I", raw[12:16])[0]
        s.J = json.loads(raw[20:20 + jl]); bo = 20 + jl; bl = struct.unpack("<I", raw[bo:bo + 4])[0]; s.BIN = raw[bo + 8:bo + 8 + bl]
        s.W = {}
        for r in s.J["scenes"][0]["nodes"]: s._gez(r, np.eye(4))
        s.MEK = s.J["scenes"][0]["extras"]["mekanizmalar"]
        s.byname = {n.get("name"): i for i, n in enumerate(s.J["nodes"])}
    def acc(s, i):
        a = s.J["accessors"][i]; v = s.J["bufferViews"][a["bufferView"]]
        n = {"SCALAR": 1, "VEC3": 3, "VEC2": 2, "VEC4": 4}[a["type"]]; dt = TD[a["componentType"]]
        off = v.get("byteOffset", 0) + a.get("byteOffset", 0)
        r = np.frombuffer(s.BIN[off:off + a["count"] * n * np.dtype(dt).itemsize], dt)
        return r.reshape(-1, n) if n > 1 else r
    @staticmethod
    def trs(nd):
        M = np.eye(4)
        if "matrix" in nd: return np.array(nd["matrix"]).reshape(4, 4).T
        t = nd.get("translation", [0, 0, 0]); q = nd.get("rotation", [0, 0, 0, 1]); sc = nd.get("scale", [1, 1, 1])
        x, y, z, w = q
        R = np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                      [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                      [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
        M[:3, :3] = R * np.array(sc)[None, :]; M[:3, 3] = t; return M
    def _gez(s, i, P):
        M = P @ s.trs(s.J["nodes"][i]); s.W[i] = M
        for c in s.J["nodes"][i].get("children", []): s._gez(c, M)
    def tris(s, ni):
        """dunya mm koordinatinda (X, T, mek) listesi her prim icin"""
        nd = s.J["nodes"][ni]; M = s.W[ni]; out = []
        for pi, pr in enumerate(s.J["meshes"][nd["mesh"]]["primitives"]):
            X = s.acc(pr["attributes"]["POSITION"]).astype(float)
            X = (X @ M[:3, :3].T + M[:3, 3]) * 1000.0
            T = s.acc(pr["indices"]).reshape(-1, 3).astype(np.int64)
            ex = pr.get("extras", {}); mek = np.full(len(T), -1, int)
            L = ex.get("mek") or []
            for k in range(0, len(L) - 2, 3): mek[L[k + 1] // 3:(L[k + 1] + L[k + 2]) // 3] = L[k]
            out.append((X, T, mek, pr.get("material"), ex))
        return out
def bilesen(X, T):
    u, inv = np.unique(np.round(X, 3), axis=0, return_inverse=True); inv = inv.reshape(-1)
    V = inv[T]; n = len(u)
    r = np.concatenate([V[:, 0], V[:, 1]]); c = np.concatenate([V[:, 1], V[:, 2]])
    k, cl = connected_components(coo_matrix((np.ones(len(r)), (r, c)), shape=(n, n)), directed=False)
    return cl[V[:, 0]]
