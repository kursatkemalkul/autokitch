# TOPPING + F ÜRETİM SACI · ENTEGRASYON NOTU (adım 5c → 5-entegrasyon)

4 Eki 2026 gece · Claude · YEREL. Ana GLB'ye (hat3_v8) ve sayfaya DOKUNULMADI. Bağımsız üreteç + çıktı + denetim.

Üreteçler (worktree, göreli yol, deterministik): `arastirma/_uretec/h3/h3_topping_sac_v1.py`, `arastirma/_uretec/h3/h3_f_sac_v1.py`
Ortak kütüphane `h3_sac_v1.py` (değişmedi) · standart `AUTOKITCH_SAC_STANDART` → `<scratchpad>/sac_standart`.
Denetim (A/B ile aynı `sac_denetim_ortak.calistir`): `topping_sac_denetim_v1.py`, `f_sac_denetim_v1.py` (bu klasör) — TOPPING_MODUL düğümleri karışık olduğundan
v8zq'da yerine geçilen bileşenler **düğüm + bileşen no** ile çıkarılır (`M.DEGISEN`).
Çıktılar: `TOPPING_sac_v1.glb`, `F_sac_v1.glb`, `TOPPING_parca.csv`, `F_parca.csv`, `TOPPING_rapor.json`, `F_rapor.json`, `acinim_TOPPING/`, `acinim_F/`,
`TOPPING_birlesik/patlatilmis/kapaksiz_ic.jpg`, `F_*.jpg`. Yardımcı tarama: `gece2/adim5c/` (dilim.py: v8zq sac orta düzlem kesiti → delikler · temas.py: duvara değen parçalar).

---------------------------------------------------------------------------------------------------------------------------------

## TOPPING (C) — h3_topping_sac_v1

### Yerine geçen v8zq bileşenleri (`DEGISEN`)
| düğüm | bileşen | ne |
|---|---|---|
| `TOPPING_MODUL__sac` | 17–28, 30, 31–81, 98, 99 | dış yan sol/sağ, taban, arka, tavan, teknik ön/sağ perde, kuru taban, cep (5), ön perde menfez parçaları, eski 40×40 yamalar |
| `TOPPING_MODUL__paslanmaz` | 105–155 | astar, raf + bükümler + köşebentler, eşik, dil kanalları, üst raf, 6 taban kovanı, alt sac, ön çerçeve, soğuk arka dış sac, evaporatör pencere sandviçi, kapalı eski dolgu kovanları (150–155) |
| `TOPPING_MODUL__pu` | 0–7, 10, 11 | soğuk oda PU (8, 9 = evaporatör kaseti PU'su → KALIR) |
| `KAIDE_C__paslanmaz` | hepsi | kaide (arka emiş filtresi aynı ölçüde yeniden: `kaide_arka_emis_filtresi`) |

KALIR: kanatlar K1/K2 (`TOPPING_MODUL__on_seffaf`, çift cidar + PU + fitil), menteşe gövdeleri (paslanmaz 84–89), bas-aç gövdeleri (90–93), POM burçlar (pom 2,5–11, 13–32),
evaporatör kasetleri, pano / DIN / sürücüler, UNO / kaset / tabla / ray / açıcı, bütün ELK / HAVA.

### Yeni düğüm önerisi
`TOPPING_GOVDE__kabuk` ← `dis_*` · `TOPPING_GOVDE__sac` ← diğer saclar + profiller + kaynak/dolgu · `TOPPING_GOVDE__cerceve` ← `on_cerceve_430` ·
`TOPPING_GOVDE__pu` ← `pu_*` (görünmez) · `TOPPING_GOVDE__paslanmaz` ← PEM / vida / pul · `TOPPING_GOVDE__conta` ← köpük kapakları, silikon dolgular ·
`TOPPING_GOVDE__pom` ← kaşar/sucuk POM kovanı. `mek` = TOPPING/Gövde · `kat` = GOVDE (kaide parçaları kat 1). `kpk` yok.

### Kurgu (kısa)
* Dış kabuk 304 1,5 kaynaklı + PU sandviç. Yanlar y 892–2200 (tavan aralarına oturur). Tavanın yan dönüşü yalnız kuru bölmede (soğuk oda arka sacı ve çerçeveyle kesişmesin), arada rahatlatma.
* **Arka = sökülür servis sacı** (Kemal 2 Eki): 17 × ISO 7380 M5 → yan / tavan / taban dönüşlerinde PEM SP-M5. Pano kutusu, DIN plakası, emiş filtresi, KD3 braketleri, evaporatör ayakları bu sacta FHP-M5 (sacla birlikte sökülür).
* Soğuk oda: çerçeve 430 1,0 · alt sac / arka dış sac 1,5 · astar 1,0 (4 düz sac, TIG + R3) · raf 3,0 / üst raf 3,0 (iki büküm + köşebent) · eşik 1,2 · dil kanalı U 1,0 (raf + eşik tek parça) · 6 düşme kovanı · 4 evaporatör kanal kovanı (iki L).
  Evaporatör pencereleri: v8zq'da astar ve arka dış sacta pencere AÇIK DEĞİLDİ (tapa saclar üst üste binmiş, hava yolu kapalıydı) → arka dış sacta kanal ağzı, astarda lazer yarık alanı, arada kovan.
* Kaide: 40×100×2 borular + enine lama 6 + **ön perde menfezli 2,0 C** (kanat menfezleri hizasında) + 4 mm plaka + cep taşıyıcı L × 2.

### Kalan parçaların bağlantısı (ARAYÜZ — karşı tarafta delik gerekir)
| karşı parça | bağlantı | gövdede hazır | karşıda gereken |
|---|---|---|---|
| A sağ yan (h3_a_sac_v1) | 4 × M8 A içinden | sol yanda PEM SP-M8 (y 1300/2000 · z −300 köpük kapaklı / −700) | A'da Ø9 hazır |
| F sol yan (h3_u_sac_v1 `f_ust_yan_sol`) | 4 × ISO 4762 M8 × 16, F içinden | sağ yanda PEM SP-M8 (y 1000 z −760 · 1250/−700 · 1700/−780 · 1950/−780) | **F sol yan sacında 4 × Ø9** (1950/−780 noktası U_F sol sacına düşer) — U sahibine |
| J1 TOPPING paneli | 4 × FHP-M5 × 25 | sağ yanda (burç eksenleri) + ağız 57 × 67 | — (E/U ile aynı) |
| B dış tavan + B_MODULER üst kiriş | KAIDE → B 4 × M8 (x 1456/−706 · 1456/−110 · 2120/−110 · 2480/−110) | kaide borusu alt Ø9, üst + plaka Ø16 | **B tavanında Ø9 + kirişte M8 kapalı perçin somun** — B sahibine (h3_b_sac_v1'de yok) |
| Tabla rayı tabanı (`TOPPING_MODUL__sac[8]`) | 4 × M6 → kaide plakası PEM SP-M6 | gövde tabanında Ø6,6 | ray tabanında Ø6,6 (x 1750/2250 · z −320/−20) |
| Gövde ↔ kaide | 2 × M6 (x 1545 / 2300 · z −458) | taban Ø6,6 + plaka PEM | — |
| Mekanizma / elektrik / hava parçaları | 46 × FHP-M5 | duvar / raf / tavan / arka / kuru taban | karşı parçada Ø5,5 (liste `TOPPING_rapor.json → arayuz`) |
| Soğutma grubu titreşim takozları | M8 saplama | cep tabanında 4 × PEM SP-M8 | — |

Atlanan saplamalar (kenara < 12 mm, rapor `notlar`): menteşe gövdeleri (z 26–39, ön kenara 6,5 mm) → menteşe kendi vidalarıyla; sağ perde alüminyum braketi (perde üstü).

### Bugünkü modelden farklar (üretim zorunluluğu)
* Sol yan tabla ağzı alta açık (taban 892'de başlıyor, eski ağız alt kenara 1,5 mm idi).
* J1 ağzı 56 × 66 → 57 × 67 (r 1); ana hat geçişinin arka kenarı −827 → −820 (U ile eş).
* Eski Ø16,4 / Ø13,9 delikler + 40 × 40 yamalar ÜRETİLMEZ.
* POM burç delikleri burcun gerçek kesitine (v8zq'da delik 0,39 mm dardı); raf askı burçları gerçek kesit.
* Ön çerçevenin alt köşelerindeki 2,5 mm şerit (menteşe ile tabla açıklığı arası) kalktı.
* Dil kanalı 65 → 69 dış (iç 67: kaset dili büküm yayına girmesin) · raf kesiği aynı genişlik.
* Kaşar/sucuk düşme kovanı POM-C CNC (artı kesitteki 6 mm basamaklar abkantla bükülemez) · üst yakası kaset dili yuvalı.
* Kıyma/kuşbaşı kovanı 3,0 (dış 44: raf deliği Ø43 tamamen kovan üstüne gelir), sos/harç boru Ø38 × 3,5.
* Teknik sağ perde arka kenarı −826,9 → −824 (taban dönüşü büküm yayı).
* Raf / eşik büküm dış yaylarının yivleri TIG dolgu + taşlama (gıda yüzeyi düz) — katı olarak modellendi.

### Açık
* **Zarf:** gövde sacları fark 0; yalnız servis sacının bombe başlı vida başları arka yüzden 2,6 mm dışarıda (Kemal izni). Sıfır istenirse: çökertme havşa + DIN 7991 (dönüşte PEM yerine perçin somun) — karar Kemal'de.
* Evaporatör ayakları arka servis sacına bağlı (v8zq iç yerleşimi) → sac sökülürken bakır hat bağlantısı ayrılmalı; ayakların yan sac / kuru tabana taşınması önerilir (iç yerleşim, onay gerekir).
* Kanatlar (K1/K2) bu adımda üretim sacına çevrilmedi (v8zq kanadı çift cidar + PU, ölçüleri uyumlu).
* PEM / menteşe ölçüleri bülten yaklaşık değerleri; K = 0,45 atölye numunesiyle kalibre edilecek.

---------------------------------------------------------------------------------------------------------------------------------

## F — h3_f_sac_v1 (U'nun yapmadığı F parçaları)

Kapsam notu (koordinatör, 5b): F üst kabinin yan / arka / tavan / taban / profilleri (y 788–1862, fırın bölgesi dahil) **h3_u_sac_v1**'de. y < 788 B'dir (F, B tavanına oturur → **F kaidesi yok**).
TP10 fırın gövdesi satın alınan cihaz (kendi kabuğu `F_TP10_GOVDE`, dokunulmadı) · yükleme bandı TP10 girişinin içinde (mekanizma) · F kutusu `ELK_ISTASYON__pano` (elektrik üreteci) ·
kompresör ayakları U üst kabin tabanında (PEM hazır). Bu yüzden F üreteci: **ön kapaklar + davlumbaz atış kanalı + baca + arayüzler**.

| v8zq | yerine | not |
|---|---|---|
| `F_UST_KAPAK__on_seffaf__KAPAK_F_SOL/SAG` [0,1,2,3,5,8] | `onyuz_kapak_F_{sol,sag}_dis_tava` (1,5, bindirme köşe, 36 panjur yarığı 90 × 5) · `_omega_{0,1}` (hazır haddeli 40 × 15 × 1,5) · `_alt_kayit` / `_ust_kayit` (U 1,5) · `_basac_karsilik` · menteşe PEM SP-M5 | kpk = KAPAK_F_SOL / KAPAK_F_SAG aynı pivot · KALIR: menteşe gövde + kanat (celik 0–3, on_seffaf 6/7), gazlı yay + bilyeli braket (4) |
| `F_DAVLUMBAZ__sac` [1] | `davlumbaz_atis_kanali_L1/L2` (296 × 196 · 1,5 · iki L) | üst ucu 1862 → 1892: baca iç kanalına 30 mm teleskopik geçme + yüksek sıcaklık silikonu |
| `U_F_BACA__sac` + `__yalitim_gorunur` + `__paslanmaz` | `baca_ic_kanal_L1/L2` 1,5 · `baca_dis_kilif_L1/L2` 0,8 · `baca_alt_kapama_lamasi_*` (4) + köşe silikonu · `yalitim_baca_0` (taş yünü A1, görünmez) · `baca_ust_flansi_*` (4 lama 3 mm) + 8 PEM SP-M6 kör başlıklı | eski "yalıtım görünür" düzeltildi |

ARAYÜZ (F): F sol yanında 4 × Ø9 (TOPPING ↔ F, U sahibi) · U_F tavanında 8 × Ø6,6 (baca flanşı, U sahibi) · menteşe kanadında 2 × Ø5,5 / menteşe.
5b'nin F sağ yan sacına eklediği K delikleri (tartı rakoru + 2 yağ hortumu) bu üreteçte yok, çakışma yok.

---------------------------------------------------------------------------------------------------------------------------------

## DENETİM SONUCU (bağımsız · sac_denetim_ortak · v8zq'ya karşı)

| madde | TOPPING | F |
|---|---|---|
| parça | 170 gövde parçası (43 sac · 7 boru · 67 bağlantı / dolgu · 51 kaynak · 2 PU) + 72 arayüz | 69 gövde parçası (22 sac · 32 bağlantı · 14 kaynak · 1 taş yünü) + 20 arayüz |
| sac kütlesi (açınım) | 175.6 kg | 33.5 kg |
| açınım doğrulaması | 43 / 43 GEÇTİ | 22 / 22 GEÇTİ |
| DFM (abkant sırası dahil) | 0 HATA · 0 UYARI | 0 HATA · 0 UYARI |
| en büyük levha | dis_arka_servis 1308 × 1061 | onyuz_kapak_F_sol_dis_tava 923 × 783 |
| dış zarf | gövde sacları fark 0,0 · servis sacı bombe başlı vida başları −2,6 (Kemal izni, açık madde) | fark 0,0 |
| gövde ↔ gövde | 0 | 0 |
| gövde ↔ v8zq (cift: manifold + örnekleme + derinlik) | ÇAKIŞMA 0 · İNCELE 0 | ÇAKIŞMA 0 · İNCELE 0 |
| havada | 0 | 0 |
| PU / taş yünü görünmez (10 mm aralık, 0,4 dışarı) | açıkta 0 | açıkta 0 |

