# Robot v18 — ana sahne entegrasyonu

Kaynak: yayındaki ana sayfanın v8 modeli (`claude_latest/hat3_v10h.glb.gz`, SHA 3d040099…). QR ise onaylanan ısıtıcısız 3×4 adım62 düzenidir. El yıkama tezgâhı ve eski QR çıkarılmıştır. Claude’un TOPPING/F montaj dosyaları değiştirilmez.
Yayındaki makine geometrisi korunur; QR62, kilitleri ve aktarılmış cihazları eklenir. Robot olarak v16 kısa turkuaz uçlu UR10e, 4164 mm ray zarfı ve kayıtlı eklem hareketleri gelir.

Önizleme: http://127.0.0.1:8766/codex-main-robot-v20/otonom/hat/makine.html
Sipariş seç, Oynat'a bas. Görev seçimi dört işi ayrı izletir. Baştan yeniden oynatır. Patatesli/tavuklu kutu hazır sinyali bekler; düğmeyle devam eder. Yoğunluk profili zaman planıdır; çok siparişin ayrı 3B hareket doğrulaması değildir.

Koordinatlar: GLB metre, Y yukarı; makine X hat boyunca, Z öne. Isaac kayıtları metre/radyan/saniye ve Z yukarı; GLB dönüşümü X etrafında -90 derece. FK tabanı/ray dönüşümleri rig.json ve rig.js içinde, özgün v16 ile aynıdır. Ray X: 0.936–5.100 m, ön konumu Z: 0.740–0.980 m. Araba merkezi X: 1.376–4.860 m. QR robot yüzü Z=1.750 m; kolonlar X=3.769/4.256/4.743 m, raf üstleri Y=0.588/0.850/1.112/1.374 m.

Üretim (worktree kökünde):
1. Node --max-old-space-size=8192 arastirma/_uretec/robot_integrated_v18/prepare_published.mjs
2. MACHINE_NATIVE=_local/codex_robot_v20/published_with_qr.glb ortam değişkenini ayarla.
3. Node --max-old-space-size=8192 arastirma/_uretec/robot_integrated_v18/build.mjs
4. Node --max-old-space-size=8192 arastirma/_uretec/robot_integrated_v18/audit.mjs

prepare_published.mjs yayındaki v10h SHA-256 doğrular, meshopt verilerini açar ve QR62 paketini ekler; build kaynak BIN geometri verisini korur, üç stok ürününün indekslerini sabit/hareketli olarak böler, native makine çevrimini ve robot görevlerini zamanlar. Meshopt kayıpsızdır. Ana sayfada panel.js tek saatle klip zamanını yönetir; düşük FPS'de sinyal kapısının atlanmasını engeller. Isaac aktarım düğmesi aynı zamanlanmış görevleri ve eklemleri JSON indirir.

Sınırlar: ideal tutuş; fizik başarısı değildir. Güncel tam makineye karşı bütün yolun çarpışma denetimi, tüm 12 gözün tam rotaları ve ikinci lahmacun alma henüz doğrulanmadı. Üretime hazır veya güvenlik sertifikalı değildir. Zincir, ortak montaj oynatıcı ve Claude'un TOPPING dosyaları değiştirilmedi.

Yerel büyük ara dosyalar commit dışıdır: published_with_qr.glb (~297 MB), combined_native.glb (~536 MB), combined_meshopt.glb (~132 MB). Tarayıcıya çıkan gzip ~64.5 MB.
