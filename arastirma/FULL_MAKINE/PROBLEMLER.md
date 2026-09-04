# GENEL — robot · BEYİN · altyapı — PROBLEM DEFTERİ
Durumlar: **ÇÖZÜLDÜ** · **ÖNERİ VAR** (Kemal onayı bekliyor) · **AÇIK**.
Kapananlar silinmez, ÇÖZÜLDÜ olarak kalır. Güncelleme: 31 Ağu 2026

| # | Problem | Durum | Çözüm / Not |
|---|---------|-------|-------------|
| G1 | Robot kol arızası — hat durur | ÖNERİ VAR | Yedek kombine el uç istasyonunda (takma otomatik); mekanik arızada eleman tezgahtan satışı manuel sürdüremez → makine kapalı, BEYİN kioskta "servis dışı" gösterir; servis sözleşmesi (entegratör SLA) şart |
| G2 | İnternet kopması | ÇÖZÜLDÜ | Yerel çalışır (mevcut karar — PLC + mini PC); yalnız uzak izleme düşer |
| G3 | Elektrik kesintisi — sipariş ortasında | ÖNERİ VAR | UPS yalnız BEYİN'i tutar (temiz kapanış + durum kaydı); güç gelince yarım işler ÇÖP'e, kuyruk baştan; kioskta bilgi |
| G4 | Kol kalibrasyonu kayarsa (çarpma vb.) | ÖNERİ VAR | Sabit referans noktaları (her istasyonda 1 nokta) + bilek kamera haftalık oto-kalibrasyon turu |
| G5 | Hijyen denetimi (belediye/tarım) | AÇIK | Ruhsat gereksinimlerine İstasyon temizlik kayıt defteri eklenecek (BEYİN loglar) — ayrı turda |
| R-T1 | Pideye doğrudan temas / hizalama | ÇÖZÜLDÜ (4 Eyl, Kemal) | Pide press'ten kutuya kadar TEPSİDE; robot tepsi ucu (kilitli) + pençe ucu, uç değiştirici |
| R-T2 | Sıcak tepsi ile uç | ÖNERİ VAR | Metal-metal kilit; silikon pençe sıcak tepsiye dokunmaz |
| R-T3 | Tepsi havuzu / yıkama (8-10 tepsi, ~80/gün) | AÇIK | Kemal ile ayrıca |
| R-T4 | Kol doluluğu ~%85 (103 sn/pide) | AÇIK | Pilot zaman etüdü |

---
