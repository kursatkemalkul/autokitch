# -*- coding: utf-8 -*-
"""GECE2 ADIM 2 · C: yesil pnomatik hortumlar kapakli kucuk HAVA KANALINDA (elk5 madde 3). Tasarim hava/htas.py.
Her grup: dayanan kutular tek surekli kanal (dayanma yuzunde ic kesit kadar agiz), hortum gectigi yerde delik (r + 1,5), 304 1,2 mm.
python a4_hava.py giris.glb cikis.glb [--kuru]   (--kuru: yalniz engel + acik uzunluk raporu)"""
import sys, os, json, pickle, re, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.dirname(os.path.dirname(HERE))
for q in (os.path.join(HERE, "hava"), os.path.join(S, "elk5"), os.path.join(S, "elk2"), os.path.join(S, "gece"), S): sys.path.insert(0, q)
from m8kit import Glb, kutu_ucgen
from elib import Yeni, plaka, KAT as KATD
from ortam_sat import tri_kutu
import htas
T = htas.T
KAY = pickle.load(open(os.path.join(HERE, "hava", "kayh.pkl"), "rb"))["KAY"]
SEG = [(np.asarray(q["a"], float), np.asarray(q["b"], float), float(q["r"])) for d in KAY for q in d["S"]]
kuru = "--kuru" in sys.argv
g = Glb(sys.argv[1]); LOG = []
def log(*a): s = " ".join(str(x) for x in a); LOG.append(s); print(s, flush=True)
MEKL = [m["kod"] for m in g.J["scenes"][0]["extras"]["mekanizmalar"]]
HORTUM = r"^(K_ELEKTRIK__hava|TOPPING_MODUL__hava_ana|HAVA_KOMPRESOR__hava_ana|ELK_ZINCIR__hava)$"
PP, AD = [], []
for p in g.prims:
    if p.get("gizli") or re.match(HORTUM, p["name"]): continue
    vis = g.gorunur(p); P = p["X"][p["T"][vis]]; PP.append(P); AD += [p["name"]] * len(P)
PP = np.concatenate(PP); AD = np.array(AD); TLO = PP.min(1); THI = PP.max(1)
def engel(lo, hi, e=0.05):
    lo = np.asarray(lo, float) + e; hi = np.asarray(hi, float) - e
    m = np.all(THI > lo, 1) & np.all(TLO < hi, 1); i = np.where(m)[0]; i = i[tri_kutu(PP[i], lo, hi)]
    out = {}
    for j in i:
        Q = PP[j]; a = out.setdefault(AD[j], [Q.min(0), Q.max(0), 0]); a[0] = np.minimum(a[0], Q.min(0)); a[1] = np.maximum(a[1], Q.max(0)); a[2] += 1
    return out


def kutu_kanal(lo, hi, komsu):
    """6 plaka; hortum delikleri + komsu kutu agizlari"""
    lo = np.asarray(lo, float); hi = np.asarray(hi, float); out = []
    for ax in range(3):
        u, w = [i for i in range(3) if i != ax]
        for sg in (-1, 1):
            v0, v1 = (lo[ax], lo[ax] + T) if sg < 0 else (hi[ax] - T, hi[ax])
            # plaka kapsami: x-yuzleri tam, y-yuzleri x icinde, z-yuzleri x,y icinde
            r = {u: [lo[u], hi[u]], w: [lo[w], hi[w]]}
            for k in (u, w):
                if k < ax: r[k] = [lo[k] + T, hi[k] - T]
            dl = []
            pl = hi[ax] if sg > 0 else lo[ax]
            for b0, b1 in komsu:
                bp = b0[ax] if sg > 0 else b1[ax]
                if abs(bp - pl) > 0.01: continue
                a0 = max(lo[u], b0[u]) + T; a1 = min(hi[u], b1[u]) - T; c0 = max(lo[w], b0[w]) + T; c1 = min(hi[w], b1[w]) - T
                if a1 > a0 and c1 > c0: dl.append((a0, a1, c0, c1))
            for a, b, rr in SEG:
                vv = b - a
                if abs(vv[ax]) < 1e-9: continue
                s = (pl - a[ax]) / vv[ax]
                if s < -1e-6 or s > 1 + 1e-6: continue
                P = a + s * vv
                if not (lo[u] - rr <= P[u] <= hi[u] + rr and lo[w] - rr <= P[w] <= hi[w] + rr): continue
                m = rr + 1.5
                dl.append((max(lo[u], P[u] - m), min(hi[u], P[u] + m), max(lo[w], P[w] - m), min(hi[w], P[w] + m)))
            out.append(plaka(ax, v0, v1, r[u][0], r[u][1], r[w][0], r[w][1], dl))
    return np.concatenate([q for q in out if len(q)])


def acik(ici):
    """hortum bilesenleri: kanal disinda kalan, uclardan 150 mm'den uzak uzunluk"""
    R = []
    for i, d in enumerate(KAY):
        L = sum(np.linalg.norm(q["b"] - q["a"]) for q in d["S"])
        if L < 1: continue
        # uc noktalari: yalniz bir kez gecen noktalar
        pts = {}
        for q in d["S"]:
            for P in (q["a"], q["b"]): k = tuple(np.round(P, 1)); pts[k] = pts.get(k, 0) + 1
        uclar = [np.array(k) for k, n in pts.items() if n == 1]
        fazla = 0.0
        for q in d["S"]:
            a, b = q["a"], q["b"]; l = np.linalg.norm(b - a); n = max(2, int(l / 2))
            for t in (np.arange(n) + 0.5) / n:
                P = a + t * (b - a)
                if ici(P) or q["ic"][min(int(t * len(q["ic"])), len(q["ic"]) - 1)]: continue
                if uclar and min(np.linalg.norm(P - u) for u in uclar) <= 150: continue      # kus ucusu (dik acili yolda guvenli taraf degil -> asagida yol boyu)
                fazla += l / n
        R.append((i, d["prim"], d["ist"], round(L), round(fazla)))
    return R


KUTU = [(grp, ist, ad, np.array(lo), np.array(hi)) for grp, ist, L in htas.GRUP for ad, lo, hi in L]
def ici(P): return any(np.all(P >= lo + 0.5) and np.all(P <= hi - 0.5) for _, _, _, lo, hi in KUTU)
Y = Yeni(); PARCA = []
if not kuru:
    for ad_, lo_, hi_ in htas.CENTIK:
        for p in g.dprims(ad_):
            if p.get("gizli"): continue
            m = g.kutu_maske(p, lo_[0], hi_[0], lo_[1], hi_[1], lo_[2], hi_[2])
            if not m.any(): continue
            e_ = g._etiketler(p, int(np.where(m)[0][0])); g.sil(p, m)
            k = [b for b in KUTU if np.all(b[3] < np.array(hi_)) and np.all(b[4] > np.array(lo_))][0]
            parc = [kutu_ucgen(lo_, (hi_[0], k[3][1] - 0.2, hi_[2])), kutu_ucgen((lo_[0], k[4][1] + 0.2, lo_[2]), hi_)]
            g._ekle_dunya(p, np.concatenate(parc), *e_); log("centik %s y %.1f-%.1f (kanal gecisi)" % (ad_, k[3][1] - 0.2, k[4][1] + 0.2))
    for grp, ist, ad, lo, hi in KUTU:
        for p in g.prims:
            if p.get("gizli") or re.match(HORTUM, p["name"]) or p["name"].startswith(("HAVA_IC", "ELK_IC")): continue
            P = p["X"][p["T"]]
            if not (np.all(P.reshape(-1, 3).max(0) > lo) and np.all(P.reshape(-1, 3).min(0) < hi)): continue
            tl, kut = g.komp(p)
            for i, (l2, h2, n) in kut.items():
                if np.all(h2 > lo + 0.05) and np.all(l2 < hi - 0.05) and (h2 - l2).max() < 60:
                    m = (tl == i) & g.gorunur(p)
                    if tri_kutu(P[m], lo + 0.05, hi - 0.05).any():
                        g.sil(p, m); log("kanal icinde kalan kelepce sil %s %s %s" % (p["name"], np.round(l2).tolist(), np.round(h2).tolist()))
for grp, ist, ad, lo, hi in KUTU:
    komsu = [(l2, h2) for g2, _, a2, l2, h2 in KUTU if g2 == grp and a2 != ad]
    e = engel(lo, hi)
    log("%s.%s %s lo %s hi %s · engel %s" % (grp, ad, ist, lo.tolist(), hi.tolist(), {k: (np.round(v[0]).tolist(), np.round(v[1]).tolist(), v[2]) for k, v in e.items()}))
    if kuru: continue
    G = kutu_kanal(lo, hi, komsu)
    Y.ekle("HAVA_IC__kanal", ("ME2_kanal", (0.70, 0.72, 0.74, 1.0), 0.8, 0.35), G, KATD["HAVA"], MEKL.index(ist + "/Hava"))
    PARCA.append(dict(ad="hava_kanali_%s_%s" % (grp, ad), ist=ist, lo=lo.tolist(), hi=hi.tolist()))
# askılar
from m8kit import Yuzey
YS = Yuzey(g, haric=("K_ELEKTRIK__hava", "TOPPING_MODUL__hava_ana", "HAVA_KOMPRESOR__hava_ana", "ELK_ZINCIR__hava", "HAVA_IC__kanal"))
KB_ = {"%s.%s" % (b[0], b[2]): b for b in KUTU}
for ka, ax, sg, konum in htas.KONSOL:
    grp, ist, ad, lo, hi = KB_[ka]
    L = int(np.argmax(hi - lo)); u = [i for i in range(3) if i not in (ax, L)][0]
    for c in konum:
        o = (lo + hi) / 2; o[L] = c; o[ax] = hi[ax] if sg > 0 else lo[ax]
        d = np.zeros(3); d[ax] = sg; ts = []
        for f in (-6.0, 0.0, 6.0):
            q = o.copy(); q[u] += f; t = YS.isin(q, d, 60)
            ts.append(t)
        if any(t is None for t in ts): log("askı yok %s %s yön %d @%.0f (60 mm içinde yapı yok)" % (ka, "xyz"[ax], sg, c)); continue
        t = min(ts)
        blo = o.copy(); bhi = o.copy()
        blo[u] -= 7; bhi[u] += 7; blo[L] -= 1; bhi[L] += 1
        e0, e1 = (o[ax], o[ax] + sg * (t - 2)) if True else (0, 0)
        blo[ax], bhi[ax] = min(e0, e1), max(e0, e1)
        flo = blo.copy(); fhi = bhi.copy(); flo[L] -= 6; fhi[L] += 6
        f0, f1 = o[ax] + sg * (t - 2), o[ax] + sg * t
        flo[ax], fhi[ax] = min(f0, f1), max(f0, f1)
        if not kuru:
            Y.ekle("HAVA_IC__aski", ("ME2_kanal", (0.70, 0.72, 0.74, 1.0), 0.8, 0.35), np.concatenate([kutu_ucgen(blo, bhi), kutu_ucgen(flo, fhi)]), KATD["HAVA"], MEKL.index(ist + "/Hava"))
        log("askı %s %s yön %+d @%.0f boy %.1f" % (ka, "xyz"[ax], sg, c, t))
for r in acik(ici):
    if r[4] > 0: log("ACIK hortum #%d %s %s L %d · 150 disi acik %d" % r)
if not kuru:
    Y.yaz(g); g.kaydet(sys.argv[2])
    json.dump(PARCA, open(os.path.join(HERE, "a4_parca.json"), "w"), indent=0)
    open(os.path.join(HERE, "a4_log.txt"), "w", encoding="utf-8").write("\n".join(LOG))
    print("yazildi", sys.argv[2])
