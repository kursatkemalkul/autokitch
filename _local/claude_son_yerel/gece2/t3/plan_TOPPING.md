# TOPPING MONTAJ PLANI v3 — çekmece v3 / B v3 / A v3 yöntemiyle

Kurallar: MONTAJ_ANIMASYON_KURALLARI.md (W\_local\hat3-v8). Model: ajan zincirinin son ham GLB'si (yoksa hat3_v9l) **+ zincir_T_tamamla.py** (aşağıda, T1…) → S kopyası; ana GLB'ye dokunulmaz.
Gövde: h3_topping_sac_v1 (acinim_TOPPING: 43 sac açınım + büküm) · gövde parçaları ana modelden adım-37 ent aralıklarıyla (hat3_v9e_ent.json, 230 parça; v9l'de üçgen sayıları birebir).
Üreteç: t3/t3_parca.py → t3/t3_montaj.py (plan + zaman) → t3/t3_cikti.py (denetim + GLB/JSON). Oynatıcı: ist_montaj/t3-montaj.js (a3-montaj.js kopyası).
Gösterim: alt montajlar havada (tezgâh YOK) · sac parça kendi yaklaşma çizgisinde düz açınım (lazer) → abkant bükümleri tek tek → PEM preslenir → tek doğru (ya da iki bacak) boyunca yerine · birleşimde yakın kamera + "ne ↔ neye, hangi elemanla" · vida / pul / somun turuncu vurgu · kaynakta dikiş / punta belirir.
Çevre (silik): B dolabı (TOPPING onun tavanına kurulur, baştan) · A sağ yanı + F sol yanı yalnız hat bağlantısı adımında.
Satın alınan TEK ÜRÜN (yalnız montajı): 4 UNO (kıyma, kuşbaşı, sos, harç), kaşar + sucuk kaseti, kaset tahrik motorları, soğutma grubu (Secop), 2 evaporatör kaseti (fan + serpantin + PU kaset), valf adası, sürücü kartları / pano cihazları, X ekseni ünitesi (ray + araba + bantlı tabla + motor), menteşe / bas-aç, emiş filtresi, rakorlar.
Acil stop YOK (Kemal kaldırttı; modeldeki ACIL_STOP animasyona alınmaz).

| # | adım | ne / neyle | yön (açık taraf) |
|---|---|---|---|
| 1 | B tavanı hazırlığı | 4 × M8 kapalı perçin somun B üst kirişinin deliklerine (perçin tabancası, sıkılır) | yukarıdan |
| 2 | Kaide çerçevesi | arka boru 100 × 40, sol / sağ / enine boru 40 × 100 (kesim boyu), 3 boyuna boru, enine lama 6 · uçlarda TIG köşe dikişleri | yukarıdan |
| 3 | Kaide plakası + perde + cep taşıyıcı | 2 cep taşıyıcı L (lazer → 1 büküm) borulara punta · menfezli ön perde C (lazer → 2 büküm) önden, borulara punta · 4 mm plaka: lazer → 2 PEM SP-M6 alttan → borulara · 17 delik kaynağı | yukarıdan / önden |
| 4 | TOPPING → B | 4 × (ISO 7092 M8 pul + ISO 4762 M8 × 25) plaka + boru üst duvarındaki Ø16'dan iner → boru alt duvarı Ø9 → B tavanı → perçin somun | yukarıdan (−y) |
| 5 | Dış taban | lazer → 3 büküm → servis PEM SP-M5 × 4 + FHP-M5 × 4 → plakaya · 2 × ISO 4762 M6 × 12 → plaka PEM SP-M6 | yukarıdan |
| 6 | Dış yan sol / sağ + tavan | sol: lazer → 1 büküm → 4 PEM SP-M8 (A) + 2 servis PEM → tabana TIG · köpük kapağı × 2 · sağ: lazer → 1 büküm → 4 PEM SP-M8 (F) + 6 servis PEM + 2 FHP-M5-25 (J1) + 4 FHP-M5 → TIG · tavan: lazer → 3 büküm → 5 servis PEM → yan saclara TIG | yanlardan / yukarıdan |
| 7 | Kuru (teknik) bölme | soğutma cebi (3 büküm + 4 PEM SP-M8 takoz) plaka / taban ağzından cep taşıyıcılara · ayırma perdesi · teknik ön perde (2 büküm) · teknik sağ perde · kuru bölme tabanı (2 büküm + 5 FHP-M5) · punta | yukarıdan / önden |
| 8 | Soğuk oda iç kabuğu | alt sac (2 FHP) · arka dış sac (12 FHP) · 4 evaporatör kanal kovanı (iki L + boyuna TIG) · arka POM geçiş blokları | önden |
| 9 | Yalıtım levhaları + astar | yüzey yüzey: PU levha (ölçüsünde kesilmiş, KESİK levha — büyüme yok) → üstüne o yüzün astar sacı (1,0) → astar köşe TIG: arka → sol → sağ → tavan · yan duvar POM raf burçları içeriden | önden (+z → −z) |
| 10 | Raf + eşik + kovanlar | raf köşebentleri · PU raf levhası · raf (4 büküm + 4 FHP) · arka köşe dolgusu · 6 düşme kovanı (kıyma / kuşbaşı iki L + TIG, sos / harç boru, kaşar / sucuk POM) · dil kanalları · eşik (3 büküm) + yiv dolguları + köşe silikonu · üst raf köşebentleri + üst raf (2 büküm) · ön çerçeve 430 | önden / yukarıdan |
| 11 | Soğutma | soğutma grubu (tek ürün) arkadan cebe, 4 titreşim takozu PEM SP-M8'lere · 2 evaporatör kaseti (tek ürün) arkadan kanal kovanı ağızlarına · bakır hatlar + yoğuşma hortumu (uzar) | arkadan (+z) |
| 12 | Kaset tahrik motorları + UNO arka grupları | kaşar / sucuk tahrik motoru arkadan · 4 UNO pnömatik silindir + duvar flanşı (UNO'dan ayrılmış arka grup) arkadan, mil duvar burcundan geçer, flanş FHP saplamaya | arkadan |
| 13 | Valf adası + hava + elektrik iç | valf adası, hava kanalı + askılar (FHP), hava hortumları (uzar) · iç kablo kanalları + braketler · J1 fiş paneli (sağ yan, FHP-M5-25) · kablolar kanal boyunca (uzar) | arkadan / sağdan |
| 14 | Arka servis sacı alt montajı (havada, arkada) | lazer (düz) → 9 FHP-M5 · pano kutusu + DIN plakası + sürücü kartları + emiş filtresi sacın üstünde | arkada havada |
| 15 | UNO ön grupları + kasetler | 4 UNO ön grubu (hazne + dozaj gövdesi + döner valf + hortum + yayıcı) önden rafa, arka grubun miline · kaşar / sucuk kaseti önden dil kanalından, kaplin motora | önden (−z) |
| 16 | Servis sacı kapanır | alt montaj arkadan gelir · 17 × DIN 7991 M5 × 6 → yan / tavan / taban dönüşündeki PEM SP-M5 | arkadan |
| 17 | X ekseni + kapaklar | X ekseni ünitesi (tek ürün) önden tabla açıklığına · menteşe gövdeleri + bas-aç ön kasaya · K1 / K2 kanatları havada 90° açık, menteşe tarafından takılır, kapanır | önden |
| 18 | Hat bağlantısı | B (baştan silik) · F (silik): 4 × M8 × 16 + pul F içinden sağ yandaki PEM SP-M8'lere · A (silik): sol yandaki PEM SP-M8'ler A içinden (A sayfasında) | yandan |

Bu plan, parça çıkarımı sonrası (t3_parca.py) yol denetiminin bulduğu sıraya göre sadeleştirilir; son hâli sayfadaki adım listesi ve denetim.md'dir.
Model açıkları → zincir_T_tamamla.py (S\gece2\t3\, girdi GLB → çıktı GLB, düğüm adı tabanlı); ana GLB DEĞİŞMEZ.
