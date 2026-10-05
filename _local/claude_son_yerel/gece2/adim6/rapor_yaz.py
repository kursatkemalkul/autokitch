# -*- coding: utf-8 -*-
import json, os, sys, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WT = r'C:/Users/Kemal/Desktop/Kemal/WEBSİTE/AUTOKITCH_COORDINATION/worktrees/claude-hat3-v8'
L = ['# Montaj animasyonu · YOL ÇAKIŞMA DENETİMİ (4 Eki 2026)', '',
     'Yöntem: her hareketli parçanın bağıl yolu ≤ 5 mm adımlarla örneklenir, ardışık örnekler arası **sürekli** (CCD) üçgen denetimi: köşe→üçgen, üçgen←köşe, kenar×kenar taraması. '
     'O anda yerinde olan + aynı adımda daha önce oturmuş + aynı anda hareket eden bütün parçalar engel. Oturma teması (dinlenme konumuna ≤ 1,0 mm) ve yüzeye paralel kayma sayılmaz. '
     'Son konumda zaten geçme olan çiftler (vida → PEM, ürün → silikon mat vb.) yol denetiminden hariç tutulur (sayısı tabloda). Kapak dönüşleri ≤ 2°/poz üçgen-üçgen.',
     'Düzeltme: çakışan hareket grubu için sırayla özgün yön → yukarıdan → önden → arkadan → yanlardan → iki aşamalı yol (açık taraftan yaklaş + kısa son oturma) → kısa yaklaşma; '
     'vida / pul / somun / saplama YALNIZ kendi ekseninde. İlk çakışmasız aday seçilir; adım metnine yeni yön yazılır, kamera yeni yöne bakar.', '',
     '| İstasyon | Adım | Parça | Hareketli | Hariç (son konum geçme) | Çakışan çift ÖNCE | SONRA | Yönü değişen grup | Çözülemeyen | Havada sac |',
     '|---|---|---|---|---|---|---|---|---|---|']
DET = []
for ist in sys.argv[1:]:
    f = os.path.join(HERE, 'yol_rapor_%s.json' % ist)
    if not os.path.exists(f): continue
    r = json.load(open(f, encoding='utf-8'))
    j = json.load(open(os.path.join(WT, 'otonom', 'hat3d', 'v3', '%s_montaj' % ist.lower(), '%s_montaj.json' % ist.lower()), encoding='utf-8'))
    L.append('| %s | %d | %d | %d | %d | %d | **%d** | %d | %d | %d |' % (ist, len(j['adimlar']), r['parca'], r['hareketli'], r['haric_cift'], len(r['once']), len(r['sonra']),
                                                                    len(r['degisen']), len(r['cozulmeyen']), len(r.get('havada', []))))
    DET.append('')
    DET.append('## %s' % ist)
    c = collections.Counter(x['olay'][:90] if 'olay' in x else '' for x in r['once'])
    ol = j['olaylar']
    def olay_at(t):
        m = ''
        for tt, mm in ol:
            if tt <= t + 1e-6: m = mm
        return m
    # önce: olay bazında
    grp = collections.OrderedDict()
    for x in sorted(r['once'], key=lambda x: x['t']):
        grp.setdefault(round(x['w'][0], 1), []).append(x)
    DET.append('### Önce bulunan içinden geçmeler (pencere başı → örnek çift)')
    for w, xs in grp.items():
        x = xs[0]
        DET.append('- t %.1f s · %d çift · ör. `%s` ↔ `%s` (%.0f mm)' % (w, len(xs), x['a'], x['b'], x['derin']))
    DET.append('### Yönü değişen gruplar')
    for d in r['degisen']:
        DET.append('- t %.2f · %d parça (`%s`…) · eski %s → **%s** · %s' % (d['t0'], len(d['grup']), d['grup'][0], d['eski'], d['yeni'], olay_at(d['t0'])[:110]))
    if r['cozulmeyen']:
        DET.append('### Çözülemeyen')
        for g, n in r['cozulmeyen']: DET.append('- %s (%d parça) — %s' % (g[0], len(g), n))
    if r['sonra']:
        DET.append('### SONRA kalan')
        for x in r['sonra']: DET.append('- t %.2f `%s` ↔ `%s` %.0f mm' % (x['t'], x['a'], x['b'], x['derin']))
    if r.get('havada'):
        DET.append('### Havada (oturduğu anda hiçbir yerinde parçaya değmeyen) sac / profil')
        for h in r['havada']: DET.append('- `%s`' % h)
    DET.append('### Adım listesi')
    for a in j['adimlar']: DET.append('%d. **%s** — %s' % (a['no'], a['ad'], a['liste']))
open(os.path.join(HERE, 'yol_denetim.md'), 'w', encoding='utf-8').write('\n'.join(L + DET) + '\n')
print('\n'.join(L))
