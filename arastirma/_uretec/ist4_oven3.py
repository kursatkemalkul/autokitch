# -*- coding: utf-8 -*-
# OVEN v3 (6 Eyl 2026) — Kemal: sadeyağ = elemanın haftalık değiştirdiği KARTUŞ (robot dokunmaz) · niş altı boş (robot tepsiyi sokar, sıkar, çeker) ·
# motorlar küçük (menteşe redüktörleri 3 cm yan boşlukta) · havalandırma + filtre + plenum · yan yalıtım (sol TOPPING +3, sağ PACK karton) · kolon 65 → 70.
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

GRN, RED, BLU, GRY, AMB, PUR, STEEL, GOLD, ICE = '#1d7a4f', '#c0392b', '#1a49b8', '#666', '#b7791f', '#6b4fa8', '#cfd8dc', '#c9a227', '#e3f2fb'
# ---------------- ölçüler (cm, zeminden) ----------------
COL_W, COL_D, COL_H = 70.0, 84.0, 197.0
OV_W, OV_D, OV_H = 64.0, 60.0, 56.0
Z = {'plint':(0,12),'pano':(12,42),'kartus':(42,72),'nis':(72,90),'firin':(90,146),'plenum':(146,172),'filtre':(172,187),'ust':(187,197)}
TEPSI = (95,123)               # tepsi düzlemleri (kapak alt kenarı +5)
KART_L = 4.0; DOZ = 4.0; PIDE = 100
LT_GUN = DOZ*PIDE/1000; HAFTA = LT_GUN*7; GUN_KART = KART_L/LT_GUN
KART_KG = KART_L*0.9+0.6
Q_STANDBY_KW = 0.7             # fırın bekleme kaybı (2 kat, biri eko)
DT = 15.0                      # egzoz hava ısınması K
M3H = Q_STANDBY_KW*1000/(1.2*1005*DT)*3600   # m³/h

o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H))
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,40,'AUTOKITCH — OVEN v3 (6 Eyl 2026) — Omake FPZ01.E21 (2 kapak) · SADEYAĞ KARTUŞU (eleman haftalık değiştirir, robot dokunmaz) · niş altı boş · menteşe motorları 3 cm yan boşlukta · plenum + fan + filtre · yan yalıtım · KOLON 70',14,'start','bold')
tx(30,62,'Kemal: "yağ kartuşu boş teneke gibi olsun, adam doldurup taksın, robot değil · bir haftalık yağ çok mu? · niş altı boş, robot tepsiyi sokar, sıkar, çeker · motorlar küçük · havalandırma/filtre var mı, iç alanda çok sıcak yapar mı, sol/sağ istasyonları etkiler mi, yalıtım?" — Cevaplar bu paftada; HAT v48 kolon 65 → 70 (hat 420).',9,'start','','#444')
ln(30,74,W-30,74,.8,'#999')

# ================= A · KOLON ÖNDEN =================
XA,YA,WA,HA_ = 40,90,340,640
rc(XA,YA,WA,HA_,1.4,4,'#111',None,'#fcfdff')
tx(XA+14,YA+22,'A · OVEN KOLONU 70 × 197 — önden',10,'start','bold')
K=2.6; cx0=XA+46; cz0=YA+48+K*COL_H
X=lambda c: cx0+K*c; Zf=lambda z: cz0-K*z
rc(X(0),Zf(COL_H),K*COL_W,K*COL_H,1.4,2,'#111',None,'#fff')
# yan yalıtım şeritleri (2 yalıtım + 1 hava) — fırın bölgesi boyunca
for xs_ in (0,COL_W-3):
    hatch(X(xs_),Zf(Z['filtre'][1]),K*2,K*(Z['filtre'][1]-Z['kartus'][0]),4,'#b08968'); rc(X(xs_+2),Zf(Z['filtre'][1]),K*1,K*(Z['filtre'][1]-Z['kartus'][0]),.5,0,'#7fb3d5',None,'#eef6fb')
zones=[('plint','#e9e4d6','plint: HAVA GİRİŞİ ızgarası'),('pano','#e3f2fb','PANO 30: PLC I/O · 2 menteşe sürücüsü · 2 SSR · pompa · 24 V'),('kartus','#fff8e0','KARTUŞ YUVASI 30 (ön kapak)'),('nis','#fbf3e6','SPREY NİŞİ 18 — altı boş'),('firin','#fff',''),('plenum','#fde9c9','PLENUM 26: sıcak hava toplanır'),('filtre','#eef3f8','FAN + yağ filtresi + aktif karbon 15'),('ust','#e9e4d6','üst çıkış ızgarası')]
for key,col,lab in zones:
    z0,z1=Z[key]; rc(X(3),Zf(z1),K*(COL_W-6),K*(z1-z0),.7,0,'#555',None,col)
    if lab and key not in ('kartus','nis'): tx(X(COL_W/2),Zf((z0+z1)/2)+2,lab,4.6,'middle','bold' if key in ('plenum','filtre','pano') else '','#333')
# fırın
z0,z1=Z['firin']
rc(X(3),Zf(z1),K*OV_W,K*OV_H,1.3,2,'#111',None,'#f4f4f4')
for (zk0,zk1,nm,tp) in ((z0,z0+28,'KAPAK 1 (alt kat)',TEPSI[0]),(z0+28,z1,'KAPAK 2 (üst kat)',TEPSI[1])):
    rc(X(6.5),Zf(zk1-4),K*57,K*(zk1-zk0-8),1.1,1,'#333',None,'#dbeeff')
    rc(X(6.5),Zf(zk0+4)+K*1.2,K*57,K*1.2,.8,0,'#333',None,'#999')
    tx(X(35),Zf((zk0+zk1)/2)+2,nm+' · hazne 40×40×10 · tepsi düzlemi %d' % tp,4.6,'middle','bold','#333')
    # menteşe redüktörü (sağ yan boşlukta, kapak alt kenarında)
    rc(X(67.2),Zf(zk0+7),K*2.4,K*6,1,1,RED,None,'#f7d7d7')
ln(X(69.6),Zf(z0+10),X(COL_W)+30,Zf(z0+10),.6,RED); tx(X(COL_W)+32,Zf(z0+10)+2,'menteşe motoru ×2 (Ø28)',3.9,'start','',RED)
# niş: nozül + tepsi (robot önden sokar)
zn0,zn1=Z['nis']
ci(X(35),Zf(zn1-1.5),3,1,GOLD,None,'#fff8e0'); poly([(X(35),Zf(zn1-1.5)),(X(20),Zf(zn0+1.5)),(X(50),Zf(zn0+1.5))],.6,GOLD,'#fff3c4',None,.5)
el(X(35),Zf(zn0+3),K*16,K*1.5,1.4,BLU); ln(X(51),Zf(zn0+3),X(57),Zf(zn0+3),1.6,BLU)
tx(X(35),Zf(zn1-4.5)+2,'nozül 90° → Ø30',4.2,'middle','bold',AMB); tx(X(58),Zf(zn0+3)+2,'tepsi',3.8,'start','',BLU)
# kartuş yuvası: kartuş + pompa
zk0_,zk1_=Z['kartus']
rc(X(8),Zf(zk1_-3),K*20,K*22,1.1,2,GOLD,None,'#fff8e0'); tx(X(18),Zf(zk0_+16)+2,'KARTUŞ 4 L',5.2,'middle','bold','#8a6a3a'); tx(X(18),Zf(zk0_+11)+2,'ısıtma ceketi 45 °C',4,'middle','','#8a6a3a'); tx(X(18),Zf(zk0_+7)+2,'kuru bağlantı altta',4,'middle','','#8a6a3a')
rc(X(32),Zf(zk0_+16),K*9,K*8,1,2,'#333',None,'#eee'); tx(X(36.5),Zf(zk0_+12)+2,'POMPA',4.2,'middle','bold'); tx(X(36.5),Zf(zk0_+9)+2,'24 V dişli',3.6,'middle','','#555')
tx(X(50),Zf(zk0_+20)+2,'ÖN KAPAK: eleman',4.2,'middle','',AMB); tx(X(50),Zf(zk0_+16)+2,'haftada 1 kartuşu',4.2,'middle','',AMB); tx(X(50),Zf(zk0_+12)+2,'değiştirir (kilit)',4.2,'middle','',AMB)
ln(X(36.5),Zf(zk0_+24),X(36.5),Zf(zn1-1.5)-3,1.1,GOLD)
# hava akışı okları
arr(X(1.5),Zf(6),X(1.5),Zf(40),'#7fb3d5',1.1); arr(X(COL_W-1.5),Zf(6),X(COL_W-1.5),Zf(40),'#7fb3d5',1.1)
arr(X(35),Zf(Z['filtre'][1]+2),X(35),Zf(COL_H-1),'#7fb3d5',1.3); tx(X(35)+5,Zf(COL_H-4),'egzoz → mekân',3.9,'start','','#1a49b8')
# ölçüler
for key,lab in (('plint','12'),('pano','30'),('kartus','30'),('nis','18'),('firin','56'),('plenum','26'),('filtre','15'),('ust','10')):
    z0,z1=Z[key]; dim(X(COL_W)+14,Zf(z1),X(COL_W)+14,Zf(z0),lab,4.6,0,GRY)
dim(X(0),Zf(COL_H)-14,X(COL_W),Zf(COL_H)-14,'70 = 3 + fırın 64 + 3',5.2)
para(XA+14,YA+572,'Yan boşluk 3 cm: 2 cm seramik elyaf yalıtım + 1 cm havalandırmalı hava aralığı; menteşe motorları bu aralıkta, kapak alt kenarı hizasında (Ø28 sonsuz vida redüktör, 24 V, 5 N·m; kapak camı ~3 kg → 4 N·m; motor yerinde yalıtım kesilir). Hava plint ızgarasından girer, yan aralıklar ve arka kanaldan plenuma çıkar, fan filtreden geçirip üst ızgaradan mekâna verir.',72,5.2,'#333')

# ================= B · YAN KESİT (derinlik 84) =================
XB,YB,WB,HB = 400,90,400,640
rc(XB,YB,WB,HB,1.4,4,'#111',None,'#fcfbf8')
tx(XB+14,YB+22,'B · YAN KESİT 84 × 197 — hava, egzoz, yalıtım, niş, kartuş',10,'start','bold')
bx=XB+95; bz=YA+48+K*COL_H
XS=lambda d: bx+K*d; ZS=lambda z: bz-K*z      # d: önden arkaya (0 ön yüz, 84 arka)
rc(XS(0),ZS(COL_H),K*COL_D,K*COL_H,1.4,2,'#111',None,'#fff')
# arka kanal 24 (fırın arkası) + arka yalıtım
hatch(XS(COL_D-2),ZS(COL_H-1),K*2,K*(COL_H-2),4,'#b08968')
rc(XS(OV_D+2),ZS(Z['plenum'][0]),K*(COL_D-OV_D-4),K*(Z['plenum'][0]-Z['plint'][1]),.6,0,'#7fb3d5',None,'#eef6fb'); tx(XS(OV_D+12),ZS(112)+2,'arka',3.9,'middle','','#1a49b8'); tx(XS(OV_D+12),ZS(108)+2,'kanal 20',3.9,'middle','','#1a49b8'); tx(XS(OV_D+12),ZS(104)+2,'hava+kablo',3.4,'middle','','#1a49b8'); tx(XS(OV_D+12),ZS(100)+2,'+buhar',3.4,'middle','','#1a49b8')
# zonlar (yandan)
for key,col in (('plint','#e9e4d6'),('pano','#e3f2fb'),('kartus','#fff8e0'),('nis','#fbf3e6'),('plenum','#fde9c9'),('filtre','#eef3f8'),('ust','#e9e4d6')):
    z0,z1=Z[key]; dd = OV_D+2 if key in ('pano','kartus','nis') else COL_D-4
    rc(XS(2),ZS(z1),K*(dd-2),K*(z1-z0),.6,0,'#555',None,col)
# fırın gövdesi + kapaklar (yandan, açık/kapalı)
z0,z1=Z['firin']
rc(XS(2),ZS(z1),K*OV_D,K*OV_H,1.3,2,'#111',None,'#f4f4f4'); tx(XS(32),ZS(z0+50)+2,'OMAKE 60 derin',4.6,'middle','bold','#333')
for (zk0,zk1,tp) in ((z0,z0+28,TEPSI[0]),(z0+28,z1,TEPSI[1])):
    rc(XS(6),ZS(zk0+9),K*40,K*1.5,.8,0,'#777',None,'#ccc'); tx(XS(26),ZS(zk0+6)+2,'taş 40 · tepsi Ø32 + kulp 6 = 38 ✓',3.8,'middle','','#555')
    rc(XS(2),ZS(zk1-4),K*1.2,K*(zk1-zk0-8),1,0,'#333',None,'#dbeeff')                                  # kapak kapalı
    ln(XS(2),ZS(zk0+4),XS(2)-K*20,ZS(zk0+4),1,'#333','3,2'); ci(XS(2),ZS(zk0+4),1.8,1,RED,None,RED)      # açık kapak (kesikli) + menteşe
    el(XS(2)-K*10,ZS(zk0+4)+K*0.4,K*1.5,K*0.8,.6,BLU)
tx(XS(2)-K*15,ZS(z0-3)+2,'kapak açık (kesikli) → tepsi girer',3.8,'middle','',GRY)
# egzoz yolu: fırın buhar çıkışı arkadan kanala, plenum, fan, filtre
arr(XS(OV_D+3),ZS(z0+30),XS(OV_D+12),ZS(Z['plenum'][0]+4),'#c0392b',1.1)
arr(XS(30),ZS(Z['plenum'][0]+6),XS(30),ZS(Z['filtre'][0]+2),'#c0392b',1.3)
ci(XS(30),ZS(Z['filtre'][0]+7),K*6,1.1,'#333',None,'#fff'); tx(XS(30),ZS(Z['filtre'][0]+7)+2,'FAN',4.2,'middle','bold'); tx(XS(30),ZS(Z['filtre'][0]+1)+2,'%d m³/h' % (round(M3H/10)*10),3.8,'middle','','#555')
rc(XS(42),ZS(Z['filtre'][1]-1),K*30,K*13,1,1,'#333',None,'#dfe7fb'); tx(XS(57),ZS(Z['filtre'][0]+9)+2,'yağ filtresi',4,'middle','bold','#333'); tx(XS(57),ZS(Z['filtre'][0]+4)+2,'+ aktif karbon',4,'middle','','#333')
arr(XS(57),ZS(Z['filtre'][1]+1),XS(57),ZS(COL_H-1),'#c0392b',1.3); tx(XS(57)+6,ZS(COL_H-4),'üst ızgara → mekâna (bacasız)',3.9,'start','',RED)
# hava girişi
arr(XS(20),ZS(1),XS(20),ZS(11),'#7fb3d5',1.1); tx(XS(24),ZS(5)+2,'plint ızgarası: hava girişi',3.9,'start','','#1a49b8')
arr(XS(OV_D+12),ZS(Z['plint'][1]+2),XS(OV_D+12),ZS(Z['plenum'][0]-3),'#7fb3d5',1.1)
# niş: nozül, tepsi önden
zn0,zn1=Z['nis']
ci(XS(30),ZS(zn1-1.5),3,1,GOLD,None,'#fff8e0'); poly([(XS(30),ZS(zn1-1.5)),(XS(15),ZS(zn0+1.5)),(XS(45),ZS(zn0+1.5))],.6,GOLD,'#fff3c4',None,.5)
el(XS(30),ZS(zn0+3),K*16,K*1.5,1.4,BLU); ln(XS(2)-K*22,ZS(zn0+3),XS(14),ZS(zn0+3),2,'#999'); tx(XS(2)-K*12,ZS(zn0+6)+2,'robot kolu',3.8,'middle','',GRY)
arr(XS(2)-K*24,ZS(zn0+9),XS(2)-K*6,ZS(zn0+9),AMB,1.1); tx(XS(2)-K*14,ZS(zn0+12)+2,'sok → 1 sn → çek',3.9,'middle','bold',AMB)
tx(XS(40),ZS(zn1-4)+2,'niş altı boş: tepsi nozülün 15 altında',3.8,'middle','','#333')
# kartuş yuvası yandan: kartuş önde, pompa arkada, ısıtmalı hat
zk0_,zk1_=Z['kartus']
rc(XS(4),ZS(zk1_-3),K*20,K*22,1.1,2,GOLD,None,'#fff8e0'); tx(XS(14),ZS(zk0_+15)+2,'KARTUŞ',4.6,'middle','bold','#8a6a3a'); tx(XS(14),ZS(zk0_+10)+2,'16×16×18',3.8,'middle','','#8a6a3a')
rc(XS(28),ZS(zk0_+14),K*10,K*8,1,2,'#333',None,'#eee'); tx(XS(33),ZS(zk0_+10)+2,'POMPA',3.9,'middle','bold')
ln(XS(24),ZS(zk0_+4),XS(28),ZS(zk0_+4),1.2,GOLD); ln(XS(33),ZS(zk0_+22),XS(33),ZS(zn0+8),1.2,GOLD); ln(XS(33),ZS(zn0+8),XS(30),ZS(zn1-1.5)-3,1.2,GOLD)
tx(XS(46),ZS(zk0_+22)+2,'ısıtmalı hat Ø6 + çek valf',3.8,'start','','#555')
rc(XS(2),ZS(zk1_-1),K*1.2,K*(zk1_-zk0_-2),1,0,AMB,None,'#fde9c9'); tx(XS(2)-K*6,ZS(zk0_+12)+2,'ön kapak',3.8,'middle','',AMB)
tx(XS(30),ZS(Z['pano'][0]+15)+2,'PANO (servis kapağı önde)',4.4,'middle','bold','#1a49b8')
dim(XS(0),ZS(COL_H)-14,XS(OV_D+2),ZS(COL_H)-14,'fırın 60',4.8,0,GRY); dim(XS(OV_D+2),ZS(COL_H)-14,XS(COL_D),ZS(COL_H)-14,'arka 24 (toplam 84)',4.8,0,GRY)
tx(XS(0)-4,ZS(150)+2,'ÖN',4.6,'end','bold',GRY); tx(XS(COL_D)+4,ZS(150)+2,'ARKA',4.6,'start','bold',GRY)
para(XB+14,YB+572,'Fırının buhar/duman çıkışı arkadadır: kanala alınır, plenumda yan aralıklardan gelen sıcak havayla birleşir, fan yağ filtresi + aktif karbondan geçirip mekâna verir (bacasız). Isı bütçesi: bekleme kaybı ≈ %s kW → %d m³/h fanla hava 15 °C ısınır; kabin yüzeyi oda + 10 °C, komşu kabinlere ısı geçmez.' % (f1(Q_STANDBY_KW),round(M3H/10)*10),80,5.2,'#333')

# ================= C · KARTUŞ =================
XC,YC,WC,HC = 820,90,300,320
rc(XC,YC,WC,HC,1.4,4,'#111',None,'#fff')
tx(XC+14,YC+22,'C · SADEYAĞ KARTUŞU — eleman değiştirir',10,'start','bold')
KC=4.4; kx=XC+120; kz=YC+215
XK=lambda x: kx+KC*x; ZK=lambda z: kz-KC*z
rc(XK(0),ZK(18),KC*16,KC*18,1.3,2,'#111',None,'#fff8e0'); rc(XK(1),ZK(15),KC*14,KC*14,0,0,'none',None,'#f6d76b')
rc(XK(3),ZK(19.5),KC*10,KC*1.5,1,1,'#333',None,'#ddd'); tx(XK(8),ZK(21.5),'geniş vidalı kapak (SERVICE'+AP+'te tenekeden doldurulur)',4,'middle','',GRY)
ln(XK(8),ZK(17),XK(8),ZK(1.5),1.2,'#333'); tx(XK(9),ZK(9)+2,'dalgıç boru',3.8,'start','','#555')
rc(XK(6.5),ZK(0),KC*3,KC*1.5,1,0,GRN,None,'#eaf6ee'); tx(XK(8),ZK(-3.5),'kuru bağlantı (takınca açılır, çıkarınca kapanır)',4,'middle','bold',GRN)
rc(XK(-1.2),ZK(16),KC*1.2,KC*15,.8,0,RED,None,'#f7d7d7'); rc(XK(16),ZK(16),KC*1.2,KC*15,.8,0,RED,None,'#f7d7d7'); tx(XK(-2),ZK(8)+2,'ısıtma ceketi (yuvada)',3.8,'end','',RED)
rc(XK(17.5),ZK(12),KC*2,KC*3,.9,1,'#333',None,'#ccc'); tx(XK(20.2),ZK(13.5)+2,'kilit mandalı',3.6,'start','','#555')
dim(XK(0),ZK(-6.5),XK(16),ZK(-6.5),'16',4.6,0,GRY); dim(XK(16)+KC*17,ZK(18),XK(16)+KC*17,ZK(0),'18',4.6,0,GRY)
para(XC+14,YC+262,('4 L paslanmaz (16×16×18, iç 4,3 L); dolu %s kg, tek elle taşınır. Eleman: ön kapağı açar, mandalı çeker, boş kartuşu alır, dolusunu takar (kuru bağlantı kendini açar), kapağı kapatır — 1 dakika. Boş kartuş SERVICE'+AP+'te 16 kg tenekeden doldurulur, bulaşıkta yıkanır. Robot dokunmaz.') % f1(KART_KG),64,5.2,'#333')

# ================= D · BİR HAFTA ÇOK MU? =================
XD,YD,WD,HD = 1140,90,280,320
rc(XD,YD,WD,HD,1.4,4,'#111',None,'#fff')
tx(XD+14,YD+22,'D · BİR HAFTALIK YAĞ ÇOK MU?',10,'start','bold')
rows=[('doz / pide','%d ml' % DOZ),('gün (%d pide)' % PIDE,'%s L' % f1(LT_GUN)),('hafta','%s L' % f1(HAFTA)),('kartuş 4 L','%d gün' % round(GUN_KART)),('dolu kartuş','%s kg' % f1(KART_KG)),('kartuş boyutu','16×16×18 cm')]
yy=YD+44
for a_,b_ in rows: tx(XD+14,yy,a_,5.6,'start','bold','#111'); tx(XD+130,yy,b_,5.6,'start','','#333'); yy+=13
yy=para(XD+14,yy+6,'HAYIR, çok değil: bir hafta 2,8 L = bir su şişesi büyüklüğü, 3,6 kg. İkiye bölmeye, robota değiştirtmeye gerek yok. Tek kartuş, tek yuva, haftada 1 eleman.',54,5.4,GRN,'bold')
yy=para(XD+14,yy+2,'Yedek: SERVICE'+AP+'te 2. (boş) kartuş + 16 kg teneke (≈ 6 hafta). Kartuş biterse şamandıra BEYİN'+AP+'e "yağ az" der; sprey olmadan pide çıkmaz, sipariş durur.',54,5.2,'#333')

# ================= E · KOMŞULAR · ISI · YALITIM · MOTORLAR =================
XE,YE,WE,HE = 820,430,600,300
rc(XE,YE,WE,HE,1.4,4,'#111',None,'#fcfdff')
tx(XE+14,YE+22,'E · İÇ ALANDA ÇOK SICAK YAPAR MI? — komşular, yalıtım, havalandırma, motorlar',10,'start','bold')
# mini plan: TOPPING | OVEN | PACK
KP=1.1; px0=XE+30; py0=YE+40
for (x0,w,nm,col) in ((0,70,'TOPPING +3 °C',ICE),(70,70,'OVEN',"#fde9c9"),(140,70,'PACK (karton kutu)','#fbf3e6')):
    rc(px0+KP*x0,py0,KP*w,KP*84,1,1,'#111',None,col); tx(px0+KP*(x0+w/2),py0+KP*44,nm,4.6,'middle','bold','#333')
hatch(px0+KP*70,py0,KP*3,KP*84,3,'#b08968'); hatch(px0+KP*137,py0,KP*3,KP*84,3,'#b08968')
rc(px0+KP*73,py0+KP*2,KP*64,KP*60,1,1,'#333',None,'#f4f4f4'); tx(px0+KP*105,py0+KP*32,'fırın 64×60',4.2,'middle','','#333')
rc(px0+KP*73,py0+KP*62,KP*64,KP*20,.6,0,'#7fb3d5',None,'#eef6fb'); tx(px0+KP*105,py0+KP*73,'arka kanal',3.8,'middle','','#1a49b8')
tx(px0+KP*105,py0+KP*84+9,'plan: yan 3 cm = yalıtım 2 + hava 1',4.2,'middle','',GRY)
ey=YE+150
ey=para(XE+14,ey,'SOL: TOPPING (+3 °C soğuk kabin, sağ yan kanalı hava dönüşü). SAĞ: PACK (116 katlı karton kutu, kutu 35 °C üstünü sevmez). İkisi de sıcak istemez → OVEN kolonunun iki yanında 2 cm seramik elyaf + 1 cm hava aralığı; aralıktan geçen hava plenuma çıkar, komşu duvara ısı geçmez (yüzey < oda + 10 °C).',105,5.2,'#333')
ey=para(XE+14,ey+2,'HAVALANDIRMA: Omake bacasızdır, kavite buharı arkadan çıkar. Kabinde: plint girişi → yan/arka kanallar → plenum 26 → fan %d m³/h → yağ filtresi + aktif karbon → üst ızgara → mekân. Filtre aylık eleman işi (O5). Duman: pide 3–4 dk, yağ az; karbon yeter, dış baca gerekmez.' % (round(M3H/10)*10),105,5.2,'#333')
ey=para(XE+14,ey+2,'MOTORLAR (küçük, yer yemez): 2 menteşe redüktörü Ø28×60 mm (3 cm yan aralıkta) · pompa 60×40×40 mm (kartuş arkasında) · fan Ø120 (filtre bölmesi) · sürücüler + SSR panoda (30 cm). Ayrı motor odası yok.',105,5.2,GRN,'bold')
ey=para(XE+14,ey+2,'Isı: bekleme kaybı ≈ 0,7 kW (biri eko), pişirme anında 2,4 kW; egzoz 15 °C ısınır, mekâna günde 6–8 kWh ısı — bir küçük radyatör kadar; klima yükü olarak kabul edilebilir.',105,5.2,'#333')

# ================= F · KONTROL · DEĞİŞİKLİK · AÇIK =================
XF,YF,WF,HF = 40,750,1380,150
rc(XF,YF,WF,HF,1.4,4,'#111',None,'#fff')
tx(XF+14,YF+22,'F · v2 → v3 DEĞİŞİKLİKLERİ · KONTROL · AÇIK',10,'start','bold')
notes=[('v3: sadeyağ TANK → KARTUŞ (4 L, eleman haftalık değiştirir, kuru bağlantı, ısıtma ceketi) · niş altı boş (robot tepsiyi sokar, sıkar, çeker) · kolon 65 → 70 (menteşe motorları + yalıtım için 3 cm yan) · plenum 26 + fan + yağ/karbon filtre · zonlar zeminden: plint 12 / pano 30 / kartuş 30 / niş 18 / fırın 56 / plenum 26 / filtre 15 / üst 10 = 197 ✓ · tepsi düzlemleri 95 / 123.',BLU,'bold'),
       ('KONTROL ✓ hazne 40×40×10: tepsi Ø32 + kulp 6 = 38 ✓ (② kapanır, kulp 6) · derinlik fırın 60 + arka 24 = 84 ✓ · kartuş 4 L = %d gün ≥ 7 ✓ · fan %d m³/h bekleme kaybı için yeter ✓ · komşu yüzey < oda + 10 °C ✓ · HAT toplamı 415 → 420.' % (round(GUN_KART),round(M3H/10)*10),GRN,'bold'),
       ('BEYİN: kapak motorları (2 switch, akım limiti) · SSR + termokupl (2 kat) · pompa rölesi (atım 0,5 sn = 4 ml) · şamandıra (yağ az) · fan (fırın açıkken hep, kapalıyken 10 dk sonra durur) · durumlar KAPALI / ÖN ISITMA / BEKLEME 340 / EKO 250 / PİŞİRME.','#333',''),
       ('AÇIK: kuru bağlantı tipi (CPC/Colder gıda tipi kaplin) · kartuş kalıbı (paslanmaz kap + vidalı kapak) · aktif karbon filtre tedariki · pilot: Omake'+AP+'de tepsili pide alt kızarması (F-T2) · kolon 70 → HAT v48 + site.',AMB,'')]
yy=YF+42
for s,c,fw in notes: yy=para(XF+14,yy,s,230,5.7,c,fw)+3
tx(W-40,H-10,'AUTOKITCH · arastirma/4_OVEN/ist4_oven_detay_v3 · 6 Eyl 2026',7,'end','',GRY)
o.append('</svg>')
svg=chr(10).join(o)
xml.dom.minidom.parseString(svg.encode('utf-8'))
out=r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\4_OVEN\ist4_oven_detay_v3.svg"
io.open(out,'w',encoding='utf-8').write(svg)
print('yazildi + XML gecerli | kartus %d gun · dolu %.1f kg · fan %d m3/h' % (round(GUN_KART),KART_KG,round(M3H/10)*10))
