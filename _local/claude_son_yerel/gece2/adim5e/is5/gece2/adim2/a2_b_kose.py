# -*- coding: utf-8 -*-
"""GECE2 ADIM 2 · D: B cekmece kablo kanali koseleri. Yan (yassi, z boyunca) kanal z -758'de, arka kanal x = ray+10'da bitiyordu;
aradaki 17,6 x 30 mm (ust sirada 71,6) kose acikti. Engel: ray arka L flansi (x 808,6-814,9 · y 269,5-277,6, z -790'a kadar).
1) L flans yalniz kose bolgesinde z -788 -> -756 kisalir (ray govdesi, arka montaj plakasi, motor plakasi DEGISMEZ); plaka ust kenari kapanir.
2) kose parcasi: 304 1,2 mm kapakli, yan kanalin altindan arka kanalin basina (x boyunca), arka montaj plakasinin onunde (z -788 ...);
   ust yuzde yan kanal agzi, arka kanala bakan ucta kanal kesiti kadar agiz + kademe kapatma cercevesi; sol uc kapali.
   Ust sira (y 684-715): motor plakasinin (y <= 684,5) ustunden; K2 sutununda ana kablo kanalinin (y >= 703, z <= -765) ustunde cep.
python a2_b_kose.py giris.glb cikis.glb"""
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.dirname(os.path.dirname(HERE))
for q in (os.path.join(S, "elk5"), os.path.join(S, "elk2"), os.path.join(S, "gece"), S): sys.path.insert(0, q)
from m8kit import Glb, kutu_ucgen
from elib import Yeni, plaka, KAT as KATD
from ortam_sat import tri_kutu

t = 1.2
g = Glb(sys.argv[1]); LOG = []
def log(*a): s = " ".join(str(x) for x in a); LOG.append(s); print(s, flush=True)
MEKL = [m["kod"] for m in g.J["scenes"][0]["extras"]["mekanizmalar"]]
MB = MEKL.index("B/Elektrik")
MAL_KANAL = ("ME2_kanal", (0.70, 0.72, 0.74, 1.0), 0.8, 0.35)

# mevcut B ic kanallari (bilesen kutulari)
KB = []
for p in g.dprims("ELK_IC__kanal"):
    if p.get("gizli"): continue
    tl, kut = g.komp(p)
    mk = np.full(len(p["T"]), -1); L = p["pr"]["extras"]["mek"]
    for k in range(0, len(L) - 2, 3): mk[L[k + 1] // 3:(L[k + 1] + L[k + 2]) // 3] = L[k]
    for i, (lo, hi, n) in kut.items():
        tri = np.where(tl == i)[0]
        if n > 20 and mk[tri[0]] == MB: KB.append((lo, hi))
yan = [b for b in KB if b[1][2] - b[0][2] > 600 and b[1][0] - b[0][0] < 12]
arka = [b for b in KB if b[1][0] - b[0][0] > 100 and abs(b[0][2] + 790) < 0.5 and abs(b[1][2] + 760) < 0.5]
KOSE = []
for ylo, yhi in yan:
    c = [a for a in arka if 0 < a[0][0] - yhi[0] < 80 and a[0][1] < yhi[1] and a[1][1] > ylo[1] - 15]
    assert c, (ylo, yhi)
    a = min(c, key=lambda a: abs(a[0][1] - ylo[1])); KOSE.append((ylo, yhi, a[0], a[1]))
log("kose sayisi", len(KOSE))

# tum model ucgenleri (engel denetimi)
PP, AD = [], []
for p in g.prims:
    if p.get("gizli"): continue
    vis = g.gorunur(p); P = p["X"][p["T"][vis]]
    PP.append(P); AD += [p["name"]] * len(P)
PP = np.concatenate(PP); AD = np.array(AD); TLO = PP.min(1); THI = PP.max(1)
def engel(lo, hi, haric=r"^ELK_DOLAP__kablo"):
    import re
    lo = np.asarray(lo, float); hi = np.asarray(hi, float)
    m = np.all(THI > lo + 0.05, 1) & np.all(TLO < hi - 0.05, 1); i = np.where(m)[0]
    i = i[tri_kutu(PP[i], lo + 0.05, hi - 0.05)]
    return sorted(set(a for a in AD[i] if not re.search(haric, a)))

Y = Yeni(); PARCA = []; ZB = -788.0; ZT = -756.8
for ylo, yhi, alo, ahi in KOSE:
    c = round(float(ylo[0] + 7.6), 1)                   # bs.py: yan kanal x c-7.6 .. c+2.1
    x0, x1 = float(ylo[0]), float(alo[0])
    ust = alo[1] > 680
    # --- 1) ray L flansi (kose bolgesinde) -> z -756
    fx0, fx1 = c + 2.3, c + 8.6                          # 808,6 .. 814,9 (c = 806,3)
    ray = None
    for p in g.prims:
        if p.get("gizli") or not p["name"].startswith("CEK_") or not p["name"].endswith("__celik"): continue
        P = p["X"][p["T"]]; lo = P.min(1); hi = P.max(1); vis = g.gorunur(p)
        yL = (ylo[1] + yhi[1]) / 2
        m = vis & (lo[:, 0] >= fx0 - 0.15) & (hi[:, 0] <= fx1 + 0.15) & (lo[:, 2] < -700) & (hi[:, 2] > -800) & (hi[:, 1] <= yL + 6.2)             & ((lo[:, 1] >= yL - 2.3) | ((lo[:, 1] >= yL - 5) & (hi[:, 2] > -787.9)))
        if not m.any(): continue
        Q = P[m]; yl, yh = Q[..., 1].min(), Q[..., 1].max()
        ray = (p, np.where(m)[0], yl, yh); break
    assert ray, ("flans yok", c, ylo)
    p, tri, yl, yh = ray
    et = g._etiketler(p, int(tri[0]))
    def kirp(Q):
        Q = Q.copy(); z = Q[..., 2]; z[z < -700] = -756.0; return Q
    g.donustur(dict(parca=[(p, tri)]), kirp)
    # arka plakanin flans altinda kalan ust kenari / ust yuzu: kapatma kutusu (plaka 2 mm, z -790..-788)
    yama = kutu_ucgen((fx0, yl, -790.0), (fx1, min(yh, yl + 2.0), -788.0))
    g._ekle_dunya(p, yama, *et)
    log("ray flansi %s x %.1f-%.1f y %.1f-%.1f: z -788 -> -756 (ucgen %d) + plaka ust kenari kapatma" % (p["name"], fx0, fx1, yl, yh, len(tri)))
    # --- 2) kose parcasi
    ya = float(min(ylo[1], alo[1])); yb = float(max(yhi[1], ahi[1]))
    if ust: ya = max(ya, 684.6)
    cep = None
    if ust and x1 > 989.5:                               # ana B kablo kanali x 988,5-4032,5 · y 703-728 · z -790..-765 (dolu kutu)
        cep = (702.8, yb); yb = 702.8                    # ana kablo kanali (y>=703, z<=-765) ustte cep
    yi0, yi1 = ylo[1] + t, yhi[1] - t; xi0, xi1 = ylo[0] + t, yhi[0] - t      # yan kanal ic kesiti
    G = []
    # x boyunca kanal: tabani (z -788), ustu (z -758, yan kanal agzi), on/arka (y) duvarlar, sol uc kapali
    G.append(plaka(2, ZB, ZB + t, x0, x1, ya, yb))
    ust_d = [(ylo[0], yhi[0], max(ylo[1], ya), min(yhi[1], yb))]
    mk_ = (AD == "ELK_DOLAP__kablo_sinyal") & (TLO[:, 2] < ZT - t / 2) & (THI[:, 2] > ZT - t / 2) & (TLO[:, 0] > yhi[0]) & (THI[:, 0] < x1) & (TLO[:, 1] > ya) & (THI[:, 1] < yb)
    if mk_.any():
        Qk = PP[mk_].reshape(-1, 3); ust_d.append((Qk[:, 0].min() - 0.6, Qk[:, 0].max() + 0.6, Qk[:, 1].min() - 0.6, Qk[:, 1].max() + 0.6))
        log("  ust plakada sensor kablosu gecis deligi", np.round(ust_d[-1], 1).tolist())
    G.append(plaka(2, ZT - t, ZT, x0, x1, ya, yb, ust_d))      # yan kanal dis izi kadar agiz (yan kanal cidarlari z -758'de oturur)
    dy = [(x0 + t, min(x0 + 9.7 - t, x1), -763.6, ZT - t)] if cep else []
    G.append(plaka(1, ya, ya + t, x0, x1, ZB + t, ZT - t))
    G.append(plaka(1, yb - t, yb, x0, x1, ZB + t, ZT - t, dy))
    G.append(plaka(0, x0, x0 + t, ya + t, yb - t, ZB + t, ZT - t))
    # arka kanala bakan uc: arka kanal ic kesiti kadar agiz, kalan kademe cerceve
    ai = (max(alo[1] + t, ya + t), min(ahi[1] - t, yb - t), max(alo[2] + t, ZB + t), min(ahi[2] - t, ZT - t))
    G.append(plaka(0, x1 - t, x1, ya + t, yb - t, ZB + t, ZT - t, [ai]))
    # arka kanal tarafinda kose kesitinin disinda kalan kademe (arka kanal tabani -790 .. -788)
    G.append(plaka(0, x1, x1 + t, alo[1] + t, ahi[1] - t, alo[2] + t, ZB + t))
    if cep:
        c0, c1 = cep
        G.append(plaka(2, -764.8, -764.8 + t, x0, x0 + 9.7, c0, c1))
        G.append(plaka(2, ZT - t, ZT, x0, x0 + 9.7, c0, c1, [(ylo[0], yhi[0], c0, yhi[1])]))
        G.append(plaka(1, c1 - t, c1, x0, x0 + 9.7, -764.8 + t, ZT - t))
        G.append(plaka(0, x0, x0 + t, c0, c1 - t, -764.8 + t, ZT - t))
        G.append(plaka(0, x0 + 9.7 - t, x0 + 9.7, c0, c1 - t, -764.8 + t, ZT - t))
    Gk = np.concatenate([q for q in G if len(q)])
    e = engel((x0, ya, ZB), (x1 + t, yb, ZT))
    e2 = engel((x0, cep[0], -764.8), (x0 + 9.7, cep[1], ZT)) if cep else []
    Y.ekle("ELK_IC__kanal", MAL_KANAL, Gk, KATD["ELEKTRIK"], MB)
    PARCA.append(dict(ad="ic_kanal_B_kose_%d_%d" % (round(c), round(ya)), lo=[x0, ya, ZB], hi=[x1 + t, max(yb, cep[1] if cep else yb), ZT]))
    log("kose x %.1f-%.1f y %.1f-%.1f z %.0f..%.0f%s · engel %s %s" % (x0, x1, ya, yb, ZB, ZT, " + cep y %.1f-%.1f" % cep if cep else "", e, e2))
Y.yaz(g)
g.kaydet(sys.argv[2])
json.dump(PARCA, open(os.path.join(HERE, "a2_parca.json"), "w"), indent=0)
open(os.path.join(HERE, "a2_log.txt"), "w", encoding="utf-8").write("\n".join(LOG))
print("yazildi", sys.argv[2])
