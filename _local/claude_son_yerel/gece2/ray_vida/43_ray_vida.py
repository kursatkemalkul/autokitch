# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 43 · B ÇEKMECE RAY VİDALARI M5 × 10 → M5 × 6 (4 Eki 2026 · Claude · YEREL · Kemal onayı)
python 43_ray_vida.py girdi.glb cikti.glb      (zincir: hat3_v9j.glb → hat3_v9k.glb)
Kaynak: tek çekmece montaj animasyonu v1 denetimi — sabit ray (Accuride DZ3832 dış eleman) → bölme sacı bağlantısındaki DIN 7991 M5 × 10 havşa
vidanın ucu PEM SP-M5'in arkasındaki köpük kapağının tabanını 3,97 mm geçiyordu (kapağı delip PU'ya giriyordu). Kemal: "M5 × 6 yap, B'deki bütün
ray vidaları". Yöntem: B_KASA__paslanmaz düğümündeki ray vidası bileşenleri (havşa başlı, kutu 10 × 10 × 10, eksen x, baş Ø10 ray tarafında) bulunur;
vidanın UÇ düzlemindeki köşeler başa doğru 4,0 mm kaydırılır → gövde boyu 7,2 → 3,2, toplam boy (DIN 7991: baş dahil) 10 → 6. Baş, PEM, kapak, ray
deliği değişmez. Beklenen adet: h3_b_sac_v1.raylar() → 42 sabit ray × 3 = 126 vida (bulunan adet günlüğe yazılır, farklıysa durur)."""
import os, sys, time, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb

gi, go = sys.argv[1:3]
t0 = time.time()
LOG = SE.log
D = "B_KASA__paslanmaz"
KISALT = 4.0                    # mm · M5 × 10 → M5 × 6
BEKLENEN = 126

g = Glb(gi)
g.bilesen(D, 0)
L = g._bc[D]
ADAY = []
for b in L:
    ext = b["hi"] - b["lo"]
    if not (abs(ext[0] - 10.0) < 0.05 and abs(ext[1] - 10.0) < 0.1 and abs(ext[2] - 10.0) < 0.1): continue
    P = np.concatenate([p["X"][p["T"][t]] for p, t in b["parca"]]).reshape(-1, 3)
    c = (b["lo"] + b["hi"]) / 2.0
    r = np.hypot(P[:, 1] - c[1], P[:, 2] - c[2])
    x0, x1 = b["lo"][0], b["hi"][0]
    r0 = r[np.abs(P[:, 0] - x0) < 0.01].max(); r1 = r[np.abs(P[:, 0] - x1) < 0.01].max()
    if abs(max(r0, r1) - 5.0) > 0.05 or abs(min(r0, r1) - 2.45) > 0.1: continue      # baş Ø10 · gövde Ø4,9 (M5)
    uc = x0 if r0 < r1 else x1; yon = 1.0 if r0 < r1 else -1.0                         # uç düzlemi · başa doğru yön
    ADAY.append((b, uc, yon))
LOG("adım 43: %s içinde %d ray vidası (beklenen %d)" % (D, len(ADAY), BEKLENEN))
assert len(ADAY) == BEKLENEN, "ray vidası sayısı beklenenden farklı"
KAYIT = []
kutular = [(b["lo"].copy(), b["hi"].copy(), uc, yon) for b, uc, yon in ADAY]
for lo, hi, uc, yon in kutular:
    g._bc.clear(); b = g.bilesen(D, lo=lo, hi=hi, tol=0.05)

    def f(Pw, _uc=uc, _y=yon):
        m = np.abs(Pw[..., 0] - _uc) < 0.01
        Pw[..., 0][m] += _y * KISALT
        return Pw
    g.donustur(b, f)
    KAYIT.append(dict(lo=[round(float(x), 2) for x in lo], uc_eski=round(float(uc), 2), uc_yeni=round(float(uc + yon * KISALT), 2)))
g._bc.clear()
tmp = go + ".e1.glb"; g.kaydet(tmp); del g
SE.sikistir(tmp, go); os.remove(tmp)
json.dump(dict(adim=43, vida="DIN 7991 M5 × 6 A2 (önce M5 × 10)", adet=len(KAYIT), kisaltma_mm=KISALT, vidalar=KAYIT),
          open(go[:-4] + "_ent.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
LOG("ADIM 43 bitti · %s · %d vida kısaltıldı · %.0f sn" % (go, len(KAYIT), time.time() - t0))
sys.stdout.flush(); os._exit(0)
