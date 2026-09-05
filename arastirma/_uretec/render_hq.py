# -*- coding: utf-8 -*-
# SVG -> PNG yuksek cozunurluk: Chrome headless, device-scale-factor 2.5 (metinler 2,5x piksel)
import sys, re, io, os, subprocess, struct, time
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
SCALE = float(os.environ.get('HQ_SCALE', '2.5'))
def size(svg):
    t = io.open(svg, encoding='utf-8').read(4000)
    w = int(float(re.search(r'<svg[^>]*\swidth="([\d.]+)"', t).group(1)))
    h = int(float(re.search(r'<svg[^>]*\sheight="([\d.]+)"', t).group(1)))
    return w, h
def png_size(p):
    with open(p,'rb') as f:
        f.seek(16); return struct.unpack('>II', f.read(8))
for svg in sys.argv[1:]:
    w, h = size(svg)
    png = svg[:-4] + '.png'
    url = 'file:///' + svg.replace('\\', '/')
    subprocess.run([CHROME, '--headless', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=%g' % SCALE,
                    '--window-size=%d,%d' % (w, h), '--screenshot=' + png, url], capture_output=True, timeout=120)
    time.sleep(0.5)
    pw, ph = png_size(png)
    print('%s -> %dx%d px (%.1fx)  %.0f KB' % (os.path.basename(png), pw, ph, pw / w, os.path.getsize(png) / 1024))
