# -*- coding: utf-8 -*-
# OVEN v5 (6 Eyl 2026) — Kemal: 1 kap olsun, 2'ye gerek yok · v4 — Kemal: pompa arka duvarda, sağda solda 2 STANDART KAP (yağ versiyonu, helezon/tarak yok), biri bitince diğeri;
# sprey ortada önde (az yer); havalandırma/filtre şart mı, baca, koku; KESME presi PACK'ten OVEN'e (pres + 4 bölen bıçak, tepsi zemine dayanır, motor hesabı);
# "her şeyi hesaplamadan büyük büyük koydun" → zonlar hesapla küçültüldü.
import io, math, xml.dom.minidom
W, H = 1460, 925
o = []
AP = chr(39)
def esc(s): return str(s).replace('&','&amp;').replace('<','&lt;')
def ln(x1,y1,x2,y2,w=1,c='#111',d=None):
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s stroke-linecap="round"/>' % (x1,y1,x2,y2,c,w,(' stroke-dasharray="%s"'%d) if d else ''))
def rc(x,y,w,h,sw=1,r=0,c='#111',d=None,f='none'):
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,w,h,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def ci(x,y,r,sw=1,c='#111',d=None,f='none'):
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def el(cx,cy,rx,ry,sw=1,c='#111',d=None,f='none'):
    o.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (cx,cy,rx,ry,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def tx(x,y,s,fs=9,anc='start',fw='',col='#111'):
    o.append('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="%s" font-weight="%s" fill="%s" font-family="Segoe UI, Arial, sans-serif">%s</text>' % (x,y,fs,anc,fw or 'normal',col,esc(s)))
def poly(pts,sw=1,c='#111',f='none',d=None,op=1):
    o.append('<polygon points="%s" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="%s"%s stroke-linejoin="round"/>' % (' '.join('%.1f,%.1f'%p for p in pts),f,op,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def arr(x1,y1,x2,y2,c='#c0392b',w=1.3):
    ln(x1,y1,x2,y2,w,c); a=math.atan2(y2-y1,x2-x1)
    for s in (1,-1): ln(x2,y2,x2-7*math.cos(a-s*.42),y2-7*math.sin(a-s*.42),w,c)
def dim(x1,y1,x2,y2,s,fs=5.6,off=0,col='#111'):
    ln(x1,y1,x2,y2,.7,col)
    for (x,y) in ((x1,y1),(x2,y2)):
        if abs(y2-y1)<abs(x2-x1): ln(x,y-3,x,y+3,.7,col)
        else: ln(x-3,y,x+3,y,.7,col)
    if abs(y2-y1)<abs(x2-x1): tx((x1+x2)/2,y1-3+off,s,fs,'middle','bold',col)
    else: tx(x1+4+off,(y1+y2)/2+2,s,fs,'start','bold',col)
def para(x,y,s,maxc,fs=5.9,col='#333',fw='',lh=None):
    lh = lh or fs*1.6; cur=''; lines=[]
    for wd in s.split(' '):
        if cur and len(cur)+1+len(wd) > maxc: lines.append(cur); cur=wd
        else: cur = (cur+' '+wd) if cur else wd
    if cur: lines.append(cur)
    for l in lines: tx(x,y,l,fs,'start',fw,col); y += lh
    return y
def hatch(x,y,w,h,step=4,c='#999'):
    rc(x,y,w,h,.6,0,c,None,'#f3f0e6')
    k=0
    while k < w+h:
        x1=x+max(0,k-h); y1=y+min(k,h); x2=x+min(k,w); y2=y+max(0,k-w)
        ln(x1,y1,x2,y2,.4,c); k+=step
def f1(v): return ('%.1f' % v).replace('.',',')

GRN, RED, BLU, GRY, AMB, PUR, GOLD, ICE = '#1d7a4f', '#c0392b', '#1a49b8', '#666', '#b7791f', '#6b4fa8', '#c9a227', '#e3f2fb'
# ---------------- ölçüler (cm, zeminden) ----------------
COL_W, COL_D, COL_H = 70.0, 84.0, 197.0
OV_W, OV_D, OV_H = 64.0, 60.0, 56.0
Z = {'plint':(0,12),'pano':(12,32),'kesme':(32,82),'yag':(82,112),'firin':(112,168),'plenum':(168,180),'filtre':(180,185),'ust':(185,197)}
TEPSI = (117,145)
KAP_L = 12.0; KAP_MAX = 12.0; DOZ = 4.0; PIDE = 100
LT_GUN = DOZ*PIDE/1000; GUN_KAP = KAP_L/LT_GUN; GUN_MAX = KAP_MAX/LT_GUN
KAP_KG = KAP_L*0.9+3.3
# kesme
BLADE_L = 28.0; N_BLADE = 2; F_CM = (15.0, 20.0); F_KN = tuple(BLADE_L*N_BLADE*f/1000 for f in F_CM)
ACT_N, ACT_STROKE, ACT_V = 1500, 100, 10
T_CUT = 2*ACT_STROKE/ACT_V*0.6   # 60 mm gerçek yol (44 → 34 + pay)

o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H))
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,40,'AUTOKITCH — OVEN v5 (6 Eyl 2026) — Omake 2 kat · 1 STANDART YAĞ KABI (sol) + pompa arka duvarda + sprey ORTADA · KESME PRESİ (PACK'+AP+'ten taşındı) · fan şart, filtre opsiyon, baca yok · zonlar hesapla küçüldü',14,'start','bold')
tx(30,62,'Kemal: "1 kap olsun, 2'+AP+'ye gerek yok · pompa arka duvarda, standart kartuş (helezonsuz) · bir kap kaç gün? · yağ sıcak mı olmalı, ısıtıcı niye? · sprey önde, az yer kaplasın · havalandırma/filtre şart mı, koku, baca, elektrikli · kesmeyi bu istasyona koy: pres + 4 bölen bıçak, tepsi zemine, motor hesabı · büyük büyük koydun"',9,'start','','#444')
ln(30,74,W-30,74,.8,'#999')

# ================= A · KOLON ÖNDEN =================
XA,YA,WA,HA_ = 40,90,340,640
rc(XA,YA,WA,HA_,1.4,4,'#111',None,'#fcfdff')
tx(XA+14,YA+22,'A · OVEN KOLONU 70 × 197 — önden (zeminden yukarı)',10,'start','bold')
K=2.6; cx0=XA+46; cz0=YA+48+K*COL_H
X=lambda c: cx0+K*c; Zf=lambda z: cz0-K*z
rc(X(0),Zf(COL_H),K*COL_W,K*COL_H,1.4,2,'#111',None,'#fff')
for xs_ in (0,COL_W-3):
    hatch(X(xs_),Zf(Z['filtre'][1]),K*2,K*(Z['filtre'][1]-Z['yag'][0]),4,'#b08968'); rc(X(xs_+2),Zf(Z['filtre'][1]),K*1,K*(Z['filtre'][1]-Z['yag'][0]),.5,0,'#7fb3d5',None,'#eef6fb')
zones=[('plint','#e9e4d6','plint 12: hava girişi ızgarası'),('pano','#e3f2fb','PANO 20: PLC · 2 menteşe + 1 pres sürücüsü · 2 SSR · pompa rölesi · 24 V'),('kesme','#f4eef8',''),('yag','#fff8e0',''),('firin','#fff',''),('plenum','#fde9c9','PLENUM 12 + FAN Ø120 (şart)'),('filtre','#eef3f8','karbon filtre 5 (opsiyon)'),('ust','#f7f7f7','üst boşluk 12 (yedek)')]
for key,col,lab in zones:
    z0,z1=Z[key]; rc(X(3),Zf(z1),K*(COL_W-6),K*(z1-z0),.7,0,'#555',None,col)
    if lab: tx(X(COL_W/2),Zf((z0+z1)/2)+2,lab,4.5,'middle','bold' if key in ('plenum','pano') else '','#333')
# fırın
z0,z1=Z['firin']
rc(X(3),Zf(z1),K*OV_W,K*OV_H,1.3,2,'#111',None,'#f4f4f4')
for (zk0,zk1,nm,tp) in ((z0,z0+28,'KAPAK 1 (alt kat)',TEPSI[0]),(z0+28,z1,'KAPAK 2 (üst kat)',TEPSI[1])):
    rc(X(6.5),Zf(zk1-4),K*57,K*(zk1-zk0-8),1.1,1,'#333',None,'#dbeeff')
    rc(X(6.5),Zf(zk0+4)+K*1.2,K*57,K*1.2,.8,0,'#333',None,'#999')
    tx(X(35),Zf((zk0+zk1)/2)+2,nm+' · hazne 40×40×10 · tepsi düzlemi %d' % tp,4.6,'middle','bold','#333')
    rc(X(67.2),Zf(zk0+7),K*2.4,K*6,1,1,RED,None,'#f7d7d7')
ln(X(69.6),Zf(z0+10),X(COL_W)+30,Zf(z0+10),.6,RED); tx(X(COL_W)+32,Zf(z0+10)+2,'menteşe motoru ×2 (Ø28)',3.9,'start','',RED)
# YAĞ + SPREY zonu: 2 kap yanlarda, tepsi ortada, nozül üstte
zy0,zy1=Z['yag']
rc(X(52.5),Zf(zy0+2+24),K*14,K*24,.8,1,'#999','4,3','none'); tx(X(59.5),Zf(zy0+13)+2,'boş 15',4,'middle','','#999')
for x0_ in (3.5,):
    rc(X(x0_),Zf(zy0+2+24),K*14,K*24,1.1,1,GOLD,None,'#dbeeff')
    rc(X(x0_+0.5),Zf(zy0+2+18),K*13,K*17,0,0,'none',None,'#f6d76b')
    for dx_ in (2,12): rc(X(x0_+dx_-1.5),Zf(zy0+2),K*3,K*2,.6,0,'#555',None,'#d0d7de')
    ln(X(x0_-0.5),Zf(zy0),X(x0_+14.5),Zf(zy0),1.2,'#555')
    tx(X(x0_+7),Zf(zy0+13)+2,'YAĞ KABI',4.4,'middle','bold','#8a6a3a'); tx(X(x0_+7),Zf(zy0+9)+2,'14×68×24',3.8,'middle','','#8a6a3a'); tx(X(x0_+7),Zf(zy0+5.5)+2,'%d L' % KAP_L,3.8,'middle','','#8a6a3a')
ci(X(35),Zf(zy1-6),3,1,GOLD,None,'#fff8e0'); poly([(X(35),Zf(zy1-6)),(X(20),Zf(zy0+8)),(X(50),Zf(zy0+8))],.6,GOLD,'#fff3c4',None,.5)
el(X(35),Zf(zy0+8),K*16,K*1.5,1.4,BLU); rc(X(19),Zf(zy0+1.5),K*32,K*1.5,.6,0,'#555',None,'#ccc')
tx(X(35),Zf(zy1-2)+2,'YAĞ + SPREY 30 · kap 15 | tepsi 34 | boş 15 · klape 4 · sıcak dolap 42 °C',4.3,'middle','bold',AMB)
tx(X(35),Zf(zy0+4.5)+2,'damlalık tavası',3.4,'middle','','#555'); tx(X(35),Zf(zy0+11)+2,'tepsi Ø32 (pay 1)',3.6,'middle','',BLU)
# KESME zonu
zk0_,zk1_=Z['kesme']
rc(X(12),Zf(zk0_+2),K*46,K*2,1,0,'#333',None,'#bbb'); tx(X(35),Zf(zk0_-1.5)+2,'zemin plakası + halka Ø33 (tepsi oturur)',3.4,'middle','','#555')
el(X(35),Zf(zk0_+4),K*16,K*1.5,1.4,BLU)
o.append('<path d="M %.1f %.1f A %.1f %.1f 0 0 1 %.1f %.1f Z" fill="#f0d9a8" stroke="#8a6a3a" stroke-width="0.8"/>' % (X(20),Zf(zk0_+4),K*15,K*4,X(50),Zf(zk0_+4)))
rc(X(21),Zf(zk0_+16),K*28,K*4,1,0,'#333',None,'#e8e8e8'); ln(X(21),Zf(zk0_+12),X(49),Zf(zk0_+12),1.4,'#111')
rc(X(32),Zf(zk0_+19),K*6,K*3,.8,1,'#333',None,'#ccc'); rc(X(17),Zf(zk0_+22),K*36,K*3,1,0,'#333',None,'#ddd')
for xg in (19,51): ln(X(xg),Zf(zk0_+2),X(xg),Zf(zk0_+40),1.6,'#555'); rc(X(xg-1.2),Zf(zk0_+22),K*2.4,K*3,.6,0,'#333',None,'#999')
rc(X(31),Zf(zk0_+46),K*8,K*21,1.2,2,PUR,None,'#ece6f5'); ln(X(35),Zf(zk0_+22),X(35),Zf(zk0_+25),2,PUR)
tx(X(40.5),Zf(zk0_+42)+2,'AKTÜATÖR',4.2,'start','bold',PUR); tx(X(40.5),Zf(zk0_+38)+2,'24 V · %d N' % ACT_N,3.6,'start','',PUR); tx(X(40.5),Zf(zk0_+34)+2,'strok %d mm' % ACT_STROKE,3.6,'start','',PUR); tx(X(40.5),Zf(zk0_+30)+2,'kendini kilitler',3.6,'start','',PUR)
arr(X(56),Zf(zk0_+16),X(56),Zf(zk0_+6),PUR,1); tx(X(58),Zf(zk0_+11)+2,'iniş 10',3.4,'start','',PUR)
tx(X(35),Zf(zk1_-2)+2,'KESME 50 · bıçak yıldızı + (2 × 28) · tepsi zemine dayanır',4.3,'middle','bold',PUR)
tx(X(10),Zf(zk0_+14)+2,'bıçak',3.4,'end','','#333'); tx(X(10),Zf(zk0_+23)+2,'kızak',3.4,'end','','#333'); tx(X(10),Zf(zk0_+5)+2,'pide',3.4,'end','','#8a6a3a')
# hava
arr(X(1.5),Zf(6),X(1.5),Zf(40),'#7fb3d5',1.1); arr(X(COL_W-1.5),Zf(6),X(COL_W-1.5),Zf(40),'#7fb3d5',1.1)
arr(X(58),Zf(Z['filtre'][1]+1),X(58),Zf(COL_H-1),'#7fb3d5',1.3); tx(X(60),Zf(COL_H-4),'egzoz → mekân',3.6,'start','',BLU)
ci(X(60),Zf(174),K*5,1,'#333',None,'#fff'); tx(X(60),Zf(174)+1.5,'FAN',3.6,'middle','bold')
for key,lab in (('plint','12'),('pano','20'),('kesme','50'),('yag','30'),('firin','56'),('plenum','12'),('filtre','5'),('ust','12')):
    z0,z1=Z[key]; dim(X(COL_W)+14,Zf(z1),X(COL_W)+14,Zf(z0),lab,4.6,0,GRY)
dim(X(0),Zf(COL_H)-14,X(COL_W),Zf(COL_H)-14,'70 = 3 + 64 + 3',5.2)
para(XA+14,YA+572,'Zonlar (zeminden): plint 12 · pano 20 · KESME 50 · YAĞ+SPREY 30 · fırın 56 · plenum+fan 12 · filtre 5 · yedek 12 = 197. v3'+AP+'e göre: plenum 26 + filtre 15 + üst 10 = 51 → 17; pano 30 → 20; niş 18 kalktı (sprey kapların arasında); kartuş yuvası 30 → yağ+sprey 30. Kazanılan 50 cm = KESME.',72,5.2,'#333')

# ================= B · YAN KESİT =================
XB,YB,WB,HB = 400,90,400,640
rc(XB,YB,WB,HB,1.4,4,'#111',None,'#fcfbf8')
tx(XB+14,YB+22,'B · YAN KESİT 84 × 197 — kap 68 + pompa arkada · sprey ortada · pres',10,'start','bold')
bx=XB+95; bz=YA+48+K*COL_H
XS=lambda d: bx+K*d; ZS=lambda z: bz-K*z
rc(XS(0),ZS(COL_H),K*COL_D,K*COL_H,1.4,2,'#111',None,'#fff')
hatch(XS(COL_D-2),ZS(COL_H-1),K*2,K*(COL_H-2),4,'#b08968')
for key,col in (('plint','#e9e4d6'),('pano','#e3f2fb'),('kesme','#f4eef8'),('yag','#fff8e0'),('plenum','#fde9c9'),('filtre','#eef3f8'),('ust','#f7f7f7')):
    z0,z1=Z[key]; rc(XS(2),ZS(z1),K*(COL_D-4),K*(z1-z0),.6,0,'#555',None,col)
# arka kanal (fırın arkası)
rc(XS(OV_D+2),ZS(Z['plenum'][0]),K*(COL_D-OV_D-4),K*OV_H,.6,0,'#7fb3d5',None,'#eef6fb')
for i,t in enumerate(('arka','kanal 20','hava+kablo','+buhar')): tx(XS(OV_D+12),ZS(150-4*i)+2,t,3.5,'middle','',BLU)
# fırın
z0,z1=Z['firin']
rc(XS(2),ZS(z1),K*OV_D,K*OV_H,1.3,2,'#111',None,'#f4f4f4'); tx(XS(32),ZS(z0+50)+2,'OMAKE 64×60×56',4.6,'middle','bold','#333')
for (zk0,zk1,tp) in ((z0,z0+28,TEPSI[0]),(z0+28,z1,TEPSI[1])):
    rc(XS(6),ZS(zk0+9),K*40,K*1.5,.8,0,'#777',None,'#ccc'); tx(XS(26),ZS(zk0+6)+2,'taş 40 · tepsi Ø32 + kulp 6 = 38',3.8,'middle','','#555')
    rc(XS(2),ZS(zk1-4),K*1.2,K*(zk1-zk0-8),1,0,'#333',None,'#dbeeff')
    ln(XS(2),ZS(zk0+4),XS(2)-K*20,ZS(zk0+4),1,'#333','3,2'); ci(XS(2),ZS(zk0+4),1.8,1,RED,None,RED)
arr(XS(OV_D+3),ZS(z0+30),XS(OV_D+12),ZS(Z['plenum'][0]+3),RED,1.1)
ci(XS(30),ZS(174),K*5,1,'#333',None,'#fff'); tx(XS(30),ZS(174)+1.5,'FAN',3.6,'middle','bold')
rc(XS(42),ZS(184.5),K*30,K*4,.8,1,'#333',None,'#dfe7fb'); tx(XS(57),ZS(182)+1.5,'karbon 40×40×5 (opsiyon)',3.3,'middle','','#333')
arr(XS(57),ZS(185.5),XS(57),ZS(COL_H-1),RED,1.2); tx(XS(57)+6,ZS(COL_H-4),'üst ızgara → mekâna (bacasız)',3.6,'start','',RED)
# YAĞ + SPREY (yandan): kap 68 önde, kuru bağlantı + pompa arkada, nozül d 20, tepsi d 4-36
zy0,zy1=Z['yag']
rc(XS(2),ZS(zy1-0.5),K*1.2,K*29,1,0,BLU,None,'#dfe7fb'); tx(XS(2)-K*5,ZS(zy0+15)+2,'klape 4',3.6,'middle','',BLU)
rc(XS(4),ZS(zy0+2+24),K*68,K*24,1,1,GOLD,'4,3','#fdf6dc')
tx(XS(55),ZS(zy0+24)+2,'YAĞ KABI 68 (solda, kesit dışı)',3.8,'middle','bold','#8a6a3a'); tx(XS(55),ZS(zy0+20)+2,'kapaklı · dolum ağzı önde',3.4,'middle','','#8a6a3a')
rc(XS(72),ZS(zy0+6),K*3,K*3,1,0,GRN,None,'#eaf6ee'); tx(XS(73.5),ZS(zy0+2)+2,'kuru bağl.',3.1,'middle','',GRN)
rc(XS(76),ZS(zy0+18),K*6,K*10,1,1,'#333',None,'#eee'); tx(XS(79),ZS(zy0+14)+2,'POMPA',3.4,'middle','bold'); tx(XS(79),ZS(zy0+10.5)+2,'24 V',3,'middle','','#555')
ln(XS(79),ZS(zy0+18),XS(79),ZS(zy1-3),1,GOLD); ln(XS(79),ZS(zy1-3),XS(20),ZS(zy1-3),1,GOLD); ln(XS(20),ZS(zy1-3),XS(20),ZS(zy1-6),1,GOLD)
ci(XS(20),ZS(zy1-6),3,1,GOLD,None,'#fff8e0'); poly([(XS(20),ZS(zy1-6)),(XS(5),ZS(zy0+8)),(XS(35),ZS(zy0+8))],.6,GOLD,'#fff3c4',None,.5)
el(XS(20),ZS(zy0+8),K*16,K*1.5,1.4,BLU); ln(XS(2)-K*22,ZS(zy0+8),XS(4),ZS(zy0+8),2,'#999')
tx(XS(2)-K*12,ZS(zy0+11)+2,'robot: sok 1 sn çek',3.4,'middle','',AMB)
tx(XS(20),ZS(zy1-1.5)+2,'nozül d 20 · tepsi 4–36 · 15 üstte → Ø30',3.4,'middle','',AMB)
rc(XS(4),ZS(zy0+1.5),K*45,K*1.5,.6,0,'#555',None,'#ccc')
# KESME (yandan)
zk0_,zk1_=Z['kesme']
rc(XS(5),ZS(zk0_+2),K*40,K*2,1,0,'#333',None,'#bbb'); el(XS(20),ZS(zk0_+4),K*16,K*1.5,1.4,BLU)
o.append('<path d="M %.1f %.1f A %.1f %.1f 0 0 1 %.1f %.1f Z" fill="#f0d9a8" stroke="#8a6a3a" stroke-width="0.8"/>' % (XS(5),ZS(zk0_+4),K*15,K*4,XS(35),ZS(zk0_+4)))
rc(XS(6),ZS(zk0_+16),K*28,K*4,1,0,'#333',None,'#e8e8e8'); ln(XS(6),ZS(zk0_+12),XS(34),ZS(zk0_+12),1.4,'#111')
rc(XS(17),ZS(zk0_+19),K*6,K*3,.8,1,'#333',None,'#ccc'); rc(XS(2),ZS(zk0_+22),K*36,K*3,1,0,'#333',None,'#ddd')
for dg in (4,36): ln(XS(dg),ZS(zk0_+2),XS(dg),ZS(zk0_+40),1.6,'#555')
rc(XS(16),ZS(zk0_+46),K*8,K*21,1.2,2,PUR,None,'#ece6f5'); ln(XS(20),ZS(zk0_+22),XS(20),ZS(zk0_+25),2,PUR)
tx(XS(25.5),ZS(zk0_+40)+2,'AKTÜATÖR',4,'start','bold',PUR); tx(XS(25.5),ZS(zk0_+36)+2,'dikey',3.2,'start','',PUR); tx(XS(25.5),ZS(zk0_+32.5)+2,'kendini kilitler',3.2,'start','',PUR)
ln(XS(2)-K*22,ZS(zk0_+4),XS(4),ZS(zk0_+4),2,'#999'); tx(XS(2)-K*12,ZS(zk0_+7.5)+2,'robot kulpu tutar',3.4,'middle','',PUR)
tx(XS(60),ZS(zk0_+30)+2,'arka: pano kabloları',3.4,'middle','','#777')
tx(XS(30),ZS(Z['pano'][0]+10)+2,'PANO 20 (servis kapağı önde)',4.2,'middle','bold',BLU)
arr(XS(20),ZS(1),XS(20),ZS(11),'#7fb3d5',1.1); tx(XS(24),ZS(5)+2,'plint ızgarası: hava girişi',3.6,'start','',BLU)
dim(XS(0),ZS(COL_H)-14,XS(OV_D+2),ZS(COL_H)-14,'fırın 60',4.8,0,GRY); dim(XS(OV_D+2),ZS(COL_H)-14,XS(COL_D),ZS(COL_H)-14,'arka 24 (84)',4.8,0,GRY)
tx(XS(0)-4,ZS(60)+2,'ÖN',4.6,'end','bold',GRY); tx(XS(COL_D)+4,ZS(60)+2,'ARKA',4.6,'start','bold',GRY)
para(XB+14,YB+572,'Yağ zonu kapalı sıcak dolaptır (42 °C, 100 W ısıtıcı + termostat, üstteki fırın da ısıtır): kap içindeki sadeyağ akışkan kalır, hat ısıtması gerekmez. Tek kap solda, pompa arka duvarda kuru bağlantının hemen arkasında; şamandıra 4 gün kala BEYİN'+AP+'e "yağ az" der. Tepsi kabın yanına 40 cm girer, nozül 20 derinlikte.',80,5.2,'#333')

# ================= C · STANDART KAP — YAĞ VERSİYONU =================
XC,YC,WC,HC = 820,90,300,320
rc(XC,YC,WC,HC,1.4,4,'#111',None,'#fff')
tx(XC+14,YC+22,'C · STANDART KAP — YAĞ VERSİYONU (14×68×24)',10,'start','bold')
KC=3.2; kx=XC+30; kz=YC+195
XK=lambda d: kx+KC*d; ZK=lambda z: kz-KC*z
rc(XK(0),ZK(24),KC*68,KC*24,1.2,2,GOLD,None,'#dbeeff'); rc(XK(0.5),ZK(18),KC*67,KC*17.5,0,0,'none',None,'#f6d76b')
ln(XK(0.5),ZK(18),XK(67.5),ZK(18),.7,'#8a6a3a','3,2'); tx(XK(34),ZK(19.5),'dolum çizgisi %d L' % KAP_L,3.8,'middle','','#8a6a3a')
rc(XK(0),ZK(25.5),KC*68,KC*1.5,1,0,'#333',None,'#ddd'); tx(XK(34),ZK(27),'geçmeli PC kapak (taşımada dökülmez)',3.8,'middle','','#333')
rc(XK(6),ZK(28.5),KC*8,KC*3,1,1,'#333',None,'#bbb'); tx(XK(10),ZK(30.5),'dolum ağzı Ø60',3.4,'middle','','#333')
rc(XK(66),ZK(5),KC*4,KC*3,1,0,GRN,None,'#eaf6ee'); tx(XK(65),ZK(9.5),'kuru bağlantı Ø12',3.4,'end','bold',GRN); tx(XK(65),ZK(6.5),'(helezon soketi yerinde)',3,'end','',GRN)
for dx_ in (20,48): rc(XK(dx_-1.5),ZK(0),KC*3,KC*2,.6,0,'#555',None,'#d0d7de')
tx(XK(34),ZK(-4),'aynı kızaklar ±5 · aynı L raf · aynı ön çekme dudağı',3.6,'middle','','#555')
ci(XK(10),ZK(9),KC*4,.6,'#999','3,2'); tx(XK(10),ZK(9)+1.5,'helezon',3,'middle','','#999'); tx(XK(10),ZK(6),'YOK',3.2,'middle','bold','#999')
rc(XK(56),ZK(16),KC*4,KC*1.5,.6,0,'#333',None,'#fff'); tx(XK(58),ZK(13),'şamandıra',3,'middle','','#333')
rc(XK(0),ZK(-1),KC*68,KC*1,.6,0,'#333',None,'#999'); tx(XK(34),ZK(-8),'alt: kapalı taban plakası (ağız/kapak/pim YOK)',3.6,'middle','','#333')
rows=[('dolum','%d L' % KAP_L),('bir kap','%d gün' % round(GUN_KAP)),('uyarı','şamandıra 4 gün kala'),('dolu kap','%s kg' % f1(KAP_KG)),('eleman','ayda 1, kapanışta (sabaha erir)'),('robot','dokunmaz')]
yy=YC+228
for a_,b_ in rows: tx(XC+14,yy,a_,5.2,'start','bold','#111'); tx(XC+80,yy,b_,5.2,'start','','#333'); yy+=10
para(XC+170,YC+228,'Değişiklik: helezon + tarak yok · taban plakası kapalı · geçmeli kapak + dolum ağzı · arka soket → kuru bağlantı · şamandıra. Gövde, kızak, raf, çatal, dudak aynı kalıp.',30,4.8,'#333')

# ================= D · KESME PRESİ =================
XD,YD,WD,HD = 1140,90,280,320
rc(XD,YD,WD,HD,1.4,4,'#111',None,'#fff')
tx(XD+14,YD+22,'D · KESME PRESİ — plan + kuvvet',10,'start','bold')
cxp,cyp,RP=XD+80,YD+95,2.6
ci(cxp,cyp,RP*16,1.4,BLU); ci(cxp,cyp,RP*15,.9,'#8a6a3a',None,'#f0d9a8')
ln(cxp-RP*14,cyp,cxp+RP*14,cyp,2.4,'#111'); ln(cxp,cyp-RP*14,cxp,cyp+RP*14,2.4,'#111'); ci(cxp,cyp,RP*2,1,'#333',None,'#ccc')
rc(cxp-RP*1.5,cyp+RP*16,RP*3,RP*6,1,1,BLU,None,'#dfe7fb'); tx(cxp+RP*3,cyp+RP*20,'kulp 6 (robot tutar)',3.6,'start','',BLU)
tx(cxp,cyp-RP*19,'bıçak + : 2 × 28 · Ø28 · tepsi Ø32',4,'middle','bold','#333')
for (dx,dy) in ((1,-1),(-1,-1),(1,1),(-1,1)): tx(cxp+dx*RP*7,cyp+dy*RP*7+2,'¼',5,'middle','bold','#8a6a3a')
rows=[('bıçak','2 × 28 cm paslanmaz 1,2 mm · yükseklik 4 · 20° taşlı'),('kuvvet','%d cm × 15–20 N/cm ≈ %s–%s kN' % (BLADE_L*N_BLADE,f1(F_KN[0]),f1(F_KN[1]))),('aktüatör','24 V lineer %d N · strok %d mm · %d mm/s · 60 W' % (ACT_N,ACT_STROKE,ACT_V)),('kılavuz','2 mil Ø12 + 4 lineer yatak · kızak plakası · göbek'),('iniş','10 cm (bıçak alt kenar z +12 → tepsi z +2) · %d sn in + %d sn çık' % (round(T_CUT/2*10/6),round(T_CUT/2*10/6))),('durak','bıçak tepsiye değer, akım limiti keser (tepsi sarf)'),('emniyet','vidalı aktüatör kendini kilitler → elektrik gitse üstte kalır'),('dizi','robot tepsiyi halkaya oturtur, kulpu bırakmaz → in → çık → alır')]
yy=YD+165
for a_,b_ in rows: tx(XD+14,yy,a_,4.9,'start','bold','#111'); tx(XD+58,yy,b_,4.7,'start','','#333'); yy+=11.5
para(XD+14,yy+4,'Robot pres kuvvetini taşımaz: tepsi zemin plakasına dayanır, robot yalnız kulpu tutar (1 kN plakaya gider). 4 parça tepside kalır, PACK'+AP+'te kutuya birlikte kayar.',60,4.8,GRN,'bold')

# ================= E · SORULAR — CEVAPLAR =================
XE,YE,WE,HE = 820,430,600,300
rc(XE,YE,WE,HE,1.4,4,'#111',None,'#fcfdff')
tx(XE+14,YE+22,'E · KEMAL'+AP+'İN SORULARI — CEVAPLAR',10,'start','bold')
QA=[('YAĞ SICAK MI OLMALI, ISITICI NİYE?','Pide için sıcak olması şart değil; ısıtıcı pompa içindir. Sadeyağ 32 °C altında katıdır, oda sıcaklığında AKMAZ (bozulmaz demiştim, o doğru; ama akmaz). 42 °C sıcak dolap: kap içindeki yağ sıvı kalır, hat/nozül dolapta → ayrı hat ısıtması yok. Isıtıcısız tek yol: sıvı yağ (ayçiçek/zeytinyağı) — lezzet kararı Kemal'+AP+'in.'),
    ('TEK KAP KAÇ GÜN GİDER?','12 L dolum = 30 gün (4 ml × 100 pide = 0,4 L/gün). Eleman AYDA 1 kap değiştirir; şamandıra 4 gün kala "yağ az" der, eleman haftalık ziyaretinde doluyu getirir. 42 °C'+AP+'de 1 ay bekleme sınırda ama yeterli (acılaşma 1 aydan sonra). Sağdaki 15 cm boş kalır.'),
    ('HAVALANDIRMA / FİLTRE ŞART MI? BACA?','Baca YOK: fırın elektrikli, gazlı olsaydı isterdi. FAN ŞART: kapalı kabinde fırın 0,7 kW bekleme ısısı birikir, kabin içi 60 °C'+AP+'yi geçer (pano, komşu kabinler). Fan Ø120, 140 m³/h, 5 W — küçük. FİLTRE OPSİYON: pide 3–4 dk, günde 100 → koku az, dükkânda pide kokusu sorun değil; AVM/ofis içindeyse 40×40×5 karbon panel (aylık ~300 TL). Duman yanık olmadıkça yok.'),
    ('SPREY ÖNDE, AZ YER — OLDU MU?','Evet: nozül 20 cm derinlikte, kabın YANINDA (kap 15 + tepsi 34 + boş 15); ayrı niş kalktı, 18 cm kazanıldı; damlalık tavası altta. Kap 68 + kuru bağlantı 4 + pompa 12 = 84 tam oturdu.'),
    ('KESME SIĞDI MI?','Evet: 50 cm zon (z 32–82), 1,5 kN aktüatör dikey. PACK'+AP+'te kesim kalktı → PACK = şarjör 116 + kutulama (tepsi eğilir, 4 parça kayar); PACK'+AP+'te 50 cm boşaldı.'),
    ('ISITICI GÜCÜ NE, GECE AÇIK MI KALIR?','Sıcak dolap yalıtımlıdır: kayıp 20–30 W, günde ≈ 0,6 kWh (buzdolabı gibi) → gece de açık kalır, fırın gece KAPALI. Yeni takılan kap oda sıcaklığında katıdır, 4–6 saatte erir → değişim KAPANIŞTA yapılır, dolap gece açık, sabaha erimiş olur.'),
    ('ELEMAN NE YAPAR?','Ayda 1, kapanışta: boş kabı öne çekip alır (14 kg, bel hizası z 82), doluyu kızağa sürer, kuru bağlantı arkada kendini takar. SERVICE'+AP+'te 16 kg tenekeden kaşıkla doldurur (katı sadeyağ, 5 dk), kapağı geçirir. Haftada 1 damlalık tavasını boşaltır. Kesme bıçağı: ayda 1 kontrol, 6 ayda 1 bileme.')]
yy=YE+42
for q,a in QA:
    tx(XE+14,yy,q,5.6,'start','bold',RED); yy+=8
    yy=para(XE+14,yy,a,150,5.0,'#333')+3

# ================= F · KONTROL · AÇIK =================
XF,YF,WF,HF = 40,750,1380,150
rc(XF,YF,WF,HF,1.4,4,'#111',None,'#fff')
tx(XF+14,YF+22,'F · v3 → v5 DEĞİŞİKLİKLERİ · KONTROL · AÇIK',10,'start','bold')
notes=[(('v5: kartuş 4 L → 1 STANDART KAP (yağ versiyonu) solda, %d L = %d gün, eleman ayda 1 (kapanışta) · pompa (24 V dişli) arka duvarda · sprey ortada önde (niş kalktı) · sıcak dolap 42 °C (klape 4) · KESME PRESİ OVEN'+AP+'de (50) · zonlar hesapla: plenum+fan 12, filtre 5 (opsiyon), pano 20, yedek 12 · tepsi düzlemleri fırın 117/145, sprey 90, kesme 36.') % (KAP_L,round(GUN_KAP)),BLU,'bold'),
       ('KONTROL ✓ 12+20+50+30+56+12+5+12 = 197 · derinlik 68+4+12 = 84 (yağ) · 60+24 = 84 (fırın) · kap 15 + tepsi 34 + boş 15 = 64 · tepsi Ø32 + pay 1 · bıçak 28 < tepsi 32 · kuvvet 0,85–1,1 kN < 1,5 kN · kap dolu %s kg (eleman, bel hizası z 82) · fırın kapağı açıkken yağ zonu önü kapanır (aynı anda gerekmez).' % f1(KAP_KG),GRN,'bold'),
       ('BEYİN: pompa rölesi + şamandıra (4 gün kala "yağ az" mesajı) · dolap termostatı 42 °C · pres aktüatörü (2 switch + akım limiti) · fan (fırın açıkken hep, kapandıktan 10 dk sonra durur) · kapak motorları · durumlar KAPALI / ÖN ISITMA / BEKLEME 340 / EKO 250 / PİŞİRME.','#333',''),
       ('AÇIK: kesme kuvveti pilotu (pide kalınlığı/kabuk, 15–20 N/cm varsayım) · sadeyağ mı sıvı yağ mı (lezzet) · PC gövde + sıcak yağ uzun süre (stres çatlağı) → pilot · kuru bağlantı tipi · PACK'+AP+'te boşalan 50 cm.',AMB,'')]
yy=YF+42
for s,c,fw in notes: yy=para(XF+14,yy,s,230,5.7,c,fw)+3
tx(W-40,H-10,'AUTOKITCH · arastirma/4_OVEN/ist4_oven_detay_v5 · 6 Eyl 2026',7,'end','',GRY)
o.append('</svg>')
svg=chr(10).join(o)
xml.dom.minidom.parseString(svg.encode('utf-8'))
out=r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\4_OVEN\ist4_oven_detay_v5.svg"
io.open(out,'w',encoding='utf-8').write(svg)
print('yazildi + XML gecerli | kap %d gun · dolu %.1f kg · kuvvet %.2f-%.2f kN' % (round(GUN_KAP),KAP_KG,F_KN[0],F_KN[1]))
