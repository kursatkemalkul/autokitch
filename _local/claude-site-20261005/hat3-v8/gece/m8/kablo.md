# MADDE 8c · KABLO / HORTUM / BORU TARAMASI (hat3_v8x · salt okuma)

Model değiştirilmedi. 325 kablo/hortum/boru bileşeni, 1233 doğru parça tarandı. Tam liste: `kablo.json` (439 bulgu, her biri düğüm · istasyon · konum mm · tür · öneri). Ağırlık: 3 kritik · 2 orta · 1 düşük.

## İSTASYON BAŞINA BULGU SAYISI

| istasyon | toplam | kritik | orta | düşük | en çok |
|---|---|---|---|---|---|
| A | 1 | 0 | 0 | 1 | acik_uzun 1 |
| TOPPING | 18 | 4 | 2 | 12 | acik_uzun 9, paralel 3, kablo_yok 2 |
| F | 14 | 1 | 6 | 7 | acik_uzun 6, bos_rakor 4, kablo_kablo 2 |
| K | 31 | 2 | 3 | 26 | acik_uzun 17, paralel 9, havada_kucuk_parca 3 |
| B | 30 | 1 | 1 | 28 | acik_uzun 22, paralel 5, havada_kelepce 1 |
| U | 7 | 1 | 0 | 6 | acik_uzun 4, paralel 2, havada_kelepce 1 |
| QR | 98 | 14 | 19 | 65 | paralel 42, acik_uzun 23, kablo_kablo 9 |
| ANA_HAT | 231 | 4 | 123 | 104 | paralel 86, kablo_kablo 85, gomulu 22 |
| ROBOT | 8 | 0 | 3 | 5 | egik 2, animasyon 2, kapak 2 |
| TEZGAH | 1 | 0 | 0 | 1 | acik_uzun 1 |

## EN KRİTİK 15

**1. TOPPING x sol limit + x sıfır sensör kabloları YOK** (bulgu no: 435)  
Sensörler (1056 / 1086, 920, −22) yerinde, kablo + 7 kelepçe v8x'te yok; G10 rakoru (1436, 1612, −720) boş. X ekseni kör kalır.  
→ v7 yolunu X motoru kablosuyla aynı hatta spiral demet olarak geri kur: x 886→1388,5 @ y 920/924,5 · z −775 → y 1612 → G10 → pano (1520, 1879,8, −730).

**2. TOPPING pnömatik hortumları yok (valf adası → 4 silindir + 2 spreader)** (bulgu no: 436)  
Ada (1998, 1295, −744) ile silindirler (x 1497 / 1624,5 / 1818,5 / 2250) arasında hortum yok.  
→ Ada → kuru bölme arka duvarı z −820'de tek dikey demet (x 2000, y 1295→1700) → üst raf geçiş contası → silindir hizasında dik iniş.

**3. KLF6.6 soğutma grubu kablosu cihazda bitmiyor** (bulgu no: 7)  
Uç (1700, 1087, −805): 30 mm içinde cihaz yüzü yok, en yakın katı G2 rakoru 14 mm (cihaz kutusu z −785…−478 · kablo 20 mm arkada havada).  
→ Ucu cihazın arka-üst yüzüne al: (1700, 1087, −780) ve 1087→1300 dikey hattı z −780'e kaydır (G2 rakoru da z −780) ya da cihazın kablo çıkış yerini (klemens kutusu) üreticiden al.

**4. Ana hat demetinde kablolar birbirinin İÇİNDEN geçiyor (85 kesişme)** (bulgu no: 27, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39 …)  
Kümeler: üst kanal y 2134–2151 → x 2555–2591, 2904–2936 (UF3/UF4 geçişi, ~20), 3284–3420, 3662–3680, 3972; TOPPING sağ dikey hat x 2423–2457 (y 748–1298); zemin kanalı x 4074–4126 (y 2–12).  
→ Kanal içinde şerit düzeni: güç katı z −810…−760, veri katı z −700…−660 (ayrı kat, EMC de ister); her dal kendi şeridinden DİK çıkar, başka şeridi kesmez — dal sırası = şerit sırası (ilk ayrılan en dış şeritte).

**5. Ana hat A güç + veri A gövde sacını deliksiz geçiyor** (bulgu no: 28, 99)  
(1432,5, 2149–2151, −805 / −817): A_GOVDE paslanmaz sacında delik / rakor yok.  
→ A sağ yan sacına (x 1432,5) 2 × M25 rakor: (y 2150, z −805) ve (y 2150, z −817) — ya da tek M40 çift delikli conta.

**6. Ana hat bina (Ø19,6) KD1 kanal kapağından geçiyor + besleme kanalına gömülü** (bulgu no: 53, 54, 119, 120, 121, 122, 123)  
(2442, 1265, −790) KD1 (x 2421–2449, z −828,3…−788,5) kapağını kesiyor; (2462,5, 1256,5, −814) ana_besleme_kanali duvarına 25 mm gömülü.  
→ Bina hattını KD1'in sağına al: x 2460 (KD1 sağ yüzü 2449 + r 9,8 + 1), z −805; besleme kanalına girişi kanal ağzından yap.

**7. QR kilit kartı uçları ×4 kanal duvarını deliyor ve karta ulaşmıyor** (bulgu no: 3, 4, 5, 6, 19, 20, 21, 22)  
(5160 / 5200 / 5240 / 5280, 1676, 1033,5→1060): kanal#0 duvarı deliksiz, uç kilit kartı elemanlarına 11 mm kala bitiyor.  
→ Uçları z 1071'e (kart yüzü) uzat; kanal#0 yan yüzünde 4 parmak yuvası (x 5160–5280, z 1033,5).

**8. QR UPS uçları ×2 iki ucu da boşta** (bulgu no: 1, 2)  
12 mm'lik eğik parça (4991–5005, 1692–1704, z 816–824 / 846–854): UPS'e de kanala da (9 mm) değmiyor.  
→ UPS çıkışından (QR_UPS x 5005) kanal#0 yan yüzüne dik: x 5005 → 4995, y 1700, z 820 / 850.

**9. QR göz ısıtıcı kabloları ×12 yalnız 3 mm'lik uç** (bulgu no: 437)  
x 4980–4984 / 5006–5010 · y 451…1451 · z 999–1001; panoya giden kablo yok.  
→ Göz sensör kablosunun yolundan kanal#2'ye (x 4994, z 930).

**10. Havada kelepçeler (8)** (bulgu no: 140, 141, 142, 143, 144, 145, 146, 150)  
Valf adası (2201,7, 1295, −732,7) · K giriş alıcı (4193, 1110, −39) · K EC5000 (4374, 1189, −727,6) · B evap fan sağ 2 (3477,5, 476, −768,5) · UF fan emiş 1 (3510, 2048, −790) · QR ana hat ×2 (4956, 1960, 783 / 797) · K hava giriş rakoru (4001, 1809, −770).  
→ Her birinde kelepçe dilini en yakın sac yüzüne uzat (M4 perçin somunu) ya da kabloyu yüzeye yaslayıp kelepçeyi o yüzeye taşı; m7'de taşınan raf / kaset yüzeyleri nedeniyle valf adası kelepçesi tabanı boşta kaldı.

**11. Boş / kaçık rakorlar (kablo geçmiyor)** (bulgu no: 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162 …)  
F üst kabin arka rakorları (2600 / 2630 / 3689, 830 / 1825, −821) · DOLAP kutu rakoru M20 (4295, 603,6, −660; harting iç kablosu 13 mm kaçık) · QR kutu rakorları (4880, 1938 / 1996, 790) · ana ayırıcı rakoru (5491, 1301, 950) · TOPPING pano rakoru (2010,8, 2040, −796) · F rakor (2840, 968, −778) · DOLAP (4240, 665, −592,5) · ana pano Harting ×8 (3472,6 / 3828).  
→ Kabloyu rakor eksenine kaydır (DOLAP harting iç kablosu ucu y 580 → 603,6) ya da kullanılmayan rakor + sac deliğini kaldır.

**12. PulsaJet nozül parçaları havada** (bulgu no: 147, 148, 149)  
(4025, 1143–1175, −170): gövde / kapak / uç hiçbir yere değmiyor; basınç hortumu ucu 11 mm uzakta.  
→ Nozülü yag_basinc_hortumu ucuna (4025, 1210, −192) dirsekle bağla ve K kesici braketine M5 ile vidala.

**13. QR alt arka paneli açılınca dikey kablolara çarpar** (bulgu no: 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434)  
Panel x 4572–5427 · y 21–446 · z 670 (robot tarafına −z açılır, kanat 425); önünde ana hat bina / QR / ROBOT / modem + robot uzatma kabloları x 5350–5400, y 12–60, z 240→640 dikey çıkıyor.  
→ Dikey çıkışları panelin yan dışına (x ≥ 5435) ya da zemin_ustu_kanal_QR_basligi kapaklı kanalının içine al; menteşe tarafını kablo tarafına koy.

**14. Ana hat kabloları kanal duvarlarına gömülü (deliksiz kanal çıkışı)** (bulgu no: 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128 …)  
ana_besleme_kanali x 2423 duvarı (y 745–763, z −614…−709: DOLAP güç, ROBOT güç, modem, DOLAP veri, QR veri 15–20 mm) · üst kanal #0 (x 2002–2110 / 2563 / 2908, y 2104–2144) · zemin kanalı (x 4043–4126, y 2) · bina ayırıcı rakoru (5477, 1103, 937).  
→ Kanal çıkışlarında parmak / kesik (kablo Ø + 2 mm) aç; dalları kanal ağzından (uç kapaktan) çıkar.

**15. Robot kablosu ↔ çekmece K3_hamur_3 çekme yolu** (bulgu no: 421, 422)  
Robot park duruşunda kol kablosu (2710, 395–411, 470) K3_hamur_3 çekmecesinin 430–700 mm açılma yolunda.  
→ Çekmece açılırken robot park yeri x < 2050 ya da > 2790 olmalı (akış kuralı); kablo kol üzerinde kalır.

## DERLİ TOPLU OLMA · DEMET ÖNERİLERİ (istasyon başına)

Kemal: "kablolar neden daha derli toplu değil" — ana neden: üreteç her kabloyu tek tek en kısa dik yolla çekiyor, ortak kanal yalnız TOPPING (KD1/KD2/sürücü), B kolonları ve ana hatta var; paralel giden kablolar 6–50 mm arayla ayrı, açık hatlarda kelepçe az ya da yok.

**TOPPING**
- Sürücü bölgesi (x 1478–1585, y 1270–1536, z −810…−700): 4 kaset motor kablosu (sürücü → KD3, y 1270–1420, 33 mm arayla) tek demet: x 1530 ± 8, y 1270→1420, z −783; kelepçe y 1300 / 1400 (UPS DIN plakası z −826,5).
- Valf adası kablosu (x 1998→2402, y 1295, z −744, 404 mm açık, kelepçesi havada) + şartlandırıcı → ada hava hattı (x 2010→2395, y 1125, z −740): ikisi de x boyunca → kuru bölme arka duvarında ortak 30 × 40 kanal: x 2000–2420, y 1110–1150, z −828…−788 (KD1'e dik bağlanır).
- Sağ cep: tabla boş + x sağ limit (x 2494, y 1070 / 1074,5) zaten çift demet; enerji zinciri demeti (x 2459, y 923,5) + sabit tahrik (x 2459, y 986,5) z −811→−460 iki ayrı açık hat → tek demet x 2459, y 923,5→986,5 arası ortak kelepçe (z −600, −700).
- KLF6.6 kablosu (x 1670, y 1300→1880, z −805, 580 mm açık) + soğutma grubu 1087→1300: sürücü dikey kanalına (x 1523–1553) bağlanmak için y 1300'de x 1670 → 1553'e dik dön; açık hat 580 → 120 mm.

**A**
- X motoru kablosu (A içinde 1968 mm açık: x 888 dikey z −462→−775, x 888→1388,5 @ y 924,5 z −775, y 924,5→1640 @ x 1388,5): A'nın arka-alt köşesinde 30 × 30 kapaklı kanal: x 880–1395, y 905–935, z −790…−760 + dikey x 1380–1395, y 935–1650. Eksik x sol limit / x sıfır kabloları da bu kanala.

**F**
- Kompresör hava ana hattı (y 1809, x 2480→3549, z −740, 1069 mm açık, 0 kelepçe) + K'ye dal (x 3549→3994, z −770, 445 mm) + dikey iniş (x 2485, y 1167→1809): F üst kabin arka duvarında (z −820) P-kelepçe her 250 mm; dal ve ana hat aynı y (1809) → ortak çift kelepçe.
- Davlumbaz fanı kablosu (x 2972→3460 @ y 900 z −780 + x 3460 y 900→1490, 1116 mm açık, 0 kelepçe) + F yükleme bandı motoru (x 2449→2784 @ y 1121,5 z −800): F arka duvarına 25 × 25 kanal x 2449–3460, y 890–910, z −800…−775; dikey kısım x 3450–3470.

**K**
- Arka dikey demet (5 kablo ayrı ayrı, 11–46 mm arayla): giriş alıcı x 4189 · DGRF_SMT8M_0 x 4200 · SMT8M_1 x 4216 · durus alıcı x 4246 — hepsi y 1632–1642, z −731…−429 ve −429…−141. Tek dikey kapaklı kanal 40 × 20: x 4180–4255, y 1625–1650, z −760…−140 (klemens sırası x 4176–4255 hemen altında).
- Y yönü yatay demet: PulsaJet (x 4025, y 1220→1642) + giriş verici (x 4185, y 1210→1534, 13 mm) ve duruş verici (x 4370) + EC5000 bant motoru (x 4374, 10 mm) → iki ortak demet: sol x 4180 ± 5 ve sağ x 4372 ± 5, z −735; kelepçe her 200 mm.
- Hava hortumları X_0 / X_1 (x 4386 / 4392, y 993→1405, 8 mm arayla, 0 kelepçe) tek spiral; DGRF ön / arka (x 4206 / 4226, z −690→−154, 23 mm arayla, 0 kelepçe) tek demet; yağ hortumları (emiş x 4080, dönüş x 4295, basınç x 4355) 0 kelepçe → K arka duvarında (z −825) P-kelepçe her 250 mm.

**B**
- Reed açık kabloları: her kolonda 4–5 kablo (x 806 / 1461 / 2116 / 2771 / 3426, y 271–703) ön → arka z −55→−760, 705–709 mm açık, 0 kelepçe (üreteç 'lamaya kablo bağıyla' diyor ama bağ yok). Kablo bağını modelle: her 150 mm (z −100, −250, −400, −550, −700) lamaya sabit klips; açık + kapalı çifti (6 mm arayla, x 812–988) tek spiral.
- Secop NLE8.8 kablosu (x 4036, z −784→−240, 544 mm açık): teknik sütun dikmesine (x 4030) 2 kelepçe daha (z −400, −600).

**U**
- UF fan kabloları: atış 0 / 1 (y 2040 / 2050, x 2691→3343 ve 2871→3343, 10 mm arayla) ve emiş 0 / 1 (y 2040 / 2050, x 3377→3912) iki ayrı çift: her çift tek spiral demet, y 2045, z −790; ortak kelepçe x 2900, 3150, 3550, 3800 (U_F havalandırma tabanı z −828).

**QR**
- QR arka ana hat (güç ROBOT 3G2,5 + QR güç + 3 Cat6A, x 4983–4995, y 28–1666, z 1002–1045): 5 kablo yan yana ama birbirini 9 noktada kesiyor, ROBOT güç + ROBOT Cat6A kanal#1 duvarını (4983, 293–307, 1045) deliksiz geçiyor → kanal#1 içinde iki kat (güç z 1036–1045, veri z 1002–1020), çıkış parmak yuvasından; 2 havada kelepçe (4955–4956, 1960, 783 / 797) kanal#0 yan yüzüne.
- Göz kabloları (motor / sensör / mandal) kanal#2'ye (x 4995, z 931 / 1079) temiz bağlı; demetleme gerekmez. Yalnız 12 ısıtıcı kablosu eksik (3 mm uç) ve UPS / kilit kartı uçları kopuk (kritik listede).

**ANA_HAT**
- Üst kanal (y 2104–2151, x 1990–4300): 14 kablo aynı kanalda; güç (7) ve veri (7) aynı katta karışık → 85 kesişme. Güç katı z −810…−760, veri katı z −700…−660 (ayrı ayırıcılı kanal); dallar istasyon hizasında kendi şeridinden dik iner: A x 2000, TOPPING x 2084, F x 2845 / 3823, ana pano x 3426–3506, K x 4295, E x 5093.
- TOPPING sağ dikey hat (x 2423–2462, y 745–1300): 7 kablo ana_besleme_kanali duvarına gömülü / birbirini kesiyor → kanal genişliği 40 → 60 mm, kablolar x sırası 2428 / 2438 / 2448 / 2458 sabit, kanaldan çıkış uç kapaktan.
- Zemin kanalı (y 0–123, x 4040–5520): bina + QR güç + ROBOT güç + modem + QR veri x 4043–4126 aralığında birbirini kesiyor; kanala giriş sırası = kanal içindeki yanal sıra.
- ana_hat_F_guc yolu 4725 mm, uçlar arası dik mesafe 2308 mm (oran 2,0): ana pano (3822, 2021, −427) → F (2845, 1041, −780) için üst kanal + TOPPING sağ dikey hat yerine F üst kabin arka duvarından doğrudan (x 3822 → 2845 @ y 1860, z −800) ~1500 mm kısalır.

## KRİTİK + ORTA BULGULAR (kısa liste)

**TOPPING** (6)
- #7 `sureklilik/bosta_uc` kablo_TOPPING_sogutma_grubu_KLF66 @ [1700.0, 1087.0, -804.9] — serbest uç boşta (uç yönü [-0.0, -1.0, -0.0]): uç yüzünün önünde r+4 mm içinde cihaz / kanal / rakor yok · en yakın 14 mm: ELK_TOPPING__rakor/rakor_G2_kuru_bolme_tabani → ucu bağlı olması gereken cihaz yüzüne / kanal parmak yuvasına uzat ya da cihaz taşındıysa yolu yeniden çek
- #116 `gecis/gomulu` kablo_TOPPING_valf_adasi @ [2420.8, 1296.4, -806.5] — kablo ELK_TOPPING__kanal/#2'e gömülü / sürtünüyor (~10 mm boyunca eksenden 0.2 mm'de katı yüzey, r 3.7) → kabloyu yüzeyden r + 0,5 mm uzaklaştır (yüzeye dayalı, içine girmeyen)
- #142 `tutucu/havada_kelepce` ELK_TOPPING__celik/kablo_TOPPING_valf_adasi_kelepce_0 @ [2201.7, 1295.0, -732.7] — kelepçe kabloyu tutuyor ama hiçbir sac / gövdeye değmiyor (0,8 mm içinde yüzey yok) · kablo kablo_TOPPING_valf_adasi → kelepçe dilini en yakın sac yüzüne uzat (M4 vida / perçin somunu) ya da kabloyu yüzeye yasla
- #435 `sureklilik/kablo_yok` kablo_TOPPING_sensor_x_limit_sol + kablo_TOPPING_sensor_x_home @ [1056.0, 920.0, -22.0] — x sol limit (1050–1062 · 914–926 · −25…−19) ve x sıfır (1080–1092) sensörleri yerinde ama KABLOLARI YOK (v7'de vardı: parca_kutulari 'kablo_TOPPING_sensor_x_limit_sol' +  → v7 yolunu geri kur: sensör (1056, 920, −19) → z −13 → x 886 → (x 886→1388,5 @ y 920 · z −775, X motoru kablosunun 4,5 mm yanında spiral demet) → y 161
- #436 `sureklilik/kablo_yok` valf adası → 4 UNO silindiri + sos/harç spreader hava hortumları @ [1998.0, 1295.0, -744.0] — valf adası 12 × 5/2 (x 1998, y 1295, z −744) ile 4 pnömatik silindir (kıyma 1624,5 · kuşbaşı 1818,5 · harç 1497 · sos 2250) ve 2 spreader hava rakoru arasında HİÇ HAVA HO → her silindire 2 × Ø6 PU (A/B portu) + 2 spreader'a 1 × Ø6: adadan +y yukarı kuru bölme arka duvarında (z −820) tek dikey demet (x 2000, y 1295→1700) →
- #438 `gecis/bos_rakor` rakor_G10_A_TOPPING_sensor_0 @ [1436.0, 1612.0, -720.0] — G10 (x sol limit + x sıfır için 2 delikli conta) rakorundan kablo geçmiyor — kablolar modelden düşmüş (yukarıdaki bulgu). → sensör kabloları geri kurulunca bu rakordan geçir; kurulmayacaksa rakor + A sağ levhası / TOPPING sol yan sac deliğini kapat

**F** (7)
- #9 `gecis/kablo_kablo` HAVA_KOMPRESOR__hava_ana#1 @ [3548.9, 1809.0, -740.0] — kablo eksenini başka kablo / hortum kesiyor: HAVA_KOMPRESOR__hava_ana#2 → kesişme noktasında birini ≥ (r1 + r2 + 2) mm kaydır ya da ikisini aynı demete al
- #10 `gecis/kablo_kablo` HAVA_KOMPRESOR__hava_ana#2 @ [3548.9, 1809.0, -427.0] — kablo eksenini başka kablo / hortum kesiyor: HAVA_KOMPRESOR__hava_ana#3 → kesişme noktasında birini ≥ (r1 + r2 + 2) mm kaydır ya da ikisini aynı demete al
- #150 `tutucu/havada_kelepce` K_ELEKTRIK__celik/hava_giris_rakoru @ [4001.0, 1809.1, -770.0] — kelepçe kabloyu tutuyor ama hiçbir sac / gövdeye değmiyor (0,8 mm içinde yüzey yok) · kablo HAVA_KOMPRESOR__hava_ana#5 → kelepçe dilini en yakın sac yüzüne uzat (M4 vida / perçin somunu) ya da kabloyu yüzeye yasla
- #156 `gecis/bos_rakor` ELK_ISTASYON__rakor/#77 @ [2840.0, 967.9, -778.0] — rakor / geçiş elemanından kablo/hortum geçmiyor (en yakın eksen 72 mm: F_bina_230V_davlumbaz) → kabloyu rakor ekseninden geçir ya da rakor + deliği kaldır (kablo taşındıysa yeni geçiş noktasına al)
- #167 `gecis/bos_rakor` F_UST_KABIN__plastik/f_ust_rakor_davlumbaz_fani @ [2600.2, 1825.0, -821.0] — rakor / geçiş elemanından kablo/hortum geçmiyor (en yakın eksen 82 mm: HAVA_KOMPRESOR__hava_ana#0) → kabloyu rakor ekseninden geçir ya da rakor + deliği kaldır (kablo taşındıysa yeni geçiş noktasına al)
- #168 `gecis/bos_rakor` F_UST_KABIN__plastik/f_ust_rakor_sinyal_firin @ [2630.2, 830.0, -821.0] — rakor / geçiş elemanından kablo/hortum geçmiyor (en yakın eksen 37 mm: F_firin_sinyal) → kabloyu rakor ekseninden geçir ya da rakor + deliği kaldır (kablo taşındıysa yeni geçiş noktasına al)
- #169 `gecis/bos_rakor` F_UST_KABIN__plastik/f_ust_rakor_kompresor @ [3689.2, 1825.0, -821.0] — rakor / geçiş elemanından kablo/hortum geçmiyor (en yakın eksen 54 mm: HAVA_KOMPRESOR__hava_ana#5) → kabloyu rakor ekseninden geçir ya da rakor + deliği kaldır (kablo taşındıysa yeni geçiş noktasına al)

**K** (5)
- #143 `tutucu/havada_kelepce` ELK_K__celik/kablo_K_urun_sensoru_giris_alici_kelepce_0 @ [4193.0, 1110.0, -39.1] — kelepçe kabloyu tutuyor ama hiçbir sac / gövdeye değmiyor (0,8 mm içinde yüzey yok) · kablo kablo_K_urun_sensoru_giris_alici → kelepçe dilini en yakın sac yüzüne uzat (M4 vida / perçin somunu) ya da kabloyu yüzeye yasla
- #144 `tutucu/havada_kelepce` ELK_K__celik/kablo_K_EC5000_bant_motoru_kelepce_0 @ [4374.0, 1189.0, -727.6] — kelepçe kabloyu tutuyor ama hiçbir sac / gövdeye değmiyor (0,8 mm içinde yüzey yok) · kablo kablo_K_EC5000_bant_motoru → kelepçe dilini en yakın sac yüzüne uzat (M4 vida / perçin somunu) ya da kabloyu yüzeye yasla
- #147 `tutucu/havada_kucuk_parca` K_YAG__celik/PulsaJet_AAB10000AUH-104210-VIFC @ [4025.0, 1174.8, -170.0] — küçük çelik/plastik parça hiçbir şeye değmiyor ve kabloya da ait değil (en yakın kablo yüzeyi 11 mm: yag_basinc_hortumu_TLM1008) → sahipsiz parça: kablo taşınmasından artık kaldıysa sil
- #148 `tutucu/havada_kucuk_parca` K_YAG__celik/PulsaJet_kapak_CP104218-SS @ [4025.0, 1150.5, -170.0] — küçük çelik/plastik parça hiçbir şeye değmiyor ve kabloya da ait değil (en yakın kablo yüzeyi 63 mm: yag_basinc_hortumu_TLM1008) → sahipsiz parça: kablo taşınmasından artık kaldıysa sil
- #149 `tutucu/havada_kucuk_parca` K_YAG__celik/PulsaJet_uc_TPU11002_PWMD @ [4025.1, 1143.3, -170.0] — küçük çelik/plastik parça hiçbir şeye değmiyor ve kabloya da ait değil (en yakın kablo yüzeyi 70 mm: yag_basinc_hortumu_TLM1008) → sahipsiz parça: kablo taşınmasından artık kaldıysa sil

**B** (2)
- #145 `tutucu/havada_kelepce` ELK_DOLAP__celik/kablo_DOLAP_evap_fan_sag_2_kelepce_0 @ [3477.5, 476.1, -768.5] — kelepçe kabloyu tutuyor ama hiçbir sac / gövdeye değmiyor (0,8 mm içinde yüzey yok) · kablo kablo_DOLAP_evap_fan_sag_2 → kelepçe dilini en yakın sac yüzüne uzat (M4 vida / perçin somunu) ya da kabloyu yüzeye yasla
- #166 `gecis/bos_rakor` ELK_ISTASYON__rakor/DOLAP_kutu_rakoru_M20 @ [4295.0, 603.6, -660.2] — rakor / geçiş elemanından kablo/hortum geçmiyor (en yakın eksen 24 mm: DOLAP_harting_ic_kablo) → kabloyu rakor ekseninden geçir ya da rakor + deliği kaldır (kablo taşındıysa yeni geçiş noktasına al)

**U** (1)
- #146 `tutucu/havada_kelepce` ELK_ISTASYON__celik/UF_fan_emis_1_kablosu_kelepce_0 @ [3510.3, 2047.9, -790.0] — kelepçe kabloyu tutuyor ama hiçbir sac / gövdeye değmiyor (0,8 mm içinde yüzey yok) · kablo UF_fan_emis_1_kablosu → kelepçe dilini en yakın sac yüzüne uzat (M4 vida / perçin somunu) ya da kabloyu yüzeye yasla

**QR** (33)
- #1 `sureklilik/bosta_uc` qrk_ups_ucu_0 @ [4990.8, 1700.8, 819.4] — serbest uç boşta (uç yönü [-0.9, 0.4, -0.1]): uç yüzünün önünde r+4 mm içinde cihaz / kanal / rakor yok · en yakın 9 mm: ELK_QR_KABLO__kanal/#0 → ucu bağlı olması gereken cihaz yüzüne / kanal parmak yuvasına uzat ya da cihaz taşındıysa yolu yeniden çek
- #2 `sureklilik/bosta_uc` qrk_ups_ucu_1 @ [4990.8, 1700.8, 849.4] — serbest uç boşta (uç yönü [-0.9, 0.4, -0.1]): uç yüzünün önünde r+4 mm içinde cihaz / kanal / rakor yok · en yakın 9 mm: ELK_QR_KABLO__kanal/#0 → ucu bağlı olması gereken cihaz yüzüne / kanal parmak yuvasına uzat ya da cihaz taşındıysa yolu yeniden çek
- #3 `sureklilik/bosta_uc` qrk_kart_ucu_0 @ [5160.0, 1676.0, 1060.0] — serbest uç boşta (uç yönü [0.0, 0.0, 1.0]): uç yüzünün önünde r+4 mm içinde cihaz / kanal / rakor yok · en yakın 11 mm: QR_KILIT_KARTI__kart/kilit_karti_elemanlari → ucu bağlı olması gereken cihaz yüzüne / kanal parmak yuvasına uzat ya da cihaz taşındıysa yolu yeniden çek
- #4 `sureklilik/bosta_uc` qrk_kart_ucu_1 @ [5200.0, 1676.0, 1060.0] — serbest uç boşta (uç yönü [0.0, 0.0, 1.0]): uç yüzünün önünde r+4 mm içinde cihaz / kanal / rakor yok · en yakın 11 mm: QR_KILIT_KARTI__kart/kilit_karti_elemanlari → ucu bağlı olması gereken cihaz yüzüne / kanal parmak yuvasına uzat ya da cihaz taşındıysa yolu yeniden çek
- #5 `sureklilik/bosta_uc` qrk_kart_ucu_2 @ [5240.0, 1676.0, 1060.0] — serbest uç boşta (uç yönü [0.0, 0.0, 1.0]): uç yüzünün önünde r+4 mm içinde cihaz / kanal / rakor yok · en yakın 11 mm: QR_KILIT_KARTI__kart/kilit_karti_elemanlari → ucu bağlı olması gereken cihaz yüzüne / kanal parmak yuvasına uzat ya da cihaz taşındıysa yolu yeniden çek
- #6 `sureklilik/bosta_uc` qrk_kart_ucu_3 @ [5280.0, 1676.0, 1060.0] — serbest uç boşta (uç yönü [0.0, 0.0, 1.0]): uç yüzünün önünde r+4 mm içinde cihaz / kanal / rakor yok · en yakın 11 mm: QR_KILIT_KARTI__kart/kilit_karti_elemanlari → ucu bağlı olması gereken cihaz yüzüne / kanal parmak yuvasına uzat ya da cihaz taşındıysa yolu yeniden çek
- #11 `gecis/rakor_tikali` qrk_goz_demeti_rakor_ucu @ [4821.2, 1698.8, 799.6] — kablo rakor / kovan gövdesini kesiyor (rakor ekseni kabloyla çakışmıyor): ELK_QR_KUTU__rakor/qr_kutu_rakoru_goz_demeti → rakoru kablo eksenine ortala (ya da kabloyu rakor eksenine kaydır)
- #12 `gecis/deliksiz` qrk_ana_hat_guc_ROBOT_3G2_5 @ [4983.0, 307.1, 1045.0] — kablo ELK_QR_KABLO__kanal/#1 içinden deliksiz + rakorsuz geçiyor (2 vuruş) → yolu bu parçanın etrafından dik açılı çek ya da geçiş noktasında IP68 rakor + delik ekle
- #19 `gecis/deliksiz` qrk_kart_ucu_0 @ [5160.0, 1676.0, 1033.5] — kablo ELK_QR_KABLO__kanal/#0 içinden deliksiz + rakorsuz geçiyor (3 vuruş) → yolu bu parçanın etrafından dik açılı çek ya da geçiş noktasında IP68 rakor + delik ekle
- #20 `gecis/deliksiz` qrk_kart_ucu_1 @ [5200.0, 1676.0, 1033.5] — kablo ELK_QR_KABLO__kanal/#0 içinden deliksiz + rakorsuz geçiyor (3 vuruş) → yolu bu parçanın etrafından dik açılı çek ya da geçiş noktasında IP68 rakor + delik ekle
- #21 `gecis/deliksiz` qrk_kart_ucu_2 @ [5240.0, 1676.0, 1033.5] — kablo ELK_QR_KABLO__kanal/#0 içinden deliksiz + rakorsuz geçiyor (3 vuruş) → yolu bu parçanın etrafından dik açılı çek ya da geçiş noktasında IP68 rakor + delik ekle
- #22 `gecis/deliksiz` qrk_kart_ucu_3 @ [5280.0, 1676.0, 1033.5] — kablo ELK_QR_KABLO__kanal/#0 içinden deliksiz + rakorsuz geçiyor (3 vuruş) → yolu bu parçanın etrafından dik açılı çek ya da geçiş noktasında IP68 rakor + delik ekle
- #24 `gecis/deliksiz` qrk_ana_hat_veri_ROBOT_Cat6A @ [4983.0, 293.0, 1045.0] — kablo ELK_QR_KABLO__kanal/#1 içinden deliksiz + rakorsuz geçiyor (2 vuruş) → yolu bu parçanın etrafından dik açılı çek ya da geçiş noktasında IP68 rakor + delik ekle
- `gecis/kablo_kablo` × 9 — ör. qrk_ana_hat_guc_ROBOT_3G2_5 @ [4994.9, 109.3, 1036.0]: kablo eksenini başka kablo / hortum kesiyor: qrk_ana_hat_veri_ROBOT_Cat6A
- #140 `tutucu/havada_kelepce` ELK_QR_KABLO__celik/qrk_ana_hat_guc_QR_3G2_5_kelepce_0 @ [4956.0, 1960.0, 783.0] — kelepçe kabloyu tutuyor ama hiçbir sac / gövdeye değmiyor (0,8 mm içinde yüzey yok) · kablo ELK_QR_KABLO__kablo#9 → kelepçe dilini en yakın sac yüzüne uzat (M4 vida / perçin somunu) ya da kabloyu yüzeye yasla
- #141 `tutucu/havada_kelepce` ELK_QR_KABLO__celik/qrk_ana_hat_veri_QR_Cat6A_kelepce_0 @ [4955.2, 1960.0, 797.0] — kelepçe kabloyu tutuyor ama hiçbir sac / gövdeye değmiyor (0,8 mm içinde yüzey yok) · kablo qrk_ana_hat_veri_QR_Cat6A → kelepçe dilini en yakın sac yüzüne uzat (M4 vida / perçin somunu) ya da kabloyu yüzeye yasla
- #151 `gecis/bos_rakor` ELK_QR_KUTU__rakor/#1 @ [4880.0, 1937.9, 790.0] — rakor / geçiş elemanından kablo/hortum geçmiyor (en yakın eksen 85 mm: ELK_QR_KABLO__kablo#9) → kabloyu rakor ekseninden geçir ya da rakor + deliği kaldır (kablo taşındıysa yeni geçiş noktasına al)
- #152 `gecis/bos_rakor` ELK_QR_KUTU__rakor/harting_QR_rakoru_M32 @ [4880.0, 1996.0, 790.3] — rakor / geçiş elemanından kablo/hortum geçmiyor (en yakın eksen 30 mm: qrk_ana_hat_veri_QR_Cat6A) → kabloyu rakor ekseninden geçir ya da rakor + deliği kaldır (kablo taşındıysa yeni geçiş noktasına al)
- #153 `gecis/bos_rakor` ELK_QR_KABLO__rakor/#0 @ [4880.0, 300.0, 960.8] — rakor / geçiş elemanından kablo/hortum geçmiyor (en yakın eksen 68 mm: qrk_ana_hat_veri_ROBOT_Cat6A) → kabloyu rakor ekseninden geçir ya da rakor + deliği kaldır (kablo taşındıysa yeni geçiş noktasına al)
- #423 `hareket/kapak` ELK_QR_KABLO__kablo#9 @ [5385.9, 59.0, 640.0] — kapak ELK_QR_MONTAJ__on_seffaf#0 açılma süpürmesinin içinde (kapak [4572.5, 21.0, 670.0]–[5427.5, 446.0, 671.5], açılma yönü -z, kanat 425 mm · menteşe yeri modelde yok:  → kabloyu kapak kanadının süpürme hacminden çıkar (kapak düzleminin iç tarafına, ≥ 20 mm geri) ya da menteşe tarafına al
- #424 `hareket/kapak` qrk_guc_ROBOT_3G2_5_giris_b_ucu @ [5401.9, 59.0, 640.0] — kapak ELK_QR_MONTAJ__on_seffaf#0 açılma süpürmesinin içinde (kapak [4572.5, 21.0, 670.0]–[5427.5, 446.0, 671.5], açılma yönü -z, kanat 425 mm · menteşe yeri modelde yok:  → kabloyu kapak kanadının süpürme hacminden çıkar (kapak düzleminin iç tarafına, ≥ 20 mm geri) ya da menteşe tarafına al
- #425 `hareket/kapak` qrk_veri_MODEM_Cat6A_giris_b_ucu @ [5353.9, 41.0, 640.0] — kapak ELK_QR_MONTAJ__on_seffaf#0 açılma süpürmesinin içinde (kapak [4572.5, 21.0, 670.0]–[5427.5, 446.0, 671.5], açılma yönü -z, kanat 425 mm · menteşe yeri modelde yok:  → kabloyu kapak kanadının süpürme hacminden çıkar (kapak düzleminin iç tarafına, ≥ 20 mm geri) ya da menteşe tarafına al
- #426 `hareket/kapak` qrk_veri_QR_Cat6A_giris_b_ucu @ [5353.9, 59.0, 640.0] — kapak ELK_QR_MONTAJ__on_seffaf#0 açılma süpürmesinin içinde (kapak [4572.5, 21.0, 670.0]–[5427.5, 446.0, 671.5], açılma yönü -z, kanat 425 mm · menteşe yeri modelde yok:  → kabloyu kapak kanadının süpürme hacminden çıkar (kapak düzleminin iç tarafına, ≥ 20 mm geri) ya da menteşe tarafına al
- #427 `hareket/kapak` qrk_veri_ROBOT_Cat6A_giris_b_ucu @ [5369.9, 59.0, 640.0] — kapak ELK_QR_MONTAJ__on_seffaf#0 açılma süpürmesinin içinde (kapak [4572.5, 21.0, 670.0]–[5427.5, 446.0, 671.5], açılma yönü -z, kanat 425 mm · menteşe yeri modelde yok:  → kabloyu kapak kanadının süpürme hacminden çıkar (kapak düzleminin iç tarafına, ≥ 20 mm geri) ya da menteşe tarafına al
- #437 `sureklilik/kopuk_uc` goz_00…51_isitici_kablosu (12 göz) @ [4982.0, 452.5, 1000.0] — 12 göz ısıtıcı kablosunun her biri yalnız 3–4 mm'lik bir uç (x 4980–4984 / 5006–5010 · y 451, 651 … 1451 · z 999–1001); kanala / panoya giden kablo yok. → her ısıtıcı ucunu kendi göz sensör kablosunun yolundan kanal#2'ye (x 4994, z 930) bağla: (x, y, 1000) → z 930 → x 4994 parmak yuvası

**ANA_HAT** (127)
- `gecis/kablo_kablo` × 85 — ör. ana_hat_A_guc @ [2001.2, 2151.3, -817.3]: kablo eksenini başka kablo / hortum kesiyor: ana_hat_A_veri
- #28 `gecis/deliksiz` ana_hat_A_guc @ [1432.5, 2151.2, -817.2] — kablo A_GOVDE__paslanmaz/#0 içinden deliksiz + rakorsuz geçiyor (4 vuruş) → yolu bu parçanın etrafından dik açılı çek ya da geçiş noktasında IP68 rakor + delik ekle
- #53 `gecis/deliksiz` ana_hat_bina @ [2442.1, 1265.5, -790.0] — kablo ELK_TOPPING__kanal/kanal_TOPPING_KD1_dikey içinden deliksiz + rakorsuz geçiyor (2 vuruş) → yolu bu parçanın etrafından dik açılı çek ya da geçiş noktasında IP68 rakor + delik ekle
- #54 `gecis/deliksiz` ana_hat_bina @ [2442.1, 1265.5, -788.5] — kablo ELK_TOPPING__kanal/#2 içinden deliksiz + rakorsuz geçiyor (2 vuruş) → yolu bu parçanın etrafından dik açılı çek ya da geçiş noktasında IP68 rakor + delik ekle
- #99 `gecis/deliksiz` ana_hat_A_veri @ [1432.5, 2149.4, -805.6] — kablo A_GOVDE__paslanmaz/#0 içinden deliksiz + rakorsuz geçiyor (4 vuruş) → yolu bu parçanın etrafından dik açılı çek ya da geçiş noktasında IP68 rakor + delik ekle
- `gecis/gomulu` × 22 — ör. ana_hat_A_guc @ [2002.9, 2109.3, -698.7]: kablo ELK_ANA_HAT__kanal/#0'e gömülü / sürtünüyor (~15 mm boyunca eksenden 0.7 mm'de katı yüzey, r 6.2)
- `gecis/bos_rakor` × 11 — ör. ELK_ANA_HAT__rakor/#0 @ [2010.8, 2040.0, -796.0]: rakor / geçiş elemanından kablo/hortum geçmiyor (en yakın eksen 74 mm: ana_hat_TOPPING_veri)
- #428 `hareket/kapak` ana_hat_bina @ [5361.4, 11.9, 241.6] — kapak ELK_QR_MONTAJ__on_seffaf#0 açılma süpürmesinin içinde (kapak [4572.5, 21.0, 670.0]–[5427.5, 446.0, 671.5], açılma yönü -z, kanat 425 mm · menteşe yeri modelde yok:  → kabloyu kapak kanadının süpürme hacminden çıkar (kapak düzleminin iç tarafına, ≥ 20 mm geri) ya da menteşe tarafına al
- #429 `hareket/kapak` ana_hat_QR_guc @ [5378.6, 19.2, 615.0] — kapak ELK_QR_MONTAJ__on_seffaf#0 açılma süpürmesinin içinde (kapak [4572.5, 21.0, 670.0]–[5427.5, 446.0, 671.5], açılma yönü -z, kanat 425 mm · menteşe yeri modelde yok:  → kabloyu kapak kanadının süpürme hacminden çıkar (kapak düzleminin iç tarafına, ≥ 20 mm geri) ya da menteşe tarafına al
- #430 `hareket/kapak` ana_hat_ROBOT_guc @ [5357.8, 29.2, 241.7] — kapak ELK_QR_MONTAJ__on_seffaf#0 açılma süpürmesinin içinde (kapak [4572.5, 21.0, 670.0]–[5427.5, 446.0, 671.5], açılma yönü -z, kanat 425 mm · menteşe yeri modelde yok:  → kabloyu kapak kanadının süpürme hacminden çıkar (kapak düzleminin iç tarafına, ≥ 20 mm geri) ya da menteşe tarafına al
- #431 `hareket/kapak` ana_hat_modem @ [5369.4, 27.3, 248.4] — kapak ELK_QR_MONTAJ__on_seffaf#0 açılma süpürmesinin içinde (kapak [4572.5, 21.0, 670.0]–[5427.5, 446.0, 671.5], açılma yönü -z, kanat 425 mm · menteşe yeri modelde yok:  → kabloyu kapak kanadının süpürme hacminden çıkar (kapak düzleminin iç tarafına, ≥ 20 mm geri) ya da menteşe tarafına al
- #432 `hareket/kapak` ana_hat_QR_veri @ [5390.3, 18.9, 615.0] — kapak ELK_QR_MONTAJ__on_seffaf#0 açılma süpürmesinin içinde (kapak [4572.5, 21.0, 670.0]–[5427.5, 446.0, 671.5], açılma yönü -z, kanat 425 mm · menteşe yeri modelde yok:  → kabloyu kapak kanadının süpürme hacminden çıkar (kapak düzleminin iç tarafına, ≥ 20 mm geri) ya da menteşe tarafına al

**ROBOT** (3)
- #139 `gecis/gomulu` robot_kablosu_kangal @ [5327.8, 57.9, 837.5] — kablo QR_GOVDE__qr_govde/#0'e gömülü / sürtünüyor (~20 mm boyunca eksenden 33.0 mm'de katı yüzey, r 69.3) → kabloyu yüzeyden r + 0,5 mm uzaklaştır (yüzeye dayalı, içine girmeyen)
- #433 `hareket/kapak` robot_kablosu_uzatma_A @ [4570.4, 12.0, 530.1] — kapak ELK_QR_MONTAJ__on_seffaf#0 açılma süpürmesinin içinde (kapak [4572.5, 21.0, 670.0]–[5427.5, 446.0, 671.5], açılma yönü -z, kanat 425 mm · menteşe yeri modelde yok:  → kabloyu kapak kanadının süpürme hacminden çıkar (kapak düzleminin iç tarafına, ≥ 20 mm geri) ya da menteşe tarafına al
- #434 `hareket/kapak` robot_kablosu_uzatma_A @ [5088.1, 50.0, 630.0] — kapak ELK_QR_MONTAJ__on_seffaf#0 açılma süpürmesinin içinde (kapak [4572.5, 21.0, 670.0]–[5427.5, 446.0, 671.5], açılma yönü -z, kanat 425 mm · menteşe yeri modelde yok:  → kabloyu kapak kanadının süpürme hacminden çıkar (kapak düzleminin iç tarafına, ≥ 20 mm geri) ya da menteşe tarafına al

## ELENEN YANLIŞ POZİTİFLER

- hava borusu ucu kendi cihazının (valf adası / şartlandırıcı) rakoruna giriyor: 2
- gömülü: < 10 mm (kanala / cihaza giriş köşesi): 24
- gömülü: motorun kendi kablo ucuyla birleşim (bağlantı, hata değil): 4
- boş rakor adayı: rakor olmayan küçük plastik parça (yatak, tapa, gider): 68

## YÖNTEM

- Model: hat3_v8x.glb (gece madde 1–7 sonrası), SALT OKUMA. Kablo / hortum / boru = düğüm malzemesi kablo · kablo_veri · hava_ana · hava · bakir · hortum_gida · hortum_yag · hortum_orgu (325 bağlı bileşen, 12 üçgenli kutular hariç).
- Eksen çıkarımı: silindir / yuvarlatılmış kare yan şeritlerinden doğru parçalar (serit.py); bulunamazsa geodezik dilim. Bileşen adı parca_kutulari (pk_yeni, m7 kaydırmalı) en küçük kapsayan kutu.
- Süreklilik: serbest uç (başka segmente r1+r2+6 mm'den uzak) önünde r+4 mm içinde başka katı yoksa boşta. Geçiş: eksen doğru parçası × tüm üçgenler (rtree + Möller–Trumbore). Gömülü: eksenden 0,55 r içinde katı yüzey (5 mm adım).
- Tutucu: ELK / K_YAG / ROBOT / HAVA küçük çelik-plastik bileşenler (< 45 mm); halka kabloyu sarıyor mu (köşe–eksen mesafesi − r < 2 mm), 0,8 mm içinde gövde yüzeyi var mı.
- Hareket: animasyonlu düğümlerin öteleme yolu boyunca (5 mm adım) yüzey örnekleri ↔ kablo noktaları; kapaklar (kpk, ≤ 25 mm kalın) kısa kenar kadar dışa açılma kutusu; kaşar/sucuk kaseti +z 300, UNO hazneleri öne; TOPPING araba/kızak/motor zarfları (h3_elk_ist_v1) ve robot koridoru (z 79–669).

## SINIRLAR

- Menteşe yerleri modelde yok → kapak süpürmesi kutu yaklaşımı (kanat = kısa kenar); kesin değil.
- Robot erişimi ayrıntılı değil (koridor kutusu); robot / enerji zinciri Kemal kuralı gereği Isaac'ta.
- Döner animasyonlu E kutu düğümleri (E_KUTU, E_KOSE) süpürmeye alınmadı (yakınında kablo yok).
- Kablo içi kanalda çizilmeyen yollar (kapaklı kanal) denetlenmedi; kanal doluluk oranı hesaplanmadı.
- Ad eşleme v7 kutularıyla: m3 / m7c ile yeniden çekilen kabloların bazıları adsız (ELK_TOPPING__kablo#9534 = tabla boş sensörü, #9632 = x sağ limit).

Betikler: `gece/m8/kablo_is/` (kablo_cikar.py → kablo_denetim.py → hareket.py → birlestir.py; ortam.py, serit.py).