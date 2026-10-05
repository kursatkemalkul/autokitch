# K montaj – TOPPING v6 uyarlaması

Kaynak: kayıtlı adım 73 çıktısı `../chain73/hat3_v10n.glb.gz` (main adım 66 + K 70–73). `repeat_audit.json` iki bağımsız koşunun GLB ve ent JSON byte eşitliğini kaydeder. F 67–69 birleşince K zinciri yeni girdide yeniden koşulmalıdır. Üretim/yayın onayı yoktur.

Mevcut t5/F betikleri uyarlandı; `_altyapi.py` ve ortak oynatıcı değiştirilmedi. Model mm/dünya; oynatıcı m.

1. Kaynak gzip'i aç; `k_cikar.py <model.glb> k_bil.pkl` yalnız girdi değiştiğinde büyük modeli okur.
2. `k_kayit.py` K 71–73 ad/kutu kayıtlarını çıkarır. `k_native_names.py` mevcut K adapterinden mekanizma adlarını okur; vendor güç kaynağı STEP'i yalnız bu metadata işleminde kullanılır, model geometrisinin yerine geçirilmez.
3. `k_parca.py` her üçgeni en küçük kaynak kutusuna eşler. Geçici eski CAD adları tekil aynı-düğüm kutusu ≤0.6 mm toleransında eşlenir; yüzey eşitliği iddia edilmez. Güncel pullar merkez/eksen/kalınlıkla eşlenir, dış çapları değiştirilmez. `part_audit.json` tüm üçgenlerin korunmasını doğrular.
4. `k_montaj.py` sıra ve kesintisiz yol denetimini yapar; `plan_audit.json` PLAN SORUNU listesini yazar. Saplama/somun eksenleri gerçek baş geometrisinden; diğer girişler kaynak CAD kayıtlarından gelir. Yalnız adları belirtilen gerçek diş/pres eşleri yazılı gerekçeyle hariçtir. Hortum/kayış kurala göre kendi yolu boyunca uzar.
5. `k_nut_probe.py` somun yollarını diğer tüm son-konum parçalarına karşı kısa test eder; bütün montajın onayı değildir.
6. PLAN SORUNU sıfır olmadan açınım/büküm üretim doğrulaması ve yayın yok. Sonra bağlantı denetimi, tam `k_cikti.py`, tarayıcı kare kontrolü ve Kemal onayı gerekir. `--hizli` yayın denetimi sayılmaz.

Pkl/raw GLB/numba cache ara dosyalardır; commit edilmez. Sitede kullanılan çıktılar `_local` altında olmayacaktır. Ortak `ist_montaj/montaj-oynatici.js` değiştirilmez.
