
## ADIM 8 · SERVİS DÜZELTMELERİ + ACİL STOP (gece 2 · 4 Eki 2026 · Claude) — adım 39–40

Betikler **yama_v9/ altında** (33–38 gibi `{YAMA}` ile çağrılır, ortak araç `sac_ent.py`; ortam aynı: `YAMA_IS_KOK`, `YAMA_URETEC`).

| # | betik | girdi → çıktı | ne yapar | doğrulama |
|---|---|---|---|---|
| 39 | `39_servis.py` | v9f → v9g | SERVIS.md D2–D4 · **D2** fırın üstü üst kaydı (F_UST_KABIN__sac 30×30×2) dikmenin sağında bölünür: sol parça kaynaklı, sağ parça x 3360–3996,5 sökülür (2 iç köşebent 5 mm lama + 4 × ISO 7380 M6×12, kayıt alt cidarında Ø6,6 delik), sağ uç kaynak dikişi silinir · **D3** yağ lansı emiş / dönüş hortumunda kapamalı hızlı kaplin (yeni düğüm K_YAG__kaplin; hortum kaplin boyunca kesilir) + seviye şalteri M12 fişi · **D4** kompresör çıkışında 4 turluk PU spiral servis halkası (z −391…−432; düz boru −437'den) + fişli besleme (yeni düğüm HAVA_KOMPRESOR__kablo: motor → hat içi fiş-priz → orta bölmede M16 rakor (Ø16 delik) → arka kablo rakoru) · **D1 uygulanmadı**: A istasyon kutusu modelde yok (A elektriksiz) | yeni parça çakışması 0 (yalnız rakor ↔ sac temas 0,02 mm³) |
| 40 | `40_acil_stop.py` | v9g → v9h | 6 acil stop (Schneider XB4BS8442 Ø40 + ZBY9330T Ø60): TOPPING (2440, 1000) · B depo çekmecesi önü (4300, 750; x ≤ 4330 → çekmece açılınca QR'a çarpmaz) · F sol üst kapak (2600, 1460) · K (4300, 1400) · E sağ üst (5150, 1300) · QR robot yüzü (5100, 1690, −z). Yeni düğümler ACIL_STOP__kirmizi / __sari / __siyah (kat 6, mek = istasyonun Elektrik grubu, kpk = kapakla gelir). Gövde (30 × 30 × 43) kapak katmanlarında cep açar (delik_ac). Kablo çizilmedi | yeni parça çakışması 0 |

Ortam değişkeni notu (zincir.py): bkz. yukarıdaki "Ortam" paragrafı; 39–40 ek bir değişken istemez. 39 m8kit'te değiştirilen üçgenleri `Karsi` görmeden önce ara GLB'ye yazıp yeniden yükler (m8kit eklenen üçgenleri kayıttan sonra görür).
Sayfaya giden kopya (W/otonom/hat3d/v3/hat3_v8.glb) zincir çıktısının **EXT_meshopt_compression** (kayıpsız, INDICES kodeği, bayt bayt geri açılır) sıkıştırılmış hâlidir: `gece2/adim8/kucuk/meshopt_kucult.mjs <ham> <sayfa> --idx seq`. Ham GLB (denetim / üreteç betikleri bunu okur) scratchpad'de `hat3_v9h.glb`.
