# -*- coding: utf-8 -*-
# Site: TOPPING bolumune v24 + kap_geometri_v1 + Picnic referans gorseli; HAT gorselini v45 yap · Picnic gorselini transkriptten cikar
import io, json, base64, os
F = r"C:\Users\Kemal\.claude\projects\C--Users-Kemal-Desktop-Kemal-WEBS-TE\75ad3429-265f-4f39-ba6b-c3380471965a.jsonl"
def find_images(obj, out):
    if isinstance(obj, dict):
        if obj.get('type') == 'image' and isinstance(obj.get('source'), dict) and obj['source'].get('data'):
            out.append(obj['source'])
        for v in obj.values(): find_images(v, out)
    elif isinstance(obj, list):
        for v in obj: find_images(v, out)
imgs = []
for line in io.open(F, encoding='utf-8', errors='replace'):
    if 'bunuda seye ekle' in line and '"base64"' in line:
        find_images(json.loads(line), imgs)
assert imgs, 'Picnic gorseli bulunamadi'
src = imgs[-1]; raw = base64.b64decode(src['data']); mt = src.get('media_type', '')
ext = {'image/jpeg': '.jpg', 'image/png': '.png', 'image/webp': '.webp'}.get(mt, '.jpg')
ROOT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH"
ref = os.path.join(ROOT, 'arastirma', '3_TOPPING', 'referans', 'picnic_istasyon_5eyl' + ext)
web = os.path.join(ROOT, 'otonom', 'img', 'picnic_istasyon' + ext)
open(ref, 'wb').write(raw); open(web, 'wb').write(raw)
print('picnic gorseli:', mt, len(raw), 'byte →', os.path.basename(web))
webname = 'img/picnic_istasyon' + ext

p = os.path.join(ROOT, 'otonom', 'index.html')
t = io.open(p, encoding='utf-8').read()
def rep(o, n, c=1):
    global t
    assert t.count(o) == c, 'A(%d): %s' % (t.count(o), o[:80])
    t = t.replace(o, n)

# ---- TOPPING: baslik + guncel karar + v24 + iki referans gorsel + eski metni arsiv etiketi ----
rep('İSTASYON 3 · TOPPING — MALZEME DOZAJI — ✔ KONSEPT KARAR (Kemal krokisi)</div>',
    'İSTASYON 3 · TOPPING — MALZEME DOZAJI — ✔ KARAR v24 (5 Eyl 2026): TEK KAP TİPİ · 3 KAT</div>')
old_img = '<img src="img/ist3_topping_detay_v8.png" alt="TOPPING istasyonu detay v8" style="width:100%;max-width:1100px;display:block;margin:6px auto 12px;border:1px solid #d7e8dc;border-radius:12px" loading="lazy">'
new_block = (
 '<div style="margin:6px 0 10px;padding:10px 14px;background:#eef7f1;border:1px solid #cfe5d6;border-radius:10px;font-size:13.5px;line-height:1.6;color:#22304a">'
 '<b style="color:#1d7a4f">GÜNCEL KARAR — 5 Eyl 2026 (v24):</b> 4 malzeme <b>kıyma (kavrulmuş) · kaşar (rende) · kuşbaşı (sote) · sucuk (küp)</b> — hepsi parça halinde gelir, çiğ harç makinede yok (su salar). '
 '<b>TEK KAP TİPİ 16×54×24 cm</b>: simetrik kama huni, U-oluk ortada, helezon (kaşar/kıyma milsiz spiral, küpler milli) + köprü kırıcı tarak, UHMW-PE gövde, kapta elektrik yok, sağ-sol ayna yok → 16 kap tek kalıp. '
 '<b>3 kat × 2 kap = 6 pozisyon</b>: kat 1 kaşar A + sucuk (sucuklu-kaşarlı), kat 2 kaşar B + boş (kaşarlı), kat 3 kıyma + kuşbaşı — her tarif tek düzlemde, kat değişimi yok. '
 'Üstte teknik bölme yok: <b>elektrik 10 cm arka duvarın içinde (motorlarla)</b>, <b>soğutma grubu ALT arkasında</b> (hava plint ızgarasından). ALT 74 = 2 sıra × 4 kap şeklinde beşik (kaşar yedeği ×4, çözülme ×2, park ×2); donmuş kıyma/kuşbaşı STORE −18 çekmecesinde 3 kap/modül. '
 'Pide Ø30 → tepsi Ø32 + spiral R 11 → ağızlar kabın ortasında (x 27 / 43), süpürme duvar içinde. Robot haftada 11 kap değişimi (kap ≤ 13 kg → 12 kg kobot yeter), eleman haftada 1 (6 kaşar + 1 sucuk + 2+2 donmuş). Tepsi düzlemleri 158 / 117 / 76 cm. '
 '<span style="color:#9a6b1f">Açık: spiral 11'+chr(39)+'in pide kenarını kapatması ve kaşar akışı (prototip) · 158 cm üst düzlem (kobot erişimi).</span></div>'
 '<img src="img/ist3_topping_detay_v24.png" alt="TOPPING istasyonu v24 — tek kap tipi, 3 kat, üst görünüm" style="width:100%;max-width:1100px;display:block;margin:6px auto 12px;border:1px solid #d7e8dc;border-radius:12px" loading="lazy">'
 '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px;margin:4px auto 14px;max-width:1100px">'
 '<figure style="margin:0"><img src="img/kap_geometri_v1.png" alt="Kap geometrisi v1 — kama huni, U-oluk, milsiz helezon, tarak, hijyen kuralları" style="width:100%;border:1px solid #d7e8dc;border-radius:12px" loading="lazy"><figcaption style="font-size:12px;color:#68758a;margin-top:5px">Kap geometrisi (araştırma, 5 Eyl): 55° kama huni, U-oluk R 38, milsiz spiral, köprü kırıcı tarak, iç köşe R ≥ 6 (EHEDG), UHMW-PE — 4 malzemenin davranış tablosuyla.</figcaption></figure>'
 '<figure style="margin:0"><img src="' + webname + '" alt="Picnic pizza istasyonu — sos ve peynir hazneleri, pepperoni oluğu, altta dönen pide (referans)" style="width:100%;border:1px solid #d7e8dc;border-radius:12px" loading="lazy"><figcaption style="font-size:12px;color:#68758a;margin-top:5px">Referans: Picnic (ABD) — üstten dolan şeffaf hazneler + helezon dozajı, altta pide; sağda pepperoni oluğu ve küp hazneleri. Firma 2026'+chr(39)+'da kapandı; hazne–helezon–tarak mantığı bizim kabın temeli.</figcaption></figure>'
 '</div>'
 '<div style="font-size:12px;color:#9a6b1f;margin:10px 0 4px"><b>Önceki tur (4 Eyl, v8) — arşiv:</b> aşağıdaki metin ve tablo eski kaset kurgusudur; ölçüler ve yerleşim yukarıdaki v24 ile değişti.</div>'
 '<img src="img/ist3_topping_detay_v8.png" alt="TOPPING istasyonu detay v8 (arşiv)" style="width:100%;max-width:700px;display:block;margin:6px auto 12px;border:1px solid #e7dcc3;border-radius:12px;opacity:.85" loading="lazy">'
)
rep(old_img, new_block)
# eski paragraf: arsiv etiketinin ustune tasi (paragraf v8 gorselinden once geliyordu) — sadece rengini soluklastir
rep('<p style="margin:8px 0 12px;font-size:14px;color:#3f4a5c">Görev: basılmış tabana kaşar + küp sucuk + kavurma + kuşbaşı dozajı',
    '<p style="margin:8px 0 12px;font-size:14px;color:#3f4a5c">Görev: basılmış tabana malzeme dozajı — güncel karar aşağıdaki yeşil kutuda (v24). <span style="color:#9a6b1f">Eski konsept (4 Eyl):</span> kaşar + küp sucuk + kavurma + kuşbaşı dozajı')

# ---- HAT genel gorunum v22 → v45 ----
rep('<img src="img/hat_on_gorunus_teknik_v22.png" alt="Soğuk depo teknik çizim v22" style="width:100%;max-width:1100px;display:block;margin:6px auto 12px;border:1px solid #d7e8dc;border-radius:12px" loading="lazy">',
    '<img src="img/hat_on_gorunus_teknik_v45.png" alt="Hat genel görünüm v45 — tüm istasyonlar son versiyon" style="width:100%;max-width:1100px;display:block;margin:6px auto 4px;border:1px solid #d7e8dc;border-radius:12px" loading="lazy">'
    '<div style="font-size:12px;color:#68758a;margin:0 0 12px;text-align:center">HAT v45 (5 Eyl 2026) — STORE v4 (alt buzluk, 19 çekmece) · PRESS v8 · TOPPING v23 (tek kap, 3 kat) · OVEN tank+pompa · PACK 116 kutu · KONTROL kutusu paftada (② fırın kavitesi, ⑩ yağ pompası, ⑫ tepsi Ø32 zinciri açık).</div>')
io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('index.html guncellendi')
