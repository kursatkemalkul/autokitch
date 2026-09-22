# -*- coding: utf-8 -*-
# TOPPING v28 — İSTASYON YERLEŞİM PAFTASI (ön · üst · yan + ölçü + parça)
# v27'ye göre değişenler: (1) kol 1,8 ile çalışmayan raf pimi → KAPAK AÇMA RAMPASI
#                         (2) ALT sıraları 4 kap, aralık 1,0 (hava kanalı yandan ARKA plenuma alındı)
#                         (3) klape menteşesi ÜSTE (alttan menteşeli klape tepsi düzlemini kapatıyordu)
import io, math, xml.dom.minidom
W, H = 1460, 900
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
def para(x, y, s, maxc, fs=5.9, col='#333', fw='', lh=None):
    lh = lh or fs*1.6; cur = ''; lines = []
    for wd in s.split(' '):
        if cur and len(cur)+1+len(wd) > maxc: lines.append(cur); cur = wd
        else: cur = (cur+' '+wd) if cur else wd
    if cur: lines.append(cur)
    for l in lines: tx(x, y, l, fs, 'start', fw, col); y += lh
    return y
def f1(v): return ('%.1f' % v).replace('.', ',')
GRN, RED, BLU, GRY, AMB = '#1d7a4f', '#c0392b', '#1a49b8', '#666', '#b7791f'
PC, POM, STEEL, LIGHT, COLD = '#dbeeff', '#f4f4f4', '#cfd8dc', '#f7f6f2', '#eaf2fb'

# ================= GEOMETRİ (cm) — SolidWorks modelinden birebir =================
KW, KD, KH = 70.0, 86.0, 197.0          # kabin: genişlik · derinlik (kasa 82 + klape 4) · yükseklik
IX0, IX1 = 4.25, 65.75                  # yalıtımlı hücre iç genişliği (61,5)
PLINT = 15.8                            # plint üstü (soğutma grubu 0–15,8) · hücre iç tabanı 20,05
KAPW, KAPH = 14.0, 26.4                 # kap dış eni · kızak+plaka dahil yüksekliği
KATX = (27.0, 43.0)                     # kat kap merkezleri (v25)
ALTX = (12.5, 27.5, 42.5, 57.5)         # ALT kap merkezleri (4 × 14 + 3 × 1,0 fuga = 59,0; kenar payı 1,25)
RAF = [("kat 1", 170.0), ("kat 2", 129.0), ("kat 3", 88.0), ("ALT 1", 47.0), ("ALT 2", 20.3)]
TEPSI = {"kat 1": 158.0, "kat 2": 117.0, "kat 3": 76.0}
KLAPE = [("kat 1", 155.8, 196.8), ("kat 2", 114.8, 155.8), ("kat 3", 73.8, 114.8), ("ALT 1", 46.8, 73.8), ("ALT 2", 19.8, 46.8)]
KAP_Z0, KAP_Z1 = 2.0, 70.0              # yan kesitte kap ön/arka (ön yüzden geriye)
S = 2.28                                 # px/cm

tx(30, 38, 'AUTOKITCH — TOPPING v28 (8 Eyl 2026) — İSTASYON YERLEŞİMİ: ön · üst · yan · kapak açma rampası — ölçüler cm', 14, 'start', 'bold', '#111')
tx(30, 58, 'v27 → v28: ① raf pimi Ø8 → KAPAK AÇMA RAMPASI (kol 1,8 ile pim 3,2 cm arkada olamaz)  ② ALT sırası 4 kap · aralık 1,0 (hava kanalı yandan ARKA plenuma)  ③ klape menteşesi ÜSTTE (alttan menteşeli klape tepsi düzlemini kapatıyordu)  ④ pano sağ arka kolona', 8.4, 'start', '', '#444')
ln(30, 70, 1430, 70, .8, '#999')

# ---------------------------------------------------------------- A · ÖN GÖRÜNÜŞ
rc(30, 84, 250, 520, 1, 6, '#bbb'); tx(42, 100, 'A · ÖN GÖRÜNÜŞ (klapeler kaldırılmış)', 8.4, 'start', 'bold')
AX, AY = 62.0, 580.0
def ax_(x): return AX + x*S
def ay_(y): return AY - y*S
rc(ax_(0), ay_(KH), KW*S, KH*S, 1.1, 0, '#111', None, LIGHT)                       # kabin dış
rc(ax_(IX0), ay_(196.8), (IX1-IX0)*S, (196.8-19.8)*S, .7, 0, '#999', None, COLD)   # yalıtımlı hücre
rc(ax_(0.5), ay_(PLINT), (KW-1)*S, PLINT*S, .7, 0, '#999', None, '#fff')           # plint
for i in range(13): ln(ax_(6+i*4.6), ay_(3), ax_(6+i*4.6), ay_(13), .5, '#aaa')
for nm, y0, y1 in KLAPE:                                                            # klape sınırları
    ln(ax_(0), ay_(y0), ax_(KW), ay_(y0), .6, RED, '4,3')
for nm, yr in RAF:
    xs = KATX if nm.startswith('kat') else ALTX
    for xc in xs:
        if nm == 'kat 2' and xc == 43.0:                                            # v25: sağ pozisyon boş
            rc(ax_(xc-KAPW/2), ay_(yr+KAPH), KAPW*S, KAPH*S, .6, 0, '#bbb', '3,3'); continue
        rc(ax_(xc-KAPW/2), ay_(yr+KAPH), KAPW*S, KAPH*S, .8, 0, '#111', None, PC)
        ci(ax_(xc), ay_(yr+16.9), 3.5*S/2, .5, '#888')                              # tarak göbeği
        ci(ax_(xc), ay_(yr+6.7), 7.0*S/2, .5, '#888')                               # helezon
    ln(ax_(xs[0]-7.3), ay_(yr), ax_(xs[-1]+7.3), ay_(yr), 1.2, GRN)                 # L raf düzlemi
for nm, ty in TEPSI.items():                                                        # robot pide tepsisi
    ln(ax_(19), ay_(ty), ax_(51), ay_(ty), 1.6, RED)
    rc(ax_(20), ay_(ty+2.0), 30*S, 2.0*S, .5, 0, RED, '2,2')
tx(ax_(35), ay_(TEPSI['kat 1'])-4, 'pide tepsisi Ø32', 5.6, 'middle', 'bold', RED)
rc(ax_(4.75), ay_(190), 14.25*S, 110*S, .6, 0, BLU, '3,3'); tx(ax_(11.9), ay_(135), 'evaporatör', 5.4, 'middle', '', BLU)
tx(ax_(11.9), ay_(129), '+ fan', 5.4, 'middle', '', BLU)
# dikey ölçü zinciri
def vdim(x, y0, y1, s, col='#111'):
    ln(x, ay_(y0), x, ay_(y1), .7, col); ln(x-3, ay_(y0), x+3, ay_(y0), .7, col); ln(x-3, ay_(y1), x+3, ay_(y1), .7, col)
    tx(x+4, (ay_(y0)+ay_(y1))/2+2, s, 5.6, 'start', 'bold', col)
XD = ax_(KW)+8
for (a, b, s_) in ((0, 15.8, '15,8'), (20.3, 46.7, '26,4'), (47.0, 73.4, '26,4'), (88.0, 114.4, '26,4'), (129.0, 155.4, '26,4'), (170.0, 196.4, '26,4')): vdim(XD, a, b, s_)
XD2 = XD+34
for (a, b, s_) in ((73.4, 88.0, '14,6'), (114.4, 129.0, '14,6'), (155.4, 170.0, '14,6')): vdim(XD2, a, b, s_, RED)
tx(XD2+2, ay_(200), 'robot / tepsi boşluğu', 5.6, 'start', 'bold', RED)
vdim(ax_(0)-14, 0, KH, '197')
tx(ax_(KW/2), ay_(-6), '70', 6.2, 'middle', 'bold')

# ---------------------------------------------------------------- B · ÜST GÖRÜNÜŞ
rc(292, 84, 246, 520, 1, 6, '#bbb'); tx(304, 100, 'B · ÜST GÖRÜNÜŞ — kat düzlemi ve ALT düzlemi', 8.4, 'start', 'bold')
def topview(bx, by, isk, baslik):
    def tx_(x): return bx + x*S
    def ty_(z): return by + z*S
    rc(tx_(0), ty_(0), KW*S, KD*S, 1.1, 0, '#111', None, LIGHT)
    rc(tx_(IX0), ty_(4.0), (IX1-IX0)*S, 75.5*S, .7, 0, '#999', None, COLD)
    tx(tx_(KW/2), ty_(0)-6, baslik, 7, 'middle', 'bold')
    xs = KATX if isk else ALTX
    for xc in xs:
        rc(tx_(xc-KAPW/2), ty_(KAP_Z0), KAPW*S, (KAP_Z1-KAP_Z0)*S, .8, 0, '#111', None, PC)
        rc(tx_(xc-2.25), ty_(62.0), 4.5*S, 5.0*S, .6, 0, RED, None, '#fff')          # ağız 5 × 4,5
    if isk:
        rc(tx_(4.75), ty_(22), 14.25*S, 35*S, .6, 0, BLU, '3,3'); tx(tx_(11.9), ty_(41), 'evaporatör', 5.2, 'middle', '', BLU)
        rc(tx_(61.25), ty_(10), 4*S, 60*S, .6, 0, BLU, '3,3'); tx(tx_(63.2), ty_(43), 'kablo', 5.2, 'middle', '', BLU)
        rc(tx_(47), ty_(4.5), 18*S, 70*S, .6, 0, AMB, '3,3'); tx(tx_(56), ty_(8), 'pano', 5.2, 'middle', '', AMB)
    else:
        rc(tx_(IX0), ty_(4.5), (IX1-IX0)*S, 6*S, .6, 0, BLU, '3,3'); tx(tx_(35), ty_(9), 'ALT hava kanalı (arka plenum)', 5.2, 'middle', '', BLU)
    rc(tx_(3), ty_(82), 64*S, 4*S, .7, 0, '#111', None, '#e8e8e8'); tx(tx_(35), ty_(85), 'klape 4', 5.2, 'middle', '', '#333')
    # yatay ölçüler
    yb = ty_(KD)+13
    ln(tx_(0), yb, tx_(KW), yb, .7); tx(tx_(KW/2), yb-3, '70', 6, 'middle', 'bold')
    yb2 = yb+12
    sol = (IX0, 20.0, f1(20.0-IX0)) if isk else (IX0, xs[0]-7, f1(xs[0]-7-IX0))
    for a, b, s_ in ([sol] + [(xc-7, xc+7, '14') for xc in xs] + [(xs[-1]+7, IX1, f1(IX1-xs[-1]-7))]):
        ln(tx_(a), yb2, tx_(b), yb2, .6); ln(tx_(a), yb2-3, tx_(a), yb2+3, .6); ln(tx_(b), yb2-3, tx_(b), yb2+3, .6)
        tx(tx_((a+b)/2), yb2-3, s_, 5.2, 'middle', 'bold')
    if not isk:
        for i in range(len(xs)-1):
            tx(tx_((xs[i]+xs[i+1])/2), yb2+11, '1,0', 5.0, 'middle', 'bold', RED)
    return yb2
topview(322, 130, True, 'kat düzlemi (kat 1-2-3)')
topview(322, 385, False, 'ALT düzlemi (sıra 1-2)')

# ---------------------------------------------------------------- C · YAN KESİT
rc(550, 84, 246, 520, 1, 6, '#bbb'); tx(562, 100, 'C · YAN KESİT — kat 1', 8.4, 'start', 'bold')
CX, CY = 578.0, 580.0
def cx_(z): return CX + z*S
def cy_(y): return CY - y*S
rc(cx_(0), cy_(KH), KD*S, KH*S, 1.1, 0, '#111', None, LIGHT)
rc(cx_(4), cy_(196.8), 75.5*S, 177*S, .7, 0, '#999', None, COLD)
rc(cx_(82), cy_(196.8), 4*S, 41*S, .8, 0, '#111', None, '#e8e8e8')                  # klape (kat 1)
ci(cx_(84), cy_(196.8), 2.2, 1.4, RED, None, RED); tx(cx_(84)+5, cy_(194), 'menteşe ÜSTTE', 5.6, 'start', 'bold', RED)
for nm, yr in RAF:                                                                   # kaplar (yandan)
    rc(cx_(KAP_Z0+12), cy_(yr+KAPH), (KAP_Z1-KAP_Z0)*S, KAPH*S, .8, 0, '#111', None, PC)
    ln(cx_(14), cy_(yr), cx_(82), cy_(yr), 1.2, GRN)
rc(cx_(14+62), cy_(170+2.4), 5*S, 2.4*S, .7, 0, RED, None, '#fff')                   # ağız (kat 1)
tx(cx_(74), cy_(174.5), 'ağız 5 × 4,5', 5.4, 'middle', 'bold', RED)
ln(cx_(60), cy_(158), cx_(92), cy_(158), 1.6, RED)                                   # tepsi düzlemi
tx(cx_(76), cy_(152), 'tepsi Ø32 · düzlem 158', 5.4, 'middle', 'bold', RED)
rc(cx_(4), cy_(196.8), 7.75*S, 177*S, .6, 0, AMB, '3,3')
tx(cx_(12), cy_(200), 'motor / pano bölmesi 7,75', 5.4, 'start', 'bold', AMB)
ln(cx_(0), cy_(-6), cx_(KD), cy_(-6), .7); tx(cx_(KD/2), cy_(-6)-3, '86 = kasa 82 + klape 4', 6, 'middle', 'bold')
for a, b, s_ in ((14, 82, '68 kap'), (4, 14, '10 arka')):
    ln(cx_(a), cy_(-16), cx_(b), cy_(-16), .6); tx(cx_((a+b)/2), cy_(-16)-3, s_, 5.4, 'middle', 'bold')

# ---------------------------------------------------------------- D · KAPAK AÇMA RAMPASI
rc(808, 84, 622, 268, 1, 6, '#bbb'); tx(820, 100, 'D · KAPAK AÇMA RAMPASI (v27 raf pimi yerine) — kesit, ölçüler mm', 8.4, 'start', 'bold')
DX, DY, DS = 860.0, 300.0, 2.9          # px/mm
def dx_(z): return DX + (z+80)*DS       # z −80 … 0
def dy_(y): return DY - y*DS
rc(dx_(-80), dy_(24), 80*DS, 4*DS, .8, 0, '#111', None, PC); tx(dx_(-60), dy_(26)+3, 'taban plakası 4', 5.4, 'middle', '', '#333')
rc(dx_(-80), dy_(20), 35*DS, 20*DS, .5, 0, '#ccc', '3,3')
rc(dx_(-80), dy_(18.5), 48*DS, 3*DS, .9, 0, RED, None, '#fff')                       # ağız kapağı (kapalı)
tx(dx_(-56), dy_(13), 'ağız kapağı PC 51 × 50 × 3 (kapalı)', 5.4, 'middle', 'bold', RED)
ci(dx_(-30), dy_(17), 2*DS, .9, '#111', None, STEEL); tx(dx_(-30), dy_(17)-9, 'menteşe mili Ø4 + burulma yayı', 5.4, 'middle', 'bold')
rc(dx_(-32), dy_(17), 4*DS, 17*DS, .9, 0, '#111', None, '#ffe9c9')                   # kol 1,8
tx(dx_(-32)-4, dy_(9), 'kol 1,8', 5.6, 'end', 'bold', AMB)
poly([(dx_(0), dy_(0)), (dx_(-15), dy_(12)), (dx_(-25), dy_(12)), (dx_(-25), dy_(-2)), (dx_(0), dy_(-2))], .9, GRN, '#dff0e6')
tx(dx_(-12), dy_(16), 'RAMPA 15 × 12 + düz tepe 10', 5.6, 'middle', 'bold', GRN)
rc(dx_(-25), dy_(-2), 15*DS, 8*DS, .8, 0, GRN, None, '#eef7f1'); tx(dx_(-17), dy_(-6)+4, 'çapraz çubuk 8×8 (L raflar arası)', 5.4, 'middle', '', GRN)
ln(dx_(-80), dy_(0), dx_(0), dy_(0), .7, '#111', '5,3'); tx(dx_(-80)-4, dy_(0)+3, 'kap alt düzlemi', 5.4, 'end', 'bold')
for a, b, s_, yy in ((-80, -30, '50 = ağız', 30), (-25, 0, '25 rampa', 30)):
    ln(dx_(a), dy_(yy), dx_(b), dy_(yy), .6); ln(dx_(a), dy_(yy)-3, dx_(a), dy_(yy)+3, .6); ln(dx_(b), dy_(yy)-3, dx_(b), dy_(yy)+3, .6)
    tx(dx_((a+b)/2), dy_(yy)-3, s_, 5.4, 'middle', 'bold')
py = para(1190, 130, 'Kap son 1,5 cm girerken kol rampaya biner, 12 mm kalkar (≈73°), kapak sarkar; düz tepe kap yerindeyken açık tutar. Kap 1,5 cm geri çekilince burulma yayı kapatır.', 44, 6.0, '#333')
py = para(1190, py+4, 'Rampa yalnız TOPPING katındaki 6 pozisyonda vardır (x +3). ALT ve STORE raflarında rampa yok → kapak hep kapalı.', 44, 6.0, '#333')
py = para(1190, py+4, 'NEDEN: pim menteşeden 3,2 cm arkada olsaydı 1,8 cm kol ona erişemezdi; 3,2 cm kol da 2 cm boşlukta 90° dönemezdi.', 44, 6.0, RED)

# ---------------------------------------------------------------- E · ALT RAF DAĞILIMI
rc(30, 620, 766, 252, 1, 6, '#bbb'); tx(42, 640, 'E · ALT RAF DAĞILIMI ve HAFTALIK DENGE (kap 12,5 L)', 8.4, 'start', 'bold')
hd = ['malzeme', 'katta', 'kap/hafta', 'ALT yedek', 'kaynak', 'dolduran']
cw = [110, 55, 70, 75, 190, 140]; x_ = 46
for i, h_ in enumerate(hd): tx(x_+sum(cw[:i]), 662, h_, 6.4, 'start', 'bold', '#111')
ln(46, 668, 780, 668, .6, '#bbb')
rows = [('KAŞAR rende', '2', '6', '4', 'eleman haftada 1 (dolu kap)', 'eleman'),
        ('SUCUK küp', '1', '2', '1', 'eleman haftada 1 (dolu kap)', 'eleman'),
        ('KIYMA kavrulmuş', '1', '3', '1 (çözülme)', 'STORE −18 → robot gece taşır', 'robot'),
        ('KUŞBAŞI sote', '1', '3', '1 (çözülme)', 'STORE −18 → robot gece taşır', 'robot'),
        ('park (boş kap)', '—', '—', '1', 'robotun boşu bıraktığı yer', '—'),
        ('kat 2 sağ pozisyon', 'BOŞ', '—', '—', '3. kaşar kabı seçeneği (Kemal kararı)', '—')]
yy = 682
for r in rows:
    for i, v in enumerate(r): tx(x_+sum(cw[:i]), yy, v, 6.2, 'start', 'bold' if i == 0 else '', '#111' if i == 0 else '#333')
    yy += 15
ln(46, yy-9, 780, yy-9, .6, '#bbb')
tx(46, yy+6, 'TOPLAM ALT slot = 4 + 1 + 1 + 1 + 1 = 8 = 2 sıra × 4 → v25 dağılımı korunuyor.', 6.6, 'start', 'bold', GRN)
yy = para(46, yy+22, 'Robot haftada ≈ 14 kap değişimi yapar (kaşar 6 · kıyma 3 · kuşbaşı 3 · sucuk 2) ve gece STORE −18\'den 4 donmuş kabı ALT çözülme slotlarına taşır. Boşalan kap, dolusunun çıktığı ALT slotuna konur; ayrı boş-kap deposu gerekmez.', 150, 6.2, '#333')
yy = para(46, yy+4, 'Eleman haftada 1 kez gelir: 5 dolu kap (4 kaşar + 1 sucuk) ALT\'a koyar, 8 boş kabı alır. ALT sırası 3 kaba düşseydi bu tur haftada 2 kez olurdu — o yüzden 4 kap korundu.', 150, 6.2, GRN, 'bold')
yy = para(46, yy+6, 'DİKEY: plint 15,8 · ALT 2 → 20,3–46,7 · ALT 1 → 47,0–73,4 · kat 3 → 88,0–114,4 · kat 2 → 129,0–155,4 · kat 1 → 170,0–196,4 · tepsi düzlemleri 76 / 117 / 158 (kap altından 12 aşağı).', 150, 6.2, '#333')
yy = para(46, yy+2, 'GENİŞLİK: hücre içi 4,25–65,75 (61,5). Kat: evaporatör 4,75–19,0 · kaplar 20–34 ve 36–50 · hava dönüşü + kablo 61,0–65,25. ALT: 4 × 14 + 3 × 1,0 = 59,0, kenar payı 1,25.', 150, 6.2, '#333')

# ---------------------------------------------------------------- F · PARÇA / ALT GRUP
rc(808, 368, 622, 372, 1, 6, '#bbb'); tx(820, 388, 'F · ALT MONTAJLAR ve PARÇA SAYILARI (SolidWorks)', 8.4, 'start', 'bold')
grp = [('KAP_14x68x24', '15 parça', '13 örnek', 'gövde PC 5 · taban plakası 0,4 · kızak ×2 · üst kapak · ön çekme dudağı · ağız kapağı + mil Ø4 + burulma yayı + kol 1,8 · helezon POM Ø70 hatve 5 · topuz Ø50 · tarak 304 (göbek Ø30 + omurga 6 + 4 çubuk Ø6) · keçe ×2'),
       ('L_RAF_CIFTI', '2 parça', '8 örnek', 'L profil 2 mm ×2 (ALT sıraları — rampa yok, kapak kapalı kalır)'),
       ('L_RAF_CIFTI_PIMLI', '4 parça', '6 örnek', 'L profil ×2 + çapraz çubuk 8×8 + kapak açma rampası (yalnız kat pozisyonları)'),
       ('SOKET_MOTOR', '4 parça', '6 örnek', 'yaylı soket ×2 (helezon z 3,8 · tarak z 14,0) + adım motoru (dozaj) + redüktörlü motor 10 W (tarak)'),
       ('KLAPE_H410', '4 parça', '3 örnek', 'bükme sac klape 1,5 + üst pivot mili + gazlı amortisör ×2 — kat 1-2-3'),
       ('KLAPE_H270', '4 parça', '2 örnek', 'aynı form, 270 yüksek — ALT 1-2'),
       ('TEPSI_PIDE_D320', '2 parça', '3 örnek', 'robot pide tepsisi Ø320 × 2 + pide Ø300 × 18 (referans)'),
       ('TOPPING kasa', '41 parça', '—', 'dış kabuk 1,5 · PU 40 · iç kabuk 1,0 · plint + soğutma grubu · evaporatör + fan ×2 · arka kapak sacı · pano (plaka + PLC + güç kaynağı + sürücü ×6)')]
gy = 408
for a_, b_, c_, d_ in grp:
    tx(820, gy, a_, 6.6, 'start', 'bold', '#111'); tx(985, gy, b_, 6.2, 'start', '', '#333'); tx(1050, gy, c_, 6.2, 'start', 'bold', GRN)
    gy = para(820, gy+11, d_, 108, 5.9, '#333') + 6
ln(820, gy, 1418, gy, .6, '#bbb'); gy += 14
tx(820, gy, 'TOPLAM: 88 bileşen · çakışma taraması 0', 7, 'start', 'bold', GRN); gy += 18
gy = para(820, gy, 'KONTROL ✓ kat 27 = kap 26,4 + raf 0,2 + pay 0,4 · robot boşluğu 14,6 ≥ tepsi 2 + pide 1,8 + pay · açık kapak sarkması 5,3 < pide payı 10 · ALT kap aralığı 1,0 ≥ çatal toleransı · klape üst menteşeli, tepsi düzlemi klape alt kenarının 2,2 cm üstünde.', 112, 6.0, GRN, 'bold')
gy = para(820, gy+4, 'AÇIK: kabin derinliği modelde 86 (v25 paftası 84 diyordu — arka teknik bölme 2 cm daha derin). Robot süpürme menzili: tepsi klape hattının 10 cm önüne taşıyor (v25 "süpürme R27" bunu öngörüyor), kobot menzili teyit edilecek. Burulma yayı kuvveti ve kapak contası hâlâ açık.', 112, 6.0, AMB)
tx(W-30, H-14, 'AUTOKITCH · arastirma/3_TOPPING/ist3_topping_detay_v28 · 8 Eyl 2026', 7, 'end', '', GRY)

svg = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">\n<rect x="0" y="0" width="%d" height="%d" fill="#fff"/>\n' % (W, H, W, H, W, H) + '\n'.join(o) + '\n</svg>'
xml.dom.minidom.parseString(svg.encode('utf-8'))
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\ist3_topping_detay_v28.svg"
io.open(out, 'w', encoding='utf-8').write(svg)
print('yazildi + XML gecerli:', out)
