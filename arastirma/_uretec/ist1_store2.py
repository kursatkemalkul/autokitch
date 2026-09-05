# -*- coding: utf-8 -*-
# IST.1 STORE — DETAY v2 (4 Eyl 2026): GERCEK KALINLIKLAR + 61'lik CEKMECE MODULLERI + ROBOT ERISIMI
# gövde PU 60 (+3) / 80 (−18 bandi, alt) · yatay izoleli ayirici 80 · cekmece onu izoleli 40 (+3) / 60 (−18) + conta
# ray: paslanmaz tam acilim 12,7 mm/yan (Accuride 3832 sinifi, 45 kg) + 1 mm pay · kutu 1,5 mm paslanmaz
# −18 bandi 2x61 modul: 4 hamur cekmecesi (1 tepsi = 20 top -> 80) + 2 kaset cekmecesi (2'ser kaset) · +3: sol 4 icecek + 1L, sag 8 taze
# dikey: kapak 20 + sogutma 220 + ust panel 60 + 8x105 + ayirici 80 + 2x105 + kaset 290 + alt panel 80 = 1800 (+50 pay) + ayak 120 = 197
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
def not_(x,y,s,a='middle',c='#555',fs=9.5): tx(x,y,s,fs,a,'',c)
def oy(x1,x2,y,cm,fs=10.5):
    ln(x1,y,x2,y,1,'#b3452b'); ln(x1,y-5,x1,y+5,1,'#b3452b'); ln(x2,y-5,x2,y+5,1,'#b3452b')
    tx((x1+x2)/2,y-6,cm,fs,'middle','bold','#b3452b')
def ox(x,y1,y2,cm,side='l',fs=10):
    ln(x,y1,x,y2,1,'#b3452b'); ln(x-5,y1,x+5,y1,1,'#b3452b'); ln(x-5,y2,x+5,y2,1,'#b3452b')
    xx = x-9 if side=='l' else x+9
    E.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="%s" font-weight="bold" fill="#b3452b" font-family="Arial" transform="rotate(-90 %.1f %.1f)">%s</text>' % (xx,(y1+y2)/2,fs,xx,(y1+y2)/2,cm))
def arr(x1,y1,x2,y2,w=1.6,c='#1d7a4f'):
    ln(x1,y1,x2,y2,w,c); a = math.atan2(y2-y1,x2-x1)
    for da in (2.6,-2.6): ln(x2,y2,x2-8*math.cos(a+da),y2-8*math.sin(a+da),w,c)

W, H = 1560, 1180
Bl, G, Rd, Gr = '#1a49b8', '#1d7a4f', '#b3452b', '#777'
PU = '#e9e4d6'   # PU panel dolgusu
tx(40,44,'İSTASYON 1 — STORE · DETAY v2 (gerçek kalınlıklar · 61 cm çekmece modülleri · alt buzluk 6 çekmeceye bölündü · robot erişimi)',17,'start','bold')
tx(40,68,'Gövde PU 60 (+3) / 80 (−18 bandı) · yatay izoleli ayırıcı 80 · çekmece önü izoleli 40 (+3) / 60 (−18) + conta · ray paslanmaz tam açılım 12,7 mm/yan (Accuride 3832 sınıfı, 45 kg) + 1 mm pay · kutu 1,5 mm paslanmaz · tepsi 53×65 derinlemesine',10.5,'start','','#555')

# ================= A) ON GORUNUS (S=0.46) =================
S = 0.46
def px(mm): return mm*S
X0, Y0 = 60, 150
GW, GH, AYAK = 1400, 1850, 120
YT = Y0+px(GH); YZ = YT+px(AYAK)
tx(X0+px(GW)/2,Y0-18,'ÖN GÖRÜNÜŞ — 19 çekmece, hepsi 61 cm modül · kapak yok',12.5,'middle','bold')
rc(X0,Y0,px(GW),px(GH),2,4)
rc(X0+14,YT,12,px(AYAK)); rc(X0+px(GW)-26,YT,12,px(AYAK)); ln(X0-40,YZ,X0+px(GW)+40,YZ,2)
# sogutma bolmesi (sac, izolesiz) 20-240
rc(X0+6,Y0+px(20),px(GW)-12,px(220),1.2,2)
for gx in (350,1050):
    ci(X0+px(gx),Y0+px(130),px(60),1.1); ln(X0+px(gx-42),Y0+px(88),X0+px(gx+42),Y0+px(172),.8); ln(X0+px(gx-42),Y0+px(172),X0+px(gx+42),Y0+px(88),.8)
not_(X0+px(700),Y0+px(60),'SOĞUTMA ×2 (sac bölme, izolesiz) — sol −18 grubu · sağ +3 grubu · üstten servis',fs=8.5)
# soguk govde: ust panel 60 (y 240-300), yan paneller 60 (+3 bolgesi), −18 bandi 80
Y3 = 300                       # +3 ic ust
rc(X0+6,Y0+px(240),px(GW)-12,px(60),1,0,'#111',None,PU)      # ust panel
rc(X0+6,Y0+px(240),px(60),px(1140),1,0,'#111',None,PU)        # sol panel +3
rc(X0+px(GW)-6-px(60),Y0+px(240),px(60),px(1140),1,0,'#111',None,PU)
rc(X0+px(690),Y0+px(300),px(20),px(840),1,0,'#111',None,'#ccc')   # dikey ince bolme (ayni sicaklik)
# +3 cekmeceler: sol 4 icecek + 1L ; sag 8 taze — cekmece onu 40 izoleli + conta
def front(x,y,w,h,c='#111',fill=PU,lab='',sub=''):
    rc(x,y,w,h,1.2,2,c,None,fill)
    ln(x+w/2-18,y+h-6,x+w/2+18,y+h-6,2,c)      # tutamak (eleman)
    if lab: tx(x+w/2,y+h/2-2,lab,7.5,'middle','bold',c)
    if sub: tx(x+w/2,y+h/2+9,sub,6.5,'middle','',c)
xl, xr = X0+px(66), X0+px(714)                     # sol/sag acikliklarin ic kenari
wcol = px(624)
for k in range(4):
    y = Y0+px(Y3+5)+k*px(105)
    front(xl,y,wcol,px(95),'#111',PU,'İÇECEK %d — 7 kanal' % (k+1),'kutu 24 · tatlı 3 · yedek 1')
front(xl,Y0+px(Y3+5)+4*px(105),wcol,px(410),'#111',PU,'1 L ÇEKMECESİ — 5 kanal × 8','şişe dik, ~40')
for r in range(8):
    y = Y0+px(Y3+5)+r*px(105)
    front(xr,y,wcol,px(95),'#111',PU,'TAZE %d — 1 tepsi 20 top' % (r+1),'')
not_(X0+px(1027),Y0+px(Y3+5)+8*px(105)+10,'8 × 20 = 160 (2 gün) · pitch 10,5: kutu 1,5 + tepsi 3 + top 4,5 + boşluk 1,5',fs=7.5)
# yatay izoleli ayirici 80 (y 1140-1220)
rc(X0+6,Y0+px(1140),px(GW)-12,px(80),1.2,0,'#111',None,PU)
tx(X0+px(700),Y0+px(1190),'YATAY İZOLELİ AYIRICI PU 80 — tek parça, tam en',8.5,'middle','bold')
# −18 bandi: paneller 80
rc(X0+6,Y0+px(1220),px(80),px(630),1,0,'#111',None,PU); rc(X0+px(GW)-6-px(80),Y0+px(1220),px(80),px(630),1,0,'#111',None,PU)
rc(X0+6,Y0+px(1770),px(GW)-12,px(80),1,0,'#111',None,PU)     # alt panel 80
rc(X0+px(690),Y0+px(1220),px(20),px(550),1,0,'#111',None,'#ccc')
xl2, xr2 = X0+px(86), X0+px(714); wcol2 = px(604)
for k in range(2):
    y = Y0+px(1225)+k*px(105)
    front(xl2,y,wcol2,px(95),Bl,'#dfe7fb','DONMUŞ %d — 20 top' % (k+1),'')
    front(xr2,y,wcol2,px(95),Bl,'#dfe7fb','DONMUŞ %d — 20 top' % (k+3),'')
front(xl2,Y0+px(1440),wcol2,px(300),Bl,'#dfe7fb','KASET: KAVURMA ×2','17×21×25 · −18 · boş yer +1')
front(xr2,Y0+px(1440),wcol2,px(300),Bl,'#dfe7fb','KASET: KUŞBAŞI ×2','17×21×25 · −18 · boş yer +1')
tx(X0+px(700),Y0+px(1758),'−18 °C bandı — 4 hamur çekmecesi = 80 top (1 gün) + 2 kaset çekmecesi · çekmece önü 60 izoleli',7.5,'middle','bold',Bl)
# olculer
oy(X0,X0+px(700),Y0-2+px(26)-14,'70'); oy(X0+px(700),X0+px(GW),Y0-2+px(26)-14,'70')
oy(X0,X0+px(GW),YZ+30,'140')
ox(X0-34,Y0,YT,'185'); ox(X0-34,YT,YZ,'12'); ox(X0-70,Y0,YZ,'197')
xr_ = X0+px(GW)+22
ox(xr_,Y0+px(20),Y0+px(240),'soğutma 22',side='r'); ox(xr_,Y0+px(240),Y0+px(300),'6',side='r'); ox(xr_,Y0+px(300),Y0+px(1140),'+3 · 84',side='r'); ox(xr_,Y0+px(1140),Y0+px(1220),'8',side='r'); ox(xr_,Y0+px(1220),Y0+px(1770),'−18 · 55',side='r'); ox(xr_,Y0+px(1770),Y0+px(1850),'8',side='r')

# ================= C) YAN KESIT (S=0.3) — cekmece tam acik, robot erisimi =================
S2 = 0.3
def p2(mm): return mm*S2
SX, SY = 1000, 150
DER = 840
tx(SX+p2(DER)/2-40,SY-18,'YAN KESİT — çekmece TAM AÇIK (70 cm), robot üstten alır',12.5,'middle','bold')
rc(SX,SY,p2(DER),p2(GH),2,4); rc(SX+10,SY+p2(GH),10,p2(AYAK)); rc(SX+p2(DER)-20,SY+p2(GH),10,p2(AYAK))
ln(SX-p2(900),SY+p2(GH+AYAK),SX+p2(DER)+30,SY+p2(GH+AYAK),2)
rc(SX+4,SY+p2(20),p2(DER)-8,p2(220),1,2); tx(SX+p2(420),SY+p2(140),'soğutma',8)
rc(SX+4,SY+p2(240),p2(DER)-8,p2(60),1,0,'#111',None,PU)
rc(SX+p2(DER)-4-p2(60),SY+p2(240),p2(60),p2(1140),1,0,'#111',None,PU)   # arka panel +3
rc(SX+4,SY+p2(1140),p2(DER)-8,p2(80),1,0,'#111',None,PU)
rc(SX+p2(DER)-4-p2(80),SY+p2(1220),p2(80),p2(630),1,0,'#111',None,PU)
rc(SX+4,SY+p2(1770),p2(DER)-8,p2(80),1,0,'#111',None,PU)
# +3 cekmeceler kapali (on yuz 40 + kutu 740)
for r in range(8):
    y = SY+p2(Y3+5)+r*p2(105)
    rc(SX+4,y,p2(40),p2(95),1,1,'#111',None,PU)
    if r != 3:
        ln(SX+p2(44),y+p2(90),SX+p2(780),y+p2(90),1); ln(SX+p2(44),y+p2(75),SX+p2(780),y+p2(75),.6,'#999')
        for i in range(5): ci(SX+p2(110)+i*p2(140),y+p2(52),p2(24),.8)
# 4. cekmece TAM ACIK: 700 mm one
y4 = SY+p2(Y3+5)+3*p2(105)
rc(SX-p2(700),y4,p2(40),p2(95),1.2,1,'#111',None,PU)                       # on yuz disarida
ln(SX-p2(656),y4+p2(90),SX+p2(80),y4+p2(90),1.4); ln(SX-p2(656),y4+p2(75),SX+p2(80),y4+p2(75),.7,'#999')
for i in range(5): ci(SX-p2(590)+i*p2(140),y4+p2(52),p2(24),1)
ln(SX+4,y4+p2(93),SX+p2(80),y4+p2(93),2.4,'#555')                            # ray (kabin tarafi)
tx(SX-p2(330),y4+p2(120),'tam açılım 70 cm — 5 sıra çukur da dışarıda',7.5,'middle','bold',G)
# pence ustten
rc(SX-p2(340),y4-p2(230),p2(60),p2(120),1.3,3,Bl); ln(SX-p2(320),y4-p2(110),SX-p2(320),y4-p2(30),1.3,Bl); ln(SX-p2(300),y4-p2(110),SX-p2(300),y4-p2(30),1.3,Bl)
ln(SX-p2(310),y4-p2(230),SX-p2(200),y4-p2(330),2,Bl); tx(SX-p2(150),y4-p2(340),'kol (araba YANDA park)',7.5,'start','',Bl)
arr(SX-p2(310),y4-p2(25),SX-p2(310),y4+p2(30),1.4,Bl)
# −18 cekmeceler
for k in range(2):
    y = SY+p2(1225)+k*p2(105)
    rc(SX+4,y,p2(60),p2(95),1,1,Bl,None,'#dfe7fb'); ln(SX+p2(64),y+p2(90),SX+p2(760),y+p2(90),1,Bl)
    for i in range(5): ci(SX+p2(130)+i*p2(135),y+p2(52),p2(24),.8,Bl)
rc(SX+4,SY+p2(1440),p2(60),p2(300),1,1,Bl,None,'#dfe7fb'); ln(SX+p2(64),SY+p2(1735),SX+p2(760),SY+p2(1735),1,Bl)
for i in range(2): rc(SX+p2(100)+i*p2(240),SY+p2(1470),p2(210),p2(250),1.1,2,Bl)
# koridor + ray + araba (yan gorunuste ray yerde)
ln(SX-p2(900),SY+p2(GH+AYAK),SX-p2(900),SY+p2(GH+AYAK)-p2(60),1)
rc(SX-p2(500),SY+p2(GH+AYAK)-p2(100),p2(100),p2(100),1.2,2,'#555'); tx(SX-p2(450),SY+p2(GH+AYAK)+14,'ray (yerde, 10 cm)',7,'middle','','#555')
tx(SX-p2(450),SY+p2(GH+AYAK)-p2(130),'çekmece rayın ÜSTÜNDEN geçer (en alt çekmece tabanı 20 cm)',7,'middle','','#555')
oy(SX-p2(700),SX,SY+p2(Y3-40),'70 açılım')
oy(SX,SX+p2(DER),SY+p2(GH+AYAK)+30,'84'); oy(SX-p2(900),SX,SY+p2(GH+AYAK)+30,'koridor 90')
ln(SX,SY+p2(60),SX,SY+p2(1850),3,'#2a6a9a')

# ================= B) KESIT DETAYI — genislik ve pitch (mm) =================
DX, DY = 760, 812
tx(DX,DY,'DETAY — 61 cm modülün EN kesiti (mm):',11.5,'start','bold')
S3 = 0.55
def p3(mm): return mm*S3
x = DX; y = DY+15
parts = [(60,'panel PU 60',PU),(2,'',None),(13,'ray 12,7','#ccc'),(1.5,'kutu 1,5','#999'),(20,'pay','#fff'),(530,'TEPSİ 530 (çukurlu GN 2/1, derinlemesine)','#f4f1ea'),(20,'pay','#fff'),(1.5,'kutu','#999'),(13,'ray','#ccc'),(2,'',None),(20,'bölme 20','#ccc')]
cx = x
for w_,lab,fl in parts:
    if fl: rc(cx,y,p3(w_),40,1,0,'#111',None,fl)
    if lab and w_>=13: tx(cx+p3(w_)/2, y+56 if w_<40 else y+24, lab, 7 if w_<40 else 8.5, 'middle','', '#333')
    cx += p3(w_)
oy(x, cx, y-8, 'modül 683 → 2 modül + paneller = 1400 ✓', 8)
tx(DX,DY+95,'−18 bandı: panel 80 + 2 modül (ray 13 + kutu 1,5 + pay 15 + tepsi 530 + pay 15 + kutu + ray) + bölme 20 + panel 80 = 1400 ✓ · derinlik: ön 60 + kutu 700 + arka 80 = 840 ✓ (tepsi 650)',8.5,'start','','#333')
tx(DX,DY+112,'+3 derinlik: ön 40 + kutu 740 + arka 60 = 840 ✓',8.5,'start','','#333')
tx(DX,DY+140,'DETAY — çekmece PITCH 105 mm (dikey):',11.5,'start','bold')
y2 = DY+150; x2 = DX
pitch = [(15,'kutu tabanı + ray 15','#ccc'),(30,'tepsi 30','#f4f1ea'),(45,'top 45 (çukurdan taşan)','#fbf3e6'),(15,'boşluk 15','#fff')]
cy = y2
for h_,lab,fl in pitch:
    rc(x2,cy,90,h_*1.3,1,0,'#111',None,fl); tx(x2+100,cy+h_*1.3/2+3,lab,8.5,'start','','#333'); cy += h_*1.3
ox(x2-12,y2,cy,'105',fs=9)
tx(DX,cy+22,'−18 hamur: aynı 105 (donmuş top büyümez) · kaset çekmecesi 290 = kaset 250 + 25 + 15',8.5,'start','','#333')
tx(DX,cy+40,'DİKEY: 20 + 220 + 60 + 8×105 + 80 + 2×105 + 290 + 80 = 1800 → 50 mm pay → 185 + ayak 12 = 197 ✓',9,'start','bold',G)

# ================= D) NOTLAR =================
NX, NY = 1290, 150
tx(NX,NY,'KARARLAR (v2):',12,'start','bold')
nots = [
 ('· 19 çekmece, hepsi 61 cm modül; kapak yok','bold','#1a1a1a'),
 ('· En alt 140\'lık çekmece ikiye bölündü (Kemal):','','#1a49b8'),
 ('  −18 bandı = 4 hamur + 2 kaset çekmecesi','','#1a49b8'),
 ('· Panel: +3 gövde 60 · −18 bandı 80 · ayırıcı 80','','#333'),
 ('  (soğuk oda kılavuzu: +3 60-80, −18 80-100)','','#666'),
 ('· Çekmece önü izoleli 40 (+3) / 60 (−18) + conta','','#333'),
 ('· Ray: paslanmaz tam açılım 12,7/yan, 45 kg','','#333'),
 ('  (Accuride 3832 sınıfı; 9301 = 227 kg, gereksiz)','','#666'),
 ('· Tepsi 53×65 DERİNLEMESİNE (modül içi 595)','','#333'),
 ('· ROBOT ERİŞİMİ: çekmece 70 cm tam açılır,','bold','#1d7a4f'),
 ('  rayın üstünden geçer; robot arabası yanda','','#1d7a4f'),
 ('  park eder, kol üstten çukur çukur alır','','#1d7a4f'),
 ('  (ön sıralar için 13/26 cm kısmi açılım da olur)','','#666'),
 ('· Pitch 105: 8 taze = 84 cm; dikey bütçe tutuyor','','#333'),
 ('','',''),
 ('STOK (değişmedi — Kemal teyidi):','bold','#333'),
 ('· içecek 255 kutu + 1 L 25 + tatlı 45 = HAFTALIK','','#333'),
 ('· taze hamur 160 = 2 GÜN (+3, 8 çekmece)','','#333'),
 ('· donmuş hamur 80 = 1 GÜN (3. gün; −18)','','#333'),
 ('  → fırıncı 3 günde bir 240 top','','#666'),
 ('· donmuş kaset kavurma ×2 + kuşbaşı ×2 = HAFTALIK','','#333'),
 ('· kutu 116 (PACK) + 320 (SERVICE) = HAFTALIK','','#333'),
 ('','',''),
 ('AÇIK:','bold','#b3452b'),
 ('· −18 çekmece contası + buzlanma (defrost)','','#b3452b'),
 ('· çekmece motoru: 24 V lineer, 20 kg, 70 cm','','#b3452b'),
 ('· kasa üreticisi teyidi (İnoksan/Öztiryakiler','','#b3452b'),
 ('  çekmeceli özel kasa mı, standart + modifiye mi)','','#666'),
]
yy = NY+22
for s_,w_,c_ in nots:
    if s_: tx(NX,yy,s_,9.8,'start',w_,c_)
    yy += 17.5

tx(W-24,H-14,'AUTOKITCH · ist1_store_detay_v2',10,'end','','#999')
svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d"><rect width="%d" height="%d" fill="#ffffff"/>%s</svg>' % (W,H,W,H,W,H,''.join(E))
OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\1_STORE\ist1_store_detay_v2.svg"
io.open(OUT,'w',encoding='utf-8').write(svg)
print('yazildi:', OUT)
