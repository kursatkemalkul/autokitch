# -*- coding: utf-8 -*-
"""8a ortak: tüm model bileşenleri (govde_denetim_dogru yöntemi) + üçgen etiketleri (mek/kat/kpk) + aday çiftler."""
import os, sys, json, struct, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, S)
import govde_denetim_dogru as G
GLB = os.path.join(S, "hat3_v8x.glb")
HARIC = ("ROBOT", "INSAN", "ZEMIN")


def glb_oku_etiket(yol):
    raw = open(yol, "rb").read()
    jl = struct.unpack("<I", raw[12:16])[0]; J = json.loads(raw[20:20 + jl]); bo = 20 + jl
    bl = struct.unpack("<I", raw[bo:bo + 4])[0]; BIN = raw[bo + 8:bo + 8 + bl]

    def acc(i):
        a = J["accessors"][i]; v = J["bufferViews"][a["bufferView"]]
        n = {"SCALAR": 1, "VEC3": 3, "VEC2": 2, "VEC4": 4}[a["type"]]; dt = G.TD[a["componentType"]]
        off = v.get("byteOffset", 0) + a.get("byteOffset", 0); st = v.get("byteStride", 0)
        isz = np.dtype(dt).itemsize
        if st and st != n * isz:
            buf = np.frombuffer(BIN[off:off + st * a["count"]], np.uint8).reshape(a["count"], st)[:, :n * isz]
            arr = np.frombuffer(buf.tobytes(), dt)
        else:
            arr = np.frombuffer(BIN[off:off + a["count"] * n * isz], dt)
        return arr.reshape(-1, n) if n > 1 else arr

    def ar_etiket(lst, nt, cift=False):
        out = np.full(nt, -1, np.int32)
        if not lst: return out
        if cift:
            for i in range(0, len(lst) - 1, 2): out[lst[i] // 3:(lst[i] + lst[i + 1]) // 3] = 1
        else:
            for k in range(0, len(lst) - 2, 3): out[lst[k + 1] // 3:(lst[k + 1] + lst[k + 2]) // 3] = lst[k]
        return out
    D = {}; nodes = J["nodes"]

    def gez(i, M):
        nd = nodes[i]; W = M @ G._mat(nd)
        if "mesh" in nd:
            ad = nd.get("name", "dugum%d" % i)
            if ad in D: ad = "%s#%d" % (ad, i)
            PP, LL = [], []
            for pr in J["meshes"][nd["mesh"]]["primitives"]:
                if pr.get("mode", 4) != 4: continue
                X = acc(pr["attributes"]["POSITION"]).astype(float)
                X = (X @ W[:3, :3].T + W[:3, 3]) * 1000.0
                T = acc(pr["indices"]).reshape(-1, 3).astype(np.int64) if "indices" in pr else np.arange(len(X)).reshape(-1, 3)
                P = X[T]; nt = len(T); ex = pr.get("extras", {}) or {}
                L = np.stack([ar_etiket(ex.get("mek"), nt), ar_etiket(ex.get("kat"), nt), ar_etiket(ex.get("kpk"), nt, True)], 1)
                ar = np.linalg.norm(np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]), axis=1)
                PP.append(P[ar > 1e-9]); LL.append(L[ar > 1e-9])
            D[ad] = (np.concatenate(PP), np.concatenate(LL)) if PP else (np.zeros((0, 3, 3)), np.zeros((0, 3), np.int32))
        for c in nd.get("children", []): gez(c, W)
    for i in J["scenes"][J.get("scene", 0)]["nodes"]: gez(i, np.eye(4))
    return J, D


def tum_bilesenler(etiket=False):
    J, D = glb_oku_etiket(GLB)
    B = []; LAB = []
    for nd in D:
        if nd.startswith(HARIC): continue
        P, L = D[nd]
        bb = G.bilesenler(nd, P)
        if etiket and bb:
            key = {P[i].tobytes(): i for i in range(len(P))}
            for b in bb:
                ii = [key.get(b.P[k].tobytes(), -1) for k in range(0, len(b.P), max(1, len(b.P) // 60))]
                ii = [i for i in ii if i >= 0]
                l = L[ii] if ii else np.full((1, 3), -1)
                vals = lambda c: np.bincount(l[:, c] + 1).argmax() - 1
                LAB.append((int(vals(0)), int(vals(1)), float((l[:, 2] > 0).mean())))
        B += bb
    return J, B, LAB


def adaylar(B, pay=G.PAY):
    LO = np.array([b.lo for b in B]); HI = np.array([b.hi for b in B]); n = len(B)
    o = np.argsort(LO[:, 0]); P = []
    for a in range(n):
        i = o[a]
        j = o[a + 1:]
        j = j[LO[j, 0] <= HI[i, 0] + pay]
        if not len(j): continue
        m = ((LO[j] <= HI[i] + pay) & (HI[j] >= LO[i] - pay)).all(1)
        for k in j[m]: P.append((min(i, k), max(i, k)))
    return P
