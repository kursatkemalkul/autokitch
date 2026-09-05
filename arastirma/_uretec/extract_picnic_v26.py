# -*- coding: utf-8 -*-
# Kemal'in son mesajindaki 4 Picnic karesini transkriptten cikar -> 3_TOPPING/referans + otonom/img
import io, json, base64, os
F = r"C:\Users\Kemal\.claude\projects\C--Users-Kemal-Desktop-Kemal-WEBS-TE\75ad3429-265f-4f39-ba6b-c3380471965a.jsonl"
ROOT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH"
def find_images(obj, out):
    if isinstance(obj, dict):
        if obj.get('type') == 'image' and isinstance(obj.get('source'), dict) and obj['source'].get('data'):
            out.append(obj['source'])
        for v in obj.values(): find_images(v, out)
    elif isinstance(obj, list):
        for v in obj: find_images(v, out)
imgs = []
for line in io.open(F, encoding='utf-8', errors='replace'):
    if 'buda picnic works bence biz boyle kuralim' in line and '"base64"' in line:
        d = json.loads(line)
        if d.get('type') == 'user':
            find_images(d, imgs)
            break
print('bulunan gorsel:', len(imgs))
assert len(imgs) == 4, 'beklenen 4 gorsel'
names = ['picnic_reload_pepp', 'picnic_kap_helezon', 'picnic_kap_tarak', 'picnic_tarak_detay']
out = []
for src, nm in zip(imgs, names):
    raw = base64.b64decode(src['data']); mt = src.get('media_type', '')
    ext = {'image/jpeg': '.jpg', 'image/png': '.png', 'image/webp': '.webp'}.get(mt, '.jpg')
    ref = os.path.join(ROOT, 'arastirma', '3_TOPPING', 'referans', nm + '_5eyl' + ext)
    web = os.path.join(ROOT, 'otonom', 'img', nm + ext)
    open(ref, 'wb').write(raw); open(web, 'wb').write(raw)
    out.append((nm + ext, mt, len(raw)))
    print(nm, mt, len(raw), 'byte')
io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'picnic_v26_files.json'), 'w', encoding='utf-8').write(json.dumps(out))
