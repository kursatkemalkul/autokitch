# AUTOKITCH — bağımsız istasyonlar, yerel v1

Önceki ana model korunur. Bu klasör yeni bir mühendislik ön tasarımıdır; üretim veya kaldırma uygunluk belgesi değildir. Robot, QR dolabı ve personel tezgâhı kapsam dışıdır. İnternete yayımlanmadı.

## 3D model

Yerel adres: `http://127.0.0.1:8779/otonom/hat/moduler-v1/`

- Kurulu makine, ayrılmış taşıma modülleri, yalnız gövde, iç düzen ve yeni parçaları vurgulama görünümleri.
- A, B, C, F, K, E ayrı seçilebilir. Mevcut A/C ortak tabla-ray mekanizması **T** adlı sökülebilir alt montajdır. Sürekli ray kesilmedi; mekanizmanın ortasına yeni bir ek yapılmadı.
- Arka −830, ön +79, alt dolap üstü 788, A/C mekanizma kotu 892 mm korunur. Taşıma kızakları yalnız taşıma görünümünde gösterilir.
- B, önceki karara uygun olarak 4000 mm uzunluğunda tek dolaptır. Bağımsız istasyon olması dar bir dükkân girişinden geçeceği anlamına gelmez; giriş, dönme ve taşıma güzergâhı ölçülmelidir.

## Değişiklikler

| Bölge | Yeni düzen |
|---|---|
| A açıcı | Kendi 1,5 mm 304 sağ duvarı; tabla geçişi ve pnömatik portları açık. Sağ gövde kayıtları yalnız 2 mm içeri alındı; mekanizma ölçüsü değişmedi. C birleşiminde sökülebilir çevre contası. |
| B alt dolap | Plint içinde 60×80×3 mm kapalı profil alt şase; ayakların üzerinde dişli bağlantı yuvaları. A/C altında 30×40×2 üst kiriş ve bölmeler içinde 30×30×2 dikmeler. |
| B ısı köprüleri | Yeni üst taşıyıcıların üzerinde ve dikme tabanlarında 3 mm GFRP ara parça. Köpük/saclarda gerçek oturma yuvaları; raylara veya gıda gözlerine kesik atılmadı. Arka dikmeler kablo kanalından 3 mm ayrıldı. |
| A/C kaideleri | Mevcut 40×100×2 mm kaideler korundu. B'ye sökülebilir M8 bağlantı; yük köpüğe değil taşıyıcıya gider. |
| F fırın | Mevcut fırın ve üst kabin kabukları/taşıyıcıları korundu. Alt dolapla birlikte kaldırılmaz. |
| K/E | Plint içinde 40×60×3 mm alt şase. Orta ayak bağlantıları da şaseye bağlandı. Mevcut kendine ait yan/arka duvarlar korundu; üst üste gereksiz ikinci duvar eklenmedi. |
| Birleşimler | B–K ve K–E alt bağlama plakaları. Bunlar hizalama bağlantısıdır, bir istasyonun ağırlığını komşuya asmaz. Dişler sadeleştirilmiş geometridir. |

Malzemeler: taşıyıcı ve yeni saclar AISI 304; yalıtım PU; çevre conta EPDM; taşıyıcı ısı kesiciler GFRP. Eski görünüm kodunun “şeffaf ön” diye işaretlediği PU çekirdekleri yeniden **PU** olarak tanımlandı. Kesit veya dış kabuk gösteriminde üçgen silerek sahte açıklık oluşturulmuyor.

## Hesap ve denetim sınırları

`checks.json` gerçek çalıştırma sonuçlarını içerir: yeni parça katı geçerliliği, yeni taşıyıcıların diğer katılarla kesişimi, temasları ve basit kiriş hesapları. Geometrik temas, kaynak veya civata dayanım hesabının yerine geçmez.

Son koşu: yeni katılarda **0 geçersiz parça**, taranan yeni taşıyıcılarda **0 çakışma**, komşusuna temas etmeyen yeni taşıyıcı **0**. Tarama hacim eşiği 0,5 mm³; temas eşiği 0,06 mm. Sadeleştirilmiş civata bağlantıları ve taşıma kızakları çakışma taramasından ayrı tutuldu. Yedi kiriş hesabı, belirtilen varsayımlarda geçti. Altı gövdenin arka sınırı −830 ve cephe sınırı +79 mm ölçüldü. Tarayıcı hatası yok; ayırma/gizleme/vurgulama ile STEP/BOM bağlantıları denendi. `mass_audit.json` düzeltmeden önceki ham hacim teşhisidir; geçerli kütle değerlendirmesi **checks.json** içindedir.

Kirişler: E=193000 MPa (muhafazakâr hesap varsayımı), izin verilen eğilme gerilmesi 140 MPa (bu ön tasarımın seçimi), sehim sınırı L/300. Basit mesnet ve ortada noktasal yük yaklaşımı; eşit yük paylaşımı varsayılır. Bunlar tüm makinenin sonlu eleman analizi değildir.

| Kontrol | Hesap yük zarfı | Destek açıklığı |
|---|---:|---:|
| B boş taşıma | 1000 kg; dinamik katsayı 2 | **en fazla 1000 mm** |
| B kullanım, yerel ayak açıklığı | 1300 kg; katsayı 1,5 | 960 mm |
| A kaide | 220 kg; katsayı 2 | 684 mm |
| C kaide | 600 kg; katsayı 2 | 446 mm |
| K alt şase | 350 kg; katsayı 2 | 500 mm |
| E alt şase | 400 kg; katsayı 2 | 710 mm |
| B A/C üst taşıyıcı | toplam 820 kg; 8 destek, katsayı 1,5 | 683 mm |

**Bu sayılar ölçülmüş makine ağırlıkları veya onaylı taşıma kapasiteleri değildir.** CAD'in bilinen malzeme hacimleri ön kontrol için kullanıldı. Bulaşık makinesinin basitleştirilmiş dolu gövdesi çelik ağırlığına çevrilmedi; kaynak üreteçte kayıtlı 70 kg katalog değeri kullanıldı. Bilinmeyen malzemeler, satın alınan parçaların iç yapısı ve gıda yükleri tamamen kapanmış değildir. Son tartım ve yük dağılımı bu zarfları aşarsa yeniden boyutlandırma gerekir.

Denetim dışında: mevcut mekanizmaların tüm dinamik taraması; robot erişimi; kaynak dikişi hesabı; ayak katalog kapasitesi; devrilme/sismik kontrol; kaldırma ekipmanı sertifikasyonu; GFRP sınıfı/sürünmesi, yoğuşma ve bütün soğutma yükünün yeniden doğrulanması. GFRP şeritleri bir malzeme sınıfı önerisidir, kesin satın alma kodu değildir. Gıda tarafındaki bağlantı ve panel birleşimleri sızdırmaz/hijyenik sonlandırılmalıdır.

## Taşıma ve kurulum sırası

1. Gıda, GN kapları ve yedek stokları boşalt; çekmeceleri/kapakları mekanik taşıma kilidiyle sabitle. Kilidin nihai donanım seçimi henüz yapılmadı.
2. A/C ortak T ray-tabla alt montajını ve modüller arası hava/elektrik bağlantılarını servis prosedürüyle ayır. T sökme sırası ve yeniden hizalama mastarı prototipte doğrulanmalıdır.
3. Üst A/C/F modüllerini taşıma kızaklarına al. Kızaklar kavramsal desteklerdir; askı mapası veya sertifikalı palet olarak değerlendirilmez.
4. B'yi sürekli yük dağıtan taşıma yatağıyla veya destek aralığı **≤1000 mm** olan ekipmanla taşı. Yalnız iki uçtan ya da gelişigüzel forklift çatallarıyla kaldırma.
5. Dükkânda önce B/K/E'yi kendi ayaklarında terazile; alt birleştirme plakalarını bağla. A/C/F'yi oturt; T'yi hizalayarak geri monte et.
6. Ön/arka düzlem, ürün geçiş kotları, kablo/hortum payları ve çekmece açıklıkları kontrol edilir. Enerji vermeden önce koruyucular ve güvenlik kilitleri ayrıca doğrulanır.

## Dosyalar ve yeniden üretim

- `otonom/hat/moduler-v1/moduler_v1.glb`: tüm makinenin yeni modüler 3D görünümü.
- `MODULER_EK_PARCA_v1.step`: 29 Eylül 2026'da siteden kaldırıldı (kural 6.7: STEP çıktısı yok). Dosya git geçmişinde ve Codex iş klasöründe duruyor.
- `BOM_EK.csv`: ek parça geometrisi/malzeme listesi; kesim ve kaynak atölye resimlerinin yerine geçmez.
- Üreteç: `arastirma/_uretec/moduler_istasyon_v1/model.py`; `--check-only` yalnız denetim yapar.
- `source_dependencies.json`, `legacy_dependencies/`, `legacy_assets/`: eksik eski bağımlılıkların görev içinde sabitlenmiş kopyaları. Ana Claude çalışma klasörü değiştirilmedi. `.cache` yeniden oluşturulabilir, sürüme alınmaz.

Malzeme ailesi referansı: [Outokumpu Core](https://www.outokumpu.com/en/products/product-ranges/core). Hesap kabulü, kaynak ve profil toleransları üreticinin sertifikalı malzemesiyle ayrıca doğrulanır.
