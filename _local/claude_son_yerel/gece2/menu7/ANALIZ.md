# TOPPING · YENİ MENÜ ANALİZİ (yalnız pide + lahmacun) — 4 Eki 2026

SALT OKUMA. Model, sayfa ya da üreteç değişmedi. Ölçüler `hat3_v9t.glb` dosyasından (TOPPING_MODUL + TOPPING_GOVDE düğümleri, bağlı parça kutuları) ve `tpaket/tp_olcu.py`'den alındı. Hesap: `menu7/hesap.py`. Şema: `menu7/yerlesim.png`.
Etiketler: **[K]** kaynaklı · **[H]** hesap · **[V]** varsayım (pilotta tartılıp ölçülecek).

---

## KISA CEVAP

1. **7 ürün sığıyor.** Kullanılabilir hacim yetmeyen tek hazne yok. **Lahmacun harcı ise tam sınırda:** 2 günde 42,0 L gerekiyor, haznenin kullanılabilir hacmi 42,3 L. Hazne üstü 30 mm yükseltilirse 52,1 L'ye çıkıyor.
2. **Hazne şekli:** yuvarlak koni bizim dar ve derin dolabımızda hacmin **%32–62'sini** kaybettirir. Hazne gövdemiz zaten "altı yuvarlak, üstü köşeli" geçiş hunisi. Önerim bu şekli korumak, **dikey köşeleri R 25 yapmak** (yalnız %0,6 hacim kaybı) ve kaynak yerlerini taşlayıp R ≥ 6 bırakmak.
3. **Üst ortaya 3. UNO sığıyor.** 200 genişlikte her iki yanda 19 mm pay kalıyor. **Tek gerçek engel arka taraf:** 3. UNO'nun pnömatik silindiri sağ evaporatörün (R) tam içine düşüyor. Çözüm için soğutmacı firmanın R kasetine kılıf (cep) açması gerekiyor (aşağıda seçenek 1).
4. **Yeşil hortum yolu çalışıyor.** Kuşbaşı ile kaşar arasında 64,9 mm boşluk açılıyor (gereken ≥ 62). Hortum ancak hazne üst bölümünün **89 mm'lik kısmında** hazneye çarpıyor. Bu yüzden haznenin tamamını dik kenarlı yapmaya gerek yok: **yalnız ön-sağ köşeden bir cep** açmak yetiyor. Böylece hazne 9,1 L'den 8,5 L'ye iniyor (tam eksantrik yapılsa 6,1 L olurdu).

---

## 1 · İKİ GÜNLÜK İHTİYAÇ ↔ HAZNE

### Satış ve doz girdileri
- **Günde 80 pide + 200 lahmacun [K]:** kural kitabı 2.1 ve stok kurgusu (16 Eyl).
- **Pide dağılımı [V]:** Kemal'in "patates ve tavuk çok satar" sözüne göre patatesli 20 · tavuklu 20 · kıymalı 10 · kuşbaşılı 10 · kaşarlı 10 · sucuklu 10. Gerçek oran farklıysa aşağıdaki "günde en çok" sütunu doğrudan okunabilir.
- **Dozlar ve yoğunluklar [K]** (`topping_v2_hesap_v2.py`): harç 110 g (1,048 g/ml) · kıyma 160 g (1,053) · kuşbaşı 145 g (0,853, parçalar arası boşluk dahil) · kaşarlı 130 g kaşar · sucuklu 70 g sucuk + 90 g kaşar.
- **Patates püresi [V]:** 150 g/pide · 1,05 g/ml. Kaynak bulunamadı, pilotta tartılacak.
- **Tavuk küp [V]:** kuşbaşı ile aynı alındı (145 g · 0,853 g/ml).
- **Hacim [H]:** brüt hacim, hazne şeklinin integraliyle hesaplandı: Ø64 yuvarlak boyundan 440 derinlikteki dikdörtgen üst kesite geçiş + üstteki kutu. Mesh dışbükey zarfıyla karşılaştırıldı, fark %3'ün altında.
- **Kullanılabilir hacim [V]:** brüt × 0,90 (kapak altında %10 doldurma payı).

| Hazne (öneri) | Ürün | Günlük | 2 gün | Brüt | Kullanılabilir | Yeterli mi | Bu hazne günde en çok |
|---|---|---|---|---|---|---|---|
| Üst sol 380 (mevcut harç) | Lahmacun harcı | 22,0 kg | 44,0 kg = **42,0 L** | 47,0 L | 42,3 L | **SINIRDA** (pay %0,7) | 201 lahmacun |
| Üst orta 200 (YENİ) | Patates püresi | 3,0 kg | 6,0 kg = 5,7 L | 25,1 L | 22,6 L | ✓ (4×) | 79 pide |
| Üst sağ 220 (eski sos) | Kıyma | 1,6 kg | 3,2 kg = 3,0 L | 17,2 L | 15,5 L | ✓ (5×) | 51 pide |
| Alt 1. UNO 190 (eski kıyma) | Tavuk | 2,9 kg | 5,8 kg = 6,8 L | 9,1 L | 8,2 L | ✓ (pay %20) | **24 pide** |
| Alt 2. UNO 190 + ön-sağ cep | Kuşbaşı | 1,45 kg | 2,9 kg = 3,4 L | 8,5 L | 7,7 L | ✓ | 23 pide |
| (Alt 2. UNO tam eksantrik) | (Kuşbaşı) | | | 6,1 L | 5,5 L | ✓ | 16 pide |
| Kaşar kaseti | Kaşar | 2,2 kg | 4,4 kg | 8,8 kg [K] | — | ✓ (2×) | — |
| Sucuk kaseti | Sucuk | 0,7 kg | 1,4 kg | 2,8 kg [K] | — | ✓ (2×) | 20 sucuklu |

### Dikkat edilecekler
- **Harç:** 200 lahmacunda pay yok. Çözüm hazne üstünü 2099'dan 2129'a çıkarmak: tavana 10 mm kalır, hazne 52,1 L brüt / 46,9 L kullanılabilir olur (pay %12). Kapak tavana 10 mm kalınca kalkabiliyor mu, ona bakılmalı. Alternatif: harç dozu 110 yerine 100 g olursa 38,2 L'ye düşer.
- **Tavuk:** hazne 190 genişliğinde. Tavuklu pide günde 24'ü geçerse yetmez. Seçenekler:
  - (a) Hazne önünü z −120'den −60'a uzatmak: 9,1 → 10,2 L, günde 27 pideye yeter.
  - (b) **Tavuk ↔ kıyma yer değiştirmesi:** tavuk üst sağdaki 17,2 L'lik hazneye geçer (dik hortum, günde en çok 45 pide), kıyma alt 1. UNO'ya iner (günde en çok 27 pide). Riski aşağıda ayrıca yazdım.
- **Kaşar:** patatesli ve tavuklu pidelere de kaşar konacaksa (ör. 60 g [V]) günlük kaşar 4,6 kg, 2 günlük 9,2 kg olur. Bu kasetin 8,8 kg'ını **aşar.** Menü netleşince bakılmalı.
- **Kuşbaşı:** 2 günde 3,4 L gerekiyor. Ön-sağ cepli haliyle 8,5 L, tam eksantrik haliyle 6,1 L; ikisi de yetiyor. Cepli olan daha çok hacim bırakıyor.

---

## 2 · HAZNE ŞEKLİ: KÖŞELİ Mİ, YUVARLAK MI?

**Önce bir düzeltme:** bizim haznemiz tam köşeli piramit değil. Boyun Ø64 yuvarlak, üst kesiti 190/220/380 × 440 dikdörtgen. Yani zaten **"kare-yuvarlak geçişli"** bir huni. Beldos'un yuvarlak hazneleri ise geniş ve kısa gövdeli makinelere göre yapılmış.

### Aynı dolap ölçüsünde hacim [H]

| Şekil | 190 × 440 × 215 (alt UNO) | 200 × 440 × 392 (orta) | 380 × 440 × 392 (harç) |
|---|---|---|---|
| A · geçiş hunisi, keskin köşe (mevcut) | 9,06 L | 25,08 L | 47,04 L |
| A' · aynısı, dikey köşeler R 25 | 9,00 (−%0,6) | 24,93 (−%0,6) | 46,89 (−%0,3) |
| B · yuvarlak koni (çap = dar kenar) | 3,46 (**−%62**) | 9,34 (**−%63**) | 32,19 (**−%32**) |
| C · oval/stadyum (uçlar yarım daire) | 8,28 (−%9) | 22,70 (−%9) | 38,46 (−%18) |
| D · eksantrik (bir kenar dik) | 6,18 (−%32) | 16,69 (−%33) | 27,67 (−%41) |

Dolaplarımız dar ve derin (190–380 × 440). Yuvarlak bir koni yalnızca dar kenarın çapını kullanabildiği için hacmin üçte biri ile üçte ikisi arasını kaybettiriyor.

### Akış (Jenike ve huni tasarımı literatürü)

**Kaynaklar:** Jenike A.W. (1964), *Storage and Flow of Solids*, Bulletin 123, Univ. of Utah · Schulze D. (2008/2021), *Powders and Bulk Solids*, Springer, huni tasarımı bölümü.

- **Kütle akışı (her şey birlikte iner) ile huni akışı (ortası boşalır, kenarlar durur):** kütle akışı ancak duvar düşeye yeterince yakınsa olur. Sınır açı, ürünün duvar sürtünmesine ve iç sürtünmesine bağlıdır.
  - Literatürdeki diyagramlarda sınır, konik huni için tipik olarak düşeyden **≈ 15–25°**.
  - Kama/geçiş hunisi (düzlemsel akış) için **≈ 8–12° daha yatık** olabilir.
  - Bu değerler diyagramdan okunan genel aralıklardır, ürünlerimiz için ölçülmemiştir.
- **Köşe (vadi) açısı:** piramit hunide köşe çizgisi duvardan daha yatıktır: tan θv = √(tan²θ₁ + tan²θ₂). Ürün önce köşede durur, ölü bölge oluşur. Yuvarlak ve geçiş hunilerinde bu köşe yoktur ya da yumuşar.
- **Bizim hunilerimizin açıları (düşeyden) [H]:**

| Hazne | Yan duvar | Ön duvar | Arka duvar | Ön köşe |
|---|---|---|---|---|
| 190 | 19° | **52,5°** | 38° | 53,5° |
| 380 | 41° | **52,5°** | 38° | 57,6° |

  **Asıl sorun köşe değil, ön duvar.** Boyun arkaya kaçık (z −387), üst kesitin merkezi ise −340'ta. Bu yüzden ön duvar yataya 37,5° kadar yatıyor. Hamur kıvamındaki ürünler (harç, kıyma, püre) bu eğimde kendi ağırlığıyla kaymaz; UNO pistonunun emişi ve ürünün ağırlığıyla iner. Ön duvarı düşeyden 30°'ye getirmek ≈ 400 mm huni yüksekliği ister, bu yer yok.
  **Öneri:** pilotta ön duvarda kalan ürüne bakılsın. Gerekirse Beldos'a karıştırıcılı hazne seçeneği sorulsun (Beldos'ta böyle bir seçenek olup olmadığını doğrulamadım).
- **Parça ürünlerde köprülenme:** tavuk ve kuşbaşı küplerinin parçalar birbirine kilitlenip boyunda köprü kurmaması için boyun en az 5–8 × parça boyu olmalı (Schulze, kaba taneli ürünlerde mekanik köprü). Ø64 boyun için **küp ≤ 12 mm** önerilir. Bugün kuşbaşı için de aynı risk geçerli.

### Hijyen ve temizlik

**Kaynaklar:** EN 1672-2:2020 · EN ISO 14159 · EHEDG Doc. 8. Değerleri hafızadan yazdım, standart metniyle teyit edilmeli.

- Gıdaya değen iç köşeler **R ≥ 3 mm** olmalı (EN 1672-2 ve ISO 14159). EHEDG mümkünse **R ≥ 6 mm** öneriyor.
- Bizim gövde standardımızda gıda köşesi R 3 (`R_GIDA`).
- Hazneler her gün sökülüp yıkanacağı için **dikey köşelerde R 25** öneriyorum: fırça rahat dönüyor, hacim kaybı yalnız %0,6.
- Kaynak dikişleri taşlanıp R ≥ 6 bırakılsın.

### Üretim

| Şekil | Nasıl yapılır | Not |
|---|---|---|
| Geçiş hunisi | Saçtan açınım, abkantta çok sayıda küçük büküm, 1–2 dikiş TIG + taşlama | Kemal'in sac standardına uygun |
| Konik | Saç haddede kıvrılır + 1 dikiş; ya da sıvama (dikişsiz, en hijyenik) | Bizim dar ölçülerimizde hacmi çok düşük |
| Eksantrik | Geçiş hunisiyle aynı yöntem | Bir yüzü düz, büküm sayısı azalır |

### Ürüne göre öneri

| Ürün | Şekil | Duvar (düşeyden) | Not |
|---|---|---|---|
| Lahmacun harcı | A' geçiş, köşe R 25 | Yan ≤ 41° (mevcut), ön 52,5° → pilotta izle | Hacim kritik, yuvarlak olmaz |
| Patates püresi | A' geçiş, köşe R 25 | ≤ 21° yan | Soğukken sertleşir; ön duvarda kalmayı izle |
| Kıyma | A' geçiş, köşe R 25 | ≤ 23° yan | |
| Tavuk küp | A' geçiş, köşe R 25 | ≤ 19° yan | Küp ≤ 12 mm |
| Kuşbaşı | A' + ön-sağ cep (köşeler R ≥ 6) | ≤ 19° yan, cep yüzü dik | Küp ≤ 12 mm |

---

## 3 · YERLEŞİM ÖLÇÜMLERİ (v9t)

**Koordinat düzeni:** x hat boyu, y yukarı, z öne doğru.
Soğuk oda içi x 1496–2440 · alt göz 1152–1534 · üst raf 1534–1575 · üst göz 1575–2139. Tüm düşme noktaları z −170'tedir.

### (a) Üst ortaya 3. UNO sığar mı? — EVET

- Harç haznesinin sağı x 1912, sağ haznenin (eski sos) solu 2149,5. **Arada 237,5 mm var**, merkez 2031.

| Orta hazne genişliği | Her iki yanda pay | Brüt hacim (üst 2099) |
|---|---|---|
| 190 | 23,8 mm | 23,9 L |
| **200 (öneri)** | **18,8 mm** | **25,1 L** |
| 210 | 13,8 mm | 26,3 L |
| 217 | 10 mm | 27,2 L |

- Huni seviyesinde en dar yer y 1887'de (harç hunisi orada 1912'ye ulaşıyor): 200 genişlikte 19 mm kalıyor.
- Vana seviyesinde (y 1575–1648) 3. UNO'nun vana takımı x 1940–2076'yı kaplıyor (yan aktüatör dahil). Harç flanşına 172 mm, sağ UNO'nun aktüatörüne 92 mm kalıyor ✓.
- Patatese 5,7 L yettiği için orta hazne daha alçak da yapılabilir. Yükseklik serbest.

### (b) 3. UNO'nun arka pnömatik silindiri ↔ evaporatör — ÇAKIŞIYOR

- Mevcut UNO'larda pnömatik takım kuru bölmede duruyor: x ±26, y 1534–1632, z −811…−630. Silindir Ø37 × 150, POM burçla arka duvardan geçiyor.
- 3. UNO'nun takımı (x 2005–2057) **sağ evaporatörün (R: x 1758–2223 · y 1383–1835 · z −826…−640) tamamen içinde** kalıyor. POM burcu da R'nin üfleme ağzından (x 1807–2174 · y 1582–1786) geçiyor.
- Nelere çarpmıyor: L evaporatörüne (1446–1670), R fanına (x 1800–1921, 91 mm uzakta) ve R'nin kollektör/TXV şeridine (2126+).
- Bugün harç takımı L ile R'nin arasındaki 88 mm boşluktan geçiyor. 3. UNO için böyle bir boşluk yok.

**Evaporatör yüzü / hacmi (`tp_olcu.py`, `tp2_log.txt`, bellek: TC v31):**

| Durum | Serpantin | Yüz (mm²) | Mevcuda göre | Eski tek kasete göre | Serpantin hacmi |
|---|---|---|---|---|---|
| Eski tek kaset (TC v31) | 397 × 137 × 85 | 54 389 | −%23 | — | 4,62 L |
| **Mevcut L + R** | 142 × 176 + 327 × 140 | **70 772** | — | +%30 | 6,01 L |
| Seçenek 1 · R'de kılıf/cep | serpantin aynı | 70 772 | **%0** (fan bölmesi kesiti ≈ −%30, fan dışında) | +%30 | 6,01 L |
| Seçenek 2 · R'yi ikiye böl (arada 88 koridor) | L + 147 × 140 (sağ parça kollektöre yeter, serpantine yetmez) | 45 572 | **−%36** | −%16 | 3,87 L |
| Seçenek 3 · R'yi soldan daralt, 3. UNO sola (c ≈ 1860) | L + 197 × 140 | 52 572 | −%26 | −%3 | 4,47 L |

- **Seçenek 1 (öneri):** R kasetinde üstten açık, yalıtımlı bir **cep** (≈ 116 mm genişliğinde, PU 20 + iki saç) açılır. 3. UNO'nun silindiri cepte durur, hava hatları cepten yukarı çıkar. Serpantin y 1425–1565'te, cep 1570'in üstünde kaldığı için serpantine dokunulmaz.
  - Şart: silindirin altındaki tutucu plakanın (bugün y 1534–1577) y 1570'in üstüne alınması.
  - Fan bölmesi daralır, fan ise etkilenmez. Üfleme ağzında yalnız burç kılıfı kadar (≈ %3) alan kaybolur.
  - Bu kaseti soğutmacı firma yapar. Bizim işimiz, kural gereği yalnız yer zarfını vermek.
- **Seçenek 2 ve 3:** serpantin yüzü %26–36 azalır. Bu, eski "buharlaşma–oda farkı 13 K, büyük bobin değerlendirilsin" notunu yeniden açar. Ayrıca seçenek 3'te orta huni çok eksantrik olur (sağ duvar düşeyden 58°). İkisini de önermiyorum.
- Ters çevirme (silindir önde) ya da 90° çevirme (silindir x yönünde) **sığmıyor:** takım boyu ≈ 420 mm. Önde 384 mm, yanda 263 mm yer var.

### (c) Yeşil hortum yolu — ÇALIŞIYOR

- **Yol:** 3. UNO'nun çıkışı rafın üstünde y ≈ 1595–1631'de rijit paslanmaz dirsekle sola döner (x 2031 → 1911,5, 2 adet 90° sıhhi dirsek, R ≈ 50). Sonra raftan dik iner: x 1890,5–1932,5 (D42), z −191…−149.
  - Esnek hortumla S-kıvrım yapılamaz: R ≈ 100 için ≈ 180 mm düşey yer gerekir, rafa kadar yalnız ≈ 40 mm var.
- **Hortum ile kuşbaşı haznesi arasındaki boşluk:**
  - Kuşbaşı hunisinin ön duvarı y 1410'un altında z −191'in gerisinde kalıyor. Hortum oralarda hazneye değmiyor.
  - Çakışma yalnız **y 1410–1499 (89 mm yükseklik)** aralığında. Bu yüzden önerim tam dik kenar yerine **ön-sağ köşe cebi** (x > 1879, z > −201, 64 × 81 × 89).
  - Cebin dik yüzü x 1879,1'de, boyunun sağ kenarıyla aynı hizada.
- **Boşluklar:**

| Nerede | Ölçü | Sonuç |
|---|---|---|
| Hazne dik yüzü 1879,1 → kaşar kılavuzu 1944,0 | **64,9 mm** | ≥ 62 ✓ (pay 2,9) |
| Hazne dik yüzü 1879,1 → kaşar kaset duvarı 1948,5 | 69,4 mm | ✓ |
| Hortum (D42) her iki yanda | ≈ 11 mm | ✓ |
| Hazne altı (y 1152–1284), hortum hizasında: kuşbaşı dirseği 1866 → kaşar 1944 | **78 mm** | ✓ |

  Kuşbaşı vanası (sağ kenarı 1889) ve flanşı (1893,5) z ≤ −342'de, hortumun 150 mm gerisinde kalıyor. Hortumla çakışmıyor.
- **Kelepçe:** yalnız uçlarda (raf ağzı ve düşme kovanı). Düz bölümde kelepçe yok, 62 mm şartı sağlanıyor.
- **Kaset sökme:** kaşar kaseti öne çekilerek sökülüyor. Hortum kasetin x aralığının dışında (≤ 1932,5 < 1944), sökmeyi engellemez ✓.
- **Düşme noktası:** x 1911,5 · z −170, tabla/hamur yolunun içinde ✓.
  - Taban sandviçinde yeni Ø38 kovan gerekir (harç/sos kovanları gibi).
  - Komşulara mesafe: kuşbaşı kovanı 1826–1870 (aradaki duvar 23 mm), kaşar mandalı 1951 (17 mm) ✓.
  - Kuşbaşı ağzıyla arası 64 mm. İkisi aynı anda dökmüyor, sorun yok.

### (d) Sos UNO'su kalkınca ne açılıyor?

- **Üst sağ UNO (220, 17,2 L) ve dik hortumu (x 2239–2280)** olduğu gibi kalır, yalnız ürünü değişir.
- **Sos yayıcısı serbest kalır:** SMC CRB2BW10 döner aktüatör (y 1194, z −130…−115), yarıklı boru, kesme vanası, tabandaki hava hattı şeridi. Raf altında x ≈ 2235–2290 bölgesi boşalır.
- **Önemli fırsat — karar 1:** patates püresi pideye **yayılarak** konur. Bu, sos ve harç gibi "YAYICI" tipi bir doz. Üst sağa **patates** konursa sos yayıcısı hiç değişmeden patatese geçer. Orta UNO'ya da **kıyma** (NOKTA, Ø33 ağız, en az hacim: 3,0 L) gelir. Bu durumda:
  - Patates için 17,2 L hazne kalır (2 gün 5,7 L ✓, günde en çok 54 pide).
  - Kıyma, bükümlü hortumdan bastırılarak iner. Çiğ kıymanın 2 dirsekte kalıntı bırakması hijyen açısından daha çok temizlik demek, ama soğuk odanın içinde.
  - Claude'un önerisinde (orta = patates) orta UNO'ya yeni bir yayıcı ya da NOKTA ağzıyla spiral gerekir. Sos yayıcısı da boşa çıkar.
- Pizza menüden kalkınca sim tarafındaki `URUN__sos_*` ürün düğümleri, E'deki `E_PIZZA` ve pizza reçeteleri de boşa düşer. Bu analizin kapsamı dışında, yalnız not.

---

## 4 · KEMAL'E KARAR LİSTESİ

1. **Üst orta / üst sağ dağılımı:**
   - (A) Claude'un önerisi: orta = patates, sağ = kıyma.
   - **(B) Önerim:** orta = kıyma, sağ = patates. Sos yayıcısı patatese aynen geçer, yeni yayıcı gerekmez.
2. **Kuşbaşı haznesi:**
   - Kemal'in çizimindeki tam dik kenar → 6,1 L.
   - **Yalnız ön-sağ köşe cebi** → 8,5 L. İkisinde de hortum payı 64,9 mm.
3. **3. UNO silindiri ↔ sağ evaporatör:**
   - **Öneri:** R kasetinde yalıtımlı cep. Serpantin aynı kalır, iş soğutmacı firmada.
   - Diğer seçenekler (R'yi bölmek / daraltmak) serpantinin %26–36'sını kaybettirir.
4. **Harç haznesi:** 200 lahmacunda tam sınırda (42,0 / 42,3 L). Üstü 30 mm yükseltilsin mi (→ 52,1 L, tavana 10 mm kalır)?
5. **Tavuk:** günde 24 pideye kadar alt 1. UNO yeter. Daha çok satacaksa iki yol var:
   - Hazne önünü uzatmak → günde 27 pide.
   - Tavuk ↔ kıyma yer değişimi → tavuk üst sağda, günde 45 pide. Risk: küpler hortumda takılabilir.
6. **Menü bilgileri (benim varsayımlarım, pilotta düzeltilecek):**
   - Patatesli ve tavuklu pidede kaşar var mı? Varsa kaşar kaseti 2 günü taşımaz (9,2 > 8,8 kg).
   - Patates dozu: 150 g varsaydım.
   - Tavuk küp boyu: ≤ 12 mm öneriyorum.
   - Tavuk çiğ mi, pişmiş mi gelecek? Gıda güvenliği ve çapraz bulaşma açısından önemli.
7. **Hazne şekli:** yuvarlağa geçilmesin. Mevcut geçiş hunisi korunsun, dikey köşeler R 25, dikişler R ≥ 6 olsun.
