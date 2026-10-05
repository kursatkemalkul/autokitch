# ADIM 3 · ÜRETEÇ NOTU — kaşar + sucuk kaseti iç çakışmaları (adım 4 taşıyacak)

GLB zinciri: `hat3_v8zp` → `a1_kaset.py` → `a1.glb` → `tg/glb_sikistir.py` = `hat3_v8zq.glb`.
Hazır yama dosyaları (eskilerin ÜSTÜNE YAZILMADI, yeni sürüm numarası): `uretec_yama/`
- `kaset_birlesim_v2.py` (v1'in kopyası + 2 değişiklik)
- `kasar_cad_v15.py` (v14 + 1 değişiklik + birleşim v2)
- `sucuk_cad_v9.py` (v8 + 1 değişiklik + birleşim v2)
- `kaset_kontrol_adim3.py` (kaset_kontrol.py maddeleri aynen, KASET listesi: kaşar v15 · kıyma v5 · kuşbaşı v4 · sucuk v9)
Üretici betik: `yama_uret.py <_uretec klasörü>` → üç dosyayı v1 / v14 / v8'den yeniden üretir (assert'li metin değişimi).

**Sürüm numarası:** görevde önerilen "kaşar v11 / sucuk v4" bu adlar ZATEN VAR (kasar_cad_v11.py, sucuk_cad_v4.py eski sürümler) ve modeldeki
kasetler kaşar **v14** / sucuk **v8**. Bu yüzden yeni sürüm **kasar_cad_v15** ve **sucuk_cad_v9** (ortak birleşim kodu **kaset_birlesim_v2**).

## 1 · KAŞAR (kasar_cad_v15) — gerçek katı çakışması
- **Bulgu:** çıkış borusu (eksen z 212,5 yerel · dış r 25) ön dış yüzü z 237,5; yatak kapağının bayonet dudağı z 236'dan başlıyor →
  kapak boruya 1,5 mm giriyordu (montaj: x 2088,5 · y 1165 · z −125; üretecin KENDİ taraması da v14'te `cikis_tupu × yatak_kapagi 62,4 mm³` yazıyordu).
- **Düzeltme:** yatak kapağının arka alın yüzü z 236 → **238** (bayonet dudağı 4,3 → 2,3 mm; boru ile 0,5 mm boşluk).
  Değişmeyen: boru ekseni / çapı (düşme deliği x'i), tüp boyu, 3 tırnak, cep / halka / tümsek / dayama kotları (240,3–245), O-ring kanalı, kapağın ön yüzü (266),
  kasetin dış ölçüsü, raydaki yeri, mandal. Kapak hacmi 28 599 → 27 552 mm³. Neden kesik / delik değil: kapak kilitlenirken 35° döner; boru için kesik
  35° + boru genişliği kadar geniş olmalı ve 210° tırnağının dudak desteğini keserdi. Dudak 2,3 mm POM, yük yalnız O-ring yayı.
- Yama: `kaset_birlesim_v1.yatak_kapagi(RT, CY, TUP_Z1)` → v2 `yatak_kapagi(RT, CY, TUP_Z1, z_arka=236.0)` (varsayılan v1 ile AYNI, diğer kasetler değişmez;
  `assert z_arka <= Z_HALKA - 2`) · kasar_cad_v15: `KAPAK_Z_ARKA = 238.0`, `BR.yatak_kapagi(RT, CY, TUP_Z1, z_arka=KAPAK_Z_ARKA)`.
- Sonuç (üretecin kendi denetimi): KATI geçerli · ÇAKIŞMA TARAMASI **TEMİZ** · 4 açıda döndürme temiz · kapak ∩ tüp 0 (tırnak cebe oturur, mesafe 0).

## 2 · SUCUK (sucuk_cad_v9) — gerçek katı çakışması (yeni bulundu)
- **Bulgu:** çıkış borusunun koni geçişi (eksen z 210, y 60'ta r 39) tüpün ön ucunu (z 246,5) 2,5 mm aşıyordu (z 249'a kadar) → tüp ucunun önünde
  ince "gaga": ön muylu ∩ tüp **16 mm³** (her dönüş açısında), yatak kapağı ∩ tüp **2,5 mm³**. Üretecin kendi taraması v8'de "2 BULGU" yazıyordu.
  (Aynı koni kodu kıyma / kuşbaşı üreteçlerinde de var — o kasetler modelde UNO olduğu için bu adımda dokunulmadı; aynı satır oralara da eklenmeli.)
- **Düzeltme:** `boru = boru.intersect(kut(-RD - 20, RD + 20, BORU_ALT - 1, CY, ZF, TUP_Z1))` (koni yalnız tüp boyunca). Tüp hacmi −18,8 mm³,
  ürün kanalı / boru içi / ağız ekseni değişmedi.
- Sonuç: KATI geçerli · ÇAKIŞMA TARAMASI **TEMİZ** (v8: 2 bulgu) · helezon ve karıştırıcı 4 açıda temiz.

## 3 · İKİ KASET — web / montaj ağı (kiriş sarkması = sahte ama GLB'de gerçek görünen çakışmalar)
- **Bulgu:** `ag(tol 0,12, aci 0,35)` kaba ağında r 39'luk deliğin kirişi 0,6 mm içeri sarkıyor; geçme boşlukları 0,2–0,3 mm → montaj GLB'sinde
  sucuk kapak ↔ tüp 0,92, gövde ↔ plaka kanalı / ön conta 0,22, (ince ağa geçince görünen) kapak ↔ O-ring 0,33. Sucuk tüp ağı ayrıca AÇIKtı (denetimde içi sorulamıyordu).
- **Düzeltme:** birleşim v2 `web_ag`: `INCE = (govde, plaka_on, plaka_arka, conta_on, conta_arka, cikis_tupu, yatak_kapagi, oring_tup, oring_kapak)` →
  `ag(kopya, 0.02, 0.1)`; INCE, KABA'dan ÖNCE sorulur (O-ringler eskiden KABA 0,4 / 0,8 idi). Katılar değişmez, yalnız ağ.
- Montaj tarafı (topping_uno_cad / montaj üreteci kasetleri nereden alıyorsa): kaşar v15 + sucuk v9'dan al, bu 9 parçayı ince ağla yaz.
- GLB etkisi: +55 bin üçgen, +4,6 MB (117,4 → 122,1 MB).

## 4 · TOPPING tarafı (topping_uno_cad v19 → bir sonraki sürüm) — yarık dili + raf kaset contası (yer / ölçü DEĞİŞMEDİ)
- **Bulgu:** `kasar_cad_v14_yarik_dili` ↔ kaşar tüp 0,14 · `sucuk_cad_v8_yarik_dili` ↔ sucuk tüp 0,34 · `raf_kaset_contasi_sucuk` ↔ tüp 0,16.
  Tasarımda dil / conta tüple TEMAS 0 (CAD'de `cut(_tup)`); kaba ağda delik kirişleri boruya sarkıyor; raf kaset contaları 60 üçgenlik kaba çokgen
  (iç kenarı çemberde bile değil), kaşar dilinin deliği r 25,05 (tüp r 25).
- **GLB'de yapılan:** dil deliği köşeleri boru ekseninde boru dış r'sine göre kirişler çembere TEĞET olacak şekilde dışa (en çok 0,49 / 0,47 mm,
  çapraz kenarlar dahil); iki raf kaset contası topping_uno_cad'deki tanımla aynı katı (Ø60 raf deliği, merkez z −150 ∩ arka yarı − tüp r) CadQuery ile ince ağ.
- **Üretece:** `_dil` ve `raf_kaset_contasi_*` web ağını ince (0,02 / 0,1) yaz; tüp kesitini `_kesit()` (tessellate'li kutu) yerine kasetin üreteç sabitlerinden al
  (kaşar: eksen x kaset ortası, z BZ 212,5 → dünya −150, r 25; sucuk: z 210 → dünya −152,5, r 24) — kaşarda ölçülen r 25,05 bu yüzden.

## 5 · parca_kutulari.json (sayfa parça adları)
- TOPPING_MODUL içindeki kaşar / sucuk kaseti + yuva + iniş + kulak + conta + dil kutuları v8zc "TOPPING cep geri"den beri eski yerdeydi
  (+26,5 / +49,5 x kaymış). 186 kutu modeldeki yerine alındı (eşleşen kutu 23 → 193). `yuva_*_mandal_*` kutuları başka yerde, eşleşmiyor → DOKUNULMADI (adım 4).
  Adlar eski (`kasar_cad_v14__…`, `sucuk_cad_v8__…`) bırakıldı; adım 4 montajı v15 / v9 ile kurunca adlar da değişir.

## 6 · Bu adımda düzeltilmeyen (kapsam dışı, eski)
- Kaset önden çekme süpürmesinde ÖNCEDEN DE olan girişler (v8zp = v8zq, birebir aynı): alt yalıtım PU (dz 0–134, 5 141 mm³), raf ön büküm (dz 2–138, 19 mm³),
  ön paslanmaz dil parçası (dz 4–152, 95 mm³), soğuk çerçeve sacı (dz 20–154, 6 mm³), kaşarda flipper kılavuzu (dz 176–562, 4 926 mm³), mandal dili (beklenen: basılır).
  Bunlar yuva / ön çerçeve tarafı (TOPPING yerleşimi — bu adımda yasak).
- `TOPPING_DONER__HELEZON_KASAR[10]` açık ağ (dönen helezon parçası) · TOPPING harç tarafında `celik[128]` ↔ `paslanmaz[17]` 2,39 mm (x 2259, kaset değil).
