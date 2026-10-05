# -*- coding: utf-8 -*-
"""TP4 · TOPPING TABLA (st_tahrik_motoru, 56 kare step) CIVATALARI.
Motor STEP agi incelendi: 4 kose (A deseni, eksen motor merkezinden +-24,9 / +-15,7) on flansta M3 civata BASI (z -431,7..-429,1, ag icinde)
ve arka kapakta disli delik/somun yuvasi (z -504,6..-501,6) var; aradaki govde kose oluklari r 3,15 (civatanin gectigi kanal).
Eski pimler O3,1 ve -493,2..-431,7 -> arka kapaga 8,4 mm bosluk (havada), ust ucu basla 0,0 ust uste.
B deseni (+-15,7 / +-24,9) 4 pim: flans ve arka kapakta hicbir delik/bas YOK (yalniz govde olugu) -> baglanti elemani degil, STEP artigi -> silinir.
Duzeltme: A deseni = M3 civata govdesi O3,0, delik eksenine (bas halkasinin cember uydurmasi) MERKEZLI, bas altindan (-431,7) arka kapaga (-501,65) kadar:
basa ve arka kapaga oturur, flansa girmez. python tp4_motor.py giris.glb cikis.glb"""
import os, sys, numpy as np
TPD = os.path.dirname(os.path.abspath(__file__)); S = os.path.dirname(TPD)
gi, go = [os.path.abspath(a) for a in sys.argv[1:3]]
sys.path.insert(0, os.path.join(S, "topfix")); sys.path.insert(0, TPD)
from tlib import *
from m8kit import silindir_ucgen
G = Glb(gi)
MOT = (2437.7, 2494.0, 958.9, 1016.1, -504.7, -408.5)
A = [(2439.3, 2442.6, 970.6, 974.0), (2439.3, 2442.6, 1002.0, 1005.4), (2489.0, 2492.4, 1002.0, 1005.4), (2489.0, 2492.4, 970.6, 974.0)]
B = [(2448.5, 2451.8, 961.4, 964.8), (2448.5, 2451.8, 1011.2, 1014.6), (2479.9, 2483.2, 961.4, 964.8), (2479.9, 2483.2, 1011.2, 1014.6)]
V = np.concatenate([p["X"][p["T"][m]].reshape(-1, 3) for p, m in tri_kutu(G, "TOPPING_MODUL__motor", MOT, e=0.2)])


def cember(c0):
    """bas halkasi (z -431,7, r 2-3) koselerine en kucuk kareler cember uydurma"""
    r = np.hypot(V[:, 0] - c0[0], V[:, 1] - c0[1]); k = (np.abs(V[:, 2] + 431.7) < 0.15) & (r > 2.0) & (r < 3.0)
    Q = np.unique(np.round(V[k, :2], 3), axis=0)
    M = np.c_[2 * Q, np.ones(len(Q))]; sol = np.linalg.lstsq(M, (Q ** 2).sum(1), rcond=None)[0]
    c = sol[:2]; R = np.sqrt(sol[2] + c @ c); return c, R, len(Q)


for x0, x1, y0, y1 in A:
    L = tri_kutu(G, "TOPPING_MODUL__motor", (x0, x1, y0, y1, -493.3, -431.6), e=0.05)
    et = etiket(G, L[0][0], L[0][1]); n = sum(G.sil(p, m) for p, m in L)
    c0 = np.array([(x0 + x1) / 2, (y0 + y1) / 2]); c, R, nq = cember(c0)
    ekle_ucgen(G, "TOPPING_MODUL__motor", silindir_ucgen((c[0], c[1], -501.65), (c[0], c[1], -431.7), 1.5, 24), *et)
    log("M3 CIVATA eksen %s (eski pim ekseni %s, fark %.3f mm; bas halkasi r %.2f, %d nokta) · O3,0 z -501,65..-431,7 · %d ucgen silindi" % (c.round(3), c0.round(2), np.linalg.norm(c - c0), R, nq, n))
for x0, x1, y0, y1 in B:
    n = sum(G.sil(p, m) for p, m in tri_kutu(G, "TOPPING_MODUL__motor", (x0, x1, y0, y1, -493.3, -440.0), e=0.05))
    log("SIL hayalet pim (B deseni, flans/kapakta delik yok) %s %d ucgen" % ([x0, y0], n))
kaydet(G, go)
sys.stdout.flush(); os._exit(0)
