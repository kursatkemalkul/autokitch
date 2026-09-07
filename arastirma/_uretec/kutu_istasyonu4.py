# -*- coding: utf-8 -*-
# PACK v4 (6 Eyl 2026) — Kemal: kutular ÜSTTE dizili (3 gün garanti, 7 gün gönül), altta katlama; kutu üstten katlama yerine insin, katlansın,
# düz zemine yükselsin, pide konsun, kapak kapansın, robot alsın. "Üstten aşağıya nasıl taşıyacak, nasıl ittirecek?" → alttan vakum plunger + kalıp.
import io, math, xml.dom.minidom
W, H = 1460, 945
o = []
AP = chr(39)
def esc(s): return str(s).replace('&','&amp;').replace('<','&lt;')
def ln(x1,y1,x2,y2,w=1,c='#111',d=None):
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s stroke-linecap="round"/>' % (x1,y1,x2,y2,c,w,(' stroke-dasharray="%s"'%d) if d else ''))
def rc(x,y,w,h,sw=1,r=0,c='#111',d=None,f='none'):
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,w,h,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def ci(x,y,r,sw=1,c='#111',d=None,f='none'):
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def el(cx,cy,rx,ry,sw=1,c='#111',d=None,f='none',rot=0):
    o.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s transform="rotate(%s %.1f %.1f)"/>' % (cx,cy,rx,ry,f,c,sw,(' stroke-dasharray="%s"'%d) if d else '',rot,cx,cy))
def tx(x,y,s,fs=9,anc='start',fw='',col='#111'):
    o.append('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="%s" font-weight="%s" fill="%s" font-family="Segoe UI, Arial, sans-serif">%s</text>' % (x,y,fs,anc,fw or 'normal',col,esc(s)))
def txr(x,y,s,fs=5,col='#555',fw=''):
    o.append('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="middle" font-weight="%s" fill="%s" font-family="Segoe UI, Arial, sans-serif" transform="rotate(-90 %.1f %.1f)">%s</text>' % (x,y,fs,fw or 'normal',col,x,y,esc(s)))
def poly(pts,sw=1,c='#111',f='none',d=None,op=1):
    o.append('<polygon points="%s" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="%s"%s stroke-linejoin="round"/>' % (' '.join('%.1f,%.1f'%p for p in pts),f,op,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def path(dstr,sw=1,c='#111',f='none',d=None):
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (dstr,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def arr(x1,y1,x2,y2,c='#c0392b',w=1.3):
    ln(x1,y1,x2,y2,w,c); a=math.atan2(y2-y1,x2-x1)
    for s in (1,-1): ln(x2,y2,x2-7*math.cos(a-s*.42),y2-7*math.sin(a-s*.42),w,c)
def dim(x1,y1,x2,y2,s,fs=5.6,off=0,col='#111'):
    ln(x1,y1,x2,y2,.7,col)
    for (x,y) in ((x1,y1),(x2,y2)):
        if abs(y2-y1)<abs(x2-x1): ln(x,y-3,x,y+3,.7,col)
        else: ln(x-3,y,x+3,y,.7,col)
    if abs(y2-y1)<abs(x2-x1): tx((x1+x2)/2,y1-3+off,s,fs,'middle','bold',col)
    else: tx(x1+4+off,(y1+y2)/2+2,s,fs,'start','bold',col)
def para(x,y,s,maxc,fs=5.9,col='#333',fw='',lh=None):
    lh = lh or fs*1.6; cur=''; lines=[]
    for wd in s.split(' '):
        if cur and len(cur)+1+len(wd) > maxc: lines.append(cur); cur=wd
        else: cur = (cur+' '+wd) if cur else wd
    if cur: lines.append(cur)
    for l in lines: tx(x,y,l,fs,'start',fw,col); y += lh
    return y
def hatch(x,y,w,h,step=4,c='#999',f='#f3f0e6'):
    rc(x,y,w,h,.6,0,c,None,f)
    k=0
    while k < w+h:
        x1=x+max(0,k-h); y1=y+min(k,h); x2=x+min(k,w); y2=y+max(0,k-w)
        ln(x1,y1,x2,y2,.4,c); k+=step
def f1(v): return ('%.1f' % v).replace('.',',')

GRN, RED, BLU, GRY, AMB, PUR, GOLD, ICE, KRAFT = '#1d7a4f','#c0392b','#1a49b8','#666','#b7791f','#6b4fa8','#c9a227','#e3f2fb','#e8d8b0'
# ---------------- sayılar ----------------
BL_W, BL_D, T_BL, M_BL = 40.0, 76.0, 0.16, 0.115          # blank 40×76 cm, E-dalga 1,6 mm, 115 g
BOX = 32.0; WALL = 4.0; WIN = 32.5
ZC = {'plint':(0,12),'pano':(12,30),'motor':(30,45),'yoke':(45,55),'kalip':(55,60),'yukleme':(60,104),'sarjor':(104,188),'ust':(188,197)}
STACK_H = ZC['sarjor'][1]-ZC['sarjor'][0]                   # 84
N_FULL = int(STACK_H/T_BL)                                   # 525
PIDE = 80
def gun(n): return n/PIDE
N3, N5, N7 = 3*PIDE, 5*PIDE, 7*PIDE
CUP_N, CUP_D, VAC = 6, 4.0, 7.0                              # 6 vantuz Ø40, −0,7 bar = 7 N/cm²
F_CUP = CUP_N*math.pi*(CUP_D/2)**2*VAC                       # 528 N
MU = 0.35
def f_need(kg): return MU*kg*9.81+50
STROKE = ZC['sarjor'][0]-(60-WALL)                           # 48

o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H))
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,40,'AUTOKITCH — PACK v4 (6 Eyl 2026) — ÜSTTEN BESLEMELİ KUTU AÇICI: açık kutular üstte yığın (84 cm = %d kutu) · alttan vakumla çekilir · kalıptan geçirilir (1 vuruş) · plakaya yükselir · pide · kapak · robot alır · KOLON 70 × 84 × 197' % N_FULL,13.5,'start','bold')
tx(30,62,'Kemal: "kutular üstte dizili olsun, katlama altta; üstten insin, katlansın, düz zemine yükselsin, pide konsun, kapağı kapansın, robot alsın · en az 3 gün, gönül ister 7 · üstten aşağıya nasıl taşıyacak, nasıl ittirecek?" — Cevap: iten yok, ÇEKEN var (vakum plunger alttan); kalıp = katlayan.',9,'start','','#444')
ln(30,74,W-30,74,.8,'#999')

# ================= A · AÇILMIŞ KUTU (BLANK) =================
XA,YA,WA,HA_ = 40,90,300,420
rc(XA,YA,WA,HA_,1.4,4,'#111',None,'#fff')
tx(XA+14,YA+22,'A · AÇILMIŞ KUTU (blank) 40 × 76 — üstten',10,'start','bold')
KA=3.9; ax=XA+70; ay=YA+52+KA*BL_D
BX=lambda x: ax+KA*x; BY=lambda y: ay-KA*y     # y: önden arkaya (0 ön)
rc(BX(0),BY(BL_D),KA*BL_W,KA*BL_D,1.2,1,'#111',None,KRAFT)
# kesikler (köşeler yok)
for (x0,y0) in ((0,72),(36,72)): rc(BX(x0),BY(y0+4),KA*4,KA*4,0,0,'none',None,'#fff')
# kırım çizgileri
for xx in (4,36): ln(BX(xx),BY(0),BX(xx),BY(76),.7,'#7a5c2e','3,2')
for yy in (4,36,40,72): ln(BX(0 if yy!=72 else 4),BY(yy),BX(40 if yy!=72 else 36),BY(yy),.7,'#7a5c2e','3,2')
# kesim çizgileri (tırnak/flap ayrımı) kırmızı
for yy in (4,36,40):
    for (x0,x1) in ((0,4),(36,40)): ln(BX(x0),BY(yy),BX(x1),BY(yy),1.1,RED)
for xx in (4,36): ln(BX(xx),BY(72),BX(xx),BY(76),1.1,RED)
# etiketler
tx(BX(20),BY(2)+2,'ÖN DUVAR 4',4.6,'middle','bold','#5a3d13'); tx(BX(2),BY(2)+1.5,'tırnak',3.4,'middle','',RED); tx(BX(38),BY(2)+1.5,'tırnak',3.4,'middle','',RED)
txr(BX(2),BY(20),'YAN DUVAR 4',4.2,'#5a3d13','bold'); txr(BX(38),BY(20),'YAN DUVAR 4',4.2,'#5a3d13','bold')
tx(BX(20),BY(22)+2,'TABAN 32 × 32',6,'middle','bold','#5a3d13'); tx(BX(20),BY(17)+2,'(pencereden aşağı çekilen panel)',4,'middle','',GRY)
tx(BX(20),BY(38)+2,'ARKA DUVAR 4 = kapak menteşesi',4.6,'middle','bold','#5a3d13'); tx(BX(2),BY(38)+1.5,'tırnak',3.4,'middle','',RED); tx(BX(38),BY(38)+1.5,'tırnak',3.4,'middle','',RED)
tx(BX(20),BY(57)+2,'KAPAK 32 × 32',6,'middle','bold','#5a3d13'); tx(BX(20),BY(52)+2,'(açıkken plakada düz yatar)',4,'middle','',GRY)
txr(BX(2),BY(56),'yan flap 4',4,'#5a3d13'); txr(BX(38),BY(56),'yan flap 4',4,'#5a3d13')
tx(BX(20),BY(74)+2,'ÖN DİL 4 (ön duvarın içine girer)',4.4,'middle','bold','#5a3d13')
tx(BX(2),BY(74)+1.5,'kesik',3.2,'middle','',GRY); tx(BX(38),BY(74)+1.5,'kesik',3.2,'middle','',GRY)
dim(BX(0),BY(76)-10,BX(40),BY(76)-10,'40 = 4 + 32 + 4',5.2)
dim(BX(40)+14,BY(76),BX(40)+14,BY(0),'76 = 4+32+4+32+4',5.2)
dim(BX(-12),BY(4),BX(-12),BY(0),'4',4.4,0,GRY); dim(BX(-12),BY(36),BX(-12),BY(4),'32',4.4,0,GRY); dim(BX(-12),BY(72),BX(-12),BY(40),'32',4.4,0,GRY)
tx(BX(20),BY(-3.5),'ÖN (robot tarafı)',4.6,'middle','bold',GRY)
para(XA+14,YA+372,'Kırmızı = kesim, kesikli = kırım. KÖŞE TIRNAKLI tepsi tipi: makinede tek vuruşta açılır (tırnak yan duvarın içine kıvrılır). E-dalga 3 katlı kraft 1,6 mm, %d g. TR standart kutular: 24 · 26 · 28 · 30 · 33 · 36 · 40 kare, boy 3,5–4,5; bizim Ø30 pide → 32×32×4 (33 standart kalıp da olur: blank 41×78, kabine 1 cm payla sığar).' % int(M_BL*1000),70,5.1,'#333')

# ================= B · KOLON KESİTİ (yandan) =================
XB,YB,WB,HB = 360,90,330,640
rc(XB,YB,WB,HB,1.4,4,'#111',None,'#fcfbf8')
tx(XB+14,YB+22,'B · KOLON YAN KESİTİ 84 × 197 — akış yukarıdan aşağı',10,'start','bold')
K=2.6; bx=XB+62; bz=YB+50+K*197
XS=lambda d: bx+K*d; ZS=lambda z: bz-K*z
rc(XS(0),ZS(197),K*84,K*197,1.4,2,'#111',None,'#fff')
ZONCOL={'plint':'#e9e4d6','pano':'#e3f2fb','motor':'#eef3f8','yoke':'#f4f0fa','kalip':'#f4f0fa','yukleme':'#fbf3e6','sarjor':'#fff8e0','ust':'#e9e4d6'}
for k_,(z0,z1) in ZC.items():
    rc(XS(2),ZS(z1),K*80,K*(z1-z0),.6,0,'#777',None,ZONCOL[k_])
tx(XS(42),ZS(6)+2,'plint 12 — hava / boş',4.4,'middle','','#333')
tx(XS(42),ZS(21)+2,'PANO 18: PLC · step sürücü · 2 motor sürücü · 3 servo · 24 V',4.4,'middle','bold','#333')
rc(XS(6),ZS(44),K*16,K*13,1,2,'#333',None,'#ddd'); tx(XS(14),ZS(38)+2,'STEP',4,'middle','bold'); tx(XS(14),ZS(34)+2,'NEMA 23',3.4,'middle','','#555')
rc(XS(56),ZS(44),K*20,K*12,1,2,'#333',None,'#eee'); tx(XS(66),ZS(39)+2,'VAKUM POMPASI',3.8,'middle','bold'); tx(XS(66),ZS(35)+2,'24 V · 30 L/dk · −0,75 bar',3.2,'middle','','#555')
# vida + ray
ln(XS(14),ZS(45),XS(14),ZS(104),1.6,'#333'); txr(XS(12),ZS(88),'bilyalı vida + 2 ray · strok %d' % STROKE,3.6,'#333')
# boyunduruk (yoke) — katlama konumu: plunger üstü z 56
rc(XS(4),ZS(55),K*72,K*3,1.1,1,PUR,None,'#ece6f6'); tx(XS(40),ZS(46.8)+2,'BOYUNDURUK 36×72 (tek dikey eksen)',4.2,'middle','bold',PUR)
rc(XS(5.9),ZS(58),K*31.6,K*2,1.1,1,PUR,None,'#ece6f6'); tx(XS(21.7),ZS(53)+2,'plunger 31,6 + 4 vantuz',3.8,'middle','',PUR)
for yv in (9,34): rc(XS(yv-1.5),ZS(59),K*3,K*1,.7,0,PUR,None,'#fff')
for yp in (50,68): ln(XS(yp),ZS(55),XS(yp),ZS(59),1.2,PUR); rc(XS(yp-1.5),ZS(60),K*3,K*1,.7,0,PUR,None,'#fff')
tx(XS(60),ZS(50.6)+2,'2 kapak vantuzu (yarıktan)',3.6,'middle','',PUR)
# kalıp plakası z 60, pencere y 5,5–38, kalıp duvarları altta
rc(XS(2),ZS(60.6),K*80,K*0.6,.8,0,'#333',None,'#999')
rc(XS(5.5),ZS(60),K*0.6,K*4.5,.8,0,'#333',None,'#666'); rc(XS(37.4),ZS(60),K*0.6,K*4.5,.8,0,'#333',None,'#666')
tx(XS(21.7),ZS(63)+2,'kalıp pencere 32,5 · duvar 4,5 · köşe plowları',3.6,'middle','','#333')
tx(XS(61),ZS(70.5)+2,'arka raylar + 3 flap parmağı (hemzemin)',3.6,'middle','','#333')
# kutu plakada (kapak açık arkada)
rc(XS(5.9),ZS(64.6),K*32.3,K*4,1.2,0,'#5a3d13',None,KRAFT)
ln(XS(38.2),ZS(64.6),XS(42),ZS(60.6),1.2,'#5a3d13'); ln(XS(42),ZS(60.6),XS(78),ZS(60.6),1.6,'#5a3d13')
tx(XS(15.5),ZS(66.3)+2,'KUTU plakada · kapak açık arkada',4.2,'start','bold','#5a3d13')
# kapak yayı
path('M %.1f %.1f A %.1f %.1f 0 0 0 %.1f %.1f' % (XS(74),ZS(64.6),K*36,K*36,XS(2),ZS(64.6)),.8,'#5a3d13','none','4,3')
tx(XS(40),ZS(102.2)+2,'kapak yayı r 36 → tepe z 100 < 104 ✓',3.8,'middle','','#5a3d13')
# çevirme kolu (dirsekli, plakada yuvada)
ln(XS(38),ZS(64.6),XS(42),ZS(60.6),1.4,GRN); ln(XS(42),ZS(60.6),XS(68),ZS(60.6),1.4,GRN); ci(XS(38),ZS(64.6),1.6,1,GRN,None,GRN)
tx(XS(61),ZS(62.4)+2,'çevirme kolu U Ø8 (yuvada) · 24 V redüktör',3.6,'middle','',GRN)
# ön dil parmağı
rc(XS(72),ZS(61),K*6,K*0.5,.8,0,AMB,None,'#fde9c9')
# vantuz stroku ve blank inişi
arr(XS(21.7),ZS(72),XS(21.7),ZS(97),PUR,1.1); tx(XS(21.7)+3,ZS(88)+2,'plunger yukarı %d' % STROKE,3.8,'start','',PUR)
arr(XS(30),ZS(97),XS(30),ZS(72),'#5a3d13',1.1); tx(XS(30)+3,ZS(78)+2,'blank aşağı',3.8,'start','','#5a3d13')
# şarjör: yığın
rc(XS(1.5),ZS(188),K*76,K*84,.8,0,'#5a3d13',None,KRAFT)
for i in range(1,21): ln(XS(1.5),ZS(104+i*4),XS(77.5),ZS(104+i*4),.35,'#a8905e')
tx(XS(40),ZS(150)+2,'ŞARJÖR — %d açık kutu yatay yığın (84 cm)' % N_FULL,5,'middle','bold','#5a3d13')
tx(XS(40),ZS(143)+2,'%d pide/gün → 3 gün %d = %s cm · 5 gün %d = %s cm · dolu %s gün' % (PIDE,N3,f1(N3*T_BL),N5,f1(N5*T_BL),f1(gun(N_FULL))),3.8,'middle','','#5a3d13')
# tutucu raylar (snubber)
for yy in (1.5,77.5): rc(XS(yy-0.5 if yy<40 else yy-1),ZS(104.6),K*1.5,K*0.6,.8,0,'#333',None,'#333')
tx(XS(40),ZS(106.5)+2,'alt tutucu raylar: yan 2 × 76 × 1 + 4 köşe parmağı — yığının ağırlığı burada',3.6,'middle','','#333')
# klape + ön kapı
rc(XS(0),ZS(104),K*1.2,K*44,1,0,BLU,None,'#dfe7fb'); txr(XS(3.4),ZS(84),'KLAPE 66×44 (robot açıklığı)',3.6,BLU,'bold')
rc(XS(0),ZS(197),K*1.2,K*93,1,0,AMB,None,'#fde9c9'); txr(XS(-3),ZS(150),'ÖN KAPI (eleman): demetleri sürer',3.8,AMB,'bold')
# robot tepsisi
el(XS(-10.5),ZS(75.5),K*10.5,K*1.6,1.4,BLU,None,'none',-28); ln(XS(-19.5),ZS(79.5),XS(-23),ZS(81),2,BLU)
arr(XS(-3),ZS(72),XS(8),ZS(66),'#5a3d13',1.1); tx(XS(-12),ZS(85)+2,'tepsi eğilir',3.8,'middle','',BLU)
tx(XS(-13),ZS(69)+2,'pide kayar',3.6,'middle','','#5a3d13')
# ölçüler
for k_,lab in (('plint','12'),('pano','18'),('motor','15'),('yoke','10'),('kalip','5'),('yukleme','44'),('sarjor','84'),('ust','9')):
    z0,z1=ZC[k_]; dim(XS(84)+14,ZS(z1),XS(84)+14,ZS(z0),lab,4.6,0,GRY)
dim(XS(0),ZS(197)-14,XS(84),ZS(197)-14,'84 (blank 76 + pay 2×4)',5)
tx(XS(4),ZS(192)+2,'ÖN',4.6,'start','bold',GRY); tx(XS(80),ZS(192)+2,'ARKA',4.6,'end','bold',GRY)
para(XB+14,YB+572,'Zonlar (zeminden): plint 12 · pano 18 · step + vakum pompası 15 · boyunduruk 10 · kalıp 5 → PLAKA z 60 · yükleme 44 (kapak yayı 40) · şarjör 84 (z 104–188) · üst pay 9 = 197 ✓. Tek dikey eksen 3 iş yapar: yukarıda blank alır, aşağıda kalıptan çeker, plakaya/robota kaldırır.',80,5.1,'#333')

# ================= C · ÜST GÖRÜNÜM (plaka) =================
XC,YC,WC,HC = 710,90,300,330
rc(XC,YC,WC,HC,1.4,4,'#111',None,'#fff')
tx(XC+14,YC+22,'C · ÜST GÖRÜNÜM 70 × 84 — kalıp plakası (z 60)',10,'start','bold')
KC=2.9; cx=XC+50; cy=YC+40+KC*84
PX=lambda x: cx+KC*x; PY=lambda y: cy-KC*y     # y: önden arkaya
rc(PX(0),PY(84),KC*70,KC*84,1.3,2,'#111',None,'#fff')
rc(PX(2),PY(82),KC*66,KC*80,.7,0,'#777',None,'#f4f4f4')
rc(PX(15),PY(77.5),KC*40,KC*76,.6,0,'#5a3d13','3,2',KRAFT)                                # blank izi
rc(PX(18.75),PY(38),KC*32.5,KC*32.5,1.2,0,'#111',None,'#fff'); tx(PX(35),PY(22)+2,'PENCERE 32,5',5,'middle','bold'); tx(PX(35),PY(17)+2,'kutu burada oluşur',3.8,'middle','',GRY)
for (xx,yy) in ((18.75,5.5),(51.25,5.5),(18.75,38),(51.25,38)):
    poly([(PX(xx),PY(yy)),(PX(xx+(1.6 if xx<35 else -1.6)),PY(yy)),(PX(xx),PY(yy+(1.6 if yy<20 else -1.6)))],.6,RED,'#f7d7d7')
tx(PX(35),PY(8.5)+2,'köşe plowları ×4 (plaka altı)',3.4,'middle','',RED)
for (xx,yy) in ((22,9),(48,9),(22,34),(48,34)): ci(PX(xx),PY(yy),KC*2,.8,PUR,'3,2','none')
for yy in (50,68): ci(PX(35),PY(yy),KC*2,.8,PUR,'3,2','none'); rc(PX(33.5),PY(yy+2.2),KC*3,KC*4.4,.6,0,PUR,None,'#ece6f6')
tx(PX(35),PY(29)+2,'6 vantuz Ø40: 4 taban + 2 kapak (yarıktan)',3.4,'middle','',PUR)
rc(PX(30),PY(79),KC*10,KC*41,.6,0,'#777',None,'#e6e6e6'); txr(PX(43),PY(60),'orta ray',3.2,'#555')
hatch(PX(15),PY(74),KC*4,KC*32,3,AMB,'#fde9c9'); hatch(PX(51),PY(74),KC*4,KC*32,3,AMB,'#fde9c9'); hatch(PX(19),PY(78),KC*32,KC*4,3,AMB,'#fde9c9')
tx(PX(35),PY(80)+1.5,'ön dil parmağı',3.2,'middle','',AMB); txr(PX(17),PY(58),'yan flap parmağı',3.2,AMB); txr(PX(53),PY(58),'yan flap parmağı',3.2,AMB)
# çevirme kolu U
ln(PX(13),PY(38),PX(13),PY(68),1.4,GRN); ln(PX(57),PY(38),PX(57),PY(68),1.4,GRN); ln(PX(13),PY(68),PX(57),PY(68),1.4,GRN)
ci(PX(13),PY(38),1.5,1,GRN,None,GRN); ci(PX(57),PY(38),1.5,1,GRN,None,GRN); tx(PX(35),PY(70.5)+1.5,'çevirme kolu U (menteşe y 38)',3.2,'middle','',GRN)
# yığın kılavuzları
for xx in (14.5,55): rc(PX(xx-0.3 if xx<30 else xx),PY(78),KC*0.6,KC*77,1,0,'#333',None,'#333')
tx(PX(9),PY(40)+2,'kılavuz',3.2,'middle','','#333'); tx(PX(61),PY(40)+2,'kılavuz',3.2,'middle','','#333')
# ray + vida
for (xx,yy,lab) in ((8,45,'vida'),(62,45,'ray'),(8,75,'ray')): ci(PX(xx),PY(yy),KC*0.9,.8,'#333',None,'#ccc'); tx(PX(xx),PY(yy-3.5)+1,lab,3,'middle','','#555')
# robot tepsisi önde
path('M %.1f %.1f A %.1f %.1f 0 0 1 %.1f %.1f' % (PX(19),PY(0),KC*16,KC*16,PX(51),PY(0)),1,BLU,'none','4,3'); tx(PX(35),PY(-4),'tepsi Ø32 (önden eğilir)',3.6,'middle','',BLU)
dim(PX(0),PY(-13.5),PX(70),PY(-13.5),'70',5); dim(PX(70)+12,PY(84),PX(70)+12,PY(0),'84',5)
tx(PX(35),PY(-9),'ÖN (robot)',4.4,'middle','bold',GRY)

# ================= D · ÇEVRİM =================
XD,YD,WD,HD = 1030,90,390,330
rc(XD,YD,WD,HD,1.4,4,'#111',None,'#fcfdff')
tx(XD+14,YD+22,'D · ÇEVRİM — bir kutu nasıl doğar (≈ 15 sn, pide 4 dk’da bir)',10,'start','bold')
steps=[('1','AL: plunger %d cm yukarı çıkar, 6 vantuz yığının EN ALT kutusuna yapışır, vakum açılır (0,5 sn).' % STROKE),
       ('2','İN: eksen aşağı; blank tutucu raylardan 1 cm bükülerek sıyrılır, 44 cm inip plakaya yatar (2 sn). Yığının ağırlığı yardım eder, kimse itmez.'),
       ('3','KATLA: taban 4 cm pencereden çekilir; 4 duvar kırımdan kalkar, köşe tırnakları plowla yan duvarın içine kıvrılır (1 sn). Kapak plakada düz kalır.'),
       ('4','YÜKSEL: eksen 4 cm yukarı; kutu kalıptan çıkıp plakaya oturur, vakum kapanır. HAZIR — pide gelene kadar bekler.'),
       ('5','PİDE: robot tepsiyi ön duvarın üstünde eğer, 4 parça kutuya kayar (5 sn).'),
       ('6','KAPAK: 3 flap parmağı flapları 90° kaldırır (1 sn); U kol kapağı 180° çevirir, flaplar duvarların içine girer, ön dil ön duvarın içine oturur; kol geri döner (4 sn).'),
       ('7','VER: eksen 6 cm daha kalkar, kutu plakadan yükselir; robot PENÇE yanlardan tutar, PICKUP dolabına götürür (4 sn).'),
       ('8','Eksen 48 cm yukarı → 1. adım; sıradaki kutu 6 sn içinde hazır. Kutu gelmezse (sensör) 2. deneme, sonra alarm.')]
yy=YD+42
for n,s_ in steps:
    tx(XD+16,yy,n,7.5,'start','bold',BLU); yy=para(XD+30,yy,s_,84,5.8,'#333')+4

# ================= E · STOK =================
XE,YE,WE,HE = 710,440,300,290
rc(XE,YE,WE,HE,1.4,4,'#111',None,'#fff')
tx(XE+14,YE+22,'E · KAÇ GÜN GİDER? (%d pide/gün)' % PIDE,10,'start','bold')
rows=[('blank','40×76 · E-dalga 1,6 mm · %d g' % int(M_BL*1000)),('şarjör boyu','84 cm (z 104–188) = %d kutu' % N_FULL),
      ('3 gün','%d kutu · %s cm · %s kg' % (N3,f1(N3*T_BL),f1(N3*M_BL))),('5 gün','%d kutu · %s cm · %s kg' % (N5,f1(N5*T_BL),f1(N5*M_BL))),
      ('7 gün','%d kutu · %s cm ✗ sığmaz' % (N7,f1(N7*T_BL))),('tam dolu','%d kutu · %s gün · %s kg' % (N_FULL,f1(gun(N_FULL)),f1(N_FULL*M_BL))),
      ('vantuz','%d × Ø%d −0,7 bar = %d N' % (CUP_N,int(CUP_D*10),int(F_CUP))),('gereken','3 gün %d N · dolu %d N' % (int(f_need(N3*M_BL)),int(f_need(N_FULL*M_BL))))]
yy=YE+44
for a_,b_ in rows: tx(XE+14,yy,a_,5.4,'start','bold','#111'); tx(XE+82,yy,b_,5.4,'start','','#333'); yy+=12.5
yy=para(XE+14,yy+4,'KARAR: 3 gün GARANTİ (38 cm, tipik makine şarjörü 30–40 cm), 5 gün HEDEF (64 cm), tam dolu 6,5 gün (84 cm) — dolu yığında vantuz payı 1,2× (pilotta doğrulanır; olmazsa şarjör 60 cm = 4,7 gün). 7 gün 90 cm ister, kolona sığmaz.',58,5.2,GRN,'bold')
yy=para(XE+14,yy+2,'Eleman haftada 1: 50'+AP+'lik demetleri (8 cm, 5,8 kg) ön kapıdan üstten sürer (z 104–188, göğüs hizası). "Kutu az" sensörü 1 gün kala BEYİN'+AP+'e yazar; yanlış yön kılavuzu (kapak arkaya).',58,5.1,'#333')

# ================= F · PARÇALAR =================
XF,YF,WF,HF = 1030,440,390,290
rc(XF,YF,WF,HF,1.4,4,'#111',None,'#fff')
tx(XF+14,YF+22,'F · PARÇALAR (hepsi elektrikli, kompresör yok) · SENSÖRLER',10,'start','bold')
parts=[('DİKEY EKSEN','bilyalı vida 1605 + 2 lineer ray Ø16, NEMA 23 step 3 N·m + sürücü; strok 50, 25 cm/sn, ≥ 500 N. Boyunduruk alu profil 36×72; plunger plakası 31,6×31,6×2 alu.'),
       ('VAKUM','6 körüklü vantuz Ø40 (4 plungerde, 2 kapak postunda); 24 V diyafram pompa 30 L/dk −0,75 bar 20 W; 1 L tank; 2 selenoid (taban / kapak grubu); vakum sensörü.'),
       ('KALIP','paslanmaz plaka 3 mm 66×79; pencere 32,5; kalıp duvarı 4,5 derin; 4 köşe plowu; yan duvar kenarı 5 mm alçak (önce tırnak, sonra duvar). Arka: orta ray yarıklı + 3 flap parmağı + 3 servo 25 kg·cm.'),
       ('KAPAK KOLU','U çubuk Ø8 paslanmaz, dirsekli kollar x 13/57, çapraz y 68; 24 V sonsuz vida redüktör 5 N·m 10 d/dk; 2 switch.'),
       ('ŞARJÖR','2 L kılavuz (iç 40), ön/arka dayama; alt tutucu raylar 2 × 76 × 1 cm + 4 köşe parmağı; seviye foto sensörü ×3 (dolu / 1 gün / boş).'),
       ('SENSÖR','plakada blank var · kutu oluştu (eksen konumu + akım) · kapak kapalı · kutu alındı · vakum OK. Pano 18: PLC I/O, sürücüler, 24 V PSU.')]
yy=YF+42
for a_,b_ in parts:
    tx(XF+14,yy,a_,5.6,'start','bold',BLU); yy=para(XF+80,yy,b_,74,5.5,'#333')+4

# ================= G · SORULAR — CEVAPLAR =================
XG,YG,WG,HG = 40,750,1380,178
rc(XG,YG,WG,HG,1.4,4,'#111',None,'#fcfdff')
tx(XG+14,YG+22,'G · KEMAL'+AP+'İN SORULARI — CEVAPLAR',10,'start','bold')
QA=[('STANDART PİZZA KUTUSU NE?','Türkiye'+AP+'de kare kutu 24–40 cm arası (26 · 30 · 33 · 36 en yaygın), boy 3,5–4,5, E-dalga 3 katlı kraft, tırnak kilitli ön kapak. Bizim: 32×32×4 (Ø30 pide + 1 cm pay). Açık hâli 40×76 (panel A). Kalıp bizim çizime göre üretici bıçak kalıbı yapar (özel baskıyla zaten sipariş edilecek).'),
    ('ÜSTTEN AŞAĞIYA NASIL İNER, KİM İTER?','Kimse itmez, ÇEKİLİR: plunger alttan yükselir, yığının en alt kutusuna yapışır (6 vantuz), aşağı çeker. Yığın raylarda durur, sadece en alttaki iner. Videodaki makine üstten alıp yana taşır; bizde yana yer yok, akış dikey.'),
    ('NASIL KATLANIR?','Kalıp = kenarları 32,5 pencere. Taban pencereden 4 cm çekilince 4 duvar kırım yerinden kalkar (senin dediğin gibi "itince katlanır" — biz çekiyoruz). Köşe tırnaklarını plowlar yan duvarın içine kıvırır → kilit. Tek vuruş, 1 sn, ek parmak yok.'),
    ('KAPAK NASIL KAPANIR?','Kapak açıkken plakada düz yatar. 3 küçük parmak flapları 90° kaldırır, U kol kapağı 180° çevirir; flaplar duvarların içine, ön dil ön duvarın içine girer (elle kapatmanın aynısı). Robot yedek: pençeyle de kapatabilir.'),
    ('ROBOT NASIL KOYAR, NASIL ALIR?','Koyma eskisi gibi: tepsi ön duvarın üstünde eğilir, 4 parça kayar. Alma: eksen kutuyu 6 cm kaldırır, pençe yanlardan tutar (0,7 kg), PICKUP'+AP+'a götürür. Kesim artık OVEN'+AP+'de (v4 pres).'),
    ('3 GÜN MÜ, 7 GÜN MÜ?','Kolona 84 cm şarjör sığar = %d kutu = %s gün (80 pide). 7 gün 90 cm ister, sığmaz. 3 gün garanti, 5 gün hedef; dolu yığın 60 kg vantuz sınırında → pilotta 40 cm ile başlanır.' % (N_FULL,f1(gun(N_FULL)))),
    ('VİDEODAKİ MAKİNEDEN FARKI?','Aynı ilke (vakumla al, kalıpla katla), 3 fark: yatay → dikey (aynı ayak izi), pnömatik → elektrik (yalnız küçük vakum pompası, kompresör yok), 1,5 m tezgâh → 70×84 kolon. Hız 1 kutu/15 sn bize yeter (onlar 600/saat).'),
    ('ELEMAN NE YAPAR?','Haftada 1 (kap/yağ ziyaretinde) ön kapıdan demetleri sürer, 5 dk. Ayda 1 vantuz ve plaka silme. Sıkışma alarmı: klapeden kutuyu alır. Başka iş yok; katlama işi bitti.')]
col_x=(XG+14, XG+700); yy=[YG+42,YG+42]
for i,(q,a_) in enumerate(QA):
    c=i%2; tx(col_x[c],yy[c],q,6.2,'start','bold',RED if c==0 else BLU); yy[c]=para(col_x[c],yy[c]+9,a_,112,5.4,'#333')+3
tx(W-40,H-8,'AUTOKITCH · arastirma/5_PACK/kutu_istasyonu_teknik_v4 · 6 Eyl 2026',7,'end','',GRY)
o.append('</svg>')
svg=chr(10).join(o)
xml.dom.minidom.parseString(svg.encode('utf-8'))
out=r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\5_PACK\kutu_istasyonu_teknik_v4.svg"
io.open(out,'w',encoding='utf-8').write(svg)
print('yazildi + XML gecerli | dolu %d kutu %.1f gun %.1f kg · vantuz %d N · gerek dolu %d N / 3 gun %d N' % (N_FULL,gun(N_FULL),N_FULL*M_BL,F_CUP,f_need(N_FULL*M_BL),f_need(N3*M_BL)))
