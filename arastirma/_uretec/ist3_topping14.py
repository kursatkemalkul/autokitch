# -*- coding: utf-8 -*-
# TOPPING v14 — TEK REVOLVER + C-ŞEKLİ DİLİM (45° sektör, helezon, tarak, V-oluk, ağız dış uçta) DOĞRUDAN KULLANILDI · geçiş rafı 3 kat · elektrik & tahrik
import io, math, xml.dom.minidom
W, H = 1460, 1150
o = []
def esc(s): return str(s).replace('&','&amp;').replace('<','&lt;')
def ln(x1,y1,x2,y2,w=1,c='#111',d=None):
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s stroke-linecap="round"/>' % (x1,y1,x2,y2,c,w,(' stroke-dasharray="%s"'%d) if d else ''))
def rc(x,y,w,h,sw=1,r=0,c='#111',d=None,f='none'):
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,w,h,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def ci(x,y,r,sw=1,c='#111',d=None,f='none'):
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def el(x,y,rx,ry,sw=1,c='#111',d=None,f='none'):
    o.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,rx,ry,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def tx(x,y,s,fs=9,anc='start',fw='',col='#111'):
    o.append('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="%s" font-weight="%s" fill="%s" font-family="Segoe UI, Arial, sans-serif">%s</text>' % (x,y,fs,anc,fw or 'normal',col,esc(s)))
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
def carc(cx,cy,r,a1,a2,c='#1a49b8',sw=1.1):
    p=lambda a:(cx+r*math.cos(math.radians(a)),cy+r*math.sin(math.radians(a)))
    x1,y1=p(a1); x2,y2=p(a2)
    path('M%.1f,%.1f A%.1f,%.1f 0 %d 1 %.1f,%.1f'%(x1,y1,r,r,1 if abs(a2-a1)>180 else 0,x2,y2),sw,c)
    a=math.radians(a2+90)
    for s in (1,-1): ln(x2,y2,x2-6*math.cos(a-s*.42),y2-6*math.sin(a-s*.42),sw,c)

GRN, RED, BLU, GRY, AMB, PUR = '#1d7a4f', '#c0392b', '#1a49b8', '#666', '#b7791f', '#6b4fa8'
FILL, MAT, SUC = '#f1efe8', '#e9dfa8', '#e8eef8'
K = 2.5
Z = [('teknik',27,'#f3f3f3'),('panel',4,'#ddd'),('REVOLVER',33,'#fff'),('tahrik',8,'#eaf6ee'),('BOŞLUK',14,'#eef3ff'),('RAF 1',37,'#f7f6f2'),('RAF 2',37,'#f7f6f2'),('RAF 3',37,'#f7f6f2')]
assert sum(z[1] for z in Z)==197
zt={}; acc=0
for ad,h,_ in Z: zt[ad]=acc; acc+=h
zR,zT,zB = zt['REVOLVER'],zt['tahrik'],zt['BOŞLUK']
NAMES = ['KAŞAR 1','KUŞBAŞI','KAŞAR 2','SUCUK 1','KAŞAR 3','KAVURMA','KAŞAR 4','SUCUK 2']

o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H))
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,42,'AUTOKITCH — İSTASYON 3 · TOPPING v14 (4 Eyl 2026) — TEK REVOLVER · C-ŞEKLİ DİLİM (45° sektör: V-oluk + helezon + tarak, ağız dış uçta) · geçiş rafı 3 kat (üst / orta / alt) · 70 × 197 × 84 · cm',15,'start','bold')
tx(30,66,'v5-C dilimi olduğu gibi kullanıldı: kutu yok. Tabla Ø66, 8 dilim; öne dönen dilimin ağzı hep (35, 69). Dilimde elektrik yok — helezon+tarak içeride, pençe kavrama iç uçta; motorlar sabit gövdede. Yedekler altta 3 kat sabit rafta (12 yuva), her yuva önden.',9.5,'start','','#444')
ln(30,78,W-30,78,.8,'#999')

# ================= ÖN GÖRÜNÜŞ =================
X0,Y0 = 60,120
tx(X0+K*35,Y0-10,'ÖN GÖRÜNÜŞ (robot tarafı) 1:4',9,'middle','bold')
rc(X0,Y0,K*70,K*197,2.2)
zz=0
for ad,h,col in Z:
    rc(X0,Y0+K*zz,K*70,K*h,.8,0,'#111',None,col); zz+=h
rc(X0+K*3,Y0+K*3,K*30,K*21,1,2,'#111',None,'#fff'); tx(X0+K*18,Y0+K*12,'SOĞUTMA',6.5,'middle','bold'); tx(X0+K*18,Y0+K*18,'1/12 HP · +3',5.6,'middle','')
rc(X0+K*37,Y0+K*3,K*30,K*21,1,2,'#111',None,'#fff'); tx(X0+K*52,Y0+K*10,'ELEKTRİK',6.5,'middle','bold'); tx(X0+K*52,Y0+K*15,'PLC · 24 V PSU',5,'middle',''); tx(X0+K*52,Y0+K*20,'3 sürücü',5,'middle','')
# revolver: on dilim dis yuzu (kiris 25,3) + yan dilimler
rc(X0+K*2,Y0+K*(zR+1),K*66,K*31,1,2,'#111','4,3','#fcfbf8')
for (xa,xb,lab) in ((4.5,22.4,'yan'),(47.6,65.5,'yan')):
    rc(X0+K*xa,Y0+K*(zR+3),K*(xb-xa),K*28,.8,1,'#999','3,2','#f7f6f2'); tx(X0+K*(xa+xb)/2,Y0+K*(zR+17),lab,5.4,'middle','','#999')
rc(X0+K*22.4,Y0+K*(zR+3),K*25.3,K*28,1.2,1,'#111',None,FILL)
tx(X0+K*35,Y0+K*(zR+12),'ÖN DİLİM',6.2,'middle','bold'); tx(X0+K*35,Y0+K*(zR+18),'dış yüz 25,3 × 28',5.2,'middle','','#333'); tx(X0+K*35,Y0+K*(zR+23),'tutamak',4.8,'middle','',GRY)
rc(X0+K*31,Y0+K*(zR+29),K*8,K*2,.9,0,GRN,None,'#eaf6ee'); tx(X0+K*35,Y0+K*(zR+27.6),'ağız 4',4.6,'middle','bold',GRN)
rc(X0+K*33,Y0+K*(zR+14),K*4,K*1.2,.8,0,'#555',None,'#bbb')
tx(X0+K*70+6,Y0+K*(zR+10),'REVOLVER 33 · 8 dilim',6.5,'start','bold'); tx(X0+K*70+6,Y0+K*(zR+18),'motorlu izole klape (ön dilim genişliği)',5.6,'start','',BLU); tx(X0+K*70+6,Y0+K*(zR+25),'yalıtımlı kutu, +3 °C',5.6,'start','',GRY)
# tahrik kati
rc(X0+K*27,Y0+K*(zT+1),K*16,K*6,1,1,'#111',None,'#eee'); tx(X0+K*35,Y0+K*(zT+5),'tabla M1',5.4,'middle','bold')
rc(X0+K*8,Y0+K*(zT+1),K*14,K*6,1,1,BLU,None,'#dfe7fb'); tx(X0+K*15,Y0+K*(zT+5),'dozaj M3',5.4,'middle','bold',BLU)
for xx_ in (5,35,65): ci(X0+K*xx_,Y0+K*(zT+7.2),2.2,1,AMB,None,'#fdf3dd')
tx(X0+K*70+6,Y0+K*(zT+5.5),'tahrik 8: M1 · M3 · yük hücresi ×3',6.3,'start','',GRY)
# bosluk
ln(X0+K*35,Y0+K*zB,X0+K*35,Y0+K*(zB+4),2,GRN); tx(X0+K*38,Y0+K*(zB+4),'ağız (35, 69)',5.6,'start','bold',GRN)
el(X0+K*35,Y0+K*(zB+11),K*17,K*1.2,1.2,BLU,None,'#dfe7fb'); tx(X0+K*35,Y0+K*(zB+9),'tepsi Ø34 (spiral)',5.2,'middle','',BLU)
tx(X0+K*70+6,Y0+K*(zB+8),'BOŞLUK 14 · ön açık · tabanı sabit plaka',6.3,'start','',BLU)
# raflar: her katta 2 dilim onde (dis yuz 25,3), arkada 2
raf_on = (('KAŞAR 5','KAŞAR 6'),('KAŞAR 7','KAŞAR 8'),('KAV. çözülme','BOŞ yuva'))
raf_ark = ('kaşar 9 · 10','kaşar 11 · 12','kuş. çözülme · boş')
for k in range(3):
    zr=zt['RAF %d'%(k+1)]
    for i,lab in enumerate(raf_on[k]):
        x_=X0+K*(5+i*35)
        dash = '4,3' if 'BOŞ' in lab else None
        rc(x_,Y0+K*(zr+4),K*25.3,K*28,1,1,'#999' if dash else '#111',dash,'#fff' if dash else FILL)
        tx(x_+K*12.6,Y0+K*(zr+16),lab,5.6,'middle','bold','#999' if dash else '#111'); tx(x_+K*12.6,Y0+K*(zr+22),'önde',4.6,'middle','',GRY)
    tx(X0+K*70+6,Y0+K*(zr+13),'RAF %d · 37 · 2 önde + 2 arkada' % (k+1),6.3,'start','',GRY)
    tx(X0+K*70+6,Y0+K*(zr+21),'arka: %s' % raf_ark[k],5.6,'start','','#333')
ln(X0,Y0+K*197+16,X0+K*70,Y0+K*197+16,.8); tx(X0+K*35,Y0+K*197+28,'70',8,'middle','bold')
ln(X0-14,Y0,X0-14,Y0+K*197,.8); tx(X0-18,Y0+K*98,'197',8,'end','bold')
zz=0
for ad,h,_ in Z: tx(X0-18,Y0+K*(zz+h/2)+3,'%g'%h,5.2,'end','',GRY); zz+=h
tx(X0+K*35,Y0+K*197+42,'27+4+33+8+14+37+37+37 = 197 ✓',7,'middle','bold',GRN)

# ================= YAN KESİT =================
XS,YS = 300,120
tx(XS+K*42,YS-10,'YAN KESİT (arka ← y → ön) 1:4',9,'middle','bold')
rc(XS,YS,K*84,K*197,2.2)
zz=0
for ad,h,col in Z:
    rc(XS,YS+K*zz,K*84,K*h,.8,0,'#111',None,col); zz+=h
rc(XS+K*2,YS+K*2,K*80,K*23,1,2,'#111',None,'#fff'); tx(XS+K*42,YS+K*14,'teknik: soğutma + elektrik (üstten servis)',5.6,'middle','')
# revolver kesiti: tabla y 7-73 eksen 40; arka dilim y 7-35; gobek 35-45; on dilim 45-73 = C sekli (r 5..33 → y 45..73)
rc(XS+K*1,YS+K*(zR+0.5),K*82,K*32,.9,2,'#111','3,2')
rc(XS+K*7,YS+K*(zR+2),K*28,K*28,1.1,0,'#111',None,FILL); tx(XS+K*21,YS+K*(zR+16),'arka dilim',5.4,'middle','')
rc(XS+K*35,YS+K*(zR+2),K*10,K*28,.8,0,'#111',None,'#ddd'); tx(XS+K*40,YS+K*(zR+16),'göbek',4.6,'middle','',GRY)
# on dilim C sekli (radyal kesit): r → y = 40 + r ; z: dilim tabani zR+30
RY=lambda r: XS+K*(40+r); RZ=lambda c: YS+K*(zR+30-c)
poly([(RY(5),RZ(28)),(RY(33),RZ(28)),(RY(33),RZ(11)),(RY(29),RZ(7)),(RY(29),RZ(0)),(RY(13),RZ(0)),(RY(13),RZ(7)),(RY(5),RZ(15))],1.2,'#111','#dff3e6')
poly([(RY(5.3),RZ(24)),(RY(32.7),RZ(24)),(RY(32.7),RZ(11)),(RY(29),RZ(7.3)),(RY(13),RZ(7.3)),(RY(5.3),RZ(15))],0,'none',MAT)
rc(RY(12),RZ(7),K*18,K*7,1,2,'#111',None,'#fff')
for k in range(8): ln(RY(13+k*2.2),RZ(7),RY(13+k*2.2),RZ(0),.6,'#999')
ln(RY(11),RZ(13),RY(31),RZ(13),1.4,BLU)
for k in range(7):
    r_=12.5+k*2.8; s=1 if k%2==0 else -1; ln(RY(r_),RZ(13),RY(r_),RZ(13+s*4.5),.9,BLU)
rc(RY(27.5),RZ(0),K*2.5,K*1,0,0,'none',None,'#fff')
tx(RY(19),RZ(19),'ÖN DİLİM = C şekli',5,'middle','bold',GRN); tx(RY(19),RZ(16),'helezon r 12-30 · tarak',4.4,'middle','',GRY)
# tabla + delik onde
rc(XS+K*7,YS+K*(zR+30),K*66,K*2,1,0,'#111',None,'#bbb'); rc(RY(27),YS+K*(zR+30),K*3.5,K*2,0,0,'none',None,'#fff')
tx(XS+K*84+4,YS+K*(zR+31.5),'tabla 2 · delik yalnız önde (y 69)',5.2,'start','',GRY)
rc(XS+K*82,YS+K*(zR+1),K*2,K*31,1,0,BLU,None,'#dfe7fb'); tx(XS+K*84+4,YS+K*(zR+10),'klape',5.2,'start','',BLU)
# tahrik: M1 gobek altinda, M3 on dilim ic ucu (y 51), yuk hucreleri
rc(XS+K*35,YS+K*(zT+1),K*10,K*6,1,1,'#111',None,'#eee'); tx(XS+K*40,YS+K*(zT+5),'M1',5,'middle','bold')
rc(XS+K*47,YS+K*(zT+1),K*8,K*6,1,1,BLU,None,'#dfe7fb'); tx(XS+K*51,YS+K*(zT+5),'M3',5,'middle','bold',BLU)
arr(XS+K*51,YS+K*(zT+1),XS+K*51,YS+K*(zT-1.5),BLU,1.1); tx(XS+K*56,YS+K*(zT+2.5),'pençe ↑ dilim iç ucu (r 11)',4.8,'start','',BLU)
for yy_ in (12,40,68): ci(XS+K*yy_,YS+K*(zT+7.2),2.2,1,AMB,None,'#fdf3dd')
tx(XS+K*84+4,YS+K*(zT+6.5),'yük hücresi ×3 (tabla toplam)',5.2,'start','',AMB)
# bosluk: agiz y 69 → tepsi
ln(XS+K*69,YS+K*zB,XS+K*69,YS+K*(zB+3.5),2,GRN); tx(XS+K*69,YS+K*(zB-1.2),'ağız y 69',5.2,'middle','bold',GRN)
rc(XS+K*38,YS+K*(zB+10.5),K*34,K*1.5,1.1,BLU,None,'#dfe7fb'); rc(XS+K*72,YS+K*(zB+9.5),K*12,K*3,1,BLU,None,'#dfe7fb')
tx(XS+K*50,YS+K*(zB+8.5),'tepsi en geride (m. y 55)',4.8,'middle','',BLU)
rc(XS,YS+K*(zB+12),K*84,K*2,1,0,'#111',None,'#bbb'); tx(XS+K*84+4,YS+K*(zB+13.5),'boşluk tabanı (sabit plaka)',5.2,'start','',GRY)
# raflar (yan): on yuva y 50-78, arka yuva y 12-40; dilim bbox derinlik 28
for k in range(3):
    zr=zt['RAF %d'%(k+1)]
    rc(XS+K*50,YS+K*(zr+4),K*28,K*28,1,1,'#111',None,FILL); tx(XS+K*64,YS+K*(zr+18),'ön yuva',5.2,'middle','')
    rc(XS+K*12,YS+K*(zr+4),K*28,K*28,.9,1,'#888','3,2','#f7f3ec'); tx(XS+K*26,YS+K*(zr+18),'arka yuva',5.2,'middle','',GRY)
    rc(XS+K*82,YS+K*(zr+1),K*2,K*35,1,0,BLU,None,'#dfe7fb')
    tx(XS+K*84+4,YS+K*(zr+18),'RAF %d: önden FIFO' % (k+1),5.2,'start','',GRY)
ln(XS,YS+K*197+16,XS+K*84,YS+K*197+16,.8); tx(XS+K*42,YS+K*197+28,'84',8,'middle','bold')
tx(XS+K*42,YS+K*197+42,'revolver ve raf izole, önden klapeli · boşluk soğuk hacmin dışında',6.3,'middle','','#333')

# ================= ÜST GÖRÜNÜŞ (C-şekli dilimlerle) =================
XU,YU = 560,120
KU=3.0
tx(XU+KU*35,YU-10,'ÜST GÖRÜNÜŞ — tabla, 8 C-dilim 1:3,3',9,'middle','bold')
rc(XU,YU,KU*70,KU*84,1.6)
rc(XU+KU*31,YU,KU*8,KU*84,0,0,'none',None,'#dff3e6')
cx,cy = XU+KU*35, YU+KU*40
ci(cx,cy,KU*33.5,1.4,'#111',None,'#f7f7f7')
for i,ad in enumerate(NAMES):
    a1=67.5+i*45; am=math.radians(a1+22.5)
    sector(cx,cy,KU*5,KU*33,a1,a1+45,1,'#111',FILL if 'KAŞAR' in ad else SUC)
    # V-oluk (aciortay boyunca yuva), helezon, tarak bandi, agiz dis ucta, pence ic ucta
    ca,sa = math.cos(am),math.sin(am)
    P=lambda r,t: (cx+KU*(r*ca - t*sa), cy+KU*(r*sa + t*ca))     # r radyal, t tanjant
    poly([P(12,-3.5),P(30,-3.5),P(30,3.5),P(12,3.5)],.8,'#111','#fff')
    for k in range(6):
        r_=13.5+k*2.7; ln(*P(r_,-3.5),*P(r_,3.5),.5,'#999')
    ln(*P(11,0),*P(31,0),1.1,BLU)
    ci(*P(29,0),2.4,1.2,GRN,None,'#fff'); ci(*P(29,0),1,1,GRN,None,GRN)
    ci(*P(10.5,0),2,1,BLU,None,'#dfe7fb')
    tx(*P(22,0),ad,4.6,'middle','bold')
    # tx offset: yazi yuvanin ustunde; tanjant kaydir
    o.pop()
    x_,y_ = P(22,-7.5 if i%2==0 else 7.5); tx(x_,y_+2,ad,4.4,'middle','bold')
ci(cx,cy,KU*5,.9,'#111',None,'#ddd'); tx(cx,cy+3,'göbek',4.6,'middle','',GRY)
ci(XU+KU*35,YU+KU*69,KU*31,.9,GRN,'5,3'); ci(XU+KU*35,YU+KU*69,4,1.6,GRN,None,'#fff')
tx(XU+KU*35,YU+KU*78,'ağız (35, 69) · süpürme R31 ✓',5.4,'middle','bold',GRN)
carc(cx,cy,KU*36,195,300,BLU,1.1); tx(cx-KU*27,cy-KU*31,'45° adım 1,5 sn',5.2,'middle','',BLU)
tx(XU+KU*35,YU+KU*84+12,'her dilim: V-oluk yuvası (r 12-30) · helezon (mavi mil) · ağız dış uçta (yeşil) · pençe iç uçta (mavi) · tarak üstte',5,'middle','','#333')
tx(XU+KU*35,YU+KU*84+22,'70 · kasetlerin hepsi C şekli — aynı dilim, aynı yuva',5.6,'middle','bold')

# ================= DİLİM C-ŞEKLİ (radyal kesit, v5-C) =================
XD,YD = 560,420
rc(XD,YD,250,290,1.2,3,'#999',None,'#fcfdff')
tx(XD+125,YD+16,'C-DİLİM — radyal kesit (v5-C)',7.5,'middle','bold')
K5=4.4
dx_,dz_ = XD+40, YD+200
RX=lambda r: dx_+K5*(r-5); DZ=lambda c: dz_-K5*c
poly([(RX(5),DZ(28)),(RX(33),DZ(28)),(RX(33),DZ(11)),(RX(29),DZ(7)),(RX(29),DZ(0)),(RX(13),DZ(0)),(RX(13),DZ(7)),(RX(5),DZ(15))],1.3,'#111',FILL)
poly([(RX(5.3),DZ(24)),(RX(32.7),DZ(24)),(RX(32.7),DZ(11)),(RX(29),DZ(7.3)),(RX(13),DZ(7.3)),(RX(5.3),DZ(15))],0,'none',MAT)
rc(RX(12),DZ(7),K5*18,K5*7,1.2,3,'#111',None,'#fff')
ln(RX(11.5),DZ(3.5),RX(30.5),DZ(3.5),1.2,'#333')
r_=12.6
for pch in (2,2.2,2.5,2.8,3.1,3.4,3.7,4):
    path('M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f'%(RX(r_),DZ(6.7),RX(r_+pch/2),DZ(3.5),RX(r_),DZ(0.3)),.9,'#111'); r_+=pch
ln(RX(11),DZ(13),RX(31),DZ(13),1.6,BLU)
for k in range(8):
    rr=12.5+k*2.4; s=1 if k%2==0 else -1; ln(RX(rr),DZ(13),RX(rr),DZ(13+s*5),1,BLU)
rc(RX(11),DZ(18.5),K5*20,K5*11,.8,3,BLU,'4,3')
rc(RX(10),DZ(2.3),K5*2,K5*2.4,1,1,BLU,None,'#dfe7fb'); tx(RX(11),DZ(-3),'pençe (iç uç)',5.2,'middle','bold',BLU)
rc(RX(27.5),DZ(0),K5*2.5,K5*1,0,0,'none',None,'#fff'); arr(RX(28.8),DZ(-1),RX(28.8),DZ(-6),GRN,1.3); tx(RX(28.8),DZ(-8.5),'ağız → (35, 69)',5.2,'middle','bold',GRN)
tx(RX(21),DZ(9.6),'helezon Ø7 · hatve 2→4 · 30 dev/dk',5,'middle','bold'); tx(RX(21),DZ(20.5),'tarak Ø11 · 3 dev/dk (1:20)',5,'middle','bold',BLU)
tx(RX(8),DZ(18),'eğimli uç',4.6,'middle','',GRY); tx(RX(31),DZ(9),'45°',4.6,'middle','bold',AMB)
ln(RX(5),DZ(29.5),RX(33),DZ(29.5),.7); tx(RX(19),DZ(31),'28,4 (r 5 → 33)',5.4,'middle','bold')
ln(RX(34.5),DZ(0),RX(34.5),DZ(28),.7); tx(RX(35.5),DZ(14),'28',5.4,'start','bold')
tx(XD+125,YD+262,'45° · 418 cm² · ~10 L · kaşar ~4 kg · dolu ≤ 6 kg · boş 1,4 kg · 1,5 mm paslanmaz · RFID',5,'middle','','#333')
tx(XD+125,YD+276,'dış yüzde tutamak (pençe robot) · ağız tabla yüzeyiyle kapalı, delik yalnız önde',5,'middle','',GRY)

# ================= ELEKTRİK & TAHRİK =================
XE,YE = 830,120
rc(XE,YE,600,440,1.4,4,'#111',None,'#fcfdff')
tx(XE+14,YE+22,'ELEKTRİK & TAHRİK — dilimde elektrik yok',10,'start','bold')
kx,ky = XE+16,YE+36
rc(kx,ky,280,200,1,3,'#999',None,'#fff'); tx(kx+140,ky+14,'PENÇE KAVRAMA (dog clutch) — dilim iç ucu',7,'middle','bold')
rc(kx+30,ky+28,230,48,1,0,'#111',None,FILL); tx(kx+145,ky+40,'dilim (pasif) — iç uç r 11',5.6,'middle','',GRY)
ln(kx+80,ky+58,kx+250,ky+58,1.6,'#333'); tx(kx+170,ky+54,'helezon mili (yatay, radyal)',5,'middle','')
poly([(kx+70,ky+50),(kx+82,ky+58),(kx+70,ky+66)],1,'#555','#eee'); poly([(kx+58,ky+66),(kx+70,ky+54),(kx+70,ky+78)],1,'#555','#eee'); tx(kx+52,ky+48,'konik',5,'end','','#555')
rc(kx+64,ky+76,12,10,1.1,1,BLU,None,'#dfe7fb'); tx(kx+82,ky+84,'dilim pençesi (taban altı)',5.2,'start','bold',BLU)
rc(kx+30,ky+86,230,8,1,0,'#111',None,'#bbb'); tx(kx+266,ky+92,'tabla',5,'start','',GRY)
rc(kx+64,ky+94,12,10,1.1,1,BLU,None,'#dfe7fb'); tx(kx+82,ky+102,'karşı pençe — yaylı, pahlı (kendi hizalar)',5.2,'start','',BLU)
rc(kx+56,ky+106,28,34,1.1,2,'#111',None,'#eee'); tx(kx+70,ky+120,'M3',6,'middle','bold'); tx(kx+70,ky+130,'24 V',4.6,'middle','')
tx(kx+92,ky+120,'dozaj motoru 40 W · enkoder',5.4,'start','bold'); tx(kx+92,ky+132,'tabla dönerken pençe aşağı basılır,',5,'start','','#333'); tx(kx+92,ky+142,'hizalanınca yayla çıkar, kilitler',5,'start','','#333')
tx(kx+140,ky+166,'M3 tek yön → helezon + (1:20) tarak',5.6,'middle','bold',BLU); tx(kx+140,ky+178,'tablada kablo yok → slip ring yok, dilim yıkanır',5.2,'middle','bold',GRN)
tx(kx+140,ky+192,'aynı pençe her dilimde: 8 dilim, 1 motor',5.2,'middle','','#333')
bx,by = XE+310,YE+36
rc(bx,by,274,200,1,3,'#999',None,'#fff'); tx(bx+137,by+14,'KONTROL ŞEMASI',7,'middle','bold')
rc(bx+90,by+24,94,26,1.2,3,'#111',None,'#f3f3f3'); tx(bx+137,by+35,'PLC / kontrolör',6,'middle','bold'); tx(bx+137,by+45,'24 V bus · CAN',4.8,'middle','')
items=[('M1 tabla 60 W',BLU),('M3 dozaj 40 W',BLU),('klape revolver',BLU),('klape raf ×3',BLU),('yük hücresi ×3',AMB),('index sensör (8 pim)',AMB),('RFID (ön pozisyon)',PUR),('soğutma +3',GRY)]
for i,(ad,col) in enumerate(items):
    x_=bx+12+(i%2)*130; y_=by+62+(i//2)*30
    rc(x_,y_,120,22,1,2,col,None,'#fff'); tx(x_+60,y_+14,ad,5.6,'middle','bold',col)
    ln(bx+137,by+50,x_+60,y_,.6,'#999')
tx(bx+137,by+190,'3 sürücü · 3 tartı · 1 PLC · slip ring yok',5.4,'middle','bold',GRN)
ny=YE+250
tx(XE+14,ny,'DOZAJ ÇEVRİMİ (bir pide, kaşar + kavurma):',8,'start','bold')
seq=['① PLC dilim haritasına bakar (RFID + sayaç) → en yakın KAŞAR, M1 ≤ 45° döner, index sensör durdurur (±1 mm) → pençe kendi kavrar',
     '② yük hücreleri tabla ağırlığını okur (W0) → M3 döner: helezon dış uçtan tepsiye döker, robot spiral (14 sn) → W0 − W = 80 g olunca durur (±3 g)',
     '③ KAVURMA: M1 döner (≤ 135°, 4,5 sn), aynı çevrim 35 g · sayaç: dilim kalanı düşer · toplam dozaj ≤ 20 sn',
     '④ dilim kalan ≤ 1 doz ya da saat doldu → değişim (sağ alt) · pençe kavramazsa M1 ±2° titretir, olmazsa dilim "arızalı"']
for i,s in enumerate(seq): tx(XE+14,ny+16+i*13,s,6.4,'start','','#333')
tx(XE+14,ny+76,'güç: M1 60 · M3 40 · klape 4×10 · soğutma 90 · PLC 15 → ~245 W tepe, ortalama ~110 W',6.6,'start','bold',GRY)
tx(XE+14,ny+90,'M1: 45° 1,5 sn (dönen kütle ~55 kg, ~6 N·m, Ø30 bilyalı ring) · M3: 30 dev/dk, 80 g = 4 tur = 8 sn (spiral 14 sn içinde)',6.6,'start','','#333')
tx(XE+14,ny+104,'yük hücresi: dilim takılınca tartılır (başlangıç) → her dozda fark → "boşaldı" tetiği; ayrı sensör yok',6.6,'start','','#333')
tx(XE+14,ny+118,'ağız tabla yüzeyiyle kapalı, delik yalnız (35, 69) → dönerken dökülme yok; helezon durunca akış durur',6.6,'start','','#333')
tx(XE+14,ny+132,'soğuk hacim: revolver kutusu + raf katları +3 °C; boşluk dışarıda; klape yalnız değişimde açılır (≤ 2/gün)',6.6,'start','','#333')
tx(XE+14,ny+146,'sucuk dilimi: helezon değil çubuk + bıçak — aynı 45° gövde, aynı pençe (bıçak tahriki), ayrı detay çizimi',6.6,'start','bold',AMB)

# ================= STOK · DEĞİŞİM =================
XT,YT = 830,580
rc(XT,YT,600,310,1.4,4)
tx(XT+14,YT+22,'STOK · DEĞİŞİM · HAFTALIK — "2 raf, üst kat alt kat": 3 kat sığdı',10,'start','bold')
rows=[('TABLA (8)','kaşar ×4 (16 kg · 2,5 gün) · sucuk ×2 (hafta) · kavurma ×1 · kuşbaşı ×1'),
      ('RAF 1 (üst)','kaşar 5 · 6 önde, 9 · 10 arkada'),
      ('RAF 2 (orta)','kaşar 7 · 8 önde, 11 · 12 arkada'),
      ('RAF 3 (alt)','kavurma çözülme · BOŞ yuva önde, kuşbaşı çözülme · boş arkada'),
      ('KAŞAR toplam','4 + 8 = 12 dilim × 4 kg = 48 kg = 7,4 gün ✓ (6,5 kg/gün) · +1 kural: 12. dilim yedek'),
      ('KÜÇÜKLER','1 taze tablada + 2 donmuş STORE −18 (çekmece 29 ≥ 28 ✓) → RAF 3'+chr(39)+'te 1 gün çözülür'),
      ('ELEMAN','haftada 1: 12 kaşar + 2 sucuk + 1+1 küçük getirir, boşları alır, dilimleri yıkar')]
for i,(a,b) in enumerate(rows):
    yy=YT+46+i*16; tx(XT+14,yy,a,6.8,'start','bold'); tx(XT+118,yy,b,6.5,'start','','#333')
ln(XT+12,YT+164,XT+588,YT+164,.8,'#bbb')
tx(XT+14,YT+182,'DEĞİŞİM (kaşar boşaldı) — 4 hamle, ~75 sn, kuyruk boşken, ≤ 2/gün:',7.5,'start','bold',BLU)
seq2=['① M1 boş dilimi öne döndürür · revolver klapesi açılır · robot tutamaktan çeker → RAF 3 BOŞ yuvasına koyar',
      '② RAF 1 klapesi açılır → robot dolu kaşarı çeker → tablaya sürer: pençe kavrar, RFID okur, tartı = başlangıç ağırlığı',
      '③ klapeler kapanır · boşalan raf yuvası yeni "boş yuva" olur · arkadaki dilim bir sonraki değişimde öne alınır (FIFO)',
      '④ küçükler: RAF 3 çözülmüş ↔ tabladaki boş · sucuk: eleman haftalık']
for i,s in enumerate(seq2): tx(XT+14,YT+198+i*13,s,6.5,'start','','#333')
tx(XT+14,YT+262,'Neden tek revolver + sabit raf: dönen tek parça, 3 motor, 55 kg; alt revolver (v12) gereksiz — yedekler zaten önden FIFO ile alınıyor.',6.5,'start','bold',GRN)
tx(XT+14,YT+276,'Dilim tipi TEK (C şekli); sucuk dilimi aynı gövde, içi çubuk + bıçak. Kutu kaset yok.',6.5,'start','','#333')
tx(XT+14,YT+292,'Açık: kaşar 45° V + helezon akışı prototip · klape contası · tabla rulmanı · sucuk çubuk dilimi detayı · kobot 133-161 cm tabla erişimi',6.3,'start','',AMB)

# ================= KONTROL =================
YK=930
rc(60,YK,1370,190,1.6,4)
tx(76,YK+24,'KONTROL — kurallar ve HAT v45 etkisi',11,'start','bold')
rows=[('① çıkış bandı: tek ağız (35, 69) ∈ [31,39] ✓ · y 69 ≥ 31 ✓ · süpürme R31: x 4–66 ✓ y 38–100 (ön açık) ✓',GRN),
      ('② erişim: boşalan dilim öne döner → önünde hiçbir şey yok ✓ · raf 3 kat, her yuva önden, arka yuvalar FIFO ✓ · park = RAF 3 boş yuva ✓',GRN),
      ('③ KARAR C doğrudan: dilim = 45° sektör, V-oluk, helezon, tarak, ağız dış uçta, pençe iç uçta; huni yok, sabit çark yok, dilimde elektrik yok ✓',GRN),
      ('④ dikey 27+4+33+8+14+37×3 = 197 ✓ · 70×84 aynı · dilim dolu ≤ 6 kg ✓ · tek dozaj düzlemi: tepsi 111-125 cm, tabla 133-161 cm',GRN),
      ('⑤ HAT v45: TOPPING bloğu bu çizimle (çark katı 21 → 8, geçiş rafı 3 kat, revolver) · STORE v4 değişmez (29 ≥ 28) · KONTROL ⑧⑨ güncellenir',BLU),
      ('⑥ AÇIK: kaşar akışı prototip · klape/soğuk hacim · sucuk çubuk dilimi · tabla rulmanı/M1 seçimi · kobot yükseklik erişimi (⑦ ile)',AMB)]
for i,(s,c) in enumerate(rows):
    tx(76+(i%2)*690,YK+48+(i//2)*44,s[:122],7.2,'start','',c)
    if len(s)>122: tx(76+(i%2)*690,YK+48+(i//2)*44+12,s[122:],7.2,'start','',c)
tx(W-40,H-12,'AUTOKITCH · arastirma/3_TOPPING/ist3_topping_detay_v14 · 4 Eyl 2026',7,'end','',GRY)
o.append('</svg>')
svg = chr(10).join(o)
xml.dom.minidom.parseString(svg.encode('utf-8'))
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\ist3_topping_detay_v14.svg"
io.open(out,'w',encoding='utf-8').write(svg)
print('yazildi + XML gecerli', out)
