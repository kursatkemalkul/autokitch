# Fırın → B yük yolu + B ağırlık zarfı · hesap v1 (29 Eylül 2026)

Codex Modüler v1'in 7 kiriş hesabında olmayan iki konu hesaplandı. Model değişmedi.

- Üreteç: `arastirma/_uretec/firin_b_yuk_hesap_v1.py`
- Sonuç: `firin_b_yuk_hesap_v1.json`

## 1 · Fırının B'ye yükü

Fırın, B içindeki taşıyıcı çerçeveye oturuyor. Çerçeve 40×40×2 kirişler (ön z −110, arka z −620) ve x 2517,5 / 3172,5 / 3792,5'teki 30×30×2 dikmelerden oluşuyor. Sağ uçta 204 mm konsol var.

Eski hesap (store_cad_v9) yalnız fırın 200 + raf yükü 99 kg'ı alıyordu. Üst kabinin 110,8 kg'ı hesapta yoktu: davlumbaz, sac kabuk, kapaklar, kompresör tavası ve küçük parçalar. Kullanımda F'nin toplamı **409,8 kg**.

Yöntem: sürekli kiriş, sonlu eleman, 2,5 mm adım. Yük katsayısı 1,5 ve izin verilen gerilme 205/1,5 = 137 MPa (store_cad_v9 ile aynı ölçüt). Üst kabin iki uçtaki yan duvarlardan iner. Kompresör kendi 4 ayağının hizasına konmuştur.

| Parça | Gerilme | Sehim | Sonuç |
|---|---:|---:|---|
| Ön kiriş | 26,8 / 137 MPa | açıklık 0,22 mm · konsol 0,23 mm | geçti |
| Arka kiriş | 37,8 / 137 MPa | açıklık 0,15 mm · konsol 0,44 mm | geçti |
| Dikme 30×30×2 | 6,2 MPa | burkulma güvenliği 104 | geçti |

Ayak başına hizmet yükü en çok 174 kg (1,7 kN). Değer, x 3172,5'teki ön ayak için: fırından gelen yük + B'nin 1000 kg zarfından düşen pay. Elesa LV.A-SST M12'nin taşıma yükü katalogdan teyit edilecek.

## 2 · B'nin boş taşıma ağırlığı

- Codex'in CAD'den hesapladığı bilinen kütle: 843 kg.
- Bilinmeyen malzemeli parçalar: GLB ağ hacmi × yoğunluk aralığı (VARSAYIM). Kalemler: motor, kart, PLC, koyu, plastik, bakır, kablo kanalı, silikon tepsi, conta.
- Secop NLE8.8CN kompresör: üretici föyüne göre 10,9 kg.
- Evaporatör lamelleri CAD'de dolu blok sayılmış (51,3 kg). Gerçeği yaklaşık 8–18 kg.

**Tahmin: 892–968 kg.** Codex'in 1000 kg zarfı tutuyor, pay dar.

- 1000 mm destek aralığıyla B en fazla 1051 kg olabilir.
- Üst uç tahminde (968 kg) gerilme 129 / 140 MPa.
- Kullanımda buna gıda eklenir: hamur ≈137 kg, içecek ≈56 kg.

**Açık:**
- B'yi tartmak.
- Ayak kataloğu.
- Fırın 200 kg VARSAYIM (katalog TP10 160 kg). Özel sipariş föyü gelince yeniden koşulacak.
