# ADIM 5b · E ve U üretim sacı — ANA GLB'YE ENTEGRASYON NOTU (4 Eki 2026 gece · Claude)

Üreteçler (worktree, commit'li): `arastirma/_uretec/h3/h3_e_sac_v1.py` · `arastirma/_uretec/h3/h3_u_sac_v1.py`
Çıktılar (bu klasör): `E_sac_v1.glb`, `U_sac_v1.glb` (parça başına düğüm, dünya koordinatı, extras: bom + sac açınım özeti + meta) ·
`E_parca.csv`, `U_parca.csv` (`;` ayraçlı, UTF-8 BOM) · `acinim_E/*.json`, `acinim_U/*.json` (her sacın açınımı: dış kontur, delikler, büküm çizgileri, R, K, BA) ·
`E_denetim.json`, `U_denetim.json` + `*_denetim_log.txt` · görüntüler `E_*.jpg`, `U_*.jpg`.
Çalıştırma: `python run_5b.py E` / `python run_5b.py U` (ADIM5 + AUTOKITCH_SAC_STANDART ortam değişkenlerini run_5b kurar; üreteçler ana depoya/GLB'ye YAZMAZ).
Montaja bağlama fonksiyonları hazır: `h3_e_sac_v1.uygula(MOD_PARCALAR)` · `h3_u_sac_v1.uygula(MOD_PARCALAR, birim, g)` (GO.uygula: eski adları çıkarır, yenileri ekler, idempotent, önek denetimli).

## 1 · Ana GLB'de NEYİN YERİNE KONACAĞI

| Ana GLB (hat3_v8zq) | Yerine | Not |
|---|---|---|
| `E_GOVDE__kabuk` (sol/sağ/arka/üst kabuk) | E_sac: `sol_sac_pizza_penceresi`, `sag_sac`, `arka_sac`, `ust_sac` (+ `*_kose_kaynagi_*`) | ad korunur (elektrik hedefi `KC/ust_sac` aynı adla) |
| `E_GOVDE__sac` (taban, ön kasa, kayıtlar, şarjör kapısı) | `taban_sac_3`, `onyuz_dikme_{sol,sag,orta}` (+`_tapa`), `onyuz_kayit_788_{sol,sag}`, `sarjor_yan_kapisi` + `_ic_tava` + lamalar, `govde_kulak_*`, `govde_kosebent_*`, kaynaklar | |
| `E_GOVDE__celik` (ayaklar, menteşe gövdeleri, kapı menteşeleri) | `ayak_0…5` (+`_kontra`) GN 20 sınıfı M12 Ø40, `onyuz_kapak_E_mentese_*_sabit` (+vida), `sarjor_yan_kapisi_mentese_*`, bağlantı elemanları | ayak konumları aynı |
| `E_GOVDE__plastik` (bas-açlar) | `onyuz_kapak_E_basac_*`, `sarjor_yan_kapisi_basac` | x 451/472 → 452/471 (±1 mm, Ø12,2 orta dikmenin düz yüzüne sığsın) |
| `E_GOVDE__on_seffaf` (4 kapak + kanatlar) — kpk | `onyuz_kapak_E_{alt,ust}_{sol,sag}` + `_ic_tava` + `_robot_agzi_kasa_*` + `_karsilik_*` + `*_mentese_*_kanat` | kapakla dönenler: `g.kapakla_doner(ad)` → kpk etiketi |
| `E_MODULER__paslanmaz` (kaide) | `kaide_e_ray_{on,arka}` (+tapalar), `kaide_e_kayit_{sol,orta,sag}`, `kaide_e_*_somun*`, `kaide_e_vida_*` | aynı 60×60×3 / 40×60×3 ölçü, kaynaklı çerçeve |
| `U_F_GOVDE__sac` + `__paslanmaz` | U_sac (U_F_GOVDE): `ust_f_taban_sac`, `ust_f_yan_{sol,sag}`, `ust_f_tavan_sac`, `ust_f_arka_sac`, `ust_f_tavan_omegasi_0`, `ust_f_giris_cebi`, `govde_f_*` | `U_F_GOVDE__on_seffaf` (F kapağı bas-açları) KALIR |
| `U_KE_GOVDE__sac` + `__paslanmaz` | U_sac (U_KE_GOVDE): `ust_ke_*`, `govde_ke_*` | |
| `F_UST_KABIN__sac`, `__yalitim`, `__paslanmaz`in profilleri (3 alt profil, ön üst kayıt, ön orta dikme + tavan kirişi) | U_sac (F_UST_KABIN): `f_ust_yan_{sol,sag}`, `f_ust_tavan_sac`, `f_ust_arka_sac`, `f_ust_panjur_lameli_*`, `f_ust_alt_profil_*`, `onyuz_f_ust_ust_kayit`, `onyuz_f_ust_dikme_0`, `f_ust_tavan_kirisi`, `f_ust_taban_levhasi`, `f_ust_taban_yalitim_kilifi_*`, `f_ust_taban_yalitimi_*`, `f_ust_taban_rakor_kovani`, `f_ust_taban_v2_kovani`, `govde_fu_*` | `F_UST_KABIN__paslanmaz`in hava hortumu kelepçe + askı lamaları (6 + 6 küçük bileşen) KALIR; `__plastik` (rakorlar) ve `__on_seffaf` (gazlı yay braketleri) KALIR |
| `F_DAVLUMBAZ__sac` içindeki bölme duvarı bileşeni (x 2501,5–3998,5 · z −441,5…−440) | `f_davlumbaz_bolme_duvari` (F_UST_KABIN) | atış kanalı + fan + filtre KALIR |
| `ELK_ZINCIR__paslanmaz` içindeki gömme cep (4 duvar + cep tabanı, x 3926,5–3983 · y 2081,5–2166,5 · z −830…−790) | `ust_f_giris_cebi` (U_F) | cep 11,5 mm sola genişledi (x 3915–3983); cep rakorları (ELK_ZINCIR__rakor) KALIR, deliklerle eş eksen |

Düğüm/etiket kuralı: sac/profil/kaynak → `<birim>__sac` (dış kabuk sacları `__kabuk`), bağlantı/katalog → `__celik`, bas-aç → `__plastik`, taş yünü → `F_UST_KABIN__yalitim` (görünmez), kapakla dönen her şey → `__on_seffaf` + kpk. `kat` / `mek` etiketleri eski düğümün değeriyle aynı (E: mek 31 · U_F/U_KE: mek 39 · F_UST: mek 18; kaide: kat 1).
Montaj programında önek listeleri: E için `GOVDE_ONEK` (h3_e_sac_v1) — `govde_`, `kaide_e_` eklenecek; U için `ONEK` sözlüğü (h3_u_sac_v1).

## 2 · Mevcut iç parçaların bağlantısı (ARAYÜZ — mekanizma tarafında delik gerekir)

Duvara/tabana/tavana değen her mekanizma ve elektrik parçasına sacda PEM FHP gömme saplama deliği açıldı (baş dış yüzde, dışta iz yok); saplamanın kendisi
ARAYÜZ elemanıdır (GLB'ye girmez, CSV'de "ARAYÜZ" satırı): karşı parçada Ø5,5 (M5) / Ø6,6 (M6) delik + DIN 125 pul + ISO 10511 fiberli somun.
Liste: `E_denetim.json → arayuz` (48 kayıt), `U_denetim.json → birimler.*.arayuz`. Özet:
* E: şarjör eşik + köşebentler (11), besleyici askıları (5), J3 panel burçları (4 · FHP-M5×25), UHMW kılavuzlar sol + arka (4), kalıp tablası (4), pano plakası burçları (4), köprü (3), elektrik sensör braketleri (3), piston askıları (3), PD + B kablo kanalları (2), robot çöpü kızağı (2) · U_KE tabanı → E üst sacı 3 × PEM SP-M8 (E içinde, hazır).
* U_F (27): ana pano ayakları (4), ELK_IC kanalı (2), fan çerçeveleri (4 × 4 köşe = 16), baca flanşı (4, tavandan), havalandırma braketi (1) · U_KE (2): K üst sacı SP-M8 arayüzü.
* F üst kabin (32): J1/J2 panel burçları (2 × 4), davlumbaz konsolları + filtre çerçevesi (12, taban + bölme), kompresör ayakları (4), K yağ tankı braketi (2), gazlı yay braketleri (2), PD kanalları (2), hava askıları (2, tavan).
* Atlanan (yer güvenli değil / yama dar — rapor json'da): J3/J1/J2 burçları otomatikte atlandı çünkü elle konuldu; piston askısı 2, şarjör eşiği 1, baca yalıtımı (yün, saplama yok).

KOMŞU İSTASYON İŞLERİ (bu adımda yapılmadı — sahibine):
* K üst sacı: U_KE ↔ K için 2 × PEM SP-M8-1 gerekir (dünya x 4100 / 4300 · z −700) — U_KE tabanında Ø9 hazır.
* K ↔ E (3 × Ø9) ve K ↔ F (4 × Ø9) delikleri E sol / F sağ sacta hazır (h3_k_sac_v1 M8_E / M8_F ile eş eksen).
* TOPPING ↔ F (x 2500) bağlantısı: TOPPING sacı 5c'de; F sol sacında yalnız J1 ağzı + burçlar var.
* F gövdesi (5c): F üst kabinin yan + arka sacları (y 788–1862, fırın gövdesi bölgesi dahil) BU üreteçte — 5c yalnız TP10 / yükleme bandı / kapak tarafını yapmalı.

## 3 · Bugünkü modelden FARKLAR (hepsi üretim zorunluluğu; dış zarf ±0,5 içinde)

E
* Üst sac yan sacların ARASINA oturur (x 1,5–828,5, yanlarda 21,5 aşağı dönüş); yan saclar y 1862'ye kadar çıkar (bugünkü modelde düz levha bükümün ötesine taşıyordu → üretilemez).
* Arka sac taban üstünden başlar (y 126, alt iç dönüş tabana), üstte iç dönüş üst sacın altında (0,5 hava); taban arkada z −830'a uzadı (arka sacın dış yüzüyle aynı).
* Sağ yan sacın arka dönüşü yalnız y 1000–1855 (şarjör kapısı açıklığı bükümün 1,75 mm yanına geliyordu → DFM); altta 3 mm köşebent.
* Ön kasa dikmelerine tepe tapası, yan sac kulakları (2 mm, dikme arkasında) ve taban kulakları (3 mm).
* J3 ağzı 66 × 56 → 67 × 57 (EPDM kovan geçme payı 0,5).
* Şarjör kapısı menteşeleri arka sactaki 2 mm taşıyıcı lamaya, bas-açı yan sactaki 3 mm lamaya bağlı (gövde yarısı ölçüleri temsili).
* Kaide rayları 3 mm kısaldı + uç tapası (dış ölçü aynı), ayaklar GN 20 sınıfı M12 (taban Ø40).
U
* Tavan (430) yan sacların ARASINA oturur, dört kenar dönüşlü (köşeler açık + kare rahatlatma); yan saclar y 2200'e kadar.
* Omega: dar şapka (taç 30 × 20) düz bıçakla bükülemiyor → HAZIR HADDELİ omega profil (boy kesim), tavanın 0,3 altında, punta.
* U_F yan ön dönüşü y 2128'de biter (F kapağı bas-açları y 2130–2150 dönüşün üstünden geçer; eski Ø10 delik büküme 1,5 mm idi).
* Yan geçiş delikleri arka kenarı −827 → −820 (dönüşe 7 mm).
* Gömme giriş cebi 11,5 mm genişledi (bina rakoru Ø22 cep duvarına 1 mm'deydi); üst ve sağ kenarda flanş yok.
* U_F arka alt dönüşü V1 kanalının solunda biter; U_F sağ arka bağlantıları V1 / cep dışında.
F üst kabin
* Arka alt profil 2 mm öne (z −826,5…−796,5: yan sacın arka dönüşünün önünde); profil uçlarında yan sac bükümü için 3 × 4 köşe pahı (kesim listesinde).
* Tavan kirişi arka ucu z −827 → −804 (arka sacın üst dönüşü) + uç tapası.
* Yan sac ön dönüşü y 1625–1858 (gazlı yaylar y 1337–1612 dönüşün altından geçer — bugünkü modelde yay dönüşü 7 mm deliyordu).
* Yan sac arka dönüşü y 788–1610 (üstünde J1/J2 PD kanalı z −826'ya iniyor); sol üstte köşebent.
* Eski 40 × 40 yamalar ve kullanılmayan bilezik delikleri ÜRETİLMEZ (delik hiç açılmaz).
* F sağ yan sacına K'dan gelen 3 geçiş deliği eklendi (tartı rakoru Ø16,5 · yağ hortumu contaları Ø20,2 / Ø18,3) — bugünkü modelde hortumlar deliksiz geçiyordu.
* Taş yünü kılıf tavasından 1,25 içeride (tava bükümü), perçin başları için yerinde Ø12 × 3 kesik; V2 kablo kanalı tabandan geçer (kenara açık çentik + 3 yüzlü kovan, arka yüzü profil kapatır).

## 4 · Açık kalanlar
* Menteşe / bas-aç / ayarlı ayak ölçüleri TEMSİLİ (Southco / EMKA / GN 20 sınıfı) → katalog teyidi.
* PEM ölçüleri bülten yaklaşık değerleri (h3_sac_v1) → sipariş öncesi teyit.
* K faktörü (0,45) atölye 3 numune bükümüyle kalibre edilecek (sac_kararlar).
* Kapak açılma süpürmesi bu adımda koşulmadı (menteşe pivotları bugünkü kapakla aynı yerde); entegrasyonda montaj süpürmesi.
* Mekanizma tarafındaki Ø5,5 / Ø6,6 delikler mekanizma üreteçlerinde açılmadı (ARAYÜZ listesi).

## 5 · Denetim sonucu (bağımsız · `E_denetim.json`, `U_denetim.json`)

| | E | U_F | U_KE | F üst kabin |
|---|---|---|---|---|
| sac / profil | 64 / 10 | 6 / – | 5 / – | 10 / 6 |
| gövde parçası (GLB düğümü) | 477 | 138 | 112 | 225 |
| açınımdan yeniden büküm (ΔV, simetrik fark < %0,5) | 64/64 | 6/6 | 5/5 | 10/10 |
| DFM HATA / UYARI (abkant sırası dahil) | 0 / 1 | 0 / 1 | 0 / 0 | 0 / 0 |
| profil DFM HATA | 0 | – | – | 0 |
| gövde ↔ gövde (OCC hacim) | 0 | 0 | 0 | 0 |
| DOĞRU çakışma aracı (govde_denetim_dogru: manifold3d + VTK yoğun örnekleme + OCC teyit) — yeni gövde ↔ bugünkü modelin bölgedeki tüm parçaları + sac ↔ sac | 0 gerçek (70 PEM gömme başı izinli) | 0 gerçek (103 PEM gömme başı / çakışık yüz izinli; U için ortamda E'nin YENİ sacı) | | |
| havada | 0 | 0 | 0 | 0 |
| dış zarf (±0,5) | GEÇTİ (fark ≤ 0,15) | GEÇTİ | GEÇTİ | GEÇTİ |
| taş yünü görünür nokta | – | – | – | 0 / 2557 |

UYARI'lar: E `govde_kulak_ust_orta` kaynak ayağı 16 (tasarım 24, mutlak 16 — dikme 40 genişliğinde) · U_F `ust_f_giris_cebi` abkant: tanım sırasında kalıp çarpar, önerilen sırada temiz (CSV abkant_sira).
Not: U'nun büyük düz levhalarında (taban / arka / tavan) OCC çakışık yüz boolean'ı boş dönüyor → simetrik fark bulanık boolean (tol 1e-4) ile yeniden hesaplandı (sonuç %0,0).
