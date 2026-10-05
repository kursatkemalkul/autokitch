# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 35 · E (KUTU KATLAMA) ÜRETİM SACI → ANA MODEL (gece 2 · adım 5-entegrasyon 1. tur · 4 Eki 2026 · Claude · YEREL)
python 35_e_sac.py girdi.glb cikti.glb      (zincir: hat3_v9b.glb → hat3_v9c.glb)
Üreteç: h3/h3_e_sac_v1.py (64 sac + 10 profil · kaynaklı ön kasa, çift cidarlı 4 kapak, şarjör yan kapısı, kaynaklı kaide) · standart yama_v9/sac_standart ·
        mekanizma FHP saplamaları için v8zq bileşen kutuları yama_v9/veri/_bilesen_v8zq.pkl (ADIM5).
GÖVDE (etiketler eski düğümün değeriyle aynı: kat 0 GOVDE / E_MODULER kat 1 · mek 31 E/Gövde):
       E_GOVDE__kabuk (sol / sağ / arka / üst kabuk sacı) · E_GOVDE__sac (taban, ön kasa profilleri, kulak / köşebent, şarjör kapısı, kaynaklar) ·
       E_GOVDE__celik (ayaklar, menteşe gövdeleri, PEM / vida / pul / somun + FHP saplamalar + arayüz cıvataları) · E_GOVDE__plastik (bas-açlar) ·
       E_GOVDE__on_seffaf (kapakla dönen her şey · kpk) · E_MODULER__paslanmaz (kaynaklı kaide: ray + kayıt + tapa + somun + vida).
KARŞI TARAF (ARAYÜZ): mekanizma / elektrik parçalarına (şarjör eşiği + köşebentler, besleyici askıları, J3 panel burçları, UHMW kılavuzlar,
       kalıp tablası, pano plakası burçları, köprü, sensör braketleri, piston askıları, kablo kanalları, robot çöpü kızağı) FHP saplamanın
       geçtiği Ø5,5 / Ø6,6 delik · U_KE ↔ E 3 × M8 cıvatası U_KE tabanından (adım 36'da yeni U_KE tabanında Ø9 hazır)."""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb
import h3_e_sac_v1 as E

gi, go = sys.argv[1:3]
t0 = time.time()
g_ = E.kur(log=SE.log)
GOVDE = E.govde_parcalari(g_)
ARAYUZ = SE.dunya_arayuz(g_)
SE.log("E üreteci: %d gövde parçası · %d arayüz elemanı · %.1f sn" % (len(GOVDE), len(ARAYUZ), time.time() - t0))
ESKI = ("E_GOVDE__", "E_MODULER__")


def hedef(p):
    m = g_.mal(p); ad = p["ad"]
    if m == "on_seffaf": return "E_GOVDE__on_seffaf"
    if ad.startswith("kaide_e_"): return "E_MODULER__paslanmaz"
    if m == "siyah": return "E_GOVDE__plastik"
    if m == "kabuk": return "E_GOVDE__kabuk"
    if m == "sac": return "E_GOVDE__sac"
    if m == "conta": return "E_GOVDE__conta"
    return "E_GOVDE__celik"


# ---------------------------------------------------------------- EVRE 1 · karşı taraf
g = Glb(gi)
K = SE.Karsi(g, haric_onek=ESKI)
SE.log("EVRE 1 · saplama boyları (yalnız kendi karşı parçasından geçer)")
kisa = K.saplama_ayarla(ARAYUZ)
SE.log("EVRE 1 · karşı taraf delikleri (%d arayüz elemanı)" % len(ARAYUZ))
kayit = K.delik_ac(ARAYUZ)
tmp = go + ".e1.glb"; g.kaydet(tmp); del g, K

# ---------------------------------------------------------------- EVRE 2 · gövde
SE.log("EVRE 2 · gövde düğümleri")
H = SE.Ham(tmp)
DUG = {}
for p in GOVDE: DUG.setdefault(hedef(p), []).append(p)
DUG["E_GOVDE__celik"] = DUG.get("E_GOVDE__celik", []) + ARAYUZ
SIRA = ["E_GOVDE__kabuk", "E_GOVDE__sac", "E_GOVDE__celik", "E_GOVDE__plastik", "E_GOVDE__on_seffaf", "E_GOVDE__conta", "E_MODULER__paslanmaz"]
for d in sorted(DUG): assert d in SIRA, d
ET = {d: H.etiket(d) for d in SIRA}
for d in SIRA:
    if d in DUG:
        kat, mek = ET[d] if ET[d][0] is not None else (0, 31)
        H.koy(d, DUG[d], kat=kat, mek=mek, kpk_fn=g_.kapakla_doner, sablon={"E_GOVDE__conta": "K_GOVDE__conta"}.get(d))
    else:
        H.bosalt(d)
H.yaz(tmp + ".e2.glb")
SE.sikistir(tmp + ".e2.glb", go)
for f in (tmp, tmp + ".e2.glb"): os.remove(f)
SE.ent_json(go[:-4] + "_ent.json", "E", [(d, DUG[d]) for d in SIRA if d in DUG], H.aralik, g_.kapakla_doner, "E/Gövde",
            ("E_GOVDE", "E_MODULER"), kayit, ek=dict(saplama_kisaltma=kisa,mek_saplama=len(getattr(g_, "MEK_SAPLAMA", [])), mek_atla=[list(map(str, a)) for a in getattr(g_, "MEK_ATLA", [])]))
SE.log("ADIM 35 bitti · %s · %.0f sn" % (go, time.time() - t0))
sys.stdout.flush(); os._exit(0)
