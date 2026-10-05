# -*- coding: utf-8 -*-
"""mekanizma_v3_8.json + parca_kutulari.json -> v8zp. python j_zp.py mek.json pk.json cache_dir"""
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ej, pj, d = sys.argv[1:4]
J = json.load(open(ej, encoding="utf-8")); PK = json.load(open(pj, encoding="utf-8"))
D = np.load(d + "/m8_onbellek.npz"); PJ = json.load(open(d + "/m8_parca.json", encoding="utf-8"))
KOD = [m["kod"] for m in PJ["MEK"]]
T = np.stack([D["A"], D["B"], D["C"]], 1); mek = D["mek"]; K = {}
for i, k in enumerate(KOD):
    m = mek == i
    if not m.any(): continue
    Q = T[m].reshape(-1, 3); lo = Q.min(0) / 1000; hi = Q.max(0) / 1000
    K[k] = [round(float(x), 4) for x in (lo[0], hi[0], lo[1], hi[1], lo[2], hi[2])]
J["kutu"] = {**{k: v for k, v in J.get("kutu", {}).items() if k not in K}, **K}
A2 = json.load(open(os.path.join(HERE, "a2_parca.json"))); A4 = json.load(open(os.path.join(HERE, "a4_parca.json")))
# ---------------- mekanizma parca listesi
SIL = {"DUZ_TEZGAH_DUVAR|duvar_kaplama_ince", "TEZGAH_GOVDE|duvar_kosebendi_ince", "TEZGAH_BULASIK|bulasik_hat_elektrik",
       "ELK_ANA_PANO_UF|ana_salter_mili_ABB_OXP6X_6mm_kare"}
P = {k: v for k, v in J["parca"].items() if k not in SIL and not k.startswith("TEZGAH_ASKI|")}
n0 = len(J["parca"])
P["ELK_ANA_PANO_UF|ana_salter_mili_ABB_OXS6X160_6mm_kare"] = "Elektrik/Ana pano"
P["ELK_ANA_PANO_UF|ana_salter_kolu_kapak_arkasi_somun_M22"] = "Elektrik/Ana pano"
for a in A2: P["ELK_IC|" + a["ad"]] = "B/Elektrik"
for a in A4: P["HAVA_IC|" + a["ad"]] = a["ist"] + "/Hava"
for ist in ("TOPPING", "K", "F"): P["HAVA_IC|hava_kanali_askilari_%s" % ist] = ist + "/Hava"
P["TEZGAH_BINA_HATTI|zemin_buati_evye"] = "Tezgâh/Gövde"
P["TEZGAH_BINA_HATTI|zemin_buati_bulasik"] = "Tezgâh/Gövde"
P["TEZGAH_BINA_HATTI|kablo_EIL3_priz"] = "Tezgâh/Evye"
P["TEZGAH_BINA_HATTI|kablo_MEIKO"] = "Tezgâh/Bulaşık makinesi"
for v in P.values(): assert v in KOD, v
J["parca"] = P
if isinstance(J.get("kapsam"), dict): J["kapsam"]["parca"] = len(P)
J["glb"] = "hat3_v8.glb (v8zp)"
J["surum"] = J["surum"] + (" · v8zp QR sola 200 (sağ dış yüzü E sağ dış yüzüyle 5230 hizada; zemin kanalı, robot zemin kutusu, kablolar, kutu/ürün giriş animasyonu birlikte);"
                           " tezgâh ince duvar sacı + askı kalktı, tezgâh 180° döndü (ön +x) ve x −620; tezgâh ayrı bina hattı (2 zemin buatı, zincire bağlı değil);"
                           " yeşil hava hortumları kapaklı hava kanalında (TOPPING 3, K 2, F 1 grup + askılar); B çekmece kablo kanalı köşeleri kapandı (ray L flanşı köşede kısaldı);"
                           " ana şalter OT40F4N2 48×68×56 + OHYS2AJ (66) + OXS6X160 mil; QR müşteri paneli gerçek ürün ölçüleri")
json.dump(J, open(os.path.join(HERE, "mekanizma_v3_8.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("mekanizma: kutu", len(K), "· parca", n0, "->", len(P))
# ---------------- parca_kutulari
def kx(x): return x - 200.0 if x > 4400 else x
QRB = [k for k in PK["parca"] if k.startswith(("QR_", "ELK_QR_"))]
for k in QRB:
    PK["parca"][k] = [[e[0], e[1], e[2] - 200, e[3] - 200] + e[4:] for e in PK["parca"][k]]
for k in PK["parca"]:
    if k.startswith("ELK_ZEMIN") and k != "ELK_ZEMIN_KANALI":
        PK["parca"][k] = [[e[0], e[1], kx(e[2]), kx(e[3])] + e[4:] for e in PK["parca"][k]]
PK["parca"]["QR_MUSTERI_PANELI"] = [["ekran_7in_RPi_Touch_Display_2", 0, 4627.5, 4817.5, 1658.0, 1778.0, 1173.0, 1188.0],
                                    ["qr_okuyucu_Newland_FM430", 0, 4859.0, 4901.0, 1687.5, 1712.5, 1138.0, 1188.0],
                                    ["pin_tus_takimi_Storm_1000_16tus", 0, 4951.75, 5034.25, 1676.75, 1759.25, 1158.0, 1188.0]]
B = PK["birim"]
B["QR_GOVDE"]["ad"] = B["QR_GOVDE"]["ad"].replace("x 4570–5430", "x 4370–5230 (sağ dış yüzü E sağ dış yüzüyle hizalı)")
B["QR_ROBOT_KONTROL"]["ad"] = B["QR_ROBOT_KONTROL"]["ad"].replace("x 4595–5070", "x 4395–4870")
B["QR_MUSTERI_PANELI"]["ad"] = ("Müşteri paneli · 7\" ekran Raspberry Pi Touch Display 2 (190 × 120 × 15) + QR okuyucu Newland NLS-FM430 (42 × 25 × 50)"
                                 " + PIN tuş takımı Storm 1000 16 tuş (panel kesiti 82,5 × 82,5) · yazıcı yok · müşteri yüzü, üst bölmenin önü")
# tezgah: 180 derece (x' = 7727 - x, z' = 2918 - z)
SILP = {("DUZ_TEZGAH_DUVAR", "duvar_kaplama_ince"), ("TEZGAH_GOVDE", "duvar_kosebendi_ince"), ("TEZGAH_BULASIK", "bulasik_hat_elektrik")}
PK["parca"].pop("TEZGAH_ASKI", None); B.pop("TEZGAH_ASKI", None)
for k in list(PK["parca"]):
    if not (k.startswith("TEZGAH_") or k == "DUZ_TEZGAH_DUVAR"): continue
    PK["parca"][k] = [[e[0], e[1], round(7727.0 - e[3], 2), round(7727.0 - e[2], 2), e[4], e[5], round(2918.0 - e[7], 2), round(2918.0 - e[6], 2)]
                      for e in PK["parca"][k] if (k, e[0]) not in SILP]
B["DUZ_TEZGAH_DUVAR"]["ad"] = "Tezgâh duvar kaplama sacı (yalnız sokak sacı · ince duvar sacı ve askı rayı kalktı · 304 1,2 · alt ucu tabla eteğine bindirmeli) — sabunluk · havluluk bunun üstünde"
B["TEZGAH_GOVDE"]["ad"] = B["TEZGAH_GOVDE"]["ad"].replace("cebi duvardan duvara doldurur (x 3842–4505 · z 1044–1874)", "180° döndü, ön +x · x 3222–3885 · z 1044–1874 (QR'ın solunda, açılma yolları QR'a ve QR müşteri kapılarına girmez)")
B["TEZGAH_BULASIK"]["ad"] = B["TEZGAH_BULASIK"]["ad"].replace("bekleme alanına (−x) açılır", "+x yönüne açılır").replace("bağlantılar arkadan niş duvarına", "elektrik: ayrı bina hattı (zemin buatından, zincire bağlı değil) · su/tahliye arkada")
PK["parca"]["TEZGAH_BINA_HATTI"] = [["zemin_buati_evye", 0, 3200.0, 3270.0, -80.0, 0.0, 1100.0, 1170.0], ["zemin_buati_bulasik", 0, 3200.0, 3270.0, -80.0, 0.0, 1760.0, 1830.0],
                                     ["kablo_EIL3_priz", 0, 3227.5, 3236.5, -60.0, 760.0, 1130.5, 1139.5], ["kablo_MEIKO", 0, 3227.5, 3245.0, -60.0, 64.5, 1790.5, 1832.5]]
B["TEZGAH_BINA_HATTI"] = {"ad": "Tezgâh AYRI BİNA HATTI (makine zincirine bağlı değil; fırın gibi): bulaşık MEIKO 14 A + el evyesi ısıtıcı Stiebel EIL 3 15,2 A · her biri kendi bina sigortası · zemin altından gizli giriş, 2 gömme paslanmaz buat (kapak zeminle aynı yüz) + rakor · kablo tezgâh içinde (görünür kablo yok)", "mal": "MS_TEZGAH_BINA"}
# ana pano salter
L = [e for e in PK["parca"]["ELK_ANA_PANO_UF"] if not e[0].startswith(("ana_salter_", "montaj_plakasi_lastik"))]
xc, yc = 3612.0, 2107.0
L += [["ana_salter_ABB_OT40F4N2_DIN", 0, xc - 24, xc + 24, yc - 34, yc + 34, -280.5, -224.5],
      ["ana_salter_mili_OXS6X160", 0, xc - 3, xc + 3, yc - 3, yc + 3, -235.5, -75.5],
      ["ana_salter_kolu_OHYS2AJ", 0, xc - 33, xc + 33, yc - 33, yc + 33, -87.0, -53.0],
      ["ana_salter_kolu_somun_M22", 0, xc - 20, xc + 20, yc - 20, yc + 20, -103.0, -89.0],
      ["montaj_plakasi_lastik_gecit", 0, xc - 13, xc + 13, 2141.5, 2167.5, -284.0, -279.0]]
PK["parca"]["ELK_ANA_PANO_UF"] = L
B["ELK_ANA_PANO_UF"]["ad"] = B["ELK_ANA_PANO_UF"]["ad"].replace("ana şalter ABB OT40F4 DIN rayında, kapakta OHYS2AJ kol + OXP6X mil", "ana şalter ABB OT40F4N2 (48 × 68 × 56) DIN rayında, kapakta OHYS2AJ seçici kol (66, kapak deliği Ø22,5 + 3,2 kama) + OXS6X160 mil")
# ic kanal + hava kanali
PK["parca"].setdefault("ELK_IC", [])
PK["parca"]["ELK_IC"] += [[a["ad"], 0, a["lo"][0], a["hi"][0], a["lo"][1], a["hi"][1], a["lo"][2], a["hi"][2]] for a in A2]
PK["parca"]["HAVA_IC"] = [[a["ad"], 0, a["lo"][0], a["hi"][0], a["lo"][1], a["hi"][1], a["lo"][2], a["hi"][2]] for a in A4]
B["HAVA_IC"] = {"ad": "Pnömatik hortum kanalları (304 1,2 mm kapaklı, hortum geçişleri delikli, kısa son dallar açık) + 14 × 2 lama askılar · TOPPING (valf adası A/B → silindirler, ana besleme) · K (valf adası → bıçak/itici, → kesici) · F (kompresör → pano iniş kanalı)", "mal": "ME2_kanal"}
json.dump(PK, open(os.path.join(HERE, "parca_kutulari.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("parca_kutulari: QR birim", len(QRB), "· ELK_IC +", len(A2), "· HAVA_IC", len(A4))
