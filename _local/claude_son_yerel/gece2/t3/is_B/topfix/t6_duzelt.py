# -*- coding: utf-8 -*-
"""TOPFIX 6 · denetim duzeltmeleri. python t6_duzelt.py giris.glb cikis.glb
 - valf adasi kablo kelepcesinin dili eski evaporator ayagina (y 1350-1383) yaslaniyordu -> ayak kalkti, dil y 1380 -> 1383 (alt kasetin taban sacina)"""
import sys, numpy as np
from tlib import *
gi, go = sys.argv[1:3]
G = Glb(gi)
n = 0
for p, m in tri_kutu(G, "ELK_TOPPING__celik", (2196.6, 2206.8, 1302.9, 1380.1, -733.5, -731.8)):
    vs = np.unique(p["T"][m].reshape(-1)); s = vs[p["X"][vs, 1] > 1379.9]; p["X"][s, 1] = 1383.0; p["degX"] = True; n += len(s)
log("kelepce dili y 1380 -> 1383:", n, "kose")
# t1'de gergi kasnagi iki kutuya birden girdigi icin iki kez tasinan 2 ucgen (gergi civatasi yuzu, x -647) -> yerine (+1502,3)
tasi_tri(G, "TOPPING_MODUL__celik", (-648.0, -644.0, 936.8, 937.2, -377.1, -365.9), lambda V: V + np.array([2378.4 - 876.1, 0, 0]), not_="gergi civatasi yuzu (cift tasima duzeltmesi)")
# tabla ray teknesinin arka duvarindaki motor centigi (x 842-910, A ucu) -> motorun yeni yeri (2344,3-2412,3); A ucundaki centik kapanir
n = 0
for p, m in tri_kutu(G, "TOPPING_MODUL__sac", (835.9, 2495.1, 893.4, 923.6, -415.1, -4.9)):
    vs = np.unique(p["T"][m].reshape(-1)); X = p["X"]
    for a, b in ((842.0, 2344.3), (910.0, 2412.3)):
        s = vs[np.abs(X[vs, 0] - a) < 0.05]; X[s, 0] = b; n += len(s)
    p["degX"] = True
log("ray teknesi motor centigi 842-910 -> 2344,3-2412,3:", n, "kose")
kaydet(G, go)
