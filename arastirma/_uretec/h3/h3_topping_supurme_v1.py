# -*- coding: utf-8 -*-
"""TOPPING v2 · X SÜPÜRMESİ: tabla arabası + bantlı kaset (TC hareketli parçaları) sol sert duruştan sağ sert duruşa (dünya 112,5 … 2375,4)
her 5 mm'de sabit parçalara (TC + TU, montajın düşürdükleri hariç) değmemeli. Aday çiftler bbox'ın x boyunca süpürülmesiyle seçilir."""
import os, sys, time
H2 = os.path.dirname(os.path.abspath(__file__)); U = os.path.dirname(H2)
for _p in (U, H2):
    if _p not in sys.path: sys.path.insert(0, _p)
import cadquery as cq
import h3_topping_v1 as T
import h3_topping_denetim_v1 as D

V = cq.Vector
TC, TU = T.kur()
HAR = [(p["ad"], p["sh"]) for p in TC if T.TC0.x_hareketli(p["ad"])]
SAB = [("TC:" + p["ad"], p["sh"]) for p in TC if not T.TC0.x_hareketli(p["ad"])]
SAB += [("TU:" + q["ad"], q["sh"]) for q in TU if not q["ad"].startswith(T.TU_YERINDE)]
XC0 = T.TC0.XC_TABLA + T.DXW + T.DXL                    # çizildiği yer (park) 857,5
X_L, X_R = T.TC0.X_SERT[0] + T.DXW + T.DXL, T.TC0.X_SERT[1] + T.DXW
print("hareketli %d · sabit %d · park %.1f · süpürme %.1f … %.1f" % (len(HAR), len(SAB), XC0, X_L, X_R))
bul = []; aday = 0; t0 = time.time()
SB = [(a, s, D._bb(s)) for a, s in SAB]
for a, s in HAR:
    b = D._bb(s)
    dx0, dx1 = X_L - XC0, X_R - XC0
    for c, t, bb in SB:
        if not (b[2] < bb[3] - 0.01 and bb[2] < b[3] - 0.01 and b[4] < bb[5] - 0.01 and bb[4] < b[5] - 0.01): continue
        lo = max(dx0, bb[0] - b[1]); hi = min(dx1, bb[1] - b[0])     # bbox'ların x'te üst üste geldiği öteleme aralığı
        if lo >= hi: continue
        aday += 1
        n = max(2, int((hi - lo) / 5.0) + 1)
        for i in range(n):
            dx = lo + (hi - lo) * i / (n - 1)
            v = D._hacim(s.translate(V(dx, 0, 0)), t)
            if v > 1.0 or v < 0:
                bul.append((a, c, round(dx + XC0, 1), round(v, 1))); break
print("aday çift %d · bulgu %d · %.0f sn" % (aday, len(bul), time.time() - t0))
for r in bul: print("   ", r)
import json
json.dump(dict(bulgu=bul, aday=aday, hareketli=len(HAR), sabit=len(SAB), x=(X_L, X_R)), open(os.path.join(H2, "_supurme_topping_v1.json"), "w", encoding="utf-8"), ensure_ascii=False)
sys.stdout.flush(); os._exit(0)
