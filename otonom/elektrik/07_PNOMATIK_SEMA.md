# 07 · PNÖMATİK ŞEMA (7 Eki 2026 gece · Claude)

Kaynak: mekanizma tablosu (mekanizma_v3_8.json · */Hava üniteleri), üreteç BOM'ları (topping_cad_v31 · topping_uno_cad_v19 · kesme_cad_v10 · kutu_cad_v13 · h3_firin_ust_v1), zincir adım 60 (MS6-SV-E), güvenlik v2 §1c (K bıçak kilidi). Model değişmedi.

## 1. ŞEMA
```
KOMPRESÖR JUN-AIR OF302-15B (F üst kabin · 15 L tank · 8 bar maks · FAD 38 l/min @ 8 bar · 43 @ 7 · 51 @ 5 [K] · 230 V 0,44 kW · 65 dB)
 │  kompresör çıkış vanası (kompresor_cikis_vana) · spiral servis halkası (d4) · otomatik tank tahliyesi
 ▼
FESTO MS6-SV-E  güvenli yumuşak başlatma + hızlı boşaltma (PL e Kat 4 · GS_HAVA_ACIK · test ayda ≥ 1)   [adım 60]
 │  susturucu üstte
 ▼  ANA HAVA HATTI PU Ø8 (hava_ana · F üst kabin → üst hat kanalı · QSSF8 J1/J2/J3 geçme bağlantıları)
 ├──► TOPPING kolu  ── şartlandırıcı filtre + regülatör (sartlandirici_filtre_regulator + manometre, 6 bar [V]) ──► VALF ADASI SMC SY3000 (valf_adasi_SS5Y3 · 12 × 5/2 · D-sub 25 → EL2809)
 │        ├─ 5 × UNO piston silindiri Ø32 (harç · kıyma · patates · tavuk · kuşbaşı — pnomatik_silindir_D32, hız kısıcı) 
 │        ├─ 5 × döner valf aktüatörü (valf_dondurme_aktuatoru, 90°)
 │        ├─ 2 × yayıcı kesme valfi (harç · patates spreader_valf)
 │        ├─ fire sileceği SMC CJ2B10-20 (fire_silecegi_silindiri)
 │        └─ kıyma orta UNO Ø6 hortumları (kiyma_orta_hava_hortumu_D6 ×2)
 ├──► K kolu  ── şartlandırıcı SMC AW20-F02-A ──► 4 × SMC SY3120 (bıçak İN · bıçak ÇEK · itici · #3 kilit pimi ÇEK)
 │        ├─ bıçak silindiri Festo DGRF-C-63-125 (yıldız bıçak, KALIR) + KARAR (b2, 7 Eki): yay kapamalı kilit pimi Festo AEN-16-15-A-P-A-Z (tek etkili ÇEKEN: hava → pim dışarı, hava kesilince yay pimi boyunduruk deliğine iter; pim Ø12 1.4057, yalnız bıçak YUKARIDA hizalı) + 2 × SMT-8M-A (574334) → GS_K_BICAK_KILITLI (2 kanal, ana pano EL1904-5, W043) · valf SY3120 #3 → DO_K_KILIT_PIM · pim kesme hesabı: F = 1870 + 59 = 1929 N × 2 = 3858 N → τ 34,1 MPa / 121 MPa (%28) · HGL pilot çek valf ek önlem [güvenlik v2 §1c]
 │        └─ aktarma iticisi SMC MY1B16-250 kolsuz silindir + 2 × AS1201F-M5-06 hız ayar + 2 × D-M9BL
 ├──► E kolu  ── (hava_QSSF8_J3_E) ──► vakum ünitesi SMC ZK2G15K5RWA-08 (ejektör Ø1,5 · besleme + bırakma valfi · vakum anahtarı PNP DI_E_VAKUM_OK) → 4 vantuz (vakum_vantuz) + vakum manifoldu
 │        └─ Z silindiri SMC CDQ2B16-20DZ (vakum başlığı iniş) · valf EL2809'dan
 └──► (A: hava YOK — açıcı hazır alınır · F: hava yok · B: hava yok · QR: hava yok)
Her kolda: yüksek/alçak basınç ayrımı yok (tek 6 bar). Hortum PU Ø8 ana · Ø6 cihaz (SMC KQ2 geçme rakorlar · duvar geçişi KQ2E bulkhead).
```

## 2. HAVA TÜKETİMİ (tam yük 52 ürün/sa · sim 2. saat)
| Tüketici | Çevrim başına | Ürün başına | Saatlik (52 ürün) | Kaynak |
|---|---|---|---|---|
| UNO piston Ø32 × strok ≤ 100 (gidiş + dönüş, 6 bar) | V = 2 × 0,8 dm³ × 7 bar(a) ≈ 1,1 Nl | 1–2 doz | ≈ 100 Nl | [V] hesap: A = 8,0 cm², s 100 mm |
| Döner aktüatör 90° ×2 | ≈ 0,1 Nl | 1–2 | ≈ 10 Nl | [V] |
| Kesme valfi + fire sileceği CJ2B10-20 | ≈ 0,05 Nl | 1 | ≈ 3 Nl | [V] |
| K bıçak DGRF-C-63-125 (gidiş + dönüş) | 2 × 0,39 dm³ × 7 ≈ 5,5 Nl | 1 | ≈ 285 Nl | [V] hesap: A 31 cm² · s 125 |
| K kilit pimi AEN-16-15 (tek etkili, çekme) | 2,0 cm² × 1,5 cm × 7 ≈ 0,02 Nl | 1 | ≈ 1 Nl | [V] hesap: Ø16 · s 15 |
| K itici MY1B16-250 | 2 × 0,05 × 7 ≈ 0,7 Nl | 1 | ≈ 36 Nl | [V] |
| E vakum ejektör ZK2 (0,4 MPa'da 90 l/min hava) | 90 l/min × 3 s tutma ≈ 4,5 Nl | 1 kutu | ≈ 235 Nl | [K] SMC ZK2 föyü (kutu_cad_v13) |
| E Z silindiri CDQ2B16-20 | ≈ 0,05 Nl | 1 | ≈ 3 Nl | [V] |
| **Toplam** | | | **≈ 670 Nl/sa ≈ 11 Nl/min** | kaçak payı +%20 → ≈ 13 Nl/min |

**Kompresör:** FAD 38 l/min @ 8 bar → ortalama yük ≈ %35 (dükkân ısı hesabı %24 ile uyumlu) → **yeterli**; 15 L tank 6→8 bar arasında ≈ 30 Nl depolar, bıçak + ejektör aynı anda (≈ 10 Nl) tankı 1 bar'dan az düşürür. Sıcaklık: JUN-AIR ortam sınırı 40 °C [K], fırın üstü kabin 35 °C hesap (dükkân ısı) → sınırda, kabin fanları (4 × 4414 FL) şart.

## 3. GÜVENLİK (EN ISO 4414 · EN ISO 13849-1)
- Enerji kesilince MS6-SV-E hattı boşaltır; yeniden verildiğinde yumuşak dolum — beklenmedik hareket yok (adım 60).
- K bıçağı düşmez (b2): bıçak YUKARIDA iken yay kapamalı kilit pimi (AEN-16-15) boyunduruğa girer; hava kesilince pim kendiliğinden kilitler, 2 kanallı izleme GS_K_BICAK_KILITLI (EL1904-5); HGL pilot çek valf ek önlem (tek başına yeterli değil, Festo). Çevrim: bıçak üst + kilitli → DO_K_KILIT_PIM (pim çek) → pim dışarı → İN → ÇEK → üst → pim bırak → kilitli (program FB_Kesme 20/22/21/25/27; 2 s içinde olmazsa alarm 28 K_PIM_HATA). Yeniden başlatmada önce ÇEK tarafına basınç (DO_K_BICAK_CEK).
- UNO pistonları: hava kesilince ürün basıncı yok (döner valf hazneye döner), tehlike yok.
- E vakum: hava kesilince vantuz bırakır, karton düşer (tehlike yok).
- Tank 15 L: Basit Basınçlı Kaplar — tedarikçi CE'si (STANDART_DURUM §2).
- Bakım: ana şalter kilitlenince kompresör durur + MS6 boşaltır; tank kendi tahliye musluğuyla (adım 60 notu).

## 4. AÇIK
1. UNO silindir strok / çap teyidi (topping_uno_cad_v19: pnomatik_silindir_D32 — üretici kodu seçilmemiş: Festo DSNU-32 / SMC CDQ2B32).
2. Bölge bölge boşaltma (istasyon başına valf) istenirse model değişikliği (güvenlik v2 §3.2 notu).
3. Şartlandırıcı su kabı erişimi (SABAH soru 10: otomatik tahliyeli tip?).
4. E vakum: karton gözenekliliği denemesi (kutu_cad_v13 notu) — ejektör boyu değişebilir.
