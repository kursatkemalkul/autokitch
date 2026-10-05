# -*- coding: utf-8 -*-
# IST.1 STORE — DETAY v4 (4 Eyl 2026): OLCU KONTROLU (Kemal) — hamur topu kubbe O9,5x6 · kutu 330 ml O66x115 · tatli 4 kanal ·
# 1 L <=28 cm · sogutma bolmesi 22->28 · −18 hamur pitch 10 · kaset cekmecesi 29 · dikey 2+28+6+84+8+49+8 = 185
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
def el(cx,cy,rx,ry,sw=1.4,c='#111',dash=None,fill='none'):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    E.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (cx,cy,rx,ry,fill,c,sw,d))
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
Bl, G, Rd = '#1a49b8', '#1d7a4f', '#b3452b'
PU = '#e9e4d6'; D = '3,3'
tx(40,44,'İSTASYON 1 — STORE · DETAY v4 (ölçü kontrolü: hamur topu Ø9,5×6 kubbe · kutu 330 ml Ø66×115 · tatlı 4 kanal · soğutma bölmesi 28 · dikey 185 ✓)',17,'start','bold')
tx(40,68,'Gövde PU 60 (+3) / 80 (−18) · ayırıcı 80 · çekmece önü 40 / 60 + conta · ray paslanmaz tam açılım 12,7/yan · kutu 1,5 · tepsi GN 2/1 53×65 derinlemesine (4×5 çukur Ø12, 13 cm aralık) · 19 çekmece × 61 cm modül · kapak yok',10.5,'start','','#555')

# ---- dikey plan (mm, ustten)
CAP, SOG, UP = 20, 280, 60           # kapak · sogutma bolmesi · ust panel
Y3 = CAP+SOG+UP                      # 360: +3 ic ust
Z3 = 840                             # +3 bolge (8x105 sag · 4x130+320 sol)
AYR = 80
YF = Y3+Z3+AYR                       # 1280: −18 ic ust
HP, KAS, BOT = 100, 290, 80          # donmus hamur pitch · kaset cekmecesi · alt panel
assert Y3+Z3+AYR+2*HP+KAS+BOT == 1850, Y3+Z3+AYR+2*HP+KAS+BOT

# ================= A) ON GORUNUS =================
S = 0.46
def px(mm): return mm*S
X0, Y0 = 60, 150
GW, GH, AYAK = 1400, 1850, 120
YT = Y0+px(GH); YZ = YT+px(AYAK)
tx(X0+px(GW)/2,Y0-18,'ÖN GÖRÜNÜŞ — içerikler kesik çizgi · 19 çekmece · kapak yok',12.5,'middle','bold')
rc(X0,Y0,px(GW),px(GH),2,4)
rc(X0+14,YT,12,px(AYAK)); rc(X0+px(GW)-26,YT,12,px(AYAK)); ln(X0-40,YZ,X0+px(GW)+40,YZ,2)
rc(X0+6,Y0+px(CAP),px(GW)-12,px(SOG),1.2,2)
for gx,lab in ((350,'−18 grubu 1/3 HP'),(1050,'+3 grubu 1/4 HP')):
    rc(X0+px(gx-170),Y0+px(CAP+30),px(340),px(220),1,3)
    ci(X0+px(gx-70),Y0+px(CAP+140),px(60),1.1); ln(X0+px(gx-112),Y0+px(CAP+98),X0+px(gx-28),Y0+px(CAP+182),.8); ln(X0+px(gx-112),Y0+px(CAP+182),X0+px(gx-28),Y0+px(CAP+98),.8)
    rc(X0+px(gx+10),Y0+px(CAP+60),px(130),px(160),.9,2); tx(X0+px(gx+75),Y0+px(CAP+150),'kond.',6.5)
    tx(X0+px(gx),Y0+px(CAP+270),lab,7.5,'middle','bold')
not_(X0+px(700),Y0+px(CAP+12),'SOĞUTMA BÖLMESİ 28 — iki grup 25-28 cm boy (22 sığmıyordu) · üstten servis',fs=8)
rc(X0+6,Y0+px(CAP+SOG),px(GW)-12,px(UP),1,0,'#111',None,PU)
rc(X0+6,Y0+px(CAP+SOG),px(60),px(UP+Z3),1,0,'#111',None,PU); rc(X0+px(GW)-6-px(60),Y0+px(CAP+SOG),px(60),px(UP+Z3),1,0,'#111',None,PU)
rc(X0+px(690),Y0+px(Y3),px(20),px(Z3),1,0,'#111',None,'#ccc')
def front(x,y,w,h,c='#111',fill=PU):
    rc(x,y,w,h,1.2,2,c,None,fill); ln(x+w/2-18,y+h-6,x+w/2+18,y+h-6,2,c)
xl, xr = X0+px(66), X0+px(714); wcol = px(624)
# sol: icecek 4 x 130 (kutu O66x115) + 1L 320
for k in range(4):
    y = Y0+px(Y3+2)+k*px(130)
    front(xl,y,wcol,px(124))
    for i in range(7):
        rc(xl+px(22)+i*px(82),y+px(5),px(66),px(115),.9,3,'#777',D); el(xl+px(55)+i*px(82),y+px(9),px(33),px(6),.7,'#777',D)
    tx(xl+wcol/2,y+px(64)+3,'İÇECEK %d — 7 kanal (kutu Ø66×115)' % (k+1),7,'middle','bold','#111')
y1L = Y0+px(Y3+2)+4*px(130)
front(xl,y1L,wcol,px(316))
for i in range(5):
    bx = xl+px(50)+i*px(110)
    rc(bx,y1L+px(60),px(85),px(240),.9,6,'#777',D); rc(bx+px(28),y1L+px(12),px(29),px(48),.9,2,'#777',D)
tx(xl+wcol/2,y1L+px(160),'1 L ÇEKMECESİ — 5 kanal × 8 (şişe ≤ 28 cm)',7,'middle','bold','#111')
not_(xl+wcol/2,y1L+px(316)+12,'kanal: kutu 24 (264) · tatlı 4 (44) · yedek 0 — tatlı 3 kanal 33 &lt; 45 idi',fs=7,c=Rd)
# sag: taze 8 x 105 — top KUBBE O9,5 x 6 (cukurda 2 gomulu, 4 tasan)
def tops(x,rim,w,c='#777'):
    for i in range(4):
        cx_ = x+px(95)+i*px(140)
        el(cx_,rim-px(10),px(47),px(30),.9,c,D)              # kubbe: rim-40 .. rim+20 (cukur ici)
    rc(x+px(30),rim,w-px(60),px(30),.9,1,c,D,'#fff')          # tepsi (30) — cukur icini gizler
    ln(x+px(30),rim,x+w-px(30),rim,.9,c,D)
for r in range(8):
    y = Y0+px(Y3+2)+r*px(105)
    front(xr,y,wcol,px(99))
    tops(xr,y+px(60),wcol)
    tx(xr+wcol/2,y+px(96)-2,'TAZE %d — 20 top' % (r+1),6.5,'middle','bold','#111')
not_(xr+wcol/2,Y0+px(Y3+2)+8*px(105)+12,'8 × 20 = 160 (2 gün) · pitch 10,5 = kutu/ray 1,5 + tepsi 3 + taşan top 4 + boşluk 2 · top ≤ 6 cm (fırıncı spec)',fs=7)
# ayirici
rc(X0+6,Y0+px(Y3+Z3),px(GW)-12,px(AYR),1.2,0,'#111',None,PU)
tx(X0+px(700),Y0+px(Y3+Z3+50),'YATAY İZOLELİ AYIRICI PU 80 — tek parça',8.5,'middle','bold')
# −18 bandi
rc(X0+6,Y0+px(YF),px(80),px(1850-YF),1,0,'#111',None,PU); rc(X0+px(GW)-6-px(80),Y0+px(YF),px(80),px(1850-YF),1,0,'#111',None,PU)
rc(X0+6,Y0+px(1850-BOT),px(GW)-12,px(BOT),1,0,'#111',None,PU)
rc(X0+px(690),Y0+px(YF),px(20),px(1850-YF-BOT),1,0,'#111',None,'#ccc')
xl2, xr2 = X0+px(86), X0+px(714); wcol2 = px(604)
for k in range(2):
    y = Y0+px(YF+3)+k*px(HP)
    for xx_,nm in ((xl2,k+1),(xr2,k+3)):
        front(xx_,y,wcol2,px(94),Bl,'#dfe7fb'); tops(xx_,y+px(58),wcol2,Bl)
        tx(xx_+wcol2/2,y+px(91)-2,'DONMUŞ %d — 20 top (pitch 10, büyümez)' % nm,6.5,'middle','bold',Bl)
yk = Y0+px(YF+2*HP+3)
for xx_,nm in ((xl2,'KAVURMA'),(xr2,'KUŞBAŞI')):
    front(xx_,yk,wcol2,px(KAS-6),Bl,'#dfe7fb')
    for i in range(2):
        rc(xx_+px(40)+i*px(185),yk+px(12),px(170),px(250),1,2,Bl,D); rc(xx_+px(40)+i*px(185)+px(150),yk+px(70),px(14),px(70),.9,1,Bl,D)
    rc(xx_+px(410),yk+px(12),px(170),px(250),.8,2,'#999',D); tx(xx_+px(495),yk+px(140),'boş +1',6,'middle','','#999')
    tx(xx_+wcol2/2,yk+px(KAS-6)-8,'KASET %s ×2 · 17×21×25 · çekmece 29' % nm,6.5,'middle','bold',Bl)
# olculer
oy(X0,X0+px(700),Y0-2+px(26)-14,'70'); oy(X0+px(700),X0+px(GW),Y0-2+px(26)-14,'70')
oy(X0,X0+px(GW),YZ+30,'140')
ox(X0-34,Y0,YT,'185'); ox(X0-34,YT,YZ,'12'); ox(X0-70,Y0,YZ,'197')
xr_ = X0+px(GW)+22
ox(xr_,Y0+px(CAP),Y0+px(CAP+SOG),'soğutma 28',side='r'); ox(xr_,Y0+px(CAP+SOG),Y0+px(Y3),'6',side='r'); ox(xr_,Y0+px(Y3),Y0+px(Y3+Z3),'+3 · 84',side='r'); ox(xr_,Y0+px(Y3+Z3),Y0+px(YF),'8',side='r'); ox(xr_,Y0+px(YF),Y0+px(1850-BOT),'−18 · 47',side='r'); ox(xr_,Y0+px(1850-BOT),Y0+px(1850),'8',side='r')

# ================= C) YAN KESIT (S=0.3) =================
S2 = 0.3
def p2(mm): return mm*S2
SX, SY = 1000, 150; DER = 840
tx(SX+p2(DER)/2-40,SY-18,'YAN KESİT — çekmece TAM AÇIK (70), robot üstten',12.5,'middle','bold')
rc(SX,SY,p2(DER),p2(GH),2,4); rc(SX+10,SY+p2(GH),10,p2(AYAK)); rc(SX+p2(DER)-20,SY+p2(GH),10,p2(AYAK))
ln(SX-p2(900),SY+p2(GH+AYAK),SX+p2(DER)+30,SY+p2(GH+AYAK),2)
rc(SX+4,SY+p2(CAP),p2(DER)-8,p2(SOG),1,2); tx(SX+p2(420),SY+p2(CAP+150),'soğutma 28',8)
rc(SX+4,SY+p2(CAP+SOG),p2(DER)-8,p2(UP),1,0,'#111',None,PU)
rc(SX+p2(DER)-4-p2(60),SY+p2(CAP+SOG),p2(60),p2(UP+Z3),1,0,'#111',None,PU)
rc(SX+4,SY+p2(Y3+Z3),p2(DER)-8,p2(AYR),1,0,'#111',None,PU)
rc(SX+p2(DER)-4-p2(80),SY+p2(YF),p2(80),p2(1850-YF),1,0,'#111',None,PU)
rc(SX+4,SY+p2(1850-BOT),p2(DER)-8,p2(BOT),1,0,'#111',None,PU)
for r in range(8):
    y = SY+p2(Y3+2)+r*p2(105)
    rc(SX+4,y,p2(40),p2(99),1,1,'#111',None,PU)
    if r != 3:
        ln(SX+p2(44),y+p2(90),SX+p2(780),y+p2(90),1)
        for i in range(5): el(SX+p2(110)+i*p2(140),y+p2(78),p2(24),p2(16),.8)
y4 = SY+p2(Y3+2)+3*p2(105)
rc(SX-p2(700),y4,p2(40),p2(99),1.2,1,'#111',None,PU)
ln(SX-p2(656),y4+p2(90),SX+p2(80),y4+p2(90),1.4)
for i in range(5): el(SX-p2(590)+i*p2(140),y4+p2(78),p2(24),p2(16),1)
tx(SX-p2(330),y4+p2(125),'tam açılım 70 — 5 sıra çukur dışarıda',7.5,'middle','bold',G)
rc(SX-p2(340),y4-p2(230),p2(60),p2(120),1.3,3,Bl); ln(SX-p2(320),y4-p2(110),SX-p2(320),y4-p2(30),1.3,Bl); ln(SX-p2(300),y4-p2(110),SX-p2(300),y4-p2(30),1.3,Bl)
ln(SX-p2(310),y4-p2(230),SX-p2(200),y4-p2(330),2,Bl); tx(SX-p2(150),y4-p2(340),'kol (araba yanda park)',7.5,'start','',Bl)
arr(SX-p2(310),y4-p2(25),SX-p2(310),y4+p2(40),1.4,Bl)
for k in range(2):
    y = SY+p2(YF+3)+k*p2(HP)
    rc(SX+4,y,p2(60),p2(94),1,1,Bl,None,'#dfe7fb'); ln(SX+p2(64),y+p2(88),SX+p2(760),y+p2(88),1,Bl)
    for i in range(5): el(SX+p2(130)+i*p2(135),y+p2(76),p2(24),p2(16),.8,Bl)
rc(SX+4,SY+p2(YF+2*HP+3),p2(60),p2(KAS-6),1,1,Bl,None,'#dfe7fb'); ln(SX+p2(64),SY+p2(1850-BOT-5),SX+p2(760),SY+p2(1850-BOT-5),1,Bl)
for i in range(3): rc(SX+p2(100)+i*p2(225),SY+p2(YF+2*HP+15),p2(200),p2(245),1.1,2,Bl,D if i==2 else None)
tx(SX+p2(420),SY+p2(YF+2*HP+30)+8,'derinlikte 3 kaset sığar (büyüme)',6.5,'middle','',Bl)
rc(SX-p2(500),SY+p2(GH+AYAK)-p2(100),p2(100),p2(100),1.2,2,'#555'); tx(SX-p2(450),SY+p2(GH+AYAK)+14,'ray (yerde, 10)',7,'middle','','#555')
oy(SX-p2(700),SX,SY+p2(Y3-60),'70 açılım')
oy(SX,SX+p2(DER),SY+p2(GH+AYAK)+30,'84'); oy(SX-p2(900),SX,SY+p2(GH+AYAK)+30,'koridor 90')
ln(SX,SY+p2(60),SX,SY+p2(1850),3,'#2a6a9a')

# ================= B) OLCU KONTROL TABLOSU =================
TX_, TY_ = 760, 790
tx(TX_,TY_,'ÖLÇÜ KONTROLÜ (gerçek değerler) — ✓ tutuyor · ✗ düzeltildi',12,'start','bold')
rows = [
 ('Hamur topu 220 g','200-280 cm³ → dinlenmiş kubbe Ø9-10 × 5-6; çukur Ø12×2 → taşan 4','✓ pitch 10,5 (top ≤ 6 cm fırıncı spec)',G),
 ('Çukurlu tepsi GN 2/1','53×65×3 silikon, 4×5 = 20 çukur, aralık 13 (Ø12 çukur, 1 cm hendek)','✓ modül içi 595 > 530; derinlik 740 > 650',G),
 ('Kutu 330 ml','Ø66 × 115 (12,3 = 355 ml idi)','✓ çekmece 13; kanal 8,2; derinlikte 11 → 28 kanal = 308',G),
 ('Tatlı (endüstriyel SKT)','45/hafta; 3 kanal × 11 = 33 &lt; 45','✗ 4 kanal (44) — kutu 24 kanal = 264 ≥ 255, yedek 0',Rd),
 ('1 L PET','Ø8-9 × 27-28 (Coca-Cola 1 L 27,5)','✓ çekmece 32; 5 kanal × 8 = 40 ≥ 25; 30 cm şişe OLMAZ',G),
 ('Donmuş kaset 17×21×25','2 kaset 34 + boş 17 = 51 ≤ 59,5; derinlik 70 → 3 sıra','✓ çekmece 29 (25 + 4); kavurma ×2 | kuşbaşı ×2',G),
 ('Soğutma grupları','+3 ≈1 m³ → 1/4 HP · −18 ≈0,35 m³ → 1/3 HP; boy 25-28','✗ bölme 22 → 28 (dikey: −18 pitch 10, kaset 29)',Rd),
 ('Panel / çekmece önü','PU 60 (+3) · 80 (−18) · ayırıcı 80 · ön 40/60 + conta','✓ en 1400 · derinlik 840 tutuyor',G),
 ('Ray','paslanmaz tam açılım 12,7/yan, 45 kg (yük ≤ 10 kg)','✓ 9301 (227 kg, 39 mm) gereksiz',G),
 ('Robot erişimi','pençe 0-140 açılır; top Ø9,5, top aralığı 13 → parmak payı 1,7','✓ sınırda ama yeter; çekmece 70 açık, araba yanda',G),
 ('Dikey bütçe','2 + 28 + 6 + 84 + 8 + (10+10+29) + 8 = 185','✓ tam kapanıyor (pay kaset çekmecesinde 4 cm)',G),
 ('Stok','taze 160 (2 g) · donmuş 80 (1 g) · kutu 264 · tatlı 44 · 1 L 40 · kaset 4','✓ haftalık/3 gün ritmi değişmedi',G),
]
yy = TY_+22
for a_,b_,c_,col in rows:
    tx(TX_,yy,a_,8.6,'start','bold','#111'); tx(TX_+150,yy,b_,8.3,'start','','#333'); tx(TX_+470,yy,c_,8.3,'start','bold',col)
    ln(TX_,yy+5,TX_+780,yy+5,.4,'#ddd'); yy += 16.5
tx(TX_,yy+12,'KAYNAK: soğuk oda panel kılavuzları (+3 60-80 / −18 80-100 mm PU) · Accuride 9301 spec (500 lb, 39 mm yan boşluk) · 330 ml kutu 66,3×115,2 · 1 L PET 27-28 cm',7.5,'start','','#888')

# ================= D) NOTLAR =================
NX, NY = 1290, 150
tx(NX,NY,'KARARLAR (v4):',12,'start','bold')
nots = [
 ('· v3 üstüne ÖLÇÜ KONTROLÜ (Kemal)','bold','#1a1a1a'),
 ('· Hamur topu kubbe Ø9,5×6 çizildi','','#333'),
 ('  (basık ellips değil); çukurda 2 gömülü','','#666'),
 ('· Kutu 330 ml Ø66×115 → 13 çekmece ✓','','#333'),
 ('· TATLI 3 → 4 kanal (33 &lt; 45 idi)','','#b3452b'),
 ('· SOĞUTMA bölmesi 22 → 28 (iki grup','','#b3452b'),
 ('  25-28 cm; 1/4 HP + 1/3 HP)','','#666'),
 ('· Dikey: 2+28+6+84+8+49+8 = 185 ✓','','#333'),
 ('  (pay kaset çekmecesinde 4 cm)','','#666'),
 ('· −18 hamur pitch 10 (donmuş büyümez)','','#333'),
 ('· Kaset çekmecesi 29; derinlikte 3 sıra','','#333'),
 ('· 1 L şişe ≤ 28 cm (çekmece 32)','','#333'),
 ('· 19 çekmece × 61 modül, kapak yok ✓','','#333'),
 ('· Robot: 70 tam açılım, araba yanda ✓','','#333'),
 ('','',''),
 ('AÇIK:','bold','#b3452b'),
 ('· fırıncıya top spec: 220 g, dinlenmiş','','#b3452b'),
 ('  boy ≤ 6 cm, Ø ≤ 10','','#666'),
 ('· −18 çekmece contası + defrost','','#b3452b'),
 ('· çekmece motoru 24 V lineer, 70 cm','','#b3452b'),
 ('· kasa üreticisi teyidi (İnoksan /','','#b3452b'),
 ('  Öztiryakiler çekmeceli özel kasa)','','#666'),

]
yy = NY+22
for s_,w_,c_ in nots:
    if s_: tx(NX,yy,s_,9.8,'start',w_,c_)
    yy += 17.5

tx(W-24,H-14,'AUTOKITCH · ist1_store_detay_v4',10,'end','','#999')
svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d"><rect width="%d" height="%d" fill="#ffffff"/>%s</svg>' % (W,H,W,H,W,H,''.join(E))
OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\1_STORE\ist1_store_detay_v4.svg"
io.open(OUT,'w',encoding='utf-8').write(svg)
print('yazildi:', OUT)
