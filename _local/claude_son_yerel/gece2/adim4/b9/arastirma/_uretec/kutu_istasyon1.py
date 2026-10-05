# -*- coding: utf-8 -*-
# KUTU ISTASYONU — konsept istek krokisi v1 (makine ureticisine ek)
# S=0.3 px/mm
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
def ci(cx,cy,r,sw=2,c='#1a1a1a',fill='none'):
    parts.append('<circle cx="%.1f" cy="%.1f" r="%.1f" stroke="%s" stroke-width="%.1f" fill="%s"/>' % (cx,cy,r,c,sw,fill))
def arrow(x1,y1,x2,y2,w=2.2,c='#b3452b'):
    ln(x1,y1,x2,y2,w,c)
    import math
    a = math.atan2(y2-y1,x2-x1)
    for da in (2.6,-2.6):
        ln(x2,y2,x2-10*math.cos(a+da),y2-10*math.sin(a+da),w,c)
def oy(x,y1,y2,label,side='r'):  # dikey olcu
    ln(x,y1,x,y2,1.2,'#b3452b'); ln(x-5,y1,x+5,y1,1.2,'#b3452b'); ln(x-5,y2,x+5,y2,1.2,'#b3452b')
    if side=='r':
        tx(x+8,(y1+y2)/2+4,label,12.5,'#b3452b','bold')
    else:
        tx(x-8,(y1+y2)/2+4,label,12.5,'#b3452b','bold','end')
def ox(y,x1,x2,label):  # yatay olcu
    ln(x1,y,x2,y,1.2,'#b3452b'); ln(x1,y-5,x1,y+5,1.2,'#b3452b'); ln(x2,y-5,x2,y+5,1.2,'#b3452b')
    tx((x1+x2)/2,y+16,label,12.5,'#b3452b','bold',anchor='middle')

# Baslik
tx(30,36,'KUTU İSTASYONU — KONSEPT İSTEK KROKİSİ v1',21,'#1a1a1a','bold')
tx(30,58,'Box-erecting station — concept request sketch (ölçüler esnek, üretici önerisine açıktır / dimensions flexible, open to manufacturer proposal)',12.5,'#666')
ln(30,70,W-30,70,1,'#999')

# Kabin: 850 x govde 1850 + ayak 120, derinlik 840
X0, Y0 = 70, 100
GW, GH, AYAK = px(850), px(1850), px(120)
rc(X0, Y0, GW, GH, 2.6)
# ayaklar
for ax in (X0+8, X0+GW-16):
    rc(ax, Y0+GH, 8, AYAK, 1.8)
ln(X0, Y0+GH, X0+GW, Y0+GH, 2.6)

# ic bolme cizgisi: sol magazin 450 / sag mekanizma 400
XM = X0 + px(450)
ln(XM, Y0, XM, Y0+GH, 1.8, '#1a1a1a', dash='7,5')

# --- SOL: yassi blank magazini ---
tx(X0, Y0-26, 'YASSI KUTU MAGAZİNİ', 12.5, '#1a1a1a', 'bold')
mx, mtop, mbot = X0+px(30), Y0+px(190), Y0+px(1780)
# istif cizgileri
iy = mbot
n = 0
while iy > mtop:
    ln(mx, iy, mx+px(390), iy, 1.6, '#8a6a3a')
    iy -= 9; n += 1
rc(mx-6, mtop-6, px(390)+12, mbot-mtop+12, 1.4, '#555', dash='4,3')

# --- SAG kolon ---
tx(X0+GW, Y0-8, 'KATLAMA BÖLGESİ', 12.5, '#1a1a1a', 'bold', 'end')
# vakum kolu: istif ustunden kaliba
vy = Y0+px(120)
ci(X0+px(160), vy, 7, 1.8, '#2a6a9a'); ci(X0+px(260), vy, 7, 1.8, '#2a6a9a')
ln(X0+px(160), vy-7, X0+px(260), vy-7, 1.6, '#2a6a9a')
arrow(X0+px(300), vy-14, XM+px(140), vy-14, 2, '#2a6a9a')
tx(X0+px(300), vy-24, 'vakum kolu en üst yaprağı kalıba taşır', 11.5, '#2a6a9a')
# kalip + piston (sag ust)
kx, ky = XM+px(60), Y0+px(300)
arrow(kx+px(140), ky-px(120), kx+px(140), ky-px(30), 2.6, '#b3452b')
tx(kx+px(150), ky-px(70), 'piston', 12.5, '#b3452b', 'bold')
ln(kx, ky, kx+px(60), ky+px(90), 2.2)
ln(kx+px(60), ky+px(90), kx+px(220), ky+px(90), 2.2)
ln(kx+px(220), ky+px(90), kx+px(280), ky, 2.2)
ln(kx-px(30), ky, kx, ky, 2.2); ln(kx+px(280), ky, kx+px(310), ky, 2.2)
tx(kx+px(140), ky+px(140), 'eğimli kalıp', 11, '#555', 'normal', 'middle')
tx(kx+px(140), ky+px(185), 'tek hamlede kilitlenir', 10.5, '#555', 'normal', 'middle')
# cikis rafi
cy_ = Y0+px(950)
rc(XM+px(40), cy_, px(330), px(160), 1.8)
rc(XM+px(70), cy_+px(35), px(270), px(90), 1.6, '#8a6a3a')
tx(XM+px(210), cy_+px(210), 'HAZIR KUTU RAFI (2-3 tampon)', 11, '#333', 'normal', 'middle')
arrow(kx+px(140), ky+px(220), XM+px(200), cy_-px(20), 2, '#b3452b')
# robot cikis oku
arrow(XM+px(370), cy_+px(80), X0+GW+30, cy_+px(80), 2.4, '#1d7a4f')
tx(X0+GW+36, cy_+px(80)+4, 'robot kol alır →', 12.5, '#1d7a4f', 'bold')
tx(X0+GW+36, cy_+px(80)+22, 'kesim/servis', 11.5, '#1d7a4f')
# alt: teknik bolme
ty_ = Y0+px(1450)
ln(XM, ty_, X0+GW, ty_, 1.6, '#1a1a1a', dash='7,5')
tx(XM+px(200), ty_+px(90), 'TEKNİK BÖLME', 12.5, '#333', 'bold', 'middle')
tx(XM+px(200), ty_+px(150), 'vakum pompası + 24V', 10.5, '#666', 'normal', 'middle')
tx(XM+px(200), ty_+px(205), 'PLC: "1 kutu kur"', 10.5, '#666', 'normal', 'middle')

# olculer
ox(Y0+GH+AYAK+26, X0, X0+GW, '≈ 85 cm (esnek 70-100)')
oy(X0+GW+14, Y0, Y0+GH, '185')
oy(X0-16, Y0, Y0+GH+AYAK, '197', side='l')
tx(X0, Y0+GH+AYAK+52, 'Derinlik 84 cm (hat standardı) · ayak 12 cm (robot süpürge geçer) · iç: magazin 45 + mekanizma 40', 12, '#666')
tx(X0, Y0+GH+AYAK+70, 'Magazin: 560 blank ≈ 170 cm = HAFTALIK stok · blank yatay yatar (41 × 78 derinlemesine) · yaylı taban istifi yukarı iter', 12, '#666')

# sag not sutunu
NX = 760
tx(NX, 110, 'İSTEK ÖZETİ / REQUEST:', 15, '#1a1a1a', 'bold')
notlar = [
 ('· Kapasite: haftada ~560 kutu', '#1a1a1a', 13, 'bold'),
 ('  (günde ~80 · tepe saatte ~12)', '#555', 12.5, 'normal'),
 ('· SÜREKLİ ÇALIŞMAZ — komut', '#1a1a1a', 13, 'bold'),
 ('  gelince TEK kutu kurar', '#1a1a1a', 13, 'bold'),
 ('· Sanayi tipi hat makinesi', '#1a1a1a', 13, 'normal'),
 ('  DEĞİL — basit, az bakımlı', '#1a1a1a', 13, 'normal'),
 ('· Kutu: standart pizza kutusu', '#1a1a1a', 13, 'normal'),
 ('  ≈ 32 × 32 × 4,5 cm', '#1a1a1a', 13, 'normal'),
 ('· Kutu tasarımı (kendinden', '#555', 12.5, 'normal'),
 ('  kilitli vb.) önerinize açık', '#555', 12.5, 'normal'),
 ('· Tetikleme: PLC/24V sinyal', '#1a1a1a', 13, 'normal'),
 ('· Ölçüler esnek — yerleşim', '#555', 12.5, 'normal'),
 ('  öneriniz değerlidir', '#555', 12.5, 'normal'),
 ('· Daha basit alternatif çözüm', '#1d7a4f', 13, 'bold'),
 ('  öneriniz varsa DİNLERİZ', '#1d7a4f', 13, 'bold'),
]
ny_ = 140
for s, c, sz, w_ in notlar:
    tx(NX, ny_, s, sz, c, w_)
    ny_ += 22
tx(NX, ny_+18, 'EN: erects ONE box on signal;', 11.5, '#888')
tx(NX, ny_+34, 'not an industrial line machine;', 11.5, '#888')
tx(NX, ny_+50, '~560 boxes/week, flat magazine,', 11.5, '#888')
tx(NX, ny_+66, 'fits a ~85 cm cabinet (flexible),', 11.5, '#888')
tx(NX, ny_+82, 'simpler alternatives welcome.', 11.5, '#888')

tx(W-30, H-16, 'AUTOKITCH · kutu_istasyonu_teknik_v1', 11, '#999', anchor='end')

svg = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d"><rect width="%d" height="%d" fill="#ffffff"/>%s</svg>' % (W,H,W,H,W,H,''.join(parts))
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\kutu_istasyonu_teknik_v1.svg"
io.open(out,'w',encoding='utf-8').write(svg)
print('ok', out)
