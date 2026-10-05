# -*- coding: utf-8 -*-
"""TOPFIX 2 · TOPPING birimleri yeni x'lere (cep yok, ic 1496-2440):
alt sira  kiyma 1501-1691 · [harc hortumu 1691-1753, eksen 1722] · kusbasi 1753-1943 · kasar govde 1948,5-2228,5 (kilavuz 1944-2233)
          · [sos hortumu 2228,5-2290,5, eksen 2259,5] · sucuk govde 2290,5-2430,5 (kilavuz 2286-2435)
ust       harc (BUYUK UNO) eksen 1722 · sos (kucuk UNO) eksen 2259,5
Birim = mek etiketi (TOPPING/Kiyma ...). Animasyonlu dugumler translation + animasyon cikti kanali ile.
python t2_tasi.py giris.glb cikis.glb"""
import sys, json, numpy as np
from tlib import *
gi, go = sys.argv[1:3]
G = Glb(gi)
KOD = {"kiyma": "TOPPING/Kıyma", "kusbasi": "TOPPING/Kuşbaşı", "kasar": "TOPPING/Kaşar", "sucuk": "TOPPING/Sucuk", "harc": "TOPPING/Harç", "sos": "TOPPING/Sos"}
DX = {"kiyma": -28.5, "kusbasi": 29.5, "kasar": 26.5, "sucuk": 5.0, "harc": 225.0, "sos": 9.5}
MK = {mek_no(G, v): k for k, v in KOD.items()}
DUGUM = {"TOPPING_DONER__VALF_KIYMA": "kiyma", "TOPPING_DONER__VALF_KUSBASI": "kusbasi", "TOPPING_DONER__VALF_SOS": "sos",
         "TOPPING_DONER__VALF_HARC": "harc", "TOPPING_DONER__HELEZON_KASAR": "kasar", "TOPPING_DONER__KARISTIRICI_KASAR": "kasar",
         "TOPPING_DONER__HELEZON_SUCUK": "sucuk", "TOPPING_DONER__KARISTIRICI_SUCUK": "sucuk"}
for u in ("KIYMA", "KUSBASI", "SOS", "HARC"):
    for mt in ("paslanmaz", "pom"): DUGUM["TOPPING_MODUL__%s__PISTON_%s" % (mt, u)] = u.lower()
say = {}
for p in G.prims:
    if p["name"] in DUGUM or p.get("gizli") or len(p["T"]) == 0: continue
    L = p["pr"].get("extras", {}).get("mek") or []
    if not L: continue
    lab = np.full(len(p["T"]), -1, int)
    for k in range(0, len(L) - 2, 3): lab[L[k + 1] // 3:(L[k + 1] + L[k + 2]) // 3] = L[k]
    vis = G.gorunur(p)
    for mk, u in MK.items():
        m = vis & (lab == mk)
        if not m.any(): continue
        r = tasi(G, p, m, lambda V, d=DX[u]: V + np.array([d, 0, 0]))
        say.setdefault(u, []).append((p["name"], int(m.sum()), r))
for u, l in say.items():
    log("TASI %-8s %+6.1f  %d prim %d ucgen (%s)" % (u, DX[u], len(l), sum(x[1] for x in l), ",".join(sorted(set(x[2] for x in l)))))
# animasyonlu dugumler (m7a yontemi)
J = G.J; yapilan = set()
for ad_, u in DUGUM.items():
    d = np.array([DX[u], 0, 0])
    ni = [k for k, nd in enumerate(J["nodes"]) if nd.get("name") == ad_][0]; nd = J["nodes"][ni]
    assert "matrix" not in nd and ni in G.J["scenes"][0]["nodes"], ad_
    nd["translation"] = (np.array(nd.get("translation", [0, 0, 0]), float) + d / 1000.0).tolist()
    for p in G.prims:
        if p["nd"] is nd:
            p["t"] = np.array(nd["translation"], float); p["X"] = p["X"] + d
            if "W" in p: p["W"] = p["W"].copy(); p["W"][:3, 3] += d / 1000.0
    for an in J.get("animations", []):
        for ch in an["channels"]:
            if ch["target"]["node"] != ni or ch["target"]["path"] != "translation": continue
            a = an["samplers"][ch["sampler"]]["output"]
            if a in yapilan: continue
            yapilan.add(a)
            A = J["accessors"][a]; v = J["bufferViews"][A["bufferView"]]
            off = v.get("byteOffset", 0) + A.get("byteOffset", 0); n = A["count"]
            arr = np.frombuffer(bytes(G.BIN[off:off + n * 12]), np.float32).reshape(-1, 3).copy() + (d / 1000.0).astype(np.float32)
            G.BIN[off:off + n * 12] = arr.tobytes()
            if "min" in A: A["min"] = arr.min(0).tolist(); A["max"] = arr.max(0).tolist()
    log("DUGUM %-40s x%+.1f" % (ad_, DX[u]))
# kaset motor soketleri (Elektrik etiketli, motorun ustunde) birimle
for (x0, x1), u in (((2057.0, 2067.0), "kasar"), ((2350.5, 2360.5), "sucuk")):
    tasi_tri(G, "TOPPING_MODUL__koyu", (x0, x1, 1141.0, 1322.0, -812.1, -801.9), lambda V, d=DX[u]: V + np.array([d, 0, 0]), not_="motor soketi " + u)
# harc yayici kelepce kanadi +x (kusbasi hortum araligina) -> -z (sos'taki gibi, m7c)
XL, ZH = 1722.0, -170.0
def don(V):
    W = V.copy(); vx = V[:, 0] - XL; vz = V[:, 2] - ZH; W[:, 0] = XL + vz; W[:, 2] = ZH - vx; return W
tasi_tri(G, "TOPPING_MODUL__paslanmaz", (1746.9, 1762.1, 1205.9, 1214.1, -174.1, -165.9), don, not_="harc kelepce kanadi +x -> -z")
kaydet(G, go)
