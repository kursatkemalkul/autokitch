# HAT v3.9 · YAMA ZİNCİRİ — SIRA (gece 2 · adım 4 · 4 Eki 2026)

2–4 Ekim'de modelde yapılan bütün değişiklikler montaj programında değil, doğrudan GLB'ye betiklerle yapılmıştı (hat3_v8 → v8b … v8zq).
Bu klasör o betikleri **özgün halleriyle, özgün sırayla** montaj programının arkasına bağlar: `h3/yap_hat3_montaj_v9.py` = montaj v7 + bu zincir → `hat3_v9.glb` (= v8zq).

- **Taban:** montaj v7'nin GLB'si (`hat3_v7.glb`). Montaj v7 deterministik (b3 2 Eki 08:09 ve b3_hiz 12:39 derlemeleri bayt bayt aynı) — ŞARTI: `h3_sac_v1` K sacı standart/kararlarını bulmalı. Bu dosyalar izlenmiyor (`<ağaç>/../../../../sac_standart`); bulunamazsa varsayılana düşer ve K_GOVDE'nin 4 düğümü farklı çıkar (4 Eki b9 ilk derlemesinde görüldü). v9: salt okunur kopyaları `sac_standart/`, `yap_hat3_montaj_v9.py` `AUTOKITCH_SAC_STANDART`'ı buna verir.
- **Montaj v8 neden taban değil:** `yap_hat3_montaj_v8.py` hiç başarıyla derlenmedi — `h3_kapak_v1.bolge_A` v3.8b'nin sildiği `onyuz_emniyet_*_alt` parçalarını arıyor → AssertionError (4 Eki 00:43 derlemesi). İçeriği (A ↔ U_A ara çerçevesi) zaten zincirin 00–02 adımları; sonraki betikler o GLB'nin üçgen/düğüm sırasına göre yazıldığı için doğru taban v7 GLB'sidir.
- **İş klasörü:** varsayılan `_local/yama_v9_is` (git dışı, geçici; ara GLB'ler ≈ 4 GB — commit edilmez, silinebilir).
- **Çalıştırma:** `python zincir.py --is <iş> --taban hat3_v7.glb --cikis hat3_v9.glb --uretec <arastirma/_uretec>` (yap_hat3_montaj_v9.py bunu çağırır). ≈ 9 dk (en uzun adım 14: ≈ 4–5 dk).
- **kaynak/**: yalnız zincirin gerçekten açtığı 137 dosya (tam zincir koşusunda Python denetim kancasıyla izlendi; `zincir.py --iz`), scratchpad'deki klasör düzeni AYNEN (betikler birbirini `../gece`, `elk2`, `birlesim` … yollarıyla çağırıyor). Mutlak yollar yer tutucu: `@@KOK_W@@` / `@@KOK_F@@` / `@@KOK_M@@` = iş klasörü, `@@PK_V7_*@@` = `_v7/parca_kutulari.json` (v7 montajının parça kutuları), `@@MEK_V3_W@@` = `_v7/mekanizma_v3.json`, `@@H3_W@@` = derleme ağacının `h3`'ü. `zincir.py` kopyalarken doldurur. Ara GLB'ler özgün adlarıyla üretilir (betiklerdeki sabit adlar — ör. `salt/yap.py` → `hat3_v8zl.glb` — bu yüzden çalışır).
- **Ara girdiler:** `_v7/parca_kutulari.json` + `_v7/mekanizma_v3.json` (montaj v7 çıktısı), küçük json/pkl ölçü dosyaları (`islem_v38bc.json`, `gece/m8t2/yollar_z2.json` …). Büyük önbellekler (m8_onbellek.npz, kay0.pkl, kayh.pkl) KOPYALANMADI — zincirde özgün komutlarıyla yeniden üretilir (adım 19, 24, 26, 28, 30).
- **Kaset üreteci yamaları:** `kaynak/_uretec_yama/` (kasar_cad_v15, sucuk_cad_v9, kaset_birlesim_v2, kaset_kontrol_adim3 + URETEC_NOTU.md); adım 31 bunları derleme ağacının `_uretec`'inden önce yükler.
- **Doğrulama:** her adım, kayıtlı girdi GLB'sinden çalıştırılıp kayıtlı çıktıyla **bayt bayt** karşılaştırıldı (sonuç sütunu). Tam zincir: bkz. `scratchpad/gece2/adim4/KARSILASTIRMA.md`.

| # | betik(ler) (klasör) | girdi → çıktı | ne yapar | doğrulama |
|---|---|---|---|---|
| 00 | `glb_parca_sil.py` + `_v7/parca_kutulari.json` | hat3_v7 → hat3_v8 | A ↔ U_A ara çerçevesi (A üst kuşakları, ön üst kayıt, A tavan / U_A taban sac çerçevesi, U_A ön alt kayıt) silinir | bayt aynı |
| 01 | `glb_duzenle.py` + `islem_v38bc.json` | v8 → v8c | A dikmeleri + sol/arka sac tavana uzar, perde kaydı + ışık perdesi + emniyet sensörü kalkar, alt dikmeler/ara lamalar silinir, ön dikmeler 788'e, alt kayıt 788–893,5 (v8b ara sürüm değil, bc birleşik işlem) | bayt aynı |
| 02 | `a_govde_yeni.py` | v8c → v8k | A + U_A gövdesi baştan tek temiz kutu (kapalı ürün, sağ yan sacında tabla geçiş ağzı, kaide A); v8d…v8j aynı betiğin ara denemeleri | bayt aynı |
| 03 | `b_cerceve_govde.py` | v8k → v8l | B ön çerçeve sacı kapak malzemesinden gövde malzemesine (opak, kpk yok) | bayt aynı |
| 04 | `b_govde_yeni.py` | v8l → v8n | B çekmece dolabı gövdesi baştan (v8m = b_depo_kapat ara denemesi, zincirde yok) | bayt aynı |
| 05 | `topping_govde_yeni.py` (+ `tg/tgeo.py`, `tg/glb_sikistir.py`) + **`v9yama/pu_sira.py`** | v8n → v8o | TOPPING gövdesi baştan (ön düzlem z 39, çift cidar, PU, kaset penceresi, evaporatör tapası …) + sıkıştır. **v9 sıra yaması:** bugün yeniden çalışınca PU duvarının sağ şeridinde 144 köşe aynı üçgenlerle farklı SIRADA çıkıyor (OCC Boolean yüz sırası); yama yalnız sırayı kayıtlı v8o'ya getirir, üçgen kümesi aynı değilse durur | sıra yamasıyla bayt aynı (yamasız: PU 144 köşe sıra farkı, geometri aynı) |
| 06 | `b_fitil_duzelt.py` → `topping_basac_alt.py` → `ug/u_govde_yeni_v8o.py` | v8o → _m1 → _m2 → v8p | B çekmece + depo fitilleri · TOPPING kanatları alt bas-aç · U_F + U_KE üst depo gövdeleri. **Not:** u_govde_yeni.py 21:45'te değiştirildi; v8p'yi üreten sürüm değişiklikten önce `ug/u_govde_yeni_v8o.py` olarak yedeklenmiş, o kullanılır | bayt aynı |
| 07 | `e_govde_yeni.py` | v8p → v8r | E (kutu katlama) gövdesi baştan | bayt aynı |
| 08 | `e_duzelt.py` | v8r → v8s | E: Kemal'in 7 maddesi (şarjör yan kapısı, …) | bayt aynı |
| 09 | `pano_fis_etiket.py` + `_v7/parca_kutulari.json` | v8s → v8t | ana panodaki istasyon fişleri → Elektrik/Ana pano mekanizması | bayt aynı |
| 10 | `u_govde_yeni.py` (son sürüm) | v8t → v8u | U_F + U_KE gövdeleri (21:45 sürümü) | bayt aynı |
| 11 | `f_kabin_yeni.py` | v8u → v8v | fırın üstü dolap: taban + çerçeve + yalıtım + orta bölme (Kemal çizimi 86) | bayt aynı |
| 12 | `gece/m1…m6_*.py` | v8v → w1 … w6 = v8w | K ara raf sil · TOPPING sağ duvar tabla geçişi · sağ kablo demeti · E kaide hizası · düz zemin · kapak parçaları kpk | bayt aynı |
| 13 | `gece/m7a_birim_tasi.py` → `m7b_kabuk.py` → `m7c_mandal_kablo.py` + sıkıştır | v8w → m7/v8x_a/b/c → v8x | TOPPING UNO/kaset yerleşimi (deneme A + sol cep), kabuk, kilit mandalı + kablolar | bayt aynı |
| 14 | `gece/m8_fix_1…5_*.py` + sıkıştır | v8x → y1 … y5 → v8y | çakışma / kablo / pnömatik / delik / havada düzeltici (m8_fix_6 derz İPTAL, zincirde yok) | bayt aynı |
| 15 | `gece/m8t2_yaz.py` (`m8t2/yollar_z2.json`, `--oluk`) → `m8t2_madde3.py` + sıkıştır | v8y → z1 → z2 → v8z | 19 ana hat kablosu sabit şerit + UF3 oluk · kör tapalar, F hava hattı kelepçeleri | bayt aynı |
| 16 | `gece/m8t3_derz.py` + sıkıştır | v8z → m8t3/za1 → v8za | davlumbaz baca kanalı çatı deliğinden baca tabanına | bayt aynı |
| 17 | `grup/grup_duzen.py` (+ `_v7/mekanizma_v3.json`) | v8za → v8zb | montaj ağacı (mek) + disiplin (kat) etiketleri; geometri aynı | bayt aynı |
| 18 | `topfix/t1_sil … t6_duzelt.py` + sıkıştır | v8zb → t1 … t6 → v8zc | TOPPING cep geri, yeni yerleşim, evaporatör iki kaset, A boş kabuk, X motoru rayın TOPPING ucunda | bayt aynı |
| 19 | `gece/m8/m8_yukle.py` (önbellek `paket/zc`) → `paket/p1_glb.py` → `p2_dugum.py` + sıkıştır | v8zc → p1 → p2 → v8zd | robot kalktı, 3 kademe (Dükkân hattı), E çöp oluğu kapakta, TOPPING perde menfezli şerit, kelepçe/A soketi/dikme/kanal | bayt aynı |
| 20 | `kalt/k_alt.py` | v8zd → v8ze | K alt yeniden: istasyon rafı 304 3 mm + 6 dik destek | bayt aynı |
| 21 | `tpaket/zincir.sh` (tp1 duvar · tp2 evaporatör · tp3 pnömatik · tp4 motor) + sıkıştır | v8ze → v8zf | TOPPING paketi: evaporatör yan yana, sürücü kartları, CRB2 aktüatör + 12 hortum, tabla motor cıvataları (tp6 animasyon zincir dışı) | bayt aynı |
| 22 | `birlesim/calistir.sh` (q1 ürün · q2 Harting · q3 QR · q4 K kablo · q5 B reed · q6 tezgâh) + sıkıştır | v8zf → v8zh | QR/tezgâh/kablo paketi TOPPING çıktısının üstüne (v8zg = aynı paket v8ze üstüne, ara deneme, zincirde yok) | bayt aynı |
| 23 | `kalanlar/t3_tapa.py` + sıkıştır | v8zh → t3 → v8zi | KD3 kanalı 4 boş kablo deliğine kör tapa | bayt aynı |
| 24 | `elk2/e1_sil.py` → (`m8_yukle` → `e1c/`) → `e2_zincir.py` → `e3_renk.py` + sıkıştır | v8zi → e1 → e2 → e3 → v8zj | elektrik tesisatı baştan: zincir (daisy chain), renk kuralı | bayt aynı |
| 25 | `elk3/e4.py` + sıkıştır | v8zj → e4 → v8zk | elektrik içeriden: dış kanal yok, birleşim panelleri, iç kanallar, gömme pano cebi | bayt aynı |
| 26 | `elk4/cikar.py` (kay0.pkl) → `elk4/b4.py ts ks fs us bs` + sıkıştır | v8zk → e5 → v8zl | iç kablolama temizliği (ELK_IC__kanal), ana şalter panoda, sabit yayıcı, yeşil hava hortumu | bayt aynı |
| 27 | `salt/yap.py` | v8zl → v8zm | panodaki eski ana şalter (iSW 4P 40A) kalktı, bina kablosu kapıdaki şaltere | bayt aynı |
| 28 | `elk5/cikar.py` (kay0.pkl) → `elk5/b5run.py qr5 k5 b5 p5` + sıkıştır | v8zm → e6 → v8zn | QR/K/B iç kablolar kanalda, pano arka çıkışı, ABB OT40 | bayt aynı |
| 29 | `derz/derz_hiza.py` | v8zn → v8zo | ön yüz derz hizası (gece 2 adım 0) | bayt aynı |
| 30 | `gece2/adim2/hava/cikar_h.py` (kayh.pkl) → `a1_qr_tezgah` → `a2_b_kose` → `a3_teyit` → `a4_hava` + sıkıştır | v8zo → a1 … a4 → v8zp | QR sola 200, tezgâh 180° + ayrı bina hattı, B kanal köşeleri, şalter/QR paneli teyitleri, hava kanalları (gece 2 adım 2) | bayt aynı |
| 31 | `gece2/adim3/a1_kaset.py` (kasar_cad_v15 + sucuk_cad_v9, `_uretec_yama/`) + sıkıştır | v8zp → a1 → v8zq | kaşar kapak arka yüzü +2 mm, sucuk tüp konisi kırpıldı, geçme parçaları ince ağ, yarık dili + raf contaları (gece 2 adım 3). Betik `os.chdir(üreteç)` yaptığı için girdi/çıktı mutlak yolla verilir; üreteç klasörü `YAMA_URETEC` | bayt aynı |

Zincir dışı kalan GLB'ler (ara deneme / iptal): v8b, v8d–v8j, v8m, v8o_fitil / v8o_basac / v8o_ust (06'nın ayrı denemeleri), _m1/_m2 (06 içinde yeniden üretilir), v8y6_derz_IPTAL, v8z1/z2, v8za1, v8zg, v8zj_k.
Elle tek seferlik (`python -c`) yapılmış ve zincire girmeyen değişiklik **bulunmadı**: 32 adımın hepsi kayıtlı girdi → kayıtlı çıktıyı bayt bayt veren betiklerle yeniden üretildi; tek "fark yaması" adım 05'teki köşe SIRASI yamasıdır (geometri değiştirmez).

## ADIM 5-ENTEGRASYON 1. TUR (gece 2 · 4 Eki 2026 · Claude) — üretim sacı gövdeleri ana modele (adım 33–36)

Betikler **yama_v9/ altında** (kaynak/ dışında; zincir `{YAMA}` yer tutucusuyla çağırır): `33_a_sac.py`, `34_b_sac.py`, `35_e_sac.py`, `36_u_sac.py` + ortak `sac_ent.py`.
Ortam (zincir.py kurar): `YAMA_URETEC` (derleme ağacının `_uretec`'i — üreteçler `h3/h3_<ist>_sac_v1.py` oradan), `AUTOKITCH_SAC_STANDART` = `yama_v9/sac_standart`
(scratchpad/sac_standart ile bayt aynı · K / A / B / E / U aynı standart), `ADIM5` = `yama_v9/veri` (E / U üreteci mekanizma FHP saplamalarını
`_bilesen_v8zq.pkl` bileşen kutularından kurar; yalnız okunur), `YAMA_IS_KOK` = iş klasörü (m8kit, tg/glb_sikistir, govde_denetim_dogru oradan).
**32 boş** (numara atlandı). 2. tur: 37 TOPPING, 38 F (adım 5c üreteçleri).
Her adım iki evre: (1) m8kit ile KARŞI TARAF — arayüz elemanının (cıvata / PEM / perçin somun / FHP saplama) geçtiği mevcut parçalara manifold3d boolean
FARK (kesici = elemanın katısı ∪ cıvata / saplamada ISO 273 orta geçiş deliği; havşa başı havşayı da açar), açık (T-birleşimli) ağda düzlemsel cep
(köpük kapağı hacmi); karşı parçaya ait elemanlar o parçanın düğümüne · FHP saplama yalnız kendi karşı parçası (+ ona alın oturan ince levha / aynı
birimin gövdesi) içinden geçer, başka parçaya giriyorsa standart seriden kısaltılır, olmuyorsa ÇIKARILIR (rapora) · (2) ham GLB: eski gövde düğümleri
boşalır / yeni üretim sacı parçaları yazılır (tessellate 0,05 / 0,25, indisli) · kat / mek eski düğümün değeri · kpk = kapakla dönenler · sıkıştır.
Her çıktının yanında `<çıktı>_ent.json` (parça → düğüm, kutu, üçgen aralığı; delik / cep / saplama günlüğü).

| # | betik | girdi → çıktı | ne yapar | doğrulama |
|---|---|---|---|---|
| 33 | `33_a_sac.py` (h3_a_sac_v1) | v8zq → v9a | A gövdesi: A_GOVDE__sac / __paslanmaz / __conta (yeni) / __plastik · KAIDE_A__paslanmaz / __sac · A_ONYUZ__on_seffaf (kpk) · eski A_ONYUZ servis kapağı / paslanmaz / plastik boşalır · karşı: açıcı kolon flanşı 4 × Ø9 (TOPPING_MODUL__sac[29]), tabla rayı 4 × Ø6,6 (sac[8]), TOPPING sol dış sacı Ø9 / Ø10,5 + **4 PEM SP-M8** (TOPPING_MODUL__paslanmaz, TOPPING/Gövde) + PU'da köpük kapağı cebi, B tavanı / GFRP ped / B_MODULER üst kirişi Ø9 · NOT: TOPPING sacı 5c'de yenilenince bu delik + PEM yeni TOPPING sacında olmalı (h3_a_sac_v1.M8_T) | yeni gerçek çakışma 0 (35 izinli = PEM gömme başı), havada 0, zarf 0 |
| 34 | `34_b_sac.py` (h3_b_sac_v1 + h3_a_sac_v1.G.M8 + KB_DELIK) | v9a → v9b | B gövdesi: B_KASA__sac / __on_cerceve / __pu / __koyu · __paslanmaz (yeni: 126 PEM SP-M5 + arayüz cıvataları) · __conta (yeni) · B_KASA__celik (14 ayak) dokunulmaz · karşı: 42 sabit ray + ara ray × 3 havşa deliği (84 bileşen, DIN 7991 M5), **18 perçin somun M8** (alt şase 10 · A → B üst kiriş 6 · K → B taşıyıcı 2; duvar kalınlığı ışınla ölçülür) → yeni B_MODULER__baglanti / B_TASIYICI__baglanti düğümleri (karşı parçanın kendi düğümünde olsa yuvasıyla tek bileşen sayılır); GFRP pedde baş cebi; dış taban / dış tavan 2'de perçin başı için Ø15,5 boşluk (üreteçte Ø9 → Ø15,5 yapılmalı) | bkz. DURUM |
| 35 | `35_e_sac.py` (h3_e_sac_v1) | v9b → v9c | E gövdesi: E_GOVDE__kabuk / __sac / __celik / __plastik / __on_seffaf (kpk) · E_MODULER__paslanmaz (kat 1) · karşı: 39 mekanizma / panel FHP deliği (şarjör, besleyici, kalıp, köprü, piston, elektrik, kanal, J3 burç) + U_KE tabanı (eski) 3 × Ø9 · 9 saplama çıkarıldı (karton yığını / çöp kovası / motor / J3 Harting önünde) | bkz. DURUM |
| 36 | `36_u_sac.py` (h3_u_sac_v1) | v9c → v9d | U_F + U_KE gövdesi (__sac / __paslanmaz) · F_UST_KABIN__sac / __yalitim · F_UST_KABIN__paslanmaz (eski 6 profil silinir, 30 kelepçe / askı kalır, yeni eklenir) · F_DAVLUMBAZ__sac eski bölme duvarı silinir · ELK_ZINCIR__paslanmaz eski gömme cep (21 bileşen) silinir · karşı: mekanizma FHP delikleri (ana pano, ELK_IC kanalı, fan çerçeveleri + fan kasası, davlumbaz konsolları, kompresör ayakları, J1/J2 burçları, gazlı yay braketleri), **K üst sacına 2 PEM SP-M8** (yeni K_GOVDE__baglanti, K/Gövde) · 19 saplama çıkarıldı (ana pano ayakları — pano kutusu hemen üstte, baca yalıtımı, J1/J2 Harting / etiket, hava askısı, davlumbaz) | bkz. DURUM |

| 37 | `37_topping_sac.py` (h3_topping_sac_v1 + h3_a_sac_v1) | v9d → v9e | TOPPING gövdesi: üretecin DEGISEN bileşenleri v8zq'daki KUTULARIYLA silinir (TOPPING_MODUL__sac 66 · __paslanmaz 51 · __pu 10) + adım 33'ün 4 PEM'i (artık TOPPING sol yan sacında) · yeni birim **TOPPING_GOVDE** (__kabuk / __sac / __cerceve / __pu / __paslanmaz / __conta / __pom; mek 7) · kaide → KAIDE_C__paslanmaz (kat 1) · karşı: F sol yan 4 × Ø9 (biri U_F sol sacında), B dış tavanı Ø9 + B_MODULER üst kirişine 4 × M8 kapalı perçin somun (→ B_MODULER__baglanti), mekanizma FHP delikleri · **üreteç düzeltmesi**: arka servis sacı 17 × ISO 7380 → DIN 7991 havşa başlı + çökertme havşa (zarf farkı 2,6 → 0) | bkz. DURUM |
| 38 | `38_f_sac.py` (h3_f_sac_v1) | v9e → v9f | F: ön kapak parçaları KAPAK_F_SOL / _SAG düğümlerine (v8zq [0,1,2,3,5,8] kutuyla silinir, menteşe + gazlı yay kalır) · atış kanalı F_DAVLUMBAZ__sac'a (eski [1] silinir) · baca → U_F_BACA__sac / __paslanmaz / __conta (yeni) / __yalitim (yeni, görünmez; eski 'yalıtım görünür' boşalır) · karşı: U_F tavanına 8 × Ø6,6 (baca flanşı M6), menteşe kanadı Ø5,5 · taş yününde cıvata yuvası | bkz. DURUM |

Doğrulama: `zincir.py --adim 33-38 --girdi-dizin <hat3_v8zq'lu klasör>` ve tam zincir 00–38 → `hat3_v9f.glb` bayt aynı (DURUM.md kaydı).

## ADIM 8 · üreteç düzeltmeleri (gece 2 · 4 Eki 2026 · Claude) — entegrasyon açıkları üreteçlere taşındı

Zincir adımları 33–38 aynı; değişen yalnız üreteçler (adımlar onları import eder). Kaldırma / taşıma üreteçlerin `kur()` SONUNDA yapılır (`h3_e_sac_v1.saplama_duzelt`, U aynısını kullanır; TOPPING kendi `saplama_duzelt`'i, PU bloklarından önce): diğer saplamaların yer seçimi (mevcut deliklere uzaklık) ve adları birebir aynı kalır — eski / yeni üreteç arayüz ad listeleri karşılaştırıldı (yalnız çıkarılanlar eksik, `_6b` ek).
- **Ortam notu (zincir.py docstring + calis()):** `YAMA_URETEC` = --uretec (üreteçler `<uretec>/h3/` altından) · `YAMA_IS_KOK` = iş klasörü ·
  `AUTOKITCH_SAC_STANDART` adım 00–31'de **KURULMAZ** (kurulursa çıktıları değişir), 33+ `sac_ent.py` `yama_v9/sac_standart`'a kurar ·
  `ADIM5` = `yama_v9/veri` (`sac_ent.py` kurar; E / U üreteci `_bilesen_v8zq.pkl` okur). Aralık koşusunda `--girdi-dizin` yalnız ilk adımın girdisini
  bağlar; 37 / 38 iş kökünde `hat3_v8zq.glb` ister.
- **(a) çıkarılan 36 FHP saplama** (`sac_ent` "UYARI saplama ÇIKARILDI"): üreteçlerde `SAPLAMA_CIKAR` sözlüğü (ad → gerekçe) — saplama, PEM'i ve sacdaki
  PEM deliği (sac kesiği) birlikte kaldırılır (boş delik kalmaz). E 9 (`h3_e_sac_v1`: J3 üst 2 burç · şarjör UHMW astarı 4 · karşı parçasız taban 3) · U 18 + 1 taşındı
  (`h3_u_sac_v1`: ana pano ayak laması 4 · eski baca flanşı 4 — F üreteci 38'de bacayı yenileyip 8 × M6 ile bağlıyor · J1/J2 üst burç 4 · hava hortumu
  askısı 2 · davlumbaz taşıyıcı laması 4) · TOPPING 8 (`h3_topping_sac_v1`: J1 üst 2 burç · ELK_IC kablo kanalı 2 · evaporatör ayağı 4).
  **Taşınan 1:** `arayuz_mek_ust_f_arka_sac_6` (fan braketi U_F_HAVALANDIRMA__celik 70 × 34, ortasında plastik gövde; braket başka saplamayla tutulmuyordu)
  → `SAPLAMA_TASI`: x 3334 + x 3386 iki saplama (`_6`, `_6b`).
- **(b) TOPPING tabla rayı M6** (x 1750 / 2250): `h3_topping_sac_v1.RAY_M6 = []` — ray tabanı o eksende yok (ray A tarafında `h3_a_sac_v1.RAY_M6` ile bağlı);
  kaide plakası PEM SP-M6, gövde tabanı Ø6,6 ve arayüz cıvatası üretilmez. 37'deki `ATLA` süzgeci boş kalır (güvenlik ağı).
- **(c) B perçin somun baş boşluğu:** `h3_b_sac_v1.PERCIN_BAS_BOSLUK = 15.5` — dış tavan 2 (K → B, 2 delik) + dış taban 1 / 2 (alt şase, 10 delik) Ø9 → Ø15,5
  (A → B dış tavan 1 delikleri Ø9 kalır: perçin somun başı o sacla kesişmiyordu, 34 de kesmiyordu). 34'teki `SE.kes_govde` güvenlik ağı olarak durur;
  kesişim 0 → "gövde boşluğu" satırı çıkmaz.
- **Açık kalan (karşı parça artık bağsız; düzeltme başka üreteçte / Kemal kararı):** J1 / J2 / J3 panellerinin üst burçları (etiket + Harting burç
  ekseninde → elektrik üreteci), şarjör UHMW astarları (dıştan havşa vida + astarda dişli burç ya da yapıştırma), ana pano ayak lamaları (alttan havşa vida),
  evaporatör ayakları + davlumbaz taşıyıcı lamaları + hava askıları (kör perçin / kaynak), ELK_IC kanal [65] (kanal perçini).
- **Doğrulama (4 Eki 05:01):** `zincir.py --adim 34-38 --girdi-dizin scratchpad/gece2/adim5e/is5` (iş: `gece2/adim8/is_gen`, kökte hat3_v8zq.glb bağlı) → 34 38 sn · 35 30 sn · 36 27 sn · 37 70 sn · 38 14 sn (180 sn) · "saplama ÇIKARILDI" **0** · 34'te "gövde boşluğu" satırı yok (Ø15,5 üreteçten) · taşınan 2 saplama U_F_HAVALANDIRMA__celik[0]'a delik açtı · hat3_v9f 191 209 748 B (önceki 191 592 564) · düğüm 824 / mesh 816 aynı · üçgen farkı yalnız E_GOVDE / U_F_GOVDE / F_UST_KABIN / TOPPING_GOVDE__kabuk / KAIDE_C (kalkan delik + PEM) ve U_F_HAVALANDIRMA__celik (+2 delik).
- **Üreteç denetimleri (ayrı klasör, adim5 çıktılarına yazılmadı):** B (`gece2/adim8/den_B`) açınım 63/63 · DFM 0 · zarf geçti · v8zq çakışma 0 · havada 0 · PU açık 0 · E (`gece2/adim8_den`) DFM 0 HATA (1 uyarı önceden) · havada 0 · zarf geçti · iç çakışma 70 = önceki koşuyla aynı (PEM saplama başı) · U DFM 0 · havada 0 (önce 2) · zarf: U_F/U_KE M8 fırın/E cıvatası payı önceki koşuyla aynı · TOPPING (`gece2/adim8/den_T`) açınım 43/43 · DFM 0 · zarf 0 · v8zq çakışma 0 · havada 0 · PU açık 0 · gövde↔gövde 17 = servis sacı DIN 7991 vida ↔ PEM SP-M5 diş içi (4 Eki havşa düzeltmesinden; ADIM 8 ile ilgisiz, açık).

## ADIM 8 · SERVİS DÜZELTMELERİ + ACİL STOP (gece 2 · 4 Eki 2026 · Claude) — adım 39–40

Betikler **yama_v9/ altında** (33–38 gibi `{YAMA}` ile çağrılır, ortak araç `sac_ent.py`; ortam aynı: `YAMA_IS_KOK`, `YAMA_URETEC`).

| # | betik | girdi → çıktı | ne yapar | doğrulama |
|---|---|---|---|---|
| 39 | `39_servis.py` | v9f → v9g | SERVIS.md D2–D4 · **D2** fırın üstü üst kaydı (F_UST_KABIN__sac 30×30×2) dikmenin sağında bölünür: sol parça kaynaklı, sağ parça x 3360–3996,5 sökülür (2 iç köşebent 5 mm lama + 4 × ISO 7380 M6×12, kayıt alt cidarında Ø6,6 delik), sağ uç kaynak dikişi silinir · **D3** yağ lansı emiş / dönüş hortumunda kapamalı hızlı kaplin (yeni düğüm K_YAG__kaplin; hortum kaplin boyunca kesilir) + seviye şalteri M12 fişi · **D4** kompresör çıkışında 4 turluk PU spiral servis halkası (z −391…−432; düz boru −437'den) + fişli besleme (yeni düğüm HAVA_KOMPRESOR__kablo: motor → hat içi fiş-priz → orta bölmede M16 rakor (Ø16 delik) → arka kablo rakoru) · **D1 uygulanmadı**: A istasyon kutusu modelde yok (A elektriksiz) | yeni parça çakışması 0 (yalnız rakor ↔ sac temas 0,02 mm³) |
| 40 | `40_acil_stop.py` | v9g → v9h | 6 acil stop (Schneider XB4BS8442 Ø40 + ZBY9330T Ø60): TOPPING (2440, 1000) · B depo çekmecesi önü (4300, 750; x ≤ 4330 → çekmece açılınca QR'a çarpmaz) · F sol üst kapak (2600, 1460) · K (4300, 1400) · E sağ üst (5150, 1300) · QR robot yüzü (5100, 1690, −z). Yeni düğümler ACIL_STOP__kirmizi / __sari / __siyah (kat 6, mek = istasyonun Elektrik grubu, kpk = kapakla gelir). Gövde (30 × 30 × 43) kapak katmanlarında cep açar (delik_ac). Kablo çizilmedi | yeni parça çakışması 0 |

Ortam değişkeni notu (zincir.py): bkz. yukarıdaki "Ortam" paragrafı; 39–40 ek bir değişken istemez. 39 m8kit'te değiştirilen üçgenleri `Karsi` görmeden önce ara GLB'ye yazıp yeniden yükler (m8kit eklenen üçgenleri kayıttan sonra görür).
Sayfaya giden kopya (W/otonom/hat3d/v3/hat3_v8.glb) zincir çıktısının **EXT_meshopt_compression** (kayıpsız, INDICES kodeği, bayt bayt geri açılır) sıkıştırılmış hâlidir: `gece2/adim8/kucuk/meshopt_kucult.mjs <ham> <sayfa> --idx seq`. Ham GLB (denetim / üreteç betikleri bunu okur) scratchpad'de `hat3_v9h.glb`.

## ADIM 9 · KALAN GERÇEK SORUNLAR (gece 2 · 4 Eki 2026 · Claude) — adım 41–42

Betikler yama_v9/ altında, ortam 39–40 ile aynı (`YAMA_IS_KOK`, `YAMA_URETEC`; ek değişken yok). Kaynak: `gece2/adim8/denetim/RAPOR.md`.

| # | betik | girdi → çıktı | ne yapar | doğrulama |
|---|---|---|---|---|
| 41 | `41_gecis_kablo.py` | v9h → v9i | **G1** piston çubukları (PISTON_SOS / _HARC / _KUSBASI Ø11,9): silindir gövdesi (aluminyum 1/5/13, Ø37,7) + burun (2/6/14) boyunca Ø12,4 çubuk kovanı; çubuk ucu somununda (PISTON [1]) üst çubuk kadar kör yuva · **G2** bakır borular 11–18: rakor / manşonda boru soketi (rakor − boru), T birleşiminde küçük boruda karşı boru hacmi · **G3** silikon hortum kelepçe bloğu (silikon 10) hortum yatakları · **G4** döner valf gövdeleri (VALF_*[0], dönel simetrik) ↔ sabit taşıyıcılar (paslanmaz 24/51/8, aluminyum 12): valf + 0,3 mm yuva · **G5** celik 125/126 ↔ paslanmaz 17/33, paslanmaz 18↔19, 34↔35, 56/57 ↔ saydam_celik 3, paslanmaz 18/34 ↔ pom 1/4 (büyük parçada küçüğün yuvası) · **K1** QR Cat6A göz çıkışları (kablo_sinyal 30–41) +z 3,5 → ısıtıcı kablosundan ayrı şerit · **P1** B ön çerçeve derzine (x 2090,75–2091,25, y 124,5–786,5, z 23–24) dolgu şeridi (B_KASA__on_cerceve) | bkz. DURUM |
| 42 | `42_havada_oturt.py` | v9i → v9j | havada 9 grup en yakın taşıyıcıya ötelenir (trimesh en kısa vektör, 0,05 mm temas payı; kanal grupları yalnız yapı düğümlerine — kablo / rakor değil): ELK_IC kanal 234–245 (+y 0,95 → F_UST_KABIN sac) · 844–855 (−y 1,45 → B_SOGUTMA) · 265–275 (−x 10,45 → U_F_HAVALANDIRMA) · 246–249 (−y 8,95) · 250–253 (−x 4,71 −y 4,17) · DOLAP evap fan kablosu 315–322 (−y 3,93) · ELK_K kablo 37–43 (−z 1,75) · RevPi DIO / AIO (−y 1,73, yanındaki modüle). 0 mm'lik 2 grup (DOLAP sigorta + klemens, kanal 215–226) ve kanal 230–233 (ötelenince fırın CEE rakoruna 3 mm giriyor) dokunulmadı | bkz. DURUM |

NOT (G1): denetim raporu aluminyum 1/5/13'ü "evaporatör kaseti / soğuk iç kaplama" diye adlandırmıştı (parca_kutulari kutu eşlemesi); geometri pnömatik silindir gövdesi (Ø37,7 × 139 + Ø23,6 burun + arka kapak, çubuk ekseninde) → körük yerine çubuk kovanı.
NOT (kart): TOPPING_MODUL__kart "32 çift" çakışma 4 sürücünün KENDİ içindeki STEP alt parçaları (gövde ↔ kart / soğutucu); sürücüler 33 mm adımla dizili, gövdeler arası 5 mm boşluk → üst üste değil, düzeltme gerekmez (üretici modeli içi).
Zincir doğrulaması: `zincir.py --adim 40-42 --girdi-dizin gece2/adim8/is_tam` (is_tam'daki v9g = 8d82d2f zinciri; gece2/adim8/hat3_v9g.glb ESKİ ara çıktı, kullanma).

## ADIM 43 · RAY VİDALARI M5 × 6 (4 Eki 2026 · Claude · Kemal onayı) — adım 43

| # | betik | girdi → çıktı | ne yapar | doğrulama |
|---|---|---|---|---|
| 43 | `43_ray_vida.py` | v9j → v9k | B_KASA__paslanmaz içindeki çekmece ray vidaları (DIN 7991 M5 havşa · kutu 10 × 10 × 10 · eksen x · baş Ø10 ray tarafında) bulunur, vidanın UÇ düzlemindeki köşeler başa doğru 4,0 mm kaydırılır → toplam boy 10 → 6 (gövde 7,2 → 3,2). Baş, PEM SP-M5, köpük kapağı, ray deliği değişmez. Beklenen 126 (h3_b_sac_v1.raylar(): 42 sabit ray × 3) — farklıysa betik durur | 126 vida bulundu / kısaltıldı · 93 sn · `hat3_v9k_ent.json` (her vidanın eski / yeni uç x'i) |

Kaynak: tek çekmece montaj animasyonu v1 denetimi (M5 × 10'un ucu köpük kapağını 3,97 mm delip PU'ya giriyordu).
**AÇIK (Kemal kararı):** M5 × 6'nın ucu (sol rayda x 1450,5) PEM'in arkasından köpük kapağının tabanına 0,77 mm giriyor — kapak tabanı 0,8 mm, delmiyor ama baskı yapıyor (kapağın iç tabanı = PEM arkası, kavite yok). Çözüm: köpük kapağı 1 mm derin (h3_b_sac_v1.raylar(): kapak boyu Lb + 0,8 → Lb + 1,8 ve PU_KES aynı) ya da M5 × 5 (DIN 7991'de standart boy değil).
Sayfa kopyası: `meshopt_kucult.mjs hat3_v9k.glb <W>/otonom/hat3d/v3/hat3_v8.glb --idx seq` (5646 bufferView bayt bayt aynı, HATA 0) · makine_v3_8.html `hat3_v8.glb?v=9k`.

## ADIM 44 · B ÇEKMECE ÜNİTESİ DÜZELTMELERİ (4 Eki 2026 · Claude · Kemal onayı, tek çekmece montaj animasyonu v2 geri bildirimi) — adım 44

| # | betik | girdi → çıktı | ne yapar | doğrulama |
|---|---|---|---|---|
| 44 | `44_cekmece_duzeltme.py` (+ `veri/cek3geo.py`, `veri/v2geo.py`) | v9k → v9l | 21 çekmecenin hepsi (her biri sol / sağ sabit rayına göre ötelenir): **A1** kayış çenesi ayrı blok (alt gövde 2,5 + ara 1,2 TIG · üst çene 2,5) · kol 3 (kutuya TIG) + kol tablası 2,5 (2 × Ø3,4, kola TIG) · 2 × ISO 7380 M3 × 12 + 2 × ISO 4032 M3 (çekmece açıkken) · mıknatıs (57135) 2 mm kulağa (tablaya TIG) 2 × ISO 7380 M3 × 8 → PEM CLS-M3-2, mıknatısta 2 yarık · **reed** (59135 × 2) +2 mm sağa, 2 mm reed plakasına (lamaya punta) 2 × M3 × 8 → PEM CLS-M3-2 · **A3** sensör plakası silindi (ELK_IC köşesinin içinde, lamaya bağsız; lama köşe yüzünden uzatılamaz) · avara mili +1 mm + E segman yuvası Ø5 + DIN 6799 RS 5 · motor braketi 2 × M5 / 4 × M3 havşa + 2 × DIN 7991 M5 × 6 + arka iç sacda 2 × PEM SP-M5-1 (Ø6,4) + 2 köpük kapağı + PU cebi · 4 × DIN 7991 M3 × 6 + motor yüzünde 4 × M3 dişli · kasnak setskur DIN 913 M3 × 4 + radyal delik · köşebent 1,5 × 4 + 4 × ISO 7380 M4 × 6 + lamada M4 dişli kör delik · ön braketlerde 2 × Ø5,5 + 4 × PEM FHS-M5-10 + pul + somun · ön kapakta PU (iç panel arkası ↔ dış kabuk, fitil kanalı boş) · ray vidası köpük kapakları (126) 1 mm derin + PU cebi. **Kör perçin UYGULANMADI**: Ø6,5 baş ön çerçevenin önünde üst çekmecenin fitiline biniyor (çerçeve önü fitil yüzeyi) → avara ön flanşı çerçeve arkasına içeriden TIG (animasyonda). Kaynaklar modelde yok. | 35 sn · B çekmece bölgesi çakışma (cek3/cak.py, kapalı bileşen çiftleri, 21 çekmece): v9k 157 → v9l 27 (126 kapak ↔ PEM giderildi), yeni gerçek çakışma 0 · tek çekmece animasyonu son kare ↔ v9l en büyük fark 0,0002 mm |

Sayfa kopyası: `meshopt_kucult.mjs hat3_v9l.glb <W>/otonom/hat3d/v3/hat3_v8.glb --idx seq` (5646 bufferView bayt bayt aynı, HATA 0; 101,0 MB) · makine_v3_8.html `hat3_v8.glb?v=9l`.
Ortam: 33+ ile aynı (`YAMA_IS_KOK` → m8kit / tg; ek değişken yok). cek3geo.py montaj animasyonu v3 ile ORTAK geometri dosyasıdır (scratchpad gece2/cekmece3 ile aynı).

## ADIM 45 · ACİL STOP BUTONLARI KALDIRILDI (4 Eki 2026 · Claude · Kemal: "kaldır, tek tuş koyduk ana şeye")

| # | betik | girdi → çıktı | ne yapar | doğrulama |
|---|---|---|---|---|
| 45 | `45_acil_stop_kaldir.py` | v9l (+ v9g) → v9m | adım 40'ın 6 Schneider XB4BS8442 butonu (TOPPING, B, F, K, E, QR servis yüzü) tamamen kalkar: ACIL_STOP__sari / __siyah / __kirmizi düğümleri + ağ + malzeme silinir (sahne / animasyon indisleri yeniden numaralanır) · adım 40'ın kapak sacı / camı / PU'da açtığı 10 gövde cebi (30 × 30 × 43), adım 40'ın girdisindeki (v9g) aynı bileşenle değiştirilerek KAPANIR (güvenlik: girdi = v9g − cep, hacim farkı = cep hacmi ±0,5 mm³, kutu dışında fark yok — değilse durur) · adım 40 zincirde kalır (41–44 onun çıktı sırasına göre yazılı) | 10 cep kapandı · iki koşu bayt aynı · ON kümesi (kapak / cam / depo) yeni çakışma 0 · mekanizma / parca_kutulari'ndan ACIL_STOP kayıtları silindi |

Zincir doğrulaması: `zincir.py --adim 45 --girdi-dizin <hat3_v9l.glb + hat3_v9g.glb>` (girdi: adım 44 çıkışı + adım 40 girdisi). Sayfa: `meshopt_kucult.mjs hat3_v9m.glb <W>/otonom/hat3d/v3/hat3_v8.glb --idx seq` (5637 bufferView bayt aynı, HATA 0; 101,2 MB) · makine_v3_8.html `?v=9m`.
zincir.py: bir adımın eski çıktısı adım başlamadan silinir (başarısız adım eski dosyayla gizlenmesin).

## ADIM 46–50 · B MODEL AÇIKLARI + A TAMAMLAMA + SIKILAŞTIRMA (4 Eki 2026 · Claude · Kemal: "her şeyi yap")

| # | betik | girdi → çıktı | ne yapar | doğrulama |
|---|---|---|---|---|
| 46 | `46_b_pu_levha.py` | v9m → v9n | B yerinde-köpük PU blokları takılabilir KESİLMİŞ LEVHALARA bölünür (manifold3d, parçaların birleşimi = eski blok → hacim / U / görünmezlik aynı, fark > 1 mm³ ise durur): arka PU yüksek / alçak → z −805'te 2 katman (arka katman flanşlar arası 23,5 · ön katman 13,8) · sol PU → ana levha + arka şerit (dış arka 1 üst flanşı altı) + 3 alt / 3 üst köşe dolgu şeridi (köşebent büküm dış yayı ↔ köşe) · teknik depo arka / sağ PU → ana levha + köşe şeridi (sağ üst köşebent 2 yolu) · taban PU → şase M8 cıvataları üstünde Ø25 boydan boya delik + 10 tapa. Şerit / tapalar yeni düğüm `B_KASA__pu_dolgu` (kesim yüzü ortak üçgenlemeli → ayrı düğümde ayrı kapalı bileşen) | her parça tek kapalı kabuk; ana levha ↔ engelin süpürdüğü hacim ≤ 0,08 mm³ (sayısal); hacim farkı 0,000 mm³ |
| 47 | `47_b_baglanti.py` (+ `veri/bag47.py`) | v9n → v9o | B'de bağlantısı olmayan her parçaya standart bağlantı, karşı tarafta delik / yuva (sac_ent.Karsi.delik_ac): A 12 dikme ayağı (uç plakası + 2 × DIN 929 M5 kaynak somunu + alttan 2 × ISO 4762 M5 × 16 + pul; şase alt duvarında Ø9,5 erişim deliği) · B 8 evaporatör braketi (üst braketlere 20 × 22 duvar kulağı; PEM FHS-M5-8 + pul + somun) · C soğutma grubu 4 ray ucu (ISO 4762 M4 + DIN 433 → M4 kapalı uçlu perçin somun / taban altı somun) · D B elektrik montaj plakası 6 × FHS-M5 · E istasyon kutusu 2 U konsol (M4 × 8 + FHS-M5) · F zincir kanalı 2 L konsol (kör perçin + FHS-M5) · G ışınım sacı 12 × FHS-M4-18 (takoz eksenleri) · H 164 iç kanal bağlantısı (FHS-M4/M3 + pul + somun, kabloya değmeyen konumda; boşluklu kanalda aralık burcu; dar kanalda kelepçe) + 26 B kablo kanalı bağlantısı · J 22 M8 perçin somun kapalı uçlu (+4 mm dolu uç) + şase / kaide M8 cıvataları × 16 · K evaporatör 1 fan kablosu kanal geçiş deliklerinin eksenine (+3,93 y, uçlarda eğimli). Her yerleşim denetlenir: eleman katısı yalnız deldiği parçalara girer (açık ağlarda üçgen prizma testi), olmazsa sonraki aday | yerleşmeyen 0; yeni düğüm `B_BAGLANTI__paslanmaz` |
| 48 | `48_a_tamamla.py` | v9o → v9p | A montaj animasyonu v3 ajanının betiği (A1 A–B pulu ISO 7092 · A2 açıcı cıvatasına DIN 125 · A3 tabla rayı M6 −5 · A4 açıcı flanşı 120 × 155) + A5 A → TOPPING 4 × M8 × 16 → × 10 (PEM'i geçmesin) + glb_sikistir | A1 cıvata arama aralığı adım 47 (M8 × 16) sonrasına göre |
| 49 | `49_b_ic_kabuk.py` | v9p → v9q | iç saclar mekanik bağlanır: iç taban arka kenarı ↑ arka sacın arkasına (F1) · iç sol duvar alt / arka / üst kenarı gıda tarafına (F4) · bölme sacları alt / arka / üst kenarı 12 mm dışa (F6, engel yerlerinde çentikli) — 15 / 12 mm flanş (sahip sacla birleşik), DIN 7337 Ø4 kör perçin ≈150 mm (213); PU levhada flanş / perçin cebi; açık bölme PU'ları 0,01 mm ızgarada kapatıldı. Tavan ↔ arka flanşı yok (arka PU levhası tavanın üstüne çıkar) | sorun 0 · 1 perçin yeri boş (kanal altında, hattın diğer perçinleri) |
| 50 | `50_sikilastir.py` | v9q → v9r | dejenere (silinmiş) üçgenler + kullanılmayan köşeler atılır, kat / mek / kpk aralıkları taşınır; geometri aynı (köşe koordinatları bayt denetimi) | %30 ölü üçgen atıldı |

Zincir doğrulaması: 45–50 iki ayrı iş klasöründe bayt aynı. Sayfa: `meshopt_kucult.mjs hat3_v9r.glb <W>/otonom/hat3d/v3/hat3_v8.glb --idx seq` · makine_v3_8.html `?v=9r`.

## ADIM 37 v2 · TOPPING GÖVDESİ DÜZELTMELERİ (4 Eki 2026 · Claude · Kemal onayı) — adım 37 artık `h3_topping_sac_v2` çağırır

Üreteç `h3/h3_topping_sac_v2.py` (v1 DEĞİŞMEDİ, üstüne yazılmadı). Zincir 37 → 50 bu üreteçle yeniden koştu (37'den sonraki betikler değişmedi).

| # | değişiklik | nasıl |
|---|---|---|
| D1 | servis sacı 17 havşa vidası | servis sacı + arkadaki dönüş flanşı birlikte **çökertilir (dimple)**, iç içe koni (DIN 7991 baş konisiyle aynı) · dış yüz düz · dönüşteki PEM SP-M5 yerine **kaynak burcu M5 Ø14 × 9** (alt yüzü dimple'a havşalı, 2 punta) · vida DIN 7991 M5 × 6 → **M5 × 12** (ucu burcun arka yüzünde, diş 6,75) |
| D2 | soğuk oda iç sacı | 4 düz sac + TIG YERİNE **bükümlü kenarlı** 4 sac (304 1,0 · iç R 3): sol / sağ arka kenarı arka iç sacın arkasına (raf ve üst raf hizasında kesik), üst kenarı tavan iç sacının üstüne, ön kenarı çerçevenin arkasına · tavan arka kenarı aşağı, ön kenarı yukarı · arka iç sac düz · **48 perçin**: 28 × ISO 15983 Ø3,2 içeriden + 20 × ISO 15984 havşa Ø3,2 çerçeveden (yüzeyle aynı düzlem) · her perçinde **POM-C ısı kesici pul Ø9 × 1** · gıda tarafı 7 köşe silikon fitili + 3 ön derz · PU yerinde köpük DEĞİL: **4 kesilmiş levha** (arka / sol / sağ / tavan; flanş, perçin, pul yuvaları açık) + dış saca 0,5 mm **yapıştırıcı** (eski zincir_T_tamamla T2 artık üreteçte) |
| D3 | evaporatör ayakları | servis sacındaki 4 sekme (v8zq TOPPING_MODUL__sac 87 / 88 / 94 / 95, DEGISEN ile silinir) yerine aynı düzlemde **2,5 mm L ayak** (kaset gövdesine üreticide kaynaklı) → kuru bölme tabanına **ISO 7380 M5 × 6 → PEM SP-M5-1** · servis sacı tek başına sökülür · evaporatör yeri aynı |
| D4 | kondenser kanalı | kuru bölme tabanında Ø32,8 delik yerine **135 × 33 geçiş deliği** (dirsekli boru taban inerken içinden geçer) + **kanal geçiş kapağı** 1,5 (sağdan açık yarık, 2 × ISO 7380 M5 → PEM) |
| T1 | TOPPING → B pulu | DIN 9021 → **ISO 7092 Ø15** (Ø16 servis deliğinden geçer) |

Abkant: yan iç sacların ön kenarı ters büküm → kaz boynu bıçak KABUL (Kemal 4 Eki, h3_topping_sac_v2.DFM_KABUL). Açık PU için raf / üst raf hizasında köşe silikon şeridi (derz_kose_*).
Denetim (topping_sac_denetim_v2, scratchpad gece2/t3/den2): DFM 0 HATA (2 kabul) · açınım 48/48 · zarf 0 · gövde ↔ gövde 0 · gövde ↔ v8zq çakışma 0 · havada 0 · **PU açık nokta 85 (AÇIK MADDE)**: çoğu iç sac R3 büküm arkasındaki gizli boşluk (gıda tarafından görünmez), birkaçı köşe şeridi uçlarında.
Zincir 37–50 v2 ile iki ayrı iş klasöründe BAYT AYNI (gece2/t3/is_A, is_B). Sayfa: meshopt (HATA 0, 102,7 MB) · makine_v3_8.html `?v=9s`.
Montajı engelleyen diğer maddeler model değişikliği İSTEMEDİ (animasyonda çözüldü): kaşar / sucuk çıkış ağzı ve mandal gövdeye ait sabit parça (alttan / yukarıdan), kaset önden dil kanalında sürülür (dil kanalı zaten önden açık yuva) · sos / harç: çıkış borusu + yayıcı alttan kovana, hortum üst raf deliğinden, mevcut kelepçe ile bağlanır · X ekseni parçalı: motor kuru bölme adımında yukarıdan köşeye, raylar + araba A tarafından · raf PU levhası köşebentten önce yukarıdan.

## ADIM 51 · B TAŞIYICI HAYALET DİSK (4 Eki 2026 · Claude · YEREL)

| # | betik | GLB | ne | denetim |
|---|---|---|---|---|
| 51 | `51_b_hayalet_disk.py` | v9r → v9s | B montaj animasyonu v4 'havada' denetimi: B_TASIYICI__celik'te taşıyıcı üst kirişin üst duvarındaki Ø10,95 perçin somun deliklerinin içinde 2 × Ø8 × 2 disk (x 4016,5 · z −570 / −480) hiçbir parçaya değmiyordu (1,475 mm) — delik kesicisinin bıraktığı çekirdek, gerçek parça değil (adım 45'ten önce de vardı). Silinir; 50_sikilastir ile dejenere üçgenler atılır | beklenen tam 2 disk; her biri komşulara > 1 mm (değen disk silinmez, betik durur) |

Zincir doğrulaması: 51 iki ayrı iş klasöründe (girdi gece2/t3/is_A/hat3_v9r.glb = adım 37 v2 zinciri) bayt aynı. Sayfa: `meshopt_kucult.mjs hat3_v9s.glb <W>/otonom/hat3d/v3/hat3_v8.glb --idx seq` · makine_v3_8.html `?v=9t`.

## ADIM 52 · ANA PANO U (ÜST DEPO) İSTASYONUNA AİT (4 Eki 2026 · Claude · YEREL · yalnız etiket)

| # | betik | GLB | ne | denetim |
|---|---|---|---|---|
| 52 | `52_pano_u.py` | v9s → v9t | Kemal: sol menüde "U · Üst depo" gizlenince ana pano açıkta kalıyordu (pano hat geneli 'Elektrik / Ana pano' ünitesindeydi, fiziksel olarak U_F içinde x 3518–3978, y 1867–2176). 'Elektrik/Ana pano' etiketli 327.268 üçgen → **'U/Elektrik'** 327.188 (pano gövdesi, kapak, ana şalter + kol + mil + somun, cihazlar, DIN, kanal, Harting, rakorlar, lastik geçit, kör tapa, pano çıkış kabloları, gömme giriş cebi + arka rakorlar, bina kablosu; panonun arkasındaki dik kanal ELK_IC zaten U/Elektrik) · U arka düzleminin (z −830) gerisindeki 80 üçgen (bina kablosunun makine dışı ucu, 48'i sıfır alanlı) → 'Elektrik/Ana hat'. 'Elektrik/Ana pano' boş → sahne 'mekanizmalar' listesinden çıktı (56 → 55, sonraki indisler −1). 'kat' / 'kpk' / kademe aynı | BIN bayt aynı · mek dışı JSON aynı · ünite başına üçgen sayısı tutar · p_dogrula etiket hatası 0 |

Zincir doğrulaması: 52 iki ayrı iş klasöründe (gece2/b4/52a, 52b; girdi 51a/hat3_v9s.glb) bayt aynı. Sayfa: `meshopt_kucult.mjs hat3_v9t.glb <W>/otonom/hat3d/v3/hat3_v8.glb --idx seq` (5643 bufferView bayt aynı, HATA 0; dogrula.mjs extras aynı) · mekanizma_v3_8.json: liste 55, 75 pano parçası U/Elektrik, birim ELK_ANA_PANO → U/Elektrik, 'Elektrik' istasyon adı "ana hat", U/Elektrik kutusu pano dahil · parca_kutulari.json değişmedi (geometri aynı) · makine_v3_8.html glb + json `?v=9u`.

## ADIM 53 · TOPPING YENİ MENÜ YERLEŞİMİ (menu7 · 4 Eki 2026 · Claude · YEREL · Kemal onayı)

| # | betik | GLB | ne | denetim |
|---|---|---|---|---|
| 53 | `53_menu7.py` | v9t → v9u | Menü pide + lahmacun. **Üniteler:** Harç → **Lahmacun harcı** · YENİ orta UNO → **Kıyma** · Sos → **Patates** (sos yayıcısı patates yayıcısı, yalnız ad) · alt Kıyma → **Tavuk** · Kuşbaşı · Kaşar · Sucuk (liste 55 → 56, sonraki indisler +1). **3. UNO** x 2031: sos UNO'sunun birebir kopyası (statik parçalar kopya, VALF / PISTON hareketli düğümleri yeni `…_KIYMA_ORTA` düğümleri, animasyonsuz) · hazne 200 × 440, üst 2099 · çıkış: paslanmaz dirsek Ø35,6 × 1,8 (+z → −x R50, −x → −y R36, rafın üstünde) → x 1911,5 z −170 dik D32 hortum (sos hortumu kopyası) → hortum ucu + boru Ø29,8 (y 1048'e) · yeni düşme kovanı: raf deliği (conta dış zarfı) + raf contası, soğuk oda tabanı Ø37 / PU Ø38 / alt sac Ø31 + kovan sacı + taban contası · soğuk oda arka iç sacında burç deliği r 15,25 · burç kılıfı (üfleme ağzında, ayaklı) · 2 yeni ada rakoru + 2 Ø6 hava hortumu (x 2124 → z −678 / −668 → x 2302 → 1850 → cebe). **Sağ evaporatör cebi** x 1973–2089, y ≥ 1568 (serpantin ≤ 1565 dokunulmadı): kaset sacı / PU / iç kutu / fan tabanı / ayırma sacı / ön conta kesildi; cep: bükümlü sac 1 + PU 20 (taban 10) + üst kapak, ön conta 10; silindir tutucu + ara plaka cep tabanına (1580–1594,6). **Hazneler (5):** Ø64 boyun ↔ üst kesit dışbükey zarfı (açınımlı geçiş), dikey köşe R25, et 1,5 · harç üstü 2099 → 2129 (tavan 2140) · kuşbaşı ön-sağ köşe cebi (x ≥ 1879,1 · z ≥ −201) | çakışma (govde_denetim_dogru, TOPPING @degisen): yeni 0 — kalanlar ya tabanda da var (kesilen gövde sacının uzak temasları, evaporatör ↔ bakır OCC 0) ya sos UNO modelinden devralınan iç geçmeler (aktüatör ↔ vana, vana 1 ↔ 2, flanş 10 ↔ 16; kaynakta aynı hacim) · havada 0 (108 değişen bileşen) · silindir ↔ cep sacı 14,6 mm · etiket hatası 0 · hazne iç hacmi: harç 51,2 · kıyma 24,6 · patates 16,9 · tavuk 9,0 · kuşbaşı 8,7 L |

Zincir doğrulaması: 53 iki ayrı iş klasöründe (gece2/menu7/z53A, z53B; girdi b4/52a/hat3_v9t.glb) bayt aynı. Sayfa: `meshopt_kucult.mjs hat3_v9u.glb <W>/otonom/hat3d/v3/hat3_v8.glb --idx seq` (5655 bv bayt aynı, HATA 0; dogrula.mjs extras aynı) · mekanizma_v3_8.json: liste 56 (yeni adlar), parça değerleri yeniden adlandı + orta UNO parçaları, TOPPING ünite kutuları yeniden · parca_kutulari.json: 4 hazne kutusu + 5 yeni parça · makine_v3_8.html glb / json `?v=9v`. topping-montaj animasyonu YENİDEN ÜRETİLMEDİ (eski menü); GLB'deki sipariş animasyonları eski menü (pizza / sos dahil) — yeni orta UNO animasyonsuz.

## ADIM 54 · KUŞBAŞI HUNİSİ TAM DİK KENAR (4 Eki 2026 · Claude · YEREL · Kemal: "o aralık boş olmalı; UNO haznesini arkaya doğru DÜZ yap, pipe aşağıya insin")

| # | betik | GLB | ne | denetim |
|---|---|---|---|---|
| 54 | `54_kusbasi_dik.py` | v9u → v9v | adım 53'ün cepli kuşbaşı hunisi (ön-sağ köşe cebi, kıyma hortumunu iki yandan sarıyordu) silinir; yerine EKSANTRİK huni: sağ (hortum tarafı) duvar önden arkaya tam boy düz düzlem **x 1880** (Ø64 boyun dış yüzüne teğet → boyundan üst kenara tek düz yüz) · sol / ön / arka / üst, boyun, R25 dikey köşe, et 1,5 aynı · etiket eski hazneden · 50_sikilastir | iç hacim 6,27 L brüt / 5,64 L kullanılabilir (2 gün ihtiyacı 3,4 L ✓) · yerinde en kısa boşluk (örnek nokta → yüzey): huni ↔ kıyma hortum hattı **10,65 mm**, UNO gövde / vana ↔ hortum hattı 36,4, huni ↔ kaşar 68,5 · süpürme (izdüşüm 0,25 mm ızgara): **huni öne ve yukarı (raf altına) TEMAS YOK** (2B boşluk 10,75) · **UNO gövdesi (vana bloğu 1889, TC kelepçe 1893,5, döner vana tahrik ucu 1891–1916) öne çekilirken kıyma düşme hattının alt hortum ucu / kelepçesine (x ≥ 1886,7, y 1182–1216) ÇARPAR** — kuşbaşı UNO gövdesi 159 mm geniş (1757–1916), harç hattı (≤ 1746,8) ile kıyma hattı (≥ 1886,7) arası 140 mm: hortum yeri sabitken gövde ancak kıyma hortumu kelepçesinden sökülünce çıkar (kb_supurme.py, scratchpad gece2/k3_uyum) |

Zincir doğrulaması: 54 iki ayrı iş klasöründe (gece2/k3_uyum/z54A, z54B; girdi menu7/is53a/hat3_v9u.glb) bayt aynı. Sayfa: `meshopt_kucult.mjs hat3_v9v.glb <W>/otonom/hat3d/v3/hat3_v8.glb --idx seq` (5655 bv bayt aynı, HATA 0; dogrula.mjs extras aynı) · mekanizma_v3_8.json TOPPING/Kuşbaşı kutusu (x üst 1943 → 1916) · parca_kutulari.json kusbasi_hazne_bizim (x 1753–1880) · makine_v3_8.html `?v=9w`.

## ADIM 55 · STANDART UYUM — PUL TEK STANDART (4 Eki 2026 · Claude · YEREL · KUYRUK 3 iş 1)

Uyum denetimi (scratchpad gece2/k3_uyum/RAPOR.md: 7 üreteç kurulup döküldü + model ölçüldü) · standart tek kaynak **`sac_standart/sac_uyum_v1.json`** (yeni; v1 standart / kararlar dosyaları değişmedi → montaj v7 ve zincir 33–38 bayt aynılığı korunur). Kalınlık / R / köşe / arayüz farkları raporda (çoğu işlevli ya da Kemal onaylı; 3 kalınlık + 2 bağlantı önerisi sonraki üreteç sürümüne). Modelde düzeltilen: gereksiz pul çeşitliliği.

| # | betik | GLB | ne | denetim |
|---|---|---|---|---|
| 55 | `55_uyum.py` (+ `sac_standart/sac_uyum_v1.json` 'pul') | v9v → v9w | **M5:** DIN 9021 Ø15 × 1,2 → ISO 7089 Ø10 × 1,0 (A 35 · K 32 · E 28 = 95; FHP / vida + ISO 10511 somun — somun 0,2 mm sac tarafına) · **M8:** DIN 9021 Ø24 × 2 → ISO 7092 Ø15 × 1,6 (A→TOPPING 4 · TOPPING→F 4 · B şase 10; cıvata 0,4 mm sac tarafına) + DIN 125 Ø16 → ISO 7092 (A açıcı flanşı 4 · U_F 6; kalınlık aynı). Pul köşeleri radyal + eksenel ölçeklenir (oturma yüzü sabit, iç Ø aynı); somun = pula değen, boyu ≤ 1,15 × ISO 10511 (perçin somun / PEM somun sayılmaz), yoksa pulu geçen cıvatanın kısa yanı baş. Beklenen sayılar tutmazsa durur | iki koşu bayt aynı (gece2/k3_uyum/z55A, z55B; girdi z54A/hat3_v9v.glb) · tam model çakışma (c8a, v9v taban ↔ v9w): YENİ 0, KALKAN 0 (1063 = gerçek 74 · kasıtlı 804 · şüpheli 185 aynı) |

Sayfa: `meshopt_kucult.mjs hat3_v9w.glb <W>/otonom/hat3d/v3/hat3_v8.glb --idx seq` (5655 bv bayt aynı, HATA 0; dogrula.mjs extras aynı) · makine_v3_8.html `?v=9x` · json'lar değişmedi (kutu / parça değişikliği 0,4 mm altında, pul parça kutusu kaydı yok).

## ADIM 56 · SOL EVAPORATÖR 2. AYAĞI 3 mm DAR (5 Eki 2026 · Claude · bulut oturumu · KUYRUK 3 iş 2 TOPPING montaj animasyonu)

| # | betik | GLB | ne | denetim |
|---|---|---|---|---|
| 56 | `56_evap_ayak.py` | v9w → v9x | TOPPING montaj v5 yol denetimi: tavuk UNO silindiri (arka grup) arkadan, mili burçtan pistona en az 179 mm eksenel girer; duvar flanşı (x 1570–1622) bu sırada sol evaporatörün 2. ayağının dik kolundan (x 1620–1650, z −828,5…−826) geçer → 2,0 mm çakışma. Sıra ile çözülmez (evaporatör yalnız yukarıdan, tavan kapanmadan; silindir UNO gövdesinden sonra). Ayak (2,5 L, kasete kaynaklı) sol kenarı x 1620 → 1623: genişlik 30 → 27, vida deliği (x 1641) ve somun yerinde, kenar mesafesi 13 mm, flanş ↔ ayak 1,0 mm. Yalnız uç yüzün 228 köşesi taşındı; 50_sikilastir | iki koşu bayt aynı (bulut: /home/user/is/z56A, z56B; girdi hat3_v9w.glb SHA256 346fd567…) · çıktı SHA256 83d54bbb… · yalnız malzeme çıkarıldı (yeni çakışma olamaz) |

Sayfa: meshopt kopyası Codex yayınında (hat3_v8.glb 100 MB üstü, GitHub'a girmez) · TOPPING montaj v5 bu modelle üretildi.

## ADIM 57 · SERVİS SACI KABLO KANALI AYAK HİZALARINDAN KESİK (5 Eki 2026 · Claude · bulut oturumu · Kemal: "kablo kanalını en mantıklısını yap")

| # | betik | GLB | ne | denetim |
|---|---|---|---|---|
| 57 | `57_kanal_kesik.py` | v9x → v9y | Servis sacına 3 braketle bağlı yatay kablo kanalı (x 1470–2400, y 1240–1270, z −798…−768) dört evaporatör ayağının dik kolunun önünden geçiyordu; servis sacı arkadan kapanırken / bakımda çıkarken kanal ayakların içinden geçmek zorundaydı (TOPPING montaj v5: 26–28 üçgen gerçek kesişim). Kanal ayak hizalarından 2 mm boşlukla kesildi → 4 parça [1496–1621] (braket 1495–1505) · [1652–1776] (dik kanal 1671–1701'e bağlı) · [1810–2171] (braket 1945–1955) · [2205–2400] (braket 2325–2335). Kablolar aralıklardan geçer; servis sacı yine tek parça sökülür. Kesilen bölümdeki boş rakor (kablosu yok) 1476 → 1608. manifold3d boolean, etiket korunur, 50_sikilastir | iki koşu bayt aynı (bulut /home/user/is/z57A, z57B) · çıktı SHA256 49fc7520… · yalnız malzeme çıkarıldı + boş rakor ötelendi |

## ADIM 58 · TEK ACİL STOP — ŞALTERİN ÖNÜNDEKİ KAPAKTA (5 Eki 2026 · Claude · bulut oturumu · Kemal: "tek bir acil butonu, o da şalterin önündeki kapakta", "küçük olsun")

| # | betik | GLB | ne | denetim |
|---|---|---|---|---|
| 58 | `58_acil_stop.py` | v9y → v9z | Adım 45'te kaldırılan 6 butonun yerine TEK buton (STANDART_DURUM.md madde 1). Ana şalter kolu U_F pano kapağında (x 3590–3782, y 2070–2147, z −91…−53); önündeki kapak = F sağ üst kapağı (KAPAK_F_SAG, altta menteşeli). Buton merkezi (3625, 1600, ön yüz z 79) — panjur yarıkları ve omegalar arasında, yerden 1,60 m. Schneider XB4BS8442 Ø40 mantar + ZBY9330T Ø60 sarı etiket diski + ZB4BZ102 gövde (30 × 30 × 43, kapak arkası). Yeni düğümler ACIL_STOP__sari / __siyah / __kirmizi **__KAPAK_F_SAG** (kat 6 Elektrik · mek 23 F/Elektrik · hepsi kpk: kapakla döner). Kapak sacında gövde cebi (−1350 mm³ = 30 × 30 × 1,5; Ø60 etiket önden örter). Kablo çizilmedi (menteşe tarafından esnek döngü → F kutusu → güvenlik devresi; şema sonra). | iki koşu (z58A, z58B) bayt aynı · SHA256 94dccd07… · kapak arkası z 16–77,5 bu noktada boş (yalnız kapak sacı) · görsel `_local/claude_son_yerel/adim58_acil_stop.png` |

## ADIM 59 · KAPI EMNİYET ANAHTARLARI (5 Eki 2026 · Claude · bulut oturumu · STANDART_DURUM.md madde 3, Kemal: "yapalım")

| # | betik | GLB | ne | denetim |
|---|---|---|---|---|
| 59 | `59_kapi_emniyet.py` | v9z → v10a | 10 ön kapak (A · TOPPING K1 / K2 · F sol / sağ üst · K · E üst sol / sağ · alt sol / sağ) için kapak arkasında, mandal tarafında emniyet anahtarı: Schmersal RSS36 RFID kodlu sensör (≈ 25 × 72 × 18, gövdeye) + RST36 aktüatör (≈ 25 × 72 × 12, kapağın iç yüzüne, kapakla döner · kpk) · 3 mm aralık. K (pnömatik yıldız bıçak): KİLİTLİ Schmersal AZM40 (≈ 40 × 120 × 20). Sensör sabit parçaya > 1 mm uzaksa 2 mm paslanmaz braket (F sol / sağ 6 mm → U_F gövde sacı; E alt sol 4 mm; E üst / alt sağ 1 mm). Yerler model ağında arandı (aktüatör + sensör + braket hacmi boş). Yeni düğümler EMNIYET__sari (sensör) · EMNIYET__siyah (+ __KAPAK_F_SOL / __KAPAK_F_SAG: F kapak aktüatörleri) · EMNIYET__paslanmaz (braket) · kat 3 Sensör · mek istasyonun Elektrik ünitesi (A: A/Gövde). Ölçüler yaklaşık (katalog teyidi açık). Kablo çizilmedi. | iki koşu (z59A, z59B) bayt aynı · SHA256 bf2d65b6… · bütün kutular boş (betik içinde denetim) · görsel `_local/claude_son_yerel/adim59_kapi_emniyet.png` |

## ADIM 60 · HAVA HATTI EMNİYET VALFİ (5 Eki 2026 · Claude · bulut oturumu · STANDART_DURUM.md madde 8)

| # | betik | GLB | ne | denetim |
|---|---|---|---|---|
| 60 | `60_hava_emniyet.py` | v10a → v10b | Bütün istasyonların havası kompresör çıkışından tek hortumla gider → hortumun düz bölümüne (x 3549 · y 1809 ekseni, z −700…−610) Festo MS6-SV-E emniyetli yumuşak başlatma + hızlı boşaltma valfi (≈ 62 × 62 × 90) + bobin / M12 (−x) + susturucu (+y). Enerji kesilince / acil stopta / kapı açılınca hat boşalır, yeniden verilince yumuşak dolar (EN ISO 4414). Hortum kesiti aynı iki parçaya bölündü (−740…−700, −610…−437). Bakım kilitleme ana şalterle (3 asma kilit); kompresör tankı kendi musluğuyla boşaltılır (kılavuz). Yeni düğümler HAVA_EMNIYET__aluminyum / __siyah (kat 4 Hava · mek 24 F/Hava). Ölçüler yaklaşık. | iki koşu (z60A, z60B) bayt aynı · SHA256 7d6b4595… · valf / bobin / susturucu hacmi boş (betik içinde denetim) |

## ADIM 61 · DAVLUMBAZ YAĞ FİLTRESİ PİZZA KUTUSU TARAFINDAN ALINIR (5 Eki 2026 · Claude · bulut oturumu · Kemal: "pide kutuları istifli, oradan ulaşsa")

| # | betik | GLB | ne | denetim |
|---|---|---|---|---|
| 61 | `61_filtre_servis.py` | v10b → v10c | EN 16282 yağ + karbon filtresi (x 3420–3920 · y 1363–1763) önündeki kompresör / yağ tankı yüzünden haftalık yıkamaya alınamıyordu. (1) Filtre çerçevesi (ağı T-birleşimli, kapalı değil) aynı ölçülerle temiz U olarak yeniden kuruldu: sol kenarı açık, 2 alt M5 deliği korunur. (2) Ray uzantısı 304 3 mm x 2790–3385 (alt / üst plaka + arka dudak; ön kılavuz bölme sacı). (3) Bölme sacında servis ağzı x 2790–3320 · y 1352–1772 (530 × 420) — pizza kutu stoğunun arkasında, kompresör bölmesinin dikey ara sacının (x 3325,5) solunda; 1,5 mm tava tapa (20 derin) + 2 Southco E5 sınıfı çeyrek tur KAM kilit (tapayla çıkar, ağızda sabit dil yok). (4) Adım 34'ün 2 M5 arayüz saplaması (y 1563) filtrenin içine 10,5 mm giriyordu (eski çakışma) → çerçevenin üst kenarına (y 1770,5); bölmede eski delikler kapandı, yeni Ø5 delik, çerçevede Ø5,5. Haftalık: kutular çıkar → 2 kilit → tapa → filtre 615 mm sola (x 2805–3305) → öne → MEIKO. Yeni düğümler F_DAVLUMBAZ_RAY__paslanmaz (mek 22) · F_UST_KABIN_TAPA__sac / __siyah (mek 19). | iki koşu (z61A, z61B) bayt aynı · SHA256 948b20c4… · kayma yolu (x 2805–3920) yalnız filtre + tapanın kamı (tapayla çıkar) · öne çekiş yolu yalnız kutu stoğu + tapa · eski saplama yerinde yalnız sıfır alanlı (silinmiş) üçgenler · görsel `_local/claude_son_yerel/adim61_filtre_servis.png` |

## ADIM 62 · TOPPING BAĞLANTISIZ SACLARA KAYNAK (5 Eki 2026 · Claude · bulut oturumu · TOPPING montaj v6, KURALLAR §2.3 kural 10)

| # | betik | GLB | ne | denetim |
|---|---|---|---|---|
| 62 | `62_topping_kaynak.py` | v10c → v10d | "Bağlı mı" denetiminin bulduğu, yalnız dayanan 9 sac fabrikada TIG 141 (ER308LSi, a ≈ 2) ile bağlandı — 23 dikiş: 4 raf köşebendi → yan astar (üstler alt kenar boyunca 502 mm, altlar ön + arka uçta dikey; gıda bölgesi: sürekli, taşlanır + pasive; raflar köşebentlere oturur, yıkamak için kalkar) · 2 kaide cep taşıyıcısı → enine lama / enine boru (iki uçta dik kol + yatay kol altı) · kaide enine laması → arka boru (sağ yüz; sol yüzde emiş filtresi) + ön perde (iki yüz) · ayırma perdesi + teknik sağ perde → dış taban (sol yüzde 3 × 40 mm; tabanın altında kaide plakası → perçin kuyruğuna yer yok). Yeni düğümler TOPPING_GOVDE__kaynak / KAIDE_C__kaynak (kat 0 · mek 7). | iki koşu (z62A, z62B) bayt aynı · SHA256 83f43eaa… · 23 dikiş hacminin hepsi boş (betik içinde denetim) |

## ADIM 63 · TOPPING UNO'LAR RAFA VİDALI · KASETLER KAPAK TAKOZUYLA KİLİTLİ (5 Eki 2026 · Claude · bulut oturumu · Kemal)

| # | betik | GLB | ne | denetim |
|---|---|---|---|---|
| 63 | `63_uno_kaset.py` | v10d → v10e | Hazır ürünlere dokunmadan bağlantı. **UNO (5):** rafa oturan taban = 82 × 82 dozaj gövdesi bloğu (z −428…−346; üstünde gövde her yana ~50 mm taşar → yukarıdan basılamaz) → iki yanında rafa TIG'li 3 mm L pabuç (ayak 25 × 30, dik kol 12) + 1 × ISO 4762 M5 × 12 + ISO 7089 pul yandan UNO tabanındaki M5 dişli deliğe (UNO siparişinde istenir); sökme 2 vida, rafta somun / açık diş yok. **Kaset (kaşar, sucuk):** yan kanal + arka dayama yerine oturtur; kapak K2 iç yüzünde kasetin 1 mm önünde POM-C takoz 40 × 40 × 14 (kpk) → kapak kapanınca kaset kilitli, tam oturmamışsa kapak kapanmaz → kapak emniyet anahtarı (adım 59) makineyi başlatmaz; kasette değişiklik yok. Yeni düğümler TOPPING_UNO_PABUC__paslanmaz / __kaynak / __vida · TOPPING_KASET_TAKOZ__pom. | iki koşu (z63A, z63B) bayt aynı · SHA256 581de6a7… · 10 vidanın hepsi UNO tabanını deler (betik durdurur) · pabuç / pul / kaynak / takoz hacmi boş · görsel `_local/claude_son_yerel/adim63_uno_kaset.png` |

## ADIM 64 · TOPPING HAZIR ÜRÜNLER BİZİM BRAKETLE BAĞLI (5 Eki 2026 · Claude · bulut oturumu · Kemal: "a, bir daha sorma")

| # | betik | GLB | ne | denetim |
|---|---|---|---|---|
| 64 | `64_hazir_baglanti.py` | v10e → v10f | Hazır ürünlere dokunmadan, bizim parçalarla bağlantı (KURALLAR §3): **kaset motorları** (flanşı gövdeden 3 mm büyük → vida yeri yok) gövdenin iki yanında soğuk oda arka dış sacına kaynaklı 3 mm L braket + ayrı dolgu takozu (montajda motor geldikten sonra), 1 × M5 × 16 yandan gövdeye (4 braket) · **valf adası** (havada duruyordu; önü ile duvar arası 30 mm boş) 2 Z braket: duvara kaynaklı, M5 × 12 valfin ön yüzüne · **X ekseni** ray tabanının arka (z −415) + ön (z −5) duvarına 2 + 2 tabana kaynaklı L pabuç, M5 × 10 → tabandaki M5 perçin somuna · **gizli menteşeler** yan sacta gömme başlı PEM FHS-M4 saplama × 2 (menteşe gövdesinden geçer, içte pul + fiberli somun) · **X sensör braketleri** alt saca preslenmiş PEM FHS-M3 saplama. Ürün siparişlerine "N × M5 dişli delik" notu. **Bağlanmayanlar (bilerek):** orta kayıt (dikme + POM takoz, model verisinde kapakla döner → kanadın parçası) · bas-aç mandalları (çerçeve deliğine geçme, kendi somunu) · X motoru (ünitenin parçası). **AÇIK:** kıyma silindirinin halka duvar flanşı (evaporatör cebinde, üretici çizimi gerek) · iç elektrik kanalları / 2 çelik braket / 1 rakor 1–10 mm havada (kuyruk 10 elektrik işiyle). Yan sacın açık ağında saplama deliği açılamadı (gömme baş yüzeyde, hacim < 0,1 cm³). | iki koşu (z64A, z64B) bayt aynı · SHA256 c15c23e8… · braket / pul / somun / kaynak hacmi parça parça boş · her vida / saplama ürünü deler · bağlanan bileşenlerin hiçbiri kapakla dönmüyor (kpk) |
| 65 | `65_kanal_daralt.py` | v10f → v10g | TOPPING montaj v6 sıra denetimi: servis sacı alt montajı (tezgâhta) arkadan girerken yatay kablo kanalı (ELK_TOPPING__kanal x 2205–2400 · y 1240–1270 · z −798…−768) sucuk motoru sensörünün (y 1265,5–1290,5 · z −812…−802; sac ile kanal arasındaki boşlukta) içinden geçiyordu; kanalın altında motor gövdesi → aşağı inemez. Kanal 25 mm (alt kenar sabit, y 1240–1265; kesit y'de 25/30) → sensörle 0,5 mm boşluk, servis sacı düz girer. Sağ uçtaki T kutusu (x 2400–2419,5) 30 mm kalır. | iki koşu (z65A, z65B) bayt aynı · SHA256 a0658609… · bileşen beklenen kutuda · yeni üst kenar ≤ 1265 |
| 66 | `66_emniyet_braket.py` | v10g → v10h | Bağlantı denetimi (kural 10): adım 59'un TOPPING K1 / K2 emniyet sensörleri (RSS36) dış tabanın üstünde vidasız duruyordu. Her sensörün arkasında 2 mm AISI 304 L braket (dik kol z 4–6, ayak tabanda arkaya z −2…4, ayağın arka kenarı tabana TIG 21 mm), dik kolda 2 × PEM S-M4-2; sensör önden kendi montaj deliklerinden 2 × ISO 4762 M4 × 20 (baş gömme yuvada; aktüatör 3 mm önde). Düğümler TOPPING_EMNIYET_BRAKET__paslanmaz / __kaynak / __vida. | iki koşu (z66A, z66B) bayt aynı · SHA256 79dea4ee… · braket / kaynak / somun hacmi boş · 4 vidanın hepsi sensörü deler |
| 67 | `67_f_arka_civata.py` | v10h → v10i | F montaj v2 sıra denetimi: F üst kabin saplamaları üç sacda üç eksende (yan → tavan x · tavan → arka y · arka → yan z) — hangi sırayla takılırsa takılsın bir sac saplamayı eksenine dik süpürüyordu. Arka ↔ yanlar (5 + 5) ve arka ↔ köşebent (1) preslenmiş saplama yerine dıştan ISO 7380-1 M5 × 10 bombe başlı cıvata (baş arka dış yüzde, içte pul + somun aynı); arka sacın üst dönüşündeki 8 tavan saplaması deliği öne açık yarık (5,5 × 9,5). Sıra: yan sol → tavan / köşebent / bölme (−x) → davlumbaz (+z) → arka (+z) → yan sağ (−x). Düğüm F_UST_KABIN_BAG__vida. | iki koşu (z67A, z67B) bayt aynı · SHA256 a733c1ae… · 11 saplama beklenen kutuda bulunup silindi · cıvata başı hacmi boş · yarık hacmi 452 mm³ |
