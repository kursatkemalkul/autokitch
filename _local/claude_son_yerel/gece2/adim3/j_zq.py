# -*- coding: utf-8 -*-
"""mekanizma_v3_8.json + parca_kutulari.json -> v8zq. python j_zq.py mek.json pk.json
pk: kaşar / sucuk kaseti ve yuvasıyla ilgili TOPPING_MODUL kutuları modeldeki gerçek yerlerine (+26,5 / +49,5 x; v8zc 'TOPPING cep geri' kaydırmasından beri
eski kalmıştı — denetim: pk_kontrol.py ile GLB bileşen kutularına 0,6 mm içinde eşleşiyor) · mandal kutuları (ayrı yerde, eşleşmiyor) DOKUNULMADI ·
kaşar yatak kapağı arka yüzü z −126,5 → −124,5."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
ej, pj = sys.argv[1:3]
J = json.load(open(ej, encoding="utf-8")); PK = json.load(open(pj, encoding="utf-8"))
J["glb"] = "hat3_v8.glb (v8zq)"
J["surum"] = J["surum"] + (" · v8zq kaşar/sucuk kaseti iç çakışmaları: kaşar yatak kapağı arka yüzü 2 mm öne (çıkış borusuna 1,5 mm giriyordu, kasar_cad_v15); "
                           "sucuk çıkış tüpünün koni geçişi tüp ucunda kırpıldı (ön muylu + kapak içine giren gaga, sucuk_cad_v9); geçme yüzeyli kaset parçaları ince ağ; "
                           "yarık dili boru deliği boru eksenine ve çapına, raf kaset contaları yeniden (kaba çokgen)")
n = 0
for e in PK["parca"]["TOPPING_MODUL"]:
    a = e[0]
    if "mandal" in a: continue
    dx = 26.5 if "kasar" in a else (49.5 if "sucuk" in a else None)
    if dx is None: continue
    e[2] = round(e[2] + dx, 2); e[3] = round(e[3] + dx, 2); n += 1
    if a == "kasar_cad_v14__yatak_kapagi": e[6] = -124.5
json.dump(J, open(os.path.join(HERE, "mekanizma_v3_8.json"), "w", encoding="utf-8"), ensure_ascii=False)
json.dump(PK, open(os.path.join(HERE, "parca_kutulari.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("pk kaydırılan", n)
