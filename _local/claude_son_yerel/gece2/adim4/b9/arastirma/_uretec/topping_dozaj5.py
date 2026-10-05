# -*- coding: utf-8 -*-
# TOPPING DOZAJ v5 — Kemal: "huniyi kaldir, rotoru boru gibi dik yap" → A cepli rotor+huni · B dik boru (neden olmaz) · C yatay HELEZON tek nokta bosaltma (huni yok) — KARAR C
import io, math
W, H = 1460, 1060
o = []
def ln(x1,y1,x2,y2,w=1,c='#111',d=None):
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s stroke-linecap="round"/>' % (x1,y1,x2,y2,c,w,(' stroke-dasharray="%s"'%d) if d else ''))
def rc(x,y,w,h,sw=1,r=0,c='#111',d=None,f='none'):
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,w,h,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def ci(x,y,r,sw=1,c='#111',d=None,f='none'):
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def tx(x,y,s,fs=9,anc='start',fw='',col='#111'):
    o.append('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="%s" font-weight="%s" fill="%s" font-family="Segoe UI, Arial, sans-serif">%s</text>' % (x,y,fs,anc,fw or 'normal',col,s))
def path(d,sw=1,c='#111',f='none',dash=None):
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="%s"%s stroke-linejoin="round"/>' % (d,f,c,sw,(' stroke-dasharray="%s"'%dash) if dash else ''))
def poly(pts,sw=1,c='#111',f='none',d=None):
    o.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (' '.join('%.1f,%.1f'%p for p in pts),f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def arr(x1,y1,x2,y2,c='#c0392b',w=1.2):
    ln(x1,y1,x2,y2,w,c); a=math.atan2(y2-y1,x2-x1)
    for s in (1,-1): ln(x2,y2,x2-6*math.cos(a-s*.42),y2-6*math.sin(a-s*.42),w,c)
def hatch(pts_x0,pts_x1,y0,y1,step=7,c='#d9c9b9'):
    y=y0
    while y<y1:
        ln(pts_x0,y,pts_x1,y,.6,c); y+=step

GRN, RED, BLU, GRY, AMB = '#1d7a4f', '#c0392b', '#1a49b8', '#666', '#b7791f'
FILL, MAT, DEAD = '#f1efe8', '#e9dfa8', '#f3d9d9'
K = 5.2

o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H))
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,42,'AUTOKITCH — TOPPING · DOZAJ v5 (4 Eyl 2026) — "huniyi kaldır, rotoru boru gibi dik yap" · üç seçenek, radyal kesit (iç uç → dış duvar) · ölçüler cm',15,'start','bold')
tx(30,66,'Soru doğru yerden: yatay cepli rotor 16 cm hat boyunca döker, o yüzden altına toplayıcı huni gerekiyor. Cevap: rotoru dik yapmak değil, cepli rotoru HELEZON yapmak — helezon malzemeyi kendi ekseninde taşıyıp TEK noktadan boşaltır, huni gerekmez.',9.5,'start','','#444')
ln(30,78,W-30,78,.8,'#999')

def govde(RX,RZ,dead_tip=True):
    # dilim govdesi radyal kesit: r 5..33, h 28; rotor bolgesi r13-29 z0-7
    poly([(RX(5),RZ(28)),(RX(33),RZ(28)),(RX(33),RZ(11)),(RX(29),RZ(7)),(RX(29),RZ(0)),(RX(13),RZ(0)),(RX(13),RZ(7)),(RX(5),RZ(15))],1.4,'#111',FILL)
    poly([(RX(5.3),RZ(24)),(RX(32.7),RZ(24)),(RX(32.7),RZ(11)),(RX(29),RZ(7.3)),(RX(13),RZ(7.3)),(RX(5.3),RZ(15))],0,'none',MAT)
def tarak(RX,RZ):
    ln(RX(11),RZ(13),RX(31),RZ(13),1.8,BLU)
    for k in range(8):
        r_=12.5+k*2.4; s=1 if k%2==0 else -1; ln(RX(r_),RZ(13),RX(r_),RZ(13+s*5),1.1,BLU)
    rc(RX(11),RZ(18.5),K*20,K*11,.8,3,BLU,'4,3')
def taban_tabla(RX,RZ,open0,open1):
    rc(RX(4),RZ(0),K*30,K*1,1,0,'#111',None,'#ddd'); rc(RX(open0),RZ(0),K*(open1-open0),K*1,0,0,'none',None,'#fff')
    rc(RX(3),RZ(-2),K*32,K*2,1.2,0,'#111',None,'#bbb')
def tepsi(RX,RZ,rc_,z):
    path('M%.1f,%.1f L%.1f,%.1f'%(RX(rc_-17),RZ(z),RX(rc_+17),RZ(z)),2.2,BLU)
    rc(RX(rc_+17),RZ(z)-K*1.2,K*6,K*2.4,.9,1,BLU,None,'#dfe7fb')

# ================= A · CEPLİ ROTOR + HUNİ (v4) =================
XA,YA = 40,100
rc(XA,YA,450,560,1.4,4,'#111',None,'#fcfdff')
tx(XA+14,YA+22,'A · CEPLİ ROTOR + toplayıcı huni (v4 — mevcut)',10,'start','bold')
ax_,az_ = XA+40, YA+250
RX=lambda r: ax_+K*(r-5); RZ=lambda c: az_-K*c
govde(RX,RZ)
rc(RX(13),RZ(7),K*16,K*7,1.3,3,'#111',None,'#fff')
for k in range(1,8): ln(RX(13+k*2),RZ(7),RX(13+k*2),RZ(0),.7,'#999')
tx(RX(21),RZ(3.2),'cepli rotor 16',6.3,'middle','bold')
tarak(RX,RZ)
taban_tabla(RX,RZ,13,29)
# 16 cm boyunca dusme oklari
for r_ in (14.5,17.5,20.5,23.5,26.5): arr(RX(r_),RZ(-3),RX(r_),RZ(-6),AMB,.9)
poly([(RX(12),RZ(-4)),(RX(30),RZ(-4)),(RX(21.5),RZ(-19)),(RX(18.5),RZ(-19))],1.1,GRN,'#eaf6ee','3,2')
tx(RX(21),RZ(-11),'SABİT HUNİ 15',6.5,'middle','bold',GRN); tx(RX(21),RZ(-14),'(çark katında)',5.6,'middle','',GRN)
arr(RX(20),RZ(-19),RX(20),RZ(-25),GRN,1.4); tx(RX(22),RZ(-23),'çıkış r 20',6.5,'start','bold',GRN)
tepsi(RX,RZ,20,-30)
ln(RX(13),RZ(-2.5)-2,RX(29),RZ(-2.5)-2,.8,AMB); tx(RX(21),RZ(-2.5)+8,'16 cm hat boyunca döker',6.3,'middle','bold',AMB)
tx(RX(34),RZ(3),'rotor Ø7',6.3,'start','',GRY); tx(RX(34),RZ(13),'tarak',6.3,'start','',BLU)
ny=YA+368
for i,s in enumerate(['+ canlı taban, en nazik, en hassas doz (cep = sabit hacim)',
                      '+ 1,3 sn'+chr(39)+'de 80 g (hızlı)',
                      '− 16 cm hat boyunca döker → altına SABİT huni şart (15 cm)',
                      '− huni tabladan ayrı, döner parçanın altında → temizlik zor,',
                      '   peynir artığı birikir (hijyen) · çark katı 21 cm yer yer',
                      '− dozaj 1,3 sn ama spiral 14 sn: hızın anlamı yok']):
    tx(XA+16,ny+i*14,s,7.2,'start','bold' if s.startswith('−') else '',RED if s.startswith('−') else ('#333' if s.startswith('+') else '#333'))
rc(XA+16,YA+470,418,70,1,3,AMB,None,'#fff8ea'); tx(XA+26,YA+490,'SONUÇ ~ çalışır, ama hunisi var',8,'start','bold',AMB)
tx(XA+26,YA+506,'Kemal'+chr(39)+'in itirazı yerinde: döner tablanın altında sabit, yıkanmayan bir huni',7,'start','','#333')
tx(XA+26,YA+520,'gıda hattında zayıf nokta. Rotorun kendisi iyi, boşaltma şekli kötü.',7,'start','','#333')

# ================= B · DİK BORU (Kemal) =================
XB,YB = 505,100
rc(XB,YB,450,560,1.4,4,'#111',None,'#fffbfb')
tx(XB+14,YB+22,'B · DİK BORU rotor / helezon (senin fikrin)',10,'start','bold')
bx_,bz_ = XB+40, YB+250
RX=lambda r: bx_+K*(r-5); RZ=lambda c: bz_-K*c
# govde: piramit/koni tabana inmek zorunda → 60° duvarlar, nokta cikis r 20
poly([(RX(5),RZ(28)),(RX(33),RZ(28)),(RX(33),RZ(21)),(RX(23.5),RZ(4)),(RX(23.5),RZ(0)),(RX(16.5),RZ(0)),(RX(16.5),RZ(4)),(RX(5),RZ(21))],1.4,'#111',FILL)
poly([(RX(5.3),RZ(24)),(RX(32.7),RZ(24)),(RX(32.7),RZ(21)),(RX(23.5),RZ(4.3)),(RX(16.5),RZ(4.3)),(RX(5.3),RZ(21))],0,'none',MAT)
# olu hacim: v4 govdesine gore kaybedilen bolge (isaretle)
poly([(RX(5),RZ(21)),(RX(16.5),RZ(4)),(RX(13),RZ(0)),(RX(13),RZ(7)),(RX(5),RZ(15))],.8,RED,DEAD,'3,2')
poly([(RX(33),RZ(21)),(RX(23.5),RZ(4)),(RX(29),RZ(0)),(RX(29),RZ(7)),(RX(33),RZ(11))],.8,RED,DEAD,'3,2')
tx(RX(9),RZ(10),'kayıp',5.8,'middle','bold',RED); tx(RX(30),RZ(10),'kayıp',5.8,'middle','bold',RED)
# dik boru + helezon
rc(RX(16.5),RZ(4),K*7,K*(4+22),1.3,0,'#111',None,'#fff')
for k in range(9):
    z_=-20+k*2.8; path('M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f'%(RX(16.8),RZ(z_),RX(20),RZ(z_+1.8),RX(23.2),RZ(z_)),1,'#111')
ln(RX(20),RZ(4),RX(20),RZ(-22),.8,'#555','3,2')
tx(RX(24.5),RZ(-8),'dik helezon Ø7',6.3,'start','bold'); tx(RX(24.5),RZ(-11),'boru 26 uzun',6,'start','','#333')
# kemer (kopru) — nokta cikis ustunde
path('M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f'%(RX(14),RZ(9),RX(20),RZ(3),RX(26),RZ(9)),2,RED,'none','5,3')
tx(RX(20),RZ(11.5),'KEMER (köprü) burada kurulur',6,'middle','bold',RED)
tarak(RX,RZ)
rc(RX(4),RZ(0),K*30,K*1,1,0,'#111',None,'#ddd'); rc(RX(16.5),RZ(0),K*7,K*1,0,0,'none',None,'#fff')
rc(RX(3),RZ(-2),K*32,K*2,1.2,0,'#111',None,'#bbb'); rc(RX(16.5),RZ(-2),K*7,K*2,0,0,'none',None,'#fff')
arr(RX(20),RZ(-22),RX(20),RZ(-26),GRN,1.4); tx(RX(22),RZ(-25),'çıkış r 20',6.5,'start','bold',GRN)
tepsi(RX,RZ,20,-30)
tx(RX(6),RZ(25.5),'60°',6,'start','bold',RED); tx(RX(30),RZ(25.5),'60°',6,'start','bold',RED)
ny=YB+368
for i,s in enumerate(['+ huni yok, tek nokta, boru dilimin içinde (yıkanır)',
                      '− giriş NOKTA çıkış olur → huni koni/piramit olmak zorunda:',
                      '   kaşar için 60°+ duvar → hacim 11,7 → ~6,5 L (−%45)',
                      '− nokta çıkış = köprülemenin tam adresi; tarak kemerin',
                      '   üstünde kalır, boru ağzını göremez',
                      '− dik helezon lifli peyniri boru içinde sıkıştırır, tıkar',
                      '− boru 26 cm aşağı sarkar → çark katı 21 yetmez']):
    tx(XB+16,ny+i*14,s,7.2,'start','bold' if s.startswith('−') else '',RED if s.startswith('−') else '#333')
rc(XB+16,YB+470,418,70,1,3,RED,None,'#fdeeee'); tx(XB+26,YB+490,'SONUÇ ✗ — kaşar / kavurma için olmaz',8,'start','bold',RED)
tx(XB+26,YB+506,'Dik boru ancak serbest akan tanede (mısır, zeytin) çalışır. Bizim ana',7,'start','','#333')
tx(XB+26,YB+520,'malzeme lifli peynir: nokta çıkışa indirdiğin an akış durur.',7,'start','','#333')

# ================= C · YATAY HELEZON, DIŞ UÇTAN TEK NOKTA =================
XC,YC = 970,100
rc(XC,YC,460,560,1.4,4,'#111',None,'#f6fcf8')
tx(XC+14,YC+22,'C · YATAY HELEZON — dış uçtan tek nokta, HUNİ YOK',10,'start','bold',GRN)
cx_,cz_ = XC+40, YC+250
RX=lambda r: cx_+K*(r-5); RZ=lambda c: cz_-K*c
govde(RX,RZ)
# helezon r 12-30, U-tekne, degisken hatve 2→4
rc(RX(12),RZ(7),K*18,K*7,1.3,3,'#111',None,'#fff')
ln(RX(11.5),RZ(3.5),RX(30.5),RZ(3.5),1.4,'#333')
pitches=[2,2.2,2.5,2.8,3.1,3.4,3.7,4]
r_=12.6
for pch in pitches:
    path('M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f'%(RX(r_),RZ(6.7),RX(r_+pch/2),RZ(3.5),RX(r_),RZ(0.3)),1,'#111')
    ln(RX(r_+pch/2),RZ(6.7),RX(r_+pch/2),RZ(0.3),.5,'#999'); r_+=pch
tx(RX(21),RZ(9.6),'helezon Ø7 · hatve 2 → 4 (değişken)',6.3,'middle','bold')
arr(RX(14),RZ(-0.9)-6,RX(27),RZ(-0.9)-6,GRN,1.1); tx(RX(20.5),RZ(-0.9)-9,'malzeme dış uca taşınır',6,'middle','bold',GRN)
tarak(RX,RZ)
# tahrik ic ucta
rc(RX(10),RZ(2.3),K*2,K*2.4,1.1,1,BLU,None,'#dfe7fb'); arr(RX(11),RZ(-7),RX(11),RZ(-2.5),BLU,1.2); tx(RX(11),RZ(-8.5),'tahrik (iç uç)',6,'middle','bold',BLU)
ci(RX(11.5),RZ(13),K*2.2,1,'#555',None,'#eee'); ln(RX(11.5),RZ(4.7),RX(11.5),RZ(13),1,'#555'); tx(RX(10.4),RZ(9),'1:20',5.4,'end','bold','#555')
# bosaltma deligi dis ucta r 28-30
rc(RX(4),RZ(0),K*30,K*1,1,0,'#111',None,'#ddd'); rc(RX(27.5),RZ(0),K*2.5,K*1,0,0,'none',None,'#fff')
rc(RX(3),RZ(-2),K*32,K*2,1.2,0,'#111',None,'#bbb'); rc(RX(27),RZ(-2),K*3.5,K*2,0,0,'none',None,'#fff')
poly([(RX(27.2),RZ(-2)),(RX(30.3),RZ(-2)),(RX(30.3),RZ(-6)),(RX(27.2),RZ(-6))],1,GRN,'#eaf6ee')
tx(RX(31.5),RZ(-4.5),'ağız 4 (dilimde, yıkanır)',6.2,'start','',GRN)
arr(RX(28.8),RZ(-6),RX(28.8),RZ(-12),GRN,1.4); tx(RX(28.8),RZ(-14.5),'çıkış r 29 → (35, 69)',6.5,'middle','bold',GRN)
tepsi(RX,RZ,29,-18)
tx(RX(29),RZ(-22),'tepsi 12 altta — çark katı 21 → 8',6,'middle','',BLU)
ny=YC+368
for i,s in enumerate(['+ huni YOK: helezon 18 cm yuvadan toplar, dış uçtaki 4 cm ağızdan döker',
                      '+ canlı taban ve V-oluk aynen kalır (köprüleme yok, hacim ~10 L)',
                      '+ ıslak parçaların hepsi dilimin içinde → dilim komple yıkanır',
                      '+ çark katı 21 → 8: dilim tepsiye yaklaşır, serpinti azalır, +13 cm raf',
                      '+ 30 dev/dk · ~20 g/tur → 80 g = 4 tur = 8 sn = spiral süresine yayılır',
                      '− helezon lifli peyniri sıkıştırabilir → geniş boşluk, yavaş devir,',
                      '   değişken hatve (yuva boyunca eşit çeker) · doz ±%10 → tartı düzeltir']):
    tx(XC+16,ny+i*14,s,7.2,'start','bold' if s.startswith('−') else '',RED if s.startswith('−') else '#333')
rc(XC+16,YC+470,428,70,1,3,GRN,None,'#eaf6ee'); tx(XC+26,YC+490,'SONUÇ ✓ KARAR — senin hedefin (huni yok) doğru araçla',8,'start','bold',GRN)
tx(XC+26,YC+506,'Dik değil yatay helezon: nokta çıkışı hunide değil helezonun ucunda yaratır;',7,'start','','#333')
tx(XC+26,YC+520,'huni zaten hunisiz akan V-oluk olarak kalır. Sucuk dilimi ayrı (çubuk + bıçak).',7,'start','','#333')

# ================= ALT · DOLAP ETKİSİ + KARAR =================
YK=685
rc(40,YK,1390,345,1.6,4)
tx(56,YK+24,'DOLABA ETKİSİ ve KARAR',12,'start','bold')
# dikey bant karsilastirma (A vs C)
def dikey(x,y,items,ad):
    tx(x,y-8,ad,7.5,'start','bold',GRY)
    zz=y
    for (h,lab,col) in items:
        rc(x,zz,150,h*1.15,1,0,'#111',None,col); tx(x+75,zz+h*1.15/2+3,'%s %g'%(lab,h),6.5,'middle','bold' if 'çark' in lab or 'raf' in lab else '')
        zz+=h*1.15
    tx(x+75,zz+12,'Σ %g' % sum(i[0] for i in items),7,'middle','bold')
dikey(60,YK+56,[(27,'teknik','#f3f3f3'),(3,'panel','#ddd'),(33,'kaset katı','#f1efe8'),(21,'çark katı','#fdf3dd'),(14,'boşluk','#eef3ff'),(99,'geçiş rafı 3×33','#f7f6f2')],'A — çark katı 21')
dikey(240,YK+56,[(27,'teknik','#f3f3f3'),(3,'panel','#ddd'),(33,'kaset katı','#f1efe8'),(8,'çark katı','#eaf6ee'),(14,'boşluk','#eef3ff'),(112,'geçiş rafı 3×37','#f7f6f2')],'C — çark katı 8')
tx(420,YK+70,'C ile geçiş rafı katları 33 → 37: dilim 28 + 9 boşluk, robot pençesi daha rahat girer.',7.4,'start','','#333')
tx(420,YK+86,'Alternatif: dilim yüksekliğini 28 → 32 yap (hacim +%14, kaşar 4,6 kg → haftalık 11 dilim) — STORE −18 çekmecesi 33 olmalı.',7.4,'start','',GRY)
rows=[
 ('Rotor neden yatay, geniş uca doğru? Çünkü çıkışın NOKTA değil HAT olması köprülemeyi bitiren şeyin ta kendisi (düzlem akış). Hattı bir noktaya indirmenin iki yolu var: altına huni (A) ya da helezonla taşıyıp uçtan dökmek (C). Dik boru (B) hattı baştan noktaya çevirir, o yüzden olmaz.','#333'),
 ('KARAR C: helezon Ø7, r 12-30, değişken hatve 2→4, 30 dev/dk, tahrik iç uçtan (konik + kavrama), 1:20 ile tarak; dış uçta 4 cm ağız → dozaj noktası (35, 69) — bant ✓, arka ≥ 31 ✓, ön açık ✓. Huni ve sabit çark yok; çark katı 8 cm (tabla motoru + kavrama).',GRN),
 ('Doz: ~20 g/tur (kaşar), 80 g = 4 tur = 8 sn; spiral zaten 14 sn → helezon spiral boyunca sürekli döker, dağılım daha düzgün. Yük hücresi turu keser (±3 g). Prototipte: hatve/boşluk kaşarla denenir; sıkıştırırsa şerit (ribbon) helezon.',BLU),
 ('Sucuk dilimi bu kurgunun dışında (çubuk + bıçak, v1-E). Kavurma / kuşbaşı aynı helezon ✓. TOPPING v12'+chr(39)+'ye bu dilim ve 8 cm çark katı girer; HAT v45'+chr(39)+'te dikey bütçe güncellenir.',GRY),
]
for i,(s,c) in enumerate(rows):
    tx(420,YK+118+i*50,s[:150],8,'start','bold' if i==1 else '',c)
    if len(s)>150: tx(420,YK+118+i*50+13,s[150:300],8,'start','',c)
    if len(s)>300: tx(420,YK+118+i*50+26,s[300:],8,'start','',c)
tx(W-40,H-14,'AUTOKITCH · arastirma/3_TOPPING/topping_dozaj_unitesi_v5 · 4 Eyl 2026',7,'end','',GRY)
o.append('</svg>')
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\topping_dozaj_unitesi_v5.svg"
io.open(out,'w',encoding='utf-8').write(chr(10).join(o))
print('yazildi', out)
