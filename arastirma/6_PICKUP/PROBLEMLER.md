# 6 · PICKUP — PROBLEM DEFTERİ
Durumlar: **ÇÖZÜLDÜ** · **ÖNERİ VAR** (Kemal onayı bekliyor) · **AÇIK**.
Güncelleme: 7 Eyl 2026

| # | Problem | Durum | Çözüm / Not |
|---|---------|-------|-------------|
| D1 | Kaç dolap lazım (Kemal, 7 Eyl) | ÖNERİ VAR | pickup_dolap_teknik_v1: 20 sipariş/saat pik × 12 dk bekleme = 4 ort., %95 8, +2 geç → 10 gerek, 12 tasarım (2×6) |
| D2 | Dolap boyutu: 3 pide + içecek + tatlı | ÖNERİ VAR | iç 56×36×16: sağ 3 kutu üst üste 13,2; sol 20: 1 L yatık + tatlı 12×12 ya da 2 kutu içecek; 4+ pide → 2 dolap tek kod |
| D3 | Arka kapak / ısıtıcı | ÖNERİ VAR | arka üst menteşeli yaylı klape + mıknatıs kilit, ön kapıyla interlock; ısıtıcı yok: PU 20 mm + 15 dk alınma kuralı + 3 buhar deliği; 20 dk SMS, 45 dk geç listesi |
| D4 | Platform kodu (Getir/Yemeksepeti/Trendyol Go), kurye nasıl açar | ÖNERİ VAR | platformlar dolap kodu üretmez, telefonu maskeler → kodu BEYİN üretir; kendi app SMS/QR + PIN; platform müşterisi ve kurye sipariş no son 4 hane; kamera, 3 yanlışta 2 dk kilit; entegratör (Adisyo/Menulux tipi) ile sipariş BEYİN'e düşer — DOĞRULANACAK: entegratör API'de sipariş no alanı |
| D5 | Robot adresleme | ÖNERİ VAR | kamera yok; BEYİN dolap tablosu (boş/dolu, sensörler) + 12 sabit XYZ hedef + IR "kutu var" |
| D6 | Türkiye'de satan var mı | ÖNERİ VAR | kargo dolabı var (pudo, Easy Point, Kargopark, Zelfbox, Emanetmatik, Fitekno, kutu.tech), iki taraflı yemek dolabı yok; yurt dışı Apex OrderHQ, Hatco Minnow; öneri: kabin entegratörden + kilit kartı (KR-CU16 tipi) + Android kiosk |
| D7 | Müşteri dolabı kapatmazsa / çöp bırakırsa | AÇIK | açık-kaldı sensörü 30 sn uyarı; IR "boş" doğrulaması; eleman haftalık silme; kamera kaydı |
| D8 | Sipariş ekranı ayrı olsun, kuryeyi bloke etmesin, ama her şey bir yerde (Kemal, 7 Eyl) | ÖNERİ VAR | kiosk_siparis_ekrani_v1: cephe 180 = sipariş kiosku 40 (32" + ÖKC POS + fiş, 1–2 dk iş) + PICKUP 140 (10" teslim ekranı, 3 sn iş); BEYİN kioskta değil, PICKUP panosunda; kiosk yedek "Gel-Al/Kurye" tuşu taşır |
| D9 | Fiş / ÖKC zorunluluğu, kağıtsız seçenek | AÇIK | ÖKC entegre POS (Ingenico Move 2500 ÖKC / PAX A920 ÖKC / Hugin) fiş keser; e-Arşiv fatura ile kağıtsız mümkün mü → mali müşavire sorulacak |
| D10 | Kurye kapağı kapatmaz → kendiliğinden kapanmalı; vandalizm (Kemal, 7 Eyl) | ÖNERİ VAR | teslim_dolabi_teknik_v2: gizli yaylı menteşe + amortisör (3 sn soft-close), yaylı dil kendini kilitler; reed 20 sn uyarı / 60 sn "açık" (robot yüklemez); 2 mm 304 kapı, 10 mm bindirme, gizli menteşe, tutamak oyuk, cam yok, torx; kod ünitesi IK10 cam + IK09 metal tuş + kamera |
