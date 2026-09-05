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

# ================= 1 STORE (v38 aynen) =================
a0,a1=xs[0],xs[1]; am=a0+px(700)
rc(a0+8,Y0+px(10),a1-a0-16,px(290),1.6)
ci(a0+px(350),Y0+px(150),px(78),1.2); ci(a0+px(1050),Y0+px(150),px(78),1.2)
ln(a0+px(312),Y0+px(112),a0+px(388),Y0+px(188),.9); ln(a0+px(312),Y0+px(188),a0+px(388),Y0+px(112),.9)
ln(a0+px(1012),Y0+px(112),a0+px(1088),Y0+px(188),.9); ln(a0+px(1012),Y0+px(188),a0+px(1088),Y0+px(112),.9)
for g in range(4): ln(a0+20,Y0+px(230)+g*px(15),a1-20,Y0+px(230)+g*px(15),.7)
rc(a0+8,Y0+px(310),a1-a0-16,px(1530),1.8)
rc(am-px(35),Y0+px(310),px(70),px(1530),1.2)
rc(a0+px(60),Y0+px(370),am-px(35)-a0-px(60),px(540),1)
rc(a0+8,Y0+px(950),am-px(35)-a0-8,px(50),1.6)
for kz in range(7):
    ln(a0+px(60),Y0+px(420)+kz*px(70),a0+px(85),Y0+px(420)+kz*px(70),.8)
    ln(am-px(85),Y0+px(420)+kz*px(70),am-px(60),Y0+px(420)+kz*px(70),.8)
for r in range(4):
    ty=Y0+px(490)+r*px(120)
    ln(a0+px(72),ty,am-px(72),ty,1.2)
    ln(a0+px(72),ty,a0+px(72),ty-px(20),1.2); ln(am-px(72),ty,am-px(72),ty-px(20),1.2)
    rc((a0+am)/2-px(80),ty+px(5),px(160),px(14),.9,2)
    for i in range(4):
        ci(a0+px(175)+i*px(125),ty-px(48),px(46),1)
        el(a0+px(175)+i*px(125),ty-px(2),px(56),px(8),.8)
not_((a0+a1)/2,Y0+px(62),"soğutma grupları ×2 — standart üst bölme (◐ Kemal: diğer istasyonlarda da ÜSTTE — burada zaten üstte)")
not_((a0+am)/2,Y0+px(332),"DONMUŞ −18° · 4 raf = 80 (1 GÜN)",fs=8.5)
not_((a0+am)/2,Y0+px(940),"yatay izoleli ayırıcı — altı +3 °C")
for k4 in range(4):
    cy4=Y0+px(1000)+k4*px(128)
    rc(a0+px(30),cy4,am-px(62)-a0,px(118),1.4,3)
    for i in range(7): rc(a0+px(40)+i*px(78),cy4+px(6),px(64),px(106),1)
rc(a0+px(30),Y0+px(1530),am-px(62)-a0,px(300),1.6,3)
for i in range(5): rc(a0+px(52)+i*px(104),Y0+px(1548),px(84),px(266),1)
not_((a0+am)/2,Y0+px(990),"İÇECEK+TATLI — 4 çekmece × 7 kanal = 28 (kutu 24 · tatlı 3 · yedek 1)")
not_((a0+am)/2,Y0+px(1522),"1L çekmecesi — 5 kanal × 8 (plan 25 + yedek)")
a2,a3=am,xs[1]
ln(a2+12,Y0+px(310),a3-15,Y0+px(310),1)
ln(a2+px(35),Y0+px(315),a3-15,Y0+px(315),1.4)
ln(a2+px(35),Y0+px(1455),a3-15,Y0+px(1455),1.4)
rc(a2+px(40),Y0+px(360),a3-px(60)-a2-px(40),px(1080),1)
for kz in range(20):
    ln(a2+px(60),Y0+px(405)+kz*px(70),a2+px(85),Y0+px(405)+kz*px(70),.8)
    ln(a3-px(85),Y0+px(405)+kz*px(70),a3-px(60),Y0+px(405)+kz*px(70),.8)
for r in range(8):
    ty=Y0+px(490)+r*px(130)
    ln(a2+px(72),ty,a3-px(72),ty,1.2)
    ln(a2+px(72),ty,a2+px(72),ty-px(22),1.2); ln(a3-px(72),ty,a3-px(72),ty-px(22),1.2)
    rc((a2+a3)/2-px(80),ty+px(6),px(160),px(16),.9,2)
    for i in range(4):
        ci(a2+px(175)+i*px(125),ty-px(52),px(50),1)
        el(a2+px(175)+i*px(125),ty-px(3),px(58),px(9),.8)
not_((a2+a3)/2,Y0+px(340),"TAZE +3 °C · 8 raf × 20 = 160 (2 GÜN)")
not_((a2+a3)/2,Y0+px(1560),"BOŞ — büyüme payı (+3 raf yeri, tek blok)")
# KONTROL 1: TOPPING donmus kasetleri icin -18 raf
for i in range(4): rc(a0+px(90)+i*px(140),Y0+px(372),px(120),px(60),1,2,'#b3452b','4,3')
nk((a0+am)/2,Y0+px(358),"① TOPPING'in 4 donmuş kaseti (≈36 L): −18 bölmede raf YOK → 5. raf",7)

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
# ust bolge: sol uc yuvalari / sag cop
xB=b0+px(335); ln(xB,Y0+px(50),xB,Y0+px(880),1.1,"#111","6,5")
rc(b0+px(35),Y0+px(70),px(280),px(790),1.5,4)
tx(b0+px(175),Y0+px(115),"UÇ YUVALARI",9.5,"middle","bold")
rc(b0+px(105),Y0+px(165),px(140),px(36),1.2,2); ln(b0+px(135),Y0+px(201),b0+px(150),Y0+px(260),1.2); ln(b0+px(215),Y0+px(201),b0+px(200),Y0+px(260),1.2)
not_(b0+px(175),Y0+px(300),"1: PENÇE ucu",fs=8)
rc(b0+px(105),Y0+px(360),px(140),px(36),1.2,2); el(b0+px(175),Y0+px(430),px(110),px(12),1.4,'#1a49b8')
not_(b0+px(175),Y0+px(480),"2: TEPSİ ucu (temiz)",fs=8)
rc(b0+px(105),Y0+px(560),px(140),px(36),1.2,2,"#999","4,3"); el(b0+px(175),Y0+px(630),px(110),px(12),1,'#1a49b8','4,3')
not_(b0+px(175),Y0+px(680),"3: yedek tepsi / boş",fs=8)
not_(b0+px(175),Y0+px(750),"kilit: pim+burç (SMARTSHIFT sınıfı)",fs=7.5)
not_(b0+px(175),Y0+px(790),"uç değişimi pide başına ×2",fs=7.5)
nk(b0+px(175),Y0+px(835),"⑥ temiz/kirli tepsi rafı 8-10 → yer AÇIK",7)
tx(b0+px(510),Y0+px(115),"ÇÖP",9.5,"middle","bold")
ln(b0+px(360),Y0+px(160),b0+px(430),Y0+px(330),1.6); ln(b0+px(660),Y0+px(160),b0+px(590),Y0+px(330),1.6); ln(b0+px(360),Y0+px(160),b0+px(660),Y0+px(160),1.6)
not_(b0+px(510),Y0+px(142),"huni — bırak-geç",fs=7.5)
rc(b0+px(400),Y0+px(380),px(220),px(470),1.6,4)
tx(b0+px(510),Y0+px(600),"KOVA 30 L",9.5,"middle","bold")
not_(b0+px(510),Y0+px(660),"motorsuz · eleman HER GÜN",fs=7.5)
not_(bm,Y0+px(880)+8,"kabin 70 — PZP üstü tam dolu: sol 33 uç yuvaları · sağ 37 çöp",fs=7.5)

# ================= 3 TOPPING (v8) =================
c0,c1=xs[2],xs[3]; cm2=(c0+c1)/2
# teknik bolme ustte
tx(cm2,Y0+px(40),"SOĞUTMA (ÜSTTE) 25 · 1/8 HP · +3 °C · BUZLUK YOK",8,"middle","bold")
rc(c0+px(55),Y0+px(60),px(180),px(160),1.2,3); ci(c0+px(145),Y0+px(140),px(50),1)
rc(c0+px(260),Y0+px(60),px(200),px(160),1.2,3); tx(c0+px(360),Y0+px(150),"kondenser",7)
rc(c0+px(490),Y0+px(60),px(150),px(160),1.2,3); ci(c0+px(565),Y0+px(140),px(45),1)
ln(c0+px(15),Y0+px(250),c1-px(15),Y0+px(250),1,"#111","6,4")
tx(cm2,Y0+px(285),"ELEKTRİK 14 · PLC I/O · 4 step sürücü · 24 V",8,"middle","bold")
rc(c0+px(50),Y0+px(300),px(150),px(80),1.1,2); tx(c0+px(125),Y0+px(348),"PLC",7)
for i in range(4): rc(c0+px(225+i*70),Y0+px(300),px(55),px(80),1,2)
rc(c0+px(525),Y0+px(300),px(120),px(80),1.1,2); tx(c0+px(585),Y0+px(348),"PSU",7)
ln(c0+px(15),Y0+px(400),c1-px(15),Y0+px(400),1.6)
# kaset kati
KY=410
kaset(c0+px(355),Y0+px(KY-8),px(165),px(250),"KAVURMA arka",dash="4,3",c="#888")
kaset(c0+px(525),Y0+px(KY-8),px(165),px(250),"KUŞBAŞI arka",dash="4,3",c="#888")
kaset(c0+px(10),Y0+px(KY),px(335),px(250),"KAŞAR A","35×42×25 · 15 kg")
kaset(c0+px(355),Y0+px(KY),px(335),px(250),"SUCUK (ön)","35×21×25 · 10 kg")
# koniler + carklar + cikislar (x 200 / 400 / 470 / 520)
CY=KY+330
ln(c0+px(15),Y0+px(KY+252),c0+px(150),Y0+px(CY-55),1.2); ln(c0+px(340),Y0+px(KY+252),c0+px(255),Y0+px(CY-55),1.2)
ln(c0+px(360),Y0+px(KY+252),c0+px(430),Y0+px(CY-40),1.2); ln(c0+px(685),Y0+px(KY+252),c0+px(510),Y0+px(CY-40),1.2)
for cx0,r in ((200,55),(470,40)):
    ci(c0+px(cx0),Y0+px(CY),px(r),1.6)
    for k in range(6):
        a=k*math.pi/3; ln(c0+px(cx0),Y0+px(CY),c0+px(cx0)+px(r)*math.cos(a),Y0+px(CY)+px(r)*math.sin(a),.9)
    ln(c0+px(cx0-16),Y0+px(CY+60),c0+px(cx0-16),Y0+px(CY+160),1.3); ln(c0+px(cx0+16),Y0+px(CY+60),c0+px(cx0+16),Y0+px(CY+160),1.3)
for cx0 in (400,520):
    ci(c0+px(cx0),Y0+px(CY-20),px(35),1,"#999","4,3")
    ln(c0+px(cx0-13),Y0+px(CY+15),c0+px(cx0-13),Y0+px(CY+160),.9,"#999","4,3"); ln(c0+px(cx0+13),Y0+px(CY+15),c0+px(cx0+13),Y0+px(CY+160),.9,"#999","4,3")
rc(c0+px(120),Y0+px(CY-20),px(45),px(40),1.1,2); tx(c0+px(142),Y0+px(CY+5),"M",7,"middle","bold")
rc(c0+px(535),Y0+px(CY-20),px(45),px(40),1.1,2); tx(c0+px(557),Y0+px(CY+5),"M",7,"middle","bold")
ln(c0+px(15),Y0+px(CY+130),c1-px(15),Y0+px(CY+130),1.6)
not_(cm2,Y0+px(CY+178),"soğuk kabin tabanı · 4 çıkış ağzı 3 cm sarkar · kapak YOK",fs=7.5)
# acik dozaj boslugu
BY=CY+130
tx(cm2,Y0+px(BY+90),"AÇIK DOZAJ BOŞLUĞU 26 — tabla · kızak · motor YOK",8,"middle","bold","#1a49b8")
tray(c0+px(200),Y0+px(BY+170),kulp=True)
rc(c0+px(430),Y0+px(BY+120),px(60),px(40),1.2,2,'#1a49b8'); tx(c0+px(460),Y0+px(BY+145),"kilit",6.5,"middle","",'#1a49b8')
ln(c0+px(460),Y0+px(BY+120),c0+px(520),Y0+px(BY+60),1.8,'#1a49b8')
nk(cm2,Y0+px(BY+235),"③ hareket KARAR BEKLİYOR: ön saçak / C-tutucu (analiz v1)",7)
ln(c0+px(15),Y0+px(BY+270),c1-px(15),Y0+px(BY+270),1,"#111","6,4")
# gecis rafi
GY=BY+270
tx(cm2,Y0+px(GY+30),"GEÇİŞ RAFI (robot takas · ayrı soğuk bölme) 2 kat",8,"middle","bold","#1a49b8")
kaset(c0+px(10),Y0+px(GY+45),px(335),px(250),"KAŞAR B","dolu +3")
kaset(c0+px(355),Y0+px(GY+45),px(335),px(250),"KAŞAR C","dolu +3")
kaset(c0+px(355),Y0+px(GY+322),px(165),px(250),"ÇÖZÜLME 1",dash="4,3",c="#1a49b8")
kaset(c0+px(525),Y0+px(GY+322),px(165),px(250),"ÇÖZÜLME 2",dash="4,3",c="#1a49b8")
kaset(c0+px(10),Y0+px(GY+335),px(335),px(250),"KAŞAR D","dolu +3")
kaset(c0+px(355),Y0+px(GY+335),px(335),px(250),"SUCUK yedek","haftalık")
not_(cm2,Y0+px(GY+640),"14 kaset döner · eleman haftada 1 · donmuşlar STORE −18",fs=7.5)
not_(cm2,Y0+px(1835),"derinlik iç 42 / dış ~55 (hat 84 — önü geride)",fs=7)

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
rc(d0+px(25),Y0+px(1180),d1-d0-px(50),px(190),1.6)
rc(dm-px(30),Y0+px(1180),px(60),px(50),1.4); ln(dm,Y0+px(1230),dm,Y0+px(1255),1.6)
ln(dm,Y0+px(1255),dm-px(110),Y0+px(1335),1,"#111","4 4"); ln(dm,Y0+px(1255),dm+px(110),Y0+px(1335),1,"#111","4 4")
tray(dm,Y0+px(1345),kulp=True)
rc(d0+18,Y0+px(1390),d1-d0-36,px(230),1.4)
for i in range(3): rc(d0+30+i*px(120),Y0+px(1425),px(100),px(160),1,2)
rc(d0+30+px(360),Y0+px(1425),px(120),px(160),1.4,2)
ln(d0+30+px(420),Y0+px(1425),d0+30+px(420),Y0+px(1215),1,"#111","3 4"); ln(d0+30+px(420),Y0+px(1215),dm+px(30),Y0+px(1215),1,"#111","3 4")
for k in range(2):
    rc(d0+18,Y0+px(1650)+k*px(105),d1-d0-36,px(90),1.4)
    ln(dm-22,Y0+px(1650)+k*px(105)+px(45),dm+22,Y0+px(1650)+k*px(105)+px(45),2)
rc(d0+px(40),Y0+px(20),d1-d0-px(80),px(115),1.4,3); ci(dm,Y0+px(77),px(42),1.1)
not_(dm,Y0+px(1172),"sadeyağ sprey — sıcak pide TEPSİDE geçer, yağ erir",fs=8)
not_(dm,Y0+px(1412),"sadeyağ teneke ×3 + pompa·ısıtıcı",fs=8)
not_(dm,Y0+px(1638),"servis çekmeceleri",fs=8)
not_(dm,Y0+px(220),"tepsi taşa konur · kilit açılır · kapak kapanır · pişince kilitlenir",fs=6.5)

# ================= 5 PACK (kesim yuvasi + robot eger) =================
e0,e1=xs[4],xs[5]; em=(e0+e1)/2
ln(em,Y0+px(80),em,Y0+px(250),2.6); rc(em-15,Y0+px(140),30,px(90),1.6)
ci(em,Y0+px(420),px(150),2)
for dx,dy in [(0,1),(1,0),(0.71,0.71),(0.71,-0.71)]:
    ln(em-px(150)*dx,Y0+px(420)-px(150)*dy,em+px(150)*dx,Y0+px(420)+px(150)*dy,1.2)
rc(em-px(200),Y0+px(590),px(400),px(40),1.4,3,'#777',None,'#eee')
tray(em,Y0+px(592),kulp=True)
not_(em,Y0+px(68),"piston + bıçak yıldızı Ø30 (kuvvet yuvaya, iz yeter)",fs=8)
not_(em,Y0+px(665),"KESİM YUVASI — tepsi oturur, kilit takılı",fs=8)
nk(em,Y0+px(695),"④ bıçak Ø30 / tepsi iç Ø32: 1 cm pay → bıçak Ø28",7)
not_(em,Y0+px(725),"itici YOK — robot tepsiyi EĞER, pide ön ağızdan kutuya",fs=7.5)
for r in range(20):
    for kx in (e0+8, e0+8+px(320)+4): rc(kx,Y0+px(760)+r*px(45),px(320),px(45),1.05)
rc(e0+8,Y0+px(1690),px(320)*2+4,px(150),1.4)
for i in range(3): ln(e0+16,Y0+px(1720)+i*px(35),e0+196,Y0+px(1720)+i*px(35),.8)
not_(em,Y0+px(1675),"katlanmış kutu 2×2×20 = 80 — ELEMAN katlar (ıslak mendil içinde)",fs=7.5)
not_(em,Y0+px(1830),"açık deste ≈40",fs=7.5)

# ================= UST GORUNUM =================
def rd(x,y,w,h,sw=1.2,c="#111"):
    E.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-dasharray="5 4"/>')
YT2=YZ+150
tx(X0,YT2-26,"ÜST GÖRÜNÜM",13,"start","bold")
for i,(_ad,_w) in enumerate(M):
    if i==2: continue
    rc(xs[i]+2,YT2,px(_w)-4,px(840),2,5)
# STORE ust
ln(am,YT2,am,YT2+px(840),1.4)
for (g0,g1) in ((a0,am),(am,a1)):
    rc(g0+px(60),YT2+px(60),g1-g0-px(120),px(700),1)
    rc(g0+px(85),YT2+px(85),px(530),px(650),1.4)
    for j in range(5):
        for i in range(4):
            ci(g0+px(162)+i*px(125),YT2+px(160)+j*px(125),px(50),1)
    rc(g0+px(20),YT2+px(770),g1-g0-px(40),px(60),1.4)
not_((a0+a1)/2,YT2+px(45),"tek kasa 2 KAPI: sol donmuş · sağ taze+içecek+tatlı")
not_((a0+a1)/2,YT2+px(890),"MOTORLU SERVİS KAPAĞI — BEYİN robot yola çıkarken açar · switch teyidi")
# PRESS ust
rc(bm-px(320),YT2+px(20),px(640),px(800),1.6)
ci(bm,YT2+px(420),px(145),1.4); ci(bm,YT2+px(420),px(170),1.2,'#1a49b8','4,3')
not_(bm,YT2+px(890),"PZP-400 64×80 · üst plaka Ø29 · tepsi Ø34 (mavi)")
# TOPPING ust: 70 x 55 (arkaya yaslı), on 29 geride
rd(c0+2,YT2,px(700)-4,px(840),1.2,'#999')
rc(c0+2,YT2,px(700)-4,px(550),2,5)
rc(c0+px(0)+6,YT2+px(60),px(350)-8,px(420),1.2); tx(c0+px(175),YT2+px(270),"KAŞAR 35×42",8,"middle","bold")
rc(c0+px(350)+2,YT2+px(60),px(170)-4,px(210),1.2); tx(c0+px(435),YT2+px(165),"KAV.",7.5,"middle","bold")
rc(c0+px(520)+2,YT2+px(60),px(170)-4,px(210),1.2); tx(c0+px(605),YT2+px(165),"KUŞ.",7.5,"middle","bold")
rc(c0+px(350)+2,YT2+px(270),px(350)-4,px(210),1.2); tx(c0+px(525),YT2+px(375),"SUCUK 35×21",8,"middle","bold")
for x_,y_ in ((200,210),(400,175),(470,300),(520,175)): ci(c0+px(x_),YT2+px(60+y_),px(18),1.3,'#b3452b',None,'#fde3dc')
ci(c0+px(200),YT2+px(270),px(170),1.1,'#1a49b8','5,4')
not_(cm2,YT2+px(590),"ön 29 cm geride (koridora yer)",fs=7.5)
not_(cm2,YT2+px(890),"kaset katı 70×42 · 4 çıkış (kırmızı) · tepsi Ø34 (mavi)")
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
not_(em,YT2+px(890),"kesim yuvası (tepsi) önde · şarjör 2×2 arkada (kesik)")
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
tx(kx,ky,"KONTROL — istasyonlar arası uyum (4 Eyl 2026)",12,"start","bold","#b3452b")
K=[
 ("① STORE −18 bölmesi: TOPPING'in 4 donmuş kaseti için raf yok","→ 5. raf / büyüme payı; STORE v39 turunda (soğutma zaten üstte)","#b3452b"),
 ("② OVEN kavite 40×40: tepsi Ø34 + kulp 12 = 46 → kapak kapanmaz","→ kavite derinliği 50 (dış boy 65 → 75) YA DA kulp 6 cm","#b3452b"),
 ("③ TOPPING dozaj hareketi: kenar tutuşlu tepsi 360° dönemez","→ karar: ön saçak (öneri) / C-tutucu — analiz v1","#b3452b"),
 ("④ PACK bıçak Ø30 – tepsi iç Ø32: 1 cm pay az","→ bıçak yıldızı Ø28 (pide Ø28 tam) + yuva pimleri","#b3452b"),
 ("⑤ PRESS üst plaka Ø40 → Ø29 (tepsi içinde basma)","→ Fersah'a kalıp/plaka sorusu; alt plaka üstünde tepsi ✓","#b3452b"),
 ("⑥ Tepsi havuzu (8-10) + kirli/temiz raf: yeri yok","→ PRESS uç yuvası 2-3 + SERVICE? — Kemal ile ayrıca","#b3452b"),
 ("⑦ Kol sınıfı 10 → ≥12 kg (kaşar kaseti 15 kg)","→ UR16e / CRX-20iA/L / H2017; ray aynı","#9a6b1f"),
 ("⑧ TOPPING derinlik 55 / hat 84: önü 29 cm geride","→ sorun değil, koridor genişler; saçak seçilirse tam yerine oturur","#1d7a4f"),
 ("⑨ Yükseklik: 5 kabin 185+12 = 197 ✓ · genişlik 140+70+70+65+70 = 415 ✓","→ TOPPING içi 40+25+23+26+69 = 183 ✓ (2 cm pay)","#1d7a4f"),
 ("⑩ Tepsi Ø34: press plaka Ø40 ✓ · sprey nişi ✓ · kesim yuvası ✓ · kutu 32 iç → pide 28 ✓","→ tek uyumsuz yer fırın kavitesi (②)","#1d7a4f"),
 ("⑪ Haftalık ritim: hamur 3 günde bir · topping/içecek/kutu haftalık · yağ aylık","→ STORE + TOPPING + SERVICE stok tabloları tutarlı ✓","#1d7a4f"),
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
tx(X0,Y0-94,"AUTOKITCH — HAT v39 · TÜM İSTASYONLAR SON VERSİYON (4 Eyl 2026) — STORE v38 · PRESS v4 + tepsi · TOPPING v8 · OVEN tepsiyle · PACK kesim yuvası · robot TEPSİ ucu v1",15,"start","bold")
tx(X0,Y0-72,"Robot: tek kol (≥12 kg), uç değiştirici — TEPSİ ucu (pide press'ten kutuya kadar tepside, fırına tepsiyle) + PENÇE ucu (hamur · kutu · içecek · kaset). Mavi = tepsi Ø34. Kırmızı = KONTROL bulguları (sağ altta liste).",10.5,"start","","#555")
tx(X0,Y0-54,"Ölçüler cm. Açık kararlar: ③ dozaj hareketi (saçak / C-tutucu) · ⑥ tepsi havuzu · ① STORE 5. raf + soğutma üstte turu · ② fırın kavitesi 50",10.5,"start","","#b3452b")

W=int(X0+px(T)+px(1420)); H=int(YT2+px(1860))
svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="#ffffff"/>'+''.join(E)+'</svg>')
OUT=r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\FULL_MAKINE\hat_on_gorunus_teknik_v39.svg"
io.open(OUT,'w',encoding='utf-8').write(svg)
print('yazildi:',OUT,'|',W,'x',H)
