# TEK ÇEKMECE MONTAJ PLANI v2 — B · K2 sütunu · 3. sıra (CEK_K2_lahm_3)

Kurallar: MONTAJ_ANIMASYON_KURALLARI.md (19 madde). Üreteç: cek_montaj_v2.py (plan + zaman) → cek_v2_cikti.py (denetim + GLB/JSON). Model: hat3_v9j (ray vidası M5×6 = zincir 43).
Açık taraf: bölme yalnız önden (çerçeve açıklığı x 1453,5–2073,5 · y 416,5–491,5). Montaj tezgâhı dolabın önünde (çekmece +z 900), üretim tezgâhı sağda (lazer/abkant noktası x 2470 z 560 + hazır rafı).

| # | adım | parça | işlem | yön | bağlantı elemanı (adet) |
|---|---|---|---|---|---|
| 1 | Üretim: kızak köşebentleri (eklendi) | köşebent ×4 (EKLENDİ) | lazer açınım (Ø4,5) → abkant 1 büküm | — | — |
| 2 | Üretim: motor braketi · sensör plakası | motor braketi 3 mm | lazer (Ø22,5 + 4×M3 havşa + 2×M5 havşa) → abkant 1 büküm | — | — |
| 2 | Üretim: motor braketi · sensör plakası | sensör plakası 2 mm | lazer, düz | — | — (model açığı A3) |
| 3 | Üretim: avara kolu · sensör laması · kaynak | avara kolu 2 + sensör laması L 2 + avara mili | lazer → abkant 2 + 1 büküm → TIG (kulak↔lama) + saplama kaynağı (mil↔kol) | lama alttan, mil +x | TIG 3 dikiş · saplama kaynağı |
| 4 | Ray ünitesi: iç eleman ayrılır | ray ünitesi sol/sağ (Accuride DZ3832, katalog) | iç eleman (kızak) ray ekseni boyunca öne çekilip ayrılır | +z | — |
| 5 | Motor braketi arka duvara | motor braketi | önden açıklıktan → arka duvar | −z | DIN 7991 M5×6 (2) → PEM SP-M5 arka iç sac (EKLENDİ) |
| 6 | Motor braketine (ekseni boyunca) | step motor | önden, sonra ekseni boyunca braket deliğine | −z, −x | DIN 7991 M3×6 (4) → redüktör M3 dişi |
| 7 | Motor kasnağı · setskur | GT3 motor kasnağı | mil ekseninde | +x | DIN 913 M3×4 setskur (1) |
| 8 | Sensör plakası (model açığı) | sensör plakası | önden arka duvara | −z | YOK — model açığı A3 |
| 9 | Ray üniteleri bölme saclarına | ray ünitesi sol/sağ (dış+ara) | önden, yana bölme sacına | −z, ∓x | DIN 7991 M5×6 (6) → PEM SP-M5 (var), ara eleman erişim deliğinden |
| 10 | Avara ünitesi · perçin · avara kasnağı · reed | avara ünitesi | 21 alçaktan açıklık → sola → yükselir → çerçeve arkası | −z, −x, +y, +z | kör perçin Ø3,2 ISO 15983 (2), önden |
| 10 | Avara ünitesi · perçin · avara kasnağı · reed | GT3 avara kasnağı · reed ×2 | mil ekseninde · yandan | −x · −x | — (E segman payı yok; reed deliği yok — açık) |
| 11 | Kutu sacları: lazer → tezgâh → TIG | kutu: taban 2 + yan ×2 + arka + ön 1 mm | lazer düz → montaj tezgâhı | üstten | TIG 4 dikiş |
| 12 | Kızak lamaları (kesim boyu, M4 dişli) → punta | lama sol/sağ 6×17,3×616 | kesim boyu + 2×M4 dişli kör delik → kutu yanına | yandan | punta 4+4 |
| 13 | Ön bağlantı braketleri: abkant → punta | ön braket sol/sağ 2 mm | lazer (2×Ø5,5) → abkant 2 büküm → kutu önü | önden | punta 2+2 |
| 14 | Kayış çenesi: alt gövde TIG → kutuya TIG · üst çene · tepsi | çene alt gövde · üst çene · tepsi | lama parçaları TIG → kutuya TIG; üst çene rafa; tepsi serbest | yandan / üstten | TIG 2+2 |
| 15 | Tezgâh: köşebentler · kızaklar | köşebent ×4 · kızak ×2 | köşebent lamaya; kızak köşebent dik koluna | üstten / yandan | ISO 7380 M4×6 (4) → lama M4 dişi · punta 2×4 (ÖNERİ) |
| 16 | Çekmece raylara sürülür | çekmece grubu | ray ekseni boyunca 900 mm; montaj tezgâhı çekilir | −z | kızak ↔ ara eleman bilyalı kafes |
| 17 | Kayış · üst çene · mıknatıs | kayış · üst çene · mıknatıs | kayış sarılır (istisna); üst çene üstten | −y | ISO 7380 M3×10 (2) + ISO 4032 M3 (2) |
| 18 | Üretim: ön kapak (8 büküm) · iç panel + PEM | kapak dış kabuk 1,5 · iç panel 1,0 | lazer → abkant 8 büküm; iç panel + PEM pres; iç panel kabuğa | — | PEM FHS-M5-10 (4) |
| 19 | Ön kapak · fitil · somunlar | fitil · ön kapak | fitil kanala; kapak saplamaları braket deliklerinden | +z · −z | DIN 125 M5 (4) + ISO 4032 M5 (4), U braketin açık yanından |
| 20 | Kablolar | kablolar | kanal boyunca (istisna) | — | — |

Bükümler (sırayla, iç R = t; model köşeleri keskin → kesim boyunda K 0,45 ile düşülür):
- on_braket_sol (t 2.0): 1 yan kol 90° → 2 ön flanş 90°
- on_braket_sag (t 2.0): 1 yan kol 90° → 2 ön flanş 90°
- motor_braketi (t 3.0): 1 motor flanş kolu 90°
- avara_kolu (t 2.0): 1 ön flanş (çerçeveye) 90° → 2 üst flanş 90°
- sensor_lamasi (t 2.0): 1 dik kol 90°
- kapak_dis (t 1.5): 1 sol kenar 90° → 2 sağ kenar 90° → 3 alt kenar 90° → 4 üst kenar 90° → 5 sol arka dönüş 90° → 6 sağ arka dönüş 90° → 7 alt arka dönüş 90° → 8 üst arka dönüş 90°
- kose_sol_1 (t 1.5): 1 dik kol (kızağa) 90°
- kose_sol_2 (t 1.5): 1 dik kol (kızağa) 90°
- kose_sag_1 (t 1.5): 1 dik kol (kızağa) 90°
- kose_sag_2 (t 1.5): 1 dik kol (kızağa) 90°
