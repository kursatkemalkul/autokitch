# HAT v3 · v8x · TÜM MODEL ÇAKIŞMA TARAMASI (madde 8a, salt okuma)

Model `hat3_v8x.glb` · 5381 katı bileşen (ROBOT/İNSAN/ZEMİN hariç) · yöntem `govde_denetim_dogru` (0,6 mm örnekleme + iç testi iki yönlü, derinlik = kapsayanın yüzeyine uzaklık, OCC doğrulama) · eşik 0,05 mm.

**Toplam çakışma 1321** · gerçek **127** · kasıtlı 544 · şüpheli 650 · temas (≤0,05 mm) 11380 · incele 0

## GERÇEK BULGULAR (istasyona göre; her grupta derinliğe göre sıralı)

### TOPPING ↔ ELEKTRIK · 2 bulgu

| derinlik mm | A | B | konum x,y,z mm | OCC | öneri |
|---|---|---|---|---|---|
| 14.00 | ELK_TOPPING__kanal · kanal_TOPPING_KD1_dikey | ELK_ANA_HAT__paslanmaz · ana_besleme_kanali | 2435, 1254, -807 | 14.00 | kanal_TOPPING_KD1_dikey, ana_besleme_kanali içine 14.0 mm giriyor: küçük parçayı en kısa yönde ~15 mm kaydır ya da büyük parçada cep/kesik aç |
| 12.50 | ELK_TOPPING__kanal · kanal_TOPPING_KD1_dikey | ELK_ANA_HAT__paslanmaz · ana_besleme_kanali | 2435, 1254, -807 | 12.50 | kanal_TOPPING_KD1_dikey, ana_besleme_kanali içine 12.5 mm giriyor: küçük parçayı en kısa yönde ~14 mm kaydır ya da büyük parçada cep/kesik aç |

### F · 8 bulgu

| derinlik mm | A | B | konum x,y,z mm | OCC | öneri |
|---|---|---|---|---|---|
| 4.86 | HAVA_KOMPRESOR__hava_ana · hava_ana#0 | HAVA_KOMPRESOR__siyah · kompresor_cikis_vanasi | 3548, 1826, -375 | 4.90 | hava_ana#0, kompresor_cikis_vanasi içine 4.9 mm giriyor: küçük parçayı en kısa yönde ~6 mm kaydır ya da büyük parçada cep/kesik aç |
| 0.50 | F_DONER__RULO_TP_CIKIS · RULO_TP_CIKIS#0 | F_DONER__RULO_TP_CIKIS · RULO_TP_CIKIS#2 | 3990, 972, -393 | 0.50 | RULO_TP_CIKIS#2, RULO_TP_CIKIS#0 içine 0.5 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |
| 0.40 | ELK_ISTASYON__cihaz · F_klemens_5 | ELK_ISTASYON__rakor · F_kutu_rakoru_davlumbaz_fani | 2951, 892, -779 | 0.40 | 0.40 mm bindirme (ölçü yuvarlaması): F_klemens_5 ya da F_kutu_rakoru_davlumbaz_fani 0.9 mm geri çekilsin |
| 0.31 | F_DONER__RULO_TP_GIRIS · RULO_TP_GIRIS#0 | F_DONER__RULO_TP_GIRIS · RULO_TP_GIRIS#2 | 2875, 953, -393 | 0.31 | 0.31 mm bindirme (ölçü yuvarlaması): RULO_TP_GIRIS#0 ya da RULO_TP_GIRIS#2 0.8 mm geri çekilsin |
| 0.13 | F_YUKLEME_BANDI__koyu · yb_gt2_kayis | F_DONER__RULO_GB_TAHRIK · RULO_GB_TAHRIK#0 | 2838, 985, -428 | 0.12 | 0.13 mm bindirme (ölçü yuvarlaması): yb_gt2_kayis ya da RULO_GB_TAHRIK#0 0.6 mm geri çekilsin |
| 0.12 | ELK_ISTASYON__celik · celik#2 | ELK_ISTASYON__kablo · F_davlumbaz_fani_kablosu | 3460, 1368, -784 | 0.12 | 0.12 mm bindirme (ölçü yuvarlaması): celik#2 ya da F_davlumbaz_fani_kablosu 0.6 mm geri çekilsin |
| 0.10 | F_TP10_KONVEYOR__paslanmaz · on_ray | F_DONER__RULO_TP_GIRIS · RULO_TP_GIRIS#1 | 2892, 972, -4 | 0.10 | 0.10 mm bindirme (ölçü yuvarlaması): on_ray ya da RULO_TP_GIRIS#1 0.6 mm geri çekilsin |
| 0.10 | F_TP10_KONVEYOR__paslanmaz · arka_ray | F_DONER__RULO_TP_GIRIS · RULO_TP_GIRIS#1 | 2892, 972, -404 | 0.10 | 0.10 mm bindirme (ölçü yuvarlaması): arka_ray ya da RULO_TP_GIRIS#1 0.6 mm geri çekilsin |

### TOPPING · 47 bulgu

| derinlik mm | A | B | konum x,y,z mm | OCC | öneri |
|---|---|---|---|---|---|
| 3.08 | TOPPING_MODUL__celik · sicak_gaz_dongusu | TOPPING_MODUL__celik · yogusma_tavasi_sicak_gazli | 2120, 905, -697 | 3.08 | sicak_gaz_dongusu, yogusma_tavasi_sicak_gazli içine 3.1 mm giriyor: küçük parçayı en kısa yönde ~4 mm kaydır ya da büyük parçada cep/kesik aç |
| 3.08 | TOPPING_MODUL__bakir · sogutma_sivi_hatti | TOPPING_MODUL__bakir · sogutma_emis_hatti | 2134, 1360, -697 | 3.08 | sogutma_emis_hatti, sogutma_sivi_hatti içine 3.1 mm giriyor: küçük parçayı en kısa yönde ~4 mm kaydır ya da büyük parçada cep/kesik aç |
| 3.08 | TOPPING_MODUL__celik · yogusma_tavasi_sicak_gazli | TOPPING_MODUL__celik · sicak_gaz_dongusu | 2120, 905, -563 | 3.08 | sicak_gaz_dongusu, yogusma_tavasi_sicak_gazli içine 3.1 mm giriyor: küçük parçayı en kısa yönde ~4 mm kaydır ya da büyük parçada cep/kesik aç |
| 3.08 | TOPPING_MODUL__bakir · sogutma_sivi_hatti | TOPPING_MODUL__bakir · sogutma_emis_hatti | 2134, 1360, -697 | 3.08 | sogutma_emis_hatti, sogutma_sivi_hatti içine 3.1 mm giriyor: küçük parçayı en kısa yönde ~4 mm kaydır ya da büyük parçada cep/kesik aç |
| 2.97 | TOPPING_MODUL__celik · sicak_gaz_dongusu | TOPPING_MODUL__celik · yogusma_tavasi_sicak_gazli | 2120, 908, -560 | 3.00 | yogusma_tavasi_sicak_gazli, sicak_gaz_dongusu içine 3.0 mm giriyor: küçük parçayı en kısa yönde ~4 mm kaydır ya da büyük parçada cep/kesik aç |
| 2.97 | TOPPING_MODUL__celik · sicak_gaz_dongusu | TOPPING_MODUL__celik · yogusma_tavasi_sicak_gazli | 2120, 908, -700 | 3.00 | yogusma_tavasi_sicak_gazli, sicak_gaz_dongusu içine 3.0 mm giriyor: küçük parçayı en kısa yönde ~4 mm kaydır ya da büyük parçada cep/kesik aç |
| 1.55 | TOPPING_MODUL__cam · kasar_cad_v14__cikis_tupu | TOPPING_MODUL__pom · kasar_cad_v14__yatak_kapagi | 2062, 1165, -125 | 1.50 | kasar_cad_v14__yatak_kapagi, kasar_cad_v14__cikis_tupu içine 1.6 mm giriyor: küçük parçayı en kısa yönde ~3 mm kaydır ya da büyük parçada cep/kesik aç |
| 1.00 | TOPPING_DONER__VALF_SOS · VALF_SOS#1 | TOPPING_DONER__VALF_SOS · VALF_SOS#2 | 2317, 1620, -388 | 1.00 | VALF_SOS#1, VALF_SOS#2 içine 1.0 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |
| 1.00 | TOPPING_MODUL__motor · sogutma_grubu_KLF66 | TOPPING_MODUL__sac · sac#36 | 1634, 816, -479 | 1.00 | sac#36, sogutma_grubu_KLF66 içine 1.0 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |
| 1.00 | TOPPING_DONER__VALF_HARC · VALF_HARC#1 | TOPPING_DONER__VALF_HARC · VALF_HARC#2 | 1564, 1620, -388 | 1.00 | VALF_HARC#1, VALF_HARC#2 içine 1.0 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |
| 1.00 | TOPPING_DONER__VALF_KUSBASI · VALF_KUSBASI#1 | TOPPING_DONER__VALF_KUSBASI · VALF_KUSBASI#2 | 1886, 1198, -388 | 1.00 | VALF_KUSBASI#1, VALF_KUSBASI#2 içine 1.0 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |
| 1.00 | TOPPING_DONER__VALF_KIYMA · VALF_KIYMA#1 | TOPPING_DONER__VALF_KIYMA · VALF_KIYMA#2 | 1692, 1198, -388 | 1.00 | VALF_KIYMA#1, VALF_KIYMA#2 içine 1.0 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |
| 0.92 | TOPPING_MODUL__cam · sucuk_cad_v8__cikis_tupu | TOPPING_MODUL__pom · sucuk_cad_v8__yatak_kapagi | 2341, 1248, -124 | 0.88 | sucuk_cad_v8__yatak_kapagi, sucuk_cad_v8__cikis_tupu içine 0.9 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |
| 0.86 | TOPPING_MODUL__aluminyum · harc__pnomatik_silindir_D32 | TOPPING_MODUL__fircali · harc__pnomatik_on_ayak | 1495, 1595, -679 | 0.90 | harc__pnomatik_on_ayak, harc__pnomatik_silindir_D32 içine 0.9 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |
| 0.86 | TOPPING_MODUL__aluminyum · kusbasi__pnomatik_silindir_D32 | TOPPING_MODUL__fircali · kusbasi__pnomatik_on_ayak | 1816, 1172, -679 | 0.90 | kusbasi__pnomatik_on_ayak, kusbasi__pnomatik_silindir_D32 içine 0.9 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |
| 0.86 | TOPPING_MODUL__aluminyum · kiyma__pnomatik_silindir_D32 | TOPPING_MODUL__fircali · kiyma__pnomatik_on_ayak | 1622, 1172, -679 | 0.90 | kiyma__pnomatik_on_ayak, kiyma__pnomatik_silindir_D32 içine 0.9 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |
| 0.86 | TOPPING_MODUL__aluminyum · sos__pnomatik_silindir_D32 | TOPPING_MODUL__fircali · sos__pnomatik_on_ayak | 2248, 1595, -679 | 0.90 | sos__pnomatik_on_ayak, sos__pnomatik_silindir_D32 içine 0.9 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |
| 0.69 | TOPPING_MODUL__conta · ust_raf_gecis_contasi_harc | TOPPING_MODUL__paslanmaz · harc_cikis_dirsegi_316L | 1507, 1572, -187 | 0.74 | ust_raf_gecis_contasi_harc, harc_cikis_dirsegi_316L içine 0.7 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |
| 0.69 | TOPPING_MODUL__conta · ust_raf_gecis_contasi_sos | TOPPING_MODUL__paslanmaz · sos_cikis_dirsegi_316L | 2260, 1572, -187 | 0.74 | ust_raf_gecis_contasi_sos, sos_cikis_dirsegi_316L içine 0.7 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |
| 0.68 | TOPPING_MODUL__cam · sucuk_cad_v8__cikis_tupu | TOPPING_MODUL__conta · raf_kaset_contasi_sucuk | 2356, 1150, -176 | 0.68 | raf_kaset_contasi_sucuk, sucuk_cad_v8__cikis_tupu içine 0.7 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |
| 0.68 | TOPPING_MODUL__conta · raf_gecis_contasi_kiyma | TOPPING_MODUL__paslanmaz · kiyma__agiz_90_derece | 1610, 1151, -181 | 0.68 | raf_gecis_contasi_kiyma, kiyma__agiz_90_derece içine 0.7 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |
| 0.68 | TOPPING_MODUL__conta · raf_gecis_contasi_kusbasi | TOPPING_MODUL__paslanmaz · kusbasi__agiz_90_derece | 1804, 1151, -181 | 0.68 | raf_gecis_contasi_kusbasi, kusbasi__agiz_90_derece içine 0.7 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |
| 0.63 | TOPPING_MODUL__cam · kasar_cad_v14__cikis_tupu | TOPPING_MODUL__conta · raf_kaset_contasi_kasar | 2062, 1150, -175 | 0.58 | raf_kaset_contasi_kasar, kasar_cad_v14__cikis_tupu içine 0.6 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |
| 0.50 | TOPPING_MODUL__sac · evap_kaseti_dis_sac | TOPPING_MODUL__silikon · silikon#15 | 2104, 1384, -779 | 0.50 | 0.50 mm bindirme (ölçü yuvarlaması): evap_kaseti_dis_sac ya da silikon#15 1.0 mm geri çekilsin |
| 0.50 | TOPPING_MODUL__pom · teknik_bolme_arka_emis_filtresi | TOPPING_MODUL__sac · sac#38 | 1630, 901, -828 | 0.50 | 0.50 mm bindirme (ölçü yuvarlaması): teknik_bolme_arka_emis_filtresi ya da sac#38 1.0 mm geri çekilsin |
| 0.48 | TOPPING_MODUL__sac · evap_kaseti_ic_sac | TOPPING_MODUL__silikon · silikon#15 | 2106, 1424, -775 | 0.50 | 0.48 mm bindirme (ölçü yuvarlaması): evap_kaseti_ic_sac ya da silikon#15 1.0 mm geri çekilsin |
| 0.43 | TOPPING_DONER__KARISTIRICI_KASAR · KARISTIRICI_KASAR#8 | TOPPING_DONER__KARISTIRICI_KASAR · KARISTIRICI_KASAR#23 | 2058, 1337, -546 | 0.42 | 0.43 mm bindirme (ölçü yuvarlaması): KARISTIRICI_KASAR#8 ya da KARISTIRICI_KASAR#23 0.9 mm geri çekilsin |
| 0.43 | TOPPING_DONER__KARISTIRICI_SUCUK · KARISTIRICI_SUCUK#6 | TOPPING_DONER__KARISTIRICI_SUCUK · KARISTIRICI_SUCUK#21 | 2352, 1306, -546 | 0.42 | 0.43 mm bindirme (ölçü yuvarlaması): KARISTIRICI_SUCUK#6 ya da KARISTIRICI_SUCUK#21 0.9 mm geri çekilsin |
| 0.43 | TOPPING_DONER__HELEZON_KASAR · HELEZON_KASAR#2 | TOPPING_DONER__HELEZON_KASAR · HELEZON_KASAR#16 | 2058, 1182, -546 | 0.42 | 0.43 mm bindirme (ölçü yuvarlaması): HELEZON_KASAR#2 ya da HELEZON_KASAR#16 0.9 mm geri çekilsin |
| 0.43 | TOPPING_DONER__HELEZON_SUCUK · HELEZON_SUCUK#2 | TOPPING_DONER__HELEZON_SUCUK · HELEZON_SUCUK#16 | 2352, 1202, -546 | 0.42 | 0.43 mm bindirme (ölçü yuvarlaması): HELEZON_SUCUK#2 ya da HELEZON_SUCUK#16 0.9 mm geri çekilsin |
| 0.34 | TOPPING_MODUL__celik__ARABA · doner_yatak | TOPPING_MODUL__sac__ARABA · siyirici_apron | 1182, 951, -192 | 0.39 | 0.34 mm bindirme (ölçü yuvarlaması): doner_yatak ya da siyirici_apron 0.8 mm geri çekilsin |
| 0.34 | TOPPING_MODUL__cam · sucuk_cad_v8__cikis_tupu | TOPPING_MODUL__pom · sucuk_cad_v8_yarik_dili | 2338, 1149, -169 | 0.33 | 0.34 mm bindirme (ölçü yuvarlaması): sucuk_cad_v8__cikis_tupu ya da sucuk_cad_v8_yarik_dili 0.8 mm geri çekilsin |
| 0.28 | TOPPING_MODUL__paslanmaz · kusbasi__cikis_tc_kelepcesi | TOPPING_MODUL__paslanmaz · kusbasi__cikis_tc_kelebegi | 1815, 1220, -242 | 0.30 | 0.28 mm bindirme (ölçü yuvarlaması): kusbasi__cikis_tc_kelepcesi ya da kusbasi__cikis_tc_kelebegi 0.8 mm geri çekilsin |
| 0.28 | TOPPING_MODUL__paslanmaz · sos__cikis_tc_kelepcesi | TOPPING_MODUL__paslanmaz · sos__cikis_tc_kelebegi | 2246, 1643, -242 | 0.30 | 0.28 mm bindirme (ölçü yuvarlaması): sos__cikis_tc_kelepcesi ya da sos__cikis_tc_kelebegi 0.8 mm geri çekilsin |
| 0.28 | TOPPING_MODUL__paslanmaz · kiyma__cikis_tc_kelepcesi | TOPPING_MODUL__paslanmaz · kiyma__cikis_tc_kelebegi | 1621, 1220, -242 | 0.30 | 0.28 mm bindirme (ölçü yuvarlaması): kiyma__cikis_tc_kelepcesi ya da kiyma__cikis_tc_kelebegi 0.8 mm geri çekilsin |
| 0.28 | TOPPING_MODUL__paslanmaz · harc__cikis_tc_kelepcesi | TOPPING_MODUL__paslanmaz · harc__cikis_tc_kelebegi | 1493, 1643, -242 | 0.30 | 0.28 mm bindirme (ölçü yuvarlaması): harc__cikis_tc_kelepcesi ya da harc__cikis_tc_kelebegi 0.8 mm geri çekilsin |
| 0.24 | TOPPING_MODUL__celik · celik#40 | TOPPING_MODUL__koyu · x_kayisi_sarim_sag | 2388, 925, -367 | 0.19 | 0.24 mm bindirme (ölçü yuvarlaması): celik#40 ya da x_kayisi_sarim_sag 0.7 mm geri çekilsin |
| 0.22 | TOPPING_MODUL__cam · sucuk_cad_v8__govde | TOPPING_MODUL__cam · sucuk_cad_v8__plaka_on | 2422, 1294, -208 | 0.20 | 0.22 mm bindirme (ölçü yuvarlaması): sucuk_cad_v8__govde ya da sucuk_cad_v8__plaka_on 0.7 mm geri çekilsin |
| 0.22 | TOPPING_MODUL__cam · sucuk_cad_v8__plaka_on | TOPPING_MODUL__silikon · sucuk_cad_v8__conta_on | 2422, 1294, -205 | 0.27 | 0.22 mm bindirme (ölçü yuvarlaması): sucuk_cad_v8__plaka_on ya da sucuk_cad_v8__conta_on 0.7 mm geri çekilsin |
| 0.22 | TOPPING_MODUL__cam · sucuk_cad_v8__govde | TOPPING_MODUL__cam · sucuk_cad_v8__plaka_arka | 2422, 1294, -520 | 0.27 | 0.22 mm bindirme (ölçü yuvarlaması): sucuk_cad_v8__govde ya da sucuk_cad_v8__plaka_arka 0.7 mm geri çekilsin |
| 0.15 | TOPPING_MODUL__celik · celik#39 | TOPPING_MODUL__koyu · x_kayisi_sarim_sol | 873, 916, -367 | 0.12 | 0.15 mm bindirme (ölçü yuvarlaması): celik#39 ya da x_kayisi_sarim_sol 0.6 mm geri çekilsin |
| 0.14 | TOPPING_MODUL__cam · kasar_cad_v14__cikis_tupu | TOPPING_MODUL__pom · kasar_cad_v14_yarik_dili | 2066, 1152, -126 | 0.17 | 0.14 mm bindirme (ölçü yuvarlaması): kasar_cad_v14__cikis_tupu ya da kasar_cad_v14_yarik_dili 0.6 mm geri çekilsin |
| 0.06 | TOPPING_DONER__TABLA · TABLA#4 | TOPPING_DONER__TABLA · TABLA#35 | 1174, 982, -22 | 0.07 | 0.06 mm bindirme (ölçü yuvarlaması): TABLA#4 ya da TABLA#35 0.6 mm geri çekilsin |
| 0.06 | TOPPING_DONER__TABLA · TABLA#4 | TOPPING_DONER__TABLA · TABLA#40 | 1084, 982, -318 | 0.07 | 0.06 mm bindirme (ölçü yuvarlaması): TABLA#4 ya da TABLA#40 0.6 mm geri çekilsin |
| 0.06 | TOPPING_DONER__TABLA · TABLA#4 | TOPPING_DONER__TABLA · TABLA#34 | 1084, 982, -22 | 0.07 | 0.06 mm bindirme (ölçü yuvarlaması): TABLA#4 ya da TABLA#34 0.6 mm geri çekilsin |
| 0.06 | TOPPING_DONER__TABLA · TABLA#4 | TOPPING_DONER__TABLA · TABLA#41 | 1174, 982, -318 | 0.07 | 0.06 mm bindirme (ölçü yuvarlaması): TABLA#4 ya da TABLA#41 0.6 mm geri çekilsin |
| 0.06 | TOPPING_DONER__TABLA · TABLA#26 | TOPPING_DONER__TABLA · TABLA#46 | 1182, 988, -330 | 0.02 | 0.06 mm bindirme (ölçü yuvarlaması): TABLA#26 ya da TABLA#46 0.6 mm geri çekilsin |

### ELEKTRIK · 11 bulgu

| derinlik mm | A | B | konum x,y,z mm | OCC | öneri |
|---|---|---|---|---|---|
| 2.12 | ELK_ANA_HAT__paslanmaz · ana_besleme_kanali | ELK_ANA_HAT__rakor · ana_besleme_taban_cercevesi | 4098, 127, -702 | 2.12 | ana_besleme_taban_cercevesi, ana_besleme_kanali içine 2.1 mm giriyor: küçük parçayı en kısa yönde ~3 mm kaydır ya da büyük parçada cep/kesik aç |
| 1.00 | ELK_ANA_HAT__kanal · ust_hat_U_F | ELK_ANA_HAT__paslanmaz · ana_pano_toplama_kanali_askisi_0 | 3325, 2105, -697 | 1.00 | ana_pano_toplama_kanali_askisi_0, ust_hat_U_F içine 1.0 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |
| 0.97 | ELK_ANA_HAT__kanal · ust_hat_U_F_kapak | ELK_ANA_HAT__paslanmaz · ana_pano_toplama_kanali_askisi_0 | 3325, 2166, -699 | 1.00 | ana_pano_toplama_kanali_askisi_0, ust_hat_U_F_kapak içine 1.0 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |
| 0.85 | ELK_ANA_HAT__kanal · ust_hat_U_KE_arka | ELK_ANA_HAT__kanal · inis_K_kanali | 4281, 2125, -825 | 0.85 | inis_K_kanali, ust_hat_U_KE_arka içine 0.9 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |
| 0.83 | ELK_ANA_HAT__kanal · ust_hat_U_KE_arka | ELK_ANA_HAT__kanal · inis_E_kanali | 5119, 2125, -825 | 0.85 | inis_E_kanali, ust_hat_U_KE_arka içine 0.8 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |
| 0.75 | ELK_ANA_HAT__kanal · ust_hat_U_F_baca | ELK_ANA_HAT__kanal · ust_hat_kesit_gecis_UF1_UF2 | 3279, 2106, -825 | 0.73 | ust_hat_kesit_gecis_UF1_UF2, ust_hat_U_F_baca içine 0.8 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |
| 0.75 | ELK_ANA_HAT__kanal · ust_hat_U_F_fan | ELK_ANA_HAT__kanal · ust_hat_kesit_gecis_UF2_UF3 | 2919, 2139, -719 | 0.70 | ust_hat_kesit_gecis_UF2_UF3, ust_hat_U_F_fan içine 0.8 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |
| 0.75 | ELK_ANA_HAT__kanal · ust_hat_U_F_baca | ELK_ANA_HAT__kanal · ust_hat_kesit_gecis_UF2_UF3 | 2921, 2106, -825 | 0.70 | ust_hat_kesit_gecis_UF2_UF3, ust_hat_U_F_baca içine 0.8 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |
| 0.75 | ELK_ANA_HAT__kanal · ust_hat_U_F_sol | ELK_ANA_HAT__kanal · ust_hat_kesit_gecis_UF3_UF4 | 2574, 2106, -825 | 0.80 | ust_hat_kesit_gecis_UF3_UF4, ust_hat_U_F_sol içine 0.8 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |
| 0.75 | ELK_ANA_HAT__kanal · ust_hat_U_F_fan | ELK_ANA_HAT__kanal · ust_hat_kesit_gecis_UF3_UF4 | 2576, 2139, -657 | 0.80 | ust_hat_kesit_gecis_UF3_UF4, ust_hat_U_F_fan içine 0.8 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |
| 0.75 | ELK_ANA_HAT__kanal · ust_hat_U_F | ELK_ANA_HAT__kanal · ust_hat_kesit_gecis_UF1_UF2 | 3281, 2106, -825 | 0.80 | ust_hat_kesit_gecis_UF1_UF2, ust_hat_U_F içine 0.8 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |

### QR ↔ Robot · 1 bulgu

| derinlik mm | A | B | konum x,y,z mm | OCC | öneri |
|---|---|---|---|---|---|
| 2.10 | ELK_QR_MONTAJ__paslanmaz · qr_giris_plakasi_a | QR_ROBOT_KONTROL__robot_kutu · robot_kontrol_kutusu_REZERV | 5040, 22, 677 | 2.10 | qr_giris_plakasi_a, robot_kontrol_kutusu_REZERV içine 2.1 mm giriyor: küçük parçayı en kısa yönde ~3 mm kaydır ya da büyük parçada cep/kesik aç |

### QR · 13 bulgu

| derinlik mm | A | B | konum x,y,z mm | OCC | öneri |
|---|---|---|---|---|---|
| 1.70 | ELK_QR_KABLO__kablo · goz_51_mandal_kablosu | ELK_QR_MONTAJ__celik · goz_51_mandal_braketi | 4995, 1602, 1148 | 1.70 | goz_51_mandal_kablosu, goz_51_mandal_braketi içine 1.7 mm giriyor: küçük parçayı en kısa yönde ~3 mm kaydır ya da büyük parçada cep/kesik aç |
| 1.70 | ELK_QR_KABLO__kablo · goz_50_mandal_kablosu | ELK_QR_MONTAJ__celik · goz_50_mandal_braketi | 4995, 1538, 1148 | 1.70 | goz_50_mandal_kablosu, goz_50_mandal_braketi içine 1.7 mm giriyor: küçük parçayı en kısa yönde ~3 mm kaydır ya da büyük parçada cep/kesik aç |
| 1.70 | ELK_QR_KABLO__kablo · goz_31_mandal_kablosu | ELK_QR_MONTAJ__celik · goz_31_mandal_braketi | 4995, 1202, 1148 | 1.70 | goz_31_mandal_kablosu, goz_31_mandal_braketi içine 1.7 mm giriyor: küçük parçayı en kısa yönde ~3 mm kaydır ya da büyük parçada cep/kesik aç |
| 1.70 | ELK_QR_KABLO__kablo · goz_21_mandal_kablosu | ELK_QR_MONTAJ__celik · goz_21_mandal_braketi | 4995, 1002, 1148 | 1.70 | goz_21_mandal_kablosu, goz_21_mandal_braketi içine 1.7 mm giriyor: küçük parçayı en kısa yönde ~3 mm kaydır ya da büyük parçada cep/kesik aç |
| 1.70 | ELK_QR_KABLO__kablo · goz_40_mandal_kablosu | ELK_QR_MONTAJ__celik · goz_40_mandal_braketi | 4995, 1338, 1148 | 1.70 | goz_40_mandal_kablosu, goz_40_mandal_braketi içine 1.7 mm giriyor: küçük parçayı en kısa yönde ~3 mm kaydır ya da büyük parçada cep/kesik aç |
| 1.70 | ELK_QR_KABLO__kablo · goz_30_mandal_kablosu | ELK_QR_MONTAJ__celik · goz_30_mandal_braketi | 4995, 1138, 1148 | 1.70 | goz_30_mandal_kablosu, goz_30_mandal_braketi içine 1.7 mm giriyor: küçük parçayı en kısa yönde ~3 mm kaydır ya da büyük parçada cep/kesik aç |
| 1.70 | ELK_QR_KABLO__kablo · goz_20_mandal_kablosu | ELK_QR_MONTAJ__celik · goz_20_mandal_braketi | 4995, 938, 1148 | 1.70 | goz_20_mandal_kablosu, goz_20_mandal_braketi içine 1.7 mm giriyor: küçük parçayı en kısa yönde ~3 mm kaydır ya da büyük parçada cep/kesik aç |
| 1.70 | ELK_QR_KABLO__kablo · goz_41_mandal_kablosu | ELK_QR_MONTAJ__celik · goz_41_mandal_braketi | 4995, 1402, 1148 | 1.70 | goz_41_mandal_kablosu, goz_41_mandal_braketi içine 1.7 mm giriyor: küçük parçayı en kısa yönde ~3 mm kaydır ya da büyük parçada cep/kesik aç |
| 1.70 | ELK_QR_KABLO__kablo · goz_00_mandal_kablosu | ELK_QR_MONTAJ__celik · goz_00_mandal_braketi | 4995, 538, 1148 | 1.70 | goz_00_mandal_kablosu, goz_00_mandal_braketi içine 1.7 mm giriyor: küçük parçayı en kısa yönde ~3 mm kaydır ya da büyük parçada cep/kesik aç |
| 1.70 | ELK_QR_KABLO__kablo · goz_01_mandal_kablosu | ELK_QR_MONTAJ__celik · goz_01_mandal_braketi | 4995, 602, 1148 | 1.70 | goz_01_mandal_kablosu, goz_01_mandal_braketi içine 1.7 mm giriyor: küçük parçayı en kısa yönde ~3 mm kaydır ya da büyük parçada cep/kesik aç |
| 1.70 | ELK_QR_KABLO__kablo · goz_11_mandal_kablosu | ELK_QR_MONTAJ__celik · goz_11_mandal_braketi | 4995, 802, 1148 | 1.70 | goz_11_mandal_kablosu, goz_11_mandal_braketi içine 1.7 mm giriyor: küçük parçayı en kısa yönde ~3 mm kaydır ya da büyük parçada cep/kesik aç |
| 1.70 | ELK_QR_KABLO__kablo · goz_10_mandal_kablosu | ELK_QR_MONTAJ__celik · goz_10_mandal_braketi | 4995, 738, 1148 | 1.70 | goz_10_mandal_kablosu, goz_10_mandal_braketi içine 1.7 mm giriyor: küçük parçayı en kısa yönde ~3 mm kaydır ya da büyük parçada cep/kesik aç |
| 0.83 | ELK_QR_KABLO__paslanmaz · qr_omurga_kanali | ELK_QR_MONTAJ__paslanmaz · qr_giris_plakasi_b | 5323, 21, 692 | 0.80 | qr_giris_plakasi_b, qr_omurga_kanali içine 0.8 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |

### A · 2 bulgu

| derinlik mm | A | B | konum x,y,z mm | OCC | öneri |
|---|---|---|---|---|---|
| 1.50 | TOPPING_MODUL__sac · acici_kolonu | KAIDE_A__sac · kaide_A_mekanizma_taban_saci | 1028, 894, -658 | 1.50 | ince parça (sac/levha) diğerini boydan geçiyor: acici_kolonu üzerinde delik/kesik aç ya da kaide_A_mekanizma_taban_saci 2 mm kaydır |
| 0.15 | TOPPING_DONER__KONI_ON · KONI_ON#0 | TOPPING_DONER__KONI_ARKA · KONI_ARKA#0 | 1086, 1068, -170 | 0.16 | 0.15 mm bindirme (ölçü yuvarlaması): KONI_ON#0 ya da KONI_ARKA#0 0.7 mm geri çekilsin |

### A ↔ ELEKTRIK · 4 bulgu

| derinlik mm | A | B | konum x,y,z mm | OCC | öneri |
|---|---|---|---|---|---|
| 1.14 | A_GOVDE__paslanmaz · paslanmaz#3 | ELK_ANA_HAT__kanal · ust_hat_TOPPING_A_kapak | 1406, 2165, -800 | 1.10 | ust_hat_TOPPING_A_kapak, paslanmaz#3 içine 1.1 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |
| 1.12 | A_GOVDE__paslanmaz · paslanmaz#3 | ELK_ANA_HAT__kanal · ust_hat_TOPPING_A | 1406, 2144, -800 | 1.10 | ust_hat_TOPPING_A, paslanmaz#3 içine 1.1 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |
| 1.00 | A_GOVDE__paslanmaz · paslanmaz#3 | ELK_ANA_HAT__kablo · ana_hat_A_guc | 1406, 2151, -811 | 1.00 | paslanmaz#3, ana_hat_A_guc içine 1.0 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |
| 1.00 | A_GOVDE__paslanmaz · paslanmaz#3 | ELK_ANA_HAT__kablo_veri · ana_hat_A_veri | 1406, 2148, -801 | 1.00 | paslanmaz#3, ana_hat_A_veri içine 1.0 mm giriyor: küçük parçayı en kısa yönde ~2 mm kaydır ya da büyük parçada cep/kesik aç |

### TOPPING ↔ A · 2 bulgu

| derinlik mm | A | B | konum x,y,z mm | OCC | öneri |
|---|---|---|---|---|---|
| 0.50 | TOPPING_MODUL__sac · enerji_zinciri_kanali | A_GOVDE__sac · A_sag_levha_cep_agizli | 1434, 894, -474 | 0.50 | 0.50 mm bindirme (ölçü yuvarlaması): enerji_zinciri_kanali ya da A_sag_levha_cep_agizli 1.0 mm geri çekilsin |
| 0.50 | TOPPING_MODUL__sac · mekanizma_teknesi | A_GOVDE__sac · A_sag_levha_cep_agizli | 1434, 894, -414 | 0.50 | 0.50 mm bindirme (ölçü yuvarlaması): mekanizma_teknesi ya da A_sag_levha_cep_agizli 1.0 mm geri çekilsin |

### B · 30 bulgu

| derinlik mm | A | B | konum x,y,z mm | OCC | öneri |
|---|---|---|---|---|---|
| 0.35 | CEK_K2_lahm_4__aluminyum · CEK_K2_lahm_4_avara | CEK_K2_lahm_4__koyu · CEK_K2_lahm_4_kayis_GT3 | 1472, 541, 2 | 0.30 | 0.35 mm bindirme (ölçü yuvarlaması): CEK_K2_lahm_4_avara ya da CEK_K2_lahm_4_kayis_GT3 0.8 mm geri çekilsin |
| 0.35 | CEK_K3_hamur_4__aluminyum · CEK_K3_hamur_4_avara | CEK_K3_hamur_4__koyu · CEK_K3_hamur_4_kayis_GT3 | 2127, 541, 2 | 0.30 | 0.35 mm bindirme (ölçü yuvarlaması): CEK_K3_hamur_4_avara ya da CEK_K3_hamur_4_kayis_GT3 0.8 mm geri çekilsin |
| 0.35 | CEK_K1_lahm_4__aluminyum · CEK_K1_lahm_4_avara | CEK_K1_lahm_4__koyu · CEK_K1_lahm_4_kayis_GT3 | 817, 541, 2 | 0.30 | 0.35 mm bindirme (ölçü yuvarlaması): CEK_K1_lahm_4_avara ya da CEK_K1_lahm_4_kayis_GT3 0.8 mm geri çekilsin |
| 0.35 | CEK_K5_ic1_1__aluminyum · CEK_K5_ic1_1_avara | CEK_K5_ic1_1__koyu · CEK_K5_ic1_1_kayis_GT3 | 2782, 541, 2 | 0.30 | 0.35 mm bindirme (ölçü yuvarlaması): CEK_K5_ic1_1_avara ya da CEK_K5_ic1_1_kayis_GT3 0.8 mm geri çekilsin |
| 0.35 | CEK_K1_lahm_1__aluminyum · CEK_K1_lahm_1_avara | CEK_K1_lahm_1__koyu · CEK_K1_lahm_1_kayis_GT3 | 817, 217, 2 | 0.30 | 0.35 mm bindirme (ölçü yuvarlaması): CEK_K1_lahm_1_avara ya da CEK_K1_lahm_1_kayis_GT3 0.8 mm geri çekilsin |
| 0.35 | CEK_K5_hamur_3__aluminyum · CEK_K5_hamur_3_avara | CEK_K5_hamur_3__koyu · CEK_K5_hamur_3_kayis_GT3 | 2782, 433, 2 | 0.30 | 0.35 mm bindirme (ölçü yuvarlaması): CEK_K5_hamur_3_avara ya da CEK_K5_hamur_3_kayis_GT3 0.8 mm geri çekilsin |
| 0.35 | CEK_K1_lahm_2__aluminyum · CEK_K1_lahm_2_avara | CEK_K1_lahm_2__koyu · CEK_K1_lahm_2_kayis_GT3 | 817, 325, 2 | 0.30 | 0.35 mm bindirme (ölçü yuvarlaması): CEK_K1_lahm_2_avara ya da CEK_K1_lahm_2_kayis_GT3 0.8 mm geri çekilsin |
| 0.35 | CEK_K1_lahm_3__aluminyum · CEK_K1_lahm_3_avara | CEK_K1_lahm_3__koyu · CEK_K1_lahm_3_kayis_GT3 | 817, 433, 2 | 0.30 | 0.35 mm bindirme (ölçü yuvarlaması): CEK_K1_lahm_3_avara ya da CEK_K1_lahm_3_kayis_GT3 0.8 mm geri çekilsin |
| 0.35 | CEK_K5_hamur_1__aluminyum · CEK_K5_hamur_1_avara | CEK_K5_hamur_1__koyu · CEK_K5_hamur_1_kayis_GT3 | 2782, 217, 2 | 0.30 | 0.35 mm bindirme (ölçü yuvarlaması): CEK_K5_hamur_1_avara ya da CEK_K5_hamur_1_kayis_GT3 0.8 mm geri çekilsin |
| 0.35 | CEK_K1_lahm_5__aluminyum · CEK_K1_lahm_5_avara | CEK_K1_lahm_5__koyu · CEK_K1_lahm_5_kayis_GT3 | 817, 649, 2 | 0.30 | 0.35 mm bindirme (ölçü yuvarlaması): CEK_K1_lahm_5_avara ya da CEK_K1_lahm_5_kayis_GT3 0.8 mm geri çekilsin |
| 0.35 | CEK_K6_ic1_1__aluminyum · CEK_K6_ic1_1_avara | CEK_K6_ic1_1__koyu · CEK_K6_ic1_1_kayis_GT3 | 3437, 325, 2 | 0.30 | 0.35 mm bindirme (ölçü yuvarlaması): CEK_K6_ic1_1_avara ya da CEK_K6_ic1_1_kayis_GT3 0.8 mm geri çekilsin |
| 0.35 | CEK_K2_lahm_1__aluminyum · CEK_K2_lahm_1_avara | CEK_K2_lahm_1__koyu · CEK_K2_lahm_1_kayis_GT3 | 1472, 217, 2 | 0.30 | 0.35 mm bindirme (ölçü yuvarlaması): CEK_K2_lahm_1_avara ya da CEK_K2_lahm_1_kayis_GT3 0.8 mm geri çekilsin |
| 0.35 | CEK_K3_hamur_2__aluminyum · CEK_K3_hamur_2_avara | CEK_K3_hamur_2__koyu · CEK_K3_hamur_2_kayis_GT3 | 2127, 325, 2 | 0.30 | 0.35 mm bindirme (ölçü yuvarlaması): CEK_K3_hamur_2_avara ya da CEK_K3_hamur_2_kayis_GT3 0.8 mm geri çekilsin |
| 0.35 | CEK_K2_lahm_3__aluminyum · CEK_K2_lahm_3_avara | CEK_K2_lahm_3__koyu · CEK_K2_lahm_3_kayis_GT3 | 1472, 433, 2 | 0.30 | 0.35 mm bindirme (ölçü yuvarlaması): CEK_K2_lahm_3_avara ya da CEK_K2_lahm_3_kayis_GT3 0.8 mm geri çekilsin |
| 0.35 | CEK_K5_hamur_2__aluminyum · CEK_K5_hamur_2_avara | CEK_K5_hamur_2__koyu · CEK_K5_hamur_2_kayis_GT3 | 2782, 325, 2 | 0.30 | 0.35 mm bindirme (ölçü yuvarlaması): CEK_K5_hamur_2_avara ya da CEK_K5_hamur_2_kayis_GT3 0.8 mm geri çekilsin |
| 0.35 | CEK_K2_lahm_5__aluminyum · CEK_K2_lahm_5_avara | CEK_K2_lahm_5__koyu · CEK_K2_lahm_5_kayis_GT3 | 1472, 649, 2 | 0.30 | 0.35 mm bindirme (ölçü yuvarlaması): CEK_K2_lahm_5_avara ya da CEK_K2_lahm_5_kayis_GT3 0.8 mm geri çekilsin |
| 0.35 | CEK_K6_tatli_1__aluminyum · CEK_K6_tatli_1_avara | CEK_K6_tatli_1__koyu · CEK_K6_tatli_1_kayis_GT3 | 3437, 217, 2 | 0.30 | 0.35 mm bindirme (ölçü yuvarlaması): CEK_K6_tatli_1_avara ya da CEK_K6_tatli_1_kayis_GT3 0.8 mm geri çekilsin |
| 0.35 | CEK_K3_hamur_1__aluminyum · CEK_K3_hamur_1_avara | CEK_K3_hamur_1__koyu · CEK_K3_hamur_1_kayis_GT3 | 2127, 217, 2 | 0.30 | 0.35 mm bindirme (ölçü yuvarlaması): CEK_K3_hamur_1_avara ya da CEK_K3_hamur_1_kayis_GT3 0.8 mm geri çekilsin |
| 0.35 | CEK_K2_lahm_2__aluminyum · CEK_K2_lahm_2_avara | CEK_K2_lahm_2__koyu · CEK_K2_lahm_2_kayis_GT3 | 1472, 325, 2 | 0.30 | 0.35 mm bindirme (ölçü yuvarlaması): CEK_K2_lahm_2_avara ya da CEK_K2_lahm_2_kayis_GT3 0.8 mm geri çekilsin |
| 0.35 | CEK_K6_ic1_2__aluminyum · CEK_K6_ic1_2_avara | CEK_K6_ic1_2__koyu · CEK_K6_ic1_2_kayis_GT3 | 3437, 488, 2 | 0.30 | 0.35 mm bindirme (ölçü yuvarlaması): CEK_K6_ic1_2_avara ya da CEK_K6_ic1_2_kayis_GT3 0.8 mm geri çekilsin |
| 0.35 | CEK_K3_hamur_3__aluminyum · CEK_K3_hamur_3_avara | CEK_K3_hamur_3__koyu · CEK_K3_hamur_3_kayis_GT3 | 2127, 433, 2 | 0.30 | 0.35 mm bindirme (ölçü yuvarlaması): CEK_K3_hamur_3_avara ya da CEK_K3_hamur_3_kayis_GT3 0.8 mm geri çekilsin |
| 0.27 | B_SOGUTMA__plastik · gider_ana_hatti_borusu | B_SOGUTMA__plastik · gider_ana_hatti_kilifi_B5 | 4028, 172, -745 | 0.28 | 0.27 mm bindirme (ölçü yuvarlaması): gider_ana_hatti_borusu ya da gider_ana_hatti_kilifi_B5 0.8 mm geri çekilsin |
| 0.26 | B_SOGUTMA__plastik · gider_ana_hatti_borusu | B_SOGUTMA__plastik · gider_ana_hatti_kilifi_B2 | 2074, 206, -746 | 0.29 | 0.26 mm bindirme (ölçü yuvarlaması): gider_ana_hatti_borusu ya da gider_ana_hatti_kilifi_B2 0.8 mm geri çekilsin |
| 0.26 | B_SOGUTMA__plastik · gider_ana_hatti_borusu | B_SOGUTMA__plastik · gider_ana_hatti_kilifi_B4 | 3418, 178, -745 | 0.28 | 0.26 mm bindirme (ölçü yuvarlaması): gider_ana_hatti_borusu ya da gider_ana_hatti_kilifi_B4 0.8 mm geri çekilsin |
| 0.25 | B_SOGUTMA__plastik · gider_ana_hatti_borusu | B_SOGUTMA__plastik · gider_ana_hatti_kelepcesi_K6 | 3700, 173, -734 | 0.23 | 0.25 mm bindirme (ölçü yuvarlaması): gider_ana_hatti_borusu ya da gider_ana_hatti_kelepcesi_K6 0.8 mm geri çekilsin |
| 0.25 | B_SOGUTMA__plastik · gider_ana_hatti_borusu | B_SOGUTMA__plastik · gider_ana_hatti_kilifi_B3 | 2762, 185, -745 | 0.29 | 0.25 mm bindirme (ölçü yuvarlaması): gider_ana_hatti_borusu ya da gider_ana_hatti_kilifi_B3 0.7 mm geri çekilsin |
| 0.23 | B_SOGUTMA__plastik · gider_ana_hatti_borusu | B_SOGUTMA__plastik · gider_ana_hatti_kelepcesi_K5 | 3250, 178, -734 | 0.22 | 0.23 mm bindirme (ölçü yuvarlaması): gider_ana_hatti_borusu ya da gider_ana_hatti_kelepcesi_K5 0.7 mm geri çekilsin |
| 0.08 | B_SOGUTMA__bakir · sicak_gaz_serpantini | DUZ_B_SERPANTIN__plastik · serpantin_tutucu_0 | 4074, 129, -720 | 0.10 | 0.08 mm bindirme (ölçü yuvarlaması): sicak_gaz_serpantini ya da serpantin_tutucu_0 0.6 mm geri çekilsin |
| 0.08 | B_SOGUTMA__bakir · sicak_gaz_serpantini | DUZ_B_SERPANTIN__plastik · serpantin_tutucu_2 | 4339, 129, -770 | 0.10 | 0.08 mm bindirme (ölçü yuvarlaması): sicak_gaz_serpantini ya da serpantin_tutucu_2 0.6 mm geri çekilsin |
| 0.08 | B_SOGUTMA__bakir · sicak_gaz_serpantini | DUZ_B_SERPANTIN__plastik · serpantin_tutucu_1 | 4219, 129, -720 | 0.10 | 0.08 mm bindirme (ölçü yuvarlaması): sicak_gaz_serpantini ya da serpantin_tutucu_1 0.6 mm geri çekilsin |

### K · 1 bulgu

| derinlik mm | A | B | konum x,y,z mm | OCC | öneri |
|---|---|---|---|---|---|
| 0.31 | K_GOVDE__sac · kose_dikmesi_20_42 | K_BANT__pom · cit_giris_1 | 4010, 996, 27 | 0.30 | 0.31 mm bindirme (ölçü yuvarlaması): kose_dikmesi_20_42 ya da cit_giris_1 0.8 mm geri çekilsin |

### E · 6 bulgu

| derinlik mm | A | B | konum x,y,z mm | OCC | öneri |
|---|---|---|---|---|---|
| 0.23 | E_KOSE__CNR_PB · kose_CNR_PB_kaplin | E_KOSE__CNR_PB · kose_CNR_PB_sifir_bayragi | 4817, 1413, -33 | 0.23 | 0.23 mm bindirme (ölçü yuvarlaması): kose_CNR_PB_kaplin ya da kose_CNR_PB_sifir_bayragi 0.7 mm geri çekilsin |
| 0.23 | E_KOSE__CNR_MF · kose_CNR_MF_kaplin | E_KOSE__CNR_MF · kose_CNR_MF_sifir_bayragi | 4503, 1413, -379 | 0.23 | 0.23 mm bindirme (ölçü yuvarlaması): kose_CNR_MF_kaplin ya da kose_CNR_MF_sifir_bayragi 0.7 mm geri çekilsin |
| 0.23 | E_KOSE__CNR_MB · kose_CNR_MB_kaplin | E_KOSE__CNR_MB · kose_CNR_MB_sifir_bayragi | 4821, 1410, -363 | 0.25 | 0.23 mm bindirme (ölçü yuvarlaması): kose_CNR_MB_kaplin ya da kose_CNR_MB_sifir_bayragi 0.7 mm geri çekilsin |
| 0.23 | E_KOSE__CNR_PF · kose_CNR_PF_kaplin | E_KOSE__CNR_PF · kose_CNR_PF_sifir_bayragi | 4499, 1410, -49 | 0.25 | 0.23 mm bindirme (ölçü yuvarlaması): kose_CNR_PF_kaplin ya da kose_CNR_PF_sifir_bayragi 0.7 mm geri çekilsin |
| 0.14 | E_KOSE__aluminyum__CNR_LIFT · CNR_LIFT#0 | E_KOSE__CNR_PF · kose_CNR_PF_kaplin | 4496, 1399, -36 | 0.18 | 0.14 mm bindirme (ölçü yuvarlaması): CNR_LIFT#0 ya da kose_CNR_PF_kaplin 0.6 mm geri çekilsin |
| 0.06 | E_BESLEYICI__aluminyum__VAC_Y · vakum_manifold | E_BESLEYICI__vakum_kaucuk__VAC_Y · vakum_dagitim_hatti | 4880, 1024, -763 | 0.08 | 0.06 mm bindirme (ölçü yuvarlaması): vakum_manifold ya da vakum_dagitim_hatti 0.6 mm geri çekilsin |

## ŞÜPHELİ · KABLO↔KABLO DEMET İÇİ GEÇİŞ (463 çift, en derin 35.4 mm) — kablo çiftine göre özet

Ana hat / QR kablo demetlerinde kablolar aynı güzergâhta birbirinin içinden geçiyor. Üretimde sorun değil ama model ölçüsü yanlış: demet içi kablolar yan yana/üst üste ofsetlenmeli (kablo çapı kadar). Tam liste cakisma.json'da.

| kablo A | kablo B | çift | en derin mm | örnek konum |
|---|---|---|---|---|
| ana_hat_DOLAP_guc | ana_hat_bina | 1 | 35.44 | 3136, 1589, -738 |
| ana_hat_DOLAP_guc | ana_hat_QR_veri | 1 | 34.25 | 3040, 1292, -705 |
| ana_hat_ROBOT_guc | ana_hat_QR_veri | 2 | 25.76 | 3420, 845, -500 |
| ana_hat_TOPPING_guc | ana_hat_A_guc | 1 | 21.52 | 2923, 2144, -741 |
| ana_hat_TOPPING_veri | ana_hat_F_veri | 1 | 20.70 | 2880, 2143, -742 |
| ana_hat_TOPPING_veri | ana_hat_modem | 1 | 20.41 | 2923, 2142, -775 |
| ana_hat_QR_guc | ana_hat_bina | 1 | 9.93 | 2437, 755, -687 |
| ana_hat_ROBOT_guc | ana_hat_bina | 1 | 9.84 | 2434, 755, -687 |
| ana_hat_bina | ana_hat_ROBOT_guc | 1 | 9.80 | 4110, 753, -689 |
| ana_hat_TOPPING_guc | ana_hat_bina | 1 | 9.74 | 2564, 2150, -814 |
| ana_hat_bina | ana_hat_QR_veri | 1 | 9.61 | 2433, 1262, -676 |
| ana_hat_bina | ana_hat_ROBOT_veri | 1 | 8.70 | 4108, 11, -683 |
| ana_hat_TOPPING_guc | ana_hat_F_veri | 1 | 8.70 | 2778, 2143, -730 |
| ana_hat_bina | ana_hat_modem | 1 | 8.61 | 2932, 2136, -815 |
| ana_hat_bina | ana_hat_DOLAP_veri | 2 | 8.61 | 3339, 2116, -756 |
| ana_hat_bina | ana_hat_F_veri | 2 | 8.60 | 3339, 2111, -704 |
| ana_hat_bina | ana_hat_A_veri | 1 | 8.55 | 2587, 2149, -814 |
| ana_hat_F_guc | ana_hat_bina | 1 | 7.48 | 3339, 2115, -713 |
| ana_hat_bina | ana_hat_TOPPING_veri | 1 | 6.18 | 2932, 2144, -810 |
| ana_hat_DOLAP_guc | ana_hat_F_guc | 1 | 6.12 | 2430, 1111, -645 |
| ana_hat_TOPPING_guc | ana_hat_modem | 1 | 6.11 | 2936, 2148, -817 |
| qrk_ana_hat_guc_QR_3G2_5 | qrk_ana_hat_guc_ROBOT_3G2_5 | 1 | 6.10 | 4995, 120, 1038 |
| ana_hat_QR_guc | ana_hat_QR_veri | 1 | 6.10 | 2453, 1262, -786 |
| ana_hat_ROBOT_guc | ana_hat_DOLAP_veri | 3 | 6.09 | 2429, 1114, -656 |
| ana_hat_TOPPING_guc | ana_hat_K_guc | 1 | 6.09 | 3390, 2134, -771 |
| ana_hat_ROBOT_guc | ana_hat_ROBOT_veri | 1 | 6.09 | 5358, 29, -178 |
| ana_hat_QR_guc | ana_hat_DOLAP_veri | 3 | 6.09 | 2932, 2128, -796 |
| ana_hat_TOPPING_guc | ana_hat_A_veri | 1 | 6.09 | 3292, 2137, -794 |
| ana_hat_DOLAP_guc | ana_hat_modem | 1 | 6.08 | 3402, 2113, -734 |
| ana_hat_DOLAP_guc | ana_hat_ROBOT_veri | 1 | 6.08 | 2429, 1090, -631 |
| ana_hat_ROBOT_guc | ana_hat_modem | 1 | 6.08 | 2429, 1114, -656 |
| ana_hat_TOPPING_guc | ana_hat_F_guc | 1 | 6.08 | 2587, 2146, -722 |
| ana_hat_K_guc | ana_hat_QR_guc | 1 | 6.08 | 3360, 2134, -676 |
| ana_hat_DOLAP_guc | ana_hat_A_guc | 1 | 6.08 | 2902, 2146, -740 |
| ana_hat_DOLAP_guc | ana_hat_A_veri | 1 | 6.08 | 2904, 2146, -740 |
| ana_hat_QR_guc | ana_hat_ROBOT_veri | 1 | 6.08 | 2431, 751, -670 |
| ana_hat_TOPPING_guc | ana_hat_QR_veri | 1 | 6.08 | 2908, 2146, -789 |
| ana_hat_TOPPING_guc | ana_hat_DOLAP_veri | 2 | 6.08 | 2908, 2146, -765 |
| ana_hat_ROBOT_guc | ana_hat_QR_guc | 1 | 6.08 | 5379, 53, 615 |
| ana_hat_QR_guc | ana_hat_ROBOT_guc | 1 | 6.08 | 5379, 45, 615 |
| … | 203 kablo çifti daha (json) | | | |

## ŞÜPHELİ · DİĞER (187)

| derinlik mm | A | B | istasyon | konum x,y,z mm | neden |
|---|---|---|---|---|---|
| 146.33 | B_KASA__sac · bolme_4_sac_a | ELK_ANA_HAT__kablo · ana_hat_QR_guc | B ↔ ELEKTRIK | 3995, 508, -775 | SAHTE olası: OCC derinlik 0 ve iki yüzey kesişmiyor (VTK iç testi kötü ağda yanıldı) |
| 146.33 | B_KASA__pu · bolme_4_pu | ELK_ANA_HAT__kablo · ana_hat_QR_guc | B ↔ ELEKTRIK | 3995, 508, -775 | SAHTE olası: OCC derinlik 0 ve iki yüzey kesişmiyor (VTK iç testi kötü ağda yanıldı) |
| 112.53 | B_KASA__sac · bolme_4_sac_b | ELK_ANA_HAT__kablo · ana_hat_QR_guc | B ↔ ELEKTRIK | 4027, 575, -760 | SAHTE olası: OCC derinlik 0 ve iki yüzey kesişmiyor (VTK iç testi kötü ağda yanıldı) |
| 109.80 | B_KASA__pu · bolme_4_pu | ELK_ANA_HAT__kablo_veri · ana_hat_QR_veri | B ↔ ELEKTRIK | 4027, 301, -744 | SAHTE olası: OCC derinlik 0 ve iki yüzey kesişmiyor (VTK iç testi kötü ağda yanıldı) |
| 109.80 | B_KASA__sac · bolme_4_sac_b | ELK_ANA_HAT__kablo_veri · ana_hat_QR_veri | B ↔ ELEKTRIK | 4027, 301, -744 | SAHTE olası: OCC derinlik 0 ve iki yüzey kesişmiyor (VTK iç testi kötü ağda yanıldı) |
| 101.45 | ELK_TOPPING__kablo · kablo#16 | ELK_ANA_HAT__paslanmaz · ana_besleme_kanali | TOPPING ↔ ELEKTRIK | 2422, 1000, -616 | SAHTE olası: OCC derinlik 0 ve iki yüzey kesişmiyor (VTK iç testi kötü ağda yanıldı) |
| 88.05 | ELK_TOPPING__kablo · kablo#16 | ELK_ANA_HAT__kablo_veri · ana_hat_ROBOT_veri | TOPPING ↔ ELEKTRIK | 2429, 1012, -631 | SAHTE olası: OCC derinlik 0 ve iki yüzey kesişmiyor (VTK iç testi kötü ağda yanıldı) |
| 55.63 | ELK_ANA_PANO_UF__cihaz · ana_pano_guc_24V_NDR-120-24 | ELK_ANA_PANO_UF__pano · ana_pano_govde | ELEKTRIK | 3610, 1977, -263 | SAHTE olası: OCC derinlik 0 ve iki yüzey kesişmiyor (VTK iç testi kötü ağda yanıldı) |
| 32.58 | CEK_K3_hamur_3__hamur__CEKMECE · CEK_K3_hamur_3_top_2_1 | URUN__top · top#0 | B ↔ URUN | 2416, 447, -358 | görsel ürün/sarf (hamur, pizza, kutu, teneke) yerleşimi |
| 28.81 | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELK_ANA_HAT__kanal · ust_hat_U_F_baca | ELEKTRIK | 3045, 2135, -781 | SAHTE olası: OCC derinlik 0 ve iki yüzey kesişmiyor (VTK iç testi kötü ağda yanıldı) |
| 24.02 | ELK_ANA_HAT__kablo_veri · ana_hat_ROBOT_guc | ELK_ZEMIN_KANALI__paslanmaz · zemin_ustu_kanal | ELEKTRIK | 4124, 26, -681 | SAHTE olası: OCC derinlik 0 ve iki yüzey kesişmiyor (VTK iç testi kötü ağda yanıldı) |
| 21.52 | B_KASA__sac · tavan_pu_T | ELK_ANA_HAT__paslanmaz · ana_besleme_kanali | B ↔ ELEKTRIK | 2450, 764, -581 | SAHTE olası: OCC derinlik 0 ve iki yüzey kesişmiyor (VTK iç testi kötü ağda yanıldı) |
| 20.74 | CEK_K3_hamur_3__silikon__CEKMECE · CEK_K3_hamur_3_tepsi | URUN__top · top#0 | B ↔ URUN | 2432, 434, -356 | görsel ürün/sarf (hamur, pizza, kutu, teneke) yerleşimi |
| 20.18 | CEK_K3_hamur_3__hamur__CEKMECE · CEK_K3_hamur_3_top_2_2 | URUN__top · top#0 | B ↔ URUN | 2418, 447, -306 | görsel ürün/sarf (hamur, pizza, kutu, teneke) yerleşimi |
| 16.67 | ELK_ANA_HAT__kablo · ana_hat_A_guc | ELK_ANA_HAT__kanal · ust_hat_U_F_baca | ELEKTRIK | 3263, 2140, -766 | SAHTE olası: OCC derinlik 0 ve iki yüzey kesişmiyor (VTK iç testi kötü ağda yanıldı) |
| 11.14 | CEK_K3_hamur_3__sac__CEKMECE · CEK_K3_hamur_3_kutu_2.0_1.0 | URUN__top · top#0 | B ↔ URUN | 2400, 424, -356 | görsel ürün/sarf (hamur, pizza, kutu, teneke) yerleşimi |
| 7.91 | ELK_ANA_HAT__kablo_veri · ana_hat_DOLAP_veri | ELK_ANA_HAT__paslanmaz · ana_pano_toplama_kanali | ELEKTRIK | 3417, 2130, -136 | SAHTE olası: OCC derinlik 0 ve iki yüzey kesişmiyor (VTK iç testi kötü ağda yanıldı) |
| 7.03 | ELK_ANA_HAT__kablo_veri · ana_hat_ROBOT_veri | ELK_ZEMIN_KANALI__paslanmaz · zemin_ustu_kanal | ELEKTRIK | 5368, 23, 592 | SAHTE olası: OCC derinlik 0 ve iki yüzey kesişmiyor (VTK iç testi kötü ağda yanıldı) |
| 5.99 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2430, 1118, -645 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 5.99 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2430, 1118, -645 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 5.99 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2430, 1118, -645 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 5.96 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2429, 1086, -646 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 5.96 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2429, 1086, -647 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 5.35 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2430, 1086, -647 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 5.12 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2428, 1086, -647 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 5.05 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2428, 1115, -656 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 5.04 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2431, 1110, -644 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 4.84 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2428, 1115, -651 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 4.73 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2430, 1118, -643 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 4.73 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2431, 1118, -645 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 4.69 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2431, 1086, -647 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 4.66 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2430, 1118, -643 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 4.47 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2430, 1112, -650 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 4.30 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2427, 1114, -651 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 4.30 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2427, 1114, -651 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 4.26 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2430, 1116, -643 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 4.18 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2427, 1086, -647 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 4.16 | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELK_ANA_HAT__kablo_veri · ana_hat_QR_veri | ELEKTRIK | 2428, 1118, -660 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 4.12 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2431, 1086, -647 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 4.08 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2431, 1088, -647 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 4.00 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2430, 1116, -656 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 3.88 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2431, 1088, -645 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 3.75 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2432, 1090, -647 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 3.72 | TOPPING_MODUL__celik · st_tahrik_diski | TOPPING_MODUL__miknatis · st_tahrik_miknatisi_2 | TOPPING | 2452, 990, -361 | gömülü mıknatıs; diskte cep modellenmemiş |
| 3.72 | TOPPING_MODUL__celik · st_tahrik_diski | TOPPING_MODUL__miknatis · st_tahrik_miknatisi_1 | TOPPING | 2461, 1000, -361 | gömülü mıknatıs; diskte cep modellenmemiş |
| 3.72 | TOPPING_MODUL__celik · st_tahrik_diski | TOPPING_MODUL__miknatis · st_tahrik_miknatisi_4 | TOPPING | 2461, 975, -361 | gömülü mıknatıs; diskte cep modellenmemiş |
| 3.72 | TOPPING_MODUL__celik · st_tahrik_diski | TOPPING_MODUL__miknatis · st_tahrik_miknatisi_3 | TOPPING | 2452, 986, -361 | gömülü mıknatıs; diskte cep modellenmemiş |
| 3.72 | TOPPING_MODUL__celik · st_tahrik_diski | TOPPING_MODUL__miknatis · st_tahrik_miknatisi_5 | TOPPING | 2472, 981, -361 | gömülü mıknatıs; diskte cep modellenmemiş |
| 3.72 | TOPPING_MODUL__celik · st_tahrik_diski | TOPPING_MODUL__miknatis · st_tahrik_miknatisi_0 | TOPPING | 2472, 993, -361 | gömülü mıknatıs; diskte cep modellenmemiş |
| 3.70 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2432, 1110, -647 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 3.67 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2432, 1090, -647 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 3.67 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2428, 1118, -647 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 3.63 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2432, 1086, -648 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 3.59 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2427, 1113, -642 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 3.52 | TOPPING_MODUL__paslanmaz · harc__valf_blogu | TOPPING_DONER__VALF_HARC · VALF_HARC#0 | TOPPING | 1497, 1614, -391 | döner valf ↔ valf bloğu/aktüatör (mil-yuva geçmesi olası; yuva boşluğu modellenmemiş) |
| 3.51 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2428, 1118, -642 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 3.46 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2432, 1088, -648 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 3.23 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2432, 1088, -648 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 3.22 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2431, 1088, -649 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 3.22 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2431, 1092, -649 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 3.22 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2431, 1088, -649 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 3.21 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2426, 1086, -647 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 3.21 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2432, 1092, -648 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 3.20 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2426, 1112, -643 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 3.19 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2426, 1113, -643 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 3.19 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2426, 1113, -643 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 3.19 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2426, 1113, -656 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 3.19 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2426, 1113, -656 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 2.89 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2431, 1117, -650 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 2.83 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2426, 1117, -656 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 2.77 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2430, 1117, -643 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 2.60 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2430, 1087, -650 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 2.60 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2430, 1093, -650 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 2.58 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2427, 1116, -643 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 2.48 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2430, 1086, -643 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 2.48 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2431, 1118, -645 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 2.48 | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELK_ANA_HAT__kablo_veri · ana_hat_QR_veri | ELEKTRIK | 2428, 1116, -656 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 2.44 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2431, 1118, -658 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 2.36 | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELK_ANA_HAT__kablo_veri · ana_hat_QR_veri | ELEKTRIK | 2428, 1118, -658 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 2.35 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2426, 1086, -647 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 2.27 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2426, 1113, -643 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 2.27 | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELK_ANA_HAT__kablo_veri · ana_hat_QR_veri | ELEKTRIK | 2426, 1113, -656 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 2.17 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2425, 1116, -656 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 2.17 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2425, 1116, -656 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 2.17 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2425, 1116, -643 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 2.17 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2425, 1116, -643 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 2.15 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2426, 1086, -643 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 2.15 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2431, 1118, -648 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 2.12 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2425, 1110, -643 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 2.11 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2431, 1092, -649 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 2.11 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2425, 1112, -643 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 2.11 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2431, 1088, -649 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 2.11 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2425, 1112, -656 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 2.11 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2431, 1088, -649 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 2.05 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2428, 1086, -642 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 2.00 | TOPPING_MODUL__aluminyum · sos__valf_dondurme_aktuatoru | TOPPING_DONER__VALF_SOS · VALF_SOS#0 | TOPPING | 2207, 1593, -385 | döner valf ↔ valf bloğu/aktüatör (mil-yuva geçmesi olası; yuva boşluğu modellenmemiş) |
| 2.00 | TOPPING_MODUL__aluminyum · kusbasi__valf_dondurme_aktuatoru | TOPPING_DONER__VALF_KUSBASI · VALF_KUSBASI#0 | TOPPING | 1776, 1170, -385 | döner valf ↔ valf bloğu/aktüatör (mil-yuva geçmesi olası; yuva boşluğu modellenmemiş) |
| 2.00 | TOPPING_MODUL__aluminyum · harc__valf_dondurme_aktuatoru | TOPPING_DONER__VALF_HARC · VALF_HARC#0 | TOPPING | 1454, 1593, -385 | döner valf ↔ valf bloğu/aktüatör (mil-yuva geçmesi olası; yuva boşluğu modellenmemiş) |
| 2.00 | TOPPING_MODUL__aluminyum · kiyma__valf_dondurme_aktuatoru | TOPPING_DONER__VALF_KIYMA · VALF_KIYMA#0 | TOPPING | 1582, 1170, -385 | döner valf ↔ valf bloğu/aktüatör (mil-yuva geçmesi olası; yuva boşluğu modellenmemiş) |
| 1.98 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2429, 1086, -651 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 1.98 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2429, 1094, -651 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 1.90 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2425, 1086, -645 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 1.90 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2426, 1118, -649 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 1.90 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2427, 1086, -649 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 1.90 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2425, 1118, -647 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 1.90 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2429, 1086, -649 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 1.90 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2425, 1118, -646 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 1.90 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2427, 1118, -650 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 1.90 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2426, 1118, -644 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 1.90 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2431, 1086, -649 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 1.90 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2426, 1086, -647 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 1.89 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2431, 1118, -659 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 1.88 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2429, 1118, -658 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 1.88 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2429, 1118, -657 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 1.85 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2431, 1118, -658 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 1.78 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2429, 1086, -651 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 1.78 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2429, 1086, -651 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 1.64 | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELK_ANA_HAT__kablo_veri · ana_hat_QR_veri | ELEKTRIK | 2429, 1117, -656 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 1.62 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2425, 1118, -659 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 1.60 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2425, 1112, -650 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 1.49 | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELK_ANA_HAT__kablo_veri · ana_hat_QR_veri | ELEKTRIK | 2427, 1118, -658 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 1.48 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2425, 1086, -647 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 1.47 | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELK_ANA_HAT__kablo_veri · ana_hat_QR_veri | ELEKTRIK | 2425, 1112, -656 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 1.46 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2425, 1112, -643 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 1.00 | ELK_ANA_HAT__kablo · ana_hat_QR_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2427, 1114, -665 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 1.00 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2424, 1109, -644 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 0.99 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2430, 1093, -650 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 0.99 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2424, 1111, -644 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 0.99 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2430, 1087, -650 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 0.99 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2424, 1111, -658 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 0.99 | ELK_ANA_HAT__kablo · ana_hat_QR_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2429, 1094, -665 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 0.99 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2430, 1093, -650 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 0.96 | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELK_ANA_HAT__kablo_veri · ana_hat_QR_veri | ELEKTRIK | 2424, 1093, -657 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 0.92 | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELK_ANA_HAT__kablo_veri · ana_hat_QR_veri | ELEKTRIK | 2431, 1118, -660 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 0.86 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2426, 1086, -651 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 0.74 | TOPPING_MODUL__paslanmaz · harc__cikis_tc_kelepcesi | TOPPING_MODUL__paslanmaz · harc__cikis_tc_ferrule_valf | TOPPING | 1500, 1588, -248 | TC kelepçe ↔ ferrule oturması (kelepçe kanal profili basit) |
| 0.74 | TOPPING_MODUL__paslanmaz · sos__cikis_tc_kelepcesi | TOPPING_MODUL__paslanmaz · sos__cikis_tc_ferrule_valf | TOPPING | 2253, 1588, -248 | TC kelepçe ↔ ferrule oturması (kelepçe kanal profili basit) |
| 0.74 | TOPPING_MODUL__paslanmaz · kiyma__cikis_tc_kelepcesi | TOPPING_MODUL__paslanmaz · kiyma__cikis_tc_ferrule_valf | TOPPING | 1628, 1165, -248 | TC kelepçe ↔ ferrule oturması (kelepçe kanal profili basit) |
| 0.74 | TOPPING_MODUL__paslanmaz · kusbasi__cikis_tc_kelepcesi | TOPPING_MODUL__paslanmaz · kusbasi__cikis_tc_ferrule_valf | TOPPING | 1822, 1165, -248 | TC kelepçe ↔ ferrule oturması (kelepçe kanal profili basit) |
| 0.64 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2424, 1118, -649 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 0.62 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2424, 1118, -662 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 0.58 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2424, 1118, -658 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 0.58 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2425, 1086, -650 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 0.58 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2424, 1110, -662 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 0.58 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2425, 1086, -650 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 0.58 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2424, 1110, -649 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 0.58 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2424, 1118, -645 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 0.43 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2423, 1118, -648 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 0.43 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2423, 1118, -662 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 0.25 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2429, 1086, -651 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 0.25 | ELK_ANA_HAT__kablo · ana_hat_DOLAP_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2429, 1094, -651 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 0.19 | TOPPING_MODUL__paslanmaz · kusbasi__valf_blogu | TOPPING_DONER__VALF_KUSBASI · VALF_KUSBASI#0 | TOPPING | 1810, 1169, -396 | döner valf ↔ valf bloğu/aktüatör (mil-yuva geçmesi olası; yuva boşluğu modellenmemiş) |
| 0.19 | TOPPING_MODUL__paslanmaz · kiyma__valf_blogu | TOPPING_DONER__VALF_KIYMA · VALF_KIYMA#0 | TOPPING | 1616, 1169, -396 | döner valf ↔ valf bloğu/aktüatör (mil-yuva geçmesi olası; yuva boşluğu modellenmemiş) |
| 0.19 | TOPPING_MODUL__paslanmaz · sos__valf_blogu | TOPPING_DONER__VALF_SOS · VALF_SOS#0 | TOPPING | 2242, 1592, -396 | döner valf ↔ valf bloğu/aktüatör (mil-yuva geçmesi olası; yuva boşluğu modellenmemiş) |
| 0.16 | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELK_ANA_HAT__kablo_veri · ana_hat_QR_veri | ELEKTRIK | 2426, 1115, -664 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 0.16 | ELK_ANA_HAT__kablo · ana_hat_ROBOT_guc | ELK_ANA_HAT__kablo_veri · ana_hat_F_veri | ELEKTRIK | 2426, 1115, -664 | yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı |
| 0.09 | TOPPING_MODUL__on_seffaf · onyuz_kilavuz_flipper | TOPPING_MODUL__pom · pom#40 | TOPPING | 1992, 1158, 3 | kapak/kanat (kpk) parçası; kapalı konumda bindirme |
| 0.08 | K_GOVDE__sac · kose_dikmesi_380_42 | K_GOVDE__siyah · onyuz_kapak_K_basac_0 | K | 4374, 1006, 55 | kapak/kanat (kpk) parçası; kapalı konumda bindirme |
| 0.08 | K_GOVDE__sac · kose_dikmesi_380_42 | K_GOVDE__siyah · onyuz_kapak_K_basac_1 | K | 4372, 1426, 55 | kapak/kanat (kpk) parçası; kapalı konumda bindirme |
| 0.08 | K_GOVDE__sac · kose_dikmesi_380_42 | K_GOVDE__siyah · onyuz_kapak_K_basac_2 | K | 4372, 1796, 55 | kapak/kanat (kpk) parçası; kapalı konumda bindirme |
| 0.07 | TOPPING_MODUL__on_seffaf · soguk_ic_kaplama_cepli | TOPPING_MODUL__on_seffaf · on_seffaf#5 | TOPPING | 1943, 2087, 34 | kapak/kanat (kpk) parçası; kapalı konumda bindirme |
| 0.07 | TOPPING_MODUL__on_seffaf · soguk_ic_kaplama_cepli | TOPPING_MODUL__on_seffaf · on_seffaf#4 | TOPPING | 1943, 1647, 34 | kapak/kanat (kpk) parçası; kapalı konumda bindirme |
| 0.07 | TOPPING_MODUL__on_seffaf · soguk_ic_kaplama_cepli | TOPPING_MODUL__on_seffaf · on_seffaf#3 | TOPPING | 1943, 1187, 34 | kapak/kanat (kpk) parçası; kapalı konumda bindirme |
| 0.07 | ELK_QR_MONTAJ__celik · goz_51_kapak_kulagi_0 | QR_GOZLER__celik__GOZ_51_KAPAK · goz_51_kapak_mili | QR | 5058, 1632, 684 | kapak/kanat (kpk) parçası; kapalı konumda bindirme |
| 0.07 | ELK_QR_MONTAJ__celik · goz_20_kapak_kulagi_1 | QR_DONER__GOZ_20_KAPAK · GOZ_20_KAPAK#0 | QR | 4948, 1032, 684 | kapak/kanat (kpk) parçası; kapalı konumda bindirme |
| 0.07 | ELK_QR_MONTAJ__celik · goz_01_kapak_kulagi_0 | QR_GOZLER__celik__GOZ_01_KAPAK · goz_01_kapak_mili | QR | 5058, 632, 684 | kapak/kanat (kpk) parçası; kapalı konumda bindirme |
| 0.07 | ELK_QR_MONTAJ__celik · goz_31_kapak_kulagi_1 | QR_GOZLER__celik__GOZ_31_KAPAK · goz_31_kapak_mili | QR | 5358, 1232, 684 | kapak/kanat (kpk) parçası; kapalı konumda bindirme |
| 0.07 | ELK_QR_MONTAJ__celik · goz_50_kapak_kulagi_0 | QR_GOZLER__celik__GOZ_50_KAPAK · goz_50_kapak_mili | QR | 4648, 1632, 684 | kapak/kanat (kpk) parçası; kapalı konumda bindirme |
| 0.07 | ELK_QR_MONTAJ__celik · goz_10_kapak_kulagi_0 | QR_GOZLER__celik__GOZ_10_KAPAK · goz_10_kapak_mili | QR | 4648, 832, 684 | kapak/kanat (kpk) parçası; kapalı konumda bindirme |
| 0.07 | ELK_QR_MONTAJ__celik · goz_30_kapak_kulagi_1 | QR_GOZLER__celik__GOZ_30_KAPAK · goz_30_kapak_mili | QR | 4948, 1232, 684 | kapak/kanat (kpk) parçası; kapalı konumda bindirme |
| 0.07 | ELK_QR_MONTAJ__celik · goz_50_kapak_kulagi_1 | QR_GOZLER__celik__GOZ_50_KAPAK · goz_50_kapak_mili | QR | 4948, 1632, 684 | kapak/kanat (kpk) parçası; kapalı konumda bindirme |
| 0.07 | ELK_QR_MONTAJ__celik · goz_11_kapak_kulagi_0 | QR_GOZLER__celik__GOZ_11_KAPAK · goz_11_kapak_mili | QR | 5058, 832, 684 | kapak/kanat (kpk) parçası; kapalı konumda bindirme |
| 0.07 | ELK_QR_MONTAJ__celik · goz_30_kapak_kulagi_0 | QR_GOZLER__celik__GOZ_30_KAPAK · goz_30_kapak_mili | QR | 4648, 1232, 684 | kapak/kanat (kpk) parçası; kapalı konumda bindirme |
| 0.07 | ELK_QR_MONTAJ__celik · goz_01_kapak_kulagi_1 | QR_GOZLER__celik__GOZ_01_KAPAK · goz_01_kapak_mili | QR | 5358, 632, 684 | kapak/kanat (kpk) parçası; kapalı konumda bindirme |
| 0.07 | ELK_QR_MONTAJ__celik · goz_41_kapak_kulagi_0 | QR_GOZLER__celik__GOZ_41_KAPAK · goz_41_kapak_mili | QR | 5058, 1432, 684 | kapak/kanat (kpk) parçası; kapalı konumda bindirme |
| 0.07 | ELK_QR_MONTAJ__celik · goz_40_kapak_kulagi_0 | QR_GOZLER__celik__GOZ_40_KAPAK · goz_40_kapak_mili | QR | 4648, 1432, 684 | kapak/kanat (kpk) parçası; kapalı konumda bindirme |
| 0.07 | ELK_QR_MONTAJ__celik · goz_31_kapak_kulagi_0 | QR_GOZLER__celik__GOZ_31_KAPAK · goz_31_kapak_mili | QR | 5058, 1232, 684 | kapak/kanat (kpk) parçası; kapalı konumda bindirme |
| 0.07 | ELK_QR_MONTAJ__celik · goz_20_kapak_kulagi_0 | QR_DONER__GOZ_20_KAPAK · GOZ_20_KAPAK#0 | QR | 4648, 1032, 684 | kapak/kanat (kpk) parçası; kapalı konumda bindirme |
| 0.07 | ELK_QR_MONTAJ__celik · goz_51_kapak_kulagi_1 | QR_GOZLER__celik__GOZ_51_KAPAK · goz_51_kapak_mili | QR | 5358, 1632, 684 | kapak/kanat (kpk) parçası; kapalı konumda bindirme |
| 0.07 | ELK_QR_MONTAJ__celik · goz_10_kapak_kulagi_1 | QR_GOZLER__celik__GOZ_10_KAPAK · goz_10_kapak_mili | QR | 4948, 832, 684 | kapak/kanat (kpk) parçası; kapalı konumda bindirme |
| 0.07 | ELK_QR_MONTAJ__celik · goz_11_kapak_kulagi_1 | QR_GOZLER__celik__GOZ_11_KAPAK · goz_11_kapak_mili | QR | 5358, 832, 684 | kapak/kanat (kpk) parçası; kapalı konumda bindirme |
| 0.07 | ELK_QR_MONTAJ__celik · goz_21_kapak_kulagi_1 | QR_GOZLER__celik__GOZ_21_KAPAK · goz_21_kapak_mili | QR | 5358, 1032, 684 | kapak/kanat (kpk) parçası; kapalı konumda bindirme |
| 0.07 | ELK_QR_MONTAJ__celik · goz_00_kapak_kulagi_0 | QR_GOZLER__celik__GOZ_00_KAPAK · goz_00_kapak_mili | QR | 4648, 632, 684 | kapak/kanat (kpk) parçası; kapalı konumda bindirme |
| 0.07 | ELK_QR_MONTAJ__celik · goz_41_kapak_kulagi_1 | QR_GOZLER__celik__GOZ_41_KAPAK · goz_41_kapak_mili | QR | 5358, 1432, 684 | kapak/kanat (kpk) parçası; kapalı konumda bindirme |
| 0.07 | ELK_QR_MONTAJ__celik · goz_40_kapak_kulagi_1 | QR_GOZLER__celik__GOZ_40_KAPAK · goz_40_kapak_mili | QR | 4948, 1432, 684 | kapak/kanat (kpk) parçası; kapalı konumda bindirme |
| 0.07 | ELK_QR_MONTAJ__celik · goz_00_kapak_kulagi_1 | QR_GOZLER__celik__GOZ_00_KAPAK · goz_00_kapak_mili | QR | 4948, 632, 684 | kapak/kanat (kpk) parçası; kapalı konumda bindirme |
| 0.07 | ELK_QR_MONTAJ__celik · goz_21_kapak_kulagi_0 | QR_GOZLER__celik__GOZ_21_KAPAK · goz_21_kapak_mili | QR | 5058, 1032, 684 | kapak/kanat (kpk) parçası; kapalı konumda bindirme |

## KASITLI (544) — nedene göre özet (tam liste cakisma.json)

| neden | adet | en derin mm | örnekler |
|---|---|---|---|
| aynı parçanın alt katıları birbirine giriyor (tek parça; boolean birleşim yapılmamış) | 286 | 15.05 | ana_pano_ana_salter_iSW_4P_40A ↔ ana_pano_ana_salter_iSW_4P_40A; ana_pano_guc_24V_NDR-120-24 ↔ ana_pano_guc_24V_NDR-120-24; ana_pano_hmi_ana_bilgisayar_RevPi_Connect_4 ↔ ana_pano_hmi_ana_bilgisayar_RevPi_Connect_4; ana_pano_kacak_akim_iID_4P_40A_30mA ↔ ana_pano_kacak_akim_iID_4P_40A_30mA |
| DIN raya geçme cihaz (cihazın ray yuvası modellenmemiş) | 62 | 3.84 | ag_anahtari_FL_SWITCH_1008N_QR ↔ qr_kutu_din_rayi; ana_pano_ag_anahtari_FL_SWITCH_1008N ↔ ana_pano_din_rayi_B; ana_pano_ana_salter_iSW_4P_40A ↔ ana_pano_din_rayi_A; ana_pano_din_rayi_B ↔ ana_pano_klemens_PT2_5_PE_16 |
| bağlantı elemanı (PEM/vida/somun) sac içinde; delik modellenmemiş | 48 | 7.50 | F_ust_arka_rakoru_230V_M20 ↔ f_ust_arka_sac; ana_besleme_kanali ↔ F_ana_hat_tavan_rakoru_M40; flap_katlayici_alt_bagi ↔ flap_katlayici_somun_kolu; govde_bag_arka_sag_1100_saplama ↔ arka_sac |
| aynı kablo/hortumun segmentleri birleşimde bindiriyor (tek parça) | 23 | 4.86 | hava_ana#0 ↔ hava_ana#1; hava_ana#0 ↔ hava_ana#5; hava_ana#1 ↔ hava_ana#10; hava_ana#1 ↔ hava_ana#12 |
| birim-içi mekanizma parçaları (B/Çekmeceler) | 21 | 0.35 | CEK_K1_lahm_1_motor_kasnagi ↔ CEK_K1_lahm_1_kayis_GT3; CEK_K1_lahm_2_motor_kasnagi ↔ CEK_K1_lahm_2_kayis_GT3; CEK_K1_lahm_3_motor_kasnagi ↔ CEK_K1_lahm_3_kayis_GT3; CEK_K1_lahm_4_motor_kasnagi ↔ CEK_K1_lahm_4_kayis_GT3 |
| mil ↔ yatak/göbek/kol geçmesi (birim-içi mekanizma) | 18 | 10.48 | besleyici_avara_yatagi ↔ besleyici_avara_mili; besleyici_kasnak_avara ↔ besleyici_avara_mili; harc__urun_mili ↔ harc__mil_kavramasi; kapak_kolu_mili ↔ kapak_kolu |
| sıkı geçme ≤0,2 mm (conta/rakor/kelepçe/burç) | 14 | 0.20 | F_firin_sinyal_kelepce_0 ↔ F_firin_sinyal; F_kutu_rakoru_230V_bina ↔ harting_F_soket; gider_ana_hatti_borusu ↔ gider_ana_hatti_kelepcesi_K3; hava_ana#2 ↔ f_ust_yan_sol |
| birim-içi mekanizma (aynı mek: E/Kutu katlama) | 9 | 0.07 | destek_motor_kaplin ↔ destek_motoru; flap_katlayici_kaplini ↔ flap_katlayici_motoru; kopru_kaplini ↔ kopru_motoru; kose_CNR_MB_motor ↔ kose_CNR_MB_kaplin |
| birim-içi mekanizma parçaları (TOPPING/Harç) | 8 | 13.59 | harc__pnomatik_on_bogaz ↔ harc__pnomatik_mil_D12; harc__pnomatik_silindir_D32 ↔ harc__pnomatik_mil_D12; harc_spreader_ucgen_dagitici ↔ harc_spreader_dagitici_boru; harc_spreader_ucgen_dagitici ↔ harc_spreader_merkez_tapasi |
| birim-içi mekanizma parçaları (TOPPING/Sos) | 8 | 13.59 | sos__pnomatik_on_bogaz ↔ sos__pnomatik_mil_D12; sos__pnomatik_silindir_D32 ↔ sos__pnomatik_mil_D12; sos_spreader_ucgen_dagitici ↔ sos_spreader_dagitici_boru; sos_spreader_ucgen_dagitici ↔ sos_spreader_merkez_tapasi |
| birim-içi mekanizma parçaları (E/Kutu katlama) | 8 | 5.00 | flap_lineer_burc_govdesi_0 ↔ flap_lineer_burc_0; kol_reduktoru ↔ kol_motoru; parmak_kasnak_alt ↔ parmak_kayisi; parmak_kayisi ↔ parmak_kasnak_ust |
| geçme konnektör (fiş soketin içinde) | 7 | 6.00 | harting_ANA_PANO_DOLAP_fis ↔ ana_pano_harting_soketi_DOLAP; harting_ANA_PANO_E_fis ↔ ana_pano_harting_soketi_E; harting_ANA_PANO_F_fis ↔ ana_pano_harting_soketi_F; harting_ANA_PANO_K_fis ↔ ana_pano_harting_soketi_K |
| birim-içi mekanizma (aynı mek: QR/Gözler) | 6 | 1.85 | goz_01_motor_kablosu ↔ goz_01_motor_braketi; goz_11_motor_kablosu ↔ goz_11_motor_braketi; goz_21_motor_kablosu ↔ goz_21_motor_braketi; goz_31_motor_kablosu ↔ goz_31_motor_braketi |
| kablo/hortum kanal-rakor-geçiş içinde | 5 | 14.00 | ana_hat_bina ↔ ana_ayirici_rakoru_alt_M32; kanal_TOPPING_KD1_dikey ↔ ana_hat_QR_guc; kanal_TOPPING_KD1_dikey ↔ ana_hat_bina; qr_kutu_rakoru_kart_modem ↔ qr_pano_alti_kablo_tavasi_kapak |
| birim-içi mekanizma parçaları (TOPPING/Kuşbaşı) | 4 | 10.00 | kusbasi__pnomatik_on_bogaz ↔ kusbasi__pnomatik_mil_D12; kusbasi__pnomatik_silindir_D32 ↔ kusbasi__pnomatik_mil_D12; kusbasi__urun_silindiri_bilezigi ↔ kusbasi__urun_silindiri_D70; kusbasi__urun_silindiri_kapagi ↔ kusbasi__urun_silindiri_D70 |
| birim-içi mekanizma parçaları (TOPPING/Kıyma) | 4 | 10.00 | kiyma__pnomatik_on_bogaz ↔ kiyma__pnomatik_mil_D12; kiyma__pnomatik_silindir_D32 ↔ kiyma__pnomatik_mil_D12; kiyma__urun_silindiri_bilezigi ↔ kiyma__urun_silindiri_D70; kiyma__urun_silindiri_kapagi ↔ kiyma__urun_silindiri_D70 |
| birim-içi mekanizma (aynı mek: F/Gövde) | 4 | 0.07 | onyuz_f_ust_gazli_yay_braketi_sag ↔ onyuz_f_ust_gazli_yay_sag_goz_a; onyuz_f_ust_gazli_yay_braketi_sol ↔ onyuz_f_ust_gazli_yay_sol_goz_a; onyuz_f_ust_kapak_sag_yay_pimi ↔ onyuz_f_ust_gazli_yay_sag_goz_b; onyuz_f_ust_kapak_sol_yay_pimi ↔ onyuz_f_ust_gazli_yay_sol_goz_b |
| PU köpük içine gömülü eleman | 3 | 1.12 | avara_rulosu_46 ↔ bant_sarim_46; evap_kaseti_PU ↔ silikon#15; tahrik_rulosu_EC5000_354 ↔ bant_sarim_354 |
| birim-içi mekanizma (aynı mek: E/Asansör) | 2 | 0.09 | asansor_kasnak_20 ↔ asansor_motoru; asansor_kasnak_40 ↔ asansor_kayisi |
| birim-içi mekanizma parçaları (E/Besleyici) | 1 | 6.29 | besleyici_kasnak_tahrik ↔ besleyici_motoru |
| birim-içi mekanizma parçaları (TOPPING/Tabla) | 1 | 0.46 | st_motor_adaptor_flansi ↔ st_tahrik_motoru |
| birim-içi mekanizma (aynı mek: F/Yükleme bandı) | 1 | 0.19 | yb_kasnak_motor ↔ yb_gt2_kayis |
| birim-içi mekanizma (aynı mek: TOPPING/Tabla) | 1 | 0.07 | st_kaplin ↔ st_tahrik_motoru |
