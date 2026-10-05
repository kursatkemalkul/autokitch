# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 34 · B (ÇEKMECELİ SOĞUK DOLAP) ÜRETİM SACI → ANA MODEL (gece 2 · adım 5-entegrasyon 1. tur · 4 Eki 2026 · Claude · YEREL)
python 34_b_sac.py girdi.glb cikti.glb      (zincir: hat3_v9a.glb → hat3_v9b.glb)
Üreteç: h3/h3_b_sac_v1.py (63 sac + 19 PU, sandviç kasa, 2 parçalı dış kabuk / çerçeve, 126 ray PEM'i) · standart yama_v9/sac_standart.
GÖVDE: B_KASA__sac (dış kabuk, köşebent, iç kabuk, bölmeler, kovanlar, ısı kalkanı, teknik kapama) · B_KASA__on_cerceve (2 parça çerçeve + ek laması;
       opak, kapak değil) · B_KASA__pu (görünmez; x-ray / kesitte sarı) · B_KASA__koyu (PTFE + cam elyaf takozlar) · B_KASA__paslanmaz (YENİ:
       PEM SP-M5 × 126 + kaynak dolguları + B içinden takılan arayüz cıvataları) · B_KASA__conta (YENİ: PEM köpük kapakları, ek yeri / gider silikonları).
       B_KASA__celik (14 ayak) DOKUNULMAZ. kat 0 (GOVDE) · mek 2 (B/Gövde) · kpk yok.
KARŞI TARAF (ARAYÜZ): 42 sabit çekmece rayı × 3 = 126 havşa delik (Ø5,5 + 90° havşa · DIN 7991 M5 × 10 başı) · B_MODULER alt şase üst duvarında
       10 × M8 perçin somun (+ cıvata deliği) · A → B: B_MODULER üst kirişi üst duvarında 6 × M8 kapalı uçlu perçin somun (A kaidesinden gelen
       cıvatalar adım 33'te) · K → B: B_TASIYICI çapraz kirişi üst duvarında 2 × M8 perçin somun (K iskeletinin cıvataları için, h3_k_sac_v1).
       Perçin somunlar B_MODULER__baglanti / B_TASIYICI__baglanti (yeni, B/Gövde) düğümüne — karşı parçanın kendi düğümünde olsa yuvasıyla tek bileşen sayılırdı."""
import os, sys, time, re
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb
import h3_b_sac_v1 as B
import h3_a_sac_v1 as A
import h3_sac_v1 as S

gi, go = sys.argv[1:3]
t0 = time.time()
GOVDE = B.dunya_listesi(B.govde_parcalari())
ARAYUZ = B.dunya_listesi(B.G.ARAYUZ)
A.kur(log=lambda *a: None)
SE.log("B üreteci: %d gövde parçası · %d arayüz elemanı · %.1f sn" % (len(GOVDE), len(ARAYUZ), time.time() - t0))
ESKI = ("B_KASA__sac", "B_KASA__pu", "B_KASA__on_cerceve", "B_KASA__koyu", "B_KASA__paslanmaz", "B_KASA__conta")


def hedef(p):
    m = B._mal(p)
    return {"pu": "B_KASA__pu", "on_cerceve": "B_KASA__on_cerceve", "kabuk": "B_KASA__sac", "sac": "B_KASA__sac", "koyu": "B_KASA__koyu",
            "conta": "B_KASA__conta"}.get(m, "B_KASA__paslanmaz")


# ---------------------------------------------------------------- EVRE 1 · karşı taraf
g = Glb(gi)


def percin(ad, x, z, dugumler, y_ust=800.0, y_alt=0.0, kayma=6.0):
    """(x, z) dikey ekseninde, y_ust'ten aşağı ilk kapalı bileşenin üst duvarına M8 perçin somun (üst dış yüz + duvar kalınlığı ışınla ölçülür;
    ışın eksenden 'kayma' kadar yanda — eksende önceki adımın cıvata deliği olabilir)"""
    for d in dugumler:
        g.bilesen(d, 0)
        for b in g._bc[d]:
            if not (b["lo"][0] - 0.1 <= x <= b["hi"][0] + 0.1 and b["lo"][2] - 0.1 <= z <= b["hi"][2] + 0.1 and b["hi"][1] <= y_ust and b["lo"][1] >= y_alt - 1): continue
            P = np.concatenate([q["X"][q["T"][t]] for q, t in b["parca"]])
            ys = SE.isin_y(P, x + kayma, z, y_ust, y_alt)
            if len(ys) < 2: continue
            y1, y2 = ys[-1], ys[-2]                                           # aşağı inen ışın: en üst iki yüz (dış, iç)
            p, c = S.percin_somun("M8", y1 - y2, (x, y1, z), (0, -1.0, 0), ad=ad, birim="B_GOVDE", kapali=True)
            return p, d, "%s[%d]" % (d, b["no"]), y1, y1 - y2
    return None, None, None, None, None


PERCIN = []
for p in ARAYUZ:                                                           # alt şase: arayuz_sase_<x>_<z> (cıvata, pul değil)
    m = re.match(r"arayuz_sase_(\d+)_(\d+)$", p["ad"])
    if m: PERCIN.append(("percin_somun_sase_%s_%s" % m.groups(), float(m.group(1)), -float(m.group(2)), ["B_MODULER__paslanmaz"], 200.0, 0.0))
for e in A.G.M8:                                                           # A kaidesi → B_MODULER üst kirişi
    if e["taraf"] == "B":
        x, _, z = e["dunya"]; PERCIN.append(("percin_somun_ab_%d_%d" % (round(x), round(-z)), x, z, ["B_MODULER__paslanmaz"], 788.0, 600.0))
for x, z in B.KB_DELIK:                                                    # K iskeleti → B_TASIYICI çapraz kirişi
    PERCIN.append(("percin_somun_kb_%d_%d" % (round(x), round(-z)), x, z, ["B_TASIYICI__celik", "B_MODULER__paslanmaz"], 788.0, 600.0))
KARSI = {}
for ad, x, z, dl, yu, ya in PERCIN:
    p, d, bad, y1, t = percin(ad, x, z, dl, yu, ya)
    if p is None: SE.log("  UYARI perçin somun yeri bulunamadı: %s (x %.1f z %.1f)" % (ad, x, z)); continue
    SE.log("  perçin somun %-28s %s üst yüz y %.2f · duvar %.2f" % (ad, bad, y1, t))
    KARSI.setdefault(d, []).append(p)
K = SE.Karsi(g, haric_onek=ESKI)
SE.log("EVRE 1 · karşı taraf delikleri (%d arayüz + %d perçin somun)" % (len(ARAYUZ), sum(len(v) for v in KARSI.values())))
kayit = K.delik_ac(ARAYUZ + [p for d in sorted(KARSI) for p in KARSI[d]])
tmp = go + ".e1.glb"; g.kaydet(tmp); del g, K

# ---------------------------------------------------------------- EVRE 2 · gövde
SE.log("EVRE 2 · gövde düğümleri")
# perçin somun başı (Ø15 × 1,5) dış tavan / dış taban sacının içine gelir → o saclarda baş boşluğu Ø15,5. ADIM 8'den beri üreteç (h3_b_sac_v1.PERCIN_BAS_BOSLUK)
# deliği doğrudan Ø15,5 açar → bu kesim etkisiz kalır (kesişim hacmi 0 → parça atlanır); güvenlik ağı olarak duruyor (log'da "gövde boşluğu" satırı çıkmamalı)
GOVDE = SE.kes_govde(GOVDE, [p for d in sorted(KARSI) for p in KARSI[d]])
H = SE.Ham(tmp)
DUG = {}
for p in GOVDE: DUG.setdefault(hedef(p), []).append(p)
DUG["B_KASA__paslanmaz"] = DUG.get("B_KASA__paslanmaz", []) + ARAYUZ
SABLON = {"B_KASA__paslanmaz": "B_MODULER__paslanmaz", "B_KASA__conta": "K_GOVDE__conta"}
SIRA = ["B_KASA__sac", "B_KASA__on_cerceve", "B_KASA__pu", "B_KASA__koyu", "B_KASA__paslanmaz", "B_KASA__conta"]
for d in sorted(DUG): assert d in SIRA, d
for d in SIRA:
    if d in DUG: H.koy(d, DUG[d], kat=0, mek=2, sablon=SABLON.get(d))
    else: H.bosalt(d)
KDUG = []
for d in sorted(KARSI):                                                    # perçin somunlar karşı birimin AYRI bağlantı düğümüne (aynı düğümde olsa yuvasıyla tek bileşen sayılır)
    kd = d.split("__")[0] + "__baglanti"; H.koy(kd, KARSI[d], kat=0, mek=2, sablon=d); KDUG.append((kd, KARSI[d]))
H.yaz(tmp + ".e2.glb")
SE.sikistir(tmp + ".e2.glb", go)
for f in (tmp, tmp + ".e2.glb"): os.remove(f)
SE.ent_json(go[:-4] + "_ent.json", "B", [(d, DUG[d]) for d in SIRA if d in DUG] + KDUG, H.aralik, lambda a: False, "B/Gövde",
            ("B_KASA",), kayit, ek=dict(karsi_eleman={d: [p["ad"] for p in KARSI[d]] for d in sorted(KARSI)}))
SE.log("ADIM 34 bitti · %s · %.0f sn" % (go, time.time() - t0))
sys.stdout.flush(); os._exit(0)
