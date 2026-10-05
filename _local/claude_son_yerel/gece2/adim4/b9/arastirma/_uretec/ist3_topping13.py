# -*- coding: utf-8 -*-
# TOPPING v13 — KARAR C (helezonlu kaset) ile SABİT dizilim, revolver YOK · 2 kat + 2 dozaj düzlemi · tüm ağızlar bantta, tüm kasetler önden · on / 2 yan kesit / ust / elektrik / stok
import io, math
W, H = 1460, 1150
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
    s=str(s).replace('&','&amp;').replace('<','&lt;')
    o.append('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="%s" font-weight="%s" fill="%s" font-family="Segoe UI, Arial, sans-serif">%s</text>' % (x,y,fs,anc,fw or 'normal',col,s))
def poly(pts,sw=1,c='#111',f='none',d=None):
    o.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (' '.join('%.1f,%.1f'%p for p in pts),f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def arr(x1,y1,x2,y2,c='#c0392b',w=1.2):
    ln(x1,y1,x2,y2,w,c); a=math.atan2(y2-y1,x2-x1)
    for s in (1,-1): ln(x2,y2,x2-6*math.cos(a-s*.42),y2-6*math.sin(a-s*.42),w,c)

GRN, RED, BLU, GRY, AMB, PUR = '#1d7a4f', '#c0392b', '#1a49b8', '#666', '#b7791f', '#6b4fa8'
FILL, PU, KAS = '#f1efe8', '#e9e4d6', '#fdf6e3'
K = 2.5
# dikey (ustten): teknik 27 · L1 kaset 32 + cerceve 3 + bosluk1 14 · L2 kaset 32 + 3 + bosluk2 14 · raf A 36 · raf B 36
Z = [('teknik',27,'#f3f3f3'),('L1',32,'#fff'),('ç',3,'#ccc'),('BOŞLUK 1',14,'#eef3ff'),('L2',32,'#fff'),('ç',3,'#ccc'),('BOŞLUK 2',14,'#eef3ff'),('RAF A',36,'#f7f6f2'),('RAF B',36,'#f7f6f2')]
assert sum(z[1] for z in Z)==197
zt={}; acc=0
for ad,h,_ in Z: zt.setdefault(ad,[]).append((acc,h)); acc+=h
zL1=zt['L1'][0][0]; zB1=zt['BOŞLUK 1'][0][0]; zL2=zt['L2'][0][0]; zB2=zt['BOŞLUK 2'][0][0]; zRA=zt['RAF A'][0][0]; zRB=zt['RAF B'][0][0]

o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H))
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,42,'AUTOKITCH — İSTASYON 3 · TOPPING v13 (4 Eyl 2026) — KARAR C ile SABİT DİZİLİM (revolver yok): helezonlu kasetler · 2 KAT + 2 DOZAJ DÜZLEMİ · 70 × 197 × 84 · ölçüler cm',15,'start','bold')
tx(30,66,'Helezon ağzı kasetin İÇ ucunda → kaset yan duvara yaslanır, ağız 31–39 bandına düşer. Her kat: sol kaşar + sağ diğer malzeme, önde, arkasında hiçbir şey yok → her kaset doğrudan çekilir. Kat 1 = sucuklu pide, Kat 2 = kavurma/kuşbaşı; tepsi pide boyunca kat değiştirmez.',9.5,'start','','#444')
ln(30,78,W-30,78,.8,'#999')

# ================= ÖN GÖRÜNÜŞ =================
X0,Y0 = 60,120
tx(X0+K*35,Y0-10,'ÖN GÖRÜNÜŞ (robot tarafı) 1:4',9,'middle','bold')
rc(X0,Y0,K*70,K*197,2.2)
zz=0
for ad,h,col in Z:
    rc(X0,Y0+K*zz,K*70,K*h,.8,0,'#111',None,col); zz+=h
rc(X0+K*3,Y0+K*3,K*30,K*21,1,2,'#111',None,'#fff'); tx(X0+K*18,Y0+K*12,'SOĞUTMA',6.5,'middle','bold'); tx(X0+K*18,Y0+K*18,'1/12 HP · +3',5.6,'middle','')
rc(X0+K*37,Y0+K*3,K*30,K*21,1,2,'#111',None,'#fff'); tx(X0+K*52,Y0+K*10,'ELEKTRİK',6.5,'middle','bold'); tx(X0+K*52,Y0+K*15,'PLC · 24 V · 6 sürücü',5,'middle','')
def kaset_on(x,z,w,h,ad,alt,col='#111',f=KAS):
    rc(X0+K*x,Y0+K*z,K*w,K*h,1.1,1,col,None,f); tx(X0+K*(x+w/2),Y0+K*(z+h/2)-1,ad,6,'middle','bold',col); tx(X0+K*(x+w/2),Y0+K*(z+h/2)+7,alt,5,'middle','',col)
# L1: kasar A (sol) | sucuk cubuk (sag)
kaset_on(2,zL1+2,30,28,'KAŞAR A','30×24×32 helezon')
kaset_on(38,zL1+2,30,28,'SUCUK çubuk','30×74×28 bıçak · sabit')
tx(X0+K*70+6,Y0+K*(zL1+10),'KAT 1 · 32: kaşar A + sucuk',6.5,'start','bold'); tx(X0+K*70+6,Y0+K*(zL1+18),'motorlu izole klape ×2 (sol/sağ)',5.6,'start','',BLU)
# bosluk 1: agizlar x 32 / 38
for xx_,col in ((32,GRN),(38,GRN)): ln(X0+K*xx_,Y0+K*zB1,X0+K*xx_,Y0+K*(zB1+3),2,col)
tx(X0+K*35,Y0+K*(zB1+6.5),'ağızlar x 32 · 38',5.2,'middle','bold',GRN)
el(X0+K*35,Y0+K*(zB1+11.5),K*17,K*1.1,1.1,BLU,None,'#dfe7fb')
tx(X0+K*70+6,Y0+K*(zB1+8),'BOŞLUK 1 · 14 · dozaj düzlemi 1 (sucuklu)',6.3,'start','',BLU)
# L2: kasar B | kavurma (ust) + kusbasi (alt)
kaset_on(2,zL2+2,30,28,'KAŞAR B','30×24×32 helezon')
kaset_on(38,zL2+2,30,13,'KAVURMA','30×24×14 · ağız uzantılı')
kaset_on(38,zL2+16,30,13,'KUŞBAŞI','30×24×14')
tx(X0+K*70+6,Y0+K*(zL2+10),'KAT 2 · 32: kaşar B + kav/kuş (üst üste)',6.5,'start','bold'); tx(X0+K*70+6,Y0+K*(zL2+18),'klape ×2',5.6,'start','',BLU)
for xx_ in (32,34,38): ln(X0+K*xx_,Y0+K*zB2,X0+K*xx_,Y0+K*(zB2+3),2,GRN)
tx(X0+K*35,Y0+K*(zB2+6.5),'ağızlar x 32 · 34 · 38',5.2,'middle','bold',GRN)
el(X0+K*35,Y0+K*(zB2+11.5),K*17,K*1.1,1.1,BLU,None,'#dfe7fb')
tx(X0+K*70+6,Y0+K*(zB2+8),'BOŞLUK 2 · 14 · dozaj düzlemi 2 (kav/kuş)',6.3,'start','',BLU)
# raflar
for zr,pair,ad in ((zRA,('KAŞAR C','KAŞAR D'),'RAF A'),(zRB,('kav. çözülme','kuş. çözülme'),'RAF B')):
    for i,lab in enumerate(pair):
        rc(X0+K*(2+i*36),Y0+K*(zr+3),K*30,K*30,1,1,'#111',None,FILL); tx(X0+K*(17+i*36),Y0+K*(zr+18),lab,5.8,'middle','bold')
    tx(X0+K*70+6,Y0+K*(zr+13),'%s 36 · önde 2 + arkada 2 yuva' % ad,6.3,'start','',GRY)
    tx(X0+K*70+6,Y0+K*(zr+21),'arka: %s' % ('kaşar E · F' if ad=='RAF A' else 'boş · boş (değişim parkı)'),5.6,'start','','#333')
ln(X0,Y0+K*197+16,X0+K*70,Y0+K*197+16,.8); tx(X0+K*35,Y0+K*197+28,'70',8,'middle','bold')
ln(X0-14,Y0,X0-14,Y0+K*197,.8); tx(X0-18,Y0+K*98,'197',8,'end','bold')
zz=0
for ad,h,_ in Z: tx(X0-18,Y0+K*(zz+h/2)+3,'%g'%h,5.2,'end','',GRY); zz+=h
tx(X0+K*35,Y0+K*197+42,'27+32+3+14+32+3+14+36+36 = 197 ✓',7,'middle','bold',GRN)

# ================= YAN KESİTLER =================
def yan(XS,baslik,sol):
    tx(XS+K*42,Y0-10,baslik,9,'middle','bold')
    rc(XS,Y0,K*84,K*197,2.2)
    zz=0
    for ad,h,col in Z:
        rc(XS,Y0+K*zz,K*84,K*h,.8,0,'#111',None,col); zz+=h
    rc(XS+K*2,Y0+K*2,K*80,K*23,1,2,'#111',None,'#fff'); tx(XS+K*42,Y0+K*14,'teknik (üstten servis)',5.6,'middle','')
    def kaset_y(y0,d,z,h,ad,alt,f=KAS):
        rc(XS+K*y0,Y0+K*z,K*d,K*h,1.1,1,'#111',None,f); tx(XS+K*(y0+d/2),Y0+K*(z+h/2)-1,ad,5.8,'middle','bold'); tx(XS+K*(y0+d/2),Y0+K*(z+h/2)+7,alt,4.8,'middle','')
    if sol:
        for zL,ad in ((zL1,'KAŞAR A'),(zL2,'KAŞAR B')):
            kaset_y(55,24,zL+2,28,ad,'helezon y 67')
            # helezon (x yonunde, kesitte daire) + tarak + V
            ci(XS+K*67,Y0+K*(zL+27),K*3.5,1,'#111',None,'#fff'); ci(XS+K*67,Y0+K*(zL+20),K*5,.7,BLU,'3,2')
            ln(XS+K*57,Y0+K*(zL+21),XS+K*63.5,Y0+K*(zL+27),.8,AMB); ln(XS+K*77,Y0+K*(zL+21),XS+K*70.5,Y0+K*(zL+27),.8,AMB)
            rc(XS+K*5,Y0+K*(zL+2),K*45,K*28,.8,2,'#999','4,3','#fafafa'); tx(XS+K*27,Y0+K*(zL+15),'BOŞ (arka) — robot erişemez',5.2,'middle','',GRY)
            rc(XS+K*82,Y0+K*(zL+1),K*2,K*30,1,0,BLU,None,'#dfe7fb')
            ln(XS+K*67,Y0+K*(zL+30),XS+K*67,Y0+K*(zL+35),1.6,GRN)
        for zB in (zB1,zB2):
            tx(XS+K*67,Y0+K*(zB+6),'ağız y 67',5,'middle','bold',GRN)
            rc(XS+K*38,Y0+K*(zB+10.5),K*34,K*1.5,1.1,BLU,None,'#dfe7fb'); rc(XS+K*72,Y0+K*(zB+9.5),K*12,K*3,1,BLU,None,'#dfe7fb')
            tx(XS+K*50,Y0+K*(zB+8.5),'tepsi en geride (m. y 53)',4.6,'middle','',BLU)
        for zr,fr,bk in ((zRA,'KAŞAR C','KAŞAR E'),(zRB,'kav. çözülme','boş')):
            kaset_y(50,30,zr+3,30,fr,'ön',FILL); kaset_y(12,30,zr+3,30,bk,'arka (FIFO)','#f7f3ec')
            rc(XS+K*82,Y0+K*(zr+1),K*2,K*34,1,0,BLU,None,'#dfe7fb')
        tx(XS+K*42,Y0+K*197+28,'sol kolon x 17: kaşar A/B önde (y 55-79), arkası boş · raf 2 derin',6.3,'middle','','#333')
    else:
        # sag kolon: L1 sucuk cubuk magazini y 5-79 (sabit), L2 kavurma ust + kusbasi alt y 55-79
        rc(XS+K*5,Y0+K*(zL1+2),K*74,K*28,1.1,1,'#111',None,KAS); tx(XS+K*42,Y0+K*(zL1+12),'SUCUK ÇUBUK MAGAZİNİ (sabit, eleman haftalık)',5.6,'middle','bold')
        for k in range(14): rc(XS+K*(8+k*5),Y0+K*(zL1+5),K*3.6,K*22,.7,1,'#555',None,'#f4ece6')
        arr(XS+K*30,Y0+K*(zL1+29.2),XS+K*60,Y0+K*(zL1+29.2),AMB,1); tx(XS+K*45,Y0+K*(zL1+28.5)-4,'çubuklar öne kayar (eğim 8°)',4.8,'middle','',AMB)
        rc(XS+K*64,Y0+K*(zL1+24),K*10,K*6,1,1,RED,None,'#fdeeee'); tx(XS+K*69,Y0+K*(zL1+28),'bıçak',4.8,'middle','bold',RED)
        ln(XS+K*67,Y0+K*(zL1+30),XS+K*67,Y0+K*(zL1+35),1.6,GRN); tx(XS+K*67,Y0+K*(zB1+6),'ağız (38, 67)',5,'middle','bold',GRN)
        rc(XS+K*82,Y0+K*(zL1+1),K*2,K*30,1,0,BLU,None,'#dfe7fb')
        rc(XS+K*55,Y0+K*(zL2+2),K*24,K*13,1.1,1,'#111',None,KAS); tx(XS+K*67,Y0+K*(zL2+9),'KAVURMA 14',5.6,'middle','bold')
        rc(XS+K*55,Y0+K*(zL2+16),K*24,K*13,1.1,1,'#111',None,KAS); tx(XS+K*67,Y0+K*(zL2+23),'KUŞBAŞI 14',5.6,'middle','bold')
        ci(XS+K*67,Y0+K*(zL2+13),K*2.5,.9,'#111',None,'#fff'); ci(XS+K*67,Y0+K*(zL2+27),K*2.5,.9,'#111',None,'#fff')
        rc(XS+K*5,Y0+K*(zL2+2),K*48,K*28,.8,2,'#999','4,3','#fafafa'); tx(XS+K*29,Y0+K*(zL2+15),'BOŞ (arka)',5.2,'middle','',GRY)
        ln(XS+K*67,Y0+K*(zL2+30),XS+K*67,Y0+K*(zL2+35),1.6,GRN); tx(XS+K*67,Y0+K*(zB2+6),'ağız (34 · 38, 67)',5,'middle','bold',GRN)
        tx(XS+K*60,Y0+K*(zL2+15.2),'uzantı 14 ↓',4.4,'end','bold',GRN)
        rc(XS+K*82,Y0+K*(zL2+1),K*2,K*30,1,0,BLU,None,'#dfe7fb')
        for zB in (zB1,zB2):
            rc(XS+K*38,Y0+K*(zB+10.5),K*34,K*1.5,1.1,BLU,None,'#dfe7fb'); rc(XS+K*72,Y0+K*(zB+9.5),K*12,K*3,1,BLU,None,'#dfe7fb')
        for zr,fr,bk in ((zRA,'KAŞAR D','KAŞAR F'),(zRB,'kuş. çözülme','boş')):
            rc(XS+K*50,Y0+K*(zr+3),K*30,K*30,1.1,1,'#111',None,FILL); tx(XS+K*65,Y0+K*(zr+18),fr,5.6,'middle','bold')
            rc(XS+K*12,Y0+K*(zr+3),K*30,K*30,1.1,1,'#111',None,'#f7f3ec'); tx(XS+K*27,Y0+K*(zr+18),bk,5.6,'middle','bold')
            rc(XS+K*82,Y0+K*(zr+1),K*2,K*34,1,0,BLU,None,'#dfe7fb')
        tx(XS+K*42,Y0+K*197+28,'sağ kolon x 53: sucuk magazini tam derinlik (sabit), kav/kuş önde üst üste',6.3,'middle','','#333')
    ln(XS,Y0+K*197+16,XS+K*84,Y0+K*197+16,.8); tx(XS+K*42,Y0+K*197+40,'84 · arka ← y → ön',7,'middle','bold')
yan(310,'YAN KESİT — SOL KOLON (x 17) 1:4',True)
yan(560,'YAN KESİT — SAĞ KOLON (x 53) 1:4',False)

# ================= ÜST GÖRÜNÜŞ KAT 1 / KAT 2 =================
XU,YU = 810,120
KU=2.2
def plan(X,Y,baslik,kat):
    tx(X+KU*35,Y-8,baslik,8.5,'middle','bold')
    rc(X,Y,KU*70,KU*84,1.4)
    rc(X+KU*31,Y,KU*8,KU*84,0,0,'none',None,'#dff3e6')
    rc(X,Y,KU*70,KU*5,0,0,'none',None,'#e5e5e5'); tx(X+KU*35,Y+KU*3.8,'arka duvar / izolasyon',4.4,'middle','',GRY)
    if kat==1:
        rc(X+KU*2,Y+KU*55,KU*30,KU*24,1.1,1,'#111',None,KAS); tx(X+KU*17,Y+KU*66,'KAŞAR A',6,'middle','bold'); tx(X+KU*17,Y+KU*72,'helezon → iç uç',4.6,'middle','')
        rc(X+KU*38,Y+KU*5,KU*30,KU*74,1.1,1,'#111',None,KAS); tx(X+KU*53,Y+KU*30,'SUCUK',6,'middle','bold'); tx(X+KU*53,Y+KU*36,'çubuk magazini',4.6,'middle',''); tx(X+KU*53,Y+KU*41,'(sabit)',4.6,'middle','')
        rc(X+KU*38,Y+KU*62,KU*8,KU*10,1,1,RED,None,'#fdeeee'); tx(X+KU*42,Y+KU*68,'bıçak',4.2,'middle','bold',RED)
        rc(X+KU*2,Y+KU*5,KU*30,KU*46,.8,2,'#999','4,3','#fafafa'); tx(X+KU*17,Y+KU*28,'boş',5,'middle','',GRY)
        outs=((32,67),(38,67))
    else:
        rc(X+KU*2,Y+KU*55,KU*30,KU*24,1.1,1,'#111',None,KAS); tx(X+KU*17,Y+KU*66,'KAŞAR B',6,'middle','bold'); tx(X+KU*17,Y+KU*72,'helezon → iç uç',4.6,'middle','')
        rc(X+KU*38,Y+KU*55,KU*30,KU*24,1.1,1,'#111',None,KAS); tx(X+KU*53,Y+KU*64,'KAVURMA (üst)',5.4,'middle','bold'); tx(X+KU*53,Y+KU*71,'KUŞBAŞI (alt)',5.4,'middle','bold')
        rc(X+KU*2,Y+KU*5,KU*66,KU*46,.8,2,'#999','4,3','#fafafa'); tx(X+KU*35,Y+KU*28,'boş (arka) — ileride',5,'middle','',GRY)
        outs=((32,67),(34,67),(38,67))
    for (ox,oy) in outs:
        ci(X+KU*ox,Y+KU*oy,KU*31,.8,GRN,'5,3'); ci(X+KU*ox,Y+KU*oy,2.6,1.3,GRN,None,'#fff')
    # helezon oku (x yonunde ic uca)
    arr(X+KU*5,Y+KU*67,X+KU*30,Y+KU*67,'#333',1); tx(X+KU*17,Y+KU*63,'helezon',4.4,'middle','','#333')
    if kat==2: arr(X+KU*65,Y+KU*67,X+KU*40,Y+KU*67,'#333',1)
    # dis uc yan disli
    rc(X-4,Y+KU*63,4,KU*8,1,0,BLU,None,'#dfe7fb'); tx(X-6,Y+KU*60,'M',4.8,'end','bold',BLU)
    if kat==2: rc(X+KU*70,Y+KU*63,4,KU*8,1,0,BLU,None,'#dfe7fb'); tx(X+KU*70+6,Y+KU*60,'M',4.8,'start','bold',BLU)
    tx(X+KU*35,Y+KU*84+10,'süpürme R31: x 1–69 ✓ · y 36–98 ✓ (ön açık)',5.4,'middle','bold',GRN)
plan(XU,YU,'ÜST — KAT 1 (sucuklu düzlem)',1)
plan(XU,YU+KU*84+40,'ÜST — KAT 2 (kavurma/kuşbaşı düzlemi)',2)
tx(XU+KU*35,YU+2*KU*84+62,'kasetler ÖNDE (y 55-79): arkalarında hiçbir şey yok →',5.6,'middle','bold','#333')
tx(XU+KU*35,YU+2*KU*84+74,'robot düz çeker; ağız y 67 ≥ 31 ✓; arka 50 cm boş kalıyor',5.6,'middle','','#333')

# ================= ELEKTRİK & TAHRİK =================
XE,YE = 1000,120
rc(XE,YE,430,420,1.4,4,'#111',None,'#fcfdff')
tx(XE+14,YE+22,'ELEKTRİK & TAHRİK',10,'start','bold')
tx(XE+14,YE+38,'Kasette elektrik yok. Helezon + tarak kasetin içinde; helezon',7,'start','','#333')
tx(XE+14,YE+50,'milinin DIŞ ucunda düz dişli. Kaset öne-arkaya raylarda kayar;',7,'start','','#333')
tx(XE+14,YE+62,'sona itilince dişli, yan duvardaki motor dişlisine YANDAN girer',7,'start','','#333')
tx(XE+14,YE+74,'(pahlı diş — kendi hizalanır). Kavrama için ek hareket yok.',7,'start','','#333')
# yan disli detay
gx,gy = XE+30,YE+90
rc(gx,gy,180,110,1,3,'#999',None,'#fff'); tx(gx+90,gy+13,'YAN DİŞLİ KAVRAMA',6.5,'middle','bold')
rc(gx+40,gy+30,120,40,1,0,'#111',None,KAS); tx(gx+100,gy+45,'kaset (pasif)',5.4,'middle','',GRY)
ln(gx+50,gy+58,gx+150,gy+58,1.4,'#333'); tx(gx+110,gy+66,'helezon mili',4.6,'middle','')
ci(gx+44,gy+58,9,1,'#111',None,'#eee'); ci(gx+30,gy+58,9,1,BLU,None,'#dfe7fb')
rc(gx+8,gy+72,44,26,1,2,'#111',None,'#eee'); tx(gx+30,gy+83,'M 40 W',5.4,'middle','bold'); tx(gx+30,gy+92,'yan duvarda',4.6,'middle','')
arr(gx+100,gy+22,gx+70,gy+22,AMB,1); tx(gx+120,gy+25,'kaset öne çekilir',4.6,'start','',AMB)
tx(gx+90,gy+106,'motor sabit · kaset dişlisi yandan meshler',4.8,'middle','bold',BLU)
# kontrol semasi
bx,by = XE+225,YE+90
rc(bx,by,190,110,1,3,'#999',None,'#fff'); tx(bx+95,by+13,'KONTROL',6.5,'middle','bold')
rc(bx+55,by+20,80,20,1.1,3,'#111',None,'#f3f3f3'); tx(bx+95,by+33,'PLC · 24 V · CAN',5.4,'middle','bold')
items=[('M1 kaşar A',BLU),('M2 sucuk bıçak',BLU),('M3 kaşar B',BLU),('M4 kavurma',BLU),('M5 kuşbaşı',BLU),('klape ×6',BLU),('yük hücresi ×5',AMB),('RFID ×5',PUR)]
for i,(ad,col) in enumerate(items):
    x_=bx+8+(i%2)*92; y_=by+46+(i//2)*15
    rc(x_,y_,84,12,.9,2,col,None,'#fff'); tx(x_+42,y_+8.5,ad,4.6,'middle','bold',col)
tx(bx+95,by+106,'6 sürücü · 5 tartı · tek PLC',4.8,'middle','bold',GRN)
ny=YE+214
tx(XE+14,ny,'DOZAJ (bir sucuklu pide, KAT 1):',7.5,'start','bold')
seq=['① robot tepsiyi düzlem 1'+chr(39)+'e getirir (yükseklik 110), ağız (32, 67) altına',
     '② M1 döner: kaşar A helezonu iç uçtan döker, robot spiral 14 sn; yük hücresi',
     '   kaset ağırlık farkını okur → 80 g'+chr(39)+'da durur (±3 g)',
     '③ tepsi (38, 67) altına ötelenir (6 cm): M2 bıçak 12 dilim keser (12 × 0,6 sn)',
     '④ kat değişmez → fırına. Kavurmalı: aynı akış KAT 2'+chr(39)+'de (kaşar B + kavurma)',
     '⑤ kaset boşaldı (tartı) / saat doldu → değişim (sağ alt)']
for i,s in enumerate(seq): tx(XE+14,ny+15+i*12.5,s,6.6,'start','','#333')
tx(XE+14,ny+96,'güç: 5 × 40 W + klape 6 × 10 + soğutma 90 + PLC 15 → ~365 W tepe · ort. ~130 W',6.6,'start','bold',GRY)
tx(XE+14,ny+110,'2 dozaj düzlemi: tepsi yüksekliği 110 / 61 cm (robot kolu her ikisine ulaşır)',6.6,'start','','#333')
tx(XE+14,ny+124,'kaşar A ve B yedeği aynı: robot hangisi boşsa onu değiştirir, iki kat birbirini yedekler',6.6,'start','',GRN)
tx(XE+14,ny+138,'yük hücresi kaset rayının altında: kaset takılınca tartılır (RFID + başlangıç ağırlığı)',6.6,'start','','#333')
tx(XE+14,ny+152,'sucuk bıçağı: çubuk eğimli tabanda öne kayar, dış uçtan itilir, 3 mm dilim → ağız',6.6,'start','','#333')
tx(XE+14,ny+166,'kavurma ağız uzantısı 14 cm kasetin parçası (sökülür); kuşbaşı ağzı 4 cm yanında',6.6,'start','','#333')
tx(XE+14,ny+180,'klapeler: her kaset cebi izole kutu, öne açılır kapak; boşluklar soğuk hacim dışında',6.6,'start','','#333')

# ================= STOK · DEĞİŞİM =================
XT,YT = 1000,560
rc(XT,YT,430,330,1.4,4)
tx(XT+14,YT+22,'STOK · DEĞİŞİM · HAFTALIK',10,'start','bold')
rows=[('KAŞAR','30×24×32 = 23 L − V 4 = 19 L → 7,8 kg (dolu 10,3 kg ≤ 12 ✓)'),
      ('','A+B çalışan 15,6 kg = 2,4 gün · C D E F rafta → 6 × 7,8 = 47 kg = 7,2 gün ✓'),
      ('SUCUK','çubuk magazini sabit: 42 çubuk Ø4×25 = 13 kg ≥ 10 kg/hafta ✓ eleman doldurur'),
      ('KAV / KUŞ','30×24×14 = 10 L − V 3 = 7 L → 3,8 kg ✓ (3,5) · 3 gün taze'),
      ('','yedek 2+2 donmuş STORE −18 (29 ≥ 14 ✓) → RAF B'+chr(39)+'de 1 gün çözülür'),
      ('RAF A','kaşar C · D önde, E · F arkada (FIFO)'),
      ('RAF B','kav / kuş çözülme önde · boş · boş arkada (değişim parkı)'),
      ('ELEMAN','haftada 1: 6 kaşar kaseti, sucuk magazini, 1+1 taze küçük; boşları alır, yıkar')]
for i,(a,b) in enumerate(rows):
    yy=YT+44+i*16; tx(XT+14,yy,a,6.8,'start','bold'); tx(XT+72,yy,b,6.5,'start','','#333')
ln(XT+12,YT+178,XT+418,YT+178,.8,'#bbb')
tx(XT+14,YT+196,'DEĞİŞİM (kaşar A boşaldı) — 4 hamle, ~1 dk:',7.5,'start','bold',BLU)
seq2=['① KAT 1 sol klape açılır → robot A'+chr(39)+'yı çeker → RAF B arkadaki boş yuvaya (ön boşsa)',
      '② RAF A → kaşar C'+chr(39)+'yi çeker → KAT 1 sol raya sürer: dişli meshler, RFID, tartı',
      '③ klape kapanır · C boşalınca D; D gidince E öne düşer (FIFO)',
      '④ kav/kuş: RAF B çözülmüş ↔ KAT 2 sağ boş · sucuk: eleman']
for i,s in enumerate(seq2): tx(XT+14,YT+212+i*12.5,s,6.6,'start','','#333')
tx(XT+14,YT+272,'v12 (revolver) ile fark: motor 3 → 5 · dönen kütle 55 kg → 0 · değişim 6 → 4 hamle',6.6,'start','bold',GRY)
tx(XT+14,YT+285,'dozaj noktası 1 → 5 (2 düzlem) · dilim tipi 1 → 3 kaset tipi · arka 50 cm boş (~120 L)',6.6,'start','',GRY)
tx(XT+14,YT+298,'kaşar dilimi 4 kg → 7,8 kg (haftalık 12 → 6 kaset) · sabit huni/çark katı yok',6.6,'start','',GRY)
tx(XT+14,YT+316,'Açık: arka boş hacim (84 derinlik tartışması) · V 45° helezon prototip · klape ×6 contası',6.4,'start','',AMB)

# ================= KONTROL =================
YK=930
rc(60,YK,1370,190,1.6,4)
tx(76,YK+24,'KONTROL — kurallar ve HAT v45 etkisi',11,'start','bold')
rows=[('① çıkış bandı: 5 ağız x 32/34/38 ∈ [31,39] ✓ · y 67 ≥ 31 ✓ · süpürme R31 x 1–69 ✓ (sağ 69 ≤ 70 ✓, sol 1 ≥ 0 ✓)',GRN),
      ('② erişim: her çalışan kasetin önünde hiçbir şey yok ✓ · raf FIFO 2 derin (yalnız yedekler) ✓ · sucuk magazini robot değil eleman ✓',GRN),
      ('③ KARAR C: helezon kasetin içinde, ağız iç uçta, huni yok, sabit çark yok, kasette elektrik yok, yan dişli kavrama ✓',GRN),
      ('④ dikey 197 ✓ · 70×84 aynı · robot yükü ≤ 10,3 kg ✓ · 2 dozaj düzlemi 110 / 61 cm — kobot erişimi kontrol (⑦ ile birlikte)',AMB),
      ('⑤ HAT v45: TOPPING bloğu bu çizimle; çark katı yok; KONTROL ⑧⑨ güncellenir · STORE v4 değişmez (kav/kuş kaseti 14 ≤ 29 ✓)',BLU),
      ('⑥ AÇIK: arka 50 cm × 2 kat boş — ya derinlik 84 → 60 (hat kuralı bozulur) ya da eleman stoğu için arka kapak · kaşar V 45° + helezon prototip',AMB)]
for i,(s,c) in enumerate(rows):
    tx(76+(i%2)*690,YK+48+(i//2)*44,s[:120],7.2,'start','',c)
    if len(s)>120: tx(76+(i%2)*690,YK+48+(i//2)*44+12,s[120:],7.2,'start','',c)
tx(W-40,H-12,'AUTOKITCH · arastirma/3_TOPPING/ist3_topping_detay_v13 · 4 Eyl 2026',7,'end','',GRY)
o.append('</svg>')
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\ist3_topping_detay_v13.svg"
io.open(out,'w',encoding='utf-8').write(chr(10).join(o))
print('yazildi', out)
