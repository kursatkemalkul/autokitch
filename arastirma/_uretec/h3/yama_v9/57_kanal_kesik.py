# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 57 · SERVİS SACI YATAY KABLO KANALI AYAK HİZALARINDAN KESİK (5 Eki 2026 · Claude · bulut oturumu · Kemal: "kablo kanalını en mantıklısını yap")
python 57_kanal_kesik.py girdi.glb cikti.glb      (zincir: hat3_v9x.glb → hat3_v9y.glb)

Sorun (TOPPING montaj v5 yol denetimi): arka servis sacına 3 braketle bağlı yatay kablo kanalı (ELK_TOPPING__kanal, x 1470–2400, y 1240–1270,
z −798…−768) dört evaporatör ayağının dik kolunun (z −828,5…−826) önünden geçer. Servis sacı arkadan kapanırken (ya da bakımda çıkarken)
kanal ayakların içinden geçmek zorunda: 26–28 üçgen gerçek kesişim. Sıra ile çözülmez (servis sacı en son kapanır, evaporatör kasete kaynaklı ayaklarla).
Seçilen düzeltme (en az değişiklik, servis sacı yine tek parça sökülür): kanal ayak hizalarından 2 mm boşlukla kesilir → 4 parça
  [1496, 1621] · [1652, 1776] · [1810, 2171] · [2205, 2400]   (ayaklar x 1464–1494 · 1623–1650 · 1778–1808 · 2173–2203)
  1. parça 1495–1505 braketinde, 2. parça dik kablo kanalına (x 1671–1701) bağlı, 3. parça 1945–1955, 4. parça 2325–2335 braketinde.
  Kablolar kesik aralıklardan ayakların önünden serbest geçer (kanal kapağı her parçada ayrı).
Kesilen ilk bölümde (x 1470–1496) duran boş rakor (kablosu yok) 1476 → 1608'e kayar (aynı aralık 33 mm, 4. sırada · ayak 1'e 3 mm).
Etiket (kat / mek / kpk) korunur. Denetim (bu betikte): kanal tek bileşen ve su geçirmez · 4 parça çıkar · rakor yeni yerinde kanal üst yüzüne oturur."""
import os, sys, time, json, subprocess
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb
import manifold3d as mf

gi, go = sys.argv[1:3]
t0 = time.time(); LOG = SE.log
HERE = os.path.dirname(os.path.abspath(__file__))
KANAL = ('ELK_TOPPING__kanal', (1470.0, 1240.0, -798.0), (2400.0, 1270.0, -768.0))
RAKOR = [('ELK_TOPPING__rakor', (1478.0, 1268.5, -786.0), (1486.0, 1270.0, -778.0)), ('ELK_TOPPING__rakor', (1476.0, 1270.0, -788.0), (1488.0, 1272.0, -776.0))]   # halka + gövde
KESIK = [(1460.0, 1496.0), (1621.0, 1652.0), (1776.0, 1810.0), (2171.0, 2205.0)]
RAKOR_DX = 132.0


def mfk(P):
    V = P.reshape(-1, 3); u, inv = np.unique(np.round(V, 5), axis=0, return_inverse=True)
    m = mf.Manifold(mf.Mesh(vert_properties=u.astype(np.float32), tri_verts=inv.reshape(-1, 3).astype(np.uint32)))
    assert m.status() == mf.Error.NoError, m.status()
    return m


def mf_P(m):
    M = m.to_mesh(); V = np.asarray(M.vert_properties)[:, :3].astype(float); T = np.asarray(M.tri_verts).astype(np.int64)
    return V[T]


g = Glb(gi)
b = g.bilesen(KANAL[0], lo=np.array(KANAL[1]), hi=np.array(KANAL[2]), tol=0.3)
P0 = np.concatenate([p["X"][p["T"][t]] for p, t in b["parca"]])
K = mfk(P0)
vol0 = K.volume()
for x0, x1 in KESIK:
    K = K - mf.Manifold.cube([x1 - x0, 60.0, 60.0]).translate([x0, 1240.0 - 15.0, -798.0 - 15.0])
parcalar = K.decompose()
LOG("kanal: %d üçgen · hacim %.0f → %.0f mm³ · %d parça" % (len(P0), vol0, K.volume(), len(parcalar)))
assert len(parcalar) == 4, "ADIM 57 DUR: parça sayısı %d" % len(parcalar)
YENI = mf_P(K)
n = g.donustur(b, lambda P: YENI)
RB = [g.bilesen(d, lo=np.array(l), hi=np.array(h), tol=0.3) for d, l, h in RAKOR]
for r in RB: g.tasi_b(r, np.array([RAKOR_DX, 0.0, 0.0]))
KAYIT = dict(adim=57, ad="servis sacı yatay kablo kanalı ayak hizalarından kesik (4 parça) + boş rakor 1476 → 1608", kesik=KESIK,
             parca=[[np.round(np.asarray(m.bounding_box())[:3], 2).tolist(), np.round(np.asarray(m.bounding_box())[3:], 2).tolist()] for m in parcalar], rakor_dx=RAKOR_DX)
tmp = go + ".d57.glb"; g.kaydet(tmp); del g
rr = subprocess.run([sys.executable, os.path.join(HERE, "50_sikilastir.py"), tmp, go]); assert rr.returncode == 0
os.remove(tmp)
KAYIT["log"] = SE.LOG
json.dump(KAYIT, open(go[:-4] + "_ent.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0, default=float)
LOG("ADIM 57 bitti · %s · parçalar %s · %.0f sn" % (go, KAYIT["parca"], time.time() - t0))
sys.stdout.flush(); os._exit(0)
