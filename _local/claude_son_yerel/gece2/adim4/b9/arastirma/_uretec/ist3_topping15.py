# -*- coding: utf-8 -*-
# TOPPING v15 — REVOLVER YOK. C-kaset (sektör, helezon, tarak, V-oluk, ağız dış uçta) SABİT "papyon" dizilimde:
# her katta sol + sağ C-kaset, tipler yan duvarda, ağızlar 31/39 bandında, arkalarında kendi yedekleri (aynı ray, öne çekilir). 2 kat + 2 dozaj düzlemi + 2 kat raf.
import io, math, xml.dom.minidom
W, H = 1460, 1170
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
def sector(cx,cy,r0,r1,a1,a2,sw=1,c='#111',f='#f1efe8',dash=None):
    p = lambda r,a: (cx+r*math.cos(math.radians(a)), cy+r*math.sin(math.radians(a)))
    x1,y1=p(r1,a1); x2,y2=p(r1,a2); x3,y3=p(r0,a2); x4,y4=p(r0,a1)
    path('M%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f Z' % (x1,y1,r1,r1,x2,y2,x3,y3,r0,r0,x4,y4),sw,c,f,dash)

GRN, RED, BLU, GRY, AMB, PUR = '#1d7a4f', '#c0392b', '#1a49b8', '#666', '#b7791f', '#6b4fa8'
FILL, MAT, SUC = '#f1efe8', '#e9dfa8', '#e8eef8'
K = 2.5
R1, R0, RA, HK = 32.0, 5.0, 29.0, 32.0        # sektör dış yarıçap, göbek, ağız yarıçapı, kaset yüksekliği
XL, XR, YC = 3.0, 67.0, 64.5                   # sol/sağ sektör merkezleri (x), çalışan pozisyon merkez y
Z = [('teknik',27,'#f3f3f3'),('KAT 1',35,'#fff'),('BOŞLUK 1',14,'#eef3ff'),('KAT 2',35,'#fff'),('BOŞLUK 2',14,'#eef3ff'),('RAF 1',36,'#f7f6f2'),('RAF 2',36,'#f7f6f2')]
assert sum(z[1] for z in Z)==197
zt={}; acc=0
for ad,h,_ in Z: zt[ad]=acc; acc+=h
z1,zb1,z2,zb2,zr1,zr2 = zt['KAT 1'],zt['BOŞLUK 1'],zt['KAT 2'],zt['BOŞLUK 2'],zt['RAF 1'],zt['RAF 2']
A60 = 60/360*math.pi*(R1**2-R0**2); A30 = A60/2

o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H))
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,42,'AUTOKITCH — İSTASYON 3 · TOPPING v15 (4 Eyl 2026) — REVOLVER YOK · C-KASET SABİT "PAPYON" DİZİLİMİ · 2 KAT + 2 DOZAJ DÜZLEMİ · yedek her kasetin ARKASINDA · 70 × 197 × 84 · cm',15,'start','bold')
tx(30,66,'C-kaset (sektör: V-oluk + helezon + tarak, ağız dış uçta) olduğu gibi: tip yan duvara, ağız ortaya → sol ağız x 31, sağ ağız x 39, ikisi de bantta. Her katta sol kaşar + sağ diğer malzeme; her kasetin arkasında aynı rayda yedeği: boşalan çekilir, arkadaki öne alınır (2 hamle). Kutu yok, dönen parça yok, huni yok.',9.5,'start','','#444')
ln(30,78,W-30,78,.8,'#999')

# ================= ÖN KESİT A-A (helezon eksenleri boyunca, kademeli) =================
X0,Y0 = 60,120
tx(X0+K*35,Y0-10,'ÖN KESİT A-A (helezon eksenleri) 1:4',9,'middle','bold')
rc(X0,Y0,K*70,K*197,2.2)
zz=0
for ad,h,col in Z:
    rc(X0,Y0+K*zz,K*70,K*h,.8,0,'#111',None,col); zz+=h
rc(X0+K*3,Y0+K*3,K*30,K*21,1,2,'#111',None,'#fff'); tx(X0+K*18,Y0+K*12,'SOĞUTMA',6.5,'middle','bold'); tx(X0+K*18,Y0+K*18,'1/12 HP · +3',5.6,'middle','')
rc(X0+K*37,Y0+K*3,K*30,K*21,1,2,'#111',None,'#fff'); tx(X0+K*52,Y0+K*10,'ELEKTRİK',6.5,'middle','bold'); tx(X0+K*52,Y0+K*15,'PLC · 24 V PSU',5,'middle',''); tx(X0+K*52,Y0+K*20,'5 sürücü',5,'middle','')
def c_profile(xc, sgn, zfloor, h, fill=MAT, ad='', alt='', screw=True, cutter=False, light=False):
    # xc: sektör merkezi x (cm); sgn +1 sola yaslı (tip solda, ağız sağda), -1 sağa yaslı; zfloor: kaset tabanı (cm, üstten)
    X=lambda r: X0+K*(xc+sgn*r); Zc=lambda c: Y0+K*(zfloor-c)
    col='#999' if light else '#111'
    poly([(X(R0),Zc(h)),(X(R1),Zc(h)),(X(R1),Zc(11)),(X(RA),Zc(7)),(X(RA),Zc(0)),(X(13),Zc(0)),(X(13),Zc(7)),(X(R0),Zc(15))],1.2,col,FILL if not light else '#f7f6f2','3,2' if light else None)
    if not light:
        poly([(X(R0+.3),Zc(h-4)),(X(R1-.3),Zc(h-4)),(X(R1-.3),Zc(11)),(X(RA),Zc(7.3)),(X(13),Zc(7.3)),(X(R0+.3),Zc(15))],0,'none',fill)
    if screw:
        rc(min(X(12),X(30)),Zc(7),K*18,K*7,1,2,col,None,'#fff')
        for k in range(7): ln(X(13.5+k*2.5),Zc(7),X(13.5+k*2.5),Zc(0),.6,'#999')
        ln(X(11),Zc(13),X(31),Zc(13),1.2,BLU)
        for k in range(6):
            r_=12.5+k*3.2; s=1 if k%2==0 else -1; ln(X(r_),Zc(13),X(r_),Zc(13+s*4.5),.8,BLU)
    if cutter:
        for k in range(6): rc(min(X(12+k*3.2),X(12+k*3.2+2.4)),Zc(h-6),K*2.4,K*(h-9),.7,1,'#555',None,'#f4ece6')
        rc(min(X(26),X(30)),Zc(4.5),K*4,K*3,1,1,RED,None,'#fdeeee'); tx(X(28),Zc(1.2),'bıçak',4.4,'middle','bold',RED)
    # ağız (tabanda r 27,5-30)
    rc(min(X(27.5),X(30)),Zc(0),K*2.5,K*1.2,0,0,'none',None,'#fff')
    ln(X(28.8),Zc(0),X(28.8),Zc(-5),1.6,GRN)
    if ad: tx(X(19),Zc(h-8),ad,6,'middle','bold'); tx(X(19),Zc(h-13),alt,4.6,'middle','','#333')
    # motor duvarda (tip ucu)
    rc(min(X(-3),X(3)),Zc(6),K*6,K*5,1,1,BLU,None,'#dfe7fb'); tx(X(0),Zc(2.5),'M',4.8,'middle','bold',BLU)
    ci(X(9.5),Zc(3.5),K*1.6,.9,'#555',None,'#eee')
def kat(zL, sol, sag):
    zfloor = zL+33
    rc(X0,Y0+K*zfloor,K*70,K*2,1,0,'#111',None,'#bbb')
    for xx in (31,39): rc(X0+K*(xx-2),Y0+K*zfloor,K*4,K*2,0,0,'none',None,'#fff')
    c_profile(XL,+1,zfloor,HK,MAT,*sol)
    if sag[0]=='SUCUK': c_profile(XR,-1,zfloor,HK,MAT,sag[0],sag[1],screw=False,cutter=True)
    else: c_profile(XR,-1,zfloor,HK,MAT,sag[0],sag[1])
    rc(X0+K*1,Y0+K*(zL+0.5),K*68,K*34,.8,2,'#111','3,2')
kat(z1,('KAŞAR A','60° · h 32 · 5,5 kg'),('SUCUK','çubuk + bıçak'))
kat(z2,('KAŞAR B','60° · h 32 · 5,5 kg'),('KAVURMA','30° (kesit y 72) · 4 kg'))
tx(X0+K*70+6,Y0+K*(z1+8),'KAT 1 · 35: kaşar A | sucuk',6.5,'start','bold'); tx(X0+K*70+6,Y0+K*(z1+16),'ağızlar (31, 64,5) · (39, 64,5)',5.6,'start','',GRN); tx(X0+K*70+6,Y0+K*(z1+23),'klape (ön, motorlu, izole)',5.4,'start','',BLU)
tx(X0+K*70+6,Y0+K*(z2+8),'KAT 2 · 35: kaşar B | kavurma + kuşbaşı',6.5,'start','bold'); tx(X0+K*70+6,Y0+K*(z2+16),'sağda 2 × 30° yan yana: ağız (39, 72) · (39, 57)',5.6,'start','',GRN); tx(X0+K*70+6,Y0+K*(z2+23),'kuşbaşı bu kesitte görünmez (y 57)',5.4,'start','',GRY)
for zb,lab in ((zb1,'BOŞLUK 1 · düzlem 1 (sucuklu) · tepsi 123 cm'),(zb2,'BOŞLUK 2 · düzlem 2 (kav/kuş) · tepsi 74 cm')):
    el(X0+K*35,Y0+K*(zb+10.5),K*17,K*1.2,1.2,BLU,None,'#dfe7fb'); tx(X0+K*35,Y0+K*(zb+8),'tepsi Ø34 · spiral',5,'middle','',BLU)
    tx(X0+K*70+6,Y0+K*(zb+8),lab,6.3,'start','',BLU)
# raflar: on yuvalar (y 48-81) kesitte C profili (hafif)
for zr,pair,ark,ad in ((zr1,('KAŞAR E','KAŞAR F'),'arka: kaşar G · H','RAF 1'),(zr2,('PARK (boş)','PARK (boş)'),'arka: kav · kuş çözülme (STORE'+chr(39)+'dan)','RAF 2')):
    zfloor=zr+34
    rc(X0,Y0+K*zfloor,K*70,K*2,1,0,'#111',None,'#bbb')
    for i,(xc,sgn) in enumerate(((XL,+1),(XR,-1))):
        light = 'PARK' in pair[i]
        c_profile(xc,sgn,zfloor,HK,'#f1efe8',light=light,screw=not light)
        tx(X0+K*(xc+sgn*19),Y0+K*(zfloor-24),pair[i],5.6,'middle','bold','#999' if light else '#111')
    tx(X0+K*70+6,Y0+K*(zr+12),'%s · 36: önde 2 + arkada 2' % ad,6.3,'start','',GRY); tx(X0+K*70+6,Y0+K*(zr+20),ark,5.4,'start','','#333')
ln(X0,Y0+K*197+16,X0+K*70,Y0+K*197+16,.8); tx(X0+K*35,Y0+K*197+28,'70',8,'middle','bold')
ln(X0-14,Y0,X0-14,Y0+K*197,.8); tx(X0-18,Y0+K*98,'197',8,'end','bold')
zz=0
for ad,h,_ in Z: tx(X0-18,Y0+K*(zz+h/2)+3,'%g'%h,5.2,'end','',GRY); zz+=h
tx(X0+K*35,Y0+K*197+42,'27+35+14+35+14+36+36 = 197 ✓',7,'middle','bold',GRN)
tx(X0+K*35,Y0+K*197+54,'kesit kademeli: sol/sağ 60° kasetlerde y 64,5; kavurmada y 72',5.4,'middle','',GRY)

# ================= YAN KESİT B-B (x 31 — sol ağız hattı) =================
XS,YS = 320,120
tx(XS+K*42,YS-10,'YAN KESİT B-B (x 31, sol ağız hattı) 1:4',9,'middle','bold')
rc(XS,YS,K*84,K*197,2.2)
zz=0
for ad,h,col in Z:
    rc(XS,YS+K*zz,K*84,K*h,.8,0,'#111',None,col); zz+=h
rc(XS+K*2,YS+K*2,K*80,K*23,1,2,'#111',None,'#fff'); tx(XS+K*42,YS+K*14,'teknik: soğutma + elektrik (üstten servis)',5.6,'middle','')
hw = 28*math.sin(math.radians(30))     # r 28 kesitinde yarı genişlik = 14
def v_section(yc, zfloor, h, light=False, lab=''):
    Yy=lambda y: XS+K*y; Zc=lambda c: YS+K*(zfloor-c)
    col='#999' if light else '#111'; d='3,2' if light else None
    poly([(Yy(yc-hw),Zc(h)),(Yy(yc+hw),Zc(h)),(Yy(yc+hw),Zc(hw-3.5)),(Yy(yc+3.5),Zc(0)),(Yy(yc-3.5),Zc(0)),(Yy(yc-hw),Zc(hw-3.5))],1.2,col,FILL if not light else '#f7f6f2',d)
    if not light:
        poly([(Yy(yc-hw+.3),Zc(h-4)),(Yy(yc+hw-.3),Zc(h-4)),(Yy(yc+hw-.3),Zc(hw-3.5)),(Yy(yc+3.5),Zc(0.3)),(Yy(yc-3.5),Zc(0.3)),(Yy(yc-hw+.3),Zc(hw-3.5))],0,'none',MAT)
        ci(Yy(yc),Zc(3.5),K*3.5,1,'#111',None,'#fff'); ci(Yy(yc),Zc(13),K*5.5,.8,BLU,'3,2'); ci(Yy(yc),Zc(13),K*0.6,1,BLU,None,'#dfe7fb')
    if lab: tx(Yy(yc),Zc(h-8),lab,5.4,'middle','bold','#999' if light else '#111')
for zL,ad in ((z1,'KAŞAR A'),(z2,'KAŞAR B')):
    zfloor=zL+33
    rc(XS+K*2,YS+K*zfloor,K*80,K*2,1,0,'#111',None,'#bbb'); rc(XS+K*(YC-2),YS+K*zfloor,K*4,K*2,0,0,'none',None,'#fff')
    v_section(YC,zfloor,HK,False,ad); v_section(YC-33,zfloor,HK,True,'yedek (arka)')
    tx(XS+K*(YC-33),YS+K*(zfloor-14),'aynı rayda',4.6,'middle','',GRY); tx(XS+K*(YC-33),YS+K*(zfloor-10),'öne çekilir →',4.6,'middle','',GRY)
    ln(XS+K*YC,YS+K*(zfloor+2),XS+K*YC,YS+K*(zfloor+6),1.6,GRN); tx(XS+K*(YC+3),YS+K*(zfloor+6),'ağız',5,'start','bold',GRN)
    rc(XS+K*82,YS+K*(zL+0.5),K*2,K*34,1,0,BLU,None,'#dfe7fb')
    rc(XS+K*1,YS+K*(zL+0.5),K*81,K*34,.8,2,'#111','3,2')
for zb in (zb1,zb2):
    rc(XS+K*(YC-17),YS+K*(zb+10.5),K*34,K*1.5,1.1,BLU,None,'#dfe7fb'); rc(XS+K*(YC+17),YS+K*(zb+9.5),K*8,K*3,1,BLU,None,'#dfe7fb')
    tx(XS+K*(YC-2),YS+K*(zb+8.5),'tepsi (merkez y 64,5)',4.8,'middle','',BLU)
    rc(XS,YS+K*(zb+12),K*84,K*2,1,0,'#111',None,'#bbb')
for zr,fr,bk in ((zr1,'KAŞAR E','KAŞAR G'),(zr2,'PARK boş','kav. çözülme')):
    zfloor=zr+34
    rc(XS+K*2,YS+K*zfloor,K*80,K*2,1,0,'#111',None,'#bbb')
    v_section(YC,zfloor,HK,'PARK' in fr,fr); v_section(YC-33,zfloor,HK,True,bk)
    rc(XS+K*82,YS+K*(zr+0.5),K*2,K*35,1,0,BLU,None,'#dfe7fb')
tx(XS+K*84+4,YS+K*(z1+6),'KAT 1',6,'start','bold'); tx(XS+K*84+4,YS+K*(z1+13),'kesit r 28: V yarı genişlik 14,',5,'start','','#333'); tx(XS+K*84+4,YS+K*(z1+19),'V derinliği 10,5 (45°)',5,'start','','#333'); tx(XS+K*84+4,YS+K*(z1+25),'helezon Ø7 · tarak Ø11',5,'start','',BLU)
tx(XS+K*84+4,YS+K*(zb1+8),'boşluk 1 · taban sabit plaka',5.4,'start','',BLU)
tx(XS+K*84+4,YS+K*(z2+6),'KAT 2',6,'start','bold'); tx(XS+K*84+4,YS+K*(z2+13),'yedek kaset arkada, aynı ray',5,'start','','#333'); tx(XS+K*84+4,YS+K*(z2+19),'(tarak arkadakinde dönmez)',5,'start','',GRY)
tx(XS+K*84+4,YS+K*(zb2+8),'boşluk 2',5.4,'start','',BLU)
tx(XS+K*84+4,YS+K*(zr1+12),'RAF 1: kaşar E / G (arka)',5.4,'start','',GRY); tx(XS+K*84+4,YS+K*(zr2+12),'RAF 2: park / çözülme (arka)',5.4,'start','',GRY)
tx(XS+K*84+4,YS+K*(zr2+22),'klape: kat 1, kat 2, raf 1, raf 2',5,'start','',BLU)
ln(XS,YS+K*197+16,XS+K*84,YS+K*197+16,.8); tx(XS+K*42,YS+K*197+28,'84 · arka ← y → ön',8,'middle','bold')
tx(XS+K*42,YS+K*197+42,'arka 0-15: soğuk hava + kablo kanalı · 15-48 yedek · 48-81 çalışan · 81-84 klape',5.4,'middle','','#333')

# ================= ÜST GÖRÜNÜŞ KAT 1 / KAT 2 =================
XU,YU = 600,120
KU=2.35
def plan(X,Y,baslik,kat):
    tx(X+KU*35,Y-8,baslik,8.5,'middle','bold')
    rc(X,Y,KU*70,KU*84,1.4)
    rc(X+KU*31,Y,KU*8,KU*84,0,0,'none',None,'#dff3e6')
    rc(X,Y,KU*70,KU*15,0,0,'none',None,'#eeeeee'); tx(X+KU*35,Y+KU*9,'arka: hava + kablo kanalı 15',4.4,'middle','',GRY)
    cxl,cxr = X+KU*XL, X+KU*XR
    def sek(cx,yc,a1,a2,light,f,lab='',alt=''):
        sector(cx,Y+KU*yc,KU*R0,KU*R1,a1,a2,1 if not light else .8,'#111' if not light else '#999',f if not light else '#f7f6f2','3,2' if light else None)
        am=math.radians((a1+a2)/2)
        px_,py_ = cx+KU*20*math.cos(am), Y+KU*(yc+20*math.sin(am))
        if lab: tx(px_,py_+2,lab,5.2,'middle','bold','#999' if light else '#111')
        if alt: tx(px_,py_+9,alt,4.2,'middle','','#999' if light else '#333')
        if not light:
            # helezon + agiz + tip disli
            ln(cx+KU*11*math.cos(am),Y+KU*(yc+11*math.sin(am)),cx+KU*31*math.cos(am),Y+KU*(yc+31*math.sin(am)),1.1,BLU)
            ax,ay = cx+KU*RA*math.cos(am), Y+KU*(yc+RA*math.sin(am)); ci(ax,ay,2.6,1.3,GRN,None,'#fff'); ci(ax,ay,1,1,GRN,None,GRN)
            ci(cx+KU*9*math.cos(am),Y+KU*(yc+9*math.sin(am)),2,1,'#555',None,'#eee')
    # sol: 60° calisan + yedek
    sek(cxl,YC,-30,30,False,FILL,'KAŞAR A' if kat==1 else 'KAŞAR B','60° · helezon')
    sek(cxl,YC-33,-30,30,True,FILL,'yedek','arka')
    if kat==1:
        sek(cxr,YC,150,210,False,SUC,'SUCUK','çubuk + bıçak')
        sek(cxr,YC-33,150,210,True,SUC,'boş / 2. sucuk','eleman')
        outs=((31,YC),(39,YC))
    else:
        sek(cxr,YC,150,180,False,SUC,'KUŞBAŞI','30°')
        sek(cxr,YC,180,210,False,SUC,'KAVURMA','30°')
        sek(cxr,YC-33,150,180,True,SUC,'kuş. yedek','')
        sek(cxr,YC-33,180,210,True,SUC,'kav. yedek','')
        outs=((31,YC),(39,57),(39,72))
    for (ox,oy) in outs:
        ci(X+KU*ox,Y+KU*oy,KU*31,.8,GRN,'5,3')
    # motorlar duvarda
    for (mx,my,lab) in ((0,YC,'M'),(70-6,YC,'M')):
        rc(X+KU*mx,Y+KU*(my-3),KU*6,KU*6,1,1,BLU,None,'#dfe7fb'); tx(X+KU*(mx+3),Y+KU*(my+1.5),lab,4.6,'middle','bold',BLU)
    if kat==2: rc(X+KU*64,Y+KU*(YC+4),KU*6,KU*5,1,1,BLU,None,'#dfe7fb')
    rc(X,Y+KU*81,KU*70,KU*3,1,0,BLU,None,'#dfe7fb'); tx(X+KU*35,Y+KU*83.2,'klape',4.2,'middle','',BLU)
    arr(X+KU*17,Y+KU*(YC-33+18),X+KU*17,Y+KU*(YC-33+30),AMB,1); tx(X+KU*17,Y+KU*(YC-33+15),'öne alınır',4.2,'middle','',AMB)
    tx(X+KU*35,Y+KU*84+11,'süpürme R31: sol x 0-62 · sağ x 8-70 · y 33-96 ✓ (ön açık)',4.8,'middle','bold',GRN)
plan(XU,YU,'ÜST — KAT 1 (sucuklu düzlem)',1)
plan(XU,YU+KU*84+36,'ÜST — KAT 2 (kavurma / kuşbaşı düzlemi)',2)
tx(XU+KU*35,YU+2*KU*84+54,'sektörler "papyon": tipler duvarda (motor), kavisler ortada birbirine değer (x 35)',5,'middle','','#333')
tx(XU+KU*35,YU+2*KU*84+65,'duvar dibindeki üçgen boşluklar: 2 × ~13 L / kat — kablo, sensör, hava',5,'middle','',GRY)

# ================= C-KASET DETAYI =================
XD,YD = 600,600
rc(XD,YD,250,300,1.2,3,'#999',None,'#fcfdff')
tx(XD+125,YD+16,'C-KASET (60°) — plan + radyal kesit',7.5,'middle','bold')
KD=2.6
cxd,cyd = XD+20, YD+78
sector(cxd,cyd,KD*R0,KD*R1,-30,30,1.2,'#111',FILL)
ln(cxd+KD*11,cyd,cxd+KD*31,cyd,1.3,BLU); ci(cxd+KD*RA,cyd,3,1.4,GRN,None,'#fff'); ci(cxd+KD*9,cyd,2.6,1,'#555',None,'#eee')
rc(cxd+KD*(R1-1),cyd-KD*3,KD*1.5,KD*6,.9,0,'#555',None,'#bbb')
ln(cxd+KD*R1*math.cos(math.radians(30))+6,cyd-KD*R1*math.sin(math.radians(30)),cxd+KD*R1*math.cos(math.radians(30))+6,cyd+KD*R1*math.sin(math.radians(30)),.7); tx(cxd+KD*R1*math.cos(math.radians(30))+16,cyd+3,'kiriş 32',5,'start','bold')
ln(cxd+KD*R0,cyd+KD*20,cxd+KD*R1,cyd+KD*20,.7); tx(cxd+KD*18,cyd+KD*20+9,'27,7 (r 5 → 32)',5,'middle','bold')
tx(cxd+KD*6,cyd-KD*8,'tip: dişli',4.4,'middle','','#555'); tx(cxd+KD*RA,cyd-KD*5,'ağız r 29',4.4,'middle','bold',GRN); tx(cxd+KD*R1+2,cyd+KD*8,'tutamak',4.2,'start','',GRY)
tx(cxd+KD*20,cyd+KD*4,'helezon',4.4,'middle','',BLU)
# radyal kesit
K5=3.2
dx_,dz_ = XD+22, YD+262
RXd=lambda r: dx_+K5*(r-5); DZ=lambda c: dz_-K5*c
poly([(RXd(5),DZ(32)),(RXd(32),DZ(32)),(RXd(32),DZ(11)),(RXd(29),DZ(7)),(RXd(29),DZ(0)),(RXd(13),DZ(0)),(RXd(13),DZ(7)),(RXd(5),DZ(15))],1.2,'#111',FILL)
poly([(RXd(5.3),DZ(28)),(RXd(31.7),DZ(28)),(RXd(31.7),DZ(11)),(RXd(29),DZ(7.3)),(RXd(13),DZ(7.3)),(RXd(5.3),DZ(15))],0,'none',MAT)
rc(RXd(12),DZ(7),K5*18,K5*7,1,2,'#111',None,'#fff'); ln(RXd(11.5),DZ(3.5),RXd(30.5),DZ(3.5),1,'#333')
r_=12.6
for pch in (2,2.2,2.5,2.8,3.1,3.4,3.7,4):
    path('M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f'%(RXd(r_),DZ(6.7),RXd(r_+pch/2),DZ(3.5),RXd(r_),DZ(0.3)),.8,'#111'); r_+=pch
ln(RXd(11),DZ(13),RXd(31),DZ(13),1.3,BLU)
for k in range(7):
    rr=12.5+k*2.8; s=1 if k%2==0 else -1; ln(RXd(rr),DZ(13),RXd(rr),DZ(13+s*4.5),.9,BLU)
rc(RXd(27.5),DZ(0),K5*2.5,K5*1,0,0,'none',None,'#fff'); arr(RXd(28.8),DZ(-1),RXd(28.8),DZ(-5),GRN,1.2)
rc(RXd(3),DZ(6),K5*5,K5*5,1,1,BLU,None,'#dfe7fb'); tx(RXd(5.5),DZ(2.5),'M',4.6,'middle','bold',BLU)
ci(RXd(9.5),DZ(3.5),K5*1.6,.9,'#555',None,'#eee')
tx(RXd(20),DZ(24),'helezon Ø7 · hatve 2→4 · 30 dev/dk',4.6,'middle','bold'); tx(RXd(20),DZ(19),'tarak Ø11 · 3 dev/dk (1:20 tipte)',4.6,'middle','bold',BLU)
tx(RXd(31),DZ(-6.5),'ağız → boşluk',4.4,'end','bold',GRN); tx(RXd(8),DZ(17.5),'eğimli uç',4.2,'middle','',GRY)
tx(XD+125,YD+290,'523 cm² × 32 = 16,7 L − V/uç 3,3 = 13,4 L → kaşar 5,5 kg · dolu ≤ 7,5 kg · 30°: 7,4 L → 4 kg',4.6,'middle','','#333')

# ================= ELEKTRİK & TAHRİK =================
XE,YE = 870,120
rc(XE,YE,560,400,1.4,4,'#111',None,'#fcfdff')
tx(XE+14,YE+22,'ELEKTRİK & TAHRİK — kasette elektrik yok, motor duvarda',10,'start','bold')
kx,ky = XE+16,YE+36
rc(kx,ky,262,180,1,3,'#999',None,'#fff'); tx(kx+131,ky+14,'TİP DİŞLİSİ — yandan meshler',7,'middle','bold')
rc(kx+60,ky+30,190,44,1,0,'#111',None,FILL); tx(kx+160,ky+42,'C-kaset (pasif) — tip ucu',5.4,'middle','',GRY)
ln(kx+90,ky+58,kx+240,ky+58,1.5,'#333'); tx(kx+170,ky+68,'helezon mili (yatay, x yönünde)',4.8,'middle','')
ci(kx+80,ky+58,10,1.1,'#111',None,'#eee'); ci(kx+58,ky+58,10,1.1,BLU,None,'#dfe7fb')
rc(kx+22,ky+70,50,30,1,2,'#111',None,'#eee'); tx(kx+47,ky+83,'M 40 W',5.4,'middle','bold'); tx(kx+47,ky+93,'yan duvar · enkoder',4.4,'middle','')
ln(kx+58,ky+68,kx+52,ky+72,1,BLU)
arr(kx+160,ky+24,kx+120,ky+24,AMB,1); tx(kx+170,ky+27,'kaset öne çekilir / arkadan gelir',4.6,'start','',AMB)
tx(kx+131,ky+118,'kaset raya itilince tip dişlisi motor dişlisine YANDAN girer',5,'middle','bold',BLU)
tx(kx+131,ky+130,'(pahlı diş) — arkadan öne alınan yedek de aynı yere oturur',5,'middle','','#333')
tx(kx+131,ky+144,'tarak 1:20 tipte, aynı milden · slip ring yok, kablo yok',5,'middle','',GRN)
tx(kx+131,ky+158,'sucuk kasetinde aynı dişli bıçak milini çevirir',5,'middle','',AMB)
tx(kx+131,ky+172,'kaset komple bulaşık makinesine girer',5,'middle','bold',GRN)
bx,by = XE+290,YE+36
rc(bx,by,254,180,1,3,'#999',None,'#fff'); tx(bx+127,by+14,'KONTROL ŞEMASI',7,'middle','bold')
rc(bx+80,by+22,94,24,1.1,3,'#111',None,'#f3f3f3'); tx(bx+127,by+33,'PLC · 24 V · CAN',5.8,'middle','bold')
items=[('M1 kaşar A',BLU),('M2 sucuk bıçak',BLU),('M3 kaşar B',BLU),('M4 kavurma',BLU),('M5 kuşbaşı',BLU),('klape ×4',BLU),('yük hücresi ×5',AMB),('RFID ×5 + raf',PUR),('soğutma +3',GRY),('kapı/klape sensör',GRY)]
for i,(ad,col) in enumerate(items):
    x_=bx+10+(i%2)*120; y_=by+54+(i//2)*23
    rc(x_,y_,112,18,.9,2,col,None,'#fff'); tx(x_+56,y_+12,ad,5.2,'middle','bold',col)
    ln(bx+127,by+46,x_+56,y_,.5,'#999')
tx(bx+127,by+172,'5 sürücü · 5 tartı · 1 PLC · ~345 W tepe',5.2,'middle','bold',GRN)
ny=YE+232
tx(XE+14,ny,'DOZAJ (sucuklu pide, KAT 1):',8,'start','bold')
seq=['① robot tepsiyi düzlem 1'+chr(39)+'e (123 cm) getirir, (31, 64,5) altına · M1: kaşar A helezonu ağızdan döker, spiral 14 sn',
     '② ray altı yük hücresi kaset ağırlık farkını okur → 80 g'+chr(39)+'da durur (±3 g) · tepsi 8 cm sağa: (39, 64,5)',
     '③ M2: bıçak çubuktan 12 dilim keser (12 × 0,6 sn), dilimler ağızdan tepsiye · kat değişmez → fırına',
     '④ kavurmalı: KAT 2 (74 cm): kaşar B (31, 64,5) + kavurma (39, 72) · kuşbaşılı: kuşbaşı (39, 57)',
     '⑤ kaset ≤ 1 doz (tartı) ya da saat doldu → DEĞİŞİM (sağ alt) · kuyruk boşken, ≤ 2/gün']
for i,s in enumerate(seq): tx(XE+14,ny+15+i*12.5,s,6.4,'start','','#333')
tx(XE+14,ny+86,'güç: 5×40 + klape 4×10 + soğutma 90 + PLC 15 → ~345 W tepe · ort. ~130 W',6.4,'start','bold',GRY)
tx(XE+14,ny+100,'yük hücresi kaset takılınca tartar (RFID + başlangıç) → her dozda fark → "boşaldı"; ayrı sensör yok',6.4,'start','','#333')
tx(XE+14,ny+114,'ağız kaset tabanında; kat tabanındaki delik yalnız çalışan pozisyonda (yedek pozisyonda taban kapalı)',6.4,'start','','#333')
tx(XE+14,ny+128,'soğuk hacim: kat 1, kat 2, raf 1, raf 2 ayrı izole kutular, önden klape; boşluklar dışarıda',6.4,'start','','#333')
tx(XE+14,ny+142,'tepsi düzlemleri 123 / 74 cm: kobot her ikisine ulaşır; bir pidede kat değişmez',6.4,'start','bold',BLU)

# ================= STOK · DEĞİŞİM =================
XT,YT = 870,540
rc(XT,YT,560,360,1.4,4)
tx(XT+14,YT+22,'STOK · DEĞİŞİM · HAFTALIK — yedek her kasetin arkasında',10,'start','bold')
rows=[('KAŞAR','A, B çalışan + C, D arkalarında + E, F, G, H rafta = 8 × 5,5 = 44 kg = 6,8 gün (≈ hafta; 9. kaset raf 2 arkaya konabilir)'),
      ('SUCUK','çubuk kaseti sabit: ~30 çubuk Ø4×25 = 9,5 kg ≈ hafta; arkasında 2. kaset (eleman) — robot dokunmaz'),
      ('KAV / KUŞ','30° kaset 4 kg (3 gün taze) · yedekleri arkada (+3, orada çözülür) · donmuşlar STORE −18 (29 ≥ 32? → yatık: 28 ✓)'),
      ('RAF 1','kaşar E, F önde · G, H arkada (FIFO)'),
      ('RAF 2','PARK ×2 önde (boşalan kaset buraya) · kav / kuş çözülme ×2 arkada (STORE'+chr(39)+'dan 1 gün önce)'),
      ('ELEMAN','haftada 1: 8 kaşar, sucuk kaseti, 1+1 taze + 2+2 donmuş küçük; boşları toplar, yıkar')]
for i,(a,b) in enumerate(rows):
    yy=YT+46+i*17; tx(XT+14,yy,a,6.8,'start','bold'); tx(XT+82,yy,b,6.2,'start','','#333')
ln(XT+12,YT+152,XT+548,YT+152,.8,'#bbb')
tx(XT+14,YT+170,'DEĞİŞİM (kaşar A boşaldı) — 2 hamle + 1, ~50 sn:',7.5,'start','bold',BLU)
seq2=['① KAT 1 klapesi açılır → robot boş A'+chr(39)+'yı tutamaktan çeker → RAF 2 PARK yuvasına koyar',
      '② arkadaki C'+chr(39)+'yi aynı raydan öne çeker: tip dişlisi meshler, RFID, tartı = başlangıç → klape kapanır',
      '③ (fırsat bulunca) RAF 1'+chr(39)+'den E'+chr(39)+'yi alıp KAT 1 arka yuvaya sürer → boş A'+chr(39)+'yı E'+chr(39)+'nin yuvasına',
      '④ sucuk: eleman · kav/kuş: aynı mantık, yedeği arkada çözülmüş bekler']
for i,s in enumerate(seq2): tx(XT+14,YT+186+i*12.5,s,6.4,'start','','#333')
tx(XT+14,YT+246,'v14 (revolver) ile fark: dönen kütle 55 kg → 0 · tabla motoru yok · dozaj noktası 1 → 5 (2 düzlem) · motor 3 → 5',6.4,'start','bold',GRY)
tx(XT+14,YT+259,'kaset tipi: 60° ve 30° (aynı gövde ailesi, aynı tip dişlisi) · kaşar 5,5 kg / kaset (revolverde 4)',6.4,'start','',GRY)
tx(XT+14,YT+272,'derinlik kullanımı: 15 kanal + 33 yedek + 33 çalışan + 3 klape = 84 ✓ (v13'+chr(39)+'teki arka boşluk kalmadı)',6.4,'start','',GRN)
tx(XT+14,YT+292,'AÇIK: kaşar 45° V + helezon akışı prototip · 60° sektör rafa 2 yan yana 64 ≤ 70 (3 cm pay) · klape contası',6.2,'start','',AMB)
tx(XT+14,YT+305,'· kav/kuş 30° kasetin STORE −18 çekmecesine yatık girmesi (28 ≤ 29) · sucuk çubuk kaseti detayı',6.2,'start','',AMB)
tx(XT+14,YT+318,'· sol ağız x 31 = süpürme sol duvara tam değer (pay 0) → duvar iç yüzü düz, çıkıntısız olmalı',6.2,'start','',AMB)
tx(XT+14,YT+336,'Not: 2 düzlem = tepsi 123 ve 74 cm; robot kolu (⑦) her ikisine ulaşmalı — HAT v45 KONTROL'+chr(39)+'e giriyor',6.2,'start','bold',BLU)

# ================= KONTROL =================
YK=935
rc(60,YK,1370,215,1.6,4)
tx(76,YK+24,'KONTROL — kurallar ve HAT v45 etkisi',11,'start','bold')
rows=[('① çıkış bandı: ağızlar x 31 · 39 ∈ [31,39] ✓ (bant kenarları) · y 57-72 ≥ 31 ✓ · süpürme R31: sol x 0-62, sağ x 8-70 → duvar içinde, pay 0 (düz iç yüzey şart)',GRN),
      ('② erişim: çalışan kasetlerin önünde hiçbir şey yok ✓ · yedek aynı rayda arkada, boşalan çıkınca öne çekilir ✓ · raf 2 derin FIFO ✓ · park = raf 2 ön',GRN),
      ('③ KARAR C doğrudan: sektör gövde, V-oluk, helezon, tarak, ağız dış uçta, tip dişlisi duvarda motora; huni yok, dönen parça yok, kasette elektrik yok ✓',GRN),
      ('④ dikey 27+35+14+35+14+36+36 = 197 ✓ · 70×84 aynı · derinlik tam kullanıldı ✓ · robot yükü ≤ 7,5 kg ✓ · 2 dozaj düzlemi 123 / 74 cm',GRN),
      ('⑤ HAT v45: TOPPING bloğu bu çizimle (çark katı yok, 2 boşluk) · STORE v4: −18 kaset çekmecesi 29 → 30° kaset yatık 28 ✓ · KONTROL ⑧⑨ + ⑦ (iki düzlem)',BLU),
      ('⑥ AÇIK: kaşar 45° V + helezon prototip · klape/soğuk hacim · sucuk çubuk kaseti detayı · duvar dibi üçgen boşluklar (kablo/hava) · kobot iki düzlem',AMB)]
for i,(s,c) in enumerate(rows):
    tx(76,YK+46+i*27,s,7.4,'start','',c)
tx(W-40,H-12,'AUTOKITCH · arastirma/3_TOPPING/ist3_topping_detay_v15 · 4 Eyl 2026',7,'end','',GRY)
o.append('</svg>')
svg = chr(10).join(o)
xml.dom.minidom.parseString(svg.encode('utf-8'))
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\ist3_topping_detay_v15.svg"
io.open(out,'w',encoding='utf-8').write(svg)
print('yazildi + XML gecerli | 60° alan %.0f cm2, 30° %.0f' % (A60, A30))
