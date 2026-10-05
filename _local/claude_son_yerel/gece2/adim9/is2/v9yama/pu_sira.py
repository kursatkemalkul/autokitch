# -*- coding: utf-8 -*-
"""v9 SIRA YAMASI (adım 05 sonu) · TOPPING_MODUL__pu köşe SIRASI.
topping_govde_yeni.py bugün yeniden çalışınca PU duvarının sağ şeridinde (x 2441–2498,5) aynı üçgenler, aynı indislerle ama köşe tamponunda
FARKLI SIRADA çıkıyor (OCC Boolean sonucunda yüz sırası bellek adresine bağlı; geometri birebir aynı: 3180 üçgen, üçgen kümesi eşit).
Sonraki 26 adım düğümleri üçgen/köşe sırasıyla işlediği için bu sıra kayıtlı v8o'daki sıraya getirilir: yalnız listelenen köşelerin
konum + normal değerleri yer değiştirir, üçgen kümesi değişmezse yazılır (değişirse DURUR). Sıra zaten kayıtlıysa dokunmaz.
python pu_sira.py hat3_v8o.glb pu_sira_v8o.json          (yerinde)
python pu_sira.py --uret yeni.glb kayitli.glb pu_sira_v8o.json   (veri dosyasını üretir)"""
import json, struct, sys
import numpy as np

DUGUM = "TOPPING_MODUL__pu"


def oku(yol):
    raw = bytearray(open(yol, "rb").read()); jl = struct.unpack("<I", raw[12:16])[0]
    J = json.loads(bytes(raw[20:20 + jl])); bo = 20 + jl + 8
    return raw, J, bo


def dizi(raw, J, bo, i):
    a = J["accessors"][i]; v = J["bufferViews"][a["bufferView"]]
    n = {"SCALAR": 1, "VEC3": 3}[a["type"]]; dt = {5126: np.float32, 5125: np.uint32, 5123: np.uint16}[a["componentType"]]
    off = bo + v.get("byteOffset", 0) + a.get("byteOffset", 0)
    return np.frombuffer(bytes(raw[off:off + a["count"] * n * np.dtype(dt).itemsize]), dt).reshape(-1, n).copy(), off


def prim(J):
    nd = [n for n in J["nodes"] if n.get("name") == DUGUM][0]
    return J["meshes"][nd["mesh"]]["primitives"][0]


def kume(X, I):
    return sorted(map(tuple, np.sort(np.round(X[I.reshape(-1, 3)].astype(float), 4).reshape(-1, 3, 3), axis=1).reshape(-1, 9).tolist()))


if sys.argv[1] == "--uret":
    ry, Jy, by = oku(sys.argv[2]); rk, Jk, bk = oku(sys.argv[3])
    py, pk = prim(Jy), prim(Jk)
    Xy, _ = dizi(ry, Jy, by, py["attributes"]["POSITION"]); Xk, _ = dizi(rk, Jk, bk, pk["attributes"]["POSITION"])
    Ny, _ = dizi(ry, Jy, by, py["attributes"]["NORMAL"]); Nk, _ = dizi(rk, Jk, bk, pk["attributes"]["NORMAL"])
    w = np.where((Xy != Xk).any(1) | (Ny != Nk).any(1))[0]
    json.dump(dict(dugum=DUGUM, kosE=len(Xk), indis=w.tolist(), X=Xk[w].tolist(), N=Nk[w].tolist()), open(sys.argv[4], "w"))
    print("sıra yaması verisi: %d köşe" % len(w)); sys.exit(0)

yol, vy = sys.argv[1], sys.argv[2]
V = json.load(open(vy)); raw, J, bo = oku(yol); p = prim(J)
X, ox = dizi(raw, J, bo, p["attributes"]["POSITION"]); N, on = dizi(raw, J, bo, p["attributes"]["NORMAL"]); I, _ = dizi(raw, J, bo, p["indices"])
assert len(X) == V["kosE"], ("köşe sayısı farklı", len(X), V["kosE"])
w = np.array(V["indis"], int); Xn = X.copy(); Nn = N.copy()
Xn[w] = np.array(V["X"], np.float32); Nn[w] = np.array(V["N"], np.float32)
if np.array_equal(Xn, X) and np.array_equal(Nn, N): print("PU sırası zaten kayıtlı sırada"); sys.exit(0)
assert kume(X, I) == kume(Xn, I), "PU üçgen kümesi değişirdi → yama uygulanmadı"
raw[ox:ox + Xn.nbytes] = Xn.tobytes(); raw[on:on + Nn.nbytes] = Nn.tobytes()
open(yol, "wb").write(bytes(raw)); print("PU köşe sırası kayıtlı v8o sırasına getirildi: %d köşe (geometri aynı)" % len(w))
