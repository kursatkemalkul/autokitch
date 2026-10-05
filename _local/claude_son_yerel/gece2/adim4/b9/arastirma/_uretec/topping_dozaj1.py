# -*- coding: utf-8 -*-
# TOPPING DOZAJ UNITESI v1 — Picnic Works referansi (2 kare) + bizim dilim kesiti + rotor tipleri + gram hesabi + sucuk problemi
import io, math, random
K = 4.0
def px(c): return c*K
W, H = 1470, 1150
o = []
def ln(x1,y1,x2,y2,w=1,c='#111',d=None):
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s stroke-linecap="round"/>' % (x1,y1,x2,y2,c,w,(' stroke-dasharray="%s"'%d) if d else ''))
def rc(x,y,w,h,sw=1,r=0,c='#111',d=None,f='none'):
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,w,h,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def ci(x,y,r,sw=1,c='#111',d=None,f='none'):
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def el(x,y,rx,ry,sw=1,c='#111',d=None,f='none'):
    o.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,rx,ry,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def tx(x,y,s,fs=9,anc='start',fw='',col='#111'):
    o.append('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="%s" font-weight="%s" fill="%s" font-family="Segoe UI, Arial, sans-serif">%s</text>' % (x,y,fs,anc,fw or 'normal',col,s))
def path(d,sw=1,c='#111',f='none',dash=None):
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="%s"%s stroke-linejoin="round"/>' % (d,f,c,sw,(' stroke-dasharray="%s"'%dash) if dash else ''))
def poly(pts,sw=1,c='#111',f='none',d=None):
    o.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (' '.join('%.1f,%.1f'%p for p in pts),f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def arr(x1,y1,x2,y2,c='#c0392b',w=1.2):
    ln(x1,y1,x2,y2,w,c); a=math.atan2(y2-y1,x2-x1)
    for s in (1,-1): ln(x2,y2,x2-7*math.cos(a-s*.42),y2-7*math.sin(a-s*.42),w,c)
def carc(cx,cy,r,a1,a2,c='#1a49b8',sw=1.2,head=True):
    p=lambda a:(cx+r*math.cos(math.radians(a)),cy+r*math.sin(math.radians(a)))
    x1,y1=p(a1); x2,y2=p(a2)
    path('M%.1f,%.1f A%.1f,%.1f 0 %d 1 %.1f,%.1f'%(x1,y1,r,r,1 if abs(a2-a1)>180 else 0,x2,y2),sw,c)
    if head:
        a=math.radians(a2+90)
        for s in (1,-1): ln(x2,y2,x2-7*math.cos(a-s*.42),y2-7*math.sin(a-s*.42),sw,c)

GRN, RED, BLU, GRY, AMB, PUR = '#1d7a4f', '#c0392b', '#1a49b8', '#666', '#b7791f', '#6b4fa8'
random.seed(7)

o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H))
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,42,'AUTOKITCH — TOPPING · DOZAJ ÜNİTESİ v1 (4 Eyl 2026) — Picnic Works referansı çözümlendi + revolver dilimine uygulanışı · gram hesabı · sucuk problemi',15,'start','bold')
tx(30,66,'İki hareket gerekiyor: (1) KÖPRÜ KIRICI tel — malzemenin huni duvarında kemer kurup akışı kesmesini engeller · (2) DOZAJ ROTORU — cep hacmi × devir = gram. İkisi tek milden dişli oranıyla döner, dilim PASİF kalır (motor yok, kablo yok, yıkanabilir).',9.5,'start','','#444')
ln(30,78,W-30,78,.8,'#999')

# ================= A · REFERANS =================
XA,YA = 40,110
rc(XA,YA,410,410,1.4,4,'#111',None,'#fcfbf8')
tx(XA+14,YA+22,'A · REFERANS — Picnic Works (video kareleri, çözümleme)',9.5,'start','bold')
tx(XA+14,YA+38,'firma Mayıs 2026'+chr(39)+'da tasfiye oldu; makine mantığı geçerli',7,'start','',GRY)
# A1
x1,y1 = XA+22, YA+56
tx(x1,y1-2,'kare 1 (0:07) — huni içi',7.5,'start','bold',BLU)
poly([(x1,y1+16),(x1+165,y1+16),(x1+120,y1+150),(x1+45,y1+150)],1.4,'#111','#f4f4f2')
ln(x1+45,y1+150,x1+120,y1+150,1.4,'#111')
path('M%d,%d C%d,%d %d,%d %d,%d' % (x1+38,y1+30, x1+70,y1+95, x1+108,y1+60, x1+128,y1+118),1.8,'#8a8a8a')
ci(x1+82,y1+96,5,1.2,'#8a8a8a',None,'#ddd')
carc(x1+82,y1+96,34,200,20,BLU,1.1)
tx(x1+82,y1+68,'2-5 dev/dk',6,'middle','bold',BLU)
for (dx,dy) in ((60,132),(96,140),(78,146)): ci(x1+dx,y1+dy,2.4,0,'none',None,'#c9c39a')
rc(x1+40,y1+158,86,18,1,3,PUR,None,'#efeaf8'); tx(x1+83,y1+171,'5 GRAMS',8,'middle','bold',PUR)
tx(x1,y1+196,'ince paslanmaz tel = KÖPRÜ KIRICI',7.2,'start','bold')
tx(x1,y1+208,'(karıştırıcı değil — yapışma için de değil)',6.8,'start','',GRY)
tx(x1,y1+220,'lifli malzeme hunide kemer kurar, altı boşalır',6.8,'start','','#333')
tx(x1,y1+232,'üstü asılı kalır → akış durur. Tel kemeri kırar.',6.8,'start','','#333')
tx(x1,y1+244,'"5 GRAMS" = tartı geri beslemeli dozaj',6.8,'start','',PUR)
# A2
x2,y2 = XA+218, YA+56
tx(x2,y2-2,'kare 2 (0:22) — huni ağzı',7.5,'start','bold',BLU)
path('M%d,%d L%d,%d L%d,%d L%d,%d Z' % (x2,y2+16, x2+150,y2+16, x2+150,y2+80, x2,y2+62),1.4,'#111','#f4f4f2')
path('M%d,%d A34,34 0 0 1 %d,%d'%(x2+10,y2+62,x2+128,y2+80),1.4,'#111')
ci(x2+72,y2+74,26,1.4,'#111',None,'#fff')
for k in range(6):
    a=math.radians(k*60+15); ln(x2+72,y2+74,x2+72+26*math.cos(a),y2+74+26*math.sin(a),1,'#111')
carc(x2+72,y2+74,34,150,30,BLU,1.1); tx(x2+72,y2+40,'rotor',6.5,'middle','bold',BLU)
for k in range(16):
    xx=x2+50+random.random()*46; yy=y2+104+random.random()*44
    el(xx,yy,3.2,1.8,0,'none',None,'#d9d38f')
el(x2+72,y2+168,58,15,1.4,'#111',None,'#faf7ee'); el(x2+72,y2+168,44,10,.8,'#bbb','3,2')
tx(x2+72,y2+172,'pide (döner)',6,'middle','',GRY)
tx(x2,y2+196,'huni ağzındaki dönen parça = DOZAJ ROTORU',7.2,'start','bold')
tx(x2,y2+208,'devir × cep hacmi = gram (senin dediğin vida mantığı)',6.8,'start','','#333')
tx(x2,y2+220,'peynirde helezon (auger) değil OLUKLU ROTOR —',6.8,'start','','#333')
tx(x2,y2+232,'helezon lifli peyniri sıkıştırıp topak yapar',6.8,'start','','#333')
tx(x2,y2+244,'NOT: orada da pide dönüyor, ağız sabit — bizim kural',6.8,'start','bold',GRN)

# ================= B · BİZİM DİLİM KESİTİ =================
XB,YB = 470,110
rc(XB,YB,470,410,1.4,4,'#111',None,'#fcfdff')
tx(XB+14,YB+22,'B · BİZİM DİLİM — dozaj kesiti (dilim pasif, motor tablada sabit)',9.5,'start','bold')
S=2.6
zx = lambda c: XB+40+S*c
zy = lambda c: YB+46+S*c
# dilim govdesi (28 derin x 28 yuksek), tabani egimli huni
rc(zx(0),zy(0),S*28,S*22,1.4,0,'#111',None,'#f1efe8')
poly([(zx(0),zy(22)),(zx(28),zy(22)),(zx(17),zy(33)),(zx(11),zy(33))],1.4,'#111','#f1efe8')
tx(zx(14),zy(11),'MALZEME',8,'middle','bold','#555')
tx(zx(14),zy(19),'kaşar 4,8 kg',6.5,'middle','','#555')
# kopru kirici tel
path('M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f'%(zx(5),zy(20),zx(11),zy(26),zx(19),zy(21),zx(24),zy(27)),1.8,'#8a8a8a')
ci(zx(14),zy(24),4,1.2,'#8a8a8a',None,'#ddd')
carc(zx(14),zy(24),S*7,200,20,BLU,1.1)
tx(zx(14)+S*9,zy(21),'köprü kırıcı · 3 dev/dk',6.5,'start','bold',BLU)
# rotor
ci(zx(14),zy(36),S*3.5,1.4,'#111',None,'#fff')
for k in range(6):
    a=math.radians(k*60+20); ln(zx(14),zy(36),zx(14)+S*3.5*math.cos(a),zy(36)+S*3.5*math.sin(a),1,'#111')
carc(zx(14),zy(36),S*5,150,30,BLU,1.1)
tx(zx(14)+S*7,zy(36),'oluklu rotor Ø7 · 6 cep · 60 dev/dk',6.5,'start','bold',BLU)
# dilim alt yuzu + kavrama
rc(zx(0),zy(40),S*28,S*2,1,0,'#111',None,'#ddd'); tx(zx(0)-4,zy(41.5),'dilim tabanı',6,'end','',GRY)
rc(zx(12.5),zy(42),S*3,S*3,1.1,0,BLU,None,'#dfe7fb'); tx(zx(14)+S*3,zy(44.5),'kavrama (kam)',6.3,'start','',BLU)
# tabla
rc(zx(-2),zy(45),S*32,S*2,1.2,0,'#111',None,'#bbb'); tx(zx(30),zy(46.5),'tabla 2',6,'start','',GRY)
# motor + disli
rc(zx(9),zy(50),S*10,S*9,1.2,2,'#111',None,'#eee'); tx(zx(14),zy(55),'DOZAJ MOTORU',6.2,'middle','bold'); tx(zx(14),zy(58),'24 V · 40 W · enkoder',5.8,'middle','')
ln(zx(14),zy(47),zx(14),zy(50),1.4,'#111')
rc(zx(19.5),zy(51),S*5,S*4,1,1,'#555',None,'#f2f2f2'); tx(zx(22),zy(53.7),'1:20',5.6,'middle','bold','#555')
tx(zx(26),zy(53.7),'dişli: rotor 60 → tel 3',6,'start','',GRY)
# huni + cikis
poly([(zx(9),zy(40)),(zx(19),zy(40)),(zx(15.5),zy(62)),(zx(12.5),zy(62))],1,BLU,'#eef3ff','3,2')
ln(zx(14),zy(62),zx(14),zy(70),1.6,GRN)
arr(zx(14),zy(64),zx(14),zy(72),GRN,1.4)
tx(zx(16),zy(70),'ÇIKIŞ (35, 60) — sabit',7,'start','bold',GRN)
# tarti hucresi
rc(zx(22),zy(45),S*6,S*3,1.1,1,AMB,None,'#fdf3dd'); tx(zx(25),zy(47),'yük hücresi',5.8,'middle','bold',AMB)
tx(zx(29.5),zy(47),'dilim öne gelince pime oturur',6,'start','',AMB)
# tepsi
el(zx(14),zy(78),S*17,S*2.5,1.2,BLU,None,'#dfe7fb'); tx(zx(14),zy(84),'tepsi (robot öteler, spiral)',6.5,'middle','',BLU)
ny=YB+372
for i,s in enumerate(['dilimde motor/kablo YOK — tek mil, alttan kavrama; dilim komple bulaşık makinesine girer',
                      'yük hücresi: dozaj öncesi/sonrası fark = verilen gram (kalibrasyon) + dilim boşaldı bilgisi',
                      'aynı hücre değişim tetiğini de veriyor → ayrı sensör gerekmiyor']):
    tx(XB+16,ny+i*13,s,7.2,'start','','#333')

# ================= C · ROTOR TİPLERİ =================
XC,YC = 960,110
rc(XC,YC,470,410,1.4,4,'#111',None,'#fcfbf8')
tx(XC+14,YC+22,'C · ROTOR TİPİ — hangi malzemeye hangisi',9.5,'start','bold')
def rot_helezon(cx,cy):
    rc(cx-46,cy-16,92,32,1.2,4,'#111',None,'#fff')
    for k in range(6):
        path('M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f'%(cx-40+k*16,cy-16,cx-34+k*16,cy,cx-40+k*16,cy+16),1.1,'#111')
    ln(cx-46,cy,cx+46,cy,.8,'#999','3,2')
def rot_oluk(cx,cy):
    ci(cx,cy,20,1.3,'#111',None,'#fff')
    for k in range(6):
        a=math.radians(k*60+15)
        path('M%.1f,%.1f L%.1f,%.1f'%(cx,cy,cx+20*math.cos(a),cy+20*math.sin(a)),1.1,'#111')
        a2=math.radians(k*60+45)
        el(cx+13*math.cos(a2),cy+13*math.sin(a2),4,4,0,'none',None,'#d9d38f')
    ci(cx,cy,3.5,1,'#111',None,'#ddd')
def rot_yildiz(cx,cy):
    ci(cx,cy,20,1.3,'#111',None,'#fff')
    for k in range(8):
        a=math.radians(k*45); ln(cx,cy,cx+20*math.cos(a),cy+20*math.sin(a),1.1,'#111')
    ci(cx,cy,3.5,1,'#111',None,'#ddd')
    path('M%.1f,%.1f A20,20 0 0 1 %.1f,%.1f'%(cx-20,cy,cx+20,cy),2.2,'#555')
items = [
 (rot_helezon,'HELEZON (auger)','vida — sürekli itme','sıvı/toz/granül: un, sos','kaşarı sıkıştırır, topak yapar ✗',RED),
 (rot_oluk,'OLUKLU ROTOR','6 cep — cep hacmi = doz','rendelenmiş peynir, kıyma, kavurma','SEÇİLEN — hassas, nazik ✓',GRN),
 (rot_yildiz,'YILDIZ VALF','hava sızdırmaz, basınçlı hat','pnömatik taşıma (bizde yok)','gereksiz karmaşık ~',AMB),
]
for i,(fn,ad,ne,nerede,karar,col) in enumerate(items):
    yy = YC+70+i*112
    fn(XC+70,yy)
    tx(XC+130,yy-24,ad,8.5,'start','bold',col)
    tx(XC+130,yy-8,ne,7,'start','','#333')
    tx(XC+130,yy+8,'kullanıldığı yer: '+nerede,7,'start','','#333')
    tx(XC+130,yy+24,karar,7.2,'start','bold',col)
    if i<2: ln(XC+16,yy+54,XC+454,yy+54,.6,'#ddd')
tx(XC+16,YC+396,'Cep hacmi 25 cm³ × 6 cep = 150 cm³/tur · rotor Ø7 × boy 8 cm · paslanmaz, sökülebilir',7.2,'start','bold','#333')

# ================= D · GRAM HESABI =================
XD,YD = 40,540
rc(XD,YD,620,290,1.4,4)
tx(XD+14,YD+24,'D · DOZAJ HESABI — cep hacmi 25 cm³, 6 cep/tur, rotor 60 dev/dk',9.5,'start','bold')
hdr = ['malzeme','porsiyon','yoğunluk','g / cep','cep','tur','süre']
colx = [XD+18, XD+118, XD+208, XD+300, XD+378, XD+436, XD+506]
for i,h in enumerate(hdr): tx(colx[i],YD+48,h,7.2,'start','bold',GRY)
ln(XD+14,YD+54,XD+606,YD+54,.8,'#bbb')
data = [('kaşar (rendelenmiş)',80,0.35),('sucuk (dilim)',45,0.50),('kavurma',35,0.55),('kuşbaşı',35,0.55)]
for i,(ad,g,yog) in enumerate(data):
    gc = 25*yog; cep = g/gc; tur = cep/6; sn = tur/1.0
    yy = YD+74+i*26
    vals=[ad,'%g g'%g,'%.2f g/cm³'%yog,'%.1f g'%gc,'%.1f'%cep,'%.2f'%tur,'%.1f sn'%sn]
    for j,v in enumerate(vals): tx(colx[j],yy,v,7.4,'start','bold' if j==0 else '','#111' if j==0 else '#333')
ln(XD+14,YD+182,XD+606,YD+182,.8,'#bbb')
for i,s in enumerate(['tek pide (kaşar + 1 malzeme): 1,3 + 0,6 = ~2 sn dozaj → 103 sn bütçede sorun yok ✓',
                      'hassasiyet: cep dolumu ±%8 → yük hücresi son cebi kısaltarak düzeltir → ±3 g',
                      'yoğunluklar gevşek dolgu kabulü; ilk kalibrasyon makinede tartılarak yapılır']):
    tx(XD+18,YD+202+i*15,s,7.3,'start','bold' if i==0 else '',GRN if i==0 else '#333')

# ================= E · SUCUK PROBLEMİ =================
XE,YE = 680,540
rc(XE,YE,750,290,1.4,4)
tx(XE+14,YE+24,'E · SUCUK — dilim malzeme rotorla verilemez (dürüst tespit)',9.5,'start','bold',RED)
tx(XE+14,YE+42,'Rendelenmiş/parçalı malzeme cebe dolar; sucuk DİLİMLERİ birbirine yapışır, cebe düzensiz girer, ikişer üçer düşer.',7.4,'start','','#333')
opts = [
 ('① rastgele dökme + rotor','dilimler kasete serbest dökülür','yapışma → doz tutmaz, en riskli',RED),
 ('② istif kanalı + sıyırıcı','dilimler dikey kanalda, alttan tek tek sıyrılır','3 kanal × 80 = 240 dilim (~20 pide) → çok az',AMB),
 ('③ ÇUBUK + DİLİMLEYİCİ','bütün sucuk çubuğu dik durur, dozajda bıçak keser','~23 çubuk × 25 cm = 3,9 kg / dilim ✓ taze kesim',GRN),
]
for i,(ad,ne,sonuc,col) in enumerate(opts):
    yy = YE+68+i*46
    rc(XE+16,yy-14,18,18,1.1,3,col,None,'#fff'); tx(XE+25,yy,str(i+1),8,'middle','bold',col)
    tx(XE+44,yy-2,ad,8,'start','bold',col); tx(XE+230,yy-2,ne,7.2,'start','','#333'); tx(XE+230,yy+12,sonuc,7.2,'start','bold' if i==2 else '',col)
# cubuk eskizi
xs_=XE+560
for k in range(5): rc(xs_+k*17,YE+70,13,80,1.1,2,'#111',None,'#f4ece6')
ln(xs_-6,YE+156,xs_+90,YE+156,1.6,RED); tx(xs_+42,YE+168,'bıçak (dozajda keser)',6.3,'middle','bold',RED)
tx(xs_+42,YE+62,'sucuk çubukları (dik)',6.5,'middle','',GRY)
for k in range(3): el(xs_+30+k*14,YE+178+k*4,7,3,.9,'#111',None,'#e8d5c8')
tx(XE+16,YE+228,'Öneri ③: 2 sucuk dilimi = 7,9 kg ≈ 5,5 gün (haftalık 10 kg için geçiş rafında 1 yedek yeter).',7.4,'start','bold',GRN)
tx(XE+16,YE+244,'Bedel: dilime bıçak + servo (dilim artık tam pasif değil — kavramadan tahrik, bıçak tek eksen).',7.4,'start','','#333')
tx(XE+16,YE+260,'Alternatif: sucuğu tedarikçiden dilimli değil çubuk al — hem ucuz hem raf ömrü uzun (kesilmemiş).',7.4,'start','',GRY)

# ================= KARAR =================
yk0 = 850
rc(30,yk0,W-60,H-yk0-30,1.6,4)
tx(48,yk0+24,'ÖZET — TOPPING v12'+chr(39)+'ye girecek dozaj kurgusu',12,'start','bold')
rows = [
 ('Her dilimin dibinde tek mil: altta OLUKLU ROTOR (Ø7, 6 cep × 25 cm³, 60 dev/dk), üstünde 1:20 dişliyle 3 dev/dk dönen KÖPRÜ KIRICI tel. Tahrik tabladaki tek sabit motordan kam-kavrama ile alınır → dilimde motor, kablo, elektronik yok; komple sökülüp yıkanır.', '#333'),
 ('Gram kontrolü: dozaj noktasındaki yük hücresi dilimi tartar; verilen ağırlık farktan okunur, son cep kısaltılarak ±3 g tutulur. Aynı hücre "dilim boşaldı" tetiğini de verir (ayrı sensör yok). Picnic'+chr(39)+'in "5 GRAMS" iddiası bu prensibin ta kendisi.', '#333'),
 ('Sucuk istisnası: dilim malzeme rotorla verilemez → sucuk dilimi ÇUBUK + DİLİMLEYİCİ olarak kurgulanır (2 dilim = 7,9 kg ≈ 5,5 gün, taze kesim). Kaşar / kavurma / kuşbaşı oluklu rotor ✓.', GRN),
 ('Açık kalanlar: rotor cep geometrisi (peynir yapışması) prototipte denenmeli · bıçak servosunun kavramaya bağlanması · rendelenmiş kaşar yerine BLOK + RENDE seçeneği hâlâ masada (köprüleme tamamen biter, ama dilime rende motoru girer).', GRY),
]
for i,(s,c) in enumerate(rows):
    tx(48,yk0+46+i*44,s[:180],8.5,'start','bold' if i==2 else '',c)
    if len(s)>180: tx(48,yk0+46+i*44+13,s[180:],8.5,'start','',c)
tx(W-40,H-36,'AUTOKITCH · arastirma/3_TOPPING/topping_dozaj_unitesi_v1 · 4 Eyl 2026',7,'end','',GRY)
o.append('</svg>')
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\topping_dozaj_unitesi_v1.svg"
io.open(out,'w',encoding='utf-8').write(chr(10).join(o))
print('yazildi', out)
