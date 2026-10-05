# -*- coding: utf-8 -*-
"""MADDE 8 · adim 6 · ayni istasyon govde saclari arasindaki <= 2 mm istenmeyen derzler (havada_pu_kapak.json k5_derz) -> ince sacin kenar yuzu
komsu saca uzatilir (kaynak/bukum birlesimi gibi temas). python m8_fix_6_derz.py giris.glb cikis.glb"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m8kit import Glb, esle
HERE = os.path.dirname(os.path.abspath(__file__))
g = Glb(sys.argv[1]); LOG = []
def log(*a): LOG.append(" ".join(str(x) for x in a)); print(*a)
D = json.load(open(os.path.join(HERE, "m8", "havada_pu_kapak.json"), encoding="utf-8"))["k5_derz"]
L = [x for x in D if x["tur"].startswith("aynı istasyon") and x["aralik_mm"] <= 2.0]
def adaylar(dugum, q, e=2.6):
    g.bilesen(dugum, 0)
    return [b for b in g._bc[dugum] if np.all(b["lo"] - e <= q) and np.all(q <= b["hi"] + e)]
IS = []; kul = set()
for x in L:
    for q in x["noktalar"]:
        q = np.array(q, float); best = None
        for A in adaylar(x["a"], q):
            for Bc in adaylar(x["b"], q):
                if A is Bc: continue
                gap = np.maximum(Bc["lo"] - A["hi"], A["lo"] - Bc["hi"])          # >0: o eksende ayrik
                ax = int(np.argmax(gap)); gv = gap[ax]
                if abs(gv - x["aralik_mm"]) > 0.35 or (np.sum(gap > 0.05) != 1): continue
                # ucu uzatilacak: gap ekseninde daha ince olan (sac kenari)
                ea = A["hi"][ax] - A["lo"][ax]; eb = Bc["hi"][ax] - Bc["lo"][ax]
                U, V = (A, Bc) if ea <= eb else (Bc, A)
                cand = (gv, ax, U, V)
                if best is None or gv < best[0]: best = cand
        if best is None: log("eslesmedi", x["a"], x["b"], q.round(1)); continue
        gv, ax, U, V = best
        ext = U["hi"] - U["lo"]; oth = [ext[i] for i in range(3) if i != ax]
        if min(oth) > 300:      # buyuk panel yuzu: uzatinca ustune oturan her sey cakisir -> elle bakilmali
            log("ATLANDI (buyuk panel yuzu)", x["a"], x["b"], q.round(0), "%.2f" % gv, "xyz"[ax], U["lo"].round(0), U["hi"].round(0)); continue
        key = (id(U), ax)
        if key in kul: continue
        kul.add(key); IS.append((x, q, gv, ax, U, V))
log("derz isleri", len(IS))
yap = {}
for x, q, gv, ax, U, V in IS:
    if U["hi"][ax] <= V["lo"][ax]: eski, yeni = U["hi"][ax], V["lo"][ax]
    else: eski, yeni = U["lo"][ax], V["hi"][ax]
    yap.setdefault(id(U), [U, []])[1].append((ax, eski, yeni))
    log("derz", x["a"], x["b"], q.round(0), "%.2f mm" % gv, "xyz"[ax], "%.2f -> %.2f" % (eski, yeni), "parca", U["lo"].round(0), U["hi"].round(0))
for U, ops in yap.values():
    def f(P, ops=ops):
        for ax, eski, yeni in ops: P = esle(P, ax, eski, yeni, tol=0.02)
        return P
    g.donustur(U, f)
g.kaydet(sys.argv[2]); log("kaydedildi", sys.argv[2])
open(os.path.splitext(sys.argv[2])[0] + "_log.txt", "w", encoding="utf-8").write("\n".join(LOG))
