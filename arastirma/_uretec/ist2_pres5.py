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
tx(40,44,'İSTASYON 2 — PRESS · DETAY v5 (tepsi rafı YATAY: 8 yuva · pençe yuvası · çöp · PZP-400 zeminde · tepsi içinde basma)',17,'start','bold')
tx(40,68,'Kemal: "tepsi ucu dikey cebe sığmaz — yatayda kurgula." Ø34 + kulp 12 = 46 cm, kabin derinliği 84 → yatay raf sığıyor; sol 36 = pençe yuvası + 8 tepsi (pitch 5) · sağ 34 = huni + 30 L kova · genişlik 70 DEĞİŞMEDİ',10.5,'start','','#555')

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

# --- UST BOLGE y 50-880: sol TEPSI RAFI + PENCE (0-360) / sag COP (360-700)
xB = X0+px(360)
ln(xB,Y0+px(50),xB,Y0+px(890),1.1,'#111','6,5')
# PENCE YUVASI
rc(X0+px(30),Y0+px(70),px(300),px(190),1.5,4)
tx(X0+px(180),Y0+px(105),'PENÇE YUVASI',10,'middle','bold')
rc(X0+px(130),Y0+px(125),px(100),px(40),1.2,2)
ln(X0+px(145),Y0+px(165),X0+px(160),Y0+px(230),1.3); ln(X0+px(215),Y0+px(165),X0+px(200),Y0+px(230),1.3)
not_(X0+px(180),Y0+px(250),'kilit pim+burç · "uç var" sensörü',fs=8)
# TEPSI RAFI — 8 yatay yuva
tx(X0+px(180),Y0+px(310),'TEPSİ RAFI — 8 YATAY YUVA',10,'middle','bold',Bl)
for i in range(8):
    yy = Y0+px(345+i*50)
    rc(X0+px(28),yy-px(7),px(18),px(14),1,1); rc(X0+px(314),yy-px(7),px(18),px(14),1,1)      # yan raylar
    el(X0+px(180),yy,px(165),px(10),1.4,Bl)
    rc(X0+px(166),yy-px(6),px(28),px(12),.9,1,Bl,None,'#dfe7fb')                                 # kulp ucu (robota bakar)
    tx(X0+px(348),yy+3,str(i+1),7,'start','','#999')
not_(X0+px(180),Y0+px(770),'pitch 5 cm · kulp ÖNE (robota) · kilit üstten oturur, 1 cm kaldır-çek',fs=8)
not_(X0+px(180),Y0+px(805),'BEYİN her yuvanın saatini bilir → en uzun soğuyanı alır',fs=8)
not_(X0+px(180),Y0+px(840),'gün sonu eleman 8 tepsiyi yıkar (bulaşık 60×60)',fs=8)
not_(X0+px(180),Y0+px(872),'8 = fırında 2 + kolda 1 + soğuyan 5',c='#1d7a4f',fs=8)
# COP
tx(X0+px(530),Y0+px(105),'ÇÖP',10,'middle','bold')
ln(X0+px(385),Y0+px(150),X0+px(450),Y0+px(320),1.6); ln(X0+px(675),Y0+px(150),X0+px(610),Y0+px(320),1.6); ln(X0+px(385),Y0+px(150),X0+px(675),Y0+px(150),1.6)
not_(X0+px(530),Y0+px(132),'huni ağzı — robot bırakır, durmaz',fs=8)
ln(X0+px(450),Y0+px(320),X0+px(450),Y0+px(360),1.2); ln(X0+px(610),Y0+px(320),X0+px(610),Y0+px(360),1.2)
rc(X0+px(415),Y0+px(370),px(230),px(480),1.6,4)
ln(X0+px(415),Y0+px(420),X0+px(645),Y0+px(420),1)
not_(X0+px(530),Y0+px(405),'poşet kelepçesi',fs=8)
tx(X0+px(530),Y0+px(600),'KOVA 30 L',10,'middle','bold')
not_(X0+px(530),Y0+px(660),'Ø30 · bel hizasında',fs=8)
not_(X0+px(530),Y0+px(700),'öne çekilir, MOTORSUZ',fs=8)
not_(X0+px(530),Y0+px(740),'eleman HER GÜN boşaltır',fs=8)

# olculer
oy(X0,xB,Y0-2+px(26),'36'); oy(xB,X0+px(GW),Y0-2+px(26),'34')
oy(X0,X0+px(GW),YZ+30,'70 — DEĞİŞMEDİ')
ox(X0-34,Y0,YT,'185'); ox(X0-34,YT,YZ,'12'); ox(X0-70,Y0,YZ,'197')
xr = X0+px(GW)+22
ox(xr,Y0+px(70),Y0+px(260),'pençe 19',side='r'); ox(xr,Y0+px(320),Y0+px(720),'tepsi rafı 40',side='r'); ox(xr,Y0+px(900),Y0+px(1850),'PZP 95',side='r')

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
# pence yuvasi (yandan)
rc(sx+px(60),Y0+px(70),px(300),px(190),1.4,4); tx(sx+px(210),Y0+px(175),'pençe',9)
# tepsi rafi yandan: her yuva = tepsi 340 + kulp 120 = 460 derinlik, onden
for i in range(8):
    yy = Y0+px(345+i*50)
    ln(sx+px(160),yy-px(2),sx+px(500),yy-px(2),2.4,Bl)                            # tepsi (yandan cizgi) — arkada
    rc(sx+px(40),yy-px(8),px(120),px(6),1.2,1,Bl,None,'#dfe7fb')                   # kulp ONDE (robot cephesi solda)
    ln(sx+px(505),yy-px(18),sx+px(505),yy+px(12),1,'#999')                          # arka ray
ln(sx,Y0+px(60),sx,Y0+px(1850),3,'#2a6a9a')
E.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="10" fill="#2a6a9a" font-family="Arial" font-weight="bold" transform="rotate(-90 %.1f %.1f)">ROBOT CEPHESİ — AÇIK</text>' % (sx-16,Y0+px(1050),sx-16,Y0+px(1050)))
oy(sx+px(40),sx+px(40)+px(460),Y0+px(320),'46 (tepsi 34 + kulp 12)')
not_(sx+px(650),Y0+px(540),'arkada 38 cm boş',fs=9)
not_(sx+px(650),Y0+px(570),'(büyüme / ikinci sıra)',fs=8.5)
oy(sx,sx+px(DER),YZ+30,'84')
ox(sx+px(DER)+34,Y0,YZ,'197')
# kilit hareketi oku (yuva 1)
yy1 = Y0+px(345)
E.append('<path d="M %.1f %.1f L %.1f %.1f L %.1f %.1f" fill="none" stroke="#1d7a4f" stroke-width="1.6" stroke-dasharray="4,3"/>' % (sx+px(100),yy1-px(60),sx+px(100),yy1-px(14),sx-px(30),yy1-px(14)))
tx(sx+px(120),yy1-px(70),'kilit kulba iner → 1 cm kaldırır → öne çeker',8.5,'start','','#1d7a4f')

# ================= NOTLAR =================
nx = sx+px(DER)+110
tx(nx,Y0+10,'KARARLAR (v5):',12.5,'start','bold')
nots = [
 ('· KABİN 70 · derinlik 84 — değişmedi','bold','#1a1a1a'),
 ('· Uç cepleri DİKEY → tepsi sığmıyordu','','#b3452b'),
 ('  (Ø34 + kulp 12 = 46 > 33 cm cep)','','#b3452b'),
 ('· Çözüm: TEPSİ RAFI YATAY — 8 yuva,','','#333'),
 ('  pitch 5 cm = 40 cm; kulp robota bakar','','#666'),
 ('· Derinlik 46 &lt; 84: sığar, arkada 38 boş','','#1d7a4f'),
 ('· ⑥ tepsi havuzu ÇÖZÜLDÜ: 8 tepsi burada','','#1d7a4f'),
 ('  (fırında 2 + kolda 1 + soğuyan 5)','','#666'),
 ('· Sıcak tepsi (150 °C) alta girer, BEYİN','','#333'),
 ('  en uzun soğuyanı verir (saat damgası)','','#666'),
 ('· Yıkama gün sonu — eleman, 8 tepsi','','#333'),
 ('· PENÇE yuvası üstte (19 cm), kilit pim+burç','','#333'),
 ('· Uç değişimi pide başına ×2 (~8 sn)','','#666'),
 ('· ÇÖP: sağ 34 — huni + 30 L kova, motorsuz','','#333'),
 ('· PZP-400 zeminde, tepsi içinde basma;','','#333'),
 ('  üst plaka Ø29 — Fersah\'a soru','','#b3452b'),
]
yy = Y0+34
for s_,w_,c_ in nots:
    tx(nx,yy,s_,10.5,'start',w_,c_)
    yy += 20

tx(W-24,H-14,'AUTOKITCH · ist2_pres_detay_v5',10,'end','','#999')
svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d"><rect width="%d" height="%d" fill="#ffffff"/>%s</svg>' % (W,H,W,H,W,H,''.join(E))
OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\2_PRESS\ist2_pres_detay_v5.svg"
io.open(OUT,'w',encoding='utf-8').write(svg)
print('yazildi:', OUT)
