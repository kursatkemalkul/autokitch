import sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', args=['--use-angle=d3d11', '--ignore-gpu-blocklist'])
    for ist in (sys.argv[1:] or list('abeu')):
        pg = b.new_page(viewport={'width': 1400, 'height': 900}); err = []
        pg.on('pageerror', lambda e: err.append(str(e))); pg.on('console', lambda m: err.append(m.text) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:8766/claude-hat3-v8/otonom/hat/%s-montaj.html' % ist); pg.wait_for_function('window.__hazir === true', timeout=120000)
        pg.click('[data-h="4"]')
        T = pg.evaluate('__km.D.toplam')
        pg.wait_for_function('+document.getElementById("tz").value >= %f' % (T - 0.01), timeout=int(T / 4 * 1000 * 3) + 20000)
        sn = pg.evaluate('document.getElementById("sn").textContent')
        print(ist, 'oynatma sonu:', sn, 'hata', len(err), err[:3])
        pg.close()
    b.close()
