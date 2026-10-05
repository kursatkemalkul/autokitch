# -*- coding: utf-8 -*-
"""menu7 havada denetimi (yerel): tabana göre DEĞİŞEN / YENİ her TOPPING bileşeni (govde_denetim_dogru ile aynı bileşen + özet) için
başka bir bileşenle temas (üçgen kutuları ≤ 0,6 mm — d2_havada.py ölçütü) var mı; sonra bu bileşenler + temaslarından oluşan grup
değişmeyen (taban) bir bileşene bağlanıyor mu (bağlanmayan grup = havada)."""
import os, sys, numpy as np
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
sys.path.insert(0, S)
import govde_denetim_dogru as G
E = 0.6
yeni, taban = sys.argv[1:3]
ON = ("TOPPING_", "ELK_TOPPING", "HAVA_IC", "ELK_IC", "ELK_ZINCIR")
TUM = G.yukle_bilesen(G.glb_oku(yeni))
eski = {(b.dugum, b.ozet) for b in G.yukle_bilesen(G.glb_oku(taban), ON)}
deg = [i for i, b in enumerate(TUM) if G.eslesir(b.dugum, ON) and (b.dugum, b.ozet) not in eski]
LO = np.array([b.lo for b in TUM]); HI = np.array([b.hi for b in TUM])
def temas(i, j):
    A, B = TUM[i], TUM[j]; lo = np.maximum(A.lo, B.lo) - E; hi = np.minimum(A.hi, B.hi) + E
    a = A.P[((A.P.max(1) >= lo) & (A.P.min(1) <= hi)).all(1)]; b = B.P[((B.P.max(1) >= lo) & (B.P.min(1) <= hi)).all(1)]
    if not len(a) or not len(b): return False
    al, ah, bl, bh = a.min(1), a.max(1), b.min(1), b.max(1)
    for s in range(0, len(al), 2000):
        if ((al[s:s + 2000, None] <= bh[None] + E) & (ah[s:s + 2000, None] >= bl[None] - E)).all(2).any(): return True
    return False
degs = set(deg); par = {i: i for i in deg}
def kok(i):
    while par[i] != i: i = par[i]
    return i
bagli = set(); komsusuz = []
for i in deg:
    m = ((LO <= HI[i] + E) & (HI >= LO[i] - E)).all(1); m[i] = False; n = 0
    for j in np.where(m)[0]:
        if not temas(i, j): continue
        n += 1
        if j in degs: par[kok(i)] = kok(j)
        else: bagli.add(i)
    if n == 0: komsusuz.append(TUM[i].ad)
gruplar = {}
for i in deg: gruplar.setdefault(kok(i), []).append(i)
havada = [[TUM[i].ad for i in L] for L in gruplar.values() if not any(i in bagli for i in L)]
print("değişen / yeni bileşen", len(deg), "· hiç temassız", len(komsusuz), komsusuz[:20])
print("HAVADA GRUP", len(havada))
for L in havada: print("  ", len(L), L[:10])
