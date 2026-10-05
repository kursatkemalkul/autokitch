# -*- coding: utf-8 -*-
"""mekanizma_v3_8.json -> v8zl: kutular yeni modelden · parça: duvar şalteri, yayıcı CRB2 aktüatörleri + 4 hortum + duvar geçiş kovanı/tapası çıktı;
iç kanallar (istasyon başına), yayıcı sabit bağlantıları, pano kapağındaki ana şalter girdi. python j_e5.py eski.json cache yeni.json"""
import sys, json, re, numpy as np
sys.path.insert(0, r"@@KOK_W@@\elk4")
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
J["kutu"] = {**{k: v for k, v in J.get("kutu", {}).items() if k not in K}, **K}
J["birim"]["ELK_IC"] = "TOPPING/Elektrik"
P = {k: v for k, v in J["parca"].items() if not k.startswith("ELK_DUVAR|") and not re.search(r"spreader_aktuator|spreader_kaplin|hava_hortumu_(harc|sos)_spreader|yayici_hortum_gecis_kovani|yayici_gecis_tapasi", k)}
n0 = len(J["parca"])
import ts, ks, fs, us, bs
for sp in (ts, ks, fs, us):
    for k in sp.KAN: P["ELK_IC|ic_kanal_%s_%s" % (sp.IST, k["ad"])] = sp.IST + "/Elektrik"
P["ELK_IC|ic_kanal_B_cekmece_arka_duvar_%d_adet" % sum(1 for k in bs.KAN if k["ad"].startswith("Barka"))] = "B/Elektrik"
P["ELK_IC|ic_kanal_B_cekmece_rayi_yassi_%d_adet" % sum(1 for k in bs.KAN if k["ad"].startswith("Byan"))] = "B/Elektrik"
P["TOPPING_MODUL|harc_yayici_sabit_paslanmaz_baglanti"] = "TOPPING/Harç"
P["TOPPING_MODUL|sos_yayici_sabit_paslanmaz_baglanti"] = "TOPPING/Sos"
P["ELK_ANA_PANO_UF|ana_salter_kapi_tipi_doner_kollu_63A_4P_kilitlenebilir"] = "Elektrik/Ana pano"
for v in P.values(): assert v in KOD, v
J["parca"] = P
if isinstance(J.get("kapsam"), dict): J["kapsam"]["parca"] = len(P)
J["glb"] = "hat3_v8.glb (v8zl)"
J["surum"] = J["surum"].split(" · v8zl")[0].replace("; şalter makinenin sağ ucunda duvarda", "") + (
    " · v8zl iç kablolama: istasyon içi kablolar kapaklı iç kanallarda (duvara yaslı, dik dallar, cihaz ucunda ≤150 mm açık);"
    " ana şalter ana pano kapağında (kilitlenebilir döner kollu); yayıcılar sabit (döner aktüatör yok); hava hortumları yeşil · güç kırmızı · bilgi mavi")
json.dump(J, open(yj, "w", encoding="utf-8"), ensure_ascii=False)
print("kutu", len(K), "· parca", n0, "->", len(P))
