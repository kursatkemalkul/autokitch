# -*- coding: utf-8 -*-
# KUTU ISTASYONU — istek krokisi v2 (SADE: mekanizma yok, problem tarifi var)
import io

S = 0.3
def px(mm): return mm*S
W, H = 1060, 800
parts = []
def ln(x1,y1,x2,y2,w=2,c='#1a1a1a',dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.1f"%s/>' % (x1,y1,x2,y2,c,w,d))
def rc(x,y,w,h,sw=2,c='#1a1a1a',fill='none',dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    parts.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" stroke="%s" stroke-width="%.1f" fill="%s"%s/>' % (x,y,w,h,c,sw,fill,d))
def tx(x,y,s,size=14,c='#1a1a1a',w='normal',anchor='start'):
    parts.append('<text x="%.1f" y="%.1f" font-family="Arial" font-size="%.1f" fill="%s" font-weight="%s" text-anchor="%s">%s</text>' % (x,y,size,c,w,anchor,s))
def oy(x,y1,y2,label,side='r'):
    ln(x,y1,x,y2,1.2,'#b3452b'); ln(x-5,y1,x+5,y1,1.2,'#b3452b'); ln(x-5,y2,x+5,y2,1.2,'#b3452b')
    if side=='r': tx(x+8,(y1+y2)/2+4,label,12.5,'#b3452b','bold')
    else: tx(x-8,(y1+y2)/2+4,label,12.5,'#b3452b','bold','end')
def ox(y,x1,x2,label):
    ln(x1,y,x2,y,1.2,'#b3452b'); ln(x1,y-5,x1,y+5,1.2,'#b3452b'); ln(x2,y-5,x2,y+5,1.2,'#b3452b')
    tx((x1+x2)/2,y+16,label,12.5,'#b3452b','bold',anchor='middle')

# Baslik
tx(30,36,'KUTU İSTASYONU — İSTEK KROKİSİ v2',21,'#1a1a1a','bold')
tx(30,58,'Box station — request sketch. Soru / question: bu hacim içinde en üstteki açık kutuyu alıp komutla katlayabilir misiniz? / can you pick the top flat blank and fold it on command within this volume?',11.5,'#666')
ln(30,70,W-30,70,1,'#999')

# Kabin
X0, Y0 = 90, 110
GW, GH, AYAK = px(850), px(1850), px(120)
rc(X0, Y0, GW, GH, 2.6)
for ax in (X0+8, X0+GW-16):
    rc(ax, Y0+GH, 8, AYAK, 1.8)
ln(X0, Y0+GH, X0+GW, Y0+GH, 2.6)

# Sol: yassi istif (blank 410 genis, 1700 yukseklik)
mx = X0+px(40)
mtop = Y0+GH-px(1700)-px(60)
mbot = Y0+GH-px(60)
iy = mbot
while iy > mtop:
    ln(mx, iy, mx+px(410), iy, 1.6, '#8a6a3a')
    iy -= 9
rc(mx-6, mtop-6, px(410)+12, mbot-mtop+12, 1.4, '#555', dash='4,3')
tx(mx+px(205), mtop-14, 'AÇIK KUTU İSTİFİ / flat stack', 12.5, '#1a1a1a', 'bold', 'middle')
# istif olculeri
oy(mx-22, mtop, mbot, '170', side='l')
ox(mbot+20, mx, mx+px(410), '41')
tx(mx+px(205), mbot+52, '560 açık kutu üst üste (haftalık)', 12, '#333', 'normal', 'middle')
tx(mx+px(205), mbot+68, '1 kutu ≈ 3 mm · derinlemesine 78 cm', 11.5, '#666', 'normal', 'middle')

# Sag: bos hacim — cozum size ait
bx = mx+px(410)+18
rc(bx, Y0+px(40), X0+GW-bx-px(40)+X0*0, GH-px(80), 1.6, '#1d7a4f', dash='8,6')
bw = (X0+GW-px(40)) - bx
parts.pop()  # yanlis genislikli rect'i geri al
rc(bx, Y0+px(40), (X0+GW-px(40))-bx, GH-px(80), 1.6, '#1d7a4f', dash='8,6')
cx_ = bx + ((X0+GW-px(40))-bx)/2
tx(cx_, Y0+GH/2-30, 'KALAN HACİM', 14, '#1d7a4f', 'bold', 'middle')
tx(cx_, Y0+GH/2-8, 'katlama çözümü', 12.5, '#1d7a4f', 'normal', 'middle')
tx(cx_, Y0+GH/2+10, 'SİZE AİT', 12.5, '#1d7a4f', 'bold', 'middle')
tx(cx_, Y0+GH/2+34, 'your solution', 11, '#7aa88c', 'normal', 'middle')

# Kabin olculeri
ox(Y0+GH+AYAK+26, X0, X0+GW, '≈ 85 cm (esnek / flexible 70-100)')
oy(X0+GW+14, Y0, Y0+GH, '185')
oy(X0-52, Y0, Y0+GH+AYAK, '197', side='l')
tx(X0, Y0+GH+AYAK+52, 'Derinlik / depth 84 cm · ayak / legs 12 cm', 12, '#666')

# Sag ust: kutu bilgisi (urun bilgisi — mekanizma degil)
NX = 660
tx(NX, 110, 'KUTU / THE BOX:', 15, '#1a1a1a', 'bold')
# acik blank cizimi
bx2, by2 = NX+10, 130
rc(bx2, by2, 156, 82, 1.8, '#8a6a3a')
ln(bx2+52, by2, bx2+52, by2+82, 1, '#c9b28e', '4,3')
ln(bx2+104, by2, bx2+104, by2+82, 1, '#c9b28e', '4,3')
ln(bx2, by2+20, bx2+156, by2+20, 1, '#c9b28e', '4,3')
ln(bx2, by2+62, bx2+156, by2+62, 1, '#c9b28e', '4,3')
tx(bx2+78, by2+100, 'AÇIK HÂLİ / flat: ≈ 78 × 41 cm', 12.5, '#333', 'normal', 'middle')
tx(bx2+78, by2+116, 'kalınlık / thickness ≈ 3 mm', 11.5, '#666', 'normal', 'middle')
# ok
tx(bx2+78, by2+146, '↓ katlanınca / folded', 12, '#b3452b', 'bold', 'middle')
# kurulu kutu
kx2, ky2 = NX+40, by2+165
rc(kx2, ky2+18, 96, 28, 1.8)
ln(kx2, ky2+18, kx2+22, ky2, 1.6); ln(kx2+22, ky2, kx2+118, ky2, 1.6); ln(kx2+118, ky2, kx2+96, ky2+18, 1.6)
tx(kx2+48, ky2+66, '32 × 32 × 4,5 cm', 12.5, '#333', 'normal', 'middle')

# Istek ozeti
ny_ = by2+265
tx(NX, ny_, 'İSTEK / REQUEST:', 15, '#1a1a1a', 'bold')
notlar = [
 ('· Haftalık ~560 kutu istifliyoruz', '#1a1a1a', 13, 'normal'),
 ('  (günde ~80 · tepe saatte ~12)', '#555', 12.5, 'normal'),
 ('· Komut gelince EN ÜSTTEKİNİ', '#1a1a1a', 13, 'bold'),
 ('  alıp TEK kutu katlayacak', '#1a1a1a', 13, 'bold'),
 ('· Sürekli çalışmaz — az üretim,', '#1a1a1a', 13, 'normal'),
 ('  sanayi tipi makine aramıyoruz', '#1a1a1a', 13, 'normal'),
 ('· Komut: 24V sinyal / PLC', '#1a1a1a', 13, 'normal'),
 ('· Ölçüler esnek — öneriniz', '#555', 12.5, 'normal'),
 ('  değerlidir', '#555', 12.5, 'normal'),
]
yy = ny_+28
for s, c, sz, w_ in notlar:
    tx(NX, yy, s, sz, c, w_)
    yy += 22
tx(NX, yy+14, 'EN: we stack ~560 flat boxes/week;', 11, '#888')
tx(NX, yy+30, 'on command, pick the TOP blank and', 11, '#888')
tx(NX, yy+46, 'fold ONE box within this volume;', 11, '#888')
tx(NX, yy+62, 'not continuous — no industrial line.', 11, '#888')

tx(W-30, H-16, 'AUTOKITCH · kutu_istasyonu_teknik_v2', 11, '#999', anchor='end')

svg = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d"><rect width="%d" height="%d" fill="#ffffff"/>%s</svg>' % (W,H,W,H,W,H,''.join(parts))
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\kutu_istasyonu_teknik_v2.svg"
io.open(out,'w',encoding='utf-8').write(svg)
print('ok', out)
