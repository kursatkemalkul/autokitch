import sys, os, json, time
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
URL = 'http://127.0.0.1:8766/claude-hat3-v8/otonom/hat/topping-montaj.html?t=0&foto=1&v=%d' % int(time.time())
KARE = [('t1_kaide', 12.0), ('t2_kuru_bolme_kanal', 40.0), ('t3_arka_levha', 52.0), ('t4_ic_sac_levha', 70.0), ('t5_percin', 98.0), ('t6_uno_kaset', 120.0), ('t7_cerceve_silikon', 133.0), ('t8_evaporator_ayak', 146.5), ('t9_servis_saci_dimple', 156.0), ('t10_bitmis', 173.5)]
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
