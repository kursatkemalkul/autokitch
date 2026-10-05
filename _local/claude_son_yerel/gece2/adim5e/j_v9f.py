# -*- coding: utf-8 -*-
"""mekanizma_v3_8.json + parca_kutulari.json → v9f (adım 5-entegrasyon: A, B, E, U, TOPPING, F üretim sacı).
python j_v9f.py mek.json pk.json hat3_v8zq.glb cikti_klasoru ent33.json … ent38.json"""
import sys, os, json
import numpy as np
mj, pj, v8, cik = sys.argv[1:5]; EJ = sys.argv[5:]
H3 = "C:/Users/Kemal/Desktop/Kemal/WEBSİTE/AUTOKITCH_COORDINATION/worktrees/claude-hat3-v8/arastirma/_uretec/h3"
os.environ.setdefault("AUTOKITCH_SAC_STANDART", H3 + "/yama_v9/sac_standart")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "is")); sys.path.insert(0, H3)
import govde_denetim_dogru as G
import h3_topping_sac_v1 as T, h3_f_sac_v1 as FF
M = json.load(open(mj, encoding="utf-8")); PK = json.load(open(pj, encoding="utf-8"))
E = [json.load(open(x, encoding="utf-8")) for x in EJ]
MEK = {"A_GOVDE": "A/Gövde", "KAIDE_A": "A/Gövde", "A_ONYUZ": "A/Gövde", "B_KASA": "B/Gövde", "E_GOVDE": "E/Gövde", "E_MODULER": "E/Gövde",
       "U_F_GOVDE": "U/Gövde", "U_KE_GOVDE": "U/Gövde", "F_UST_KABIN": "F/Gövde", "TOPPING_GOVDE": "TOPPING/Gövde", "KAIDE_C": "TOPPING/Gövde",
       "F_UST_KAPAK": "F/Gövde", "F_DAVLUMBAZ": "F/Davlumbaz", "U_F_BACA": "F/Davlumbaz"}
F_ESKI = {"f_ust_yan_sol", "f_ust_yan_sag", "f_ust_tavan_sac", "f_ust_arka_sac", "f_ust_panjur_lamelleri_0", "f_ust_panjur_lamelleri_1", "f_ust_alt_profil_on",
          "f_ust_alt_profil_orta", "f_ust_alt_profil_arka", "f_ust_taban_levhasi", "f_ust_taban_yalitimi_on", "f_ust_taban_yalitimi_arka",
          "f_ust_taban_yalitim_kilifi_on", "f_ust_taban_yalitim_kilifi_arka", "f_ust_taban_rakor_kovani", "onyuz_f_ust_ust_kayit", "onyuz_f_ust_dikme_0",
          "f_davlumbaz_bolme_duvari", "f_ust_tavan_kirisi", "onyuz_f_ust_kayit", "onyuz_f_ust_kayit_takozu_0", "onyuz_f_ust_kayit_takozu_1", "onyuz_f_ust_kayit_takozu_2"}
D8 = G.glb_oku(v8); SILK = {}
for deg in (T.DEGISEN, FF.DEGISEN):
    for d, sec in deg.items():
        B0 = G.bilesenler(d, D8[d]); b = d.split("__")[0]
        SILK.setdefault(b, []).extend([(x.lo, x.hi) for x in (B0 if sec == "hepsi" else [B0[i] for i in sec])])


def kalir(b, e):
    ad, kpk = e[0], e[1]
    if b in ("A_GOVDE", "KAIDE_A", "A_ONYUZ", "U_A_GOVDE", "E_GOVDE", "E_MODULER", "U_KE_GOVDE", "KAIDE_C", "U_F_BACA"): return False
    if b == "B_KASA": return ad.startswith("ayak_")
    if b == "U_F_GOVDE": return bool(kpk)
    if b == "F_UST_KABIN": return ad not in F_ESKI
    if b in SILK:
        lo = np.array(e[2::2], float); hi = np.array(e[3::2], float)
        return not any(np.all(np.abs(lo - a) < 0.6) and np.all(np.abs(hi - c) < 0.6) for a, c in SILK[b])
    return True


cik_say = {}
for b in list(PK["parca"]):
    if b not in MEK and b != "U_A_GOVDE" and b not in SILK: continue
    L0 = PK["parca"][b]; L1 = [e for e in L0 if kalir(b, e)]
    cik_say[b] = len(L0) - len(L1); PK["parca"][b] = L1
eklenen = {}
for e in E:
    for ad, p in e["parca"].items():
        b = p["dugum"].split("__")[0]
        PK["parca"].setdefault(b, []).append([ad, int(p["kpk"])] + [round(v, 1) for v in p["kutu"]])
        eklenen[b] = eklenen.get(b, 0) + 1
kalan = set((b, e[0]) for b, L in PK["parca"].items() for e in L)
for k in list(M["parca"]):
    b, _, ad = k.partition("|")
    if (b in MEK or b in SILK) and (b, ad) not in kalan: del M["parca"][k]
for e in E:
    for ad, p in e["parca"].items():
        b = p["dugum"].split("__")[0]
        M["parca"]["%s|%s" % (b, ad)] = MEK.get(b, "?")
M["birim"].setdefault("E_MODULER", "E/Gövde"); M["birim"].setdefault("TOPPING_GOVDE", "TOPPING/Gövde")
PK["birim"].setdefault("TOPPING_GOVDE", {"ad": "TOPPING gövdesi · ÜRETİM SACI (h3_topping_sac_v1): kaynaklı dış kabuk + PU sandviç, sökülür arka servis sacı (havşa başlı vida), soğuk oda astar / raf / eşik", "mal": "MC_TOPPING_GOVDE"})
M["glb"] = "hat3_v8.glb (v9f)"
M["surum"] = M["surum"] + (" · v9f (4 Eki · adım 5-entegrasyon): A, B, E, U (+ F üst kabin), TOPPING, F (kapak / atış kanalı / baca) gövdeleri ÜRETİM SACI "
                           "(h3_a/b/e/u/topping/f_sac_v1; bükümlü sac + PEM / vida, kaynaklı kaide / iskelet, çift cidarlı kapaklar) · karşı tarafta delikler "
                           "(açıcı flanşı, ray tabanı, çekmece rayı havşaları, mekanizma FHP delikleri), B_MODULER / B_TASIYICI perçin somunları, K üst sacına 2 PEM SP-M8 · zincir adım 33–38")
os.makedirs(cik, exist_ok=True)
json.dump(M, open(os.path.join(cik, "mekanizma_v3_8.json"), "w", encoding="utf-8"), ensure_ascii=False)
json.dump(PK, open(os.path.join(cik, "parca_kutulari.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("pk çıkan", cik_say, "· eklenen", eklenen, "· mek parca", len(M["parca"]))
os._exit(0)
