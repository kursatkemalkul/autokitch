# -*- coding: utf-8 -*-
# IST.3 TOPPING — tek istasyon DETAY v1 (mevcut karar: dozaj kulesi konsepti)
# Dozaj MEKANIZMASI ACIK — piyasa arastirmasi suruyor
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

GW, GH, AYAK, DER = 700, 1850, 120, 840
X0, Y0 = 110, 150
YT = Y0+px(GH); YZ = YT+px(AYAK)

tx(X0,Y0-96,'İSTASYON 3 — TOPPING · DETAY ÇİZİMİ v1',17,'start','bold')
tx(X0,Y0-72,'Mevcut karar (konsept A — dozaj kulesi): 3 soğutmalı hazne + döner tabla. DOZAJ MEKANİZMASI AÇIK — piyasa araştırması sürüyor.',11,'start','','#555')
tx(X0,Y0-54,'Günlük: kaşar ~6,5 kg · sucuk ~1,3 kg (8-10 dilim/pide) · kavurma ~1,2 kg — hazneler 2-3 günlük, ELEMAN doldurur',11,'start','','#555')

# ================= ON GORUNUS =================
tx(X0+px(GW)/2,Y0-18,'ÖN GÖRÜNÜŞ (robot tarafı)',12.5,'middle','bold')
rc(X0,Y0,px(GW),px(GH),2.2,5)
rc(X0+12,YT,12,px(AYAK)); rc(X0+px(GW)-24,YT,12,px(AYAK))
ln(X0-40,YZ,X0+px(GW)+40,YZ,2)

# hazne bolgesi cerceve (+3 sogutma ceketi)
rc(X0+px(25),Y0+px(70),px(650),px(760),1.6,4)
tx(X0+px(350),Y0+px(120),'HAZNE BÖLGESİ — soğutmalı +3 °C',10.5,'middle','bold')
# arka hazne (kesik)
rc(X0+px(230),Y0+px(160),px(240),px(300),1.2,3,'#777','5,4')
ln(X0+px(230),Y0+px(460),X0+px(310),Y0+px(560),1.1,'#777','5,4')
ln(X0+px(470),Y0+px(460),X0+px(390),Y0+px(560),1.1,'#777','5,4')
not_(X0+px(350),Y0+px(320),'H3 KAVURMA')
not_(X0+px(350),Y0+px(360),'(arkada)')
# on iki hazne
for cx0,lab in ((170,'H1 KAŞAR (rende)'),(530,'H2 SUCUK (dilim kartuşu)')):
    rc(X0+px(cx0-120),Y0+px(200),px(240),px(330),1.5,3)
    ln(X0+px(cx0-120),Y0+px(530),X0+px(cx0-40),Y0+px(640),1.4)
    ln(X0+px(cx0+120),Y0+px(530),X0+px(cx0+40),Y0+px(640),1.4)
    tx(X0+px(cx0),Y0+px(185),lab,9.5)
# dozaj kapilari
for cx0 in (170,350,530):
    rc(X0+px(cx0-45),Y0+px(650),px(90),px(60),1.5,2)
tx(X0+px(350),Y0+px(750),'DOZAJ BAŞLIKLARI — mekanizma AÇIK (araştırma):',10,'middle','bold','#b3452b')
not_(X0+px(350),Y0+px(790),'kaşar=serpme? · sucuk=dilim itici? · kavurma=vidalı?')

# dusus oklari + doner tabla
for cx0 in (170,350,530):
    ln(X0+px(cx0),Y0+px(710),X0+px(cx0),Y0+px(900),1,'#777','3,3')
el(X0+px(350),Y0+px(950),px(200),px(24))
el(X0+px(350),Y0+px(938),px(140),px(16),1.1)
tx(X0+px(350),Y0+px(915),'pide Ø28',9)
not_(X0+px(350),Y0+px(1010),'DÖNER TABLA Ø40 — taban döner, kanal sabit')
not_(X0+px(350),Y0+px(1050),'(eşit dağılım) · zeminden ~90')

# alt bolge: motor + kuvetler
ln(X0+px(15),Y0+px(1100),X0+px(GW)-px(15),Y0+px(1100),1.2,'#111','7,5')
rc(X0+px(40),Y0+px(1150),px(220),px(420),1.4,3)
ci(X0+px(150),Y0+px(1300),px(70),1.2)
tx(X0+px(150),Y0+px(1520),'soğutma',9.5); tx(X0+px(150),Y0+px(1545),'motoru',9.5)
for r in range(3):
    for c in range(2):
        rc(X0+px(300+c*180),Y0+px(1150+r*215),px(160),px(190),1.2,3)
not_(X0+px(480),Y0+px(1790),'GN 1/2 küvet ×9 (2 sıra derin) — yedek malzeme +3°')

# olculer
oy(X0,X0+px(GW),YZ+30,'70')
ox(X0-34,Y0,YT,'185'); ox(X0-34,YT,YZ,'12'); ox(X0-70,Y0,YZ,'197')

# ================= YAN KESIT =================
sx = X0+px(GW)+180
tx(sx+px(DER)/2,Y0-18,'YAN KESİT',12.5,'middle','bold')
rc(sx,Y0,px(DER),px(GH),2.2,5)
rc(sx+12,YT,12,px(AYAK)); rc(sx+px(DER)-24,YT,12,px(AYAK))
ln(sx-40,YZ,sx+px(DER)+40,YZ,2)
# on hazne + arka hazne
rc(sx+px(60),Y0+px(200),px(300),px(330),1.5,3)
tx(sx+px(210),Y0+px(380),'ön hazne',9)
rc(sx+px(460),Y0+px(200),px(300),px(330),1.5,3)
tx(sx+px(610),Y0+px(380),'arka hazne',9)
not_(sx+px(420),Y0+px(120),'hazneler 2 önde + 1 arkada')
# tabla
el(sx+px(260),Y0+px(950),px(180),px(20))
tx(sx+px(260),Y0+px(920),'döner tabla',9)
# kuvetler
rc(sx+px(80),Y0+px(1150),px(640),px(620),1.2,3,'#777','5,4')
tx(sx+px(400),Y0+px(1470),'küvetler (2 derin)',9.5,'middle','','#777')
ln(sx,Y0+px(60),sx,Y0+px(1850),3,'#2a6a9a')
E.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="10" fill="#2a6a9a" font-family="Arial" font-weight="bold" transform="rotate(-90 %.1f %.1f)">ROBOT CEPHESİ — AÇIK</text>' % (sx-16,Y0+px(1050),sx-16,Y0+px(1050)))
not_(sx+px(420),Y0+px(1810),'hazne DOLUM kapağı: üstten/önden — ELEMAN doldurur (yerleşimle netleşir)')
oy(sx,sx+px(DER),YZ+30,'84')
ox(sx+px(DER)+34,Y0,YZ,'197')

# ================= NOTLAR =================
nx = sx+px(DER)+120
tx(nx,Y0+10,'DURUM:',12.5,'start','bold')
nots = [
 ('· Menü: kaşarlı · sucuklu ·','','#333'),
 ('  kavurmalı · karışık','','#666'),
 ('· Miktarlar (pide başına):','','#333'),
 ('  kaşar ~80 g · sucuk 8-10 dilim','','#666'),
 ('  · kavurma ~60 g','','#666'),
 ('· Hazneler soğutmalı +3 °C:','','#333'),
 ('  kaşar rende 2-3 hafta dayanır,','','#666'),
 ('  sucuk vakumlu, kavurma küvetten','','#666'),
 ('· Dolum: ELEMAN (dükkânda hep var)','','#333'),
 ('  hazne 2-3 günlük, küvetten takviye','','#666'),
 ('· Pide DÖNER TABLADA döner —','','#333'),
 ('  malzeme sabit noktadan yağar','','#666'),
 ('· AÇIK: dozaj mekanizmaları','bold','#b3452b'),
 ('  (kaşar/sucuk/kavurma) —','','#b3452b'),
 ('  piyasa araştırması SÜRÜYOR;','','#b3452b'),
 ('  hazır sistem bulunursa bu','','#666'),
 ('  çizim ona göre revize edilir','','#666'),
]
yy = Y0+34
for s_,w_,c_ in nots:
    tx(nx,yy,s_,10.5,'start',w_,c_)
    yy += 20

tx(W-24,H-14,'AUTOKITCH · ist3_topping_detay_v1',10,'end','','#999')

svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d"><rect width="%d" height="%d" fill="#ffffff"/>%s</svg>' % (W,H,W,H,W,H,''.join(E))
OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\ist3_topping_detay_v1.svg"
io.open(OUT,'w',encoding='utf-8').write(svg)
print('yazildi:', OUT)
