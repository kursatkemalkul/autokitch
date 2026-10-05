# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 38 · F ÜRETİM SACI (ön kapaklar + davlumbaz atış kanalı + baca) → ANA MODEL (gece 2 · adım 5-entegrasyon 2. tur · 4 Eki 2026 · Claude · YEREL)
python 38_f_sac.py girdi.glb cikti.glb      (zincir: hat3_v9e.glb → hat3_v9f.glb)
Üreteç: h3/h3_f_sac_v1.py (22 sac · kapak dış tava 1,5 + haddeli omega + kayıtlar · atış kanalı iki L · baca iç kanal 1,5 + dış kılıf 0,8 + taş yünü + üst flanş).
F üst kabin yan / arka / tavan / taban / profiller adım 36'da (h3_u_sac_v1). TP10 fırın (satın alınan) DOKUNULMAZ.
ESKİ (v8zq kutusuyla): F_UST_KAPAK__on_seffaf__KAPAK_F_SOL / _SAG [0,1,2,3,5,8] (menteşe gövde + kanat, gazlı yay braketleri KALIR) · F_DAVLUMBAZ__sac [1] (atış kanalı) ·
      U_F_BACA__sac / __yalitim_gorunur / __paslanmaz tümü.
GÖVDE: kapak parçaları → KAPAK_F_SOL / _SAG düğümlerine (kpk, mevcutlara eklenir) · davlumbaz_* → F_DAVLUMBAZ__sac (eklenir) · baca_* → U_F_BACA__sac / __paslanmaz /
      __conta (yeni) · yalitim_baca → U_F_BACA__yalitim (yeni, taş yünü görünmez; eski 'yalıtım görünür' boşalır). Etiketler eski düğümün değeriyle.
KARŞI TARAF: U_F tavanına 8 × Ø6,6 (baca flanşı M6 cıvataları) · F sol yan 4 × Ø9 (adım 37'de TOPPING cıvatalarının ISO 273 geçiş deliğiyle açıldı; burada tekrar kesilmez) ·
      menteşe kanadında Ø5,5 (menteşe vidaları)."""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb
import h3_f_sac_v1 as F

gi, go = sys.argv[1:3]
t0 = time.time()
GOVDE = F.dunya_listesi(F.govde_parcalari())
ARAYUZ = F.dunya_listesi(F.G.ARAYUZ)
YALNIZ_DELIK = [p for p in ARAYUZ if p.get("std") == "ISO 273 orta"]        # F sol yan Ø9 (TOPPING ↔ F) — parça değil, yalnız kesici
PARCA_AR = [p for p in ARAYUZ if p.get("std") != "ISO 273 orta"]
SE.log("F üreteci: %d gövde parçası · %d arayüz (%d yalnız delik) · %.1f sn" % (len(GOVDE), len(ARAYUZ), len(YALNIZ_DELIK), time.time() - t0))

g = Glb(gi)
SE.log("EVRE 1 · eski F parçaları")
SE.degisen_sil(g, os.path.join(SE.KOK, "hat3_v8zq.glb"), F.DEGISEN)
K = SE.Karsi(g, haric_onek=("F_GOVDE__", "U_F_BACA__"), acik_dene=True)
SE.log("EVRE 1 · karşı taraf delikleri (%d arayüz)" % len(PARCA_AR))
kayit = K.delik_ac(PARCA_AR)                                               # F sol yan Ø9: adım 37 TOPPING cıvatalarının geçiş deliğiyle zaten açık (tekrar kesilmez — cıvatayı da keserdi)
tmp = go + ".e1.glb"; g.kaydet(tmp); del g, K

SE.log("EVRE 2 · gövde düğümleri")
H = SE.Ham(tmp)


def hedef(p):
    ad = p["ad"]; m = F._mal(p)
    if ad.startswith("onyuz_kapak_F_sol"): return "F_UST_KAPAK__on_seffaf__KAPAK_F_SOL"
    if ad.startswith("onyuz_kapak_F_sag"): return "F_UST_KAPAK__on_seffaf__KAPAK_F_SAG"
    if ad.startswith("davlumbaz_"): return "F_DAVLUMBAZ__sac"
    if m == "yalitim": return "U_F_BACA__yalitim"
    if m == "conta": return "U_F_BACA__conta"
    if m == "sac": return "U_F_BACA__sac"
    return "U_F_BACA__paslanmaz"


# baca flanşı M6 cıvatalarının ucu taş yünü sargısına giriyor → yalıtımda cıvata yuvası (cıvata katısı kadar, köpük / yün yerinde kesilir)
civ = [SE.sekil(p) for p in PARCA_AR if p["ad"].startswith("arayuz_baca_flans")]
for i, p in enumerate(GOVDE):
    if F._mal(p) == "yalitim" and civ:
        sh = SE.sekil(p); v0 = sh.Volume(); sh = sh.cut(*civ).clean()
        if sh.ShapeType() != "Solid" and len(sh.Solids()) == 1: sh = sh.Solids()[0]
        q = dict(p); q["sh"] = sh; q.pop("wp", None); GOVDE[i] = q
        SE.log("  yalıtım cıvata yuvası: %s · −%.1f mm³" % (p["ad"], v0 - sh.Volume()))
DUG = {}
for p in GOVDE + PARCA_AR: DUG.setdefault(hedef(p), []).append(p)
EKLE = ("F_UST_KAPAK__on_seffaf__KAPAK_F_SOL", "F_UST_KAPAK__on_seffaf__KAPAK_F_SAG", "F_DAVLUMBAZ__sac")
SABLON = {"U_F_BACA__yalitim": "F_UST_KABIN__yalitim", "U_F_BACA__conta": "F_UST_KABIN__conta"}
SIRA = list(EKLE) + ["U_F_BACA__sac", "U_F_BACA__paslanmaz", "U_F_BACA__conta", "U_F_BACA__yalitim"]
for d in sorted(DUG): assert d in SIRA, d
ET = {d: H.etiket(d) for d in SIRA}
for d in SIRA:
    if d in DUG:
        kat, mek = ET[d] if ET[d][0] is not None else ET["U_F_BACA__sac"]
        H.koy(d, DUG[d], kat=kat, mek=mek, kpk_fn=F.kapakla_doner, ekle=d in EKLE, sablon=SABLON.get(d))
    elif d.startswith("U_F_BACA"): H.bosalt(d)
if "U_F_BACA__yalitim" in DUG: H.bosalt("U_F_BACA__yalitim_gorunur")
H.yaz(tmp + ".e2.glb")
SE.sikistir(tmp + ".e2.glb", go)
for f in (tmp, tmp + ".e2.glb"): os.remove(f)
SE.ent_json(go[:-4] + "_ent.json", "F", [(d, DUG[d]) for d in SIRA if d in DUG], H.aralik, F.kapakla_doner, "F/Gövde",
            ("F_UST_KAPAK", "U_F_BACA"), kayit, ek=dict(yalniz_delik=[p["ad"] for p in YALNIZ_DELIK]))
SE.log("ADIM 38 bitti · %s · %.0f sn" % (go, time.time() - t0))
sys.stdout.flush(); os._exit(0)
