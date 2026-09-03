# ARASTIRMA KLASÖR DÜZENİ (31 Ağu 2026)

Her istasyonun kendi klasörü var — o istasyonla ilgili çizim versiyonları,
belgeler, mail taslakları oraya gider. Yeni netlik = yeni versiyon, ilgili klasöre.

- 1_STORE    — soğuk depo (kiler): dolap/buzluk/içecek   [güncel karar hat çiziminde: v38]
- 2_PRESS    — Fersah PZP-400 + uç cepleri + çöp          [güncel: ist2_pres_detay_v4]
- 3_TOPPING  — dozaj/malzeme (hazne kulesi kararı AÇIK)
- 4_OVEN     — fırın
- 5_PACK     — kesim + kutu (kutu şema/mail arşivi burada) [kutu katlama artık ELEMAN işi]
- 6_PICKUP   — QR teslim dolabı
- 7_SERVICE  — servis istasyonu (ayrı ünite)
- FULL_MAKINE — bütün istasyonların BİR ARADA olduğu çizimler:
    hat_on_gorunus_teknik_v3..v38 (ön görünüş serisi; v38 GÜNCEL)
    hat_plan_* (yerleşim planları v32-v37 — yerleşim kararı SONRA)
    kombine_el_detay (robot eli)
- _uretec    — tüm çizimlerin Python üreteçleri (teknik_cizimN.py vb.)

İstasyon isimleri (ONAYLI): 1 STORE · 2 PRESS · 3 TOPPING · 4 OVEN · 5 PACK · 6 PICKUP (+SERVICE)
İstek üzerine tüm istasyonlar birleştirilip tek "full makine" çizimi üretilir (_uretec'ten).
