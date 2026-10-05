# TEK ÇEKMECE MONTAJ v3 — DENETİM (4 Eki 2026)

Sayfa: http://127.0.0.1:8766/claude-hat3-v8/otonom/hat/cekmece-montaj.html · süre 281 s · 23 adım · 111 öğe (+ 8 silik çevre)

## SONUÇ: GEÇTİ

| ölçüt | değer |
|---|---|
| yol çakışması (2 mm, üçgen CCD, 1517 çift) | **0** |
| üretim kareleri (büküm / çevirme / PEM) | 0 |
| yerinde belirme | 0 (istisna: kayış, kablolar, kaynak dikişleri, PU köpük) |
| havada | 0 |
| son konum ↔ model hat3_v9l | 79 öğe/grup, en büyük kutu farkı 0.0002 mm |
| son konumda kesişim | yalnız kabul edilen: arka_kasnak ↔ kayis (kayış dişi kasnak dişine oturur (model teması)) |
| ana model B çekmece bölgesi çakışma (cak.py, 21 çekmece, kapalı bileşen çiftleri) | yeni gerçek çakışma **0**; v9k'daki 126 köpük kapağı ↔ PEM çakışması giderildi; kalan 27 = önceden var (kasnak ↔ kayış dişi 21, köpük kapağı ↔ sac 6) |

## VİDA / DELİK / DİŞ (kural 18)

| eleman | delik | karşı diş | kavrama mm | uç taşma mm |
|---|---|---|---|---|
| vida_sol_1 DIN 7991 M5 × 6 | ray dış eleman havşası + ara eleman erişim deliği | PEM SP-M5-1 (bölme sacı) | 2.0 | 0.77 |
| vida_sag_1 DIN 7991 M5 × 6 | ray dış eleman havşası + ara eleman erişim deliği | PEM SP-M5-1 (bölme sacı) | 2.0 | 0.77 |
| vida_sol_2 DIN 7991 M5 × 6 | ray dış eleman havşası + ara eleman erişim deliği | PEM SP-M5-1 (bölme sacı) | 2.0 | 0.77 |
| vida_sag_2 DIN 7991 M5 × 6 | ray dış eleman havşası + ara eleman erişim deliği | PEM SP-M5-1 (bölme sacı) | 2.0 | 0.77 |
| vida_sol_3 DIN 7991 M5 × 6 | ray dış eleman havşası + ara eleman erişim deliği | PEM SP-M5-1 (bölme sacı) | 2.0 | 0.77 |
| vida_sag_3 DIN 7991 M5 × 6 | ray dış eleman havşası + ara eleman erişim deliği | PEM SP-M5-1 (bölme sacı) | 2.0 | 0.77 |
| vida_braket_1 DIN 7991 M5 × 6 | motor braketi tabanı Ø5,5 + havşa | PEM SP-M5-1 (arka iç sac, Ø6,4) | 2.0 | 0.77 |
| vida_braket_2 DIN 7991 M5 × 6 | motor braketi tabanı Ø5,5 + havşa | PEM SP-M5-1 (arka iç sac, Ø6,4) | 2.0 | 0.77 |
| vida_motor_1 DIN 7991 M3 × 6 | motor braketi Ø3,4 + havşa (3 mm sac) | motor yüzü M3 dişli delik (derinlik 5) | 3.0 | -2.0 |
| vida_motor_2 DIN 7991 M3 × 6 | motor braketi Ø3,4 + havşa (3 mm sac) | motor yüzü M3 dişli delik (derinlik 5) | 3.0 | -2.0 |
| vida_motor_3 DIN 7991 M3 × 6 | motor braketi Ø3,4 + havşa (3 mm sac) | motor yüzü M3 dişli delik (derinlik 5) | 3.0 | -2.0 |
| vida_motor_4 DIN 7991 M3 × 6 | motor braketi Ø3,4 + havşa (3 mm sac) | motor yüzü M3 dişli delik (derinlik 5) | 3.0 | -2.0 |
| vida_kose_sol_1 ISO 7380 M4 × 6 | köşebent Ø4,5 | lamada M4 dişli kör delik (5 derin, 6 mm lama) | 4.5 | -0.6 |
| vida_kose_sol_2 ISO 7380 M4 × 6 | köşebent Ø4,5 | lamada M4 dişli kör delik (5 derin, 6 mm lama) | 4.5 | -0.6 |
| vida_kose_sag_1 ISO 7380 M4 × 6 | köşebent Ø4,5 | lamada M4 dişli kör delik (5 derin, 6 mm lama) | 4.5 | -0.6 |
| vida_kose_sag_2 ISO 7380 M4 × 6 | köşebent Ø4,5 | lamada M4 dişli kör delik (5 derin, 6 mm lama) | 4.5 | -0.6 |
| vida_cene_1 ISO 7380 M3 × 12 | tabla + üst çene + ara + alt çene Ø3,4 | ISO 4032 M3 somun (alt çenenin altında) | 2.4 | 0.84 |
| vida_miknatis_1 ISO 7380 M3 × 8 | mıknatıs yarığı Ø3,18 × 7,82 | PEM CLS-M3-2 (kulak 2 mm) | 1.65 | -0.35 |
| vida_reed_arka_1 ISO 7380 M3 × 8 | reed yarığı Ø3,18 × 7,82 | PEM CLS-M3-2 (reed plakası 2 mm) | 1.65 | -0.35 |
| vida_reed_on_1 ISO 7380 M3 × 8 | reed yarığı Ø3,18 × 7,82 | PEM CLS-M3-2 (reed plakası 2 mm) | 1.65 | -0.35 |
| vida_cene_2 ISO 7380 M3 × 12 | tabla + üst çene + ara + alt çene Ø3,4 | ISO 4032 M3 somun (alt çenenin altında) | 2.4 | 0.84 |
| vida_miknatis_2 ISO 7380 M3 × 8 | mıknatıs yarığı Ø3,18 × 7,82 | PEM CLS-M3-2 (kulak 2 mm) | 1.65 | -0.35 |
| vida_reed_arka_2 ISO 7380 M3 × 8 | reed yarığı Ø3,18 × 7,82 | PEM CLS-M3-2 (reed plakası 2 mm) | 1.65 | -0.35 |
| vida_reed_on_2 ISO 7380 M3 × 8 | reed yarığı Ø3,18 × 7,82 | PEM CLS-M3-2 (reed plakası 2 mm) | 1.65 | -0.35 |
| setskur DIN 913 M3 × 4 | kasnak göbeği radyal M3 dişli delik | kasnak göbeği (alüminyum) | 14.0 | 0.0 |
| pem_kapak_sol_1 PEM FHS-M5-10 saplama | braket flanşı Ø5,5 | DIN 125 M5 pul + ISO 4032 M5 somun | 4.7 | 1.3 |
| pem_kapak_sol_2 PEM FHS-M5-10 saplama | braket flanşı Ø5,5 | DIN 125 M5 pul + ISO 4032 M5 somun | 4.7 | 1.3 |
| pem_kapak_sag_1 PEM FHS-M5-10 saplama | braket flanşı Ø5,5 | DIN 125 M5 pul + ISO 4032 M5 somun | 4.7 | 1.3 |
| pem_kapak_sag_2 PEM FHS-M5-10 saplama | braket flanşı Ø5,5 | DIN 125 M5 pul + ISO 4032 M5 somun | 4.7 | 1.3 |

Not: PEM CLS-M3-2 / SP-M5-1 diş boyu sac kalınlığı kadar (2 mm). Reed ve mıknatıs vidalarında kavrama 1,65 mm (< 1×d): reed tarafında vida uzarsa ucu kablo kanalına (x 1463,4), mıknatıs tarafında M3 × 10 ucu çene cıvatasının yoluna giriyor — kural 18 "sacta PEM ile" yorumuyla kabul, Kemal teyidi.
Setskur satırı: kavrama = göbek deliği boyu (14 mm), uç mile basar.

