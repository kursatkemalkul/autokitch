# -*- coding: utf-8 -*-
"""mekanizma_v3_8.json + parca_kutulari.json -> v8zn. python j_e6.py mek_eski.json pk_eski.json cache mek_yeni.json pk_yeni.json"""
import sys, json, numpy as np
sys.path.insert(0, r"@@KOK_W@@\elk5")
sys.path.insert(0, r"@@KOK_W@@\elk4")
ej, pj, d, yj, ypj = sys.argv[1:6]
J = json.load(open(ej, encoding="utf-8"))
D = np.load(d + "/m8_onbellek.npz"); PJ = json.load(open(d + "/m8_parca.json", encoding="utf-8"))
KOD = [m["kod"] for m in PJ["MEK"]]
T = np.stack([D["A"], D["B"], D["C"]], 1); mek = D["mek"]; K = {}
for i, k in enumerate(KOD):
    m = mek == i
    if not m.any(): continue
    Q = T[m].reshape(-1, 3); lo = Q.min(0) / 1000; hi = Q.max(0) / 1000
    K[k] = [round(float(x), 4) for x in (lo[0], hi[0], lo[1], hi[1], lo[2], hi[2])]
J["kutu"] = {**{k: v for k, v in J.get("kutu", {}).items() if k not in K}, **K}
SIL = ("ELK_ANA_PANO_UF|ana_pano_rakor_bina_besleme_5G6_M32", "ELK_ANA_PANO_UF|ana_pano_rakor_modem_Cat6A_M20", "ELK_ANA_PANO_UF|ana_pano_rakor_fan_24V_M20",
       "ELK_ANA_PANO_UF|ana_salter_kapi_tipi_doner_kollu_63A_4P_kilitlenebilir")
P = {k: v for k, v in J["parca"].items() if k not in SIL}
n0 = len(J["parca"])
import qr5, k5, b5, p5
for sp in (qr5, k5, b5, p5):
    for k in sp.KAN: P["ELK_IC|ic_kanal_%s_%s" % (sp.IST, k["ad"])] = ("Elektrik/Ana pano" if sp.IST == "U" else sp.IST + "/Elektrik")
P["ELK_ANA_PANO_UF|ana_salter_ABB_OT40F4_4P_40A_DIN_rayinda"] = "Elektrik/Ana pano"
P["ELK_ANA_PANO_UF|ana_salter_kapi_kolu_ABB_OHYS2AJ_IP65_kilitlenebilir"] = "Elektrik/Ana pano"
P["ELK_ANA_PANO_UF|ana_salter_mili_ABB_OXP6X_6mm_kare"] = "Elektrik/Ana pano"
P["ELK_ANA_PANO_UF|montaj_plakasi_lastik_gecit_bina_kablosu"] = "Elektrik/Ana pano"
P["ELK_ANA_PANO_UF|kapak_kor_tapa_eski_salter_deligi"] = "Elektrik/Ana pano"
P["ELK_ZINCIR|pano_arka_dik_kanal_V1_ust_kapagi"] = "F/Elektrik"
P["ELK_QR_KABLO|musteri_paneli_kablolari_5_adet"] = "QR/Elektrik"
for v in P.values(): assert v in KOD, v
J["parca"] = P
if isinstance(J.get("kapsam"), dict): J["kapsam"]["parca"] = len(P)
J["glb"] = "hat3_v8.glb (v8zn)"
J["surum"] = J["surum"] + (" · v8zn iç kablolama son tur: QR göz arkası 3 dik kapaklı kanal + üst toplayıcı + müşteri paneli kanalı; K sağ duvar sensörleri itici süpürme bandı dışından;"
                           " B fan + soğutma beslemesi kanalda; ana pano kabloları arka rakorlardan dik kapaklı kanala (güç | bilgi ayrı bölme) → U tabanı → F arka iç kanalı;"
                           " ana şalter ABB OT40F4 DIN rayında, kapakta OHYS2AJ kol + OXP6X mil; pano yan rakorları kalktı")
json.dump(J, open(yj, "w", encoding="utf-8"), ensure_ascii=False)
print("mekanizma: kutu", len(K), "· parca", n0, "->", len(P))
# parca_kutulari
PK = json.load(open(pj, encoding="utf-8"))
L = [e for e in PK["parca"]["ELK_ANA_PANO_UF"] if not e[0].startswith("ana_pano_rakor_")]
xc, yc = 3612.0, 2107.0
L += [["ana_salter_ABB_OT40F4_DIN", 0, xc - 24, xc + 24, yc - 28, yc + 28, -273.0, -205.0],
      ["ana_salter_mili_OXP6X", 0, xc - 3, xc + 3, yc - 3, yc + 3, -205.0, -87.0],
      ["ana_salter_kolu_OHYS2AJ", 0, xc - 32.5, xc + 32.5, yc - 32.5, yc + 32.5, -87.0, -39.0],
      ["montaj_plakasi_lastik_gecit", 0, xc - 13, xc + 13, 2133.0, 2159.0, -284.0, -279.0],
      ["kapak_kor_tapa", 0, 3736.5, 3753.5, 2101.5, 2118.5, -90.5, -85.5]]
PK["parca"]["ELK_ANA_PANO_UF"] = L
PK["birim"]["ELK_ANA_PANO_UF"]["ad"] = PK["birim"]["ELK_ANA_PANO_UF"]["ad"].replace("kapakta kapı tipi döner ana şalter", "ana şalter ABB OT40F4 DIN rayında, kapakta OHYS2AJ kol + OXP6X mil").replace(" + 3 rakor", " · kablolar arka rakorlardan (sol yan rakorlar kalktı)")
IC = []
for sp in (qr5, k5, b5, p5):
    for k in sp.KAN: IC.append(["ic_kanal_%s_%s" % (sp.IST, k["ad"]), 0] + [float(k["lo"][0]), float(k["hi"][0]), float(k["lo"][1]), float(k["hi"][1]), float(k["lo"][2]), float(k["hi"][2])])
PK["parca"]["ELK_IC"] = IC
PK["birim"]["ELK_IC"] = {"ad": "İstasyon iç kapaklı kablo kanalları (304, 1,2 mm, kapaklı; v8zn turunda eklenenler: QR · K · B · ana pano arkası)", "mal": "ME2_kanal"}
json.dump(PK, open(ypj, "w", encoding="utf-8"), ensure_ascii=False)
print("parca_kutulari: ELK_ANA_PANO_UF", len(L), "· ELK_IC", len(IC))
