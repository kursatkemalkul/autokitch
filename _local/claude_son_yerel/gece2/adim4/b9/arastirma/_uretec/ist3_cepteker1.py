# -*- coding: utf-8 -*-
# IST.3 TOPPING — CEP TEKERI DOZAJ UNITESI v1: tek unite kesiti + 4'lu dizilim + motor karari
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
def tx(x,y,s,fs=11,a='middle',w='',col='#111'):
    fw = ' font-weight="%s"' % w if w else ''
    E.append('<text x="%.1f" y="%.1f" text-anchor="%s" font-size="%s" fill="%s" font-family="Arial"%s>%s</text>' % (x,y,a,fs,col,fw,s))
def not_(x,y,s,a='middle'): tx(x,y,s,10,a,'','#555')
def arr(x1,y1,x2,y2,w=1.8,c='#1d7a4f'):
    ln(x1,y1,x2,y2,w,c)
    a = math.atan2(y2-y1,x2-x1)
    for da in (2.6,-2.6):
        ln(x2,y2,x2-9*math.cos(a+da),y2-9*math.sin(a+da),w,c)
def oy(x1,x2,y,cm):
    ln(x1,y,x2,y,1,'#b3452b'); ln(x1,y-5,x1,y+5,1,'#b3452b'); ln(x2,y-5,x2,y+5,1,'#b3452b')
    tx((x1+x2)/2,y-6,cm,11,'middle','bold','#b3452b')
def ox(x,y1,y2,cm):
    ln(x,y1,x,y2,1,'#b3452b'); ln(x-5,y1,x+5,y1,1,'#b3452b'); ln(x-5,y2,x+5,y2,1,'#b3452b')
    E.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="11" font-weight="bold" fill="#b3452b" font-family="Arial" transform="rotate(-90 %.1f %.1f)">%s</text>' % (x-9,(y1+y2)/2,x-9,(y1+y2)/2,cm))

W, H = 1560, 1000
tx(40,44,'TOPPING — CEP TEKERİ DOZAJ ÜNİTESİ v1 (Rosseto çarkı + motor = bizim ünitemiz)',17,'start','bold')
tx(40,68,'Soru: 4 hazne tek motordan mı, ayrı mı? — CEVAP: HER HAZNEYE AYRI KÜÇÜK MOTOR (×4). Sebepleri sağda.',11,'start','','#555')

# ================= PANEL 1: TEK UNITE KESITI (buyuk, sematik ~ 3 px/mm) =================
S = 1.55
def px(mm): return mm*S
X1, Y1 = 150, 170
tx(X1+px(120),Y1-52,'TEK ÜNİTE — YAN KESİT · hazne ≈ 17 × 20 × 22 cm, 2-4 kg',12.5,'middle','bold')
# hazne: 170 en x 250 yuksek (kesitte derinlik gorunuyor: 200)
hx, hy, hw, hh = X1+px(30), Y1+px(10), px(200), px(170)
rc(hx,hy,hw,hh,1.8,3)
# dolum kapagi ustte
rc(hx+px(30),hy-px(12),hw-px(60),px(12),1.4,2)
not_(hx+hw/2,hy-px(20),'DOLUM KAPAĞI (üstten) — eleman doldurur, +3 °C bölgesi')
# kupler
for i in range(6):
    for j in range(4):
        rc(hx+px(15)+i*px(30),hy+px(15)+j*px(32),px(20),px(20),.8,1,'#8a6a3a')
# koni
ln(hx,hy+hh,hx+px(70),hy+hh+px(45),1.8); ln(hx+hw,hy+hh,hx+hw-px(70),hy+hh+px(45),1.8)
# kopru kirici kanat (mil uzantisi hazne icinde)
kx = hx+hw/2
ln(kx,hy+hh+px(45),kx,hy+px(40),1.6,'#1a49b8')
ln(kx-px(45),hy+px(60),kx+px(45),hy+px(60),2.2,'#1a49b8'); ln(kx-px(30),hy+px(110),kx+px(30),hy+px(110),2.2,'#1a49b8')
tx(kx+px(52),hy+px(64),'köprü kırıcı kanat',9.5,'start','bold','#1a49b8')
tx(kx+px(52),hy+px(64)+13,'(aynı mille döner — topaklanmayı bozar)',8.5,'start','','#1a49b8')
# ROTOR govdesi
ry_ = hy+hh+px(45)+px(55)
rc(hx+px(45),hy+hh+px(45),px(110),px(110),1.8,4)
ci(kx,ry_,px(48),2)
for k in range(6):
    a = k*math.pi/3 + math.pi/6
    ln(kx,ry_,kx+px(48)*math.cos(a),ry_+px(48)*math.sin(a),1.4)
ci(kx,ry_,px(8),1.4,fill='#fff')
# cep icinde kupler (ust cep dolu)
for dx,dy in ((-8,-30),(8,-30),(0,-18)):
    rc(kx+px(dx)-px(5),ry_+px(dy)-px(5),px(10),px(10),.8,1,'#8a6a3a')
tx(kx-px(60),ry_+px(4),'ROTOR Ø10',9.5,'end','bold')
tx(kx-px(60),ry_+px(4)+13,'6 GENİŞ CEP',9,'end','','#555')
tx(kx-px(60),ry_+px(4)+26,'cep ≈ 25-30 cm³ (~20 g)',8.5,'end','','#555')
tx(kx-px(60),ry_+px(4)+39,'düşme boşluklu (ezmez)',8.5,'end','','#555')
# cikis
ln(kx-px(25),hy+hh+px(155),kx-px(25),hy+hh+px(195),1.6); ln(kx+px(25),hy+hh+px(155),kx+px(25),hy+hh+px(195),1.6)
for dy in (205,225,245):
    rc(kx-px(4),hy+hh+px(dy),px(8),px(8),.8,1,'#8a6a3a')
not_(kx,hy+hh+px(270),'çıkış → nozül → tabla')
not_(kx,hy+hh+px(286),'1 cep = 60° = bir tutam · porsiyon = cep sayısı')
# motor (sagda, kaplin)
mx = hx+px(45)+px(110)+px(20)
rc(mx,ry_-px(30),px(55),px(60),1.8,3)
tx(mx+px(27),ry_+px(4),'M',13,'middle','bold')
ln(hx+px(45)+px(110),ry_,mx,ry_,2.2)
rc(hx+px(45)+px(110)+px(4),ry_-px(7),px(12),px(14),1.2,1)
tx(mx+px(62),ry_-px(14),'STEP MOTOR (NEMA 17 sınıfı)',9.5,'start','bold')
tx(mx+px(62),ry_-px(14)+13,'+ kaplin — tur/adım kontrollü',8.5,'start','','#555')
tx(mx+px(62),ry_-px(14)+26,'her ünitenin KENDİ motoru',8.5,'start','','#555')
# sokme oku
arr(hx+px(20),ry_+px(70),hx-px(30),ry_+px(70),1.8,'#b3452b')
tx(hx-px(35),ry_+px(74),'rotor öne çekilir',9,'end','','#b3452b')
tx(hx-px(35),ry_+px(74)+12,'(tek vida) → bulaşık mak.',8.5,'end','','#b3452b')
# olculer
ox(hx-px(22),hy,hy+hh+px(45),'~22')

# ================= PANEL 2: 4'LU DIZILIM (on gorunus, kabin 70) =================
S2 = 0.55
def p2(mm): return mm*S2
X2, Y2 = 880, 130
tx(X2+p2(350),Y2-14,'4 ÜNİTE YAN YANA — ÖN GÖRÜNÜŞ (kabin 70)',12.5,'middle','bold')
rc(X2,Y2,p2(700),p2(720),2,4)
adlar = ['KÜP SUCUK','KAŞAR','KAVURMA','KUŞBAŞI']
for i,ad in enumerate(adlar):
    ux = X2+p2(20)+i*p2(167)
    rc(ux,Y2+p2(40),p2(150),p2(300),1.5,3)               # hazne
    ln(ux,Y2+p2(340),ux+p2(55),Y2+p2(400),1.4); ln(ux+p2(150),Y2+p2(340),ux+p2(95),Y2+p2(400),1.4)
    ci(ux+p2(75),Y2+p2(450),p2(40),1.6)                  # rotor
    for k in range(6):
        a = k*math.pi/3
        ln(ux+p2(75),Y2+p2(450),ux+p2(75)+p2(40)*math.cos(a),Y2+p2(450)+p2(40)*math.sin(a),1)
    rc(ux+p2(45),Y2+p2(510),p2(60),p2(45),1.4,2)         # motor
    tx(ux+p2(75),Y2+p2(540),'M%d' % (i+1),10,'middle','bold')
    tx(ux+p2(75),Y2+p2(200),ad,9.5,'middle','bold')
    tx(ux+p2(75),Y2+p2(230),'2-4 kg',8.5)
    ln(ux+p2(75),Y2+p2(490),ux+p2(75),Y2+p2(600),1,'#777','3,3')   # cikis borusu
    # cikislar merkeze
    ln(ux+p2(75),Y2+p2(600),X2+p2(350),Y2+p2(660),1,'#777','3,3')
ci(X2+p2(350),Y2+p2(670),p2(14),1.4,'#b3452b')
tx(X2+p2(350),Y2+p2(700),'nozül bölgesi → döner-kayar tabla',9.5,'middle','','#b3452b')
oy(X2,X2+p2(700),Y2-2+p2(24),'')
for i in range(4):
    oy(X2+p2(20)+i*p2(167),X2+p2(20)+i*p2(167)+p2(150),Y2+p2(30),'17')
# PLC hat
rc(X2+p2(230),Y2+p2(600)+p2(120),p2(240),p2(60),1.4,3)
tx(X2+p2(350),Y2+p2(600)+p2(158),'PLC → 4 step sürücü',10,'middle','bold')
for i in range(4):
    ln(X2+p2(20)+i*p2(167)+p2(75),Y2+p2(555),X2+p2(20)+i*p2(167)+p2(75),Y2+p2(575),1,'#1a49b8')
    ln(X2+p2(20)+i*p2(167)+p2(75),Y2+p2(575),X2+p2(350),Y2+p2(720),1,'#1a49b8','2,2')

# ================= PANEL 3: KARAR NOTLARI =================
NX = 880; NY = 580
tx(NX,NY,'NEDEN AYRI MOTOR (×4):',12.5,'start','bold')
nots = [
 ('· Her malzemenin porsiyonu farklı → farklı tur sayısı','#333'),
 ('  (kaşar 4 cep · sucuk 3 · kavurma 3 · kuşbaşı 3-4)','#666'),
 ('· Sıra sıra çalışırlar; karışık pidede 4\'ü peş peşe','#333'),
 ('· Tek motor = kavrama/vites/mil = mekanik karmaşa,','#333'),
 ('  arıza noktası, temizlikte sökülmesi zor','#666'),
 ('· Küçük step motor ucuz; biri bozulsa 3\'ü çalışır','#333'),
 ('· Her ünite BAĞIMSIZ sökülür (kendi motoru kaplinden ayrılır)','#333'),
 ('','#333'),
 ('KENDİMİZ YAPABİLİR MİYİZ? — EVET, PİLOT YOLU:','#1d7a4f'),
 ('· Rosseto porsiyon çarkı al (bulaşık mak. uyumlu, 5-42 g cep)','#1d7a4f'),
 ('· Kolunu sök, step motor + kaplin tak, PLC/Arduino ile döndür','#1d7a4f'),
 ('· Soğuk küp sucuk / kaşar / kavurma ile AKIŞ TESTİ yap','#1d7a4f'),
 ('· Çalışırsa aynı geometriyi paslanmaz büyütülmüş hâlde','#1d7a4f'),
 ('  Denge Proses / TMD\'ye yaptır (gövde + özel rotor)','#666'),
]
yy = NY+22
for s_,c_ in nots:
    if s_: tx(NX,yy,s_,10.5,'start','bold' if c_=='#1d7a4f' and s_.startswith('KEND') else '',c_)
    yy += 19

tx(W-24,H-14,'AUTOKITCH · ist3_cep_tekeri_v1',10,'end','','#999')
svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d"><rect width="%d" height="%d" fill="#ffffff"/>%s</svg>' % (W,H,W,H,W,H,''.join(E))
OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\ist3_cep_tekeri_v1.svg"
io.open(OUT,'w',encoding='utf-8').write(svg)
print('yazildi:', OUT)
