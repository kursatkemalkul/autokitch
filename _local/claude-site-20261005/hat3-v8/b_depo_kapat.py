# -*- coding: utf-8 -*-
"""B dolabı · DEPO (K4, x 4028,5–4398,5) çevresinde AÇIKTA KALAN PU + PU/sac arası boşluklar kapatılır (üretime yönelik):
  1. Sağ dış kenar şeridi (x 4370–4398,5): ön çerçeve sacı 4370'te bitiyor, dış dönüş sacı 37,5'te → sağ PU'nun önü (z 23…37,5) AÇIKTI → PU dolgu + dönüş sacı 434,5'e kadar iner
  2. Sağ / tavan PU'nun arkası (z −440) ile arka PU (−441) arasında 1 mm boşluk → PU dolgu
  3. Ara raf PU'su (y 434,5–462,5): üstü (depo tabanı), altı ve arkası ÇIPLAKTI → 1,0 mm 304 iç sac (depo taban sacı · ara alt sac · ara arka sac)
Parçalar mevcut düğümlere EKLENİR (B_KASA__pu, B_KASA__sac). Kullanım: python b_depo_kapat.py giris.glb cikis.glb"""
import json, struct, sys
import numpy as np
import cadquery as cq


def kutu(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, cq.Vector(x0, y0, z0))


PU = {"tk_depo_sag_on_pu_dolgu": kutu(4370.0, 4398.5, 434.5, 729.0, 23.0, 37.5),
      "tk_depo_sag_arka_pu_dolgu": kutu(4338.5, 4398.5, 463.5, 729.0, -441.0, -440.0),
      "tk_depo_tavan_arka_pu_dolgu": kutu(4028.5, 4398.5, 729.0, 786.5, -441.0, -440.0)}
SAC = {"kasa_yan_on_donus_sag_alt": kutu(4370.0, 4398.5, 434.5, 463.5, 37.5, 39.0),
       "tk_depo_taban_ic_sac": kutu(4028.5, 4337.5, 462.5, 463.5, -440.0, 23.0),
       "tk_ara_alt_sac": kutu(4028.5, 4398.5, 433.5, 434.5, -494.0, 23.0),
       "tk_ara_arka_sac": kutu(4028.5, 4398.5, 433.5, 463.5, -495.0, -494.0)}


def ag(solidler):
    P, I = [], []
    for s in solidler:
        for f in s.Faces():
            v, t = f.tessellate(0.1, 0.2); o = sum(len(p) for p in P)
            P.append(np.array([[q.x, q.y, q.z] for q in v], float)); I.append(np.array(t, np.int64) + o)
    X = np.vstack(P); T = np.vstack(I)
    Xf = X[T.reshape(-1)]; n = np.cross(Xf[1::3] - Xf[0::3], Xf[2::3] - Xf[0::3]); n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
    return (Xf / 1000.0).astype(np.float32), np.repeat(n, 3, axis=0).astype(np.float32)


if __name__ == "__main__":
    gi, go = sys.argv[1:3]
    raw = open(gi, "rb").read(); jl = struct.unpack("<I", raw[12:16])[0]; J = json.loads(raw[20:20 + jl]); bo = 20 + jl
    bl = struct.unpack("<I", raw[bo:bo + 4])[0]; BIN = bytearray(raw[bo + 8:bo + 8 + bl])
    TD = {5126: np.float32, 5125: np.uint32, 5123: np.uint16}

    def oku(i):
        a = J["accessors"][i]; v = J["bufferViews"][a["bufferView"]]; n = {"SCALAR": 1, "VEC3": 3}[a["type"]]; dt = TD[a["componentType"]]
        off = v.get("byteOffset", 0) + a.get("byteOffset", 0)
        r = np.frombuffer(bytes(BIN[off:off + a["count"] * n * np.dtype(dt).itemsize]), dt)
        return r.reshape(-1, n) if n > 1 else r

    def ekle(arr, tip, hedef):
        global BIN
        while len(BIN) % 4: BIN += b"\0"
        off = len(BIN); BIN += arr.tobytes()
        J["bufferViews"].append({"buffer": 0, "byteOffset": off, "byteLength": arr.nbytes, "target": hedef})
        a = {"bufferView": len(J["bufferViews"]) - 1, "componentType": 5126 if arr.dtype == np.float32 else 5125, "count": int(len(arr)), "type": tip}
        if tip == "VEC3": a["min"] = arr.min(axis=0).tolist(); a["max"] = arr.max(axis=0).tolist()
        J["accessors"].append(a); return len(J["accessors"]) - 1

    def ilave(dugum, solidler):
        nd = [n for n in J["nodes"] if n.get("name") == dugum][0]; pr = J["meshes"][nd["mesh"]]["primitives"][0]
        X0 = oku(pr["attributes"]["POSITION"]); N0 = oku(pr["attributes"]["NORMAL"]); I0 = oku(pr["indices"]).astype(np.uint32)
        Xn, Nn = ag(solidler)
        X = np.vstack([X0, Xn]).astype(np.float32); N = np.vstack([N0, Nn]).astype(np.float32)
        I = np.concatenate([I0, np.arange(len(X0), len(X0) + len(Xn), dtype=np.uint32)])
        pr["attributes"] = {"POSITION": ekle(X, "VEC3", 34962), "NORMAL": ekle(N, "VEC3", 34962)}; pr["indices"] = ekle(I, "SCALAR", 34963)
        ex = pr.get("extras", {}); ek = len(Xn)
        for k in ("kat", "mek"):
            if ex.get(k): ex[k] = ex[k] + [ex[k][-3], len(I0), ek]               # yeni üçgenler, düğümün son aralığının etiketiyle (İNDİS sayısı)
        print("  %-22s +%d üçgen (%s)" % (dugum, ek // 3, ", ".join(sorted(solidler and [k for k in (PU if solidler is not None else {})] or []))[:0]))

    ilave("B_KASA__pu", list(PU.values()))
    ilave("B_KASA__sac", list(SAC.values()))
    J["buffers"][0]["byteLength"] = len(BIN)
    jb = json.dumps(J, separators=(",", ":")).encode(); jb += b" " * ((4 - len(jb) % 4) % 4)
    while len(BIN) % 4: BIN += b"\0"
    open(go, "wb").write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(jb) + 8 + len(BIN)) + struct.pack("<II", len(jb), 0x4E4F534A) + jb + struct.pack("<II", len(BIN), 0x004E4942) + bytes(BIN))
    print("yazıldı", go)
