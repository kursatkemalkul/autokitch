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
