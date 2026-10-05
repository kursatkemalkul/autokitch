# -*- coding: utf-8 -*-
"""m8t2: 4 havada kelepçe durumu (v8y): bileşen kutusu + 6 yöndeki en yakın yapı yüzü"""
import sys, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from m8kit import Glb, Yuzey, bosluk
g = Glb(sys.argv[1])
YS = Yuzey(g)
KEL = [("ELK_QR_KABLO__celik", (4956.0, 1960.0, 783.0)), ("ELK_QR_KABLO__celik", (4955.2, 1960.0, 797.0)),
       ("ELK_K__celik", (4193.0, 1110.0, -39.1)), ("ELK_K__celik", (4374.0, 1189.0, -727.6))]
for d, q in KEL:
    try:
        b = g.bul_nokta(d, q, tol=0.5)
    except KeyError as e:
        print("yok", d, q); continue
    print(d, q, "kutu", b["lo"].round(1), b["hi"].round(1))
    R = bosluk(g, YS, b["lo"], b["hi"], d, maxd=200.0, n=3, yapi=True)
    print("   yapı:", [(round(t, 1), "xyz"[ax], sg) for t, ax, sg in R[:6]])
    R2 = bosluk(g, YS, b["lo"], b["hi"], d, maxd=200.0, n=3, yapi=False)
    print("   her şey:", [(round(t, 1), "xyz"[ax], sg) for t, ax, sg in R2[:6]])
