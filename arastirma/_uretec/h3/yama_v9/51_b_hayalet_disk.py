# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 51 · B TAŞIYICI ÜST KİRİŞİNDE HAYALET DİSK SİLİNDİ (4 Eki 2026 · Claude · YEREL)
python 51_b_hayalet_disk.py girdi.glb cikti.glb      (zincir: hat3_v9r.glb → hat3_v9s.glb)

B montaj animasyonu v4 'havada' denetimi buldu: B_TASIYICI__celik düğümünde iki Ø8 × 2 mm disk (x 4016,5 · z −570 / −480, y 784,5…786,5)
taşıyıcı üst kirişin üst duvarındaki Ø10,95 perçin somun deliğinin İÇİNDE, hiçbir parçaya değmeden duruyor (kirişe 1,475 mm, perçin somuna
1,475 mm). Gerçek bir parça değil: delik açılırken boru biçimli kesicinin bıraktığı çekirdek (adım 45'ten önce de vardı). Bu adım:
  1. B_TASIYICI__celik bileşenlerinden en büyük ölçüsü < 10 mm, en küçük ölçüsü ≤ 2,1 mm olanları bulur (beklenen tam 2 — değilse DURUR);
  2. her diskin düğümün geri kalanına ve B_TASIYICI__baglanti / B_MODULER__baglanti bileşenlerine en yakın köşe uzaklığı > 1 mm değilse DURUR
     (yani yalnız hiçbir şeye değmeyen disk silinir);
  3. diskleri siler; 50_sikilastir ile dejenere üçgenler / kullanılmayan köşeler atılır (geometrinin geri kalanı aynı)."""
import os, sys, time, json, subprocess
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb

gi, go = sys.argv[1:3]
t0 = time.time(); LOG = SE.log
g = Glb(gi)
D = "B_TASIYICI__celik"
g._bc.pop(D, None); g.bilesen(D, 0)


def ucg(b):
    return np.concatenate([p["X"][p["T"][t]] for p, t in b["parca"]])


DISK = []
for b in g._bc[D]:
    e = np.asarray(b["hi"]) - np.asarray(b["lo"])
    if e.max() < 10.0 and e.min() <= 2.1: DISK.append(b)
assert len(DISK) == 2, "ADIM 51 DUR: beklenen 2 disk, bulunan %d" % len(DISK)
KOMSU = []
DNO = set(b["no"] for b in DISK)
for d in (D, "B_TASIYICI__baglanti", "B_MODULER__baglanti", "B_MODULER__paslanmaz"):
    if d != D:
        g._bc.pop(d, None)
        try: g.bilesen(d, 0)
        except (IndexError, ValueError, KeyError): continue
    for b in g._bc[d]:
        if d == D and b["no"] in DNO: continue
        KOMSU.append(ucg(b).reshape(-1, 3))
KOMSU = np.concatenate(KOMSU)
KAYIT = []
for b in DISK:
    P = ucg(b).reshape(-1, 3); lo, hi = P.min(0), P.max(0)
    m = np.all(KOMSU >= lo - 6, 1) & np.all(KOMSU <= hi + 6, 1)
    dmin = float(np.min(np.linalg.norm(KOMSU[m][:, None, :] - P[None, :, :], axis=2))) if m.any() else 99.0
    # köşe-köşe uzaklığı yüzeye uzaklıktan büyük olabilir: disk kenarı (r 4) ↔ delik duvarı (r 5,475) için yeterli ölçüt
    assert dmin > 1.0, "ADIM 51 DUR: disk %s[%d] bir parçaya değiyor (%.3f mm)" % (D, b["no"], dmin)
    KAYIT.append(dict(bilesen="%s[%d]" % (D, b["no"]), kutu=[round(float(v), 2) for v in list(lo) + list(hi)], en_yakin_mm=round(dmin, 3)))
    LOG("  hayalet disk: %s[%d] · kutu %s … %s · en yakın parça %.3f mm" % (D, b["no"], lo.round(2), hi.round(2), dmin))
for b in DISK: g.sil_b(b)
tmp = go + ".d51.glb"; g.kaydet(tmp); del g
r = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "50_sikilastir.py"), tmp, go]); assert r.returncode == 0
os.remove(tmp)
json.dump(dict(adim=51, ad="B taşıyıcı hayalet disk silindi", disk=KAYIT, log=SE.LOG), open(go[:-4] + "_ent.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
LOG("ADIM 51 bitti · %d disk silindi · %s · %.0f sn" % (len(DISK), go, time.time() - t0))
sys.stdout.flush(); os._exit(0)
