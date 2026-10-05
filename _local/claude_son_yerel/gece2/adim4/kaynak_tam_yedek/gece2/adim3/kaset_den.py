# -*- coding: utf-8 -*-
"""ADIM 3 · kaset bolgesi cakisma denetimi (govde_denetim_dogru yontemi aynen, iki yonlu + OCC).
Kume = kutusu tamamen KASET BOLGESI icinde kalan bilesenler (kasar / sucuk) · komsu = TUM model.
python kaset_den.py model.glb cikti [--taban eski.glb]  (taban verilirse yalniz degisen/yeni bilesenler kume olur)"""
import os, sys, json, time, numpy as np
S = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, S)
import govde_denetim_dogru as G
BOLGE = {"KASAR": ((1940, 1135, -550), (2236, 1515, -85)), "SUCUK": ((2284, 1135, -550), (2440, 1515, -85))}
glb, cikti = sys.argv[1], sys.argv[2]; taban = sys.argv[sys.argv.index("--taban") + 1] if "--taban" in sys.argv else None
os.makedirs(cikti, exist_ok=True); LOG = open(os.path.join(cikti, "rapor.txt"), "w", encoding="utf-8")
def yaz(*x):
    s = " ".join(str(v) for v in x); print(s, flush=True); LOG.write(s + "\n"); LOG.flush()
t0 = time.time(); D = G.glb_oku(glb); TUM = G.yukle_bilesen(D)
eski = set()
if taban: eski = {(b.dugum, b.ozet) for b in G.yukle_bilesen(G.glb_oku(taban))}
LO = np.array([b.lo for b in TUM]); HI = np.array([b.hi for b in TUM])
yaz("model %s · %d bilesen · %.0f s" % (os.path.basename(glb), len(TUM), time.time() - t0))
SON = {}
for kad, (lo, hi) in BOLGE.items():
    lo = np.array(lo, float); hi = np.array(hi, float)
    ozn = [i for i, b in enumerate(TUM) if (b.lo >= lo).all() and (b.hi <= hi).all() and not b.dugum.startswith("URUN__") and (b.dugum, b.ozet) not in eski]
    oz = set(ozn); bul, tem, inc, acik = [], [], [], []; gor = set()
    for i in ozn:
        A = TUM[i]
        if not A.kapali: acik.append(A.ad)
        m = ((LO <= A.hi + G.PAY) & (HI >= A.lo - G.PAY)).all(1); m[i] = False
        for j in np.where(m)[0]:
            if TUM[j].dugum.startswith("URUN__"): continue
            k = (min(i, j), max(i, j))
            if k in gor: continue
            gor.add(k); r = G.cift(A, TUM[j])
            if r is None: continue
            kay = dict(parca=A.ad, komsu=TUM[j].ad, tip=r[0], derinlik=r[1], hacim=None if r[2] is None else round(r[2], 3), bilgi=r[3])
            if r[0] == "CAKISMA":
                kap = A if r[3]["yon"] == "a" else TUM[j]; kay["occ"] = G.occ_dogrula(kap, np.array([r[3]["nokta"]])); bul.append(kay)
            elif r[0] == "INCELE": inc.append(kay)
            else: tem.append(kay)
    SON[kad] = dict(n=len(ozn), acik=acik, cakisma=bul, incele=inc, temas=tem)
    yaz("\n== %s · %d bilesen · acik ag %d · CAKISMA %d · INCELE %d · TEMAS %d · %.0f s" % (kad, len(ozn), len(acik), len(bul), len(inc), len(tem), time.time() - t0))
    for r in sorted(bul, key=lambda r: -r["derinlik"]):
        yaz("   CAKISMA %-34s <-> %-34s derinlik %.3f · OCC %s · hacim %s · nokta %s · yon %s" % (r["parca"], r["komsu"], r["derinlik"], r["occ"], r["hacim"], np.round(r["bilgi"]["nokta"], 1).tolist(), r["bilgi"]["yon"]))
    for r in inc: yaz("   INCELE  %s <-> %s hacim %s" % (r["parca"], r["komsu"], r["hacim"]))
json.dump(SON, open(os.path.join(cikti, "denetim.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
LOG.close(); sys.stdout.flush(); os._exit(0)
