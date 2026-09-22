# -*- coding: utf-8 -*-
# AUTOKITCH — 2 · PRESS v5 üretim paftası (9 Eyl 2026)
# SADE: ön + üst + yan görünüş + ölçüler + parça listesi. Açıklama mesajda.
import io, xml.dom.minidom
W, H = 1460, 1030
o = []
def esc(s): return str(s).replace('&', '&amp;').replace('<', '&lt;')
def ln(x1, y1, x2, y2, w=1, c='#111', d=None):
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s stroke-linecap="round"/>' % (x1, y1, x2, y2, c, w, (' stroke-dasharray="%s"' % d) if d else ''))
def rc(x, y, w, h, sw=1, c='#111', d=None, f='none'):
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x, y, w, h, f, c, sw, (' stroke-dasharray="%s"' % d) if d else ''))
def tx(x, y, s, fs=8, anc='start', fw='', col='#111', rot=None):
    r = ' transform="rotate(%s %.1f %.1f)"' % (rot, x, y) if rot else ''
    o.append('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="%s" font-weight="%s" fill="%s" font-family="Segoe UI, Arial, sans-serif"%s>%s</text>' % (x, y, fs, anc, fw or 'normal', col, r, esc(s)))
GRY, BLU, RED, GRN = '#777', '#1a49b8', '#c0392b', '#1d7a4f'
SAC, PU, MAK, AGZ, ICL = '#e9e6df', '#f3efe6', '#d8dee6', '#ffffff', '#f6f4f0'

# ---------- model sabitleri (sw_press5.py ile birebir) ----------
KW, KH, KD = 700.0, 1970.0, 860.0            # z −820..40
SOVE, FUGA, T = 45.0, 3.0, 1.5
XP0, XP1, XC1, XR0 = 48.0, 652.0, 452.0, 455.0
TAKOZ, PRES = (121.5, 141.5), (141.5, 1091.5)
RAF1, UC, RAF2, COP, ATMA = (1091.5, 1093.5), (1093.5, 1393.5), (1393.5, 1395.5), (1395.5, 1675.5), (1675.5, 1968.5)
O1 = (68.0, 632.0, 760.0, 1020.0); O2 = (68.0, 632.0, 1120.0, 1370.0); O3 = (68.0, 432.0, 1697.0, 1947.0)
COPK = (60.0, 440.0, 1397.0, 1657.0, -680.0, -80.0)
S = 0.40
FX, FY = 92.0, 152.0                          # ön görünüş sol-üst
SX, SY = 452.0, 152.0                         # yan görünüş sol-üst  (arka solda, ön sağda)
TX_, TY = 860.0, 152.0                        # üst görünüş sol-üst  (arka üstte, ön altta)
def fx(x): return FX + x*S
def fy(y): return FY + (KH - y)*S
def sx(z): return SX + (z + 820.0)*S
def sy(y): return SY + (KH - y)*S
def tpx(x): return TX_ + x*S
def tpy(z): return TY + (z + 820.0)*S

tx(30, 36, 'AUTOKITCH — 2 · PRESS v5 · DÜZ KAPALI CEPHE — ölçüler mm', 14, 'start', 'bold')
tx(30, 54, 'Kabin 700 × 1970 × 860 · cephe 5 düz panel + fuga 3 · kulp/girinti yok (bas-aç mandalı) · üç açıklık, üçü de içine girecek parçadan hesaplandı', 8.2, 'start', '', '#444')
ln(30, 66, 1430, 66, .8, '#999')

# ================= ÖN GÖRÜNÜŞ =================
tx(FX, FY-12, 'ÖN GÖRÜNÜŞ', 9, 'start', 'bold')
rc(fx(0), fy(KH), KW*S, KH*S, 1.3, '#111', None, SAC)
rc(fx(0), fy(120), KW*S, 120*S, 1, '#111', None, PU)                      # plint
tx(fx(350), fy(60)+4, 'plint', 6.2, 'middle', '', GRY)
for a, b in ((0.0, SOVE), (KW-SOVE, KW)):                                  # söve
    rc(fx(a), fy(KH), (b-a)*S, (KH-120)*S, 1, '#111', None, PU)
PAN = [('PRES KAPAĞI', XP0, XP1, TAKOZ[0], 1091.5, O1, 1),
       ('UÇ PANELİ',   XP0, XP1, 1094.5,   1392.5, O2, 0),
       ('ÇÖP KAPAĞI',  XP0, XC1, COP[0],   1672.5, None, 1),
       ('ATMA PANELİ', XP0, XC1, ATMA[0],  1968.5, O3, 0),
       ('BOŞ · KAPALI', XR0, XP1, COP[0],  1968.5, None, 0)]
for ad, x0, x1, y0, y1, ac, kapi in PAN:
    rc(fx(x0), fy(y1), (x1-x0)*S, (y1-y0)*S, 1.1, '#111', None, ICL)
    if ac:
        rc(fx(ac[0]), fy(ac[3]), (ac[1]-ac[0])*S, (ac[3]-ac[2])*S, 1.2, BLU, None, AGZ)
        tx(fx((ac[0]+ac[1])/2), fy((ac[2]+ac[3])/2)+3, '%.0f × %.0f' % (ac[1]-ac[0], ac[3]-ac[2]), 6.6, 'middle', 'bold', BLU)
    if kapi:                                                               # menteşe tarafı + açılma yönü
        ln(fx(x0), fy(y0), fx(x0), fy(y1), 2.2, GRN)
        ln(fx(x0), fy(y0), fx(x1), fy((y0+y1)/2), .7, GRN, '4 3'); ln(fx(x0), fy(y1), fx(x1), fy((y0+y1)/2), .7, GRN, '4 3')
    ty = fy(y1) + 12 if ac else fy((y0+y1)/2) + 3
    tx(fx((x0+x1)/2), ty, ad, 6.4, 'middle', 'bold', '#111')
    if not ac: tx(fx((x0+x1)/2), ty+10, '%.0f × %.0f' % (x1-x0, y1-y0), 6.0, 'middle', '', GRY)
# ölçü zinciri — düşey (solda)
def dimv(xx, y0, y1, s, off=0):
    X = fx(0) - 16 - off
    ln(X, fy(y0), X, fy(y1), .7, RED); ln(X-3, fy(y0), X+3, fy(y0), .7, RED); ln(X-3, fy(y1), X+3, fy(y1), .7, RED)
    tx(X-4, (fy(y0)+fy(y1))/2+2, s, 6.2, 'end', '', RED)
for y0, y1, s in ((0, 120, '120'), (121.5, 141.5, '20'), *[(PRES[0], PRES[1], '950')], (UC[0], UC[1], '300'),
                  (COP[0], COP[1], '280'), (ATMA[0], ATMA[1], '293')): dimv(0, y0, y1, s)
dimv(0, 0, KH, '1970', 34)
# ölçü zinciri — yatay (altta)
def dimh(x0, x1, s, off=0):
    Y = fy(0) + 18 + off
    ln(fx(x0), Y, fx(x1), Y, .7, RED); ln(fx(x0), Y-3, fx(x0), Y+3, .7, RED); ln(fx(x1), Y-3, fx(x1), Y+3, .7, RED)
    tx((fx(x0)+fx(x1))/2, Y-3, s, 6.2, 'middle', '', RED)
for x0, x1, s in ((0, SOVE, '45'), (XP0, XP1, '604'), (KW-SOVE, KW, '45')): dimh(x0, x1, s)
dimh(0, KW, '700', 18)
tx(fx(XC1)+2, fy(COP[1])-6, 'fuga 3', 5.8, 'start', '', GRY)

# ================= YAN GÖRÜNÜŞ =================
tx(SX, SY-12, 'YAN GÖRÜNÜŞ (soldan · arka solda, ön sağda)', 9, 'start', 'bold')
rc(sx(-820), sy(KH), KD*S, KH*S, 1.3, '#111', None, SAC)
rc(sx(-820), sy(120), KD*S, 120*S, 1, '#111', None, PU)
rc(sx(-818.5), sy(1091.5), (818.5-38.5)*S, 2*S+1, 1, '#111', None, '#bbb')   # raf 1
rc(sx(-818.5), sy(1393.5), (818.5-38.5)*S, 2*S+1, 1, '#111', None, '#bbb')   # raf 2
rc(sx(-818), sy(PRES[1]), 800*S, 950*S, 1.2, '#111', None, MAK)              # FERSAH
tx(sx(-418), sy(620), 'FERSAH PZP-400', 7.2, 'middle', 'bold'); tx(sx(-418), sy(560), '640 × 950 × 800', 6.2, 'middle', '', GRY)
rc(sx(-280), sy(1380), 260*S, 8*S+1, 1, '#111', None, '#999')                # askı plakası 1372–1380
rc(sx(-240), sy(1388), 200*S, 30*S, 1, '#111', None, '#cfd6de')              # ISO 9409 dock plakası
tx(sx(-140), sy(1398), 'askı plakası 8 + dock', 6.0, 'middle', '', '#111')
rc(sx(-510), sy(1360), 500*S, 74*S, 1, '#111', None, '#e2e8ef'); tx(sx(-270), sy(1312), 'ÇATAL', 5.8, 'middle', '', '#111')
rc(sx(-160), sy(1360), 98*S, 190*S, 1, '#111', None, '#e2e8ef'); tx(sx(-111), sy(1252), 'PENÇE', 5.8, 'middle', '', '#111')
rc(sx(-120), sy(1360), 40*S, 44*S, 1, '#111', None, '#e2e8ef')
# çöp kutusu — ÜSTÜ AÇIK, üç kenar çizilir (arka · taban · ön), üstte çizgi yok
rc(sx(-680), sy(1657), 600*S, 260*S, 0, '#111', None, '#eef1f4')
ln(sx(-680), sy(1657), sx(-680), sy(1397), 1.2); ln(sx(-680), sy(1397), sx(-80), sy(1397), 1.2)
ln(sx(-80), sy(1397), sx(-80), sy(1657), 1.2)
tx(sx(-380), sy(1600), 'ÜSTÜ AÇIK', 6.2, 'middle', 'bold', GRN)
tx(sx(-380), sy(1520), 'ÇÖP 59 L', 7.0, 'middle', 'bold'); tx(sx(-380), sy(1465), '380 × 260 × 600', 6.0, 'middle', '', GRY)
# robot kolun bıraktığı çöpün yolu: ağız -> huni -> kova
for _p, _q in (((30, 1830), (-260, 1750)), ((-260, 1750), (-260, 1560))):
    ln(sx(_p[0]), sy(_p[1]), sx(_q[0]), sy(_q[1]), 1.1, GRN, '5 3')
o.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>' % (
    sx(-260), sy(1548), sx(-252), sy(1572), sx(-268), sy(1572), GRN))
tx(sx(-250), sy(1790), 'robot kol kovanın üstüne kadar girer', 5.8, 'middle', 'bold', GRN)
o.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="#f0e6d8" stroke="#111" stroke-width="1"/>' % (
    sx(-20), sy(1699.5), sx(-100), sy(1668), sx(-100), sy(1699.5)))          # eşik sacı (kısa)
tx(sx(-70), sy(1714), 'eşik sacı', 5.6, 'middle', '', '#111')
tx(sx(-300), sy(1900), 'AĞIZ TAMAMEN AÇIK — klape yok', 6.4, 'middle', 'bold', GRN)
rc(sx(-818.5), sy(1373.5), 132*S, 260*S, 1, '#111', None, '#eceff2')         # pano
tx(sx(-750), sy(1250), 'PANO', 6.4, 'middle', 'bold')
for _, _, c, d in (O1+(0,0),)[:0]: pass
for ac, nm in ((O1, 'O1'), (O2, 'O2'), (O3, 'O3')):                          # açıklıkların derinlik izi
    ln(sx(38.5), sy(ac[2]), sx(38.5), sy(ac[3]), 2.4, BLU)
    tx(sx(40)+6, (sy(ac[2])+sy(ac[3]))/2+2, nm, 6.4, 'start', 'bold', BLU)
def dimhs(z0, z1, s, off=0):
    Y = sy(0) + 18 + off
    ln(sx(z0), Y, sx(z1), Y, .7, RED); ln(sx(z0), Y-3, sx(z0), Y+3, .7, RED); ln(sx(z1), Y-3, sx(z1), Y+3, .7, RED)
    tx((sx(z0)+sx(z1))/2, Y-3, s, 6.2, 'middle', '', RED)
dimhs(-820, 40, '860')

# ================= ÜST GÖRÜNÜŞ =================
tx(TX_, TY-12, 'ÜST GÖRÜNÜŞ (ön altta)', 9, 'start', 'bold')
rc(tpx(0), tpy(-820), KW*S, KD*S, 1.3, '#111', None, SAC)
rc(tpx(29), tpy(-818), 640*S, 800*S, 1.2, '#111', None, MAK)
tx(tpx(349), tpy(-420), 'FERSAH 640 × 800', 6.6, 'middle', 'bold')
rc(tpx(0), tpy(-820), SOVE*S, KD*S, 1, '#111', None, PU); rc(tpx(KW-SOVE), tpy(-820), SOVE*S, KD*S, 1, '#111', None, PU)
ln(tpx(O1[0]), tpy(40), tpx(O1[1]), tpy(40), 2.4, BLU); tx(tpx(350), tpy(40)+11, 'O1 564', 6.2, 'middle', 'bold', BLU)
def dimht(x0, x1, s, off=0):
    Y = tpy(40) + 26 + off
    ln(tpx(x0), Y, tpx(x1), Y, .7, RED); ln(tpx(x0), Y-3, tpx(x0), Y+3, .7, RED); ln(tpx(x1), Y-3, tpx(x1), Y+3, .7, RED)
    tx((tpx(x0)+tpx(x1))/2, Y-3, s, 6.2, 'middle', '', RED)
dimht(0, KW, '700')

# ================= AÇIKLIK HESABI + PARÇA LİSTESİ =================
BY = 560
rc(TX_-6, BY, 578, 180, 1, '#bbb'); tx(TX_+6, BY+18, 'AÇIKLIK HESABI — içine girecek parçadan', 8.4, 'start', 'bold')
hd = ['açıklık', 'giren parça', 'genişlik', 'yükseklik', 'ölçü']
cw = [92, 168, 104, 108, 92]
for i, hh in enumerate(hd): tx(TX_+6+sum(cw[:i]), BY+38, hh, 6.4, 'start', 'bold')
ln(TX_+6, BY+44, TX_+566, BY+44, .6, '#bbb')
rows = [('O1 PRES', 'pençe 100 + hamur Ø95', 'panel boyu − 2×20', '190 + 70 bilek', '564 × 260'),
        ('O2 UÇ', '3 uç yuvası yan yana', 'panel boyu − 2×20', '190 + 2×30', '564 × 250'),
        ('O3 ATMA', 'pençe 100 + hamur Ø95', 'çöp kolonu − 2×20', '190 + 60', '364 × 250')]
yy = BY+60
for r in rows:
    for i, v in enumerate(r): tx(TX_+6+sum(cw[:i]), yy, v, 6.3, 'start', 'bold' if i in (0, 4) else '', '#111' if i in (0, 4) else '#333')
    yy += 17
ln(TX_+6, yy-9, TX_+566, yy-9, .6, '#bbb')
tx(TX_+6, yy+8, 'GENİŞLİK: açıklıklar panel genişliğince açık, her iki yanda yalnız 20 alın. Yükseklikler parçadan hesaplandı.', 6.2, 'start', '', GRY)
tx(TX_+6, yy+22, 'O3 ağzında KLAPE YOK — robot kol açıklıktan girip kovanın üstüne kadar ulaşır. Kovanın üstü açık (5 yüz).', 6.2, 'start', 'bold', GRN)
tx(TX_+6, yy+36, 'O3 yalnız çöp kolonu genişliğinde — sağdaki boş kolona taşmıyor. Sağ kolon 197 × 573 × 800 tam kapalı.', 6.2, 'start', '', GRY)

PY = 756
rc(TX_-6, PY, 578, 250, 1, '#bbb'); tx(TX_+6, PY+18, 'PARÇA LİSTESİ', 8.4, 'start', 'bold')
hd2 = ['poz', 'parça', 'adet', 'ölçü / malzeme']
cw2 = [34, 246, 44, 244]
for i, hh in enumerate(hd2): tx(TX_+6+sum(cw2[:i]), PY+36, hh, 6.4, 'start', 'bold')
ln(TX_+6, PY+42, TX_+566, PY+42, .6, '#bbb')
plist = [('1', 'Dış kabuk (yan · üst · arka · alt)', '5', 'DKP/paslanmaz 1,5'),
         ('2', 'Plint U + 4 ayar ayağı M12', '1+4', 'bükme sac 1,5'),
         ('3', 'Söve sol / sağ', '2', 'bükme sac 1,5 · 45 geniş'),
         ('4', 'Pres kapağı (3 gizli menteşe)', '1', '604 × 970 · bükme 1,5'),
         ('5', 'Uç paneli (sabit)', '1', '604 × 298 · bükme 1,5'),
         ('6', 'Çöp kapağı (2 gizli menteşe)', '1', '404 × 277 · bükme 1,5'),
         ('7', 'Atma paneli (sabit)', '1', '404 × 293 · bükme 1,5'),
         ('8', 'Sağ boş panel (tam kapalı)', '1', '197 × 573 · bükme 1,5'),
         ('9', 'Ara raf (uç · çöp)', '2', 'sac 2,0 · ön-arka bükümlü'),
         ('10', 'Uç askı plakası (3 U yuva 116)', '1', '500 × 260 × 8'),
         ('11', 'Uç yan taşıyıcı', '2', 'sac 8'),
                  ('12', 'Çöp kutusu + tam çekmece rayı', '1+2', '380 × 260 × 600 = 59 L'),
                  ('13', 'Atma eşik sacı + 2 yan', '3', 'sac 1,5'),
         ('14', 'Pres ankraj plakası + 4 titreşim takozu', '1+4', 'plaka 4 · takoz 40 × 20'),
         ('15', 'Elektrik panosu (PLC · 24 V · 2 sürücü)', '1', 'uç bölmesi arkası'),
         ('16', 'Ön çerçeve iskeleti (kutu profil 20 × 16)', '6', 'panel + menteşe bağlantısı, z 4–20'),
         ('17', 'FERSAH PZP-400 (satın alma)', '1', '640 × 950 × 800')]
yy = PY+58
for r in plist:
    for i, v in enumerate(r): tx(TX_+6+sum(cw2[:i]), yy, v, 6.1, 'start', 'bold' if i == 0 else '', '#111' if i == 1 else '#333')
    yy += 9.7

svg = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d"><rect width="%d" height="%d" fill="#fff"/>%s</svg>' % (W, H, W, H, W, H, ''.join(o))
p = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\2_PRESS_v5\ist2_press_detay_v9.svg"
io.open(p, 'w', encoding='utf-8').write(svg); print('yazildi:', p)
try:
    import cairosvg; cairosvg.svg2png(url=p, write_to=p.replace('.svg', '.png'), output_width=W*2, output_height=H*2); print('png ok')
except Exception as e: print('png yok:', e)
