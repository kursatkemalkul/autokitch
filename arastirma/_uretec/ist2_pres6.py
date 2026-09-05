# -*- coding: utf-8 -*-
# IST.2 PRESS v5 — TEPSI RAFI YATAY (Kemal, 4 Eyl): Ø34 + kulp 12 = 46 cm tepsi dikey cebe sigmaz ->
# sol 36 cm: PENCE yuvasi + 8 YATAY tepsi yuvasi (pitch 5, kulp robota bakar, kilit ustten) · sag 34 cm: cop huni + 30 L kova
# PZP-400 zeminde (v4 aynen). Tepsi icinde basma. Yan kesit: raf derinligi 46 < 84.
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

W, H = 1560, 1180
S = 0.46
def px(mm): return mm*S
X0, Y0 = 120, 150
GW, GH, AYAK, DER = 700, 1850, 120, 840
YT = Y0+px(GH); YZ = YT+px(AYAK)
Bl = '#1a49b8'
tx(40,44,'İSTASYON 2 — PRESS · DETAY v6 (3 tepsi: yatay raf 2 yan yana · üstünde çöp + 3 uç yuvası · PZP-400 zeminde · tepsi içinde basma)',17,'start','bold')
tx(40,68,'Kemal: "1-2 tepsi yeter, yatay kur, üstüne çöpü koy." 3 tepsi = fırında 2 + kolda 1 (press plakası ısıtmalı → soğuma beklemez). Alt bant 8 cm: 2 tepsi yan yana (kulp öne) · üstte sol huni + 30 L kova, sağ 3 uç yuvası · 70 × 84 DEĞİŞMEDİ',10.5,'start','','#555')

# ================= ON GORUNUS =================
tx(X0+px(GW)/2,Y0-18,'ÖN GÖRÜNÜŞ (robot tarafı — cephe açık)',12.5,'middle','bold')
rc(X0,Y0,px(GW),px(GH),2.2,5)
rc(X0+12,YT,12,px(AYAK)); rc(X0+px(GW)-24,YT,12,px(AYAK))
ln(X0-40,YZ,X0+px(GW)+40,YZ,2)

# --- PZP-400 zeminde (y 900-1850)
rc(X0+px(15),Y0+px(900),px(670),px(950),1.8,3)
tx(X0+px(350),Y0+px(960),'FERSAH PZP-400 (zeminde — 170 kg · 64×80×95)',10.5,'middle','bold')
rc(X0+px(220),Y0+px(1010),px(260),px(110),1.4,3)
ln(X0+px(350),Y0+px(1120),X0+px(350),Y0+px(1200),1.6)
rc(X0+px(205),Y0+px(1200),px(290),px(40),1.4,2)
not_(X0+px(350),Y0+px(1280),'ısıtmalı ÜST PLAKA Ø29 (Ø40 → Ø29: tepsi bordürüne çarpmaz — Fersah\'a soru) · UN YOK',c='#b3452b',fs=9)
el(X0+px(350),Y0+px(1385),px(170),px(20),1.8,Bl); el(X0+px(350),Y0+px(1378),px(140),px(9),1,'#8a6a3a')
ln(X0+px(520),Y0+px(1382),X0+px(640),Y0+px(1382),2,Bl); ln(X0+px(520),Y0+px(1392),X0+px(640),Y0+px(1392),2,Bl)
rc(X0+px(150),Y0+px(1405),px(400),px(25),1.4,2)
tx(X0+px(350),Y0+px(1355),'TEPSİ Ø34 alt plakada bekler · pençe topu koyar · press tepsi İÇİNDE basar',9,'middle','',Bl)
not_(X0+px(350),Y0+px(1465),'alt plaka (ısıtmalı) — zeminden ~90 · kulp robota (sağda gösterildi)',fs=8.5)
rc(X0+px(80),Y0+px(1520),px(540),px(290),1.2,3)
not_(X0+px(350),Y0+px(1675),'motor + rezistans gövdesi · 3,5 kW · 220 V',fs=9)

# --- UST BOLGE y 50-890: sol HUNI+KOVA (x 20-360) · sag 3 UC YUVASI (x 380-680) · alt bant y 805-890 TEPSI RAFI (2 yan yana)
xB = X0+px(370)
ln(xB,Y0+px(50),xB,Y0+px(795),1.1,'#111','6,5')
ln(X0+px(15),Y0+px(800),X0+px(685),Y0+px(800),1.1,'#111','6,5')
# COP (sol)
tx(X0+px(190),Y0+px(95),'ÇÖP',10,'middle','bold')
ln(X0+px(40),Y0+px(120),X0+px(110),Y0+px(300),1.6); ln(X0+px(340),Y0+px(120),X0+px(270),Y0+px(300),1.6); ln(X0+px(40),Y0+px(120),X0+px(340),Y0+px(120),1.6)
not_(X0+px(190),Y0+px(200),'huni ağzı — robot bırakır, durmaz',fs=8)
ln(X0+px(110),Y0+px(300),X0+px(110),Y0+px(330),1.2); ln(X0+px(270),Y0+px(300),X0+px(270),Y0+px(330),1.2)
rc(X0+px(75),Y0+px(340),px(230),px(440),1.6,4)
ln(X0+px(75),Y0+px(390),X0+px(305),Y0+px(390),1); not_(X0+px(190),Y0+px(376),'poşet kelepçesi',fs=7.5)
tx(X0+px(190),Y0+px(560),'KOVA 30 L',10,'middle','bold')
not_(X0+px(190),Y0+px(620),'Ø30 · göğüs hizasında',fs=8)
not_(X0+px(190),Y0+px(660),'öne çekilir, MOTORSUZ',fs=8)
not_(X0+px(190),Y0+px(700),'eleman HER GÜN boşaltır',fs=8)
# 3 UC YUVASI (sag)
for k,(ad,dash) in enumerate((('1 · PENÇE ucu',None),('2 · YEDEK PENÇE',None),('3 · BOŞ (büyüme)','4,3'))):
    y0_ = Y0+px(70+k*245)
    rc(X0+px(390),y0_,px(290),px(220),1.4,4,'#999' if dash else '#111',dash)
    tx(X0+px(535),y0_+px(35),ad,9,'middle','bold','#999' if dash else '#111')
    if k<2:
        rc(X0+px(485),y0_+px(65),px(100),px(40),1.2,2); ln(X0+px(500),y0_+px(105),X0+px(515),y0_+px(175),1.3); ln(X0+px(570),y0_+px(105),X0+px(555),y0_+px(175),1.3)
        not_(X0+px(535),y0_+px(205),'kilit pim+burç · "uç var" sensörü',fs=7)
# TEPSI RAFI yatay — 2 yuva yan yana
tx(X0+px(350),Y0+px(822),'TEPSİ RAFI — YATAY · 2 yuva yan yana (+1 kolda = 3 tepsi)',9.5,'middle','bold',Bl)
for i in range(2):
    cx_ = X0+px(180+i*340)
    rc(cx_-px(174),Y0+px(846),px(16),px(16),1,1); rc(cx_+px(158),Y0+px(846),px(16),px(16),1,1)
    el(cx_,Y0+px(854),px(165),px(10),1.4,Bl); rc(cx_-px(14),Y0+px(848),px(28),px(12),.9,1,Bl,None,'#dfe7fb')
    tx(cx_,Y0+px(882),'yuva %d' % (i+1),7,'middle','','#999')

# olculer
oy(X0,xB,Y0-2+px(26),'37 çöp'); oy(xB,X0+px(GW),Y0-2+px(26),'33 uç')
oy(X0,X0+px(GW),YZ+30,'70 — DEĞİŞMEDİ')
ox(X0-34,Y0,YT,'185'); ox(X0-34,YT,YZ,'12'); ox(X0-70,Y0,YZ,'197')
xr = X0+px(GW)+22
ox(xr,Y0+px(70),Y0+px(780),'çöp + uç yuvaları 71',side='r'); ox(xr,Y0+px(805),Y0+px(890),'tepsi 8',side='r'); ox(xr,Y0+px(900),Y0+px(1850),'PZP 95',side='r')

# ================= YAN KESIT =================
sx = X0+px(GW)+150
tx(sx+px(DER)/2,Y0-18,'YAN KESİT (sol kolon — tepsi rafı)',12.5,'middle','bold')
rc(sx,Y0,px(DER),px(GH),2.2,5)
rc(sx+12,YT,12,px(AYAK)); rc(sx+px(DER)-24,YT,12,px(AYAK))
ln(sx-40,YZ,sx+px(DER)+40,YZ,2)
rc(sx+px(20),Y0+px(900),px(800),px(950),1.6,3)
tx(sx+px(420),Y0+px(1000),'PZP-400 · derinlik 80',10,'middle','bold')
el(sx+px(330),Y0+px(1385),px(170),px(20),1.6,Bl); ln(sx+px(160),Y0+px(1380),sx+px(40),Y0+px(1380),2.2,Bl)
tx(sx+px(330),Y0+px(1350),'tepsi + kulp (öne)',9,'middle','',Bl)
# ust bolge yandan: kova + uc yuvalari (derinlik icinde), altta tepsi rafi tek seviye
rc(sx+px(60),Y0+px(70),px(700),px(710),1.2,4,'#777','5,4'); tx(sx+px(410),Y0+px(400),'çöp kovası / uç yuvaları (derinlik 84 içinde)',9,'middle','','#777')
yy = Y0+px(854)
ln(sx+px(160),yy-px(2),sx+px(500),yy-px(2),2.6,Bl)                                  # tepsi (yandan) — arkada
rc(sx+px(40),yy-px(8),px(120),px(6),1.2,1,Bl,None,'#dfe7fb')                         # kulp ONDE (robot cephesi)
ln(sx+px(505),yy-px(20),sx+px(505),yy+px(14),1,'#999')                                # arka ray
E.append('<path d="M %.1f %.1f L %.1f %.1f L %.1f %.1f" fill="none" stroke="#1d7a4f" stroke-width="1.6" stroke-dasharray="4,3"/>' % (sx+px(100),yy-px(70),sx+px(100),yy-px(14),sx-px(30),yy-px(14)))
tx(sx+px(120),yy-px(80),'kilit kulba iner → 1 cm kaldırır → öne çeker',8.5,'start','','#1d7a4f')
oy(sx+px(40),sx+px(500),yy+px(40),'46 (tepsi 34 + kulp 12)')
not_(sx+px(650),Y0+px(870),'arkada 38 boş',fs=8.5)

ln(sx,Y0+px(60),sx,Y0+px(1850),3,'#2a6a9a')
E.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="10" fill="#2a6a9a" font-family="Arial" font-weight="bold" transform="rotate(-90 %.1f %.1f)">ROBOT CEPHESİ — AÇIK</text>' % (sx-16,Y0+px(1050),sx-16,Y0+px(1050)))
oy(sx,sx+px(DER),YZ+30,'84')
ox(sx+px(DER)+34,Y0,YZ,'197')

# ================= NOTLAR =================
nx = sx+px(DER)+110
tx(nx,Y0+10,'KARARLAR (v6):',12.5,'start','bold')
nots = [
 ('· KABİN 70 · derinlik 84 — değişmedi','bold','#1a1a1a'),
 ('· 8 tepsi GEREKMEZ (Kemal): press plakası','','#b3452b'),
 ('  ısıtmalı → sıcak tepsi hemen kullanılır','','#b3452b'),
 ('· 3 tepsi = fırında 2 + kolda 1 (pik 30/saat)','','#333'),
 ('· Raf YATAY, 2 yuva yan yana, 8 cm bant','','#333'),
 ('  (v5\'teki 8 katlı raf iptal)','','#666'),
 ('· Üstünde: sol huni + 30 L kova (göğüs','','#333'),
 ('  hizası, öne çekilir) · sağ 3 uç yuvası:','','#666'),
 ('  pençe · yedek pençe · boş (büyüme)','','#666'),
 ('· Kilit kulba üstten iner, 1 cm kaldırır,','','#333'),
 ('  öne çeker · kulp robota bakar','','#666'),
 ('· Derinlik 46 &lt; 84: arkada 38 boş','','#1d7a4f'),
 ('· Uç değişimi pide başına ×2 (~8 sn)','','#666'),
 ('· PZP-400 zeminde, tepsi içinde basma;','','#333'),
 ('  üst plaka Ø29 — Fersah\'a soru','','#b3452b'),
]
yy = Y0+34
for s_,w_,c_ in nots:
    tx(nx,yy,s_,10.5,'start',w_,c_)
    yy += 20

tx(W-24,H-14,'AUTOKITCH · ist2_pres_detay_v6',10,'end','','#999')
svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d"><rect width="%d" height="%d" fill="#ffffff"/>%s</svg>' % (W,H,W,H,W,H,''.join(E))
OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\2_PRESS\ist2_pres_detay_v6.svg"
io.open(OUT,'w',encoding='utf-8').write(svg)
print('yazildi:', OUT)
