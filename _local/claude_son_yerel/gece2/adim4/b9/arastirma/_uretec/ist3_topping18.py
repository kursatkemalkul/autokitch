# -*- coding: utf-8 -*-
# TOPPING v18 — KAPLAR: BÜYÜK (kaşar 3 gün) + KÜÇÜK (sucuk hafta / kavurma 3 gün / kuşbaşı 3 gün, aynı ölçü) · içinde TEK tarak (köprü kırıcı) + altta dozaj helezonu
# üst/ön/yan · ölçüler · kg · yerleşim (kat 1 / kat 2) · tablo
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
def poly(pts,sw=1,c='#111',f='none',d=None):
    o.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (' '.join('%.1f,%.1f'%p for p in pts),f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def arr(x1,y1,x2,y2,c='#c0392b',w=1.2):
    ln(x1,y1,x2,y2,w,c); a=math.atan2(y2-y1,x2-x1)
    for s in (1,-1): ln(x2,y2,x2-6*math.cos(a-s*.42),y2-6*math.sin(a-s*.42),w,c)
def dim_h(x1,x2,y,s,fs=6): ln(x1,y,x2,y,.7); ln(x1,y-3,x1,y+3,.7); ln(x2,y-3,x2,y+3,.7); tx((x1+x2)/2,y-3,s,fs,'middle','bold')
def dim_v(x,y1,y2,s,fs=6): ln(x,y1,x,y2,.7); ln(x-3,y1,x+3,y1,.7); ln(x-3,y2,x+3,y2,.7); tx(x+4,(y1+y2)/2+2,s,fs,'start','bold')

GRN, RED, BLU, GRY, AMB, PUR = '#1d7a4f', '#c0392b', '#1a49b8', '#666', '#b7791f', '#6b4fa8'
FILL, MAT, SUC, LIGHT = '#f1efe8', '#e9dfa8', '#e8eef8', '#f7f6f2'
def hacim(L,Wd,Hh):
    w=Wd/2; v=(w*w-12.25)*L/1000; g=L*Wd*Hh/1000; return g,v,g-v
gB,vB,uB = hacim(27,65,48); gS,vS,uS = hacim(27,21,28)

o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H))
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,42,'AUTOKITCH — TOPPING v18 (5 Eyl 2026) — KAPLAR: BÜYÜK KAP kaşar 3 gün · KÜÇÜK KAP sucuk hafta / kavurma 3 gün / kuşbaşı 3 gün (aynı ölçü) · içinde TEK tarak + altta dozaj helezonu · ölçüler cm',15,'start','bold')
tx(30,66,'Evet: her kabın içinde boydan boya dönen bir TARAK (köprü kırıcı tel, pimli mil) ve en altta malzemeyi gramajlı iten DOZAJ HELEZONU var; başka hareketli parça yok. Gram = helezon turu + ray altındaki yük hücresi. Kaşar daha büyük kap ister (3 gün = 23 kg); sucuk/kavurma/kuşbaşı tek küçük kapta.',9.5,'start','','#444')
ln(30,78,W-30,78,.8,'#999')

# ================= BÜYÜK KAP =================
XB,YB = 40,100
rc(XB,YB,500,560,1.4,4,'#111',None,'#fcfdff')
tx(XB+14,YB+22,'BÜYÜK KAP — KAŞAR · 27 × 65 × 48 · 3 gün (+½ gün pay) = 23 kg',10,'start','bold')
K=3.0
L,Wd,Hh = 27,65,48
# UST
ux,uy = XB+30, YB+50
rc(ux,uy,K*L,K*Wd,1.2,1,'#111',None,FILL)
ln(ux+K*1,uy+K*(Wd/2-3.5),ux+K*(L-1),uy+K*(Wd/2-3.5),.7,AMB,'3,2'); ln(ux+K*1,uy+K*(Wd/2+3.5),ux+K*(L-1),uy+K*(Wd/2+3.5),.7,AMB,'3,2')
ln(ux+K*1,uy+K*Wd/2,ux+K*(L-1),uy+K*Wd/2,1.3,BLU)
ln(ux+K*1,uy+K*Wd/2,ux+K*(L-1),uy+K*Wd/2,1.3,BLU)
for k in range(8):
    xx=ux+K*(2.5+k*3.2); s=1 if k%2==0 else -1; ln(xx,uy+K*Wd/2,xx,uy+K*(Wd/2+s*8),1,'#6b4fa8')
ci(ux+K*(L-2),uy+K*Wd/2,3,1.4,GRN,None,'#fff'); ci(ux+K*(L-2),uy+K*Wd/2,1.2,1,GRN,None,GRN)
ci(ux-1,uy+K*Wd/2,2.6,1.1,'#555',None,'#eee')
tx(ux+K*L/2,uy-6,'ÜST',6.5,'middle','bold',GRY)
dim_h(ux,ux+K*L,uy+K*Wd+14,'27'); dim_v(ux+K*L+8,uy,uy+K*Wd,'65')
tx(ux+K*L/2,uy+K*10,'V-oluk',5,'middle','',AMB); tx(ux+K*L/2,uy+K*(Wd/2-6),'tarak pimleri',4.8,'middle','',PUR); tx(ux+K*L/2,uy+K*(Wd/2+13),'helezon',4.8,'middle','',BLU)
tx(ux+K*L+14,uy+K*Wd/2+3,'ağız (iç uç)',5,'start','bold',GRN); tx(ux-6,uy+K*Wd/2-6,'dişli',4.8,'end','','#555')
# ON (helezon boyunca)
fx,fy = XB+160, YB+50
Zf=lambda c: fy+K*(Hh-c)
rc(fx,fy,K*L,K*Hh,1.2,1,'#111',None,FILL)
rc(fx+K*.3,Zf(Hh-4),K*(L-.6),K*(Hh-4-7.3),0,0,'none',None,MAT)
rc(fx+K*1,Zf(7),K*(L-2),K*7,1,2,'#111',None,'#fff')
for k in range(1,10): ln(fx+K*(1+k*2.5),Zf(7),fx+K*(1+k*2.5),Zf(0),.6,'#999')
ln(fx+K*1,Zf(3.5),fx+K*(L-1),Zf(3.5),.8,'#555','3,2')
ln(fx+K*1,Zf(14),fx+K*(L-1),Zf(14),1.5,PUR)
for k in range(8):
    xx=fx+K*(2.5+k*3.2); s=1 if k%2==0 else -1; ln(xx,Zf(14),xx,Zf(14+s*8),1,PUR)
rc(fx+K*(L-3),Zf(0),K*2,K*1.2,0,0,'none',None,'#fff'); ln(fx+K*(L-2),Zf(0),fx+K*(L-2),Zf(-5),1.8,GRN)
ci(fx-1,Zf(3.5),2.6,1.1,'#555',None,'#eee')
rc(fx-K*4,Zf(7),K*3.4,K*7,1,1,BLU,None,'#dfe7fb'); tx(fx-K*2.3,Zf(1.6),'M',4.6,'middle','bold',BLU)
tx(fx+K*L/2,fy-6,'ÖN (helezon boyu)',6.5,'middle','bold',GRY)
dim_v(fx+K*L+8,fy,fy+K*Hh,'48'); dim_h(fx,fx+K*L,fy+K*Hh+14,'27')
tx(fx+K*L/2,Zf(30),'depo',5.2,'middle','','#333'); tx(fx+K*L/2,Zf(19),'tarak mili z 14',4.6,'middle','',PUR); tx(fx+K*L/2,Zf(9.5),'dozaj helezonu',4.6,'middle','',BLU)
tx(fx+K*L+14,Zf(-3),'ağız',5,'start','bold',GRN)
# YAN (V kesiti)
sx,sy = XB+270, YB+50
w=Wd/2; vd=w-3.5
Zs=lambda c: sy+K*(Hh-c)
poly([(sx,Zs(Hh)),(sx+K*Wd,Zs(Hh)),(sx+K*Wd,Zs(vd)),(sx+K*(w+3.5),Zs(0)),(sx+K*(w-3.5),Zs(0)),(sx,Zs(vd))],1.2,'#111',FILL)
poly([(sx+K*.3,Zs(Hh-4)),(sx+K*Wd-K*.3,Zs(Hh-4)),(sx+K*Wd-K*.3,Zs(vd)),(sx+K*(w+3.5),Zs(.3)),(sx+K*(w-3.5),Zs(.3)),(sx+K*.3,Zs(vd))],0,'none',MAT)
ci(sx+K*w,Zs(3.5),K*3.5,1.1,'#111',None,'#fff')
for k in range(6):
    a=math.radians(k*60+20); ln(sx+K*w,Zs(3.5),sx+K*w+K*3.5*math.cos(a),Zs(3.5)+K*3.5*math.sin(a),.6,'#999')
ci(sx+K*w,Zs(14),K*8,1,PUR,'4,3'); ci(sx+K*w,Zs(14),K*.7,1.1,PUR,None,'#efeaf8')
for a_ in (0,120,240):
    a=math.radians(a_); ln(sx+K*w,Zs(14),sx+K*w+K*8*math.cos(a),Zs(14)-K*8*math.sin(a),1.2,PUR)
tx(sx+K*Wd/2,sy-6,'YAN (V kesiti)',6.5,'middle','bold',GRY)
dim_h(sx,sx+K*Wd,sy+K*Hh+14,'65'); dim_v(sx+K*Wd+8,sy,sy+K*Hh,'48')
tx(sx+K*6,Zs(vd/2+2),'45°',5.4,'start','bold',AMB); tx(sx+K*Wd-K*6,Zs(vd/2+2),'45°',5.4,'end','bold',AMB)
tx(sx+K*w,Zs(Hh-9),'dik depo 19',5,'middle','','#333'); tx(sx+K*w,Zs(28),'V derinliği 29',5,'middle','',AMB)
tx(sx+K*w+K*10,Zs(14)+3,'tarak Ø16 · 3 dev/dk',5,'start','bold',PUR); tx(sx+K*w+K*10,Zs(3.5)+3,'helezon Ø7 · 30 dev/dk',5,'start','bold',BLU)
# metin
ny=YB+330
lines=[('Hacim: %.0f L brüt − V-oluk %.0f L = %.0f L → kaşar %.0f kg (0,41 kg/L)' % (gB,vB,uB,uB*0.41),'#111','bold'),
       ('Günlük kaşar ~6,1 kg (80 pide) → 3 gün 18,3 kg; kap 23 kg = 3,5 gün (pay)','#333',''),
       ('İKİ kaşar kabı (kat 1 + kat 2) → her biri pidelerin yarısına bakar → 8 gün ≥ hafta ✓','#1d7a4f','bold'),
       ('→ eleman haftada 1 doldurur; robot kaşara dokunmaz (dolu 35 kg)','#1d7a4f',''),
       ('Gövde PE-HD 8 mm ~9 kg + paslanmaz helezon/tarak/dişli 3 kg → boş 12 kg','#333',''),
       ('Tek tarak: pimli mil z 14, 27 boyunca, süpürme Ø16 — V dibini tarar; üstteki 45°','#333',''),
       ('duvarlar kendi akar. Helezon Ø7 × 25, hatve 2→4, ~20 g/tur → 80 g = 4 tur = 8 sn','#333',''),
       ('Ağız iç uçta (bant x 31/39) · dış uçta dişli → duvardaki 40 W motor (4 cm boşluk)','#333',''),
       ('Doldurma: kap rayda 60 cm öne çekilir, üst kapak, 2 torba × 10 kg + 3 kg','#333',''),
       ('Yıkama: boşken çıkar (12 kg), helezon + tarak tek parça, sökmeden yıkanır','#333','')]
for i,(s,c,fw) in enumerate(lines): tx(XB+14,ny+i*14,s,6.3,'start',fw,c)
tx(XB+14,ny+150,'Neden 65 derin: 3 günlük 23 kg tek helezonla ancak geniş V ile sığar (V 29 cm derin, 28 L kayıp).',5.6,'start','',GRY)
tx(XB+14,ny+163,'Daha derin kap (78) hacmi artırmaz — V büyür (bkz. v17 çift helezon). 3 gün için 65 doğru.',5.6,'start','',GRY)
tx(XB+14,ny+176,'AÇIK: 45° V + tarak ile rendelenmiş kaşar akış prototipi; kap tepsi düzlemi 42 cm (kat 2) kobot erişimi.',5.6,'start','',AMB)

# ================= KÜÇÜK KAP =================
XS,YS = 560,100
rc(XS,YS,400,560,1.4,4,'#111',None,'#fcfbf8')
tx(XS+14,YS+22,'KÜÇÜK KAP — SUCUK · KAVURMA · KUŞBAŞI · 27 × 21 × 28 (tek ölçü)',10,'start','bold')
L2,W2,H2 = 27,21,28
# UST helezonlu
ux2,uy2 = XS+30, YS+50
rc(ux2,uy2,K*L2,K*W2,1.2,1,'#111',None,SUC)
ln(ux2+K*1,uy2+K*(W2/2-3.5),ux2+K*(L2-1),uy2+K*(W2/2-3.5),.7,AMB,'3,2'); ln(ux2+K*1,uy2+K*(W2/2+3.5),ux2+K*(L2-1),uy2+K*(W2/2+3.5),.7,AMB,'3,2')
ln(ux2+K*1,uy2+K*W2/2,ux2+K*(L2-1),uy2+K*W2/2,1.3,BLU)
for k in range(8):
    xx=ux2+K*(2.5+k*3.2); s=1 if k%2==0 else -1; ln(xx,uy2+K*W2/2,xx,uy2+K*(W2/2+s*5),1,PUR)
ci(ux2+K*(L2-2),uy2+K*W2/2,3,1.4,GRN,None,'#fff'); ci(ux2-1,uy2+K*W2/2,2.6,1.1,'#555',None,'#eee')
tx(ux2+K*L2/2,uy2-6,'ÜST (kavurma / kuşbaşı)',6.5,'middle','bold',GRY)
dim_h(ux2,ux2+K*L2,uy2+K*W2+14,'27'); dim_v(ux2+K*L2+8,uy2,uy2+K*W2,'21')
# ON
fx2,fy2 = XS+160, YS+50
Z2=lambda c: fy2+K*(H2-c)
rc(fx2,fy2,K*L2,K*H2,1.2,1,'#111',None,SUC)
rc(fx2+K*.3,Z2(H2-4),K*(L2-.6),K*(H2-4-7.3),0,0,'none',None,MAT)
rc(fx2+K*1,Z2(7),K*(L2-2),K*7,1,2,'#111',None,'#fff')
for k in range(1,10): ln(fx2+K*(1+k*2.5),Z2(7),fx2+K*(1+k*2.5),Z2(0),.6,'#999')
ln(fx2+K*1,Z2(11),fx2+K*(L2-1),Z2(11),1.5,PUR)
for k in range(8):
    xx=fx2+K*(2.5+k*3.2); s=1 if k%2==0 else -1; ln(xx,Z2(11),xx,Z2(11+s*5),1,PUR)
rc(fx2+K*(L2-3),Z2(0),K*2,K*1.2,0,0,'none',None,'#fff'); ln(fx2+K*(L2-2),Z2(0),fx2+K*(L2-2),Z2(-5),1.8,GRN)
ci(fx2-1,Z2(3.5),2.6,1.1,'#555',None,'#eee'); rc(fx2-K*4,Z2(7),K*3.4,K*7,1,1,BLU,None,'#dfe7fb'); tx(fx2-K*2.3,Z2(1.6),'M',4.6,'middle','bold',BLU)
tx(fx2+K*L2/2,fy2-6,'ÖN',6.5,'middle','bold',GRY); dim_v(fx2+K*L2+8,fy2,fy2+K*H2,'28'); dim_h(fx2,fx2+K*L2,fy2+K*H2+14,'27')
tx(fx2+K*L2/2,Z2(20),'depo',5,'middle','','#333'); tx(fx2+K*L2/2,Z2(15),'tarak z 11',4.4,'middle','',PUR)
# YAN
sx2,sy2 = XS+270, YS+50
w2=W2/2; vd2=w2-3.5
Zs2=lambda c: sy2+K*(H2-c)
poly([(sx2,Zs2(H2)),(sx2+K*W2,Zs2(H2)),(sx2+K*W2,Zs2(vd2)),(sx2+K*(w2+3.5),Zs2(0)),(sx2+K*(w2-3.5),Zs2(0)),(sx2,Zs2(vd2))],1.2,'#111',SUC)
poly([(sx2+K*.3,Zs2(H2-4)),(sx2+K*W2-K*.3,Zs2(H2-4)),(sx2+K*W2-K*.3,Zs2(vd2)),(sx2+K*(w2+3.5),Zs2(.3)),(sx2+K*(w2-3.5),Zs2(.3)),(sx2+K*.3,Zs2(vd2))],0,'none',MAT)
ci(sx2+K*w2,Zs2(3.5),K*3.5,1.1,'#111',None,'#fff'); ci(sx2+K*w2,Zs2(11),K*5.5,1,PUR,'4,3'); ci(sx2+K*w2,Zs2(11),K*.7,1.1,PUR,None,'#efeaf8')
for a_ in (0,120,240):
    a=math.radians(a_); ln(sx2+K*w2,Zs2(11),sx2+K*w2+K*5.5*math.cos(a),Zs2(11)-K*5.5*math.sin(a),1.2,PUR)
tx(sx2+K*W2/2,sy2-6,'YAN (V kesiti)',6.5,'middle','bold',GRY); dim_h(sx2,sx2+K*W2,sy2+K*H2+14,'21'); dim_v(sx2+K*W2+8,sy2,sy2+K*H2,'28')
tx(sx2+K*2,Zs2(vd2/2+1.5),'45°',5,'start','bold',AMB); tx(sx2+K*w2+K*7,Zs2(11)+3,'tarak Ø11',5,'start','bold',PUR); tx(sx2+K*w2+K*5,Zs2(3.5)+3,'helezon Ø7',5,'start','bold',BLU)
# sucuk varyanti (ayni kabuk): ust + on kucuk
vx,vy = XS+30, YS+195
tx(vx,vy-6,'SUCUK varyantı — aynı kabuk, içi çubuk kanalı + bıçak',6.5,'start','bold',AMB)
rc(vx,vy,K*L2,K*W2,1.2,1,'#111',None,SUC)
for r in range(4):
    for k in range(6): ci(vx+K*(2.5+k*4.4),vy+K*(3+r*5),K*1.9,.6,'#555',None,'#f4ece6')
rc(vx+K*(L2-6),vy+K*(W2/2-4),K*5,K*8,1,1,RED,None,'#fdeeee'); tx(vx+K*(L2-3.5),vy+K*W2/2+1,'bıçak',4,'middle','bold',RED)
ci(vx+K*(L2-2),vy+K*W2/2,3,1.4,GRN,None,'#fff'); ci(vx-1,vy+K*W2/2,2.6,1.1,'#555',None,'#eee')
arr(vx+K*4,vy+K*W2+6,vx+K*(L2-8),vy+K*W2+6,AMB,1); tx(vx+K*L2/2,vy+K*W2+16,'çubuklar eğimli tabanda (8°) bıçağa kayar',4.6,'middle','',AMB)
fx3,fy3 = XS+160, YS+195
Z3=lambda c: fy3+K*(H2-c)
rc(fx3,fy3,K*L2,K*H2,1.2,1,'#111',None,SUC)
for k in range(6): rc(fx3+K*(2+k*4),Z3(H2-1.5),K*2.8,K*25,.7,1,'#555',None,'#f4ece6')
poly([(fx3+K*1,Z3(2)),(fx3+K*(L2-1),Z3(5.5)),(fx3+K*(L2-1),Z3(0)),(fx3+K*1,Z3(0))],.8,AMB,'#fff8ea')
rc(fx3+K*(L2-6),Z3(6.5),K*4,K*3,1,1,RED,None,'#fdeeee'); tx(fx3+K*(L2-4),Z3(9.5),'bıçak',4,'middle','bold',RED)
rc(fx3+K*(L2-3),Z3(0),K*2,K*1.2,0,0,'none',None,'#fff'); ln(fx3+K*(L2-2),Z3(0),fx3+K*(L2-2),Z3(-5),1.8,GRN)
ci(fx3-1,Z3(3.5),2.6,1.1,'#555',None,'#eee'); rc(fx3-K*4,Z3(7),K*3.4,K*7,1,1,BLU,None,'#dfe7fb'); tx(fx3-K*2.3,Z3(1.6),'M',4.6,'middle','bold',BLU)
tx(fx3+K*L2/2,fy3-6,'ÖN — çubuklar Ø4 × 25 dik',6,'middle','bold',GRY)
tx(fx3+K*L2+10,Z3(20),'aynı dişli bıçak',4.8,'start','',BLU); tx(fx3+K*L2+10,Z3(15),'milini çevirir',4.8,'start','',BLU)
tx(fx3+K*L2+10,Z3(8),'3 mm dilim → ağız',4.8,'start','',GRN)
ny2=YS+315
lines2=[('Hacim: %.1f L brüt − V %.1f = %.1f L' % (gS,vS,uS),'#111','bold'),
        ('KUŞBAŞI 3 gün: 3,6 kg (+pay 4 kg = 7,3 L) → kap %55 dolu ✓','#333',''),
        ('KAVURMA 3 gün: 3,0 kg (+pay 3,3 kg = 6 L) → kap %45 dolu ✓','#333',''),
        ('SUCUK hafta: 8,4 kg (+pay 10 kg) = 32 çubuk Ø4×25 → 27×21 tabana 6×4 = 24 ✗','#c0392b','bold'),
        ('  → ya çubuk Ø4×25 × 24 = 7,5 kg (6,2 gün) ya da kap 27×25 (32 çubuk)','#c0392b',''),
        ('  KARAR: küçük kap 27×21×28 kalır, sucuk 24 çubuk + eleman gerekirse 2. kap','#1d7a4f','bold'),
        ('Boş 4 kg · dolu ≤ 12 kg (sucuk) → robot 12 kg kobotla taşır ✓','#333',''),
        ('Tarak Ø11 z 11 · helezon Ø7 × 25 aynı parça (büyük kapla aynı helezon, dişli, motor)','#333',''),
        ('Kavurma/kuşbaşı 3 günde robot değiştirir; donmuş yedek STORE −18 çekmecesi 29 ≥ 28 ✓','#333',''),
        ('Sucuk haftalık: eleman değiştirir (kavurmanın arkasında durur)','#333','')]
for i,(s,c,fw) in enumerate(lines2): tx(XS+14,ny2+i*13.5,s,6.1,'start',fw,c)
tx(XS+14,ny2+145,'Üç malzeme aynı kabukta: sucukta helezon+tarak yerine çubuk kanalı + bıçak takılır; dış ölçü, ray, dişli, dok aynı.',5.6,'start','',GRY)
tx(XS+14,ny2+158,'Kavurma yapışkan: tarak şart · kuşbaşı küp: tarak hafif ama aynı parça · sucuk: tarak yok.',5.6,'start','',GRY)

# ================= YERLEŞİM =================
XP,YP = 980,100
rc(XP,YP,450,560,1.4,4)
tx(XP+14,YP+22,'YERLEŞİM — 70 × 84 · 2 kat · kaplar nerede',10,'start','bold')
KU=2.0
def kat_plan(X,Y,ad,kat):
    tx(X+KU*35,Y-6,ad,7,'middle','bold')
    rc(X,Y,KU*70,KU*84,1.2); rc(X+KU*31,Y,KU*8,KU*84,0,0,'none',None,'#dff3e6')
    # kasar 27x65: x 4-31, y 11-76
    rc(X+KU*4,Y+KU*11,KU*27,KU*65,1.1,1,'#111',None,FILL); ln(X+KU*5,Y+KU*43.5,X+KU*30,Y+KU*43.5,1,BLU); ci(X+KU*29,Y+KU*43.5,2.4,1.2,GRN,None,'#fff')
    tx(X+KU*17.5,Y+KU*30,'KAŞAR',5.6,'middle','bold'); tx(X+KU*17.5,Y+KU*36,'A' if kat==1 else 'B',5.6,'middle','bold'); tx(X+KU*17.5,Y+KU*58,'27×65×48',4.4,'middle','','#333'); tx(X+KU*17.5,Y+KU*64,'23 kg · 3,5 g',4.2,'middle','','#333')
    rc(X,Y+KU*40,KU*4,KU*7,1,1,BLU,None,'#dfe7fb')
    # sag: on kucuk kap y 55-76, arka y 32-53
    fr,bk = (('KAVURMA','3 gün · robot'),('SUCUK','hafta · eleman')) if kat==1 else (('KUŞBAŞI','3 gün · robot'),('kuş. yedek','çözülme'))
    rc(X+KU*39,Y+KU*55,KU*27,KU*21,1.1,1,'#111',None,SUC); ln(X+KU*40,Y+KU*65.5,X+KU*65,Y+KU*65.5,1,BLU); ci(X+KU*41,Y+KU*65.5,2.4,1.2,GRN,None,'#fff')
    tx(X+KU*52.5,Y+KU*63,fr[0],5.2,'middle','bold'); tx(X+KU*52.5,Y+KU*69.5,fr[1],4,'middle','','#333')
    lt = 'yedek' in bk[0]
    rc(X+KU*39,Y+KU*32,KU*27,KU*21,1 if not lt else .8,1,'#111' if not lt else '#999','3,2' if lt else None,SUC if not lt else LIGHT)
    if not lt: ln(X+KU*40,Y+KU*42.5,X+KU*65,Y+KU*42.5,1,BLU); ci(X+KU*41,Y+KU*42.5,2.4,1.2,GRN,None,'#fff')
    tx(X+KU*52.5,Y+KU*40,bk[0],5.2,'middle','bold','#999' if lt else '#111'); tx(X+KU*52.5,Y+KU*46.5,bk[1],4,'middle','','#999' if lt else '#333')
    rc(X+KU*66,Y+KU*62,KU*4,KU*7,1,1,BLU,None,'#dfe7fb'); rc(X+KU*66,Y+KU*39,KU*4,KU*7,1,1,BLU,None,'#dfe7fb')
    for (ox,oy) in ((31,43.5),(39,65.5)) + (((39,42.5),) if not lt else ()): ci(X+KU*ox,Y+KU*oy,KU*31,.7,GRN,'4,3')
    rc(X,Y+KU*79,KU*70,KU*3,1,0,BLU,None,'#dfe7fb'); tx(X+KU*35,Y+KU*81.3,'klape',4,'middle','',BLU)
    rc(X,Y,KU*70,KU*11,0,0,'none',None,'#eeeeee'); tx(X+KU*35,Y+KU*7,'hava + kablo kanalı 11',4,'middle','',GRY)
kat_plan(XP+20,YP+48,'KAT 1 — sucuklu & kavurmalı düzlem',1)
kat_plan(XP+250,YP+48,'KAT 2 — kuşbaşılı & kaşarlı düzlem',2)
ny3=YP+232
for i,(s,c) in enumerate([('Ağızlar: kaşar (31, 43,5) · ön küçük (39, 65,5) · arka küçük (39, 42,5) → hepsi bantta, y ≥ 31 ✓',GRN),
                          ('Kat 1: sucuklu pide (sucuk + kaşar A), kavurmalı (kavurma + kaşar A) · Kat 2: kuşbaşılı (kuşbaşı + kaşar B), kaşarlı (kaşar B)',BLU),
                          ('→ iki kaşar kabı dengeli tükenir (~2,9 kg/gün her biri) → 23 kg = 8 gün ≥ hafta',BLU),
                          ('Robot yalnız ÖNDEKİ küçük kapları değiştirir (kavurma kat 1, kuşbaşı kat 2) — 3 günde 1, dolu ≤ 12 kg',GRN),
                          ('Sucuk kavurmanın ARKASINDA: haftalık, eleman kavurmayı çekip değiştirir; kat 2 arka: kuşbaşı yedeği çözülür',GRY),
                          ('Dikey: teknik 27 · kat 1 51 · boşluk 14 · kat 2 51 · boşluk 14 · alt 40 = 197 ✓ · tepsi düzlemleri 107 / 42 cm',GRY),
                          ('Derinlik: kanal 11 + kaşar 65 + klape 3 + pay 5 = 84 ✓ · küçük kaplar 32-53 / 55-76',GRY)]):
    tx(XP+14,ny3+i*13.5,s,5.8,'start','bold' if i in (0,3) else '',c)
# on kesit mini
KM=1.35
mx,my = XP+30, YP+340
Zm=[('teknik',27,'#f3f3f3'),('KAT 1',51,'#fff'),('B1',14,'#eef3ff'),('KAT 2',51,'#fff'),('B2',14,'#eef3ff'),('ALT',40,'#f7f6f2')]
rc(mx,my,KM*70,KM*197,1.4); zz=0
for ad,h,col in Zm:
    rc(mx,my+KM*zz,KM*70,KM*h,.6,0,'#111',None,col); tx(mx+KM*70+4,my+KM*(zz+h/2)+2,'%s %g'%(ad,h),4.6,'start','',GRY); zz+=h
for z0 in (27,92):
    rc(mx+KM*4,my+KM*(z0+2),KM*27,KM*48,.9,1,'#111',None,FILL); tx(mx+KM*17.5,my+KM*(z0+27),'KAŞAR',4.4,'middle','bold')
    rc(mx+KM*39,my+KM*(z0+22),KM*27,KM*28,.9,1,'#111',None,SUC); tx(mx+KM*52.5,my+KM*(z0+37),'küçük',4.4,'middle','bold')
    for xx in (31,39): ln(mx+KM*xx,my+KM*(z0+51),mx+KM*xx,my+KM*(z0+55),1.4,GRN)
    el(mx+KM*35,my+KM*(z0+61),KM*17,KM*1.2,.9,BLU,None,'#dfe7fb')
tx(mx+KM*35,my+KM*197+10,'ÖN KESİT 1:7,4',5,'middle','bold',GRY)
tx(mx+KM*70+60,my+KM*60,'küçük kaplar (28) kaşarla',4.8,'start','','#333'); tx(mx+KM*70+60,my+KM*68,'aynı tabanda, üstü boş',4.8,'start','','#333')
tx(mx+KM*70+60,my+KM*100,'ALT 40: boş küçük kap',4.8,'start','','#333'); tx(mx+KM*70+60,my+KM*108,'parkı ×2 + elektrik',4.8,'start','','#333')
tx(mx+KM*70+60,my+KM*140,'tepsi düzlemi 2 = 42 cm',4.8,'start','bold',AMB); tx(mx+KM*70+60,my+KM*148,'(kobot alçak erişim — kontrol)',4.6,'start','',AMB)

# ================= TABLO + KARAR =================
YT=690
rc(40,YT,1390,460,1.6,4)
tx(56,YT+24,'DÖRT MALZEME — KAP · KG · GÜN · KİM DEĞİŞTİRİR',12,'start','bold')
hdr=['malzeme','kap (L×W×H)','kap hacmi','dolum','gün','porsiyon / pide','günlük','raf ömrü (+3)','içinde','değiştiren']
cx_=[56,190,330,430,500,560,720,800,910,1120]
for i,h in enumerate(hdr): tx(cx_[i],YT+50,h,7,'start','bold',GRY)
ln(54,YT+56,1414,YT+56,.8,'#bbb')
rows=[('KAŞAR ×2','BÜYÜK 27×65×48','56 L','23 kg','3,5 (×2 kap = 8)','120 / 80 / 60 / 40 g','6,1 kg','14 gün','tarak + helezon','eleman haftalık (rayda doldurur)'),
      ('SUCUK ×1 (+1)','KÜÇÜK 27×21×28','13 L','24 çubuk 7,5 kg','6,2 (hafta)','50 g (10 dilim)','1,2 kg','7 gün','çubuk kanalı + bıçak','eleman haftalık'),
      ('KAVURMA ×4','KÜÇÜK 27×21×28','13 L','3,3 kg (%45)','3','60 g','1,0 kg','3-4 gün (pişmiş)','tarak + helezon','robot 3 günde (STORE −18 → çözülme → ön)'),
      ('KUŞBAŞI ×4','KÜÇÜK 27×21×28','13 L','4 kg (%55)','3','100 g','1,2 kg','2-3 gün (çiğ)','tarak + helezon','robot 3 günde (aynı)')]
for i,r in enumerate(rows):
    yy=YT+74+i*20
    for j,v in enumerate(r): tx(cx_[j],yy,v,6.6,'start','bold' if j==0 else '','#111' if j==0 else '#333')
ln(54,YT+160,1414,YT+160,.8,'#bbb')
notes=[('Kabuller: 80 pide/gün · karışım kaşarlı %25 · sucuklu %30 · kavurmalı %20 · kuşbaşılı %15 (kıyma yok) · kaşar porsiyonu pide türüne göre 120/80/60/40 g',GRY,''),
       ('Her kapta hareketli parça: (1) TARAK = pimli mil, boydan boya, V ağzında, 3 dev/dk — köprü kırıcı (bridge breaker) · (2) DOZAJ HELEZONU = Ø7 × 25 altta, 30 dev/dk — gramajlı iter · sucukta (1)(2) yerine bıçak',BLU,'bold'),
       ('Gram: helezon turu sayılır + ray altındaki yük hücresi kabı tartar → ±3 g. Tahrik: kabın dış ucundaki dişli, kap raya oturunca duvardaki 40 W motora yandan meshler. Kapta elektrik yok.',BLU,''),
       ('Kaşar neden büyük: 3 günde 18 kg → 45 L; küçük kap 13 L. Kaşar için 27×65×48 (V 29 derin, tek helezon yeter). Daha büyük istersen çift helezonlu 27×78 (v17, 31 kg) hazır.',GRN,'bold'),
       ('Sucuk: 27×21 tabana 24 çubuk sığıyor (7,5 kg = 6,2 gün). Tam 7 gün için ya çubuk Ø3,8 (32 adet) ya da 2. kap arkada — eleman haftalık zaten geliyor; 6,2 gün + 2. kap = sorun yok.',AMB,''),
       ('Kavurma/kuşbaşı 3 günlük kapta %45-55 dolu: küçük kap sucuk ölçüsüne göre; boş hacim zarar değil, tarak küçük yığını da besler. Aynı kap = aynı yedek parça, aynı dok, aynı ray, aynı STORE çekmecesi (28 ≤ 29).',GRN,''),
       ('Bütün istasyon: 2 büyük + 4 küçük pozisyon (kat 1: kaşar A, kavurma önde, sucuk arkada · kat 2: kaşar B, kuşbaşı önde, yedek arkada). Robot 2 kabı değiştirir (kavurma, kuşbaşı), eleman 3 kabı doldurur.',GRN,'bold'),
       ('AÇIK: rendelenmiş kaşar 45° V + tek tarakla akış prototipi (olmazsa 2. tarak z 30) · kat 2 tepsi düzlemi 42 cm · klape contası · HAT v45 TOPPING bloğu bu kurguyla',AMB,'')]
for i,(s,c,fw) in enumerate(notes): tx(56,YT+180+i*20,s,6.6,'start',fw,c)
tx(56,YT+345,'Cevap: EVET — her kabın içinde komple boyda dönen tek tarak (tel değil pimli mil; tel de olur, pimli mil kavurmada daha güvenli) + en altta gramajla iten helezon. Kaşar daha büyük hazne ister: 27×65×48. Sucuk/kavurma/kuşbaşı tek ölçü: 27×21×28.',7.2,'start','bold','#111')
tx(56,YT+362,'Bunlar v16/v17 ölçülerinin yerini alır (kaşar 27×38 ve 27×78 iptal). Yerleşim aynı papyon mantığı, 2 kat, 2 düzlem; dikey 197 ✓.',7,'start','','#333')
tx(W-40,H-12,'AUTOKITCH · arastirma/3_TOPPING/ist3_topping_detay_v18 · 5 Eyl 2026',7,'end','',GRY)
o.append('</svg>')
svg = chr(10).join(o)
xml.dom.minidom.parseString(svg.encode('utf-8'))
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\ist3_topping_detay_v18.svg"
io.open(out,'w',encoding='utf-8').write(svg)
print('yazildi + XML gecerli | buyuk %.0f-%.0f=%.0f L → %.0f kg | kucuk %.1f-%.1f=%.1f L' % (gB,vB,uB,uB*0.41,gS,vS,uS))
