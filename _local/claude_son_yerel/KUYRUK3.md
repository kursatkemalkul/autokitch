# KUYRUK 3 — Kemal 4 Eki akşam talimatı (sırayla, her biri bitince COMMIT)

Kemal: "TOPPING bitince sırayla tüm istasyonları montaj gerçekçi üretim animasyonu, ne varsa tek tek tüm istasyonlara uygula. B'de kırmızı kaynağı göremedim, en son ona tekrar bak. Elektrik ana hat açtığımda elektrik sisteminin tümü görünsün (ayrı). Bitirip bitirip kaydet. İstasyonlar birbirine tam denk gelsin, eşit olsun; radius, sac kalınlığı, vida — her şey standartlara uygun ve uyumlu, saçma şey yapma. Her istasyonu tek tek yapıp kaydet. En sonda internette yayınla."

Kurallar: W\_local\hat3-v8\MONTAJ_ANIMASYON_KURALLARI.md · ortak oynatıcı W\otonom\hat\montaj-oynatici.js (lejant, kalıcı kırmızı kaynak) · yöntem B v4 (S\gece2\b4\anim) / A v3 (S\gece2\a3) · model değişikliği = zincir yeni adım (W\arastirma\_uretec\h3\yama_v9, SIRA.md, zincir.py, bayt doğrulama, meshopt) · acil stop YOK · A içi boş · dış zarf · renk güç kırmızı / bilgi mavi / hava yeşil.

| # | İş | Durum | Commit |
|---|----|-------|--------|
| 0 | TOPPING 7 ürün yerleşimi modele (zincir 53) | BİTTİ | 30a5c9a (v9u) |
| 1 | STANDART UYUM denetimi + düzeltme: tüm istasyon gövdelerinde sac kalınlığı ailesi, büküm iç yarıçapı, köşe R'leri, vida/PEM/perçin standart seti, komşu istasyon birleşim yüzleri/delik desenleri/yükseklikler tam denk ve eşit | BİTTİ (adım 55 · ham S\gece2\k3_uyum\z55A\hat3_v9w.glb · rapor S\gece2\k3_uyum\RAPOR.md) | aca69ae |
| 2 | TOPPING montaj animasyonu (yeni yerleşimle) | ÇALIŞIYOR | |
| 3 | F montaj animasyonu | BEKLİYOR | |
| 4 | K montaj animasyonu (eski K sayfası claude-k-montaj-v1 → yeni yöntemle hat3-v8'de k-montaj) | BEKLİYOR | |
| 5 | E montaj animasyonu | BEKLİYOR | |
| 6 | U montaj animasyonu | BEKLİYOR | |
| 7 | QR + tezgâh montaj animasyonu | İPTAL (Kemal: yapma) | |
| 8 | A animasyonu kontrol (A–TOPPING M8×10) + çekmece | BEKLİYOR | |
| 9 | B: kırmızı kaynak görünmüyor — kontrol/düzelt | BEKLİYOR | |
| 10 | Elektrik: sol menüde "Elektrik" (hat geneli) açılınca TÜM elektrik + BİLGİ (internet/Ethernet/sinyal, modem, switch, PC) sistemi görünsün (tüm istasyonların Elektrik üniteleri + ana hat + pano), ayrı görünüm | BEKLİYOR | |
| 11 | Son tam denetim + İNTERNETTE YAYIN (Kemal açık izin verdi: "en sonda internette yayınla") — coord prepare/publish/confirm, yayın kilidi, CLAUDE_BASLA.md | BEKLİYOR | |

## Kayıt
- 22:57 Kemal: QR+tezgâh animasyonu iptal; elektrik görünümüne bilgi/internet kabloları da dahil.
- 23:20 0 bitti (30a5c9a, ham S\gece2\menu7 altında v9u). 1 başlatıldı.
- 23:50 ÖNCELİKLİ EK bitti: adım 54 kuşbaşı hunisi tam dik kenar x 1880 (30bc5ce, ham S\gece2\k3_uyum\z54A\hat3_v9v.glb, ?v=9w). Huni ↔ hortum 10,65 mm, huni öne/yukarı süpürme temas 0; UNO GÖVDESİ (vana tahrik ucu x 1916, TC kelepçe 1893,5) kıyma hortum alt ucuna/kelepçesine çarpar — hortum sabitken gövde ancak hortum sökülünce çıkar (Kemal'e sorulacak). Uyum işi 55 numarasıyla devam.
- 00:55 1 bitti (aca69ae, adım 55, ham S\gece2\k3_uyum\z55A\hat3_v9w.glb, ?v=9x): pul tek standart — M5 DIN 9021 → ISO 7089 (95), M8 DIN 9021/DIN 125 → ISO 7092 (28); tek kaynak yama_v9/sac_standart/sac_uyum_v1.json. R/köşe/arayüz (z 79, −830, 2200, 788, 1862, derz 3) uyumlu, delik kayması 0. Tam çakışma yeni 0. Açık (Kemal'e): TOPPING iç sac 1,0↔B 1,2, F kapak iç 1,5, F_UST kılıf 0,5, U_KE ISO 7380 M8, kör perçin Ø4↔Ø3,2, B çekmece derzleri üst istasyon derzleriyle hizasız; kuşbaşı UNO gövdesi hortum sökülmeden çıkmaz. Sıradaki: 2 (TOPPING montaj animasyonu) — zincir sonu artık 55 (v9w).
- 00:35 iş 2 (TOPPING animasyon) başlatıldı. SABAH Kemal'e: kuşbaşı UNO gövdesi (159 mm) kıyma hortumu sökülmeden öne çıkmıyor (huni çıkıyor) — öneri: hortum alt parçası TC kelepçeli sökülebilir boru; ya da gövde yukarı+öne (raf engeli).
