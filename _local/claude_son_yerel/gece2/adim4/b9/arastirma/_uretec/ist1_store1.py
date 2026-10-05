# -*- coding: utf-8 -*-
# IST.1 STORE — DETAY v1 (4 Eyl 2026, Kemal): ALT BUZLUK tam genislik + TAM CEKMECELI, KAPAKSIZ kasa 140x197x84
# ust: sogutma gruplari x2 (29) · +3: sol icecek 4 cekmece + 1L, sag taze hamur 8 cekmece (96) · yatay izoleli ayirici (5)
# alt −18 bandi (52): 2 hamur cekmecesi (2 tepsi yan yana = 40'ar top -> 80) + 1 kaset cekmecesi (4 donmus kaset: kavurma x2, kusbasi x2)
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
def oy(x1,x2,y,cm):
    ln(x1,y,x2,y,1,'#b3452b'); ln(x1,y-5,x1,y+5,1,'#b3452b'); ln(x2,y-5,x2,y+5,1,'#b3452b')
    tx((x1+x2)/2,y-6,cm,11,'middle','bold','#b3452b')
def ox(x,y1,y2,cm,side='l'):
    ln(x,y1,x,y2,1,'#b3452b'); ln(x-5,y1,x+5,y1,1,'#b3452b'); ln(x-5,y2,x+5,y2,1,'#b3452b')
    xx = x-9 if side=='l' else x+9
    E.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#b3452b" font-family="Arial" transform="rotate(-90 %.1f %.1f)">%s</text>' % (xx,(y1+y2)/2,xx,(y1+y2)/2,cm))

W, H = 1560, 1180
S = 0.46
def px(mm): return mm*S
X0, Y0 = 90, 150
GW, GH, AYAK, DER = 1400, 1850, 120, 840
YT = Y0+px(GH); YZ = YT+px(AYAK)
Bl, G, Rd = '#1a49b8', '#1d7a4f', '#b3452b'
tx(40,44,'İSTASYON 1 — STORE · DETAY v1 (ALT BUZLUK tam genişlik · TAM ÇEKMECELİ, KAPAKSIZ kasa 140 × 197 × 84 · soğutma üstte)',17,'start','bold')
tx(40,68,'Kemal (4 Eyl): büyük kapak yok, cam yok — her şey çekmece, her çekmecenin ön yüzü izoleli = kendi kapağı. −18 en altta tam genişlik (2 hamur çekmecesi 2 tepsi yan yana = 80 top + 1 kaset çekmecesi: kavurma ×2, kuşbaşı ×2). +3 üstte: sol içecek + 1 L, sağ taze hamur 8 çekmece.',10.5,'start','','#555')

# ================= ON GORUNUS =================
tx(X0+px(GW)/2,Y0-18,'ÖN GÖRÜNÜŞ (robot tarafı = eleman tarafı — tek cephe, tümü çekmece)',12.5,'middle','bold')
rc(X0,Y0,px(GW),px(GH),2.2,5)
rc(X0+14,YT,12,px(AYAK)); rc(X0+px(GW)-26,YT,12,px(AYAK))
ln(X0-40,YZ,X0+px(GW)+40,YZ,2)
# sogutma gruplari (ust 0-290)
rc(X0+8,Y0+px(10),px(GW)-16,px(280),1.6,3)
for gx in (350,1050):
    ci(X0+px(gx),Y0+px(150),px(75),1.2)
    ln(X0+px(gx-55),Y0+px(95),X0+px(gx+55),Y0+px(205),.9); ln(X0+px(gx-55),Y0+px(205),X0+px(gx+55),Y0+px(95),.9)
for g in range(4): ln(X0+20,Y0+px(230)+g*px(14),X0+px(GW)-20,Y0+px(230)+g*px(14),.7)
not_(X0+px(700),Y0+px(62),'SOĞUTMA ×2 — üstte (erişim üstten): sol grup −18 (alt bant) · sağ grup +3 (üst bölge)',fs=9)
ln(X0+8,Y0+px(300),X0+px(GW)-8,Y0+px(300),1.8)
# +3 bolgesi 300-1270: sol icecek / sag taze
xm = X0+px(700)
ln(xm,Y0+px(300),xm,Y0+px(1270),1,'#111','5,4')
tx(X0+px(350),Y0+px(325),'+3 °C — İÇECEK + TATLI + 1 L (sol)',9.5,'middle','bold')
tx(X0+px(1050),Y0+px(325),'+3 °C — TAZE HAMUR 8 çekmece × 20 = 160 (2 gün) (sağ)',9.5,'middle','bold')
# icecek 4 cekmece
for k in range(4):
    cy = Y0+px(345)+k*px(128)
    rc(X0+px(30),cy,px(640),px(118),1.5,3)
    for i in range(7): rc(X0+px(42)+i*px(90),cy+px(8),px(76),px(102),1)
    ln(X0+px(330),cy+px(112),X0+px(370),cy+px(112),2.2)
not_(X0+px(350),Y0+px(870),'4 çekmece × 7 kanal = 28 (kutu 24 · tatlı 3 · yedek 1) — dik kutu + yaylı itici',fs=8)
# 1L cekmecesi
rc(X0+px(30),Y0+px(890),px(640),px(360),1.6,3)
for i in range(5): rc(X0+px(55)+i*px(124),Y0+px(908),px(100),px(324),1)
ln(X0+px(330),Y0+px(1244),X0+px(370),Y0+px(1244),2.2)
not_(X0+px(350),Y0+px(1268),'1 L çekmecesi — 5 kanal × 8 (plan 25 + yedek)',fs=8)
# taze 8 cekmece
for r in range(8):
    cy = Y0+px(345)+r*px(116)
    rc(X0+px(730),cy,px(640),px(106),1.4,3)
    for i in range(4):
        ci(X0+px(800)+i*px(165),cy+px(48),px(42),1); el(X0+px(800)+i*px(165),cy+px(95),px(52),px(7),.8)
    ln(X0+px(1030),cy+px(100),X0+px(1070),cy+px(100),2.2)
not_(X0+px(1050),Y0+px(1268),'çukurlu silikon GN 2/1 tepsi (20 top) — çekmece 12 cm aralık',fs=8)
# yatay izoleli ayirici 1270-1320
rc(X0+8,Y0+px(1270),px(GW)-16,px(50),1.8,0,'#111',None,'#eee')
tx(X0+px(700),Y0+px(1305),'YATAY İZOLELİ AYIRICI — tek parça, tam genişlik (üstü +3 · altı −18)',8.5,'middle','bold')
# −18 bandi 1320-1850
rc(X0+8,Y0+px(1320),px(GW)-16,px(530),1.2,0,'#1a49b8',None,'rgba(26,73,184,0.04)')
tx(X0+px(700),Y0+px(1345),'−18 °C — ALT BUZLUK tam genişlik (soğuk hava dibe çöker, tek evaporatör)',9.5,'middle','bold',Bl)
for k in range(2):
    cy = Y0+px(1360)+k*px(128)
    rc(X0+px(30),cy,px(1340),px(118),1.5,3,Bl)
    for i in range(8):
        ci(X0+px(115)+i*px(165),cy+px(52),px(44),1,Bl); el(X0+px(115)+i*px(165),cy+px(104),px(54),px(7),.8,Bl)
    ln(X0+px(680),cy+px(112),X0+px(720),cy+px(112),2.2,Bl)
    tx(X0+px(1380)+6,cy+px(70),'2 tepsi yan yana = 40 top',7.5,'start','',Bl)
rc(X0+px(30),Y0+px(1620),px(1340),px(215),1.5,3,Bl)
for i,ad in enumerate(('KAVURMA','KAVURMA','KUŞBAŞI','KUŞBAŞI')):
    rc(X0+px(60)+i*px(180),Y0+px(1635),px(170),px(185),1.3,2,Bl,None,'#eef2fb')
    rc(X0+px(60)+i*px(180)+px(150),Y0+px(1690),px(14),px(60),1,1,Bl)
    tx(X0+px(145)+i*px(180),Y0+px(1725),ad,7.5,'middle','bold',Bl); tx(X0+px(145)+i*px(180),Y0+px(1750),'17×21×25 · −18',6.5,'middle','',Bl)
rc(X0+px(800),Y0+px(1635),px(540),px(185),1,2,'#999','4,3'); tx(X0+px(1070),Y0+px(1735),'büyüme (5.-6. malzeme / yedek)',7.5,'middle','','#999')
ln(X0+px(680),Y0+px(1828),X0+px(720),Y0+px(1828),2.2,Bl)
not_(X0+px(700),Y0+px(1852)-4,'',fs=1)
# olculer
oy(X0,xm,Y0-2+px(26),'70'); oy(xm,X0+px(GW),Y0-2+px(26),'70')
oy(X0,X0+px(GW),YZ+30,'140')
ox(X0-34,Y0,YT,'185'); ox(X0-34,YT,YZ,'12'); ox(X0-70,Y0,YZ,'197')
xr = X0+px(GW)+22
ox(xr,Y0+px(10),Y0+px(290),'soğutma 28',side='r'); ox(xr,Y0+px(300),Y0+px(1270),'+3 · 97',side='r'); ox(xr,Y0+px(1270),Y0+px(1320),'5',side='r'); ox(xr,Y0+px(1320),Y0+px(1850),'−18 · 53',side='r')

# ================= YAN KESIT =================
sx = X0+px(GW)+140
tx(sx+px(DER)/2,Y0-18,'YAN KESİT (sağ kolon)',12.5,'middle','bold')
rc(sx,Y0,px(DER),px(GH),2.2,5)
rc(sx+12,YT,12,px(AYAK)); rc(sx+px(DER)-24,YT,12,px(AYAK))
ln(sx-40,YZ,sx+px(DER)+40,YZ,2)
rc(sx+8,Y0+px(10),px(DER)-16,px(280),1.4,3); tx(sx+px(420),Y0+px(160),'soğutma',9)
ln(sx+8,Y0+px(300),sx+px(DER)-8,Y0+px(300),1.6)
for r in range(8):
    cy = Y0+px(345)+r*px(116)
    rc(sx+px(20),cy,px(30),px(106),1.4,1,'#111',None,'#ddd')            # izoleli on yuz (kapak)
    ln(sx+px(50),cy+px(100),sx+px(780),cy+px(100),1.2)                    # tepsi/raf
    for i in range(5): ci(sx+px(120)+i*px(140),cy+px(52),px(40),.9)
rc(sx+8,Y0+px(1270),px(DER)-16,px(50),1.8,0,'#111',None,'#eee')
rc(sx+8,Y0+px(1320),px(DER)-16,px(530),1,0,Bl,None,'rgba(26,73,184,0.04)')
for k in range(2):
    cy = Y0+px(1360)+k*px(128)
    rc(sx+px(20),cy,px(30),px(118),1.4,1,Bl,None,'#dfe7fb'); ln(sx+px(50),cy+px(112),sx+px(780),cy+px(112),1.2,Bl)
    for i in range(5): ci(sx+px(120)+i*px(140),cy+px(56),px(40),.9,Bl)
rc(sx+px(20),Y0+px(1620),px(30),px(215),1.4,1,Bl,None,'#dfe7fb'); ln(sx+px(50),Y0+px(1830),sx+px(780),Y0+px(1830),1.2,Bl)
for i in range(2): rc(sx+px(80)+i*px(230),Y0+px(1640),px(210),px(180),1.2,2,Bl)
# cekmece acilis oku
E.append('<path d="M %.1f %.1f L %.1f %.1f" stroke="#1d7a4f" stroke-width="1.6" stroke-dasharray="4,3" fill="none"/>' % (sx+px(20),Y0+px(690),sx-px(160),Y0+px(690)))
tx(sx-px(80),Y0+px(675),'çekmece motorla öne',8,'middle','',G); tx(sx-px(80),Y0+px(715),'kol üstten alır',8,'middle','',G)
ln(sx,Y0+px(60),sx,Y0+px(1850),3,'#2a6a9a')
E.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="10" fill="#2a6a9a" font-family="Arial" font-weight="bold" transform="rotate(-90 %.1f %.1f)">ROBOT + ELEMAN CEPHESİ — KAPAK YOK</text>' % (sx-16,Y0+px(1000),sx-16,Y0+px(1000)))
tx(sx+px(420),Y0+px(1560),'izoleli ön yüz = her çekmecenin kendi kapağı',8,'middle','','#333')
oy(sx,sx+px(DER),YZ+30,'84')
ox(sx+px(DER)+34,Y0,YZ,'197')

# ================= NOTLAR =================
nx = sx+px(DER)+90
tx(nx,Y0+10,'KARARLAR (STORE v1 — 4 Eyl):',12.5,'start','bold')
nots = [
 ('· KAPAK YOK, CAM YOK — tümü çekmece','bold','#1a1a1a'),
 ('  her çekmecenin ön yüzü izoleli = kapağı;','','#666'),
 ('  robot yalnız çektiğini açar, eleman','','#666'),
 ('  haftalık dolumda sırayla çeker','','#666'),
 ('· −18 EN ALTTA, tam genişlik (Kemal):','bold','#1a49b8'),
 ('  soğuk hava dibe çöker → verim ↑,','','#666'),
 ('  tek evaporatör, 3 çekmece / 5 motor az','','#666'),
 ('· Hamur −18: 2 çekmece × 2 tepsi = 80 (1 gün)','','#333'),
 ('· Kaset çekmecesi: kavurma ×2 + kuşbaşı ×2','','#333'),
 ('  (17×21×25) + büyüme yeri; robot bitişten','','#666'),
 ('  1 gün önce alır → TOPPING arka sıra','','#666'),
 ('· +3 sol: içecek 4 × 7 kanal (28) + 1 L (40)','','#333'),
 ('· +3 sağ: taze 8 × 20 = 160 (2 gün)','','#333'),
 ('· Yatay izoleli ayırıcı tek parça, tam en','','#333'),
 ('· Soğutma ×2 ÜSTTE: −18 grubu + +3 grubu','','#333'),
 ('· Dikey bütçe: 28 + 97 + 5 + 53 = 183 + 2','','#333'),
 ('· Bedel: eleman 80 top + 4 kaseti alt','','#b3452b'),
 ('  çekmecelere eğilerek koyar (haftada 1)','','#b3452b'),
 ('· Robot: alçak çekmece sorun değil (kol','','#666'),
 ('  15-50 cm seviyesine iner)','','#666'),
 ('· Fırıncı 3 günde bir 240 top: 160 taze','','#333'),
 ('  + 80 şoklu; içecek/kaset haftalık','','#333'),
]
yy = Y0+34
for s_,w_,c_ in nots:
    tx(nx,yy,s_,10.3,'start',w_,c_)
    yy += 19.5

tx(W-24,H-14,'AUTOKITCH · ist1_store_detay_v1',10,'end','','#999')
svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d"><rect width="%d" height="%d" fill="#ffffff"/>%s</svg>' % (W,H,W,H,W,H,''.join(E))
OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\1_STORE\ist1_store_detay_v1.svg"
io.open(OUT,'w',encoding='utf-8').write(svg)
print('yazildi:', OUT)
