# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 37 · TOPPING ÜRETİM SACI → ANA MODEL (gece 2 · adım 5-entegrasyon 2. tur · 4 Eki 2026 · Claude · YEREL)
python 37_topping_sac.py girdi.glb cikti.glb      (zincir: hat3_v9d.glb → hat3_v9e.glb)
Üreteç: h3/h3_topping_sac_v1.py (43 sac + 7 profil + 2 PU · kaynaklı dış kabuk + PU sandviç · sökülür arka servis sacı (17 × DIN 7991 M5 havşa başlı,
        çökertme havşa — 4 Eki düzeltmesi: bombe başlar zarftan 2,6 mm taşıyordu) · soğuk oda astar / raf / eşik / dil kanalları · kaide).
ESKİ: üretecin DEGISEN tablosundaki v8zq bileşenleri (TOPPING_MODUL__sac / __paslanmaz / __pu) v8zq'daki KUTULARIYLA bulunup silinir (önceki adımlar bileşen
      numaralarını kaydırmış olabilir) · KAIDE_C__paslanmaz tümü · adım 33'te TOPPING_MODUL__paslanmaz'a eklenen 4 PEM SP-M8 (A ↔ TOPPING) silinir — artık
      TOPPING üretecinin sol yan sacında.
GÖVDE (YENİ birim TOPPING_GOVDE · mek 7 TOPPING/Gövde · kat 0): __kabuk (dis_*) · __sac · __cerceve (430 ön çerçeve) · __pu (görünmez) · __paslanmaz (PEM / vida / pul +
      arayüz cıvataları) · __conta · __pom (kaşar / sucuk düşme kovanı) · __koyu · kaide parçaları → KAIDE_C__paslanmaz (kat 1).
KARŞI TARAF: F sol yan sacı 4 × Ø9 (biri U_F sol sacında) · tabla rayı tabanı Ø6,6 · B dış tavanı Ø9 + B_MODULER üst kirişine 4 × M8 kapalı perçin somun
      (TOPPING kaidesi → B) · mekanizma / elektrik / hava parçalarına FHP delikleri (saplama yalnız kendi karşı parçasından; engel varsa kısaltılır / çıkarılır)."""
import os, sys, time, re
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb
import h3_topping_sac_v2 as T          # v2 (4 Eki · Kemal onayı): dimple + bükümlü iç sac + perçin + PU levha + evaporatör ayakları + kanal deliği
import h3_a_sac_v1 as A
import h3_sac_v1 as S

gi, go = sys.argv[1:3]
t0 = time.time()
GOVDE = T.dunya_listesi(T.govde_parcalari())
ARAYUZ = T.dunya_listesi(T.G.ARAYUZ)
A.kur(log=lambda *a: None)
# tabla rayı → kaide plakası M6 (x 1750 / 2250): bu eksenlerde ray tabanı yok → ADIM 8'den beri üreteç bunları hiç üretmez (h3_topping_sac_v1.RAY_M6 = []);
# aşağıdaki süzgeç boş kalır (güvenlik ağı)
ATLA = [p["ad"] for p in ARAYUZ if p["ad"] in ("arayuz_kaide_M6_2", "arayuz_kaide_M6_3", "arayuz_kaide_M6_4", "arayuz_kaide_M6_5")]
ARAYUZ = [p for p in ARAYUZ if p["ad"] not in ATLA]
# gövdeden geçen kendi cıvataları (kaide ↔ gövde M6 teknik ön perdeden) + A'dan gelen M8 cıvata uçları (PU + köpük kapağı) → gövde katısında yuva
A_CIV = [q for q in A.dunya_listesi(A.G.ARAYUZ) if q["ad"].startswith("arayuz_m8_T_") and not q["ad"].endswith(("_pem", "_pul"))]
YUVA = [p for p in ARAYUZ if SE.vida_mi(p) and (p.get("meta") or {}).get("pem_tip") != "FHP"] + A_CIV
GOVDE = SE.kes_tam(GOVDE, YUVA)
SE.log("TOPPING üreteci: %d gövde parçası · %d arayüz elemanı · %.1f sn" % (len(GOVDE), len(ARAYUZ), time.time() - t0))
ESKI = ("TOPPING_GOVDE__", "KAIDE_C__")

g = Glb(gi)
SE.log("EVRE 1 · eski TOPPING gövde bileşenleri")
SE.degisen_sil(g, os.path.join(SE.KOK, "hat3_v8zq.glb"), {k: v for k, v in T.DEGISEN.items() if k != "KAIDE_C__paslanmaz"})
pem33 = []
for p in A.dunya_listesi([q for q in A.G.ARAYUZ if q["ad"].endswith("_pem")]):
    b = SE.sekil(p).BoundingBox(); P = SE.ucgen(SE.sekil(p)).reshape(-1, 3); pem33.append((P.min(0), P.max(0)))
SE.kutu_sil(g, "TOPPING_MODUL__paslanmaz", pem33, tol=0.05)


def percin(ad, x, z, dl, y_ust=788.0, y_alt=600.0, kayma=6.0):
    for d in dl:
        g.bilesen(d, 0)
        for b in g._bc[d]:
            if not (b["lo"][0] - 0.1 <= x <= b["hi"][0] + 0.1 and b["lo"][2] - 0.1 <= z <= b["hi"][2] + 0.1 and b["hi"][1] <= y_ust and b["lo"][1] >= y_alt - 1): continue
            P = np.concatenate([q["X"][q["T"][t]] for q, t in b["parca"]])
            ys = SE.isin_y(P, x + kayma, z, y_ust, y_alt)
            if len(ys) < 2: continue
            y1, y2 = ys[-1], ys[-2]
            p, c = S.percin_somun("M8", y1 - y2, (x, y1, z), (0, -1.0, 0), ad=ad, birim="B_GOVDE", kapali=True)
            return p, d, "%s[%d]" % (d, b["no"]), y1, y1 - y2
    return None, None, None, None, None


PER = []
for p in ARAYUZ:
    m = re.match(r"arayuz_kb_(\d+)_(\d+)$", p["ad"])
    if not m: continue
    x, z = float(m.group(1)), -float(m.group(2))
    q, d, bad, y1, t = percin("percin_somun_tb_%s_%s" % m.groups(), x, z, ["B_MODULER__paslanmaz", "B_TASIYICI__celik"])
    if q is None: SE.log("  UYARI perçin somun yeri bulunamadı: x %.0f z %.0f" % (x, z)); continue
    SE.log("  perçin somun %-26s %s üst yüz y %.2f · duvar %.2f" % (q["ad"], bad, y1, t)); PER.append((d, q))
K = SE.Karsi(g, haric_onek=ESKI, acik_dene=True)
SE.log("EVRE 1 · saplama boyları")
kisa = K.saplama_ayarla(ARAYUZ)
SE.log("EVRE 1 · karşı taraf delikleri (%d arayüz + %d perçin somun)" % (len(ARAYUZ), len(PER)))
kayit = K.delik_ac(ARAYUZ + [q for _, q in PER])
tmp = go + ".e1.glb"; g.kaydet(tmp); del g, K

SE.log("EVRE 2 · gövde düğümleri")
H = SE.Ham(tmp)


def hedef(p):
    m = T._mal(p)
    if p["ad"].startswith("kaide_"): return "KAIDE_C__paslanmaz"
    return {"pu": "TOPPING_GOVDE__pu", "kabuk": "TOPPING_GOVDE__kabuk", "cerceve": "TOPPING_GOVDE__cerceve", "sac": "TOPPING_GOVDE__sac",
            "conta": "TOPPING_GOVDE__conta", "pom": "TOPPING_GOVDE__pom", "koyu": "TOPPING_GOVDE__koyu"}.get(m, "TOPPING_GOVDE__paslanmaz")


DUG = {}
for p in GOVDE: DUG.setdefault(hedef(p), []).append(p)
DUG["TOPPING_GOVDE__paslanmaz"] = DUG.get("TOPPING_GOVDE__paslanmaz", []) + ARAYUZ
SABLON = {"TOPPING_GOVDE__pu": "TOPPING_MODUL__pu", "TOPPING_GOVDE__kabuk": "TOPPING_MODUL__sac", "TOPPING_GOVDE__cerceve": "TOPPING_MODUL__sac",
          "TOPPING_GOVDE__sac": "TOPPING_MODUL__sac", "TOPPING_GOVDE__conta": "TOPPING_MODUL__conta", "TOPPING_GOVDE__pom": "TOPPING_MODUL__pom",
          "TOPPING_GOVDE__koyu": "TOPPING_MODUL__koyu", "TOPPING_GOVDE__paslanmaz": "TOPPING_MODUL__paslanmaz"}
SIRA = ["TOPPING_GOVDE__kabuk", "TOPPING_GOVDE__sac", "TOPPING_GOVDE__cerceve", "TOPPING_GOVDE__pu", "TOPPING_GOVDE__paslanmaz", "TOPPING_GOVDE__conta",
        "TOPPING_GOVDE__pom", "TOPPING_GOVDE__koyu", "KAIDE_C__paslanmaz"]
for d in sorted(DUG): assert d in SIRA, d
for d in SIRA:
    if d in DUG: H.koy(d, DUG[d], kat=1 if d.startswith("KAIDE_C") else 0, mek=7, sablon=SABLON.get(d))
    elif d == "KAIDE_C__paslanmaz": H.bosalt(d)
KDUG = []
for d in sorted(set(d for d, _ in PER)):                                  # perçin somunlar B'nin bağlantı düğümüne (adım 34'te kuruldu → eklenir)
    kd = d.split("__")[0] + "__baglanti"; L_ = [q for d_, q in PER if d_ == d]
    H.koy(kd, L_, kat=0, mek=2, sablon=d, ekle=H.dugum(kd) is not None and "mesh" in H.dugum(kd)); KDUG.append((kd, L_))
H.yaz(tmp + ".e2.glb")
SE.sikistir(tmp + ".e2.glb", go)
for f in (tmp, tmp + ".e2.glb"): os.remove(f)
SE.ent_json(go[:-4] + "_ent.json", "TOPPING", [(d, DUG[d]) for d in SIRA if d in DUG] + KDUG, H.aralik, lambda a: False, "TOPPING/Gövde",
            ("TOPPING_GOVDE", "KAIDE_C"), kayit, ek=dict(saplama_kisaltma=kisa, karsi_eleman=[q["ad"] for _, q in PER], atlanan_arayuz=ATLA))
SE.log("ADIM 37 bitti · %s · %.0f sn" % (go, time.time() - t0))
sys.stdout.flush(); os._exit(0)
