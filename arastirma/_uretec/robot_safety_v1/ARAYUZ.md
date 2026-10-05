# Robot / QR emniyeti v1 — işlev taslağı

Taban: origin/main a5133e2. KURALLAR.md, KOORDINASYON.md ve STANDART_DURUM.md okundu.
Kapsam: hücre kapısı ve 12 QR müşteri kapısının robot erişimiyle kilitlenmesi.
Makine, zincir, acil stop ve makine kapakları değiştirilmedi. Devre şeması hazırlanmadı.

## Teslim edilen

`otonom/hat/robot-safety-v1/interlock.mjs`: platformdan bağımsız işlev referansı.
`adapter.mjs`: web/Isaac hareket yürütücüsüne bağlanacak izin/son karede bekletme arayüzü.
Mevcut oynatıcıya takılmadı; GLB animasyonu veya tarayıcıdaki duraklama emniyet devresi değildir.
Referans kod gerçek robotun emniyet girişlerini sürmek üzere sertifikalı değildir.

1. İlk açılışta hareket yok. İki kanallı kapı/harici izin, 12 kapının kapalı-kilitli durumu,
   doğrulanmış duruş ve boş hücre kontrolünden sonra ayrı reset ve başlat gerekir.
2. Hücre kapısı açılır, kanal uyuşmaz, kilit kaybolur veya veri eskirse duruş talebi tutulur.
   Kapı kapatmak yeniden başlatmaz. Reset hareket başlatmaz.
3. QR gözü robot için ayrılır; iki kanallı gerçek kapalı VE kilitli geri bildirim gelmeden giriş izni yoktur.
   Yazılımın kilit komutu, kilidin tuttuğunun kanıtı değildir.
4. Robotun gözde olduğu ve çıkışının doğrulandığı ayrı izlenir. Çıkış komutu tek başına kilidi çözmez.
5. Müşteri erişim isteği robotu önce durdurur. Robotun güvenli duruşu VE tüm QR alanından çıkışı
   doğrulanmadan müşteri kilidi çözülmez. Kapanma ve yeniden kilitlenme sonrası reset/başlat gerekir.
6. Mevcut QR arkadan açık: müşteri bir gözdeyken başka göze geçişin güvenli olduğu kanıtlanmadı.
   Bu nedenle v1'de herhangi bir müşteri kapısı açıkken bütün robot hareketleri engellenir.
   Eşzamanlı teslim ve robot hareketi için erişim mesafeleri/bölge ayrımı ayrıca doğrulanmalıdır.
7. Hücre içine kişi girdiyse kapının yeniden kapanması yeterli değildir. Hücre boşluğunu doğrulayan
   prosedür/koruyucu çözüm olmadan `cellOccupied=false` üretilemez; bu mevcut durumda açık tasarım konusudur.

## Donanım arayüzü — pin şeması değil

Girişler bağımsız, uygun güvenlik donanımından alınır. Normal PLC biti, web mesajı,
animasyon zamanı veya tek reed kontağı güvenli konum/duruş kanıtı sayılmaz.
Seçilecek röle/PLC'nin kanal teşhisi, kablo kısa devre teşhisi ve yanıt süresi ayrıca hesaplanır.

| Sinyal | İşlev |
|---|---|
| cellDoorClosed A/B | Hücre kapısının emniyet anahtarı; kapı açıkken izin düşer |
| QR01…QR12 closed A/B | Müşteri kapısının emniyetli kapalı durumu |
| QR01…QR12 locked A/B | Kilitleme mekanizmasının emniyetli tutulma durumu |
| standstill A/B | Robot VE rayın doğrulanmış duruşu |
| zoneClear[12] A/B | El/parmak dahil robotun ilgili gözden tamamen çıktığının güvenli bilgisi |
| externalPermit A/B | Claude'un ortak acil stop/makine emniyet devresinden izin; yerel bypass yok |
| safetyHealthy | Ortak güvenlik sisteminin teşhis durumu |
| cellOccupied | Hücrede insan var / bilinmiyor ise başlatma yok |
| robotMotionPermit / safeguardStopDemand | Ortak güvenlik devresine işlevsel talep; gerçek robot ve ray aynı anda durdurulur |
| lockCommands[12] | Kilit tutma talebi; geri bildirimden ayrı |

100 ms kod watchdog'u yalnız benzetim varsayımıdır; fiziksel güvenlik yanıt süresi veya durma
mesafesi olarak kullanılamaz. Duruş kategorisi, PLr, toplam yanıt süresi ve ray çıkışı ortak devrede belirlenir.
Reset hücre dışında, tehlikeli alan görülebilen yerden; başlatma ayrı ve kasıtlı olmalıdır.

## Fiziksel modelde henüz yapılmayanlar

- Hücre kapısının güncel koordinatları ve gerçek anahtar/aktüatör montaj delikleri doğrulanmadı.
- QR'nin mevcut normal elektrikli kilitlerinin emniyet derecesi bilinmiyor. Yardımcı bir kontak eklemek
  onları emniyet kilidine dönüştürmez; kapalı ve kilitleme durumunu emniyetli izleyen ürün gerekir.
- Ürün seçilmeden braket, delik, vida, kablo klipsi ve sökme erişimi kesin ölçüde çizilmedi.
- Katalog örneği: Schmersal AZM40Z izlenen kilitleme ailesi; bu bir satın alma/uygunluk kararı değildir.
  Modelde yer ihtimali 119,5 × 40 × 20 mm gövdeye ilaveten aktüatör, bağlantı ve servis boşluğu içerir.
- KURALLAR §5 mekanik çakışma/bağlantı/vida denetimleri bu teslimde uygulanamaz: geometri değişmedi.
  Fiziksel montaj ve devre doğrulanmış/üretime hazır olarak işaretlenmez.
- STANDART_DURUM robotu FR5, mevcut Codex rig'i UR10e olarak anıyor. Üreticiye özgü pinler seçilmedi;
  nihai robot doğrulanınca doğru güvenlik kılavuzu kullanılacak.

## Doğrulama ve devam

`node --test arastirma/_uretec/robot_safety_v1/interlock.test.mjs`.
12 gözü tek tek sınayan işlev testleri; fiziksel güvenlik doğrulaması değildir.
`node arastirma/_uretec/robot_safety_v1/audit.mjs` JSON denetim sonucunu üretir.
Sonraki ortak iş: gerçek anahtar/kilit seçimi, yerleşim + bağlantılar, güvenlik devresi/PL hesabı,
robot ve ray durma ölçümü, sıkışma ve kaçış erişimi, bütün arayüzlerin donanımda doğrulanması.
Müşteri QR açma komutu emniyet kararını atlayamaz. Güç kesilmesinde kilidin mekanik davranışı
ve hücre içinden kaçış seçilecek ürün/prosedürle çözülmelidir.

## Üretici kaynakları

- UR10e güvenlik girişleri ve ayrı safeguard reset:
  https://www.universal-robots.com/manuals/EN/PDF/SW5_25_1/user-manual-UR10e-PDF_online/711-039-00_UR10e_User_Manual_en_Global.pdf
- AZM40 montaj/donanım ve kilitleme izleme koşulları:
  https://products.schmersal.com/upload/orig/10/00/55/87/DOC_MAN_MEC_mrl-azm40_SEN_AIN_V3.pdf
- Gövde ölçüsü:
  https://www.schmersal.com/en/azm40
