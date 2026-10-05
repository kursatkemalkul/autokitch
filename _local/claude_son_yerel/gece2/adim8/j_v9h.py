# -*- coding: utf-8 -*-
"""mekanizma_v3_8.json + parca_kutulari.json (v9f) → son sürüm (adım 8: zincir 39 servis D2–D4, 40 acil stop).
python j_v9h.py mek.json pk.json cikti_klasoru surum_harfi ent39.json ent40.json"""
import sys, os, json
mj, pj, cik, harf = sys.argv[1:5]; EJ = sys.argv[5:]
M = json.load(open(mj, encoding="utf-8")); PK = json.load(open(pj, encoding="utf-8"))
L = M["liste"]
MEKK = {"F_UST_KABIN": "F/Gövde", "HAVA_KOMPRESOR": "F/Hava", "K_YAG": "K/Sprey"}
YER = {}
eklenen = {}
for f in EJ:
    e = json.load(open(f, encoding="utf-8"))
    for y in e.get("yer", []): YER[y[0]] = L[y[5]]["kod"]
    for ad, p in e["parca"].items():
        b = p["dugum"].split("__")[0]
        Lb = PK["parca"].setdefault(b, [])
        Lb[:] = [x for x in Lb if x[0] != ad]
        Lb.append([ad, int(p["kpk"])] + [round(v, 1) for v in p["kutu"]])
        if b == "ACIL_STOP":
            ist = ad.split("_")[2]; kod = YER.get(ist, "Elektrik/Ana hat")
        else:
            kod = MEKK.get(b, M["birim"].get(b, "?"))
        M["parca"]["%s|%s" % (b, ad)] = kod
        eklenen[b] = eklenen.get(b, 0) + 1
# D2: kayıt artık iki parça — parca_kutulari'nda bilgi notu (kutular: sol 2501,5–3358 · sağ 3360–3996,5)
for b in ("F_UST_KABIN",):
    for x in PK["parca"].get(b, []):
        pass
M["birim"].setdefault("ACIL_STOP", "Elektrik/Ana hat")
PK["birim"].setdefault("ACIL_STOP", {"ad": "ACİL STOP · Schneider Harmony XB4BS8442 Ø40 mantar (1 NC, çevirerek bırakma) + ZBY9330T sarı etiket Ø60 · istasyon başına 1 (A hariç), QR'da servis yüzü · kapak üstünde (ön yüzde sabit yüz yok)", "mal": "ME2_ACIL_STOP"})
M["glb"] = "hat3_v8.glb (v9%s)" % harf
M["surum"] = M["surum"] + (" · v9%s (4 Eki · adım 8): servis düzeltmeleri — fırın üstü üst kaydının sağ yarısı cıvatalı (kompresör çıkar), yağ lansı hortumlarında "
                           "2 kapamalı kaplin + seviye şalteri M12 fişi, kompresör çıkışında spiral servis halkası + fişli besleme · 6 acil stop butonu (TOPPING, B, F, K, E, QR servis yüzü) · zincir adım 39–40" % harf)
os.makedirs(cik, exist_ok=True)
json.dump(M, open(os.path.join(cik, "mekanizma_v3_8.json"), "w", encoding="utf-8"), ensure_ascii=False)
json.dump(PK, open(os.path.join(cik, "parca_kutulari.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("eklenen", eklenen, "· mek parca", len(M["parca"]))
