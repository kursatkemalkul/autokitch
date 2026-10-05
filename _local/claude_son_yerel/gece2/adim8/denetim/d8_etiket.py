# -*- coding: utf-8 -*-
"""Kalem 8 etiket: python d8_etiket.py [glb] [mekanizma.json]
her primitif: extras mek/kat (üçlü: değer, başlangıç, adet; indis birimi) ve kpk (çift: başlangıç, adet) → aralık indis sayısı içinde mi, 3'ün katı mı,
çakışan aralık, mek < liste uzunluğu, kat < kategori sayısı, mek/kat etiketsiz üçgen."""
import sys, json, struct, numpy as np
from collections import Counter
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
glb = sys.argv[1] if len(sys.argv) > 1 else S + r"\gece2\adim8\hat3_v9h.glb"
mj = sys.argv[2] if len(sys.argv) > 2 else r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\otonom\hat3d\v3\mekanizma_v3_8.json"
raw = open(glb, "rb").read(); jl = struct.unpack("<I", raw[12:16])[0]; J = json.loads(raw[20:20 + jl])
NM = len(json.load(open(mj, encoding="utf-8"))["liste"]); ex = J["scenes"][0].get("extras", {})
NMG = len(ex.get("mekanizmalar", [])); NK = len(ex.get("kategoriler", []))
H = Counter(); ornek = {}; top_idx = 0; etsiz = Counter()
def hata(k, s):
    H[k] += 1; ornek.setdefault(k, []).append(s) if len(ornek.get(k, [])) < 6 else None
mesh_ad = {}
for i, nd in enumerate(J["nodes"]):
    if "mesh" in nd: mesh_ad.setdefault(nd["mesh"], nd.get("name", "dugum%d" % i))
for mi, m in enumerate(J["meshes"]):
    for pi, pr in enumerate(m["primitives"]):
        ad = "%s/p%d" % (mesh_ad.get(mi, "mesh%d" % mi), pi)
        n = J["accessors"][pr["indices"]]["count"] if "indices" in pr else J["accessors"][pr["attributes"]["POSITION"]]["count"]
        top_idx += n; nt = n // 3; e = pr.get("extras", {}) or {}
        for anah, ust in (("mek", NM), ("kat", NK)):
            L = e.get(anah)
            if not L: etsiz[anah] += nt; hata(anah + "_yok", ad); continue
            if len(L) % 3: hata(anah + "_uzunluk", ad); continue
            kap = np.zeros(nt, np.int16)
            for k in range(0, len(L), 3):
                v, s, c = L[k:k + 3]
                if s % 3 or c % 3: hata(anah + "_3kati_degil", "%s %s" % (ad, L[k:k + 3]))
                if s < 0 or c <= 0 or s + c > n: hata(anah + "_aralik_disi", "%s %s n=%d" % (ad, L[k:k + 3], n)); continue
                if not (0 <= v < ust): hata(anah + "_deger_disi", "%s v=%s ust=%d" % (ad, v, ust))
                kap[s // 3:(s + c) // 3] += 1
            if (kap == 0).any(): etsiz[anah] += int((kap == 0).sum()); hata(anah + "_etiketsiz_ucgen", "%s %d üçgen" % (ad, (kap == 0).sum()))
            if (kap > 1).any(): hata(anah + "_cakisan_aralik", "%s %d üçgen" % (ad, (kap > 1).sum()))
        L = e.get("kpk")
        if L:
            if len(L) % 2: hata("kpk_uzunluk", ad)
            for k in range(0, len(L) - 1, 2):
                s, c = L[k:k + 2]
                if s % 3 or c % 3: hata("kpk_3kati_degil", "%s %s" % (ad, L[k:k + 2]))
                if s < 0 or c <= 0 or s + c > n: hata("kpk_aralik_disi", "%s %s n=%d" % (ad, L[k:k + 2], n))
print("GLB", glb.split("\\")[-1], "· mesh", len(J["meshes"]), "· toplam indis", top_idx, "· mekanizma liste", NM, "(GLB içi", NMG, ") · kategori", NK)
print("HATA toplam", sum(H.values()), dict(H)); print("etiketsiz üçgen", dict(etsiz))
for k, v in ornek.items(): print(" ", k, v)
