# -*- coding: utf-8 -*-
# IST.2 PRES — DETAY v3: kabin 70 KALDI; PZP ustu bosluk optimum:
# solda uc cepleri (dikey 2 cep), sagda cop (huni+kova) — yan yana, bosluk yok
import io

S = 0.5
def px(mm): return mm*S
W, H = 1420, 1320
E = []
def ln(x1,y1,x2,y2,w=1.4,c='#111',dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    E.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s/>' % (x1,y1,x2,y2,c,w,d))
def rc(x,y,w_,h,sw=1.4,rx=0,c='#111',dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    E.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="none" stroke="%s" stroke-width="%s"%s/>' % (x,y,w_,h,rx,c,sw,d))
def ci(cx,cy,r,sw=1.4,c='#111'):
    E.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-width="%s"/>' % (cx,cy,r,c,sw))
def el(cx,cy,rx,ry,sw=1.4):
    E.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="none" stroke="#111" stroke-width="%s"/>' % (cx,cy,rx,ry,sw))
def tx(x,y,s,fs=11,a='middle',w='',col='#111'):
    fw = ' font-weight="%s"' % w if w else ''
    E.append('<text x="%.1f" y="%.1f" text-anchor="%s" font-size="%s" fill="%s" font-family="Arial"%s>%s</text>' % (x,y,a,fs,col,fw,s))
def not_(x,y,s): tx(x,y,s,10,'middle','','#555')
def oy(x1,x2,y,cm,fs=11):
    ln(x1,y,x2,y,1); ln(x1,y-5,x1,y+5,1); ln(x2,y-5,x2,y+5,1)
    tx((x1+x2)/2,y-6,cm,fs)
def ox(x,y1,y2,cm,fs=11):
    ln(x,y1,x,y2,1); ln(x-5,y1,x+5,y1,1); ln(x-5,y2,x+5,y2,1)
    E.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="%s" fill="#111" font-family="Arial" transform="rotate(-90 %.1f %.1f)">%s</text>' % (x-9,(y1+y2)/2,fs,x-9,(y1+y2)/2,cm))

GW, GH, AYAK, DER = 700, 1850, 120, 840
X0, Y0 = 110, 150
YT = Y0+px(GH); YZ = YT+px(AYAK)

tx(X0,Y0-96,'İSTASYON 2 — PRES · DETAY ÇİZİMİ v3',17,'start','bold')
tx(X0,Y0-72,'KABİN 70 KALDI (hat 415 aynı) — PZP üstü boşluk OPTİMUM: solda uç cepleri (dikey), sağda çöp; aralarda boşluk yok',11,'start','','#555')
tx(X0,Y0-54,'İsimler: 1 KİLER · 2 PRES · 3 DOLUM · 4 FIRIN · 5 PAKET · 6 TESLİM (+SERVİS) — öneri',11,'start','','#555')

# ================= ON GORUNUS =================
tx(X0+px(GW)/2,Y0-18,'ÖN GÖRÜNÜŞ (robot tarafı — cephe açık)',12.5,'middle','bold')
rc(X0,Y0,px(GW),px(GH),2.2,5)
rc(X0+12,YT,12,px(AYAK)); rc(X0+px(GW)-24,YT,12,px(AYAK))
ln(X0-40,YZ,X0+px(GW)+40,YZ,2)

# --- PZP-400 zeminde (y 900-1850) — kabini dolduruyor
rc(X0+px(15),Y0+px(900),px(670),px(950),1.8,3)
tx(X0+px(350),Y0+px(960),'FERSAH PZP-400 (zeminde — 170 kg · en 64)',10.5,'middle','bold')
rc(X0+px(220),Y0+px(1010),px(260),px(110),1.4,3)
ln(X0+px(350),Y0+px(1120),X0+px(350),Y0+px(1200),1.6)
rc(X0+px(170),Y0+px(1200),px(360),px(40),1.4,2)
not_(X0+px(350),Y0+px(1285),'ısıtmalı ÜST PLAKA (~90 °C · yapışmaz — UN YOK)')
el(X0+px(350),Y0+px(1385),px(180),px(22))
tx(X0+px(350),Y0+px(1362),'tabla Ø28 — zeminden ~90',9.5)
rc(X0+px(80),Y0+px(1490),px(540),px(310),1.2,3)
not_(X0+px(350),Y0+px(1655),'motor + rezistans gövdesi · 3,5 kW · 220 V')

# --- UST BOLGE y 60-880: sol UC CEPLERI (0-330) / sag COP (340-680)
xB = X0+px(335)
ln(xB,Y0+px(50),xB,Y0+px(890),1.1,'#111','6,5')

# SOL: uc cepleri dikey
rc(X0+px(35),Y0+px(70),px(280),px(790),1.5,4)
tx(X0+px(175),Y0+px(115),'UÇ CEPLERİ',10.5,'middle','bold')
# CEP 1 (ust): kurek
rc(X0+px(105),Y0+px(170),px(140),px(36),1.2,2)
ln(X0+px(125),Y0+px(206),X0+px(125),Y0+px(235),1.1); ln(X0+px(225),Y0+px(206),X0+px(225),Y0+px(235),1.1)
rc(X0+px(65),Y0+px(248),px(220),px(22),1.3,2)
not_(X0+px(175),Y0+px(310),'CEP 1: kürek ucu')
# CEP 2 (orta): yedek el
rc(X0+px(105),Y0+px(380),px(140),px(36),1.2,2)
ln(X0+px(125),Y0+px(416),X0+px(125),Y0+px(445),1.1); ln(X0+px(225),Y0+px(416),X0+px(225),Y0+px(445),1.1)
ln(X0+px(135),Y0+px(458),X0+px(175),Y0+px(520),1.3); ln(X0+px(215),Y0+px(458),X0+px(175),Y0+px(520),1.3)
not_(X0+px(175),Y0+px(560),'CEP 2: yedek el')
# CEP 3 (alt): bos yuva
rc(X0+px(105),Y0+px(630),px(140),px(36),1.2,2,'#999','4,3')
not_(X0+px(175),Y0+px(700),'CEP 3: boş yuva')
not_(X0+px(175),Y0+px(775),'kilit Ø7-8 · pin+burç')
not_(X0+px(175),Y0+px(815),'"uç var" sensörü')

# SAG: cop — huni + kova
tx(X0+px(510),Y0+px(115),'ÇÖP',10.5,'middle','bold')
ln(X0+px(360),Y0+px(160),X0+px(430),Y0+px(330),1.6); ln(X0+px(660),Y0+px(160),X0+px(590),Y0+px(330),1.6)
ln(X0+px(360),Y0+px(160),X0+px(660),Y0+px(160),1.6)
not_(X0+px(510),Y0+px(140),'huni ağzı — robot bırakır, durmaz')
ln(X0+px(430),Y0+px(330),X0+px(430),Y0+px(370),1.2); ln(X0+px(590),Y0+px(330),X0+px(590),Y0+px(370),1.2)
rc(X0+px(400),Y0+px(380),px(220),px(470),1.6,4)
ln(X0+px(400),Y0+px(430),X0+px(620),Y0+px(430),1)
not_(X0+px(510),Y0+px(415),'poşet kelepçesi')
tx(X0+px(510),Y0+px(600),'KOVA 30 L',10.5,'middle','bold')
not_(X0+px(510),Y0+px(660),'3 günde ~5 L')
not_(X0+px(510),Y0+px(710),'kova bel hizasında —')
not_(X0+px(510),Y0+px(750),'öne çekilir, MOTORSUZ')
not_(X0+px(510),Y0+px(800),'boşaltma: fırıncı ziyareti')

# olculer
oy(X0,xB,Y0-2+px(26),'33'); oy(xB,X0+px(GW),Y0-2+px(26),'37')
oy(X0,X0+px(GW),YZ+30,'70 — DEĞİŞMEDİ')
ox(X0-34,Y0,YT,'185'); ox(X0-34,YT,YZ,'12'); ox(X0-70,Y0,YZ,'197')

# ================= YAN KESIT =================
sx = X0+px(GW)+180
tx(sx+px(DER)/2,Y0-18,'YAN KESİT',12.5,'middle','bold')
rc(sx,Y0,px(DER),px(GH),2.2,5)
rc(sx+12,YT,12,px(AYAK)); rc(sx+px(DER)-24,YT,12,px(AYAK))
ln(sx-40,YZ,sx+px(DER)+40,YZ,2)
rc(sx+px(20),Y0+px(900),px(800),px(950),1.6,3)
tx(sx+px(420),Y0+px(1000),'PZP-400 · derinlik 80',10,'middle','bold')
el(sx+px(300),Y0+px(1385),px(170),px(20))
tx(sx+px(300),Y0+px(1360),'tabla',9)
rc(sx+px(80),Y0+px(70),px(700),px(790),1.4,4)
tx(sx+px(430),Y0+px(430),'uç cepleri + çöp',9.5)
tx(sx+px(430),Y0+px(465),'(yan yana bant)',9.5)
ln(sx,Y0+px(60),sx,Y0+px(1850),3,'#2a6a9a')
E.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="10" fill="#2a6a9a" font-family="Arial" font-weight="bold" transform="rotate(-90 %.1f %.1f)">ROBOT CEPHESİ — AÇIK</text>' % (sx-16,Y0+px(1050),sx-16,Y0+px(1050)))
oy(sx,sx+px(DER),YZ+30,'84')
ox(sx+px(DER)+34,Y0,YZ,'197')

# ================= NOTLAR =================
nx = sx+px(DER)+120
tx(nx,Y0+10,'KARARLAR:',12.5,'start','bold')
nots = [
 ('· KABİN 70 — genişlemedi; hat 415','bold','#1a1a1a'),
 ('· PZP-400: 64×80×95 · 170 kg ·','','#333'),
 ('  3,5 kW · 220 V (teyitli)','','#666'),
 ('· PZP üstü boşluk tam dolu:','','#333'),
 ('  sol 33 = 3 uç yuvası (dikey),','','#666'),
 ('  sağ 37 = huni + 30 L kova','','#666'),
 ('· Robot ucu kendisi takar/bırakır','','#333'),
 ('  (pnömatik kilit, hazır kit)','','#666'),
 ('· UN GEREKMEZ — ısıtmalı pres;','','#333'),
 ('  temizlik insan/ziyarette (COP)','','#666'),
 ('· Çöp motorsuz: bırak-geç huni,','','#333'),
 ('  kova bel hizasında, poşetli','','#666'),
]
yy = Y0+34
for s_,w_,c_ in nots:
    tx(nx,yy,s_,10.5,'start',w_,c_)
    yy += 20

tx(W-24,H-14,'AUTOKITCH · ist2_pres_detay_v3',10,'end','','#999')

svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d"><rect width="%d" height="%d" fill="#ffffff"/>%s</svg>' % (W,H,W,H,W,H,''.join(E))
OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\ist2_pres_detay_v3.svg"
io.open(OUT,'w',encoding='utf-8').write(svg)
print('yazildi:', OUT)
