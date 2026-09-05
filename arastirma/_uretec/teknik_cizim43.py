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

# ================= 1 STORE v39 (-18: 4 hamur rafi + 5. raf donmus kasetler; 1L cekmecesi sag kolon altina) =================
a0,a1=xs[0],xs[1]; am=a0+px(700)
rc(a0+8,Y0+px(10),a1-a0-16,px(290),1.6)
ci(a0+px(350),Y0+px(150),px(78),1.2); ci(a0+px(1050),Y0+px(150),px(78),1.2)
ln(a0+px(312),Y0+px(112),a0+px(388),Y0+px(188),.9); ln(a0+px(312),Y0+px(188),a0+px(388),Y0+px(112),.9)
ln(a0+px(1012),Y0+px(112),a0+px(1088),Y0+px(188),.9); ln(a0+px(1012),Y0+px(188),a0+px(1088),Y0+px(112),.9)
for g in range(4): ln(a0+20,Y0+px(230)+g*px(15),a1-20,Y0+px(230)+g*px(15),.7)
rc(a0+8,Y0+px(310),a1-a0-16,px(1530),1.8)
rc(am-px(35),Y0+px(310),px(70),px(1530),1.2)
rc(a0+px(60),Y0+px(370),am-px(35)-a0-px(60),px(820),1)
rc(a0+8,Y0+px(1190),am-px(35)-a0-8,px(50),1.6)
for kz in range(11):
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
# 5. raf: 4 donmus kucuk kaset (kavurma x2, kusbasi x2) — onde 2, arkada 2 (kesik)
ln(a0+px(72),Y0+px(1170),am-px(72),Y0+px(1170),1.2); rc((a0+am)/2-px(80),Y0+px(1174),px(160),px(14),.9,2)
for i in range(2):
    rc(a0+px(100)+i*px(180),Y0+px(905),px(170),px(250),1,2,'#1a49b8','4,3')
    rc(a0+px(90)+i*px(180),Y0+px(918),px(170),px(250),1.3,2,'#1a49b8',None,'#eef2fb')
    tx(a0+px(175)+i*px(180),Y0+px(1035),['KAV','KUŞ'][i]+' −18',7.5,'middle','bold','#1a49b8')
    tx(a0+px(175)+i*px(180),Y0+px(1060),'×2 (arka kesik)',6.5,'middle','','#1a49b8')
rc(a0+px(470),Y0+px(918),px(150),px(250),1,2,'#999','4,3'); tx(a0+px(545),Y0+px(1045),'büyüme',6.5,'middle','','#999')
tx((a0+am)/2,Y0+px(895),'① ✓ 5. RAF: 4 donmuş kaset 17×21×25 (kavurma ×2 · kuşbaşı ×2) — robot bitişten 1 gün önce alır',6.5,'middle','bold','#1d7a4f')
not_((a0+am)/2,Y0+px(332),'DONMUŞ −18° · 4 raf hamur = 80 (1 GÜN) + 5. raf TOPPING kasetleri',fs=8)
not_((a0+am)/2,Y0+px(1230),'yatay izoleli ayırıcı — altı +3 °C',fs=8)
for k4 in range(4):
    cy4=Y0+px(1260)+k4*px(135)
    rc(a0+px(30),cy4,am-px(62)-a0,px(120),1.4,3)
    for i in range(7): rc(a0+px(40)+i*px(78),cy4+px(6),px(64),px(108),1)
not_((a0+am)/2,Y0+px(1252),'İÇECEK+TATLI — 4 çekmece × 7 kanal = 28 (kutu 24 · tatlı 3 · yedek 1)',fs=7.5)
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
not_((a2+a3)/2,Y0+px(340),'TAZE +3 °C · 8 raf × 20 = 160 (2 GÜN)')
rc(a2+px(40),Y0+px(1480),a3-px(62)-a2-px(40),px(350),1.6,3)
for i in range(5): rc(a2+px(62)+i*px(104),Y0+px(1498),px(84),px(314),1)
not_((a2+a3)/2,Y0+px(1472),'1L çekmecesi — 5 kanal × 8 (SOL kolondan buraya: −18\'e yer açıldı)',fs=7.5)

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
# ust bolge v7 — YATAY KATMANLAR (alttan uste): tepsi rafi 8 · uc yuvalari 14 · cop cekmecesi 22 · huni
for yy_ in (790, 630, 390): ln(b0+px(15),Y0+px(yy_),b1-px(15),Y0+px(yy_),1,'#111','6,4')
# katman 1: tepsi rafi (2 yan yana)
tx(bm,Y0+px(816),'TEPSİ RAFI — 2 yan yana (+1 kolda = 3)',7,'middle','bold','#1a49b8')
for i in range(2):
    cx_=b0+px(180+i*340)
    rc(cx_-px(172),Y0+px(848),px(14),px(14),1,1); rc(cx_+px(158),Y0+px(848),px(14),px(14),1,1)
    el(cx_,Y0+px(855),px(165),px(9),1.3,'#1a49b8'); rc(cx_-px(12),Y0+px(850),px(24),px(10),.8,1,'#1a49b8',None,'#dfe7fb')
# katman 2: uc yuvalari YATAY (pence · yedek pence · bos)
tx(bm,Y0+px(655),'UÇ YUVALARI — yatay, yan yana',7,'middle','bold')
for k,(ad,dash) in enumerate((('PENÇE',None),('YEDEK PENÇE',None),('boş',' 4,3'))):
    x_=b0+px(30+k*225)
    rc(x_,Y0+px(670),px(205),px(110),1.2,3,'#999' if dash else '#111',dash)
    if not dash: rc(x_+px(60),Y0+px(690),px(85),px(30),1,2); ln(x_+px(75),Y0+px(720),x_+px(85),Y0+px(765),1.1); ln(x_+px(130),Y0+px(720),x_+px(120),Y0+px(765),1.1)
    tx(x_+px(102),Y0+px(772)+(0 if dash else 0),ad,6.5,'middle','bold','#999' if dash else '#111')
# katman 3: cop cekmecesi YATAY (boyu boyunca) 30-40 L
rc(b0+px(30),Y0+px(405),b1-b0-px(60),px(210),1.6,4)
ln(bm-25,Y0+px(600),bm+25,Y0+px(600),2.2)
tx(bm,Y0+px(485),'ÇÖP ÇEKMECESİ — yatay, 70×60×20 ≈ 40 L',8,'middle','bold')
not_(bm,Y0+px(540),'poşetli · öne çekilir, motorsuz · eleman HER GÜN',fs=6.8)
# katman 4: huni / birak-gec agzi
ln(b0+px(60),Y0+px(80),b0+px(200),Y0+px(380),1.6); ln(b1-px(60),Y0+px(80),b1-px(200),Y0+px(380),1.6); ln(b0+px(60),Y0+px(80),b1-px(60),Y0+px(80),1.6)
tx(bm,Y0+px(150),'HUNİ — robot bırakır, geçer',8,'middle','bold')
not_(bm,Y0+px(230),'ağız 58 · çekmeceye düşer',fs=7)
not_(bm,Y0+px(880)+8,'v7: hepsi YATAY — tepsi 8 · uçlar 14 · çöp 22 · huni 32 (kabin 70×84 aynı)',fs=6.5)

# ================= 3 TOPPING v10 (70x84 — herkesle ayni · cikislar ORTA KUME · on sira calisan + arka sira siradaki · bosluk 14 · gecis rafi 3 kat) =================
c0,c1=xs[2],xs[3]; cm2=(c0+c1)/2
tx(cm2,Y0+px(35),'SOĞUTMA (ÜSTTE) 15 — minibar sınıfı 1/12 HP · +3 °C · buzluk YOK',7.5,'middle','bold')
rc(c0+px(60),Y0+px(48),px(150),px(100),1.2,3); ci(c0+px(135),Y0+px(98),px(35),1)
rc(c0+px(240),Y0+px(48),px(220),px(100),1.2,3); tx(c0+px(350),Y0+px(103),'kondenser',6.5)
rc(c0+px(490),Y0+px(48),px(150),px(100),1.2,3); ci(c0+px(565),Y0+px(98),px(30),1)
ln(c0+px(15),Y0+px(160),c1-px(15),Y0+px(160),1,'#111','6,4')
tx(cm2,Y0+px(188),'ELEKTRİK 12 · PLC I/O · 4 step sürücü · 24 V',7.5,'middle','bold')
rc(c0+px(50),Y0+px(200),px(150),px(70),1.1,2); tx(c0+px(125),Y0+px(242),'PLC',7)
for i in range(4): rc(c0+px(225+i*70),Y0+px(200),px(55),px(70),1,2)
rc(c0+px(525),Y0+px(200),px(120),px(70),1.1,2); tx(c0+px(585),Y0+px(242),'PSU',7)
ln(c0+px(15),Y0+px(290),c1-px(15),Y0+px(290),1.6)
KY=300
# arka sira (siradaki, acik gri) · on sira: sol KASAR A · sag: SUCUK en onde, arkasinda KUSBASI/KAVURMA (orta) ve siradaki kucukler (sag)
kaset(c0+px(20),Y0+px(KY-16),px(320),px(250),'KAŞAR B (arka sıra)',dash='3,3',c='#aaa')
kaset(c0+px(365),Y0+px(KY-16),px(320),px(250),'SUCUK yedek (arka sıra)',dash='3,3',c='#aaa')
kaset(c0+px(525),Y0+px(KY-8),px(160),px(250),'sıradaki KAV/KUŞ',dash='4,3',c='#999')
kaset(c0+px(355),Y0+px(KY-6),px(165),px(250),'KAVURMA · KUŞBAŞI',dash='4,3',c='#777')
kaset(c0+px(10),Y0+px(KY),px(335),px(250),'KAŞAR A','35×42×25 · 15 kg')
kaset(c0+px(355),Y0+px(KY),px(335),px(250),'SUCUK (en ön)','35×21×25 · 10 kg')
CY=KY+320
# koniler ORTA HATTA (x 35) toplanir
ln(c0+px(15),Y0+px(KY+252),c0+px(300),Y0+px(CY-55),1.2); ln(c0+px(340),Y0+px(KY+252),c0+px(330),Y0+px(CY-55),1.2)
ln(c0+px(360),Y0+px(KY+252),c0+px(370),Y0+px(CY-55),1.2); ln(c0+px(685),Y0+px(KY+252),c0+px(400),Y0+px(CY-55),1.2)
# 4 cark ayni x'te (derinlikte arka arkaya) — onden ust uste gorunur: en ondeki (B sucuk) duz, digerleri kesik/kaydirilmis
for k,(dx,r,c_,dash) in enumerate(((-30,38,'#aaa','3,3'),(-15,38,'#999','4,3'),(15,55,'#777','4,3'),(0,40,'#111',None))):
    ci(c0+px(350+dx),Y0+px(CY-6*k),px(r),1.6 if not dash else 1,c_,dash)
    ln(c0+px(350+dx-16),Y0+px(CY+60),c0+px(350+dx-16),Y0+px(CY+150),1.3 if not dash else .9,c_,dash); ln(c0+px(350+dx+16),Y0+px(CY+60),c0+px(350+dx+16),Y0+px(CY+150),1.3 if not dash else .9,c_,dash)
for k in range(6):
    a=k*math.pi/3; ln(c0+px(350),Y0+px(CY),c0+px(350)+px(40)*math.cos(a),Y0+px(CY)+px(40)*math.sin(a),.9)
rc(c0+px(120),Y0+px(CY-20),px(45),px(40),1.1,2); tx(c0+px(142),Y0+px(CY+5),'M',7,'middle','bold')
rc(c0+px(540),Y0+px(CY-20),px(45),px(40),1.1,2); tx(c0+px(562),Y0+px(CY+5),'M ×4',6.5,'middle','bold')
tx(c0+px(350),Y0+px(CY+178),'4 ağız ORTA HATTA x 35 · derinlikte y 34·46·58·70 (önden üst üste)',6,'middle','bold','#b3452b')
FL=CY+120
ln(c0+px(15),Y0+px(FL),c1-px(15),Y0+px(FL),1.6)
tx(cm2,Y0+px(FL-8),'soğuk kabin tabanı · ağızlar 3 cm sarkar',6,'middle','','#888')
tray(c0+px(350),Y0+px(FL+95),kulp=True)
rc(c0+px(575),Y0+px(FL+55),px(55),px(28),1.1,2,'#1a49b8'); tx(c0+px(602),Y0+px(FL+73),'kilit',5.5,'middle','','#1a49b8')
tx(c0+px(120),Y0+px(FL+50),'AÇIK BOŞLUK 14',6,'middle','bold','#1a49b8')
tx(c0+px(120),Y0+px(FL+72),'③ ✓ yalnız ÖTELEME',6,'middle','bold','#1d7a4f')
GY=FL+140
ln(c0+px(15),Y0+px(GY),c1-px(15),Y0+px(GY),1,'#111','6,4')
tx(cm2,Y0+px(GY+22),'GEÇİŞ RAFI (ayrı soğuk bölme · 70×84) — 3 kat',7.5,'middle','bold','#1a49b8')
kaset(c0+px(10),Y0+px(GY+35),px(335),px(250),'KAŞAR C','dolu +3 (arkada D)')
kaset(c0+px(355),Y0+px(GY+35),px(335),px(250),'SUCUK yedek','+ boş yuvalar (arka)')
kaset(c0+px(10),Y0+px(GY+310),px(335),px(250),'BOŞ kasetler','biten → eleman toplar',dash=None,c='#555')
kaset(c0+px(355),Y0+px(GY+310),px(335),px(250),'BOŞ kasetler','',dash=None,c='#555')
kaset(c0+px(10),Y0+px(GY+585),px(680),px(250),'büyüme: 5. malzeme kasetleri (kıyma / zeytin) — 70×84',dash='4,3',c='#999')
not_(cm2,Y0+px(1832),'14 kaset: 4 çalışan + 4 sıradaki (üst) + 2 kaşar + sucuk + boşlar (geçiş rafı) · donmuşlar STORE −18',fs=6)

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
ci(b0+px(180),YT2+px(560),px(170),1.1,'#1a49b8','5,4'); ci(b0+px(520),YT2+px(560),px(170),1.1,'#1a49b8','5,4'); tx(bm,YT2+px(790),'tepsi rafı: 2 yan yana (üst, kesik)',7,'middle','','#1a49b8')
ci(bm,YT2+px(420),px(145),1.4); ci(bm,YT2+px(420),px(170),1.2,'#1a49b8','4,3')
not_(bm,YT2+px(890),"PZP-400 64×80 · üst plaka Ø29 · üstte 2 tepsi yan yana (kesik)")
# TOPPING ust v11: tepsi DONMEZ — agizlar orta hatta x 35 (y 34/46/58/70); kaset kati: sol kasar A(on)/B(arka), sag: sucuk(on)/yedek(arka), orta kav/kus, sag siradaki
def tk2(x,y,w,h,ad,alt='',front=True):
    c_='#111' if front else '#999'
    rc(c0+px(x)+2,YT2+px(y)+2,px(w)-4,px(h)-4,1.2 if front else 1,2,c_,None if front else '4,3')
    tx(c0+px(x+w/2),YT2+px(y+h/2)-1,ad,6.8 if w>200 else 6,'middle','bold',c_)
    if alt: tx(c0+px(x+w/2),YT2+px(y+h/2)+9,alt,5.5,'middle','',c_)
tk2(0,0,350,420,'KAŞAR B','sıradaki',False); tk2(350,0,350,210,'SUCUK yedek','',False)
tk2(350,210,170,210,'KAVURMA'); tk2(350,420,170,210,'KUŞBAŞI'); tk2(520,210,170,210,'sır. KAV','',False); tk2(520,420,170,210,'sır. KUŞ','',False)
tk2(0,420,350,420,'KAŞAR A','35×42'); tk2(350,630,350,210,'SUCUK','35×21')
rc(c0+px(170),YT2+px(170),px(360),px(670),1,0,'#1d7a4f','5,3')
for y_,ad in ((340,'C'),(460,'D'),(580,'A'),(700,'B')):
    ci(c0+px(350),YT2+px(y_),px(20),1.4,'#b3452b',None,'#fde3dc'); tx(c0+px(350),YT2+px(y_)+3,ad,6,'middle','bold','#b3452b')
ci(c0+px(350),YT2+px(580),px(140),.9,'#1d7a4f','4,3')
ci(c0+px(350),YT2+px(720),px(170),1.2,'#1a49b8','5,4'); rc(c0+px(335),YT2+px(890),px(30),px(120),1,1,'#1a49b8')
not_(cm2,YT2+px(890),'v11: tepsi DÖNMEZ → ağızlar orta hatta x 35 (C kav 34 · D kuş 46 · A kaşar 58 · B sucuk 70) · yeşil: C bölgesi + A için C-diski',fs=6.2)
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
tx(kx,ky,"KONTROL — istasyonlar arası uyum (4 Eyl 2026)",12,"start","bold","#b3452b")
K=[
 ("① ✓ STORE −18: 5. raf — 4 donmuş kaset (kav ×2 · kuş ×2); 1L sağa","→ kapak: çekmece modeli — kapak yok, her çekmece izoleli ön yüzlü (cevap)","#1d7a4f"),
 ("② OVEN kavite 40×40: tepsi Ø34 + kulp 12 = 46 → kapak kapanmaz","→ kavite derinliği 50 (dış 65 → 75) YA DA kulp 6 cm — KARAR","#b3452b"),
 ("③ ✓ TEPSİ DÖNMEZ (Kemal) → yalnız öteleme: ağızlar ORTA HATTA x 35, y 34·46·58·70","→ tepsi merkezi ağız etrafında r 14 tam daire çizer; izinli bölge x 17-53, y ≥17 → analiz v2","#1d7a4f"),
 ("④ ✓ PACK: bıçak yatay, önden ince; açık deste kalktı → şarjör 2×2×29 = 116 kutu","→ bıçak Ø28 + yuva pimleri","#1d7a4f"),
 ("⑤ PRESS üst plaka Ø40 → Ø29 (tepsi içinde basma)","→ Fersah'a kalıp/plaka sorusu","#b3452b"),
 ("⑥ ✓ PRESS v7 hepsi YATAY: tepsi 2 · uç yuvaları 3 · çöp çekmecesi 40 L · huni","→ 3 tepsi = fırında 2 + kolda 1; 70×84 aynı","#1d7a4f"),
 ("⑦ Kol sınıfı ≥12 kg (kaşar kaseti 15 kg) — UR16e / CRX-20iA/L","→ ray aynı","#9a6b1f"),
 ("⑧ ✓ TOPPING 70×84: kaset katı ÖN sıra çalışan + ARKA sıra sıradaki → tam dolu","→ 'çözülme alanı' yok: donmuş kaset arka sıradaki küçük yuvaya 1 gün önce gelir","#1d7a4f"),
 ("⑨ ✓ Dozaj boşluğu 14 · soğutma 15 (minibar sınıfı) · elektrik 12","→ kilit tepeye 8,5 cm, ağız 11 cm → 2,5 cm pay; düşme 6,5 cm","#1d7a4f"),
 ("⑩ OVEN sadeyağ: tank ÜSTTE + 12 V pompa 8 W (püskürtme basınç ister)","→ cazibe yalnız damlatır; çekmeceler kalktı → teneke stoğu ×3 (4 ay)","#9a6b1f"),
 ("⑪ 197 ✓ · 415 ✓ · derinlik 84 HER KABİN ✓ · TOPPING içi 27+25+21+14+83 = 170 + 15","→ STORE sol kolon 29+7+82+5+54 = 177 + 8 pay ✓","#1d7a4f"),
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
tx(X0,Y0-94,"AUTOKITCH — HAT v43 · TÜM İSTASYONLAR SON VERSİYON (4 Eyl 2026) — STORE v39 · PRESS v7 (yatay) · TOPPING v11 (70×84, tepsi dönmez, ağızlar orta hatta) · OVEN tank+pompa · PACK 116",15,"start","bold")
tx(X0,Y0-72,"Robot: tek kol (≥12 kg), uç değiştirici — TEPSİ ucu (pide press'ten kutuya kadar tepside, fırına tepsiyle) + PENÇE ucu (hamur · kutu · içecek · kaset). Mavi = tepsi Ø34. Kırmızı = KONTROL bulguları (sağ altta liste).",10.5,"start","","#555")
tx(X0,Y0-54,"Ölçüler cm. HER KABİN 70/65/140 × 197 × 84. Açık: ② fırın kavitesi 50 / kulp 6 · ⑤ Fersah Ø29 · STORE kapak modeli (cevap) — bu turda çözülen: ③ ④ ⑥ ⑧ ⑨ (yeşil)",10.5,"start","","#b3452b")

W=int(X0+px(T)+px(1420)); H=int(YT2+px(1860))
svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="#ffffff"/>'+''.join(E)+'</svg>')
OUT=r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\FULL_MAKINE\hat_on_gorunus_teknik_v43.svg"
io.open(OUT,'w',encoding='utf-8').write(svg)
print('yazildi:',OUT,'|',W,'x',H)
