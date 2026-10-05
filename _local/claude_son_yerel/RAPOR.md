# KUYRUK 3 · İŞ 1 · STANDART UYUM — RAPOR (4 Eki 2026 gece · Claude · YEREL)

Kapsam: A, B, TOPPING, F (üst kabin / kapak / baca), K, E, U_F, U_KE gövdeleri (QR / tezgâh hariç).
Kaynak: 7 üretecin kendisi kuruldu ve döküldü (`envanter.py` / `envanter2.py` → `env_*.json`, `env2_*.json`: her sac t / R / büküm R'leri / bölge,
her profil, her bağlantı elemanı + arayüz elemanı dünya konumu) + ana model GLB'si ölçüldü (`on_yuz.py`, `zarf.py`, `pul_bul.py`).
Model zinciri: v9v (adım 54) → **v9w (adım 55, bu iş)**.

---

## 1 · ÖZET

| Kalem | Bulunan uyumsuzluk | Düzeltilen (adım 55) | Korunan (işlevli / Kemal onaylı) | Açık öneri (sonraki üreteç sürümü) |
|---|---|---|---|---|
| (a) sac kalınlığı | 6 | — | 3 | 3 |
| (b) büküm iç R | 0 | — | — | — |
| (c) köşe R | 0 | — | — | — |
| (d) bağlantı elemanı | 5 | **2 (123 pul)** | 1 | 2 |
| (e) komşu arayüz | 1 (alt sıra çekmece derzleri üst istasyon derzleriyle hizasız) | — | 1 | — |
| (f) aynı tip katalog parça | 1 | — | 1 | — |

**Düzeltildi (adım 55, 123 pul):** M5 pul DIN 9021 → ISO 7089 (95 adet: A 35, K 32, E 28; somun 0,2 mm sac tarafına) ·
M8 pul DIN 9021 / DIN 125 → ISO 7092 (28 adet: A→TOPPING 4, TOPPING→F 4, B şase 10, A açıcı flanşı 4, U_F 6; DIN 9021'lerde cıvata 0,4 mm sac tarafına).
Standart tek kaynak: `yama_v9/sac_standart/sac_uyum_v1.json` (yeni dosya; `sac_standart_v1.json` / `sac_kararlar_v1.json` değişmedi → montaj v7 ve zincir 33–38 bayt aynılığı korunur).

---

## 2 · (a) SAC KALINLIKLARI

Kullanılan değerler (üreteçlerden, adet = sac parçası):

| t (mm) | A | B | TOPPING | F | K | E | U_F | U_KE | F_UST | Aile? |
|---|---|---|---|---|---|---|---|---|---|---|
| 0,5 | | | | | | | | | 2 (yalıtım kılıfı) | **HAYIR** |
| 0,8 | | 1 (ışınım sacı) | | 6 (baca kılıfı + lamalar) | | | | | | evet |
| 1,0 | 1 (kapak iç) | 3 (ön çerçeve) | 15 (soğuk iç sac, ön çerçeve, kanal kovanı, dil kanalı) | 2 (bas-aç karşılığı) | 1 (kapak iç) | 8 (kapak iç + robot ağzı kasası) | | | | evet |
| 1,2 | | 33 (gıda iç sac R3, kovan, kalkan) | 1 (soğuk eşik) | | | | | | | evet |
| 1,5 | 9 (kabuk, kapak dış) | 26 (kabuk) | 13 (kabuk) | 12 (kapak dış + iç, kanal) | 8 | 17 | 6 | 5 | 6 | evet |
| 2,0 | 4 (dikme tapası) | | 1 (kaide ön perdesi) | | 4 (tapa) | 22 (tapa + ön dikme kulağı) | | | 1 (tapa) | evet |
| 2,5 | | | 4 (evaporatör L ayağı) | | | | | | | **HAYIR** |
| 3,0 | 22 (kulak) | | 16 (raf, köşebent, düşme kovanı, kulak) | 4 | 28 (kulak, raf) | 17 (braket) | | | 1 | evet |
| 4,0 | 1 (kaide plakası) | | 1 (kaide plakası) | | | | | | | plaka (izinli) |
| 6,0 | | | 1 (kaide laması) | | | | | | | plaka (izinli) |

Aynı işlev — istasyonlar arası:

| İşlev | Değer | Sonuç |
|---|---|---|
| Dış kabuk | 1,5 her istasyonda | ✔ |
| Kapak dış tava | 1,5 (A K E F TOPPING) | ✔ |
| Kapak iç tava | 1,0 (A K E) · **1,5 (F)** | ✘ — F üretecinde gerekçe yazılı değil → **öneri: F v2'de 1,0** (dış ölçü değişmez) |
| Gıda (soğuk) iç sac | **B 1,2 · TOPPING 1,0** (ikisi de R 3) | ✘ — TOPPING 1,0 Kemal onaylı (topping_sac_v2 D2, 4 Eki) → KORUNDU; öneri: yeni TOPPING sürümünde 1,2 |
| Ön çerçeve | 1,0 (B, TOPPING) | ✔ |
| Raf / yük sacı | 3,0 (TOPPING raf + üst raf, K istasyon rafı) | ✔ (kararlar dosyası 1,5 der; iki istasyon da 3,0 → tablo 3,0'a çekildi) |
| Kulak (panel → iskelet) | 3,0 (A K TOPPING F_UST) · **2,0 E ön dikme** | KORUNDU — E üreteci bilerek seçmiş: dar ön dikme (20 mm) |
| Dikme tapası | 2,0 her yerde | ✔ |
| Aile dışı 0,5 (F_UST yalıtım kılıfı) | | ✘ → öneri U v2'de 0,8 (taş yünü 0,3 incelir) |
| Aile dışı 2,5 (TOPPING evaporatör ayağı) | | KORUNDU — Kemal onaylı (topping_sac_v2 D3); öneri 3,0 |

Neden bu adımda kalınlık değiştirilmedi: kalınlık değişikliği üreteç → zincir 34/36/37'den itibaren yeniden koşu ister; 39–53 adımları B / TOPPING / F_UST
bileşenlerini kutu ölçüsüyle buluyor (0,3 mm tolerans) → kırılma riski yüksek, kazanç görsel değil. Üç öneri yeni üreteç sürümüne (v2) bırakıldı.

## 3 · (b) BÜKÜM İÇ YARIÇAPI — uyumsuzluk 0

Bütün istasyonlarda `R_iç = 1,5 t` (kararlar `ic_radyus_carpan`): 0,8 → 1,2 · 1,0 → 1,5 · 1,2 → 1,8 · 1,5 → 2,25 · 2,0 → 3,0 · 2,5 → 3,75 · 3,0 → 4,5.
Gıda tarafı iç saclar (B iç kabuk 1,2 · TOPPING astar 1,0 / eşik 1,2 / dil kanalı 1,0) **R 3** — EHEDG en az 3; iki soğuk istasyonda aynı kural. K 0,45 / 0,41 tablodan.

## 4 · (c) KÖŞE R — uyumsuzluk 0

Profil dış R = 2t her yerde (30×30×2 → R4; 40×100×2 → R4; E kaidesi 60×60×3 → R6). Gıda iç köşe R 3 büküm + 3×3 silikon (TOPPING), servis / geçiş
ağzı köşesi R6 (A tabla geçişi), hazne dikey köşesi R25 (TOPPING, 5 hazne aynı). Dış görünür köşeler TIG + taşlama (kapak tavaları). Not: her lazer kesiğin köşe R'si tek tek taranmadı (üreteç DFM'leri 0 HATA).

## 5 · (d) BAĞLANTI ELEMANLARI

Kullanılan set (üreteçler + model):

| Eleman | Ölçüler | İstasyon |
|---|---|---|
| PEM FHP saplama (A286) | M5 × 10 / 12 / 15 / 25 (yığına göre) · M6 × 15 (E) | A E K TOPPING U F_UST |
| PEM SP somun (A286) | M5-1 / M5-2 · M6-2 · M8-1 / M8-2 (kod = sac kalınlığı: 1,0–1,3 → 1 · ≥ 1,4 → 2) | A B E F K TOPPING F_UST |
| ISO 10511 fiberli somun | M5 · M8 | A E K U F_UST |
| ISO 4762 silindir baş | M5 × 16 · M6 × 12 / 16 · M8 × 10 / 16 / 20 / 25 / 50 | hepsi |
| ISO 7380 bombe baş | M5 × 6 / 10 / 12 · **M8 × 16 (U_KE → E / K)** | A E F K TOPPING U |
| DIN 7991 havşa | M5 × 6 (B ray, kısaltılmış) / × 12 (TOPPING servis, dimple + kaynak burcu) | B TOPPING |
| Perçin somun M8 | açık uç (K iskelet) · kapalı uç (B, ıslak) | K B |
| Kör perçin | **DIN 7337 Ø4 (B iç kabuk, 213)** · **ISO 15983 Ø3,2 (TOPPING 28 + F_UST 16)** · ISO 15984 havşa Ø3,2 (TOPPING çerçeve 20) | B TOPPING F_UST |
| DIN 929 kaynak somunu | M8 · M12 (ayak) | E |

Uyumsuzluklar:

| # | Ne | Durum |
|---|---|---|
| D1 | M5 pul (FHP / vida + fiberli somun): A, K, E'nin 28'i DIN 9021 Ø15 × 1,2 · E'nin 42'si, U_F 35, U_KE 31, F_UST 36, B 42 DIN 125 Ø10 × 1,0 | **DÜZELTİLDİ** → ISO 7089 (DIN 125-A) M5. Gerekçe: pul 2–3 mm kulağa / profile basar (ince sac değil); E üreteci dar dikmede zaten DIN 125'e geçmiş. 95 pul, somun 0,2 mm sac tarafına |
| D2 | M8 modül cıvatası pulu: DIN 9021 Ø24 (A→TOPPING, TOPPING→F, B şase) · DIN 125 Ø16 (A açıcı, U_F, K) · ISO 7092 Ø15 (A→B, TOPPING→B — Ø16 servis deliği) | **DÜZELTİLDİ** → ISO 7092 M8 (silindir başın kendi pulu; her yerden geçer). 28 pul, DIN 9021'lerde cıvata 0,4 mm sac tarafına. K'nın 9 DIN 125 M8 pulu ve 6 DIN 9021 M5 pulu modelde ayrı halka bileşeni olarak bulunamadı (montaj v7'de komşu parçayla birleşik) → modelde değişmedi, tablo ISO 7092 / ISO 7089 der (K üreteci v2'de) |
| D3 | M8 modül cıvatası baş tipi: U_KE → E / K 5 adet ISO 7380 (bombe) · diğer bütün modül bağlantıları ISO 4762 | AÇIK — U v2'de ISO 4762'ye çekme önerisi (baş 4,4 → 8, U_KE taban üstünde yer kontrolü gerek) |
| D4 | Kör perçin çapı: B Ø4 (DIN 7337) ↔ TOPPING / F_UST Ø3,2 (ISO 15983) — aynı işlev (iç sac flanşı ↔ sac) | AÇIK — öneri tek çap Ø4 ISO 15983 A2/A2 (TOPPING v3 + U v2); 64 delik + POM pul yuvası değişir, zincir 36/37'den yeniden koşu |
| D5 | Perçin somun açık uç (K) / kapalı uç (B) | KORUNDU — işlevli (B ıslak / soğuk bölge) |

Vida boyu / diş: FHP boyları üreteçlerde yığına göre seçilmiş (sac_ent saplama boyu denetimi); adım 55'te M5 somunlar 0,2 sac tarafına kaydı → saplama çıkıntısı 0,2 arttı (diş kavrama aynı / fazla). M8 × 10 (A→TOPPING) ve M8 × 16 (TOPPING→F), M8 × 20 (B şase) cıvatalar 0,4 derin girdi → uç PEM / perçin somun içinde (çakışma denetimi aşağıda).

## 6 · (e) KOMŞU İSTASYON ARAYÜZÜ (model ölçümü, v9w)

| Ölçü | A | TOPPING | F | K | E | U_F / U_KE | B | Sonuç |
|---|---|---|---|---|---|---|---|---|
| Kapak ön yüzü z | 79 | 79 | 79 | 79 | 79 | — | 79 | ✔ |
| Gövde ön düzlemi z | 59 | 39 (soğuk) | 59 | 59 | 59 | 59 | 39 (soğuk) | ✔ (soğuk istasyonda kapak 40, nötrde 20 — işlevli) |
| Arka z | −830 | −830 | −830 | −830 | −830 | −830 | −830 | ✔ |
| Üst y | 2200 | 2200 | (U_F) 2200 | (U_KE) 2200 | (U_KE) 2200 | 2200 | 788 | ✔ |
| Alt y (B üstü) | 788 | 788 | 788 | 788 | 123 (kendi kaidesi) | 1862 (U altı = F_UST / K / E üstü 1862) | 123 | ✔ |
| Gövde x | 736–1436 | 1436–2500 | 2500–4000 | 4000–4400 | 4400–5230 | 2500–4000 / 4000–5230 | 736–4400 | ✔ modül derzi 0 |
| Kapak üst kotu | 2197 | 2197 | 2197 | 2197 | 2197 | | | ✔ |
| Alt sıra üstü / üst sıra altı | 785 / 788 | 785 / 788 | F fırın 788–1305, kapak 1308 | 785 / 788 | 785 / 788 | | | ✔ derz 3 |

Kapak derzleri (üst sıra, x): A 736–1434,5 │3│ TOPPING 1437,5–1965,75 │3│ 1968,75–2497 │3│ F 2500–3248,5 │3│ 3251,5–4000 │3│ K 4003–4399 │3│
E 4402–4860 │3│ 4863–5230 → **hepsi 3,0**. Alt sıra (B çekmeceleri + E alt): 736–1434,5 │3│ 1437,5–2089,5 │3│ 2092,5–2744,5 │3│ 2747,5–3399,5 │3│
3402,5–4000 │3│ 4003–4399 │3│ 4402–4860 │3│ 4863–5230 → **hepsi 3,0**; çekmece satır derzleri de 3,0 (126 → 290,5 │ 293,5 …).
İç tava payı: nötr kapaklar 2,0 (A K E), soğuk kapak / çekmece 1,5 (TOPPING, B) — kendi içinde aynı.

**Korunan fark:** alt sıra B çekmece sütun derzleri üst istasyon derzleriyle yalnız A|TOPPING, F|K, K|E'de hizalı; TOPPING ortası (1965,75), TOPPING|F (2497)
ve F ortası (3248,5) altında çekmece derzi yok (B çekmece genişlikleri 698,5 / 652 / 652 / 652 / 597,5 tepsi ölçüsünden). Hizalamak B'nin 21 çekmecesini
baştan bölmek demek → yapılmadı, Kemal'e not.

Delik eşleşmesi (cıvata ekseni ↔ karşı PEM / perçin somun / delik; üreteç verisi `arayuz_eslesme.json`):

| Arayüz | Adet | Eleman | Eksen kayması |
|---|---|---|---|
| A → TOPPING | 4 | ISO 4762 M8 × 10 + ISO 7092 → PEM SP-M8 (TOPPING sol dış sacı) | 0,000 |
| A açıcı kolonu | 4 | M8 × 20 + ISO 7092 → PEM SP-M8 (kaide plakası) | 0,000 |
| A → B | 6 | M8 × 16 + ISO 7092 → kapalı uçlu perçin somun (B üst kiriş) | 0 (karşı delik cıvata ekseninden delindi, adım 34 / 47) |
| TOPPING → F | 4 | M8 × 16 + ISO 7092 → F sol yan Ø9 | 0,000 |
| TOPPING → B | 4 | M8 × 25 + ISO 7092 → perçin somun | 0 (cıvata ekseninden) |
| K → F | 4 | M8 × 25 + DIN 125 → perçin somun M8 | 0,000 |
| K → E | 3 | M8 × 25 + DIN 125 → perçin somun M8 | 0,000 |
| K → B | 2 | M8 × 50 + DIN 125 | 0 (cıvata ekseninden) |
| B şase | 10 | M8 × 20 + ISO 7092 → kapalı uçlu perçin somun | 0 (cıvata ekseninden) |
| U_KE → E | 3 | ISO 7380 M8 × 16 → PEM SP-M8 (E üst sacı) | 0,000 |
| U_KE → K | 2 | ISO 7380 M8 × 16 → PEM SP-M8 (K üst sacı) | 0 (cıvata ekseninden) |

Bağlantı yeri seçimi her iki istasyonun üretecinde AYNI koordinat sabitinden (ör. `h3_a_sac_v1.M8_T` hem A cıvatasını hem TOPPING PEM'ini kurar) →
kayma tasarım gereği 0; modelde cıvata ↔ sac çakışması çakışma denetiminde (§8) aranır.

## 7 · (f) AYNI TİP KATALOG PARÇA

| Parça | Ürün | Sonuç |
|---|---|---|
| Ön kapak menteşesi | Southco R6 / EMKA 1046 sınıfı gizli 180° kaldır-çıkar (A 3, K 3, E 12) | ✔ · E şarjör yan kapısı Southco E6 (küçük kapı, farklı ürün — işlevli, korundu) |
| Bas-aç | Southco 97 / EMKA 1080 Ø12 (A K E F) | ✔ |
| Ayak | GN 20 hijyenik M12 (yalnız E yere basar; A / TOPPING / F / K B'ye oturur) | ✔ |
| Fitil / conta | nötr kapakta fitil yok (A K E — dikme önüne 0,5 boşluk), soğukta (B TOPPING) fitil | ✔ işlevli |
| Kulp | yok (bas-aç) her yerde | ✔ |

## 8 · ADIM 55 DENETİMİ

- Zincir: `55_uyum.py` v9v → v9w, iki ayrı iş klasöründe (z55A, z55B) **bayt aynı**. 123 pul: beklenen sayılar tuttu (DIN 9021 M5 95 · DIN 9021 M8 18 · DIN 125 M8 10).
- Somun / cıvata yönü: somun = pula değen, boyu ≤ 1,15 × ISO 10511 yüksekliği (perçin somun / PEM somun sayılmaz); yoksa pulu geçen cıvatanın kısa uzantılı
  yanı baş. Örnek ölçüm: B şase pul 124,5–126,1 (oturma B tabanında), cıvata 110,1–134,1 (−0,4) · A→TOPPING pul 1432,9–1434,5, cıvata +0,4.
- Çakışma (tam model, c8a 22 işçi, 12 118 bileşen; taban v9v aynı araçla): v9v 1063 = gerçek 74 · kasıtlı 804 · şüpheli 185 → v9w aynı 1063 / 74 / 804 / 185 · **YENİ 0, KALKAN 0** (cak/fark.txt). Temas 23 494 → 23 474 (büyük pulların komşuya değmesi kalktı). Pul oturma yüzü korunduğu için havada parça oluşmaz; somun / cıvata pula değer.
- Sayfa: meshopt kayıpsız (5655 bv bayt aynı, HATA 0, dogrula.mjs extras aynı) · makine_v3_8.html `?v=9x`.

## 9 · KUŞBAŞI (adım 54, öncelikli ek) — özet

Huni sağ duvarı x 1880 düz (önden arkaya), hortum ↔ huni 10,65 mm, huni öne / yukarı süpürme temas 0, iç hacim 6,27 L (kullanılabilir 5,64 ≥ 3,4).
**UNO gövdesi** (vana bloğu 1889, TC kelepçe 1893,5, döner vana tahrik ucu 1891–1916) öne çekilirken kıyma hattının alt hortum ucu / kelepçesine çarpar:
gövde 159 mm geniş, harç hattı ile kıyma hattı arası 140 mm → hortum yeri sabitken gövde ancak kıyma hortumu kelepçesinden sökülünce çıkar (Kemal kararı).
