# -*- coding: utf-8 -*-
# OVEN v2 (6 Eyl 2026) — Omake FPZ01.E21 çift katlı taş tabanlı fırın (64×60×56, 2 kapak, 4,8 kW) + motorlu kapaklar +
# SADEYAĞ SPREY ÜNİTESİ (4 L ısıtmalı tank + dişli pompa + 90° tam koni nozül, tek atım 4 ml) + haftalık stok mantığı + satın alma seçenekleri.
import io, math, xml.dom.minidom
W, H = 1460, 1020
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
def leader(x1,y1,x2,y2,c='#999'): ln(x1,y1,x2,y2,.6,c,'2,2')
def f1(v): return ('%.1f' % v).replace('.',',')

GRN, RED, BLU, GRY, AMB, PUR, STEEL, GOLD = '#1d7a4f', '#c0392b', '#1a49b8', '#666', '#b7791f', '#6b4fa8', '#cfd8dc', '#c9a227'

# ---------------- sayılar ----------------
DOZ_ML = 4.0                 # ml / pide (3–5)
PIDE_GUN = 100
LT_GUN = DOZ_ML*PIDE_GUN/1000        # 0,4 L/gün
TANK_L = 4.0
GUN_TANK = TANK_L/LT_GUN             # 10 gün
HAFTA_L = LT_GUN*7                   # 2,8 L
POMPA_LMIN = 0.5                     # L/dk
ATIM_S = DOZ_ML/(POMPA_LMIN*1000/60) # 0,48 s
NOZ_H = 15.0; NOZ_ANG = 90.0
IZ_D = 2*NOZ_H*math.tan(math.radians(NOZ_ANG/2))   # 30 cm
# kolon yerleşimi (zeminden, cm)
LAY = [('ayak / plint',0,12,'#e9e4d6'),('BOŞ — ileride (pano büyümesi / 2. ünite)',12,52,'#f7f6f2'),('PANO: PLC I/O, 2 aktüatör sürücüsü, 2 SSR + termokupl, pompa rölesi',52,72,'#e3f2fb'),
       ('SADEYAĞ ÜNİTESİ: tank 4 L + ısıtıcı + pompa (ön kapak, eleman doldurur)',72,102,'#fff8e0'),('SPREY NİŞİ 18: tepsi geçişi 14 + nozül',102,120,'#fbf3e6'),
       ('OMAKE FPZ01.E21 — alt kat (kapak 1)',120,148,'#fff'),('OMAKE FPZ01.E21 — üst kat (kapak 2)',148,176,'#fff'),('karbon filtre + fan (bacasız)',176,191,'#eef3f8'),('üst pay',191,197,'#e9e4d6')]

o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H))
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,40,'AUTOKITCH — OVEN v2 (6 Eyl 2026) — Omake FPZ01.E21 çift katlı taş fırın (64×60×56, 2 kapak, 4,8 kW) + motorlu kapaklar + SADEYAĞ SPREY ÜNİTESİ (4 L tank, pompa, tek atım nozül) + haftalık stok',14,'start','bold')
tx(30,62,'Kemal: "fırın iki kapaklı mı? · yağ sıkan yeri düzgünce tasarla · satın alınabilir mi (Türkiye / yurt dışı / Çin)? · ne kadar yağ stoğu, 1 hafta yeter mi, soğukta mı beklemeli?" — Kolon 65 × 197 × 84 aynı, HAT v47 yerleşimi korunur; eski 90 cm fırın + 3 teneke bölmesi kalkar.',9,'start','','#444')
ln(30,74,W-30,74,.8,'#999')

# ================= A · OVEN KOLONU ÖN GÖRÜNÜŞ =================
XA,YA,WA,HA_ = 40,90,330,640
rc(XA,YA,WA,HA_,1.4,4,'#111',None,'#fcfdff')
tx(XA+14,YA+22,'A · OVEN KOLONU 65 × 197 (ön) — yeni dizilim',10,'start','bold')
K=2.6; cx0=XA+40; cz0=YA+50+K*197
X=lambda c: cx0+K*c; Z=lambda z: cz0-K*z
rc(X(0),Z(197),K*65,K*197,1.4,2,'#111',None,'#fff')
for (lab,z0,z1,col) in LAY:
    rc(X(0),Z(z1),K*65,K*(z1-z0),.7,0,'#555',None,col)
# fırın gövdesi (64 geniş, 56 yüksek) + 2 kapak + camlar + termostat düğmeleri
rc(X(0.5),Z(176),K*64,K*56,1.3,2,'#111',None,'#f4f4f4')
for (zk0,zk1,nm) in ((120,148,'KAPAK 1 (alt kat) · tepsi 125'),(148,176,'KAPAK 2 (üst kat) · tepsi 153')):
    rc(X(4),Z(zk1-4),K*56,K*(zk1-zk0-8),1.1,1,'#333',None,'#dbeeff')          # cam kapak
    rc(X(4),Z(zk0+4)+K*1.2,K*56,K*1.2,.8,0,'#333',None,'#999')                   # tutamak
    tx(X(32),Z((zk0+zk1)/2)+2,nm,5,'middle','bold','#333'); tx(X(32),Z((zk0+zk1)/2)-7,'hazne 40×40×10',4.2,'middle','','#555')
    rc(X(61),Z(zk1-6),K*3,K*3,.8,3,'#333',None,'#ccc'); rc(X(61),Z(zk0+8),K*3,K*3,.8,3,'#333',None,'#ccc')
    # aktüatör (yanda, kesikli)
    rc(X(60.5),Z(zk1-8),K*2.6,K*16,.8,1,RED,'3,2','none')
tx(X(63),Z(120)-6,'aktüatör ×2',4,'middle','',RED)
tx(X(32),Z(191)+K*7,'karbon filtre + fan',5,'middle','','#1a49b8')
# sprey nişi: nozül + tepsi
ci(X(32),Z(117),3,1,GOLD,None,'#fff8e0'); poly([(X(32),Z(117)),(X(17),Z(102)),(X(47),Z(102))],.6,GOLD,'#fff3c4',None,.5)
el(X(32),Z(104),K*16,K*1.6,1.4,BLU); ln(X(48),Z(104),X(54),Z(104),1.6,BLU)
tx(X(32),Z(111)+2,'nozül 90° · Ø30 iz',4.6,'middle','bold',AMB); tx(X(32),Z(99)+2,'tepsi 1 sn durur, tek atım 4 ml',4.4,'middle','',BLU)
# yağ ünitesi
rc(X(6),Z(100),K*22,K*24,1.1,2,GOLD,None,'#fff8e0'); tx(X(17),Z(90)+2,'TANK 4 L',5.4,'middle','bold','#8a6a3a'); tx(X(17),Z(85)+2,'45 °C · seviye',4.2,'middle','','#8a6a3a')
rc(X(32),Z(92),K*10,K*10,1,2,'#333',None,'#eee'); tx(X(37),Z(87)+2,'POMPA',4.4,'middle','bold'); tx(X(37),Z(83)+2,'24 V dişli',3.8,'middle','','#555')
rc(X(46),Z(92),K*14,K*10,.9,2,'#555',None,'#f4f4f4'); tx(X(53),Z(88)+2,'ısıtmalı hat',4,'middle','','#555'); tx(X(53),Z(84)+2,'+ çek valf',4,'middle','','#555')
ln(X(37),Z(97),X(37),Z(102),1.2,GOLD); ln(X(37),Z(102),X(32),Z(114),1.2,GOLD)
tx(X(32),Z(76)+2,'ön kapak: eleman haftada 1 doldurur (2,8 L)',4.4,'middle','',AMB)
tx(X(32),Z(62)+2,'PANO',5,'middle','bold','#1a49b8'); tx(X(32),Z(57)+2,'PLC I/O · 2 aktüatör · 2 SSR · pompa rölesi',4,'middle','','#1a49b8')
tx(X(32),Z(34)+2,'BOŞ (ileride)',5,'middle','bold','#999'); tx(X(32),Z(28)+2,'eski 3 teneke bölmesi kalktı',4,'middle','','#999')
# ölçüler (sağ)
for (z0,z1,lab) in ((0,12,'12'),(12,52,'40'),(52,72,'20'),(72,102,'30'),(102,120,'18'),(120,176,'56 fırın'),(176,191,'15'),(191,197,'6')):
    dim(X(65)+14,Z(z1),X(65)+14,Z(z0),lab,4.6,0,GRY)
dim(X(0),Z(197)-14,X(65),Z(197)-14,'65 (fırın 64)',5.4)
para(XA+14,YA+572,'İki kapak: her katın kendi camlı, aşağı açılır kapağı ve kendi alt/üst termostatı var. Her kapağa 24 V lineer aktüatör (strok 15, 200 N) + 2 switch; sıkışma akım limiti. Normalde alt kat çalışır, üst kat EKO/KAPALI; kuyruk ≥ 2 siparişte BEYİN üst katı ısıtır. Derinlik: fırın 60 + arka 24 (kablo, egzoz → filtre) = 84 ✓.',66,5.4,'#333')

# ================= B · SPREY ÜNİTESİ KESİT =================
XB,YB,WB,HB = 390,90,520,640
rc(XB,YB,WB,HB,1.4,4,'#111',None,'#fcfbf8')
tx(XB+14,YB+22,'B · SADEYAĞ SPREY ÜNİTESİ — kesit (tank · pompa · ısıtmalı hat · nozül · tepsi)',10,'start','bold')
KB=5.0; bx=XB+60; bz=YB+236
XBp=lambda x: bx+KB*x; ZB=lambda z: bz-KB*z
# tank (çift cidar) 20×24 (kesit), 4 L
rc(XBp(0),ZB(24),KB*20,KB*24,1.2,2,'#111',None,'#fff'); rc(XBp(1),ZB(23),KB*18,KB*23,.8,1,'#999',None,'#fff8e0')
rc(XBp(1),ZB(19),KB*18,KB*18,0,0,'none',None,'#f6d76b')                      # yağ seviyesi
rc(XBp(2),ZB(25.5),KB*16,KB*1.5,1,1,'#333',None,'#ddd'); tx(XBp(10),ZB(27),'kapak (kilitli, eleman doldurur)',4.4,'middle','',GRY)
rc(XBp(3),ZB(3),KB*14,KB*1.2,1,1,RED,None,'#f7d7d7'); tx(XBp(10),ZB(0.5)+2,'ısıtıcı 100 W + termostat 45 °C',4.2,'middle','',RED)
ci(XBp(17),ZB(19),2.2,1,'#333',None,'#fff'); ln(XBp(17),ZB(19),XBp(17),ZB(23.5),.8,'#333'); tx(XBp(17)+4,ZB(19)+2,'şamandıra (yağ az)',4,'start','',GRY)
tx(XBp(10),ZB(12)+2,'SADEYAĞ 4 L · 45 °C',5.4,'middle','bold','#8a6a3a'); tx(XBp(10),ZB(8)+2,'çift cidar, yalıtımlı, paslanmaz',4.2,'middle','','#8a6a3a')
rc(XBp(20),ZB(6),KB*4,KB*3,.9,1,'#333',None,'#ccc'); tx(XBp(22),ZB(1.5)+2,'tahliye',3.8,'middle','',GRY)
# pompa + hat + nozül
ln(XBp(10),ZB(0),XBp(10),ZB(-4),1.6,GOLD)
rc(XBp(6),ZB(-4),KB*8,KB*5,1.1,2,'#333',None,'#eee'); tx(XBp(10),ZB(-11.5)+2,'POMPA 24 V dişli · 0,5 L/dk',4.2,'middle','bold'); tx(XBp(10),ZB(-14.5)+2,'doz = süre: 4 ml = %s sn' % f1(ATIM_S),4,'middle','','#555')
ln(XBp(14),ZB(-6.5),XBp(40),ZB(-6.5),2.2,GOLD); ln(XBp(14),ZB(-6.5),XBp(40),ZB(-6.5),.8,RED,'2,2')
tx(XBp(16),ZB(-4.6)+2,'Ø6 paslanmaz hat, ısıtma şeridi 40 °C (sadeyağ 32 °C altında donar)',4.2,'start','','#555')
ln(XBp(40),ZB(-6.5),XBp(40),ZB(-22),2.2,GOLD)
rc(XBp(38.5),ZB(-14),KB*3,KB*3,1,1,'#333',None,'#fff'); tx(XBp(45),ZB(-12)+2,'yaylı çek valf (damla önleyici)',4.2,'start','',GRY)
ci(XBp(40),ZB(-23),3.2,1.2,GOLD,None,'#fff8e0'); tx(XBp(45),ZB(-23)+2,'nozül tam koni 90°, gıda tipi',4.4,'start','bold',AMB)
poly([(XBp(40),ZB(-23)),(XBp(40-IZ_D/2),ZB(-23-NOZ_H)),(XBp(40+IZ_D/2),ZB(-23-NOZ_H))],.6,GOLD,'#fff3c4',None,.5)
el(XBp(40),ZB(-23-NOZ_H-1),KB*16,KB*1.6,1.4,BLU); ln(XBp(56),ZB(-23-NOZ_H-1),XBp(62),ZB(-23-NOZ_H-1),1.6,BLU)
el(XBp(40),ZB(-23-NOZ_H-2),KB*15,KB*1.0,.8,'#8a6a3a')
tx(XBp(40),ZB(-23-NOZ_H-5)+2,'tepsi Ø32 + pide Ø30 · robot 1 sn durur · atım → iz Ø%d' % round(IZ_D),4.4,'middle','',BLU)
dim(XBp(40)+KB*17,ZB(-23),XBp(40)+KB*17,ZB(-23-NOZ_H),'%d' % NOZ_H,4.6,0,GRY)
dim(XBp(0),ZB(24)+KB*3.5,XBp(20),ZB(24)+KB*3.5,'20',4.6,0,GRY)
para(XB+14,YB+HB-58,'Çalışma: BEYİN "atım" rölesi → pompa %s sn → 4 ml sadeyağ, 90° koni ile pidenin tamamına (Ø30). Robot tepsiyi nozülün 15 cm altında 1 sn tutar; süpürme yok. Gün sonu mini-CIP: tank boşken 60 °C su + deterjan 30 sn pompadan geçer, tahliyeden atılır; nozül haftada 1 sökülür.' % f1(ATIM_S),100,5.4,'#333')

# ================= C · STOK · SOĞUK ZİNCİR =================
XC,YC,WC,HC = 930,90,490,400
rc(XC,YC,WC,HC,1.4,4,'#111',None,'#fff')
tx(XC+14,YC+22,'C · NE KADAR YAĞ · 1 HAFTA YETER Mİ · SOĞUKTA MI',10,'start','bold')
rows=[('doz / pide','%d ml (3–5)' % DOZ_ML),('günlük (%d pide)' % PIDE_GUN,'%s L' % f1(LT_GUN)),('haftalık','%s L' % f1(HAFTA_L)),('tank 4 L → kaç gün','%d gün' % round(GUN_TANK)),
      ('eleman dolumu','haftada 1, tanka 2,8 L'),('teneke (16 kg ≈ 17 L)','≈ 6 hafta; SERVICE kuru rafında, oda sıcaklığı'),('makinede teneke deposu','YOK (v45'+AP+'teki 3 teneke bölmesi kalktı)')]
yy=YC+46
for a_,b_ in rows:
    tx(XC+14,yy,a_,5.8,'start','bold','#111'); tx(XC+150,yy,b_,5.8,'start','','#333'); yy+=14
ln(XC+12,yy-4,XC+WC-12,yy-4,.8,'#bbb')
yy=para(XC+14,yy+8,'SOĞUKTA BEKLEMESİ GEREKMEZ: sadeyağın suyu < %0,5, kapalı teneke oda sıcaklığında aylarca durur; açık teneke serin-karanlık yerde 1–2 ay. Bu yüzden tereyağı değil SADEYAĞ seçildi (tereyağı buzdolabı ister, suyu püskürtmede sıçrar).',82,5.4,GRN,'bold')
yy=para(XC+14,yy+2,'Tankta 45 °C'+AP+'de 1 hafta: sadeyağ için sorun değil (endüstride 60 °C'+AP+'de haftalarca tutulur); şartlar: kapalı, paslanmaz, karanlık tank; haftalık boşalt-yıka; termostat 45 (daha sıcak = daha hızlı acılaşma).',82,5.4,'#333')
yy=para(XC+14,yy+2,('1 HAFTA YETER: 4 L tank = %d gün. Eleman haftalık turunda tankı doldurur, tenekeyi SERVICE'+AP+'te tutar. Makinede yağ stoğu tutmaya gerek yok → OVEN kolonunun altında 40 cm boşaldı.') % round(GUN_TANK),82,5.4,AMB)

# ================= D · SATIN ALMA SEÇENEKLERİ =================
XD,YD,WD,HD = 930,510,490,220
rc(XD,YD,WD,HD,1.4,4,'#111',None,'#fcfdff')
tx(XD+14,YD+22,'D · YAĞ ÜNİTESİ SATIN ALINABİLİR Mİ? — üç yol',10,'start','bold')
yy=YD+40
for a_,b_,c_,d_ in [('1 HAZIR (ABD)','Gold Medal 2496: torba-kutu tereyağı/sadeyağ dispenseri, sıcak hava 52–54 °C, elektrikli pompa (düğme → BEYİN rölesi), 310 W, 56×41×61 cm.','ABD (katom.com); önceki notumuz ~1.300 $, teyit edilecek; Türkiye'+AP+'de yok.','Uyarlama: teneke dolum adaptörü + nozül + çek valf.'),
                     ('2 UCUZ (Çin)','Alibaba ısıtmalı elektrikli pompalı sos dispenseri, 2–3 L, dokunmatik, porsiyon ayarlı.','≈ 185 $ + nakliye + gümrük.','Uyarlama: pompa rölesi + nozül + ısıtmalı hat; kalite belirsiz, pilot için.'),
                     ('3 YAPTIR (Türkiye) — ÖNERİ','B kesiti: 4 L paslanmaz tank + 100 W ısıtıcı + termostat + 24 V gıda tipi dişli pompa + ısıtma şeridi + 90° koni nozül + çek valf.','Entegratör; parçalar 8–12 bin TL + işçilik. Türkiye'+AP+'de hazır otomatik ürün yok (basmalı sos pompaları manuel, ~3 bin TL).','BEYİN doğrudan sürer, kolona gömülü, mini-CIP tahliyeli.'),
                     ('4 ENDÜSTRİYEL','Fırıncılık hattı püskürtme üniteleri (Sinobake, Farhat, OVA, Spray Dynamics).','Çin/İtalya/ABD, 1–3 m konveyörlü, 5–20 bin $.','Bize büyük; fikir kaynağı.')]:
    tx(XD+14,yy,a_,5.8,'start','bold','#111'); yy+=9
    yy=para(XD+14,yy,b_+' '+c_+' '+d_,88,5.1,'#333')+4

# ================= E · KONTROL =================
XE,YE,WE,HE = 40,750,1380,250
rc(XE,YE,WE,HE,1.4,4,'#111',None,'#fff')
tx(XE+14,YE+22,'E · KONTROL · BEYİN BAĞLANTISI · AÇIK',10,'start','bold')
notes=[('② FIRIN KAVİTESİ ÇÖZÜLÜYOR: Omake hazne 40×40×10 → tepsi Ø32 + kulp 6 = 38 ≤ 40 ✓ (kulp 12 ile 44 sığmazdı). Karar: kulp 6 cm — robot_tepsi_el v2'+AP+'ye işlenecek. Hazne yüksekliği 10: tepsi 1 + pide 3–4 ✓.',GRN,'bold'),
       ('FIRIN: Omake FPZ01.E21 çift kat, 64×60×56, 57 kg, 4,8 kW 400 V (kat başına 2,4), 400 °C, refrakter taş, alt/üst termostat, camlı kapak ×2 — 40.169 TL (Cafemarkt, 6 Eyl). Alternatif Atalay APF-40-2 (65×51×50, 7 kW, 49.077 TL).','#333',''),
       ('BEYİN: her kapak → aktüatör + 2 switch; her kat → termokupl + SSR (fırının termostatı yedek); "kat hazır" = taş ≥ set −15 °C; durumlar KAPALI / ÖN ISITMA (açılıştan 20–25 dk önce) / BEKLEME 340 / EKO 250 / PİŞİRME (sabit süre); üst kat yalnız pik/kuyrukta.','#333',''),
       ('SPREY: pompa rölesi + tank termostatı + şamandıra (yağ az → eleman ekranı); atım 4 ml (reçeteye göre 3–5); tepsi 1 sn durur; nozül ile pide arası 15 → Ø30 iz. Gün sonu mini-CIP otomatik (sıcak su hattı SERVICE'+AP+'ten).',AMB,''),
       ('AÇIK: Gold Medal 2496 güncel fiyat/ithalat mı, entegratör yapımı mı (öneri: yaptır) · nozül tipi pilotu (koni mi, 3 nozül fan mı) · sadeyağ tedarik (teneke 16 kg) · kolon altındaki 40 cm boşluk (2. ünite / pano) · HAT v48'+AP+'de OVEN bloğu bu dizilime çekilecek.',RED,'bold')]
yy=YE+42
for s,c,fw in notes: yy=para(XE+14,yy,s,225,5.8,c,fw)+3
tx(W-40,H-10,'AUTOKITCH · arastirma/4_OVEN/ist4_oven_detay_v2 · 6 Eyl 2026',7,'end','',GRY)
o.append('</svg>')
svg=chr(10).join(o)
xml.dom.minidom.parseString(svg.encode('utf-8'))
out=r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\4_OVEN\ist4_oven_detay_v2.svg"
io.open(out,'w',encoding='utf-8').write(svg)
print('yazildi + XML gecerli | doz %.0f ml · %.2f L/gun · hafta %.1f L · tank %d gun · atim %.2f s · iz %.0f cm' % (DOZ_ML,LT_GUN,HAFTA_L,round(GUN_TANK),ATIM_S,IZ_D))
