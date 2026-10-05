# -*- coding: utf-8 -*-
"""yeni parçaların (ent json) model içinde çakışması: python yeni_cak.py model.glb ent1.json [ent2.json ...]
her yeni parça bileşeni ↔ kutusu kesişen diğer tüm bileşenler: manifold kesişim hacmi (> 0.01 mm³ yazılır) + en yakın temas (havada denetimi: kutu 0.2 mm şişirilince değen var mı)"""
import sys, os, json, io, numpy as np
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
sys.path.insert(0, S)
import govde_denetim_dogru as G
W = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec\h3\yama_v9"
sys.path.insert(0, W)
import sac_ent as SE

D = G.glb_oku(sys.argv[1])
E = [json.load(open(f, encoding="utf-8")) for f in sys.argv[2:]]
BC = {}
def comps(d):
    if d not in BC: BC[d] = G.bilesenler(d, D[d]) if d in D else []
    return BC[d]
KUTU = {d: (D[d].reshape(-1, 3).min(0), D[d].reshape(-1, 3).max(0)) for d in D if len(D[d])}
MF = {}
def mfk(d, b):
    k = (d, b.no)
    if k not in MF: MF[k] = SE.mf_ucgen(b.P)
    return MF[k]
toplam = 0
for e in E:
    for ad, p in e["parca"].items():
        d = p["dugum"]; k = p["kutu"]; lo = np.array(k[0::2]); hi = np.array(k[1::2])
        bb = [b for b in comps(d) if np.all(b.lo >= lo - 0.6) and np.all(b.hi <= hi + 0.6)]
        if not bb: print("BULUNAMADI", ad, d); continue
        kendi = set((d, b.no) for b in bb)
        cak = []; temas = []
        for d2, (a, c) in KUTU.items():
            if np.any(c < lo - 0.5) or np.any(a > hi + 0.5): continue
            for b2 in comps(d2):
                if (d2, b2.no) in kendi: continue
                if np.any(b2.hi < lo - 0.2) or np.any(b2.lo > hi + 0.2): continue
                m2 = mfk(d2, b2)
                for b in bb:
                    if np.any(b2.hi < b.lo - 0.2) or np.any(b2.lo > b.hi + 0.2): continue
                    temas.append("%s[%d]" % (d2, b2.no))
                    m1 = mfk(d, b)
                    if m1 is None or m2 is None:
                        cak.append(("ACIK", "%s[%d]" % (d2, b2.no), -1)); continue
                    v = (m1 ^ m2).volume()
                    if v > 0.01: cak.append(("", "%s[%d]" % (d2, b2.no), v))
        toplam += len([c for c in cak if c[2] > 0.01])
        print("%-40s %-32s bileşen %d · çakışma %s · yakın %d" % (ad, d, len(bb), ", ".join("%s%s %.2f" % (f, n, v) for f, n, v in cak) or "0", len(set(temas))))
print("TOPLAM çakışma", toplam)
