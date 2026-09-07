# -*- coding: utf-8 -*-
# DÜKKAN PLANI v3 (7 Eyl 2026) — Kemal: krokiyi 90° döndür, sokak cephesi AŞAĞI baksın, düzen aynı; TEK FİNAL RESİM (plan + sokak cephesi).
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
# ---------------- ölçüler (cm) — x soldan, y önden (0 = sokak) ----------------
SW,SD=560.0,320.0
FZ=140.0; WALL=6.0; COR=90.0; LINE_D=84.0                        # ön zon 0–140 · ince duvar 140–146 · robot 146–236 · hat 236–320
YW0,YW1=FZ,FZ+WALL; YC0,YC1=YW1,YW1+COR; YL0,YL1=YC1,SD
KORX=100.0                                                       # sol koridor 0–100
HX0=100.0                                                        # hat x 100–520
M=[('1 STORE',140),('2 PRESS',70),('3 TOPPING',70),('4 OVEN',70),('5 PACK',70)]
RY=(YC0+YC1)/2                                                   # ray ekseni y 191
LEG_X=498.0; LEG_Y0=100.0; LEGW0=436.0; WLX=430.0                 # sağ bacak: x 436–560 (dolap genişliği), ray x 498, y 100'e iner; bacak duvarı x 430–436
DOL=(436.0,560.0); DOL_D=52.0
EKR=(300.0,345.0); KOD=(405.0,425.0); DOOR=(5.0,95.0); WIN=(110.0,190.0)
SRV=(200.0,284.0,56.0,140.0)
WDOOR=(10.0,90.0)
K=1.05; ox=60; oy=90+K*SD
X=lambda x: ox+K*x; Y=lambda y: oy-K*y
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,32,'AUTOKITCH — DÜKKAN v3 · PLAN + SOKAK CEPHESİ · al-git (müşteri içeri girmez) · iç %d × %d = %s · ölçüler cm'%(SW,SD,m2(SW*SD/1e4)),13,'start','bold')
tx(30,50,'kroki 90° döndürüldü, sokak cephesi aşağıda · arka duvarda HAT 420 · önünde robot koridoru 90 (sağ uçta öne kıvrılır) · ince duvar 6 · ön zon 140: sol koridor + kapı · tezgah sokağa bakar · SERVICE · sipariş ekranı · teslim dolabı sağ uçta',8.5,'start','','#444')
ln(30,60,W-30,60,.8,'#999')
tx(X(-30),Y(SD)-12,'PLAN (üstten)',9.5,'start','bold')
# kaldırım + dış duvar
rc(X(-40),Y(0),K*(SW+80),K*70,0,0,'none',None,'#f0efe9'); tx(X(SW/2),Y(0)+64,'KALDIRIM / SOKAK — müşteri burada durur',7,'middle','bold','#888')
rc(X(0)-10,Y(SD)-10,K*SW+20,K*SD+20,0,0,'none',None,'#bfbfbf'); rc(X(0),Y(SD),K*SW,K*SD,1.6,0,'#111',None,'#fff')
# zonlar
rc(X(0),Y(YC1),K*SW,K*COR,.6,0,'#7fb3d5',None,'#eef6fb')                                  # robot koridoru (arka)
rc(X(LEGW0),Y(YC0),K*(SW-LEGW0),K*(YC0-DOL_D),.6,0,'#7fb3d5',None,'#eef6fb')              # sağ bacak (dolaba iner)
rc(X(0),Y(YW0),K*WLX,K*FZ,.5,0,'#ccc',None,'#f4f4f4')                                     # ön zon (personel)
rc(X(0),Y(SD),K*KORX,K*(SD-YC1),.5,0,'#ccc',None,'#f4f4f4')                               # sol arka köşe (hat solu boş)
rc(X(520),Y(SD),K*40,K*(SD-YC1),.5,0,'#ccc',None,'#f4f4f4')
# hat (arka duvar)
xx=HX0
for nm,w in M:
    rc(X(xx),Y(YL1),K*w,K*LINE_D,1.2,2,'#111',None,'#e4e6ea'); tx(X(xx+w/2),Y((YL0+YL1)/2)+3,nm,7,'middle','bold'); xx+=w
tx(X(50),Y((YL0+YL1)/2)+3,'boş 100',6,'middle','','#999'); tx(X(540),Y((YL0+YL1)/2)+3,'boş 40',5.4,'middle','','#999')
# ray: düz + sağda 90° kavis + bacak
R=45.0; RX0,RX1=130.0,LEG_X-R
for off in (-4,4):
    path('M %.1f %.1f L %.1f %.1f A %.1f %.1f 0 0 1 %.1f %.1f L %.1f %.1f'%(X(RX0),Y(RY+off),X(RX1),Y(RY+off),K*(R-off),K*(R-off),X(LEG_X-off),Y(RY-R),X(LEG_X-off),Y(LEG_Y0)),1.6,'#333')
for xr in range(int(RX0),int(RX1)+1,50): ln(X(xr),Y(RY-4),X(xr),Y(RY+4),.6,'#333')
for yr in range(int(LEG_Y0),int(RY-R)+1,25): ln(X(LEG_X-4),Y(yr),X(LEG_X+4),Y(yr),.6,'#333')
rc(X(300-20),Y(RY+20),K*40,K*40,1.2,3,'#111',None,'#fff'); ci(X(300),Y(RY),K*13,1.4,'#111',None,'#fff'); tx(X(300),Y(RY)+3,'ROBOT',5.6,'middle','bold')
ci(X(LEG_X),Y(LEG_Y0),K*130,.7,'#1a49b8','4,3','none'); ci(X(LEG_X),Y(LEG_Y0),K*6,1,'#1a49b8','3,2','#eef6fb')
tx(X(200),Y(YC1-10)+3,'ROBOT KORİDORU 90 · RAY %d + kavis R 45 + bacak %d'%(RX1-RX0,RY-R-LEG_Y0),6.2,'middle','bold','#1a49b8')
tx(X(LEG_X)+K*60,Y(LEG_Y0-8),'kol menzili 130',5.2,'start','','#1a49b8')
# ince duvar: y 140–146, x 0–470 (sağda bacak açık); sol uçta kapı
hatch(X(WDOOR[1]),Y(YW1),K*(WLX-WDOOR[1]),K*WALL,3,'#b08968','#efe4d4'); hatch(X(0),Y(YW1),K*WDOOR[0],K*WALL,3,'#b08968','#efe4d4')
hatch(X(WLX),Y(YW1),K*WALL,K*(YW1-DOL_D),3,'#b08968','#efe4d4')                                       # bacağın sol duvarı (dikey)
ln(X(WDOOR[0]),Y(YW0),X(WDOOR[0]),Y(YW0-80),1.2); path('M %.1f %.1f A %.1f %.1f 0 0 0 %.1f %.1f'%(X(WDOOR[0]),Y(YW0-80),K*80,K*80,X(WDOOR[1]),Y(YW0)),.8,'#333','none','3,3')
tx(X(50),Y(YW0-90)+3,'KAPI 80 (kilitli, açılınca robot durur)',5,'middle','','#c0392b')
tx(X(250),Y(YW0+3)+2,'İNCE DUVAR 6 (2 sac + yalıtım)',5.2,'middle','bold','#7a5c2e')
tx(X(WLX+3),Y(100)+3,'ince duvar (bacak)',4.8,'middle','','#7a5c2e',-90)
# teslim dolabı sağ uçta, ön duvar içinde
rc(X(DOL[0]),Y(DOL_D),K*(DOL[1]-DOL[0]),K*DOL_D,1.4,1,'#111',None,'#dfe1e4'); tx(X(498),Y(30)+3,'TESLİM DOLABI 124 × 52',6.2,'middle','bold'); tx(X(498),Y(16)+3,'12 dolap · ön duvar içinde',5,'middle','','#555')
ln(X(DOL[0]),Y(DOL_D),X(DOL[1]),Y(DOL_D),1.6,'#1d7a4f'); tx(X(498),Y(DOL_D)-4,'robot klapeleri (arka yüz)',5,'middle','','#1d7a4f')
# ön duvar açıklıkları
FW=Y(0)
rc(X(DOOR[0]),FW-2,K*(DOOR[1]-DOOR[0]),5,0,0,'none',None,'#fff'); ln(X(DOOR[0]),FW,X(DOOR[0]),FW-K*90,1.2); path('M %.1f %.1f A %.1f %.1f 0 0 1 %.1f %.1f'%(X(DOOR[0]),FW-K*90,K*90,K*90,X(DOOR[1]),FW),.8,'#333','none','3,3')
tx(X(50),FW+14,'KAPI 90',5.6,'middle','bold','#333'); tx(X(50),FW+22,'eleman · kurye · ikmal',4.6,'middle','','#555')
rc(X(WIN[0]),FW-3,K*(WIN[1]-WIN[0]),6,1,0,'#1a49b8',None,'#dbeeff'); tx(X(150),FW+14,'PENCERE 80',5.6,'middle','bold','#1a49b8'); tx(X(150),FW+22,'sürme cam',4.6,'middle','','#1a49b8')
rc(X(WIN[0]),Y(40),K*(WIN[1]-WIN[0]),K*40,1.2,2,'#111',None,'#f3e6d3'); tx(X(150),Y(20)+3,'TEZGAH 80×40',6,'middle','bold')
ci(X(150),Y(72),K*18,1.2,'#111',None,'#fff'); tx(X(150),Y(72)+3,'eleman',5.4,'middle','')
rc(X(EKR[0]),FW,K*(EKR[1]-EKR[0]),K*14,1,0,'#111',None,'#2b2e33'); tx(X(322.5),FW+22,'SİPARİŞ EKRANI 45',5.4,'middle','bold'); tx(X(322.5),FW+30,'dışa asılı 14',4.6,'middle','','#555')
rc(X(KOD[0]),FW,K*(KOD[1]-KOD[0]),K*8,1,0,'#111',None,'#b8bec5'); tx(X(415),FW+18,'KOD 20',5.4,'middle','bold')
for (xx_,lab,c) in ((150,'tezgah','#333'),(322,'sipariş','#1a49b8'),(498,'teslim','#1d7a4f')): ci(X(xx_),FW+K*48,K*12,1,c,'3,2','none'); tx(X(xx_),FW+K*48+3,lab,4.4,'middle','',c)
# SERVICE + koridor
rc(X(SRV[0]),Y(SRV[3]),K*(SRV[1]-SRV[0]),K*(SRV[3]-SRV[2]),1.2,2,'#111',None,'#e4e6ea'); tx(X(242),Y(98)+3,'7 SERVICE 84 × 84',6.2,'middle','bold'); tx(X(242),Y(84)+3,'(kapı öne)',4.8,'middle','','#555')
ln(X(SRV[0]+10),Y(SRV[2]),X(SRV[0]+60),Y(SRV[2]),1.2)
tx(X(50),Y(115)+3,'ELEMAN',5.8,'middle','bold','#555'); tx(X(50),Y(105)+3,'KORİDORU 100',5.8,'middle','bold','#555')
tx(X(360),Y(90)+3,'eleman geçişi',5,'middle','','#888')
# ölçü zincirleri
yb=FW+80
dim(X(0),yb,X(KORX),yb,'koridor 100'); dim(X(KORX),yb,X(520),yb,'HAT 420'); dim(X(520),yb,X(SW),yb,'40'); dim(X(0),yb+18,X(SW),yb+18,'%d'%SW,7)
for (a,b,t) in ((DOOR[0],DOOR[1],'90'),(WIN[0],WIN[1],'80'),(EKR[0],EKR[1],'45'),(KOD[0],KOD[1],'20'),(DOL[0],DOL[1],'124')): dim(X(a),FW+40,X(b),FW+40,t,5.4,'#666')
xr=X(SW)+30
dim(xr,Y(SD),xr,Y(YL0),'hat 84'); dim(xr,Y(YL0),xr,Y(YC0),'robot 90'); dim(xr,Y(YC0),xr,Y(DOL_D),'bacak 94 × 124'); dim(xr,Y(DOL_D),xr,Y(0),'52')
xl=X(0)-30
dim(xl,Y(SD),xl,Y(YC0),'174'); dim(xl,Y(YC0),xl,Y(YW0),'6'); dim(xl,Y(YW0),xl,Y(0),'ön zon 140'); dim(X(0)-52,Y(SD),X(0)-52,Y(0),'%d'%SD,7)
tx(X(SW/2),Y(SD)-12,'ARKA DUVAR',7,'middle','bold','#888')
# ================= SOKAK CEPHESİ (önden) =================
FY=Y(0)+120+K*300; KF=K
FX=lambda x: ox+KF*x; FZ_=lambda z: FY-KF*z
tx(X(-30),FZ_(300)-12,'SOKAK CEPHESİ (önden, kaldırımdan bakış) · duvar boyu 300',9.5,'start','bold')
rc(FX(0),FZ_(300),KF*SW,KF*300,1.6,0,'#111',None,'#dcdcd8')
ln(FX(-40),FZ_(0),FX(SW+40),FZ_(0),2)
rc(FX(DOOR[0]),FZ_(210),KF*90,KF*210,1.2,1,'#111',None,'#eceef1'); tx(FX(50),FZ_(105)+3,'KAPI 90×210',6,'middle','bold'); rc(FX(80),FZ_(105),3,14,0,1,'none',None,'#444')
rc(FX(WIN[0]),FZ_(200),KF*80,KF*100,1.2,1,'#1a49b8',None,'#dbeeff'); tx(FX(150),FZ_(150)+3,'PENCERE 80×100',6,'middle','bold','#1a49b8'); tx(FX(150),FZ_(136)+3,'sürme cam · eşik z 100',4.8,'middle','','#1a49b8'); ln(FX(150),FZ_(200),FX(150),FZ_(100),.8,'#1a49b8')
rc(FX(EKR[0]),FZ_(189),KF*45,KF*104,1.2,1,'#111',None,'#2b2e33'); rc(FX(302.5),FZ_(186),KF*40,KF*71,.8,1,'#666',None,'#111'); tx(FX(322.5),FZ_(150)+3,'32"',6,'middle','bold','#fff'); tx(FX(322.5),FZ_(78)+3,'SİPARİŞ EKRANI',5.4,'middle','bold'); tx(FX(322.5),FZ_(70)+3,'z 85–189',4.8,'middle','','#555')
rc(FX(KOD[0]),FZ_(144),KF*20,KF*34,1.2,1,'#111',None,'#b8bec5'); tx(FX(415),FZ_(102)+3,'KOD',5.4,'middle','bold'); tx(FX(415),FZ_(94)+3,'z 110–144',4.6,'middle','','#555')
rc(FX(DOL[0]),FZ_(165),KF*124,KF*165,1.4,1,'#111',None,'#dfe1e4')
for r in range(6):
    for c in range(2):
        x0=DOL[0]+2+c*60; z0=40+r*20; rc(FX(x0),FZ_(z0+19),KF*58,KF*18,.7,1,'#666',None,'#eceef1'); rc(FX(x0+53),FZ_(z0+13),KF*2,KF*8,.6,1,'#444',None,'#444')
rc(FX(DOL[0]+2),FZ_(40),KF*120,KF*25,.7,0,'#666',None,'#e3f2fb'); tx(FX(498),FZ_(26)+3,'pano (servis kapağı)',5,'middle','','#1a49b8')
tx(FX(498),FZ_(178)+3,'TESLİM DOLABI 124×165 · 12 dolap',6,'middle','bold')
dim(FX(SW)+30,FZ_(0),FX(SW)+30,FZ_(300),'300'); dim(FX(SW)+48,FZ_(0),FX(SW)+48,FZ_(165),'165',5.6,'#666')
for (a,b,t) in ((DOOR[0],DOOR[1],'90'),(WIN[0],WIN[1],'80'),(EKR[0],EKR[1],'45'),(KOD[0],KOD[1],'20'),(DOL[0],DOL[1],'124')): dim(FX(a),FZ_(0)+22,FX(b),FZ_(0)+22,t,5.4,'#666')
dim(FX(0),FZ_(0)+40,FX(SW),FZ_(0)+40,'%d'%SW,7)
# ================= alan tablosu =================
bx=X(SW)+80; by=Y(SD)
rc(bx,by,300,300,1.2,4,'#111',None,'#fff'); tx(bx+12,by+18,'ALANLAR',9.5,'start','bold')
rows=[('hat kabinleri',LINE_D*420/1e4),('robot koridoru + sağ bacak',(COR*SW+(SW-LEGW0)*(YC0-DOL_D))/1e4),('ince duvar',WALL*WLX/1e4+WALL*(YW1-DOL_D)/1e4),('teslim dolabı (ön duvar içi)',124*DOL_D/1e4),('ön zon: koridor, tezgah, SERVICE, eleman',FZ*WLX/1e4),('hat yanı boş (sol 100 + sağ 40)',(100+40)*LINE_D/1e4)]
yy=by+40
for a_,v in rows: tx(bx+12,yy,a_,6.2,'start','','#333'); tx(bx+288,yy,m2(v),6.4,'end','bold'); yy+=14
ln(bx+12,yy-6,bx+288,yy-6,.6,'#999'); tx(bx+12,yy+6,'TOPLAM İÇ',6.8,'start','bold'); tx(bx+288,yy+6,m2(SW*SD/1e4),6.8,'end','bold')
yy=para(bx+12,yy+26,'Ray: arka koridorda düz %d (x 130–%d), sağ uçta R 45 kavis, öne %d bacak (bacak 124 geniş = dolap) → robot y 100'%(RX1-RX0,RX1,RY-R-LEG_Y0)+"'"+'de durur, dolap arkası y 52: 48 cm önde, 12 dolabın hepsi menzilde (130). PACK ve STORE düz raydan.',56,6,'#333')
yy=para(bx+12,yy+2,'Ön zon 140: tezgah 40 + eleman 100. SERVICE 84×84 ince duvara dayalı, kapısı öne. Sol koridor 100: sokak kapısından robot koridoru kapısına (kilitli).',56,6,'#333')
para(bx+12,yy+2,'Müşteri kaldırımdan: sipariş ekranı → kod ünitesi → teslim dolabı, yan yana 2,6 m; tezgah penceresi solda ayrı. Dükkan 5,6 × 3,2 m.',56,6,'#1d7a4f','bold')
tx(W-30,H-8,'AUTOKITCH · arastirma/FULL_MAKINE/dukkan_plani_v3 · 7 Eyl 2026',6.5,'end','','#666')
svg='<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'%(W,H,W,H)+chr(10).join(o)+'</svg>'
xml.dom.minidom.parseString(svg.encode('utf-8'))
out=r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\FULL_MAKINE\dukkan_plani_v3.svg"; io.open(out,'w',encoding='utf-8').write(svg); print('ok')
