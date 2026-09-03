# -*- coding: utf-8 -*-
"""v7 — govde 185 + ayak 12; buzluk raflari dolapla ayni aralikta (140); 385 cm hat."""
import io

S=0.3
X0,Y0=90,150
HG,HA=1850,120          # govde / ayak mm
M=[("HAMUR — ÇİFT SICAKLIK",1400),("PRES",700),("DOZAJ",700),("FIRIN",650),("KESİM+KUTU",700),("İÇECEK",600)]
T=sum(w for _,w in M)   # 3850
def px(mm): return mm*S
YT=Y0+px(HG); YZ=YT+px(HA)
E=[]
def ln(x1,y1,x2,y2,w=1.4): E.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#111" stroke-width="{w}"/>')
def rc(x,y,w,h,sw=1.4,rx=0): E.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="none" stroke="#111" stroke-width="{sw}"/>')
def ci(cx,cy,r,sw=1.4): E.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="#111" stroke-width="{sw}"/>')
def el(cx,cy,rx,ry,sw=1.4): E.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="none" stroke="#111" stroke-width="{sw}"/>')
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
def not_(x,y,s): tx(x,y,s,9.5,"middle","", "#555")

xs=[X0+px(sum(w for _,w in M[:i])) for i in range(7)]
for i,(_ad,_w) in enumerate(M):                                   # MODULER: her istasyon bagimsiz kabin
    _x=xs[i]
    rc(_x+2,Y0,px(_w)-4,px(HG),2.2,5)
    rc(_x+14,YT,12,px(HA),1.4); rc(_x+px(_w)-26,YT,12,px(HA),1.4)
ln(X0-46,YZ,X0+px(T)+70,YZ,2)

# A HAMUR CIFT SICAKLIK 1400 (cift kapili standart kasa)
a0,a1=xs[0],xs[1]; am=a0+px(700)
rc(a0+8,Y0+px(10),a1-a0-16,px(290),1.6)
ci(a0+px(350),Y0+px(140),px(80),1.2); ci(a0+px(1050),Y0+px(140),px(80),1.2)
ln(a0+px(310),Y0+px(100),a0+px(390),Y0+px(180),.9); ln(a0+px(310),Y0+px(180),a0+px(390),Y0+px(100),.9)
ln(a0+px(1010),Y0+px(100),a0+px(1090),Y0+px(180),.9); ln(a0+px(1010),Y0+px(180),a0+px(1090),Y0+px(100),.9)
for g in range(4): ln(a0+20,Y0+px(225)+g*px(15),a1-20,Y0+px(225)+g*px(15),.7)
rc(a0+8,Y0+px(310),a1-a0-16,px(1530),1.8)                         # TEK GOVDE
rc(am-px(35),Y0+px(310),px(70),px(1530),1.2)                      # izoleli ara bolme
rc(a0+px(60),Y0+px(370),am-px(35)-a0-px(60),px(1410),1)
for kz in range(19):
    ln(a0+px(60),Y0+px(420)+kz*px(70),a0+px(85),Y0+px(420)+kz*px(70),.8)
    ln(am-px(85),Y0+px(420)+kz*px(70),am-px(60),Y0+px(420)+kz*px(70),.8)
for r in range(10):
    ty=Y0+px(560)+r*px(126)
    ln(a0+px(72),ty,am-px(72),ty,1.2)
    ln(a0+px(72),ty,a0+px(72),ty-px(20),1.2); ln(am-px(72),ty,am-px(72),ty-px(20),1.2)
    rc((a0+a1)/2-px(80),ty+px(5),px(160),px(14),.9,2)
    for i in range(4):
        ci(a0+px(130)+i*px(125),ty-px(48),px(46),1)
        el(a0+px(130)+i*px(125),ty-px(2),px(56),px(8),.8)
not_((a0+a1)/2,Y0+px(58),"TEK PARÇA kombine dolap (standart) · soğutma ×2: sol −18° · sağ +3°")
not_((a0+am)/2,Y0+px(345),"DONMUŞ −18° · 10 raf × 20 ≈ 200 · aynı çukurlu tepsi")

# A2 sag yari: ILIK + TAZE + iade
a2,a3=am,xs[1]
ln(a2+12,Y0+px(310),a3-15,Y0+px(310),1)
ln(a2+15,Y0+px(590),a3-15,Y0+px(590),1)
ln(a2+px(70),Y0+px(448),a3-px(70),Y0+px(448),1)
for i in range(4): ci(a2+px(130)+i*px(125),Y0+px(395),px(50))
for i in range(4): ci(a2+px(130)+i*px(125),Y0+px(538),px(50))
ln(a2+px(35),Y0+px(600),a3-15,Y0+px(600),1.4)
rc(a2+px(40),Y0+px(655),a3-px(60)-a2-px(40),px(1130),1)
for kz in range(15):
    ln(a2+px(60),Y0+px(700)+kz*px(70),a2+px(85),Y0+px(700)+kz*px(70),.8)
    ln(a3-px(85),Y0+px(700)+kz*px(70),a3-px(60),Y0+px(700)+kz*px(70),.8)
for r in range(8):
    ty=Y0+px(795)+r*px(140)
    ln(a2+px(72),ty,a3-px(72),ty,1.2)
    ln(a2+px(72),ty,a2+px(72),ty-px(22),1.2); ln(a3-px(72),ty,a3-px(72),ty-px(22),1.2)
    rc((a2+a3)/2-px(80),ty+px(6),px(160),px(16),.9,2)
    for i in range(4):
        ci(a2+px(130)+i*px(125),ty-px(52),px(50),1)
        el(a2+px(130)+i*px(125),ty-px(3),px(58),px(9),.8)
not_((a2+a3)/2,Y0+px(345),"ılık AÇIK raf · 2×4")
not_((a2+a3)/2,Y0+px(638),"TAZE +3 °C · 8 raf × 20 ≈ 160 · çukurlu tepsi")

# B PRES 700 (PZP-400 64x80x95)
b0,b1=xs[1],xs[2]; bm=(b0+b1)/2
rc(bm-px(320),Y0+px(180),px(640),px(950),1.8)
ln(bm-px(120),Y0+px(240),bm-px(120),Y0+px(760),2.2); ln(bm+px(120),Y0+px(240),bm+px(120),Y0+px(760),2.2)
rc(bm-px(170),Y0+px(300),px(340),px(90),1.6)
rc(bm-px(170),Y0+px(640),px(340),px(70),1.6)
el(bm,Y0+px(760),px(140),7)
rc(b0+18,Y0+px(1210),b1-b0-36,px(620),1.6)                        # alt kabin
rc(b0+30,Y0+px(1300),px(300),px(35),1.4)                          # yedek el: kurek
ln(b0+30+px(300),Y0+px(1317),b0+30+px(380),Y0+px(1317),1.6)
rc(b0+30+px(400),Y0+px(1250),px(110),px(45),1.4)                  # pence
ln(b0+30+px(415),Y0+px(1295),b0+30+px(440),Y0+px(1370),1.4)
ln(b0+30+px(495),Y0+px(1295),b0+30+px(470),Y0+px(1370),1.4)
ln(b0+24,Y0+px(1400),b1-24,Y0+px(1400),1)
rc(b0+40,Y0+px(1420),px(400),px(370),1.4,3)                       # cop
ci(b0+40+px(90),Y0+px(1815),px(28),1); ci(b0+40+px(310),Y0+px(1815),px(28),1)
tx(b0+40+px(200),Y0+px(1620),"çöp 50 L",9.5,"middle","","#555")
not_(bm,Y0+px(168),"Fersah PZP-400 · 64×80×95")
not_(bm,Y0+px(800),"taban Ø28")
not_(bm,Y0+px(1240),"yedek kombine el: kürek + pençe")

# C DOZAJ 650 (2 onde + 1 arkada; tabla Ø40)
c0,c1=xs[2],xs[3]; cw=px(280)
for i in range(2):
    hx=c0+px(60)+i*(cw+px(20))
    rc(hx,Y0+px(70),cw,px(340),1.6)
    E.append(f'<path d="M {hx:.1f} {Y0+px(410):.1f} L {hx+cw/2-8:.1f} {Y0+px(550):.1f} h 16 L {hx+cw:.1f} {Y0+px(410):.1f}" fill="none" stroke="#111" stroke-width="1.6"/>')
    ln(hx+cw/2,Y0+px(550),hx+cw/2,Y0+px(670),2)
cm2=(c0+c1)/2
el(cm2,Y0+px(750),px(200),10,2); el(cm2,Y0+px(738),px(140),6)
ln(cm2,Y0+px(762),cm2,Y0+px(830),2.2); ln(c0+26,Y0+px(850),c1-26,Y0+px(850),1.6)
rc(c0+18,Y0+px(1100),c1-c0-36,px(730),1.6)                        # alt kabin
ln(c0+px(310),Y0+px(1100),c0+px(310),Y0+px(1830),1.2)
rc(c0+px(30),Y0+px(1230),px(250),px(380),1.4,4)                   # kompresor
ci(c0+px(155),Y0+px(1420),px(100),1.2)
for a in range(5): ln(c0+px(45),Y0+px(1660)+a*px(38),c0+px(265),Y0+px(1660)+a*px(38),.9)
for r in range(3):
    yk=Y0+px(1330)+r*px(230); ln(c0+px(320),yk,c1-8,yk,1)
    rc(c0+px(340),yk-px(200),px(265),px(200),1,2)
not_(cm2,Y0+px(58),"hazne 3×28 — 2 önde + 1 arkada")
not_(cm2,Y0+px(900),"döner tabla Ø40 · pide Ø28")
not_(cm2,Y0+px(1125),"soğutma motoru · GN 1/2 küvet ×9")

# D FIRIN 650 (ic 40x40; 2 kat + sprey nisi + yag rafi + cekmeceler)
d0,d1=xs[3],xs[4]
for k in range(2):
    ky=Y0+px(170)+k*px(540)
    rc(d0+px(25),ky,d1-d0-px(50),px(450),2)
    rc(d0+px(80),ky+px(70),d1-d0-px(160),px(300),1.4)
    ln(d0+px(25),ky+px(450),d1-px(25),ky+px(450),2.6)
dm=(d0+d1)/2
rc(d0+px(25),Y0+px(1180),d1-d0-px(50),px(190),1.6)                # sprey nisi
rc(dm-px(30),Y0+px(1180),px(60),px(50),1.4)
ln(dm,Y0+px(1230),dm,Y0+px(1255),1.6)
E.append(f'<line x1="{dm:.1f}" y1="{Y0+px(1255):.1f}" x2="{dm-px(110):.1f}" y2="{Y0+px(1335):.1f}" stroke="#111" stroke-width="1" stroke-dasharray="4 4"/>')
E.append(f'<line x1="{dm:.1f}" y1="{Y0+px(1255):.1f}" x2="{dm+px(110):.1f}" y2="{Y0+px(1335):.1f}" stroke="#111" stroke-width="1" stroke-dasharray="4 4"/>')
el(dm,Y0+px(1345),px(140),6)
rc(d0+18,Y0+px(1390),d1-d0-36,px(230),1.4)                        # yag rafi
for i in range(3): rc(d0+30+i*px(120),Y0+px(1425),px(100),px(160),1,2)
rc(d0+30+px(360),Y0+px(1425),px(120),px(160),1.4,2)               # pompa+isitici
E.append(f'<line x1="{d0+30+px(420):.1f}" y1="{Y0+px(1425):.1f}" x2="{d0+30+px(420):.1f}" y2="{Y0+px(1215):.1f}" stroke="#111" stroke-width="1" stroke-dasharray="3 4"/>')
E.append(f'<line x1="{d0+30+px(420):.1f}" y1="{Y0+px(1215):.1f}" x2="{dm+px(30):.1f}" y2="{Y0+px(1215):.1f}" stroke="#111" stroke-width="1" stroke-dasharray="3 4"/>')
for k in range(2):
    rc(d0+18,Y0+px(1650)+k*px(105),d1-d0-36,px(90),1.4)           # cekmeceler
    ln(dm-22,Y0+px(1650)+k*px(105)+px(45),dm+22,Y0+px(1650)+k*px(105)+px(45),2)
not_((d0+d1)/2,Y0+px(158),"APF-40-1 sınıfı · iç 40×40 · taş taban")
not_((d0+d1)/2,Y0+px(1172),"sadeyağ sprey nozülü + döner taban Ø28")
not_((d0+d1)/2,Y0+px(1412),"sadeyağ teneke ×3 + pompa·ısıtıcı")
not_((d0+d1)/2,Y0+px(1638),"servis çekmeceleri")

# E KESIM+KUTU 700 (80'lik sarjor + kucuk acik deste)
e0,e1=xs[4],xs[5]; em=(e0+e1)/2
ln(em,Y0+px(80),em,Y0+px(250),2.6); rc(em-15,Y0+px(140),30,px(90),1.6)
ci(em,Y0+px(420),px(150),2)
for dx,dy in [(0,1),(1,0),(0.71,0.71),(0.71,-0.71)]:
    ln(em-px(150)*dx,Y0+px(420)-px(150)*dy,em+px(150)*dx,Y0+px(420)+px(150)*dy,1.2)
el(em,Y0+px(600),px(150),8)
for r in range(20):
    for kx in (e0+8, e0+8+px(320)+4): rc(kx,Y0+px(680)+r*px(45),px(320),px(45),1.05)
rc(e0+8,Y0+px(1640),px(320)*2+4,px(190),1.4)                      # acik deste
for i in range(3): ln(e0+16,Y0+px(1680)+i*px(40),e0+196,Y0+px(1680)+i*px(40),.8)
not_(em,Y0+px(68),"piston + bıçak yıldızı Ø30")
not_(em,Y0+px(655),"kesim tablası Ø30")
not_(em,Y0+px(1618),"katlanmış: 2 cephe × 2 derin × 20 = 80")
not_(em,Y0+px(1815),"açık yatay deste ≈40 · koli dükkân rafında")

# F ICECEK 550 (6 kola / 5 sise / paketli)
f0,f1=xs[5],xs[6]
rc(f0+10,Y0+px(60),f1-f0-20,px(1000),1.6)
for yk in (px(300),px(540)):
    yv=Y0+yk; ln(f0+16,yv,f1-16,yv,1)
    for i in range(6): rc(f0+16+i*px(70),yv-px(118),px(66),px(115),1)
yv=Y0+px(995); ln(f0+16,yv,f1-16,yv,1)
for i in range(5): rc(f0+16+i*px(87),yv-px(305),px(90),px(300),1)
rc(f0+10,Y0+px(1080),f1-f0-20,px(480),1.6)
for r in range(2):
    yv2=Y0+px(1080)+px(220)+r*px(220); ln(f0+16,yv2,f1-16,yv2,1)
    for i in range(6): ci(f0+27+i*px(73),yv2-px(40),px(35),1)
rc(f0+10,Y0+px(1590),f1-f0-20,px(250),1.6)                        # MOTOR bolmesi (standart altta)
ci((f0+f1)/2,Y0+px(1715),px(85),1.2)
ln((f0+f1)/2-px(60),Y0+px(1655),(f0+f1)/2+px(60),Y0+px(1775),.9); ln((f0+f1)/2-px(60),Y0+px(1775),(f0+f1)/2+px(60),Y0+px(1655),.9)
for g in range(4): ln(f0+22,Y0+px(1620)+g*px(11),f0+70,Y0+px(1620)+g*px(11),.7)
for g in range(4): ln(f1-70,Y0+px(1620)+g*px(11),f1-22,Y0+px(1620)+g*px(11),.7)
not_((f0+f1)/2,Y0+px(48),"2 raf × 6 kola + 5 × 1L")
not_((f0+f1)/2,Y0+px(1068),"paketli tatlı / saçet · 2 raf")
not_((f0+f1)/2,Y0+px(1578),"soğutma grubu — standart alt bölme")

# ================= UST GORUNUM =================
def rd(x,y,w,h,sw=1.2):  # kesik cizgili dikdortgen (alt/ust seviye)
    E.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="none" stroke="#111" stroke-width="{sw}" stroke-dasharray="5 4"/>')
YT2=YZ+150
tx(X0,YT2-26,"ÜST GÖRÜNÜM",13,"start","bold")
for i,(_ad,_w) in enumerate(M):
    rc(xs[i]+2,YT2,px(_w)-4,px(840),2,5)

# HAMUR x2: iki kabin ayni tepsi duzeni + kapi
ln(am,YT2,am,YT2+px(840),1.4)
for (g0,g1) in ((a0,am),(am,a1)):
    rc(g0+px(60),YT2+px(60),g1-g0-px(120),px(700),1)
    rc(g0+px(85),YT2+px(85),px(530),px(650),1.4)
    ln(g0+px(75),YT2+px(85),g0+px(75),YT2+px(735),1); ln(g1-px(75),YT2+px(85),g1-px(75),YT2+px(735),1)
    for j in range(5):
        for i in range(4):
            ci(g0+px(150)+i*px(125),YT2+px(160)+j*px(125),px(50),1)
            ci(g0+px(150)+i*px(125),YT2+px(160)+j*px(125),px(60),.7)
    rc(g0+px(20),YT2+px(770),g1-g0-px(40),px(60),1.4)
    ci(g1-px(40),YT2+px(800),px(14),1.2)
    E.append(f'<path d="M {g0+px(20):.1f} {YT2+px(800):.1f} A {g1-g0-px(60):.1f} {g1-g0-px(60):.1f} 0 0 1 {g1-px(40):.1f} {YT2+px(800)+(g1-g0-px(60)):.1f}" fill="none" stroke="#111" stroke-width="1" stroke-dasharray="5 4"/>')
not_((a0+a1)/2,YT2+px(45),"tek kasa çift kapı: sol donmuş · sağ taze — tepsi 4×5=20 · kapı yayları")

# PRES: PZP govde 64x80, taban Ø28
rc(bm-px(320),YT2+px(20),px(640),px(800),1.6)
ci(bm,YT2+px(420),px(140),1.4)
not_(bm,YT2+px(890),"PZP-400 · 64×80")

# DOZAJ: 2 on + 1 arka silo, tabla alt seviyede (kesik)
ci(c0+px(200),YT2+px(620),px(140),1.6); ci(c0+px(500),YT2+px(620),px(140),1.6)
ci(cm2,YT2+px(260),px(140),1.6)
E.append(f'<circle cx="{cm2:.1f}" cy="{YT2+px(500):.1f}" r="{px(200):.1f}" fill="none" stroke="#111" stroke-width="1.2" stroke-dasharray="5 4"/>')
not_(cm2,YT2+px(890),"hazne 2 önde + 1 arkada · tabla altta (kesik)")

# FIRIN: govde + tas taban 40x40 (kesik, 2 kat)
rc(d0+px(25),YT2+px(120),d1-d0-px(50),px(620),1.6)
rd(dm-px(200),YT2+px(230),px(400),px(400))
not_((d0+d1)/2,YT2+px(890),"taş taban iç 40×40 · 2 kat üst üste")

# KESIM: bicak ustte, sarjor 2x2 altta (kesik)
ci(em,YT2+px(640),px(150),1.6)
for dx,dy in [(0,1),(1,0),(0.71,0.71),(0.71,-0.71)]:
    ln(em-px(150)*dx,YT2+px(640)-px(150)*dy,em+px(150)*dx,YT2+px(640)+px(150)*dy,1)
rd(e0+8,YT2+px(90),px(320),px(320)); rd(e0+8+px(320)+4,YT2+px(90),px(320),px(320))
rd(e0+8,YT2+px(430),px(320),px(320)); rd(e0+8+px(320)+4,YT2+px(430),px(320),px(320))
not_(em,YT2+px(890),"şarjör 2 cephe × 2 derin (altta) · bıçak önde")

# ICECEK: 6 egimli kanal derinlemesine
for i in range(7): ln(f0+16+i*px(70),YT2+px(60),f0+16+i*px(70),YT2+px(780),1)
for i in range(6):
    for j in range(3): ci(f0+16+px(35)+i*px(70),YT2+px(150)+j*px(250),px(30),.9)
not_((f0+f1)/2,YT2+px(890),"eğimli kanal ×6 — arkadaki öne kayar")

# ROBOT KORIDORU + RAY + CAM
ln(X0,YT2+px(840),X0,YT2+px(1740),1); ln(X0+px(T),YT2+px(840),X0+px(T),YT2+px(1740),1)
ry=YT2+px(1290)
ln(X0+px(200),ry-5,X0+px(T)-px(200),ry-5,1.6); ln(X0+px(200),ry+5,X0+px(T)-px(200),ry+5,1.6)
rc(cm2-px(160),ry-px(90),px(320),px(180),1.6,3)                   # ray arabasi
ci(cm2,ry,px(120),1.8)                                            # kol tabani
E.append(f'<path d="M {cm2-px(1300):.1f} {ry:.1f} A {px(1300):.1f} {px(1300):.1f} 0 0 1 {cm2+px(1300):.1f} {ry:.1f}" fill="none" stroke="#111" stroke-width="1" stroke-dasharray="6 5"/>')
tx(cm2+px(300),ry-14,"3-4 m ray · 7. eksen — kesik yay: kol erişimi (~130 cm)",9.5,"start","","#555")
ln(X0-30,YT2+px(1740),X0+px(T)+30,YT2+px(1740),2.4)
ln(X0-30,YT2+px(1762),X0+px(T)+30,YT2+px(1762),1)
tx(X0+px(T)/2,YT2+px(1815),"CAM VİTRİN — müşteri tarafı · kiosk + QR teslimat dolabı cam hattında",10,"middle","","#555")
ox(X0+px(T)+28,YT2,YT2+px(840),"84")
ox(X0+px(T)+28,YT2+px(840),YT2+px(1740),"90 koridor")

# OLCULER (cm)
for i,(ad,w) in enumerate(M):
    oy(xs[i],xs[i+1],Y0-24,str(round(w/10)))
    tx((xs[i]+xs[i+1])/2,YZ+24,ad,11.5,w="bold")
oy(X0,X0+px(T),YZ+52,"TOPLAM "+str(round(T/10))+" cm",12)
ox(X0-30,Y0,YT,str(round(HG/10)))
ox(X0-30,YT,YZ,str(round(HA/10)))
ox(X0-64,Y0,YZ,"TOPLAM "+str(round((HG+HA)/10)))
xr=X0+px(T)+28
ox(xr,Y0+px(170),Y0+px(620),"45"); ox(xr,Y0+px(710),Y0+px(1160),"45")
tx(X0,Y0-70,"AUTOKITCH — HAT v13 · MODÜLER · 475 × 197 × 84 cm",15,"start","bold")
tx(X0,Y0-50,"ölçüler cm · 3 GÜNDE BİR TESLİMAT (Pzt+Per) ~240 top · kapasite: donmuş 200 + taze 160 + ılık 8 ≈ 368 · hamur TEK PARÇA kombine dolap (140 — GN kombine sınıfı, standart ürün) · ayak 12",10.5,"start")

W=int(X0+px(T)+110); H=int(YT2+px(1860))
svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
     f'<rect width="{W}" height="{H}" fill="#ffffff"/>'+''.join(E)+'</svg>')
OUT=r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\hat_on_gorunus_teknik_v13.svg"
io.open(OUT,'w',encoding='utf-8').write(svg)
print('yazildi:',OUT,'|',W,'x',H)
