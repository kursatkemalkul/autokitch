# -*- coding: utf-8 -*-
"""adım 6 · her sayfayı baştan sona tarar (0,25 s adımla; konsol / sayfa hatası toplar) + 2 ekran görüntüsü (sac bitti, tümü bitti)"""
import sys, os, json, time
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
URL = 'http://127.0.0.1:8766/claude-hat3-v8/otonom/hat/%s-montaj.html'
istler = sys.argv[1:] or ['a', 'b', 'e', 'u']
SONUC = {}
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', args=['--use-angle=d3d11', '--enable-webgl', '--ignore-gpu-blocklist'])
    for ist in istler:
        pg = b.new_page(viewport={'width': 1400, 'height': 820})
        hata = []
        pg.on('console', lambda m: hata.append('%s: %s' % (m.type, m.text)) if m.type in ('error', 'warning') else None)
        pg.on('pageerror', lambda e: hata.append('pageerror: %s' % e))
        log = []
        pg.on('console', lambda m: log.append(m.text) if m.type == 'log' else None)
        pg.goto(URL % ist + '?t=0&foto=1', wait_until='load')
        pg.wait_for_function('window.__hazir === true', timeout=120000)
        D = pg.evaluate('({T: __km.D.toplam, A: __km.D.adimlar.map(a => [a.no, a.ad, a.t0, a.t1])})')
        T = D['T']
        # tarama
        t0 = time.time(); n = 0
        tt = 0.0
        while tt <= T + 1e-6:
            pg.evaluate('t => __km.git(t)', tt); pg.wait_for_timeout(16); n += 1; tt += 0.25
        tarama_sn = time.time() - t0
        # sac bitti = ilk "Mekanizmalar"/"Açıcı" adımının başı
        sac_t = next(a[2] for a in D['A'] if a[1].startswith(('Mekanizmalar', 'Açıcı')))
        for ad, t in (('sac_bitti', sac_t - 0.05), ('tum_bitti', T)):
            pg.evaluate('t => __km.git(t)', t); pg.wait_for_timeout(1800)
            pg.screenshot(path=os.path.join(HERE, '%s_%s.jpg' % (ist.upper(), ad)), type='jpeg', quality=85)
        SONUC[ist] = dict(toplam_sn=T, adim=len(D['A']), kare=n, tarama_sn=round(tarama_sn, 1), hata=hata, log=log, sac_bitti_t=sac_t)
        print(ist, 'süre', T, 'adım', len(D['A']), 'taranan kare', n, 'hata', len(hata), hata[:5], log[:3])
        pg.close()
    b.close()
json.dump(SONUC, open(os.path.join(HERE, 'foto_test_sonuc.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
