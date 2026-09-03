# -*- coding: utf-8 -*-
# IST.3 TOPPING v2 — KEMAL KONSEPTI: 4 hazne (KUP/PARCA malzeme, dilimleyici IPTAL)
# + hucreli tambur dozaj (pat dokulmez) + doner-KAYAR tabla (spiral kaplama)
import io, math

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
def tx(x,y,s,fs=11,a='middle',w='',col='#111'):
    fw = ' font-weight="%s"' % w if w else ''
    E.append('<text x="%.1f" y="%.1f" text-anchor="%s" font-size="%s" fill="%s" font-family="Arial"%s>%s</text>' % (x,y,a,fs,col,fw,s))
def not_(x,y,s): tx(x,y,s,10,'middle','','#555')
def arr(x1,y1,x2,y2,w=1.8,c='#1d7a4f'):
    ln(x1,y1,x2,y2,w,c)
    a = math.atan2(y2-y1,x2-x1)
    for da in (2.6,-2.6):
        ln(x2,y2,x2-9*math.cos(a+da),y2-9*math.sin(a+da),w,c)

W, H = 1560, 1150
tx(40,44,'İSTASYON 3 — TOPPING · DETAY v2 — KEMAL KONSEPTİ',17,'start','bold')
tx(40,68,'KÜP/PARÇA malzeme (Dominos yöntemi — dilimleyici İPTAL, baton takma işi YOK) · 4 hazne AYNI mekanizma: HÜCRELİ TAMBUR (pat dökülmez, cep cep verir) · tabla DÖNER + KAYAR (spiral kaplama)',10.5,'start','','#555')

# ================= PANEL 1: UST GORUNUM =================
S2 = 0.42
def p2(mm): return mm*S2
X1, Y1 = 70, 130
tx(X1+p2(350),Y1-16,'ÜST GÖRÜNÜM (senin krokinin teknik hâli)',12,'middle','bold')
rc(X1,Y1,p2(700),p2(840),2.2,5)
hazneler = [(180,210,'H1 KÜP SUCUK'),(520,210,'H2 KAŞAR'),(180,630,'H3 KAVURMA'),(520,630,'H4 KUŞBAŞI')]
for hx,hy,ad in hazneler:
    ci(X1+p2(hx),Y1+p2(hy),p2(125),1.6)
    parts = ad.split(' ',1)
    tx(X1+p2(hx),Y1+p2(hy)-4,parts[0],10,'middle','bold')
    tx(X1+p2(hx),Y1+p2(hy)+12,parts[1],8.5)
# nozuller merkez hattina iner (4 nozul tek sira)
for hx,hy,ny in ((180,210,330),(520,210,375),(180,630,510),(520,630,465)):
    ln(X1+p2(hx),Y1+p2(hy),X1+p2(350),Y1+p2(ny),1,'#777','4,3')
    ci(X1+p2(350),Y1+p2(ny),p2(18),1.3,'#b3452b')
tx(X1+p2(350)+p2(40),Y1+p2(330)+4,'nozüller (4)',8.5,'start','','#b3452b')
# tabla (altta - kesik) + kizak + spiral
ci(X1+p2(350),Y1+p2(420),p2(200),1.6,'#1a49b8','7,5')
ln(X1+p2(350),Y1+p2(150),X1+p2(350),Y1+p2(700),1.4,'#1a49b8','2,4')
arr(X1+p2(350),Y1+p2(560),X1+p2(350),Y1+p2(660),1.8,'#1a49b8')
# donme oku
E.append('<path d="M %.1f %.1f A %.1f %.1f 0 1 1 %.1f %.1f" fill="none" stroke="#1a49b8" stroke-width="1.6"/>' % (X1+p2(350)+p2(150),Y1+p2(420),p2(150),p2(150),X1+p2(350),Y1+p2(420)-p2(150)))
tx(X1+p2(350),Y1+p2(770),'TABLA (altta, kesik): DÖNER + kızakta KAYAR',9.5,'middle','bold','#1a49b8')
not_(X1+p2(350),Y1+p2(800),'dönme + ileri-geri = SPİRAL kaplama, dış+orta her yer dolar')

# ================= PANEL 2: YAN KESIT =================
S = 0.44
def px(mm): return mm*S
X2, Y2 = 520, 130
GH, AYAK = 1850, 120
YT = Y2+px(GH); YZ = YT+px(AYAK)
tx(X2+px(350),Y2-16,'YAN KESİT (mekanizma)',12,'middle','bold')
rc(X2,Y2,px(700),px(GH),2.2,5)
rc(X2+12,YT,12,px(AYAK)); rc(X2+px(700)-24,YT,12,px(AYAK))
ln(X2-40,YZ,X2+px(700)+40,YZ,2)
# sogutmali hazne bolgesi
rc(X2+px(25),Y2+px(60),px(650),px(760),1.4,4)
tx(X2+px(350),Y2+px(105),'4 hazne — soğutmalı +3 °C (2 önde + 2 arkada)',9.5,'middle','bold')
# on hazne kesiti (kupler taramali)
rc(X2+px(120),Y2+px(150),px(220),px(280),1.6,3)
for i in range(5):
    for j in range(3):
        rc(X2+px(140+i*40),Y2+px(180+j*70),px(26),px(26),.8)
ln(X2+px(120),Y2+px(430),X2+px(200),Y2+px(520),1.5); ln(X2+px(340),Y2+px(430),X2+px(260),Y2+px(520),1.5)
tx(X2+px(230),Y2+px(140),'küp/parça malzeme',8.5)
# arka hazne (kesik)
rc(X2+px(420),Y2+px(150),px(220),px(280),1.2,3,'#999','5,4')
tx(X2+px(530),Y2+px(300),'arka hazne',8.5,'middle','','#999')
# HUCRELI TAMBUR
tcx, tcy = X2+px(230), Y2+px(590)
ci(tcx,tcy,px(60),1.8)
for k in range(6):
    a = k*math.pi/3
    ln(tcx,tcy,tcx+px(60)*math.cos(a),tcy+px(60)*math.sin(a),1.1)
ci(tcx,tcy,px(10),1.2)
tx(tcx+px(85),tcy-px(30),'HÜCRELİ TAMBUR',9.5,'start','bold','#b3452b')
tx(tcx+px(85),tcy-px(30)+15,'yavaş döner; her cep 3-5 küp',8.5,'start','','#555')
tx(tcx+px(85),tcy-px(30)+29,'alır, CEP CEP bırakır — asla',8.5,'start','','#555')
tx(tcx+px(85),tcy-px(30)+43,'pat diye dökülmez; gramaj =',8.5,'start','','#555')
tx(tcx+px(85),tcy-px(30)+57,'cep sayısı (kalibrasyon kolay)',8.5,'start','','#555')
# nozul + dusme
ln(tcx-px(20),Y2+px(660),tcx-px(20),Y2+px(720),1.4); ln(tcx+px(20),Y2+px(660),tcx+px(20),Y2+px(720),1.4)
for dy in (740,770,800):
    ci(tcx,Y2+px(dy),px(9),.9,'#777')
# tabla + kizak
ty = Y2+px(880)
E.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="none" stroke="#111" stroke-width="1.6"/>' % (tcx,ty,px(160),px(16)))
tx(tcx,ty-px(30),'pide Ø28',8.5)
rc(X2+px(90),ty+px(30),px(520),px(36),1.4,2)
rc(tcx-px(70),ty+px(20),px(140),px(24),1.3,2)
arr(tcx+px(90),ty+px(42),tcx+px(230),ty+px(42),1.6,'#1a49b8')
arr(tcx-px(90),ty+px(42),tcx-px(120),ty+px(42),1.6,'#1a49b8')
not_(X2+px(350),ty+px(105),'KIZAK: tabla arabası nozül altında İLERİ-GERİ + tabla motoru DÖNDÜRÜR (2 eksen)')
# alt bolge
ln(X2+px(15),Y2+px(1180),X2+px(685),Y2+px(1180),1.2,'#111','7,5')
rc(X2+px(50),Y2+px(1230),px(200),px(400),1.3,3)
ci(X2+px(150),Y2+px(1370),px(60),1.1)
tx(X2+px(150),Y2+px(1580),'soğutma',8.5); tx(X2+px(150),Y2+px(1600),'motoru',8.5)
for r in range(2):
    for c in range(2):
        rc(X2+px(300+c*180),Y2+px(1230+r*215),px(160),px(190),1.1,3)
not_(X2+px(480),Y2+px(1720),'GN küvetler — yedek malzeme +3°')
tx(X2+px(350),YZ+22,'70 × 197 × 84 — kabin aynı',9.5,'middle','bold')

# ================= NOTLAR =================
NX = 1150
tx(NX,140,'KARARLAR (bu tur):',12.5,'start','bold')
nots = [
 ('· KÜP/PARÇA SUCUK (Dominos gibi) —','bold','#1d7a4f'),
 ('  dilimleyici + baton takma İPTAL;','','#1d7a4f'),
 ('  tedarik: kasaptan küp doğranmış','','#666'),
 ('· 4 HAZNE: küp sucuk · kaşar ·','bold','#333'),
 ('  kavurma · KUŞBAŞI','','#333'),
 ('· 4 hazne = AYNI mekanizma','bold','#333'),
 ('  (tek tasarım, tek yedek parça)','','#666'),
 ('· Dozaj: HÜCRELİ TAMBUR — senin','','#333'),
 ('  "parça parça versin" şartın;','','#666'),
 ('  hazne ağzı hiç tam açılmıyor','','#666'),
 ('· Dağılım: tabla DÖNER + KAYAR —','','#333'),
 ('  önce dış halka, içeri doğru','','#666'),
 ('  spiral; orta da dış da dolar','','#666'),
 ('','',''),
 ('DİKKAT — KUŞBAŞI (T7, deftere):','bold','#b3452b'),
 ('· Çiğ kuşbaşı 2-3 dk fırında','','#b3452b'),
 ('  PİŞMEZ → önceden soteli/yarı','','#b3452b'),
 ('  pişmiş kuşbaşı kullanılmalı','','#b3452b'),
 ('  (kavurma gibi) veya ayrı uzun','','#666'),
 ('  pişirme reçetesi','','#666'),
 ('· Nemli et tamburda yapışır →','','#b3452b'),
 ('  cep sıyırıcısı + soğuk tutma','','#666'),
 ('','',''),
 ('Kaşar notu: rende yerine KÜP','','#333'),
 ('kaşar da olur (Dominos küp de','','#666'),
 ('kullanır) — tambur cebi için','','#666'),
 ('daha akıcı; pilotta denenir','','#666'),
]
yy = 166
for s_,w_,c_ in nots:
    if s_: tx(NX,yy,s_,10.5,'start',w_,c_)
    yy += 19

tx(W-24,H-14,'AUTOKITCH · ist3_topping_detay_v2',10,'end','','#999')

svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d"><rect width="%d" height="%d" fill="#ffffff"/>%s</svg>' % (W,H,W,H,W,H,''.join(E))
OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\ist3_topping_detay_v2.svg"
io.open(OUT,'w',encoding='utf-8').write(svg)
print('yazildi:', OUT)
