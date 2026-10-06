# Robot/ray/QR v21 · ana sahne

Makine tabanı main adım80 `hat3_v10l.glb.gz`; K/E/TOPPING dosyaları değişmez. Yeni ana sayfa v21 birleşik modeli kullanır. Eski tezgâh ve dış tesisat çıkarılmıştır. Robot UR10e, kısa turkuaz ortak uç ve onaylanan ısıtıcısız 3×4 QR aynıdır.

GLB metre / Y yukarı. Isaac kayıtları metre, radyan, saniye / Z yukarı; dönüşüm X etrafında −90°. Ray ekseni dünya Z=0.960, robot taban kotu Y=0.130; ray uçları X=0.978–5.058 (4080 mm). Konsept strok 3684 mm; oynayan araba merkezi X=1.376–4.860. Üretici CAD'in araba ve kesitleri korunmuştur. Yalnız sürekli eksen bölgesi uzatılmıştır: bu özel boy için üretici moment / sürücü / montaj delikleri onayı gerekir.

QR robot yüzü Z=1.750, kolon merkezleri X=3.769 / 4.256 / 4.743; raflar Y=0.588 / 0.850 / 1.112 / 1.374. UR kutusu boyu 475×423×268 mm, QR altında X=4.355–4.830, Y=0.100–0.523, Z=1.775–2.043. Ayaklı kendi kaidesinin altında kablo geçişi vardır. Eksen sürücüsü ayrıca QR sol alt servis alanındadır; kutu boyu varsayımdır.

Besleme duvar şalteri (5.30,1.48,−.80) → zemin dağıtımı → üç kol: makine, QR panosu, UR kutusu. Hareketli kolun bağlantısı UR kutusunun robot çıkışı → sabit korumalı kablo yolu → 80 baklalı enerji zinciri → arabadaki P klipsler → robot tabanı. Eksen motoru kendi sürücüsüne gider; motor ve sürücü CAD değil, destekli yerleşim zarflarıdır ve tedarikçi seçimi açıktır. Zincir dönüş yarıçapı150 mm; UR yüksek esnek kablo Ø14.6 mm için dinamik alt sınır116.8 mm'den büyük.

Kaynak STEP: `_local/codex_robot_v21/igus_ZLW_20200_3000.stp`; igus resmi CAD portalından indirilmiş SKU ZLW-20200S-I0BW0-D0A4B-0A0A0-3000. Orijinal değişmeden saklandı. CAD sha `2c6462714c47b7cfb665d1a7e579d27576ff2f4d923c7fbdf1cb4d82f892cd94`; tessellation/provenance `rail_cad.json`. 3684 mm boy üreticinin yayımlanmış standart STEP'i değildir.

Çalıştırma (repo kökünde, Python/numpy + Node):
`python arastirma/_uretec/robot_integrated_v21/run.py _local/claude_son_yerel/hat3_v10l.glb.gz --repeat 2`
Node PATH'te yoksa AUTOKITCH_NODE ortam değişkeni kullanılır. CadQuery yalnız cache yeniden tessellenecekse gerekir. Zincir90 sarmalayıcısı native GLB girdi/çıktı alır. E/K yeni adımları birleştirilince giriş olarak o birleşik SON model verilir ve iki koşu yeniden doğrulanır.

Ana sayfa: Sipariş seç → Oynat; görev seçiminden hamur / içecek / tatlı / kutu ayrı izlenir. Baştan yeniden oynatır. Patatesli/tavuklu kutu hazır düğmesini bekler. Isaac aktarım JSON'u görevleri ve eklemleri verir. Tutma ideal: ürün robotla birlikte gider; fiziksel kavrama başarısı değildir.

Denetimler `integration_audit.json`, `repeat_build.json`, `browser_checks.json`. Tam robot yolunun güncel modele çarpışma onayı, tüm12 QR rotası ve ikinci lahmacun alma açık; devre / özel ray / kendi adaptörlerinin üretim onayı yok. İstenen cam bölmesi çerçeve / kapı parçalarıyla çıkarıldığı için koruma tasarımı da eksiktir. Üretime hazır veya emniyet sertifikalı değildir. Büyük ham/native GLB dosyaları commit dışı; tarayıcı modeli gzip71MB.
