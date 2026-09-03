# -*- coding: utf-8 -*-
# IST.3 TOPPING v3 — KEMAL KROKISI (376a654b/244412fb): kaset hazneler 2x2 sifir bosluk,
# hucreli cark+motor, doner-kayar tabla+motor, 4 DOLU YEDEK kaset, altta sogutma grubu
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
tx(40,44,'İSTASYON 3 — TOPPING · DETAY v5 (soğutma gerçek boyut 25 cm · kasetler 35 cm · elektrik bölmesi)',17,'start','bold')
tx(40,68,'Üstten aşağı: 4 KASET HAZNE (2 önde 2 arkada, sıfır boşluk) → hücreli çark + motor (×4), HER BİRİNİN KENDİ ÇIKIŞI → DÖNER+KAYAR TABLA + motoru → 4 DOLU YEDEK KASET → SOĞUTMA 25 (tezgah altı buzdolabı sınıfı, +3 °C) → ELEKTRİK BÖLMESİ',10.5,'start','','#555')

# ================= ON GORUNUS =================
S = 0.46
def px(mm): return mm*S
X0, Y0 = 120, 130
GW, GH, AYAK = 700, 1850, 120
YT = Y0+px(GH); YZ = YT+px(AYAK)
tx(X0+px(350),Y0-44,'ÖN GÖRÜNÜŞ (robot tarafı)',12.5,'middle','bold')
rc(X0,Y0,px(GW),px(GH),2.2,5)
rc(X0+12,YT,12,px(AYAK)); rc(X0+px(GW)-24,YT,12,px(AYAK))
ln(X0-40,YZ,X0+px(GW)+40,YZ,2)

def kaset(x,y,w,h,ad1,ad2,dash=None,c='#111'):
    rc(x,y,w,h,1.6,3,c,dash)
    rc(x+w-px(22),y+px(40),px(18),px(60),1.2,2,c,dash)   # kulp (yan)
    if dash:
        tx(x+w/2,y+px(22),ad1+' '+ad2,8.5,'middle','bold',c)
    else:
        tx(x+w/2,y+h/2+4,ad1,9.5,'middle','bold',c)
        tx(x+w/2,y+h/2+18,ad2,8.5,'middle','',c)

# --- KASET HAZNELER y 40-300 (arka ikisi kesik, hafif yukari/sag)
kaset(X0+px(60),Y0+px(28),px(300),px(350),'H3 KAVURMA','(arka)','5,4','#888')
kaset(X0+px(400),Y0+px(28),px(300),px(350),'H4 KUŞBAŞI','(arka)','5,4','#888')
kaset(X0+px(25),Y0+px(60),px(325),px(350),'H1 KÜP SUCUK','kaset 35×42×35 · 4-6 kg')
kaset(X0+px(350),Y0+px(60),px(325),px(350),'H2 KAŞAR','kaset 35×42×35 · 4-6 kg')
not_(X0+px(350),Y0+px(40)-30,'KASET HAZNELER — üstten kaldırılır (kulp), birbirine SIFIR boşluk',c='#333')
# koniler
ln(X0+px(30),Y0+px(410),X0+px(235),Y0+px(460),1.4); ln(X0+px(345),Y0+px(410),X0+px(305),Y0+px(460),1.4)
ln(X0+px(355),Y0+px(410),X0+px(395),Y0+px(460),1.4); ln(X0+px(670),Y0+px(410),X0+px(465),Y0+px(460),1.4)

# --- HUCRELI CARK + MOTOR y 360-480
for cx0,sgn in ((270,-1),(430,1)):
    ci(X0+px(cx0),Y0+px(520),px(45),1.8)
    for k in range(6):
        a=k*math.pi/3
        ln(X0+px(cx0),Y0+px(520),X0+px(cx0)+px(45)*math.cos(a),Y0+px(520)+px(45)*math.sin(a),1.1)
    mx = X0+px(cx0+sgn*105) - (px(50) if sgn<0 else 0)
    rc(mx,Y0+px(500),px(50),px(40),1.4,2)
    tx(mx+px(25),Y0+px(526),'M',10,'middle','bold')
    ln(X0+px(cx0+sgn*45),Y0+px(520),X0+px(cx0+sgn*55),Y0+px(520),2)
    # KENDI CIKIS AGZI — dogrudan cark altinda, boru yok
    ln(X0+px(cx0-20),Y0+px(565),X0+px(cx0-20),Y0+px(620),1.5); ln(X0+px(cx0+20),Y0+px(565),X0+px(cx0+20),Y0+px(620),1.5)
    for dy in (535,560,585):
        rc(X0+px(cx0)-px(4),Y0+px(dy),px(8),px(8),.8,1,'#8a6a3a')
# arka carklar + cikislari (kesik)
for cx0 in (300,460):
    ci(X0+px(cx0),Y0+px(500),px(45),1.1,'#999','5,4')
    ln(X0+px(cx0-20),Y0+px(545),X0+px(cx0-20),Y0+px(600),1,'#999','4,3'); ln(X0+px(cx0+20),Y0+px(545),X0+px(cx0+20),Y0+px(600),1,'#999','4,3')
tx(X0+px(350),Y0+px(445),'4 çark KASETLERİN İÇ KENARINDA',8.5,'middle','bold','#b3452b')
not_(X0+px(350),Y0+px(712),'4 AYRI ÇIKIŞ — ortak nozül/boru YOK: karışma yok, tıkanma yok',c='#b3452b')

# --- TABLA + MOTOR y 620-820
el(X0+px(350),Y0+px(740),px(140),px(13),1.1)
tx(X0+px(500),Y0+px(745),'pide Ø28',8.5,'start')
el(X0+px(350),Y0+px(768),px(200),px(22),1.8)
tx(X0+px(350)+px(215),Y0+px(772),'TABLA Ø40',9,'start','bold')
rc(X0+px(90),Y0+px(800),px(520),px(30),1.4,2)                       # kizak
rc(X0+px(280),Y0+px(792),px(140),px(22),1.3,2)                      # araba
arr(X0+px(430),Y0+px(815),X0+px(560),Y0+px(815),1.6,'#1a49b8'); arr(X0+px(270),Y0+px(815),X0+px(140),Y0+px(815),1.6,'#1a49b8')
rc(X0+px(190),Y0+px(850),px(320),px(70),1.5,3)
tx(X0+px(350),Y0+px(880),'TABLA MOTORLARI',9.5,'middle','bold')
tx(X0+px(350),Y0+px(900),'M dönme + M kayma (ileri-geri)',8.5)
not_(X0+px(350),Y0+px(950),'tabla AKTİF çıkışın altına kayar + döner → spiral kaplama (dış + orta dolar)',c='#1a49b8')

# --- YEDEK KASETLER y 900-1180
ln(X0+px(15),Y0+px(980),X0+px(685),Y0+px(980),1.2,'#111','7,5')
kaset(X0+px(60),Y0+px(1000),px(300),px(350),'YEDEK H3','(arka, dolu)','5,4','#888')
kaset(X0+px(400),Y0+px(1000),px(300),px(350),'YEDEK H4','(arka, dolu)','5,4','#888')
kaset(X0+px(25),Y0+px(1030),px(325),px(350),'YEDEK H1','dolu — takas için')
kaset(X0+px(350),Y0+px(1030),px(325),px(350),'YEDEK H2','dolu — takas için')
not_(X0+px(350),Y0+px(1415),'4 DOLU YEDEK KASET — eleman boşu çıkarır, doluyu takar; boşu yıkar-doldurur, buraya koyar',c='#333')

# --- SOGUTMA y 1440-1690 (25 cm — tezgah alti buzdolabi sinifi)
ln(X0+px(15),Y0+px(1435),X0+px(685),Y0+px(1435),1.2,'#111','7,5')
tx(X0+px(350),Y0+px(1470),'SOĞUTMA GRUBU — 25 cm · 1/8 HP ~150 W · +3 °C tüm kabin',9.5,'middle','bold')
rc(X0+px(60),Y0+px(1490),px(180),px(170),1.4,3)
ci(X0+px(150),Y0+px(1575),px(55),1.2)
tx(X0+px(150),Y0+px(1580),'kompresör',8)
rc(X0+px(270),Y0+px(1490),px(200),px(170),1.4,3)
tx(X0+px(370),Y0+px(1580),'kondenser',8)
rc(X0+px(500),Y0+px(1490),px(140),px(170),1.4,3)
ci(X0+px(570),Y0+px(1575),px(45),1.1)
for k in range(4):
    a=k*math.pi/2+0.4
    ln(X0+px(570),Y0+px(1575),X0+px(570)+px(40)*math.cos(a),Y0+px(1575)+px(40)*math.sin(a),1.1)
tx(X0+px(570),Y0+px(1580)+px(70),'fan',8)
not_(X0+px(350),Y0+px(1685),'hesap: hacim ~0,45 m³ · duvar 60 mm PU · ısı yükü &lt; 100 W — buz yok, sadece +3',c='#555')
# --- ELEKTRIK y 1700-1850
ln(X0+px(15),Y0+px(1700),X0+px(685),Y0+px(1700),1.2,'#111','7,5')
tx(X0+px(350),Y0+px(1730),'ELEKTRİK BÖLMESİ — PLC I/O · 4 step sürücü · 24 V güç · tabla sürücüleri',9.5,'middle','bold')
rc(X0+px(50),Y0+px(1750),px(150),px(80),1.3,2); tx(X0+px(125),Y0+px(1797),'PLC I/O',8.5)
for i in range(4):
    rc(X0+px(230+i*70),Y0+px(1750),px(55),px(80),1.2,2); tx(X0+px(257+i*70),Y0+px(1797),'S%d'%(i+1),8)
rc(X0+px(530),Y0+px(1750),px(120),px(80),1.3,2); tx(X0+px(590),Y0+px(1797),'24V PSU',8.5)

# olculer
oy(X0,X0+px(GW),YZ+30,'70')
ox(X0-34,Y0,YT,'185'); ox(X0-34,YT,YZ,'12'); ox(X0-70,Y0,YZ,'197')
xr = X0+px(GW)+22
ox(xr,Y0+px(28),Y0+px(410),'kaset 38',side='r'); ox(xr,Y0+px(460),Y0+px(690),'çark+nozül 23',side='r')
ox(xr,Y0+px(720),Y0+px(960),'tabla+motor 24',side='r'); ox(xr,Y0+px(1000),Y0+px(1430),'yedek 43',side='r'); ox(xr,Y0+px(1440),Y0+px(1690),'soğutma 25',side='r'); ox(xr,Y0+px(1700),Y0+px(1850),'elektrik 15',side='r')

# ================= UST GORUNUM =================
S2 = 0.5
def p2(mm): return mm*S2
X2, Y2 = 760, 150
tx(X2+p2(350),Y2-36,'ÜST GÖRÜNÜM (kaset katı) — 70 × 84',12.5,'middle','bold')
rc(X2,Y2,p2(700),p2(840),2.2,4)
kas = [(0,0,'H1 KÜP SUCUK'),(350,0,'H2 KAŞAR'),(0,420,'H3 KAVURMA'),(350,420,'H4 KUŞBAŞI')]
for kx,ky,ad in kas:
    rc(X2+p2(kx)+3,Y2+p2(ky)+3,p2(350)-6,p2(420)-6,1.6,3)
    rc(X2+p2(kx)+p2(350)-p2(40),Y2+p2(ky)+p2(170),p2(30),p2(80),1.3,2)   # kulp (sagda — Kemal krokisi)
    tx(X2+p2(kx)+p2(160),Y2+p2(ky)+p2(200),ad,10,'middle','bold')
    tx(X2+p2(kx)+p2(160),Y2+p2(ky)+p2(230),'35 × 42',8.5)
    # cikis (merkeze yakin kose) kesik
    ci(X2+p2(kx)+(p2(300) if kx==0 else p2(50)),Y2+p2(ky)+(p2(380) if ky==0 else p2(40)),p2(16),1.1,'#b3452b','3,2')
ci(X2+p2(350),Y2+p2(420),p2(200),1.3,'#1a49b8','7,5')
ln(X2+p2(350),Y2+p2(180),X2+p2(350),Y2+p2(660),1.2,'#1a49b8','2,4')
tx(X2+p2(350),Y2+p2(880),'kırmızı: 4 AYRI çıkış (kasetlerin iç köşesi, merkezden ~8 cm) · mavi: tabla Ø40 + kızak',9.5,'middle','','#1a49b8')
tx(X2+p2(350),Y2+p2(905),'4 kaset SIFIR boşluk — kulp sağda, üstten kaldırılır',9.5,'middle','','#555')
oy(X2,X2+p2(350),Y2-14,'35'); oy(X2+p2(350),X2+p2(700),Y2-14,'35')
ox(X2-16,Y2,Y2+p2(420),'42'); ox(X2-16,Y2+p2(420),Y2+p2(840),'42')

# ================= NOTLAR: NASIL CALISIR =================
NX = 1140; NY = 150
tx(NX,NY,'NASIL ÇALIŞIR:',12.5,'start','bold')
nots = [
 ('1. Kol basılmış tabanı TABLAYA koyar','#333'),
 ('2. BEYİN reçeteyi açar: kaşarlı = H2 4 cep;','#333'),
 ('   karışık = H1 3 + H2 4 + H3 3 cep','#666'),
 ('3. Tabla ilgili ÇIKIŞIN altına kayar + döner;','#333'),
 ('   o çark cep cep bırakır → spiral örtü','#666'),
 ('4. Kol pideyi fırına götürür (~20-30 sn)','#333'),
 ('','#333'),
 ('DOLUM / TEMİZLİK (eleman):','#1d7a4f'),
 ('· Kaset boşalınca uyarı → eleman kulptan','#1d7a4f'),
 ('  çıkarır, alttaki DOLU YEDEĞİ takar','#1d7a4f'),
 ('· Boş kaset bulaşıkta yıkanır, doldurulur,','#1d7a4f'),
 ('  yedek yuvasına konur — sıfır kesinti','#1d7a4f'),
 ('· Çark rotoru tek vida ile sökülür','#1d7a4f'),
 ('','#333'),
 ('KARARLAR:','#333'),
 ('· Tüm malzeme KÜP/PARÇA (Dominos):','#333'),
 ('  dilimleyici YOK, 4 hazne aynı mekanizma','#666'),
 ('· Her çarka ayrı step motor (×4)','#333'),
 ('· HER HAZNENİN KENDİ ÇIKIŞI (Kemal):','#b3452b'),
 ('  ortak boru yok → malzeme karışmaz,','#b3452b'),
 ('  tıkanacak boru yok, çıkış çarkla sökülür','#b3452b'),
 ('· Tüm kabin +3 °C — yağlı küp yapışmaz','#333'),
 ('· Soğutma GERÇEK boyut: 25 cm bant,','#333'),
 ('  tezgah altı buzdolabı motoru (1/8 HP);','#666'),
 ('  kazanılan yer → kaset 35 cm (4-6 kg)','#666'),
 ('  + elektrik bölmesi (PLC, 4 sürücü)','#666'),
 ('· Porsiyon = cep sayısı (kalibrasyon kolay)','#333'),
 ('· Kuşbaşı: soteli/yarı pişmiş (çiğ 2-3 dk','#b3452b'),
 ('  fırında pişmez) — T7','#b3452b'),
 ('· Pilot: Rosseto çarkı + step motor ile','#666'),
 ('  soğuk küp sucuk akış testi','#666'),
]
yy = NY+22
for s_,c_ in nots:
    if s_: tx(NX,yy,s_,10.5,'start','bold' if s_.endswith(':') else '',c_)
    yy += 19

tx(W-24,H-14,'AUTOKITCH · ist3_topping_detay_v5',10,'end','','#999')
svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d"><rect width="%d" height="%d" fill="#ffffff"/>%s</svg>' % (W,H,W,H,W,H,''.join(E))
OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\ist3_topping_detay_v5.svg"
io.open(OUT,'w',encoding='utf-8').write(svg)
print('yazildi:', OUT)
