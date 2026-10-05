# -*- coding: utf-8 -*-
"""TOPFIX 5 · BAGLILAR: 8 pnomatik hortum (valf adasi -> 4 UNO silindiri, yeni x) · KD3 kanali + 4 kaset motor kablosu (yeni motor x)
· x sifir sensoru rayin TOPPING ucuna (x 2345, sag limitin 30 mm solu) + kablosu sag duvar demetine -> KD1 · X ekseni motoru kablosu
(motor TOPPING ucunda) -> KD1. A'nin icinde kablo YOK. python t5_bagli.py giris.glb cikis.glb"""
import os, sys, json, pickle, numpy as np
from tlib import *
import tgeo as TG
Kb, S_, kes, tekle, bb, boru = TG.kutu, TG.silindir, TG.kes, TG.tekle, TG._bb, TG.boru
gi, go = sys.argv[1:3]
G = Glb(gi)
ETK = json.load(open("t1_etiket.json"))
HK = ETK["hortum"]; KD = ETK["kd3"]; MK = ETK["motor_kablo"]; AK = ETK["a_kablo"]
# ---------------- 1 · pnomatik hortumlar (O6, r 3) — portlar silindir ust yuzunde: on z -688, arka z -795 (eksen -3 / +3 ... m8_fix_3 ile ayni duzen)
H = {
    "kusbasi_on": [(1843.5, 1250, -688), (1843.5, 1208.9, -688)],
    "kusbasi_arka": [(1853.5, 1250, -750), (1853.5, 1225, -750), (1853.5, 1225, -795), (1853.5, 1208.5, -795)],
    "kiyma_on": [(1700, 1250, -688), (1700, 1225, -688), (1591.5, 1225, -688), (1591.5, 1209.0, -688)],
    "kiyma_arka": [(1710, 1250, -750), (1710, 1225, -750), (1710, 1225, -795), (1601.5, 1225, -795), (1601.5, 1208.5, -795)],
    "harc_on": [(1690, 1275, -670), (1686, 1275, -670), (1686, 1648, -670), (1719, 1648, -670), (1719, 1648, -688), (1719, 1632.5, -688)],
    "harc_arka": [(1690, 1290, -682), (1678, 1290, -682), (1678, 1655, -682), (1725, 1655, -682), (1725, 1655, -795), (1725, 1632.4, -795)],
    "sos_on": [(1998, 1302, -670), (2297, 1302, -670), (2297, 1648, -670), (2256.5, 1648, -670), (2256.5, 1648, -688), (2256.5, 1632.5, -688)],
    "sos_arka": [(1998, 1265, -676), (2307, 1265, -676), (2307, 1655, -676), (2262.5, 1655, -676), (2262.5, 1655, -795), (2262.5, 1632.4, -795)],
}
for k, pts in H.items():
    x, y, z = pts[-1]
    ust = 1209.5 if y < 1400 else 1632.5
    pts = pts[:-1] + [(x, ust + 5.0, z)]
    ekle_ucgen(G, "TOPPING_MODUL__hava_ana", kutu_ucgen([x - 4, ust, z - 4], [x + 4, ust + 5.0, z + 4]), *HK)
    ekle_ucgen(G, "TOPPING_MODUL__hava_ana", tup(pts, 3.0, 12), *HK)
    log("hortum", k, pts[0], "->", pts[-1])
# ---------------- 2 · KD3 + kaset motor kablolari (m7c ile ayni duzen, yeni x)
xk, xs = 2088.5, 2360.5
x0, x1, y0, y1, z0, z1 = 1470.0, 2400.0, 1240.0, 1270.0, -798.0, -768.0
t = 1.5
kan = Kb(x0, x1, y0, y1, z0, z1).cut(Kb(x0 - 1, x1 + 1, y0 + t, y1 - t, z0 + t, z1 - t))
XH_K, XH_S = xk + 63.0, 2392.0
giris = [S_(4.5, (xs, 1255.0, z0 - 1), (xs, 1255.0, z0 + t + 1))]
giris += [S_(4.0, (x, y0 - 1, -782.0), (x, y0 + t + 1, -782.0)) for x in (XH_K, XH_S)]
giris += [S_(4.0, (x, y1 - t - 1, -782.0), (x, y1 + 1, -782.0)) for x in (xk, 1482.0, 1515.0, 1548.0, 1581.0)]
ekle_kati(G, "ELK_TOPPING__kanal", [kes(kan, giris)], *KD)
r = 3.0
for ad, P in (("sucuk_rotor", [(xs, 1265.5, -807.0), (xs, 1255.0, -807.0), (xs, 1255.0, z0)]),
              ("sucuk_helezon", [(xs, 1161.5, -807.0), (xs, 1150.0, -807.0), (xs, 1150.0, -782.0), (XH_S, 1150.0, -782.0), (XH_S, y0, -782.0)]),
              ("kasar_rotor", [(xk, 1296.5, -807.0), (xk, 1285.0, -807.0), (xk, 1285.0, -782.0), (xk, y1, -782.0)]),
              ("kasar_helezon", [(xk, 1141.5, -807.0), (xk, 1130.0, -807.0), (xk, 1130.0, -782.0), (XH_K, 1130.0, -782.0), (XH_K, y0, -782.0)])):
    ekle_kati(G, "ELK_TOPPING__kablo", [boru(P, r)], *MK); log("motor kablosu", ad)
# ---------------- 3 · x sifir sensoru (A ucundan -> TOPPING ucu, x 1086 -> 2345) + kablosu
SK = pickle.load(open("sensor_kopya.pkl", "rb"))
DXS = 2345.1 - 1086.1
for ad, key in (("TOPPING_MODUL__celik", "celik"), ("TOPPING_MODUL__koyu", "koyu")):
    for Pw, (kt, mk, kp) in SK[key]: ekle_ucgen(G, ad, Pw + np.array([DXS, 0, 0]), kt, mk, kp)
XS0 = 2345.1
P = [(XS0, 920.0, -18.7), (XS0, 920.0, -16.0), (XS0, 931.5, -16.0), (XS0, 931.5, 5.0), (2488.5, 931.5, 5.0), (2488.5, 1074.5, 5.0),
     (2488.5, 1074.5, -797.0), (2449.2, 1074.5, -797.0)]
ekle_kati(G, "ELK_TOPPING__kablo", [boru(P, 2.0)], *AK); log("x sifir sensoru + kablo -> KD1")
# ---------------- 4 · X ekseni motoru kablosu (motor rayin TOPPING ucunda, t1) -> teknik bolme sag perdesinin onunden -> KD1 sag yuzu
P = [(2390.4, 924.5, -462.0), (2390.4, 924.5, -470.0), (2390.4, 940.0, -470.0), (2457.0, 940.0, -470.0), (2457.0, 940.0, -805.0), (2449.2, 940.0, -805.0)]
ekle_kati(G, "ELK_TOPPING__kablo", [boru(P, 3.0)], *AK); log("X motoru kablosu -> KD1")
kaydet(G, go)
sys.stdout.flush(); os._exit(0)
