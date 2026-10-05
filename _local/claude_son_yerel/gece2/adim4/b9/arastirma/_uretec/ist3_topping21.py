# -*- coding: utf-8 -*-
# TOPPING v21 — Kemal'in ŞEKLİ (simetrik V, helezon ortada) korundu; bant için kabın ön ucunda kısa ÇAPRAZ HELEZON (aynı motor, konik dişli) ağzı 31/39'a taşır
# kat 1 KAŞAR hafta + SUCUK KÜP hafta · kat 2 KAVURMA 3 gün + KUŞBAŞI 3 gün · ALT = kap değişim/çözülme rafı · STORE −18 kesiti aynı paftada
import io, math, xml.dom.minidom
W, H = 1460, 1170
o = []
def esc(s): return str(s).replace('&','&amp;').replace('<','&lt;')
def ln(x1,y1,x2,y2,w=1,c='#111',d=None):
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s stroke-linecap="round"/>' % (x1,y1,x2,y2,c,w,(' stroke-dasharray="%s"'%d) if d else ''))
def rc(x,y,w,h,sw=1,r=0,c='#111',d=None,f='none'):
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,w,h,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def ci(x,y,r,sw=1,c='#111',d=None,f='none'):
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def tx(x,y,s,fs=9,anc='start',fw='',col='#111'):
    o.append('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="%s" font-weight="%s" fill="%s" font-family="Segoe UI, Arial, sans-serif">%s</text>' % (x,y,fs,anc,fw or 'normal',col,esc(s)))
def poly(pts,sw=1,c='#111',f='none',d=None,op=1):
    o.append('<polygon points="%s" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="%s"%s stroke-linejoin="round"/>' % (' '.join('%.1f,%.1f'%p for p in pts),f,op,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def elp(x,y,rx,ry,sw=1,c='#111',f='none',op=1,rot=0):
    o.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="%s" transform="rotate(%g %.1f %.1f)"/>' % (x,y,rx,ry,f,op,c,sw,rot,x,y))
def arr(x1,y1,x2,y2,c='#c0392b',w=1.4):
    ln(x1,y1,x2,y2,w,c); a=math.atan2(y2-y1,x2-x1)
    for s in (1,-1): ln(x2,y2,x2-8*math.cos(a-s*.42),y2-8*math.sin(a-s*.42),w,c)

GRN, RED, BLU, GRY, AMB, PUR = '#1d7a4f', '#c0392b', '#1a49b8', '#666', '#b7791f', '#6b4fa8'
KAS, DIG, PLATE, WALL, LIGHT = '#f3efe4', '#e9eef7', '#dfe7fb', '#d9d9d9', '#f7f6f2'
S=3.0; c30=math.cos(math.radians(30))
X0, Y0 = 70, 120+217*S
def P(x,yb,z): return (X0 + S*(x*c30 + yb*c30), Y0 + S*(x*0.5 - yb*0.5 - z))
def ipoly(pts3,sw=1,c='#111',f='none',d=None,op=1): poly([P(*p) for p in pts3],sw,c,f,d,op)
def iline(p1,p2,w=1,c='#111',d=None): a=P(*p1); b=P(*p2); ln(a[0],a[1],b[0],b[1],w,c,d)

WALLT, YF = 10, 4
# kaplar: (ad, x0, x1, L, H, kat, agiz_x, fill, alt)
def area(Wd,Hh):
    vd=Wd/2-3.5; return (Wd+7)/2*vd + Wd*(Hh-vd)
KAPS = [('KAŞAR',   2,42,70,50,1,31,KAS,'hafta · 50 kg · eleman'),
        ('SUCUK KÜP',44,68,20,50,1,39,DIG,'hafta · 9 kg · eleman'),
        ('KAVURMA', 2,34,15,28,2,31,DIG,'3 gün · 3,3 kg · robot'),
        ('KUŞBAŞI', 36,68,15,28,2,39,DIG,'3 gün · 4 kg · robot')]
VOL = {ad: area(x1-x0,Hh)*L/1000 for (ad,x0,x1,L,Hh,kat,ax,f,alt) in KAPS}
Z = {'alt':(0,58),'b2':(58,72),'k2':(72,103),'b1':(103,117),'k1':(117,170),'tek':(170,197)}
assert Z['tek'][1]==197

o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H))
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,42,'AUTOKITCH — TOPPING v21 (5 Eyl 2026) — SENİN ŞEKLİN: simetrik V, helezon ortada · ağız banda kısa ÇAPRAZ HELEZONLA · kat 1 kaşar + sucuk küp (hafta) · kat 2 kavurma + kuşbaşı (3 gün) · ALT değişim rafı · STORE −18 kesiti',15,'start','bold')
tx(30,66,'Soru 1 cevabı: şekli bant yüzünden değiştirmiştim — tepsi 34 + spiral 14 → ağız yan duvardan ≥ 31 olmalı (x 31-39). Kabın ortası 22 / 56'+chr(39)+'da kalıyor. Çözüm senin şekli bozmadan: helezonun ön ucunda 9-17 cm'+chr(39)+'lik çapraz helezon (konik dişli, aynı motor) malzemeyi banda taşır. Eğimli duvar yok, boru yok.',9.5,'start','','#444')
ln(30,78,W-30,78,.8,'#999')

# ================= İZOMETRİK =================
tx(X0+60,Y0-217*S-14,'İZOMETRİK — dolap içi z 0-175 · 1:3,3',9,'start','bold')
zlo,zhi=0,175
for (a,b) in (((0,0,zlo),(0,0,zhi)),((70,0,zlo),(70,0,zhi)),((0,84,zlo),(0,84,zhi)),((70,84,zlo),(70,84,zhi)),
              ((0,0,zlo),(70,0,zlo)),((0,0,zlo),(0,84,zlo)),((0,0,zhi),(70,0,zhi)),((0,0,zhi),(0,84,zhi)),((70,0,zhi),(70,84,zhi)),((0,84,zhi),(70,84,zhi)),((70,0,zlo),(70,84,zlo))):
    iline(a,b,.7,'#bbb')
ipoly([(0,84-WALLT,zlo),(70,84-WALLT,zlo),(70,84-WALLT,zhi),(0,84-WALLT,zhi)],1,'#555',WALL,None,.9)
ipoly([(0,84-WALLT,zhi),(70,84-WALLT,zhi),(70,84,zhi),(0,84,zhi)],1,'#555','#c8c8c8',None,.9)
ipoly([(70,84-WALLT,zlo),(70,84,zlo),(70,84,zhi),(70,84-WALLT,zhi)],1,'#555','#cfcfcf',None,.9)
def motor(x,zf):
    ipoly([(x-3,84-WALLT+1,zf),(x+3,84-WALLT+1,zf),(x+3,84-WALLT+8,zf),(x-3,84-WALLT+8,zf)],.9,BLU,'#dfe7fb','3,2',.9)
    ipoly([(x-3,84-WALLT+1,zf+7),(x+3,84-WALLT+1,zf+7),(x+3,84-WALLT+8,zf+7),(x-3,84-WALLT+8,zf+7)],.9,BLU,'#dfe7fb','3,2',.9)
    iline((x-3,84-WALLT+1,zf),(x-3,84-WALLT+1,zf+7),.9,BLU,'3,2'); iline((x+3,84-WALLT+1,zf),(x+3,84-WALLT+1,zf+7),.9,BLU,'3,2')
for (ad,x0,x1,L,Hh,kat,ax,f,alt) in KAPS: motor((x0+x1)/2, Z['k%d'%kat][0])
# plakalar
for z in (Z['k2'][0],Z['k1'][0]):
    ipoly([(0,0,z),(70,0,z),(70,84-WALLT,z),(0,84-WALLT,z)],1.2,BLU,PLATE,None,.85)
    ipoly([(0,0,z-2),(70,0,z-2),(70,0,z),(0,0,z)],1,BLU,'#c9d6f5',None,.9)
    ipoly([(70,0,z-2),(70,84-WALLT,z-2),(70,84-WALLT,z),(70,0,z)],1,BLU,'#c9d6f5',None,.9)
# ALT raf: 2 sıra × 2 yuva (28 yüksek), küçük kaplar (çözülme + park)
ipoly([(0,0,29),(70,0,29),(70,84-WALLT,29),(0,84-WALLT,29)],.9,'#999','#ececec',None,.8)
for (x0,zf,lab,dash) in ((2,30,'kav. çözülme',None),(36,30,'kuş. çözülme',None),(2,1,'boş / park',True),(36,1,'boş / park',True)):
    col='#999' if dash else '#333'
    for (yb0,yb1) in ((YF,YF+15),):
        ipoly([(x0,yb0,zf),(x0+32,yb0,zf),(x0+32,yb0,zf+26),(x0,yb0,zf+26)],.9,col,LIGHT,'3,2' if dash else None,.85)
        ipoly([(x0,yb0,zf+26),(x0+32,yb0,zf+26),(x0+32,yb1,zf+26),(x0,yb1,zf+26)],.8,col,LIGHT,'3,2' if dash else None,.7)
        ipoly([(x0+32,yb0,zf),(x0+32,yb1,zf),(x0+32,yb1,zf+26),(x0+32,yb0,zf+26)],.8,col,'#ebe9e2','3,2' if dash else None,.8)
    t=P(x0+16,yb0+2,zf+13); tx(t[0],t[1],lab,5.6,'middle','bold','#666' if dash else '#333')
t=P(0,-2,50); tx(t[0]-6,t[1]+8,'ALT 58: değişim rafı — 2 sıra × 2 yuva (28)',6.5,'end','bold',GRY)

def kap(ad,x0,x1,yb0,L,zf,Hh,ax,fill,alt):
    Wd=x1-x0; vd=Wd/2-3.5; xc=(x0+x1)/2
    front=[(x0,yb0,zf+vd),(x0,yb0,zf+Hh),(x1,yb0,zf+Hh),(x1,yb0,zf+vd),(xc+3.5,yb0,zf),(xc-3.5,yb0,zf)]
    back=[(x,yb0+L,z) for (x,_,z) in front]
    ipoly(back,1,'#333',fill,None,.95)
    n=len(front)
    for i in range(n):
        a,b=front[i],front[(i+1)%n]; a2,b2=back[i],back[(i+1)%n]
        ipoly([a,b,b2,a2],.9,'#333',fill,None,.9)
    # helezon ortada (yeşil), tarak ortada (mor)
    iline((xc,yb0+1,zf+3.5),(xc,yb0+L-1,zf+3.5),2.2,GRN)
    for k in range(max(3,int(L/3.5))):
        y=yb0+2+k*3.5
        if y>yb0+L-2: break
        iline((xc-3,y,zf+1),(xc+3,y,zf+6),1.2,GRN)
    zt_=min(vd,Hh-6)+1
    iline((xc,yb0+1,zf+zt_),(xc,yb0+L-1,zf+zt_),1.6,PUR)
    for k in range(max(3,int(L/3.5))):
        y=yb0+2.5+k*3.5
        if y>yb0+L-2: break
        s=1 if k%2==0 else -1; iline((xc,y,zf+zt_),(xc,y,zf+zt_+s*5),1,PUR)
    # ÇAPRAZ HELEZON: ön uçta, xc → ax, z 3.5 (kabın içinde, ön 5 cm)
    ipoly([(xc,yb0+0.5,zf+0.5),(ax,yb0+0.5,zf+0.5),(ax,yb0+0.5,zf+6.5),(xc,yb0+0.5,zf+6.5)],.8,AMB,'#fff3d6',None,.9)
    iline((xc,yb0+2.5,zf+3.5),(ax,yb0+2.5,zf+3.5),2.2,AMB)
    nt=max(2,int(abs(ax-xc)/2.5))
    for k in range(nt):
        xx=xc+(ax-xc)*(k+0.5)/nt; iline((xx,yb0+1,zf+1.5),(xx,yb0+4,zf+5.5),1,AMB)
    cpt=P(xc,yb0+2.5,zf+3.5); ci(cpt[0],cpt[1],3.2,1,'#555','#eee')
    # üst + ön yüz yarı saydam
    ipoly([front[1],front[2],back[2],back[1]],1,'#333',fill,None,.55)
    ipoly(front,1.3,'#111',fill,None,.5)
    # ağız (ax, ön, plakadan aşağı 7)
    ipoly([(ax-2.5,yb0+1,zf-7),(ax+2.5,yb0+1,zf-7),(ax+2.5,yb0+5,zf-7),(ax-2.5,yb0+5,zf-7)],1,GRN,'#eaf6ee')
    for (dx,dy) in ((-2.5,1),(2.5,1),(2.5,5),(-2.5,5)): iline((ax+dx,yb0+dy,zf),(ax+dx,yb0+dy,zf-7),1,GRN)
    a=P(ax,yb0+3,zf-7); arr(a[0],a[1]+2,a[0],a[1]+16,GRN,1.4)
    if yb0+L < 84-WALLT-1: iline((xc,yb0+L,zf+3.5),(xc,84-WALLT,zf+3.5),1.2,BLU,'4,3')
    ipoly([(xc-2,yb0+L,zf+1.5),(xc+2,yb0+L,zf+1.5),(xc+2,yb0+L+2,zf+1.5),(xc-2,yb0+L+2,zf+1.5)],.9,BLU,'#dfe7fb')
    t=P(xc,yb0+L*0.55,zf+Hh+3); tx(t[0],t[1]-4,ad,8.5,'middle','bold'); tx(t[0],t[1]+6,'%g×%g×%g · %.0f L · %s' % (Wd,L,Hh,VOL[ad],alt),5.8,'middle','','#333')
for (ad,x0,x1,L,Hh,kat,ax,f,alt) in KAPS: kap(ad,x0,x1,YF,L,Z['k%d'%kat][0],Hh,ax,f,alt)
for (z,x) in ((Z['b1'][0]+3,31),(Z['b2'][0]+3,31)):
    cpt=P(x,YF+10,z); elp(cpt[0],cpt[1],17*S*0.95,17*S*0.5,1.2,BLU,'#dfe7fb',.9,-30)
    cpt2=P(x+17,YF+10,z); tx(cpt2[0]+12,cpt2[1],'tepsi Ø34',6,'start','',BLU)
ipoly([(0,0,Z['tek'][0]),(70,0,Z['tek'][0]),(70,84-WALLT,Z['tek'][0]),(0,84-WALLT,Z['tek'][0])],.8,'#999','#f3f3f3',None,.5)
t=P(35,40,Z['tek'][0]+3); tx(t[0],t[1],'teknik 27 ↑',6.5,'middle','',GRY)
a=P(-6,-4,Z['k2'][0]+14); arr(a[0]-40,a[1]+24,a[0],a[1],AMB,1.6); tx(a[0]-44,a[1]+36,'ÖN (robot)',8,'middle','bold',AMB)
t=P(70,84-WALLT/2,zhi+4); tx(t[0]+6,t[1],'ARKA DUVAR 10 — motorlar içinde',7.5,'start','bold',BLU)
lx,ly=X0+300,Y0-217*S+8
for i,(col,lab) in enumerate(((GRN,'dozaj helezonu (ortada)'),(PUR,'tarak (ortada)'),(AMB,'çapraz helezon → ağız (ön uç, kabın içinde)'),(BLU,'kavrama / ara mil / motor'))):
    ln(lx,ly+i*13,lx+18,ly+i*13,2.2,col); tx(lx+24,ly+i*13+3,lab,6.5,'start','','#333')

# ================= KAP DETAYI (soru 1) =================
XD,YD = 560,100
rc(XD,YD,360,300,1.3,3,'#999',None,'#fcfdff')
tx(XD+180,YD+16,'KAP DETAYI — senin şeklin + çapraz helezon (kaşar 40×70×50)',7.5,'middle','bold')
K=2.2
fx,fy = XD+22, YD+40
Wd,Hh,vd = 40,50,16.5
Zf=lambda c: fy+K*(Hh-c); Xf=lambda c: fx+K*c
poly([(Xf(0),Zf(vd)),(Xf(0),Zf(Hh)),(Xf(Wd),Zf(Hh)),(Xf(Wd),Zf(vd)),(Xf(Wd/2+3.5),Zf(0)),(Xf(Wd/2-3.5),Zf(0))],1.2,'#111',KAS)
ci(Xf(Wd/2),Zf(3.5),K*3.5,1.1,GRN,'#fff'); ci(Xf(Wd/2),Zf(14),K*6,1,PUR,'none'); ci(Xf(Wd/2),Zf(14),K*.7,1,PUR,'#efeaf8')
for a_ in (0,120,240):
    a=math.radians(a_); ln(Xf(Wd/2),Zf(14),Xf(Wd/2)+K*6*math.cos(a),Zf(14)-K*6*math.sin(a),1.2,PUR)
tx(Xf(Wd/2),fy-4,'ÖN KESİT — simetrik V, her şey ortada',6,'middle','bold',GRY)
tx(Xf(3),Zf(vd/2+2),'45°',5,'start','bold',AMB); tx(Xf(Wd-3),Zf(vd/2+2),'45°',5,'end','bold',AMB)
tx(Xf(Wd/2)+K*8,Zf(3.5)+3,'helezon',5,'start','bold',GRN); tx(Xf(Wd/2)+K*8,Zf(14)+3,'tarak Ø12',5,'start','bold',PUR)
tx(Xf(Wd/2),Zf(38),'depo',5,'middle','','#333')
ln(Xf(0),Zf(-4),Xf(Wd),Zf(-4),.7); tx(Xf(Wd/2),Zf(-6),'40',5.5,'middle','bold'); tx(Xf(Wd)+6,Zf(25),'50',5.5,'start','bold')
# üst görünüş: helezon y boyunca, ön uçta çapraz helezon → ağız x 31
ux,uy = XD+150, YD+40
KU=1.35
Lk=70
rc(ux,uy,KU*Wd,KU*Lk,1.2,1,'#111',None,KAS)
ln(ux+KU*Wd/2,uy+KU*2,ux+KU*Wd/2,uy+KU*(Lk-6),1.8,GRN)
ln(ux+KU*Wd/2,uy+KU*3,ux+KU*Wd/2,uy+KU*(Lk-7),1.2,PUR)
for k in range(9):
    yy=uy+KU*(5+k*7); s=1 if k%2==0 else -1; ln(ux+KU*Wd/2,yy,ux+KU*(Wd/2+s*6),yy,.9,PUR)
rc(ux+KU*(Wd/2-3.5),uy+KU*(Lk-6),KU*(29-(Wd/2-3.5)+3.5+2),KU*5,1,1,AMB,None,'#fff3d6')
ln(ux+KU*Wd/2,uy+KU*(Lk-3.5),ux+KU*29,uy+KU*(Lk-3.5),2,AMB)
ci(ux+KU*Wd/2,uy+KU*(Lk-3.5),3,1,'#555','#eee'); ci(ux+KU*29,uy+KU*(Lk-3.5),3,1.4,GRN,'#fff')
rc(ux+KU*(Wd/2-2),uy-6,KU*4,6,1.1,1,BLU,None,'#dfe7fb')
tx(ux+KU*Wd/2,uy-12,'ÜST — kavrama arkada',6,'middle','bold',GRY)
tx(ux+KU*Wd+6,uy+KU*(Lk-3.5)+3,'ağız x 31 (bant)',5.2,'start','bold',GRN)
tx(ux+KU*Wd+6,uy+KU*(Lk-12),'çapraz helezon 9',5.2,'start','bold',AMB); tx(ux+KU*Wd+6,uy+KU*(Lk-19),'konik dişli, aynı motor',5,'start','',AMB)
tx(ux+KU*Wd+6,uy+KU*30,'helezon + tarak ortada',5,'start','',GRY)
tx(ux-6,uy+KU*4,'ARKA',4.8,'end','',GRY); tx(ux-6,uy+KU*Lk,'ÖN',4.8,'end','',GRY)
ny=YD+205
for i,(s,c) in enumerate([('Kabın ortası x 22 (sol) / 56 (sağ); bant 31-39. Fark 9 / 17 cm → ön uçtaki çapraz helezon taşır.','#333'),
                          ('Çapraz helezon kabın içinde (ön 5 cm), kapla birlikte çıkar-yıkanır; eğim yok, boru yok, yapışma yok.',GRN),
                          ('Sucuk küp 56 → 39: 17 cm · kavurma 18 → 31: 13 · kuşbaşı 52 → 39: 13 · kaşar 22 → 31: 9','#333'),
                          ('Alternatif (v20): eğimli tek duvar, çapraz helezon yok — ama senin şeklin değil. Karar senin.',GRY)]):
    tx(XD+12,ny+i*13,s,5.8,'start','bold' if i==1 else '',c)
tx(XD+12,ny+60,'Kesit alanı: (W+7)/2 × (W/2−3,5) + W × (H − W/2 + 3,5) → hacim = alan × boy',5.6,'start','',GRY)
tx(XD+12,ny+73,'Ağız yan duvardan 31: tepsi R17 + spiral R14 → süpürme duvarın içinde kalır (sol x 0-62, sağ 8-70)',5.6,'start','',GRY)

# ================= ÖN KESİT (dolap) =================
XC,YC = 560,420
tx(XC+88,YC-6,'ÖN KESİT 1:4',8.5,'middle','bold')
K=2.5
rc(XC,YC,K*70,K*197,1.8)
for ad,(z0,z1),col in (('teknik',Z['tek'],'#f3f3f3'),('KAT 1',Z['k1'],'#fff'),('boşluk 1',Z['b1'],'#eef3ff'),('KAT 2',Z['k2'],'#fff'),('boşluk 2',Z['b2'],'#eef3ff'),('ALT',Z['alt'],'#f7f6f2')):
    rc(XC,YC+K*(197-z1),K*70,K*(z1-z0),.7,0,'#111',None,col); tx(XC+K*70+4,YC+K*(197-(z0+z1)/2)+3,'%s %g'%(ad,z1-z0),5.4,'start','',GRY)
for (ad,x0,x1,L,Hh,kat,ax,f,alt) in KAPS:
    zf=Z['k%d'%kat][0]; Zc=lambda c: YC+K*(197-zf-c); Wd=x1-x0; vd=Wd/2-3.5; xc=(x0+x1)/2
    poly([(XC+K*x0,Zc(vd)),(XC+K*x0,Zc(Hh)),(XC+K*x1,Zc(Hh)),(XC+K*x1,Zc(vd)),(XC+K*(xc+3.5),Zc(0)),(XC+K*(xc-3.5),Zc(0))],1.1,'#111',f)
    ci(XC+K*xc,Zc(3.5),K*3.5,1,GRN,'#fff'); ci(XC+K*xc,Zc(min(vd,Hh-6)+1),K*5.5,.8,PUR,'none','3,2')
    ln(XC+K*xc,Zc(3.5),XC+K*ax,Zc(3.5),2,AMB); ln(XC+K*ax,Zc(0),XC+K*ax,Zc(-6),1.6,GRN)
    tx(XC+K*xc,Zc(Hh-7),ad,5.6,'middle','bold'); tx(XC+K*xc,Zc(Hh-13),'%.0f L' % VOL[ad],5,'middle','','#333')
for z in (Z['b1'][0]+3,Z['b2'][0]+3):
    o.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#dfe7fb" stroke="%s" stroke-width="1"/>' % (XC+K*35,YC+K*(197-z),K*17,K*1.2,BLU))
for (x0,z0,lab,dash) in ((2,30,'kav. çözülme',None),(36,30,'kuş. çözülme',None),(2,1,'boş / park','3,2'),(36,1,'boş / park','3,2')):
    rc(XC+K*x0,YC+K*(197-z0-26),K*32,K*26,.9,1,'#999' if dash else '#333',dash,LIGHT); tx(XC+K*(x0+16),YC+K*(197-z0-12),lab,5,'middle','','#666' if dash else '#333')
tx(XC+K*35,YC+K*197+14,'70',7,'middle','bold'); tx(XC+K*35,YC+K*197+26,'27+53+14+31+14+58 = 197 ✓',6.5,'middle','bold',GRN)
tx(XC+K*35,YC+K*197+38,'tepsi düzlemleri 105 / 60 cm',6,'middle','',BLU)

# ================= STORE −18 KESİTİ (soru 3) =================
XS,YS = 960,100
rc(XS,YS,470,300,1.3,3,'#999',None,'#fcfbf8')
tx(XS+235,YS+16,'STORE −18 KASET ÇEKMECESİ — kavurma/kuşbaşı kapları sığıyor mu?',7.5,'middle','bold')
KS=2.0
# STORE dikey konumu (kucuk): 185 dikey, -18 band alt: hamur 10+10, kaset cekmecesi 29
sx,sy = XS+16, YS+30
rc(sx,sy,KS*70,KS*185,1.1);
for (z0,h,lab,col) in ((0,2,'',''),(2,28,'soğutma 28','#f3f3f3'),(30,6,'','#ddd'),(36,84,'+3 bölge 84','#fff'),(120,8,'ayırıcı','#e9e4d6'),(128,10,'hamur 10','#e3f2fb'),(138,10,'hamur 10','#e3f2fb'),(148,29,'KASET ÇEKMECESİ 29','#dbeafe'),(177,8,'','#e9e4d6')):
    rc(sx,sy+KS*z0,KS*70,KS*h,.6,0,'#111',None,col if col else '#fff')
    if lab: tx(sx+KS*35,sy+KS*(z0+h/2)+2,lab,4.6,'middle','bold' if 'KASET' in lab else '','#111')
tx(sx+KS*35,sy+KS*185+10,'STORE v4 (sol modül 61) — dikey konum',5,'middle','',GRY)
# cekmece on gorunusu: 61 modül (iç 59,5) × 29 yükseklik, kaplar 32×15×28 döndürülmüş (15 en) → 3 adet
dx,dy = XS+190, YS+40
KD=2.6
rc(dx,dy,KD*61,KD*29,1.4,1,'#111',None,'#dbeafe')
rc(dx+KD*0.75,dy+KD*0.5,KD*59.5,KD*28,.8,0,'#555','3,2','none')
for k in range(3):
    rc(dx+KD*(1.5+k*16),dy+KD*0.8,KD*15,KD*28,1.1,1,'#111',None,DIG); tx(dx+KD*(9+k*16),dy+KD*15,'kav.' if k<2 else 'boş',5.4,'middle','bold'); tx(dx+KD*(9+k*16),dy+KD*20,'32×15×28',4.2,'middle','','#333')
tx(dx+KD*30.5,dy-6,'ÖN — kavurma modülü 61 × 29 (iç 59,5 × 28)',6,'middle','bold',GRY)
ln(dx,dy+KD*29+10,dx+KD*61,dy+KD*29+10,.7); tx(dx+KD*30.5,dy+KD*29+8,'61 (3 × 15 = 45 ≤ 59,5 ✓)',5.4,'middle','bold',GRN)
ln(dx+KD*61+8,dy,dx+KD*61+8,dy+KD*29,.7); tx(dx+KD*61+12,dy+KD*15,'29 (28 ✓ pay 1)',5.4,'start','bold',GRN)
# ust gorunus cekmece: derinlik 65 (ic 59,5), kaplar 32 derin → 1 sıra
tx(dx+KD*30.5,dy+KD*29+34,'ÜST — çekmece 61 × 65: kap 32 derin → 1 sıra, 3 yan yana',6,'middle','bold',GRY)
uy2=dy+KD*29+42
rc(dx,uy2,KD*61,KD*40,1.2,1,'#111',None,'#dbeafe')
for k in range(3):
    rc(dx+KD*(1.5+k*16),uy2+KD*3,KD*15,KD*32*0.6,1,1,'#111',None,DIG)
tx(dx+KD*30.5,uy2+KD*32,'(derinlik 1:1,67 kısaltıldı) · 2. sıra sığmaz (64 > 59,5)',4.6,'middle','',GRY)
ny=YS+232
for i,(s,c) in enumerate([('İki modül: sol KAVURMA ×2 (+1 boş yuva) · sağ KUŞBAŞI ×2 (+1) → haftalık 2+2 donmuş yedek sığar ✓',GRN),
                          ('Kap 32×15×28: STORE çekmecesine döndürülüp (15 en) girer; 28 ≤ 29 → pay 1 cm — çekmece 31 önerilir (STORE v5)',AMB),
                          ('Akış: eleman haftalık donmuş 4 kabı STORE −18'+chr(39)+'e koyar → robot 1 gün önce TOPPING ALT çözülme yuvasına → 3. gün öne',BLU),
                          ('ALT 58 (TOPPING): üst sıra çözülme ×2, alt sıra boş/park ×2 — "1 haftalık değişim için kapların yeri"','#333')]):
    tx(XS+12,ny+i*13,s,5.8,'start','bold' if i==0 else '',c)

# ================= TABLO =================
XT,YT = 960,420
rc(XT,YT,470,540,1.4,4)
tx(XT+14,YT+22,'DÖRT KAP — soru 2: sucuk & kaşar hafta, kavurma & kuşbaşı 3 gün',10,'start','bold')
hdr=['kap','en×boy×yük','hacim','dolum','gün','kim']
cx_=[XT+14,XT+92,XT+190,XT+248,XT+320,XT+380]
for i,h in enumerate(hdr): tx(cx_[i],YT+46,h,6.6,'start','bold',GRY)
ln(XT+12,YT+52,XT+458,YT+52,.8,'#bbb')
rows=[('KAŞAR','40 × 70 × 50','%.0f L' % VOL['KAŞAR'],'50 kg','7,6 hafta','eleman'),
      ('SUCUK KÜP','24 × 20 × 50','%.0f L' % VOL['SUCUK KÜP'],'9,2 kg','7 hafta','eleman'),
      ('KAVURMA','32 × 15 × 28','%.0f L' % VOL['KAVURMA'],'3,3 kg','3','robot'),
      ('KUŞBAŞI','32 × 15 × 28','%.0f L' % VOL['KUŞBAŞI'],'4 kg','3','robot')]
for i,r in enumerate(rows):
    yy=YT+70+i*18
    for j,v in enumerate(r): tx(cx_[j],yy,v,6.4,'start','bold' if j==0 else '','#111' if j==0 else '#333')
ln(XT+12,YT+146,XT+458,YT+146,.8,'#bbb')
notes=[('KAŞAR hafta: 45,5 kg + pay → 50 kg = 122 L → en 40 (kat 1'+chr(39)+'de sucukla 40+24+6 = 70), boy 70, yük 50.',GRN,'bold'),
       ('SUCUK hafta: 8,4 kg küp (0,55 kg/L) = 15 L + pay → 24 × 20 × 50 = 23 L (%75). Aynı yükseklik, kısa boy.','#333',''),
       ('KAVURMA / KUŞBAŞI 3 gün: 6 / 7,3 L → 32 × 15 × 28 = 11 L (%54 / %66). Robot taşır: dolu 7-8 kg ✓',GRN,'bold'),
       ('Kat 1 = haftalık ikili (eleman), kat 2 = 3 günlük ikili (robot) — senin 2. maddene göre yer değişti.','#333',''),
       ('Ağırlık: kaşar dolu 66 kg (kap 16) → rayda çekilir, yerinde doldurulur · sucuk 15 kg · küçükler ≤ 8 kg','#333',''),
       ('Dikey: teknik 27 · kat 1 53 · boşluk 14 · kat 2 31 · boşluk 14 · ALT 58 = 197 ✓ · derinlik 4 + 70 + 10 = 84 ✓',GRN,''),
       ('Çapraz helezon: Ø5, 9-17 cm, konik dişli ile ana helezondan; kap içinde, sökülmez; +1 konik + 1 kısa vida / kap',AMB,''),
       ('Kesit simetrik: helezon ortada, tarak ortada — senin krokin. Eğimli tek duvar (v20) iptal, çapraz helezon onun yerine.',AMB,'bold'),
       ('STORE −18: 28 ≤ 29 sığar (pay 1); 2+2 donmuş + 2 boş yuva. ALT: çözülme ×2 + park ×2.','#333',''),
       ('AÇIK: kaşar 45° simetrik V + tarak akış prototipi · çapraz helezon kaşarda sıkıştırma testi · çekmece 29 → 31',AMB,'')]
for i,(s,c,fw) in enumerate(notes): tx(XT+14,YT+164+i*17,s,6.1,'start',fw,c)
tx(XT+14,YT+350,'Robot: kat 2 iki kap, 3 günde 1 (2 hamle: boş → ALT park, ALT çözülmüş → kat 2) · Eleman haftalık: kaşar + sucuk doldurur,',6,'start','','#333')
tx(XT+14,YT+363,'STORE −18'+chr(39)+'e 4 donmuş kap koyar, parktaki boşları alır. Kavurmalı/kuşbaşılı pide: kat 2 → kat 1 (kaşar) +5 sn.',6,'start','','#333')
tx(XT+14,YT+383,'Sonraki: HAT v45 (TOPPING v21) · STORE v5 (çekmece 31) · kaşar prototip listesi',6.2,'start','bold',GRY)
tx(W-40,H-12,'AUTOKITCH · arastirma/3_TOPPING/ist3_topping_detay_v21 · 5 Eyl 2026',7,'end','',GRY)
o.append('</svg>')
svg = chr(10).join(o)
xml.dom.minidom.parseString(svg.encode('utf-8'))
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\ist3_topping_detay_v21.svg"
io.open(out,'w',encoding='utf-8').write(svg)
print('yazildi + XML gecerli | ' + ' · '.join('%s %.0f L' % (k,v) for k,v in VOL.items()))
