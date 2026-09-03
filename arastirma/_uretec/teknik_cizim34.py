# -*- coding: utf-8 -*-
# v34 — DUZ HAT (tek yon), 3 GUNLUK VERSIYON — plan gorunusu
import io, math

S = 0.22
def px(mm): return mm*S
W, H = 1240, 700
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

tx(30,36,'v34 — DÜZ HAT (tek yön) — 3 GÜNLÜK VERSİYON (üstten görünüş)',21,'#1a1a1a','bold')
tx(30,58,'Kabinler tek sıra duvar boyunca (soğuk depo 140 · 3 günlük, v29 iç düzeni), önünde robot koridoru + boydan boya CAM şov cephesi.',11.5,'#666')
ln(30,70,W-30,70,1,'#999')

X0, Y0 = 90, 120
yU0, yU1 = Y0, Y0+px(840)          # kabin sirasi (sirt duvara)
yK0, yK1 = yU1, yU1+px(950)        # koridor 95
# kabinler soldan saga
xs = [0,1400,2100,2800,3450,4150]
adlar = [('1 · SOĞUK DEPO','140 · 2 kapı — v29 düzeni'),('2 · PRES','70 · PZP-400 + çöp'),('3 · DOZAJ','70 · hazne 2+1'),('4 · FIRIN','65 · 2 kat'),('5 · KESİM+KUTU','70')]
for i,(ad,alt) in enumerate(adlar):
    x0_, x1_ = X0+px(xs[i]), X0+px(xs[i+1])
    rc(x0_,yU0,x1_-x0_,px(840),2.4)
    tx((x0_+x1_)/2,yU0+px(380),ad,13,'#1a1a1a','bold','middle')
    tx((x0_+x1_)/2,yU0+px(380)+16,alt,10,'#555','normal','middle')
    num((x0_+x1_)/2,yU0+px(680),i+1)
xE = X0+px(4150)
# akis oklari
for i in range(4):
    arrow(X0+px((xs[i]+xs[i+1])/2)+px(150),yU0+px(680),X0+px((xs[i+1]+xs[i+2])/2)-px(150),yU0+px(680),1.8,'#1d7a4f',dash='4,3')

# QR teslim sag ucta koridor bandinda
xQ1 = X0+px(4700)
rc(xE,yK0,px(550),px(950),2.4)
tx((xE+xQ1)/2,yK0+px(360),'6 · QR',13,'#1a1a1a','bold','middle')
tx((xE+xQ1)/2,yK0+px(360)+16,'TESLİM',13,'#1a1a1a','bold','middle')
tx((xE+xQ1)/2,yK0+px(360)+32,'10-12 göz',10,'#555','normal','middle')
num((xE+xQ1)/2,yK0+px(160),6)
arrow(X0+px(3800)+px(150),yU0+px(680),(xE+xQ1)/2,yK0+px(140),1.8,'#1d7a4f',dash='4,3')
arrow(xQ1+8,yK0+px(475),xQ1+46,yK0+px(475),2.2,'#2a6a9a')
tx(xQ1+10,yK0+px(475)+24,'MÜŞTERİ',11,'#2a6a9a','bold')

# CAM: koridorun on uzun kenari
ln(X0,yK1,xE,yK1,4,'#2a6a9a')
tx((X0+xE)/2,yK1+18,'CAM — müşteri robotu BOYDAN BOYA önden izler (4 m şov cephesi)',11.5,'#2a6a9a','bold','middle')

# duvar (kabinlerin sirti)
ln(X0-px(60),yU0-6,xQ1+px(60),yU0-6,5,'#888')
tx(xQ1+px(58),yU0-14,'DUVAR — kesintisiz 4,70 m',10.5,'#888','normal','end')

# robot ray
ry = (yK0+yK1)/2
rx0, rx1 = X0+px(400), X0+px(3700)
ln(rx0,ry,rx1,ry,3.5,'#8a2be2')
ci((rx0+rx1)/2,ry,9,2,'#8a2be2','#ffffff')
tx((rx0+rx1)/2,ry+26,'ROBOT — ray 330',11.5,'#8a2be2','bold','middle')
for cx_ in (rx0,rx1):
    ci(cx_,ry,px(1300),1.2,'#8a2be2',dash='5,5')

# olculer
ox(yU0-30,X0,X0+px(1400),'140')
ox(yU0-30,X0+px(1400),X0+px(2100),'70')
ox(yU0-30,X0+px(2100),X0+px(2800),'70')
ox(yU0-30,X0+px(2800),X0+px(3450),'65')
ox(yU0-30,X0+px(3450),xE,'70')
ox(yK1+44,X0,xQ1,'TOPLAM UZUNLUK ≈ 470')
oy(X0-40,yU0,yU1,'84',side='l')
oy(X0-40,yK0,yK1,'95',side='l')

# alt notlar
ny = yK1+70
ln(30,ny-10,W-30,ny-10,1,'#999')
tx(30,ny+10,'AYAK İZİ: ≈ 4,70 × 1,79 m ≈ 8,4 m² — AMA 4,70 m KESİNTİSİZ DÜZ DUVAR İSTER',12.5,'#1a1a1a','bold')
tx(30,ny+30,'· Stok 3 günlük: top 240 · içecek/tatlı 3G · kutu 240 — lojistik haftada 2-3 ziyaret · servis istasyonu 70 ayrı duvarda',11.5,'#333')
tx(30,ny+48,'· Artısı: boydan boya CAM şov cephesi (müşteri tüm hattı önden izler) · Eksisi: uzun duvar şartı + ray 330 (en pahalı ray)',11.5,'#333')
tx(W-30,H-14,'AUTOKITCH · hat_plan_duz_3gun_v34',10.5,'#999','normal','end')

svg = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d"><rect width="%d" height="%d" fill="#ffffff"/>%s</svg>' % (W,H,W,H,W,H,''.join(parts))
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\hat_plan_duz_3gun_v34.svg"
io.open(out,'w',encoding='utf-8').write(svg)
print('ok', out)
