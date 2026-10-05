# -*- coding: utf-8 -*-
"""menu7 · sayfa jsonları: mekanizma_v3_8.json (liste / parca / kutu / kapsam) + parca_kutulari.json (TOPPING_MODUL parça kutuları) — hat3_v9u.glb'den.
python sayfa_json.py hat3_v9u.glb hat3_v9u_ent.json <W/otonom/hat3d/v3>"""
import json, struct, sys, os
import numpy as np
gi, ent, V3 = sys.argv[1:4]
TD = {5126: np.float32, 5125: np.uint32, 5123: np.uint16, 5121: np.uint8}
raw = open(gi, "rb").read(); jl = struct.unpack("<I", raw[12:16])[0]; J = json.loads(raw[20:20 + jl]); bo = 20 + jl
bl = struct.unpack("<I", raw[bo:bo + 4])[0]; BIN = raw[bo + 8:bo + 8 + bl]


def acc(i):
    a = J["accessors"][i]; v = J["bufferViews"][a["bufferView"]]
    n = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}[a["type"]]; dt = TD[a["componentType"]]
    off = v.get("byteOffset", 0) + a.get("byteOffset", 0)
    r = np.frombuffer(BIN[off:off + a["count"] * n * np.dtype(dt).itemsize], dt)
    return r.reshape(-1, n) if n > 1 else r


def trs(nd):
    if "matrix" in nd: return np.array(nd["matrix"]).reshape(4, 4).T
    M = np.eye(4); t = nd.get("translation", [0, 0, 0]); x, y, z, w = nd.get("rotation", [0, 0, 0, 1]); s = nd.get("scale", [1, 1, 1])
    R = np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)], [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                  [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
    M[:3, :3] = R * np.array(s)[None, :]; M[:3, 3] = t; return M


W = {}
def gez(i, P):
    M = P @ trs(J["nodes"][i]); W[i] = M
    for c in J["nodes"][i].get("children", []): gez(c, M)
for r in J["scenes"][0]["nodes"]: gez(r, np.eye(4))
LISTE = J["scenes"][0]["extras"]["mekanizmalar"]; KOD = [m["kod"] for m in LISTE]
LO = np.full((len(KOD), 3), np.inf); HI = np.full((len(KOD), 3), -np.inf)
for ni, nd in enumerate(J["nodes"]):
    if "mesh" not in nd or ni not in W: continue
    M = W[ni]
    if abs(np.linalg.det(M[:3, :3])) < 1e-9: continue
    for pr in J["meshes"][nd["mesh"]]["primitives"]:
        L = (pr.get("extras") or {}).get("mek")
        if not L: continue
        X = acc(pr["attributes"]["POSITION"]).astype(float) @ M[:3, :3].T + M[:3, 3]
        T = acc(pr["indices"]).astype(np.int64).reshape(-1, 3)
        dej = (T[:, 0] == T[:, 1]) & (T[:, 1] == T[:, 2])
        for k in range(0, len(L) - 2, 3):
            t = T[L[k + 1] // 3:(L[k + 1] + L[k + 2]) // 3][~dej[L[k + 1] // 3:(L[k + 1] + L[k + 2]) // 3]]
            if not len(t): continue
            Q = X[np.unique(t)]; LO[L[k]] = np.minimum(LO[L[k]], Q.min(0)); HI[L[k]] = np.maximum(HI[L[k]], Q.max(0))
KUTU = {KOD[i]: [round(float(LO[i][0]), 4), round(float(HI[i][0]), 4), round(float(LO[i][1]), 4), round(float(HI[i][1]), 4), round(float(LO[i][2]), 4), round(float(HI[i][2]), 4)]
        for i in range(len(KOD)) if np.isfinite(LO[i]).all()}

YM = os.path.join(V3, "mekanizma_v3_8.json"); M = json.load(open(YM, encoding="utf-8"))
ESKI = {"TOPPING/Harç": "TOPPING/Lahmacun harcı", "TOPPING/Sos": "TOPPING/Patates", "TOPPING/Kıyma": "TOPPING/Tavuk"}
# kutu yöntemi denetimi: değişmeyen ünitelerde eski kutu = yeni hesap
fark = []
for k, v in M["kutu"].items():
    if k.startswith("TOPPING/") or k not in KUTU: continue
    d = max(abs(a - b) for a, b in zip(v, KUTU[k]))
    if d > 0.002: fark.append((k, round(d, 4)))
print("kutu yöntemi (TOPPING dışı ünitelerde eski ↔ yeni en büyük fark > 2 mm):", fark or "YOK")
M["glb"] = "hat3_v8.glb (v9u)"
M["liste"] = LISTE
M["parca"] = {k: ESKI.get(v, v) for k, v in M["parca"].items()}
YENI_PARCA = {}
for k, v in list(M["parca"].items()):
    if v == "TOPPING/Patates" and k.startswith("TOPPING_MODUL|sos__"):
        YENI_PARCA[k.replace("|sos__", "|kiyma_orta__")] = "TOPPING/Kıyma"
YENI_PARCA.update({"TOPPING_MODUL|kiyma_orta_hazne_200x440_R25": "TOPPING/Kıyma", "TOPPING_MODUL|kiyma_orta_cikis_dirsegi_paslanmaz_D35": "TOPPING/Kıyma",
                   "TOPPING_MODUL|kiyma_orta_urun_hortumu_D32": "TOPPING/Kıyma", "TOPPING_MODUL|kiyma_orta_raf_gecis_contasi": "TOPPING/Kıyma",
                   "TOPPING_MODUL|kiyma_orta_taban_borusu_D29.8": "TOPPING/Kıyma", "TOPPING_MODUL|kiyma_orta_burc_kilifi": "TOPPING/Kıyma",
                   "TOPPING_MODUL|evaporator_R_silindir_cebi_sac": "TOPPING/Soğutma", "TOPPING_MODUL|evaporator_R_silindir_cebi_PU": "TOPPING/Soğutma",
                   "TOPPING_MODUL|evaporator_R_silindir_cebi_conta": "TOPPING/Soğutma", "TOPPING_MODUL|kiyma_orta_hava_hortumu_D6_x2": "TOPPING/Hava",
                   "TOPPING_MODUL|kiyma_orta_valf_adasi_rakoru_x2": "TOPPING/Hava"})
M["parca"].update(YENI_PARCA)
ESKI_KUTU = M["kutu"]
M["kutu"] = {k: (KUTU[k] if k.startswith("TOPPING/") else ESKI_KUTU.get(ESKI.get(k, k), KUTU.get(k))) for k in [m["kod"] for m in LISTE] if (k in KUTU or k in ESKI_KUTU)}   # yalnız TOPPING üniteleri yeniden ölçülür; diğerleri eski kutu
if isinstance(M.get("kapsam"), dict) and "parca" in M["kapsam"]: M["kapsam"]["parca"] = len(M["parca"])
M["surum"] = M["surum"] + " · v9u (4 Eki 2026, menu7): pide + lahmacun menüsü — Lahmacun harcı / Kıyma (yeni orta UNO) / Patates / Tavuk / Kuşbaşı; Sos kalktı; sağ evaporatörde silindir cebi"
json.dump(M, open(YM, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("mekanizma_v3_8.json: liste", len(LISTE), "· parça", len(M["parca"]), "(+%d)" % len(YENI_PARCA), "· kutu", len(KUTU))
for k in ("TOPPING/Lahmacun harcı", "TOPPING/Kıyma", "TOPPING/Patates", "TOPPING/Tavuk", "TOPPING/Kuşbaşı", "TOPPING/Soğutma", "TOPPING/Hava"): print("  ", k, KUTU.get(k))

# parca_kutulari.json: TOPPING_MODUL parça kutuları (mm) — hazneler yeni ölçü + yeni parçalar
E = json.load(open(ent, encoding="utf-8"))
YP = os.path.join(V3, "parca_kutulari.json"); P = json.load(open(YP, encoding="utf-8"))
L = dict(P["parca"])["TOPPING_MODUL"] if isinstance(P["parca"], dict) else None
PL = P["parca"]["TOPPING_MODUL"]
ESKI_HAZ = {"harc_hazne_bizim": "harc", "sos_hazne_bizim": "patates", "kiyma_hazne_bizim": "tavuk", "kusbasi_hazne_bizim": "kusbasi"}
n_g = 0
for row in PL:
    if row[0] in ESKI_HAZ:
        b = E["hazne"][ESKI_HAZ[row[0]]]["kutu"]; row[2:8] = [round(b[0], 1), round(b[3], 1), round(b[1], 1), round(b[4], 1), round(b[2], 1), round(b[5], 1)]; n_g += 1
b = E["hazne"]["kiyma_orta"]["kutu"]
ekle = [["kiyma_orta_hazne_bizim", 0, round(b[0], 1), round(b[3], 1), round(b[1], 1), round(b[4], 1), round(b[2], 1), round(b[5], 1)],
        ["kiyma_orta_cikis_dirsegi_paslanmaz_D35", 0, 1893.7, 2048.8, 1551.0, 1631.3, -235.2, -152.2],
        ["kiyma_orta_urun_hortumu_D32", 0, 1890.7, 1932.3, 1216.0, 1539.0, -191.0, -149.6],
        ["kiyma_orta_taban_borusu_D29.8", 0, 1896.6, 1926.4, 1048.0, 1182.0, -184.6, -155.0],
        ["evaporator_R_silindir_cebi", 0, 1973.0, 2089.0, 1568.0, 1835.0, -826.0, -630.0]]
PL[:] = [r for r in PL if r[0] not in [e[0] for e in ekle]] + ekle
json.dump(P, open(YP, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("parca_kutulari.json: hazne kutusu güncellendi", n_g, "· eklendi", len(ekle))
