# GECE 2 · ADIM 1 · TEYİT (yalnız araştırma — modele dokunulmadı) · 3 Eki 2026 23:15

İndirilen belgeler + hesap betiği: `gece2\kaynak\` (abb_ot_kat.pdf, sveba_tp.pdf, klf66_sp.pdf, nle88c.pdf, fm430.pdf, combisteel_tunnel.pdf, firin_ust_isi.py).
Güven: **Y** = üretici belgesinden okundu · **O** = üretici dışı / arama özeti / ikinci el · **D** = bulunamadı, tahmin.
Not: bu makinede yerel DNS kopuktu; sveba / secop / storm sayfaları Google DNS ile indirildi. Sveba kurulum kılavuzu ve JUN-AIR föyü indirilemedi.

---

## 1 · FIRIN (Sveba Dahlen TP10) ÜST YÜZÜ + KABİN TABANI 20 mm TAŞ YÜNÜ

Modeldeki fırın: **Sveba Dahlen TP10** kesiti, boy 1500'e uzatılmış özel sipariş (`firin_tp10_cad_v10.py`, kaynak "Sveba Dahlen 990004-002 (Oca 2024)").
Kabin tabanı kurgusu (`scratchpad\f_kabin_yeni.py`): fırın üst sacı y 1305 → **21 mm hava** → 0,5 mm 304 kılıf → **20 mm taş yünü** (A1, ≥ 100 kg/m³) → 1,5 mm 304 taban (üst 1348). Eski ışınım kalkanlı raf kalktı.
"Isı hesabı yöntemi" `gece\DEGISIKLIKLER.md`'de YOK (dosyada fırın üstü bölümü bulunmadı, f_kabin_yeni.py "gerekçe raporda" diyor ama rapor yok). Yerine aynı zincirdeki `firin_ust_v37\yama_ud.py → isi_dengesi()` yöntemi kullanıldı (seri dirençler, λ 0,040, üst yüz h 4, ε 304 = 0,15).

| değer | sonuç | birim | kaynak | güven |
|---|---|---|---|---|
| TP10 elektrik gücü | 9,5 | kW | Sveba Dahlen "TP Infinity" broşürü 990004-002, s. 7 (sveba.com/wp-content/uploads/2026/07/TP-Pizza-Series_990004-002_EN.pdf) | Y |
| TP10 önerilen sigorta | 25 | A | aynı, s. 7 | Y |
| TP10 bant × boy · ağız yüksekliği · ağırlık | 381 × 1450 · 85 · 160 | mm · mm · kg | aynı, s. 6–7 | Y |
| TP10 yükseklik (ayaklı) / ayak | 599–637 / 82–120 | mm | aynı, s. 6 (gövde 517 = model ile aynı) | Y |
| Ara parça (spacer) | "TP10 ve TP20'de spacer yok"; spacer = duvara hava boşluğu için | — | aynı, s. 6 | Y |
| TP20 = iki TP10 katı üst üste (ara parçasız) | 939–977 yükseklik | mm | aynı, s. 6–7 | Y |
| Dış yüzey için üretici ifadesi | "well-insulated oven chamber … maintains a lower temperature on the outside" (sayı yok) | — | aynı, s. 5 madde 5 | Y |
| **TP10 üst dış yüzey sıcaklığı (çalışırken)** | **BULUNAMADI** · en iyi tahmin **60–100 °C** (400 °C'de) | °C | broşürde yok; kurulum kılavuzu herkese açık değil (sveba.com/en/support/manuals ve service.sveba.com MediaStore'da TP için yalnız görsel var). Tahmin gerekçesi: TP20'de ikinci kat doğrudan birinci katın üstüne oturuyor (üst yüz bir fırın tabanının dayanacağı sıcaklıkta) | D |
| **TP10 yalıtım kalınlığı** | **BULUNAMADI** · gövdeden çıkarım: tünel üstü (y 1095) ile gövde üstü (1305) arası 210 mm, bunun içinde üst IR ısıtıcı + yalıtım | mm | model ölçüsü (föy kesitinden) | D |
| **Üretici üst boşluk / ısı mesafesi** | **BULUNAMADI** (Sveba). Benzer elektrikli tünel fırın: "çevresinde en az 30 cm boş alan, yanıcı malzemeden uzak" | cm | Combisteel 7485.0150–0165 tünel fırın kılavuzu s. 6 (horecakoeling.be/files/products/combisteel/manual-7485-0150-0155-0160-0165.pdf) — başka üretici, yalnız referans | O |
| Kompresör ortam sınırı (fırın üstündeki JUN-AIR) | 0–40 | °C | JUN-AIR OF302-40M kılavuzu s. 6 (manualslib 1617149) — aynı OF302 motor ailesi | O |
| Davlumbaz fanı (kabin havasını emer) | Systemair RS 30-15 sileo · 51 W · 0,224 A · en çok 464 m³/h; modelde işletme noktası 210 m³/h @ 228 Pa | — | shop.systemair.com RS 30-15 sileo (arama özeti) | O |

### Hesap (firin_ust_isi.py) — kabin tabanından kabine giren ısı ve taban üst yüz sıcaklığı
Alan 1,33 m² · boşluk: alttan ısıtılan yatay katman (Globe–Dropkin) + ışınım (ε fırın 0,25 VARSAYIM, kılıf 0,15) · taş yünü λ 0,040 · üst yüz h 4. Isı köprüsü (30 × 30 profiller, yan saclar) DAHİL DEĞİL.

| fırın üstü T_s | kabin havası | yalıtımsız (41,5 boşluk) | **20 mm** | 30 mm | 40 mm |
|---|---|---|---|---|---|
| 60 °C | 40 °C | 41 W · taban 47,8 °C | **22 W · 44,2 °C** | 18 W · 43,4 | 16 W · 42,9 |
| 80 °C | 40 °C | 91 W · 57,2 °C | **47 W · 48,9 °C** | 38 W · 47,2 | 32 W · 46,1 |
| 100 °C | 40 °C | 145 W · 67,3 °C | **73 W · 53,8 °C** | 59 W · 51,1 | 50 W · 49,3 |
| 120 °C | 40 °C | 202 W · 78,0 °C | **100 W · 58,9 °C** | 80 W · 55,2 | 67 W · 52,7 |
| 150 °C | 40 °C | 291 W · 94,9 °C | **142 W · 66,8 °C** | 113 W · 61,4 | 95 W · 57,8 |

- Kabin havasına etkisi küçük: davlumbaz fanı kabini 100–210 m³/h emerse ρc·V = 31–65 W/K → 20 mm'de T_s 100 °C için kabin havası yalnız **+1,1…+2,4 K** (yalıtımsız +2,2…+4,7 K).
- Asıl sınır: **JUN-AIR ortam 40 °C** ve kompresör ayaklarının bastığı taban sacı. 20 mm ile taban üstü ≈ kabin havası + 9…14 K (T_s 80–100 °C) — ayak kauçuğu ve karton için sorun değil; kompresörün emdiği hava kabin havasıdır.
- **ÖNERİ: 20 mm taş yünü YETERLİ** (T_s ≤ ~120 °C aralığında); 30–40 mm'ye çıkmak kabine girişi yalnız 15–25 W azaltır (kabin havası < 0,5 K) — modelde değişiklik gerekmez. **Açık kalan:** TP10 üst yüz sıcaklığı Sveba'ya sorulmalı ya da ilk fırında temas termometresiyle ölçülmeli; T_s > 150 °C çıkarsa 40 mm. Kompresörün 40 °C sınırı fırından değil DÜKKÂN sıcaklığından tehlikede (hafıza: yaz 38–44 °C, klimasız) — kabin havası = oda + ~2 K.

---

## 2 · AKIM HESABI — CİHAZ GÜÇLERİ (föy) + ZİNCİR KOLLARI

Modeldeki güncel cihazlar `otonom/hat3d/v3/parca_kutulari.json` (birim tanımları) + üreteçlerden okundu. B soğutması GÜNCEL modelde **Secop NLE8.8CN** (KLF4.0CND v6'da kalmış eski seçim — "309 W @ 32 °C yetmiyordu").

| istasyon · cihaz (modeldeki) | nominal güç / akım (föy) | koşul | kaynak | güven |
|---|---|---|---|---|
| TOPPING · Secop **KLF6.6CND** R290 CSIR | RLA **2,1 A** · LRA 13,2 A · P 285 W / 1,78 A (Te −10, Tc 55) · en çok 342 W / 1,99 A (Te +7,2, Tc 55) | 220 V 50 Hz | Secop Single Pack 195B4596 föyü (DB 1 Eki 2026) s. 3–4 | Y |
| TOPPING · kondenser fanı (KLF6.6 grubu) | **BULUNAMADI** · ~10–30 W tahmin | — | grup "CU" mu çıplak kompresör mü belirsiz | D |
| TOPPING · 24 V tüm yükler (6 × STP-DRV-4830 + STP-MTR-23079, 2 × San Ace 9WPA1224, valf adası, UPS UB10.242) | NDR-240-24 ile sınırlı: **1,3 A** AC @ 230 V (tam yük, PF > 0,95, η 88,5 %) · inrush 35 A | 240 W çıkış | Mean Well NDR-240-SPEC (arama özeti) | O |
| ⤷ STP-DRV-4830 | 12–48 VDC · 0,35–3,0 A/faz · 3 A hızlı sigorta | — | AutomationDirect STP-DRV-4830 cut sheet | O |
| ⤷ STP-MTR-23079 | 2,8 A/faz · 276 oz-in | — | AutomationDirect ürün sayfası | O |
| ⤷ San Ace 9WPA1224P4G001 (120 mm IP68) | 0,50 A · 12 W @ 24 V · 3,30 m³/dk | — | products.sanyodenki.com (arama özeti) | O |
| TOPPING · X ekseni STP-MTRAC-23078 + STP-DRVAC-24025 (doğrudan şebeke) | sürücü 90–240 VAC, 0,6–2,5 A çıkış, hatta **4 A sigorta** önerisi · giriş akımı **BULUNAMADI** (~0,5–1 A tahmin) | 230 V | AutomationDirect STP-DRVAC-24025 hızlı başlangıç | O / D |
| F · JUN-AIR **OF302-15B** | motor **0,44 kW** (0,6 hp) · akım **BULUNAMADI** (föy indirilemedi; arama özeti "3,4 A @ 230 V 50 Hz", hesapla 0,44 / (0,7 × 0,85 × 230) ≈ 3,2 A) · kalkış akımı bilinmiyor | 230 V 50 Hz | medicalexpo / directindustry JUN-AIR OF302-15B (arama özeti) | O / D |
| F · davlumbaz Systemair RS 30-15 sileo | 51 W · **0,224 A** | 230 V | shop.systemair.com | O |
| F · yükleme bandı NEMA23 (+ sürücü) | sürücü modeli F kutusunda belirsiz · ≤ 100 W tahmin (~0,5 A) | — | — | D |
| K · tüm 24 V yükleri (EC5000, GJ-N21 pompa, S7-1200, SIWAREX, valfler) | NDR-240-24 ile sınırlı: **1,3 A** @ 230 V | — | Mean Well | O |
| ⤷ Interroll EC5000 ø50 IP66 24 V **35 W** (modelde 35 W) | 2,4 A anma · 5,5 A kalkış @ 24 V | 24 V DC | Interroll EC5000_50mm_IP66_EN.pdf (arama özeti) | O |
| B · Secop **NLE8.8CN** R290 CSIR | RLA **2,15 A** · LRA 11,3 A · P 362 W / **2,08 A** (Te −10, Tc 55) · 326 W / 1,95 A (Te −10, Tc 45) | 220 V 50 Hz | Secop föyü 105H6880 (DB 1 Eyl 2019) s. 1, 4 (kaeltetechnik-shop.at kopyası) | Y |
| B · kondenser fanı (CU NLE8.8CN) | **BULUNAMADI** ~10–30 W | — | — | D |
| B · 24 V yükleri (21 × Transmotec PD3665, 4 × 4414 FL, S7-1200, Electromen EM-324C) | NDR-240-24: **1,3 A** @ 230 V | — | Mean Well | O |
| ⤷ ebm-papst 4414 FL | **1,2 W** · 18–28 V | 24 V DC | ebm-papst DC-axial-fan-4414FL-ENU.pdf (arama özeti) | O |
| ⤷ Transmotec PD3665-24-51-BFEC | **BULUNAMADI** (12 V eşi PD3665-12-51-BFEC 2,05 A / 6,54 W) | — | transmotec.com | D |
| E · 48 V (Beckhoff 7 × EL7062 → 13 step) | NDR-240-48: ~**1,3 A** @ 230 V (NDR-240 serisi) · EL7062: kanal başına en çok 5 A, terminal toplamı 6 A | — | Beckhoff EL7062 sayfası (arama özeti) | O |
| E · Oriental PKP268D28M2 (frenli) | 2,8 A/faz · fren 24 V 0,23 A · 0,8 N·m | — | Oriental Motor katalog (arama özeti) | O |
| E · 24 V tarafı (S7-1200 + G/Ç) | PSU modeli "Mean Well 24/48 V" — 24 V kaynak belirsiz · NDR-120 varsayımıyla 1,3 A | — | — | D |
| QR · 12 göz taban ısıtıcısı | **60 W** / göz (12 × 60 = 720 W → 3,1 A) — üretici değil, `qr_cad_v1.py` A × h × ΔT hesabı (h 10, ΔT 35) | 230 V | model hesabı | D |
| QR · APC Back-UPS BX500CI | 500 VA / 300 W · **en çok giriş 2 A** | 230 V | Schneider/APC föyü (reichelt kopyası, arama özeti) | O |
| QR · NDR-120-24 | **1,3 A** @ 230 V (tipik) · 120 W | — | Mean Well NDR-120-SPEC (arama özeti) | O |
| ROBOT rezerv · Fairino FR5 | tipik 260–270 W · tepe **620 W** · kutu 100–240 VAC | — | fairino satıcı sayfaları (arama özeti, değerler kaynaklar arasında 310 / 620 W tepe farklı) | O |
| ANA PANO · NDR-120-24 + RevPi + switch | 1,3 A tipik · pano ısısı ~35 W | 230 V | Mean Well · h3_ana_pano_v1 | O |
| U · 4 × ebm-papst 4414 FL | 4 × 1,2 W = 4,8 W (24 V) | — | ebm-papst | O |
| **TEZGÂH · MEIKO M-iClean US** | **2,7 kW · 14,0 A** (1N 230 V) ya da 6,7 kW 3N 400 V | — | MEIKO teknik veri (arama özeti) + model birimi | O |
| **TEZGÂH · Stiebel Eltron EIL 3 Premium** | **3,53 kW · 15,2 A** · sigorta 16 A | 230 V | stiebel-eltron.com EIL 3 Premium teknik föy (arama özeti) | O |
| F_TP10 fırın (zincir dışı, CEE 32 A) | föy 9,5 kW / 25 A (1450 bant) · 1500 boy ≈ 14 kW VARSAYIM → 400 V 3N'de ≈ 20 A/faz → CEE 32 A yeterli | — | Sveba 990004-002 s. 7 | Y (TP10) / D (1500) |

### Faz akımları — YENİDEN (tek faz, 230 V, en kötü sürekli yük; kalkış ayrı)
| kol · faz | istasyon | SEMA.md | **föyden** | not |
|---|---|---|---|---|
| SOL · L1 | TOPPING | 7,0 A | **≈ 4,6 A** (2,1 + 1,3 + 1,0 + 0,2) | KLF LRA 13,2 A < 1 s |
| SOL · L2 | F (kontrol) | 4,5 A | **≈ 4,1 A** (3,4 + 0,22 + 0,5) | JUN-AIR akımı föyden teyit edilemedi |
| SAĞ · L3 | K | 2,6 A | **≈ 1,3 A** | NDR-240 tavanı |
| SAĞ · L1 | B | 2,2 A | **≈ 3,6 A** (2,15 + 1,3 + 0,2) | SEMA düşük; NLE LRA 11,3 A |
| SAĞ · L2 | E | 3,5 A | **≈ 2,6 A** | |
| SAĞ · L3 | QR | 5,2 A | **≈ 6,4 A** (3,1 + 2,0 + 1,3) | ısıtıcı + UPS şarjı aynı anda |
| SAĞ · L1 | ROBOT rezerv | 6,5 A | **2,7 A** (FR5 tepe) / SEMA rezervi korunursa 6,5 | |

- **Sol kol en yüklü faz: L1 ≈ 4,6 A** (SEMA 7,0) · **Sağ kol en yüklü faz: L1 = 3,6 + 6,5 = 10,1 A** (SEMA 8,7; robot gerçek tepesiyle 6,3 A) · L3 = 1,3 + 6,4 = **7,7 A** (SEMA 7,8).
- Kalkış: sağ L1'de NLE LRA 11,3 A + robot 6,5 A = 17,8 A < 1 s → C eğrisi (manyetik 5–10 × In = 80–160 A) açmaz; termik açmaz. NDR-240 inrush 35 A (ms) aynı.
- **C16 kol sigortası + H07RN-F 5G2,5: YETERLİ** (en yüklü sürekli faz 10,1 A ≈ %63). Gerilim düşümü 9 m · 10 A · 2,5 mm² → 2 × 9 × 10 × 0,0178 / 2,5 = 1,3 V = **%0,56** (SEMA "< %1" doğru).
- Bina (zincir) toplamı faz başına: L1 ≈ 4,6 + 10,1 + pano 1,3 = **16 A**, L2 ≈ 6,7 A, L3 ≈ 7,7 A → iID 40 A / OT40F4 40 A yeterli.
- **SEMA'da OLMAYAN BÜYÜK YÜKLER: bulaşık MEIKO 14,0 A + el evyesi EIL 3 15,2 A** (ikisi birlikte 29 A, tek faz). Zincire bağlanırsa her biri tek başına bir C16 kolunu doldurur → **bina tesisatından ayrı hatlar olmalı** (fırın gibi), ya da MEIKO 3N 400 V sürümü. Şemada yazılı değil — Kemal'e açık soru.
- SEMA'daki B satırı "0,5 kW / 2,2 A" → **0,8 kW / 3,6 A** olmalı; QR "1,2 kW / 5,2 A" → **1,5 kW / 6,4 A**; TOPPING ve K SEMA'da fazla (güvenli taraf).

---

## 3 · ABB ANA ŞALTER (OT40F4N2 + OHYS2AJ + mil)

| değer | sonuç | kaynak | güven |
|---|---|---|---|
| OT40F4N2 sipariş no | 1SCA104932R1001 · 4 kutup · DIN ray (EN 50022) ya da taban · ön kumandalı | ABB katalog 1SCC301020C0201 (library.e.abb.com "ABB_Spinace OT_katEN14.pdf") s. 21 sipariş tablosu; new.abb.com ürün sayfası | Y |
| **Ölçü G × Y × D** | **48 × 68 × 56 mm** (D = montaj yüzeyinden kaplin ucuna: gövde önü 45 + kaplin 11) · ağırlık 0,125 kg | ABB ürün verisi (standardelectricsupply ABB_OT40F4N2_Datasheet.pdf / new.abb.com); katalog s. 72 çizimi (3 kutuplu: 45 / 40 / 68 / 35 ray) | Y |
| Akım | AC-21A 40 A · AC-23A 23 A (s. 21 sipariş tablosu "40/23") · yalıtım 750 V · ön IP20 | katalog s. 21; ABB ürün sayfası | Y |
| **OHYS2AJ** | 1SCA105296R1001 · **seçici tip (selector) kol**, kırmızı-sarı, **IP65**, NEMA 1/3R/12, en çok 3 asma kilit (5–8 mm), AÇIK konumda kapı kilidi (yetkiliyle aşılabilir) · OT16…125F için | katalog s. 43 | Y |
| OHYS2AJ ölçü | ön **□66 mm** · kapıdan öne **34 mm** (kilit kolu dahil 19 + 34 = 53) · kapı arkası 14 mm (M22×1, Ø40) | katalog s. 99 (OH_S2A_ çizimi); s. 72 "OH_S2 = 34,5" | Y |
| **Kapak delik** | **Ø22,5 + 3,2 mm genişlikte kama çentiği** (çentik ucu delik alt kenarından 24,5) | katalog s. 99 | Y |
| **Mil ailesi** | OHYS2AJ (seçici kol) **OXS6X…** mili ister; **OXP6X… tabanca (pistol) kollar içindir** → modeldeki "OXP6X" YANLIŞ AİLE | katalog s. 52 ("For selector type handles … OXS6X" / "For pistol type handles … OXP6X") | Y |
| OXS6X boyları + L aralığı (OT16…40F + OH_S2) | 85 → 107–126 · 105 → 127–146 · 120 → 142–161 · 130 → 152–171 · **160 → 182–201** · 180 → 202–221 · 250 → 272–291 · 330 → 352–371 mm (L = montaj yüzeyi → kapı) | katalog s. 72 tablo; s. 52 sipariş | Y |
| OXP6X boyları (bilgi için) | 150 · 170 · 265 · 400 (OT16…125F pistol) | katalog s. 52 | Y |
| **Panoya göre doğru mil** | montaj plakası önü z −280,5 · kapak dış yüzü −87 → **L = 193,5 mm** (iç yüz −89 → 191,5) → **OXS6X160 (1SCA101656R1001)** · L 182–201 aralığının ortasında | h3_ana_pano_v1.py PLAKA / KAPAK + katalog s. 72 | Y |
| Modele etkisi (yalnız bilgi) | modeldeki şalter 48 × **56 (y)** × **68 (z)** çizilmiş → doğrusu y 68 × z 56 (gövde önü plaka + 45 = −235,5, kaplin −224,5) · sarı plaka 65 → **66** · kol öne 48 → 34 (+19 kol) · mil adı OXP6X → **OXS6X160** | — | — |

---

## 4 · QR MÜŞTERİ PANELİ

Modeldeki parçalar (`qr_cad_v1.py` s. 240–247) üretici seçilmemiş **VARSAYIM zarflar**: yazıcı YOK (DEGISIKLIKLER'deki "tuş/yazıcı" kablosu yalnız tuş takımına gidiyor).

| modeldeki | model zarfı | gerçek ürün önerisi (örnek) | gerçek ölçü | kaynak | güven |
|---|---|---|---|---|---|
| 7" dokunmatik ekran modülü | 175 × 110 × 25 | Raspberry Pi Touch Display 2 (7") | **189,5 × 120 × 15** (kılavuzda 189,32 × 120,24 × 8,55 gövde) · görünür alan 155,5 × 88 · güç host'tan 5 V (ayrı besleme yok) | raspberrypi.com/documentation/accessories/touch-display-2 | Y |
| ⤷ uyarı | | RPi host ister (ana panodaki RevPi Connect 4 HDMI çıkışlı; ayrı RPi gerekebilir) — endüstriyel 7" HMI seçilirse ölçü değişir | | | — |
| Gömme 2D QR okuyucu | 80 × 60 × 45 | Newland **NLS-FM430** (kiosk/kilit dolabı için, telefon ekranından okur) | **41,5 × 49,5 × 24,3** (G × D × Y) · 75 g · 5 V, 277 mA tipik (1,6 W) · USB / RS-232 · IP54 · −20…60 °C · QR alan derinliği 40–210 mm | Newland NLS-FM430 föyü (cdn.barcodesinc.com/…/fm430.pdf) | Y |
| PIN tuş takımı 4 × 4 paslanmaz | 86 × 86 × 30 | Storm Interface 1000 serisi 16 tuş (ör. 1K160103) | panel kesiti **82,5 × 82,5** (1K160103) · USB'li ışıklı 1K16T101 ≈ 118 × 118 × 11 · 24 V 50 mA | Newark / Amazon ürün sayfaları (arama özeti; Storm föyü indirilemedi) | O |
| Yazıcı | YOK | — | — | — | — |

Modele etkisi (yalnız bilgi): ekran zarfı 175 × 110 → **190 × 120** (panel penceresi `PANEL_PENCERE["ekran"]` 165 × 100 → görünür alan 155,5 × 88'e uyuyor) · okuyucu zarfı 80 × 60 × 45 → **42 × 50 × 25** (pencere 70 × 50 yeterli) · tuş takımı ölçüsü Storm föyüyle teyit edilmeli.

---

## ÖZET — DEĞİŞMESİ GEREKENLER
1. **Ana şalter mili: OXP6X → OXS6X160** (OHYS2AJ seçici kol; L 193,5 mm). Şalter çizimi y/z ekseni ters (68 yükseklik, 56 derinlik); kol plakası 66.
2. **SEMA akım tablosu:** B 2,2 → 3,6 A; QR 5,2 → 6,4 A; sağ kol L1 8,7 → 10,1 A — **C16 + 5G2,5 yine yeterli**.
3. **Tezgâh yükleri (MEIKO 14 A + EIL 3 15,2 A) şemada yok** → ayrı bina hattı gerekir; Kemal'e sorulacak.
4. **Fırın üstü 20 mm taş yünü yeterli** (T_s ≤ 120 °C varsayımıyla); TP10 üst yüz sıcaklığı Sveba'dan / ölçümle teyit edilmeli. Kompresörün 40 °C sınırı dükkân sıcaklığına bağlı.
5. QR paneli zarfları gerçek ürünlere göre küçülür/büyür (ekran 190 × 120, okuyucu 42 × 50 × 25).

BULUNAMADI listesi: TP10 üst yüz sıcaklığı · TP10 yalıtım kalınlığı · Sveba kurulum mesafesi · JUN-AIR OF302-15B akımı (föy) · KLF6.6 / NLE8.8 kondenser fanı · STP-DRVAC-24025 giriş akımı · Transmotec PD3665-24-51 akımı · F yükleme bandı sürücüsü · E 24 V güç kaynağı modeli.
