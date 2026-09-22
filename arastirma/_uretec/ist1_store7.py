# -*- coding: utf-8 -*-
# STORE v7 — MİNİMUM AÇIKLIK HESABI + İKİ YERLEŞİM ALTERNATİFİ (karar paftası)
#   alt buzluk (−18) · üst dolap (+3) · teknik bölme (soğutma + pano) ÜSTTE · ayaklar duruyor
#   A: kabuk aynı (teknik bölme 300)      → 16 çekmece
#   B: teknik bölme 225 + ayırıcı 62      → 17 çekmece, v1 kapasitesi tam
import io, xml.dom.minidom
W, H = 1460, 1010
o = []
def esc(s): return str(s).replace('&', '&amp;').replace('<', '&lt;')
def ln(x1, y1, x2, y2, w=1, c='#111', d=None):
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s stroke-linecap="round"/>' % (x1, y1, x2, y2, c, w, (' stroke-dasharray="%s"' % d) if d else ''))
def rc(x, y, w, h, sw=1, r=0, c='#111', d=None, f='none'):
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x, y, w, h, r, f, c, sw, (' stroke-dasharray="%s"' % d) if d else ''))
def tx(x, y, s, fs=9, anc='start', fw='', col='#111'):
    o.append('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="%s" font-weight="%s" fill="%s" font-family="Segoe UI, Arial, sans-serif">%s</text>' % (x, y, fs, anc, fw or 'normal', col, esc(s)))
def para(x, y, s, maxc, fs=6.0, col='#333', fw='', lh=None):
    lh = lh or fs*1.6; cur = ''; lines = []
    for wd in s.split(' '):
        if cur and len(cur)+1+len(wd) > maxc: lines.append(cur); cur = wd
        else: cur = (cur+' '+wd) if cur else wd
    if cur: lines.append(cur)
    for l in lines: tx(x, y, l, fs, 'start', fw, col); y += lh
    return y
GRN, RED, BLU, GRY, AMB = '#1d7a4f', '#c0392b', '#1a49b8', '#666', '#b7791f'
LIGHT, COLD, FRZ, PANEL, TECH = '#f7f6f2', '#eaf2fb', '#dde9f7', '#dfe6ee', '#f0ece3'

KW, KH = 1400.0, 1970.0
SOVE, BIND, FUGA, ALIN = 45.0, 15.0, 3.0, 33.0
WO = 620.0; XL, XR = 63.0, 716.0

tx(30, 38, 'AUTOKITCH — 1 · STORE v7 (9 Eyl 2026) — MİNİMUM AÇIKLIK ve İKİ YERLEŞİM ALTERNATİFİ — ölçüler mm', 14, 'start', 'bold', '#111')
tx(30, 58, 'Alt bölme buzluk (−18) · üst bölme dolap (+3) · soğutma ve pano ÜSTTEKİ teknik bölmede · ayaklar duruyor · her açıklık contalı (alın 33) · AYIRICI BANT İKİ MODÜLDE AYNI HİZADA', 8.4, 'start', '', '#444')
ln(30, 70, 1430, 70, .8, '#999')

# ============================== A · MİNİMUM AÇIKLIK HESABI
rc(30, 84, 560, 300, 1, 6, '#bbb'); tx(42, 102, 'A · MİNİMUM AÇIKLIK — içerik yüksekliğinden', 8.6, 'start', 'bold')
hd = ['içerik', 'içerik üstü', 'emniyet payı', 'MİNİMUM', 'v2\'deki', 'kazanç']
cw = [150, 82, 82, 72, 68, 62]; x_ = 46
for i, hh in enumerate(hd): tx(x_+sum(cw[:i]), 124, hh, 6.4, 'start', 'bold')
ln(46, 130, 578, 130, .6, '#bbb')
rows = [('hamur topu + GN 2/1 tepsi', '78,5', '9,5', '88', '108', '−20'),
        ('donmuş hamur (aynı içerik)', '78,5', '9,5', '88', '160', '−72'),
        ('kutu kola 330 + yuva', '121', '11', '132', '133', '−1'),
        ('1 L şişe + yuva', '290', '10', '300', '316', '−16'),
        ('TOPPING kabı + L raf + kaldırma 5', '271', '13', '284', '284', '0')]
yy = 146
for r in rows:
    for i, v in enumerate(r):
        col = GRN if (i == 5 and v != '0') else ('#111' if i == 0 else '#333')
        tx(x_+sum(cw[:i]), yy, v, 6.2, 'start', 'bold' if i in (0, 3) else '', col)
    yy += 16
ln(46, yy-10, 578, yy-10, .6, '#bbb')
yy = para(46, yy+8, 'EMNİYET PAYI: tam açıkta ray sarkması ≈ 3 + imalat toleransı ≈ 3 + kapanma payı ≈ 3. Sekiz-on bir mm yeterli; altına inilmez.', 118, 6.2, '#333')
yy = para(46, yy+4, 'TOPPING KABI: contası yok, robot çatalla girip 5 mm kaldırıp çekiyor. Kap 264 + L raf 2 + kaldırma 5 = 271, üstüne 13 pay → 284. Mevcut ölçü zaten bu, değişmiyor.', 118, 6.2, AMB)
yy = para(46, yy+4, 'SONUÇ: gereksiz alan hamur ve özellikle DONMUŞ çekmecelerinde. Donmuşta 72 mm boşa gidiyor — içeriği hamurla birebir aynı.', 118, 6.2, GRN, 'bold')

# ============================== ön görünüş çizici
S = 0.238
def cephe(bx, by, baslik, alt, tek_h, bant_ust, ayr_sol, ayr_sag, sol_ust, sol_alt, sag_ust, sag_alt, renk):
    """alt: (etiket, y0, h) listeleri; ayr_* = (y0,y1) ayırıcı bandı"""
    def ax(x): return bx + x*S
    def ay(y): return by - y*S
    rc(ax(0), ay(KH), KW*S, KH*S, 1.1, 0, '#111', None, LIGHT)
    tx(ax(KW/2), ay(KH)-8, baslik, 9.0, 'middle', 'bold', renk)
    # bantlar
    rc(ax(0), ay(KH), KW*S, (KH-tek_h)*S, .7, 0, '#999', None, TECH)
    tx(ax(KW/2), ay(KH-tek_h/2)+2, 'TEKNİK BÖLME (soğutma + pano) %d' % tek_h, 6.0, 'middle', 'bold', AMB)
    rc(ax(0), ay(KH-tek_h), KW*S, 60*S, .6, 0, '#999', None, PANEL)
    for (a, b) in (ayr_sol, ayr_sag):
        pass
    rc(ax(SOVE), ay(ayr_sol[1]), (683-SOVE)*S, (ayr_sol[1]-ayr_sol[0])*S, .6, 0, '#999', None, PANEL)
    rc(ax(716), ay(ayr_sag[1]), (KW-SOVE-716)*S, (ayr_sag[1]-ayr_sag[0])*S, .6, 0, '#999', None, PANEL)
    rc(ax(0), ay(182.5), KW*S, 62.5*S, .6, 0, '#999', None, PANEL)
    rc(ax(0), ay(120), KW*S, 120*S, .6, 0, '#999', None, '#fff'); tx(ax(KW/2), ay(60)+2, 'ayak 120', 5.6, 'middle', '', '#666')
    # hücre gölgeleri
    rc(ax(SOVE), ay(ayr_sol[0]), (683-SOVE)*S, (ayr_sol[0]-182.5)*S, .5, 0, '#aaa', None, FRZ)
    rc(ax(716), ay(ayr_sag[0]), (KW-SOVE-716)*S, (ayr_sag[0]-182.5)*S, .5, 0, '#aaa', None, FRZ)
    rc(ax(SOVE), ay(KH-tek_h-60), (683-SOVE)*S, (KH-tek_h-60-ayr_sol[1])*S, .5, 0, '#aaa', None, COLD)
    rc(ax(716), ay(KH-tek_h-60), (KW-SOVE-716)*S, (KH-tek_h-60-ayr_sag[1])*S, .5, 0, '#aaa', None, COLD)
    # açıklıklar
    for x0, dizi in ((XL, sol_alt + sol_ust), (XR, sag_alt + sag_ust)):
        for et, y0, h in dizi:
            rc(ax(x0-BIND), ay(y0+h+BIND), (WO+2*BIND)*S, (h+2*BIND)*S, .9, 0, '#111', None, PANEL)
            tx(ax(x0+WO/2), ay(y0+h/2)+2, '%s %d' % (et, h), 5.8, 'middle', 'bold' if et == 'KLAPE' else '', GRN if et == 'KLAPE' else '#333')
    tx(ax((SOVE+683)/2), ay(200), 'BUZLUK −18', 6.0, 'middle', 'bold', BLU)
    tx(ax((716+KW-SOVE)/2), ay(200), 'BUZLUK −18', 6.0, 'middle', 'bold', BLU)
    ln(ax(0), ay(0)+12, ax(KW), ay(0)+12, .7); tx(ax(KW/2), ay(0)+9, '1400', 6.2, 'middle', 'bold')
    # dikey ölçü: teknik + hücreler
    xd = ax(KW)+8
    for a, b, s_ in ((KH-tek_h, KH, str(int(tek_h))), (ayr_sol[0], ayr_sol[1], str(int(ayr_sol[1]-ayr_sol[0]))),
                     (182.5, ayr_sol[0], '%.0f' % (ayr_sol[0]-182.5)), (ayr_sol[1], KH-tek_h-60, '%.0f' % (KH-tek_h-60-ayr_sol[1]))):
        ln(xd, ay(a), xd, ay(b), .7); ln(xd-3, ay(a), xd+3, ay(a), .7); ln(xd-3, ay(b), xd+3, ay(b), .7)
        tx(xd+3, (ay(a)+ay(b))/2+2, s_, 5.6, 'start', 'bold')

def dizi(x_et, y0, adet, h, gap=ALIN):
    out = []; y = y0
    for i in range(adet): out.append((x_et, y, h)); y += h + gap
    return out

# ---- ALTERNATİF A
rc(30, 400, 690, 600, 1, 6, '#bbb'); tx(42, 420, 'B · ALTERNATİF A — kabuk aynı (teknik bölme 300)', 8.6, 'start', 'bold')
A_sol_alt = [('KLAPE', 197.5, 284.0), ('donmuş', 514.5, 88.0)]
A_sol_ust = [('1L', 781.0, 300.0)] + dizi('içecek', 1114.0, 3, 132.0)
A_sag_alt = dizi('donmuş', 197.5, 4, 88.0)
A_sag_ust = dizi('hamur', 781.0, 7, 88.0)
cephe(120, 975, 'A · 16 çekmece + 1 klape · ayırıcı 690', None, 300.0, 60.0, (690.0, 766.0), (690.0, 766.0),
      A_sol_ust, A_sol_alt, A_sag_ust, A_sag_alt, BLU)

# ---- ALTERNATİF B
rc(740, 400, 690, 600, 1, 6, '#bbb'); tx(752, 420, 'C · ALTERNATİF B — teknik bölme 225, ayırıcı 62', 8.6, 'start', 'bold')
B_sol_alt = [('KLAPE', 197.5, 284.0), ('donmuş', 514.5, 88.0)]
B_sol_ust = [('1L', 710.0, 300.0)] + dizi('içecek', 1043.0, 4, 132.0)
B_sag_alt = dizi('donmuş', 197.5, 3, 88.0)
B_sag_ust = dizi('hamur', 710.0, 8, 88.0)
cephe(830, 975, 'B · 17 çekmece + 1 klape · ayırıcı 633 (düz hat)', None, 225.0, 60.0, (633.0, 695.0), (633.0, 695.0),
      B_sol_ust, B_sol_alt, B_sag_ust, B_sag_alt, GRN)

# ============================== D · KARŞILAŞTIRMA
rc(600, 84, 830, 300, 1, 6, '#bbb'); tx(612, 102, 'D · KARŞILAŞTIRMA', 8.6, 'start', 'bold')
hd2 = ['', 'v1 (contasız)', 'v2 (bugün)', 'ALTERNATİF A', 'ALTERNATİF B']
cw2 = [170, 150, 140, 150, 150]; x2 = 616
for i, hh in enumerate(hd2): tx(x2+sum(cw2[:i]), 124, hh, 6.4, 'start', 'bold', GRN if i == 4 else '#111')
ln(616, 130, 1418, 130, .6, '#bbb')
rows2 = [('içecek', '4 · 280 kutu', '3 · 210', '3 · 210', '4 · 280'),
         ('1 litrelik', '1 · 42 şişe', '1 · 42', '1 · 42', '1 · 42'),
         ('hamur', '8 · 160 top', '6 · 120', '7 · 140', '8 · 160'),
         ('donmuş', '4 · 80 top', '2 · 40', '5 · 100', '4 · 80'),
         ('kaset klapesi', '1 · 4 kap', '2 · 8 kap', '1 · 4 kap', '1 · 4 kap'),
         ('TOPLAM çekmece', '17', '12', '16', '17'),
         ('TOPLAM hamur topu', '240', '160', '240', '240'),
         ('ayırıcı bant', 'düz 690', 'düz 690', 'düz 690', 'düz 633'),
         ('ön yüz tipi sayısı', '4', '5', '4', '4'),
         ('her çekmece contalı', 'HAYIR', 'evet', 'evet', 'evet')]
yy = 146
for r in rows2:
    for i, v in enumerate(r):
        b = 'bold' if (i == 0 or r[0].startswith('TOPLAM') or i == 4) else ''
        tx(x2+sum(cw2[:i]), yy, v, 6.2, 'start', b, GRN if i == 4 else ('#111' if i == 0 else '#333'))
    yy += 16
ln(616, yy-10, 1418, yy-10, .6, '#bbb')
yy = para(616, yy+8, 'ALTERNATİF B kabuğu değiştirmiyor: dış ölçü 1400 × 1970 × 860 aynı, ayaklar aynı, soğutma ve pano yine üstte. Tek değişen teknik bölme 300 → 225 ve ayırıcı 76 → 62.', 176, 6.2, '#333')
yy = para(616, yy+4, 'B ile v1 kapasitesine BİREBİR dönülüyor: 17 çekmece · 280 kutu · 42 şişe · 8 hamur + 4 donmuş = 240 top · 4 kaset kabı. Ayırıcı bant iki modülde de 633 hizasında, tek düz panel.', 176, 6.2, GRN, 'bold')
yy = para(616, yy+4, 'ÖN YÜZ TİPİ 4 ADET: 88 (hamur ve donmuş aynı) · 132 (içecek) · 300 (1 litrelik) · 284 (klape). Tek kalıp, tek conta boyu, az stok.', 176, 6.2, '#333')
yy = para(616, yy+4, 'RİSK: teknik bölme 225 mm\'ye inince iki kondenser yassı tip olmalı ve pano arka plenuma taşınmalı. Tedarikçiden 225 mm\'lik grup teyidi gerekir. Alternatif A bu riski taşımaz ama bir içecek çekmecesi (70 kutu) eksik kalır.', 176, 6.2, AMB)
tx(W-30, H-14, 'AUTOKITCH · arastirma/1_STORE/ist1_store_detay_v7 · 9 Eyl 2026', 7, 'end', '', GRY)

svg = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">\n<rect x="0" y="0" width="%d" height="%d" fill="#fff"/>\n' % (W, H, W, H, W, H) + '\n'.join(o) + '\n</svg>'
xml.dom.minidom.parseString(svg.encode('utf-8'))
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\1_STORE\ist1_store_detay_v7.svg"
io.open(out, 'w', encoding='utf-8').write(svg)
print('yazildi:', out)
