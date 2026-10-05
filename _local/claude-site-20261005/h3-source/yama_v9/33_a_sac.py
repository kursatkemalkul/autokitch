# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 33 · A (AÇICI KABUĞU) ÜRETİM SACI → ANA MODEL (gece 2 · adım 5-entegrasyon 1. tur · 4 Eki 2026 · Claude · YEREL)
python 33_a_sac.py girdi.glb cikti.glb      (zincir: hat3_v8zq.glb → hat3_v9a.glb)
Üreteç: h3/h3_a_sac_v1.py (37 sac + 15 boru, kaynaklı kaide + iskelet + 4 panel + çift cidarlı kapak) · standart yama_v9/sac_standart.
GÖVDE: A_GOVDE__sac (panel / profil / kaynak) · A_GOVDE__paslanmaz (PEM, vida, pul, somun, menteşe gövdesi + A tarafındaki arayüz cıvataları) ·
       A_GOVDE__conta (servis tapaları, silikon) · KAIDE_A__paslanmaz (kaide boruları + kaynakları) · KAIDE_A__sac (kaide plakası + damlama sacı) ·
       A_ONYUZ__on_seffaf (kapakla dönen her şey · kpk) · eski A_ONYUZ__on_seffaf__SERVIS_KAPAGI / __paslanmaz / __plastik boşalır.
       kat 0 (GOVDE) · mek 0 (A/Gövde).
KARŞI TARAF (ARAYÜZ): açıcı kolon taban flanşı 4 × Ø9 · tabla rayı tabanı 4 × Ø6,6 · TOPPING sol dış sacı 4 × Ø10,5 + PEM SP-M8 (gövde PU tarafında;
       PU'da PEM yuvası) — PEM'ler TOPPING_MODUL__paslanmaz'a (TOPPING/Gövde) · NOT: TOPPING üretim sacı 5c'de yapılıyor; o gelince bu delik/PEM
       yeni TOPPING sacında olmalı (h3_a_sac_v1.M8_T eksenleri) · A → B cıvatalarının B tarafı (B dış tavanı Ø9, GFRP ped, B_MODULER üst kirişi)
       bu adımda yalnız delik; perçin somunlar adım 34'te (B)."""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb
import h3_a_sac_v1 as A

gi, go = sys.argv[1:3]
t0 = time.time()
GOVDE = A.dunya_listesi(A.govde_parcalari())
ARAYUZ = A.dunya_listesi(A.G.ARAYUZ)
SE.log("A üreteci: %d gövde parçası · %d arayüz elemanı · %.1f sn" % (len(GOVDE), len(ARAYUZ), time.time() - t0))
ESKI = ("A_GOVDE__", "KAIDE_A__", "A_ONYUZ__", "A_MODULER__", "U_A_GOVDE__")


def hedef(p):
    m = A._mal(p); ad = p["ad"]
    if m == "on_seffaf": return "A_ONYUZ__on_seffaf"
    if ad.startswith("kaide_") and p.get("tur") == "sac": return "KAIDE_A__sac"
    if ad.startswith("kaide_") and p.get("tur") in ("profil", "kaynak"): return "KAIDE_A__paslanmaz"
    if m in ("kabuk", "sac"): return "A_GOVDE__sac"
    if m == "conta": return "A_GOVDE__conta"
    if m == "siyah": return "A_GOVDE__plastik"
    return "A_GOVDE__paslanmaz"


PEM_T = [p for p in ARAYUZ if p["ad"].endswith("_pem")]                    # TOPPING sol dış sacına preslenen PEM SP-M8 (karşı taraf)
A_TARAF = [p for p in ARAYUZ if not p["ad"].endswith("_pem")]              # A içinden takılan cıvata + pul → A gövde bağlantısı

# ---------------------------------------------------------------- EVRE 1 · karşı taraf
g = Glb(gi)
K = SE.Karsi(g, haric_onek=ESKI)
SE.log("EVRE 1 · karşı taraf delikleri (%d arayüz elemanı)" % len(ARAYUZ))
kayit = K.delik_ac(ARAYUZ)
SE.ekle_karsi(g, "TOPPING_MODUL__paslanmaz", PEM_T, kat=0, mek=7)
tmp = go + ".e1.glb"; g.kaydet(tmp); del g, K

# ---------------------------------------------------------------- EVRE 2 · gövde
SE.log("EVRE 2 · gövde düğümleri")
H = SE.Ham(tmp)
DUG = {}
for p in GOVDE: DUG.setdefault(hedef(p), []).append(p)
DUG["A_GOVDE__paslanmaz"] = DUG.get("A_GOVDE__paslanmaz", []) + A_TARAF
SABLON = {"A_GOVDE__conta": "F_UST_KABIN__conta", "A_GOVDE__plastik": "A_ONYUZ__plastik"}
SIRA = ["A_GOVDE__sac", "A_GOVDE__paslanmaz", "A_GOVDE__conta", "A_GOVDE__plastik", "KAIDE_A__paslanmaz", "KAIDE_A__sac", "A_ONYUZ__on_seffaf"]
for d in sorted(DUG): assert d in SIRA, d
for d in SIRA:
    if d not in DUG: continue
    H.koy(d, DUG[d], kat=0, mek=0, kpk_fn=A.kapakla_doner, sablon=SABLON.get(d))
for d in ("A_ONYUZ__on_seffaf__SERVIS_KAPAGI", "A_ONYUZ__paslanmaz", "A_ONYUZ__plastik"):
    if d not in DUG: H.bosalt(d)
H.yaz(tmp + ".e2.glb")
SE.sikistir(tmp + ".e2.glb", go)
for f in (tmp, tmp + ".e2.glb"): os.remove(f)
SE.ent_json(go[:-4] + "_ent.json", "A", [(d, DUG[d]) for d in SIRA if d in DUG], H.aralik, A.kapakla_doner, "A/Gövde",
            ("A_GOVDE", "KAIDE_A", "A_ONYUZ"), kayit, ek=dict(karsi_eleman=[p["ad"] for p in PEM_T]))
SE.log("ADIM 33 bitti · %s · %.0f sn" % (go, time.time() - t0))
sys.stdout.flush(); os._exit(0)
