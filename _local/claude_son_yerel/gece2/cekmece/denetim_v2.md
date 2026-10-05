# TEK ÇEKMECE MONTAJ v2 — DENETİM (4 Eki 2026)

Sayfa: http://127.0.0.1:8766/claude-hat3-v8/otonom/hat/cekmece-montaj.html · veri otonom/hat3d/v3/cekmece_montaj/ (GLB 1,47 MB, morph hedefli) · süre 226 s · 20 adım

## SONUÇ: GEÇMEDİ — 2 model açığı (kural 19: Kemal kararı gerekli)

| ölçüt | değer |
|---|---|
| yol çakışması (2 mm, üçgen CCD, 842 çift) | **2** — ikisi de model açığı (A1, A3) |
| üretim kareleri (büküm / çevirme ↔ tezgâh + görünen parçalar) | 0 |
| yerinde belirme | 0 (istisna: kayış, kablolar, kaynak dikişleri) |
| havada | 0 |
| son konum | tarayıcıda 104 öğe, en büyük fark 0,0005 mm; üretilen saclar ↔ model kutu farkı ≤ 0,0001 mm |
| tarayıcı | baştan sona oynatıldı, konsol hatası yok |

## MODEL AÇIKLARI (düzeltilmeden yayın yok)
- **A1 · kayış çenesi ↔ avara kasnağı:** çene (y 457,95–466,5, x 1470,5–1483,5) çekmece sürülürken avara kasnağının (y ≤ 463,5) içinden geçiyor. Kasnak çekmeceden sonra da takılamaz (kapalıyken kutu, açıkken çene kolu yolu kapatıyor). Öneri: çene bloğu kola kaynaklı değil, çekmece açıkken 2 × M3 ile bağlanan ayrı parça.
- **A3 · sensör plakası:** kablo kanalının (ELK_IC) içinde, sensör lamasına bağlı değil (lama ucu 32 mm önde). Bağlantı yapılmadı. Öneri: plakayı kaldır ya da lamayı arka duvara uzatıp plakayla vidala.

## DİĞER AÇIKLAR
- Ray vidası DIN 7991 M5×6 (zincir 43, ayrı commit 3f62a79): uç köpük kapağı tabanına 0,77 mm baskı yapıyor (kapak iç tabanı = PEM arkası) — kapak 1 mm derin olmalı.
- PEM SP-M5/M4 diş boyu 2,0 mm (proje katalog tablosu) < 1×d; kural 18 "sacta PEM ile" diye yorumlandı — teyit gerekir.
- Kızak ↔ lama: modelde bağ yoktu (1 mm temas). Köşebent 1,5 × 4 + ISO 7380 M4×6 eklendi; kızak ↔ köşebent PUNTA önerisi (iç eleman ↔ ara eleman arası 1 mm, vida başı sığmıyor).
- Reed ×2 ve mıknatıs (Littelfuse 59135 / 57135): montaj delikleri / flanş yüzü modelde yok — bağlantısız oturuyor.
- Avara mili ucu E segman (DIN 6799) için 1 mm uzamalı.
- Kör perçin delikleri flanş kenarına 1,35 mm (DFM sınırda).
- Modele eklenecek (çevre): arka iç sacda 2 × PEM SP-M5 + köpük kapağı (motor braketi), ön çerçevede 2 × Ø3,3 perçin deliği. Sütunun dikey kablo kanalı (B_KABLO) tahriklerden sonra takılır (animasyonda yok).
- Ön kapakta PU köpük modelde yok.

## ÜRETİLEN ↔ MODEL KIYAS (hacim farkı = eklenen delikler)
- on_braket_sol: {'kutu_fark': 0.0, 'model_hacim': 4214.0, 'uretim_hacim': 4119.6, 'fark_hacim': 94.4}
- on_braket_sag: {'kutu_fark': 0.0001, 'model_hacim': 4213.8, 'uretim_hacim': 4119.6, 'fark_hacim': 94.5}
- motor_braketi: {'kutu_fark': 0.0001, 'model_hacim': 9140.1, 'uretim_hacim': 8721.2, 'fark_hacim': 467.0}
- sensor_plakasi: {'kutu_fark': 0.0}
- lama_sol: {'kutu_fark': 0.0, 'model_hacim': 63941.0, 'uretim_hacim': 63816.6, 'fark_hacim': 124.2}
- lama_sag: {'kutu_fark': 0.0001, 'model_hacim': 63941.4, 'uretim_hacim': 63816.6, 'fark_hacim': 124.2}
- avara_unitesi: {'kutu_fark': 0.0}
- kutu: {'kutu_fark': 0.0001, 'model_hacim': 829811.8, 'uretim_hacim': 829812.0, 'fark_hacim': 2.2}
- cene: {'kutu_fark': 0.0, 'model_hacim': 5484.4, 'uretim_hacim': 5371.4, 'fark_hacim': 112.9}
- kapak: {'kutu_fark': 0.0, 'not_': 'model ağı kapalı değil (hacim kıyası yapılamaz) — dış kutu kıyaslandı'}

## VİDA / DELİK / DİŞ (kural 18)
| eleman | delik | karşı diş | kavrama mm | uç taşma mm |
|---|---|---|---|---|
| vida_sol_1 DIN 7991 M5 × 6 | ray dış eleman havşası + ara eleman erişim deliği | PEM SP-M5-1 (bölme sacı) | 2.0 | 0.77 |
| vida_sag_1 DIN 7991 M5 × 6 | ray dış eleman havşası + ara eleman erişim deliği | PEM SP-M5-1 (bölme sacı) | 2.0 | 0.77 |
| vida_sol_2 DIN 7991 M5 × 6 | ray dış eleman havşası + ara eleman erişim deliği | PEM SP-M5-1 (bölme sacı) | 2.0 | 0.77 |
| vida_sag_2 DIN 7991 M5 × 6 | ray dış eleman havşası + ara eleman erişim deliği | PEM SP-M5-1 (bölme sacı) | 2.0 | 0.77 |
| vida_sol_3 DIN 7991 M5 × 6 | ray dış eleman havşası + ara eleman erişim deliği | PEM SP-M5-1 (bölme sacı) | 2.0 | 0.77 |
| vida_sag_3 DIN 7991 M5 × 6 | ray dış eleman havşası + ara eleman erişim deliği | PEM SP-M5-1 (bölme sacı) | 2.0 | 0.77 |
| vida_braket_1 DIN 7991 M5 × 6 | motor braketi tabanı Ø5,5 + havşa | PEM SP-M5-1 (arka iç sac, eklendi) | 1.77 | 1.0 |
| vida_braket_2 DIN 7991 M5 × 6 | motor braketi tabanı Ø5,5 + havşa | PEM SP-M5-1 (arka iç sac, eklendi) | 1.77 | 1.0 |
| vida_motor_1 DIN 7991 M3 × 6 | motor braketi Ø3,4 + havşa (3 mm sacta gömme) | redüktör yüzü M3 dişli delik (derinlik 5) | 3.0 | -2.0 |
| vida_motor_2 DIN 7991 M3 × 6 | motor braketi Ø3,4 + havşa (3 mm sacta gömme) | redüktör yüzü M3 dişli delik (derinlik 5) | 3.0 | -2.0 |
| vida_motor_3 DIN 7991 M3 × 6 | motor braketi Ø3,4 + havşa (3 mm sacta gömme) | redüktör yüzü M3 dişli delik (derinlik 5) | 3.0 | -2.0 |
| vida_motor_4 DIN 7991 M3 × 6 | motor braketi Ø3,4 + havşa (3 mm sacta gömme) | redüktör yüzü M3 dişli delik (derinlik 5) | 3.0 | -2.0 |
| vida_kose_sol_1 ISO 7380 M4 × 6 | köşebent Ø4,5 | lamada M4 dişli kör delik (5 derin, 6 mm lama) | 4.5 | -0.6 |
| vida_kose_sol_2 ISO 7380 M4 × 6 | köşebent Ø4,5 | lamada M4 dişli kör delik (5 derin, 6 mm lama) | 4.5 | -0.6 |
| vida_kose_sag_1 ISO 7380 M4 × 6 | köşebent Ø4,5 | lamada M4 dişli kör delik (5 derin, 6 mm lama) | 4.5 | -0.6 |
| vida_kose_sag_2 ISO 7380 M4 × 6 | köşebent Ø4,5 | lamada M4 dişli kör delik (5 derin, 6 mm lama) | 4.5 | -0.6 |
| vida_cene_1 ISO 7380 M3 × 10 | üst çene + ara parça + alt çene Ø3,4 | ISO 4032 M3 somun (alt çenenin altında) | 2.4 | 1.34 |
| vida_cene_2 ISO 7380 M3 × 10 | üst çene + ara parça + alt çene Ø3,4 | ISO 4032 M3 somun (alt çenenin altında) | 2.4 | 1.34 |
| pem_kapak_sol_1 PEM FHS-M5-10 saplama | braket flanşı Ø5,5 | DIN 125 M5 pul + ISO 4032 M5 somun | 4.7 | 1.3 |
| pem_kapak_sol_2 PEM FHS-M5-10 saplama | braket flanşı Ø5,5 | DIN 125 M5 pul + ISO 4032 M5 somun | 4.7 | 1.3 |
| pem_kapak_sag_1 PEM FHS-M5-10 saplama | braket flanşı Ø5,5 | DIN 125 M5 pul + ISO 4032 M5 somun | 4.7 | 1.3 |
| pem_kapak_sag_2 PEM FHS-M5-10 saplama | braket flanşı Ø5,5 | DIN 125 M5 pul + ISO 4032 M5 somun | 4.7 | 1.3 |

## HARİÇ TUTULAN ÇİFTLER
- cevre_sac ↔ vida_braket_1: arka iç sacda PEM deliği modelde yok (eklenecek) — PEM çevrede gösterildi
- cevre_pu ↔ vida_braket_1: köpük kapağı yeri PU'da kesilmedi (çevre, eklenecek)
- cevre_sac ↔ vida_braket_2: arka iç sacda PEM deliği modelde yok (eklenecek) — PEM çevrede gösterildi
- cevre_pu ↔ vida_braket_2: köpük kapağı yeri PU'da kesilmedi (çevre, eklenecek)
- kapak_ic ↔ pem_kapak_sol_1: PEM FHS başı iç panelde kenetli (presleme)
- kapak_ic ↔ pem_kapak_sol_2: PEM FHS başı iç panelde kenetli (presleme)
- kapak_ic ↔ pem_kapak_sag_1: PEM FHS başı iç panelde kenetli (presleme)
- kapak_ic ↔ pem_kapak_sag_2: PEM FHS başı iç panelde kenetli (presleme)
- arka_kasnak ↔ kayis: kayış dişi kasnak dişine oturur (model teması)
- cevre_on_cerceve ↔ percin_1: ön çerçevede Ø3,3 perçin deliği modelde yok (eklenecek)
- cevre_on_cerceve ↔ percin_2: ön çerçevede Ø3,3 perçin deliği modelde yok (eklenecek)
- cevre_kopuk_kapagi ↔ vida_sol_1: M5 × 6 ucu köpük kapağı tabanına 0,77 mm giriyor (onaylı M5 × 6; kapak 1 mm derin olmalı) — AÇIK
- cevre_kopuk_kapagi ↔ vida_sol_2: M5 × 6 ucu köpük kapağı tabanına 0,77 mm giriyor (onaylı M5 × 6; kapak 1 mm derin olmalı) — AÇIK
- cevre_kopuk_kapagi ↔ vida_sol_3: M5 × 6 ucu köpük kapağı tabanına 0,77 mm giriyor (onaylı M5 × 6; kapak 1 mm derin olmalı) — AÇIK
- cevre_kopuk_kapagi ↔ vida_sag_1: M5 × 6 ucu köpük kapağı tabanına 0,77 mm giriyor (onaylı M5 × 6; kapak 1 mm derin olmalı) — AÇIK
- cevre_kopuk_kapagi ↔ vida_sag_2: M5 × 6 ucu köpük kapağı tabanına 0,77 mm giriyor (onaylı M5 × 6; kapak 1 mm derin olmalı) — AÇIK
- cevre_kopuk_kapagi ↔ vida_sag_3: M5 × 6 ucu köpük kapağı tabanına 0,77 mm giriyor (onaylı M5 × 6; kapak 1 mm derin olmalı) — AÇIK

Ekran görüntüleri: v2_acinim_duz · v2_acinim_bukum · v2_kapak_bukum · v2_pem_presleme · v2_vidalama_yakin · v2_profil_birlesim · v2_ray_boyunca_surme · v2_bitmis (.jpg)
