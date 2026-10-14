# 09 · BİNA DAĞITIMI — GÖMÜLÜ ZEMİN KANALI KESİTLERİ (üretildi: elektrik_hesap_v1.py)
**Kemal kararı 12:55:** (1) şalter kutusu (duvar panosu) KALIR, bina beslemesi DUVARDAN girer. (2) Dağıtım kutunun ALTINDAN ayrılır; her kol gideceği yere (makine teknik sütunu, QR, robot kutusu, fırın CEE, tezgâh, AP) GÖMÜLÜ zemin kanalıyla gider; **zemin üstünde kanal yok.** (3) Kanallar KÜÇÜK ve STANDART katalog ölçüsünde (OBO / Legrand döşeme altı kanal — standart iç genişlik × yükseklik föyden), doluluk ≤ %50'yi sağlayan EN KÜÇÜK standart boy; güç ve veri AYRI bölme. Makinenin ayırıcısı (kol 1,2 m) şalter kutusunun yanında, duvarda (W001 duvar yüzeyinde, zemin kanalına girmez).
**Bu belge kanal ÖLÇÜSÜ seçmez** (güzergâh uzunluğu, dirsek sayısı ve standart ürün seçimi QR + robot oturumunda); her kol için kablo dış çaplarından GEREKEN ISI KESİTİNİ verir. Kanal iç serbest alanı ≥ ΣA ÷ 0,50; büküm yarıçapı R ≥ 5 × Ø (sabit döşeme, KABLO_SAHIPLIK kural 2) → dirsek / iniş yarıçapı kablonun en büyüğüne göre.
| kol | bölme | hedef | kablo (dış Ø mm) | ΣA mm² | gereken iç serbest alan mm² (≤ %50) | min. büküm R mm (5 × Ø) |
|---|---|---|---|---|---|---|
| MAKİNE (iC60N 3P C32) | güç | ayırıcı (sağ duvar x 5360, panonun yanında) → gömülü kanal → teknik sütun → U_KE → ana pano | W002 (Ø19,9) | 311 | 622 | 100 |
| FIRIN (iC60N 3P C32) | güç | fırın TP10 CEE 32 A prizi (duvarda, fırına dokunmadan) | W003 (Ø19,9) | 311 | 622 | 100 |
| TEZGÂH (iC60N 1P+N C16) | güç | tezgâh IP44 prizi (ani ısıtıcı) | W004 (Ø12,5) | 123 | 245 | 62 |
| ROBOT (iC60N C16) | güç | QR alt giriş → robot kontrol kutusu | W014 (Ø12,5) | 123 | 245 | 62 |
| EKSEN (iC60N C16) | güç | QR alt giriş → robot bölmesi, ray servo | W014b (Ø12,5) | 123 | 245 | 62 |
| QR (iC60N C16) | güç | QR istasyon kutusu (KEL-DPZ giriş plakası) | W015 (Ø12,5) | 123 | 245 | 62 |
| ANA PANO → ER605 (duvar panosu) | veri | ana pano FL SWITCH → duvar panosu router (W002 ile aynı gömülü yol, VERİ bölmesi) | W020 (Ø8,7) | 59 | 119 | 44 |
| HMI AP | veri | ana pano switch → Wi-Fi erişim noktası (personel duvarı) | W029 (Ø8,7) | 59 | 119 | 44 |
| E → QR EtherCAT | veri | E EK1100 OUT → QR EK1100 IN | W025 (Ø8,7) | 59 | 119 | 44 |

## Ortak gövde (kutunun altından çıkan tüm kollar aynı kanalda gidiyorsa en kötü hâl)
- **GÜÇ bölmesi:** W002, W003, W004, W014, W014b, W015 → ΣA = 1113 mm² → iç serbest alan ≥ 2226 mm² (≤ %50 doluluk)
- **VERI bölmesi:** W020, W029, W025 → ΣA = 178 mm² → iç serbest alan ≥ 357 mm² (≤ %50 doluluk)

**Ayrı bölme (güç ↔ veri):** 400 V H07RN-F 5G6 ile Cat.6A / EtherCAT aynı bölmede DEĞİL (EMC gereği: veri hattı güç hattından ayrı bölme; üretici kurulum kılavuzu [V — madde numarası föyden teyit]). Kanalda ara bölme / çift bölmeli profil seçilir.

**Açık / varsayım:** kablo dış çapı [K] Lapp föyü (W003 / W020 dahil [V] işaretliler 04'te); kanal standart iç ölçüsü ve OBO / Legrand ürün kodu föyden QR + robot oturumunca seçilecek (bu oturumda föy erişilmedi → VARSAYIM yok, değer yok); kablo sayıları yeni kablo eklenince (W045b … ) bu tablo yeniden üretilir.
