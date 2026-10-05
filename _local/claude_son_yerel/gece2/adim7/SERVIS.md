# ADIM 7 · SERVİS / TADİLAT ERİŞİLEBİLİRLİK İNCELEMESİ (SALT OKUMA)

4 Eki 2026 gece · Claude · YEREL. Model DEĞİŞTİRİLMEDİ. Düzeltmeler adım 8'de uygulanacak.

**Kaynaklar:** `hat3_v9d.glb` (v8zq + A, B, E, U üretim sacı; 5-entegrasyonun son çıktısı, `gece2/adim5e/is/`) · `parca_kutulari.json` (v8zq adlı parça kutuları) ·
`gece2/adim5/*_ENTEGRASYON.md` + `*_parca.csv` (TOPPING ve F sacı henüz entegre değil, notlarından okundu) · `grup/ozet.md` (ünite etiketleri).
**Araçlar (bu klasörde):** `erisim.py` → `erisim_cikti.txt` / `erisim.json` (93 servis parçası: ön düzlemden derinlik + önünü kapatan parçalar) ·
`kutu_sor.py` (v9d'de bir kutunun içinde ne var: çıkarma yolu, kapak önü, boş yer denetimi; önbellek `_v9d_ucgen.pkl`).

## Ölçüt

* Koordinat: x hat boyu, y yükseklik (zemin 0), z derinlik: **ön düzlem +79 (robot koridoru tarafı), arka −830 = DUVAR** (makine duvara yaslı, arka boşluk ≈ 20 mm, kural kitabı).
  Önde robot rayı z 485–575 (zeminde); servisçi makine önü ile ray / QR arasında durur (406 mm, QR önünde 591 mm). Robot servis konumunda kilitli kabul.
* **Erişilir:** ön kapaktan ≤ 600 mm, önünde engel yok, el/alet boşluğu ≥ 100 mm. **Zor:** 600–700 mm ya da önünde sökülür parça var ya da boşluk < 100 mm.
  **Erişilemez:** > 700 mm (omuz açıklıktan içeri girmediğinde kol erişimi ≈ 600–650 mm; EN 547-3 / ISO 14738 mertebesi) ya da yol kapalı.
* "Duvara yaslı iken" sütunu: arka sac / arka kapak servis yolu SAYILMAZ.

---------------------------------------------------------------------------------------------------------------------------------

## 1 · ÖZET — EN ÖNEMLİ BULGULAR

1. **Arkadan erişim gereken çok parça var (KRİTİK, basit çözülmez → Kemal'e soru 1).** İstasyon panoları ve valf adaları hep arka duvarda (z ≈ −820), ön kapaktan 780–900 mm derinde,
   önlerinde mekanizma var: TOPPING kuru bölmesinin tamamı (pano, 4 sürücü, 12'li valf adası, şartlandırıcı, 4 kaset motoru, evaporatör kaseti, KLF6.6 grubu), K panosu + valf adası + AW20,
   E panosu (PLC + CX9240 + 6 sürücü + 3 güç kaynağı), B panosu (PLC + 21 röle), DOLAP kutusu, U_F fan filtreleri. TOPPING'in tasarlanmış servis yolu (17 vidalı **arka servis sacı**) duvara yaslı iken kullanılamaz.
2. **Fırın (TP10) teknik bölmesi arkaya bakıyor (KRİTİK → soru 1 / 3).** Fan × 2, fırın ana şalteri, ekran, servis plakası, CEE priz, konveyör tahrik/gergi ve yükleme bandı motoru (NEMA23)
   fırın sırtı z −651'de; arkada yalnız 177 mm aralık + sabit tek parça arka sac. **F istasyon kutusunun kapağı fırın sırtına 77 mm** (arkadan açılsa bile çalışılamaz).
   Ayrıca tünelin iki ucu TOPPING ve K'ye kapalı, fırın önü kapalı → **kırıntı tepsisi ve konveyör bandı çıkış yolu yok.**
3. **Davlumbaz yağ filtresi (EN 16282, haftalık yıkama) önden alınamıyor (KRİTİK → soru 2).** Filtrenin (x 3420–3920 · y 1350–1750 · z −466…−442) önünde kompresör (25 kg, 62 mm aralık) ve yağ tenekesi
   (28 mm aralık) var; her temizlikte ikisi de çıkmalı.
4. **Kompresör kabinden çıkamıyor (BASİT DÜZELTME D2).** Kompresör üstü y 1858, fırın üstü kapak açıklığının üst kaydı (kaynaklı 30 × 30, alt yüzü 1830,5) → 27,5 mm takılıyor.
   Emiş filtresi kompresör kafasında (üstünde 2,5 mm) → filtre bakımı için de kompresör çıkmalı. Çıkış vanası motorun arkasında (439 mm).
5. **Ana şalter kolu 2,07–2,14 m'de ve kapalı fırın üstü kapağının arkasında (soru 5).** EN 60204-1 5.3.4: ayırıcı kolu 0,6–1,9 m ve kolay erişilir olmalı. Ana pano kendisi önden
   166 mm'de, merdivenle erişilir — iyi.

Önden iyi olanlar (sorun yok): B soğutma grubu (4 klipsli ön panel, kompresör 238 mm), depo çekmecesi, robot çöp kovası (kızaklı), TOPPING kasetleri / UNO hazneleri (TC kelepçe), yayıcı kesme valfleri,
mekanizma kanatları + ön emiş filtresi, kırıntı çekmecesi, tabla sensörleri, K bıçağı / DGRF / EC5000 bandı / PulsaJet / yağ pompa rafı, E motorlarının çoğu (257–432 mm), ana pano,
QR UPS / robot kontrol kutusu / kilit kartı / QR kutusu / filtreli fanlar (servis kapaklarında), tezgâh (bulaşık, evye dolabı).

**Uygulanacak basit düzeltme: 4 madde (D1–D4).** Kemal'e soru: 7 madde.

---------------------------------------------------------------------------------------------------------------------------------

## 2 · İSTASYON TABLOSU

Derinlik = ön düzlemden (z +79) parçanın ön yüzüne. Sökülen = parçaya ulaşmak için açılan/sökülen parça sayısı (kapak dahil). ✓ erişilir · ◐ zor · ✗ erişilemez.

### A — açıcı (x 736–1436)
| parça | konum (x · y · z) | erişim yolu | derinlik | sökülen | duvara yaslı | sorun | öneri |
|---|---|---|---|---|---|---|---|
| Açıcı ön motoru | 1088–1144 · 1106–1185 · −65…8 | A ön kapağı (tam boy, 3 gizli menteşe + 3 bas-aç) | 71 | 1 | ✓ | — | — |
| Açıcı arka motoru | 1058–1114 · 1067–1140 · −507…−428 | ön kapak, koniler / millerin arkası | 507 | 1 (+ açıcı parçaları) | ◐ | önünde açıcı konileri, milleri, ön motor | satın alınan cihaz; üretici servisi — değişiklik yok |
| Açıcı pnömatiği | 1064–1108 · 1280–1474 · −562…−518 | ön kapak | 596 | 1 | ◐ | sınırda | — |
| Tabla X motoru | 848–904 · 896–953 · −462…−398 | ön kapak, diz hizası | 477 | 1 | ✓ | — | — |
| Işık perdesi / emniyet sensörü | ön çerçevede z +28…+57 | önden | < 60 | 0–1 | ✓ | — | — |
| **A istasyon kutusu** (C16 + klemens + Harting A) | 1240–1400 · 1880–2050 · −828…−730 (U_A içinde) | ön kapak + merdiven, U_A tabanı (1864) üstünden 314 mm'lik boşluğa | **810** | 1 | **✗** | sigorta atınca 1,9–2,05 m'de 810 mm derine el yetmez; U_A boş | **D1: kutuyu U_A içinde öne al** |

### TOPPING (x 1436–2500) — üretim sacı henüz entegre değil (5c notu: arka = 17 × M5 sökülür servis sacı)
| parça | konum | erişim yolu | derinlik | sökülen | duvara yaslı | sorun | öneri |
|---|---|---|---|---|---|---|---|
| Kaşar / sucuk kasetleri, UNO hazneleri | soğuk oda | K1/K2 kanatları, kaset kızağı / TC kelepçe | 120–560 | 1 | ✓ | — (kaset ≤ ~10 kg, tek kişi) | — |
| Yayıcı kesme valfleri (sos, harç) | 1631–1659 / 2176–2204 · 1162–1208 · −144…−116 | soğuk oda kanadı | 195 | 1 | ✓ | — | — |
| UNO valf blokları + döndürme aktüatörleri | z −428…−346 | kanat + TC çıkış borusu sökülür | 425 | 2–3 | ✓ | — | — |
| Tabla sensörleri (x home/limit, tabla boş) | z −25…−161 | mekanizma kanatları (alt, y 828–1102) | 98–240 | 1 | ✓ | — | — |
| Kırıntı çekmecesi | 1536–2280 · 896–912 · −240…−212 | mekanizma kanadı, öne çekilir (ray örtüsü altından) | 291 | 1 | ✓ | — | — |
| Ön kanat emiş filtresi | 1465–1600 · 823–886 · +62…+78 | kanadın içinde | 2 | 0 | ✓ | — | — |
| Sabit tahrik motoru (bant kaseti) | 2438–2494 · 957–1016 · −505…−408 | mekanizma kanadı | 488 | 1 | ◐ | sağ duvara 3 mm; disk / mıknatıs önünde | — |
| **Soğutma grubu KLF6.6** | 1633–2013 · 815–1087 · −785…−478 (kaide cebi) | önde mekanizma teknesi, lineer raylar, ray örtüsü; kaide ön perdesi 104 mm (grup 272 mm) | 557 (yol kapalı) | — | **✗** | ön perdeden çıkmaz; yalnız arkadan | soru 1 |
| **Arka emiş filtresi** (teknik bölme) | 1442–1630 · 900–1105 · −828…−814 | arka sacta | 894 | — | **✗** | temizlenemez + duvara 20 mm'den emer (ön kanat filtresi zaten var) | soru 1 |
| **Kuru bölme pano kutusu** | 1443–1993 · 1880–2140 · −828…−708 | yalnız tavan servis kapağı (1436–2500 · z −830…−630, y 2200) — önden 710–910 mm geride, 2,2 m'de | 788 | 1 + merdiven / makine üstü | **✗ / ◐** | tavan kapağı önden uzanılamaz | soru 1 |
| **DIN plakası (UPS, güç)** · **4 sürücü** · **valf adası 12 bobin** · **şartlandırıcı** | z −828…−660 · y 1082–1840 | yalnız arka servis sacı | 739–906 | arka sac (17 vida) | **✗** | önde soğuk oda + PU duvar; tavan kapağından 750–1100 mm aşağıda | soru 1 |
| **Kaset motorları** (kaşar / sucuk helezon + rotor, 4) | 2060–2116 / 2332–2388 · 1163–1375 · −814…−749 | yalnız arka | 828 | arka sac | **✗** | soğuk oda arka duvarının (−630) arkasında | soru 1 |
| **Evaporatör kaseti** (2 fan, lamel, TXV, tava, tahliye) | 1676–2216 · 1383–1765 · −826…−630 | yalnız arka; kaset (540 × 382) soğuk oda penceresinden (496 × 338) geçmez | 780 | arka sac | **✗** | 5c notu: evaporatör ayakları + pano + DIN arka servis sacına bağlı → sac sökülürken hepsi sacla gelir | soru 1 |

### B — çekmeceli dolap (x 736–4400, y 123–788)
| parça | konum | erişim yolu | derinlik | sökülen | duvara yaslı | sorun | öneri |
|---|---|---|---|---|---|---|---|
| Soğutma grubu (Secop NLE8.8CN) kompresör | 4128–4298 · 146–308 · −329…−159 | teknik sütun ön paneli (4 klips) | 238 | 1 | ✓ | — | — |
| Kondenser + fanı | 4044–4384 · 146–428 · −554…−466 | ön panel; fan önünden fırça | 545–573 | 1 | ◐ | aylık temizlik fan arkasından | grup çekilecekse bakır hatlarda servis halkası (soğutma işinde) |
| Grubun tamamı (≈ 20–25 kg) | 4038–4388 · 124–428 | ön açıklık 4003–4399 × 126–454 → geçer, zemin hizası | — | 1 + bakır hat | ◐ | ön rayların üstünden öne kayar | 2 kişi |
| Buharlaştırma tavası + serpantin | 4034–4394 · 124–158 · −785…−705 | grup çıkınca | 784 | 2 | ◐ | yerde, grubun arkasında | yıllık; grup çıkarılarak |
| Depo çekmecesi (kaşar / sucuk) | 4041–4325 · 466–703 | PU kapak + bas-aç | 0 | 1 | ✓ | — | — |
| **B panosu** (PLC + 3 SM + 21 röle + NDR-240) | 4035–4392 · 455–745 · −828…−706 | depo kutusu çıksa da arkasında PU'lu depo arka duvarı (−470) | 784–823 | — | **✗** | önden yol yok | soru 1 |
| **DOLAP istasyon kutusu** (C16 + Harting) | 4160–4320 · 605–725 · −698…−612 | kapağı öne bakıyor ama önünde 140 mm sonra depo arka duvarı | 691 (yol kapalı) | — | **✗** | sigorta resetlenemez | soru 1 |
| Evaporatör fanları (4, ebm 4414 FL) | sol 1724–2023 · 390–510 / sağ 3034–3333 · 303–422 · −641…−616 | K2 / K5 çekmeceleri çıkarılır | 695 | 2–3 çekmece | ◐ | çekmece boşluğundan yerde yatarak | — |
| Çekmece motorları + GT3 kayış + "kapalı" reed (21 adet) | ör. K1: 829–988 · 212–248 · −790…−751 | çekmece kutusu raydan çıkarılır; motor kutunun arkasında | 866 | 1–3 çekmece | ◐ / ✗ | tek çekmece boşluğu 160 mm → kol 866'ya yetmez; 2–3 çekmece çıkarılıp omuz içeri sokulursa olur | servis sıklığı düşük — kabul (adım 8'de değişiklik yok) |

### F — fırın + üst kabin (x 2500–4000)
| parça | konum | erişim yolu | derinlik | sökülen | duvara yaslı | sorun | öneri |
|---|---|---|---|---|---|---|---|
| **Kompresör JUN-AIR OF302-15B** (25 kg) | 3359–3739 · 1348–1858 · −380…−80 | fırın üstü sağ düşer kapak (açıklık y 1338–1830,5) | 159 | 1 | **✗ çıkmaz** | üstü 1858 > üst kayıt altı 1830,5 (kaynaklı); emiş filtresi kafada, tavana 2,5 mm | **D2** (kaydı sök) + **D4** (hortum / fiş) · 2 kişi |
| Kompresör çıkış vanası | 3541–3557 · 1821–1837 · −380…−360 | motorun arkası | 439 | 1 | ◐ | önünde motor | **D4** |
| Yağ tenekesi 18 L (≈ 17 kg) | 3746–3981 · 1421–1791 · −414…−178 | sağ düşer kapak | 258 | 1 | ◐ | lans tepesi 1791 → tavan 1860,5: 69 mm (lans 360 mm, yerinde çıkmaz); hortumlar sabit | **D3** |
| Yağ tartısı (PW15AH) | 3788–3938 · 1367–1407 · −308…−284 | teneke çıkınca | 362 | 2 | ✓ | — | — |
| **Davlumbaz yağ filtresi + karbon filtre** | 3420–3920 · 1350–1750 · −496…−442 | önü kompresör + teneke ile kapalı (aralık 62 / 28 mm) | 520–546 | 3 (kapak + kompresör + teneke) | **✗** | haftalık yıkama | soru 2 |
| Davlumbaz fanı RS 30-15 | 3248–3650 · 1321–1661 · −742…−525 | filtrelerin ve kompresörün arkası | 604 | 4+ | ✗ | — | soru 2 ile birlikte |
| Pizza kutusu yedeği (320) | 2520–3324 · 1348–1860 | sol kapak, elle tek tek | 99 | 1 | ✓ | — | — |
| **TP10 teknik bölmesi** (fan × 2, ana şalter, ekran, servis plakası, CEE priz, sinyal kutusu, konveyör tahrik/gergi) | 2502–3998 · 790–1304 · sırt z −651 | yalnız arkadan (fırın sırtı ↔ arka sac 177 mm, arka sac tek parça) | 730–740 | — | **✗** | satın alınan cihaz arkadan servis ister | soru 1 / 3 |
| **Yükleme bandı motoru** (NEMA23 + GT2) | 2752–2808 · 1093–1150 · −496…−431 | TP10 teknik bölme duvarının (−410) arkasında | 510 (yol kapalı) | — | ✗ | — | soru 1 |
| **F istasyon kutusu** (2 × C6 + Harting F) | 2800–2960 · 830–950 · −828…−730 | kapağı fırın sırtına 77 mm | 809 | — | **✗** | arkadan da açılamaz | soru 1 |
| **Kırıntı tepsisi + konveyör bandı** | 2860–3928 · 821–826 (tepsi) | tünel uçları TOPPING (2500) ve K (4000) duvarına kapalı, fırın önü kapalı | — | — | **✗** | günlük kırıntı / bant temizliği yolu yok | soru 3 |

### U — üst depolar (y 1862–2200) + ANA PANO
| parça | konum | erişim yolu | derinlik | sökülen | duvara yaslı | sorun | öneri |
|---|---|---|---|---|---|---|---|
| ANA PANO (kapak, sigortalar, RevPi, DC-UPS, switch) | 3518–3978 · 1866–2176 · −320…−87 | fırın üstü sağ kapak + merdiven, pano kapağı (çeyrek tur kilit) | 166 | 2 | ✓ | 1,87–2,18 m → merdiven | — |
| Ana pano Harting soketleri (8) | sol yan 3489–3545 / arka 3646–3850 | pano solu önden; A · F soketleri arkada (z −349…−293) | 197–372 | 2 | ✓ / ◐ | — | — |
| **Ana şalter kolu OHYS2AJ** | 3579–3645 · **2074–2140** · −87…−53 | kapalı F üst kapağının arkasında | 132 | 1 | ◐ | EN 60204-1: 0,6–1,9 m, kolay erişilir | soru 5 |
| **U_F havalandırma: 4 fan + G3 keçe + STEGO** | emiş 3600–3920 · 1870–1990 / atış 2580–2880 · 2016–2134 · −828…−794 | arka sacta; emişlerin önünde ana pano, atışların önünde pizza kutusu yedeği (170) | 857–898 | — | **✗** | keçe değişimi (1–3 ayda bir) yapılamaz; emiş/atış duvara 20 mm | soru 4 |
| İçecek / kutu yedekleri | U_KE / U_F rafları | ön kapaklar | < 450 | 1 | ✓ | — | — |

### K — kesme (x 4000–4400)
| parça | konum | erişim yolu | derinlik | sökülen | duvara yaslı | sorun | öneri |
|---|---|---|---|---|---|---|---|
| Yıldız bıçak + koruma halkası | 4042–4358 · 1122–1166 · −364…−48 | K ön kapağı (tam boy) | 127 | 1 | ✓ | günlük temizlik — iyi | — |
| DGRF kesici | 4119–4281 · 1254–1591 · −266…−148 | ön kapak | 244 | 1 | ✓ | — | — |
| PulsaJet nozül | 4010–4040 · 1141–1216 · −200…−129 | ön kapak | 230 | 1 | ✓ | — | — |
| EC5000 tahrik rulosu + bant | 4329–4379 · 944–994 · −411…−13 | ön kapak | 92 | 1 | ✓ | — | — |
| Ürün sensörleri (alıcı önde, verici arkada) | z −6…14 / −438…−418 | ön kapak | 65–497 | 1 | ✓ | — | — |
| Yağ pompası · PM1704 · 10 µm emiş filtresi · KBP | 4067–4322 · 1644–1810 · −600…−486 | ön kapak, raf üstü | 565–586 | 1 | ◐ | sınırda; filtrenin solunda duvara 45 mm | — |
| İtici X (MY1B 250) | 4035–4365 · 964–984 · −713…−687 | bandın altından | 766 | 1 | ✗ / ◐ | önünde bant + rulolar | soru 1 (değişim nadir) |
| İtici Z (MY1B 350) + arka D-M9N | 4062–4088 · 1051–1078 · −805…−360 | ön kapak | 454 (sensör 853) | 1 | ◐ | arka sensör stroka bağlı, öne alınamaz | — |
| **K panosu** (PLC + WP231 + NDR-240) | 4068–4332 · 1472–1857 · −822…−688 | ön kapak (açıklık 330), önde DGRF + pompa rafı | 814 | 1 | **✗** | — | soru 1 |
| **K valf adası SS5Y3 + 3 × SY3120** | 4072–4142 · 1482–1549 · −818…−764 | önde DGRF kılavuzu, yan boşluk 84 mm | 877 | 1 | **✗** | — | soru 1 |
| **AW20 şartlandırıcı** (tahliye kabı) | 4290–4330 · 1482–1637 · −816…−766 | sağ duvar boyunca yol açık ama derin | 845 | 1 | **✗** | haftalık tahliye yapılamaz | soru 7 |

### E — kutu (x 4400–5230)
| parça | konum | erişim yolu | derinlik | sökülen | duvara yaslı | sorun | öneri |
|---|---|---|---|---|---|---|---|
| Robot çöp kovası 15 L | 4424–4590 · 128–428 · −371…+29 | alt sol kapak, kızakla öne | 50 | 1 | ✓ | — | — |
| Kalıp destek / köprü / flap motorları | z −329…−178 · y 610–797 | alt kapaklar | 257–351 | 1 | ✓ | — | — |
| Piston motoru (frenli) | 4712–4768 · 1712–1842 · −346…−290 | üst kapaklar | 369 | 1 | ✓ | — | — |
| Parmak / kaldırma motorları (ön) | z −80…+16 | üst kapaklar | < 100 | 1 | ✓ | — | — |
| Köşe motorları MF / MB (arka) | 4473–4846 · 1405–1503 · −403…−344 | PF / PB motorlarının arkasında | 423 | 1 | ◐ | yan boşluk 66–71 mm (< 100) | yazılımda servis konumu (köşe takımı kaldırılır) — modelde değişiklik yok |
| Asansör / besleyici motorları | z −410…−317 | alt / üst sağ kapak | 396–432 | 1 | ✓ | — | — |
| Yığın üstü sensörü | 5170–5181 · 1022–1053 · −800…−780 | şarjör yan kapısından (x 5230, açıklık üstü 986) | ~40 (yan) | 1 | ✓ | sağda ≥ 804 mm yan boşluk şart (zemin 6336'ya kadar var) | — |
| Besleyici arka sensörü · vakum Z silindiri | z −820…−778 · y 1080–1318 | üst kapaklar, travers arkası | 856–870 | 1 | ✗ | strok sonuna bağlı | soru 1 (nadir) |
| **E panosu** (S7-1200 + CX9240 + 6 × EL7062 + 3 güç) | 4460–5180 · 1397–1857 · −826…−692 | üst kapaklar, önde köşe takımı + piston + parmak | 771–819 | 2 | **✗** | — | soru 1 |

### QR (x 4370–5230, z 670–1190) ve tezgâh
| parça | konum | erişim yolu | derinlik | sökülen | duvara yaslı | sorun | öneri |
|---|---|---|---|---|---|---|---|
| UPS · robot kontrol kutusu · QR kutusu | z 675–943 | robot yüzü servis kapakları (menteşe + çeyrek tur) | < 280 | 1–2 | ✓ (robot yüzü koridorda) | — | — |
| Kilit kartı · 24 V · modem | 4925–5210 · 1656–2040 · z 1038–1103 | üst servis kapağı | ≈ 420 | 1 | ✓ | — | — |
| Müşteri paneli (ekran, QR okuyucu, tuş) | müşteri yüzü y 1658–1778 | içeriden, üst servis kapağı | 470–520 | 1 | ✓ | — | — |
| Filtreli fanlar (2) | servis kapaklarında | kapakta | 0 | 0 | ✓ | — | — |
| Göz tabanı / ısıtıcı ped / müşteri kapısı mandalı | göz içi | müşteri kapısından | < 450 | 1 | ✓ | — | — |
| **Göz kapak motorları · kapak sensörleri · mil yatakları (12 göz)** | ör. göz 00: 4402–4434 · 590–638 · z 673–709 | robot yüzü göz sacı (4372–5228 × 447–1653, tek parça) ile göz kasası arasında 38 mm | — | — | **✗** | sac sökülemiyor; mil yatağı braketi sacın üstünde | soru 6 |
| Tezgâh: bulaşık (MEIKO), evye dolabı (EIL 3, sifon, musluk), çekmece | x 3222–3885 · z 1044–1874 | ön (+x) kapaklar | — | 1 | ✓ | standart | — |

---------------------------------------------------------------------------------------------------------------------------------

## 3 · UYGULANACAK BASİT DÜZELTMELER (adım 8)

Yalnız küçük, kesin faydalı ve başka istasyona dokunmayanlar. Mekanizma taşıma, yeni kapı, istasyon büyütme YOK.

### D1 · A istasyon kutusunu U_A içinde öne al
* **Şimdi:** `A_istasyon_kutusu_160x170x100` x 1240–1400 · y 1880–2050 · z −828…−730 (kapak −730'da öne bakıyor) + `A_kutu_din_rayi`, `A_sigorta_iC60N_1PN_C16`, `A_klemens_*`,
  `harting_A_soket` / `_fis` / `_rakoru_M32` (y 2019–2135) + `onyuz_A_istasyon_kutusu_kapagi`.
* **Yeni:** hepsi **z +459** (kutu z −369…−271, kapak ön düzlemden 350 mm), x ve y aynı. Kutu U_A tabanına (y 1862–1864) 2 × L konsol (1,5 mm, y 1864–1880) ile.
  Ana hat A güç + veri kablosu uzar: mevcut üst kanal `ust_hat_TOPPING_A` (x 1250–1993 · y 2143–2166 · z −826…−766) A ucundan **öne 60 × 22 kapaklı kanal**
  x 1250–1310 · y 2143–2166 · z −766…−300 (tavan sacı 2178'in altında, Harting rakor tepesi 2135'in üstünde).
* **Denetim:** v9d'de hedef hacim (1240–1400 × 1878–2140 × −400…−260) BOŞ (`kutu_sor.py`). U_A tavan kirişi x 842–872'de — çakışmaz.
* **Gerekçe:** kutuda açıcının C16 sigortası var; atınca bugün 1,9–2,05 m'de 810 mm derine el yetmez (U_A iç yüksekliği 314 mm). Yeni yerde merdivenle 350 mm. U_A boş yedek depo; kutu 160 mm yer kaplar.

### D2 · Fırın üstü üst kaydının sağ yarısını sökülebilir yap (kompresör çıkışı)
* **Şimdi:** `onyuz_f_ust_ust_kayit` 30 × 30 × 2 boru, x 2501,5–3998,5 · y 1830,5–1860,5 · z 27–57, iki ucu yan saclara, ortası `onyuz_f_ust_dikme_0` (x 3326–3356) ve
  `f_ust_tavan_kirisi` ile kaynaklı.
* **Yeni:** kayıt dikmenin sağ yüzünde (x 3356) bölünür. **Sol parça** x 2501,5–3356 kaynaklı kalır (dikme + tavan kirişi düğümü bunda).
  **Sağ parça** x 3357–3997 (640 mm) sökülür: iki ucunda 2 mm iç köşebent (30 × 25, kayıt içine geçme) → dikme sağ yüzüne ve `f_ust_yan_sag` iç yüzüne **2 × M6 × 12 ISO 7380 A2**
  (karşıda PEM SP-M6 / dikmede M6 perçin somun). `onyuz_f_ust_ust_kayit_yan_kaynagi_3998_0` ve dikme üst kaynağının sağ yarısı kalkar.
* **Gerekçe:** kompresör üstü y 1858, kayıt altı 1830,5 → 27,5 mm takılıyor; kompresör (25 kg) değişimi ve kafadaki emiş filtresi bakımı (tavana 2,5 mm) için çıkması şart.
  Sağ fırın üstü kapağı (x 3252–4000) kayıt bölgesini kapatır → dış görünüş değişmez. Kayıt sökülünce tavan sacının ön kenarı 640 mm boyunca serbest kalır; U_F tabanı ve ana pano
  kendi ön alt kaydına (`onyuz_ust_f_alt_kayit`, y 1864–1894) oturduğu için yük almaz.

### D3 · Yağ tenekesi lansına hızlı kaplin + fişli seviye şalteri
* **Şimdi:** ProMinent 1038304 emme lansı başlığı (`K_YAG__pom` x 3924–3974 · y 1791–1821 · z −231…−181), emiş + dönüş hortumları (y 1821–1833) sabit; lans tepesi → tavan 69 mm.
* **Yeni:** emiş (PFA 10 × 8) ve dönüş (8 × 6) hortumlarına lans başlığında **gıda tipi kapamalı hızlı kaplin** (CPC / Colder sınıfı, erkek yarı lansta, y ≤ 1821),
  seviye şalteri kablosuna **M12 fiş** (başlık yanında). Hortum dişi yarıları mevcut güzergâhta kalır.
* **Gerekçe:** teneke değişimi (haftalık, ≈ 17 kg) önden tek kişi: kapak aç → 2 kaplin + 1 fiş ayır → teneke + lans tartıdan öne çekilir (lans başlığı 1821 < kayıt altı 1830,5)
  → lans dışarıda yeni tenekeye takılır. Bugün lans yerinde çıkmıyor, hortumlar teneke ile birlikte çekilemiyor.

### D4 · Kompresör hava çıkışında servis halkası + fişli besleme
* **Şimdi:** çıkış vanası x 3541–3557 · y 1821–1837 · z −380…−360 (motorun arkasında, 439 mm); Ø10 ana hat buradan arkaya (z −740) TOPPING rakoruna; besleme `f_ust_rakor_kompresor` (arka sac).
* **Yeni:** vanadan sonra **600 mm spiral PU servis halkası** (Ø10, davlumbaz üstü y 1790–1840 bandında, kompresörün arkasında) + kompresör beslemesi **fişli** (priz arka rakorun yanında, z ≈ −800).
  Modelde: hortum güzergâhına halka + priz kutusu; BOM notu.
* **Gerekçe:** D2 ile kompresör hortumu ayırmadan 400 mm öne çekilir, sonra vana / fiş önden ayrılır; 2 kişi kaldırır (raf 1348, ağırlık 25 kg).

---------------------------------------------------------------------------------------------------------------------------------

## 4 · KEMAL'E SORULAR (kritik, basit çözülmeyen)

1. **Makine duvara yaslı → arkadan servis gereken parçalar ne olacak?** Yukarıda ✗ işaretli 40'tan fazla servis parçası yalnız arkadan erişilebilir (TOPPING kuru bölmesi tümü, TP10 teknik bölmesi +
   yükleme bandı motoru + F kutusu, B / K / E panoları, K valf adası, DOLAP kutusu, U_F fan filtreleri, KLF6.6, evaporatör kaseti). TOPPING'in arka servis sacı (2 Eki kararı) duvarda iken açılamaz.
   Seçenekler: **(a)** makine arkasında ≥ 600 mm servis aralığı (en az TOPPING + F altında: x 1436–4000; dükkân derinliği +0,6 m) — satın alınan TP10 ve soğutma grupları için en gerçekçi;
   **(b)** hat bina bağlantıları (baca flanşı, besleme, zemin kanalı) sökülüp servis için öne çekilir — 5,2 m'lik bağlı hat için gerçekçi değil;
   **(c)** panolar / valf adaları / sigortalar istasyon içinde ön kapak arkasına (≤ 400 mm) alınır — istasyon başına iç yerleşim işi. Önerim: TOPPING + F için (a), panolar için uzun vadede (c).
   Not: 5c notundaki "evaporatör ayakları + pano + DIN arka servis sacına bağlı" konusu da bu karara bağlı.
2. **Davlumbaz yağ filtresi (haftalık):** önünde kompresör + yağ tenekesi. Kompresör / teneke yer değiştirmeden çözülmüyor (filtre yukarı 50 mm, yana pizza yığını / yan sac).
   Seçenek: kompresörü başka yere (ör. U_F boş yedek depo alanına) almak ya da filtreyi davlumbazın sol yarısına + pizza yedeğini sağa — karar sende.
3. **TP10 kırıntı tepsisi + konveyör bandı:** tünel uçları komşu istasyonlara, fırın önü kapalı. Üreticiye (özel sipariş) **önden servis kapağı / önden çekilen kırıntı tepsisi** ve teknik bölmenin
   öne alınması sorulsun mu?
4. **U_F havalandırma (4 fan + G3 keçe):** arka sacta, emişler ana panonun, atışlar pizza yedeğinin arkasında, duvara 20 mm'den emip atıyor. Izgarayı üst kapak bandına / tavana almak (hava yolu da düzelir) — onay?
5. **Ana şalter kolu 2,07–2,14 m ve kapalı kapak arkasında:** EN 60204-1 5.3.4 (0,6–1,9 m, kolay erişilir) ile uyumsuz. Kol F üst kapağına (kapak kilitli şalter) ya da ≤ 1,7 m'ye
   ayrı bir dış kumanda → karar. (Ayrıca modelde **acil stop butonu yok** — bilgi.)
6. **QR göz motorları / sensörleri / mil yatakları (12 göz):** robot yüzü göz sacı ile göz kasası arasında 38 mm'de, sac tek parça. Öneri: sac kolon başına iki sökülür panel
   (x 4372–4800 / 4800–5228, M5 FHP + tırtıllı somun) + mil yatağı braketleri sactan göz kasasına. Mekanizma bağlantısı değiştiği için onay gerekir.
7. **Şartlandırıcılar (TOPPING x 2420–2470 · K x 4290–4330, 779–845 mm):** tahliye kabı haftalık boşaltılamaz. Seçenek: otomatik tahliyeli tip (SMC AW20-F02**C**-A sınıfı) + Ø6 tahliye
   hortumu (nereye akacak: TOPPING evaporatör tahliyesi / B gideri) ya da kompresör çıkışında önden erişilir tek otomatik tahliyeli ön filtre (F rafı). Hangisi?

---------------------------------------------------------------------------------------------------------------------------------

## 5 · Yöntem notu / sınırlar
* Derinlikler `parca_kutulari.json` (v8zq) kutularından; A/B/E/U sacı v9d'de aynı zarfta (fark ≤ 0,5). Önemli yerler `kutu_sor.py` ile v9d üzerinde ayrıca doğrulandı
  (kompresör ↔ üst kayıt, A kutusu hedef hacmi, U_F fanlar + ana pano, F kutusu ↔ fırın sırtı 77 mm, DOLAP kutusu ↔ depo duvarı 140 mm, lans başlığı ↔ tavan).
* TOPPING ve F (kapak / davlumbaz kanalı) sacı v9d'de yok → 5c notu esas alındı; entegrasyonda TOPPING tavan servis kapağının bağlantı tipi kontrol edilmeli.
* El / ağırlık değerlendirmesi kutu geometrisiyle yapıldı; menteşe açılma süpürmesi bu adımda koşulmadı (adım 5 açığı).
