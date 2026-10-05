# TEK ÇEKMECE MONTAJ — DENETİM RAPORU (4 Eki 2026)

Sayfa: http://127.0.0.1:8766/claude-hat3-v8/otonom/hat/cekmece-montaj.html
Veri: otonom/hat3d/v3/cekmece_montaj/cekmece_montaj.glb (0,72 MB) + cekmece_montaj.json
Üreteç: gece2/cekmece/cikar.py (parça çıkarma) → cek_montaj.py (plan + denetim + çıktı) · denetçi: gece2/adim6/yol_denetim.py

## SONUÇ
| Ölçüt | Değer |
|---|---|
| Adım | 12 (50,5 s) |
| Hareket eden parça | 31 (+ 3 çekme/sarma) · çevre 9 öğe + tezgâh |
| Denetlenen parça çifti | 209 |
| Yol adımı | 2 mm (tüm hareketler; ray boyunca sürme dahil), üçgen düzeyinde sürekli çarpışma (CCD) |
| YOL ÇAKIŞMASI | **0** |
| Yerinde belirme | **0** (istisna: kablolar + kayış, aşağıda) |
| Havada parça | **0** (son konumda 31 parça + tezgâhta 10 + 4 parça ayrıca) |
| Son kare | 43 öğe kaynak modelle aynı yerde, en büyük fark 0,0005 mm |
| Tarayıcı | baştan sona oynatıldı (4×), konsol hatası yok |

Sayılmayanlar (Kemal kuralı): oturma teması (dinlenme konumuna ≤ 1 mm), ray↔kızak ve yüzeye paralel kayma ≤ 0,75 mm sıyırma.
Vida ↔ PEM somunu tam denetlendi: vida gövdesi PEM deliğinin içinde 0,045 mm boşlukla ilerliyor, temas yok.

## İSTİSNALAR / AÇIK NOTLAR
1. **MODEL HATASI — vida boyu:** 6 ray vidasının (M5 × 10 havşa) ucu köpük kapağının tabanını **3,97 mm** geçiyor
   (son konumda var; yol hatası değil). Rayın dış yüzünden kapak tabanına yalnız 3 mm diş boyu var.
   Öneri: M5 × 6 havşa vida ya da ≥ 5 mm daha derin köpük kapağı. Bu 6 çift yol denetiminden çıkarıldı ve sayfada not olarak yazıyor.
2. **Kayış yerinde sarılıyor:** kapalı GT3 kayış iki flanşlı kasnağa rijit hareketle takılamaz; animasyonda kablolar gibi yerinde
   uzayarak gelir. (Kemal'in istisnası yalnız kablo kanal çekmeydi — kayışı da bu sınıfa koydum, onay gerekir.)
   Son konumda kayış dişi kasnak dişine 36 üçgende geçiyor (modeldeki diş teması).
3. Kablolar (reed + motor) kanal boyunca çekilir — izinli istisna.
4. Motor grubu tezgâhta kuruluyor (dolabın içinde motor braketine hiçbir yönden giremiyor — dikey kablo kanalı +x yolunu kapatıyor).

## ADIMLAR
1. Tezgâh: motor grubu (braket, step motor + flanş kendi ekseninde, GT3 motor kasnağı mil ekseninde)
2. Motor grubu arka duvara (ön çerçeve açıklığından)
3. Sensör plakası · sabit raylar (önden, sonra yana → bölme sacına)
4. Ray vidaları (6 × M5 × 10, kendi ekseninde)
5. Avara braketi + sensör laması · 2 reed sensör
6. Ara raylar (ray ekseni boyunca)
7. Tezgâh: çekmece gövdesi · silikon tepsi
8. Tezgâh: kızak lamaları · kızaklar · kayış laması · mıknatıs · ön braketler
9. Çekmece ray ekseni boyunca 900 mm sürülür (kızak ara rayın içinde)
10. Avara kasnağı + mili · GT3 kayış
11. Ön panel · şeffaf ön kapak
12. Kablolar

## EKRAN GÖRÜNTÜLERİ
- 1_ray_vidalama.jpg (t 16,3) · 2_cekmece_ray_boyunca.jpg (t 35,6) · 3_tamamlandi.jpg (t 50,45)
