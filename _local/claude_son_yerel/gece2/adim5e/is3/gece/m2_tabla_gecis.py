# -*- coding: utf-8 -*-
"""MADDE 2 (88.png) · TOPPING sag duvari (x 2498,5–2500) tabla gecis boslugu F duvarindaki karsi bosluga ESITLENIR.
ESKI: TOPPING boslugu y 893,5–1042 · z −510…+5 (515 × 148,5 — arkaya, sabit tahrik motoruna dogru 169 mm fazla, alta 71,5 mm fazla)
      F boslugu (F_TP10_GOVDE sol duvari) y 965–1042 · z −341…−10 (331 × 77) — tabla Ø302 (z −321…−19) + yukleme bandi buradan gecer.
YENI: iki bosluk AYNI: y 965–1042 · z −341…−10. Duvar yuzlerindeki 4 bosluk kosesi (iki yuz + kenar yuzleri) yeni koselere tasinir
      (ucgen donmesi denetlenir) → duvar yeniden orulmeden bosluk kuculur.
CONTA (TOPPING_MODUL__silikon, ic yuzde x 2492–2498,5): eski 417 × 87 cerceve silinir, yeni bosluk cevresine 8 mm kenarli cerceve:
      dis y 957–1050 · z −349…−2, ic = bosluk.
Kullanim: python m2_tabla_gecis.py giris.glb cikis.glb"""
import sys, numpy as np
import cadquery as cq
sys.path.insert(0, r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\gece2\adim5e\is3\gece")
import glbkit

gi, go = sys.argv[1:3]
G = glbkit.Glb(gi)
ESKI = {(893.5, -510.0): (965.0, -341.0), (893.5, 5.0): (965.0, -10.0), (1042.0, -510.0): (1042.0, -341.0), (1042.0, 5.0): (1042.0, -10.0)}

p = G.bul("TOPPING_MODUL__sac"); X = p["X"]; T = p["T"]; tl, kut = G.komp(p)
v0 = np.argmin(np.linalg.norm(X - [2500, 893.5, -510], axis=1)); ci = tl[np.where((T == v0).any(1))[0][0]]
duvar = np.zeros(len(X), bool); duvar[np.unique(T[(tl == ci) & G.gorunur(p)].reshape(-1))] = True
vis = G.gorunur(p)
ilgili = np.zeros(len(T), bool)
n_old = np.cross(X[T[:, 1]] - X[T[:, 0]], X[T[:, 2]] - X[T[:, 0]])
tasinan = 0
for (y, z), (y2, z2) in ESKI.items():
    sec = duvar & (np.abs(X[:, 1] - y) < 0.02) & (np.abs(X[:, 2] - z) < 0.02) & ((np.abs(X[:, 0] - 2500) < 0.02) | (np.abs(X[:, 0] - 2498.5) < 0.02))
    ilgili |= np.isin(T, np.where(sec)[0]).any(1)
    X[sec, 1] = y2; X[sec, 2] = z2; tasinan += int(sec.sum())
p["degX"] = True
n_new = np.cross(X[T[:, 1]] - X[T[:, 0]], X[T[:, 2]] - X[T[:, 0]])
m = ilgili & vis
flip = (np.einsum("ij,ij->i", n_old[m], n_new[m]) <= 0).sum()
print("  duvar kosesi tasindi: %d kose · etkilenen ucgen %d · donen ucgen %d" % (tasinan, m.sum(), flip))
assert flip == 0, "ucgen dondu — yontem uygun degil"

# conta
p = G.bul("TOPPING_MODUL__silikon"); tl, kut = G.komp(p)
eski = [i for i, (a, b, n) in kut.items() if a[0] >= 2491.9 and b[0] <= 2498.6 and a[1] >= 954.9 and b[1] <= 1042.1 and a[2] >= -417.1 and b[2] <= 0.1]
print("  eski conta bilesen", len(eski), "ucgen", G.sil(p, np.isin(tl, eski)))
dis = cq.Solid.makeBox(6.5, 1050 - 957, -2 - (-349), cq.Vector(2492.0, 957.0, -349.0))
ic = cq.Solid.makeBox(8.5, 1042 - 965, -10 - (-341), cq.Vector(2491.0, 965.0, -341.0))
Xn, Tn = G.ag([dis.cut(ic)])
print("  yeni conta ucgen", G.ekle(p, Xn, Tn))
G.kaydet(go); print("yazildi", go)
