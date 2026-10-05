# A MONTAJ v3 — DENETİM (4 Eki 2026)

Sayfa: http://127.0.0.1:8766/claude-hat3-v8/otonom/hat/a-montaj.html · süre 141 s · 13 adım · 384 öğe (7 silik çevre) · model hat3_v9l (zincir 00–44) + zincir_A_tamamla.py (S kopyası hat3_v9l_A.glb; ana GLB DEĞİŞMEDİ)

## SONUÇ: TEMİZ — kural 17–18 tutuyor (model tamamlaması zincire eklenince ana modelle aynı olur)

| ölçüt | değer |
|---|---|
| yol çakışması (2 mm, üçgen CCD, 736 çift; kapak dönüşü poz-poz) | **0** |
| büküm kareleri (o an görünen parçalara karşı) | 0 sorun |
| yerinde belirme | 0 (istisna: kaynak dikişi ve punta işaretleri birleşme anında büyür; silik çevre) |
| havada | 0 |
| son konumda kesişim (0,3 mm düzlem payı) | 0 çift |
| bükümlü sac (açınımdan kurulan ağ) ↔ model kutusu | en büyük 0.0001 mm |
| son kare ↔ model (tarayıcı, bbox) | 384 öğe, en büyük bbox farkı 0,0005 mm · tarama 0,25 s × 564 kare, konsol hatası 0 |
| plan anı yol seçimi sorunu | 0 |

## VİDA / DELİK / DİŞ (kural 18 · eksen boyunca ölçü, delik geçişi = son konumda kesişim yok)

| eleman | adet | karşı diş | kavrama mm | diş boyu mm | uç taşma mm | delik |
|---|---|---|---|---|---|---|
| ISO 4762 M8 × 25 (+ ISO 7092 pul) | 6 | B kirişi M8 perçin somun | 17.0 | 17.0 | 1.4 | TEMİZ |
| ISO 4762 M8 × 20 (+ DIN 125 pul) | 4 | PEM SP-M8-2 (kaide plakası) | 5.47 | 5.47 | 1.14 | TEMİZ |
| ISO 4762 M6 × 16 | 4 | PEM SP-M6-2 (kaide plakası) | 4.08 | 4.08 | 5.63 | TEMİZ |
| ISO 4762 M8 × 16 (+ DIN 9021 pul) | 4 | TOPPING sol dış sacı PEM SP-M8 | 5.47–6.27 | 5.47–6.27 | 6.11–6.91 | TEMİZ |
| PEM FHP-M5-12 saplama (arka sac) | 13 | ISO 10511 M5 fiberli somun | 5.0 | 5.0 | 2.8 | TEMİZ |
| PEM FHP-M5-15 saplama (yan / üst sac) | 22 | ISO 10511 M5 fiberli somun | 5.0 | 5.0 | 4.3 | TEMİZ |
| ISO 7380 M5 × 12 | 6 | menteşe gövdesi M5 dişi | 7.0 | 8.0 | -1.0 | TEMİZ |
| ISO 7380 M5 × 6 | 6 | PEM SP-M5-1 (iç tava) | 2.0 | 2.0 | 2.47 | TEMİZ |

Notlar: M5 × 6 → PEM SP-M5-1 (1 mm iç tava) kavrama 2,0 = PEM dişinin tamamı (sacta PEM ile, B v3 ray vidalarıyla aynı kabul). M8 × 16 (A → TOPPING) PEM'i 6,1 mm geçer, ucu
TOPPING köpük kapağındaki cebe girer (model böyle; kapalı kapak istenirse M8 × 10 yeter — TOPPING sahibi). M6 × 16 ray cıvatası PEM'i 5,6 mm geçer, plaka altı boş.
Menteşe gövdesi M5 × 12: 8 mm dişin 7'si kavranır, uç gövdede kalır (−1,0).

## MODEL TAMAMLAMA — zincir_A_tamamla.py (S\gece2\a3\, girdi GLB → çıktı GLB, düğüm adı tabanlı)

Ana GLB'ye DOKUNULMADI; betik S kopyasına uygulandı (hat3_v9l → hat3_v9l_A.glb) ve animasyon bu hâle göre kuruldu. Koordinatör zincire ekleyecek.

| # | açık | düzeltme | düğüm |
|---|---|---|---|
| A1 | A → B 6 × M8 × 25 başının altındaki DIN 9021 pul Ø24, kaide borusu / plaka / damlama sacındaki Ø16 servis deliğinden GEÇEMEZ (boru kapalı, kaynaklı) | ISO 7092 M8 küçük seri pul 8,4 / 15 × 1,6; cıvata 0,4 aşağı (kavrama 17) | A_GOVDE__paslanmaz (köşe taşıma) |
| A2 | açıcı kolonu 4 × M8 × 20 başı flanştan 1,5 mm havada; arayüz şartı "M8 + DIN 125", pul yok | DIN 125-1 M8 pul (902,0–903,6) eklendi, cıvata 0,1 yukarı | A_GOVDE__paslanmaz (+1024 üçgen, sona) |
| A3 | tabla rayı 4 × M6 × 16 başı ray tabanından 5,0 mm havada | cıvata 5,0 aşağı (baş ray tabanına; PEM SP-M6 dişi tam, uç 5,6 geçer) | A_GOVDE__paslanmaz |
| A4 | açıcı modelinin taban flanşı 120 × 50 (z −660…−610); A gövdesi 4 köşe Ø9 (90 × 125, z −645 / −520) bekliyor → öndeki 2 cıvata boşluğa basıyordu | temsili ürün flanşı şartnameye göre 120 × 155'e uzatıldı (z −610…−505, 2 × Ø9) — gerçek üründe flanş ya da 8,5 mm adaptör plakası satın alırken doğrulanmalı (Kemal kararı) | TOPPING_MODUL__sac (mek A/Açıcı, +276 üçgen) |

Kendi kontrolü: her işlemde beklenen bileşen sayısı bulunmazsa betik durur; dokunulmayan köşeler bayt aynı kalır; yeni üçgenler primitif sonunda (ent indisleri geçerli).

## BEYANLI KABULLER

- Punta işaretleri modelde yok (h3_a_sac_v1 puntaları yalnız etiket): animasyonda 0,1 mm × Ø5 işaret olarak birleşme anında belirir — damlama sacı 9, iç tava ↔ dış tava 30, karşılık plakaları 6. Son konumda hiçbir parçayla kesişmez.
- Dikme tapası alın kaynağı taşlanır (dikiş katısı yok, tapa vurgulanır). Diğer bütün kaynaklar (kaide 20, delik kaynağı 16, dikme ↔ damlama 8, halka 8, kulak 44, dış tava köşe 4) modeldeki dikişlerdir.
- Arka sacın 13 somunu: saplama dikmenin / kaide borusunun / üst halkanın tam arkasında, eksenden somun takılamaz → pul + somun önce 13,5 mm yarığa yandan sürülür, arka sac arkadan gelir, somun SW8 ile döndürülür (h3_a_sac_v1 notuyla aynı).
- Kapak kaldır-çıkar menteşesi temsili ölçülü (Southco R6 / EMKA 1046 sınıfı): 0–180° dönüş poz denetimi temiz; "pime iner" adımı 25 mm düşey iniş olarak gösterildi.
- Açıcı tek ürün; denetim ağı için kafa ve kolon ayrı düğüm, birlikte hareket eder (sayfada tek ürün).
- Çevre (silik): B dolabının kabuk sacları + üst kiriş + GFRP + perçin somunları baştan; TOPPING gövdesi, sol duvar PEM'leri ve tabla rayı tabanı yalnız 11. adımda (TOPPING sahibi). Çevre yol denetimine engel olarak girer.
- A içinden kablo / kanal / hortum geçmez; acil stop yok.

## GÖRÜNTÜLER (S\gece2\a3\)

- 1_acinim_duz.jpg
- 2_bukum.jpg
- 3_kaide_kaynagi.jpg
- 4_plaka_pem_delik_kaynagi.jpg
- 5_iskelet_birlesimi.jpg
- 6_panel_montaji.jpg
- 7_arka_somun_yarik.jpg
- 8_acici_montaji.jpg
- 9_kapak_alt_montaj.jpg
- 10_kapak_mentese.jpg
- 11_kapak_acik_yaklasir.jpg
- 12_kapak_kapanir.jpg
- 13_bitmis.jpg
