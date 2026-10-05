# -*- coding: utf-8 -*-
"""menu7 hesap v2: 2 günlük ihtiyaç ↔ MODELLENEN hazne iç hacmi (adım 53 _ent.json: manifold iç boşluk, boyun → üst). Girdiler hesap.py ile aynı."""
import json, sys
E = json.load(open(sys.argv[1], encoding="utf-8"))["hazne"]
ADET = dict(lahmacun=200, patatesli=20, tavuklu=20, kiymali=10, kusbasili=10, kasarli=10, sucuklu=10)   # V · günlük
URUN = {  # hazne anahtarı, ürün, g/adet, yoğunluk g/ml, adet anahtarı, kaynak
    "harc": ("Lahmacun harcı", 110, 110 / 105, "lahmacun", "K"),
    "kiyma_orta": ("Kıyma", 160, 160 / 152, "kiymali", "K"),
    "patates": ("Patates püresi", 150, 1.05, "patatesli", "V"),
    "tavuk": ("Tavuk", 145, 145 / 170, "tavuklu", "V"),
    "kusbasi": ("Kuşbaşı", 145, 145 / 170, "kusbasili", "K"),
}
print("| Hazne | Ürün | Günlük kg | 2 gün L | İç hacim (brüt) L | Kullanılabilir (×0,90) L | Pay | Günde en çok |")
print("|---|---|---|---|---|---|---|---|")
out = {}
for k, (ad, g, rho, ak, kay) in URUN.items():
    gun = ADET[ak] * g / 1000.0; L2 = 2 * gun / rho
    V = E[k]["ic_hacim_L"]; Vk = V * 0.90
    enc = Vk * rho * 1000.0 / g / 2.0
    pay = (Vk - L2) / L2 * 100
    out[k] = dict(urun=ad, gunluk_kg=round(gun, 2), iki_gun_L=round(L2, 2), brut_L=round(V, 2), kull_L=round(Vk, 2), pay_yuzde=round(pay, 0), gunde_en_cok=int(enc))
    print("| %s | %s | %.2f | %.2f | %.2f | %.2f | %s%%%.0f | %d |" % (k, ad, gun, L2, V, Vk, "+" if pay >= 0 else "", pay, enc))
json.dump(out, open("hesap_v2_sonuc.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
