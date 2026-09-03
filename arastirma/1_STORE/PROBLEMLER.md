# 1 · STORE (soğuk depo) — PROBLEM DEFTERİ
Durumlar: **ÇÖZÜLDÜ** · **ÖNERİ VAR** (Kemal onayı bekliyor) · **AÇIK**.
Kapananlar silinmez, ÇÖZÜLDÜ olarak kalır. Güncelleme: 31 Ağu 2026

| # | Problem | Durum | Çözüm / Not |
|---|---------|-------|-------------|
| S1 | Çekmece/raf motoru sıkışırsa robot bekler | ÖNERİ VAR | Motor akım sensörü sıkışmayı algılar → BEYİN o rafı devre dışı bırakır, diğer raftan devam; elemana uyarı |
| S2 | Servis kapağı açık kalırsa soğuk kaçar | ÇÖZÜLDÜ | Kapak switch'i + süre bekçisi: 60 sn açık kalırsa alarm; kapak motoru ters komutla tekrar dener |
| S3 | Donmuş top zamanında çözülmezse (çözülme senkronu) | ÇÖZÜLDÜ | Min-max kuralı + çözülme bekçisi 8-12 saat (mevcut karar); BEYİN eritmeyi satış tahminine göre önden başlatır |
| S4 | Elektrik kesintisi — soğuk zincir | ÖNERİ VAR | BEYİN mini UPS'te; dolap kapalı kasada 2-3 saat sıcaklık tutar; kesinti >30 dk ise elemana SMS/uyarı; jeneratör GEREKSİZ |
| S5 | Yanlış çukurdan alma / boş çukur | ÇÖZÜLDÜ | Kayıt defteri birincil + bilek kamerası alma anında doğrular (0,2 sn — mevcut karar) |
