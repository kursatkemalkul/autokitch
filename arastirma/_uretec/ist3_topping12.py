# -*- coding: utf-8 -*-
# TOPPING v12 — REVOLVER x2 (ust kat calisan · alt kat sira) + helezonlu pasif dilim · on gorunus / yan kesit / ust gorunus / ELEKTRIK & TAHRIK / stok / degisim
import io, math
W, H = 1460, 1130
o = []
def ln(x1,y1,x2,y2,w=1,c='#111',d=None):
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s stroke-linecap="round"/>' % (x1,y1,x2,y2,c,w,(' stroke-dasharray="%s"'%d) if d else ''))
def rc(x,y,w,h,sw=1,r=0,c='#111',d=None,f='none'):
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,w,h,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def ci(x,y,r,sw=1,c='#111',d=None,f='none'):
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def el(x,y,rx,ry,sw=1,c='#111',d=None,f='none'):
    o.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,rx,ry,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def tx(x,y,s,fs=9,anc='start',fw='',col='#111'):
    o.append('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="%s" font-weight="%s" fill="%s" font-family="Segoe UI, Arial, sans-serif">%s</text>' % (x,y,fs,anc,fw or 'normal',col,s))
def path(d,sw=1,c='#111',f='none',dash=None):
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="%s"%s stroke-linejoin="round"/>' % (d,f,c,sw,(' stroke-dasharray="%s"'%dash) if dash else ''))
def poly(pts,sw=1,c='#111',f='none',d=None):
    o.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (' '.join('%.1f,%.1f'%p for p in pts),f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def arr(x1,y1,x2,y2,c='#c0392b',w=1.2):
    ln(x1,y1,x2,y2,w,c); a=math.atan2(y2-y1,x2-x1)
    for s in (1,-1): ln(x2,y2,x2-6*math.cos(a-s*.42),y2-6*math.sin(a-s*.42),w,c)
def sector(cx,cy,r0,r1,a1,a2,sw=1,c='#111',f='#f1efe8'):
    p = lambda r,a: (cx+r*math.cos(math.radians(a)), cy+r*math.sin(math.radians(a)))
    x1,y1=p(r1,a1); x2,y2=p(r1,a2); x3,y3=p(r0,a2); x4,y4=p(r0,a1)
    path('M%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f Z' % (x1,y1,r1,r1,x2,y2,x3,y3,r0,r0,x4,y4),sw,c,f)

GRN, RED, BLU, GRY, AMB, PUR = '#1d7a4f', '#c0392b', '#1a49b8', '#666', '#b7791f', '#6b4fa8'
FILL, PU = '#f1efe8', '#e9e4d6'
K = 2.6
# dikey butce (ustten, cm)
Z = [('teknik',27,'#f3f3f3'),('panel',3,'#ddd'),('ÜST REVOLVER',33,'#fff'),('tahrik',8,'#eaf6ee'),('BOŞLUK',14,'#eef3ff'),('ALT REVOLVER',33,'#fff'),('tahrik',5,'#eaf6ee'),('RAF A',37,'#f7f6f2'),('RAF B',37,'#f7f6f2')]
assert sum(z[1] for z in Z)==197, sum(z[1] for z in Z)
zt = {}; acc=0
for ad,h,_ in Z:
    zt.setdefault(ad,[]).append((acc,h)); acc+=h

o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H))
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,42,'AUTOKITCH — İSTASYON 3 · TOPPING v12 (4 Eyl 2026) — ÇİFT REVOLVER: üst kat çalışan 8 dilim · alt kat sıra 8 dilim · helezonlu pasif dilim · 70 × 197 × 84 · ölçüler cm',15,'start','bold')
tx(30,66,'Kemal: "2 raf, üst kat alt kat" → alt revolver = sıra rafı; her yedek dilim de öne döner, robot iki katta tek noktadan çalışır. Tablalarda elektrik yok (slip ring yok): iki tabla motoru, bir dozaj motoru, üç yük hücresi, bir RFID — hepsi sabit gövdede.',9.5,'start','','#444')
ln(30,78,W-30,78,.8,'#999')

# ================= ÖN GÖRÜNÜŞ =================
X0,Y0 = 60,120
tx(X0+K*35,Y0-10,'ÖN GÖRÜNÜŞ (robot tarafı) 1:3,85',9,'middle','bold')
rc(X0,Y0,K*70,K*197,2.2)
zz=0
for ad,h,col in Z:
    rc(X0,Y0+K*zz,K*70,K*h,.8,0,'#111',None,col); zz+=h
# teknik: sogutma + elektrik
rc(X0+K*3,Y0+K*3,K*30,K*21,1,2,'#111',None,'#fff'); tx(X0+K*18,Y0+K*12,'SOĞUTMA',6.5,'middle','bold'); tx(X0+K*18,Y0+K*18,'1/12 HP · +3',5.6,'middle','')
rc(X0+K*37,Y0+K*3,K*30,K*21,1,2,'#111',None,'#fff'); tx(X0+K*52,Y0+K*10,'ELEKTRİK',6.5,'middle','bold'); tx(X0+K*52,Y0+K*15,'PLC · 24 V PSU',5.4,'middle',''); tx(X0+K*52,Y0+K*20,'4 sürücü',5.4,'middle','')
# ust revolver: dilim ustlerinin on gorunusu (on 3 dilim kesikli) + klape
z0=zt['ÜST REVOLVER'][0][0]
rc(X0+K*2,Y0+K*(z0+1),K*66,K*31,1.1,2,'#111','4,3','#fcfbf8')
for xx_,lab in ((35,'ÖN DİLİM'),(12,'yan'),(58,'yan')):
    rc(X0+K*(xx_-10),Y0+K*(z0+3),K*20,K*28,.8,1,'#999','3,2'); tx(X0+K*xx_,Y0+K*(z0+18),lab,5.6,'middle','bold' if xx_==35 else '','#333' if xx_==35 else '#999')
tx(X0+K*35,Y0+K*(z0+27),'motorlu izole klape (değişimde açılır)',5.2,'middle','',BLU)
tx(X0+K*70+6,Y0+K*(z0+16),'ÜST REVOLVER 33 · çalışan 8',6.5,'start','bold')
# tahrik kati (ust)
z1=zt['tahrik'][0][0]
rc(X0+K*27,Y0+K*(z1+1),K*16,K*6,1,1,'#111',None,'#eee'); tx(X0+K*35,Y0+K*(z1+5),'tabla M1',5.4,'middle','bold')
rc(X0+K*8,Y0+K*(z1+1),K*14,K*6,1,1,BLU,None,'#dfe7fb'); tx(X0+K*15,Y0+K*(z1+5),'dozaj M3',5.4,'middle','bold',BLU)
for xx_ in (5,35,65): ci(X0+K*xx_,Y0+K*(z1+7.2),2.2,1,AMB,None,'#fdf3dd')
tx(X0+K*70+6,Y0+K*(z1+5),'tahrik 8: M1 + M3 + yük hücresi ×3',6.5,'start','',GRY)
# bosluk + tepsi + cikis
z2=zt['BOŞLUK'][0][0]
ln(X0+K*35,Y0+K*(z2),X0+K*35,Y0+K*(z2+4),2,GRN); tx(X0+K*38,Y0+K*(z2+4),'ağız (35, 69)',5.6,'start','bold',GRN)
el(X0+K*35,Y0+K*(z2+11),K*17,K*1.2,1.2,BLU,None,'#dfe7fb'); tx(X0+K*35,Y0+K*(z2+9),'tepsi Ø34 (spiral)',5.4,'middle','',BLU)
tx(X0+K*70+6,Y0+K*(z2+8),'BOŞLUK 14 · ön açık · tabanı sabit plaka',6.5,'start','',BLU)
# alt revolver
z3=zt['ALT REVOLVER'][0][0]
rc(X0+K*2,Y0+K*(z3+1),K*66,K*31,1.1,2,'#111','4,3','#fcfbf8')
for xx_,lab in ((35,'SIRA DİLİMİ'),(12,'yan'),(58,'yan')):
    rc(X0+K*(xx_-10),Y0+K*(z3+3),K*20,K*28,.8,1,'#999','3,2'); tx(X0+K*xx_,Y0+K*(z3+18),lab,5.4,'middle','bold' if xx_==35 else '','#333' if xx_==35 else '#999')
tx(X0+K*35,Y0+K*(z3+27),'motorlu izole klape',5.2,'middle','',BLU)
tx(X0+K*70+6,Y0+K*(z3+16),'ALT REVOLVER 33 · sıra 8 (kaşar)',6.5,'start','bold')
z4=zt['tahrik'][1][0]
rc(X0+K*27,Y0+K*(z4+0.5),K*16,K*4,1,1,'#111',None,'#eee'); tx(X0+K*35,Y0+K*(z4+3.4),'tabla M2',5.2,'middle','bold')
tx(X0+K*70+6,Y0+K*(z4+3.5),'tahrik 5: M2 (dozaj yok)',6.5,'start','',GRY)
# raflar
for k,(ad,pair) in enumerate((('RAF A',('PARK (boş yuva)','BOŞ DİLİM yedek')),('RAF B',('KAVURMA çözülme','KUŞBAŞI çözülme')))):
    zr=zt[ad][0][0]
    for i,lab in enumerate(pair):
        x_=X0+K*(3+i*33)
        rc(x_,Y0+K*(zr+4),K*31,K*29,1,2,'#111' if 'PARK' not in lab else '#999',None if 'PARK' not in lab else '4,3',FILL if 'PARK' not in lab else '#fff')
        tx(x_+K*15.5,Y0+K*(zr+17),lab.split(' ')[0],6,'middle','bold'); tx(x_+K*15.5,Y0+K*(zr+23),' '.join(lab.split(' ')[1:]),5.2,'middle','','#333')
    tx(X0+K*70+6,Y0+K*(zr+18),'%s 37 · 2 yuva önden' % ad,6.5,'start','',GRY)
# olculer
ln(X0,Y0+K*197+16,X0+K*70,Y0+K*197+16,.8); tx(X0+K*35,Y0+K*197+28,'70',8,'middle','bold')
ln(X0-14,Y0,X0-14,Y0+K*197,.8); tx(X0-18,Y0+K*98,'197',8,'end','bold')
zz=0
for ad,h,_ in Z:
    tx(X0-18,Y0+K*(zz+h/2)+3,'%g'%h,5.4,'end','',GRY); zz+=h
tx(X0+K*35,Y0+K*197+42,'dikey: 27+3+33+8+14+33+5+37+37 = 197 ✓',7,'middle','bold',GRN)

# ================= YAN KESİT =================
XS,YS = 330,120
tx(XS+K*42,YS-10,'YAN KESİT (arka ← y → ön) 1:3,85',9,'middle','bold')
rc(XS,YS,K*84,K*197,2.2)
zz=0
for ad,h,col in Z:
    rc(XS,YS+K*zz,K*84,K*h,.8,0,'#111',None,col); zz+=h
rc(XS+K*2,YS+K*2,K*80,K*23,1,2,'#111',None,'#fff'); tx(XS+K*42,YS+K*14,'teknik: soğutma + elektrik (üstten servis)',5.8,'middle','')
for (zr,lab,dosaj) in ((z0,'üst',True),(z3,'alt',False)):
    # tabla O66 eksen y 40 → y 7..73; dilimler kesit: arka dilim y 7-35, gobek 35-45, on dilim 45-73
    rc(XS+K*7,YS+K*(zr+2),K*28,K*28,1.1,0,'#111',None,FILL); tx(XS+K*21,YS+K*(zr+16),'arka dilim',5.4,'middle','')
    rc(XS+K*45,YS+K*(zr+2),K*28,K*28,1.1,0,'#111',None,'#dff3e6' if dosaj else FILL); tx(XS+K*59,YS+K*(zr+14),'ön dilim',5.4,'middle','bold' if dosaj else '')
    if dosaj: tx(XS+K*59,YS+K*(zr+19),'(dozajda)',5,'middle','',GRN)
    rc(XS+K*35,YS+K*(zr+2),K*10,K*28,.8,0,'#111',None,'#ddd'); tx(XS+K*40,YS+K*(zr+16),'göbek',4.6,'middle','',GRY)
    rc(XS+K*7,YS+K*(zr+30),K*66,K*2,1,0,'#111',None,'#bbb')
    # helezon on dilimde (yatay, radyal) + agiz dis ucta
    ln(XS+K*52,YS+K*(zr+28),XS+K*70,YS+K*(zr+28),1.4,'#333')
    for k in range(7): ln(XS+K*(53+k*2.5),YS+K*(zr+26.5),XS+K*(53+k*2.5),YS+K*(zr+29.5),.7,'#111')
    tx(XS+K*61,YS+K*(zr+25),'helezon',4.8,'middle','',GRY)
    # klape (on)
    rc(XS+K*82,YS+K*(zr+1),K*2,K*31,1,0,BLU,None,'#dfe7fb'); tx(XS+K*84+4,YS+K*(zr+8),'klape',5.2,'start','',BLU)
    # yalitim kutusu
    rc(XS+K*1,YS+K*(zr+0.5),K*82,K*32,.9,2,'#111','3,2')
# ust tahrik: kavrama on dilim ic ucunda (y 50), tabla motoru gobek altinda (y 40), yuk hucreleri
rc(XS+K*35,YS+K*(z1+1),K*10,K*6,1,1,'#111',None,'#eee'); tx(XS+K*40,YS+K*(z1+5),'M1',5,'middle','bold')
rc(XS+K*47,YS+K*(z1+1),K*8,K*6,1,1,BLU,None,'#dfe7fb'); tx(XS+K*51,YS+K*(z1+5),'M3',5,'middle','bold',BLU)
arr(XS+K*51,YS+K*(z1+1),XS+K*51,YS+K*(z1-1.5),BLU,1.1); tx(XS+K*56,YS+K*(z1+2),'pençe kavrama ↑ dilim iç ucu',4.8,'start','',BLU)
for yy_ in (12,40,68): ci(XS+K*yy_,YS+K*(z1+7.2),2.2,1,AMB,None,'#fdf3dd')
tx(XS+K*84+4,YS+K*(z1+6),'yük hücresi ×3 (tabla toplam)',5.2,'start','',AMB)
# bosluk: agiz y 69 → tepsi
ln(XS+K*69,YS+K*(z2),XS+K*69,YS+K*(z2+3.5),2,GRN); tx(XS+K*69,YS+K*(z2-1.5),'ağız y 69',5.2,'middle','bold',GRN)
rc(XS+K*38,YS+K*(z2+10.5),K*34,K*1.5,1.1,BLU,None,'#dfe7fb'); rc(XS+K*72,YS+K*(z2+9.5),K*12,K*3,1,BLU,None,'#dfe7fb')
tx(XS+K*50,YS+K*(z2+8.5),'tepsi en geride (m. y 55)',4.8,'middle','',BLU)
rc(XS,YS+K*(z2+12),K*84,K*2,1,0,'#111',None,'#bbb'); tx(XS+K*84+4,YS+K*(z2+13),'boşluk tabanı (sabit plaka)',5.2,'start','',GRY)
rc(XS+K*35,YS+K*(z4+0.5),K*10,K*4,1,1,'#111',None,'#eee'); tx(XS+K*40,YS+K*(z4+3.4),'M2',5,'middle','bold')
# raflar (yan): tek yuva derinlikte
for ad in ('RAF A','RAF B'):
    zr=zt[ad][0][0]
    rc(XS+K*50,YS+K*(zr+4),K*30,K*29,1,2,'#111',None,FILL); tx(XS+K*65,YS+K*(zr+19),'dilim',5.4,'middle','')
    tx(XS+K*25,YS+K*(zr+19),'arka: boş (erişim yok)',5,'middle','',GRY)
ln(XS,YS+K*197+16,XS+K*84,YS+K*197+16,.8); tx(XS+K*42,YS+K*197+28,'84',8,'middle','bold')
tx(XS+K*42,YS+K*197+42,'her iki revolver izole kutuda, önden klapeli; boşluk soğuk hacmin DIŞINDA',6.5,'middle','','#333')

# ================= ÜST GÖRÜNÜŞ (üst revolver) =================
XU,YU = 640,120
tx(XU+K*35,YU-10,'ÜST GÖRÜNÜŞ — üst revolver (çalışan)',9,'middle','bold')
rc(XU,YU,K*70,K*84,1.6)
cx,cy = XU+K*35, YU+K*40
ci(cx,cy,K*33.5,1.3,'#111',None,'#f7f7f7')
names=['KAŞAR 1','KUŞBAŞI','KAŞAR 2','SUCUK 1','KAŞAR 3','KAVURMA','KAŞAR 4','SUCUK 2']
for i,ad in enumerate(names):
    a1=67.5+i*45; am=math.radians(a1+22.5)
    sector(cx,cy,K*5,K*33,a1,a1+45,.9,'#111',FILL if 'KAŞAR' in ad else '#e8eef8')
    tx(cx+K*24*math.cos(am),cy+K*24*math.sin(am)+2,ad,4.6,'middle','bold')
ci(cx,cy,K*5,.9,'#111',None,'#ddd')
ci(XU+K*35,YU+K*69,K*31,.9,GRN,'5,3'); ci(XU+K*35,YU+K*69,3.2,1.4,GRN,None,'#fff')
tx(XU+K*35,YU+K*78,'ağız (35, 69) · süpürme R31 ✓',5.4,'middle','bold',GRN)
rc(XU+K*31,YU,K*8,K*84,0,0,'none',None,'#dff3e6')
tx(XU+K*35,YU+K*84+12,'70',7,'middle','bold')
# alt revolver plan (kucuk)
YU2 = YU+K*84+40
tx(XU+K*35,YU2-8,'alt revolver (sıra) — 8 × kaşar',7.5,'middle','bold')
rc(XU,YU2,K*70,K*84,1.2)
cx2,cy2 = XU+K*35, YU2+K*40
ci(cx2,cy2,K*33.5,1.1,'#111',None,'#f7f7f7')
for i in range(8):
    a1=67.5+i*45; am=math.radians(a1+22.5)
    sector(cx2,cy2,K*5,K*33,a1,a1+45,.8,'#111',FILL)
    tx(cx2+K*24*math.cos(am),cy2+K*24*math.sin(am)+2,'KAŞAR %d'%(i+5),4.4,'middle','bold')
ci(cx2,cy2,K*5,.9,'#111',None,'#ddd')
arr(cx2,cy2+K*74,cx2,cy2+K*82,BLU,1.1); tx(cx2,cy2+K*90,'öne döner → robot çeker',5.4,'middle','',BLU)
# raf plan
YU3 = YU2+K*84+52
tx(XU+K*35,YU3-8,'RAF A / B planı — 2 yuva yan yana, önden',7.5,'middle','bold')
rc(XU,YU3,K*70,K*84,1.2)
for i,lab in enumerate(('PARK','BOŞ yedek')):
    sector(XU+K*(18+i*34),YU3+K*30,K*5,K*33,67.5,112.5,.9,'#111' if i else '#999',FILL if i else '#fff')
    tx(XU+K*(18+i*34),YU3+K*55,lab,5.4,'middle','bold')
tx(XU+K*35,YU3+K*78,'RAF B: kavurma / kuşbaşı çözülme (STORE −18'+chr(39)+'den 1 gün önce)',5,'middle','','#333')

# ================= ELEKTRİK & TAHRİK =================
XE,YE = 870,120
rc(XE,YE,560,470,1.4,4,'#111',None,'#fcfdff')
tx(XE+14,YE+22,'ELEKTRİK & TAHRİK — "rotor nasıl elektriklenecek?"',10,'start','bold')
tx(XE+14,YE+38,'Cevap: dilimde elektrik yok. Helezon + tarak dilimin içinde pasif; döndüren motor sabit gövdede, tabla durunca kavrar.',7,'start','','#333')
# kavrama detayi (sol)
kx,ky = XE+20,YE+60
rc(kx,ky,250,190,1,3,'#999',None,'#fff')
tx(kx+125,ky+14,'PENÇE KAVRAMA (dog clutch)',7,'middle','bold')
# dilim tabani + konik disli + helezon mili
rc(kx+20,ky+30,210,44,1,0,'#111',None,FILL); tx(kx+125,ky+40,'dilim (pasif)',5.8,'middle','',GRY)
ln(kx+60,ky+56,kx+220,ky+56,1.6,'#333'); tx(kx+150,ky+52,'helezon mili (yatay)',5.2,'middle','')
poly([(kx+50,ky+48),(kx+62,ky+56),(kx+50,ky+64)],1,'#555','#eee'); poly([(kx+38,ky+64),(kx+50,ky+52),(kx+50,ky+76)],1,'#555','#eee')
tx(kx+30,ky+46,'konik',5,'end','','#555')
rc(kx+44,ky+74,12,10,1.1,1,BLU,None,'#dfe7fb'); tx(kx+62,ky+82,'dişli pençe (dilim altı, r 11)',5.2,'start','bold',BLU)
rc(kx+20,ky+84,210,8,1,0,'#111',None,'#bbb'); tx(kx+236,ky+90,'tabla',5,'start','',GRY)
rc(kx+44,ky+92,12,10,1.1,1,BLU,None,'#dfe7fb'); tx(kx+62,ky+100,'karşı pençe — yaylı, pahlı (kendi hizalar)',5.2,'start','',BLU)
rc(kx+36,ky+104,28,34,1.1,2,'#111',None,'#eee'); tx(kx+50,ky+118,'M3',6,'middle','bold'); tx(kx+50,ky+128,'24 V',4.6,'middle','')
tx(kx+72,ky+118,'dozaj motoru 40 W · enkoder',5.4,'start','bold'); tx(kx+72,ky+130,'tabla dönerken pençe aşağı basılır,',5,'start','','#333'); tx(kx+72,ky+140,'hizalanınca yayla yukarı çıkar, kilitler',5,'start','','#333')
arr(kx+50,ky+150,kx+50,ky+140,BLU,1.1)
tx(kx+125,ky+170,'M3 tek yön döner → helezon + (1:20) tarak',5.6,'middle','bold',BLU); tx(kx+125,ky+182,'geri dönüş yok: helezon boşalmaz, doz sıfırdan başlar',5,'middle','','#333')
# blok sema (sag)
bx,by = XE+290,YE+60
rc(bx,by,250,190,1,3,'#999',None,'#fff')
tx(bx+125,by+14,'KONTROL ŞEMASI',7,'middle','bold')
rc(bx+80,by+24,90,26,1.2,3,'#111',None,'#f3f3f3'); tx(bx+125,by+35,'PLC / kontrolör',6,'middle','bold'); tx(bx+125,by+45,'24 V bus · CAN',4.8,'middle','')
items=[('M1 üst tabla',BLU),('M2 alt tabla',BLU),('M3 dozaj',BLU),('klape ×2',BLU),('yük hücresi ×3',AMB),('index sensör ×2',AMB),('RFID okuyucu',PUR),('soğutma +3',GRY)]
for i,(ad,col) in enumerate(items):
    col_=i%2; row=i//2
    x_=bx+12+col_*122; y_=by+62+row*30
    rc(x_,y_,112,22,1,2,col,None,'#fff'); tx(x_+56,y_+14,ad,5.6,'middle','bold',col)
    ln(bx+125,by+50,x_+56,y_,.6,'#999')
tx(bx+125,by+182,'tablada kablo yok → slip ring yok, dilim yıkanır',5.4,'middle','bold',GRN)
# calisma sirasi
ny=YE+262
tx(XE+14,ny,'DOZAJ ÇEVRİMİ (bir pide, kaşar + kavurma)',8,'start','bold')
seq=['① sipariş: PLC dilim haritasına bakar (RFID + sayaç) → KAŞAR en yakın, M1 ≤ 45° döner, index sensör durdurur (±1 mm)',
     '② M3 pençesi kendi hizalanır → yük hücreleri tabla ağırlığını okur (W0) → M3 döner, helezon dış uçtan tepsiye döker; robot spiral (14 sn)',
     '③ W0 − W = 80 g olunca M3 durur (±3 g) · sayaç: dilim kalan −80 g · sonra KAVURMA: M1 döner, aynı çevrim 35 g',
     '④ dilim kalan ≤ 1 doz ya da saat doldu → değişim: M2 alt tablada dolu kaşarı öne getirir (bkz. sağ alt)',
     '⑤ hata: pençe kavramazsa (enkoder dönmüyor) M1 ±2° titretir; yine olmazsa dilim "arızalı" → değişim']
for i,s in enumerate(seq): tx(XE+14,ny+16+i*13,s,6.6,'start','','#333')
tx(XE+14,ny+90,'güç: M1/M2 60 W · M3 40 W · klape 2×10 W · soğutma 90 W · PLC 15 W → ~275 W tepe, ortalama ~120 W',6.6,'start','bold',GRY)
tx(XE+14,ny+104,'M1 hız: 45° 1,5 sn · M3: 30 dev/dk (80 g = 4 tur = 8 sn, spiral 14 sn içinde) · index: 8 pim + endüktif sensör',6.6,'start','','#333')

# ================= STOK + DEĞİŞİM =================
XT,YT = 870,610
rc(XT,YT,560,300,1.4,4)
tx(XT+14,YT+22,'STOK · DEĞİŞİM · HAFTALIK',10,'start','bold')
rows=[('ÜST (çalışan)','kaşar ×4 (16 kg · 2,5 gün) · sucuk ×2 (10 kg · hafta) · kavurma ×1 · kuşbaşı ×1','#111'),
      ('ALT (sıra)','kaşar ×8 (32 kg) → toplam kaşar 12 dilim = 48 kg = 7,4 gün ✓ (6,5 kg/gün)','#111'),
      ('RAF A','PARK boş yuva (değişimde ara durak) + boş dilim yedek','#111'),
      ('RAF B','kavurma / kuşbaşı çözülme: STORE −18'+chr(39)+'den 1 gün önce buraya (2 donmuş yedek STORE'+chr(39)+'da)','#111'),
      ('ELEMAN (haftada 1)','12 dolu kaşar dilimi getirir (alt 8 + üst 4), 2 sucuk, 1+1 taze küçük; boşları alır; helezonlu dilimleri yıkar',GRN)]
for i,(a,b,c) in enumerate(rows):
    yy=YT+46+i*18; tx(XT+14,yy,a,7,'start','bold',c); tx(XT+130,yy,b,6.6,'start','',c)
ln(XT+12,YT+140,XT+548,YT+140,.8,'#bbb')
tx(XT+14,YT+158,'DEĞİŞİM (kaşar boşaldı, ≤ 2 kez/gün, ~2 dk, kuyruk boşken):',7.5,'start','bold',BLU)
seq2=['① M1: boş dilim öne · üst klape açılır · robot pençeyle dilimi çeker → RAF A PARK yuvasına koyar',
      '② M2: dolu kaşar öne · alt klape açılır · robot çeker → üst revolvere sürer (pençe kavrar, RFID okur, tartılır = W başlangıç)',
      '③ robot PARK'+chr(39)+'taki boşu alır → alt revolverdeki boşalan yuvaya sürer · klapeler kapanır · 6 hamle',
      '④ küçükler: RAF B'+chr(39)+'deki çözülmüş dilim ↔ üstteki boş; sucuk: haftalık eleman']
for i,s in enumerate(seq2): tx(XT+14,YT+174+i*13,s,6.6,'start','','#333')
tx(XT+14,YT+236,'Neden alt revolver (Kemal'+chr(39)+'in "2 raf" fikri): 8 yedek de öne döner → robot tek noktadan çalışır, FIFO derinlik kısıtı yok;',6.6,'start','bold',GRN)
tx(XT+14,YT+249,'sabit geçiş rafı 3 kat → 2 kat (park + çözülme) · bedel: 2. tabla + M2 (~60 W) · alt tabla dozaj yapmaz, kavrama yok',6.6,'start','','#333')
tx(XT+14,YT+270,'Dilim: 45° · 418 cm² · h 28 · ~10 L · kaşar ~4 kg · helezon Ø7 r 12-30 · tarak · ağız dış uçta · pençe iç uçta · RFID · boş 1,4 kg',6.4,'start','',GRY)
tx(XT+14,YT+284,'Açık: klape contası, soğuk hacimde helezon donması (+3 °C, yağlı peynir OK), dilim RFID yeri, M3 pençe pah açısı — prototip',6.4,'start','',GRY)

# ================= KONTROL (alt) =================
YK=940
rc(60,YK,1370,160,1.6,4)
tx(76,YK+24,'KONTROL — v11 → v12 farkları ve HAT v45 etkisi',11,'start','bold')
rows=[('① kaset katı → ÇİFT REVOLVER: üst çalışan (dozaj) + alt sıra (yedek); geçiş rafı 3 kat → 2 kat (park + çözülme)',GRN),
      ('② dozaj: 4 sabit ağız orta hatta (v11) → TEK ağız (35, 69), dilim öne döner; çark katı 21 → 8; boru/huni yok',GRN),
      ('③ dilim pasif (helezon + tarak içinde, pençe kavrama dışında); tablada elektrik yok; motorlar M1 M2 M3 + klape ×2 sabit gövdede',GRN),
      ('④ dikey 27+3+33+8+14+33+5+37+37 = 197 ✓ · 70 × 84 aynı · robot kolu: dilim dolu ≤ 6 kg ✓ (12 kg sorunu kapandı)',GRN),
      ('⑤ STORE v4: −18 kaset çekmecesi 29 ≥ dilim 28 ✓ değişiklik yok · HAT v45: TOPPING bloğu bu çizimle değişir, KONTROL ⑧⑨ güncellenir',BLU),
      ('⑥ AÇIK: kaşar 45° V + helezon akışı prototip · klape/soğuk hacim · sucuk dilimi = çubuk + bıçak (ayrı çizim) · tabla rulmanı seçimi',AMB)]
for i,(s,c) in enumerate(rows):
    tx(76+(i%2)*690,YK+48+(i//2)*34,s[:118],7.2,'start','',c)
    if len(s)>118: tx(76+(i%2)*690,YK+48+(i//2)*34+12,s[118:],7.2,'start','',c)
tx(W-40,H-12,'AUTOKITCH · arastirma/3_TOPPING/ist3_topping_detay_v12 · 4 Eyl 2026',7,'end','',GRY)
o.append('</svg>')
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\ist3_topping_detay_v12.svg"
io.open(out,'w',encoding='utf-8').write(chr(10).join(o))
print('yazildi', out)
