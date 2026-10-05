# -*- coding: utf-8 -*-
"""HAT v39 — TUM ISTASYONLAR SON VERSIYON (4 Eyl 2026): STORE v38 · PRESS v4 + tepsi icinde basma · TOPPING v8
(teknik bolme ustte, tabla yok, acik dozaj boslugu, gecis rafi) · OVEN tepsiyle · PACK kesim yuvasi + robot eger ·
SERVICE · robot tepsi ucu. Ust gorunum + KONTROL bulgulari (istasyonlar arasi uyumsuzluklar)."""
import io, math

S=0.3
X0,Y0=90,150
HG,HA=1850,120
M=[("1 · STORE — soğuk depo (hamur + içecek + tatlı)",1400),("2 · PRESS",700),("3 · TOPPING",700),("4 · OVEN",650),("5 · PACK",700)]
T=sum(w for _,w in M)
def px(mm): return mm*S
YT=Y0+px(HG); YZ=YT+px(HA)
E=[]
def ln(x1,y1,x2,y2,w=1.4,c="#111",dash=None):
    d=f' stroke-dasharray="{dash}"' if dash else ""
    E.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}/>')
def rc(x,y,w,h,sw=1.4,rx=0,c="#111",dash=None,fill="none"):
    d=f' stroke-dasharray="{dash}"' if dash else ""
    E.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{c}" stroke-width="{sw}"{d}/>')
def ci(cx,cy,r,sw=1.4,c="#111",dash=None,fill="none"):
    d=f' stroke-dasharray="{dash}"' if dash else ""
    E.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{c}" stroke-width="{sw}"{d}/>')
def el(cx,cy,rx,ry,sw=1.4,c="#111",dash=None):
    d=f' stroke-dasharray="{dash}"' if dash else ""
    E.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="none" stroke="{c}" stroke-width="{sw}"{d}/>')
def tx(x,y,s,fs=11,a="middle",w="",col="#111"):
    s=str(s).replace("<","&lt;")
    fw=f' font-weight="{w}"' if w else ""
    E.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{a}" font-size="{fs}" fill="{col}" font-family="Arial"{fw}>{s}</text>')
def oy(x1,x2,y,cm,fs=11):
    ln(x1,y,x2,y,1); ln(x1,y-5,x1,y+5,1); ln(x2,y-5,x2,y+5,1)
    E.append(f'<path d="M {x1:.1f} {y:.1f} l 8 -3 v 6 z" fill="#111"/><path d="M {x2:.1f} {y:.1f} l -8 -3 v 6 z" fill="#111"/>')
    tx((x1+x2)/2,y-6,cm,fs)
def ox(x,y1,y2,cm,fs=11):
    ln(x,y1,x,y2,1); ln(x-5,y1,x+5,y1,1); ln(x-5,y2,x+5,y2,1)
    E.append(f'<path d="M {x:.1f} {y1:.1f} l -3 8 h 6 z" fill="#111"/><path d="M {x:.1f} {y2:.1f} l -3 -8 h 6 z" fill="#111"/>')
    E.append(f'<text x="{x-9:.1f}" y="{(y1+y2)/2:.1f}" text-anchor="middle" font-size="{fs}" fill="#111" font-family="Arial" transform="rotate(-90 {x-9:.1f} {(y1+y2)/2:.1f})">{cm}</text>')
def not_(x,y,s,c="#555",fs=9.5): tx(x,y,s,fs,"middle","",c)
def nk(x,y,s,fs=9): tx(x,y,s,fs,"middle","bold","#b3452b")   # KONTROL bulgusu (kirmizi)
def kaset(x,y,w,h,ad,alt='',dash=None,c='#111',fs=8.5):
    rc(x,y,w,h,1.4,2,c,dash)
    rc(x+w-px(18),y+px(60),px(14),px(70),1,1,c,dash)
    if dash: tx(x+w/2,y-3,ad,7.5,'middle','bold',c)
    else:
        tx(x+w/2,y+h/2+2,ad,fs,'middle','bold',c)
        if alt: tx(x+w/2,y+h/2+14,alt,7.5,'middle','',c)
def tray(cx,cy,r=170,kulp=False,c='#1a49b8'):
    el(cx,cy,px(r),px(18),1.8,c); el(cx,cy-px(6),px(140),px(9),1,'#8a6a3a')
    if kulp: ln(cx+px(r),cy-px(4),cx+px(r+120),cy-px(4),2,c); ln(cx+px(r),cy+px(6),cx+px(r+120),cy+px(6),2,c)

xs=[X0+px(sum(w for _,w in M[:i])) for i in range(6)]
for i,(_ad,_w) in enumerate(M):
    _x=xs[i]
    rc(_x+2,Y0,px(_w)-4,px(HG),2.2,5)
    rc(_x+14,YT,12,px(HA),1.4); rc(_x+px(_w)-26,YT,12,px(HA),1.4)
ln(X0-46,YZ,X0+px(T)+70,YZ,2)

# ================= 1 STORE v4 (alt buzluk 6 cekmece · 19 cekmece x 61 · PU 60/80 · kapak yok) =================
a0,a1=xs[0],xs[1]; am=a0+px(700)
PU='#e9e4d6'
rc(a0+6,Y0+px(20),a1-a0-12,px(280),1.2,2)
for gx,lab in ((350,'−18 grubu 1/3 HP'),(1050,'+3 grubu 1/4 HP')):
    ci(a0+px(gx-60),Y0+px(160),px(55),1.1); rc(a0+px(gx+20),Y0+px(90),px(120),px(150),.9,2); tx(a0+px(gx),Y0+px(278),lab,7,'middle','bold')
not_((a0+a1)/2,Y0+px(58),'SOĞUTMA ×2 — bölme 28, üstten servis',fs=8)
rc(a0+6,Y0+px(300),a1-a0-12,px(60),1,0,'#111',None,PU)
rc(a0+6,Y0+px(300),px(60),px(900),1,0,'#111',None,PU); rc(a1-6-px(60),Y0+px(300),px(60),px(900),1,0,'#111',None,PU)
rc(a0+px(690),Y0+px(360),px(20),px(840),1,0,'#111',None,'#ccc')
rc(a0+6,Y0+px(1200),a1-a0-12,px(80),1,0,'#111',None,PU)
rc(a0+6,Y0+px(1280),px(80),px(570),1,0,'#111',None,PU); rc(a1-6-px(80),Y0+px(1280),px(80),px(570),1,0,'#111',None,PU)
rc(a0+6,Y0+px(1770),a1-a0-12,px(80),1,0,'#111',None,PU)
rc(a0+px(690),Y0+px(1280),px(20),px(490),1,0,'#111',None,'#ccc')
def fr(x,y,w,h,c='#111',fill=PU):
    rc(x,y,w,h,1,1,c,None,fill); ln(x+w/2-10,y+h-4,x+w/2+10,y+h-4,1.5,c)
xl,xr=a0+px(66),a0+px(714); wc=px(624)
for k in range(4):
    y=Y0+px(362)+k*px(130); fr(xl,y,wc,px(124))
    for i in range(7): rc(xl+px(22)+i*px(82),y+px(5),px(66),px(115),.6,2,'#777','3,3')
    tx(xl+wc/2,y+px(68),'İÇECEK %d · 7 kanal' % (k+1),6,'middle','bold')
y1=Y0+px(362)+4*px(130); fr(xl,y1,wc,px(316))
for i in range(5): rc(xl+px(50)+i*px(110),y1+px(50),px(85),px(250),.6,4,'#777','3,3')
tx(xl+wc/2,y1+px(170),'1 L · 5 kanal × 8',6,'middle','bold')
for r in range(8):
    y=Y0+px(362)+r*px(105); fr(xr,y,wc,px(99))
    for i in range(4): el(xr+px(95)+i*px(140),y+px(50),px(45),px(28),.6,'#777','3,3')
    ln(xr+px(30),y+px(60),xr+wc-px(30),y+px(60),.6,'#777','3,3')
    tx(xr+wc/2,y+px(92),'TAZE %d · 20 top' % (r+1),5.5,'middle','bold')
tx(a0+px(700),Y0+px(1252),'YATAY İZOLELİ AYIRICI PU 80',6.5,'middle','bold')
xl2,xr2=a0+px(86),a0+px(714); wc2=px(604)
for k in range(2):
    y=Y0+px(1283)+k*px(100)
    for xx_,nm in ((xl2,k+1),(xr2,k+3)):
        fr(xx_,y,wc2,px(94),'#1a49b8','#dfe7fb')
        for i in range(4): el(xx_+px(92)+i*px(140),y+px(48),px(45),px(26),.6,'#1a49b8','3,3')
        tx(xx_+wc2/2,y+px(88),'DONMUŞ %d · 20 top' % nm,5.5,'middle','bold','#1a49b8')
yk=Y0+px(1483)
for xx_,nm in ((xl2,'KIYMA'),(xr2,'KUŞBAŞI')):
    fr(xx_,yk,wc2,px(284),'#1a49b8','#dfe7fb')
    for i in range(2): rc(xx_+px(30)+i*px(190),yk+px(20),px(160),px(240),.9,2,'#1a49b8',None,'#eef3ff')
    rc(xx_+px(410),yk+px(20),px(160),px(240),.6,2,'#999','3,3')
    tx(xx_+wc2/2,yk+px(275),'TOPPING KABI %s ×2 + boş · 16×54×24 · −18' % nm,5.4,'middle','bold','#1a49b8')
tx((a0+a1)/2,Y0+px(347),'① ✓ STORE v4: 19 çekmece × 61 (kapak yok) · alt −18 6 çekmece · PU 60/80 · içecek 13 / taze 10,5 / donmuş 10',6.5,'middle','bold','#1d7a4f')
a2,a3=am,xs[1]

# ================= 2 PRESS (v4 + tepsi icinde basma) =================
b0,b1=xs[1],xs[2]; bm=(b0+b1)/2
rc(b0+px(15),Y0+px(900),b1-b0-px(30),px(950),1.8,3)
tx(bm,Y0+px(955),"FERSAH PZP-400 (zeminde · 64×80×95 · 170 kg)",8.5,"middle","bold")
rc(bm-px(130),Y0+px(1000),px(260),px(110),1.4,3)
ln(bm,Y0+px(1110),bm,Y0+px(1190),1.6)
rc(bm-px(145),Y0+px(1190),px(290),px(40),1.4,2)
not_(bm,Y0+px(1270),"üst plaka Ø29 ısıtmalı (Ø40 → Ø29: tepsi bordürüne çarpmasın)",fs=8)
tray(bm,Y0+px(1380),kulp=False)
rc(bm-px(200),Y0+px(1398),px(400),px(22),1.4,2)
not_(bm,Y0+px(1345),"TEPSİ Ø34 alt plakada bekler · top tepsiye · press tepsi İÇİNDE basar",fs=8)
not_(bm,Y0+px(1445),"alt plaka (ısıtmalı) · zeminden ~90",fs=8)
rc(b0+px(80),Y0+px(1500),b1-b0-px(160),px(300),1.2,3)
not_(bm,Y0+px(1660),"motor + rezistans · 3,5 kW · 220 V",fs=8)
# ust bolge v8: sol yari kova + 14 kol boslugu · sag yari bos · altta yatay bantlar (uclar 14, tepsi 8)
xB=b0+px(350); ln(xB,Y0+px(40),xB,Y0+px(640),1.1,'#111','6,5')
rc(b0+px(55),Y0+px(190),px(240),px(440),1.6,3); ln(b0+px(55),Y0+px(240),b0+px(295),Y0+px(240),.8)
tx(b0+px(175),Y0+px(420),'KOVA 30 L',8,'middle','bold'); not_(b0+px(175),Y0+px(470),'kapaksız · poşetli · öne çekilir',fs=6); not_(b0+px(175),Y0+px(510),'eleman HER GÜN boşaltır',fs=6)
rc(b0+px(30),Y0+px(45),px(290),px(140),1,2,'#1a49b8','4,3'); tx(b0+px(175),Y0+px(105),'KOL BOŞLUĞU 14',7,'middle','bold','#1a49b8'); tx(b0+px(175),Y0+px(140),'huni YOK · pençe bırakır',6,'middle','','#1a49b8')
rc(b0+px(380),Y0+px(45),px(290),px(585),1,3,'#999','4,3'); tx(b0+px(525),Y0+px(330),'BOŞ (şimdilik)',8,'middle','bold','#999'); tx(b0+px(525),Y0+px(360),'35×59×84',6.5,'middle','','#999')
ln(b0+px(15),Y0+px(650),b1-px(15),Y0+px(650),1,'#111','6,4')
tx(bm,Y0+px(672),'UÇ YUVALARI — yatay · 14',7,'middle','bold')
for k,(ad,dash) in enumerate((('PENÇE',None),('YEDEK',None),('boş',' 4,3'))):
    x_=b0+px(30+k*225); rc(x_,Y0+px(685),px(205),px(105),1.1,2,'#999' if dash else '#111',dash); tx(x_+px(102),Y0+px(745),ad,6,'middle','bold','#999' if dash else '#111')
ln(b0+px(15),Y0+px(800),b1-px(15),Y0+px(800),1,'#111','6,4')
tx(bm,Y0+px(820),'TEPSİ RAFI — 2 yan yana (+1 kolda) · 8',7,'middle','bold','#1a49b8')
for i in range(2):
    cx_=b0+px(180+i*340); el(cx_,Y0+px(855),px(160),px(9),1.2,'#1a49b8'); rc(cx_-px(12),Y0+px(850),px(24),px(10),.8,1,'#1a49b8',None,'#dfe7fb')
not_(bm,Y0+px(880)+8,'v8: sol kova + 14 boşluk · sağ boş · altta uçlar + tepsiler',fs=6.5)

# ================= 3 TOPPING v23 (tek kap 16x54x24 simetrik · 3 kat x 2 · ust teknik YOK: elektrik arka duvar, sogutma ALT arkasi · ALT 2x4 besik) =================
c0,c1=xs[2],xs[3]; cm2=(c0+c1)/2
KAPN={0:('KAŞAR A','SUCUK küp'),410:('KAŞAR B','boş / kav.'),820:('KIYMA kav.','KUŞBAŞI sote')}
for yt in (0,410,820):
    rc(c0+px(15),Y0+px(yt+250),c1-c0-px(30),px(20),1,0,'#1a49b8',None,'#dfe7fb')
    for xk,nm in ((190,KAPN[yt][0]),(350,KAPN[yt][1])):
        bos=nm.startswith('boş'); col='#999' if bos else '#111'; dsh='4,3' if bos else None
        rc(c0+px(xk),Y0+px(yt+10),px(160),px(240),1.3,2,col,dsh,'#f7f6f2' if bos else '#f3efe4')
        if not bos:
            rc(c0+px(xk+8),Y0+px(yt+40),px(144),px(150),0,0,'none',None,'#e9dfa8')
            ln(c0+px(xk+8),Y0+px(yt+215),c0+px(xk+42),Y0+px(yt+240),.8,'#111'); ln(c0+px(xk+152),Y0+px(yt+215),c0+px(xk+118),Y0+px(yt+240),.8,'#111')
            ci(c0+px(xk+80),Y0+px(yt+212),px(35),1.1,'#1d7a4f',None,'#fff'); ci(c0+px(xk+80),Y0+px(yt+125),px(45),.9,'#6b4fa8','3,2')
            ln(c0+px(xk+80),Y0+px(yt+250),c0+px(xk+80),Y0+px(yt+300),2,'#1d7a4f')
        tx(c0+px(xk+80),Y0+px(yt+22),nm,6.4,'middle','bold',col)
        if not bos: tx(c0+px(xk+80),Y0+px(yt+34),'16×54×24 · 14,8 L',5.2,'middle','','#333')
    tx(c1-px(20),Y0+px(yt+22),'KAT %d' % (yt//410+1),6.5,'end','bold','#555')
for b in (270,680,1090):
    tray(c0+px(270),Y0+px(b+75),160,True); el(c0+px(430),Y0+px(b+75),px(160),px(18),1,'#1a49b8','4,3')
    tx(c1-px(20),Y0+px(b+40),'boşluk 14 · tepsi Ø32',5.6,'end','','#1a49b8')
# ALT 74: evaporator 12 + 2 sira besik (27+27) + plint 8; sogutma grubu arkada (kesikli)
rc(c0+px(15),Y0+px(1230),c1-c0-px(30),px(120),.9,0,'#7fb3d5',None,'#e3f2fb'); tx(cm2,Y0+px(1300),'evaporatör + fan (soğuk hava arka kanaldan katlara)',6,'middle','','#1a49b8')
rc(c0+px(20),Y0+px(1420),c1-c0-px(40),px(460),1,3,'#555','5,3','none'); tx(cm2,Y0+px(1455),'SOĞUTMA GRUBU arkada (20 derin, 1/12 HP)',5.6,'middle','bold','#555')
for r_,yt in ((1,1350),(0,1620)):
    for i in range(4):
        xk=12+i*172; lab=[['park','park','çöz. kıyma','çöz. kuşbaşı'],['kaşar yd','kaşar yd','kaşar yd','kaşar yd']][r_][i]
        dsh = r_==0 and i<2
        rc(c0+px(xk),Y0+px(yt+240),px(160),px(30),1,1,'#555',None,'#d8d4c8')
        rc(c0+px(xk),Y0+px(yt),px(160),px(240),1 if dsh else 1.2,2,'#999' if dsh else '#111','4,3' if dsh else None,'#f7f6f2' if dsh else '#e9eef7')
        tx(c0+px(xk+80),Y0+px(yt+128),lab,5.6,'middle','bold','#777' if dsh else '#333')
rc(c0+px(15),Y0+px(1890),c1-c0-px(30),px(80),1,0,'#555',None,'#9e9e9e'); tx(cm2,Y0+px(1940),'plint ızgarası (hava)',6,'middle','','#fff')
tx(c1-px(20),Y0+px(1250),'ALT 74',6.5,'end','bold','#555')
not_(cm2,Y0+px(1832)-px(1832)+Y0*0+Y0+px(1832)-Y0,'',fs=1)
tx(cm2,Y0+px(1215),'motorlar + elektrik paneli 10 cm ARKA DUVARDA (görünmez) · kapta elektrik yok · 16 kap tek tip',5.8,'middle','','#1a49b8')

# ================= 4 OVEN (tepsiyle) =================
d0,d1=xs[3],xs[4]; dm=(d0+d1)/2
for k in range(2):
    ky=Y0+px(170)+k*px(540)
    rc(d0+px(25),ky,d1-d0-px(50),px(450),2)
    rc(d0+px(80),ky+px(70),d1-d0-px(160),px(300),1.4)
    ln(d0+px(25),ky+px(450),d1-px(25),ky+px(450),2.6)
    rc(d0+px(85),ky+px(330),d1-d0-px(170),px(35),1,1,'#777',None,'#eee')
    tray(dm,ky+px(322),kulp=True)
not_(dm,Y0+px(155),"karbon filtre + fan · iç 40×40 · taş taban · 2 kavite")
nk(dm,Y0+px(650),"② tepsi 34 + kulp 12 = 46 > kavite 40:",7)
nk(dm,Y0+px(672),"kavite derinliği 50 (fırın +10) ya da kulp 6",7)
rc(d0+px(25),Y0+px(1180),d1-d0-px(50),px(120),1.6)
rc(d0+px(45),Y0+px(1195),px(230),px(90),1.4,3,'#c9a227',None,'#fff8e0'); tx(d0+px(160),Y0+px(1232),'TANK 4 L',7,'middle','bold','#8a6a3a'); tx(d0+px(160),Y0+px(1258),'45 °C ısıtıcı',6,'middle','','#8a6a3a')
rc(d0+px(300),Y0+px(1195),px(130),px(90),1.2,3); tx(d0+px(365),Y0+px(1232),'POMPA',6.5,'middle','bold'); tx(d0+px(365),Y0+px(1258),'12 V · 8 W',6,'middle','','#555')
rc(d0+px(450),Y0+px(1195),px(120),px(90),1,2); tx(d0+px(510),Y0+px(1245),'vana',6.5,'middle','','#555')
tx(dm,Y0+px(1172),'⑩ SADEYAĞ ÜSTTE + MİNİ POMPA: püskürtme 1-2 bar ister, cazibe damlatır',6.3,'middle','bold','#9a6b1f')
rc(dm-px(22),Y0+px(1300),px(44),px(28),1.3); ln(dm,Y0+px(1328),dm,Y0+px(1345),1.4)
rc(d0+px(25),Y0+px(1320),d1-d0-px(50),px(145),1.4)
ln(dm,Y0+px(1345),dm-px(100),Y0+px(1425),1,'#111','4 4'); ln(dm,Y0+px(1345),dm+px(100),Y0+px(1425),1,'#111','4 4')
tray(dm,Y0+px(1437),kulp=True)
not_(dm,Y0+px(1458),'sprey nişi 14 — tepsi 2 sn geçer, yağ sıcak pidede erir',fs=6.3)
rc(d0+18,Y0+px(1490),d1-d0-36,px(345),1.4,3)
for i in range(3): rc(d0+px(60)+i*px(180),Y0+px(1540),px(150),px(250),1.2,2); tx(d0+px(135)+i*px(180),Y0+px(1675),'teneke',6.5)
not_(dm,Y0+px(1520),'SADEYAĞ STOĞU — 3 teneke ≈ 4 ay (kapaklı bölme; çekmece yok)',fs=6.5)

rc(d0+px(40),Y0+px(20),d1-d0-px(80),px(115),1.4,3); ci(dm,Y0+px(77),px(42),1.1)
not_(dm,Y0+px(220),"tepsi taşa konur · kilit açılır · kapak kapanır · pişince kilitlenir",fs=6.5)

# ================= 5 PACK (bicak yildizi YATAY -> onden ince plaka; kesim bolgesi 41 cm) =================
e0,e1=xs[4],xs[5]; em=(e0+e1)/2
rc(em-px(60),Y0+px(60),px(120),px(90),1.4,3); ln(em,Y0+px(150),em,Y0+px(250),2.6)
rc(em-px(150),Y0+px(250),px(300),px(14),1.6,2)
for i in range(7): ln(em-px(135)+i*px(45),Y0+px(264),em-px(135)+i*px(45),Y0+px(298),1.2)
rc(em-px(200),Y0+px(330),px(400),px(35),1.4,3,'#777',None,'#eee')
tray(em,Y0+px(332),kulp=True)
rc(em-px(190),Y0+px(400),px(380),px(70),1.2,2,'#8a6a3a',None,'#fbf3e6'); tx(em,Y0+px(445),'AÇIK KUTU 32×32 — tepsi eğilir, pide kayar',6.5,'middle','','#8a6a3a')
not_(em,Y0+px(48),'24V piston · bıçak yıldızı YATAY (önden ince plaka) · iz yeter',fs=7.5)
not_(em,Y0+px(316),'kesim yuvası — tepsi oturur, kilit takılı',fs=7)
nk(em,Y0+px(385),'④ bıçak Ø28 (tepsi iç 32)',6.5)
for r in range(29):
    for kx in (e0+8, e0+8+px(320)+4): rc(kx,Y0+px(520)+r*px(45),px(320),px(45),1.05)
not_(em,Y0+px(505),'katlanmış kutu 2×2×29 = 116 — ELEMAN katlar (ıslak mendil içinde) · açık deste YOK',fs=7)

# ================= UST GORUNUM =================
def rd(x,y,w,h,sw=1.2,c="#111"):
    E.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-dasharray="5 4"/>')
YT2=YZ+150
tx(X0,YT2-26,"ÜST GÖRÜNÜM",13,"start","bold")
for i,(_ad,_w) in enumerate(M):
    rc(xs[i]+2,YT2,px(_w)-4,px(840),2,5)
# STORE ust v4: sol kolon icecek 7 kanal (11 kutu derinlemesine), sag kolon taze tepsi 4x5; −18 altta; on: 19 cekmece onu
ln(am,YT2,am,YT2+px(840),1.4)
for i in range(7): rc(a0+px(62)+i*px(82),YT2+px(60),px(66),px(700),1,2)
for j in range(11): ln(a0+px(62),YT2+px(80)+j*px(62),a0+px(62)+7*px(82),YT2+px(80)+j*px(62),.5,'#999')
tx(a0+px(350),YT2+px(45),'içecek: 7 kanal × 11 kutu (derinlemesine) · 1 L altında',7,'middle','','#555')
rc(am+px(85),YT2+px(85),px(530),px(650),1.4)
for j in range(5):
    for i in range(4):
        ci(am+px(162)+i*px(125),YT2+px(160)+j*px(125),px(50),1); ci(am+px(162)+i*px(125),YT2+px(160)+j*px(125),px(60),.7)
tx(am+px(350),YT2+px(45),'taze tepsi 53×65, 4×5 çukur · −18 bandı altta',7,'middle','','#555')
rc(a0+px(20),YT2+px(770),a1-a0-px(40),px(60),1.4,0,'#111',None,PU)
not_((a0+a1)/2,YT2+px(890),'19 çekmece önü (izoleli) — kapak yok · çekmece 70 tam açılır, robot arabası yanda park eder')

# PRESS ust
rc(bm-px(320),YT2+px(20),px(640),px(800),1.6)
ci(b0+px(180),YT2+px(560),px(170),1.1,'#1a49b8','5,4'); ci(b0+px(520),YT2+px(560),px(170),1.1,'#1a49b8','5,4'); tx(bm,YT2+px(790),'tepsi rafı: 2 yan yana (üst, kesik)',7,'middle','','#1a49b8')
ci(bm,YT2+px(420),px(145),1.4); ci(bm,YT2+px(420),px(170),1.2,'#1a49b8','4,3')
not_(bm,YT2+px(890),"PZP-400 64×80 · üst plaka Ø29 · üstte 2 tepsi yan yana (kesik)")
# TOPPING ust v23: kat 1 plani (kasar A + sucuk), helezon x 270/430, agizlar onde y 620, supurme R 270 (tepsi 160 + spiral 110); arka duvar 100 motorlu
rc(c0+px(20),YT2,c1-c0-px(40),px(100),1,0,'#555',None,'#d9d9d9'); tx(cm2,YT2+px(60),'arka duvar 10: motorlar + elektrik',6.2,'middle','bold','#333')
for xk,nm,alt in ((190,'KAŞAR A','16×54'),(350,'SUCUK küp','16×54')):
    rc(c0+px(xk),YT2+px(260),px(160),px(540),1.3,2,'#111',None,'#f3efe4')
    ln(c0+px(xk+80),YT2+px(280),c0+px(xk+80),YT2+px(780),1.4,'#1d7a4f'); ln(c0+px(xk+80),YT2+px(100),c0+px(xk+80),YT2+px(260),1,'#1a49b8','4,3')
    ci(c0+px(xk+80),YT2+px(780),px(22),1.4,'#1d7a4f',None,'#fff'); ci(c0+px(xk+80),YT2+px(780),px(270),1,'#1d7a4f','5,3')
    tx(c0+px(xk+80),YT2+px(400),nm,6.8,'middle','bold'); tx(c0+px(xk+80),YT2+px(430),alt,5.6,'middle','','#333')
    rc(c0+px(xk+60),YT2+px(100),px(40),px(40),1,1,'#1a49b8',None,'#dfe7fb')
rc(c0+px(15),YT2+px(800),c1-c0-px(30),px(40),1,0,'#1a49b8',None,'#dfe7fb')
not_(cm2,YT2+px(890),'kat 1 planı · ağızlar kap ORTASINDA x 27/43 (pide Ø30: tepsi Ø32 + spiral 11 = 27 → duvar içi) · kat 2 kaşar B + boş · kat 3 kıyma + kuşbaşı · ALT 2×4 beşik',fs=6)

# OVEN ust
rc(d0+px(25),YT2+px(120),d1-d0-px(50),px(620),1.6)
rd(dm-px(200),YT2+px(230),px(400),px(400))
ci(dm,YT2+px(430),px(170),1.2,'#1a49b8','4,3'); rc(dm+px(170),YT2+px(415),px(120),px(30),1,1,'#1a49b8')
not_(dm,YT2+px(890),"taş 40×40 · tepsi 34 + kulp 12 = 46 ②")
# PACK ust
rc(em-px(200),YT2+px(440),px(400),px(400),1.4,4,'#777')
ci(em,YT2+px(640),px(170),1.2,'#1a49b8','4,3'); ci(em,YT2+px(640),px(150),1.6)
for dx,dy in [(0,1),(1,0),(0.71,0.71),(0.71,-0.71)]:
    ln(em-px(150)*dx,YT2+px(640)-px(150)*dy,em+px(150)*dx,YT2+px(640)+px(150)*dy,1)
rd(e0+8,YT2+px(60),px(320),px(320)); rd(e0+8+px(320)+4,YT2+px(60),px(320),px(320))
not_(em,YT2+px(890),"kesim yuvası (tepsi) önde · bıçak yatay · şarjör 2×2 arkada (kesik)")
# ROBOT KORIDORU
ln(X0,YT2+px(840),X0,YT2+px(1740),1); ln(X0+px(T),YT2+px(840),X0+px(T),YT2+px(1740),1)
ry=YT2+px(1290)
ln(X0+px(200),ry-5,X0+px(T)-px(200),ry-5,1.6); ln(X0+px(200),ry+5,X0+px(T)-px(200),ry+5,1.6)
rc(cm2-px(160),ry-px(90),px(320),px(180),1.6,3); ci(cm2,ry,px(120),1.8)
E.append(f'<path d="M {cm2-px(1300):.1f} {ry:.1f} A {px(1300):.1f} {px(1300):.1f} 0 0 1 {cm2+px(1300):.1f} {ry:.1f}" fill="none" stroke="#111" stroke-width="1" stroke-dasharray="6 5"/>')
tx(cm2+px(300),ry-14,"3-4 m ray · kol ≥12 kg (UR16e / CRX-20) · uçlar: TEPSİ + PENÇE (uç değiştirici PRESS kabininde)",9.5,"start","","#555")
ln(X0-30,YT2+px(1740),X0+px(T)+30,YT2+px(1740),2.4); ln(X0-30,YT2+px(1762),X0+px(T)+30,YT2+px(1762),1)
tx(X0+px(T)/2,YT2+px(1815),"KAPALI PANEL — CAM YOK · tek açıklık: kiosk + QR teslim dolabı (PICKUP, müşteri cephesi — bu çizimde değil)",10,"middle","","#555")
ox(X0+px(T)+28,YT2,YT2+px(840),"84")
ox(X0+px(T)+28,YT2+px(840),YT2+px(1740),"90 koridor")

# ================= SERVICE =================
sv=X0+px(T)+px(260); sw=px(700)
rc(sv,Y0,sw,px(HG),2.2,5); rc(sv+12,YT,12,px(HA),1.4); rc(sv+sw-24,YT,12,px(HA),1.4)
ln(sv+8,Y0+px(300),sv+sw-8,Y0+px(300),1.4)
rc(sv+px(40),Y0+px(60),px(200),px(160),1.4,3); tx(sv+px(140),Y0+px(155),"UPS",10,"middle","bold")
rc(sv+px(300),Y0+px(90),px(320),px(110),1.4,20); ci(sv+px(320),Y0+px(145),px(28),1.1)
not_(sv+sw/2,Y0+px(272),"TEKNİK: mini UPS (yalnız BEYİN) · yangın tüpü · priz")
ln(sv+8,Y0+px(780),sv+sw-8,Y0+px(780),1); ln(sv+8,Y0+px(1260),sv+sw-8,Y0+px(1260),1.4)
for rrr in (330,810):
    for i in range(6): ln(sv+px(80)+i*px(95),Y0+px(rrr),sv+px(80)+i*px(95),Y0+px(rrr)+px(400),.8)
not_(sv+sw/2,Y0+px(322),"AMBALAJ: yassı kutu 2 raf × 160 = 320 (haftalık)")
rc(sv+px(60),Y0+px(1320),sw-px(120),px(360),1.4,4); ci(sv+px(120),Y0+px(1360),px(16),1.1)
for i in range(4): rc(sv+px(110)+i*px(130),Y0+px(1450),px(90),px(190),1,3)
not_(sv+sw/2,Y0+px(1305),"TEMİZLİK — kilitli · mop kapı içinde")
rc(sv+px(40),Y0+px(1720),sw-px(80),px(100),1.4,3); ln(sv+sw/2-20,Y0+px(1770),sv+sw/2+20,Y0+px(1770),2)
not_(sv+sw/2,Y0+px(1708),"poşet + çöp poşedi çekmecesi")
oy(sv,sv+sw,Y0-24,"70")
tx(sv+sw/2,YZ+24,"7 · SERVICE",11.5,"middle","bold"); tx(sv+sw/2,YZ+42,"(ayrı duvarda — makineye bağlı değil)",9.5,"middle","","#555")

# ================= KONTROL KUTUSU =================
kx=X0+px(T)+px(120); ky=YT2+10
rc(kx-10,ky-18,px(1270),px(1500),1.4,6,'#b3452b',None,'#fff8f5')
tx(kx,ky,"KONTROL — istasyonlar arası uyum (5 Eyl 2026)",12,"start","bold","#b3452b")
K=[
 ("① ✓ STORE v4: alt −18 6 çekmece (4 hamur + 2 kaset) · 19 çekmece × 61 · kapak yok","→ PU 60/80 · ray 12,7 · ölçü kontrolü: tatlı 4 kanal, soğutma 28, top ≤ 6 cm · dikey 185 ✓","#1d7a4f"),
 ("② OVEN kavite 40×40: tepsi Ø32 + kulp 12 = 44 → kapak yine kapanmaz","→ kavite derinliği 50 (dış 65 → 75) YA DA kulp 6 cm — KARAR","#b3452b"),
 ("③ ✓ TEPSİ DÖNMEZ → v23: ağızlar kap ORTASINDA x 27/43 (y 78); süpürme R 27 = tepsi 16 + spiral 11","→ sol x 0-54, sağ 16-70: duvar içi, pay 0 (iç yüzey düz) · spiral 11 kenar kapatma → prototip","#1d7a4f"),
 ("④ ✓ PACK: bıçak yatay, önden ince; açık deste kalktı → şarjör 2×2×29 = 116 kutu","→ bıçak Ø28 + yuva pimleri","#1d7a4f"),
 ("⑤ ✓ PRESS üst plaka Ø29: Fersah cevabı (26 Ağu) CP-330 max 36 cm açar, PLC olur, PZR-250 konveyör olur","→ 'aynı hatta pide olmaz' dedi — yuvarlak Ø30 taban olduğu tekrar sorulacak","#9a6b1f"),
 ("⑥ ✓ PRESS v8: sol yarı 30 L kova + 14 cm kol boşluğu (huni/çekmece yok) · sağ yarı boş","→ altta yatay uç yuvaları 14 + tepsi rafı 8 (2 yan yana + 1 kolda)","#1d7a4f"),
 ("⑦ ✓ Kol yükü ≤ 13 kg: tek kap 16×54×24 (kaşar 6,1 kg + kap 3,5) — 37 kg kaşar kabı yok","→ 12 kg kobot yeter (UR10e / CRX-10iA) · ray aynı","#1d7a4f"),
 ("⑧ ✓ TOPPING v23: TEK kap tipi 16×54×24 (simetrik, ayna yok, 16 kap) · 3 kat × 2 · üst teknik yok","→ elektrik arka duvar içi, soğutma grubu ALT arkası (plint ızgarası) · ALT 2×4 beşik · STORE −18 3/modül","#1d7a4f"),
 ("⑨ ✓ Dozaj boşluğu 14 × 3 kat (tepsi 158 / 117 / 76 cm) · kilit 8,5 < ağız 11","→ 158 cm üst düzlem: kobot erişimi kontrol · her tarif tek düzlemde (kat değişimi yok)","#1d7a4f"),
 ("⑩ OVEN sadeyağ: tank ÜSTTE + 12 V pompa 8 W (püskürtme basınç ister)","→ cazibe yalnız damlatır; çekmeceler kalktı → teneke stoğu ×3 (4 ay)","#9a6b1f"),
 ("⑪ 197 ✓ · 415 ✓ · derinlik 84 HER KABİN ✓ · TOPPING içi 3×(27+14) + 74 = 197 ✓","→ STORE sol kolon 29+7+82+5+54 = 177 + 8 pay ✓ · TOPPING derinlik 4 + 54/70 + 10 = 84 ✓","#1d7a4f"),
 ("⑫ Pide Ø30 → tepsi Ø34 → Ø32 zinciri: PRESS plaka Ø29 ✓ · PACK bıçak Ø28 ✓ · OVEN 44 (②) · robot uç","→ robot_tepsi_el v1 (Ø34) → v2; harçlar KAVRULMUŞ/SOTE vakumlu (çiğ olmaz); kaşar akış prototipi","#9a6b1f"),
]
yy=ky+22
for a_,b_,c_ in K:
    tx(kx,yy,a_,9.2,"start","bold",c_); yy+=13
    tx(kx+12,yy,b_,8.8,"start","","#444"); yy+=17

# ================= OLCULER + BASLIK =================
for i,(ad,w) in enumerate(M):
    oy(xs[i],xs[i+1],Y0-24,str(round(w/10)))
    tx((xs[i]+xs[i+1])/2,YZ+24,ad,10.5,w="bold")
oy(X0,X0+px(T),YZ+52,"TOPLAM "+str(round(T/10))+" cm",12)
ox(X0-30,Y0,YT,str(round(HG/10))); ox(X0-30,YT,YZ,str(round(HA/10))); ox(X0-64,Y0,YZ,"TOPLAM "+str(round((HG+HA)/10)))
tx(X0,Y0-94,"AUTOKITCH — HAT v45 · TÜM İSTASYONLAR SON VERSİYON (5 Eyl 2026) — STORE v4 · PRESS v8 · TOPPING v23 (tek kap 16×54×24, 3 kat, üst teknik yok) · OVEN tank+pompa · PACK 116",15,"start","bold")
tx(X0,Y0-72,"Robot: tek kol (12 kg yeter — en ağır kap 13 kg), uç değiştirici — TEPSİ ucu (pide press'ten kutuya kadar tepside, fırına tepsiyle) + PENÇE ucu (hamur · kutu · içecek · kap). Mavi = tepsi Ø32 (pide Ø30). Kırmızı = KONTROL bulgusu.",10,"start","","#333")
tx(X0,Y0-54,"Ölçüler cm. HER KABİN 70/65/140 × 197 × 84. Açık: ② fırın kavitesi 44 · ⑩ yağ pompa · ⑫ tepsi Ø32 zinciri (robot uç v2) · TOPPING prototip (spiral 11, kaşar akış) — bu turda çözülen: ③ ⑤ ⑦ ⑧ ⑨ ⑪",10,"start","","#333")

W=int(X0+px(T)+px(1420)); H=int(YT2+px(1860))
svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="#ffffff"/>'+''.join(E)+'</svg>')
OUT=r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\FULL_MAKINE\hat_on_gorunus_teknik_v45.svg"
io.open(OUT,'w',encoding='utf-8').write(svg)
print('yazildi:',OUT,'|',W,'x',H)
