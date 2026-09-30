# K v8 · denetim özeti (30 Eyl 2026 · Claude)

Parça 231 · geçersiz 0 · durağan kesişim 0 · hareket kesişimi 0 · ürün yolu 0 · havada 0
Beklenen temas: bıçaklar (kesim) + E'ye geçişte düz disk modelinin inişi (en derin 14.1 mm; E'nin kendi modeli de aynı)

Hareketli kütleler (CAD hacmi × yoğunluk): KESICI 10.09 kg, ITICI_ARABA 3.26 kg, ITICI_CAPRAZ 0.39 kg, ITICI_KOL 0.90 kg, ITICI_YUZ 0.13 kg, Z_hareketli 1.42 kg, X_hareketli 4.68 kg

| eksen | strok | süre | ort. | tepe | çarpma | sınır | not | durum |
|---|---|---|---|---|---|---|---|---|
| Z itici MY1B10G-350 (lastik tampon) | 350 | 2.92 s | 120 | 180 | 168 | 181.0 | çarpma ≤ 0,9 × tampon sınırı(1.42 kg) · ort. 100–500 | OK |
| X itici MY1B10G-250 + 2 × RB0805 | 250 | 1.67 s | 150 | 225 | 210 | 1000.0 | E = 0.103 J ≤ 1,0 J (RB0805) · X kütlesi 4.68 kg ≤ 5 kg (m1max) · ort. 100–1000 | OK |
| Kesici DGRF-C-63-125 dönüş | 125 | 0.80 s | 156 | 234 | 219 | None | çarpma enerjisi 0.241 J ≤ 1,3 J (Festo 562221) · kesici kütlesi 10.09 kg | OK |
| Kesici DGRF-C-63-125 iniş | 125 | 1.40 s | 89 | 134 | 125 | None | bıçak strok sonunda (bant + 0,5) · 1870 N @ 6 bar | OK |
| Bant EC5000 49:1 (ürün) | 260 | 2.00 s | 130 | 195 | 182 | 370.0 | tepe 195 mm/s ≤ 370 | OK |

İstasyon periyodu 37 s (K + E bir ürün 35.65 s) · E, K saatine göre -10.63 s önce başlar, 25.02 s'de biter · robot çatalı K saati [18.24, 19.44, 19.94, 21.64]
