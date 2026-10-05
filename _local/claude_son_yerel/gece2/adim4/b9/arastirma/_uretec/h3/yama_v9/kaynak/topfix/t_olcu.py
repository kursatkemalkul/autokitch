# -*- coding: utf-8 -*-
"""TOPFIX tek olcu kaynagi · iki evaporator kaseti (alt = alt bolme, ust = ust bolme) — ikisi de harc silindirinin SAGINDA, sos silindirinin SOLUNDA.
Harc silindiri grubu x 1696-1748 (braket) -> kaset 1758 (net 10) · sos braketi 2233,5-2285,5 -> kaset 2223 (net 10,5).
Kaset: dis sac 1 + PU 39 + ic sac 1 (= 41) · ic x 1799-2182: fan bolmesi 1799-1922 · ara perde 1922-1923 · serpantin 1923-2127 · perde 2127-2128 · kollektor/TXV 2128-2182."""
X0, X1 = 1758.0, 2223.0
XI0, XI1 = 1799.0, 2182.0
KASET = {"alt": (1383.0, 1604.0), "ust": (1614.0, 1835.0)}          # dis y
W = 41.0
Z0, Z1 = -826.0, -640.0                                              # dis sac / PU on yuzu (POM cerceve -640…-630)
ZI0 = -785.0                                                          # ic arka yuz
FAN_X = (1799.0, 1922.0); SER_X = (1923.0, 2127.0); KOL_X = (2128.0, 2182.0)
SER_Z = (-731.0, -646.0)                                              # serpantin derinligi 85 (eski ile ayni)


def ic(k):
    y0, y1 = KASET[k]; return y0 + W, y1 - W


KAN, PEN = [], []
for k in ("alt", "ust"):
    a, b = ic(k)
    ya, yb = (a + 4.0, 1530.0) if k == "alt" else (a + 4.0, b - 4.0)   # alt: ust raf arka bukumu (y 1534-1572) onunu kapatir -> 1530'da biter
    KAN += [(1803.0, 1918.0, ya, yb), (1927.0, 2123.0, ya, yb)]      # ufleme (fan onu) · donus (serpantin onu)
    PEN.append((1799.0, 2127.0, ya - 4.0, yb + 4.0))
AGIZ = [(x0 + 3, x1 - 3, y0 + 3, y1 - 3) for x0, x1, y0, y1 in KAN]
