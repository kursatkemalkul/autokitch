# AUTOKITCH · ALÇAK HAT · montaj v57 ölçü belgesi (27 Eyl 2026)

Kaynak resimler (Kemal onayladı: "bu teknik resme göre 3D modelle, sitede her şeyi güncelle, kontrol et"):
- FULL_MAKINE/ALCAK_HAT_RESIM1_v4 (teknik_alcak_hat_resim1_v4.py): makinenin ön görünüşü ve kesitleri
- FULL_MAKINE/QR_TEZGAH_v4 (teknik_qr_tezgah_v4.py): QR dolabı, tezgâh, robot çöpü, kablo yolu, deterjan
Bu belge ile resimler çelişirse RESİM geçerlidir. Kemal'in kuralı: ölçüsü alınmış parçanın ölçüsü DEĞİŞTİRİLMEZ, yer bulunamıyorsa söylenir.

## Koordinat
X sağa (0 = hattın sol ucu), Y yukarı (0 = zemin), Z koridora doğru (+), modül ön yüzü z = 0, gövde z −830'a kadar. mm.

## Kotlar (eski → yeni, fark −168)
| ne | v56 | v57 |
|---|---|---|
| düz çizgi = çekmeceli dolap üstü = A, C ve fırın altı | B 1060 · F dolabı 956 | **788** (tek yatay çizgi, basamak yok) |
| A / C mekanizma tabanı (kaide 104 üstü) | 1060 | 892 (= 788 + 104 kaide) |
| disk (TOPPING tablası) | 1168 | 1000 |
| fırın gövdesi | 956–1473 | 788–1305 |
| fırın bandı | 1166 | 998 |
| fırın üstü raf üstü | 1516 | 1348 |
| K istasyon tabanı | 1060 | 892 |
| K bandı / kesme plakası | 1164 | 996 |
| E kutu tepsisi | 1104 | 936 |
| E alt raf | 786–790 | 618–622 |
| E kutu şarjörü yığını | 240–1148 (567 kutu) | 240–980 (462 kutu) |
| makine üstü (bütün istasyonlar) | 2030 | 1862 |
| plint / alt taban çizgisi | 0–123 | 0–123 (değişmez) |
| en alt çekmece önü | 167,5 | 167,5 (değişmez) |

## Çekmeceli dolap (tek parça istasyon, 0–4000 × 830 × 123–788, +3 °C)
Çekmece adımı = HH + 33: pide 108 · lahmacun 93 · tatlı 104 · içecek 159. Yığın 167,5'ten başlar.
- K1 62,5–682,5: 6 × lahmacun (36 top)  → yığın 558 = sınır (L−230)
- K2 717,5–1337,5: 6 × lahmacun
- K3 1372,5–1992,5: 5 × pide (20 top) → boş 18
- K4 2011,5–2500: Secop CU KLF4.0CND 128,5–400,5 (önde) + B panosu (PLC) arkasında (2038–2418 × 132–398, z −790…−667) + kaşar/sucuk deposu 423–669 (GN 1/1-100 + GN 1/2-100, kapaklı) · dar içecek YOK
- K5 2535–3155 (fırın altı): alttan üste pide, pide, pide, tatlı (2 şerit × 6 = 12 kap) → boş 70
- K6 3190–3775 (fırın altı): 3 × içecek (48 kutu, 6 şerit × 8) → boş 21
- PU 60 ısı kalkanı fırın altında dolabın içinde: x 2517–3793, y 728–788
- ŞERİT 3810–4000 (soğuk DEĞİL, 3810'da yalıtımlı ara duvar): ROBOT ÇÖPÜ 15 L kova 3822–3988 × 126–426 × z −20…−420 (poşetli), üstünde 426–785 atma boşluğu, ön yüzde yaylı klape (y ~745)
- Toplam 24 çekmece: pide 8 (160 = 2 gün) · lahmacun 12 (432; 2 gün 400) · içecek 3 (144; 2 gün 139) · tatlı 1 (12; 2 gün 11)
- Soğutma: Secop + 6 kolon evaporatörü (eskiden 4) — kapasite hesabı AÇIK (VARSAYIM)

## A + C (TOPPING) — içleri aynı, 168 aşağı
- A kabini 0–700 × 788–1862; C kabini 700–2500 × 788–1862
- İçlerinde mekanizma kaidesi 788–892 (104) → mekanizma tabanı 892, disk 1000
- A'ya başka hiçbir şey konmaz (Kemal: "orası dolu")
- Aktarma iticisi (itici_cad_v3) 168 aşağı

## F fırın (TP10 1500, 79 öne) — hepsi 168 aşağı
- gövde 788–1305, bant 998, giriş bandı / çıkış plakası 168 aşağı
- fırın üstü raf 1305–1348 (takozlu), üstünde: PİZZA KUTUSU YEDEĞİ 320 (2520–3324 × 1348–1860) · 3336–3598 BOŞ (temizlik tezgâha gitti) · KOMPRESÖR JUN-AIR 3600–3980 × 1348–1858 · DAVLUMBAZ arka yarı 2500–4000 × 1315–1862 × z −830…−425
- F taban dolabı (123–956) KALKAR → yeri çekmeceli dolabın K5, K6 ve şeridi

## K kesme (600) — taban 892, üstü 1862
- K tabanı 889–892; üstündeki her şey (bant, kesici + sprey, yağ tankı, pano, itici) 168 aşağı
- K altı (126–889): BULAŞIK MAKİNESİ MEIKO M-iClean US 460 × 700 × 633, x 4108,5–4568,5 (sağ ön köşe dikmesine yaslı, dikmelerin arasında → kapağı dikmeye çarpmaz), y 126–826, z −12…−645
- bulaşığın solu: önde 77 (4031,5–4108,5), dikmenin arkasında 107 → BOŞ
- DETERJAN + PARLATICI: bulaşığın ARKASINDA tek sıra, raf 325–330 üstünde; kanister (5 L, ~190 × 125 × 285, VARSAYIM) 4060–4250 ve 4270–4460 × 330–615 × z −675…−800; bağlantılar (y ≤ 310) altta kalır; MEIKO arka payı 25 (z −645…−670) korunur

## E kutu katlama (830) — üstü 1862
- alt raf 618–622; üstündeki her şey (kalıp, köprü, kapak, piston, besleyici, pano, kutulama ağzı) 168 aşağı
- şarjör + asansör tabanı yerinde; yığın 240–980 → 462 kutu (+ fırın üstü 320 = 782 = 2,8 gün)
- E altı önde: İÇECEK YEDEĞİ 6 koli (400 × 267 × 123, 24 kutu), 2 sütun × 3 kat: x 4603–5003 ve 5005–5405, y 130–499, z −350…−83 (ön köşe dikmeleri 787 bıraktığı ve kablo_kanali_dikey_alt x 5401–5426 z −50…−25 olduğu için geride) → dolaptaki 144 + 144 = 288 (4 gün 277)

## Robot, ray, kablo
- FR5 yer rayı x 200–5100 (montajdaki yer: ray ekseni z 360 — DEĞİŞMEZ), omuz 970, pratik erişim 779
- ZİNCİR OLUĞU ray boyunca 200–5100, rayın koridor tarafında (z ≈ 490–580), zeminde (y 0–60)
- ENERJİ ZİNCİRİ: sabit ucu ray ortası x 2650, hareketli ucu robot arabasında
- ZEMİN KANALI (kapaklı, üstüne basılır): QR'ın robot tarafından (x ≈ 4800, z 670) zincir oluğuna, koridoru geçer
- ROBOT KABLOSU (kol ↔ kontrol kutusu, tek kablo): gereken ≈ 6,5 m; Fairino standart 4 m YETMEZ → 11 m uzatma ile 15 m (inluxrobotics.eu); artan ≈ 8,5 m QR altında kangal

## QR dolabı (koridorun karşısında, robot yüzü z 670)
- 860 × 520 × 2050; x 4570–5430, z 670 (robot tarafı) … 1190 (müşteri tarafı)
- ayak 0–20 · ALT BÖLME 20–447: ROBOT KONTROL KUTUSU 475 × 423 × 268 (rezerv ölçü, robot tarafında) + kablo kangalı (~8,5 m) · raf 447–450
- 12 GÖZ 2 × 6, göz 380 × 190 × 440, satır adımı 200, 450–1650 (göz tabanları 450, 650, 850, 1050, 1250, 1450)
- raf 1650–1653 · ÜST BÖLME 1653–2048: ANA PANO 400 × 350 × 250 + UPS APC BX500CI 115 × 185 × 213 + QR kilit/kapak kartı (~270 × 200) + modem
- Teknik bölmelerin servis kapağı robot tarafında, müşteri tarafında yalnız göz kapakları
- Erişim (ray ekseni z 360 → QR yüzü 310, göz yanal 200 → yatay 369): dikey ±√(779² − 369²) = ±686 → 284–1656; bilek hedefi = göz tabanı + 100 (VARSAYIM) → 550 … 1550 ✓

## Tezgâh + askı (ön zon, öneri)
- TEZGÂH 600 × 450 × 900: x 3950–4550, z 1429–1879 (ön duvara yaslı); plint 0–100, gövde 100–870, tabla 870–900
- içi: altta TEMİZLİK 2 × 5 L bidon (105–405) + boş · raf 412 · BEZ / ELDİVEN / POŞET kutusu (418–568) + ÇÖP 10 L (418–668) · en üstte KİLİTLİ KİŞİSEL ÇEKMECE (700–855)
- DUVAR ASKISI 1650'de, tezgâhın üstünde, basit (3 kanca)

## Kaldırılan / taşınan (v56 → v57)
- D_TABAN_KABIN, D_SUPURGELIK_KABIN (F dolabı) → yok (çekmeceli dolap 0–4000)
- D_TEMIZLIK → tezgâh · D_DETERJAN → K altı bulaşığın arkası · D_BULASIK → K altı
- D_ROBOT_KONTROL, D_ANA_PANO, D_UPS → QR dolabı
- D_ICECEK_YEDEK_A/B → E altı 6 koli
- B çekmece modülü (store_cad_v5, 0–2500 × 1060) → yeni tek parça dolap (0–4000 × 788)
- QR_DOLABI yer tutucusu (x 4295–5300, z 900–1340) → gerçek QR (x 4570–5430, z 670–1190)

## Kesinleşen kararlar (keşif sonrası, 27 Eyl gece)
- Robot rayı ekseni z 360 KALIR (montaj/pafta değeri; dükkân v13'teki 330 kullanılmaz). QR robot yüzü z 670 → yatay 310.
- A / C: TOPPING CAD (TC, yerel Y) tabanı 892 (TOPPING_MODUL y 892–1862); TU (dünya Y) tek seferde −168 kaydırılır; kaide 788–892.
- K: kesme_cad_v4 = v3 + 168 mm dilim çıkarma (bant 700–868), K tabanı 892, bant 996; kutu_cad_v5'i içe alır (urun_merkez).
- E: kutu_cad_v5 = v4 + dilim (bant 400–568), tepsi 936, alt raf 618–622, şarjör 462 kutu.
- F: firin_tp10_cad_v7 BANT_UST_HAT 998 (mutlak sabitler ona bağlanır) · itici_cad_v4 DISK_UST 1000.
- Bulaşık: BM.X0/Y0/Z0 → x 4108,5–4568,5 (ön dikmelerin arasında), z −12…−645; zemin K'nin alt sacı.
- Deterjan + parlatıcı: bulaşığın arkasında raf 325–330 üstünde, kanister 190 × 125 × 285 (VARSAYIM), x 4060–4250 / 4270–4460, y 330–615, z −675…−800 (K modülünün parçası).
- QR + tezgâh yeni modül "S" (SERVİS / TESLİM) → modul_S.glb; zincir oluğu + enerji zinciri + zemin kanalı + robot kablosu modül "-" (R).
- Zincir oluğu z 485–575 (araba 240–480'in koridor tarafı), x 200–5100, y 0–60; zemin kanalı x 4760–4840, z 575–670, y −60…0.
- Pizza kutusu stoğu 462 + 320 = 782 ≈ 2,8 gün (Kemal'e resimde söylendi, resmi onayladı).
