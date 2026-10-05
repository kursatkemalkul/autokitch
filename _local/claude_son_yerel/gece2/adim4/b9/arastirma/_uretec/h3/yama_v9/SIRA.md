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
