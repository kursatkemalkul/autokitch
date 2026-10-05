# -*- coding: utf-8 -*-
# v33 — KARSILIKLI PLAN, 3 GUNLUK VERSIYON (soguk depo 140, v29 ic duzeni)
import io, math

S = 0.26
def px(mm): return mm*S
W, H = 900, 980
parts = []
def ln(x1,y1,x2,y2,w=2,c='#1a1a1a',dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.1f"%s/>' % (x1,y1,x2,y2,c,w,d))
def rc(x,y,w,h,sw=2,c='#1a1a1a',fill='none',dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    parts.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" stroke="%s" stroke-width="%.1f" fill="%s"%s/>' % (x,y,w,h,c,sw,fill,d))
def tx(x,y,s,size=14,c='#1a1a1a',w='normal',anchor='start'):
    parts.append('<text x="%.1f" y="%.1f" font-family="Arial" font-size="%.1f" fill="%s" font-weight="%s" text-anchor="%s">%s</text>' % (x,y,size,c,w,anchor,s))
def ci(cx,cy,r,sw=2,c='#1a1a1a',fill='none',dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    parts.append('<circle cx="%.1f" cy="%.1f" r="%.1f" stroke="%s" stroke-width="%.1f" fill="%s"%s/>' % (cx,cy,r,c,sw,fill,d))
def oy(x,y1,y2,label,side='r'):
    ln(x,y1,x,y2,1.2,'#b3452b'); ln(x-5,y1,x+5,y1,1.2,'#b3452b'); ln(x-5,y2,x+5,y2,1.2,'#b3452b')
    if side=='r': tx(x+8,(y1+y2)/2+4,label,12,'#b3452b','bold')
    else: tx(x-8,(y1+y2)/2+4,label,12,'#b3452b','bold','end')
def ox(y,x1,x2,label):
    ln(x1,y,x2,y,1.2,'#b3452b'); ln(x1,y-5,x1,y+5,1.2,'#b3452b'); ln(x2,y-5,x2,y+5,1.2,'#b3452b')
    tx((x1+x2)/2,y+15,label,12,'#b3452b','bold',anchor='middle')
def arrow(x1,y1,x2,y2,w=2,c='#1d7a4f',dash=None):
    ln(x1,y1,x2,y2,w,c,dash)
    a = math.atan2(y2-y1,x2-x1)
    for da in (2.6,-2.6):
        ln(x2,y2,x2-9*math.cos(a+da),y2-9*math.sin(a+da),w,c)
def num(cx,cy,n):
    ci(cx,cy,11,1.8,'#1d7a4f','#ffffff')
    tx(cx,cy+4.5,str(n),12.5,'#1d7a4f','bold','middle')

tx(30,36,'v33 — KARŞILIKLI PLAN — 3 GÜNLÜK VERSİYON (üstten görünüş)',21,'#1a1a1a','bold')
tx(30,58,'Haftalık v32 ile aynı diziliş; tek fark SOĞUK DEPO 210 → 140 (2 kapı, 3 günlük stok — v29 iç düzeni). Lojistik: haftada 2-3 teslimat.',11.5,'#666')
ln(30,70,W-30,70,1,'#999')

X0, Y0 = 100, 120
# bantlar: ust sira y 0-840 · koridor 840-1790 (95) · alt sira 1790-2630
yU0, yU1 = Y0, Y0+px(840)
yK0, yK1 = yU1, yU1+px(950)
yA0, yA1 = yK1, yK1+px(840)
# x: QR 0-550 · sonra kabinler 550-3350
xQ0, xQ1 = X0, X0+px(550)
xS0, xS1 = xQ1, xQ1+px(1400)   # soguk depo 140
xP1 = xS1+px(700)              # pres
# alt sira sagdan: DOZAJ 2650-3350, FIRIN 2000-2650, KESIM 1300-2000, (bosluk/servis 550-1250)
xD0 = xQ1+px(1400); xD1 = xQ1+px(2100)
xF0 = xQ1+px(750); xF1 = xD0
xC0 = xQ1+px(50);  xC1 = xF0

# UST SIRA
rc(xS0,yU0,px(1400),px(840),2.4)
tx((xS0+xS1)/2,yU0+px(390),'1 · SOĞUK DEPO',14,'#1a1a1a','bold','middle')
tx((xS0+xS1)/2,yU0+px(390)+18,'140 · 2 kapı — v29 düzeni',10.5,'#555','normal','middle')
rc(xS1,yU0,px(700),px(840),2.4)
tx((xS1+xP1)/2,yU0+px(360),'2 · PRES',13.5,'#1a1a1a','bold','middle')
tx((xS1+xP1)/2,yU0+px(360)+16,'70 · PZP-400',10.5,'#555','normal','middle')
tx((xS1+xP1)/2,yU0+px(360)+31,'+ çöp + yedek el',10,'#777','normal','middle')

# ALT SIRA
rc(xD0,yA0,px(700),px(840),2.4)
tx((xD0+xD1)/2,yA0+px(400),'3 · DOZAJ',13.5,'#1a1a1a','bold','middle')
tx((xD0+xD1)/2,yA0+px(400)+16,'70 · hazne 2+1',10.5,'#555','normal','middle')
rc(xF0,yA0,px(550),px(840),2.4)
tx((xF0+xF1)/2,yA0+px(400),'4 · FIRIN',13.5,'#1a1a1a','bold','middle')
tx((xF0+xF1)/2,yA0+px(400)+16,'65 · 2 kat',10.5,'#555','normal','middle')
rc(xC0,yA0,px(700),px(840),2.4)
tx((xC0+xC1)/2,yA0+px(400),'5 · KESİM+KUTU',13.5,'#1a1a1a','bold','middle')
tx((xC0+xC1)/2,yA0+px(400)+16,'70',10.5,'#555','normal','middle')

# QR TESLIM (sol uc, koridor bandi)
rc(xQ0,yK0,px(550),px(950),2.4)
tx((xQ0+xQ1)/2,yK0+px(380),'6 · QR',13.5,'#1a1a1a','bold','middle')
tx((xQ0+xQ1)/2,yK0+px(380)+16,'TESLİM',13.5,'#1a1a1a','bold','middle')
tx((xQ0+xQ1)/2,yK0+px(380)+33,'10-12 ısıtmalı göz',10,'#555','normal','middle')
tx((xQ0+xQ1)/2,yK0+px(380)+47,'arkadan robot doldurur',10,'#555','normal','middle')
arrow(xQ0-8,yK0+px(475),xQ0-46,yK0+px(475),2.2,'#2a6a9a')
tx(xQ0-10,yK0+px(475)+24,'MÜŞTERİ',11,'#2a6a9a','bold','end')
tx(xQ0-10,yK0+px(475)+38,'cephesi',10,'#2a6a9a','normal','end')

# CAM (sag uc)
ln(xD1,yK0,xD1,yK1,4,'#2a6a9a')
tx(xD1+8,(yK0+yK1)/2-4,'CAM',11.5,'#2a6a9a','bold')
tx(xD1+8,(yK0+yK1)/2+12,'izleme',10,'#2a6a9a')

# ROBOT: kisa ray + erisim
ry = (yK0+yK1)/2
rx0, rx1 = xQ1+px(250), xQ1+px(1650)
ln(rx0,ry,rx1,ry,3.5,'#8a2be2')
ci((rx0+rx1)/2,ry,9,2,'#8a2be2','#ffffff')
tx((rx0+rx1)/2,ry-16,'ROBOT — ray 140',11.5,'#8a2be2','bold','middle')
for cx_ in (rx0,rx1):
    ci(cx_,ry,px(1300),1.2,'#8a2be2',dash='5,5')
tx(rx1+px(300),ry+px(680),'erişim R130',10,'#8a2be2','normal','middle')

# AKIS OKLARI
num((xS0+xS1)/2,yU0+px(180),1)
num((xS1+xP1)/2,yU0+px(180),2)
num((xD0+xD1)/2,yA0+px(660),3)
num((xF0+xF1)/2,yA0+px(660),4)
num((xC0+xC1)/2,yA0+px(660),5)
num((xQ0+xQ1)/2,yK0+px(160),6)
arrow((xS0+xS1)/2+px(180),yU0+px(180),(xS1+xP1)/2-px(120),yU0+px(180),1.8,'#1d7a4f',dash='4,3')
arrow((xS1+xP1)/2+px(60),yU0+px(700),(xD0+xD1)/2+px(60),yA0+px(140),1.8,'#1d7a4f',dash='4,3')
arrow((xD0+xD1)/2-px(120),yA0+px(660),(xF0+xF1)/2+px(120),yA0+px(660),1.8,'#1d7a4f',dash='4,3')
arrow((xF0+xF1)/2-px(100),yA0+px(660),(xC0+xC1)/2+px(130),yA0+px(660),1.8,'#1d7a4f',dash='4,3')
arrow((xC0+xC1)/2-px(140),yA0+px(140),(xQ0+xQ1)/2+px(140),yK0+px(700),1.8,'#1d7a4f',dash='4,3')

# OLCULER
ox(yU0-22,xS0,xS1,'140')
ox(yU0-22,xS1,xP1,'70')
ox(yA1+24,xC0,xF0,'70')
ox(yA1+24,xF0,xD0,'65')
ox(yA1+24,xD0,xD1,'70')
ox(yA1+58,xQ0,xD1,'TOPLAM UZUNLUK ≈ 265')
oy(xD1+px(320),yU0,yU1,'84')
oy(xD1+px(320),yK0,yK1,'95')
oy(xD1+px(320),yA0,yA1,'84')
oy(xQ0-46,yU0,yA1,'263',side='l')

# ALT NOTLAR
ny = yA1+92
ln(30,ny-14,W-30,ny-14,1,'#999')
tx(30,ny+6,'AYAK İZİ: ≈ 2,65 × 2,65 m ≈ 7,0 m² KARE BLOK (haftalık v32: 3,35 × 2,65 ≈ 8,9 m²)',12.5,'#1a1a1a','bold')
tx(30,ny+26,'· Soğuk depo 140 · 2 kapı · 2 soğutma grubu (haftalıkta 210 · 3 kapı · 3 grup) — kasa daha ucuz',11.5,'#333')
tx(30,ny+44,'· Stok: top 240 = 3 gün · içecek/tatlı 3 günlük · kutu 240 — LOJİSTİK: fırıncı 3 günde bir + haftalık kalemler = haftada 2-3 ziyaret',11.5,'#333')
tx(30,ny+62,'· Servis istasyonu 70 ayrı duvarda (blok içinde boşluk kalmıyor); ray 140, koridor 95, akış v32 ile aynı',11.5,'#333')
tx(W-30,H-14,'AUTOKITCH · hat_plan_karsilikli_3gun_v33',10.5,'#999','normal','end')

svg = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d"><rect width="%d" height="%d" fill="#ffffff"/>%s</svg>' % (W,H,W,H,W,H,''.join(parts))
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\hat_plan_karsilikli_3gun_v33.svg"
io.open(out,'w',encoding='utf-8').write(svg)
print('ok', out)
