# -*- coding: utf-8 -*-
"""mekanizma_v3_8.json -> v8zj: ünite kutuları yeni modelden (p3_json mantığı) · birim: ELK_ZINCIR -> Elektrik/Ana hat, ELK_DUVAR -> Çevre/Dükkân hattı,
*_sinyal -> kendi istasyon Elektrik'i · parça sayacı: eski yıldız ana hat / zemin kanalı / pano Harting adları çıktı, zincir parçaları girdi."""
import sys, json, numpy as np
ej, d, yj = sys.argv[1:4]
J = json.load(open(ej, encoding="utf-8"))
D = np.load(d + "/m8_onbellek.npz"); PJ = json.load(open(d + "/m8_parca.json", encoding="utf-8"))
KOD = [m["kod"] for m in PJ["MEK"]]
T = np.stack([D["A"], D["B"], D["C"]], 1); mek = D["mek"]; K = {}
for i, k in enumerate(KOD):
    m = mek == i
    if not m.any(): continue
    Q = T[m].reshape(-1, 3); lo = Q.min(0) / 1000; hi = Q.max(0) / 1000
    K[k] = [round(float(x), 4) for x in (lo[0], hi[0], lo[1], hi[1], lo[2], hi[2])]
K0 = J.get("kutu", {}); J["kutu"] = {**{k: v for k, v in K0.items() if k not in K}, **K}
J["birim"]["ELK_ZINCIR"] = "Elektrik/Ana hat"
J["birim"]["ELK_DUVAR"] = "Çevre/Dükkân hattı"
J["birim"].pop("ELK_ZEMIN_KANALI", None)
SIL = ("ELK_ANA_HAT|", "ELK_ZEMIN_KANALI|")
P = {k: v for k, v in J["parca"].items() if not k.startswith(SIL) and not ("harting" in k.lower() and k.startswith(("ELK_ANA_PANO_UF|", "ELK_ISTASYON|")))}
n0 = len(J["parca"])
for ist, u in (("TOPPING", "TOPPING/Elektrik"), ("F", "F/Elektrik"), ("K", "K/Elektrik"), ("B", "B/Elektrik"), ("E", "E/Elektrik"), ("QR", "QR/Elektrik")):
    for p in ("fis_paneli", "guc_giris_Han10B", "veri_giris_M12X", "guc_cikis_Han10B", "veri_cikis_M12X"):
        P["ELK_ZINCIR|%s_%s" % (p, ist)] = u
    if ist in ("TOPPING", "F", "K", "E"):
        P["ELK_ZINCIR|hava_giris_QSSF8_%s" % ist] = u; P["ELK_ZINCIR|hava_cikis_QSSF8_%s" % ist] = u
for p in ("ana_kanal_arka", "pano_inis_kanali", "dirsek_kutusu_U_gecisi", "E_ucu_inis_kanali", "zemin_kanali_E_alti", "fis_cebi_TOPPING", "fis_cebi_F", "fis_cebi_K", "fis_cebi_B", "fis_cebi_E",
          "kol_sol_guc_5G2.5", "kol_sol_veri_Cat6A", "kol_sag_guc_5G2.5", "kol_sag_veri_Cat6A", "ara_F_TOPPING_guc", "ara_F_TOPPING_veri", "ara_K_B_guc", "ara_K_B_veri",
          "ara_B_E_guc", "ara_B_E_veri", "ara_E_QR_guc", "ara_E_QR_veri", "hava_F_TOPPING", "hava_F_K", "hava_K_E"):
    P["ELK_ZINCIR|" + p] = "Elektrik/Ana hat"
for p in ("bina_5G6", "bina_Cat6A", "pano_arka_rakorlari"):
    P["ELK_ZINCIR|" + p] = "Elektrik/Ana pano"
for p in ("ana_salter_Eaton_P3-63_I4", "duvar_flansi", "QR_onu_kanal_basligi", "robot_rezerv_kutusu", "QR_ROBOT_guc", "QR_ROBOT_veri"):
    P[("ELK_DUVAR|" if "salter" in p or "duvar" in p else "ELK_ZINCIR|") + p] = "Çevre/Dükkân hattı"
for v in P.values(): assert v in KOD, v
J["parca"] = P
if isinstance(J.get("kapsam"), dict): J["kapsam"]["parca"] = len(P)
J["glb"] = "hat3_v8.glb (v8zj)"
J["surum"] = J["surum"].split(" · v8z")[0] + " · v8zj elektrik zinciri: duvar şalteri + gizli giriş, ana pano iki kol, arka ana kanal, istasyon fiş panelleri (Han 10B / M12 X / QSSF-8), QR alttan + robot rezerv; güç kırmızı · bilgi mavi"
json.dump(J, open(yj, "w", encoding="utf-8"), ensure_ascii=False)
print("kutu", len(K), "· parca", n0, "->", len(P), "· eksik kutu", [k for k in KOD if k not in K])
