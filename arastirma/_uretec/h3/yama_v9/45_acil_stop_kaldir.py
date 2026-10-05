# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 45 · ACİL STOP BUTONLARI KALDIRILDI (4 Eki 2026 · Claude · YEREL · Kemal: "bu ne, kaldır, tek tuş koyduk ana şeye")
python 45_acil_stop_kaldir.py girdi.glb v9g.glb cikti.glb      (zincir: hat3_v9l.glb + hat3_v9g.glb → hat3_v9m.glb)

Adım 40'ın eklediği 6 Schneider XB4BS8442 butonu (TOPPING, B, F, K, E, QR servis yüzü) tamamen kalkar:
  1. ACIL_STOP__sari / __siyah / __kirmizi düğümleri (etiket diski, bilezik, mantar, gövde + kontak bloğu) silinir — düğüm, ağ, malzeme;
     sahne / çocuk / animasyon kanalı düğüm indisleri yeniden numaralanır. Adım 40 kablo, conta, montaj deliği ÇİZMEMİŞTİ (yalnız gövde cebi).
  2. Adım 40'ın kapak sacı / camı / PU'da açtığı gövde cepleri (30 × 30 × 43, delik_ac) KAPATILIR: cebin açıldığı her bileşen, adım 40'ın
     GİRDİSİNDEKİ (hat3_v9g) aynı bileşenle değiştirilir. Güvenlik: girdi bileşeni = v9g bileşeni − cep kutusu (hacim farkı = v9g ∩ kutu hacmi,
     ±0,5 mm³; kutu dışında üçgenler aynı) değilse betik DURUR (41–44 bu bileşenlere dokunmadı).
Adım 40 zincirde kalır (41–44 onun çıktısının üçgen / düğüm sırasına göre yazıldı); bu adım onun etkisini geri alır."""
import os, sys, time, json, struct
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb

gi, g9, go = sys.argv[1:4]
t0 = time.time(); LOG = SE.log
# adım 40 YER tablosu (istasyon, x, y, ön yüz z, normal) — cep = gövde 30 × 30 × 43 kapağın arkasında
YER = [("TOPPING", 2440.0, 1000.0, 79.0, +1), ("B", 4300.0, 750.0, 79.0, +1), ("F", 2600.0, 1460.0, 79.0, +1),
       ("K", 4300.0, 1400.0, 79.0, +1), ("E", 5150.0, 1300.0, 79.0, +1), ("QR", 5100.0, 1690.0, 670.0, -1)]
CEP = []
for ist, x, y, z0, n in YER:
    a, b = sorted((z0, z0 - n * 43.0))
    CEP.append((ist, np.array([x - 15.0, y - 15.0, a]), np.array([x + 15.0, y + 15.0, b])))
ACIL = ("ACIL_STOP__sari", "ACIL_STOP__siyah", "ACIL_STOP__kirmizi")


def kutu_kesisir(lo, hi, a, b, pay=0.01):
    return bool(np.all(hi >= a - pay) and np.all(b >= lo - pay))


def ucg(b):
    return np.concatenate([p["X"][p["T"][t]] for p, t in b["parca"]])


# ---------------------------------------------------------------- 1. cepleri kapat (m8kit)
g = Glb(gi); g0 = Glb(g9)
KAYIT = []
for ist, lo, hi in CEP:
    adaylar = []
    for d in sorted(set(p["name"] for p in g.prims)):
        if d.startswith("ACIL_STOP"): continue
        Q = [p for p in g.dprims(d) if not p.get("gizli") and p["pr"].get("mode", 4) == 4]
        if not Q: continue
        X = np.concatenate([p["X"] for p in Q])
        if not kutu_kesisir(lo, hi, X.min(0), X.max(0)): continue
        g._bc.pop(d, None)
        try: g.bilesen(d, 0)
        except (IndexError, ValueError): continue
        for b in g._bc[d]:
            if not kutu_kesisir(lo, hi, b["lo"], b["hi"]): continue
            P = ucg(b)
            # bileşenin kutu içine giren üçgeni (cep yüzü) var mı?
            c = P.mean(1)
            if not np.any(np.all((c > lo - 0.01) & (c < hi + 0.01), 1)): continue
            adaylar.append((d, b))
    for d, b in adaylar:
        g0._bc.pop(d, None)
        try:
            b0 = g0.bilesen(d, lo=b["lo"], hi=b["hi"], tol=0.05)
        except KeyError:
            continue
        P1 = ucg(b); P0 = ucg(b0)
        m1 = SE.mf_ucgen(P1); m0 = SE.mf_ucgen(P0)
        if m1 is None or m0 is None:
            LOG("  atla (kapalı değil): %s %s" % (d, ist)); continue
        import manifold3d as mf
        kut = mf.Manifold.cube([float(v) for v in (hi - lo)]).translate([float(v) for v in lo])
        v_cep = (m0 ^ kut).volume(); fark = m0.volume() - m1.volume()
        if fark < 1e-3 and v_cep < 1e-3: continue                      # cep bu bileşende değil (kutu yalnız teğet)
        if abs(fark - v_cep) > 0.5:
            raise SystemExit("ADIM 45 DUR: %s (%s) girdi ≠ v9g − cep (fark %.2f, cep %.2f mm³)" % (d, ist, fark, v_cep))
        # (girdi − v9g) farkı yalnız cep kutusunda: (m0 − kutu) ile (m1 − kutu) aynı katı
        d_dis = abs((m0 - kut).volume() - (m1 - kut).volume())
        if d_dis > 0.5:
            raise SystemExit("ADIM 45 DUR: %s (%s) kutu dışında da fark var (%.2f mm³)" % (d, ist, d_dis))
        ilk = [True]
        def f(_, P0=P0):
            if ilk[0]: ilk[0] = False; return P0
            return None
        g.donustur(b, f)
        KAYIT.append(dict(istasyon=ist, bilesen="%s[%d]" % (d, b["no"]), kutu=[round(float(v), 2) for v in list(b["lo"]) + list(b["hi"])],
                          hacim_once=round(m1.volume(), 1), hacim_sonra=round(m0.volume(), 1), dolan=round(fark, 2)))
        LOG("  cep kapandı: %-44s %s · +%.1f mm³" % ("%s[%d]" % (d, b["no"]), ist, fark))
del g0
n_cep = len(KAYIT)
assert n_cep >= 6, "ADIM 45: beklenen ≥ 6 cep (her butonda en az 1), bulunan %d" % n_cep
tmp = go + ".e1.glb"; g.kaydet(tmp); del g

# ---------------------------------------------------------------- 2. ACIL_STOP düğümleri / ağları / malzemeleri sil (ham GLB)
raw = open(tmp, "rb").read(); jl = struct.unpack("<I", raw[12:16])[0]; J = json.loads(raw[20:20 + jl]); bo = 20 + jl
bl = struct.unpack("<I", raw[bo:bo + 4])[0]; BIN = raw[bo + 8:bo + 8 + bl]
sil_n = [i for i, nd in enumerate(J["nodes"]) if nd.get("name") in ACIL]
assert len(sil_n) == 3, ("ACIL_STOP düğüm sayısı", len(sil_n))
assert not any(nd.get("children") for i, nd in enumerate(J["nodes"]) if i in sil_n)
nmap = {}; yeni = []
for i, nd in enumerate(J["nodes"]):
    if i in sil_n: continue
    nmap[i] = len(yeni); yeni.append(nd)
for nd in yeni:
    if "children" in nd: nd["children"] = [nmap[c] for c in nd["children"] if c in nmap]
for sc in J["scenes"]: sc["nodes"] = [nmap[c] for c in sc["nodes"] if c in nmap]
for an in J.get("animations", []):
    ch = [c for c in an["channels"] if c["target"].get("node") not in sil_n]
    for c in ch:
        if "node" in c["target"]: c["target"]["node"] = nmap[c["target"]["node"]]
    an["channels"] = ch
for sk in J.get("skins", []):
    sk["joints"] = [nmap[j] for j in sk["joints"] if j in nmap]
sil_m = sorted(set(J["nodes"][i]["mesh"] for i in sil_n if "mesh" in J["nodes"][i]))
kalan_m = set(nd["mesh"] for nd in yeni if "mesh" in nd)
sil_m = [m for m in sil_m if m not in kalan_m]
mmap = {}; ym = []
for i, m in enumerate(J["meshes"]):
    if i in sil_m: continue
    mmap[i] = len(ym); ym.append(m)
for nd in yeni:
    if "mesh" in nd: nd["mesh"] = mmap[nd["mesh"]]
J["nodes"] = yeni; J["meshes"] = ym
kul_mat = set(p.get("material") for m in ym for p in m["primitives"] if "material" in p)
sil_mat = [i for i, mt in enumerate(J["materials"]) if mt.get("name", "").find("ACIL_STOP") >= 0 and i not in kul_mat]
matmap = {}; ymat = []
for i, mt in enumerate(J["materials"]):
    if i in sil_mat: continue
    matmap[i] = len(ymat); ymat.append(mt)
for m in ym:
    for p in m["primitives"]:
        if "material" in p: p["material"] = matmap[p["material"]]
J["materials"] = ymat
LOG("  silindi: %d düğüm (%s) · %d ağ · %d malzeme" % (len(sil_n), ", ".join(ACIL), len(sil_m), len(sil_mat)))
jb = json.dumps(J, separators=(",", ":"), ensure_ascii=False).encode(); jb += b" " * ((4 - len(jb) % 4) % 4)
tmp2 = tmp + ".e2.glb"
with open(tmp2, "wb") as f:
    f.write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(jb) + 8 + len(BIN)) + struct.pack("<II", len(jb), 0x4E4F534A) + jb
            + struct.pack("<II", len(BIN), 0x004E4942) + bytes(BIN))
SE.sikistir(tmp2, go)
for f_ in (tmp, tmp2): os.remove(f_)
json.dump(dict(adim=45, ad="acil stop kaldırıldı", cep=KAYIT, silinen_dugum=list(ACIL), log=SE.LOG),
          open(go[:-4] + "_ent.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
LOG("ADIM 45 bitti · %d cep kapandı · %s · %.0f sn" % (n_cep, go, time.time() - t0))
sys.stdout.flush(); os._exit(0)
