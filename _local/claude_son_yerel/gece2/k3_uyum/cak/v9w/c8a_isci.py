# -*- coding: utf-8 -*-
"""python m8_isci.py k N  → parca_k.json (aday çiftlerin k::N dilimi, karışık sıra)"""
import os, sys, json, time, numpy as np
import c8a_ortak as M
k, N = int(sys.argv[1]), int(sys.argv[2])
J, B, _ = M.tum_bilesenler(False)
P = M.adaylar(B)
rng = np.random.default_rng(8); o = rng.permutation(len(P))
mine = [P[i] for i in o[k::N]]
out = dict(cak=[], inc=[], temas=0, yavas=[], hata=[]); t0 = time.time()
log = open("isci_%02d.log" % k, "w", encoding="utf-8")
for n, (i, j) in enumerate(mine):
    t = time.time()
    try:
        r = M.G.cift(B[i], B[j])
    except Exception as e:
        out["hata"].append([i, j, str(e)]); continue
    dt = time.time() - t
    if dt > 20: out["yavas"].append([i, j, round(dt, 1)])
    if r is None: continue
    if r[0] == "CAKISMA": out["cak"].append(dict(i=int(i), j=int(j), d=r[1], hacim=r[2], bilgi=r[3]))
    elif r[0] == "INCELE": out["inc"].append(dict(i=int(i), j=int(j), d=r[1], hacim=r[2], bilgi=r[3]))
    else: out["temas"] += 1
    if n % 200 == 0: log.write("%d/%d %.0f s\n" % (n, len(mine), time.time() - t0)); log.flush()
json.dump(out, open("parca_%02d.json" % k, "w", encoding="utf-8"), default=float)
log.write("BITTI %.0f s\n" % (time.time() - t0)); log.close()
sys.stdout.flush(); os._exit(0)
