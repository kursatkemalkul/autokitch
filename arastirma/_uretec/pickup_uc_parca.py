# -*- coding: utf-8 -*-
# PICKUP cephesi 3 ayrı teknik resim (7 Eyl 2026): (1) sipariş ekranı 45×104×14 duvar tipi, (2) teslim dolabı 124×165×52, (3) kod ünitesi 20×34×8.
# Kemal: yalnız teknik resim (ön/üst/yan), soru-cevap ve akış görseli YOK, gereksiz hacim YOK, vandalizm + kendiliğinden kapanan kapı.
import io, math, xml.dom.minidom
AP=chr(39); OUTDIR=r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\6_PICKUP"
GRY,BLU,RED,GRN,AMB,DARK,STEEL,PU,GLASS='#666','#1a49b8','#c0392b','#1d7a4f','#b7791f','#2b2e33','#cfd3d8','#f3e6d3','#dbeeff'
class D:
    def __init__(s,W,H): s.W,s.H,s.o=W,H,[]
    def esc(s,t): return str(t).replace('&','&amp;').replace('<','&lt;')
    def ln(s,x1,y1,x2,y2,w=1,c='#111',d=None): s.o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s stroke-linecap="round"/>'%(x1,y1,x2,y2,c,w,(' stroke-dasharray="%s"'%d) if d else ''))
    def rc(s,x,y,w,h,sw=1,r=0,c='#111',d=None,f='none'): s.o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>'%(x,y,w,h,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
    def ci(s,x,y,r,sw=1,c='#111',d=None,f='none'): s.o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>'%(x,y,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
    def tx(s,x,y,t,fs=8,anc='start',fw='',col='#111'): s.o.append('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="%s" font-weight="%s" fill="%s" font-family="Segoe UI, Arial, sans-serif">%s</text>'%(x,y,fs,anc,fw or 'normal',col,s.esc(t)))
    def txr(s,x,y,t,fs=5,col='#555',fw=''): s.o.append('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="middle" font-weight="%s" fill="%s" font-family="Segoe UI, Arial, sans-serif" transform="rotate(-90 %.1f %.1f)">%s</text>'%(x,y,fs,fw or 'normal',col,x,y,s.esc(t)))
    def dim(s,x1,y1,x2,y2,t,fs=6,col='#111'):
        s.ln(x1,y1,x2,y2,.7,col)
        for (x,y) in ((x1,y1),(x2,y2)):
            if abs(y2-y1)<abs(x2-x1): s.ln(x,y-3,x,y+3,.7,col)
            else: s.ln(x-3,y,x+3,y,.7,col)
        if abs(y2-y1)<abs(x2-x1): s.tx((x1+x2)/2,y1-3,t,fs,'middle','bold',col)
        else: s.txr(x1-5,(y1+y2)/2,t,fs,col,'bold')
    def hatch(s,x,y,w,h,step=4,c='#999',f='#f3f0e6'):
        s.rc(x,y,w,h,.6,0,c,None,f); k=0
        while k<w+h: s.ln(x+max(0,k-h),y+min(k,h),x+min(k,w),y+max(0,k-w),.4,c); k+=step
    def para(s,x,y,t,maxc,fs=6.2,col='#333',fw=''):
        lh=fs*1.55; cur=''; lines=[]
        for wd in t.split(' '):
            if cur and len(cur)+1+len(wd)>maxc: lines.append(cur); cur=wd
            else: cur=(cur+' '+wd) if cur else wd
        if cur: lines.append(cur)
        for l in lines: s.tx(x,y,l,fs,'start',fw,col); y+=lh
        return y
    def lead(s,x1,y1,x2,y2,t,fs=5.6,col='#333',anc='start'):
        s.ln(x1,y1,x2,y2,.6,col); s.ci(x1,y1,1.2,.6,col,None,col); s.tx(x2+(3 if anc=='start' else -3),y2+2,t,fs,anc,'',col)
    def title(s,t,sub):
        s.rc(0,0,s.W,s.H,0,0,'none',None,'#fff'); s.tx(30,36,t,13,'start','bold'); s.tx(30,54,sub,8.5,'start','','#444'); s.ln(30,64,s.W-30,64,.8,'#999')
    def box(s,x,y,w,h,t): s.rc(x,y,w,h,1.2,4,'#111',None,'#fff'); s.tx(x+12,y+18,t,9.5,'start','bold')
    def save(s,name):
        svg='<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'%(s.W,s.H,s.W,s.H)+chr(10).join(s.o)+'</svg>'
        xml.dom.minidom.parseString(svg.encode('utf-8')); p=OUTDIR+'\\'+name+'.svg'; io.open(p,'w',encoding='utf-8').write(svg); print('ok',name); return p

# ======================================================= 1 · SİPARİŞ EKRANI =======================================================
d=D(1200,760); d.title('AUTOKITCH — SİPARİŞ EKRANI (KİOSK) v2 · duvar tipi 45 × 104 × 14 · zeminden 85–189','32" dokunmatik + ÖKC POS + fiş yazıcı + 2D okuyucu · arkada gövde YOK (14 cm, duvara asılır) · BEYİN yok, LAN istemci · ölçüler cm')
UW,UH,UD,Z0=45.0,104.0,14.0,85.0
# --- ön
d.box(30,80,400,650,'ÖN GÖRÜNÜŞ'); K=5.4; ox=100; oy=110+K*UH
X=lambda x: ox+K*x; Y=lambda y: oy-K*y
d.rc(X(0),Y(UH),K*UW,K*UH,1.6,3,'#111',None,STEEL)
d.rc(X(2.5),Y(101),K*40,K*71,1.2,2,'#111',None,DARK); d.tx(X(22.5),Y(66),'32" dokunmatik · 40 × 71 · cam 6 mm temperli',6,'middle','bold','#fff')
d.ci(X(22.5),Y(102.6),2,1,'#333',None,'#333'); d.tx(X(25),Y(102.6)+2,'kamera',5,'start','','#333')
for i in range(6): d.ln(X(4+i*1.2),Y(102.2),X(4+i*1.2),Y(103.2),.8,'#555')
d.rc(X(19.5),Y(28),K*6,K*3.5,1,1,'#333',None,'#9aa0a6'); d.tx(X(22.5),Y(23)+2,'2D okuyucu',5,'middle','','#333')
d.rc(X(3),Y(22),K*19,K*14,1.2,2,'#111',None,'#c9ced4'); d.rc(X(5),Y(19.5),K*15,K*9,1,1,'#333',None,'#e6e6e6'); d.tx(X(12.5),Y(14.5)+2,'ÖKC POS (temassız · çip)',5.2,'middle','bold'); d.tx(X(12.5),Y(10.5)+2,'yuvada, 20° eğik',4.6,'middle','','#333')
d.rc(X(26),Y(16.5),K*16,K*1.4,1,1,'#111',None,'#111'); d.tx(X(34),Y(20)+2,'fiş ağzı 80 mm',5.2,'middle','bold'); d.tx(X(34),Y(11)+2,'(yazıcı arkada)',4.6,'middle','','#333')
for i in range(8): d.ln(X(30+i*1.2),Y(3.5),X(30+i*1.2),Y(5.5),.8,'#555')
d.tx(X(34),Y(1.5)+2,'hoparlör',4.6,'middle','','#333')
d.dim(X(0),Y(UH)-12,X(UW),Y(UH)-12,'45'); d.dim(X(UW)+14,Y(UH),X(UW)+14,Y(0),'104')
d.dim(X(UW)+30,Y(101),X(UW)+30,Y(30),'ekran 71',5.2,GRY); d.dim(X(UW)+30,Y(22),X(UW)+30,Y(8),'POS 14',5.2,GRY)
d.tx(X(-6),Y(0)+2,'z 85',5.6,'end','bold',GRY); d.tx(X(-6),Y(UH)+2,'z 189',5.6,'end','bold',GRY); d.tx(X(-6),Y(15)+2,'z 100',5.2,'end','',GRY); d.tx(X(-6),Y(65)+2,'z 150',5.2,'end','',GRY)
# --- yan
d.box(450,80,330,650,'YAN GÖRÜNÜŞ (kesit)'); sx=560; sy=oy
SX=lambda x: sx+K*x; SY=lambda y: sy-K*y
d.hatch(SX(UD),SY(UH+6),K*6,K*(UH+12),4,'#b08968','#efe4d4'); d.txr(SX(UD+3),SY(UH/2),'DUVAR',6,'#7a5c2e','bold')
d.rc(SX(0),SY(UH),K*UD,K*UH,1.6,2,'#111',None,STEEL)
d.rc(SX(0),SY(101),K*0.6,K*71,.8,0,'#333',None,GLASS); d.rc(SX(0.6),SY(101),K*3.4,K*71,.8,0,'#333',None,DARK); d.tx(SX(2),SY(66)+2,'LCD',4.6,'middle','','#fff')
d.rc(SX(6),SY(60),K*4,K*12,1,1,'#333',None,'#eee'); d.tx(SX(8),SY(54)+2,'mini PC',4.4,'middle','bold'); d.tx(SX(8),SY(50)+2,'12×12×4',3.8,'middle','','#333')
d.rc(SX(6),SY(45),K*3,K*5,1,1,'#333',None,'#eee'); d.tx(SX(7.5),SY(42.5)+2,'PSU',4,'middle','','#333')
d.rc(SX(0.5),SY(28),K*4,K*3.5,1,1,'#333',None,'#9aa0a6')
d.rc(SX(1),SY(22),K*6,K*14,1,1,'#111',None,'#c9ced4'); d.ln(SX(1.5),SY(9),SX(5.5),SY(20),1.6,'#333'); d.tx(SX(4),SY(24)+2,'POS 20°',4.4,'middle','','#333')
d.rc(SX(1),SY(21),K*12,K*13,1.2,1,'#333',None,'#e6e6e6'); d.tx(SX(7),SY(15)+2,'FİŞ YAZICI',4.6,'middle','bold'); d.tx(SX(7),SY(11)+2,'12×14×13',3.8,'middle','','#333'); d.rc(SX(0),SY(17),K*1,K*1.4,.8,0,'#111',None,'#111')
d.ln(SX(UD),SY(50),SX(UD+6),SY(50),1.6,BLU); d.tx(SX(UD+3),SY(47)+2,'LAN + 220 V',4.4,'middle','',BLU)
d.dim(SX(0),SY(UH)-12,SX(UD),SY(UH)-12,'14'); d.tx(SX(-4),SY(0)+2,'z 85',5.6,'end','bold',GRY)
d.tx(SX(-2),SY(60)+2,'MÜŞTERİ',5.6,'end','bold',GRY)
# --- üst
d.box(800,80,370,320,'ÜST GÖRÜNÜŞ'); tx0=850; ty0=150
TX=lambda x: tx0+K*x; TY=lambda yd: ty0+K*yd    # yd: önden (0) arkaya (14)
d.hatch(TX(0),TY(UD),K*UW,K*6,4,'#b08968','#efe4d4'); d.tx(TX(22.5),TY(UD+4),'DUVAR',6,'middle','bold','#7a5c2e')
d.rc(TX(0),TY(0),K*UW,K*UD,1.6,2,'#111',None,STEEL)
d.rc(TX(2.5),TY(0),K*40,K*0.6,.8,0,'#333',None,GLASS); d.rc(TX(2.5),TY(0.6),K*40,K*3.4,.8,0,'#333',None,DARK); d.tx(TX(22.5),TY(2.8),'ekran',4.6,'middle','','#fff')
d.rc(TX(3),TY(8),K*12,K*4,1,1,'#333',None,'#eee'); d.tx(TX(9),TY(10.6),'mini PC',4.4,'middle','')
d.rc(TX(26),TY(1),K*14,K*12,1.2,1,'#333',None,'#e6e6e6'); d.tx(TX(33),TY(7.5),'fiş yazıcı',4.6,'middle','bold')
d.rc(TX(3),TY(1),K*19,K*6,1.2,1,'#111',None,'#c9ced4'); d.tx(TX(12.5),TY(4.6),'POS yuvası',4.6,'middle','')
d.ln(TX(22.5),TY(UD),TX(22.5),TY(UD+6),1.6,BLU); d.tx(TX(22.5)+4,TY(UD+3),'kablo',4.4,'start','',BLU)
d.dim(TX(0),TY(0)-12,TX(UW),TY(0)-12,'45'); d.dim(TX(UW)+14,TY(0),TX(UW)+14,TY(UD),'14')
d.tx(TX(22.5),TY(-5),'MÜŞTERİ',5.6,'middle','bold',GRY)
# --- notlar
d.box(800,420,370,310,'PARÇA · MALZEME')
yy=d.para(812,458,'GÖVDE: 2 mm 304 paslanmaz kutu 45×104×14, duvara 4 dübelle asılır, gizli güvenlik torx vidası; ön yüzde açık vida yok. Cam 6 mm temperli, IK10.',66,5.8)
yy=d.para(812,yy+2,'EKRAN 32" portre PCAP dokunmatik, 1080×1920, 500 nit. Mini PC i5/8 GB. Kablo (LAN + 220 V) duvar içinden, dışarıda kablo yok.',66,5.8)
yy=d.para(812,yy+2,'POS: ÖKC entegre (Ingenico Move 2500 / PAX A920 tipi) çelik yuvada 20° eğik, kablosu içeride; yalnız kart okuma yüzeyi dışarıda. FİŞ: 80 mm termal kiosk yazıcısı, kesici, rulo eleman servis kapağından (arka değil, alt kenar).',66,5.8)
yy=d.para(812,yy+2,'2D OKUYUCU: cam arkası modül (app QR, kupon). Kamera + hoparlör üstte. Yükseklik: ekran merkezi z 150, POS z 93–107, alt kenar z 85 (tekerlekli sandalye ≤ 120 ✓).',66,5.8)
d.para(812,yy+2,'Arkada gövde yok: ekranın arkası 14 cm, tamamı parçalarla dolu. Altındaki duvar (z 0–85) boş, başka kullanım için serbest.',66,5.8,GRN,'bold')
d.tx(d.W-30,d.H-8,'AUTOKITCH · arastirma/6_PICKUP/siparis_ekrani_teknik_v2 · 7 Eyl 2026',6.5,'end','',GRY)
d.save('siparis_ekrani_teknik_v2')

# ======================================================= 2 · TESLİM DOLABI =======================================================
d=D(1460,900); d.title('AUTOKITCH — TESLİM DOLABI (PICKUP) v2 · 124 × 165 × 52 · 12 dolap 2 × 6 · iç 56 × 36 × 16','ön kapı müşteri (yaylı gizli menteşe + amortisör = kendiliğinden kapanır, yaylı dil kendini kilitler) · arka klape robot · ısıtıcı yok, PU 20 mm · vandalizm: 2 mm 304, 10 mm bindirme, gizli menteşe · ölçüler cm')
CW,CH,CD=124.0,165.0,52.0; LP=(60.0,20.0); ZL0=40.0
# --- ön
d.box(30,80,470,720,'ÖN GÖRÜNÜŞ (müşteri)'); K=3.2; ox=90; oy=120+K*CH
X=lambda x: ox+K*x; Y=lambda z: oy-K*z
d.rc(X(0),Y(CH),K*CW,K*CH,1.6,3,'#111',None,STEEL); d.rc(X(0),Y(15),K*CW,K*15,1,0,'#555',None,'#9e9e9e'); d.tx(X(62),Y(6)+2,'plint 15',5,'middle','','#fff')
d.rc(X(2),Y(40),K*120,K*25,1,0,'#666',None,'#e3f2fb'); d.tx(X(62),Y(26)+2,'PANO 25: BEYİN PC · 12 kilit kontrol kartı · 12 V PSU · router · servis kapağı önde (anahtarlı)',5.2,'middle','bold',BLU)
for r in range(6):
    for c in range(2):
        x0=2+c*60; z0=ZL0+r*20
        d.rc(X(x0+1),Y(z0+19),K*58,K*18,1,1,'#333',None,'#e6e8eb')
        for hz in (z0+3,z0+9.5,z0+16): d.rc(X(x0+1.2),Y(hz+1),K*1,K*2,.5,0,'#555',None,'#555')      # gizli menteşe izi
        d.rc(X(x0+53),Y(z0+13.5),K*2,K*8,.8,2,'#333',None,'#4a4f55')                                   # tutamak oyuğu
        d.rc(X(x0+4),Y(z0+17.5),K*10,K*0.8,.5,0,GRN,None,'#9fe2b8')                                     # LED
        d.tx(X(x0+30),Y(z0+8.5)+2,'%d'%(r*2+c+1),7,'middle','bold','#333')
d.dim(X(0),Y(CH)-12,X(CW),Y(CH)-12,'124 = 2 + 60 + 60 + 2'); d.dim(X(CW)+14,Y(0),X(CW)+14,Y(CH),'165')
d.dim(X(CW)+30,Y(ZL0),X(CW)+30,Y(ZL0+120),'6 × 20 = 120',5.2,GRY); d.dim(X(CW)+30,Y(15),X(CW)+30,Y(40),'25',5.2,GRY)
d.tx(X(-5),Y(ZL0)+2,'z 40',5.4,'end','bold',GRY); d.tx(X(-5),Y(160)+2,'z 160',5.4,'end','bold',GRY)
d.para(42,770,'Kapı 58×18, 2 mm 304 paslanmaz; sol kenarda 3 gizli yaylı menteşe (izleri), sağda tutamak oyuğu (çıkıntı yok), üstte LED şerit. Kenar kasanın içine 10 mm biner (levye giremez), ön yüzde vida ve menteşe görünmez, cam yok. Numaralar lazer.',110,5.6)
# --- yan kesit
d.box(520,80,420,720,'YAN KESİT (bir sütun)'); sx=640; sy=oy
SX=lambda yd: sx+K*yd; SY=lambda z: sy-K*z      # yd: müşteri (0) → robot (52)
d.rc(SX(0),SY(CH),K*CD,K*CH,1.6,2,'#111',None,STEEL); d.rc(SX(0),SY(15),K*CD,K*15,1,0,'#555',None,'#9e9e9e')
d.rc(SX(2),SY(40),K*48,K*25,1,0,'#666',None,'#e3f2fb'); d.tx(SX(26),SY(27)+2,'PANO',5,'middle','bold',BLU)
for r in range(6):
    z0=ZL0+r*20
    d.hatch(SX(4),SY(z0+20),K*40,K*2,3,'#b08968',PU); d.hatch(SX(4),SY(z0+2),K*40,K*2,3,'#b08968',PU)
    d.rc(SX(4),SY(z0+18),K*40,K*16,.9,0,'#333',None,'#fff')
    d.rc(SX(2),SY(z0+19),K*2,K*18,1,0,'#111',None,'#cfd3d8')                                            # ön kapı 2
    d.rc(SX(3.2),SY(z0+11),K*1.6,K*3,.8,0,'#111',None,'#111')                                            # yaylı dil + elektrikli kilit
    d.rc(SX(4),SY(z0+17.5),K*6,K*1.2,.6,0,'#333',None,'#999')                                            # amortisör (kapak üst kenarı)
    d.ln(SX(44),SY(z0+18),SX(38),SY(z0+9),1.4,GRN); d.ln(SX(44),SY(z0+18),SX(44),SY(z0+2),.9,GRN,'3,2'); d.ci(SX(44),SY(z0+18),1.4,1,GRN,None,GRN)   # arka klape
    d.ci(SX(42.5),SY(z0+16),1,.7,RED,None,RED)                                                           # IR
    for yy_ in (36,39,42): d.ci(SX(yy_),SY(z0+18.6),.8,.5,'#555',None,'#fff')                            # buhar delikleri
    d.rc(SX(4),SY(z0+2.5),K*40,K*0.5,.6,0,'#333',None,'#bbb')                                            # çıkarılabilir taban tepsisi
d.rc(SX(50),SY(CH),K*2,K*150,1,0,'#333',None,'#8a8f95')                                                  # arka çerçeve
d.tx(SX(-3),SY(100)+2,'MÜŞTERİ',5.6,'end','bold',GRY); d.tx(SX(CD)+4,SY(100)+2,'ROBOT',5.6,'start','bold',GRY)
d.dim(SX(0),SY(CH)-12,SX(CD),SY(CH)-12,'52 = kapı 2 + PU 2 + iç 36 + klape 8 + çerçeve 2 + pay 2')
d.dim(SX(CD)+16,SY(ZL0+100),SX(CD)+16,SY(ZL0+120),'20',5.2,GRY); d.dim(SX(CD)+30,SY(ZL0+102),SX(CD)+30,SY(ZL0+118),'iç 16',5.2,GRY)
z=ZL0+60
d.lead(SX(3),SY(z+19.5),SX(-10),SY(z+30)+4,'ön kapı 2 mm 304 · gizli yaylı menteşe',5,'#333','end')
d.lead(SX(4),SY(z+12.5),SX(-10),SY(z+24)+4,'elektrikli kilit + yaylı dil (5 kN)',5,'#333','end')
d.lead(SX(7),SY(z+18),SX(-10),SY(z+37)+4,'amortisör (soft-close 3 sn)',5,'#333','end')
d.lead(SX(41),SY(z+13),SX(56),SY(z+33)+4,'arka klape: üst menteşe, içeri açılır, yay + mıknatıs kilit',5,GRN,'start')
d.lead(SX(42.5),SY(z+16),SX(56),SY(z+27)+4,'IR sensör "kutu var"',5,RED,'start')
d.lead(SX(39),SY(z+18.6),SX(56),SY(z+39)+4,'buhar delikleri Ø8 ×3',5,'#555','start')
d.lead(SX(24),SY(z+2.8),SX(56),SY(z-8)+4,'çıkarılabilir taban tepsisi (yıkanır)',5,'#555','start')
d.lead(SX(24),SY(z+21),SX(56),SY(z-2)+4,'PU 20 mm (alt/üst/yan) — ısıtıcı yok',5,'#7a5c2e','start')
d.para(532,770,'Kapı bırakılınca amortisörlü yay 3 sn içinde kapatır; dil yaylı olduğu için kapı çarpınca kendi kilitlenir, kurye kapatmasa da olur. Kapı 20 sn açık kalırsa reed sensör → ekranda uyarı + buzzer; 60 sn → BEYİN dolabı "açık" işaretler, robot yüklemez. Ön kapı ile arka klape kilitleri karşılıklı (interlock).',96,5.6)
# --- üst
d.box(960,80,470,420,'ÜST GÖRÜNÜŞ (bir sıra, kapaklar kapalı)'); tx0=1010; ty0=130; KT=3.0
TX=lambda x: tx0+KT*x; TY=lambda yd: ty0+KT*yd
d.rc(TX(0),TY(0),KT*CW,KT*CD,1.6,2,'#111',None,STEEL)
for c in range(2):
    x0=2+c*60
    d.rc(TX(x0),TY(0),KT*60,KT*2,1,0,'#111',None,'#cfd3d8')                                              # kapı
    d.rc(TX(x0+1),TY(2),KT*58,KT*2,.5,0,'#b08968',None,PU)                                                # PU
    d.rc(TX(x0+2),TY(4),KT*56,KT*36,1,0,'#333',None,'#fff')                                               # iç 56×36
    d.ln(TX(x0+22),TY(5),TX(x0+22),TY(39),.8,'#999','3,2')                                               # bölme 20 | 36
    d.rc(TX(x0+3.5),TY(6),KT*8.5,KT*27,.8,3,BLU,'3,2','none'); d.rc(TX(x0+12.5),TY(8),KT*9,KT*13,.8,1,AMB,'3,2','none')
    d.rc(TX(x0+23.5),TY(5.5),KT*32.4,KT*32.4,.9,1,'#5a3d13','3,2','none'); d.tx(TX(x0+39.7),TY(22),'kutu 32×32',5,'middle','','#5a3d13')
    d.tx(TX(x0+7.7),TY(21),'1 L',4.6,'middle','',BLU); d.tx(TX(x0+17),TY(15.5),'tatlı',4.6,'middle','',AMB)
    d.rc(TX(x0+2),TY(40),KT*56,KT*8,.6,0,'#333',None,'#f4f4f4'); d.ln(TX(x0+4),TY(40),TX(x0+56),TY(40),1.4,GRN)   # klape zonu
    d.tx(TX(x0+30),TY(45),'arka klape zonu 8',4.8,'middle','',GRN)
    d.rc(TX(x0+2),TY(48),KT*56,KT*2,.6,0,'#333',None,'#8a8f95')                                           # arka çerçeve
    for hz in (x0+0.8,): d.ci(TX(hz),TY(1),1.2,.6,'#555',None,'#555')                                    # menteşe (sol)
    d.rc(TX(x0+55),TY(0.2),KT*2.5,KT*1.6,.6,0,'#111',None,'#111')                                        # kilit dili (sağ)
    d.ci(TX(x0+56.5),TY(6),1,.6,RED,None,RED)
d.tx(TX(62),TY(-8),'MÜŞTERİ',5.6,'middle','bold',GRY); d.tx(TX(62),TY(CD)+12,'ROBOT (koridor)',5.6,'middle','bold',GRY)
d.dim(TX(0),TY(0)-16,TX(CW),TY(0)-16,'124'); d.dim(TX(CW)+14,TY(0),TX(CW)+14,TY(CD),'52')
d.dim(TX(2)+0,TY(CD)+4,TX(24),TY(CD)+4,'20',5,GRY); d.dim(TX(24),TY(CD)+4,TX(60),TY(CD)+4,'36',5,GRY)
d.lead(TX(2.8),TY(1),TX(-6),TY(-4)+0,'menteşe sol',5,'#333','end'); d.lead(TX(58),TY(1),TX(78),TY(-4),'kilit sağ',5,'#333','start')
# --- parça
d.box(960,520,470,280,'PARÇA · VANDALİZM')
yy=d.para(972,558,'KASA: 2 mm 304 paslanmaz, duvar açıklığına gömülü, dış yüzde vida yok (güvenlik torx içeriden). Kapı 58×18×2, gizli yaylı menteşe ×3 (dışarıdan sökülmez), kasa içine 10 mm bindirme kenarı, tutamak oyuk (çıkıntı yok, kırılacak parça yok). Cam yok.',82,5.6)
yy=d.para(972,yy+2,'KİLİT: 12 V elektrikli dil (fail-secure, 5 kN çekme), yaylı dil = kapı itilince kendi kilitlenir; reed sensör kapı; enerji kesilince kilitli kalır, eleman anahtarla açar (pano). Arka klape: mıknatıs kilit 12 V, sadece BEYİN açar.',82,5.6)
yy=d.para(972,yy+2,'İÇ: PU 20 mm alt/üst/yan, paslanmaz iç kabuk, çıkarılabilir taban tepsisi, IR sensör, Ø8 buhar deliği ×3 arka üst, LED şerit kapı üstü. Isıtıcı yok.',82,5.6)
d.para(972,yy+2,'KAMERA kod ünitesinde (ayrı resim); her açılış kayıt. Dolap boyu 165: plint 15 + pano 25 + 6 × 20 + üst 5; gereksiz boşluk yok.',82,5.6,GRN,'bold')
d.tx(d.W-30,d.H-8,'AUTOKITCH · arastirma/6_PICKUP/teslim_dolabi_teknik_v2 · 7 Eyl 2026',6.5,'end','',GRY)
d.save('teslim_dolabi_teknik_v2')

# ======================================================= 3 · KOD ÜNİTESİ =======================================================
d=D(1100,640); d.title('AUTOKITCH — KOD ÜNİTESİ (dolap açma) v1 · duvar tipi 20 × 34 × 8 · zeminden 110–144','7" ekran + metal PIN pad + 2D okuyucu + kamera · yalnız kod girişi (müşteri PIN / QR, kurye sipariş no son 4 hane) · dolabın yanına, sağ · vandal: IK10 cam, IK09 metal tuş, IP65 · ölçüler cm')
UW,UH,UD,Z0=20.0,34.0,8.0,110.0
d.box(30,80,330,540,'ÖN GÖRÜNÜŞ'); K=9; ox=110; oy=110+K*UH
X=lambda x: ox+K*x; Y=lambda y: oy-K*y
d.rc(X(0),Y(UH),K*UW,K*UH,1.6,3,'#111',None,STEEL)
d.rc(X(1),Y(33),K*18,K*1,.6,0,GRN,None,'#9fe2b8'); d.tx(X(10),Y(33.5)+1.5,'LED şerit (yeşil: sizin dolabınız · kırmızı: hata)',3.6,'middle','','#1d7a4f')
d.rc(X(2.2),Y(31.5),K*15.6,K*9.5,1.2,2,'#111',None,DARK); d.tx(X(10),Y(27.5)+2,'7" ekran',5.4,'middle','bold','#fff'); d.tx(X(10),Y(24.5)+2,'"Kodunuzu girin" · dolap no',4,'middle','','#ddd')
d.ci(X(18),Y(32.6),1.6,.8,'#333',None,'#333'); d.tx(X(16.5),Y(32.6)+1.5,'kamera',3.6,'end','','#333')
for r in range(4):
    for c in range(3):
        d.rc(X(4.5+c*3.8),Y(20.3-r*3.6),K*3.2,K*3.0,.9,2,'#333',None,'#b8bec5'); d.tx(X(6.1+c*3.8),Y(18.5-r*3.6)+2,str([1,2,3,4,5,6,7,8,9,'←',0,'✓'][r*3+c]),5,'middle','bold','#111')
d.tx(X(10),Y(6.2)+2,'metal PIN pad 4×3 (IK09, IP65)',4,'middle','','#333')
d.rc(X(7),Y(4.8),K*6,K*3,1,1,'#333',None,'#9aa0a6'); d.tx(X(10),Y(3.2)+1.5,'2D okuyucu',3.8,'middle','','#fff')
d.rc(X(16),Y(4.8),K*3,K*3,.8,1,'#333',None,'#bbb'); d.tx(X(17.5),Y(1)+1,'KURYE',3.2,'middle','bold','#333')
d.dim(X(0),Y(UH)-12,X(UW),Y(UH)-12,'20'); d.dim(X(UW)+14,Y(UH),X(UW)+14,Y(0),'34')
d.tx(X(-5),Y(0)+2,'z 110',5.4,'end','bold',GRY); d.tx(X(-5),Y(UH)+2,'z 144',5.4,'end','bold',GRY)
# yan
d.box(380,80,300,540,'YAN GÖRÜNÜŞ (kesit)'); sx=470; sy=oy
SX=lambda x: sx+K*x; SY=lambda y: sy-K*y
d.hatch(SX(UD),SY(UH+4),K*4,K*(UH+8),4,'#b08968','#efe4d4'); d.txr(SX(UD+2),SY(UH/2),'DUVAR',6,'#7a5c2e','bold')
d.rc(SX(0),SY(UH),K*UD,K*UH,1.6,2,'#111',None,STEEL)
d.rc(SX(0),SY(31.5),K*0.6,K*9.5,.8,0,'#333',None,GLASS); d.rc(SX(0.6),SY(31.5),K*1.4,K*9.5,.8,0,'#333',None,DARK)
d.rc(SX(0),SY(21),K*1.2,K*15,.8,0,'#333',None,'#b8bec5'); d.tx(SX(3.2),SY(14)+2,'tuş',4,'start','','#333')
d.rc(SX(0.6),SY(4.8),K*3,K*3,.8,0,'#333',None,'#9aa0a6')
d.rc(SX(3),SY(26),K*3,K*10,1,1,'#333',None,'#eee'); d.tx(SX(4.5),SY(21)+2,'kontrolcü',3.8,'middle','bold'); d.tx(SX(4.5),SY(18.5)+2,'(RPi tipi)',3.4,'middle','','#333')
d.rc(SX(4),SY(12),K*2.5,K*4,.8,1,'#333',None,'#eee'); d.tx(SX(5.2),SY(9.5)+2,'PSU',3.6,'middle','','#333')
d.ln(SX(UD),SY(17),SX(UD+4),SY(17),1.6,BLU); d.tx(SX(UD+2),SY(14)+2,'LAN + 12 V',4,'middle','',BLU)
d.dim(SX(0),SY(UH)-12,SX(UD),SY(UH)-12,'8'); d.tx(SX(-2),SY(17)+2,'MÜŞTERİ',5.2,'end','bold',GRY)
# üst
d.box(700,80,370,240,'ÜST GÖRÜNÜŞ'); tx0=780; ty0=150
TX=lambda x: tx0+K*x; TY=lambda yd: ty0+K*yd
d.hatch(TX(0),TY(UD),K*UW,K*4,4,'#b08968','#efe4d4'); d.tx(TX(10),TY(UD+2.8),'DUVAR',5.6,'middle','bold','#7a5c2e')
d.rc(TX(0),TY(0),K*UW,K*UD,1.6,2,'#111',None,STEEL); d.rc(TX(2.2),TY(0),K*15.6,K*0.6,.6,0,'#333',None,GLASS); d.rc(TX(2.2),TY(0.6),K*15.6,K*1.4,.6,0,'#333',None,DARK)
d.rc(TX(6),TY(3),K*8,K*3,1,1,'#333',None,'#eee'); d.tx(TX(10),TY(4.9),'kontrolcü',4,'middle','')
d.ln(TX(10),TY(UD),TX(10),TY(UD+4),1.6,BLU)
d.dim(TX(0),TY(0)-12,TX(UW),TY(0)-12,'20'); d.dim(TX(UW)+14,TY(0),TX(UW)+14,TY(UD),'8'); d.tx(TX(10),TY(-22),'MÜŞTERİ',5.2,'middle','bold',GRY)
d.box(700,340,370,280,'PARÇA · VANDALİZM')
yy=d.para(712,378,'GÖVDE 2 mm 304 paslanmaz 20×34×8, duvara gömme ya da yüzeye, güvenlik torx; cam 6 mm temperli IK10; tuşlar paslanmaz IK09, IP65 (eldivenle basılır); 2D okuyucu cam arkasında; kamera geniş açı, her açılışta 10 sn kayıt.',60,5.6)
yy=d.para(712,yy+2,'KONTROLCÜ: RPi tipi, LAN ile BEYİN'+AP+'e; kilit kartı dolabın panosunda (bu kutuda kilit yok, sadece giriş). Enerji 12 V duvar içinden.',60,5.6)
d.para(712,yy+2,'YERLEŞİM: dolabın hemen sağında, ekran merkezi z 130, tuşlar z 115–126 (tekerlekli sandalye ✓). Sipariş ekranı ayrı birim (solda).',60,5.6,GRN,'bold')
d.tx(d.W-30,d.H-8,'AUTOKITCH · arastirma/6_PICKUP/kod_unitesi_teknik_v1 · 7 Eyl 2026',6.5,'end','',GRY)
d.save('kod_unitesi_teknik_v1')
