# K montaj – TOPPING v6 uyarlaması

Kaynak: yerel `k73.glb.gz` (adım61 + yerel70–73). Ortak zincire henüz geçirilmedi. Bu çalışma yayın/üretim onayı değildir.

Mevcut `t5`/F betikleri uyarlandı; `_altyapi.py`, üçgen yol denetimi ve ortak oynatıcı korunur. Model mm/dünya koordinatları; oynatıcı çıktısı m.

1. Gzip girdiyi bu klasöre `k73.glb` olarak aç.
2. `k_cikar.py k73.glb k_bil.pkl`: modeli yalnız değiştiğinde okur; kaynak boyutu/zamanı önbellek JSON'unda.
3. `k_kayit.py`: yerel71–73 CAD kayıtları. `k_parca.py`: en küçük kayıt kutusu/üçgen eşleştirmesi. Eski CAD adları yalnız <0,01 mm ve tekil kutu eşleşmesinde geçici etiketlenir; yüzey eşitliği iddia edilmez.
4. `k_montaj.py`: önce yalnız tam sıra. `plan_audit.json` PLAN SORUNU listesini verir. Sıfır olmadan çıktı yayınlanmaz.
5. Sıra temizlenince açınım/PEM/bağlantı aşaması eklenir, `baglanti_denetim.py` ve tam `k_cikti.py` çalıştırılır; `--hizli` yayın doğrulaması sayılmaz.

Pkl/raw GLB/cache dosyaları geçicidir. Büyük model her sıra turunda tekrar okunmaz. Ortak `ist_montaj/montaj-oynatici.js` değiştirilmez.
