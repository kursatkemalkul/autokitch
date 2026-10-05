# -*- coding: utf-8 -*-
"""v8zq GLB okuyucu (tam dünya dönüşümü, m8_yukle mantığı) · düğüm → üçgenler (mm) · bağlı bileşen parçaları"""
import json, struct, sys, os, numpy as np
TD = {5126: np.float32, 5125: np.uint32, 5123: np.uint16, 5121: np.uint8}
class GLB:
    def __init__(s, yol):
        raw = open(yol, "rb").read(); jl = struct.unpack("<I", raw[12:16])[0]
        s.J = json.loads(raw[20:20 + jl]); bo = 20 + jl; bl = struct.unpack("<I", raw[bo:bo + 4])[0]; s.BIN = raw[bo + 8:bo + 8 + bl]
        s.W = {}
        def trs(nd):
            M = np.eye(4)
            if "matrix" in nd: return np.array(nd["matrix"]).reshape(4, 4).T
            t = nd.get("translation", [0, 0, 0]); q = nd.get("rotation", [0, 0, 0, 1]); sc = nd.get("scale", [1, 1, 1]); x, y, z, w = q
            R = np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)], [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                          [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
            M[:3, :3] = R * np.array(sc)[None, :]; M[:3, 3] = t; return M
        def gez(i, P):
            M = P @ trs(s.J["nodes"][i]); s.W[i] = M
            for c in s.J["nodes"][i].get("children", []): gez(c, M)
        for r in s.J["scenes"][0]["nodes"]: gez(r, np.eye(4))
    def acc(s, i):
        a = s.J["accessors"][i]; v = s.J["bufferViews"][a["bufferView"]]
        n = {"SCALAR": 1, "VEC3": 3, "VEC2": 2, "VEC4": 4}[a["type"]]; dt = TD[a["componentType"]]
        off = v.get("byteOffset", 0) + a.get("byteOffset", 0)
        r = np.frombuffer(s.BIN[off:off + a["count"] * n * np.dtype(dt).itemsize], dt)
        return r.reshape(-1, n) if n > 1 else r
    def dugum_ucgen(s, ni):
        nd = s.J["nodes"][ni]; M = s.W[ni]; out = []
        sc = np.abs(np.linalg.det(M[:3, :3])) ** (1 / 3)
        if sc < 0.01: return []
        for pr in s.J["meshes"][nd["mesh"]]["primitives"]:
            X = s.acc(pr["attributes"]["POSITION"]).astype(float); X = (X @ M[:3, :3].T + M[:3, 3]) * 1000.0
            T = s.acc(pr["indices"]).reshape(-1, 3).astype(np.int64)
            ok = (T[:, 0] != T[:, 1]) & (T[:, 1] != T[:, 2]) & (T[:, 0] != T[:, 2]); T = T[ok]
            out.append((X, T, pr.get("extras", {}), ok))
        return out
def bilesenler(X, T, tol=0.01):
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    u, inv = np.unique(np.round(X / tol).astype(np.int64), axis=0, return_inverse=True); inv = inv.reshape(-1)
    Ti = inv[T]
    r = np.concatenate([Ti[:, 0], Ti[:, 1]]); c = np.concatenate([Ti[:, 1], Ti[:, 2]])
    k, cl = connected_components(coo_matrix((np.ones(len(r)), (r, c)), shape=(len(u), len(u))), directed=False)
    tl = cl[Ti[:, 0]]
    return tl
