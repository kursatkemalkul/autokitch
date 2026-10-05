# -*- coding: utf-8 -*-
"""python m8_occ.py k N → occ_k.json : her çakışmanın en derin noktası OCC (BRepClass3d + BRepExtrema) ile"""
import os, sys, json, time, numpy as np
import c8a_ortak as M
k, N = int(sys.argv[1]), int(sys.argv[2])
J, B, _ = M.tum_bilesenler(False)
C = json.load(open("birlesik.json"))["cak"]
out = {}
for n in range(k, len(C), N):
    r = C[n]; kap = B[r["i"]] if r["bilgi"]["yon"] == "a" else B[r["j"]]
    if len(kap.P) > 60000: out[n] = "atlandı (büyük katı %d üçgen)" % len(kap.P); continue
    out[n] = M.G.occ_dogrula(kap, np.array([r["bilgi"]["nokta"]]))
json.dump(out, open("occ_%02d.json" % k, "w"), default=float)
sys.stdout.flush(); os._exit(0)
