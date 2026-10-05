import sys, os, json, time
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
URL = 'http://127.0.0.1:8766/claude-hat3-v8/otonom/hat/b-montaj.html?t=0&foto=1&v=%d' % int(time.time())
KARE = [('1_acinim_duz', 14.15), ('2_bukum', 14.5), ('3_sase_kaynak_yakin', 2.6), ('4_pem_presleme', 31.5), ('5_kovan_kaynak', 33.5), ('6_yalitim_levhasi', 36.5),
        ('7_ic_sac_kapanir', 39.5), ('8_sogutma_grubu', 82.6), ('9_tahrik_vida', 92.9), ('10_iskelet_birlesim', 134.5), ('11_on_cerceve_avara', 143.5),
        ('12_raylar_vida', 148.5), ('13_cekmece_surme', 153.8), ('14_kayis_cenesi', 157.6), ('15_bitmis', 196.2)]
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', args=['--use-angle=d3d11', '--enable-webgl', '--ignore-gpu-blocklist'])
    pg = b.new_page(viewport={'width': 1400, 'height': 820})
    hata = []; log = []
    pg.on('console', lambda m: hata.append('%s: %s' % (m.type, m.text)) if m.type in ('error', 'warning') else log.append(m.text))
    pg.on('pageerror', lambda e: hata.append('pageerror: %s' % e))
    pg.goto(URL, wait_until='load'); pg.wait_for_function('window.__hazir === true', timeout=180000)
    T = pg.evaluate('__km.D.toplam'); tt = 0.0; n = 0
    while tt <= T + 1e-6:
        pg.evaluate('t => __km.git(t)', tt); pg.wait_for_timeout(16); n += 1; tt += 0.25
    for ad, t in KARE:
        pg.evaluate('t => __km.git(t)', t); pg.wait_for_timeout(1900)
        pg.screenshot(path=os.path.join(HERE, ad + '.jpg'), type='jpeg', quality=85)
    dog = pg.evaluate("document.getElementById('dog') ? document.getElementById('dog').innerText : ''")
    print('süre', T, 'kare', n, 'hata', len(hata), hata[:8]); print('log', log[:5]); print('DOG', dog)
    b.close()
