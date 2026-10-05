# B (ÇEKMECELİ SOĞUK DOLAP) MONTAJ PLANI v3 — çekmece v3 yöntemiyle

Kurallar: MONTAJ_ANIMASYON_KURALLARI.md. Model: hat3_v9l (zincir 00–44). Gövde sacı: h3_b_sac_v1 (acinim_B: 63 sac, açınım + büküm) · gövde parçaları ana modelden adım-34 ent aralıklarıyla (hat3_v9b_ent.json) birebir alınır.
Üreteç: b3/b3_montaj.py (plan + zaman) → b3/b3_cikti.py (denetim + GLB/JSON). Oynatıcı: ist_montaj/b3-montaj.js (cekmece-montaj.js v3 kopyası).
Gösterim: alt montajlar havada (tezgâh yok) · her sac parça kendi YAKLAŞMA ÇİZGİSİ üzerinde (yerinin üstünde / önünde / arkasında) düz açınım olarak belirir, abkantta bükülür, montaj yönüne çevrilir, sonra tek doğru boyunca yerine iner · birleşimde yakın kamera + "ne ↔ neye, hangi elemanla" · vidalı birleşimde turuncu · kaynakta dikiş belirir.
Satın alınan ürünler (ayak, evaporatör, soğutma grubu, elektrik kutusu, ray ünitesi, motor, sensör) tek parça.

| # | adım | ne / neyle | yön (açık taraf) |
|---|---|---|---|
| 1 | Şase | 2 boy profili 60×60 + 8 çapraz profil (kesim boyu) · uçlarda TIG çevre dikişi (16) · üst duvara 10 × M8 perçin somun (sıkılır) | profiller yukarıdan |
| 2 | Ayaklar | 14 ayarlı ayak · şase altındaki burçlara vidalanır | aşağıdan (+y) |
| 3 | Dış taban | dis_taban_1 / 2 (lazer, düz, delikli) + ek laması (punta 18) | yukarıdan |
| 4 | Modüler iskelet | 6 GFRP takoz · arka / ön merdiven çerçeve · 3 ara dikme (üstte TIG) · taşıyıcı: 7 dikme + üst çerçeve (TIG) · üstte 2 GFRP şerit · 10 + 2 × M8 perçin somun | yukarıdan |
| 5 | Dış kabuk | 12 köşebent (1 büküm) · sol / sağ yan (1 büküm) · arka 1 / 2 (2 büküm) + ek laması | yan / üst: yukarıdan · arka: arkadan |
| 6 | Taban sandviçi | PU taban levhası (kesilmiş) · iç taban 1 / 2 · 10 × M8 şase cıvatası + pul (perçin somunlara) | yukarıdan |
| 7 | Arka + sol duvar sandviçi | PU arka (alçak / yüksek) · iç arka 1 / 2 · PU sol · iç sol duvar (+ 15 PEM SP-M5 + köpük kapağı) · teknik sol duvar | yukarıdan |
| 8 | Bölmeler 1–5 | her bölme: sac A (+ PEM SP-M5 + köpük kapağı preslenir) → kovanlar (1–2 büküm, köşe TIG) → PU levha → sac B (+ PEM) → gider silikonu | yukarıdan |
| 9 | Isı kalkanı + teknik kapama | ısı kalkanı U (2 büküm) + ışınım sacı + 12 PTFE takoz · PU köşe / B5 üst / teknik PU · ara arka sac | yukarıdan |
| 10 | Tavan sandviçi | iç tavan 1 / 2 · PU tavan (3) · dış tavan 1 / 2 + 3 ek laması · ek yeri silikonları | yukarıdan |
| 11 | Ön çerçeve | 430 ferritik çerçeve 1 / 2 + ek laması + derz dolgu şeridi | önden (−z) |
| 12 | Soğutma | 2 evaporatör (tek ürün, kendi braketleriyle) · soğutma grubu (sağ alt bölme) · gider hortumu (kanal boyunca) | önden |
| 13 | Elektrik | B elektrik kutusu + istasyon kutusu · B kablo kanalları (5) · iç kanallar · güç (kırmızı) / bilgi (mavi) kabloları kanal boyunca | önden |
| 14 | Sabit raylar | 42 ray ünitesi (Accuride DZ3832, sütun sütun) · 126 × DIN 7991 M5 × 6 → PEM SP-M5 (her rayda 3) | önden, vida ±x |
| 15 | Tahrik + avara | her çekmece: tahrik ünitesi (motor + braket + kasnak, 2 × M5 × 6 arka PEM'lere) · avara ünitesi (ön çerçeveye içeriden TIG) | önden |
| 16 | Çekmeceler | İLK çekmecenin tam montajı: çekmece sayfası (bağlantı + özet) · 21 çekmece bitmiş alt montaj olarak sütun sütun ray ekseni boyunca sürülür · kayış sarılır · çekmece açılır · kayış çenesi 2 × ISO 7380 M3 × 12 + 2 × M3 somun · kapanır · reed / motor kabloları | önden (−z) |
| 17 | Soğuk depo + ön paneller | depo rayları + depo çekmecesi (ön panel, conta, PU) · soğutma bölmesi ön ızgarası · acil stop | önden |

Ürün YOK (çekmece içerikleri gösterilmez).
Model açığı olarak listelenecekler (bağlantı elemanı modelde yok): dikme / çerçeve ↔ dış taban · evaporatör braketi ↔ iç arka sac · soğutma grubu · elektrik kutusu · kablo kanalları — denetim.md'de.
