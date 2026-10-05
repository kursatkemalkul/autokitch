# -*- coding: utf-8 -*-
"""elk4 · İÇ KABLOLAMA TEMİZLİĞİ (v8zk -> e5): istasyon iç kabloları kapaklı iç kanallara alınır (yeni ELK_IC__kanal), kanal dışında
kalan uzun açık kollar yeniden çizilir (uç noktalar aynı), kanal içinde kalan / boşa düşen kelepçeler silinir, duvar şalteri kalkar.
python b4.py giris.glb cikis.glb spec1 spec2 ..."""
import sys, importlib, re, numpy as np
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\gece2\menu7\z53A"
sys.path.insert(0, S + r"\elk4")
from b4lib import *
import m8kit
from m8kit import delik_ucgenler
from elib import Yeni
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
gi, go = sys.argv[1:3]; SP = [importlib.import_module(m) for m in sys.argv[3:]]
G = m8kit.Glb(gi)
MEKL = [m["kod"] for m in G.J["scenes"][0]["extras"]["mekanizmalar"]]
MAL_KANAL = ("ME2_kanal", (0.70, 0.72, 0.74, 1.0), 0.8, 0.35)
R = []
def rapor(a, n=0): R.append((a, n)); print("  %-80s %s" % (a, n), flush=True)

# 1 · duvar şalteri (Eaton P3-63) kalkar
for p in G.prims:
    if p["name"].startswith("ELK_DUVAR__") and not p.get("gizli"):
        rapor("sil " + p["name"], G.sil(p, G.gorunur(p)))

import ek
for sp in SP:
    for ad_re, lo, hi, et in getattr(sp, "SIL_KUTU", []): ek.sil_kutu_ici(G, ad_re, lo, hi, rapor, et)
# 2 · kablolar yeniden
eski_yol = []; yeni_yol = []
for sp in SP:
    for ci, y in sp.YOL.items():
        d = KAY[ci]; p = G.prims[d["pi"]]; assert p["name"] == d["prim"], (p["name"], d["prim"])
        et = G._etiketler(p, int(d["tri"][0]))
        m = np.zeros(len(p["T"]), bool); m[d["tri"]] = True
        n = G.sil(p, m); eski_yol += [(q["a"], q["b"], q["r"]) for q in d["S"]]
        r = y.get("r", d["r"]); k = 0
        for Q in y["yol"]:
            k += G._ekle_dunya(p, tup(Q, r, 16), *et); yeni_yol += [(np.asarray(a, float), np.asarray(b, float), r) for a, b in zip(Q[:-1], Q[1:])]
        rapor("kablo #%d %s yeniden (sil %d / ekle %d)" % (ci, d["prim"], n, k))

# 3 · yeni kanallar (delikler kablo geçişlerinden)
Y = Yeni(); KUTU = []
for sp in SP:
    import ek
    istc = [ci for ci, dd in enumerate(KAY) if dd["ist"] == sp.IST and dd["S"] and ci not in ek.HORTUM_KAY]
    segs = [s for ci in istc for s in seg_list(ci, sp.YOL)] + [s for s in yeni_yol] + [(np.asarray(a, float), np.asarray(b, float), r) for a, b, r in getattr(sp, "EK_SEG", [])]
    for k in sp.KAN:
        g, dl, uc = kanal_geo(k, segs)
        Y.ekle("ELK_IC__kanal", MAL_KANAL, g, 6, MEKL.index(k["ist"] + "/Elektrik"))
        KUTU.append((np.asarray(k["lo"], float), np.asarray(k["hi"], float)))
        rapor("kanal %s %s %s delik %d uç %s" % (k["ad"], np.round(k["lo"], 1).tolist(), np.round(k["hi"], 1).tolist(), sum(len(v) for v in dl.values()), uc), len(g))
    for ad, eks, lo, hi, rects in getattr(sp, "DELIK", []):
        # mevcut kanal duvarında kablo geçiş deliği
        for p in G.dprims(ad):
            if p.get("gizli"): continue
            P = p["X"][p["T"]]; vis = G.gorunur(p)
            mm = vis & np.all(P.max(1) >= np.asarray(lo), 1) & np.all(P.min(1) <= np.asarray(hi), 1)
            nn = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]); L = np.linalg.norm(nn, axis=1); nn /= np.maximum(L[:, None], 1e-12)
            mm &= (np.abs(nn[:, eks]) > 0.999) & (np.ptp(P[:, :, eks], axis=1) < 0.01)
            if not mm.any(): continue
            duz = sorted(set(np.round(P[mm][:, 0, eks], 3).tolist()))
            gr = {}
            for t in np.where(mm)[0]: gr.setdefault(G._etiketler(p, t), []).append(t)
            for et, tt in gr.items():
                tt = np.array(tt); Q = P[tt]
                for rc in rects:
                    for dd in duz: Q = delik_ucgenler(Q, eks, [dd], *rc)
                mk = np.zeros(len(P), bool); mk[tt] = True; G.sil(p, mk); G._ekle_dunya(p, Q, *et)
            rapor("delik %s %s" % (ad, rects), int(mm.sum()))

# 4 · kelepçeler: yeni kanalın içinde kalan ya da eski (yeniden çizilen) kablo yolunda boşa düşen
def nokta_seg(P, segs):
    best = 1e9
    for a, b, r in segs:
        v = b - a; L2 = max(v @ v, 1e-9); t = np.clip((P - a) @ v / L2, 0, 1); best = min(best, np.linalg.norm(a + t * v - P) - r)
    return best
nsil = 0
for p in G.prims:
    if p.get("gizli") or not re.match(r"ELK_\w+__celik$", p["name"]): continue
    vis = G.gorunur(p)
    if not vis.any(): continue
    idx = np.where(vis)[0]; P = p["X"][p["T"][idx]]
    Pq = np.round(P.reshape(-1, 3), 2); u, inv = np.unique(Pq, axis=0, return_inverse=True); Ti = inv.reshape(-1, 3)
    rr = np.r_[Ti[:, 0], Ti[:, 1]]; cc = np.r_[Ti[:, 1], Ti[:, 2]]
    _, lab = connected_components(coo_matrix((np.ones(len(rr)), (rr, cc)), shape=(len(u), len(u))), directed=False); tl = lab[Ti[:, 0]]
    for c in np.unique(tl):
        mm = tl == c; Q = P[mm].reshape(-1, 3); lo, hi = Q.min(0), Q.max(0); cen = (lo + hi) / 2
        if np.max(hi - lo) > 60: continue
        icte = any(np.all(hi > a + 0.2) and np.all(lo < b - 0.2) for a, b in KUTU)
        bos = eski_yol and nokta_seg(cen, eski_yol) < 8 and nokta_seg(cen, yeni_yol) > 8
        if icte or bos:
            m = np.zeros(len(p["T"]), bool); m[idx[mm]] = True; nsil += G.sil(p, m)
            rapor("kelepçe sil %s %s (%s)" % (p["name"], np.round(cen).astype(int).tolist(), "kanal içi" if icte else "boşa düştü"))
import ek
from elib import KAT as KATD
ek.calistir(G, KAY, rapor, Y, MEKL, KATD)
Y.yaz(G)
G.kaydet(go)
print("yazildi", go, "· kelepçe üçgeni silinen", nsil)
