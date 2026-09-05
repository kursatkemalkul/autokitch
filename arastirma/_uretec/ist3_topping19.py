# -*- coding: utf-8 -*-
# TOPPING v19 — KAPLAR ÖNE DÖNDÜ: helezon derinlik (y) yönünde, V-kesit ÖN yüz, motor ARKADA (taktığı gibi kavrar, eksenel pençe)
# kat 1: sol KAŞAR tam derinlik (haftalık) + sağ SUCUK · kat 2: sol KAVURMA + sağ KUŞBAŞI · alt: yedekler (buzluk gerekmeyenler) · STORE −18: kav/kuş
import io, math, xml.dom.minidom
W, H = 1460, 1180
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
def poly(pts,sw=1,c='#111',f='none',d=None):
    o.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (' '.join('%.1f,%.1f'%p for p in pts),f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def arr(x1,y1,x2,y2,c='#c0392b',w=1.2):
    ln(x1,y1,x2,y2,w,c); a=math.atan2(y2-y1,x2-x1)
    for s in (1,-1): ln(x2,y2,x2-6*math.cos(a-s*.42),y2-6*math.sin(a-s*.42),w,c)
def dim_h(x1,x2,y,s,fs=6): ln(x1,y,x2,y,.7); ln(x1,y-3,x1,y+3,.7); ln(x2,y-3,x2,y+3,.7); tx((x1+x2)/2,y-3,s,fs,'middle','bold')
def dim_v(x,y1,y2,s,fs=6): ln(x,y1,x,y2,.7); ln(x-3,y1,x+3,y1,.7); ln(x-3,y2,x+3,y2,.7); tx(x+4,(y1+y2)/2+2,s,fs,'start','bold')

GRN, RED, BLU, GRY, AMB, PUR = '#1d7a4f', '#c0392b', '#1a49b8', '#666', '#b7791f', '#6b4fa8'
FILL, MAT, SUC, LIGHT = '#f1efe8', '#e9dfa8', '#e8eef8', '#f7f6f2'
# kap kesiti: asimetrik kama — dış duvar 45°, iç duvar dik, oluk iç kenarda (ağız bant kenarında x 31 / 39)
WK = 32.5      # kap eni (x)
SLOPE = 25.5   # 45° eğim yatay = düşey (dış duvar x 2 → oluk kenarı x 27,5)
def kesit_alan(Hh): return WK*Hh - SLOPE*SLOPE/2          # cm²
LB,HB = 70,55; LS,HS = 20,28
vB = kesit_alan(HB)*LB/1000; vS = kesit_alan(HS)*LS/1000
Z = [('teknik',27,'#f3f3f3'),('KAT 1',58,'#fff'),('BOŞLUK 1',14,'#eef3ff'),('KAT 2',31,'#fff'),('BOŞLUK 2',14,'#eef3ff'),('ALT',53,'#f7f6f2')]
assert sum(z[1] for z in Z)==197

o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H))
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,42,'AUTOKITCH — TOPPING v19 (5 Eyl 2026) — KAPLAR ÖNE DÖNDÜ: helezon derinlik yönünde, V-kesit ÖN yüz, MOTOR ARKADA (taktığı gibi kavrar) · kat 1 kaşar + sucuk · kat 2 kavurma + kuşbaşı · alt yedekler',15,'start','bold')
tx(30,66,'Kemal: "yan dediğin ön olsun, motor dolabın arkasında olsun, üst sol full kaşar, yanında sucuk; alt sol kavurma sağ kuşbaşı; altta yedekler, donması gerekenler buzlukta." → Kap 90° döndü: oluk ve helezon arkadan öne uzanır, ağız kabın ÖN ucunda (bant x 31 / 39), dişli kavrama ARKA uçta.',9.5,'start','','#444')
ln(30,78,W-30,78,.8,'#999')

# ================= BÜYÜK KAP (KAŞAR) =================
XB,YB = 40,100
rc(XB,YB,520,540,1.4,4,'#111',None,'#fcfdff')
tx(XB+14,YB+22,'BÜYÜK KAP — KAŞAR · 32,5 × 70 × 55 · tam derinlik · %.0f L → %.0f kg = 6,9 gün (HAFTALIK, yedek gerekmez)' % (vB, vB*0.41),9.5,'start','bold')
K=2.6
# ON (V kesiti, asimetrik) — sol kap: dis duvar solda 45°, ic duvar sagda dik, oluk sagda
fx,fy = XB+30, YB+50
Zf=lambda c: fy+K*(HB-c)
Xf=lambda c: fx+K*c
poly([(Xf(0),Zf(HB)),(Xf(WK),Zf(HB)),(Xf(WK),Zf(0)),(Xf(WK-7),Zf(0)),(Xf(0),Zf(SLOPE))],1.3,'#111',FILL)
poly([(Xf(.3),Zf(HB-4)),(Xf(WK-.3),Zf(HB-4)),(Xf(WK-.3),Zf(.3)),(Xf(WK-7),Zf(.3)),(Xf(.3),Zf(SLOPE))],0,'none',MAT)
ci(Xf(WK-3.5),Zf(3.5),K*3.5,1.1,'#111',None,'#fff')
for k in range(6):
    a=math.radians(k*60+20); ln(Xf(WK-3.5),Zf(3.5),Xf(WK-3.5)+K*3.5*math.cos(a),Zf(3.5)+K*3.5*math.sin(a),.6,'#999')
ci(Xf(WK-9),Zf(16),K*6,1,PUR,'4,3'); ci(Xf(WK-9),Zf(16),K*.7,1.1,PUR,None,'#efeaf8')
for a_ in (0,120,240):
    a=math.radians(a_); ln(Xf(WK-9),Zf(16),Xf(WK-9)+K*6*math.cos(a),Zf(16)-K*6*math.sin(a),1.2,PUR)
tx(Xf(WK/2),fy-6,'ÖN (V kesiti) — bu yüz robota bakar',6.5,'middle','bold',GRY)
dim_h(Xf(0),Xf(WK),fy+K*HB+14,'32,5'); dim_v(Xf(WK)+8,fy,fy+K*HB,'55')
tx(Xf(6),Zf(SLOPE/2+2),'45°',5.4,'start','bold',AMB); tx(Xf(WK-3.5)+K*5,Zf(3.5)+3,'helezon Ø7',5,'start','bold',BLU); tx(Xf(WK-9)+K*7,Zf(16)+3,'tarak Ø12',5,'start','bold',PUR)
tx(Xf(WK/2),Zf(HB-9),'dik depo 29,5',5,'middle','','#333'); tx(Xf(WK-14),Zf(8),'dik iç duvar',4.6,'middle','',GRY)
tx(Xf(WK-3.5),Zf(-4),'ağız hattı x 31',4.8,'middle','bold',GRN)
# UST: helezon y yonunde (arkadan one), tarak paralel, agiz on ucta, kavrama arka ucta
ux,uy = XB+160, YB+50
KU=1.9
rc(ux,uy,KU*WK,KU*LB,1.2,1,'#111',None,FILL)
ln(ux+KU*(WK-7),uy+KU*1,ux+KU*(WK-7),uy+KU*(LB-1),.7,AMB,'3,2'); ln(ux+KU*WK-1,uy+KU*1,ux+KU*WK-1,uy+KU*(LB-1),.7,AMB,'3,2')
ln(ux+KU*(WK-3.5),uy+KU*2,ux+KU*(WK-3.5),uy+KU*(LB-2),1.3,BLU)
ln(ux+KU*(WK-9),uy+KU*2,ux+KU*(WK-9),uy+KU*(LB-2),1.2,PUR)
for k in range(14):
    yy=uy+KU*(4+k*4.6); s=1 if k%2==0 else -1; ln(ux+KU*(WK-9),yy,ux+KU*(WK-9+s*6),yy,.9,PUR)
ci(ux+KU*(WK-3.5),uy+KU*(LB-2.5),3,1.4,GRN,None,'#fff'); ci(ux+KU*(WK-3.5),uy+KU*(LB-2.5),1.2,1,GRN,None,GRN)
rc(ux+KU*(WK-5.5),uy-6,KU*4,6,1.1,1,BLU,None,'#dfe7fb'); tx(ux+KU*(WK-3.5),uy-9,'pençe kavrama (arka uç)',4.8,'middle','bold',BLU)
tx(ux+KU*WK/2,uy-20,'ÜST',6.5,'middle','bold',GRY)
tx(ux-6,uy+KU*6,'ARKA',5,'end','bold',GRY); tx(ux-6,uy+KU*LB-2,'ÖN',5,'end','bold',GRY)
dim_v(ux+KU*WK+8,uy,uy+KU*LB,'70'); dim_h(ux,ux+KU*WK,uy+KU*LB+14,'32,5')
tx(ux+KU*(WK/2-4),uy+KU*30,'45° eğimli taban',4.8,'middle','',AMB); tx(ux+KU*(WK-3.5)+8,uy+KU*(LB-2.5)+3,'ağız',5,'start','bold',GRN)
tx(ux+KU*(WK-9)-6,uy+KU*50,'tarak',4.6,'end','',PUR); tx(ux+KU*(WK-3.5)+4,uy+KU*40,'helezon',4.6,'start','',BLU)
# YAN (y boyunca): arka duvar motor, kavrama, helezon 66, tarak, agiz onde
sx,sy = XB+270, YB+50
KY=1.9
Zs=lambda c: sy+KY*(HB-c); Ys=lambda c: sx+KY*c
rc(Ys(0),Zs(HB),KY*LB,KY*HB,1.2,1,'#111',None,FILL)
rc(Ys(.3),Zs(HB-4),KY*(LB-.6),KY*(HB-4-7.3),0,0,'none',None,MAT)
rc(Ys(2),Zs(7),KY*(LB-4),KY*7,1,2,'#111',None,'#fff')
for k in range(1,26): ln(Ys(2+k*2.5),Zs(7),Ys(2+k*2.5),Zs(0),.5,'#999')
ln(Ys(2),Zs(3.5),Ys(LB-2),Zs(3.5),.8,'#555','3,2')
ln(Ys(2),Zs(16),Ys(LB-2),Zs(16),1.4,PUR)
for k in range(14):
    yy=Ys(4+k*4.6); s=1 if k%2==0 else -1; ln(yy,Zs(16),yy,Zs(16+s*6),.9,PUR)
rc(Ys(LB-4),Zs(0),KY*2.5,KY*1.2,0,0,'none',None,'#fff'); ln(Ys(LB-2.7),Zs(0),Ys(LB-2.7),Zs(-6),1.8,GRN)
rc(Ys(-6),Zs(7),KY*5,KY*7,1.1,1,BLU,None,'#dfe7fb'); tx(Ys(-3.5),Zs(1.5),'M',5,'middle','bold',BLU)
rc(Ys(-1),Zs(5),KY*1.2,KY*3,1,0,BLU,None,'#dfe7fb'); rc(Ys(.2),Zs(5),KY*1.2,KY*3,1,0,'#555',None,'#eee')
rc(Ys(-12),Zs(HB+3),KY*4,KY*(HB+8),1,0,'#111',None,'#ccc'); tx(Ys(-10),Zs(HB/2),'arka duvar',4.6,'middle','',GRY)
tx(Ys(LB/2),sy-6,'YAN (derinlik boyunca)',6.5,'middle','bold',GRY)
dim_h(Ys(0),Ys(LB),sy+KY*HB+14,'70'); dim_v(Ys(LB)+8,sy,sy+KY*HB,'55')
tx(Ys(LB/2),Zs(35),'depo',5.2,'middle','','#333'); tx(Ys(LB/2),Zs(21),'tarak mili · 3 dev/dk',4.8,'middle','',PUR); tx(Ys(LB/2),Zs(10),'helezon 66 · 30 dev/dk',4.8,'middle','',BLU)
tx(Ys(LB-2.7),Zs(-9),'ağız (ön uç)',5,'middle','bold',GRN); tx(Ys(-3.5),Zs(-3),'motor arkada',4.6,'middle','',BLU)
arr(Ys(20),Zs(HB+4),Ys(40),Zs(HB+4),AMB,1); tx(Ys(30),Zs(HB+7),'kap öne çekilir (ray) → doldurma',4.8,'middle','',AMB)
# metin
ny=YB+330
lines=[('Kesit: asimetrik kama — dış duvar 45° (x 2 → 27,5), iç duvar dik, oluk bant kenarında (ağız x 31). Kesit alanı %.0f cm² × 70 = %.0f L' % (kesit_alan(HB), vB),'#111','bold'),
       ('Kaşar %.0f kg (0,41 kg/L) = 6,9 gün → HAFTALIK: eleman rayda öne çeker, üstten 4 × 10 kg torba; robot dokunmaz; yedek kap GEREKMEZ' % (vB*0.41),'#1d7a4f','bold'),
       ('3 günlük istersen: aynı kesit, boy 45 → 23 kg — ama yedeğini (35 kg) robot taşıyamaz, eleman hafta ortası gelmeli → haftalık daha doğru','#333',''),
       ('Tarak Ø12, oluğun üstünde eğimli tarafa 5,5 cm kaydırılmış (dik duvara çarpmaz), boydan boya 66, pimli mil, 3 dev/dk','#333',''),
       ('Helezon Ø7 × 66, hatve 2→4 öne doğru, 30 dev/dk, ~20 g/tur; ağız ön uçta kabın tabanında; kat tabanındaki delik (31, 76)','#333',''),
       ('Arka uçta pençe kavrama: kap raya itilince eksenel oturur ("taktığın gibi bağlanır"); motor arka duvarda, kapta elektrik yok','#1a49b8','bold'),
       ('Gövde PE-HD 8 mm ~14 kg + paslanmaz helezon/tarak 4 kg → boş 18 kg, dolu 60 kg → ray 80 kg teleskopik; yıkama boşken (18 kg, 2 kişi ya da tekerlekli)','#333',''),
       ('Yükseklik 55: dik depo 29,5 + V 25,5 — kat 1 = 58; alternatif 48 (35 kg, 5,4 gün) → kat 51','#333','')]
for i,(s,c,fw) in enumerate(lines): tx(XB+14,ny+i*14,s,6,'start',fw,c)
tx(XB+14,ny+120,'Neden asimetrik: iki kap yan yana, ağızlar 31 ve 39'+chr(39)+'da → oluklar iç kenarda olmak zorunda; dış duvar 45° eğimle malzemeyi oluğa getirir, tarak köprüyü kırar.',5.6,'start','',GRY)
tx(XB+14,ny+133,'Asimetrik kama huni sanayide standart (tek eğimli duvar); akış için eğimli duvar 45° yeterli çünkü tarak var.',5.6,'start','',GRY)
tx(XB+14,ny+150,'AÇIK: rendelenmiş kaşar 45° tek eğim + tarak prototipi · 60 kg kabı çekmek (ray) · üst kapak (izole, menteşeli)',5.6,'start','',AMB)

# ================= KÜÇÜK KAP =================
XS,YS = 580,100
rc(XS,YS,380,540,1.4,4,'#111',None,'#fcfbf8')
tx(XS+14,YS+22,'KÜÇÜK KAP — SUCUK · KAVURMA · KUŞBAŞI · 32,5 × 20 × 28 · %.1f L' % vS,9.5,'start','bold')
# ON (V kesiti kucuk) — sag kap: ic duvar SOLDA dik, dis duvar sagda 45° (ayna)
fx2,fy2 = XS+30, YS+50
Z2=lambda c: fy2+K*(HS-c); X2=lambda c: fx2+K*c
poly([(X2(0),Z2(HS)),(X2(WK),Z2(HS)),(X2(WK),Z2(SLOPE if SLOPE<HS else HS)),(X2(7),Z2(0)),(X2(0),Z2(0))],1.3,'#111',SUC)
ci(X2(3.5),Z2(3.5),K*3.5,1.1,'#111',None,'#fff'); ci(X2(9),Z2(14),K*5,1,PUR,'4,3'); ci(X2(9),Z2(14),K*.7,1.1,PUR,None,'#efeaf8')
for a_ in (0,120,240):
    a=math.radians(a_); ln(X2(9),Z2(14),X2(9)+K*5*math.cos(a),Z2(14)-K*5*math.sin(a),1.2,PUR)
tx(X2(WK/2),fy2-6,'ÖN (V kesiti) — sağ kap: oluk solda (x 39)',6.5,'middle','bold',GRY)
dim_h(X2(0),X2(WK),fy2+K*HS+14,'32,5'); dim_v(X2(WK)+8,fy2,fy2+K*HS,'28')
tx(X2(WK-6),Z2(12),'45°',5.4,'end','bold',AMB); tx(X2(3.5),Z2(-4),'ağız x 39',4.8,'middle','bold',GRN)
tx(X2(9)+K*6,Z2(14)+3,'tarak Ø10',5,'start','bold',PUR); tx(X2(3.5)+K*5,Z2(3.5)+3,'helezon Ø7',5,'start','bold',BLU)
tx(X2(WK/2+3),Z2(HS-5),'V duvarı 25,5 — kabın tamamı huni',4.6,'middle','','#333')
# UST kucuk
ux2,uy2 = XS+160, YS+50
rc(ux2,uy2,KU*WK,KU*LS,1.2,1,'#111',None,SUC)
ln(ux2+KU*3.5,uy2+KU*1.5,ux2+KU*3.5,uy2+KU*(LS-1.5),1.3,BLU); ln(ux2+KU*9,uy2+KU*1.5,ux2+KU*9,uy2+KU*(LS-1.5),1.2,PUR)
for k in range(4):
    yy=uy2+KU*(3+k*4.6); s=1 if k%2==0 else -1; ln(ux2+KU*9,yy,ux2+KU*(9+s*5),yy,.9,PUR)
ci(ux2+KU*3.5,uy2+KU*(LS-2),3,1.4,GRN,None,'#fff'); rc(ux2+KU*1.5,uy2-6,KU*4,6,1.1,1,BLU,None,'#dfe7fb')
tx(ux2+KU*WK/2,uy2-20,'ÜST',6.5,'middle','bold',GRY); tx(ux2+KU*3.5,uy2-9,'kavrama',4.6,'middle','bold',BLU)
dim_v(ux2+KU*WK+8,uy2,uy2+KU*LS,'20'); dim_h(ux2,ux2+KU*WK,uy2+KU*LS+14,'32,5')
# YAN kucuk
sx2,sy2 = XS+270, YS+50
Zs2=lambda c: sy2+KY*(HS-c); Ys2=lambda c: sx2+KY*c
rc(Ys2(0),Zs2(HS),KY*LS,KY*HS,1.2,1,'#111',None,SUC)
rc(Ys2(1.5),Zs2(7),KY*(LS-3),KY*7,1,2,'#111',None,'#fff'); ln(Ys2(1.5),Zs2(14),Ys2(LS-1.5),Zs2(14),1.3,PUR)
rc(Ys2(LS-3.5),Zs2(0),KY*2.2,KY*1.2,0,0,'none',None,'#fff'); ln(Ys2(LS-2.4),Zs2(0),Ys2(LS-2.4),Zs2(-6),1.8,GRN)
rc(Ys2(-6),Zs2(7),KY*5,KY*7,1.1,1,BLU,None,'#dfe7fb'); tx(Ys2(-3.5),Zs2(1.5),'M',5,'middle','bold',BLU)
tx(Ys2(LS/2),sy2-6,'YAN',6.5,'middle','bold',GRY); dim_h(Ys2(0),Ys2(LS),sy2+KY*HS+14,'20'); dim_v(Ys2(LS)+8,sy2,sy2+KY*HS,'28')
tx(Ys2(-3.5),Zs2(-3),'motor arkada',4.4,'middle','',BLU); tx(Ys2(LS-2.4),Zs2(-9),'ağız',4.8,'middle','bold',GRN)
# sucuk varyanti: yatay cubuk magazini + itici + bicak (ust gorunus)
vx,vy = XS+30, YS+225
tx(vx,vy-6,'SUCUK varyantı — aynı kabuk: yatay çubuk magazini + itici + bıçak',6.5,'start','bold',AMB)
rc(vx,vy,KU*WK,KU*LS,1.2,1,'#111',None,SUC)
for r in range(4): rc(vx+KU*7,vy+KU*(1.5+r*4.5),KU*25,KU*4,.7,2,'#555',None,'#f4ece6')
rc(vx+KU*1,vy+KU*(LS/2-3),KU*5,KU*6,1,1,RED,None,'#fdeeee'); tx(vx+KU*3.5,vy+KU*LS/2+1,'bıçak',4,'middle','bold',RED)
arr(vx+KU*32,vy+KU*LS/2,vx+KU*8,vy+KU*LS/2,AMB,1); tx(vx+KU*20,vy+KU*LS/2-3,'itici → çubuğu bıçağa sürer',4.4,'middle','',AMB)
ci(vx+KU*3.5,vy+KU*(LS-2),3,1.4,GRN,None,'#fff')
tx(vx+KU*WK/2,vy+KU*LS+10,'çubuklar Ø4×25 yatay (x), 4 sıra × 7 kat = 28 çubuk = 8,7 kg ≈ hafta ✓ · alttaki çubuk bıçağa iner (yerçekimi)',4.6,'middle','','#333')
tx(vx+KU*WK/2,vy+KU*LS+20,'itici vidalı (arka motordan), bıçak 3 mm dilim, dilim ağızdan tepsiye · tarak/helezon yok',4.6,'middle','','#333')
ny2=YS+310
lines2=[('Kesit alanı %.0f cm² × 20 = %.1f L' % (kesit_alan(HS), vS),'#111','bold'),
        ('KUŞBAŞI 3 gün 4 kg = 7,3 L → %%%d dolu ✓ · KAVURMA 3 gün 3,3 kg = 6 L → %%%d ✓' % (7.3/vS*100, 6/vS*100),'#333',''),
        ('SUCUK 28 çubuk 8,7 kg ≈ 7 gün ✓ (en 32,5 → çubuk 25 + bıçak 6 sığdı)','#1d7a4f','bold'),
        ('Boş 4,5 kg · dolu ≤ 13 kg → robot 12 kg kobotla taşır (sucuğu eleman da olur)','#333',''),
        ('STORE −18 kaset çekmecesi: 28 ≤ 29 ✓, 61 modülde 32,5 → 1 kap yan yana (2 modül = 2 kap)','#333',''),
        ('Tarak Ø10 z 14 · helezon Ø7 × 17 · aynı dişli, aynı pençe, aynı motor tipi','#333',''),
        ('Kavurma yapışkan → tarak şart · kuşbaşı küp → aynı parça · sucuk → bıçaklı iç','#333','')]
for i,(s,c,fw) in enumerate(lines2): tx(XS+14,ny2+i*13.5,s,6,'start',fw,c)
tx(XS+14,ny2+108,'Küçük kap kısa (20) çünkü V duvarı zaten 25,5 yatay: 20 derinlikte %.1f L yeter. Daha uzun kap = daha çok yedek alanı; gerek yok.' % vS,5.6,'start','',GRY)
tx(XS+14,ny2+121,'Sağ kaplar sol kapların aynası: oluk sol kenarda (x 39), eğim sağa (dış duvara) doğru.',5.6,'start','',GRY)
tx(XS+14,ny2+138,'AÇIK: sucuk yatay magazin + itici detayı (vida hatvesi, çubuk çapı toleransı Ø38-42) · STORE modülünde 32,5 en (1 kap/modül)',5.6,'start','',AMB)

# ================= YERLEŞİM + DOK =================
XP,YP = 980,100
rc(XP,YP,450,540,1.4,4)
tx(XP+14,YP+22,'YERLEŞİM 70 × 84 — motorlar arkada · DOK',10,'start','bold')
KP=1.85
def kat_plan(X,Y,ad,kat):
    tx(X+KP*35,Y-6,ad,6.8,'middle','bold')
    rc(X,Y,KP*70,KP*84,1.2); rc(X+KP*31,Y,KP*8,KP*84,0,0,'none',None,'#dff3e6')
    rc(X,Y,KP*70,KP*8,0,0,'none',None,'#e5e5e5'); tx(X+KP*35,Y+KP*5.5,'arka: motorlar + elektrik 8',4,'middle','',GRY)
    if kat==1:
        rc(X+KP*2,Y+KP*8,KP*WK,KP*LB,1.1,1,'#111',None,FILL); ln(X+KP*31,Y+KP*10,X+KP*31,Y+KP*76,1,BLU); ci(X+KP*31,Y+KP*76,2.4,1.2,GRN,None,'#fff')
        tx(X+KP*17,Y+KP*36,'KAŞAR',5.6,'middle','bold'); tx(X+KP*17,Y+KP*42,'32,5×70×55',4.2,'middle','','#333'); tx(X+KP*17,Y+KP*47,'42 kg · hafta',4.2,'middle','','#333')
        rc(X+KP*27,Y+KP*2,KP*8,KP*6,1,1,BLU,None,'#dfe7fb'); tx(X+KP*31,Y+KP*6.2,'M1',3.8,'middle','bold',BLU)
        rc(X+KP*35.5,Y+KP*56,KP*WK,KP*LS,1.1,1,'#111',None,SUC); ci(X+KP*39,Y+KP*74,2.4,1.2,GRN,None,'#fff')
        tx(X+KP*52,Y+KP*64,'SUCUK',5.6,'middle','bold'); tx(X+KP*52,Y+KP*70,'32,5×20×28 · hafta',4,'middle','','#333')
        rc(X+KP*35.5,Y+KP*48,KP*8,KP*6,1,1,BLU,None,'#dfe7fb'); tx(X+KP*39.5,Y+KP*52.2,'M2',3.8,'middle','bold',BLU)
        ln(X+KP*39,Y+KP*8,X+KP*39,Y+KP*48,.8,BLU,'3,2'); tx(X+KP*52,Y+KP*30,'ara mil / motor',4,'middle','',BLU); tx(X+KP*52,Y+KP*35,'doğrudan kabın',4,'middle','',BLU); tx(X+KP*52,Y+KP*40,'arkasında',4,'middle','',BLU)
        outs=((31,76),(39,74))
    else:
        for (x0,lab,ox) in ((2,'KAVURMA',31),(35.5,'KUŞBAŞI',39)):
            rc(X+KP*x0,Y+KP*56,KP*WK,KP*LS,1.1,1,'#111',None,SUC); ci(X+KP*ox,Y+KP*74,2.4,1.2,GRN,None,'#fff')
            tx(X+KP*(x0+16),Y+KP*64,lab,5.6,'middle','bold'); tx(X+KP*(x0+16),Y+KP*70,'32,5×20×28 · 3 gün',4,'middle','','#333')
            rc(X+KP*(ox-4),Y+KP*48,KP*8,KP*6,1,1,BLU,None,'#dfe7fb'); tx(X+KP*ox,Y+KP*52.2,'M',3.8,'middle','bold',BLU)
            ln(X+KP*ox,Y+KP*8,X+KP*ox,Y+KP*48,.8,BLU,'3,2')
        rc(X+KP*2,Y+KP*10,KP*66,KP*36,.8,2,'#999','4,3','#fafafa'); tx(X+KP*35,Y+KP*28,'boş (arka) — motor/kablo/hava',4.6,'middle','',GRY)
        outs=((31,74),(39,74))
    for (ox,oy) in outs: ci(X+KP*ox,Y+KP*oy,KP*31,.7,GRN,'4,3')
    rc(X,Y+KP*79,KP*70,KP*3,1,0,BLU,None,'#dfe7fb'); tx(X+KP*35,Y+KP*81.3,'klape',4,'middle','',BLU)
kat_plan(XP+16,YP+46,'KAT 1 — kaşar + sucuk (düzlem 1)',1)
kat_plan(XP+236,YP+46,'KAT 2 — kavurma + kuşbaşı (düzlem 2)',2)
# dok detayi (yan): kap arkaya itilir, pence eksenel oturur
dkx,dky = XP+16, YP+230
rc(dkx,dky,418,120,1,3,'#999',None,'#fff'); tx(dkx+209,dky+14,'DOK — "taktığın gibi bağlanır": eksenel pençe kavrama (yan görünüş)',6.8,'middle','bold')
KDk=2.2
Xd=lambda c: dkx+60+KDk*c; Zd=lambda c: dky+96-KDk*c
rc(Xd(0),Zd(28),KDk*40,KDk*28,1.1,1,'#111',None,SUC); tx(Xd(20),Zd(16),'KAP (pasif)',5.6,'middle','bold'); tx(Xd(20),Zd(10),'helezon mili',4.4,'middle','',GRY)
ln(Xd(2),Zd(3.5),Xd(38),Zd(3.5),1.2,'#333'); rc(Xd(-1.5),Zd(5.5),KDk*1.5,KDk*4,1,0,'#555',None,'#eee'); rc(Xd(-3.2),Zd(5.5),KDk*1.5,KDk*4,1,0,BLU,None,'#dfe7fb')
rc(Xd(-12),Zd(7.5),KDk*8.5,KDk*8,1.1,1,BLU,None,'#dfe7fb'); tx(Xd(-7.7),Zd(2.5),'M 40 W',5,'middle','bold',BLU)
rc(Xd(-14),Zd(32),KDk*1.5,KDk*36,1,0,'#111',None,'#ccc'); tx(Xd(-16),Zd(20),'arka',4.4,'end','',GRY)
arr(Xd(46),Zd(20),Xd(41),Zd(20),AMB,1.2); tx(Xd(47),Zd(22),'kap raya itilir →',4.8,'start','',AMB); tx(Xd(47),Zd(16),'pençe eksenel oturur',4.8,'start','bold',BLU)
tx(Xd(47),Zd(10),'pahlı diş, yaylı → kendi hizalar',4.6,'start','','#333'); tx(Xd(47),Zd(4),'kapta elektrik/motor yok',4.6,'start','bold',GRN)
for xx in (4,36): rc(Xd(xx),Zd(-1),KDk*2.5,KDk*1.6,1,1,AMB,None,'#fdf3dd')
tx(Xd(20),Zd(-4.5),'yük hücresi ×2 (ray taşıyıcısı altında) → gram + "boşaldı"',4.4,'middle','',AMB)
rc(Xd(-14),Zd(-1),KDk*56,KDk*1,.8,0,'#111',None,'#bbb')
# on kesit mini
KM=1.2
mx,my = XP+16, YP+366
rc(mx,my,KM*70,KM*197,1.3); zz=0
for ad,h,col in Z:
    rc(mx,my+KM*zz,KM*70,KM*h,.6,0,'#111',None,col); tx(mx+KM*70+4,my+KM*(zz+h/2)+2,'%s %g'%(ad,h),4.4,'start','',GRY); zz+=h
rc(mx+KM*2,my+KM*(27+2),KM*WK,KM*55,.9,1,'#111',None,FILL); tx(mx+KM*18,my+KM*58,'KAŞAR 55',4.2,'middle','bold')
rc(mx+KM*35.5,my+KM*(27+29),KM*WK,KM*28,.9,1,'#111',None,SUC); tx(mx+KM*52,my+KM*72,'SUCUK',4.2,'middle','bold')
for xx in (31,39): ln(mx+KM*xx,my+KM*85,mx+KM*xx,my+KM*89,1.3,GRN)
el(mx+KM*35,my+KM*95,KM*17,KM*1.2,.9,BLU,None,'#dfe7fb')
rc(mx+KM*2,my+KM*(99+2),KM*WK,KM*28,.9,1,'#111',None,SUC); rc(mx+KM*35.5,my+KM*(99+2),KM*WK,KM*28,.9,1,'#111',None,SUC)
tx(mx+KM*18,my+KM*117,'KAV.',4.2,'middle','bold'); tx(mx+KM*52,my+KM*117,'KUŞ.',4.2,'middle','bold')
for xx in (31,39): ln(mx+KM*xx,my+KM*130,mx+KM*xx,my+KM*134,1.3,GRN)
el(mx+KM*35,my+KM*140,KM*17,KM*1.2,.9,BLU,None,'#dfe7fb')
for (xx,lab) in ((2,'sucuk yedek'),(35.5,'çözülme ×2')):
    rc(mx+KM*xx,my+KM*(144+12),KM*WK,KM*28,.8,1,'#999','3,2',LIGHT); tx(mx+KM*(xx+16),my+KM*172,lab,3.8,'middle','','#666')
tx(mx+KM*35,my+KM*197+10,'ÖN KESİT 1:8,3',4.8,'middle','bold',GRY)
tx(mx+KM*70+70,my+KM*30,'dikey 27+58+14+31+14+53 = 197 ✓',5.2,'start','bold',GRN)
tx(mx+KM*70+70,my+KM*42,'tepsi düzlemleri 100 / 55 cm',5,'start','',BLU)
tx(mx+KM*70+70,my+KM*54,'kat 1: kaşar 55 + sucuk 28 (üstü boş)',5,'start','','#333')
tx(mx+KM*70+70,my+KM*66,'kat 2: iki küçük kap, arkası boş',5,'start','','#333')
tx(mx+KM*70+70,my+KM*78,'ALT 53: sucuk yedeği + kav/kuş çözülme',5,'start','','#333')
tx(mx+KM*70+70,my+KM*90,'+ boş kap parkı · kaşar yedeği YOK (haftalık)',5,'start','','#333')
tx(mx+KM*70+70,my+KM*106,'kavurmalı/kuşbaşılı pide: kaşarı kat 1'+chr(39)+'den',5,'start','bold',AMB)
tx(mx+KM*70+70,my+KM*118,'alır → tepsi bir kez kat değiştirir (+5 sn)',5,'start','',AMB)
tx(mx+KM*70+70,my+KM*134,'STORE −18: kav ×2 + kuş ×2 küçük kap (28 ≤ 29)',5,'start','','#333')
tx(mx+KM*70+70,my+KM*146,'robot: kav/kuş 3 günde 1 + sucuk haftada 1',5,'start','bold',GRN)
tx(mx+KM*70+70,my+KM*158,'eleman: kaşar doldurur, STORE'+chr(39)+'u yeniler',5,'start','',GRN)

# ================= TABLO + KARAR =================
YT=670
rc(40,YT,1390,480,1.6,4)
tx(56,YT+24,'DÖRT KAP — v19 ÖZET · KONTROL',12,'start','bold')
hdr=['malzeme','kap','hacim','dolum','gün','kat / pozisyon','ağız','motor','değiştiren','yedek']
cx_=[56,170,310,380,470,540,700,790,880,1120]
for i,h in enumerate(hdr): tx(cx_[i],YT+50,h,7,'start','bold',GRY)
ln(54,YT+56,1414,YT+56,.8,'#bbb')
rows=[('KAŞAR','32,5×70×55','%.0f L' % vB,'42 kg','6,9 (hafta)','kat 1 sol, tam derinlik','(31, 76)','arka duvar M1','eleman haftalık (rayda doldurur)','yok'),
      ('SUCUK','32,5×20×28','%.1f L' % vS,'28 çubuk 8,7 kg','7 (hafta)','kat 1 sağ, önde','(39, 74)','kabın arkasında M2','robot haftalık (ALT'+chr(39)+'tan)','ALT: 1 kap'),
      ('KAVURMA','32,5×20×28','%.1f L' % vS,'3,3 kg','3','kat 2 sol, önde','(31, 74)','kabın arkasında M3','robot 3 günde','STORE −18 ×2 → ALT çözülme'),
      ('KUŞBAŞI','32,5×20×28','%.1f L' % vS,'4 kg','3','kat 2 sağ, önde','(39, 74)','kabın arkasında M4','robot 3 günde','STORE −18 ×2 → ALT çözülme')]
for i,r in enumerate(rows):
    yy=YT+74+i*20
    for j,v in enumerate(r): tx(cx_[j],yy,v,6.6,'start','bold' if j==0 else '','#111' if j==0 else '#333')
ln(54,YT+160,1414,YT+160,.8,'#bbb')
notes=[('Döndürme ne kazandırdı: (1) motor arkada, kap itilince eksenel pençe oturur — dişli hizalama derdi yok · (2) ön yüz = V kesiti, tarak ve oluk öne bakar, gözle kontrol · (3) kaşar tam derinlik 70 → 42 kg HAFTALIK, yedek kap ve robot taşıması bitti',GRN,'bold'),
       ('Bedel: oluk bant kenarında olmak zorunda → kesit asimetrik (tek eğimli duvar 45°, iç duvar dik); tarak eğimli tarafa kaydırıldı. Sanayide standart, kaşar için prototip şart.',AMB,''),
       ('Kesit alanı sabit (%.0f cm² büyük, %.0f cm² küçük): kap boyu = hacim. Kaşar 70 → 42 kg; 45 → 23 kg (3 gün). Küçükler 20 derinlik yeter (%.1f L).' % (kesit_alan(HB), kesit_alan(HS), vS),'#333',''),
       ('Kat 2 arkası boş (36 × 66): motorlar, kablo, hava kanalı; istersen ileride 3. küçük kap (ör. mısır/zeytin) — ağız bantta olmaz ama arka kap öndekinin yedeği olabilir.','#333',''),
       ('Robot hamleleri: kav/kuş 3 günde 1 (2 hamle: boş → ALT park, ALT çözülmüş → kat 2), sucuk haftada 1; kol yükü ≤ 13 kg ✓ 12 kg kobot sınırda → sucuk kabını eleman değiştirsin (10 kg kural)','#333',''),
       ('Kavurmalı / kuşbaşılı pidede tepsi kat 2 → kat 1 (kaşar) geçer: +5 sn, pidelerin %35'+chr(39)+'i · sucuklu ve kaşarlı tek düzlemde',AMB,''),
       ('KONTROL: bant ✓ (31/39) · arka ≥ 31 ✓ (74-76) · süpürme sol x 0-62 / sağ 8-70 ✓ · dikey 197 ✓ · derinlik 8 motor + 70 kap + 3 klape + 3 = 84 ✓ · STORE 28 ≤ 29 ✓ · kol ≤ 12 kg ✓',GRN,'bold'),
       ('AÇIK: kaşar 45° tek eğim + tarak akış prototipi · sucuk yatay magazin/itici detayı · 60 kg kap rayı ve üst kapak · klape contası · HAT v45 TOPPING bloğu (kat 58/31)',AMB,'')]
for i,(s,c,fw) in enumerate(notes): tx(56,YT+180+i*20,s,6.5,'start',fw,c)
tx(56,YT+350,'v18 → v19: kaplar 90° döndü (helezon derinlik yönünde), kaşar 27×65×48 → 32,5×70×55 haftalık, küçük 27×21×28 → 32,5×20×28 (sucuk 28 çubuk sığdı), motorlar arkada, yerleşim Kemal'+chr(39)+'in dediği gibi.',7,'start','bold','#111')
tx(56,YT+368,'Sıradaki: HAT v45 (TOPPING bloğu v19) · sucuk magazin detayı · kaşar prototip listesi.',7,'start','','#333')
tx(W-40,H-12,'AUTOKITCH · arastirma/3_TOPPING/ist3_topping_detay_v19 · 5 Eyl 2026',7,'end','',GRY)
o.append('</svg>')
svg = chr(10).join(o)
xml.dom.minidom.parseString(svg.encode('utf-8'))
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\ist3_topping_detay_v19.svg"
io.open(out,'w',encoding='utf-8').write(svg)
print('yazildi + XML gecerli | buyuk kesit %.0f cm2 → %.0f L → %.0f kg | kucuk %.0f cm2 → %.1f L' % (kesit_alan(HB),vB,vB*0.41,kesit_alan(HS),vS))
