# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 50 · GLB SIKILAŞTIRMA (4 Eki 2026 · Claude · YEREL)
python 50_sikilastir.py girdi.glb cikti.glb      (zincir: hat3_v9q.glb → hat3_v9r.glb)

Zincir betikleri (m8kit) sildikleri üçgenleri dejenere (üç köşe aynı indis) bırakır, yeni üçgenleri sona ekler; 44–49 sonrası dosyada ~%40 ölü üçgen /
köşe birikti. Bu adım geometriyi DEĞİŞTİRMEZ: her primitifte dejenere üçgenler atılır, kullanılmayan köşeler atılır (sıra korunur), kat / mek
(değer, ilk indis, sayı) ve kpk (ilk indis, sayı) aralıkları yeni indislere taşınır. Morph target'lı primitiflere dokunulmaz.
Denetim: her primitifin dejenere olmayan üçgen kümesi (köşe koordinatları, bayt) önce = sonra; her üçgenin kat / mek / kpk değeri önce = sonra."""
import json, struct, sys, os, subprocess
import numpy as np

gi, go = sys.argv[1:3]
TD = {5126: np.float32, 5125: np.uint32, 5123: np.uint16, 5121: np.uint8}
raw = open(gi, "rb").read(); jl = struct.unpack("<I", raw[12:16])[0]; J = json.loads(raw[20:20 + jl]); bo = 20 + jl
bl = struct.unpack("<I", raw[bo:bo + 4])[0]; BIN = bytearray(raw[bo + 8:bo + 8 + bl])
assert not J.get("extensionsUsed"), J.get("extensionsUsed")


def oku(i):
    a = J["accessors"][i]; v = J["bufferViews"][a["bufferView"]]
    n = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}[a["type"]]; dt = TD[a["componentType"]]
    off = v.get("byteOffset", 0) + a.get("byteOffset", 0)
    r = np.frombuffer(bytes(BIN[off:off + a["count"] * n * np.dtype(dt).itemsize]), dt).copy()
    return r.reshape(-1, n) if n > 1 else r


def ekle(arr, tip, hedef):
    global BIN
    while len(BIN) % 4: BIN.extend(b"\0")
    off = len(BIN); BIN.extend(arr.tobytes())
    J["bufferViews"].append({"buffer": 0, "byteOffset": off, "byteLength": arr.nbytes, "target": hedef})
    a = {"bufferView": len(J["bufferViews"]) - 1, "componentType": 5126 if arr.dtype == np.float32 else 5125, "count": int(len(arr)), "type": tip}
    if tip == "VEC3": a["min"] = arr.min(axis=0).tolist(); a["max"] = arr.max(axis=0).tolist()
    J["accessors"].append(a); return len(J["accessors"]) - 1


def etiket_dizi(L, n_tri, adim=3):
    """aralık listesi → üçgen başına değer (adim 3: [değer, ilk indis, sayı]) · aralık dışı: None"""
    v = np.full(n_tri, -1, np.int64)
    for k in range(0, len(L) - 2, 3):
        a, b = L[k + 1] // 3, (L[k + 1] + L[k + 2]) // 3; v[a:b] = L[k]
    return v


def aralik_yap(v):
    """üçgen başına değer → [değer, ilk indis, sayı] (−1 yazılmaz)"""
    out = []; n = len(v); i = 0
    while i < n:
        j = i
        while j + 1 < n and v[j + 1] == v[i]: j += 1
        if v[i] >= 0: out += [int(v[i]), 3 * i, 3 * (j - i + 1)]
        i = j + 1
    return out


atilan = 0; toplam = 0; kv = 0
for m in J["meshes"]:
    for pr in m["primitives"]:
        if pr.get("targets") or pr.get("mode", 4) != 4 or "indices" not in pr: continue
        I = oku(pr["indices"]).astype(np.int64); T = I.reshape(-1, 3); nt = len(T)
        iyi = (T[:, 0] != T[:, 1]) & (T[:, 1] != T[:, 2]) & (T[:, 0] != T[:, 2])
        if iyi.all() and len(np.unique(T)) == len(oku(pr["attributes"]["POSITION"])): continue
        X = oku(pr["attributes"]["POSITION"]); atr = {k: oku(i) for k, i in pr["attributes"].items()}
        ex = pr.get("extras", {})
        kat = etiket_dizi(ex.get("kat") or [], nt); mek = etiket_dizi(ex.get("mek") or [], nt)
        kp = np.zeros(nt, bool); K_ = ex.get("kpk") or []
        for k in range(0, len(K_) - 1, 2): kp[K_[k] // 3:(K_[k] + K_[k + 1]) // 3] = True
        T2 = T[iyi]
        if not len(T2): continue                                        # boşaltılmış düğüm (tek dejenere yer tutucu) olduğu gibi kalır
        kul, yeni = np.unique(T2.reshape(-1), return_inverse=True)
        T3 = yeni.reshape(-1, 3)
        # denetim: üçgen köşe koordinatları ve etiketler aynı
        assert np.array_equal(X[kul][T3], X[T2]), "köşe"
        pr["attributes"] = {k: ekle(np.ascontiguousarray(a[kul]).astype(a.dtype), "VEC3" if a.shape[1] == 3 else ("VEC2" if a.shape[1] == 2 else "VEC4"), 34962) for k, a in atr.items()}
        pr["indices"] = ekle(T3.reshape(-1).astype(np.uint32), "SCALAR", 34963)
        if ex:
            if ex.get("kat"): ex["kat"] = aralik_yap(kat[iyi])
            if ex.get("mek"): ex["mek"] = aralik_yap(mek[iyi])
            if "kpk" in ex:
                q = kp[iyi]; out = []; i = 0
                while i < len(q):
                    if q[i]:
                        j = i
                        while j + 1 < len(q) and q[j + 1]: j += 1
                        out += [3 * i, 3 * (j - i + 1)]; i = j + 1
                    else: i += 1
                ex["kpk"] = out
            pr["extras"] = ex
        atilan += int((~iyi).sum()); toplam += nt; kv += len(X) - len(kul)
J["buffers"][0]["byteLength"] = len(BIN)
jb = json.dumps(J, separators=(",", ":"), ensure_ascii=False).encode(); jb += b" " * ((4 - len(jb) % 4) % 4)
tmp = go + ".e1.glb"
with open(tmp, "wb") as f:
    f.write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(jb) + 8 + len(BIN)) + struct.pack("<II", len(jb), 0x4E4F534A) + jb + struct.pack("<II", len(BIN), 0x004E4942) + bytes(BIN))
KOK = os.environ.get("YAMA_IS_KOK") or os.getcwd()
r = subprocess.run([sys.executable, os.path.join(KOK, "tg", "glb_sikistir.py"), tmp, go]); assert r.returncode == 0
os.remove(tmp)
print("ADIM 50: %d / %d üçgen dejenere atıldı · %d kullanılmayan köşe atıldı · %s" % (atilan, toplam, kv, go))
