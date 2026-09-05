# -*- coding: utf-8 -*-
# TOPPING DOZAJ v4 — EN DOGRU GEOMETRI (kama huni + canli taban + tarak) vs BIZIM 45° DILIM · ust / on / yan · uc gorunus karsilastirma
import io, math
W, H = 1460, 1010
o = []
def ln(x1,y1,x2,y2,w=1,c='#111',d=None):
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s stroke-linecap="round"/>' % (x1,y1,x2,y2,c,w,(' stroke-dasharray="%s"'%d) if d else ''))
def rc(x,y,w,h,sw=1,r=0,c='#111',d=None,f='none'):
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,w,h,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def ci(x,y,r,sw=1,c='#111',d=None,f='none'):
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def tx(x,y,s,fs=9,anc='start',fw='',col='#111'):
    o.append('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="%s" font-weight="%s" fill="%s" font-family="Segoe UI, Arial, sans-serif">%s</text>' % (x,y,fs,anc,fw or 'normal',col,s))
def path(d,sw=1,c='#111',f='none',dash=None):
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="%s"%s stroke-linejoin="round"/>' % (d,f,c,sw,(' stroke-dasharray="%s"'%dash) if dash else ''))
def poly(pts,sw=1,c='#111',f='none',d=None):
    o.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (' '.join('%.1f,%.1f'%p for p in pts),f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def arr(x1,y1,x2,y2,c='#c0392b',w=1.2):
    ln(x1,y1,x2,y2,w,c); a=math.atan2(y2-y1,x2-x1)
    for s in (1,-1): ln(x2,y2,x2-6*math.cos(a-s*.42),y2-6*math.sin(a-s*.42),w,c)
def carc(cx,cy,r,a1,a2,c='#1a49b8',sw=1.1):
    p=lambda a:(cx+r*math.cos(math.radians(a)),cy+r*math.sin(math.radians(a)))
    x1,y1=p(a1); x2,y2=p(a2)
    path('M%.1f,%.1f A%.1f,%.1f 0 %d 1 %.1f,%.1f'%(x1,y1,r,r,1 if abs(a2-a1)>180 else 0,x2,y2),sw,c)
    a=math.radians(a2+90)
    for s in (1,-1): ln(x2,y2,x2-6*math.cos(a-s*.42),y2-6*math.sin(a-s*.42),sw,c)
def sector(cx,cy,r0,r1,a1,a2,sw=1,c='#111',f='#f1efe8'):
    p = lambda r,a: (cx+r*math.cos(math.radians(a)), cy+r*math.sin(math.radians(a)))
    x1,y1=p(r1,a1); x2,y2=p(r1,a2); x3,y3=p(r0,a2); x4,y4=p(r0,a1)
    path('M%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f Z' % (x1,y1,r1,r1,x2,y2,x3,y3,r0,r0,x4,y4),sw,c,f)
def rotor_yan(x,zc,r,sw=1.3):      # eksene bakis: daire + 6 cep
    ci(x,zc,r,sw,'#111',None,'#fff')
    for k in range(6):
        a=math.radians(k*60+20); ln(x,zc,x+r*math.cos(a),zc+r*math.sin(a),.9,'#111')
    ci(x,zc,r*0.2,.9,'#111',None,'#ddd')
def tarak_yan(x,zc,K):             # eksene bakis: mil + 3 pim + suporme
    ci(x,zc,K*0.6,1.1,BLU,None,'#dfe7fb')
    ln(x,zc,x+K*5,zc,1.3,BLU); ln(x,zc,x-K*2.5,zc+K*4.3,1.3,BLU); ln(x,zc,x-K*2.5,zc-K*4.3,1.3,BLU)
    ci(x,zc,K*5.5,.9,BLU,'4,3')

GRN, RED, BLU, GRY, AMB = '#1d7a4f', '#c0392b', '#1a49b8', '#666', '#b7791f'
FILL, MAT = '#f1efe8', '#e9dfa8'
K = 5.5

o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H))
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,42,'AUTOKITCH — TOPPING · DOZAJ v4 (4 Eyl 2026) — EN DOĞRU GEOMETRİ (ders kitabı: kama huni + canlı taban + tarak) ile BİZİM 45° DİLİM yan yana · üst / ön / yan · ölçüler cm',15,'start','bold')
tx(30,66,'Ön ve yan görünüşler KESİT olarak çizildi (içi görünsün diye). Ön = rotor eksenine bakış (robot tarafı) · Yan = rotor eksenine dik. Her ikisinde de aynı ölçek 1:1,8.',9.5,'start','','#444')
ln(30,78,W-30,78,.8,'#999')

def kolon_basliklari(y):
    for x,s in ((210,'ÜST (plan)'),(570,'ÖN KESİT — rotor eksenine bakış'),(920,'YAN KESİT — rotor boyunca')):
        tx(x,y,s,8.5,'middle','bold',GRY)

# ======================= SATIR 1 · EN DOĞRU GEOMETRİ =======================
Y1 = 100
rc(40,Y1,1060,410,1.4,4,'#111',None,'#fcfdff')
tx(54,Y1+22,'1 · EN DOĞRU GEOMETRİ — kama (V) huni · rotor tüm boy (canlı taban) · üstünde tarak · dik uç duvarlar',10,'start','bold')
kolon_basliklari(Y1+42)
L, Wd, Hh = 20.0, 25.0, 28.0            # boy, en, yukseklik
# --- UST ---
ux,uy = 210-K*Wd/2, Y1+70
rc(ux,uy,K*Wd,K*L,1.4,0,'#111',None,FILL)
rc(ux+K*(Wd/2-3.5),uy,K*7,K*L,1.2,0,'#111',None,'#fff')
for k in range(1,10): ln(ux+K*(Wd/2-3.5),uy+K*k*2,ux+K*(Wd/2+3.5),uy+K*k*2,.7,'#999')
rc(ux+K*(Wd/2-5.5),uy,K*11,K*L,.9,2,BLU,'4,3')
ln(ux+K*Wd/2,uy,ux+K*Wd/2,uy+K*L,1.8,BLU)
for k in range(8):
    yy=uy+K*(1.3+k*2.5); s=1 if k%2==0 else -1; ln(ux+K*Wd/2,yy,ux+K*(Wd/2+s*5),yy,1.1,BLU)
for yy_ in (uy+K*5,uy+K*15):
    arr(ux+4,yy_,ux+K*(Wd/2-3.5)-3,yy_,AMB,1); arr(ux+K*Wd-4,yy_,ux+K*(Wd/2+3.5)+3,yy_,AMB,1)
tx(ux+K*Wd/2,uy+K*L+14,'%g' % Wd,7,'middle','bold'); ln(ux,uy+K*L+6,ux+K*Wd,uy+K*L+6,.8)
ln(ux-8,uy,ux-8,uy+K*L,.8); tx(ux-12,uy+K*L/2+3,'%g' % L,7,'end','bold')
tx(ux+K*Wd+6,uy+K*4,'rotor 7 × 20',6.5,'start','bold'); tx(ux+K*Wd+6,uy+K*7,'= boyun tamamı',6.3,'start','','#333')
tx(ux+K*Wd+6,uy+K*11,'tarak Ø11',6.5,'start','bold',BLU); tx(ux+K*Wd+6,uy+K*14,'45° V-oluk',6.5,'start','bold',AMB)
# --- ON KESIT ---
ox,oz = 570, Y1+70+K*Hh+K*2
X=lambda c: ox+K*c; Z=lambda c: oz-K*c
poly([(X(-12.5),Z(28)),(X(12.5),Z(28)),(X(12.5),Z(16)),(X(3.5),Z(7)),(X(3.5),Z(0)),(X(-3.5),Z(0)),(X(-3.5),Z(7)),(X(-12.5),Z(16))],1.4,'#111',FILL)
poly([(X(-12.2),Z(24)),(X(12.2),Z(24)),(X(12.2),Z(16)),(X(3.5),Z(7)),(X(-3.5),Z(7)),(X(-12.2),Z(16))],0,'none',MAT)
rotor_yan(X(0),Z(3.5),K*3.5); carc(X(0),Z(3.5),K*4.8,150,30,'#111',.9)
tarak_yan(X(0),Z(13),K)
rc(X(-14),Z(0),K*28,K*1,1,0,'#111',None,'#ddd'); rc(X(-3.5),Z(0),K*7,K*1,0,0,'none',None,'#fff')
rc(X(-16),Z(-2),K*32,K*2,1.2,0,'#111',None,'#bbb')
poly([(X(-4),Z(-4)),(X(4),Z(-4)),(X(1.2),Z(-12)),(X(-1.2),Z(-12))],1,GRN,'#eaf6ee','3,2'); arr(X(0),Z(-12),X(0),Z(-15),GRN,1.3)
tx(X(-12.5)+3,Z(12.8),'45°',6,'start','bold',AMB)
tx(X(14.5),Z(3),'rotor Ø7',6.5,'start','bold'); tx(X(14.5),Z(13),'tarak Ø11 · z 13',6.5,'start','bold',BLU)
tx(X(14.5),Z(21),'depo (dik duvar)',6.5,'start','','#333'); tx(X(14.5),Z(-1.6),'taban + tabla',6,'start','',GRY); tx(X(14.5),Z(-8),'huni → nokta',6,'start','',GRN)
ln(X(-12.5),Z(29.5),X(12.5),Z(29.5),.8); tx(X(0),Z(30.8),'25',7,'middle','bold')
ln(X(-15.5),Z(0),X(-15.5),Z(28),.8); tx(X(-16.5),Z(14),'28',7,'end','bold')
ln(X(-12.5)-2,Z(16),X(-12.5)-2,Z(7),.7,AMB); tx(X(-13.5),Z(11),'9',6,'end','bold',AMB)
# --- YAN KESIT ---
sx = 920-K*L/2; SZ=lambda c: oz-K*c; SX=lambda c: sx+K*c
poly([(SX(0),SZ(28)),(SX(L),SZ(28)),(SX(L),SZ(0)),(SX(0),SZ(0))],1.4,'#111',FILL)
poly([(SX(0.3),SZ(24)),(SX(L-0.3),SZ(24)),(SX(L-0.3),SZ(7.3)),(SX(0.3),SZ(7.3))],0,'none',MAT)
rc(SX(0),SZ(7),K*L,K*7,1.3,3,'#111',None,'#fff')
for k in range(1,10): ln(SX(k*2),SZ(7),SX(k*2),SZ(0),.7,'#999')
ln(SX(-0.5),SZ(3.5),SX(L+0.5),SZ(3.5),.8,'#555','3,2')
ln(SX(0),SZ(13),SX(L),SZ(13),1.8,BLU)
for k in range(8):
    r_=1.3+k*2.5; s=1 if k%2==0 else -1; ln(SX(r_),SZ(13),SX(r_),SZ(13+s*5),1.1,BLU)
rc(SX(0),SZ(18.5),K*L,K*11,.9,3,BLU,'4,3')
rc(SX(L-2.4),SZ(1.2)-K*1.2,K*2.4,K*2.4,1.1,1,BLU,None,'#dfe7fb'); arr(SX(L-1.2),SZ(-7),SX(L-1.2),SZ(-2.5),BLU,1.2); tx(SX(L-1.2),SZ(-8.5),'tahrik',6,'middle','bold',BLU)
rc(SX(-1),SZ(0),K*(L+2),K*1,1,0,'#111',None,'#ddd'); rc(SX(0),SZ(0),K*L,K*1,0,0,'none',None,'#fff')
rc(SX(-2),SZ(-2),K*(L+4),K*2,1.2,0,'#111',None,'#bbb')
poly([(SX(0),SZ(-4)),(SX(L),SZ(-4)),(SX(L/2+1.5),SZ(-12)),(SX(L/2-1.5),SZ(-12))],1,GRN,'#eaf6ee','3,2'); arr(SX(L/2),SZ(-12),SX(L/2),SZ(-15),GRN,1.3)
ln(SX(0),SZ(29.5),SX(L),SZ(29.5),.8); tx(SX(L/2),SZ(30.8),'20',7,'middle','bold')
tx(SX(L)+8,SZ(3),'rotor tüm boy',6.5,'start','bold'); tx(SX(L)+8,SZ(0.5),'= canlı taban',6.3,'start','','#333')
tx(SX(L)+8,SZ(13),'tarak tüm boy',6.5,'start','bold',BLU); tx(SX(L)+8,SZ(22),'uç duvar DİK',6.5,'start','bold'); tx(SX(L)+8,SZ(19.5),'(köşe ölü değil)',6.2,'start','','#333')
tx(SX(L)+8,SZ(-9),'huni hattı noktaya',6,'start','',GRN)
# ilkeler
ny = Y1+352
for i,s in enumerate(['İLKELER: ① kama (düzlem akış) huni — koniye göre 10° daha yatık duvar yeter · ② rotor tüm boyu tarar → tabanda durgun bölge yok (canlı taban) · ③ tarak V ağzında, rotora paralel',
                      '④ uç duvarlar dik olabilir (canlı taban köşeyi de boşaltır) · ⑤ çıkış 20 cm hat, altta sabit huni noktaya toplar · ⑥ hacim 25×20×28 = 14 L − V 3,1 L = ~10,9 L']):
    tx(54,ny+i*14,s,7.3,'start','bold' if i==0 else '','#333')

# ======================= SATIR 2 · BİZİM 45° DİLİM =======================
Y2 = 530
rc(40,Y2,1060,410,1.4,4,'#111',None,'#fcfbf8')
tx(54,Y2+22,'2 · BİZİMKİ — 45° revolver dilimi: aynı ilkeler üçgene uyarlanmış (kiriş 25,3 · radyal 28,4 · h 28 · rotor 16)',10,'start','bold')
kolon_basliklari(Y2+42)
# --- UST ---
cx,cy = 210, Y2+56          # sanal eksen; dilim asagi bakar
sector(cx,cy,K*5,K*33,67.5,112.5,1.4,'#111',FILL)
sector(cx,cy,K*5,K*13,67.5,112.5,.8,'#999','#f7f3ec')
rc(cx-K*5.5,cy+K*12,K*11,K*18,.9,2,BLU,'4,3')
rc(cx-K*3.5,cy+K*13,K*7,K*16,1.2,0,'#111',None,'#fff')
for k in range(1,8): ln(cx-K*3.5,cy+K*(13+k*2),cx+K*3.5,cy+K*(13+k*2),.7,'#999')
ln(cx,cy+K*11,cx,cy+K*31,1.8,BLU)
for k in range(8):
    yy=cy+K*(12.5+k*2.4); s=1 if k%2==0 else -1; ln(cx,yy,cx+s*K*5,yy,1.1,BLU)
for r_ in (17,26):
    ww=K*r_*math.sin(math.radians(22.5)); arr(cx-ww+4,cy+K*r_,cx-K*3.5-3,cy+K*r_,AMB,1); arr(cx+ww-4,cy+K*r_,cx+K*3.5+3,cy+K*r_,AMB,1)
ci(cx,cy+K*20,3.5,1.4,GRN,None,'#fff'); ci(cx,cy+K*20,1.3,1,GRN,None,GRN)
tx(cx,cy+K*9.5,'eğimli uç',5.4,'middle','',GRY)
ln(cx-K*12.6,cy+K*34.5,cx+K*12.6,cy+K*34.5,.8); tx(cx,cy+K*36.5,'25,3',7,'middle','bold')
ln(cx-K*15,cy+K*5,cx-K*15,cy+K*33,.8); tx(cx-K*15.6,cy+K*19,'28,4',7,'end','bold')
tx(cx+K*13.5,cy+K*15,'rotor 7 × 16',6.5,'start','bold'); tx(cx+K*13.5,cy+K*18,'r 13-29',6.3,'start','','#333')
tx(cx+K*13.5,cy+K*22,'tarak Ø11',6.5,'start','bold',BLU); tx(cx+K*13.5,cy+K*25,'çıkış r 20',6.5,'start','bold',GRN); tx(cx+K*13.5,cy+K*28,'45° V-oluk',6.5,'start','bold',AMB)
# --- ON KESIT (r 21, rotor eksenine bakis) ---
ox2,oz2 = 570, Y2+70+K*Hh+K*2
X2=lambda c: ox2+K*c; Z2=lambda c: oz2-K*c
hw=21*math.sin(math.radians(22.5))   # 8,0
poly([(X2(-hw),Z2(28)),(X2(hw),Z2(28)),(X2(hw),Z2(11.5)),(X2(3.5),Z2(7)),(X2(3.5),Z2(0)),(X2(-3.5),Z2(0)),(X2(-3.5),Z2(7)),(X2(-hw),Z2(11.5))],1.4,'#111',FILL)
# dis uc (r 29) siluet: daha genis V — kesikli
hw2=29*math.sin(math.radians(22.5))  # 11,1
poly([(X2(-hw2),Z2(28)),(X2(hw2),Z2(28)),(X2(hw2),Z2(14.6)),(X2(3.5),Z2(7)),(X2(-3.5),Z2(7)),(X2(-hw2),Z2(14.6))],.9,'#888','none','4,3')
poly([(X2(-hw+0.3),Z2(24)),(X2(hw-0.3),Z2(24)),(X2(hw-0.3),Z2(11.5)),(X2(3.5),Z2(7)),(X2(-3.5),Z2(7)),(X2(-hw+0.3),Z2(11.5))],0,'none',MAT)
rotor_yan(X2(0),Z2(3.5),K*3.5); carc(X2(0),Z2(3.5),K*4.8,150,30,'#111',.9)
tarak_yan(X2(0),Z2(13),K)
rc(X2(-14),Z2(0),K*28,K*1,1,0,'#111',None,'#ddd'); rc(X2(-3.5),Z2(0),K*7,K*1,0,0,'none',None,'#fff')
rc(X2(-16),Z2(-2),K*32,K*2,1.2,0,'#111',None,'#bbb')
poly([(X2(-4),Z2(-4)),(X2(4),Z2(-4)),(X2(1.2),Z2(-12)),(X2(-1.2),Z2(-12))],1,GRN,'#eaf6ee','3,2'); arr(X2(0),Z2(-12),X2(0),Z2(-15),GRN,1.3)
tx(X2(-hw)+3,Z2(9.4),'45°',6,'start','bold',AMB)
tx(X2(14.5),Z2(3),'rotor Ø7',6.5,'start','bold'); tx(X2(14.5),Z2(13),'tarak Ø11 · z 13',6.5,'start','bold',BLU)
tx(X2(14.5),Z2(22),'r 21 kesiti (düz)',6.5,'start','','#333'); tx(X2(14.5),Z2(19.5),'r 29 silueti (kesik)',6.3,'start','','#888')
tx(X2(14.5),Z2(-8),'huni → (35, 60)',6,'start','',GRN)
ln(X2(-hw),Z2(29.5),X2(hw),Z2(29.5),.8); tx(X2(0),Z2(30.8),'16 (r 21) · 22 (r 29)',7,'middle','bold')
ln(X2(-15.5),Z2(0),X2(-15.5),Z2(28),.8); tx(X2(-16.5),Z2(14),'28',7,'end','bold')
ln(X2(-hw)-2,Z2(11.5),X2(-hw)-2,Z2(7),.7,AMB); tx(X2(-hw)-3,Z2(9),'4,5',6,'end','bold',AMB)
# --- YAN KESIT (acıortay boyunca) ---
sx2 = 920-K*28.4/2; RX=lambda r: sx2+K*(r-5); RZ=lambda c: oz2-K*c
poly([(RX(5),RZ(28)),(RX(33),RZ(28)),(RX(33),RZ(11)),(RX(29),RZ(7)),(RX(29),RZ(0)),(RX(13),RZ(0)),(RX(13),RZ(7)),(RX(5),RZ(15))],1.4,'#111',FILL)
poly([(RX(5.3),RZ(24)),(RX(32.7),RZ(24)),(RX(32.7),RZ(11)),(RX(29),RZ(7.3)),(RX(13),RZ(7.3)),(RX(5.3),RZ(15))],0,'none',MAT)
rc(RX(13),RZ(7),K*16,K*7,1.3,3,'#111',None,'#fff')
for k in range(1,8): ln(RX(13+k*2),RZ(7),RX(13+k*2),RZ(0),.7,'#999')
ln(RX(12),RZ(3.5),RX(30),RZ(3.5),.8,'#555','3,2')
ln(RX(11),RZ(13),RX(31),RZ(13),1.8,BLU)
for k in range(8):
    r_=12.5+k*2.4; s=1 if k%2==0 else -1; ln(RX(r_),RZ(13),RX(r_),RZ(13+s*5),1.1,BLU)
rc(RX(11),RZ(18.5),K*20,K*11,.9,3,BLU,'4,3')
ci(RX(11.5),RZ(3.5),K*1.2,1,'#555',None,'#eee'); ci(RX(11.5),RZ(13),K*2.2,1,'#555',None,'#eee'); ln(RX(11.5),RZ(3.5),RX(11.5),RZ(13),1,'#555'); tx(RX(10.6),RZ(8.5),'1:20',5.6,'end','bold','#555')
rc(RX(29),RZ(1.2)-K*1.2,K*2.4,K*2.4,1.1,1,BLU,None,'#dfe7fb'); arr(RX(30.2),RZ(-7),RX(30.2),RZ(-2.5),BLU,1.2); tx(RX(30.2),RZ(-8.5),'tahrik',6,'middle','bold',BLU)
rc(RX(4),RZ(0),K*30,K*1,1,0,'#111',None,'#ddd'); rc(RX(13),RZ(0),K*16,K*1,0,0,'none',None,'#fff')
rc(RX(3),RZ(-2),K*32,K*2,1.2,0,'#111',None,'#bbb')
poly([(RX(12),RZ(-4)),(RX(30),RZ(-4)),(RX(21.5),RZ(-12)),(RX(18.5),RZ(-12))],1,GRN,'#eaf6ee','3,2'); arr(RX(20),RZ(-12),RX(20),RZ(-15),GRN,1.3)
ln(RX(5),RZ(29.5),RX(33),RZ(29.5),.8); tx(RX(19),RZ(30.8),'28,4',7,'middle','bold')
tx(RX(7.5),RZ(18),'eğimli uç',5.4,'middle','',GRY); tx(RX(31),RZ(9.5),'45°',5.4,'middle','bold',AMB)
tx(RX(33)+8,RZ(3),'rotor 16 / 28',6.5,'start','bold'); tx(RX(33)+8,RZ(0.5),'(boyun %57'+chr(39)+'si)',6.3,'start','','#333')
tx(RX(33)+8,RZ(13),'tarak 20 / 28',6.5,'start','bold',BLU); tx(RX(33)+8,RZ(22),'iç uç 45° eğim',6.5,'start','bold',AMB); tx(RX(33)+8,RZ(19.5),'(canlı değil)',6.2,'start','','#333')
tx(RX(33)+8,RZ(-9),'huni → (35, 60)',6,'start','',GRN)
ny = Y2+352
for i,s in enumerate(['FARKLAR: ① genişlik iç uca doğru daralır → V derinliği 4,5 (r 21) → 7,5 (r 29), sabit değil · ② rotor boyun %57'+chr(39)+'si; iç uç r 5-13 canlı değil → 45° eğimle rotora akar (depo sayılmaz)',
                      '③ dış duvar dibi 45° → rotor dış ucuna · ④ tahrik dış uçtan konik + kavrama (ders kitabında yan) · ⑤ hacim 11,7 − V/uç 1,7 = ~10 L (ideal 10,9) — %8 fark']):
    tx(54,ny+i*14,s,7.3,'start','bold' if i==0 else '','#333')

# ======================= SAĞ SÜTUN · KARŞILAŞTIRMA =======================
XK = 1120
rc(XK,Y1,310,850,1.4,4)
tx(XK+14,Y1+22,'KARŞILAŞTIRMA',10,'start','bold')
rows = [
 ('kama huni (düzlem akış)','✓','✓',GRN),
 ('canlı taban (rotor tüm boy)','✓','~ %57',AMB),
 ('tarak V ağzında, paralel','✓','✓',GRN),
 ('ölü köşe yok','✓','✓ (uç eğimli)',GRN),
 ('V derinliği sabit','✓','✗ 4,5-7,5',AMB),
 ('duvar eğimi 45°','✓','✓',GRN),
 ('hacim (L)','10,9','~10',GRN),
 ('tahrik yeri','yan','dış uç',GRY),
 ('dilim pasif','✓','✓',GRN),
 ('tek dozaj noktası','—','✓ (35, 60)',GRN),
]
tx(XK+14,Y1+46,'ölçüt',7,'start','bold',GRY); tx(XK+178,Y1+46,'ideal',7,'middle','bold',GRY); tx(XK+255,Y1+46,'bizim',7,'middle','bold',GRY)
ln(XK+12,Y1+52,XK+298,Y1+52,.8,'#bbb')
for i,(a,b,c,col) in enumerate(rows):
    yy=Y1+70+i*22
    tx(XK+14,yy,a,7.2,'start',''); tx(XK+178,yy,b,7.4,'middle','bold',GRN if b=='✓' else '#333'); tx(XK+255,yy,c,7.2,'middle','bold',col)
ln(XK+12,Y1+296,XK+298,Y1+296,.8,'#bbb')
notes = [
 ('SONUÇ', 'bold', '#111'),
 ('Bizimki ders kitabı geometrisinin', '', '#333'),
 ('üçgene uyarlanmış hali: ilkelerin', '', '#333'),
 ('tamamı korunuyor, iki sapma var:', '', '#333'),
 ('', '', '#333'),
 ('① iç uç canlı değil → 45° eğim +', '', AMB),
 ('   tarak o bölgeyi de tarıyor (r 11)', '', AMB),
 ('② V derinliği değişken → dış uçta', '', AMB),
 ('   7,5; hacim kaybı %8, kabul', '', AMB),
 ('', '', '#333'),
 ('İdeal daha basit ama revolvere', '', '#333'),
 ('dikdörtgen kutu sığmaz (8 × 25 × 20', '', '#333'),
 ('yan yana = 200 cm çevre, Ø66 tabla', '', '#333'),
 ('207 çevre → köşeler boş kalır,', '', '#333'),
 ('hacim %35 düşer). Sektör doğru.', 'bold', GRN),
 ('', '', '#333'),
 ('Prototipte denenecek: kaşarın 45°', '', GRY),
 ('V'+chr(39)+'de tarakla akışı; gerekirse V 50°.', '', GRY),
]
for i,(s,fw,c) in enumerate(notes):
    tx(XK+14,Y1+316+i*15.5,s,7.6 if fw else 7.2,'start',fw,c)
tx(XK+14,Y1+840-10,'TOPPING v12'+chr(39)+'ye bu dilim giriyor.',7.4,'start','bold',BLU)
tx(W-40,H-24,'AUTOKITCH · arastirma/3_TOPPING/topping_dozaj_unitesi_v4 · 4 Eyl 2026',7,'end','',GRY)
o.append('</svg>')
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\topping_dozaj_unitesi_v4.svg"
io.open(out,'w',encoding='utf-8').write(chr(10).join(o))
print('yazildi', out)
