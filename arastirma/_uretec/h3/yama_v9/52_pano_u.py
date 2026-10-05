# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 52 · ANA PANO U (ÜST DEPO) İSTASYONUNA AİT (4 Eki 2026 · Claude · YEREL) — GEOMETRİ DEĞİŞMEZ, yalnız etiket
python 52_pano_u.py girdi.glb cikti.glb      (zincir: hat3_v9s.glb → hat3_v9t.glb)

Kemal: sol menüde "U · Üst depo" gizlenince ana pano açıkta kalıyordu — pano 'Elektrik / Ana pano' (hat geneli) ünitesindeydi, oysa fiziksel
olarak fırın üstü U_F'nin içinde (x 3518–3978, y 1867–2176). Bu adım:
  1. 'Elektrik/Ana pano' etiketli her üçgen (pano gövdesi, kapağı, ana şalter + kol + mil + somun, cihazlar, DIN, kanal, Harting, rakorlar,
     lastik geçit, kör tapa, pano içi / çıkış kabloları, pano gömme giriş cebi + arka rakorlar, bina giriş kabloları) → 'U/Elektrik'
     (U istasyonunun Elektrik ünitesi; panonun arkasındaki dik kapaklı kanal ELK_IC zaten U/Elektrik'te);
  2. YALNIZ U gövdesinin arka düzleminin (z −830) gerisinde kalan üçgenler (bina kablosunun makine dışındaki ucu: 3 köşesi de z < −830,5)
     → 'Elektrik/Ana hat' (makine dışı, istasyonlar arası hat tarafı);
  3. 'Elektrik/Ana pano' boş kalır → sahne extras 'mekanizmalar' listesinden çıkarılır, sonraki indisler bir azaltılır
     (kademe yapısı, 'kat' disiplin etiketleri, 'kpk', BIN bayt bayt AYNI).
Denetim: her primitive'de mek aralıkları indis sayısını tam kapsar; etiket başına üçgen sayısı (eski → yeni) tutar; BIN değişmez."""
import json, struct, sys, os, time
import numpy as np

gi, go = sys.argv[1:3]
t0 = time.time()
ESKI, YENI_IC, YENI_DIS = "Elektrik/Ana pano", "U/Elektrik", "Elektrik/Ana hat"
Z_ARKA = -830.0 - 0.5          # U_F / U_KE gövdesinin arka düzlemi (U/Gövde kutusu z −830 … 76) − 0,5 mm pay

raw = open(gi, "rb").read()
jl = struct.unpack("<I", raw[12:16])[0]
J = json.loads(raw[20:20 + jl]); bo = 20 + jl
bl = struct.unpack("<I", raw[bo:bo + 4])[0]; BIN = raw[bo + 8:bo + 8 + bl]
TD = {5126: np.float32, 5125: np.uint32, 5123: np.uint16, 5121: np.uint8}


def acc(i):
    a = J["accessors"][i]; v = J["bufferViews"][a["bufferView"]]
    n = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}[a["type"]]; dt = TD[a["componentType"]]
    off = v.get("byteOffset", 0) + a.get("byteOffset", 0); st = v.get("byteStride", 0); isz = np.dtype(dt).itemsize
    if st and st != n * isz:
        b = np.frombuffer(BIN[off:off + st * a["count"]], np.uint8).reshape(a["count"], st)[:, :n * isz]
        r = np.frombuffer(b.tobytes(), dt)
    else:
        r = np.frombuffer(BIN[off:off + a["count"] * n * isz], dt)
    return r.reshape(-1, n) if n > 1 else r


def trs(nd):
    if "matrix" in nd: return np.array(nd["matrix"]).reshape(4, 4).T
    M = np.eye(4); t = nd.get("translation", [0, 0, 0]); x, y, z, w = nd.get("rotation", [0, 0, 0, 1]); s = nd.get("scale", [1, 1, 1])
    R = np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                  [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                  [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
    M[:3, :3] = R * np.array(s)[None, :]; M[:3, 3] = t; return M


W = {}


def gez(i, P):
    M = P @ trs(J["nodes"][i]); W[i] = M
    for c in J["nodes"][i].get("children", []): gez(c, M)


for r in J["scenes"][0]["nodes"]: gez(r, np.eye(4))
EX = J["scenes"][0]["extras"]
KOD = [m["kod"] for m in EX["mekanizmalar"]]
ia, iu, ih = KOD.index(ESKI), KOD.index(YENI_IC), KOD.index(YENI_DIS)
YK = [k for k in KOD if k != ESKI]
ESLE = {i: YK.index(YENI_IC if i == ia else k) for i, k in enumerate(KOD)}     # eski indis → yeni indis (ia → U/Elektrik)
ESLE_DIS = YK.index(YENI_DIS)


def aralik(L, n):
    out = np.full(n, -1, np.int64)
    for k in range(0, len(L) - 2, 3): out[L[k + 1] // 3:(L[k + 1] + L[k + 2]) // 3] = L[k]
    return out


def kodla(a):
    out = []; s = 0
    for i in range(1, len(a) + 1):
        if i == len(a) or a[i] != a[s]:
            out += [int(a[s]), s * 3, (i - s) * 3]; s = i
    return out


say_eski = np.zeros(len(KOD), np.int64); say_yeni = np.zeros(len(YK), np.int64)
dugum = {}; n_ic = n_dis = 0
islenen = set()
for ni, nd in enumerate(J["nodes"]):
    if "mesh" not in nd or ni not in W: continue
    mi = nd["mesh"]
    for pi, pr in enumerate(J["meshes"][mi]["primitives"]):
        ex = pr.get("extras") or {}; L = ex.get("mek")
        if not L: continue
        n = J["accessors"][pr["indices"]]["count"] // 3
        mk = aralik(L, n); assert (mk >= 0).all(), nd["name"]
        if (mi, pi) in islenen:                # aynı ağı paylaşan düğüm: etiket ağa ait, bir kez işlenir (paylaşım varsa konum ilk düğüme göre)
            continue
        islenen.add((mi, pi))
        np.add.at(say_eski, mk, 1)
        yeni = np.array([ESLE[int(v)] for v in range(len(KOD))], np.int64)[mk]
        s = np.where(mk == ia)[0]
        if len(s):
            T = acc(pr["indices"]).reshape(-1, 3).astype(np.int64)[s]
            X = acc(pr["attributes"]["POSITION"]).astype(float); M = W[ni]
            Zw = ((X @ M[:3, :3].T + M[:3, 3]) * 1000.0)[:, 2]
            dis = np.all(Zw[T] < Z_ARKA, axis=1)
            yeni[s[dis]] = ESLE_DIS
            n_dis += int(dis.sum()); n_ic += int((~dis).sum())
            d = dugum.setdefault(nd["name"], [0, 0]); d[0] += int((~dis).sum()); d[1] += int(dis.sum())
        np.add.at(say_yeni, yeni, 1)
        L2 = kodla(yeni)
        assert sum(L2[2::3]) == n * 3 and L2[1] == 0 and all(L2[3 * i + 1] + L2[3 * i + 2] == L2[3 * i + 4] for i in range(len(L2) // 3 - 1)), nd["name"]
        ex["mek"] = L2

# denetim: üçgen sayıları
for i, k in enumerate(KOD):
    if i == ia: continue
    beklenen = say_eski[i] + (n_ic if i == iu else n_dis if i == ih else 0)
    assert say_yeni[YK.index(k)] == beklenen, (k, int(say_eski[i]), int(say_yeni[YK.index(k)]))
assert n_ic + n_dis == say_eski[ia] and say_eski.sum() == say_yeni.sum()
assert n_dis < 200, "ADIM 52 DUR: U dışında beklenenden çok pano üçgeni (%d)" % n_dis

EX["mekanizmalar"] = [m for m in EX["mekanizmalar"] if m["kod"] != ESKI]
EX["gruplama"] = EX.get("gruplama", "") + " · v3 4 Eki 2026: ana pano U/Elektrik'te (U gizlenince pano da gizlenir), 'Elektrik/Ana pano' ünitesi kalktı"
js = json.dumps(J, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
js += b" " * ((4 - len(js) % 4) % 4)
binc = raw[bo:]
out = struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(js) + len(binc)) + struct.pack("<II", len(js), 0x4E4F534A) + js + binc
open(go, "wb").write(out)
KAYIT = dict(adim=52, ad="ana pano U/Elektrik'e", u_elektrik_eklenen_ucgen=n_ic, ana_hat_eklenen_ucgen=n_dis,
             dugum={k: dict(U_Elektrik=v[0], Ana_hat=v[1]) for k, v in sorted(dugum.items())},
             mekanizmalar_eski=len(KOD), mekanizmalar_yeni=len(YK))
json.dump(KAYIT, open(go[:-4] + "_ent.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("ADIM 52 · 'Elektrik/Ana pano' %d üçgen → U/Elektrik %d · Elektrik/Ana hat %d (U arka düzleminin gerisi) · ünite %d → %d · BIN aynı · %s · %.0f sn"
      % (int(say_eski[ia]), n_ic, n_dis, len(KOD), len(YK), go, time.time() - t0))
