# -*- coding: utf-8 -*-
"""GLB okuma yardımcıları: düğüm adı → (köşeler mm, üçgen indisleri)."""
import json, struct
import numpy as np

TD = {5126: np.float32, 5125: np.uint32, 5123: np.uint16}


def yukle(yol):
    raw = open(yol, "rb").read()
    jl = struct.unpack("<I", raw[12:16])[0]; J = json.loads(raw[20:20 + jl]); bo = 20 + jl
    bl = struct.unpack("<I", raw[bo:bo + 4])[0]; BIN = raw[bo + 8:bo + 8 + bl]

    def acc(i):
        a = J["accessors"][i]; v = J["bufferViews"][a["bufferView"]]
        n = {"SCALAR": 1, "VEC3": 3}[a["type"]]; dt = TD[a["componentType"]]
        off = v.get("byteOffset", 0) + a.get("byteOffset", 0)
        arr = np.frombuffer(BIN[off:off + a["count"] * n * np.dtype(dt).itemsize], dt)
        return arr.reshape(-1, n) if n > 1 else arr
    D = {}
    for nd in J["nodes"]:
        if "mesh" not in nd: continue
        t = np.array(nd.get("translation", [0, 0, 0]))
        for pr in J["meshes"][nd["mesh"]]["primitives"]:
            X = (acc(pr["attributes"]["POSITION"]).astype(float) + t) * 1000.0
            T = acc(pr["indices"]).reshape(-1, 3).astype(np.int64)
            T = T[(T[:, 0] != T[:, 1]) | (T[:, 1] != T[:, 2])]
            D[nd["name"]] = (X, T)
    return J, D
