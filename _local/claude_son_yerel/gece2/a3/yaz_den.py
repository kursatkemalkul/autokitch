# -*- coding: utf-8 -*-
"""denetim.md (sonuc_a3.json + a_montaj.json + foto log'undan)"""
import json, os, sys, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'sonuc_a3.json'), encoding='utf-8'))
W = r'C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\otonom\hat3d\v3\a_montaj\a_montaj.json'
J = json.load(open(W, encoding='utf-8'))
FOTO = sys.argv[1] if len(sys.argv) > 1 else ''
L = []
L.append('# A MONTAJ v3 — DENETİM (4 Eki 2026)\n')
L.append('Sayfa: http://127.0.0.1:8766/claude-hat3-v8/otonom/hat/a-montaj.html · süre %.0f s · %d adım · %d öğe (%d silik çevre) · model hat3_v9l (zincir 00–44) + zincir_A_tamamla.py (S kopyası hat3_v9l_A.glb; ana GLB DEĞİŞMEDİ)\n'
         % (J['toplam'], len(J['adimlar']), D['parca'], D['cevre']))
temiz = D['cakisma'] == 0 and not D['uretim_kare_sorun'] and D['belirme'] == 0 and not D['havada'] and not D['son_konum']
L.append('## SONUÇ: %s\n' % ('TEMİZ — kural 17–18 tutuyor (model tamamlaması zincire eklenince ana modelle aynı olur)' if temiz else 'SORUN VAR — yayımlanmaz'))
L.append('| ölçüt | değer |\n|---|---|')
L.append('| yol çakışması (2 mm, üçgen CCD, %d çift; kapak dönüşü poz-poz) | **%d** |' % (D['cift'], D['cakisma']))
L.append('| büküm kareleri (o an görünen parçalara karşı) | %d sorun |' % len(D['uretim_kare_sorun']))
L.append('| yerinde belirme | %d (istisna: kaynak dikişi ve punta işaretleri birleşme anında büyür; silik çevre) |' % D['belirme'])
L.append('| havada | %d |' % len(D['havada']))
L.append('| son konumda kesişim (0,3 mm düzlem payı) | %d çift |' % len(D['son_konum']))
L.append('| bükümlü sac (açınımdan kurulan ağ) ↔ model kutusu | en büyük %s mm |' % max(x[1] for x in D['sac_model']))
L.append('| son kare ↔ model (tarayıcı, bbox) | %s |' % (FOTO or '—'))
L.append('| plan anı yol seçimi sorunu | %d |\n' % len(D['plan_sorun']))
L.append('## VİDA / DELİK / DİŞ (kural 18 · eksen boyunca ölçü, delik geçişi = son konumda kesişim yok)\n')
L.append('| eleman | adet | karşı diş | kavrama mm | diş boyu mm | uç taşma mm | delik |\n|---|---|---|---|---|---|---|')
oz = collections.OrderedDict()
for r in D['vida']:
    k = (r['std'], r['karsi']); oz.setdefault(k, []).append(r)
for (std, ka), R in oz.items():
    f = lambda key: '%s' % (min(x[key] for x in R) if min(x[key] for x in R) == max(x[key] for x in R) else '%s–%s' % (min(x[key] for x in R), max(x[key] for x in R)))
    L.append('| %s | %d | %s | %s | %s | %s | %s |' % (std, len(R), ka, f('kavrama_mm'), f('dis_boyu_mm'), f('uc_tasma_mm'), 'TEMİZ' if all(x['delik_gecis'] == 'TEMİZ' for x in R) else 'KESİŞİM'))
L.append('''
Notlar: M5 × 6 → PEM SP-M5-1 (1 mm iç tava) kavrama 2,0 = PEM dişinin tamamı (sacta PEM ile, B v3 ray vidalarıyla aynı kabul). M8 × 16 (A → TOPPING) PEM'i 6,1 mm geçer, ucu
TOPPING köpük kapağındaki cebe girer (model böyle; kapalı kapak istenirse M8 × 10 yeter — TOPPING sahibi). M6 × 16 ray cıvatası PEM'i 5,6 mm geçer, plaka altı boş.
Menteşe gövdesi M5 × 12: 8 mm dişin 7'si kavranır, uç gövdede kalır (−1,0).
''')
L.append('## MODEL TAMAMLAMA — zincir_A_tamamla.py (S\\gece2\\a3\\, girdi GLB → çıktı GLB, düğüm adı tabanlı)\n')
L.append('''Ana GLB'ye DOKUNULMADI; betik S kopyasına uygulandı (hat3_v9l → hat3_v9l_A.glb) ve animasyon bu hâle göre kuruldu. Koordinatör zincire ekleyecek.

| # | açık | düzeltme | düğüm |
|---|---|---|---|
| A1 | A → B 6 × M8 × 25 başının altındaki DIN 9021 pul Ø24, kaide borusu / plaka / damlama sacındaki Ø16 servis deliğinden GEÇEMEZ (boru kapalı, kaynaklı) | ISO 7092 M8 küçük seri pul 8,4 / 15 × 1,6; cıvata 0,4 aşağı (kavrama 17) | A_GOVDE__paslanmaz (köşe taşıma) |
| A2 | açıcı kolonu 4 × M8 × 20 başı flanştan 1,5 mm havada; arayüz şartı "M8 + DIN 125", pul yok | DIN 125-1 M8 pul (902,0–903,6) eklendi, cıvata 0,1 yukarı | A_GOVDE__paslanmaz (+1024 üçgen, sona) |
| A3 | tabla rayı 4 × M6 × 16 başı ray tabanından 5,0 mm havada | cıvata 5,0 aşağı (baş ray tabanına; PEM SP-M6 dişi tam, uç 5,6 geçer) | A_GOVDE__paslanmaz |
| A4 | açıcı modelinin taban flanşı 120 × 50 (z −660…−610); A gövdesi 4 köşe Ø9 (90 × 125, z −645 / −520) bekliyor → öndeki 2 cıvata boşluğa basıyordu | temsili ürün flanşı şartnameye göre 120 × 155'e uzatıldı (z −610…−505, 2 × Ø9) — gerçek üründe flanş ya da 8,5 mm adaptör plakası satın alırken doğrulanmalı (Kemal kararı) | TOPPING_MODUL__sac (mek A/Açıcı, +276 üçgen) |

Kendi kontrolü: her işlemde beklenen bileşen sayısı bulunmazsa betik durur; dokunulmayan köşeler bayt aynı kalır; yeni üçgenler primitif sonunda (ent indisleri geçerli).
''')
L.append('''## BEYANLI KABULLER

- Punta işaretleri modelde yok (h3_a_sac_v1 puntaları yalnız etiket): animasyonda 0,1 mm × Ø5 işaret olarak birleşme anında belirir — damlama sacı 9, iç tava ↔ dış tava 30, karşılık plakaları 6. Son konumda hiçbir parçayla kesişmez.
- Dikme tapası alın kaynağı taşlanır (dikiş katısı yok, tapa vurgulanır). Diğer bütün kaynaklar (kaide 20, delik kaynağı 16, dikme ↔ damlama 8, halka 8, kulak 44, dış tava köşe 4) modeldeki dikişlerdir.
- Arka sacın 13 somunu: saplama dikmenin / kaide borusunun / üst halkanın tam arkasında, eksenden somun takılamaz → pul + somun önce 13,5 mm yarığa yandan sürülür, arka sac arkadan gelir, somun SW8 ile döndürülür (h3_a_sac_v1 notuyla aynı).
- Kapak kaldır-çıkar menteşesi temsili ölçülü (Southco R6 / EMKA 1046 sınıfı): 0–180° dönüş poz denetimi temiz; "pime iner" adımı 25 mm düşey iniş olarak gösterildi.
- Açıcı tek ürün; denetim ağı için kafa ve kolon ayrı düğüm, birlikte hareket eder (sayfada tek ürün).
- Çevre (silik): B dolabının kabuk sacları + üst kiriş + GFRP + perçin somunları baştan; TOPPING gövdesi, sol duvar PEM'leri ve tabla rayı tabanı yalnız 11. adımda (TOPPING sahibi). Çevre yol denetimine engel olarak girer.
- A içinden kablo / kanal / hortum geçmez; acil stop yok.
''')
L.append('## GÖRÜNTÜLER (S\\gece2\\a3\\)\n')
for f in sorted(os.listdir(HERE), key=lambda x: (len(x.split('_')[0]), x)):
    if f.endswith('.jpg'): L.append('- %s' % f)
open(os.path.join(HERE, 'denetim.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('\n'.join(L[:16]))
