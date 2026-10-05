# -*- coding: utf-8 -*-
"""topfix ortak: m8kit Glb (dunya mm) + bilesen bul/sil/tasi + katı ekle"""
import os, sys, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.dirname(H)
sys.path.insert(0, os.path.join(S, "gece")); sys.path.insert(0, os.path.join(S, "tg")); sys.path.insert(0, H)
from m8kit import Glb, tup, kutu_ucgen, silindir_ucgen
LOG = []
def log(*a):
    s = " ".join(str(x) for x in a); LOG.append(s); print(s)

def komps(G, ad):
    """[(p, tri_mask, lo, hi, n)] ad adli tum primlerdeki bilesenler"""
    out = []
    for p in G.prims:
        if p["name"] != ad or p.get("gizli") or len(p["T"]) == 0: continue
        if p["pr"].get("mode", 4) != 4: continue
        tl, kut = G.komp(p); vis = G.gorunur(p)
        for c, (lo, hi, n) in kut.items():
            out.append((p, (tl == c) & vis, np.asarray(lo), np.asarray(hi), n))
    return out

def kutu_esit(lo, hi, K, tol=1.0):
    return all(abs(a - b) <= tol for a, b in zip([lo[0], hi[0], lo[1], hi[1], lo[2], hi[2]], K))

def icinde(lo, hi, K, e=0.05):
    return lo[0] >= K[0] - e and hi[0] <= K[1] + e and lo[1] >= K[2] - e and hi[1] <= K[3] + e and lo[2] >= K[4] - e and hi[2] <= K[5] + e

def etiket(G, p, m):
    t = int(np.where(m)[0][0]); ex = p["pr"].get("extras", {})
    kat = G.etiket_of(p, t, "kat") if ex.get("kat") else None
    mek = G.etiket_of(p, t, "mek") if ex.get("mek") else None
    kpk = bool(G.kpk_maske(p)[t]) if ex.get("kpk") else False
    return kat, mek, kpk

def sil_kutu(G, ad, K, tol=1.0, adet=1, not_=""):
    c = [x for x in komps(G, ad) if kutu_esit(x[2], x[3], K, tol)]
    if adet is not None and len(c) != adet:
        log("UYARI sil_kutu", ad, K, "bulunan", len(c), not_)
    et = None
    for p, m, lo, hi, n in c:
        et = etiket(G, p, m); G.sil(p, m)
    log("SIL %-28s %s x%d %s" % (ad, [round(v, 1) for v in K], len(c), not_))
    return et

def sil_pred(G, ad, pred, not_=""):
    c = [x for x in komps(G, ad) if pred(x[2], x[3], x[4])]
    for p, m, lo, hi, n in c:
        G.sil(p, m)
    log("SIL %-28s %d bilesen %s" % (ad, len(c), not_))
    return c

def tasi(G, p, m, f):
    """yerinde tasi; kose paylasimi varsa sil + yeniden ekle (ayni etiket)"""
    vis = G.gorunur(p)
    vin = np.unique(p["T"][m].reshape(-1)); vout = np.unique(p["T"][vis & ~m].reshape(-1))
    if np.intersect1d(vin, vout).size == 0:
        p["X"][vin] = f(p["X"][vin].copy()); p["degX"] = True; return "yerinde"
    # paylasimli: etiket gruplari ile yeniden ekle
    idx = np.where(m)[0]; gr = {}
    for t in idx:
        ex = p["pr"].get("extras", {})
        k = (G.etiket_of(p, t, "kat") if ex.get("kat") else None, G.etiket_of(p, t, "mek") if ex.get("mek") else None,
             bool(G.kpk_maske(p)[t]) if ex.get("kpk") else False)
        gr.setdefault(k, []).append(t)
    Pw = p["X"][p["T"]]
    for (kat, mek, kpk), tt in gr.items():
        Q = f(Pw[np.array(tt)].reshape(-1, 3).copy()).reshape(-1, 3, 3)
        G._ekle_dunya(p, Q, kat, mek, kpk)
    G.sil(p, m); return "yeniden"

def ekle_kati(G, ad, solids, kat, mek, kpk=False, tol=0.1, ang=0.2):
    if not isinstance(solids, (list, tuple)): solids = [solids]
    P, I = G.ag(solids, tol, ang)
    p = [q for q in G.prims if q["name"] == ad and not q.get("gizli")][0]
    return G._ekle_dunya(p, P[I], kat, mek, kpk)

def ekle_ucgen(G, ad, Pw, kat, mek, kpk=False):
    p = [q for q in G.prims if q["name"] == ad and not q.get("gizli")][0]
    return G._ekle_dunya(p, np.asarray(Pw, float), kat, mek, kpk)

def mek_no(G, kod):
    M = G.J["scenes"][0]["extras"]["mekanizmalar"]
    return [i for i, m in enumerate(M) if m["kod"] == kod][0]

def kat_no(G, kod):
    K = G.J["scenes"][0]["extras"]["kategoriler"]
    return [i for i, k in enumerate(K) if k["kod"] == kod][0]

def kaydet(G, yol):
    G.kaydet(yol); open(os.path.splitext(yol)[0] + "_log.txt", "w", encoding="utf-8").write("\n".join(LOG)); log("yazildi", yol)


def tri_kutu(G, ad, K, e=0.1):
    """[(p, maske)] ucgenleri tamamen K kutusunda"""
    out = []
    for p in G.prims:
        if p["name"] != ad or p.get("gizli") or len(p["T"]) == 0: continue
        P = p["X"][p["T"]]; lo = P.min(1); hi = P.max(1)
        m = G.gorunur(p) & (lo[:, 0] >= K[0] - e) & (hi[:, 0] <= K[1] + e) & (lo[:, 1] >= K[2] - e) & (hi[:, 1] <= K[3] + e) & (lo[:, 2] >= K[4] - e) & (hi[:, 2] <= K[5] + e)
        if m.any(): out.append((p, m))
    return out


def sil_tri(G, ad, K, e=0.1, not_="", bekle=True):
    L = tri_kutu(G, ad, K, e); n = 0; et = None
    for p, m in L:
        et = etiket(G, p, m); n += G.sil(p, m)
    log("SIL-TRI %-26s %s %d ucgen %s" % (ad, [round(v, 1) for v in K], n, not_))
    if bekle and n == 0: log("   UYARI: bos")
    return et, n


def tasi_tri(G, ad, K, f, e=0.1, not_=""):
    L = tri_kutu(G, ad, K, e); n = 0
    for p, m in L:
        tasi(G, p, m, f); n += int(m.sum())
    log("TASI-TRI %-25s %s %d ucgen %s" % (ad, [round(v, 1) for v in K], n, not_))
    if n == 0: log("   UYARI: bos")
    return n


def al_tri(G, ad, K, e=0.1):
    """kutudaki ucgenlerin dunya koordinati + etiket (kopya icin)"""
    out = []
    for p, m in tri_kutu(G, ad, K, e):
        out.append((p["X"][p["T"][m]].copy(), etiket(G, p, m)))
    return out
