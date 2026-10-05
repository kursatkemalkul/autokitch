# -*- coding: utf-8 -*-
# IST.2 PRES — tek istasyon DETAY cizimi v1 (on gorunus + yan kesit)
# Kabin onerisi 70 -> 100 (PZP 64 zeminde + cop kolonu 30 + uc istasyonu ustte)
import io

S = 0.5
def px(mm): return mm*S
W, H = 1500, 1320
E = []
def ln(x1,y1,x2,y2,w=1.4,c='#111',dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    E.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s/>' % (x1,y1,x2,y2,c,w,d))
def rc(x,y,w_,h,sw=1.4,rx=0,c='#111',dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    E.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="none" stroke="%s" stroke-width="%s"%s/>' % (x,y,w_,h,rx,c,sw,d))
def ci(cx,cy,r,sw=1.4,c='#111',dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    E.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-width="%s"%s/>' % (cx,cy,r,c,sw,d))
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

GW, GH, AYAK, DER = 1000, 1850, 120, 840   # mm
X0, Y0 = 110, 150
YT = Y0+px(GH); YZ = YT+px(AYAK)

tx(X0,Y0-96,'İSTASYON 2 — PRES · DETAY ÇİZİMİ v1',17,'start','bold')
tx(X0,Y0-72,'Kabin önerisi: 70 → 100 cm (PZP-400 zeminde 64 en + çöp kolonu 30 + üstte robot uç istasyonu) — hat toplamı 415 → 445',11,'start','','#555')
tx(X0,Y0-54,'İsimler: 1 KİLER · 2 PRES · 3 DOLUM · 4 FIRIN · 5 PAKET · 6 TESLİM (+SERVİS) — öneri',11,'start','','#555')

# ================= ON GORUNUS =================
tx(X0+px(GW)/2,Y0-18,'ÖN GÖRÜNÜŞ (robot tarafı — cephe açık)',12.5,'middle','bold')
rc(X0,Y0,px(GW),px(GH),2.2,5)
rc(X0+12,YT,12,px(AYAK)); rc(X0+px(GW)-24,YT,12,px(AYAK))
ln(X0-40,YZ,X0+px(GW)+40,YZ,2)

# ic bolme: sol PZP kolonu 0-660, sag cop kolonu 660-1000
xB = X0+px(660)
ln(xB,Y0+px(60),xB,YT-6,1.2,'#111','7,5')

# --- SOL: ust bant kontrol + pnomatik (y 60-240)
rc(X0+px(40),Y0+px(70),px(280),px(150),1.2,3)
tx(X0+px(180),Y0+px(155),'PLC I/O + valf',9.5)
not_(X0+px(330),Y0+px(155),'· pnömatik hat (uç kilidi için)')

# --- SOL: UC ISTASYONU (dock) y 280-830
rc(X0+px(30),Y0+px(280),px(600),px(560),1.6,4)
tx(X0+px(330),Y0+px(330),'ROBOT UÇ İSTASYONU (dock)',11,'middle','bold')
# cep 1: kurek
rc(X0+px(70),Y0+px(400),px(220),px(60),1.2,2)          # pin plakasi
ln(X0+px(90),Y0+px(460),X0+px(90),Y0+px(500),1.2); ln(X0+px(270),Y0+px(460),X0+px(270),Y0+px(500),1.2)  # pinler
rc(X0+px(60),Y0+px(520),px(240),px(28),1.4,2)          # kurek yuzu (yatay)
not_(X0+px(180),Y0+px(590),'CEP 1: kürek/spatula ucu')
# cep 2: yedek pence
rc(X0+px(360),Y0+px(400),px(220),px(60),1.2,2)
ln(X0+px(380),Y0+px(460),X0+px(380),Y0+px(500),1.2); ln(X0+px(560),Y0+px(460),X0+px(560),Y0+px(500),1.2)
ln(X0+px(420),Y0+px(520),X0+px(470),Y0+px(600),1.4); ln(X0+px(520),Y0+px(520),X0+px(470),Y0+px(600),1.4)  # V pence
not_(X0+px(470),Y0+px(640),'CEP 2: YEDEK kombine el')
not_(X0+px(330),Y0+px(720),'pin + burç hizalama · her cepte "uç var" sensörü')
not_(X0+px(330),Y0+px(760),'robot kilidi pnömatik açar/kapar — İNSAN ELİ DEĞMEZ')
not_(X0+px(330),Y0+px(800),'(SMARTSHIFT / RSP CoboShift sınıfı)')

# --- SOL: PZP-400 zeminde (y 900-1850)
rc(X0+px(10),Y0+px(900),px(640),px(950),1.8,3)
tx(X0+px(330),Y0+px(960),'FERSAH PZP-400 (zeminde — 170 kg)',10.5,'middle','bold')
# gövde ici: ust plaka + silindir + tabla
rc(X0+px(200),Y0+px(1000),px(260),px(120),1.4,3)       # ust plaka kafasi
ln(X0+px(330),Y0+px(1120),X0+px(330),Y0+px(1210),1.6)  # mil
rc(X0+px(150),Y0+px(1210),px(360),px(40),1.4,2)        # isitmali ust plaka
not_(X0+px(330),Y0+px(1290),'ısıtmalı ÜST PLAKA (~90 °C · yapışmaz)')
el(X0+px(330),Y0+px(1390),px(180),px(22))              # tabla
tx(X0+px(330),Y0+px(1370),'tabla Ø28 — zeminden ~90',9.5)
rc(X0+px(60),Y0+px(1500),px(540),px(300),1.2,3)        # alt govde
not_(X0+px(330),Y0+px(1660),'motor + rezistans gövdesi · 3,5 kW · 220 V')

# --- SAG: COP KOLONU (30)
tx((xB+X0+px(GW))/2,Y0+px(330),'ÇÖP',11,'middle','bold')
# huni
ln(xB+px(40),Y0+px(420),xB+px(140),Y0+px(560),1.6); ln(X0+px(GW)-px(40),Y0+px(420),X0+px(GW)-px(140),Y0+px(560),1.6)
ln(xB+px(40),Y0+px(420),X0+px(GW)-px(40),Y0+px(420),1.6)
not_((xB+X0+px(GW))/2,Y0+px(395),'huni ağzı ~Ø26 — robot bırakır, durmaz')
# saft
ln(xB+px(140),Y0+px(560),xB+px(140),Y0+px(1150),1,'#111','5,4')
ln(X0+px(GW)-px(140),Y0+px(560),X0+px(GW)-px(140),Y0+px(1150),1,'#111','5,4')
# kova
rc(xB+px(60),Y0+px(1180),px(220),px(560),1.6,4)
ln(xB+px(60),Y0+px(1240),xB+px(280),Y0+px(1240),1)      # poset kenari
not_((xB+X0+px(GW))/2,Y0+px(1160),'poşet kelepçesi')
tx((xB+X0+px(GW))/2,Y0+px(1480),'KOVA 30 L',10.5,'middle','bold')
not_((xB+X0+px(GW))/2,Y0+px(1560),'3 günde ~5 L dolar')
not_((xB+X0+px(GW))/2,Y0+px(1600),'boşaltma: fırıncı ziyaretinde')
# kizak
ln(xB+px(50),Y0+px(1790),xB+px(290),Y0+px(1790),1.6)
not_((xB+X0+px(GW))/2,Y0+px(1830),'öne çekilir — MOTORSUZ')

# olculer on
oy(X0,xB,Y0-2+px(28),'66'); oy(xB,X0+px(GW),Y0-2+px(28),'34')
oy(X0,X0+px(GW),YZ+30,'100 (öneri — eski 70)')
ox(X0-34,Y0,YT,'185'); ox(X0-34,YT,YZ,'12'); ox(X0-70,Y0,YZ,'197')

# ================= YAN KESIT =================
sx = X0+px(GW)+170
tx(sx+px(DER)/2,Y0-18,'YAN KESİT (PZP hizasından)',12.5,'middle','bold')
rc(sx,Y0,px(DER),px(GH),2.2,5)
rc(sx+12,YT,12,px(AYAK)); rc(sx+px(DER)-24,YT,12,px(AYAK))
ln(sx-40,YZ,sx+px(DER)+40,YZ,2)
# PZP govde derinligi 800
rc(sx+px(20),Y0+px(900),px(800),px(950),1.6,3)
tx(sx+px(420),Y0+px(1000),'PZP-400',10,'middle','bold')
tx(sx+px(420),Y0+px(1022),'derinlik 80',9.5)
el(sx+px(300),Y0+px(1390),px(170),px(20))
tx(sx+px(300),Y0+px(1365),'tabla',9)
# uc istasyonu yan
rc(sx+px(60),Y0+px(280),px(500),px(560),1.4,4)
tx(sx+px(310),Y0+px(560),'uç istasyonu',9.5)
# on aciklik (robot tarafi)
ln(sx,Y0+px(250),sx,Y0+px(1850),3,'#2a6a9a')
tx(sx-14,Y0+px(1000),'',9)
E.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="10" fill="#2a6a9a" font-family="Arial" font-weight="bold" transform="rotate(-90 %.1f %.1f)">ROBOT CEPHESİ — AÇIK</text>' % (sx-16,Y0+px(1050),sx-16,Y0+px(1050)))
oy(sx,sx+px(DER),YZ+30,'84')
ox(sx+px(DER)+34,Y0,YZ,'197')

# ================= NOTLAR =================
nx = sx+px(DER)+120
tx(nx,Y0+10,'KARARLAR / SORULAR:',12.5,'start','bold')
nots = [
 '· PZP-400 TEYİT: 64×80×95 · 170 kg',
 '  3,5 kW · 220 V · 500-700 ad/saat',
 '  (Fersah resmî sayfası)',
 '· UN GEREKMEZ — ısıtmalı pres,',
 '  yapışmaz plaka; gerekirse hafif',
 '  yağ. Plaka kaplaması Fersah&apos;a',
 '  sorulacak (teflon/krom?)',
 '· Temizlik: ziyarette İNSAN siler;',
 '  uçlar sökülüp yıkanır (COP) —',
 '  otomatik yıkama GEREKSİZ',
 '· Uç istasyonu: robot ucu kendisi',
 '  takar/bırakır (pnömatik kilit,',
 '  hazır kit: SMARTSHIFT / RSP /',
 '  TripleA Wingman sınıfı)',
 '· Çöp: 30 L · motorsuz · poşetli',
 '  huniden bırak-geç · 3 günde bir',
 '  boşaltma (fırıncı ziyareti)',
 '· KABİN 70→100 ONAY BEKLİYOR',
 '  (hat 415 → 445)',
]
yy = Y0+34
for s_ in nots:
    tx(nx,yy,s_,10.5,'start','' if s_.startswith('  ') else ('bold' if 'ONAY' in s_ else ''),'#333' if not s_.startswith('  ') else '#666')
    yy += 20

tx(W-24,H-14,'AUTOKITCH · ist2_pres_detay_v1',10,'end','','#999')

svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d"><rect width="%d" height="%d" fill="#ffffff"/>%s</svg>' % (W,H,W,H,W,H,''.join(E))
OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\ist2_pres_detay_v1.svg"
io.open(OUT,'w',encoding='utf-8').write(svg)
print('yazildi:', OUT)
