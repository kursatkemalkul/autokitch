# -*- coding: utf-8 -*-
# IST.2 PRESS v8 (Kemal, 4 Eyl): ust bolge ortadan ikiye — SOL yari kucuk cop kovasi 30 L + ustunde 14 cm bosluk (huni YOK, cekmece YOK;
# robot kolu girer, ceviririr, bosaltir) · SAG yari BOS (simdilik) · altta yatay bantlar: uc yuvalari (14) + tepsi rafi 2 yan yana (8) · PZP zeminde
import io, math

E = []
def ln(x1,y1,x2,y2,w=1.4,c='#111',dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    E.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s/>' % (x1,y1,x2,y2,c,w,d))
def rc(x,y,w_,h,sw=1.4,rx=0,c='#111',dash=None,fill='none'):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    E.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,w_,h,rx,fill,c,sw,d))
def ci(cx,cy,r,sw=1.4,c='#111',dash=None,fill='none'):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    E.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (cx,cy,r,fill,c,sw,d))
def el(cx,cy,rx,ry,sw=1.4,c='#111',dash=None,fill='none'):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    E.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (cx,cy,rx,ry,fill,c,sw,d))
def tx(x,y,s,fs=11,a='middle',w='',col='#111'):
    fw = ' font-weight="%s"' % w if w else ''
    E.append('<text x="%.1f" y="%.1f" text-anchor="%s" font-size="%s" fill="%s" font-family="Arial"%s>%s</text>' % (x,y,a,fs,col,fw,s))
def not_(x,y,s,a='middle',c='#555',fs=10): tx(x,y,s,fs,a,'',c)
def oy(x1,x2,y,cm):
    ln(x1,y,x2,y,1,'#b3452b'); ln(x1,y-5,x1,y+5,1,'#b3452b'); ln(x2,y-5,x2,y+5,1,'#b3452b')
    tx((x1+x2)/2,y-6,cm,11,'middle','bold','#b3452b')
def ox(x,y1,y2,cm,side='l'):
    ln(x,y1,x,y2,1,'#b3452b'); ln(x-5,y1,x+5,y1,1,'#b3452b'); ln(x-5,y2,x+5,y2,1,'#b3452b')
    xx = x-9 if side=='l' else x+9
    E.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#b3452b" font-family="Arial" transform="rotate(-90 %.1f %.1f)">%s</text>' % (xx,(y1+y2)/2,xx,(y1+y2)/2,cm))
def arr(x1,y1,x2,y2,w=1.6,c='#1d7a4f'):
    ln(x1,y1,x2,y2,w,c); a = math.atan2(y2-y1,x2-x1)
    for da in (2.6,-2.6): ln(x2,y2,x2-8*math.cos(a+da),y2-8*math.sin(a+da),w,c)

W, H = 1560, 1180
S = 0.46
def px(mm): return mm*S
X0, Y0 = 120, 150
GW, GH, AYAK, DER = 700, 1850, 120, 840
YT = Y0+px(GH); YZ = YT+px(AYAK)
Bl, G, Rd = '#1a49b8', '#1d7a4f', '#b3452b'
tx(40,44,'İSTASYON 2 — PRESS · DETAY v8 (üst bölge ikiye: sol küçük çöp kovası + 14 cm kol boşluğu · sağ BOŞ · altta yatay bantlar: uçlar + 2 tepsi · PZP zeminde)',17,'start','bold')
tx(40,68,'Kemal: "huniye gerek yok, çekmece yok — üstünde sadece kolun girip çevirip boşaltacağı kadar boşluk (topping/yağdaki gibi 14); ortadan ikiye böl, sol küçük kova, sağ şimdilik boş." Kabin 70 × 197 × 84 aynı.',10.5,'start','','#555')

# ================= ON GORUNUS =================
tx(X0+px(GW)/2,Y0-18,'ÖN GÖRÜNÜŞ (robot tarafı — cephe açık)',12.5,'middle','bold')
rc(X0,Y0,px(GW),px(GH),2.2,5)
rc(X0+12,YT,12,px(AYAK)); rc(X0+px(GW)-24,YT,12,px(AYAK)); ln(X0-40,YZ,X0+px(GW)+40,YZ,2)
# PZP zeminde
rc(X0+px(15),Y0+px(900),px(670),px(950),1.8,3)
tx(X0+px(350),Y0+px(960),'FERSAH PZP-400 (zeminde — 170 kg · 64×80×95)',10.5,'middle','bold')
rc(X0+px(220),Y0+px(1010),px(260),px(110),1.4,3); ln(X0+px(350),Y0+px(1120),X0+px(350),Y0+px(1200),1.6); rc(X0+px(205),Y0+px(1200),px(290),px(40),1.4,2)
not_(X0+px(350),Y0+px(1280),'ısıtmalı ÜST PLAKA Ø29 (Fersah\'a soru) · UN YOK',c=Rd,fs=9)
el(X0+px(350),Y0+px(1385),px(170),px(20),1.8,Bl); el(X0+px(350),Y0+px(1378),px(140),px(9),1,'#8a6a3a')
ln(X0+px(520),Y0+px(1382),X0+px(640),Y0+px(1382),2,Bl); ln(X0+px(520),Y0+px(1392),X0+px(640),Y0+px(1392),2,Bl)
rc(X0+px(150),Y0+px(1405),px(400),px(25),1.4,2)
tx(X0+px(350),Y0+px(1355),'TEPSİ Ø34 alt plakada bekler · pençe topu koyar · press tepsi İÇİNDE basar',9,'middle','',Bl)
not_(X0+px(350),Y0+px(1465),'alt plaka (ısıtmalı) — zeminden ~90',fs=8.5)
rc(X0+px(80),Y0+px(1520),px(540),px(290),1.2,3); not_(X0+px(350),Y0+px(1675),'motor + rezistans gövdesi · 3,5 kW · 220 V',fs=9)
# bant 1: tepsi rafi 805-885
ln(X0+px(15),Y0+px(800),X0+px(685),Y0+px(800),1.1,'#111','6,5')
tx(X0+px(350),Y0+px(822),'TEPSİ RAFI — 2 yan yana (+1 kolda = 3 tepsi) · 8 cm',9,'middle','bold',Bl)
for i in range(2):
    cx_ = X0+px(180+i*340)
    rc(cx_-px(174),Y0+px(846),px(16),px(16),1,1); rc(cx_+px(158),Y0+px(846),px(16),px(16),1,1)
    el(cx_,Y0+px(854),px(165),px(10),1.4,Bl); rc(cx_-px(14),Y0+px(848),px(28),px(12),.9,1,Bl,None,'#dfe7fb')
# bant 2: uc yuvalari yatay 655-795
ln(X0+px(15),Y0+px(650),X0+px(685),Y0+px(650),1.1,'#111','6,5')
tx(X0+px(350),Y0+px(672),'UÇ YUVALARI — yatay, yan yana · 14 cm',9,'middle','bold')
for k,(ad,dash) in enumerate((('PENÇE',None),('YEDEK PENÇE',None),('boş',' 4,3'))):
    x_ = X0+px(30+k*225)
    rc(x_,Y0+px(685),px(205),px(105),1.3,3,'#999' if dash else '#111',dash)
    if not dash:
        rc(x_+px(60),Y0+px(700),px(85),px(30),1.1,2); ln(x_+px(75),Y0+px(730),x_+px(85),Y0+px(770),1.1); ln(x_+px(130),Y0+px(730),x_+px(120),Y0+px(770),1.1)
    tx(x_+px(102),Y0+px(782),ad,7.5,'middle','bold','#999' if dash else '#111')
not_(X0+px(350),Y0+px(640)-2,'kilit pim+burç · "uç var" sensörü · uç değişimi pide başına ×2',fs=7.5)
# ust bolge 40-640: sol kova + bosluk, sag bos
xB = X0+px(350); ln(xB,Y0+px(40),xB,Y0+px(640),1.1,'#111','6,5')
rc(X0+px(55),Y0+px(190),px(240),px(440),1.8,4)
ln(X0+px(55),Y0+px(240),X0+px(295),Y0+px(240),1); not_(X0+px(175),Y0+px(228),'poşet kelepçesi',fs=7.5)
tx(X0+px(175),Y0+px(420),'ÇÖP KOVASI',10,'middle','bold'); tx(X0+px(175),Y0+px(455),'30 L · Ø30 × 45',9)
not_(X0+px(175),Y0+px(510),'kapaksız · poşetli',fs=8); not_(X0+px(175),Y0+px(545),'öne çekilir, motorsuz',fs=8); not_(X0+px(175),Y0+px(580),'eleman HER GÜN boşaltır',fs=8)
rc(X0+px(30),Y0+px(45),px(290),px(140),1,3,Bl,'5,4')
tx(X0+px(175),Y0+px(100),'KOL BOŞLUĞU 14',9,'middle','bold',Bl); tx(X0+px(175),Y0+px(130),'robot kolu girer, çevirir, boşaltır',7.5,'middle','',Bl); tx(X0+px(175),Y0+px(160),'huni YOK · kapak YOK',7.5,'middle','',Bl)
rc(X0+px(380),Y0+px(45),px(290),px(585),1,4,'#999','5,4')
tx(X0+px(525),Y0+px(320),'BOŞ — şimdilik',10,'middle','bold','#999'); tx(X0+px(525),Y0+px(355),'(35 × 59 × 84)',8.5,'middle','','#999')
# olculer
oy(X0,xB,Y0-2+px(26),'35'); oy(xB,X0+px(GW),Y0-2+px(26),'35')
oy(X0,X0+px(GW),YZ+30,'70 — DEĞİŞMEDİ')
ox(X0-34,Y0,YT,'185'); ox(X0-34,YT,YZ,'12'); ox(X0-70,Y0,YZ,'197')
xr = X0+px(GW)+22
ox(xr,Y0+px(45),Y0+px(185),'boşluk 14',side='r'); ox(xr,Y0+px(190),Y0+px(630),'kova 44',side='r'); ox(xr,Y0+px(655),Y0+px(795),'uçlar 14',side='r'); ox(xr,Y0+px(805),Y0+px(885),'tepsi 8',side='r'); ox(xr,Y0+px(900),Y0+px(1850),'PZP 95',side='r')

# ================= YAN KESIT (sol yari) =================
sx = X0+px(GW)+150
tx(sx+px(DER)/2,Y0-18,'YAN KESİT (sol yarı — kova + kol boşluğu)',12.5,'middle','bold')
rc(sx,Y0,px(DER),px(GH),2.2,5); rc(sx+12,YT,12,px(AYAK)); rc(sx+px(DER)-24,YT,12,px(AYAK)); ln(sx-40,YZ,sx+px(DER)+40,YZ,2)
rc(sx+px(20),Y0+px(900),px(800),px(950),1.6,3); tx(sx+px(420),Y0+px(1000),'PZP-400 · derinlik 80',10,'middle','bold')
el(sx+px(330),Y0+px(1385),px(170),px(20),1.6,Bl); ln(sx+px(160),Y0+px(1380),sx+px(40),Y0+px(1380),2.2,Bl); tx(sx+px(330),Y0+px(1350),'tepsi + kulp (öne)',9,'middle','',Bl)
# tepsi rafi + uc yuvasi yandan
ln(sx+px(160),Y0+px(852),sx+px(500),Y0+px(852),2.6,Bl); rc(sx+px(40),Y0+px(846),px(120),px(6),1.2,1,Bl,None,'#dfe7fb'); tx(sx+px(600),Y0+px(858),'tepsi (kulp öne)',8,'middle','',Bl)
rc(sx+px(40),Y0+px(685),px(300),px(105),1.2,3); tx(sx+px(190),Y0+px(745),'pençe (yatık)',8)
# kova on tarafta + bosluk + kol
rc(sx+px(40),Y0+px(190),px(320),px(440),1.8,4); tx(sx+px(200),Y0+px(420),'KOVA 30 L',9.5,'middle','bold'); tx(sx+px(200),Y0+px(455),'ön tarafta — öne çekilir',8)
rc(sx+px(20),Y0+px(45),px(800),px(140),1,3,Bl,'5,4'); tx(sx+px(420),Y0+px(120),'kol boşluğu 14 — pençe atığı kovanın üstünden bırakır',8,'middle','',Bl)
rc(sx-px(60),Y0+px(60),px(60),px(90),1.3,2,Bl); ln(sx-px(30),Y0+px(60),sx-px(120),Y0+px(20),2,Bl); ln(sx-px(40),Y0+px(150),sx-px(40),Y0+px(175),1.3,Bl); ln(sx-px(20),Y0+px(150),sx-px(20),Y0+px(175),1.3,Bl)
arr(sx-px(30),Y0+px(180),sx+px(120),Y0+px(200),1.4,Bl)
not_(sx+px(600),Y0+px(400),'arkada 48 cm boş',fs=9); not_(sx+px(600),Y0+px(430),'(büyüme)',fs=8.5)
ln(sx,Y0+px(60),sx,Y0+px(1850),3,'#2a6a9a')
E.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="10" fill="#2a6a9a" font-family="Arial" font-weight="bold" transform="rotate(-90 %.1f %.1f)">ROBOT CEPHESİ — AÇIK</text>' % (sx-16,Y0+px(1050),sx-16,Y0+px(1050)))
oy(sx,sx+px(DER),YZ+30,'84'); ox(sx+px(DER)+34,Y0,YZ,'197')

# ================= NOTLAR =================
nx = sx+px(DER)+110
tx(nx,Y0+10,'KARARLAR (v8):',12.5,'start','bold')
nots = [
 ('· KABİN 70 × 84 — değişmedi','bold','#1a1a1a'),
 ('· ÇÖP: huni YOK, çekmece YOK (v7 iptal)','bold','#b3452b'),
 ('  sol yarıda 30 L kova (Ø30×45), kapaksız,','','#333'),
 ('  poşetli; üstünde 14 cm KOL BOŞLUĞU:','','#333'),
 ('  pençe atığı kovanın üstünden bırakır','','#666'),
 ('  (topping/yağ boşluğuyla aynı ölçü)','','#666'),
 ('· Sağ yarı BOŞ — şimdilik (35×59×84)','','#333'),
 ('· Koku: kapaksız kova → eleman HER GÜN','','#333'),
 ('  boşaltır (günde ~1,5 L; 30 L bol)','','#666'),
 ('· Altta yatay bantlar (v7\'den):','','#333'),
 ('  uç yuvaları 14 (pençe · yedek · boş)','','#666'),
 ('  tepsi rafı 8 (2 yan yana + 1 kolda)','','#666'),
 ('· PZP-400 zeminde, tepsi içinde basma;','','#333'),
 ('  üst plaka Ø29 — Fersah\'a soru','','#b3452b'),
 ('· Dikey: 4 + 14 + 44 + 2 + 14 + 1 + 8 + 1','','#333'),
 ('  + 95 = 183 + 2 pay ✓','','#333'),
 ('','',''),
 ('AÇIK:','bold','#b3452b'),
 ('· Kova taşıma: pençe çöpü ne kadar sıkı','','#b3452b'),
 ('  tutar (süresi dolan top) — pilot','','#666'),
 ('· Sağ yarının kullanımı (büyüme)','','#b3452b'),
]
yy = Y0+34
for s_,w_,c_ in nots:
    if s_: tx(nx,yy,s_,10.5,'start',w_,c_)
    yy += 20

tx(W-24,H-14,'AUTOKITCH · ist2_pres_detay_v8',10,'end','','#999')
svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d"><rect width="%d" height="%d" fill="#ffffff"/>%s</svg>' % (W,H,W,H,W,H,''.join(E))
OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\2_PRESS\ist2_pres_detay_v8.svg"
io.open(OUT,'w',encoding='utf-8').write(svg)
print('yazildi:', OUT)
