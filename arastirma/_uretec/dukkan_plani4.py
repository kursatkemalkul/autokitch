# -*- coding: utf-8 -*-
# DÜKKAN PLANI v4 (7 Eyl 2026) — Kemal: krokiyi 90° döndür, sokak cephesi AŞAĞI baksın, düzen aynı; TEK FİNAL RESİM (plan + sokak cephesi).
# Kroki (döndürülmüş): arka duvar boyunca HAT · önünde robot koridoru (sağ uçta öne kıvrılır, teslim dolabına) · ince duvar · ön zon: sol koridor + kapı, tezgah (sokağa bakar), SERVICE, sipariş ekranı, teslim dolabı sağ uçta.
import io, math, xml.dom.minidom
o=[]; W,H=1320,1000
def esc(t): return str(t).replace('&','&amp;').replace('<','&lt;')
def ln(x1,y1,x2,y2,w=1,c='#111',d=None): o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s stroke-linecap="round"/>'%(x1,y1,x2,y2,c,w,(' stroke-dasharray="%s"'%d) if d else ''))
def rc(x,y,w,h,sw=1,r=0,c='#111',d=None,f='none'): o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>'%(x,y,w,h,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def ci(x,y,r,sw=1,c='#111',d=None,f='none'): o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>'%(x,y,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def tx(x,y,t,fs=8,anc='middle',fw='',col='#111',rot=0): o.append('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="%s" font-weight="%s" fill="%s" font-family="Segoe UI, Arial, sans-serif"%s>%s</text>'%(x,y,fs,anc,fw or 'normal',col,(' transform="rotate(%s %.1f %.1f)"'%(rot,x,y)) if rot else '',esc(t)))
def path(d_,sw=1,c='#111',f='none',d=None): o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="%s"%s stroke-linecap="round"/>'%(d_,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def dim(x1,y1,x2,y2,t,fs=6.5,col='#111'):
    ln(x1,y1,x2,y2,.7,col)
    for (x,y) in ((x1,y1),(x2,y2)):
        if abs(y2-y1)<abs(x2-x1): ln(x,y-3,x,y+3,.7,col)
        else: ln(x-3,y,x+3,y,.7,col)
    if abs(y2-y1)<abs(x2-x1): tx((x1+x2)/2,y1-3,t,fs,'middle','bold',col)
    else: tx(x1-5,(y1+y2)/2,t,fs,'middle','bold',col,-90)
def hatch(x,y,w,h,step=4,c='#999',f='#eee'):
    rc(x,y,w,h,.6,0,c,None,f); k=0
    while k<w+h: ln(x+max(0,k-h),y+min(k,h),x+min(k,w),y+max(0,k-w),.4,c); k+=step
def para(x,y,t,maxc,fs=6.4,col='#333',fw=''):
    lh=fs*1.55; cur=''; lines=[]
    for wd in t.split(' '):
        if cur and len(cur)+1+len(wd)>maxc: lines.append(cur); cur=wd
        else: cur=(cur+' '+wd) if cur else wd
    if cur: lines.append(cur)
    for l in lines: tx(x,y,l,fs,'start',fw,col); y+=lh
    return y
def m2(v): return ('%.1f m²'%v).replace('.',',')
# ---------------- ölçüler (cm) — x soldan, y önden (0 = sokak) — KROKİ BİREBİR, 90° döndürülmüş ----------------
SW,SD=600.0,320.0
KORX=100.0; WALL=6.0; COR=90.0; LINE_D=84.0; FZ=140.0
YW0,YW1=FZ,FZ+WALL; YC0,YC1=YW1,YW1+COR; YL0,YL1=YC1,SD           # ön zon 0–140 · ince duvar 140–146 · robot 146–236 · hat 236–320
HX0=100.0; M=[('1 STORE',140),('2 PRESS',70),('3 TOPPING',70),('4 OVEN',70),('5 PACK',70)]
RY=(YC0+YC1)/2; RX0,RX1=130.0,570.0
WLX1=370.0                                                        # ince duvar x 100–370 (yalnız tezgah bölgesi)
SRV=(370.0,440.0,56.0,140.0)                                      # SERVICE 70×84, ince duvarın sağ ucunda
DOL=(470.0,594.0); DOL_D=52.0                                     # teslim dolabı sağda, ön duvar içinde; arkası açık robot alanına bakar
EKR=(380.0,425.0); KOD=(435.0,455.0); DOOR=(10.0,90.0); WIN=(120.0,280.0)
TEZ=(110.0,290.0); KDOOR=(40.0,120.0); RDOOR=(160.0,230.0)         # tezgah · koridor→ön zon kapısı · koridor→robot kapısı (x=100 duvarında)
K=1.0; ox=60; oy=90+K*SD
X=lambda x: ox+K*x; Y=lambda y: oy-K*y
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,32,'AUTOKITCH — DÜKKAN v4 · PLAN + SOKAK CEPHESİ · kroki birebir (90° döndürüldü, sokak aşağıda) · al-git · iç %d × %d = %s · ölçüler cm'%(SW,SD,m2(SW*SD/1e4)),13,'start','bold')
tx(30,50,'arka duvarda HAT · önünde robot koridoru · ince duvar yalnız tezgah bölgesinde · sağda koridor dolabın arkasına kadar iner · SERVICE arada · sipariş ekranı SERVICE önünde, yanında teslim dolabı · sol şerit koridor + sokak kapısı',8.5,'start','','#444')
ln(30,60,W-30,60,.8,'#999')
tx(X(-30),Y(SD)-12,'PLAN (üstten)',9.5,'start','bold')
rc(X(-40),Y(0),K*(SW+80),K*70,0,0,'none',None,'#f0efe9'); tx(X(SW/2),Y(0)+64,'KALDIRIM / SOKAK — müşteri burada durur',7,'middle','bold','#888')
rc(X(0)-10,Y(SD)-10,K*SW+20,K*SD+20,0,0,'none',None,'#bfbfbf'); rc(X(0),Y(SD),K*SW,K*SD,1.6,0,'#111',None,'#fff')
# zonlar
rc(X(KORX),Y(YC1),K*(SW-KORX),K*COR,.6,0,'#7fb3d5',None,'#eef6fb')                          # robot koridoru
rc(X(SRV[1]),Y(YC0),K*(SW-SRV[1]),K*(YC0-DOL_D),.6,0,'#7fb3d5',None,'#eef6fb')                # sağda koridor öne iner (dolap arkasına)
rc(X(KORX),Y(YW0),K*(WLX1-KORX),K*FZ,.5,0,'#ccc',None,'#f4f4f4')                              # ön zon (tezgah + eleman)
rc(X(0),Y(SD),K*KORX,K*SD,.5,0,'#ccc',None,'#faf7ee')                                         # sol koridor
rc(X(SRV[1]),Y(DOL_D),K*(DOL[0]-SRV[1]),K*DOL_D,.5,0,'#999',None,'#ddd')                      # dolap solu dolu duvar
# hat
xx=HX0
for nm,w in M:
    rc(X(xx),Y(YL1),K*w,K*LINE_D,1.2,2,'#111',None,'#e4e6ea'); tx(X(xx+w/2),Y((YL0+YL1)/2)+3,nm,7,'middle','bold'); xx+=w
tx(X(560),Y((YL0+YL1)/2)+3,'boş 80',5.6,'middle','','#999')
# ray + robot (düz)
ln(X(RX0),Y(RY-4),X(RX1),Y(RY-4),1.6,'#333'); ln(X(RX0),Y(RY+4),X(RX1),Y(RY+4),1.6,'#333')
for xr in range(int(RX0),int(RX1)+1,50): ln(X(xr),Y(RY-4),X(xr),Y(RY+4),.6,'#333')
rc(X(300-20),Y(RY+20),K*40,K*40,1.2,3,'#111',None,'#fff'); ci(X(300),Y(RY),K*13,1.4,'#111',None,'#fff'); tx(X(300),Y(RY)+3,'ROBOT',5.6,'middle','bold')
ci(X(532),Y(RY),K*150,.7,'#1a49b8','4,3','none'); ci(X(532),Y(RY),K*6,1,'#1a49b8','3,2','#eef6fb')
tx(X(250),Y(YC1-10)+3,'ROBOT KORİDORU 90 · RAY %d düz (x %d–%d)'%(RX1-RX0,RX0,RX1),6.2,'middle','bold','#1a49b8')
tx(X(532),Y(RY+22)+3,'ray ucu: dolap arkası %d cm önde → kol ≥ 150 (H2017 170)'%(RY-DOL_D),5,'middle','','#1a49b8')
# ince duvar (yalnız tezgah bölgesi) + kapılar (x=100 duvarı)
hatch(X(KORX),Y(YW1),K*(WLX1-KORX),K*WALL,3,'#b08968','#efe4d4'); tx(X(235),Y(YW0+3)+2,'İNCE DUVAR 6 (2 sac + yalıtım) · x 100–370',5.2,'middle','bold','#7a5c2e')
ln(X(KORX),Y(SD),X(KORX),Y(RDOOR[1]),1.4); ln(X(KORX),Y(RDOOR[0]),X(KORX),Y(KDOOR[1]),1.4); ln(X(KORX),Y(KDOOR[0]),X(KORX),Y(0),1.4)
ln(X(KORX),Y(RDOOR[0]),X(KORX)+K*70,Y(RDOOR[0]),1.1); path('M %.1f %.1f A %.1f %.1f 0 0 0 %.1f %.1f'%(X(KORX)+K*70,Y(RDOOR[0]),K*70,K*70,X(KORX),Y(RDOOR[1])),.8,'#333','none','3,3'); tx(X(KORX)+K*40,Y(RDOOR[1]+8)+3,'robot kapısı 70 (kilitli)',4.8,'middle','','#c0392b')
ln(X(KORX),Y(KDOOR[0]),X(KORX)+K*80,Y(KDOOR[0]),1.1); path('M %.1f %.1f A %.1f %.1f 0 0 0 %.1f %.1f'%(X(KORX)+K*80,Y(KDOOR[0]),K*80,K*80,X(KORX),Y(KDOOR[1])),.8,'#333','none','3,3'); tx(X(KORX)+K*45,Y(KDOOR[1]+8)+3,'ön zon kapısı 80',4.8,'middle','','#555')
tx(X(50),Y(200)+3,'KORİDOR 100',6.5,'middle','bold','#555',-90)
# SERVICE
rc(X(SRV[0]),Y(SRV[3]),K*(SRV[1]-SRV[0]),K*(SRV[3]-SRV[2]),1.2,2,'#111',None,'#e4e6ea'); tx(X(405),Y(100)+3,'7 SERVICE',6.2,'middle','bold'); tx(X(405),Y(88)+3,'70 × 84',5.4,'middle','','#555')
ln(X(SRV[0]),Y(SRV[2]+12),X(SRV[0]),Y(SRV[2]+62),1.2); tx(X(SRV[0])-4,Y(SRV[2]+37)+3,'kapı',4.8,'end','','#555')
# tezgah + eleman
rc(X(TEZ[0]),Y(40),K*(TEZ[1]-TEZ[0]),K*40,1.2,2,'#111',None,'#f3e6d3'); tx(X(200),Y(20)+3,'TEZGAH 180 × 40 — sokağa bakar',6,'middle','bold')
ci(X(200),Y(75),K*18,1.2,'#111',None,'#fff'); tx(X(200),Y(75)+3,'eleman',5.4,'middle','')
tx(X(330),Y(90)+3,'eleman alanı',5,'middle','','#888')
# teslim dolabı
rc(X(DOL[0]),Y(DOL_D),K*(DOL[1]-DOL[0]),K*DOL_D,1.4,1,'#111',None,'#dfe1e4'); tx(X(532),Y(30)+3,'TESLİM DOLABI 124 × 52',6.2,'middle','bold'); tx(X(532),Y(16)+3,'12 dolap · ön duvar içinde',5,'middle','','#555')
ln(X(DOL[0]),Y(DOL_D),X(DOL[1]),Y(DOL_D),1.6,'#1d7a4f'); tx(X(532),Y(DOL_D)-4,'robot klapeleri (arka yüz, açık robot alanına bakar)',5,'middle','','#1d7a4f')
# ön duvar açıklıkları
FW=Y(0)
rc(X(DOOR[0]),FW-2,K*(DOOR[1]-DOOR[0]),5,0,0,'none',None,'#fff'); ln(X(DOOR[0]),FW,X(DOOR[0]),FW-K*80,1.2); path('M %.1f %.1f A %.1f %.1f 0 0 1 %.1f %.1f'%(X(DOOR[0]),FW-K*80,K*80,K*80,X(DOOR[1]),FW),.8,'#333','none','3,3')
tx(X(50),FW+14,'KAPI 80',5.6,'middle','bold','#333'); tx(X(50),FW+22,'eleman · kurye · ikmal',4.6,'middle','','#555')
rc(X(WIN[0]),FW-3,K*(WIN[1]-WIN[0]),6,1,0,'#1a49b8',None,'#dbeeff'); tx(X(200),FW+14,'TEZGAH PENCERESİ 160',5.6,'middle','bold','#1a49b8'); tx(X(200),FW+22,'sürme cam',4.6,'middle','','#1a49b8')
rc(X(EKR[0]),FW,K*(EKR[1]-EKR[0]),K*14,1,0,'#111',None,'#2b2e33'); tx(X(402),FW+22,'SİPARİŞ EKRANI 45',5.4,'middle','bold'); tx(X(402),FW+30,'SERVICE önünde, dışa asılı',4.6,'middle','','#555')
rc(X(KOD[0]),FW,K*(KOD[1]-KOD[0]),K*8,1,0,'#111',None,'#b8bec5'); tx(X(445),FW+14,'KOD 20',5.4,'middle','bold')
for (xx_,lab,c) in ((200,'tezgah','#333'),(402,'sipariş','#1a49b8'),(532,'teslim','#1d7a4f')): ci(X(xx_),FW+K*48,K*12,1,c,'3,2','none'); tx(X(xx_),FW+K*48+3,lab,4.4,'middle','',c)
# ölçü zincirleri
yb=FW+80
dim(X(0),yb,X(KORX),yb,'koridor 100'); dim(X(KORX),yb,X(520),yb,'HAT 420'); dim(X(520),yb,X(SW),yb,'80'); dim(X(0),yb+18,X(SW),yb+18,'%d'%SW,7)
for (a,b,t) in ((DOOR[0],DOOR[1],'80'),(WIN[0],WIN[1],'160'),(EKR[0],EKR[1],'45'),(KOD[0],KOD[1],'20'),(DOL[0],DOL[1],'124')): dim(X(a),FW+40,X(b),FW+40,t,5.4,'#666')
xr=X(SW)+30
dim(xr,Y(SD),xr,Y(YL0),'hat 84'); dim(xr,Y(YL0),xr,Y(YC0),'robot 90'); dim(xr,Y(YC0),xr,Y(DOL_D),'robot alanı 94'); dim(xr,Y(DOL_D),xr,Y(0),'dolap 52')
xl=X(0)-30
dim(xl,Y(SD),xl,Y(YC0),'174'); dim(xl,Y(YC0),xl,Y(YW0),'6'); dim(xl,Y(YW0),xl,Y(0),'ön zon 140'); dim(X(0)-52,Y(SD),X(0)-52,Y(0),'%d'%SD,7)
tx(X(SW/2),Y(SD)-12,'ARKA DUVAR',7,'middle','bold','#888')
# ================= SOKAK CEPHESİ (önden) =================
FY=Y(0)+120+K*300; KF=K
FX=lambda x: ox+KF*x; FZ_=lambda z: FY-KF*z
tx(X(-30),FZ_(300)-12,'SOKAK CEPHESİ (önden, kaldırımdan bakış) · duvar boyu 300',9.5,'start','bold')
rc(FX(0),FZ_(300),KF*SW,KF*300,1.6,0,'#111',None,'#dcdcd8')
ln(FX(-40),FZ_(0),FX(SW+40),FZ_(0),2)
rc(FX(DOOR[0]),FZ_(210),KF*80,KF*210,1.2,1,'#111',None,'#eceef1'); tx(FX(50),FZ_(105)+3,'KAPI 80×210',6,'middle','bold'); rc(FX(80),FZ_(105),3,14,0,1,'none',None,'#444')
rc(FX(WIN[0]),FZ_(200),KF*160,KF*100,1.2,1,'#1a49b8',None,'#dbeeff'); tx(FX(200),FZ_(150)+3,'TEZGAH PENCERESİ 160×100',6,'middle','bold','#1a49b8'); tx(FX(200),FZ_(136)+3,'sürme cam · eşik z 100',4.8,'middle','','#1a49b8'); ln(FX(200),FZ_(200),FX(200),FZ_(100),.8,'#1a49b8')
rc(FX(EKR[0]),FZ_(189),KF*45,KF*104,1.2,1,'#111',None,'#2b2e33'); rc(FX(382.5),FZ_(186),KF*40,KF*71,.8,1,'#666',None,'#111'); tx(FX(402.5),FZ_(150)+3,'32"',6,'middle','bold','#fff'); tx(FX(402.5),FZ_(78)+3,'SİPARİŞ EKRANI',5.4,'middle','bold'); tx(FX(402.5),FZ_(70)+3,'z 85–189',4.8,'middle','','#555')
rc(FX(KOD[0]),FZ_(144),KF*20,KF*34,1.2,1,'#111',None,'#b8bec5'); tx(FX(445),FZ_(102)+3,'KOD',5.4,'middle','bold'); tx(FX(445),FZ_(94)+3,'z 110–144',4.6,'middle','','#555')
rc(FX(DOL[0]),FZ_(165),KF*124,KF*165,1.4,1,'#111',None,'#dfe1e4')
for r in range(6):
    for c in range(2):
        x0=DOL[0]+2+c*60; z0=40+r*20; rc(FX(x0),FZ_(z0+19),KF*58,KF*18,.7,1,'#666',None,'#eceef1'); rc(FX(x0+53),FZ_(z0+13),KF*2,KF*8,.6,1,'#444',None,'#444')
rc(FX(DOL[0]+2),FZ_(40),KF*120,KF*25,.7,0,'#666',None,'#e3f2fb'); tx(FX(532),FZ_(26)+3,'pano (servis kapağı)',5,'middle','','#1a49b8')
tx(FX(532),FZ_(178)+3,'TESLİM DOLABI 124×165 · 12 dolap',6,'middle','bold')
dim(FX(SW)+30,FZ_(0),FX(SW)+30,FZ_(300),'300'); dim(FX(SW)+48,FZ_(0),FX(SW)+48,FZ_(165),'165',5.6,'#666')
for (a,b,t) in ((DOOR[0],DOOR[1],'80'),(WIN[0],WIN[1],'160'),(EKR[0],EKR[1],'45'),(KOD[0],KOD[1],'20'),(DOL[0],DOL[1],'124')): dim(FX(a),FZ_(0)+22,FX(b),FZ_(0)+22,t,5.4,'#666')
dim(FX(0),FZ_(0)+40,FX(SW),FZ_(0)+40,'%d'%SW,7)
# ================= alan tablosu =================
bx=X(SW)+80; by=Y(SD)
rc(bx,by,290,290,1.2,4,'#111',None,'#fff'); tx(bx+12,by+18,'ALANLAR',9.5,'start','bold')
rows=[('hat kabinleri',LINE_D*420/1e4),('robot koridoru + sağ ön alan',(COR*(SW-KORX)+(SW-SRV[1])*(YC0-DOL_D))/1e4),('ince duvar',WALL*(WLX1-KORX)/1e4),('teslim dolabı (ön duvar içi)',124*DOL_D/1e4),('ön zon: tezgah + eleman',FZ*(WLX1-KORX)/1e4),('SERVICE',70*84/1e4),('sol koridor',KORX*SD/1e4),('hat yanı boş 80',80*LINE_D/1e4)]
yy=by+40
for a_,v in rows: tx(bx+12,yy,a_,6.2,'start','','#333'); tx(bx+278,yy,m2(v),6.4,'end','bold'); yy+=13
ln(bx+12,yy-5,bx+278,yy-5,.6,'#999'); tx(bx+12,yy+7,'TOPLAM İÇ',6.8,'start','bold'); tx(bx+278,yy+7,m2(SW*SD/1e4),6.8,'end','bold')
yy=para(bx+12,yy+26,'Ray düz 440 (x 130–570). Sağ tarafta ince duvar yok: koridor dolabın arkasına kadar iner, robot ray ucundan dolap arkasına %d cm uzanır → kol menzili en az 150 (H2017 170; CRX-20iA/L 142 sınırda).'%(RY-DOL_D),54,6,'#333')
para(bx+12,yy+2,'Sol koridor 100: sokak kapısından ön zon kapısına (80) ve kilitli robot kapısına (70). Müşteri kaldırımda: tezgah penceresi · sipariş ekranı (SERVICE önünde) · kod · teslim dolabı.',54,6,'#333')
tx(W-30,H-8,'AUTOKITCH · arastirma/FULL_MAKINE/dukkan_plani_v4 · 7 Eyl 2026',6.5,'end','','#666')
svg='<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'%(W,H,W,H)+chr(10).join(o)+'</svg>'
xml.dom.minidom.parseString(svg.encode('utf-8'))
out=r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\FULL_MAKINE\dukkan_plani_v4.svg"; io.open(out,'w',encoding='utf-8').write(svg); print('ok')
