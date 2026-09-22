# -*- coding: utf-8 -*-
# STORE v6 — CONTALI ÖN YÜZ ÜRETİM PAFTASI (v2 modeli): ön görünüş · conta detayı · yan kesit ·
#            sağ alt bölme seçenekleri · kapasite. Ölçüler mm.
import io, math, xml.dom.minidom
W, H = 1460, 950
o = []
def esc(s): return str(s).replace('&', '&amp;').replace('<', '&lt;')
def ln(x1, y1, x2, y2, w=1, c='#111', d=None):
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s stroke-linecap="round"/>' % (x1, y1, x2, y2, c, w, (' stroke-dasharray="%s"' % d) if d else ''))
def rc(x, y, w, h, sw=1, r=0, c='#111', d=None, f='none'):
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x, y, w, h, r, f, c, sw, (' stroke-dasharray="%s"' % d) if d else ''))
def ci(x, y, r, sw=1, c='#111', d=None, f='none'):
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x, y, r, f, c, sw, (' stroke-dasharray="%s"' % d) if d else ''))
def tx(x, y, s, fs=9, anc='start', fw='', col='#111'):
    o.append('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="%s" font-weight="%s" fill="%s" font-family="Segoe UI, Arial, sans-serif">%s</text>' % (x, y, fs, anc, fw or 'normal', col, esc(s)))
def poly(pts, sw=1, c='#111', f='none', d=None):
    o.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s"%s stroke-linejoin="round"/>' % (' '.join('%.1f,%.1f' % p for p in pts), f, c, sw, (' stroke-dasharray="%s"' % d) if d else ''))
def para(x, y, s, maxc, fs=6.0, col='#333', fw='', lh=None):
    lh = lh or fs*1.6; cur = ''; lines = []
    for wd in s.split(' '):
        if cur and len(cur)+1+len(wd) > maxc: lines.append(cur); cur = wd
        else: cur = (cur+' '+wd) if cur else wd
    if cur: lines.append(cur)
    for l in lines: tx(x, y, l, fs, 'start', fw, col); y += lh
    return y
GRN, RED, BLU, GRY, AMB = '#1d7a4f', '#c0392b', '#1a49b8', '#666', '#b7791f'
LIGHT, COLD, PANEL, SEAL = '#f7f6f2', '#eaf2fb', '#dfe6ee', '#f6d5cf'

# ---------------- GEOMETRİ (mm, SolidWorks modelinden) ----------------
KW, KH, KD = 1400.0, 1970.0, 860.0
SOVE, BIND, FUGA, ALIN = 45.0, 15.0, 3.0, 33.0
WO = 620.0; XL, XR = 63.0, 716.0
CELL0, CELL1 = 182.5, 1610.0
BOL0, BOL1 = 683.0, 716.0
ACIK = [("1L", XL, 781.0, 316.0), ("içecek", XL, 1130.0, 133.0), ("içecek", XL, 1296.0, 133.0), ("içecek", XL, 1462.0, 133.0),
        ("hamur", XR, 781.0, 108.0), ("hamur", XR, 922.0, 108.0), ("hamur", XR, 1063.0, 108.0),
        ("hamur", XR, 1204.0, 108.0), ("hamur", XR, 1345.0, 108.0), ("hamur", XR, 1486.0, 108.0),
        ("donmuş", XL, 198.0, 160.0), ("donmuş", XR, 198.0, 160.0),
        ("klape", XL, 391.0, 284.0), ("klape", XR, 391.0, 284.0)]

tx(30, 38, 'AUTOKITCH — 1 · STORE v6 (9 Eyl 2026) — CONTALI ÖN YÜZ: ön görünüş · conta kesiti · yan kesit · sağ alt bölme seçenekleri — ölçüler mm', 14, 'start', 'bold', '#111')
tx(30, 58, 'Manyetik conta ön yüzün arkasında, kasadaki çerçeve sacına basar. Bindirme 15 · fuga 3 → açıklıklar arası alın 33. Kulp ve girinti yok.', 8.4, 'start', '', '#444')
ln(30, 70, 1430, 70, .8, '#999')

# =============================================== A · ÖN GÖRÜNÜŞ
rc(30, 84, 420, 590, 1, 6, '#bbb'); tx(42, 102, 'A · ÖN GÖRÜNÜŞ — 14 açıklık (12 çekmece + 2 klape)', 8.6, 'start', 'bold')
S = 0.255; AX, AY = 92.0, 645.0
def ax(x): return AX + x*S
def ay(y): return AY - y*S
rc(ax(0), ay(KH), KW*S, KH*S, 1.1, 0, '#111', None, LIGHT)
rc(ax(SOVE), ay(CELL1), (KW-2*SOVE)*S, (CELL1-CELL0)*S, .6, 0, '#aaa', None, COLD)
rc(ax(0), ay(KH), SOVE*S, (KH-120)*S, .6, 0, '#999', None, PANEL)             # söve sol
rc(ax(KW-SOVE), ay(KH), SOVE*S, (KH-120)*S, .6, 0, '#999', None, PANEL)       # söve sağ
rc(ax(BOL0), ay(CELL1), (BOL1-BOL0)*S, (CELL1-CELL0)*S, .6, 0, '#999', None, PANEL)
for nm, x0, y0, h in ACIK:
    rc(ax(x0-BIND), ay(y0+h+BIND), (WO+2*BIND)*S, (h+2*BIND)*S, .9, 0, '#111', None, PANEL)   # bindirmeli ön yüz
    rc(ax(x0), ay(y0+h), WO*S, h*S, .4, 0, '#bbb', '2,2')                                     # açıklık (gizli)
    if nm == "klape": tx(ax(x0+WO/2), ay(y0+h/2), 'KLAPE', 6.2, 'middle', 'bold', GRN)
    else: tx(ax(x0+WO/2), ay(y0+h/2)+2, nm, 6.0, 'middle', '', '#444')
for y0, y1, s_ in ((CELL1, 1670, 'bant'), (690, 766, 'ayırıcı'), (1670, KH, 'soğutma + pano'), (120, CELL0, 'bant')):
    rc(ax(SOVE), ay(y1), (KW-2*SOVE)*S, (y1-y0)*S, .6, 0, '#999', None, PANEL)
    tx(ax(KW/2), ay((y0+y1)/2)+2, s_, 5.8, 'middle', '', '#555')
# dikey ölçü zinciri — sol modül
def vdim(x, a, b, s_, col='#111', fs=5.6):
    ln(x, ay(a), x, ay(b), .7, col); ln(x-3, ay(a), x+3, ay(a), .7, col); ln(x-3, ay(b), x+3, ay(b), .7, col)
    tx(x+4, (ay(a)+ay(b))/2+2, s_, fs, 'start', 'bold', col)
XD = ax(KW)+10
for a, b, s_ in ((198, 358, '160'), (358, 391, '33'), (391, 675, '284'), (781, 1097, '316'),
                 (1097, 1130, '33'), (1130, 1263, '133'), (1296, 1429, '133'), (1462, 1595, '133')): vdim(XD, a, b, s_)
XD2 = XD + 40
for a, b, s_ in ((0, KH, '1970'), (CELL0, CELL1, '1427,5 hücre')): vdim(XD2, a, b, s_, GRY)
YB = ay(0) + 16
ln(ax(0), YB, ax(KW), YB, .7); tx(ax(KW/2), YB-3, '1400', 6.4, 'middle', 'bold')
YB2 = YB + 13
for a, b, s_ in ((0, SOVE, '45'), (XL, XL+WO, '620'), (BOL0, BOL1, '33'), (XR, XR+WO, '620'), (KW-SOVE, KW, '45')):
    ln(ax(a), YB2, ax(b), YB2, .6); ln(ax(a), YB2-3, ax(a), YB2+3, .6); ln(ax(b), YB2-3, ax(b), YB2+3, .6)
    tx(ax((a+b)/2), YB2-3, s_, 5.6, 'middle', 'bold')

# =============================================== C · YAN KESİT
rc(466, 84, 258, 590, 1, 6, '#bbb'); tx(478, 102, 'C · YAN KESİT — çekmece', 8.6, 'start', 'bold')
CS = 0.255; CX, CY = 492.0, 645.0
def cx(z): return CX + (z+860)*CS      # z −860…0
def cy(y): return CY - y*CS
rc(cx(-860), cy(KH), KD*CS, KH*CS, 1.1, 0, '#111', None, LIGHT)
rc(cx(-820), cy(CELL1), 780*CS, (CELL1-CELL0)*CS, .6, 0, '#aaa', None, COLD)
for nm, x0, y0, h in ACIK:
    if x0 != XL: continue
    if nm == "klape":
        rc(cx(-16), cy(y0+h+BIND), 56*CS, (h+2*BIND)*CS, .9, 0, '#111', None, PANEL); continue
    rc(cx(-700), cy(y0+h-10), 700*CS, (h-18)*CS, .7, 0, '#111', None, '#fff')          # kutu
    rc(cx(-16), cy(y0+h+BIND), 56*CS, (h+2*BIND)*CS, .9, 0, '#111', None, PANEL)       # bindirmeli ön yüz + conta
    ln(cx(-660), cy(y0+40), cx(0), cy(y0+40), 1.0, GRY)                                 # ray 660
    rc(cx(-698), cy(y0-3), 36*CS, 43*CS, .7, 0, AMB, None, '#fdf3e0')                   # motor (alın boşluğunda)
    ln(cx(-730), cy(y0-16), cx(-80), cy(y0-16), 1.2, GRN)                               # kayış
rc(cx(-755), cy(1500), 45*CS, 100*CS, .7, 0, BLU, None, '#e8f0fb')
rc(cx(-755), cy(600), 45*CS, 100*CS, .7, 0, BLU, None, '#e8f0fb')
tx(cx(-733), cy(1560), 'evaporatör', 5.4, 'middle', '', BLU)
tx(cx(-400), cy(120), 'motor + kayış alın boşluğunda', 5.8, 'middle', 'bold', AMB)
tx(cx(-350), cy(1700), 'çekmece kutusu 700 · ray 660', 5.8, 'middle', 'bold', GRY)
YC = cy(0) + 16
for a, b, s_ in ((-860, 0, '860'), (-700, 0, '700 çekmece'), (-40, 0, '40 ön yüz')):
    ln(cx(a), YC, cx(b), YC, .6); ln(cx(a), YC-3, cx(a), YC+3, .6); ln(cx(b), YC-3, cx(b), YC+3, .6)
    tx(cx((a+b)/2), YC-3, s_, 5.6, 'middle', 'bold'); YC += 12

# =============================================== B · CONTA DETAYI
rc(740, 84, 690, 350, 1, 6, '#bbb'); tx(752, 102, 'B · CONTA DETAYI — iki komşu ön yüz arası (yatay kesit, büyütülmüş)', 8.6, 'start', 'bold')
D = 3.4; DX, DY = 790.0, 300.0
def dx(z): return DX + (z+30)*D          # z −30…+45
def dy(u): return DY - u*D               # u = alın ekseni boyunca (mm)
# kasa: çerçeve sacı + yalıtım
rc(dx(-30), dy(20), 14*D, 40*D, .8, 0, '#111', None, '#e9e9e9'); tx(dx(-23), dy(-24), 'PU 37,5 / iç sac', 5.4, 'middle', '', '#555')
rc(dx(-16), dy(20), 1*D, 40*D, 1.0, 0, '#111', None, '#bfc7cf')
tx(dx(-16)-6, dy(22), 'ÇERÇEVE SACI 1,0', 6.0, 'end', 'bold', '#111')
# conta halkaları (iki komşu ön yüz)
rc(dx(-15), dy(20), 15*D, 15*D, .9, 0, RED, None, SEAL); tx(dx(-7.5), dy(12)+3, 'conta', 5.6, 'middle', 'bold', RED)
rc(dx(-15), dy(-2), 15*D, 15*D, .9, 0, RED, None, SEAL); tx(dx(-7.5), dy(-10)+3, 'conta', 5.6, 'middle', 'bold', RED)
# ön yüzler (40 sandviç)
for u0, u1 in ((1.5, 21.5), (-18.5, -1.5)):
    rc(dx(0), dy(u1), 1*D, (u1-u0)*D, .8, 0, '#111', None, '#f2f2f2')
    rc(dx(1), dy(u1), 37.5*D, (u1-u0)*D, .8, 0, '#111', None, PANEL)
    rc(dx(38.5), dy(u1), 1.5*D, (u1-u0)*D, .9, 0, '#111', None, '#cfd8dc')
tx(dx(20), dy(21.5)-6, 'ÖN YÜZ 40 = iç sac 1,0 + PU 37,5 + dış sac 1,5', 6.2, 'middle', 'bold')
# fuga
ln(dx(0), dy(1.5), dx(40), dy(1.5), .5, RED, '3,2'); ln(dx(0), dy(-1.5), dx(40), dy(-1.5), .5, RED, '3,2')
tx(dx(44), dy(0)+3, 'fuga 3', 6.0, 'start', 'bold', RED)
# ölçüler
def hdim(u0, u1, s_, xx, col='#111'):
    ln(xx, dy(u0), xx, dy(u1), .7, col); ln(xx-3, dy(u0), xx+3, dy(u0), .7, col); ln(xx-3, dy(u1), xx+3, dy(u1), .7, col)
    tx(xx+4, (dy(u0)+dy(u1))/2+2, s_, 5.8, 'start', 'bold', col)
hdim(1.5, 16.5, '15 conta', dx(-18)-34)
hdim(-16.5, 16.5, '33 ALIN', dx(-18)-70, GRN)
hdim(16.5, 21.5, '5 pay', dx(-18)-34)
ln(dx(-16), dy(30), dx(0), dy(30), .7); ln(dx(-16), dy(30)-3, dx(-16), dy(30)+3, .7); ln(dx(0), dy(30)-3, dx(0), dy(30)+3, .7)
tx(dx(-8), dy(30)-3, '15 conta yüksekliği (profil 18,5 · sıkışmış 15)', 5.8, 'middle', 'bold')
py = para(1160, 130, 'CONTA: endüstriyel geçmeli manyetik profil. Toplam genişlik 21 · yüzeyden yükseklik 18,5 · saçtaki kanal 6,3 · geçme dişi 8,3. Şerit mıknatıs içinde; iç saca açılan kanala tornavidasız geçer, sökülüp yıkanır.', 40, 6.2, '#333')
py = para(1160, py+6, 'ÇERÇEVE SACI: 1,0 paslanmaz, tek parça, 14 açıklık lazer kesim. Ön yüzden 15 mm geride; conta bu alına basar.', 40, 6.2, '#333')
py = para(1160, py+6, 'BİNDİRME 15 + FUGA 3 + BİNDİRME 15 = 33 mm alın. Yalıtım ve iç kabuk çerçeve sacının arkasında biter.', 40, 6.2, GRN, 'bold')

# =============================================== D · SAĞ ALT BÖLME SEÇENEKLERİ
rc(740, 448, 690, 226, 1, 6, '#bbb'); tx(752, 466, 'D · SAĞ ALT BÖLME (182,5–690) — klape yerine çekmece seçenekleri', 8.6, 'start', 'bold')
DS = 0.30; bx = 770.0
def kutu(x0, baslik, dizi, renk):
    by = 632.0
    rc(x0, by-507.5*DS, 130, 507.5*DS, .9, 0, '#111', None, COLD)
    tx(x0+65, by-507.5*DS-6, baslik, 6.6, 'middle', 'bold', renk)
    yy = 182.5 + 15
    for h, et in dizi:
        rc(x0+6, by-(yy+h-182.5)*DS, 118, h*DS, .8, 0, '#111', None, PANEL)
        tx(x0+65, by-(yy+h/2-182.5)*DS+2, et, 5.6, 'middle', 'bold' if et.startswith('KLAPE') else '', '#222')
        yy += h + ALIN
    ln(x0+134, by, x0+134, by-507.5*DS, .7); tx(x0+137, by-507.5*DS/2, '507,5', 5.6, 'start', 'bold')
kutu(bx, 'MEVCUT', [(160.0, 'donmuş 160'), (284.0, 'KLAPE 284')], GRN)
kutu(bx+175, 'SEÇENEK 1', [(94.0, 'donmuş 94'), (94.0, 'donmuş 94'), (94.0, 'donmuş 94'), (94.0, 'donmuş 94')], BLU)
kutu(bx+350, 'SEÇENEK 2', [(137.0, 'donmuş 137'), (137.0, 'donmuş 137'), (137.0, 'donmuş 137')], BLU)
kutu(bx+525, 'SEÇENEK 3', [(222.0, 'donmuş 222'), (222.0, 'donmuş 222')], BLU)
para(752, 648, 'Hesap: 507,5 − 2 × 15 uç payı = 477,5 · n çekmece için n × H + (n−1) × 33 ≤ 477,5. Klape kalkarsa 4, 3 veya 2 çekmece sığar.', 150, 6.2, '#333')
para(752, 660, 'Klapeyi kaldırırsan TOPPING yedek kabı 8 → 4 düşer; sol moduldeki klape kalır.', 150, 6.2, AMB)

# =============================================== E · KAPASİTE + MOTOR
rc(30, 690, 1400, 232, 1, 6, '#bbb'); tx(42, 710, 'E · KAPASİTE ve ALIN BOŞLUĞUNA MOTOR YERLEŞİMİ', 8.6, 'start', 'bold')
hd = ['bölme', 'v1 (contasız)', 'v2 (contalı)', 'SEÇENEK 1 ile']
cw = [150, 190, 190, 200]; x_ = 46
for i, hh in enumerate(hd): tx(x_+sum(cw[:i]), 732, hh, 6.6, 'start', 'bold')
ln(46, 738, 780, 738, .6, '#bbb')
rows = [('içecek', '4 çekmece · 280 kutu', '3 · 210 kutu', '3 · 210 kutu'),
        ('1 litrelik', '1 · 42 şişe', '1 · 42 şişe', '1 · 42 şişe'),
        ('hamur', '8 · 160 top', '6 · 120 top', '6 · 120 top'),
        ('donmuş', '4 · 80 top', '2 · 40 top', '5 · 100 top'),
        ('kaset klapesi', '1 · 4 kap', '2 · 8 kap', '1 · 4 kap'),
        ('TOPLAM açıklık', '19', '14', '17')]
yy = 752
for r in rows:
    for i, v in enumerate(r): tx(x_+sum(cw[:i]), yy, v, 6.2, 'start', 'bold' if i == 0 or r[0].startswith('TOPLAM') else '', '#111' if i == 0 else '#333')
    yy += 15
ln(46, yy-9, 780, yy-9, .6, '#bbb')
# motor yerleşim krokisi
mx, my = 820.0, 760.0; MS = 0.42
rc(mx, my, WO*MS, 51*MS, .9, 0, '#111', None, '#fff')
tx(mx+WO*MS/2, my-6, 'ALIN BOŞLUĞU — çekmece kutusu üstü ile üstteki kutu altı arası: 620 × 51', 6.4, 'middle', 'bold')
for i in range(2):
    rc(mx+10+i*185*MS*2.05, my+4, 173*MS, 43.5*MS, .9, 0, AMB, None, '#fdf3e0')
    tx(mx+10+i*185*MS*2.05+173*MS/2, my+4+43.5*MS/2+2, 'motor 173 × 43,5', 5.6, 'middle', 'bold', AMB)
ln(mx, my+51*MS+10, mx+WO*MS, my+51*MS+10, .7); tx(mx+WO*MS/2, my+51*MS+7, '620', 6.0, 'middle', 'bold')
ln(mx+10, my+51*MS+22, mx+10+173*MS, my+51*MS+22, .6, AMB); tx(mx+10+173*MS/2, my+51*MS+19, '173', 5.6, 'middle', 'bold', AMB)
py = para(820, 830, 'YAN YANA İKİ ÇEKMECE: alın boşluğu 620 mm geniş, motor 173 mm. İki motor yan yana 346 mm tutar, 274 mm boş kalır — SIĞAR. Çekmece açıklığı ikiye bölünürse her biri (620 − 33) / 2 = 293,5 mm olur.', 100, 6.2, GRN, 'bold')
py = para(820, py+6, 'AMA KAPASİTE ARTMAZ: ortaya bir alın daha girdiği için kullanılabilir genişlik 620 → 587 düşer. İçecek 70 → 60 kutu; hamur GN 2/1 tepsi (530 geniş) 293,5 açıklığa girmez, GN 1/2\'ye inmek gerekir (tepsi başına 20 → 8 top). Bölmek yalnız robotun daha küçük hacim açması gerekiyorsa mantıklı.', 100, 6.2, RED)
tx(W-30, H-14, 'AUTOKITCH · arastirma/1_STORE/ist1_store_detay_v6 · 9 Eyl 2026', 7, 'end', '', GRY)

svg = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">\n<rect x="0" y="0" width="%d" height="%d" fill="#fff"/>\n' % (W, H, W, H, W, H) + '\n'.join(o) + '\n</svg>'
xml.dom.minidom.parseString(svg.encode('utf-8'))
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\1_STORE\ist1_store_detay_v6.svg"
io.open(out, 'w', encoding='utf-8').write(svg)
print('yazildi + XML gecerli:', out)
