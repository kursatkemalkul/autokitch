# TOPPING MONTAJ v3 — ARA DENETİM (4 Eki 2026 · yerel)

## SONUÇ: TEMİZ DEĞİL → YAYIMLANMADI, COMMIT YOK (kural 19)

Model: hat3_v9l + zincir_T_tamamla.py (T1, T2). S kopyası: t3/hat3_v9l_T.glb. Ana GLB DEĞİŞMEDİ.
Ajanın son GLB'si (hat3_v9m/v9n) bu oturum boyunca S\ altında hiç oluşmadı. Son üretim o GLB ile yeniden çalıştırılmalı
(komut sırası aşağıda).
Plan (t3_montaj.py): 18 adım · 366 öğe · 159 s. **Plan anında yol sorunu: 22 parça** (aşağıda). Çıktı (t3_cikti), sayfa ve görüntü üretilmedi.

## Son konumda kesişim (yeni parçalarla, 0,3 mm payla)
Temiz, şu beyanlı / model kaynaklı çiftler dışında:
- Servis sacı 17 × DIN 7991 M5 havşa başı ↔ yan / tavan / taban dönüşü (her biri 2,4 mm³). Baş 2,8 mm; servis sacı 1,5 mm, kalan 1,3 mm dönüşe giriyor. **MODEL AÇIĞI T3:** "çökertme havşa" dönüşte modellenmemiş (Kemal kararı: dönüş de çökertilsin mi, ISO 7380 mi).
- Dış tavan ↔ ön çerçeve 430 (5,3 mm³) ve dış tavan ↔ soğuk arka dış sac (2,6 mm³): sac bindirmeleri, model açığı (küçük).
- Kaset ↔ motor kaplini: geçme (beyanlı).

## Plan anında kalan yol sorunları (22)
| parça | engel | neden / öneri |
|---|---|---|
| kuru bölme tabanı | kondenser kanalı | tabanda kanal için yarık yok; kanal tabandan önce gelirse taban inemiyor → **model açığı** (tabanda arkaya açık yarık ya da kanal 2 parça) |
| PU levha sol | astar arka | kesim / sıra ayarı (aynı yöntemle sağ levha geçiyor), çözülebilir |
| PU raf levhası | raf köşebentleri | köpük köşebendi sarıyor → levhada köşebent cebi açılmalı (T2 gibi çıkarma) |
| UNO sos / harç ön grubu | eşik yiv dolgusu, raf, tavan | harç haznesi tavana 41 mm uzaklıkta, çıkış borusu kovana inmek için 104 mm kalkmalı → **model açığı** |
| UNO harç çıkışı · kaşar / sucuk kaset çıkışı | alt sac, PU raf levhası | çıkış ağzının başı alt sac deliğinden büyük; alttan giremiyor, kaset önden sürülemiyor → **model açığı** (alt sacta öne açık yarık) |
| kaşar / sucuk kaseti | raf, eşik, PU raf | önden sürmede dil, eşik kesiğine sıfır boşlukta / çıkış rafın altında → yukarıdaki açıkla birlikte |
| hava askısı × 2 · hava kanalı × 2 | kondenser kanalı, yoğuşma hortumu, kuru taban saplamaları | sıra sorunu (hava parçaları kondenserden ve hortumdan önce gelmeli) |
| iç kanal (sağ ön) | yan sağ saplamaları | saplama ekseninde (+x) son bacak gerekiyor |
| sensör × 3 (motor yanı) · rakor (kuru taban) | motor, kuru taban | sıra sorunu (motorlardan önce / tabandan önce) |
| X ekseni | M6 başları, ayırma perdesi | ne önden ne A tarafından kayarak giriyor: önden girerken raylar taban saplamasına, motor yan saplamaya çarpıyor (aradaki boşluk 7 mm'den az) → **model açığı** |
| X sensör braketi × 2 | X ekseni | X ekseninden sonra alttan girmeli |

## Model tamamlama: zincir_T_tamamla.py (S\gece2\t3\, giriş GLB → çıkış GLB)
- **T1** TOPPING → B 4 × M8 × 25: DIN 9021 pul (Ø24), kaide plakasındaki Ø16 servis deliğinden geçmiyor. ISO 7092 pul (Ø15 × 1,6) yapıldı, cıvata 0,4 mm aşağı alındı (A1 ile aynı açık).
- **T2** Soğuk oda yalıtımı yerinde köpük tek blok. Dış tavanın dönüşlerini sardığı için (≈ 3,5 cm³) kesilmiş levha olarak takılamıyor. Blok 4 levhaya bölündü (arka / sol / sağ / tavan). Sacla bindiren hacim levhadan çıkarıldı, yani flanş yarığı açıldı. Dış sac yüzüne 0,5 mm yapıştırıcı katmanı, gıda tarafındaki 7 iç köşeye 3 × 3 silikon derz eklendi. Ent indisleri korundu.
- Önerildi, uygulanmadı: T3 (havşa), kuru taban yarığı, alt sac öne açık yarıklar, X ekseni girişi, harç UNO yüksekliği.

## Kemal'in ek istekleri (sonradan geldi)
- (a) Yapıştırıcı ve (c) derz silikonu modele eklendi (T2) ve plana alındı (yeşil, birleşme anında belirir).
- (b) **Yapılmadı:** iç sacın bükümlü flanşla ön çerçeveye / komşu iç saca perçin ya da vidayla bağlanması (plastik ara pul / ısı kesici). Bugünkü üreteçte (h3_topping_sac_v1) astar 4 düz sac, aralarında TIG var. Flanşlı astar ve perçin üreteç değişikliği ister (astar açınımları + perçin yerleri); Kemal'in detay kararıyla yeni bir iş olarak açılmalı.
- Renk lejantı (sarı PU, turuncu takılan, kırmızı kalıcı kaynak, mavi vida, yeşil yapıştırıcı / silikon) ve ham ad içermeyen adım metinleri: oynatıcı henüz kopyalanmadı. Adım ve olay metinleri sade Türkçe yazıldı.

## Yeniden çalıştırma (son GLB gelince)
python zincir_T_tamamla.py <son.glb> hat3_T.glb → python cikar_t.py hat3_T.glb t_bil.pkl → python t3_parca.py hat3_T.glb t_bil.pkl → python t3_montaj.py
(t3_cikti.py henüz yazılmadı · a3_cikti.py uyarlanacak)
