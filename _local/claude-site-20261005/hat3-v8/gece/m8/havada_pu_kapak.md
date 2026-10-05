# HAT v3 · GECE MADDE 8b — HAVADA PARÇA + AÇIKTA YALITIM + KAPAK GİZLEME TARAMASI

Model: `hat3_v8x.glb` (salt okuma, model DEĞİŞTİRİLMEDİ) · 3 Eki 2026 · tam veri: `havada_pu_kapak.json`

## YÖNTEM (kısaca)
- **Parça** = düğüm içi bağlı bileşen, (mek, kpk) etiketine göre bölünmüş → 4 432 parça, 1,66 M üçgen. Dünya dönüşümü TAM (dönüş + ölçek + hiyerarşi; eski `glb_oku`/`glbkit` yalnız öteleme uyguluyor — E_KUTU/E_KOSE/E_PARMAK düğümlerinde yanlış konum verir, dikkat).
- **Temas** ≤ 0,5 mm: köşe→üçgen kesin uzaklık; havada görünen kümelerde 0,7 mm kenar örneğiyle ikinci tur (106 kenar teması eklendi).
- **Havada** = zemine (y ≤ 1 mm) bağlanmayan küme. İstasyon görünümünde en büyük küme istasyon gövdesi sayılır (A/F/K/TOPPING 788'de B üstünde, U 1862'de — tasarım gereği).
- **PU** = 6 yön ortografik z‑tampon; 1 mm (24 iş) + 0,5 mm (hat, 12 iş); kapalı = ön kapak opak, açık = kpk gizli.
- **Derz** = GÖVDE sac malzemeleri, hiç değmeyen çiftin en yakın uzaklığı 0,2–15 mm.

## ÖZET
| Madde | Bulgu |
|---|---|
| 1 Havada (tam model) | 21 küme düzeltilecek + 3 insan figürü (hariç) |
| 2 Kapak gizli | 12 küme havada kalıyor · 2 TERS (gövde sacı kpk'lı) · 8 kpk'sız parça yalnız kapağa bağlı |
| 3 İstasyon görünümü | 13 küme (9'u Elektrik ana hat — bilgi) · 4 düzeltilecek |
| 4 Açıkta PU | 1 mm'de 0 · 0,5 mm'de 2 yarık (TOPPING, kapaklar açıkken) |
| 5 Derz | 46 aynı‑istasyon çift grubu (117 nokta); 18 grup ≤ 2 mm öncelikli (41 nokta) · 339 kapak derzi + 97 modül arası (kasıtlı, ayrıldı) |

## 1 · HAVADA PARÇA (tam model)
| # | Düğüm | İstasyon | Konum x / y / z (mm) | Boşluk | Öneri |
|---|---|---|---|---|---|
| 1 | K_ITICI__aluminyum__ITICI_ARABA ×2 | K/İtici | 4050–4100 / 984–1042 / −767…−743 ve −657…−633 | 4,0 | **BİLİNEN, doğrulandı.** Araba plakasına 4 mm kaydır ya da ara burç |
| 2 | TOPPING_MODUL__motor ×8 pim + 4'lü küçük grup | TOPPING/Tabla | 2439–2492 / 957–1015 / −500…−432 | 0,5–1,35 | Tabla motoru cıvataları delikte boşta: baş flanşa otursun / delik = cıvata |
| 3 | K_BANT__aluminyum ×2 (46×46×382) | K/Bant | 4023–4070 ve 4331–4378 / 946–992 / −403…−21 | 0,87–1,1 | Bant yan profilleri hiçbir yere bağlı değil: şaseye köşebent |
| 4 | ELK_TOPPING__kanal (556 mm yatay) | TOPPING/Pano | 1892–2448 / 1842–1878 / −827…−790 | 1,5 | Arka saca yasla / klips |
| 5 | E_GOVDE__sac (11,5×745×389) | E/Gövde | 5217–5229 / 238–983 / −811…−422 | 1,5 | Komşu sac kenarına kaydır |
| 6 | ELK_ANA_PANO_UF__cihaz_koyu 2×2 modül (7,8 mm) | Elektrik/Ana pano | 3770–3809 / 1928–1978 / −170…−149 | 1,78 | DIN rayına oturt |
| 7 | TOPPING_DONER__TABLA küçük parça (20×8×33) | TOPPING/Tabla | 1076–1096 / 973–981 / −308…−275 | 1,0 | Tabla göbeğine bağla |
| 8 | TEZGAH_EVYE__krom + sensor_cam | Tezgâh/Evye | 4140–4220 / 960–1006 / 1683–1707 | 0,58 | Batarya kafasını 0,6 mm gövdeye yaklaştır |
| 9 | TEZGAH_SARF__poset | Tezgâh | 4350–4480 / 104–173 / 1779–1849 | 1,0 | Ruloyu askıya oturt |
| — | INSAN_180cm ×3 uzuv | Çevre | — | 2,5–7,3 | Hariç (görsel) |

ROBOT, URUN (ölçek 0,0001 = gizli), E_KUTU yığını havada bulgu VERMEDİ. QR göz kümeleri ve TOPPING piston/alüminyum kümeleri ilk turda havada göründü, kenar örneğiyle temaslı çıktı (sorun yok).

## 2 · KAPAK GİZLEME (kpk)
**Kapak gizlenince havada kalan (kpk'sız ama yalnız kapağa bağlı → kpk EKLE):**
| Düğüm | İstasyon | Konum x / y / z | Boşluk | Öneri |
|---|---|---|---|---|
| QR_MUSTERI_PANELI ekran_cam + paslanmaz + plastik | QR/Müşteri paneli | 4835–5236 / 1663–1773 / 1143–1189 | 10–30 | **BİLİNEN, doğrulandı.** Ön panel (QR_GOVDE__on_seffaf) sabitse ondan kpk kaldır; açılıyorsa paneli 3 parçasına kpk ekle |
| TEZGAH_BULASIK__kulp_isik | Tezgâh/Bulaşık | 3849–3857 / 597–627 / 1266–1295 | 22 | **BİLİNEN, doğrulandı.** kpk ekle |
| TEZGAH_BULASIK__ekran_cam (YENİ) | Tezgâh/Bulaşık | 3856–3857 / 655–685 / 1220–1340 | 22 | kpk ekle |
| QR_HAVALANDIRMA__plastik ×2 (YENİ) | QR/Pano | 5225–5395 / 275–425 ve 1885–2035 / 672–712 | 13–22 | kpk ekle (kpk'lı panele takılı) |
| TEZGAH_CEKMECE__celik ×3 (YENİ) | Tezgâh | 3834–3881 / 790–866 / 1210–1350 | 4–18 | Kulpsa kpk ekle; raysa gövdeye bağla |
| E_COP__sac + DUZ_E_OLUK (YENİ) | E/Robot çöpü | 4449–4609 / 546–603 / 0–59 | 26,9 | Yalnız E ön kapağına değiyor: kapakla açılıyorsa kpk, değilse kalıp/gövdeye braket |
| ELK_ISTASYON cihaz+din+rakor (YENİ) | B/Elektrik | 4168–4312 / 620–710 / −698…−525 | 1,0 | TERS durumun sonucu (aşağı) |

**TERS (gövdeye ait olup kpk'lı):**
| Düğüm | İstasyon | Konum | Öneri |
|---|---|---|---|
| ELK_ISTASYON__pano arka sac 160×120×2 | B/Elektrik | x 4160–4320 · y 605–725 · z −700…−698 | Arka montaj sacı kpk'lı, cihazlar ona bağlı → kpk KALDIR (ön kapak z −612 kpk kalsın) |
| ELK_ISTASYON__pano arka sac 160×120×2 | F/Elektrik | x 2800–2960 · y 830–950 · z −730…−728 | Aynı durum → kpk KALDIR |

Bilgi (sorun değil): ELK_QR_KUTU, QR_GOVDE ön panelleri, TEZGAH_CEKMECE önü, bulaşık kapağı — kpk'lı ama menteşe/kilit kpk komşusu yok (tek parça kapak). Menteşe yarısı/kilit/mıknatıs/fitil için kpk'sız→kapağa yalnız bağlı başka parça çıkmadı.

## 3 · İSTASYON GÖRÜNÜMÜ
Düzeltilecek:
| İstasyon | Düğüm | Konum x / y / z | Durum | Öneri |
|---|---|---|---|---|
| TOPPING | ELK_TOPPING__celik klips (16×27×12) | 880–896 / 894–921 / −628…−616 | Yalnız KAIDE_A'ya değiyor | A/Gövde etiketi ya da TOPPING sacına taşı |
| TOPPING | ELK_TOPPING__kanal dikey 25×932 | 2423–2448 / 907–1839 / −827…−790 | Yalnız Elektrik ana hattına değiyor, TOPPING sacına 1,5 | Kanalı TOPPING arka sacına yasla |
| F | ELK_ISTASYON__rakor | 2972–3008 / 779–800 / −690…−654 | B kasası + ana hatta bağlı, fırın sacına 2,5 | Fırın sacına oturt ya da Elektrik/Ana hat etiketi |
| QR | ELK_QR_MONTAJ__paslanmaz braket | 5040–5157 / 21–84 / 670–692 | Robot kontrol kutusu/kablo köprüsüne bağlı, QR gövdesine 0,6 | 0,6 mm yaklaştır ya da Robot/Kontrol kutusu etiketi |

Bilgi: Elektrik görünümünde 9 küme (ana hat rakor/kablo/kanal, K tartı kablosu, ana pano tavası x 2689–3914 y ~2030 z −828) diğer istasyonların sacına bağlı — Elektrik tek başına açılınca havada; tasarım gereği sayılabilir. Çapraz etiket (bilgi): TOPPING_DONER KONI_ON/ARKA → A/Açıcı, ELK_TOPPING (4 parça) → F/Yükleme bandı, ELK_QR_KABLO (11 parça) → Robot / Ana hat.

## 4 · AÇIKTA PU / YALITIM
- 1 mm raster, 24 iş (6 yön × kapalı/açık × hat/karşı): **> 4 mm² açık PU YOK.**
- 0,5 mm raster (hat): **2 yarık, kapaklar AÇIKKEN önden** — TOPPING_MODUL__pu ön yüzü (z 20), x 2030–2094 ve 2324–2387, y 1142,5–1143 (63 × ≤0,5 mm, 32 mm² her biri). Öneri: komşu sac kenarını 0,5 mm uzat ya da PU ön yüzünü 1 mm geri çek.
- U_F_BACA__yalitim_gorunur hiçbir yönden görünmüyor (örtülü).

## 5 · BOŞLUK / DERZ (0,2–15 mm)
Kasıtlı (ayrıldı): kapak‑gövde derzi 339 nokta (228'i ön yüz) · modüller arası 97 (çoğu 2–3 mm).
**Öncelikli aday (aynı istasyon, ≤ 2 mm — değmesi gereken sac):**
| Aralık | Çift | Adet | Örnek nokta x/y/z |
|---|---|---|---|
| 0,50 | F_UST_KABIN__sac ↔ F_DAVLUMBAZ__sac | 1 | 2952 / 1861 / −523 |
| 0,51 | K_GOVDE__sac ↔ K_GOVDE__sac (taban, y 793) | 12 | 4103 / 793 / −785 |
| 1,0 | B_KASA__sac ↔ B_KASA__sac | 1 | 2501 / 740 / −772 |
| 1,2 | TOPPING_MODUL__paslanmaz ↔ paslanmaz | 1 | 1726 / 1535 / −571 |
| 1,3 | B_KASA__sac ↔ B_MODULER__paslanmaz | 2 | 1420 / 728 / −694 |
| 1,5 | TOPPING_MODUL__paslanmaz ↔ KAIDE_C | 4 | 1465 / 894 / 33 |
| 1,5 | F_UST_KABIN ↔ F_DAVLUMBAZ / F_TP10 / U_F_BACA | 5 | 3954 / 1348 / −442 |
| 1,5 | K_GOVDE__sac ↔ K_GOVDE__sac / kabuk | 8 | 4005 / 1007 / −802 |
| 1,5 | E_GOVDE__sac ↔ E_GOVDE__sac | 1 | 5229 / 241 / −812 |
| 2,0 | TOPPING paslanmaz↔sac · B_KASA on_cerceve↔sac · K kabuk↔sac | 5 | 1938 / 896 / 17 |

Kontrol (3–15 mm; çift cidar / iç bölme olabilir, görsel bakılmalı): K_GOVDE kabuk↔sac 7,5–13,5 (20 nokta), K_GOVDE sac↔sac 3–12,9 (15), TOPPING↔KAIDE_C 3,5–8 (11), B_MODULER 4,5–10,1 (8), F_UST_KABIN↔F_TP10 11,5–13 (3 — ikisi ön yüzde), QR_GOZLER/QR_GOVDE 10 mm (14, ön yüz — göz derzi olabilir), E kabuk↔sac/E_COP 3–14,5 (3). Tüm liste JSON `k5_derz`.

## SINIRLAR
- PU yalnız 6 eksen yönünden; eğik bakışla görünen yarıklar kapsanmadı. 0,5 mm altı yarık atlanabilir.
- Varsayılan animasyon pozu (siparişte hareket eden parçaların ara konumları taranmadı).
- Derz en yakın nokta ölçüsü; kasıtlı/istenmeyen ayrımı sezgisel (kpk/on_seffaf = kapak derzi, farklı istasyon = modül arası).
