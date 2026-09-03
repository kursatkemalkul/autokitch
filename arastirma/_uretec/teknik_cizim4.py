# -*- coding: utf-8 -*-
"""v3 — internetten dogrulanmis standart olculerle cm olculendirmeli cizgi altligi."""
import io

S=0.3
X0,Y0=90,150
HG,HA=2050,150          # govde / ayak mm
M=[("HAMUR",600),("PRES",700),("DOZAJ",650),("FIRIN",650),("KESİM+KUTU",700),("İÇECEK",550)]
T=sum(w for _,w in M)   # 4400
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
rc(X0,Y0,px(T),px(HG),2.6,8)
for i in range(1,6): ln(xs[i],Y0,xs[i],YT,2)
for fx in [X0+15,X0+px(T)-27]+[xs[i]-6 for i in range(1,6)]: rc(fx,YT,12,px(HA),1.4)
ln(X0-46,YZ,X0+px(T)+70,YZ,2)

# A HAMUR 750 (GN600 sinifi 70x83,5x206,5; ic bolmeler 35/100/60)
a0,a1=xs[0],xs[1]
rc(a0+8,Y0+px(50),a1-a0-16,px(350),1.6)
ln(a0+15,Y0+px(225),a1-15,Y0+px(225),1)
for i in range(5): ci(a0+26+i*px(107),Y0+px(175),px(50))
for i in range(5): ci(a0+26+i*px(107),Y0+px(350),px(50))
rc(a0+8,Y0+px(430),a1-a0-16,px(1000),1.6)
for r in range(7):
    yv=Y0+px(430)+px(138)+r*px(138); ln(a0+15,yv,a1-15,yv,1)
    for i in range(5): ci(a0+26+i*px(107),yv-px(50),px(50),1)
rc(a0+8,Y0+px(1470),a1-a0-16,px(560),1.6)
for r in range(3):
    yv=Y0+px(1470)+px(186)+r*px(186)
    if r<2: ln(a0+15,yv,a1-15,yv,1)
    for i in range(5): ci(a0+26+i*px(107),yv-px(50),px(50),1)
not_((a0+a1)/2,Y0+px(418),"ılık raf · 2×5 top Ø10")
not_((a0+a1)/2,Y0+px(1458),"GN 2/1 derinlemesine · 7 raf ≈210 + rezerv ≈60")
tx(a0+14,Y0+px(70),"35",9.5,"start","", "#555"); tx(a0+14,Y0+px(450),"100",9.5,"start","", "#555"); tx(a0+14,Y0+px(1500),"60",9.5,"start","", "#555")

# B PRES 700 (Fersah PZP-400 64x80x95)
b0,b1=xs[1],xs[2]; bm=(b0+b1)/2
rc(bm-px(320),Y0+px(180),px(640),px(950),1.8)
ln(bm-px(120),Y0+px(240),bm-px(120),Y0+px(760),2.2); ln(bm+px(120),Y0+px(240),bm+px(120),Y0+px(760),2.2)
rc(bm-px(170),Y0+px(300),px(340),px(90),1.6)
rc(bm-px(170),Y0+px(640),px(340),px(70),1.6)
el(bm,Y0+px(760),px(140),7)
rc(b0+18,Y0+px(1300),b1-b0-36,px(720),1.6)
ln(b0+24,Y0+px(1560),b1-24,Y0+px(1560),1)
rc(b0+30,Y0+px(1460),px(300),px(35),1.4)
ln(b0+30+px(300),Y0+px(1477),b0+30+px(380),Y0+px(1477),1.6)
rc(b0+30+px(400),Y0+px(1400),px(110),px(45),1.4)
ln(b0+30+px(415),Y0+px(1445),b0+30+px(440),Y0+px(1530),1.4)
ln(b0+30+px(495),Y0+px(1445),b0+30+px(470),Y0+px(1530),1.4)
rc(b0+40,Y0+px(1580),px(400),px(380),1.4,3)
ln(b0+40,Y0+px(1650),b0+40+px(400),Y0+px(1650),1)
ci(b0+40+px(90),Y0+px(1990),px(30),1); ci(b0+40+px(310),Y0+px(1990),px(30),1)
tx(b0+40+px(200),Y0+px(1800),"çöp 50 L",9.5,"middle","","#555")
not_(bm,Y0+px(168),"Fersah PZP-400 · 64×80×95")
not_(bm,Y0+px(800),"taban Ø28")
not_(bm,Y0+px(1352),"yedek kombine el: kürek + pençe")

# C DOZAJ 900 (custom; hazne 3x28; tabla Ø40)
c0,c1=xs[2],xs[3]; cw=px(280)
for i in range(2):
    hx=c0+px(30)+i*(cw+px(20))
    rc(hx,Y0+px(70),cw,px(340),1.6)
    E.append(f'<path d="M {hx:.1f} {Y0+px(410):.1f} L {hx+cw/2-8:.1f} {Y0+px(550):.1f} h 16 L {hx+cw:.1f} {Y0+px(410):.1f}" fill="none" stroke="#111" stroke-width="1.6"/>')
    ln(hx+cw/2,Y0+px(550),hx+cw/2,Y0+px(670),2)
cm2=(c0+c1)/2
el(cm2,Y0+px(750),px(200),10,2); el(cm2,Y0+px(738),px(140),6)
ln(cm2,Y0+px(762),cm2,Y0+px(830),2.2); ln(c0+26,Y0+px(850),c1-26,Y0+px(850),1.6)
rc(c0+18,Y0+px(1100),c1-c0-36,px(920),1.6)
ln(c0+px(310),Y0+px(1100),c0+px(310),Y0+px(2020),1.2)
rc(c0+px(30),Y0+px(1300),px(250),px(420),1.4,4)
ci(c0+px(155),Y0+px(1510),px(100),1.2)
for a in range(5): ln(c0+px(45),Y0+px(1790)+a*px(45),c0+px(265),Y0+px(1790)+a*px(45),.9)
for r in range(3):
    yk=Y0+px(1400)+r*px(270); ln(c0+px(320),yk,c1-8,yk,1)
    rc(c0+px(340),yk-px(200),px(265),px(200),1,2)
not_(cm2,Y0+px(58),"hazne 3×28 — 2 önde + 1 arkada")
not_(cm2,Y0+px(900),"döner tabla Ø40 · pide Ø28")
not_(cm2,Y0+px(1160),"soğutma motoru · GN 1/2 küvet ×9")

# D FIRIN 700 (Atalay APF-40-1 sinifi; ic 40x40; 2 kat)
d0,d1=xs[3],xs[4]
for k in range(2):
    ky=Y0+px(170)+k*px(540)
    rc(d0+px(25),ky,d1-d0-px(50),px(450),2)
    rc(d0+px(80),ky+px(70),d1-d0-px(160),px(300),1.4)
    ln(d0+px(25),ky+px(450),d1-px(25),ky+px(450),2.6)
dm=(d0+d1)/2
rc(d0+px(25),Y0+px(1180),d1-d0-px(50),px(190),1.6)               # sprey nisi
rc(dm-px(30),Y0+px(1180),px(60),px(50),1.4)                       # nozul govdesi
ln(dm,Y0+px(1230),dm,Y0+px(1255),1.6)                             # nozul ucu
E.append(f'<line x1="{dm:.1f}" y1="{Y0+px(1255):.1f}" x2="{dm-px(110):.1f}" y2="{Y0+px(1335):.1f}" stroke="#111" stroke-width="1" stroke-dasharray="4 4"/>')
E.append(f'<line x1="{dm:.1f}" y1="{Y0+px(1255):.1f}" x2="{dm+px(110):.1f}" y2="{Y0+px(1335):.1f}" stroke="#111" stroke-width="1" stroke-dasharray="4 4"/>')
el(dm,Y0+px(1345),px(140),6)                                      # yuvarlak taban Ø28
rc(d0+18,Y0+px(1400),d1-d0-36,px(310),1.4)
for i in range(3): rc(d0+30+i*px(120),Y0+px(1460),px(100),px(215),1,2)
rc(d0+30+px(360),Y0+px(1460),px(120),px(215),1.4,2)
E.append(f'<line x1="{d0+30+px(420):.1f}" y1="{Y0+px(1460):.1f}" x2="{d0+30+px(420):.1f}" y2="{Y0+px(1215):.1f}" stroke="#111" stroke-width="1" stroke-dasharray="3 4"/>')
E.append(f'<line x1="{d0+30+px(420):.1f}" y1="{Y0+px(1215):.1f}" x2="{dm+px(30):.1f}" y2="{Y0+px(1215):.1f}" stroke="#111" stroke-width="1" stroke-dasharray="3 4"/>')
for k in range(2):
    rc(d0+18,Y0+px(1750)+k*px(150),d1-d0-36,px(120),1.4)
    ln(dm-22,Y0+px(1750)+k*px(150)+px(60),dm+22,Y0+px(1750)+k*px(150)+px(60),2)
not_((d0+d1)/2,Y0+px(158),"APF-40-1 sınıfı · iç 40×40 · taş taban")
not_((d0+d1)/2,Y0+px(1172),"sadeyağ sprey nozülü + döner taban Ø28")
not_((d0+d1)/2,Y0+px(1444),"sadeyağ teneke ×3 + pompa·ısıtıcı")
not_((d0+d1)/2,Y0+px(1738),"servis çekmeceleri")

# E KESIM+KUTU 700 (bicak Ø30; kutu 32x4,5 x20)
e0,e1=xs[4],xs[5]; em=(e0+e1)/2
ln(em,Y0+px(80),em,Y0+px(250),2.6); rc(em-15,Y0+px(140),30,px(90),1.6)
ci(em,Y0+px(420),px(150),2)
for dx,dy in [(0,1),(1,0),(0.71,0.71),(0.71,-0.71)]:
    ln(em-px(150)*dx,Y0+px(420)-px(150)*dy,em+px(150)*dx,Y0+px(420)+px(150)*dy,1.2)
el(em,Y0+px(600),px(150),8)
for r in range(16):
    for kx in (e0+8, e0+8+px(320)+4): rc(kx,Y0+px(700)+r*px(50),px(320),px(45),1.05)
rc(e0+8,Y0+px(1560),px(320)*2+4,px(400),1.4)
for i in range(9): ln(e0+16,Y0+px(1600)+i*px(40),e0+196,Y0+px(1600)+i*px(40),.8)
not_(em,Y0+px(68),"piston + bıçak yıldızı Ø30")
not_(em,Y0+px(660),"kesim tablası Ø30")
not_(em,Y0+px(1532),"katlanmış kutu 32×4,5 — 2×16 = 32")
not_(em,Y0+px(1995),"açık karton · yatay deste (64×45) ≈ 120")

# F ICECEK 650 (vitrin 60 sinifi; kola 6,6x11,5; 1L Ø9x31)
f0,f1=xs[5],xs[6]
rc(f0+10,Y0+px(60),f1-f0-20,px(1000),1.6)
for yk in (px(300),px(540),px(725)):
    yv=Y0+px(60)+yk-px(60); ln(f0+16,yv,f1-16,yv,1)
    for i in range(6): rc(f0+16+i*px(70),yv-px(118),px(66),px(115),1)
yv=Y0+px(60)+px(985); ln(f0+16,yv,f1-16,yv,1)
for i in range(5): rc(f0+16+i*px(87),yv-px(312),px(90),px(310),1)
rc(f0+10,Y0+px(1120),f1-f0-20,px(900),1.6)
for r in range(3):
    yv2=Y0+px(1120)+px(225)+r*px(225); ln(f0+16,yv2,f1-16,yv2,1)
    for i in range(6): ci(f0+27+i*px(73),yv2-px(40),px(35),1)
not_((f0+f1)/2,Y0+px(48),"3 raf × 6 kola + 5 × 1L")
not_((f0+f1)/2,Y0+px(1108),"paketli tatlı / saçet — 3 raf × 7")

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
tx(X0,Y0-70,"AUTOKITCH — HAT ÖN GÖRÜNÜŞÜ v4 · OPTİMUM GENİŞLİK",15,"start","bold")
tx(X0,Y0-50,"ölçüler cm · derinlik 84 · GN tepsi derinlemesine (raf başına 30 top) · hazne 2+1 · pres CP-330 seçilirse toplam 375",10.5,"start")

W=int(X0+px(T)+110); H=int(YZ+86)
svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
     f'<rect width="{W}" height="{H}" fill="#ffffff"/>'+''.join(E)+'</svg>')
OUT=r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\hat_on_gorunus_teknik_v4.svg"
io.open(OUT,'w',encoding='utf-8').write(svg)
print('yazildi:',OUT,'|',W,'x',H)
