# TOPPING / B yalıtım görüntüsü — 28 Eylül 2026

Kaynak: canlı v69 ile aynı GLB; değişiklik sadece görüntüleyicide.

## Neden ve düzeltme

- Eski dış kabuk filtresi üçgenleri parça zarfıyla tek tek siliyordu. İç içe geçen zarflar gerçek yalıtım yüzlerini de eksiltiyordu. Artık TOPPING ve B gövde PU ağları birebir korunuyor; diğer yüzeyler bağlı bileşen olarak tutuluyor veya gizleniyor. Bir parçanın ortasından yüzey silinmiyor.
- Raf köşebentleri, raf bükümleri, yarık dilleri, geçiş bloğu ve B bölmeleri kabuk grubuna alındı. Gizleme yüzünden oluşan yalancı boşluklar kaldırıldı.
- model3d_v21, TOPPING/B köpükte eski koyu arka-yüz boyamasını kullanmıyor. yalitim-kesit.js gerçek üçgen/düzlem kesişiminden düzlemsel dolgu üretiyor. Delikler çift/tek kesişim kuralıyla korunuyor. Açık konturu varsayımla kapatmıyor. Kesit kapanınca dolgu kayboluyor.
- Diğer malzemelerde eski kesit davranışı korunmuştur; bütün makineye üretim onayı verilmiş değildir.

## Kontrol sonuçları

- TOPPING PU: normalde 912 üçgen, dış kabukta 912. Açık kenar 0.
- B gövde PU: normalde 1284 üçgen, dış kabukta 1284. İlk taramada bulunan dört tekil kenarın iki ucu aynı 1 mikrometre koordinata düşüyor (sıfır uzunluk); gerçek açıklık kanıtı değil. Yerleri: x 2010 / 2517 mm, y 183,45–187,27 mm, z -698 / -637 mm. CAD değiştirilmedi.
- TOPPING kaynakta yan sandviç 1 + 57,5 + 1,5 = 60 mm; alt PU 39 mm. Alt uçlardaki 3 mm kesikler raf köşebendi içindir. Ön/arka yan sınırları üst yalıtımla aynı. Bunlar kaynak ve parça zarfları üzerinden kontrol edildi; yeniden tam CAD kesişim hesabı çalıştırılmadı.
- Gerçek v69 ile 721 ağdan 115 kabuk ağı; motor/kart/robot/ürün gizli. Dört aç/kapa çevriminde geometri/görünürlük tam geri döndü.
- X/Y/Z düzlemleri yalıtım içinden geçirilerek gerçek dolgu üretildi; kapatma sonrası dolgu sızıntısı ve JS hatası yok. Ön görünüşten kesit ekranı incelendi.
- Matematik testi: dolu kare, delikli kare, delik içinde ada, ayrık katılar ve açık kontur. Alanlar doğru, delik doldurulmadı.

Yerel önizleme: http://127.0.0.1:8778/hat/makine.html
Bu görevde yayın yapılmadı. Eski model3d.js ve GLB dosyaları değiştirilmedi.
