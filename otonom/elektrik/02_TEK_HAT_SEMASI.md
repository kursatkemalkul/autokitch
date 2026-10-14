# 02 · TEK HAT ŞEMASI + YÜK TABLOSU (üretildi: elektrik_hesap_v1.py)
Bina 400 V 3F 50 Hz TN-S varsayımı. Kablo renkleri EN 60204-1 (PE sarı-yeşil · N açık mavi · DC kontrol koyu mavi · güç siyah); 3B'deki 'güç kırmızı / bilgi mavi / hava yeşil' yalnız ekran rengidir (STANDART_DURUM §3-13).

```
BİNA DAĞITIM ──► DUVAR PANOSU (Codex · sağ duvar 600×700×250)
                 ├─ iSW 4P 63 A ── iID 4P 63 A 30 mA tip B
                 ├─ iC60N 3P C32 MAKİNE ──► ANA AYIRICI IP65 40 A 4P (QR sağ yanı, kol 1,21 m, 3 asma kilit) ──► ANA PANO (U_F · 638 · 2 ray × 590) iSW 4P 40 A ── iID 4P 40 A 30 mA tip A
                 │                                                                                             ├─ iC60N C16 TOPPING ── Han 10B ──► TOPPING panosu (iDPN C10 · 2 × NDR-240-48 · NDR-120-24)
                 │                                                                                             ├─ iC60N C16 DOLAP  ── Han 10B ──► DOLAP kutusu ──► B panosu (NDR-240-24 · Secop NLE8.8)
                 │                                                                                             ├─ iC60N C16 K      ── Han 10B ──► K panosu (NDR-120-24)
                 │                                                                                             ├─ iC60N C16 E      ── Han 10B ──► E panosu (2×NDR-240-24 · NDR-120-24)
                 │                                                                                             ├─ (ROBOT · QR Harting soketleri: yalnız Han RJ45 = EtherCAT; güç duvar panosundan)
                 │                                                                                             ├─ iDPN  C16 A      ── Han 10B (arka) ──► açıcı (hazır ürün)
                 │                                                                                             └─ iDPN  C6  PANO_24V ──► NDR-120-24 ── QUINT4-CAP ── CX9240 · TwinSAFE · switch
                 ├─ iC60N 3P C32 FIRIN ──► CEE 32 A ──► Sveba TP10 (≈14 kW anma · kendi kumandası)            [AYRI DEVRE — ana panodan geçmez]
                 ├─ iC60N 1P+N C16 QR ──► QR kutusu iC60N C10 (NDR-120-24 · 12 SSR)                            [duvar panosu QR'nin sağında, kısa hat]
                 ├─ iC60N 1P+N C16 ROBOT ──► robot kontrol kutusu (QR rezerv bölmesi, 230 V 10 A)
                 ├─ iC60N 1P+N C16 EKSEN ──► ray servo NDR-480-48 → EL2911 (GS_STO_RAY) → EL7211
                 ├─ iC60N 1P+N C16 TEZGÂH ──► ani ısıtıcı 3,5 kW (+ bulaşık MEIKO M-iClean US ayrı)                       [BİNA — Kemal teyidi]
                 ├─ iC60N 1P+N C10 AYDINLATMA
                 └─ iC60N 1P+N C6  AĞ ──► ER605 router + LTE yedek (QR modemi KALKTI)
F kutusu (F üst kabini, sağ ön kapak arkası): 11 Eki YÖNETİCİ (i) — PASİF geçiş kutusu (davlumbaz fanı C6 + 16 PT 2,5); F G/Ç kartları + yükleme bandı EL7062 + NDR-120-24 E panosunda (W133 sinyal · W134 termokupl · W065 motor).

EtherCAT (Cat.6A, Han RJ45 modülleri): CX9240 X001 ──► F ──► K ──► E ──► QR ──► ROBOT/RAY (hat 1)   ·   CX9240 X000 ──► ana pano EK1100 ──► EK1122 ──► dal A: TOPPING · dal B: B (7 Eki topoloji kararı)
Ethernet (FL SWITCH 1008N): CX ──► router (internet + 4G yedek) · robot TCP · HMI AP · SCADA
Güvenlik (FSoE): EL6910 + 6×EL1904 + 3×EL2904 ANA PANODA · EL2911 güç grubu kesme (STO) HER İSTASYON PANOSUNDA (TOPPING · F · K · E · RAY · QR kapak)  [F yükleme bandı sürücüsü EL7062 + EL2911 F KUTUSUNDA — istasyon = kapalı ürün]
```

## 2.1 Yük tablosu (cihaz başına)
| istasyon | cihaz | adet | V | faz | W / adet | W anma | eşzaman | W eşzaman | kaynak |
|---|---|---|---|---|---|---|---|---|---|
| ANA | Beckhoff CX9240-0215 (tek beyin) | 1 | 24 | DC | 7 | 7 | 1.0 | 7 | [K] Beckhoff CX9240 föyü: maks 7 W |
| ANA | TwinSAFE EL6910 + 6 × EL1904 + 3 × EL2904 | 1 | 24 | DC | 12 | 12 | 1.0 | 12 | [V] E-bus + alan beslemesi ≈ 12 W (klemens föyleri toplanacak) |
| ANA | EK1100 + EL1809/EL2809 (hat sinyalleri: kule, reset, başlat) | 1 | 24 | DC | 4 | 4 | 1.0 | 4 | [V] |
| ANA | Phoenix FL SWITCH 1008N | 1 | 24 | DC | 2.2 | 2.2 | 1.0 | 2 | [K] h3_ana_pano_v1 ISI_W |
| ANA | Mean Well NDR-120-24 kaybı | 1 | 230 | L | 4 | 4 | 1.0 | 4 | [K] η 0,86 (h3_ana_pano_v1) |
| ANA | QUINT4-CAP DC-UPS bekleme | 1 | 24 | DC | 1 | 1 | 1.0 | 1 | [K] |
| ANA | U_F fanları 4 × ebm-papst 4414 FL (STEGO termostatlı) | 4 | 24 | DC | 5 | 20 | 0.5 | 10 | [K] 4414 FL 24 V ≈ 5 W (ebm-papst föyü: teyit) |
| ANA | Işık kulesi + reset lambası | 1 | 24 | DC | 3 | 3 | 1.0 | 3 | [V] |
| TOPPING | Secop KLF6.6CND yoğuşma ünitesi (R290) | 1 | 230 | L | 320 | 320 | 0.6 | 192 | [V] KLF4.8 259 W ölçülü (dükkân ısı 29 Eyl); KLF6.6 ≈ 320 W föyden teyit |
| TOPPING | Evaporatör fanları 2 × San Ace 9WPA 24 V PWM | 2 | 24 | DC | 6 | 12 | 1.0 | 12 | [V] fan föyü |
| TOPPING | Pano filtreli fanı Rittal SK 3237.124 + çıkış filtresi SK 3237.200 (11 Eki ısı bütçesi) | 1 | 24 | DC | 2.4 | 2.4 | 1.0 | 2 | [K] Rittal föyü 2,4 W · 15 m³/sa |
| ROBOT | Robot bölmesi filtreli fanı Rittal SK 3237.124 + SK 3237.200 (11 Eki ısı bütçesi) | 1 | 24 | DC | 2.4 | 2.4 | 1.0 | 2 | [K] Rittal föyü |
| TOPPING | X ekseni Nanotec ST5918S2008-B + NOE2-05-B enkoder (EL7047, 48 V) | 1 | 48 | DC | 90 | 90 | 0.4 | 36 | [P] 90 W sınıfı · hareket oranı sim (Nanotec föyünden teyit) |
| TOPPING | Tabla Nanotec ST5918X2008-A + çevre tahriki i 6,33 (TOPPING 189; EL7047, 48 V · enkoder RLS AksIM-2 → EL5042) | 1 | 48 | DC | 90 | 90 | 0.5 | 45 | [P] 90 W sınıfı (Nanotec föyünden teyit) |
| TOPPING | Sabit tahrik bant motoru (EL7062 kanalı) | 1 | 48 | DC | 60 | 60 | 0.1 | 6 | [K] AX_TOP_BANT |
| TOPPING | Kaşar / sucuk kaset motorları 4 × STP-MTR-23079 (2 × EL7062) | 4 | 48 | DC | 60 | 240 | 0.3 | 72 | [K] AX_TOP_KASAR_* / SUCUK_* |
| TOPPING | 3 × NDR-240-48 güç kaynağı kaybı (11 Eki: kol 2 ikiye bölündü) | 1 | 230 | L | 40 | 40 | 1.0 | 40 | [K] η 0,90 (föy) |
| TOPPING | Valf adası SMC SY3000 12 × 5/2 + 5 döner aktüatör + 2 kesme + fire sileceği | 1 | 24 | DC | 6 | 6 | 1.0 | 6 | [K] SY3120 0,35 W / bobin |
| TOPPING | Sensörler (3 endüktif M12 · tabla sıfır M8 · lazer · 2 kaset var) + EK1100 + EL klemensler | 1 | 24 | DC | 10 | 10 | 1.0 | 10 | [V] |
| TOPPING | Kapak emniyet RSS36 × 2 | 2 | 24 | DC | 1 | 2 | 1.0 | 2 | [K] Schmersal ≤ 0,05 A |
| TOPPING | 48 V STO kontaktör bobinleri 2 × 3RT2316-1BB40 + 2 × 3RT2015-1BB42 + yerel EL2904 / EL1904 | 4 | 24 | DC | 4 | 16 | 1.0 | 16 | [K] Siemens 3RT2 S00 bobin 4 W (3RT2015 föyü; 3RT2316 aynı boy [V]) |
| ROBOT | 48 V STO kontaktör bobinleri 2 × Siemens 3RT2015-1BB42 + yerel EL2904 / EL1904 | 2 | 24 | DC | 4 | 8 | 1.0 | 8 | [K] Siemens föyü bobin 4 W |
| F | Fırın Sveba Dahlen TP10 (özel 1500 gövde) — AYRI CEE 32 A DEVRESİ | 1 | 400 | 3F | 14000 | 14000 | 0.34 | 4760 | [K] anma ≈ 14 kW (9,5 × 1316/892) · çeker 4,7 kW (%34) — dükkân ısı 29 Eyl |
| F | Yükleme bandı STP-MTR-23079 (EL7062 + NDR-120-24 E PANOSUNDA — 11 Eki YÖNETİCİ (i): F üst kabin > 40 °C, F kutusu pasif) → 24 V KARAR; istasyon = kapalı ürün) | 1 | 24 | DC | 60 | 60 | 0.1 | 6 | [K] AX_F_YBANT · tork payı 9,6 (eksen listesi) |
| F | Davlumbaz fanı Systemair RS 30-15 sileo | 1 | 230 | L | 51 | 51 | 1.0 | 51 | [K] 77284 föyü 51 W |
| F | Kompresör JUN-AIR OF302-15B | 1 | 230 | L | 440 | 440 | 0.24 | 106 | [K] 0,44 kW · %24 çalışma (dükkân ısı 29 Eyl) |
| F | F G/Ç grubu E panosunda: EK1100 + EL1809 + EL2809 + EL3314 + EL7062 + EL2911 (TP10 sinyal · fan · termokupl · yükleme bandı) | 1 | 24 | DC | 6 | 6 | 1.0 | 6 | [V] |
| F | Kapak emniyet RSS36 × 2 + acil stop (adım 58) | 1 | 24 | DC | 2 | 2 | 1.0 | 2 | [K] |
| K | Bant: Interroll EC5000 AI Ø50 motorlu rulo | 1 | 24 | DC | 35 | 35 | 0.5 | 18 | [K] EC5000 AI 24 V · 35 W sınıfı (föyden teyit) |
| K | Yağ pompası Micropump GJ-N21 + EagleDrive DEMSE | 1 | 24 | DC | 60 | 60 | 0.2 | 12 | [V] EagleDrive 24 V ≈ 60 W (föy) |
| K | PulsaJet AAB10000 sprey (PWM bobin) | 1 | 24 | DC | 20 | 20 | 0.1 | 2 | [V] Spraying Systems föyü |
| K | Valfler SY3120 × 4 (bıçak in · çek · itici · kilit pimi #3) + AZM40 kilit | 1 | 24 | DC | 4 | 4 | 1.0 | 4 | [K] |
| K | Sensörler: 2 × E3Z-T61 · PM1704 · bıçak üst / kilit · EK1100 + EL1008 + EL2008 + EL4002 + EL3356 | 1 | 24 | DC | 8 | 8 | 1.0 | 8 | [V] |
| E | 13 × STP-MTR-23079 (7 × EL7062, 24 V — 9 Eki karar (a)) — aynı anda ≤ 3 eksen | 3 | 24 | DC | 60 | 180 | 0.5 | 90 | [K] kutu_cad_v13: aynı anda en çok 3 eksen döner |
| E | 2 × NDR-240-24 kaybı | 2 | 230 | L | 20 | 40 | 1.0 | 40 | [V] η ≈ 0,92 (NDR-240-24 föyünden teyit) |
| E | Vakum ünitesi SMC ZK2G15K5RWA-08 valfleri + Z silindir valfi | 1 | 24 | DC | 3 | 3 | 1.0 | 3 | [K] |
| E | Sensörler 15 (E2E-X2MF1 PNP · E3Z-D62 × 2 · ZK2 vakum anahtarı) + EK1100 + EL1809 + EL2809 | 1 | 24 | DC | 10 | 10 | 1.0 | 10 | [V] |
| E | Kapak emniyet RSS36 × 4 | 4 | 24 | DC | 1 | 4 | 1.0 | 4 | [K] |
| B | Secop NLE8.8CN yoğuşma ünitesi (R290) | 1 | 230 | L | 407 | 407 | 0.6 | 244 | [K] 407 W (dükkân ısı 29 Eyl) |
| B | Evaporatör fanları 4 × ebm-papst 4414 FL 24 V | 4 | 24 | DC | 5 | 20 | 1.0 | 20 | [K] teyit |
| B | Çekmece motoru Transmotec PD3665-24 (EL7342, aynı anda 1) | 1 | 24 | DC | 70 | 70 | 0.15 | 10 | [K] 24 V · akım sınırı 3 A (EL7342 3,5 A / kanal) |
| B | NDR-240-24 kaybı | 1 | 230 | L | 18 | 18 | 1.0 | 18 | [K] |
| B | 42 reed + EK1100 + EK1122 + 12 × EP7342-0002 + 5 × EP1809-0021 (kolon kutuları, Us) | 1 | 24 | DC | 15 | 15 | 1.0 | 15 | [V] kutu öz tüketimi; motor akımı ayrı satırda (Up, aynı anda 1 motor) |
| QR | Göz ısıtıcı pedleri 12 × 60 W 230 V (SSR, termostatlı) | 12 | 230 | L | 60 | 720 | 0.3 | 216 | [K] 60 W / göz · ort. 218 W (dükkân ısı 29 Eyl) |
| QR | Kapak motorları 12 × 24 V mini redüktörlü (6 × EL7342, aynı anda 1) | 1 | 24 | DC | 10 | 10 | 0.1 | 1 | [V] |
| QR | Müşteri mandalları 12 × 24 V (it-aç, darbe) | 1 | 24 | DC | 12 | 12 | 0.05 | 1 | [V] |
| QR | QR okuyucu Newland NLS-FM430 (5 V) + PIN tuş takımı Storm 1000 (7" ekran 10 Eki K6 ile KALKTI) | 1 | 24 | DC | 4 | 4 | 1.0 | 4 | [V] FM430 föyü 5 V |
| QR | Filtreli fan 2 × 120 mm 24 V | 2 | 24 | DC | 4 | 8 | 1.0 | 8 | [V] |
| QR | QR kutusu EK1100 + EL1809 × 2 + EL2809 × 2 + 6 × EL7342 + Mean Well NDR-120-24 kaybı — duvar panosu QR C16 | 1 | 230 | L | 10 | 10 | 1.0 | 10 | [V] |
| QR | Müşteri kapısı AZM40 × 12 (kilit + kilit izleme, seri; SF8d → UR düzlemi) | 12 | 24 | DC | 1 | 12 | 1.0 | 12 | [K] |
| ROBOT | Robot kontrol kutusu (Fairino FR5 2 kW mini / UR10e — Codex alanı) — duvar panosu ROBOT C16 | 1 | 230 | L | 410 | 410 | 0.67 | 275 | [K] FR5: tepe 410 W · ortalama 276 W · 176–264 V 10 A |
| ROBOT | Ray ekseni servo (EL7211-0010, 48 V) + NDR-480-48 kaybı — duvar panosu EKSEN C16 | 1 | 230 | L | 250 | 250 | 0.3 | 75 | [V] AM81xx 48 V · ray 0,5 m/s |
| DUVAR | Router TP-Link ER605 + 12 V adaptör + LTE yedek modem | 1 | 230 | L | 15 | 15 | 1.0 | 15 | [V] |
| DUVAR | Dükkân aydınlatması LED | 1 | 230 | L | 124 | 124 | 1.0 | 124 | [V] dükkân ısı 29 Eyl |
| TEZGAH | Ani su ısıtıcı Stiebel Eltron EIL 3 Premium — BİNA AYRI HAT (SABAH soru 4, Kemal teyidi) | 1 | 230 | L | 3500 | 3500 | 0.05 | 175 | [K] EIL 3: 3,5 kW |
| TEZGAH | Bulaşık makinesi MEIKO M-iClean US — BİNA AYRI HAT | 1 | 400 | 3F | 6000 | 6000 | 0.1 | 600 | [V] M-iClean US föyünden güç teyit (model A+B meiko.com doğruladı) |
| DUVAR | Müşteri kioskü Samsung QM32C (LH32QMCEBGCXEN) 32" dikey — ayırıcı duvar | 1 | 230 | L | 55 | 55 | 0.53 | 29 | [K] distribütör föyü: maks 55 W · tipik 29 W · bekleme 0,5 W (Samsung PDF teyit) |
| DUVAR | Bekleme TV'si Samsung QB43C (LH43QBCEBGCXEN) 43" dikey — sağ duvar | 1 | 230 | L | 85 | 85 | 0.7 | 59 | [V] QB43C föyü teyit edilecek |
| DUVAR | Dış cephe şerit ekran LG 37BH7N-H (32:9) — hücre duvarı | 1 | 230 | L | 50 | 50 | 0.8 | 40 | [K] Comsys föyü: maks 50 W · tipik 40 W (LG föyü teyit) |
| DUVAR | Müşteri kapısı sürgü operatörü dormakaba ES 200 (+ TS 93) | 1 | 230 | L | 250 | 250 | 0.2 | 50 | [K] dormakaba ES 200 veri sayfası: 230 V 50/60 Hz · 250 W |
| DUVAR | Interkom 2N IP Verso 2.0 (PoE 802.3af sınıf 0, 12,95 W) — 2. PoE enjektöründen | 1 | 48 | DC | 13 | 13 | 0.6 | 8 | [K] 2N kısa kılavuz: 802.3af sınıf 0 · 12,95 W |
| DUVAR | Wi-Fi AP TP-Link EAP650 (PoE 802.3at, TL-POE160S üstünden, W124) | 1 | 48 | DC | 13.5 | 13.5 | 1.0 | 14 | [K] distribütör föyü: AB 13,5 W |
| DUVAR | 4G yedek Teltonika RUT241 (12 V adaptör) | 1 | 12 | DC | 6.5 | 6.5 | 1.0 | 6 | [V] RUT241 föyü teyit |
| ROBOT | Dükkân bilgisayarı Beckhoff C6030 (QR62 alt servis bölmesi, adım 177) — robot bölmesi NDR-120-24 | 1 | 24 | DC | 96 | 96 | 0.5 | 48 | [K] Beckhoff C6030 ATEX/IECEx kılavuzu: 24 V besleme sigortası ≤ 4 A → en kötü 96 W |
| ROBOT | Robot UPS APC SMT1500I (1500 VA / 1000 W, sağ duvar zemini, adım 177) — bekleme / şarj kaybı | 1 | 230 | L | 30 | 30 | 1.0 | 30 | [V] APC föyü: verim / şarj gücü teyit (UR + C6030 yükü kendi satırlarında, UPS üstünden) |
| TEZGAH | Personel tableti Samsung Galaxy Tab Active5 (SM-X300) — 2 POGO şarj yuvası (tezgâh + A ön yüzü) | 2 | 230 | L | 15 | 30 | 0.5 | 15 | [V] 15 W şarj adaptörü (Samsung EP-T1510) |

## 2.2 Kol akımları (230 V tek faz kollar; DC yükler güç kaynağı η 0,9 ile 230 V'a yansıtıldı)
| kol | W anma | W eşzaman | I anma [A] | I eşzaman [A] | sigorta |
|---|---|---|---|---|---|
| ANA PANO (iç) | 59 | 48 | 0.3 | 0.2 | C16 (1P+N) |
| TOPPING C16 | 947 | 462 | 4.6 | 2.2 | C16 (1P+N) |
| DUVAR PANOSU → ROBOT C16 + EKSEN C16 (Codex) | 808 | 445 | 3.9 | 2.1 | C16 (1P+N) |
| AYRI DEVRE: Fırın Sveba Dahlen TP10 (özel 1500 gövde | 14000 | 4760 | 22.5 | 7.6 | 3P C32 |
| F (fırın ayrı CEE 32 A · F kutusu sinyal + 230 V bina devresi) | 567 | 172 | 2.7 | 0.8 | C16 (1P+N) |
| K C16 | 141 | 48 | 0.7 | 0.2 | C16 (1P+N) |
| E C16 | 259 | 159 | 1.3 | 0.8 | C16 (1P+N) |
| DOLAP C16 | 542 | 313 | 2.6 | 1.5 | C16 (1P+N) |
| DUVAR PANOSU → QR C16 (Codex) | 781 | 254 | 3.8 | 1.2 | C16 (1P+N) |
| duvar panosu AĞ / AYDINLATMA | 616 | 349 | 3.0 | 1.7 | C16 (1P+N) |
| AYRI DEVRE: Ani su ısıtıcı Stiebel Eltron EIL 3 Prem | 3500 | 175 | 16.9 | 0.8 | C20 — KONTROL |
| AYRI DEVRE: Bulaşık makinesi MEIKO M-iClean US | 6000 | 600 | 9.6 | 1.0 | 3P C32 |
| BİNA (ayrı hat) | 30 | 15 | 0.1 | 0.1 | C16 (1P+N) |

**Makine toplamı (ana pano kolları, fırın ve bina hariç):** anma ≈ 4103 W · eşzaman ≈ 1901 W → 3 faza dengeli dağıtımda faz başına ≈ 3.1 A eşzaman (anma 6.6 A). Ana şalter 40 A ve bina 5G6 (≈ 34 A, H07RN-F) yeterli; cos φ ve güç kaynağı tepe akımları (NDR-480-48 açılış) için iC60N C16 eğrisi uygundur. **SABAH 4 Eki şeması ile karşılaştırma:** B 3,6 A · QR 6,4 A · sağ kol 10,1 A · sol kol 4,6 A (belgeye göre düzeltilmiş akımlar) — bu tablo aynı mertebede.

**Faz dağıtımı önerisi (ana pano iC60N'ler):** L1: TOPPING + A · L2: DOLAP + K · L3: E + ROBOT + QR. PANO_24V L1.

## 2.3 Koruma ve kesit seçimi
- Bina → ana ayırıcı → ana pano: H07RN-F 5G6, ≤ 15 m, Iz ≈ 34 A (H07RN-F 6 mm² serbest hava · teyit TS/IEC 60364-5-52), gerilim düşümü %1'in altında.
- İstasyon kolları: iC60N 1P+N C16 + H07RN-F 3G2,5 (Iz ≈ 25 A) · Harting Han E 16 A modülü → **soketin sınırı 16 A**, kol sigortası C16 uygun.
- 48 V motor grupları: TOPPING 2 × NDR-240-48 (2 × 5 A, iki ayrı EL2911 kolu — 7 Eki: NDR-480-48 derinliği 125,2 mm panoya sığmıyordu) · ray NDR-480-48 (10 A) — çıkış kablosu 4 mm², EL2911 10 A sınırı. E'de 2 × NDR-240-48 (5 A × 2) → iki EL2911 grubu ya da tek EL2911 + 10 A toplam kontrolü (AÇIK: eksen oturumu eşzamanlı akım).
- 24 V kontrol: PELV, güvenlik beslemesi ayrı sigortalı (2 A), RSS36 / AZM40 toleransı −15/+10 %.
- Kaçak akım: ana pano iID tip A 30 mA (mevcut); duvar panosunda Codex tip B 63 A — iki RCD seri: seçicilik için üstteki 300 mA tip B gecikmeli olmalı (AÇIK, Codex / elektrikçi).
- PE: her metal gövde + ana pano PE barası + Harting PE çerçevesi; EtherCAT kablo ekranı tek uçtan (pano) topraklanır.
- Fırın 14 kW: bina 3P C32 + CEE 32 A, kendi kumandası, ana panoda yalnız sinyal (F kutusu EK1100).
