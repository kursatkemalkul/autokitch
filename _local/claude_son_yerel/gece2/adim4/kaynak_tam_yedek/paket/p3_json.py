# -*- coding: utf-8 -*-
"""mekanizma_v3_8.json (sayfa agaci) v8zd: yeni unite listesi (Robot yok, QR/Robot kutusu (rezerv), Cevre/Dukkan hatti) + unite kutulari yeni
modelden + 3 kademe tanimi (dukkan > makine > istasyon). python p3_json.py eski.json zd yeni.json"""
import sys, json, numpy as np
ej, d, yj = sys.argv[1:4]
J = json.load(open(ej, encoding="utf-8"))
D = np.load(d + "/m8_onbellek.npz"); PJ = json.load(open(d + "/m8_parca.json", encoding="utf-8"))
MEK = PJ["MEK"]; KOD = [m["kod"] for m in MEK]
J["liste"] = [{"kod": m["kod"], "istasyon": m["istasyon"], "ad": m["ad"]} for m in MEK]
IST = []
for s in J["istasyon"]:
    if s["kod"] == "Robot": continue
    if s["kod"] == "Elektrik": s = dict(s, ad="Elektrik · ana pano + ana hat", modul=[])
    if s["kod"] == "Çevre": s = dict(s, ad="Çevre · zemin · dükkân hattı · ürün · insan")
    IST.append(s)
J["istasyon"] = IST
# kutu
T = np.stack([D["A"], D["B"], D["C"]], 1); mek = D["mek"]; K = {}
for i, k in enumerate(KOD):
    m = mek == i
    if not m.any(): continue
    Q = T[m].reshape(-1, 3); lo = Q.min(0) / 1000; hi = Q.max(0) / 1000
    K[k] = [round(float(x), 4) for x in (lo[0], hi[0], lo[1], hi[1], lo[2], hi[2])]
J["kutu"] = K
# parca (adli parca -> unite; yalniz sayac icin)
ESL = {}
try:
    for e in json.load(open(sys.argv[4], encoding="utf-8"))["parca"]:
        if e["ad"]: ESL[e["dugum"].split("__")[0] + "|" + e["ad"]] = e
except Exception: pass
SIL = ("qrk_ana_hat_guc_ROBOT", "qrk_guc_ROBOT", "qrk_ana_hat_veri_ROBOT", "qrk_veri_ROBOT", "harting_ROBOT_rakoru", "ana_hat_ROBOT_", "harting_ANA_PANO_ROBOT_", "harting_ANA_PANO_A_")
YP = {}
for k, v in J["parca"].items():
    ad = k.split("|", 1)[1] if "|" in k else k
    if any(ad.startswith(s) for s in SIL): continue
    if v == "Robot/Kontrol kutusu": v = "QR/Robot kutusu (rezerv)"
    elif v.startswith("Robot/"):
        if ad.startswith("giris_a_KT_20"): v = "Çevre/Dükkân hattı"
        else: continue
    elif v == "Elektrik/Ana hat":
        e = ESL.get(k)
        if e and (e["lo"][0] >= 5230 or e["lo"][2] >= 79): v = "Çevre/Dükkân hattı"
        elif k.startswith("ELK_ZEMIN_KANALI|") or k.startswith("ELK_ANA_HAT|ayirici") : v = "Çevre/Dükkân hattı"
    assert v in KOD, (k, v)
    YP[k] = v
J["parca"] = YP
J["birim"] = {k: ("QR/Robot kutusu (rezerv)" if v == "Robot/Kontrol kutusu" else v) for k, v in J["birim"].items() if not k.startswith("ROBOT")}
J["birim"]["ELK_ZEMIN_KANALI"] = "Çevre/Dükkân hattı"
for v in J["birim"].values(): assert v in KOD, v
# 3 kademe: Dukkan (her sey) > Makine (istasyonlar + makine ici elektrik; zemin yuzeyi kalir) > Istasyon (uniteler)
J["kademe"] = {
    "dukkan": {"ad": "Dükkân", "grup": [{"kod": "Makine", "ad": "Makine"}, {"kod": "QR"}, {"kod": "Tezgâh"}, {"kod": "Çevre"}]},
    "makine": {"ad": "Makine", "ist": ["A", "B", "TOPPING", "F", "K", "E", "U", "Elektrik"], "ek": ["Çevre/Zemin"]},
}
J["glb"] = "hat3_v8.glb (v8zd)"
J["surum"] = "v3_8 gruplama v2 (3 Eki 2026) · robot kalktı · 3 kademe (dükkân › makine › istasyon) · IEC 81346: mek = montaj ağacı, kat = disiplin"
json.dump(J, open(yj, "w", encoding="utf-8"), ensure_ascii=False)
print("unite", len(J["liste"]), "· istasyon", [s["kod"] for s in IST], "· kutu", len(K), "· parca", len(YP))
print("eksik kutu:", [k for k in KOD if k not in K])
