# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 36 · U (ÜST DEPOLAR U_F + U_KE) + F ÜST KABİN ÜRETİM SACI → ANA MODEL (gece 2 · adım 5-entegrasyon 1. tur · 4 Eki 2026 · Claude · YEREL)
python 36_u_sac.py girdi.glb cikti.glb      (zincir: hat3_v9c.glb → hat3_v9d.glb)
Üreteç: h3/h3_u_sac_v1.py (U_F 6 sac · U_KE 5 sac · F üst kabin 10 sac + 6 profil · omega haddeli profil · gömme giriş cebi) · standart yama_v9/sac_standart ·
        mekanizma FHP saplamaları için yama_v9/veri/_bilesen_v8zq.pkl (ADIM5).
GÖVDE (etiketler eski düğümün değeriyle aynı: kat 0 · U_F / U_KE mek 39 U/Gövde · F üst kabin mek 18 F/Gövde):
       U_F_GOVDE__sac + __paslanmaz · U_KE_GOVDE__sac + __paslanmaz (değişir) · U_F_GOVDE__on_seffaf (F kapağı bas-açları) KALIR ·
       F_UST_KABIN__sac (yan / tavan / arka / panjur / taban levhası / kılıf / profiller / davlumbaz bölme duvarı) · F_UST_KABIN__yalitim (taş yünü, görünmez) ·
       F_UST_KABIN__paslanmaz: eski 6 profil bileşeni silinir, hava hortumu kelepçe + askı lamaları (30 küçük bileşen) KALIR, yeni bağlantı elemanları eklenir ·
       F_DAVLUMBAZ__sac: eski bölme duvarı bileşeni silinir (yenisi F_UST_KABIN'de) · ELK_ZINCIR__paslanmaz: eski gömme cep (21 bileşen) silinir
       (yenisi U_F'de 'ust_f_giris_cebi', cep rakorları ELK_ZINCIR__rakor KALIR, deliklerle eş eksen).
KARŞI TARAF (ARAYÜZ): ana pano ayakları, ELK_IC kanalı, fan çerçeveleri, baca flanşı, havalandırma braketi, J1/J2 panel burçları, davlumbaz konsolları +
       filtre çerçevesi, kompresör ayakları, K yağ tankı braketi, gazlı yay braketleri, PD kanalları, hava askıları → FHP saplamanın geçtiği Ø5,5 delik ·
       K üst sacına 2 × PEM SP-M8-1 (dünya x 4100 / 4300 · z −700; U_KE tabanında Ø9 hazır) → yeni K_GOVDE__baglanti düğümüne (K/Gövde)."""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb
import h3_u_sac_v1 as U

gi, go = sys.argv[1:3]
t0 = time.time()
GG = U.kur(log=SE.log)
BIRIMLER = [("U_F_GOVDE", GG["U_F"]), ("U_KE_GOVDE", GG["U_KE"]), ("F_UST_KABIN", GG["F_UST"])]
GOVDE = {b: U.govde_parcalari(g_) for b, g_ in BIRIMLER}
ARAYUZ = {b: SE.dunya_arayuz(g_) for b, g_ in BIRIMLER}
DONER = lambda a: any(g_.kapakla_doner(a) for _, g_ in BIRIMLER)
SE.log("U üreteci: %s · %.1f sn" % (" · ".join("%s %d gövde + %d arayüz" % (b, len(GOVDE[b]), len(ARAYUZ[b])) for b, _ in BIRIMLER), time.time() - t0))
ESKI = ("U_F_GOVDE__sac", "U_F_GOVDE__paslanmaz", "U_KE_GOVDE__", "F_UST_KABIN__sac", "F_UST_KABIN__yalitim", "F_UST_KABIN__paslanmaz")


def hedef(b, g_, p):
    m = g_.mal(p)
    if p.get("tur") == "yalitim": return "F_UST_KABIN__yalitim"
    if m == "on_seffaf": return b + "__on_seffaf"
    if m in ("sac", "kabuk"): return b + "__sac"
    return b + "__paslanmaz"


# ---------------------------------------------------------------- EVRE 1 · eski parça bileşenleri + karşı taraf
g = Glb(gi)
SE.log("EVRE 1 · eski bileşenler (kısmi düğümler)")
SE.bilesen_sil(g, "F_UST_KABIN__paslanmaz", lambda lo, hi: (hi - lo).max() > 300.0, beklenen=6)          # 3 alt profil, ön üst kayıt, ön orta dikme, tavan kirişi
SE.bilesen_sil(g, "F_DAVLUMBAZ__sac", lambda lo, hi: lo[2] > -442.0 and hi[2] < -439.5 and hi[0] - lo[0] > 1000.0, beklenen=1)   # bölme duvarı
SE.bilesen_sil(g, "ELK_ZINCIR__paslanmaz", lambda lo, hi: lo[0] >= 3926.0 and hi[0] <= 3983.5 and lo[1] >= 2081.0 and hi[1] <= 2167.0 and lo[2] >= -830.5 and hi[2] <= -789.5,
               beklenen=21)                                                                              # gömme cep (4 duvar + taban)
PEM_K = []
for x in (4100.0, 4300.0):
    p, d, bad, y1, t = SE.pem_yeri(g, "pem_sp_m8_k_ust_%d" % x, x, -700.0, ["K_GOVDE__kabuk", "K_GOVDE__sac"], 1862.05, 1700.0)
    if p is None: SE.log("  UYARI K üst sacı bulunamadı x %.0f" % x); continue
    SE.log("  PEM SP-M8 %s · %s üst yüz y %.2f · sac %.2f" % (p["ad"], bad, y1, t)); PEM_K.append((d, p))
K = SE.Karsi(g, haric_onek=ESKI)
TUM_AR = [p for b, _ in BIRIMLER for p in ARAYUZ[b]]
SE.log("EVRE 1 · saplama boyları (yalnız kendi karşı parçasından geçer)")
kisa = K.saplama_ayarla(TUM_AR)
ARAYUZ = {b: [q for q in TUM_AR if q.get("birim") == b] for b, _ in BIRIMLER}
assert sum(len(v) for v in ARAYUZ.values()) == len(TUM_AR), "arayüz birimi"
SE.log("EVRE 1 · karşı taraf delikleri (%d arayüz + %d PEM)" % (len(TUM_AR), len(PEM_K)))
kayit = K.delik_ac(TUM_AR + [p for _, p in PEM_K])
tmp = go + ".e1.glb"; g.kaydet(tmp); del g, K

# ---------------------------------------------------------------- EVRE 2 · gövde
SE.log("EVRE 2 · gövde düğümleri")
H = SE.Ham(tmp)
DUG = {}
for b, g_ in BIRIMLER:
    for p in GOVDE[b]: DUG.setdefault(hedef(b, g_, p), []).append(p)
    DUG[b + "__paslanmaz"] = DUG.get(b + "__paslanmaz", []) + ARAYUZ[b]
EKLE = ("F_UST_KABIN__paslanmaz", "U_F_GOVDE__on_seffaf", "U_KE_GOVDE__on_seffaf")    # mevcut (kalan) üçgenler korunur
SIRA = ["U_F_GOVDE__sac", "U_F_GOVDE__paslanmaz", "U_F_GOVDE__on_seffaf", "U_KE_GOVDE__sac", "U_KE_GOVDE__paslanmaz", "U_KE_GOVDE__on_seffaf",
        "F_UST_KABIN__sac", "F_UST_KABIN__yalitim", "F_UST_KABIN__paslanmaz"]
for d in sorted(DUG): assert d in SIRA, d
ET = {d: H.etiket(d) for d in SIRA}
VARS = {"U_F_GOVDE": (0, 39), "U_KE_GOVDE": (0, 39), "F_UST_KABIN": (0, 18)}
for d in SIRA:
    if d not in DUG: continue
    kat, mek = ET[d] if ET[d][0] is not None else VARS[d.split("__")[0]]
    H.koy(d, DUG[d], kat=kat, mek=mek, kpk_fn=DONER, ekle=d in EKLE)
KDUG = []
if PEM_K:                                                                  # K üst sacı PEM'leri ayrı bağlantı düğümüne (K/Gövde)
    H.koy("K_GOVDE__baglanti", [p for _, p in PEM_K], kat=0, mek=24, sablon="K_GOVDE__celik"); KDUG.append(("K_GOVDE__baglanti", [p for _, p in PEM_K]))
H.yaz(tmp + ".e2.glb")
SE.sikistir(tmp + ".e2.glb", go)
for f in (tmp, tmp + ".e2.glb"): os.remove(f)
SE.ent_json(go[:-4] + "_ent.json", "U", [(d, DUG[d]) for d in SIRA if d in DUG] + KDUG, H.aralik, DONER, "U/Gövde + F/Gövde",
            ("U_F_GOVDE", "U_KE_GOVDE", "F_UST_KABIN"), kayit, ek=dict(saplama_kisaltma=kisa, karsi_eleman=[p["ad"] for _, p in PEM_K],
            mek_saplama={b: len(getattr(g_, "MEK_SAPLAMA", [])) for b, g_ in BIRIMLER}))
SE.log("ADIM 36 bitti · %s · %.0f sn" % (go, time.time() - t0))
sys.stdout.flush(); os._exit(0)
