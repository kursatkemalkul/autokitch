# -*- coding: utf-8 -*-
"""Kalem 2 havada: python d2_havada.py   (DENETIM_GLB ile başka GLB; varsayılan gece2/adim8/hat3_v9h.glb)
bileşenler (govde_denetim_dogru.bilesenler) → temas grafiği: iki bileşenin ÜÇGEN kutuları ≤ 0,6 mm (kaba ama hızlı; eğik büyük üçgende temas fazla sayılabilir)
→ union-find; zemin = lo_y ≤ 1 mm olan bileşenler; zemine bağlanmayan gruplar listelenir. ROBOT/INSAN/ZEMIN hariç."""
import os, sys, json, time, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "cak"))
import c8a_ortak as M
E = 0.6
t0 = time.time()
J, B, _ = M.tum_bilesenler(False)
n = len(B); print(n, "bileşen", "%.0f s" % (time.time() - t0), flush=True)
TLO = [b.P.min(1) for b in B]; THI = [b.P.max(1) for b in B]
par = list(range(n))
def kok(i):
    while par[i] != i: par[i] = par[par[i]]; i = par[i]
    return i
def temas(i, j):
    A, Bb = B[i], B[j]
    lo = np.maximum(A.lo, Bb.lo) - E; hi = np.minimum(A.hi, Bb.hi) + E
    ma = ((THI[i] >= lo) & (TLO[i] <= hi)).all(1); mb = ((THI[j] >= lo) & (TLO[j] <= hi)).all(1)
    if not ma.any() or not mb.any(): return False
    al, ah = TLO[i][ma], THI[i][ma]; bl, bh = TLO[j][mb], THI[j][mb]
    if len(al) > len(bl): al, ah, bl, bh = bl, bh, al, ah
    CH = max(1, int(4e6 // max(len(bl), 1)))
    for s in range(0, len(al), CH):
        if ((al[s:s + CH, None] <= bh[None] + E) & (ah[s:s + CH, None] >= bl[None] - E)).all(2).any(): return True
    return False
P = M.adaylar(B, pay=E); print(len(P), "aday çift", "%.0f s" % (time.time() - t0), flush=True)
test = 0
for i, j in P:
    ri, rj = kok(i), kok(j)
    if ri == rj: continue
    test += 1
    if temas(i, j): par[ri] = rj
print(test, "temas testi", "%.0f s" % (time.time() - t0), flush=True)
zem = set(kok(i) for i, b in enumerate(B) if b.lo[1] <= 1.0)
from collections import defaultdict
G = defaultdict(list)
for i in range(n):
    r = kok(i)
    if r not in zem: G[r].append(i)
meta = None
try: meta = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cak", "meta.json"), encoding="utf-8"))["bil"]
except Exception: pass
def ad(i): return "%s[%d] %s" % (B[i].dugum, B[i].no, (meta[i]["ad"] if meta and i < len(meta) and meta[i]["dugum"] == B[i].dugum else "") or "")
out = []
for r, L in sorted(G.items(), key=lambda kv: -len(kv[1])):
    lo = np.min([B[i].lo for i in L], 0); hi = np.max([B[i].hi for i in L], 0)
    out.append(dict(adet=len(L), kutu=np.round(np.r_[lo, hi], 1).tolist(), parca=[ad(i) for i in L[:12]]))
print("HAVADA GRUP", len(out), "· bileşen", sum(o["adet"] for o in out))
for o in out[:80]: print("  %3d bileşen kutu %s · %s" % (o["adet"], o["kutu"], "; ".join(o["parca"][:4])))
json.dump(out, open(os.environ.get("HAVADA_CIKTI", "havada.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
sys.stdout.flush(); os._exit(0)
