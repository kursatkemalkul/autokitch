# -*- coding: utf-8 -*-
"""Gece temizligi GLB arac takimi (dogrudan GLB duzenleme). Tum primitive'ler, extras (kat/mek/kpk) korunur.
G = Glb(yol); G.prims -> [{nd, name, pi, pr, X(mm, dunya), T, t(translation m)}]; G.kaydet(yol).
 - komp(p): ucgen basina bagli bilesen etiketi + bilesen kutulari
 - sil(p, maske) . tasi(p, maske, fonk) . ekle(p, X, T, kpk)"""
import json, struct, numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
TD = {5126: np.float32, 5125: np.uint32, 5123: np.uint16}


class Glb:
    def __init__(s, yol):
        raw = open(yol, "rb").read(); jl = struct.unpack("<I", raw[12:16])[0]
        s.J = json.loads(raw[20:20 + jl]); bo = 20 + jl; bl = struct.unpack("<I", raw[bo:bo + 4])[0]
        s.BIN = bytearray(raw[bo + 8:bo + 8 + bl])
        s.prims = []
        kul = {}
        for ni, nd in enumerate(s.J["nodes"]):
            if "mesh" not in nd: continue
            t = np.array(nd.get("translation", [0, 0, 0]), float)
            for pi, pr in enumerate(s.J["meshes"][nd["mesh"]]["primitives"]):
                for a in (pr["attributes"]["POSITION"], pr["indices"]):
                    kul[a] = kul.get(a, 0) + 1
                X = s._oku(pr["attributes"]["POSITION"]).astype(float); X = (X + t) * 1000.0
                T = s._oku(pr["indices"]).reshape(-1, 3).astype(np.int64)
                s.prims.append(dict(nd=nd, name=nd.get("name", ""), pi=pi, pr=pr, X=X, T=T, t=t, degX=False, degT=False))
        s.paylasim = [a for a, n in kul.items() if n > 1]

    def _oku(s, i):
        a = s.J["accessors"][i]; v = s.J["bufferViews"][a["bufferView"]]
        n = {"SCALAR": 1, "VEC3": 3, "VEC2": 2, "VEC4": 4}[a["type"]]; dt = TD[a["componentType"]]
        off = v.get("byteOffset", 0) + a.get("byteOffset", 0)
        r = np.frombuffer(bytes(s.BIN[off:off + a["count"] * n * np.dtype(dt).itemsize]), dt).copy()
        return r.reshape(-1, n) if n > 1 else r

    def bul(s, name):
        r = [p for p in s.prims if p["name"] == name]
        if not r: raise KeyError(name)
        return r[0]

    @staticmethod
    def gorunur(p):
        T = p["T"]; return (T[:, 0] != T[:, 1]) | (T[:, 1] != T[:, 2])

    @staticmethod
    def komp(p):
        X, T = p["X"], p["T"]
        P = np.round(X, 2); u, inv = np.unique(P, axis=0, return_inverse=True); inv = inv.reshape(-1)
        Ti = inv[T]; n = len(u)
        r = np.concatenate([Ti[:, 0], Ti[:, 1]]); c = np.concatenate([Ti[:, 1], Ti[:, 2]])
        k, lab = connected_components(coo_matrix((np.ones(len(r)), (r, c)), shape=(n, n)), directed=False)
        tl = lab[Ti[:, 0]]
        vis = (T[:, 0] != T[:, 1]) | (T[:, 1] != T[:, 2])
        kut = {}
        for i in np.unique(tl[vis]):
            m = (tl == i) & vis; Q = u[np.unique(Ti[m])]
            kut[int(i)] = (Q.min(0), Q.max(0), int(m.sum()))
        return tl, kut

    def kutu_maske(s, p, x0, x1, y0, y1, z0, z1, e=0.05):
        """bilesen kutusu tamamen verilen kutunun icindeki gorunur ucgenler"""
        tl, kut = s.komp(p)
        sec = [i for i, (a, b, n) in kut.items() if a[0] >= x0 - e and b[0] <= x1 + e and a[1] >= y0 - e and b[1] <= y1 + e and a[2] >= z0 - e and b[2] <= z1 + e]
        return np.isin(tl, sec) & s.gorunur(p)

    def sil(s, p, m):
        T = p["T"]; m = m & s.gorunur(p); T[m, 1] = T[m, 0]; T[m, 2] = T[m, 0]; p["degT"] = True; return int(m.sum())

    def tasi(s, p, m, f):
        """m: ucgen maskesi . f(V mm Nx3) -> yeni V"""
        vs = np.unique(p["T"][m].reshape(-1)); p["X"][vs] = f(p["X"][vs].copy()); p["degX"] = True; return len(vs)

    def _ekle_arr(s, arr, tip, hedef):
        while len(s.BIN) % 4: s.BIN += b"\0"
        off = len(s.BIN); s.BIN += arr.tobytes()
        s.J["bufferViews"].append({"buffer": 0, "byteOffset": off, "byteLength": arr.nbytes, "target": hedef})
        a = {"bufferView": len(s.J["bufferViews"]) - 1, "componentType": 5126 if arr.dtype == np.float32 else 5125, "count": int(len(arr)), "type": tip}
        if tip == "VEC3": a["min"] = arr.min(axis=0).tolist(); a["max"] = arr.max(axis=0).tolist()
        s.J["accessors"].append(a); return len(s.J["accessors"]) - 1

    @staticmethod
    def ag(solidler, tol=0.1, ang=0.2):
        P, I = [], []
        for so in solidler:                                                   # butun sekil birlikte: komsu yuzler ayni kenar bolmesini paylasir (kapali ag)
            v, t = so.tessellate(tol, ang)
            if not t: continue
            o = sum(len(q) for q in P)
            P.append(np.array([[q.x, q.y, q.z] for q in v], float)); I.append(np.array(t, np.int64) + o)
        return np.vstack(P), np.vstack(I)

    def ekle(s, p, X_mm, T_new, kpk=False):
        """p primitive'ine ucgen ekler (duz golgeleme, kose ucgen basina). kat/mek: son araligin etiketiyle; kpk=True -> kpk araligi"""
        Xf = X_mm[np.asarray(T_new).reshape(-1)]
        n = np.cross(Xf[1::3] - Xf[0::3], Xf[2::3] - Xf[0::3]); n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
        N = np.repeat(n, 3, axis=0)
        p.setdefault("ekX", []).append(Xf); p.setdefault("ekN", []).append(N); p.setdefault("ekK", []).append(kpk)
        return len(Xf) // 3

    def kpk_maske(s, p):
        n = len(p["T"]); m = np.zeros(n, bool); k = p["pr"].get("extras", {}).get("kpk") or []
        for i in range(0, len(k) - 1, 2): m[k[i] // 3:(k[i] + k[i + 1]) // 3] = True
        return m

    def kaydet(s, yol):
        for p in s.prims:
            pr = p["pr"]
            if p.get("ekX"):
                for k_ in pr["attributes"]:
                    if k_ not in ("POSITION", "NORMAL"): raise RuntimeError("ek oznitelik var: " + k_)
                N0 = s._oku(pr["attributes"]["NORMAL"]).astype(np.float32)
                X0 = p["X"]; T0 = p["T"].reshape(-1).astype(np.uint32)
                X = np.vstack([X0] + p["ekX"]); N = np.vstack([N0] + [n.astype(np.float32) for n in p["ekN"]])
                ex = pr.get("extras", {}); I = [T0]; base = len(X0); ibase = len(T0)
                for Xf, kp in zip(p["ekX"], p["ekK"]):
                    k = len(Xf); I.append(np.arange(base, base + k, dtype=np.uint32))
                    for key in ("kat", "mek"):
                        if ex.get(key): ex[key] = ex[key] + [ex[key][-3], ibase, k]
                    if kp: ex["kpk"] = ex.get("kpk", []) + [ibase, k]
                    base += k; ibase += k
                if ex: pr["extras"] = ex
                Xm = ((X / 1000.0) - p["t"]).astype(np.float32)
                pr["attributes"] = {"POSITION": s._ekle_arr(Xm, "VEC3", 34962), "NORMAL": s._ekle_arr(N.astype(np.float32), "VEC3", 34962)}
                pr["indices"] = s._ekle_arr(np.concatenate(I).astype(np.uint32), "SCALAR", 34963)
                continue
            if p["degX"]:
                a = s.J["accessors"][pr["attributes"]["POSITION"]]; v = s.J["bufferViews"][a["bufferView"]]
                off = v.get("byteOffset", 0) + a.get("byteOffset", 0)
                Xm = ((p["X"] / 1000.0) - p["t"]).astype(np.float32); s.BIN[off:off + Xm.nbytes] = Xm.tobytes()
                a["min"] = Xm.min(0).tolist(); a["max"] = Xm.max(0).tolist()
            if p["degT"]:
                a = s.J["accessors"][pr["indices"]]; v = s.J["bufferViews"][a["bufferView"]]; dt = TD[a["componentType"]]
                off = v.get("byteOffset", 0) + a.get("byteOffset", 0)
                arr = p["T"].reshape(-1).astype(dt); s.BIN[off:off + arr.nbytes] = arr.tobytes()
        while len(s.BIN) % 4: s.BIN += b"\0"
        s.J["buffers"][0]["byteLength"] = len(s.BIN)
        jb = json.dumps(s.J, separators=(",", ":"), ensure_ascii=False).encode(); jb += b" " * ((4 - len(jb) % 4) % 4)
        open(yol, "wb").write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(jb) + 8 + len(s.BIN)) + struct.pack("<II", len(jb), 0x4E4F534A) + jb + struct.pack("<II", len(s.BIN), 0x004E4942) + bytes(s.BIN))
