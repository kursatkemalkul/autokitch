# -*- coding: utf-8 -*-
"""E v13: çift karton algılayıcı ve ön dil sensörü çevresindeki parçalar (t anlarında sınır kutusu)"""
import kutu_cad_v13 as K

K.modul()
P = {p["ad"]: p for p in K.PARCALAR}
S = {n: p["wp"].val() for n, p in P.items()}
GRUPSUZ = ("PIZZA", "CATAL", "K_ITICI", "SABIT_REF")
BOLGE = {"UDC": (700, 830, 880, 1070, -470, -340), "PARMAK_SEN": (100, 160, 1290, 1350, -30, 5), "SARJOR": (0, 830, 900, 1000, -830, -380)}
ANLAR = [0.0, 1.0, 1.35, 1.65, 2.0, 2.7, 3.0, 4.3, 6.0, 7.5, 9.0, 10.0, 12.0, 15.0]
for t in ANLAR:
    W = K.blank_dunya(t)
    for n in S:
        g = P[n]["grup"]
        if g in GRUPSUZ: continue
        M = W[g] if g.startswith("B_") else K.grup_matrisi(g, t)
        b = K.uygula(S[n], M).BoundingBox()
        for ad, (x0, x1, y0, y1, z0, z1) in BOLGE.items():
            if b.xmax > x0 and b.xmin < x1 and b.ymax > y0 and b.ymin < y1 and b.zmax > z0 and b.zmin < z1:
                if ad != "SARJOR" or n.startswith(("sarjor", "asansor", "kilavuz", "karton_yig")):
                    print("t %5.2f %-10s %-10s %-40s %s" % (t, ad, g, n[:40], [round(v, 1) for v in (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)]))
