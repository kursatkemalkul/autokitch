# -*- coding: utf-8 -*-
# STORE v5 paftası — CONTALI SÜRÜM (1_STORE_v2 modelinden): ön · yan kesit · conta detayı + ölçü + parça
import io, math, xml.dom.minidom
W, H = 1460, 980
o = []
def esc(s): return str(s).replace('&', '&amp;').replace('<', '&lt;')
def ln(x1, y1, x2, y2, w=1, c='#111', d=None):
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s stroke-linecap="round"/>' % (x1, y1, x2, y2, c, w, (' stroke-dasharray="%s"' % d) if d else ''))
def rc(x, y, w, h, sw=1, r=0, c='#111', d=None, f='none'):
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x, y, w, h, r, f, c, sw, (' stroke-dasharray="%s"' % d) if d else ''))
def ci(x, y, r, sw=1, c='#111', f='none'):
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"/>' % (x, y, r, f, c, sw))
def tx(x, y, s, fs=9, anc='start', fw='', col='#111'):
    o.append('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="%s" font-weight="%s" fill="%s" font-family="Segoe UI, Arial, sans-serif">%s</text>' % (x, y, fs, anc, fw or 'normal', col, esc(s)))
def poly(pts, sw=1, c='#111', f='none'):
    o.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round"/>' % (' '.join('%.1f,%.1f' % p for p in pts), f, c, sw))
def para(x, y, s, maxc, fs=6.0, col='#333', fw=''):
    lh = fs*1.6; cur = ''; lines = []
    for wd in s.split(' '):
        if cur and len(cur)+1+len(wd) > maxc: lines.append(cur); cur = wd
        else: cur = (cur+' '+wd) if cur else wd
    if cur: lines.append(cur)
    for l in lines: tx(x, y, l, fs, 'start', fw, col); y += lh
    return y
GRN, RED, BLU, GRY, AMB = '#1d7a4f', '#c0392b', '#1a49b8', '#666', '#b7791f'
LIGHT, COLD, PCB, GSK = '#f7f6f2', '#eaf2fb', '#dbeeff', '#f6d9d5'

KW, KH = 1400.0, 1970.0
SOVE, WO, BIND, FUGA = 45.0, 620.0, 15.0, 3.0
XL, XR = 63.0, 716.0
TIPH = {"1L": 316.0, "icecek": 133.0, "taze": 108.0, "donmus": 160.0, "klape": 284.0}
ORNEK = ([("1L", XL, 781.0)] + [("icecek", XL, y) for y in (1130.0, 1296.0, 1462.0)] +
         [("taze", XR, y) for y in (781.0, 922.0, 1063.0, 1204.0, 1345.0, 1486.0)] +
         [("donmus", XL, 198.0), ("donmus", XR, 198.0), ("klape", XL, 391.0), ("klape", XR, 391.0)])
S = 0.40                                   # px/mm

tx(30, 36, 'AUTOKITCH — STORE v5 (9 Eyl 2026) — CONTALI SÜRÜM: bindirmeli ön yüz + manyetik conta + ön çerçeve sacı — ölçüler mm', 14, 'start', 'bold')
tx(30, 56, 'Model: arastirma/1_STORE_v2/STORE_v2.SLDASM · 182 bileşen · parça seviyesinde çakışma 0 · 12 çekmece + 2 klape hareketli. v4 (contasız, 19 açıklık) arastirma/1_STORE altında korunuyor.', 8.4, 'start', '', '#444')
ln(30, 68, 1430, 68, .8, '#999')

# ---------------------------------------------------------------- A · ÖN GÖRÜNÜŞ
rc(30, 82, 640, 880, 1, 6, '#bbb'); tx(42, 100, 'A · ÖN GÖRÜNÜŞ — 14 açıklık, fuga 3, kulp yok', 8.4, 'start', 'bold')
AX, AY = 90.0, 930.0
def ax_(x): return AX + x*S
def ay_(y): return AY - y*S
rc(ax_(0), ay_(KH), KW*S, KH*S, 1.1, 0, '#111', None, LIGHT)
rc(ax_(SOVE), ay_(1610), (KW-2*SOVE)*S, (1610-182.5)*S, .7, 0, '#999', None, COLD)
for tip, x0, y0 in ORNEK:
    h = TIPH[tip]
    rc(ax_(x0-BIND), ay_(y0+h+BIND), (WO+2*BIND)*S, (h+2*BIND)*S, .9, 0, '#111', None, PCB)   # bindirmeli ön yüz
    rc(ax_(x0), ay_(y0+h), WO*S, h*S, .4, 0, RED, '3,2')                                       # açıklık (gizli)
tx(ax_(KW/2), ay_(-8), '1400', 7, 'middle', 'bold')
ln(ax_(0), ay_(-16), ax_(KW), ay_(-16), .7)
for a, b, s_ in ((0, SOVE, '45'), (XL-BIND, XL+WO+BIND, '650'), (683, 716, '33'), (XR-BIND, XR+WO+BIND, '650'), (KW-SOVE, KW, '45')):
    ln(ax_(a), ay_(-30), ax_(b), ay_(-30), .6); ln(ax_(a), ay_(-34), ax_(a), ay_(-26), .6); ln(ax_(b), ay_(-34), ax_(b), ay_(-26), .6)
    tx(ax_((a+b)/2), ay_(-30)-3, s_, 5.8, 'middle', 'bold')
XD = ax_(KW)+10
for a, b, s_ in ((120, 182.5, '62'), (198, 358, '160'), (391, 675, '284'), (781, 1097, '316'),
                 (1130, 1263, '133'), (1296, 1429, '133'), (1462, 1595, '133'), (1610, 1670, '60'), (1670, 1970, '300')):
    ln(XD, ay_(a), XD, ay_(b), .7); ln(XD-3, ay_(a), XD+3, ay_(a), .7); ln(XD-3, ay_(b), XD+3, ay_(b), .7)
    tx(XD+4, (ay_(a)+ay_(b))/2+2, s_, 5.8, 'start', 'bold')
tx(XD+34, ay_(1900), 'teknik bölme', 5.8, 'start', 'bold', GRY)
tx(XD+34, ay_(1200), 'açıklıklar arası alın 33', 5.8, 'start', 'bold', RED)
tx(ax_(XL+WO/2), ay_(1900), 'SOL MODÜL', 7, 'middle', 'bold', GRY)
tx(ax_(XR+WO/2), ay_(1900), 'SAĞ MODÜL', 7, 'middle', 'bold', GRY)

# ---------------------------------------------------------------- B · CONTA DETAYI
rc(686, 82, 744, 430, 1, 6, '#bbb'); tx(698, 100, 'B · CONTA ve ÖN ÇERÇEVE DETAYI (yatay kesit) — geçmeli manyetik conta 21 × 18,5', 8.4, 'start', 'bold')
DX, DY, DS = 760.0, 400.0, 2.6
def dx_(z): return DX + (z+40)*DS
def dy_(y): return DY - y*DS
rc(dx_(-40), dy_(70), 24*DS, 70*DS, .8, 0, '#999', None, '#efefef'); tx(dx_(-28), dy_(36), 'PU 60', 6.0, 'middle', '', '#555')
rc(dx_(-16), dy_(70), 1*DS, 70*DS, 1.4, 0, GRN, None, GRN)
tx(dx_(-16)+4, dy_(74), 'ÖN ÇERÇEVE SACI 1,0  (z −16…−15)', 6.4, 'start', 'bold', GRN)
rc(dx_(-15), dy_(15), 15*DS, 15*DS, 1.0, 0, RED, None, GSK)
tx(dx_(42), dy_(9), 'MANYETİK CONTA 21 × 18,5 — sıkışmış 15', 6.2, 'start', 'bold', RED)
ln(dx_(0), dy_(8), dx_(40), dy_(8), .6, RED, '3,2')
rc(dx_(0), dy_(60), 1*DS, 60*DS, .9, 0, '#111', None, '#dfe6ea')
rc(dx_(1), dy_(60), 37.5*DS, 60*DS, .9, 0, '#111', None, '#f2efe4')
rc(dx_(38.5), dy_(60), 1.5*DS, 60*DS, .9, 0, '#111', None, '#dfe6ea')
tx(dx_(20), dy_(64), 'ÖN YÜZ 40 = 1,0 iç sac + 37,5 PU + 1,5 dış sac', 6.4, 'middle', 'bold')
tx(dx_(42), dy_(28), 'bindirme 15 · fuga 3 · alın 33', 6.2, 'start', 'bold', BLU)
for a_, b_, s_, yy in ((-16, -15, '1,0', 44), (-15, 0, '15', 52), (0, 40, '40', 60)):
    ln(dx_(a_), dy_(yy), dx_(b_), dy_(yy), .6, BLU)
    ln(dx_(a_), dy_(yy)-3, dx_(a_), dy_(yy)+3, .6, BLU); ln(dx_(b_), dy_(yy)-3, dx_(b_), dy_(yy)+3, .6, BLU)
    tx(dx_((a_+b_)/2), dy_(yy)-3, s_, 5.8, 'middle', 'bold', BLU)
tx(dx_(-38), dy_(-8), 'iç sacın kenarına conta kanalı 6,3 açılır (geçme dişi 8,3) — tornavidasız takılır', 6.0, 'start', '', '#333')
py = para(1170, 140, 'Standart profil: toplam genişlik 21 · yüzeyden yükseklik 18,5 · saçtaki kanal 6,3 · geçme dişi 8,3. Sıkışmış hâlde 15 mm, kapak kapalıyken ön yüzün arkası çerçeve sacına 15 mm mesafede durur.', 42, 6.0)
py = para(1170, py+4, 'Ön yüz açıklığa her kenardan 15 mm biner. Komşu ön yüzler arası fuga 3 mm. Bu yüzden açıklıklar arası alın 15 + 3 + 15 = 33 mm olmak zorunda.', 42, 6.0)
py = para(1170, py+4, 'Söve ve sabit paneller de 40 mm sandviç; dış kabuğun üst, alt ve yan ön dönüşleri kapalı, arkada boşluk kalmıyor.', 42, 6.0, GRN, 'bold')

# ---------------------------------------------------------------- C · TAHRİK
rc(686, 522, 744, 200, 1, 6, '#bbb'); tx(698, 540, 'C · ÇEKMECE TAHRİKİ (yan kesit şeması)', 8.4, 'start', 'bold')
CX, CY, CS = 720.0, 690.0, 0.62
def cx_(z): return CX + (z+800)*CS
def cy_(y): return CY - y*CS
rc(cx_(-800), cy_(180), 840*CS, 180*CS, .8, 0, '#999', None, LIGHT)
rc(cx_(-700), cy_(150), 700*CS, 140*CS, .9, 0, '#111', None, PCB); tx(cx_(-350), cy_(85), 'çekmece kutusu 700 derin', 6.0, 'middle', '', '#333')
rc(cx_(-757), cy_(120), 20*CS, 120*CS, .8, 0, BLU, None, '#e3ecf7'); tx(cx_(-747)+4, cy_(130), 'evaporatör (arka plenum 57,5)', 5.8, 'start', 'bold', BLU)
rc(cx_(-745), cy_(30), 36*CS, 36*CS, .9, 0, AMB, None, '#fbeecf'); tx(cx_(-727), cy_(-4), '24 V motor + enkoder', 5.8, 'middle', 'bold', AMB)
ln(cx_(-727), cy_(6), cx_(-80), cy_(6), 1.6, GRN); tx(cx_(-420), cy_(12), 'GT3 kayış — kutunun altında', 5.8, 'middle', 'bold', GRN)
rc(cx_(-80), cy_(20), 40*CS, 20*CS, .8, 0, GRN, None, '#e6f2ea'); tx(cx_(-60), cy_(26), 'pabuç', 5.4, 'middle', '', GRN)
rc(cx_(0), cy_(180), 40*CS, 180*CS, .9, 0, '#111', None, '#dfe6ea'); tx(cx_(20), cy_(186), 'ön yüz', 5.6, 'middle', '', '#333')
ci(cx_(-25), cy_(90), 3, 1.2, RED); tx(cx_(-25)+6, cy_(96), 'reed sensör + mıknatıs (kapalı konum)', 5.8, 'start', 'bold', RED)

# ---------------------------------------------------------------- D · KAPASİTE / PARÇA
rc(686, 736, 744, 226, 1, 6, '#bbb'); tx(698, 754, 'D · KAPASİTE (v4 contasız → v5 contalı) ve PARÇA', 8.4, 'start', 'bold')
hd = ['bölme', 'v4', 'v5', 'içerik']
cw = [150, 95, 105, 300]; x_ = 700
for i, h_ in enumerate(hd): tx(x_+sum(cw[:i]), 774, h_, 6.4, 'start', 'bold')
ln(700, 780, 1420, 780, .6, '#bbb')
rows = [('İÇECEK çekmecesi', '4 · 280 kutu', '3 · 210 kutu', 'yuvalı sac + 330 ml kutu (7 × 10)'),
        ('1 LİTRELİK', '1 · 42 şişe', '1 · 42 şişe', 'yuvalı sac + 1 L şişe (6 × 7)'),
        ('HAMUR (taze)', '8 · 160 top', '6 · 120 top', 'GN 2/1 silikon tepsi + 20 × 220 g top'),
        ('DONMUŞ', '4 · h 94', '2 · h 160', 'GN 2/1 tepsi + donmuş hamur'),
        ('KASET KLAPESİ', '1', '2', 'TOPPING yedek kabı: 4 → 8 kap'),
        ('toplam açıklık', '19', '14', 'conta alını 33 mm zorunluluğu')]
yy = 794
for r in rows:
    for i, v in enumerate(r): tx(x_+sum(cw[:i]), yy, v, 6.2, 'start', 'bold' if i == 0 else '', '#111' if i == 0 else '#333')
    yy += 15
ln(700, yy-9, 1420, yy-9, .6, '#bbb')
yy = para(700, yy+6, 'Çekmece başına: 2 dış ray profili + GT3 kayış + 24 V redüktörlü motor (enkoderli) + 24 V kablo + reed sensör. Klape başına: klape motor grubu + sensör. Pano teknik bölmede: Modbus PLC, 24 V 20 A güç kaynağı, 14 sürücü, klemens, kablo kanalı.', 148, 6.0)
yy = para(700, yy+2, 'AÇIK: klape menteşesi telafili (4 kollu) olmalı — kapak açılırken önce öne çıkıp contadan ayrılmalı; katalog parçası seçilecek.', 148, 6.0, AMB)
tx(W-30, H-14, 'AUTOKITCH · arastirma/1_STORE/ist1_store_detay_v5 · 9 Eyl 2026', 7, 'end', '', GRY)

svg = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">\n<rect x="0" y="0" width="%d" height="%d" fill="#fff"/>\n' % (W, H, W, H, W, H) + '\n'.join(o) + '\n</svg>'
xml.dom.minidom.parseString(svg.encode('utf-8'))
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\1_STORE\ist1_store_detay_v5.svg"
io.open(out, 'w', encoding='utf-8').write(svg)
print('yazildi:', out)
