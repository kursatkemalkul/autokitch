# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 56 · SOL EVAPORATÖR 2. AYAĞI 3 mm DAR (5 Eki 2026 · Claude · bulut oturumu · KUYRUK 3 iş 2: TOPPING montaj animasyonu)
python 56_evap_ayak.py girdi.glb cikti.glb      (zincir: hat3_v9w.glb → hat3_v9x.glb)

Montaj yol denetimi (TOPPING v5): tavuk UNO'sunun pnömatik silindiri (arka grup: silindir + duvar flanşı + piston mili) arkadan, mili
burçtan geçerek gelir; mil ucu burcun arkasından (z −635) pistona (z −456) en az 179 mm eksenel ilerlemelidir. Bu sürede duvar flanşı
(x 1570–1622, y 1110,9–1209,4) sol evaporatörün 2. ayağının dik kolunun (x 1620–1650, z −828,5…−826) içinden geçer: 2,0 mm çakışma.
Sıra ile çözülmez: evaporatör yalnız yukarıdan girer (sol yan sacın arka dönüşü arkadan yolu kapatır) ve tavan kapanmadan gelmelidir;
silindir ise UNO gövdesinden (piston) sonra gelebilir, gövde iç sac + raftan sonra, onlar da tavandan sonra.
Düzeltme: ayak (2,5 mm L, kasete üreticide kaynaklı) sol kenarı x 1620 → 1623 (genişlik 30 → 27 mm). Vida deliği (x 1641) ve somun yerinde;
kenar mesafesi 13 mm. Flanş ↔ ayak boşluğu 1,0 mm. Başka parça değişmez; etiket (kat / mek / kpk) korunur.
Denetim (bu betikte): ayak bileşeni tek ve beklenen kutuda · yalnız x = 1620 yüzündeki köşeler taşınır · yeni kutu x 1623–1650."""
import os, sys, time, json, subprocess
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb

gi, go = sys.argv[1:3]
t0 = time.time(); LOG = SE.log
HERE = os.path.dirname(os.path.abspath(__file__))
DUG = 'TOPPING_GOVDE__sac'
LO, HI = np.array([1620.0, 1109.0, -828.5]), np.array([1650.0, 1322.0, -798.5])
X0, X1 = 1620.0, 1623.0

g = Glb(gi)
b = g.bilesen(DUG, lo=LO, hi=HI, tol=0.3)
P0 = np.concatenate([p["X"][p["T"][t]] for p, t in b["parca"]])
Q = P0.reshape(-1, 3)
assert np.all(np.abs(Q.min(0) - LO) < 0.3) and np.all(np.abs(Q.max(0) - HI) < 0.3), "ADIM 56 DUR: ayak kutusu %s %s" % (Q.min(0), Q.max(0))
kenar = np.abs(Q[:, 0] - X0) < 0.02
ic = Q[~kenar][:, 0]
assert ic.min() > X1 + 1.0, "ADIM 56 DUR: kırpılan bantta köşe var (x %.3f)" % ic.min()     # 1620 ile 1624 arasında başka köşe yok → düz uç yüz
LOG("ayak 1: %d üçgen · uç yüz köşesi %d · iç en küçük x %.2f" % (len(P0), int(kenar.sum()), ic.min()))


def f(P):
    R = P.reshape(-1, 3).copy()
    m = np.abs(R[:, 0] - X0) < 0.02
    R[m, 0] = X1
    return R.reshape(P.shape)


n = g.donustur(b, f)
KAYIT = dict(adim=56, ad="sol evaporatör 2. ayağı 3 mm dar (tavuk silindiri flanşı geçişi)", dugum=DUG, eski=[LO.tolist(), HI.tolist()],
             yeni=[[X1, LO[1], LO[2]], HI.tolist()], ucgen=int(n))
tmp = go + ".d56.glb"; g.kaydet(tmp); del g
r = subprocess.run([sys.executable, os.path.join(HERE, "50_sikilastir.py"), tmp, go]); assert r.returncode == 0
os.remove(tmp)
g2 = Glb(go)
b2 = g2.bilesen(DUG, lo=np.array([X1, LO[1], LO[2]]), hi=HI, tol=0.3)
LOG("ADIM 56 denetim: yeni ayak kutusu %s %s" % (np.round(b2["lo"], 2).tolist(), np.round(b2["hi"], 2).tolist()))
KAYIT["log"] = SE.LOG
json.dump(KAYIT, open(go[:-4] + "_ent.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0, default=float)
LOG("ADIM 56 bitti · %s · %.0f sn" % (go, time.time() - t0))
sys.stdout.flush(); os._exit(0)
