# -*- coding: utf-8 -*-
"""ADIM 3 · kaset ÖNDEN ÇEKME süpürmesi: kaset (gövde + bütün iç parçaları + dönen helezon/karıştırıcı + kasetle çıkan yarık dili) +z yönünde
0 → 700 mm, 2 mm adımla öne çekilir; her adımda hareketli küme (manifold birleşimi) ∩ sabit komşular hacmi. Eşik 0,5 mm³ (temas sayılmaz).
Sabit yuva parçalarının (kılavuz, dayama, mandal) kasete DEĞMESİ beklenir → 0 → 2 mm aralığı ayrı yazılır.
python supur.py model.glb pk.json cikti.txt"""
import os, sys, json, time, numpy as np
S = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, S)
import govde_denetim_dogru as G
import manifold3d as mf
glb, pkj, cik = sys.argv[1:4]
D = G.glb_oku(glb); TUM = G.yukle_bilesen(D)
PK = json.load(open(pkj, encoding="utf-8"))["parca"]["TOPPING_MODUL"]
KAS = {"KASAR": ("kasar_cad_v14", 26.5, "KASAR", (1948.5, 2228.5)), "SUCUK": ("sucuk_cad_v8", 49.5, "SUCUK", (2290.5, 2430.5))}
out = open(cik, "w", encoding="utf-8")
def yaz(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); out.write(s + "\n"); out.flush()
for kad, (onek, dx, dn, (x0, x1)) in KAS.items():
    # hareketli: adı kaset öneki ile başlayan pk kutusuna (dx kaydırmalı) uyan bileşenler + dönen düğümler + yarık dili; motor/kovan/mil (yuva tarafı) HARİÇ
    kut = []
    for e in PK:
        a = e[0]
        if (a.startswith(onek + "__") or a == onek + "_yarik_dili"):
            kut.append((a, np.array([e[2] + dx, e[4], e[6]]), np.array([e[3] + dx, e[5], e[7]])))
    H, Hn = [], []
    for b in TUM:
        if b.dugum.startswith("TOPPING_DONER__") and b.dugum.endswith(dn):
            if b.lo[2] >= -546.0: H.append(b); Hn.append(b.dugum)          # tahrik mili / redüktör yuvada kalır
            continue
        if not b.dugum.startswith("TOPPING_MODUL__"): continue
        if not (x0 - 1 <= b.lo[0] and b.hi[0] <= x1 + 1): continue
        for a, lo, hi in kut:
            if np.all(b.lo >= lo - 0.8) and np.all(b.hi <= hi + 0.8) and np.all(b.lo <= lo + 0.8 + (hi - lo)) :
                if a.endswith(("yarik_dili", "yatak_kapagi")) or (np.abs(b.lo - lo).max() < 0.8 and np.abs(b.hi - hi).max() < 0.8) or a.endswith("cikis_tupu"):
                    H.append(b); Hn.append(a); break
    hs = set(id(b) for b in H)
    LO = np.min([b.lo for b in H], 0); HI = np.max([b.hi for b in H], 0)
    yaz("\n== %s · hareketli %d bileşen (%d adlı) · kutu %s..%s" % (kad, len(H), len(set(Hn)), np.round(LO, 1).tolist(), np.round(HI, 1).tolist()))
    kapali = [b for b in H if b.mf()]
    acik = [b.ad for b in H if not b.mf()]
    if acik: yaz("   açık ağ (birleşime girmedi):", acik)
    M = mf.Manifold.batch_boolean([b.mf() for b in kapali], mf.OpType.Add)
    # sabit komşular: süpürme kutusuna giren, hareketli olmayan kapalı bileşenler
    SLO = LO - 0.5; SHI = HI + np.array([0.5, 0.5, 700.5])
    F = [b for b in TUM if id(b) not in hs and not b.dugum.startswith(("URUN__", "INSAN", "ROBOT")) and "seffaf" not in b.dugum and "KAPAK" not in b.dugum and np.all(b.hi >= SLO) and np.all(b.lo <= SHI)]
    Fk = [b for b in F if b.mf()]
    yaz("   sabit komşu %d (kapalı %d; açık ağlar: %s)" % (len(F), len(Fk), [b.ad for b in F if not b.mf()][:12]))
    t0 = time.time(); bulgu = {}
    for dz in np.arange(0.0, 700.01, 2.0):
        Mt = M.translate([0.0, 0.0, float(dz)])
        blo = LO + [0, 0, dz] - 0.1; bhi = HI + [0, 0, dz] + 0.1
        for b in Fk:
            if np.any(b.hi < blo) or np.any(b.lo > bhi): continue
            v = (Mt ^ b.mf()).volume()
            if v > 0.5:
                r = bulgu.setdefault(b.ad, [dz, dz, 0.0]); r[1] = dz; r[2] = max(r[2], v)
    yaz("   süpürme 0 → 700 mm (2 mm adım) · %.0f s" % (time.time() - t0))
    if not bulgu: yaz("   TEMİZ — çekme yolunda hiçbir sabit parçaya girmiyor")
    for k, (a, b_, v) in sorted(bulgu.items(), key=lambda x: x[1][0]):
        yaz("   GİRİŞ %-36s dz %5.0f → %5.0f mm · en büyük ortak hacim %.1f mm³" % (k, a, b_, v))
out.close(); sys.stdout.flush(); os._exit(0)
