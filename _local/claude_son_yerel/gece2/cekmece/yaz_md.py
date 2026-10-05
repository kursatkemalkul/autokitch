# -*- coding: utf-8 -*-
import pickle, json, sys, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
D = pickle.load(open('plan_v2.pkl', 'rb'))
L = ['# TEK ÇEKMECE MONTAJ PLANI v2 — B · K2 sütunu · 3. sıra (CEK_K2_lahm_3)', '',
     'Kurallar: MONTAJ_ANIMASYON_KURALLARI.md (19 madde). Üreteç: cek_montaj_v2.py (plan + zaman) → cek_v2_cikti.py (denetim + GLB/JSON). Model: hat3_v9j (ray vidası M5×6 = zincir 43).',
     'Açık taraf: bölme yalnız önden (çerçeve açıklığı x 1453,5–2073,5 · y 416,5–491,5). Montaj tezgâhı dolabın önünde (çekmece +z 900), üretim tezgâhı sağda (lazer/abkant noktası x 2470 z 560 + hazır rafı).', '',
     '| # | adım | parça | işlem | yön | bağlantı elemanı (adet) |', '|---|---|---|---|---|---|']
rows = [
    (1, 'köşebent ×4 (EKLENDİ)', 'lazer açınım (Ø4,5) → abkant 1 büküm', '—', '—'),
    (2, 'motor braketi 3 mm', 'lazer (Ø22,5 + 4×M3 havşa + 2×M5 havşa) → abkant 1 büküm', '—', '—'),
    (2, 'sensör plakası 2 mm', 'lazer, düz', '—', '— (model açığı A3)'),
    (3, 'avara kolu 2 + sensör laması L 2 + avara mili', 'lazer → abkant 2 + 1 büküm → TIG (kulak↔lama) + saplama kaynağı (mil↔kol)', 'lama alttan, mil +x', 'TIG 3 dikiş · saplama kaynağı'),
    (4, 'ray ünitesi sol/sağ (Accuride DZ3832, katalog)', 'iç eleman (kızak) ray ekseni boyunca öne çekilip ayrılır', '+z', '—'),
    (5, 'motor braketi', 'önden açıklıktan → arka duvar', '−z', 'DIN 7991 M5×6 (2) → PEM SP-M5 arka iç sac (EKLENDİ)'),
    (6, 'step motor', 'önden, sonra ekseni boyunca braket deliğine', '−z, −x', 'DIN 7991 M3×6 (4) → redüktör M3 dişi'),
    (7, 'GT3 motor kasnağı', 'mil ekseninde', '+x', 'DIN 913 M3×4 setskur (1)'),
    (8, 'sensör plakası', 'önden arka duvara', '−z', 'YOK — model açığı A3'),
    (9, 'ray ünitesi sol/sağ (dış+ara)', 'önden, yana bölme sacına', '−z, ∓x', 'DIN 7991 M5×6 (6) → PEM SP-M5 (var), ara eleman erişim deliğinden'),
    (10, 'avara ünitesi', '21 alçaktan açıklık → sola → yükselir → çerçeve arkası', '−z, −x, +y, +z', 'kör perçin Ø3,2 ISO 15983 (2), önden'),
    (10, 'GT3 avara kasnağı · reed ×2', 'mil ekseninde · yandan', '−x · −x', '— (E segman payı yok; reed deliği yok — açık)'),
    (11, 'kutu: taban 2 + yan ×2 + arka + ön 1 mm', 'lazer düz → montaj tezgâhı', 'üstten', 'TIG 4 dikiş'),
    (12, 'lama sol/sağ 6×17,3×616', 'kesim boyu + 2×M4 dişli kör delik → kutu yanına', 'yandan', 'punta 4+4'),
    (13, 'ön braket sol/sağ 2 mm', 'lazer (2×Ø5,5) → abkant 2 büküm → kutu önü', 'önden', 'punta 2+2'),
    (14, 'çene alt gövde · üst çene · tepsi', 'lama parçaları TIG → kutuya TIG; üst çene rafa; tepsi serbest', 'yandan / üstten', 'TIG 2+2'),
    (15, 'köşebent ×4 · kızak ×2', 'köşebent lamaya; kızak köşebent dik koluna', 'üstten / yandan', 'ISO 7380 M4×6 (4) → lama M4 dişi · punta 2×4 (ÖNERİ)'),
    (16, 'çekmece grubu', 'ray ekseni boyunca 900 mm; montaj tezgâhı çekilir', '−z', 'kızak ↔ ara eleman bilyalı kafes'),
    (17, 'kayış · üst çene · mıknatıs', 'kayış sarılır (istisna); üst çene üstten', '−y', 'ISO 7380 M3×10 (2) + ISO 4032 M3 (2)'),
    (18, 'kapak dış kabuk 1,5 · iç panel 1,0', 'lazer → abkant 8 büküm; iç panel + PEM pres; iç panel kabuğa', '—', 'PEM FHS-M5-10 (4)'),
    (19, 'fitil · ön kapak', 'fitil kanala; kapak saplamaları braket deliklerinden', '+z · −z', 'DIN 125 M5 (4) + ISO 4032 M5 (4), U braketin açık yanından'),
    (20, 'kablolar', 'kanal boyunca (istisna)', '—', '—')]
for r in rows:
    a = D['ADIM'][r[0] - 1]; L.append('| %d | %s | %s | %s | %s | %s |' % (r[0], a['ad'], r[1], r[2], r[3], r[4]))
L += ['', 'Bükümler (sırayla, iç R = t; model köşeleri keskin → kesim boyunda K 0,45 ile düşülür):']
for a, s in D['SAC'].items():
    if s['bukum']: L.append('- %s (t %.1f): ' % (a, s['t']) + ' → '.join('%d %s %d°' % (b['no'], b['ack'], b['aci']) for b in s['bukum']))
open('plan_v2.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n')
R = json.load(open('sonuc_v2.json', encoding='utf-8'))
M = ['# TEK ÇEKMECE MONTAJ v2 — DENETİM (4 Eki 2026)', '',
     'Sayfa: http://127.0.0.1:8766/claude-hat3-v8/otonom/hat/cekmece-montaj.html · veri otonom/hat3d/v3/cekmece_montaj/ (GLB 1,47 MB, morph hedefli) · süre %.0f s · %d adım' % (D['TOPLAM'], len(D['ADIM'])), '',
     '## SONUÇ: GEÇMEDİ — 2 model açığı (kural 19: Kemal kararı gerekli)', '',
     '| ölçüt | değer |', '|---|---|',
     '| yol çakışması (2 mm, üçgen CCD, %d çift) | **%d** — ikisi de model açığı (A1, A3) |' % (R['cift'], R['cakisma']),
     '| üretim kareleri (büküm / çevirme ↔ tezgâh + görünen parçalar) | %d |' % len(R['uretim_kare_sorun']),
     '| yerinde belirme | %d (istisna: kayış, kablolar, kaynak dikişleri) |' % R['belirme'],
     '| havada | %d |' % len(R['havada']),
     '| son konum | tarayıcıda 104 öğe, en büyük fark 0,0005 mm; üretilen saclar ↔ model kutu farkı ≤ 0,0001 mm |',
     '| tarayıcı | baştan sona oynatıldı, konsol hatası yok |', '',
     '## MODEL AÇIKLARI (düzeltilmeden yayın yok)',
     '- **A1 · kayış çenesi ↔ avara kasnağı:** çene (y 457,95–466,5, x 1470,5–1483,5) çekmece sürülürken avara kasnağının (y ≤ 463,5) içinden geçiyor. Kasnak çekmeceden sonra da takılamaz (kapalıyken kutu, açıkken çene kolu yolu kapatıyor). Öneri: çene bloğu kola kaynaklı değil, çekmece açıkken 2 × M3 ile bağlanan ayrı parça.',
     '- **A3 · sensör plakası:** kablo kanalının (ELK_IC) içinde, sensör lamasına bağlı değil (lama ucu 32 mm önde). Bağlantı yapılmadı. Öneri: plakayı kaldır ya da lamayı arka duvara uzatıp plakayla vidala.', '',
     '## DİĞER AÇIKLAR',
     '- Ray vidası DIN 7991 M5×6 (zincir 43, ayrı commit 3f62a79): uç köpük kapağı tabanına 0,77 mm baskı yapıyor (kapak iç tabanı = PEM arkası) — kapak 1 mm derin olmalı.',
     '- PEM SP-M5/M4 diş boyu 2,0 mm (proje katalog tablosu) < 1×d; kural 18 "sacta PEM ile" diye yorumlandı — teyit gerekir.',
     '- Kızak ↔ lama: modelde bağ yoktu (1 mm temas). Köşebent 1,5 × 4 + ISO 7380 M4×6 eklendi; kızak ↔ köşebent PUNTA önerisi (iç eleman ↔ ara eleman arası 1 mm, vida başı sığmıyor).',
     '- Reed ×2 ve mıknatıs (Littelfuse 59135 / 57135): montaj delikleri / flanş yüzü modelde yok — bağlantısız oturuyor.',
     '- Avara mili ucu E segman (DIN 6799) için 1 mm uzamalı.',
     '- Kör perçin delikleri flanş kenarına 1,35 mm (DFM sınırda).',
     '- Modele eklenecek (çevre): arka iç sacda 2 × PEM SP-M5 + köpük kapağı (motor braketi), ön çerçevede 2 × Ø3,3 perçin deliği. Sütunun dikey kablo kanalı (B_KABLO) tahriklerden sonra takılır (animasyonda yok).',
     '- Ön kapakta PU köpük modelde yok.', '',
     '## ÜRETİLEN ↔ MODEL KIYAS (hacim farkı = eklenen delikler)']
for k, v in R['kiyas'].items(): M.append('- %s: %s' % (k, v))
M += ['', '## VİDA / DELİK / DİŞ (kural 18)', '| eleman | delik | karşı diş | kavrama mm | uç taşma mm |', '|---|---|---|---|---|']
for v in R['vida']: M.append('| %s %s | %s | %s | %s | %s |' % (v['eleman'], v['std'], v['delik'], v['karsi'], v['kavrama_mm'], v['uc_tasma_mm']))
M += ['', '## HARİÇ TUTULAN ÇİFTLER'] + ['- %s: %s' % (k, v) for k, v in R['haric'].items()]
M += ['', 'Ekran görüntüleri: v2_acinim_duz · v2_acinim_bukum · v2_kapak_bukum · v2_pem_presleme · v2_vidalama_yakin · v2_profil_birlesim · v2_ray_boyunca_surme · v2_bitmis (.jpg)']
open('denetim_v2.md', 'w', encoding='utf-8').write('\n'.join(M) + '\n')
print('ok')
