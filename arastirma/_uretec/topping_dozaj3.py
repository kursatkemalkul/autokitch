# -*- coding: utf-8 -*-
# TOPPING DOZAJ v3 — kopru kirici SEKTOR (ucgen) dilimde nasil calisir: yatay TARAK mili (Picnic'in dikey teli degil) · plan + 2 kesit + malzeme tablosu
import io, math
W, H = 1460, 1130
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
    for s in (1,-1): ln(x2,y2,x2-7*math.cos(a-s*.42),y2-7*math.sin(a-s*.42),w,c)
def carc(cx,cy,r,a1,a2,c='#1a49b8',sw=1.2):
    p=lambda a:(cx+r*math.cos(math.radians(a)),cy+r*math.sin(math.radians(a)))
    x1,y1=p(a1); x2,y2=p(a2)
    path('M%.1f,%.1f A%.1f,%.1f 0 %d 1 %.1f,%.1f'%(x1,y1,r,r,1 if abs(a2-a1)>180 else 0,x2,y2),sw,c)
    a=math.radians(a2+90)
    for s in (1,-1): ln(x2,y2,x2-7*math.cos(a-s*.42),y2-7*math.sin(a-s*.42),sw,c)
def sector(cx,cy,r0,r1,a1,a2,sw=1,c='#111',f='#f1efe8'):
    p = lambda r,a: (cx+r*math.cos(math.radians(a)), cy+r*math.sin(math.radians(a)))
    x1,y1=p(r1,a1); x2,y2=p(r1,a2); x3,y3=p(r0,a2); x4,y4=p(r0,a1)
    path('M%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f Z' % (x1,y1,r1,r1,x2,y2,x3,y3,r0,r0,x4,y4),sw,c,f)
def hatch(x,y,w,h,step=6,c='#c9b8a8'):
    k=0
    while k < w+h:
        x1=x+max(0,k-h); y1=y+min(k,h); x2=x+min(k,w); y2=y+max(0,k-w)
        ln(x1,y1,x2,y2,.6,c); k+=step

GRN, RED, BLU, GRY, AMB = '#1d7a4f', '#c0392b', '#1a49b8', '#666', '#b7791f'
FILL, MAT = '#f1efe8', '#e9dfa8'

o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H))
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,42,'AUTOKITCH — TOPPING · DOZAJ v3 (4 Eyl 2026) — KÖPRÜ KIRICI: şart mı, hangi malzemede, ÜÇGEN (sektör) dilimde nasıl çalışır? · ölçüler cm',15,'start','bold')
tx(30,66,'Cevap: Picnic'+chr(39)+'in dikey dönen teli daire süpürür — üçgende köşeler ölü kalır. Sektörde doğrusu: rotora PARALEL yatay TARAK mili (radyal), aynı milden 1:20, dilim yine pasif. Tarak sayesinde taban 45° yeter → hacim korunur.',9.5,'start','','#444')
ln(30,78,W-30,78,.8,'#999')

# ================= 1 · PLAN (sektör) =================
K = 6.0
XP,YP = 40,100
rc(XP,YP,420,560,1.4,4)
tx(XP+14,YP+22,'1 · PLAN — 45° dilim, üstten (1:1,67)',9.5,'start','bold')
cx,cy = XP+210, YP+40         # sanal eksen (tablanin merkezi) — dilim asagi bakar
p = lambda r,a: (cx+K*r*math.cos(math.radians(a)), cy+K*r*math.sin(math.radians(a)))
sector(cx,cy,K*5,K*33,67.5,112.5,1.4,'#111',FILL)
# olu uc (r 5-13): egimli taban, depo degil
sector(cx,cy,K*5,K*13,67.5,112.5,.8,'#999','#f7f3ec')
tx(cx,cy+K*10,'eğimli uç',5.6,'middle','',GRY); tx(cx,cy+K*12,'(depo değil)',5.2,'middle','',GRY)
# tarak suporme bandi (O11, r 12-30)
rc(cx-K*5.5,cy+K*12,K*11,K*18,1,3,BLU,'4,3','#eef3ff')
# rotor yuvasi (slot 7 genis, r 13-29)
rc(cx-K*3.5,cy+K*13,K*7,K*16,1.3,2,'#111',None,'#fff')
for k in range(8): ln(cx-K*3.5,cy+K*(13+k*2)+K,cx+K*3.5,cy+K*(13+k*2)+K,.8,'#111')
tx(cx,cy+K*21,'ROTOR',6.2,'middle','bold'); tx(cx,cy+K*23.2,'6 cep · 16 uzun',5.4,'middle','')
# tarak mili + pimler
ln(cx,cy+K*11,cx,cy+K*31,2,BLU)
for k in range(9):
    yy=cy+K*(12.5+k*2.2); s = 1 if k%2==0 else -1
    ln(cx,yy,cx+s*K*5,yy,1.2,BLU)
tx(cx+K*6.5,cy+K*15,'TARAK MİLİ',6.5,'start','bold',BLU); tx(cx+K*6.5,cy+K*17,'pim 5 · süpürme Ø11',5.6,'start','',BLU)
tx(cx+K*6.5,cy+K*19,'3 dev/dk (1:20)',5.6,'start','',BLU)
# disli (ic ucta)
ci(cx,cy+K*11.5,K*1.4,1,'#555',None,'#eee'); ci(cx,cy+K*13.2,K*0.9,1,'#555',None,'#eee'); tx(cx-K*2,cy+K*11.5,'dişli',5.2,'end','','#555')
# V oluk egimi oklari (tanjant yon)
for r_ in (17,25):
    ww=K*r_*math.sin(math.radians(22.5))
    arr(cx-ww+4,cy+K*r_,cx-K*3.5-3,cy+K*r_,AMB,1); arr(cx+ww-4,cy+K*r_,cx+K*3.5+3,cy+K*r_,AMB,1)
tx(cx-K*13,cy+K*25.5,'45° V-oluk',5.8,'end','bold',AMB)
# dozaj noktasi r 20 (cikis) — altta sabit huni
ci(cx,cy+K*20,4.5,1.6,GRN,None,'#fff'); ci(cx,cy+K*20,1.8,1,GRN,None,GRN)
tx(cx-K*4.5,cy+K*20+3,'çıkış r 20',6,'end','bold',GRN)
# olculer
ln(cx-K*12.6,cy+K*34.5,cx+K*12.6,cy+K*34.5,.8); tx(cx,cy+K*36.5,'dış kiriş 25,3',6.5,'middle','bold')
ln(cx+K*14,cy+K*5,cx+K*14,cy+K*33,.8); tx(cx+K*14.6,cy+K*19,'28,4',6.5,'start','bold')
ln(cx+K*15.5,cy+K*13,cx+K*15.5,cy+K*29,.8,BLU); tx(cx+K*16.1,cy+K*21.5,'16',6,'start','bold',BLU)
tx(cx-K*13,cy+K*7,'A',8,'middle','bold',RED); tx(cx+K*13,cy+K*7,'A',8,'middle','bold',RED)
ln(cx-K*12,cy+K*21,cx+K*12,cy+K*21,.8,RED,'6,3'); tx(cx-K*13,cy+K*21+3,'A',8,'end','bold',RED); tx(cx+K*13,cy+K*21+3,'A',8,'start','bold',RED)
ln(cx-K*9,cy+K*4,cx-K*9,cy+K*34,.8,RED,'6,3'); tx(cx-K*9,cy+K*3,'B',8,'middle','bold',RED); tx(cx-K*9,cy+K*36.5,'B',8,'middle','bold',RED)
tx(XP+14,YP+520,'B-B kesiti dilim ortasından (açıklık için yana çizildi)',6.5,'start','',GRY)
tx(XP+14,YP+536,'üçgende daire süpüren dikey tel yerine radyal mil: dar iç uçtan geniş dış',6.5,'start','','#333')
tx(XP+14,YP+548,'kenara kadar aynı Ø11 silindiri süpürür — köşe kalmaz.',6.5,'start','','#333')

# ================= 2 · KESİT A-A (tanjant, r 21) =================
K2 = 7.0
XA,YA = 480,100
rc(XA,YA,440,560,1.4,4)
tx(XA+14,YA+22,'2 · KESİT A-A — r 21'+chr(39)+'de, oluğa dik (1:1,43)',9.5,'start','bold')
hw = 21*math.sin(math.radians(22.5))          # 8,0 yari genislik
ox_,oz_ = XA+220, YA+330                       # dilim taban plakasi ust yuzu (z=0)
X = lambda c: ox_+K2*c
Z = lambda c: oz_-K2*c
# dilim duvarlari (dik, z 11.5-28) + V (45°) + rotor yuvasi
poly([(X(-hw),Z(28)),(X(hw),Z(28)),(X(hw),Z(11.5)),(X(3.5),Z(7)),(X(3.5),Z(0)),(X(-3.5),Z(0)),(X(-3.5),Z(7)),(X(-hw),Z(11.5))],1.4,'#111',FILL)
# malzeme
poly([(X(-hw+0.3),Z(24)),(X(hw-0.3),Z(24)),(X(hw-0.3),Z(11.5)),(X(3.5),Z(7)),(X(-3.5),Z(7)),(X(-hw+0.3),Z(11.5))],0,'none',MAT)
# rotor
ci(X(0),Z(3.5),K2*3.5,1.4,'#111',None,'#fff')
for k in range(6):
    a=math.radians(k*60+20); ln(X(0),Z(3.5),X(0)+K2*3.5*math.cos(a),Z(3.5)+K2*3.5*math.sin(a),1,'#111')
ci(X(0),Z(3.5),K2*0.7,1,'#111',None,'#ddd')
carc(X(0),Z(3.5),K2*5,150,30,'#111',1)
tx(X(6),Z(2),'rotor Ø7 · 60 dev/dk',6.5,'start','bold')
# tarak mili + pimler + suporme
ci(X(0),Z(13),K2*0.6,1.2,BLU,None,'#dfe7fb')
ln(X(0),Z(13),X(5),Z(13),1.4,BLU); ln(X(0),Z(13),X(-2.5),Z(13+4.3),1.4,BLU); ln(X(0),Z(13),X(-2.5),Z(13-4.3),1.4,BLU)
ci(X(0),Z(13),K2*5,1,BLU,'4,3')
carc(X(0),Z(13),K2*6.2,200,20,BLU,1)
tx(X(7),Z(15),'tarak Ø11 · 3 dev/dk',6.5,'start','bold',BLU)
tx(X(7),Z(12.5),'pimler helis dizili, V ağzını tarar',6,'start','',BLU)
# egim etiketi
tx(X(-hw)+4,Z(9.6),'45°',6,'start','bold',AMB)
# taban plakasi + acik yuva + tabla + sabit huni
rc(X(-hw)-4,Z(0),K2*(2*hw)+8,K2*1,1,0,'#111',None,'#ddd'); tx(X(hw)+8,Z(-0.6),'dilim tabanı',6,'start','',GRY)
rc(X(-3.5),Z(0),K2*7,K2*1,0,0,'none',None,'#fff')
rc(X(-hw)-14,Z(-2),K2*(2*hw)+28,K2*2,1.2,0,'#111',None,'#bbb'); tx(X(hw)+8,Z(-2.6),'tabla 2 (açıklığı var)',6,'start','',GRY)
poly([(X(-4),Z(-4)),(X(4),Z(-4)),(X(1.5),Z(-19)),(X(-1.5),Z(-19))],1,GRN,'#eaf6ee','3,2')
arr(X(0),Z(-19),X(0),Z(-23),GRN,1.4); tx(X(3),Z(-22),'ÇIKIŞ (35, 60)',7,'start','bold',GRN)
tx(X(3),Z(-9),'sabit huni (çark katı 21)',6,'start','',GRN)
# olculer
ln(X(hw)+34,Z(0),X(hw)+34,Z(28),.8); tx(X(hw)+38,Z(14),'28',7,'start','bold')
ln(X(-hw),Z(29.5),X(hw),Z(29.5),.8); tx(X(0),Z(30.8),'16 (r 21'+chr(39)+'de genişlik)',6.5,'middle','bold')
ln(X(-3.5),Z(-0.8)-0,X(3.5),Z(-0.8),.8,'#111'); tx(X(0),Z(-1.5)-6,'7',6,'middle','bold')
tx(XA+14,YA+520,'V-oluk derinliği yarı-genişlik × tan45° = 4,5 (r 21) · 7,5 (r 29)',6.5,'start','','#333')
tx(XA+14,YA+534,'tarak olmasaydı kaşar için 60°+ duvar gerekirdi → V 14 derin, hacim yarıya iner',6.5,'start','bold',AMB)
tx(XA+14,YA+548,'rotor cepleri yukarı açık: tarak V ağzından cebe besler, cep altta boşalır',6.5,'start','','#333')

# ================= 3 · KESİT B-B (radyal) =================
K3 = 5.6
XB,YB = 940,100
rc(XB,YB,490,560,1.4,4)
tx(XB+14,YB+22,'3 · KESİT B-B — açıortay boyunca, iç uçtan dış duvara (1:1,79)',9.5,'start','bold')
bx_,bz_ = XB+50, YB+330
RX = lambda r: bx_+K3*(r-5)
RZ = lambda c: bz_-K3*c
# govde: ic uc (r5) egimli taban z 15→7 (r 13), rotor bolgesi r 13-29 z 0-7, dis uc r 29-33 egim z 7→11, duvar r33 dik
poly([(RX(5),RZ(28)),(RX(33),RZ(28)),(RX(33),RZ(11)),(RX(29),RZ(7)),(RX(29),RZ(0)),(RX(13),RZ(0)),(RX(13),RZ(7)),(RX(5),RZ(15))],1.4,'#111',FILL)
poly([(RX(5.3),RZ(24)),(RX(32.7),RZ(24)),(RX(32.7),RZ(11)),(RX(29),RZ(7.3)),(RX(13),RZ(7.3)),(RX(5.3),RZ(15))],0,'none',MAT)
# rotor (yan gorunus: silindir)
rc(RX(13),RZ(7),K3*16,K3*7,1.3,3,'#111',None,'#fff')
for k in range(1,8): ln(RX(13+k*2),RZ(7),RX(13+k*2),RZ(0),.7,'#999')
ln(RX(12),RZ(3.5),RX(30),RZ(3.5),.8,'#555','3,2')
tx(RX(21),RZ(3.2),'rotor 16 · Ø7',6.5,'middle','bold')
# tarak mili r 11-31, z 13, pimler helis
ln(RX(11),RZ(13),RX(31),RZ(13),2,BLU)
for k in range(9):
    r_=12.5+k*2.2; s = 1 if k%2==0 else -1
    ln(RX(r_),RZ(13),RX(r_),RZ(13+s*5),1.2,BLU)
rc(RX(11),RZ(18.5),K3*20,K3*11,1,3,BLU,'4,3')
tx(RX(21),RZ(20),'tarak mili · pim 5 · süpürme Ø11',6.5,'middle','bold',BLU)
# disli cifti ic ucta (rotor mili → tarak mili, 1:20 iki kademe)
ci(RX(11.5),RZ(3.5),K3*1.2,1,'#555',None,'#eee'); ci(RX(11.5),RZ(13),K3*2.2,1,'#555',None,'#eee'); ln(RX(11.5),RZ(3.5),RX(11.5),RZ(13),1,'#555')
tx(RX(10.8),RZ(8.5),'1:20',5.6,'end','bold','#555'); tx(RX(10.8),RZ(6.5),'dişli',5.4,'end','','#555')
# tahrik: dis ucta konik disli + kavrama (tabla altindan)
rc(RX(29),RZ(1.2),K3*2.4,K3*2.4,1.1,1,BLU,None,'#dfe7fb'); tx(RX(30.2),RZ(-1.4),'konik + kavrama',5.6,'middle','',BLU)
arr(RX(30.2),RZ(-8),RX(30.2),RZ(-3),BLU,1.3); tx(RX(30.2),RZ(-9.5),'sabit motor (tabla)',5.8,'middle','bold',BLU)
# taban, tabla, sabit huni → cikis r 20
rc(RX(4),RZ(0),K3*30,K3*1,1,0,'#111',None,'#ddd'); rc(RX(13),RZ(0),K3*16,K3*1,0,0,'none',None,'#fff')
rc(RX(3),RZ(-2),K3*32,K3*2,1.2,0,'#111',None,'#bbb'); tx(RX(3),RZ(-3.2),'tabla 2',5.8,'start','',GRY)
poly([(RX(12),RZ(-4)),(RX(30),RZ(-4)),(RX(21.5),RZ(-19)),(RX(18.5),RZ(-19))],1,GRN,'#eaf6ee','3,2')
arr(RX(20),RZ(-19),RX(20),RZ(-23),GRN,1.4); tx(RX(22),RZ(-22),'ÇIKIŞ r 20 = (35, 60)',7,'start','bold',GRN)
tx(RX(22),RZ(-12),'sabit huni — 16 cm hattı noktaya toplar',6,'start','',GRN)
# olculer
ln(RX(5),RZ(29.5),RX(33),RZ(29.5),.8); tx(RX(19),RZ(30.8),'28,4 (iç uç r 5 → dış duvar r 33)',6.5,'middle','bold')
ln(RX(34.5),RZ(0),RX(34.5),RZ(28),.8); tx(RX(35.2),RZ(14),'28',7,'start','bold')
tx(RX(7),RZ(17.5),'eğimli uç',5.6,'middle','',GRY)
tx(XB+14,YB+520,'iç uç: r 5-13 arası 45° eğimle rotora akar, depo sayılmaz (hacim payı düşüldü)',6.5,'start','','#333')
tx(XB+14,YB+534,'dış duvar dibi 45° eğim → rotor dış ucuna · her iki mil dilimin içinde, dilim PASİF',6.5,'start','','#333')
tx(XB+14,YB+548,'tahrik dış uçtan: tabladaki sabit motor → konik dişli → rotor → 1:20 → tarak',6.5,'start','bold',BLU)

# ================= 4 · MALZEME TABLOSU =================
XT,YT = 40,680
rc(XT,YT,880,240,1.4,4)
tx(XT+14,YT+22,'4 · ŞART MI? — malzemeye göre köprüleme',9.5,'start','bold')
hdr=['malzeme','köprüler mi','neden','tarak']
cx_=[XT+14, XT+180, XT+330, XT+760]
for i,h in enumerate(hdr): tx(cx_[i],YT+44,h,7.2,'start','bold',GRY)
ln(XT+12,YT+50,XT+868,YT+50,.8,'#bbb')
rows=[('rendelenmiş kaşar','EVET, ağır','lifli + yağlı; +3 °C'+chr(39)+'de keçeleşir, hunide kemer kurar','ŞART',RED),
      ('kavurma','EVET','yapışkan lif + yağ, topaklanır','ŞART',RED),
      ('kuşbaşı 1,5-2 cm küp','orta','küp serbest akar ama dar çıkışta kilitlenir: çıkış ≥ 6-8 × parça = 12-16, bizde 7','ŞART (hafif)',AMB),
      ('sucuk','—','çubuk + bıçak, huni yok','gerekmez',GRY),
      ('mısır / zeytin (ileride)','hafif','nemli, yuvarlak; yalnız uzun beklemede yapışır','yeter',GRN),
      ('un / toz (genel)','EVET','kohezif toz — endüstri standardı: tarak + vidalı besleyici','ŞART',RED)]
for i,(a,b,c,d,col) in enumerate(rows):
    yy=YT+68+i*19
    tx(cx_[0],yy,a,7.4,'start','bold'); tx(cx_[1],yy,b,7.2,'start','bold',col); tx(cx_[2],yy,c,7,'start','','#333'); tx(cx_[3],yy,d,7.2,'start','bold',col)
ln(XT+12,YT+188,XT+868,YT+188,.8,'#bbb')
tx(XT+14,YT+206,'Endüstride: Grote / Quantum peynir serpiciler, hacimsel toz besleyiciler (Coperion K-Tron), kahve çekirdek hazneleri, kuruyemiş-mama dolum, Picnic-Middleby pizza hatları.',7.2,'start','','#333')
tx(XT+14,YT+222,'Sonuç: dört malzemenin üçünde şart → her dilimde STANDART (tek dilim tipi bozulmaz); sucuk diliminde huni yok, tarak yok.',7.4,'start','bold',GRN)

# ================= 5 · KARAR =================
XK,YK = 940,680
rc(XK,YK,490,240,1.4,4)
tx(XK+14,YK+22,'5 · KARAR',9.5,'start','bold')
rows=[('Şart mı? Bizim malzemede evet. Tarak yalnız akışı sürdürmüyor, hacmi de kurtarıyor: onunla 45° taban yeter, onsuz kaşar 60°+ ister.','#333'),
      ('Üçgende nasıl? Dikey tel değil, rotora paralel yatay TARAK mili. Radyal mil dar iç uçtan geniş dış kenara aynı Ø11 silindiri süpürür; ölü köşe kalmaz. Aynı milden 1:20, dilim pasif.',BLU),
      ('Hacim: V-oluk + eğimli uç ~1,7 L götürür → kaşar ~4 kg / dilim → haftalık 12 (+1) = 13: tabla 4 + raf 9 → 12 yuva: 9 kaşar + 3 boş, sığar. Dilim 30 yapılırsa 11 (+1).',GRN),
      ('TOPPING v12'+chr(39)+'ye: dilim = V-oluk + radyal rotor 16 + tarak mili, dış uçta konik kavrama; tablada r 20 sabit huni + yük hücresi.',GRY)]
for i,(s,c) in enumerate(rows):
    tx(XK+14,YK+46+i*50,s[:88],7.6,'start','bold' if i==1 else '',c)
    if len(s)>88: tx(XK+14,YK+46+i*50+12,s[88:176],7.6,'start','',c)
    if len(s)>176: tx(XK+14,YK+46+i*50+24,s[176:],7.6,'start','',c)
tx(W-40,H-30,'AUTOKITCH · arastirma/3_TOPPING/topping_dozaj_unitesi_v3 · 4 Eyl 2026',7,'end','',GRY)
o.append('</svg>')
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\topping_dozaj_unitesi_v3.svg"
io.open(out,'w',encoding='utf-8').write(chr(10).join(o))
print('yazildi', out)
