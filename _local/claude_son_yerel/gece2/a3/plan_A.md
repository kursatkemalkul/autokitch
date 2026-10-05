# A (AÇICI) MONTAJ PLANI v3 — çekmece v3 / B v3 yöntemiyle

Kurallar: MONTAJ_ANIMASYON_KURALLARI.md (W\_local\hat3-v8). Model: hat3_v9l (zincir 00–44) **+ zincir_A_tamamla.py** (aşağıda, A1–A3) → hat3_v9l_A.glb (yalnız S kopyası; ana GLB'ye dokunulmadı).
Gövde: h3_a_sac_v1 (acinim_A: 37 sac açınım + büküm) · parçalar ana modelden adım-33 ent aralıklarıyla (hat3_v9a_ent.json, v9l'de 326/326 geçerli) birebir.
Üreteç: a3/a3_parca.py → a3/a3_montaj.py (plan + zaman) → a3/a3_cikti.py (denetim + GLB/JSON). Oynatıcı: ist_montaj/a3-montaj.js (b3-montaj.js kopyası).
Gösterim: alt montajlar havada (tezgâh YOK) · sac parça kendi yaklaşma çizgisinde düz açınım (lazer) → abkant bükümleri tek tek → PEM preslenir → tek doğru boyunca yerine · birleşimde yakın kamera + "ne ↔ neye, hangi elemanla" · vida / pul / somun turuncu vurgu · kaynakta dikiş belirir.
Çevre: B dolabı silik (A onun üstüne kurulur, baştan görünür); TOPPING sol duvarı + tabla rayı tabanı silik (yalnız hat bağlantısı adımında belirir).
Satın alınan: açıcı (dönme kafası + kolon + motor — TEK ÜRÜN), gizli menteşe (gövde + kanat yarısı), bas-aç, silikon tapa — tek parça, yalnız montajı.
A içinden kablo / kanal / hortum GEÇMEZ (kural) · acil stop YOK.

| # | adım | ne / neyle | yön (açık taraf) |
|---|---|---|---|
| 1 | Kaide çerçevesi | ön + arka boru 100 × 40 × 2 (kesim boyu 690) B tavanına · sol / sağ / enine boru (792) aralarına · boyuna sol / sağ (285) · her uçta 2 TIG köşe dikişi (20) | yukarıdan |
| 2 | Kaide plakası + damlama sacı | 4 mm plaka: lazer (düz) → 4 × PEM SP-M8 (açıcı) + 4 × PEM SP-M6 (ray) ALTTAN preslenir → borulara iner → 16 delik kaynağı · 1,5 mm damlama sacı (lazer, dikme çentikli) → plakaya 9 punta | yukarıdan |
| 3 | A → B bağlantısı | 6 × ISO 7092 M8 pul + ISO 4762 M8 × 25: plaka / damlama / boru üst duvarındaki Ø16'dan iner, boru alt duvarı Ø9 → B dış tavan Ø9 → GFRP → B kirişindeki M8 perçin somun · 6 silikon tapa Ø16'ları kapatır | yukarıdan (−y) |
| 4 | İskelet | 4 köşe dikmesi 30 × 30 × 2 (kesim boyu 1302,5; sol ön dikmede 3 menteşe penceresi + 6 vida deliği, sağ ön dikmede 3 bas-aç deliği) damlama çentiklerinden plakaya · 8 TIG (dikme ↔ damlama + plaka) · 4 tapa (alın kaynağı, taşlanır) · üst halka ön / arka (630) + 4 TIG · sol / sağ (812) + 4 TIG | yukarıdan |
| 5 | Kulaklar | 22 kulak 3 mm (lazer → 1 büküm) dikme / halka iç yüzlerine · her biri 2 TIG | içeriden, yüzeye dik |
| 6 | Sol yan sac | lazer → 2 büküm (arka 22 · ön 16,5) → 8 × PEM FHP-M5-15 dıştan preslenir → saplamalar kulak deliklerine → 8 × (DIN 9021 pul + ISO 10511 somun) İÇERİDEN | soldan (+x) · somun içeriden |
| 7 | Sağ yan sac (tabla geçiş ağzı) | aynı · 8 saplama · 8 pul + somun | sağdan (−x) |
| 8 | Üst sac | lazer → 2 büküm → 6 × FHP-M5-15 → üst halka kulaklarına · 6 pul + somun (alttan) | yukarıdan |
| 9 | Arka sac | lazer → 1 büküm (alt dönüş) → 13 × FHP-M5-12 → yan sacların ve üst sacın arka dönüş deliklerinden · 13 pul + somun içeriden (dikme ↔ arka sac yarığı) | arkadan (+z) |
| 10 | Açıcı | satın alınan TEK ÜRÜN, açık önden 5 mm yukarıda sürülür, damlama sacına iner · 4 × DIN 125 M8 pul + ISO 4762 M8 × 20 → flanş Ø9 → damlama Ø9 → plakanın altındaki PEM SP-M8 | önden (−z) · cıvata üstten |
| 11 | Hat bağlantısı | TOPPING (silik) yanına gelir: 4 × DIN 9021 M8 pul + M8 × 16 A İÇİNDEN sağ yan sacın Ø9'undan → TOPPING sol dış sacındaki PEM SP-M8 · TOPPING ile gelen tabla rayı (silik): 4 × M6 × 16 → ray tabanı Ø6,6 → damlama Ø6,6 → PEM SP-M6 | içeriden (+x) / üstten |
| 12 | Kapak alt montajı (havada, önde) + menteşe gövdeleri | dış tava: lazer → 4 büküm → 4 köşe TIG · iç tava: lazer → 4 büküm → 6 × PEM SP-M5 · 3 karşılık plakası → iç tavaya 2'şer punta · iç tava dış tavanın içine → 30 punta · 3 menteşe kanadı → 6 × ISO 7380 M5 × 6 → PEM · dolapta: 3 menteşe gövdesi sol ön dikmenin penceresine + 6 × ISO 7380 M5 × 12 (içeriden) · 3 bas-aç sağ ön dikmeye (geçme) | önden |
| 13 | Kapak takılır | alt montaj havada 90° açılır, menteşe tarafından yaklaşır, kanatlar gövdelere yukarıdan iner (kaldır-çıkar), kapak kapanır, bas-aç kilitler | menteşe tarafından |

Model açıkları (zincir_A_tamamla.py · S kopyasına uygulandı, ana GLB DEĞİŞMEDİ):
- A1 A → B pulu DIN 9021 Ø24, Ø16 servis deliğinden geçemez → ISO 7092 M8 Ø15 × 1,6, cıvata 0,4 aşağı.
- A2 açıcı cıvatası başı flanştan 1,5 mm havada, DIN 125 pul yok → pul eklendi, cıvata 0,1 yukarı.
- A3 tabla rayı M6 başı ray tabanından 5,0 mm havada → cıvata 5,0 aşağı.
Animasyonda üretilen (modelde yok, beyanlı): damlama sacı 9 punta · iç tava ↔ dış tava 30 punta · karşılık 6 punta (0,1 mm işaret).
