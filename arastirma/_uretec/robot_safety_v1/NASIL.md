# Robot / QR adım62 — inceleme yerleşimi

Kaynak: Claude adım61 `hat3_v10c`, SHA256948b20c4520cf917711a8dea730ea037379793b11bb6e975c649155c83ef9c1d. Makinenin QR dışındaki düğümleri ve özgün geometri tamponu değiştirilmez. Bu dosyalar üretim serbest bırakması veya güvenlik sertifikası değildir.

QR:3 sütun ×4 satır. Raf üstleri588/850/1112/1374mm; göz açıklığı250mm. Sütun içleri x3769/4256/4743mm, her biri475mm. Robot yüzü z1750mm, müşteri yüzü z2074mm. Kilitler/kablolar müşteri yüzünün dışında. Teknik üst bölme1653–2050mm. Robot kontrol kutusu rezervi alt bölmede. CAD mm, glTF metre, Y yukarı. UR10e kısa turkuaz uç değişmeden, özgün eklem FK'siyle aktarılır.

Taşınanlar: eski pano/DIN/cihaz kümeleri, UPS, kilit kartı/güç kaynağı/modem kümesi, ekran/okuyucu ve robot kontrol kutusu rezervi. Ölçekleme yok; yalnız katı öteleme. Eski motorlu raflar aktarılmaz: onaylanan düzende raflar sabittir. Eski fanların150×150×40mm zarfı kullanılır. Kemal kararı: QR dolabında ısıtıcı yoktur; eski ısıtıcılar aktarılmadı.

12 müşteri kapısında ve hücre girişinde Schmersal AZM40Z-I1-ST-1P2P-PH (kilit izlemeli Z tipi) / AZM40-B1-PH zarfı. Ölçü ve delikler üretici AZM40 el kitabı§3.3: gövde119.5×40×20mm, gövde bağlantı adımı100mm, aktüatör24.5mm. M5 geçişØ5.5, nut servis cebiØ9. Üretici M5 için paslanmaz dayanım sınıfı80 ister: bu bağlantılarda A2-80; genel A2-70 kuralının cihaz el kitabı gereği istisnası. [Üretici el kitabı](https://products.schmersal.com/upload/orig/10/00/55/87/DOC_MAN_MEC_mrl-azm40_SEN_AIN_V3.pdf).

Hücre kapısı personelin robot koridoruna girdiği kapıdır; makine servis kapağı değildir. Kapı x5600mm'de sağ koridor kenarında yerleşim önerisi olarak bulunur. Kilitli kapının içeriden kaçış açması, zemin ankrajları, sabit çevre muhafazası ve duruş mesafesi tamamlanmadan fiziksel hücre tamamlanmış sayılmaz.

Referans yazılım `otonom/hat/robot-safety-v1/interlock.mjs`: gerçek iki kanallı kapalı/kilitli geri bildirimi olmadan hareket izni vermez. Robot gözdeyken kapı kilitli kalır; kapı açılması/kilit kaybı duruş ister. Ortak açık arka alan nedeniyle müşteri erişiminde tüm robot/ray durur. Güvenli duruş + göz boşluğu doğrulandıktan sonra açılabilir; reset sonrasında ayrı başlatma gerekir. Bu JS gerçek emniyet PLC'si değildir. Ortak güvenlik şeması kullanıcı kararı gereği sonraki iştir.

Üretim açıkları: müşteri menteşe/kol/stop katalog seçimi; servis kapağı vidaları, fan montaj ve havalandırma delikleri; hücre kapısı kaçış açması/ankraj/sabit koruma; gerçek güvenlik devresi/PL/duruş zamanı ve güvenli göz-boş ölçümü; standart metnindeki FR5 ile kullanıcının seçtiği UR10e'nin eşleştirilmesi. Montaj animasyonu hazırlanmadı. Mevcut makine animasyonları QR dışındaki kanallarıyla korunur; robot yalnız yerleşim pozunda gösterilir.

Çalıştırma (CadQuery/numpy ve Node>=20 kurulu ortam):
```
python build.py hat3_v10c.glb layout.glb
node add_robot.mjs layout.glb hat3_v10d.glb
python mechanical_audit.py
node reach_audit.mjs layout.glb
node audit.mjs
```
Denetimler sonucun yanındaki JSON'lara kaydedilir. Erişim testi bütün kayıtlı QR giriş/çekilme pozlarını kontrol eder; makineden alma rotalarını veya sürekli fiziksel güvenliği doğruladığını iddia etmez.
