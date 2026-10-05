# K montaj · devam kaydı (kaynak adım61)

İş dalı: codex/k-montaj. Claude TOPPING 62–69; K model değişiklikleri 70–79. Ortak oynatıcıya ve TOPPING dosyalarına dokunulmadı. Henüz animasyon teslimi veya üretim/yayın onayı değildir.

1. Kaynak `_local/claude_son_yerel/hat3_v10c.glb.gz` açılır, SHA256 948b20c4520cf917711a8dea730ea037379793b11bb6e975c649155c83ef9c1d doğrulanır.
2. `source_components.py`: gerçek GLB'nin K, K yağ ve K elektrik grupları ayrıştırılır; 782 geometrik bileşen. Bileşen, imalat parçası demek değildir (temaslı parçalar birleşebilir; hazır ürün farklı katılar içerir).
3. `inspect_source.py`, `full_dfm.py`: eski K sac pilotu üretim bilgisi için okunur. 41 açınım, 14 profil, 38 bağlantı. Bu pilot güncel modelin yerine kullanılmaz: adım12 ara taban, adım55 pullar, diğer zincir düzeltmeleri farklıdır. `catalog.py` eşleştirme raporu bunu kaydeder.
4. `plan.py`: yazılı lazer / PEM / büküm hazırlık planı (162 işlem). Bu henüz gerçek kaynakla eşleşmiş tam kurulum/hareket planı değildir. Eski üretecin uyarıları güncel model kusuru gibi sayılmaz.
5. `fastener_audit.py`: gerçek kaynakta 32 M5 panel saplaması somundan 1–3 diş şartını aşar. `70_k_saplama_boyu.py girdi.glb cikti.glb` yalnız bu saplamaların ucunu katalog boyuna çeker; delik, pul ve somun yerleri korunur. Kendi çalışma klasöründe iki koşu: k70a ve k70b, SHA256 4354446e3c4203f18fc1991c0110ec5537663fd222fcc5018571628ca55cbe33. Katalog seçimi ve taşma k70a.json'dadır.
6. `audit_step70.py`: 32 saplama dışında bütün istasyon yüzeyleri (K gövdesi dahil) 0,01mm denetiminde aynı; 32/32 çıkıntı geçti; iki koşu bayt aynı. Dişin gerçek helis profili modellenmiş sayılmaz.

Çalıştırma: CadQuery/numpy ortamında betikler Python ile çalışır. İş çıktıları `_local/codex_k_montaj/`; CAD mm, GLB metre/Y yukarı. Kaynak dosya ve ara 100MB üstü GLB'ler commit edilmez; k70.glb.gz kayıpsız kayıt.

Sonraki: güncel K geometri/üretim eşleştirmesi tamamlanacak; kesici/bant/itici/yağ/pano gerçek bağlantıları planlanacak; bütün saclar gerçek açınım ve sırayla abkantta bükülür, PEM deliklerine basılır. Her parçanın gelişinde gerçek bağlantı veya ekranda geçici dayalı uyarısı; bağlı olmadan yük yok. 2mm aralıklarla yol kontrolü, son konum 0,01mm, vida–delik/diş kontrolü ve bütün §5 geçmeden yayın yok.

Güncel durum: eski K kapsamları dosyalar korunarak bırakıldı. Aktif görev `codex-k-montaj-v2`, dal `codex/k-montaj`. Kemal tamamlanınca yayınlanmasını istedi. Bu yetki §5 tamamlanmadan yayın anlamına gelmez. Ana model zinciri ve site henüz değiştirilmedi.

Model adım70 ana zincire eklenmedi. Birleştirmeden önce güncel KOORDINASYON zincir kilidi alınacak; Claude'un TOPPING çıktısı üzerine tekrar iki koşu yapılacak ve son modelden animasyon yeniden üretilecek.

İkinci yerel hazırlık: `surface_match.py` kaynak GLB köşelerini CAD sınırına örnekler (tek yönlü örnek denetim; tam yüzey eşitliği değildir). Kapak dış genişliği kaynakta 4003–4399, eski pilotta 4003–4398 idi. `current_cad.py` yalnız üretim tanımının bu ölçüsünü kaynakla eşler; model dosyasını değiştirmez. 33/41 sac örnek kontrolde eşleşir. Kalanlar: ara taban ve altı orta kulak güncel kaynakla eşleşmez; üst sacda yaklaşık 0,12mm farklı bir nokta vardır. Bunlar kurulumda kullanılacak diye varsayılmadı.

`bending_data.py` eşleşen 33 sac için 33 büküm üretir. Nötr çizgi boyu korunarak açı ve yarıçap sürekli değişir; başlangıç ve son panel dönüşümleri CAD tanımıyla 0,01mm altında eşleşir. İki JSON üretimi bayt aynı: c3da7718ef35e362faa3775ceff3a0fda1f18d025f9c32eb11846ea62fd20d6b. Bu büküm geometrisi denetimidir; abkant hareketi boyunca takım çarpışması ve sacın tüm yüzeyleri için kaynak eşitliği henüz doğrulanmadı.

Yerel hazırlık önizlemesi: `/codex-k-montaj/arastirma/_uretec/codex/k_montaj/bending-preview.html` (8766 sunucusu). Seçilen gerçek delikli açınım sırayla bükülür, oynat/duraklat/başa dön ve zaman kaydırıcısı vardır. Tarayıcıda sol sac seçimi ve oynatma görsel kontrol edildi. Bu sayfa atölye GEOMETRİ hazırlığıdır; takım, destek, PEM ve bağlı kurulum henüz gösterilmez. K sayfası teslimi sayılmaz ve siteye yayımlanmaz. Ortak oynatıcı değiştirilmedi. §5 `publish_allowed=false` olarak kalır.

## Doğrulanmış yerel bağlantı düzeltmeleri (70–73; zincire henüz eklenmedi)

- 71: gerçek alt bağlantı delikleri, 6 boş 40×40×1,5 profil, 6 mm dişli üst kapaklar, 12 alt FHP-M5-15 bağlantısı ve 12 havşa üst bağlantısı. Raf iki büküm + iki kaynaklı yan sac; servis eksenleri korunur. 131 parça / 24 bağlantı. İç katı kesişim, DFM, diş ve taşma denetimleri geçti.
- 72: bant ayaklarına gerçek 4 M6 bağlantı, itici ayaklarına 8 M5 bağlantı. İtici tabanları iki 4 mm plaka; eski 8 mm kot korunur. Kısa PEM'e ek tam dişli ISO10511 alt somunlar. 112 parça / 12 bağlantı. İç denetim ve kaynak model bağlamında katı kesişim denetimi geçti.
- 73: U'nun mevcut M8×16 cıvataları değişmeden K tavanına iki 4 mm dişli plaka + 3 mm ara plaka. Diş tutuşu 8 mm, taşma 2 mm. 31 parça; 2 bağlantı. Yerel diş, DFM ve kesişim denetimi geçti.
- Her adım iki koşuda bayt aynı; izin verilen K düğümleri dışında bütün geometri 0,01 mm denetiminde aynı. Bunlar tam animasyon yol/bağlantı zamanı denetimi değildir.
- Son kayıpsız kayıt `_local/codex_k_montaj/k73.glb.gz` (55.311.616 bayt); açılmış SHA256 `9d454410dd5ad55d530357b74a6a028de2d16966e303a977df133cb05ff42b45`. `checkpoint.py` üretir/doğrular. 73 tavanın tamamını eski pilottan değiştirmez: kaynak tavanını korur, yalnız iki M8 yatağında delik geometrisini yeniler. Diğer çelik saplama ve elektrik arayüzleri korunur. 30 yeni takviye/kaynak parçası için bütün istasyonlarla temas denetimi geçti; kaynak modelin eski bütün temaslarına üretim onayı verilmedi.
- `cutter_layers.py`: kaynak kesicinin 8 adet kalın plakasını 16 izinli kalınlıkta katmana ayıran üretim önerisi. Katman birleşimi kaynak katısına eşittir; kaynak erişimi/delik DFM henüz doğrulanmadığından modele veya zincire uygulanmadı.

Kalan: tüm K parçalarının güncel kaynak geometri/bağlantı eşleştirmesi, gerçek imalat takımları, geçici dayalı parçalarda fiziksel destek ve sabitleme adımları, her yolun 2 mm örneklenmesi, bütün cihazların bağlantısı ve §5. Tam montaj sayfası henüz teslim edilmedi. Önceki raporlardaki yayımlanabilirlik false korunur.

`source_bending.py`: son k73a modelinin 33 eşleşmiş sacındaki bütün kaynak köşelerini panel/büküm dilimine ters eşler; sınıflanmayan köşe 0, bitiş hatası 0,01 mm altında. Son konumda başka CAD ağına geçiş yok. Bileşen numaraları değiştiği için kaynak ölçülerinden tekil kimlik eşlemesi yapılır; bu kimlik seçimi tek başına yüzey eşitliği sayılmaz. `source-bending-preview.html/js` bu gerçek geometriyi oynatır; takım/kurulum henüz gösterilmez. Yalnız yerel çalışma önizlemesidir, yayımlanmaz.

`support_motion.py`: 6 desteğin alt flans/profil/üst kapak girişleri 2 mm aralıkla toplam 918 konumda denetlendi; beklenmeyen katı kesişimi 0. Bu kontrol kaynak takımı, fikstür yükleri veya K'ye kurulum yollarını kapsamaz. Tam §5 yerine sayılmaz.

`bend_encode.py` / `updated_sheet_bending.py`: yeni 71 rafı ve kaynak tavanı koruyan 73 tavanı da eklendi, toplam 35 sac. Bütün kaynak köşeleri sınıflandı ve bitiş hatası sıfır. M8 delik ağının ideal silindirden yaklaşık 0,003 mm kiriş farkı kimlik eşlemesinde 0,01 mm kabul toleransıyla değerlendirilir; bitiş köşeleri değiştirilmez. Rafın havşa yüzeyleri malzeme içinden sonradan işlenmiştir: havşa imalat adımının ayrıca gösterilmesi hâlâ gereklidir. `source_bending_updated.json` çalışma önizlemesi verisidir, üretim/yayın onayı değildir. İlk bağlantı düzeltme checkpoint'i `40aa8780`; sonraki commit yeni iki sac eşlemesini ekler.
