# GÜNAYDIN KEMAL — HAT v3 GECE 2 RAPORU (4 Ekim 2026)

Her şey yerelde. İnternete yayın, push ve coord yok.

## MODELİ NEREDEN GÖRÜRSÜN

- Ana makine: http://127.0.0.1:8766/claude-hat3-v8/otonom/hat/makine_v3_8.html
- İstasyon montaj animasyonları (6 sayfa):
  - A: http://127.0.0.1:8766/claude-hat3-v8/otonom/hat/a-montaj.html
  - B: http://127.0.0.1:8766/claude-hat3-v8/otonom/hat/b-montaj.html
  - TOPPING: http://127.0.0.1:8766/claude-hat3-v8/otonom/hat/topping-montaj.html
  - F: http://127.0.0.1:8766/claude-hat3-v8/otonom/hat/f-montaj.html
  - E: http://127.0.0.1:8766/claude-hat3-v8/otonom/hat/e-montaj.html
  - U: http://127.0.0.1:8766/claude-hat3-v8/otonom/hat/u-montaj.html

Sunucu kapalıysa Claude'a "önizleme sunucusunu aç" demen yeter.

Model dosyası artık **192 MB yerine 76 MB**. Telefonda belirgin şekilde daha hızlı açılması gerekir. Sıkıştırma kayıpsız: parçalar, etiketler ve animasyonlar bayt bayt aynı.

## GECE NE YAPILDI (SIRAYLA)

1. **Ön yüz derzleri hizalandı** (commit 88acd9d). İki kademe farkı giderildi.
2. **Teyitler toplandı.** Fırın üstü sıcaklığı, cihaz güçleri, ana şalter ve müşteri paneli ölçüleri üretici belgelerinden okundu. Model bu adımda değişmedi.
3. **QR ve tezgâh düzenlendi** (5fc84f0). QR makinenin sağ ucuna hizalandı. Tezgâhın arka rafı kalktı ve tezgâh 180° döndürüldü. Hava hortumları kanala alındı. B çekmece kanal köşeleri düzeltildi.
4. **Kaşar ve sucuk kasetlerindeki iç çakışmalar giderildi** (b1de249).
5. **Bütün değişiklikler tek bir tarifte toplandı** (938daff). Model artık programla baştan, adım adım kurulabiliyor. Bu gece eski sürümden son sürüme kadar yeniden kuruldu ve her adım birebir aynı çıktı.
6. **Altı gövde üretim sacına çevrildi:** A, B, TOPPING, F, E, U (32dee8d, 22f9b53, c45c627, ac8aefc; modele işlenmesi 4a7d766). Gövdeler gerçek bükümlü sac, PEM ve vidayla kuruldu. Mutfakçı 3B'den üretebilir.
7. **Her istasyon için montaj animasyonu yapıldı** (bc2fec2, df4908b). Animasyon önce sac gövdeyi, sonra içindeki parçaları sırayla gösteriyor. Linkler yukarıda.
8. **Servis erişimi incelendi.** Her parçanın önden elle ulaşılıp ulaşılamayacağına bakıldı. Model bu adımda değişmedi.
9. **Bu sabahki son tur** (8d82d2f):
   - **Kompresör artık çıkarılabiliyor.** Fırın üstündeki üst kirişin sağ yarısı kaynak yerine 4 cıvatayla takılıyor. Dışarıdan görünüş aynı. Kompresör çıkış hortumuna spiral bir servis halkası, elektriğine fiş eklendi. Kompresör öne çekilince hortum uzuyor ve fiş önden ayrılıyor.
   - **Yağ tenekesi tek kişi değiştirilebiliyor.** Lansın iki hortumuna damlatmaz hızlı kaplin (CPC), seviye şalterine fiş (M12) eklendi.
   - **Acil stop butonları eklendi.** Modelde hiç yoktu, oysa standart (EN 60204-1) şart koşuyor. Altı adet Schneider XB4 kırmızı mantar butonu kondu: TOPPING, B, F, K, E ve QR'ın servis yüzü. A'nın elektriği olmadığı için A'ya konmadı.
   - **Gece kalan sac açıkları kapatıldı.** Boşta kalan 36 delikten 35'i kaldırıldı, 1 saplama başka yere taşındı. Gereksiz ray cıvatası kaldırıldı. B'deki perçin boşluğu düzeltildi.
   - **A istasyon kutusunu öne alma işi gerekmedi.** O kutu modelde artık yok, çünkü A'nın elektriği yok.
   - **Elektrik şeması güncellendi.** Akımlar belgelere göre düzeltildi: B 3,6 A, QR 6,4 A, sağ kol 10,1 A, sol kol 4,6 A. B soğutucusunun adı Secop NLE8.8CN olarak düzeltildi.

## DENETİM SONUÇLARI (SON MODEL)

Bütün model baştan tarandı.

- **Çakışma:** son turda eklenen hiçbir parça başka bir parçanın içine girmiyor.
- **Önceden var olan sorunlar:** bunlar düzeltilmedi, aşağıdaki "AÇIK KALANLAR" bölümünde.
- **Havada parça:** son turda yeni havada parça çıkmadı.
- **Dış kabuk:** makinenin dışına taşan yeni parça yok. Acil stop mantarları bilerek dışarıda.
- **A'nın içi:** boş, yalnız açıcı ve tabla geçişi var.
- **Etiketler:** hatasız. Her parça kendi istasyonuna ve grubuna bağlı.
- **Acil stop butonları:** kapakları açınca hiçbir yere çarpmıyor. B'deki buton QR'a çarpıyordu, 7 cm sola alındı.
- **Sayfalar:** ana makine sayfası ve 6 montaj sayfası açılıyor, hata yok.

Sayılarla:

- **Çakışma taraması:** model yaklaşık 10 000 parçadan oluşuyor. 1 068 çakışma bulundu: 904'ü bilerek yapılmış (vida somunun içinde, PEM sacın içinde gibi), 56'sı şüpheli, 108'i gerçek. Bu 108'in hepsi bu geceki son turdan önce de vardı, son tur yeni çakışma getirmedi. Taşınan saplamada yalnız 2 bilerek yapılmış çakışma eklendi.
- **Kapak süpürmesi:** butonlu kapaklar 0'dan 100°'ye kadar açılıp kontrol edildi. TOPPING, B, F, K ve E temiz. QR'ın servis kapağı yaklaşık 50°'de E kapağına çarpıyor, ama bu buton yüzünden değil (soru 11).
- **Tekrar kurulabilirlik:** model baştan iki kez kuruldu, iki sonuç bayt bayt aynı. Eski sürümden bu geceye kadar olan kısım da yeniden kurulup birebir aynı çıktı.

## KEMAL'E SORULAR

1. **(En önemli) Arka servis aralığı.** Makine duvara yaslı duruyor. 40'tan fazla servis parçasına yalnız arkadan ulaşılabiliyor: TOPPING'in arka bölmesi, fırının teknik bölmesi, B, K ve E panoları, soğutma grupları. Üç yol var:
   - (a) Makinenin arkasında en az 60 cm servis boşluğu bırakmak. Dükkân 60 cm derinleşir. Önerim en az TOPPING ve fırın arkasında bu.
   - (b) Hattı servis için duvardan öne çekmek. 5,2 m'lik bağlı hatta gerçekçi değil.
   - (c) Panoları istasyonların içinde ön kapağın arkasına taşımak. Uzun vadeli bir iş.
2. **Ana şalter kolu çok yüksek.** Kol 2,07–2,14 m'de, sınır 1,9 m. Model değiştirilmedi. Kolu fırın üst kapağına mı alalım, yoksa 1,7 m altına ayrı bir dış kol mu koyalım?
3. **Tezgâhın yönü.** Tezgâhı 180° çevirip 620 mm sola aldım, önü QR'a bakıyor. Senin istediğin bu muydu, yoksa 90° mi?
4. **Tezgâhın elektriği.** Bulaşık makinesi ve evye ısıtıcısını makinenin elektrik zincirine bağlamadım, binadan ayrı hat varsaydım. Onaylıyor musun?
5. **Fırın üstü sıcaklığı Sveba'ya sorulsun mu?** Fırının üst yüzünün gerçek sıcaklığı bilinmiyor. Hesap varsayımla yapıldı.
6. **Davlumbaz yağ filtresi.** Filtrenin her hafta yıkanması gerekiyor, ama önünde kompresör ve yağ tenekesi var. Kompresörü başka yere mi alalım, yoksa filtreyi davlumbazın sol yarısına mı?
7. **Fırının kırıntı tepsisi ve bandı.** Önden çıkarılamıyor. Sveba'ya önden servis kapağı sorulsun mu?
8. **Üst bölmenin havalandırması.** Fan ve filtreler arka sacta, değiştirilemiyor. Izgarayı üst kapak bandına ya da tavana alalım mı?
9. **QR göz motorları.** Motorlara ulaşmak için robot yüzündeki tek parça sacın ikiye bölünüp sökülebilir yapılması gerekiyor. Onay?
10. **Hava şartlandırıcılarının su kabı.** Kap her hafta boşaltılmalı ama derinde kalıyor. Otomatik tahliyeli tipe geçelim mi? Geçersek su nereye aksın?
11. **QR'ın üst servis kapağı en fazla 44° açılıyor.** 855 mm'lik tek kanat, makineyle QR arasındaki 59 cm'lik koridora sığmıyor ve E kapağına çarpıyor. Kapak iki kanatlı ya da katlanır yapılsın mı?
12. **B'deki acil stop.** B'nin önünde açılmayan bir yüzey yok, bu yüzden buton depo çekmecesinin önüne kondu. Çekmece açılınca buton da birlikte geliyor. Böyle kalsın mı, yoksa K kapağına ikinci bir buton mu koyalım?

## AÇIK KALANLAR (KISA)

- **Acil stop kabloları çizilmedi.** Kablo kapağın menteşe tarafından istasyonun iç kanalına gidecek. Modelde henüz yok.
- **Dönüş hattı kaplini kısa kaldı.** Dönüş hattındaki düz parça yalnız 23 mm. Modeldeki 21 mm'lik kaplinin gerçek ürün boyu teyit edilmeli. Gerekirse dirsekli kaplin kullanılır.
- **TOPPING'in içinde önceden var olan çakışmalar.** Bunlar iç yerleşim olduğu için dokunulmadı:
  - Piston çubukları evaporatör kasetinin duvarından geçiyor, duvarda delik yok.
  - Bakır borular kaset sacının içinden geçiyor.
  - Sürücü kartları üst üste binmiş.
- **QR'da kablo çakışması.** Göz ısıtıcı kabloları kanal içinde veri kablosuna 1,3 mm giriyor.
- **Havada 12 küçük grup.** Hepsi önceden vardı: kablo kanalı parçaları ve iki RevPi modülü, 1–10 mm boşlukla duruyor.
- **B'de 1 mm'lik yalıtım çizgisi.** İki ön sac arasındaki derzden ince bir yalıtım şeridi görünüyor.
- **Çözülmesi başka işlere bağlı vidalar:**
  - Boşalan bağlantılar: J1/J2/J3 üst burçları, şarjör astarı, pano ayakları, evaporatör ayakları.
  - TOPPING servis sacındaki 17 vida PEM somununun içine giriyor. Bu normal vida bağlantısı, sorun değil.
- **Parça kutusu listesinde eski kayıtlar.** 670 kayıt modelde artık olmayan ya da yer değiştirmiş parçalara ait. Liste yeniden üretilmeli. Görünüşü etkilemiyor.
- **Android AR riski.** Android'deki Scene Viewer sıkıştırılmış dosyayı açamayabilir. Tarayıcıdaki AR ve iPhone etkilenmez.

## GÖRÜNTÜLER

Klasör: `scratchpad\gece2\sabah\`

1. `1_makine_genel_acil_stop.jpg`: makinenin önü, acil stoplar görünüyor.
2. `2_firin_ustu_kayit_kompresor.jpg`: fırın üstü sağ bölme, kompresör ve teneke.
3. `3_kayit_sag_parca_civatalar.jpg`: bölünen üst kiriş, köşebent ve cıvatalar.
4. `4_yag_lansi_kaplin_M12.jpg`: lans, hızlı kaplinler ve M12 fiş.
5. `5_kompresor_spiral_fis.jpg`: spiral servis halkası, hat içi fiş ve kablo geçişi.
6. `6_acil_stop_K_E_QR.jpg`: K, E ve B acil stopları.
