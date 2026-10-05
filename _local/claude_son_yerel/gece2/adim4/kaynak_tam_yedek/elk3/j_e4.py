# -*- coding: utf-8 -*-
"""mekanizma_v3_8.json -> v8zk: ünite kutuları yeni modelden · birim ELK_ZEMIN -> Çevre/Dükkân hattı · parça listesi: eski dış zincir
(arka kanal, fiş cepleri, iniş, dirsek, dış paneller, duvar flanşı, QR önü başlık) çıktı; birleşim panelleri, contalı geçişler, iç kanallar,
pano gömme cebi, zemin içi kanal, robot rezerv zemin kutusu girdi. python j_e4.py eski.json cache yeni.json"""
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
J["birim"]["ELK_ZEMIN"] = "Çevre/Dükkân hattı"
P = {k: v for k, v in J["parca"].items() if not k.startswith(("ELK_ZINCIR|", "ELK_DUVAR|"))}
n0 = len(J["parca"])
ad = lambda s: s
# birleşim panelleri (her birleşimde iki taraf: sol / sağ istasyon)
for j, L, R in (("J1", "TOPPING", "F"), ("J2", "F", "K"), ("J3", "K", "E")):
    for ist, yon in ((L, "sag_duvar"), (R, "sol_duvar")):
        u = ist + "/Elektrik"
        for p in ("birlesim_paneli_304", "guc_Han10B_govde_kapak", "veri_M12X", "panel_kanali"):
            P["ELK_ZINCIR|%s_%s_%s_%s" % (p, j, ist, yon)] = u
        P["ELK_ZINCIR|hava_QSSF8_%s_%s" % (j, ist)] = ist + "/Hava"
    P["ELK_ZINCIR|contali_gecis_%s_%s_%s" % (j, L, R)] = "Elektrik/Ana hat"
    for k in ("guc_5G2.5", "veri_Cat6A"): P["ELK_ZINCIR|ara_kablo_%s_%s" % (j, k)] = "Elektrik/Ana hat"
    P["ELK_ZINCIR|ara_hortum_%s_PU8" % j] = "F/Hava"
for p in ("F_ust_arka_kanal_H1", "F_pano_inis_kanali_V1", "F_kutu_kanali_V2", "F_bant_motor_kablosu", "F_kutu_baglanti"):
    P["ELK_ZINCIR|" + p] = "F/Elektrik"
P["ELK_ZINCIR|F_kompresor_cikis_hortumu"] = "F/Hava"
for p in ("K_sol_dik_kanal", "K_ust_kanal", "K_sag_dik_kanal", "K_kutu_kanal_kolu"):
    P["ELK_ZINCIR|" + p] = "K/Elektrik"
P["ELK_ZINCIR|K_hava_giris_hortumu"] = "K/Hava"
P["ELK_ZINCIR|T_kanal_kolu"] = "TOPPING/Elektrik"; P["ELK_ZINCIR|T_regulator_giris_hortumu"] = "TOPPING/Hava"
P["ELK_ZINCIR|E_kanal_kolu"] = "E/Elektrik"
P["ELK_ZINCIR|B_dik_kanal"] = "B/Elektrik"; P["ELK_ZINCIR|B_pano_kanali"] = "B/Elektrik"
for p in ("pano_gomme_giris_cebi", "pano_arka_rakorlari", "bina_5G6", "bina_Cat6A", "kol_sol_guc_5G2.5", "kol_sol_veri_Cat6A", "kol_sag_guc_5G2.5", "kol_sag_veri_Cat6A"):
    P["ELK_ZINCIR|" + p] = "Elektrik/Ana pano"
for p in ("zemin_kolu_guc_5G2.5", "zemin_kolu_veri_Cat6A"):
    P["ELK_ZINCIR|" + p] = "Çevre/Dükkân hattı"
for p in ("zemin_ici_oluk", "zemin_kapak_saci", "robot_rezerv_zemin_kutusu", "robot_Han10B_kapakli", "robot_M12_kapakli",
          "pano_B_guc", "pano_B_veri", "B_QR_guc", "B_QR_veri", "QR_robot_guc", "QR_robot_veri"):
    P["ELK_ZEMIN|" + p] = "Çevre/Dükkân hattı"
P["ELK_ZEMIN|B_zemin_kovani"] = "B/Elektrik"; P["ELK_ZEMIN|QR_zemin_kovani"] = "QR/Elektrik"; P["ELK_ZEMIN|QR_robot_kovani"] = "QR/Elektrik"
P["ELK_DUVAR|ana_salter_Eaton_P3-63_I4_sag_uc"] = "Çevre/Dükkân hattı"; P["ELK_ZINCIR|QR_kilit_karti_veri_hatti"] = "QR/Elektrik"
for v in P.values(): assert v in KOD, v
J["parca"] = P
if isinstance(J.get("kapsam"), dict): J["kapsam"]["parca"] = len(P)
J["glb"] = "hat3_v8.glb (v8zk)"
J["surum"] = J["surum"].split(" · v8zj")[0] + (" · v8zk elektrik İÇERİDEN: makinenin dış yüzlerinde kanal/panel yok (arka düz); istasyonlar komşu yan duvarlardaki"
             " gömme birleşim panelleriyle (Han 10B / M12 X / QSSF-8, contalı geçiş, tek yükseklik y 1468–1602) bağlı; iç kanallar kapaklı;"
             " pano gömme arka giriş; B · QR · robot rezerv zemin içinden; şalter makinenin sağ ucunda duvarda; güç kırmızı · bilgi mavi")
json.dump(J, open(yj, "w", encoding="utf-8"), ensure_ascii=False)
print("kutu", len(K), "· parca", n0, "->", len(P), "· eksik kutu", [k for k in KOD if k not in K])
