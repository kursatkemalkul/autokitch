# 3 · TOPPING — PROBLEM DEFTERİ
Durumlar: **ÇÖZÜLDÜ** · **ÖNERİ VAR** (Kemal onayı bekliyor) · **AÇIK**.
Kapananlar silinmez, ÇÖZÜLDÜ olarak kalır. Güncelleme: 3 Eyl 2026 (v7 — haftalık tedarik)

| # | Problem | Durum | Çözüm / Not |
|---|---------|-------|-------------|
| T1 | **Sucuk batonu pide ORTASINDA biterse** (15 dilimin 7'sinde) — Kemal | ÖNERİ VAR | 3 katman: (1) **Başlamadan kontrol:** BEYİN her dozajı sayaçla düşer; sipariş başında "bu pide için yeterli mi?" teyidi — yetersizse dozaj HİÇ BAŞLAMAZ, yarım pide oluşamaz. (2) **Çift baton:** biri biterse makine ikinci batona otomatik geçer, kaldığı açıdan devam eder (tabla pozisyonu bilinir). (3) Her ikisi de biterse pide fırına gitmez, çiğ hâlde BEKLER + elemana uyarı — eleman baton yükler, kayıp yok |
| T2 | Kaşar rendesi topaklanır, akmaz (köprülenme) | ÖNERİ VAR | Titreşimli dozaj (vida değil — endüstri tercihi) + hazne içi köprü kırıcı çubuk; nem kontrolü (+3° kuru hava) |
| T3 | Kavurma yağlanıp vidaya yapışır | ÖNERİ VAR | Sökülebilir hazne+vida (eleman 3 günde bir yıkar); gerekirse titreşim destekli akış |
| T4 | Gramaj zamanla sapar (az/çok malzeme) | ÖNERİ VAR | Haftalık kalibrasyon: eleman boş kaba 1 dozaj alır, tartar, BEYİN'e girer (2 dk iş) |
| T5 | Hazne boşalması gün içinde | ÇÖZÜLDÜ | Kasette boş sensörü → ROBOT geçiş rafındaki doluyu takar (saat önemsiz); eleman haftada bir doldurur |
| T6 | Dozaj mekanizması seçimi | ÇÖZÜLDÜ | Küp/parça malzeme + kaset hazne + motorlu hücreli çark, her hazne kendi çıkışı (Kemal konsepti v3-v6) |
| T7 | Kuşbaşı çiğ hâlde 2-3 dk fırında pişmez | ÖNERİ VAR | Soteli/yarı pişmiş kuşbaşı (kavurma gibi) veya kuşbaşılı pideye ayrı uzun reçete |
| T8 | Yedek kaset raf ömrünü aşıyor (3+3 = 6 gün; kavurma/kuşbaşı 3-4 gün) | ÇÖZÜLDÜ (v7) | Kaset boyu = raf ömrü × tüketim: kaşar 35×42×25 (15 kg, 2,3 g) · sucuk 35×21×25 (10 kg haftalık) · kavurma/kuşbaşı 17×21×25 (3,5 kg, 2,3 g); 2.-3. kasetler STORE −18'de, 1 gün önce çözülür |
| T9 | TOPPING'e buzluk gerekir mi? | ÇÖZÜLDÜ (v7) | HAYIR — STORE'un mevcut −18 kolonu (≈36 L); TOPPING tek +3, 25 cm grup |
| T10 | Kavurma az/çok satıldı (kaset erken/geç bitti) | ÇÖZÜLDÜ (v7) | Saat kuralı (kavurma/kuşbaşı 3,5 g) dolan kaseti çıkarır (≤1 kg fire); donmuş kasetin saati durur, haftaya devreder; çok satışta robot erken çözer, biterse kiosk çeşidi kapatır |
| T11 | Kaşar 15 kg kasette topaklanma | ÖNERİ VAR | Sütun 25 cm'e indi; pilot testi, gerekirse çark miline köprü kırıcı kanat |
| T12 | Robot 15 kg kaset takası — kobot yükü, kulp, kapaklar | AÇIK | Kobot ≥12 kg sınıfı (UR16e / CRX-20), kaset kulpu = robot tutamağı, üst/alt kapak motorlu-sensörlü — robot turu |
| T13 | Farklı boy kasetlerde çıkışlar pideye simetrik gelmiyor | ÇÖZÜLDÜ (v7) | 4 çıkış tabla kayma ekseni üzerinde (±3 cm, x 30·39·45,5·53,5); tabla Ø36 kayar+döner → merkezden kenara spiral |
| T14 | Soğutma/elektrik erişimi | ÇÖZÜLDÜ (v7) | Teknik bölme EN ÜSTTE (soğutma 25 + elektrik 14), servis üstten; diğer istasyonlarda da (STORE) aynı ilke |
