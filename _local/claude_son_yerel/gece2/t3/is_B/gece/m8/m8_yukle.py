# -*- coding: utf-8 -*-
"""m8: GLB'yi TAM dunya donusumuyle (TRS + hiyerarsi) yukler, ucgen basina etiket (mek/kat/kpk) + PARCA (ayni prim, ayni mek+kpk, bagli bilesen).
Cikti: m8_onbellek.npz + m8_parca.json"""
import json, struct, sys, numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
TD = {5126: np.float32, 5125: np.uint32, 5123: np.uint16, 5121: np.uint8}
GLB = sys.argv[1]
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
MEK = J["scenes"][0]["extras"]["mekanizmalar"]; KAT = [k["kod"] for k in J["scenes"][0]["extras"]["kategoriler"]]
A_, B_, C_, TP, TMEK, TKAT, TKPK = [], [], [], [], [], [], []
PR = []; parca = []; pbase = 0
for ni, nd in enumerate(J["nodes"]):
    if "mesh" not in nd or ni not in W: continue
    M = W[ni]; sc = np.abs(np.linalg.det(M[:3, :3])) ** (1 / 3)
    for pi, pr in enumerate(J["meshes"][nd["mesh"]]["primitives"]):
        X = acc(pr["attributes"]["POSITION"]).astype(float)
        X = (X @ M[:3, :3].T + M[:3, 3]) * 1000.0
        T = acc(pr["indices"]).reshape(-1, 3).astype(np.int64); n = len(T)
        ex = pr.get("extras", {})
        mek = np.full(n, -1, int); kat = np.full(n, -1, int); kpk = np.zeros(n, bool)
        for key, arr in (("mek", mek), ("kat", kat)):
            L = ex.get(key) or []
            for k in range(0, len(L) - 2, 3): arr[L[k + 1] // 3:(L[k + 1] + L[k + 2]) // 3] = L[k]
        L = ex.get("kpk") or []
        for k in range(0, len(L) - 1, 2): kpk[L[k] // 3:(L[k] + L[k + 1]) // 3] = True
        if nd["name"].endswith("__on_seffaf") or "__on_seffaf__" in nd["name"]: pass
        vis = (T[:, 0] != T[:, 1]) & (T[:, 1] != T[:, 2]) & (T[:, 0] != T[:, 2])
        P = X[T]; ar = np.linalg.norm(np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]), axis=1)
        vis &= ar > 1e-9
        if sc < 0.01: vis[:] = False          # gizli urun (olcek 0,0001)
        idx = np.where(vis)[0]
        if not len(idx): PR.append(dict(ad=nd["name"], ni=ni, pi=pi, n=0, gizli=bool(sc < 0.01))); continue
        Tv = T[idx]
        u, inv = np.unique(np.round(X, 2), axis=0, return_inverse=True); inv = inv.reshape(-1)
        lab = (mek[idx] + 1) * 2 + kpk[idx]
        ul, li = np.unique(lab, return_inverse=True)
        Vi = inv[Tv] * len(ul) + li[:, None]          # etiketli kose
        uv, vv = np.unique(Vi.reshape(-1), return_inverse=True); vv = vv.reshape(-1, 3)
        r = np.concatenate([vv[:, 0], vv[:, 1]]); c = np.concatenate([vv[:, 1], vv[:, 2]])
        k, cl = connected_components(coo_matrix((np.ones(len(r)), (r, c)), shape=(len(uv), len(uv))), directed=False)
        tc = cl[vv[:, 0]]
        uc, tci = np.unique(tc, return_inverse=True)
        Pv = P[idx]
        for j in range(len(uc)):
            m = tci == j; Q = Pv[m].reshape(-1, 3)
            parca.append(dict(prim=len(PR), ad=nd["name"], mek=int(mek[idx][m][0]), kpk=bool(kpk[idx][m][0]),
                              kat=int(np.bincount(kat[idx][m] + 1).argmax() - 1), n=int(m.sum()),
                              lo=Q.min(0).round(2).tolist(), hi=Q.max(0).round(2).tolist()))
        A_.append(Pv[:, 0]); B_.append(Pv[:, 1]); C_.append(Pv[:, 2]); TP.append(tci + pbase)
        TMEK.append(mek[idx]); TKAT.append(kat[idx]); TKPK.append(kpk[idx]); pbase += len(uc)
        PR.append(dict(ad=nd["name"], ni=ni, pi=pi, n=len(idx), gizli=False))
A_ = np.vstack(A_); B_ = np.vstack(B_); C_ = np.vstack(C_)
np.savez("m8_onbellek.npz", A=A_, B=B_, C=C_, P=np.concatenate(TP), mek=np.concatenate(TMEK), kat=np.concatenate(TKAT), kpk=np.concatenate(TKPK))
json.dump(dict(parca=parca, prim=PR, MEK=MEK, KAT=KAT), open("m8_parca.json", "w"), ensure_ascii=False)
print(len(A_), "ucgen", len(parca), "parca", sum(1 for p in PR if p.get("gizli")), "gizli prim")
