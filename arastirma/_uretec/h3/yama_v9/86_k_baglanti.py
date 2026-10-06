# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 86 · K İSTASYONU: BAĞLANTISIZ PARÇALARIN GERÇEK BAĞLANTILARI (6 Eki 2026 · Claude · bulut oturumu · K montaj, Codex devri)
python 86_k_baglanti.py girdi.glb cikti.glb      (K kolu: hat3_v10ze.glb (Codex K prototipi) → hat3_v10zf.glb)

Kemal (6 Eki): "Codex'in yarım K işini kendi yönteminle bitir; her şey üretilebilir, standart." Codex devrinde 199 (Claude denetiminde 212)
taşıyıcı parçaya hiçbir bağlantı elemanı değmiyordu (KURALLAR §2.3 kural 10, §5). Bağlantı tasarımı `veri/86_k_baglanti.json`'da
(üreten: _local/codex_k_montaj/k1/k_baglanti_plan.py — her parça için oturduğu yüzey, temas yaması, normal; vida yeri yamada kenardan ≥ d;
baş + anahtar yolu + somun hacmi boş; gövde yalnız iki parçadan geçer; diş tutuşu ≥ 1 × d; katalog boyu):
  vida     ISO 4762 / ISO 7380 / DIN 7991 A2-70 + (dişli delik | ISO 4032 somun | kör perçin somun) · delik_ac iki parçada geçiş / dişli delik açar
  saplama  PEM FHS (dış sacta, baş yüzeyle aynı) + fiberli somun · bıçak seti merkez saplaması M8 + kelebek somun
  pim      ISO 8734 Ø6 (bıçak seti göbeği ↔ kafa plakası, dönmez)
  kaynak   TIG / punta işareti iki parçanın temas yüzeyinde
  taşı     koruma braketleri kafa plakası kenarına yaslanır (0–2,9 mm boşluk) · kelebek somun göbek eksenine
  sil      bıçakların arasında karşı parçası olmayan iki kelebek somun proxy'si
Beyanlı bağlantılar (dişli rakor, DIN raya geçme, oluk sensörü, kelepçe, rulman mil, ürün iç parçası, elle çıkan) bu adımda geometri değil;
K montaj bağlantı denetiminde karşı parçaya temasla doğrulanır.
Denetim (bu betikte): taşınan / silinen bileşen beklenen kutuda · her vida / saplama / pim en az bir karşı parçayı deler."""
import os, sys, time, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb
import cadquery as cq

gi, go = sys.argv[1:3]
t0 = time.time(); LOG = SE.log
V = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'veri', '86_k_baglanti.json'), encoding='utf-8'))
v3 = lambda x: cq.Vector(*[float(t) for t in x])


def sil_(p0, p1, r):
    p0 = np.asarray(p0, float); p1 = np.asarray(p1, float); L = float(np.linalg.norm(p1 - p0))
    return cq.Solid.makeCylinder(float(r), L, v3(p0), v3((p1 - p0) / L))


def boru(p0, p1, r0, r1):
    return cq.Workplane("XY").add(sil_(p0, p1, r0)).cut(cq.Workplane("XY").add(sil_(p0, p1, r1))).val()


g = Glb(gi)


def bul(dug, lo, hi, tol=0.6):
    g.bilesen(dug, no=0)
    return [b for b in g._bc[dug] if np.all(b["lo"] >= np.array(lo) - tol) and np.all(b["hi"] <= np.array(hi) + tol)]


# ---- taşı / sil (bileşen: düğüm + parçanın eski kutusu)
for ad, k in V["tasi"].items():
    L = bul(k["dugum"], k["lo"], k["hi"])
    assert L, "ADIM 86 DUR: taşınacak %s bulunamadı" % ad
    d_ = np.array(k["v"], float)
    for b in L: g.donustur(b, lambda P, d_=d_: P + d_)
    g._bc.pop(k["dugum"], None)
    LOG("  taşındı %-22s %d bileşen · %s mm" % (ad, len(L), np.round(d_, 2).tolist()))
for ad, k in V["sil"].items():
    L = bul(k["dugum"], k["lo"], k["hi"])
    assert L, "ADIM 86 DUR: silinecek %s bulunamadı" % ad
    for b in L: g.sil_b(b)
    g._bc.pop(k["dugum"], None)
    LOG("  silindi %-22s %d bileşen" % (ad, len(L)))
tmp0 = go + ".e0.glb"; g.kaydet(tmp0); del g
g = Glb(tmp0); os.remove(tmp0)
# ---- elemanlar
VIDA, SOM, KAY = [], [], []
for e in V["eleman"]:
    t = e["tip"]
    if t == "vida":
        p0, p1, r = e["govde"]
        sh = sil_(p0, p1, r)
        if e.get("bas"):
            b0, b1, rb = e["bas"]; sh = sh.fuse(sil_(b0, b1, rb))
        elif e.get("havsa"):
            ax = np.asarray(p1, float) - np.asarray(p0, float); ax /= np.linalg.norm(ax)
            sh = sh.fuse(cq.Solid.makeCone(2 * r, r, r, v3(p0), v3(ax)))       # 90° havşa baş, üst parçaya gömülü (delik_ac havşayı açar)
        VIDA.append(dict(ad=e["ad"], sh=sh, bom=[e["bom"]]))
    elif t in ("saplama", "pim"):
        p0, p1, r = e["govde"]
        VIDA.append(dict(ad=e["ad"], sh=sil_(p0, p1, r), bom=[e["bom"]]))
    elif t == "somun":
        p0, p1, r = e["sil"]; d = e["d"]
        SOM.append(dict(ad=e["ad"], sh=boru(p0, p1, r, d / 2 - 0.05), bom=[e["bom"]]))
    elif t == "kaynak":
        c = np.asarray(e["merkez"], float); ax = np.asarray(e["eks"], float); ax /= np.linalg.norm(ax)
        r = 2.0 if e["yontem"] == "TIG" else 2.5
        KAY.append(dict(ad=e["ad"], sh=sil_(c - ax * 0.6, c + ax * 0.6, r), bom=[e["bom"]]))
LOG("  eleman: %d vida / saplama / pim · %d somun · %d kaynak" % (len(VIDA), len(SOM), len(KAY)))
K = SE.Karsi(g, acik_dene=True)
kayit = K.delik_ac(VIDA)
delinen = set(a for k in kayit for a in k.get("eleman", []))
eksik = sorted(set(p["ad"] for p in VIDA) - delinen)
for x in eksik: LOG("  ÇIKARILDI (hiçbir parçayı kesmiyor): %s" % x)
VIDA = [p for p in VIDA if p["ad"] not in eksik]
SOM = [p for p in SOM if p["ad"].rsplit("_", 1)[0] not in set(x.rsplit("_", 1)[0] for x in eksik)]
assert len(eksik) <= 4, "ADIM 86 DUR: karşı parçaya girmeyen eleman çok %s" % eksik
tmp = go + ".e1.glb"; g.kaydet(tmp); del g, K
H = SE.Ham(tmp)
PAR = [("K_BAG__vida", "K_GOVDE__celik", VIDA + SOM), ("K_BAG__kaynak", "K_GOVDE__sac", KAY)]
TUM = {}
for d, sb, L in PAR:
    if not L: continue
    H.koy(d, L, kat=0, mek=25, kpk_fn=lambda a: False, sablon=sb)
    TUM[d] = L
H.yaz(tmp + ".e2.glb")
SE.sikistir(tmp + ".e2.glb", go)
for f in (tmp, tmp + ".e2.glb"): os.remove(f)
for d in TUM: H.aralik[d] = {p["ad"]: (0, 0) for p in TUM[d]}
SE.ent_json(go[:-4] + "_ent.json", "K_BAGLANTI", [(d, TUM[d]) for d in sorted(TUM)], H.aralik, lambda a: False, "K/Gövde", (), kayit,
            ek=dict(tasi=V["tasi"], sil=V["sil"]))
LOG("ADIM 86 bitti · %s · %d vida/saplama/pim · %d somun · %d kaynak · %.0f sn" % (go, len(VIDA), len(SOM), len(KAY), time.time() - t0))
sys.stdout.flush(); os._exit(0)
