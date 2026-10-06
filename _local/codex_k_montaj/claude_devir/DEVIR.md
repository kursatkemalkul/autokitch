# K MONTAJ — CLAUDE DEVİR FORMU

**Kemal'in son talimatı:** K'nin kalanını Claude tamamlasın. Codex'in son çalışma yeri, model ve denetimleri korunup devredilsin.

| Alan | Güncel durum |
|---|---|
| Dal | `codex/k-montaj` |
| Yerel çalışma | `AUTOKITCH_COORDINATION/worktrees/codex-k-montaj-v3` |
| Son MODEL | Bu klasördeki `hat3_v10ze.glb.gz`; ana modele henüz alınmayan K prototipidir |
| Açılmış model SHA256 | `9ce8fdfd34ead660b71ef13660bacb7d451848747e6b4ace648af441c4ab7158` |
| Son plan | `_local/codex_k_montaj/k1/plan_k_clip_full.pkl` — paketten geri yüklenir |
| Plan SHA256 (devirden önce) | `eeceddad3ee1f1972e97d799573ef4ea75b797d25d37dc620ea08e6a530f0a5d` |
| Parçalar | 1.037; adları ve gerçek üçgenleri devam paketinde |
| Montaj süresi | 867,645 s; 30 tezgâh grubu |
| Kalan bağlantı kaydı | **199**; tek tek listesi `../k1/clip_join_evidence.json` → `remaining_unresolved` |
| Yayın | **Yapılmadı. Üretim ve bağlantı son kapıları geçmedi.** |
| U üst raf | Başlamadı. K tamamen bittikten sonra ele alınacak |

## Başlangıç: önce bu noktayı aç, eski çalışmayı yeniden kurma

Bu devir formunun bulunduğu commit'i `codex/k-montaj` dalından al. `KURALLAR.md`, güncel main'deki `KOORDINASYON.md` ve `AUTOKITCH_COORDINATION/CLAUDE_BASLA.md` okunmalı. Diğer ajanın F/TOPPING işlerine dokunma. K'nın bu dalını bulutta ayrı çalışma ağacında aç; kendi devam işini sahiplen. Zincir değişikliğini birleştirmeden önce güncel zincir kilidini al.

Repo kökünde:

```text
python _local/codex_k_montaj/devir_paket.py --restore
```

Bu komut `devam_verisi.zip` içindeki JSON/NumPy verisini açar ve yalnız kendi K çalışma klasörüne üç cache'i yazar:

- `k1/plan_k_clip_full.pkl`: tüm montaj planı, hareketler, üretim kareleri, geçici destekler, kaynak işlemleri.
- `k1/k_parca_clip_verified.pkl`: 1.037 parçanın tam adlandırılmış gerçek model üçgenleri.
- `k1/k_bil_clip.pkl`: büyük modelin bir kez çıkarılmış K + çevre bileşenleri. Büyük GLB'yi model değişmedikçe yeniden okuma.
- `electrical_clip_weld_candidate/A/hat3_v10ze.glb`: tam son prototip.

**Önemli:** JSON/NumPy paketinin açılıp kapanması bütün veriler için birebir eşitlikle doğrulandı. Python/NumPy sürümü, nesne paylaşımı ve pickle serileştirmesi nedeniyle geri yüklenen `.pkl` dosyasının BAYT SHA'sı değişebilir. Geometri ve hareketin değiştiği anlamına gelmez. Eski denetim JSON'larını yeni SHA ile sessizce düzenleyip geçmiş sayma: önce `k_son_kaynak.py`'yi mevcut `clip` dosyalarına uyarlayıp kaynak üçgenlerini yeniden bağla, sonra değişen dosya/hash bağımlılıklarını yeniden doğrula. `restore_receipt.json` eski/yeni hashleri ayırır. Üretim kapıları kendiliğinden açılmaz.

## Tamamlanan ve kanıtı bulunan işler

1. Kaynak bileşenlerini bir kez okuyan, yüzeyleri parça adlarına tam eşleyen v6 altyapısı uyarlandı. Son kaynakta **785.552 üçgenin tamamı** eşleşti; belirsiz/yitirilmiş üçgen 0. `clip_ownership_rebind_audit.json` ve `clip_plan_source_binding_audit.json`.
2. 30 tezgâh grubu ve K istasyon sırası kuruldu. Son başlık planında PLAN SORUNU 0, yerleştirilmemiş parça 0. Ortak TOPPING v6 oynatıcı değişmedi.
3. Dört profil tapasının gerçek sürekli, taşlanmış kaynak işlemi plana bağlandı; yalnız görüntüden kaynak çıkarımı yapılmadı.
4. Kesici kafası: kaynak 8/10 mm plakalar izinli **6+2 / 6+4 mm** stok katmanlarına ayrıldı; dış çizgi ve kesme kotu korundu. Üç alt DIN7991 M8×20, dört üst DIN7991 M8×25, üç çevresel dikme kaynağı. Vida boyu, diş tutuşu, kör dip payı ve anahtar yolları ölçüldü. `head_join_evidence.json` ve kafa adayının JSON'ları.
5. Kafa grubu tezgâhtan makineye gelirken silindiri kesen eski düşey yol düzeltildi: önce ön taraftaki boş alanda alçalıyor, ardından alttan yerine giriyor. Alt kaset ve üst ara plaka için destek uyarıları ve gerçek vida tamamlama anına bağlı bırakma olayları var. **Fikstür geometrisi son denetimi hâlâ açık.**
6. Tam kafa+K rijit hareket denetimi: **18.513 parça çifti, çarpışma 0**. `full_ccd_plan_k_head_full.json`. Uyarı metni eklenen planın aynı geometrisi/hareketleri birebir doğrulanarak sonuç devralındı: `head_support_motion_inheritance.json`.
7. Dört kendi kablo kelepçesinin ayağı şasemize **16 gerçek çevresel TIG dikişiyle** bağlandı. 32 kaynak-taşıyıcı teması doğrulandı; 16 torç zarfı geçti. Dikişler 467,478–477,078 s arası; ilk ilgili kablo 848,245 s'de gelir. Destek uyarıları var, kablo takılmadan sabitlenir. `clip_join_evidence.json`, `electrical_clip_weld_candidate/torch_access_audit.json`.
8. Yeni kaynaklar için tüm sahneye karşı ek denetim: **16.456 çift değerlendirildi, 213 hareket çifti test edildi, çarpışma 0**. Eski 1.021 parçanın geometri/hareket/istisnaları aynı olduğundan eski tam denetim korunuyor. `clip_delta_ccd.json`. Bu sonuç üretilebilirlik ve fikstür denetimi değildir.
9. Son prototip A/B iki koşuda bayt aynı: model SHA yukarıda. `electrical_clip_weld_candidate/A/hat3_v10ze.json` ve B kaydı.

## Kalan iş: Claude'un yapacağı

**Kesin açık liste:** `k1/clip_join_evidence.json` / `remaining_unresolved`. Sayaç bir mühendislik kaydıdır; 199 ayrı yeni tasarım anlamına gelmez. Hazır ürünün kendi parçaları ancak gerçek montaj arayüzü/klips/diş/conta kanıtıyla sınıflandırılabilir; hepsini topluca 'hazır ürün' diye kapatma.

| Aile | Açık kayıt |
|---|---:|
| Elektrik, kanallar, cihazlar | 67 |
| İtici | 39 |
| Gövde, çit, ürün sensörü | 27 |
| Yağ, sprey, tartı | 24 |
| Hava, silindir | 21 |
| Bıçak, koruma | 14 |
| Bant | 7 |

Önerilen sıradaki somut iş: bıçak/koruma grubunu birlikte çöz. Henüz bu aile için yeni geometri yazılmadı. Kaynak tanımı `kesme_cad_v4.py`/v2, `kesme_cad_v8.py` ve mevcut parça cache'inden bulunabiliyor:

- Alt bıçak ağzı **y=1121,5**; kapandığında y=996,5. Bir taşıyıcı ekleyip bıçakları aşağı kaydırma: bant y=996 olduğu için kesme geometrisi bozulur.
- Alt kafa plakası 6+2 mm, y=1166,5–1174,5; üst adaptör 6+4 mm, y=1244,5–1254,5.
- Altı bıçak 1,5 mm; göbek halkası, altı eski koruma braketi ve koruma halkasının gerçek bağlantıları açık. Eski koruma braketleri 8 mm ve kafa ile örtüşüyor; kalınlık/bağlantı arayüzünü beraber çözmek gerekiyor.
- Üç eski 'kelebek somun' proxy'sinde gerçek karşı saplama/diş yok; üç silindir görüntüsünü bağlantı kanıtı sayma.
- Yeni kelepçe çözümü satın alınmış silindire kaynak/delik açmıyor. Silindir üstündeki ve destek yüzeyi olmayan diğer kelepçeler hâlâ açık; kendi basit desteğine taşı.
- Yüzeye oturan cihaz/kanal için gerçek vida, klips veya kaynak gerekir. DIN rayına geometrik temas tek başına kilit kanıtı değildir.
- Üç eski kaynakta iki taşıyıcı teması eksik: `onyuz_kapak_K_kose_kaynagi_3`, `taban_sac_tasiyici_20_kovan_kaynagi_480`, `...570`; son denetimde çöz.

## Açık üretim/yayın kapıları — atlanmayacak

- `manufacturing_release_audit.json` ve `connection_release_audit.json` **henüz yok/geçmedi**. `k_cikti.py` bunlar mevcut model ve plan SHA'sına bağlı, passed ve open_items=[] olmadan çıktı yayınlamayı engeller. Bu korumayı kaldırma.
- 119 fiziksel sacın kapalı ağ kontrolü geçti; bu, bütün bükümlerin abkantta üretilebilirliği demek değildir. `current_sheet_bending_head.json`, `physical_sheet_closure_audit_head.json`, `native_sheet_mapping_audit_head.json` birlikte kullan.
- Geçici destek/fikstür geometrisi, destek bırakmadan önce yük binmeme, son gerçek bağlantılar, son konum çakışmaları ve üretim kareleri denetlenmeli.
- Festo boyunduruk proxy'sindeki eksik fabrika M8 arayüzü açıkça temsil edildi; üretici gövdesine atölyede delik açma talimatı değildir. Resmî tablo D2=M8/T1=17/B4=80/H4=40; CAD eksenleri görsel olarak teyit edilmedi, bu ayrım kayıtta duruyor.
- Tüm K sırası ve üretim kapıları tamamlanınca ortak `ist_montaj/montaj-oynatici.js` ile GLB+JSON çıkar, tarayıcıda aç, örnek üretim/montaj karelerini kontrol et. Yeni oynatıcı yazma.
- Yerel 70–79 adayları ana zincire tamamen alınmış sayılmıyor. Güncel main/F/TOPPING değişikliklerini koruyarak K adımlarını son modele yeniden uygula; yeni girdide iki koşu bayt aynı şartını yeniden denetle. Kilit, SIRA.md, kapsam ve yayın kurallarına uy.
- Kemal'in istediği teslim **K'nin TAMAMI**, sonra U üst raf. 6 destek veya sadece kafayı tamamlamak teslim sayılmıyor.

## Hangi betik neyi yapıyor?

`_local/codex_k_montaj/k1/`:

- `k_cikar.py`, `k_parca.py`, `k78_rebind_ownership.py`: kaynak/cache/adlandırma altyapısı.
- `head_station.py`, `head_benches.py`, `head_bench_integrate.py`: 30 grup, gerçek kafa sırası ve ön boşluktan teslim yolu.
- `head_support_events.py`: kafanın geçici destek bırakma olayları.
- `clip_extract.py`, `clip_rebind.py`: son kelepçe modelinin bir kez çıkarılması ve tam üçgen eşleme.
- `clip_integrate.py`: 16 dikişi mevcut plana ekledi; bütün önceki hareketleri değiştirmedi.
- `clip_delta_ccd.py`, `clip_join_evidence.py`: yeni parçaların hareket ve gerçek kaynak/taşıyıcı/sıra kanıtı.
- `k_son_kaynak.py`: planı tam kaynak üçgen çoklu kümesine bağlar.
- `k_full_ccd.py`, `baglanti_denetim.py`, `k_cikti.py`: tam hareket, bağlantı ve zorunlu çıktı kapıları.

`arastirma/_uretec/codex/k_montaj/`:

- `cut_head_*`: 6+2/6+4 stok, 7 M8, 3 TIG, erişim ve tam kaynağa uygulama.
- `electrical_clip_weld_candidate.py`, `electrical_clip_torch_access.py`, `electrical_clip_apply.py`: son dört kelepçenin gerçek dikişleri ve GLB uygulaması.
- Önceki panel/DIN/bant/yağ/aktüatör adayları burada; mevcut model bunların sonuçlarını içeriyor. Baştan tekrar kurma.

## Korunacaklar

Kirli ana checkout'a yazma; F/TOPPING ve ortak oynatıcıya dokunma. Yerel K worktree'sinde miras kalan şu beş değişmiş JSON bu devir commit'ine alınmadı: `mount_connection_measured_audit.json`, `native_sheet_mapping_audit_pump.json`, `pump_order_constraints.json`, `pump_plan_audit.json`, `pump_plan_progress.json`. Bunları temizle/reset/stash yapma. Güncel doğrulanmış sonuçlar yukarıdaki `head_*` ve `clip_*` kayıtlarıdır.

**Codex bu devirden sonra K üzerinde yeni tasarım yapmayacak.** Ana model/site bu devir işleminde değiştirilmedi. Dosyalar yalnız devam için K dalına gönderildi; üretime hazır ilan edilmedi.
