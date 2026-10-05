# -*- coding: utf-8 -*-
"""Kalanlar 3 · KD3 kanali ust yuzundeki 4 bos kablo giris deligi (O8, eski kaset motor kablolari, x 1482/1515/1548/1581, z -782)
-> kor tapa (delik dolgu O8 x 1,5 + ust yuzde O12 x 2 mm baslik), KD3 kanalinin etiketiyle. python t3_tapa.py giris.glb cikis.glb"""
import sys
from qlib import *
gi, go = sys.argv[1:3]
G = m8kit.Glb(gi)
p = prim(G, "ELK_TOPPING__kanal")
P = p["X"][p["T"]]; c = P.mean(1)
t0 = int(np.where(G.gorunur(p) & (np.abs(c[:, 1] - 1269.25) < 1.0) & (np.abs(c[:, 0] - 1482) < 6) & (np.abs(c[:, 2] + 782) < 6))[0][0])
et = G._etiketler(p, t0); print("etiket", et)
Pw = []
for x in (1482.0, 1515.0, 1548.0, 1581.0):
    Pw.append(silindir_ucgen((x, 1268.5, -782.0), (x, 1270.0, -782.0), 4.0, 24))
    Pw.append(silindir_ucgen((x, 1270.0, -782.0), (x, 1272.0, -782.0), 6.0, 24))
n = ekle(G, "ELK_TOPPING__rakor", np.concatenate(Pw), et); print("kor tapa 4 · ucgen", n)
G.kaydet(go); print("yazildi", go)
