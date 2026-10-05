# E v14 · özet (30 Eyl 2026 · Claude) — kutu_cad_v14 = v13 + kutu_ek_v14

Kemal (ekran görüntüsü, E kapak bölgesi): "bu neden kesik yarım ve oradaki yatay parça havada"

## Neden
- **Havadaki yatay parça = `agiz_ust_kirisi`** (15 × 20 çelik, x 21,5–808,5 · y 1162–1177 · z 29–49). v1'de "ön köşe plow'larını taşır" diye kondu; plow'lar hiç
  modellenmedi, v10'da 4 motorlu köşe katlayıcı geldi → taşıdığı parça yok. Yalnız iki ucundaki ön dikmelere (onyuz_dikme_sol/sag) değiyordu; montaj
  `ON_SEFFAF ^onyuz_` ile ön çerçeveyi de saydam ön kapak malzemesine aldığından kiriş görüntüleyicide havada duruyordu. Robot ağzının (y 886–1062)
  100 mm üstünde, ön panellerin 10 mm arkasında — ağız kenarı ya da panel tutucu değil.
- **Kesik dikme = sağ ön dikey kablo kanalı** (x 806–826 · z −50…−25): v10'dan önce kiriş z −40…−20'de kanalın içinden geçtiği için kanal y 1157–1177'de
  20 mm kesikti (alt + üst iki parça). v10 kirişi z 29–49'a aldı, kesik boş kaldı.

## Değişiklik
- `agiz_ust_kirisi` kalktı.
- `kablo_kanali_dikey_alt` + `kablo_kanali_dikey_ust` → tek `kablo_kanali_dikey` y 126–1827 (1701 mm, 2 m boydan [V]); tabana + 3 üst mesafe burcuna değer.
- Başka hiçbir parça ve hareket değişmedi.

## Denetim (kutu_v14_check.py baglanti · _local/e-v14/denetim.json)
- v13 ↔ v14 parça parça: çıkan tam 3, eklenen 1, kalan 432 parça ad/grup/malzeme/BOM/hacim/zarf AYNI.
- Kinematik: 461 an × 20 grup + blank_dunya BİREBİR; DONGU / DONGU_GERCEK / E_HAZIR_GERCEK / Z_CATAL(_GERCEK) aynı.
- Katılar geçerli · zaman ihlali 0 · kafa↔besleme en kısa 4,30 mm · tam tarama 128 an kesişim 0 · makine↔karton 0 · yeni kanal durağan çakışma 0.
- Bağlantı: 401 + asansör kayışı (v13 gibi) · GÖRSEL HAVADA (yalnız saydam ön yüze değen opak parça) 0 · yalnız saydam kabuğa değen 0.

## Açık
- E v13'ün açıkları aynen (FEFCO 0426 açınımı ~825 × 410 kararı Kemal'de, çift karton algılayıcı yeri, kafa enerji zinciri Isaac).
