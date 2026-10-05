# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 65 · TOPPING SERVİS SACI: MOTOR SENSÖRÜNÜN ÖNÜNDEKİ KABLO KANALI 30 → 25 mm (5 Eki 2026 · Claude · bulut oturumu · TOPPING montaj v6)
python 65_kanal_daralt.py girdi.glb cikti.glb      (zincir: hat3_v10f.glb → hat3_v10g.glb)

Montaj sırası denetimi (TOPPING v6): servis sacı alt montajı (pano + kanallar, tezgâhta) arkadan girerken yatay kablo kanalı
(ELK_TOPPING__kanal x 2205–2400 · y 1240–1270 · z −798…−768) sucuk motorunun arkasındaki sensörün
(x 2355,5–2365,5 · y 1265,5–1290,5 · z −812…−802) içinden geçer: sensör sac ile kanal arasındaki boşlukta, kanalın üst kenarının 4,5 mm altında.
Bitmiş hâlde çakışma yok, ama kanal sensörü geçmeden yerine giremez. Kanalın altında motor gövdesi (y 1240'ta temas) → aşağı inemez.
Çözüm: kanal 25 mm yüksekliğinde (standart 25 × 30 kanal) · alt kenar aynı (y 1240), üst kenar 1265 → sensörle 0,5 mm boşluk, servis sacı düz girer.
Kanal kesiti y ekseninde 25/30 ölçeklenir (alt kenar sabit). Denetim: bileşen beklenen kutuda; sağ uçtaki T kutusu (x 2400–2419,5) 30 mm kalır, 25'lik kanal içine girer · yeni üst kenar ≤ 1265,0."""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb

gi, go = sys.argv[1:3]
t0 = time.time(); LOG = SE.log
Y0, Y1, Y1Y = 1240.0, 1270.0, 1265.0
KANAL = [("ELK_TOPPING__kanal", (2205.0, 1240.0, -798.0), (2400.0, 1270.0, -768.0))]   # x 2400–2419,5 T kutusu (ELK_IC) 30 mm kalır: sensörün izinde değil
SENSOR = ((2355.5, 1265.5, -812.0), (2365.5, 1290.5, -802.0))

g = Glb(gi)
for dug, lo, hi in KANAL:
    b = g.bilesen(dug, lo=np.array(lo), hi=np.array(hi), tol=0.3)
    P0 = np.concatenate([p["X"][p["T"][t]] for p, t in b["parca"]])
    assert np.allclose(P0.reshape(-1, 3).min(0), lo, atol=0.3) and np.allclose(P0.reshape(-1, 3).max(0), hi, atol=0.3), "ADIM 65 DUR: %s kutusu beklenen değil" % dug

    def f(P):
        P[..., 1] = Y0 + (P[..., 1] - Y0) * (Y1Y - Y0) / (Y1 - Y0)
        return P
    n = g.donustur(b, f)
    LOG("  %s x %.1f–%.1f: y %.0f–%.0f → %.0f–%.0f (%d üçgen)" % (dug, lo[0], hi[0], Y0, Y1, Y0, Y1Y, n))
    P1 = f(P0.copy()).reshape(-1, 3)
    assert P1[:, 1].max() <= Y1Y + 1e-3, "ADIM 65 DUR: %s üst kenarı %.2f" % (dug, P1[:, 1].max())
    assert P1[:, 0].max() < SENSOR[0][0] or P1[:, 1].max() < SENSOR[0][1] or P1[:, 0].min() > SENSOR[1][0], "ADIM 65 DUR: kanal hâlâ sensörün izinde"
tmp = go + ".e1.glb"; g.kaydet(tmp); del g
SE.sikistir(tmp, go); os.remove(tmp)
LOG("ADIM 65 bitti · %s · %.0f sn" % (go, time.time() - t0))
sys.stdout.flush(); os._exit(0)
