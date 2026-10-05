# TEK ÇEKMECE MONTAJ PLANI v3 — B · K2 sütunu · 3. sıra (CEK_K2_lahm_3)

Kurallar: MONTAJ_ANIMASYON_KURALLARI.md. Model: hat3_v9l (zincir adım 44 · çekmece düzeltmesi, 21 çekmece). Geometri ortak: cek3geo.py (adım 44 ile animasyon AYNI katıları kullanır).
Üreteç: cekmece3/cek_montaj_v3.py (plan + zaman) → cek_v3_cikti.py (denetim + GLB/JSON) · son_kiyas.py (son kare ↔ model).
Tezgâh kutuları YOK: alt montajlar montaj alanında (dolabın önü, +z 900) havada durur. Her birleşimde yakın kamera + olay metni (ne ↔ neye, hangi elemanla).

| # | adım | ne / neyle |
|---|---|---|
| 1 | Üretim: kızak köşebentleri | köşebent × 4 · 1,5 mm · 1 büküm · Ø4,5 |
| 2 | Üretim: motor braketi · reed plakaları | motor braketi 3 mm (1 büküm) · reed plakası 2 mm × 2 + 4 × PEM CLS-M3-2 |
| 3 | Üretim: avara ünitesi (kol · sensör laması · mil · reed plakaları) | avara kolu (2 büküm) · sensör laması (1 büküm) · mil · 2 reed plakası · TIG + saplama kaynağı + punta |
| 4 | Üretim: kayış çenesi (ayrı blok) | çene alt gövdesi (alt çene 2,5 + ara 1,2 · TIG 2 × 28 mm) · üst çene 2,5 |
| 5 | Ray ünitesi: iç eleman ayrılır | ray ünitesi sol / sağ (katalog) · iç eleman ayrılır |
| 6 | Motor braketi → arka duvar | motor braketi · 2 × DIN 7991 M5 × 6 → 2 × PEM SP-M5-1 (arka iç sac) |
| 7 | Step motor → braket | step motor · 4 × DIN 7991 M3 × 6 → motor yüzü M3 dişleri |
| 8 | Motor kasnağı · setskur | GT3 motor kasnağı · DIN 913 M3 × 4 setskur |
| 9 | Ray üniteleri → bölme sacları | ray ünitesi sol / sağ · 6 × DIN 7991 M5 × 6 → PEM SP-M5 |
| 10 | Avara ünitesi → ön çerçeve (TIG, içeriden) | avara ünitesi · TIG köşe 2 × 8 mm (içeriden) |
| 11 | Avara kasnağı · E segman | GT3 avara kasnağı · DIN 6799 RS 5 E segman |
| 12 | Reed sensörler → reed plakaları | reed sensör × 2 · 4 × ISO 7380 M3 × 8 → 4 × PEM CLS-M3-2 |
| 13 | Kutu sacları: lazer → montaj alanı → TIG | kutu tabanı 2 · yan sol / sağ 1 · arka 1 · ön 1 · 4 TIG dikişi |
| 14 | Kızak lamaları → kutu (punta) | lama sol / sağ · 2 × M4 dişli · punta 4 + 4 |
| 15 | Ön bağlantı braketleri → kutu önü (punta) | ön braket sol / sağ · 2 büküm · punta 2 + 2 |
| 16 | Kayış kolu · tabla · mıknatıs kulağı (kutuya) | kol 3 · tabla 2,5 · kulak 2 + 2 PEM · TIG 3 birleşim |
| 17 | Mıknatıs → kulak | mıknatıs · 2 × ISO 7380 M3 × 8 → 2 × PEM CLS-M3-2 |
| 18 | Köşebentler · kızaklar (montaj alanında) | köşebent × 4 + 4 × ISO 7380 M4 × 6 · kızak × 2 (punta 2 × 2) |
| 19 | Çekmece raylara sürülür | çekmece grubu · 900 mm sürme · ray ekseni z |
| 20 | Kayış · çekmece açılır · çene bloğu | GT3 kayış (sarılır) · çekmece açık · alt gövde · üst çene · 2 × ISO 7380 M3 × 12 · 2 × ISO 4032 M3 |
| 21 | Üretim: ön kapak (8 büküm) · iç panel + PEM · PU | dış kabuk 1,5 (8 büküm) · iç panel 1,0 · 4 × PEM FHS-M5-10 · PU köpük |
| 22 | Ön kapak · fitil · somunlar | fitil · ön kapak (saplamalar) · 4 × DIN 125 M5 · 4 × ISO 4032 M5 |
| 23 | Kablolar | reed sensör kabloları · motor kablosu |

Süre 281 s · 23 adım.
