# v27 / adım96
Kaynak: v26 yayınlanmış birleşik model. Makine, robot, ray, QR, tüm14klip ve9kablo geometri/matrisleri aynıdır. Yalnız aktif eski dükkân/floor-trench kökleri çıkarılır; yeni kompakt zemin ve standart gömme kanal yerleşimi eklenir.

Çalıştırma: `AUTOKITCH_NODE` kurulu Node; Shapely bulunan Python ile `run.py --repeat 2`. GLB girdi/çıktı desteklenir. Sonuç gzip web model, plan ve gerçek denetim JSON'larıdır. Ham169MB GLB commit dışıdır.

Kanal aile ölçüleri OBO OKA-G kataloglarına dayanır;200/300/400/500mm genişlik,100mm seçilen yükseklik. Geometri katalog ölçülerinden basitleştirilmiştir; OEM STEP modeli değildir. L/T yan açıklıkları gerçek, modüller üst üste geçmez. Alın derzi0.2mm; kapaklarY0; güç/data ayırıcı ve mevcut yuvarlak kablo dönüşleri korunur. Eş yükseklikte iki delik arasındaki yüzey üçgenleri T-düğümü bırakmadan bölünür.

Kaynaklar `floor_plan.json/sources`;81kapalı mesh,29.223kablo noktası,2mm yüzey payı kontrolü. Bu kanıt yeni kanal/kablo ilişkisi içindir; önceki tüm robot çarpışması ve kavraması değildir. Üretici nihai ürün/aksesuar seçimi, kapak yükü, döşeme ve elektrik proje onayı gerekir.
