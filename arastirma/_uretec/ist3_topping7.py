# -*- coding: utf-8 -*-
# IST.3 TOPPING v7 — HAFTALIK TEDARIK KURGUSU (Kemal, 3 Eyl 2026):
# 3 taban x tek yukseklik 25 cm (BUYUK 35x42 kasar / ORTA 35x21 sucuk / KUCUK 17x21 kavurma-kusbasi), ust kat 70x42 tam dolu;
# SOGUTMA + ELEKTRIK EN USTTE (Kemal: erisilebilirlik); 4 cikis TABLA EKSENINDE (+-3 cm) -> tabla kayar+doner, merkez dahil spiral;
# altta GECIS RAFI (2 kat, robot takas); buzluk YOK — donmus kavurma/kusbasi STORE buzlugunda.
import io, math

E = []
def ln(x1,y1,x2,y2,w=1.4,c='#111',dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    E.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s/>' % (x1,y1,x2,y2,c,w,d))
def rc(x,y,w_,h,sw=1.4,rx=0,c='#111',dash=None,fill='none'):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    E.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,w_,h,rx,fill,c,sw,d))
def ci(cx,cy,r,sw=1.4,c='#111',dash=None,fill='none'):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    E.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (cx,cy,r,fill,c,sw,d))
def el(cx,cy,rx,ry,sw=1.4,c='#111',dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    E.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="none" stroke="%s" stroke-width="%s"%s/>' % (cx,cy,rx,ry,c,sw,d))
def tx(x,y,s,fs=11,a='middle',w='',col='#111'):
    fw = ' font-weight="%s"' % w if w else ''
    E.append('<text x="%.1f" y="%.1f" text-anchor="%s" font-size="%s" fill="%s" font-family="Arial"%s>%s</text>' % (x,y,a,fs,col,fw,s))
def not_(x,y,s,a='middle',c='#555'): tx(x,y,s,10,a,'',c)
def arr(x1,y1,x2,y2,w=1.8,c='#1d7a4f'):
    ln(x1,y1,x2,y2,w,c)
    a = math.atan2(y2-y1,x2-x1)
    for da in (2.6,-2.6):
        ln(x2,y2,x2-9*math.cos(a+da),y2-9*math.sin(a+da),w,c)
def oy(x1,x2,y,cm):
    ln(x1,y,x2,y,1,'#b3452b'); ln(x1,y-5,x1,y+5,1,'#b3452b'); ln(x2,y-5,x2,y+5,1,'#b3452b')
    tx((x1+x2)/2,y-6,cm,11,'middle','bold','#b3452b')
def ox(x,y1,y2,cm,side='l'):
    ln(x,y1,x,y2,1,'#b3452b'); ln(x-5,y1,x+5,y1,1,'#b3452b'); ln(x-5,y2,x+5,y2,1,'#b3452b')
    xx = x-9 if side=='l' else x+9
    E.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#b3452b" font-family="Arial" transform="rotate(-90 %.1f %.1f)">%s</text>' % (xx,(y1+y2)/2,xx,(y1+y2)/2,cm))

W, H = 1560, 1180
tx(40,44,'İSTASYON 3 — TOPPING · DETAY v7 (HAFTALIK tedarik · 3 kaset tabanı × tek yükseklik 25 · soğutma EN ÜSTTE · çıkışlar tabla ekseninde)',17,'start','bold')
tx(40,68,'Üstten aşağı: TEKNİK BÖLME (soğutma 25 + elektrik 14 — erişim üstten) → KASET KATI 70×42 tam dolu (kaşar 35×42 · sucuk 35×21 · kavurma 17×21 · kuşbaşı 17×21) → çark + motor ×4, HER BİRİNİN KENDİ ÇIKIŞI → DÖNER+KAYAR TABLA → GEÇİŞ RAFI 2 kat (robot takas) · buzluk YOK',10.5,'start','','#555')

# ================= ON GORUNUS =================
S = 0.46
def px(mm): return mm*S
X0, Y0 = 120, 130
GW, GH, AYAK = 700, 1800, 120
YT = Y0+px(GH); YZ = YT+px(AYAK)
tx(X0+px(350),Y0-44,'ÖN GÖRÜNÜŞ (robot tarafı)',12.5,'middle','bold')
rc(X0,Y0,px(GW),px(GH),2.2,5)
rc(X0+12,YT,12,px(AYAK)); rc(X0+px(GW)-24,YT,12,px(AYAK))
ln(X0-40,YZ,X0+px(GW)+40,YZ,2)

def kaset(x,y,w,h,ad1,ad2,dash=None,c='#111',fs=9.5):
    rc(x,y,w,h,1.6,3,c,dash)
    rc(x+w-px(20),y+px(70),px(16),px(80),1.2,2,c,dash)   # kulp (yan) = robot tutamagi
    if dash:
        tx(x+w/2,y-4,ad1+' '+ad2,7.8,'middle','bold',c)
    else:
        tx(x+w/2,y+h/2+2,ad1,fs,'middle','bold',c)
        tx(x+w/2,y+h/2+16,ad2,8.2,'middle','',c)

# --- TEKNIK BOLME EN USTTE: SOGUTMA y 10-260 + ELEKTRIK y 270-400
tx(X0+px(350),Y0+px(38),'SOĞUTMA GRUBU (ÜSTTE) — 25 cm · 1/8 HP ~150 W · +3 °C tüm kabin · BUZLUK YOK',9.5,'middle','bold')
rc(X0+px(60),Y0+px(60),px(180),px(170),1.4,3)
ci(X0+px(150),Y0+px(145),px(55),1.2)
tx(X0+px(150),Y0+px(150),'kompresör',8)
rc(X0+px(270),Y0+px(60),px(200),px(170),1.4,3)
tx(X0+px(370),Y0+px(150),'kondenser',8)
rc(X0+px(500),Y0+px(60),px(140),px(170),1.4,3)
ci(X0+px(570),Y0+px(145),px(45),1.1)
for k in range(4):
    a=k*math.pi/2+0.4
    ln(X0+px(570),Y0+px(145),X0+px(570)+px(40)*math.cos(a),Y0+px(145)+px(40)*math.sin(a),1.1)
tx(X0+px(570),Y0+px(150)+px(70),'fan',8)
tx(X0+px(350),Y0+px(255),'sıcak hava üstten atılır · servis üstten, kabin açılmadan (üstten motorlu dolap gibi)',8.5,'middle','','#555')
ln(X0+px(15),Y0+px(268),X0+px(685),Y0+px(268),1.2,'#111','7,5')
tx(X0+px(350),Y0+px(295),'ELEKTRİK BÖLMESİ (ÜSTTE) — PLC I/O · 4 step sürücü · 24 V güç · tabla sürücüleri',9.5,'middle','bold')
rc(X0+px(50),Y0+px(312),px(150),px(75),1.3,2); tx(X0+px(125),Y0+px(356),'PLC I/O',8.5)
for i in range(4):
    rc(X0+px(230+i*70),Y0+px(312),px(55),px(75),1.2,2); tx(X0+px(257+i*70),Y0+px(356),'S%d'%(i+1),8)
rc(X0+px(530),Y0+px(312),px(120),px(75),1.3,2); tx(X0+px(590),Y0+px(356),'24V PSU',8.5)
ln(X0+px(15),Y0+px(405),X0+px(685),Y0+px(405),1.6,'#111')
tx(X0+px(350),Y0+px(425),'— izoleli tavan: soğuk bölge başlar —',8.5,'middle','','#888')

# --- KASET KATI y 440-690 (25 cm) — kasar sol, sucuk sag on, kavurma+kusbasi sag arka (kesik)
KY0 = 440
kaset(X0+px(355),Y0+px(KY0-10),px(165),px(250),'KAVURMA','arka','5,4','#888')
kaset(X0+px(525),Y0+px(KY0-10),px(165),px(250),'KUŞBAŞI','arka','5,4','#888')
kaset(X0+px(10),Y0+px(KY0),px(335),px(250),'KAŞAR A · 35×42×25','15 kg = 2,3 gün · 37 L')
kaset(X0+px(355),Y0+px(KY0),px(335),px(250),'SUCUK · 35×21×25 (ön)','10 kg = HAFTALIK · 18 L')
# koniler -> carklar (cikislar tabla ekseninde: kasar 300 / kavurma 390 / sucuk 455 / kusbasi 535)
ln(X0+px(15),Y0+px(KY0+252),X0+px(255),Y0+px(KY0+300),1.4); ln(X0+px(340),Y0+px(KY0+252),X0+px(345),Y0+px(KY0+300),1.4)
ln(X0+px(360),Y0+px(KY0+252),X0+px(410),Y0+px(KY0+300),1.4); ln(X0+px(685),Y0+px(KY0+252),X0+px(500),Y0+px(KY0+300),1.4)

# --- CARKLAR + MOTOR y 740-930
CY = KY0+355
for cx0,r,sgn in ((300,55,-1),(455,40,1)):
    cy = Y0+px(CY)
    ci(X0+px(cx0),cy,px(r),1.8)
    for k in range(6):
        a=k*math.pi/3
        ln(X0+px(cx0),cy,X0+px(cx0)+px(r)*math.cos(a),cy+px(r)*math.sin(a),1.1)
    mx = X0+px(cx0+sgn*(r+60)) - (px(50) if sgn<0 else 0)
    rc(mx,cy-px(20),px(50),px(40),1.4,2)
    tx(mx+px(25),cy+5,'M',10,'middle','bold')
    ln(X0+px(cx0+sgn*r),cy,X0+px(cx0+sgn*(r+10)),cy,2)
    ln(X0+px(cx0-18),Y0+px(CY+60),X0+px(cx0-18),Y0+px(CY+120),1.5); ln(X0+px(cx0+18),Y0+px(CY+60),X0+px(cx0+18),Y0+px(CY+120),1.5)
    for dy in (70,93,115):
        rc(X0+px(cx0)-px(4),Y0+px(CY+dy),px(8),px(8),.8,1,'#8a6a3a')
for cx0 in (390,535):
    ci(X0+px(cx0),Y0+px(CY-20),px(35),1.1,'#999','5,4')
    ln(X0+px(cx0-14),Y0+px(CY+15),X0+px(cx0-14),Y0+px(CY+90),1,'#999','4,3'); ln(X0+px(cx0+14),Y0+px(CY+15),X0+px(cx0+14),Y0+px(CY+90),1,'#999','4,3')
tx(X0+px(120),Y0+px(CY+70),'kaşar çarkı BÜYÜK',8.5,'middle','bold','#b3452b')
tx(X0+px(120),Y0+px(CY+87),'(80 g/porsiyon)',8,'middle','','#b3452b')
not_(X0+px(350),Y0+px(CY+150),'4 AYRI ÇIKIŞ, hepsi TABLA EKSENİNDE (x 30·39·45,5·53,5) — ortak boru YOK',c='#b3452b')

# --- TABLA + MOTOR y 960-1180
TY = CY+205
el(X0+px(350),Y0+px(TY),px(140),px(13),1.1)
tx(X0+px(500),Y0+px(TY+5),'pide Ø28',8.5,'start')
el(X0+px(350),Y0+px(TY+28),px(180),px(20),1.8)
tx(X0+px(350)+px(195),Y0+px(TY+32),'TABLA Ø36',9,'start','bold')
rc(X0+px(60),Y0+px(TY+60),px(580),px(30),1.4,2)                      # kizak
rc(X0+px(280),Y0+px(TY+52),px(140),px(22),1.3,2)                     # araba
arr(X0+px(430),Y0+px(TY+75),X0+px(600),Y0+px(TY+75),1.6,'#1a49b8'); arr(X0+px(270),Y0+px(TY+75),X0+px(100),Y0+px(TY+75),1.6,'#1a49b8')
rc(X0+px(190),Y0+px(TY+105),px(320),px(60),1.5,3)
tx(X0+px(350),Y0+px(TY+132),'TABLA MOTORLARI',9.5,'middle','bold')
tx(X0+px(350),Y0+px(TY+152),'M dönme + M kayma (merkez 18 → 52 cm)',8.5)

# --- GECIS RAFI y 1190-1790 (2 kat) — robot takas rafi
GY = TY+195
ln(X0+px(15),Y0+px(GY),X0+px(685),Y0+px(GY),1.2,'#111','7,5')
tx(X0+px(350),Y0+px(GY+20),'GEÇİŞ RAFI (robot takas) — kat A',9.5,'middle','bold','#1a49b8')
kaset(X0+px(10),Y0+px(GY+35),px(335),px(250),'KAŞAR B','dolu, +3 — sıradaki',fs=9)
kaset(X0+px(355),Y0+px(GY+35),px(335),px(250),'KAŞAR C','dolu, +3',fs=9)
tx(X0+px(175),Y0+px(GY+312),'kat B',9.5,'middle','bold','#1a49b8')
kaset(X0+px(355),Y0+px(GY+312),px(165),px(250),'ÇÖZÜLME 1','arka','5,4','#1a49b8')
kaset(X0+px(525),Y0+px(GY+312),px(165),px(250),'ÇÖZÜLME 2','arka','5,4','#1a49b8')
kaset(X0+px(10),Y0+px(GY+325),px(335),px(250),'KAŞAR D','dolu, +3',fs=9)
kaset(X0+px(355),Y0+px(GY+325),px(335),px(250),'SUCUK yedek (ön)','eleman gününde dolu takılır',fs=9)
tx(X0+px(350),Y0+px(GY+598),'kat A: 2 büyük · kat B: 1 büyük + 1 orta + 2 küçük (çözülme) · biten BOŞ kaset de buraya iner',8.5,'middle','','#333')

# olculer
oy(X0,X0+px(GW),YZ+30,'70')
ox(X0-34,Y0,YT,'180'); ox(X0-34,YT,YZ,'12'); ox(X0-70,Y0,YZ,'192')
xr = X0+px(GW)+22
ox(xr,Y0+px(10),Y0+px(265),'soğutma 25',side='r'); ox(xr,Y0+px(270),Y0+px(405),'elektrik 14',side='r')
ox(xr,Y0+px(KY0),Y0+px(KY0+250),'kaset 25',side='r'); ox(xr,Y0+px(KY0+255),Y0+px(CY+125),'çark+çıkış 22',side='r')
ox(xr,Y0+px(TY-10),Y0+px(TY+170),'tabla+motor 18',side='r'); ox(xr,Y0+px(GY),Y0+px(GY+610),'geçiş rafı 61',side='r')

# ================= UST GORUNUM (kaset kati + tabla ekseni) =================
S2 = 0.5
def p2(mm): return mm*S2
X2, Y2 = 760, 150
tx(X2+p2(350),Y2-36,'ÜST GÖRÜNÜM (kaset katı) — 70 × 42 · TAM DOLU · çıkışlar tabla ekseninde',12.5,'middle','bold')
rc(X2,Y2,p2(700),p2(420),2.2,4)
def tk(kx,ky,kw,kh,ad,alt,kulp=True):
    rc(X2+p2(kx)+3,Y2+p2(ky)+3,p2(kw)-6,p2(kh)-6,1.6,3)
    if kulp: rc(X2+p2(kx)+p2(kw)-p2(28),Y2+p2(ky)+p2(kh/2)-p2(30),p2(20),p2(60),1.2,2)
    tx(X2+p2(kx)+p2(kw/2)-(p2(12) if kulp else 0),Y2+p2(ky)+p2(kh/2)-2,ad,9.5,'middle','bold')
    tx(X2+p2(kx)+p2(kw/2)-(p2(12) if kulp else 0),Y2+p2(ky)+p2(kh/2)+12,alt,8.2)
tk(0,0,350,420,'KAŞAR','35 × 42')
tk(350,0,170,210,'KAVURMA','17 × 21')
tk(520,0,170,210,'KUŞBAŞI','17 × 21')
tk(350,210,350,210,'SUCUK','35 × 21')
# tabla ekseni + travel (merkez 180..520, tabla O36)
ln(X2+p2(20),Y2+p2(210),X2+p2(680),Y2+p2(210),1.3,'#1a49b8','6,4')
ci(X2+p2(180),Y2+p2(210),p2(180),1.1,'#1a49b8','3,3')
ci(X2+p2(520),Y2+p2(210),p2(180),1.1,'#1a49b8','3,3')
arr(X2+p2(200),Y2+p2(395),X2+p2(500),Y2+p2(395),1.4,'#1a49b8'); arr(X2+p2(500),Y2+p2(395),X2+p2(200),Y2+p2(395),1.4,'#1a49b8')
tx(X2+p2(350),Y2+p2(385),'tabla merkezi 18 → 52',8,'middle','','#1a49b8')
# cikislar (kirmizi) — her biri kendi kasetinin altinda, eksene ±3 cm
for cx_,cy_ in ((300,210),(390,185),(455,240),(535,185)):
    ci(X2+p2(cx_),Y2+p2(cy_),p2(18),1.4,'#b3452b','3,2')
    ci(X2+p2(cx_),Y2+p2(cy_),2.2,1,'#b3452b',None,'#b3452b')
tx(X2+p2(350),Y2+p2(455),'kırmızı: 4 ÇIKIŞ, tabla eksenine ±3 cm (rotor kasetin ALTINDA, koni içeri çeker) · mavi: tabla Ø36 travel',9.5,'middle','','#1a49b8')
tx(X2+p2(350),Y2+p2(478),'tabla çıkışın altına kayar + döner → çıkış pide üstünde MERKEZDEN KENARA spiral çizer (r 0-3 → 14 cm)',9.5,'middle','','#b3452b')
oy(X2,X2+p2(350),Y2-14,'35'); oy(X2+p2(350),X2+p2(520),Y2-14,'17'); oy(X2+p2(520),X2+p2(700),Y2-14,'18')
ox(X2-16,Y2,Y2+p2(210),'21'); ox(X2-16,Y2+p2(210),Y2+p2(420),'21')

# ================= KASET AILESI =================
KY = Y2+p2(420)+96
tx(X2,KY,'KASET AİLESİ — 3 taban × tek yükseklik 25 cm (ölçekli)',12.5,'start','bold')
fam = [(0,350,420,'BÜYÜK 35×42×25 · 37 L','kaşar 15 kg = 2,3 gün','4 kaset (1 çalışan + 3 dolu)'),
       (145,350,210,'ORTA 35×21×25 · 18 L','sucuk 10 kg = HAFTALIK','2 kaset (1 çalışan+1 yedek)'),
       (285,170,210,'KÜÇÜK 17×21×25 · 9 L','kavurma/kuşbaşı 3,5 kg','= 2,3 gün · 4+4 kaset','(1 taze+2 donmuş+1 boş)')]
S3 = 0.36
for f in fam:
    fx,fw,fh,a1,a2,a3 = f[:6]
    x = X2+fx; y = KY+18
    rc(x,y,fw*S3,fh*S3,1.5,3)
    rc(x+fw*S3-p2(16),y+fh*S3/2-p2(20),p2(12),p2(40),1.1,2)
    yb = KY+18+420*S3
    tx(x,yb+16,a1,9.5,'start','bold')
    tx(x,yb+30,a2,8.8,'start','','#333')
    tx(x,yb+44,a3,8.8,'start','','#1d7a4f')
    if len(f) > 6: tx(x,yb+58,f[6],8.8,'start','','#1d7a4f')
tx(X2,KY+18+420*S3+84,'Toplam 14 kaset · haftalık dolum: kaşar 3 × 15 · sucuk 1 × 10 ·',10,'start','','#333')
tx(X2,KY+18+420*S3+99,'kavurma 3 × 3,5 · kuşbaşı 3 × 3,5 kg',10,'start','','#333')
tx(X2,KY+18+420*S3+118,'kural 1: kaset sayısı = haftalık parça + 1 (o an çalışan)',10,'start','bold','#333')
tx(X2,KY+18+420*S3+133,'kural 2: kaset boyu = +3\'te güvenli gün × günlük tüketim',10,'start','bold','#333')

# ================= NOTLAR =================
NX = 1192; NY = 150
tx(NX,NY,'HAFTALIK DÖNGÜ (eleman haftada 1 gelir):',12.5,'start','bold')
nots = [
 ('GÜN 0 — eleman: boşları toplar, yıkar,','#1d7a4f'),
 ('  poşetten kasete doldurur (poşette stok YOK):','#1d7a4f'),
 ('  kaşar 3 dolu → geçiş rafı (üste robot takar);','#1d7a4f'),
 ('  sucuk yedek → geçiş rafı; kavurma+kuşbaşı','#1d7a4f'),
 ('  1 taze → geçiş rafı, 2\'şer donmuş → STORE −18','#1d7a4f'),
 ('  Eleman ÜST KATA hiç uzanmaz — robot taşır.','#1d7a4f'),
 ('ROBOT — kaset "boş" sensörü → üstteki boşu','#1a49b8'),
 ('  çıkarır, geçiş rafındaki doluyu takar, boşu','#1a49b8'),
 ('  boş yuvaya koyar. Saat önemsiz (1 saatte de).','#1a49b8'),
 ('  Donmuş kaseti bitişten 1 gün önce STORE\'dan','#1a49b8'),
 ('  ÇÖZÜLME yuvasına indirir (+3, 24 saat).','#1a49b8'),
 ('SAAT KURALI — her kasetin takılma saati BEYİN\'de:','#b3452b'),
 ('  kaşar 14 g · sucuk 7 g · kavurma/kuşbaşı 3,5 g','#b3452b'),
 ('  Süre dolan kaset dolu olsa da çıkar (≤1 kg fire).','#b3452b'),
 ('  Donmuş kasetin saati DURUR → haftaya devreder.','#b3452b'),
 ('UYGULAMA MESAJI — BEYİN tüketimi ölçer:','#333'),
 ('  "bu hafta kaşar 42 · sucuk 9 · kavurma 12 · kuşbaşı 8 kg"','#666'),
 ('  Stok biterse kiosk o çeşidi kapatır (hamur gibi).','#666'),
 ('','#333'),
 ('NASIL ÇALIŞIR (pide başına ~20-30 sn):','#333'),
 ('1. Kol basılmış tabanı TABLAYA koyar','#333'),
 ('2. BEYİN reçete: kaşar 4 cep; karışık +3+3 cep','#333'),
 ('3. Tabla ilgili ÇIKIŞIN altına kayar + döner:','#333'),
 ('   merkezden kenara spiral, orta da dış da dolar','#666'),
 ('4. Kol pideyi fırına götürür','#333'),
 ('','#333'),
 ('KARARLAR (v7):','#333'),
 ('· SOĞUTMA + ELEKTRİK EN ÜSTTE (Kemal): servis','#b3452b'),
 ('  üstten, kaset katı 40 cm aşağı iner → robot ve','#b3452b'),
 ('  eleman erişimi kolay; sıcak hava yukarı atılır','#b3452b'),
 ('· 4 çıkış tabla ekseninde ±3 cm: rotor kasetin','#333'),
 ('  altında, koni malzemeyi eksene çeker (boru yok)','#666'),
 ('· Kaset boyu = raf ömrü × tüketim → 3 taban,','#333'),
 ('  tek yükseklik 25; üst kat 70×42 SIFIR boşluk','#666'),
 ('· Kaşar 3 parça × 15 kg: hafif + topaklanma ↓','#333'),
 ('· Sucuk tek haftalık kaset (7 gün dayanır)','#333'),
 ('· Kavurma/kuşbaşı 2,3 günlük: 1 gün çözülme +','#333'),
 ('  2,3 gün çalışma = 3,3 gün ≤ raf ömrü','#666'),
 ('· TOPPING\'e buzluk YOK — STORE\'un −18\'i kullanılır','#b3452b'),
 ('· Alt bölme "yedek deposu" değil GEÇİŞ RAFI','#333'),
 ('· Kaset kulpu = robot tutamağı; kobot ≥12 kg','#333'),
 ('  (UR16e / CRX-20 sınıfı) — robot turunda','#666'),
 ('· Kabin derinliği 42 iç → ~55 dış (v6: 84)','#666'),
]
yy = NY+22
for s_,c_ in nots:
    if s_: tx(NX,yy,s_,10.2,'start','bold' if s_.endswith(':') else '',c_)
    yy += 17.5

tx(W-24,H-14,'AUTOKITCH · ist3_topping_detay_v7',10,'end','','#999')
svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d"><rect width="%d" height="%d" fill="#ffffff"/>%s</svg>' % (W,H,W,H,W,H,''.join(E))
OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\ist3_topping_detay_v7.svg"
io.open(OUT,'w',encoding='utf-8').write(svg)
print('yazildi:', OUT)
